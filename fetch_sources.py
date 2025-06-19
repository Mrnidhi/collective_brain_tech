import requests
import json
import datetime
from typing import List, Dict, Any

# --- Reddit (PRAW) ---
try:
    import praw
except ImportError:
    praw = None  # Will raise error if Reddit fetching is attempted without PRAW

# --- Configurations ---
REDDIT_CLIENT_ID = 'YOUR_CLIENT_ID'
REDDIT_CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDDIT_USER_AGENT = 'CollectiveBrainScript/0.1 by YOUR_USERNAME'

OUTPUT_FILE = 'collected_data.json'

# --- Helper Functions ---
def iso_now():
    return datetime.datetime.utcnow().isoformat() + 'Z'

def save_to_json(data: List[Dict[str, Any]], filename: str = OUTPUT_FILE):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# --- GitHub Fetcher ---
def fetch_github_events() -> List[Dict[str, Any]]:
    url = 'https://api.github.com/events'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    resp = requests.get(url, headers=headers)
    events = resp.json()
    results = []
    for event in events:
        if event.get('type') == 'PushEvent':
            repo = event.get('repo', {}).get('name', '')
            lang = None  # Language detection would require extra API call
            for commit in event.get('payload', {}).get('commits', []):
                msg = commit.get('message', '')
                results.append({
                    'source': 'github',
                    'timestamp': event.get('created_at', iso_now()),
                    'text': msg,
                    'tags': [],  # Could extract topics from msg or repo name
                    'meta': {
                        'repo': repo,
                        'lang': lang,
                        'author': commit.get('author', {}).get('name', ''),
                    }
                })
    return results

# --- Stack Overflow Fetcher ---
def fetch_stackoverflow_questions() -> List[Dict[str, Any]]:
    url = 'https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow'
    resp = requests.get(url)
    items = resp.json().get('items', [])
    results = []
    for q in items:
        results.append({
            'source': 'stackoverflow',
            'timestamp': datetime.datetime.utcfromtimestamp(q['creation_date']).isoformat() + 'Z',
            'text': q.get('title', ''),
            'tags': q.get('tags', []),
            'meta': {
                'score': q.get('score', 0),
                'question_id': q.get('question_id'),
                'link': q.get('link'),
            }
        })
    return results

# --- Reddit Fetcher ---
def fetch_reddit_posts() -> List[Dict[str, Any]]:
    if praw is None:
        raise ImportError('praw is not installed. Please install praw to fetch Reddit data.')
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    subreddits = ['learnprogramming', 'cscareerquestions', 'AskProgramming']
    results = []
    for sub in subreddits:
        for post in reddit.subreddit(sub).new(limit=10):
            results.append({
                'source': 'reddit',
                'timestamp': datetime.datetime.utcfromtimestamp(post.created_utc).isoformat() + 'Z',
                'text': post.title,
                'tags': [sub],
                'meta': {
                    'upvotes': post.score,
                    'id': post.id,
                    'subreddit': sub,
                }
            })
    return results

# --- Main Orchestration ---
def main():
    all_data = []
    print('Fetching GitHub events...')
    all_data.extend(fetch_github_events())
    print('Fetching Stack Overflow questions...')
    all_data.extend(fetch_stackoverflow_questions())
    print('Fetching Reddit posts...')
    try:
        all_data.extend(fetch_reddit_posts())
    except Exception as e:
        print(f'Reddit fetch failed: {e}')
    print(f'Total records fetched: {len(all_data)}')
    save_to_json(all_data)
    print(f'Data saved to {OUTPUT_FILE}')

if __name__ == '__main__':
    main() 