
import shutil
import sqlite3

import pytest
import aion.database as database

from aion.backup import create_backup, verify_backup
from aion.identity import load_or_create_identity
from aion.event_store import append_event, get_events
from aion.memory_store import (
    initialize_memory_store,
    create_memory,
    get_memories,
)


def test_backup_and_restore_roundtrip(tmp_path, monkeypatch):
    source = tmp_path / "original.db"
    monkeypatch.setattr(database, "DATABASE_PATH", source)

    initialize_memory_store()
    identity = load_or_create_identity().agent_id

    event_id = append_event(
        "user_message",
        {"text": "recuerda que me gusta Python"},
    )

    memory_id = create_memory(
        memory_type="explicit_user_memory",
        content="me gusta Python",
        source_event_ids=[event_id],
    )

    backup_path = tmp_path / "backup.db"
    create_backup(backup_path)

    report = verify_backup(backup_path)

    assert report["agent_id"] == identity
    assert report["events"] == 1
    assert report["memories"] == 1
    assert report["memory_sources"] == 1

    # Modificamos el original después de la copia.
    append_event(
        "user_message",
        {"text": "mensaje posterior"},
    )

    # Simulamos restauración en OTRO archivo temporal.
    restored = tmp_path / "restored.db"
    shutil.copy2(backup_path, restored)

    monkeypatch.setattr(
        database, "DATABASE_PATH", restored
    )

    assert load_or_create_identity().agent_id == identity

    events = get_events()
    memories = get_memories()

    assert len(events) == 1
    assert events[0]["event_id"] == event_id

    assert len(memories) == 1
    assert memories[0]["memory_id"] == memory_id
    assert memories[0]["source_event_ids"] == [event_id]


def test_existing_backup_is_not_overwritten(
    tmp_path, monkeypatch
):
    source = tmp_path / "original.db"
    monkeypatch.setattr(database, "DATABASE_PATH", source)

    initialize_memory_store()
    load_or_create_identity()

    destination = tmp_path / "backup.db"
    destination.write_bytes(b"NO SOBRESCRIBIR")

    with pytest.raises(FileExistsError):
        create_backup(destination)

    assert destination.read_bytes() == b"NO SOBRESCRIBIR"


def test_missing_source_is_not_created(
    tmp_path, monkeypatch
):
    source = tmp_path / "missing.db"
    monkeypatch.setattr(database, "DATABASE_PATH", source)

    destination = tmp_path / "backup.db"

    with pytest.raises(FileNotFoundError):
        create_backup(destination)

    assert not source.exists()
    assert not destination.exists()


def test_invalid_database_is_rejected(
    tmp_path, monkeypatch
):
    source = tmp_path / "invalid.db"
    monkeypatch.setattr(database, "DATABASE_PATH", source)

    # SQLite válida, pero sin las tablas de AION.
    with sqlite3.connect(source):
        pass

    destination = tmp_path / "backup.db"

    with pytest.raises(RuntimeError):
        create_backup(destination)

    assert not destination.exists()

