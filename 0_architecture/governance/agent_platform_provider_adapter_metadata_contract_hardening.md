# P1.2 - Provider Adapter Metadata Contract Hardening

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | Provider Adapter Metadata Contract Hardening |
| Ticket | P1.2 |
| Status | Accepted provider adapter metadata contract hardening |
| Date | 2026-07-04 |
| Scope | Harden the metadata-only provider/adapter contract for AGENT PLATFORM / Siamese so future context records, tools, agents, validation records, security records, Cognitive Semantic System records, and Siamese product-readiness records can reference providers and adapters safely. |
| Authority | Provider/adapter metadata contract hardening only, not provider activation, adapter activation, auth approval, credential approval, API approval, MCP activation, network permission, context source loading, source tracking approval, tool execution approval, agent execution approval, product activation, Graphify adoption, or Cognitive Semantic System substrate selection. |
| Related documents | P0.1 Activation Gate Enforcement Map, P0.2 Validation Execution Gate Design, P0.3 Security Enforcement Hardening Plan, G-01 Activation Gate Charter, G-19 Hybrid Parallel Work Packet Dependency Map, I-A Implementation Audit, I-04 Provider / Adapter Layer, I-03 Context Pack Runtime, I-01 Validation Registry Implementation, I-02 Security / Access Enforcement, I-05 Agent Runtime Boundary, I-06 Tool Execution Boundary, I-07 Cognitive Semantic System Prototype, S-03 Local-only / Secrets / Credentials Policy, S-04 Tool / Shell / Network / MCP Execution Policy, CSS ADR/audit, Graphify Repo Map Summary, `.gitignore`, `.graphifyignore`, README.md, and P1.1 Context Runtime Contract Hardening because it exists. |
| Output | Provider adapter metadata contract hardening. |

This document is the canonical Provider Adapter Metadata Contract Hardening record for AGENT PLATFORM / Siamese. Provider adapter metadata contract hardening is not provider runtime activation.

## 2. Purpose

P0.1 mapped activation gates and confirmed that AGENT PLATFORM remains gated by exact-scope governance controls. P0.2 defined validation execution gate design without running validation. P0.3 defined security enforcement hardening without implementing runtime enforcement.

P1.2 hardens provider/adapter metadata contracts so future lanes can reference providers safely without treating metadata as activation, auth approval, API access, MCP activation, network permission, credential approval, tool execution, agent execution, context source loading, or product activation.

P1.2 does not activate providers. P1.2 does not activate adapters. P1.2 does not configure auth. P1.2 does not approve API, network, or MCP use. P1.2 does not inspect credentials or secrets. P1.2 does not start P1.3 or P2.1.

AGENT PLATFORM remains pre-active at AL-1. Validation evaluates; governance decides.

## 3. Current Provider / Adapter Posture

| Area | Current posture | P1.2 result |
| --- | --- | --- |
| Activation level | AGENT PLATFORM remains pre-active at AL-1 metadata skeleton. | No promotion. |
| Provider/adapter layer | Metadata-only by I-04 implementation record. | Contract hardening only. |
| Provider descriptors | Provider descriptors are not live provider instances. | Preserve non-activation semantics. |
| Adapter descriptors | Adapter descriptors are not runtime adapters. | Preserve non-runtime semantics. |
| Provider capabilities | Provider capabilities are not permission to call providers. | Preserve blockers and review requirements. |
| Auth requirements | Auth requirements are not auth approval. | Preserve secure review gates. |
| Network requirements | Network requirements are not network approval. | Preserve GT-08 and security blockers. |
| Credential refs | Credential refs are metadata only. | Values remain prohibited. |
| Provider-bound context transmission | Not approved. | Requires future gate approval. |

Credential refs must never contain secret values. Provider-bound context transmission is not approved. AGENT PLATFORM remains pre-active at AL-1.

## 4. Provider Adapter Metadata Contract Definition

A provider adapter metadata contract is a metadata contract that defines how provider descriptors, adapter descriptors, capabilities, auth requirements, network requirements, credential references, activation blockers, evidence references, validation references, security references, limitations, and retention posture are represented without authorizing provider activation, adapter activation, credential use, API calls, network calls, MCP activation, tool execution, agent execution, or product activation.

| Clarification | Rule |
| --- | --- |
| Provider adapter metadata contract hardening is not provider runtime activation. | P1.2 hardens metadata semantics only. |
| Provider metadata is not provider activation. | A provider record cannot call, connect, authenticate, transmit, or execute. |
| Adapter metadata is not adapter activation. | An adapter record cannot route, execute, invoke, or connect. |
| API key availability is not API key approval. | Credential existence or local availability never authorizes use. |
| Credential refs are metadata only. | Credential refs must be redacted IDs or categories, never values. |
| Network requirements are metadata only. | Endpoint or network need descriptions do not grant permission. |
| MCP requirements are metadata only. | MCP server/tool/resource references do not activate MCP. |
| Provider-bound context transmission requires future approval. | GT-08, GT-05, GT-04, retention posture, and rollback planning are required before any transmission. |
| Provider metadata is not context source loading approval. | Context refs remain metadata and cannot become raw source reads. |
| Provider metadata is not tool execution approval. | GT-07 remains required for tool, shell, package, build, test, network, or Git actions. |
| Provider metadata is not agent execution approval. | Future agent activation gates remain required. |
| Provider metadata is not Cognitive Semantic System substrate selection. | Cognitive Semantic System substrate remains deferred. |

No provider/auth/API/MCP activation is approved by P1.2.

## 5. Provider Object Model

| Object | Meaning | Required fields | Forbidden fields | Security posture | Validation posture |
| --- | --- | --- | --- | --- | --- |
| ProviderDescriptor | Metadata record for a provider candidate or known provider surface. | `provider_id`, `provider_name`, `provider_kind`, `provider_owner`, `provider_scope`, `provider_status`, `provider_capabilities`, `adapter_refs`, `auth_requirements`, `network_requirements`, `mcp_requirements`, `credential_refs`, `activation_state`, `activation_blockers`, `evidence_refs`, `validation_refs`, `security_refs`, `retention_posture`, `review_required`, `limitations` | API keys, tokens, passwords, secret values, raw configs, live sessions, provider outputs | Security refs constrain and blockers persist. | Future completeness and blocker validation only. |
| AdapterDescriptor | Metadata record for a possible provider-facing or provider-adjacent adapter. | `adapter_id`, `provider_id`, `adapter_name`, `adapter_kind`, `adapter_owner`, `adapter_scope`, `adapter_status`, `supported_operations`, `activation_blockers`, `evidence_refs`, `validation_refs`, `security_refs`, `review_required`, `limitations` | Runtime code, callable objects, commands, live handles, auth sessions, raw outputs | Adapter metadata cannot grant execution or auth. | Future completeness and non-activation checks only. |
| ProviderCapability | Metadata record for an operation a provider may support later. | `capability_id`, `provider_id`, `capability_name`, `capability_kind`, `input_metadata_contract`, `output_metadata_contract`, `auth_requirements`, `network_requirements`, `risk_level`, `activation_blockers` | Executable payloads, prompts containing secrets, raw provider responses | Capability metadata is not permission. | Future risk/blocker validation only. |
| ProviderConstraint | Metadata record for limits on provider use. | `constraint_id`, `provider_id`, `constraint_kind`, `constraint_scope`, `required_gate`, `blockers`, `limitations` | Bypass instructions or unscoped permission language | Constraints block by default when unknown. | Future constraint preservation validation only. |
| AuthRequirement | Metadata record describing auth need. | `auth_requirement_id`, `provider_id`, `auth_type`, `auth_scope`, `credential_ref_ids`, `approval_gate`, `security_review_required`, `validation_review_required`, `blockers` | Secret values, token values, password values, session material | Auth metadata does not approve auth. | Future metadata completeness only. |
| NetworkRequirement | Metadata record describing network/API need. | `network_requirement_id`, `provider_id`, `network_kind`, `endpoint_classification`, `allowed_metadata_use`, `forbidden_use`, `approval_gate`, `blockers` | Live endpoint credentials, request payloads, responses, auth headers | Network metadata does not approve network. | Future blocker and gate-reference validation only. |
| MCPRequirement | Metadata record describing MCP need. | `mcp_requirement_id`, `provider_id`, `mcp_server_ref`, `mcp_capability_refs`, `mcp_scope`, `approval_gate`, `blockers` | MCP auth, live server handles, resource payloads, invoked tool outputs | MCP metadata does not activate MCP. | Future MCP blocker validation only. |
| CredentialRef | Redacted metadata reference to credential need or class. | `credential_ref_id`, `provider_id`, `credential_kind`, `credential_owner`, `storage_classification`, `sensitivity`, `local_only`, `secret_related`, `credential_related`, `approval_gate`, `review_required`, `blockers` | Credential values, token values, API key values, private keys, refresh tokens, browser auth, `.env` content | Never content; safe metadata only. | Future redaction invariant only; no value validation. |
| ProviderEndpointRef | Metadata reference to endpoint class or category. | `endpoint_ref_id`, `provider_id`, `endpoint_kind`, `endpoint_classification`, `network_requirement_id`, `approval_gate`, `limitations` | Live credentials, secret query params, request bodies, response bodies | Endpoint ref is not API call approval. | Future endpoint metadata completeness only. |
| ProviderConfigRef | Metadata reference to config need or config class. | `config_ref_id`, `provider_id`, `config_kind`, `config_owner`, `storage_classification`, `local_only`, `approval_gate`, `blockers` | Raw config contents, provider config files, keys, tokens, account state | Config refs are metadata only and blocked by default. | Future redaction and local-only posture validation only. |
| ProviderActivationBlocker | Explicit provider activation stop condition. | `blocker_id`, `provider_id`, `blocker_type`, `blocker_reason`, `blocked_capabilities`, `blocked_operations`, `required_gate`, `status` | Bypass text, hidden exceptions, broad approvals | Blockers must travel downstream. | Future blocker preservation validation only. |
| ProviderEvidenceRef | Metadata evidence reference. | `evidence_ref_id`, `evidence_type`, `evidence_source`, `evidence_scope`, `evidence_limitations`, `retention_posture` | Raw local-only output, secrets, credential values, provider payloads | Evidence supports, does not authorize. | Future evidence posture validation only. |
| ProviderValidationRef | Metadata reference to validation posture. | `validation_ref_id`, `validation_gate`, `validation_target`, `validation_status`, `proof_level`, `validation_limitations`, `not_executed_reason` | Unapproved command output as authority, secret-bearing output | Validation evaluates; governance decides. | Must cite GT-04 for future execution. |
| ProviderSecurityRef | Metadata reference to security posture. | `security_ref_id`, `security_policy`, `security_scope`, `sensitivity`, `approval_status`, `blockers`, `incident_requirements`, `retention_requirements`, `publication_blockers` | Secret values, credential values, auth material | Security refs constrain and can block; they do not grant permission. | Future blocker and sensitivity validation only. |
| ProviderRetentionRecord | Metadata record for retention, redaction, quarantine, deletion, and publication posture. | `retention_id`, `provider_id`, `retention_class`, `redaction_required`, `quarantine_trigger`, `publication_blocker`, `tracking_requirement`, `incident_route` | Retained secrets, credential values, raw auth, unapproved provider outputs | Retention minimizes exposure. | Future retention field validation only. |
| ProviderLimitation | Metadata record for uncertainty or constrained use. | `limitation_id`, `provider_id`, `description`, `impact`, `review_route`, `created_at` | Claims of unrestricted provider readiness or activation | Limitations remain attached downstream. | Future limitation preservation validation only. |

## 6. ProviderDescriptor Contract

| Field | Required meaning |
| --- | --- |
| `provider_id` | Stable identifier for the provider metadata record. |
| `provider_name` | Human-readable provider name without implying adoption or activation. |
| `provider_kind` | Provider class such as governance metadata, implementation metadata, offline stub, local runtime, hosted API, model provider, MCP provider, external data provider, internal product adapter, credential-bound provider, secret-bound provider, generated-output provider, or unknown. |
| `provider_owner` | Accountable owner or `unknown` with blocker. |
| `provider_scope` | Exact metadata scope for the provider descriptor. |
| `provider_status` | Draft, metadata only, blocked, needs review, activation not approved, rejected for scope, or retired. |
| `provider_capabilities` | Capability refs or summaries, not callable capabilities. |
| `adapter_refs` | Metadata references to AdapterDescriptor records. |
| `auth_requirements` | AuthRequirement refs or `none`. |
| `network_requirements` | NetworkRequirement refs or `none`. |
| `mcp_requirements` | MCPRequirement refs or `none`. |
| `credential_refs` | CredentialRef metadata IDs only. |
| `endpoint_refs` | ProviderEndpointRef metadata IDs only. |
| `config_refs` | ProviderConfigRef metadata IDs only. |
| `context_refs` | Context metadata refs, not context source loading approval. |
| `tool_refs` | Tool metadata refs, not tool execution approval. |
| `agent_refs` | Agent metadata refs, not agent execution approval. |
| `product_refs` | Product-readiness refs, not product activation approval. |
| `activation_state` | Metadata-only activation posture, defaulting to blocked or not approved. |
| `activation_blockers` | ProviderActivationBlocker refs that must travel downstream. |
| `evidence_refs` | Evidence refs that support metadata posture without granting approval. |
| `validation_refs` | Validation posture refs or `none`; no validation execution by P1.2. |
| `security_refs` | Security posture refs that constrain provider metadata and activation. |
| `retention_posture` | Retention, redaction, quarantine, tracking, and publication posture. |
| `review_required` | Review requirement; defaults to true. |
| `limitations` | Known gaps, blocked inferences, and restricted-use statements. |

ProviderDescriptor must never include API keys, tokens, passwords, secret values, live credentials, raw provider configs, runtime sessions, network responses, or provider output content.

## 7. AdapterDescriptor Contract

| Field | Required meaning |
| --- | --- |
| `adapter_id` | Stable identifier for the adapter metadata record. |
| `provider_id` | ProviderDescriptor ID that the adapter metadata references. |
| `adapter_name` | Human-readable adapter name without implying runtime availability. |
| `adapter_kind` | Adapter class such as provider API, local tool, shell, filesystem, Git, validation, security, product backend, Omniverse, EnergyPlus, web, desktop, CLI, MCP, or unknown. |
| `adapter_owner` | Accountable owner or `unknown` with blocker. |
| `adapter_scope` | Exact metadata scope for the adapter descriptor. |
| `adapter_status` | Draft, metadata only, blocked, needs review, activation not approved, rejected for scope, or retired. |
| `supported_operations` | Operation metadata only; not executable operations. |
| `input_contract_refs` | Metadata refs for future input contracts. |
| `output_contract_refs` | Metadata refs for future output contracts. |
| `provider_capability_refs` | ProviderCapability refs the adapter may map to later. |
| `context_requirement_refs` | Context requirement metadata refs, not source loading approval. |
| `tool_requirement_refs` | Tool requirement metadata refs, not tool execution approval. |
| `agent_requirement_refs` | Agent requirement metadata refs, not agent execution approval. |
| `auth_posture` | Auth requirement posture and blockers. |
| `network_posture` | Network/API requirement posture and blockers. |
| `mcp_posture` | MCP requirement posture and blockers. |
| `execution_posture` | Execution not approved by default. |
| `activation_requirements` | Future gate and evidence requirements for any activation request. |
| `activation_blockers` | Activation blockers that must travel downstream. |
| `evidence_refs` | Evidence posture refs. |
| `validation_refs` | Validation posture refs. |
| `security_refs` | Security posture refs. |
| `retention_posture` | Retention and output handling posture. |
| `review_required` | Review requirement; defaults to true. |
| `limitations` | Known gaps and restricted-use statements. |

AdapterDescriptor must never include runtime implementation, executable code, command payloads, live provider handles, live auth sessions, raw provider outputs, or callable endpoint objects.

## 8. Provider Capability Contract

| Field | Required meaning |
| --- | --- |
| `capability_id` | Stable identifier for the capability metadata record. |
| `provider_id` | ProviderDescriptor ID. |
| `capability_name` | Human-readable capability name. |
| `capability_kind` | Capability class such as metadata lookup, generation, embedding, retrieval, storage, notification, simulation, product integration, MCP resource, MCP tool, or unknown. |
| `capability_description` | Safe metadata description of what may be supported in the future. |
| `input_metadata_contract` | Metadata-only description of future input classes. |
| `output_metadata_contract` | Metadata-only description of future output classes. |
| `context_requirements` | Context requirement metadata; not context transmission approval. |
| `auth_requirements` | AuthRequirement refs or `none`. |
| `network_requirements` | NetworkRequirement refs or `none`. |
| `mcp_requirements` | MCPRequirement refs or `none`. |
| `risk_level` | Metadata risk label based on auth, network, MCP, product, local-only, generated-output, credential, and secret sensitivity. |
| `allowed_metadata_use` | Exact allowed metadata-only use. |
| `forbidden_use` | Explicit forbidden uses including execution, provider calls, auth, network, MCP, tool routing, agent routing, and product activation. |
| `activation_blockers` | Blockers that remain until future approval. |
| `evidence_refs` | Evidence refs supporting the metadata claim. |
| `validation_refs` | Validation refs or `none`. |
| `security_refs` | Security refs constraining the capability. |
| `limitations` | Known limitations and uncertainty. |

Capability metadata documents what a provider may support in the future. It does not approve execution, calls, auth, context transmission, tool use, or agent use.

## 9. Auth Requirement And Credential Reference Contract

| AuthRequirement field | Required meaning |
| --- | --- |
| `auth_requirement_id` | Stable identifier for auth metadata. |
| `provider_id` | ProviderDescriptor ID. |
| `auth_type` | Metadata class such as none, API key, OAuth, cloud, registry, browser session, token, certificate, service account, MCP auth, local app auth, or unknown. |
| `auth_scope` | Exact metadata scope and future activation boundary. |
| `credential_ref_ids` | CredentialRef IDs only, never values. |
| `required_for_capabilities` | Capability refs that would require auth in a future gate. |
| `approval_gate` | Required future gate, usually GT-08 plus security review. |
| `security_review_required` | Whether security review is required; defaults to true when auth is not `none`. |
| `validation_review_required` | Whether validation posture review is required before future activation. |
| `forbidden_material` | Material that must never be included, such as secret values and credential values. |
| `blockers` | Current auth blockers. |
| `limitations` | Known auth limitations and uncertainty. |

| CredentialRef field | Required meaning |
| --- | --- |
| `credential_ref_id` | Stable redacted credential metadata identifier. |
| `provider_id` | ProviderDescriptor ID. |
| `credential_kind` | Credential class such as API key, token, OAuth refresh token, cloud credential, registry token, SSH key, cookie, service account, certificate, local app credential, MCP credential, or unknown. |
| `credential_owner` | Accountable owner or `unknown` with blocker. |
| `storage_classification` | Metadata-only storage class, such as local-only, secret store candidate, environment file, browser auth, token store, provider config, unknown, or none. |
| `sensitivity` | Secret, credential, local-only, unknown, or other declared sensitivity. |
| `local_only` | Whether credential material is local-only; true by default for credential-related material. |
| `secret_related` | Whether the ref relates to secret material. |
| `credential_related` | Whether the ref relates to credential material. |
| `allowed_metadata_use` | Exact safe metadata use, such as identifying that a future credential gate is needed. |
| `forbidden_use` | Value inspection, printing, partial reveal, hashing, testing, auth, provider calls, context inclusion, publication, staging, and commit. |
| `approval_gate` | Required future gate and explicit secure approval route. |
| `evidence_refs` | Evidence refs supporting metadata posture only. |
| `validation_refs` | Validation refs or `none`. |
| `security_refs` | Security refs constraining the credential reference. |
| `retention_posture` | Metadata-only retention, redaction, quarantine, and incident posture. |
| `review_required` | Review requirement; defaults to true. |
| `blockers` | Current credential blockers. |
| `limitations` | Known limitations and uncertainty. |

CredentialRef is metadata only. CredentialRef must never include credential value, secret value, token value, API key value, password, private key, refresh token, browser auth data, local credential-store content, or `.env` content. API key availability is not API key approval. Credential existence is not credential-use approval. Credential reference is not auth activation.

## 10. Network, API, And MCP Requirement Contract

| NetworkRequirement field | Required meaning |
| --- | --- |
| `network_requirement_id` | Stable identifier for network/API metadata. |
| `provider_id` | ProviderDescriptor ID. |
| `network_kind` | HTTP, socket, cloud API, model provider API, registry, telemetry, database, webhook, local service, remote service, MCP transport, or unknown. |
| `endpoint_classification` | Endpoint class or category without live credential details. |
| `external_related` | Whether external data, source, or service is implicated. |
| `product_related` | Whether product data or product source is implicated. |
| `allowed_metadata_use` | Exact allowed metadata-only use. |
| `forbidden_use` | Network calls, API calls, auth, endpoint testing, credential use, provider-bound context transmission, and response retention. |
| `approval_gate` | Required future gate, usually GT-08 plus security review. |
| `evidence_refs` | Evidence refs supporting metadata posture. |
| `validation_refs` | Validation refs or `none`. |
| `security_refs` | Security refs constraining network/API use. |
| `review_required` | Review requirement; defaults to true. |
| `blockers` | Current network/API blockers. |
| `limitations` | Known limitations and uncertainty. |

| MCPRequirement field | Required meaning |
| --- | --- |
| `mcp_requirement_id` | Stable identifier for MCP metadata. |
| `provider_id` | ProviderDescriptor ID. |
| `mcp_server_ref` | Metadata ref to an MCP server candidate, not a config or live connection. |
| `mcp_capability_refs` | MCP tool/resource capability refs as metadata only. |
| `mcp_scope` | Exact metadata scope and future activation boundary. |
| `allowed_metadata_use` | Exact allowed metadata-only use. |
| `forbidden_use` | Starting, connecting, listing, authenticating, invoking, registering config, exposing resources, or retaining raw output. |
| `approval_gate` | Required future gate, usually GT-08 plus GT-07/GT-05 as applicable. |
| `evidence_refs` | Evidence refs supporting metadata posture. |
| `validation_refs` | Validation refs or `none`. |
| `security_refs` | Security refs constraining MCP use. |
| `review_required` | Review requirement; defaults to true. |
| `blockers` | Current MCP blockers. |
| `limitations` | Known limitations and uncertainty. |

Network requirement metadata is not network permission. API endpoint metadata is not API call approval. MCP requirement metadata is not MCP activation. No provider/auth/API/MCP activation is approved by P1.2.

## 11. Provider Classification And Risk Model

| Classification | Examples | Allowed AL-1 metadata use | Blocked use | Required gate |
| --- | --- | --- | --- | --- |
| `governance_metadata_provider` | Governance docs, gate records, policy references | Cite metadata posture, blockers, limitations | Treating governance docs as provider activation | Active ticket scope; GT as needed for activation |
| `implementation_metadata_provider` | I-04 provider/adapter implementation record | Cite metadata-only component posture | Reading live implementation source, executing code | GT-01/GT-05/GT-07 as applicable |
| `offline_stub_provider` | Placeholder provider metadata, mock descriptor | Record future possibility and blockers | Treating stub as callable provider | GT-08 before any activation |
| `local_runtime_provider` | Local service candidate, local model/server candidate | Record requirement metadata only | Starting server, connecting, reading state, authenticating | GT-06, GT-08, GT-05, GT-15 |
| `hosted_api_provider` | Hosted API, SaaS endpoint, cloud service | Record endpoint class and auth/network blockers | API calls, auth, payload transmission, endpoint testing | GT-08 plus S-03/S-04 security review |
| `model_provider` | LLM, embedding, generation, evaluation provider | Record capability and data-retention concerns | Prompt calls, embeddings, key use, provider output retention | GT-08 plus output/retention review |
| `mcp_provider` | MCP server/tool/resource candidate | Record MCP need and blockers | Starting, connecting, listing, invoking, registering MCP config | GT-08 plus GT-07/GT-05 |
| `external_data_provider` | External data service, external source API | Record provenance and external boundary metadata | External calls, data ingestion, source copying, external instruction adoption | GT-11 plus GT-08/security review |
| `internal_product_adapter` | Siamese product backend, Omniverse/EnergyPlus adapter planning | Readiness-only metadata and gate requirements | Product source inspection, product execution, product adapter activation | GT-09 plus GT-08/GT-07/security/validation |
| `credential_bound_provider` | Provider requiring credential class | Record credential requirement as redacted metadata | Credential inspection, testing, use, auth flow | GT-08 plus explicit secure approval |
| `secret_bound_provider` | Provider requiring secret material | Record blocker and secure route only | Secret value handling, context inclusion, validation by value | Secure incident/auth route plus GT-08/GT-15 |
| `generated_output_provider` | Generated summaries, curated Graphify summary as evidence source | Cite curated generated evidence with limitations | Raw generated output as authority, publication, tracking | GT-04/GT-12/GT-15 as applicable |
| `unknown_provider` | Unclassified provider or adapter candidate | Mark blocked and require review | Any activation, auth, network, context transmission, tool/agent routing | GT-01/GT-05/GT-08 |

## 12. Provider Activation Blocker Contract

| Field | Required meaning |
| --- | --- |
| `blocker_id` | Stable identifier for the blocker. |
| `provider_id` | ProviderDescriptor ID. |
| `blocker_type` | One of the blocker types listed below or a future governed extension. |
| `blocker_reason` | Human-readable reason that does not reveal secrets or credentials. |
| `blocked_capabilities` | Capability refs blocked by this blocker. |
| `blocked_operations` | Operation metadata blocked by this blocker. |
| `required_gate` | Required gate before the blocker can be reviewed. |
| `required_evidence` | Evidence refs or evidence requirements. |
| `required_validation` | Validation posture requirements. |
| `required_security_review` | Security review requirements. |
| `rollback_requirement` | Rollback requirement before any future activation. |
| `incident_requirement` | Incident handling requirement if the blocker is breached. |
| `status` | Open, blocked, needs review, rejected for scope, superseded, or retired. |
| `limitations` | Known limitations and uncertainty. |

| Blocker type | Meaning |
| --- | --- |
| `missing_governance_approval` | Required governance decision is absent. |
| `missing_security_review` | Required security review is absent. |
| `missing_validation_posture` | Required validation posture is absent. |
| `credential_not_approved` | Credential use is not approved. |
| `auth_not_approved` | Auth is not approved. |
| `network_not_approved` | Network/API use is not approved. |
| `mcp_not_approved` | MCP activation is not approved. |
| `context_transmission_not_approved` | Provider-bound context transmission is not approved. |
| `tool_execution_not_approved` | Tool execution is not approved. |
| `agent_execution_not_approved` | Agent execution is not approved. |
| `product_access_not_approved` | Product source/access/activation is not approved. |
| `source_tracking_not_approved` | Source tracking, staging, commit, push, force-add, or publication is not approved. |
| `unknown_sensitivity` | Sensitivity is unknown or mixed. |
| `generated_output_boundary` | Generated output is local-only or not curated. |
| `local_only_boundary` | Local-only material blocks provider use or publication. |

## 13. Provider Evidence / Validation / Security Reference Contract

| ProviderEvidenceRef field | Required meaning |
| --- | --- |
| `evidence_ref_id` | Stable evidence metadata identifier. |
| `evidence_type` | Architecture record, implementation record, validation record, security record, curated Graphify summary, product readiness metadata, incident record, or other safe metadata evidence. |
| `evidence_source` | Exact source ref or path without embedding raw local-only or secret content. |
| `evidence_scope` | Exact scope supported by the evidence. |
| `evidence_limitations` | Known evidence gaps and blocked inferences. |
| `generated_output_related` | Whether generated output is implicated. |
| `local_only` | Whether evidence is local-only or derived from local-only posture. |
| `retention_posture` | Metadata-only, generated-sensitive, local-only, quarantine, deletion candidate, or unknown. |

| ProviderValidationRef field | Required meaning |
| --- | --- |
| `validation_ref_id` | Stable validation metadata identifier. |
| `validation_gate` | GT-04 reference or `none` when no execution is approved. |
| `validation_target` | Metadata target being evaluated or proposed for future evaluation. |
| `validation_status` | Draft, not executed, proposed, blocked, needs review, rejected for scope, or future accepted evidence. |
| `proof_level` | Proof posture, not activation approval. |
| `validation_limitations` | Validation gaps and restrictions. |
| `not_executed_reason` | Reason validation was not run, when applicable. |

| ProviderSecurityRef field | Required meaning |
| --- | --- |
| `security_ref_id` | Stable security metadata identifier. |
| `security_policy` | S-03, S-04, P0.3, or future security policy reference. |
| `security_scope` | Exact security scope. |
| `sensitivity` | Sensitivity class or highest inherited sensitivity. |
| `approval_status` | Metadata-only security posture, not runtime permission. |
| `blockers` | Security blockers that must travel downstream. |
| `incident_requirements` | Incident handling requirements. |
| `retention_requirements` | Redaction, quarantine, deletion, and retention requirements. |
| `publication_blockers` | Publication, Git, and source tracking blockers. |

Evidence, validation, and security refs are references to posture, not approval by themselves.

## 14. Provider / Context Interface

Context may reference provider metadata. Provider metadata may reference context requirements. Context inclusion is not permission.

| Rule | Contract consequence |
| --- | --- |
| Context packets must not contain provider secrets, API keys, tokens, endpoint credentials, auth material, or raw provider configs. | Context records must preserve credential and provider-auth blockers. |
| Provider-bound context transmission is not approved by P1.2. | Future gate approval, security review, validation posture, and retention posture are required. |
| Provider summaries are generated evidence, not authority. | Generated summaries need evidence refs, limitations, and retention posture. |
| Context source refs remain metadata. | Provider metadata cannot convert context refs into source loading approval. |
| Context sensitivity constrains provider use. | Local-only, generated-sensitive, product, external, secret, credential, and unknown sensitivity block provider transmission by default. |

## 15. Provider / Tool Interface

Tools may reference provider metadata, but tool execution is not approved.

| Rule | Contract consequence |
| --- | --- |
| Provider metadata does not authorize tool inputs. | Tool input construction from provider metadata requires future GT-07 posture. |
| Provider capability metadata does not authorize tool routing. | Capability records are metadata and blockers must remain attached. |
| Tool requests involving providers require future GT-07 posture and provider/auth review. | Exact action, cwd, inputs, outputs, side effects, rollback, and security review are required. |
| Tool output involving providers requires generated-output classification, validation/security review, and retention posture. | Provider output cannot be retained or promoted by default. |
| Tool access to provider credentials is blocked by default. | Credential refs remain redacted metadata. |
| Tool access to provider network/API/MCP is blocked by default. | Network, API, and MCP gates remain required. |

## 16. Provider / Agent Interface

Agent task/handoff metadata may reference provider descriptors and adapter descriptors.

| Rule | Contract consequence |
| --- | --- |
| Provider reference is not agent execution. | Agent runtime activation requires future gates. |
| Adapter reference is not handoff execution. | Handoff records remain metadata only. |
| Provider availability is not permission to act. | Provider refs cannot authorize task execution, tool execution, auth, network, MCP, or context transmission. |
| Agent provider use requires auth, network, MCP, validation, security, context, and product posture review. | Blockers must be preserved in task and handoff records. |
| Agent handoff must preserve provider blockers, credential blockers, network blockers, and context transmission blockers. | Downstream agents receive the same restrictions and limitations. |

## 17. Provider / Validation Interface

Validation may evaluate provider metadata completeness in the future. Validation may evaluate provider activation blockers in the future. Validation may evaluate credential-ref redaction invariants in the future. Validation may evaluate provider-bound context blockers in the future.

Validation cannot approve provider activation. Validation cannot approve credential use. Validation cannot approve network calls. Validation cannot approve MCP activation. Validation cannot approve source tracking expansion. Validation evidence must cite GT-04. Validation evaluates; governance decides.

## 18. Provider / Security Interface

Security constrains provider metadata, auth requirements, credential refs, network requirements, MCP requirements, provider-bound context transmission, retention, and publication.

| Security rule | Provider contract consequence |
| --- | --- |
| Unknown sensitivity blocks provider activation. | Unknown or mixed sensitivity keeps activation blocked. |
| Secrets and credentials are never provider metadata content. | Credential refs must remain redacted metadata. |
| Product-bound providers remain blocked. | GT-09, security review, validation posture, source tracking posture, and rollback planning are required before activation. |
| External providers remain blocked unless scoped. | External, license, provenance, network, auth, and retention review are required. |
| Generated provider output remains local-only unless curated. | Raw provider output cannot be retained, tracked, or published by default. |
| Provider adapter contracts must consume security refs as blockers, not permissions. | Security review is required before provider/auth/API/MCP activation. |

## 19. Provider / Cognitive Semantic System Interface

Cognitive Semantic System may reference provider metadata as evidence or claim support.

| Rule | Contract consequence |
| --- | --- |
| Provider metadata is not truth by default. | Semantic records require evidence, validation, security refs, blockers, and limitations. |
| Provider metadata cannot select substrate. | Cognitive Semantic System substrate remains deferred. |
| Graph remains candidate only. | Provider-derived graph or semantic records cannot choose graph as final substrate. |
| Provider-derived semantic records require evidence, validation, and security refs. | Records must preserve credential, network, MCP, local-only, product, external, and generated-output blockers. |
| Provider output cannot become authority through semantic inclusion. | Semantic inclusion is not governance approval, truth creation, or activation. |

## 20. Provider / Graphify Interface

Graphify repo map summary is curated generated evidence only. Raw Graphify output under `9_artifacts/` is local-only. Graphify labels are not governance labels. `.graphifyignore` constrains Graphify input but is not permission.

Provider metadata may reference curated Graphify summaries, not raw outputs by default. Graphify evidence cannot become authority through provider metadata inclusion. Graphify evidence cannot approve provider activation. Graphify evidence cannot approve auth, network, MCP, tool, agent, or product use.

## 21. Provider / Siamese Product Interface

Siamese is product vision, not product activation.

| Product rule | Provider contract consequence |
| --- | --- |
| Product source cannot be inspected or loaded by default. | Product-bound provider metadata remains readiness-only. |
| Product providers/adapters cannot be activated by P1.2. | Product provider activation requires future gates. |
| Product readiness planning may reference provider gate requirements. | Readiness records may list blockers and future gate prerequisites. |
| Omniverse/EnergyPlus/provider planning remains readiness-only. | Native/domain execution and product adapters remain blocked. |
| Product-bound provider metadata requires GT-09, security review, validation posture, source tracking posture, and rollback planning before activation. | Internal product adapters must remain blocked until exact scope is approved. |

## 22. Provider Retention And Output Handling

| Retention area | Contract rule |
| --- | --- |
| Provider descriptor retention posture | Retain metadata fields, blockers, limitations, and refs only. |
| Adapter descriptor retention posture | Retain adapter metadata only, never runtime code or callable endpoint objects. |
| Credential-ref retention posture | Retain redacted credential ref metadata only; never values or value-derived identifiers. |
| Auth metadata retention posture | Retain auth requirement categories and blockers only; never sessions, tokens, cookies, or raw auth material. |
| Network metadata retention posture | Retain endpoint classifications and blockers only; never request payloads, responses, auth headers, or live endpoint credentials. |
| MCP metadata retention posture | Retain server/capability refs and blockers only; never MCP auth, resource payloads, or invoked tool outputs. |
| Generated provider summary retention posture | Treat as generated-sensitive unless curated by a future gate; preserve evidence refs and limitations. |
| Local-only retention posture | Local-only material remains excluded by default; safe metadata only when exact future scope allows. |
| Redaction rules | Omit unsafe content entirely; do not reveal partial secrets, hashes, fingerprints, prefixes, suffixes, or transformed credential values. |
| Deletion/quarantine triggers | Forbidden material, secret/credential exposure, raw provider config, raw auth, raw provider output, unknown sensitivity, or unapproved local-only material triggers quarantine/removal review. |
| Publication blockers | Local-only, generated-sensitive, product, external, secret, credential, unknown, unreviewed, or provider-auth-related material blocks publication. |
| Source tracking requirements | GT-02 and GT-12 are required before tracking provider metadata derivatives, generated summaries, or curated outputs. |
| Incident response | Stop, report safe metadata only, preserve evidence refs, avoid repeating unsafe content, and require governance/security direction. |

Provider metadata must not retain secret values. Provider metadata must not retain credential values. Provider metadata must not retain live auth material. Provider metadata must not retain raw provider output unless explicitly classified and approved in a future gate. Any accidental inclusion of secrets, credentials, tokens, API keys, or raw auth material must trigger incident handling and quarantine.

## 23. Provider Contract Invariants

| ID | Invariant |
| --- | --- |
| PRV-001 | Provider adapter metadata contract hardening is not provider runtime activation. |
| PRV-002 | Provider metadata is not provider activation. |
| PRV-003 | Adapter metadata is not adapter activation. |
| PRV-004 | API key availability is not API key approval. |
| PRV-005 | Credential refs are metadata only. |
| PRV-006 | Credential refs must never include secret values. |
| PRV-007 | Network requirements are metadata only. |
| PRV-008 | MCP requirements are metadata only. |
| PRV-009 | No provider/auth/API/MCP activation is approved by P1.2. |
| PRV-010 | Provider-bound context transmission requires future gate approval. |
| PRV-011 | Context inclusion is not permission. |
| PRV-012 | Tool use from provider metadata requires GT-07. |
| PRV-013 | Agent use from provider metadata requires future agent activation gates. |
| PRV-014 | Product-bound provider use remains blocked until GT-09. |
| PRV-015 | Validation evaluates; governance decides. |
| PRV-016 | Cognitive Semantic System substrate remains deferred. |
| PRV-017 | Graphify evidence is supporting evidence only, not authority. |
| PRV-018 | AGENT PLATFORM remains pre-active at AL-1. |

## 24. Future Validation Targets

These are future validation targets only. P1.2 does not execute validation.

| Future validation target | Purpose | Required future gate |
| --- | --- | --- |
| Provider required fields completeness | Check ProviderDescriptor required fields. | GT-04 |
| Adapter required fields completeness | Check AdapterDescriptor required fields. | GT-04 |
| Provider capability blocker preservation | Check capability blockers remain attached. | GT-04 |
| Auth requirement metadata completeness | Check auth requirement fields without auth use. | GT-04 plus GT-08 if activation requested |
| Credential-ref redaction invariant | Check CredentialRef records do not include values. | GT-04 plus GT-05; no secret scanning by value |
| No-secret/no-credential provider metadata invariant | Check provider metadata forbids secret and credential content. | GT-04 plus GT-05 |
| API key availability is not approval invariant | Check records preserve non-approval wording. | GT-04 |
| Provider-bound context blocker invariant | Check context transmission blockers require future gate approval. | GT-04 plus GT-08 |
| Network requirement blocker invariant | Check network metadata preserves blockers. | GT-04 plus GT-08 |
| MCP requirement blocker invariant | Check MCP metadata preserves blockers. | GT-04 plus GT-08/GT-07 |
| Tool-bound provider blocker invariant | Check provider-tool refs preserve GT-07 requirement. | GT-04 plus GT-07 |
| Agent-bound provider blocker invariant | Check provider-agent refs preserve agent activation blockers. | GT-04 plus future agent gates |
| Product-bound provider blocker invariant | Check product-bound providers remain blocked until GT-09. | GT-04 plus GT-09 |
| Generated provider output local-only invariant | Check generated provider outputs remain local-only/generated-sensitive unless future gates approve. | GT-04 plus GT-12/GT-15 |
| Graphify evidence boundary invariant | Check Graphify evidence remains supporting evidence only. | GT-04/GT-11 |
| Source tracking posture invariant | Check provider metadata does not approve tracking, staging, commit, push, force-add, or publication. | GT-04 plus GT-12 if tracking requested |

## 25. Future Hardening Candidates

These are future candidates only and are not started by P1.2.

| Candidate ticket | Purpose | P1.2 status |
| --- | --- | --- |
| PRV-HARD-01 — Provider Descriptor Schema Alignment | Align ProviderDescriptor fields across context, validation, security, tool, agent, Cognitive Semantic System, and product-readiness records. | Not started. |
| PRV-HARD-02 — Adapter Descriptor Schema Alignment | Align AdapterDescriptor fields and non-activation semantics across downstream interfaces. | Not started. |
| PRV-HARD-03 — Credential Ref Redaction Contract | Harden redaction requirements and incident routing for CredentialRef metadata. | Not started. |
| PRV-HARD-04 — Provider Capability / Risk Classification Model | Refine capability risk classes and blocker inheritance. | Not started. |
| PRV-HARD-05 — Provider-To-Context / Tool / Agent Boundary Contract | Harden cross-lane provider reference rules. | Not started. |
| PRV-HARD-06 — Provider-Bound Context Transmission Gate Design | Define future gate design for any provider-bound context transmission. | Not started. |
| PRV-HARD-07 — Provider Output Retention & Quarantine Contract | Define generated provider output retention, redaction, quarantine, and publication blockers. | Not started. |

## 26. Created / Not Created Register

| Artifact or action | P1.2 status |
| --- | --- |
| Provider adapter metadata contract hardening document | Created. |
| `0_architecture/governance/agent_platform_provider_adapter_metadata_contract_hardening.md` | Created. |
| Provider runtime code | Not modified. |
| Adapter runtime code | Not modified. |
| Auth configuration | Not created. |
| API key | Not inspected. |
| Credential | Not inspected. |
| Secret | Not inspected. |
| `.env` | Not inspected. |
| Provider config | Not inspected. |
| Token store | Not inspected. |
| Browser auth | Not inspected. |
| Local credential store | Not inspected. |
| Provider connectivity | Not tested. |
| Provider/API/network/MCP call | Not executed. |
| Provider activation | Not approved. |
| Adapter activation | Not approved. |
| Provider/auth/API/MCP activation | Not approved. |
| Context source loading | Not approved. |
| Product source | Not inspected. |
| External source | Not inspected. |
| Tool execution | Not approved. |
| Agent execution | Not approved. |
| Validation command | Not executed. |
| Graphify | Not rerun. |
| `.graphifyignore` | Not modified. |
| `.gitignore` | Not modified. |
| Generated outputs | Not modified or tracked. |
| Cognitive Semantic System substrate | Not selected. |
| P1.3 | Not started. |
| P2.1 | Not started. |
| Git staging/commit/push/force-add/publication | Not authorized or performed. |

## 27. Recommended Next Tickets

After P1.2:

| Ticket | Recommendation |
| --- | --- |
| P1.3 - Tool Execution Boundary Contract Hardening | Recommended actual next ticket after explicit instruction. |
| P1.4 - Agent Runtime Boundary Contract Hardening | Follow with provider/tool/context refs preserved. |
| P1.5 - Cognitive Semantic System Prototype Hardening | Follow while preserving substrate deferral. |
| P2.1 - Shared Metadata Vocabulary Alignment | Follow after enough P1 contracts exist. |

Recommended actual: P1.3 - Tool Execution Boundary Contract Hardening.

Do not start P1.3. Do not start P2.1.

## 28. Final Verdict

| Question | Answer |
| --- | --- |
| What did P1.2 create? | The canonical Provider Adapter Metadata Contract Hardening document. |
| What provider/adapter contract was hardened? | ProviderDescriptor, AdapterDescriptor, ProviderCapability, AuthRequirement, NetworkRequirement, MCPRequirement, CredentialRef, ProviderEndpointRef, ProviderConfigRef, ProviderActivationBlocker, ProviderEvidenceRef, ProviderValidationRef, ProviderSecurityRef, ProviderRetentionRecord, and ProviderLimitation metadata contracts. |
| What ProviderDescriptor fields are required? | `provider_id`, `provider_name`, `provider_kind`, `provider_owner`, `provider_scope`, `provider_status`, `provider_capabilities`, `adapter_refs`, `auth_requirements`, `network_requirements`, `mcp_requirements`, `credential_refs`, `endpoint_refs`, `config_refs`, `context_refs`, `tool_refs`, `agent_refs`, `product_refs`, `activation_state`, `activation_blockers`, `evidence_refs`, `validation_refs`, `security_refs`, `retention_posture`, `review_required`, and `limitations`. |
| What AdapterDescriptor fields are required? | `adapter_id`, `provider_id`, `adapter_name`, `adapter_kind`, `adapter_owner`, `adapter_scope`, `adapter_status`, `supported_operations`, `input_contract_refs`, `output_contract_refs`, `provider_capability_refs`, `context_requirement_refs`, `tool_requirement_refs`, `agent_requirement_refs`, `auth_posture`, `network_posture`, `mcp_posture`, `execution_posture`, `activation_requirements`, `activation_blockers`, `evidence_refs`, `validation_refs`, `security_refs`, `retention_posture`, `review_required`, and `limitations`. |
| What AuthRequirement and CredentialRef fields are required? | AuthRequirement requires `auth_requirement_id`, `provider_id`, `auth_type`, `auth_scope`, `credential_ref_ids`, `required_for_capabilities`, `approval_gate`, `security_review_required`, `validation_review_required`, `forbidden_material`, `blockers`, and `limitations`. CredentialRef requires `credential_ref_id`, `provider_id`, `credential_kind`, `credential_owner`, `storage_classification`, `sensitivity`, `local_only`, `secret_related`, `credential_related`, `allowed_metadata_use`, `forbidden_use`, `approval_gate`, `evidence_refs`, `validation_refs`, `security_refs`, `retention_posture`, `review_required`, `blockers`, and `limitations`. |
| What provider classifications are defined? | `governance_metadata_provider`, `implementation_metadata_provider`, `offline_stub_provider`, `local_runtime_provider`, `hosted_api_provider`, `model_provider`, `mcp_provider`, `external_data_provider`, `internal_product_adapter`, `credential_bound_provider`, `secret_bound_provider`, `generated_output_provider`, and `unknown_provider`. |
| What interfaces were hardened? | Provider/context, provider/tool, provider/agent, provider/validation, provider/security, provider/Cognitive Semantic System, provider/Graphify, and provider/Siamese product interfaces. |
| Did P1.2 activate providers? | No. |
| Did P1.2 activate adapters? | No. |
| Did P1.2 configure provider/auth? | No. |
| Did P1.2 inspect credentials or secrets? | No. |
| Did P1.2 call provider/API/network/MCP? | No. |
| Did P1.2 modify runtime code? | No. |
| Was product source inspected? | No. |
| Was tool/agent execution approved? | No. |
| Was Cognitive Semantic System substrate selected? | No. Cognitive Semantic System substrate remains deferred. |
| What is the next ticket? | P1.3 - Tool Execution Boundary Contract Hardening, after explicit instruction only. |

Stop rule: After completing P1.2, STOP. Do not start P1.3. Do not start P2.1. Do not implement code. Do not run validation. Do not inspect secrets. Do not inspect credentials. Do not configure provider/auth. Do not call provider/API/network/MCP. Do not load source. Do not rerun Graphify. Do not modify generated outputs. Do not stage, commit, push, force-add, or publish.
