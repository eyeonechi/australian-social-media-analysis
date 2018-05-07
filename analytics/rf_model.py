import sys
import os
import httplib2
import json
import csv
import codecs
import time as t
from couch import Couch
from pyspark.sql import SparkSession
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import RandomForest
from pyspark.sql.functions import udf
from pyspark.sql.types import *
from keywords import Keywords

os.environ['SPARK_HOME'] = "spark"
sys.path.append("spark/python")
sys.path.append("spark/python/lib")

#COUCHDB_NAME = "cl_richard"
COUCHDB_NAME = "classified1"
#OUT_COUCHDB_NAME = "prediction11885"
OUT_COUCHDB_NAME = "test001"
REFORMED_FILE = "data/output0.csv"
APP_NAME = "random forest model"
SPARK_URL = "local[*]"
RANDOM_SEED = 12345
TRAINING_DATA_RATIO = 0.7
RF_NUM_TREES = 10
RF_MAX_DEPTH = 5
RF_NUM_BINS = 32
food_dict = {}
rev_dict = {}
food_pre = False
homeless_pre = False


# get coordinates of a given city
def cityPos(name):
    url = "https://maps.googleapis.com/maps/api/geocode/json?" + \
          "key=AIzaSyBsZErhxaT1oVgMrT-xGLcAN5nK3UHeGBU&address=" + name
    req = httplib2.Http(".cache")
    resp, content = req.request(url, "GET")
    res = json.loads(content)
    return res["results"][0]["geometry"]

# reform the data preparing for fitting the model
def trans(path):
    con = Couch(COUCHDB_NAME)
    jsonData = con.query_all()

    csvfile = open(REFORMED_FILE, 'w', newline='')
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
    keys=['id', 'time', 'timestamp', 'lat', 'lng', 'polarity', 'followers', \
          'following', 'homeless', 'homeless_trend', 'food_class']
    writer.writerow(keys)
    
    i = 0
    for dic in jsonData:
        # get coordinates
        if dic['location']['coordinates'] is None:
            city = dic['location']['place_name']
            city = city.replace(" ","%20")
            coor = cityPos(city)
            lng = coor['location']['lng']
            lat = coor['location']['lat']
        else:
            lng = dic['location']['coordinates'][0]
            lat = dic['location']['coordinates'][1]
            
        # get time amd timesptamp
        time = dic['created_at']['day']+ '-' + \
                    trans_month(dic['created_at']['month'])+ '-' + \
                    dic['created_at']['year']+ ' ' +dic['created_at']['time']
        timeArray = t.strptime(time, "%d-%m-%Y %H:%M:%S")
        timestamp = t.mktime(timeArray)
        
        # to ensure at least one of homeless info and food info appears
        home = dic['homeless']
        foods = dic['food_list']
        if home is None and foods is None:
            continue
        
        # get homeless information
        if home is None:
            homeless = -1
            homeless_trend = 0
        else:
            try:
                homeless = dic['homeless']['cnt16']
                homeless_trend = dic['homeless']['incre/decre']
            except:
                continue
        # get food
        if foods is None or len(foods) == 0:
            writer.writerow([i, time, timestamp, lat, lng, dic['polarity'], \
                             dic['user']['followers'], \
                             dic['user']['following'], homeless, \
                             homeless_trend, "-1"])
            i += 1
        else:
            for food in foods:
                food_class = get_food_class(food)
                writer.writerow([i, time, timestamp, lat, lng, \
                                 dic['polarity'], dic['user']['followers'], \
                                 dic['user']['following'], homeless, \
                                 homeless_trend, food_class])
                i += 1
    csvfile.close()
    
def trans_month(month):
    month_dic = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', \
                 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', \
                 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    return month_dic[month]

def get_food_class(food):
    if not food in food_dict.keys():
        food_dict[food] = str(len(food_dict))
    return food_dict[food]

def generate_rev_dict():
    for key,value in food_dict.items():
        rev_dict[value] = key
        
# get food name by food class
def get_food_type(food_class):
    the_class = str(food_class)
    if the_class in rev_dict.keys():
        return rev_dict[the_class]
    return None

# get food group by food name
def get_food_group(food):
    if food in Keywords.fastfood:
        return "fastfood"
    if food in Keywords.fruits:
        return "fruits"
    if food in Keywords.grains:
        return "grains"
    if food in Keywords.meat:
        return "meat"
    if food in Keywords.seafood:
        return "seafood"
    if food in Keywords.vegetables:
        return "vegetables"
    return None



if __name__ == "__main__":
    
    spark = SparkSession.builder.appName(APP_NAME) \
            .master(SPARK_URL).getOrCreate()
            
    # read data from couchdb and reform them into a dataframe
    trans(REFORMED_FILE)

    df = spark.read.options(header = "true", inferschema = "true")\
            .csv(REFORMED_FILE)

    print("\nTotal number of rows loaded: %d" % df.count())
    
    df = df.drop_duplicates()
    print("\nTotal number of rows without duplicates: %d" % df.count())
    df.show()
    
    # filter dataframe
    df_no_food = df.filter(df['food_class'] == -1)
    df_no_homeless = df.filter(df['homeless'] == -1)
    df_all_info = df.filter(df['food_class'] >= 0).filter(df['homeless'] >= 0)

    print("\nNumber of rows having all information: %d" % df_all_info.count())
    print("number of rows without food information: %d" % df_no_food.count())
    print("number of rows without homeless information: %d" % df_no_homeless.count())
            
    # transform dataframe into RDD and split reformed data into tranning data and test data
    transformed_df_food = df_all_info.rdd.map(lambda row: LabeledPoint(row[-1], Vectors.dense(row[2:-1])))
    transformed_df_homeless = df_all_info.rdd.map(lambda row: LabeledPoint(row[-3], Vectors.dense(row[2],row[3],row[4],row[5],row[6],row[7],row[10])))
    transformed_df_homeless_trend = df_all_info.rdd.map(lambda row: LabeledPoint(row[-2], Vectors.dense(row[2],row[3],row[4],row[5],row[6],row[7],row[10])))

    splits = [TRAINING_DATA_RATIO, 1.0 - TRAINING_DATA_RATIO]
    training_data_food, test_data_food = transformed_df_food.randomSplit(splits, RANDOM_SEED)
    training_data_homeless, test_data_homeless = transformed_df_homeless.randomSplit(splits, RANDOM_SEED)
    training_data_homeless_trend, test_data_homeless_trend = transformed_df_homeless_trend.randomSplit(splits, RANDOM_SEED)

    print("\nNumber of training set rows: %d" % training_data_food.count())
    print("Number of test set rows: %d" % test_data_food.count())
    
    # train the classification model using training data
    start_time = t.time()
    num_classes = len(food_dict)

    model_food_classifier = RandomForest.trainClassifier(training_data_food, \
                            numClasses=num_classes,categoricalFeaturesInfo={},\
                            numTrees=RF_NUM_TREES, \
                            featureSubsetStrategy="auto", impurity="gini", \
                            maxDepth=RF_MAX_DEPTH, maxBins=32, \
                            seed=RANDOM_SEED)

    end_time = t.time()
    elapsed_time = end_time - start_time
    print("\nTime to train food classifier: %.3f seconds" % elapsed_time)
    
    # train the regression model using training data
    start_time = t.time()
    model_homeless_regressor = RandomForest.trainRegressor(training_data_homeless,\
                            categoricalFeaturesInfo={},numTrees=RF_NUM_TREES, \
                            featureSubsetStrategy="auto", impurity="variance",\
                            maxDepth=RF_MAX_DEPTH, maxBins=32, seed=RANDOM_SEED)

    model_homeless_trend_regressor = RandomForest.trainRegressor(training_data_homeless_trend, categoricalFeaturesInfo={}, \
              numTrees=RF_NUM_TREES, featureSubsetStrategy="auto", impurity="variance", \
              maxDepth=RF_MAX_DEPTH, maxBins=32, seed=RANDOM_SEED)

    end_time = t.time()
    elapsed_time = end_time - start_time
    print("\nTime to train homeless regressor: %.3f seconds" % elapsed_time)
    
    # make predictions using test data and calculate the accuracy
    food_predictions = model_food_classifier.predict(test_data_food.map(lambda x: x.features))
    homeless_predictions = model_homeless_regressor.predict(test_data_homeless.map(lambda x: x.features))
    homeless_trend_predictions = model_homeless_trend_regressor.predict(test_data_homeless_trend.map(lambda x: x.features))


    labels_and_predictions_food = test_data_food.map(lambda x: x.label).zip(food_predictions)
    labels_and_predictions_homeless = test_data_homeless.map(lambda x: x.label).zip(homeless_predictions)
    labels_and_predictions_homeless_trend = test_data_homeless_trend.map(lambda x: x.label).zip(homeless_trend_predictions)

    food_acc = labels_and_predictions_food.filter(lambda x: x[0] == x[1]).count() / float(test_data_food.count())
    homeless_acc = labels_and_predictions_homeless.filter(lambda x: abs(x[0]-x[1]) < 10).count() / float(test_data_homeless.count())
    homeless_trend_acc = labels_and_predictions_homeless_trend.filter(lambda x: abs(x[0]-x[1]) < 10).count() / float(test_data_homeless_trend.count())

    print("\nFood classifier accuracy: %.3f%%" % (food_acc * 100))
    print("Homeless regressor accuracy: %.3f%%" % (homeless_acc * 100))
    print("Homeless trend regressor accuracy: %.3f%%" % (homeless_trend_acc * 100))
    
    food_pre = df_no_food.count() > 0
    homeless_pre = df_no_homeless.count() > 0

    # make food predictions
    if food_pre:
        transformed_df_no_food = df_no_food.rdd.map(lambda row: LabeledPoint(row[-1], Vectors.dense(row[2:-1])))
        predict_foods = model_food_classifier.predict(transformed_df_no_food.map(lambda x: x.features))

    # make homeless predictions
    if homeless_pre:
        transformed_df_no_homeless = df_no_homeless.rdd.map(lambda row: LabeledPoint(row[8], Vectors.dense(row[2],row[3],row[4],row[5],row[6],row[7],row[10])))
        transformed_df_no_homeless_trend = df_no_homeless.rdd.map(lambda row: LabeledPoint(row[9], Vectors.dense(row[2],row[3],row[4],row[5],row[6],row[7],row[10])))
        predict_homeless = model_homeless_regressor.predict(transformed_df_no_homeless.map(lambda x: x.features))
        predict_homeless_trend = model_homeless_trend_regressor.predict(transformed_df_no_homeless_trend.map(lambda x: x.features))
    
    # combine id with predictions
    if food_pre:
        rdd_predict_foods = df_no_food.rdd.map(lambda row: row[0]).zip(predict_foods.map(int))
        list_predict_foods = rdd_predict_foods.collect()
    if homeless_pre:
        rdd_predict_homeless = df_no_homeless.rdd.map(lambda row: row[0]).zip(predict_homeless.map(int))
        rdd_predict_homeless_trend = df_no_homeless.rdd.map(lambda row: row[0]).zip(predict_homeless_trend.map(int))
        list_predict_homeless = rdd_predict_homeless.collect()
        list_predict_homeless_trend = rdd_predict_homeless_trend.collect()
    
    # transform predicted rdd to dataframe and join it to original data that without food
    if food_pre:
        df_predict_foods = spark.createDataFrame(list_predict_foods, schema=["id","food_class"])
        df_no_food = df_no_food.drop('food_class')
        concat_df_food = df_no_food.join(df_predict_foods, on='id')
    
    if homeless_pre:
        df_predict_homeless = spark.createDataFrame(list_predict_homeless, schema=["id","homeless"])
        df_predict_homeless_trend = spark.createDataFrame(list_predict_homeless_trend, schema=["id","homeless_trend"])
    
        df_no_homeless = df_no_homeless.drop('homeless').drop('homeless_trend')
        concat_df_homeless = df_no_homeless.join(df_predict_homeless, on='id').join(df_predict_homeless_trend, on='id')
            

    generate_rev_dict()
    
    get_food_type_udf = udf(get_food_type, StringType())

    get_food_group_udf = udf(get_food_group, StringType())

    df_all_info = df_all_info.withColumn('food', get_food_type_udf(df_all_info['food_class']))
    df_all_info = df_all_info.drop('food_class')

    # reform the dataframe to prepare for tranforming to json
    if food_pre:
        concat_df_food = concat_df_food.withColumn('food', get_food_type_udf(concat_df_food['food_class']))
        concat_df_food = concat_df_food.drop('food_class')

        union_df = df_all_info.union(concat_df_food)
    else:
        union_df = df_all_info
    
    
    if homeless_pre:
        concat_df_homeless = concat_df_homeless.withColumn('food', get_food_type_udf(concat_df_homeless['food_class']))
        concat_df_homeless = concat_df_homeless.drop('food_class')
    
        union_df = union_df.union(concat_df_homeless)
   
    union_df = union_df.drop('id')
    union_df = union_df.drop('timestamp')

    union_df = union_df.withColumn('food_group', get_food_group_udf(union_df['food']))

    print("\nTotal number of rows of final data: %d" % (union_df.count()))
    union_df.show()
    
    json_data = union_df.toJSON()
    
    # insert data into couchdb
    my_db = Couch(OUT_COUCHDB_NAME)

    final_json = {}
    final_json["type"] = "FeatureCollection"
    final_json["features"] = []

    j = 0
    for row in json_data.collect():
        entry = {}
        entry["type"] = "Feature"
        entry["properties"] = {}
        entry["geometry"] = {}
        entry["geometry"]["type"] = "Point"
        entry["geometry"]["coordinates"] = []
    
        json_obj = json.loads(row)
        entry["properties"]["time"] = json_obj["time"]
        entry["properties"]["polarity"] = json_obj["polarity"]
        entry["properties"]["followers"] = json_obj["followers"]
        entry["properties"]["following"] = json_obj["following"]
        entry["properties"]["food"] = json_obj["food"]
        entry["properties"]["food_group"] = json_obj["food_group"]
        entry["properties"]["homeless"] = json_obj["homeless"]
        entry["properties"]["homeless_trend"] = json_obj["homeless_trend"]
        entry["geometry"]["coordinates"].append(json_obj["lat"])
        entry["geometry"]["coordinates"].append(json_obj["lng"])
    
        final_json["features"].append(entry)
        j += 1
    
    print('\n')
    my_db.insert(final_json)
    print("\nTotal number of rows inserted: %d" % (j))
            
    spark.stop()
            
            
            
            
            
            
            
            
            
            
            
            