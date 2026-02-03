import feedparser
import json

def parse_feed(feed, source_name):
    articles = []
    for entry in feed.entries:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "summary": entry.summary,
            "source": source_name
        })
    return articles

def save_articles(all_articles, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, indent=4)

if __name__ == "__main__":
    ign_feed = feedparser.parse("https://feeds.feedburner.com/ign/all")
    verge_feed = feedparser.parse("https://www.theverge.com/rss/index.xml")

    ign_articles = parse_feed(ign_feed, "IGN")
    verge_articles = parse_feed(verge_feed, "The Verge")
    all_articles = ign_articles + verge_articles
    save_articles(all_articles, "articles.json")