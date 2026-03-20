from typing import List, Dict
from datetime import datetime

FASHION_TERMS = [
    "linen blazer",
    "wide leg trousers",
    "quiet luxury",
    "gorpcore",
    "ballet flat",
    "sheer top",
    "cargo pants",
    "workwear fashion",
    "streetwear 2026",
    "fashion week",
]

GEO_REGIONS = {
    "ES": "Spain",
    "FR": "France",
    "IT": "Italy",
    "GB": "United Kingdom",
    "US": "United States",
    "JP": "Japan",
    "KR": "South Korea",
}


def collect_trends() -> List[Dict]:
    """
    Collect Google Trends data for fashion terms.
    Uses pytrends — install separately: pip install pytrends
    Falls back to mock data if pytrends fails (rate limiting is common).
    """
    signals = []

    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl="en-US", tz=0, timeout=(10, 25))

        # Build payload in batches of 5 (pytrends limit)
        batch = FASHION_TERMS[:5]
        pytrends.build_payload(batch, timeframe="now 7-d", geo="")
        interest_df = pytrends.interest_over_time()

        if not interest_df.empty:
            latest = interest_df.iloc[-1]
            for term in batch:
                if term in latest:
                    velocity = int(latest[term])
                    signals.append({
                        "id": f"trends_{term.replace(' ', '_')}",
                        "source": "Google Trends · Global",
                        "title": f'"{term}" trending globally',
                        "content": f"Search interest score: {velocity}/100 over the past 7 days.",
                        "url": f"https://trends.google.com/trends/explore?q={term.replace(' ', '+')}",
                        "region": "global",
                        "fetched_at": datetime.utcnow().isoformat(),
                        "velocity": velocity,
                    })

        print(f"[trends] Collected {len(signals)} trend signals")

    except ImportError:
        print("[trends] pytrends not installed, using mock data")
        signals = _mock_trends()
    except Exception as e:
        print(f"[trends] Error (likely rate limited): {e} — using mock data")
        signals = _mock_trends()

    return signals


def _mock_trends() -> List[Dict]:
    """Fallback mock data when pytrends is rate-limited."""
    mock_data = [
        ("linen blazer", 94, "Europe"),
        ("wide leg trousers", 78, "Global"),
        ("quiet luxury", 65, "US"),
        ("ballet flat", 58, "Europe"),
        ("gorpcore", 42, "Global"),
    ]
    return [
        {
            "id": f"trends_mock_{term.replace(' ', '_')}",
            "source": f"Google Trends · {region}",
            "title": f'"{term}" is trending',
            "content": f"Search velocity: {vel}/100 this week.",
            "url": "",
            "region": "global",
            "fetched_at": datetime.utcnow().isoformat(),
            "velocity": vel,
        }
        for term, vel, region in mock_data
    ]
