import re
from bs4 import BeautifulSoup

def clean_text_advanced(text: str) -> str:
    # Remove code blocks (triple backticks or indented)
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'\n    .+', '', text)
    # Remove inline code (single backticks)
    text = re.sub(r'`[^`]+`', '', text)
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    # Remove HTML tags
    text = BeautifulSoup(text, 'html.parser').get_text()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text 