"""
@Team info:
    CCC Team 42 (Melbourne)
    Hannah Ha   963370
    Lan Zhou    824371
    Zijian Wang 950618
    Ivan Chee   736901
    Duer Wang   824325
@Module: WebServer
@Function: Provide a webservice running on port 5000, webpages should only query database through this service.
@Methods:
    query_all: get all data with specified database name.
    query: query current database with given selector, return result.
    aggregate: get information of aggregated data of specific database.
@Usage: should be running standalone.
    python3 WebServer.py
"""
from flask import Flask, request
import Couch
import json
import flask

# start the web service.
app = Flask(__name__)


@app.route('/')
def index():
    """
    For test if the service works.
    :return: NoneType
    """
    return "Hello, World!"


@app.route('/database/<string:db_name>', methods=["GET"])
def query_all(db_name):
    """
    get all data with specified database name.
    :param db_name: string; the name of target database
    :return: res: respond object including the query result.
    """
    db = Couch.Couch(db_name)
    q_res = {"data": db.query_all()}
    res = flask.make_response(flask.jsonify(q_res))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


@app.route('/database/<string:db_name>/query', methods=["POST"])
def query(db_name):
    """
    query current database with given selector, return result.
    :param db_name: string; the name of target database
    :return: res: respond object including the query result.
    """
    data = request.get_data()
    data = data.decode("utf-8")
    selector = json.loads(data)
    db = Couch.Couch(db_name)
    q_res = {"data": db.query(selector)}
    res = flask.make_response(flask.jsonify(q_res))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


@app.route('/databate/<string:db_name>/aggregation', methods=["GET"])
def aggregate(db_name):
    """
    get information of aggregated data of specific database.
    :param db_name: string; the name of target database
    :return: res: respond object including the query result.
    """
    db = Couch.Couch(db_name)
    q_res = {"data": db.get_aggr_view()}
    res = flask.make_response(flask.jsonify(q_res))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
