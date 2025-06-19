import logging
import requests
from typing import List, Dict, Any
from .utils import parse_timestamp

logger = logging.getLogger(__name__)


def fetch_github_push_events() -> List[Dict[str, Any]]:
    """Fetch recent GitHub PushEvents and extract commit messages, repo info, and language."""
    url = "https://api.github.com/events"
    headers = {"Accept": "application/vnd.github.v3+json"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        events = resp.json()
    except Exception as e:
        logger.error(f"Failed to fetch GitHub events: {e}")
        return []
    results = []
    for event in events:
        if event.get("type") != "PushEvent":
            continue
        repo_name = event["repo"]["name"]
        for commit in event["payload"]["commits"]:
            results.append({
                "source": "github",
                "timestamp": parse_timestamp(event["created_at"]),
                "text": commit["message"],
                "tags": [],
                "meta": {
                    "repo": repo_name,
                    "lang": "",  # can be filled later using GitHub API
                    "url": f"https://github.com/{repo_name}"
                }
            })
    logger.info(f"Fetched {len(results)} GitHub PushEvents")
    return results 