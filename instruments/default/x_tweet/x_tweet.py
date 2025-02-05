### x_tweet

import tweepy
import sys

# X or Twitter API credentials
X_TWITTER_API_TOKEN_KEY = sys.argv[1]
X_TWITTER_API_TOKEN_SECRET = sys.argv[2]

X_TWITTER_ACCESS_TOKEN = sys.argv[3]
X_TWITTER_ACCESS_TOKEN_SECRET = sys.argv[4]

# Text from user
Text = " ".join(sys.argv[5:])

# Connect to client
try:
    client = tweepy.Client(
        consumer_key=X_TWITTER_API_TOKEN_KEY, consumer_secret=X_TWITTER_API_TOKEN_SECRET,
        access_token=X_TWITTER_ACCESS_TOKEN, access_token_secret=X_TWITTER_ACCESS_TOKEN_SECRET
    )

    # Response
    response = client.create_tweet(
        text=Text
    )

    # Output
    print("Response : "+str(response))
    print("Link : "+f"https://x.com/user/status/{response.data['id']}")

# Error handling
except Exception as e:
    print(e)
