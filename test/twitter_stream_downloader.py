# First edit config.py with your configuration
# mkdir data
# python twitter_stream_download.py -q apple -d data
# Produces list of tweets for query "apple" in file data/stream_apple.json

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

def main():
    consumer_key = "YOUR-CONSUMER-KEY"
    consumer_secret = "YOUR-CONSUMER-SECRET"
    access_token = "YOUR-ACCESS-TOKEN"
    access_secret = "YOUR-ACCESS-SECRET"

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    """ Accessing the Data """
    # Read our own timeline
    for status in tweepy.Cursor(api.home_timeline).items(10):
        # Process a single status
        print(status.text)
        process_or_store(status._json)

    for friend in tweepy.Cursor(api.friends).items():
        process_or_store(friend._json)

    for tweet in tweepy.Cursor(api.user_timeline).items():
        process_or_store(tweet._json)

    def process_or_store(tweet):
        print(json.dumps(tweet))

    """ Streaming """
    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(track=["#python"])

""" Custom StreamListener for streaming data
"""
class MyListener(StreamListener):

    def __init__(self, data_dir, query):
        query_fname = format_filename(query)
        self.conn = Couch("test")
        #self.outfile = "%s/stream_%s.json" % (data_dir, query_fname)

    def on_data(self, data):
        print(data)
        self.conn.insert(json.loads(data))
        '''
        try:
            with open(self.outfile, "a") as f:
                f.write(data)
                print(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        '''
        return True

    def on_error(self, status):
        print(status)
        return True

""" Get parser for command line arguments
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

""" Convert file name into a safe string
    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
"""
def format_filename(fname):
    return ''.join(convert_valid(one_char) for one_char in fname)

""" Convert a character into '_' if invalid
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

# To know how many tweets are gathered
# wc -l python.json

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)
    twitter_stream = Stream(auth, MyListener(args.data_dir, args.query))
    twitter_stream.filter(track=[args.query])
