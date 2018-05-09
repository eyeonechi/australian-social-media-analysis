import json
from shapely.geometry import shape, Point
# depending on your version, use: from shapely.geometry import shape, Point

# load GeoJSON file containing sectors
with open('geojson/aus_lga2.json') as f:
    js = json.load(f)
with open('geojson/homeless.json') as f:
    hl = json.load(f)

i = 0
with open("geojson/aus_lga2_merge.json", "w") as output:
    for data in hl['data']:
        lat = (data['bbox'][0] + data['bbox'][2]) / 2
        lon = (data['bbox'][1] + data['bbox'][3]) / 2
        point = Point(lat, lon)
        for feature in js['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                print(i)
                outfeature = feature
                outfeature['cnt2011'] = data['cnt2011']
                outfeature['cnt2016'] = data['cnt2016']
                output.write(json.dumps(outfeature) + ',\n')
            i += 1
