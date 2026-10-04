# Legal and Ethical Boundaries

> Engineering note, not legal advice. Last reviewed: 2026-10-04.

## 1. Current project posture

AION is currently a personal research/engineering project.

Building a persistent personal agent, experimenting with long-term memory, self-models, spiking neural networks or biologically inspired controllers is not in itself prohibited in Spain or the European Union.

The relevant legal risk comes primarily from **what the system does, what data it processes, whose systems it accesses, and whether it is offered to other people**, not from calling a component a Neurocore or investigating machine cognition.

## 2. EU AI Act

Regulation (EU) 2024/1689 uses a risk-based framework.

Important scope points for the project:
- certain research, testing and development activities before a system is placed on the market or put into service are outside parts of the Regulation's scope, subject to the Regulation's exact conditions;
- use by a natural person in a purely personal, non-professional activity receives different treatment from professional deployment;
- these assumptions must be re-checked if AION is distributed, commercialized, used professionally or provided to third parties.

For interactive AI, Article 50 contains transparency obligations. From **2 August 2026**, providers of covered systems intended to interact directly with natural persons must ensure people are informed that they are interacting with AI unless that is obvious in context.

Design consequence:
- any future third-party-facing AION interface should clearly identify itself as an AI system where required.

Official references:
- EU AI Act consolidated text: https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng
- European Commission Article 50 guidance: https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems

## 3. Personal data and privacy

A personal prototype mainly processing the owner's own data is materially different from a service that processes data for many users.

The project should nevertheless apply privacy-by-design from the start:
- collect only what is needed;
- separate secrets from source code;
- encrypt private stores where feasible;
- make retention/deletion policies explicit;
- keep provenance for derived memories;
- avoid sending sensitive data to external model providers unless necessary and authorized;
- treat third-party personal data as higher-risk than the owner's own data.

Before public or professional deployment, re-assess GDPR/LOPDGDD obligations, lawful bases, notices, data-subject rights, processors/subprocessors, international transfers and retention.

## 4. Authorized system access

AION may be given tools that read files, operate applications, call APIs or control devices.

Core rule:

> Possessing a technical ability is not the same as having authorization to use it.

The capability gate should ensure that AION acts only on systems/resources the user is authorized to access and only within granted scopes.

The project must not normalize:
- unauthorized access to third-party systems;
- credential theft;
- interception of communications without authorization;
- bypassing access controls;
- destructive actions outside an authorized environment.

## 5. Third-party services, models and datasets

Every integrated provider has its own terms, licenses and data-handling rules.

Track:
- model/API terms;
- open-source licenses;
- dataset licenses;
- attribution requirements;
- redistribution restrictions;
- commercial-use restrictions;
- privacy/data-processing conditions.

Do not assume that publicly accessible data is automatically free to train on, redistribute or store indefinitely.

## 6. Sentience does not currently create a special legal shortcut

A future AION might have richer memory, self-models, internal dynamics or highly convincing self-reports.

Those properties do not automatically:
- prove sentience;
- grant the software legal personhood;
- remove existing safety/privacy obligations;
- authorize the system to ignore its operator's permission model.

If the scientific or legal landscape changes, this document must be reviewed.

See [COGNITION_AND_SENTIENCE.md](COGNITION_AND_SENTIENCE.md).

## 7. Release gate

Before AION moves from personal research to a public release, hosted service or commercial product, perform a dedicated review covering at least:

- intended users and jurisdictions;
- AI Act role: provider/deployer and applicable risk/transparency duties;
- GDPR/LOPDGDD;
- security/threat model;
- logging and auditability;
- user consent and permission UX;
- model and dataset licensing;
- third-party API terms;
- incident response;
- high-impact capabilities.

ADR-013 makes this review a design requirement rather than an afterthought.
