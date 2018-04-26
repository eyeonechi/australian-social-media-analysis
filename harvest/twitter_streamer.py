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

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from couch import Couch

"""
Custom StreamListener for streaming data
"""
class TwitterStreamListener(StreamListener):

    def __init__(self, data_dir, query):
        query_fname = format_filename(query)
        self.conn = Couch("test1")
        self.outfile = "%s/%s.json" % (data_dir, query_fname)

    def on_data(self, data):
        self.conn.insert(json.loads(data))
        try:
            with open(self.outfile, "a") as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
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
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(
        config.consumer_key,
        config.consumer_secret
    )
    auth.set_access_token(
        config.access_token,
        config.access_secret
    )
    api = tweepy.API(auth)
    twitter_stream = Stream(
        auth,
        TwitterStreamListener(
            args.data_dir,
            args.query
        )
    )
    twitter_stream.filter(track=[args.query])

if __name__ == '__main__':
    main()
