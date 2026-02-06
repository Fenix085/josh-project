from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def load_articles(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def filter_articles(articles):
    filtered = []
    for i, article in enumerate(articles):
        prompt = f"""
        Evaluate if an article is worth posting based on these criteria:
        - Would readers want to discuss this with friends?
        - Is it surprising, significant, or conversation-worthy?
        - NOT just a shopping deal or routine minor update

        Examples:
        Article: Samsung QN90F Review -> SKIP
        Article: Pokémon Character Designer Reveals... -> POST
        Article: Valve’s Steam Machine has been delayed... -> SKIP
        Article: "PS6 announced" → POST
        Article: "Kindle 10% thinner" → SKIP
        Article: "Best Buy TV sale" → SKIP
        Article: "Nintendo smell controller patent" → POST
        Article: Tech review -> SKIP

        Respond with only: POST or SKIP
        Article Title: {article['title']}
        Article Content: {article['content']}
        Article Source: {article['source']}
        """
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=10,
            system="You are a content filter for a Ukrainian gaming/tech news channel.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        decision = response.content[0].text.strip().upper().split()[0]  # Get first word of response
        
        if decision == "POST":
            filtered.append(article)
    return filtered

if __name__ == "__main__":
    articles = load_articles('articles_raw.json')
    filtered_articles = filter_articles(articles)
    with open('articles_filtered.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_articles, f, ensure_ascii=False, indent=4)