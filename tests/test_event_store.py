import aion.database

from aion.event_store import (
    initialize_event_store,
    append_event,
    get_events,
)


def test_event_can_be_stored(tmp_path, monkeypatch):
    test_db = tmp_path / "aion_test.db"
    monkeypatch.setattr(aion.database, "DATABASE_PATH", test_db)

    initialize_event_store()

    event_id = append_event(
        "test_event",
        {"text": "AION test"}
    )

    events = get_events()

    assert any(
        event["event_id"] == event_id
        for event in events
    )