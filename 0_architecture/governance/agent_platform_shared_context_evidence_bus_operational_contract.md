# Shared Context / Evidence Bus Operational Contract

## Document Header

| Field | Value |
| --- | --- |
| Title | Shared Context / Evidence Bus Operational Contract |
| Ticket | P6.3 |
| Status | Accepted shared context / evidence bus operational contract |
| Date | 2026-07-05 |
| Scope | Define the metadata-only Shared Context / Evidence Bus operational contract for AGENT PLATFORM / Siamese. |
| Authority | Shared Context / Evidence Bus operational contract only, not bus runtime implementation, persistence, database storage, event store, event streaming, telemetry, queue/broker/websocket activation, message dispatch, context materialization from raw source, source loading, source inspection, product source inspection, external source inspection, GBrain/Hermes source inspection, Graphify raw output inspection, provider/auth/API/MCP activation, credential use, API calls, MCP calls, tool execution, agent execution, task execution, handoff execution, scheduler/orchestration activation, live connector activation, GBrain implementation/adoption/execution, Hermes activation, Cadence activation, validation execution, security enforcement activation, vector DB implementation, embeddings generation, graph DB implementation, Graphify adoption, Codegraph execution, generated output tracking approval, source tracking approval, publication approval, Git mutation approval, or Cognitive Semantic System substrate selection. |
| Related documents | P5.R Minimal Active Agent Platform Audit; P5.1 Validation Runner Skeleton; P5.2 Security Dry-Run Skeleton; P5.3 Context Assembly Skeleton; P5.4 Tool Sandbox / Allowlist Skeleton; P5.5 Provider Adapter Skeleton; P5.6 Agent Task / Handoff Skeleton; P5.7 Audit / Retention / Rollback Hooks; P3.BR Activation Decision Reconciliation Closure; P3.3 Tool Execution Activation Decision; P3.4 Provider/Auth/API/MCP Activation Decision; P3.5 Agent Runtime Activation Decision; P3.R Activation Readiness Reconciliation Closure; P3.0 Controlled Source Classification Readiness; P3.1 Validation Execution Readiness; P3.2 Security Enforcement Readiness; P2.KR Knowledge / Retrieval Architecture Reconciliation Closure; P2.R Cross-Lane Integration Reconciliation Closure; P2.1 Shared Metadata Vocabulary Alignment; P2.2 Cross-Lane Evidence Reference Contract; P2.3 Audit / Retention / Rollback Baseline; P1.1 Context Runtime Contract Hardening; P1.2 Provider Adapter Metadata Contract Hardening; P1.3 Tool Execution Boundary Contract Hardening; P1.4 Agent Runtime Boundary Contract Hardening; P1.5 Cognitive Semantic System Prototype Hardening; P0.1 Activation Gate Enforcement Map; P0.2 Validation Execution Gate Design; P0.3 Security Enforcement Hardening Plan; Activation Gate Charter; Tool / Shell / Network / MCP Execution Policy; Local-Only / Secrets / Credentials Policy; Cognitive Semantic System ADR / audit; README.md; .gitignore; .graphifyignore; Optional P6.1 if present; Optional P6.2 if present; Optional P6.4 if present; Optional P6.5 if present; Optional P6.6 if present. |
| Output | shared context / evidence bus operational contract |

## Purpose

P6 defines operational contracts without activating operations.

P6.3 defines how shared context and evidence would be referenced across future AGENT PLATFORM components. It turns the P5.3 Context Assembly Skeleton and P5.7 Audit / Retention / Rollback Hooks into a higher-level operational contract for metadata references only.

P6.3 defines metadata envelopes for context/evidence references, source refs, validation refs, security refs, retention refs, rollback refs, incident refs, and publication decisions.

P6.3 does not create bus runtime. P6.3 does not create persistence. P6.3 does not create event streaming. P6.3 does not materialize context from raw source. P6.3 does not dispatch messages. P6.3 does not activate agents, tools, providers, live connectors, GBrain, Hermes, or Cadence. P6.3 does not select Cognitive Semantic System substrate. P6.3 does not start P6.7.

## Current Posture

AGENT PLATFORM remains AL-1 metadata skeleton.

Operational planning is not activation.

Registry is not runtime.

Protocol is not message dispatch.

Bus is not persistence.

ApprovalRef is not approval.

Monitoring model is not monitoring runtime.

Incident route is not incident automation.

Capability metadata is not capability execution.

Agent metadata is not agent execution.

Tool metadata is not tool execution.

Provider metadata is not provider activation.

Context inclusion is not permission.

Evidence supports; it does not decide.

Validation evaluates; governance decides.

Security constrains; it does not activate.

Cognitive Semantic System substrate remains deferred unless P6.6 creates a decision record.

Siamese is product vision, not product activation.

GBrain / Hermes / Cadence remain future and inactive.

No active runtime, active agents, task execution, handoff execution, tool execution, provider calls, live connectors, product integration, Cadence, GBrain/Hermes activation, Graphify/Codegraph adoption, CSS substrate implementation, persistence, telemetry, vector DB, graph DB, generated output tracking, source tracking expansion, publication, or Git mutation is approved by P6.3.

## Inputs Reviewed

| input | status | role in P6.3 | limitations |
| --- | --- | --- | --- |
| `0_architecture/governance/agent_platform_minimal_active_agent_platform_audit.md` | Present / reviewed | P5.R baseline and AL-1 skeleton audit. | Audit is not activation. |
| `0_architecture/implementation/agent_platform_validation_runner_minimal_implementation.md` | Present / reviewed | P5.1 validation skeleton posture. | No validation execution. |
| `0_architecture/implementation/agent_platform_security_policy_dry_run_candidate.md` | Present / reviewed | P5.2 security dry-run skeleton posture. | No security enforcement activation. |
| `0_architecture/implementation/agent_platform_context_assembly_runtime_candidate.md` | Present / reviewed | P5.3 context assembly skeleton and ContextPackRef source. | No source loading or context materialization. |
| `0_architecture/implementation/agent_platform_tool_execution_sandbox_allowlist_candidate.md` | Present / reviewed | P5.4 tool blocker and tool metadata posture. | No tool execution. |
| `0_architecture/implementation/agent_platform_provider_adapter_runtime_candidate.md` | Present / reviewed | P5.5 provider metadata posture. | No provider/auth/API/MCP activation. |
| `0_architecture/implementation/agent_platform_agent_task_runtime_handoff_candidate.md` | Present / reviewed | P5.6 agent task/handoff envelope posture. | No agent, task, or handoff execution. |
| `0_architecture/implementation/agent_platform_audit_retention_rollback_runtime_hooks.md` | Present / reviewed | P5.7 audit, retention, rollback, incident, and blocker hook shapes. | No persistence, active logging, rollback automation, or incident automation. |
| `0_architecture/governance/agent_platform_activation_decision_reconciliation_closure.md` | Present / reviewed | P3.BR reconciled activation decision posture. | Decision is not execution. |
| `0_architecture/governance/agent_platform_tool_execution_activation_decision.md` | Present / reviewed | P3.3 tool activation decision. | Tool execution remains deferred/blocked. |
| `0_architecture/governance/agent_platform_provider_auth_api_mcp_activation_decision.md` | Present / reviewed | P3.4 provider/auth/API/MCP decision. | Provider/auth/API/MCP activation remains deferred/blocked. |
| `0_architecture/governance/agent_platform_agent_runtime_activation_decision.md` | Present / reviewed | P3.5 agent runtime decision. | Agent runtime activation remains deferred/blocked. |
| `0_architecture/governance/agent_platform_activation_readiness_reconciliation_closure.md` | Present / reviewed | P3.R activation readiness closure. | Readiness is not activation. |
| `0_architecture/governance/agent_platform_controlled_source_classification_readiness.md` | Present / reviewed | P3.0 source classification posture. | Classification is not source loading permission. |
| `0_architecture/governance/agent_platform_validation_execution_readiness.md` | Present / reviewed | P3.1 validation readiness posture. | No validation run. |
| `0_architecture/governance/agent_platform_security_enforcement_readiness.md` | Present / reviewed | P3.2 security readiness posture. | No scanner or enforcement runtime. |
| `0_architecture/governance/agent_platform_knowledge_retrieval_architecture_reconciliation_closure.md` | Present / reviewed | P2.KR retrieval, memory, live connector, Cadence, Graphify, and substrate boundary. | No retrieval runtime, vector DB, graph DB, or live connector activation. |
| `0_architecture/governance/agent_platform_cross_lane_integration_reconciliation_closure.md` | Present / reviewed | P2.R integrated P2 baseline. | Reconciliation only. |
| `0_architecture/governance/agent_platform_shared_metadata_vocabulary_alignment.md` | Present / reviewed | P2.1 vocabulary for status, refs, blockers, sensitivity, posture, and source classification. | No schema runtime. |
| `0_architecture/governance/agent_platform_cross_lane_evidence_reference_contract.md` | Present / reviewed | P2.2 EvidenceRef, SourceRef, ValidationRef, SecurityRef, GraphifyRef, ProductRef semantics. | Evidence supports; it does not decide. |
| `0_architecture/governance/agent_platform_audit_retention_rollback_baseline.md` | Present / reviewed | P2.3 audit, retention, rollback, quarantine, incident, blocker, and tracking baseline. | No runtime logging, persistence, or automation. |
| `0_architecture/governance/agent_platform_context_runtime_contract_hardening.md` | Present / reviewed | P1.1 context metadata and source-ref boundary. | Context inclusion is not permission. |
| `0_architecture/governance/agent_platform_provider_adapter_metadata_contract_hardening.md` | Present / reviewed | P1.2 provider metadata and credential-ref boundary. | Provider metadata is not provider activation. |
| `0_architecture/governance/agent_platform_tool_execution_boundary_contract_hardening.md` | Present / reviewed | P1.3 tool metadata and execution blocker boundary. | Tool metadata is not tool execution. |
| `0_architecture/governance/agent_platform_agent_runtime_boundary_contract_hardening.md` | Present / reviewed | P1.4 agent, task, handoff, approval, output, and blocker boundary. | Agent metadata is not agent execution. |
| `0_architecture/governance/agent_platform_cognitive_semantic_system_prototype_hardening.md` | Present / reviewed | P1.5 Cognitive Semantic System metadata and substrate boundary. | No graph/vector/database/ontology runtime. |
| `0_architecture/governance/agent_platform_activation_gate_enforcement_map.md` | Present / reviewed | P0.1 gate control map. | Gate references are not approvals. |
| `0_architecture/governance/agent_platform_validation_execution_gate_design.md` | Present / reviewed | P0.2 validation gate model. | Gate design does not execute validation. |
| `0_architecture/governance/agent_platform_security_enforcement_hardening_plan.md` | Present / reviewed | P0.3 security hardening model. | Hardening design is not enforcement. |
| `0_architecture/governance/agent_platform_activation_gate_charter.md` | Present / reviewed | Activation gate authority, gate fields, and stop rules. | Charter is not activation. |
| `0_architecture/security/agent_platform_tool_shell_network_mcp_execution_policy.md` | Present / reviewed | S-04 execution policy and blocked defaults. | No shell, network, MCP, tool, package, test, build, CI, or Git execution. |
| `0_architecture/security/agent_platform_local_only_secrets_credentials_policy.md` | Present / reviewed | S-03 local-only, secret, credential, generated output, and provider-auth handling. | No secret, credential, `.env`, provider config, token store, browser auth, or API key inspection. |
| `0_architecture/cognitive_semantic_system/agent_platform_cognitive_semantic_system_naming_substrate_adr.md` | Present / reviewed | Accepted Cognitive Semantic System name and substrate deferral. | ADR is not implementation authorization. |
| `0_architecture/cognitive_semantic_system/agent_platform_cognitive_semantic_system_decision_audit.md` | Present / reviewed | CSS naming/substrate audit. | No substrate selected. |
| `README.md` | Present / reviewed | Repository orientation. | No runtime effect. |
| `.gitignore` | Present / reviewed | Local-only/generated/secrets/provider-auth hygiene posture. | Not modified; ignore rules are not enforcement. |
| `.graphifyignore` | Present / reviewed | Graphify default-deny and hard-exclusion posture. | Not modified; not permission to run or adopt Graphify. |
| Optional P6.1 Agent Capability Registry Operational Contract | Absent | Not consumed. | `pending_P6.1_agent_registry_alignment`. |
| Optional P6.2 Agent-to-Agent Communication Protocol | Absent | Not consumed. | `pending_P6.2_agent_to_agent_protocol_alignment`. |
| Optional P6.4 Human Approval / Review Loop Operational Contract | Absent | Not consumed. | `pending_P6.4_human_approval_alignment`. |
| Optional P6.5 Runtime Monitoring / Incident Handling Operational Contract | Absent | Not consumed. | `pending_P6.5_monitoring_incident_alignment`. |
| Optional P6.6 Cognitive Semantic System Substrate Decision | Absent | Not consumed. | `cognitive_semantic_system_substrate_deferred`. |
| `external/sources` | Absent by path-only check | Candidate path metadata only. | Contents not inspected. |
| `external/sources/gbrain-master` | Absent by path-only check | If later present, remains external_source_candidate and cadence_reference_candidate. | not adopted; not executed; not imported; not configured; not dependency-approved; not provider/auth-approved; not Cadence-active; not substrate; content not inspected. |
| `3_platform` | Present by path-only check | Platform path posture only. | Contents not inspected. |
| `3_platform/_governed_skeleton` | Present by path-only check | Skeleton path posture only. | No P5 skeleton code inspected or modified by P6.3. |
| `9_artifacts` | Present by path-only check | Generated/local-only path metadata only. | Contents not inspected or modified. |
| `graphify-out` | Absent by path-only check | Generated output path metadata only. | Contents not inspected. |

## Dependency Posture

P6.3 consumes P5.3 Context Assembly Runtime Candidate.

P6.3 consumes P5.7 Audit / Retention / Rollback Runtime Hooks.

P6.3 consumes P2.2 Cross-Lane Evidence Reference Contract.

P6.3 consumes P2.3 Audit / Retention / Rollback Baseline.

P6.3 consumes P2.KR Knowledge / Retrieval Architecture Reconciliation Closure.

P6.3 consumes P3.0 Controlled Source Classification Readiness.

P6.3 consumes P3.1 Validation Execution Readiness.

P6.3 consumes P3.2 Security Enforcement Readiness.

P6.3 consumes P3.BR Activation Decision Reconciliation Closure.

P6.3 consumes P1.1 Context Runtime Contract Hardening.

P6.3 may consume P6.1, P6.2, P6.4, P6.5, and P6.6 if present.

P6.3 must not create, modify, or supersede P6.1, P6.2, P6.4, P6.5, P6.6, or P6.7.

P6.3 may record drift candidates for P6.7 reconciliation.

## Operational Model

The Shared Context / Evidence Bus is a metadata-only coordination contract for future platform components. It defines how components would reference context packs, evidence records, source refs, validation refs, security refs, retention refs, rollback refs, incident refs, publication decisions, and blocker posture.

Bus contract is not bus runtime.

Bus message envelope is not message dispatch.

Bus publication decision is not publication approval.

Bus retention posture is not persistence.

ContextPackRef is not context materialization.

EvidenceRef binding is not authority.

SourceRef binding is not source loading.

ValidationRef binding is not validation execution.

SecurityRef binding is not security enforcement activation.

RetentionRef binding is not persistence.

RollbackRef binding is not rollback automation.

IncidentRef binding is not incident automation.

Graph / relationship references are not Cognitive Semantic System substrate selection.

## Object Model

| object | meaning | required fields | forbidden fields | security posture | validation posture | governance posture |
| --- | --- | --- | --- | --- | --- | --- |
| ContextBusRecord | Top-level metadata record for context refs moving through the contract. | Context refs, source/evidence/validation/security/retention/rollback/incident bindings, blockers, limitations, review. | Raw source content, secrets, credentials, provider payloads, raw generated outputs, dispatch fields. | Highest sensitivity and blockers propagate. | Future completeness validation only. | Metadata contract only. |
| EvidenceBusRecord | Top-level metadata record for evidence refs and evidence relationships. | Evidence refs, bindings, source posture, authority posture, blockers, limitations, review. | Raw evidence content, raw Graphify output, source bodies, provider/tool/agent payloads. | Evidence sensitivity and generated-output blockers propagate. | Future completeness validation only. | Evidence supports; it does not decide. |
| BusMessageEnvelope | Metadata-only message envelope for future protocol references. | Sender/receiver refs, context/evidence refs, dispatch metadata, blockers, stop rules. | Queue IDs as runtime handles, broker topics, websocket channels, payload bodies, execution triggers. | No secrets, credentials, raw source, provider output, or live connector payloads. | Future field completeness only. | Envelope is not dispatch. |
| ContextPackRef | Reference to a future or existing context pack metadata record. | Pack identity, owner, scope, source refs, blockers, evidence/validation/security refs. | Context content, source body, secret/credential values, raw generated output. | Source classification and sensitivity required. | Future ref completeness only. | Context inclusion is not permission. |
| EvidenceRefBinding | Binding between evidence ref and target metadata object. | Evidence ref, bound target, authority posture, source classification, limitations, review. | Self-approval, raw evidence body, Graphify authority claim. | Sensitive or generated evidence remains constrained. | Future invariant validation only. | EvidenceRef binding is not authority. |
| SourceRefBinding | Binding between source ref and target metadata object. | Source ref, classification, sensitivity, path metadata, allowed/blocked use, blockers. | Source body, traversal payloads, product/external/raw/generated content. | Unknown, secret, credential, product, external, generated, and local-only classes remain blocked. | Future classification validation only. | SourceRef binding is not source loading. |
| ValidationRefBinding | Binding between validation ref and target metadata object. | Validation ref, target, status, scope, limitations, output posture, blockers. | Validation command output as authority, execution command, logs with sensitive data. | Generated output and sensitive validation output remain blocked. | Validation evaluates; governance decides. | Not validation execution. |
| SecurityRefBinding | Binding between security ref and target metadata object. | Security ref, target, status, scope, blockers, sensitivity, posture. | Permission grants, secret values, credential values, auth material. | Security constrains and blocks. | Future blocker preservation only. | SecurityRef binding does not activate. |
| RetentionRefBinding | Binding between retention ref and target metadata object. | Retention ref, posture, reason, redaction/quarantine route, blockers. | Storage implementation, event store, file log, DB handle. | Retention minimizes exposure. | Future retention field check only. | RetentionRef binding is not persistence. |
| RollbackRefBinding | Binding between rollback ref and target metadata object. | Rollback trigger, route, owner, impacted surfaces, review requirements. | Rollback executor, deletion command, credential rotation command, automation trigger. | Security review required for impacted surfaces. | Future route completeness only. | RollbackRef binding is not rollback automation. |
| IncidentRefBinding | Binding between incident ref and target metadata object. | Incident type, trigger, safe metadata, forbidden content, routes, review requirements. | Alerting runtime, monitoring daemon, automatic quarantine/deletion/rollback. | Sensitive content avoidance required. | Future incident field check only. | IncidentRef binding is not incident automation. |
| BusPublicationDecision | Metadata posture for whether a target could ever be published. | Status, scope, blockers, required reviews, allowed/blocked use. | Approved publication status, publication action, Git mutation. | Security review required when sensitive. | Validation review required when evidence/output is involved. | Cannot approve publication in P6.3. |
| BusRetentionPosture | Metadata posture for retaining bus-related refs. | Status, scope, reason, local-only posture, redaction/quarantine/rollback/incident routes. | Storage handle, DB, event store, telemetry pipeline, file log. | Local-only and generated-output constraints preserved. | Future retention validation only. | Not persistence. |

## ContextBusRecord Contract

Required fields:

```text
context_bus_record_id
bus_scope
bus_status
context_pack_refs
context_item_refs
source_ref_bindings
evidence_ref_bindings
validation_ref_bindings
security_ref_bindings
retention_ref_bindings
rollback_ref_bindings
incident_ref_bindings
source_classification
sensitivity
local_only
generated_output_posture
product_posture
provider_auth_posture
live_connector_posture
publication_decision_ref
retention_posture_ref
publication_blockers
source_tracking_blockers
generated_output_blockers
allowed_metadata_use
blocked_use
limitations
review_required
```

ContextBusRecord is metadata only.

ContextBusRecord does not create a bus runtime.

ContextBusRecord does not materialize context.

ContextBusRecord does not load source.

ContextBusRecord does not persist.

## EvidenceBusRecord Contract

Required fields:

```text
evidence_bus_record_id
bus_scope
bus_status
evidence_refs
evidence_ref_bindings
source_ref_bindings
validation_ref_bindings
security_ref_bindings
retention_ref_bindings
rollback_ref_bindings
incident_ref_bindings
graphify_refs
product_refs
authority_posture
evidence_posture
source_classification
sensitivity
local_only
generated_output_posture
publication_decision_ref
retention_posture_ref
publication_blockers
source_tracking_blockers
generated_output_blockers
limitations
review_required
```

Evidence supports; it does not decide.

EvidenceBusRecord cannot make evidence authoritative.

Graphify evidence remains supporting generated evidence only.

Generated evidence remains generated evidence unless future governance promotes exact scope.

## BusMessageEnvelope Contract

Required fields:

```text
bus_message_envelope_id
message_type
sender_ref
receiver_ref
conversation_ref
handoff_ref
context_pack_refs
evidence_refs
source_refs
validation_refs
security_refs
retention_refs
rollback_refs
incident_refs
approval_refs
publication_decision_refs
source_classification
sensitivity
local_only
generated_output_posture
product_posture
provider_auth_posture
live_connector_posture
dispatch_status
dispatch_decision
allowed_metadata_use
blocked_use
stop_rules
limitations
review_required
```

BusMessageEnvelope is not message dispatch.

Dispatch status must remain metadata-only.

No queue, broker, websocket, event stream, provider call, MCP call, tool call, agent wake-up, scheduler, orchestration loop, or handoff execution is approved by P6.3.

## ContextPackRef Contract

Required fields:

```text
context_pack_ref_id
context_pack_id
context_pack_owner
context_pack_scope
context_pack_status
context_source_refs
source_classification
sensitivity
local_only
generated_output_posture
product_posture
external_posture
credential_related
secret_related
allowed_metadata_use
blocked_use
evidence_refs
validation_refs
security_refs
retention_refs
publication_blockers
source_tracking_blockers
limitations
review_required
```

ContextPackRef is a reference only.

ContextPackRef does not include context content.

ContextPackRef does not authorize source loading.

Context inclusion is not permission.

## EvidenceRefBinding Contract

Required fields:

```text
evidence_ref_binding_id
evidence_ref
bound_target_ref
bound_target_type
evidence_status
authority_posture
source_classification
sensitivity
generated_output_posture
graphify_related
product_related
validation_refs
security_refs
retention_refs
limitations
review_required
```

EvidenceRef binding supports review only.

EvidenceRef binding does not decide.

EvidenceRef binding does not override validation/security/governance.

## SourceRefBinding Contract

Required fields:

```text
source_ref_binding_id
source_ref
bound_target_ref
source_classification
sensitivity
path_or_identifier_metadata
allowed_metadata_use
blocked_use
required_future_gate
tracking_posture
retention_posture
evidence_posture
security_refs
validation_refs
blockers
limitations
review_required
```

SourceRef binding is not source loading.

Path presence is not content inspection permission.

Product source, external source content, GBrain/Hermes source, raw generated output, raw Graphify output, local-only content, secrets, and credentials remain blocked unless future exact gates approve.

## ValidationRefBinding Contract

Required fields:

```text
validation_ref_binding_id
validation_ref
bound_target_ref
validation_status
validation_scope
validation_limitations
validation_output_posture
generated_output_posture
security_refs
evidence_refs
retention_refs
publication_blockers
source_tracking_blockers
limitations
review_required
```

ValidationRef binding is not validation execution.

Validation evaluates; governance decides.

Validation output handling must preserve generated-output posture, retention posture, rollback route, incident route, publication blockers, and source tracking blockers.

## SecurityRefBinding Contract

Required fields:

```text
security_ref_binding_id
security_ref
bound_target_ref
security_status
security_scope
security_limitations
security_blockers
source_classification
sensitivity
provider_auth_posture
tool_execution_posture
agent_execution_posture
live_connector_posture
product_posture
publication_blockers
source_tracking_blockers
limitations
review_required
```

SecurityRef binding constrains.

SecurityRef binding does not activate.

SecurityRef binding does not approve source loading, tool execution, provider/auth, agent execution, live connector activation, publication, source tracking, or generated output tracking.

## RetentionRefBinding Contract

Required fields:

```text
retention_ref_binding_id
retention_ref
bound_target_ref
retention_posture
retention_reason
retention_limitations
local_only
generated_output_posture
redaction_route
quarantine_route
publication_blockers
source_tracking_blockers
review_required
```

RetentionRef binding is not persistence.

Retention posture does not approve database storage, event store, file log, telemetry, source tracking, generated output tracking, or publication.

## RollbackRefBinding Contract

Required fields:

```text
rollback_ref_binding_id
rollback_ref
bound_target_ref
rollback_trigger
rollback_route
rollback_owner
impacted_surfaces
deactivation_route
removal_route
credential_rotation_route
evidence_retention_requirement
security_review_required
validation_review_required
governance_review_required
limitations
review_required
```

RollbackRef binding is not rollback automation.

Rollback route does not execute rollback, deletion, quarantine, deactivation, credential rotation, or remediation.

## IncidentRefBinding Contract

Required fields:

```text
incident_ref_binding_id
incident_ref
bound_target_ref
incident_type
incident_trigger
safe_metadata_to_record
forbidden_content_to_avoid
stop_condition
quarantine_route
rollback_route
security_review_requirement
validation_review_requirement
governance_review_requirement
publication_blockers
source_tracking_blockers
follow_up_ticket_requirement
limitations
review_required
```

IncidentRef binding is not incident automation.

Incident route does not create alerting, monitoring runtime, background workers, automatic quarantine, deletion, publication, or rollback.

## BusPublicationDecision Contract

Required fields:

```text
bus_publication_decision_id
target_ref
target_type
publication_status
publication_scope
publication_blockers
source_tracking_blockers
generated_output_blockers
required_security_review
required_validation_review
required_governance_review
required_human_approval
allowed_publication_use
blocked_publication_use
limitations
review_required
```

Allowed publication statuses:

```text
blocked
not_evaluated
requires_security_review
requires_validation_review
requires_governance_review
requires_human_approval
rejected_for_scope
```

BusPublicationDecision cannot approve publication in P6.3.

Publication remains blocked unless future exact-scope governance approves.

## BusRetentionPosture Contract

Required fields:

```text
bus_retention_posture_id
target_ref
target_type
retention_status
retention_scope
retention_reason
retention_limitations
local_only
generated_output_posture
redaction_route
quarantine_route
rollback_route
incident_route
publication_blockers
source_tracking_blockers
generated_output_blockers
review_required
```

Allowed retention statuses:

```text
metadata_only
local_only_metadata
blocked_content
deferred
requires_security_review
requires_governance_review
```

BusRetentionPosture is not persistence.

Retention posture cannot create storage.

Retention posture cannot approve logs, event stores, databases, telemetry, source tracking, generated output tracking, or publication.

## Boundary Model

### Source Loading Boundary

Blocked:

```text
source loading
context materialization from raw source
source path traversal
product source bus
external source content bus
GBrain/Hermes source bus
raw generated output bus
raw Graphify output bus
local-only content bus
secret / credential bus
```

Only metadata refs may move through the contract.

No raw source content may move through the bus.

### Persistence Boundary

Blocked:

```text
persistent bus
database
event store
file logs
telemetry
event streaming
queue
broker
websocket
background worker
```

Bus is not persistence.

Bus contract does not create storage.

Bus contract does not create a transport.

### Execution Boundary

Blocked:

```text
agent execution
task execution
handoff execution
message dispatch
scheduler
orchestration
autonomous loop
tool execution
provider/API/MCP call
live connector activation
Cadence behavior
```

Bus envelope is not dispatch.

Bus record is not runtime.

### Generated Output Boundary

Blocked:

```text
raw generated output bus
raw Graphify output bus
generated output tracking
generated evidence as authority
generated output publication
```

Generated output may be referenced only as metadata with blockers, limitations, retention posture, and review requirements.

### Product Boundary

Siamese is product vision, not product activation.

Product/Siamese source cannot be moved through the bus.

Product-related metadata may be referenced only for readiness planning and blockers.

Product-bound bus behavior requires future P4/product gates.

### Cognitive Semantic System Boundary

Cognitive Semantic System substrate remains deferred unless P6.6 creates a governed no-implementation decision record.

P6.3 does not select substrate.

P6.3 does not implement graph DB, vector DB, ontology runtime, or persistence.

Graph / relationship references remain candidate/evidence posture only.

Graphify evidence remains generated supporting evidence only, not authority.

## Interfaces With P5 Skeletons

### Interface With P5.3 Context Assembly

P6.3 consumes P5.3 Context Assembly Runtime Candidate as source of ContextPackRef and ContextSourceRef metadata.

P6.3 must not cause P5.3 to load source.

P6.3 must preserve P5.3 limitations, blockers, evidence refs, validation refs, security refs, retention refs, publication blockers, and source tracking blockers.

### Interface With P5.7 Audit / Retention / Rollback Hooks

P6.3 consumes P5.7 hook shapes as metadata refs only.

P6.3 must not cause audit persistence.

P6.3 must not cause active logging.

P6.3 must not cause rollback automation.

P6.3 must not cause incident automation.

P6.3 must preserve audit refs, retention refs, rollback refs, incident refs, publication blockers, source tracking blockers, and generated output blockers.

### Interface With P5.1 Validation Runner

P6.3 may reference validation readiness and future ValidationRef bindings.

P6.3 must not execute validation.

P6.3 must not dispatch validation jobs.

### Interface With P5.2 Security Dry-Run

P6.3 may reference security refs and dry-run readiness metadata.

P6.3 must not implement security enforcement.

P6.3 must not run security dry-runs.

### Interface With P5.4 Tool Sandbox

P6.3 may reference tool-related blockers only as metadata.

P6.3 must not execute tools.

P6.3 must not route tool payloads.

### Interface With P5.5 Provider Adapter

P6.3 may reference provider metadata and provider blockers only as metadata.

P6.3 must not call providers.

P6.3 must not route provider auth material.

P6.3 must not route provider output payloads.

### Interface With P5.6 Agent Task / Handoff

P6.3 may reference agent task / handoff metadata as envelope refs.

P6.3 must not execute tasks.

P6.3 must not execute handoffs.

P6.3 must not wake agents or dispatch messages.

## Interfaces With P3 Decisions

P3.3 deferred tool execution activation.

P3.4 deferred provider/auth/API/MCP activation.

P3.5 deferred agent runtime activation.

P3.BR reconciled activation decisions but did not activate runtime behavior.

P6.3 must preserve these decisions.

No bus contract may bypass P3-B decisions.

## Evidence / Validation / Security Interfaces

### Evidence Interface

Evidence supports; it does not decide.

EvidenceRef bindings must preserve limitations, source classification, sensitivity, validation refs, security refs, retention posture, publication blockers, and source tracking blockers.

Graphify evidence is supporting generated evidence only, not authority.

Generated evidence cannot become authority by bus inclusion.

### Validation Interface

Validation evaluates; governance decides.

ValidationRef bindings must not execute validation.

ValidationRef bindings must preserve validation limitations and output handling posture.

### Security Interface

Security constrains; it does not activate.

SecurityRef bindings must preserve blockers.

SecurityRef bindings cannot approve source loading, execution, provider/auth, tool use, agent use, publication, source tracking, generated output tracking, persistence, telemetry, or bus dispatch.

## Retention / Rollback / Incident Posture

P6.3 must preserve P2.3 and P5.7 audit / retention / rollback posture.

Every bus record must carry or reference:

```text
retention posture
redaction route
quarantine route
rollback route
incident route
publication blockers
source tracking blockers
generated output blockers
limitations
review_required
```

P6.3 does not implement logging.

P6.3 does not implement persistence.

P6.3 does not implement rollback automation.

P6.3 does not implement incident automation.

## Human Approval Requirements

Any future bus behavior beyond metadata-only references requires exact future ticket scope and human approval.

Any future publication decision requires explicit human approval and governance.

Any future source tracking or generated output tracking decision requires explicit human approval and governance.

Any future live connector, provider, tool, agent, product, Cadence, persistence, or substrate-related bus behavior requires future exact gates and human approval.

P6.3 grants none of these approvals.

## Stop Rules

```text
bus runtime implementation attempted
message dispatch attempted
queue / broker / websocket attempted
event streaming attempted
telemetry attempted
persistence / database attempted
file logging attempted
context materialization from raw source attempted
source loading attempted
source inspection attempted
product source inspection attempted
external source content inspection attempted
GBrain/Hermes source inspection attempted
raw Graphify output bus attempted
raw generated output bus attempted
secret / credential bus attempted
provider output bus attempted
tool execution attempted
provider/API/MCP call attempted
agent execution attempted
task execution attempted
handoff execution attempted
scheduler/orchestration attempted
autonomous loop attempted
live connector activation attempted
GBrain/Hermes/Cadence activation attempted
Graphify/Codegraph adoption or execution attempted
validation execution attempted
security enforcement activation attempted
vector DB / embeddings attempted
graph DB / ontology runtime attempted
generated output tracking attempted
source tracking expansion attempted
publication attempted
Git mutation attempted
Cognitive Semantic System substrate selection attempted
unknown sensitivity encountered without blocker
missing retention / rollback / incident posture
```

## Drift Register

| drift_id | source_area | observed_term_or_rule | canonical_or_proposed_rule | status | pending_dependency | impact | resolution_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BUS-DRIFT-001 | P6 sibling | missing P6.1 registry alignment | Agent/capability registry metadata can align later. | open | `pending_P6.1_agent_registry_alignment` | Registry refs remain generic. | P6.1 or P6.7 reconciliation. |
| BUS-DRIFT-002 | P6 sibling | missing P6.2 protocol alignment | BusMessageEnvelope remains protocol-adjacent metadata only. | open | `pending_P6.2_agent_to_agent_protocol_alignment` | Message fields may need later alignment. | P6.2 or P6.7 reconciliation. |
| BUS-DRIFT-003 | P6 sibling | missing P6.4 human approval alignment | Approval refs remain non-approval metadata. | open | `pending_P6.4_human_approval_alignment` | Human approval route not operationalized. | P6.4 or P6.7 reconciliation. |
| BUS-DRIFT-004 | P6 sibling | missing P6.5 monitoring / incident alignment | Incident refs remain non-runtime route metadata. | open | `pending_P6.5_monitoring_incident_alignment` | Monitoring and incident runtime absent. | P6.5 or P6.7 reconciliation. |
| BUS-DRIFT-005 | contract boundary | bus contract vs bus runtime | Bus contract is metadata-only; no bus runtime. | guarded | `pending_P6.7_operational_readiness_reconciliation` | Prevents accidental queue/broker implementation. | P6.7 invariant check. |
| BUS-DRIFT-006 | envelope boundary | bus message envelope vs message dispatch | Envelope metadata cannot dispatch messages. | guarded | `pending_P6.7_operational_readiness_reconciliation` | Prevents scheduler/dispatch inference. | P6.7 invariant check. |
| BUS-DRIFT-007 | context boundary | ContextPackRef vs context materialization | ContextPackRef is reference only. | guarded | none | Prevents raw source inclusion. | Future schema hardening. |
| BUS-DRIFT-008 | evidence boundary | EvidenceRef binding vs evidence authority | EvidenceRef binding supports review only. | guarded | none | Prevents evidence self-approval. | Future evidence validation. |
| BUS-DRIFT-009 | source boundary | SourceRef binding vs source loading | SourceRef binding is not source loading. | guarded | none | Prevents path/content expansion. | Future source gate. |
| BUS-DRIFT-010 | retention boundary | RetentionRef binding vs persistence | RetentionRef binding is not persistence. | guarded | none | Prevents storage/log/event-store inference. | Future persistence gate if ever scoped. |
| BUS-DRIFT-011 | rollback boundary | RollbackRef binding vs rollback automation | RollbackRef binding is not rollback automation. | guarded | none | Prevents automatic remediation. | Future rollback gate. |
| BUS-DRIFT-012 | incident boundary | IncidentRef binding vs incident automation | IncidentRef binding is not incident automation. | guarded | `pending_P6.5_monitoring_incident_alignment` | Prevents alerting/runtime worker inference. | P6.5/P6.7. |
| BUS-DRIFT-013 | publication boundary | BusPublicationDecision vs publication approval | Publication cannot be approved by P6.3. | guarded | `pending_P6.4_human_approval_alignment` | Prevents publishing/Git mutation. | Future exact gate. |
| BUS-DRIFT-014 | Graphify boundary | Graphify evidence vs authority/substrate | Graphify evidence is supporting generated evidence only. | guarded | `cognitive_semantic_system_substrate_deferred` | Prevents generated evidence from selecting substrate. | P6.6/P6.7. |
| BUS-DRIFT-015 | CSS boundary | Cognitive Semantic System relationship refs vs substrate selection | Relationship refs are substrate-neutral. | guarded | `cognitive_semantic_system_substrate_deferred` | Prevents graph/vector/ontology runtime inference. | P6.6 or defer. |
| BUS-DRIFT-016 | live connector boundary | live connector data vs persistent bus | Live connector payloads cannot move through the bus. | guarded | `pending_P6.7_operational_readiness_reconciliation` | Prevents live ingestion/persistence. | Future connector gate only. |

## Operational Invariants

BUS-001 P6.3 is a Shared Context / Evidence Bus operational contract only.

BUS-002 Operational planning is not activation.

BUS-003 Bus is not persistence.

BUS-004 Bus message envelope is not message dispatch.

BUS-005 ContextPackRef is not context materialization.

BUS-006 SourceRef binding is not source loading.

BUS-007 EvidenceRef binding is not authority.

BUS-008 ValidationRef binding is not validation execution.

BUS-009 SecurityRef binding is not security enforcement activation.

BUS-010 RetentionRef binding is not persistence.

BUS-011 RollbackRef binding is not rollback automation.

BUS-012 IncidentRef binding is not incident automation.

BUS-013 BusPublicationDecision is not publication approval.

BUS-014 Context inclusion is not permission.

BUS-015 Evidence supports; it does not decide.

BUS-016 Validation evaluates; governance decides.

BUS-017 Security constrains; it does not activate.

BUS-018 Provider metadata is not provider activation.

BUS-019 Tool metadata is not tool execution.

BUS-020 Agent metadata is not agent execution.

BUS-021 Raw generated output cannot move through the bus.

BUS-022 Raw Graphify output cannot move through the bus.

BUS-023 Product source cannot move through the bus.

BUS-024 Live connector payloads cannot move through the bus.

BUS-025 Secrets and credentials cannot move through the bus.

BUS-026 No persistence, database, event stream, or telemetry is approved by P6.3.

BUS-027 No vector DB or graph DB is approved by P6.3.

BUS-028 Cognitive Semantic System substrate remains deferred.

BUS-029 GBrain / Hermes / Cadence remain future and inactive.

BUS-030 AGENT PLATFORM remains AL-1 metadata skeleton.

## Future Validation Targets

The following are proposed future validation targets only; none are executed by P6.3:

```text
shared context evidence bus document exists
ContextBusRecord required fields completeness
EvidenceBusRecord required fields completeness
BusMessageEnvelope required fields completeness
ContextPackRef required fields completeness
EvidenceRefBinding required fields completeness
SourceRefBinding required fields completeness
ValidationRefBinding required fields completeness
SecurityRefBinding required fields completeness
RetentionRefBinding required fields completeness
RollbackRefBinding required fields completeness
IncidentRefBinding required fields completeness
BusPublicationDecision required fields completeness
BusRetentionPosture required fields completeness
no bus runtime invariant
no persistence invariant
no event streaming invariant
no telemetry invariant
no message dispatch invariant
no context materialization invariant
no source loading invariant
no product source bus invariant
no raw generated output bus invariant
no raw Graphify output bus invariant
no secret / credential bus invariant
EvidenceRef binding does not decide invariant
ValidationRef binding does not execute invariant
SecurityRef binding does not activate invariant
RetentionRef binding does not persist invariant
RollbackRef binding does not automate invariant
IncidentRef binding does not automate invariant
P6.1 registry alignment completeness
P6.2 protocol alignment completeness
P6.4 approval alignment completeness
P6.5 monitoring/incident alignment completeness
Cognitive Semantic System substrate deferred invariant
```

## Future Hardening Candidates

Future tickets proposed only, not started:

```text
BUS-HARD-01 - ContextBusRecord Schema Alignment
BUS-HARD-02 - EvidenceBusRecord Schema Alignment
BUS-HARD-03 - BusMessageEnvelope Schema Alignment
BUS-HARD-04 - ContextPackRef / SourceRef Binding Alignment
BUS-HARD-05 - EvidenceRef / ValidationRef / SecurityRef Binding Alignment
BUS-HARD-06 - RetentionRef / RollbackRef / IncidentRef Binding Alignment
BUS-HARD-07 - BusPublicationDecision Boundary Alignment
BUS-HARD-08 - BusRetentionPosture Boundary Alignment
BUS-HARD-09 - Shared Context / Evidence Bus Drift Validation Design
BUS-HARD-10 - Bus Contract Integration With Agent Protocol
BUS-HARD-11 - Bus Contract Integration With Human Approval Loop
BUS-HARD-12 - Bus Contract Integration With Monitoring / Incident Handling
```

## Created / Not Created Register

```text
shared context / evidence bus operational contract created
no bus runtime implemented
no queue implemented
no broker implemented
no websocket implemented
no message dispatch implemented
no event streaming implemented
no telemetry implemented
no database implemented
no persistence implemented
no source loading approved
no context materialization from raw source approved
no source inspection performed
no product source inspected
no external source inspected
no GBrain source inspected
no Hermes source inspected
no raw Graphify output inspected
no raw generated output bus approved
no raw Graphify output bus approved
no product source bus approved
no live connector payload bus approved
no secret / credential bus approved
no provider output bus approved
no provider/auth/API/MCP activation approved
no credential use approved
no API calls executed
no MCP calls executed
no network calls executed
no tool execution approved
no agent execution approved
no task execution approved
no handoff execution approved
no scheduler/orchestration activated
no autonomous loop activated
no live connector activated
no GBrain activated
no GBrain adopted
no Hermes activated
no Cadence activated
no always-on behavior activated
no Graphify rerun
no Graphify adoption approved
no Codegraph execution approved
no validation executed
no tests executed
no CI executed
no scripts executed
no security enforcement activated
no vector DB implemented
no embeddings generated
no graph DB implemented
no ontology runtime implemented
no Cognitive Semantic System substrate selected
no generated outputs modified/tracked
no source tracking expansion approved
no publication approved
no Git mutation by the agent
no .graphifyignore modified
no .gitignore modified
no P6.1 created or modified
no P6.2 created or modified
no P6.4 created or modified
no P6.5 created or modified
no P6.6 created or modified
no P6.7 started
no P7 started
no P4 started
no EXT.* started
```

## Recommended Next Tickets

After P6.3:

```text
P6.1 - Agent Registry / Capability Registry, if not already completed
P6.2 - Agent-to-Agent Communication Protocol, if not already completed
P6.4 - Human Approval / Review Loop, if not already completed
P6.5 - Runtime Monitoring / Incident Handling, if not already completed
P6.6 - Cognitive Semantic System Substrate Decision, only if needed
P6.7 - Operational Readiness Audit, after P6.1-P6.5 and P6.6 decision/defer posture
```

Recommended actual if P6.1/P6.2/P6.4/P6.5 are incomplete:

```text
Complete the remaining parallel P6 operational contracts before P6.7.
```

Recommended actual after P6.1-P6.5 are complete and P6.6 is either deferred or complete:

```text
P6.7 - Operational Readiness Audit
```

Do not recommend runtime activation, agent execution, task execution, handoff execution, tool execution, provider/auth activation, live connector activation, product activation, Graphify/Codegraph adoption, GBrain/Hermes/Cadence activation, source loading, source tracking expansion, vector DB implementation, graph DB implementation, or Cognitive Semantic System substrate implementation.

## Final Verdict

| Question | Answer |
| --- | --- |
| What did P6.3 create? | A single metadata-only Shared Context / Evidence Bus operational contract. |
| What Shared Context / Evidence Bus operational contract was defined? | A coordination contract for referencing context, evidence, source, validation, security, retention, rollback, incident, approval, monitoring, agent, tool, provider, and publication metadata without runtime behavior. |
| What ContextBusRecord was defined? | A metadata-only record carrying context pack refs, context item refs, bindings, classifications, blockers, allowed metadata use, blocked use, limitations, and review posture. |
| What EvidenceBusRecord was defined? | A metadata-only record carrying evidence refs and bindings with source, authority, generated-output, Graphify, product, retention, blocker, and review posture. |
| What BusMessageEnvelope was defined? | A metadata-only protocol envelope for future sender/receiver/conversation/handoff refs, context/evidence refs, dispatch metadata, blockers, stop rules, and review posture. |
| What ContextPackRef was defined? | A reference-only contract to a context pack metadata record, not context content and not source loading permission. |
| What EvidenceRef binding was defined? | A review-support binding between evidence refs and targets that cannot decide or override validation, security, or governance. |
| What SourceRef binding was defined? | A source metadata binding that preserves classification, sensitivity, allowed/blocked use, blockers, and review without loading source. |
| What ValidationRef binding was defined? | A validation metadata binding that preserves validation status, scope, output posture, blockers, and limitations without executing validation. |
| What SecurityRef binding was defined? | A security metadata binding that constrains source, tool, provider, agent, live connector, product, publication, and tracking posture without activation. |
| What RetentionRef binding was defined? | A retention metadata binding that records posture, reason, redaction/quarantine routes, and blockers without persistence. |
| What RollbackRef binding was defined? | A rollback route metadata binding without rollback, deletion, quarantine, deactivation, credential rotation, or remediation automation. |
| What IncidentRef binding was defined? | An incident route metadata binding without alerting, monitoring runtime, background workers, quarantine, deletion, publication, or rollback automation. |
| What BusPublicationDecision was defined? | A metadata decision posture that can block, defer, reject, or require reviews but cannot approve publication in P6.3. |
| What BusRetentionPosture was defined? | A metadata retention posture that cannot create logs, event stores, databases, telemetry, tracking, publication, or storage. |
| What source loading boundaries were defined? | Source loading, context materialization from raw source, path traversal, product source bus, external source content bus, GBrain/Hermes source bus, raw generated output bus, raw Graphify output bus, local-only content bus, and secret / credential bus are blocked. |
| What persistence boundaries were defined? | Persistent bus, database, event store, file logs, telemetry, event streaming, queue, broker, websocket, and background worker are blocked. |
| What execution boundaries were defined? | Agent execution, task execution, handoff execution, message dispatch, scheduler, orchestration, autonomous loop, tool execution, provider/API/MCP call, live connector activation, and Cadence behavior are blocked. |
| What generated output boundaries were defined? | Raw generated output bus, raw Graphify output bus, generated output tracking, generated evidence as authority, and generated output publication are blocked. |
| What product boundaries were defined? | Siamese remains product vision only; product/Siamese source cannot move through the bus and product-bound behavior requires future product gates. |
| What Cognitive Semantic System substrate boundaries were defined? | Substrate remains deferred; no vector DB, graph DB, ontology runtime, persistence, Graphify adoption, or substrate selection is approved. |
| How does P6.3 interface with P5.3? | It consumes P5.3 ContextPackRef and ContextSourceRef metadata and preserves no-source-loading limitations and blockers. |
| How does P6.3 interface with P5.7? | It consumes P5.7 audit, retention, rollback, incident, and blocker shapes as metadata refs only. |
| How does P6.3 interface with P3 decisions? | It preserves P3.3 tool deferral, P3.4 provider/auth/API/MCP deferral, P3.5 agent runtime deferral, and P3.BR non-activation. |
| Were bus runtime, queue, broker, websocket, or message dispatch implemented? | No. |
| Was persistence, database, event store, event streaming, or telemetry implemented? | No. |
| Was context materialized from raw source? | No. |
| Was source loading approved? | No. |
| Was product source inspected? | No. |
| Was external source inspected? | No. |
| Was GBrain/Hermes source inspected? | No. |
| Were raw Graphify outputs inspected? | No. |
| Were secrets or credentials inspected? | No. |
| Was raw generated output bus approved? | No. |
| Was raw Graphify output bus approved? | No. |
| Was secret / credential bus approved? | No. |
| Was provider output bus approved? | No. |
| Was provider/auth/API/MCP activated? | No. |
| Were tools executed? | No. |
| Were agents executed? | No. |
| Were tasks or handoffs executed? | No. |
| Were live connectors activated? | No. |
| Were GBrain/Hermes/Cadence activated? | No. |
| Was Graphify/Codegraph adopted or executed? | No. |
| Was validation executed? | No. |
| Was security enforcement activated? | No. |
| Was vector DB or graph DB implemented? | No. |
| Were embeddings generated? | No. |
| Was generated output tracking approved? | No. |
| Was source tracking expansion approved? | No. |
| Was publication approved? | No. |
| Was Cognitive Semantic System substrate selected? | No. |
| What pending P6 alignments remain? | `pending_P6.1_agent_registry_alignment`, `pending_P6.2_agent_to_agent_protocol_alignment`, `pending_P6.4_human_approval_alignment`, `pending_P6.5_monitoring_incident_alignment`, and `cognitive_semantic_system_substrate_deferred`. |
| What is the next ticket? | Complete the remaining parallel P6 operational contracts before P6.7; if P6.1/P6.2/P6.4/P6.5 are incomplete, start one of those next. |
