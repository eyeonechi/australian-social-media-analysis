library(rgdal)
library(spdplyr)
library(geojsonio)
library(rmapshaper)
# Load Australian State and Territories shapefile data
aus_ste <- readOGR(dsn = "/Users/kannishida/Downloads/STE11aAust", layer = "STE11aAust")
# Convert to GeoJSON
aus_ste_json <- geojson_json(aus_ste)
# Simplify the polygons to reduce the size
aus_ste_sim <- ms_simplify(aus_ste_json)
# Write GeoJSON file out to a file system
geojson_write(aus_ste_sim, file = "/Users/kannishida/Downloads/aus_ste.geojson")

/*
# Load Australia Local Government Area in Google Earth format into R
aus_LGA <- readOGR(dsn = "/Users/kannishida/Downloads/doc.kml", layer = "NewFeatureType")
# Convert to GeoJSON
aus_LGA_json <- geojson_json(aus_LGA)
# Simplify the polygons to reduce the size
aus_LGA_sim <- ms_simplify(aus_LGA_json)
# Write GeoJSON file out to a file system
geojson_write(aus_LGA_sim, file = "/Users/kannishida/Downloads/aus_LGA2.geojson")
*/
