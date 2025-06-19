import re
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Any, List

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_tags(text: str) -> List[str]:
    # Basic keyword extraction logic (can be replaced with NLP)
    common_keywords = ["python", "java", "bug", "error", "flutter", "js", "sql"]
    return [word.lower() for word in text.split() if word.lower() in common_keywords]

def clean_text_advanced(text: str) -> str:
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'\n    .+', '', text)
    text = re.sub(r'`[^`]+`', '', text)
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = BeautifulSoup(text, 'html.parser').get_text()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_timestamp(ts: Any) -> str:
    """Parse a timestamp string or object and return ISO 8601 string."""
    if isinstance(ts, str):
        try:
            return datetime.fromisoformat(ts.replace('Z', '+00:00')).isoformat()
        except Exception:
            pass
    if isinstance(ts, datetime):
        return ts.isoformat()
    return str(ts) 