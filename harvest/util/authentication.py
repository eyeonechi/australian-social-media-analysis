from tweepy import OAuthHandler

class Authentication:

    def __init__(self):
        consumer_key = "zH2FibbwW0YYh3CfXDCw4kqd6"
        consumer_secret = "iCAzNqRroptDtG9GzObk5z74ckqZlPpd45YvHCYMij59Xl9JEA"
        access_token = "1052753850-F4e2TNaABpyPGlGbPVXsLRAOUqeSXBhWyzwx1PG"
        access_secret = "YQTu7a8ca8blOW9k1uPsNYpnteiIOs2SGZXHKThZ9gnKY"
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.auth = auth

    def get_auth(self):
        return self.auth
