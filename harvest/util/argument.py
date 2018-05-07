import os
import argparse

class Argument:

    def __init__(self):
        parser = argparse.ArgumentParser(description="Twitter Streamer")
        configuration = os.path.join(os.path.dirname(__file__), "../config.json")

        # Authentication
        parser.add_argument("-a", dest="auth")

        # Config file
        parser.add_argument("-c", dest="config", default=configuration)

        # Save to file
        parser.add_argument("-d", dest="directory")

        # Input file
        parser.add_argument("-i", dest="input", default=None)

        # Output file
        parser.add_argument("-o", dest="output", default=None)

        # Query
        parser.add_argument("-q", dest="query")

        # Screen name
        parser.add_argument("-s", dest="screen_name")

        args = parser.parse_args()
        self.args = args

    def get_args(self):
        return self.args
