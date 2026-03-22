from engine.snapshot_store import get_latest_snapshot, get_velocity_history
from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from pipeline import run_pipeline

router = APIRouter(prefix="/api")


@router.get("/health")
def health():
    return {"status": "ok", "service": "PULSE Fashion Intelligence"}


@router.get("/dashboard")
def get_dashboard(lang: str = Query("en", regex="^(en|es)$")):
    snapshot = get_latest_snapshot(lang=lang)
    if not snapshot:
        # No snapshot for this lang yet — trigger generation
        run_pipeline(lang=lang)
        snapshot = get_latest_snapshot(lang=lang)
    if not snapshot:
        raise HTTPException(status_code=503, detail="No dashboard data yet.")
    return snapshot


@router.get("/archive")
def get_archive(lang: str = Query("en", regex="^(en|es)$"), limit: int = 10):
    conn = __import__('database').get_connection()
    rows = conn.execute(
        """SELECT payload, generated_at, signal_count
           FROM dashboard_snapshots
           WHERE lang = ?
           ORDER BY id DESC LIMIT ?""",
        (lang, limit)
    ).fetchall()
    conn.close()

    result = []
    for row in rows:
        import json
        payload = json.loads(row["payload"])
        payload["generated_at"] = row["generated_at"]
        payload["signal_count"] = row["signal_count"]
        result.append(payload)
    return result


@router.get("/velocity-history")
def get_history(days: int = 7):
    return get_velocity_history(days=days)


@router.post("/refresh")
def manual_refresh(background_tasks: BackgroundTasks, lang: str = Query("en", regex="^(en|es)$")):
    background_tasks.add_task(run_pipeline, lang=lang)
    return {"status": f"refresh triggered for lang={lang}"}


@router.get("/heatmap")
def get_heatmap(days: int = 28):
    """Returns daily signal count for the last N days — for the activity heatmap."""
    conn = __import__('database').get_connection()
    rows = conn.execute(
        """SELECT DATE(generated_at) as day, COUNT(*) as count
           FROM dashboard_snapshots
           WHERE generated_at >= datetime('now', ?)
           GROUP BY DATE(generated_at)
           ORDER BY day ASC""",
        (f"-{days} days",)
    ).fetchall()
    conn.close()
    return [{"day": row["day"], "count": row["count"]} for row in rows]


@router.get("/velocity-chart")
def get_velocity_chart(days: int = 7, lang: str = Query("en", regex="^(en|es)$")):
    conn = __import__('database').get_connection()
    rows = conn.execute(
        """SELECT DATE(generated_at) as day,
                  AVG(json_extract(payload, '$.kpis.top_velocity')) as avg_velocity,
                  AVG(json_extract(payload, '$.kpis.active_signals')) as avg_signals,
                  COUNT(*) as snapshots
           FROM dashboard_snapshots
           WHERE generated_at >= datetime('now', ?)
           AND lang = ?
           AND json_extract(payload, '$.kpis.top_velocity') > 0
           GROUP BY DATE(generated_at)
           ORDER BY day ASC""",
        (f"-{days} days", lang)
    ).fetchall()
    conn.close()
    return [
        {
            "day": row["day"],
            "velocity": round(row["avg_velocity"] or 0),
            "signals": round(row["avg_signals"] or 0),
            "snapshots": row["snapshots"]
        }
        for row in rows
    ]

@router.get("/colours")
def get_colours(lang: str = Query("en", regex="^(en|es)$")):
    from datetime import datetime

    from database import get_connection
    from engine.colour_engine import (_fallback_colours,
                                      generate_colour_forecast,
                                      save_colour_forecast,
                                      save_colour_forecast_next)

    conn = get_connection()
    rows = conn.execute(
        """SELECT DISTINCT source, title, content FROM raw_signals
           WHERE fetched_at >= datetime('now', '-48 hours')
           ORDER BY fetched_at DESC
           LIMIT 80"""
    ).fetchall()
    conn.close()

    if not rows:
        return _fallback_colours()

    signals = [
        {"source": r["source"], "title": r["title"], "content": r["content"] or ""}
        for r in rows
    ]

    result = generate_colour_forecast(signals, lang=lang)
    cycle_id = datetime.utcnow().strftime("%Y%m%d%H%M")

    # Guardar SS26 colours
    save_colour_forecast(result.get("colours", []), lang=lang, cycle_id=cycle_id)

    # Guardar FW26 forecast — acumulando para consenso futuro
    save_colour_forecast_next(result.get("forecast_next", []), lang=lang, cycle_id=cycle_id)

    return result


@router.get("/colours/consensus")
def get_colours_consensus(
    lang: str = Query("en", regex="^(en|es)$"),
    days: int = 7,
    threshold: float = 25.0
):
    from engine.colour_engine import get_colour_consensus
    return get_colour_consensus(lang=lang, days=days, threshold=threshold)

@router.get("/colours/consensus/fw26")
def get_colours_consensus_fw26(
    lang: str = Query("en", regex="^(en|es)$"),
    days: int = 30,
    threshold: float = 25.0
):
    """FW26 colour consensus — needs more data to be meaningful."""
    from engine.colour_engine import get_colour_consensus
    return get_colour_consensus(lang=f"{lang}_fw26", days=days, threshold=threshold)

