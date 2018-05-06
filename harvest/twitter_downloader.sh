#!/bin/bash

# Twitter data
# Tweets can be extracted with the following HTTP requests.
# This is to extract geocoded tweets; the key is the geohash (whose value can be gotten from ),
# and http://geohash.gofreerange.com/ year-month-day,
# while the skip and limit requests parameters can be used to page results
# (there are about 36M tweets, increasing by a million every two days or so):
curl -XGET "http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/geoindex?include_docs=true&reduce=  --user "readonly:ween7ighai9gahR6"false&skip=0&limit=5"

# This is to extract all tweets (geocoded or not),
# the skip and limit request parameters can be used to page through the results just as above (key is city, year, month, and day):
curl -XGET "http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary?include_docs=true&reduce=f --user "readonly:ween7ighai9gahR6" alse&skip=0&limit=5"

# This is to extract GeoJSON, ready to be viewed in a GIS, limited to an area around Melbourne ("r1r1" geohash), starting from 2014 and ending in 2017:
curl -XGET " n/twitter/\ http://45.113.232.90/couchdbro/twitter/_design/twitter/_list/geojson/geoindex?reduce=false&start_key=\[\"r1r0\",2014,1,1\]\&end_key=\[\"r1r1\",2017,12,31\]&skip=0&limit=5" --user "readonly:ween7ighai9gahR6"

# To aggregate tweets by city, the "summary" view can be used:
curl -XGET "http://45.113.232.90/couchdbro/twitter/_desig n/twitter/_view/summary?include_docs=false&reduce=true&group_level=1&skip=0&limi t=5" --user "readonly:ween7ighai9gahR6"

# Instagram data
# Instagram data are indexed in the same way, and can be extracted analogously, by changing the database to "instagram" and the view to "instagram" as well.
# For instance:
curl -XGET "http://45.113.232.90/couchdbro/instagram/_des ign/instagram/_view/summary?include_docs=false&reduce=true&group_level=1&skip=0& limit=5" --user "readonly:ween7ighai9gahR6"
