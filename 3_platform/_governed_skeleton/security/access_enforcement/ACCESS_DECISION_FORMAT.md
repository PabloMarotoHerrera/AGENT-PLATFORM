# Access Decision Format

## AccessRequest Fields
| field | required | meaning |
| --- | --- | --- |
| `request_id` | yes | Unique declared access request ID. |
| `actor_id` | yes | Actor requesting the action. |
| `action` | yes | Declared action category. |
| `target` | yes | Declared target identifier. |
| `target_sensitivity` | yes | Declared sensitivity level. |
| `purpose` | yes | Declared purpose. |
| `evidence_refs` | yes | Evidence reference IDs or paths, not raw source contents. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |
| `blockers` | yes | Known blockers retained with the request. |

## AccessDecision Fields
| field | required | meaning |
| --- | --- | --- |
| `request_id` | yes | Request ID being evaluated. |
| `status` | yes | Decision status. |
| `reasons` | yes | Decision reasons. |
| `blockers` | yes | Retained and generated blockers. |
| `limitations` | yes | Scope limitations. |
| `review_required` | yes | Review flag. |
| `created_at` | yes | Decision timestamp or timestamp reference. |

## Sensitivity Levels
Allowed sensitivity levels: `public_metadata`, `governance_metadata`, `local_only`, `generated_sensitive`, `secret`, `credential`, and `unknown`.

## Action Categories
Allowed action categories: `read_governance_metadata`, `record_validation_metadata`, `create_governance_artifact`, `inspect_local_only_source`, `read_secret`, `read_credential`, `execute_tool`, `shell_command`, `network_call`, `provider_api_call`, `mcp_activation`, `source_tracking`, `git_mutation`, `force_add`, `publish`, `adopt_dependency`, `activate_product`, `create_runtime`, and `unknown`.

## Decision Statuses
Allowed decision statuses: `allowed_for_metadata_only`, `blocked`, `needs_review`, and `rejected_for_scope`.

## Evidence Reference Rules
Evidence references must be references or IDs only. Evidence references must not copy raw source contents, secrets, credentials, generated outputs, product source, or local-only contents into the evaluator.

## Blocker Rules
Blockers must be retained. `blocked` and `needs_review` decisions preserve reasons and blockers for governance review.

## Limitation Rules
Limitations must be retained. `allowed_for_metadata_only` remains limited to declared metadata scope.

## Review-required Rule
`review_required` defaults to true. Unknown sensitivity requires review. High-risk actions require review or blocking.

## Non-approval Semantics
`allowed_for_metadata_only` is not governance approval and does not authorize execution, source tracking, dependency adoption, provider activation, product activation, publication, CSS substrate selection, implementation readiness, or security exceptions.
