import shared
import json
import os
import dateutil.parser
import mysql.connector as mysql
import redis

r = redis.Redis(host=os.environ.get('REDIS_HOST'), port=int(os.environ.get('REDIS_PORT')),
                db=int(os.environ.get('REDIS_DB')))
db = mysql.connect(
    host=os.environ.get('MYSQL_HOST'),
    user=os.environ.get('MYSQL_USER'),
    passwd=os.environ.get('MYSQL_PASS'),
    database=os.environ.get('MYSQL_DB'),
    charset="utf8mb4"
)
TWEET_INSERT_QUERY = 'INSERT INTO tweets (ID, created_at, text, author_id, referenced_tweets, entities, includes, matching_rules, user_info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
buffer = []
TWEETS_COLLECTED = 0


def flush_buffer():
    global TWEETS_COLLECTED
    cursor = db.cursor()

    for parsed_tweet in buffer:
        cursor.execute(
            TWEET_INSERT_QUERY,
            (
                int(parsed_tweet['tweet']['id']),
                dateutil.parser.isoparse(parsed_tweet['tweet']['created_at']),
                parsed_tweet['tweet']['text'],
                int(parsed_tweet['tweet']['author_id']),
                json.dumps(
                    parsed_tweet['tweet']['referenced_tweets'] if 'referenced_tweets' in parsed_tweet['tweet'] else []),
                json.dumps(parsed_tweet['tweet']['entities'] if 'entities' in parsed_tweet['tweet'] else []),
                json.dumps(parsed_tweet['includes'] if 'includes' in parsed_tweet else []),
                json.dumps(parsed_tweet['matching_rules'] if 'matching_rules' in parsed_tweet else []),
                json.dumps(parsed_tweet['author'])
            )
        )

    db.commit()
    TWEETS_COLLECTED += len(buffer)
    buffer.clear()


def handle_message(msg):
    inner_data = str(msg['data'], 'utf-8')
    parsed_data = json.loads(inner_data)
    parsed_tweet = parsed_data['data']
    tweet_author = [x for x in parsed_data['includes']['users'] if x['id'] == parsed_tweet['author_id']][0]

    buffer.append(
        {'tweet': parsed_tweet, 'includes': parsed_data['includes'], 'matching_rules': parsed_data['matching_rules'],
         'author': tweet_author})

    if len(buffer) >= 128:
        flush_buffer()
        print("Flushed buffer. Collected %d tweets" % TWEETS_COLLECTED)


def run_app():
    p = r.pubsub()
    p.subscribe('tweets')

    for msg in p.listen():
        if msg['type'] == 'message' and msg['channel'] == b'tweets':
            handle_message(msg)

    pass


run_app()
