"""
COMP90024 Cluster and Cloud Computing
Semester 1 2018
Assignment 2 - Australian Social Media Analysis
twitter_hydrator.py

Team 42
963370 Thuy Ngoc Ha
824371 Lan Zhou
950618 Zijian Wang
736901 Ivan Chee
824325 Duer Wang
"""

import json

from twarc import Twarc
from util.argument import Argument
from util.authentication import Authentication
from util.config import Config
from util.couch import Couch
import util.spatial

def main():
    args = Argument().get_args()
    config = Config(args.config, args.auth).get_config()
    auth = Authentication(config).get_auth()
    t = Twarc(auth)
    data = []

    for tweet in t.hydrate(open(args.input)):
        data.append(json.dumps(tweet))

    with open(args.output, 'w') as outfile:
        outfile.write("\n".join(data) + '\n')

if __name__ == '__main__':
    main()
