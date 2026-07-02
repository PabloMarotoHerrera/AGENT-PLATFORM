# Tool Execution Contract

## ToolDescriptor Fields
| field | required | meaning |
| --- | --- | --- |
| `tool_id` | yes | Unique tool metadata ID. |
| `name` | yes | Tool display name. |
| `tool_kind` | yes | Declared tool kind. |
| `description` | yes | Metadata description. |
| `activation_status` | yes | Activation posture metadata. |
| `allowed_scope` | yes | Declared allowed metadata scope. |
| `forbidden_scope` | yes | Declared forbidden scope. |
| `side_effects` | yes | Declared side effects. |
| `filesystem_required` | yes | Filesystem requirement flag. |
| `shell_required` | yes | Shell requirement flag. |
| `network_required` | yes | Network requirement flag. |
| `credential_required` | yes | Credential requirement flag. |
| `provider_refs` | yes | Provider metadata refs only. |
| `adapter_refs` | yes | Adapter metadata refs only. |
| `mcp_refs` | yes | MCP metadata refs only. |
| `evidence_refs` | yes | Evidence reference IDs only. |
| `limitations` | yes | Known limitations retained with the descriptor. |
| `blockers` | yes | Known blockers retained with the descriptor. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## ToolCapabilityDescriptor Fields
| field | required | meaning |
| --- | --- | --- |
| `capability_id` | yes | Unique capability metadata ID. |
| `tool_id` | yes | Tool descriptor ID. |
| `name` | yes | Capability display name. |
| `description` | yes | Metadata description. |
| `activation_status` | yes | Activation posture metadata. |
| `input_classes` | yes | Declared input classes. |
| `output_classes` | yes | Declared output classes. |
| `side_effects` | yes | Declared side effects. |
| `filesystem_behavior` | yes | Declared filesystem behavior metadata. |
| `shell_behavior` | yes | Declared shell behavior metadata. |
| `network_behavior` | yes | Declared network behavior metadata. |
| `credential_behavior` | yes | Declared credential behavior metadata. |
| `provider_behavior` | yes | Declared provider behavior metadata. |
| `mcp_behavior` | yes | Declared MCP behavior metadata. |
| `evidence_refs` | yes | Evidence reference IDs only. |
| `limitations` | yes | Known limitations retained with the capability. |
| `blockers` | yes | Known blockers retained with the capability. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## ToolExecutionRequest Fields
| field | required | meaning |
| --- | --- | --- |
| `request_id` | yes | Unique request metadata ID. |
| `tool_id` | yes | Tool descriptor ID. |
| `capability_id` | yes | Capability descriptor ID. |
| `requested_by` | yes | Requesting actor metadata ID. |
| `target_id` | yes | Target metadata ID. |
| `intent` | yes | Declared intent. |
| `input_summary` | yes | Safe input summary only. |
| `risk_level` | yes | Declared risk level. |
| `status` | yes | Request status. |
| `context_pack_refs` | yes | Context pack refs only. |
| `validation_refs` | yes | Validation refs only. |
| `security_decision_refs` | yes | Security decision refs only. |
| `agent_task_refs` | yes | Agent task refs only. |
| `provider_adapter_refs` | yes | Provider/adapter refs only. |
| `evidence_refs` | yes | Evidence refs only. |
| `limitations` | yes | Known limitations retained with the request. |
| `blockers` | yes | Known blockers retained with the request. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## ToolExecutionDecision Fields
| field | required | meaning |
| --- | --- | --- |
| `decision_id` | yes | Unique decision metadata ID. |
| `request_id` | yes | Request metadata ID. |
| `status` | yes | Decision status. |
| `reasons` | yes | Decision reasons. |
| `risk_level` | yes | Declared risk level. |
| `limitations` | yes | Known limitations retained with the decision. |
| `blockers` | yes | Known blockers retained with the decision. |
| `evidence_refs` | yes | Evidence refs only. |
| `created_by` | yes | Creator identifier. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## Tool Kinds
Allowed tool kinds: `metadata_tool`, `validation_tool`, `security_tool`, `context_tool`, `agent_metadata_tool`, `provider_adapter_metadata_tool`, `shell_tool`, `filesystem_tool`, `git_tool`, `package_manager_tool`, `build_tool`, `test_runner_tool`, `network_tool`, `provider_api_tool`, `mcp_tool`, `product_tool`, `simulation_tool`, and `unknown`.

## Activation Statuses
Allowed activation statuses: `metadata_only`, `blocked`, `needs_review`, `activation_not_approved`, and `rejected_for_scope`.

## Risk Levels
Allowed risk levels: `metadata_only`, `governance_metadata`, `local_only_risk`, `filesystem_risk`, `shell_risk`, `network_risk`, `credential_risk`, `provider_risk`, `mcp_risk`, `dependency_risk`, `product_risk`, `destructive_risk`, and `unknown`.

## Request Statuses
Allowed request statuses: `draft`, `proposed_for_review`, `blocked`, `needs_review`, `rejected_for_scope`, and `recorded_metadata_only`.

## Decision Statuses
Allowed decision statuses: `metadata_recorded_only`, `execution_not_approved`, `blocked`, `needs_review`, and `rejected_for_scope`.

## Provider/adapter/MCP/context/validation/security/agent Reference Rules
All references are metadata IDs only. They do not activate providers, adapters, MCP, context loading, validation, security enforcement, agents, or tools.

## Evidence Reference Rules
Evidence references must be references or IDs only. Evidence references must not copy raw source contents, secrets, credentials, generated outputs, product source, external source, datasets, models, artifacts, or local-only contents into the boundary.

## Input Summary Rules
Input summaries must be summaries only. Input summaries must not include raw payloads, secrets, credentials, raw source contents, product source, external source, datasets, models, artifacts, or generated-sensitive contents.

## Blocker Rules
Blockers must be retained. Tool, capability, request, and decision records with execution, shell, filesystem, network, credential, provider, MCP, dependency, package, build, test, Git, product, simulation, destructive, or side-effect risk retain blockers for governance/security review.

## Limitation Rules
Limitations must be retained. Tool execution boundary metadata remains limited to declared metadata scope.

## Review-required Rule
`review_required` defaults to true. `metadata_only`, `recorded_metadata_only`, `metadata_recorded_only`, `activation_not_approved`, and `execution_not_approved` still require governance interpretation before future activation or execution.

## Non-activation And Non-execution Semantics
Tool registration is not tool activation. Capability registration is not tool permission. Execution request creation is not execution approval. Execution decision metadata is not execution authorization. Shell availability is not command approval. Tool availability is not permission. Provider/adapter/MCP refs are metadata only. The boundary cannot approve execution, source tracking, dependency adoption, provider activation, MCP activation, product activation, publication, CSS substrate selection, implementation readiness, or security exceptions.
