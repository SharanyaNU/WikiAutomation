"""SQLite storage. The schema lives in schema.sql and is applied on first use."""

import sqlite3
from pathlib import Path

from flask import current_app, g

SCHEMA = Path(__file__).with_name("schema.sql")


def connect() -> sqlite3.Connection:
    if "db" not in g:
        path = current_app.config["DATABASE"]
        if path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(path)
        g.db.row_factory = sqlite3.Row
        g.db.executescript(SCHEMA.read_text(encoding="utf-8"))
    return g.db


def close(_error=None) -> None:
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_app(app) -> None:
    app.teardown_appcontext(close)


def add_learner(name: str, email: str) -> int:
    conn = connect()
    cur = conn.execute("INSERT INTO learners (name, email) VALUES (?, ?)", (name, email))
    conn.execute("INSERT INTO enrollments (learner_id, course) VALUES (?, ?)", (cur.lastrowid, "ai-engineer"))
    conn.commit()
    return int(cur.lastrowid)


def get_learner(learner_id: int) -> dict | None:
    row = connect().execute(
        "SELECT l.id, l.name, l.email, e.course, e.enrolled_at FROM learners l "
        "JOIN enrollments e ON e.learner_id = l.id WHERE l.id = ?", (learner_id,)
    ).fetchone()
    return dict(row) if row else None
