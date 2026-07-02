# Context Pack Format

## ContextSourceRef Fields
| field | required | meaning |
| --- | --- | --- |
| `source_id` | yes | Unique source reference ID. |
| `source_type` | yes | Declared source type. |
| `title` | yes | Human-readable source title. |
| `reference` | yes | Metadata reference or ID, not raw contents. |
| `sensitivity` | yes | Declared sensitivity. |
| `allowed_for_context` | yes | Context-use flag, not source tracking approval. |
| `limitations` | yes | Known limitations retained with the source. |
| `blockers` | yes | Known blockers retained with the source. |
| `created_at` | yes | Creation timestamp or timestamp reference. |

## ContextItem Fields
| field | required | meaning |
| --- | --- | --- |
| `item_id` | yes | Unique context item ID. |
| `source_id` | yes | Source reference ID. |
| `target_id` | yes | Target or task ID. |
| `claim` | yes | Scope-bound claim. |
| `summary` | yes | Safe summary only, not raw source content. |
| `sensitivity` | yes | Declared sensitivity. |
| `evidence_refs` | yes | Metadata references or IDs, not raw contents. |
| `limitations` | yes | Known limitations retained with the item. |
| `blockers` | yes | Known blockers retained with the item. |
| `status` | yes | Context item status. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## ContextPack Fields
| field | required | meaning |
| --- | --- | --- |
| `pack_id` | yes | Unique context pack ID. |
| `target_id` | yes | Target or task ID. |
| `purpose` | yes | Declared pack purpose. |
| `item_ids` | yes | Context item IDs. |
| `status` | yes | Context pack status. |
| `limitations` | yes | Known limitations retained with the pack. |
| `blockers` | yes | Known blockers retained with the pack. |
| `created_by` | yes | Creator identifier. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## Source Types
Allowed source types: `governance_document`, `architecture_record`, `validation_record`, `security_decision`, `product_governance`, `implementation_record`, `external_metadata`, `migration_metadata`, `safe_summary`, and `unknown`.

## Sensitivity Levels
Allowed sensitivity levels: `public_metadata`, `governance_metadata`, `safe_summary`, `local_only`, `generated_sensitive`, `secret`, `credential`, `raw_product_source`, `raw_external_source`, `dataset`, `model`, `artifact`, and `unknown`.

## Item Statuses
Allowed item statuses: `draft`, `candidate`, `included_for_review`, `blocked`, `rejected_for_scope`, and `needs_review`.

## Pack Statuses
Allowed pack statuses: `draft`, `assembled_for_review`, `blocked`, `rejected_for_scope`, and `needs_review`.

## Evidence Reference Rules
Evidence references must be references or IDs only. Evidence references must not copy raw source contents, secrets, credentials, generated outputs, product source, external source, datasets, models, artifacts, or local-only contents into the runtime.

## Blocker Rules
Blockers must be retained. Blocked and review-required context records preserve blockers for governance review.

## Limitation Rules
Limitations must be retained. Context packs remain limited to declared metadata scope.

## Review-required Rule
`review_required` defaults to true. `included_for_review` and `assembled_for_review` still require governance interpretation.

## Non-permission Semantics
Context inclusion is not permission. Context inclusion is not source tracking. Context inclusion is not migration. The runtime cannot approve execution, dependency adoption, provider activation, product activation, publication, CSS substrate selection, implementation readiness, or security exceptions.
