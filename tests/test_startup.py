
import sqlite3

import pytest
import aion.database as database

from aion.core import AionCore
from aion.identity import load_or_create_identity
from aion.memory_store import initialize_memory_store
from aion.migrations import migrate_database


def configure_test(tmp_path, monkeypatch):
    path = tmp_path / "aion_test.db"

    monkeypatch.setattr(
        database, "DATABASE_PATH", path
    )
    monkeypatch.setenv("AION_PROVIDER", "mock")
    monkeypatch.setenv("AION_MODELS", "mock")

    return path


def schema_version(path):
    with sqlite3.connect(path) as connection:
        return connection.execute(
            "PRAGMA user_version"
        ).fetchone()[0]


def test_first_start_creates_schema_v1(
    tmp_path, monkeypatch
):
    path = configure_test(tmp_path, monkeypatch)

    core = AionCore()

    assert path.exists()
    assert schema_version(path) == 1
    assert core.identity.agent_id


def test_existing_v1_starts_normally(
    tmp_path, monkeypatch
):
    path = configure_test(tmp_path, monkeypatch)

    first = AionCore()
    second = AionCore()

    assert schema_version(path) == 1
    assert first.identity.agent_id == second.identity.agent_id


def test_legacy_schema_requires_manual_migration(
    tmp_path, monkeypatch
):
    path = configure_test(tmp_path, monkeypatch)

    initialize_memory_store()
    identity = load_or_create_identity().agent_id

    assert schema_version(path) == 0

    with pytest.raises(RuntimeError, match="esquema v0"):
        AionCore()

    assert schema_version(path) == 0

    # Tras migrarla explícitamente, AION puede arrancar.
    migrate_database()

    core = AionCore()
    assert core.identity.agent_id == identity
    assert schema_version(path) == 1

