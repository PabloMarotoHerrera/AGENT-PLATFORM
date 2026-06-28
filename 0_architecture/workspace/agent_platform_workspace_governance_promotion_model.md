# AGENT PLATFORM Workspace Governance and Promotion Model

Status: Canonical W-11 workspace output  
Date: 2026-06-28  
Scope: Governance, decision, lifecycle, and promotion model for AGENT PLATFORM  
Authority: Governance and promotion architecture only. This document does not implement governance automation, enforce permissions, move files, rename folders, migrate documents, run external code, install dependencies, authenticate services, stage, commit, push, or create W-12.

## 1. Purpose

This document defines how AGENT PLATFORM governs evidence, claims, proposals, decisions, documentation, migrations, external-source reuse, product workspaces, validation outputs, agent outputs, generated outputs, and future authority promotion.

Governance and promotion come after W-10 because W-10 defines agent behavior boundaries. Agents can inspect, classify, draft, validate when scoped, and propose. They cannot approve, promote, publish, migrate, decide substrate, or change repository history by themselves.

Clarifications:

| Clarification | Rule |
| --- | --- |
| Agents can propose but not approve. | Agent output is evidence or recommendation until a human or governance process accepts it. |
| Validation evaluates but does not govern. | Validation can support, block, or qualify a promotion, but governance decides authority-sensitive outcomes. |
| Documentation status is not enough by itself. | A status label must be backed by scope, owner, evidence, validation posture, governance posture, and lifecycle handling. |
| Git commits are not governance approval. | Git history records artifacts and changes; it does not create semantic truth or promotion by itself. |
| Context inclusion is not promotion. | A context pack can expose material for a task without making it authoritative. |
| External source presence is not promotion. | A cloned source, external README, license file, or generated report remains evidence until reviewed and promoted. |
| Promotion is scoped. | Accepted material governs only the declared scope. |
| The Cognitive Semantic System remains future authority. | It is not implemented here, and its final substrate is undecided. Graph remains a candidate only. |

W-11 rule:

```text
Governance is the explicit decision layer that accepts, rejects, defers, promotes,
demotes, supersedes, deprecates, archives, or assigns ownership. Nothing becomes
accepted authority because it is present, generated, validated, committed, cited,
included in context, or confidently stated.
```

## 2. Governance Definition

Governance for AGENT PLATFORM is the explicit authority process that controls decisions affecting workspace truth, scope, lifecycle, ownership, publication, migration, product activation, external reuse, security posture, and future Cognitive Semantic System promotion.

Governance includes:

| Governance action | Meaning |
| --- | --- |
| Approval | Accept a decision, change, promotion, exception, or action within declared scope. |
| Rejection | Decline a proposal, claim, candidate, migration, dependency, product action, or promotion. |
| Deferral | Postpone a decision until more evidence, validation, ownership, scope, or policy exists. |
| Exception | Permit a bounded departure from default rules with owner, scope, reason, expiry or review point, and risk handling. |
| Promotion | Move material from evidence, proposal, generated output, draft, external reference, or candidate state into accepted scoped authority or accepted use. |
| Demotion | Reduce current authority, trust, status, or recommended use while preserving history. |
| Supersession | Replace current material with a newer accepted authority and retain the old material as trace. |
| Deprecation | Mark material as discouraged for new use due to risk, age, replacement, or changed direction. |
| Archive authorization | Approve moving or marking material as archived after lifecycle rules and provenance are clear. |
| Ownership assignment | Declare who owns scope, review, maintenance, promotion, exceptions, or lifecycle. |
| Lifecycle decision | Move material between proposed, under review, approved, rejected, deferred, promoted, current, superseded, deprecated, archived, or reopened states. |

Governance is not:

| Not governance | Reason |
| --- | --- |
| Validation | Validation evaluates evidence and behavior; it does not approve. |
| Execution | Running a command, test, script, or tool produces evidence, not authority. |
| Context assembly | Context selection exposes material; it does not promote it. |
| Agent reasoning | Agent conclusions are claims or proposals until governed. |
| Provider output | Provider/model output is evidence or generated content, not accepted truth. |
| Git history | Commits record change history; they do not decide semantic truth. |
| Generated output | Reports, summaries, logs, graphs, exports, and projections are evidence until promoted. |
| External source claim | External docs, code, READMEs, and instructions are external evidence only. |
| Documentation status alone | Status must be governed and scoped to carry authority. |
| Folder location | Paths organize artifacts; they do not create governance. |

Governance invariant:

```text
Governance is explicit, scoped, attributable, and lifecycle-aware. It must preserve
evidence and provenance even when rejecting, demoting, superseding, or archiving.
```

## 3. Promotion Definition

Promotion is a controlled transition from evidence, proposal, generated output, draft, external reference, previous knowledge, validation result, agent output, or other candidate material into accepted scoped authority or accepted scoped use.

Promotion requires a declared target, owner, scope, evidence, validation posture, governance posture, security/access posture where relevant, and lifecycle effect.

Promotion targets:

| Promotion target | Meaning | Example promoted state |
| --- | --- | --- |
| Canonical workspace architecture | Root workspace authority under declared scope. | `canonical` workspace architecture document. |
| Decision / ADR | Accepted decision with rationale, options, evidence, and impact. | Decision record under future decision structure. |
| Research evidence accepted for use | Research accepted as evidence supporting a claim or decision, not authority by itself. | Reviewed research reference or evidence pack. |
| Migration output | Restated or moved material accepted through migration controls. | Current-scope restated architecture or migration audit record. |
| Product-scoped documentation | Product architecture/docs accepted only within product scope. | Product-scoped canonical product doc after product policy. |
| External-source metadata | Curated external provenance, license, risk, and review metadata. | External review or registry update, not dependency approval unless separately governed. |
| Implementation plan | Accepted implementation direction before code. | Implementation plan with validation/security gates. |
| Validation result | Validation evidence accepted for a decision or promotion record. | Retained validation reference. |
| Human-facing projection | Documentation projection accepted as an explanation of source authority. | Reviewed `6_docs/` guide, still projection unless promoted otherwise. |
| Future Cognitive Semantic System record | Accepted semantic record when future system exists. | Scoped accepted semantic truth, not implemented by W-11. |

Promotion rule:

```text
Promotion changes authority or accepted-use posture. It must be deliberate,
traceable, scoped, and reversible in understanding even when not reversible in Git.
```

## 4. Governance Objects

Governance can act on the following objects.

| Object | Default state | Possible governance action | What cannot happen automatically |
| --- | --- | --- | --- |
| Evidence | Evidence only. | Accept for use, reject as insufficient, defer, archive, cite, request validation. | Become truth by existence, frequency, recency, or inclusion. |
| Claim | Unaccepted statement. | Validate, accept, reject, defer, scope, revise, promote into decision/doc. | Become decision because it is plausible or confidently stated. |
| Proposal | Candidate recommendation. | Approve, reject, defer, revise, require evidence, require validation. | Become policy because an agent wrote it. |
| Decision | Accepted choice only after governance. | Approve, supersede, deprecate, reopen, archive. | Apply outside declared scope. |
| Document | Artifact with status and scope. | Promote status, demote, supersede, deprecate, archive, request revision. | Become canonical by filename or folder. |
| Context Pack | Projection for task context. | Approve for task use, mark stale, regenerate, archive as trace. | Become source, permission, truth, or promotion. |
| Migration Candidate | Candidate source or concept for movement/restatement. | Approve migration, reject, defer, require restatement, require audit. | Move, copy, rename, archive, or commit itself. |
| External Source | External evidence. | Approve metadata, approve pattern adoption, restrict, reject reuse, require review. | Become dependency, active instruction, or architecture by proximity. |
| Product Workspace | Bounded product candidate. | Activate, defer, retire, scope, assign owner, set Git posture. | Define root authority or become tracked by default. |
| Validation Result | Evaluation evidence. | Accept as support, reject as insufficient, require rerun, retain, qualify promotion. | Approve promotion or commit by itself. |
| Agent Output | Agent-produced evidence or recommendation. | Accept as evidence, request revision, reject, use as proposal input. | Become governance, validation approval, or semantic truth. |
| Generated Output | Tool/model/script output. | Review, validate, cite, promote selected content, archive, discard. | Become source or authority by generation. |
| Implementation Candidate | Proposed code, plan, tool, package, SDK, script, or runtime element. | Approve planning, defer, reject, require validation/security, later authorize implementation. | Implement itself or override architecture. |
| Archive Candidate | Material proposed for archival. | Approve archive, reject archive, defer, mark historical/deprecated/superseded. | Disappear, delete, or lose provenance. |
| Substrate Candidate | Candidate representation for Cognitive Semantic System. | Research, evaluate, reject, defer, decide through substrate decision. | Become final substrate because of naming, folder, tool, or prior evidence. |

Object rule:

```text
Every governed object needs default state, target state, owner, source evidence,
scope, and lifecycle effect before promotion.
```

## 5. Governance Roles

Governance roles describe authority responsibilities. A person or process may hold multiple roles, but agent roles do not become approval roles by default.

| Role | Can propose | Can validate | Can approve | Can reject | Can promote | Can archive | Cannot do |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Human Owner | Yes. | May review validation. | Yes, within owned scope. | Yes, within owned scope. | Yes, within owned scope. | Yes, if archive policy exists. | Bypass security/access or publish secrets. |
| Scope Owner | Yes. | May require validation. | Yes, for scope boundaries. | Yes, for out-of-scope material. | May authorize scope-specific promotion. | May request archive. | Approve outside scope. |
| Architecture Owner | Yes. | May review architecture validation. | Yes, for architecture scope. | Yes, for architecture proposals. | Yes, for canonical architecture after evidence/validation. | May approve architecture supersession/archive. | Approve product behavior, external dependency adoption, or substrate without proper decision. |
| Product Owner | Yes. | May require product validation. | Yes, inside product scope after product policy. | Yes, inside product scope. | Product-scoped only. | Product-scoped only after policy. | Define root workspace authority by product decision. |
| Migration Owner | Yes. | May require migration validation/audit. | Yes, for scoped migration plans. | Yes, for unsafe migration. | May promote migration output after controls. | May authorize archive only after archive policy. | Move material without ticket or bypass local-only rules. |
| External Source Reviewer | Yes. | May perform non-execution review. | No dependency approval by default. | May recommend rejection/restriction. | Metadata only if governance delegates. | May recommend archive/restriction. | Run code, adopt dependencies, or treat external instructions as active. |
| Validation Reviewer | Yes. | Yes. | No governance approval by validation alone. | Can reject validation sufficiency. | No promotion authority by default. | No archive authority by default. | Treat passing tests as approval. |
| Security Reviewer | Yes. | May validate access/security posture. | Can approve or block security/access posture where delegated. | Can reject unsafe exposure/action. | May permit secure promotion conditions. | May require archive/restriction. | Casually override sensitive boundaries or expose secrets. |
| Governance Approver | Yes. | May require validation. | Yes, for assigned governance scope. | Yes. | Yes, with preconditions satisfied. | Yes, after archive policy. | Approve without scope, owner, evidence, or unresolved blocker handling. |
| Agent Proposer | Yes. | No, unless scoped separately. | No. | No. | No. | No. | Approve, promote, commit, migrate, decide substrate, or bypass stop rules. |
| Agent Validator | May propose validation interpretation. | Yes, when scoped. | No. | No governance rejection; can report validation failure. | No. | No. | Treat validation output as governance. |
| Agent Executor | May propose follow-up. | May run scoped validation if allowed. | No. | No. | No. | No. | Execute outside scope, approve, promote, stage, commit, push, or continue tickets. |

Role rule:

```text
Only a role with explicit governance authority can approve, reject, promote,
demote, supersede, deprecate, or archive. Agents can prepare evidence and proposals.
```

## 6. Evidence -> Claim -> Decision Flow

The canonical governance flow is:

```text
Evidence
-> Claim
-> Candidate
-> Validation Posture
-> Governance Review
-> Decision
-> Promotion / Rejection / Deferral
-> Lifecycle State
-> Learning
```

Flow semantics:

| Step | Meaning | Required control |
| --- | --- | --- |
| Evidence | Source material, observations, outputs, research, previous docs, external sources, validation results, or agent output. | Source class, status, scope, provenance, and sensitivity known. |
| Claim | Statement formed from evidence. | Claim cites evidence and uncertainty. |
| Candidate | Claim or material proposed for acceptance, action, migration, reuse, documentation, or promotion. | Owner, target scope, intended outcome, and blockers declared. |
| Validation Posture | Evaluation of evidence, claim, artifact, or behavior. | Validation scope, result, command/review, and limitations recorded. |
| Governance Review | Approval-capable role reviews preconditions, evidence, validation, security, ownership, and impact. | No unresolved blocker; exceptions explicit. |
| Decision | Accepted, rejected, deferred, scoped, excepted, or returned-for-more-evidence outcome. | Decision record or governance artifact when material. |
| Promotion / Rejection / Deferral | Candidate becomes accepted scoped authority/use, rejected evidence, or deferred. | Lifecycle state and trace recorded. |
| Lifecycle State | Current, superseded, deprecated, archived, reopened, or other governed state. | Provenance and replacement/retention rules preserved. |
| Learning | Reviewed outcome improves future rules, context, docs, or processes. | Learning is accepted only after review; it does not rewrite history. |

Flow rules:

| Rule | Meaning |
| --- | --- |
| No transition is automatic. | Evidence does not become a claim; claim does not become a decision; validation does not become approval. |
| Validation can block or support. | Failed, missing, stale, or partial validation can block promotion or require qualification. |
| Governance can approve, reject, defer, or require more evidence. | Governance is not forced by validation results. |
| Learning requires reviewed outcome. | Raw memory, repeated behavior, or agent preference is not durable learning by itself. |

## 7. Decision Types

| Decision type | Scope | Required evidence | Required validation | Required approver | Output artifact |
| --- | --- | --- | --- | --- | --- |
| Workspace Decision | Root workspace policy, topology, authority, Git posture, or cross-area boundary. | W-series authority, source evidence, impact analysis. | Validation of affected files/paths/status where applicable. | Human Owner, Scope Owner, or Governance Approver. | Decision record or canonical workspace doc. |
| Architecture Decision | Architecture boundaries, domains, models, documentation structure, context, agent, runtime, or semantic authority. | Current W-series docs, prior evidence, alternatives, risks. | Architecture consistency review; validation if artifacts change. | Architecture Owner or Governance Approver. | ADR/decision record or canonical architecture doc. |
| Documentation Decision | Status, scope, lifecycle, projection, supersession, or docs target. | W-09 status/scope model, source citations. | Link/status/citation review. | Architecture Owner, Documentation Owner if assigned, or Governance Approver. | Doc update, decision record, or status/lifecycle record. |
| Migration Decision | Restatement, movement, archive candidate, previous knowledge extraction, or local-only handling. | W-02/W-08 classifications, source paths, target scope, risk register. | Migration validation and audit plan. | Migration Owner and relevant Scope Owner. | Migration record, audit reference, or migrated/restated artifact. |
| External Source Decision | External metadata, pattern adoption, dependency adoption, or execution approval. | W-03 registry, source review, provenance, license, security risk. | Non-execution review first; security/dependency validation for adoption. | External Source Reviewer plus Governance/Security Approver. | External review, approval/rejection record, dependency decision if allowed. |
| Product Workspace Decision | Product activation, ownership, Git posture, product docs, product dependencies, product retirement. | Product scope evidence, root constraints, product files if scoped. | Product validation as relevant. | Product Owner plus Scope/Governance Approver for root-impacting choices. | Product policy/decision record. |
| Validation Decision | Validation method, proof level, evidence retention, rerun requirement, or sufficiency posture. | Validation output, commands, logs, expected proof level. | Validation review itself. | Validation Reviewer; Governance Approver for promotion effect. | Validation reference or sufficiency record. |
| Security/Access Decision | Secrets, credentials, sensitive data, network, provider auth, external execution, publication. | Risk evidence, source classification, sensitivity, exposure path. | Security review and, where needed, controlled validation. | Security Reviewer and Governance Approver. | Security review reference or access decision. |
| Implementation Decision | Implementation plan, code start, package/tool/test/SDK adoption, runtime behavior. | Architecture readiness, implementation plan, tests/security needs. | Validation plan and readiness checks. | Architecture Owner plus Implementation/Scope Owner. | Implementation decision or plan. |
| Archive Decision | Archive path, lifecycle, superseded/deprecated/retired material, restoration. | Source path, reason, replacement, lifecycle impact. | Link/provenance validation. | Governance Approver and relevant owner. | Archive record after archive policy exists. |
| Substrate Decision | Cognitive Semantic System representation or storage approach. | Substrate evaluation across graph, relational, document, vector, event-sourced, hybrid, and other options as applicable. | Architecture, validation, security, migration, and implementation feasibility review. | Governance Approver plus Architecture Owner. | Explicit substrate decision record. |

Decision rule:

```text
The higher the scope and reversibility risk, the stronger the evidence,
validation, security, and approval requirements.
```

## 8. Promotion Preconditions

Promotion cannot proceed unless these preconditions are satisfied or explicitly marked not applicable by governance.

| Precondition | Required posture |
| --- | --- |
| Source status known | Canonical, draft, proposal, research, evidence, migration evidence, external reference, product-scoped, generated, historical, or other W-09 status. |
| Scope declared | Workspace root, architecture domain, product workspace, research, external source, migration, operations, implementation, human docs, or local-only scope. |
| Owner declared | Responsible human, role, owner, reviewer, or governance placeholder. |
| Evidence cited | Source paths, W-series docs, W-02 state, W-03 registry, validation, product evidence, or other provenance. |
| Validation posture known | Validated, failed, partial, stale, not run, blocked, or explicitly not applicable. |
| Governance posture known | Proposed, under review, approved, rejected, deferred, exception, or not applicable. |
| Security/access posture known | Sensitive, restricted, safe to expose, not reviewed, no secrets, or requires security review. |
| Migration impact known | No migration, restatement only, move/copy/rename/archive candidate, local-only effect, or audit need. |
| External/license posture known | Required for external claims, metadata, dependencies, execution, or reuse. |
| Product scope known | Required for product docs, source, validation, dependencies, activation, or retirement. |
| Stop rule obeyed | Agent/task stopped before next ticket, commit, migration, execution, or promotion unless authorized. |
| No unresolved blocker | Naming, scope, ownership, validation, security, license, product, external, migration, or substrate blockers resolved or deferred explicitly. |

Promotion precondition rule:

```text
Missing preconditions do not always reject a candidate, but they block promotion
until governance explicitly resolves, defers, or scopes them.
```

## 9. Rejection / Deferral / Demotion

Governance handles negative or non-final outcomes without erasing evidence.

| Outcome | Meaning | Required handling |
| --- | --- | --- |
| Rejection | Candidate is not accepted for the requested scope or use. | Preserve evidence, rationale, rejecting authority, and future reconsideration conditions if any. |
| Deferral | Candidate is postponed. | State missing evidence, validation, owner, policy, security review, or decision dependency. |
| Demotion | Current authority or accepted use is reduced. | Preserve prior authority history, reason, and new status. |
| Supersession | Newer authority replaces older material. | Point to replacement, preserve old source, update citations where future work depends on it. |
| Deprecation | Material remains known but discouraged. | Explain risk, replacement, expiry/review point if any. |
| Archive | Material is retired and retained for audit/reference. | Requires archive policy, archive record, provenance, reason, and restoration rule. |
| Rollback | Return to a previous state or undo a governed action where possible. | Requires provenance, affected artifacts, reason, risk review, and validation of restored posture. |

Clarifications:

| Clarification | Rule |
| --- | --- |
| Rejection does not erase evidence. | Rejected material may remain useful history. |
| Demotion changes currentness, not history. | Prior authority should remain traceable. |
| Archive is not trash. | Archive retains lifecycle and provenance. |
| Supersession points to replacement. | Future readers must know which authority replaced which material. |
| Rollback requires provenance. | Reverting without trace creates governance drift. |

## 10. Documentation Governance

Documentation governance uses W-09 status and scope labels, but status changes require governance posture.

| Documentation status | Who can change status | Evidence required | Supersession/staleness handling |
| --- | --- | --- | --- |
| `canonical` | Architecture Owner, Product Owner for product scope, or Governance Approver. | Source evidence, scope, owner, citations, validation posture, governance approval. | Review when dependencies change; supersede explicitly. |
| `draft` | Document owner or scoped agent by ticket. | Draft source and intended scope. | May be revised, promoted, rejected, or abandoned. |
| `proposal` | Proposal owner or Governance Approver. | Problem, options, evidence, rationale, impacts. | Accept, reject, defer, or supersede with record. |
| `research` | Research owner or reviewer. | Sources, method, uncertainty, date/freshness. | Promote only through proposal/decision path. |
| `evidence` | Evidence owner, reviewer, or governance role. | Source, provenance, relevance, uncertainty. | Retain, reject as insufficient, archive, or cite. |
| `projection` | Documentation/context owner. | Source authority and projection method. | Mark stale when source authority changes. |
| `migration_evidence` | Migration Owner. | Original path, W-02 state, migration use. | Preserve; restate rather than overwrite. |
| `external_reference` | External Source Reviewer or Governance Approver. | W-03 entry, source provenance, license/risk posture. | Review, restrict, reject reuse, or promote metadata. |
| `product_scoped` | Product Owner plus product policy. | Product scope, product evidence, root constraints. | Cannot become root authority without root decision. |
| `implementation_note` | Implementation owner after implementation scope exists. | Source files, tests, architecture constraints. | Cannot override architecture. |
| `generated` | Task owner or reviewer. | Generator, inputs, command/method, review status. | Promote selected content only after review. |
| `historical` | Governance or migration owner. | Original source and historical reason. | Preserve; do not treat as current. |
| `superseded` | Owner of replacement authority or Governance Approver. | Replacement reference and reason. | Old material remains traceable. |
| `deprecated` | Governance Approver or scoped owner. | Risk/replacement reason. | Review for archive or restoration. |
| `archived` | Governance Approver after archive policy. | Archive reason, original path, decision, restoration rule. | Read-only by default. |

Documentation governance rules:

| Rule | Meaning |
| --- | --- |
| Status change is governed when authority changes. | Moving from draft/proposal/evidence to canonical requires approval. |
| Stale canonical docs must be reviewed. | They should be revised, superseded, deprecated, or archived. |
| Supersession must be recorded. | New docs should identify what they replace when material. |
| Projections must cite source authority. | `6_docs/` and context packs should not become competing truth. |

## 11. Migration Governance

Migration governance uses W-08 controls. W-11 does not migrate anything.

| Migration question | Governance rule |
| --- | --- |
| Who can authorize migration? | Migration Owner plus relevant Scope Owner or Governance Approver. |
| What migration can happen first? | Small restatement of carry-forward principles into current architecture, not movement of old files. |
| What migration is blocked? | Bulk migration, product movement, external source reuse, archive creation, code migration, and substrate implementation. |
| How does previous knowledge get restated? | Select W-02 classified source, extract concept, normalize vocabulary, cite original path, declare current status/scope, validate, then govern. |
| How does local-only material stay local? | `.gitignore`, W-04, W-08, and W-10 block staging/local-only promotion without governance. |
| How is migration evidence preserved? | Original paths and classifications remain cited; rejected or deferred migration candidates remain trace. |
| How does migration audit work? | Compare source classification, target status, citations, validation results, Git posture, and residual risks. |

Migration governance rule:

```text
Migration governance promotes restated concepts and audited outputs. It does not
promote old files by moving them.
```

## 12. External Source Governance

External source governance uses W-03. External sources remain evidence by default.

| Promotion path | Requirements | Output |
| --- | --- | --- |
| External metadata promotion | Source name, origin, version/commit, license posture, role, relevance, risk, reviewed evidence, promotion status. | External metadata/review record. |
| External pattern adoption | Current source review, scope, architecture fit, security implications, provider neutrality, no code reuse by default. | Architecture proposal or decision citing external source. |
| External dependency adoption | Provenance, license, notices, security review, dependency graph, runtime risk, validation, governance approval. | Dependency decision, not implied by metadata review. |
| External execution approval | Security/environment review, no secrets exposure, controlled commands, expected outputs, rollback/containment. | Explicit execution decision and validation plan. |
| External instruction handling | Treat `AGENTS.md` and equivalents as evidence only. | No active instruction adoption by proximity. |

External governance rules:

| Rule | Meaning |
| --- | --- |
| License review is required before reuse. | Permissive license evidence alone is not approval. |
| Security review is required before execution or adoption. | External harnesses, engines, SDKs, scripts, and package managers are risky. |
| External repositories do not define platform architecture. | They can inform proposals and decisions only through citations and governance. |
| External graph-oriented sources do not decide substrate. | Cognitive Semantic System substrate requires explicit substrate decision. |

## 13. Product Workspace Governance

Product workspace governance is scoped. It does not define root workspace authority unless a future root governance decision explicitly delegates a bounded authority.

| Product governance topic | Governance requirement |
| --- | --- |
| Product activation | Active product name, purpose, owner, scope, Git posture, validation baseline, and root-boundary statement. |
| Product ownership | Product Owner, root interaction owner, validation owner, external dependency owner, and lifecycle owner. |
| Product Git posture | Decide whether product remains local-only, becomes tracked in current repo, splits to separate repo, or remains deferred. |
| Product documentation status | Product docs can be `product_scoped` and canonical only inside declared product scope. |
| Product validation | Product acceptance criteria, test/evidence posture, domain validation, and residual risks. |
| Product external dependencies | Product-specific provenance, license, security, validation, and governance review. |
| Product archive / retirement | Retire or archive product candidates with reason, owner, evidence, and restoration/reopen rule. |

Product governance rules:

| Rule | Meaning |
| --- | --- |
| Product governance is contained. | Product decisions govern product scope only. |
| Product docs do not override root architecture. | Root W-series and future root decisions remain higher authority for workspace boundaries. |
| Product activation is governed. | Existing folders under `2_products/` are candidates, not active governed products by default. |
| Product local-only posture remains. | `2_products/` stays ignored/local-only until governance changes posture. |

## 14. Validation Governance

Validation governance defines how validation evidence is used in decisions.

| Validation interaction | Governance meaning |
| --- | --- |
| Validation evaluates. | It reports whether evidence, artifact, behavior, or claim satisfies scoped checks. |
| Governance decides. | It accepts, rejects, defers, promotes, or requests more evidence. |
| Validation can support promotion. | Passing scoped validation can be cited as evidence. |
| Validation can block promotion. | Failed, stale, incomplete, or missing validation can block or qualify a decision. |
| Passing validation does not approve. | Approval still requires governance. |
| Failed validation requires blocker handling. | Fix within scope, defer, reject, or record exception; do not hide failure. |
| Validation evidence must be retained when used for promotion. | Commands, outputs, review notes, scope, and limitations should be traceable. |

Validation governance rule:

```text
Validation supplies a validity posture. Governance decides what to do with that
posture.
```

## 15. Security / Access Governance

Security and access governance can block exposure or action even when governance otherwise wants to proceed.

| Security/access area | Governance requirement |
| --- | --- |
| Secrets | Never expose, summarize, commit, or embed; stop and use secure handling. |
| Credentials | Authentication and credential use require explicit approval and secure handling. |
| Sensitive files | Identify sensitivity, minimize exposure, restrict context, and avoid publication. |
| Local-only material | Respect `.gitignore`, W-04, W-07, W-08, and W-10; do not stage or publish by default. |
| External code execution | Requires explicit security/environment review and governance approval. |
| Provider authentication | Requires explicit approval, provider scope, credential handling, and data-retention awareness. |
| Network calls | Require explicit scope, reason, and risk review. |
| Product data | Product scope, sensitivity, privacy, and retention must be governed. |
| Datasets | Provenance, license, sensitivity, size, and retention required. |
| Models | Provenance, license, safety, use scope, and storage posture required. |
| Generated artifacts | Review for secrets, private data, license content, stale claims, and authority confusion. |
| Publication | Requires review for sensitive content, license, product claims, external reuse, and authority posture. |

Security/access rules:

| Rule | Meaning |
| --- | --- |
| Security can block exposure or action. | A promotion with unresolved security risk must be rejected, deferred, scoped, or excepted explicitly. |
| Governance cannot override security casually. | Exceptions need owner, reason, scope, mitigation, and review point. |
| Approval must preserve sensitive boundaries. | Do not convert sensitive evidence into public or committed material by approval alone. |

## 16. Git Governance

Git is a record mechanism and collaboration tool. It is not semantic authority by itself.

| Git action | Governance posture |
| --- | --- |
| Staging | Governed action requiring explicit instruction and intended file list. |
| Commits | Governed action requiring status/diff review and human approval. |
| Pushes | Governed publication action requiring explicit approval and remote/diff awareness. |
| Amends/rebases/resets | High-risk history actions requiring explicit approval. |
| `git add .` | Prohibited unless explicitly approved; prefer exact paths. |
| Local-only material | Must not be staged by default. |
| Git status reporting | Required before proposed commit/push and after scoped W-series work. |

Git governance clarifications:

| Clarification | Rule |
| --- | --- |
| Git history records decisions but does not create semantic truth. | A committed doc still needs status, scope, evidence, and governance posture. |
| A commit can contain unapproved material if staging is careless. | Review status and intended files before staging. |
| A commit can lag governance. | Governance records should be cited; commit hash alone is not approval. |
| Ignored does not mean irrelevant. | Local-only evidence can matter, but publication/tracking requires governance. |

## 17. Agent Governance

Agent governance uses W-10. Agents are bounded operators, not approval authorities.

| Agent capability | Governance boundary |
| --- | --- |
| Agents may propose. | Proposals require evidence, scope, citations, and human/governance review. |
| Agents may classify. | Classifications are evidence unless accepted by governance or canonical docs. |
| Agents may validate when scoped. | Validation output is evidence, not approval. |
| Agents may draft. | Drafts are not canonical until promoted. |
| Agents may not approve. | Approval requires human or delegated governance role. |
| Agents may not promote. | Agents can recommend promotion; governance promotes. |
| Agents may not decide substrate. | Cognitive substrate decision requires explicit decision record and evaluation. |
| Agents may not continue tickets automatically. | W-series continuation requires explicit instruction. |
| Subagents return evidence only. | Parent/human/governance merges and decides. |
| Agents may not stage/commit/push unless explicitly instructed. | Git history remains human-governed. |

Agent governance rule:

```text
Agent work can feed governance. It does not replace governance.
```

## 18. Governance Artifacts

Future governance artifacts should make decisions auditable. W-11 defines artifact types only and does not create schemas.

| Artifact | Purpose |
| --- | --- |
| Decision Record | Captures accepted decision, scope, rationale, evidence, impacts, and owner. |
| Approval Record | Captures who approved what, within which scope, and under which conditions. |
| Promotion Record | Captures transition from evidence/candidate/proposal to accepted scoped authority/use. |
| Rejection Record | Captures rejected candidate, reason, evidence retained, and reconsideration conditions. |
| Deferral Record | Captures missing evidence, validation, owner, scope, or policy required to resume. |
| Exception Record | Captures bounded departure from rules, risk, mitigation, owner, and review point. |
| Supersession Record | Captures replacement relationship between old and new authority. |
| Deprecation Record | Captures discouraged material, reason, risk, and recommended replacement. |
| Archive Record | Captures archive reason, source path, owner, date, lifecycle, and restoration rule. |
| Validation Reference | Links validation evidence to a decision or promotion without making it approval. |
| Security Review Reference | Links security/access review to decision, exception, or promotion. |
| Migration Record | Captures migration source, target, classification, restatement, validation, and audit result. |

Artifact rule:

```text
Governance artifacts should preserve why a decision was made, not only what changed.
```

## 19. Governance Lifecycle

Governance lifecycle is not Git status. It describes decision and authority maturity.

| Lifecycle state | Meaning |
| --- | --- |
| `proposed` | Candidate exists but is not under formal review or accepted. |
| `under_review` | Evidence, validation, security, ownership, and scope are being evaluated. |
| `approved` | Governance accepts the decision or action within declared scope. |
| `rejected` | Governance declines the candidate for requested scope/use. |
| `deferred` | Governance postpones decision pending missing preconditions. |
| `promoted` | Candidate has moved into accepted scoped authority/use. |
| `current` | Accepted material is the active authority/use within scope. |
| `superseded` | Replaced by newer accepted authority. |
| `deprecated` | Discouraged for new use due to risk, age, replacement, or changed direction. |
| `archived` | Retired and retained for audit/reference. |
| `reopened` | Previously resolved item is reopened with explicit reason. |

Lifecycle rules:

| Rule | Meaning |
| --- | --- |
| Lifecycle is not Git status. | A tracked file may be draft; an untracked local artifact may be important evidence. |
| Lifecycle preserves provenance. | Every transition should keep source, owner, reason, date, and prior state. |
| Reopened decisions require explicit reason. | Reopening without rationale creates governance drift. |
| Current is scoped. | Current for product scope is not current for workspace root. |
| Archived is retained. | Archive is not deletion. |

## 20. Governance Invariants

| ID | Invariant |
| --- | --- |
| GOV-001 | Evidence is not approval. |
| GOV-002 | Validation is not governance. |
| GOV-003 | Agent output is not governance. |
| GOV-004 | Context inclusion is not promotion. |
| GOV-005 | Git commit is not semantic truth. |
| GOV-006 | External source presence is not adoption. |
| GOV-007 | Product scope does not define root authority. |
| GOV-008 | Archive is not deletion. |
| GOV-009 | Promotion requires declared scope. |
| GOV-010 | Cognitive substrate remains undecided until decision. |
| GOV-011 | Documentation status requires governance when authority changes. |
| GOV-012 | Security/access can block exposure or action. |
| GOV-013 | Rejection and demotion preserve history. |
| GOV-014 | Ownership is required for durable authority. |
| GOV-015 | No next-ticket execution without explicit instruction. |

Invariant rule:

```text
If a candidate violates a governance invariant, governance must reject, defer,
scope, or require corrective evidence before promotion.
```

## 21. Governance Anti-patterns

| Anti-pattern | Failure mode | Required correction |
| --- | --- | --- |
| Approve by commit | Treats Git history as authority. | Require explicit governance record or status/scope authority. |
| Approve by confidence | Treats model certainty or human intuition as proof. | Require evidence and rationale. |
| Approve by tests only | Treats validation as governance. | Use validation as evidence for governance. |
| Approve by external README | Treats external claims as internal truth. | Use W-03 review and promotion controls. |
| Approve by folder location | Treats paths as authority. | Use status, scope, and governance. |
| Approve by previous canonical label | Imports old scope. | Use W-02 and restatement. |
| Approve by generated summary | Treats projection as source. | Cite inputs, validate, and govern. |
| Promote without owner | Creates orphaned authority. | Assign owner before promotion. |
| Promote without citation | Breaks auditability. | Cite evidence and uncertainty. |
| Archive unresolved conflict | Hides decision debt. | Resolve, defer with reason, or preserve conflict visibly. |
| Product-root collapse | Lets product decisions define root workspace. | Keep product governance scoped. |
| Substrate decision by naming | Lets labels or folders decide architecture. | Use explicit Cognitive Semantic System substrate decision. |
| Governance by agent output | Lets agent reports approve themselves. | Agents propose; governance approves. |
| Security exception without mitigation | Exposes sensitive material or risky execution. | Record owner, scope, mitigation, and review point. |

Anti-pattern rule:

```text
Governance drift occurs when acceptance is inferred from convenience, confidence,
location, tests, commits, generation, or proximity instead of an explicit decision.
```

## 22. Readiness For W-12

Expected next ticket: `W-12 - Product Workspace Policy`.

W-12 can define product workspace activation and product governance after W-11 because W-11 defines the root governance and promotion model that product policy must follow.

Readiness assessment:

| Area | Verdict | Reason |
| --- | --- | --- |
| Root governance definition | Ready enough. | W-11 defines approval, rejection, deferral, exception, promotion, demotion, supersession, deprecation, archive authorization, ownership, and lifecycle. |
| Promotion model | Ready enough. | W-11 defines preconditions, targets, and evidence-to-decision flow. |
| Product boundary | Ready for product policy. | W-11 keeps product governance scoped and blocks product-root collapse. |
| Product activation | Ready for policy definition only. | Active product list, owner, Git posture, validation, and retirement rules remain unresolved. |
| Product Git posture | Not decided. | W-12 should decide whether and how `2_products/` remains local-only, becomes tracked, or splits. |
| Product documentation | Ready for policy definition. | W-09/W-11 define product-scoped docs and governance requirements. |
| Product validation | Needs W-12 detail. | Product-specific validation and acceptance criteria remain undefined. |
| Product external dependencies | Needs W-12 detail. | External dependency policy must follow W-03/W-11 but be product-specific. |
| Implementation | Not ready. | Product policy should precede product implementation migration or activation. |

W-12 should consume:

| Input | Why |
| --- | --- |
| W-01 workspace charter | Product/root boundary and authority precedence. |
| W-03 external source registry | External/domain dependencies and risks. |
| W-04 responsibility map | Product access/Git/local-only posture. |
| W-07 topology | Product folder topology and local-only status. |
| W-08 migration plan | Product migration blockers and policy prerequisites. |
| W-09 documentation structure | Product-scoped documentation rules. |
| W-10 agent operating rules | Product read/edit/stop boundaries. |
| W-11 governance model | Product activation, ownership, promotion, validation, and lifecycle governance. |

Readiness verdict:

```text
W-11 makes AGENT PLATFORM ready for W-12 product workspace policy after explicit
instruction. It does not create W-12, activate products, move product files, change
Git posture, or authorize product implementation.
```

## 23. Final Verdict

| Question | Answer |
| --- | --- |
| What is governance in AGENT PLATFORM? | The explicit scoped decision layer for approval, rejection, deferral, exceptions, promotion, demotion, supersession, deprecation, archive authorization, ownership, and lifecycle decisions. |
| What is promotion? | A controlled transition from evidence, proposal, candidate, generated output, external reference, previous knowledge, or agent output into accepted scoped authority or accepted scoped use. |
| What can agents propose but never approve? | Architecture changes, documentation status changes, migration actions, external reuse, dependency adoption, product activation, validation sufficiency, security exceptions, Git history changes, authority promotion, and substrate decisions. |
| What can be promoted first? | Low-risk current-scope restatements of carry-forward principles, curated external metadata, reviewed validation references, and documentation/projection updates that satisfy ownership, citations, validation posture, governance posture, and security posture. |
| What remains blocked? | Bulk migration, product activation, product Git posture changes, external dependency adoption, external code execution, archive creation, implementation, governance automation, and final Cognitive Semantic System substrate decision. |
| What should W-12 consume? | W-01 through W-11, especially product boundaries, external-source risks, local-only posture, migration controls, documentation status/scope, agent operating limits, and this governance/promotion model. |

Final W-11 statement:

```text
AGENT PLATFORM governance turns evidence and proposals into accepted scoped
authority only through explicit decisions. Agents, validation, context, generated
outputs, external sources, documentation status, and Git commits can support
governance, but none replaces it. W-11 stops at the governance and promotion model
and does not start W-12.
```
