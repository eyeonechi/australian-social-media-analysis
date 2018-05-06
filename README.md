# comp90024-team-42
Australian Social Media Analysis

# Analysis Ideas
- Check who is most favourited/retweeted
- Who's discussing with who
- What are the most popular hashtags

# Instances
classifier 115.146.85.190
cultivator 115.146.86.105
harvester 115.146.86.17
bulldozer 115.146.85.206

couchdb database 115.146.85.206:5984
couchdb database 115.146.85.206:5000 (Web)

# Instructions (Harvester)
sudo pip install cloudant
sudo pip install tweepy
python twitter_streamer.py -q <query> -d <directory>
Listens and streams a list of tweets for query <query> in <directory>
To know how many tweets are gathered
wc -l <file>.json

## The structure of a Tweet
### Attributes:
text
  the text of the tweet itself
created_at
  the date of creation
favorite_count, retweet_count
  the number of favourties and retweets
favorited, retweeted
  boolean stating whether the authentiated user (you) have favourited or retweeted this tweet
lang
  acronym for the language
id
  the tweet identifier
place, coordinates, geo
  geo-location information if available
user
  the author's full profile
entities
  list of entities like URLs, @-mentions, hashtags, and symbols
in_reply_to_user_id
  user identifier if the tweet is a reply to a specific user
in_reply_to_status_id
  status identifier id the tweet is a reply to a specific status

{
  "created_at": "Mon Apr 30 22:04:12 +0000 2018",
  "id": 991075775737614336,
  "id_str": "991075775737614336",
  "text": "With the name change from Monte Carlo to Park MGM it is time to get those chips and cards from the newest closed La… https://t.co/ymW1isk9Nv",
  "display_text_range": [
    0,
    140
  ],
  "source": "<a href=\"http://twitter.com\" rel=\"nofollow\">Twitter Web Client</a>",
  "truncated": true,
  "in_reply_to_status_id": null,
  "in_reply_to_status_id_str": null,
  "in_reply_to_user_id": null,
  "in_reply_to_user_id_str": null,
  "in_reply_to_screen_name": null,
  "user": {
    "id": 55301549,
    "id_str": "55301549",
    "name": "Spinettis Gaming",
    "screen_name": "Spinettis",
    "location": "810 S. Commerce St. Las Vegas, NV",
    "url": "http://www.spinettisgaming.com",
    "description": "Your one stop shop for all your home gaming needs! 702-362-8767",
    "translator_type": "none",
    "protected": false,
    "verified": false,
    "followers_count": 172,
    "friends_count": 357,
    "listed_count": 9,
    "favourites_count": 21,
    "statuses_count": 695,
    "created_at": "Thu Jul 09 17:33:04 +0000 2009",
    "utc_offset": -25200,
    "time_zone": "Pacific Time (US & Canada)",
    "geo_enabled": true,
    "lang": "en",
    "contributors_enabled": false,
    "is_translator": false,
    "profile_background_color": "1A1B1F",
    "profile_background_image_url": "http://pbs.twimg.com/profile_background_images/155197803/twitter.jpg",
    "profile_background_image_url_https": "https://pbs.twimg.com/profile_background_images/155197803/twitter.jpg",
    "profile_background_tile": false,
    "profile_link_color": "19CF86",
    "profile_sidebar_border_color": "181A1E",
    "profile_sidebar_fill_color": "252429",
    "profile_text_color": "666666",
    "profile_use_background_image": true,
    "profile_image_url": "http://pbs.twimg.com/profile_images/896172291897270272/sh6_LQ7U_normal.jpg",
    "profile_image_url_https": "https://pbs.twimg.com/profile_images/896172291897270272/sh6_LQ7U_normal.jpg",
    "profile_banner_url": "https://pbs.twimg.com/profile_banners/55301549/1460160151",
    "default_profile": false,
    "default_profile_image": false,
    "following": null,
    "follow_request_sent": null,
    "notifications": null
  },
  "geo": null,
  "coordinates": null,
  "place": null,
  "contributors": null,
  "is_quote_status": false,
  "extended_tweet": {
    "full_text": "With the name change from Monte Carlo to Park MGM it is time to get those chips and cards from the newest closed Las Vegas casino. You can purchase the Monte Carlo chips here: https://t.co/j9osDNdCx0 and the Monte Carlo deck of cards here: https://t.co/o8P9vG1b0D https://t.co/sQnCXpCsPD",
    "display_text_range": [
      0,
      263
    ],
    "entities": {
      "hashtags": [],
      "urls": [
        {
          "url": "https://t.co/j9osDNdCx0",
          "expanded_url": "https://buff.ly/2FuPEAU",
          "display_url": "buff.ly/2FuPEAU",
          "indices": [
            176,
            199
          ]
        },
        {
          "url": "https://t.co/o8P9vG1b0D",
          "expanded_url": "https://buff.ly/2KqQGS3",
          "display_url": "buff.ly/2KqQGS3",
          "indices": [
            240,
            263
          ]
        }
      ],
      "user_mentions": [],
      "symbols": [],
      "media": [
        {
          "id": 991075747346477057,
          "id_str": "991075747346477057",
          "indices": [
            264,
            287
          ],
          "media_url": "http://pbs.twimg.com/media/DcECJCoXcAEp9r1.jpg",
          "media_url_https": "https://pbs.twimg.com/media/DcECJCoXcAEp9r1.jpg",
          "url": "https://t.co/sQnCXpCsPD",
          "display_url": "pic.twitter.com/sQnCXpCsPD",
          "expanded_url": "https://twitter.com/Spinettis/status/991075775737614336/photo/1",
          "type": "photo",
          "sizes": {
            "thumb": {
              "w": 150,
              "h": 150,
              "resize": "crop"
            },
            "large": {
              "w": 400,
              "h": 400,
              "resize": "fit"
            },
            "small": {
              "w": 400,
              "h": 400,
              "resize": "fit"
            },
            "medium": {
              "w": 400,
              "h": 400,
              "resize": "fit"
            }
          }
        }
      ]
    },
    "extended_entities": {
      "media": [
        {
          "id": 991075747346477057,
          "id_str": "991075747346477057",
          "indices": [
            264,
            287
          ],
          "media_url": "http://pbs.twimg.com/media/DcECJCoXcAEp9r1.jpg",
          "media_url_https": "https://pbs.twimg.com/media/DcECJCoXcAEp9r1.jpg",
          "url": "https://t.co/sQnCXpCsPD",
          "display_url": "pic.twitter.com/sQnCXpCsPD",
          "expanded_url": "https://twitter.com/Spinettis/status/991075775737614336/photo/1",
          "type": "photo",
          "sizes": {
            "thumb": {
              "w": 150,
              "h": 150,
              "resize": "crop"
            },
            "large": {
              "w": 400,
              "h": 400,
              "resize": "fit"
            },
            "small": {
              "w": 400,
              "h": 400,
              "resize": "fit"
            },
            "medium": {
              "w": 400,
              "h": 400,
              "resize": "fit"
            }
          }
        }
      ]
    }
  },
  "quote_count": 0,
  "reply_count": 0,
  "retweet_count": 0,
  "favorite_count": 0,
  "entities": {
    "hashtags": [],
    "urls": [
      {
        "url": "https://t.co/ymW1isk9Nv",
        "expanded_url": "https://twitter.com/i/web/status/991075775737614336",
        "display_url": "twitter.com/i/web/status/9…",
        "indices": [
          117,
          140
        ]
      }
    ],
    "user_mentions": [],
    "symbols": []
  },
  "favorited": false,
  "retweeted": false,
  "possibly_sensitive": false,
  "filter_level": "low",
  "lang": "en",
  "timestamp_ms": "1525125852890"
}
