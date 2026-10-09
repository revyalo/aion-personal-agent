import pytest
import aion.database

from aion.instance_lock import (
    InstanceAlreadyRunningError,
    single_instance_lock,
)


def test_second_instance_is_rejected(tmp_path, monkeypatch):
    test_db = tmp_path / "aion_test.db"
    monkeypatch.setattr(
        aion.database, "DATABASE_PATH", test_db
    )

    with single_instance_lock():
        # Simulamos otro intento de adquirir el bloqueo.
        with pytest.raises(InstanceAlreadyRunningError):
            with single_instance_lock():
                pass


def test_lock_is_released_after_exit(tmp_path, monkeypatch):
    test_db = tmp_path / "aion_test.db"
    monkeypatch.setattr(
        aion.database, "DATABASE_PATH", test_db
    )

    with single_instance_lock():
        pass

    # Una vez liberado debe poder adquirirse otra vez.
    with single_instance_lock():
        pass


def test_lock_is_released_after_error(tmp_path, monkeypatch):
    test_db = tmp_path / "aion_test.db"
    monkeypatch.setattr(
        aion.database, "DATABASE_PATH", test_db
    )

    with pytest.raises(ValueError):
        with single_instance_lock():
            raise ValueError("Error simulado")

    # La excepción no debe dejar el bloqueo retenido.
    with single_instance_lock():
        pass

