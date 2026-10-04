import json
import uuid
from datetime import datetime, timezone

from aion.database import get_connection

def initialize_event_store():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS events (
            seq INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id TEXT UNIQUE NOT NULL,
            event_type TEXT NOT NULL,
            payload TEXT NOT NULL,
            occurred_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def append_event(event_type: str, payload: dict):
    connection = get_connection()

    event_id = str(uuid.uuid4())
    occurred_at = datetime.now(timezone.utc).isoformat()

    connection.execute("""
        INSERT INTO events (
            event_id,
            event_type,
            payload,
            occurred_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        event_id,
        event_type,
        json.dumps(payload),
        occurred_at
    ))

    connection.commit()
    connection.close()

    return event_id

def get_events():
    connection = get_connection()

    rows = connection.execute("""
        SELECT
            seq,
            event_id,
            event_type,
            payload,
            occurred_at
        FROM events
        ORDER BY seq ASC
    """).fetchall()

    connection.close()

    events = []

    for row in rows:
        events.append({
            "seq": row[0],
            "event_id": row[1],
            "event_type": row[2],
            "payload": json.loads(row[3]),
            "occurred_at": row[4]
        })

    return events