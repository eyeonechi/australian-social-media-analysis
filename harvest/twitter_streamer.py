"""
COMP90024 Cluster and Cloud Computing
Semester 1 2018
Assignment 2 - Australian Social Media Analysis
Team 42
twitter_streamer.py
"""

"""
Instructions
sudo pip install cloudant
sudo pip install tweepy
python twitter_streamer.py -q <query> -d <directory>
Listens and streams a list of tweets for query <query> in <directory>
To know how many tweets are gathered
wc -l <file>.json
"""

import argparse
import config
import json
import string
import time
import tweepy

from keywords import Keywords

from tweepy import Stream
from tweepy.streaming import StreamListener
from util.argument import Argument
from util.authentication import Authentication
from util.config import Config
#from util.couch import Couch
import util.spatial

"""
Custom StreamListener for streaming data
"""
class TwitterStreamListener(StreamListener):

    def __init__(self, data_dir, query):
        query_fname = format_filename(query)
        self.conn = Couch(query)
        self.outfile = "%s/%s.json" % (data_dir, query_fname)

    def on_data(self, data):
        json_data = json.loads(data)
        self.conn.insert(json_data)
        if ("text" in json_data):
            print(json.dumps(json_data["text"]))
        '''
        try:
            with open(self.outfile, "a") as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        '''
        return True

    def on_error(self, status):
        print(status)
        return True

"""
Get parser for command line arguments
Return:
    ArgumentParser -- the argument parser
"""
def get_parser():
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument(
        "-q",
        "--query",
        dest="query",
        help="Query/Filter",
        default="-"
    )
    parser.add_argument(
        "-d",
        "--data-dir",
        dest="data_dir",
        help="Output/Data Directory"
    )
    return parser

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
    auth = Authentication().get_auth()
    api = tweepy.API(auth)
    #config = Config(args.config).getConfig()
    listener = TwitterStreamListener(args.directory, args.query)
    stream = Stream(auth, listener)

    # Bounding box
    bounding_box = [113.338953078, -43.6345972634, 153.569469029, -10.6681857235]
    print("boundary: ", bounding_box)
    stream.filter(locations=bounding_box);

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
