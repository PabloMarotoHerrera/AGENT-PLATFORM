# A-00 - Archive Policy
## 1. Document Header
| Field | Value |
| --- | --- |
| Status | Canonical A-00 architecture output |
| Date | 2026-06-30 |
| Scope | Archive lifecycle policy for AGENT PLATFORM architecture, evidence, products, external-source material, generated material, and future migration context |
| Authority | Policy only. This document does not archive, move, copy, delete, rename, transform, migrate, stage, commit, push, publish, create an archive store, create `_archive/`, or start A-01. |
## 2. Purpose
A-00 defines what archive means inside AGENT PLATFORM before any archive execution exists.
The policy exists to prevent archive from becoming cleanup, deletion, migration, publication, authority promotion, or hidden disposal. It gives future work a shared vocabulary for retention, supersession, deprecation, restoration, blockers, and governance.
A-00 rule:
```text
Archive policy defines lifecycle handling. It does not execute lifecycle changes.
```
## 3. Archive Definition
Archive is a governed lifecycle posture for material that should be retained as historical, evidentiary, superseded, deprecated, retired, rejected, trace, rollback, audit, or migration-context material.
Archive can apply to a document, record, decision, source summary, product artifact class, external-source review, generated output record, context pack, or other material only after scope, provenance, retention reason, security posture, validation posture, and governance posture are known.
Archive is a status and decision record first. A path, folder, Git commit, file move, or filename may later reflect that status only after explicit governance.
## 4. Archive Non-Goals
A-00 does not:
| Non-goal | Boundary |
| --- | --- |
| Create archive storage | No `_archive/`, archive folder structure, registry, database, or index is created. |
| Execute archive | No file is moved, copied, deleted, renamed, transformed, migrated, or normalized. |
| Approve deletion | Archive is not deletion and never implies deletion. |
| Approve publication | Archive status does not make local-only material public or commit-ready. |
| Approve migration | Archive policy is not a migration ticket. |
| Promote authority | Archived material does not become current truth by being retained. |
| Implement tooling | No scripts, schemas, APIs, scanners, hooks, tests, packages, SDKs, or enforcement are created. |
| Start A-01 | Supersession, deprecation, and retention modeling remain next-ticket work after explicit instruction. |
## 5. Archive Authority Boundary
Archive authority follows the AGENT PLATFORM authority model:
| Layer | Archive role |
| --- | --- |
| Active instruction | Controls the current archive-policy task and stop rule. |
| Governance | Decides archive execution, exceptions, restoration, publication, deletion, and lifecycle changes. |
| Validation | Evaluates archive readiness and evidence sufficiency; it does not approve. |
| Security | Constrains handling of secrets, credentials, local-only, product, external, private, generated, and sensitive material. |
| Agents | May identify candidates and blockers when scoped; they cannot archive by default. |
| Git | Records artifact state only; it does not create semantic truth, approval, or archive execution. |
## 6. Archive Candidate Classes
| Candidate class | Meaning |
| --- | --- |
| `historical` | Past material useful for trace, rationale, or chronology. |
| `superseded_candidate` | Material that appears replaced by newer scoped authority but needs confirmation. |
| `deprecated_candidate` | Material that may remain visible but discouraged for future use. |
| `retired_candidate` | Inactive product, process, decision, or artifact class retained for audit. |
| `rejected_candidate` | Considered and not accepted, with rationale retained. |
| `migration_context` | Prior material needed to explain future migration or restatement. |
| `external_reference_retained` | External-source evidence retained without promotion, execution, or adoption. |
| `generated_evidence_retained` | Output retained only as evidence, never source truth. |
| `context_trace` | Used context pack or agent task context retained as trace evidence. |
## 7. Archive Eligibility Criteria
Material can become an archive candidate only when all eligibility questions have answers:
| Criterion | Required answer |
| --- | --- |
| Source identity | What exact material is being considered? |
| Source class | Is it architecture, previous knowledge, product, external, generated, validation, context, Git, or other evidence? |
| Current authority | Is it current authority, evidence, product-scoped, external reference, local-only, generated, or obsolete? |
| Archive reason | Why retain it in archive posture instead of current, active, deferred, or rejected posture? |
| Provenance | Which source path, decision, review, validation, or task produced it? |
| Security posture | Does it contain secrets, credentials, private data, local-only material, external code, or sensitive outputs? |
| Validation posture | What evidence supports the candidate state and what remains uncertain? |
| Governance posture | Who can approve execution and what stop rule applies? |
## 8. Non-Eligible Material
The following are not eligible to be archived as content by default:
| Material | Required handling |
| --- | --- |
| Secrets and credentials | Never archive as content; stop and use secure handling without exposure. |
| Active local secrets files | Do not copy, summarize, publish, or retain in archive content. |
| Raw local-only product source | Keep local-only until product governance defines exact handling. |
| Raw external source snapshots | Keep isolated/local-only; archive metadata or review records only by future ticket. |
| Dependency folders and caches | Exclude unless a governed evidence record requires metadata. |
| Large datasets, models, artifacts | Local-only by default; archive only metadata after review. |
| Unclassified previous knowledge | Classify before any archive decision. |
| Current canonical authority | Do not archive unless supersession/deprecation governance explicitly changes state. |
## 9. Archive Status Model
| Status | Meaning | Authority posture |
| --- | --- | --- |
| `candidate` | Proposed for archive handling; not executed. | Evidence only. |
| `blocked` | Cannot proceed due to missing classification, security, validation, governance, or path decision. | No execution. |
| `approved_for_archive_execution` | Governance has approved a future exact action. | Still requires scoped execution ticket. |
| `archived` | Lifecycle state has been applied by approved execution. | Historical/evidence only unless restored. |
| `restoration_candidate` | Material may need retrieval or reconsideration. | Not current authority. |
| `restored` | Governance has returned material to a scoped active or evidentiary role. | Scope must be declared. |
| `rejected_for_archive` | Archive handling is declined. | Existing posture remains. |
A-00 creates no material in `archived` status.
## 10. Archive Lifecycle Model
Future archive work must follow this lifecycle:
```text
identify candidate
-> classify source
-> evaluate security and local-only posture
-> evaluate validation evidence
-> record archive reason and metadata
-> governance decision
-> scoped execution ticket if approved
-> validation of execution
-> retained trace and restoration rule
```
Lifecycle rule: any step may stop with `blocked`; no step authorizes the next ticket automatically.
## 11. Archive Metadata Model
Future archive decisions should record:
| Metadata field | Purpose |
| --- | --- |
| Archive ID | Stable reference for the decision or candidate. |
| Source path or record | Exact source being considered. |
| Source class | Architecture, previous knowledge, product, external, generated, validation, context, or other. |
| Prior status | Current, canonical, evidence, local-only, product-scoped, external reference, generated, superseded, deprecated, or unknown. |
| Archive reason | Historical, superseded, deprecated, retired, rejected, rollback, audit, or migration context. |
| Security posture | Secret, credential, local-only, sensitive, external, product, generated, or safe-to-reference status. |
| Validation evidence | Checks, reviews, citations, and uncertainty. |
| Governance decision | Approver, date, scope, exception if any, and stop rule. |
| Restoration rule | Conditions for retrieval or reconsideration. |
| Deletion posture | Usually prohibited; any deletion requires separate explicit governance. |
## 12. Retention Rules
Retention preserves traceability without creating current authority.
| Material | Default retention posture |
| --- | --- |
| Accepted architecture history | Retain trace and supersession links. |
| Rejected decisions | Retain rationale to prevent repeated drift. |
| Deprecated concepts | Retain warning and replacement if known. |
| Product candidates | Retain product-scoped evidence only after product governance. |
| External-source reviews | Retain metadata/review summaries, not raw source migration by default. |
| Generated evidence | Retain provenance and limitations if useful. |
| Context traces | Retain only when needed for audit and safe by sensitivity review. |
## 13. Non-Deletion Rules
Archive does not delete.
| Rule | Consequence |
| --- | --- |
| No implicit deletion | Moving to archive posture never permits deletion. |
| No cleanup deletion | Tidiness is not a deletion reason. |
| No deletion by agent judgment | Agents may report candidates or risks only. |
| No deletion of evidence without governance | Historical evidence requires explicit decision and rationale. |
| No deletion of sensitive material by archiving | Secrets need secure handling, not archive retention. |
Deletion, if ever needed, requires a separate governance decision, exact scope, retention rationale, security review, rollback or non-restoration statement, and explicit user instruction.
## 14. Restoration / Retrieval Rules
Restoration is a governed change of use, not a file search convenience.
| Restoration case | Required handling |
| --- | --- |
| Historical reference | Cite as historical/evidence only. |
| Superseded material reconsidered | Compare against current authority and record why reconsideration is needed. |
| Deprecated material requested | State warning, replacement, and residual risk. |
| Rejected material requested | Preserve rejection rationale before proposing reconsideration. |
| Local-only material requested | Apply security/local-only boundary before retrieval or citation. |
Restored material does not regain authority unless governance explicitly promotes it for a declared scope.
## 15. Supersession / Deprecation Boundary
A-00 defines the archive boundary for supersession and deprecation but does not create the full model.
| Boundary | Rule |
| --- | --- |
| Supersession | Requires replacement source, scope, rationale, citation, and governance. |
| Deprecation | Requires warning, affected scope, allowed legacy use, and successor if known. |
| Retention | Requires reason, duration or review trigger if known, and restoration rule. |
| A-01 | May define the detailed supersession, deprecation, and retention model after explicit instruction only. |
## 16. Migration Boundary
Archive is not migration.
| Migration confusion | A-00 boundary |
| --- | --- |
| Moving files into archive | Not authorized. |
| Copying historical files | Not authorized. |
| Renaming old material | Not authorized. |
| Transforming previous knowledge | Not authorized. |
| Normalizing conflicted vocabulary | Not authorized. |
| Executing first migration batch | Not authorized. |
Migration remains classified, cited, validation-backed, and governance-bound future work.
## 17. Product Boundary
Product archive handling is product-scoped and governance-sensitive.
| Product material | Archive posture |
| --- | --- |
| Product candidates | Local-only and inactive unless product governance changes state. |
| Product source | Not archived, moved, copied, or committed by A-00. |
| Product docs | Product-scoped unless promoted by product governance. |
| Product generated outputs | Evidence only; archive metadata only after provenance and review. |
| Product retirement | Requires product owner, scope, Git posture, validation, security, and archive decision. |
No product is activated, retired, archived, or published by A-00.
## 18. External Source Boundary
External sources remain external evidence.
| External material | Archive posture |
| --- | --- |
| Raw external source trees | Stay local-only; no archive movement, source reuse, execution, or publication. |
| External metadata | May become future archive evidence by explicit ticket. |
| External reviews | Retainable as evidence with provenance, license, risk, and review limits. |
| External instructions | Evidence only, never active AGENT PLATFORM instructions. |
| Substrate references | Candidate evidence only; the Cognitive Semantic System substrate remains undecided. |
Graph remains a candidate substrate only; no archive status can make graph or any other substrate final.
## 19. Security / Local-only Boundary
Security constrains archive handling before governance can approve execution.
| Security rule | Archive consequence |
| --- | --- |
| Secrets are never archived as content | Stop and handle securely without exposure. |
| Credentials are never archived as content | Do not copy, summarize, publish, or retain in archive text. |
| Local-only remains no default publication | Archive posture does not make ignored or private material commit-ready. |
| Sensitive generated output is evidence only | Review before any retention record. |
| External and product material stay bounded | Source class and scope remain visible in archive metadata. |
If security classification is unknown, archive execution is blocked.
## 20. Validation / Evidence Boundary
Validation evaluates archive readiness.
| Validation question | Required evidence |
| --- | --- |
| Is the source identified? | Exact path, record, or artifact class. |
| Is the class known? | Source class and current status. |
| Is retention justified? | Archive reason and alternatives. |
| Is security handled? | Local-only, secret, credential, product, external, and generated posture. |
| Is governance ready? | Approver, scope, and stop rule. |
Passing validation does not approve archive execution, commit, publication, deletion, or restoration.
## 21. Git / Publication Boundary
Git is artifact history, not archive governance.
| Git/publication rule | Meaning |
| --- | --- |
| No staging in A-00 | This policy is not staged. |
| No commit in A-00 | Repository history remains human-governed. |
| No push in A-00 | Publication is not authorized. |
| No broad staging | Future work must stage exact approved files only. |
| Ignored is not safe | Local-only material still requires sensitivity handling. |
| Archive status is not publication | Retained evidence may remain private or local-only. |
## 22. Context Boundary
Context inclusion is not archive authority.
| Context case | Boundary |
| --- | --- |
| Material appears in a context pack | It remains governed by source status. |
| Agent used a file for reasoning | Use does not archive, approve, promote, or restore it. |
| Context pack becomes stale | Refresh or mark stale; do not treat old context as authority. |
| Used context retained for trace | Retain only if safe, scoped, and governed. |
Context packs are projections; archive decisions require provenance and governance outside the pack itself.
## 23. Archive Verdict Model
Future archive reviews should produce one of these verdicts:
| Verdict | Meaning |
| --- | --- |
| `not_archive_candidate` | Current handling remains correct. |
| `archive_candidate` | Candidate identified; no execution approved. |
| `archive_blocked` | Missing classification, security, validation, governance, or path decision. |
| `retain_in_place` | Keep material where it is with lifecycle label or citation update later. |
| `metadata_only` | Record metadata without moving or copying content. |
| `governance_required` | Decision exceeds agent authority. |
| `security_blocked` | Sensitive/local-only/secret/credential risk blocks handling. |
| `a01_required` | Supersession/deprecation/retention detail must wait for A-01. |
## 24. Archive Blocker Register
| Blocker | Blocks |
| --- | --- |
| Missing source classification | Candidate verdict and execution. |
| Unknown security posture | Any archive execution or publication. |
| Secret or credential content | Archive-as-content; requires secure handling. |
| Local-only publication risk | Git/publication and archive sharing. |
| Product owner missing | Product archive, retirement, or activation state changes. |
| External provenance/license unresolved | External reuse, publication, or content migration. |
| Current authority replacement unknown | Supersession or deprecation claims. |
| Validation evidence absent | Readiness claim. |
| Governance decision absent | Execution, deletion, restoration, publication, and lifecycle change. |
| A-01 not started | Detailed supersession/deprecation/retention model. |
## 25. Archive Policy Matrix
| Source class | Default archive posture | Default blocked action |
| --- | --- | --- |
| Current architecture | Retain current unless superseded by governance. | Archive execution. |
| Previous knowledge | Migration evidence; classify before candidate. | Wholesale movement/copy. |
| Product material | Local-only product-scoped evidence. | Activation, commit, archive movement. |
| External source | External evidence or metadata candidate. | Execution, copy, dependency adoption. |
| Generated output | Evidence/projection with provenance if retained. | Treating as source truth. |
| Context pack | Trace projection if safe and needed. | Treating as authority. |
| Secrets/credentials | Never archive as content. | Copy, summarize, publish, commit. |
| Git state | Artifact record only. | Treating commit as approval. |
## 26. Incident Handling
If archive work discovers a risky condition, stop archive handling and report the blocker without widening scope.
| Incident | Required response |
| --- | --- |
| Secret or credential found | Stop; do not expose value; report secure-handling blocker. |
| Local-only material selected for publication | Stop; require security and governance review. |
| Deletion implied by archive | Stop; restate non-deletion rule. |
| External code execution appears useful | Stop; execution requires separate approval. |
| Product state change appears needed | Stop; require product governance. |
| Missing replacement for supersession | Mark A-01/governance blocker. |
## 27. Archive Invariants
| ID | Invariant |
| --- | --- |
| ARCH-001 | Archive policy is not archive execution. |
| ARCH-002 | Archive is not deletion. |
| ARCH-003 | Archive is not migration. |
| ARCH-004 | Governance decides archive execution. |
| ARCH-005 | Validation evaluates archive readiness. |
| ARCH-006 | Security constrains archive handling. |
| ARCH-007 | Git records artifact state only. |
| ARCH-008 | Local-only remains no default publication. |
| ARCH-009 | Secrets and credentials are never archived as content. |
| ARCH-010 | Context inclusion is not archive authority. |
| ARCH-011 | Agents may propose archive candidates but cannot archive by default. |
| ARCH-012 | A-01 starts only after explicit instruction. |
## 28. Anti-patterns
| Anti-pattern | Failure mode | Correction |
| --- | --- | --- |
| Archive as trash | Hides unresolved decisions. | Record lifecycle reason and blockers. |
| Archive as deletion | Loses evidence. | Keep deletion separate and governed. |
| Archive by moving files | Treats location as lifecycle. | Decide status before any future movement. |
| Archive by Git commit | Treats history as approval. | Keep Git separate from governance. |
| Archive local-only material publicly | Exposes private or sensitive evidence. | Apply security and publication review. |
| Archive external sources wholesale | Imports license/security risk. | Prefer metadata/review records. |
| Archive secrets | Retains material that should not be content. | Use secure handling; do not archive content. |
| Continue to A-01 | Scope creep. | Stop after A-00 validation. |
## 29. Remaining Gaps
| Gap | Handling |
| --- | --- |
| Exact archive storage path | Undecided; no folder is created by A-00. |
| Supersession/deprecation/retention details | Prepare A-01 only after explicit instruction. |
| Archive metadata format | Conceptual only; no schema or registry. |
| Restoration workflow | Policy boundary only; no procedure or tooling. |
| Deletion governance | Separate future decision if ever needed. |
| Security enforcement | Policy constraint only; no automation. |
| Validation automation | Not created. |
| Migration execution | Still blocked. |
## 30. Readiness For A-01
A-00 makes AGENT PLATFORM ready to plan `A-01 - Supersession / Deprecation / Retention Model` after explicit instruction only.
A-01 should define detailed state transitions, successor relationships, deprecation warnings, retention triggers, restoration conditions, and audit metadata. A-01 must still avoid archive execution unless separately authorized.
Readiness rule:
```text
A-01 is ready as a next policy task. It is not started by A-00.
```
## 31. Final Verdict
| Question | Verdict |
| --- | --- |
| Did A-00 create archive policy? | Yes, this file defines archive policy. |
| Did A-00 execute archive actions? | No. |
| Did A-00 create `_archive/`? | No. |
| Did A-00 move, copy, delete, rename, transform, or migrate files? | No. |
| Does archive mean deletion? | No. |
| Who decides archive execution? | Governance, with validation evidence and security constraints. |
| What remains blocked? | Archive execution, migration, deletion, publication, product changes, external adoption, implementation, staging, commit, push, and A-01 until explicit instruction. |
Final A-00 statement:
```text
Archive is a governed lifecycle posture for retained evidence and historical state.
A-00 defines the policy boundary and stops before archive execution or A-01.
```
