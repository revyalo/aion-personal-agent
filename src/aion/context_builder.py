def build_conversation_context(
    events: list[dict],
    max_events: int = 6,
    current_user_event_id: str | None = None,
) -> str:
    if current_user_event_id is not None:
        try:
            current_index = next(
                index
                for index, event in enumerate(events)
                if event["event_type"] == "user_message"
                and event["event_id"] == current_user_event_id
            )
        except StopIteration as error:
            raise ValueError(
                "El turno actual no existe en el Event Store."
            ) from error

        # Solo utilizamos eventos registrados hasta
        # el mensaje que estamos procesando.
        events = events[:current_index + 1]

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

    # El presupuesto debe ser positivo.
    if max_events < 1:
        raise ValueError(
            "max_events debe ser mayor que cero."
        )

    # El último evento puede ser una pregunta aún
    # pendiente de respuesta.
    pending_event = (
        conversation_events[-1]
        if conversation_events
        and conversation_events[-1]["event_type"] == "user_message"
        else None
    )

    # Los demás eventos forman parejas completas:
    # pregunta + respuesta.
    complete_events = (
        conversation_events[:-1]
        if pending_event is not None
        else conversation_events
    )

    # Reservamos espacio para la pregunta actual.
    remaining = max_events - (
        1 if pending_event is not None else 0
    )

    # Cada pareja consume dos posiciones.
    pairs_to_keep = remaining // 2

    if pairs_to_keep > 0:
        recent_events = complete_events[-2 * pairs_to_keep:]
    else:
        recent_events = []

    # La pregunta actual siempre se conserva.
    if pending_event is not None:
        recent_events.append(pending_event)


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