import os
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from api.routes import router
from database import init_db
from pipeline import run_pipeline

REFRESH_MINUTES = int(os.getenv("REFRESH_INTERVAL_MINUTES", "15"))

scheduler = BackgroundScheduler()


def run_both_languages():
    run_pipeline(lang="en")
    run_pipeline(lang="es")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("[main] Initializing database...")
    init_db()

    print(f"[main] Starting scheduler — refresh every {REFRESH_MINUTES} min")
    scheduler.add_job(run_both_languages, "interval", minutes=REFRESH_MINUTES, id="pipeline")
    scheduler.start()

    print("[main] Running initial pipeline on startup...")
    run_pipeline(lang="en")
    run_pipeline(lang="es")

    yield

    # Shutdown
    scheduler.shutdown()
    print("[main] Scheduler stopped.")


app = FastAPI(
    title="PULSE — Fashion Intelligence API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)