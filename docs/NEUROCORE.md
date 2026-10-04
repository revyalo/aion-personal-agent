# AION Neurocore — Experimental Research Track

## 1. Motivation

AION should not need to run a large reasoning model continuously just to decide whether something deserves attention.

The Neurocore hypothesis is:

> A small, cheap and continuously stateful controller may be able to maintain salience, habituation, internal priorities and wake/sleep decisions while expensive language/reasoning models remain inactive most of the time.

This would make AION feel more persistent at the systems level without pretending that an LLM is continuously "thinking".

## 2. What the Neurocore is

The Neurocore is an **optional control layer** between events and expensive reasoning.

    messages ---------+
    calendar ---------+
    device events ----+----> Neurocore ----> ignore / queue / retrieve / wake
    memory signals ---+
    task state -------+

Candidate inputs:
- urgency;
- novelty;
- goal relevance;
- unresolved-task pressure;
- recent interaction history;
- confidence/uncertainty;
- interruption cost;
- time since last interaction;
- user engagement/dismissal history;
- computational/energy budget.

Candidate internal dynamics:
- activation and decay;
- habituation;
- competing priorities;
- refractory/cooldown periods;
- short-lived working state;
- slowly changing baselines.

Candidate outputs:
- discard/ignore;
- record only;
- increase/decrease salience;
- retrieve relevant memory;
- queue for later;
- wake a reasoning model;
- propose a safe high-level action.

## 3. What it is not

The Neurocore is not:
- the identity of AION;
- the long-term memory store;
- the permission system;
- a replacement for the LLM;
- evidence of consciousness;
- a requirement to simulate an entire biological brain.

A full adult Drosophila connectome contains roughly 139,255 neurons and 54.5 million synapses. That is scientifically fascinating, but copying the wiring diagram is not equivalent to importing a fly's cognition into software.

A connectome alone also does not give AION the biological body's sensors, neural dynamics, neuromodulation, developmental history, learning history or semantics needed to interpret its activity.

Therefore the project uses Drosophila and other compact nervous systems as **architectural inspiration**, not as a drop-in brain.

## 4. Why Drosophila is still interesting

Compact nervous systems demonstrate that relatively small neural systems can support:
- sensory integration;
- action selection;
- navigation;
- associative learning;
- state-dependent behaviour;
- competition between behavioural drives.

Those are closer to the Neurocore's intended role than language generation is.

Useful inspirations include:
- recurrent circuits;
- sparse specialized pathways;
- competing action channels;
- salience-like routing;
- persistent internal dynamics;
- temporal integration;
- neuromodulatory/state-dependent switching.

The engineering question is not "can we make AION a fly?" but:

> Which compact biological control principles remain useful after translating them into an auditable software agent?

## 5. Progressive implementation

### Stage A — deterministic baseline

Start with explicit equations/rules.

Example conceptual update:

    urgency(t+1) =
        decay * urgency(t)
        + event_urgency
        - cooldown

This is intentionally simple and interpretable.

### Stage B — explicit recurrent state

Introduce interactions between variables:

    novelty ----+
                +--> salience --> wake_score
    urgency ----+
    focus_cost -+
    habituation -+

### Stage C — learned low-cost controller

Train a small recurrent model from logged decisions/corrections.

The model may recommend a wake/action class, but capability authorization remains outside it.

### Stage D — spiking/bio-inspired experiment

Only after baselines exist, compare a small SNN or related temporal model against conventional alternatives.

Do not add neural complexity without an evaluation target.

## 6. Evaluation

Possible metrics:
- accepted proactive turns / total proactive turns;
- dismissal or ignore rate;
- missed important events;
- unnecessary LLM wake-ups;
- model tokens/cost per useful proactive action;
- response latency;
- state stability;
- recovery after repetitive inputs;
- susceptibility to adversarial salience manipulation;
- reproducibility;
- interpretability of wake/action decisions.

A Neurocore experiment succeeds only if it beats a simpler baseline on meaningful metrics.

## 7. Safety invariants

The Neurocore can propose; it cannot authorize.

It must never:
- grant a capability;
- bypass confirmation;
- infer consent from its activation state;
- directly execute high-impact actions;
- modify the identity kernel;
- permanently write semantic memory without the normal evidence path.

Every version must support:
- state inspection;
- event logging;
- reset;
- deterministic safe fallback;
- bounded output space.

## 8. Relationship to "sentience"

Persistent internal state may make AION behave more organism-like. That is not, by itself, evidence of subjective experience.

If a variable called "concern" increases and changes behaviour, the computational state is real. The project should still describe it operationally: a control variable affected by particular inputs and producing measurable outputs.

See [COGNITION_AND_SENTIENCE.md](COGNITION_AND_SENTIENCE.md).

## 9. References

- Dorkenwald, S. et al. (2024), **Neuronal wiring diagram of an adult brain**, Nature 634, 124–138. https://doi.org/10.1038/s41586-024-07558-y
- Lin, A. et al. (2024), **Network statistics of the whole-brain connectome of Drosophila**, Nature 634, 153–165. https://doi.org/10.1038/s41586-024-07968-y
- Schlegel, P. et al. (2024), **Whole-brain annotation and multi-connectome cell typing of Drosophila**, Nature 634, 139–152. https://doi.org/10.1038/s41586-024-07686-5
