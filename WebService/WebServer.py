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
import os

# start the web service.
app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
@app.route('/index')
def index():
    """
    For test if the service works.
    :return: NoneType
    """
    return flask.render_template('index.html', title='Home')

@app.route('/graph')
def graph():
    return flask.render_template('graph.html', title='Graph')

@app.route('/graphHomeless')
def graphHomeless():
    return flask.render_template('graphHomeless.html', title='Homeless Graph')

@app.route('/graphSentiment')
def graphSentiment():
    return flask.render_template('graphSentiment.html', title='Sentiment Graph')

@app.route('/mapFood')
def mapFood():
    return flask.render_template('mapFood.html', title='Food Map')

@app.route('/mapHomelessAndFoods')
def mapHomelessAndFoods():
    return flask.render_template('mapHomelessAndFoods.html', title='Homeless and Foods Map')

@app.route('/mapHomelessBySuburb')
def mapHomelessBySuburb():
    return flask.render_template('mapHomelessBySuburb.html', title='Homeless by Suburb Map')

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


@app.route('/database/<string:db_name>/period', methods=["GET"])
def period_view(db_name):
    """
    get information of aggregated data of specific database.
    :param db_name: string; the name of target database
    :return: res: respond object including the query result.
    """
    db = Couch.Couch(db_name)
    q_res = {"data": db.get_aggr_view("view1")}
    res = flask.make_response(flask.jsonify(q_res))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


@app.route('/database/<string:db_name>/day', methods=["GET"])
def day_view(db_name):
    """
    get information of aggregated data of specific database.
    :param db_name: string; the name of target database
    :return: res: respond object including the query result.
    """
    db = Couch.Couch(db_name)
    q_res = {"data": db.get_aggr_view("view2")}
    res = flask.make_response(flask.jsonify(q_res))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


@app.route('/database/<string:db_name>/date', methods=["GET"])
def date_view(db_name):
    """
    get information of aggregated data of specific database.
    :param db_name: string; the name of target database
    :return: res: respond object including the query result.
    """
    db = Couch.Couch(db_name)
    q_res = {"data": db.get_aggr_view("view3")}
    res = flask.make_response(flask.jsonify(q_res))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=False)
