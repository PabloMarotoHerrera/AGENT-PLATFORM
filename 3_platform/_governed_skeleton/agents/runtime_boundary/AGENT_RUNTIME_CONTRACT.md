# Agent Runtime Contract

## AgentDescriptor Fields
| field | required | meaning |
| --- | --- | --- |
| `agent_id` | yes | Unique agent metadata ID. |
| `name` | yes | Agent display name. |
| `agent_kind` | yes | Declared agent kind. |
| `description` | yes | Metadata description. |
| `activation_status` | yes | Activation posture metadata. |
| `allowed_scope` | yes | Declared allowed metadata scope. |
| `forbidden_scope` | yes | Declared forbidden scope. |
| `provider_refs` | yes | Provider metadata reference IDs only. |
| `adapter_refs` | yes | Adapter metadata reference IDs only. |
| `tool_refs` | yes | Tool metadata reference IDs only. |
| `context_pack_refs` | yes | Context pack metadata reference IDs only. |
| `evidence_refs` | yes | Evidence reference IDs only. |
| `limitations` | yes | Known limitations retained with the descriptor. |
| `blockers` | yes | Known blockers retained with the descriptor. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## AgentCapabilityDescriptor Fields
| field | required | meaning |
| --- | --- | --- |
| `capability_id` | yes | Unique capability metadata ID. |
| `agent_id` | yes | Agent descriptor ID. |
| `name` | yes | Capability display name. |
| `description` | yes | Metadata description. |
| `activation_status` | yes | Activation posture metadata. |
| `input_classes` | yes | Declared input classes. |
| `output_classes` | yes | Declared output classes. |
| `side_effects` | yes | Declared side effects. |
| `tool_required` | yes | Tool requirement flag. |
| `provider_required` | yes | Provider requirement flag. |
| `context_required` | yes | Context requirement flag. |
| `evidence_refs` | yes | Evidence reference IDs only. |
| `limitations` | yes | Known limitations retained with the capability. |
| `blockers` | yes | Known blockers retained with the capability. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## AgentTaskEnvelope Fields
| field | required | meaning |
| --- | --- | --- |
| `task_id` | yes | Unique task envelope ID. |
| `agent_id` | yes | Agent descriptor ID. |
| `target_id` | yes | Target or task target ID. |
| `intent` | yes | Declared intent metadata. |
| `status` | yes | Task envelope status. |
| `context_pack_refs` | yes | Context pack reference IDs only. |
| `validation_refs` | yes | Validation reference IDs only. |
| `security_decision_refs` | yes | Security decision reference IDs only. |
| `provider_adapter_refs` | yes | Provider/adapter reference IDs only. |
| `tool_refs` | yes | Tool reference IDs only. |
| `blockers` | yes | Known blockers retained with the task. |
| `limitations` | yes | Known limitations retained with the task. |
| `created_by` | yes | Creator identifier. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## AgentHandoffRecord Fields
| field | required | meaning |
| --- | --- | --- |
| `handoff_id` | yes | Unique handoff metadata ID. |
| `from_agent_id` | yes | Source agent descriptor ID. |
| `to_agent_id` | yes | Destination agent descriptor ID. |
| `task_id` | yes | Task envelope ID. |
| `reason` | yes | Declared handoff reason. |
| `status` | yes | Handoff status. |
| `context_pack_refs` | yes | Context pack reference IDs only. |
| `evidence_refs` | yes | Evidence reference IDs only. |
| `blockers` | yes | Known blockers retained with the handoff. |
| `limitations` | yes | Known limitations retained with the handoff. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## Agent Kinds
Allowed agent kinds: `governance_agent`, `validation_agent`, `security_agent`, `context_agent`, `provider_adapter_agent`, `tool_boundary_agent`, `product_agent`, `implementation_agent`, `review_agent`, `orchestration_agent`, and `unknown`.

## Activation Statuses
Allowed activation statuses: `metadata_only`, `blocked`, `needs_review`, `activation_not_approved`, and `rejected_for_scope`.

## Task Statuses
Allowed task statuses: `draft`, `proposed_for_review`, `blocked`, `needs_review`, `rejected_for_scope`, and `recorded_metadata_only`.

## Handoff Statuses
Allowed handoff statuses: `draft`, `proposed_for_review`, `blocked`, `needs_review`, `rejected_for_scope`, and `recorded_metadata_only`.

## Provider/adapter/tool/context Reference Rules
Provider refs, adapter refs, tool refs, and context pack refs must be metadata references or IDs only. They do not activate providers, adapters, tools, MCP, context loading, or execution.

## Evidence Reference Rules
Evidence references must be references or IDs only. Evidence references must not copy raw source contents, secrets, credentials, generated outputs, product source, external source, datasets, models, artifacts, or local-only contents into the boundary.

## Blocker Rules
Blockers must be retained. Agents, capabilities, task envelopes, and handoff records with activation, execution, tool, provider, network, credential, orchestration, or side-effect risk retain blockers for governance/security review.

## Limitation Rules
Limitations must be retained. Agent runtime metadata remains limited to declared metadata scope.

## Review-required Rule
`review_required` defaults to true. `metadata_only`, `recorded_metadata_only`, and `activation_not_approved` still require governance interpretation before future activation or execution.

## Non-activation And Non-execution Semantics
Agent registration is not agent activation. Task envelope creation is not task execution. Handoff record creation is not handoff execution. Capability registration is not tool permission. Provider/adapter refs are metadata only. Tool refs are metadata only. The boundary cannot approve execution, source tracking, dependency adoption, provider activation, MCP activation, product activation, publication, CSS substrate selection, implementation readiness, or security exceptions.
