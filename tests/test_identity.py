
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest
import aion.database

from aion.identity import load_or_create_identity


def test_identity_is_persistent(tmp_path, monkeypatch):
    test_db = tmp_path / "aion_test.db"
    monkeypatch.setattr(aion.database, "DATABASE_PATH", test_db)

    first_identity = load_or_create_identity()
    second_identity = load_or_create_identity()

    assert first_identity.agent_id == second_identity.agent_id


def test_concurrent_identity_bootstrap(tmp_path, monkeypatch):
    test_db = tmp_path / "aion_test.db"
    monkeypatch.setattr(aion.database, "DATABASE_PATH", test_db)

    # Ocho ejecuciones intentarán arrancar al mismo tiempo.
    barrier = Barrier(8)

    def start_aion(_):
        barrier.wait()
        return load_or_create_identity().agent_id

    with ThreadPoolExecutor(max_workers=8) as executor:
        identities = list(executor.map(start_aion, range(8)))

    # Todas deben recibir exactamente la misma identidad.
    assert len(set(identities)) == 1

    # Y la base solo debe contener una fila.
    with sqlite3.connect(test_db) as connection:
        rows = connection.execute(
            "SELECT agent_id FROM aion_instance"
        ).fetchall()

    assert len(rows) == 1
    assert rows[0][0] == identities[0]


def test_multiple_existing_identities_are_rejected(
    tmp_path, monkeypatch
):
    test_db = tmp_path / "aion_test.db"
    monkeypatch.setattr(aion.database, "DATABASE_PATH", test_db)

    # Simulamos una base antigua con dos identidades.
    with sqlite3.connect(test_db) as connection:
        connection.execute("""
            CREATE TABLE aion_instance (
                agent_id TEXT PRIMARY KEY
            )
        """)

        connection.executemany(
            "INSERT INTO aion_instance (agent_id) VALUES (?)",
            [("identity-A",), ("identity-B",)],
        )

    with pytest.raises(RuntimeError):
        load_or_create_identity()
