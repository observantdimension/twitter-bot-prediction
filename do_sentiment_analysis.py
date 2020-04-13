import shared
import json
import os
import typing
from sentiment import analyze_sentiment
from bs4 import BeautifulSoup


def load_articles(filename: str) -> typing.List[dict]:
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return [item for page in data for item in page['docs']]


def extract_article_text(article_filename: str) -> str:
    with open(article_filename, 'r', encoding='utf-8') as article_file:
        soup = BeautifulSoup(article_file.read())
        body_columns = soup.findAll('div', {'class': 'StoryBodyCompanionColumn'})
        text = ''

        for body_column in body_columns:
            sections = body_column.findAll('div')

            for section in sections:
                paragraphs = section.findAll('p')
                paragraph_class = ''

                for paragraph in paragraphs:
                    # remove "contributed reporting"
                    if paragraph_class != '' and paragraph['class'][0] != paragraph_class:
                        break
                    else:
                        paragraph_class = paragraph['class'][0]
                    text += paragraph.text + os.linesep

        return text


def run_app():
    all_articles = load_articles('generated_data/recent_political_articles.json')
    sentiments: typing.Dict[str, dict] = {}
    print("Examining sentiments...")
    for article in all_articles:
        if article['document_type'] != 'article':
            continue
        article_path = 'generated_data/articles/%s.html' % str(article['_id'])[len("nyt://article/"):]
        print("Examining: %s" % article['headline']['main'])
        sentiment = analyze_sentiment(extract_article_text(article_path)).document_sentiment
        sentiments[article['_id']] = {'score': sentiment.score, 'magnitude': sentiment.magnitude}
    print("Saving sentiments...")
    with open('generated_data/article_sentiments.json', 'w', encoding='utf-8') as sentiments_file:
        json.dump(sentiments, sentiments_file, sort_keys=True, indent=4, ensure_ascii=False)
    print("Done!")


run_app()
