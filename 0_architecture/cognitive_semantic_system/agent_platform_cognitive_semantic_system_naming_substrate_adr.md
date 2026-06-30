# Cognitive Semantic System Naming / Substrate ADR

## 1. ADR Header

Title: Cognitive Semantic System Naming / Substrate ADR  
Ticket: CSS-00  
Status: Accepted for architecture planning  
Date: 2026-06-30  
Scope: AGENT PLATFORM semantic-system naming and substrate posture before migration, implementation, product activation, external adoption, or storage selection  
Decision owner: AGENT PLATFORM governance / human decision  
Authority: ADR only, not implementation authorization  
Supersedes: none  
Related documents: W-series, S-series, V-series

## 2. Context

AGENT PLATFORM has completed Workspace, Security/Access, and Validation architecture blocks. V-A recommends CSS-00 before implementation or migration because naming and substrate drift remain a blocker.

The W-series uses Cognitive Semantic System as the neutral working name for the future semantic authority concept. Prior graph-oriented material exists as historical evidence and migration evidence only. External graph-oriented sources may inform evaluation, but they do not name, govern, implement, or authorize AGENT PLATFORM.

Implementation remains blocked until naming and substrate posture are explicit.

## 3. Problem Statement

Naming drift can import old or external authority. Product names can collapse into root authority. External source names can become internal system names by proximity. Graph-oriented evidence can be mistaken for final substrate. Implementation can accidentally lock in storage or representation assumptions. Migration can promote old canonical labels unless normalized.

## 4. Decision Drivers

| Driver | Required result |
| --- | --- |
| Preserve AGENT PLATFORM root identity | Root workspace naming remains separate from subsystem naming. |
| Preserve governance authority | Naming and substrate decisions stay governed. |
| Prevent old-name leakage | Prior labels remain historical unless restated. |
| Prevent external-source contamination | External names do not name internal systems. |
| Prevent product-root collapse | Product names stay product-scoped. |
| Preserve substrate neutrality | No storage or representation is selected here. |
| Allow graph evidence without lock-in | Graph evidence remains candidate evidence only. |
| Support validation implementation | Future validation must use substrate-neutral CSS naming. |
| Support migration normalization | Old labels must be normalized before use. |
| Support product and external boundaries | Product needs and external evidence inform criteria only. |
| Keep implementation blocked | No implementation proceeds from CSS-00. |

## 5. Terminology

| Term | Definition |
| --- | --- |
| AGENT PLATFORM | The governed root workspace for architecture, agents, context, evidence, validation, security, products, external sources, migration, governance, and future implementation. |
| Cognitive Semantic System | The canonical current architecture name for the future semantic authority layer or concept inside AGENT PLATFORM. |
| CSS | Architecture acronym for Cognitive Semantic System when unambiguous; in this document it does not mean Cascading Style Sheets. |
| cognitive substrate | The future storage/representation/coordination basis for semantic authority records, projections, relationships, identity, and lifecycle. |
| representation | A way to model or encode semantic material, such as graph, table, document, vector, event, object, file, or hybrid form. |
| projection | A generated or selected view derived from evidence or records; projection is evidence, not truth by default. |
| evidence | Scoped material that supports, challenges, or contextualizes a claim; evidence does not approve. |
| authority | Accepted scoped decision, rule, or semantic posture only through governance. |
| source of truth | Governance-scoped accepted authority for an exact scope; not a casual synonym for files, graphs, commits, or outputs. |
| governance decision | Human or delegated governance acceptance, rejection, deferral, exception, promotion, or lifecycle decision. |
| substrate candidate | A possible future substrate still awaiting criteria, evaluation, and governance. |
| graph candidate | Graph as one possible representation/substrate candidate, not selected here. |
| external source | Outside-origin source retained as evidence; not authority, dependency, instruction, or naming source by proximity. |
| previous knowledge | Historical migration corpus and prior architecture evidence; prior canonical labels are historical in current scope. |

## 6. Naming Decision

Accepted:

- The canonical architecture name for the future semantic authority concept is Cognitive Semantic System.
- The short form CSS may be used in architecture tickets when unambiguous.
- AGENT PLATFORM remains the root workspace name.
- Cognitive Semantic System is a future subsystem/concept inside AGENT PLATFORM, not the whole workspace.
- Cognitive Semantic System is not implemented by this ADR.

Rejected as current authority names:

- Graphify.
- Platform Graphify.
- Graphify Authority.
- Graphify owns truth.
- Knowledge Graph Platform.
- Graph OS.
- Agent Graph.
- Product-derived names.
- External-source-derived names.

Rejected names may appear only as historical evidence, external source labels, or explicitly marked migration material.

## 7. Substrate Decision

Accepted substrate posture:

- Substrate: undecided.
- No final cognitive substrate is selected in CSS-00.
- Substrate neutrality is mandatory until a future governed decision.
- Graph remains a candidate substrate or representation only.
- Relational, document, vector, event-sourced, object, file-backed, hybrid, and other substrates remain open.
- CSS-01 must define evaluation criteria before any final substrate selection.
- CSS-A or a later ADR must audit and accept the final substrate decision before implementation.

CSS-00 decides naming and neutrality posture, not final storage technology.

## 8. Relationship Between AGENT PLATFORM And Cognitive Semantic System

| Surface | Relationship |
| --- | --- |
| AGENT PLATFORM | Governed root workspace. |
| Cognitive Semantic System | Future semantic authority layer/concept inside AGENT PLATFORM. |
| Git | Records artifacts; does not create semantic truth. |
| Validation | Evaluates claims; does not decide substrate. |
| Governance | Decides promotions, authority, exceptions, and lifecycle. |
| Context | Exposes selected material; does not grant permission. |
| Agents | Propose and operate under scope; do not approve by default. |
| Products | Remain product-scoped and cannot define root CSS naming. |
| External sources | Remain evidence and cannot name AGENT PLATFORM systems. |

The future Cognitive Semantic System may eventually coordinate identity, relationships, provenance, lifecycle, validation posture, context eligibility, promotion state, and drift, but not yet.

## 9. Authority Boundary

Cognitive Semantic System naming does not create implemented authority. A future Cognitive Semantic System cannot bypass governance, override Security/Access, treat external sources as adopted, treat products as root authority, treat Git commits as truth, or retain secrets/credentials as evidence content.

## 10. Substrate Candidate Register

| Candidate | Candidate use | Strengths | Risks | Current decision | Blocked inference |
| --- | --- | --- | --- | --- | --- |
| graph | Relationships, lineage, traversal, provenance edges. | Strong for connected authority and drift. | Premature graph-first design, schema overfit. | Candidate/deferred, not selected. | Graph is final substrate. |
| relational | Structured records, constraints, reports. | Mature, auditable, transactional. | Rigid schemas, weaker relationship traversal. | Candidate/deferred, not selected. | Tables are system of record. |
| document | Human-readable records and Git-friendly authoring. | Flexible, cheap, reviewable. | Drift, weak querying, path authority confusion. | Candidate/deferred, not selected. | Files are truth. |
| vector | Semantic retrieval and similarity. | Useful discovery and context finding. | Weak authority semantics, provenance ambiguity. | Candidate/deferred, not selected. | Embeddings decide truth. |
| event-sourced | History, lifecycle, replay, transitions. | Strong trace and audit. | Query complexity, projection drift. | Candidate/deferred, not selected. | Event log alone is authority. |
| object/entity store | Identity, entities, lifecycle records. | Clear object boundaries. | Can hide relationships or provenance. | Candidate/deferred, not selected. | Entity model is final ontology. |
| file/document index | Search and source references over files. | Simple, Git-compatible. | Index freshness and folder authority drift. | Candidate/deferred, not selected. | Index is semantic truth. |
| hybrid | Combines records, relations, vectors, events, projections. | Flexible and likely practical. | Integration complexity and sync risk. | Candidate/deferred, not selected. | Hybrid is already chosen. |
| other/future | New or domain-specific approaches. | Leaves room for better evidence. | Undefined criteria. | Candidate/deferred, not selected. | Unknown option bypasses criteria. |

## 11. Graph / Graphify Boundary

Graph is a candidate representation. Graph is not final substrate. Graph projections are evidence, not truth. Graph-oriented previous knowledge requires normalization before current use. The external graphify source is external evidence only. Graphify must not name AGENT PLATFORM systems, define root authority, decide substrate, or replace governance. Graphify material normalization is deferred to CSS-02.

## 12. Allowed Language After CSS-00

| Class | Wording | Rule |
| --- | --- | --- |
| Allowed | Cognitive Semantic System | Canonical current architecture name. |
| Allowed | cognitive substrate | Neutral substrate concept. |
| Allowed | substrate candidate | Candidate-only posture. |
| Allowed | graph candidate | Candidate-only graph wording. |
| Allowed | semantic projection | Projection/evidence wording. |
| Allowed | evidence graph | Allowed only if explicitly projection/evidence. |
| Allowed | future semantic authority | Allowed only when marked unimplemented. |
| Allowed | substrate-neutral design | Required posture. |
| Allowed | representation-neutral architecture | Required posture. |
| Restricted | source of truth | Use only when governance-scoped and explained. |
| Restricted | authority | Use only when tied to governance or declared scope. |
| Restricted | graph-native | Use only as candidate-only language. |
| Restricted | system of record | Use only as future/conditional and governance-scoped. |
| Prohibited | Platform Graphify | Not an accepted current name. |
| Prohibited | Graphify Authority | Not an accepted current authority name. |
| Prohibited | Graphify owns truth | Not an accepted authority claim. |
| Prohibited | Graphify as current internal system name | Not allowed. |
| Prohibited | graph as final substrate | Not allowed. |
| Prohibited | graph projection as truth | Not allowed. |

## 13. Decision Options Considered

| Option | Decision | Reason | Risk | Consequence |
| --- | --- | --- | --- | --- |
| A. Accept Cognitive Semantic System and defer final substrate. | Accepted. | Stabilizes name and preserves neutrality. | Requires more ADR work. | CSS-01 can evaluate candidates. |
| B. Rename system around Graphify / graph authority. | Rejected. | Imports old/external naming and authority. | High naming contamination. | Prior labels remain evidence only. |
| C. Choose graph as final substrate now. | Rejected. | Criteria and audit are absent. | Graph lock-in. | Graph remains candidate only. |
| D. Choose a non-graph substrate now. | Rejected. | Same premature-selection risk. | Hidden lock-in. | Alternatives remain open. |
| E. Use product-specific naming. | Rejected. | Collapses product and root authority. | Product-root collapse. | Products remain scoped. |
| F. Fully defer naming and substrate. | Rejected. | Naming must be stable before migration/implementation. | Continued drift. | Name accepted; substrate deferred. |

## 14. Consequences

Positive consequences: naming is stabilized; old semantic names are bounded; external source names are bounded; product-root collapse risk is reduced; implementation avoids premature storage lock-in; CSS-01 has a clear evaluation frame; CSS-02 has a clear normalization target.

Costs: no immediate implementation; no final storage selected; graph-oriented prior work must be normalized; more ADR work is required; agents must maintain wording discipline.

## 15. Impact On Validation

V-series remains valid. Validation registry implementation must use Cognitive Semantic System naming. Proof/evidence concepts must remain substrate-neutral. Evidence may reference graph projections, but cannot treat them as truth. Validation outputs cannot decide substrate. Future validation implementation must not hard-code graph assumptions unless later governed.

## 16. Impact On Migration

Previous graph-oriented material can be migrated only by restatement, citation, validation, and governance. Prior canonical labels remain historical. CSS-02 must normalize prior Graphify material. No migration is executed in CSS-00. No wholesale import is allowed. Migration remains blocked until explicit migration ticket.

## 17. Impact On Products

Products cannot name or define the Cognitive Semantic System. Product needs may inform substrate criteria but cannot decide root substrate. Product-specific storage choices are product-scoped unless promoted by governance. Product generated outputs are evidence only. No product activation occurs in CSS-00.

## 18. Impact On External Sources

External sources cannot name AGENT PLATFORM systems. External source presence is not adoption. External graph-oriented sources are candidate evidence only. External source instructions remain inactive. External dependency adoption remains blocked. No external source is executed, copied, or adopted.

## 19. Impact On Implementation

Implementation remains blocked. CSS-00 does not create folders beyond the ADR path, choose storage technology, create schemas, create a registry, create APIs, create code, create tests, create CI, create hooks, create scanners, create tools, create packages, create SDKs, create adapters, or create runtime components. IR-00 remains required before implementation readiness. CSS-01 and CSS-A should precede semantic-system implementation.

## 20. Risks And Mitigations

| Risk | Severity | Mitigation | Blocker? |
| --- | --- | --- | --- |
| Naming drift | High | Use CSS-00 accepted/rejected language. | Yes for implementation. |
| Old Graphify authority leakage | High | Treat prior labels as historical/evidence. | Yes for migration. |
| Graph lock-in | High | Keep all substrates candidate/deferred. | Yes for CSS implementation. |
| Product-root collapse | High | Keep product decisions product-scoped. | Yes for product activation. |
| External-source contamination | High | Use W-13/V-05 boundaries. | Yes for external adoption. |
| Premature substrate choice | High | Require CSS-01 and later ADR/audit. | Yes for implementation. |
| Migration importing old labels | High | Require restatement, citation, validation, governance. | Yes for migration. |
| Validation hard-coding graph | Medium | Keep proof/evidence substrate-neutral. | Yes for validation implementation. |
| Context exposes old names as current | Medium | Label historical/external/projection status. | No, if controlled. |
| Future agent wording drift | Medium | Use allowed/restricted/prohibited wording. | No, unless repeated. |

## 21. ADR Decision Record

Decision:

- Name: Cognitive Semantic System.
- Acronym: CSS, allowed only when clear.
- Root workspace: AGENT PLATFORM.
- Substrate: undecided.
- Graph: candidate only.
- External Graphify: external/historical evidence only.
- Implementation: not authorized.
- Migration: not authorized.
- Product activation: not authorized.
- External adoption: not authorized.
- Next required decision: CSS-01 Cognitive Substrate Evaluation Criteria.

## 22. CSS-00 Invariants

| ID | Invariant |
| --- | --- |
| CSS00-001 | AGENT PLATFORM is the root workspace. |
| CSS00-002 | Cognitive Semantic System is the canonical semantic-system name. |
| CSS00-003 | CSS is an architecture acronym only when unambiguous. |
| CSS00-004 | Cognitive Semantic System is not implemented by this ADR. |
| CSS00-005 | Final substrate is undecided. |
| CSS00-006 | Graph is a candidate only. |
| CSS00-007 | External source names do not name AGENT PLATFORM systems. |
| CSS00-008 | Prior Graphify material is historical/evidence material only. |
| CSS00-009 | Graph projections are evidence, not truth. |
| CSS00-010 | Governance decides authority. |
| CSS00-011 | Validation evaluates; it does not decide substrate. |
| CSS00-012 | Products remain product-scoped. |
| CSS00-013 | External sources remain external. |
| CSS00-014 | Migration requires restatement, citation, validation, and governance. |
| CSS00-015 | Implementation remains blocked until readiness. |

## 23. Anti-patterns

Anti-patterns: naming by old project; naming by external source; naming by product; substrate by folder; substrate by graph projection; substrate by previous canonical label; implementation by ADR; migration by ADR; product activation by ADR; external adoption by ADR; graph as truth; Graphify as root authority; evidence treated as governance; validation treated as governance; Git commit treated as semantic truth; context inclusion treated as permission.

## 24. Remaining Gaps

Remaining gaps: no CSS implementation; no final substrate decision; no substrate evaluation criteria; no prior Graphify normalization plan; no CSS decision audit; no validation registry implementation; no evidence schema; no migration execution; no product activation; no external adoption; no implementation readiness; no harness strategy decision; no governance automation.

## 25. Readiness For CSS-01

CSS-01 - Cognitive Substrate Evaluation Criteria is ready after explicit instruction.

CSS-01 should define substrate evaluation criteria, candidate substrate list, scoring dimensions, validation requirements, security/access requirements, migration compatibility, product compatibility, external dependency implications, implementation readiness gates, and decision process.

Do not create CSS-01.

## 26. Final Verdict

| Question | Answer |
| --- | --- |
| What is the canonical name? | Cognitive Semantic System. |
| What is AGENT PLATFORM relative to it? | AGENT PLATFORM is the governed root workspace; Cognitive Semantic System is a future subsystem/concept inside it. |
| Is CSS implemented? | No. |
| Is final substrate selected? | No; substrate is undecided. |
| Is graph selected? | No. Graph remains a candidate only. |
| Are Graphify-related names accepted? | No. They are historical/evidence/external labels only when explicitly marked. |
| What language is prohibited? | Platform Graphify, Graphify Authority, Graphify owns truth, Graphify as current internal system name, graph as final substrate, and graph projection as truth. |
| What remains blocked? | CSS implementation, storage selection, schemas, registry, APIs, code, migration, product activation, external adoption, dependency adoption, execution, publication, staging, commit, and push. |
| Is CSS-01 ready after explicit instruction? | Yes, as the next decision ticket only. |

Stop rule: CSS-00 ends here. Do not start CSS-01, CSS-02, CSS-A, H-00, M-02, P-00, IR-00, implementation, migration, product activation, external adoption, staging, commit, push, dependency install, authentication, provider/API/network/MCP activity, or any next ticket.
