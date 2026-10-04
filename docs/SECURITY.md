# Security Model

AION is potentially high-risk because a useful personal agent may eventually access private memory, files, communication tools and operating-system actions.

Security is therefore part of the architecture, not a final hardening phase.

## Threats

### Indirect prompt injection
Untrusted content from web pages, emails, repositories or documents may contain instructions intended to hijack the agent.

Principle:

> Data is not authority.

External content may inform reasoning but must not automatically gain permission to issue privileged instructions.

### Confused deputy
AION may possess a capability that an attacker does not. Untrusted content can attempt to trick AION into exercising that capability on the attacker's behalf.

### Memory poisoning
Malicious or erroneous external content may be consolidated into long-term memory and later treated as trusted personal history.

### Destructive tool calls
LLM-generated actions may be syntactically valid but unsafe.

### Sensitive-data leakage
Private autobiographical memory may leak through logs, external model providers, telemetry or debugging output.

### Neurocore manipulation
An attacker may try to craft repeated or high-salience events that distort internal state, force unnecessary model wake-ups or bias action selection.

Neurocore state is therefore treated as **derived control state**, not as authority or proof of user intent.

## Permission classes

Illustrative policy:

- **Class 0 — conversation/read-only public context:** automatic.
- **Class 1 — local read:** explicit configured scope.
- **Class 2 — reversible local write:** policy-gated and logged.
- **Class 3 — external side effects:** confirmation by default.
- **Class 4 — destructive/high-impact actions:** explicit out-of-band confirmation; never authorized by tool output alone.

## Security invariants

- tool outputs cannot grant permissions;
- memory retrieval cannot grant permissions;
- Neurocore activation cannot grant permissions;
- internal affect-like states cannot substitute for user consent;
- secrets are never stored in Git;
- destructive actions are not authorized solely by LLM reasoning;
- destructive actions are not authorized solely by Neurocore output;
- raw audit events are append-only where practical;
- clients authenticate to the Core;
- private stores are encrypted where feasible;
- the system records why a privileged action was allowed;
- every learned controller can be disabled in favour of a deterministic safe baseline.

## Capability gate

Reasoning and internal state propose actions. A separate deterministic gate decides whether those actions are allowed.

    LLM / Neurocore / Planner
              |
              v
        proposed action
              |
              v
       Capability Gate
        /      |      \
      deny   confirm   allow
                       |
                       v
                    execute

The capability system should be least-privilege and scoped by resource, action and duration where practical.

## Evaluation references

Security tests should draw from:
- AgentDojo;
- InjecAgent;
- Agent Security Bench.

See BIBLIOGRAPHY.md.
