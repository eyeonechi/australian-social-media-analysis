import httplib2
import json


def cityPos(name):
    url = "https://maps.googleapis.com/maps/api/geocode/json?" + \
          "key=AIzaSyBsZErhxaT1oVgMrT-xGLcAN5nK3UHeGBU&address=" + name
    req = httplib2.Http(".cache")
    resp, content = req.request(url, "GET")
    res = json.loads(content)
    return res["results"][0]["geometry"]
