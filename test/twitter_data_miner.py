import json
import operator
import string

from collections import Counter
from collections import defaultdict
from nltk import bigrams
from nltk.corpus import stopwords

''' Term frequencies '''
fname = "mytweets.json"
with open(fname, "r") as f:
    count_all = Counter()
    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        terms_all = [term for term in proprocess(tweet['text'])]
        # Update the counter
        count_all.update(terms_all)
    # Print the first 5 most frequent words
    print(count_all.most_common(5))

punctuation = list(string.punctuation)
stop = stopwords.words("english") + punctuation + ["rt", "via"]
terms_stop = [term for term in preprocess(tweet["text"]) if term not in stop]

# Count terms only once, equivalent to Document Frequency
terms_single = set(terms_all)
# Count hashtags only
terms_hash = [term for term in preprocess(tweet["text"]) if term.startswith("#")]
# Count terms only (no hashtags, no mentions)
terms_only = [term for term in preprocess(tweet["text"]) if term not in stop and not term.startswith(("#", "@"))]
# Sequence of two terms
terms_bigram = bigrams(terms_stop)

''' Term co-occurences '''
com = defaultdict(lambda : defaultdict(int))

# f is the file pointer to the JSON data set
for line in f:
    tweet = json.loads(line)
    terms_only = [term for term in preprocess(tweet["text"]) if term not in stop and not term.startswith(("#", "@"))]
    # Build co-occurrence matrix
    for i in range(len(terms_only) - 1):
        for j in range(i + 1, len(terms_only)):
            w1, w2 = sorted([terms_only[i], terms_only[j]])
            if w1 != w2:
                com[w1][w2] += 1
    com_max = []
    # For each term, look for the most common co-occurrent terms
    for t1 in com:
        t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
        for t2, t2_count in t1_max_terms:
            com_max.append(((t1, t2), t2_count))
    # Get the most frequent co-occurrences
    terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
    print(terms_max[:5])

# Look for a specific term and extract its most frequent co-occurrences
search_word = sys.argv[1]
count_search = Counter()
for line in f:
    tweet = json.loads(line)
    terms_only = [term for term in preprocess(tweet["text"]) if term not in stop and not term.startswith(("#", "@"))]
    if search_word in term_only:
        count_search.update(terms_only)
print("Co-occurrence for %s:" % search_word)
print(count_search.most_common(20))
