import json

class Config:

    def __init__(self, config_file):
        with open(config_file) as file:
            data = json.load(file)
        self.config_dict = data

    def get_config(self):
        return self.config_dict
