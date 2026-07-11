# P8.8 - Hermes Interface / Runtime Candidate Boundary

## Purpose

This document defines the MVP-0 governance boundary for considering Hermes as an interface-pattern and runtime-candidate source without activating, importing, executing, configuring, adapting, or integrating Hermes.

Hermes may be referenced only as a conceptual candidate boundary for future review. This file does not approve Hermes runtime use, Hermes orchestration use, Hermes Cadence use, Hermes MCP/provider use, Hermes live connector use, Hermes API use, Hermes authentication use, or Hermes product adoption.

## Scope

In scope:

- Define Hermes conceptual candidate records for MVP-0 governance.
- Separate interface-pattern consideration from runtime activation.
- Separate UI inspiration from Hermes adoption.
- Preserve all Hermes runtime, orchestration, Cadence, adapter, provider, MCP, API, authentication, and live-connector paths as blocked.
- Record path-only posture for known Hermes source candidate locations without inspecting source contents.
- Record dependencies on P8.0, P8.1, and P8.5 as hard prerequisites.

Out of scope:

- Hermes runtime activation.
- Hermes source import.
- Hermes execution.
- Hermes configuration.
- Hermes adapter creation.
- Hermes UI implementation.
- Hermes MCP or provider activation.
- Hermes API or authentication wiring.
- Hermes Cadence activation.
- Autonomous orchestration, dispatch, handoff, reviewer assignment, or live integration.
- Tests, CI, scripts, builds, package-manager actions, Python execution, or security enforcement implementation.
- Graphify rerun or adoption.
- GBrain, GStack, Codegraph, OpenCode, vector DB, embedding, graph DB, ontology runtime, telemetry, event stream, generated-output tracking, publication, or Git mutation.

## Prerequisite Posture

The following posture is path-only and does not represent content inspection.

| Reference | Path | Posture | Boundary effect |
| --- | --- | --- | --- |
| P8.0 | `0_architecture/governance/agent_platform_p8_platform_mvp_scope_external_integration_boundary.md` | present | Required hard prerequisite satisfied. |
| P8.1 | `0_architecture/governance/agent_platform_external_source_inventory_graphify_gbrain_gstack_hermes_opencode.md` | present | Required hard prerequisite satisfied. |
| P8.5 | `0_architecture/governance/agent_platform_p8_security_activation_gate_model.md` | present | Required hard prerequisite satisfied. |
| P8.2 | `0_architecture/governance/agent_platform_mvp_interaction_surface_architecture.md` | present | Interaction-surface alignment available. |
| P8.4 | `0_architecture/governance/agent_platform_local_workspace_state_model.md` | present | Local workspace-state alignment available. |
| P8.7 | `0_architecture/governance/agent_platform_gbrain_gstack_memory_compatibility_boundary.md` | absent | `pending_P8.7_gbrain_gstack_memory_boundary_alignment`. |
| P8.9 | `0_architecture/governance/agent_platform_opencode_harness_upgrade_boundary.md` | present | OpenCode harness upgrade boundary alignment available by path-only recheck. |
| P7.0.0 | `0_architecture/governance/agent_platform_agent_native_organization_research_carry_forward.md` | present | Agent-native carry-forward context available. |
| P7.0.E | `0_architecture/governance/agent_platform_manual_harness_opencode_hermes_boundary_strategy.md` | present | Harness and Hermes boundary context available. |
| P7.0.F legacy | `0_architecture/governance/agent_platform_manual_reviewer_approval_pipeline_contract.md` | absent | `pending_P7_legacy_reviewer_path_alignment`. |
| P7.0.F accepted | `0_architecture/governance/agent_platform_reviewer_mesh_immune_safeguards_contract.md` | present | Reviewer safeguard context available. |
| P7.0.G | `0_architecture/governance/agent_platform_manual_integrator_commit_advisory_protocol.md` | present | Integrator advisory context available. |
| P7.0.H | `0_architecture/governance/agent_platform_first_manual_agentic_workflow_pilot_playbook.md` | present | Pilot playbook context available. |

## Candidate Source Posture

The following posture is path-only. No Hermes, external, product, Siamese, generated, Graphify, GBrain, GStack, OpenCode, secret, credential, `.env`, raw output, or runtime content was inspected.

| Candidate path | Posture | Boundary classification |
| --- | --- | --- |
| `external/sources/hermes` | absent | No local Hermes candidate source available at this path. |
| `external/sources/Hermes` | absent | No local Hermes candidate source available at this path. |

If a Hermes candidate path appears in a later ticket, this document permits only path/class metadata until a prior gate explicitly permits narrower review. The allowed metadata tags are `interface_candidate`, `runtime_candidate`, `orchestration_candidate`, `cadence_candidate`, `not_activated`, `not_imported`, `not_executed`, `not_configured`, `not_dependency_approved`, `not_provider_auth_approved`, `not_MCP_active`, `not_Cadence_active`, `not_AGENT_PLATFORM_runtime`, `not_substrate`, and `content_not_inspected_unless_prior_gate_allows`.

## Boundary Decisions

| Decision | Status | Rationale |
| --- | --- | --- |
| `HermesInterfaceCandidate` | permitted as conceptual MVP-0 input only | Interface patterns may inform governance vocabulary, but do not create runtime adoption. |
| `HermesUICandidate` | permitted as UI inspiration only if evidence exists | UI ideas require evidence and remain non-adoptive. No UI implementation is approved here. |
| `HermesRuntimeCandidate` | blocked | Runtime use requires future gate approval and is not approved by this file. |
| `HermesOrchestrationCandidate` | blocked | Autonomous dispatch, handoff, reviewer assignment, and orchestration remain prohibited. |
| `HermesCadenceCandidate` | blocked | Cadence concepts remain non-active and cannot be treated as Cadence activation. |
| `HermesAdapterCandidate` | future-gated | Adapter work requires a later explicit ticket and security gate approval. |
| `HermesMCPOrProviderCandidate` | blocked | MCP, provider, authentication, and API paths remain inactive. |
| `HermesLiveConnectorCandidate` | blocked | Live network, credential, source, provider, or connector paths remain prohibited. |
| `HermesProductCandidate` | blocked | Product adoption is outside MVP-0 and requires later governance. |

## Required Objects

### HermesCandidateRecord

Defines the top-level governance record for any future Hermes reference.

Required fields:

- `candidate_id`: stable local identifier.
- `candidate_kind`: one of `interface_candidate`, `runtime_candidate`, `orchestration_candidate`, or `cadence_candidate`.
- `source_path_ref`: path-only reference when available.
- `source_content_review_status`: must remain `content_not_inspected_unless_prior_gate_allows` for MVP-0.
- `activation_status`: must remain `not_activated`.
- `import_status`: must remain `not_imported`.
- `execution_status`: must remain `not_executed`.
- `configuration_status`: must remain `not_configured`.
- `dependency_status`: must remain `not_dependency_approved`.
- `security_gate_ref`: reference to `HermesSecurityRef`.
- `boundary_decision_ref`: reference to `HermesBoundaryDecision`.

### HermesInterfaceCandidate

Defines conceptual interface-pattern consideration only.

Required constraints:

- Must not imply Hermes runtime activation.
- Must not imply Hermes source import.
- Must not imply Hermes UI implementation.
- Must not imply API, provider, MCP, authentication, or connector activation.
- Must reference P8.2 when translating conceptual interaction-surface language.

### HermesRuntimeCandidate

Defines a blocked runtime-candidate placeholder.

Required constraints:

- Must remain `not_AGENT_PLATFORM_runtime`.
- Must remain `not_substrate`.
- Must remain `not_activated`.
- Must not be executed, configured, installed, imported, wrapped, or invoked.
- Must not be used as an autonomous orchestration mechanism.

### HermesOrchestrationCandidate

Defines a blocked orchestration-candidate placeholder.

Required constraints:

- Must not dispatch work packets.
- Must not assign reviewers.
- Must not perform handoff.
- Must not merge or integrate output.
- Must not operate as an agent manager, planner, scheduler, or execution controller.

### HermesCadenceCandidate

Defines a blocked Cadence-candidate placeholder.

Required constraints:

- Must remain `not_Cadence_active`.
- Must not start, schedule, execute, or configure Cadence behavior.
- Must not be represented as a workflow engine for Agent Platform MVP-0.

### HermesUIFeasibilityRecord

Defines the evidence record required before any Hermes UI idea can be referenced as inspiration.

Required fields:

- `ui_feasibility_id`: stable local identifier.
- `evidence_ref`: reference to `HermesEvidenceRef`.
- `interaction_surface_ref`: reference to P8.2.
- `adoption_status`: must remain `not_adopted`.
- `implementation_status`: must remain `not_implemented`.
- `runtime_dependency_status`: must remain `not_dependency_approved`.

### HermesBoundaryDecision

Defines the explicit decision applied to a Hermes candidate.

Allowed values:

- `conceptual_interface_only`.
- `ui_inspiration_only_if_evidenced`.
- `runtime_blocked`.
- `orchestration_blocked`.
- `cadence_blocked`.
- `adapter_future_gated`.
- `mcp_provider_blocked`.
- `live_connector_blocked`.
- `product_adoption_blocked`.

### HermesActivationBlocker

Defines the blockers that prevent Hermes from becoming active in MVP-0.

Required blockers:

- `not_activated`.
- `not_imported`.
- `not_executed`.
- `not_configured`.
- `not_dependency_approved`.
- `not_provider_auth_approved`.
- `not_MCP_active`.
- `not_Cadence_active`.
- `not_AGENT_PLATFORM_runtime`.
- `not_substrate`.

### HermesEvidenceRef

Defines evidence references without reading or embedding source contents.

Required constraints:

- Must reference only governance files or path/class metadata unless a future gate permits content inspection.
- Must not include copied Hermes source content.
- Must not include raw Graphify output.
- Must not include secrets, credentials, `.env` values, or generated artifacts.
- Must preserve `content_not_inspected_unless_prior_gate_allows`.

### HermesValidationRef

Defines non-runtime validation posture.

Required constraints:

- Must not run tests, CI, scripts, builds, package-manager actions, Python, runtime commands, or source analysis.
- May record only path-existence checks and exact marker checks allowed by the ticket.
- Must not imply security enforcement implementation.

### HermesSecurityRef

Defines dependency on the P8.5 security activation gate.

Required constraints:

- Must keep all Hermes runtime paths blocked until an explicit future gate approves them.
- Must keep provider authentication blocked.
- Must keep MCP blocked.
- Must keep network and live connectors blocked.
- Must keep credentials and secrets uninspected.

### HermesRetentionRef

Defines retention posture for Hermes candidate metadata.

Required constraints:

- Retain only governance-level path metadata, candidate classification, and decision status.
- Do not retain source excerpts.
- Do not retain generated output excerpts.
- Do not retain credentials, secrets, tokens, or local environment values.

### HermesRollbackRef

Defines rollback posture for mistaken activation attempts.

Required constraints:

- Any Hermes activation attempt must be treated as invalid for MVP-0.
- Rollback advice is governance-only and does not run Git, scripts, runtime cleanup, or destructive commands.
- Human review is required before any future remediation action.

### HermesIncidentRef

Defines incident posture for boundary violations.

Required incident triggers:

- Hermes source content inspection without prior gate approval.
- Hermes runtime import, execution, configuration, installation, or wrapping.
- Hermes orchestration, dispatch, handoff, reviewer assignment, or autonomous control.
- Hermes Cadence activation or scheduling.
- Hermes MCP, provider, API, authentication, network, or live connector activation.
- Secret, credential, `.env`, generated-output, raw Graphify, product-source, or Siamese-source inspection.

## Core Invariants

- Hermes interface candidate is not Hermes runtime activation.
- Hermes UI inspiration is not Hermes adoption.
- Hermes runtime candidate is not autonomous orchestration.
- Hermes Cadence candidate is not Cadence activation.
- Hermes adapter discussion is not adapter approval.
- Hermes MCP/provider discussion is not MCP/provider activation.
- Hermes path existence is not source-content approval.
- Hermes source inventory is not source adoption.
- Hermes candidate metadata is not Agent Platform substrate selection.

## MVP-0 Usage Rule

For MVP-0, Hermes may appear only as a governed conceptual boundary in planning documents. Any future ticket that proposes Hermes source inspection, runtime activation, UI implementation, adapter work, API/provider/authentication work, MCP work, Cadence work, live connector work, orchestration work, or product adoption must first reference P8.0, P8.1, P8.5, and this file, then obtain a new explicit gate.

## Pending Alignment

- `pending_P8.7_gbrain_gstack_memory_boundary_alignment`: P8.7 was absent during this path-only posture check.
- `pending_P7_legacy_reviewer_path_alignment`: the legacy P7.0.F reviewer path was absent, while the accepted reviewer mesh safeguard path was present.

## Not Created

- No Hermes runtime implementation.
- No Hermes UI implementation.
- No Hermes adapter.
- No Hermes MCP or provider configuration.
- No Hermes authentication or API wiring.
- No Hermes Cadence configuration.
- No Hermes live connector.
- No autonomous orchestration layer.
- No tests, scripts, CI, builds, package-manager changes, Python execution, security enforcement, generated artifacts, source modifications, or Git mutations.
