import shared
import datetime
import json, os, mysql.connector as mysql

db = mysql.connect(
    host=os.environ.get('MYSQL_HOST'),
    user=os.environ.get('MYSQL_USER'),
    passwd=os.environ.get('MYSQL_PASS'),
    database=os.environ.get('MYSQL_DB'),
    charset="utf8mb4"
)
SAMPLE_SIZE = 50000
RANDOM_TWEET_QUERY = 'SELECT ID, created_at, text, author_id, ' \
                     'referenced_tweets, entities, includes, ' \
                     'matching_rules, user_info FROM tweets ORDER BY rand() LIMIT %d' % SAMPLE_SIZE


def run_app():
    cursor = db.cursor()
    cursor.execute(RANDOM_TWEET_QUERY)
    random_records = []
    tweet_id: int
    created_at: datetime
    text: str
    author_id: int
    referenced_tweets: str
    entities: str
    includes: str
    matching_rules: str
    user_info: str

    for obj in cursor:
        tweet_id, created_at, text, author_id, referenced_tweets, entities, includes, matching_rules, user_info = obj
        random_records.append({
            'id': tweet_id,
            'created_at': created_at.isoformat(),
            'text': text,
            'author_id': author_id,
            'referenced_tweets': json.loads(referenced_tweets),
            'entities': json.loads(entities),
            'includes': json.loads(includes),
            'matching_rules': json.loads(matching_rules),
            'user_info': json.loads(user_info),
        })
    cursor.close()
    db.close()
    print("Retrieved %d random Tweets" % len(random_records))
    with open('generated_data/sampled_tweets.json', 'w', encoding='utf-8') as sampleFile:
        json.dump(random_records, sampleFile, sort_keys=True, indent=4, ensure_ascii=False)
    print("Exported random Tweets to sampled_tweets.json")


run_app()
