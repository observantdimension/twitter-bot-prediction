import json
import time
import typing
import requests


def load_articles(filename: str) -> typing.List[dict]:
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return [item for page in data for item in page['docs']]


def fetch_article_html(web_url: str) -> str:
    response = requests.get(web_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.92 Safari/537.36 '
    })
    if response.status_code < 200 or response.status_code > 399:
        raise RuntimeError("failed to fetch article")
    return response.text


def run_app():
    all_articles = load_articles('generated_data/recent_political_articles.json')

    for article in all_articles:
        article_path = 'generated_data/articles/%s.html' % str(article['_id'])[len("nyt://article/"):]
        print("Fetch article: %s @ %s -> %s" % (article['headline']['main'], article['web_url'], article_path))
        with open(article_path, 'w', encoding='utf-8') as file:
            file.write(fetch_article_html(article['web_url']))
        time.sleep(1)


run_app()
