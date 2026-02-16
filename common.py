import json
from anthropic import Anthropic
from dotenv import load_dotenv
import os
import requests as req

load_dotenv()

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
gist = os.environ.get("GIST_API")
gist_id = "6f7ce78bc50d93452daf0b71544be89a"


def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_to_gist(data, filename = "articles_tweets.json"):
    token = gist
    req.patch(
        f"https://api.github.com/gists/{gist_id}",
        headers = {"Authorization": f"token {token}"},
        json = {"files": {filename: {"content": json.dumps(data, ensure_ascii=False, indent=4)}}}
    )

def load_from_gist(filename = "articles_tweets.json"):
    token = gist
    if not token:
        return []
    resp = req.get(
        f"https://api.github.com/gists/{gist_id}",
        headers={"Authorization": f"token {token}"}
    )
    if resp.status_code != 200:
        return []
    files = resp.json().get("files", {})
    if filename not in files:
        return []
    return json.loads(files[filename]["content"])