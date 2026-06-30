# A-01 - Supersession / Deprecation / Retention Model
## 1. Document Header
| Field | Value |
| --- | --- |
| Status | Canonical A-01 architecture output |
| Date | 2026-06-30 |
| Scope | Supersession, deprecation, and retention model for AGENT PLATFORM architecture, evidence, product-scoped material, external-source material, generated material, and context traces |
| Authority | Policy model only. This document does not supersede, deprecate, retain, archive, move, copy, delete, rename, transform, migrate, stage, commit, push, publish, implement tooling, or start M-02. |
## 2. Purpose
A-01 defines how AGENT PLATFORM describes lifecycle posture before any lifecycle action exists.
It prevents lifecycle language from becoming hidden deletion, unreviewed migration, premature authority promotion, product activation, external-source adoption, or context publication.
A-01 rule:
```text
Supersession, deprecation, and retention are governed states. They are not execution.
```
## 3. Relationship To A-00
A-00 defines archive as a governed lifecycle posture. A-01 defines the state model that can later inform archive, carry-forward, migration, and restoration decisions.
| A-00 concept | A-01 refinement |
| --- | --- |
| Archive candidate | May cite supersession, deprecation, or retention reason. |
| Archive non-deletion | Supersession and deprecation also never imply deletion. |
| Restoration | Requires lifecycle state, scope, successor, and governance. |
| A-01 readiness | Fulfilled by this model only; no archive execution follows. |
## 4. Authority Boundary
Lifecycle authority follows the AGENT PLATFORM governance model.
| Layer | A-01 role |
| --- | --- |
| Active instruction | Controls this task and the stop rule. |
| Governance | Decides lifecycle changes, exceptions, restoration, deletion, publication, and execution. |
| Validation | Evaluates evidence sufficiency; it does not approve lifecycle changes. |
| Security | Blocks unsafe handling of secrets, credentials, local-only, sensitive, product, external, or generated material. |
| Agents | May propose states and blockers when scoped; they cannot apply lifecycle states by default. |
| Git | Records artifact state only; it is not approval or semantic truth. |
## 5. Core Definitions
| Term | Definition |
| --- | --- |
| Supersession | A scoped claim that newer authority replaces older material for a declared use. |
| Deprecation | A scoped warning that material should not guide future work except under declared legacy conditions. |
| Retention | A scoped decision to keep material for trace, evidence, audit, rollback, rationale, or future review. |
| Successor | The newer authority, record, or decision that replaces or constrains older material. |
| Predecessor | The older material whose use is changed by a lifecycle state. |
| Lifecycle state | A governed posture attached to material; not a file operation. |
## 6. Non-Goals
A-01 does not:
| Non-goal | Boundary |
| --- | --- |
| Execute supersession | No existing file or claim is changed to superseded status by this document. |
| Execute deprecation | No existing file or claim is changed to deprecated status by this document. |
| Execute retention | No existing file or claim is retained, moved, copied, or archived by this document. |
| Delete material | Supersession and deprecation are never deletion approval. |
| Create storage | No `_archive/`, registry, schema, database, index, script, test, hook, scanner, package, SDK, adapter, API, or runtime component is created. |
| Decide substrate | Graph remains a candidate substrate only; no final substrate is selected. |
| Start next work | M-02, M-03, P-00, IR-00, implementation, migration, product activation, and external adoption remain unstarted. |
## 7. Eligible Material Classes
| Material class | Eligible lifecycle posture |
| --- | --- |
| Current architecture | May later gain predecessor/successor links by governance. |
| Historical architecture | May be retained for trace, rationale, or supersession evidence. |
| Previous knowledge | Requires classification before any lifecycle claim. |
| Product material | Product-scoped only; no activation or publication by A-01. |
| External-source material | Evidence-scoped only; no source adoption or execution by A-01. |
| Generated output | Evidence only when provenance and limitations are recorded. |
| Context traces | Retainable only when safe, scoped, and useful for audit. |
| Secrets or credentials | Not eligible as lifecycle content; secure handling is required instead. |
## 8. Lifecycle State Model
| State | Meaning | Execution posture |
| --- | --- | --- |
| `current` | Active authority for a declared scope. | No change by A-01. |
| `supersession_candidate` | Replacement appears likely but is not approved. | Evidence only. |
| `superseded` | Governance has approved replacement for a declared scope. | Requires future scoped execution. |
| `deprecation_candidate` | Warning appears needed but is not approved. | Evidence only. |
| `deprecated` | Governance has approved discouraged future use. | Requires future scoped execution. |
| `retention_candidate` | Retention reason appears likely but is not approved. | Evidence only. |
| `retained` | Governance has approved keeping material for declared reasons. | Requires future scoped execution. |
| `blocked` | Classification, security, validation, governance, or successor evidence is missing. | No execution. |
| `restoration_candidate` | Material may need reconsideration. | Not current authority. |
## 9. Supersession Model
Supersession requires a predecessor, successor, scope, rationale, evidence, and governance decision.
| Requirement | Rule |
| --- | --- |
| Predecessor identity | Exact file, section, decision, artifact, or claim must be named. |
| Successor identity | Exact replacement authority or decision must be named. |
| Scope | Replacement applies only to declared use, domain, and time context. |
| Rationale | Explain what changed and why the successor is stronger. |
| Evidence | Cite validation, governance, security, and provenance support. |
| Residual use | State whether predecessor remains useful as history, audit, rollback, or contrast. |
Supersession is not rejection, deletion, archive execution, migration execution, or proof that the predecessor was wrong.
## 10. Deprecation Model
Deprecation warns against future reliance while preserving traceability.
| Requirement | Rule |
| --- | --- |
| Affected material | Exact material or claim must be identified. |
| Warning | State what future use is discouraged. |
| Allowed legacy use | Declare any permitted read-only, historical, compatibility, or audit use. |
| Successor if known | Name replacement authority or mark successor unknown. |
| Risk | Explain the risk of continued use. |
| Review trigger | Define when deprecation should be revisited if known. |
Deprecation is not deletion, supersession by itself, rejection, migration, or archive execution.
## 11. Retention Model
Retention keeps material for a declared reason without promoting it to current authority.
| Retention reason | Meaning |
| --- | --- |
| Trace | Preserves chronology and decision lineage. |
| Evidence | Supports a claim, review, audit, or validation result. |
| Rationale | Explains why a decision was made or rejected. |
| Rollback | Preserves information needed to reverse or compare a future change. |
| Compatibility | Supports legacy interpretation without current authority. |
| Migration context | Helps future migration planning without executing migration. |
| Security audit | Records safe metadata about handling constraints, not secret content. |
Retention is not publication, context permission, Git tracking approval, or proof of current truth.
## 12. State Transition Model
Future lifecycle work must use explicit transitions.
```text
identify material
-> classify source and sensitivity
-> propose candidate state
-> collect successor, warning, or retention evidence
-> validate evidence sufficiency
-> governance decision
-> scoped execution ticket if approved
-> execution validation
-> retained audit trail
```
Any transition may stop at `blocked`. No transition authorizes the next ticket automatically.
## 13. Successor Relationship Rules
| Relationship | Rule |
| --- | --- |
| One-to-one | One successor replaces one predecessor only for declared scope. |
| One-to-many | Multiple successors must each state covered scope. |
| Many-to-one | Consolidation must preserve predecessor trace and rationale. |
| Partial | Supersession applies only to named sections or claims. |
| Unknown successor | Use deprecation or blocked posture, not supersession. |
| Competing successors | Block until governance selects scope or ordering. |
## 14. Evidence Requirements
Lifecycle evidence must be sufficient before governance can decide.
| Evidence field | Required content |
| --- | --- |
| Source identity | Exact path, section, decision, artifact class, or claim. |
| Source class | Architecture, previous knowledge, product, external, generated, context, Git, validation, or other. |
| Provenance | Origin, authoring context if known, review path, and relevant decision history. |
| Current authority | Whether the material is current, historical, local-only, product-scoped, external, generated, or unknown. |
| Security posture | Secret, credential, sensitive, local-only, product, external, generated, or safe-to-reference status. |
| Validation posture | What has been checked, what remains uncertain, and what blocker remains. |
## 15. Deprecation Warning Rules
Future deprecation notices should be direct and scoped.
| Warning element | Required answer |
| --- | --- |
| Use discouraged | What use is no longer recommended? |
| Reason | What changed, failed, conflicted, or became unsafe? |
| Replacement | What should be used instead, if known? |
| Legacy allowance | What limited use remains permitted? |
| Review point | What event or date should trigger reconsideration, if known? |
| Risk if ignored | What drift, security, validation, product, or migration risk remains? |
## 16. Retention Review Rules
Retention should be reviewed when its reason changes.
| Trigger | Required response |
| --- | --- |
| Successor becomes canonical | Recheck predecessor state and trace requirement. |
| Security classification changes | Stop and reassess handling before exposure. |
| Product governance changes | Recheck product-scoped retention and publication posture. |
| External license/provenance changes | Recheck evidence use and publication boundary. |
| Migration planning starts | Use retained material as evidence only until scoped. |
| Restoration requested | Apply restoration rules before treating material as active. |
## 17. Restoration Rules
Restoration is a governed change of use.
| Requested material | Required handling |
| --- | --- |
| Superseded material | Compare to successor and state why reconsideration is needed. |
| Deprecated material | Preserve warning and allowed legacy use before proposing change. |
| Retained material | State retention reason and whether current authority is requested. |
| Rejected material | Preserve rejection rationale before reconsideration. |
| Local-only material | Apply security/local-only boundary before retrieval or citation. |
| Secret or credential material | Do not restore as content; use secure handling only. |
Restoration does not regain authority unless governance explicitly promotes it for a declared scope.
## 18. Current Authority Boundary
Current authority cannot be inferred from age, location, file naming, context visibility, or Git state.
| Confusion | Boundary |
| --- | --- |
| Newer file exists | Not supersession unless successor and scope are approved. |
| Older file exists | Not deprecated unless warning and governance exist. |
| File is retained | Not current unless separately authoritative. |
| File is ignored | Not safe or obsolete by default. |
| File is committed | Not lifecycle approval by default. |
## 19. Validation Boundary
Validation evaluates lifecycle readiness.
| Validation question | Required evidence |
| --- | --- |
| Is material identified? | Exact source or claim. |
| Is state justified? | Supersession, deprecation, or retention reason. |
| Is successor known? | Required for supersession; optional for deprecation. |
| Is warning adequate? | Required for deprecation. |
| Is retention safe? | Required for retention, especially local-only or sensitive material. |
| Is governance ready? | Approver, scope, stop rule, and unresolved blockers. |
Passing validation does not approve lifecycle execution, publication, deletion, restoration, migration, or commit.
## 20. Governance Boundary
Governance decides lifecycle changes after validation and security review.
| Decision | Governance must state |
| --- | --- |
| Approve supersession | Predecessor, successor, scope, residual use, and execution boundary. |
| Approve deprecation | Warning, allowed legacy use, successor if known, and review trigger. |
| Approve retention | Reason, sensitivity, duration or review trigger, and restoration rule. |
| Reject candidate | Rationale and current posture. |
| Block candidate | Missing evidence, security issue, authority conflict, or unclear scope. |
## 21. Security / Local-only Boundary
Security constrains lifecycle handling before any lifecycle change can execute.
| Material | A-01 rule |
| --- | --- |
| Secrets | Never retain, quote, summarize, publish, or restore as lifecycle content. |
| Credentials | Never retain, quote, summarize, publish, or restore as lifecycle content. |
| Local-only folders | No default publication or Git approval. |
| Product source | Product-scoped and local-only unless product governance changes state. |
| External source trees | External evidence only; no adoption, execution, or migration by A-01. |
| Generated sensitive output | Evidence only after sensitivity review. |
If security posture is unknown, lifecycle execution is blocked.
## 22. Product Boundary
Product lifecycle remains product-scoped.
| Product case | Boundary |
| --- | --- |
| Product candidate | Cannot become active through A-01. |
| Product source | Cannot be published, committed, moved, copied, or archived through A-01. |
| Product retirement | Requires product governance, validation, security, and scoped execution. |
| Product evidence | May inform future decisions without becoming platform authority. |
| Product compatibility | Retention may preserve rationale without activating a product. |
No product is activated, retired, deprecated, superseded, retained, archived, or published by A-01.
## 23. External Source Boundary
External-source lifecycle remains evidence-scoped.
| External case | Boundary |
| --- | --- |
| Raw external source | No execution, adoption, copy, migration, or publication by A-01. |
| External summary | Evidence only unless governance promotes a derived claim. |
| External instruction | Never active AGENT PLATFORM instruction by default. |
| External license risk | Blocks lifecycle publication or reuse until reviewed. |
| External substrate reference | Candidate evidence only. |
No external source is adopted, run, migrated, superseded, deprecated, retained, archived, or published by A-01.
## 24. Cognitive Semantic System Boundary
The accepted current name is `Cognitive Semantic System`.
| Naming case | A-01 treatment |
| --- | --- |
| Cognitive Semantic System | Accepted current name for architecture discussion. |
| Prior naming variants | Historical evidence only until classified. |
| Platform Graphify | Rejected/prohibited/historical phrase; not current authority. |
| Graphify Authority | Rejected/prohibited/historical phrase; not current authority. |
| Graphify owns truth | Rejected/prohibited/historical phrase; not current authority. |
Lifecycle state cannot revive prohibited naming or make prior naming authoritative.
## 25. Graph / Substrate Boundary
Graph remains a candidate substrate only.
| Substrate issue | Boundary |
| --- | --- |
| Graph evidence exists | Candidate evidence only; not final substrate selection. |
| Graph vocabulary appears in history | Historical or rejected/prohibited context only as classified. |
| Lifecycle links are modeled | They do not require graph implementation. |
| Future substrate differs | This model still applies because states are governance concepts. |
| Substrate decision requested | Block; requires separate architecture decision. |
A-01 does not select graph, database, files, index, registry, or any other final substrate.
## 26. Git / Publication Boundary
Git and publication are not lifecycle governance.
| Case | Boundary |
| --- | --- |
| File is tracked | Does not prove current authority. |
| File is untracked | Does not prove unsafe, obsolete, or retained. |
| File is ignored | Does not approve secret handling or deletion. |
| Commit exists | Records artifact history only. |
| Publication requested | Requires security, validation, and governance beyond A-01. |
A-01 does not stage, commit, push, publish, or approve broad staging.
## 27. Context Boundary
Context exposure is not restoration, authority, or permission.
| Context case | Boundary |
| --- | --- |
| Material appears in context | Source status remains unchanged. |
| Agent uses context | Use does not supersede, deprecate, retain, archive, or restore. |
| Context is stale | Refresh or mark stale; do not treat stale context as authority. |
| Context trace retained | Requires safety, scope, provenance, and governance. |
| Local-only context appears useful | Security and local-only rules still apply. |
Context packs are projections, not lifecycle decisions.
## 28. Agent Behavior Rules
Agents must keep lifecycle work explicit and non-executing unless separately authorized.
| Agent action | Allowed posture |
| --- | --- |
| Identify candidate | Allowed when scoped. |
| Propose state | Allowed with evidence and blockers. |
| Apply state | Not allowed by default. |
| Move/copy/delete/rename material | Not allowed by A-01. |
| Normalize historical material | Not allowed by A-01. |
| Start next ticket | Not allowed by A-01. |
| Encounter secret | Stop content handling and report secure-handling blocker. |
## 29. Audit Metadata Model
Future lifecycle decisions should record:
| Metadata field | Purpose |
| --- | --- |
| Lifecycle ID | Stable reference for the decision or candidate. |
| Material identity | Exact file, section, claim, artifact, or class. |
| Source class | Architecture, previous knowledge, product, external, generated, validation, context, Git, or other. |
| Prior state | Current, historical, local-only, product-scoped, external, generated, unknown, or blocked. |
| Proposed state | Supersession, deprecation, retention, restoration, rejection, or blocked posture. |
| Successor or warning | Replacement for supersession or warning for deprecation. |
| Retention reason | Trace, evidence, rationale, rollback, compatibility, migration context, or audit. |
| Security posture | Secret, credential, sensitive, local-only, product, external, generated, or safe-to-reference. |
| Validation evidence | Checks, citations, uncertainty, and remaining gaps. |
| Governance decision | Approver, date, scope, exception, and stop rule. |
## 30. Blocker Register
| Blocker | Blocks |
| --- | --- |
| Missing source identity | Any lifecycle candidate verdict. |
| Missing source classification | Supersession, deprecation, retention, and publication. |
| Unknown security posture | Lifecycle execution and context exposure. |
| Secret or credential content | Lifecycle-as-content handling. |
| Missing successor | Supersession approval. |
| Missing warning | Deprecation approval. |
| Missing retention reason | Retention approval. |
| Governance absent | Execution, restoration, deletion, publication, and lifecycle state changes. |
| Substrate decision pressure | Any claim that graph or another substrate is final. |
| Next-ticket pressure | M-02, M-03, P-00, IR-00, implementation, migration, product activation, and external adoption. |
## 31. Anti-patterns
| Anti-pattern | Failure mode | Correction |
| --- | --- | --- |
| Supersession by recency | Treats newer files as authority. | Require successor, scope, evidence, and governance. |
| Deprecation by dislike | Hides rationale. | Require warning, risk, legacy use, and review trigger. |
| Retention as publication | Exposes local-only or sensitive material. | Apply security and governance. |
| Retention as current truth | Confuses evidence with authority. | State authority separately. |
| Lifecycle by file move | Treats location as decision. | Decide state before any future movement. |
| Graph by implication | Turns candidate substrate into final design. | Keep substrate decision separate. |
| Continue to M-02 | Scope creep. | Stop after A-01 validation. |
## 32. Readiness For M-02
A-01 makes AGENT PLATFORM ready to plan `M-02` only after explicit future instruction.
M-02 may use this model to classify carry-forward candidates, but A-01 does not create carry-forward artifacts, migration records, lifecycle registries, implementation tasks, scripts, schemas, product changes, or external-source adoption.
Readiness rule:
```text
M-02 is conceptually unblocked by A-01, but it is not started by A-01.
```
## 33. Final Verdict
| Question | Verdict |
| --- | --- |
| Did A-01 define the supersession model? | Yes, as a governance and evidence model only. |
| Did A-01 define the deprecation model? | Yes, as a warning and legacy-use model only. |
| Did A-01 define the retention model? | Yes, as a trace/evidence/rationale model only. |
| Did A-01 execute any lifecycle change? | No. |
| Did A-01 archive, move, copy, delete, rename, transform, migrate, stage, commit, push, or publish anything? | No. |
| Did A-01 select graph or any final substrate? | No; graph remains a candidate substrate only. |
| Did A-01 start M-02 or another next ticket? | No. |
Final A-01 statement:
```text
A-01 defines lifecycle states and evidence boundaries for supersession, deprecation, and retention.
It stops before lifecycle execution, migration, product activation, external adoption, implementation, publication, Git actions, and M-02.
```
