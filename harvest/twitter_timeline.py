"""
COMP90024 Cluster and Cloud Computing
Semester 1 2018
Assignment 2 - Australian Social Media Analysis
twitter_timeline.py

Team 42
963370 Thuy Ngoc Ha
824371 Lan Zhou
950618 Zijian Wang
736901 Ivan Chee
824325 Duer Wang
"""

import json
import re
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

    with open(args.input, "r") as input:
        with open(args.output, "a") as output:
            with open(args.output2, "a") as useroutput:
                for line in input:
                    screen_name = '@' + line
                    print("\ntimeline user: " + screen_name)
                    for status in tweepy.Cursor(api.user_timeline, screen_name=screen_name).items():
                        text = json.dumps(status._json['text'])
                        regex = re.compile(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9_]+)', re.UNICODE)
                        mentions = regex.findall(text)
                        print(text)
                        output.write(json.dumps(status._json) + '\n')
                        for mention in mentions:
                            useroutput.write(mention + '\n')

if __name__ == '__main__':
    main()
