# P8.9 - OpenCode Harness Upgrade Boundary

## Document Header
| Field | Value |
|---|---|
| Title | OpenCode Harness Upgrade Boundary |
| Ticket | P8.9 |
| Status | Accepted OpenCode harness upgrade boundary |
| Date | 2026-07-06 |
| Scope | Documentation-only OpenCode harness upgrade boundary for AGENT PLATFORM / Siamese MVP-0. |
| Authority | OpenCode harness upgrade boundary only, not OpenCode execution, executable adapter implementation, provider/auth/API/MCP activation, tool execution, agent execution, autonomous orchestration, automatic dispatch, automatic reviewer assignment, automatic integration, automatic task routing, source loading, source inspection, product source inspection, external source inspection, Graphify adoption/rerun, GBrain runtime, GStack runtime, Hermes runtime, Cadence, vector DB, embeddings, graph DB, ontology runtime, generated output tracking, source tracking expansion, publication, Git mutation, or Cognitive Semantic System substrate selection. |
| Related documents | P8.0, P8.1, P8.5, P8.2 if present, P8.3 if present, P8.4 if present, P8.6 if present, P8.7 if present, P8.8 if present, P7.R, P7.0.H, P7.0.A-P7.0.G, P7.0.0, P6.7, P6.1-P6.6, P5.R, P3.BR, P3.3, P3.4, P3.5, P3.R, P3.0, P3.1, P3.2, P2.KR, P2.1, P2.2, P2.3, P1.1, P1.2, P1.3, P1.4, P1.5, P0.1, P0.2, P0.3, S-03, S-04, CSS ADR/audit, Graphify Repo Map Summary, README, `.gitignore`, `.graphifyignore`. |
| Output | OpenCode harness upgrade boundary. |

## Purpose
P8 creates a Platform MVP / Interaction Layer.

P8.9 defines how OpenCode participates in MVP-0 without becoming internal runtime.

P8.9 formalizes OpenCode H0 current usage.

P8.9 defines H1 metadata-only adapter design boundary.

P8.9 evaluates H2 controlled execution adapter as future gated candidate only.

P8.9 blocks H2/H3 by default.

P8.9 defines how AGENT PLATFORM may generate HarnessInputPackage and prompt packages for manual OpenCode use.

P8.9 defines how AGENT PLATFORM may receive user-pasted OpenCode output.

P8.9 defines how OpenCode output should be treated as generated evidence until reviewed and integrated.

P8.9 supports the MVP-0 direction: AGENT PLATFORM local MVP captures user objective, generates WorkPacket / HarnessInputPackage, user manually copies package to OpenCode, user manually runs OpenCode, user pastes OpenCode output back into AGENT PLATFORM, AGENT PLATFORM structures HarnessOutputPackage, AGENT PLATFORM assists review checklist, AGENT PLATFORM assists integration checklist, AGENT PLATFORM renders exact-path CommitCandidate, and the user decides and executes Git manually.

P8.9 does not execute OpenCode.

P8.9 does not implement an OpenCode adapter.

P8.9 does not activate tools, providers, MCP, agents, runtime, or Git mutation.

## Current Posture
| Posture | Statement |
|---|---|
| P8.0 prerequisite | P8.0 must define MVP scope and external integration boundary before P8.9. P8.0 is present. |
| P8.1 prerequisite | P8.1 must inventory and classify OpenCode before P8.9. P8.1 is present. |
| P8.5 prerequisite | P8.5 must define security / activation gate levels before P8.9. P8.5 is present. |
| Round | P8.9 is a Round 2 external boundary ticket after P8.1 and P8.5. |
| Current OpenCode use | OpenCode current use is H0 user-operated external harness. |
| H0 | H0 remains allowed. |
| H1 | H1 metadata-only adapter design may be described but not implemented. |
| H2 | H2 controlled execution adapter remains blocked by default. |
| H3 | H3 autonomous orchestration adapter remains blocked. |
| Runtime adoption | Manual OpenCode usage is not internal runtime adoption. |
| Output posture | OpenCode output is generated evidence by default. |
| Git authority | The user remains final commit authority. |
| Git mutation | The agent never mutates Git. |

## Inputs Reviewed
| Input | Expected role | Present / missing | OpenCode-boundary use | Blocking consequence if missing |
|---|---|---|---|---|
| P8.0 Platform MVP Scope / External Integration Boundary | Required prerequisite. | Present. | Defines MVP scope and external integration boundary. | If missing, STOP with `missing_P8.0_platform_mvp_scope_external_integration_boundary`. |
| P8.1 External Source Inventory / Classification | Required prerequisite. | Present. | Defines OpenCode inventory/classification boundary. | If missing, STOP with `missing_P8.1_external_source_inventory_classification`. |
| P8.5 Security / Activation Gate Model | Required prerequisite. | Present. | Defines activation/security gates for H1/H2/H3. | If missing, STOP with `missing_P8.5_security_activation_gate_model`. |
| P8.2 MVP Interaction Surface Architecture, if present | Optional sibling. | Present. | Aligns future manual interaction surface. | None. |
| P8.3 Core Workflow Schema Candidates, if present | Optional sibling. | Present. | Aligns WorkPacket / HarnessInputPackage / HarnessOutputPackage naming. | None. |
| P8.4 Local Workspace / State Model, if present | Optional sibling. | Present. | Aligns output intake, review, integration, and CommitCandidate state. | None. |
| P8.6 Graphify Read-Only Evidence Boundary, if present | Optional sibling. | Missing. | Would align Graphify evidence boundaries. | `pending_P8.6_graphify_boundary_alignment`. |
| P8.7 GBrain / GStack Memory Compatibility Boundary, if present | Optional sibling. | Missing. | Would align memory/runtime candidate boundaries. | `pending_P8.7_gbrain_gstack_boundary_alignment`. |
| P8.8 Hermes Interface / Runtime Candidate Boundary, if present | Optional sibling. | Missing. | Would align Hermes runtime candidate boundary. | `pending_P8.8_hermes_boundary_alignment`. |
| P7.R Manual Agentic Workflow Planning Closure | Manual workflow closure. | Present. | Confirms manual workflow closure. | Manual workflow alignment incomplete if absent. |
| P7.0.H First Manual Agent-Native Pilot Playbook | Manual pilot baseline. | Present. | Manual harness pattern source. | Pilot alignment incomplete if absent. |
| P7.0.0 Agent-Native Organization Research Carry-Forward | Agent-native pattern set. | Present. | Confirms manual projection and harness boundary. | Agent-native alignment incomplete if absent. |
| P7.0.E Manual Harness / OpenCode-Hermes Boundary | Manual harness boundary. | Present. | Prior OpenCode/Hermes boundary. | Harness alignment incomplete if absent. |
| P7.0.F Reviewer Agent / Approval Pipeline Contract | Reviewer pipeline. | Missing. | Would align review checklist semantics. | Review boundary carries missing baseline limitation. |
| P7.0.G Integrator / Commit Advisory Protocol | Integrator / commit advisory. | Present. | CommitCandidate and Git advisory boundary. | Integrator alignment incomplete if absent. |
| P6.4 Human Approval / Review Loop Operational Contract | Approval boundary. | Present. | Human approval and no-self-approval posture. | Approval boundary incomplete if absent. |
| P6.5 Runtime Monitoring / Incident Handling Operational Contract | Incident boundary. | Present. | Incident refs and stop rules. | Incident alignment incomplete if absent. |
| P5.R Minimal Active Agent Platform Audit | Skeleton baseline. | Present. | Prevents runtime activation. | Runtime baseline incomplete if absent. |
| P3.BR Activation Decision Reconciliation Closure | Activation decision reconciliation. | Present. | Decision is not execution. | Activation-decision alignment incomplete if absent. |
| P3.3 Tool Execution Activation Decision | Tool boundary. | Present. | Blocks tool execution. | Tool boundary incomplete if absent. |
| P3.4 Provider/Auth/API/MCP Activation Decision | Provider/API/MCP boundary. | Present. | Blocks provider/auth/API/MCP activation. | Provider boundary incomplete if absent. |
| P3.5 Agent Runtime Activation Decision | Agent runtime boundary. | Present. | Blocks agent execution. | Agent boundary incomplete if absent. |
| P3.0 Controlled Source Classification Readiness | Source classification. | Present. | Package/source classification posture. | Source classification incomplete if absent. |
| P3.1 Validation Execution Readiness | Validation posture. | Present. | Validation boundary. | Validation posture incomplete if absent. |
| P3.2 Security Enforcement Readiness | Security posture. | Present. | Security blockers. | Security posture incomplete if absent. |
| P2.1 Shared Metadata Vocabulary Alignment | Vocabulary. | Present. | Object naming alignment. | Vocabulary alignment incomplete if absent. |
| P2.2 EvidenceRef Contract | Evidence semantics. | Present. | OpenCode output as generated evidence. | Evidence semantics incomplete if absent. |
| P2.3 Audit / Retention / Rollback Baseline | Lifecycle baseline. | Present. | Retention, rollback, incident posture. | Lifecycle posture incomplete if absent. |
| P1.3 Tool Execution Boundary Contract Hardening | Tool boundary. | Present. | Blocks OpenCode execution as tool. | Tool boundary incomplete if absent. |
| P1.2 Provider Adapter Metadata Contract Hardening | Provider boundary. | Present. | Blocks provider activation. | Provider boundary incomplete if absent. |
| P1.4 Agent Runtime Boundary Contract Hardening | Agent boundary. | Present. | Blocks agent runtime. | Agent boundary incomplete if absent. |
| P1.1 Context Runtime Contract Hardening | Context boundary. | Present. | Context refs are not source loading. | Context boundary incomplete if absent. |
| S-03 Tool / Shell / Network / MCP Execution Policy | Execution policy. | Present. | Blocks OpenCode/tool/network/MCP execution. | Policy alignment incomplete if absent. |
| S-04 Local-Only Secrets / Credentials Policy | Secrets/credentials policy. | Present. | Secrets and credentials excluded from packages. | Secret boundary incomplete if absent. |
| README | Repository posture. | Present. | Boundary context only. | Repository posture incomplete if absent. |
| `.gitignore` | Ignore boundary. | Present. | Ignored artifact posture only; not modified. | Ignore boundary incomplete if absent. |
| `.graphifyignore` | Graphify ignore boundary. | Present. | Generated evidence boundary only; not modified. | Graphify ignore boundary incomplete if absent. |

## Dependency Posture
If P8.0 is missing, STOP with `missing_P8.0_platform_mvp_scope_external_integration_boundary`.

If P8.1 is missing, STOP with `missing_P8.1_external_source_inventory_classification`.

If P8.5 is missing, STOP with `missing_P8.5_security_activation_gate_model`.

P8.2 is present.

P8.3 is present.

P8.4 is present.

P8.6 is missing, so P8.9 records `pending_P8.6_graphify_boundary_alignment`.

P8.7 is missing, so P8.9 records `pending_P8.7_gbrain_gstack_boundary_alignment`.

P8.8 is missing, so P8.9 records `pending_P8.8_hermes_boundary_alignment`.

P8.9 must not synthesize missing sibling documents.

P8.9 must not create P8.10.

## Harness Level Model
| Level | Meaning | Allowed in P8.9 | Blocked behavior | Required future gate | Retention posture | Limitations |
|---|---|---|---|---|---|---|
| H0 | User manually copies tickets / packages into external harness and manually pastes output back. | Yes. | Automation, API calls, OpenCode execution by AGENT PLATFORM. | No future gate for manual external use; future implementation still requires exact approval. | Local-only metadata and generated evidence posture. | User-operated only. |
| H1 | Metadata-only harness adapter design. | Yes, design only. | Executable adapter, CLI/API/MCP integration, output fetching. | Future implementation gate. | Metadata-only retention. | No execution. |
| H2 | Controlled tool execution adapter. | No. | Any OpenCode execution, commands, network/API/MCP, tool side effects. | Future exact tool/provider/security/validation/human approval gate. | Future-gated. | H2 controlled execution adapter is blocked by default. |
| H3 | Autonomous orchestration adapter. | No. | Autonomous routing, scheduling, review, integration, Git mutation. | Future AL-2+ governance if ever considered. | Future-gated. | H3 autonomous orchestration adapter is blocked. |

Required decisions:

| Decision | P8.9 posture |
|---|---|
| H0 | H0 user-operated harness is allowed. |
| H1 | H1 metadata-only adapter design is allowed as design only. |
| H2 | H2 controlled execution adapter is blocked by default. |
| H3 | H3 autonomous orchestration adapter is blocked. |
| Hermes runtime | Blocked. |
| MCP activation | Blocked. |
| Provider/auth automation | Blocked. |
| Automatic tool execution | Blocked. |
| Automatic task routing | Blocked. |
| Automatic output retrieval | Blocked. |
| Automatic review | Blocked. |
| Automatic integration | Blocked. |
| Git mutation | Blocked. |

## OpenCode Current-State Model
OpenCode is a manual external development harness candidate.

OpenCode is used by the user, not by AGENT PLATFORM runtime.

OpenCode may receive manually copied HarnessInputPackage content.

OpenCode may produce output that the user manually pastes back.

OpenCode output must be treated as generated evidence by default.

OpenCode output must be reviewed before integration.

OpenCode output must be integrated manually or through future non-executing MVP checklist assistance.

OpenCode output must not become accepted output automatically.

OpenCode must not mutate AGENT PLATFORM Git state through P8.9.

OpenCode remains H0 user-operated harness.

OpenCode current use is H0 user-operated harness.

OpenCode current use is not tool execution by AGENT PLATFORM.

OpenCode current use is not OpenCode adoption as runtime.

## OpenCode Boundary Object Model
| Object | Meaning | Required fields | Forbidden fields | Security posture | Validation posture | Activation posture |
|---|---|---|---|---|---|---|
| OpenCodeHarnessBoundary | Metadata boundary for OpenCode harness use. | ID, harness name, level, allowed/blocked use, refs, posture, stop rules. | Runtime config, credentials, adapter code. | Must exclude secrets/credentials. | Not validation execution. | Metadata only. |
| HarnessLevelDecision | H0/H1/H2/H3 decision record. | Level, decision, allowed/blocked behavior, future gate. | Activation by decision. | Preserve blockers. | Not validation. | Not execution. |
| OpenCodeH0ManualUseRecord | H0 user-operated use record. | User owner, work packet, package refs, output boundary. | AGENT PLATFORM execution permission. | Manual copy/paste only. | Requires review. | H0 only. |
| OpenCodeH1MetadataAdapterCandidate | H1 metadata-only adapter candidate. | Scope, metadata inputs/outputs, no-execution boundaries. | Executable adapter, API/MCP/CLI integration. | No auth/network. | Future validation only. | Design only. |
| OpenCodeH2ControlledExecutionCandidate | H2 future controlled execution candidate. | Candidate scope, required gates, command scope, policies. | Approval by P8.9. | Requires security/human approval. | Requires future readiness. | Blocked by default. |
| OpenCodeH3AutonomousOrchestrationCandidate | H3 future autonomous candidate. | Orchestration scope, blocked-by-default, future governance. | Implementation or activation. | Requires future AL-2+ security. | Requires future validation. | Blocked. |
| HarnessInputPackageRef | Ref to package for manual harness use. | Package ref, scope, context/evidence refs, stop rules. | Raw forbidden content. | No secrets/product/raw external. | Not validation. | Not execution. |
| OpenCodePromptPackage | Prompt package candidate for manual OpenCode use. | Allowed scope, forbidden scope, expected output, boundaries. | Credentials, raw source, API calls. | Package safety required. | Completeness is not validation. | Not OpenCode execution. |
| ManualCopyPasteBoundary | Boundary for user copy/paste. | User action, allowed content, warnings, limitations. | Automation. | Preserves classification. | Not validation. | Not dispatch. |
| HarnessOutputSubmission | User-submitted output record. | Submitter, method, work packet, output refs, posture. | Auto-fetch. | Quarantine if unsafe. | Requires review. | Not execution. |
| OpenCodeOutputEvidenceRef | Evidence ref for OpenCode output. | Output ref, generated evidence posture, limitations. | Authority posture. | Generated evidence. | Evidence supports; it does not decide. | Not accepted output. |
| HarnessOutputPackageRef | Structured output package ref. | Output refs, review status, blockers, limitations. | Accepted output by default. | Preserve blockers. | Requires review/integration. | Not integration. |
| ReviewChecklistRef | Review checklist ref. | Review scope, items, evidence refs, blockers. | Auto-review. | Review cannot bypass blockers. | Checklist is not validation execution. | Not approval. |
| IntegrationChecklistRef | Integration checklist ref. | Integration scope, accepted/rejected refs, drift. | Automatic integration. | Preserves safety posture. | Not validation. | Not merge. |
| CommitCandidateRef | Commit candidate ref. | Exact paths, excluded paths, message candidate, human approval. | Git mutation. | Exact path safety. | Not validation. | Not Git mutation. |
| GitAdvisoryRef | Git advisory ref. | Advisory command refs, limitations, user action required. | Agent-executed Git. | Preserve user authority. | Not validation. | Advisory only. |
| HarnessStopRule | Stop rule for harness boundary. | Condition, blocked consequence, required human action. | Auto-waiver. | Stops on security blockers. | Not validation. | Blocks activation. |
| HarnessIncidentRef | Incident route metadata. | Trigger, route, owner/ref, limitations. | Incident automation. | Required for sensitive/forbidden material. | Not validation. | Not runtime monitoring. |

## OpenCodeHarnessBoundary Contract
OpenCodeHarnessBoundary fields:

| Field | Requirement |
|---|---|
| boundary_id | Stable identifier. |
| harness_name | OpenCode. |
| harness_classification | External user-operated harness candidate. |
| current_level | H0. |
| allowed_levels | H0; H1 as design only. |
| blocked_levels | H2 and H3 blocked by default. |
| allowed_uses | Manual package generation and user copy/paste boundary. |
| forbidden_uses | OpenCode execution, adapter implementation, API/MCP integration, output fetching, Git mutation. |
| manual_copy_paste_boundary | User-only copy/paste boundary. |
| input_package_refs | HarnessInputPackage refs. |
| output_submission_refs | HarnessOutputSubmission refs. |
| evidence_refs | OpenCodeOutputEvidenceRef refs. |
| validation_refs | Validation refs. |
| security_refs | Security refs. |
| retention_refs | Retention refs. |
| rollback_refs | Rollback refs. |
| incident_refs | Incident refs. |
| tool_execution_posture | Not approved. |
| provider_auth_posture | Not approved. |
| mcp_posture | Not active. |
| network_posture | Not approved. |
| git_mutation_posture | Forbidden for agent. |
| source_loading_posture | Not approved. |
| product_boundary_posture | Product/Siamese source blocked. |
| generated_output_posture | Generated evidence by default. |
| human_approval_required | Required for future implementation or gate changes. |
| future_gate_requirements | Required for H1 implementation and any H2/H3 consideration. |
| stop_rules | HarnessStopRule refs. |
| limitations | Limitations. |

OpenCodeHarnessBoundary is metadata.

OpenCodeHarnessBoundary does not execute OpenCode.

OpenCodeHarnessBoundary does not implement adapter behavior.

## H0 Manual Use Contract
H0 fields:

| Field | Requirement |
|---|---|
| h0_use_id | Stable identifier. |
| user_owner | User owner. |
| work_packet_ref | WorkPacket ref. |
| harness_input_package_ref | HarnessInputPackage ref. |
| manual_prompt_package_ref | Prompt package ref. |
| copy_paste_instruction | Manual copy/paste instruction. |
| manual_execution_note | User manually runs OpenCode. |
| expected_output_contract | Expected output contract. |
| output_paste_boundary | User paste boundary. |
| review_required | Required. |
| integration_required | Required. |
| git_mutation_forbidden_for_agent | Required. |
| retention_posture | Retention posture. |
| rollback_posture | Rollback posture. |
| incident_posture | Incident posture. |
| blockers | Blockers. |
| limitations | Limitations. |

H0 is user-operated.

H0 does not authorize AGENT PLATFORM to execute OpenCode.

H0 does not authorize AGENT PLATFORM to inspect OpenCode state.

H0 does not authorize AGENT PLATFORM to fetch output.

H0 does not authorize AGENT PLATFORM to mutate Git.

## H1 Metadata Adapter Candidate Contract
H1 fields:

| Field | Requirement |
|---|---|
| h1_candidate_id | Stable identifier. |
| adapter_scope | Metadata-only scope. |
| adapter_purpose | Package/rendering metadata design. |
| metadata_inputs | Metadata inputs only. |
| metadata_outputs | Metadata outputs only. |
| supported_package_refs | Supported package refs. |
| schema_refs | Schema refs. |
| rendering_contract_refs | Rendering contract refs. |
| no_execution_boundary | Required. |
| no_api_boundary | Required. |
| no_mcp_boundary | Required. |
| no_auth_boundary | Required. |
| no_network_boundary | Required. |
| no_file_write_boundary | Required until implementation gate. |
| no_git_mutation_boundary | Required. |
| required_future_validation_refs | Future refs. |
| required_future_security_refs | Future refs. |
| retention_posture | Retention posture. |
| rollback_posture | Rollback posture. |
| incident_posture | Incident posture. |
| blockers | Blockers. |
| limitations | Limitations. |

H1 metadata-only adapter design is metadata-only design.

H1 may describe how packages would be rendered or indexed.

H1 may describe how manual copy/paste instructions would be produced.

H1 must not execute OpenCode.

H1 must not invoke OpenCode.

H1 must not automate task routing.

H1 must not fetch OpenCode output.

H1 must not write repo state.

## H2 Controlled Execution Adapter Candidate Contract
H2 fields:

| Field | Requirement |
|---|---|
| h2_candidate_id | Stable identifier. |
| candidate_scope | Future exact scope only. |
| required_tool_gate | Required future exact tool gate. |
| required_provider_gate_if_any | Required if provider/auth/API/MCP implicated. |
| required_security_review | Required. |
| required_validation_readiness | Required. |
| required_human_approval | Required. |
| allowed_command_scope_candidate | Future exact candidate only. |
| blocked_command_scope | Broad command scope blocked. |
| input_surface_requirements | Required future input boundaries. |
| output_surface_requirements | Required future output boundaries. |
| side_effect_profile | Required. |
| credential_policy | No credential use without exact future gate. |
| network_policy | No network without exact future gate. |
| retention_posture | Required. |
| rollback_posture | Required. |
| incident_posture | Required. |
| stop_rules | Required. |
| limitations | Required. |

H2 is future candidate only.

H2 controlled execution is blocked by default.

H2 must not be implemented by P8.9.

H2 must not be approved by P8.9.

H2 requires future exact gate.

H2 requires exact command/action scope before any execution decision.

## H3 Autonomous Orchestration Candidate Contract
H3 fields:

| Field | Requirement |
|---|---|
| h3_candidate_id | Stable identifier. |
| orchestration_scope | Future autonomous scope only. |
| autonomous_dispatch_scope | Blocked. |
| scheduler_scope | Blocked. |
| handoff_scope | Blocked. |
| review_assignment_scope | Blocked. |
| integration_scope | Blocked. |
| git_scope | Blocked. |
| blocked_by_default | Required. |
| required_future_governance | Future AL-2+ governance. |
| required_future_security | Future security review. |
| required_future_validation | Future validation readiness. |
| required_future_human_approval | Future human approval. |
| limitations | Limitations. |

H3 is blocked.

H3 autonomous orchestration is not a P8.9 candidate for implementation.

H3 requires future AL-2+ governance, if ever considered.

## Prompt / HarnessInputPackage Boundary
AGENT PLATFORM may generate HarnessInputPackage as future MVP-0 behavior.

AGENT PLATFORM may render a prompt package for manual OpenCode use as future MVP-0 behavior.

HarnessInputPackage generation is not harness execution.

Prompt package rendering is not OpenCode execution.

Prompt package must include allowed scope, forbidden scope, context refs, evidence refs, expected output format, stop rules, security boundaries, and Git mutation prohibition.

Prompt package must not include secrets, credentials, raw product source, raw external source, raw Graphify output, provider auth material, token stores, browser auth, API keys, unknown-sensitivity material, or unreviewed local-only content.

## Manual Copy / Paste Boundary
Manual copy/paste is performed by the user.

Manual copy/paste is not automated dispatch.

Manual copy/paste is not internal runtime adoption.

Manual copy/paste is not provider/auth.

Manual copy/paste is not MCP.

Manual copy/paste is not Git mutation.

Manual copy/paste must preserve source classification and sensitivity.

Manual copy/paste must include warning when local-only, generated, product, external, or sensitive boundaries exist.

## HarnessOutput Intake Boundary
OpenCode output enters AGENT PLATFORM only when pasted by the user.

HarnessOutputSubmission is user-submitted.

HarnessOutputPackage is structured generated evidence.

HarnessOutputPackage is not accepted output.

HarnessOutputPackage requires review.

HarnessOutputPackage requires integration pass.

HarnessOutputPackage must preserve generated-output posture.

HarnessOutputPackage must preserve source classification, sensitivity, blockers, retention, rollback, and incident posture.

HarnessOutputPackage must be quarantined or rejected if it contains secrets, credentials, product source, raw external source, raw Graphify output, unknown-sensitivity material, or forbidden material.

## Review / Integration Boundary
Review checklist is not auto-review.

Reviewer verdict is not Git approval.

Integration checklist is not automatic integration.

Integrator output is not automatic merge.

AcceptedOutputRegister is not commit approval.

CommitCandidate is not Git mutation.

CommitCommandBlock is advisory only.

The user remains final commit authority.

Never recommend git add ..

## OpenCode / Security Interface
Secrets and credentials are never OpenCode package content.

API keys, tokens, passwords, private keys, OAuth sessions, browser auth, provider configs, token stores, local credential stores, `.env`, and credential values are never package content.

Unknown sensitivity blocks package generation.

Product/Siamese source is blocked.

External source contents are blocked unless future exact review approves.

Raw Graphify output is blocked.

Raw live connector payloads are blocked.

Customer-sensitive data is blocked unless future exact review approves.

Security constrains; it does not activate.

## OpenCode / Validation Interface
Validation evaluates; governance decides.

Prompt package completeness is not validation execution.

Harness output review is not validation execution.

No tests, scripts, CI, build, lint, typecheck, package-manager, OpenCode command, or validation command is approved by P8.9.

## OpenCode / Source Classification Interface
Source classification is not source loading permission.

Path presence is not content inspection permission.

HarnessInputPackage may include metadata refs but not unapproved raw source content.

HarnessOutputPackage may include generated evidence only after user paste.

P8.9 must preserve P3.0 source classification posture.

P8.9 must preserve P8.0 and P8.1 external integration boundaries.

## OpenCode / Provider / MCP Interface
OpenCode H0 manual use is not provider/auth activation.

OpenCode H1 metadata adapter design is not provider/auth activation.

OpenCode H2/H3 would require future exact provider/tool/MCP gates if they involve API/MCP/network/tool behavior.

P8.9 does not approve provider/auth/API/MCP.

P8.9 does not approve network.

P8.9 does not approve MCP.

P8.9 does not approve credential use.

## OpenCode / Agent Runtime Interface
Agent metadata is not agent execution.

Generating HarnessInputPackage is not agent dispatch.

Manual harness use is not agent runtime.

OpenCode output does not wake agents.

OpenCode output does not trigger automatic review.

OpenCode output does not trigger automatic integration.

OpenCode output does not trigger Git mutation.

## OpenCode / External Candidate Interface
OpenCode is external harness candidate.

OpenCode is not adopted as internal runtime.

OpenCode source inspection is not approved.

OpenCode execution is not approved.

OpenCode adapter implementation is not approved.

Manual OpenCode use remains H0.

External path metadata posture: `external/sources/gbrain-master`, `external/sources/gstack`, `external/sources/gstack-master`, `external/sources/hermes`, and `external/sources/graphify` were absent in boundary checks and were not inspected.

## Product / Siamese Boundary
Siamese is product vision, not product activation.

P8.9 must not inspect product source.

P8.9 must not load product source into OpenCode packages.

P8.9 must not create product-bound harness packages from product source.

Product/Siamese package generation remains blocked until future product-bound readiness and exact source gate.

MVP-0 OpenCode flow must be product-independent by default.

## Retention / Rollback / Incident Posture
| Boundary record | Required posture |
|---|---|
| OpenCodeHarnessBoundary | Retention, rollback, incident, human approval, stop rules. |
| OpenCodeH0ManualUseRecord | Retention, rollback, incident, manual copy/paste limits. |
| OpenCodeH1MetadataAdapterCandidate | Metadata-only retention, rollback, incident, future validation/security refs. |
| OpenCodeH2ControlledExecutionCandidate | Future-gated retention, rollback, incident, command scope and side-effect posture. |
| OpenCodeH3AutonomousOrchestrationCandidate | Future AL-2+ retention, rollback, incident, governance limits. |
| HarnessInputPackageRef | Retention, source classification, security exclusions. |
| OpenCodePromptPackage | Retention, forbidden content exclusions, stop rules. |
| ManualCopyPasteBoundary | Retention and user action boundary. |
| HarnessOutputSubmission | Retention, quarantine, incident posture. |
| OpenCodeOutputEvidenceRef | Generated evidence retention and limitations. |
| HarnessOutputPackageRef | Review/integration retention and blocker posture. |
| ReviewChecklistRef | Review retention and non-auto-review posture. |
| IntegrationChecklistRef | Integration retention and non-automatic-integration posture. |
| CommitCandidateRef | Exact-path retention, rollback note, human approval. |
| GitAdvisoryRef | Advisory-only retention, no Git mutation. |

Every OpenCode boundary record must include retention posture.

Every OpenCode boundary record with downstream decision impact must include rollback posture.

Every OpenCode boundary record with sensitive, product, external, provider, live connector, generated output, or unknown-sensitivity material must include incident posture.

Accidental inclusion of secrets, credentials, product source, raw external source, raw Graphify output, or raw live connector payloads requires STOP and safe reporting.

## Human Approval Requirements
Human user must manually run OpenCode in H0.

Human user must manually paste OpenCode output.

Human user must approve any future H1 implementation.

Human user must approve any future H2/H3 consideration.

Human user remains final commit authority.

Human user performs Git manually.

No OpenCode output can replace human approval.

No HarnessOutputPackage can replace review/integration/human decision.

## Stop Rules
STOP if P8.0 is missing.

STOP if P8.1 is missing.

STOP if P8.5 is missing.

STOP if P8.9 attempts to execute OpenCode.

STOP if P8.9 attempts to implement OpenCode adapter code.

STOP if P8.9 attempts to send prompts to OpenCode.

STOP if P8.9 attempts to fetch OpenCode output.

STOP if P8.9 attempts to inspect OpenCode source/config/auth/state.

STOP if P8.9 attempts to activate H2 or H3.

STOP if P8.9 attempts provider/auth/API/MCP.

STOP if P8.9 attempts tool execution.

STOP if P8.9 attempts automatic task routing.

STOP if P8.9 attempts automatic review or integration.

STOP if P8.9 attempts Git mutation.

STOP if package content includes secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, or credential values.

STOP if package content includes product/Siamese source.

STOP if package content includes raw external source.

STOP if package content includes raw Graphify output.

STOP if package content includes unknown-sensitivity material.

STOP if OpenCode output is treated as accepted without review.

STOP if review verdict is treated as Git approval.

STOP if CommitCandidate is treated as Git mutation.

STOP if git add . is recommended.

## Required P8.9 Invariants
| Invariant | Statement |
|---|---|
| OC-001 | P8.9 is OpenCode harness upgrade boundary only. |
| OC-002 | OpenCode harness upgrade boundary is not OpenCode adapter implementation. |
| OC-003 | OpenCode remains H0 user-operated harness. |
| OC-004 | H0 user-operated harness is allowed. |
| OC-005 | H1 metadata-only adapter design is allowed as design only. |
| OC-006 | H2 controlled execution adapter is blocked by default. |
| OC-007 | H3 autonomous orchestration adapter is blocked. |
| OC-008 | HarnessInputPackage generation is not harness execution. |
| OC-009 | Prompt package rendering is not OpenCode execution. |
| OC-010 | Manual copy/paste is not integration. |
| OC-011 | Manual OpenCode use is not internal runtime adoption. |
| OC-012 | OpenCode output is generated evidence by default. |
| OC-013 | HarnessOutputPackage is not accepted output. |
| OC-014 | Review checklist is not auto-review. |
| OC-015 | Integration checklist is not automatic integration. |
| OC-016 | CommitCandidate is not Git mutation. |
| OC-017 | CommitCommandBlock is advisory only. |
| OC-018 | No OpenCode execution. |
| OC-019 | No OpenCode adapter implementation. |
| OC-020 | No OpenCode API/MCP integration. |
| OC-021 | No provider/auth/API/MCP activation. |
| OC-022 | No tool execution. |
| OC-023 | No automatic task routing. |
| OC-024 | No automatic output retrieval. |
| OC-025 | No automatic review. |
| OC-026 | No automatic integration. |
| OC-027 | No product/Siamese source in packages. |
| OC-028 | No secrets or credentials in packages. |
| OC-029 | No generated output tracking. |
| OC-030 | No source tracking expansion. |
| OC-031 | The user remains final commit authority. |
| OC-032 | The agent never mutates Git. |
| OC-033 | Never recommend git add .. |

## Future Validation Targets
Future validation targets are proposed only and were not executed:

| Target | Purpose |
|---|---|
| OpenCodeHarnessBoundary required fields completeness | Verify boundary fields. |
| HarnessLevelDecision H0/H1/H2/H3 compliance | Verify harness level decisions. |
| H0 manual-use-only invariant | Verify H0 stays user-operated. |
| H1 metadata-only invariant | Verify H1 stays design-only. |
| H2 blocked-by-default invariant | Verify H2 remains blocked. |
| H3 blocked invariant | Verify H3 remains blocked. |
| HarnessInputPackage no-execution invariant | Verify packages do not execute harnesses. |
| Prompt package no-OpenCode-execution invariant | Verify prompt rendering does not execute OpenCode. |
| ManualCopyPasteBoundary no-dispatch invariant | Verify manual copy/paste is not dispatch. |
| HarnessOutputSubmission user-pasted invariant | Verify output is user-pasted. |
| OpenCodeOutputEvidenceRef generated-evidence invariant | Verify OpenCode output is generated evidence. |
| HarnessOutputPackage not-accepted-output invariant | Verify output package is not accepted output. |
| review-checklist-not-auto-review invariant | Verify review is not automatic. |
| integration-checklist-not-auto-integration invariant | Verify integration is not automatic. |
| CommitCandidate no-Git-mutation invariant | Verify commit candidate is not Git mutation. |
| no-secret/no-credential package invariant | Verify forbidden material excluded. |
| no-product-source package invariant | Verify product source excluded. |
| no-raw-external-source package invariant | Verify raw external source excluded. |
| no-raw-Graphify-output package invariant | Verify raw Graphify output excluded. |
| no-provider-auth-MCP invariant | Verify provider/auth/MCP inactive. |
| no-tool-execution invariant | Verify no tool execution. |
| no-OpenCode-execution invariant | Verify OpenCode is not executed. |
| no-OpenCode-adapter-implementation invariant | Verify no adapter implementation. |
| never-recommend-git-add-dot invariant | Verify exact Git safety. |
| P8.2 interaction surface alignment | Future alignment check. |
| P8.3 schema alignment | Future alignment check. |
| P8.4 state model alignment | Future alignment check. |
| P8.5 security gate alignment | Future alignment check. |
| P8.10 synthesis readiness check | Future readiness check. |

## Future Hardening Candidates
Future tickets are proposed only and not started:

| Candidate | Purpose |
|---|---|
| OC-HARD-01 - OpenCode H0 Manual Harness Package Contract | Harden H0 manual package contract. |
| OC-HARD-02 - OpenCode H1 Metadata Adapter Schema Boundary | Harden H1 metadata-only boundary. |
| OC-HARD-03 - HarnessInputPackage Prompt Safety Checklist | Harden prompt package exclusions. |
| OC-HARD-04 - HarnessOutputPackage Intake Safety Checklist | Harden output intake safety. |
| OC-HARD-05 - OpenCode Output Generated Evidence Boundary | Harden generated evidence posture. |
| OC-HARD-06 - OpenCode H2 Future Execution Gate Checklist | Define future H2 gate checklist. |
| OC-HARD-07 - OpenCode H3 Autonomous Orchestration Rejection Checklist | Define H3 rejection checklist. |
| OC-HARD-08 - Manual Harness Git Safety Checklist | Harden manual harness Git safety. |

## Created / Modified / Not Created Register
| Item | Status |
|---|---|
| OpenCode harness upgrade boundary document | Created. |
| OpenCodeHarnessBoundary model | Created. |
| HarnessLevelDecision model | Created. |
| OpenCodeH0ManualUseRecord model | Created. |
| OpenCodeH1MetadataAdapterCandidate model | Created. |
| OpenCodeH2ControlledExecutionCandidate model | Created. |
| OpenCodeH3AutonomousOrchestrationCandidate model | Created. |
| HarnessInputPackageRef model | Created. |
| OpenCodePromptPackage model | Created. |
| ManualCopyPasteBoundary model | Created. |
| HarnessOutputSubmission model | Created. |
| OpenCodeOutputEvidenceRef model | Created. |
| HarnessOutputPackageRef model | Created. |
| ReviewChecklistRef model | Created. |
| IntegrationChecklistRef model | Created. |
| CommitCandidateRef model | Created. |
| GitAdvisoryRef model | Created. |
| H0 user-operated harness | Confirmed. |
| H1 metadata-only adapter design | Allowed as design only. |
| H2 controlled execution adapter | Blocked by default. |
| H3 autonomous orchestration adapter | Blocked. |
| OpenCode executed | No OpenCode executed. |
| `opencode` command run | No opencode command run. |
| OpenCode prompt sent | No OpenCode prompt sent. |
| OpenCode output fetched | No OpenCode output fetched. |
| OpenCode adapter implemented | Not created. |
| OpenCode wrapper implemented | Not created. |
| OpenCode CLI/API/MCP integration created | Not created. |
| MVP package created | Not created. |
| `3_platform/_governed_skeleton` modified | Not modified. |
| Runtime code implemented | Not implemented. |
| Runtime activation | Not created. |
| Autonomous orchestration | Not created. |
| Automatic dispatch | Not created. |
| Automatic handoff | Not created. |
| Automatic reviewer assignment | Not created. |
| Automatic integration | Not created. |
| Automatic task routing | Not created. |
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
| OpenCode source inspection | Not created. |
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
P8.9 is one Round 2 external candidate boundary ticket.

Round 2 after P8.1 and P8.5:

| Ticket | Name | Current posture |
|---|---|---|
| P8.6 | Graphify Read-Only Evidence Boundary | Missing; pending alignment. |
| P8.7 | GBrain / GStack Memory Compatibility Boundary | Missing; pending alignment. |
| P8.8 | Hermes Interface / Runtime Candidate Boundary | Missing; pending alignment. |
| P8.9 | OpenCode Harness Upgrade Boundary | Complete by this document. |

After P8.2-P8.9:

| Ticket | Name | Boundary |
|---|---|---|
| P8.10 | MVP-0 Architecture Synthesis | Do not start P8.10 inside P8.9. |

Recommended actual: Continue remaining P8.6-P8.9 external boundary tickets until Round 2 is complete.

When P8.2-P8.9 are complete, proceed to P8.10 - MVP-0 Architecture Synthesis.

Do not start P8.10 inside P8.9.

## Final Verdict
| Question | Answer |
|---|---|
| What did P8.9 create? | `0_architecture/governance/agent_platform_opencode_harness_upgrade_boundary.md`. |
| What OpenCode harness upgrade boundary was defined? | OpenCode remains H0 user-operated harness, H1 is metadata-only adapter design, H2 is future-gated and blocked by default, and H3 is blocked. |
| What is OpenCode current posture? | OpenCode remains H0 user-operated external harness, not internal runtime. |
| What is H0? | User manually copies package to OpenCode, manually runs OpenCode, and manually pastes output back. |
| What is H1? | Metadata-only adapter design; design only, no execution or implementation in P8.9. |
| What is H2? | Controlled execution adapter candidate; blocked by default and future-gated. |
| What is H3? | Autonomous orchestration adapter candidate; blocked. |
| Which harness levels are allowed? | H0 is allowed; H1 is allowed as design only. |
| Which harness levels are blocked? | H2 controlled execution adapter is blocked by default and H3 autonomous orchestration adapter is blocked. |
| Can AGENT PLATFORM generate HarnessInputPackage / prompt packages for manual OpenCode use? | Yes as future MVP-0 behavior, but generation is not execution. |
| Does HarnessInputPackage generation execute OpenCode? | No. HarnessInputPackage generation is not harness execution. |
| Does prompt package rendering execute OpenCode? | No. Prompt package rendering is not OpenCode execution. |
| How does OpenCode output enter AGENT PLATFORM? | Only by user-pasted HarnessOutputSubmission. |
| Is OpenCode output accepted output? | No. OpenCode output is generated evidence by default and HarnessOutputPackage is not accepted output. |
| What review/integration boundary applies to OpenCode output? | Review checklist is not auto-review, Integration checklist is not automatic integration, and output must pass review/integration before any CommitCandidate. |
| Did P8.9 execute OpenCode? | No. |
| Did P8.9 implement an OpenCode adapter? | No. |
| Did P8.9 create OpenCode CLI/API/MCP integration? | No. |
| Did P8.9 activate H2 or H3? | No. |
| Did P8.9 activate provider/auth/API/MCP? | No. |
| Did P8.9 execute tools? | No. |
| Did P8.9 activate agents or autonomous orchestration? | No. |
| Did P8.9 inspect product/Siamese source? | No. |
| Did P8.9 inspect OpenCode source/config/auth/state? | No. |
| Did P8.9 approve generated output tracking? | No. |
| Did P8.9 approve source tracking expansion? | No. |
| Did P8.9 mutate Git? | No. |
| Can the agent recommend git add .? | No. Never recommend git add .. |
| Who remains final commit authority? | The user remains final commit authority. |
| What is the next ticket? | Continue missing Round 2 external boundary tickets P8.6, P8.7, and P8.8; do not start P8.10 inside P8.9. |

Final verdict: P8.9 is accepted as the OpenCode Harness Upgrade Boundary for MVP-0 architecture. It formalizes H0 manual OpenCode use, allows H1 metadata-only adapter design as design only, blocks H2/H3 by default, creates no adapter, executes no OpenCode command, activates nothing, and leaves Git entirely manual.
