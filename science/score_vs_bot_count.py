import json
import typing

import matplotlib.pyplot as plt


def load_article_sentiments(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_sampled_tweets(filename: str) -> typing.List[dict]:
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_user_predictions(filename: str) -> typing.Dict[str, int]:
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_score_data(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_articles(filename: str) -> typing.List[dict]:
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return [item for page in data for item in page['docs']]


def run_app():
    articles = [x for x in load_articles('../generated_data/recent_political_articles.json') if
                x['document_type'] == 'article']
    user_predictions = load_user_predictions('../generated_data/user_predictions.json')
    score_data = load_score_data('../generated_data/final_score_data.json')

    stats_dict = {x['_id']: 0 for x in articles}

    for tweet in score_data['tweets']:
        prediction = user_predictions[tweet['user_info']['username']]
        if prediction == 1:
            actual_articles = [x for x in tweet['matched_articles_sorted'] if 'article' in x]
            for i in range(0, min(3, len(actual_articles))):
                stats_dict[actual_articles[i]] += 1

    plt.figure(figsize=(20, 8))
    plt.bar([round(score_data['article_scores'][x['_id']]) for x in articles],
            [stats_dict[x['_id']] for x in articles], color='green')
    plt.title('Article score vs # of detected bots', fontsize=24)
    plt.xlabel('Score', fontsize=20)
    plt.ylabel('Apparent bots', fontsize=18)
    plt.savefig('../graphs/score_vs_bots.png')

    articles_with_bots = [x for x in articles if stats_dict[x['_id']] > 0]
    plt.figure(figsize=(20, 8))
    plt.bar([round(score_data['article_scores'][x['_id']]) for x in articles_with_bots],
            [stats_dict[x['_id']] for x in articles_with_bots], color='green')
    plt.title('Article score vs # of detected bots (non-zero only)', fontsize=24)
    plt.xlabel('Score', fontsize=20)
    plt.ylabel('Apparent bots', fontsize=18)
    plt.savefig('../graphs/score_vs_bots_nonzero.png')

    print("Generated graph!")

    with open('../graphs/score_vs_bots.txt', 'w', encoding='utf-8') as txt_file:
        txt_file.write('id,name,score,bots\n')
        for article in articles:
            txt_file.write('%s,%s,%d,%d\n' %
                           (
                               article['_id'],
                               article['headline']['main'],
                               round(score_data['article_scores'][article['_id']]),
                               stats_dict[article['_id']]
                           ))


run_app()
