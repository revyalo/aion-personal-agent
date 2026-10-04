# Architecture

## 1. Core principle

AION is not the LLM. The Core owns persistent identity and state; reasoning models are replaceable services.

## 2. Canonical vs derived state

### Canonical
- raw user/assistant messages;
- tool-call events;
- explicit user corrections;
- identity-kernel version;
- permission decisions;
- timestamps and device origin.

### Derived
- summaries;
- semantic facts;
- embeddings;
- memory links;
- personality updates;
- relevance scores;
- knowledge-graph structures;
- Neurocore activations and interpreted internal-state labels.

Derived state must be rebuildable from canonical evidence whenever practical.

## 3. Initial architecture

    Text Client
        |
        v
    AION Core
        |
        +-- Identity Manager
        +-- Conversation Service
        +-- Event Store
        +-- Memory Service
        +-- Model Provider
        +-- Permission Layer
        |
        v
    SQLite

This is intentionally boring. H1 should prove persistence before adding distributed systems.

## 4. Target architecture

                                  +------------------+
                                  |  Model Providers |
                                  +---------+--------+
                                            |
                                            v
    +-----------+       secure       +------+----------------------+
    |  Clients  | <----------------> |          AION Core          |
    |-----------|                     |-----------------------------|
    | Windows   |                     | Identity / Personality      |
    | macOS     |                     | Canonical Event Store       |
    | Android   |                     | Memory Router               |
    +-----+-----+                     | Reasoning / Model Router    |
          |                           | Proactivity / Neurocore     |
          | local                     | Permission / Tool Gateway   |
          | sensors/tools             +---+-----------+-------------+
          |                               |           |
          +-------------------------------+           |
                                                      v
                                          +----------------------+
                                          | Derived Memory Index |
                                          | vectors / lexical /  |
                                          | temporal / graph     |
                                          +----------------------+

The Neurocore is an optional controller inside the Core. It is not a source of permissions and does not replace the reasoning layer.

## 5. Memory model

AION should eventually distinguish:

- **working memory** — current interaction state;
- **episodic memory** — events and experiences;
- **semantic memory** — structured facts and preferences;
- **autobiographical memory** — important long-term narrative events;
- **reflections** — derived interpretations that remain linked to evidence.

A memory record should be able to carry:
- source event IDs;
- created_at;
- valid_from;
- valid_until;
- confidence;
- importance;
- retrieval metadata.

## 6. Identity model

### Identity kernel
Stable, human-controlled configuration:
- name;
- core role;
- non-negotiable behavioural constraints;
- security boundaries.

### Adaptive personality state
Bounded and versioned:
- humour;
- formality;
- initiative;
- verbosity;
- interaction preferences.

Every automatic update requires:
- reason;
- evidence IDs;
- previous value;
- new value;
- timestamp.

## 7. Proactivity

Do not poll a frontier model continuously.

    OS / calendar / conversation event
                |
                v
    deterministic fast filter
                |
           candidate?
                |
                v
    optional cheap arbiter / Neurocore
                |
           useful enough?
                |
                v
    main reasoning model
                |
                v
    voice / notification / queue

## 8. Experimental Neurocore

The long-term idea is to explore a small, cheap, continuously stateful controller inspired by biological action-selection and salience systems.

It may integrate signals such as:
- urgency;
- novelty;
- relevance to current goals;
- confidence/uncertainty;
- interruption cost;
- recent user engagement;
- computational budget;
- unresolved task pressure;
- habituation and cooldown.

Possible outputs:
- ignore an event;
- increase/decrease salience;
- retrieve specific memories;
- queue an event;
- wake a reasoning model;
- choose among safe high-level behaviours.

It must **not**:
- grant itself capabilities;
- authorize destructive actions;
- infer user consent from its own internal state;
- modify the identity kernel without the normal audited update path.

Implementation should progress from the simplest baseline:

    deterministic rules
          |
          v
    explicit state machine
          |
          v
    learned/stateful controller
          |
          v
    optional spiking / biologically inspired model

A literal simulation of the complete Drosophila brain is not a project requirement. Biological connectomes are research inspiration, not a ready-made cognitive architecture for AION.

See [NEUROCORE.md](NEUROCORE.md).

## 9. Wake/sleep model

The project should avoid keeping an expensive LLM active when no deep reasoning is required.

    external/local events
            |
            v
      cheap persistent layer
            |
       salient enough?
         /       \
       no         yes
       |           |
    record      retrieve context
                   |
                   v
              wake model
                   |
                   v
             reason / act
                   |
                   v
              return idle

"Sleep" is an engineering power/cost state, not a claim of biological sleep or consciousness.

## 10. Model migration

Model and embedding drift are expected.

Therefore:
- provider-specific prompts stay behind adapters;
- embeddings never become canonical facts;
- embedding-model metadata is stored with indexes;
- re-embedding must be supported;
- identity/personality tests are run when changing reasoning providers.

## 11. Offline strategy

Early versions use the Core as the canonical writer.

Offline clients may cache recent state and queue raw events, but should not independently rewrite long-term semantic memory until conflict handling is explicitly designed and tested.
