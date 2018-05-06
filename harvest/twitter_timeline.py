"""
COMP90024 Cluster and Cloud Computing
Semester 1 2018
Assignment 2 - Australian Social Media Analysis
Team 42
twitter_timeline.py
"""

import tweepy

from util.argument import Argument
from util.authentication import Authentication
from util.config import Config
from util.couch import Couch
import util.spatial

"""
Main function
"""
def main():
    # Arguments parsing
    args = Argument().get_args()
    # Consumer keys and access tokens, used for OAuth
    config = Config(args.config, args.auth).get_config()
    # OAuth process, using the keys and tokens
    auth = Authentication(config)
    # Creation of the actual interface, using authentication
    api = tweepy.API(auth.get_auth())

    with open(args.input, "r") as f:
        for line in f:
            screen_name = '@' + line
            print("\nscraping timeline: " + screen_name)
            for status in tweepy.Cursor(api.user_timeline, screen_name=screen_name).items():
                #print status._json['text']
                print status

if __name__ == '__main__':
    main()
