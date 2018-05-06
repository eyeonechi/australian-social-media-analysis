import json

class Config:

    def __init__(self, configuration, username):
        with open(configuration, "r") as file:
            data = json.load(file)
            self.consumer_key = data[username]["consumer_key"]
            self.consumer_secret = data[username]["consumer_secret"]
            self.access_token = data[username]["access_token"]
            self.access_secret = data[username]["access_secret"]

        self.configuration = data

    def get_config(self):
        #return self.configuration
        return self

    def get_consumer_key(self):
        return self.consumer_key

    def get_consumer_secret(self):
        return self.consumer_secret

    def get_access_token(self):
        return self.access_token

    def get_access_secret(self):
        return self.access_secret
