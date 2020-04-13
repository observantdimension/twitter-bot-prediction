import os
import requests
import json
from ratelimit import limits, RateLimitException
from backoff import on_exception, expo

NYTIMES_API_KEY = os.environ.get('NYTIMES_API_KEY')


@on_exception(expo, RateLimitException, max_tries=8)
@limits(calls=10, period=60)
def do_article_search(key: str = NYTIMES_API_KEY, params=None) -> dict:
    if params is None:
        params = {}
    response = requests.get('https://api.nytimes.com/svc/search/v2/articlesearch.json?api-key=%s' % key, params=params)

    if response.status_code < 200 or response.status_code > 399:
        raise RuntimeError(
            "Request to ArticleSearch API failed with status %d - body: %s" % (response.status_code, response.text))
    return json.loads(response.text)['response']
