# AION Milestones

The roadmap is capability-driven. A milestone is complete only when its exit criteria are satisfied.

## H0 — Foundations

Goal: freeze the first engineering/research baseline before implementation expands.

Deliverables:
- project vision and boundaries;
- literature baseline;
- initial threat model;
- architecture principles;
- measurable research questions;
- initial data/privacy policy.

Exit criteria:
- README and core design documents exist;
- first implementation scope is intentionally small;
- raw events are defined as the canonical historical source.

## H1 — Birth

Goal: create the smallest persistent AION that can survive process restarts.

Scope:
- Python Core;
- model-provider interface;
- terminal/text client;
- persistent identity;
- append-only conversation/event log;
- SQLite storage;
- configuration and secrets outside Git.

Exit test:
1. converse with AION;
2. terminate the process;
3. restart it;
4. AION retains the same identity and canonical conversation history.

## H2 — Remember

Goal: retrieve useful memories instead of replaying the entire history.

Scope:
- episodic memories;
- semantic facts;
- provenance from every derived memory to raw event IDs;
- retrieval by semantic, lexical and temporal signals;
- confidence metadata.

Evaluation:
- targeted memory QA;
- temporal questions;
- changed-preference questions;
- abstention when evidence is missing.

## H3 — Consolidate

Goal: prevent memory pollution and historical distortion.

Scope:
- memory consolidation pipeline;
- temporal validity: valid_from / valid_until;
- contradiction handling;
- superseded facts without deleting history;
- importance/relevance scoring;
- rebuildable derived indexes.

Key invariant:

> Embeddings, summaries and knowledge structures are disposable indexes. Raw events are not.

## H4 — Voice

Goal: natural low-latency conversation.

Scope:
- local wake word or explicit activation;
- local VAD;
- streaming speech input/output;
- interruption handling;
- latency instrumentation;
- privacy controls for microphone use.

## H5 — Initiative

Goal: allow AION to start a conversation without behaving like spam.

Architecture:
- event-driven triggers;
- deterministic fast filters;
- interruption-cost model;
- optional small-model arbiter;
- frontier-model generation only after acceptance;
- cooldown/backoff after ignored proactive turns.

Evaluation:
- proactive precision;
- dismissal/ignore rate;
- useful follow-up rate;
- interruptions during focus states.

## H6 — Hands

Goal: safely use external tools.

Scope:
- standard tool protocol where practical (e.g. MCP-compatible adapters);
- capability-based permissions;
- read/write/destructive action classes;
- sandboxed execution;
- explicit confirmation for sensitive actions;
- audit trail.

Security evaluation:
- indirect prompt injection;
- malicious tool output;
- data exfiltration attempts;
- confused-deputy scenarios.

## H7 — Presence

Goal: one AION identity across multiple devices.

Scope:
- Core/client protocol;
- authenticated device registration;
- Windows/macOS client prototype;
- Android client prototype;
- handoff of active conversation;
- canonical server-side state;
- encrypted client cache.

Offline conflict resolution is explicitly postponed until online handoff is reliable.

## H8 — Evolve

Goal: adapt behaviour without losing identity.

Scope:
- immutable identity kernel;
- bounded adaptive personality state;
- evidence-backed personality updates;
- versioned diffs;
- snapshots and rollback;
- correction-driven preference learning.

Evaluation:
- correction frequency;
- preference consistency;
- identity-drift tests;
- rollback reproducibility.

## H9 — Intelligence

Goal: make reasoning engines replaceable and selectable.

Scope:
- model router;
- task-specific provider selection;
- optional local/private model;
- benchmark history by task;
- fallback strategy;
- migration tests across providers and embedding models.

## H10 — Harden

Goal: test long-horizon reliability rather than demo quality.

Scope:
- LoCoMo/LongMemEval-inspired evaluation;
- synthetic multi-year timelines;
- storage migrations;
- re-embedding and index rebuilds;
- recovery from corrupted derived state;
- performance and cost profiling;
- security regression suite.

## H11 — AION 1.0

Target capabilities:
- persistent identity;
- evidence-backed long-term memory;
- text and voice interaction;
- controlled proactive dialogue;
- secure tool use;
- multi-device continuity;
- auditable personality adaptation;
- model-agnostic reasoning.

AION 1.0 is not defined by consciousness claims. It is defined by observable engineering properties: continuity, memory, adaptivity, safe agency and portability.

The experimental Neurocore track is **not required** to call H11 complete.

# Experimental N-track — Neurocore

This track begins only when simple baselines exist. It may run in parallel after H5/H6 or after H11 without blocking the main roadmap.

## N0 — Baseline internal state

Goal: make the control problem measurable before adding neural complexity.

Scope:
- explicit scalar state for urgency, novelty, relevance, interruption cost and cooldown;
- deterministic update rules;
- full logging;
- tests for model wake/sleep decisions.

Exit criterion:
- reproducible baseline dataset and metrics for accepted/rejected proactive events.

## N1 — Stateful controller

Goal: replace selected hand-written transitions with a cheap persistent controller.

Scope:
- recurrent/state-machine or small learned controller;
- bounded state;
- deterministic capability gate remains external;
- ability to fall back to N0.

Evaluation:
- proactive precision;
- unnecessary wake-ups;
- latency;
- compute cost;
- stability under repetitive/adversarial stimuli.

## N2 — Bio-inspired controller

Goal: test whether spiking or other biologically inspired dynamics provide useful behaviour beyond simpler controllers.

Scope:
- small SNN or equivalent temporal neural model;
- salience/action-selection experiments;
- habituation and competing-goal dynamics;
- interpretable input/output bridge.

Explicit non-goal:
- reproducing the full Drosophila brain.

## N3 — Comparative evaluation

Goal: decide whether the Neurocore deserves a permanent place in AION.

Compare:
1. deterministic rules;
2. explicit state machine;
3. small conventional learned controller;
4. bio-inspired/spiking controller.

Keep the simplest design that wins on useful behaviour, cost, reliability and auditability. A biologically inspired design is not preferred merely because it is biologically inspired.
