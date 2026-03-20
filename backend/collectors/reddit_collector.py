import os
from datetime import datetime
from typing import Dict, List

import praw

SUBREDDITS = [
    {"name": "femalefashionadvice", "region": "global"},
    {"name": "streetwear", "region": "global"},
    {"name": "malefashionadvice", "region": "global"},
    {"name": "fashionadvice", "region": "global"},
]


def _get_reddit_client():
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT", "pulse-dashboard/1.0"),
    )


def collect_reddit() -> List[Dict]:
    signals = []

    # If no Reddit credentials, return empty gracefully
    if not os.getenv("REDDIT_CLIENT_ID") or not os.getenv("REDDIT_CLIENT_SECRET"):
        print("[reddit] No credentials found, skipping.")
        return signals

    try:
        reddit = _get_reddit_client()

        for sub_info in SUBREDDITS:
            subreddit = reddit.subreddit(sub_info["name"])
            posts = list(subreddit.hot(limit=10))

            for post in posts:
                if post.score < 50:  # filter low-engagement posts
                    continue

                signals.append({
                    "id": f"reddit_{post.id}",
                    "source": f"Reddit · r/{sub_info['name']}",
                    "title": post.title,
                    "content": post.selftext[:400] if post.selftext else post.title,
                    "url": f"https://reddit.com{post.permalink}",
                    "region": sub_info["region"],
                    "fetched_at": datetime.utcnow().isoformat(),
                    "score": post.score,
                })

            print(f"[reddit] r/{sub_info['name']}: {len(posts)} posts fetched")

    except Exception as e:
        print(f"[reddit] Error: {e}")

    return signals


def collect_reddit_trends() -> List[str]:
    """Return top trending terms from Reddit titles for LLM context."""
    signals = collect_reddit()
    return [s["title"] for s in signals[:20]]
