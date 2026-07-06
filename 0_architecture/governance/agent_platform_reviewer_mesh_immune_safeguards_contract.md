# P7.0.F - Reviewer Mesh / Immune Safeguards Contract

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | Reviewer Mesh / Immune Safeguards Contract |
| Ticket | P7.0.F |
| Status | Accepted reviewer mesh / immune safeguards contract |
| Date | 2026-07-06 |
| Scope | Documentation-only manual workflow design for an agent-native ReviewerMesh and ImmuneSafeguard layer for AGENT PLATFORM / Siamese. |
| Authority | Manual workflow design only, not reviewer runtime, auto-review, automatic approval, AI self-approval, automatic reviewer assignment, autonomous reviewer mesh, automatic rework dispatch, automatic integration, Git mutation, runtime activation, validation execution, security enforcement, provider/auth/API/MCP activation, tool/agent/task/handoff execution, orchestration, live connectors, GBrain runtime, Hermes runtime, Cadence, Graphify rerun/adoption, Codegraph execution/adoption, persistence, vector DB, embeddings, graph DB, Cognitive Semantic System substrate selection, publication, generated-output tracking, source tracking expansion, product activation, external adoption, or product/Siamese source inspection. |
| Related documents | P7.0.0, P7.0.A, P7.0.B, P7.0.C, P7.0.D, P6.7, P6.1-P6.6, P5.R, P3.BR, P3.3, P3.4, P3.5, P2.KR, P2.1-P2.3, P1.1-P1.5, P0.1-P0.3, G-01, S-03, S-04, Cognitive Semantic System ADR/audit, README.md, `.gitignore`, `.graphifyignore`. |
| Optional peer posture | P7.0.E absent: `pending_P7.0.E_harness_boundary_alignment`; P7.0.G not reviewed or consumed by P7.0.F: `pending_P7.0.G_integrator_commit_protocol_alignment`; P7.0.H absent: `P7.0.H_not_started_expected`; P7.0.R absent: `P7.0.R_not_started_expected`. |
| Output | Canonical P7.0.F Reviewer Mesh / Immune Safeguards Contract. |

P7.0.F creates a review and safeguard contract. It does not create a reviewer runtime.

## 2. Purpose

P7.0.F defines how manual agentic outputs are reviewed through an agent-native safeguard model before any integrator acceptance or human final decision.

The contract corrects the reviewer model from a simple human approval pipeline into a `ReviewerMesh` and `ImmuneSafeguard` design. The manual review pipeline is preserved only as a projection:

```text
output -> reviewer checklist -> verdict -> rework/integration
```

The agent-native model is:

```text
ReviewInputPackage -> anomaly / drift / contradiction / unsafe-output detection -> containment / rework / escalation / integrator-routing -> HumanFinalDecision
```

P7.0.F defines review metadata, marker semantics, containment recommendations, rework routing, integrator acceptance boundaries, and human decision points. It does not activate automatic review, automatic assignment, automatic quarantine, automatic rejection, automatic rework dispatch, automatic integration, or Git mutation.

## 3. Current Baseline

| Area | Current baseline inherited by P7.0.F |
| --- | --- |
| Activation posture | AGENT PLATFORM remains AL-1 metadata skeleton. |
| P7 target posture | AL-1.5 manual controlled agentic workflow planning only. |
| Activation transition | `activation_level_transition: not_approved`. |
| Runtime activation | `runtime_activation: not_approved`. |
| Manual bridge layer | P7.0.A/B/C/D are present and aligned as `manual_bridge_layer` peers. |
| Agent-native layer | P7.0.0 defines the missing `agent_native_internal_organization_layer` pattern set. |
| Reviewer posture | Reviewer agents are manual roles and safeguard projections, not runtime agents. |
| Approval posture | `ApprovalRef` is not approval; reviewer approval is not Git approval. |
| Evidence posture | Evidence supports; it does not decide. |
| Validation posture | Validation evaluates; governance decides. |
| Security posture | Security constrains; it does not activate. |
| Product posture | Product-bound work remains blocked pending P4. |
| External posture | EXT.* reviews remain required before external adoption. |
| GBrain / Hermes / Cadence posture | Future inactive candidates only; no runtime, Cadence, provider/auth, MCP, persistence, or substrate approval. |
| Graphify posture | Supporting generated evidence only, not authority, not source, not substrate, not adopted. |
| Cognitive Semantic System posture | `cognitive_semantic_system_substrate_deferred`; markdown canonical docs plus metadata refs remain baseline. |
| Git posture | Human user remains final Git authority; exact-path advice only; never recommend `git add .`. |

P7.0.F may describe AL-1.5 manual review behavior as vocabulary. It does not approve an activation-level transition.

## 4. Inputs Reviewed

Inputs were reviewed as governance metadata and documentation only. No product source, external source content, GBrain source content, Graphify raw output, generated output content, secrets, credentials, provider config, token store, browser auth, local credential store, API key, validation runtime, tests, scripts, package manager, provider/API/network/MCP call, runtime, or Git mutation was used.

| Input | P7.0.F use | Boundary preserved |
| --- | --- | --- |
| P7.0.0 Agent-Native Organization Research Carry-Forward | Supplies `ImmuneReviewPattern`, `ReviewerMeshRef`, `ImmuneReviewMarker`, task graph, blackboard, capability cell, routing, and memory-fabric concepts. | Pattern set is conceptual; no runtime topology activation. |
| P7.0.A Manual Lead Agent / User Gateway | Supplies `ReviewRoutingRequest`, `HumanDecisionPoint`, user gateway, and manual lead role. | Lead agent is manual control plane, not orchestrator. |
| P7.0.B Roadmap Generation / Work Breakdown | Supplies review object precedent, `ReviewerMeshProjection`, `ManualExecutionProjection`, and exact Git boundary. | Roadmap and review route do not dispatch work. |
| P7.0.C Parallel Agent Lane / Work Packet Taxonomy | Supplies manual lane output, reviewer lane, integrator lane, `ReviewerMeshRef`, lane stop rules, and output acceptance rules. | Manual lanes are projections, not runtime agents. |
| P7.0.D Manual Context / Memory Manifest Strategy | Supplies `MemoryManifest`, `ContextPack`, `EvidencePack`, `ContradictionMarker`, `EvidenceConflictMarker`, and context freshness posture. | Memory fabric is metadata only, not persistence or retrieval. |
| P6.7 Operational Readiness Audit | Supplies accepted planning readiness, AL-1 posture, and active blockers. | P6 readiness is not activation. |
| P6.4 Human Approval / Review Loop | Supplies ApprovalRequest/ApprovalDecision/ReviewerRef boundaries and `ApprovalRef is not approval`. | Approval metadata does not activate workflow. |
| P6.5 Runtime Monitoring / Incident Handling | Supplies containment, incident, rollback, and monitoring boundary language. | Containment route is not automatic containment or incident automation. |
| P6.6 Cognitive Semantic System Substrate Decision | Supplies substrate deferral, GBrain candidate-only, Graphify evidence-only posture. | No substrate selected. |
| P5.R and P5 skeleton records | Supply AL-1 skeleton limitations. | Skeletons are not active services. |
| P3.BR, P3.3, P3.4, P3.5 | Supply tool/provider/agent activation blockers. | Decisions are not execution. |
| P2.KR, P2.1, P2.2, P2.3 | Supply retrieval boundary, vocabulary, EvidenceRef semantics, audit/retention/rollback posture. | No retrieval runtime or persistence. |
| P1.1-P1.5 | Supply context/provider/tool/agent/CSS metadata-only boundaries. | Metadata contracts are not runtime activation. |
| P0.1-P0.3 and G-01 | Supply activation gate, validation gate, security hardening, and gate-charter boundaries. | Gates are not approvals. |
| S-03 and S-04 | Supply local-only, secrets, credentials, tool, shell, network, MCP, and Git blocked defaults. | Policies are not enforcement activation. |
| Cognitive Semantic System ADR/audit | Supplies accepted name and substrate neutrality. | No implementation authorization. |
| README.md, `.gitignore`, `.graphifyignore` | Supply repository and ignore boundary posture. | Hygiene and default-deny posture are not runtime controls. |

## 5. Non-Action Statement

P7.0.F creates a documentation-only review contract.

| Not performed by P7.0.F | Reason |
| --- | --- |
| Reviewer runtime creation | Runtime activation remains not approved. |
| Automatic reviewer assignment | Manual user/lead routing remains required. |
| Auto-review, auto-approval, or AI self-approval | P6.4 blocks implicit approval and AI self-approval. |
| Automatic containment, quarantine, rejection, or rework dispatch | P7.0.F may recommend containment or rework metadata only. |
| Automatic integration or merge | Integrator acceptance is metadata and human-mediated. |
| Validation/test/build/script execution | P0.2, P3.1, and S-04 keep execution blocked unless a future exact gate approves. |
| Security enforcement or scanning | P0.3 and S-03/S-04 define constraints only. |
| Provider/auth/API/network/MCP calls | P3.4 and S-04 keep these blocked. |
| Tool/agent/task/handoff execution | P3.3/P3.5 and S-04 keep execution blocked. |
| Source loading or source inspection | SourceRef/FileRef are metadata and do not grant read permission. |
| Product-bound work or product/Siamese source inspection | P4 remains required first. |
| External adoption or external source inspection | EXT.* reviews remain required first. |
| GBrain/Hermes/Cadence activation | Candidate-only posture is preserved. |
| Graphify rerun/adoption or raw output inspection | Graphify remains supporting generated evidence only. |
| Persistence, vector DB, embeddings, graph DB, event stream, telemetry, monitoring runtime, incident automation, or rollback automation | Not approved by P6.7. |
| Cognitive Semantic System substrate selection | `cognitive_semantic_system_substrate_deferred` remains active. |
| Generated-output tracking, source tracking expansion, publication, staging, commit, push, or force-add | GT-12/human authority remains required. |

## 6. Authority Model

| Authority surface | P7.0.F rule |
| --- | --- |
| User | Final execution authority, final acceptance authority, final approval authority, and final Git authority. |
| Manual Lead Agent | May assemble `ReviewRequest`, route manual review prompts, summarize findings, and ask for human decisions. |
| ReviewerMesh | Metadata topology for review coverage and safeguards; not a live mesh. |
| ReviewerCell | Manual role or prompt pattern for scoped review; not active worker. |
| ImmuneSafeguard | Metadata safeguard for detecting anomaly, drift, contradiction, unsafe output, and scope violation; not enforcement. |
| Reviewer | May produce `ReviewFinding`, markers, `ContainmentAction` recommendations, `ReworkRequest`, and `ReviewVerdict`. |
| Integrator | May reconcile reviewed outputs and produce `IntegratorAcceptance` metadata. |
| Governance | Decides activation, exceptions, product/external boundaries, publication, and substrate decisions. |
| Validation | Evaluates; it does not decide approval, activation, publication, product work, or Git mutation. |
| Security | Constrains and can block; it does not activate runtime or approve action by itself. |
| Evidence | Supports decisions; it does not decide. |
| Git | User-operated record of accepted artifacts; not semantic truth and not reviewer approval. |

No agent role created by this contract may self-approve, execute runtime work, perform Git mutation, bypass the user, or bypass governance.

## 7. Reviewer Mesh / Immune Safeguard Boundary

`ReviewerMesh` is an agent-native conceptual topology for review coverage. It maps outputs, risks, boundaries, markers, reviewer cells, immune checks, containment recommendations, rework routing, escalation, and integration acceptance.

`ImmuneSafeguard` is a metadata safeguard concept for detecting and responding to anomalous or unsafe output. It is inspired by immune review, but it is not an active immune system.

| Concept | Allowed use | Blocked interpretation |
| --- | --- | --- |
| `ReviewerMesh` | Manual review topology metadata. | Runtime reviewer swarm, automatic reviewer assignment, auto-review. |
| `ReviewerMeshNode` | Node in review coverage graph. | Runnable node, task queue item, live worker. |
| `ReviewerCell` | Scoped manual reviewer capability. | Active agent, process, service, provider route. |
| `ImmuneSafeguard` | Metadata safeguard for anomaly/drift/contradiction/unsafe-output detection. | Enforcement engine, scanner, active security system. |
| `ImmuneCheck` | Checklist-style detection rule. | Automated detector or validation command. |
| `ContainmentAction` | Recommendation to pause, isolate, limit, or route output manually. | Automatic quarantine, deletion, rollback, rejection, or incident action. |
| `ReviewVerdict` | Manual review metadata. | Git approval, runtime approval, activation approval, or final human decision. |
| `HumanFinalDecision` | Explicit user decision over exact scope. | Silent approval, inferred approval, self-approval. |

Reviewer mesh design is not runtime activation. Immune safeguard design is not security enforcement activation.

## 8. Manual Review Projection Lifecycle

The agent-native review lifecycle is projected into manual workflow steps.

| Step | Agent-native object | Manual projection | Allowed action | Blocked action | Human decision point |
| --- | --- | --- | --- | --- | --- |
| Output assembled | `ReviewInputPackage` | User returns or identifies lane output. | Package exact scope and limitations. | Automatic ingest. | User decides what to submit. |
| Review requested | `ReviewRequest` | Lead agent drafts reviewer prompt. | Define reviewer cells, checklists, and stop rules. | Automatic assignment. | User chooses whether to run review. |
| Mesh scoped | `ReviewerMesh` / `ReviewerMeshNode` | Review coverage map. | Map risks and reviewer cells. | Live mesh activation. | User accepts route. |
| Safeguards applied | `ImmuneSafeguard` / `ImmuneCheck` | Checklist-based manual checks. | Detect markers and findings. | Automated scanning/enforcement. | User accepts manual review scope. |
| Findings emitted | `ReviewFinding` and markers | Reviewer output. | Record risks, blockers, and recommendations. | Auto-rejection or auto-change. | User/integrator reviews findings. |
| Containment recommended | `ContainmentAction` | Pause/limit/escalate recommendation. | Recommend safe manual handling. | Automatic quarantine/deletion/rollback. | User decides containment route. |
| Rework requested | `ReworkRequest` | Manual rework ticket candidate. | Describe exact rework need. | Automatic dispatch. | User decides whether to start rework. |
| Verdict issued | `ReviewVerdict` | Reviewer verdict metadata. | State accepted/limited/rework/blocked/out-of-scope. | Approval or Git authority. | Human decision still required. |
| Escalation routed | `ApprovalEscalation` | Human/governance/security/validation route. | Request exact-scope decision. | Escalation automation. | User/governance decides. |
| Integration reviewed | `IntegratorAcceptance` | Integrator accepts/rejects output for synthesis. | Integrate reviewed outputs manually. | Automatic merge or commit. | User final decision for Git. |
| Final decision | `HumanFinalDecision` | Explicit user decision. | Approve exact next action or stop. | Silent approval. | Required. |

## 9. Core Object Model

| Object | Meaning | Required fields | Forbidden fields | Boundary |
| --- | --- | --- | --- | --- |
| `ReviewRequest` | Metadata request for manual reviewer mesh review. | id, target, scope, requester, reviewer mesh, checklists, inputs, stop rules, verdict format. | reviewer daemon config, auto-assign flag, approval token. | Request is not approval. |
| `ReviewInputPackage` | Bounded package of output and context to review. | id, target output, scope, files/surfaces, context refs, evidence refs, blockers, limitations. | secrets, credentials, raw product source, raw external source, raw Graphify output. | Input package is not source loading permission. |
| `ReviewerMesh` | Review coverage topology metadata. | id, target, reviewer cells, mesh nodes, immune safeguards, escalation, manual projection. | runtime topology, live routing, scheduler. | Mesh is not runtime. |
| `ReviewerCell` | Scoped manual reviewer capability. | id, role, scope, allowed checks, blocked checks, authority limits, output format. | active worker id, provider credentials, commit authority. | Cell is not active agent. |
| `ReviewerMeshNode` | Node in review graph linking target risk to reviewer cells and checks. | id, node type, target refs, reviewer cell refs, check refs, dependencies, status. | queue state, daemon state, automatic trigger. | Node is metadata only. |
| `ReviewChecklist` | Manual checklist for a review scope. | id, review type, criteria, stop rules, required markers, verdict options. | validation command as executed, scanner config. | Checklist is not validation execution. |
| `ImmuneSafeguard` | Metadata safeguard category for unsafe or inconsistent output. | id, safeguard type, risks, checks, markers, containment route, escalation route. | enforcement policy engine, automatic quarantine flag. | Safeguard is not enforcement. |
| `ImmuneCheck` | Individual detection rule used manually. | id, check type, condition, evidence needed, marker emitted, stop rule. | executable detector, network call, provider call. | Check is manual metadata. |
| `ReviewFinding` | Reviewer finding with evidence and recommendation. | id, severity, summary, evidence refs, affected refs, risk, recommendation, blocker status. | automatic file edits, secret values. | Finding is evidence, not change. |
| `AnomalyMarker` | Marker for unexpected or suspicious output. | id, anomaly class, evidence refs, affected output, severity, route. | auto-reject flag. | Manual review cue. |
| `DriftMarker` | Marker for divergence from scope, baseline, or expected posture. | id, drift type, baseline refs, affected output, severity, route. | silent correction. | Manual integrator cue. |
| `ContradictionMarker` | Marker for conflicting claims. | id, conflicting claim refs, evidence refs, severity, review route. | automatic conflict resolution. | Manual review cue. |
| `EvidenceConflictMarker` | Marker for conflicting evidence. | id, conflicting evidence refs, affected claims, escalation route, limitations. | evidence-as-authority. | Manual escalation cue. |
| `UnsafeOutputMarker` | Marker for output that may be unsafe to accept or expose. | id, unsafe class, affected content class, safe summary, containment route. | secret/credential content, raw unsafe payload. | Safe metadata only. |
| `ScopeViolationMarker` | Marker for crossing allowed scope. | id, violation class, allowed scope, observed drift, required stop. | automatic waiver. | Stop and review. |
| `ContainmentAction` | Recommended manual containment step. | id, trigger marker, action type, owner, allowed handling, blocked automation. | automatic quarantine, deletion, rollback. | Recommendation only. |
| `ReworkRequest` | Metadata request for manual rework. | id, source finding, exact scope, required changes, blocked actions, reviewer required. | automatic dispatch flag. | Rework requires user selection. |
| `ReviewVerdict` | Reviewer conclusion metadata. | id, target, verdict status, conditions, findings, blockers, limitations. | Git approval, activation approval. | Verdict is not final authority. |
| `ApprovalEscalation` | Route for exact human/governance/security/validation decision. | id, trigger, target authority, exact question, required evidence, stop rules. | notification runtime, auto-escalation. | Escalation is metadata. |
| `IntegratorAcceptance` | Integrator decision over reviewed output. | id, output refs, verdict refs, accepted scope, rejected scope, residual blockers. | merge automation, Git mutation. | Acceptance is not Git approval. |
| `HumanFinalDecision` | Explicit human decision over exact action. | id, decision owner, exact scope, selected option, evidence, limitations. | silent approval, inferred approval, AI self-approval. | Required before Git or phase movement. |

## 10. ReviewRequest Contract

`ReviewRequest` fields:

| Field | Requirement |
| --- | --- |
| `review_request_id` | Stable identifier. |
| `request_title` | Human-readable title. |
| `requester_ref` | User, lead agent, integrator, or governance metadata ref. |
| `target_output_refs` | Output package, work packet, document, or decision refs under review. |
| `review_scope` | Exact in-scope surfaces. |
| `excluded_scope` | Explicit exclusions and inherited blocked surfaces. |
| `review_type` | Architecture, security, validation-readiness, consistency, memory/context, product-boundary, external-boundary, Git-advisory, or integration review. |
| `reviewer_mesh_ref` | `ReviewerMesh` metadata ref. |
| `reviewer_cell_refs` | `ReviewerCell` refs expected for manual review. |
| `review_checklist_refs` | `ReviewChecklist` refs. |
| `immune_safeguard_refs` | `ImmuneSafeguard` refs. |
| `review_input_package_ref` | `ReviewInputPackage` ref. |
| `evidence_refs` | EvidenceRef-compatible refs. |
| `validation_refs` | Validation posture refs; not execution. |
| `security_refs` | Security posture refs; not activation. |
| `source_classification_refs` | Source classification metadata refs. |
| `sensitivity` | Sensitivity posture; unknown sensitivity blocks review acceptance. |
| `stop_rules` | Review stop rules. |
| `required_verdict_format` | Required `ReviewVerdict` format. |
| `human_decision_points` | Required `HumanFinalDecision` refs or placeholders. |
| `limitations` | Known limitations. |

`ReviewRequest` is a request for manual review. It is not reviewer assignment, approval, runtime activation, or dispatch.

## 11. ReviewInputPackage Contract

`ReviewInputPackage` fields:

| Field | Requirement |
| --- | --- |
| `review_input_package_id` | Stable identifier. |
| `target_output_ref` | Output under review. |
| `source_work_packet_ref` | Work packet or lane output source. |
| `source_lane_ref` | Manual lane or capability-cell projection source. |
| `allowed_scope` | Exact surfaces allowed for review. |
| `blocked_scope` | Explicit blocked surfaces. |
| `output_summary` | Safe summary of the output. |
| `changed_artifact_refs` | Exact metadata refs for files or docs if applicable. |
| `context_pack_refs` | Manual context refs. |
| `memory_manifest_refs` | Manual MemoryManifest refs. |
| `evidence_pack_refs` | EvidencePack refs. |
| `blackboard_refs` | Blackboard or blackboard-memory refs, if applicable. |
| `contradiction_marker_refs` | Known contradiction markers. |
| `evidence_conflict_marker_refs` | Known evidence conflict markers. |
| `freshness_markers` | Current, stale, missing, unknown, or conflicting context markers. |
| `source_classification_refs` | Source classification metadata. |
| `sensitivity_flags` | Local-only, product, external, generated, provider, secret, credential, or unknown flags. |
| `blockers` | Active blockers. |
| `excluded_material` | Material intentionally not included. |
| `safe_reporting_requirements` | Safe reporting format for sensitive findings. |
| `limitations` | Known limitations. |

`ReviewInputPackage` must not include secrets, credential values, raw product source, raw external source, raw GBrain source, raw Graphify output, raw live connector payloads, token stores, provider configs, browser auth, API keys, or unknown-sensitivity material.

## 12. ReviewerMesh Contract

`ReviewerMesh` fields:

| Field | Requirement |
| --- | --- |
| `reviewer_mesh_id` | Stable identifier. |
| `mesh_title` | Human-readable title. |
| `target_scope` | Exact target scope. |
| `mesh_pattern` | `immune_review_pattern`, `task_graph_review_pattern`, `blackboard_review_pattern`, `cell_boundary_review_pattern`, or hybrid. |
| `reviewer_cell_refs` | Manual reviewer cells included in coverage. |
| `reviewer_mesh_node_refs` | Coverage nodes. |
| `immune_safeguard_refs` | Safeguards applied. |
| `review_checklist_refs` | Checklists available to cells. |
| `marker_taxonomy_refs` | Marker categories used. |
| `containment_routes` | Manual containment recommendation routes. |
| `rework_routes` | Manual rework request routes. |
| `escalation_routes` | Manual human/governance/security/validation escalation routes. |
| `integrator_route` | Integrator synthesis route. |
| `manual_reviewer_projection` | Human-operable review prompt projection. |
| `blocked_automation` | Explicit blocked automation. |
| `limitations` | Known limitations. |

`ReviewerMesh` is manual review topology metadata. It is not a live reviewer mesh, automatic reviewer assignment, auto-review, automatic quarantine, automatic rejection, or reviewer runtime.

## 13. ReviewerCell And ReviewerMeshNode Contracts

`ReviewerCell` fields:

| Field | Requirement |
| --- | --- |
| `reviewer_cell_id` | Stable identifier. |
| `cell_name` | Human-readable role. |
| `cell_type` | Architecture, security, validation-readiness, memory/context, product-boundary, external-boundary, evidence-consistency, Git-advisory, or integrator-precheck. |
| `review_scope` | Exact surfaces the cell can review. |
| `allowed_checks` | Allowed manual checks. |
| `blocked_checks` | Blocked checks, including execution and source inspection. |
| `required_inputs` | Required ReviewInputPackage and evidence/context refs. |
| `output_format` | Required findings, markers, verdict, and limitations format. |
| `authority_limitations` | No Git, runtime, activation, or final approval authority. |
| `conflict_of_interest_posture` | Conflict limitations if applicable. |
| `human_required` | Whether a human review or human decision is required. |
| `stop_rules` | Stop triggers. |
| `limitations` | Known limitations. |

`ReviewerMeshNode` fields:

| Field | Requirement |
| --- | --- |
| `reviewer_mesh_node_id` | Stable identifier. |
| `node_type` | Scope node, risk node, evidence node, contradiction node, safeguard node, escalation node, or integration node. |
| `target_refs` | Output, work packet, task graph, blackboard, file, or decision refs. |
| `reviewer_cell_refs` | Cells mapped to this node. |
| `immune_check_refs` | Immune checks mapped to this node. |
| `dependency_refs` | Review ordering dependencies. |
| `marker_outputs` | Markers this node may emit. |
| `blocking_conditions` | Conditions that block acceptance. |
| `manual_projection` | Human-readable review prompt/checklist projection. |
| `status` | draft, requested, in_manual_review, findings_reported, needs_rework, blocked, accepted_with_limitations, superseded, or retired. |
| `limitations` | Known limitations. |

`ReviewerCell` and `ReviewerMeshNode` are not active agents, workers, queues, daemons, provider routes, or scheduler entries.

## 14. ReviewChecklist Contract

`ReviewChecklist` fields:

| Field | Requirement |
| --- | --- |
| `review_checklist_id` | Stable identifier. |
| `checklist_name` | Human-readable checklist name. |
| `review_type` | Review type covered. |
| `scope_rules` | Exact scope and exclusion rules. |
| `required_inputs` | Required package, context, evidence, and decision refs. |
| `criteria` | Manual criteria. |
| `immune_check_refs` | Related ImmuneCheck refs. |
| `marker_requirements` | Markers to emit if issues are found. |
| `blocking_findings` | Findings that block acceptance. |
| `allowed_verdicts` | Allowed ReviewVerdict statuses. |
| `stop_rules` | Stop triggers. |
| `safe_reporting_format` | Safe format for sensitive or blocked material. |
| `limitations` | Known limitations. |

ReviewChecklist is not validation execution, security scanning, tool execution, source inspection, or approval.

## 15. ImmuneSafeguard And ImmuneCheck Contracts

`ImmuneSafeguard` fields:

| Field | Requirement |
| --- | --- |
| `immune_safeguard_id` | Stable identifier. |
| `safeguard_name` | Human-readable safeguard name. |
| `safeguard_type` | anomaly, drift, contradiction, evidence conflict, unsafe output, scope violation, approval shortcut, source boundary, security boundary, validation boundary, product boundary, external boundary, Git boundary, or substrate boundary. |
| `risk_surface` | Surface being protected. |
| `immune_check_refs` | Checks included. |
| `marker_outputs` | Markers emitted by matching checks. |
| `containment_action_refs` | Recommended containment actions. |
| `rework_request_route` | Manual rework route if needed. |
| `approval_escalation_route` | Manual escalation route if needed. |
| `integrator_route` | Integrator route if output can proceed with limitations. |
| `blocked_automation` | Explicit blocked automation. |
| `limitations` | Known limitations. |

`ImmuneCheck` fields:

| Field | Requirement |
| --- | --- |
| `immune_check_id` | Stable identifier. |
| `check_name` | Human-readable check name. |
| `check_type` | anomaly, drift, contradiction, evidence conflict, unsafe output, scope violation, approval shortcut, or boundary check. |
| `condition` | Manual condition to inspect in the output. |
| `required_evidence` | Evidence refs needed to evaluate manually. |
| `emitted_marker` | Marker emitted if condition is met. |
| `severity_rule` | Severity assignment rule. |
| `containment_recommendation` | Manual containment recommendation. |
| `rework_recommendation` | Manual rework recommendation. |
| `escalation_recommendation` | Manual escalation recommendation. |
| `stop_rule` | Stop trigger if condition is unsafe or scope-breaking. |
| `limitations` | Known limitations. |

ImmuneSafeguard and ImmuneCheck are metadata-only. They do not run scans, enforce policies, quarantine outputs, or reject outputs automatically.

## 16. Findings And Marker Contracts

`ReviewFinding` fields:

| Field | Requirement |
| --- | --- |
| `review_finding_id` | Stable identifier. |
| `review_request_ref` | Linked ReviewRequest. |
| `reviewer_cell_ref` | Reviewer cell that produced the finding. |
| `finding_type` | anomaly, drift, contradiction, evidence conflict, unsafe output, scope violation, boundary issue, missing context, stale context, approval shortcut, or residual risk. |
| `severity` | info, low, medium, high, blocking, or stop. |
| `summary` | Safe summary. |
| `affected_refs` | Affected output, file, decision, task, marker, or evidence refs. |
| `evidence_refs` | Supporting EvidenceRef-compatible refs. |
| `marker_refs` | Marker refs emitted by the finding. |
| `risk` | Risk description. |
| `recommendation` | Manual recommendation. |
| `blocker_status` | none, limitation, blocks_acceptance, blocks_integration, blocks_git, or stop_required. |
| `safe_reporting_limitations` | Reporting limitations. |

Marker fields:

| Marker | Required fields | Boundary |
| --- | --- | --- |
| `AnomalyMarker` | `anomaly_marker_id`, `anomaly_class`, `target_ref`, `evidence_refs`, `severity`, `review_route`, `limitations`. | Manual anomaly cue, not automatic rejection. |
| `DriftMarker` | `drift_marker_id`, `drift_class`, `baseline_refs`, `observed_output_ref`, `affected_scope`, `severity`, `resolution_route`, `limitations`. | Manual drift cue, not silent correction. |
| `ContradictionMarker` | `contradiction_marker_id`, `conflicting_claim_refs`, `source_refs`, `evidence_refs`, `severity`, `review_required`, `resolution_route`, `limitations`. | Manual contradiction cue, not automatic conflict resolution. |
| `EvidenceConflictMarker` | `evidence_conflict_marker_id`, `conflicting_evidence_refs`, `affected_claim_refs`, `affected_task_refs`, `review_required`, `escalation_route`, `limitations`. | Manual evidence conflict cue, not evidence deciding. |
| `UnsafeOutputMarker` | `unsafe_output_marker_id`, `unsafe_class`, `affected_output_ref`, `safe_summary`, `sensitivity_flags`, `containment_route`, `stop_rule`, `limitations`. | Safe metadata only, not exposure of unsafe content. |
| `ScopeViolationMarker` | `scope_violation_marker_id`, `violation_class`, `allowed_scope_ref`, `observed_scope_drift`, `affected_refs`, `required_stop`, `review_route`, `limitations`. | Stop-and-review cue, not automatic waiver. |

Findings and markers support manual decisions. They do not decide acceptance, approval, activation, integration, or Git.

## 17. ContainmentAction Contract

`ContainmentAction` fields:

| Field | Requirement |
| --- | --- |
| `containment_action_id` | Stable identifier. |
| `trigger_marker_ref` | Marker or finding that triggered containment recommendation. |
| `containment_type` | pause_review, limit_scope, isolate_output_metadata, request_safe_summary, block_acceptance, block_git_advice, escalate_to_human, escalate_to_security, escalate_to_validation, escalate_to_governance, or request_rework. |
| `recommended_owner` | User, lead agent, reviewer, integrator, security reviewer, validation reviewer, product boundary reviewer, external boundary reviewer, or governance. |
| `allowed_manual_action` | Exact manual action allowed. |
| `blocked_automation` | Automatic quarantine, deletion, rollback, rejection, incident automation, notification, dispatch, integration, or Git mutation. |
| `safe_reporting_format` | Safe format for reporting. |
| `rework_route` | ReworkRequest route if applicable. |
| `escalation_route` | ApprovalEscalation route if applicable. |
| `human_decision_required` | Required HumanFinalDecision condition. |
| `limitations` | Known limitations. |

ContainmentAction is a recommendation. It is not automatic quarantine, automatic deletion, automatic rollback, automatic rejection, or incident automation.

## 18. ReworkRequest Contract

`ReworkRequest` fields:

| Field | Requirement |
| --- | --- |
| `rework_request_id` | Stable identifier. |
| `source_review_request_ref` | ReviewRequest that produced the rework need. |
| `source_finding_refs` | Findings that justify rework. |
| `source_marker_refs` | Markers that justify rework. |
| `target_output_refs` | Output requiring rework. |
| `exact_rework_scope` | Exact allowed rework scope. |
| `blocked_rework_scope` | Explicit blocked actions and surfaces. |
| `required_changes` | Human-readable required changes. |
| `required_context_refs` | Context/evidence/memory refs needed. |
| `review_required_after_rework` | Review needed after rework. |
| `integrator_required_after_rework` | Whether integrator pass is required. |
| `human_decision_required_before_rework` | Human decision point. |
| `git_posture` | No Git mutation; exact-path advice only after later acceptance. |
| `stop_rules` | Stop triggers. |
| `limitations` | Known limitations. |

ReworkRequest is metadata for a future manual work packet or user-selected follow-up. It is not automatic rework dispatch.

## 19. ReviewVerdict Contract

`ReviewVerdict` fields:

| Field | Requirement |
| --- | --- |
| `review_verdict_id` | Stable identifier. |
| `review_request_ref` | Linked ReviewRequest. |
| `reviewer_cell_refs` | Reviewer cells contributing. |
| `target_output_refs` | Reviewed outputs. |
| `verdict_status` | allowed status from the controlled vocabulary. |
| `accepted_scope` | Exact scope accepted for manual integration consideration, if any. |
| `rejected_scope` | Exact scope rejected or blocked, if any. |
| `conditions` | Conditions that must travel downstream. |
| `finding_refs` | ReviewFinding refs. |
| `marker_refs` | Marker refs. |
| `containment_action_refs` | ContainmentAction refs. |
| `rework_request_refs` | ReworkRequest refs. |
| `approval_escalation_refs` | ApprovalEscalation refs. |
| `human_final_decision_required` | Required HumanFinalDecision flag and reason. |
| `limitations` | Known limitations. |

Allowed verdict statuses:

| Status | Meaning |
| --- | --- |
| `accepted_for_integrator_review` | Output may proceed to integrator review with exact scope. |
| `accepted_with_limitations_for_integrator_review` | Output may proceed with limitations and conditions. |
| `needs_rework` | Rework is required before acceptance. |
| `blocked_by_anomaly` | Anomaly blocks acceptance. |
| `blocked_by_drift` | Drift blocks acceptance. |
| `blocked_by_contradiction` | Contradiction blocks acceptance. |
| `blocked_by_evidence_conflict` | Evidence conflict blocks acceptance. |
| `blocked_by_unsafe_output` | Unsafe output blocks acceptance or safe reporting. |
| `blocked_by_scope_violation` | Scope violation blocks acceptance. |
| `blocked_by_missing_context` | Required context is missing. |
| `blocked_by_stale_context` | Context staleness blocks trust. |
| `blocked_by_security` | Security blocker present. |
| `blocked_by_validation` | Validation posture blocker present. |
| `blocked_by_product_boundary` | Product boundary blocker present. |
| `blocked_by_external_boundary` | External boundary blocker present. |
| `blocked_by_git_boundary` | Git/source tracking/publication blocker present. |
| `out_of_scope` | Output is outside allowed scope. |
| `escalated_for_human_final_decision` | Exact human decision required. |

ReviewVerdict is review metadata. It is not approval, Git approval, activation approval, final human decision, validation execution, security enforcement, or integration automation.

## 20. ApprovalEscalation And HumanFinalDecision Contracts

`ApprovalEscalation` fields:

| Field | Requirement |
| --- | --- |
| `approval_escalation_id` | Stable identifier. |
| `trigger_ref` | Finding, marker, verdict, containment action, or rework request that triggered escalation. |
| `escalation_type` | human_final_decision, governance_review, security_review, validation_review, product_boundary_review, external_boundary_review, Git_authority_review, or substrate_boundary_review. |
| `exact_question` | Exact decision question. |
| `decision_scope` | Exact scope for decision. |
| `required_evidence_refs` | Required evidence refs. |
| `required_security_refs` | Required security posture refs. |
| `required_validation_refs` | Required validation posture refs. |
| `blocked_actions_pending_decision` | Actions blocked until decision. |
| `expiration_or_staleness_posture` | Staleness handling. |
| `safe_reporting_format` | Safe reporting requirements. |
| `limitations` | Known limitations. |

`HumanFinalDecision` fields:

| Field | Requirement |
| --- | --- |
| `human_final_decision_id` | Stable identifier. |
| `decision_owner` | Human user or accountable governance owner. |
| `decision_label` | Human-readable decision label. |
| `decision_scope` | Exact scope. |
| `decision_options` | Allowed options. |
| `selected_option` | Explicit selected option. |
| `evidence_refs` | Evidence used. |
| `review_verdict_refs` | Review verdicts considered. |
| `integrator_acceptance_refs` | Integrator acceptance refs considered. |
| `conditions` | Conditions attached to the decision. |
| `blocked_automatic_action` | Automation that remains blocked. |
| `git_authority_statement` | User remains final Git authority. |
| `limitations` | Known limitations. |

ApprovalEscalation is not escalation automation. HumanFinalDecision cannot be inferred from silence, user intent without exact scope, reviewer verdict, evidence, validation, security, or ApprovalRef.

## 21. IntegratorAcceptance Contract

`IntegratorAcceptance` fields:

| Field | Requirement |
| --- | --- |
| `integrator_acceptance_id` | Stable identifier. |
| `integration_scope` | Exact integration scope. |
| `input_output_refs` | Outputs considered. |
| `review_verdict_refs` | ReviewVerdict refs considered. |
| `finding_refs` | Material findings considered. |
| `marker_refs` | Material markers considered. |
| `accepted_output_refs` | Outputs accepted for synthesis. |
| `rejected_output_refs` | Outputs rejected or deferred. |
| `accepted_scope` | Exact accepted scope. |
| `deferred_scope` | Deferred scope. |
| `residual_blockers` | Blockers still active. |
| `rework_request_refs` | Required or optional rework refs. |
| `approval_escalation_refs` | Escalation refs that remain open. |
| `human_final_decision_required` | Required human decision. |
| `commit_advice_posture` | Advice only, exact paths only, no `git add .`. |
| `limitations` | Known limitations. |

IntegratorAcceptance is integration metadata. It is not automatic integration, merge automation, Git approval, Git mutation, runtime approval, or publication approval.

## 22. Reviewer Cell Taxonomy

| ReviewerCell type | Allowed checks | Typical markers | Required escalation | Blocked actions |
| --- | --- | --- | --- | --- |
| Architecture ReviewerCell | Contract consistency, topology fit, scope and boundary preservation. | DriftMarker, ContradictionMarker, ScopeViolationMarker. | Governance or integrator if contract conflict appears. | Runtime design activation, source inspection. |
| Security ReviewerCell | Secrets/credentials, local-only, unsafe output, provider/auth, publication, Git safety. | UnsafeOutputMarker, ScopeViolationMarker, AnomalyMarker. | Security or human final decision for sensitive blockers. | Secret inspection, scanning, enforcement activation. |
| Validation ReviewerCell | Validation-readiness, proof posture, future target clarity. | DriftMarker, EvidenceConflictMarker. | Validation review if validation posture is missing. | Test/build/script execution. |
| Memory / Context ReviewerCell | Context freshness, MemoryManifest completeness, evidence and source refs. | DriftMarker, ContradictionMarker, EvidenceConflictMarker. | Human decision if required context is missing or stale. | Source loading, automatic retrieval, persistence. |
| Product Boundary ReviewerCell | Product/Siamese boundary and P4 blockers. | ScopeViolationMarker, UnsafeOutputMarker. | Product boundary review and P4 route. | Product source inspection or activation. |
| External Boundary ReviewerCell | EXT.* blockers, external candidate posture, GBrain/Hermes/Cadence boundaries. | ScopeViolationMarker, EvidenceConflictMarker, AnomalyMarker. | External review route. | External source inspection, adoption, execution. |
| Evidence Consistency ReviewerCell | EvidenceRef consistency, conflicting claims, supporting-only posture. | ContradictionMarker, EvidenceConflictMarker. | Integrator or governance if material contradiction persists. | Evidence deciding. |
| Git Advisory ReviewerCell | Exact-path commit advice boundary and no broad staging. | ScopeViolationMarker, UnsafeOutputMarker. | Human final Git decision. | Staging, commit, push, `git add .`. |
| Integrator Precheck ReviewerCell | Synthesis readiness and residual blockers. | DriftMarker, ContradictionMarker. | IntegratorAcceptance and HumanFinalDecision. | Automatic merge or mutation. |

Reviewer cell taxonomy is manual review projection. It is not the final internal runtime taxonomy.

## 23. Immune Check Matrix

| ImmuneCheck type | Detection question | Marker emitted | Default manual route | Blocked shortcut |
| --- | --- | --- | --- | --- |
| Anomaly check | Does output contain unexpected structure, authority claim, unsafe recommendation, or unexplained artifact? | AnomalyMarker | Reviewer/integrator review. | Auto-rejection. |
| Drift check | Does output drift from ticket scope, P7 boundaries, prior baseline, or manual projection? | DriftMarker | ReworkRequest or integrator limitation. | Silent correction. |
| Contradiction check | Does output contradict another accepted record or claim? | ContradictionMarker | Evidence consistency review and escalation if material. | Automatic conflict resolution. |
| Evidence conflict check | Do evidence refs disagree or fail to support a claim? | EvidenceConflictMarker | Evidence review and limitation. | Evidence as authority. |
| Unsafe output check | Does output include or request secrets, credentials, raw source, unsafe exposure, or blocked execution? | UnsafeOutputMarker | ContainmentAction and security escalation. | Printing unsafe content. |
| Scope violation check | Did output inspect, modify, recommend, or activate out-of-scope surfaces? | ScopeViolationMarker | Stop, containment, rework, or escalation. | Waiver by reviewer alone. |
| Approval shortcut check | Does output treat reviewer verdict, evidence, validation, security, ApprovalRef, DecisionRef, or user intent as approval? | ScopeViolationMarker | HumanFinalDecision route. | Implicit approval. |
| Git boundary check | Does output recommend broad staging, commit/push by agent, generated tracking, product/external tracking, or publication? | UnsafeOutputMarker or ScopeViolationMarker | Human Git authority route. | `git add .` or agent Git mutation. |
| Substrate boundary check | Does output select graph/vector/GBrain/Graphify/CSS substrate or persistence? | DriftMarker or ScopeViolationMarker | Governance/substrate future gate. | Substrate by review. |
| Runtime boundary check | Does output imply scheduler, queue, worker, runtime, task/handoff execution, or autonomous orchestration? | ScopeViolationMarker | Activation gate route. | AL-2 by wording. |

Immune checks are manual. They do not execute commands, scan files, call providers, or enforce policy.

## 24. Input / Output Acceptance Rules

```text
ReviewInputPackage is bounded context, not source loading.
ReviewRequest is a manual request, not assignment.
ReviewerMesh is topology metadata, not runtime.
ReviewerCell is a manual review role, not an active agent.
ReviewChecklist is not validation execution.
ImmuneSafeguard is not security enforcement.
ImmuneCheck is not an automated detector.
ReviewFinding is evidence, not file mutation.
AnomalyMarker is a cue, not rejection.
DriftMarker is a cue, not correction.
ContradictionMarker is a cue, not resolution.
EvidenceConflictMarker is a cue, not evidence authority.
UnsafeOutputMarker is safe metadata, not unsafe content exposure.
ScopeViolationMarker requires stop/review, not automatic waiver.
ContainmentAction is recommendation, not quarantine automation.
ReworkRequest is not dispatch.
ReviewVerdict is not approval.
ApprovalEscalation is not escalation automation.
IntegratorAcceptance is not Git approval.
HumanFinalDecision must be explicit.
```

No review output becomes canonical until accepted by the intended manual process and, where applicable, explicit human final decision.

## 25. Evidence, Validation, Security, And Approval Interfaces

| Interface | P7.0.F rule |
| --- | --- |
| EvidenceRef | Evidence supports findings, markers, verdicts, and decisions; it does not decide. |
| SourceRef | SourceRef is metadata; it is not source loading or file-read permission. |
| FileRef | FileRef is metadata; it is not file reading, writing, or Git tracking permission. |
| ValidationRef | Validation evaluates; it does not approve review verdicts, activation, product work, publication, or Git mutation. |
| SecurityRef | Security constrains and can block; it does not activate runtime or approve unsafe action. |
| ApprovalRef | ApprovalRef is not approval. |
| DecisionRef | DecisionRef is not approval by default and not execution permission. |
| ReviewVerdict | Review metadata only; not Git approval, activation approval, or human final decision. |
| IntegratorAcceptance | Integration metadata only; not automatic merge and not Git approval. |
| HumanFinalDecision | Required for exact final acceptance, phase movement, Git, product/external expansion, runtime-sensitive work, or publication. |
| CommitAdviceRef | Advice only; exact paths only; never `git add .`; user performs Git manually. |

Reviewer approval is not Git approval. Integrator acceptance is not Git approval. Human user remains final commit authority.

## 26. P7 Peer Alignment Register

| Peer | Current status | Required marker | P7.0.F handling |
| --- | --- | --- | --- |
| P7.0.A Lead Gateway Alignment | Present and aligned by P7.0-NATIVE-ALIGN-01. | `resolved_by_alignment` | Consumes Manual Lead Agent, User Gateway, `ReviewRoutingRequest`, and `HumanDecisionPoint`. |
| P7.0.B Roadmap / Work Breakdown Alignment | Present and aligned by P7.0-NATIVE-ALIGN-01. | `resolved_by_alignment` | Consumes review object precedent and `ReviewerMeshProjection`. |
| P7.0.C Lane Taxonomy Alignment | Present and aligned by P7.0-NATIVE-ALIGN-01. | `resolved_by_alignment` | Consumes manual lanes, reviewer lane, integrator lane, and lane output posture as manual projections. |
| P7.0.D Context / Memory Manifest Alignment | Present and aligned by P7.0-NATIVE-ALIGN-01. | `resolved_by_alignment` | Consumes MemoryManifest, EvidencePack, context freshness, `ContradictionMarker`, and `EvidenceConflictMarker`. |
| P7.0.E Harness Boundary Alignment | Absent. | `pending_P7.0.E_harness_boundary_alignment` | Harness-specific reviewer execution remains undefined; no harness runtime, OpenCode/Hermes/MCP integration, hooks, or watch mode. |
| P7.0.G Integrator Commit Protocol Alignment | Not reviewed or consumed by P7.0.F. | `pending_P7.0.G_integrator_commit_protocol_alignment` | IntegratorAcceptance and commit posture remain metadata-only; exact Git command protocol awaits accepted P7.0.G alignment. |
| P7.0.H First Manual Pilot | Not started. | `P7.0.H_not_started_expected` | P7.0.F does not start a pilot. |
| P7.0.R Planning Closure | Not started. | `P7.0.R_not_started_expected` | P7.0.F does not close P7. |

If a future peer contradicts this contract, create an explicit reconciliation record rather than silently changing execution posture.

## 27. Product, External, Graphify, GBrain, And CSS Boundaries

| Surface | P7.0.F posture |
| --- | --- |
| Siamese/product | Product vision only. No product source inspection, product activation, product execution, product output tracking, or product-bound review beyond metadata. P4 required first. |
| Product Boundary ReviewerCell | May review product boundary metadata and blockers only. It may not inspect product source. |
| External sources | Candidate/review posture only. No external content inspection, adoption, copying, installation, execution, or instruction adoption. EXT.* required first. |
| External Boundary ReviewerCell | May review path/class metadata and approved safe metadata only. It may not inspect raw external source content. |
| `external/sources/gbrain-master` | Absent by path/class check in this P7.0.F sequence; if present later, remains path/class metadata only unless future exact review approves. |
| GBrain | Candidate notation only; not adopted, executed, dependency-approved, provider/auth-approved, MCP-active, Cadence-active, persistent, or substrate. |
| Hermes / Cadence | Future inactive references only. No always-on, scheduler, dream cycle, polling, or runtime. |
| Graphify | Supporting generated evidence only. No rerun, raw output inspection, authority, truth engine, adoption, source authority, or substrate inference. |
| Codegraph | Candidate/tooling boundary only. No execution or adoption. |
| Cognitive Semantic System | Accepted name; `cognitive_semantic_system_substrate_deferred`; markdown canonical docs plus metadata refs remain baseline. |
| Graph/vector/database/ontology | Candidate concepts only; no runtime, persistence, embeddings, or substrate selection. |

Reviewer mesh findings cannot promote product, external, GBrain, Hermes, Cadence, Graphify, Codegraph, or Cognitive Semantic System substrate posture.

## 28. Blocker And Pending Register

| Blocker | Status | Blocks |
| --- | --- | --- |
| `activation_level_transition_not_approved` | Active | AL transition and runtime activation. |
| `runtime_activation_not_approved` | Active | Scheduler, queue, worker, daemon, process lifecycle, autonomous loop, reviewer runtime. |
| `reviewer_runtime_not_approved` | Active | Live ReviewerMesh, auto-review, automatic reviewer assignment. |
| `automatic_approval_blocked` | Active | Auto-approval, AI self-approval, approval by evidence/validation/security/reviewer verdict. |
| `automatic_containment_blocked` | Active | Automatic quarantine, deletion, rollback, rejection, incident automation. |
| `automatic_rework_dispatch_blocked` | Active | Rework dispatch, task creation, handoff execution. |
| `automatic_integration_blocked` | Active | Automatic merge, integrator automation, Git mutation. |
| `agent_task_handoff_execution_blocked` | Active | Agent execution, task execution, handoff execution, dispatch. |
| `tool_execution_blocked` | Active | Shell, subprocess, package, build, test, tool, Git execution by agents. |
| `provider_auth_api_mcp_blocked` | Active | Provider calls, auth, network/API, MCP activation. |
| `secret_credential_content_blocked` | Active | Secret/credential inspection, use, printing, summarization, validation. |
| `source_loading_blocked` | Active | Source loading, product source inspection, external source inspection, GBrain source inspection. |
| `p4_required_before_product_bound_work` | Expected future blocker | Product-bound review beyond metadata and product activation. |
| `future_EXT_reviews_required_before_external_adoption` | Expected future blocker | External adoption, execution, dependency approval, source copying. |
| `future_EXT.GB_HARD_reviews_required_before_selection` | Expected future blocker | GBrain selection, adoption, dependency approval, provider/auth, MCP, Cadence, persistence, substrate. |
| `cognitive_semantic_system_substrate_deferred` | Active | Graph/vector/database/ontology/runtime substrate selection. |
| `generated_output_tracking_blocked` | Active | Generated/local-only output tracking and publication. |
| `source_tracking_git_publication_blocked` | Active | Staging, commit, push, force-add, publication without human gate. |
| `pending_P7.0.E_harness_boundary_alignment` | Pending peer alignment | Harness-specific review packaging and manual harness boundary details. |
| `pending_P7.0.G_integrator_commit_protocol_alignment` | Pending peer alignment | Detailed integrator and commit-advice protocol. |
| `P7.0.H_not_started_expected` | Expected absence | First manual pilot. |
| `P7.0.R_not_started_expected` | Expected absence | P7 planning closure. |

Blockers remain active until a future authorized record resolves them.

## 29. Stop Rules

STOP if any P7.0.F review path requires:

| Trigger | Required route |
| --- | --- |
| Reviewer runtime, live ReviewerMesh, auto-review, automatic reviewer assignment, auto-approval, AI self-approval, automatic quarantine, automatic rejection, or autonomous immune system | Stop and require future exact activation/reviewer-runtime gate. |
| Runtime activation, scheduler, queue, worker, daemon, autonomous loop, task execution, handoff execution, or orchestration | Stop and require future activation gate. |
| Tool, shell, subprocess, package, build, test, CI, Git mutation, or generated command execution | Stop and require exact future tool/security/Git gate. |
| Provider/auth/API/network/MCP call, credential use, token refresh, browser auth, local credential store, provider config, or API key use | Stop and require secure explicit future approval. |
| Secret or credential content | Stop; report safe metadata only. |
| Product source inspection, product execution, product dependency, product output tracking, or product activation | Stop and require P4/product gate. |
| External source inspection beyond authorized metadata, external execution, source copying, dependency adoption, or external instruction adoption | Stop and require EXT.* exact review. |
| GBrain/Hermes/Cadence adoption, execution, MCP activation, provider/auth approval, Cadence/always-on behavior, or memory runtime | Stop and require future exact EXT/governance gates. |
| Graphify rerun, raw output inspection, provider-labelled output, generated output tracking, Graphify adoption, or Codegraph execution/adoption | Stop and require future exact tooling/generated-output gate. |
| Cognitive Semantic System substrate selection, graph DB, vector DB, embeddings, ontology runtime, persistence, event stream, telemetry, monitoring runtime, or semantic memory | Stop and require future substrate decision gate. |
| Reviewer verdict treated as Git approval, runtime approval, product approval, publication approval, or activation approval | Stop and route to HumanFinalDecision/governance. |
| Evidence, validation, security, ApprovalRef, DecisionRef, path presence, registry presence, user intent, or context inclusion treated as approval | Stop and route to exact human/governance decision. |
| Source tracking expansion, force-add, staging, commit, push, broad Git advice, `git add .`, or publication | Stop; human user remains final Git authority. |
| Starting P7.0.E, P7.0.G, P7.0.H, P7.0.R, P7.1, P8, P4, EXT.*, runtime, product, external, substrate, generated-output tracking, source tracking, publication, or Git work inside P7.0.F | Stop and require separate explicit instruction. |

## 30. Future Validation Targets

Future validation targets are proposed only and were not executed:

| Target | Purpose |
| --- | --- |
| ReviewerMesh required fields completeness | Check mesh metadata fields. |
| ReviewerCell authority boundary completeness | Check no cell has runtime/Git/final approval authority. |
| ReviewerMeshNode metadata-only invariant | Check nodes are not runnable queue items. |
| ReviewRequest required fields completeness | Check request metadata. |
| ReviewInputPackage excluded-material invariant | Check no secrets, credentials, raw product/external/GBrain/Graphify material. |
| ReviewChecklist no-validation-execution invariant | Check checklist does not run commands. |
| ImmuneSafeguard no-enforcement invariant | Check safeguards are metadata only. |
| ImmuneCheck no-automation invariant | Check checks are manual and not detectors. |
| ReviewFinding safe-reporting completeness | Check findings preserve safe summary limits. |
| AnomalyMarker presence | Check anomaly marker schema. |
| DriftMarker presence | Check drift marker schema. |
| ContradictionMarker presence | Check contradiction marker schema. |
| EvidenceConflictMarker presence | Check evidence conflict marker schema. |
| UnsafeOutputMarker presence | Check unsafe output marker schema. |
| ScopeViolationMarker presence | Check scope violation marker schema. |
| ContainmentAction recommendation-only invariant | Check no automatic quarantine/deletion/rollback/rejection. |
| ReworkRequest no-dispatch invariant | Check rework requests are not tasks. |
| ReviewVerdict no-approval invariant | Check verdict is not approval or Git authority. |
| ApprovalEscalation metadata-only invariant | Check escalation is not notification/workflow runtime. |
| IntegratorAcceptance no-merge/no-Git invariant | Check integrator acceptance is not automatic integration or Git approval. |
| HumanFinalDecision explicitness invariant | Check no silent or inferred approval. |
| EvidenceRef supporting-only invariant | Check evidence supports, does not decide. |
| ValidationRef non-approval invariant | Check validation evaluates only. |
| SecurityRef non-activation invariant | Check security constrains only. |
| ApprovalRef is not approval invariant | Check no ref is treated as approval. |
| Product/external/GBrain/Graphify/CSS boundary invariant | Check candidate/evidence/deferred postures remain. |
| No runtime activation invariant | Check no runtime or reviewer automation is introduced. |
| No Git mutation and no `git add .` invariant | Check exact-path advice only. |
| P7 peer pending marker invariant | Check P7.0.E/G/H/R markers remain present until peers exist. |

## 31. Created / Not Created Register

| Artifact or action | P7.0.F status |
| --- | --- |
| `0_architecture/governance/agent_platform_reviewer_mesh_immune_safeguards_contract.md` | Created. |
| P7.0.A, P7.0.B, P7.0.C, P7.0.D | Not modified. |
| P7.0.E, P7.0.G, P7.0.H, P7.0.R | Not created or started. |
| P7.1, P8, P4, EXT.* | Not created or started. |
| Runtime implementation | Not created or modified. |
| Reviewer runtime, auto-review, automatic reviewer assignment, automatic approval | Not created or approved. |
| Autonomous reviewer mesh or autonomous immune system | Not created or approved. |
| Automatic containment, quarantine, rejection, rework dispatch, or integration | Not created or approved. |
| Agent runtime, task execution, handoff execution, scheduler, orchestration, autonomous loop | Not activated. |
| Validation, tests, CI, scripts, builds, package managers | Not run or approved. |
| Security enforcement, scanners, policy engines | Not run, created, or approved. |
| Provider/auth/API/MCP, network, credentials | Not configured, called, inspected, or used. |
| Product source, external source, GBrain source, Graphify source, raw generated output | Not inspected. |
| `9_artifacts/`, Graphify outputs, generated outputs | Not inspected, modified, or tracked. |
| Cognitive Semantic System substrate, graph DB, vector DB, embeddings, ontology runtime, persistence, telemetry, event stream | Not selected, created, or approved. |
| `.gitignore`, `.graphifyignore`, README.md, P6/P5/P4/P3/P2/P1/P0 docs | Not modified by P7.0.F. |
| Source tracking, staging, commit, push, force-add, publication | Not performed or approved. |

## 32. Final Verdict

| ID | Invariant |
| --- | --- |
| P70F-001 | P7.0.F creates the canonical Reviewer Mesh / Immune Safeguards Contract. |
| P70F-002 | ReviewerMesh is review topology metadata, not reviewer runtime. |
| P70F-003 | ImmuneSafeguard is safeguard metadata, not security enforcement or autonomous immune behavior. |
| P70F-004 | ReviewRequest is manual request metadata, not automatic reviewer assignment. |
| P70F-005 | ReviewInputPackage is bounded review context, not source loading permission. |
| P70F-006 | ReviewerCell and ReviewerMeshNode are manual projection objects, not active agents or runnable nodes. |
| P70F-007 | ReviewChecklist and ImmuneCheck are manual checks, not validation execution or scanners. |
| P70F-008 | ReviewFinding, AnomalyMarker, DriftMarker, ContradictionMarker, EvidenceConflictMarker, UnsafeOutputMarker, and ScopeViolationMarker are review cues and evidence, not automatic decisions. |
| P70F-009 | ContainmentAction is recommendation only, not automatic quarantine, deletion, rollback, rejection, or incident automation. |
| P70F-010 | ReworkRequest is not automatic rework dispatch. |
| P70F-011 | ReviewVerdict is not approval, Git approval, activation approval, product approval, publication approval, or final human decision. |
| P70F-012 | ApprovalEscalation is not escalation automation or notification runtime. |
| P70F-013 | IntegratorAcceptance is not automatic integration, merge automation, or Git approval. |
| P70F-014 | HumanFinalDecision must be explicit and cannot be inferred from silence, evidence, validation, security, ApprovalRef, DecisionRef, reviewer verdict, or user intent without exact scope. |
| P70F-015 | Evidence supports; it does not decide. |
| P70F-016 | Validation evaluates; governance decides. |
| P70F-017 | Security constrains; it does not activate. |
| P70F-018 | ApprovalRef is not approval. |
| P70F-019 | Reviewer approval is not Git approval. |
| P70F-020 | User remains final execution authority and final Git authority. |
| P70F-021 | `activation_level_transition: not_approved` remains active. |
| P70F-022 | `runtime_activation: not_approved` remains active. |
| P70F-023 | Product-bound work remains blocked pending P4. |
| P70F-024 | EXT.* remains required before external adoption. |
| P70F-025 | GBrain, Hermes, and Cadence remain future inactive candidates only. |
| P70F-026 | Graphify remains supporting generated evidence only, not authority. |
| P70F-027 | Cognitive Semantic System substrate remains deferred. |
| P70F-028 | No source loading, product source inspection, external source inspection, GBrain source inspection, raw generated output inspection, credential inspection, provider/auth use, API/network/MCP call, validation execution, security enforcement, tool execution, agent execution, or Git mutation is approved. |
| P70F-029 | P7.0.F records `pending_P7.0.E_harness_boundary_alignment`, `pending_P7.0.G_integrator_commit_protocol_alignment`, `P7.0.H_not_started_expected`, and `P7.0.R_not_started_expected`. |
| P70F-030 | P7.0.F stops before P7.0.E, P7.0.G, P7.0.H, P7.0.R, P7.1, P8, P4, EXT.*, runtime, product, external, substrate, generated-output tracking, source tracking, publication, and Git work. |

Final verdict: P7.0.F creates the canonical documentation-only Reviewer Mesh / Immune Safeguards Contract for AGENT PLATFORM / Siamese. It defines `ReviewerMesh`, `ImmuneSafeguard`, `ReviewRequest`, `ReviewInputPackage`, `ReviewerCell`, `ReviewerMeshNode`, `ReviewChecklist`, `ImmuneCheck`, `ReviewFinding`, `AnomalyMarker`, `DriftMarker`, `ContradictionMarker`, `EvidenceConflictMarker`, `UnsafeOutputMarker`, `ScopeViolationMarker`, `ContainmentAction`, `ReworkRequest`, `ReviewVerdict`, `ApprovalEscalation`, `IntegratorAcceptance`, and `HumanFinalDecision`. It preserves the manual review projection while modeling review as an agent-native safeguard mesh. It does not activate runtime, automate reviewers, approve work automatically, execute validation or security enforcement, inspect source, inspect product/external/GBrain/Graphify/raw generated outputs, use providers/auth/API/MCP, select substrate, track generated outputs, expand source tracking, publish, stage, commit, push, mutate Git, or start adjacent tickets.
