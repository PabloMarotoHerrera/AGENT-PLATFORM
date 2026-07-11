# P3.4 - Provider/Auth/API/MCP Activation Decision

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Provider/Auth/API/MCP Activation Decision |
| Ticket | P3.4 |
| Status | Accepted provider/auth/API/MCP activation decision record with activation deferred |
| Date | 2026-07-04 |
| Scope | Decide the current provider/auth/API/MCP activation posture for AGENT PLATFORM / Siamese after P3 readiness reconciliation, without executing or implementing activation. |
| Authority | Decision record only, not runtime activation, provider runtime implementation, auth configuration, credential approval, API calls, network calls, MCP activation, live connector activation, validation execution, security enforcement implementation, source loading, source tracking approval, generated-output tracking approval, product activation, Graphify adoption, Git mutation, publication, or Cognitive Semantic System substrate selection. |
| Required upstream records | P3.R, P3.0, P3.1, P3.2, P2.KR, P2.R, P2.1, P2.2, P2.3, P1.1-P1.5, P0.1-P0.3, G-19, G-01, Graphify Repo Map Summary, S-03, S-04, Cognitive Semantic System ADR/audit, README.md, `.gitignore`, `.graphifyignore`. |
| Optional peer records checked | P3.3 Tool Execution Activation Decision and EXT.GB-01 GBrain External Source Intake Review. |
| Output | ProviderAuthActivationDecision documentation contract and current decision posture. |

Decision is not execution.

AGENT PLATFORM remains pre-active at AL-1.

## 2. Purpose
P3.4 records whether AGENT PLATFORM / Siamese may activate providers, authentication, APIs, network calls, MCP servers/tools/resources, live connector provider routes, provider-bound context transmission, or model/provider calls at the current stage.

The decision is intentionally conservative: provider/auth/API/MCP activation is deferred by default. P3.4 may define a future exact activation candidate, but that candidate is metadata-only and cannot authorize implementation, execution, credentials, provider calls, network calls, MCP sessions, live connectors, generated-output tracking, source tracking expansion, product source inspection, product activation, or publication.

P3.4 consumes P3.R, which reconciled P3.0 source classification readiness, P3.1 validation execution readiness, and P3.2 security enforcement readiness. P3.R made P3.4 eligible as an activation-decision ticket only. Eligibility is not activation approval.

## 3. Current Posture
| Area | Current posture | P3.4 decision |
| --- | --- | --- |
| Activation level | AGENT PLATFORM remains pre-active at AL-1 metadata skeleton. | No promotion. |
| Provider metadata | ProviderDescriptor and AdapterDescriptor contracts exist as metadata only. | Provider metadata is not provider activation. |
| Auth material | Secrets, credentials, API keys, tokens, `.env`, provider configs, token stores, browser auth, and local credential stores remain blocked. | CredentialRef metadata only. |
| API/network | Network/API/provider execution remains blocked by S-04 and GT-08. | No API, network, provider, model, cloud, registry, database, or telemetry calls. |
| MCP | MCP availability or metadata does not start, connect, list, authenticate, register, invoke, or expose resources. | MCP metadata is not MCP activation. |
| Validation | P3.1 defines readiness only. | No validation execution. |
| Security | P3.2 defines readiness only. | No security enforcement implementation or scanners. |
| Source classification | P3.0 is canonical source classification readiness. | Source classification is not source loading permission. |
| Evidence | P2.2 EvidenceRef supports decisions only. | Evidence supports; it does not decide. |
| Retention/rollback/incident | P2.3 defines metadata baselines. | No runtime persistence, telemetry, or rollback automation. |
| Product/Siamese | Siamese is product vision only. | No product source inspection or product activation. |
| Graphify | Curated generated supporting evidence only. | Graphify evidence is not authority or activation evidence by itself. |
| GBrain / Hermes / Cadence | Future inactive candidates only. | Not adopted, not executed, not provider/auth-approved, not Cadence-active. |
| Cognitive Semantic System | Accepted name; substrate deferred. | Cognitive Semantic System substrate remains deferred. |

API key availability is not API key approval.

## 4. Inputs Reviewed
| Input | P3.4 use | Limitation |
| --- | --- | --- |
| `0_architecture/governance/agent_platform_shared_metadata_vocabulary_alignment.md` | Canonical blocker, sensitivity, source, status, provider_auth_posture, and ref terms. | No schema or runtime implementation. |
| `0_architecture/governance/agent_platform_cross_lane_evidence_reference_contract.md` | EvidenceRef, SourceRef, ValidationRef, SecurityRef, GraphifyRef, ProductRef boundaries. | No evidence execution or raw content inclusion. |
| `0_architecture/governance/agent_platform_audit_retention_rollback_baseline.md` | Retention, rollback, quarantine, publication, tracking, incident posture. | No runtime logging, telemetry, persistence, rollback automation, or publication. |
| `0_architecture/governance/agent_platform_context_runtime_contract_hardening.md` | Context refs as metadata and provider-bound context blockers. | No source loading or provider transmission approval. |
| `0_architecture/governance/agent_platform_provider_adapter_metadata_contract_hardening.md` | ProviderDescriptor, AdapterDescriptor, CredentialRef, NetworkRequirement, MCPRequirement, and provider blockers. | No provider activation. |
| `0_architecture/governance/agent_platform_tool_execution_boundary_contract_hardening.md` | Tool execution blocker interface when provider/MCP tooling is implicated. | No tool execution. |
| `0_architecture/governance/agent_platform_agent_runtime_boundary_contract_hardening.md` | Agent provider refs and agent activation blockers. | No agent execution or handoff execution. |
| `0_architecture/governance/agent_platform_cognitive_semantic_system_prototype_hardening.md` | Cognitive Semantic System provider refs and substrate-neutral semantic boundaries. | No substrate selection. |
| `0_architecture/governance/agent_platform_activation_gate_enforcement_map.md` | GT-08, GT-05, GT-07, GT-12, GT-15 gate dependencies and stop rules. | Gate map is not approval. |
| `0_architecture/governance/agent_platform_validation_execution_gate_design.md` | Provider/auth readiness validation format and non-execution principle. | No validation command approval. |
| `0_architecture/governance/agent_platform_security_enforcement_hardening_plan.md` | Security hardening posture for provider/auth, credentials, network, MCP, source, generated outputs. | No enforcement runtime. |
| `0_architecture/governance/agent_platform_hybrid_parallel_work_packet_dependency_map.md` | G-19 sequencing for P3.4 and blocked activation lanes. | Planning only. |
| `0_architecture/governance/agent_platform_activation_gate_charter.md` | G-01 GT-08 Provider / API / MCP Activation Gate and universal gate fields. | Charter is not activation. |
| `0_architecture/security/agent_platform_local_only_secrets_credentials_policy.md` | S-03 local-only, secrets, credentials, provider auth, environment file, generated-output, Git safety rules. | No secret or credential inspection. |
| `0_architecture/security/agent_platform_tool_shell_network_mcp_execution_policy.md` | S-04 execution risk levels, network/API/provider, authentication, MCP, Git, package, product execution blocks. | No execution approval. |
| `0_architecture/cognitive_semantic_system/agent_platform_cognitive_semantic_system_naming_substrate_adr.md` | Accepted name and substrate-deferred posture. | No implementation authorization. |
| `README.md` | Root workspace orientation. | No runtime effect. |
| `.gitignore` | Local-only, generated, secrets, credentials, provider auth hygiene posture. | Hygiene, not security enforcement. |
| `.graphifyignore` | Graphify default-deny input boundary and hard exclusions. | Not permission to run Graphify or broaden source. |

Only governance, security, Cognitive Semantic System, README, `.gitignore`, and `.graphifyignore` inputs were inspected. Restricted source contents, product source, external source contents, secrets, credentials, generated raw outputs, provider configs, token stores, browser auth, local credential stores, API keys, model/provider endpoints, MCP servers, and runtime state were not inspected.

## 5. Optional Peer And External Review Checks
| Optional input | P3.4 path observation | P3.4 posture |
| --- | --- | --- |
| P3.3 Tool Execution Activation Decision | `0_architecture/governance/agent_platform_tool_execution_activation_decision.md` absent. | No pending P3.3 alignment required. Tool execution remains blocked by P1.3, S-04, GT-07, P3.R. |
| EXT.GB-01 GBrain External Source Intake Review | `0_architecture/governance/agent_platform_gbrain_external_source_intake_review.md` absent. | `pending_EXT.GB_01_external_source_review` remains active. |
| GBrain reference path | `external/sources/gbrain-master` absent in P3.4 path check. | Path/class metadata only if referenced; no contents inspected. |

The absence of P3.3 does not block this P3.4 decision because P3.4 does not approve tool execution. The absence of EXT.GB-01 preserves the external-source blocker for GBrain-related posture.

## 6. Decision Method
| Rule | P3.4 application |
| --- | --- |
| Choose the stricter interpretation when records overlap. | Non-activation, default-deny, no-secret, no-credential, no-network, no-MCP, no-source-loading, no-product, no-publication controls win. |
| Treat readiness as non-activation. | P3.0/P3.1/P3.2/P3.R readiness and reconciliation do not activate providers. |
| Treat provider metadata as metadata. | ProviderDescriptor, AdapterDescriptor, ProviderScope, AuthScope, NetworkScope, MCPScope, CredentialRef, and requirement records cannot call, authenticate, connect, transmit, or invoke. |
| Require exact future gate for any activation. | GT-08, GT-05, GT-04 where validation is involved, GT-07 where tools/MCP actions are involved, GT-09 where product is involved, GT-12/GT-15 where tracking/publication/output/incident is involved. |
| Preserve AL-1. | P3.4 does not promote AGENT PLATFORM beyond AL-1. |
| Preserve evidence roles. | EvidenceRef supports; ValidationRef evaluates posture; SecurityRef constrains; governance decides. |
| Preserve source classification. | P3.0 source classes and blockers propagate into ProviderAuthActivationDecision. |
| Preserve retention and incident rules. | P2.3 retention/rollback/incident metadata applies without automation. |
| Preserve external boundary. | GBrain/Hermes/Cadence remain future inactive candidate classes only. |

## 7. ProviderAuthActivationDecision Object Model
P3.4 defines the required documentation object `ProviderAuthActivationDecision`. It is a metadata decision object, not code, schema, registry implementation, config, provider setup, auth setup, MCP setup, or runtime object.

| Field | P3.4 binding |
| --- | --- |
| `decision_id` | Stable decision ID, such as `P3.4-PROVIDER-AUTH-DECISION-001`. |
| `decision_status` | Current default is `provider_auth_api_mcp_activation_deferred`. |
| `decision_scope` | Provider/auth/API/MCP activation decision only; no execution. |
| `provider_scope` | ProviderScope metadata only; no live provider instances. |
| `auth_scope` | AuthScope metadata only; no auth, session, token, key, OAuth, browser auth, or credential-store use. |
| `network_scope` | NetworkScope metadata only; no HTTP, socket, cloud, registry, database, provider, telemetry, or model calls. |
| `mcp_scope` | MCPScope metadata only; no start, connect, list, register, authenticate, invoke, or resource exposure. |
| `exact_provider_identity_required` | Required before any future activation can move beyond draft. |
| `data_sent` | `none` for P3.4; future gate must list exact data before any provider/network/MCP action. |
| `data_received` | `none` for P3.4; future gate must list expected output and retention before any action. |
| `credential_ref_model` | CredentialRef metadata only; no values, partial values, hashes, fingerprints, prefixes, suffixes, or derived identifiers. |
| `credential_value_policy` | Values are prohibited; stop and incident route if encountered. |
| `provider_config_policy` | Provider config content is not inspected, retained, created, or used. |
| `token_store_policy` | Token store content is not inspected, retained, created, or used. |
| `browser_auth_policy` | Browser auth state, cookies, sessions, and profiles are not inspected or used. |
| `local_credential_store_policy` | Local credential stores are not inspected or used. |
| `api_key_policy` | API key availability is not API key approval. No key validation or use. |
| `provider_output_policy` | No provider output is generated; future provider output is generated-sensitive unless curated by future gate. |
| `model_output_policy` | No model output is generated; future model output is evidence only, not authority. |
| `cost_posture` | No cost-bearing calls. Future cost posture required before any activation. |
| `telemetry_posture` | No telemetry, update checks, provider logging, analytics, or remote state. |
| `retention_posture` | Metadata-only retention; no secrets, credentials, provider configs, auth material, request payloads, responses, or raw generated outputs. |
| `rollback_posture` | Future rollback required before activation; P3.4 has no runtime to roll back. |
| `incident_posture` | Stop, safe metadata only, quarantine/removal review, credential rotation route if exposure is suspected. |
| `validation_requirements` | P3.1/P0.2-aligned future GT-04 validation proposal required; none executed by P3.4. |
| `security_requirements` | P3.2/P0.3/S-03/S-04-aligned future security review required; no enforcement implemented. |
| `source_classification_requirements` | P3.0 classification and blockers required for any future data, source, provider, product, external, generated, live connector, or auth scope. |
| `evidence_refs` | EvidenceRef metadata only, citing governance/security/CSS docs and curated Graphify summary where applicable. |
| `validation_refs` | ValidationRef metadata only; current validation status `not_executed`. |
| `security_refs` | SecurityRef metadata only; security constrains and blocks by default. |
| `product_refs` | ProductRef metadata only; Siamese product source remains blocked until GT-09. |
| `graphify_refs` | GraphifyRef metadata only for curated Graphify Repo Map Summary; raw output blocked. |
| `human_approval_required` | Required for any future exact provider/auth/API/MCP activation. |
| `stop_rules` | Stop on secret, credential, auth, provider config, token store, browser auth, local credential store, API call, network call, MCP action, product source, external source, generated-output tracking, publication, or Git mutation pressure. |
| `allowed_future_provider_classes` | Metadata registry candidates only, listed in section 11. |
| `blocked_provider_classes` | Activation/use blocked classes listed in section 12. |
| `candidate_for_future_exact_activation` | Provider metadata registry only; no runtime, credentials, calls, MCP, product, source loading, tracking, or publication. |
| `implementation_prerequisites` | Future exact implementation ticket, GT-08, GT-05, GT-04 if validation is involved, retention/rollback/incident plan, human approval, and exact scope. |
| `decision_limitations` | Documentation-only decision; no runtime proof, no connectivity proof, no secret inspection, no provider validation, no MCP validation. |
| `pending_alignment_refs` | `pending_EXT.GB_01_external_source_review` for GBrain-related external source posture; no P3.3 pending alignment required. |

## 8. Decision Status Model
| Status | Meaning | Activation implication |
| --- | --- | --- |
| `provider_auth_api_mcp_activation_deferred` | Current default: activation is not approved and may be reconsidered only by future exact gate. | No activation. |
| `provider_auth_api_mcp_activation_blocked` | Scope is unsafe, broad, missing required gate, or implicates forbidden material. | No activation. |
| `candidate_for_future_exact_activation` | Candidate metadata appears narrow enough for a future exact activation request. | No activation until future exact approval. |
| `eligible_for_later_implementation_ticket` | A future implementation ticket may be proposed after required gates and human approval. | No implementation by this status. |
| `rejected_for_scope` | Scope is wrong, broad, unsafe, or premature. | No activation. |
| `pending_alignment` | Required peer, source, security, validation, external, product, or gate alignment remains unresolved. | No activation. |
| `superseded` | Replaced by a newer governed decision. | No activation. |
| `deprecated` | No longer current. | No activation. |
| `unknown_decision_status` | Decision state is unknown. | Treat as blocked. |

No status in P3.4 permits provider calls, auth use, API calls, network calls, MCP activation, source loading, product activation, generated-output tracking, source tracking expansion, publication, or Git mutation.

## 9. Default Decision
| Decision ID | Decision question | Result |
| --- | --- | --- |
| P3.4-DEC-001 | Should AGENT PLATFORM activate providers, auth, APIs, network, MCP, live connectors, model/provider calls, or provider-bound context transmission now? | No. `provider_auth_api_mcp_activation_deferred`. |
| P3.4-DEC-002 | Does P3.4 approve credential use, credential inspection, auth config, API key validation, token store use, browser auth use, or local credential store use? | No. |
| P3.4-DEC-003 | Does P3.4 approve a future exact candidate scope? | Yes, only `candidate_for_future_exact_activation: provider metadata registry only`. |
| P3.4-DEC-004 | Does P3.4 approve implementation of that candidate? | No. Future exact implementation ticket and gates required. |
| P3.4-DEC-005 | Does P3.4 approve MCP activation? | No. MCP metadata is not MCP activation. |
| P3.4-DEC-006 | Does P3.4 change AL-1? | No. AGENT PLATFORM remains pre-active at AL-1. |
| P3.4-DEC-007 | Does P3.4 select Cognitive Semantic System substrate? | No. Cognitive Semantic System substrate remains deferred. |

Default decision status: `provider_auth_api_mcp_activation_deferred`.

## 10. Candidate Future Exact Activation Scope
P3.4 defines one narrow future candidate, but does not activate it:

```text
candidate_for_future_exact_activation: provider metadata registry only
```

Allowed future candidate scope:

| Scope item | Candidate allowance | Boundary |
| --- | --- | --- |
| Provider metadata registry | May be proposed later as a metadata-only registry for ProviderDescriptor and AdapterDescriptor records. | No code, runtime, provider clients, provider calls, network, auth, MCP, source loading, product source, generated-output tracking, source tracking, publication, or Git mutation by P3.4. |
| ProviderDescriptor records | May define provider identity, owner, kind, capabilities, blockers, evidence_refs, validation_refs, security_refs, retention_posture, review_required, limitations. | No live handles, endpoints with credentials, payloads, responses, provider outputs, or activation flags. |
| AdapterDescriptor records | May define adapter metadata, scope, supported operation metadata, blockers, refs, retention, review, limitations. | No callable adapter, runtime code, command, SDK, client, MCP config, or live session. |
| CredentialRef records | CredentialRef metadata only. | No credential values, token values, API key values, private keys, refresh tokens, browser auth, local credential-store content, `.env` content, partial values, hashes, or derived identifiers. |
| ProviderScope | Metadata-only exact scope field. | Not permission to connect, call, transmit, execute, route, or activate. |
| AuthScope | Metadata-only auth boundary field. | Not auth approval. |
| NetworkScope | Metadata-only network boundary field. | Not network/API/provider approval. |
| MCPScope | Metadata-only MCP boundary field. | Not MCP activation. |

This candidate is eligible only for a later exact implementation ticket if a human explicitly requests it and the future ticket provides exact scope, gates, validation/security posture, rollback, incident handling, and stop rules.

## 11. Allowed Future Provider Classes
Allowed means candidate metadata-only classification for a later review. It does not mean activation.

| Provider class | Allowed future metadata use | Blocked interpretation |
| --- | --- | --- |
| `governance_metadata_provider` | Cite governance records as metadata inputs for provider decision records. | Treating governance docs as provider activation. |
| `implementation_metadata_provider` | Cite implementation records as metadata posture, not live source. | Reading live implementation source or executing code. |
| `offline_stub_provider` | Record placeholder/stub provider metadata and blockers. | Treating stub as callable provider. |
| `generated_output_provider` | Cite curated generated evidence only when governed. | Raw generated output as provider authority, publication, or tracking. |
| `unknown_provider` | Mark blocked and require review. | Any activation while unknown. |

All allowed future classes remain subject to P3.0 source classification, P3.1 validation readiness, P3.2 security readiness, P2.3 retention/rollback/incident posture, S-03, S-04, G-01, and P0.1.

## 12. Blocked Provider/Auth/API/MCP Classes
| Blocked class | Current P3.4 status | Required future route |
| --- | --- | --- |
| `local_runtime_provider` | Blocked. | GT-06, GT-08, GT-05, GT-15, exact start/stop, rollback, security review. |
| `hosted_api_provider` | Blocked. | GT-08 plus S-03/S-04, exact endpoint, data sent/received, auth posture, cost, retention, rollback. |
| `model_provider` | Blocked. | GT-08 plus prompt/data/output, cost, telemetry, retention, generated-output, validation/security review. |
| `mcp_provider` | Blocked. | GT-08 plus GT-07/GT-05, server identity, transport, tools/resources, auth, file/network exposure, stop plan. |
| `external_data_provider` | Blocked. | GT-11 plus GT-08/security/license/provenance review. |
| `internal_product_adapter` | Blocked. | GT-09 plus GT-08/GT-07/GT-05/GT-15 as applicable. |
| `credential_bound_provider` | Blocked. | GT-08 plus explicit secure approval; no credential value inspection by P3.4. |
| `secret_bound_provider` | Blocked. | Secure incident/auth route plus GT-08/GT-15; no secret content. |
| Provider-bound context transmission | Blocked. | GT-08, GT-05, GT-04 if validation is involved, source classification, retention, rollback, incident posture. |
| Live connector provider route | Blocked. | GT-08, GT-05, GT-15, privacy/security/retention review, exact connector scope. |

## 13. ProviderScope / AuthScope / NetworkScope / MCPScope
| Scope object | Required future metadata | P3.4 current status |
| --- | --- | --- |
| ProviderScope | Exact provider identity, owner, provider kind, capability metadata, data classes, blockers, limitations, evidence_refs, validation_refs, security_refs. | Metadata-only; no live provider. |
| AuthScope | Auth type, credential_ref_ids, approval gate, security review, forbidden material, blockers, limitations. | Metadata-only; no auth. |
| NetworkScope | Network kind, endpoint classification, data sent, data received, external/product relation, approval gate, security refs, blockers. | Metadata-only; no network/API/provider call. |
| MCPScope | MCP server ref, capability refs, transport class, tool/resource exposure, auth posture, file/network access posture, approval gate, blockers. | Metadata-only; no MCP activation. |

Any future scope with unknown provider identity, unknown data exposure, unknown credential posture, unknown endpoint, unknown MCP resource/tool exposure, missing owner, missing rollback, missing validation/security posture, or unknown sensitivity stays blocked.

## 14. CredentialRef, Secrets, And Auth Material Policy
CredentialRef metadata only.

| Material | P3.4 policy |
| --- | --- |
| Secret values | Never inspect, print, summarize, normalize, transform, test, validate, copy, retain, or include. |
| Credential values | Never inspect, print, test, refresh, use, copy, retain, or infer approval from existence. |
| API keys | API key availability is not API key approval; no validation or use. |
| Tokens / refresh tokens | No inspection, refresh, testing, retention, or use. |
| Passwords / private keys | No inspection, copying, hashing, partial reveal, or use. |
| `.env` / `.env.*` | Do not inspect content. Reviewed templates are not implicated by P3.4. |
| Provider configs | Do not inspect, create, modify, retain, or use. |
| Token stores | Do not inspect or use. |
| Browser auth / cookies / sessions | Do not inspect or use. |
| Local credential stores | Do not inspect or use. |
| MCP auth | Do not authenticate MCP tools/resources. |

If any secret, credential, provider auth, API key, token, browser auth, local credential store, or provider config content appears necessary, P3.4 stop rules require STOP and safe metadata reporting only.

## 15. API, Network, Provider, And Model Call Policy
P3.4 approves no API, network, provider, or model calls.

| Call class | Current decision |
| --- | --- |
| HTTP / socket / webhook | Blocked. |
| Cloud API / registry / package index | Blocked. |
| Model provider / embedding / generation / evaluation provider | Blocked. |
| Database or service call | Blocked. |
| Telemetry, analytics, update check, version check | Blocked. |
| Provider SDK/client call | Blocked. |
| Provider connectivity test | Blocked. |
| API key test | Blocked. |
| Provider-bound context transmission | Blocked. |

Future approval requires exact endpoint/service class, data sent, data received, credential/auth posture, privacy/retention, cost/rate-limit posture, output handling, rollback, incident posture, and explicit human/governance approval.

## 16. MCP Scope Decision
MCP metadata is not MCP activation.

P3.4 does not approve:

| MCP action | P3.4 status |
| --- | --- |
| Starting MCP servers | Blocked. |
| Connecting to MCP servers | Blocked. |
| Listing MCP tools/resources when activation/auth/connection is required | Blocked. |
| Invoking MCP tools | Blocked. |
| Using MCP resources | Blocked. |
| Registering MCP config | Blocked. |
| Installing MCP dependencies | Blocked. |
| Authenticating MCP tools/resources | Blocked. |
| Exposing files, folders, services, providers, local-only content, generated outputs, or credentials through MCP | Blocked. |

Any future MCP request requires server identity, origin, owner, version, local/remote classification, transport, tools/actions, resource exposure, filesystem boundaries, network access, credential posture, side effects, logging/output handling, exact approval, and stop plan.

## 17. Evidence / Validation / Security Interfaces
| Interface | P3.4 rule |
| --- | --- |
| EvidenceRef | EvidenceRef is metadata only. Evidence supports; it does not decide. |
| SourceRef | SourceRef is metadata only. SourceRef relationship is not permission to read source or track source. |
| ValidationRef | ValidationRef records not-executed or future posture. Validation evaluates; governance decides. |
| SecurityRef | SecurityRef constrains provider/auth/API/MCP decisions and defaults to blocker where restrictive or unknown. |
| GraphifyRef | GraphifyRef may cite curated Graphify Repo Map Summary only; raw Graphify output remains blocked. |
| ProductRef | ProductRef is product-readiness metadata only; product source remains blocked until GT-09. |

No evidence reference may include raw secret values, credential values, API keys, tokens, passwords, private keys, provider configs, token stores, browser auth, `.env` contents, raw local-only source, raw product source, raw external source, raw generated Graphify output, provider output payloads, MCP resource payloads, tool output payloads, or agent output payloads.

## 18. Source Classification Interface
| Source/data class | P3.0 classification posture | P3.4 implication |
| --- | --- | --- |
| Governance docs | `governance_metadata`, canonical markdown input. | Allowed for P3.4 reasoning only. |
| Provider metadata | `provider_metadata`. | Metadata only; not activation. |
| Provider auth material | `provider_auth_material`, blocked by default. | No config/auth/session/key/token inspection or use. |
| Credentials | `credential_reference`, safe metadata only. | CredentialRef metadata only. |
| Secrets | `secret_value`, never memory content. | Stop and safe metadata only. |
| Product/Siamese source | `product_restricted`, blocked until GT-09. | No product source inspection or product activation. |
| Generated outputs / raw Graphify outputs | `generated_local_only`, blocked raw output. | No raw output inspection, tracking, publication, or authority. |
| Curated Graphify summary | `generated_graphify_evidence`, supporting only. | May support but cannot decide. |
| External source candidates | `external_source_candidate`, blocked until review. | No external content inspection, adoption, execution, import, install, copy, or dependency approval. |
| Live connector classes | `live_connector_class`, gate-controlled. | No connector access, polling, sync, ingestion, or permanent memory. |
| Cognitive Semantic System substrate candidates | `semantic_metadata`, substrate deferred. | No vector DB, graph DB, ontology runtime, database, persistence, or substrate selection. |
| Unknown sensitivity | `unknown_sensitivity`, blocked/needs review. | Treat as blocked. |

Path presence is not content inspection permission. Path absence is not approval to create, import, execute, or configure the path.

## 19. GBrain / Hermes / Cadence Boundary
P3.4 records the required GBrain boundary without inspecting external source contents.

| Boundary item | P3.4 posture |
| --- | --- |
| `external/sources/gbrain-master` | Path/class metadata only; path absent in P3.4 check; no content inspected. |
| Classification | `external_source_candidate` and `cadence_reference_candidate`. |
| EXT.GB-01 | Absent, so `pending_EXT.GB_01_external_source_review` remains active. |
| Adoption | not adopted. |
| Execution | not executed. |
| Import | not imported. |
| Configuration | not configured. |
| Dependency approval | not dependency-approved. |
| Provider/auth approval | not provider/auth-approved. |
| Cadence status | not Cadence-active. |
| Substrate status | not substrate. |
| Product/runtime status | Not product-active, not runtime-active, not live connector-active. |

GBrain / Hermes / Cadence remain future and inactive. P3.4 does not approve GBrain implementation, Hermes activation, Cadence activation, always-on behavior, polling, sync, notification, autonomous routing, memory refresh, live connector access, provider/auth/API/MCP use, dependency adoption, source copying, import, install, execution, or substrate selection.

## 20. Product / Siamese Boundary
Siamese remains product vision, not product activation.

P3.4 does not approve product source inspection, product source loading, product source tracking, product dependencies, product execution, product generated-output tracking, product provider adapters, product API/MCP use, product runtime, Omniverse/EnergyPlus execution, or product publication.

Any future product-bound provider, internal product adapter, product connector, product output, or product API/MCP route requires GT-09 plus applicable GT-08, GT-07, GT-05, GT-04, GT-12, and GT-15 review.

## 21. Cognitive Semantic System Boundary
Cognitive Semantic System is the accepted architecture name. Cognitive Semantic System substrate remains deferred.

P3.4 does not approve graph runtime, vector runtime, database, graph DB, vector DB, ontology runtime, persistence, embeddings, semantic index, semantic runtime, reasoning runtime, substrate scoring, substrate decision, or Graphify adoption.

Provider metadata may be referenced by future Cognitive Semantic System semantic records only as metadata with EvidenceRef, ValidationRef, SecurityRef, blockers, limitations, and substrate-neutral posture. Provider output cannot become authority through semantic inclusion.

## 22. Retention, Rollback, And Incident Posture
| Posture | P3.4 decision |
| --- | --- |
| Retention | Metadata-only retention for P3.4 decision fields, blockers, limitations, and refs. |
| Provider output retention | No provider output is generated. Future provider/model output is generated-sensitive unless curated by a future gate. |
| Credential retention | No credential values, value-derived identifiers, provider configs, token stores, browser auth, or local credential-store content may be retained. |
| Network/API/MCP output retention | No request payloads, responses, auth headers, MCP resource payloads, invoked tool outputs, telemetry, or logs are generated or retained. |
| Rollback | P3.4 has no runtime to roll back. Future activation requires rollback owner, trigger, deactivation, quarantine/removal, state restore/export, credential rotation route, evidence retention, and follow-up governance. |
| Incident | Stop on forbidden content or pressure to use credentials/auth/network/MCP/provider/product/source/generated output/Git. Report safe metadata only. |
| Publication | Publication blocked. |
| Source tracking | Source tracking expansion blocked. |
| Generated-output tracking | Generated-output tracking blocked. |

P3.4 implements no runtime logging, persistence, telemetry, rollback automation, incident automation, scanners, cleanup, quarantine action, deletion, rotation, or publication.

## 23. Human Approval Requirements
Any future provider/auth/API/MCP activation request must include explicit human/governance approval for exact scope only. AI agents may draft metadata but cannot be sole final approver.

Required future human approval fields:

| Field | Required content |
| --- | --- |
| Owner | Accountable human/governance owner. |
| Requester | Human or agent requesting exact review. |
| Provider identity | Exact provider, endpoint/service class, owner, and provider kind. |
| Auth posture | Credential class, CredentialRef metadata only, secure approval route, forbidden material. |
| Data sent | Exact prompts, files, metadata, headers, payloads, paths, environment data, user data, or none. |
| Data received | Expected response/output/artifacts/logs and sensitivity. |
| MCP scope | Exact server, transport, tools/resources, file/network/auth access, side effects, stop plan. |
| Validation posture | Future GT-04 proof target and exact command/data/output if validation is involved. |
| Security posture | S-03/S-04/P3.2-aligned constraints, incident route, local-only/product/external/generated-output handling. |
| Retention/rollback/incident | P2.3/GT-15-aligned plan. |
| Cost/telemetry | Cost, quota, retry, logging, retention, telemetry, training, remote storage posture. |
| Git/publication | Exact GT-12 approval if tracking, staging, commit, push, force-add, or publication is implicated. |

Broad approval is invalid. Approval for one exact scope cannot authorize adjacent providers, adjacent endpoints, adjacent commands, adjacent MCP tools, retries with new flags, package installs, product source, generated-output tracking, publication, or Git mutation.

## 24. Stop Rules
P3.4 stop rules require STOP and safe metadata reporting only when any of the following appears necessary or occurs:

| Trigger | Stop route |
| --- | --- |
| Secret, credential, API key, token, password, private key, `.env`, provider config, token store, browser auth, cookie, local credential store, cloud config, registry auth, SSH auth, service account, or MCP auth content is needed or encountered. | Stop; do not reveal, inspect, test, validate, copy, retain, or transform; report safe metadata only; require secure approval. |
| Provider/API/network/model/cloud/registry/database/telemetry call is needed. | Stop; require GT-08 and S-04 exact approval. |
| MCP server/tool/resource start, connect, list, register, authenticate, invoke, expose, or install is needed. | Stop; require exact MCP activation review. |
| Provider-bound context transmission is needed. | Stop; require source classification, GT-08, GT-05, retention, rollback, incident, and validation posture. |
| Tool/shell/subprocess/package/build/test/Git mutation is needed. | Stop; require GT-07/GT-14/GT-12 as applicable. |
| Product/Siamese source, product execution, product dependency, or product output is needed. | Stop; require GT-09. |
| External source content, external code, external dependency, or external instruction adoption is needed. | Stop; require GT-11 and exact external-source review. |
| `external/sources/gbrain-master` contents are needed. | Stop; require EXT.GB-01 or equivalent exact external-source review. |
| Generated raw output, raw Graphify output, `9_artifacts/`, generated-output tracking, source tracking expansion, publication, force-add, staging, commit, or push is needed. | Stop; require GT-12/GT-15 and exact human approval. |
| Runtime, scheduler, worker, service, daemon, live connector, polling, sync, watcher, Cadence, GBrain, Hermes, agent execution, or product activation is needed. | Stop; require future exact activation gates. |
| Cognitive Semantic System substrate, graph/vector/database/ontology runtime, embeddings, semantic persistence, or Graphify adoption is needed. | Stop; require GT-10/GT-13 and future substrate decision. |

## 25. Blockers Maintained
| Blocker | Status after P3.4 |
| --- | --- |
| `provider_auth_blocker` | Open. |
| `provider_network_blocker` | Open. |
| `provider_mcp_blocker` | Open. |
| `credential_exposure_blocker` | Open. |
| `secret_exposure_blocker` | Open. |
| `validation_execution_blocker` | Open for any future validation execution. |
| `security_review_blocker` | Open for any future activation. |
| `source_loading_blocker` | Open. |
| `source_tracking_blocker` | Open. |
| `generated_output_tracking_blocker` | Open. |
| `publication_blocker` | Open. |
| `product_source_blocker` | Open. |
| `product_activation_blocker` | Open. |
| `external_source_blocker` | Open. |
| `gbrain_adoption_blocker` | Open; `pending_EXT.GB_01_external_source_review`. |
| `cadence_activation_blocker` | Open. |
| `live_connector_activation_blocker` | Open. |
| `runtime_activation_blocker` | Open. |
| `tool_execution_blocker` | Open. |
| `agent_execution_blocker` | Open. |
| `graphify_authority_blocker` | Open. |
| `graphify_raw_output_blocker` | Open. |
| `substrate_selection_blocker` | Open. |
| `retention_review_blocker` | Open for any future activation/output. |
| `rollback_readiness_blocker` | Open for any future activation. |
| `incident_route_blocker` | Open for any future activation/output/credential risk. |

## 26. Created / Not Created Register
| Artifact or action | P3.4 status |
| --- | --- |
| `0_architecture/governance/agent_platform_provider_auth_api_mcp_activation_decision.md` | Created. |
| Provider/Auth/API/MCP Activation Decision | Created. |
| ProviderAuthActivationDecision documentation object | Defined. |
| Runtime code | Not created or modified. |
| Provider runtime code | Not created or modified. |
| Provider metadata registry implementation | Not created. |
| Auth configuration | Not created or modified. |
| Provider config | Not inspected, created, or modified. |
| API key | Not inspected, validated, or used. |
| Credential | Not inspected, validated, or used. |
| Secret | Not inspected. |
| `.env` | Not inspected. |
| Token store | Not inspected. |
| Browser auth | Not inspected or used. |
| Local credential store | Not inspected or used. |
| API/network/provider/model/MCP call | Not executed. |
| MCP server/tool/resource activation | Not executed. |
| Live connector | Not activated. |
| Validation | Not executed. |
| Tests / CI / lint / typecheck / build / package-manager commands | Not run. |
| Security enforcement / scanners / policy engine | Not implemented or run. |
| Source loading | Not approved. |
| Product/Siamese source | Not inspected or activated. |
| GBrain source contents | Not inspected. |
| GBrain / Hermes / Cadence | Not adopted, not executed, not imported, not configured, not dependency-approved, not provider/auth-approved, not Cadence-active, not substrate. |
| Graphify | Not rerun or adopted. |
| Raw generated outputs / `9_artifacts/` contents | Not inspected or modified. |
| Generated-output tracking | Not approved. |
| Source tracking expansion | Not approved. |
| `.gitignore` | Not modified. |
| `.graphifyignore` | Not modified. |
| Git staging/commit/push/force-add/publication | Not performed or approved. |
| P3.3 | Not created or started. |
| P3.5 | Not created or started. |
| P4 / P5 / EXT.* | Not created or started. |

## 27. Decision Limitations
| Limitation | Effect |
| --- | --- |
| Documentation-only decision | No technical enforcement or runtime guard exists because of P3.4. |
| No provider connectivity test | P3.4 has no proof of provider reachability and does not need it. |
| No credential inspection | P3.4 cannot confirm credential existence or validity and does not seek to. |
| No API/network/MCP execution | P3.4 cannot confirm endpoint, provider, or MCP behavior. |
| No validation execution | P3.4 relies on readiness records and document inspection only. |
| No security enforcement implementation | P3.4 relies on security policy/readiness constraints only. |
| No source loading | P3.4 does not evaluate raw source or product/external contents. |
| No generated output inspection | P3.4 does not inspect raw Graphify or `9_artifacts/` outputs. |
| GBrain path absent and EXT.GB-01 absent | GBrain remains path/class metadata only with pending external-source review. |
| P3.3 absent | Tool execution remains governed by existing P1.3/S-04/GT-07 blockers; no P3.3 alignment is required for this P3.4 non-activation decision. |

## 28. Final Verdict
| Question | Answer |
| --- | --- |
| What did P3.4 decide? | Provider/auth/API/MCP activation is deferred by default: `provider_auth_api_mcp_activation_deferred`. |
| Did P3.4 activate providers, auth, APIs, network, MCP, live connectors, model/provider calls, or provider-bound context transmission? | No. |
| Did P3.4 approve credentials, secrets, API keys, token stores, browser auth, local credential stores, `.env`, or provider configs? | No. |
| Did P3.4 approve a future candidate? | Yes, only `candidate_for_future_exact_activation: provider metadata registry only`. |
| Does that future candidate authorize implementation? | No. It requires a later exact implementation ticket and gates. |
| Did P3.4 inspect product source, external source contents, GBrain contents, or generated raw outputs? | No. |
| Did P3.4 approve Graphify adoption or Cognitive Semantic System substrate selection? | No. Cognitive Semantic System substrate remains deferred. |
| What remains active? | Provider/auth/API/MCP, credential, network, MCP, product, external, GBrain/Hermes/Cadence, generated-output, source tracking, publication, runtime, tool, agent, Graphify, and substrate blockers remain active. |
| Recommended next ticket | P3.5 only if explicitly requested later; P3.4 does not start P3.5. |

Stop rule: After completing P3.4, STOP. Do not start P3.3, P3.5, P3.BR, P4, P5, EXT.* files, implementation, activation, validation execution, security enforcement, source loading, provider/auth/API/MCP calls, MCP activation, live connectors, Graphify, product work, generated-output tracking, source tracking expansion, Git staging, commit, push, force-add, or publication.
