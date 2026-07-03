# P0.1 - Activation Gate Enforcement Map

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Activation Gate Enforcement Map |
| Ticket | P0.1 |
| Status | Accepted governance control-plane map |
| Date | 2026-07-03 |
| Scope | Convert the G-01 activation gate charter and G-19 work-packet lane model into a practical documentation-only control-plane map for future AGENT PLATFORM / Siamese tickets. |
| Authority | Governance mapping only, not runtime enforcement, activation, source tracking approval, provider/auth approval, product activation, Graphify adoption, or Cognitive Semantic System substrate selection. |
| Related documents | G-00, G-01, G-18, G-19, I-A, I-01 through I-07, S-03, S-04, CSS-00, CSS-A, `.graphifyignore`, `.gitignore`, README.md. |

This document is the Activation Gate Enforcement Map for AGENT PLATFORM. Gate enforcement map is not runtime enforcement.

## 2. Purpose
P0.1 turns the activation gate charter into a usable control-plane reference for future tickets. It names which gate types block which activation moves, what evidence must exist before review, what stop rules apply, and which downstream lanes consume each gate.

P0.1 does not activate AGENT PLATFORM. AGENT PLATFORM remains pre-active at AL-1 metadata skeleton. Validation evaluates; governance decides.

## 3. Current Activation Posture
| Area | Current posture | P0.1 control-plane result |
| --- | --- | --- |
| Activation level | AL-1 metadata skeleton | No promotion. |
| Implementation | I-01 through I-07 metadata-only, in-memory, stdlib-only by contract | No code changes. |
| Validation | Metadata registry only | No validation execution. |
| Security | Metadata policy evaluator and policy docs only | No runtime enforcement. |
| Context | Metadata context runtime only | No source loading. |
| Providers/adapters | Metadata descriptors only | No provider/API/MCP activation. |
| Agents | Metadata boundary only | No agent, task, handoff, or orchestration execution. |
| Tools | Metadata boundary only | No tool, shell, subprocess, filesystem, network, package, build, test, or Git execution approval. |
| Cognitive Semantic System | Accepted name and metadata prototype | Cognitive Semantic System substrate remains deferred. |
| Products | Siamese vision only; product workspaces local-only/inactive | No product source inspection or activation. |
| Graphify | Supporting generated evidence only | Not authority, not source, not substrate. |
| Git/publication | Exact human approval required | No staging, commit, push, force-add, or publication. |

## 4. Non-Action Statement
This map is documentation and governance control-plane material only.

| Not performed by P0.1 | Reason |
| --- | --- |
| Runtime enforcement | Requires future enforcement gate and implementation approval. |
| Activation level promotion | Governance decision, evidence, security review, validation review, owner, and rollback are missing for every higher AL level. |
| Source tracking expansion | Requires GT-02 and exact human Git approval. |
| Existing `3_platform` sibling classification | Requires GT-01; siblings remain uninspected and unapproved. |
| Product source inspection or activation | Requires GT-09; product workspaces remain local-only. |
| Provider/auth/API/MCP activation | Requires GT-08 and secure approval. |
| Tool/shell/test/build/package execution | Requires GT-07 and exact command approval. |
| Cognitive Semantic System substrate selection | Requires GT-10 and future multi-candidate evidence. |
| Graphify adoption | Graphify remains supporting generated evidence only. |
| Git mutation or publication | Requires GT-12 and explicit human approval. |

## 5. Inputs Reviewed
| Input | Use in P0.1 |
| --- | --- |
| G-00 Active Platform Direction Decision | Current AL-1 ceiling, staged activation ladder, direction-only posture. |
| G-01 Activation Gate Charter | Gate types GT-01 through GT-15, gate record format, promotion matrix, stop rules. |
| G-19 Hybrid Parallel Work Packet Dependency Map | Parallel lanes L0 through L10 and WP-GOV-01 acceptance criteria. |
| G-18 Graphify Semantic Curation Gate | Graphify evidence-only boundary and code-only limitations. |
| Graphify Repo Map Summary | Supporting component-lane signals only. |
| I-A Implementation Audit | Bounded metadata implementation audit and residual blockers. |
| I-01 through I-07 implementation records | Component-specific metadata-only and non-activation boundaries. |
| S-03 Local-only / Secrets / Credentials Policy | Local-only, secrets, credentials, provider auth, artifact, and Git exposure rules. |
| S-04 Tool / Shell / Network / MCP Execution Policy | Execution risk levels, command approval, tool/network/auth/MCP/product blocks. |
| CSS-00 and CSS-A | Cognitive Semantic System naming accepted; substrate deferred. |
| `.graphifyignore` | Graphify input boundary: default-deny, governed skeleton Python only, exclusions retained. |
| `.gitignore` | Local-only and generated output hygiene posture. |
| README.md | Root workspace descriptor. |

## 6. Authority Model
| Layer | P0.1 authority |
| --- | --- |
| Governance | Decides promotion, deferral, rejection, exception, lifecycle, source tracking, product activation, provider activation, substrate decision, and publication. |
| Validation | Evaluates evidence, proof posture, limitations, blockers, and revalidation needs. Validation evaluates; governance decides. |
| Security | Constrains local-only material, secrets, credentials, execution, shell, filesystem, network, providers, MCP, products, generated outputs, and publication. |
| Product governance | Constrains Siamese/product workspaces, product dependencies, validation baselines, generated outputs, and root/product separation. |
| Cognitive Semantic System governance | Preserves accepted naming and substrate neutrality until a future substrate gate. |
| Git | Records artifacts after exact human approval only; Git does not approve authority. |
| Graphify | Supplies supporting generated evidence only; Graphify is not authority. |
| AI agents | May draft scoped metadata, but cannot be sole final approver or bypass gates. |

## 7. Activation Level Control Map
| From | To | Control-plane requirement | Current result |
| --- | --- | --- | --- |
| AL-1 | AL-2 Controlled classification | GT-01 Source Classification Gate, GT-02 as needed, GT-15 rollback/incident. | Blocked until exact paths, owner, sensitivity, and Git posture exist. |
| AL-2 | AL-3 Validation/security dry-run | GT-04 Validation Execution Gate, GT-05 dry-run posture, GT-15. | Blocked; P0.2 may design validation execution but cannot run it. |
| AL-3 | AL-4 Enforced local policy | GT-05 Security Enforcement Gate, GT-07 if tools involved, GT-15. | Blocked; P0.3 may design hardening but cannot enforce. |
| AL-4 | AL-5 Minimal runtime candidate | GT-06 Runtime Activation Gate, GT-13 if state, GT-15. | Blocked; no runtime lifecycle exists. |
| AL-5 | AL-6 Tool/provider candidate | GT-07, GT-08, GT-03, GT-15. | Blocked; tool/provider/auth/network/package risks unresolved. |
| AL-6 | AL-7 CSS active substrate | GT-10, GT-13, GT-05, GT-15. | Blocked; Cognitive Semantic System substrate remains deferred. |
| AL-7 | AL-8 Product pilot | GT-09, GT-14, GT-12 if Git/publication, GT-15. | Blocked; product source remains local-only/inactive. |
| AL-8 | AL-9 Operational active platform | All relevant gates plus readiness audit. | Blocked; operational audit and runtime evidence absent. |

No row is approved by this map. The map records gate dependencies only.

## 8. Gate Enforcement Matrix
| Gate | Controls | Required before review | Blocks by default | Downstream lanes |
| --- | --- | --- | --- | --- |
| GT-01 Source Classification Gate | Exact path/source/sensitivity classification | Owner, target paths, exclusions, source class, sensitivity, local-only posture, evidence refs | Existing `3_platform` reuse, product/external/raw source use, broad inspection | L0, L3, L10 |
| GT-02 Source Tracking Gate | Exact Git tracking posture | Exact paths, ignore/tracked state, sensitivity, owner, human approval route | Broad staging, force-add, generated/product/external/local-only tracking | L0, L9, L10 |
| GT-03 Dependency Adoption Gate | Packages, SDKs, solvers, external dependencies | Name, version, provenance, license, scripts, network/auth behavior, rollback | Package managers, manifests, lockfiles, SDK/client adoption | L4, L5, L10 |
| GT-04 Validation Execution Gate | Exact future validation execution | Proof target, command/path/data scope, retention, reviewer, limitations | Tests, CI, validation commands, broad evidence execution | L1 and all activation lanes |
| GT-05 Security Enforcement Gate | Security/access movement toward enforceable policy | Sensitivity model, local-only boundary, secret/credential handling, incident plan | Runtime enforcement, scanning, credential use, local-only leakage | L2 and all execution lanes |
| GT-06 Runtime Activation Gate | Scheduler, worker, queue, service, process lifecycle | Runtime owner, lifecycle, start/stop plan, logs, persistence, rollback | Runtime service, autonomous loop, daemon/process startup | L6, L8 |
| GT-07 Tool Execution Gate | Shell, filesystem, subprocess, package/build/test/Git/tool actions | Exact command/action, cwd, inputs/outputs, side effects, audit, rollback | Tool execution, shell/subprocess, package managers, tests/builds, Git mutation | L5, L6, L10 |
| GT-08 Provider / API / MCP Activation Gate | Providers, APIs, networks, MCP tools/resources | Provider identity, endpoint, data exposure, auth posture, credential-ref model, retention, cost, rollback | Provider calls, auth, network/API, MCP activation | L4, L5, L6, L10 |
| GT-09 Product Activation Gate | Siamese/product work | Product owner, source posture, dependencies, validation baseline, generated-output controls, rollback | Product source inspection, product execution, product Git posture, product-root collapse | L10 |
| GT-10 Cognitive Semantic System Substrate Gate | Final semantic substrate decision | Multi-candidate evidence, security/validation review, migration/export/rollback, decision record | Graph/vector/database/ontology/persistence substrate selection | L7 |
| GT-11 External Architecture Assimilation Gate | External pattern assimilation as evidence | Provenance, license, dependency, instruction-risk, security review, limitations | External code adoption, external instructions, source copy, install/run pressure | L9, L4, L6 |
| GT-12 Publication / Git Mutation Gate | Staging, commit, push, force-add, release, publication | Exact paths, diff/status review, sensitive-output review, human approval, rollback | `git add .`, commit, push, publication, generated/local-only leakage | L0, L8, L9, L10 |
| GT-13 Persistence / State Store Gate | Operational state store | Owner, retention, sensitivity, schema/change control, backup/export, removal plan | Persistence, hidden state store, secret retention, CSS substrate confusion | L7, L8 |
| GT-14 Test / CI Gate | Tests, static checks, CI | Exact command, dependencies, data, environment, output handling, rollback | Test execution, CI creation, product/external execution, package side effects | L1, L10 |
| GT-15 Rollback / Incident Gate | Deactivation, quarantine, removal, restore, rotation, reporting | Rollback owner, trigger, impacted paths, quarantine/removal/state restore, incident route | Irreversible activation, unknown impact, missing rollback | All lanes |

## 9. Universal Gate Record Control Fields
Future gate records must include all of these fields before a review can move beyond draft.

| Field group | Required fields | Blocker if missing |
| --- | --- | --- |
| Identity | `gate_id`, `gate_type`, `title`, `owner`, `requester`, `created_at` | Yes |
| Scope | `target_paths`, `excluded_paths`, `activation_level_from`, `activation_level_to`, `current_status`, `requested_status` | Yes |
| Posture | `source_posture`, `git_posture`, `dependency_posture`, `validation_posture`, `security_posture`, `product_posture`, `external_source_posture`, `CSS_substrate_impact` | Yes |
| Evidence | `evidence_refs`, `proof_level_target`, `limitations`, `blockers` | Yes |
| Safety | `rollback_plan`, `stop_rules`, `validation_commands_allowed`, `incident_response` | Yes |
| Decision | `decision_status`, `decision_authority`, `review_required` | Yes |

If a field is unknown, the gate remains `blocked`, `needs_evidence`, `needs_security_review`, `needs_validation_review`, or `rejected_for_scope`.

## 10. Work Packet And Lane Binding
| Lane | First ticket | P0.1 binding |
| --- | --- | --- |
| L0 Governance / Activation Gate Control Plane | P0.1 | This map is the control-plane reference; no activation. |
| L1 Validation Execution Gate | P0.2 | May design validation execution route after P0.1; must not execute validation. |
| L2 Security Enforcement Gate | P0.3 | May design security hardening after P0.1; must not implement enforcement or inspect secrets. |
| L3 Context Runtime Hardening | P1.1 | Must preserve context-as-metadata and no source-loading semantics. |
| L4 Provider Adapter Metadata Layer | P1.2 | Must preserve provider/auth/network/MCP blockers. |
| L5 Tool Execution Boundary | P1.3 | Must preserve execution-not-approved defaults and S-04 risk controls. |
| L6 Agent Runtime Boundary | P1.4 | Must preserve agent/task/handoff metadata-only posture. |
| L7 Cognitive Semantic System Prototype | P1.5 | Must preserve Cognitive Semantic System naming and substrate deferral. |
| L8 Observability / Audit / Retention / Rollback | P2.3 | Must align with GT-15 and generated-output sensitivity controls. |
| L9 Graphify Operating Support | GX-03 if needed | Must keep Graphify local-only/supporting evidence only; no rerun by this map. |
| L10 Siamese Product Integration Readiness | P4.1 | Must preserve product local-only/inactive posture until product gate. |

## 11. Evidence And Proof Control
| Evidence class | Allowed P0.1 use | Not allowed inference |
| --- | --- | --- |
| Architecture record | Cite governance/security/validation decisions. | Runtime approval. |
| Implementation record | Cite metadata-only component boundaries. | Execution readiness. |
| Validation record | Cite proof posture and limitations. | Governance approval or activation. |
| Security decision | Cite access and sensitivity constraints. | Runtime enforcement by itself. |
| Graphify summary | Cite supporting code-only component signals. | Authority, source truth, substrate selection, or activation readiness. |
| `.graphifyignore` | Cite Graphify input boundary. | Permission to rerun Graphify or broaden source. |
| `.gitignore` | Cite local-only hygiene. | Security guarantee or staging approval. |
| README.md | Cite root workspace description. | Activation approval. |

Evidence supports decision; evidence does not decide.

## 12. Stop Rule Map
| Trigger | Required stop behavior | Future route |
| --- | --- | --- |
| Runtime, service, scheduler, worker, queue, or autonomous loop needed | Stop. | GT-06. |
| Validation command, test, build, CI, or package command needed | Stop. | GT-04, GT-14, GT-07, and exact command approval. |
| Tool, shell, subprocess, filesystem, network, Git mutation, or generated command execution needed | Stop. | GT-07 and S-04 approval. |
| Provider/API/MCP/network/auth or credential use needed | Stop. | GT-08 and S-03/S-04 secure approval. |
| Secret or credential content appears necessary | Stop; report safe metadata only. | S-03 secure handling. |
| Product source inspection, execution, dependency, or source tracking needed | Stop. | GT-09. |
| Existing `3_platform` sibling inspection or reuse needed | Stop. | GT-01. |
| Source tracking expansion, force-add, staging, commit, push, or publication needed | Stop. | GT-02 and GT-12 with exact human approval. |
| Final CSS substrate, graph/vector/database/ontology runtime, or persistence needed | Stop. | GT-10 and GT-13. |
| Graphify rerun, labelled backend/provider setup, or Graphify adoption needed | Stop. | Future Graphify-specific gate with provider/auth/security review if applicable. |
| P0.2 or P0.3 implementation pressure appears inside P0.1 | Stop or defer to future ticket. | Start only after explicit instruction. |

## 13. Blocker Register
| Blocker | Current status | Blocks |
| --- | --- | --- |
| No source classification for existing `3_platform` siblings | Open | AL-2 promotion, sibling reuse, source tracking expansion. |
| No validation execution design accepted yet | Open | AL-3 promotion and validation dry-runs. |
| No security enforcement hardening accepted yet | Open | AL-4 promotion and local enforcement design. |
| No runtime lifecycle design | Open | AL-5 promotion. |
| No provider/auth/network/MCP approval | Open | AL-6 provider/tool candidate work. |
| No dependency review/adoption | Open | Package, SDK, Graphify/Hermes/provider/tool adoption. |
| No final Cognitive Semantic System substrate | Open | AL-7 promotion and persistent semantic authority. |
| No product activation gate record | Open | AL-8 product pilot. |
| No test/CI gate | Open | Test execution and CI creation. |
| No audit/retention/rollback baseline | Open | Operational readiness and AL-9. |
| Generated outputs local-only | Open | Generated output tracking/publication. |
| Product source local-only | Open | Product inspection, execution, source tracking. |
| Graphify evidence-only posture | Open by design | Graphify authority, adoption, or substrate inference. |

## 14. Decision Status Model
| Status | Meaning | May activate? |
| --- | --- | --- |
| `draft` | Gate record incomplete. | No. |
| `candidate_for_review` | Required fields appear present but not accepted. | No. |
| `needs_evidence` | Evidence or proof target missing. | No. |
| `needs_security_review` | Security/access/sensitivity review missing. | No. |
| `needs_validation_review` | Validation/proof review missing. | No. |
| `blocked` | Stop condition prevents progress. | No. |
| `rejected_for_scope` | Scope is unsafe, broad, wrong, or premature. | No. |
| `approved_for_exact_scope` | Future governance/human approval for named scope only. | Only if the gate explicitly authorizes that exact activation. |
| `approved_with_cautions` | Future approval with retained limitations/blockers. | Only within exact retained limits. |
| `superseded` | Replaced by newer gate. | No. |
| `retired` | No longer active. | No. |

No status can override secrets, credentials, missing ownership, unknown sensitivity, missing rollback, or missing exact scope.

## 15. Rollback And Incident Control
Every future activation gate must define rollback before approval.

| Rollback field | Required content |
| --- | --- |
| Owner | Human or governance owner accountable for rollback. |
| Trigger | Condition that starts rollback or incident response. |
| Impacted paths/surfaces | Exact files, runtime surfaces, products, providers, generated outputs, or Git surfaces. |
| Deactivation path | How to stop or disable the approved action. |
| Quarantine/removal | How unsafe files, outputs, configs, or artifacts are isolated or removed. |
| State restore/export | How state is preserved, exported, restored, or discarded. |
| Credential rotation route | Required if a credential might be exposed or used; values must never be documented. |
| Evidence retention | Safe records retained without secrets/local-only leakage. |
| Follow-up governance | Review, incident, audit, or superseding gate required after rollback. |

Incident response defaults to STOP, report safe metadata only, preserve boundaries, and require governance/security direction.

## 16. Graphify Evidence Boundary
Graphify evidence is supporting evidence, not authority.

| Graphify surface | P0.1 posture |
| --- | --- |
| Current valid graph | Local-only generated evidence from the G-17-safe run. |
| Current curated use | Component separation and shared metadata signals only. |
| Labelled-output attempt | Blocked by missing provider/backend; no provider/auth setup approved. |
| `.graphifyignore` | Default-deny root profile; only approved governed skeleton Python files were included. |
| Generated outputs | Local-only under `9_artifacts/`; not source by default. |
| Authority | None. Governance decisions override generated projections. |
| Substrate | None. Graphify does not select the Cognitive Semantic System substrate. |
| Future action | Any rerun, output tracking, provider/backend labelling, OpenCode/MCP integration, or adoption requires a future exact gate. |

## 17. Component Activation Boundary Map
| Component | Current accepted artifact | Activation boundary |
| --- | --- | --- |
| Validation registry | I-01 metadata registry | Not validation execution, CI, test runner, or approval engine. |
| Security/access evaluator | I-02 metadata evaluator | Not runtime enforcement, secret scanner, filesystem guard, or network guard. |
| Context pack runtime | I-03 metadata runtime | Not source loading, context permission, migration, or raw source inclusion. |
| Provider/adapter layer | I-04 metadata layer | Not provider activation, adapter runtime, API client, network call, credential access, or MCP activation. |
| Agent runtime boundary | I-05 metadata boundary | Not agent activation, task execution, handoff execution, scheduler, or orchestration runtime. |
| Tool execution boundary | I-06 metadata boundary | Not tool execution, shell/subprocess execution, filesystem/network action, package/build/test execution, or Git mutation. |
| Cognitive Semantic System prototype | I-07 metadata prototype | Not truth engine, reasoning execution, persistence, graph/vector/database/ontology runtime, or substrate selection. |

## 18. Downstream Ticket Controls
| Ticket | May do after explicit instruction | Must not do |
| --- | --- | --- |
| P0.2 | Design the Validation Execution Gate route, proof target model, command proposal format, evidence retention model, and limitations. | Run validation, tests, CI, package managers, product checks, provider calls, or treat validation as approval. |
| P0.3 | Design Security Enforcement Hardening Plan, policy-to-gate mapping, sensitivity handling, escalation, and incident posture. | Implement enforcement, scan secrets, inspect credentials, call network/providers/MCP, execute tools, or activate products. |
| P1.1-P1.5 | Harden metadata contracts under gate references. | Activate runtime, source loading, providers, tools, agents, products, persistence, or CSS substrate. |
| P2.x | Align shared vocabulary, evidence references, audit, retention, and rollback. | Create runtime logging/persistence/publication without gates. |
| P3.x | Prepare activation readiness decisions. | Activate without exact gate records and approvals. |
| P4.1 | Define Siamese product integration readiness. | Inspect or activate product source by default. |

P0.2 and P0.3 are named as downstream routes only. P0.1 does not start P0.2 or P0.3.

## 19. Created / Not Created Register
| Artifact or action | P0.1 status |
| --- | --- |
| `0_architecture/governance/agent_platform_activation_gate_enforcement_map.md` | Created. |
| Runtime enforcement | Not created. |
| Implementation code | Not modified. |
| `3_platform/_governed_skeleton/` | Not modified. |
| Existing `3_platform` siblings | Not inspected, classified, approved, or modified. |
| Product workspaces | Not inspected, activated, tracked, or modified. |
| `.graphifyignore` | Not modified. |
| `.gitignore` | Not modified. |
| Graphify | Not run, configured, adopted, or treated as authority. |
| Generated outputs under `9_artifacts/` | Not modified or tracked. |
| Provider/auth/API/MCP | Not configured, inspected, called, or activated. |
| Tools/shell/tests/package managers | Not approved or activated by this map. |
| Cognitive Semantic System substrate | Not selected. |
| Git staging/commit/push/publication | Not authorized. |
| P0.2 / P0.3 | Not started. |

## 20. Invariants And Final Verdict
| ID | Invariant |
| --- | --- |
| P01-001 | Activation Gate Enforcement Map is a governance control-plane document only. |
| P01-002 | Gate enforcement map is not runtime enforcement. |
| P01-003 | AGENT PLATFORM remains pre-active at AL-1 metadata skeleton. |
| P01-004 | No activation level promotion occurs in P0.1. |
| P01-005 | Validation evaluates; governance decides. |
| P01-006 | Security constrains execution, source access, provider/auth, local-only material, secrets, credentials, products, MCP, publication, and generated outputs. |
| P01-007 | Cognitive Semantic System substrate remains deferred. |
| P01-008 | Graph remains candidate only. |
| P01-009 | Graphify remains evidence only, not authority. |
| P01-010 | Siamese remains the living energy twin product vision; product workspaces remain local-only and inactive. |
| P01-011 | Source tracking expansion, force-add, staging, commit, push, and publication remain human-gated and not approved. |
| P01-012 | P0.1 stops before P0.2 and P0.3. |

Final verdict: P0.1 creates the documentation-only Activation Gate Enforcement Map. It maps G-01 gate types, AL promotion blockers, required evidence, stop rules, rollback/incident expectations, lane bindings, and downstream routes. It does not implement runtime enforcement, approve activation, broaden source tracking, inspect product source, run Graphify, configure providers/auth, execute tools, select the Cognitive Semantic System substrate, stage, commit, push, publish, or start P0.2/P0.3.
