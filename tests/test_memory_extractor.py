from aion.memory_extractor import extract_memory_candidates


def test_explicit_memory_creates_candidate():
    candidates = extract_memory_candidates(
        "recuerda que mi comida favorita es la lasaña",
        "event-1",
    )

    assert len(candidates) == 1

    candidate = candidates[0]

    assert candidate.memory_type == "explicit_user_memory"
    assert candidate.content == "mi comida favorita es la lasaña"
    assert candidate.confidence == 1.0
    assert candidate.source_event_ids == ["event-1"]


def test_normal_message_does_not_create_candidate():
    candidates = extract_memory_candidates(
        "hola AION",
        "event-2",
    )

    assert candidates == []