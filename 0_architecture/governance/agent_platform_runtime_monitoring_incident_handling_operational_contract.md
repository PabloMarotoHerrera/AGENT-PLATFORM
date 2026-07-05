# Runtime Monitoring / Incident Handling Operational Contract

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | Runtime Monitoring / Incident Handling Operational Contract |
| Ticket | P6.5 |
| Status | Accepted Runtime Monitoring / Incident Handling operational contract |
| Date | 2026-07-05 |
| Scope | Metadata-only runtime monitoring and incident handling operational contract for AGENT PLATFORM / Siamese. |
| Authority | Metadata-only runtime monitoring / incident handling operational contract, not monitoring runtime, telemetry, file logging, database logging, event streaming, alerting, background workers, incident automation, containment automation, rollback automation, recovery automation, quarantine automation, deletion automation, live connector monitoring, Cadence activation, runtime activation, agent execution, task execution, handoff execution, scheduler activation, orchestration activation, autonomous loop activation, tool execution, provider/auth/API/MCP activation, validation execution, source loading, source inspection, security enforcement activation, product activation, Graphify adoption, Codegraph execution, GBrain/Hermes/Cadence activation, persistence/database/event streaming, vector DB implementation, graph DB implementation, generated output tracking, source tracking expansion, Cognitive Semantic System substrate selection, or publication. |
| Related documents | P5.R, P5.7, P5.6, P5.2, P3.2, P2.3, P3.BR, P3.0, P3.1, P3.3, P3.4, P3.5, P2.1, P2.2, P1.4, P1.3, P1.2, P1.1, P1.5, P0.1, P0.2, P0.3, S-03, S-04, CSS ADR/audit. |
| Optional sibling inputs | P6.1, P6.2, P6.3, and P6.4 are present by path-only check; P6.6 is absent. |
| Pending alignments | `pending_P6.1_agent_registry_alignment` not applied because P6.1 is present; `pending_P6.2_protocol_alignment` not applied because P6.2 is present; `pending_P6.3_context_evidence_bus_alignment` not applied because P6.3 is present; `pending_P6.4_human_approval_alignment` not applied because P6.4 is present; `pending_P6.6_substrate_decision_alignment` applied where substrate posture is referenced because P6.6 is absent. |
| Output | Runtime Monitoring / Incident Handling operational contract |

Operational planning is not activation. Monitoring model is not monitoring runtime. Incident route is not incident automation. RuntimeObservationRecord is not telemetry. MonitoringSignal is not live monitoring. IncidentRecord is not incident automation. ContainmentDecision is not automatic containment. RollbackTrigger is not automatic rollback. RecoveryDecision is not automatic recovery. This contract creates no monitoring runtime, no incident automation, no telemetry, and no Cadence.

## 2. Purpose

P6 creates operational contracts, not active operations. P6.5 defines how runtime observations, monitoring signals, incident triggers, incident records, incident routes, containment decisions, rollback triggers, recovery decisions, and monitoring boundaries are represented as metadata.

P6.5 consumes P5.7 audit/retention/rollback hooks, P5.6 agent task/handoff skeleton, P5.2 security dry-run skeleton, P3.2 security readiness, P2.3 audit/retention/rollback baseline, S-03, S-04, and P3.BR as governance inputs only.

P6.5 does not create monitoring runtime. P6.5 does not create telemetry. P6.5 does not create event streams, logs, workers, alerting, or notifications. P6.5 does not automate incident response, containment, rollback, recovery, quarantine, or deletion. P6.5 does not activate live connector monitoring. P6.5 does not activate Cadence. P6.5 does not start P6.1, P6.2, P6.3, P6.4, P6.6, or P6.7.

## 3. Current Posture

| Area | Current state | P6.5 interpretation | Blocked interpretation |
| --- | --- | --- | --- |
| AGENT PLATFORM activation level | AL-1 metadata skeleton. | Operational monitoring model may be documented as metadata. | Runtime activation. |
| P5.R skeleton audit | Present by path-only check. | Baseline evidence only. | Audit as activation. |
| P5.7 audit/retention/rollback hooks | Present by path-only check. | Metadata posture for audit/rollback/incident refs. | Persistence, rollback automation, audit sink. |
| P5.6 agent task/handoff skeleton | Present by path-only check. | Agent surfaces can be referenced as metadata. | Agent runtime monitoring or agent execution. |
| P5.2 security dry-run skeleton | Present by path-only check. | Security constraints can be referenced. | Security enforcement or enforcement telemetry. |
| P3.2 security readiness | Present by path-only check. | Security readiness constrains incident posture. | Security activation. |
| P2.3 audit/retention/rollback baseline | Present by path-only check. | Retention, rollback, and incident names align to baseline. | Automation or durable storage. |
| S-03 local-only/secrets/credentials policy | Present by path-only check. | Secret/credential surfaces route to stop rules. | Secret scanning or content retention. |
| S-04 tool/shell/network/MCP policy | Present by path-only check. | Tool, shell, network, MCP requests remain blocked. | Tool/network/MCP monitoring runtime. |
| runtime monitoring | Contract only. | MonitoringBoundary and RuntimeObservationRecord metadata. | active monitoring, monitoring daemon. |
| runtime observation | Metadata only. | RuntimeObservationRecord describes future review. | live observation stream. |
| monitoring signals | Metadata only. | MonitoringSignal describes signal classes. | active telemetry or live monitoring. |
| incidents | Metadata only. | IncidentRecord describes incident posture. | automatic incident response. |
| incident routes | Metadata only. | IncidentRoute describes human review routing. | incident daemon or routing automation. |
| containment | Metadata decision only. | ContainmentDecision records blocked action posture. | automatic containment. |
| rollback | Metadata trigger only. | RollbackTrigger records future rollback need. | automatic rollback. |
| recovery | Metadata decision only. | RecoveryDecision records future recovery posture. | automatic recovery. |
| file logs | Not created. | Logging boundary is metadata only. | file logging active. |
| database logs | Not created. | Database logging blocked. | database logging active. |
| event streams | Not created. | Event stream boundary is metadata only. | event stream active, event bus runtime. |
| telemetry | Not created. | Telemetry boundary is metadata only. | active telemetry, telemetry pipeline. |
| alerting | Not created. | Human review refs only. | alerting active. |
| background workers | Not created. | Background worker boundary blocks runtime. | background worker active. |
| live connector monitoring | Blocked. | Metadata only. | live connector monitoring active. |
| Cadence | Future inactive. | GBrain / Hermes / Cadence remain future and inactive. | Cadence active, always-on monitoring active. |
| GBrain/Hermes | Future inactive. | Metadata blocker only. | GBrain active, Hermes active. |
| product/Siamese | Product vision only. | Product-bound observations blocked. | product/Siamese source as readable by default. |
| Graphify/Codegraph | Evidence/tooling not authority. | Graphify evidence only. | Graphify Authority, Graphify truth engine, Graphify substrate, Codegraph authority. |
| Cognitive Semantic System substrate | Deferred. | `pending_P6.6_substrate_decision_alignment`. | Cognitive Semantic System substrate selected. |

AGENT PLATFORM remains AL-1 metadata skeleton. P6.5 is operational contract only. Monitoring model is not monitoring runtime. Incident route is not incident automation. No monitoring/incident surface is active by P6.5.

## 4. Inputs Reviewed

| Input group | Document | Review mode | Monitoring/incident use | Limitation |
| --- | --- | --- | --- | --- |
| P5.R audit | `agent_platform_minimal_active_agent_platform_audit.md` | governance_markdown_review | Baseline audit posture. | No activation inferred. |
| P5.7 audit/retention/rollback hooks | `agent_platform_audit_retention_rollback_runtime_hooks.md` | implementation_skeleton_review | Audit, retention, rollback, incident metadata posture. | No persistence or automation. |
| P5.6 agent task/handoff skeleton | `agent_platform_agent_task_runtime_handoff_candidate.md` | implementation_skeleton_review | Agent/task/handoff observation classes. | No agent execution or runtime monitoring. |
| P5.2 security dry-run skeleton | `agent_platform_security_policy_dry_run_candidate.md` | implementation_skeleton_review | Security dry-run constraints. | No enforcement activation. |
| P3.2 security readiness | `agent_platform_security_enforcement_readiness.md` | readiness_record_review | Security readiness boundaries. | Readiness is not activation. |
| P3.BR activation decision reconciliation | `agent_platform_activation_decision_reconciliation_closure.md` | activation_decision_review | Activation decision baseline. | No activation shortcut. |
| P2.3 audit/retention/rollback baseline | `agent_platform_audit_retention_rollback_baseline.md` | metadata_contract_review | Retention, rollback, incident vocabulary. | No automation. |
| P2.2 EvidenceRef contract | `agent_platform_cross_lane_evidence_reference_contract.md` | metadata_contract_review | Evidence refs. | Evidence supports; it does not decide. |
| P2.1 vocabulary | `agent_platform_shared_metadata_vocabulary_alignment.md` | metadata_contract_review | Naming alignment. | No runtime schema. |
| P1.4 agent boundary | `agent_platform_agent_runtime_boundary_contract_hardening.md` | metadata_contract_review | Agent boundary. | Agent metadata is not agent execution. |
| P1.3 tool boundary | `agent_platform_tool_execution_boundary_contract_hardening.md` | metadata_contract_review | Tool boundary. | Tool metadata is not tool execution. |
| P1.2 provider boundary | `agent_platform_provider_adapter_metadata_contract_hardening.md` | metadata_contract_review | Provider boundary. | Provider metadata is not provider activation. |
| P1.1 context boundary | `agent_platform_context_runtime_contract_hardening.md` | metadata_contract_review | Context boundary. | Context inclusion is not permission. |
| P1.5 Cognitive Semantic System boundary | `agent_platform_cognitive_semantic_system_prototype_hardening.md` | metadata_contract_review | Substrate boundary. | Cognitive Semantic System substrate remains deferred. |
| S-03 / S-04 policies | Security policy records. | policy_review | Secret/credential/tool/shell/network/MCP stop rules. | No enforcement or execution. |
| optional P6 siblings | P6.1-P6.4 present; P6.6 absent. | sibling_operational_contract_review | P6.1-P6.4 future alignment; P6.6 pending. | No sibling modification or activation. |

## 5. Dependency Posture

| Dependency | Required for P6.5 | Current posture | Monitoring/incident consequence | Blocker if missing |
| --- | --- | --- | --- | --- |
| P5.R minimal active agent platform audit | Yes | Present. | Baseline audit posture available. | Stop if absent. |
| P5.7 audit/retention/rollback hooks | Yes | Present. | Retention/rollback/incident refs can be modeled. | Stop if absent. |
| P5.6 agent skeleton | Yes | Present. | Agent observation classes can be metadata-only. | Stop if absent. |
| P5.2 security dry-run | Yes | Present. | Security constraints can be carried. | Stop if absent. |
| P3.2 security readiness | Yes | Present. | Security readiness constrains triggers. | Stop if absent. |
| P3.BR activation decision reconciliation | Yes | Present. | Activation blockers preserved. | Stop if absent. |
| P2.3 audit/retention/rollback baseline | Yes | Present. | Posture vocabulary available. | Stop if absent. |
| P2.2 EvidenceRef | Yes | Present. | EvidenceRef can be carried. | Stop if absent. |
| P2.1 vocabulary | Yes | Present. | Naming alignment available. | Stop if absent. |
| S-03/S-04 | Yes | Present. | Secret/credential/tool/shell/network/MCP boundaries apply. | Stop if absent. |
| P6.1 registry, if present | No | Present. | Registry/capability observations can align. | `pending_P6.1_agent_registry_alignment` if absent. |
| P6.2 protocol, if present | No | Present. | Protocol incident refs can align later. | `pending_P6.2_protocol_alignment` if absent. |
| P6.3 context/evidence bus, if present | No | Present. | Context/evidence incident refs can align later. | `pending_P6.3_context_evidence_bus_alignment` if absent. |
| P6.4 approval loop, if present | No | Present. | Human review metadata can align later. | `pending_P6.4_human_approval_alignment` if absent. |
| P6.6 substrate decision, if present | No | Absent. | `pending_P6.6_substrate_decision_alignment` where substrate posture is referenced. | Pending alignment only. |

## 6. Operational Model

Runtime monitoring is a metadata-only observation model. Monitoring signals are declared signal classes, not live signals. Incident triggers are trigger metadata, not automatic triggers. Incident records are incident metadata, not automation. Incident routes are routing metadata, not routing execution. Containment decisions are decision metadata, not containment automation. Rollback triggers are rollback metadata, not rollback execution. Recovery decisions are recovery metadata, not recovery automation. Monitoring boundaries are constraints.

| Operational component | Meaning | Current P6.5 status | Allowed use | Blocked use | Future consumer |
| --- | --- | --- | --- | --- | --- |
| RuntimeObservationRecord | Metadata record for an observation candidate. | Contract only. | Describe future review surface. | Telemetry event or live observation. | P6.7. |
| MonitoringSignal | Metadata signal descriptor. | Contract only. | Classify possible signal semantics. | Live monitoring signal. | P6.7. |
| MonitoringStatus | Monitoring status vocabulary. | Metadata only. | State monitoring posture. | Runtime state. | P6.7. |
| IncidentTrigger | Incident trigger metadata. | Contract only. | Define trigger class and route needs. | Automatic trigger/detection. | P6.7. |
| IncidentRecord | Incident metadata record. | Contract only. | Capture incident posture. | Incident automation record or persistent store entry. | P6.7. |
| IncidentSeverity | Severity vocabulary. | Metadata only. | Classify manual review priority. | Alerting severity pipeline. | P6.7. |
| IncidentRoute | Human route metadata. | Contract only. | Define reviewer/escalation refs. | Routing execution or notification. | P6.4/P6.7. |
| ContainmentDecision | Containment decision metadata. | Contract only. | State allowed metadata action. | Automatic containment. | P6.7. |
| RollbackTrigger | Rollback trigger metadata. | Contract only. | State rollback need. | Automatic rollback. | P5.7/P6.7. |
| RecoveryDecision | Recovery decision metadata. | Contract only. | State recovery review. | Automatic recovery. | P6.7. |
| MonitoringBoundary | Monitoring boundary metadata. | Required. | Preserve blockers and limits. | Monitoring runtime. | P6.7. |

## 7. Object Model

These objects are metadata only. They are not telemetry events, log records, event stream messages, queue messages, monitoring jobs, incident automation records, rollback automation records, persistence records, or approvals.

| Object | Meaning | Required fields | Forbidden fields | Allowed use | Blocked interpretation |
| --- | --- | --- | --- | --- | --- |
| `RuntimeObservationRecord` | Metadata-only observation record. | `observation_id`, `observation_label`, `observation_scope`, `observed_surface_ref`, `observation_source`, `monitoring_status`, `signal_refs`, `evidence_refs`, `validation_refs`, `security_refs`, `retention_refs`, `rollback_refs`, `incident_refs`, `sensitivity`, `source_classification`, `blockers`, `limitations`, `review_required`. | Timestamps from live telemetry, file paths to logs, database ids, event stream offsets. | Describe observation candidate. | RuntimeObservationRecord is telemetry. |
| `MonitoringSignal` | Metadata-only signal descriptor. | `signal_id`, `signal_label`, `signal_type`, `signal_scope`, `source_surface_ref`, `expected_semantics`, `blocked_runtime_use`, `security_refs`, `validation_refs`, `retention_posture`, `incident_route_refs`, `blockers`, `limitations`, `review_required`. | Metrics endpoint, polling interval, watcher config. | Classify future signal semantics. | MonitoringSignal is live monitoring. |
| `MonitoringStatus` | Monitoring status vocabulary. | status value and meaning. | Activation flags. | State metadata posture. | Active monitoring. |
| `IncidentTrigger` | Incident trigger metadata. | `trigger_id`, `trigger_label`, `trigger_scope`, `trigger_condition_metadata`, `affected_surfaces`, `required_evidence_refs`, `required_security_refs`, `required_human_review`, `blocked_automation`, `incident_route_refs`, `blockers`, `limitations`. | Watcher predicate, script, alert rule, webhook. | Define manual trigger class. | Automatic trigger. |
| `IncidentRecord` | Incident metadata record. | `incident_id`, `incident_label`, `incident_type`, `incident_severity`, `affected_surfaces`, `evidence_refs`, `validation_refs`, `security_refs`, `containment_decision_refs`, `rollback_trigger_refs`, `recovery_decision_refs`, `retention_refs`, `incident_route_refs`, `publication_blockers`, `source_tracking_blockers`, `blockers`, `limitations`, `review_required`. | Persistent incident store id, log file, ticket creation hook. | Record incident posture. | IncidentRecord is incident automation. |
| `IncidentSeverity` | Incident severity vocabulary. | severity value and meaning. | Alert priority implementation. | Manual review priority. | Alerting automation. |
| `IncidentRoute` | Incident route metadata. | `route_id`, `route_label`, `route_scope`, `reviewer_refs`, `escalation_refs`, `required_human_approval`, `allowed_metadata_action`, `blocked_automation`, `retention_posture`, `limitations`. | Notification endpoint, webhook, queue. | Human review route description. | Incident route is incident automation. |
| `ContainmentDecision` | Containment decision metadata. | `decision_id`, `target_incident_ref`, `containment_scope`, `decision_status`, `allowed_metadata_action`, `blocked_runtime_action`, `required_approval_refs`, `required_evidence_refs`, `required_security_refs`, `limitations`. | Kill switch, quarantine command, firewall rule. | Manual decision posture. | ContainmentDecision is automatic containment. |
| `RollbackTrigger` | Rollback trigger metadata. | `rollback_trigger_id`, `target_surface_ref`, `trigger_scope`, `trigger_condition_metadata`, `rollback_plan_refs`, `blocked_automation`, `required_human_approval`, `limitations`. | Rollback command, Git mutation, deployment hook. | Describe rollback need. | RollbackTrigger is automatic rollback. |
| `RecoveryDecision` | Recovery decision metadata. | `recovery_decision_id`, `target_incident_ref`, `recovery_scope`, `decision_status`, `allowed_metadata_action`, `blocked_runtime_action`, `required_approval_refs`, `required_evidence_refs`, `required_security_refs`, `limitations`. | Restart command, requeue hook, recovery script. | Manual recovery posture. | RecoveryDecision is automatic recovery. |
| `MonitoringBoundary` | Monitoring boundary metadata. | `boundary_id`, `monitored_surface_ref`, `allowed_metadata_use`, `blocked_runtime_use`, `telemetry_limits`, `logging_limits`, `persistence_limits`, `cadence_limits`, `live_connector_limits`, `product_limits`, `source_limits`, `blockers`, `limitations`. | Monitoring daemon config, database sink, event stream config. | Preserve monitoring constraints. | Runtime monitoring. |

## 8. Status / Severity Vocabulary

No status value activates monitoring, incident response, containment, rollback, recovery, persistence, telemetry, or alerting.

| Vocabulary | Status/severity value | Meaning | Allowed use | Blocked interpretation |
| --- | --- | --- | --- | --- |
| `MonitoringStatus` | `metadata_only` | Metadata record only. | Default safe posture. | Monitoring runtime. |
| `MonitoringStatus` | `inactive` | Not active. | Non-monitoring posture. | active monitoring. |
| `MonitoringStatus` | `not_monitoring` | Explicitly no monitoring. | Boundary clarity. | Hidden telemetry. |
| `MonitoringStatus` | `blocked` | Blocked by gate. | Preserve blockers. | Runtime bypass. |
| `MonitoringStatus` | `deferred` | Future review. | Planning posture. | Activation. |
| `MonitoringStatus` | `candidate_for_future_review` | Review candidate. | Future ticket input. | Approval. |
| `MonitoringStatus` | `requires_human_review` | Human review required. | Stop condition. | Approval granted. |
| `MonitoringStatus` | `requires_security_review` | Security review required. | Stop condition. | Security approved. |
| `MonitoringStatus` | `requires_incident_route` | Incident route required. | Stop condition. | Incident automation. |
| `MonitoringStatus` | `rejected_for_scope` | Out of scope. | Block. | Future reuse without review. |
| `MonitoringStatus` | `unknown` | Unknown posture. | Needs review. | Safe by default. |
| `IncidentSeverity` | `info` | Informational. | Manual review priority. | Alert emission. |
| `IncidentSeverity` | `low` | Low impact. | Manual review priority. | Alert emission. |
| `IncidentSeverity` | `medium` | Moderate impact. | Manual review priority. | Alert emission. |
| `IncidentSeverity` | `high` | High impact. | Manual review priority. | Alert emission. |
| `IncidentSeverity` | `critical` | Critical risk. | Manual review priority. | Automatic incident response. |
| `IncidentSeverity` | `unknown` | Unknown impact. | Needs review. | Safe by default. |
| `IncidentLifecycleStatus` | `metadata_only` | Metadata record only. | Default. | Active incident workflow. |
| `IncidentLifecycleStatus` | `not_active` | No active incident. | Boundary clarity. | Hidden incident daemon. |
| `IncidentLifecycleStatus` | `needs_review` | Review needed. | Stop condition. | Automatic route. |
| `IncidentLifecycleStatus` | `blocked` | Blocked. | Preserve blocker. | Automation bypass. |
| `IncidentLifecycleStatus` | `deferred` | Future review. | Planning posture. | Activation. |
| `IncidentLifecycleStatus` | `contained_by_metadata` | Metadata notes containment posture only. | Documentation. | Containment execution. |
| `IncidentLifecycleStatus` | `rejected_for_scope` | Out of scope. | Block. | Future reuse without review. |
| `IncidentLifecycleStatus` | `closed_metadata_only` | Closed as documentation only. | Governance closure. | Automated closure. |
| `IncidentLifecycleStatus` | `unknown` | Unknown. | Needs review. | Safe by default. |
| `ContainmentDecisionStatus` | `metadata_only` | Metadata only. | Default. | Automatic containment. |
| `ContainmentDecisionStatus` | `not_executed` | Not executed. | Required posture. | Execution. |
| `ContainmentDecisionStatus` | `blocked` | Blocked. | Preserve blockers. | Workaround. |
| `ContainmentDecisionStatus` | `deferred` | Future review. | Planning posture. | Approval. |
| `ContainmentDecisionStatus` | `requires_human_approval` | Human approval needed. | Stop condition. | Approval granted. |
| `ContainmentDecisionStatus` | `requires_security_review` | Security review needed. | Stop condition. | Security approved. |
| `ContainmentDecisionStatus` | `rejected_for_scope` | Out of scope. | Block. | Reuse without review. |
| `ContainmentDecisionStatus` | `unknown` | Unknown. | Needs review. | Safe by default. |
| `RecoveryDecisionStatus` | `metadata_only` | Metadata only. | Default. | Automatic recovery. |
| `RecoveryDecisionStatus` | `not_executed` | Not executed. | Required posture. | Recovery execution. |
| `RecoveryDecisionStatus` | `blocked` | Blocked. | Preserve blockers. | Workaround. |
| `RecoveryDecisionStatus` | `deferred` | Future review. | Planning posture. | Approval. |
| `RecoveryDecisionStatus` | `requires_human_approval` | Human approval needed. | Stop condition. | Approval granted. |
| `RecoveryDecisionStatus` | `requires_security_review` | Security review needed. | Stop condition. | Security approved. |
| `RecoveryDecisionStatus` | `rejected_for_scope` | Out of scope. | Block. | Reuse without review. |
| `RecoveryDecisionStatus` | `unknown` | Unknown. | Needs review. | Safe by default. |

## 9. Monitoring Surface Classification Matrix

| Monitoring surface | Monitoring status | Allowed metadata use | Blocked runtime use | Required dependencies | Required gates | Blockers | Future consumer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| validation runner skeleton observations | metadata-only candidate | Reference P5.1 posture. | Validation execution telemetry. | P5.1, P3.1. | Future validation review. | validation_execution_blocker. | P6.7. |
| security dry-run skeleton observations | metadata-only | Reference P5.2/P3.2 posture. | Enforcement telemetry. | P5.2, P3.2, S-03/S-04. | Security review. | security_enforcement_blocker. | P6.7. |
| context assembly skeleton observations | metadata-only candidate | Reference context metadata. | Source loading. | P5.3, P3.0, P1.1. | Context review. | source_loading_blocker. | P6.3/P6.7. |
| tool sandbox skeleton observations | metadata-only candidate | Reference P5.4 deny posture. | Tool execution monitoring. | P5.4, P3.3. | Tool gate future. | tool_execution_blocker. | P6.7. |
| provider adapter skeleton observations | metadata-only candidate | Reference P5.5 provider posture. | Provider/API/MCP telemetry. | P5.5, P3.4. | Provider gate future. | provider_auth_blocker. | P6.7. |
| agent task/handoff skeleton observations | metadata-only | Reference P5.6 envelopes. | Agent runtime monitoring. | P5.6, P3.5. | Agent gate future. | agent_execution_blocker. | P6.7. |
| audit/retention/rollback hook observations | metadata-only | Reference P5.7 refs. | Persistence or automation. | P5.7, P2.3. | Audit review. | persistence_blocker. | P6.7. |
| registry/capability observations, if P6.1 present | metadata-only | Reference P6.1 records. | Registry runtime monitoring. | P6.1 present. | P6.7 review. | registry_runtime_blocker. | P6.7. |
| agent-to-agent protocol observations, if P6.2 present | metadata-only | Reference protocol docs. | Message dispatch monitoring. | P6.2 present. | P6.7 review. | dispatch_blocker. | P6.7. |
| context/evidence bus observations, if P6.3 present | metadata-only | Reference bus contract. | Bus runtime or persistence. | P6.3 present. | P6.7 review. | event_bus_blocker. | P6.7. |
| human approval observations, if P6.4 present | metadata-only | Reference human review metadata. | Approval automation. | P6.4 present. | Human approval. | approval_ref_not_approval. | P6.7. |
| substrate decision observations, if P6.6 present | pending alignment | `pending_P6.6_substrate_decision_alignment`. | Substrate selection. | P6.6 absent. | P6.6 if needed. | substrate_selection_blocker. | P6.6/P6.7. |
| runtime state observations | blocked | Blocker metadata only. | Runtime telemetry. | Future activation review. | Runtime gate. | runtime_activation_blocker. | P6.7. |
| tool execution observations | blocked | Blocker metadata only. | Tool execution telemetry. | P3.3/P5.4 future. | GT-07 future. | tool_execution_blocker. | P6.7. |
| provider/API/MCP observations | blocked | Blocker metadata only. | Provider/API/MCP telemetry. | P3.4/P5.5 future. | GT-08 future. | provider_auth_blocker. | P6.7. |
| live connector observations | blocked | Blocker metadata only. | Live connector monitoring. | Future exact connector review. | GT-08/GT-15 future. | live_connector_blocker. | P6.7. |
| product/Siamese observations | blocked until product readiness and exact gates | Product boundary metadata. | Product source monitoring. | P4/GT-09 future. | Product readiness. | product_blocker. | P4/P6.7. |
| Graphify/Codegraph observations | blocked for execution/adoption | Graphify evidence remains evidence only. | Graphify/Codegraph execution or authority. | Curated evidence only. | GT-11 future. | graphify_codegraph_blocker. | P6.7. |
| GBrain/Hermes/Cadence observations | blocked / future inactive | External/cadence metadata only. | Cadence or always-on monitoring. | Future EXT review. | EXT/future cadence gate. | cadence_activation_blocker. | Future EXT. |
| source loading observations | blocked | SourceClassificationRef only. | Source inspection telemetry. | P3.0. | GT-01/GT-05 future. | source_loading_blocker. | P6.7. |
| generated output tracking observations | blocked | Metadata blocker only. | Generated output tracking. | P2.3/P5.7 future. | GT-12/GT-15 future. | generated_output_blocker. | P6.7. |
| source tracking/publication observations | blocked | Metadata blocker only. | Source tracking expansion or publication. | Future exact review. | GT-12 future. | publication_blocker. | P6.7. |
| secret/credential observations | incident route only; no content retention | Secret/credential risk classification only. | Secret scanning, value capture, retention. | S-03. | Human/security review. | secret_credential_blocker. | P6.7. |

## 10. Incident Trigger Classification Matrix

Incident triggers are metadata trigger definitions only. P6.5 does not detect, poll, alert, escalate, contain, rollback, recover, quarantine, delete, or route automatically.

| Incident trigger class | Trigger source | Default severity | Allowed metadata handling | Blocked automation | Required route | Retention posture | Rollback need |
| --- | --- | --- | --- | --- | --- | --- | --- |
| secret/credential exposure risk | S-03 boundary. | critical | Record risk class only; no value. | Secret scanning, alerting. | Security human review. | No content retention. | Manual review. |
| `.env` interaction risk | S-03 boundary. | critical | Record attempted boundary class. | File read, alerting. | Security human review. | No content retention. | Manual review. |
| provider auth material interaction risk | P3.4/S-03. | critical | Record auth-material risk. | Provider config inspection. | Security human review. | No content retention. | Manual review. |
| product source interaction risk | Product/Siamese boundary. | high | Record product boundary risk. | Product source read. | Product/security review. | Metadata only. | Manual review. |
| source loading request | P3.0 boundary. | high | Record source loading risk. | Source traversal. | Governance/security review. | Metadata only. | Manual review. |
| external source content interaction | External boundary. | high | Record external source risk. | External content inspection. | Governance/security review. | Metadata only. | Manual review. |
| live connector activation request | P3.4/live connector boundary. | high | Record connector activation risk. | Connector polling/sync. | Security/platform review. | Metadata only. | Manual review. |
| tool execution request | P3.3/P5.4. | high | Record tool execution risk. | Tool execution. | Platform/security review. | Metadata only. | Manual review. |
| provider/API/MCP activation request | P3.4/P5.5. | high | Record provider/MCP risk. | API/MCP calls. | Security/platform review. | Metadata only. | Manual review. |
| agent execution request | P3.5/P5.6. | high | Record agent execution risk. | Agent execution. | Platform review. | Metadata only. | Manual review. |
| handoff execution request | P5.6. | high | Record handoff risk. | Handoff dispatch. | Platform review. | Metadata only. | Manual review. |
| scheduler/orchestration request | Runtime boundary. | critical | Record orchestration risk. | Scheduler/orchestration. | Governance review. | Metadata only. | Manual review. |
| Cadence activation request | Cadence boundary. | critical | Record cadence risk. | Cadence active, always-on behavior. | Governance/security review. | Metadata only. | Manual review. |
| GBrain/Hermes activation request | External/cadence boundary. | high | Record external/cadence risk. | GBrain/Hermes activation. | EXT/governance review. | Metadata only. | Manual review. |
| Graphify/Codegraph execution/adoption request | Graphify/Codegraph boundary. | medium | Record tooling/adoption risk. | Execution/adoption/authority. | Governance review. | Metadata only. | Manual review. |
| generated output tracking request | P2.3/P5.7. | medium | Record output tracking risk. | Tracking generated outputs. | Governance review. | Metadata only. | Manual review. |
| source tracking expansion request | Source tracking boundary. | high | Record source tracking risk. | Tracking expansion. | Governance/security review. | Metadata only. | Manual review. |
| publication request | Publication boundary. | high | Record publication risk. | Publishing. | Governance review. | Metadata only. | Manual review. |
| persistence/database/event stream request | Persistence boundary. | high | Record persistence risk. | Database/event stream creation. | Governance/security review. | Metadata only. | Manual review. |
| telemetry request | Telemetry boundary. | high | Record telemetry risk. | Telemetry pipeline. | Governance/security review. | Metadata only. | Manual review. |
| vector/graph DB implementation request | Substrate boundary. | high | Record substrate implementation risk. | Vector/graph DB creation. | P6.6/governance review. | Metadata only. | Manual review. |
| Cognitive Semantic System substrate selection request | CSS boundary. | high | Record substrate decision pressure. | Substrate selection. | P6.6 if needed. | Metadata only. | Manual review. |
| unknown sensitivity | Unknown surface. | critical | Record unknown sensitivity. | Any automation. | Security human review. | Minimal metadata only. | Manual review. |

## 11. Boundary Model

| Boundary | P6.5 rule | Blocked interpretation | Required future gate |
| --- | --- | --- | --- |
| monitoring runtime boundary | Monitoring model is not monitoring runtime. | active monitoring, monitoring daemon. | P6.7/future runtime gate. |
| telemetry boundary | RuntimeObservationRecord is not telemetry. | active telemetry, telemetry pipeline. | Human/security approval. |
| logging boundary | No file or database logs. | file logging active, database logging active. | Persistence/logging review. |
| event stream boundary | No event stream or event-store behavior. | event stream active, event bus runtime. | Event/persistence review. |
| persistence boundary | Metadata only, no durable storage. | persistent incident store. | P5.7/P6.7 future. |
| background worker boundary | No workers, polling, watchers, scheduled jobs. | background worker active. | Runtime gate. |
| alerting boundary | No alerting or notifications. | alerting active, automatic notification active. | Human approval workflow. |
| incident automation boundary | Incident route is not incident automation. | automatic incident response. | Incident automation review. |
| rollback automation boundary | RollbackTrigger is not automatic rollback. | automatic rollback. | Rollback/human approval review. |
| quarantine/deletion automation boundary | No quarantine or deletion automation. | quarantine automation, deletion automation. | Security/governance approval. |
| live connector monitoring boundary | No live connector monitoring. | live connector monitoring active. | P3.4/P6.7 future. |
| Cadence boundary | No Cadence or always-on behavior. | Cadence active, always-on monitoring active. | Future cadence review. |
| source boundary | Source classification is not source loading permission. | Source loading or inspection. | GT-01/GT-05 future. |
| security boundary | Security constrains; it does not activate. | Security enforcement. | Security activation review. |
| validation boundary | Validation evaluates; governance decides. | Validation execution. | GT-04 future. |
| tool boundary | Tool metadata is not tool execution. | Tool execution. | GT-07 future. |
| provider/API/MCP boundary | Provider metadata is not provider activation. | Provider/API/MCP calls. | GT-08/P3.4 future. |
| agent execution boundary | Agent metadata is not agent execution. | Agent/task/handoff execution. | P3.5/P6.7 future. |
| product/Siamese boundary | Siamese is product vision. | Product source readable by default. | P4/GT-09 future. |
| Graphify/Codegraph boundary | Evidence/tooling not authority. | Graphify Authority, Graphify truth engine, Graphify substrate, Codegraph authority. | GT-11/future exact review. |
| GBrain/Hermes boundary | Future inactive only. | GBrain active, Hermes active. | EXT/future exact review. |
| Cognitive Semantic System substrate boundary | Cognitive Semantic System substrate remains deferred; `pending_P6.6_substrate_decision_alignment`. | Graph/vector substrate selected. | P6.6 if needed. |

## 12. Interfaces With P5 Skeletons

| P5 skeleton | Monitoring/incident consumption | Allowed metadata observation | Blockers preserved | Blocked interpretation |
| --- | --- | --- | --- | --- |
| P5.1 validation runner skeleton | Validation observation surface. | Metadata observation of runner posture. | validation_execution_blocker. | Runtime validation monitoring. |
| P5.2 security dry-run skeleton | Security dry-run observation surface. | Metadata observation of dry-run posture. | security_enforcement_blocker. | Enforcement telemetry. |
| P5.3 context assembly skeleton | Context observation surface. | Metadata observation of context refs. | source_loading_blocker. | Source loading. |
| P5.4 tool sandbox / allowlist skeleton | Tool posture observation surface. | Metadata observation of deny-by-default posture. | tool_execution_blocker. | Calling sandbox executors. |
| P5.5 provider adapter skeleton | Provider posture observation surface. | Metadata observation of provider metadata. | provider_auth_blocker. | Provider/API/MCP calls. |
| P5.6 agent task/handoff skeleton | Agent/task/handoff observation surface. | Metadata observation of envelopes and blocked decisions. | agent_execution_blocker. | Agent runtime monitoring or execution. |
| P5.7 audit/retention/rollback hooks | Audit/retention/rollback posture surface. | Metadata observation of hooks and refs. | persistence_blocker, rollback_automation_blocker. | Persistence or automatic rollback. |
| P5.R minimal active agent platform audit | Audit baseline. | Metadata audit reference. | activation_blocker. | P5.R as runtime approval. |

P6.5 can define metadata observations over P5 skeletons. P6.5 cannot monitor skeletons at runtime. P6.5 cannot convert skeletons into runtime services.

## 13. Interfaces With P3 Decisions

| P3 decision/readiness record | P6.5 consumption | Effect on monitoring/incident model | Blocked shortcut |
| --- | --- | --- | --- |
| P3.0 source classification readiness | SourceClassificationRef constraints. | Source-loading incidents and observations remain blocked. | Source inspection. |
| P3.1 validation execution readiness | ValidationRef constraints. | Validation monitoring remains metadata-only. | Validation execution. |
| P3.2 security enforcement readiness | SecurityRef constraints. | Security incident triggers require human review. | Security enforcement activation. |
| P3.R activation readiness reconciliation | Readiness baseline. | Readiness remains non-activation. | Activation shortcut. |
| P3.3 tool execution activation decision | Tool execution baseline. | Tool execution observations blocked. | Tool execution. |
| P3.4 provider/auth/API/MCP activation decision | Provider/MCP baseline. | Provider/API/MCP observations blocked. | Provider/API/MCP activation. |
| P3.5 agent runtime activation decision | Agent runtime baseline. | Agent runtime observations blocked. | Agent execution. |
| P3.BR activation decision reconciliation | P3-B reconciliation. | Deferred decisions remain deferred. | Broad activation. |

P3 decisions constrain monitoring and incident triggers. P3 decisions do not activate monitoring or incident handling. Deferred P3 decisions remain deferred in P6.5.

## 14. Evidence / Validation / Security Interfaces

| Interface | Monitoring/incident-carried refs | Required preservation rule | Blocked interpretation |
| --- | --- | --- | --- |
| EvidenceRef | evidence_refs. | Preserve source and limitations. | Evidence deciding. |
| ValidationRef | validation_refs. | Preserve non-execution posture. | Validation execution. |
| SecurityRef | security_refs. | Preserve constraints and review need. | Security activation. |
| SourceClassificationRef | source_classification refs. | Preserve class and sensitivity blockers. | Source loading. |
| ContextRef | context refs. | Preserve context inclusion limits. | Context permission or source read. |
| ToolRef | tool refs. | Preserve P3.3/P5.4 blockers. | Tool execution. |
| ProviderRef | provider refs. | Preserve P3.4/P5.5 blockers. | Provider activation. |
| AgentRef | agent refs. | Preserve P3.5/P5.6 blockers. | Agent execution. |
| ApprovalRef | approval refs. | Preserve human approval requirement. | Approval granted. |
| RetentionRef | retention refs. | Preserve no-persistence posture. | Storage approval. |
| RollbackRef | rollback refs. | Preserve no-automation posture. | Rollback execution. |
| IncidentRef | incident refs. | Preserve route requirement. | Incident automation. |
| AuditRef | audit refs. | Preserve metadata-only audit posture. | Audit sink/logging runtime. |

Evidence supports; it does not decide. Validation evaluates; governance decides. Security constrains; it does not activate. ApprovalRef is not approval. Monitoring refs do not authorize telemetry or runtime observation. Incident refs do not automate incident response.

## 15. Retention / Rollback / Incident Posture

| Record type | Retention posture | Rollback posture | Incident route | Publication blocker | Source tracking blocker | Generated output blocker |
| --- | --- | --- | --- | --- | --- | --- |
| monitoring metadata records | Metadata-only; no durable storage. | Manual governance rollback only. | Manual review route. | publication_blocker. | source_tracking_blocker. | generated_output_blocker. |
| observation metadata records | Metadata-only; no telemetry retention. | Manual governance update only. | Manual review route. | publication_blocker. | source_tracking_blocker. | generated_output_blocker. |
| signal metadata records | Metadata-only; no live signal retention. | Manual governance update only. | Manual review route. | publication_blocker. | source_tracking_blocker. | generated_output_blocker. |
| incident metadata records | Metadata-only; no persistent incident store. | Manual governance update only. | Manual route only. | publication_blocker. | source_tracking_blocker. | generated_output_blocker. |
| route metadata records | Metadata-only; no notification log. | Manual governance update only. | Human route metadata. | publication_blocker. | source_tracking_blocker. | generated_output_blocker. |
| containment metadata decisions | Metadata-only; not executed. | Manual governance update only. | Manual security review. | publication_blocker. | source_tracking_blocker. | generated_output_blocker. |
| rollback trigger metadata | Metadata-only; not executed. | Manual rollback review only. | Manual route. | publication_blocker. | source_tracking_blocker. | generated_output_blocker. |
| recovery metadata decisions | Metadata-only; not executed. | Manual recovery review only. | Manual route. | publication_blocker. | source_tracking_blocker. | generated_output_blocker. |
| blocked trigger records | Preserve blockers. | Manual governance update only. | Escalate attempted bypass. | publication_blocker. | source_tracking_blocker. | generated_output_blocker. |
| future candidate records | Future review posture. | Manual governance update only. | Escalate premature activation. | publication_blocker. | source_tracking_blocker. | generated_output_blocker. |

P6.5 does not implement retention, rollback, incident, quarantine, deletion, logging, telemetry, persistence, or publication automation.

## 16. Human Approval Requirements

Human review metadata is not approval. ApprovalRef is not approval.

| Approval event | Required approver role | Required evidence package | Stop rule if absent |
| --- | --- | --- | --- |
| Future monitoring runtime | Human platform owner plus security reviewer. | P6.5 contract, P6.7 audit, P5.7 refs, P3/P2 blockers closure. | Stop. |
| Future telemetry | Human platform owner plus security reviewer. | Telemetry scope, sensitivity review, retention plan. | Stop. |
| Future logging | Human platform owner plus security reviewer. | Log field list, retention/rollback/incident posture. | Stop. |
| Future event streaming | Human platform owner plus governance reviewer. | Event schema, sink, retention, incident posture. | Stop. |
| Future incident automation | Human platform owner plus security reviewer. | Automation scope, failure modes, rollback and incident route. | Stop. |
| Future automatic containment | Human platform owner plus security reviewer. | Containment plan and approvals. | Stop. |
| Future automatic rollback | Human platform owner plus release/governance reviewer. | Rollback plan and evidence package. | Stop. |
| Future automatic recovery | Human platform owner plus governance reviewer. | Recovery plan and safety posture. | Stop. |
| Future quarantine/deletion automation | Security owner plus platform owner. | Data classification, retention, deletion and incident plan. | Stop. |
| Future live connector monitoring | Security owner plus platform owner. | Connector scope, auth posture, incident route. | Stop. |
| Future Cadence/always-on monitoring | Platform owner plus governance reviewer. | Cadence scope, stop rules, rollback, incident route. | Stop. |
| Future product-bound monitoring | Product owner plus platform owner. | P4/GT-09 readiness and product incident route. | Stop. |
| Future provider/API/MCP-bound monitoring | Security owner plus platform owner. | P3.4/P5.5 refs, auth posture, retention plan. | Stop. |

## 17. Stop Rules

Stop on active monitoring request. Stop on telemetry request. Stop on file logging request. Stop on database logging request. Stop on event stream request. Stop on background worker request. Stop on alerting request. Stop on notification request. Stop on polling/watcher request. Stop on incident automation request. Stop on automatic containment request. Stop on automatic rollback request. Stop on automatic recovery request. Stop on quarantine automation request. Stop on deletion automation request. Stop on live connector monitoring request. Stop on Cadence activation request. Stop on GBrain/Hermes activation request. Stop on source loading request. Stop on product source request. Stop on external source inspection request. Stop on secret/credential request. Stop on `.env` request. Stop on provider/auth/API/MCP request. Stop on tool execution request. Stop on agent execution request. Stop on task/handoff execution request. Stop on scheduler/orchestration request. Stop on Graphify/Codegraph adoption or execution request. Stop on validation execution request. Stop on security enforcement activation request. Stop on persistence/database request. Stop on vector/graph DB request. Stop on generated output tracking request. Stop on source tracking expansion request. Stop on publication request. Stop on substrate selection request. Stop on unknown sensitivity.

## 18. Parallel P6 Alignment Rules

P6.1 registry records may later identify monitoring/incident capability metadata; P6.5 must not treat that as active monitoring. P6.2 communication protocol may later carry incident refs; P6.5 must not treat that as message dispatch. P6.3 context/evidence bus may later carry evidence/incident refs; P6.5 must not treat that as bus runtime or persistence. P6.4 human approval loop may later review incidents; P6.5 must not treat ApprovalRef as approval. P6.6 substrate decision, if present, may constrain relationship representation; P6.5 must not select substrate.

If sibling documents are absent, P6.5 records pending alignment markers and remains valid as standalone monitoring/incident contract. P6.1, P6.2, P6.3, and P6.4 are present by path-only check, so their pending markers are not applied. P6.6 is absent by path-only check; `pending_P6.6_substrate_decision_alignment` is applied where substrate posture is referenced. P6.5 does not start downstream tickets.

## 19. Future Validation Targets

Future validation targets, not executed:

| Target | Status |
| --- | --- |
| RuntimeObservationRecord required field completeness. | Future only. |
| MonitoringSignal required field completeness. | Future only. |
| MonitoringStatus vocabulary conformance. | Future only. |
| IncidentTrigger required field completeness. | Future only. |
| IncidentRecord required field completeness. | Future only. |
| IncidentSeverity vocabulary conformance. | Future only. |
| IncidentRoute required field completeness. | Future only. |
| ContainmentDecision metadata-only invariant. | Future only. |
| RollbackTrigger metadata-only invariant. | Future only. |
| RecoveryDecision metadata-only invariant. | Future only. |
| MonitoringBoundary completeness. | Future only. |
| Monitoring model is not monitoring runtime invariant. | Future only. |
| Incident route is not incident automation invariant. | Future only. |
| No telemetry invariant. | Future only. |
| No file/database logs invariant. | Future only. |
| No event stream invariant. | Future only. |
| No background worker invariant. | Future only. |
| No alerting invariant. | Future only. |
| No automatic incident response invariant. | Future only. |
| No automatic rollback invariant. | Future only. |
| No quarantine/deletion automation invariant. | Future only. |
| No live connector monitoring invariant. | Future only. |
| No Cadence invariant. | Future only. |
| P5.7 audit/retention/rollback interface coverage. | Future only. |
| P5.6 agent skeleton interface coverage. | Future only. |
| P5.2 security dry-run interface coverage. | Future only. |
| P3.2 security readiness conformance. | Future only. |
| P2.3 retention/rollback/incident conformance. | Future only. |
| S-03/S-04 boundary conformance. | Future only. |
| GBrain/Hermes/Cadence inactive invariant. | Future only. |
| Graphify/Codegraph non-adoption invariant. | Future only. |
| Product/Siamese inactive invariant. | Future only. |
| Cognitive Semantic System substrate-deferred invariant. | Future only. |
| No persistence/telemetry invariant. | Future only. |

## 20. Future Hardening Candidates

Future tickets, not started:

| Candidate | Description |
| --- | --- |
| MON-HARD-01 | RuntimeObservationRecord Schema Candidate. |
| MON-HARD-02 | MonitoringSignal Taxonomy Hardening. |
| MON-HARD-03 | IncidentTrigger Classification Hardening. |
| MON-HARD-04 | IncidentRecord Schema Candidate. |
| MON-HARD-05 | IncidentSeverity Review Matrix. |
| MON-HARD-06 | IncidentRoute Human Review Matrix. |
| MON-HARD-07 | ContainmentDecision Boundary Checklist. |
| MON-HARD-08 | RollbackTrigger Boundary Checklist. |
| MON-HARD-09 | RecoveryDecision Boundary Checklist. |
| MON-HARD-10 | MonitoringBoundary No-Runtime Checklist. |
| MON-HARD-11 | No-Telemetry / No-Event-Stream Invariant Checklist. |
| MON-HARD-12 | P6.7 Monitoring / Incident Audit Input. |

## 21. Created / Not Created Register

Created:

| File |
| --- |
| `0_architecture/governance/agent_platform_runtime_monitoring_incident_handling_operational_contract.md` |

Modified:

| Scope |
| --- |
| none |

Not created / not approved:

| Item | Posture |
| --- | --- |
| runtime activation | Not created or approved. |
| monitoring runtime | Not created or approved. |
| telemetry | Not created or approved. |
| file logs | Not created. |
| database logs | Not created. |
| event streams | Not created. |
| background workers | Not created. |
| alerting | Not created. |
| notifications | Not created. |
| polling/watchers | Not created. |
| incident automation | Not created or approved. |
| automatic containment | Not created or approved. |
| automatic rollback | Not created or approved. |
| automatic recovery | Not created or approved. |
| quarantine automation | Not created or approved. |
| deletion automation | Not created or approved. |
| live connector monitoring | Not created or approved. |
| Cadence | Not activated. |
| agent execution | Not created or approved. |
| task execution | Not created or approved. |
| handoff execution | Not created or approved. |
| scheduler/orchestration/autonomous loop | Not created or approved. |
| tool execution | Not created or approved. |
| provider/auth/API/MCP activation | Not created or approved. |
| credential use | Not performed. |
| API calls | Not performed. |
| live connector activation | Not created or approved. |
| source loading | Not created or approved. |
| source inspection | Not performed. |
| product source inspection | Not performed. |
| external source inspection | Not performed. |
| GBrain/Hermes/Cadence activation | Not created or approved. |
| Graphify/Codegraph adoption or execution | Not created or approved. |
| validation execution | Not created or approved. |
| tests/CI/scripts/builds | Not run. |
| security enforcement activation | Not created or approved. |
| persistence/database/event stream | Not created or approved. |
| vector DB / embeddings | Not created or approved. |
| graph DB / substrate implementation | Not created or approved. |
| generated output tracking | Not created or approved. |
| source tracking expansion | Not created or approved. |
| publication | Not created or approved. |
| Git mutation | Not performed. |

## 22. Recommended Next Ticket

After P6.5, the recommended queue is:

| Ticket | Sequence posture |
| --- | --- |
| P6.2 - Agent-to-Agent Communication Protocol | Complete if not already completed. |
| P6.3 - Shared Context / Evidence Bus | Complete if not already completed. |
| P6.4 - Human Approval / Review Loop | Complete if not already completed. |
| P6.6 - Cognitive Semantic System Substrate Decision | Only if needed. |
| P6.7 - Operational Readiness Audit | After P6.1-P6.5 and P6.6 if created/deferred. |

Recommended actual: P6.7 - Operational Readiness Audit only if P6.1-P6.5 are complete and P6.6 is either completed or explicitly deferred.

If P6.2, P6.3, or P6.4 are not complete, recommend completing the missing operational contracts before P6.7. If P6.6 is needed but absent, recommend P6.6 before P6.7. If P6.6 is not needed, P6.7 must record explicit substrate deferral.

Do not start P6.2. Do not start P6.3. Do not start P6.4. Do not start P6.6. Do not start P6.7.

## 23. Final Verdict

| Question | Answer |
| --- | --- |
| What did P6.5 create? | The canonical Runtime Monitoring / Incident Handling operational contract. |
| What Runtime Monitoring contract was defined? | A metadata-only observation and signal model, not monitoring runtime. |
| What Incident Handling contract was defined? | Metadata-only incident trigger, record, route, containment, rollback, and recovery model, not automation. |
| What RuntimeObservationRecord was defined? | Metadata-only observation record with scope, surface refs, status, refs, sensitivity, classification, blockers, limitations, and review requirement. |
| What MonitoringSignal was defined? | Metadata-only signal descriptor with signal semantics, blocked runtime use, refs, blockers, limitations, and review requirement. |
| What MonitoringStatus vocabulary was defined? | metadata_only, inactive, not_monitoring, blocked, deferred, candidate_for_future_review, requires_human_review, requires_security_review, requires_incident_route, rejected_for_scope, unknown. |
| What IncidentTrigger was defined? | Metadata-only trigger definition with condition metadata, affected surfaces, evidence/security refs, human review, route refs, blockers, and limitations. |
| What IncidentRecord was defined? | Metadata-only incident record with severity, affected surfaces, refs, containment/rollback/recovery refs, blockers, and review requirement. |
| What IncidentSeverity vocabulary was defined? | info, low, medium, high, critical, unknown. |
| What IncidentRoute was defined? | Metadata route record with reviewer/escalation refs, human approval requirement, allowed metadata action, blocked automation, retention posture, and limitations. |
| What ContainmentDecision was defined? | Metadata decision record, not automatic containment. |
| What RollbackTrigger was defined? | Metadata trigger record, not automatic rollback. |
| What RecoveryDecision was defined? | Metadata decision record, not automatic recovery. |
| What MonitoringBoundary was defined? | Boundary metadata covering telemetry, logging, persistence, cadence, live connector, product, source, blockers, and limitations. |
| Which monitoring surfaces were classified? | P5 skeleton observations, P6 sibling observations, runtime state, tool/provider/agent/live connector/product/Graphify/Codegraph/GBrain/Hermes/Cadence/source/generated-output/source-tracking/secret surfaces. |
| Which incident trigger classes were classified? | Secret/credential, `.env`, provider auth, product source, source loading, external source, live connector, tool/provider/agent/handoff/scheduler/Cadence/GBrain/Hermes/Graphify/Codegraph/generated-output/source-tracking/publication/persistence/telemetry/vector-graph/substrate/unknown sensitivity triggers. |
| Which monitoring/incident surfaces remain metadata-only? | P5 skeleton observations, P6.1-P6.4 observations, incident routes, incident records, containment decisions, rollback triggers, and recovery decisions. |
| Which monitoring/incident surfaces remain blocked? | Runtime state, tool execution, provider/API/MCP, live connector, product/Siamese, Graphify/Codegraph execution/adoption, GBrain/Hermes/Cadence, source loading, generated output tracking, source tracking/publication, and secret/credential content retention surfaces. |
| How does P6.5 consume P5.7? | As audit/retention/rollback metadata posture only. |
| How does P6.5 consume P5.6? | As non-executing agent/task/handoff observation metadata only. |
| How does P6.5 consume P5.2? | As non-enforcing security dry-run posture only. |
| How does P6.5 consume P3.2? | As security readiness constraints only. |
| How does P6.5 consume P2.3? | As retention/rollback/incident vocabulary and posture only. |
| How are EvidenceRef / ValidationRef / SecurityRef preserved? | As metadata refs with non-decision, non-execution, non-activation semantics. |
| How are retention / rollback / incident postures preserved? | As metadata refs and required future posture; no automation. |
| What human approval requirements were defined? | Human approval is required before future monitoring runtime, telemetry, logging, event streaming, incident automation, containment, rollback, recovery, quarantine/deletion automation, live connector monitoring, Cadence/always-on monitoring, product monitoring, or provider/API/MCP monitoring. |
| What stop rules were defined? | Stop on active monitoring, telemetry, logging, event streams, workers, alerting, notification, polling/watcher, incident/containment/rollback/recovery/quarantine/deletion automation, live connector monitoring, Cadence, GBrain/Hermes, source/product/external/secret/credential, provider/API/MCP, tool/agent/task/handoff, scheduler/orchestration, Graphify/Codegraph, validation/security activation, persistence, vector/graph DB, tracking, publication, substrate, or unknown sensitivity requests. |
| Were pending P6 sibling alignments recorded? | P6.1-P6.4 pending markers are recorded as not applied because paths are present; `pending_P6.6_substrate_decision_alignment` is applied because P6.6 is absent and substrate posture is referenced. |
| Did P6.5 create monitoring runtime? | No. |
| Did P6.5 create telemetry? | No. |
| Did P6.5 create file logs, database logs, event streams, background workers, alerting, notifications, or polling? | No. |
| Did P6.5 automate incident response, containment, rollback, recovery, quarantine, or deletion? | No. |
| Did P6.5 activate live connector monitoring? | No. |
| Did P6.5 activate Cadence? | No. |
| Did P6.5 execute agents, tasks, handoffs, tools, providers, validation, or security enforcement? | No. |
| Did P6.5 load or inspect source? | No. |
| Did P6.5 inspect product source? | No. |
| Did P6.5 activate GBrain or Hermes? | No. |
| Did P6.5 adopt Graphify or Codegraph? | No. |
| Did P6.5 implement persistence, database, event stream, or telemetry? | No. |
| Did P6.5 select Cognitive Semantic System substrate? | No. |
| What is the next recommended ticket? | P6.7 only if P6.1-P6.5 are complete and P6.6 is completed or explicitly deferred; otherwise complete missing P6.2/P6.3/P6.4/P6.6 as needed. |

Stop after P6.5. Do not start P6.2, P6.3, P6.4, P6.6, or P6.7.
