
import sqlite3

import pytest
import aion.database as database

from aion.identity import load_or_create_identity
from aion.event_store import append_event, get_events
from aion.memory_store import (
    initialize_memory_store,
    create_memory,
    get_memories,
)
from aion.migrations import migrate_database


def prepare_legacy_database(tmp_path, monkeypatch):
    path = tmp_path / "aion_test.db"

    monkeypatch.setattr(database, "DATABASE_PATH", path)

    initialize_memory_store()
    identity = load_or_create_identity().agent_id

    return path, identity


def test_migration_preserves_data(tmp_path, monkeypatch):
    path, identity = prepare_legacy_database(
        tmp_path, monkeypatch
    )

    event_id = append_event(
        "user_message",
        {"text": "recuerda que me gusta Python"},
    )

    memory_id = create_memory(
        memory_type="explicit_user_memory",
        content="me gusta Python",
        source_event_ids=[event_id],
    )

    assert migrate_database() == 1

    with sqlite3.connect(path) as connection:
        version = connection.execute(
            "PRAGMA user_version"
        ).fetchone()[0]

        # Intentar añadir una segunda identidad debe fallar.
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO aion_instance VALUES (?)",
                ("otra-identidad",),
            )

    assert version == 1
    assert load_or_create_identity().agent_id == identity
    assert get_events()[0]["event_id"] == event_id

    memories = get_memories()
    assert memories[0]["memory_id"] == memory_id
    assert memories[0]["source_event_ids"] == [event_id]

    # Ejecutarla nuevamente no debe modificar nada.
    assert migrate_database() == 1


def test_rejects_multiple_legacy_identities(
    tmp_path, monkeypatch
):
    path, _ = prepare_legacy_database(
        tmp_path, monkeypatch
    )

    with sqlite3.connect(path) as connection:
        connection.execute(
            "INSERT INTO aion_instance VALUES (?)",
            ("otra-identidad",),
        )

    with pytest.raises(RuntimeError):
        migrate_database()

    with sqlite3.connect(path) as connection:
        assert connection.execute(
            "PRAGMA user_version"
        ).fetchone()[0] == 0

        assert connection.execute(
            "SELECT COUNT(*) FROM aion_instance"
        ).fetchone()[0] == 2


def test_rejects_future_schema(tmp_path, monkeypatch):
    path, _ = prepare_legacy_database(
        tmp_path, monkeypatch
    )

    with sqlite3.connect(path) as connection:
        connection.execute("PRAGMA user_version = 2")

    with pytest.raises(RuntimeError):
        migrate_database()

    with sqlite3.connect(path) as connection:
        assert connection.execute(
            "PRAGMA user_version"
        ).fetchone()[0] == 2


def test_missing_database_is_not_created(
    tmp_path, monkeypatch
):
    path = tmp_path / "missing.db"
    monkeypatch.setattr(database, "DATABASE_PATH", path)

    with pytest.raises(FileNotFoundError):
        migrate_database()

    assert not path.exists()

