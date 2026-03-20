import json
from datetime import datetime
from typing import Dict, List, Optional

from database import get_connection


def save_snapshot(payload: Dict, signal_count: int, lang: str = "en"):
    conn = get_connection()
    conn.execute(
        "INSERT INTO dashboard_snapshots (payload, signal_count, lang) VALUES (?, ?, ?)",
        (json.dumps(payload), signal_count, lang)
    )
    conn.commit()
    conn.close()
    print(f"[store] Snapshot saved ({signal_count} signals, lang={lang})")


def get_latest_snapshot(lang: str = "en") -> Optional[Dict]:
    conn = get_connection()
    row = conn.execute(
        """SELECT payload, generated_at FROM dashboard_snapshots
           WHERE lang = ? ORDER BY id DESC LIMIT 1""",
        (lang,)
    ).fetchone()
    conn.close()

    if not row:
        return None

    payload = json.loads(row["payload"])
    payload["generated_at"] = row["generated_at"]
    return payload


def save_raw_signals(signals: List[Dict]):
    conn = get_connection()
    for s in signals:
        conn.execute(
            """INSERT OR IGNORE INTO raw_signals
               (id, source, title, content, url, region, fetched_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                s["id"], s["source"], s["title"],
                s.get("content", ""), s.get("url", ""),
                s.get("region", "global"), s.get("fetched_at", datetime.utcnow().isoformat())
            )
        )
    conn.commit()
    conn.close()


def save_velocity(term: str, velocity: float, region: str = "global"):
    conn = get_connection()
    conn.execute(
        "INSERT INTO trend_velocity (term, velocity, region) VALUES (?, ?, ?)",
        (term, velocity, region)
    )
    conn.commit()
    conn.close()


def get_velocity_history(days: int = 7) -> List[Dict]:
    conn = get_connection()
    rows = conn.execute(
        """SELECT term, velocity, region, recorded_at
           FROM trend_velocity
           WHERE recorded_at >= datetime('now', ?)
           ORDER BY recorded_at DESC""",
        (f"-{days} days",)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
