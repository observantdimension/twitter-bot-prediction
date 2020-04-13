import datetime
import json
import typing
import pytz
from dateutil import parser


def load_articles(filename: str) -> typing.List[dict]:
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return [item for page in data for item in page['docs']]


def load_sampled_tweets(filename: str) -> typing.List[dict]:
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def article_diff_sort(value: typing.Tuple[datetime.datetime, dict, datetime.timedelta]) -> float:
    (_, _, diff) = value
    return diff.total_seconds()


def save_scoring_info(filename: str, tweets: typing.List[dict], articles: typing.List[dict],
                      article_scores: typing.Dict[str, float]):
    with open(filename, 'w', encoding='utf-8') as file:
        scoring_info = {
            'articles': {x['_id']: x for x in articles},
            'tweets': tweets,
            'article_scores': article_scores
        }

        json.dump(scoring_info, file, sort_keys=True, indent=4, ensure_ascii=False, default=str)


def prepare_scored_tweet(tweet: dict,
                         all_sorted_matches: typing.Dict[
                             int, typing.List[typing.Tuple[datetime.datetime, dict, datetime.timedelta]]]) -> dict:
    tweet_id = int(tweet['id'])
    matches_list = [a['_id'] for (_, a, _) in all_sorted_matches[tweet_id]]
    return {**tweet, **{'matched_articles_sorted': matches_list}}


def run_app():
    all_articles = load_articles('generated_data/recent_political_articles.json')
    print("loaded %d articles" % len(all_articles))
    sampled_tweets = load_sampled_tweets('generated_data/sampled_tweets.json')
    print("loaded %d tweets" % len(sampled_tweets))
    article_time_map: typing.Dict[datetime.datetime, dict] = {}

    print("setting up article times + scores")

    # build time map
    all_pub_datetimes = []
    article_score_map: typing.Dict[str, float] = {}
    for article in all_articles:
        parsed_pub_datetime = parser.isoparse(article['pub_date'])
        article_time_map[parsed_pub_datetime] = article
        all_pub_datetimes.append(parsed_pub_datetime)
        article_score_map[article['_id']] = 0

    print("calculating article scores")
    all_sorted_matches: typing.Dict[int, typing.List[typing.Tuple[datetime.datetime, dict, datetime.timedelta]]] = {}

    # for each Tweet, find correlated articles and update scores (score is based on how close an article's
    # publication time is to a Tweet's time)
    for tweet in sampled_tweets:
        parsed_tweet_datetime = pytz.utc.localize(parser.isoparse(tweet['created_at']))
        relative_matches = [
            (
                article_time,
                article,
                parsed_tweet_datetime - article_time
            ) for article_time, article in article_time_map.items() if article_time <= parsed_tweet_datetime]
        sorted_matches: typing.List[typing.Tuple[datetime.datetime, dict, datetime.timedelta]] = sorted(
            relative_matches, key=article_diff_sort)
        i = 0

        for (_, ar, _) in sorted_matches:
            i += 1
            article_score_map[ar['_id']] += 1.0 / i
        all_sorted_matches[int(tweet['id'])] = sorted_matches
    print("saving score info")
    save_scoring_info("generated_data/final_score_data.json",
                      [prepare_scored_tweet(x, all_sorted_matches) for x in sampled_tweets],
                      all_articles,
                      article_score_map)
    print("done!")


run_app()
