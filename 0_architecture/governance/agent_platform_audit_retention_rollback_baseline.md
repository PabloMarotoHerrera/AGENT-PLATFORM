# P2.3 - Audit / Retention / Rollback Baseline

## Document Header
| Field | Value |
| --- | --- |
| Title | Audit / Retention / Rollback Baseline |
| Ticket | P2.3 |
| Status | Accepted audit / retention / rollback baseline |
| Date | 2026-07-04 |
| Scope | Define the cross-lane audit, retention, generated-output handling, local-only handling, redaction, quarantine, rollback, publication blocker, source tracking blocker, and incident-handling metadata baseline for AGENT PLATFORM / Siamese across P1 metadata-only contracts. |
| Authority | Audit / retention / rollback baseline only, not runtime logging, persistence, telemetry, rollback automation, validation execution, source loading, source tracking approval, generated output tracking approval, provider/auth approval, tool execution approval, agent execution approval, product activation, Graphify adoption, publication approval, Git mutation approval, or Cognitive Semantic System substrate selection. |
| Related documents | P0.1, P0.2, P0.3, G-19, Activation Gate Charter, P1.1 Context Runtime Contract Hardening, P1.2 Provider Adapter Metadata Contract Hardening, P1.3 Tool Execution Boundary Contract Hardening, P1.4 Agent Runtime Boundary Contract Hardening, P1.5 Cognitive Semantic System Prototype Hardening, Implementation Audit, Context Pack Runtime implementation record, Provider Adapter Layer implementation record, Tool Execution Boundary implementation record, Agent Runtime Boundary implementation record, Validation Registry implementation record, Security Access Enforcement implementation record, Cognitive Semantic System Prototype implementation record, Tool / Shell / Network / MCP Execution Policy, Local-Only / Secrets / Credentials Policy, Cognitive Semantic System ADR / audit, Graphify Repo Map Summary, `.gitignore`, `.graphifyignore`, README.md, Optional P2.1 if present, Optional P2.2 if present. |
| Output | audit / retention / rollback baseline |

This document is the canonical Audit / Retention / Rollback Baseline for AGENT PLATFORM / Siamese.

## Purpose
P1 hardened separate metadata-only contracts for context, providers, tools, agents, and Cognitive Semantic System.

P2 integrates common cross-lane posture without activating any runtime behavior.

P2.3 defines the baseline for audit metadata, evidence retention, generated-output retention, local-only retention, redaction, quarantine, rollback, publication blockers, source tracking blockers, and incident handling.

P2.3 prepares governance readiness for future P3 validation/security readiness.

P2.3 does not execute validation.

P2.3 does not implement runtime logging.

P2.3 does not implement persistence.

P2.3 does not implement telemetry.

P2.3 does not implement rollback automation.

P2.3 does not implement automatic rollback.

P2.3 does not activate provider/auth.

P2.3 does not execute tools.

P2.3 does not execute agents.

P2.3 does not activate product workspaces.

P2.3 does not select Cognitive Semantic System substrate.

P2.3 does not start P3.1.

P2.3 does not start P3.2.

## Current Cross-Lane Posture
AGENT PLATFORM remains pre-active at AL-1 metadata skeleton.

P1.1-P1.5 are metadata-only contracts.

Context inclusion is not permission.

Provider metadata is not provider activation.

Tool metadata is not tool execution.

Agent metadata is not agent execution.

Cognitive Semantic System substrate remains deferred.

Evidence supports review; evidence does not decide.

Validation evaluates; governance decides.

Security constrains.

Graphify evidence is supporting generated evidence only, not authority.

Generated output is not authority by default.

Product-readiness metadata is not Siamese product activation.

No runtime logging, persistence, telemetry, rollback automation, source loading, validation execution, provider/auth, tool execution, agent execution, product activation, Graphify rerun/adoption, generated output tracking, source tracking expansion, or publication is approved by P2.3.

## P2.1 / P2.2 Dependency Posture
P2.3 consumes or anticipates P2.1 vocabulary.

P2.3 consumes or anticipates P2.2 evidence-reference contract.

If P2.1 is present, P2.3 must use P2.1 canonical vocabulary.

If P2.1 is absent, P2.3 must mark vocabulary-dependent names as `pending_P2.1_alignment`.

If P2.2 is present, P2.3 must use P2.2 canonical EvidenceRef shape and relationship model.

If P2.2 is absent, P2.3 must mark evidence-dependent names as `pending_P2.2_alignment`.

P2.1 was absent during P2.3 posture checks, so vocabulary-dependent names in this document remain `pending_P2.1_alignment`.

P2.2 was absent during P2.3 posture checks, so evidence-reference-dependent names in this document remain `pending_P2.2_alignment`.

P2.3 must not create, modify, or supersede P2.1 or P2.2.

P2.3 may record drift candidates for later alignment.

## Audit / Retention / Rollback Baseline Definition
An audit / retention / rollback baseline is a cross-lane governance metadata contract that defines how AGENT PLATFORM records audit events, retention posture, redaction requirements, quarantine routes, rollback requirements, publication blockers, source tracking blockers, and incident handling expectations without implementing runtime logging, persistence, telemetry, rollback automation, or operational incident systems.

Audit metadata is not runtime logging.

Retention posture is not persistence implementation.

Rollback baseline is not rollback automation.

Incident handling baseline is not incident automation.

Publication blocker metadata is not publication approval.

Source tracking blocker metadata is not source tracking approval.

Generated output retention metadata is not generated output tracking approval.

Local-only retention metadata is not permission to include local-only material.

Security incident metadata is not permission to inspect secrets or credentials.

Product-source incident metadata is not permission to inspect product source.

Provider/auth incident metadata is not provider/auth approval.

Tool execution incident metadata is not tool execution approval.

Agent output incident metadata is not agent execution approval.

Graphify output handling is not Graphify adoption.

## Cross-Lane Baseline Object Model
| object | meaning | required fields | forbidden fields | security posture | validation posture | governance posture |
| --- | --- | --- | --- | --- | --- | --- |
| AuditEventMetadata | Cross-lane safe metadata record describing an audit-relevant event or posture. | Identity, type, lane/ticket/actor/target refs, source/evidence/validation/security/Graphify/product/context/provider/tool/agent/semantic refs, classification, sensitivity, retention, publication, rollback, incident, blockers, limitations, review date. | Runtime logs, executable payloads, secrets, credentials, API keys, raw auth, raw product source, raw Graphify output. | Security refs constrain and blockers persist. | Future completeness validation only; no validation execution. | Records review posture only; does not decide. |
| RetentionRecord | Metadata posture for whether and how a record or output may be retained. | Object refs, lane, classification, sensitivity, local-only, generated/product/provider posture, retention reason/cycle, redaction/quarantine refs, blockers, review, limitations. | Storage handles, raw sensitive content, credential values, persistence approval. | Retention minimizes exposure. | Future field completeness and propagation validation only. | Not persistence approval. |
| RedactionRecord | Metadata route for omitting forbidden content. | Target, reason, scope, method, status, sensitivity flags, refs, blockers, review, limitations. | Secret transformations, hashes, partial values, copied product source, raw Graphify output. | Safe metadata only; forbidden content omitted. | Future redaction invariant validation only. | Not permission to inspect content. |
| QuarantineRecord | Metadata route for isolating unsafe or blocked material in future handling. | Quarantined ref/type, trigger, reason, sensitivity, source classification, flags, impacted lanes/surfaces, owner, review route, release/removal route, blockers, refs, limitations. | File movement, deletion commands, content inspection, secret values. | Quarantine route blocks publication and tracking. | Future quarantine field validation only. | Route only; does not move/delete files. |
| RollbackRecord | Metadata route for future rollback expectations. | Trigger, reason, owner, impacted lanes/surfaces/records/outputs, statuses, required stop/quarantine/removal/deactivation/rotation/evidence/review routes, incident/audit refs, limitations. | Automated rollback hooks, destructive commands, credential rotation commands. | Requires security review when sensitive. | Future rollback readiness validation only. | Future expectation only; not approval. |
| IncidentRecord | Safe metadata record for an incident or suspected boundary breach. | Incident type/trigger/summary, target, classification, sensitivity flags, impacted lanes/surfaces, refs, quarantine, rollback, blockers, owner, review, follow-up, limitations. | Quoted forbidden content, secret values, credentials, raw product source, raw Graphify output. | Safe metadata only; stop behavior required. | Future incident metadata validation only. | Does not approve remediation or publication. |
| PublicationBlocker | Explicit metadata blocker preventing publication. | Blocked ref/type, reason, source classification, sensitivity flags, tracking posture, required gate/reviews, clearance, limitations. | Publication approval, broad exception, hidden waiver. | Blocks publication until reviewed. | Future blocker completeness validation only. | Does not approve publication. |
| SourceTrackingBlocker | Explicit metadata blocker preventing tracking, staging, commit, push, force-add, or generated-output tracking. | Blocked ref/type, reason, source classification, sensitivity flags, required gate/reviews, clearance, limitations. | Git mutation approval, source tracking approval, `git add .` permission. | Blocks tracking by default. | Future blocker validation only. | Does not approve tracking. |
| GeneratedOutputHandlingRecord | Metadata posture for generated outputs. | Output ref/type, generator/context, generated posture, local-only, classification, sensitivity, authority/evidence posture, refs, retention/redaction/quarantine, blockers, promotion/removal, review, limitations. | Authority by default, raw secret/product/provider/Graphify content. | Generated outputs are local-only until curated. | Future generated-output posture validation only. | Not tracking or publication approval. |
| LocalOnlyRetentionRecord | Metadata posture for local-only material. | Local-only ref/type, lane, classification, sensitivity, retention reason/posture, allowed metadata use, forbidden use, redaction/quarantine, blockers, refs, review, limitations. | Raw local-only content, publication approval, tracking approval. | Safe metadata only. | Future local-only propagation validation only. | Does not approve inclusion. |
| SecretCredentialIncidentRecord | Specialized safe metadata route for suspected secret or credential incidents. | Incident/detected refs, type flags, safe summary, forbidden handling, stop/redaction/quarantine/security/governance/rotation routes, blockers, rollback, limitations. | Secret/credential values, hashes, partial values, derived identifiers. | Stop and safe metadata only. | No value validation. | Requires future secure review. |
| ProductSourceIncidentRecord | Specialized safe metadata route for product-source boundary incidents. | Incident/product refs, product scope/posture, classification, sensitivity, safe summary, stop/quarantine/review/source tracking/rollback/blockers, limitations. | Product source content, product summaries as substitute for approval. | Product source blocked. | Future product validation only after gate. | Does not activate Siamese. |
| ProviderAuthIncidentRecord | Specialized safe metadata route for provider/auth incidents. | Incident/provider/auth refs, auth posture, secret/credential flags, safe summary, stop/quarantine/security/governance/rotation/deactivation routes, blockers, rollback, limitations. | Provider auth material, tokens, API keys, configs, sessions. | Auth material never retained as content. | No auth validation by P2.3. | Does not configure provider/auth. |
| ToolExecutionIncidentRecord | Specialized safe metadata route for tool execution incidents. | Incident/tool/request/decision refs, execution status/surface, side effects, classification, sensitivity, generated posture, safe summary, stop/quarantine/reviews/rollback/blockers, limitations. | Execution approval, command outputs with forbidden content, shell payloads as approved. | Blocks further execution. | Future validation review only. | Does not approve tool execution. |
| AgentOutputIncidentRecord | Specialized safe metadata route for agent-output incidents. | Incident/agent/task/handoff/output refs, execution status, classification, sensitivity, generated posture, flags, safe summary, stop/quarantine/reviews/rollback/blockers, limitations. | Agent execution approval, raw forbidden output, secrets, credentials. | Agent output remains generated evidence. | Future validation review only. | Does not approve agent execution. |
| GraphifyOutputHandlingRecord | Specialized posture for curated and raw Graphify outputs. | Graphify refs/type/posture, curated flag, raw-output flag, generated/local-only/authority/evidence posture, refs, retention/quarantine, blockers, review, limitations. | Raw Graphify output in context, authority claims, substrate selection, rerun/adoption approval. | Raw output remains local-only. | Future boundary validation only. | Evidence only; not authority. |

## AuditEventMetadata Contract
Required AuditEventMetadata fields:

```text
audit_event_id
audit_event_type
lane_ref
ticket_ref
actor_type
actor_ref
target_ref
target_type
source_refs
evidence_refs
validation_refs
security_refs
graphify_refs
product_refs
related_context_refs
related_provider_refs
related_tool_refs
related_agent_refs
related_semantic_refs
source_classification
sensitivity
local_only
generated_output_posture
product_posture
provider_auth_posture
execution_status
activation_status
tracking_posture
retention_posture
publication_posture
rollback_ref
incident_ref
blockers
limitations
review_required
created_or_reviewed_date
```

AuditEventMetadata is a metadata record only.

AuditEventMetadata does not implement runtime logging.

AuditEventMetadata does not approve execution.

AuditEventMetadata does not approve publication.

AuditEventMetadata must never contain secret values, credential values, API keys, tokens, raw provider auth material, raw product source, or raw generated Graphify output.

## RetentionRecord Contract
Required RetentionRecord fields:

```text
retention_record_id
retained_object_ref
retained_object_type
lane_ref
source_classification
sensitivity
local_only
generated_output_posture
product_posture
provider_auth_posture
retention_posture
retention_reason
retention_duration_or_review_cycle
redaction_ref
quarantine_ref
publication_blockers
source_tracking_blockers
security_refs
validation_refs
evidence_refs
incident_refs
deletion_or_removal_triggers
review_required
limitations
```

RetentionRecord defines metadata posture only.

RetentionRecord does not create storage.

RetentionRecord does not approve persistence.

RetentionRecord does not approve generated output tracking.

RetentionRecord does not approve source tracking.

## RedactionRecord Contract
Required RedactionRecord fields:

```text
redaction_record_id
target_ref
target_type
redaction_reason
redaction_scope
redaction_method
redaction_required
redaction_completed_status
secret_related
credential_related
product_related
external_related
generated_output_related
local_only
security_refs
validation_refs
evidence_refs
blockers
limitations
review_required
```

Secrets and credentials must be omitted, not transformed, summarized, hashed, partially quoted, normalized, or copied.

Redaction metadata is not permission to inspect the sensitive content.

Redaction records must preserve safe metadata only.

## QuarantineRecord Contract
Required QuarantineRecord fields:

```text
quarantine_record_id
quarantined_ref
quarantined_object_type
quarantine_trigger
quarantine_reason
detected_sensitivity
detected_source_classification
local_only
generated_output_related
product_related
provider_auth_related
credential_related
secret_related
graphify_related
impacted_lanes
impacted_surfaces
required_owner
required_security_review
required_validation_review
required_governance_review
removal_or_release_route
publication_blockers
source_tracking_blockers
incident_ref
rollback_ref
limitations
review_required
```

QuarantineRecord does not move files.

QuarantineRecord does not delete files.

QuarantineRecord does not inspect forbidden content.

QuarantineRecord records the governance route for future handling.

## RollbackRecord Contract
Required RollbackRecord fields:

```text
rollback_record_id
rollback_trigger
rollback_reason
rollback_owner
impacted_lanes
impacted_surfaces
impacted_records
impacted_outputs
activation_status
execution_status
provider_auth_posture
product_posture
generated_output_posture
tracking_posture
required_stop_action
required_quarantine_route
required_removal_route
required_deactivation_route
required_credential_rotation_route
required_evidence_retention
required_governance_review
required_security_review
required_validation_review
incident_refs
audit_refs
limitations
review_required
```

RollbackRecord defines future rollback expectations only.

RollbackRecord does not implement rollback automation.

RollbackRecord does not execute rollback.

RollbackRecord does not approve destructive action.

RollbackRecord does not approve credential rotation, unless a future security process authorizes it.

## IncidentRecord Contract
Required IncidentRecord fields:

```text
incident_record_id
incident_type
incident_trigger
incident_summary_metadata
detected_lane
detected_target_ref
detected_source_classification
detected_sensitivity
secret_related
credential_related
product_related
provider_auth_related
tool_execution_related
agent_output_related
graphify_output_related
generated_output_related
local_only
impacted_lanes
impacted_surfaces
audit_refs
evidence_refs
validation_refs
security_refs
quarantine_ref
rollback_ref
publication_blockers
source_tracking_blockers
required_owner
required_review_route
required_follow_up
limitations
```

IncidentRecord contains safe metadata only.

IncidentRecord must not quote, summarize, transform, or copy forbidden content.

IncidentRecord does not implement incident automation.

IncidentRecord does not approve publication.

## PublicationBlocker Contract
Required PublicationBlocker fields:

```text
publication_blocker_id
blocked_ref
blocked_object_type
blocker_type
blocker_reason
source_classification
sensitivity
local_only
generated_output_related
product_related
external_related
provider_auth_related
credential_related
secret_related
graphify_related
tracking_posture
required_gate
required_security_review
required_validation_review
required_governance_review
clearance_requirement
limitations
```

Required PublicationBlocker types:

```text
local_only_publication_blocker
generated_output_publication_blocker
raw_graphify_output_publication_blocker
product_source_publication_blocker
external_source_publication_blocker
provider_auth_publication_blocker
credential_publication_blocker
secret_publication_blocker
unknown_sensitivity_publication_blocker
validation_missing_publication_blocker
security_missing_publication_blocker
source_tracking_publication_blocker
governance_approval_missing_blocker
```

## SourceTrackingBlocker Contract
Required SourceTrackingBlocker fields:

```text
source_tracking_blocker_id
blocked_ref
blocked_object_type
blocker_type
blocker_reason
source_classification
sensitivity
local_only
generated_output_related
product_related
external_related
provider_auth_related
credential_related
secret_related
graphify_related
required_gate
required_security_review
required_validation_review
required_governance_review
clearance_requirement
limitations
```

Required SourceTrackingBlocker types:

```text
source_tracking_not_approved
generated_output_tracking_not_approved
local_only_tracking_blocked
product_source_tracking_blocked
external_source_tracking_blocked
raw_graphify_output_tracking_blocked
secret_tracking_blocked
credential_tracking_blocked
provider_auth_tracking_blocked
unknown_sensitivity_tracking_blocked
publication_not_approved
git_mutation_not_approved
```

## GeneratedOutputHandlingRecord Contract
Required GeneratedOutputHandlingRecord fields:

```text
generated_output_record_id
generated_output_ref
generated_output_type
generator_ref
generation_context_ref
generated_output_posture
local_only
source_classification
sensitivity
authority_posture
evidence_posture
validation_refs
security_refs
evidence_refs
retention_ref
redaction_ref
quarantine_ref
publication_blockers
source_tracking_blockers
promotion_requirement
deletion_or_removal_triggers
review_required
limitations
```

Generated outputs are not authority by default.

Generated outputs are local-only unless explicitly curated, validated, security-reviewed, and governed for exact scope.

Generated output retention metadata is not generated output tracking approval.

Generated output evidence posture is not truth.

## LocalOnlyRetentionRecord Contract
Required LocalOnlyRetentionRecord fields:

```text
local_only_retention_record_id
local_only_ref
local_only_type
lane_ref
source_classification
sensitivity
retention_reason
retention_posture
allowed_metadata_use
forbidden_use
redaction_requirement
quarantine_requirement
publication_blockers
source_tracking_blockers
security_refs
validation_refs
evidence_refs
review_required
limitations
```

Local-only material remains blocked from publication and tracking unless future governance explicitly approves exact scope.

Local-only metadata may reference existence or posture only.

Local-only retention does not approve raw content inclusion.

## SecretCredentialIncidentRecord Contract
Required SecretCredentialIncidentRecord fields:

```text
secret_credential_incident_record_id
incident_ref
detected_ref
detected_type
secret_related
credential_related
provider_auth_related
safe_summary_metadata
forbidden_content_handling
required_stop_action
required_redaction_route
required_quarantine_route
required_security_review
required_governance_review
credential_rotation_route
publication_blockers
source_tracking_blockers
rollback_ref
limitations
```

Do not inspect, quote, summarize, transform, hash, normalize, partially copy, or validate secret or credential values.

If secret or credential material is suspected, STOP handling the content and report safe metadata only.

## ProductSourceIncidentRecord Contract
Required ProductSourceIncidentRecord fields:

```text
product_source_incident_record_id
incident_ref
detected_product_ref
product_scope
product_posture
source_classification
sensitivity
safe_summary_metadata
required_stop_action
required_quarantine_route
required_security_review
required_validation_review
required_governance_review
required_source_tracking_review
rollback_ref
publication_blockers
source_tracking_blockers
limitations
```

Product source cannot be loaded, inspected, retained, published, or tracked by P2.3.

Product-source incident metadata records posture and route only.

Siamese is product vision, not product activation.

## ProviderAuthIncidentRecord Contract
Required ProviderAuthIncidentRecord fields:

```text
provider_auth_incident_record_id
incident_ref
provider_ref
auth_material_ref
provider_auth_posture
credential_related
secret_related
safe_summary_metadata
required_stop_action
required_quarantine_route
required_security_review
required_governance_review
credential_rotation_route
provider_deactivation_route
publication_blockers
source_tracking_blockers
rollback_ref
limitations
```

Provider/auth material must never be retained as content.

Provider/auth incident handling does not configure provider/auth.

Provider metadata is not provider activation.

## ToolExecutionIncidentRecord Contract
Required ToolExecutionIncidentRecord fields:

```text
tool_execution_incident_record_id
incident_ref
tool_ref
tool_request_ref
tool_decision_ref
execution_status
execution_surface
side_effect_profile
source_classification
sensitivity
generated_output_posture
safe_summary_metadata
required_stop_action
required_quarantine_route
required_security_review
required_validation_review
required_governance_review
rollback_ref
publication_blockers
source_tracking_blockers
limitations
```

Tool execution incident metadata does not approve tool execution.

Tool metadata is not tool execution.

No shell, subprocess, filesystem, network, package manager, build, test, CI, Git, MCP, provider/auth, or tool execution is approved by P2.3.

## AgentOutputIncidentRecord Contract
Required AgentOutputIncidentRecord fields:

```text
agent_output_incident_record_id
incident_ref
agent_ref
task_ref
handoff_ref
agent_output_ref
execution_status
source_classification
sensitivity
generated_output_posture
product_related
provider_auth_related
tool_related
safe_summary_metadata
required_stop_action
required_quarantine_route
required_security_review
required_validation_review
required_governance_review
rollback_ref
publication_blockers
source_tracking_blockers
limitations
```

Agent output incident metadata does not approve agent execution.

Agent metadata is not agent execution.

Agent output remains generated evidence until reviewed, validated, security-constrained, and governed.

## GraphifyOutputHandlingRecord Contract
Required GraphifyOutputHandlingRecord fields:

```text
graphify_output_handling_record_id
graphify_ref
graphify_output_type
graphify_output_posture
curated_summary_available
raw_output_related
generated_output_posture
local_only
authority_posture
evidence_posture
validation_refs
security_refs
evidence_refs
retention_ref
quarantine_ref
publication_blockers
source_tracking_blockers
review_required
limitations
```

Graphify repo map summary is curated generated evidence only.

Raw Graphify output under `9_artifacts/` is local-only.

Graphify evidence is supporting evidence only, not authority.

Graphify labels are not governance labels.

Graphify output handling is not Graphify rerun, adoption, authority, or substrate selection.

## Retained Evidence Classes
| evidence class | examples | allowed AL-1 retention | blocked retention | publication posture | tracking posture | required review |
| --- | --- | --- | --- | --- | --- | --- |
| governance_metadata | P0/P1/P2 governance docs, gate records. | Safe metadata and scoped citations. | Treating accepted status as activation. | Future publication gate required. | Exact-path only after approval. | Governance review. |
| implementation_metadata | I-series architecture records. | Metadata-only component posture. | Live source, runtime code, implementation execution. | Publication-gated. | Exact-path only after approval. | Governance/security review. |
| validation_record_metadata | Validation posture refs, proof targets. | Metadata refs and limitations. | Validation command output as authority. | Requires GT-04 posture and review. | Exact future tracking only. | Validation/governance review. |
| security_record_metadata | Security refs, blocked actions, sensitivity. | Safe metadata and blockers. | Secrets, credentials, raw incident content. | Security review required. | Security and governance review. | Security/governance review. |
| evidence_ref_metadata | Cross-lane evidence refs. | Safe refs, scope, limitations. | Raw local-only or secret-bearing evidence. | Review required. | pending_P2.2_alignment. | Evidence contract review. |
| generated_summary | Curated or generated summaries. | Generated evidence with limitations. | Authority by default, secrets, product source. | Security/validation/governance required. | GT-12 if tracked. | Security/validation review. |
| generated_raw_output | Raw reports, logs, artifacts. | Local-only metadata only. | Raw content retention by default. | Blocked. | Blocked. | Security/governance review. |
| local_only_material | `9_artifacts/`, logs, outputs, local-only refs. | Safe metadata only. | Content copy, context inclusion, publication. | Blocked. | Blocked. | Security/governance review. |
| product_related_metadata | Product gate/readiness metadata. | Safe metadata and blockers. | Product source content. | Product/security/governance required. | GT-09/GT-12 required. | Product/security review. |
| product_source | Siamese product source. | None by P2.3. | Inspection, summary, retention, publication, tracking. | Blocked. | Blocked. | GT-09 future review. |
| external_source | Raw external source. | Metadata only when scoped. | Raw content, instructions, execution output. | Blocked unless future gated. | Blocked unless future gated. | GT-11/security/license review. |
| provider_auth_metadata | Auth requirement categories, credential refs. | Safe metadata only. | Auth material, tokens, keys, configs. | Blocked. | Blocked. | GT-08/security review. |
| credential_reference | Redacted credential requirement. | Metadata marker with blockers. | Values, hashes, prefixes, suffixes, tests. | Blocked. | Blocked. | Secure review. |
| secret_value | API key, token, password, private key. | None. | Any content retention. | Never publish. | Never track. | Secure incident route. |
| tool_output_metadata | Tool result refs and classifications. | Metadata only; generated evidence posture. | Raw tool output with forbidden content. | Blocked until reviewed. | Blocked unless future gated. | Security/validation/governance review. |
| agent_output_metadata | Agent output refs and classifications. | Metadata only; generated evidence posture. | Raw forbidden output or authority claim. | Blocked until reviewed. | Blocked unless future gated. | Security/validation/governance review. |
| graphify_curated_summary | Graphify Repo Map Summary. | Curated generated evidence with limitations. | Authority or substrate inference. | Publication-gated. | Exact-path only after governance. | Governance/security review. |
| graphify_raw_output | Raw Graphify output under `9_artifacts/`. | Local-only metadata only. | Raw output inclusion, publication, tracking. | Blocked. | Blocked. | Future Graphify/output review. |
| semantic_record_metadata | Cognitive Semantic System metadata records. | Metadata refs, blockers, limitations. | Truth by default, substrate selection, persistence. | Publication-gated. | Exact future tracking only. | Governance/validation/security review. |
| unknown_sensitivity | Unclassified/mixed material. | Blocked metadata marker only. | Retention as safe, publication, tracking. | Blocked. | Blocked. | Classification/security review. |

Safe metadata may be retained when scoped and ticket-approved.

Raw generated output is local-only by default.

Raw Graphify output is local-only by default.

Product source is blocked.

External source is blocked unless future scoped governance approves.

Secrets and credentials are never retained as content.

Unknown sensitivity blocks retention, publication, and tracking until classified.

## Generated Output Retention Baseline
Generated outputs are generated evidence, not authority.

Generated summaries remain generated evidence until reviewed.

Raw generated outputs remain local-only unless future governance approves exact scope.

Generated output retention does not approve generated output tracking.

Generated output tracking requires future source tracking / generated output tracking governance.

Generated output publication requires security review, validation posture, governance approval, and exact-scope clearance.

Generated outputs suspected to include secrets, credentials, product source, local-only material, external raw source, raw Graphify output, or unknown sensitivity must be quarantined by metadata route.

## Local-Only Retention Baseline
Local-only material may be represented by metadata refs.

Local-only content must not be copied into audit records, evidence records, incident records, summaries, generated outputs, or publication surfaces.

Local-only metadata must preserve blockers.

Local-only retention does not approve publication.

Local-only retention does not approve source tracking.

Local-only material must be treated as blocked until future exact-scope governance approves handling.

## Redaction Baseline
Redaction means preventing forbidden content from being retained, quoted, summarized, transformed, copied, normalized, partially disclosed, or published.

Secrets and credentials must be omitted, not transformed.

Product source must not be summarized as a substitute for inspection approval.

Raw Graphify output must not be transformed into authority.

Generated output with unknown sensitivity must not be published.

Redaction records must preserve safe metadata, blockers, refs, and limitations only.

## Quarantine / Removal Baseline
Quarantine is a governance metadata route, not automatic file movement.

Removal is a future governed action, not P2.3 execution.

Quarantine triggers include suspected secret, credential, provider/auth material, product source, raw external source, raw generated output, raw Graphify output, unknown sensitivity, unauthorized tool output, unauthorized agent output, publication blocker breach, source tracking blocker breach, or generated-output tracking breach.

Quarantine records must identify owner, impacted surfaces, review route, publication blockers, source tracking blockers, incident refs, rollback refs, and limitations.

## Rollback Baseline
Rollback baseline defines future response expectations only.

Rollback baseline does not execute rollback.

Rollback baseline does not mutate files.

Rollback baseline does not deactivate runtime.

Rollback baseline does not rotate credentials.

Rollback baseline does not remove generated outputs.

Rollback baseline must define:

```text
rollback owner
rollback trigger
rollback reason
impacted lanes
impacted surfaces
impacted records
impacted outputs
required stop action
required quarantine route
required removal route
required deactivation route
required credential rotation route when applicable
required evidence retention
required governance review
required security review
required validation review
limitations
```

Rollback triggers include:

```text
forbidden source inclusion
secret or credential exposure
provider/auth exposure
product-source exposure
unauthorized tool execution
unauthorized agent execution
unauthorized provider/API/MCP call
unauthorized generated output tracking
unauthorized source tracking expansion
unauthorized publication
Graphify raw output misuse
Cognitive Semantic System substrate violation
unknown sensitivity escalation
```

## Incident Handling Baseline
| incident type | safe metadata to record | forbidden content to avoid | stop condition | quarantine route | rollback route | security review requirement | validation review requirement | governance review requirement | publication blockers | source tracking blockers | follow-up ticket requirement | limitations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| secret/credential incident | Safe path/ref/category, suspected type, affected lane, blockers. | Values, partials, hashes, fingerprints, summaries, tests. | Stop content handling immediately. | SecretCredentialIncidentRecord. | RollbackRecord with rotation route as future security process. | Required. | No value validation; metadata only. | Required. | Secret and credential blockers. | Secret and credential tracking blockers. | Secure incident ticket. | Safe metadata only. |
| product-source incident | Product ref/category, product scope, safe posture. | Product source content or summary. | Stop source handling. | ProductSourceIncidentRecord. | RollbackRecord with product review route. | Required. | Required only after GT-09 scope. | Required. | Product source blocker. | Product source tracking blocker. | Product gate or incident ticket. | Siamese remains inactive. |
| provider/auth incident | Provider/auth category, credential-related flags. | Tokens, keys, configs, sessions, endpoints with auth. | Stop auth/provider handling. | ProviderAuthIncidentRecord. | RollbackRecord with future deactivation/rotation route. | Required. | Metadata-only. | Required. | Provider/auth blocker. | Provider/auth tracking blocker. | Provider/auth security ticket. | No provider configured. |
| tool execution incident | Tool/ref/action category, execution status, safe side-effect category. | Raw forbidden output, commands as approved follow-ups, secrets. | Stop execution chain. | ToolExecutionIncidentRecord. | RollbackRecord with exact future action route. | Required. | Required before evidence acceptance. | Required. | Tool output/generated blockers. | Tool output tracking blockers. | Tool incident/readiness ticket. | Does not approve tools. |
| agent output incident | Agent/task/output refs, generated posture, safe category. | Raw forbidden output, secrets, product source. | Stop publication/context use. | AgentOutputIncidentRecord. | RollbackRecord with handoff/output route. | Required. | Required before evidence acceptance. | Required. | Agent output blockers. | Agent output tracking blockers. | Agent output incident ticket. | Does not execute agents. |
| Graphify output incident | Graphify ref, raw/curated classification, generated posture. | Raw Graphify output, labels as authority. | Stop inclusion/tracking/publication. | GraphifyOutputHandlingRecord and QuarantineRecord. | RollbackRecord with output-handling route. | Required. | Required for evidence use. | Required. | Raw Graphify blocker. | Raw Graphify tracking blocker. | Graphify evidence handling ticket. | No rerun/adoption. |
| generated output incident | Output ref/type, generator, sensitivity flags. | Raw sensitive output, source dumps, secrets. | Stop retention/publication/tracking. | GeneratedOutputHandlingRecord and QuarantineRecord. | RollbackRecord with deletion/removal review route. | Required. | Required before evidence acceptance. | Required. | Generated output blocker. | Generated output tracking blocker. | Output handling ticket. | Local-only by default. |
| local-only incident | Local-only ref/category and safe posture. | Local-only content. | Stop content copying/inclusion. | LocalOnlyRetentionRecord and QuarantineRecord. | RollbackRecord with future removal review. | Required. | Metadata-only unless future scope. | Required. | Local-only blocker. | Local-only tracking blocker. | Local-only handling ticket. | Safe metadata only. |
| publication incident | Published/ref category, safe exposure class. | Forbidden content values. | Stop further publication. | QuarantineRecord. | RollbackRecord with publication response route. | Required. | Required for evidence correction. | Required. | All applicable blockers. | Source tracking blockers if coupled. | Publication incident ticket. | No publication by P2.3. |
| source tracking incident | Ref/path category, tracking posture, safe status. | Secrets, local-only content, raw output. | Stop Git/source tracking actions. | QuarantineRecord. | RollbackRecord with future Git/security route. | Required. | Required if evidence affected. | Required. | Publication blocker if tracked. | Source tracking not approved. | Source tracking incident ticket. | No Git mutation by P2.3. |
| unknown sensitivity incident | Unknown ref/category and affected lane. | Treating unknown as safe content. | Stop inclusion/retention/publication/tracking. | QuarantineRecord. | RollbackRecord if already propagated. | Required. | Future classification validation only. | Required. | Unknown sensitivity blocker. | Unknown sensitivity tracking blocker. | Classification ticket. | Unknown blocks progress. |

## Publication Blockers
Publication blockers apply to:

```text
secret values
credential values
provider/auth material
product source
external raw source
local-only material
raw generated output
raw Graphify output
unknown sensitivity
unreviewed generated evidence
unvalidated claims
missing security refs
missing validation refs
missing governance approval
source tracking not approved
runtime activation not approved
provider/auth not approved
tool execution not approved
agent execution not approved
Cognitive Semantic System substrate not selected
```

Publication blocker metadata does not approve publication.

Publication requires future exact-scope governance.

## Source Tracking Blockers
Source tracking blockers apply to:

```text
source tracking not approved
local-only tracking blocked
product source tracking blocked
external source tracking blocked
raw Graphify output tracking blocked
secret tracking blocked
credential tracking blocked
provider/auth tracking blocked
unknown sensitivity tracking blocked
publication not approved
Git mutation not approved
```

Source tracking blocker metadata does not approve source tracking.

Generated output tracking remains blocked unless future governance approves exact scope.

Git mutation remains blocked unless explicitly approved by human review for exact paths.

## Cross-Lane Interface Rules
### Audit / Context Interface
Context packs may reference audit metadata.

Context inclusion is not permission.

Context source refs are metadata.

Context records must preserve retention, redaction, quarantine, rollback, publication blockers, source tracking blockers, evidence refs, validation refs, security refs, sensitivity, local-only flags, generated-output flags, product flags, external flags, credential flags, secret flags, and limitations.

### Audit / Provider Interface
Provider metadata may reference audit and incident metadata.

Provider metadata is not provider activation.

Provider/auth material must not enter audit or incident content.

Provider/auth incidents require safe metadata only and security review.

### Audit / Tool Interface
Tool metadata may reference audit, retention, rollback, and incident metadata.

Tool metadata is not tool execution.

Tool output is generated evidence by default.

Tool execution incidents require stop, quarantine, security review, validation review, governance review, rollback route, publication blockers, and source tracking blockers.

### Audit / Agent Interface
Agent metadata may reference audit, retention, rollback, and incident metadata.

Agent metadata is not agent execution.

Agent output remains generated evidence by default.

Agent output incidents require safe metadata only, quarantine route, rollback route, and review.

### Audit / Cognitive Semantic System Interface
Cognitive Semantic System records may reference audit, retention, rollback, and incident metadata as evidence support.

Cognitive Semantic System records are not truth by default.

Cognitive Semantic System substrate remains deferred.

Semantic records derived from audit or incident metadata must preserve evidence refs, validation refs, security refs, blockers, retention posture, and limitations.

### Audit / Graphify Interface
Graphify repo map summary is curated generated evidence only.

Raw Graphify output is local-only.

Graphify output handling must preserve generated-output posture, local-only posture, publication blockers, source tracking blockers, retention posture, and limitations.

Graphify evidence cannot become authority through audit inclusion.

### Audit / Siamese Product Interface
Siamese is product vision, not product activation.

Product source remains blocked.

Product-source incident metadata must record safe metadata only.

Product-related audit metadata must preserve product posture, source tracking blockers, publication blockers, rollback route, and security review requirement.

## Cross-Lane Drift Register
| drift_id | source_lane | observed_term | canonical_or_proposed_term | status | reason | pending_dependency | impact | resolution_route |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ARR-DRIFT-001 | Context / Provider / Tool / Agent / Cognitive Semantic System | `retention_posture`, `retention_class`, `retention_requirements` | `retention_posture` | pending | Multiple P1 contracts use related retention terms. | pending_P2.1_alignment | Schema drift risk. | P2.1 vocabulary alignment. |
| ARR-DRIFT-002 | Context / Tool / Agent / Cognitive Semantic System | `publication_blocker`, `publication_blockers`, `publication posture` | `PublicationBlocker` plus `publication_posture` | pending | Blocker object and posture field need vocabulary split. | pending_P2.1_alignment | Publication gating ambiguity. | P2.1 vocabulary alignment. |
| ARR-DRIFT-003 | Context / Provider / Tool / Agent / Cognitive Semantic System | `evidence_refs`, `EvidenceRef`, lane-specific evidence refs | `EvidenceRef` relationship model | pending | Evidence refs are lane-local until P2.2 exists. | pending_P2.2_alignment | Evidence lineage ambiguity. | P2.2 evidence-reference contract. |
| ARR-DRIFT-004 | Context / Provider / Tool / Agent / Cognitive Semantic System | `validation_refs`, lane-specific validation refs | `ValidationRef` relationship model | pending | Validation refs need cross-lane evidence relationship. | pending_P2.2_alignment | Proof/evidence coupling ambiguity. | P2.2 evidence-reference contract. |
| ARR-DRIFT-005 | Context / Provider / Tool / Agent / Cognitive Semantic System | `security_refs`, lane-specific security refs | `SecurityRef` relationship model | pending | Security refs need shared blocker propagation semantics. | pending_P2.2_alignment | Security blocker propagation risk. | P2.2 and P2.1 alignment. |
| ARR-DRIFT-006 | Tool / Agent | `generated_output_related`, `generated_output_posture`, `output_classification` | `generated_output_posture` plus source flags | pending | Generated output terms overlap with output class. | pending_P2.1_alignment | Output handling drift. | P2.1 vocabulary alignment. |
| ARR-DRIFT-007 | Provider / Tool / Agent | `incident_requirement`, `incident_route`, `incident_refs` | `IncidentRecord` plus `incident_ref` | pending | P1 records name incident paths differently. | pending_P2.1_alignment | Incident routing ambiguity. | P2.1 vocabulary alignment. |
| ARR-DRIFT-008 | Cognitive Semantic System / Graphify | `Graphify evidence`, `curated Graphify summary`, `raw Graphify output` | `graphify_curated_summary` and `graphify_raw_output` | proposed | Separates curated summary from raw local-only output. | pending_P2.1_alignment | Prevents authority confusion. | P2.1 vocabulary alignment. |

P2.3 may propose terms but must not override P2.1 or P2.2.

## Baseline Invariants
| ID | Invariant |
| --- | --- |
| ARR-001 | P2.3 is audit / retention / rollback baseline only. |
| ARR-002 | P2.3 does not implement runtime logging. |
| ARR-003 | P2.3 does not implement persistence. |
| ARR-004 | P2.3 does not implement telemetry. |
| ARR-005 | P2.3 does not implement rollback automation. |
| ARR-006 | Audit metadata is not runtime logging. |
| ARR-007 | Retention posture is not persistence approval. |
| ARR-008 | Rollback baseline is not rollback execution. |
| ARR-009 | Incident handling baseline is not incident automation. |
| ARR-010 | Evidence supports review; evidence does not decide. |
| ARR-011 | Validation evaluates; governance decides. |
| ARR-012 | Security constrains. |
| ARR-013 | Generated outputs are not authority by default. |
| ARR-014 | Raw generated outputs remain local-only unless future governance approves exact scope. |
| ARR-015 | Raw Graphify output remains local-only. |
| ARR-016 | Graphify evidence is supporting generated evidence only, not authority. |
| ARR-017 | Secrets and credentials are never retained as content. |
| ARR-018 | Product source remains blocked until future exact-scope governance. |
| ARR-019 | Provider/auth material must not enter audit or incident content. |
| ARR-020 | Tool execution incident metadata does not approve tool execution. |
| ARR-021 | Agent output incident metadata does not approve agent execution. |
| ARR-022 | Publication blockers do not approve publication. |
| ARR-023 | Source tracking blockers do not approve source tracking. |
| ARR-024 | Cognitive Semantic System substrate remains deferred. |
| ARR-025 | AGENT PLATFORM remains pre-active at AL-1. |

## Future Validation Targets
These are future validation targets only. P2.3 does not execute validation.

```text
audit event required fields completeness
retention record required fields completeness
redaction record required fields completeness
quarantine record required fields completeness
rollback record required fields completeness
incident record required fields completeness
publication blocker completeness
source tracking blocker completeness
generated output retention posture propagation
local-only retention posture propagation
secret/credential incident invariant
product-source incident invariant
provider/auth incident invariant
tool execution incident invariant
agent output incident invariant
Graphify raw output local-only invariant
evidence refs preserved across audit records
validation refs preserved across audit records
security refs preserved across audit records
P2.1 vocabulary alignment completeness
P2.2 evidence reference alignment completeness
no runtime logging implementation invariant
no persistence implementation invariant
no rollback automation invariant
```

## Future Hardening Candidates
These are future tickets only and are not started by P2.3.

```text
ARR-HARD-01 — Audit Event Schema Alignment
ARR-HARD-02 — Retention Posture Propagation Model
ARR-HARD-03 — Redaction / Quarantine Contract Alignment
ARR-HARD-04 — Rollback Record Contract Alignment
ARR-HARD-05 — Incident Metadata Contract Alignment
ARR-HARD-06 — Publication Blocker Contract Alignment
ARR-HARD-07 — Source Tracking Blocker Contract Alignment
ARR-HARD-08 — Generated Output Handling Contract Alignment
ARR-HARD-09 — Local-Only Retention Contract Alignment
```

## Created / Not Created Register
| Register item | P2.3 status |
| --- | --- |
| audit / retention / rollback baseline document created | Created at `0_architecture/governance/agent_platform_audit_retention_rollback_baseline.md`. |
| no runtime logging implemented | Confirmed. |
| no persistence implemented | Confirmed. |
| no telemetry implemented | Confirmed. |
| no rollback automation implemented | Confirmed. |
| no incident automation implemented | Confirmed. |
| no context runtime code modified | Confirmed. |
| no provider adapter code modified | Confirmed. |
| no tool execution code modified | Confirmed. |
| no agent runtime code modified | Confirmed. |
| no Cognitive Semantic System code modified | Confirmed. |
| no validation implementation modified | Confirmed. |
| no security implementation modified | Confirmed. |
| no validation command executed | Confirmed. |
| no tests executed | Confirmed. |
| no provider/auth configured | Confirmed. |
| no tool execution approved | Confirmed. |
| no agent execution approved | Confirmed. |
| no source loading approved | Confirmed. |
| no product source inspected | Confirmed. |
| no external source inspected | Confirmed. |
| no secrets inspected | Confirmed. |
| no credentials inspected | Confirmed. |
| no Graphify rerun | Confirmed. |
| no Graphify adoption approved | Confirmed. |
| no generated outputs modified/tracked | Confirmed. |
| no source tracking expansion approved | Confirmed. |
| no publication approved | Confirmed. |
| no .graphifyignore modified | Confirmed. |
| no .gitignore modified | Confirmed. |
| no Cognitive Semantic System substrate selected | Confirmed. |
| no P2.1 created or modified | Confirmed. |
| no P2.2 created or modified | Confirmed. |
| no P3.1 started | Confirmed. |
| no P3.2 started | Confirmed. |

## Recommended Next Tickets
After P2.3:

```text
P2.1 — Shared Metadata Vocabulary Alignment, if not already completed
P2.2 — Cross-Lane Evidence Reference Contract, if not already completed
P3.1 — Validation Execution Readiness, after P2.1/P2.2/P2.3 alignment is reconciled
P3.2 — Security Enforcement Readiness, after P2.1/P2.2/P2.3 alignment is reconciled
```

Recommended actual if P2.1 or P2.2 are not complete:

```text
P2.1 — Shared Metadata Vocabulary Alignment
```

or:

```text
P2.2 — Cross-Lane Evidence Reference Contract
```

Recommended actual after P2.1, P2.2, and P2.3 are complete and reconciled:

```text
P3.1 — Validation Execution Readiness
```

Do not recommend tool execution, provider/auth activation, agent runtime activation, product activation, Graphify adoption, source tracking expansion, or Cognitive Semantic System substrate selection.

## Final Verdict
| Question | Answer |
| --- | --- |
| What did P2.3 create? | The canonical Audit / Retention / Rollback Baseline document. |
| What audit baseline was defined? | AuditEventMetadata as cross-lane safe metadata for lane, ticket, actor, target, source, evidence, validation, security, Graphify, product, context, provider, tool, agent, semantic, classification, retention, publication, rollback, incident, blocker, limitation, and review posture. |
| What retention baseline was defined? | RetentionRecord, GeneratedOutputHandlingRecord, LocalOnlyRetentionRecord, and retained evidence classes that keep safe metadata only and block raw generated, local-only, product, external, secret, credential, provider/auth, and raw Graphify content by default. |
| What rollback baseline was defined? | RollbackRecord metadata for future rollback owner, trigger, reason, impacted lanes/surfaces/records/outputs, stop action, quarantine, removal, deactivation, credential rotation route, evidence retention, governance/security/validation review, and limitations. |
| What incident handling baseline was defined? | IncidentRecord plus specialized secret/credential, product-source, provider/auth, tool execution, agent output, Graphify output, generated output, local-only, publication, source tracking, and unknown sensitivity incident handling with safe metadata, stop, quarantine, rollback, review, blockers, follow-up, and limitations. |
| What publication blockers were defined? | Blockers for secrets, credentials, provider/auth material, product source, external raw source, local-only material, raw generated output, raw Graphify output, unknown sensitivity, unreviewed evidence, unvalidated claims, missing refs, missing governance, source/generated tracking gaps, and unapproved runtime/provider/tool/agent/Cognitive Semantic System posture. |
| What source tracking blockers were defined? | Source tracking not approved, generated output tracking not approved, local-only/product/external/raw Graphify/secret/credential/provider-auth/unknown tracking blocked, publication not approved, and Git mutation not approved. |
| What generated output handling posture was defined? | Generated outputs are generated evidence, not authority; raw outputs remain local-only unless future exact-scope governance curates, validates, security-reviews, and approves handling. |
| What local-only retention posture was defined? | Local-only material may be represented by metadata refs only; content must not be copied into records, summaries, outputs, context, publication, or tracking without future exact-scope governance. |
| What cross-lane interfaces were covered? | Audit/context, audit/provider, audit/tool, audit/agent, audit/Cognitive Semantic System, audit/Graphify, and audit/Siamese product interfaces. |
| Were runtime logging, persistence, telemetry, or rollback automation implemented? | No. |
| Was validation executed? | No. |
| Were tests executed? | No. |
| Was provider/auth configured? | No. |
| Were tools executed? | No. |
| Were agents executed? | No. |
| Was product source inspected? | No. |
| Was source loading approved? | No. |
| Was generated output tracking approved? | No. |
| Was source tracking expansion approved? | No. |
| Was Graphify rerun or adopted? | No. |
| Was Cognitive Semantic System substrate selected? | No. Cognitive Semantic System substrate remains deferred. |
| What dependencies remain pending with P2.1 or P2.2? | Vocabulary-dependent names remain `pending_P2.1_alignment`; evidence-reference relationships remain `pending_P2.2_alignment`. |
| What is the next ticket? | P2.1 - Shared Metadata Vocabulary Alignment if absent; P2.2 - Cross-Lane Evidence Reference Contract if P2.1 is complete and P2.2 remains absent; P3.1 only after P2.1/P2.2/P2.3 are complete and reconciled. |

Stop rule: After completing P2.3, STOP. Do not start P2.1. Do not start P2.2. Do not start P3.1. Do not start P3.2. Do not implement code. Do not implement runtime logging. Do not implement persistence. Do not implement telemetry. Do not implement rollback automation. Do not implement incident automation. Do not run validation. Do not run tests. Do not execute tools. Do not execute agents. Do not inspect secrets. Do not inspect credentials. Do not configure provider/auth. Do not load source. Do not inspect product source. Do not approve source tracking expansion. Do not approve generated output tracking. Do not approve publication. Do not approve tool execution. Do not approve provider/auth activation. Do not approve agent runtime activation. Do not rerun Graphify. Do not modify generated outputs. Do not modify `.graphifyignore`. Do not modify `.gitignore`. Do not stage, commit, push, force-add, or publish.
