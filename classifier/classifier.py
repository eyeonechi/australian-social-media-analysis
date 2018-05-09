#!/usr/local/bin/python3

#pip install textblob,vaderSentitment,shapely,Cloudant
import Couch
from keywords import Keywords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from shapely.geometry import shape,Point,box
from textblob import TextBlob
import textblob
import sys
import json
import re

#load maps
print('loading maps...')
act = json.load(open('/home/ubuntu/geo_info/australian_capital_territory/act.json'))
act_sa2 = json.load(open('/home/ubuntu/geo_info/australian_capital_territory/act_sa2.json'))
nsw = json.load(open('/home/ubuntu/geo_info/new_south_wales/nsw.json'))
nsw_sa2 = json.load(open('/home/ubuntu/geo_info/new_south_wales/nsw_sa2.json'))
nt = json.load(open('/home/ubuntu/geo_info/northern_territory/nt.json'))
nt_sa2 = json.load(open('/home/ubuntu/geo_info/northern_territory/nt_sa2.json'))
ot = json.load(open('/home/ubuntu/geo_info/other_territories/ot.json'))
ot_sa2 = json.load(open('/home/ubuntu/geo_info/other_territories/ot.json'))
q = json.load(open('/home/ubuntu/geo_info/queensland/q.json'))
q_sa2 = json.load(open('/home/ubuntu/geo_info/queensland/q_sa2.json'))
sa = json.load(open('/home/ubuntu/geo_info/south_australia/sa.json'))
sa_sa2 = json.load(open('/home/ubuntu/geo_info/south_australia/sa_sa2.json'))
t = json.load(open('/home/ubuntu/geo_info/tasmania/t.json'))\
t_sa2 = json.load(open('/home/ubuntu/geo_info/tasmania/t.json'))
v = json.load(open('/home/ubuntu/geo_info/victoria/v.json'))
v_sa2 = json.load(open('/home/ubuntu/geo_info/victoria/v_sa2.json'))
wa = json.load(open('/home/ubuntu/geo_info/western_australia/wa.json'))
wa_sa2 = json.load(open('/home/ubuntu/geo_info/western_australia/wa_sa2.json'))
print('Maps loaded...')

#initial vadersentiment analyser
analyser = SentimentIntensityAnalyzer()

#textblob translate error
TranslateError = textblob.exceptions.NotTranslated

#features to be extracted from raw tweets
features = ['created_at','lang','text','user']

#check for food keywords in tweet text
def find_food(text):
    text = text.lower()
    food_list = []
    for food in Keywords.fastfood:
        if re.search(r'\b'+food,text):
            food_list.append(food)
    for food in Keywords.fruits:
        if re.search(r'\b'+food,text):
            food_list.append(food)
    for food in Keywords.grains:
        if re.search(r'\b'+food,text):
            food_list.append(food)
    for food in Keywords.meat:
        if re.search(r'\b'+food,text):
            food_list.append(food)
    for food in Keywords.seafood:
        if re.search(r'\b'+food,text):
            food_list.append(food)
    for food in Keywords.vegetables:
        if re.search(r'\b'+food,text):
            food_list.append(food)
    return food_list
    
#preprocess tweet text
def preprocess(text):
    text = re.sub(r'#','',text)
    #text = re.sub(r'(^|(?<=\s))#\S*(\s|$)','',text)
    text = re.sub(r'(^|(?<=\s))@\S*(\s|$)','',text)
    text = re.sub(r'(^|(?<=\s))https?:\/\/\S*(\s|$)','',text)
    text = re.sub(r'(^|(?<=\s))RT(\s|$)','',text)
    return text #return a preprocessed tweets

#extract features needed
def fil(tweet,features,loc,aurin): #input a single tweet, features needed, location info and aurin stats
    doc = {}
    doc.update({'location':loc})
    doc.update({'homeless':aurin})
    for feature in features: #iterate through each feature in feature list
        if feature == 'text': #for 'text'
            try:
                raw_text = tweet['extended_tweet']['full_text'] #get raw text
                #print('extended')
            except KeyError:
                raw_text = tweet[feature]
            text = preprocess(raw_text) #do preprocess on raw text
            if tweet['lang'] != 'en': #if language not english translate:
                text = TextBlob(text) #turn to a textblob object
                try:
                    text = str(text.translate(to='en')) #translate to english
                except TranslateError:
                    text = str(text)
            food_list = find_food(text)
            doc.update({'food_list':food_list})
            
            score = analyser.polarity_scores(text)['compound'] #sentiment analysis
            doc.update({'polarity':score}) #update sentiment score

        elif feature == 'created_at':#get time
            time = tweet[feature]
            tokens = time.split()
            value = {}
            value.update({'weekday':tokens[0]})
            value.update({'month':tokens[1]})
            value.update({'day':tokens[2]})
            value.update({'time':tokens[3]})
            value.update({'year':tokens[5]})
            doc.update({feature:value})
            
        elif feature == 'user':
            user = {}
            user.update({'following':tweet[feature]['friends_count']})
            user.update({'followers':tweet[feature]['followers_count']})
            doc.update({'user':user})
            
        else:#for other features get and insert directly
            doc.update({feature:tweet[feature]})
            
    return doc #return a json object with features extracted

#find suburb
def check_coor(polygons,coor):
    for suburb in polygons['features']:
        polygon = shape(suburb['geometry'])
        suburb_name = None
        if polygon.contains(coor):
            suburb_name = suburb['properties']['feature_name']
            break
    return suburb_name
def sub_classifier(sa2,coor):
    sub_sa2 = check_coor(sa2,coor)
    return sub_sa2

#attach aurin stats to a tweet
def homeless_count(coor,aurin_homeless):
    count_16 = None
    diff = None
    for area in aurin_homeless:
        bbox = box(area['bbox'][0],area['bbox'][1],area['bbox'][2],area['bbox'][3])
        if bbox.contains(coor):
            try:
                count_16 = area['cnt2016']
                diff = area['cnt2016'] - area['cnt2011']
            except TypeError:
                count_16 = None
                diff = None
    return count_16,diff

#get location info
def location(tweet,aurin_homeless):
    coor = []
    aus = False
    sub_sa2 = None
    ste = None
    place_type = None
    name = None
    loc = {}
    aurin = {}
    count_16 = None
    diff = None

    if tweet['place'] is not None:
        if tweet['place']['country_code'] == 'AU':
            aus = True
            name = tweet['place']['name']
            place_type = tweet['place']['place_type']
        else:
            return aus,loc,aurin

    if tweet['coordinates'] is not None:
        coor = Point(tweet['coordinates']['coordinates'])
        count_16,diff = homeless_count(coor,aurin_homeless)

    if coor:
        if check_coor(act,coor) is not None:
            aus = True
            ste = 'Australian Capital Territory'
            sub_sa2 = sub_classifier(act_sa2,coor)
        elif check_coor(nsw,coor) is not None:
            aus = True
            ste = 'New South Wales'
            sub_sa2 = sub_classifier(nsw_sa2,coor)
        elif check_coor(nt,coor) is not None:
            aus = True
            ste = 'Northern Territory'
            sub_sa2 = sub_classifier(nt_sa2,coor)

        elif check_coor(ot,coor) is not None:
            aus = True
            ste = 'Other Territories'
            sub_sa2 = sub_classifier(ot_sa2,coor)
        elif check_coor(q,coor) is not None:
            aus = True
            ste = 'Queensland'
            sub_sa2 = sub_classifier(q_sa2,coor)
        elif check_coor(sa,coor) is not None:
            aus = True
            ste = 'South Australia'
            sub_sa2 = sub_classifier(sa_sa2,coor)
        elif check_coor(t,coor) is not None:
            aus = True
            ste = 'Tasmania'
            sub_sa2 = sub_classifier(t_sa2,coor)
        elif check_coor(v,coor) is not None:
            aus = True
            ste = 'Victoria'
            sub_sa2 = sub_classifier(v_sa2,coor)

        elif check_coor(wa,coor) is not None:
            aus = True
            ste = 'Western Australia'
            sub_sa2 = sub_classifier(wa_sa2,coor)
        if count_16 != None and diff != None:
            aurin.update({'cnt16': count_16})
            aurin.update({'incre/decre': diff})
    else:
        aurin = None

    loc.update({'place_type':place_type})
    loc.update({'place_name':name})
    loc.update({'state_and_territories': ste})
    #loc.update({'sub_sa4':sub_sa4})
    #loc.update({'sub_sa3':sub_sa3})
    loc.update({'sub_sa2':sub_sa2})
    
    try:
        loc.update({'coordinates':tweet['coordinates']['coordinates']})
    except TypeError:
        loc.update({'coordinates':None})
        
    return aus,loc, aurin
    
#main function
def main(input_db,output_db,action):
    #get raw tweets
    raw = Couch.Couch(input_db) 
    tweets = raw.query_all() 
    
    #get tweet already there
    classified = Couch.Couch(output_db)
    classified_tweets = classified.query_all()
    
    #get aurin stats from db
    aurin_info = Couch.Couch('homeless') 
    aurin_homeless = aurin_info.query_all()
    
    inserted = 0
    counter = 0
    
    for tweet in tweets:
        try:
            aus,loc,aurin = location(tweet,aurin_homeless)
        except KeyError:
            aus = False
        if aus == True:
            filtered = fil(tweet,features,loc,aurin)
            if action == 'print':
                print (filtered)
            elif action == 'insert':
                classified.insert(filtered)
            else:
                print ('invalid action arg')
                break
            inserted += 1

    print('classification finished')
    print('total in raw:', raw.count())
    print('total classified:',inserted)
    print('total in output database:',classified.count())
    raw.close()
    classified.close()
    aurin_info.close()


if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])
