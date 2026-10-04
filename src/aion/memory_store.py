import uuid
from datetime import datetime, timezone

from aion.database import get_connection
from aion.event_store import initialize_event_store


def initialize_memory_store():
    initialize_event_store()

    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            memory_id TEXT PRIMARY KEY,
            memory_type TEXT NOT NULL,
            content TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS memory_sources (
            memory_id TEXT NOT NULL,
            event_id TEXT NOT NULL,

            PRIMARY KEY (memory_id, event_id),

            FOREIGN KEY (memory_id)
                REFERENCES memories(memory_id)
                ON DELETE CASCADE,

            FOREIGN KEY (event_id)
                REFERENCES events(event_id)
        )
    """)

    connection.commit()
    connection.close()

def create_memory(
    memory_type: str,
    content: str,
    source_event_ids: list[str],
    confidence: float = 1.0,
) -> str:
    if not source_event_ids:
        raise ValueError("A memory must have at least one source event")

    if not 0.0 <= confidence <= 1.0:
        raise ValueError("Confidence must be between 0.0 and 1.0")

    initialize_memory_store()

    memory_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO memories (
                memory_id,
                memory_type,
                content,
                confidence,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            memory_id,
            memory_type,
            content,
            confidence,
            created_at,
        ))

        for event_id in source_event_ids:
            connection.execute("""
                INSERT INTO memory_sources (
                    memory_id,
                    event_id
                )
                VALUES (?, ?)
            """, (
                memory_id,
                event_id,
            ))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return memory_id

def get_memories() -> list[dict]:
    connection = get_connection()

    rows = connection.execute("""
        SELECT
            memory_id,
            memory_type,
            content,
            confidence,
            created_at
        FROM memories
        ORDER BY created_at ASC
    """).fetchall()

    memories = []

    for row in rows:
        source_rows = connection.execute("""
            SELECT event_id
            FROM memory_sources
            WHERE memory_id = ?
        """, (row[0],)).fetchall()

        memories.append({
            "memory_id": row[0],
            "memory_type": row[1],
            "content": row[2],
            "confidence": row[3],
            "created_at": row[4],
            "source_event_ids": [
                source[0] for source in source_rows
            ],
        })

    connection.close()

    return memories