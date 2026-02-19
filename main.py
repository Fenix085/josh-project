# main.py

#scrap -> filter -> llm -> tweet_maker

import re
from llm import *
from filter import *
from scraper import *
from twitter import *
from common import *
from datetime import datetime, timezone, timedelta

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
    config = load_from_gist('config.json')
    all_articles = []
    for source in config["sources"]:
        if source["active"]:
            feed = feedparser.parse(source["url"])
            all_articles.extend(parse_feed(feed, source["name"]))
    
    save_articles(all_articles, "articles_raw.json")
    return True

def run_filter():
    articles = load_json('articles_raw.json')
    queue = load_from_gist("articles_tweets.json")
    existing_links = {item["link"] for item in queue}
    articles = [a for a in articles if a["link"] not in existing_links]

    filtered_articles = filter_articles(articles)
    with open('articles_filtered.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_articles, f, ensure_ascii=False, indent=4)
    return True

def run_llm():
    articles = load_json('articles_filtered.json')
    queue = load_from_gist("articles_tweets.json")

    for article in articles:
        thread = generate_thread(article)
        tweets = tweet_maker(thread)
        queue.append({
            "Image": article["image"],
            "Tweets": tweets,
            "link": article["link"],
            "posted": False,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    save_to_gist(queue, "articles_tweets.json")
    return True

def run_twitter():
    queue = load_from_gist("articles_tweets.json")
    unposted = [item for item in queue if not item["posted"]]

    if not unposted:
        return
    pick = random.choice(unposted)
    tweet_thread([pick])
    pick["posted"] = True
    
    clean_time = datetime.now(timezone.utc) - timedelta(hours = 6)
    queue = [item for item in queue if not item["posted"] or datetime.fromisoformat(item["timestamp"]) > clean_time]

    save_to_gist(queue, "articles_tweets.json")

if __name__ == "__main__":
    run_scraper()
    run_filter()
    run_llm()
    run_twitter()
