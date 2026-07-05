# P6.4 - Human Approval / Review Loop Operational Contract

## Document Header
| Field | Value |
|---|---|
| Title | Human Approval / Review Loop Operational Contract |
| Ticket | P6.4 |
| Status | Accepted human approval / review loop operational contract |
| Date | 2026-07-05 |
| Scope | AGENT PLATFORM / Siamese operational metadata-only approval and review loop model. |
| Authority | Operational metadata-only approval/review contract, not runtime activation, approval workflow activation, notification runtime, UI workflow, task queue, auto-approval, reviewer automation, escalation automation, agent execution, task execution, handoff execution, scheduler/orchestration/autonomous loop, tool execution, provider/auth/API/MCP activation, credential use, API calls, live connector activation, source loading, source inspection, product source inspection, external source inspection, GBrain/Hermes/Cadence activation, Graphify evidence / Codegraph candidate adoption or execution, validation execution, security enforcement activation, persistence/database/event streaming, telemetry, vector DB, embeddings, graph DB, substrate implementation, generated output tracking, source tracking expansion, publication, Git mutation, or Cognitive Semantic System substrate selection. |
| Related documents | P6 roadmap, P5.R, P5.1, P5.2, P5.3, P5.4, P5.5, P5.6, P5.7, P3.BR, P3.3, P3.4, P3.5, P3.R, P3.0, P3.1, P3.2, P2.1, P2.2, P2.3, P2.KR, P1.1, P1.2, P1.3, P1.4, P1.5, P0.1, P0.2, P0.3, S-03, S-04, CSS ADR/audit, README, `.gitignore`, `.graphifyignore`. |
| Output | Human approval / review loop operational contract. |

P6 may define operational contracts. P6 must not activate operations. P6.4 is documentation-only and metadata-only.

## Purpose
P6 operationalizes the P5 skeleton baseline as governed metadata-only operational contracts.

P6.4 defines a Human Approval / Review Loop contract so future controlled runtime decisions can require exact-scope human review before any future explicit gate can consider a controlled action.

P6.4 makes approval explicit, scoped, evidence-bound, security-aware, validation-aware, retention-aware, rollback-aware, and incident-aware.

P6.4 prevents implicit approval from refs, validation, security dry-run, evidence, registry presence, user intent, agent requests, approval metadata, reviewer refs, evidence packages, validation results, security dry-runs, registry presence, or runtime candidate presence.

P6.4 defines ApprovalRequest, ApprovalDecision, ApprovalStatus, ReviewerRef, ReviewScope, ApprovalEvidencePackage, ApprovalBlocker, RejectionReason, ExpirationPolicy, HumanOverridePolicy, and EscalationRouteRef.

P6.4 does not activate workflow.

P6.4 does not create notifications.

P6.4 does not create approval queues.

P6.4 does not automate approval.

P6.4 does not start P6.7.

## Current Posture
| Posture | Statement |
|---|---|
| Activation level | AGENT PLATFORM remains AL-1 metadata skeleton. |
| P6 boundary | Operational planning is not activation. |
| Approval refs | ApprovalRef is not approval. |
| Approval metadata | Approval metadata is not approval. |
| Registry | Registry presence is not approval. |
| Validation | Validation passing is not approval. |
| Security | Security dry-run passing is not approval. |
| Evidence | Evidence availability is not approval. |
| User intent | User intent without exact scope is not approval. |
| Agent request | Agent request is not approval. |
| Tool request | Tool request is not approval. |
| Provider request | Provider request is not approval. |
| P5.6 | P5.6 provides agent task / handoff skeleton metadata, not execution. |
| P5.7 | P5.7 provides audit / retention / rollback hooks, not automated rollback or incident automation. |
| P3.BR | P3.BR provides activation-decision reconciliation, not activation. |
| P3.3 / P3.4 / P3.5 | P3.3 / P3.4 / P3.5 provide decisions, not execution. |
| S-03 / S-04 | S-03 and S-04 remain security policies / boundaries, not runtime enforcement. |
| Workflow | No active workflow exists. |
| Notification | No notification runtime exists. |
| Approval automation | No approval automation exists. |
| Agent execution | No agent execution exists. |
| Tool execution | No tool execution exists. |
| Provider/auth/API/MCP | No provider/auth/API/MCP activation exists. |

## Inputs Reviewed
| Input | Expected role | Present / missing | Approval-loop use | Blocking consequence if missing |
|---|---|---|---|---|
| P5.R Minimal Active Agent Platform Audit | P5 skeleton baseline audit. | Present. | Defines baseline that approval metadata must not upgrade into activation. | Block approval contract finalization until baseline is known. |
| P5.1 Validation Runner Skeleton | Validation metadata candidate. | Present. | ValidationRef support for approval records. | Mark validation posture incomplete. |
| P5.2 Security Dry-Run Skeleton | Security metadata candidate. | Present. | SecurityRef support and blocker source. | Mark security posture incomplete. |
| P5.3 Context Assembly Skeleton | Context assembly candidate. | Present. | Context refs and context inclusion boundary. | Mark context transfer review incomplete. |
| P5.4 Tool Sandbox / Allowlist Skeleton | Tool candidate boundary. | Present. | Future exact tool approval dependency. | Mark tool approval boundary incomplete. |
| P5.5 Provider Adapter Skeleton | Provider/auth/API/MCP candidate boundary. | Present. | Future exact provider approval dependency. | Mark provider approval boundary incomplete. |
| P5.6 Agent Task / Handoff Skeleton | Agent task / handoff candidate boundary. | Present. | Approval dependencies for future task and handoff candidates. | Mark task/handoff approval boundary incomplete. |
| P5.7 Audit / Retention / Rollback Hooks | Audit, retention, rollback hook candidate. | Present. | ApprovalAuditRef, ApprovalRetentionRef, ApprovalRollbackRef, and incident route posture. | Mark retention / rollback / incident posture incomplete. |
| P3.BR Activation Decision Reconciliation Closure | Activation-decision reconciliation posture. | Present. | Prevents P6.4 from upgrading decisions into execution. | Block final approval posture. |
| P3.3 Tool Execution Activation Decision | Tool decision boundary. | Present. | Human approval dependency before future exact tool execution. | Mark tool gate alignment incomplete. |
| P3.4 Provider/Auth/API/MCP Activation Decision | Provider/auth/API/MCP decision boundary. | Present. | Human approval dependency before future exact provider/auth/API/MCP scope. | Mark provider gate alignment incomplete. |
| P3.5 Agent Runtime Activation Decision | Agent runtime decision boundary. | Present. | Human approval dependency before future runtime launch, tasks, and handoffs. | Mark agent gate alignment incomplete. |
| P3.2 Security Enforcement Readiness | Security readiness posture. | Present. | Security blockers and dry-run boundaries. | Mark security readiness alignment incomplete. |
| P2.2 EvidenceRef Contract | EvidenceRef semantics. | Present. | ApprovalEvidencePackage evidence semantics. | Mark evidence package semantics incomplete. |
| P2.3 Audit / Retention / Rollback Baseline | Audit, retention, rollback, incident baseline. | Present. | Retention posture, rollback posture, incident route requirements. | Mark record lifecycle posture incomplete. |
| P2.1 Shared Metadata Vocabulary | Shared metadata names. | Present. | Preserves vocabulary for refs, gates, blockers, and statuses. | Mark vocabulary alignment incomplete. |
| P1.4 Agent Runtime Boundary Contract Hardening | Agent runtime boundary. | Present. | Agent execution and handoff stop rules. | Mark agent boundary incomplete. |
| P1.3 Tool Execution Boundary Contract Hardening | Tool execution boundary. | Present. | Tool metadata is not execution and tool approval boundaries. | Mark tool boundary incomplete. |
| P1.2 Provider Adapter Metadata Contract Hardening | Provider metadata boundary. | Present. | Provider metadata is not provider activation. | Mark provider boundary incomplete. |
| P1.1 Context Runtime Contract Hardening | Context boundary. | Present. | Context inclusion is not permission. | Mark context boundary incomplete. |
| P1.5 Cognitive Semantic System Prototype Hardening | Cognitive Semantic System boundary. | Present. | Preserves deferred substrate posture. | Mark CSS boundary incomplete. |
| P0.1 Activation Gate Enforcement Map | Gate posture. | Present. | Approval metadata can only support a future explicit gate. | Mark activation gate posture incomplete. |
| P0.2 Validation Execution Gate Design | Validation gate posture. | Present. | Validation evaluates; governance decides. | Mark validation gate posture incomplete. |
| P0.3 Security Enforcement Hardening Plan | Security hardening posture. | Present. | Security constrains; it does not activate. | Mark security hardening posture incomplete. |
| S-03 Tool / Shell / Network / MCP Execution Policy | Tool, shell, network, MCP security boundary. | Present. | Blocks tool/network/MCP approval shortcuts. | Mark execution policy posture incomplete. |
| S-04 Local-Only Secrets / Credentials Policy | Secrets and credentials boundary. | Present. | Secrets and credentials are never approval content. | Mark secrets/credentials posture incomplete. |
| CSS ADR/audit | Cognitive Semantic System naming and audit posture. | Present. | Uses accepted Cognitive Semantic System name and deferred substrate posture. | Mark CSS naming/audit posture incomplete. |
| README | Repository-level context. | Present. | Boundary posture only. | Mark repository posture incomplete. |
| `.gitignore` | Ignore boundary. | Present. | Boundary posture only; not modified. | Mark ignore boundary posture incomplete. |
| `.graphifyignore` | Graphify evidence boundary. | Present. | Boundary posture only; not modified. | Mark Graphify evidence boundary posture incomplete. |
| P6.1 Agent Registry / Capability Registry Operational Contract | Optional sibling registry alignment. | Missing. | Registry presence remains not approval. | pending_P6.1_agent_registry_alignment. |
| P6.2 Agent-to-Agent Communication Protocol | Optional sibling protocol alignment. | Missing. | Protocol is not message dispatch. | pending_P6.2_agent_to_agent_protocol_alignment. |
| P6.3 Shared Context / Evidence Bus Operational Contract | Optional sibling bus alignment. | Missing. | Bus is not persistence. | pending_P6.3_context_evidence_bus_alignment. |
| P6.5 Runtime Monitoring / Incident Handling Operational Contract | Optional sibling monitoring/incident alignment. | Missing. | Monitoring model is not monitoring runtime. | pending_P6.5_monitoring_incident_alignment. |
| P6.6 Cognitive Semantic System Substrate Decision, if created | Optional conditional substrate decision. | Missing. | Substrate remains deferred. | css_substrate_deferred_or_pending_P6.6_decision. |

## Dependency Posture
P6.4 depends on P5.6 for task / handoff skeleton boundaries.

P6.4 depends on P5.7 for audit / retention / rollback hooks.

P6.4 depends on P3.BR for activation-decision reconciliation posture.

P6.4 depends on P3.3 for tool decision boundaries.

P6.4 depends on P3.4 for provider/auth/API/MCP decision boundaries.

P6.4 depends on P3.5 for agent runtime decision boundaries.

P6.4 depends on P2.2 for EvidenceRef semantics.

P6.4 depends on P2.3 for audit / retention / rollback / incident baseline.

P6.4 depends on P3.2, S-03, and S-04 for security posture.

P6.4 must preserve P2.1 vocabulary.

P6.4 must preserve P1.1-P1.5 boundary contracts.

P6.1 is missing, so P6.4 records `pending_P6.1_agent_registry_alignment`.

P6.2 is missing, so P6.4 records `pending_P6.2_agent_to_agent_protocol_alignment`.

P6.3 is missing, so P6.4 records `pending_P6.3_context_evidence_bus_alignment`.

P6.5 is missing, so P6.4 records `pending_P6.5_monitoring_incident_alignment`.

P6.6 is missing or deferred, so P6.4 records `css_substrate_deferred_or_pending_P6.6_decision`.

## Candidate External Path Metadata
| Path | Metadata class | Posture |
|---|---|---|
| `external/sources/gbrain-master` | external_source_candidate; cadence_reference_candidate | Not adopted; not executed; not imported; not configured; not dependency-approved; not provider/auth-approved; not Cadence-active; not substrate. Path contents were not inspected. |

GBrain / Hermes / Cadence remain future and inactive.

## Operational Model
The Human Approval / Review Loop is a metadata-only operational contract for requesting, reviewing, approving, rejecting, expiring, escalating, overriding, and blocking future controlled actions.

The review loop does not dispatch messages.

The review loop does not notify reviewers.

The review loop does not assign active tasks.

The review loop does not create workflow state machines.

The review loop does not execute approved actions.

The review loop does not activate tools, providers, agents, live connectors, Cadence, product behavior, source loading, tracking, publication, or runtime.

Human approval requires exact scope, accountable reviewer, evidence package, validation posture, security posture, source classification, allowed actions, blocked actions, retention posture, rollback posture, incident route, expiration policy, and stop rules.

Approval records are metadata until acted on by a future explicit gate.

## Object Model
| Object | Meaning | Required fields | Forbidden fields | Security posture | Validation posture | Activation posture |
|---|---|---|---|---|---|---|
| ApprovalRequest | Metadata request for human review of a future controlled action. | ID, requester, requested action, exact scope, evidence refs, validation refs, security refs, reviewers, stop rules. | Runtime credentials, secrets, raw source, broad activation grants. | Must include security posture and blockers. | Must include validation posture when required. | Not approval and not execution. |
| ApprovalDecision | Metadata decision by accountable human reviewer over exact scope. | ID, request ID, status, reviewer, approved exact scope, blocked actions, conditions, refs, stop rules. | Broad approval, self-approval, credential values, source-loading permission without exact future gate. | Cannot override security blockers. | Cannot override validation blockers. | Metadata unless future explicit gate consumes it. |
| ApprovalStatus | Controlled status vocabulary for approval lifecycle metadata. | Status value and subject. | Any status implying execution in P6.4. | Blocking statuses must preserve security blockers. | Blocking statuses must preserve validation blockers. | No status activates workflow or execution. |
| ReviewerRef | Metadata reference to accountable reviewer authority. | Reviewer ID, type, role, authority scope, allowed actions, forbidden actions, limitations. | Assignment automation, notification config, approval outcome. | Must identify security access boundary. | Must identify validation authority if applicable. | Not reviewer assignment automation and not approval. |
| ReviewScope | Exact review surface and boundary. | Scope class, surfaces, allowed actions, blocked actions, limitations. | Broad or generic activation. | Must preserve sensitive boundaries. | Must preserve validation dependencies. | Scope is not activation. |
| ApprovalEvidencePackage | Evidence package metadata for approval review. | Evidence refs, source classification refs, validation refs, security refs, audit refs, limitations. | Secrets, credentials, raw product source, raw external source, raw Graphify evidence output. | Must exclude sensitive prohibited content. | May support but cannot decide. | Evidence supports; it does not decide. |
| ApprovalBlocker | Metadata blocker that prevents approval usability. | Blocker class, source, affected scope, required resolution, downstream propagation. | Silent clearance by validation, security dry-run, registry presence, or agent request. | Must travel downstream. | Must not be cleared by validation evidence alone. | Blocks future activation until resolved by exact future gate. |
| RejectionReason | Controlled reason for rejecting request. | Reason class, affected scope, evidence refs, limitations. | Runtime side effects. | Preserves security rejection reason. | Preserves validation rejection reason. | Rejection is a valid metadata output. |
| ExpirationPolicy | Metadata policy for stale or expired approval records. | TTL/deadline, trigger, post-expiration status, renewal rules. | Automatic renewal or execution. | Stale security behavior required. | Stale validation behavior required. | Expired metadata cannot be used for future activation. |
| HumanOverridePolicy | Metadata policy for exact-scope human override boundaries. | Scope, owner, allowed/forbidden overrides, required reviews, expiration, audit refs. | Secrets bypass, broad activation, runtime activation inside P6.4. | Cannot bypass secrets/credentials policy. | Cannot bypass required validation review. | Override metadata is not runtime activation. |
| EscalationRouteRef | Metadata route reference for unresolved blockers or review escalation. | Trigger, source record, target reviewer/governance/security/validation/incident/rollback route, expected metadata outcome. | Notification runtime, incident automation, escalation automation. | May route security review metadata. | May route validation review metadata. | EscalationRouteRef is metadata only. |
| ApprovalDependencyRef | Metadata link to gates, decisions, or sibling contracts. | Dependency ID, dependency type, required status, limitations. | Automatic dependency satisfaction. | Preserves security dependencies. | Preserves validation dependencies. | Dependency presence is not activation. |
| ApprovalAuditRef | Metadata link to audit records. | Audit ID, subject, retention class, limitations. | Runtime log streaming. | Preserves audit sensitivity. | Records validation audit refs if present. | Audit refs are not execution. |
| ApprovalRetentionRef | Metadata link to retention posture. | Retention ID, retention class, expiry, limitations. | Database creation or persistence implementation. | Preserves sensitive retention boundaries. | Preserves validation record retention. | Retention posture is not persistence. |
| ApprovalRollbackRef | Metadata link to rollback posture. | Rollback ID, affected surface, rollback owner, limitations. | Automated rollback execution. | Preserves security rollback needs. | Preserves validation rollback needs. | Rollback ref is not rollback automation. |
| ApprovalIncidentRef | Metadata link to incident route. | Incident route ID, trigger, owner, limitations. | Incident automation or notification runtime. | Preserves security incident route. | Preserves validation incident route if relevant. | Incident route is not incident automation. |
| ApprovalStopRule | Metadata rule requiring stop before downstream action. | Stop condition, affected scope, blocker, resolution route. | Auto-clearance or self-approval. | Stops on security blockers. | Stops on validation blockers. | Stop rule blocks future activation. |

## ApprovalRequest Contract
ApprovalRequest fields:

| Field | Requirement |
|---|---|
| approval_request_id | Stable metadata identifier. |
| request_title | Human-readable title. |
| request_owner | Accountable owner for the request. |
| requester_ref | Ref for requester identity or role metadata. |
| requested_action | Future controlled action being requested. |
| decision_surface | Decision surface affected by the request. |
| exact_scope | Exact bounded scope of the requested action. |
| activation_surface | Surface that would be activated by a future gate, if any. |
| source_classification_refs | Source classification metadata refs. |
| sensitivity | Sensitivity class; unknown sensitivity blocks approval. |
| input_surface_refs | Input surfaces implicated by the request. |
| output_surface_refs | Output surfaces implicated by the request. |
| context_refs | Context metadata refs. |
| evidence_refs | EvidenceRef-compatible refs. |
| validation_refs | Validation posture refs. |
| security_refs | Security posture refs. |
| tool_refs | Tool metadata refs, if relevant. |
| provider_refs | Provider metadata refs, if relevant. |
| agent_refs | Agent metadata refs, if relevant. |
| handoff_refs | Handoff metadata refs, if relevant. |
| product_refs | Product boundary refs, if relevant. |
| live_connector_refs | Live connector refs, if relevant. |
| gbrain_hermes_cadence_refs | Future/blocked/candidate refs only. |
| required_gates | Explicit future gates required before action. |
| required_reviewers | ReviewerRef requirements. |
| required_human_approval | Human approval requirement flag and reason. |
| allowed_actions_requested | Exact actions requested for future gate review. |
| blocked_actions_acknowledged | Actions explicitly blocked and acknowledged. |
| side_effect_profile | Declared side-effect posture. |
| credential_use_posture | Credential use posture; credential values are forbidden. |
| source_loading_posture | Source loading posture; P6.4 does not permit loading. |
| product_boundary_posture | Product boundary posture. |
| generated_output_tracking_posture | Generated output tracking posture; not approved by P6.4. |
| source_tracking_posture | Source tracking posture; not approved by P6.4. |
| retention_posture | Retention posture. |
| rollback_posture | Rollback posture where side effects may exist. |
| incident_posture | Incident route posture where sensitive surfaces may exist. |
| expiration_policy_ref | ExpirationPolicy ref. |
| escalation_route_ref | EscalationRouteRef, metadata only. |
| stop_rules | ApprovalStopRule refs. |
| blockers | ApprovalBlocker refs or inline blocker metadata. |
| limitations | Explicit limitations and exclusions. |

ApprovalRequest is a request for review, not approval.

ApprovalRequest cannot execute actions.

ApprovalRequest cannot imply user approval.

ApprovalRequest cannot authorize broad or generic activation.

## ApprovalDecision Contract
ApprovalDecision fields:

| Field | Requirement |
|---|---|
| approval_decision_id | Stable metadata identifier. |
| approval_request_id | Linked ApprovalRequest. |
| decision_status | ApprovalStatus value. |
| reviewer_ref | Accountable ReviewerRef. |
| review_scope | Exact ReviewScope. |
| decision_timestamp | Metadata timestamp. |
| approved_exact_scope | Exact scope approved for future gate review. |
| approved_actions | Exact allowed actions, if any. |
| blocked_actions | Actions blocked by the decision. |
| deferred_actions | Actions deferred for future review. |
| rejected_actions | Actions rejected. |
| conditions | Conditions that must travel downstream. |
| required_follow_up_gates | Future gates required before any action. |
| evidence_refs | EvidenceRef-compatible refs. |
| validation_refs | Validation posture refs. |
| security_refs | Security posture refs. |
| retention_refs | Retention refs. |
| rollback_refs | Rollback refs. |
| incident_refs | Incident route refs. |
| expiration_policy_ref | ExpirationPolicy ref. |
| human_override_policy_ref | HumanOverridePolicy ref, if applicable. |
| escalation_route_ref | EscalationRouteRef, metadata only. |
| audit_refs | Audit refs. |
| limitations | Explicit limits and exclusions. |
| stop_rules | Stop rules that must travel downstream. |

ApprovalDecision is metadata unless a future explicit gate consumes it.

ApprovalDecision must be exact-scope.

ApprovalDecision must not approve broad runtime activation.

ApprovalDecision must not override security blockers.

ApprovalDecision must not override validation blockers.

ApprovalDecision must not override source classification blockers.

ApprovalDecision must not override secrets / credentials blockers.

ApprovalDecision must not self-approve.

## ApprovalStatus Model
Allowed statuses:

| Status | Meaning |
|---|---|
| draft_request_metadata_only | Request metadata draft, not approval. |
| pending_human_review | Human review required, no workflow activation. |
| blocked_by_missing_exact_scope | Missing exact scope blocks review. |
| blocked_by_missing_reviewer | Missing human reviewer blocks review. |
| blocked_by_security | Security blocker present. |
| blocked_by_validation | Validation blocker present. |
| blocked_by_source_classification | Source classification blocker present. |
| blocked_by_retention_rollback_incident_gap | Retention, rollback, or incident posture missing. |
| blocked_by_tool_gate | Tool gate blocks approval usability. |
| blocked_by_provider_gate | Provider/auth/API/MCP gate blocks approval usability. |
| blocked_by_agent_gate | Agent gate blocks approval usability. |
| blocked_by_product_gate | Product gate blocks approval usability. |
| blocked_by_live_connector_gate | Live connector gate blocks approval usability. |
| blocked_by_gbrain_hermes_cadence_gate | GBrain / Hermes / Cadence gate blocks approval usability. |
| rejected_for_scope | Rejected because scope is invalid or too broad. |
| rejected_for_security | Rejected because security posture blocks. |
| rejected_for_validation | Rejected because validation posture blocks. |
| rejected_for_policy | Rejected because policy blocks. |
| deferred | Deferred for later review. |
| expired | Expired and unusable for future activation. |
| superseded | Superseded by another metadata record. |
| escalated_metadata_only | Escalated as metadata only. |
| approved_metadata_only | Approved as metadata only, not execution. |
| approved_for_future_gate_review | Approved only for future explicit gate review. |
| approved_exact_scope_metadata_only | Exact-scope metadata approval, not activation. |
| executed_out_of_scope_for_p6_4_prohibited | Prohibited status for any execution attempt under P6.4. |

No P6.4 status may imply execution.

No P6.4 status may activate workflow.

No P6.4 status may activate tools, providers, agents, live connectors, Cadence, product behavior, source loading, tracking, or publication.

## ReviewerRef Contract
ReviewerRef fields:

| Field | Requirement |
|---|---|
| reviewer_ref_id | Stable reviewer metadata identifier. |
| reviewer_type | Human reviewer type. |
| reviewer_role | Role or governance function. |
| reviewer_scope | Surfaces the reviewer can review. |
| authority_scope | Exact authority boundary. |
| required_for_surfaces | Surfaces requiring this reviewer. |
| allowed_review_actions | Review actions allowed. |
| forbidden_review_actions | Review actions forbidden. |
| conflict_of_interest_posture | Conflict posture. |
| human_required | Human review requirement. |
| delegate_allowed | Whether delegation is allowed. |
| delegation_boundary | Exact delegation boundary. |
| evidence_access_boundary | Evidence access boundary. |
| security_access_boundary | Security access boundary. |
| approval_expiration_boundary | Expiration boundary. |
| blockers | Reviewer blockers. |
| limitations | Explicit limitations. |

ReviewerRef is not reviewer assignment automation.

ReviewerRef is not notification.

ReviewerRef is not approval.

ReviewerRef must identify authority scope and limits.

AI self-approval is blocked.

## ReviewScope Contract
Review scope classes:

| Scope class | Boundary |
|---|---|
| documentation_only_review | Review documentation only. |
| metadata_contract_review | Review metadata contract only. |
| source_classification_review | Review source classification metadata only. |
| validation_readiness_review | Review validation readiness metadata. |
| security_readiness_review | Review security readiness metadata. |
| retention_rollback_incident_review | Review retention, rollback, and incident posture. |
| tool_execution_decision_review | Review future exact tool decision dependency. |
| provider_auth_api_mcp_decision_review | Review future exact provider/auth/API/MCP decision dependency. |
| agent_runtime_decision_review | Review future exact agent runtime decision dependency. |
| context_evidence_transfer_review | Review context/evidence metadata transfer. |
| handoff_metadata_review | Review handoff metadata only. |
| product_boundary_review | Review product boundary metadata only. |
| live_connector_boundary_review | Review live connector boundary metadata only. |
| gbrain_hermes_cadence_boundary_review | Review future/blocked/candidate GBrain / Hermes / Cadence boundary metadata only. |
| publication_tracking_review | Review publication or tracking boundary metadata only. |

ReviewScope must be exact.

Broad approval is blocked.

Approval by user intent without exact scope is blocked.

Approval by registry presence is blocked.

## ApprovalEvidencePackage Contract
ApprovalEvidencePackage fields:

| Field | Requirement |
|---|---|
| approval_evidence_package_id | Stable metadata identifier. |
| approval_request_id | Linked ApprovalRequest. |
| evidence_refs | EvidenceRef-compatible refs. |
| source_classification_refs | Source classification refs. |
| context_refs | Context refs. |
| validation_refs | Validation posture refs. |
| security_refs | Security posture refs. |
| audit_refs | Audit refs. |
| retention_refs | Retention refs. |
| rollback_refs | Rollback refs. |
| incident_refs | Incident route refs. |
| decision_refs | Decision refs. |
| limitations | Limitations. |
| known_gaps | Known gaps. |
| excluded_sources | Excluded sources. |
| blocked_sources | Blocked sources. |
| review_notes | Human review notes metadata. |

Evidence supports; it does not decide.

Evidence package availability is not approval.

Evidence package must not include secrets, credentials, raw product source, raw external source, raw Graphify evidence output, raw live connector payloads, or unknown-sensitivity content.

## ApprovalBlocker Model
Blocker classes:

| Blocker class | Meaning |
|---|---|
| missing_exact_scope | Exact scope is missing. |
| missing_human_reviewer | Accountable human reviewer is missing. |
| missing_evidence_package | Evidence package is missing. |
| missing_validation_posture | Validation posture is missing. |
| missing_security_posture | Security posture is missing. |
| missing_source_classification | Source classification is missing. |
| missing_retention_posture | Retention posture is missing. |
| missing_rollback_posture | Rollback posture is missing. |
| missing_incident_route | Incident route is missing. |
| secret_or_credential_risk | Secret or credential risk exists. |
| provider_auth_risk | Provider/auth risk exists. |
| tool_execution_risk | Tool execution risk exists. |
| agent_execution_risk | Agent execution risk exists. |
| product_source_risk | Product source risk exists. |
| live_connector_risk | Live connector risk exists. |
| gbrain_hermes_cadence_risk | GBrain / Hermes / Cadence risk exists. |
| graphify_codegraph_risk | Graphify evidence / Codegraph candidate risk exists. |
| generated_output_tracking_risk | Generated output tracking risk exists. |
| source_tracking_expansion_risk | Source tracking expansion risk exists. |
| publication_risk | Publication risk exists. |
| broad_approval_risk | Broad approval risk exists. |
| ai_self_approval_risk | AI self-approval risk exists. |
| unknown_sensitivity | Sensitivity is unknown. |

ApprovalBlocker must travel downstream.

ApprovalBlocker cannot be cleared by validation evidence alone.

ApprovalBlocker cannot be cleared by security dry-run alone.

ApprovalBlocker cannot be cleared by registry presence.

ApprovalBlocker cannot be cleared by agent request.

## RejectionReason Model
Rejection reasons:

| Rejection reason | Meaning |
|---|---|
| scope_too_broad | Requested scope is too broad. |
| missing_exact_scope | Exact scope is missing. |
| unsupported_activation_surface | Activation surface is unsupported. |
| unsafe_source_classification | Source classification is unsafe or incomplete. |
| security_blocker | Security blocker is present. |
| validation_blocker | Validation blocker is present. |
| retention_gap | Retention posture gap exists. |
| rollback_gap | Rollback posture gap exists. |
| incident_route_gap | Incident route gap exists. |
| human_authority_gap | Human reviewer authority gap exists. |
| credential_risk | Credential risk exists. |
| secret_risk | Secret risk exists. |
| product_boundary_risk | Product boundary risk exists. |
| provider_auth_risk | Provider/auth risk exists. |
| tool_execution_risk | Tool execution risk exists. |
| agent_execution_risk | Agent execution risk exists. |
| live_connector_risk | Live connector risk exists. |
| gbrain_hermes_cadence_risk | GBrain / Hermes / Cadence risk exists. |
| graphify_codegraph_adoption_risk | Graphify evidence / Codegraph candidate adoption risk exists. |
| publication_risk | Publication risk exists. |
| tracking_risk | Tracking risk exists. |
| unknown_sensitivity | Sensitivity is unknown. |

Rejected approval requests are valid outputs.

Deferred approval requests are valid outputs.

## ExpirationPolicy Model
ExpirationPolicy fields:

| Field | Requirement |
|---|---|
| expiration_policy_id | Stable metadata identifier. |
| applies_to | Approval records covered by the policy. |
| ttl_or_review_deadline | TTL or review deadline. |
| expiration_trigger | Trigger that expires metadata. |
| post_expiration_status | Status after expiration. |
| renewal_allowed | Whether renewal is allowed. |
| renewal_requirements | Requirements for renewal. |
| stale_evidence_behavior | Behavior for stale evidence. |
| stale_security_behavior | Behavior for stale security posture. |
| stale_validation_behavior | Behavior for stale validation posture. |
| stale_source_classification_behavior | Behavior for stale source classification. |
| incident_on_expired_use | Incident route if expired metadata is used. |

Expired approval metadata cannot be used for future activation.

Expired approval metadata must be treated as blocker until renewed.

## HumanOverridePolicy Model
HumanOverridePolicy fields:

| Field | Requirement |
|---|---|
| human_override_policy_id | Stable metadata identifier. |
| override_scope | Exact override scope. |
| override_owner | Accountable override owner. |
| override_allowed | Exact overrides allowed. |
| override_forbidden | Overrides forbidden. |
| override_requires_evidence | Evidence requirement. |
| override_requires_security_review | Security review requirement. |
| override_requires_validation_review | Validation review requirement. |
| override_requires_retention_rollback_incident_review | Retention, rollback, incident review requirement. |
| override_expiration | Override expiration. |
| override_audit_refs | Audit refs. |
| blockers | Override blockers. |
| limitations | Limitations. |

Human override cannot bypass secrets / credentials policy.

Human override cannot bypass source classification blockers without exact future gate.

Human override cannot approve broad activation.

Human override cannot activate runtime inside P6.4.

## EscalationRouteRef Contract
EscalationRouteRef fields:

| Field | Requirement |
|---|---|
| escalation_route_ref_id | Stable metadata identifier. |
| trigger | Metadata trigger for escalation route. |
| source_record | Source metadata record. |
| target_reviewer_ref | Target ReviewerRef. |
| target_governance_route | Governance route. |
| security_route | Security review route. |
| validation_route | Validation review route. |
| incident_route | Incident route. |
| rollback_route | Rollback route. |
| expected_metadata_outcome | Expected metadata-only outcome. |
| blocked_automation | Automation explicitly blocked. |
| limitations | Limitations. |

EscalationRouteRef is not escalation automation.

EscalationRouteRef is not notification runtime.

EscalationRouteRef is not incident automation.

## Boundary Model
Blocked approval shortcuts:

| Shortcut | Boundary |
|---|---|
| AI self-approval | AI self-approval is blocked. |
| Broad approval | Broad approval is blocked. |
| Implicit approval from refs | Implicit approval from refs is blocked. |
| Passing validation | Approval by passing validation is blocked. |
| Security dry-run | Approval by security dry-run is blocked. |
| Evidence | Approval by evidence is blocked. |
| Registry presence | Approval by registry presence is blocked. |
| Capability metadata | Approval by capability metadata is blocked. |
| Context inclusion | Approval by context inclusion is blocked. |
| Tool metadata | Approval by tool metadata is blocked. |
| Provider metadata | Approval by provider metadata is blocked. |
| Agent metadata | Approval by agent metadata is blocked. |
| User intent without exact scope | Approval by user intent without exact scope is blocked. User intent without exact scope is not approval. |
| Path presence | Approval by path presence is blocked. |
| Generated evidence | Approval by generated evidence is blocked. |
| Graphify evidence | Approval by Graphify evidence is blocked. |
| P5 skeleton presence | Approval by P5 skeleton presence is blocked. |
| P3 decision eligibility | Approval by P3 decision eligibility is blocked. |

## Human Approval Requirements
Mandatory requirements before any future approval may be considered usable:

| Requirement | Boundary |
|---|---|
| Exact scope | Required; missing exact scope blocks downstream activation. |
| Human reviewer | Required; missing human reviewer blocks downstream activation. |
| Reviewer authority scope | Required and exact. |
| Approval subject | Required and unambiguous. |
| Allowed actions | Required and exact. |
| Blocked actions | Required and explicit. |
| Source classification | Required. |
| Sensitivity | Required; unknown sensitivity blocks approval. |
| Input surface | Required where applicable. |
| Output surface | Required where applicable. |
| Side-effect profile | Required. |
| Tool/provider/agent/product/live-connector/Cadence posture | Required where implicated. |
| EvidenceRef package | Required. |
| ValidationRef posture | Required where validation applies. |
| SecurityRef posture | Required where security applies. |
| Retention posture | Required for every approval record. |
| Rollback posture | Required for side-effecting future action. |
| Incident route | Required for sensitive future action. |
| Expiration policy | Required. |
| Human override policy if applicable | Required when override is possible. |
| Audit refs | Required. |
| Limitations | Required. |
| Stop rules | Required. |

Missing any mandatory approval requirement blocks downstream activation.

Approval metadata does not execute approved action.

## Interfaces With P5 Skeletons
P5.1 validation runner skeleton may produce future validation metadata, but validation does not approve.

P5.2 security dry-run skeleton may produce future security metadata, but security dry-run does not approve.

P5.3 context assembly skeleton may reference approval requirements, but context inclusion is not permission.

P5.4 tool sandbox / allowlist skeleton may require ApprovalDecision metadata before future exact tool activation, but tool metadata is not tool execution.

P5.5 provider adapter skeleton may require ApprovalDecision metadata before future exact provider/auth/API/MCP activation, but provider metadata is not provider activation.

P5.6 agent task / handoff skeleton may require ApprovalDecision metadata before future task/handoff execution, but agent metadata is not agent execution.

P5.7 audit / retention / rollback hooks may bind approval records to audit/retention/rollback metadata, but hooks are not automation.

## Interfaces With P3 Decisions
P3.3 tool decision may require human approval before future exact tool execution.

P3.4 provider/auth/API/MCP decision may require human approval before future provider/auth/API/MCP scope.

P3.5 agent runtime decision may require human approval before future runtime launch, task execution, handoff execution, tool use, provider use, live connector use, product-bound action, or generated output tracking.

P3.BR may declare P5 eligibility, but P5 eligibility is not implementation and not activation.

P6.4 must not upgrade P3 decisions into execution.

## Evidence / Validation / Security Interfaces
Evidence supports; it does not decide.

Validation evaluates; governance decides.

Security constrains; it does not activate.

ApprovalEvidencePackage must use P2.2 EvidenceRef semantics.

ValidationRef may support an approval decision, but cannot grant approval by itself.

SecurityRef may constrain or block an approval decision, but cannot activate by itself.

Security blockers cannot be overridden by approval metadata unless future exact gate explicitly approves a safe route.

Secrets and credentials are never approval content.

Unknown sensitivity blocks approval.

## Source Classification Interfaces
Source classification is not source loading permission.

Path presence is not content inspection permission.

Approval requests must preserve P3.0 source classification.

Approval decisions must preserve source classification and sensitivity.

Approval decisions must not approve product source inspection without future exact product gate.

Approval decisions must not approve external source inspection without future exact review gate.

Approval decisions must not approve `external/sources/gbrain-master` inspection inside P6.4.

Approval decisions must treat secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, and credential values as never content.

## Retention / Rollback / Incident Posture
| Record or future approval surface | Required posture |
|---|---|
| Approval requests | Retention posture, rollback posture if side-effecting, incident route if sensitive. |
| Approval decisions | Retention posture, rollback posture if side-effecting, incident route if sensitive. |
| Approval evidence packages | Retention posture and excluded/blocked source posture. |
| Approval blockers | Downstream retention and propagation posture. |
| Rejections | Retention posture and decision audit refs. |
| Deferrals | Retention posture and expiration posture. |
| Expirations | Expiration status, renewal requirements, stale evidence/security/validation behavior. |
| Human overrides | Retention, rollback, incident, expiration, and audit refs. |
| Escalation routes | Metadata route retention and no-automation boundary. |
| Future tool approvals | Retention, rollback, and incident posture for side effects. |
| Future provider/auth/API/MCP approvals | Retention, rollback, incident, and secrets/credentials posture. |
| Future agent runtime approvals | Retention, rollback, incident, task, handoff, and tool/provider posture. |
| Future product-bound approvals | Retention, rollback, incident, product boundary, and sensitivity posture. |
| Future live connector approvals | Retention, rollback, incident, connector, and payload sensitivity posture. |
| Future Cadence / GBrain / Hermes approvals | Future/blocked/candidate route only with explicit future gate. |

Every approval record must include retention posture.

Every approval record must include rollback posture where action may have downstream side effects.

Every approval record must include incident route where sensitive data, credentials, product surfaces, provider surfaces, live connectors, external sources, or generated outputs are implicated.

Approval records with missing retention / rollback / incident posture must remain blocked.

Human approval cannot remove incident requirements.

## Stop Rules
STOP if exact scope is missing.

STOP if human reviewer is missing.

STOP if reviewer authority scope is missing.

STOP if approval subject is ambiguous.

STOP if evidence package is missing.

STOP if source classification is missing.

STOP if sensitivity is unknown.

STOP if validation posture is required but missing.

STOP if security posture is required but missing.

STOP if retention posture is missing.

STOP if rollback posture is missing for side-effecting future action.

STOP if incident route is missing for sensitive future action.

STOP if user intent is broad or ambiguous.

STOP if AI self-approval is attempted.

STOP if approval is inferred from refs, validation, security dry-run, evidence, registry presence, or path presence.

STOP if approval would permit source loading, product inspection, external source inspection, credential use, provider/auth/API/MCP, tool execution, agent execution, live connectors, Cadence, GBrain, Hermes, Graphify evidence / Codegraph candidate, generated output tracking, source tracking expansion, publication, persistence, telemetry, vector DB, graph DB, or substrate selection without future exact gate.

## Required P6.4 Invariants
| Invariant | Statement |
|---|---|
| APP-001 | P6.4 is an operational metadata-only contract. |
| APP-002 | Operational planning is not activation. |
| APP-003 | AGENT PLATFORM remains AL-1 metadata skeleton. |
| APP-004 | ApprovalRef is not approval. |
| APP-005 | ApprovalRequest is not approval. |
| APP-006 | ApprovalDecision is metadata unless future explicit gate consumes it. |
| APP-007 | AI self-approval is blocked. |
| APP-008 | Broad approval is blocked. |
| APP-009 | User intent without exact scope is not approval. |
| APP-010 | Approval by passing validation is blocked. |
| APP-011 | Approval by security dry-run is blocked. |
| APP-012 | Approval by evidence is blocked. |
| APP-013 | Approval by registry presence is blocked. |
| APP-014 | Approval by context inclusion is blocked. |
| APP-015 | Approval by tool metadata is blocked. |
| APP-016 | Approval by provider metadata is blocked. |
| APP-017 | Approval by agent metadata is blocked. |
| APP-018 | Evidence supports; it does not decide. |
| APP-019 | Validation evaluates; governance decides. |
| APP-020 | Security constrains; it does not activate. |
| APP-021 | Secrets and credentials are never approval content. |
| APP-022 | Source classification is not source loading permission. |
| APP-023 | Path presence is not content inspection permission. |
| APP-024 | Cognitive Semantic System substrate remains deferred unless P6.6 creates a decision record. |
| APP-025 | GBrain / Hermes / Cadence remain future and inactive. |
| APP-026 | P6.4 creates no active workflow. |
| APP-027 | P6.4 creates no notification runtime. |
| APP-028 | P6.4 creates no approval automation. |
| APP-029 | P6.4 executes no agents, tasks, handoffs, tools, providers, connectors, validation, security enforcement, runtime, or product behavior. |
| APP-030 | P6.4 does not approve generated output tracking, source tracking expansion, publication, Git mutation, or substrate implementation. |

## Future Validation Targets
Future validation targets are proposed only and were not executed:

| Target | Purpose |
|---|---|
| ApprovalRequest required fields completeness | Verify required request metadata is present. |
| ApprovalDecision required fields completeness | Verify required decision metadata is present. |
| ReviewerRef authority-scope completeness | Verify reviewer authority is exact. |
| ReviewScope exact-scope invariant | Verify no broad scope. |
| ApprovalEvidencePackage EvidenceRef conformance | Verify P2.2 EvidenceRef semantics. |
| ApprovalBlocker preservation | Verify blockers travel downstream. |
| RejectionReason completeness | Verify rejection reasons are controlled. |
| ExpirationPolicy completeness | Verify stale and expired approvals block future activation. |
| HumanOverridePolicy boundary completeness | Verify override cannot bypass policy. |
| EscalationRouteRef metadata-only invariant | Verify escalation route is not automation. |
| no-AI-self-approval invariant | Verify AI self-approval remains blocked. |
| no-broad-approval invariant | Verify broad approval remains blocked. |
| no-implicit-approval-from-refs invariant | Verify refs are not approval. |
| no-approval-by-validation invariant | Verify validation passing is not approval. |
| no-approval-by-security-dry-run invariant | Verify security dry-run is not approval. |
| no-approval-by-evidence invariant | Verify evidence availability is not approval. |
| no-approval-by-registry-presence invariant | Verify registry presence is not approval. |
| no-secret/no-credential approval-content invariant | Verify secrets and credentials are never approval content. |
| source-classification-preservation invariant | Verify source classification is preserved. |
| retention / rollback / incident completeness | Verify record lifecycle posture. |
| P3.3 tool-decision approval dependency check | Verify future exact tool execution requires approval dependency where applicable. |
| P3.4 provider-auth approval dependency check | Verify future exact provider/auth/API/MCP scope requires approval dependency where applicable. |
| P3.5 agent-runtime approval dependency check | Verify future exact agent runtime scope requires approval dependency where applicable. |
| P5.6 task/handoff approval-boundary check | Verify task and handoff metadata preserve approval boundary. |
| P5.7 audit/retention/rollback approval-binding check | Verify approval records bind to audit/retention/rollback metadata. |
| P6 sibling alignment checks | Verify P6.1, P6.2, P6.3, P6.5, and P6.6 alignment or deferral. |

## Future Hardening Candidates
Future tickets are proposed only and not started:

| Candidate | Purpose |
|---|---|
| APP-HARD-01 - ApprovalRequest Schema Alignment | Align ApprovalRequest schema with P6 sibling contracts. |
| APP-HARD-02 - ApprovalDecision Exact-Scope Contract | Harden exact-scope decision metadata. |
| APP-HARD-03 - ReviewerRef Authority Boundary Contract | Harden reviewer authority and delegation boundaries. |
| APP-HARD-04 - ApprovalEvidencePackage Contract | Harden evidence package semantics and exclusions. |
| APP-HARD-05 - Human Override / Escalation Boundary Contract | Harden override and escalation metadata boundaries. |
| APP-HARD-06 - Approval Expiration / Renewal Contract | Harden expiration and renewal semantics. |
| APP-HARD-07 - Approval-to-P5 Implementation Gate Checklist | Define future gate checklist without implementing it. |
| APP-HARD-08 - No-Self-Approval / No-Broad-Approval Validation Checklist | Define future validation checklist without executing validation. |

## Created / Not Created Register
| Item | Status |
|---|---|
| Human approval / review loop operational contract document | Created. |
| ApprovalRequest model | Created. |
| ApprovalDecision model | Created. |
| ApprovalStatus model | Created. |
| ReviewerRef model | Created. |
| ReviewScope model | Created. |
| ApprovalEvidencePackage model | Created. |
| ApprovalBlocker model | Created. |
| RejectionReason model | Created. |
| ExpirationPolicy model | Created. |
| HumanOverridePolicy model | Created. |
| EscalationRouteRef model | Created. |
| Runtime activation | Not created. |
| Agent execution | Not created. |
| Task execution | Not created. |
| Handoff execution | Not created. |
| Scheduler/orchestration/autonomous loop | Not created. |
| Approval workflow activated | Not created. |
| Notification runtime created | Not created. |
| UI workflow created | Not created. |
| Task queue created | Not created. |
| Approval queue created | Not created. |
| Approval automation created | Not created. |
| Auto-approval approved | Not created. |
| Reviewer automation created | Not created. |
| Escalation automation created | Not created. |
| Tool execution | Not created. |
| Provider/auth/API/MCP activation | Not created. |
| Credential use | Not created. |
| API calls | Not created. |
| Live connector activation | Not created. |
| Source loading | Not created. |
| Source inspection | Not created. |
| Product source inspection | Not created. |
| External source inspection | Not created. |
| GBrain/Hermes/Cadence activation | Not created. |
| Graphify evidence / Codegraph candidate adoption or execution | Not created. |
| Validation execution | Not created. |
| Security enforcement activation | Not created. |
| Persistence/database/event stream | Not created. |
| Telemetry | Not created. |
| Vector DB / embeddings | Not created. |
| Graph DB / substrate implementation | Not created. |
| Generated output tracking | Not created. |
| Source tracking expansion | Not created. |
| Publication | Not created. |
| Git mutation | Not created. |
| `.gitignore` modified | Not created. |
| `.graphifyignore` modified | Not created. |
| Generated outputs modified/tracked | Not created. |
| Cognitive Semantic System substrate selected | Not created. |
| P6.7 started | Not created. |
| P7 or later roadmap phase started | Not created. |

## Recommended Next Tickets
P6.4 is one parallel P6 operational contract.

Parallel P6 tickets:

| Ticket | Name | Current P6.4 posture |
|---|---|---|
| P6.1 | Agent Registry / Capability Registry | Missing; continue remaining parallel P6 operational contract tickets. |
| P6.2 | Agent-to-Agent Communication Protocol | Missing; continue remaining parallel P6 operational contract tickets. |
| P6.3 | Shared Context / Evidence Bus | Missing; continue remaining parallel P6 operational contract tickets. |
| P6.4 | Human Approval / Review Loop | Complete by this document. |
| P6.5 | Runtime Monitoring / Incident Handling | Missing; continue remaining parallel P6 operational contract tickets. |

Conditional:

| Ticket | Name | Current P6.4 posture |
|---|---|---|
| P6.6 | Cognitive Semantic System Substrate Decision, if needed | Missing/deferred; Cognitive Semantic System substrate remains deferred unless P6.6 creates a decision record. |

Final:

| Ticket | Name | Boundary |
|---|---|---|
| P6.7 | Operational Readiness Audit | Do not start P6.7 inside P6.4. |

Recommended actual: If P6.1, P6.2, P6.3, and P6.5 are not complete, continue the remaining parallel P6 operational contract tickets.

Recommended actual: If P6.1, P6.2, P6.3, P6.4, and P6.5 are complete and P6.6 is either created or explicitly deferred, proceed to P6.7 - Operational Readiness Audit.

Do not start P6.7 inside P6.4.

## Final Verdict
| Question | Answer |
|---|---|
| What did P6.4 create? | The Human Approval / Review Loop Operational Contract document. |
| What human approval / review loop contract was defined? | A metadata-only contract for exact-scope ApprovalRequest, ApprovalDecision, reviewer, evidence, blocker, expiration, override, escalation, stop-rule, retention, rollback, and incident posture. |
| What approval objects were defined? | ApprovalRequest, ApprovalDecision, ApprovalStatus, ReviewerRef, ReviewScope, ApprovalEvidencePackage, ApprovalBlocker, RejectionReason, ExpirationPolicy, HumanOverridePolicy, EscalationRouteRef, ApprovalDependencyRef, ApprovalAuditRef, ApprovalRetentionRef, ApprovalRollbackRef, ApprovalIncidentRef, and ApprovalStopRule. |
| What is an ApprovalRequest? | A request for human review of a future controlled action; it is not approval and cannot execute actions. |
| What is an ApprovalDecision? | Exact-scope human decision metadata that remains inactive unless a future explicit gate consumes it. |
| What is a ReviewerRef? | Metadata identifying human reviewer authority scope and limits; it is not assignment automation, notification, or approval. |
| What is a ReviewScope? | Exact metadata scope defining what is reviewed and what remains blocked. |
| What is an ApprovalEvidencePackage? | EvidenceRef-compatible metadata package supporting review; evidence supports, it does not decide. |
| What approval shortcuts are blocked? | AI self-approval, broad approval, implicit approval from refs, validation, security dry-run, evidence, registry presence, capability metadata, context inclusion, tool metadata, provider metadata, agent metadata, user intent without exact scope, path presence, generated evidence, Graphify evidence, P5 skeleton presence, and P3 decision eligibility. |
| Is ApprovalRef approval? | No. ApprovalRef is not approval. |
| Is user intent approval? | No. User intent without exact scope is not approval. |
| Is validation passing approval? | No. Validation passing is not approval. |
| Is security dry-run approval? | No. Security dry-run passing is not approval. |
| Is evidence availability approval? | No. Evidence availability is not approval. |
| Is registry presence approval? | No. Registry presence is not approval. |
| Is AI self-approval allowed? | No. AI self-approval is blocked. |
| Is broad approval allowed? | No. Broad approval is blocked. |
| Did P6.4 activate workflow? | No. P6.4 creates no active workflow. |
| Did P6.4 create notification runtime? | No. P6.4 creates no notification runtime. |
| Did P6.4 create approval automation? | No. P6.4 creates no approval automation. |
| Did P6.4 execute agents, tasks, or handoffs? | No. P6.4 executes no agents, tasks, or handoffs. |
| Did P6.4 execute tools? | No. P6.4 executes no tools. |
| Did P6.4 configure provider/auth/API/MCP? | No. P6.4 configures no provider/auth/API/MCP. |
| Did P6.4 use credentials? | No. P6.4 uses no credentials. |
| Did P6.4 activate live connectors? | No. P6.4 activates no live connectors. |
| Did P6.4 activate GBrain, Hermes, or Cadence? | No. GBrain / Hermes / Cadence remain future and inactive. |
| Did P6.4 load or inspect source? | No. P6.4 did not load or inspect source. |
| Did P6.4 inspect product source? | No. P6.4 did not inspect product source. |
| Did P6.4 run validation or tests? | No. P6.4 did not run validation or tests. |
| Did P6.4 activate security enforcement? | No. P6.4 did not activate security enforcement. |
| Did P6.4 create persistence, database, event stream, or telemetry? | No. P6.4 created no persistence, database, event stream, or telemetry. |
| Did P6.4 implement vector DB, embeddings, graph DB, or substrate? | No. P6.4 implemented no vector DB, embeddings, graph DB, or substrate. |
| Did P6.4 approve generated output tracking or source tracking expansion? | No. P6.4 did not approve generated output tracking or source tracking expansion. |
| Was Cognitive Semantic System substrate selected? | No. Cognitive Semantic System substrate remains deferred unless P6.6 creates a decision record. |
| What is the next ticket? | Continue missing parallel P6 operational contracts P6.1, P6.2, P6.3, and P6.5; P6.6 remains conditional; do not start P6.7 inside P6.4. |

Final verdict: P6.4 is accepted as an operational metadata-only human approval / review loop contract. It creates no runtime behavior and activates nothing.
