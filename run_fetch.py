from fetch_sources.github_fetcher import fetch_github_push_events
from fetch_sources.so_fetcher import fetch_stackoverflow_questions
from fetch_sources.reddit_fetcher import fetch_reddit_posts
from fetch_sources.utils import clean_text, extract_tags
import json

def run_all():
    all_data = (
        fetch_github_push_events()
        + fetch_stackoverflow_questions()
        + fetch_reddit_posts()
    )

    # Normalize and clean
    for d in all_data:
        d["text"] = clean_text(d["text"])
        if not d["tags"]:
            d["tags"] = extract_tags(d["text"])

    with open("fetched_data.json", "w") as f:
        json.dump(all_data, f, indent=2)

    print(f"Fetched {len(all_data)} entries ✅")

if __name__ == "__main__":
    run_all() 