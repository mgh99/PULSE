import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pulse.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS raw_signals (
            id          TEXT PRIMARY KEY,
            source      TEXT NOT NULL,
            title       TEXT,
            content     TEXT,
            url         TEXT,
            region      TEXT DEFAULT 'global',
            fetched_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
            processed   INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS dashboard_snapshots (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            payload         TEXT NOT NULL,
            generated_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
            signal_count    INTEGER DEFAULT 0,
            lang            TEXT DEFAULT 'en'
        );

        CREATE TABLE IF NOT EXISTS trend_velocity (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            term        TEXT NOT NULL,
            velocity    REAL DEFAULT 0,
            region      TEXT DEFAULT 'global',
            recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS colour_forecasts (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            colour_name  TEXT NOT NULL,
            hex          TEXT NOT NULL,
            status       TEXT,
            confidence   INTEGER DEFAULT 0,
            lang         TEXT DEFAULT 'en',
            cycle_id     TEXT,
            recorded_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()
    print("[db] Database initialized.")
