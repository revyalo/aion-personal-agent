# Bibliography

This file tracks papers that directly influence AION's design. Priority indicates how early they should be read for the project.

## Priority A — Core reading

### Generative Agents: Interactive Simulacra of Human Behavior
Park et al., 2023.  
https://arxiv.org/abs/2304.03442

**Why it matters:** foundational architecture combining a record of experiences, dynamic retrieval, reflection and planning. Particularly relevant to AION's episodic memory, reflection and spontaneous interaction.

### MemGPT: Towards LLMs as Operating Systems
Packer et al., 2023.  
https://arxiv.org/abs/2310.08560

**Why it matters:** treats context as a hierarchy of memory tiers and demonstrates multi-session conversational agents that remember and evolve. Strong conceptual reference for separating active context from persistent memory.

### Evaluating Very Long-Term Conversational Memory of LLM Agents (LoCoMo)
Maharana et al., ACL 2024.  
https://aclanthology.org/2024.acl-long.747/

**Why it matters:** shows that long-context and ordinary RAG remain weak on long-range temporal/causal conversational memory. Useful benchmark and warning against assuming that "more context" solves memory.

### LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory
Wu et al., 2024.  
https://arxiv.org/abs/2410.10813

**Why it matters:** evaluates extraction, multi-session reasoning, temporal reasoning, knowledge updates and abstention. These map almost directly to AION memory tests.

### In Prospect and Retrospect: Reflective Memory Management for Long-term Personalized Dialogue Agents
Tan et al., ACL 2025.  
https://aclanthology.org/2025.acl-long.413/

**Why it matters:** proposes multi-granularity prospective reflection and retrospective retrieval refinement. Relevant to consolidation without flattening all conversations into one summary.

### TiMem: Temporal-Hierarchical Memory Consolidation for Long-Horizon Conversational Agents
Li et al., Findings ACL 2026.  
https://aclanthology.org/2026.findings-acl.1091/

**Why it matters:** makes temporal continuity a first-class structure and reports strong long-horizon results with reduced recalled context. Highly relevant to AION's timeline and consolidation design.

### PersonaAgent: Bridging Memory and Action for Personalized LLM Agents
Zhang et al., Findings ACL 2026.  
https://aclanthology.org/2026.findings-acl.1315/

**Why it matters:** combines episodic/semantic personalized memory with action selection and test-time persona adaptation. Directly relevant to AION's memory-personality-action loop.

### ProactiveEval: A Unified Evaluation Framework for Proactive Dialogue Agents
Liu et al., ACL 2026.  
https://aclanthology.org/2026.acl-long.1906/

**Why it matters:** provides a framework for evaluating proactive dialogue rather than judging it only by feel. Useful when implementing H5.

## Priority B — Memory evolution and identity

### Inside Out: Evolving User-Centric Core Memory Trees for Long-Term Personalized Dialogue Systems
Zhao et al., ACL 2026.  
https://aclanthology.org/2026.acl-long.614/

**Why it matters:** structured PersonaTree with interpretable ADD/UPDATE/DELETE/NO_OP operations. Relevant to bounded, auditable user/persona evolution.

### Towards Lifelong Dialogue Agents via Timeline-based Memory Management
Ong et al., NAACL 2025.  
https://aclanthology.org/2025.naacl-long.435/

**Why it matters:** preserves outdated memories as historical context and links events temporally and causally instead of deleting the past. Strong match for AION's valid_from / valid_until model.

### A-MEM: Agentic Memory for LLM Agents
Xu et al., 2025.  
https://arxiv.org/abs/2502.12110

**Why it matters:** dynamically links and evolves memories using a Zettelkasten-inspired structure. Useful comparison for AION's derived memory graph.

### Locomo-Plus: Beyond-Factual Cognitive Memory Evaluation Framework for LLM Agents
Li et al., ACL 2026.  
https://aclanthology.org/2026.acl-long.1150/

**Why it matters:** tests whether agents can retain and later apply implicit constraints, not merely recall explicit facts. Useful for evaluating whether AION actually uses stored personal context appropriately.

## Priority B — Learning without weight updates

### Reflexion: Language Agents with Verbal Reinforcement Learning
Shinn et al., 2023.  
https://arxiv.org/abs/2303.11366

**Why it matters:** demonstrates improvement through stored linguistic feedback rather than weight updates. Relevant to AION's auditable behavioural learning.

### Self-Refine: Iterative Refinement with Self-Feedback
Madaan et al., 2023.  
https://arxiv.org/abs/2303.17651

**Why it matters:** useful reference for test-time self-critique/refinement, although AION should avoid uncontrolled recursive self-rewriting.

## Priority A — Agent security

### AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents
Debenedetti et al., 2024.  
https://arxiv.org/abs/2406.13352

**Why it matters:** realistic benchmark for agents acting over untrusted tool data. Directly useful for H6 security regression testing.

### InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents
Zhan et al., 2024.  
https://arxiv.org/abs/2403.02691

**Why it matters:** demonstrates that malicious instructions embedded in external content can hijack tool-using agents. Motivates strict separation between authority and data.

### Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents
Zhang et al., 2024.  
https://arxiv.org/abs/2410.02644

**Why it matters:** broad attack/defense benchmark covering prompt handling, tools and memory. Relevant to threat-model completeness.

## Reading order

1. Generative Agents
2. MemGPT
3. LoCoMo
4. LongMemEval
5. Reflective Memory Management
6. TiMem
7. PersonaAgent
8. Inside Out
9. ProactiveEval
10. AgentDojo + InjecAgent
11. Timeline-based Memory Management
12. A-MEM / LoCoMo-Plus / Reflexion

## Rule for adding papers

A paper should be added only if it can change:
- an architecture decision;
- a measurable hypothesis;
- an evaluation method;
- a security assumption; or
- an implementation milestone.

The bibliography is not intended to become a generic list of agent papers.
