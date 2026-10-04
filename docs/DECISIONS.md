# Architecture Decisions

This document records decisions that should remain stable unless evidence justifies changing them.

## ADR-001 — AION is model-agnostic

**Decision:** identity and memory must not belong to one LLM provider.

**Reason:** model providers, APIs and quality change faster than the intended lifetime of AION.

## ADR-002 — Raw events are canonical

**Decision:** raw interaction/action events are the historical source of truth. Summaries, embeddings, facts and graphs are derived.

**Reason:** derived representations drift and may need to be rebuilt after model or embedding migrations.

## ADR-003 — Identity kernel is separated from adaptive personality

**Decision:** core identity is human-controlled and stable. Adaptation occurs through bounded, versioned state.

**Reason:** recursive free-text persona rewriting risks uncontrolled identity drift.

## ADR-004 — Proactivity is event-driven

**Decision:** AION will not continuously call an expensive LLM to ask whether it should speak.

**Reason:** cost, latency and noise. Deterministic filters should reject most events before model reasoning.

## ADR-005 — Core owns canonical state

**Decision:** early multi-device clients are peripherals; the Core is the canonical writer for identity and long-term memory.

**Reason:** prevents premature distributed-state conflicts.

## ADR-006 — Offline semantic merging is deferred

**Decision:** offline clients may queue raw events, but autonomous long-term semantic consolidation is not an early requirement.

**Reason:** semantic conflict reconciliation is substantially harder than chronological event synchronization.

## ADR-007 — Security policy is deterministic where possible

**Decision:** permission checks, destructive-action gates and sandbox boundaries are enforced outside the LLM.

**Reason:** a probabilistic model must not be the final authority over its own permissions.

## ADR-008 — Build differentiating layers, reuse infrastructure

**Decision:** reuse mature storage, speech and tool-protocol components where they fit. Custom engineering effort should focus on continuity, evidence-backed memory, identity evolution, proactivity and cross-device presence.

**Reason:** rebuilding databases, VAD or generic tool runtimes provides little project differentiation.

## ADR-009 — Neurocore is optional and incremental

**Decision:** a persistent bio-inspired controller may be researched after deterministic proactivity baselines exist. A full Drosophila-brain simulation is not required.

**Reason:** the useful hypothesis is whether cheap internal dynamics improve salience and action selection, not whether copying a biological connectome makes AION intelligent.

## ADR-010 — Neurocore cannot grant authority

**Decision:** Neurocore state may rank or propose actions, but it cannot grant permissions, bypass confirmations or authorize destructive/external side effects.

**Reason:** internal activation is not equivalent to user intent or authorization.

## ADR-011 — No sentience/consciousness claim from behaviour alone

**Decision:** AION documentation and evaluation distinguish observable functions from claims about subjective experience.

**Reason:** memory, self-reference, persistent state, affect-like variables and fluent self-report do not establish sentience. The project should make claims that can be operationalized and tested.

## ADR-012 — Human-like internal labels remain inspectable engineering state

**Decision:** labels such as curiosity, urgency, concern, confidence or fatigue refer to explicit computational variables unless evidence supports a stronger interpretation.

**Reason:** this keeps the system auditable and avoids confusing anthropomorphic interfaces with scientific evidence.

## ADR-013 — Release/commercialization triggers a fresh compliance review

**Decision:** legal/privacy assumptions for a personal research prototype are not carried forward automatically to public distribution, third-party users or commercial deployment.

**Reason:** obligations can change materially with purpose, users, data processed, capabilities and jurisdiction.
