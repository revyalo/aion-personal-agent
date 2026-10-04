from aion.memory_candidate import MemoryCandidate


def should_persist_memory(
    candidate: MemoryCandidate,
) -> bool:
    if not candidate.content.strip():
        return False

    if not candidate.source_event_ids:
        return False

    if not 0.0 <= candidate.confidence <= 1.0:
        return False

    if candidate.memory_type == "explicit_user_memory":
        return True

    return False