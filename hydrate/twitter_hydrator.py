from twarc import Twarc
import json

consumer_key = "LcSG7Vd1yPgEXfOmvJ72fKLRl"
consumer_secret = "KQpdirJQeypfGEaRfgXoHbPJpaH7SlFwulpoUxzV158xPZJHjR"
access_token = "72584345-gEtHTPXUNGIk16bo27WzRmc6oQJpEHZTGubrAcpEb"
access_token_secret = "WwBYLqomDtSrcPAEk0TojZ1Eu2ve1xNm1ri4Bmzb0UKvq"

t = Twarc(consumer_key, consumer_secret, access_token, access_token_secret)
data = []

for tweet in t.hydrate(open('bth_ids/bth_ids_2014-06-01.txt')):
    data.append(json.dumps(tweet))

with open('bth_ids_hydrated/bth_data_2014-06-01.json', 'w') as outfile:
    outfile.write("\n".join(data) + '\n')
