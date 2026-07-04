# P2.K3 - Harness-Agnostic Routing / Memory Manifest Strategy

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Harness-Agnostic Routing / Memory Manifest Strategy |
| Ticket | P2.K3 |
| Status | Accepted strategy baseline with pending optional alignment |
| Date | 2026-07-04 |
| Scope | Define a documentation-only, harness-agnostic routing and memory manifest strategy for future AGENT PLATFORM / Siamese harness projections without creating runtime routing, memory ingestion, harness configuration, or persistent memory artifacts. |
| Authority | Strategy and governance alignment only, not routing implementation, memory system implementation, projection generation, agent execution, tool execution, provider/auth activation, source loading, source tracking approval, generated output tracking approval, product activation, Graphify adoption, publication, Git mutation, live connector activation, or Cognitive Semantic System substrate selection. |
| Related documents | P2.R Cross-Lane Integration Reconciliation Closure, P2.1 Shared Metadata Vocabulary Alignment, P2.2 Cross-Lane Evidence Reference Contract, P2.3 Audit / Retention / Rollback Baseline, P1.1-P1.5, P0.1-P0.3, G-19, G-01 Activation Gate Charter, Graphify Repo Map Summary, S-03, S-04, Cognitive Semantic System ADR/audit, `.gitignore`, `.graphifyignore`, README.md. |
| Optional dependency posture | P2.K1 absent, P2.K2 absent, P2.K4 absent during P2.K3 posture checks. |
| Output | Harness-agnostic routing / memory manifest strategy document only. |

This document is the canonical P2.K3 strategy record for harness-agnostic routing and memory manifest planning. It defines a future-facing metadata contract only.

## 2. Purpose
P2.K3 defines how future harness-facing context, routing, and memory instructions should be derived from a single governed manifest instead of being authored separately in harness-specific files.

The purpose is to prevent Codex, OpenCode, Claude, Hermes, or future harnesses from becoming competing sources of authority. The canonical memory manifest is the authority candidate for future derived projections. Harness-specific projections are derived views, not source-of-truth records.

P2.K3 prepares later alignment work for P2.KR, P3.0, P3.1, and P3.2 without starting any of those tickets.

P2.K3 does not implement routing code.

P2.K3 does not implement a memory system.

P2.K3 does not create memory ingestion.

P2.K3 does not create a projection generator.

P2.K3 does not create vector storage, graph storage, embeddings, databases, or persistence.

P2.K3 does not create or modify AGENTS.md.

P2.K3 does not create or modify CLAUDE.md.

P2.K3 does not create or modify OpenCode, Codex, Claude, Hermes, MCP, agent, tool, plugin, or provider configuration.

AGENT PLATFORM remains pre-active at AL-1 metadata skeleton.

## 3. Current Posture
| Area | Current posture | P2.K3 strategy result |
| --- | --- | --- |
| Activation level | AGENT PLATFORM remains pre-active at AL-1 metadata skeleton. | No promotion. |
| P2 baseline | P2.R reconciled P2.1, P2.2, and P2.3. | P2.K3 consumes the reconciled vocabulary, evidence, audit, retention, rollback, and incident posture. |
| Context | Context inclusion is not permission. | Routing inputs must preserve source refs, blockers, sensitivity, and limitations. |
| Providers | Provider metadata is not provider activation. | Routing cannot imply provider/auth/API/MCP availability. |
| Tools | Tool metadata is not tool execution. | Routing cannot approve shell, subprocess, filesystem, network, package, build, test, CI, Git, MCP, or tool execution. |
| Agents | Agent metadata is not agent execution. | Routing cannot approve task execution, handoff execution, orchestration, scheduler, or autonomous loop behavior. |
| Cognitive Semantic System | Name accepted; substrate deferred. | Memory manifest strategy remains substrate-neutral. |
| Graphify | Curated generated evidence only. | Graphify may be cited as supporting evidence only, not authority or substrate. |
| Product | Siamese is product vision, not product activation. | Product source remains blocked until GT-09. |
| Audit / retention / rollback | P2.3 defines metadata baseline only. | Manifest records retention and incident posture but does not create runtime logging or persistence. |
| Git / publication | Exact human approval required. | P2.K3 does not stage, commit, push, force-add, publish, or approve source tracking expansion. |

Evidence supports; it does not decide.

Validation evaluates; governance decides.

Security constrains; it does not activate.

## 4. P2.K1 / P2.K2 / P2.K4 Dependency Posture
P2.K3 checked for optional dependency documents before writing this strategy.

| Optional dependency | Expected path | Posture during P2.K3 | Alignment marker | P2.K3 handling |
| --- | --- | --- | --- | --- |
| P2.K1 - Four Cs / Five Levels Mapping | `0_architecture/governance/agent_platform_four_cs_five_levels_mapping.md` | Absent. | `pending_P2.K1_alignment` | Do not infer final context/routing level taxonomy. Carry forward pending marker. |
| P2.K2 - Hybrid Retrieval Mode Decision Matrix | `0_architecture/governance/agent_platform_hybrid_retrieval_mode_decision_matrix.md` | Absent. | `pending_P2.K2_alignment` | Do not select retrieval mode, vector mode, graph mode, hybrid mode, or ranking strategy. Carry forward pending marker. |
| P2.K4 - Live Connections / Cadence Boundary Strategy | `0_architecture/governance/agent_platform_live_connections_cadence_boundary_strategy.md` | Absent. | `pending_P2.K4_alignment` | Do not activate live connectors, watch mode, refresh cadence, background sync, or always-on behavior. Carry forward pending marker. |

P2.K3 does not create, modify, supersede, or start P2.K1, P2.K2, or P2.K4.

P2.K3 may name the pending markers so later P2.KR can reconcile them.

## 5. Harness-Agnostic Strategy Definition
A harness-agnostic routing / memory manifest strategy is a governance metadata strategy that defines how future harness-specific routing instructions, memory inclusion rules, context selection hints, and projection files should be derived from a single canonical memory manifest without making any harness-specific file authoritative.

| Clarification | Rule |
| --- | --- |
| Harness means a compatible agent execution or assistant environment. | Examples include Codex, OpenCode, Claude, Hermes, and future compatible systems. |
| The canonical memory manifest is the future shared source for projection metadata. | It records governed memory/routing intent, blockers, sensitivity, and projection eligibility. |
| harness-specific projections are derived views. | Derived projections cannot override the canonical manifest, governance gates, security refs, validation refs, or audit refs. |
| Routing means metadata routing strategy. | P2.K3 does not implement routers, dispatchers, selectors, schedulers, queues, agents, tools, or runtime behavior. |
| Memory means governed context/memory metadata. | P2.K3 does not implement permanent memory ingestion, vector DB, graph DB, embeddings, indexers, GBrain, Hermes, Cadence, or persistence. |
| Projection means a future generated view. | P2.K3 does not generate AGENTS.md, CLAUDE.md, OpenCode config, Codex config, Hermes config, MCP config, wiki, MOC, memory.md, or decisions.md. |
| Context inclusion remains non-permission. | Any future memory entry still carries source classification, sensitivity, blockers, limitations, and review requirements. |
| Evidence remains support only. | Evidence refs cannot become authority by projection. |
| Security remains constraining. | Security refs block or constrain projection and routing eligibility. |
| Validation remains evaluative. | Validation refs may later check completeness but cannot approve activation or publication. |

## 6. Decision Model
The future decision stack must preserve authority order.

| Decision layer | Current P2.K3 status | Future role | Blocked inference |
| --- | --- | --- | --- |
| Governance records | Existing docs are accepted metadata. | Decide canonical terms, manifest scope, projection scope, and exceptions. | Harness files deciding authority. |
| Canonical memory manifest | Strategy only; not created. | Future exact manifest may become the governed source for routing and memory projection metadata. | Runtime memory store or persistent truth. |
| Evidence refs | P2.2 contract exists. | Support manifest entries with source, validation, security, Graphify, product, and audit refs. | Evidence deciding routing. |
| Security refs | S-03/S-04 and P0.3 constrain scope. | Block forbidden content, provider/auth, tools, products, source tracking, publication, and unknown sensitivity. | Security refs granting permission. |
| Validation refs | P0.2 and P2.1/P2.2 define posture. | Future validation may check manifest completeness and projection consistency. | Validation approval as activation. |
| Audit / retention / rollback refs | P2.3 baseline exists. | Preserve retention, redaction, quarantine, publication blocker, source tracking blocker, rollback, and incident posture. | Runtime logging, persistence, or rollback automation. |
| Harness-specific projections | Not created. | Future generated views for Codex, OpenCode, Claude, Hermes, or compatible systems. | Projection as authority. |
| Runtime harness behavior | Not active. | Future gate-bound execution environment only if approved. | Availability as permission. |

Future decision rule: if a harness projection conflicts with the canonical memory manifest, P2.1 vocabulary, P2.2 evidence contract, P2.3 retention baseline, S-03/S-04, G-01, or P0 gates, the stricter governance/security/blocker interpretation controls.

## 7. Canonical Memory Manifest Contract
The canonical memory manifest is not created by P2.K3. This section defines the future contract for such a manifest.

Required future fields:

```text
manifest_id
manifest_title
manifest_version
manifest_status
manifest_owner
manifest_scope
activation_status
source_refs
context_refs
validation_refs
security_refs
audit_refs
retention_refs
rollback_refs
incident_refs
projection_targets
harness_scope
memory_entry_refs
routing_policy_refs
source_classification
sensitivity
local_only
generated_output_posture
product_posture
provider_auth_posture
execution_status
tracking_posture
retention_posture
publication_posture
substrate_posture
blockers
limitations
review_required
pending_alignment_refs
created_or_reviewed_date
```

| Field group | Meaning | P2.K3 posture | Forbidden content |
| --- | --- | --- | --- |
| Identity | Stable manifest identity, owner, version, status, and exact scope. | Strategy only. | Runtime handles, executable config, hidden state. |
| Source refs | Metadata-only source references. | Must preserve P2.1 and P2.2 naming. | Raw source content, product source, external raw source, local-only dumps. |
| Evidence refs | Supporting evidence references. | Evidence supports; it does not decide. | Raw Graphify output, provider output, tool output payloads, secrets. |
| Validation refs | Validation posture references. | Validation evaluates; governance decides. | Unapproved command output as authority. |
| Security refs | Security constraints and blockers. | Security constrains; it does not activate. | Secret values, credential values, auth material. |
| Audit / retention / rollback refs | P2.3 metadata posture. | No runtime logging, persistence, or rollback automation. | Logs, storage handles, destructive commands, credential rotation commands. |
| Projection targets | Future intended derived views. | Projection eligibility only. | Generated AGENTS.md, CLAUDE.md, harness config, MCP config, or live connector config. |
| Harness scope | Harness classes eligible for future projection. | Harness-agnostic metadata only. | Harness activation, tool execution, provider calls, always-on behavior. |
| Memory entries | Governed memory metadata refs. | No permanent memory ingestion. | Secret/credential content, product source, raw local-only content. |
| Routing policy refs | Strategy refs and blockers. | No routing code. | Dispatch code, selectors, scheduler config, agent runtime config. |

The canonical memory manifest must carry `pending_P2.K1_alignment`, `pending_P2.K2_alignment`, and `pending_P2.K4_alignment` until those optional dependencies exist and P2.KR or a later exact ticket reconciles them.

## 8. Memory Entry Contract
Future memory entries must be safe metadata records, not durable content ingestion by default.

| Future field | Required meaning | Blocked interpretation |
| --- | --- | --- |
| `memory_entry_id` | Stable metadata ID. | Database primary key or persistent store implementation. |
| `memory_entry_kind` | Governance, policy, context, provider, tool, agent, semantic, product-readiness, Graphify, audit, incident, or unknown. | Permission to read or execute source. |
| `memory_entry_scope` | Exact bounded scope. | Broad workspace memory. |
| `source_refs` | Source metadata refs only. | Raw source loading. |
| `evidence_refs` | Evidence metadata refs only. | Evidence as authority. |
| `security_refs` | Security blockers and constraints. | Security permission. |
| `validation_refs` | Validation posture. | Validation execution. |
| `retention_posture` | Metadata-only, local-only, generated-sensitive, quarantine, deletion review, publication blocked, or unknown. | Persistence approval. |
| `projection_eligibility` | Whether a future projection may include safe metadata. | Immediate generation. |
| `harness_projection_notes` | Harness-neutral notes for future adapters. | Harness-specific authority. |
| `blockers` | P2.1 canonical blockers. | Bypass instructions. |
| `limitations` | Known gaps and restricted-use statements. | Erased uncertainty. |
| `review_required` | Governance/security/validation/audit review needs. | Approval. |

Memory entries must not contain secret values, credential values, API keys, tokens, passwords, private keys, browser auth, provider configs, `.env` contents, raw local-only source, raw product source, raw external source, raw generated Graphify output, provider output payloads, tool execution outputs, or agent execution outputs.

## 9. Routing Metadata Contract
Future routing metadata may describe intended routing outcomes but cannot route anything by itself.

| Future object | Meaning | Required fields | P2.K3 boundary |
| --- | --- | --- | --- |
| RoutingIntent | Metadata statement that a memory/context category may be useful for a future target. | `routing_intent_id`, `target_scope`, `source_refs`, `evidence_refs`, `security_refs`, `validation_refs`, `blockers`, `limitations`, `review_required`. | No execution or selection runtime. |
| RoutingPolicyRef | Metadata ref to governed routing rules. | `routing_policy_ref_id`, `policy_scope`, `allowed_metadata_use`, `forbidden_use`, `required_gates`, `blockers`. | No parser, dispatcher, selector, or code. |
| ProjectionEligibilityRecord | Metadata record deciding whether a safe entry can be included in a future projection. | `projection_eligibility_id`, `manifest_ref`, `harness_scope`, `entry_refs`, `sensitivity`, `retention_posture`, `blockers`, `limitations`. | No projection generated. |
| HarnessProjectionSpec | Future spec for a derived view. | `projection_spec_id`, `harness_family`, `target_surface`, `included_entry_refs`, `excluded_entry_refs`, `source_classification`, `review_required`. | Not AGENTS.md, not CLAUDE.md, not config. |
| RoutingDecisionRecord | Governance metadata for accepting, blocking, or deferring a routing/projection decision. | `decision_id`, `decision_scope`, `decision_status`, `decision_authority`, `evidence_refs`, `security_refs`, `validation_refs`, `audit_refs`, `blockers`, `limitations`. | Decision metadata only. |

Routing metadata cannot approve source loading, provider-bound transmission, tool execution, agent execution, product activation, publication, source tracking, generated output tracking, or Cognitive Semantic System substrate selection.

## 10. Harness-Specific Projection Contract
Future harness-specific projections are derived views.

The exact governing phrase is: harness-specific projections are derived views.

| Harness family | Future possible projection surface | Current P2.K3 status | Required future gate / review | Blocked current action |
| --- | --- | --- | --- | --- |
| Codex-compatible | `AGENTS.md` or equivalent if later approved. | Not created, not modified. | Exact projection ticket, security review, validation review, source tracking review, publication/Git gate if tracked. | P2.K3 does not create or modify AGENTS.md. |
| Claude-compatible | `CLAUDE.md` or equivalent if later approved. | Not created, not modified. | Exact projection ticket, security review, validation review, source tracking review, publication/Git gate if tracked. | P2.K3 does not create or modify CLAUDE.md. |
| OpenCode-compatible | `.opencode/`, opencode config, agents, skills, plugins, permissions if later approved. | Not created, not modified. | Exact OpenCode projection/config ticket and customize-opencode-scope review if applicable. | No `.opencode/` or OpenCode config modified. |
| Hermes-compatible | Hermes projection or adapter view if later approved. | Not created, not modified. | External/harness gate, source boundary, security, validation, provider/auth review if applicable. | Hermes source not inspected and Hermes not adopted. |
| MCP-compatible | MCP server/resource/tool projection if later approved. | Not created, not modified. | GT-08 plus GT-07/security review. | No MCP activation or config. |
| Future harness | Derived projection format to be defined later. | Not created. | Governance, security, validation, audit, rollback, source tracking review. | No harness activation. |

Derived projections must be regenerated from the canonical memory manifest if a future generator exists. P2.K3 does not build that generator.

Derived projections must include source classification, sensitivity, blockers, limitations, review requirements, and stop rules. They must not include secret values, credential values, raw local-only content, raw product source, raw external source, raw generated outputs, provider output payloads, tool execution outputs, or agent execution outputs.

## 11. Source Eligibility And Exclusion Model
| Source class | Eligible for future manifest metadata? | Eligible for future projection content? | Required posture |
| --- | --- | --- | --- |
| Governance metadata | Yes, when ticket-scoped. | Safe metadata and citations only. | Preserve non-activation language. |
| Security policy metadata | Yes, when ticket-scoped. | Safe constraints and stop rules only. | Security constrains; it does not activate. |
| Validation metadata | Yes, when ticket-scoped. | Validation posture only. | Validation evaluates; governance decides. |
| Context metadata | Yes, when safe. | Context refs and safe summaries only. | Context inclusion is not permission. |
| Provider metadata | Yes, when safe. | Provider blockers and metadata only. | Provider metadata is not provider activation. |
| Tool metadata | Yes, when safe. | Tool blockers and metadata only. | Tool metadata is not tool execution. |
| Agent metadata | Yes, when safe. | Agent/task/handoff blockers and metadata only. | Agent metadata is not agent execution. |
| Semantic metadata | Yes, when safe. | Semantic refs and substrate-neutral metadata only. | Cognitive Semantic System substrate remains deferred. |
| Graphify curated summary | Yes, as supporting generated evidence. | Only curated evidence posture and limitations. | Graphify evidence is supporting generated evidence only, not authority. |
| Raw Graphify output | Blocked marker only. | No. | Raw generated output remains local-only. |
| Product source | Blocked marker only. | No. | GT-09 required. |
| External raw source | Blocked marker only. | No. | GT-11/security/license review required. |
| Local-only material | Safe metadata only if exact scope approves. | No by default. | S-03 local-only posture applies. |
| Secrets / credentials / provider auth | Safe blocked category only. | Never. | Stop and secure handling route. |
| Unknown sensitivity | Blocked marker only. | No. | Classify with safe metadata before use. |

## 12. Projection Inclusion Rules
| Rule | Required behavior |
| --- | --- |
| Canonical source | Future projections must be derived from the canonical memory manifest, not manually divergent harness files. |
| Stricter boundary wins | If any ref or policy conflicts, stricter blocker/security posture wins. |
| Sensitivity propagation | Highest sensitivity travels into manifest entries and projections. |
| Blocker propagation | Blockers from P2.1, P2.2, P2.3, S-03, S-04, P0 gates, and P1 lanes must travel downstream. |
| Limitation propagation | Limitations must travel with projected entries. |
| Local-only propagation | Local-only posture blocks publication, provider transmission, and default projection content. |
| Generated-output propagation | Generated outputs remain generated-sensitive/local-only unless future exact gates curate and approve. |
| Product posture propagation | Product source and product outputs remain blocked until GT-09. |
| Provider/auth propagation | Provider/auth requirements remain blockers until GT-08 and secure approval. |
| Tool execution propagation | Tool refs remain blockers until GT-07 and exact approval. |
| Agent execution propagation | Agent refs remain metadata until runtime and action gates approve. |
| Substrate propagation | Cognitive Semantic System substrate remains deferred; graph remains candidate only. |
| Audit propagation | Retention, rollback, publication blocker, source tracking blocker, quarantine, and incident posture must travel into projections. |
| Unknown sensitivity | Unknown sensitivity downgrades to blocked or needs review. |
| No manual override | Harness-specific files must not override canonical blockers. |

## 13. Cross-Lane Contracts
| Lane | P2.K3 contract |
| --- | --- |
| Context | Memory manifest entries may reference context metadata, but context inclusion is not permission and source refs remain metadata. |
| Provider | Manifest and projection records may reference provider metadata, but provider metadata is not provider activation and provider-bound context transmission remains blocked. |
| Tool | Manifest and projection records may reference tool metadata, but tool metadata is not tool execution and no command/action is approved. |
| Agent | Manifest and projection records may reference agent metadata, task records, and handoff records, but agent metadata is not agent execution. |
| Cognitive Semantic System | Manifest records may reference semantic metadata and substrate candidates, but semantic records are not truth by default and substrate remains deferred. |
| Evidence | Manifest entries must use EvidenceRef semantics; evidence supports but does not decide. |
| Validation | Future checks may evaluate manifest completeness and projection consistency; P2.K3 does not execute validation. |
| Security | Security refs constrain inclusion, projection, retention, publication, and provider/tool/agent boundaries. |
| Audit / retention / rollback | Manifest strategy must preserve P2.3 audit, retention, rollback, quarantine, publication blocker, source tracking blocker, and incident metadata. |
| Graphify | Graphify Repo Map Summary is curated generated evidence only. Raw Graphify output remains local-only. |
| Siamese product | Siamese is product vision, not product activation. Product source remains blocked until GT-09. |

## 14. Routing Tables
### 14.1 Harness Projection Routing Table
| Input category | Canonical manifest route | Future projection behavior | Current blocker |
| --- | --- | --- | --- |
| Governance rule | Manifest entry with governance refs. | May project safe rule text or citation after review. | Publication/source tracking review if persisted. |
| Stop rule | Manifest entry with security and governance refs. | May project stop behavior to harness-specific view. | Must preserve exact blockers. |
| Context summary | Manifest entry with context refs and sensitivity. | May project safe summary if not local-only/product/external/secret/credential. | Context permission blocker. |
| Provider need | Manifest entry with provider refs and auth blockers. | May project provider-blocked note only. | Provider/auth blocker. |
| Tool need | Manifest entry with tool refs and execution blockers. | May project tool-blocked note only. | Tool execution blocker. |
| Agent task | Manifest entry with agent refs and execution blockers. | May project metadata-only task boundary. | Agent execution blocker. |
| Semantic relation | Manifest entry with semantic refs and substrate posture. | May project substrate-neutral relation metadata. | Substrate selection blocker. |
| Graphify evidence | Manifest entry with GraphifyRef and limitations. | May project curated evidence caveat only. | Graphify authority/raw-output blockers. |
| Product readiness | Manifest entry with ProductRef and GT-09 blockers. | May project product-readiness caveat only. | Product activation/source blockers. |
| Incident route | Manifest entry with incident/audit refs. | May project safe incident stop route. | Incident automation blocked. |

### 14.2 Memory Inclusion Routing Table
| Memory class | Include in canonical memory manifest? | Include in future derived projection? | Required note |
| --- | --- | --- | --- |
| Governance metadata | Yes. | Yes, if safe and scoped. | Does not activate. |
| Policy stop rules | Yes. | Yes, if safe and scoped. | Security constrains. |
| Validation posture | Yes. | Yes, if safe and scoped. | Validation evaluates; governance decides. |
| Security posture | Yes. | Yes, if safe and scoped. | Security is not permission. |
| Context refs | Yes. | Maybe, safe refs only. | Context inclusion is not permission. |
| Provider refs | Yes. | Maybe, blocked metadata only. | Provider metadata is not activation. |
| Tool refs | Yes. | Maybe, blocked metadata only. | Tool metadata is not execution. |
| Agent refs | Yes. | Maybe, blocked metadata only. | Agent metadata is not execution. |
| Semantic refs | Yes. | Maybe, substrate-neutral only. | Not truth by default. |
| Graphify summary | Yes. | Maybe, curated caveat only. | Evidence only, not authority. |
| Raw generated output | Blocked marker only. | No. | Local-only/generated-sensitive. |
| Product source | Blocked marker only. | No. | GT-09 required. |
| External raw source | Blocked marker only. | No. | GT-11 required. |
| Secrets / credentials | Blocked safe category only. | Never. | Stop and secure handling. |

## 15. Drift Register
| drift_id | Drift area | Observed posture | P2.K3 decision | Pending marker | Future route |
| --- | --- | --- | --- | --- | --- |
| K3-DRIFT-001 | Harness files as authority | Harness ecosystems often use root instruction files. | Harness-specific files must be derived views, not authority. | none | Future projection ticket. |
| K3-DRIFT-002 | Memory manifest schema | No canonical memory manifest file exists. | Define future contract only; do not create manifest file. | none | P2.KR or later manifest ticket. |
| K3-DRIFT-003 | Four Cs / five levels mapping | Optional P2.K1 absent. | Do not define final level mapping. | `pending_P2.K1_alignment` | P2.K1 then P2.KR. |
| K3-DRIFT-004 | Retrieval mode | Optional P2.K2 absent. | Do not choose hybrid retrieval, vector, graph, lexical, or ranking mode. | `pending_P2.K2_alignment` | P2.K2 then P2.KR. |
| K3-DRIFT-005 | Live connection cadence | Optional P2.K4 absent. | Do not activate connectors, cadence, polling, sync, watch, or always-on behavior. | `pending_P2.K4_alignment` | P2.K4 then P2.KR. |
| K3-DRIFT-006 | Graphify evidence pressure | Graphify summary can suggest components and metadata patterns. | Keep Graphify supporting generated evidence only. | none | Graphify evidence gate if needed. |
| K3-DRIFT-007 | Product pressure | Siamese product vision can influence routing priorities. | Keep Siamese as product vision, not activation or root authority. | none | Product gate later. |
| K3-DRIFT-008 | Substrate pressure | Memory wording can imply persistence/substrate. | Keep manifest substrate-neutral and metadata-only. | none | GT-10/GT-13 later. |
| K3-DRIFT-009 | Projection generation | Future generator may be tempting. | P2.K3 does not create generator or projection output. | none | Future exact implementation/readiness ticket. |
| K3-DRIFT-010 | Permanent memory ingestion | Memory manifest wording may imply ingestion. | P2.K3 blocks permanent memory ingestion. | none | Future memory/storage gate only. |

## 16. Strategy Invariants
| ID | Invariant |
| --- | --- |
| K3-001 | P2.K3 is documentation-only strategy. |
| K3-002 | P2.K3 does not implement routing code. |
| K3-003 | P2.K3 does not implement a memory system. |
| K3-004 | P2.K3 does not create permanent memory ingestion. |
| K3-005 | P2.K3 does not create a parser, projection generator, vector DB, embeddings, graph DB, graph persistence, GBrain, Hermes, Cadence, or live connector. |
| K3-006 | The canonical memory manifest is the future shared authority candidate for projection metadata. |
| K3-007 | harness-specific projections are derived views, not authority. |
| K3-008 | P2.K3 does not create or modify AGENTS.md. |
| K3-009 | P2.K3 does not create or modify CLAUDE.md. |
| K3-010 | P2.K3 does not create or modify OpenCode, Codex, Claude, Hermes, MCP, provider, agent, tool, plugin, skill, or permission configuration. |
| K3-011 | Context inclusion is not permission. |
| K3-012 | Provider metadata is not provider activation. |
| K3-013 | Tool metadata is not tool execution. |
| K3-014 | Agent metadata is not agent execution. |
| K3-015 | Evidence supports; it does not decide. |
| K3-016 | Validation evaluates; governance decides. |
| K3-017 | Security constrains; it does not activate. |
| K3-018 | Graphify evidence is supporting generated evidence only, not authority. |
| K3-019 | Cognitive Semantic System substrate remains deferred. |
| K3-020 | AGENT PLATFORM remains pre-active at AL-1. |
| K3-021 | `pending_P2.K1_alignment` remains open. |
| K3-022 | `pending_P2.K2_alignment` remains open. |
| K3-023 | `pending_P2.K4_alignment` remains open. |
| K3-024 | P2.K3 does not start P2.KR, P3.0, P3.1, or P3.2. |

## 17. Future Validation Targets
These are future validation targets only. P2.K3 does not execute validation.

| Future validation target | Purpose | Required future gate |
| --- | --- | --- |
| Memory manifest required fields completeness | Check future canonical manifest fields. | GT-04 |
| Memory entry required fields completeness | Check future memory entry metadata. | GT-04 |
| Routing metadata required fields completeness | Check RoutingIntent, RoutingPolicyRef, ProjectionEligibilityRecord, HarnessProjectionSpec, and RoutingDecisionRecord. | GT-04 |
| Harness projection derived-view invariant | Check projections state they are derived views. | GT-04 plus source tracking review if files exist. |
| No harness-specific authority invariant | Check AGENTS.md, CLAUDE.md, OpenCode/Codex/Hermes/MCP projections do not override manifest authority. | GT-04 plus GT-12 if tracked. |
| No secret/no credential projection invariant | Check projections exclude forbidden content without scanning values. | GT-04 plus GT-05. |
| Context inclusion non-permission invariant | Check context refs do not grant source loading. | GT-04. |
| Provider/auth blocker propagation | Check provider/auth blockers travel into manifest and projections. | GT-04 plus GT-08 if activation requested. |
| Tool execution blocker propagation | Check tool blockers travel into manifest and projections. | GT-04 plus GT-07 if execution requested. |
| Agent execution blocker propagation | Check agent blockers travel into manifest and projections. | GT-04 plus GT-06 if runtime requested. |
| Generated output local-only invariant | Check raw generated output remains blocked. | GT-04 plus GT-12/GT-15 if tracking requested. |
| Graphify support-only invariant | Check Graphify evidence remains supporting evidence only. | GT-04/GT-11. |
| Substrate deferral invariant | Check memory wording does not select substrate or persistence. | GT-04 plus GT-10/GT-13 if substrate/state requested. |
| P2.K1 alignment check | Reconcile Four Cs / five levels mapping when P2.K1 exists. | Future P2.K1/P2.KR. |
| P2.K2 alignment check | Reconcile retrieval mode choices when P2.K2 exists. | Future P2.K2/P2.KR. |
| P2.K4 alignment check | Reconcile live connection/cadence boundaries when P2.K4 exists. | Future P2.K4/P2.KR. |

## 18. Future Hardening Candidates
These are future candidates only and are not started by P2.K3.

| Candidate ticket | Purpose | P2.K3 status |
| --- | --- | --- |
| K3-HARD-01 - Canonical Memory Manifest Schema | Define an exact schema for the canonical memory manifest. | Not started. |
| K3-HARD-02 - Harness Projection Eligibility Contract | Define exact rules for future derived projections. | Not started. |
| K3-HARD-03 - Harness Projection Generator Readiness | Evaluate whether a generator is needed after gates. | Not started. |
| K3-HARD-04 - No-Harness-Authority Validation Plan | Plan checks that harness files remain derived views. | Not started. |
| K3-HARD-05 - Memory Entry Sensitivity Propagation Model | Expand sensitivity/blocker propagation for memory entries. | Not started. |
| K3-HARD-06 - Routing Metadata Boundary Contract | Refine routing metadata without code. | Not started. |
| K3-HARD-07 - P2.KR Reconciliation Input | Feed unresolved P2.K1/P2.K2/P2.K4 markers into P2.KR. | Not started. |

## 19. Created / Not Created Register
| Artifact or action | P2.K3 status |
| --- | --- |
| Harness-agnostic routing / memory manifest strategy document | Created. |
| `0_architecture/governance/agent_platform_harness_agnostic_routing_memory_manifest_strategy.md` | Created. |
| Canonical memory manifest file | Not created. |
| Memory manifest schema file | Not created. |
| Memory ingestion | Not created. |
| Memory system | Not implemented. |
| Routing code | Not implemented. |
| Parser | Not created. |
| Projection generator | Not created. |
| Harness-specific projections | Not created. |
| `AGENTS.md` | Not created or modified. |
| `CLAUDE.md` | Not created or modified. |
| OpenCode config or `.opencode/` | Not created or modified. |
| Codex config | Not created or modified. |
| Claude config | Not created or modified. |
| Hermes config/source | Not created, modified, adopted, or inspected. |
| MCP server/resource/tool config | Not created or activated. |
| `.agents/`, `.claude/`, `.codex/` | Not created or modified. |
| `memory.md`, `decisions.md`, wiki/MOC files | Not created or modified. |
| Runtime code | Not modified. |
| Context runtime code | Not modified. |
| Provider adapter code | Not modified. |
| Tool execution code | Not modified. |
| Agent runtime code | Not modified. |
| Cognitive Semantic System runtime/code | Not modified. |
| GBrain, Hermes, Cadence, live connector, always-on behavior | Not created or activated. |
| Vector DB, graph DB, embeddings, graph persistence, database, ontology runtime, persistence | Not created or selected. |
| Validation execution | Not executed. |
| Tests/builds/package managers | Not run. |
| Provider/auth/API/network/MCP call | Not executed. |
| Tool execution | Not approved or executed. |
| Agent execution | Not approved or executed. |
| Source loading | Not approved. |
| Product source | Not inspected. |
| External raw source | Not inspected. |
| Secrets / credentials / `.env` | Not inspected. |
| Graphify | Not run or rerun. |
| `/graphify` | Not run. |
| Raw generated Graphify output | Not inspected. |
| Generated outputs | Not modified or tracked. |
| `.gitignore` | Not modified. |
| `.graphifyignore` | Not modified. |
| Source tracking expansion | Not approved. |
| Generated output tracking | Not approved. |
| Publication | Not approved. |
| Cognitive Semantic System substrate | Not selected. |
| Graph as substrate | Not selected. |
| P2.K1 | Not started. |
| P2.K2 | Not started. |
| P2.K4 | Not started. |
| P2.KR | Not started. |
| P3.0 | Not started. |
| P3.1 | Not started. |
| P3.2 | Not started. |
| Git staging/commit/push/force-add/publication | Not authorized or performed. |

## 20. Recommendations
| Ticket | Recommendation |
| --- | --- |
| P2.K1 - Four Cs / Five Levels Mapping | Complete before treating levels as canonical. |
| P2.K2 - Hybrid Retrieval Mode Decision Matrix | Complete before selecting retrieval/ranking/memory query mode. |
| P2.K4 - Live Connections / Cadence Boundary Strategy | Complete before live connectors, refresh cadence, watch mode, or always-on behavior. |
| P2.KR - K-Series Reconciliation | Reconcile P2.K1, P2.K2, P2.K3, and P2.K4 after explicit instruction and after missing optional docs exist or are intentionally deferred. |
| P3.0 | Do not start from P2.K3. Keep as future readiness only. |
| P3.1 | Do not start from P2.K3. Validation execution remains future-gated. |
| P3.2 | Do not start from P2.K3. Security enforcement remains future-gated. |

Recommended actual next ticket: P2.K1 - Four Cs / Five Levels Mapping, if the K-series is continuing in dependency order. If P2.K1 and P2.K2 are intentionally deferred, the next governance action should explicitly decide whether P2.KR may reconcile open markers without them.

Do not start P2.K1, P2.K2, P2.K4, P2.KR, P3.0, P3.1, or P3.2 from this document.

## 21. Final Verdict
| Question | Answer |
| --- | --- |
| What did P2.K3 create? | The Harness-Agnostic Routing / Memory Manifest Strategy document. |
| What is the central strategy? | Use a future canonical memory manifest as the governed source for memory/routing metadata and treat harness-specific projections as derived views. |
| Did P2.K3 create the canonical memory manifest file? | No. It defined the future contract only. |
| Did P2.K3 implement routing code? | No. P2.K3 does not implement routing code. |
| Did P2.K3 implement memory ingestion or persistence? | No. |
| Did P2.K3 create AGENTS.md? | No. P2.K3 does not create or modify AGENTS.md. |
| Did P2.K3 create CLAUDE.md? | No. P2.K3 does not create or modify CLAUDE.md. |
| Did P2.K3 create or modify harness config? | No. |
| Are harness-specific projections authoritative? | No. harness-specific projections are derived views. |
| Are P2.K1, P2.K2, and P2.K4 resolved? | No. `pending_P2.K1_alignment`, `pending_P2.K2_alignment`, and `pending_P2.K4_alignment` remain open. |
| Did P2.K3 activate runtime, providers, tools, agents, products, Graphify, or live connectors? | No. |
| Did P2.K3 select Cognitive Semantic System substrate? | No. Cognitive Semantic System substrate remains deferred. |
| Did P2.K3 start P2.KR, P3.0, P3.1, or P3.2? | No. |

Stop rule: After P2.K3, STOP. Do not implement code. Do not run validation. Do not run tests. Do not create harness projections. Do not create or modify AGENTS.md. Do not create or modify CLAUDE.md. Do not create or modify OpenCode/Codex/Claude/Hermes configuration. Do not create a canonical memory manifest file. Do not create memory.md, decisions.md, wiki, or MOC files. Do not activate providers/API/network/MCP. Do not execute tools. Do not activate agents. Do not inspect product source. Do not inspect secrets or credentials. Do not rerun Graphify. Do not inspect raw generated Graphify output. Do not modify generated outputs. Do not modify `.gitignore`. Do not modify `.graphifyignore`. Do not approve source tracking expansion. Do not approve generated output tracking. Do not select Cognitive Semantic System substrate. Do not start P2.K1, P2.K2, P2.K4, P2.KR, P3.0, P3.1, or P3.2. Do not stage, commit, push, force-add, or publish.
