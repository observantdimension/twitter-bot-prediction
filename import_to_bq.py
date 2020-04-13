import shared
import json
import typing
from dateutil import parser
import bqml


def load_sampled_tweets(filename: str) -> typing.List[dict]:
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def convert_user_to_bq(user: dict) -> dict:
    return {
        'followers_count': user['stats']['followers_count'],
        'friends_count': user['stats']['following_count'],
        'verified': user['verified'],
        'statuses_count': user['stats']['tweet_count'],
        'created_at': parser.isoparse(user['created_at']),
        'name': user['username'],
        'twitter_id': int(user['id']),
        'default_profile_image': 'default_profile_image' in user['profile_image_url'],
    }


def partition_list(input_list: typing.List, partition_size):
    for i in range(0, len(input_list), partition_size):
        yield input_list[i:i + partition_size]


def run_app():
    sampled_tweets = load_sampled_tweets('generated_data/sampled_tweets.json')
    sampled_users: typing.Dict[int, dict] = {}

    for tweet in sampled_tweets:
        sampled_users[tweet['author_id']] = tweet['user_info']
    test_data = list(map(convert_user_to_bq, sampled_users.values()))
    print("Clearing test data")
    bqml.clear_test_data()
    print("Inserting test data")
    for batch in partition_list(test_data, 5000):
        print("Inserting batch")
        result = bqml.setup_test_data(batch)
        if result is None:
            print("Insert succeeded")
        else:
            print("Insert failed")
            print(result)
    print("Running prediction")

    for predicted_row in bqml.predict_data():
        print("Row:", predicted_row)


run_app()
