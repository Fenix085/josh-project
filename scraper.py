import feedparser
import json
from bs4 import BeautifulSoup

def parse_feed(feed, source_name):
    articles = []
    for entry in feed.entries:
        articles.append({
            "title": entry.title,
            "image": entry.media_content[0]['url'] if hasattr(entry, "media_content") else BeautifulSoup(entry.content[0].value, "html.parser").find('img')['src'] if hasattr(entry, "content") else None,
            "link": entry.link,
            "published": entry.published,
            "summary": entry.summary,
            "content": BeautifulSoup(entry.content[0].value, "html.parser").get_text(separator="\n") if hasattr(entry, "content") else "",
            "source": source_name
        })
    return articles

def save_articles(all_articles, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, indent=4)

def load_links(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

if __name__ == "__main__":
    config = load_links('config.json')
    all_articles = []
    for source in config["sources"]:
        feed = feedparser.parse(source["url"])
        all_articles.extend(parse_feed(feed, source["name"]))
    
    save_articles(all_articles, "articles_raw.json")