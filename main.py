# main.py

#scrap -> filter -> llm -> tweet_maker

import re
import json
from llm import *
from filter import *
from scraper import *

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

if __name__ == "__main__":
    
    #scraper
    ign_feed = feedparser.parse("https://feeds.feedburner.com/ign/all")
    verge_feed = feedparser.parse("https://www.theverge.com/rss/index.xml")

    ign_articles = parse_feed(ign_feed, "IGN")
    verge_articles = parse_feed(verge_feed, "The Verge")
    all_articles = ign_articles + verge_articles
    save_articles(all_articles, "articles_raw.json")

    #filter
    articles = load_articles('articles_raw.json')
    filtered_articles = filter_articles(articles)
    with open('articles_filtered.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_articles, f, ensure_ascii=False, indent=4)

    #llm
    articles = load_articles('articles_filtered.json')
    fin_tweets = []
    for article in articles:
        thread = generate_thread(article)
        tweets = tweet_maker(thread)
        fin_tweets.append(tweets)
    with open('articles_tweets.json', 'w', encoding='utf-8') as f:
        json.dump(fin_tweets, f, ensure_ascii=False, indent=4)
    # thread = generate_thread(articles[0])
    # # print(thread)

