"""
COMP90024 Cluster and Cloud Computing
Semester 1 2018
Assignment 2 - Australian Social Media Analysis
argument.py

Team 42
963370 Thuy Ngoc Ha
824371 Lan Zhou
950618 Zijian Wang
736901 Ivan Chee
824325 Duer Wang
"""

import os
import argparse

class Argument:

    def __init__(self):
        parser = argparse.ArgumentParser(description="Twitter Streamer")
        configuration = os.path.join(os.path.dirname(__file__), "../config.json")

        # Authentication
        parser.add_argument("-a", dest="auth", default='duer')

        # Config file
        parser.add_argument("-c", dest="config", default=configuration)

        # Save to file
        parser.add_argument("-d", dest="directory", default='data')

        # Input file
        parser.add_argument("-i", dest="input", default='data/australia_users.json')

        # Output file
        parser.add_argument("-o", dest="output", default='data/australia_users1.json')

        # Output2 file
        parser.add_argument("-o2", dest="output2", default='data/australia_users11.json')

        # Query
        parser.add_argument("-q", dest="query", default='australia')

        # Screen name
        parser.add_argument("-s", dest="screen_name")

        args = parser.parse_args()
        self.args = args

    def get_args(self):
        return self.args
