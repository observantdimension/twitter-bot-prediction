import json
import typing

import matplotlib.pyplot as plt


def load_articles(filename: str) -> typing.List[dict]:
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return [item for page in data for item in page['docs']]


def load_article_sentiments(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_score_data(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def run_app():
    score_data = load_score_data('../generated_data/final_score_data.json')['article_scores']
    article_sentiments = load_article_sentiments('../generated_data/article_sentiments.json')
    articles = [x for x in load_articles('../generated_data/recent_political_articles.json') if
                x['document_type'] == 'article']

    print("Generating graph...")
    plt.figure(figsize=(20, 8))
    plt.bar([round(article_sentiments[x['_id']]['magnitude']) for x in articles],
            [score_data[x['_id']] for x in articles], color='green')
    plt.title('Sentiment (magnitude) vs article score', fontsize=24)
    plt.xlabel('Sentiment (magnitude)', fontsize=20)
    plt.ylabel('Score', fontsize=18)
    plt.savefig('../graphs/sentiment_vs_score.png')
    plt.figure(figsize=(20, 8))
    nonzero_articles = [x for x in articles if score_data[x['_id']] > 0]
    plt.bar([round(article_sentiments[x['_id']]['magnitude']) for x in nonzero_articles],
            [score_data[x['_id']] for x in nonzero_articles], color='green')
    plt.title('Sentiment (magnitude) vs article score (non-zero only)', fontsize=24)
    plt.xlabel('Sentiment (magnitude)', fontsize=20)
    plt.ylabel('Score', fontsize=18)
    plt.savefig('../graphs/sentiment_vs_score_nonzero.png')
    print("Generated graph!")
    with open('../graphs/sentiment_vs_score.txt', 'w', encoding='utf-8') as txt_file:
        txt_file.write('id,name,sentiment,score\n')
        for article in articles:
            txt_file.write('%s,%s,%d,%d\n' %
                           (
                               article['_id'],
                               article['headline']['main'],
                               round(article_sentiments[article['_id']]['magnitude']),
                               score_data[article['_id']]
                           ))


run_app()
