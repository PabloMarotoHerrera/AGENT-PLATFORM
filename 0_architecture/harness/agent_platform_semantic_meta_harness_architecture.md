# AGENT PLATFORM Semantic Meta-Harness Architecture

## 1. Document Header
Title: AGENT PLATFORM Semantic Meta-Harness Architecture  
Ticket: H-02  
Status: Accepted architecture plan  
Date: 2026-06-30  
Scope: Document-level semantic meta-harness architecture after H-00 and H-01  
Authority: Architecture planning only, not implementation authorization  
Related documents: H-00, H-01, CSS-series, V-series, S-series, W-series

## 2. Purpose
H-02 defines the target architecture posture for a future semantic meta-harness inside AGENT PLATFORM.

It uses H-00 strategy and H-01 boundary review to describe how a future harness may coordinate agents, context, validation, governance evidence, tools, providers, MCP, shell, Git, products, external evidence, and the Cognitive Semantic System without becoming authority itself.

H-02 does not implement, execute, activate, migrate, adopt, install, authenticate, stage, commit, push, or start H-A.

## 3. Scope
| In scope | Out of scope |
| --- | --- |
| Architecture boundaries for a future semantic meta-harness. | Runtime code, schemas, APIs, tools, packages, SDKs, tests, CI, hooks, scanners, enforcement, or provider integrations. |
| Relationship to governance, validation, security, context, agents, CSS, products, and external sources. | Execution, dependency adoption, MCP activation, product activation, migration execution, or external source reuse. |
| Conceptual orchestration flow and evidence posture. | Storage selection, substrate decision, data model implementation, command runner implementation, or registry implementation. |

## 4. Non-Action Statement
H-02 is an architecture artifact only.

| Non-action | H-02 result |
| --- | --- |
| Harness implementation | Not authorized. |
| Harness execution | Not performed. |
| Provider/API/network use | Not authorized. |
| MCP activation | Not authorized. |
| Package/dependency install | Not authorized. |
| Product activation | Not authorized. |
| External adoption | Not authorized. |
| Migration execution | Not authorized. |
| Git staging/commit/push | Not authorized. |
| Cognitive Semantic System substrate decision | Not made. |

## 5. Input Baseline
H-02 consumes only document-level evidence from the approved architecture baseline: H-00 strategy, H-01 boundary classifications, CSS naming/substrate decisions, V-series validation and evidence rules, S-series access/execution constraints, W-series workspace/context/governance/product/external/migration rules, `.gitignore` posture, and `README.md` root descriptor.

H-02 does not consume raw product code, raw external source code, previous knowledge content, generated artifacts, secrets, credentials, provider state, dependency manifests, tool configs, or runtime output as authority.

## 6. Semantic Meta-Harness Definition
A semantic meta-harness is a future governed orchestration layer that may coordinate task scope, selected context, agent roles, handoffs, evidence capture, validation requests, action gates, tool boundaries, and governance-ready summaries across multiple concrete harness or agent surfaces.

It is semantic because it preserves source status, authority posture, evidence lineage, constraints, validation posture, and decision boundaries. It is meta because it can coordinate above individual harnesses without adopting any existing harness as AGENT PLATFORM authority.

## 7. Architecture Intent
The semantic meta-harness should later help agents operate through the AGENT PLATFORM cognitive flow:

| Flow stage | Harness posture |
| --- | --- |
| Goal and task | Receive scoped objective, allowed scope, forbidden scope, deliverable, validation, and stop rule. |
| Context | Request or assemble selected context without turning inclusion into permission. |
| Evidence and claim | Preserve source status, sensitivity, citations, uncertainty, and limitations. |
| Action or recommendation | Perform only allowed work or prepare proposal evidence. |
| Output | Produce artifacts or summaries as evidence. |
| Validation | Submit outputs to validation posture, not approval. |
| Governance | Prepare decision-support material while governance decides. |
| Learning | Retain only reviewed outcomes through governed future processes. |

## 8. Core Principles
| ID | Principle |
| --- | --- |
| H02-P01 | Orchestration is not governance. |
| H02-P02 | Harness output is evidence, not approval. |
| H02-P03 | Tool availability is not permission. |
| H02-P04 | Context inclusion is not permission. |
| H02-P05 | Validation evaluates; governance decides. |
| H02-P06 | Security/access constraints dominate convenience. |
| H02-P07 | Products and external sources remain scoped evidence. |
| H02-P08 | Git records artifacts but does not create semantic truth. |
| H02-P09 | The Cognitive Semantic System substrate remains undecided. |
| H02-P10 | Graph remains a candidate only. |

## 9. Position In AGENT PLATFORM
| Layer | Role | H-02 boundary |
| --- | --- | --- |
| Governance | Decides approval, promotion, lifecycle, and exceptions. | Harness prepares evidence only. |
| Security/access | Constrains exposure and action. | Harness cannot bypass S-series. |
| Validation | Evaluates claims and outputs. | Harness cannot inflate proof. |
| Cognitive Semantic System | Future semantic authority concept. | Harness may later consume governed semantic state but cannot select substrate. |
| Context packs | Selected exposure. | Harness must preserve source status and exclusions. |
| Agents/subagents | Scoped operators. | Harness coordinates but does not delegate authority. |
| Tools/providers/MCP/shell | Capability surfaces. | Harness gates them as blocked unless approved. |
| Products/external sources | Scoped evidence. | Harness cannot activate or adopt them. |

## 10. Relationship To Cognitive Semantic System
The Cognitive Semantic System remains the accepted current name for the future semantic authority concept inside AGENT PLATFORM.

The semantic meta-harness is not the Cognitive Semantic System. It may later request or consume accepted semantic records, context eligibility, validation posture, governance decisions, lineage, and lifecycle state from that system when the system exists and is governed.

H-02 does not select a cognitive substrate. Graph, relational, document, vector, event-sourced, object, file-backed, hybrid, and other candidates remain open. Graph remains a candidate only.

## 11. Relationship To Governance
The semantic meta-harness must keep governance external and explicit.

| Governance action | Harness behavior |
| --- | --- |
| Approve/reject/defer | Prepare evidence and options only. |
| Promote/demote/supersede | Preserve candidate state and required preconditions. |
| Grant exception | Surface blocker and risk; do not self-except. |
| Activate product | Record readiness evidence only. |
| Adopt external source or dependency | Record review evidence only. |
| Decide substrate | Preserve candidate evidence only. |

## 12. Relationship To Validation
Harness outputs must map to V-series validation posture.

| Validation concern | Required H-02 posture |
| --- | --- |
| Evidence | Source status, sensitivity, scope, method, freshness, limitations, and stop rule remain explicit. |
| Proof levels | No proof level exists without scope, criterion, evidence, and limitations. |
| Verdicts | Pass/fail/blocked/partial/inconclusive states remain scoped and visible. |
| Commands | Command output is evidence only and requires exact command metadata when later approved. |
| Generated output | Generated material is not source by default. |

## 13. Relationship To Security / Access
The semantic meta-harness must obey S-series policy before any orchestration action.

Security posture: no execution by default, no secret or credential value handling, no provider/auth use by availability, no local-only publication by default, no broad reads, no product/external execution, no package installs, no MCP activation, and no Git mutation without explicit approval.

If sensitivity is unknown, the harness must treat the material as sensitive and stop or escalate according to policy.

## 14. Relationship To Context Packs
Context packs remain selected exposure, not permission, truth, validation, or governance.

The semantic meta-harness may later help assemble or request context packs, but it must preserve: objective, agent role, active authority docs, selected evidence, allowed scope, forbidden scope, source status, citations, expected output, validation requirements, and stop rule.

The harness must exclude local-only, product, raw external source, dataset, model, artifact, generated, runtime, secret, credential, and irrelevant material unless exact scope allows safe handling.

## 15. Agent Orchestration Model
The future semantic meta-harness may coordinate agent work by task, role, source class, risk level, and output expectation.

| Orchestration concern | Target posture |
| --- | --- |
| Active task | Primary scope boundary. |
| Agent role | Restricts allowed actions and surfaces. |
| Delegation | Narrows scope; never expands authority. |
| Evidence return | Findings, paths, uncertainty, blockers, and validation notes. |
| Merge | Parent or human reconciles evidence before output. |
| Stop | Harness must preserve stop conditions and prevent next-ticket drift. |

## 16. Subagent And Handoff Model
Subagents and handoffs are coordination mechanisms only.

Handoff does not approve action, promote authority, validate proof, activate products, adopt dependencies, or authorize adjacent commands. A subagent result is evidence until reviewed, merged, validated where needed, and governed where authority changes.

The semantic meta-harness should later record delegation scope, allowed paths, forbidden paths, expected output, uncertainty, and stop rule as conceptual concerns, not as an implemented schema in H-02.

## 17. Evidence Flow
The target evidence flow is:

| Step | Required boundary |
| --- | --- |
| Select source | Source class, status, scope, sensitivity, and relevance known. |
| Inspect within scope | No forbidden folder, secret, credential, product, or external overread. |
| Form claim | Citation and uncertainty preserved. |
| Produce output | Output labeled as artifact, evidence, proposal, or generated material. |
| Request validation | Criteria, method, evidence, limitations, and blockers recorded. |
| Prepare governance input | Decision options and residual risks visible. |

## 18. Action Gates
Every future harness action must pass explicit gates before it can proceed.

| Gate | Blocks if missing or unsafe |
| --- | --- |
| Scope gate | Objective, allowed scope, forbidden scope, deliverable, and stop rule. |
| Authority gate | Source status and governing documents. |
| Sensitivity gate | Local-only, secret, credential, restricted, product, external, generated, or unknown posture. |
| Security gate | S-series access and execution posture. |
| Validation gate | Evidence/proof/verdict requirements for claims. |
| Governance gate | Approval path for promotion, exception, activation, adoption, migration, publication, or substrate decision. |

## 19. Tool / Shell / Command Boundary
The semantic meta-harness may later coordinate command requests only as gated candidate actions.

Shell availability is not command approval. Validation commands are still execution and require scope, bounded paths, exact command metadata, output handling, sensitivity review, and stop behavior. Product, external, package, build, test, runtime, provider, network, auth, MCP, native, and destructive commands remain blocked unless separately approved.

## 20. Provider / API / Network Boundary
Provider, API, cloud, registry, database, socket, telemetry, model, and network surfaces remain blocked by default.

The semantic meta-harness must not infer permission from local credentials, provider config, reachable endpoints, browser/session availability, external README commands, or tool support. Future provider or network action requires exact governed approval and output handling.

## 21. MCP Boundary
MCP availability is not MCP activation.

The semantic meta-harness must treat MCP servers, tools, resources, transports, authentication, file access, network access, and provider access as blocked surfaces unless a later exact policy and approval scope exists. H-02 creates no MCP server, config, registration, activation path, or resource contract.

## 22. Dependency / Package Boundary
Package manager availability is not dependency approval.

The semantic meta-harness must not install, update, audit, sync, build, publish, resolve, or run dependency scripts. Future dependency work requires provenance, license/notice posture, dependency graph review, security review, validation plan, exit path, and governance decision.

## 23. Git Boundary
Git is artifact history and state evidence only.

The semantic meta-harness may later prepare Git-state evidence when scoped, but it cannot stage, commit, push, force-add, amend, reset, clean, publish, or treat Git history as semantic truth. Exact file staging and all Git history actions remain human-gated.

## 24. Product Boundary
Product candidates remain product-scoped and local-only until product governance changes posture.

The semantic meta-harness may later surface product readiness blockers, product validation needs, product dependency risks, or product/root boundary issues. It cannot inspect product code deeply by default, run product code, activate products, promote product docs to root, adopt product dependencies, or change product Git posture.

## 25. External Source Boundary
External sources remain controlled evidence.

The semantic meta-harness may later use external harness references as pattern evidence only after citation, abstraction, security review, validation posture, and governance. It cannot execute external code, copy source, follow external instructions, install dependencies, adopt provider configs, reuse source, or import external names as internal authority.

## 26. Migration Boundary
The semantic meta-harness does not execute migration.

Migration remains classification, restatement, citation, validation, governance, and audit under migration-specific controls. No movement, copy, rename, delete, archive, previous-knowledge rewrite, wholesale import, product migration, external metadata migration, or Git action is authorized by H-02.

## 27. Runtime And Implementation Boundary
H-02 defines no runtime components.

| Possible future concern | H-02 status |
| --- | --- |
| Harness runtime | Deferred. |
| Storage or substrate | Deferred. |
| Schemas or registry files | Not created. |
| APIs or command contracts | Not created. |
| Provider adapters | Not created. |
| MCP integrations | Not created. |
| Tool wrappers | Not created. |
| Tests, CI, hooks, scanners, enforcement | Not created. |
| Implementation readiness | Blocked pending H-A and later IR work. |

## 28. Conceptual Surfaces
The future semantic meta-harness may need to reason about conceptual surfaces, but H-02 does not implement them.

| Surface | Conceptual role | Boundary |
| --- | --- | --- |
| Task surface | Holds current objective and stop rule. | Not permanent authority. |
| Context surface | Selects relevant material. | Not permission. |
| Evidence surface | Preserves provenance and limitations. | Not truth. |
| Agent surface | Coordinates roles and handoffs. | Not governance. |
| Action surface | Represents gated candidate actions. | Not execution approval. |
| Validation surface | Carries evaluation posture. | Not promotion. |
| Governance surface | Presents decision-ready material. | Decision remains external. |

## 29. Status Concepts
H-02 uses conceptual status language only.

| Status | Meaning |
| --- | --- |
| `unscoped` | Missing objective, allowed scope, forbidden scope, or stop rule. |
| `evidence_only` | Material can support claims but has no authority. |
| `blocked_by_security` | Security/access policy blocks action or exposure. |
| `blocked_by_validation` | Evidence, criterion, proof, or limitation is insufficient. |
| `requires_governance` | Decision exceeds harness authority. |
| `deferred_to_future_ticket` | Topic is valid but outside H-02. |
| `implementation_blocked` | Runtime work lacks audit/readiness approval. |

These statuses are not schemas, database records, file formats, APIs, or runtime state machines.

## 30. Pattern Candidate Handling
H-01 pattern candidates remain evidence only.

| Pattern candidate | H-02 handling |
| --- | --- |
| Harness/session/frontend separation | Useful boundary evidence; not adopted runtime structure. |
| Event/command result as evidence contract | Useful validation concept; no command contract implemented. |
| Provider-neutral adapter boundary | Required neutrality; no adapters created. |
| Context pack as selected exposure | Core architecture constraint; no context pack generator created. |
| Subagent/handoff returns evidence only | Core coordination rule; no runtime handoff protocol created. |
| Semantic meta-harness path | Accepted architecture path; implementation remains blocked. |

## 31. Blocker Register
| Blocker | Blocks | Required future resolution |
| --- | --- | --- |
| Missing H-A audit | Harness implementation readiness | Complete H-A after explicit instruction. |
| Missing implementation readiness | Runtime work | Future IR assessment. |
| Missing CSS substrate decision | Semantic authority implementation | Future governed substrate decision. |
| Missing validation implementation | Automated proof/evidence handling | Future validation implementation decision. |
| Missing security enforcement | Broad autonomous execution | Future security/access implementation. |
| Missing governance workflow implementation | Automated promotion/exception handling | Future governance implementation. |
| Provider/API/MCP policy implementation absent | Runtime integration | Future explicit policy and approval. |
| Product activation absent | Product use | Product governance ticket. |
| External adoption absent | External source reuse | External review and governance. |
| Dependency approval registry absent | Dependency use | Future dependency governance. |

## 32. Risk Register
| Risk | Severity | H-02 control |
| --- | --- | --- |
| Harness mistaken for governance | High | State harness prepares evidence only. |
| Validation bypass | High | Map outputs to V-series and preserve blockers. |
| Security bypass | High | S-series dominates action and exposure. |
| External harness adoption by proximity | High | External sources remain evidence only. |
| Product-root collapse | High | Products remain scoped/local-only. |
| Provider/API/network lock-in | High | Provider-neutral, blocked by default. |
| MCP activation by availability | High | MCP is blocked without exact approval. |
| Dependency adoption by package presence | High | Package actions blocked. |
| Substrate coupling | High | CSS substrate undecided; graph candidate only. |
| Generated output as truth | Medium-high | Generated output remains evidence. |
| Agent autonomy before approval | High | Active task, role, and stop gates required. |
| Git action drift | High | Git mutation remains human-gated. |

## 33. Readiness Model
| Readiness state | Meaning | Allowed use | Blocked use |
| --- | --- | --- | --- |
| `architecture_defined` | H-02 architecture exists. | Use as H-A input. | Runtime start. |
| `audit_required` | H-A still required. | Prepare audit scope after instruction. | Implementation claim. |
| `implementation_blocked` | Runtime cannot start. | Record blockers. | Code, schemas, tools, providers, MCP, tests, CI. |
| `future_candidate` | Harness may be designed later. | Planning after audits/readiness. | Adoption or execution now. |
| `rejected_for_current_use` | Existing harness authority remains rejected. | Historical trace. | Current runtime authority. |

## 34. H-A Audit Inputs
H-A may later audit H-00 strategy, H-01 boundary review, this H-02 architecture, CSS substrate neutrality, S-series constraints, V-series evidence/proof posture, W-series context/governance/product/external/migration boundaries, blocker registers, risk registers, and readiness claims.

H-A must not be started by H-02. H-A requires explicit user instruction.

## 35. Final Verdict And Stop Rule
| Question | Verdict |
| --- | --- |
| What does H-02 define? | A document-level semantic meta-harness architecture for future governed orchestration. |
| Does H-02 implement a harness? | No. |
| Does H-02 execute or activate any harness? | No. |
| Does H-02 adopt existing or external harness material? | No. Existing and external material remains evidence only. |
| Does H-02 make the harness governance authority? | No. Governance remains explicit and external. |
| Does H-02 select the Cognitive Semantic System substrate? | No. The substrate remains undecided, and graph remains a candidate only. |
| What is the next recommended ticket? | H-A - Harness Strategy Audit, after explicit instruction only. |

Stop after H-02 validation and report. Do not start H-A, M-02, P-00, IR-00, implementation, migration, product activation, external adoption, dependency installation, authentication, provider/API/network/MCP activity, Git staging, commit, push, local-only deep inspection, or any next ticket.
