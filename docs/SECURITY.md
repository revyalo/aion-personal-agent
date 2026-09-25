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
- secrets are never stored in Git;
- destructive actions are not authorized solely by LLM reasoning;
- raw audit events are append-only where practical;
- clients authenticate to the Core;
- private stores are encrypted where feasible;
- the system records why a privileged action was allowed.

## Evaluation references

Security tests should draw from:
- AgentDojo;
- InjecAgent;
- Agent Security Bench.

See BIBLIOGRAPHY.md.
