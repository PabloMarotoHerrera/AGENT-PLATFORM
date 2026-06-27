# Agent Platform Workspace Charter

Status: canonical workspace charter  
Ticket: W-01 - Agent Platform Workspace Charter & Vocabulary Normalization  
Scope: AGENT PLATFORM root purpose, workspace vocabulary, authority boundaries, identity, and current canonical surfaces  
Date: 2026-06-27

## 1. Purpose

This document is the first canonical workspace-level architecture document for AGENT PLATFORM.

It defines the root purpose, vocabulary, authority boundaries, and workspace identity that future W-series architecture work must use unless this document is explicitly superseded by a later canonical workspace document or by promoted Cognitive Semantic System authority.

This document is based on:

| Input | Current use |
| --- | --- |
| `0_architecture/workspace/agent_platform_knowledge_assembly.md` | W-00 assembly output and source-audit recommendation. |
| `previusknowledge/docs/architecture/repository_vision.md` | Prior AgentLab repository vision, used as migration evidence. |
| `previusknowledge/docs/architecture/repository_principles.md` | Durable principles to carry forward after workspace normalization. |
| `previusknowledge/docs/architecture/source_of_truth_strategy.md` | Authority, evidence, promotion, demotion, generated artifact, and conflict model. |
| `previusknowledge/docs/architecture/graphify_canonical_semantic_model.md` | Prior Graphify-labeled semantic boundary and truth/evidence/projection distinctions. |
| `previusknowledge/docs/architecture/graphify_semantic_authority_architecture.md` | Semantic authority, boundaries, lifecycle, promotion, demotion, and federation model. |
| `previusknowledge/docs/architecture/agent_architecture_final_synthesis.md` | Agent role, organism, authority, runtime mediation, traceability, and security constraints. |
| `previusknowledge/docs/architecture/context_architecture_final_synthesis.md` | Context as bounded, selected, traceable, governed, security-constrained exposure. |
| `previusknowledge/docs/architecture/adapter_final_synthesis.md` | Adapters as provider-facing mediation posture, not authority or implementation. |
| `previusknowledge/docs/architecture/provider_final_synthesis.md` | Providers as external capability owners with non-authoritative output by default. |
| `previusknowledge/docs/architecture/runtime_final_synthesis.md` | Runtime as participation, execution, and exposure posture, not engines or authority. |

This document does not move files, delete files, edit previous documents, create W0, implement code, stage changes, commit, or push.

Charter rule:

```text
AGENT PLATFORM is a workspace-level architecture and governance context first.
Implementation, restructuring, product workspaces, and runtime systems must follow
the vocabulary and authority boundaries established here.
```

## 2. AGENT PLATFORM Definition

AGENT PLATFORM is the root workspace for designing, governing, and operating an agent-native platform.

It exists to coordinate:

| Area | Meaning inside AGENT PLATFORM |
| --- | --- |
| Architecture | Canonical workspace principles, boundaries, decisions, and vocabulary. |
| Agents | Roles that consume context, reason, plan, execute permitted work, and produce evidence. |
| Context | Bounded, selected, traceable, governed information surfaces for tasks and consumers. |
| Adapters | Platform-owned mediation posture for provider-facing capability translation, projection, preparation, exposure, compatibility, and coordination. |
| Providers | External capability owners such as coding agents, model providers, tools, workflow systems, or execution environments. |
| Runtime posture | Conceptual participation, execution, and exposure posture for future runtime systems without defining engines, queues, services, or code. |
| Governance | Approval, policy, lifecycle, ownership, promotion, exception, and authority-sensitive decisions. |
| Validation | Evidence sufficiency, validity posture, checks, verdicts, and proof boundaries. |
| Security/Access | Permissions, exposure, sensitivity, private data, secrets, trust, and risk constraints. |
| Knowledge | Reviewed durable material, decisions, context packages, references, and explanations. |
| External sources | Reference repositories, tools, engines, docs, examples, and vendor materials with provenance. |
| Product workspaces | Bounded product or domain areas that consume platform capabilities without defining root platform authority. |

AGENT PLATFORM is not the old AgentLab Digital Twin product repository. The old AgentLab and Digital Twin architecture remains valuable migration evidence, but the current root is broader than any one product.

## 3. Workspace vs Repository

The word `workspace` means the operating environment where AGENT PLATFORM architecture, knowledge, external references, product workspaces, agent work, validation evidence, and future implementation artifacts are coordinated.

The word `repository` means a version-controlled source unit or a concrete Git repository. The current AGENT PLATFORM root may also be a Git repository, but the workspace concept is broader than repository mechanics.

Vocabulary rules:

| Term | Use | Do not use it for |
| --- | --- | --- |
| Workspace | The AGENT PLATFORM root context and its governed operating environment. | A single product, package, service, or Git history mechanism. |
| Repository | A concrete version-controlled artifact store. | The full AGENT PLATFORM identity when workspace-level meaning is intended. |
| Workspace root | The current root where architecture, external references, previous knowledge, and future work are coordinated. | Proof of truth, ownership, or authority by path alone. |
| Repository artifact | A file, folder, commit, generated output, config, doc, or source artifact in a repository. | Cross-artifact truth by itself. |

Current rule:

```text
Use workspace when discussing AGENT PLATFORM root authority.
Use repository only for concrete Git/source-storage boundaries.
```

## 4. Platform vs Product

The platform is the agent-native enablement, governance, context, adapter, provider, runtime-posture, validation, security, and semantic-authority environment.

A product is a bounded user-facing or domain-facing outcome built within or alongside the platform.

| Concept | Owns | Does not own |
| --- | --- | --- |
| Platform | Agent-native operating model, architecture, authority boundaries, workspace governance, context posture, adapter posture, provider posture, runtime posture, validation/security constraints, and cross-product semantic continuity. | Product-specific user value, domain-specific behavior, or external provider behavior. |
| Product | User-facing outcomes, domain value, product-specific behavior, product-specific source, product-specific validation, and product-specific knowledge. | Root workspace authority, future Cognitive Semantic System truth, generic adapter/provider/runtime architecture, or global governance. |

Platform and product may interact, but their authority must not collapse.

Platform-to-product rule:

```text
The platform enables product workspaces.
Product workspaces consume platform capabilities.
No product workspace defines AGENT PLATFORM root authority by default.
```

## 5. Product Workspace Definition

A product workspace is a bounded workspace area for a product, domain, or solution that consumes AGENT PLATFORM capabilities while preserving its own product-specific scope.

A product workspace may contain:

| Surface | Product workspace meaning |
| --- | --- |
| Product source | Authoritative for implemented product behavior within product scope. |
| Product architecture | Canonical only for that product scope after explicit promotion. |
| Domain knowledge | Product/domain evidence or knowledge, not root authority by default. |
| Product validation | Evidence for product behavior, not global truth by default. |
| Product external references | Domain-specific external evidence with provenance. |
| Product generated outputs | Generated/evidence artifacts unless explicitly promoted. |

The Digital Twin, Omniverse, EnergyPlus, OpenStudio, simulation, visualization, and related materials from previous AgentLab work are candidates for future product workspaces. They do not define AGENT PLATFORM root identity.

Product workspace rule:

```text
A product workspace can own product meaning and product behavior.
It cannot own AGENT PLATFORM root truth, workspace vocabulary, Cognitive Semantic
System authority, generic agent/context/adapter/provider/runtime boundaries, or global
governance unless explicitly delegated by a future authority decision.
```

## 6. Architecture vs Research vs Docs

Architecture, research, and docs are different authority classes.

| Surface | Definition | Default authority |
| --- | --- | --- |
| Architecture | Accepted boundaries, principles, vocabulary, responsibility models, and decisions that constrain future work. | Authoritative only when marked canonical and scoped. |
| Research | Investigation, evidence, comparison, analysis, source review, or recommendation. | Evidence only until promoted. |
| Docs | Human-readable artifacts, guides, explanations, notes, decisions, research, runbooks, or generated summaries. | Varies by status and scope. |
| Previous knowledge | Historical and migration corpus from earlier AgentLab architecture work. | Migration evidence unless explicitly carried forward. |
| External references | Third-party source material, cloned repositories, docs, examples, tools, engines, or packages. | External evidence only. |

Documentation status terms:

| Status | Meaning |
| --- | --- |
| `canonical` | Accepted authority within declared scope. |
| `draft` | Proposed material, not authoritative. |
| `research` | Evidence or analysis, not a decision. |
| `generated` | Produced from another source, not source by default. |
| `projection` | Derived view for a consumer or provider, not truth by default. |
| `migration_evidence` | Historical input preserved for analysis and carry-forward decisions. |
| `external_reference` | Outside source retained for evidence, provenance, and comparison. |
| `historical` | Preserved past state, not current authority. |
| `superseded` | Replaced by newer authority. |
| `deprecated` | Known but discouraged for new work. |
| `archived` | Retired and retained for audit or reference. |

Documentation rule:

```text
Docs are artifacts.
Research is evidence.
Architecture is authority only when explicitly canonical, scoped, and current.
```

## 7. Previous Knowledge Status

`previusknowledge/` is the migrated previous-knowledge corpus.

Its current status is:

```text
Historical and migration evidence with many prior canonical-in-old-scope documents.
```

The original `Status: canonical` labels in previous documents remain evidence of prior intent. They do not automatically make those documents canonical for AGENT PLATFORM root.

Carry-forward classifications:

| Classification | Meaning |
| --- | --- |
| `carry_forward` | Principle or conceptual architecture remains valid and should be restated in current workspace docs. |
| `scope_limit` | Valid only inside a product workspace or bounded domain, not root authority. |
| `migration_evidence` | Useful for history, rationale, and migration analysis. |
| `conflicted` | Contains naming, scope, authority, or roadmap conflict requiring normalization. |
| `superseded` | Replaced by newer current workspace authority after explicit decision. |

Current carry-forward principles include:

| Principle | Workspace interpretation |
| --- | --- |
| Governed semantic authority owns truth. | The future Cognitive Semantic System owns accepted semantic truth when implemented and promoted, independent of its internal representation. |
| Files are artifacts. | Files carry content and evidence; they do not own cross-artifact truth by path. |
| Agents are roles. | Agents consume truth and produce bounded support material. |
| Context is bounded exposure. | Context packages are selected, governed, traceable, and non-authoritative by default. |
| Adapters are projections/mediation. | Adapter surfaces expose posture without authority transfer. |
| Providers are external. | Provider output and behavior remain external evidence unless accepted. |
| Runtime hosts and mediates. | Runtime posture does not own truth, governance, validation, security, or product acceptance. |
| Evidence is not truth. | Promotion requires authority path, provenance, validation, and governance posture. |
| Generated is not source. | Generated outputs and projections require explicit promotion to become source. |
| Human approval is required before commits and pushes. | Repository history and publication remain human-governed unless a future policy changes this. |

Previous-knowledge rule:

```text
Previous documents may be cited as evidence.
Only current workspace documents under `0_architecture/workspace/` define current
AGENT PLATFORM root vocabulary until Cognitive Semantic System authority is
implemented and promoted.
```

## 8. External Sources Status

`4_external/sources/` contains external repositories, tools, engines, harnesses, examples, and reference material.

Its current status is:

```text
External reference evidence only.
```

External source rules:

| Rule | Meaning |
| --- | --- |
| External authority stays external. | A third-party repository owns its own local meaning, not AGENT PLATFORM truth. |
| Proximity is not promotion. | Being cloned under `4_external/sources/` does not make a source internal or canonical. |
| Output is evidence. | Reports, generated graphs, README claims, examples, and code are evidence until accepted. |
| Integration requires review. | License, provenance, version, trust, risk, security, and validation must be checked before promotion or dependency adoption. |
| Harnesses are providers or adapter targets. | OpenCode, Codex-like systems, Pi, Tau, Hermes, OpenClaw, ACP, and ECC-style systems do not define the platform. |
| Domain engines are product references. | EnergyPlus and OpenStudio inform product/domain workspaces, not the root agent platform by default. |

Required external-source metadata for future registry work:

| Field | Purpose |
| --- | --- |
| Source name | Stable local identifier. |
| Origin URL | Provenance and upstream authority. |
| Version or commit | Freshness and reproducibility. |
| License | Legal use boundary. |
| Role | Harness, provider, domain engine, registry, tool, example corpus, or product reference. |
| Relevance | Why it exists in the workspace. |
| Risk | Executable, network, credential, security, data, privacy, or licensing risk. |
| Promotion status | External reference, candidate, reviewed, approved, restricted, deprecated, or archived. |

External-source rule:

```text
External sources may inform architecture.
They do not become AGENT PLATFORM architecture without explicit promotion.
```

## 9. Cognitive Semantic System Naming Rule

This workspace has two related naming and substrate risks: prior architecture uses Graphify as the semantic-authority name, while `4_external/sources/graphify` is an external graph-generation skill/library; and the future cognitive substrate has not been decided.

Until an explicit naming ADR exists, the neutral working name is `Cognitive Semantic System`.

This name does not imply that the future system is graph-based, database-backed, file-backed, vector-only, ontology-only, or any other implementation design. Graph structures remain the strongest current candidate hypothesis, not an accepted implementation decision.

The normalized names are:

| Name | Meaning | Authority status |
| --- | --- | --- |
| `Cognitive Semantic System` | The future AGENT PLATFORM system for canonical semantic authority in the agent-native cognitive workspace. | Neutral provisional name; conceptual authority, not implemented here yet. |
| `cognitive semantic authority` | The authority function for accepting, rejecting, promoting, demoting, superseding, and preserving accepted semantic truth. | Canonical vocabulary for authority discussions until a naming ADR supersedes it. |
| `prior Graphify-labeled architecture` | Previous documents that used Graphify as the semantic-authority name and often assumed graph-oriented representation. | Migration evidence and candidate-substrate input, not current naming authority. |
| `external graphify tool` | The repository under `4_external/sources/graphify`, including its skill/library and generated outputs. | External reference and projection generator only. |
| `external graphify output` | Generated outputs such as graph reports, graph JSON, HTML views, or extraction results. | Evidence or projection until promoted. |

Naming rules:

| Rule | Required use |
| --- | --- |
| Prefer `Cognitive Semantic System` in workspace architecture. | Use this when discussing the future AGENT PLATFORM semantic authority system. |
| Prefer `cognitive semantic authority` for authority mechanics. | Use this when discussing acceptance, promotion, demotion, conflict, lifecycle, or truth. |
| Do not call external tool output truth. | Call it `external graphify projection`, `external graphify output`, or `generated graph evidence`. |
| Do not use `Graphify` as the current or future system name. | Use it only when citing old document names, prior terminology, or the external source. |
| Do not treat graph as an implementation decision. | Graph, another complex-system organization, or a hybrid model remains subject to later architecture and validation. |

Canonical naming statement:

```text
In AGENT PLATFORM architecture, Cognitive Semantic System is the neutral working
name for the future semantic authority in the agent-native cognitive workspace.
Its internal representation remains undecided. The external graphify tool is a
reference and projection generator only.
```

## 10. Agent-Native Workspace Principles

AGENT PLATFORM is agent-native because humans and agents are expected to collaborate through explicit context, authority, validation, and governance boundaries.

Canonical principles:

| Principle | Rule |
| --- | --- |
| Agents are roles. | Agents may reason, plan, inspect, edit when allowed, validate, and report; they do not own truth. |
| Context is selected. | Agents should receive bounded context selected by task, authority, freshness, sensitivity, lineage, and budget. |
| Evidence is promoted, not assumed. | Agent outputs, tool outputs, validation results, logs, and research are evidence until accepted. |
| Runtime mediates. | Future runtime systems host and mediate participation but do not own authority. |
| Adapters mediate providers. | Adapters translate, project, prepare, expose, classify, and coordinate posture without authority transfer. |
| Providers stay external. | Provider capability, behavior, output, interface, and availability remain provider-owned. |
| Governance decides. | Approval, promotion, policy, exceptions, lifecycle, and ownership decisions require governance authority. |
| Validation evaluates. | Validation provides evidence and validity posture; it does not approve or promote. |
| Security constrains. | Security/Access may restrict visibility, tools, providers, data, context, memory, shell, network, MCP, and publication. |
| Files are artifacts. | Files are readable, executable, generated, evidentiary, or source artifacts with declared authority status. |
| Agent cognition drives organization. | Architecture should optimize how agents reason, retrieve, relate, validate, evolve, and coordinate knowledge, not traditional repository organization. |
| External material stays external. | Cloned repos and source snapshots require provenance and promotion before internal authority. |
| Generated output is not source. | Generated files, graph outputs, reports, logs, and context packs are not source unless promoted. |
| Plan before build. | Architecture, migration, risky work, and cross-boundary changes require planning before implementation. |
| Human approval gates history. | Staging, commits, pushes, and publication require explicit human approval unless future governance changes this. |

Agent-native invariant:

```text
The workspace may be optimized for agent work, but agent convenience must not
override authority boundaries, context limits, validation needs, governance, or
security constraints.
```

## 11. Authority Model

AGENT PLATFORM authority is explicit, scoped, and boundary-preserving.

Authority owners:

| Domain | Owns | Does not own |
| --- | --- | --- |
| Future Cognitive Semantic System | Accepted semantic truth, stable identity, relationships, lifecycle, provenance, ownership posture, validation posture references, governance posture references, context eligibility, drift, continuity, and semantic history where represented. | Governance decisions, validation execution, security enforcement, runtime execution, provider behavior, agent cognition, or repository mechanics. |
| Governance | Policy, approval, promotion authorization, exceptions, lifecycle authorization, ownership authorization, and authority-sensitive decisions. | Validation correctness, security enforcement, runtime execution, provider behavior, or cognitive-system storage. |
| Validation | Checks, methods, verdicts, evidence sufficiency, freshness assessment, and validity posture. | Governance approval, truth acceptance, security permission, or product acceptance. |
| Security/Access | Permission, exposure, sensitivity, trust, credential protection, minimization, redaction, and access restrictions. | Truth, validation verdicts, governance decisions, provider behavior, or product meaning. |
| Runtime | Conceptual hosting, mediation, participation posture, execution posture, exposure posture, trace, blockers, and readiness. | Truth, governance, validation, security authority, engines, queues, services, deployment, or source code. |
| Agents | Bounded cognition, planning, recommendations, execution within scope, produced evidence, handoff material, and traceable reports. | Truth, approval, promotion, governance, validation authority, security authority, context authority, or commit/push authority. |
| Context | Bounded information exposure, lineage, freshness, eligibility, constraints, and task-specific packaging. | Truth, permission, governance, validation, runtime execution, or provider behavior. |
| Adapters | Provider-facing mediation posture: translation, projection, exposure, execution preparation, compatibility, and coordination. | Providers, truth, governance, validation, security, runtime authority, product meaning, or execution authority. |
| Providers | External capability, behavior, output, interfaces, availability, limits, environment posture, and constraints. | Local truth, product meaning, agent cognition, validation proof, governance approval, security permission, or local authority. |
| Repositories and files | Artifact content and versioned source behavior within narrow scope. | Cross-artifact truth, lifecycle, ownership, context eligibility, or governance by path alone. |
| Product workspaces | Product behavior, product meaning, product-specific source, product-specific knowledge, and product validation within scope. | Root workspace authority or generic platform architecture by default. |
| External sources | Their own external records and source material. | AGENT PLATFORM truth unless accepted through explicit promotion. |

Current precedence within AGENT PLATFORM root:

| Precedence | Surface | Applies to |
| ---: | --- | --- |
| 1 | Human-approved governance and accepted decisions | Policy, approval, exceptions, lifecycle, and authority-sensitive outcomes. |
| 2 | Cognitive Semantic System when implemented and promoted | Accepted semantic truth, identity, relationships, lifecycle, provenance, ownership posture, context eligibility, drift, and continuity. |
| 3 | Canonical workspace docs in `0_architecture/workspace/` | Current human-readable workspace purpose, vocabulary, architecture, and authority boundaries. |
| 4 | Current ticket instructions | Allowed scope, forbidden scope, deliverables, validation, and expected response for the active task. |
| 5 | Product source in a product workspace | Implemented product behavior within product scope. |
| 6 | Previous knowledge and research | Migration evidence unless explicitly promoted. |
| 7 | External sources and generated outputs | Evidence or projection unless explicitly promoted. |
| 8 | Agent outputs, logs, memory, runtime state | Working evidence unless promoted through authority path. |

Authority transition rule:

```text
Evidence -> candidate -> validation posture -> governance posture -> accepted
truth only through explicit authority transition.
Existence, recency, location, generation, provider confidence, or agent confidence
does not create authority.
```

## 12. What AGENT PLATFORM Is Not

AGENT PLATFORM is not:

| Not | Reason |
| --- | --- |
| The old AgentLab Digital Twin repository | Digital Twin material is product/workspace evidence, not root identity. |
| A product repository only | The root platform is broader than any product. |
| A vendor archive | External sources require provenance, status, license, relevance, and promotion. |
| A graphify-output folder | Generated graph reports are evidence/projections, not Cognitive Semantic System authority. |
| A pure AI coding-agent config repo | Harness configs are projections and provider/adapters, not root truth. |
| A folder-first truth system | Folder placement helps navigation but does not define authority. |
| A generated-output dump | Generated, runtime, cache, log, simulation, graph, or context output is not source by default. |
| A secrets or private-data store | Credentials and sensitive data must not be committed or exposed by default. |
| A place where every agent edits everything | Agents need scoped roles, permissions, context, validation, and reporting. |
| A runtime implementation plan | Runtime architecture here is conceptual posture, not engines, queues, services, or code. |
| A provider implementation | Providers remain external capability owners unless separately implemented and governed. |
| A replacement for governance | Governance decisions remain explicit and authority-bound. |
| A replacement for validation | Validation evidence and verdicts remain distinct from approval and truth. |
| A replacement for security | Security/Access constrains exposure and action independently. |

Non-goal rule:

```text
This charter defines identity and vocabulary.
It does not authorize implementation, restructuring, W0 creation, product buildout,
provider integration, cognitive-system implementation, or broad agent permissions.
```

## 13. Current Canonical Surfaces

Current AGENT PLATFORM canonical and evidence surfaces are:

| Surface | Status | Authority role |
| --- | --- | --- |
| `0_architecture/workspace/agent_platform_workspace_charter.md` | Canonical workspace charter. | Current authority for AGENT PLATFORM root identity, vocabulary, and high-level authority boundaries. |
| `0_architecture/workspace/agent_platform_knowledge_assembly.md` | W-00 assembly output. | Source audit, migration recommendation, and evidence base for W-01. |
| Current W-series ticket instructions | Active task authority. | Defines current allowed scope, forbidden scope, deliverables, and validation for the active task only. |
| `previusknowledge/` | Migration evidence. | Historical prior architecture and research corpus. Not root authority by default. |
| `4_external/sources/` | External references. | Evidence and pattern sources. Not internal authority by default. |
| Future Cognitive Semantic System | Conceptual/future semantic authority. | Will own accepted semantic truth when implemented, governed, and promoted. |

Current workspace-authority rule:

```text
Until the Cognitive Semantic System is implemented and promoted, current
canonical workspace documents under `0_architecture/workspace/` are the
human-readable authority for AGENT PLATFORM root vocabulary and architecture
boundaries.
```

## 14. Open Conflicts

The following conflicts remain open after W-01 and should not be guessed away.

| Conflict | Current status | Required future work |
| --- | --- | --- |
| Cognitive Semantic System implementation | Conceptual authority exists; implementation and substrate do not. | Create naming ADR; define semantic authority boundary, substrate evaluation, storage/projection/sync model, and promotion workflow in later tickets. |
| External graphify naming | Normalized by this charter, but old docs and external source names remain. | Enforce neutral future-system naming in future docs and registries. |
| Cognitive substrate | Graph structures are the strongest current candidate hypothesis, but not an implementation decision. | Evaluate graph, other complex-system organization, and hybrid models before implementation. |
| Previous document classification | W-00 grouped documents, but all 237 markdown files are not individually classified. | Create W-02 classification index. |
| External source registry | W-00 reviewed sources, but no governed registry exists. | Create W-03 external source registry. |
| Current workspace folder map | `0_architecture/` and `4_external/` exist, but full workspace responsibility map is undefined. | Create W-04 workspace responsibility map. |
| Product workspace boundary | Product workspace concept is defined; concrete product areas are not. | Define product workspace policy before moving or creating product structures. |
| Digital Twin migration | Prior Digital Twin scope remains product evidence. | Decide whether and where Digital Twin becomes a product workspace. |
| Context pack strategy | Context principles are carried forward; no concrete format exists. | Create W-05 context pack strategy. |
| Agent permission model | Principles exist; concrete permission profiles do not. | Define agent roles, permissions, allowed surfaces, tools, and validation gates. |
| Governance process | Authority owner concepts exist; concrete governance workflow does not. | Define decision, approval, promotion, exception, and lifecycle procedures. |
| Validation model | Validation is distinguished from governance; concrete validation registry does not exist. | Define validation surfaces, evidence retention, and task proof levels. |
| Security/Access model | Security constraints exist; concrete access policy does not. | Define sensitivity, secrets, private data, shell, network, MCP, provider, and publication rules. |
| W0 | Explicitly not created. | Create only after charter, classification, source registry, and workspace map are ready enough. |

Open-conflict rule:

```text
An open conflict is a blocker for authority transfer, not permission to improvise.
Future work must preserve the conflict until a ticket resolves it explicitly.
```

## 15. Final Charter Statement

AGENT PLATFORM is the agent-native workspace root for governing, coordinating, and evolving platform capabilities, product workspaces, previous knowledge, external references, agents, context, adapters, providers, runtime posture, validation, governance, security, and future semantic authority.

The workspace is broader than any one repository and broader than any one product. The old AgentLab Digital Twin repository architecture is migration evidence. Product and domain materials may become product workspaces only through explicit scope and authority decisions.

`Cognitive Semantic System` is the neutral working name for the future semantic authority concept and system that owns accepted semantic truth. External graphify tooling and generated graph outputs are evidence/projections only until promoted.

Agents, context, adapters, providers, runtime, files, external sources, generated outputs, memory, and research are not truth by default. They produce or carry evidence, posture, content, or bounded exposure. Authority-sensitive outcomes require explicit boundaries, provenance, validation posture, governance posture, security constraints, and promotion.

Final charter:

```text
AGENT PLATFORM is a governed, agent-native workspace.

Its root authority begins with canonical workspace architecture in
`0_architecture/workspace/` and must evolve toward Cognitive Semantic System
authority without letting files, products, external sources, generated outputs,
providers, harnesses, agents, runtime state, memory, or context become competing
truth by default.
```
