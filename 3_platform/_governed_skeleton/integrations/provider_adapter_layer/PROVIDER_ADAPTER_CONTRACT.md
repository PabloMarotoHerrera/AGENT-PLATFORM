# Provider / Adapter Contract

## ProviderDescriptor Fields
| field | required | meaning |
| --- | --- | --- |
| `provider_id` | yes | Unique provider metadata ID. |
| `name` | yes | Provider display name. |
| `provider_kind` | yes | Declared provider kind. |
| `description` | yes | Metadata description. |
| `activation_status` | yes | Activation posture metadata. |
| `auth_required` | yes | Whether auth would be required if later approved. |
| `network_required` | yes | Whether network would be required if later approved. |
| `data_exposure_risk` | yes | Declared exposure risk metadata. |
| `credential_refs` | yes | Credential reference IDs only, not credential values. |
| `evidence_refs` | yes | Metadata evidence references or IDs. |
| `limitations` | yes | Known limitations retained with the descriptor. |
| `blockers` | yes | Known blockers retained with the descriptor. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## AdapterDescriptor Fields
| field | required | meaning |
| --- | --- | --- |
| `adapter_id` | yes | Unique adapter metadata ID. |
| `provider_id` | yes | Provider descriptor ID. |
| `name` | yes | Adapter display name. |
| `adapter_kind` | yes | Declared adapter kind. |
| `description` | yes | Metadata description. |
| `activation_status` | yes | Activation posture metadata. |
| `allowed_scope` | yes | Declared allowed metadata scope. |
| `forbidden_scope` | yes | Declared forbidden scope. |
| `evidence_refs` | yes | Metadata evidence references or IDs. |
| `limitations` | yes | Known limitations retained with the descriptor. |
| `blockers` | yes | Known blockers retained with the descriptor. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## AdapterCapability Fields
| field | required | meaning |
| --- | --- | --- |
| `capability_id` | yes | Unique capability metadata ID. |
| `adapter_id` | yes | Adapter descriptor ID. |
| `name` | yes | Capability display name. |
| `description` | yes | Metadata description. |
| `activation_status` | yes | Activation posture metadata. |
| `input_classes` | yes | Declared input classes. |
| `output_classes` | yes | Declared output classes. |
| `side_effects` | yes | Declared side effects. |
| `network_behavior` | yes | Declared network behavior metadata. |
| `credential_behavior` | yes | Declared credential behavior metadata. |
| `evidence_refs` | yes | Metadata evidence references or IDs. |
| `limitations` | yes | Known limitations retained with the capability. |
| `blockers` | yes | Known blockers retained with the capability. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## Provider Kinds
Allowed provider kinds: `llm_provider`, `cloud_provider`, `storage_provider`, `identity_auth_provider`, `package_registry_provider`, `telemetry_analytics_provider`, `hosting_deployment_provider`, `simulation_solver_provider`, `omniverse_nucleus_provider`, `data_ingestion_provider`, `notification_provider`, `local_service_provider`, and `unknown`.

## Adapter Kinds
Allowed adapter kinds: `provider_api_adapter`, `local_tool_adapter`, `shell_command_adapter`, `file_system_adapter`, `git_adapter`, `validation_adapter`, `security_adapter`, `product_backend_adapter`, `omniverse_adapter`, `energyplus_adapter`, `web_platform_adapter`, `desktop_adapter`, `cli_adapter`, `mcp_adapter`, and `unknown`.

## Activation Statuses
Allowed activation statuses: `metadata_only`, `blocked`, `needs_review`, `activation_not_approved`, and `rejected_for_scope`.

## Credential Reference Rules
Credential references must be metadata references or IDs only. Credential references must not contain secrets, tokens, API keys, cookies, auth sessions, or provider config contents.

## Network/Auth Rules
`network_required=True` and `auth_required=True` require review and blockers. Network-required metadata is not network approval. Auth-required metadata is not auth approval.

## Evidence Reference Rules
Evidence references must be references or IDs only. Evidence references must not copy raw source contents, secrets, credentials, generated outputs, product source, external source, datasets, models, artifacts, or local-only contents into the layer.

## Blocker Rules
Blockers must be retained. Activation blockers remain visible for governance/security review.

## Limitation Rules
Limitations must be retained. Provider, adapter, and capability metadata remain limited to declared metadata scope.

## Review-required Rule
`review_required` defaults to true. `metadata_only` and `activation_not_approved` still require governance interpretation before future activation.

## Non-activation Semantics
Provider registration is not provider activation. Adapter registration is not adapter activation. Capability registration is not tool execution. MCP adapter metadata is not MCP activation. The layer cannot approve execution, source tracking, dependency adoption, provider activation, MCP activation, product activation, publication, CSS substrate selection, implementation readiness, or security exceptions.
