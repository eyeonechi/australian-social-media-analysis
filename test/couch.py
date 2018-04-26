from cloudant.client import CouchDB
from cloudant.database import CloudantDatabase
from cloudant.document import Document
from cloudant.database import CouchDatabase


class Couch:
    db = None
    c_db = None

    # usage: database = Couch(db_name)
    # fields: db_name -> str
    def __init__(self, db_name):
        self.client = CouchDB('aassddff', 'ffddssaa', url='http://115.146.85.206:5984/', connect=True, auto_renew=True)
        #self.client = CouchDB('aassddff', 'ffddssaa', url='http://127.0.0.1:5984/', connect=True, auto_renew=True)
        self.select_db(db_name)

    # Get one database selected; if the database doesn't exist, create it.
    # usage: database.select_db(db_name);
    # fields: db_name -> str
    def select_db(self, db_name):
        couch_db = CouchDatabase(self.client, db_name)
        if not couch_db.exists():
            couch_db.create()
        self.db = self.client[db_name]
        self.c_db = CloudantDatabase(self.client, db_name)

    # usage: database.close()
    # Database should be closed when finish using
    def close(self):
        self.client.disconnect()

    # Get everything from the database;
    # usage: database.query_all();
    def query_all(self):
        for document in self.db:
            print(document)

    # Select something from the database;
    # usage: database.query(selector);
    # fields: selector -> Dictionary
    def query(self, selector):
        result = self.c_db.get_query_result(selector)
        for document in result:
            print(document)

    # insert operation of the database;
    # usage: database.insert(doc);
    # fields: doc -> Dictionary
    def insert(self, doc):
        document = self.db.create_document(doc)
        if document.exists():
            print("Insert success")

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


if __name__ == "__main__":
    conn = Couch("test1")
    #doc = {'foo': 'bar2'}
    #conn.delete({'foo': 'bar'})
    conn.query_all()
