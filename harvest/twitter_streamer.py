"""
COMP90024 Cluster and Cloud Computing
Semester 1 2018
Assignment 2 - Australian Social Media Analysis
Team 42
twitter_streamer.py
"""

import json
import re
import string
import time
import tweepy

from keywords import Keywords
from tweepy import Stream
from tweepy.streaming import StreamListener
from util.argument import Argument
from util.authentication import Authentication
from util.config import Config
from util.couch import Couch
import util.spatial

"""
Custom StreamListener for streaming data
"""
class TwitterStreamListener(StreamListener):

    def __init__(self, data_dir, query):
        query_fname = format_filename(query)
        #self.conn = Couch(query)
        self.outfile = "%s/%s.json" % (data_dir, query_fname)
        self.userfile = "%s/%s_users.json" % (data_dir, query_fname)

    def on_data(self, data):
        json_data = json.loads(data)
        #self.conn.insert(json_data)
        mentions = []
        print(data)
        '''
        if "text" in json_data:
            print(json.dumps(json_data["text"]))
            regex = re.compile(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9_]+)', re.UNICODE)
            mentions = regex.findall(json.dumps(json_data["text"]))
        if "user" in json_data:
            if ("screen_name" in json_data["user"]):
                mentions.append(json.dumps(json_data["user"]["screen_name"])[1:-1])
        if "entities" in json_data:
            if "user_mentions" in json_data:
                for user in json_data["entities"]["user_mentions"]:
                    if "id_str" in json_data["entities"]["user_mentions"][i]:
                        print("user_mentions_user_id: " + json_data["entities"]["user_mentions"][i]["id_str"])
        if "retweeted_status" in json_data:
            if "user" in json_data["retweeted_status"]:
                if "id_str" in json_data["retweeted_status"]["user"]:
                    print("retweeted_status_user_id" + json_data["retweeted_status"]["user"]["id_str"])
        '''
        '''
        try:
            with open(self.outfile, "a") as f:
                f.write(data)
            with open(self.userfile, "a") as f:
                for mention in mentions:
                    f.write(mention + '\n')
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        '''
        #To get user screen name from user id
        #user = api.get_user(1088398616)
        #user.screen_name

        #To get user id from user screen name
        #user = api.get_user(screen_name = 'saimadhup')
        #print(user.id)
        return True

    def on_error(self, status):
        print(status)
        return True

"""
Convert file name into a safe string
Arguments:
    fname -- the file name to convert
Return:
    String -- converted file name
"""
def format_filename(fname):
    return ''.join(convert_valid(one_char) for one_char in fname)

"""
Convert a character into '_' if invalid
Arguments:
    one_char -- the char to convert
Return:
    Character -- converted character
"""
def convert_valid(one_char):
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    return '_'

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    steattr(status, 'json', json.dumps(raw))
    return status

"""
Main function
"""
def main():

    # Arguments parsing
    args = Argument().get_args()
    config = Config(args.config, args.auth).get_config()
    auth = Authentication(config)
    api = tweepy.API(auth)
    listener = TwitterStreamListener(args.directory, args.query)
    stream = Stream(auth, listener)

    # Bounding box
    bounding_box = [113.338953078, -43.6345972634, 153.569469029, -10.6681857235]
    print("boundary: ", bounding_box)
    #stream.filter(locations=bounding_box);

'''
    if (args.query == "fastfood"):
        stream.filter(track=[word for word in Keywords.fastfood])
    elif (args.query == "fruits"):
        stream.filter(track=[word for word in Keywords.fruits])
    elif (args.query == "grains"):
        stream.filter(track=[word for word in Keywords.grains])
    elif (args.query == "meat"):
        stream.filter(track=[word for word in Keywords.meat])
    elif (args.query == "seafood"):
        stream.filter(track=[word for word in Keywords.seafood])
    elif (args.query == "vegetables"):
        stream.filter(track=[word for word in Keywords.vegetables])
'''

if __name__ == '__main__':
    main()
