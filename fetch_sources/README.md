# Data Collection Module

This module is responsible for gathering information from various technology platforms. It collects data from GitHub, Stack Overflow, and Reddit to understand what developers are working on and discussing.

## How It Works

### 1. GitHub Collector (`github_fetcher.py`)
This component tracks GitHub activity:
- Fetches recent push events from GitHub's public API
- Extracts commit messages and repository information
- Collects repository names and URLs
- Handles API rate limits and errors gracefully

### 2. Stack Overflow Collector (`so_fetcher.py`)
This part focuses on developer questions:
- Fetches recent questions from Stack Overflow API
- Collects question titles, tags, and scores
- Monitors activity-based sorting
- Retrieves question URLs for reference

### 3. Reddit Collector (`reddit_fetcher.py`)
This component analyzes programming discussions:
- Fetches posts from r/learnprogramming, r/AskProgramming, and r/cscareerquestions
- Collects post titles, scores, and URLs
- Uses PRAW library for Reddit API access
- Requires Reddit API credentials

### 4. Utilities (`utils.py`)
This helper module contains common tools:
- Timestamp parsing functions
- Data formatting utilities
- Error handling helpers

## How to Use

1. Set up your Reddit API credentials in `.env`:
   ```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_SECRET=your_client_secret
   ```

2. Run the main collection script:
   ```bash
   python run_fetch.py
   ```

3. Or use individual collectors:
   ```python
   from fetch_sources import github_fetcher, so_fetcher, reddit_fetcher
   
   # Collect from specific platforms
   github_data = github_fetcher.fetch_github_push_events()
   so_data = so_fetcher.fetch_stackoverflow_questions()
   reddit_data = reddit_fetcher.fetch_reddit_posts()
   ```

## Data Format

All collectors format their data consistently:
```json
{
    "source": "platform_name",
    "timestamp": "2024-03-20T10:30:00Z",
    "text": "The main content (commit message, question title, or post title)",
    "tags": ["relevant", "tags"],
    "meta": {
        "repo": "repository_name",  // GitHub only
        "url": "source_url",
        "score": 42,  // Stack Overflow/Reddit
        "lang": ""    // GitHub (placeholder)
    }
}
```

## Configuration

### GitHub
- Uses public API (no authentication required)
- Fetches recent push events
- Extracts commit messages and repo info

### Stack Overflow
- Uses Stack Exchange API
- Fetches 30 most recent questions
- Sorts by activity

### Reddit
- Requires Reddit API credentials
- Fetches 25 posts from each subreddit
- Monitors programming-related communities

## Error Handling

The module includes error handling for:
- Network connection issues
- API rate limits
- Missing credentials
- Invalid data formats

## Output

Data is saved to `fetched_data.json` in the project root directory, containing all collected information in a unified format ready for analysis. 