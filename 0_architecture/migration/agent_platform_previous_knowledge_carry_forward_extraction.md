# M-02 - Previous Knowledge Carry-Forward Extraction
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Previous Knowledge Carry-Forward Extraction |
| Ticket | M-02 |
| Status | Accepted carry-forward extraction |
| Date | 2026-06-30 |
| Scope | Safe-metadata extraction of W-02 `carry_forward` previous-knowledge records into migration planning candidates |
| Authority | Extraction planning only, not migration execution, promotion, archive execution, lifecycle action, product activation, external adoption, implementation, staging, commit, push, publication, or M-03 start |
| Related documents | A-00, A-01, V-03, CSS-02, W-02, W-08, S-series |
## 2. Purpose
M-02 follows A-00 and A-01. A-00 defined archive policy; A-01 defined lifecycle states for supersession, deprecation, and retention.
M-02 extracts carry-forward candidates from approved W-02 classification metadata. It does not migrate, copy, move, rewrite, archive, normalize, or promote previous knowledge.
M-02 prepares M-03 - Conflicted Semantic Material Normalization by identifying deferred/conflicted routing. M-02 does not start M-03.
## 3. Carry-Forward Definition
Carry-forward is a previous-knowledge concept, pattern, rationale, constraint, or architectural insight that may remain useful for AGENT PLATFORM after restatement, citation, validation, lifecycle review, security review, and governance.
Carry-forward is not current authority, migration execution, content copy, archive execution, supersession, product activation, external adoption, or validation approval.
Carry-forward is candidate evidence only until governed.
## 4. Extraction Authority Boundary
| Layer | M-02 boundary |
| --- | --- |
| Governance | Decides promotion, migration, acceptance, rejection, lifecycle, publication, and exceptions. |
| Validation | Evaluates carry-forward readiness; V-03 controls migration validation posture. |
| Evidence | Supports candidate extraction through source reference, W-02 class, limits, and blockers. |
| Security | Constrains local-only, secret, credential, product, external, generated, and sensitive handling. |
| A-00/A-01 | Define archive/lifecycle posture without executing lifecycle states. |
| CSS-02 | Defines Graphify normalization boundaries and substrate neutrality. |
| Agents | May extract safe metadata; they cannot migrate, promote, normalize, or apply lifecycle states. |
## 5. Source Boundary
W-02 previous knowledge classification index is the primary extraction source. Raw `previusknowledge/` files remain local-only and were not deeply inspected.
Source paths, line groups, titles, classifications, and handling notes from W-02 may be retained as safe metadata. Missing or ambiguous W-02 references become blockers.
Each candidate preserves original W-02 classification and uncertainty; prior canonical labels remain historical only.
## 6. Extraction Scope
| In scope | Out of scope |
| --- | --- |
| W-02 `carry_forward` records and clearly equivalent W-02 carry-forward model entries | Raw source content extraction |
| Safe metadata, source reference, classification, target area, rationale, lifecycle, validation, blockers | Wholesale migration, source rewriting, conflicted normalization, archive execution |
| Future routing to validation, M-03, product, external, archive/lifecycle, or later migration | Product activation, external metadata migration, file movement, lifecycle execution |
## 7. Non-Carry-Forward Handling
| W-02 state | M-02 handling | Future owner | Blocked inference |
| --- | --- | --- | --- |
| `scope_limit` | Not extracted as root carry-forward; reference as product/scope blocker only. | Product governance later. | Root authority or product activation. |
| `migration_evidence` | Retain as historical context only. | Migration/audit later. | Current governing rule. |
| `conflicted` | Not extracted as carry-forward; route to M-03. | M-03/CSS controls. | Promotion before normalization. |
| `external_reference` | Not carry-forward by default; use as external context only. | External review/migration later. | Adoption, execution, dependency approval. |
| `superseded` | None found in W-02 count; historical only if later assigned. | A-later lifecycle handling. | Current authority. |
| unknown/unclassified | Classification blocker. | Classification/governance. | Any migration use. |
## 8. Carry-Forward Candidate Record Model
Conceptual fields: `candidate_id`, source reference, source classification, source status, safe title/label, previous-knowledge area, carry-forward rationale, normalized current topic, target AGENT PLATFORM area, lifecycle posture, validation posture, security/local-only posture, CSS/Graphify caveat if applicable, blockers, future ticket, retention posture, reviewer/date, and stop rule.
This is not a schema, registry, database, file format, API, script, or implementation.
## 9. Extraction Status Model
| Status | Meaning | Allowed use | Blocked use | Next action |
| --- | --- | --- | --- | --- |
| `carry_forward_candidate` | W-02 safe metadata extracted. | Planning evidence. | Authority/promotion. | Validate. |
| `carry_forward_ready_for_validation` | Source/status/security/lifecycle are sufficient for review. | V-03 review input. | Migration execution. | Citation/coherence review. |
| `carry_forward_blocked_pending_source_reference` | Source ref missing/ambiguous. | Blocker. | Use as candidate. | Resolve W-02 reference. |
| `carry_forward_blocked_pending_classification` | W-02 class absent/unclear. | Gap. | Migration use. | Classify. |
| `carry_forward_blocked_pending_security_review` | Sensitivity/local-only risk unclear. | Safe metadata only. | Exposure/publication. | Security review. |
| `carry_forward_blocked_pending_lifecycle_review` | Retention/lifecycle posture unclear. | Gap. | Lifecycle claim. | A-01/A-later review. |
| `carry_forward_blocked_pending_normalization` | Naming/scope/substrate conflict. | M-03 input. | Promotion. | Normalize later. |
| `carry_forward_deferred_to_M-03` | Conflicted semantic material detected. | M-03 planning. | Carry-forward extraction. | Explicit M-03 ticket. |
| `carry_forward_deferred_to_product` | Product/scope-limited. | Product planning. | Root authority. | Product governance. |
| `carry_forward_deferred_to_external_review` | External reference. | External review. | Adoption. | External ticket. |
| `carry_forward_rejected_for_current_scope` | Not usable for M-02 scope. | Historical trace. | Current claim. | Retain rationale. |
## 10. Lifecycle Posture Mapping
| Posture | Use for carry-forward candidates | A-01 boundary |
| --- | --- | --- |
| `retain_migration_context` | Default for W-02 carry-forward groups. | Retention reason only; no state applied to files. |
| `retain_historical_trace` | Prior rationale and source lineage. | Not current authority. |
| `retain_audit_evidence` | Candidate count, classification, blockers, route. | Evidence only. |
| `retain_safe_metadata_only` | Source paths/titles/classes without raw content. | No content copy. |
| `retain_local_only_reference` | `previusknowledge/` reference remains local-only. | No publication/Git approval. |
| `blocked_unknown` | Missing class/status/security/lifecycle. | No execution. |
| `incident_restricted` | Secret/credential/local-only leak risk. | Stop and secure handling. |
M-02 does not apply lifecycle state to actual source files.
## 11. Validation Posture Mapping
V-03 and V-01 proof targets for M-02: PL-1 for source/index metadata; PL-2 for classification/source status; PL-3 for citation/provenance review; PL-4 for future restatement/coherence review; PL-7 for future migration audit; PL-8 only for reproduced migration audit.
M-02 mostly reaches PL-1 to PL-3 because it extracts W-02 metadata and does not restate source claims. No proof level approves migration.
## 12. Security / Local-only Boundary
`previusknowledge/` remains local-only. M-02 retains safe metadata only and copies no raw previous knowledge content.
Secrets and credentials are never extracted or retained. Unknown sensitivity blocks extraction. Local-only evidence cannot be published by default. Incident conditions stop work.
## 13. CSS / Graphify Boundary
Graphify-related carry-forward candidates are candidate evidence only. `Cognitive Semantic System` is the accepted current name.
Graphify is not current authority; graph remains a candidate only; graph projections are evidence, not truth. Actual Graphify normalization is not executed in M-02.
`Platform Graphify`, `Graphify Authority`, and `Graphify owns truth` are rejected/prohibited historical examples only. Graphify conflicts or authority leakage defer to M-03/CSS controls.
## 14. Migration Boundary
M-02 extracts candidates only: no migration batch, file movement, content copying, source rewriting, archive execution, wholesale migration, or previous knowledge promotion.
M-03 handles conflicted semantic material later after explicit instruction.
## 15. Product Boundary
Product-scoped previous material is not root carry-forward unless W-02 classifies it as root-relevant `carry_forward` and the boundary is explicit.
W-02 product entries are `scope_limit`, so they are not extracted in M-02. Product material remains product-scoped/local-only; product source is not inspected; product activation is blocked.
## 16. External Source Boundary
`external_reference` material is not carry-forward by default. External material remains external evidence.
M-02 performs no external source adoption, copying, execution, package install, instruction adoption, or metadata migration. External candidates defer to external review/migration.
## 17. Git / Publication Boundary
Git state is evidence only. Staging is not migration; commit is not promotion; push is publication-like.
No `git add .`, staging, commit, push, or publication occurs in M-02. Local-only staged material would be a blocker.
## 18. Context Boundary
Extracted candidates may inform future context packs only if safe, scoped, cited, and labeled as carry-forward candidates.
Context inclusion is not promotion, migration, permission, validation approval, or lifecycle action. Local-only source content remains excluded by default.
## 19. Extraction Method
Method used: read W-02 classification index; identify entries classified `carry_forward`; retain only safe metadata from the index; group by architecture area; assign candidate IDs; assign target AGENT PLATFORM area; attach lifecycle, validation, security/local-only posture; identify blockers; prepare M-03/M-later routing; stop before content migration.
If W-02 lacks detail, record a blocker, do not inspect raw `previusknowledge/` deeply, and do not invent source claims.
## 20. Carry-Forward Extraction Table
W-02 reports 91 file-level `carry_forward` records out of 237 previous markdown files. M-02 extracts them as 7 grouped candidate records to stay compact and avoid source-content copying.
| candidate_id | source reference / safe label | W-02 class | target area | extraction rationale | lifecycle posture | validation posture | blocker / next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M02-CF-001 | W-02 Appendix A lines 351-360, adapter cluster, 10 paths | `carry_forward` | external-source boundary; validation/evidence | Preserve adapter mediation, security, governance, taxonomy, validation vocabulary. | retain_migration_context; safe metadata only | PL-2 now; PL-3 needed | Validate citations before restatement. |
| M02-CF-002 | W-02 Appendix A lines 363-392, agent cluster, 28 paths | `carry_forward` | harness/agents/context; security/access | Preserve agent role, boundary, autonomy, permission, memory, handoff, orchestration, taxonomy concepts. | retain_migration_context; local-only reference | PL-2 now; PL-3 needed | Restate later; no agent authority promotion. |
| M02-CF-003 | W-02 Appendix A lines 412-438, context cluster, 26 paths | `carry_forward` | harness/agents/context; archive/lifecycle | Preserve context selection, lifecycle, sensitivity, retrieval, taxonomy, validation, governance ideas. | retain_migration_context; audit evidence | PL-2 now; PL-3 needed | Future context/citation review. |
| M02-CF-004 | W-02 Appendix A lines 446 and 559-564, external/provider cluster, 7 paths | `carry_forward` | external-source boundary | Preserve external/provider neutrality and provider abstraction without adopting sources. | retain_safe_metadata_only | PL-2 now; PL-3 needed | Revalidate provider facts before use. |
| M02-CF-005 | W-02 Appendix A lines 396, 445, 514, 567, 570-574, runtime/workflow cluster, 9 paths | `carry_forward` | implementation-readiness later; migration | Preserve runtime/workflow posture while avoiding engine/code decisions. | retain_migration_context | PL-2 now; PL-4 later | Defer implementation readiness. |
| M02-CF-006 | W-02 Appendix A lines 439, 447, 499, 501, 510, 512, 513, 565, 568, 569, governance/workspace cluster, 10 paths | `carry_forward` | workspace/governance; validation/evidence | Preserve source-of-truth, ownership, modularity, platform principles, governance, scalability. | retain_historical_trace; retain_audit_evidence | PL-2/PL-3 candidate | Governance restatement later. |
| M02-CF-007 | W-02 Appendix A line 498, knowledge layer, 1 path | `carry_forward` | Cognitive Semantic System; migration | Preserve knowledge-boundary concepts without selecting substrate. | retain_migration_context | PL-2 now; PL-4 later | CSS/substrate neutrality review. |
## 21. Target Area Grouping
| Target area | M-02 grouping result |
| --- | --- |
| workspace/governance | M02-CF-006; source-of-truth, ownership, governance, platform principles. |
| security/access | Security/access concepts appear inside M02-CF-001, M02-CF-002, M02-CF-003, and M02-CF-006. |
| validation/evidence | Adapter/context validation and authority/evidence concepts appear in M02-CF-001, M02-CF-003, and M02-CF-006. |
| archive/lifecycle | Context lifecycle and source-of-truth carry-forward inform lifecycle review only; no state applied. |
| migration | All seven groups are migration-planning candidates only. |
| Cognitive Semantic System | M02-CF-007 plus authority concepts; prior Graphify-conflicted material is deferred to M-03. |
| harness/agents/context | M02-CF-002 and M02-CF-003; H-series keeps harness evidence bounded. |
| product boundary | No root carry-forward extracted; W-02 product material is `scope_limit`. |
| external-source boundary | M02-CF-004; external/provider ideas only, no adoption. |
| implementation-readiness later | M02-CF-005; runtime/workflow posture only. |
| unknown/deferred | Conflicted, external, product, migration_evidence, unknown, and future superseded material are not extracted as carry-forward. |
## 22. Blocker Register
| Blocker | Stop behavior | Required action | Blocks use? | Blocks migration? |
| --- | --- | --- | --- | --- |
| W-02 index missing | Stop extraction. | Restore/locate W-02. | Yes | Yes |
| no carry_forward entries found | Mark inconclusive. | Record search evidence. | Yes | Yes |
| source reference missing | Stop candidate. | Add safe W-02 reference. | Yes | Yes |
| classification ambiguous | Stop use. | Classify. | Yes | Yes |
| source status unknown | Stop promotion-quality claim. | Source-status review. | Yes | Yes |
| sensitivity unknown/local-only risk | Safe metadata only. | Security review. | Yes | Yes |
| secret/credential risk | Stop immediately. | Secure handling. | Yes | Yes |
| raw content required | Stop extraction. | Request explicit scope or reject. | Yes | Yes |
| Graphify authority leakage | Stop wording. | Defer to M-03/CSS. | Yes | Yes |
| product-root collapse | Stop root claim. | Product governance. | Yes | Yes |
| external adoption leakage | Stop adoption claim. | External review. | Yes | Yes |
| lifecycle posture missing | Block lifecycle claim. | A-01/A-later review. | Maybe | Yes |
| validation posture missing | Block readiness. | V-03 review. | Yes | Yes |
| governance path missing | Block promotion. | Governance path. | Yes | Yes |
| wholesale migration implied | Stop. | Narrow/restated ticket. | Yes | Yes |
| M-03 conflict detected | Defer. | Explicit M-03. | Yes | Yes |
## 23. Extraction Verdict Model
| Verdict | Meaning |
| --- | --- |
| `extraction_complete_for_index_scope` | All W-02 carry-forward metadata extracted for M-02 scope. |
| `extraction_complete_with_cautions` | Extracted, but future citation/security/lifecycle/governance review remains. |
| `extraction_blocked_by_missing_index` | W-02 absent. |
| `extraction_blocked_by_missing_classification` | W-02 class absent/unclear. |
| `extraction_blocked_by_security_risk` | Secret/credential/sensitive risk. |
| `extraction_blocked_by_local_only_risk` | Local-only exposure risk. |
| `extraction_blocked_by_raw_content_requirement` | Raw corpus content would be needed. |
| `extraction_blocked_by_governance_gap` | Decision path absent. |
| `extraction_inconclusive` | Evidence insufficient or conflicting. |
| `extraction_deferred` | Safe to postpone to M-03/product/external/archive later. |
Verdict is not migration approval.
## 24. Candidate Routing Model
| Route | Meaning |
| --- | --- |
| `ready_for_validation` | Future V-03 citation/source-status review. |
| `deferred_to_M-03` | Conflicted naming, scope, authority, or substrate normalization. |
| `deferred_to_product` | Product-scoped material and W-02 `scope_limit`. |
| `deferred_to_external_review` | External references and provider facts needing revalidation. |
| `deferred_to_archive_lifecycle` | Future A-later retention/supersession/deprecation handling. |
| `rejected_for_current_scope` | Historical trace only for M-02. |
| `blocked` | Required action before use. |
## 25. Evidence Retention Rules
Retain safe metadata: source reference, W-02 classification, candidate rationale, lifecycle posture, validation posture, blocker status, and future route.
Do not retain secrets, credentials, raw previous knowledge content, unsafe local-only content, raw product/external source, or generated-sensitive content without review.
## 26. Incident Handling
Incidents include secret/credential discovery, raw local-only content copied, wholesale previous knowledge migration, Graphify name promoted to current authority, graph selected by implication, product material promoted to root, external source treated as adopted, source copied from `previusknowledge/`, file movement attempted, Git staging attempted, or M-03/next ticket started.
Response: STOP, report safe metadata, do not continue adjacent work, and require human/security/governance decision.
## 27. M-02 Invariants
| ID | Invariant |
| --- | --- |
| M02-001 | Carry-forward extraction is not migration execution. |
| M02-002 | Carry-forward candidate is not current authority. |
| M02-003 | Safe metadata is preferred over source content. |
| M02-004 | Previous knowledge remains local-only. |
| M02-005 | Secrets and credentials are never extracted. |
| M02-006 | Graphify remains evidence, not authority. |
| M02-007 | Graph remains a candidate only. |
| M02-008 | Product material remains product-scoped. |
| M02-009 | External material remains external-source scoped. |
| M02-010 | Validation evaluates; governance decides. |
| M02-011 | Lifecycle states are not executed by M-02. |
| M02-012 | No wholesale migration. |
| M02-013 | Git state is evidence, not promotion. |
| M02-014 | Context exposure is not migration. |
| M02-015 | M-02 stops before M-03. |
## 28. Anti-patterns
Anti-patterns: extraction by copy-paste; raw file read; folder move; search-and-replace; old canonical label; carry-forward as authority; carry-forward as migration; carry-forward as publication; carry-forward as product activation; Graphify as current system name; graph as final substrate; external source as adopted dependency; generated output as source; lifecycle state as execution; Git commit as promotion; `git add .`; starting M-03 inside M-02.
## 29. Remaining Gaps
No migration executed; no migration batch; no raw source extraction; no conflicted normalization; no actual lifecycle state applied; no archive execution; no product activation; no external adoption; no implementation readiness; no validation registry implementation; no security/access enforcement; no final Cognitive Semantic System substrate decision; no M-03 started.
## 30. Readiness For M-03
M-03 - Conflicted Semantic Material Normalization is ready after explicit instruction if M-02 identifies conflicted/deferred candidates or W-02 already contains conflicted material, and if carry-forward, CSS-02, and V-03 boundaries remain preserved.
M-03 should normalize conflicted semantic material while still avoiding migration execution, file movement, raw local-only copying, product activation, external adoption, and substrate decision. Do not create M-03.
## 31. Final Verdict
| Question | Answer |
| --- | --- |
| What does M-02 extract? | Seven grouped carry-forward candidate records representing the 91 W-02 `carry_forward` file-level records. |
| Did M-02 inspect raw previusknowledge deeply? | No. |
| Did M-02 copy previous knowledge content? | No. Safe metadata only. |
| Did M-02 migrate material? | No. |
| Did M-02 apply lifecycle states? | No. |
| Did M-02 archive files? | No. |
| Did M-02 promote any candidate to current authority? | No. |
| What remains blocked? | Migration execution, raw content copying, lifecycle execution, archive execution, M-03, product activation, external adoption, implementation, publication, staging, commit, and push. |
| Is M-03 ready after explicit instruction? | Yes, as a future normalization-planning task only. |
Final M-02 statement:
```text
M-02 extracts W-02 carry-forward safe metadata into candidate records and stops.
It does not copy, migrate, normalize, promote, archive, publish, or start M-03.
```
