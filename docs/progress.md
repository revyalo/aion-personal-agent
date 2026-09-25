# Progress Log

## 2026-09-26 — H0: project initialized

### Vision

Created **A.I.O.N. — Adaptive Intelligence Orchestration Nexus** as a long-term personal AI-agent project.

Initial target:
- persistent identity;
- evidence-backed long-term memory;
- proactive conversation;
- adaptive but auditable personality;
- model-independent reasoning;
- secure tool use;
- continuity across Windows, macOS and Android.

### Key decisions

- AION is not identified with one LLM.
- Raw events are the source of truth.
- Embeddings and summaries are rebuildable derived state.
- Identity kernel and adaptive personality are separated.
- Proactivity will be event-driven rather than continuous LLM polling.
- The first implementation will be intentionally small: text + SQLite + one provider adapter.
- Multi-device offline conflict resolution is deferred.
- Security and permission boundaries are first-class design concerns.

### Research baseline

Initial literature focuses on:
- Generative Agents;
- MemGPT;
- LoCoMo and LongMemEval;
- Reflective Memory Management;
- TiMem;
- PersonaAgent;
- Inside Out;
- ProactiveEval;
- AgentDojo / InjecAgent / Agent Security Bench.

### Next step

Start **H1 — Birth**:
1. define the initial SQLite schema;
2. implement the provider abstraction;
3. implement persistent identity;
4. append conversation events;
5. create the first terminal client.
