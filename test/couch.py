"""
@Team info:
    CCC Team 42 (Melbourne)
    Hannah Ha   963370
    Lan Zhou    824371
    Zijian Wang 950618
    Ivan Chee   736901
    Duer Wang   824325
@Module: Couch
@Function: Provide an api with couchDB using cloudant.
@Methods:
    select_db: select a database, create it if not exist.
    close: close current database.
    count: get the count of items in current database.
    query_all: get all stuffs in current database.
    query: query current database with given selector, return result.
    insert: add something to current database.
    update: change all items in current database with given condition.
    delete: delete all items from current database satisfying given selector.
    aggr_sentiment_analysis: get result from a map&reduced custom view.
                             View details are in MapReduce.js
"""
from cloudant.client import CouchDB
from cloudant.database import CloudantDatabase
from cloudant.document import Document
from cloudant.database import CouchDatabase
from cloudant.design_document import DesignDocument


class Couch:
    db = None
    c_db = None
    couch_db = None

    # usage: database = Couch(db_name)
    # fields: db_name -> str
    def __init__(self, db_name):
        self.client = CouchDB('aassddff', 'ffddssaa', url='http://115.146.85.206:5984/', connect=True, auto_renew=True)
        self.select_db(db_name)

    # Get one database selected; if the database doesn't exist, create it.
    # usage: database.select_db(db_name);
    # fields: db_name -> str
    def select_db(self, db_name):
        self.couch_db = CouchDatabase(self.client, db_name)
        if not self.couch_db.exists():
            self.couch_db.create()
        self.db = self.client[db_name]
        self.c_db = CloudantDatabase(self.client, db_name)

    # usage: database.close()
    # Database should be closed when finish using
    def close(self):
        self.client.disconnect()

    # Get count of documents in current database;
    # usage database.count();
    def count(self):
        return self.couch_db.doc_count()

    # Get everything from the database;
    # usage: database.query_all();
    # note: after query_all, iterate the returned item to get every document
    def query_all(self):
        qlist = []
        for doc in self.db:
            qlist.append(doc)
        return qlist

    # Select something from the database;
    # usage: database.query(selector);
    # fields: selector -> Dictionary
    # note: after query, iterate the returned item to get every document
    def query(self, selector):
        qlist = []
        result = self.c_db.get_query_result(selector)
        for doc in result:
            qlist.append(doc)
        return qlist

    # insert operation of the database;
    # usage: database.insert(doc);
    # fields: doc -> Dictionary
    def insert(self, doc):
        document = self.db.create_document(doc)
        if document.exists():
            return document['id']

    # update operation of the database;
    # usage: database.update(field, old_value, new_value)
    # fields: field -> str; value -> str; new_value -> str
    def update(self, field, value, new_value):
        selector = {field: value}
        q_res = self.c_db.get_query_result(selector)
        for document in q_res:
            id = document['_id']
            doc = Document(self.db, id)
            doc.update_field(
                action=doc.field_set,
                field=field,
                value=new_value
            )

    # delete operation of the database;
    # usage: database.delete(selector)
    # fields: selector -> Dictionary
    def delete(self, selector):
        q_res = self.c_db.get_query_result(selector)
        for document in q_res:
            id = document['_id']
            rev = document['_rev']
            doc = Document(self.db, id)
            doc['_rev'] = rev
            doc.delete()

    # get aggregated data using map&reduce to get average sentiment score of different time periods
    # the view has been already created on the couchDB server.
    def get_aggr_view(self):
        dd = self.db.get_design_document("_design001")
        view = dd.get_view("view1")
        if view is None:
            self.set_aggr_view()
            dd = self.db.get_design_document("_design001")
            view = dd.get_view("view1")
        return view.result[0][0]["value"]

    # set the view of analyzing sentiment score with time periods using built-in map&reduce function.
    def set_aggr_view(self):
        view_name = "view1"
        map_func = """
            function (doc) {
            var t = doc.created_at.time.split(":");
            if(parseInt(t) < 6 ) t = "Midnight";
            else if(parseInt(t) < 12) t = "Morning";
            else if(parseInt(t) < 18) t = "Afternoon";
            else t = "Evening";
            emit([t], doc.polarity);
            }
        """
        reduce_func = """
            function (keys, values, rereduce){
            var key_set = ["Midnight", "Afternoon", "Morning", "Evening"]
            var dict = {}
            for(var i = 0; i < key_set.length; i++) {
            dict[key_set[i]] = {"sum":0, "cnt":0, "avg":0};
            }
            if (rereduce) {
            for(var j = 0; j < values.length; j++){
            for(var i = 0; i < key_set.length; i++) {
            dict[key_set[i]]["sum"] += values[j][key_set[i]]["sum"];
            dict[key_set[i]]["cnt"] += values[j][key_set[i]]["cnt"];
            }
            }
            for(var i = 0; i < key_set.length; i++)
            dict[key_set[i]]["avg"] = (dict[key_set[i]]["sum"] / dict[key_set[i]]["cnt"]);
            return dict;
            }
            else {
            for(var i = 0; i < key_set.length; i++) {
            for(var j = 0; j < values.length; j++){
              if(key_set[i] == keys[j][0][0]){
                dict[key_set[i]]["sum"] += values[j];
                dict[key_set[i]]["cnt"] += 1;
                dict[key_set[i]]["avg"] = (dict[key_set[i]]["sum"] / dict[key_set[i]]["cnt"]);
              }
            }
            }
            return dict;
            }
            }
        """
        dd = DesignDocument(self.db, "_design001")
        dd.add_view(view_name, map_func, reduce_func)
        dd.save()


if __name__ == "__main__":
    conn = Couch("asdfasdf")
    res = conn.get_aggr_view()
    print(res)
