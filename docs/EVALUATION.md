# Evaluation

AION should be evaluated as a system, not by subjective impressions alone.

## Memory

Candidate metrics:
- factual recall accuracy;
- temporal reasoning accuracy;
- contradiction/update handling;
- abstention accuracy;
- provenance coverage;
- retrieval precision;
- relevant-context tokens per answer.

Test families:
- facts stated once long ago;
- repeated facts with changed values;
- temporal questions;
- causal chains;
- preference evolution;
- unsupported-memory traps.

## Identity

Metrics:
- behaviour consistency across restarts;
- consistency across model providers;
- personality-state change magnitude;
- correction frequency;
- successful rollback reproducibility.

## Proactivity

Define a proactive turn as **accepted** when the user meaningfully engages with it rather than immediately dismissing/ignoring it.

Candidate metrics:
- Proactive Precision Rate = accepted proactive turns / emitted proactive turns;
- dismissal rate;
- focus-state interruption rate;
- average cooldown after rejection;
- cost per accepted proactive interaction.

## Tools

Metrics:
- task success rate;
- invalid tool-call rate;
- user-aborted tool-call rate;
- permission violations;
- destructive-action confirmations;
- latency.

## Security

Metrics:
- indirect prompt-injection attack success;
- data-exfiltration success;
- malicious tool-output success;
- false-positive block rate;
- utility under defense.

## Voice

Metrics:
- end-of-speech to first-audio latency;
- interruption recovery;
- false wake rate;
- missed wake rate;
- transcription error on representative conditions.

## Long-horizon testing

Before claiming robust persistence, create synthetic timelines spanning months/years with:
- preference changes;
- contradictory statements;
- forgotten/irrelevant chatter;
- important autobiographical events;
- model-provider migrations;
- re-embedding migrations.

Derived indexes should be destructible and rebuildable while preserving expected answers from canonical events.
