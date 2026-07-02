# Registry Record Format

## ValidationRecord Fields
| field | required | meaning |
| --- | --- | --- |
| `record_id` | yes | Unique validation record ID. |
| `target_id` | yes | Target being evaluated. |
| `claim` | yes | Scope-bound claim being evaluated. |
| `status` | yes | Registry status for this record. |
| `proof_level` | yes | Proof level PL-0 through PL-8. |
| `evidence_refs` | yes | Evidence reference IDs or paths, not raw source contents. |
| `limitations` | yes | Known limitations retained with the record. |
| `blockers` | yes | Known blockers retained with the record. |
| `created_by` | yes | Creator identifier. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## Proof Levels
Allowed proof levels: PL-0, PL-1, PL-2, PL-3, PL-4, PL-5, PL-6, PL-7, PL-8.

## Statuses
Allowed statuses: `draft`, `evidence_recorded`, `blocked`, `validated_for_scope`, `rejected_for_scope`, and `needs_review`.

## Evidence Reference Rules
Evidence references must be references or IDs only. Evidence references must not copy raw source contents, secrets, credentials, generated outputs, or product source into the registry.

## Blocker Rules
Blockers must be retained. A status change does not erase blockers. Blockers remain visible for governance review.

## Limitation Rules
Limitations must be retained. A validation record remains scope-bound and cannot claim broader readiness than its recorded limitations allow.

## Review-required Rule
`review_required` defaults to true. `validated_for_scope` still requires governance interpretation and does not bypass review.

## Non-approval Semantics
Validation registry status is not governance approval. Proof level is not authorization. The registry cannot approve execution, source tracking, dependency adoption, provider activation, product activation, publication, implementation readiness, or security exceptions.
