# M-09 - First Controlled Migration Batch
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | First Controlled Migration Batch |
| Ticket | M-09 |
| Status | Accepted first controlled metadata-only migration batch |
| Date | 2026-07-01 |
| Scope | One small metadata-only controlled migration batch record for AGENT PLATFORM migration planning posture |
| Batch ID | M09-BATCH-001 |
| Authority | Metadata-only migration batch record; not raw migration, archive execution, product activation, external adoption, implementation, publication, staging, commit, or push |
| Related documents | A-00, A-01, M-02 through M-08, V-03, S-series, W-series, CSS-series, H-series |

## 2. Purpose
M-09 follows M-08. A-00/A-01 defined archive and lifecycle posture. M-02 through M-07 prepared safe-metadata migration planning. M-08 defined archive execution policy. M-09 executes the first controlled batch as metadata-only by creating one batch record and no other artifacts.
M-09 does not migrate raw files, create `_archive/`, move, copy, delete, rename, transform, archive, stage, commit, push, publish, or apply lifecycle states. M-09 prepares M-A - Migration Audit and does not start M-A.

## 3. Batch Definition
M09-BATCH-001 is a small, exact-scope, metadata-only controlled migration batch that consolidates accepted safe migration-planning metadata from M-02 through M-08 into a single auditable batch record.
It is a batch record, metadata-only, and controlled migration process validation. It is not raw content migration, archive execution, product activation, external adoption, dependency adoption, implementation, publication, or Git approval.

## 4. Batch Authorization Boundary
The explicit M-09 ticket authorizes creation of `0_architecture/migration/agent_platform_first_controlled_migration_batch.md` only. It does not authorize raw migration, file movement, archive execution, Git staging/commit/push, product/external/provider/API/MCP activation, dependency adoption, publication, implementation, or starting M-A.

## 5. Exact Source Scope
| source_id | exact path | role in batch | allowed metadata use | blocked use |
| --- | --- | --- | --- | --- |
| SRC-001 | `0_architecture/archive/agent_platform_archive_policy.md` | A-00 Archive Policy | Archive non-deletion/lifecycle posture. | Archive execution or `_archive/`. |
| SRC-002 | `0_architecture/archive/agent_platform_supersession_deprecation_retention_model.md` | A-01 lifecycle model | Supersession/deprecation/retention vocabulary. | Applying states to files. |
| SRC-003 | `0_architecture/migration/agent_platform_previous_knowledge_carry_forward_extraction.md` | M-02 carry-forward | Prior safe metadata summary. | Raw previous-knowledge migration. |
| SRC-004 | `0_architecture/migration/agent_platform_conflicted_semantic_material_normalization.md` | M-03 conflicts | Naming/substrate conflict posture. | Raw normalization or current authority. |
| SRC-005 | `0_architecture/migration/agent_platform_agent_context_runtime_provider_adapter_migration.md` | M-04 representation planning | Agent/context/runtime/provider/adapter posture. | Implementation or activation. |
| SRC-006 | `0_architecture/migration/agent_platform_research_evidence_migration.md` | M-05 research evidence | Research evidence route summary. | Research adoption or raw copying. |
| SRC-007 | `0_architecture/migration/agent_platform_external_metadata_migration.md` | M-06 external metadata | External source metadata posture. | External source adoption/execution. |
| SRC-008 | `0_architecture/migration/agent_platform_product_workspace_charter_preparation.md` | M-07 product preparation | Product charter-prep posture. | Product activation/source migration. |
| SRC-009 | `0_architecture/archive/agent_platform_archive_execution_policy.md` | M-08 archive execution policy | Future exact-scope archive gates. | Archive execution now. |
| SRC-010 | `0_architecture/validation/agent_platform_migration_validation_model.md` | V-03 migration validation | Migration proof/verdict/blocker posture. | Migration approval. |
| SRC-011 | `0_architecture/validation/agent_platform_validation_evidence_model.md` | V-02 evidence model | Evidence retention/sensitivity posture. | Evidence as truth. |
| SRC-012 | `0_architecture/validation/agent_platform_proof_levels.md` | V-01 proof levels | PL-1 through PL-8 vocabulary. | Proof as governance. |
| SRC-013 | `0_architecture/security/` | S-series Security / Access docs | Local-only, secret, execution, Git constraints. | Execution/auth/network/Git permission. |
| SRC-014 | `0_architecture/workspace/agent_platform_previous_knowledge_classification_index.md` | W-02 classification | Source-class counts and local-only posture. | Raw corpus use. |
| SRC-015 | `0_architecture/workspace/agent_platform_migration_plan.md` | W-08 migration plan | Controlled migration principles. | Bulk movement. |
| SRC-016 | `0_architecture/workspace/agent_platform_workspace_governance_promotion_model.md` | W-11 governance | Governance decision boundary. | Agent approval. |
| SRC-017 | `0_architecture/workspace/agent_platform_product_workspace_policy.md` | W-12 product policy | Product local-only/inactive posture. | Product authority/activation. |
| SRC-018 | `0_architecture/workspace/agent_platform_external_source_handling_policy.md` | W-13 external policy | External local-only/evidence posture. | Source reuse/dependency adoption. |
| SRC-019 | `0_architecture/cognitive_semantic_system/agent_platform_cognitive_semantic_system_decision_audit.md` | CSS-series decision/audit | Naming/substrate neutrality. | Final substrate decision. |
| SRC-020 | `0_architecture/harness/agent_platform_harness_strategy_audit.md` | H-series audit/strategy | Harness evidence-only posture. | Harness/runtime activation. |

## 6. Exact Target Scope
Target: `0_architecture/migration/agent_platform_first_controlled_migration_batch.md`.
This file is the only target artifact. No source file is modified, moved, copied, deleted, renamed, transformed, archived, or replaced. No archive folder is created. No migration output outside this file is produced.

## 7. Batch Action Type
Action type: `metadata_only_controlled_migration_record`.
Meaning: restates compact safe metadata from accepted planning docs, produces one auditable batch ledger, demonstrates exact-scope process, and preserves blockers and boundaries.
Blocked: raw source migration, file operation, archive execution, lifecycle state execution, product activation, external adoption, dependency adoption, implementation, publication, and Git action.

## 8. Migrated Metadata Classes
| Metadata class | Meaning | Allowed use | Blocked use |
| --- | --- | --- | --- |
| `migration_planning_summary` | M-02 through M-07 posture. | M-A audit input. | Raw migration. |
| `lifecycle_policy_summary` | A-00/A-01 lifecycle constraints. | Lifecycle vocabulary. | State execution. |
| `archive_execution_policy_summary` | M-08 gates. | Archive-readiness audit. | Archive action. |
| `previous_knowledge_safe_metadata_summary` | W-02/M-02 safe metadata. | Trace planning. | Raw corpus copy. |
| `conflicted_semantic_safe_metadata_summary` | M-03/CSS conflict posture. | Naming/substrate caution. | Current old naming. |
| `agent_context_runtime_provider_adapter_summary` | M-04/H evidence posture. | Future architecture review. | Runtime/tool activation. |
| `research_evidence_summary` | M-05 evidence posture. | Research audit input. | Research adoption. |
| `external_metadata_summary` | M-06/W-13 posture. | External metadata audit. | Source reuse/dependency. |
| `product_charter_preparation_summary` | M-07/W-12 posture. | Product audit input. | Product activation. |
| `validation_security_governance_summary` | V/S/W controls. | Readiness review. | Approval. |
| `blocker_summary` | Cross-series blockers. | M-A blocker ledger. | Bypassing blockers. |
| `audit_readiness_summary` | M-A readiness posture. | Next audit planning. | Starting M-A. |

## 9. Explicit Non-Migration Classes
| Excluded class | Reason excluded | Future route if needed |
| --- | --- | --- |
| raw previous knowledge | Local-only and classified only. | Exact migration/restatement ticket. |
| raw external source | External/local-only risk. | External review. |
| raw product source | Product-scoped/local-only. | Product governance. |
| generated artifacts | Generated-sensitive. | Provenance review. |
| datasets | Local-only/sensitivity. | Data policy/review. |
| models | Local-only/safety/license. | Model policy/review. |
| secrets | Never retained as content. | Secure handling. |
| credentials | Never inspected or used. | Secure auth ticket. |
| dependency content | Supply-chain/license risk. | Dependency review. |
| provider/auth material | Credential/network risk. | Security approval. |
| runtime output | Generated-sensitive. | Validation/evidence review. |
| product build/test output | Product generated-sensitive. | Product validation. |
| archived file content | No archive execution. | M-08-governed future batch. |
| current canonical source replacement | No supersession execution. | Governance/lifecycle ticket. |

## 10. Batch Eligibility Check
M09-BATCH-001 is eligible because the exact target file is declared; exact source documents are declared; source documents exist or are represented by allowed series folders; the batch is metadata-only; no raw local-only source, product/external inspection, file movement, Git action, archive execution, or implementation is required; validation/security posture is declared; rollback/restoration path is declared; stop rules are declared; and M-A readiness is declared.

## 11. Batch Non-Eligibility Cases
The batch is blocked if raw previous knowledge, raw external source, product source, source-code copying, file movement, archive execution, deletion, staging/commit/push, product activation, external adoption, dependency adoption, provider/API/MCP activation, substrate decision, broad migration, or M-A start is required or implied.

## 12. Controlled Migration Method
Method: read accepted architecture/planning documents only; confirm exact source and target scope; retain only safe metadata; create one batch record; summarize prior planning posture compactly; preserve validation, security, lifecycle, product, external, CSS, harness, Git, and context boundaries; record blockers and excluded material; declare restoration/rollback path; declare M-A readiness; stop before next ticket or Git action.

## 13. Batch Ledger
| batch_id | action_type | source scope | target artifact | migrated content class | execution status | blocked content | validation posture | security posture | restoration path | next route |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M09-BATCH-001 | `metadata_only_controlled_migration_record` | A-00/A-01/M-02..M-08/V/S/W/CSS/H approved docs | `0_architecture/migration/agent_platform_first_controlled_migration_batch.md` | safe metadata summaries only | executed as document creation only | raw content/file operations blocked | PL-1 through PL-4 planning evidence | local-only preserved | delete target doc if rollback required; source docs unchanged | M-A Migration Audit |

## 14. Controlled Migration Table
| record_id | source | metadata migrated into M-09 | allowed future use | blocked inference | route |
| --- | --- | --- | --- | --- | --- |
| M09-REC-001 | A-00/A-01 | Archive/lifecycle non-execution baseline. | M-A lifecycle audit. | File state change. | lifecycle review later. |
| M09-REC-002 | M-02/W-02 | Previous knowledge safe-metadata posture. | Carry-forward audit. | Raw corpus migration. | M-A. |
| M09-REC-003 | M-03/CSS | Conflicted semantic normalization posture. | Naming/substrate audit. | Old name/current authority. | M-A/CSS later. |
| M09-REC-004 | M-04/H | Agent/context/runtime/provider/adapter posture. | Harness/runtime boundary audit. | Tool/runtime/provider activation. | M-A/H later. |
| M09-REC-005 | M-05 | Research evidence posture. | Evidence audit. | Research adoption. | M-A. |
| M09-REC-006 | M-06/W-13 | External metadata posture. | External audit. | Source reuse/dependency approval. | M-A/external review. |
| M09-REC-007 | M-07/W-12 | Product charter-prep posture. | Product boundary audit. | Product activation. | M-A/product governance. |
| M09-REC-008 | M-08 | Archive execution gates. | Archive execution audit criteria. | Archive action. | M-A. |
| M09-REC-009 | V/S/W | Validation/security/governance posture. | Process audit. | Approval or permission. | M-A. |
| M09-REC-010 | M-02..M-08 | Audit readiness baseline. | M-A scope seed. | Starting M-A now. | M-A after instruction. |

## 15. Validation Evidence
V-03/V-02/V-01 apply. PL-1: target file exists and source docs exist. PL-2: source status, classification, and sensitivity posture are retained. PL-3: source references and provenance are retained. PL-4: batch coherence and boundary preservation are reviewed. PL-5 is not used by M-09 unless exact future command scope is approved. PL-7 is for future M-A audit. PL-8 is for future reproduced M-A audit.
Validation does not approve broad migration, archive execution, product activation, external adoption, provider/API/MCP activation, dependency adoption, implementation, publication, staging, commit, or push.

## 16. Security / Local-only Posture
`previusknowledge/`, `2_products/`, `4_external/sources/`, datasets, models, and artifacts remain local-only. Secrets and credentials are never extracted. Unknown sensitivity blocks use. M-09 uses safe metadata only, migrates no local-only raw content, and contains no raw local-only content.

## 17. Lifecycle / Archive Boundary
M-09 does not apply lifecycle states to actual files, execute archive, create `_archive/`, or mark actual files superseded, deprecated, retained, archived, restored, or deleted. Lifecycle posture is summarized only as safe metadata.

## 18. Product Boundary
Product candidates remain local-only, inactive, product-scoped, dependency-blocked, and Git-unchanged. Product source is not inspected. Product charters are not activated. Product dependencies are not adopted. Product material is not migrated. Product Git posture is not changed.

## 19. External Source Boundary
External sources remain external/local-only. Raw external sources are not inspected deeply or migrated. External metadata remains evidence only. External instructions remain inactive. Dependency adoption, source reuse, execution, provider/API/MCP activation, and publication remain blocked.

## 20. Cognitive Semantic System Boundary
`Cognitive Semantic System` is the accepted current name. Final substrate remains undecided. Graph remains a candidate only. Graphify remains external, historical, or candidate evidence only. `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth` appear only as rejected/prohibited/historical naming examples. M-09 does not decide substrate or create graph implementation, graph registry, GNN, vector index, relational schema, or CSS implementation.

## 21. Harness / Runtime / Provider / Tool Boundary
Harness, runtime, provider, tool, and MCP material remains evidence only. OpenCode/operator-tool behavior is not platform authority. Tool availability is not permission. Provider credentials are not provider permission. MCP availability is not MCP activation. No runtime, tool, provider, MCP, harness, or agent implementation or activation occurs.

## 22. Git / Publication Boundary
M-09 does not stage, commit, push, amend, reset, clean, publish, force-add, or use `git add .`. Git state is evidence only. Commit is not migration approval. Push is publication-like. Future commit, if a user chooses, must be exact-path only after explicit approval.

## 23. Restoration / Rollback Path
Source docs remain unchanged. The target artifact is the only new file. Rollback path: delete or revert only the target M-09 file before commit, or revert the exact commit later if committed by a human. Rollback does not touch source docs. Restoration is not a current-authority change. No archive restoration is needed because no archive execution occurs.

## 24. Stop Rules
Stop if a source document is missing and cannot be safely handled; target file already exists with conflicting content; raw content, local-only raw inspection, secret/credential handling, file operation beyond target creation, product/external execution, provider/API/MCP activation, Git staging/commit/push, substrate decision, broad migration, or M-A scope begins.

## 25. Blocker Register
| blocker | stop behavior | required action | blocks M-09? | blocks M-A? |
| --- | --- | --- | --- | --- |
| missing M-08 | Stop batch. | Create/validate M-08. | Yes | Yes |
| missing M-02 through M-07 | Stop source scope. | Restore inputs. | Yes | Yes |
| missing A-00/A-01 | Stop lifecycle claims. | Restore inputs. | Yes | Yes |
| missing V-03/V-02 | Stop validation posture. | Restore inputs. | Yes | Yes |
| missing S-series | Stop security posture. | Restore inputs. | Yes | Yes |
| target path conflict | Stop write. | Human decision. | Yes | Maybe |
| raw content requirement | Stop. | New scoped ticket. | Yes | Yes |
| unknown sensitivity | Safe metadata only. | Security review. | Yes | Yes |
| local-only exposure risk | Stop exposure. | Security/governance review. | Yes | Yes |
| secret/credential risk | Stop immediately. | Secure handling. | Yes | Yes |
| file movement implied | Stop. | Migration governance. | Yes | Yes |
| archive execution implied | Stop. | M-08-governed future ticket. | Yes | Yes |
| product activation implied | Stop. | Product governance. | Yes | Yes |
| external adoption implied | Stop. | External review. | Yes | Yes |
| dependency adoption implied | Stop. | Dependency governance. | Yes | Yes |
| provider/API/MCP activation implied | Stop. | Security/governance approval. | Yes | Yes |
| broad migration implied | Stop. | Narrow exact batch. | Yes | Yes |
| Git action implied | Stop. | Human exact-path approval later. | Yes | Maybe |
| M-A started | Stop adjacent work. | Wait explicit M-A instruction. | No | Yes |

## 26. Incident Handling
Incidents include raw previous knowledge copied, raw external content copied, raw product content copied, secret/credential exposed, source file moved/copied/deleted/renamed/transformed, `_archive/` created, archive execution performed, lifecycle state applied to actual file, product activated, external source adopted, dependency installed/adopted, provider/API/MCP activated, Git staging attempted, publication attempted, or M-A started.
Response: STOP, report safe metadata only, do not continue adjacent work, and require human/security/governance decision.

## 27. Batch Verdict Model
Verdicts: `controlled_batch_executed_metadata_only`, `controlled_batch_ready_for_audit`, `controlled_batch_complete_with_cautions`, `controlled_batch_blocked_by_missing_inputs`, `controlled_batch_blocked_by_raw_content_requirement`, `controlled_batch_blocked_by_security_risk`, `controlled_batch_blocked_by_local_only_risk`, `controlled_batch_blocked_by_scope_expansion`, `controlled_batch_blocked_by_git_action`, `controlled_batch_blocked_by_governance_gap`, and `controlled_batch_inconclusive`.
A verdict is not approval for broad migration.

## 28. M-09 Invariants
| ID | Invariant |
| --- | --- |
| M09-001 | First controlled batch is metadata-only. |
| M09-002 | Controlled migration is not broad migration. |
| M09-003 | Exact source scope is mandatory. |
| M09-004 | Exact target scope is mandatory. |
| M09-005 | Safe metadata is preferred over raw content. |
| M09-006 | Local-only remains no default publication. |
| M09-007 | Previous knowledge remains local-only. |
| M09-008 | Product material remains product-scoped. |
| M09-009 | External sources remain external. |
| M09-010 | Archive execution is not performed. |
| M09-011 | Lifecycle states are not applied to actual files. |
| M09-012 | Git state is evidence, not migration approval. |
| M09-013 | Graph remains a candidate only. |
| M09-014 | Validation evaluates; governance decides. |
| M09-015 | M-09 stops before M-A. |

## 29. Anti-patterns
Anti-patterns: first batch as broad migration; first batch by folder copy; first batch by raw source dump; first batch by search-and-replace; first batch by archive execution; first batch by product activation; first batch by external adoption; first batch by dependency installation; first batch by provider/API/MCP activation; metadata-only batch treated as content migration; Git commit as migration approval; `git add .`; starting M-A inside M-09.

## 30. Remaining Gaps
No raw previous knowledge migration, raw external source migration, product migration, archive execution, `_archive/`, file movement, lifecycle state execution, product activation, external adoption, dependency adoption, provider/API/MCP activation, implementation readiness, validation registry implementation, security/access enforcement, broad migration batch, or M-A has started.

## 31. Readiness For M-A
M-A - Migration Audit is ready after explicit instruction if the M-09 target exists, exact source/target scope is declared, the batch remains metadata-only, and no raw content migration, file movement, archive execution, product activation, external adoption, dependency adoption, provider/API/MCP activation, or Git action occurred.
M-A should audit the complete controlled migration phase: A-00, A-01, M-02, M-03, M-04, M-05, M-06, M-07, M-08, and M-09. Do not create M-A.

## 32. Final Verdict
| Question | Answer |
| --- | --- |
| What does M-09 execute? | One metadata-only controlled migration batch record. |
| What is the batch ID? | M09-BATCH-001. |
| What is the exact source scope? | A-00/A-01, M-02 through M-08, V-03/V-02/V-01, S-series, W-02/W-08/W-11/W-12/W-13, CSS-A, H-A, `.gitignore`, and `README.md` as safe metadata sources. |
| What is the exact target scope? | `0_architecture/migration/agent_platform_first_controlled_migration_batch.md` only. |
| Is the batch metadata-only? | Yes. |
| Did M-09 migrate raw previous knowledge? | No. |
| Did M-09 migrate raw external/product content? | No. |
| Did M-09 move/copy/delete/rename/transform/archive existing files? | No. |
| Did M-09 create `_archive/`? | No. |
| Did M-09 execute archive actions? | No. |
| Did M-09 apply lifecycle states to actual files? | No. |
| Did M-09 activate products, adopt external sources/dependencies, or activate providers/API/MCP? | No. |
| Did M-09 stage, commit, push, or publish? | No. |
| What remains blocked? | Raw migration, file operations, archive execution, lifecycle execution, product activation, external adoption, dependency adoption, provider/API/MCP activation, implementation, publication, Git actions, broad migration, and M-A. |
| Is M-A ready after explicit instruction? | Yes, as migration audit only; M-A is not started. |
M-09 final verdict:
```text
M-09 is complete as M09-BATCH-001, a metadata-only controlled migration batch
record. It creates one auditable ledger and stops before raw migration, file
operations, archive execution, lifecycle execution, activation, adoption,
implementation, publication, Git actions, and M-A.
```
