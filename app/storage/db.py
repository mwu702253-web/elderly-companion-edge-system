import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path("data/elderly_companion.db")

def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_conn() as conn:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS env_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT,
                temperature REAL,
                humidity REAL,
                smoke REAL,
                gas REAL,
                alert TEXT
            )
            '''
        )
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                time_text TEXT,
                status TEXT DEFAULT 'pending'
            )
            '''
        )

def insert_env_record(record: dict, alert: str):
    with get_conn() as conn:
        conn.execute(
            '''
            INSERT INTO env_records (created_at, temperature, humidity, smoke, gas, alert)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                record["created_at"],
                record["temperature"],
                record["humidity"],
                record["smoke"],
                record["gas"],
                alert,
            ),
        )

def get_recent_env_records(limit: int = 10):
    with get_conn() as conn:
        return pd.read_sql_query(
            "SELECT created_at, temperature, humidity, smoke, gas, alert FROM env_records ORDER BY id DESC LIMIT ?",
            conn,
            params=(limit,),
        )

def insert_reminder(title: str, time_text: str):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO reminders (title, time_text) VALUES (?, ?)",
            (title, time_text),
        )

def get_reminders():
    with get_conn() as conn:
        return pd.read_sql_query(
            "SELECT title, time_text, status FROM reminders ORDER BY id DESC",
            conn,
        )
