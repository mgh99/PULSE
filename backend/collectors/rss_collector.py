import hashlib
from datetime import datetime
from typing import Dict, List

import feedparser

RSS_FEEDS = {
    "vogue": {
        "url": "https://www.vogue.com/feed/rss",
        "region": "global",
        "label": "Vogue"
    },
    "bof": {
        "url": "https://www.businessoffashion.com/rss",
        "region": "global",
        "label": "Business of Fashion"
    },
    "harpers": {
        "url": "https://www.harpersbazaar.com/rss/all.xml",
        "region": "global",
        "label": "Harper's Bazaar"
    },
    "refinery29": {
        "url": "https://www.refinery29.com/rss.xml",
        "region": "global",
        "label": "Refinery29"
    },
    "wwd": {
        "url": "https://wwd.com/feed/",
        "region": "global",
        "label": "WWD"
    },
    "elle": {
        "url": "https://www.elle.com/rss/all.xml/",
        "region": "global",
        "label": "Elle"
    },
    "instyle": {
        "url": "https://www.instyle.com/rss/all.xml",
        "region": "global",
        "label": "InStyle"
    },
    "highsnobiety": {
        "url": "https://www.highsnobiety.com/feed/",
        "region": "global",
        "label": "Highsnobiety"
    },
    "vogue_paris": {
        "url": "https://www.vogue.fr/rss/all.xml",
        "region": "paris",
        "label": "Vogue Paris"
    },
    "hypebeast": {
        "url": "https://hypebeast.com/feed",
        "region": "global",
        "label": "Hypebeast"
    },
    "dazed": {
        "url": "https://www.dazeddigital.com/rss",
        "region": "london",
        "label": "Dazed Digital"
    },
}

FASHION_KEYWORDS = [
    "trend", "fashion", "style", "collection", "runway", "designer",
    "luxury", "brand", "season", "wear", "outfit", "look", "aesthetic",
    "silhouette", "fabric", "couture", "streetwear", "editorial",
    "ss26", "fw26", "spring", "summer", "fall", "winter",
    "milan", "paris", "new york", "london", "tokyo", "seoul",
    "prada", "gucci", "chanel", "dior", "saint laurent", "bottega",
    "lemaire", "sacai", "acne", "balenciaga", "loewe", "celine"
]


def _is_fashion_relevant(title: str, summary: str) -> bool:
    text = (title + " " + summary).lower()
    return any(kw in text for kw in FASHION_KEYWORDS)


def _make_id(source: str, url: str) -> str:
    return hashlib.md5(f"{source}:{url}".encode()).hexdigest()


def collect_rss() -> List[Dict]:
    signals = []

    for key, feed_info in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(feed_info["url"])
            entries = feed.entries[:10]  # max 10 per feed

            for entry in entries:
                title = entry.get("title", "")
                summary = entry.get("summary", entry.get("description", ""))
                url = entry.get("link", "")

                if not _is_fashion_relevant(title, summary):
                    continue

                signals.append({
                    "id": _make_id(key, url),
                    "source": feed_info["label"],
                    "title": title,
                    "content": summary[:500],
                    "url": url,
                    "region": feed_info["region"],
                    "fetched_at": datetime.utcnow().isoformat(),
                })

            print(f"[rss] {feed_info['label']}: {len(signals)} signals collected")

        except Exception as e:
            print(f"[rss] Error fetching {feed_info['label']}: {e}")

    return signals
