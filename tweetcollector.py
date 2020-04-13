import shared
import json
import os
import time
import typing
import redis
from twitter import credentials, streaming_rules, streaming

TWITTER_CONSUMER_API_KEY = os.environ.get('TWITTER_CONSUMER_API_KEY')
TWITTER_CONSUMER_API_SECRET_KEY = os.environ.get('TWITTER_CONSUMER_API_SECRET_KEY')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
TWITTER_BEARER_TOKEN: typing.Optional[dict] = None
r = redis.Redis(host=os.environ.get('REDIS_HOST'), port=int(os.environ.get('REDIS_PORT')),
                db=int(os.environ.get('REDIS_DB')))


def initialize():
    global TWITTER_BEARER_TOKEN

    TWITTER_BEARER_TOKEN = credentials.create_twitter_token(TWITTER_CONSUMER_API_KEY, TWITTER_CONSUMER_API_SECRET_KEY)


def publish_tweet(tweet: str):
    # print(tweet)
    r.publish('tweets', tweet)


def run_app():
    initialize()
    streaming_rules.clear_streaming_rules(TWITTER_BEARER_TOKEN)
    with open('rules.json', 'r') as rulesFile:
        loaded_rules = json.load(rulesFile)
        print("Loaded %d rules" % len(loaded_rules))

        if streaming_rules.create_streaming_rules(TWITTER_BEARER_TOKEN, loaded_rules):
            print("Waiting 20 seconds to accommodate delay")
            time.sleep(20)

        # Start streaming
        print("Starting...")
        for tweet in streaming.start_tweet_stream(TWITTER_BEARER_TOKEN):
            if tweet:
                publish_tweet(tweet)


run_app()
