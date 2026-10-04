import aion.database

from aion.core import AionCore
from aion.memory_store import get_memories


def test_explicit_memory_is_persisted_through_core(
    tmp_path,
    monkeypatch,
):
    # Base de datos temporal exclusiva para este test.
    test_db = tmp_path / "aion_test.db"

    monkeypatch.setattr(
        aion.database,
        "DATABASE_PATH",
        test_db,
    )

    # No queremos llamar a Gemini durante los tests.
    monkeypatch.setenv(
        "AION_PROVIDER",
        "mock",
    )

    monkeypatch.setenv(
        "AION_MODELS",
        "mock",
    )

    # Creamos una instancia de AION.
    core = AionCore()

    # Hablamos con él como lo haría el usuario real.
    core.chat(
        "recuerda que mi color favorito es el verde"
    )

    # Consultamos la memoria persistente.
    memories = get_memories()

    assert len(memories) == 1

    memory = memories[0]

    assert memory["memory_type"] == "explicit_user_memory"
    assert memory["content"] == "mi color favorito es el verde"
    assert memory["confidence"] == 1.0
    assert len(memory["source_event_ids"]) == 1  