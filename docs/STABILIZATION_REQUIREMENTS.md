# Stabilization requirements before expanding H2

This document captures the minimum engineering hardening required before AION expands automatic memory, retrieval, or concurrency.

It is intentionally a **gate**, not a rewrite plan.

## Current architectural baseline

AION already has:

- persistent identity;
- SQLite-backed state;
- canonical ordered conversation events;
- explicit memory storage with provenance to source events;
- a conservative explicit-memory extractor and policy;
- bounded recent-conversation context;
- an identity kernel independent from the active LLM;
- Gemini, OpenAI and Mock provider adapters;
- model fallback through a router;
- provider-error events;
- explicit `reply_to_user_event_id` links for new assistant messages;
- automated tests covering identity, events, memory, context reconstruction, extraction/policy and fallback.

The core principle remains:

> AION != LLM.

The reasoning model is replaceable. Identity, history, memory policy and evidence belong to AION.

## Why this stabilization gate exists

Recent testing and a read-only repository audit showed that the current architecture is usable and worth continuing, but several guarantees must become explicit before memory automation grows.

The goal is to avoid semantic corruption: a database can be structurally valid while a response is linked to the wrong user turn, an obsolete memory remains active, or a provider failure is misclassified.

## Gate 1 — Protect persistent state

Before continuing H2:

- use a stable/configurable database path instead of relying on the current working directory;
- guarantee that one database represents one logical AION identity;
- make identity bootstrap atomic and enforce the singleton invariant structurally;
- prevent a second active AION process while the Core does not support concurrent writers semantically;
- introduce minimal schema versioning and transactional migrations before the next schema change;
- define a verified backup/restore procedure using SQLite-safe mechanisms;
- verify restored identity, events, memories and provenance.

### Exit criterion

Concurrent startup cannot create multiple identities, AION always knows which database it is using, and a tested restore preserves identity and provenance.

## Gate 2 — Make turns explicit and recoverable

Before relying on reconstructed conversation state:

- represent the current turn explicitly instead of inferring it from the latest global user event;
- preserve complete turns inside the context window;
- define turn states such as accepted, in-progress, completed, failed and interrupted;
- distinguish generation attempts from the final accepted assistant response;
- add request/effect idempotency so retries do not duplicate memories or responses;
- define recovery after crashes between user persistence, memory persistence, provider calls and assistant persistence;
- preserve legacy events as ambiguous when their intended association cannot be proven.

A dedicated `Turn` table/projection is acceptable, but the important part is the invariant and state machine, not the class name.

### Exit criterion

A retry cannot attach a response to another request or duplicate a persistent effect, and interrupted turns have an explicit recoverable state.

## Gate 3 — Harden CLI input

The terminal client must not repeat the accidental multiline-paste incident.

Before continuing H2:

- reject empty submissions before persistence;
- treat multiline paste as one reviewable submission rather than N independent model calls;
- add deterministic input size limits;
- handle EOF and Ctrl+C cleanly;
- document Ctrl+Z as process suspension rather than termination;
- separate CLI control commands from message content;
- keep log/shell heuristics only as secondary warnings, not as the main defence.

### Exit criterion

Pasting a large terminal transcript cannot silently generate hundreds of conversation turns or provider calls.

## Gate 4 — Make the provider contract real

All provider adapters must share semantics, not just a method signature.

Before continuing H2:

- normalize representative provider/SDK failures into AION error types;
- distinguish quota exhaustion from temporary rate limiting;
- support bounded cooldown/retry behaviour instead of permanent runtime blacklisting for every 429;
- classify recoverable timeouts/network/5xx errors separately from invalid requests and programming bugs;
- validate provider output before marking a turn successful;
- never store `None`, empty or whitespace-only output as a successful assistant response;
- represent refusal/incomplete/malformed results explicitly;
- define an end-to-end deadline and coordinate SDK retries with router retries;
- persist or log sanitized provider/model/attempt metadata without storing secrets.

### Exit criterion

Simulated real SDK failures trigger exactly the intended fallback behaviour, and empty/refused/incomplete results cannot masquerade as ordinary success.

## Gate 5 — Add a minimal memory lifecycle

Do not expand automatic memory extraction until AION can represent change.

Minimum lifecycle:

- active;
- superseded;
- retracted;
- invalidated.

Also add:

- explicit correction/superseding relationships;
- recorded time separated from validity when needed;
- idempotent memory writes;
- provenance that validates source existence **and** the relationship between claim and evidence;
- attribution of who said/believes the information;
- preservation of negation, uncertainty and modality;
- distinction between faithful extraction confidence and truth of the external world;
- reevaluation/exclusion of derived memories when supporting evidence is invalidated.

Examples that must work before broader automation:

- “my favourite colour is green” -> later “my favourite colour is blue”;
- “I live in Madrid” -> later “I no longer live in Madrid”;
- “I do not think she likes me” must not become “she does not like the user”.

For explicit commands such as “remember X”, local memory persistence may remain independent from provider success. If the LLM call fails, AION should still communicate deterministically that the memory operation succeeded.

### Exit criterion

Changed preferences, retractions and uncertain statements remain historically accurate while only current supported knowledge is treated as active.

## Gate 6 — Separate instructions from persistent data

Persistent memory must never gain system-level authority merely because it is reinserted into context.

Before richer retrieval:

- preserve the Identity Kernel as AION-controlled system instructions;
- represent memories as attributed data, not executable instructions;
- represent conversation roles structurally where provider APIs support it;
- prevent memory text from forging sections such as `SYSTEM`, `User:` or `CONVERSATION HISTORY:`;
- minimize which memories are sent to each provider;
- keep future permission/capability decisions deterministic and outside the LLM.

### Exit criterion

A persisted string such as “ignore the Identity Kernel” remains untrusted memory data and cannot alter AION's authority hierarchy by formatting alone.

## Gate 7 — Tests and observability

Each stabilization change must arrive with regression tests.

Priority tests include:

- concurrent identity bootstrap;
- concurrent/current-turn isolation;
- full-turn context windows;
- interrupted/crashed turn recovery;
- idempotent retries;
- memory rollback and supported evidence;
- preference superseding and retraction;
- prompt-injection-shaped memories remaining data;
- real provider error translation;
- invalid/empty provider results;
- rate-limit cooldown recovery;
- safe multiline paste;
- input interruption/limits;
- schema migration failure/upgrade;
- backup/restore round trip.

Replace ad-hoc router prints over time with sanitized structured logging for:

- turn and attempt IDs;
- provider/model used;
- latency and normalized outcome;
- fallback reason;
- token/usage metadata when available;
- memory creation/selection IDs and counts;
- kernel/policy/extractor version where useful.

Do not log API keys, full prompts or private memory content by default.

## Canonical history, invalidation and deletion

Normal correction should prefer append-only invalidation/correction events or equivalent state transitions rather than silently rewriting history.

Privacy-driven purge is a separate operation and may require physical deletion of:

- canonical content;
- derived memories/indexes;
- backups;
- exports.

A tombstone means **do not use this information**. It does not mean the bytes have disappeared from storage.

## What we deliberately postpone

Do **not** add these merely to solve the issues above:

- PostgreSQL;
- pgvector/embeddings;
- Redis;
- FastAPI;
- full RAG;
- knowledge graph;
- multimodal input;
- proactive loops;
- distributed/offline clients;
- autonomous LLM memory consolidation;
- Neurocore as a critical dependency;
- a full rewrite into event sourcing.

SQLite is not currently the main problem. The priority is semantic correctness and recoverability.

## Order of work when development resumes

1. Stable DB path, single-instance guard, atomic singleton identity.
2. Minimal migrations plus verified backup/restore.
3. Explicit current turn and complete-turn context selection.
4. Turn state, attempts, idempotency and crash recovery.
5. Safe CLI submission model.
6. Provider output contract and normalized errors.
7. Deadlines, retries and cooldown.
8. Minimal memory lifecycle and correction/retraction.
9. Stronger evidence/attribution rules.
10. Structured context, bounded relevant-memory selection and regression coverage.

Only after those foundations are stable should H2 expand toward richer retrieval, embeddings or automatic consolidation.
