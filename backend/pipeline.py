from collectors.reddit_collector import collect_reddit
from collectors.rss_collector import collect_rss
from collectors.trends_collector import collect_trends
from engine.llm_client import _fallback_dashboard, generate_dashboard
from engine.snapshot_store import (save_raw_signals, save_snapshot,
                                   save_velocity)


def run_pipeline(lang: str = "en"):
    """
    Main pipeline: collect → process → store.
    Called by APScheduler every N minutes and on manual refresh.
    """
    print(f"[pipeline] Starting refresh cycle (lang={lang})...")

    # 1. Collect from all sources
    rss_signals = collect_rss()
    reddit_signals = collect_reddit()
    trend_signals = collect_trends()

    all_signals = rss_signals + reddit_signals + trend_signals
    print(f"[pipeline] Total signals collected: {len(all_signals)}")

    if not all_signals:
        print("[pipeline] No signals collected — skipping LLM call")
        return

    # 2. Persist raw signals to SQLite
    save_raw_signals(all_signals)

    # 3. Generate dashboard via LLM
    dashboard = generate_dashboard(all_signals, lang=lang)

    if dashboard is None:
        print("[pipeline] LLM failed — using fallback dashboard")
        dashboard = _fallback_dashboard(all_signals)

    # 4. Save velocity data for historical chart
    for term in dashboard.get("search_terms", []):
        save_velocity(term.get("term", ""), term.get("velocity", 0), term.get("region", "global"))

    # 5. Save snapshot
    save_snapshot(dashboard, len(all_signals), lang=lang)
    print(f"[pipeline] Refresh cycle complete (lang={lang}).")
