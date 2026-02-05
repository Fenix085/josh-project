import json
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def load_articles(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def generate_thread(article, model = "claude-haiku-4-5"):
    prompt = f"""
        Create a thread of 3-5 tweets based on this news article. Requirements:
        - Each tweet must be under 280 characters but close to the limit (except the first tweet)
        - First tweet: attention-grabbing hook to draw readers in
        - Following tweets: reveal the details and complete the story
        - Write in an engaging, conversational tone for a young audience
        - No hashtags, no links, no emojis
        - Format: only the tweets, numbered (*first is not numbered*, 2/n, 3/n, ...), each on a new line

        Article:
        Title: {article['title']}
        Content: {article['content']}
        Source: {article['source']}
        """
        
    response = client.messages.create(
        model = "claude-haiku-4-5",
        max_tokens = 1000,
        system = "You are a social media manager for a gaming/tech news channel.",
        messages=[
            {"role": "user",
            "content": prompt,
            }
        ]
    )
    
    thread = response.content[0].text
    return thread
    
if __name__ == "__main__":
    articles = load_articles('articles.json')
    thread = generate_thread(articles[0])
    print(thread)