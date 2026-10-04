import aion.database

from aion.event_store import append_event
from aion.memory_store import (
    initialize_memory_store,
    create_memory,
    get_memories,
)

def test_memory_keeps_source_provenance(tmp_path, monkeypatch):
    test_db = tmp_path / "aion_test.db"

    monkeypatch.setattr(
        aion.database,
        "DATABASE_PATH",
        test_db
    )

    initialize_memory_store()

    event_id = append_event(
        "user_message",
        {
            "text": "Carolina es amiga de David."
        }
    )

    memory_id = create_memory(
        memory_type="relationship",
        content="Carolina es amiga de David.",
        source_event_ids=[event_id],
        confidence=1.0,
    )

    memories = get_memories()

    memory = next(
        item
        for item in memories
        if item["memory_id"] == memory_id
    )

    assert memory["content"] == "Carolina es amiga de David."
    assert memory["confidence"] == 1.0
    assert event_id in memory["source_event_ids"]