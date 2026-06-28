# AGENT PLATFORM Workspace Final Synthesis

Status: Canonical W-14 workspace output  
Date: 2026-06-28  
Scope: Final architecture/documentation synthesis for Proyecto W - Agent Workspace Architecture  
Authority: Workspace baseline synthesis only. This document closes Proyecto W at the architecture/documentation level. It does not migrate files, implement code, automate governance, decide the Cognitive Semantic System substrate, activate products, adopt external dependencies, modify `.gitignore`, stage, commit, push, or create any post-W ticket.

## 1. Purpose

W-14 closes Proyecto W at the architecture and documentation level by synthesizing W-00 through W-13 into one current AGENT PLATFORM workspace baseline.

This synthesis answers:

| Question | W-14 answer type |
| --- | --- |
| What is AGENT PLATFORM now? | Current governed workspace definition. |
| What has Proyecto W decided? | Closure summary of W-00 through W-13 decisions. |
| What is canonical? | Current human-readable authority baseline. |
| What remains evidence? | Previous knowledge, research, external sources, products, generated outputs, validation outputs, and agent outputs unless promoted. |
| What remains local-only? | Ignored, product, external source, data, model, artifact, previous knowledge, generated, dependency, and sensitive material. |
| What remains explicitly undecided? | Naming, substrate, product activation, archive, validation, security, implementation, governance automation, context-pack format, and first migration batch decisions. |
| What blocks implementation? | Missing security/access, validation, product, external dependency, substrate, harness, and readiness decisions. |
| What is the next macroproject or operational phase? | Recommended next phase after Proyecto W. |

Clarifications:

| W-14 is not | Meaning |
| --- | --- |
| Migration | It does not move, copy, rename, delete, archive, or restate previous documents into new target areas. |
| Implementation | It does not create platform code, scripts, tools, tests, packages, SDKs, products, adapters, providers, runtimes, or semantic-system implementation. |
| Governance automation | It does not implement approval workflows, enforcement, roles, permissions, hooks, policies, or tools. |
| Substrate decision | It does not decide whether graph, relational, document, vector, event-sourced, hybrid, or another substrate becomes final. |
| Product activation | It does not activate any product workspace or change product Git posture. |
| External dependency adoption | It does not run, install, copy, authenticate, integrate, or approve any external source. |

W-14 closure rule:

```text
Proyecto W is complete when the workspace architecture baseline is explicit enough
to audit before migration, implementation, product activation, dependency adoption,
or substrate selection. Closure is not execution.
```

## 2. W-Series Closure Summary

| Ticket | Core decision | Authority contribution | Unresolved items |
| --- | --- | --- | --- |
| W-00 Knowledge Assembly | The previous knowledge base is valuable migration evidence, and the current root is AGENT PLATFORM, not the old product repository. External sources are references only. | Created the initial source audit, carry-forward principle list, external-source review, and recommendation to proceed with agent-native workspace architecture. | Needed W-01 vocabulary normalization, W-02 file-level classification, W-03 external registry, and later workspace policy. |
| W-01 Workspace Charter | AGENT PLATFORM is a governed, agent-native workspace broader than any product or repository. `Cognitive Semantic System` is the neutral working name for future semantic authority. | Established current root vocabulary, workspace/product boundary, authority precedence, previous knowledge status, external source status, and canonical workspace surface. | Cognitive Semantic System implementation, final name, final substrate, product boundaries, validation, governance, security/access, and W0 remained unresolved. |
| W-02 Previous Knowledge Classification | `previusknowledge/` was classified semantically and by file as migration evidence, not current authority. | Classified 237 markdown files and separated `carry_forward`, `scope_limit`, `migration_evidence`, `conflicted`, and `external_reference` material. | Carry-forward concepts still require restatement; conflicted semantic material requires normalization; product material remains scope-limited; no migration executed. |
| W-03 External Source Registry | All 12 external sources under `4_external/sources/` are external references, not promoted. | Classified source types, relevance, license posture, runtime/security risk, recommended handling, promotion rules, and risk register. | No external metadata migration, source reuse, execution, dependency approval, product integration, or substrate decision. |
| W-04 Workspace Responsibility Map | Top-level folders are responsibility projections, not truth. Current W-series architecture lives under `0_architecture/workspace/`. | Mapped each root area by purpose, authority posture, Git posture, access posture, and migration posture. | Folder permanence, archive path, product activation, external tracking posture, security/access enforcement, script/tool trust, and implementation policy remained unresolved. |
| W-05 Agent Context Pack Strategy | Context packs are selected, bounded, traceable exposure for a task; context is not truth or permission. | Defined source classes, context pack types, selection rules, exclusions, citations, edit rules, lifecycle, and agent behavior expectations. | No physical context-pack format or folder created; no automation; security/access and validation registry remained absent. |
| W-06 Cognitive Workspace Model | AGENT PLATFORM is a cognitive operating environment before it is a folder topology, harness, implementation, or substrate. | Defined cognitive primitives and the flow from goal to task, context, evidence, claim, output, validation, governance, promotion/rejection, and learning. | No implementation, harness decision, governance automation, validation registry, security/access policy, or final cognitive substrate decision. |
| W-07 Workspace Topology | Keep the current numbered topology short-term as a provisional projection; numeric prefixes are navigation aids only. | Established folder topology baseline, local-only topology, product/external/platform boundaries, and `_archive/` as a future-only concept. | No renames or moves; numbered folder permanence, archive policy, product policy, and implementation readiness remained unresolved. |
| W-08 Migration Plan | Migration means classified, cited, incremental, validation-backed, governance-bound restatement or transition, not file movement. | Defined migration principles, source classes, target areas, previous knowledge migration flow, external metadata posture, archive strategy, commit strategy, validation rules, and migration sequence. | No migration batch executed; no archive created; product migration, external metadata migration, implementation, and commits remained blocked. |
| W-09 Canonical Documentation Structure | Documentation requires status, scope, citations, lifecycle, validation posture, governance posture, and source class. | Defined documentation status model, scope model, target doc areas, ADR structure, research/external/product/human-doc projection rules, metadata header, citations, lifecycle, and migration targets. | No folders created or docs migrated; product docs, archive movement, implementation docs, and broad agent permissions remained unresolved. |
| W-10 Agent Operating Rules | Agents are bounded operators. Capability, context, or tool availability does not equal permission. | Defined agent roles, read/write/execution/Git/citation/context/previous/external/product/subagent/validation/governance/output/stop rules. | Enforcement not implemented; agents still require explicit task scope; commits, migration, execution, dependency adoption, product activation, and substrate decisions remain approval-gated. |
| W-11 Governance & Promotion Model | Governance is the explicit decision layer; evidence, validation, context, Git, generated output, and agent output do not approve themselves. | Defined governance objects, roles, evidence-to-decision flow, decision types, promotion preconditions, rejection/deferral/demotion, documentation/migration/external/product/validation/security/Git/agent governance, lifecycle, artifacts, invariants, and anti-patterns. | No governance automation; no archive policy; product activation, implementation, security/access decisions, validation registry, external execution, dependency adoption, and final substrate remained blocked. |
| W-12 Product Workspace Policy | Product folders are local-only candidates; no product is active. Product authority is scoped and cannot define root authority. | Inventoried six product candidates and defined product states, ownership, authority boundary, Git posture, documentation, validation, external dependency, agent access, migration, activation, risk, invariants, and recommendations. | No product charter, owner, activation, Git posture change, code inspection, validation, security posture, external dependency adoption, or product implementation. |
| W-13 External Source Handling Policy | External sources are controlled evidence. Metadata, pattern, dependency, execution, product, Git, and substrate decisions stay separate. | Defined external source definition, classes, status model, review dimensions, license/reuse, execution, dependency, pattern, instruction, metadata, review format, source-specific rules, product dependency handling, substrate handling, risks, promotion/rejection, Git, and agent rules. | No external metadata migration, execution, dependency approval, product integration, source reuse, or substrate decision. |

W-series closure verdict:

```text
Proyecto W establishes the current AGENT PLATFORM workspace architecture baseline.
It makes the workspace ready for audit and controlled next-phase planning, not for
implementation, migration execution, product activation, external dependency
adoption, or final substrate selection.
```

## 3. Current AGENT PLATFORM Definition

AGENT PLATFORM is a governed, agent-native cognitive workspace for coordinating architecture, agents, context, evidence, products, external sources, migration, governance, validation, security posture, and future implementation.

The current baseline is:

| Aspect | Current definition |
| --- | --- |
| Workspace identity | AGENT PLATFORM is the root workspace for architecture, governance, evidence, context, product candidates, external references, and future platform implementation. |
| Cognitive model | Humans and agents coordinate through tasks, selected context, evidence, claims, outputs, validation, governance, promotion/rejection, and learning. |
| Authority posture | Current human-readable authority lives in W-series docs under `0_architecture/workspace/`; future Cognitive Semantic System authority is conceptual and not implemented. |
| Product posture | Products are contained local-only candidates until activated by policy and governance. |
| External posture | External sources are evidence-only snapshots and remain blocked for execution, dependency adoption, instruction use, and source reuse by default. |
| Implementation posture | Implementation areas exist as placeholders or candidates, but no implementation authority exists yet. |

AGENT PLATFORM is not:

| Not | Reason |
| --- | --- |
| A product repo | The root workspace is broader than `backend-energyplus`, `cli`, `desktop`, `experimental`, `omniverse-app`, `web-platform`, or any future product. |
| A kit-app-template | Product or application templates cannot define root platform architecture. |
| An external harness | `opencode`, `pi`, `tau`, `ECC-main`, `hermes-agent`, `openclaw`, `acpx`, and other sources are references, not root runtime owners. |
| The external `graphify` source | The local external source can inform projection evaluation but cannot name or govern AGENT PLATFORM. |
| A graph database | Graph is a candidate cognitive substrate only. |
| An implementation repo yet | `3_platform/`, scripts, tools, tests, packages, and SDK areas are not ready for implementation authority. |
| A documentation dump | Documentation must declare status, scope, source class, citations, lifecycle, validation posture, and governance posture. |

## 4. Canonical Authority Baseline

Current authority layers are:

| Layer | Current role | Boundary |
| --- | --- | --- |
| Active user instruction / ticket | Controls current task scope, allowed scope, forbidden scope, deliverable, validation, and stop rule. | It does not create permanent authority outside the task unless documented and governed. |
| Human-approved governance and accepted decisions | Control approval, promotion, exceptions, lifecycle, publication, and authority-sensitive outcomes where present. | Governance is not automated yet. |
| W-series docs under `0_architecture/workspace/` | Current human-readable workspace authority baseline for Proyecto W. | Authority remains scoped by each document header and may be superseded later. |
| Future Cognitive Semantic System | Conceptual future semantic authority for accepted truth, provenance, lifecycle, relationships, context eligibility, and drift. | Not implemented; final name and substrate remain undecided. |
| Previous knowledge | Migration evidence with W-02 classification. | Prior `canonical` labels are historical only and require restatement before current authority use. |
| External sources | External evidence with W-03 and W-13 classification. | Not dependencies, active instructions, root authority, product authority, or substrate decisions. |
| Products | Local-only product candidates under `2_products/`. | Not active and not root authority. |
| Git | Artifact history and collaboration mechanism. | Git commits do not create semantic truth, governance approval, or promotion by themselves. |

Authority baseline rule:

```text
Current AGENT PLATFORM authority is explicit, scoped, cited, and governed. Nothing
becomes true because it is present, recent, generated, committed, included in
context, validated, or confidently stated.
```

## 5. Core Workspace Principles

| Principle | Current baseline |
| --- | --- |
| Active ticket controls scope. | Every task begins from the current objective, allowed scope, forbidden scope, validation, and stop rule. |
| Context is selected exposure. | Agents receive the smallest sufficient task-scoped context. |
| Context is not permission. | Reading or seeing material does not authorize edits, execution, migration, staging, commits, dependency adoption, or promotion. |
| Evidence is not truth. | Evidence supports claims but requires validation and governance before accepted authority. |
| Validation evaluates. | Validation produces validity posture and evidence; it does not approve. |
| Governance decides. | Approval, promotion, exceptions, lifecycle, ownership, and authority-sensitive outcomes require governance. |
| Agents propose; humans/governance approve. | Agents can inspect, classify, draft, validate when scoped, and recommend; they cannot approve by default. |
| Products are contained workspaces. | Product material can govern only product scope after activation and cannot define root authority by proximity. |
| External sources are evidence only. | External repositories, engines, SDKs, examples, tools, instructions, and outputs remain external unless reviewed and promoted. |
| Folder location is not authority. | Paths organize responsibility and retrieval; they do not decide truth. |
| Git commit is not semantic truth. | Repository history records artifacts but does not approve or promote meaning. |
| Generated output is not source. | Reports, logs, graphs, summaries, exports, run outputs, and generated docs are evidence/projections until reviewed and promoted. |
| Cognitive substrate remains undecided. | Graph remains a candidate only; other substrates and hybrids remain open. |

## 6. Cognitive Operating Model

W-06 defines the cognitive operating flow:

```text
Goal
-> Task
-> Context Pack
-> Evidence
-> Claim
-> Action / Recommendation
-> Output
-> Validation
-> Governance
-> Promotion / Rejection
-> Learning
```

Flow meaning:

| Transition | Current rule |
| --- | --- |
| Goal -> Task | A desired outcome must become scoped work with deliverable, validation, and stop rule. |
| Task -> Context Pack | Context is selected by source class, authority, freshness, sensitivity, and relevance. |
| Context Pack -> Evidence | Agents inspect only allowed sources and preserve status/uncertainty. |
| Evidence -> Claim | Claims must cite evidence and preserve uncertainty. |
| Claim -> Action / Recommendation | Actions require permission; recommendations require rationale. |
| Action / Recommendation -> Output | Outputs are artifacts or evidence, not truth by default. |
| Output -> Validation | Validation checks evidence or behavior within scope. |
| Validation -> Governance | Validity posture informs decisions but does not decide. |
| Governance -> Promotion / Rejection | Governance accepts, rejects, defers, scopes, or returns material for more evidence. |
| Promotion / Rejection -> Learning | Reviewed outcomes improve future behavior without rewriting evidence history. |

No transition is automatic. A useful claim does not become a decision. Passing validation does not become governance. Generated output does not become source. Agent memory does not become knowledge. External source presence does not become adoption.

## 7. Workspace Topology Baseline

The current topology remains a provisional numbered navigation model. Numbered folders are temporary navigation aids only; they do not imply priority, authority, lifecycle, or final structure.

| Area | Current baseline |
| --- | --- |
| `0_architecture/` | Architecture authority surface when status, scope, and currency allow. Current W-series root authority is under `0_architecture/workspace/`. |
| `1_research/` | Research and evidence area. Evidence only until promoted. |
| `2_products/` | Local-only product candidates. Not active, not tracked, and not root authority. |
| `3_platform/` | Future implementation candidate. Code or folders here do not define architecture by existence. |
| `4_external/` | External references, licenses, datasets, standards, and source snapshots. Evidence only. |
| `4_external/sources/` | Local-only raw external sources. Ignored and not approved for execution, dependency adoption, source reuse, or active instructions. |
| `5_workspace/` | Future workspace operations, task scaffolds, and context-pack projections. Operational support only unless promoted. |
| `6_docs/` | Future human-facing projection area. Human docs must cite source authority and do not override architecture. |
| `7_datasets/` | Local-only data area. No authority by default. |
| `8_models/` | Local-only model/checkpoint area. No authority by default. |
| `9_artifacts/` | Local-only generated artifact/output area. Generated evidence only until promoted. |
| `10_scripts/` | Future reviewed automation area. Scripts do not grant execution permission by location. |
| `11_tools/` | Future reviewed tool area. Tools require trust, lifecycle, and execution policy. |
| `12_tests/` | Future validation support area. Tests and validation results evaluate but do not govern. |
| `13_packages/` | Future package/release area. Packaging requires ownership, security, validation, and release policy. |
| `14_sdk/` | Future SDK/interface area. SDK claims require boundary, compatibility, validation, and governance. |
| `previusknowledge/` | Local migration evidence. Not current root authority and not to be committed wholesale. |

Topology rule:

```text
Use folders to find responsibility. Do not use folders to decide authority.
```

## 8. Documentation Baseline

W-09 establishes that documentation is useful only when its authority posture is explicit.

Documentation requires:

| Requirement | Meaning |
| --- | --- |
| Status | `canonical`, `draft`, `proposal`, `research`, `evidence`, `projection`, `migration_evidence`, `external_reference`, `product_scoped`, `implementation_note`, `generated`, `historical`, `superseded`, `deprecated`, or `archived`. |
| Scope | Workspace root, architecture domain, product workspace, research, external source, migration, operational, implementation, human docs, or local-only scope. |
| Citations | Claims that affect architecture, migration, product scope, external reuse, validation, governance, or security must cite evidence or be marked as proposals. |
| Lifecycle | Proposed, drafted, reviewed, canonical, superseded, deprecated, archived, or equivalent state must remain traceable. |
| Validation posture | Whether checks are not run, partial, passed for scope, failed, stale, or not applicable. |
| Governance posture | Whether material is proposed, reviewed, approved, rejected, deferred, excepted, or not applicable. |
| Source class | Canonical architecture, previous knowledge, research, external reference, product-scoped, generated, implementation note, projection, or other class. |

Current documentation baseline:

| Surface | Current role |
| --- | --- |
| `0_architecture/workspace/` | Current W-series authority surface. |
| `6_docs/` | Future human-facing projection area. |
| `1_research/` | Evidence/research area. |
| `4_external/` reviews/metadata later | Future external evidence/review area; raw sources remain local-only. |
| Product docs | Future product-scoped material after product policy and activation. |
| Generated docs | Projections/evidence only until reviewed and promoted. |
| Previous docs | Migration evidence until restated and promoted. |

## 9. Agent Operating Baseline

W-10 establishes agents as bounded operators.

Agents may, within explicit scope:

| Allowed when scoped | Meaning |
| --- | --- |
| Read | Inspect permitted authority and evidence surfaces. |
| Reason | Form claims, uncertainty, options, and recommendations from selected context. |
| Cite | Reference W-series docs, evidence paths, validation commands, and source status. |
| Draft | Create or edit explicitly allowed documentation or files. |
| Classify | Assign source status or risk posture when the task permits. |
| Validate | Run explicitly allowed validation commands and report results. |
| Propose | Recommend next decisions, blockers, and follow-up tickets without starting them. |

Agents may not do these without explicit approval:

| Prohibited by default | Meaning |
| --- | --- |
| Approve or promote | Agents cannot create authority-sensitive decisions by themselves. |
| Migrate | No moves, copies, renames, archive creation, bulk restatement, or previous knowledge transfer without a migration ticket. |
| Stage, commit, push | Repository history is human-governed. |
| Run external code | External execution requires review and approval. |
| Install dependencies | Dependency adoption requires provenance, license, security, validation, and governance. |
| Authenticate | Provider/API/OAuth/registry/channel authentication requires explicit approval. |
| Activate products | Product activation requires charter, owner, scope, Git posture, validation, security/access, dependency posture, and governance. |
| Decide substrate | Cognitive Semantic System substrate requires an explicit decision and evaluation. |

Subagents return evidence only. They do not own truth, validation approval, governance, promotion, scope expansion, or stop-rule decisions.

## 10. Governance and Promotion Baseline

W-11 defines governance as the explicit decision layer.

Governance flow:

```text
Evidence
-> Claim
-> Candidate
-> Validation Posture
-> Governance Review
-> Decision
-> Promotion / Rejection / Deferral
-> Lifecycle State
-> Learning
```

Governance clarifications:

| Clarification | Rule |
| --- | --- |
| Validation is not governance. | Checks and review can support decisions but cannot approve them. |
| Git is not governance. | Commits record state; they do not create semantic truth. |
| Context is not promotion. | Included context remains governed by source status. |
| External source presence is not adoption. | Cloned sources remain evidence until promoted by explicit decision. |
| Product scope is not root authority. | Product decisions govern product scope only unless root governance explicitly promotes a bounded claim. |

Promotion requires source status, scope, owner, evidence, validation posture, governance posture, security/access posture where relevant, migration impact, external/license posture where relevant, product scope where relevant, stop-rule compliance, and no unresolved blocker.

## 11. Product Baseline

W-12 identifies six product candidates:

| Product candidate | Current state |
| --- | --- |
| `backend-energyplus` | Local-only candidate, inactive, untracked, domain/backend integration risk. |
| `cli` | Local-only candidate, inactive, untracked, interface product candidate. |
| `desktop` | Local-only candidate, inactive, untracked, desktop runtime/package/security risk. |
| `experimental` | Local-only experimental area, blocked for activation by default. |
| `omniverse-app` | Local-only candidate, inactive, untracked, visualization/domain application risk. |
| `web-platform` | Local-only candidate, inactive, untracked, web/auth/data/deployment risk. |

Current product state:

| State | Meaning |
| --- | --- |
| All local-only | `2_products/` remains ignored. |
| All inactive | No product is active or implementation-ready. |
| All untracked | Product material must not be staged or committed by default. |
| None root authority | Product source/docs/outputs cannot define AGENT PLATFORM root architecture. |

Product activation requires:

| Requirement | Meaning |
| --- | --- |
| Charter | Product purpose, users, outcomes, non-goals, and root relationship. |
| Owner | Accountable product owner and relevant product roles. |
| Scope | Product boundaries, product authority, root interactions, and product-specific behavior. |
| Git posture | Local-only, docs-only, source-tracked, split repo, submodule/subtree/reference, or deferred/archive decision. |
| Validation | Baseline checks, acceptance criteria, evidence retention, and limitations. |
| Security/access | Secrets, credentials, data, network, provider auth, local files, generated outputs, and publication posture. |
| External dependency posture | Product-specific provenance, license, security, validation, and governance review. |
| Governance | Activation approval, lifecycle, root-boundary statement, and blocker handling. |

## 12. External Source Baseline

W-03 and W-13 cover 12 current external sources:

| Source | Current baseline |
| --- | --- |
| `acpx` | Assistant/protocol integration evidence. |
| `ai-cookbook-main` | Cookbook/example corpus evidence. |
| `clawhub` | Registry/catalog evidence. |
| `ECC-main` | Agent harness / agent OS evidence. |
| `EnergyPlusV24-2-0` | Domain simulation engine reference, product/domain scoped. |
| `graphify` | External graph-oriented projection/candidate substrate evidence only. |
| `hermes-agent` | Self-improving agent evidence and risk source. |
| `openclaw` | Assistant/gateway evidence. |
| `opencode` | Coding-agent session/context/tool evidence. |
| `openstudio` | Building energy modeling SDK/tooling reference, product/domain scoped. |
| `pi` | Coding-agent harness evidence. |
| `tau` | Minimalist coding-agent harness evidence with license/instruction caution. |

Current source status:

| Status | Applies now |
| --- | --- |
| `external_reference` | Yes, all 12 sources. |
| `local_only` | Yes, all raw source snapshots under `4_external/sources/`. |
| `not_promoted` | Yes, all 12 sources. |
| `execution_blocked` | Yes, all 12 sources. |
| `dependency_blocked` | Yes, all 12 sources. |
| `instruction_blocked` | Yes, all external instructions and equivalent files. |

External sources can teach AGENT PLATFORM through reviewed patterns, risks, vocabulary, and evidence. They cannot execute, authorize, name, govern, become active instructions, become dependencies, activate products, decide substrate, or become root architecture by proximity.

## 13. Migration Baseline

W-08 defines migration as controlled transition, not movement.

Migration means:

```text
classify
-> restate
-> cite
-> validate
-> govern
-> promote / retain / defer / archive
```

Migration clarifications:

| Clarification | Rule |
| --- | --- |
| No bulk migration | Do not copy the previous corpus into current architecture or docs. |
| No previous knowledge dump | Use W-02 classification and restate concepts in current vocabulary. |
| No product code migration | Product movement requires product policy, activation, Git posture, validation, and security review. |
| No external source migration | Raw external source snapshots stay isolated and local-only. |
| No archive until archive policy | `_archive/` is future-only until lifecycle, metadata, restoration, and deletion rules exist. |
| First migration should be small | The first controlled batch should be narrow, cited, validation-backed, auditable, and reversible in understanding. |

Migration readiness:

| Area | Current state |
| --- | --- |
| Previous knowledge | Classified and ready for controlled restatement planning only. |
| Current W-series docs | Preserved in place as current authority baseline. |
| External metadata | Policy exists, but migration not executed. |
| Product material | Blocked until product charters and product governance exist. |
| Archive | Blocked until archive policy exists. |
| Implementation | Blocked until implementation readiness exists. |

## 14. Current Local-Only / Do-Not-Commit Baseline

The following material must remain local-only or must not be committed by default:

| Material | Reason |
| --- | --- |
| `previusknowledge/` | Migration evidence; do not commit wholesale without governance. |
| `2_products/` | Product candidates are ignored/local-only and inactive. |
| `4_external/sources/` | Raw external sources are ignored/local-only and license/security sensitive. |
| `7_datasets/` | Data may be large, licensed, private, or unreviewed. |
| `8_models/` | Models/checkpoints may be large, licensed, unsafe, or private. |
| `9_artifacts/` | Generated outputs are evidence/projections, not source by default. |
| Generated outputs | Reports, exports, builds, run outputs, summaries, and projections require review before promotion. |
| Runtime logs | Logs can contain sensitive, partial, stale, or misleading evidence. |
| Office files | `*.xlsx`, `*.xls`, `~$*`, `desktop.ini`, and `Thumbs.db` are ignored/local artifacts. |
| Secrets | Never commit or expose. |
| Credentials | Never commit or expose. |
| Dependency folders | `.venv/`, `venv/`, `node_modules/`, `dist/`, `build/`, caches, and similar generated/dependency material. |
| Product code | Local-only until product Git posture changes by governance. |
| Raw external source code | Local-only until exact source reuse/tracking is approved. |

Local-only rule:

```text
Ignored does not mean irrelevant, and local-only does not mean safe to expose.
Local-only material can be evidence, but it is not commit-ready by default.
```

## 15. Current Commit-Safe Baseline

The following can be committed only by explicit human approval and exact file staging:

| Material | Commit condition |
| --- | --- |
| W-series canonical docs under `0_architecture/workspace/` | Commit-safe after review, validation, and explicit human approval. |
| `README.md` | Only by explicit docs/workspace ticket. |
| `.gitignore` | Only by explicit workspace/Git ticket and approval for ignore-policy change. |
| Future `1_research/` docs | Only after source review, sensitivity review, status/scope labels, and explicit ticket. |
| Future external metadata/reviews | Only after provenance, license/risk posture, review limits, and explicit ticket; raw source snapshots remain excluded. |
| Future docs projections | Only after source authority exists and projections cite canonical sources. |

Commit rules:

| Rule | Meaning |
| --- | --- |
| No `git add .` | Broad staging can include local-only, generated, product, external, dependency, or sensitive material. |
| Exact file staging only | Stage only paths explicitly approved by a human. |
| Git status first | Inspect `git status --short` before any proposed commit. |
| Git does not promote | A commit records artifacts but does not create truth, validation approval, or governance approval. |

## 16. Open Decisions / Explicitly Undecided

| Open decision | Current state |
| --- | --- |
| Final Cognitive Semantic System name | `Cognitive Semantic System` is the neutral working name; final naming ADR remains open. |
| Final cognitive substrate | Undecided. |
| Whether graph remains primary substrate | Undecided; graph remains a candidate only. |
| Numbered folder permanence | Current numbered topology is provisional navigation only. |
| Product activation | No products active. |
| Product Git posture | `2_products/` remains ignored/local-only. |
| External metadata migration | Policy exists; migration not executed. |
| Archive policy | Not defined; `_archive/` not created. |
| Validation registry | Not defined. |
| Security/access policy | Not defined. |
| Implementation readiness | Not established. |
| Harness strategy | Own harness vs existing harness vs semantic meta-layer remains undecided. |
| Governance automation | Conceptual model exists; automation not implemented. |
| Context-pack physical format | Strategy exists; physical storage and generation format remain undecided. |
| Migration first batch | Not selected or executed. |

Open-decision rule:

```text
An unresolved decision is a blocker, not permission to improvise. Future work must
preserve uncertainty until a scoped decision resolves it.
```

## 17. Implementation Blockers

Implementation must not begin until these blockers are resolved or explicitly excepted by governance:

| Blocker | Why it blocks implementation |
| --- | --- |
| No security/access policy | Agents, scripts, tools, providers, shell, network, MCP, secrets, sensitive files, and publication need enforceable boundaries. |
| No validation registry/proof model | Implementation needs tests, proof levels, evidence retention, and validation sufficiency rules. |
| No archive policy | Migration and supersession need lifecycle handling before moving old or obsolete material. |
| No product charters | Product code cannot become active without purpose, owner, scope, validation, security, and Git posture. |
| No external dependency approvals | External code, SDKs, engines, examples, packages, and tools cannot be installed, run, copied, or adopted. |
| No Cognitive Semantic System substrate decision | Semantic-system implementation cannot choose storage/representation prematurely. |
| No implementation readiness assessment | `3_platform/`, scripts, tools, tests, packages, and SDK areas lack readiness gates. |
| No Git posture for product or external metadata | Product and external material cannot be tracked safely without explicit decisions. |
| No migration audit | Any first migration batch needs audit criteria before execution. |
| No harness strategy decision | The workspace has not decided own harness, existing harness adoption, or semantic meta-layer approach. |

Implementation blocker rule:

```text
Architecture readiness is not implementation readiness. Proyecto W closes the
workspace baseline; it does not clear the blockers for building the platform.
```

## 18. Recommended Next Phase

The next phase should reduce risk before any migration, implementation, product activation, or external adoption.

| Option | Description | Strength | Risk / limitation | W-14 evaluation |
| --- | --- | --- | --- | --- |
| A) W-A - Workspace Architecture Audit | Audit W-00 through W-14 for consistency, coverage, conflicts, citations, local-only posture, stop rules, and readiness. | Lowest-risk closure check before action; validates the baseline before it becomes a launchpad. | Delays execution, but intentionally. | Recommended next phase. |
| B) M-01 - Workspace Canonical Docs Commit Hygiene | Prepare status/diff/file list for a possible human-approved commit. | Useful after audit for preserving W-series docs. | Premature if architecture issues remain. | Do after W-A unless the human prioritizes commit hygiene. |
| C) W-15 - Harness Strategy Decision | Decide own harness vs existing harness vs semantic meta-layer. | Important before agent/runtime implementation. | Too early without security/access and validation audit. | Defer until after W-A and likely S-00/V-00. |
| D) S-00 - Security / Access Architecture | Define secrets, files, shell, network, provider, MCP, publication, and local-only access policy. | Critical blocker for implementation and agent execution. | Should consume audit findings. | High-priority after W-A. |
| E) V-00 - Validation Registry Architecture | Define proof levels, validation evidence retention, and command posture. | Critical blocker for migration and implementation. | Should align with security/access and audit results. | High-priority after W-A. |
| F) CSS-00 - Cognitive Semantic System Naming/Substrate ADR | Decide naming path and substrate evaluation frame. | Critical before semantic-system implementation. | Too important to rush; needs security, validation, and audit context. | Defer until after W-A, then schedule deliberately. |
| G) First controlled migration batch | Restate one small carry-forward concept set. | Useful once controls exist. | Premature before audit, archive, validation, and security posture. | Not recommended immediately. |

Recommended next phase:

```text
Run W-A - Workspace Architecture Audit before implementation or migration.
```

Rationale:

| Reason | Explanation |
| --- | --- |
| W-series is now large enough to audit. | W-00 through W-14 create a complete baseline that should be checked for consistency before it drives work. |
| Audit is lower risk than migration. | It reads and verifies; it does not move files or change Git posture. |
| Audit can sequence blockers. | It can identify whether S-00, V-00, CSS-00, M-01, or harness strategy should happen next. |
| Audit protects authority. | It prevents contradictions, stale claims, missing citations, and drift from becoming implementation assumptions. |

## 19. Final Readiness Verdict

| Question | Verdict |
| --- | --- |
| Is Proyecto W complete at architecture level? | Yes. W-14 closes the architecture/documentation baseline for Proyecto W. |
| Is AGENT PLATFORM ready for implementation? | No. Security/access, validation registry, implementation readiness, substrate, harness, and dependency decisions are missing. |
| Is AGENT PLATFORM ready for migration execution? | No. It is ready for audit and migration planning, but not first migration execution. |
| Is AGENT PLATFORM ready for product activation? | No. No product has charter, owner, scope, Git posture, validation baseline, security/access posture, external dependency posture, or governance approval. |
| Is AGENT PLATFORM ready for external dependency adoption? | No. External sources remain evidence-only, execution-blocked, dependency-blocked, and instruction-blocked. |
| Is AGENT PLATFORM ready for final substrate decision? | No. Graph and other substrate options require explicit evaluation and ADR. |
| What is it ready for now? | Workspace Architecture Audit, commit-hygiene planning after audit, security/access architecture, validation registry architecture, and scoped next-phase decision planning. |

Readiness statement:

```text
AGENT PLATFORM is ready to be audited as a governed architecture baseline. It is
not ready to be built, migrated, activated as products, connected to external
dependencies, or collapsed into a final cognitive substrate.
```

## 20. Final Synthesis Statement

AGENT PLATFORM is now defined as a governed, agent-native cognitive workspace. Its current human-readable authority is the W-series architecture under `0_architecture/workspace/`. The workspace separates authority, evidence, context, validation, governance, products, external sources, migration, local-only material, generated output, and future implementation.

Proyecto W decides that the platform root is not a product repository, not an external harness, not the external `graphify` source, not a graph database, not an implementation repo, and not a documentation dump. The future Cognitive Semantic System remains conceptual, neutrally named, and substrate-undecided. Graph remains a candidate only.

Previous knowledge remains classified migration evidence. External sources remain controlled evidence. Product folders remain inactive local-only candidates. Generated outputs remain projections/evidence. Agents remain bounded operators. Validation evaluates. Governance decides. Git records artifacts but does not create semantic truth.

Final baseline:

```text
Proyecto W closes with AGENT PLATFORM as a governed workspace architecture baseline:
explicit scope, selected context, evidence separation, human/governance approval,
product containment, external-source isolation, migration discipline, and substrate
neutrality before implementation.
```

## 21. Stop Rule

After W-14, stop.

Do not:

| Prohibited after W-14 without new instruction | Meaning |
| --- | --- |
| Create W-A | Recommendation only; do not start it here. |
| Create W-15 | Harness strategy remains a future decision. |
| Start migration | No movement, copy, rename, archive, or restatement batch. |
| Stage files | No Git staging. |
| Commit | No commit. |
| Push | No push. |
| Move files | No topology or migration action. |
| Run code | Validation path checks are allowed by the W-14 ticket; no code execution otherwise. |
| Inspect external sources deeply | W-14 consumes W-03 and W-13 only. |
| Create implementation files | No platform, product, scripts, tools, tests, packages, SDK, or semantic-system implementation. |

W-14 stop statement:

```text
W-14 closes Proyecto W and stops. The next phase requires explicit user instruction.
```
