import json
import math
import os
from typing import Dict, Optional

from database import get_connection
from engine.prompt_builder import COLOUR_SYSTEM_PROMPT, build_colour_prompt
from mistralai import Mistral


def _get_client() -> Mistral:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY not set")
    return Mistral(api_key=api_key)


def generate_colour_forecast(signals: list, lang: str = "en") -> Optional[Dict]:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        return _fallback_colours()

    client = Mistral(api_key=api_key)
    prompt = build_colour_prompt(signals, lang=lang)

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "system", "content": COLOUR_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=2500,
        )

        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        result = json.loads(raw)
        print(f"[colour] Forecast generated — hero: {result.get('hero_colour', {}).get('name', 'n/a')}")
        return result

    except json.JSONDecodeError as e:
        print(f"[colour] JSON parse error: {e}")
        return _fallback_colours()
    except Exception as e:
        print(f"[colour] Mistral error: {e}")
        return _fallback_colours()


def _fallback_colours() -> Dict:
    return {
        "season": "SS26",
        "hero_colour": {
            "name": "Warm Tobacco",
            "hex": "#8B7355",
            "subtitle": "Earthy warmth with intellectual edge",
            "signal_strength": {
                "runway": 88, "street": 72, "search": 85, "editorial": 90
            }
        },
        "colours": [
            {
                "name": "Warm Tobacco", "hex": "#8B7355", "status": "hero",
                "confidence": 94,
                "description": "Earthy warmth dominant across Milan runway and search signals.",
                "combinations": ["#E8D4A8", "#C4B49A", "#4A3728", "#F5F0E8", "#C9A05A"],
                "sources": ["Vogue", "Google Trends"]
            },
            {
                "name": "Sage Whisper", "hex": "#7B9E8C", "status": "rising",
                "confidence": 88,
                "description": "Botanical calm meets quiet luxury in editorial photography.",
                "combinations": ["#E8E0D4", "#C9A05A", "#3D5448", "#F0EBE2", "#8B7355"],
                "sources": ["Harper's Bazaar", "BoF"]
            },
            {
                "name": "Terracotta Dusk", "hex": "#C4876A", "status": "rising",
                "confidence": 82,
                "description": "Mediterranean warmth carried from resort into mainline.",
                "combinations": ["#F5E6D8", "#8B5E3C", "#E8C9A0", "#2C1810", "#D4C4A0"],
                "sources": ["WWD", "Highsnobiety"]
            },
            {
                "name": "Forest Protocol", "hex": "#4A6741", "status": "watching",
                "confidence": 76,
                "description": "Deep botanical driven by sustainability narratives.",
                "combinations": ["#C9D4B8", "#8B7355", "#E8F0E0", "#1C2B19", "#D4C4A0"],
                "sources": ["Dazed", "Reddit"]
            },
            {
                "name": "Lavender Smoke", "hex": "#B8A9C9", "status": "watching",
                "confidence": 71,
                "description": "Muted violet carrying over from FW25 into spring.",
                "combinations": ["#F0EBF4", "#7B6E8A", "#E8D4A8", "#2C2438", "#C9A05A"],
                "sources": ["Vogue Paris", "Elle"]
            },
            {
                "name": "Parchment Lux", "hex": "#D4C4A0", "status": "emerging",
                "confidence": 65,
                "description": "Ultra-refined neutral redefining quiet luxury for 2026.",
                "combinations": ["#8B7355", "#F5F0E8", "#4A3728", "#C9A05A", "#18150f"],
                "sources": ["InStyle", "BoF"]
            }
        ],
        "forecast_next": [
            {"name": "Midnight Cobalt", "hex": "#2C3E5C", "confidence": 88, "season": "FW26"},
            {"name": "Bordeaux Revival", "hex": "#8B3A3A", "confidence": 76, "season": "FW26"},
            {"name": "Raw Linen", "hex": "#C4A882", "confidence": 71, "season": "FW26"},
            {"name": "Graphite Mist", "hex": "#4A4A4A", "confidence": 64, "season": "FW26"}
        ],
        "editorial_analysis": "SS26 gravitates toward earth and botanical tones — a collective retreat from maximalism. Warm Tobacco bridges luxury and utility, two previously opposing forces now converging."
    }

def _hex_to_hsv(hex_color: str) -> tuple:
    """Convert hex to HSV (hue 0-360, saturation 0-1, value 0-1)."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return (0, 0, 0)
    r, g, b = (int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    delta = max_c - min_c

    # Value
    v = max_c

    # Saturation
    s = delta / max_c if max_c != 0 else 0

    # Hue
    if delta == 0:
        h = 0
    elif max_c == r:
        h = 60 * (((g - b) / delta) % 6)
    elif max_c == g:
        h = 60 * (((b - r) / delta) + 2)
    else:
        h = 60 * (((r - g) / delta) + 4)

    return (h, s, v)


def _hex_distance(hex1: str, hex2: str) -> float:
    """
    Euclidean RGB distance with HSV hue check.
    If both colours are saturated (s > 0.15) and their hues differ
    by more than 30 degrees, treat them as different regardless of RGB distance.
    """
    def to_rgb(h):
        h = h.lstrip('#')
        if len(h) != 6:
            return (0, 0, 0)
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    try:
        r1, g1, b1 = to_rgb(hex1)
        r2, g2, b2 = to_rgb(hex2)
        rgb_dist = math.sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)

        # If RGB distance already too large, skip HSV check
        if rgb_dist > 40:
            return rgb_dist

        # HSV hue check — only for saturated colours
        h1, s1, v1 = _hex_to_hsv(hex1)
        h2, s2, v2 = _hex_to_hsv(hex2)

        SAT_THRESHOLD = 0.15
        HUE_THRESHOLD = 30  # degrees

        if s1 > SAT_THRESHOLD and s2 > SAT_THRESHOLD:
            # Ambos saturados — check de hue
            hue_diff = abs(h1 - h2)
            if hue_diff > 180:
                hue_diff = 360 - hue_diff
            if hue_diff > HUE_THRESHOLD:
                return 999
        elif (s1 > SAT_THRESHOLD) != (s2 > SAT_THRESHOLD):
            # Uno saturado, otro gris — siempre distintos
            return 999

        return rgb_dist

    except Exception:
        return 999


def save_colour_forecast(colours: list, lang: str = "en", cycle_id: str = None):
    """Save individual colours from a forecast cycle to SQLite."""
    conn = get_connection()
    for c in colours:
        conn.execute(
            """INSERT INTO colour_forecasts
               (colour_name, hex, status, confidence, lang, cycle_id)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                c.get("name", ""),
                c.get("hex", "#000000"),
                c.get("status", "watching"),
                c.get("confidence", 0),
                lang,
                cycle_id or ""
            )
        )
    conn.commit()
    conn.close()
    print(f"[colour] Saved {len(colours)} colours to forecast history")


def get_colour_consensus(lang: str = "en", days: int = 7, threshold: float = 25.0) -> list:
    """
    Group colours by hex proximity and return ranked consensus.
    X=25 distance threshold — colours within this distance are grouped.
    """
    conn = get_connection()
    rows = conn.execute(
        """SELECT colour_name, hex, confidence, recorded_at
           FROM colour_forecasts
           WHERE lang = ?
           AND recorded_at >= datetime('now', ?)
           ORDER BY recorded_at DESC""",
        (lang, f"-{days} days")
    ).fetchall()
    conn.close()

    if not rows:
        return []

    # Count total cycles for frequency calculation
    conn = get_connection()
    total_cycles = conn.execute(
        """SELECT COUNT(DISTINCT cycle_id) as cnt
           FROM colour_forecasts
           WHERE lang = ?
           AND recorded_at >= datetime('now', ?)""",
        (lang, f"-{days} days")
    ).fetchone()["cnt"]
    conn.close()

    # Group colours by hex proximity
    groups = []

    for row in rows:
        hex_val = row["hex"]
        name    = row["colour_name"]
        conf    = row["confidence"]

        matched = False
        for group in groups:
            if _hex_distance(hex_val, group["representative_hex"]) <= threshold:
                group["appearances"] += 1
                group["total_confidence"] += conf
                group["names"].add(name)
                # Update representative to highest confidence name
                if conf > group["best_confidence"]:
                    group["best_name"]       = name
                    group["best_hex"]        = hex_val
                    group["best_confidence"] = conf
                    # group["representative_hex"] = hex_val
                matched = True
                break

        if not matched:
            groups.append({
                "representative_hex": hex_val,
                "best_name":          name,
                "best_hex":           hex_val,
                "best_confidence":    conf,
                "appearances":        1,
                "total_confidence":   conf,
                "names":              {name},
            })

    # Calculate avg confidence and sort by appearances desc
    result = []
    for g in groups:
        avg_conf    = round(g["total_confidence"] / g["appearances"])
        freq_pct    = round((g["appearances"] / max(total_cycles * 6, 1)) * 100)
        aliases     = list(g["names"] - {g["best_name"]})[:4]

        # Badge based on frequency
        if freq_pct >= 60:
            badge = "dominant"
        elif freq_pct >= 35:
            badge = "strong"
        else:
            badge = "emerging"

        result.append({
            "name":         g["best_name"],
            "hex":          g["best_hex"],
            "appearances":  g["appearances"],
            "total_cycles": total_cycles * 6,
            "avg_confidence": avg_conf,
            "freq_pct":     freq_pct,
            "badge":        badge,
            "aliases":      aliases,
        })

    result.sort(key=lambda x: (x["appearances"], x["avg_confidence"]), reverse=True)
    return result[:8]

def save_colour_forecast_next(forecast_next: list, lang: str = "en", cycle_id: str = None):
    """Save FW26 forecast colours to SQLite for future consensus."""
    conn = get_connection()
    for c in forecast_next:
        conn.execute(
            """INSERT INTO colour_forecasts
               (colour_name, hex, status, confidence, lang, cycle_id)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                c.get("name", ""),
                c.get("hex", "#000000"),
                "forecast",
                c.get("confidence", 0),
                f"{lang}_fw26",
                cycle_id or ""
            )
        )
    conn.commit()
    conn.close()
    print(f"[colour] Saved {len(forecast_next)} FW26 forecast colours")