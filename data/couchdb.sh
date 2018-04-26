#!/bin/bash

echo -- Pull Docker image
docker pull couchdb:2.1.1

echo -- Set node IP addresses, electing the first as master node and admin credentials
export nodes=(172.17.0.2 172.17.0.3 172.17.0.4)
export masternode=`echo ${nodes} | cut -f1 -d' '`
export othernodes=`echo ${nodes[*]} | sed s/${masternode}//`
export size=${#nodes[*]}
export user=admin
export pass=admin
echo nodes ${nodes[*]}
echo masternode $masternode
echo othernodes $othernodes
echo size $size
echo user $user
echo pass $admin

echo -- Create Docker containers
for node in ${nodes[*]}}; do docker create couchdb:2.1.1 -–ip=${node}; done

echo -- Put in conts the Docker container IDs
declare -a conts=(`docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)

echo -- Start the containers
for cont in "${conts[*]}"; do docker start ${cont}; done
sleep 3

echo -- Write the cookie name and node name to the CouchDB configuration on every node
for (( i=0; i<${size}; i++ )); do
    docker exec ${conts[${i}]} \
      bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"
    docker exec ${conts[${i}]} \
      bash -c "echo \"-name couchdb@${nodes[${i}]}\" >> /opt/couchdb/etc/vm.args"
done

echo -- Restart containers to pick-up changes to CouchDB configurations
for cont in "${conts[*]}"; do docker restart ${cont}; done
sleep 3
for node in "${nodes[*]}"; do
    curl -XPUT "http://${node}:5984/_node/_local/_config/admins/${user}" --data "\"${pass}\""
    curl -XPUT "http://${user}:${pass}@${node}:5984/_node/couchdb@${node}/_config/chttpd/bind_address" --data '"0.0.0.0"'
done
for node in "${nodes[*]}"; do
    curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup" \
      --header "Content-Type: application/json" \
      --data "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\", \
        \"username\": \"${user}\", \"password\":\"${pass}\", \"port\": \"5984\", \
        \"remote_node\": \"${node}\", \
        \"remote_current_user\":\"${user}\", \"remote_current_password\":\"${pass}\"}"
done
for node in "${nodes[*]}"; do
    curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup" \
      --header "Content-Type: application/json" \
      --data "{\"action\": \"add_node\", \"host\":\"${node}\", \
        \"port\": \"5984\", \"username\": \"${user}\", \"password\":\"${pass}\"}"
done
curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup" \
    --header "Content-Type: application/json" --data "{\"action\": \"finish_cluster\"}"
rev=`curl -XGET "http://172.17.0.2:5986/_nodes/nonode@nohost" --user "${user}:${pass}" | sed -e 's/[{}"]//g' | cut -f3 -d:`
curl -X DELETE "http://172.17.0.2:5986/_nodes/nonode@nohost?rev=${rev}"  --user "${user}:${pass}"

echo -- Check the correct cluster configuration
for node in "${nodes[*]}"; do  curl -X GET "http://${user}:${pass}@${node}:5984/_membership"; done

echo -- Adding a database to one node of the cluster cause it to be created on all other nodes as well
curl -XPUT "http://${user}:${pass}@${masternode}:5984/twitter"
for node in "${nodes[*]}"; do  curl -X GET "http://${user}:${pass}@${node}:5984/_all_dbs"; done

echo -- Put in conts the Docker container IDs
declare -a conts=(`docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)

echo -- Starts the cluster
for cont in "${conts[*]}"; do docker start ${cont}; done
sleep 3

echo -- Shutdowns the cluster nicely
for cont in "${conts[*]}"; do docker stop ${cont}; done

echo -- Deletes the cluster containers
for cont in "${conts[*]}"; do docker rm --force ${cont}; done

echo -- Add Twitter data
curl -XPOST "http://${user}:${pass}@${masternode}:5984/twitter/_bulk_docs " --header "Content-Type: application/json" \
  --data @./twitter/data.json

echo -- Add a design document with MapReduce Views, Lists and Shows functions
grunt couch-compile
grunt couch-push

echo -- Request a MapReduce View
curl -XGET "http://${user}:${pass}@${masternode}:5984/twitter/_design/language/_view/language?reduce=true&group_level=2"

echo -- Request a show function returning HTML
docid=`curl -XGET "http://${masternode}:5984/twitter/_all_docs?limit=1" | jq '.rows[].id' | sed 's/"//g'`
curl -XGET "http://${user}:${pass}@${masternode}:5984/twitter/_design/language/_show/html/${docid}"

echo -- Request a list function returning HTML
curl -XGET "http://${user}:${pass}@${masternode}:5984/twitter/_design/language/_list/html/language?reduce=true&group_level=2"

echo -- Request a list function returning GeoJSON
curl -XGET "http://${user}:${pass}@${masternode}:5984/twitter/_design/language/_list/geojson/language?reduce=false&include_docs=true" | jq '.' > /tmp/twitter.geojson"
echo You can now load the GeoJSON in a text editor, or display them on a map using QGIS

echo -- Mango query request
curl -XPOST "http://${user}:${pass}@${masternode}:5984/twitter/_find" \
--header "Content-Type: application/json" --data '{
   "fields" : ["_id", "text", "user.screen_name"],
   "selector": {
      "user.lang": {"$eq": "ja"}
   }
}'  | jq '.' -M

echo -- Mango query explanation (use of indexes, or lack there-of, etc)
curl -XPOST "http://${user}:${pass}@${masternode}:5984/twitter/_explain" \
--header "Content-Type: application/json" --data '{
   "fields" : ["_id", "text", "user.screen_name"],
   "selector": {
      "user.lang": {"$eq": "ja"}
   }
}'  | jq '.' -M

echo -- More complex Mango query, with tweets sorted by screen_name (it should fail, because no index has been defined for the sort field)
curl -XPOST "http://${user}:${pass}@${masternode}:5984/twitter/_find" --header "Content-Type: application/json" --data '{
   "fields" : ["_id", "user.lang", "user.screen_name", "text"],
   "selector": {
      "$and": [
        {"user.lang": {"$eq": "en"}},
        {"user.screen_name": {"$gt": "pin"}}
      ]
   },
   "sort": [{"user.screen_name": "asc"}]
}' | jq '.' -M

echo -- Create index for lang and screen_name, hence the above query runs faster, but, still, it cannot sort by screen_name, since this index order documents for the combination of lang and screen_name, not for either field taken in isolation (same as SQL DBSMes)
curl -XPOST "http://${user}:${pass}@${masternode}:5984/twitter/_index" \
--header "Content-Type: application/json" --data '{
   "ddoc": "indexes",
   "index": {
      "fields": ["user.lang", "user.screen_name"]
   },
   "name": "lang-screen-index",
   "type": "json"
}'

echo -- Create index for just the screen_name, now the query above should work
curl -XPOST "http://${user}:${pass}@${masternode}:5984/twitter/_index" \
--header "Content-Type: application/json" --data '{
   "ddoc": "indexes",
   "index": {
      "fields": ["user.screen_name"]
   },
   "name": "screen-index",
   "type": "json"
}'

echo -- Get the list of indexes
curl -XGET "http://${user}:${pass}@${masternode}:5984/twitter/_index" | jq '.' -M

echo -- (Partial indexes selextor may be used to exclude some documents from indexing, in order to speed up indexing) Indexes can be deleted as usual
curl -XDELETE "http://${user}:${pass}@${masternode}:5984/twitter/_index/indexes/json/lang-screen-index"

echo -- Index by location (works only for points, unfortunately)
curl -XPOST "http://${user}:${pass}@${masternode}:5984/twitter/_index" \
--header "Content-Type: application/json" --data '{
   "ddoc": "indexes",
   "index": {
      "fields": ["coordinates.coordinates"]
   },
   "name": "coordinates",
   "type": "json"
}'

echo -- Query data by their location (the index is now built, analogously to the MapReduce views)
curl -XPOST "http://${user}:${pass}@${masternode}:5984/twitter/_find" --header "Content-Type: application/json" --data '{
   "fields" : ["_id", "user.lang", "user.screen_name", "text", "created_at", "coordinates"],
   "selector": {
      "$and": [
        {"coordinates.coordinates": {"$gt": [100, -31]}},
        {"coordinates.coordinates": {"$lt": [116, -33]}}
      ]
   }
}' | jq '.' -M
