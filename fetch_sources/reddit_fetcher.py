import praw
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    user_agent="collective-brain"
)

SUBS = ["learnprogramming", "AskProgramming", "cscareerquestions"]

def fetch_reddit_posts(limit=25):
    results = []
    for sub in SUBS:
        for post in reddit.subreddit(sub).new(limit=limit):
            results.append({
                "source": "reddit",
                "timestamp": datetime.utcfromtimestamp(post.created_utc).isoformat() + 'Z',
                "text": post.title,
                "tags": [sub],
                "meta": {
                    "score": post.score,
                    "url": f"https://reddit.com{post.permalink}"
                }
            })
    return results 