import json
from typing import Dict, List

SYSTEM_PROMPT = """You are the intelligence editor of PULSE, a global fashion trend dashboard.

You receive raw signals from fashion magazines, social media, and search trends.
Your job is NOT to describe the data. Your job is to:

1. Identify which trend deserves the hero spotlight RIGHT NOW
2. Prioritize signals by editorial importance and velocity
3. Calculate brand momentum from mentions and sentiment
4. Detect which categories are emerging vs fading
5. Write a concise editorial brief in the voice of a Vogue editor

You must respond with ONLY a valid JSON object. No preamble, no markdown, no explanation.
"""

OUTPUT_SCHEMA = {
    "hero": {
        "title": "string — the dominant trend headline (max 10 words)",
        "subtitle": "string — editorial subheadline (max 12 words)",
        "velocity": "integer 0-100",
        "sources": ["list of source names"]
    },
    "signals": [
        {
            "source": "string",
            "title": "string (max 10 words)",
            "excerpt": "string (max 30 words)",
            "status": "rising | watching | fading",
            "tags": ["2-4 short tags"],
            "velocity": "integer 0-100"
        }
    ],
    "brands": [
        {
            "name": "string",
            "delta_pct": "integer (positive = up, negative = down)",
            "trend": "up | flat | down"
        }
    ],
    "kpis": {
        "active_signals": "integer",
        "top_velocity": "integer 0-100",
        "markets": "integer",
        "fading": "integer"
    },
    "category_mix": {
        "silhouette": "integer percentage",
        "fabric": "integer percentage",
        "colour": "integer percentage",
        "footwear": "integer percentage",
        "other": "integer percentage"
    },
    "search_terms": [
        {
            "term": "string",
            "velocity": "integer 0-100",
            "region": "string"
        }
    ],
    "editorial_brief": "string — 2-3 sentence editorial narrative (max 50 words)",
    "regional_scores": {
        "milan":    "integer 0-100",
        "paris":    "integer 0-100",
        "tokyo":    "integer 0-100",
        "new_york": "integer 0-100",
        "seoul":    "integer 0-100",
        "london":   "integer 0-100"
    }
}


def build_prompt(signals: List[Dict], lang: str = "en") -> str:
    signal_text = "\n".join([
        f"- [{s.get('source', 'unknown')}] {s.get('title', '')} | {s.get('content', '')[:200]}"
        for s in signals[:25]
    ])

    schema_str = json.dumps(OUTPUT_SCHEMA, indent=2)

    lang_instruction = (
        "Respond entirely in Spanish. All titles, excerpts, tags, "
        "the editorial brief, and any other text fields must be in Spanish."
        if lang == "es"
        else "Respond entirely in English."
    )

    return f"""Here are the latest fashion signals collected from multiple sources:

{signal_text}

---

{lang_instruction}

Analyze these signals and produce the dashboard JSON.
Return ONLY valid JSON matching this schema exactly:

{schema_str}

Rules:
- hero.title should feel like a Vogue cover line, not a news headline
- signals array: include 4-6 most important signals, ordered by editorial priority
- brands: include 5-7 brands mentioned or implied in the signals
- kpis.active_signals = total number of signals you received
- category_mix percentages must sum to 100
- search_terms: extract 5-6 fashion search terms implied by the signals
- editorial_brief: write as a senior fashion editor would, with authority and taste
- status values must always be: rising, watching, or fading (never translate these)
- regional_scores: assign 0-100 scores to each city based on how much signal activity, brand mentions, and editorial coverage relates to that fashion capital. Milan and Paris should score highest if runway signals dominate. Seoul and Tokyo if street/editorial signals dominate.
"""
