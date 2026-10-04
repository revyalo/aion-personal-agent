from aion.memory_candidate import MemoryCandidate


EXPLICIT_MEMORY_PREFIXES = (
    "recuerda que ",
    "acuérdate de que ",
    "acuerdate de que ",
    "quiero que recuerdes que ",
)


def extract_memory_candidates(
    message: str,
    source_event_id: str,
) -> list[MemoryCandidate]:
    normalized_message = message.strip()

    if not normalized_message:
        return []

    lower_message = normalized_message.lower()

    for prefix in EXPLICIT_MEMORY_PREFIXES:
        if lower_message.startswith(prefix):
            content = normalized_message[len(prefix):].strip()

            if not content:
                return []

            candidate = MemoryCandidate(
                memory_type="explicit_user_memory",
                content=content,
                confidence=1.0,
                source_event_ids=[
                    source_event_id,
                ],
            )

            return [candidate]

    return []