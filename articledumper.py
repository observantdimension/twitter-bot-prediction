import shared
import json
import typing
from nytimes import api


def collect_article_pages(params: dict, page_count: int = 10) -> typing.List[dict]:
    pages: typing.List[dict] = []

    for i in range(page_count):
        params['page'] = i
        print("Fetching page index %d" % i)
        pages.append(api.do_article_search(params=params))

    return pages


def run_app():
    recent_political_articles = collect_article_pages(
        {
            'fq': 'subsection_name:("Politics") AND source:("The New York Times") AND persons:("Trump, Donald J") AND '
                  'document_type:("article")',
            'sort': 'newest'
        }, 5)
    with open('generated_data/recent_political_articles.json', 'w', encoding='utf-8') as articlesFile:
        json.dump(recent_political_articles, articlesFile, sort_keys=True, indent=4, ensure_ascii=False)
    pass


run_app()
