from tweepy import OAuthHandler

class Authentication:

    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.auth = auth

    def get_auth(self):
        return self.auth
