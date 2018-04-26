import json
import re

from nltk.tokenize import word_tokenize

'''
with open("mytweets.json", "r") as f:
    #line = f.readline()
    for line in f:
        tweet = json.loads(line)
        tokens = preprocess(tweet['text'])
        do_something_else(tokens)
        print(json.dumps(tweet, indent=4))
'''

tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
print(word_tokenize(tweet))
# ['RT', '@', 'marcobonzanini', ':', 'just', 'an', 'example', '!', ':', 'D', 'http', ':', '//example.com', '#', 'NLP']

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r"<[^>]+>", # HTML tags
    r"(?:@[\w_]+)", # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # Hashtags
    r"http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+", # URLs
    r"(?:(?:\d+,?)+(?:\.?\d+)?)", # Numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # Words with - and '
    r"(?:[\w_]+)", # Other words
    r"(?:\S)" # Anything else
]

tokens_re = re.compile(r"("+"|".join(regex_str)+")", re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r"^"+emoticons_str+"$", re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=false):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
print(preprocess(tweet))
# ['RT', '@marcobonzanini', ':', 'just', 'an', 'example', '!', ':D', 'http://example.com', '#NLP']
