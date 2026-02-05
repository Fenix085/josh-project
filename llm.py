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
        Створи тред із 3-5 твітів на основі цієї новини. Вимоги:
        - Кожен твіт до 280 символів, але близько до ліміту (окрім першого)
        - Перший твіт: інтригуючий хук, щоб привернути увагу
        - Наступні твіти: розкривають деталі та завершують історію
        - Пиши живою, розмовною українською для молодої аудиторії
        - Без хештегів, без посилань, без емодзі
        - Формат: тільки твіти, пронумеровані (*перший без номера*, 2/n, 3/n, ...), кожен з нового рядка

        Стаття:
        Заголовок: {article['title']}
        Зміст: {article['content']}
        Джерело: {article['source']}
        """
        
    response = client.messages.create(
        model = "claude-haiku-4-5",
        max_tokens = 2048,
        system = "Ти — SMM-менеджер українського ігрового/технологічного каналу. Пишеш природною українською мовою.",
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