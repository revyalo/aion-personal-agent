from aion.config import Config
from aion.context_builder import (
    build_conversation_context,
    build_memory_context,
)
from aion.event_store import append_event, get_events
from aion.identity import load_or_create_identity
from aion.identity_kernel import build_identity_kernel
from aion.memory_extractor import extract_memory_candidates
from aion.memory_policy import should_persist_memory
from aion.memory_store import (
    create_memory,
    get_memories,
    initialize_memory_store,
)
from aion.providers.factory import create_provider


class AionCore:
    def __init__(self):
        # Prepara Event Store + Memory Store.
        initialize_memory_store()

        # Carga configuración.
        self.config = Config()

        # Recupera la identidad persistente de AION.
        self.identity = load_or_create_identity()

        # Crea el router/proveedor con la cadena de modelos configurada.
        self.provider = create_provider(
            self.config.provider,
            self.config.models,
        )

    def chat(self, message: str) -> str:
        # 1. Guardamos el mensaje del usuario como evento canónico.
        user_event_id = append_event(
            "user_message",
            {
                "text": message,
            },
        )

        # 2. Buscamos posibles recuerdos en el mensaje.
        memory_candidates = extract_memory_candidates(
            message,
            user_event_id,
        )

        # 3. La Memory Policy decide cuáles pueden persistirse.
        for candidate in memory_candidates:
            if should_persist_memory(candidate):
                create_memory(
                    memory_type=candidate.memory_type,
                    content=candidate.content,
                    source_event_ids=candidate.source_event_ids,
                    confidence=candidate.confidence,
                )

        # 4. Recuperamos eventos y memorias persistentes.
        events = get_events()
        memories = get_memories()

        # 5. Construimos el contexto reciente de conversación.
        conversation_context = build_conversation_context(
            events
        )

        # 6. Construimos el contexto de memoria persistente.
        memory_context = build_memory_context(
            memories
        )

        # 7. Unimos memoria + conversación.
        context = f"""
PERSISTENT MEMORY:
{memory_context}

CONVERSATION HISTORY:
{conversation_context}
""".strip()

        # 8. Construimos el Identity Kernel.
        system_instruction = build_identity_kernel(
            self.identity.agent_id
        )

        # 9. Pedimos una respuesta al Provider Router.
        try:
            response = self.provider.generate(
                context,
                system_instruction,
            )

        except Exception as error:
            append_event(
                "provider_error",
                {
                    "user_event_id": user_event_id,
                    "error_type": error.__class__.__name__,
                },
            )

            raise

        # 10. Guardamos la respuesta y la vinculamos
        # con el mensaje concreto del usuario.
        append_event(
            "assistant_message",
            {
                "text": response,
                "reply_to_user_event_id": user_event_id,
            },
        )

        return response