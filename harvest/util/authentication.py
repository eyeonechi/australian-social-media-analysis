from tweepy import OAuthHandler

class Authentication:

    def __init__(self, config):
        consumer_key = config.get_consumer_key()
        consumer_secret = config.get_consumer_secret()
        access_token = config.get_access_token()
        access_secret = config.get_access_secret()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.auth = auth

    def get_auth(self):
        return self.auth
