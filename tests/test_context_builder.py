from aion.context_builder import build_conversation_context
import pytest

def test_failed_user_turn_is_not_included():
    events = [
        {
            "event_id": "user-1",
            "event_type": "user_message",
            "payload": {
                "text": "¿Yo le gusto a Caro?"
            },
        },
        {
            "event_id": "error-1",
            "event_type": "provider_error",
            "payload": {
                "user_event_id": "user-1",
                "error_type": "ProviderQuotaExceeded",
            },
        },
        {
            "event_id": "user-2",
            "event_type": "user_message",
            "payload": {
                "text": "Hola AION"
            },
        },
    ]

    context = build_conversation_context(
        events,
        max_events=10,
    )

    assert "¿Yo le gusto a Caro?" not in context
    assert "User: Hola AION" in context


def test_orphan_user_message_is_not_attached_to_later_response():
    events = [
        {
            "event_id": "user-1",
            "event_type": "user_message",
            "payload": {
                "text": "python3 -m aion.cli"
            },
        },
        {
            "event_id": "user-2",
            "event_type": "user_message",
            "payload": {
                "text": "?"
            },
        },
        {
            "event_id": "assistant-1",
            "event_type": "assistant_message",
            "payload": {
                "text": "¿En qué puedo ayudarte?"
            },
        },
    ]

    context = build_conversation_context(
        events,
        max_events=10,
    )

    assert "python3 -m aion.cli" not in context
    assert "User: ?" in context
    assert "AION: ¿En qué puedo ayudarte?" in context

def test_explicit_turn_linking_overrides_event_order():
    events = [
        {
            "event_id": "user-1",
            "event_type": "user_message",
            "payload": {
                "text": "Primera pregunta"
            },
        },
        {
            "event_id": "user-2",
            "event_type": "user_message",
            "payload": {
                "text": "Segunda pregunta"
            },
        },
        {
            "event_id": "assistant-1",
            "event_type": "assistant_message",
            "payload": {
                "text": "Respuesta a la primera",
                "reply_to_user_event_id": "user-1",
            },
        },
    ]

    context = build_conversation_context(
        events,
        max_events=10,
    )

    expected = (
        "User: Primera pregunta\n"
        "AION: Respuesta a la primera\n"
        "User: Segunda pregunta"
    )

    assert context == expected


def test_current_turn_ignores_later_user_messages():
    events = [
        {
            "event_id": "user-a",
            "event_type": "user_message",
            "payload": {"text": "Pregunta A"},
        },
        {
            "event_id": "user-b",
            "event_type": "user_message",
            "payload": {"text": "Pregunta B"},
        },
    ]

    context = build_conversation_context(
        events,
        current_user_event_id="user-a",
    )

    assert context == "User: Pregunta A"


def test_missing_current_turn_is_rejected():
    with pytest.raises(ValueError):
        build_conversation_context(
            [],
            current_user_event_id="missing",
        )


def test_odd_budget_preserves_complete_pair():
    events = [
        {
            "event_id": "u1",
            "event_type": "user_message",
            "payload": {"text": "Pregunta 1"},
        },
        {
            "event_id": "a1",
            "event_type": "assistant_message",
            "payload": {
                "text": "Respuesta 1",
                "reply_to_user_event_id": "u1",
            },
        },
        {
            "event_id": "u2",
            "event_type": "user_message",
            "payload": {"text": "Pregunta 2"},
        },
        {
            "event_id": "a2",
            "event_type": "assistant_message",
            "payload": {
                "text": "Respuesta 2",
                "reply_to_user_event_id": "u2",
            },
        },
    ]

    context = build_conversation_context(
        events, max_events=3
    )

    assert context == (
        "User: Pregunta 2\n"
        "AION: Respuesta 2"
    )


def test_pending_turn_keeps_latest_complete_pair():
    events = [
        {
            "event_id": "u1",
            "event_type": "user_message",
            "payload": {"text": "Pregunta 1"},
        },
        {
            "event_id": "a1",
            "event_type": "assistant_message",
            "payload": {
                "text": "Respuesta 1",
                "reply_to_user_event_id": "u1",
            },
        },
        {
            "event_id": "u2",
            "event_type": "user_message",
            "payload": {"text": "Pregunta 2"},
        },
        {
            "event_id": "a2",
            "event_type": "assistant_message",
            "payload": {
                "text": "Respuesta 2",
                "reply_to_user_event_id": "u2",
            },
        },
        {
            "event_id": "u3",
            "event_type": "user_message",
            "payload": {"text": "Pregunta actual"},
        },
    ]

    context = build_conversation_context(
        events, max_events=4
    )

    assert context == (
        "User: Pregunta 2\n"
        "AION: Respuesta 2\n"
        "User: Pregunta actual"
    )


def test_zero_event_budget_is_rejected():
    with pytest.raises(ValueError):
        build_conversation_context([], max_events=0)
