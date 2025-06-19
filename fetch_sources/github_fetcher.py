import requests

def fetch_github_push_events():
    url = "https://api.github.com/events"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    events = response.json()

    results = []
    for event in events:
        if event.get("type") != "PushEvent":
            continue
        repo_name = event["repo"]["name"]
        for commit in event["payload"]["commits"]:
            results.append({
                "source": "github",
                "timestamp": event["created_at"],
                "text": commit["message"],
                "tags": [],
                "meta": {
                    "repo": repo_name,
                    "lang": "",  # can be filled later using GitHub API
                    "url": f"https://github.com/{repo_name}"
                }
            })
    return results 