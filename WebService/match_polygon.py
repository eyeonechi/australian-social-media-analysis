import json
from shapely.geometry import shape, Point
# depending on your version, use: from shapely.geometry import shape, Point

# load GeoJSON file containing sectors
with open('geojson/aus_lga2.json') as f:
    js = json.load(f)
with open('geojson/homeless.json') as f:
    hl = json.load(f)
with open('geojson/test000.json') as f:
    ts = json.load(f)

features = js['features']

for feature in features:
    polygon = shape(feature['geometry'])
    for data in hl['data']:
        lat = (data['bbox'][0] + data['bbox'][2]) / 2
        lon = (data['bbox'][1] + data['bbox'][3]) / 2
        point = Point(lat, lon)
        if polygon.contains(point):
            feature['cnt2011'] = data['cnt2011']
            feature['cnt2016'] = data['cnt2016']
    for data in ts['data'][0]['features']:
        lat2 = data['geometry']['coordinates'][1]
        lon2 = data['geometry']['coordinates'][0]
        point = Point(lat2, lon2)
        if polygon.contains(point):
            feature['followers'] = data['properties']['followers']
            feature['following'] = data['properties']['following']
            feature['food'] = data['properties']['food']
            feature['polarity'] = data['properties']['polarity']
            feature['time'] = data['properties']['time']

with open("geojson/aus_lga2_merge.json", "w") as output:
    for feature in features:
        output.write(json.dumps(feature) + ',\n')

'''
features = []
i = 0
for feature in js['features']:
    polygon = shape(feature['geometry'])
    for data in hl['data']:
        lat = (data['bbox'][0] + data['bbox'][2]) / 2
        lon = (data['bbox'][1] + data['bbox'][3]) / 2
        point = Point(lat, lon)
        if polygon.contains(point):
            outfeature = feature
            outfeature['cnt2011'] = data['cnt2011']
            outfeature['cnt2016'] = data['cnt2016']
            features.append(outfeature)
    for data in ts['data'][0]['features']:
        lon2 = data['geometry']['coordinates'][1]
        lat2 = data['geometry']['coordinates'][0]
        point = Point(lon2, lat2)
        if polygon.contains(point):
            outfeature = feature
            outfeature['followers'] = data['properties']['followers']
            outfeature['following'] = data['properties']['following']
            outfeature['food'] = data['properties']['food']
            outfeature['polarity'] = data['properties']['polarity']
            outfeature['time'] = data['properties']['time']
            features.append(outfeature)
    print(i)
    i += 1

with open("geojson/aus_lga2_merge.json", "w") as output:
    for feature in features:
        output.write(json.dumps(feature) + ',\n')
'''
