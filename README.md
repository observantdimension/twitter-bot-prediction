# twitter-bot-prediction-code

## Summary
Code for programs used for the AP Research paper about the relationship between news articles and Twitter bot activity. 
This is mainly meant to serve as a reference implementation for research purposes.

## Modules

- **bqml**: Interacts with Google BigQuery API
- **nytimes**: Interacts with the New York Times (NYT) API
- **science**: Generates charts based on data
- **sentiment**: Interacts with Google Natural Language API for sentiment analysis
- **shared**: Shared setup code for most of the programs
- **twitter**: Interacts with the Twitter API

## What's inside

- **articlecorrelator.py**: Generates scores for articles based on collected data.
- **articledumper.py**: Retrieves metadata about political articles with the NYT Article Search API
- **do_sentiment_analysis.py**: Submits downloaded NYT articles to the sentiment analysis API
- **fetch_articles.py**: Downloads NYT articles based on recorded metadata
- **import_to_bq.py**: Imports user data extracted from Tweets into a BigQuery table for later analysis.
- **predict_from_bq.py**: Retrieves bot model results based on previously imported user data. Saves results to a file.
- **tweetcollector.py**: Connects to the Twitter streaming API and "listens" for Tweets which are then made available to **tweetlistener**
- **tweetlistener.py**: Waits for information about Tweets to be made available. Saves Tweets to a **MySQL** database.
- **tweetsampler.py**: Obtains a random sample of **up to 50,000 Tweets** from a **MySQL** database. Saves sample to a file.

## Technologies used

- Python (for all of the code)
- Google BigQuery (for evaluating accounts according to a machine learning model)
- Google Natural Language API (for sentiment analysis)
- NYT Article Search API (to find latest political articles)
- [Python Requests library](https://github.com/psf/requests) - to obtain data from NYT and Twitter APIs
- [MySQL](https://mysql.com) - to locally store data about Tweets
- [Redis](https://redis.io) - to facilitate communication between **tweetcollector** and **tweetlistener**
