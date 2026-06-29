# AGENT PLATFORM Validation Evidence Model

Status: Canonical V-02R validation evidence model  
Date: 2026-06-29  
Scope: Validation evidence architecture for AGENT PLATFORM. This document specializes evidence handling after V-00 and V-01.  
Authority: Architecture only. This document does not implement a registry, evidence storage, schemas, code, tests, CI, hooks, scanners, tools, packages, SDKs, enforcement, migration, product activation, external adoption, provider calls, execution, staging, commit, or push.

## 1. Purpose

V-02R defines the compact canonical Validation Evidence Model for AGENT PLATFORM.

V-00 defines validation registry architecture: targets, claims, methods, status, verdicts, blockers, freshness, retention, and governance/security relationships. V-01 defines proof levels PL-0 through PL-8 and how evidence strength supports scoped validation. V-02R defines what validation evidence is, how it is referenced, retained, limited, classified, and used.

V-02R is not registry implementation, an evidence database, a schema, CI, a test suite, evidence automation, governance approval, migration authorization, implementation authorization, product activation, external adoption, provider/API/network/MCP authorization, execution approval, staging approval, commit approval, or push approval.

## 2. Validation Evidence Definition

Validation evidence is material that can support, challenge, qualify, block, or contextualize a validation claim, proof level, verdict, blocker, limitation, residual risk, or governance review.

Evidence rules:

| Rule | Meaning |
| --- | --- |
| Evidence is not truth. | Evidence supports interpretation; it does not make a claim true by itself. |
| Evidence is not proof by itself. | Proof level requires scope, criterion, method, evidence, freshness, and limitations. |
| Evidence is not governance. | Governance decides acceptance, rejection, promotion, exception, and lifecycle. |
| Evidence is not approval. | Passing or strong evidence does not approve action. |
| Evidence is not permission. | Evidence does not grant read, write, execute, migrate, publish, stage, commit, push, or promote rights. |
| Evidence requires source status. | Canonical, evidence, generated, product-scoped, external, local-only, historical, or unknown status must be known. |
| Evidence requires sensitivity posture. | Public, internal, local-only, sensitive, restricted, secret, credential, external-restricted, product-restricted, generated-sensitive, or unknown must be handled. |
| Evidence requires scope. | Evidence applies only to declared target, claim, method, and timeframe. |
| Evidence requires limitations. | Missing limitations invalidate promotion-supporting use. |

Evidence can become stale, be superseded, be invalidated, remain local-only, or become generated-sensitive.

## 3. Evidence Object Model

An evidence item is the minimum conceptual unit used by validation. It is not a storage schema.

Required fields:

```text
evidence item
+ target
+ claim/question
+ source
+ source status
+ evidence type
+ method
+ proof relationship
+ validation status/verdict relationship
+ sensitivity
+ retention posture
+ reference/location
+ freshness
+ limitations
+ reviewer/date
+ revalidation trigger
+ governance/security relationship
+ stop rule
```

Invalidity rule: an evidence item is invalid for promotion-supporting use if source, scope, sensitivity, or limitations are missing. It may still be retained as a gap, blocker, or historical trace when safe.

Location/reference policy: evidence may be referenced by inline validation summary, source path, source section, Git status/diff reference, command record, local artifact path, local-only artifact path, external review path, product-scoped review path, migration audit path, decision/governance reference, incident reference, or future Cognitive Semantic System record reference. This chooses no database, graph, JSON, YAML, schema, storage folder, registry file, or implementation.

## 4. Evidence Type Catalog

| Evidence type | Definition | Sensitivity risk | Retention posture | Proof support | Key limitation |
| --- | --- | --- | --- | --- | --- |
| path existence evidence | Confirms a path exists or is missing. | Low to medium. | safe metadata. | PL-1, PL-5. | Existence is not correctness. |
| file metadata evidence | Size, modified date, path, basic file metadata. | Low to medium. | safe metadata. | PL-1, PL-5. | Metadata is not semantic review. |
| Git status/diff/ignore evidence | Worktree, diff, staged, untracked, ignored posture. | Medium. | summary or command record. | PL-1, PL-5. | Git state is not correctness or approval. |
| citation evidence | Source path and claim linkage. | Low to medium. | reference or review note. | PL-3, PL-4. | Provenance, not truth. |
| source-status evidence | Source class, authority, freshness, and sensitivity classification. | Medium. | summary or review note. | PL-2, PL-3, PL-4. | Classification can be stale or incomplete. |
| content review evidence | Scoped manual/agent review of file content. | Medium to high. | review note or redacted summary. | PL-3, PL-4, PL-7. | Review can miss issues. |
| policy coherence evidence | Cross-policy consistency review. | Medium. | review note. | PL-4, PL-7. | Coherence is not enforcement. |
| matrix alignment evidence | Matrix comparison across policies. | Medium. | review note. | PL-4, PL-7. | Depends on selected matrices. |
| contradiction register evidence | Recorded conflicts, tensions, blockers. | Medium. | review note or historical trace. | PL-4, PL-7. | Register does not resolve conflicts. |
| naming check evidence | Bounded terminology/prohibited naming check. | Low to medium. | command record or summary. | PL-1, PL-5. | Only covers searched paths/patterns. |
| security/access review evidence | Review against S-series access, sensitivity, execution, local-only rules. | High. | redacted summary or restricted note. | PL-4, PL-7. | Does not implement enforcement. |
| local-only posture evidence | Evidence that material is ignored/local-only or excluded. | Medium to high. | safe metadata or local-only reference. | PL-1, PL-2, PL-5. | Local-only can still leak if copied. |
| secret/credential posture evidence | Safe metadata that secret/credential handling is blocked or classified. | High. | safe metadata only or do_not_retain. | PL-2, PL-4, PL-7. | Values must never be retained. |
| command output evidence | Output from exact scoped command. | Medium to high. | command record, summary, excerpt if safe. | PL-5. | Command proves only its criterion. |
| validation command evidence | Low-risk listed validation command result. | Medium. | command record. | PL-1, PL-5. | Still scoped execution. |
| test/build/runtime output evidence | Test, build, or runtime results when explicitly approved. | High. | summary, excerpt, or local-only. | PL-5, PL-6, PL-7. | Not allowed by V-02R; later scope only. |
| generated artifact evidence | Reports, exports, generated docs/artifacts. | High. | generated artifact or safe metadata. | PL-1, PL-2, PL-4, PL-5. | Generated is not source by default. |
| log evidence | Logs, traces, runtime records. | High. | local-only or redacted summary. | PL-5, PL-6, PL-7. | Logs may contain secrets/credentials. |
| manual review note | Structured reviewer findings and limits. | Medium. | review note. | PL-3, PL-4, PL-7. | Not proof by itself. |
| audit report evidence | Structured scoped audit. | Medium to high. | review note or historical trace. | PL-7, PL-8 if reproduced. | Audit quality depends on scope. |
| reproduction evidence | Independent rerun/review result. | Medium to high. | command/audit record. | PL-8. | May share assumptions. |
| external source metadata/review evidence | Provenance, license posture, runtime/dependency/instruction risk. | High. | external reference or review note. | PL-2, PL-3, PL-4, PL-7. | Does not approve adoption/execution. |
| product review evidence | Product inventory, scope, owner, baseline, blockers. | High. | product-scoped reference. | PL-2, PL-3, PL-4, PL-7. | Product-scoped only. |
| migration classification/audit evidence | W-02/W-08 classification, source/target, fidelity, blockers. | Medium to high. | migration audit/reference. | PL-3, PL-4, PL-7. | Does not execute migration. |
| dataset/model metadata evidence | Provenance, license, sensitivity, intended use, storage posture. | High. | safe metadata or local-only. | PL-2, PL-4, PL-7. | Does not authorize use/training/execution. |
| context pack evidence | Included/excluded sources, status, sensitivity, freshness, stop rules. | Medium. | summary or reference. | PL-2, PL-3, PL-4. | Context inclusion is not validation. |
| governance/human approval reference | Decision, approval, rejection, deferral, exception reference. | Medium to high. | governance reference. | Traceability only. | Governance reference is not proof level. |
| incident/blocker evidence | Safe record of incident, blocker, failure, skipped/blocked state. | High. | redacted summary, restricted trace. | PL-0, PL-4, PL-7. | May restrict further use. |

## 5. Evidence Non-Types

Not evidence by itself: model confidence, repeated agent assertion, subagent agreement, context inclusion, folder proximity, folder name, Git commit, Git push, clean worktree, README claim, external source presence, product folder presence, old canonical label, generated summary without source, graph projection without validation, absence of output, unreviewed artifact, passing test without scope, command output without command metadata, citation without source-status review, license file without license review, and `.gitignore` match as security proof.

## 6. Evidence Retention Model

| Posture | Compact meaning |
| --- | --- |
| `retain_none` | Nothing retained because evidence is irrelevant, unsafe, or not needed. |
| `retain_safe_metadata_only` | Keep path/category/status/size/date/ignored status when safe. |
| `retain_summary` | Keep concise factual summary without sensitive content. |
| `retain_redacted_summary` | Keep summary with sensitive details removed. |
| `retain_reference` | Keep pointer/path/section/ref, not copied content. |
| `retain_review_note` | Keep structured reviewer findings, scope, limitations, citations. |
| `retain_command_record` | Keep exact command metadata, cwd, target, result summary, limitations. |
| `retain_output_excerpt` | Keep small reviewed excerpt only when safe and necessary. |
| `retain_full_output` | Keep full output only when low-risk, reviewed, scoped, and needed. |
| `retain_local_only` | Keep in local-only area/reference; no publication or commit by default. |
| `retain_generated_artifact` | Keep generated artifact as generated-sensitive until reviewed. |
| `retain_external_reference` | Keep external metadata/review reference, not raw source copy. |
| `retain_product_scoped` | Keep evidence inside product scope and limits. |
| `retain_sensitive_restricted` | Keep only with narrow access and security/governance review. |
| `retain_governance_reference` | Keep decision/approval/rejection/defer/exception reference. |
| `retain_historical_trace` | Keep stale/superseded/invalidated record for audit only. |
| `do_not_retain` | Never store content, especially secret/credential values. |

Retention defaults: references and summaries are preferred over raw output. Commit-safe evidence must be non-secret, non-credential, non-local-only, reviewed, scoped, and not product/external restricted by default. Context/publication require stricter review.

## 7. Evidence Sensitivity Model

S-03 sensitivity categories apply: `public`, `internal`, `local_only`, `sensitive`, `restricted`, `secret`, `credential`, `external_restricted`, `product_restricted`, `generated_sensitive`, and `unknown_sensitivity`.

Handling rules:

| Category group | Evidence handling |
| --- | --- |
| public/internal | May be retained or cited when scoped and reviewed. Publication still needs review. |
| local_only | May support local review, but not default context, commit, or publication. |
| sensitive/restricted | Use redacted summaries, restricted references, and escalation. |
| secret/credential | Values are never retained as evidence content. Safe metadata about posture may be evidence. |
| external_restricted | Retain metadata/review references; raw sources remain local-only by default. |
| product_restricted | Retain product-scoped evidence only; no root authority implication. |
| generated_sensitive | Treat outputs/logs/artifacts as unsafe until reviewed. |
| unknown_sensitivity | Treat as sensitive and escalate before exposure or retention. |

## 8. Command Output and Git Evidence Policy

Command output evidence requires: exact command, working directory, actor/profile, date, target, criterion, expected output, actual output summary, exit status if available, files affected, side effects, execution risk, sensitivity review, local-only review, retention posture, limitations, and revalidation trigger.

Command rules: command output is evidence; it may be sensitive; raw output is not retained by default; low-risk validation commands are still scoped execution; passing output approves nothing; failed, skipped, partial, or blocked command evidence must remain visible.

Git evidence: `git status --short`, `git diff --name-status`, `git diff --cached --name-status`, `git check-ignore`, branch, remote, log, staged files, untracked files, and ignored files may support Git-state claims. Git evidence does not prove semantic correctness, does not approve anything, may reveal local-only risk, and must stop if staged secret/local-only material appears. Git commit and Git push are not proof. Exact staging remains human-gated.

## 9. Review Note and Citation Evidence Policy

Manual review notes are non-command validation evidence. Required fields: reviewer, role/profile, date, files inspected, files not inspected, scope, criteria, findings, uncertainty, contradictions, blockers, residual risks, citations, limitations, and freshness triggers.

Review notes can support PL-3, PL-4, or PL-7 depending on structure and scope, but are not proof by themselves.

Citation evidence requires source path, source status, cited claim, citation target, relevance, freshness, limitation, direct/indirect posture, and missing/stale/conflicted citation records where applicable. Citation evidence supports provenance and auditability, not truth.

## 10. Generated / Log / Runtime Evidence Policy

Generated evidence includes generated docs, summaries, reports, artifacts, graphs/projections, logs, exports, command output, model-generated text, and tool-generated output.

Generated evidence requires source inputs, generator/tool identity, command or method when applicable, generated status, sensitivity review, retention posture, citation requirements, and freshness risk. Generated evidence is not source by default.

Logs and runtime outputs are generated-sensitive by default. They may contain secrets, credentials, local paths, provider output, partial state, or incomplete state. Raw logs remain local-only unless explicitly reviewed. Safe summaries may be retained when provenance and limitations are explicit.

Generated graphs/projections do not decide the Cognitive Semantic System substrate. Graph remains a candidate representation only.

## 11. External / Product / Migration / Dataset / Model Evidence Policies

| Domain | Evidence policy |
| --- | --- |
| External sources | Source metadata, provenance, license posture, notices, runtime risk, dependency risk, instruction status, network/auth risk, pattern evidence, substrate candidate evidence, and blocked-use evidence are review evidence only. They do not approve dependency adoption, reuse, execution, publication, or active instructions. V-05 specializes later. |
| Products | Product inventory, charter draft, scope, owner, Git posture, validation baseline, dependency posture, security posture, generated output, test output, and activation blockers are product-scoped. Product tests do not activate products or prove root authority. V-04 specializes later. |
| Migration | Classification, source/target paths, source status, restatement fidelity, citation coverage, local-only/security posture, blocker, and audit evidence support migration planning only. Migration evidence does not execute or approve migration. V-03 specializes later. |
| Datasets | Provenance, license, sensitivity, privacy, size/format, intended use, retention, publication posture, and local-only posture may be metadata evidence. Raw datasets remain local-only by default. |
| Models | Provenance, license, safety, intended use, storage, execution/use posture, evaluation status, and local-only posture may be metadata evidence. Metadata does not authorize use, training, execution, deployment, or publication. |

## 12. Evidence Quality and Usability

Quality dimensions: directness, completeness, provenance, source status clarity, citation adequacy, method fit, reproducibility, freshness, sensitivity handling, local-only handling, reviewer clarity, limitation clarity, residual risk clarity, revalidation trigger clarity, governance linkage, and security/access compliance.

Strong evidence is direct, scoped, cited, fresh, sensitivity-reviewed, reproducible enough for its use, and explicit about limitations. Weak evidence is indirect, stale, missing source status, missing sensitivity, missing criteria, or unclear about reviewer/method. Disqualifying conditions include exposed secrets/credentials, missing scope, missing source, missing limitations, or unsafe retention.

Evidence can support answers, explanations, proposals, proof-level support, validation verdict support, blocker support, governance review, promotion review, migration planning, product review, external review, later implementation readiness, publication review, incident review, and historical trace. Evidence does not approve these uses.

## 13. Evidence Lifecycle / Freshness

Lifecycle states: `proposed_evidence`, `collected`, `metadata_recorded`, `reviewed`, `accepted_for_validation`, `rejected_for_validation`, `retained`, `retained_local_only`, `redacted`, `summarized`, `stale`, `invalidated`, `superseded`, `historical`, `incident_restricted`, `do_not_retain`.

Freshness triggers: source changed, target changed, citation changed, policy changed, proof criteria changed, security/access changed, execution policy changed, product state changed, external source version changed, dataset/model metadata changed, command changed, environment changed, generated output regenerated, Git state changed, context pack regenerated, incident occurred, governance decision superseded, or Cognitive Semantic System substrate decision affects representation.

Stale evidence remains historical, can support audit trail, must be labeled, and cannot support current promotion without review.

## 14. Evidence Incident Handling

Incidents include: evidence contains secret, evidence contains credential, evidence contains sensitive local-only content, evidence copied into wrong doc, evidence retained in unsafe place, command output contains secret, log contains credential, generated artifact leaks local-only data, evidence cited without source status, stale evidence used as current, evidence interpreted as approval, local-only evidence staged, raw external source copied, product evidence used as root authority, or migration evidence treated as migration approval.

General response: STOP, report safe metadata only, require human/security/governance action, do not expose values, do not quote or transform secret/credential material, do not continue adjacent work, do not stage/commit/push, and mark affected evidence `incident_restricted`, `invalidated`, `redacted`, or `do_not_retain` as appropriate.

## 15. Compact Evidence Matrices

### Matrix A. Evidence Type Vs Retention Posture

| Evidence group | Default retention | Local-only? | Commit-safe? | Proof support |
| --- | --- | --- | --- | --- |
| path/file/Git metadata | safe metadata, command record | Usually no, unless paths sensitive | Usually if reviewed | PL-1, PL-5 |
| citation/source-status/review/coherence/matrix | reference, review note, summary | Depends on source | Yes if non-sensitive | PL-2, PL-3, PL-4, PL-7 |
| command/test/build/runtime/log | command record, summary, excerpt if safe | Often yes | Only after review | PL-5, PL-6, PL-7 |
| generated artifacts/context packs | generated artifact, safe metadata, reference | Default yes for artifacts | Not by default | PL-1 to PL-5 |
| external/product/migration/data/model | external/product/migration/local-only reference | Often yes | Only scoped metadata | PL-2, PL-3, PL-4, PL-7 |
| governance/incident/blocker | governance reference, restricted trace | Depends | Only sanitized | Traceability, PL-0, PL-4, PL-7 |

### Matrix B. Source Class Vs Evidence Handling

| Source class group | Allowed evidence | Default retention | Ceiling before specialization | Future ticket/governance |
| --- | --- | --- | --- | --- |
| canonical/security/validation docs | metadata, citation, review, coherence, command checks | summary/review note | PL-7, PL-8 if reproduced | Governance for promotion/publication |
| research/previous knowledge | source-status, citation, review, migration classification | reference/review note/local-only as needed | PL-4 before migration | V-03 for migration |
| external metadata/raw sources | metadata/review only; raw source local-only | external reference | PL-4/PL-7 for review only | V-05 and governance |
| product docs/code | product review/baseline evidence only | product-scoped/local-only | PL-4/PL-7 for review only | V-04 and product governance |
| implementation/scripts/tests/packages/SDK | planning/review; execution only when approved later | summary/command record if scoped | PL-4 without approved execution | Future implementation readiness |
| datasets/models/artifacts/logs/generated | safe metadata, provenance, review, redacted summaries | local-only/default restricted | PL-2/PL-4 unless validated | Future data/model/artifact policy |
| Git/context/publication/Cognitive Semantic System records | Git state, context assembly, publication review, candidate record review | reference/summary | PL-4/PL-7 | Governance and future substrate decision |

### Matrix C. Evidence Type Vs Proof Level Support

| Evidence group | Supports PL-1 | PL-2 | PL-3 | PL-4 | PL-5 | PL-6 | PL-7 | PL-8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| path/file/Git metadata | Yes | Sometimes | No | No | Yes if command | No | Audit input | Recheck input |
| source-status/citation | No | Yes | Yes | Yes | Sometimes | No | Audit input | Reproduced review |
| content/coherence/matrix/contradiction/review note | No | Sometimes | Yes | Yes | No | No | Yes | Reproduced review |
| command/validation command | Yes | Sometimes | Sometimes | Sometimes | Yes | No | Audit input | Rerun evidence |
| test/build/runtime/log | No | Sometimes | No | Sometimes | Yes | Yes if scoped | Yes | Reproduced run |
| generated/context/external/product/migration/data/model | Sometimes | Yes | Sometimes | Yes when reviewed | Sometimes | Domain later | Yes when audited | Yes if reproduced |
| governance/incident/blocker | Gap only | No | No | Qualifies | No | No | Audit trace | No proof by itself |

## 16. Evidence Invariants

| ID | Invariant |
| --- | --- |
| EVID-001 | Evidence is not truth. |
| EVID-002 | Evidence is not governance. |
| EVID-003 | Evidence is not approval. |
| EVID-004 | Evidence requires source status. |
| EVID-005 | Evidence requires sensitivity posture. |
| EVID-006 | Evidence requires scope. |
| EVID-007 | Evidence requires limitations. |
| EVID-008 | Secret values are never retained as evidence. |
| EVID-009 | Credential values are never retained as evidence. |
| EVID-010 | Generated evidence is not source by default. |
| EVID-011 | Local-only evidence is no default publication. |
| EVID-012 | Command output is scoped evidence only. |
| EVID-013 | Git state is evidence, not proof of correctness. |
| EVID-014 | Citation evidence is provenance, not truth. |
| EVID-015 | Product evidence is product-scoped. |
| EVID-016 | External evidence does not approve adoption. |
| EVID-017 | Migration evidence does not execute migration. |
| EVID-018 | Stale evidence cannot support current promotion without review. |
| EVID-019 | Context inclusion is not evidence validation. |
| EVID-020 | Cognitive substrate remains undecided. |

## 17. Anti-patterns

Evidence anti-patterns: evidence by confidence, evidence by repetition, evidence by subagent agreement, evidence by context inclusion, evidence by folder proximity, evidence by Git commit, evidence by clean worktree, evidence by no output, evidence by README claim, evidence by old canonical label, evidence by generated summary, evidence by graph projection, evidence by unreviewed artifact, evidence by hidden log, evidence by secret exposure, evidence by raw `.env` content, product test as root truth, external license as adoption approval, migration audit as migration approval, retaining full sensitive output unnecessarily, publishing local-only evidence, and treating safe metadata as permission to inspect content.

## 18. Remaining Gaps

V-02R does not solve: no V-03, no V-04, no V-05, no V-A, no validation registry implementation, no schemas, no CI, no tests, no scanners, no enforcement, no evidence database, no context-pack validation generator, no product baselines, no dependency approval registry, no implementation readiness, and no Cognitive Semantic System implementation.

## 19. Readiness For V-03

V-03 is ready after explicit instruction. It should specialize migration validation for migration plans, migration batches, previous knowledge restatement, source/target mapping, restatement fidelity, citation coverage, local-only posture, security/access posture, Git posture, evidence retention, blockers, and migration audit.

Do not create V-03 from V-02R.

## 20. Final Verdict

| Question | Answer |
| --- | --- |
| What is validation evidence? | Scoped material that can support, challenge, qualify, block, or contextualize validation claims, proof levels, verdicts, limitations, residual risks, or governance review. |
| What evidence types exist? | Metadata, Git, citation, source-status, review, coherence, command, generated, log, audit, reproduction, external, product, migration, dataset/model, context, governance, incident, and blocker evidence. |
| What can be retained? | Safe metadata, summaries, redacted summaries, references, review notes, command records, reviewed excerpts, scoped full output only when safe, local-only references, generated artifacts, governance references, and historical traces. |
| What must remain local-only? | Raw local-only material, raw external sources, product-restricted material by default, raw logs/runtime outputs, raw datasets/models, generated-sensitive artifacts, and any sensitive output not reviewed for broader exposure. |
| What must never be retained? | Secret values, credential values, unsafe raw `.env` content, token fragments, private key material, credential-derived fingerprints, and sensitive raw output without approved handling. |
| How does evidence support proof levels? | Evidence supplies the material required for PL-1 through PL-8, but only when source status, sensitivity, scope, method, freshness, criteria, and limitations are explicit. |
| What remains blocked? | V-03/V-04/V-05/V-A, registry implementation, schemas, CI, tests, scanners, enforcement, migration execution, product activation, external adoption, implementation readiness, staging, commit, push, and Cognitive Semantic System implementation. |
| Is V-03 ready? | Yes, after explicit instruction only. |

Stop rule: after completing V-02R, STOP. Do not start V-03, stage, commit, push, implement, migrate, activate products, adopt external sources, run project/product/external code, install dependencies, authenticate, or call network/provider/API/MCP.
