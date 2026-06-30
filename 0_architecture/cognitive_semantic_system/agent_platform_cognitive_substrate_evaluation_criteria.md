# Agent Platform Cognitive Substrate Evaluation Criteria

Status: Accepted for CSS-01 criteria definition | Date: 2026-06-30 | Scope: Architecture criteria only | Canonical subsystem name: Cognitive Semantic System | Decision posture: No substrate selected

## 1. Purpose
This document defines criteria for selecting a future Cognitive Semantic System substrate inside AGENT PLATFORM. It does not select, implement, migrate to, activate, procure, install, or configure any substrate.

## 2. Evaluation Problem
The platform needs a future substrate that can represent, retrieve, validate, govern, and expose cognitive workspace knowledge without confusing evidence, context, authority, proof, execution, or Git history. The evaluation problem is to compare substrate families against architecture, validation, security, governance, workspace, product, and external-source constraints before implementation.

## 3. Non-Decision Statement
CSS-01 is a criteria artifact only. No candidate family receives final approval in this document. No graph, vector, document, relational, rule, hybrid, product-derived, or external-source-derived substrate is selected.

## 4. Naming Boundary
The accepted subsystem name is Cognitive Semantic System. `CSS` may be used only when unambiguous and architecture-scoped. The subsystem is a future concept inside AGENT PLATFORM, not the whole workspace.

## 5. Source Constraints
CSS-01 is constrained by the W-series, S-series, V-series, and CSS-00. Those inputs establish that validation evaluates, evidence supports, proof is scoped, security constrains, governance decides, context exposes selected material, and Git records artifacts only.

## 6. Evaluation Principles
| Principle | Meaning |
| --- | --- |
| Substrate neutrality | Criteria must not be written to predetermine a winner. |
| Evidence before authority | Stored material is not automatically true, approved, or promotable. |
| Governance before activation | Governance decision records are required before implementation or migration. |
| Security before convenience | Local-only, secret, credential, and access boundaries can block useful candidates. |
| Validation before claims | Claims require validation records, proof scope, command scope, and evidence retention rules. |
| Context is exposure | Context packs expose selected material; they do not grant truth or permission. |
| Products stay scoped | Product workspaces remain inactive/local-only unless future product governance approves activation. |
| External sources stay evidence | External sources remain evidence-only until reuse, dependency, and execution approval exist. |

## 7. Candidate Families
| Family | Description |
| --- | --- |
| Document-first substrate | Markdown, ADR, registry, and file-based knowledge with structured metadata. |
| Graph substrate | Nodes and edges representing concepts, evidence, dependencies, claims, and governance relations. |
| Vector retrieval substrate | Embedding/search layer for semantic retrieval and context assembly. |
| Relational substrate | Tables, constraints, and queryable records for registries, validation, and audit state. |
| Rule/logic substrate | Explicit inference, constraint, policy, or proof rules. |
| Hybrid substrate | A governed combination of substrate families with explicit authority boundaries. |

## 8. Candidate Status
All candidate families are unselected. Graph remains a candidate only. Hybrid remains possible only if each component has a bounded role and no component silently becomes the authority layer.

## 9. Mandatory Requirements
| ID | Requirement |
| --- | --- |
| CSS-REQ-001 | Preserve Cognitive Semantic System naming and AGENT PLATFORM root identity. |
| CSS-REQ-002 | Separate semantic representation from governance authority. |
| CSS-REQ-003 | Separate evidence from proof and proof from approval. |
| CSS-REQ-004 | Preserve validation records, proof levels, command scope, and evidence retention posture. |
| CSS-REQ-005 | Support security constraints for sensitivity, access profile, local-only material, secrets, credentials, execution, providers, APIs, networks, MCP, and publication. |
| CSS-REQ-006 | Support context-pack generation as selected exposure, not truth or permission. |
| CSS-REQ-007 | Keep product and external-source boundaries explicit. |
| CSS-REQ-008 | Support migration by classification, restatement, validation, and governance; not bulk import or file movement as approval. |
| CSS-REQ-009 | Remain auditable through architecture artifacts and future decision records. |
| CSS-REQ-010 | Avoid dependency, runtime, provider, or database commitment before explicit approval. |

## 10. Criterion Groups
| Group | Concern |
| --- | --- |
| A | Semantic model fit |
| B | Validation and proof |
| C | Governance and authority |
| D | Security and access |
| E | Context and agent usability |
| F | Migration and evidence handling |
| G | Product and external-source boundaries |
| H | Operations and implementation readiness |
| I | Interoperability and reversibility |

## 11. A - Semantic Model Fit
| Criterion | Evaluation question |
| --- | --- |
| A1 | Can the candidate represent concepts, claims, decisions, evidence, constraints, and relationships without overloading one record type? |
| A2 | Can it preserve source identity, lineage, and uncertainty? |
| A3 | Can it model competing claims without forcing premature truth selection? |
| A4 | Can it support both human-readable architecture review and future machine-assisted retrieval? |

## 12. B - Validation And Proof
| Criterion | Evaluation question |
| --- | --- |
| B1 | Can validation records be attached to claims without turning all records into proof? |
| B2 | Can proof levels and proof scope be represented explicitly? |
| B3 | Can command scope, non-execution constraints, and evidence retention be preserved? |
| B4 | Can invalidated, stale, superseded, or disputed records remain auditable? |

## 13. C - Governance And Authority
| Criterion | Evaluation question |
| --- | --- |
| C1 | Can governance decisions remain the source of approval authority? |
| C2 | Can promotion, rejection, deprecation, and supersession be recorded clearly? |
| C3 | Can ownership, review state, and decision history be queried without changing authority rules? |
| C4 | Can Git history remain artifact history rather than semantic truth? |

## 14. D - Security And Access
| Criterion | Evaluation question |
| --- | --- |
| D1 | Can the candidate preserve sensitivity labels and access profiles? |
| D2 | Can local-only material be excluded or represented only by safe references? |
| D3 | Can secrets, credentials, tokens, provider auth, and private config be blocked from retention? |
| D4 | Can execution, package manager, provider, API, network, MCP, and publication boundaries be represented as blocked unless approved? |
| D5 | Can access filtering be applied before context exposure? |

## 15. E - Context And Agent Usability
| Criterion | Evaluation question |
| --- | --- |
| E1 | Can it produce bounded context packs for agents and humans? |
| E2 | Can context selection include rationale, scope, exclusions, and freshness? |
| E3 | Can it avoid treating retrieval ranking as truth, permission, or approval? |
| E4 | Can it support precise citations back to architecture artifacts and evidence records? |

## 16. F - Migration And Evidence Handling
| Criterion | Evaluation question |
| --- | --- |
| F1 | Can migration be staged as inventory, classification, restatement, validation, governance, and audit? |
| F2 | Can evidence-only material remain evidence-only after ingestion or reference? |
| F3 | Can prior knowledge be summarized safely without copying local-only or sensitive material? |
| F4 | Can incomplete, conflicting, or deprecated inputs remain traceable? |

## 17. G - Product And External-Source Boundaries
| Criterion | Evaluation question |
| --- | --- |
| G1 | Can inactive product workspaces remain product-scoped and local-only? |
| G2 | Can external snapshots remain evidence-only and execution-blocked? |
| G3 | Can source license, provenance, reuse approval, and dependency approval be represented distinctly? |
| G4 | Can product activation and external adoption remain future governance events? |

## 18. H - Operations And Implementation Readiness
| Criterion | Evaluation question |
| --- | --- |
| H1 | Can the candidate be evaluated without installation, runtime activation, network calls, authentication, or dependency adoption? |
| H2 | Does future implementation require new operational controls that are not yet designed? |
| H3 | Can backup, export, review, and recovery be reasoned about before implementation? |
| H4 | Can the candidate fail safely when enforcement tooling does not exist? |

## 19. I - Interoperability And Reversibility
| Criterion | Evaluation question |
| --- | --- |
| I1 | Can records be exported to human-readable artifacts? |
| I2 | Can the substrate interoperate with future validation, governance, security, and context artifacts? |
| I3 | Can the platform replace or revise the substrate without losing governance history? |
| I4 | Can schema evolution be reviewed through architecture decisions rather than hidden runtime mutation? |

## 20. Scoring Scale

Scores are assigned per criterion only during a future evaluation round.

| Score | Meaning |
| ---: | --- |
| 0 | Fails or contradicts the criterion. |
| 1 | Weak fit; major unresolved architecture or security gaps. |
| 2 | Partial fit; plausible but needs significant constraints or companion systems. |
| 3 | Adequate fit; known gaps are governable. |
| 4 | Strong fit; clean alignment with minor open questions. |
| 5 | Excellent fit; directly supports the criterion with clear auditability and low residual risk. |

## 21. Weighting Model

Weights guide comparison but cannot override blockers.

| Group | Weight |
| --- | ---: |
| A - Semantic model fit | 15 |
| B - Validation and proof | 15 |
| C - Governance and authority | 15 |
| D - Security and access | 20 |
| E - Context and agent usability | 10 |
| F - Migration and evidence handling | 10 |
| G - Product and external-source boundaries | 5 |
| H - Operations and implementation readiness | 5 |
| I - Interoperability and reversibility | 5 |

## 22. Score Calculation

Future evaluation may calculate a weighted score as:

```text
candidate_score = sum(group_average_score * group_weight) / 100
```

A score is comparative evidence only. It is not approval, implementation readiness, or substrate selection.

## 23. Blockers

A candidate is blocked regardless of score if it has any of these properties.

| ID | Blocker |
| --- | --- |
| CSS-BLOCK-001 | Requires treating stored records, graph edges, embeddings, tables, files, or commits as governance authority. |
| CSS-BLOCK-002 | Cannot preserve validation scope, proof level, evidence lineage, and uncertainty. |
| CSS-BLOCK-003 | Requires retention of secrets, credentials, provider auth, private config, or sensitive local-only content. |
| CSS-BLOCK-004 | Cannot exclude ignored/local-only areas or represent them only through safe references. |
| CSS-BLOCK-005 | Requires execution, package install, provider/API/network/MCP activity, authentication, product activation, or external-source adoption before approval. |
| CSS-BLOCK-006 | Collapses context exposure into truth, permission, or approval. |
| CSS-BLOCK-007 | Collapses products or external sources into root platform authority. |
| CSS-BLOCK-008 | Requires hidden schema mutation, unreviewable inference, or non-auditable promotion. |
| CSS-BLOCK-009 | Prevents future export, review, or replacement of the substrate. |
| CSS-BLOCK-010 | Uses rejected or product-derived naming as the accepted subsystem identity. |

## 24. Minimum Passing Thresholds

Before any final decision, a candidate must satisfy all blockers and meet these thresholds.

| Threshold | Requirement |
| --- | --- |
| Security floor | D group average must be at least 4.0. |
| Governance floor | C group average must be at least 4.0. |
| Validation floor | B group average must be at least 4.0. |
| Overall floor | Weighted score must be at least 3.5. |
| Evidence floor | Every score must cite source evidence, assumption, or explicit gap. |

## 25. Evaluation Matrix Template

Future evaluation rounds should use this template.

| Candidate | A | B | C | D | E | F | G | H | I | Blocked? | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Document-first | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Evidence required. |
| Graph | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Candidate only. |
| Vector retrieval | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Retrieval is not authority. |
| Relational | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Registry fit must be tested. |
| Rule/logic | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Inference auditability required. |
| Hybrid | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Component authority boundaries required. |

## 26. Combination Model

A hybrid candidate may be valid only if each component has a declared role.

| Role | Allowed purpose |
| --- | --- |
| Record store | Durable architecture, registry, validation, and governance records. |
| Relationship layer | Querying explicit links among concepts, decisions, evidence, and constraints. |
| Retrieval layer | Finding relevant material for review or context packs. |
| Rule layer | Checking explicit policies, blockers, and promotion conditions. |
| Context layer | Preparing bounded context exposure for agents and humans. |

No layer may silently become governance authority.

## 27. Candidate Evaluation Notes

These notes are non-scoring prompts for future CSS evaluation.

| Family | Key risk to test |
| --- | --- |
| Document-first | May be highly auditable but weak for complex relationship queries. |
| Graph | May model relationships well but can be misused as authority or overfit to edges. |
| Vector retrieval | Useful for discovery but cannot by itself preserve proof, authority, or permissions. |
| Relational | Strong for registries and audit state but may need companion semantic retrieval. |
| Rule/logic | Strong for constraints but risky if inference is opaque or exceeds approved rules. |
| Hybrid | Potentially strongest but only if boundaries, schemas, and authority are explicit. |

## 28. Evidence Requirements

Every future candidate evaluation must include:

| Evidence type | Requirement |
| --- | --- |
| Architecture citations | Cite accepted W-series, S-series, V-series, CSS, or future governance artifacts. |
| Assumption log | Mark assumptions separately from validated facts. |
| Security review | Identify local-only, secrets, credentials, sensitivity, access, execution, provider, API, network, MCP, and publication implications. |
| Validation review | Identify proof levels, command scope, evidence retention, and validation sufficiency. |
| Boundary review | Identify product, external-source, migration, and Git boundaries. |
| Residual risk | List unresolved gaps and whether they block selection or implementation. |

## 29. Evaluation Process

A future substrate decision must follow this process.

1. Define candidate scope without installing, running, authenticating, or adopting dependencies.
2. Map candidate behavior to each criterion group.
3. Apply blockers before scoring.
4. Score each criterion with cited evidence and assumptions.
5. Review security/access implications before any implementation readiness claim.
6. Review validation/proof implications before any migration readiness claim.
7. Review governance authority and naming boundaries.
8. Publish a decision record only if a human explicitly authorizes the next CSS ticket.

## 30. Decision Gates

| Gate | Required result |
| --- | --- |
| Naming gate | Uses Cognitive Semantic System as the subsystem name. |
| Security gate | No blocker under security/access constraints. |
| Validation gate | Proof, evidence, and validation scope remain explicit. |
| Governance gate | Approval remains a governance decision, not a substrate side effect. |
| Boundary gate | Product, external-source, local-only, and Git boundaries remain intact. |
| Operations gate | No unapproved implementation, runtime, dependency, network, provider, API, MCP, authentication, or publication step is required. |

## 31. Invariants

These statements must remain true after any future substrate decision.

| ID | Invariant |
| --- | --- |
| CSS-INV-001 | The Cognitive Semantic System is inside AGENT PLATFORM. |
| CSS-INV-002 | Stored knowledge does not equal approved truth. |
| CSS-INV-003 | Retrieval does not equal permission. |
| CSS-INV-004 | Validation evidence does not equal governance approval. |
| CSS-INV-005 | Git history does not equal semantic authority. |
| CSS-INV-006 | Product workspaces and external sources do not become root authority by ingestion or reference. |
| CSS-INV-007 | Local-only and sensitive material must not leak into shared substrate records. |
| CSS-INV-008 | Substrate choice must remain revisable through architecture governance. |

## 32. Anti-Patterns

| Anti-pattern | Why it is rejected |
| --- | --- |
| Selecting a substrate because it is fashionable | Violates evidence-led architecture. |
| Treating a graph edge as approval | Collapses representation into authority. |
| Treating embedding similarity as truth | Collapses retrieval into proof. |
| Bulk importing prior material | Bypasses classification, validation, security, and governance. |
| Activating product code to evaluate substrate fit | Violates product boundary and execution constraints. |
| Running external-source code for comparison | Violates evidence-only and execution-blocked posture. |
| Designing schemas as implementation | CSS-01 is criteria only. |

## 33. Known Gaps And CSS-02 Readiness

CSS-01 leaves these gaps for later explicit work.

| Gap | Status |
| --- | --- |
| Candidate-specific evidence packets | Not started. |
| Detailed scoring records | Not started. |
| Substrate decision record | Not started. |
| Schema or registry design | Not authorized. |
| Implementation readiness | Blocked. |
| Migration execution | Blocked. |
| Product activation or external adoption | Blocked. |

CSS-02 may begin only after explicit instruction. CSS-01 provides criteria that CSS-02 or a later ticket can use, but it does not authorize that work.

## 34. Final Verdict

CSS-01 defines Cognitive Semantic System substrate evaluation criteria, scoring, blockers, process, gates, invariants, and readiness boundaries.

The final substrate remains undecided.

Graph remains a candidate only.

No CSS-02 work, implementation, migration execution, product activation, external-source adoption, dependency adoption, runtime activation, authentication, provider/API/network/MCP call, schema creation, registry creation, Git staging, commit, push, or publication is authorized by this document.
