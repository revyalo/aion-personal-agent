# A.I.O.N.

**Adaptive Intelligence Orchestration Nexus**

A research-oriented personal AI agent focused on **persistent identity, long-term memory, proactive interaction, cross-device continuity and secure tool use**.

AION is not intended to be another chat UI around a language model. The project explores a harder systems question:

> **Can a personal AI agent preserve a coherent identity and relationship with its user across years, model upgrades and multiple devices, while remaining useful, auditable and secure?**

## Core idea

AION is treated as an entity that is **independent from any single model, application or device**.

```text
AION != LLM
AION != device
AION != conversation

AION =
    identity
  + memory
  + history
  + state
  + learned behaviour
  + capabilities
```

The LLM is a replaceable reasoning engine. Windows, macOS and Android clients are peripherals through which the same persistent AION instance can observe, converse and act.

## Design principles

- **Continuity first.** The process may stop; the identity should persist.
- **Raw events are the source of truth.** Summaries, embeddings and graphs are derived and rebuildable.
- **Memory requires evidence.** Important memories should retain provenance to their original events.
- **Identity and personality are different.** A stable identity kernel is separated from slowly evolving, auditable traits.
- **Proactivity is event-driven.** Cheap deterministic filters decide whether an event deserves deeper reasoning.
- **Model agnostic.** Reasoning providers should be replaceable without destroying AION's identity or history.
- **Security before autonomy.** Tool access is capability-based, least-privilege and confirmation-gated for sensitive actions.
- **Private by design.** Personal memory is never committed to the source repository.

## Long-term vision

A mature AION should be able to:

- maintain conversations over months and years;
- recall relevant past interactions with temporal context and evidence;
- distinguish current facts from historical facts and changed preferences;
- adapt interaction style without uncontrolled personality drift;
- initiate useful or social conversation without becoming intrusive;
- move naturally between desktop and mobile clients while preserving one identity;
- use tools, files and applications under explicit permissions;
- support multiple reasoning models and local models;
- explain why it remembers something and where that memory originated;
- remain testable through objective memory, proactivity, safety and latency metrics.

## Initial architecture

```text
                    AION CORE
       +--------------------------------+
       | Identity                       |
       | Event Log                      |
       | Memory                         |
       | Context                        |
       | Personality                    |
       | Reasoning / Model Router       |
       | Proactivity                    |
       | Tool & Permission Gateway      |
       +---------------+----------------+
                       |
              secure client protocol
                       |
          +------------+-------------+
          |            |             |
       Windows       macOS        Android
        client       client        client
```

The initial implementation deliberately starts much smaller: one text client, one Core process, SQLite, a model-provider abstraction and persistent memories.

## Research questions

- **RQ1 — Long-term memory:** How can AION preserve useful personal memory for years without accumulating noise, contradictions or unverifiable summaries?
- **RQ2 — Identity continuity:** How can personality adapt while a stable, auditable identity survives model and prompt changes?
- **RQ3 — Proactivity:** How can the agent initiate conversation at useful moments without becoming intrusive or expensive?
- **RQ4 — Cross-device continuity:** How can one canonical agent state be preserved across heterogeneous clients and intermittent connectivity?
- **RQ5 — Agent security:** How can AION use powerful tools while resisting indirect prompt injection, confused-deputy failures and accidental destructive actions?

## Milestones

Development is organized around named milestones rather than a fixed deadline.

- **H0 — Foundations:** scope, literature, threat model and architecture baseline.
- **H1 — Birth:** persistent identity, text conversation, event log and provider abstraction.
- **H2 — Remember:** episodic/semantic memory with provenance and retrieval.
- **H3 — Consolidate:** temporal facts, contradictions, evidence lineage and memory maintenance.
- **H4 — Voice:** low-latency speech interaction with local wake/VAD components.
- **H5 — Initiative:** event-driven proactive conversation and interruption control.
- **H6 — Hands:** tools, permissions, sandboxing and agent-security evaluation.
- **H7 — Presence:** Core/client split and cross-device continuity.
- **H8 — Evolve:** auditable adaptive personality and behavioural learning.
- **H9 — Intelligence:** model routing, evaluation-driven selection and optional local models.
- **H10 — Harden:** long-horizon evaluation, reliability, migration and recovery.
- **H11 — AION 1.0:** persistent personal agent with memory, voice, initiative, tools and multi-device continuity.

See [HITOS.md](HITOS.md) for detailed exit criteria.

## Documentation

- [Project context](docs/PROJECT_CONTEXT.md)
- [Research scope](docs/RESEARCH_SCOPE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Bibliography](docs/BIBLIOGRAPHY.md)
- [Evaluation](docs/EVALUATION.md)
- [Security](docs/SECURITY.md)
- [Decisions](docs/DECISIONS.md)
- [Progress log](docs/progress.md)

## Status

**H0 — research and architecture baseline.**

No claim in the roadmap should be interpreted as an implemented feature until it is marked as completed and backed by code/tests.
