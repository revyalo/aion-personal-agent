from dataclasses import dataclass


@dataclass
class MemoryCandidate:
    memory_type: str
    content: str
    confidence: float
    source_event_ids: list[str]