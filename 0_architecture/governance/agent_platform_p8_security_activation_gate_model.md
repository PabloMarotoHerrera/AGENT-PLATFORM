# P8 Security / Activation Gate Model

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | P8 Security / Activation Gate Model |
| Ticket | P8.5 |
| Status | Accepted Security / Activation Gate Model |
| Date | 2026-07-06 |
| Scope | Documentation-only security and activation gate model for AGENT PLATFORM / Siamese P8 MVP planning. |
| Authority | Security/activation gate design only, not implementation, not gate enforcement runtime, not runtime activation, not autonomous orchestration, not automatic dispatch, not automatic reviewer assignment, not automatic integration, not Git mutation, not product/Siamese source inspection, not OpenCode execution, not Graphify execution, not GBrain runtime, not GStack execution, not Hermes runtime, not Cadence, not provider/auth/API/MCP activation, not live connector activation, not persistence, not vector DB, not graph DB, not Cognitive Semantic System substrate selection, and not publication. |
| Prerequisite | P8.0 Platform MVP Scope / External Integration Boundary. |
| Related documents | P8.0, P8.1 if present, P8.2 if present, P8.3 if present, P8.4 if present, P7.R, P7.0.A-P7.0.H, P6.7, P6.1-P6.6, P5.R, P5.1-P5.7, P3.BR, P3.3, P3.4, P3.5, P2.1, P2.2, P2.3, P2.KR, P1.1-P1.5, P0.1-P0.3, S-03, S-04, CSS ADR/audit. |
| External candidates | Graphify, GBrain, GStack, Hermes, OpenCode. |
| Present P8 sibling alignments | P8.1 external inventory alignment present; P8.4 local workspace/state alignment present. |
| Pending alignments | `pending_P8.2_interaction_surface_alignment`; `pending_P8.3_schema_alignment`. |
| Output | P8 Security / Activation Gate Model. |
| Target result | `p8_security_activation_gate_model_ready`. |

## 2. Purpose

P8.5 hardens P8.0's preliminary scope levels into a security / activation gate model.

P8.5 defines the allowed and blocked behavior at `P8-L0` through `P8-L5`, gate evidence requirements, human approval requirements, external candidate gates, adapter design vs execution boundaries, source inspection gates, Git mutation boundaries, product/Siamese readiness dependency, and the ticket-level gate requirements future P8 tickets must satisfy.

P8.5 decides which future P8 tickets may move toward static implementation, local non-executing interaction surfaces, read-only metadata adapters, or future human-approved controlled execution candidates.

P8.5 does not activate runtime. P8.5 does not implement enforcement. P8.5 does not execute tools, agents, OpenCode, Graphify, GBrain, GStack, Hermes, providers, API, MCP, live connectors, or product behavior. P8.5 does not mutate Git.

## 3. Current Posture

P8.5 defines gates; it does not cross them. `P8-L4` is a future candidate level only. `P8-L5` is blocked.

| Area | Current state | P8.5 interpretation | Blocked interpretation |
| --- | --- | --- | --- |
| P8.0 boundary | P8.0 is present and accepted. | P8.5 may harden P8.0 scope levels. | Treating P8.0 as runtime approval. |
| MVP-0 | MVP-0 is a local interactive manual workflow assistant candidate. | MVP-0 may structure manual workflow only after future gates. | Product generator or autonomous runtime. |
| P8-S0/P8-L0 documentation/design | Documentation-only work is allowed. | P8.5 itself is `P8-L0`. | Implementation or execution by design document. |
| schema/static template implementation | Candidate future implementation track. | `P8-L1` may be authorized later by P8.10/P8.11. | Runtime schemas or automatic execution contracts. |
| local non-executing UI/CLI | Candidate future local interaction surface. | `P8-L2` may be authorized later as non-executing. | Command execution, dispatch, provider calls, or Git mutation. |
| read-only metadata adapters | Candidate future adapter class. | `P8-L3` requires P8.1, P8.5, boundary ticket, and explicit implementation approval. | Adapter execution or source-of-truth adoption. |
| human-approved controlled execution candidate | Future-only candidate level. | `P8-L4` can be defined but is not active. | Execution approval by P8.5. |
| autonomous runtime | Not approved. | P8-L5 autonomous runtime remains blocked. | autonomous AGENT PLATFORM as accepted behavior. |
| external inventory | P8.1 is present as path/class metadata inventory. | Inventory informs future candidate gates. | External source content inspection or adoption. |
| interaction surface | P8.2 absent. | Record `pending_P8.2_interaction_surface_alignment`. | Inventing or implementing UI/CLI in P8.5. |
| schema candidates | P8.3 absent. | Record `pending_P8.3_schema_alignment`. | Creating schemas in P8.5. |
| local state | P8.4 is present as state model. | State model informs local-only and no-persistence boundaries. | Creating state store or workspace artifacts. |
| Graphify | Read-only/imported evidence candidate. | Design/reference only until P8.6 and future gate. | Active Graphify runner, rerun, authority, or substrate. |
| GBrain | Memory architecture candidate. | Metadata compatibility candidate only. | Active GBrain runtime or persistent memory. |
| GStack | GBrain-compatible skill-stack candidate. | Compatibility inventory candidate only. | Active GStack runtime or GStack execution. |
| Hermes | Interface/runtime/orchestration candidate. | UI feasibility candidate only after P8.8. | Active Hermes runtime, Hermes orchestration, or Cadence. |
| OpenCode | H0 user-operated harness. | User manually copies prompts and pastes outputs. | Active OpenCode adapter or OpenCode execution from AGENT PLATFORM. |
| provider/auth/API/MCP | Blocked. | Boundary metadata only. | Active provider/auth/API/MCP. |
| credentials | Blocked. | No inspection, use, or configuration. | Credential access or auth setup. |
| live connectors | Blocked. | Named only as blocked surfaces. | Active live connectors. |
| product/Siamese | Siamese is product vision. | Product-bound use requires P4 / GT-09 or equivalent. | Product/Siamese source readable by default. |
| Git | User-owned. | no Git mutation by AGENT PLATFORM. | Automatic commit, automatic push, or broad staging. |

## 4. Inputs Reviewed

Review was limited to approved governance, architecture, implementation, security, and path/class metadata records. Product source, external source contents, generated output contents, secrets, credentials, datasets, models, runtime files, and local credential stores were not inspected.

| Input group | Document | Review mode | Gate model use | Limitation |
| --- | --- | --- | --- | --- |
| P8.0 scope boundary | `0_architecture/governance/agent_platform_p8_platform_mvp_scope_external_integration_boundary.md` | `p8_scope_boundary_review` | Source for P8 scope levels, MVP-0 definition, candidate classes, and blocked surfaces. | No P8.0 modification. |
| P8.1-P8.4 if present | P8.1 external inventory present; P8.4 local state model present; P8.2 absent; P8.3 absent. | `p8_sibling_alignment_review` | Aligns external inventory and local-only state posture. | Records `pending_P8.2_interaction_surface_alignment` and `pending_P8.3_schema_alignment`. |
| P7.R closure and P7 workflow docs | P7.R maturity closure and P7.0.A-P7.0.H manual workflow docs. | `manual_workflow_closure_review` | Confirms P7 manual workflow maturity and H0/manual boundaries. | Named reviewer pipeline path absent; accepted P7 reviewer mesh path is inherited from P7.R. |
| P7.0.0 / agent-native alignment docs | Agent-native organization carry-forward and bridge documents. | `agent_native_alignment_review` | Supplies manual task graph, blackboard, capability, route, and memory concepts. | Conceptual only, not runtime. |
| P7 compact pilot/runbook docs | Compact runbook and P7.3 report where present. | `manual_workflow_closure_review` | Supports local interactive manual assistant need. | Does not establish runtime readiness. |
| P6 operational contracts | Operational readiness, capability registry, communication, evidence bus, approval loop, monitoring/incident records. | `operational_contract_review` | Supplies review, incident, approval, monitoring, and evidence requirements. | No operational activation. |
| P5 skeleton baseline | Minimal active audit and implementation skeleton candidates. | `implementation_skeleton_review` | Preserves skeleton-as-candidate posture and implementation blockers. | No implementation created. |
| P3 activation decisions | Activation reconciliation and tool/provider/agent activation decisions. | `activation_decision_review` | Preserves blocked tool, provider, API, MCP, and agent runtime posture. | No activation decision changed. |
| P2/P2.K knowledge architecture | Knowledge/retrieval closure, metadata vocabulary, evidence refs, audit/retention/rollback baseline. | `metadata_contract_review` | Supplies evidence, retention, rollback, metadata, and no-live-retrieval semantics. | No retrieval runtime. |
| P1 metadata contracts | Context, provider, tool, agent, and Cognitive Semantic System hardening records. | `metadata_contract_review` | Supplies context/provider/tool/agent boundary vocabulary. | Metadata is not execution. |
| P0 gates/security/validation | Activation gate map, validation gate design, security hardening plan. | `security_policy_review` | Supplies gate and validation posture. | No security enforcement implemented. |
| S-03/S-04 policies | Tool/shell/network/MCP execution policy and local-only secrets/credentials policy. | `security_policy_review` | Supplies default no-execution, no-MCP, no-credential, and local-only rules. | No credentials inspected. |
| CSS ADR/audit | Cognitive Semantic System naming and audit records. | `metadata_contract_review` | Preserves Cognitive Semantic System naming and substrate deferral. | No substrate selected. |
| external candidates, path/class metadata only | Graphify, GBrain, GStack, Hermes, OpenCode, Codegraph if later considered. | `external_candidate_path_only_review` | Defines candidate gate defaults and inspection levels. | No source tree enumeration, content inspection, import, install, execution, or adoption. |
| blocked surfaces | Product source, external source content, credentials, generated output contents, datasets, models, runtime files. | `not_reviewed_blocked` | Preserved as blocked surfaces. | Not reviewed. |

## 5. Activation Level Model

`P8ActivationLevel` is the P8 security and activation classification for P8 design, static implementation, local non-executing surfaces, read-only metadata adapters, future controlled execution candidates, and blocked autonomous runtime.

| Level | Definition | Allowed artifacts | Blocked behavior | Minimum prerequisites | Required human approval | Allowed ticket classes | Stop rule |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `P8-L0` | Documentation/design. | Governance docs, architecture docs, boundary docs, candidate models, gate models. | Implementation, adapters, runtime, execution, source loading, product source, Git mutation. | P8.0 present for P8 work; P7.R present for manual workflow lineage. | Active task approval only. | P8.1-P8.5; P8.6-P8.9 as boundary/design unless later approved. | Stop if asked to implement or execute. |
| `P8-L1` | Schema/static template implementation. | Static schemas, static templates, markdown renderers, non-network local transformations if later approved. | Runtime execution, external calls, provider/API/MCP, live connectors, automatic dispatch, Git mutation. | P8.5 plus P8.10/P8.11 explicit authorization. | Exact implementation-scope approval. | P8.12-P8.15 only if P8.10/P8.11 authorize. | Stop if implementation exceeds static/non-executing scope. |
| `P8-L2` | Local non-executing UI/CLI. | Local UI/CLI/TUI/web shell that captures text, renders packages, accepts pasted output, displays checklists, renders CommitCandidate. | Command execution, provider/API calls, tool execution, background workers, telemetry, dispatch, reviewer assignment, Git mutation. | P8.2, P8.4, P8.5, P8.10/P8.11 authorization. | Exact local-surface approval. | P8.12-P8.16 only if synthesized and planned. | Stop if local surface executes commands or calls services. |
| `P8-L3` | Read-only metadata adapters. | Read-only metadata adapter candidates that load explicitly approved local metadata only. | Adapter execution, source-of-truth adoption, source tree traversal, runtime calls, external APIs, Graphify rerun, GBrain/GStack/Hermes/OpenCode execution. | P8.1, P8.5, specific boundary ticket P8.6/P8.7/P8.8/P8.9, and later explicit implementation approval. | Exact adapter-surface approval and security review. | Future implementation tickets after boundary approval. | Stop if adapter reads source content, calls runtime, or becomes authority. |
| `P8-L4` | Human-approved controlled execution candidate. | Future request records and exact action candidates only. | Execution by P8.5, broad credentials, silent providers, implicit tool/runtime permission, uncontrolled side effects. | P8.R or later readiness, external boundary, security review, audit/retention/rollback/incident model, exact action scope. | Explicit scope-bound human approval. | Future post-P8 candidate gate only. | Stop until exact gate approves exact action. |
| `P8-L5` | Autonomous runtime, blocked. | None. | Autonomous orchestration, automatic dispatch, automatic reviewer assignment, automatic integration, autonomous provider/tool/agent execution, automatic Git, Cadence. | Not available in P8 MVP-0. | Not available. | None in P8. | Stop and report blocked runtime request. |

Decisions:

- P8.5 itself is `P8-L0`.
- P8.1-P8.5 are `P8-L0`/design only.
- P8.10/P8.11 may authorize a `P8-L1`/`P8-L2` implementation plan if all gates remain clean.
- P8.12+ may implement only what P8.10/P8.11 authorize.
- `P8-L3` read-only metadata adapters require P8.1, P8.5, specific boundary ticket P8.6/P8.7/P8.8/P8.9, and later explicit implementation approval.
- `P8-L4` may be defined only as future candidate level and is not active in P8.5.
- P8-L5 autonomous runtime remains blocked.

## 6. Gate Object Model

Gate objects are metadata only. They are not enforcement runtime, permission grants, approval automation, provider activation, tool execution, or Git mutation.

| Object | Meaning | Required fields | Forbidden fields | Allowed use | Blocked interpretation |
| --- | --- | --- | --- | --- | --- |
| `ActivationGateRecord` | Metadata record defining a gate for a target surface and level. | `gate_id`, `target_level`, `target_surface`, `current_status`, evidence, review, approval, blocked surfaces, policies, stop rules. | Credential values, executable commands as approvals, broad path grants, provider tokens. | Define gate conditions and blockers. | Automatic gate opening. |
| `GateDecision` | Decision vocabulary for a gate claim. | Decision value, rationale, evidence ref, limitation. | Runtime permission, provider auth, Git command execution. | Classify allowed/deferred/blocked posture. | Approval to execute. |
| `GateStatus` | Status vocabulary for gate lifecycle. | Status value, date, owner/ref, limitation. | Hidden approval state or inferred execution permission. | Track design or implementation readiness. | Runtime authorization. |
| `GateEvidencePackage` | Evidence metadata package required by a gate. | Evidence refs, source class, scope, limitation, reviewer/security refs. | Secret values, raw external contents, generated output dumps, credential paths beyond safe metadata. | Support review. | Evidence deciding by itself. |
| `RequiredHumanApproval` | Scope-bound approval metadata requirement. | Approver, exact surface, allowed action, blocked actions, evidence package, date. | Implied approval, broad tool permission, open-ended credentials. | Record required approval conditions. | Automatic approval. |
| `BlockedSurface` | Named surface that remains blocked. | Surface name, reason, default status, future gate, stop rule. | Workaround, exception without approval, hidden allowlist. | Preserve denied defaults. | Future permission by being named. |
| `SecurityReviewRequirement` | Required security review metadata. | Surface, review type, evidence, reviewer/authority, blocker list, escalation gate. | Secret values, auth tests, scanner output by default. | Define security preconditions. | Security enforcement implementation. |
| `ExternalCandidateGate` | Gate metadata for external candidates. | Candidate, default level, allowed path, blocked shortcuts, required future tickets. | Source content adoption, runtime adoption, license conclusions without review. | Route external candidates safely. | External dependency approval. |
| `ExternalInspectionGate` | Gate metadata for source/content inspection levels. | Inspection level, allowed scope, blocked scope, approval, eligible tickets. | Broad recursive inspection, import/install/run permission. | Define inspection escalation. | Permission to inspect contents by path presence. |
| `AdapterActivationBoundary` | Boundary between adapter design, metadata read, execution, runtime, and product use. | Category, status, allowed future level, blocked use, required gates. | Executable adapter grants, credentials, source-of-truth claims. | Separate design from execution. | Adapter implementation or adapter execution approval. |
| `RuntimeEscalationRequest` | Metadata request to move a surface toward execution/runtime. | Request id, target surface, requested/current level, reason, evidence, security, approval, rollback, incident route, blockers. | Approval itself, broad tool commands, credentials. | Record an escalation request. | Permission to execute. |
| `GitMutationBoundary` | Boundary for Git advisory vs mutation. | Allowed advisory behavior, blocked mutation, exact-path command requirement, stop rules. | `git add .`, automatic staging, commit, push, force-add. | Preserve user Git authority. | Agent Git permission. |
| `ProductReadinessGateRef` | Reference to future product/Siamese readiness gate. | Product scenario, required gate, blocked shortcut, limitation. | Product source grants, product execution commands. | Defer product-bound use to P4 / GT-09 or equivalent. | Product activation. |

## 7. ActivationGateRecord Contract

`ActivationGateRecord` defines a gate; it does not open it automatically.

| Field | Meaning |
| --- | --- |
| `gate_id` | Stable identifier for the gate record. |
| `gate_label` | Human-readable gate label. |
| `target_level` | Target `P8ActivationLevel`. |
| `target_surface` | Surface governed by the gate. |
| `current_status` | Current `GateStatus`. |
| `required_inputs` | Required prior tickets, documents, decisions, and policies. |
| `required_evidence_package` | Required `GateEvidencePackage`. |
| `required_security_review` | Required `SecurityReviewRequirement`. |
| `required_human_approval` | Required `RequiredHumanApproval`. |
| `required_boundary_docs` | Required boundary documents before escalation. |
| `blocked_surfaces` | Applicable `BlockedSurface` values. |
| `allowed_actions` | Narrow actions allowed at the current gate level. |
| `blocked_actions` | Actions that remain blocked. |
| `source_inspection_policy` | External/product/source inspection policy. |
| `adapter_policy` | Adapter design, read-only, execution, runtime, or product posture. |
| `runtime_policy` | Runtime and execution posture. |
| `git_policy` | Git advisory/mutation posture. |
| `product_readiness_refs` | `ProductReadinessGateRef` entries if product-bound. |
| `retention_refs` | Retention requirements or inherited baselines. |
| `rollback_refs` | Rollback requirements or inherited baselines. |
| `incident_refs` | Incident route requirements or inherited baselines. |
| `limitations` | Known absences, pending alignments, and blocked assumptions. |
| `stop_rules` | Conditions that require stop/report instead of proceeding. |

## 8. GateDecision / GateStatus Vocabulary

`GateDecision` values:

| GateDecision | Meaning |
| --- | --- |
| `allowed_at_current_level` | Allowed within the current gate level only. |
| `allowed_as_design_only` | Allowed only as documentation/design. |
| `allowed_as_static_schema_only` | Allowed only as static schema/template work after authorization. |
| `allowed_as_local_non_executing_surface_only` | Allowed only as local UI/CLI surface with no execution. |
| `allowed_as_read_only_metadata_candidate` | Allowed only as read-only metadata candidate after gates. |
| `deferred_to_future_gate` | Deferred to a later gate/ticket. |
| `blocked` | Not allowed. |
| `requires_human_approval` | Requires explicit scope-bound human approval. |
| `requires_security_review` | Requires security review before escalation. |
| `requires_external_review` | Requires external candidate/source review gate. |
| `requires_product_readiness` | Requires P4 / GT-09 or equivalent product readiness gate. |
| `requires_p8_synthesis` | Requires P8.10 synthesis. |
| `requires_implementation_plan` | Requires P8.11 or equivalent implementation plan. |
| `out_of_scope` | Outside this ticket or P8 MVP-0 scope. |

`GateStatus` values:

| GateStatus | Meaning |
| --- | --- |
| `not_started` | No gate work has started. |
| `metadata_only` | Safe metadata only. |
| `design_only` | Documentation/design only. |
| `candidate` | Candidate status without approval. |
| `blocked` | Blocked by default. |
| `deferred` | Deferred to future ticket/gate. |
| `pending_alignment` | Waiting for sibling/prerequisite alignment. |
| `requires_review` | Requires review before escalation. |
| `approved_for_design` | Approved for design only. |
| `approved_for_static_implementation` | Approved for static implementation only. |
| `approved_for_local_non_executing_surface` | Approved for local non-executing surface only. |
| `not_approved_for_execution` | Execution is not approved. |
| `not_approved_for_runtime` | Runtime is not approved. |
| `rejected` | Rejected or not accepted. |

No status value approves autonomous runtime or Git mutation.

## 9. P8-L0 Documentation / Design Gate

`P8-L0` allows governance docs, boundary docs, architecture docs, schema candidate docs, state model docs, and gate model docs.

`P8-L0` blocks implementation, adapters, runtime, source inspection, tool execution, provider/API/MCP, Git mutation, and product source.

| Allowed artifact | Required evidence | Blocked shortcut | Future escalation path |
| --- | --- | --- | --- |
| Governance document | P8.0 prerequisite and relevant upstream policy refs. | Treating document as enforcement. | P8.10/P8.11 synthesis and plan if implementation is needed. |
| Boundary document | Named surface, allowed/blocked matrix, stop rules. | Treating boundary as adapter. | Specific boundary ticket plus future gate. |
| Architecture document | Current posture, non-action statement, limitations. | Implementing local files or runtime. | P8.10 synthesis. |
| Schema candidate document | Object names and field candidates only. | Creating schema files. | `P8-L1` after P8.10/P8.11. |
| State model document | Local-only state concepts only. | Creating state store or workspace artifacts. | `P8-L1`/`P8-L2` after P8.10/P8.11. |
| Gate model document | Gate metadata and blocker definitions. | Implementing security enforcement. | Future hardening/schema candidate ticket. |

## 10. P8-L1 Schema / Static Template Implementation Gate

`P8-L1` may allow future implementation of static schemas, dataclass/pydantic candidates if approved later, markdown template renderers, static validators that do not execute external tools, and non-network local transformations.

`P8-L1` blocks runtime execution, external tool calls, provider/API/MCP, live connectors, automatic dispatch, automatic integration, Git mutation, and source loading by default.

P8.5 does not authorize `P8-L1` implementation directly; P8.10/P8.11 must explicitly authorize it.

| Candidate artifact | Allowed only if | Blocked behavior | Required future ticket |
| --- | --- | --- | --- |
| Static schema file | P8.3 schema candidates exist and P8.10/P8.11 authorize exact implementation. | Runtime schema execution or provider calls. | P8.11 then P8.12+. |
| Dataclass/pydantic candidate | Approved as static/local only with no runtime activation. | Validation command execution by default. | P8.11 implementation plan. |
| Markdown template renderer | Renders local text only. | Tool execution, API calls, automatic dispatch. | P8.13 if authorized. |
| Static validator | Does not execute external tools, providers, scripts, builds, tests, or source loading. | Runtime validation, CI, tests, package managers. | Future exact validation gate. |
| Non-network local transformation | Bounded local text/object transformation only. | Network, provider/API/MCP, telemetry, background workers. | P8.11/P8.13 if authorized. |

## 11. P8-L2 Local Non-Executing UI / CLI Gate

`P8-L2` may allow a future local UI/CLI/TUI/web shell that captures text, renders packages, accepts pasted output, displays checklists, and renders `CommitCandidate`.

`P8-L2` blocks command execution, provider/API calls, tool execution, background workers, telemetry, automatic dispatch, automatic reviewer assignment, and Git mutation.

`P8-L2` remains non-executing.

| Local surface function | Allowed only if | Blocked behavior | Required future ticket |
| --- | --- | --- | --- |
| Capture user objective | Local text capture only, no source loading. | Product source inspection, automatic task creation. | P8.2 then P8.10/P8.11. |
| Render WorkPacket/HarnessInputPackage | Static rendering from user-provided text and approved metadata. | Automatic dispatch or harness execution. | P8.13 if authorized. |
| Accept pasted output | User-pasted text only. | OpenCode execution or provider/API fetch. | P8.14 if authorized. |
| Display review checklist | Manual checklist rendering. | Automatic reviewer assignment or auto-review. | P8.14 if authorized. |
| Display integration checklist | Manual checklist rendering. | Automatic integration or file edits by checklist. | P8.15 if authorized. |
| Render CommitCandidate | Exact-path advisory only. | Git staging, commit, push, force-add. | P8.15 if authorized. |

## 12. P8-L3 Read-Only Metadata Adapter Gate

`P8-L3` may allow future read-only metadata adapter candidates that load explicitly approved local metadata, not external source content by default.

`P8-L3` blocks adapter execution, source-of-truth adoption, source tree traversal, runtime calls, external API calls, Graphify rerun, GBrain runtime, GStack execution, Hermes runtime, and OpenCode execution.

| Adapter candidate | Allowed read-only metadata | Blocked content | Required boundary ticket | Required future gate |
| --- | --- | --- | --- | --- |
| Graphify read-only evidence candidate | Curated evidence refs and approved metadata summaries. | Raw generated output contents, source-of-truth claims, rerun outputs. | P8.6 | `P8-L3` implementation approval after P8.6/P8.10/P8.11. |
| GBrain/GStack metadata compatibility candidate | Candidate names, compatible metadata fields, memory architecture notes. | GBrain source, GStack source, runtime memory, vector/graph DB content. | P8.7 | Explicit read-only metadata gate. |
| Hermes UI metadata candidate | Interface feasibility metadata and blocked runtime refs. | Hermes source, runtime, orchestration, Cadence. | P8.8 | Explicit read-only metadata gate. |
| OpenCode H1 metadata adapter candidate | Harness metadata, package names, user-paste boundaries. | OpenCode execution, command invocation, adapter execution. | P8.9 | Explicit H1 metadata gate. |

## 13. P8-L4 Human-Approved Controlled Execution Candidate Gate

`P8-L4` is a future-only level. It requires explicit human approval, P8.R or later readiness, external candidate boundary, security review, audit/retention/rollback/incident model, exact action scope, no broad credentials, no silent provider/API/MCP activation, rollback plan, and stop rule.

P8.5 defines `P8-L4` as a future candidate level only. P8.5 does not authorize any `P8-L4` execution.

| Execution candidate | Minimum prerequisites | Required human approval | Blocked until | Stop rule |
| --- | --- | --- | --- | --- |
| Exact local command candidate | P8.R or later readiness, command-specific security review, rollback/incident route. | Explicit command and exact path/scope approval. | Future execution gate. | Stop if command is broad, generated, or side effects unclear. |
| OpenCode execution candidate | P8.9 boundary, security review, user approval, audit/rollback/incident model. | Explicit exact action approval. | Future gate after P8.R or later. | Stop if AGENT PLATFORM would execute OpenCode. |
| External adapter execution candidate | External review gate, license/security review, exact adapter boundary. | Explicit adapter/action approval. | Future external execution gate. | Stop if source content or runtime is assumed safe by path. |
| Provider/API/MCP candidate | Provider/auth/security gate, data policy, cost/retention policy. | Explicit secure provider/API/MCP approval. | Future provider/auth/API/MCP gate. | Stop if credentials or endpoint use is implicit. |
| Git automation candidate | Outside P8 MVP-0. | Not available in P8. | Post-P8 explicit Git governance if ever considered. | Stop; user owns Git. |

## 14. P8-L5 Autonomous Runtime Gate

`P8-L5` is blocked.

Autonomous runtime is outside P8 MVP-0. There is no automatic orchestration, no automatic dispatch, no automatic reviewer assignment, no automatic integration, no automatic Git, no autonomous provider/tool/agent execution, and no Cadence.

P8-L5 autonomous runtime remains blocked and cannot be opened by P8.5.

## 15. Blocked Surface Matrix

| Blocked surface | Default status | Allowed design-only reference | Required future gate | Stop rule |
| --- | --- | --- | --- | --- |
| provider/auth/API/MCP | Blocked. | Boundary metadata only. | Future provider/auth/API/MCP gate. | Stop before auth, API, MCP, or provider action. |
| credentials/secrets/`.env` | Blocked. | Safe category mention only. | Secure credentials gate. | Stop before inspection, use, or configuration. |
| tool execution | Blocked. | Tool metadata only. | Exact execution gate. | Stop before invoking tools. |
| agent execution | Blocked. | Agent role metadata only. | Agent runtime gate. | Stop before running agents. |
| task/handoff execution | Blocked. | WorkPacket/HarnessPackage metadata only. | Runtime/handoff gate. | Stop before automatic dispatch or handoff. |
| OpenCode adapter execution | Blocked. | H0/H1 boundary metadata. | P8.9 plus future execution gate. | Stop before OpenCode invocation. |
| Graphify automatic rerun | Blocked. | Graphify candidate metadata. | P8.6 plus future exact gate. | Stop before Graphify execution or `/graphify`. |
| Graphify as source of truth | Blocked. | Supporting evidence reference only. | Governance evidence review. | Stop if Graphify is treated as authority. |
| GBrain runtime | Blocked. | Memory architecture candidate. | P8.7 plus runtime gate. | Stop before runtime activation. |
| GBrain persistent memory | Blocked. | Memory model metadata only. | Storage/memory gate. | Stop before persistence or retrieval. |
| GStack execution | Blocked. | Compatibility candidate metadata. | P8.7 plus execution gate. | Stop before executing GStack. |
| Hermes runtime | Blocked. | Interface candidate metadata. | P8.8 plus runtime gate. | Stop before runtime activation. |
| Hermes orchestration | Blocked. | Orchestration candidate as blocked/future only. | Runtime/orchestration gate. | Stop before automatic orchestration. |
| Cadence | Blocked. | Future always-on runtime candidate only. | Explicit Cadence gate. | Stop before scheduler/always-on activation. |
| live connectors | Blocked. | Connector boundary metadata only. | Connector security gate. | Stop before connection. |
| product/Siamese source | Blocked by default. | Product vision metadata only. | P4 / GT-09 or equivalent. | Stop before product source inspection. |
| external source content inspection | Blocked by default. | EI-0/EI-1 metadata only. | External review gate EI-3+. | Stop before opening source contents. |
| source loading | Blocked. | SourceRef metadata only. | Source loading gate. | Stop before loading content. |
| persistence DB | Blocked. | Storage candidate metadata only. | Persistence gate. | Stop before creating database. |
| vector DB / embeddings | Blocked. | Candidate concept only. | CSS/storage gate. | Stop before embeddings or vector DB. |
| graph DB / ontology runtime | Blocked. | Candidate concept only. | CSS/storage gate. | Stop before graph DB or ontology runtime. |
| telemetry / event streaming | Blocked. | Incident/audit posture only. | Telemetry/event gate. | Stop before instrumentation or streaming. |
| generated output tracking | Blocked. | Generated artifact metadata only. | Tracking approval gate. | Stop before approving generated output tracking. |
| source tracking expansion | Blocked. | SourceRef metadata only. | Source tracking gate. | Stop before expanding tracking. |
| publication | Blocked. | Publication blocker metadata. | Publication gate. | Stop before publishing. |
| Git mutation | Blocked. | Exact-path advisory only. | Human Git action only. | Stop before staging, commit, push, force-add. |
| `git add .` | Blocked. | Prohibited example only. | None in P8. | Never recommend git add . |

## 16. External Candidate Gate Matrix

| Candidate | P8.5 default level | Allowed gate path | Blocked shortcuts | Required future tickets |
| --- | --- | --- | --- | --- |
| Graphify | `P8-L0` design. | Future `P8-L3` read-only evidence only after P8.6 and explicit implementation plan. | Rerun, `/graphify`, source of truth, authority, substrate. | P8.6, P8.10/P8.11, later explicit implementation approval. |
| GBrain | `P8-L0` design. | Future metadata compatibility only after P8.7. | Runtime, persistent memory, vector/graph DB, automatic retrieval. | P8.7, later exact gate. |
| GStack | `P8-L0` design. | Future compatibility inventory only after P8.7. | Execution, adoption, bootstrap runtime. | P8.7, later exact gate. |
| Hermes | `P8-L0` design. | UI feasibility candidate after P8.8. | Runtime, Cadence, automatic dispatch, orchestration. | P8.8, later exact gate. |
| OpenCode | H0 user-operated harness. | Future H1 metadata adapter candidate after P8.9. | Active OpenCode adapter, OpenCode execution from AGENT PLATFORM. | P8.9, later exact gate. |
| Codegraph | Not adopted. | Future EXT review required. | Codegraph execution, adoption, authority. | Future EXT.* or explicit review gate. |
| provider/model APIs | Blocked. | Boundary metadata only. | API/provider activation, auth, credential use. | Future provider/auth/API gate. |
| MCP servers/tools/resources | Blocked. | Boundary metadata only. | MCP activation, listing, connecting, invoking. | Future MCP gate. |
| live connectors | Blocked. | Boundary metadata only. | Active connectors or background sync. | Future connector gate. |
| product/Siamese integrations | Deferred. | P4 / GT-09 or equivalent product readiness. | Product source inspection, product generator, product execution. | P4 / GT-09 or equivalent. |
| Git tools | User manual Git only. | Advisory exact-path command rendering only. | Agent staging, commit, push, force-add, `git add .`. | Human action outside AGENT PLATFORM. |

## 17. External Inspection Gate

`ExternalInspectionGate` defines external candidate inspection levels. Path presence is not content inspection permission. Path presence is not dependency approval.

| Inspection level | Allowed scope | Blocked scope | Required approval | Eligible tickets |
| --- | --- | --- | --- | --- |
| `EI-0` | Named candidate only. | Path traversal, content, install, import, execution. | Active task scope. | P8.0, P8.1, P8.5. |
| `EI-1` | Path existence only. | Directory tree enumeration or file content. | Active task scope and exact path. | P8.1 and path-only checks referenced by P8.5. |
| `EI-2` | Shallow top-level metadata inventory. | Source content, dependency execution, recursive inspection. | Explicit external inventory approval. | P8.1 may propose rules. |
| `EI-3` | Controlled documentation/source review. | Broad source mining, secrets, generated outputs, execution. | Explicit external review gate. | Future P8/EXT review ticket. |
| `EI-4` | Adapter design. | Adapter implementation or execution. | Adapter design approval. | P8.6-P8.9 or later. |
| `EI-5` | Adapter execution. | Runtime adoption, broad credentials, silent providers. | Future exact execution gate. | Blocked by default. |
| `EI-6` | Runtime adoption. | Autonomous runtime or product adoption by default. | Future activation-level review. | Blocked by default. |

P8.5 allows `EI-0` and references `EI-1` as path-only if already checked by allowed commands. `EI-3+` require explicit external review gate. `EI-5` and `EI-6` remain blocked by default.

## 18. Adapter Activation Boundary

`AdapterActivationBoundary` separates adapter design, metadata read, execution, runtime, and product use. Adapter execution remains blocked unless a future exact gate authorizes it.

| Adapter category | P8.5 status | Allowed future level | Blocked use | Required gates |
| --- | --- | --- | --- | --- |
| Static adapter contract | Design only. | `P8-L0`/`P8-L1` after authorization. | Runtime behavior or external calls. | P8.10/P8.11 and exact implementation plan. |
| Metadata-only adapter design | Design only. | `P8-L0`. | Loading external source content. | Candidate boundary ticket. |
| Read-only metadata adapter candidate | Future candidate. | `P8-L3`. | Execution, source-of-truth adoption, source tree traversal. | P8.1, P8.5, P8.6-P8.9, implementation approval. |
| Controlled execution adapter candidate | Future-only. | `P8-L4`. | Execution by P8.5 or implicit approval. | P8.R or later, security review, human approval, rollback/incident model. |
| Runtime adapter | Blocked. | None in P8 MVP-0. | Runtime activation or automation. | Future activation review only. |
| Product adapter | Deferred. | Product readiness gate. | Product/Siamese source or product execution by default. | P4 / GT-09 or equivalent. |

## 19. Human Approval Model

Approval must be explicit, scope-bound, name the target surface, name the allowed action, name blocked actions, include an evidence package, include rollback/incident posture for execution candidates, and cannot be inferred from user intent alone.

ApprovalRef is not approval. Reviewer verdict is not approval. Validation success is not approval. Security review is not approval. Registry presence is not approval.

| Approval event | Required approver | Required evidence | Blocked inference |
| --- | --- | --- | --- |
| Design approval | User or named governance authority. | Scope doc, blocked surfaces, limitations. | Design approval means implementation approval. |
| Static implementation approval | User with exact ticket scope. | P8.10/P8.11 plan, target paths, rollback posture. | Schema/static work means runtime permission. |
| Local non-executing surface approval | User with exact surface scope. | UI/CLI function list, no-execution proof, Git boundary. | Local UI means command execution. |
| Read-only metadata adapter approval | User plus security/external review if applicable. | Candidate boundary, metadata scope, source inspection policy. | Adapter presence means source-of-truth or execution. |
| Controlled execution candidate approval | User with explicit exact-action approval. | Evidence package, security review, rollback, incident route, stop rule. | ApprovalRef, reviewer verdict, or validation result means execution approval. |
| Git action approval | User only. | Exact paths and commit intent. | CommitCandidate means Git approval. |

## 20. Security Review Requirement Model

| Surface | Required security review | Blocked shortcut | Escalation gate |
| --- | --- | --- | --- |
| credentials/secrets | Secure handling review before any access. | Inspecting `.env`, token stores, API keys, browser auth, or local credential stores. | Secure credential gate. |
| provider/auth/API/MCP | Auth, data, endpoint, cost, retention, and MCP exposure review. | Provider metadata or MCP availability as activation. | Provider/auth/API/MCP gate. |
| external source inspection | Provenance/license/security/scope review. | Path presence as content permission. | `ExternalInspectionGate` `EI-3+`. |
| tool execution | Exact command, side effects, rollback, output handling review. | Tool metadata as execution permission. | Runtime/execution gate. |
| agent execution | Agent role, authority, context, dispatch, review, rollback review. | Agent metadata as execution permission. | Agent runtime gate. |
| local UI/CLI | No-execution, local-only, no telemetry, no background worker review. | CLI availability as command permission. | `P8-L2` approval. |
| state files | Local-only, retention, sensitivity, publication, cleanup review. | State model as state store creation. | P8.4/P8.10/P8.11. |
| generated artifacts | Generated-sensitive review and tracking approval. | Treating generated output as source. | Generated artifact gate. |
| Graphify evidence | Evidence/support-only and no-rerun review. | Graphify as authority or substrate. | P8.6. |
| GBrain/GStack memory candidates | Memory persistence, retrieval, vector/graph DB, source scope review. | GBrain/GStack metadata as runtime. | P8.7. |
| Hermes runtime/UI candidate | Interface vs runtime, orchestration, Cadence, dispatch review. | Hermes UI candidate as runtime. | P8.8. |
| OpenCode harness upgrade | H0/H1 boundary, user copy/paste, no execution review. | Harness package as OpenCode invocation. | P8.9. |
| Git command rendering | Exact-path advisory, no mutation, no broad staging review. | `git add .` or automatic Git. | `GitMutationBoundary`. |
| product/Siamese boundary | Product readiness, source scope, product security review. | Siamese vision as product source permission. | P4 / GT-09 or equivalent. |

## 21. Runtime Escalation Request Model

`RuntimeEscalationRequest` records a request; it does not approve escalation.

| Field | Meaning |
| --- | --- |
| `request_id` | Stable identifier for the request. |
| `target_surface` | Surface proposed for escalation. |
| `requested_level` | Requested `P8ActivationLevel`. |
| `current_level` | Current `P8ActivationLevel`. |
| `reason` | Why escalation is requested. |
| `required_evidence` | Evidence needed before review. |
| `required_security_review` | Required security review. |
| `required_human_approval` | Required explicit approval. |
| `required_boundary_docs` | Boundary docs required before decision. |
| `required_rollback_plan` | Rollback posture required for execution candidates. |
| `required_incident_route` | Incident route required for execution candidates. |
| `blocked_surfaces` | Surfaces that remain blocked. |
| `decision_status` | Current `GateDecision`/`GateStatus`. |
| `limitations` | Known blockers and exclusions. |

## 22. Git Mutation Boundary

`GitMutationBoundary` preserves user Git authority.

AGENT PLATFORM may render `CommitCandidate` in a future MVP. AGENT PLATFORM may render exact `CommitCommandBlock`. AGENT PLATFORM must not mutate Git. The user performs Git manually. Never recommend git add .

`CommitCandidate` does not imply approval. Reviewer verdict does not imply Git approval. Integrator acceptance does not imply Git mutation. Any future Git automation is out of P8 MVP-0 scope.

Required command pattern for user-only advisory rendering:

```powershell id="0unkpk"
git status --short

git add <exact_path_1> `
        <exact_path_2>

git commit -m "<exact ticket message>"

git push origin main
```

| Git surface | Allowed future MVP behavior | Blocked behavior | Stop rule |
| --- | --- | --- | --- |
| Status inspection | Render/read `git status --short` when scoped. | Treat status as semantic approval. | Stop if status requires broad or unrelated handling. |
| CommitCandidate | Exact-path advisory metadata. | Automatic staging or approval. | Stop before Git mutation. |
| CommitCommandBlock | Exact-path command text for user. | Running commands by AGENT PLATFORM. | Stop before executing Git command. |
| Staging | User manual only. | Agent staging, force-add, `git add .`. | Stop and report blocked Git mutation. |
| Commit | User manual only. | Agent commit or amend. | Stop and report blocked Git mutation. |
| Push | User manual only. | Agent push or publication. | Stop and report blocked Git mutation. |

## 23. Product / Siamese Readiness Gate

Siamese is product vision, not product activation. P8 MVP is AGENT PLATFORM interaction layer, not product generator. P8.5 does not inspect product/Siamese source. Product/Siamese source is blocked by default. Product-bound work requires P4 / GT-09 or equivalent product readiness gate. `ProductReadinessGateRef` may be referenced but not opened by P8.5.

| Product-bound scenario | P8.5 decision | Blocked shortcut | Future gate |
| --- | --- | --- | --- |
| Product source inspection | Blocked by default. | Siamese vision as source permission. | P4 / GT-09 or equivalent. |
| Product generator | Out of P8 MVP-0 scope. | MVP-0 as product generator. | Product readiness gate. |
| Product-bound adapter | Deferred. | Product adapter by AGENT PLATFORM MVP. | Product readiness and adapter gate. |
| Product execution/build/test | Blocked. | Product readiness inferred from P8. | Product validation/security gate. |
| Product publication | Blocked. | Publication from MVP readiness. | Publication/product gate. |

## 24. P8 Ticket-Level Gate Requirements

| Future ticket | Allowed maximum level | Required inputs | Blocked actions | Gate notes |
| --- | --- | --- | --- | --- |
| P8.1 External Source Inventory / Classification | `P8-L0` | P8.0; path/class metadata only. | Source content inspection, execution, adoption. | Present; informs P8.5 external gates. |
| P8.2 MVP Interaction Surface Architecture | `P8-L0` | P8.0; P7 manual workflow. | CLI/TUI/web implementation. | Pending alignment. |
| P8.3 Core Workflow Schema Candidates | `P8-L0` | P8.0; P7 packages; P2/P1 metadata. | Schema file creation. | Pending alignment. |
| P8.4 Local Workspace / State Model | `P8-L0` | P8.0; P7/P6/P2 local-only posture. | State store, workspace artifacts, DB. | Present; informs local-only posture. |
| P8.6 Graphify Read-Only Evidence Boundary | `P8-L0` unless later authorized | P8.1, P8.5. | Graphify rerun, raw output inspection, authority. | May define boundary only. |
| P8.7 GBrain / GStack Memory Compatibility Boundary | `P8-L0` unless later authorized | P8.1, P8.5. | GBrain runtime, GStack execution, persistent memory. | May define compatibility boundary only. |
| P8.8 Hermes Interface / Runtime Candidate Boundary | `P8-L0` unless later authorized | P8.1, P8.5. | Hermes runtime, orchestration, Cadence. | May define interface/runtime candidate boundary only. |
| P8.9 OpenCode Harness Upgrade Boundary | `P8-L0` unless later authorized | P8.1, P8.5, P7.0.E. | OpenCode execution from AGENT PLATFORM. | May define H0/H1 boundary only. |
| P8.10 MVP-0 Architecture Synthesis | `P8-L0`, may propose `P8-L1`/`P8-L2` | P8.1-P8.5 and P8.6-P8.9 if available. | Implementation by synthesis. | Synthesis may recommend implementation scope. |
| P8.11 MVP-0 Implementation Plan | `P8-L0`, may authorize `P8-L1`/`P8-L2` plan | P8.10, P8.5 gates, security reviews. | Runtime, adapters, Git mutation. | Plan must name exact non-executing implementation. |
| P8.12 MVP-0 Skeleton Package | `P8-L1`/`P8-L2` only if authorized | P8.10/P8.11. | Runtime activation, provider/API/MCP, state DB. | May implement only non-executing authorized skeleton. |
| P8.13 WorkPacket / Harness Package Renderer | `P8-L1`/`P8-L2` only if authorized | P8.3, P8.10/P8.11. | Harness execution, OpenCode invocation. | Static rendering only if approved. |
| P8.14 HarnessOutput Intake / Review Checklist | `P8-L1`/`P8-L2` only if authorized | P8.2/P8.3/P8.10/P8.11. | Auto-review, automatic reviewer assignment. | User-pasted output only. |
| P8.15 Integrator / CommitCandidate Renderer | `P8-L1`/`P8-L2` only if authorized | P8.3/P8.5/P8.10/P8.11. | Git mutation, automatic integration. | Exact-path advisory only. |
| P8.16 MVP-0 Manual Pilot | `P8-L2` manual pilot only if authorized | P8.12-P8.15 if authorized and implemented. | Runtime execution, autonomous operation. | Manual pilot using approved non-executing surfaces only. |
| P8.R Platform MVP Readiness Closure | `P8-L0` readiness closure | P8.1-P8.16 as applicable. | Autonomy activation. | Decides readiness; it does not activate autonomy. |

## 25. Evidence / Retention / Rollback / Incident Requirements

P8.5 does not implement retention, rollback, incident handling, logging, telemetry, or persistence automation.

| Gate level | Evidence requirement | Retention posture | Rollback posture | Incident posture | Publication blocker |
| --- | --- | --- | --- | --- | --- |
| Design-only gates | Inputs reviewed, decisions, blockers, pending alignments. | Governance doc retained in repo if user commits. | Revert doc by exact path if needed. | Report boundary drift. | No publication by P8.5. |
| Schema/static template implementation | P8.10/P8.11 authorization, exact paths, static-only proof. | Local source files only if approved. | Exact-path revert/removal plan. | Report validation/security drift. | No publication without gate. |
| Local non-executing UI/CLI | No-execution proof, UI/CLI function matrix, Git boundary. | Local-only artifacts by default. | Disable/remove exact surface. | Report execution or data exposure drift. | No publication without gate. |
| Read-only metadata adapters | Candidate boundary, approved metadata scope, source inspection policy. | Metadata refs only; no raw external/source content by default. | Disable adapter/read path. | Report unexpected content or execution drift. | No external publication without review. |
| Future controlled execution candidates | Evidence package, security review, human approval, exact action, rollback and incident route. | Execution evidence local-only until reviewed. | Exact rollback plan required. | Incident route required before execution. | Publication blocked by default. |

## 26. Stop Rules

| Stop trigger | Required response |
| --- | --- |
| runtime activation request | Stop and report `runtime_activation_blocked`. |
| autonomous orchestration request | Stop and report `autonomous_orchestration_blocked`. |
| automatic dispatch request | Stop and report `automatic_dispatch_blocked`. |
| automatic reviewer assignment request | Stop and report `automatic_reviewer_assignment_blocked`. |
| automatic integration request | Stop and report `automatic_integration_blocked`. |
| automatic commit/push request | Stop and report `git_mutation_blocked`. |
| OpenCode execution request | Stop and report `opencode_execution_blocked`. |
| OpenCode adapter implementation request | Stop and report `opencode_adapter_implementation_blocked`. |
| Graphify execution request | Stop and report `graphify_execution_blocked`. |
| Graphify rerun request | Stop and report `graphify_rerun_blocked`. |
| Graphify as source of truth request | Stop and report `graphify_authority_blocked`. |
| GBrain runtime request | Stop and report `gbrain_runtime_blocked`. |
| GBrain persistent memory activation request | Stop and report `gbrain_persistent_memory_blocked`. |
| GStack execution request | Stop and report `gstack_execution_blocked`. |
| Hermes runtime request | Stop and report `hermes_runtime_blocked`. |
| Hermes orchestration request | Stop and report `hermes_orchestration_blocked`. |
| Cadence request | Stop and report `cadence_blocked`. |
| provider/auth/API/MCP activation request | Stop and report `provider_auth_api_mcp_blocked`. |
| credential request | Stop and report `credentials_blocked`. |
| API call request | Stop and report `api_call_blocked`. |
| MCP activation request | Stop and report `mcp_activation_blocked`. |
| live connector request | Stop and report `live_connector_blocked`. |
| product/Siamese source request | Stop and report `product_siamese_source_blocked`. |
| external source content inspection request | Stop and report `external_source_content_inspection_blocked`. |
| source loading request | Stop and report `source_loading_blocked`. |
| source inspection request | Stop and report `source_inspection_blocked`. |
| tool execution request | Stop and report `tool_execution_blocked`. |
| agent execution request | Stop and report `agent_execution_blocked`. |
| persistence DB request | Stop and report `persistence_db_blocked`. |
| vector DB request | Stop and report `vector_db_blocked`. |
| graph DB request | Stop and report `graph_db_blocked`. |
| telemetry/event streaming request | Stop and report `telemetry_event_streaming_blocked`. |
| generated output tracking request | Stop and report `generated_output_tracking_blocked`. |
| source tracking expansion request | Stop and report `source_tracking_expansion_blocked`. |
| publication request | Stop and report `publication_blocked`. |
| Cognitive Semantic System substrate selection request | Stop and report `css_substrate_selection_blocked`. |
| Git mutation by agent request | Stop and report `git_mutation_blocked`. |
| `git add .` recommendation request | Stop and report `git_add_dot_blocked`. |
| request to create P8.1+ files in this ticket | Stop and report `out_of_scope_file_creation_blocked`. |
| request to implement MVP package in this ticket | Stop and report `mvp_package_implementation_blocked`. |
| request to approve P8-L4 execution in this ticket | Stop and report `p8_l4_execution_not_approved`. |
| request to open P8-L5 autonomous runtime | Stop and report `p8_l5_autonomous_runtime_blocked`. |

## 27. Future Validation Targets

Future validation targets are proposed but not executed:

- P8.0 prerequisite invariant.
- P8-L0 definition completeness.
- P8-L1 definition completeness.
- P8-L2 definition completeness.
- P8-L3 definition completeness.
- P8-L4 future-only definition completeness.
- P8-L5 blocked invariant.
- ActivationGateRecord required field completeness.
- GateDecision vocabulary completeness.
- GateStatus vocabulary completeness.
- GateEvidencePackage completeness.
- RequiredHumanApproval model completeness.
- BlockedSurface matrix completeness.
- ExternalCandidateGate completeness.
- ExternalInspectionGate completeness.
- AdapterActivationBoundary completeness.
- RuntimeEscalationRequest completeness.
- GitMutationBoundary completeness.
- ProductReadinessGateRef completeness.
- Provider/auth/API/MCP blocked invariant.
- Credentials blocked invariant.
- Tool execution blocked invariant.
- Agent execution blocked invariant.
- OpenCode adapter execution blocked invariant.
- Graphify rerun blocked invariant.
- GBrain runtime blocked invariant.
- GStack execution blocked invariant.
- Hermes runtime blocked invariant.
- Cadence blocked invariant.
- Git mutation blocked invariant.
- No `git add .` invariant.
- P8.6-P8.9 boundary ticket readiness.
- P8.10/P8.11 synthesis and implementation plan readiness.

## 28. Future Hardening Candidates

Future tickets are proposed but not started:

- P8-GATE-HARD-01 - ActivationGateRecord Schema Candidate.
- P8-GATE-HARD-02 - GateEvidencePackage Checklist.
- P8-GATE-HARD-03 - ExternalInspectionGate Matrix Hardening.
- P8-GATE-HARD-04 - AdapterActivationBoundary Checklist.
- P8-GATE-HARD-05 - Human Approval Scope Checklist.
- P8-GATE-HARD-06 - RuntimeEscalationRequest Checklist.
- P8-GATE-HARD-07 - GitMutationBoundary Checklist.
- P8-GATE-HARD-08 - ProductReadinessGateRef Checklist.
- P8-GATE-HARD-09 - P8-L4 Future Execution Candidate Checklist.
- P8-GATE-HARD-10 - P8-L5 Blocked Runtime Invariant Checklist.

## 29. Created / Not Created Register

Created:

- `0_architecture/governance/agent_platform_p8_security_activation_gate_model.md`

Modified:

- none

Not created / not approved:

- no P8.1-P8.R files
- no implementation files
- no MVP package
- no schemas
- no CLI/TUI/web shell
- no state store
- no local workspace artifacts
- no adapters
- no executable adapters
- no OpenCode adapter
- no Graphify adapter
- no GBrain adapter
- no GStack adapter
- no Hermes adapter
- no provider/API/MCP adapter
- no product/Siamese adapter
- no runtime activation
- no autonomous orchestration
- no scheduler
- no Cadence
- no Hermes runtime
- no GBrain runtime
- no GStack execution
- no OpenCode execution from AGENT PLATFORM
- no Graphify execution
- no Codegraph execution
- no provider/auth/API/MCP activation
- no credentials
- no API calls
- no MCP calls
- no live connectors
- no product/Siamese source inspection
- no external source content inspection
- no source loading
- no tool execution
- no agent execution
- no task execution
- no handoff execution
- no automatic dispatch
- no automatic reviewer assignment
- no automatic integration
- no automatic commits
- no automatic pushes
- no persistence DB
- no vector DB
- no graph DB
- no telemetry
- no event streaming
- no generated output tracking
- no source tracking expansion
- no publication
- no Git mutation by the agent
- no P8-L4 execution approved
- no P8-L5 autonomous runtime opened
- no Cognitive Semantic System substrate selection

## 30. Recommended Next Ticket

After P8.5, continue the Round 1 parallel queue if not already completed:

- P8.1 - External Source Inventory / Classification
- P8.2 - MVP Interaction Surface Architecture
- P8.3 - Core Workflow Schema Candidates
- P8.4 - Local Workspace / State Model

If P8.1-P8.5 are complete, the next parallel queue is:

- P8.6 - Graphify Read-Only Evidence Boundary
- P8.7 - GBrain / GStack Memory Compatibility Boundary
- P8.8 - Hermes Interface / Runtime Candidate Boundary
- P8.9 - OpenCode Harness Upgrade Boundary

Recommended actual: P8.2 - MVP Interaction Surface Architecture, because P8.1 and P8.4 are present while P8.2 and P8.3 are absent. If the user prefers the prompt order, P8.1 remains the standard Round 1 recommendation unless already completed.

Do not start P8.1. Do not start P8.2. Do not start P8.3. Do not start P8.4. Do not start P8.6. Do not start P8.7. Do not start P8.8. Do not start P8.9. Do not start P8.10. Do not start P8.11. Do not start P8.12+. Do not start P8.R.

## 31. Final Verdict

| Question | Answer |
| --- | --- |
| What did P8.5 create? | The canonical `P8 Security / Activation Gate Model`. |
| What Security / Activation Gate Model was defined? | A six-level `P8ActivationLevel` model plus gate records, decisions, statuses, evidence, approvals, blocked surfaces, external candidate gates, inspection gates, adapter boundaries, runtime escalation, Git boundary, and product readiness refs. |
| What P8-L0 means. | Documentation/design only. |
| What P8-L1 means. | Future schema/static template implementation only if authorized by P8.10/P8.11. |
| What P8-L2 means. | Future local non-executing UI/CLI only if authorized. |
| What P8-L3 means. | Future read-only metadata adapters only after candidate boundary and implementation gates. |
| What P8-L4 means. | Future human-approved controlled execution candidate only; not approved by P8.5. |
| What P8-L5 means. | Autonomous runtime, blocked. |
| What ActivationGateRecord was defined? | A metadata contract with target level, surface, status, inputs, evidence, security review, human approval, boundary docs, blocked/allowed actions, policies, lifecycle refs, limitations, and stop rules. |
| What GateDecision vocabulary was defined? | Allowed/current, design-only, static schema, local non-executing, read-only metadata, deferred, blocked, review/approval/product/synthesis/plan requirements, and out-of-scope values. |
| What GateStatus vocabulary was defined? | Lifecycle statuses from not started through design/candidate/blocked/deferred/review/approved-for-static/non-executing and explicit not-approved-for-execution/runtime/rejected. |
| What GateEvidencePackage was defined? | A metadata evidence package supporting review, not deciding or approving actions by itself. |
| What RequiredHumanApproval model was defined? | Explicit, scope-bound, target-surface/action-specific approval with evidence, blocked actions, and rollback/incident posture for execution candidates. |
| What BlockedSurface matrix was defined? | A matrix preserving blocked defaults for providers, credentials, tools, agents, handoffs, OpenCode, Graphify, GBrain, GStack, Hermes, Cadence, live connectors, product/source, persistence, vector/graph DB, telemetry, publication, Git, and `git add .`. |
| What ExternalCandidateGate was defined? | Candidate-level gate paths for Graphify, GBrain, GStack, Hermes, OpenCode, Codegraph, providers, MCP, connectors, product integrations, and Git tools. |
| What ExternalInspectionGate was defined? | `EI-0` through `EI-6`, from named candidate to runtime adoption, with `EI-5`/`EI-6` blocked by default. |
| What AdapterActivationBoundary was defined? | Static contract, metadata design, read-only metadata candidate, controlled execution candidate, runtime adapter, and product adapter categories. |
| What RuntimeEscalationRequest was defined? | A request metadata model that records escalation interest without approving escalation. |
| What GitMutationBoundary was defined? | Future exact-path advisory rendering is allowed; AGENT PLATFORM Git mutation is blocked; user owns Git; Never recommend git add . |
| What ProductReadinessGateRef was defined? | A future reference to P4 / GT-09 or equivalent for product/Siamese readiness, not opened by P8.5. |
| What blocked surfaces were preserved? | Runtime, autonomy, dispatch, review automation, integration automation, OpenCode/Graphify/GBrain/GStack/Hermes/Cadence execution, providers/API/MCP, credentials, product/external source inspection, persistence, telemetry, publication, Git mutation, and CSS substrate selection. |
| What external candidate gates were defined for Graphify? | `P8-L0` design now; future `P8-L3` read-only evidence only after P8.6 and explicit implementation plan; rerun and authority blocked. |
| What external candidate gates were defined for GBrain? | `P8-L0` design now; future metadata compatibility after P8.7; runtime/persistent memory blocked. |
| What external candidate gates were defined for GStack? | `P8-L0` design now; future compatibility inventory after P8.7; execution blocked. |
| What external candidate gates were defined for Hermes? | `P8-L0` design now; UI feasibility candidate after P8.8; runtime/Cadence blocked. |
| What external candidate gates were defined for OpenCode? | H0 user-operated harness now; future H1 metadata adapter after P8.9; execution blocked. |
| What external inspection levels were defined? | `EI-0`, `EI-1`, `EI-2`, `EI-3`, `EI-4`, `EI-5`, and `EI-6`. |
| What adapter activation boundaries were defined? | Design, metadata-only, read-only candidate, controlled execution candidate, runtime adapter blocked, and product adapter deferred. |
| What human approval rules were defined? | Approval must be explicit, scope-bound, evidence-backed, target-specific, action-specific, and cannot be inferred from refs, verdicts, validation, security review, or registry presence. |
| What security review requirements were defined? | Requirements for credentials, providers/API/MCP, external inspection, tool/agent execution, local UI/CLI, state, generated artifacts, Graphify, GBrain/GStack, Hermes, OpenCode, Git, and product/Siamese. |
| What P8 ticket-level gate requirements were defined? | P8.1-P8.5 remain `P8-L0`; P8.6-P8.9 are boundary/design unless later authorized; P8.10/P8.11 may plan `P8-L1`/`P8-L2`; P8.12-P8.15 may implement only authorized non-executing components; P8.16 manual pilot only; P8.R readiness only. |
| Did P8.5 create implementation files? | No. |
| Did P8.5 create adapters? | No. |
| Did P8.5 activate runtime? | No. |
| Did P8.5 approve P8-L4 execution? | No. |
| Did P8.5 open P8-L5 autonomous runtime? | No. |
| Did P8.5 execute OpenCode, Graphify, GBrain, GStack, Hermes, Codegraph, tools, agents, providers, API, MCP, or live connectors? | No. |
| Did P8.5 inspect external source contents? | No. |
| Did P8.5 inspect product/Siamese source? | No. |
| Did P8.5 create persistence, vector DB, graph DB, telemetry, or event streaming? | No. |
| Did P8.5 mutate Git? | No. |
| What is the next recommended ticket? | P8.2 if continuing from current present siblings; otherwise P8.1 as the standard Round 1 recommendation unless already completed. |
