"""
JSON Structure
(use coordinates, geo field is depreciated)
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [some_latitude, some_longitude]
            },
            "properties": {
                "text": "This is sample a tweet",
                "created_at": "Sat Mar 21 12:30:00 +0000 2015"
            }
        },
        /* more tweets ... */
    ]
}
"""

# Tweets are stored in fname
with open(fname, "r") as f:
    geo_data = {
        "type": "FeatureCollection",
        "features": []
    }
    for line in f:
        tweet = json.loads(line)
        if tweet["coordinates"]:
            geo_json_feature = {
                "type": "Feature",
                "geometry": tweet["coordinates"],
                "properties": {
                    "text": tweet["text"],
                    "created_at": tweet["created_at"]
                }
            }
            geo_data["features"].append(geo_json_feature)

# Save geo data
with open("geo_data.json", "w") as fout:
    fout.write(json.dumps(geo_data, indent=4))
