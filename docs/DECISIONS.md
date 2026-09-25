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
