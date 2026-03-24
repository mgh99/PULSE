import json
import os
from typing import Dict, Optional

import httpx
from engine.prompt_builder import SYSTEM_PROMPT, build_prompt


def generate_dashboard(signals: list, lang: str = "en") -> Optional[Dict]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")

    prompt = build_prompt(signals, lang=lang)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": SYSTEM_PROMPT + "\n\n" + prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 3000,
        }
    }

    try:
        with httpx.Client(timeout=60) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()

        data = response.json()
        raw = data["candidates"][0]["content"]["parts"][0]["text"].strip()

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
        print(f"[llm] Gemini API error: {e}")
        return None


def _fallback_dashboard(signals: list) -> Dict:
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
        "editorial_brief": "Collecting the latest signals from global fashion sources. Please wait for the first analysis."
    }