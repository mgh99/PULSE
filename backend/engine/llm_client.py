import json
import os
from typing import Dict, Optional

from engine.prompt_builder import SYSTEM_PROMPT, build_prompt
from mistralai import Mistral


def _get_client() -> Mistral:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY not set in environment")
    return Mistral(api_key=api_key)


def generate_dashboard(signals: list, lang: str = "en") -> Optional[Dict]:
    client = _get_client()
    prompt = build_prompt(signals, lang=lang)

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
            max_tokens=3000,
        )

        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        dashboard = json.loads(raw)
        dashboard["lang"] = lang
        print(f"[llm] Dashboard generated ({lang}) — hero: {dashboard.get('hero', {}).get('title', 'n/a')}")
        return dashboard

    except json.JSONDecodeError as e:
        print(f"[llm] JSON parse error: {e}")
        return None
    except Exception as e:
        print(f"[llm] Mistral API error: {e}")
        return None


def _fallback_dashboard(signals: list) -> Dict:
    """
    Returns a minimal valid dashboard structure when LLM fails.
    Prevents the frontend from breaking.
    """
    return {
        "hero": {
            "title": "Fashion intelligence loading...",
            "subtitle": "Collecting signals from global sources",
            "velocity": 0,
            "sources": []
        },
        "signals": [],
        "brands": [],
        "kpis": {
            "active_signals": len(signals),
            "top_velocity": 0,
            "markets": 6,
            "fading": 0
        },
        "category_mix": {
            "silhouette": 25,
            "fabric": 20,
            "colour": 20,
            "footwear": 15,
            "other": 20
        },
        "search_terms": [],
        "editorial_brief": "Collecting the latest signals from global fashion sources. Please wait for the first analysis.",
        "regional_scores": {
            "milan":    88,
            "paris":    81,
            "tokyo":    74,
            "new_york": 69,
            "seoul":    62,
            "london":   55
        }
    }
