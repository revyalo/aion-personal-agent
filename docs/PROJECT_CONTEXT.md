# Project Context

## Why AION exists

Current AI assistants are usually experienced as isolated conversations attached to a product, device or model. Even when they expose memory, the identity of the assistant is often coupled to a specific provider and its current context-management implementation.

AION explores a different abstraction:

> A personal agent should be a persistent software identity whose models and devices are replaceable components.

The project is motivated by five long-horizon requirements:

1. **Continuity** — remain the same logical agent across restarts, upgrades and devices.
2. **Memory** — preserve relevant history without reducing years of interaction to unreliable summaries.
3. **Presence** — move between desktop and mobile contexts without creating separate personas.
4. **Initiative** — sometimes begin useful or social interaction instead of only responding to commands.
5. **Evolution** — adapt to the user while keeping identity changes bounded, inspectable and reversible.

## What AION is not

AION is not intended to:
- train a foundation model from scratch;
- claim machine consciousness or subjective experience;
- replace established databases, speech models or tool protocols with custom versions for novelty;
- give an LLM unrestricted authority over the operating system;
- store private user memory in the public source repository.

## Primary engineering thesis

The differentiating problem is not raw model intelligence. It is **persistent orchestration around replaceable intelligence**.

AION therefore treats:
- the LLM as a reasoning backend;
- embeddings as rebuildable indexes;
- devices as authenticated peripherals;
- personality as explicit state;
- raw events as historical evidence;
- tools as permissioned capabilities.

## Long-term scenario

A conversation can begin on a desktop, continue on a phone, and later resume on another computer while preserving:
- the same identity;
- the same history;
- the same current goals;
- the same learned interaction preferences;
- the provenance of remembered information.

Years later, a model migration should not erase that history. A new embedding model should trigger re-indexing, not amnesia.
