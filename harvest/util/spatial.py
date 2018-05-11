"""
COMP90024 Cluster and Cloud Computing
Semester 1 2018
Assignment 2 - Australian Social Media Analysis
spatial.py

Team 42
963370 Thuy Ngoc Ha
824371 Lan Zhou
950618 Zijian Wang
736901 Ivan Chee
824325 Duer Wang
"""

import math

def bounding_box(core_lon, core_lat, radius):
    lon = core_lon
    lat = core_lat
    R = 6371 # Radius of the Earth in km
    lon1 = lon - math.degrees(radius / R / math.cos(math.radians(lat)))
    lat1 = lat - math.degrees(radius / R)
    lon2 = lon + math.degrees(raidus / R / math.cos(math.radians(lat)))
    lat2 = lat + math.degrees(radius / R)
    return [lon1, lat1, lon2, lat2]

def in_box(point_lon, point_lat, box_lon1, box_lat1, box_lon2, box_lat2):
    if (box_lon1 <= point_lon and point_lon <= box_lon2 and box_lat1 <= point_lat and point_lat <= box_lat2):
        return True
    return False
