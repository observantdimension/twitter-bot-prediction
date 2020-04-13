import typing
import requests


def start_tweet_stream(token: dict) -> typing.Generator[str, None, None]:
    response = requests.get(
        url='https://api.twitter.com/labs/1/tweets/stream/filter?user.format=detailed&tweet.format=detailed&place'
            '.format=detailed&expansions=author_id',
        headers={
            'Authorization': 'Bearer %s' % token['access_token'],
            'User-Agent': 'curl/7.54.0'
        },
        stream=True
    )

    response.encoding = 'utf-8'

    for line in response.iter_lines(decode_unicode=True):
        yield str(line).encode('utf-8')
