# Semantic Record Contract

## CognitiveEntity Fields
| field | required | meaning |
| --- | --- | --- |
| `entity_id` | yes | Unique cognitive entity metadata ID. |
| `entity_kind` | yes | Declared entity kind. |
| `title` | yes | Entity title. |
| `summary` | yes | Safe summary only. |
| `status` | yes | Semantic record status. |
| `context_refs` | yes | Context metadata refs only. |
| `evidence_refs` | yes | Evidence metadata refs only. |
| `validation_refs` | yes | Validation metadata refs only. |
| `security_refs` | yes | Security metadata refs only. |
| `limitations` | yes | Known limitations retained with the entity. |
| `blockers` | yes | Known blockers retained with the entity. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## SemanticClaim Fields
| field | required | meaning |
| --- | --- | --- |
| `claim_id` | yes | Unique semantic claim metadata ID. |
| `subject_entity_id` | yes | Subject entity metadata ID. |
| `claim` | yes | Scope-bound claim text. |
| `status` | yes | Semantic record status. |
| `evidence_refs` | yes | Evidence metadata refs only. |
| `validation_refs` | yes | Validation metadata refs only. |
| `limitations` | yes | Known limitations retained with the claim. |
| `blockers` | yes | Known blockers retained with the claim. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## SemanticRelation Fields
| field | required | meaning |
| --- | --- | --- |
| `relation_id` | yes | Unique semantic relation metadata ID. |
| `source_entity_id` | yes | Source entity metadata ID. |
| `target_entity_id` | yes | Target entity metadata ID. |
| `relation_kind` | yes | Declared relation kind. |
| `status` | yes | Semantic record status. |
| `evidence_refs` | yes | Evidence metadata refs only. |
| `limitations` | yes | Known limitations retained with the relation. |
| `blockers` | yes | Known blockers retained with the relation. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## SubstrateCandidateRecord Fields
| field | required | meaning |
| --- | --- | --- |
| `candidate_id` | yes | Unique substrate candidate metadata ID. |
| `candidate_kind` | yes | Declared substrate candidate kind. |
| `name` | yes | Candidate display name. |
| `description` | yes | Candidate description. |
| `decision_status` | yes | Candidate-only decision posture. |
| `evidence_refs` | yes | Evidence metadata refs only. |
| `limitations` | yes | Known limitations retained with the candidate. |
| `blockers` | yes | Known blockers retained with the candidate. |
| `created_at` | yes | Creation timestamp or timestamp reference. |
| `review_required` | yes | Governance review flag, default true. |

## Semantic Entity Kinds
Allowed entity kinds: `goal`, `task`, `context_pack`, `evidence`, `claim`, `action`, `recommendation`, `output`, `validation_record`, `security_decision`, `agent_record`, `tool_record`, `provider_adapter_record`, `product_governance`, `implementation_artifact`, `governance_decision`, `substrate_candidate`, and `unknown`.

## Semantic Relation Kinds
Allowed relation kinds: `supports`, `contradicts`, `refines`, `depends_on`, `derived_from`, `contextualizes`, `constrains`, `validates_scope`, `security_limits`, `blocks`, `supersedes`, `candidate_for`, and `unknown`.

## Semantic Record Statuses
Allowed semantic record statuses: `draft`, `candidate`, `linked_for_review`, `blocked`, `needs_review`, `rejected_for_scope`, and `recorded_metadata_only`.

## Substrate Candidate Kinds
Allowed substrate candidate kinds: `graph_candidate`, `vector_index_candidate`, `relational_store_candidate`, `document_index_candidate`, `ontology_candidate`, `hybrid_candidate`, `memory_only_candidate`, and `unknown`.

## Substrate Decision Statuses
Allowed substrate decision statuses: `candidate_only`, `deferred`, `blocked`, `needs_review`, and `rejected_for_scope`.

## Context/evidence/validation/security Reference Rules
Context refs, evidence refs, validation refs, and security refs must be metadata IDs only. They do not load sources, validate claims, enforce security, select substrate, or approve permissions.

## Blocker Rules
Blockers must be retained. Blocked, review-required, deferred, and candidate-only records preserve blockers for governance review.

## Limitation Rules
Limitations must be retained. Semantic metadata remains limited to declared scope.

## Review-required Rule
`review_required` defaults to true. Candidate-only, deferred, recorded-metadata-only, linked-for-review, blocked, and needs-review records still require governance interpretation.

## Non-truth, Non-validation, Non-reasoning, And Non-selection Semantics
Semantic entity registration is not truth creation. Semantic claim registration is not validation. Semantic relation registration is not reasoning execution. Substrate candidate registration is not substrate selection. Graph candidate metadata is not graph adoption. Graphify evidence metadata is not Graphify authority. Validation evaluates; governance decides.
