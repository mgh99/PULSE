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
    """Returns max velocity per day for the sparkline charts."""
    conn = __import__('database').get_connection()
    rows = conn.execute(
        """SELECT DATE(generated_at) as day,
                  MAX(json_extract(payload, '$.kpis.top_velocity')) as max_velocity
           FROM dashboard_snapshots
           WHERE generated_at >= datetime('now', ?)
           AND lang = ?
           GROUP BY DATE(generated_at)
           ORDER BY day ASC""",
        (f"-{days} days", lang)
    ).fetchall()
    conn.close()
    return [{"day": row["day"], "velocity": row["max_velocity"] or 0} for row in rows]
