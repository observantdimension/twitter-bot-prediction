import json
import requests
import requests.auth
import base64


def create_twitter_token(consumer_key: str, consumer_secret: str) -> dict:
    auth_creds = "%s:%s" % (consumer_key, consumer_secret)
    auth_creds_b64 = base64.b64encode(auth_creds.encode('utf-8')).decode('utf-8')

    response = requests.post(
        url='https://api.twitter.com/oauth2/token',
        data='grant_type=client_credentials',
        headers={
            'Authorization': 'Basic %s' % str(auth_creds_b64),
            'User-Agent': 'curl/7.54.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )

    if response.status_code != 200:
        raise RuntimeError("Failed to generate bearer token")
    decoded_token = json.loads(response.text)
    return decoded_token
