import json
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)