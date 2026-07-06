# P8.4 - Local Workspace / State Model

## Document Header
| Field | Value |
|---|---|
| Title | Local Workspace / State Model |
| Ticket | P8.4 |
| Status | Accepted local workspace / state model |
| Date | 2026-07-06 |
| Scope | Documentation-only local workspace / state architecture for AGENT PLATFORM / Siamese MVP-0. |
| Authority | Local workspace / state architecture only, not workspace implementation, runtime activation, autonomous orchestration, automatic dispatch, automatic handoff, automatic reviewer assignment, automatic integration, automatic context retrieval, persistent memory, live retrieval, GBrain runtime, GStack runtime, Hermes runtime, Cadence, provider/auth/API/MCP activation, tool execution, OpenCode execution, agent execution, reviewer execution, integrator execution, source loading, source inspection, product source inspection, external source inspection, Graphify adoption/rerun, Codegraph execution, vector DB, embeddings, graph DB, ontology runtime, generated output tracking, source tracking expansion, publication, Git mutation, or Cognitive Semantic System substrate selection. |
| Related documents | P8.0, P8.1 if present, P8.2 if present, P8.3 if present, P8.5 if present, P7.R, P7.0.H, P7.0.A-P7.0.G, P7.0.0, P6.7, P6.1-P6.6, P5.R, P3.BR, P3.3, P3.4, P3.5, P3.R, P3.0, P3.1, P3.2, P2.KR, P2.1, P2.2, P2.3, P1.1, P1.2, P1.3, P1.4, P1.5, P0.1, P0.2, P0.3, S-03, S-04, CSS ADR/audit, Graphify Repo Map Summary, README, `.gitignore`, `.graphifyignore`. |
| Output | Local workspace / state model. |

P8 builds an interactive MVP layer.

## Purpose
P8 creates a Platform MVP / Interaction Layer.

P8.4 defines the local state model required by MVP-0.

P8.4 defines where session state, draft work packets, harness inputs, returned harness outputs, pasted harness outputs, review records, integration records, commit candidates, audit records, local-only artifacts, ignored/generated artifacts, generated artifacts, retention records, rollback records, and incident records should be represented.

P8.4 supports a future local interactive manual workflow assistant.

P8.4 supports this MVP-0 direction: AGENT PLATFORM local MVP captures user objective, generates WorkPacket / HarnessInputPackage, records context / memory / evidence, allows user to paste OpenCode or other harness output, structures HarnessOutputPackage, assists review checklist, assists integration checklist, renders exact-path CommitCandidate, and leaves Git decisions and execution to the user.

P8.4 does not implement local storage.

P8.4 does not create workspace files.

P8.4 does not create a database.

P8.4 does not activate runtime.

P8.4 does not execute harnesses.

P8.4 does not mutate Git.

## Current Posture
| Posture | Statement |
|---|---|
| P8.0 prerequisite | P8.0 must define MVP scope and external integration boundary before P8.4. P8.0 is present. |
| Round | P8.4 is one Round 1 parallel architecture ticket after P8.0. |
| Sibling posture | P8.4 may proceed in parallel with P8.1, P8.2, P8.3, and P8.5. |
| Missing siblings | P8.4 must mark pending alignment for missing sibling docs. |
| MVP-0 intent | MVP-0 is intended as local interactive manual workflow assistant. |
| Autonomy | MVP-0 is not autonomous runtime. |
| Product | MVP-0 is not product generator. |
| OpenCode | MVP-0 is not OpenCode executor. |
| Provider/API/MCP | MVP-0 is not provider/API/MCP runtime. |
| GBrain/GStack/Hermes/Cadence | MVP-0 is not GBrain/GStack/Hermes/Cadence runtime. |
| Graphify | MVP-0 is not Graphify runtime. |
| Git | MVP-0 keeps Git manual. |
| Final authority | The user remains final commit authority. |

## Inputs Reviewed
| Input | Expected role | Present / missing | State-model use | Blocking consequence if missing |
|---|---|---|---|---|
| P8.0 Platform MVP Scope / External Integration Boundary | Required P8 prerequisite. | Present. | Defines MVP scope and external boundary. | If missing, STOP with `missing_P8.0_platform_mvp_scope_external_integration_boundary`. |
| P8.1 External Source Inventory / Classification, if present | Optional P8 sibling. | Missing. | Would align external source inventory. | `pending_P8.1_external_inventory_alignment`. |
| P8.2 MVP Interaction Surface Architecture, if present | Optional P8 sibling. | Missing. | Would align UI/interaction surfaces. | `pending_P8.2_interaction_surface_alignment`. |
| P8.3 Core Workflow Schema Candidates, if present | Optional P8 sibling. | Missing. | Would align schema object naming. | `pending_P8.3_core_schema_alignment`. |
| P8.5 Security / Activation Gate Model, if present | Optional P8 sibling. | Missing. | Would align security gates. | `pending_P8.5_security_gate_alignment`. |
| P7.R Manual Agentic Workflow Planning Closure | Manual workflow closure. | Present. | P7 manual workflow baseline. | P7 closure alignment incomplete if absent. |
| P7.0.H First Manual Agent-Native Pilot Playbook | Manual pilot playbook. | Present. | MVP-0 workflow source. | Pilot alignment incomplete if absent. |
| P7.0.A Manual Lead Agent / User Gateway Contract | User gateway. | Present. | User objective and manual authority state. | Gateway alignment incomplete if absent. |
| P7.0.B Roadmap Generation / Work Breakdown Contract | Work breakdown. | Present. | Draft work packet and roadmap refs. | Roadmap alignment incomplete if absent. |
| P7.0.C Parallel Agent Lane / Work Packet Taxonomy | Work packet/lane taxonomy. | Present. | Manual lane and work packet refs. | Lane alignment incomplete if absent. |
| P7.0.D Manual Context / Memory Manifest Strategy | Context/memory manifest. | Present. | Context, memory, freshness, source refs. | Context state alignment incomplete if absent. |
| P7.0.E Manual Harness Strategy / OpenCode-Hermes Boundary | Harness boundary. | Present. | HarnessInputDraft and harness output intake boundaries. | Harness alignment incomplete if absent. |
| P7.0.F Reviewer Agent / Approval Pipeline Contract | Reviewer pipeline. | Missing. | Would align review state. | Review state carries limitation until reviewer pipeline is present. |
| P7.0.G Integrator / Reconciliation / Commit Advisory Protocol | Integration and commit advisory. | Present. | Integration records and CommitCandidate model. | Integrator alignment incomplete if absent. |
| P6.7 Operational Readiness Audit | Operational baseline. | Present. | P6 closure posture. | P6 closure alignment incomplete if absent. |
| P6.4 Human Approval / Review Loop Operational Contract | Approval boundary. | Present. | Human approval requirements and review refs. | Approval boundary incomplete if absent. |
| P6.5 Runtime Monitoring / Incident Handling Operational Contract | Monitoring/incident boundary. | Present. | IncidentStateRecord and incident posture. | Incident state alignment incomplete if absent. |
| P5.R Minimal Active Agent Platform Audit | Skeleton baseline. | Present. | Prevents MVP-0 from activating runtime skeleton. | Runtime skeleton baseline incomplete if absent. |
| P3.BR Activation Decision Reconciliation Closure | Activation decision closure. | Present. | Decision-is-not-execution posture. | Activation decision alignment incomplete if absent. |
| P3.0 Controlled Source Classification Readiness | Source classification. | Present. | Artifact and source classification posture. | Source classification incomplete if absent. |
| P3.1 Validation Execution Readiness | Validation readiness. | Present. | Validation boundary. | Validation posture incomplete if absent. |
| P3.2 Security Enforcement Readiness | Security readiness. | Present. | Security blockers. | Security posture incomplete if absent. |
| P2.KR Knowledge / Retrieval Architecture Reconciliation Closure | Knowledge/retrieval posture. | Present. | Blocks automatic retrieval and substrate assumptions. | Retrieval posture incomplete if absent. |
| P2.1 Shared Metadata Vocabulary Alignment | Vocabulary. | Present. | State object naming. | Vocabulary alignment incomplete if absent. |
| P2.2 EvidenceRef Contract | Evidence refs. | Present. | Harness output and evidence package posture. | Evidence semantics incomplete if absent. |
| P2.3 Audit / Retention / Rollback Baseline | Lifecycle baseline. | Present. | Audit, retention, rollback, incident posture. | Lifecycle posture incomplete if absent. |
| P1.1 Context Runtime Contract Hardening | Context boundary. | Present. | Context is not source loading. | Context boundary incomplete if absent. |
| P1.4 Agent Runtime Boundary Contract Hardening | Agent boundary. | Present. | State is not agent runtime. | Agent boundary incomplete if absent. |
| S-03 Tool / Shell / Network / MCP Execution Policy | Tool/network/MCP boundary. | Present. | Blocks tool/MCP/network state activation. | Execution policy incomplete if absent. |
| S-04 Local-Only Secrets / Credentials Policy | Secrets/credentials boundary. | Present. | Secrets and credentials are never state content. | Secret boundary incomplete if absent. |
| CSS ADR/audit | Cognitive Semantic System naming and substrate posture. | Present. | Preserves substrate deferral. | CSS posture incomplete if absent. |
| Graphify Repo Map Summary | Curated Graphify evidence. | Present. | Graphify evidence boundary only. | Graphify evidence alignment incomplete if absent. |
| README | Repository posture. | Present. | Boundary context only. | Repo posture incomplete if absent. |
| `.gitignore` | Ignore boundary. | Present. | Ignored artifact posture; not modified. | Ignore boundary incomplete if absent. |
| `.graphifyignore` | Graphify ignore boundary. | Present. | Generated Graphify boundary; not modified. | Graphify ignore boundary incomplete if absent. |

## Dependency Posture
If P8.0 is missing, STOP with `missing_P8.0_platform_mvp_scope_external_integration_boundary`.

P8.1 is missing, so P8.4 records `pending_P8.1_external_inventory_alignment`.

P8.2 is missing, so P8.4 records `pending_P8.2_interaction_surface_alignment`.

P8.3 is missing, so P8.4 records `pending_P8.3_core_schema_alignment`.

P8.5 is missing, so P8.4 records `pending_P8.5_security_gate_alignment`.

P8.4 must not synthesize missing sibling documents.

P8.4 must not create P8.10.

P8.4 must not start implementation tickets.

## Local Workspace Design Principles
| Principle | Meaning | P8.4 consequence | Blocked interpretation | Future gate if needed |
|---|---|---|---|---|
| local_first | MVP-0 state is local by design. | Use local-only candidate posture. | Publication or remote sync. | P8.10/P8.11 plus human approval. |
| manual_first | User manually drives harnesses and Git. | User-pasted harness outputs and advisory Git only. | Automation. | Future exact gate. |
| file_based_candidate | Candidate storage can be simple files. | markdown/json local files may be proposed as architecture. | Creating files now. | P8.10/P8.11. |
| markdown_json_candidate | Candidate local state representation can be markdown/json local files. | Markdown/json local file model is not database implementation. | JSON/markdown runtime state files now. | Implementation ticket. |
| database_deferred | Database is not needed for MVP-0 architecture baseline. | No database. | Persistence layer. | Future storage gate. |
| runtime_state_deferred | Runtime state is deferred. | State model is architecture only. | Agent runtime state. | Future runtime gate. |
| external_runtime_deferred | External candidates stay inactive. | No GBrain/GStack/Hermes/OpenCode runtime state. | Candidate adoption. | P8.6-P8.9 or later. |
| product_state_blocked_by_default | Product/Siamese state is blocked. | No product source state. | Product-bound MVP state. | P4/product gate. |
| generated_artifacts_not_source_by_default | Generated output remains generated. | Generated artifact is not source by default. | Treating generated output as source. | Tracking approval gate. |
| local_only_by_default_for_session_artifacts | Session artifacts are local-only by default. | Local-only artifact is not publishable by default. | Publishing local session records. | Publication gate. |
| exact_path_git_advisory_only | Commit advice uses exact paths only. | CommitCommandBlock is advisory only. | Broad Git commands. | Human approval. |
| no_git_mutation_by_agent | Agent never mutates Git. | The user remains final commit authority. | Agent commit/push/stage. | None in P8.4. |

## Local Workspace Boundary Model
Candidate state boundaries:

| Boundary candidate | Meaning | P8.4 posture |
|---|---|---|
| workspace_root_candidate | Candidate root for future local workspace. | Architecture candidate only. |
| session_space_candidate | Candidate session state area. | No directories created. |
| draft_space_candidate | Candidate draft work packet area. | No files created. |
| harness_input_space_candidate | Candidate harness input package area. | No harness execution. |
| harness_output_intake_space_candidate | Candidate user-pasted output intake area. | No parser implementation. |
| review_space_candidate | Candidate review records area. | No auto-review. |
| integration_space_candidate | Candidate integration records area. | No automatic integration. |
| commit_candidate_space_candidate | Candidate commit advisory records area. | No Git mutation. |
| audit_space_candidate | Candidate audit records area. | No telemetry runtime. |
| local_artifact_space_candidate | Candidate local-only artifacts area. | Not publishable by default. |
| generated_artifact_space_candidate | Candidate generated artifact references area. | Not source by default. |
| ignored_artifact_space_candidate | Candidate ignored artifact references area. | Not tracking approval. |
| quarantine_space_candidate | Candidate quarantine references area. | Not publishable. |

These are candidate boundaries only.

P8.4 must not create directories.

P8.4 must not create files.

P8.4 must not define final implementation paths unless marked candidate.

P8.4 must preserve future P8.10/P8.11 synthesis authority.

## Recommended MVP-0 Storage Posture
MVP-0 should start with markdown/json local files as a candidate architecture.

No database.

No persistent DB.

No vector DB.

No graph DB.

No GBrain runtime memory.

No automatic retrieval.

No live retrieval.

No live connector state.

No product source state.

No external runtime state.

No credential state.

No provider auth state.

No telemetry/event stream.

No generated output tracking by default.

No source tracking expansion by default.

## Local Workspace Object Model
| Object | Meaning | Required fields | Forbidden fields | Security posture | Validation posture | Activation posture |
|---|---|---|---|---|---|---|
| LocalWorkspace | Candidate architecture root for MVP-0 local workspace. | ID, name, scope, owner, candidate storage mode, allowed/blocked surfaces. | Runtime config, credentials, final paths as implementation. | Local-only by default. | Not validation. | Not implementation. |
| WorkspaceSession | Manual session state candidate. | ID, owner, status, refs, freshness, retention, rollback, incident. | Agent runtime state. | No secrets or credentials. | State completeness is not validation. | Not autonomous runtime state. |
| SessionManifest | Manifest of session refs and blockers. | Session refs, artifacts, decisions, limits, stop rules. | Source contents, product source. | Preserves blockers. | Not validation. | Not runtime. |
| UserObjectiveState | Captured user objective metadata. | Objective, owner, scope, limits, sensitivity, blockers. | Product data unless gated. | Unknown sensitivity blocks. | Not validation. | Not execution. |
| DraftWorkPacketRecord | Draft work packet state. | Work packet refs, context, expected output, review/integration needs. | Dispatch config. | Preserves source classification. | Draft state is not accepted output. | Not dispatch. |
| HarnessInputDraft | Candidate harness input package. | Work packet, harness class, context refs, allowed manual use. | Harness credentials, runtime config. | Copy/paste boundary. | Not validation. | Not harness execution. |
| HarnessOutputIntakeRecord | User-pasted harness output intake state. | Work packet, submitted by, output boundary, classification, quarantine flags. | Secret/credential content, accepted output by default. | Generated evidence by default. | Must be reviewed. | Not harness execution. |
| HarnessOutputPackageRecord | Structured returned harness outputs. | Output refs, source posture, review status, blockers. | Auto-accepted output. | Generated evidence by default. | Requires review. | Not integration. |
| ReviewChecklistState | Checklist state for manual review. | Checklist items, refs, scope, limitations. | Auto-review logic. | Preserves blockers. | Checklist is not validation execution. | Not auto-review. |
| ReviewRecord | Manual review record. | Reviewer ref, scope, findings, blockers, limitations. | Git approval. | Review cannot bypass security. | Not validation execution. | Not auto-review. |
| ReviewVerdictRecord | Review verdict metadata. | Verdict, scope, reasons, limitations, follow-up. | Final Git authority. | Cannot override blockers. | Not validation. | Not Git approval. |
| IntegrationChecklistState | Checklist for manual integration. | Items, accepted/rejected refs, drift refs. | Automatic integration logic. | Preserves blockers. | Not validation execution. | Not automatic integration. |
| IntegrationRecord | Manual integration record. | Inputs, outputs, decisions, drift, limitations. | Merge execution. | Preserves blockers. | Not validation. | Not Git mutation. |
| IntegrationSummaryRecord | Summary of manual integration. | Accepted outputs, rejected outputs, drift, follow-ups. | Commit approval. | Preserves incident posture. | Not validation. | Advisory only. |
| DriftRegisterState | Drift and unresolved difference register. | Drift item, severity, owner, resolution/limitation. | Silent resolution. | Sensitive drift triggers incident posture. | Not validation. | Not automation. |
| AcceptedOutputRegisterState | Register of outputs accepted for integration consideration. | Output refs, review refs, limitations. | Commit approval. | Must preserve blockers. | Not validation. | Not Git approval. |
| RejectedOutputRegisterState | Register of rejected outputs. | Output refs, reasons, rollback/incident posture. | Deletion approval. | Preserves safety. | Not validation. | Not automation. |
| CommitCandidateRecord | Candidate exact-path commit package. | Paths, excluded paths, message candidate, rollback note, human approval required. | Git mutation. | Exact paths only. | Not validation. | Not Git mutation. |
| CommitCommandBlockRecord | Advisory Git command block metadata. | Exact add paths, commit message candidate, push target candidate, warnings. | Broad `git add` advice. | Blocks generated/product paths unless gated. | Not validation. | Advisory only. |
| GitAdvisoryRecord | Advisory Git decision record. | Candidate, owner, limitations, user action required. | Agent-executed Git. | Preserves user authority. | Not validation. | Not mutation. |
| AuditLogRecord | Audit model record. | Event type, actor, refs, timestamp, posture. | Telemetry stream. | No secrets/credentials. | Not validation. | Not telemetry runtime. |
| LocalArtifactRef | Local-only artifact metadata ref. | Artifact ID, class, local-only posture, retention. | Publication by default. | Local-only. | Not validation. | Not publishable. |
| GeneratedArtifactRef | Generated artifact metadata ref. | Artifact ID, generator/source refs, tracking posture. | Source posture by default. | Generated output blockers. | Not validation. | Not tracking approval. |
| IgnoredArtifactRef | Ignored artifact metadata ref. | Path/ref, ignore posture, tracking posture. | Deletion/tracking approval. | Local-only unless gated. | Not validation. | Not tracking approval. |
| QuarantineArtifactRef | Quarantine metadata ref. | Artifact ref, reason, incident route, retention. | Publication. | STOP and safe reporting. | Not validation. | Not publishable. |
| RetentionStateRecord | Retention posture metadata. | Retention class, owner, limits. | Persistence implementation. | Sensitive data limits. | Not validation. | Not database. |
| RollbackStateRecord | Rollback posture metadata. | Affected refs, rollback note, owner, limitations. | Automatic rollback. | Preserves incident posture. | Not validation. | Not automation. |
| IncidentStateRecord | Incident posture metadata. | Trigger, route, owner, limitations. | Incident automation. | Required for sensitive surfaces. | Not validation. | Not runtime monitoring. |
| StateIndexCandidate | Candidate local index of refs. | Ref list, scope, freshness, limits. | Search DB, vector index. | No source contents. | Not validation. | Not index implementation. |
| WorkspaceStopRule | State stop rule. | Condition, consequence, required human action. | Auto-waiver. | Stops on security blockers. | Not validation. | Blocks activation. |

## LocalWorkspace Contract
LocalWorkspace fields:

| Field | Requirement |
|---|---|
| workspace_id | Stable metadata identifier. |
| workspace_name | Human-readable name. |
| workspace_scope | Exact MVP-0 local workspace scope. |
| workspace_owner | Accountable owner. |
| mvp_level | MVP-0. |
| storage_mode_candidate | markdown/json local files candidate posture. |
| root_path_candidate | Candidate root only; not directory creation. |
| allowed_state_surfaces | Allowed candidate state surfaces. |
| blocked_state_surfaces | Blocked state surfaces. |
| session_refs | WorkspaceSession refs. |
| artifact_refs | Artifact refs. |
| retention_policy_ref | Retention policy ref. |
| rollback_policy_ref | Rollback policy ref. |
| incident_policy_ref | Incident policy ref. |
| source_classification_posture | P3.0/P8.0 posture. |
| sensitivity_posture | Sensitivity posture. |
| local_only_posture | Local-only posture. |
| generated_output_posture | Generated output posture. |
| git_tracking_posture | Tracking posture. |
| review_required | Review requirement. |
| human_owner | Human owner. |
| stop_rules | Stop rules. |
| limitations | Limitations. |

LocalWorkspace is architecture metadata, not implementation.

LocalWorkspace does not create directories.

LocalWorkspace does not activate runtime.

## WorkspaceSession Contract
WorkspaceSession fields:

| Field | Requirement |
|---|---|
| session_id | Stable identifier. |
| session_title | Human-readable title. |
| session_owner | Accountable owner. |
| session_status | Session status. |
| user_objective_ref | User objective ref. |
| roadmap_ref | Roadmap ref. |
| work_packet_refs | Work packet refs. |
| harness_input_refs | Harness input refs. |
| harness_output_refs | Harness output refs. |
| review_refs | Review refs. |
| integration_refs | Integration refs. |
| commit_candidate_refs | Commit candidate refs. |
| audit_refs | Audit refs. |
| created_at | Creation metadata timestamp. |
| updated_at | Updated metadata timestamp. |
| freshness_marker | Freshness marker. |
| retention_posture | Retention posture. |
| rollback_posture | Rollback posture. |
| incident_posture | Incident posture. |
| local_only | Local-only posture. |
| review_required | Review requirement. |
| blockers | Blockers. |
| limitations | Limitations. |

WorkspaceSession is local manual session state candidate.

WorkspaceSession is not autonomous runtime state.

WorkspaceSession is not agent execution state.

WorkspaceSession is not persistent memory.

## Session Status Model
Allowed session statuses:

| Status | Meaning |
|---|---|
| draft_metadata_only | Draft metadata, no execution. |
| active_manual_session | Manual session active. |
| waiting_for_user_input | Waiting for user input. |
| waiting_for_manual_harness_output | Waiting for user to paste harness output. |
| waiting_for_review | Waiting for manual review. |
| waiting_for_integration | Waiting for manual integration. |
| waiting_for_human_git_decision | Waiting for user Git decision. |
| closed_accepted | Closed with accepted outcome. |
| closed_rejected | Closed with rejected outcome. |
| closed_with_limitations | Closed with limitations. |
| blocked | Blocked. |
| quarantined | Quarantined. |
| superseded | Superseded. |
| archived_local_only | Archived local-only. |

No status may imply autonomous execution.

No status may imply Git mutation.

No status may imply tool/provider/agent execution.

## Draft Work Packet State
DraftWorkPacketRecord fields:

| Field | Requirement |
|---|---|
| draft_work_packet_id | Stable identifier. |
| source_user_objective_ref | Source objective ref. |
| roadmap_ref | Roadmap ref. |
| task_graph_ref | Task graph ref. |
| blackboard_ref | Blackboard ref. |
| manual_lane_ref | Manual lane ref. |
| harness_target_candidate | Harness target candidate. |
| context_manifest_ref | Context/memory manifest ref. |
| input_package_ref | HarnessInputPackage ref. |
| expected_output_contract | Expected output contract. |
| review_requirement | Review requirement. |
| integration_requirement | Integration requirement. |
| source_classification | Source classification. |
| sensitivity | Sensitivity. |
| allowed_use | Allowed use. |
| forbidden_use | Forbidden use. |
| retention_posture | Retention posture. |
| rollback_posture | Rollback posture. |
| incident_posture | Incident posture. |
| status | Draft status. |
| blockers | Blockers. |
| limitations | Limitations. |

DraftWorkPacketRecord is not dispatch.

DraftWorkPacketRecord is not agent execution.

DraftWorkPacketRecord is not harness execution.

## Harness Input State
HarnessInputDraft fields:

| Field | Requirement |
|---|---|
| harness_input_id | Stable identifier. |
| work_packet_ref | Work packet ref. |
| harness_class | Harness class. |
| harness_mode | Harness mode. |
| target_harness_candidate | Target harness candidate. |
| input_body_ref | Input body ref. |
| context_pack_refs | Context pack refs. |
| evidence_pack_refs | Evidence pack refs. |
| allowed_manual_use | Allowed manual use. |
| forbidden_use | Forbidden use. |
| copy_paste_boundary | Copy/paste boundary. |
| source_classification | Source classification. |
| sensitivity | Sensitivity. |
| secret_credential_policy | Secret/credential policy. |
| product_boundary_policy | Product boundary policy. |
| external_boundary_policy | External boundary policy. |
| retention_posture | Retention posture. |
| rollback_posture | Rollback posture. |
| incident_posture | Incident posture. |
| status | Status. |
| blockers | Blockers. |
| limitations | Limitations. |

HarnessInputDraft may be manually copied by user in H0 mode.

HarnessInputDraft does not execute OpenCode.

HarnessInputDraft does not call any harness.

HarnessInputDraft does not activate provider/auth/API/MCP.

## Harness Output Intake State
HarnessOutputIntakeRecord fields:

| Field | Requirement |
|---|---|
| harness_output_intake_id | Stable identifier. |
| work_packet_ref | Work packet ref. |
| harness_class | Harness class. |
| harness_mode | Harness mode. |
| submitted_by | Submitter, usually user. |
| submission_method | Paste/manual intake method. |
| raw_output_boundary | Raw output boundary. |
| structured_output_ref | HarnessOutputPackage ref. |
| source_classification | Source classification. |
| sensitivity | Sensitivity. |
| generated_output_related | Generated output flag. |
| secret_credential_scan_posture_metadata | Metadata posture only, not scanner execution. |
| product_boundary_flags | Product boundary flags. |
| external_boundary_flags | External boundary flags. |
| accepted_for_review | Whether accepted for review. |
| quarantine_required | Quarantine flag. |
| retention_posture | Retention posture. |
| rollback_posture | Rollback posture. |
| incident_posture | Incident posture. |
| status | Status. |
| blockers | Blockers. |
| limitations | Limitations. |

Harness output is user-pasted output.

Harness output is generated evidence by default.

Harness output is not accepted output.

Harness output must be reviewed before integration.

Harness output must be blocked/quarantined if it contains secrets, credentials, product source, raw external source, raw Graphify output, unknown sensitivity, or forbidden material.

## Review State Model
ReviewChecklistState, ReviewRecord, and ReviewVerdictRecord represent manual review state.

Allowed review verdicts:

| Verdict | Meaning |
|---|---|
| accepted | Accepted for integration consideration. |
| accepted_with_limitations | Accepted with explicit limitations. |
| needs_rework | Requires rework. |
| blocked | Blocked. |
| out_of_scope | Out of scope. |

Review state is not auto-review.

Review verdict is not Git approval.

Review verdict is not human final authority.

Review state must preserve checklist inputs, evidence refs, blockers, limitations, and reviewer scope.

## Integration State Model
IntegrationChecklistState, IntegrationRecord, IntegrationSummaryRecord, DriftRegisterState, AcceptedOutputRegisterState, and RejectedOutputRegisterState represent manual integration state.

Integration state is not automatic integration.

Integration state is not merge.

Integration state is not Git mutation.

Drift remains open until manually resolved or accepted as limitation.

AcceptedOutputRegister is not commit approval.

RejectedOutputRegister must preserve reason and rollback/incident posture where applicable.

## Commit Candidate State Model
CommitCandidateRecord, CommitCommandBlockRecord, and GitAdvisoryRecord represent exact-path commit advisory state.

Required fields:

| Field | Requirement |
|---|---|
| commit_candidate_id | Stable identifier. |
| source_ticket_ref | Source ticket ref. |
| accepted_output_refs | Accepted output refs. |
| modified_path_refs | Exact modified path refs. |
| created_path_refs | Exact created path refs. |
| excluded_path_refs | Excluded path refs. |
| generated_output_refs | Generated output refs. |
| ignored_artifact_refs | Ignored artifact refs. |
| git_add_paths_exact | Exact add paths only. |
| commit_message_candidate | Commit message candidate. |
| push_target_candidate | Push target candidate. |
| rollback_note | Rollback note. |
| human_approval_required | Human approval requirement. |
| git_mutation_forbidden_for_agent | Must be true. |
| never_git_add_dot | Must be true. |
| retention_posture | Retention posture. |
| incident_posture | Incident posture. |
| limitations | Limitations. |

CommitCandidate is not Git mutation.

CommitCommandBlock is advisory only.

The agent never mutates Git.

The user commits and pushes manually.

Never recommend git add ..

## Audit Log State Model
AuditLogRecord fields:

| Field | Requirement |
|---|---|
| audit_record_id | Stable identifier. |
| session_ref | Session ref. |
| event_type | Event type. |
| event_summary | Event summary. |
| actor_ref | Actor ref. |
| manual_or_automated | Manual/automated marker; P8.4 is manual architecture only. |
| source_refs | Source refs. |
| evidence_refs | Evidence refs. |
| validation_refs | Validation refs. |
| security_refs | Security refs. |
| retention_refs | Retention refs. |
| rollback_refs | Rollback refs. |
| incident_refs | Incident refs. |
| timestamp | Metadata timestamp. |
| local_only | Local-only flag. |
| generated_output_related | Generated output flag. |
| limitations | Limitations. |

Audit log model is not telemetry runtime.

Audit log model is not event streaming.

Audit log model is not persistence implementation.

Audit log records must not contain secrets or credentials.

## Artifact Classification Model
| Artifact class | Meaning | Default tracking posture | Retention posture | Allowed MVP-0 use | Blocked use |
|---|---|---|---|---|---|
| local_session_artifact | Local session metadata candidate. | Not tracked by default. | Local-only. | Manual session reference. | Publication by default. |
| draft_work_packet_artifact | Draft work packet artifact. | Not tracked until approved. | Local-only until accepted. | Drafting. | Treated as accepted output. |
| harness_input_artifact | Harness input draft. | Not tracked by default. | Local-only. | User copy/paste. | Harness execution. |
| user_pasted_harness_output_artifact | User-pasted harness output. | Generated artifact, not source by default. | Review/quarantine posture. | Review intake. | Accepted output by default. |
| review_record_artifact | Review record. | Candidate exact tracking only after approval. | Retain with session. | Manual review history. | Git approval. |
| integration_record_artifact | Integration record. | Candidate exact tracking only after approval. | Retain with session. | Manual integration history. | Automatic merge. |
| commit_candidate_artifact | Commit advisory artifact. | Candidate exact tracking only after approval. | Retain with session. | Exact-path advisory. | Git mutation. |
| audit_record_artifact | Audit model artifact. | Candidate exact tracking only after approval. | Retain per audit posture. | Audit trace. | Telemetry/event streaming. |
| generated_artifact | Generated output. | Not source by default. | Local-only/generated posture. | Review evidence. | Source by default. |
| ignored_artifact | Ignored/local artifact. | Ignored unless future exact tracking approval. | Local-only. | Boundary reference. | Delete/track approval. |
| quarantined_artifact | Quarantined artifact. | Not tracked. | Incident/quarantine posture. | Safe reporting route. | Publication. |
| raw_external_artifact | Raw external source/content artifact. | Blocked. | Quarantine/incident if encountered. | None by default. | Persistence/tracking. |
| raw_product_artifact | Raw product/Siamese artifact. | Blocked. | Quarantine/incident if encountered. | None by default. | Persistence/tracking. |
| secret_credential_artifact | Secret/credential material. | Never tracked. | Do not persist as content. | Safe reporting metadata only. | Persistence, copying, publication. |
| unknown_sensitivity_artifact | Unknown sensitivity material. | Blocked. | Quarantine until classified. | Safe limitation marker. | Persistence/tracking. |

Generated artifact is not source by default.

Ignored artifact is not approval to delete or track.

Quarantined artifact is not publishable.

Secret/credential artifact must never be persisted as content.

Raw product artifact is blocked.

Raw external artifact is blocked unless future exact gate allows.

## State Lifecycle Model
Lifecycle states:

| Lifecycle state | Meaning |
|---|---|
| created | Metadata object created conceptually. |
| drafted | Draft state. |
| ready_for_manual_harness | Ready for user to run external harness manually. |
| waiting_for_manual_output | Waiting for user-pasted output. |
| output_received | Harness output pasted by user. |
| quarantined | Quarantined. |
| ready_for_review | Ready for manual review. |
| reviewed | Reviewed. |
| needs_rework | Needs rework. |
| ready_for_integration | Ready for manual integration. |
| integrated | Integrated conceptually. |
| commit_candidate_rendered | Commit candidate rendered conceptually. |
| waiting_for_user_git_decision | Waiting for user Git decision. |
| closed | Closed. |
| archived_local_only | Archived local-only. |
| superseded | Superseded. |
| deleted_by_manual_policy | Deleted by manual policy. |

Lifecycle is not automation.

Lifecycle transition does not execute external action.

Lifecycle transition does not mutate Git.

Lifecycle transition must preserve retention, rollback, incident, and blockers.

## Local-Only / Generated / Ignored Handling
Local-only artifacts remain local by default.

Generated artifacts remain generated and non-source by default.

Ignored artifacts remain ignored unless future exact tracking decision approves otherwise.

Generated outputs under `9_artifacts` remain blocked unless future exact tracking approval exists.

Graphify outputs remain generated evidence only.

No generated output tracking is approved by P8.4.

No source tracking expansion is approved by P8.4.

No Git mutation is approved by P8.4.

## Security Boundary
Secrets and credentials are never state content.

API keys, tokens, passwords, private keys, OAuth sessions, browser auth, provider configs, token stores, local credential stores, `.env`, and credential values are never workspace state.

Provider auth material must not be stored.

Unknown sensitivity blocks persistence.

Product/Siamese source is blocked.

External source contents are blocked unless future exact review approves.

Raw Graphify output is blocked.

Raw live connector payloads are blocked.

Customer-sensitive data is blocked unless future exact review approves.

Security constrains; it does not activate.

## Validation Boundary
Validation evaluates; governance decides.

State completeness is not validation execution.

State model does not run checks.

Review checklist state is not validation execution.

No tests, scripts, CI, build, lint, typecheck, or validation commands are approved by P8.4.

## Source Classification Boundary
Source classification is not source loading permission.

Path presence is not content inspection permission.

LocalWorkspace path candidate is not directory creation permission.

FileRef is not file read permission.

ArtifactRef is not tracking permission.

P8.4 must preserve P3.0 source classification posture.

P8.4 must preserve P8.0 external integration boundary.

## External Candidate Boundary
Graphify evidence may remain read-only evidence candidate only.

GBrain may remain memory architecture candidate only.

GStack may remain GBrain-compatible skill stack candidate only.

Hermes may remain interface/runtime candidate only.

OpenCode may remain H0 user-operated harness only.

P8.4 must not activate any candidate.

P8.4 must not create candidate runtime state.

P8.4 must not inspect external source contents.

External path metadata posture: `external/sources/gbrain-master`, `external/sources/gstack`, `external/sources/gstack-master`, `external/sources/hermes`, and `external/sources/graphify` were absent in boundary checks and were not inspected.

## Product / Siamese Boundary
Siamese is product vision, not product activation.

P8.4 must not inspect product source.

P8.4 must not load product source into state.

P8.4 must not create product-bound state from product source.

Product/Siamese state remains blocked until future product-bound readiness and exact source gate.

MVP-0 local workspace state must be product-independent by default.

## Retention / Rollback / Incident Posture
| State record | Required posture |
|---|---|
| LocalWorkspace | Retention policy ref, rollback policy ref, incident policy ref. |
| WorkspaceSession | Retention, rollback, incident, local-only posture. |
| SessionManifest | Ref retention, blocker retention, incident posture where sensitive. |
| DraftWorkPacketRecord | Retention, rollback, incident posture. |
| HarnessInputDraft | Retention and copy/paste boundary; incident posture where sensitive. |
| HarnessOutputIntakeRecord | Retention, quarantine, rollback, incident posture. |
| HarnessOutputPackageRecord | Retention, review, rollback, incident posture. |
| ReviewRecord | Retention, limitations, blocker posture. |
| ReviewVerdictRecord | Retention, limitation, non-Git-approval posture. |
| IntegrationRecord | Retention, drift, rollback, incident posture. |
| IntegrationSummaryRecord | Retention and limitation posture. |
| DriftRegisterState | Retention and resolution/limitation posture. |
| AcceptedOutputRegisterState | Retention and non-commit-approval posture. |
| RejectedOutputRegisterState | Retention, rejection reason, rollback/incident posture. |
| CommitCandidateRecord | Retention, exact paths, rollback note, human approval requirement. |
| CommitCommandBlockRecord | Retention, advisory-only posture, exact paths only. |
| AuditLogRecord | Retention and no-telemetry posture. |
| LocalArtifactRef | Local-only retention posture. |
| GeneratedArtifactRef | Generated artifact and non-source posture. |
| IgnoredArtifactRef | Ignored and non-tracking-approval posture. |
| QuarantineArtifactRef | Quarantine and incident posture. |

Every state record must include retention posture.

Every state record with downstream decision impact must include rollback posture.

Every state record with sensitive, product, external, provider, live connector, generated output, or unknown-sensitivity material must include incident posture.

Accidental inclusion of secrets, credentials, product source, raw external source, raw Graphify output, or raw live connector payloads requires STOP and safe reporting.

## Human Approval Requirements
Human user must approve any future implementation of the state model.

Human user must manually run external harnesses.

Human user remains final commit authority.

Human user performs Git manually.

No state record can replace human approval.

No CommitCandidate can replace user Git decision.

## Stop Rules
STOP if P8.0 is missing.

STOP if state model attempts to create workspace directories.

STOP if state model attempts to create runtime files.

STOP if state model attempts to implement local session store.

STOP if state model attempts to implement persistence/database/event streaming/telemetry.

STOP if state model attempts to implement vector DB, graph DB, embeddings, ontology runtime, GBrain runtime memory, or automatic retrieval.

STOP if state model attempts to store secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, or credential values.

STOP if state model attempts to include product/Siamese source.

STOP if state model attempts to include raw external source.

STOP if state model attempts to include raw Graphify output.

STOP if state model attempts to track generated outputs.

STOP if state model attempts source tracking expansion.

STOP if state model treats harness output as accepted without review.

STOP if state model treats review verdict as Git approval.

STOP if state model treats CommitCandidate as Git mutation.

STOP if state model weakens user authority over Git.

STOP if git add . is recommended.

## Required P8.4 Invariants
| Invariant | Statement |
|---|---|
| STATE-001 | P8.4 is local workspace / state architecture only. |
| STATE-002 | Local workspace model is not workspace implementation. |
| STATE-003 | State model is not state persistence. |
| STATE-004 | Session state is not autonomous runtime state. |
| STATE-005 | Draft state is not accepted output. |
| STATE-006 | DraftWorkPacketRecord is not dispatch. |
| STATE-007 | HarnessInputDraft is not harness execution. |
| STATE-008 | HarnessOutputPackage state is user-pasted output, not harness execution. |
| STATE-009 | Harness output is generated evidence by default. |
| STATE-010 | Review record is not auto-review. |
| STATE-011 | Review verdict is not Git approval. |
| STATE-012 | Integration record is not automatic integration. |
| STATE-013 | CommitCandidate is not Git mutation. |
| STATE-014 | CommitCommandBlock is advisory only. |
| STATE-015 | Audit log model is not telemetry runtime. |
| STATE-016 | Local-only artifact is not publishable by default. |
| STATE-017 | Generated artifact is not source by default. |
| STATE-018 | Ignored artifact is not approval to delete or track. |
| STATE-019 | Quarantined artifact is not publishable. |
| STATE-020 | Markdown/json local file model is not database implementation. |
| STATE-021 | No persistent DB. |
| STATE-022 | No vector DB. |
| STATE-023 | No graph DB. |
| STATE-024 | No GBrain runtime memory. |
| STATE-025 | No automatic retrieval. |
| STATE-026 | No live retrieval. |
| STATE-027 | No live connector state. |
| STATE-028 | No product/Siamese source state. |
| STATE-029 | No provider auth state. |
| STATE-030 | No telemetry/event stream. |
| STATE-031 | No generated output tracking. |
| STATE-032 | No source tracking expansion. |
| STATE-033 | The user remains final commit authority. |
| STATE-034 | The agent never mutates Git. |
| STATE-035 | Never recommend git add .. |

## Future Validation Targets
Future validation targets are proposed only and were not executed:

| Target | Purpose |
|---|---|
| LocalWorkspace required fields completeness | Verify required workspace metadata. |
| WorkspaceSession required fields completeness | Verify required session metadata. |
| SessionManifest completeness | Verify manifest refs and blockers. |
| DraftWorkPacketRecord no-dispatch invariant | Verify draft work packet is not dispatch. |
| HarnessInputDraft no-execution invariant | Verify input draft does not execute harness. |
| HarnessOutputIntakeRecord user-pasted-output invariant | Verify output is user-pasted. |
| ReviewRecord no-auto-review invariant | Verify review is manual. |
| IntegrationRecord no-auto-integration invariant | Verify integration is manual. |
| CommitCandidate no-Git-mutation invariant | Verify commit candidate is advisory only. |
| CommitCommandBlock advisory-only invariant | Verify command block is advisory. |
| AuditLogRecord no-telemetry-runtime invariant | Verify audit model is not telemetry runtime. |
| Artifact classification completeness | Verify all artifact classes. |
| local-only artifact boundary check | Verify local-only remains local. |
| generated-artifact-not-source invariant | Verify generated artifact is not source. |
| ignored-artifact-not-tracking-approval invariant | Verify ignored artifact is not tracking approval. |
| quarantine artifact non-publication invariant | Verify quarantine blocks publication. |
| no-secret/no-credential state invariant | Verify secrets and credentials are never state content. |
| no-product-source state invariant | Verify product source remains blocked. |
| no-raw-external-source state invariant | Verify raw external source remains blocked. |
| no-raw-Graphify-output state invariant | Verify raw Graphify output remains blocked. |
| no-persistent-DB invariant | Verify no persistent DB. |
| no-vector-DB invariant | Verify no vector DB. |
| no-graph-DB invariant | Verify no graph DB. |
| no-GBrain-runtime-memory invariant | Verify no GBrain runtime memory. |
| no-automatic-retrieval invariant | Verify no automatic retrieval. |
| no-live-connector-state invariant | Verify no live connector state. |
| P8.2 interaction surface alignment | Future alignment check. |
| P8.3 schema alignment | Future alignment check. |
| P8.5 security gate alignment | Future alignment check. |
| P8.10 synthesis readiness check | Future readiness check. |
| never-recommend-git-add-dot invariant | Verify exact Git advisory safety. |

## Future Hardening Candidates
Future tickets are proposed only and not started:

| Candidate | Purpose |
|---|---|
| STATE-HARD-01 - LocalWorkspace Schema Alignment | Harden workspace schema. |
| STATE-HARD-02 - WorkspaceSession / SessionManifest Contract | Harden session and manifest contracts. |
| STATE-HARD-03 - HarnessOutput Intake State Safety Contract | Harden output intake safety. |
| STATE-HARD-04 - Review / Integration State Contract | Harden review and integration state. |
| STATE-HARD-05 - CommitCandidate / Git Advisory State Contract | Harden exact-path commit advisory state. |
| STATE-HARD-06 - Local Artifact Classification Contract | Harden artifact classification. |
| STATE-HARD-07 - Local-Only / Generated / Ignored Artifact Handling Contract | Harden local/generated/ignored boundaries. |
| STATE-HARD-08 - MVP-0 File-Based State Validation Checklist | Define future checklist without executing validation. |

## Created / Modified / Not Created Register
| Item | Status |
|---|---|
| Local workspace / state model document | Created. |
| LocalWorkspace model | Created. |
| WorkspaceSession model | Created. |
| SessionManifest model | Created. |
| DraftWorkPacketRecord model | Created. |
| HarnessInputDraft model | Created. |
| HarnessOutputIntakeRecord model | Created. |
| HarnessOutputPackageRecord model | Created. |
| ReviewChecklistState model | Created. |
| ReviewRecord model | Created. |
| ReviewVerdictRecord model | Created. |
| IntegrationChecklistState model | Created. |
| IntegrationRecord model | Created. |
| IntegrationSummaryRecord model | Created. |
| DriftRegisterState model | Created. |
| AcceptedOutputRegisterState model | Created. |
| RejectedOutputRegisterState model | Created. |
| CommitCandidateRecord model | Created. |
| CommitCommandBlockRecord model | Created. |
| GitAdvisoryRecord model | Created. |
| AuditLogRecord model | Created. |
| LocalArtifactRef model | Created. |
| GeneratedArtifactRef model | Created. |
| IgnoredArtifactRef model | Created. |
| QuarantineArtifactRef model | Created. |
| RetentionStateRecord model | Created. |
| RollbackStateRecord model | Created. |
| IncidentStateRecord model | Created. |
| Candidate markdown/json local-file posture | Recorded. |
| Actual workspace directories | Not created. |
| Actual session files | Not created. |
| Actual JSON state files | Not created. |
| Actual markdown state files | Not created. |
| Runtime code | Not implemented. |
| `3_platform/_governed_skeleton` | Not modified. |
| MVP package | Not created. |
| Local session store | Not implemented. |
| Persistence/database/event stream | Not created. |
| Telemetry | Not created. |
| Runtime activation | Not created. |
| Autonomous orchestration | Not created. |
| Automatic dispatch | Not created. |
| Automatic handoff | Not created. |
| Automatic reviewer assignment | Not created. |
| Automatic integration | Not created. |
| Automatic context retrieval | Not created. |
| Live retrieval | Not created. |
| Persistent memory | Not created. |
| GBrain runtime | Not created. |
| GStack runtime | Not created. |
| Hermes runtime | Not created. |
| Cadence | Not created. |
| OpenCode execution | Not created. |
| Agent execution | Not created. |
| Reviewer execution | Not created. |
| Integrator execution | Not created. |
| Tool execution | Not created. |
| Provider/auth/API/MCP activation | Not created. |
| Credential use | Not created. |
| API calls | Not created. |
| MCP activation | Not created. |
| Live connector activation | Not created. |
| Source loading | Not created. |
| Source inspection | Not created. |
| Product source inspection | Not created. |
| External source inspection | Not created. |
| External source content inspection | Not created. |
| `external/sources/gbrain-master` content inspection | Not created. |
| GStack source inspection | Not created. |
| Hermes source inspection | Not created. |
| Graphify implementation inspection | Not created. |
| Graphify rerun/adoption | Not created. |
| Codegraph execution/adoption | Not created. |
| Validation execution | Not created. |
| Tests / CI / scripts / builds | Not created. |
| Security enforcement activation | Not created. |
| Vector DB / embeddings | Not created. |
| Graph DB / substrate implementation | Not created. |
| Generated output tracking | Not created. |
| Source tracking expansion | Not created. |
| Publication | Not created. |
| Git mutation | Not created. |
| Auto-commit | Not created. |
| Auto-push | Not created. |
| `.gitignore` modified | Not created. |
| `.graphifyignore` modified | Not created. |
| Generated outputs modified/tracked | Not created. |
| Cognitive Semantic System substrate selected | Not created. |
| P8.10 started | Not created. |
| P8.11 started | Not created. |
| P8.12 or later implementation files started | Not created. |
| P8.R started | Not created. |

## Recommended Next Tickets
P8.4 is one Round 1 parallel P8 architecture ticket.

Round 1 after P8.0:

| Ticket | Name | Current posture |
|---|---|---|
| P8.1 | External Source Inventory / Classification | Missing; pending alignment. |
| P8.2 | MVP Interaction Surface Architecture | Missing; pending alignment. |
| P8.3 | Core Workflow Schema Candidates | Missing; pending alignment. |
| P8.4 | Local Workspace / State Model | Complete by this document. |
| P8.5 | Security / Activation Gate Model | Missing; pending alignment. |

After P8.1 and P8.5:

| Ticket | Name |
|---|---|
| P8.6 | Graphify Read-Only Evidence Boundary. |
| P8.7 | GBrain / GStack Memory Compatibility Boundary. |
| P8.8 | Hermes Interface / Runtime Candidate Boundary. |
| P8.9 | OpenCode Harness Upgrade Boundary. |

After P8.2-P8.9:

| Ticket | Name | Boundary |
|---|---|---|
| P8.10 | MVP-0 Architecture Synthesis | Do not start P8.10 inside P8.4. |

Recommended actual: Continue remaining Round 1 P8 architecture tickets until P8.1-P8.5 are complete.

If P8.1 and P8.5 are complete, proceed to P8.6-P8.9 in parallel.

Do not start P8.10 inside P8.4.

## Final Verdict
| Question | Answer |
|---|---|
| What did P8.4 create? | `0_architecture/governance/agent_platform_local_workspace_state_model.md`. |
| What local workspace / state model was defined? | A candidate local-only markdown/json local files state model for MVP-0 sessions, work packets, harness input/output, review, integration, commit advisory, audit, artifacts, retention, rollback, and incident posture. |
| What is LocalWorkspace? | Architecture metadata for a candidate MVP-0 local workspace; LocalWorkspace is not implementation and does not create directories. |
| What is WorkspaceSession? | Local manual session state candidate; WorkspaceSession is not autonomous runtime state, agent execution state, or persistent memory. |
| What is SessionManifest? | A metadata manifest of session refs, artifacts, decisions, blockers, limitations, and stop rules. |
| What draft work packet state is defined? | DraftWorkPacketRecord, which is not dispatch, agent execution, or harness execution. |
| What harness input state is defined? | HarnessInputDraft, which may be manually copied by the user but does not execute OpenCode or any harness. |
| What harness output intake state is defined? | HarnessOutputIntakeRecord and HarnessOutputPackageRecord for user-pasted generated evidence requiring review. |
| What review state is defined? | ReviewChecklistState, ReviewRecord, and ReviewVerdictRecord; review state is not auto-review and review verdict is not Git approval. |
| What integration state is defined? | IntegrationChecklistState, IntegrationRecord, IntegrationSummaryRecord, drift, accepted output, and rejected output registers; integration state is not automatic integration. |
| What commit candidate state is defined? | CommitCandidateRecord, CommitCommandBlockRecord, and GitAdvisoryRecord; CommitCandidate is not Git mutation and CommitCommandBlock is advisory only. |
| What audit log state is defined? | AuditLogRecord; audit log model is not telemetry runtime, event streaming, or persistence implementation. |
| What artifact classes are defined? | Local session, draft work packet, harness input, user-pasted harness output, review, integration, commit candidate, audit, generated, ignored, quarantined, raw external, raw product, secret/credential, and unknown-sensitivity artifacts. |
| What storage posture is recommended for MVP-0? | Candidate markdown/json local files, with no database, no persistent DB, no vector DB, no graph DB, no GBrain runtime memory, no automatic retrieval, and no live retrieval. |
| Does P8.4 create actual workspace directories? | No. |
| Does P8.4 create actual state files? | No. |
| Does P8.4 implement a local session store? | No. |
| Does P8.4 create a database? | No. |
| Does P8.4 implement persistent memory? | No. |
| Does P8.4 implement vector DB, embeddings, graph DB, or ontology runtime? | No. |
| Does P8.4 activate GBrain, GStack, Hermes, Cadence, Graphify, OpenCode, Codegraph, tools, providers, agents, or live connectors? | No. |
| Does P8.4 inspect product/Siamese source? | No. |
| Does P8.4 inspect external source contents? | No. |
| Does P8.4 approve generated output tracking? | No. |
| Does P8.4 approve source tracking expansion? | No. |
| Does P8.4 mutate Git? | No. |
| Can the agent recommend git add .? | No. Never recommend git add .. |
| Who remains final commit authority? | The user remains final commit authority. |
| What is the next ticket? | Continue remaining Round 1 P8 architecture tickets P8.1, P8.2, P8.3, and P8.5; do not start P8.10 inside P8.4. |

Final verdict: P8.4 is accepted as the Local Workspace / State Model for MVP-0 architecture. It defines candidate state records and boundaries only, creates no state files or directories, implements no runtime or persistence, activates nothing, and leaves Git entirely manual.
