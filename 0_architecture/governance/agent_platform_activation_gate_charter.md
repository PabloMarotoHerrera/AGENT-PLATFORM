# G-01 - Activation Gate Charter

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Activation Gate Charter |
| Ticket | G-01 |
| Status | Accepted activation gate charter |
| Date | 2026-07-02 |
| Scope | Formal gate model for promoting AGENT PLATFORM capabilities from pre-active metadata skeleton toward an active governed agent platform for Siamese. |
| Authority | Governance gate model only, not activation. |
| Related documents | G-00, I-A, I-00 through I-07, IR-A, P-A, W-series, V-series, S-series, CSS-series, H-series, `.gitignore`, README.md, Siamese Product Vision |
| Decision target | Activation gate model for AGENT PLATFORM |

## 2. Purpose
G-00 selected the direction toward an active governed agent platform for Siamese. G-01 defines the gate model required before any activation-level promotion.

G-01 prevents roadmap drift and loose projects by requiring every future activation request to name owner, exact scope, evidence, security posture, validation posture, rollback, stop rules, and decision authority. G-01 does not implement, activate, inspect source, adopt dependencies, approve source tracking, or start G-02.

## 3. Current Activation Posture
| Area | Current posture |
| --- | --- |
| Activation ceiling | Current activation ceiling remains AL-1 metadata skeleton. |
| I-00 through I-07 | Bounded metadata-only, in-memory, stdlib-only modules. |
| Runtime/execution | No runtime activation, execution, persistence, scheduler, worker, service, or autonomous process. |
| Tests/CI | No tests, scripts, tools, package manifests, lockfiles, or CI. |
| Providers/API/MCP/products | No provider/API/MCP activation and no product activation. |
| Cognitive Semantic System | Accepted name; final substrate deferred. |
| Source boundary | `3_platform/_governed_skeleton/` is the only approved implementation subroot; existing `3_platform` siblings remain uninspected and unapproved. |

## 4. Activation Gate Charter Definition
An activation gate charter is a governance model that defines what evidence, ownership, scope, security posture, validation posture, source posture, rollback path, and stop rules are required before any capability may move from candidate or metadata-only status toward active operation.

Activation gate charter is not activation. It is not implementation, source tracking approval, dependency adoption, provider/API/MCP activation, product activation, or Cognitive Semantic System substrate selection.

## 5. Gate Authority Model
| Layer | Authority |
| --- | --- |
| Governance | Decides promotion, rejection, deferral, exception, lifecycle, and activation level changes. |
| Validation | Evaluates evidence and proof posture; validation evaluates; governance decides. |
| Security | Constrains action, exposure, execution, credentials, network, MCP, local-only, and publication. |
| Product governance | Constrains product work, product activation, product dependencies, and product source posture. |
| Git | Records approved artifacts after exact human approval; Git does not approve. |
| Agents | May prepare metadata only unless explicitly authorized; AI agents cannot be sole final approver. |
| External sources | Provide evidence only; relevance is not adoption. |

## 6. Activation Ladder Binding
| Level | Name | G-01 posture |
| --- | --- | --- |
| AL-0 | Architecture records | Achieved as records. |
| AL-1 | Metadata skeleton | Current ceiling. |
| AL-2 | Controlled classification | Future gate required. |
| AL-3 | Validation/security dry-run | Future gate required. |
| AL-4 | Enforced local policy | Future gate required. |
| AL-5 | Minimal runtime candidate | Future gate required. |
| AL-6 | Tool/provider candidate | Future gate required. |
| AL-7 | Cognitive Semantic System active substrate | Future gate required. |
| AL-8 | Product pilot | Future gate required. |
| AL-9 | Operational active platform | Future gate required. |

G-01 does not promote beyond AL-1. Every promotion requires a gate record.

## 7. Gate Types
| Gate | Purpose |
| --- | --- |
| GT-01 Source Classification Gate | Classify exact paths, sensitivity, source class, owner, and reuse boundary. |
| GT-02 Source Tracking Gate | Decide exact Git tracking posture and exclusions. |
| GT-03 Dependency Adoption Gate | Review package, SDK, solver, source, license, security, supply chain, and rollback. |
| GT-04 Validation Execution Gate | Approve exact validation commands, data, paths, proof targets, and evidence retention. |
| GT-05 Security Enforcement Gate | Move security/access metadata toward enforceable local policy only after review. |
| GT-06 Runtime Activation Gate | Approve scheduler, worker, queue, service, lifecycle, logs, and rollback. |
| GT-07 Tool Execution Gate | Approve shell, filesystem, subprocess, package, build, test, and audit boundaries. |
| GT-08 Provider / API / MCP Activation Gate | Approve provider descriptors, auth boundary, data exposure, MCP resources/tools, and rollback. |
| GT-09 Product Activation Gate | Approve product owner, source, dependencies, validation baseline, output controls, and rollback. |
| GT-10 Cognitive Semantic System Substrate Gate | Decide substrate only after candidate evidence and rollback planning. |
| GT-11 External Architecture Assimilation Gate | Assimilate external patterns as evidence, not adoption. |
| GT-12 Publication / Git Mutation Gate | Approve exact staging, commit, push, force-add, or publication scope. |
| GT-13 Persistence / State Store Gate | Approve operational state store without selecting final CSS substrate. |
| GT-14 Test / CI Gate | Govern future unit, integration, static, and CI checks. |
| GT-15 Rollback / Incident Gate | Define deactivation, quarantine, artifact removal, rotation, and reporting. |

## 8. Universal Gate Record Format
| field | required? | description | blocker if missing? |
| --- | --- | --- | --- |
| gate_id | yes | Stable gate identifier. | yes |
| gate_type | yes | One GT-01 through GT-15 type. | yes |
| title | yes | Human-readable exact scope. | yes |
| owner | yes | Accountable human/governance owner. | yes |
| requester | yes | Person or agent requesting review. | yes |
| target_paths | yes | Exact included paths or surfaces. | yes |
| excluded_paths | yes | Exact exclusions, especially local-only, product, external, secrets. | yes |
| activation_level_from | yes | Current AL level. | yes |
| activation_level_to | yes | Requested AL level. | yes |
| current_status | yes | Current candidate, blocked, metadata, or inactive status. | yes |
| requested_status | yes | Requested promotion/status. | yes |
| source_posture | yes | Internal, product, external, generated, local-only, unknown, or classified. | yes |
| git_posture | yes | Trackable, ignored, local-only, exact-path, or blocked. | yes |
| dependency_posture | yes | None, candidate, reviewed, adopted, rejected, or blocked. | yes |
| validation_posture | yes | Proof target, evidence, commands, limitations. | yes |
| security_posture | yes | Sensitivity, access, execution, network, secret, credential, local-only posture. | yes |
| product_posture | yes | Product impact or not applicable. | yes |
| external_source_posture | yes | External evidence, review, adoption, or blocked posture. | yes |
| CSS_substrate_impact | yes | None, candidate impact, or substrate decision impact. | yes |
| evidence_refs | yes | Architecture, validation, security, audit, and approval references. | yes |
| proof_level_target | yes | PL target and sufficiency rationale. | yes |
| limitations | yes | Known gaps and uncertainty. | yes |
| blockers | yes | Stop conditions still open. | yes |
| rollback_plan | yes | Deactivate, remove, restore, quarantine, or rotate path. | yes |
| stop_rules | yes | Conditions requiring STOP and escalation. | yes |
| validation_commands_allowed | yes | Exact commands or `none`. | yes |
| incident_response | yes | Response if gate is breached. | yes |
| decision_status | yes | Draft, blocked, approved exact scope, or other status. | yes |
| decision_authority | yes | Governance/human authority required. | yes |
| created_at | yes | Date of gate record. | yes |
| review_required | yes | Required validation/security/product/release reviews. | yes |

## 9. Gate Status Model
| Status | Meaning |
| --- | --- |
| draft | Incomplete gate record. |
| candidate_for_review | Complete enough for review, not approved. |
| blocked | Stop condition prevents progress. |
| needs_evidence | Evidence refs or proof target missing. |
| needs_security_review | Security/access/sensitivity review missing. |
| needs_validation_review | Validation/proof review missing. |
| rejected_for_scope | Scope is unsafe, too broad, or wrong ticket. |
| approved_for_exact_scope | Approved only for named paths, commands, data, level, and owner. |
| approved_with_cautions | Approved with retained limitations and blockers. |
| superseded | Replaced by newer governed gate. |
| retired | No longer active for future promotion. |

`approved_for_exact_scope` is not broad approval. `approved_with_cautions` requires retained blockers and limitations. No gate status can override secrets, credentials, unknown sensitivity, or missing ownership.

## 10. Source Classification Gate
Purpose: classify exact paths only before reuse, source tracking, execution, context inclusion, product activation, or implementation expansion. Required inputs: owner, exact include/exclude paths, source class, sensitivity, local-only posture, prior decisions, and rollback. Allowed evidence: path existence, architecture records, safe metadata, Git ignore posture, and content review only when explicitly scoped. Forbidden actions: execution, tracking approval, broad inspection, secret/credential inspection, or source adoption. Output statuses: candidate_for_review, blocked, needs_evidence, approved_for_exact_scope, rejected_for_scope. Stop rules: missing owner, unknown sensitivity, secrets, broad path request, or need to inspect existing `3_platform` siblings without exact gate. Existing `3_platform` siblings require this gate before reuse.

## 11. Source Tracking Gate
Purpose: decide exact source tracking posture. Required Git posture: current ignore/tracked state, exact paths, exclusions, sensitivity, owner, and human approval. Exact-path staging model: only named files may be considered; no `git add .`. Force-add policy: no force-add without explicit approval and exact rationale. `.gitignore` relationship: ignored does not mean safe; `.gitignore` is hygiene, not security. Product, external, generated, local-only, secret, credential, dependency, cache, and unknown-sensitive material remain excluded. Source tracking is not implementation approval. Git action requires explicit human approval. Stop on broad staging, local-only force-add, unclear Git posture, or secret risk.

## 12. Dependency Adoption Gate
Purpose: govern dependencies, SDKs, packages, solvers, external code, registries, and manifests. Required metadata: name, version, source, scope, owner, provenance, license, notices, transitive graph, scripts, network/auth behavior, runtime behavior, lock strategy, validation, security, and rollback. License, security, and supply-chain review are mandatory. Manifests and lockfiles require explicit approval and rollback. Dependency relevance is not adoption. Package installation is not allowed without exact approval. Hermes/Graphify dependencies are not adopted by this charter. Stop on missing license, unknown transitive risk, package scripts, native/runtime risk, network/auth risk, or unclear rollback.

## 13. Validation Execution Gate
Purpose: move from metadata registry/review to exact validation execution. Metadata registry records criteria and evidence; execution runs exact commands or reviews exact data. Required proof levels: target PL, method, criteria, command/path/data scope, limitations, reviewer, retention, and revalidation trigger. Allowed validation commands must be exact command/path/data scoped. Evidence retention follows V-series summaries, references, redaction, command records, and no secret values. Validation evaluates, does not decide. Stop on unapproved command, broad data, sensitive output, provider/network/package side effects, or missing proof target.

## 14. Security Enforcement Gate
Purpose: move access/security metadata toward enforceable local policy only after governance. Required distinctions: access metadata is not enforcement; a policy record is not runtime control. Secrets/credentials: no value inspection, use, summarization, or retention. No secret scanning by reading secrets without security approval. Local-only boundaries, network/tool/provider/MCP constraints, and incident response must be explicit. Unknown sensitivity blocks or requires review. Stop on secret/credential exposure, unscoped scan, local-only leakage, network/provider/MCP action, or missing incident plan.

## 15. Runtime Activation Gate
Purpose: approve any scheduler, worker, queue, daemon, service, process lifecycle, task runner, or autonomous loop. Required: runtime owner, exact process model, start/stop commands, dry-run plan, persistence/log policy, rollback, security posture, validation evidence, and incident handling. Metadata module is not runtime. Dry-run can precede execution. No autonomous runtime by default. Stop on missing owner, uncontrolled loop, unclear process lifecycle, persistence without gate, logs with sensitive data, or rollback absence.

## 16. Tool Execution Gate
Purpose: govern tool, shell, subprocess, filesystem, package manager, build, test, native, and mutation-capable actions. Risk levels must separate read-only inspection from mutation-capable, execution, network, auth, native, destructive, and publication actions. Shell availability is not command approval. Tool availability is not permission. Execution decision metadata is not authorization. Audit logging must record exact action, actor, cwd, inputs, outputs, side effects, sensitivity, and rollback. Stop on unapproved command, broad filesystem access, package/build/test side effects, or missing audit record.

## 17. Provider / API / MCP Activation Gate
Purpose: govern providers, APIs, model endpoints, networks, MCP servers, tools, and resources. Required descriptors: provider identity, endpoint, data sent/received, auth posture, credential reference model without values, cost/retention, network exposure, security review, validation plan, rollback. Provider credentials are not provider permission. Provider registration is not activation. MCP availability is not MCP activation. MCP resource exposes data; MCP tool can perform actions and is higher risk. Stop on credential use, unknown data exposure, network side effects, unreviewed MCP tool/resource, or missing rollback.

## 18. Product Activation Gate
Purpose: approve product work only inside declared product scope. Required: product owner, source posture, dependency posture, validation baseline, security/local-only posture, generated-output controls, Git posture, root-boundary statement, rollback. Product charter is not product activation. Siamese product vision informs requirements but does not activate source. EnergyPlus remains solver, Omniverse Kit remains interface. Stop on missing owner, local-only product source, unreviewed dependencies, unrun/unauthorized validation, generated-output sensitivity, product-root collapse, or rollback absence.

## 19. Cognitive Semantic System Substrate Gate
Purpose: decide future CSS substrate only through multi-candidate evidence. Required: candidate substrate evidence, query workload evidence, validation/security/governance review, migration/rollback, data retention, export/replacement path, and substrate decision record. Cognitive Semantic System name is accepted. Cognitive Semantic System substrate remains deferred. Graph remains candidate only until governed decision. Graph/vector/ontology/database are candidates only. Graphify remains evidence only, not authority. Stop on graph lock-in, product/external naming pressure, missing evaluation, migration risk, secret/local-only retention, or irreversible substrate choice.

## 20. External Architecture Assimilation Gate
Purpose: convert external architecture relevance into internal governed patterns without adoption. Applies to Hermes, Graphify, OpenCode, Clawhub, OpenClaw, ai-cookbook, and other sources. Required: evidence extraction, pattern mapping, provenance, license review, dependency review, security review, instruction-risk review, adapter candidate review, limitations, and exact future ticket for any source inspection. External relevance is not adoption. Hermes is not adopted by G-01. Graphify is not adopted by G-01. Source inspection requires exact future ticket. Stop on source-copy pressure, install/run pressure, external instruction adoption, adapter activation, or license/security gaps.

## 21. Publication / Git Mutation Gate
Purpose: govern staging, commit, push, force-add, release, and publication. Required: exact paths, diff/status review, generated/local-only exclusions, secret/credential review, human approval, rollback, and publication target. No broad staging. No force-add without explicit approval. No publication by audit or gate status alone. Stop on `git add .`, unclear staged set, ignored/local-only material, secrets, credentials, generated-sensitive output, product/external raw source, or missing human approval.

## 22. Test / CI Gate
Purpose: govern future Q-series tests, static checks, integration checks, runners, and CI. Tests are future, not created by G-01. Unit, integration, static, product, external, and runtime checks require exact commands, dependencies, data, environment, output handling, and approval. Test commands must be exact and approved. CI is not created by G-01. Stop on package manager side effects, unreviewed dependency impact, network/auth use, product/external execution, or missing rollback.

## 23. Persistence / State Store Gate
Purpose: govern operational state stores separately from final Cognitive Semantic System substrate. JSONL and SQLite may be candidate operational stores only after future review. Operational state store is not final CSS substrate. Required: retention, sensitivity, schema/change control, backup, export, rollback, security review, validation, and owner. No persistence created by G-01. Stop on secret retention, local-only leakage, hidden database creation, substrate confusion, or missing removal plan.

## 24. Rollback / Incident Gate
Purpose: ensure every activation can be reversed or contained. Required rollback fields: owner, trigger, impacted paths, deactivation steps, quarantine, artifact removal, state restore, credential rotation if applicable, incident reporting, evidence retention, and follow-up governance. Stop rules: unknown impact, missing rollback owner, irreversible action, secret/credential exposure, uncontrolled runtime, Git/publication mutation, or inability to quarantine.

## 25. Promotion Rule Matrix
| from_level | to_level | required gates | minimum evidence | explicit blocker |
| --- | --- | --- | --- | --- |
| AL-1 | AL-2 | GT-01, GT-02 as needed, GT-15 | Exact paths, owner, source/sensitivity/Git posture. | Existing `3_platform` siblings unknown. |
| AL-2 | AL-3 | GT-04, GT-05 dry-run, GT-15 | PL target, validation/security dry-run evidence. | Execution command not exact. |
| AL-3 | AL-4 | GT-05, GT-07 if tools involved, GT-15 | Security decision, local policy dry-run, rollback. | Unknown sensitivity or secret risk. |
| AL-4 | AL-5 | GT-06, GT-13 if state, GT-15 | Runtime owner, lifecycle, logs, no autonomous default. | No rollback or process control. |
| AL-5 | AL-6 | GT-07, GT-08, GT-03, GT-15 | Tool/provider/API/MCP exact scope, dependency review. | Auth/network/package risk unresolved. |
| AL-6 | AL-7 | GT-10, GT-13, GT-05, GT-15 | Multi-candidate CSS evidence and migration/rollback. | Final substrate not governed. |
| AL-7 | AL-8 | GT-09, GT-14, GT-12 if Git/publication, GT-15 | Product owner, baseline, source/dependency/security review. | Product source local-only. |
| AL-8 | AL-9 | All relevant gates, GT-15, audit | Operational audit, validation, security, rollback, publication posture. | Any missing owner, evidence, security, or rollback. |

## 26. Gate Evidence Model
Evidence types: architecture record, validation record, security decision, context pack, dependency review, license review, source classification, Git posture decision, test result, audit log, rollback plan, incident review, and human approval.

Evidence supports decision; evidence does not decide. Missing evidence blocks promotion unless governance records an explicit bounded exception that still cannot override secrets, credentials, unknown sensitivity, or missing ownership.

## 27. Gate Ownership Model
Required roles: owner, reviewer, validator, security reviewer, product owner if applicable, release approver if applicable, and rollback owner. No owner means blocked. AI agents may draft, summarize, classify, validate when scoped, and prepare metadata, but AI agents cannot be sole final approver.

## 28. No-loose-projects Enforcement
Any future ticket must map to roadmap phase, gate type, activation level, exact paths, owner, non-goals, stop rules, and audit route. Work without these fields remains evidence or candidate material only.

## 29. Created / Not Created Register
| artifact/action | status in G-01 | reason |
| --- | --- | --- |
| Activation gate charter | Created | Required G-01 governance artifact. |
| Implementation code | Not created | Governance only. |
| Tests | Not created | Future GT-14/Q-series. |
| Runtime | Not activated | GT-06 required later. |
| Providers/API/MCP | Not activated | GT-08 required later. |
| Hermes | Not adopted | External evidence only. |
| Graphify | Not adopted | Evidence only, not authority. |
| CSS substrate | Not selected | GT-10 required later. |
| Source tracking | Not expanded | GT-02 required later. |
| Next ticket | Not started | G-01 stops before G-02. |

## 30. Residual Risk Register
| Risk | Current handling |
| --- | --- |
| Gate model exists but not enforced by runtime | Manual governance only. |
| No tests | Future GT-14. |
| No persistence | Future GT-13. |
| No source classification yet | Future GT-01. |
| No dependency review | Future GT-03. |
| No runtime activation | Future GT-06. |
| No provider/MCP activation | Future GT-08. |
| No CSS substrate | Future GT-10. |
| Existing `3_platform` siblings unknown | Uninspected and unapproved. |
| Product source local-only | Product gate required. |
| Hermes unevaluated | External architecture gate required. |
| Roadmap can drift if gates are bypassed | No-loose-projects rule and incident handling. |

## 31. Blocker Register
Blockers: missing owner; missing exact path; missing rollback; missing validation evidence; missing security review; unknown sensitivity; dependency unknown; source posture unknown; Git posture unclear; product impact unclear; external source pressure; runtime activation pressure; tool execution pressure; provider/MCP activation pressure; CSS substrate pressure; next-ticket pressure. Any blocker keeps the requested promotion blocked, narrowed, or deferred.

## 32. Incident Handling
Incidents include: G-01 starts implementation; G-01 promotes activation level; G-01 inspects `3_platform` siblings; G-01 adopts Hermes; G-01 adopts Graphify; G-01 selects CSS substrate; G-01 activates providers/API/MCP; G-01 approves tool execution; G-01 approves broad source tracking; G-01 inspects external/product/secrets; G-01 modifies implementation artifacts; G-01 starts G-02; Git mutation attempted.

Response: STOP, report safe metadata only, require governance/security decision.

## 33. G-01 Invariants
| ID | Invariant |
| --- | --- |
| G01-001 | Activation gate charter is not activation. |
| G01-002 | Gate approval is exact-scope only. |
| G01-003 | Roadmap phase is not permission. |
| G01-004 | Current activation ceiling remains AL-1. |
| G01-005 | Runtime activation remains blocked. |
| G01-006 | Tool execution remains blocked. |
| G01-007 | Provider/API/MCP activation remains blocked. |
| G01-008 | Product activation remains blocked. |
| G01-009 | Dependencies remain unadopted. |
| G01-010 | Existing 3_platform siblings remain uninspected and unapproved. |
| G01-011 | Hermes is not adopted by G-01. |
| G01-012 | Graphify remains evidence only, not authority. |
| G01-013 | Cognitive Semantic System substrate remains deferred. |
| G01-014 | Validation evaluates; governance decides. |
| G01-015 | G-01 stops before G-02. |

## 34. Anti-patterns
Anti-patterns: gate charter as activation; gate status as broad approval; roadmap as permission; source tracking as implementation approval; dependency relevance as adoption; provider registration as activation; tool decision as execution authorization; context inclusion as permission; CSS candidate as substrate selection; Hermes usefulness as Hermes adoption; Graphify evidence as authority; existing `3_platform` as approved source; `git add .`; starting G-02 inside G-01.

Rejected/prohibited/historical examples only: `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth`. No such string is accepted as a current AGENT PLATFORM or Cognitive Semantic System name.

## 35. Next Ticket Recommendation
Recommended next ticket: G-02 — Source Tracking Expansion Decision.

Alternative: G-03 — Existing 3_platform Classification.

Recommended sequence: 1. G-02 Source Tracking Expansion Decision; 2. G-03 Existing 3_platform Classification; 3. G-04 External Architecture Assimilation Strategy; 4. G-05 Hermes Architecture Evaluation Gate; 5. G-06 Dependency / License / Security Adoption Gate; 6. G-A Post-Implementation Governance Audit.

G-01 does not start G-02.

## 36. Final Verdict
| Question | Answer |
| --- | --- |
| What does G-01 define? | The canonical activation gate model for AGENT PLATFORM capabilities. |
| Does G-01 activate AGENT PLATFORM? | No. |
| Does G-01 promote beyond AL-1? | No. |
| Does G-01 approve source tracking expansion? | No. |
| Does G-01 inspect or approve `3_platform` siblings? | No. |
| Does G-01 adopt Hermes? | No. |
| Does G-01 adopt Graphify? | No. |
| Does G-01 select CSS substrate? | No. |
| Does G-01 create implementation, tests, runtime, providers, MCP, or products? | No. |
| What remains blocked? | Implementation, activation, runtime, tools, providers/API/MCP, products, dependencies, source tracking expansion, existing `3_platform` reuse, CSS substrate selection, persistence, tests/CI, publication, staging, commit, push, and G-02. |
| What is the next recommended ticket? | G-02 — Source Tracking Expansion Decision, after explicit instruction only. |
