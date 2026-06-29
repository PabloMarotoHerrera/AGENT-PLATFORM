# AGENT PLATFORM Migration Validation Model

Status: Canonical V-03 migration validation model  
Date: 2026-06-29  
Scope: Migration validation architecture for AGENT PLATFORM.  
Authority: Architecture only. This document validates migration readiness and evidence; it does not execute migration, approve migration, promote material, create archives, alter Git history, implement tooling, or authorize next tickets.

## 1. Purpose

V-03 specializes migration validation after V-00 registry architecture, V-01 proof levels, and V-02 validation evidence. It defines how AGENT PLATFORM validates migration plans, batches, previous knowledge restatements, source/target mapping, restatement fidelity, citation coverage, local-only posture, security/access posture, Git posture, evidence retention, blockers, and migration audits.

V-03 validates migration readiness and migration evidence. It does not execute migration, approve migration, promote migrated material, move/copy/rename/delete/archive files, create `_archive/`, or authorize staging, commit, push, publication, implementation, product activation, external adoption, provider calls, network/API/MCP, tests, package managers, authentication, or any next ticket.

## 2. Migration Validation Definition

Migration validation is evaluation of whether a migration candidate, plan, restatement, batch, or audit satisfies declared criteria before any movement, promotion, archive, Git action, or governance decision.

| Boundary | Rule |
| --- | --- |
| Migration validation evaluates. | It checks criteria, evidence, proof level, blockers, and residual risk. |
| Governance decides. | Approval, rejection, deferral, exception, promotion, archive, and lifecycle are governance decisions. |
| Security constrains. | S-series local-only, secret, credential, execution, and access policy can block migration. |
| Evidence supports. | V-02 evidence supports readiness but does not approve. |
| Proof is scoped. | V-01 proof levels apply only to declared target, criterion, evidence, freshness, and limitations. |
| Git records. | Git state can be evidence; Git is not approval or semantic truth. |
| Migration validation does not execute migration. | No movement, copy, rename, archive, deletion, staging, commit, or push occurs in V-03. |

## 3. Migration Validation Object Model

Conceptual fields for a migration validation target:

```text
source candidate + source path + source classification + target path + target status
+ migration intent + restatement claim + citation set + validation criteria
+ proof level + evidence record + local-only posture + security/access posture
+ Git posture + governance posture + blocker + residual risk + verdict + stop rule
```

Invalidity rule: promotion-supporting migration validation is invalid if source classification, source path/reference, target path, target status, scope, sensitivity, citations, limitations, or stop rule are missing.

## 4. Migration Target Classes

| Target class | Can validate | Cannot infer | Default proof | Common blockers |
| --- | --- | --- | --- | --- |
| migration plan | Criteria, scope, target classes, blockers. | Execution readiness by itself. | PL-3/PL-4. | Missing scope/governance. |
| previous knowledge restatement | Source claim, current wording, citations. | Current authority without governance. | PL-3/PL-4. | Missing source or fidelity failure. |
| carry_forward extraction | Useful concept restated in current vocabulary. | Direct copy as authority. | PL-3/PL-4. | No restatement or citation. |
| conflicted material normalization | Naming/scope/substrate correction. | Final Cognitive Semantic System substrate. | PL-4/PL-7. | Legacy naming or substrate assumption. |
| scope-limited product material review | Product-only relevance and root boundary. | Root architecture authority. | PL-2/PL-4. | Product-root collapse. |
| migration_evidence retention | Historical/rationale trace. | Current governing rule. | PL-2/PL-3. | Old label treated as current. |
| external_reference restatement | External claim restated as evidence. | Adoption, execution, reuse. | PL-3/PL-4. | External posture missing. |
| external metadata migration candidate | Metadata/review readiness. | Raw source migration or dependency approval. | PL-2/PL-4. | License/security unknown. |
| product documentation migration candidate | Product doc target/status readiness. | Product activation. | PL-3/PL-4. | Missing product owner/scope. |
| archive candidate | Reason, lifecycle, replacement, trace. | Archive execution. | PL-3/PL-4. | No archive policy. |
| first controlled migration batch | Batch criteria, bounded sources/targets, audit readiness. | Permission to move files. | PL-4/PL-7. | Local-only/Git/governance blockers. |
| migration audit | Evidence, verdicts, blockers, residual risks. | Migration approval. | PL-7. | Missing evidence or reviewer. |

## 5. Source Classification Validation

| W-02/W-08 state | Required criteria | Allowed outcome | Prohibited outcome | Evidence | Blocker |
| --- | --- | --- | --- | --- | --- |
| `carry_forward` | Source path, concept, current restatement, citations. | Restated current proposal. | Direct copy as authority. | Classification + citation + fidelity note. | Missing restatement. |
| `scope_limit` | Product/domain scope and root boundary. | Product-scoped candidate. | Root authority. | Classification + product-scope evidence. | Product scope unknown. |
| `migration_evidence` | Historical value and trace need. | Retain/cite as evidence. | Current governing rule. | Source path + rationale. | Old label used as current. |
| `conflicted` | Conflict type, normalized vocabulary, substrate neutrality. | Normalized proposal/evidence. | Promotion before normalization. | Conflict note + coherence review. | Naming/substrate leakage. |
| `external_reference` | External posture, provenance, license/security uncertainty. | Evidence or reviewed metadata. | Dependency/adoption/execution. | External review/source-status evidence. | External review missing. |
| `superseded` | Replacement and historical trace. | Historical citation or archive candidate. | Current authority. | Supersession reference. | Replacement unknown. |
| unknown/unclassified | Classify first. | Defer. | Migration. | Gap/blocker evidence. | Classification absent. |

## 6. Migration Criteria Catalog

Canonical criteria: source exists or source reference exists; source classification/status/scope/sensitivity known; target path/status/scope declared; restatement required where applicable; restatement fidelity checked; current vocabulary used; prohibited naming absent; Cognitive Semantic System substrate not decided by migration; citations complete; local-only posture preserved; secrets/credentials excluded; product scope preserved; external source posture preserved; generated output not treated as source; Git posture checked; no wholesale migration; no source mutation; validation evidence retained safely; governance preconditions listed; stop rule obeyed.

## 7. Restatement Fidelity Model

Restatement validation checks: source claim identified; current claim restated; old vocabulary normalized; current vocabulary used; obsolete naming removed; product/domain scope preserved; external/source status preserved; uncertainty retained; citations preserved; no hidden promotion; no substrate assumption; no wholesale copy.

Fidelity rule: a restatement carries forward a scoped concept, not old authority, old status, old wording, file location, product assumptions, external instructions, or substrate choices.

## 8. Citation Coverage Model

Required citations: previous knowledge source path/reference; W-02 classification; W-08 migration rule; W-09 documentation status/scope; W-11 governance boundary; S-series security/access posture; V-00/V-01/V-02 validation evidence and proof posture.

Citation evidence is provenance, not truth. Missing, stale, indirect, or source-status-blind citations block promotion-quality migration validation.

## 9. Local-only / Security Validation

Migration validation must confirm: `previusknowledge/` remains local-only; `2_products/` remains local-only; `4_external/sources/` remains local-only; datasets/models/artifacts remain local-only; secrets and credentials are excluded; local-only evidence is not published by default; safe metadata is preferred; unknown sensitivity escalates.

Security rule: secret/credential values are never migration evidence content and must never be copied, summarized, transformed, tested, retained, staged, committed, or published.

## 10. Git Validation For Migration

`git status`, `git diff`, and `git check-ignore` can be migration evidence for worktree, changed-file, and local-only posture. Git commit is not validation, staging is not validation, push is publication, and exact staging remains human-gated.

Local-only staged material is a blocker. Secret/credential staged material is a blocker. Migration validation must not stage or commit.

## 11. Migration Proof Level Model

| Proof level | Migration use |
| --- | --- |
| PL-1 | Metadata/path/ignore/Git presence checks. |
| PL-2 | Source status, classification, sensitivity, scope checks. |
| PL-3 | Citation review for source, classification, target, and authority claims. |
| PL-4 | Restatement fidelity, coherence, policy, matrix, contradiction review. |
| PL-5 | Scoped commands such as `Test-Path`, `git status`, `git check-ignore`, bounded naming checks. |
| PL-7 | Structured migration audit. |
| PL-8 | Reproduced migration validation/audit. |

Migration execution support requires V-03 criteria plus governance, security/access, and exact future ticket scope. V-03 itself still does not execute migration.

## 12. Migration Evidence Model

Evidence types: source classification evidence; source path evidence; target path evidence; citation evidence; restatement fidelity evidence; local-only posture evidence; security/access posture evidence; Git status/diff/check-ignore evidence; blocker evidence; audit evidence; governance reference evidence.

Retention rules: references over copied content; safe metadata over local-only content; no secret/credential values; audit trace retained safely; failed/blocked/skipped/stale evidence remains visible when safe; raw product/external/local-only/generated material is not copied by default.

## 13. Migration Verdict Model

| Verdict | Meaning |
| --- | --- |
| `migration_ready_for_governance_review` | Criteria satisfied enough for governance review. |
| `migration_ready_with_cautions` | Ready only with explicit residual risks. |
| `migration_blocked_by_source_classification` | Source class missing, unknown, or incompatible. |
| `migration_blocked_by_missing_citation` | Provenance is incomplete. |
| `migration_blocked_by_local_only_risk` | Local-only exposure/Git/publication risk unresolved. |
| `migration_blocked_by_secret_or_credential_risk` | Secret/credential risk requires stop. |
| `migration_blocked_by_product_scope` | Product material risks root promotion. |
| `migration_blocked_by_external_source_posture` | External evidence risks adoption/execution/reuse confusion. |
| `migration_blocked_by_substrate_assumption` | Migration implies final substrate. |
| `migration_blocked_by_missing_target_status` | Target status/scope/lifecycle absent. |
| `migration_blocked_by_missing_governance` | Owner/approval path absent. |
| `migration_blocked_by_git_posture` | Git/local-only/staging posture unsafe. |
| `migration_inconclusive` | Evidence insufficient or conflicting. |
| `migration_deferred` | Safe to postpone pending later ticket/decision. |

Verdict is not approval.

## 14. Migration Blocker Register

| Blocker group | Examples | Stop behavior | Required action | Blocks execution/promotion? |
| --- | --- | --- | --- | --- |
| source | unknown classification, missing source path, stale evidence | Stop validation use. | Classify, locate, or defer. | Yes/yes. |
| target | missing target path/status/scope | Stop target claim. | Declare target metadata. | Yes/yes. |
| citation | missing citations, weak provenance | Stop promotion-quality use. | Add source/status citations. | Yes/yes. |
| fidelity | restatement failure, old naming leakage, prior label treated current | Stop restatement. | Normalize and re-review. | Yes/yes. |
| local/security | local-only leak, secret/credential risk, generated output as source | Stop exposure. | Safe metadata, redact, escalate. | Yes/yes. |
| product/external | product-root collapse, external adoption leakage | Stop scope expansion. | Product/external review and governance. | Yes/yes. |
| Git | local-only staged, secret staged, unsafe diff | Stop Git path. | Human/security review. | Yes/yes. |
| governance/proof | governance missing, proof insufficient | Stop decision framing. | Add owner/evidence/proof or defer. | Yes/yes. |
| substrate | graph/projection treated as final substrate | Stop substrate claim. | Restore substrate neutrality. | Yes/yes. |

## 15. Migration Audit Model

Audit fields: `migration_id`, source class, source path/reference, target path, target status, source claim, restated claim, citations, proof level, evidence retained, validation verdict, blockers, residual risks, security/access posture, Git posture, governance posture, reviewer/date, revalidation trigger, stop rule.

Migration audit is evidence, not approval. Audit may support governance review, block migration, or preserve historical trace.

## 16. Matrices

### Matrix A. Source Classification Vs Allowed Migration Outcome

| State | restate | retain | defer | normalize | product only | external only | blocked |
| --- | --- | --- | --- | --- | --- | --- | --- |
| carry_forward | Yes | Yes | Optional | If needed | No | No | If uncited |
| scope_limit | No root | Yes | Yes | If needed | Yes | No | If root-promoted |
| migration_evidence | No authority | Yes | Optional | No | No | No | If treated current |
| conflicted | After normalization | Yes | Yes | Yes | Maybe | Maybe | Until normalized |
| external_reference | Restate as evidence | Yes | Yes | If naming risk | Maybe | Yes | If adopted/executed |
| superseded/unknown | No | Historical/gap | Yes | If classified | No | No | Until classified/replaced |

### Matrix B. Migration Target Vs Minimum Proof Level

| Target | proposal | governance review | execution support | blockers |
| --- | --- | --- | --- | --- |
| migration plan | PL-3 | PL-4 | PL-7 + governance later | scope/governance missing |
| restatement | PL-3 | PL-4 | PL-7 later | citation/fidelity failure |
| conflicted normalization | PL-4 | PL-7 | PL-7/PL-8 later | naming/substrate leakage |
| product-scoped material | PL-3 | PL-4 | V-04 later | product-root collapse |
| external metadata | PL-3 | PL-4 | V-05 later | adoption/execution risk |
| first migration batch | PL-4 | PL-7 | PL-7 + explicit ticket | local-only/Git/security |
| migration audit | PL-7 | PL-7 | Audit only | missing evidence/reviewer |

### Matrix C. Migration Blocker Vs Required Action

| Group | stop | fix | defer | govern | reject |
| --- | --- | --- | --- | --- | --- |
| source | Yes | classify/locate | Yes | If promoted | If invalid |
| citation | Yes | add citations | Yes | If exception | If unsupported |
| local-only/security | Yes | redact/safe metadata | Yes | Security required | If unsafe |
| product | Yes | scope product | Yes | Product governance | If root collapse |
| external | Yes | external review | Yes | External governance | If adoption leak |
| Git | Yes | review status/diff | Yes | Human Git decision | If secret staged |
| governance | Yes | owner/decision path | Yes | Required | If no owner |
| substrate | Yes | neutralize wording | Yes | Substrate decision later | If assumption persists |

## 17. Migration Incidents

Incidents: local-only content copied into current doc; secret/credential copied into migration output; product material promoted to root; external source copied or treated as dependency; prior canonical label treated as current authority; graph/projection treated as substrate decision; generated output treated as source; staged local-only migration material; migration executed without ticket; archive created without policy.

Response: STOP, report safe metadata, do not continue adjacent work, do not expose values, do not stage/commit/push, do not move/copy/rename/delete/archive, and require human/governance/security decision.

## 18. Migration Invariants

| ID | Invariant |
| --- | --- |
| MIGVAL-001 | Migration validation evaluates; governance decides. |
| MIGVAL-002 | Migration validation does not execute migration. |
| MIGVAL-003 | Migration audit is not migration approval. |
| MIGVAL-004 | Previous canonical labels are historical. |
| MIGVAL-005 | Carry-forward requires restatement. |
| MIGVAL-006 | Conflicted material requires normalization. |
| MIGVAL-007 | Scope-limited material stays scoped. |
| MIGVAL-008 | External references remain external. |
| MIGVAL-009 | Product material remains product-scoped. |
| MIGVAL-010 | Local-only means no default publication. |
| MIGVAL-011 | Secrets and credentials are never migrated. |
| MIGVAL-012 | Git commit is not promotion. |
| MIGVAL-013 | Generated output is not source by default. |
| MIGVAL-014 | Cognitive substrate remains undecided. |
| MIGVAL-015 | No wholesale migration. |

## 19. Anti-patterns

Anti-patterns: migration by copying, folder move, old canonical label, summary without citation, product-root collapse, external source proximity, graph projection, generated output, Git commit, audit as approval, hidden local-only content, ignoring blockers, broad context dump, `git add .`, archive as cleanup, restatement without source path, and proof level inflation.

## 20. Remaining Gaps

V-03 does not solve: no migration execution, no first migration batch, no archive policy execution, no product migration execution, no external metadata migration execution, no registry implementation, no schemas, no CI, no tests, no enforcement, no product validation specialization, no external source validation specialization, no validation audit, and no Cognitive Semantic System implementation.

## 21. Readiness For V-04

V-04 - Product Validation Model is ready after explicit instruction. V-04 should specialize product charters, product scope, product activation, product validation baselines, product tests, product generated outputs, product dependency posture, and product-root boundaries.

Do not create V-04 from V-03.

## 22. Final Verdict

| Question | Answer |
| --- | --- |
| What is migration validation? | Scoped evaluation of migration candidates, plans, restatements, batches, and audits before movement, promotion, archive, Git action, or governance decision. |
| What migration targets can now be validated? | Plans, restatements, carry-forward extractions, conflicted normalization, product/external candidates, archive candidates, first-batch readiness, and audits. |
| What proof levels apply? | PL-1, PL-2, PL-3, PL-4, PL-5, PL-7, and PL-8 where reproduced; PL-6 is generally not migration-specific here. |
| What evidence is required? | Source classification/path, target path/status, citations, fidelity review, local-only/security/Git posture, blocker evidence, audit evidence, and governance references. |
| What blocks migration? | Unknown classification, missing source/target/citations/scope/status, fidelity failure, old naming leakage, product/external leakage, substrate assumption, local-only/secret/Git risk, missing governance, stale evidence, or insufficient proof. |
| Does V-03 authorize migration execution? | No. V-03 validates readiness only. |
| Is V-04 ready after explicit instruction? | Yes. |

Stop rule: after completing V-03, STOP. Do not start V-04, stage, commit, push, execute migration, move/copy/rename/delete/archive files, inspect local-only folders deeply, or start any next ticket.
