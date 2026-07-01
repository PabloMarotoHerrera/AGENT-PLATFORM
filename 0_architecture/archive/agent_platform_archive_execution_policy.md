# M-08 - Archive Execution Policy
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Archive Execution Policy |
| Ticket | M-08 |
| Status | Accepted archive execution policy |
| Date | 2026-07-01 |
| Scope | Future archive execution governance, validation, scope, blockers, security, Git, context, and M-09 readiness for AGENT PLATFORM |
| Authority | Execution policy only, not archive execution, file movement, file copying, deletion, renaming, transformation, staging, commit, push, publication, migration execution, or `_archive/` creation |
| Related documents | A-00, A-01, M-02 through M-07, V-03, S-series, W-series |

## 2. Purpose
M-08 follows M-07. A-00 defined archive policy. A-01 defined lifecycle states. M-02 through M-07 prepared safe-metadata migration planning across previous knowledge, conflicted semantics, runtime/provider/adapter posture, research evidence, external metadata, and product workspace charter preparation.
M-08 defines how future archive execution would be governed before the first controlled migration batch. It does not execute archive actions, create `_archive/`, move, copy, delete, rename, transform, stage, commit, push, publish, or migrate files. It prepares M-09 and does not start M-09.

## 3. Archive Execution Definition
Archive execution is a future governed, exact-scope action that changes the lifecycle handling, location, reference status, or archive posture of explicitly approved material according to A-00/A-01, validation evidence, security constraints, and governance decision.
Archive execution is not deletion, cleanup, migration by itself, publication, rejection by default, Git approval, product activation, external adoption, or implementation. It requires an explicit future ticket.

## 4. Non-Execution Statement
M-08 defines execution policy only. M-08 performs no archive execution, no file movement, no copy, no deletion, no renaming, no transformation, no staging, no commit, no push, no publication, and no `_archive/` creation.

## 5. Archive Execution Authority Boundary
| Layer | Archive execution role |
| --- | --- |
| Governance | Decides archive execution, lifecycle changes, exceptions, deletion candidates, restoration, publication, and Git posture. |
| Validation | Evaluates archive execution readiness and evidence sufficiency; it does not approve. |
| Evidence | Supports archive claims only when source status, scope, sensitivity, provenance, and limits are visible. |
| Security | Constrains material handling, local-only exposure, secrets, credentials, product/external restrictions, generated output, and publication. |
| Git | Records artifact changes only after explicit human approval; Git is evidence, not approval. |
| Agents | May propose or prepare future archive execution packets but cannot execute archive actions. |
| Context | May expose archive references only when safe, scoped, cited, labeled, and not local-only by default. |

## 6. Archive Execution Eligibility
Archive execution is eligible for future governance review only when exact source path/reference, material class, lifecycle state, archive reason, successor/deprecation/retention relation or not-applicable note, sensitivity posture, local-only posture, restoration path, validation evidence, governance owner/path, Git posture, no secret/credential content, no unresolved current authority, and no unresolved product/external/local-only blocker are known.

## 7. Non-Eligible Archive Execution Cases
Blocked cases: unknown sensitivity; possible secret/credential content; unclassified previous knowledge; raw local-only material without safe handling; product material without product governance; external source material without external governance; current canonical authority without supersession; generated output without provenance; material needed by an active ticket; missing restoration path; or any archive action that implies deletion, publication, migration, product activation, dependency adoption, or external adoption.

## 8. Archive Execution Scope Model
Exact scope is mandatory. Future archive execution records must name: `execution_id`, source path/reference, material class, lifecycle reason, archive action type, allowed operation, forbidden operation, validation evidence, security posture, local-only posture, governance decision, Git posture, restoration path, rollback/non-rollback note, reviewer/date, and stop rule.
This is a conceptual model, not a schema, registry, database, script, API, scanner, workflow, tool, or implementation.

## 9. Archive Action Types
| Action type | Meaning | Allowed future use | Blocked use | Governance requirement |
| --- | --- | --- | --- | --- |
| `mark_archive_candidate` | Identify possible archive handling. | Candidate review. | Treating as executed archive. | Owner and reason. |
| `mark_retained_in_place` | Keep where located with lifecycle note later. | Trace without movement. | Hidden current-authority change. | Lifecycle decision. |
| `mark_historical_reference` | Label material as historical evidence. | Citation/audit. | Current authority. | Historical reason. |
| `mark_superseded_reference` | Label replaced material. | Predecessor trace. | Supersession without successor. | Successor and scope. |
| `mark_deprecated_reference` | Label discouraged use. | Warning and legacy use. | Deletion or rejection. | Warning and review trigger. |
| `move_to_archive_later` | Future exact movement candidate. | Governed batch only. | Movement now. | Exact source/target approval. |
| `copy_to_archive_later` | Future exact copy candidate. | Governed copy with provenance. | Copying local-only/raw content. | Security and scope approval. |
| `metadata_only_archive_later` | Retain metadata without content. | Safer local-only/product/external handling. | Content migration. | Metadata scope approval. |
| `archive_index_record_later` | Future index/reference record. | Audit lookup. | Registry implementation by M-08. | Index governance later. |
| `restoration_candidate_later` | Possible future restoration review. | Reconsideration path. | Current authority restoration. | Restoration governance. |
| `deletion_candidate_later` | Possible deletion review only. | Separate deletion ticket. | Deletion approval by archive. | Separate exact deletion governance. |

## 10. No-Deletion Execution Rules
Archive execution does not delete by default. Deletion requires separate governance, security/access review, validation of non-current authority, retention/audit assessment, explicit exact-scope deletion ticket, and human decision. Deletion is blocked for unknown sensitivity and material needed for audit, provenance, migration, rollback, lifecycle trace, or active work. M-08 does not authorize deletion.

## 11. Restoration Path Requirements
Every archive execution candidate must have a restoration path or explicit non-restoration statement. Restoration requires governance and revalidation, does not restore current authority by default, must preserve historical lifecycle labels, cannot expose secrets/credentials, and cannot bypass product, external, local-only, security, validation, or Git boundaries.

## 12. Archive Batch Constraints
Future batches must be small, exact-path/reference listed, single-purpose, governed by one decision, supported by explicit validation evidence, local-only preserving, secret/credential free, reviewable before execution, reversible or non-restoration declared, and stopped on first incident. A batch must not mix product, external, previous-knowledge, generated, and current-canonical material without explicit justification.

## 13. Archive Execution Validation Model
Use V-03 with V-02 evidence and V-01 proof levels. PL-1 supports path/status metadata; PL-2 supports source status, classification, and sensitivity; PL-3 supports citation/provenance review; PL-4 supports lifecycle/coherence review; PL-5 supports future exact scoped Git/path checks; PL-7 supports future archive execution audit; PL-8 applies only to reproduced archive execution audit. No proof level approves archive execution by itself.

## 14. Archive Execution Governance Packet
Future packets must include objective, exact material list, archive action type, reason, lifecycle posture, validation evidence, security review, local-only review, Git posture, restoration path, rollback/non-rollback note, residual risks, blockers, human decision, and stop rule. A packet is future planning; M-08 does not instantiate execution packets for actual files.

## 15. Security / Local-only Execution Rules
`previusknowledge/`, `2_products/`, `4_external/sources/`, datasets, models, and artifacts remain local-only. Secrets and credentials are never archived as content. Unknown sensitivity blocks execution. Safe metadata is preferred. Incident-restricted material requires security/governance handling. Local-only archive movement or publication is blocked by default.

## 16. Previous Knowledge Boundary
Previous knowledge remains local-only. Archive execution of previous knowledge is blocked until an exact migration/archive batch. Safe metadata may be used, raw previous-knowledge content is not copied, M-02 carry-forward and M-03 conflicted records do not authorize archive execution, and wholesale archive of previous knowledge is prohibited.

## 17. Product Boundary
Product material remains product-scoped/local-only. Product archive execution requires product governance. Product source is not inspected by M-08. Product generated output is generated-sensitive. Product Git posture change and product activation are blocked. Archive execution cannot retire, activate, migrate, publish, or validate products by implication.

## 18. External Source Boundary
External sources remain external/local-only. Raw external source archive execution is blocked by default. External metadata archive may become a future review record only. Archive execution does not approve source reuse, dependency adoption, execution, publication, provider/API/MCP activation, or active instructions. Source names do not become internal names. Rejected/prohibited historical labels `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth` may appear only as historical prior material, external source, prohibited naming, or candidate graph/projection evidence examples.
The accepted current architecture name is `Cognitive Semantic System`. Do not assume the final Cognitive Semantic System substrate is graph-based. Graph remains a candidate only.

## 19. Current Canonical Architecture Boundary
Current canonical docs are not archive execution candidates unless supersession is explicit. Supersession/deprecation must be governed before current authority is archived. Current authority cannot be archived by oldness alone. Validation and audit docs remain active unless governance changes posture. Archive execution cannot break roadmap continuity.

## 20. Generated Output Boundary
Generated outputs are not source by default and require provenance before archive handling. Raw generated-sensitive reports, screenshots, logs, exports, projections, and artifacts remain local-only until reviewed. Generated material cannot become authority through archive. Unsafe generated outputs are blocked from archive execution.

## 21. Git / Publication Execution Rules
Git state is evidence only. Staging is execution-adjacent and requires human approval. Commit is not archive approval. Push is publication-like. Local-only staged material and secret/credential staged material are blockers. Future staging must be exact path only; no `git add .`. M-08 does not stage, commit, push, amend, reset, clean, or publish.

## 22. Context Exposure Rules
Archived references may appear in future context only when safe, scoped, cited, labeled, and source status is visible. Context inclusion is not archive execution, restoration, current authority, publication, permission, or Git approval. Local-only archive references remain excluded by default, and archive state must be visible when exposed.

## 23. Archive Execution Candidate Routing
Routes: `ready_for_archive_governance_review`, `blocked_pending_classification`, `blocked_pending_security_review`, `blocked_pending_lifecycle_review`, `blocked_pending_validation`, `blocked_pending_governance`, `deferred_to_M-09`, `deferred_to_product_governance`, `deferred_to_external_review`, `deferred_to_lifecycle_review`, `metadata_only`, and `rejected_for_current_scope`.

## 24. Archive Execution Verdict Model
Verdicts: `archive_execution_policy_ready`, `archive_execution_candidate_ready_for_governance`, `archive_execution_candidate_ready_with_cautions`, `archive_execution_blocked_by_missing_classification`, `archive_execution_blocked_by_security_risk`, `archive_execution_blocked_by_local_only_risk`, `archive_execution_blocked_by_missing_lifecycle`, `archive_execution_blocked_by_missing_validation`, `archive_execution_blocked_by_missing_governance`, `archive_execution_blocked_by_current_authority`, `archive_execution_blocked_by_product_scope`, `archive_execution_blocked_by_external_posture`, `archive_execution_blocked_by_git_posture`, `archive_execution_deferred`, and `archive_execution_rejected_for_current_scope`.
A verdict is not archive execution approval.

## 25. Blocker Register
| Blocker | Stop behavior | Required action | Blocks archive execution? | Blocks M-09? |
| --- | --- | --- | --- | --- |
| missing exact path/reference | Stop candidate. | Name source. | Yes | Yes |
| unknown classification | Stop use. | Classify material. | Yes | Yes |
| unknown sensitivity | Stop exposure. | Security review. | Yes | Yes |
| missing lifecycle posture | Stop lifecycle claim. | A-01 review. | Yes | Yes |
| missing archive reason | Stop archive claim. | State reason. | Yes | Yes |
| missing restoration path | Stop execution. | Add path or non-restoration statement. | Yes | Yes |
| current authority unresolved | Stop archive of current docs. | Supersession/deprecation decision. | Yes | Yes |
| missing validation evidence | Stop readiness claim. | V-03/V-02/V-01 review. | Yes | Yes |
| missing governance decision | Stop action. | Human/governance decision. | Yes | Yes |
| local-only exposure risk | Stop exposure/Git. | Safe metadata/security review. | Yes | Yes |
| secret/credential risk | Stop immediately. | Secure handling. | Yes | Yes |
| product scope unresolved | Stop product handling. | Product governance. | Yes | Yes |
| external posture unresolved | Stop external handling. | External review. | Yes | Yes |
| generated output provenance missing | Stop output use. | Provenance review. | Yes | Yes |
| Git posture unsafe | Stop Git path. | Exact status/diff/governance. | Yes | Yes |
| deletion implied | Stop. | Separate deletion ticket. | Yes | Yes |
| publication implied | Stop. | Publication/security/governance review. | Yes | Yes |
| migration implied | Stop. | M-09 or later exact ticket. | Yes | Yes |
| product activation implied | Stop. | Product activation governance. | Yes | Yes |
| broad batch implied | Stop. | Narrow exact batch. | Yes | Yes |
| M-09 scope pressure detected | Stop adjacent work. | Wait explicit M-09 instruction. | No | Yes |

## 26. Archive Execution Policy Matrix
| Material | Execution eligible? | Default action posture | Required evidence | Governance needed | Local-only handling | Blocked inference |
| --- | --- | --- | --- | --- | --- | --- |
| current canonical doc | Only if superseded | Retain current | successor/scope | Yes | Normal docs review | oldness means archive |
| superseded doc | Candidate | mark superseded/historical | successor/provenance | Yes | Preserve trace | deletion |
| deprecated policy | Candidate | mark deprecated/reference | warning/replacement | Yes | Review before exposure | rejection |
| previous knowledge | Blocked now | metadata only later | W-02/M records | Yes | Local-only | wholesale archive |
| carry-forward candidate | Blocked now | retain metadata | M-02 + validation | Yes | Safe metadata | migration approval |
| conflicted candidate | Blocked now | retain conflict trace | M-03/CSS | Yes | Safe metadata | current wording |
| product material | Blocked by default | product governance later | W-12/V-04 | Product yes | `2_products/` local-only | activation/retirement |
| external source metadata | Maybe later | metadata record | W-13/V-05/M-06 | Yes | No raw source | adoption |
| raw external source | No by default | blocked | external review | Yes | `4_external/sources/` local-only | source reuse |
| generated artifact | Blocked until provenance | metadata/provenance | V-02/S-series | Yes | generated-sensitive | source truth |
| context trace | Maybe | labeled trace | source/status/sensitivity | Yes | exclude local-only | authority/restoration |
| validation/audit doc | Usually active | retain current | supersession if any | Yes | normal docs review | archive by age |
| secret/credential material | No | do not retain content | safe incident metadata | Security yes | never expose | archive as content |
| unknown material | No | blocked | classify/sensitivity | Yes | treat sensitive | safe to archive |

## 27. Incident Handling
Incidents include secret/credential found, local-only material exposed, archive execution used as deletion, archive execution used as migration, archive execution used as publication, current authority archived without supersession, product material archived as root material, external source archived as adopted dependency, generated output archived as source, Git staging attempted, broad batch attempted, or M-09 started.
Response: STOP, report safe metadata, do not continue adjacent work, and require human/security/governance decision.

## 28. M-08 Invariants
| ID | Invariant |
| --- | --- |
| M08-001 | Archive execution policy is not archive execution. |
| M08-002 | Archive execution is not deletion. |
| M08-003 | Archive execution is not migration. |
| M08-004 | Governance decides archive execution. |
| M08-005 | Validation evaluates archive readiness. |
| M08-006 | Security constrains archive handling. |
| M08-007 | Exact scope is mandatory. |
| M08-008 | Restoration path or non-restoration statement is mandatory. |
| M08-009 | Local-only remains no default publication. |
| M08-010 | Secrets and credentials are never archived as content. |
| M08-011 | Git state is evidence, not archive approval. |
| M08-012 | Context exposure is not restoration. |
| M08-013 | Product material remains product-scoped. |
| M08-014 | External sources remain external. |
| M08-015 | M-08 stops before M-09. |

## 29. Anti-patterns
Anti-patterns: archive execution by folder move; archive execution by Git commit; archive execution by `git add .`; archive execution by oldness; archive execution by cleanup preference; archive as deletion; archive as migration; archive as publication; archive as product retirement; archive as external adoption; archive of secrets/credentials; archive of current authority without supersession; archive of local-only content into public docs; broad archive batch; starting M-09 inside M-08.

## 30. Remaining Gaps
No archive execution, `_archive/` folder, archive execution batch, actual file movement, actual staging/commit/push, migration execution, first controlled migration batch, product activation, external adoption, deletion policy execution, restoration workflow implementation, validation registry implementation, security/access enforcement, implementation readiness, or M-09 has started.

## 31. Readiness For M-09
M-09 - First Controlled Migration Batch is ready after explicit instruction if M-08 archive execution policy exists, M-02 through M-07 safe-metadata planning is preserved, A-00/A-01 lifecycle rules are preserved, V-03 migration validation rules are preserved, S-series security/local-only rules are preserved, exact source and target scope are declared, and no broad migration, raw local-only copying, product activation, external adoption, dependency adoption, provider/API/MCP activation, publication, or implementation is implied.
M-09 should define and execute, only if explicitly authorized, the first small controlled migration batch. It must not be broad, automatic, or unbounded. Do not create M-09.

## 32. Final Verdict
| Question | Answer |
| --- | --- |
| What does M-08 define? | Canonical archive execution governance policy for future exact-scope archive actions. |
| Did M-08 execute archive actions? | No. |
| Did M-08 create `_archive/`? | No. |
| Did M-08 move/copy/delete/rename/transform/archive files? | No. |
| Did M-08 stage, commit, push, or publish? | No. |
| Did M-08 execute migration? | No. |
| Did M-08 apply lifecycle states? | No. |
| What remains blocked? | Archive execution, `_archive/` creation, file movement/copy/deletion/rename/transformation, migration execution, lifecycle state application, product activation, external adoption, dependency adoption, provider/API/MCP activation, implementation, publication, staging, commit, push, and M-09. |
| Is M-09 ready after explicit instruction? | Yes, as the first small controlled migration batch only; M-09 is not started. |
M-08 final verdict:
```text
M-08 is complete as archive execution policy only. It defines future exact-scope
archive execution governance and stops before archive execution, _archive creation,
file movement, migration execution, lifecycle application, Git actions, publication,
product activation, external adoption, implementation, and M-09.
```
