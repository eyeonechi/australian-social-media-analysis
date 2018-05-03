import json

class Config:

    def __init__(self, configuration):
        with open(configuration, "r") as file:
            data = json.load(file)
        self.configuration = data

    def get_config(self):
        #return self.configuration
        return self

    def get_consumer_key(self):
        return "YUNUdSMzyEBSi13eehfBDF06t"

    def get_consumer_secret(self):
        return "S1lQmet9U6cYuVq9kd2V9xfphE1VBJyfwVab6ESimYKfgmR4Dz"

    def get_access_token(self):
        return "3155253092-mphGphCcXsTZshneJuJ2Gz9qQU5gm6PEScVNy4W"

    def get_access_secret(self):
        return"T5Cs7jFTjo8ocpGGQ2zYr0N0XANfC1lyQNvNF2NPb5nYL"
