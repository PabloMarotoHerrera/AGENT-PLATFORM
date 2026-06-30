# AGENT PLATFORM Prior Graphify Material Normalization Plan

Ticket: CSS-02  
Status: Accepted for normalization planning  
Date: 2026-06-30  
Scope: Prior Graphify-related material classification, normalization, citation, retention, and blocker handling before use in the future Cognitive Semantic System  
Authority: Normalization plan only, not migration execution, actual normalization, implementation, or substrate decision  
Related documents: CSS-00, CSS-01, V-series, S-series, W-series

## 1. Document Header
This document is the canonical CSS-02 plan for handling prior Graphify-related material before it can inform AGENT PLATFORM. It is architecture planning only and creates no normalized records, schemas, registries, code, tools, migration batches, substrate scores, or implementation artifacts.

## 2. Purpose
CSS-02 follows CSS-00 and CSS-01. CSS-00 accepted `Cognitive Semantic System` as the canonical current name and kept the posture that the final substrate remains undecided. CSS-01 defined substrate-neutral evaluation criteria. CSS-02 defines how prior Graphify-related material must be normalized before use. CSS-02 does not normalize files, migrate material, select a substrate, or implement the Cognitive Semantic System.

## 3. Problem Statement
Prior Graphify-related material may contain useful graph, projection, semantic, harness, report, or substrate ideas. It may also contain obsolete names, authority claims, graph-first assumptions, external-source contamination, generated-truth confusion, product/root collapse, and migration risks.

The plan prevents old names becoming current names, old authority claims becoming current authority, graph projections becoming truth, graph candidate evidence becoming final substrate, external graphify source becoming dependency or naming authority, generated material becoming source, wholesale migration, and hidden promotion through restatement.

## 4. Normalization Definition
Normalization is a controlled process that converts prior Graphify-related material into current AGENT PLATFORM vocabulary and evidence posture through classification, source citation, restatement, validation, blocker handling, and governance readiness.

Normalization is not migration execution, acceptance, promotion, source-code reuse, substrate selection, or implementation.

## 5. Material Classes
| Material class | Default status | Allowed handling | Prohibited inference | Required evidence | Blocker condition |
| --- | --- | --- | --- | --- | --- |
| prior internal Graphify naming material | conflicted/historical | Restate name only. | Current system name. | W-02/CSS-00 citation. | Old name used current. |
| prior graph-authority claims | authority risk | Extract concept only. | Graph or Graphify owns truth. | Source path + claim summary. | Authority leakage. |
| prior graph substrate assumptions | substrate risk | Use as candidate evidence. | Final graph substrate. | CSS-01 criteria citation. | Graph chosen by implication. |
| prior graph projection/report material | generated evidence | Retain as projection evidence. | Projection is truth. | Generator/source/provenance. | Missing provenance. |
| prior semantic model material | candidate evidence | Restate under current vocabulary. | Prior model is current authority. | Source class + citations. | Missing classification. |
| prior harness/tooling material using Graphify language | scoped evidence | Normalize terms; defer tooling. | Tooling implementation approval. | Source status + S-04 posture. | Execution/tool adoption implied. |
| external graphify source metadata | external_reference | Cite W-03/W-13 metadata. | Internal dependency/name. | External registry citation. | External review missing. |
| external graphify source claims | external evidence | Restate as external claim. | Source claim is platform truth. | V-05/W-13 citation. | Claim adopted directly. |
| generated graph/projection outputs | generated-sensitive | Cite as generated evidence. | Generated output is source. | V-02 provenance fields. | Source/generator absent. |
| product-scoped Graphify references | product_scoped | Keep inside product scope. | Root substrate/root authority. | V-04 product boundary. | Product-root collapse. |
| migration_evidence Graphify references | migration_evidence | Retain historical rationale. | Current governing rule. | W-02/W-08/V-03 citation. | Treated current. |
| conflicted Graphify references | conflicted | Normalize or defer. | Promotion before correction. | Conflict note + review. | Conflict unresolved. |
| unknown Graphify references | unknown | Block pending classification. | Any current use. | Safe metadata only. | Source class absent. |

## 6. Current Naming Boundary
Accepted current name: `Cognitive Semantic System`.

Rejected as current authority names: `Graphify`, `Platform Graphify`, `Graphify Authority`, `Graphify owns truth`, `graph authority`, `graph as source of truth`, product-derived semantic-system names, and external-source-derived semantic-system names.

Rejected names may appear only when explicitly marked as historical, external, prohibited, or normalization target.

## 7. Vocabulary Normalization Map
| Old or ambiguous wording | Old/ambiguous meaning | Normalized wording | Allowed use | Prohibited use | Required caveat |
| --- | --- | --- | --- | --- | --- |
| Graphify | prior/internal or external label | historical Graphify material | Historical/external label. | Current system name. | Cognitive Semantic System is current. |
| Platform Graphify | old platform name | Cognitive Semantic System | Rejected-name example. | Accepted name. | Historical/prohibited only. |
| Graphify Authority | old authority label | governance-backed authority claim | Rejected-name example. | Current authority name. | Governance decides. |
| Graphify owns truth | old truth claim | evidence, not authority | Prohibited claim example. | Current rule. | Evidence supports. |
| graph owns truth | graph-authority claim | governance decides | Prohibited claim example. | Semantic rule. | Graph cannot approve. |
| graph as source of truth | graph-truth claim | graph candidate evidence | Historical claim. | Final authority. | Substrate undecided. |
| graph memory | memory/projection claim | candidate substrate evidence | Candidate evidence. | Accepted memory system. | Memory is evidence. |
| graph brain | metaphor | graph candidate | Historical metaphor. | Architecture name. | Avoid metaphor authority. |
| knowledge graph platform | product/system label | Cognitive Semantic System | Rejected naming example. | Current name. | Substrate undecided. |
| agent graph | agent relationship graph | graph projection evidence | Projection evidence. | Agent authority. | Agents do not govern. |
| graph substrate | graph candidate | graph candidate | Candidate family. | Final substrate. | Compare via CSS-01. |
| graph projection | generated graph view | generated projection | Evidence. | Truth/source. | Generated output. |
| graph report | generated report | graph projection evidence | Evidence. | Source. | Cite generator. |
| graph evidence | graph-oriented evidence | candidate substrate evidence | Evidence input. | Decision by itself. | Governance required. |
| semantic graph | semantic relation model | graph candidate evidence | Candidate evidence. | Final ontology. | Alternatives open. |
| external graphify source | external source label | external graphify source | External evidence. | Dependency/name. | W-13/V-05 apply. |

## 8. Source Classification Rules
| Classification | Graphify-specific meaning | Required handling | Allowed normalization result | Blocked result | Proof/evidence requirement |
| --- | --- | --- | --- | --- | --- |
| carry_forward | Useful concept survives old wording. | Restate and cite. | normalized_claim_candidate | Direct copy authority. | PL-3/PL-4. |
| scope_limit | Product/domain-only relevance. | Keep scoped. | product_scoped_graphify_reference | Root claim. | PL-2/PL-4 + V-04. |
| migration_evidence | Historical rationale/sequence. | Retain as evidence. | historical_graphify_evidence | Current rule. | PL-2/PL-3. |
| conflicted | Naming/authority/substrate conflict. | Normalize before use. | naming/authority risk record. | Promotion. | PL-4/PL-7. |
| external_reference | Outside-origin evidence. | Use W-13/V-05. | external_graphify_reference | Adoption/execution. | PL-2/PL-4. |
| superseded | Replaced by current authority. | Cite historically. | historical trace. | Current authority. | Replacement citation. |
| unknown/unclassified | Class absent. | Block and classify. | blocked_pending_classification | Any use. | Safe metadata/PL-1. |

## 9. Normalization Status Model
| Status | Meaning | Allowed use | Blocked use | Next action |
| --- | --- | --- | --- | --- |
| unreviewed_graphify_material | Mentioned but not classified. | Gap record. | Restatement/use. | Classify. |
| historical_graphify_evidence | Historical prior label/claim. | Rationale. | Current authority. | Cite limits. |
| graph_candidate_evidence | Graph option evidence. | CSS-01 input. | Final choice. | Compare candidates. |
| projection_evidence | Generated graph/report output. | Support review. | Truth/source. | Cite generator. |
| naming_conflict | Old name conflicts with CSS-00. | Blocker record. | Current naming. | Restate. |
| authority_leakage_risk | Old claim implies authority. | Risk note. | Approval. | Remove authority. |
| substrate_assumption_risk | Graph implied final. | Risk note. | Selection. | Restore neutrality. |
| external_graphify_reference | External source evidence. | Metadata/pattern evidence. | Dependency/adoption. | V-05 review. |
| product_scoped_graphify_reference | Product-only reference. | Product evidence. | Root authority. | V-04 review. |
| normalized_claim_candidate | Restated but unvalidated. | Candidate claim. | Promotion. | Validate. |
| normalized_claim_ready_for_validation | Restated/cited/classified. | Validation input. | Governance approval. | V-series review. |
| blocked_pending_classification | Source status missing. | Blocker only. | Normalization. | Classify. |
| blocked_pending_citation | Provenance absent. | Blocker only. | Use. | Add citation. |
| blocked_pending_security_review | Sensitivity/local-only unclear. | Safe metadata. | Exposure. | Security review. |
| rejected_for_current_use | Unsafe or incompatible. | Historical trace. | Current claim. | Retain/reject. |
| deferred_to_substrate_evaluation | Candidate evidence only. | CSS-01/CSS-A input. | Decision. | Later evaluation. |
| deferred_to_migration_ticket | Needs future migration scope. | Plan input. | Migration now. | Explicit ticket. |

## 10. Normalization Workflow
1. Identify Graphify-related material from existing indexes/policies only.
2. Classify source class.
3. Record source path/reference.
4. Record source status.
5. Record sensitivity/local-only posture.
6. Identify old claim.
7. Identify naming, substrate, and authority risk.
8. Restate claim using current vocabulary.
9. Preserve uncertainty.
10. Attach citation/provenance.
11. Assign proof/evidence posture.
12. Apply blockers.
13. Decide whether material is candidate evidence, deferred, rejected, or ready for later validation.
14. Stop before migration, promotion, implementation, or substrate decision.

## 11. Restatement Rules
Restate concepts, not authority. Preserve source status. Remove old naming, final-substrate assumptions, and graph-truth claims. Keep graph as candidate only. Keep generated projections as generated evidence. Keep external graphify as external evidence only. Cite source and classification. Mark uncertainty and limitations. Preserve local-only posture. Do not wholesale copy.

## 12. Citation And Evidence Requirements
Every normalized claim must include source path/reference, source classification, source status, old claim summary, normalized claim, citation/provenance, sensitivity posture, evidence type, proof level target, limitations, blocker status, reviewer/date, and revalidation trigger.

V-02/V-03 apply: evidence supports; citation is provenance, not truth; migration evidence does not execute migration.

## 13. Proof Level Model
| Proof level | CSS-02 use |
| --- | --- |
| PL-1 | Path/index metadata. |
| PL-2 | Source status/classification. |
| PL-3 | Citation/provenance review. |
| PL-4 | Restatement/coherence review. |
| PL-5 | Scoped path/Git/naming checks only. |
| PL-7 | Normalization audit. |
| PL-8 | Reproduced normalization audit. |

No proof level selects substrate, approves migration, approves product activation, approves external adoption, or replaces governance.

## 14. Graph Candidate Evidence Handling
Graph relationships may be useful evidence. Graph projections may support future evaluation. Graph candidate evidence must be compared against non-graph candidates. Graph evidence must not become final substrate, must be assessed against CSS-01 criteria, must preserve generated-output status, and cannot bypass governance.

## 15. External Graphify Source Handling
The external graphify source remains external evidence and local-only by default. No source code copying, package install, execution, dependency adoption, instruction adoption, internal naming adoption, generated-truth adoption, or substrate decision is authorized. W-13 and V-05 control any later review.

## 16. Migration Boundary
CSS-02 plans normalization only. It performs no migration execution, file movement, source transformation, previous knowledge rewrite, archive creation, or wholesale import. Normalized claims may support later migration planning only after explicit ticket under V-03/W-08 controls.

## 17. Product Boundary
Product-scoped Graphify material remains product-scoped. Product needs cannot decide root substrate. Product generated outputs are not source. Product dependencies do not become root dependencies. No product activation occurs. Product validation is required before product-specific use.

## 18. Security / Local-only Boundary
`previusknowledge/`, `4_external/sources/`, and `2_products/` remain local-only. Secrets and credentials are never copied, retained, summarized, or normalized content. Safe metadata is preferred. Unknown sensitivity escalates. Local-only evidence cannot be published by default.

## 19. Blocker Register
| Blocker | Stop behavior | Required action | Blocks normalization? | Blocks migration? | Blocks substrate decision? |
| --- | --- | --- | --- | --- | --- |
| missing source classification | Stop use. | Classify. | Yes | Yes | Yes |
| missing source path/reference | Stop use. | Locate/cite. | Yes | Yes | Yes |
| missing citation | Stop promotion-quality use. | Add provenance. | Yes | Yes | Yes |
| old naming treated as current | Stop wording. | Restate. | Yes | Yes | Yes |
| Graphify treated as AGENT PLATFORM system name | Stop document. | Replace with current name. | Yes | Yes | Yes |
| graph treated as final substrate | Stop claim. | Restore candidate wording. | Yes | Yes | Yes |
| graph projection treated as truth | Stop claim. | Mark generated evidence. | Yes | Yes | Yes |
| external graphify source treated as dependency | Stop adoption framing. | External review/governance. | Yes | Yes | Yes |
| generated output treated as source | Stop source claim. | Cite generator/source. | Yes | Yes | Yes |
| product-root collapse | Stop root claim. | Scope to product. | Yes | Yes | Yes |
| local-only leakage | Stop exposure. | Safe metadata/security review. | Yes | Yes | Maybe |
| secret/credential risk | Stop immediately. | Secure handling. | Yes | Yes | Yes |
| wholesale copy/migration risk | Stop migration path. | Restate only. | Yes | Yes | Maybe |
| prior canonical label treated as current authority | Stop claim. | Mark historical. | Yes | Yes | Yes |
| missing governance path | Stop readiness claim. | Define decision path. | Maybe | Yes | Yes |
| proof insufficient | Stop support claim. | Add proof or defer. | Maybe | Yes | Yes |
| stale evidence | Stop current use. | Revalidate or mark historical. | Maybe | Yes | Yes |

## 20. Normalization Matrices
### Matrix A. Material Class Vs Allowed Outcome
| Class | normalize | retain as evidence | defer | reject | blocked |
| --- | --- | --- | --- | --- | --- |
| prior naming | Yes, name only | Historical | If unclear | If persistent | Current-name leak |
| authority claim | Concept only | Yes | If conflicted | If unfixable | Authority leak |
| substrate assumption | Candidate only | Yes | To CSS evaluation | If overclaim | Graph-final claim |
| graph projection | Label generated | Yes | If provenance missing | If unsafe | Truth claim |
| semantic model | Restate | Yes | If uncited | If incoherent | Missing citation |
| external graphify | Metadata only | Yes | V-05 | If adoption leak | Execution/copy |
| product-scoped reference | Product scope | Yes | V-04 | If root collapse | Product leak |
| generated output | Generated evidence | Yes | If source absent | If unsafe | Source claim |
| unknown | No | Gap only | Yes | If unsafe | Unclassified |

### Matrix B. Old Wording Vs Normalized Wording
| Old wording | Normalized phrase | Allowed caveat | Prohibited inference |
| --- | --- | --- | --- |
| Graphify | historical Graphify material | Historical/external only. | Current name. |
| Platform Graphify | Cognitive Semantic System | Rejected name only. | Accepted current name. |
| Graphify Authority | governance-backed authority claim | Rejected authority label. | Current authority. |
| Graphify owns truth | evidence, not authority | Prohibited claim. | Truth ownership. |
| graph owns truth | governance decides | Prohibited claim. | Graph approval. |
| graph as source of truth | graph candidate evidence | Substrate undecided. | Final substrate. |
| graph memory | candidate substrate evidence | Memory is evidence. | Accepted memory system. |
| graph brain | graph candidate | Metaphor only. | Architecture name. |
| knowledge graph platform | Cognitive Semantic System | Rejected name. | Current name. |
| agent graph | graph projection evidence | Agents do not govern. | Agent authority. |
| graph substrate | graph candidate | Compare via CSS-01. | Final substrate. |
| graph projection | generated projection | Generated evidence. | Truth/source. |
| graph report | graph projection evidence | Cite generator. | Source. |
| graph evidence | candidate substrate evidence | Governance required. | Decision. |
| semantic graph | graph candidate evidence | Alternatives open. | Final ontology. |
| external graphify source | external graphify source | W-13/V-05 apply. | Dependency/name. |

### Matrix C. Blocker Vs Required Action
| Group | stop | fix | defer | govern | reject |
| --- | --- | --- | --- | --- | --- |
| naming | Yes | Restate current name. | If conflict remains. | CSS/governance. | If old name persists. |
| authority | Yes | Remove approval claim. | If owner missing. | Governance. | If authority leak persists. |
| substrate | Yes | Candidate wording. | CSS evaluation. | Substrate ADR later. | If finality persists. |
| citation | Yes | Add source. | If unavailable. | Exception only. | If unsupported. |
| source status | Yes | Classify. | If unknown. | Migration governance. | If unsafe. |
| external | Yes | V-05/W-13 review. | Yes. | External governance. | If adoption leak. |
| product | Yes | Scope product. | Yes. | Product governance. | If root collapse. |
| security | Yes | Safe metadata/review. | Yes. | Security decision. | If secret leak. |
| migration | Yes | Restate, do not copy. | Explicit ticket. | Migration governance. | If wholesale copy required. |

### Matrix D. CSS-01 Criteria Relationship
| CSS-01 group | How Graphify material may inform | What it cannot decide |
| --- | --- | --- |
| semantic fit | Relationship/model evidence. | Final model. |
| validation/proof | Projection/provenance risks. | Proof sufficiency by itself. |
| governance | Authority-leak examples. | Governance outcome. |
| security/access | Local-only/generated risks. | Security approval. |
| context | Candidate retrieval/projection ideas. | Permission/truth. |
| migration | Normalization blockers. | Migration execution. |
| product/external | Boundary cases. | Root authority/adoption. |
| operations | Runtime/tooling cautions. | Implementation readiness. |
| interoperability | Export/reversibility evidence. | Substrate selection. |

## 21. Incident Handling
Incidents include Graphify name copied as current system name, Graphify authority claim copied into current docs, graph selected by implication, graph projection treated as accepted truth, external graphify code copied, external graphify executed, prior material migrated wholesale, product-scoped material promoted to root, local-only material exposed, secret/credential copied, generated report treated as source, or Git staged local-only Graphify material.

Response: STOP, report safe metadata, do not continue adjacent work, and require human/security/governance decision.

## 22. Normalization Output Template
```markdown
# Normalized Graphify Material Record: <id>
Status: <candidate | blocked | deferred | rejected | ready_for_validation>
Source reference: <path/reference>
Source class: <carry_forward | conflicted | external_reference | etc.>
Source status: <historical | external | local_only | generated | unknown>
Old claim summary: <summary>
Normalized claim: <current vocabulary>
Graph/substrate posture: <candidate only | not applicable | blocked>
Evidence type: <type>
Proof target: <PL-x>
Citations: <references>
Limitations: <limits>
Blockers: <blockers>
Decision needed: <none | governance | validation | security | migration | substrate evaluation>
Stop rule: <rule>
```
This template is illustrative format only and is not instantiated in CSS-02.

## 23. Normalization Invariants
| ID | Invariant |
| --- | --- |
| CSS02-001 | Cognitive Semantic System is the canonical current name. |
| CSS02-002 | Graphify is historical/external evidence, not current authority. |
| CSS02-003 | Normalization does not execute migration. |
| CSS02-004 | Normalization does not approve substrate. |
| CSS02-005 | Graph remains a candidate only. |
| CSS02-006 | Graph projections are evidence, not truth. |
| CSS02-007 | External graphify source remains external. |
| CSS02-008 | Product-scoped material remains product-scoped. |
| CSS02-009 | Prior canonical labels are historical. |
| CSS02-010 | Generated outputs are not source by default. |
| CSS02-011 | Local-only remains no default publication. |
| CSS02-012 | Secrets and credentials are never normalized content. |
| CSS02-013 | Evidence supports; governance decides. |
| CSS02-014 | No wholesale migration. |
| CSS02-015 | No substrate selected. |
| CSS02-016 | Implementation remains blocked. |

## 24. Anti-patterns
Anti-patterns: normalization by copy-paste; normalization by search-and-replace only; Graphify as current system name; graph as final substrate; graph projection as truth; old canonical label as authority; external source as dependency; external README as authority; product reference as root design; generated report as source; migration by normalization plan; substrate decision by normalization plan; evidence treated as governance; validation treated as governance; Git commit treated as semantic truth; context inclusion treated as permission; proof level inflation.

## 25. Remaining Gaps
No actual Graphify material inventory was created. No normalized records were created. No migration was executed. No final substrate decision, candidate scoring packet, substrate ADR, CSS decision audit, Cognitive Semantic System implementation, validation registry implementation, evidence schema, product activation, external adoption, or implementation readiness exists.

## 26. Readiness For CSS-A
CSS-A - Cognitive Semantic System Decision Audit is ready after explicit instruction. CSS-A should audit CSS-00, CSS-01, CSS-02, naming consistency, substrate neutrality, Graphify boundary, migration/product/external/security/validation alignment, and readiness for H-00, M-02, P-00, or IR-00 recommendations. Do not create CSS-A.

## 27. Final Verdict
| Question | Answer |
| --- | --- |
| What does CSS-02 decide? | It decides normalization rules, classes, statuses, blockers, evidence/proof posture, matrices, and boundaries for prior Graphify-related material. |
| Does CSS-02 normalize actual files? | No. |
| Does CSS-02 migrate material? | No. |
| Does CSS-02 select graph? | No. Graph remains a candidate only. |
| What is Graphify's current status? | Historical prior material label, external source label, rejected/prohibited naming example, or candidate graph/projection evidence label only. |
| What normalized language is accepted? | Cognitive Semantic System, graph candidate, graph projection evidence, candidate substrate evidence, external graphify source, historical Graphify material, generated projection, evidence not authority, and substrate undecided. |
| What remains blocked? | Actual normalization, migration, wholesale copy, product activation, external adoption, dependency adoption, execution, implementation, substrate decision, schema/registry/code/tooling, Git staging, commit, push, and CSS-A. |
| Is CSS-A ready after explicit instruction? | Yes, as an audit only; it is not created here. |

Stop rule: CSS-02 ends here. Do not start CSS-A, normalize actual files, migrate material, select substrate, implement the Cognitive Semantic System, execute migration, activate products, adopt external sources, stage, commit, push, install dependencies, authenticate, call network/provider/API/MCP, inspect local-only folders deeply, or start any next ticket.
