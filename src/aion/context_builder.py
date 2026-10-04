def build_conversation_context(
    events: list[dict],
    max_events: int = 6,
) -> str:
    # Mensajes de usuario cuyo turno terminó con error.
    failed_user_event_ids = {
        event["payload"]["user_event_id"]
        for event in events
        if event["event_type"] == "provider_error"
        and "user_event_id" in event["payload"]
    }

    # Para poder encontrar un user_message concreto por su event_id.
    user_events = {
        event["event_id"]: event
        for event in events
        if event["event_type"] == "user_message"
    }

    conversation_events = []
    paired_user_event_ids = set()

    # Último mensaje de usuario todavía sin respuesta.
    pending_user_event = None

    for event in events:
        event_type = event["event_type"]

        if event_type == "user_message":
            # Si sabemos que este turno falló, no lo consideramos pendiente.
            if event["event_id"] in failed_user_event_ids:
                continue

            # Si aparecen varios mensajes seguidos sin respuesta,
            # conservamos como pendiente el más reciente.
            pending_user_event = event

        elif event_type == "assistant_message":
            reply_to_user_event_id = event["payload"].get(
                "reply_to_user_event_id"
            )

            # Turnos nuevos: usamos la relación explícita.
            if reply_to_user_event_id is not None:
                user_event = user_events.get(
                    reply_to_user_event_id
                )

                if (
                    user_event is not None
                    and reply_to_user_event_id
                    not in failed_user_event_ids
                    and reply_to_user_event_id
                    not in paired_user_event_ids
                ):
                    conversation_events.append(user_event)
                    conversation_events.append(event)

                    paired_user_event_ids.add(
                        reply_to_user_event_id
                    )

                if (
                    pending_user_event is not None
                    and pending_user_event["event_id"]
                    == reply_to_user_event_id
                ):
                    pending_user_event = None

            # Compatibilidad con respuestas antiguas,
            # creadas antes de implementar turn linking.
            elif pending_user_event is not None:
                user_event_id = pending_user_event["event_id"]

                if user_event_id not in paired_user_event_ids:
                    conversation_events.append(
                        pending_user_event
                    )
                    conversation_events.append(event)

                    paired_user_event_ids.add(
                        user_event_id
                    )

                pending_user_event = None

    # Cuando Core construye el contexto, el mensaje actual todavía
    # no tiene respuesta. Lo añadimos al final.
    if (
        pending_user_event is not None
        and pending_user_event["event_id"]
        not in failed_user_event_ids
        and pending_user_event["event_id"]
        not in paired_user_event_ids
    ):
        conversation_events.append(
            pending_user_event
        )

    # Limitamos el contexto después de reconstruir los turnos válidos.
    recent_events = conversation_events[-max_events:]

    lines = []

    for event in recent_events:
        event_type = event["event_type"]
        payload = event["payload"]

        if event_type == "user_message":
            lines.append(
                f"User: {payload['text']}"
            )

        elif event_type == "assistant_message":
            lines.append(
                f"AION: {payload['text']}"
            )

    return "\n".join(lines)


def build_memory_context(
    memories: list[dict],
) -> str:
    if not memories:
        return "No persistent memories available."

    lines = []

    for memory in memories:
        lines.append(
            f"- {memory['content']} "
            f"(confidence: {memory['confidence']})"
        )

    return "\n".join(lines)