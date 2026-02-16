# main.py

#scrap -> filter -> llm -> tweet_maker

import re
from llm import *
from filter import *
from scraper import *
from twitter import *
from common import *

def tweet_maker(raw):
    tweets = raw.splitlines()
    tweets = [tweet for tweet in tweets if tweet.strip() != '']
    tweets_fin = []
    i = 0
    while i < len(tweets):
        if re.match(r"^\d+/\d+$", tweets[i].strip()) and i+1 < len(tweets):
            tweets_fin.append(tweets[i] + "\n" + tweets[i+1])
            i += 2  
        else:
            tweets_fin.append(tweets[i])
            i += 1
    return tweets_fin

def run_scraper():
    config = load_json('config.json')
    all_articles = []
    for source in config["sources"]:
        if source["active"]:
            feed = feedparser.parse(source["url"])
            all_articles.extend(parse_feed(feed, source["name"]))
    
    save_articles(all_articles, "articles_raw.json")
    return True

def run_filter():
    articles = load_json('articles_raw.json')
    filtered_articles = filter_articles(articles)
    with open('articles_filtered.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_articles, f, ensure_ascii=False, indent=4)
    return True

def run_llm():
    articles = load_json('articles_filtered.json')
    fin_tweets = []
    for article in articles:
        thread = generate_thread(article)
        tweets = tweet_maker(thread)
        fin_tweets.append({"Image": article["image"], "Tweets": tweets})
    with open('articles_tweets.json', 'w', encoding='utf-8') as f:
        json.dump(fin_tweets, f, ensure_ascii=False, indent=4)
    return True

def run_twitter():
    tweets_file = load_json('articles_tweets.json')
    tweet_thread([random.choice(tweets_file)])

if __name__ == "__main__":
    run_scraper()
    run_filter()
    run_llm()
    save_to_gist(load_json('articles_tweets.json'))
    run_twitter()