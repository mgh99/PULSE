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

COLOUR_SYSTEM_PROMPT = """You are a colour forecasting editor at PULSE, a global fashion intelligence platform.

You receive live fashion signals and your job is to identify and predict the dominant colours of the coming season.
You think like a senior colour forecaster at Pantone or WGSN — authoritative, precise, editorial.

You must respond with ONLY a valid JSON object. No preamble, no markdown, no explanation.
"""

COLOUR_OUTPUT_SCHEMA = {
    "season": "string — e.g. 'SS26' or 'FW26'",
    "hero_colour": {
        "name": "string — editorial colour name (e.g. 'Warm Tobacco', not just 'brown')",
        "hex": "string — approximate hex code",
        "subtitle": "string — one evocative line about this colour",
        "signal_strength": {
            "runway": "integer 0-100",
            "street": "integer 0-100",
            "search": "integer 0-100",
            "editorial": "integer 0-100"
        }
    },
    "colours": [
        {
            "name": "string — editorial colour name",
            "hex": "string — approximate hex code",
            "status": "hero | rising | watching | emerging",
            "confidence": "integer 0-100",
            "description": "string — max 20 words, why this colour is emerging",
            "combinations": ["list of 4-5 hex codes that pair well with this colour"],
            "sources": ["list of 2-3 source names that signal this colour"]
        }
    ],
    "forecast_next": [
        {
            "name": "string — editorial colour name",
            "hex": "string — approximate hex code",
            "confidence": "integer 0-100",
            "season": "string — e.g. 'FW26'"
        }
    ],
    "editorial_analysis": "string — 2-3 sentences from a senior colour editor. Max 50 words."
}


def build_colour_prompt(signals: list, lang: str = "en") -> str:
    signal_text = "\n".join([
        f"- [{s.get('source', 'unknown')}] {s.get('title', '')} | {s.get('content', '')[:150]}"
        for s in signals[:15]
    ])

    schema_str = json.dumps(COLOUR_OUTPUT_SCHEMA, indent=2)

    lang_instruction = (
        "Respond entirely in Spanish. All colour names, descriptions, and analysis must be in Spanish."
        if lang == "es"
        else "Respond entirely in English."
    )

    return f"""Here are the latest fashion signals:

{signal_text}

---

{lang_instruction}

Analyse these signals and identify the dominant and emerging colours for the coming season.
Return ONLY valid JSON matching this schema exactly:

{schema_str}

Rules:
- colour names must be editorial and evocative, never generic (not 'brown', but 'Warm Tobacco')
- hex codes should be realistic approximations of the colour described
- combinations should be harmonious palettes that a stylist would actually use
- confidence scores should reflect actual signal strength, not be uniformly high
- include exactly 6 colours in the colours array
- include exactly 4 colours in forecast_next
- status 'hero' for the single most dominant colour, 'rising' for strong signals, 'watching' for emerging, 'emerging' for early signals
"""


def build_prompt(signals: List[Dict], lang: str = "en") -> str:
    signal_text = "\n".join([
        f"- [{s.get('source', 'unknown')}] {s.get('title', '')} | {s.get('content', '')[:200]}"
        for s in signals[:15]
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
