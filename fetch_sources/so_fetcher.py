import requests
from datetime import datetime

def fetch_stackoverflow_questions():
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "order": "desc",
        "sort": "activity",
        "site": "stackoverflow",
        "pagesize": 30
    }
    resp = requests.get(url, params=params)
    data = resp.json()

    results = []
    for item in data["items"]:
        results.append({
            "source": "stackoverflow",
            "timestamp": datetime.utcfromtimestamp(item["creation_date"]).isoformat() + 'Z',
            "text": item["title"],
            "tags": item["tags"],
            "meta": {
                "score": item["score"],
                "url": item["link"]
            }
        })
    return results 