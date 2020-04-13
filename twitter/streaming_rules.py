import json

import requests
import typing


def create_streaming_rules(token: dict, rules: typing.List[dict]) -> bool:
    if rules is None:
        raise RuntimeError("no rules provided")

    response = requests.post(
        url='https://api.twitter.com/labs/1/tweets/stream/filter/rules',
        headers={
            'Authorization': 'Bearer %s' % token['access_token'],
            'User-Agent': 'curl/7.54.0'
        },
        json={
            'add': rules
        }
    )

    if response.status_code < 200 or response.status_code > 399:
        raise RuntimeError("Failed to create rules")
    return json.loads(response.text)['meta']['summary']['created'] != 0


def get_streaming_rules(token: dict) -> typing.List[dict]:
    response = requests.get(
        url='https://api.twitter.com/labs/1/tweets/stream/filter/rules',
        headers={
            'Authorization': 'Bearer %s' % token['access_token'],
            'User-Agent': 'curl/7.54.0'
        }
    )

    if response.status_code != 200:
        raise RuntimeError("Failed to get rules")

    response_data = json.loads(response.text)

    if "data" in response_data:
        return response_data["data"]

    return []


def delete_streaming_rules(ids: typing.List[str], token: dict):
    if len(ids):
        response = requests.post(
            url='https://api.twitter.com/labs/1/tweets/stream/filter/rules',
            headers={
                'Authorization': 'Bearer %s' % token['access_token'],
                'User-Agent': 'curl/7.54.0'
            },
            json={
                'delete': {
                    'ids': ids
                }
            }
        )

        if response.status_code != 200:
            raise Exception("Failed to delete rule")


def clear_streaming_rules(token: dict):
    rules = get_streaming_rules(token)
    delete_streaming_rules(list(x['id'] for x in rules), token)
