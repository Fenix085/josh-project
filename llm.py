import ollama
import json
import deepl

translator = deepl.Translator("fd8f8927-3a91-4988-8e20-f565f0657813:fx")

def load_articles(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def generate_thread(article, model = "gpt-oss:20b"):
    prompt = f"""You are a social media manager for a gaming/tech news channel.

        Create a thread of 3-5 tweets based on this news article. Requirements:
        - Each tweet must be under 280 characters
        - First tweet: attention-grabbing hook to draw readers in
        - Following tweets: reveal the details and complete the story
        - Write in an engaging, conversational tone for a young audience
        - No hashtags, no links
        - Format: only the tweets, numbered (1., 2., 3., ...), each on a new line

        Article:
        Title: {article['title']}
        Content: {article['content']}
        Source: {article['source']}
        """
        
    response = ollama.chat(model=model, messages=[
        {'role': 'user', 'content': prompt}
    ])
    
    english_thread = response['message']['content']
    ukrainian_thread = translate_to_ukrainian(english_thread)

    return ukrainian_thread

def translate_to_ukrainian(text):
    result = translator.translate_text(text, target_lang="UK")
    return result.text

if __name__ == "__main__":
    articles = load_articles('articles.json')
    thread = generate_thread(articles[0])
    print(thread)