# G-00 - Active Platform Direction Decision

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Active Platform Direction Decision |
| Ticket | G-00 |
| Status | Accepted direction decision |
| Date | 2026-07-02 |
| Scope | Decide the post-I-A direction from bounded metadata implementation toward a future active governed AGENT PLATFORM for Siamese. |
| Authority | Governance direction only, not implementation, activation, source tracking expansion, dependency adoption, or product activation. |
| Related documents | I-A, I-00 through I-07, IR-A, P-08 through P-10, W-03, W-12, W-13, V-series, S-series, H-series, CSS-series, `.gitignore`, README.md |

## 2. Purpose
I-A closed FASE 6 at bounded metadata-implementation audit level only. G-00 decides the strategic platform direction after that audit. G-00 does not create runtime, agents, tools, providers, adapters, products, APIs, MCP, graph, vector, database, ontology, persistence, tests, scripts, package manifests, or activation artifacts.

The purpose of G-00 is to define what an active platform should mean, how AGENT PLATFORM should move toward it through governed phases, and which gates remain mandatory before any future implementation expansion.

## 3. Decision Summary
AGENT PLATFORM should proceed toward an active governed agent platform, not a collection of loose projects, cloned harnesses, product prototypes, or source-adjacent experiments.

The chosen direction is:

| Decision area | G-00 direction | Current authorization |
| --- | --- | --- |
| Platform identity | Build AGENT PLATFORM as the governed root platform for Siamese. | Direction only. |
| Product vision | Siamese remains the living energy twin product vision context. | Terminology/context only. |
| Active platform | Future target state with governed runtime, evidence, validation, security, agents, tools, providers, and products. | Not active now. |
| Implementation path | Use staged activation gates from metadata-only skeleton to active platform. | Future tickets only. |
| Cognitive Semantic System | Keep accepted name and substrate-neutral posture. | No final substrate selected. |
| Graph | Remains a candidate representation/substrate only. | Not adopted. |
| Graphify | Evidence only, not authority. | Not adopted. |
| Hermes | External architecture evidence and possible future adapter candidate only. | Not adopted or inspected. |
| Validation | Evaluates evidence. | Does not decide. |
| Governance | Decides activation and exceptions. | Required for every promotion. |

G-00 advances direction, not activation level.

## 4. Current State After I-A
| Area | Current post-I-A state | Boundary retained |
| --- | --- | --- |
| FASE 6 | Audit-complete at bounded metadata-implementation level. | Not production-ready or runtime-ready. |
| Governed skeleton | `3_platform/_governed_skeleton/` is the only approved implementation subroot. | Existing `3_platform` siblings remain uninspected and unapproved. |
| Validation registry | Metadata-only, in-memory, stdlib-only by contract. | No validation execution. |
| Security/access evaluator | Metadata-only, in-memory, stdlib-only by contract. | No runtime enforcement or secret scanning. |
| Context runtime | Metadata-only, in-memory, stdlib-only by contract. | No source loading or context permission. |
| Provider/adapter layer | Metadata-only, in-memory, stdlib-only by contract. | No API, network, auth, provider, adapter, or MCP activation. |
| Agent runtime boundary | Metadata-only, in-memory, stdlib-only by contract. | No agent execution, task execution, handoff execution, or orchestration runtime. |
| Tool execution boundary | Metadata-only, in-memory, stdlib-only by contract. | No tool, shell, subprocess, filesystem, network, or Git execution authorization. |
| Cognitive Semantic System prototype | Metadata-only, in-memory, stdlib-only by contract. | No final substrate, graph runtime, vector runtime, database, ontology, persistence, or reasoning engine. |
| Products | Inactive and local-only. | No product source tracking, execution, dependency adoption, or activation. |
| External sources | Local-only external evidence. | No source reuse, dependency adoption, execution, or active instructions. |
| Git | Exact-path review only after human approval. | No broad staging, force-add, commit, push, or publication. |

The platform is therefore pre-active. It has governance records and bounded metadata components, but no active runtime authority.

## 5. North Star
AGENT PLATFORM should become the governed agent-native operating layer for Siamese, a living energy twin platform for buildings.

The target platform should eventually be able to receive governed goals, assemble bounded context, represent evidence and semantic state, evaluate validation and security posture, route work through approved agents and tools, interact with approved providers and product surfaces, and produce auditable outputs without leaking local-only data or confusing evidence with authority.

The North Star is not unrestricted autonomy. It is controlled agency under governance, validation, security, provenance, least privilege, and reversible activation.

## 6. Active Platform Definition
An active AGENT PLATFORM is a future state where governed runtime components can perform approved work under explicit scope, evidence, security, validation, and audit controls.

Active platform means all of the following are present before meaningful activation:

| Capability | Required future property | Current state |
| --- | --- | --- |
| Governance | Each promotion has owner, scope, stop rule, rollback, and decision record. | Direction only. |
| Validation | Evidence can be evaluated and retained with proof limits. | Metadata only. |
| Security | Access decisions can constrain real actions. | Metadata only. |
| Context | Context packs can be assembled from approved sources only. | Metadata only. |
| Runtime | Runtime can schedule and execute approved task envelopes. | Not created. |
| Agents | Agents can participate only within approved roles and permissions. | Not active. |
| Tools | Tools can execute only after exact approval and audit logging. | Not executable. |
| Providers/adapters | Providers and adapters can be activated only after dependency, auth, network, and data review. | Not active. |
| Cognitive Semantic System | Semantic state can support memory, claims, relations, and provenance under a selected substrate. | Substrate deferred. |
| Products | Product surfaces can consume platform capabilities only after product activation gates. | Inactive. |

Active platform does not mean self-modification, broad file access, automatic product activation, external-source promotion, provider access by convenience, or semantic truth by generated projection.

## 7. Direction Principles
| ID | Principle |
| --- | --- |
| G00-P01 | Direction precedes activation. |
| G00-P02 | Governance decides; validation evaluates. |
| G00-P03 | Metadata components do not authorize runtime behavior. |
| G00-P04 | No source, product, dependency, provider, tool, or external architecture becomes authority by proximity. |
| G00-P05 | Product work remains product-scoped and cannot decide root platform authority. |
| G00-P06 | Cognitive Semantic System remains the accepted name; final substrate remains deferred. |
| G00-P07 | Graph remains candidate only. |
| G00-P08 | Graphify remains evidence only, not authority. |
| G00-P09 | Hermes remains evidence and possible future adapter candidate only. |
| G00-P10 | Every active capability must be least-privilege, auditable, reversible, and explicitly approved. |

## 8. Roadmap FASE 7-17
The roadmap below is a direction sequence. G-00 does not authorize any listed phase to start.

| Phase | Direction | Required future gate | Explicitly not authorized by G-00 |
| --- | --- | --- | --- |
| FASE 7 | Governance activation charter. | Define owners, activation ladder, exact artifacts, stop rules, and decision authority. | Runtime, source inspection, implementation. |
| FASE 8 | Source and project classification. | Classify existing `3_platform` siblings and any proposed platform work by exact scope. | Broad inspection or approval of sibling contents. |
| FASE 9 | Validation execution gate design. | Decide how metadata validation can become controlled validation execution. | Tests, CI, scans, or validation execution. |
| FASE 10 | Security enforcement gate design. | Decide how access metadata can become enforceable policy runtime. | Secret scanning, credential access, runtime enforcement. |
| FASE 11 | Dependency and package posture. | Review exact root dependencies, package managers, manifests, lock strategy, and rollback. | Dependency adoption or package installation. |
| FASE 12 | Cognitive Semantic System substrate decision process. | Run multi-candidate substrate evaluation and governance decision. | Final substrate selection by G-00. |
| FASE 13 | Runtime kernel readiness. | Define minimal scheduler/task/runtime architecture with no tools or providers by default. | Runtime service creation. |
| FASE 14 | Tool execution and provider activation gates. | Approve exact tools, provider adapters, API/MCP/network/auth boundaries, audit logs, and containment. | Tool/provider/API/MCP activation. |
| FASE 15 | Product integration gates for Siamese surfaces. | Decide product owner, scope, source posture, validation baseline, dependency posture, and generated-output controls. | Product activation or product source tracking. |
| FASE 16 | Observability, audit, retention, and rollback hardening. | Define retained evidence, logs, privacy, replay, incident response, and rollback. | Production operation. |
| FASE 17 | Active platform readiness audit. | Audit all prior gates before any live operation, publication, or broad source tracking. | Automatic launch, staging, commit, push, or publish. |

FASE 7 should be governance-only. Later phases must be created only by explicit instruction and must keep exact scope.

## 9. Activation Ladder
| Level | Name | Meaning | Current status |
| --- | --- | --- | --- |
| AL-0 | Architecture records | Direction, policy, readiness, and audit documents exist. | Achieved. |
| AL-1 | Metadata skeleton | Bounded in-memory/stdlib metadata components exist under governed skeleton. | Current ceiling after I-A. |
| AL-2 | Controlled classification | Existing source areas and proposed work are classified by exact path and sensitivity. | Future only. |
| AL-3 | Validation/security dry-run | Validation and security decisions are evaluated against metadata with retained evidence. | Future only. |
| AL-4 | Enforced local policy | Security and validation constrain approved local actions without providers or products. | Future only. |
| AL-5 | Minimal runtime candidate | A governed runtime can execute non-destructive approved task envelopes. | Future only. |
| AL-6 | Tool/provider candidate | Exact tools, adapters, APIs, or MCP endpoints can be activated under least privilege. | Future only. |
| AL-7 | Cognitive Semantic System active substrate | A selected substrate stores governed semantic state with provenance and validation boundaries. | Future only. |
| AL-8 | Product pilot | One Siamese product surface consumes governed platform capability under product gates. | Future only. |
| AL-9 | Operational active platform | Runtime, validation, security, products, providers, evidence, and rollback pass readiness audit. | Future only. |

G-00 leaves AGENT PLATFORM at AL-1. Promotion above AL-1 requires explicit governance decision, validation evidence, security review, exact artifacts, and rollback path.

## 10. Cognitive Semantic System Direction
Cognitive Semantic System is the accepted architecture name. It is the future semantic authority layer or concept inside AGENT PLATFORM, not the whole workspace and not a product-owned system.

The final substrate remains deferred. Candidate substrate classes may include graph, vector index, relational store, document index, ontology, event-sourced store, hybrid, memory-only, or another approach after evaluation. No candidate is selected by G-00.

Semantic records, claims, and relations remain metadata until future gates decide validation, truth, persistence, substrate, and runtime behavior. A semantic claim is not proof. A relation is not reasoning execution. A candidate substrate record is not adoption.

## 11. Graph And Graphify Posture
Graph remains a candidate only. Graph may later be evaluated for relationships, provenance, dependencies, entities, evidence links, or projections, but graph structure does not decide governance or truth.

Graphify remains evidence only, not authority. Graphify source is not inspected, adopted, migrated, executed, installed, or used as naming authority by G-00. Rejected strings such as `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth` may appear only as rejected, prohibited, or historical examples.

Any future graph or Graphify-derived idea must pass normalization, provenance review, license review, security review, dependency review, validation review, and governance before it can influence implementation.

## 12. Hermes Posture
Hermes / `hermes-agent` remains external architecture evidence only. Its current relevance is as high-risk evidence for agent lifecycle, self-improvement loops, package split, rollback needs, validation gates, and possible future adapter patterns.

Hermes is not adopted by G-00. Hermes source is not inspected by G-00. Hermes dependencies, package manifests, runtime behavior, self-improvement behavior, commands, tests, examples, provider configuration, and credentials remain blocked.

Future Hermes review may occur only through an exact external-source review ticket. The only allowed future posture from G-00 is evidence or adapter candidate; not authority, not runtime, not self-modification policy, and not dependency adoption.

## 13. External Architecture Posture
External sources remain controlled evidence. W-03 and W-13 classify them as local-only, not promoted, execution-blocked, dependency-blocked, and instruction-blocked.

External architecture may inform future internal patterns only when restated under AGENT PLATFORM governance. Source code copy, dependency adoption, execution, provider authentication, external instructions, MCP activation, and product incorporation require separate exact approval.

No external source may become the root platform model by reputation, proximity, usefulness, or naming convenience.

## 14. Product Direction For Siamese
Siamese is the product vision context: a living energy twin platform for buildings connecting energy models, real data, calibration, prediction, recommendation/control, and continuous operation.

Products remain inactive. Product source remains local-only. `omniverse-app`, `backend-energyplus`, `cli`, `desktop`, `web-platform`, and `experimental` remain candidate, deferred, inactive, or blocked according to product governance. EnergyPlus remains solver, not internal model. Omniverse Kit remains interface, not backend.

Product needs can inform future platform requirements only through governance records. Product needs cannot decide root platform authority, final Cognitive Semantic System substrate, source tracking, dependency adoption, provider activation, or runtime activation.

## 15. No-loose-projects Rule
AGENT PLATFORM must not accumulate loose projects. A loose project is any platform, product, tool, source tree, experiment, external clone, runtime service, agent, provider adapter, MCP surface, dataset, model, artifact, or generated output that is used as if it were approved without a governance record.

Future work must have all of these before promotion or activation:

| Required field | Meaning |
| --- | --- |
| Owner | Human or governance owner for lifecycle and exceptions. |
| Exact path | Bounded location and explicit include/exclude list. |
| Scope | Purpose, non-goals, and authority boundary. |
| Source posture | Internal, product, external, generated, local-only, sensitive, or unknown. |
| Git posture | Trackable, local-only, ignored, exact-path review, or blocked. |
| Dependency posture | None, candidate, reviewed, adopted, rejected, or blocked. |
| Validation posture | Evidence, proof level, limitations, and revalidation trigger. |
| Security posture | Access, secrets, credentials, network, local-only, generated output, and exposure rules. |
| Activation posture | Inactive, candidate, approved for exact activation, or blocked. |
| Rollback | Removal, quarantine, deactivation, or restore path. |
| Stop rule | Condition that halts work before unsafe expansion. |

If any field is missing, the work remains evidence or candidate material only.

## 16. Git And Source Tracking Direction
G-00 does not stage, commit, push, publish, force-add, or modify `.gitignore`. Broad staging remains blocked. `git add .` remains prohibited.

Only exact governance documents may be considered for future exact-path review after human approval. Product source, external sources, previous knowledge corpus, generated outputs, datasets, models, artifacts, secrets, credentials, provider auth, dependency folders, runtime caches, and unknown local-only material remain not trackable by default.

Existing `3_platform` siblings remain uninspected and unapproved. The governed skeleton subroot does not approve sibling content.

## 17. Validation And Security Direction
Validation may support future gates by evaluating evidence, proof levels, coherence, and readiness. Validation never approves activation by itself.

Security constrains local-only material, secrets, credentials, execution, filesystems, shell, subprocess, network, providers, MCP, products, publication, and generated outputs. Security metadata is not runtime enforcement until a future governance gate authorizes enforcement design and activation.

Future validation or security execution must name exact commands, paths, data exposure, side effects, retention, rollback, and approval scope.

## 18. Blocker Register
| Blocker | Stop behavior | Future route |
| --- | --- | --- |
| Need to activate runtime | Stop. | Runtime readiness gate. |
| Need to inspect existing `3_platform` siblings | Stop. | Source classification gate. |
| Need final Cognitive Semantic System substrate | Stop. | Substrate decision process. |
| Need graph/vector/database/ontology runtime | Stop. | Substrate and dependency gates. |
| Need Graphify adoption | Stop. | Normalization and external-source governance. |
| Need Hermes adoption or inspection | Stop. | External-source review ticket. |
| Need dependency/package manifest/lockfile | Stop. | Dependency posture gate. |
| Need validation/security execution | Stop. | Validation/security execution gates. |
| Need provider/API/MCP/network/auth | Stop. | Provider activation gate. |
| Need tool/shell/subprocess/filesystem execution | Stop. | Tool execution gate. |
| Need product activation or source tracking | Stop. | Product governance gate. |
| Need Git staging, commit, push, publication, or force-add | Stop. | Explicit human Git approval. |

## 19. Incident Handling
Incidents include implementation expansion during G-00, runtime or tool activation, source inspection outside approved docs, product source inspection, external source inspection, Hermes or Graphify source inspection, dependency adoption, package manifest or lockfile creation, validation/security execution, provider/API/MCP/network/auth activation, credential inspection, final substrate selection, product activation, broad source tracking, `.gitignore` modification, staging, commit, push, publish, or starting G-01.

Response: stop, preserve safe metadata only, report the incident, and require human/governance/security decision before continuing.

## 20. Next Ticket Recommendation
Recommended next ticket: G-01 - Activation Gate Charter.

G-01 should be governance-only and should define the exact gate model for FASE 7, activation ladder promotion criteria, owner fields, artifact fields, source classification intake, validation/security evidence requirements, rollback requirements, stop rules, and allowed validation commands.

G-01 should not implement runtime, inspect `3_platform` siblings, inspect product source, inspect external source, inspect Hermes, inspect Graphify, adopt dependencies, create package manifests, run tools/tests/builds, activate providers/API/MCP, select the Cognitive Semantic System substrate, stage, commit, push, or publish.

G-01 is recommended only after explicit instruction. G-00 does not start it.

## 21. G-00 Invariants
| ID | Invariant |
| --- | --- |
| G00-001 | G-00 is a governance direction decision only. |
| G00-002 | AGENT PLATFORM remains pre-active after G-00. |
| G00-003 | Current activation ceiling remains AL-1 metadata skeleton. |
| G00-004 | Existing `3_platform` siblings remain uninspected and unapproved. |
| G00-005 | No runtime, tool, agent, provider, API, MCP, product, graph, vector, database, ontology, or persistence is activated. |
| G00-006 | Cognitive Semantic System remains the accepted name. |
| G00-007 | Final Cognitive Semantic System substrate remains deferred. |
| G00-008 | Graph remains candidate only. |
| G00-009 | Graphify remains evidence only, not authority. |
| G00-010 | Hermes remains external evidence or adapter candidate only. |
| G00-011 | Product source remains local-only. |
| G00-012 | External sources remain local-only evidence. |
| G00-013 | Dependencies remain unadopted. |
| G00-014 | Validation evaluates; governance decides. |
| G00-015 | No Git mutation or publication is authorized. |
| G00-016 | G-00 stops before G-01. |

## 22. Final Verdict
G-00 accepts the direction that AGENT PLATFORM should become an active governed agent platform for the Siamese living energy twin vision through a staged activation ladder and roadmap from FASE 7 through FASE 17.

G-00 does not activate the platform. It does not expand implementation. It does not inspect or approve existing `3_platform` siblings. It does not activate products. It does not adopt dependencies. It does not activate providers, adapters, APIs, MCP, agents, tools, runtime, graph, vector, database, ontology, persistence, validation execution, or security enforcement. It does not select the final Cognitive Semantic System substrate. It does not adopt Graphify. It does not adopt Hermes. It does not stage, commit, push, publish, force-add, or modify `.gitignore`.

After G-00, the platform remains at AL-1 metadata skeleton, with direction approved for future governance-only activation planning. G-01 - Activation Gate Charter is recommended after explicit instruction only.
