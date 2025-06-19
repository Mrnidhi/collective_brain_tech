import re

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def extract_tags(text):
    # Basic keyword extraction logic (can be replaced with NLP)
    common_keywords = ["python", "java", "bug", "error", "flutter", "js", "sql"]
    return [word.lower() for word in text.split() if word.lower() in common_keywords] 