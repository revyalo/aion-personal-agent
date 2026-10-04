import aion.database
from aion.identity import load_or_create_identity


def test_identity_is_persistent(tmp_path, monkeypatch):
    test_db = tmp_path / "aion_test.db"
    monkeypatch.setattr(aion.database, "DATABASE_PATH", test_db)

    first_identity = load_or_create_identity()
    second_identity = load_or_create_identity()

    assert first_identity.agent_id == second_identity.agent_id