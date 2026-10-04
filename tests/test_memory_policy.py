from aion.memory_candidate import MemoryCandidate
from aion.memory_policy import should_persist_memory


def test_explicit_user_memory_is_allowed():
    candidate = MemoryCandidate(
        memory_type="explicit_user_memory",
        content="mi comida favorita es la lasaña",
        confidence=1.0,
        source_event_ids=["event-1"],
    )

    assert should_persist_memory(candidate) is True


def test_unknown_memory_type_is_rejected():
    candidate = MemoryCandidate(
        memory_type="model_guess",
        content="Carolina siente algo por David",
        confidence=0.7,
        source_event_ids=["event-2"],
    )

    assert should_persist_memory(candidate) is False


def test_memory_without_source_is_rejected():
    candidate = MemoryCandidate(
        memory_type="explicit_user_memory",
        content="mi comida favorita es la lasaña",
        confidence=1.0,
        source_event_ids=[],
    )

    assert should_persist_memory(candidate) is False