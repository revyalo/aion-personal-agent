# Research Scope

AION is an engineering project with research-oriented evaluation.

## Research questions

### RQ1 — Long-term memory
How can a conversational agent preserve relevant memory over long horizons while minimizing noise, contradiction, stale facts and unsupported recollection?

Variables of interest:
- retrieval accuracy;
- temporal reasoning;
- knowledge update handling;
- abstention;
- provenance coverage;
- memory size and retrieval cost.

### RQ2 — Identity continuity
How can an adaptive agent evolve its conversational behaviour without uncontrolled identity drift?

Variables:
- stability of kernel traits;
- frequency and magnitude of personality updates;
- correction rate;
- reproducibility after rollback;
- consistency across model providers.

### RQ3 — Proactive dialogue
How can AION initiate interactions that are useful or welcome while minimizing interruption cost?

Variables:
- proactive precision;
- ignore/dismissal rate;
- follow-up engagement;
- interruptions during detected focus;
- inference cost per accepted proactive turn.

### RQ4 — Cross-device continuity
How can one canonical state be maintained while clients appear, disappear and hand off active interaction?

Initial scope:
- online handoff;
- authenticated clients;
- canonical Core state;
- ephemeral encrypted client cache.

Deferred:
- fully autonomous offline long-term-memory consolidation;
- complex semantic merge of divergent offline histories.

### RQ5 — Secure agency
How can AION act through tools without treating untrusted content as authority?

Variables:
- task success;
- unsafe action rate;
- prompt-injection attack success;
- human-confirmation rate;
- false blocks;
- permission violations.

## Research principles

- Compare against simple baselines.
- Preserve negative results.
- Prefer reproducible tests to anecdotal demos.
- Separate claims about engineering behaviour from claims about cognition.
- Do not equate fluent persona simulation with consciousness.
