import os
import argparse

class Argument:

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Twitter Streamer"
        )
        configuration = os.path.join(os.path.dirname(__file__), "config.json")
        # Config file
        parser.add_argument("-c", dest="config", default=configuration)
        # Save to file
        parser.add_argument("-d", dest="directory")
        # Input file
        parser.add_argument("-i")
        # Query
        parser.add_argument("-q", dest="query")
        args = parser.parse_args()
        self.args = args

    def get_args(self):
        return self.args
