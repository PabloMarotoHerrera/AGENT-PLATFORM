# M-03 - Conflicted Semantic Material Normalization
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Conflicted Semantic Material Normalization |
| Ticket | M-03 |
| Status | Accepted conflicted semantic normalization |
| Date | 2026-07-01 |
| Scope | Controlled normalization-planning records for W-02 `conflicted` previous-knowledge metadata |
| Authority | Normalization planning only, not migration execution, promotion, raw-file normalization, archive execution, lifecycle action, product activation, external adoption, implementation, staging, commit, push, publication, or M-04 start |
| Related documents | M-02, A-00, A-01, V-03, CSS-02, W-02, W-08, S-series |
## 2. Purpose
M-03 follows M-02. M-02 extracted W-02 `carry_forward` candidates as safe metadata. M-03 normalizes conflicted semantic material from approved classification metadata into planning records.
M-03 does not migrate, copy, move, rewrite, archive, normalize raw files, normalize actual Graphify files, or promote previous knowledge. M-03 prepares M-04 - Agent / Context / Runtime / Provider / Adapter Migration, but does not start M-04.
## 3. Conflicted Semantic Material Definition
Conflicted semantic material is previous-knowledge metadata, labels, claims, patterns, or references whose meaning conflicts with current AGENT PLATFORM naming, authority, governance, substrate neutrality, product boundaries, external-source posture, validation posture, security posture, or lifecycle policy.
Conflict is not rejection by default, deletion, migration approval, or current authority. Conflict requires classification, restatement, citation, validation, lifecycle review, security review, and governance before use.
## 4. Normalization Authority Boundary
| Layer | M-03 boundary |
| --- | --- |
| Governance | Decides acceptance, promotion, migration, lifecycle, publication, and exceptions. |
| Validation | Evaluates normalization readiness; V-03 controls migration validation posture. |
| Evidence | Supports candidate normalization through source reference, classification, limits, and blockers. |
| Security | Constrains local-only, secret, credential, product, external, generated, and sensitive handling. |
| A-00/A-01 | Define lifecycle posture without executing lifecycle states. |
| V-03 | Defines migration validation and proof targets for conflicted normalization. |
| CSS-02 | Defines Graphify normalization boundaries and substrate neutrality. |
| Agents | May extract safe metadata and propose normalized wording; they cannot migrate, promote, or apply lifecycle states. |
## 5. Source Boundary
W-02 previous knowledge classification index is the primary source. M-02 carry-forward extraction is contextual input.
Raw `previusknowledge/` files remain local-only and were not deeply inspected. W-02 source paths, titles, line groups, classifications, and handling notes may be retained as safe metadata. Missing or ambiguous W-02 source references become blockers. Conflicted candidates preserve original classification and uncertainty.
## 6. Normalization Scope
| In scope | Out of scope |
| --- | --- |
| W-02 `conflicted` records, safe metadata, source reference, source classification, conflict type, normalized topic, target area, lifecycle posture, validation posture, blocker status, future route | Raw source content extraction, wholesale migration, actual file normalization, product activation, external metadata migration, actual supersession/deprecation/retention, file movement, archive execution |
## 7. Conflict Class Catalog
| Conflict class | Meaning | Normalized handling | Blocked inference | Required evidence | Future route |
| --- | --- | --- | --- | --- | --- |
| `naming_conflict` | Old or ambiguous name conflicts with current vocabulary. | Restate under current AGENT PLATFORM terms. | Current name. | W-02 class + CSS-02 naming rule. | validation/CSS. |
| `Graphify_authority_leakage` | Historical Graphify label implies authority. | Treat as historical evidence only. | Graphify authority. | W-02 + CSS-02 caveat. | M-03/CSS. |
| `graph_as_truth_conflict` | Graph or projection implies truth ownership. | Evidence, not authority. | Truth by graph/projection. | V-02/V-03 evidence status. | validation. |
| `substrate_assumption_conflict` | Graph or any substrate implied final. | Candidate only; alternatives open. | Final substrate. | CSS-02/CSS-A substrate posture. | substrate decision later. |
| `product_root_collapse` | Product-scoped need becomes root architecture. | Keep product-scoped. | Root authority/activation. | W-02/W-12/V-04 posture. | product governance. |
| `external_adoption_leakage` | External source/tool treated as adopted. | External evidence only. | Dependency/use/execution. | W-13/V-05 posture. | external review. |
| `old_canonical_label_conflict` | Prior `canonical` status treated current. | Historical prior status only. | Current authority. | W-02 + W-09 status. | governance review. |
| `governance_authority_conflict` | Evidence, agent, validation, or Git implies approval. | Governance decides. | Approval/promotion. | W-11 posture. | governance. |
| `validation_approval_conflict` | Proof/checks imply approval. | Validation evaluates only. | Governance approval. | V-01/V-03 proof limits. | validation. |
| `evidence_truth_conflict` | Evidence treated as truth. | Evidence supports claims only. | Truth/source. | V-02 evidence status. | validation. |
| `context_permission_conflict` | Context inclusion implies permission. | Context is selected exposure. | Edit/execute/read permission. | W-05/S-series. | context/security. |
| `Git_truth_conflict` | Git state implies truth or promotion. | Git is artifact evidence. | Semantic truth/promotion. | W-11/S-04 Git posture. | Git governance. |
| `generated_output_source_conflict` | Generated output/projection treated as source. | Generated evidence/projection only. | Source authority. | V-02/S-03 provenance. | evidence review. |
| `lifecycle_execution_conflict` | Lifecycle wording implies state applied. | Candidate posture only. | Supersession/archive execution. | A-00/A-01 posture. | archive/lifecycle later. |
| `security_local_only_conflict` | Local-only/sensitive handling unclear. | Safe metadata only; escalate. | Publication/commit/copy. | S-series sensitivity. | security review. |
| `unknown_or_ambiguous_conflict` | Conflict cannot be classified safely. | Block pending classification. | Any use. | Source/status metadata. | blocked. |
## 8. Non-Conflicted Handling
| W-02 state | M-03 handling | Allowed reference | Future owner | Blocked inference |
| --- | --- | --- | --- | --- |
| `carry_forward` | Already handled by M-02; not normalized as conflict by default. | Context only. | M-02/V-03. | Current authority or migration. |
| `scope_limit` | Product/scope material; conflict only if W-02 marks conflict. | Product blocker. | Product governance. | Root authority/product activation. |
| `migration_evidence` | Historical context only. | Rationale trace. | Migration/audit. | Current governing rule. |
| `external_reference` | External evidence; conflict only if adoption/naming leaks. | External blocker. | External review/migration. | Adoption/execution/dependency approval. |
| `superseded` | None assigned in W-02; historical only if later assigned. | Lifecycle trace. | A-later lifecycle. | Current authority. |
| unknown/unclassified | Classification blocker. | Gap only. | Classification/governance. | Any migration use. |
## 9. Normalization Candidate Record Model
Conceptual fields: `candidate_id`, source reference, source classification, source status, safe title/label, conflict class, old/ambiguous wording or posture, normalized current wording, target AGENT PLATFORM area, lifecycle posture, validation posture, security/local-only posture, CSS/Graphify caveat if applicable, blockers, future ticket, retention posture, reviewer/date, and stop rule.
This is not a schema, registry, database, file format, API, script, or implementation.
## 10. Normalization Status Model
| Status | Meaning | Allowed use | Blocked use | Next action |
| --- | --- | --- | --- | --- |
| `conflicted_candidate` | W-02 conflicted metadata captured. | Planning evidence. | Authority/promotion. | Normalize wording. |
| `normalization_ready_for_validation` | Source/status/boundaries sufficient for review. | V-03 review input. | Migration execution. | Citation/coherence review. |
| `normalization_blocked_pending_source_reference` | Source ref missing/ambiguous. | Blocker. | Use as candidate. | Resolve W-02 reference. |
| `normalization_blocked_pending_classification` | W-02 class absent/unclear. | Gap. | Migration use. | Classify. |
| `normalization_blocked_pending_security_review` | Sensitivity/local-only risk unclear. | Safe metadata only. | Exposure/publication. | Security review. |
| `normalization_blocked_pending_lifecycle_review` | Retention/lifecycle posture unclear. | Gap. | Lifecycle claim. | A-01/A-later review. |
| `normalization_blocked_pending_citation` | Provenance insufficient. | Gap. | Promotion-quality use. | Add citations later. |
| `normalization_blocked_pending_governance` | Decision path absent. | Proposal only. | Promotion. | Governance path. |
| `normalization_deferred_to_product` | Product scope controls. | Product planning. | Root authority. | Product governance. |
| `normalization_deferred_to_external_review` | External posture controls. | External review. | Adoption. | External ticket. |
| `normalization_deferred_to_substrate_decision` | Substrate choice pressure exists. | Candidate evidence. | Final substrate. | Future CSS decision. |
| `normalization_rejected_for_current_scope` | Not usable in M-03 scope. | Historical trace. | Current claim. | Retain rationale. |
## 11. Lifecycle Posture Mapping
| Posture | M-03 use | A-01 boundary |
| --- | --- | --- |
| `retain_migration_context` | Default for conflicted candidates. | Retention reason only; no state applied. |
| `retain_historical_trace` | Prior labels/claims retained as history. | Not current authority. |
| `retain_audit_evidence` | Counts, classifications, blockers, and routes. | Evidence only. |
| `retain_safe_metadata_only` | Path/title/class/status without raw content. | No content copy. |
| `retain_local_only_reference` | `previusknowledge/` reference remains local-only. | No publication/Git approval. |
| `blocked_unknown` | Missing status/security/lifecycle. | No execution. |
| `incident_restricted` | Secret/credential/local-only leak risk. | Stop and secure handling. |
M-03 does not apply lifecycle state to actual source files.
## 12. Validation Posture Mapping
V-03/V-01 proof targets: PL-1 for source/index metadata; PL-2 for classification/source status; PL-3 for citation/provenance review; PL-4 for normalization/coherence review; PL-7 for future migration audit; PL-8 only for reproduced migration audit.
M-03 may reach PL-1 to PL-3 using W-02 metadata and may define a PL-4 target for later review. No proof level approves migration.
## 13. Security / Local-only Boundary
`previusknowledge/` remains local-only. M-03 uses safe metadata only and copies no raw previous knowledge content.
Secrets and credentials are never extracted or retained. Unknown sensitivity blocks normalization. Local-only evidence cannot be published by default. Incident conditions stop work.
## 14. CSS / Graphify Boundary
Graphify-related conflicted candidates are historical or candidate evidence only. Graphify is not current authority. `Cognitive Semantic System` is the accepted current name.
Graph remains a candidate only. Graph projections are evidence, not truth. Actual Graphify file normalization is not executed in M-03. Prohibited Graphify authority wording must be marked rejected/prohibited/historical. Substrate decisions defer to future governed decision.
## 15. Naming Normalization Rules
Old names do not become current names. Product-derived names and external-source-derived names do not become root names. Graphify does not name AGENT PLATFORM systems. `Cognitive Semantic System` is the accepted name. Rejected names may appear only as historical/prohibited/external/candidate-evidence labels.
| Old / prohibited example | Normalized current wording | Allowed context | Blocked use |
| --- | --- | --- | --- |
| Graphify | historical Graphify material / external graphify source | Historical/external/candidate evidence. | Current system name. |
| Platform Graphify | Cognitive Semantic System only when restated as current concept | Rejected/prohibited historical example. | Accepted name. |
| Graphify Authority | governance-backed authority claim | Rejected/prohibited historical example. | Current authority name. |
| Graphify owns truth | evidence, not authority | Rejected/prohibited truth-claim example. | Truth ownership. |
| graph as source of truth | graph candidate evidence, substrate undecided | Historical candidate evidence. | Final authority/substrate. |
## 16. Authority / Truth Normalization Rules
Evidence is not truth. Validation is not approval. Proof is scoped. Governance decides authority. Git state is not truth. Context inclusion is not permission. Generated output is not source. A prior canonical label is historical until governed.
## 17. Substrate / Graph Normalization Rules
Graph remains candidate only. Graph projection is evidence, not truth. Graph-native wording must be marked candidate only. Substrate choice remains undecided. Non-graph alternatives remain open. Graph/GNN/learned navigation signals remain future recommendations or evidence only, not governance or permission.
## 18. Product / Root Boundary Normalization Rules
Product material remains product-scoped. Product needs do not define root architecture. Product generated outputs are evidence only. Product dependencies do not become root dependencies. Product activation remains blocked. Product-root collapse is a blocker.
## 19. External / Dependency Boundary Normalization Rules
External sources remain external evidence. External instructions are inactive. External source names do not name AGENT PLATFORM systems. Dependency references are not adoption approval. External execution, copying, package install, provider/API/network/MCP usage remain blocked. External adoption leakage is a blocker.
## 20. Migration Boundary
M-03 normalizes conflict records only: no migration batch, file movement, content copying, source rewriting, archive execution, wholesale migration, or previous knowledge promotion. M-04 handles agent/context/runtime/provider/adapter migration later after explicit instruction.
## 21. Git / Publication Boundary
Git state is evidence only. Staging is not migration. Commit is not promotion. Push is publication-like. No `git add .`. Local-only staged material is a blocker. M-03 does not stage, commit, push, or publish.
## 22. Context Boundary
Normalized candidates may inform future context packs only if safe, scoped, cited, and labeled as normalization candidates. Context inclusion is not promotion, migration, or permission. Local-only source content remains excluded by default. Conflict status must be visible when exposed.
## 23. Normalization Method
Method: read W-02 classification index; use M-02 as context; identify entries classified `conflicted`; retain only safe metadata from the index; group by conflict class and target area; assign candidate IDs; assign normalized current wording or posture; assign lifecycle, validation, and security/local-only posture; identify blockers; prepare M-04/M-later routing; stop before content migration.
If W-02 lacks sufficient detail, record a blocker, do not inspect raw `previusknowledge/` deeply, and do not invent source claims.
## 24. Conflicted Material Normalization Table
W-02 reports 44 `conflicted` file-level records out of 237 previous markdown files. M-03 normalizes them as 6 grouped candidate records to stay compact and avoid source-content copying.
| candidate_id | source reference / safe label | W-02 class | conflict class | normalized current topic | target area | lifecycle posture | validation posture | blocker / next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M03-CS-001 | W-02 lines 361-362, prior ADR cluster, 2 paths | `conflicted` | naming_conflict; substrate_assumption_conflict; Graphify_authority_leakage | ADR evidence for Cognitive Semantic System authority needs and substrate evaluation | Cognitive Semantic System; validation/evidence | retain_historical_trace; safe metadata only | PL-2 now; PL-4 later | Rewrite only through governed ADR/review. |
| M03-CS-002 | W-02 lines 450, 462, 478, 482, 487, semantic authority/vocabulary cluster, 5 paths | `conflicted` | naming_conflict; governance_authority_conflict; evidence_truth_conflict | Semantic authority concepts restated as governance-backed Cognitive Semantic System candidates | workspace/governance; Cognitive Semantic System | retain_migration_context | PL-2 now; PL-3/PL-4 later | Neutralize old name and authority leakage. |
| M03-CS-003 | W-02 lines 454, 456, 466-468, 470, substrate/ontology/relationship cluster, 6 paths | `conflicted` | substrate_assumption_conflict; graph_as_truth_conflict | Graph, ontology, metamodel, node, and relationship material as candidate substrate evidence only | Cognitive Semantic System; unknown/deferred | retain_migration_context | PL-2 now; PL-4 later | Defer final substrate decision. |
| M03-CS-004 | W-02 lines 455, 459, 463, 475-477, 480, 486, schema/storage/lifecycle cluster, 8 paths | `conflicted` | lifecycle_execution_conflict; validation_approval_conflict; generated_output_source_conflict | Schema, storage, lifecycle, import/export, and validation ideas as non-implemented planning evidence | archive/lifecycle; validation/evidence; implementation-readiness later | retain_audit_evidence | PL-2 now; PL-4 later | No schema/registry/storage commitment. |
| M03-CS-005 | W-02 lines 449, 453, 460-461, 469, 472-474, 481, 485, API/projection/repository/runtime cluster, 10 paths | `conflicted` | context_permission_conflict; Git_truth_conflict; external_adoption_leakage | Projection, repository, API, integration, runtime, and engine ideas as bounded evidence, not execution or truth | migration; harness/agents/context; implementation-readiness later | retain_migration_context | PL-2 now; PL-4 later | Defer M-04; no API/runtime implementation. |
| M03-CS-006 | W-02 lines 377, 448, 451-452, 457-458, 464-465, 471, 479, 483-484, 488, representation cluster, 13 paths | `conflicted` | naming_conflict; Graphify_authority_leakage; context_permission_conflict | Agent, command, dependency, adapter, hook, MCP, memory, repository, skill, ticket, tool, and workflow representations as neutral migration candidates | harness/agents/context; external-source boundary; M-04 | retain_migration_context; local-only reference | PL-2 now; PL-3/PL-4 later | Route to M-04 after validation; no tooling/permission adoption. |
## 25. Target Area Grouping
| Target area | M-03 grouping result |
| --- | --- |
| workspace/governance | M03-CS-002; authority, governance, and source-of-truth language normalized. |
| security/access | M03-CS-006 and all groups retain local-only/security blockers. |
| validation/evidence | M03-CS-001, M03-CS-002, M03-CS-004, M03-CS-005; evidence/proof boundaries. |
| archive/lifecycle | M03-CS-004; lifecycle/schema ideas remain candidate posture only. |
| migration | All six groups are migration-planning candidates only. |
| Cognitive Semantic System | M03-CS-001 to M03-CS-004; current name and substrate neutrality preserved. |
| harness/agents/context | M03-CS-005 and M03-CS-006; M-04-relevant but not started. |
| product boundary | No conflicted product-root promotion; product Graphify material remains `scope_limit`. |
| external-source boundary | External adoption leakage blocked; external source names do not name systems. |
| implementation-readiness later | M03-CS-004 and M03-CS-005; no code/schema/API/runtime implementation. |
| unknown/deferred | Substrate decision and ambiguous conflict resolution deferred. |
## 26. Blocker Register
| Blocker | Stop behavior | Required action | Blocks use? | Blocks migration? |
| --- | --- | --- | --- | --- |
| W-02 index missing | Stop normalization. | Restore/locate W-02. | Yes | Yes |
| no conflicted entries found | Mark inconclusive. | Record search evidence. | Yes | Yes |
| source reference missing | Stop candidate. | Add safe reference. | Yes | Yes |
| classification ambiguous | Stop use. | Classify. | Yes | Yes |
| source status unknown | Stop promotion-quality claim. | Source-status review. | Yes | Yes |
| sensitivity unknown | Safe metadata only. | Security review. | Yes | Yes |
| local-only risk | Stop exposure. | Preserve local-only posture. | Yes | Yes |
| secret/credential risk | Stop immediately. | Secure handling. | Yes | Yes |
| raw content required | Stop extraction. | Request scope or reject. | Yes | Yes |
| Graphify authority leakage | Stop wording. | Mark historical/prohibited and restate. | Yes | Yes |
| old naming treated as current | Stop wording. | Use current vocabulary. | Yes | Yes |
| graph treated as final substrate | Stop claim. | Restore candidate wording. | Yes | Yes |
| graph projection treated as truth | Stop claim. | Mark generated/evidence. | Yes | Yes |
| product-root collapse | Stop root claim. | Product governance. | Yes | Yes |
| external adoption leakage | Stop adoption claim. | External review. | Yes | Yes |
| lifecycle posture missing | Block lifecycle claim. | A-01/A-later review. | Maybe | Yes |
| validation posture missing | Block readiness. | V-03 review. | Yes | Yes |
| governance path missing | Block promotion. | Governance path. | Yes | Yes |
| wholesale migration implied | Stop. | Narrow/restated ticket. | Yes | Yes |
| M-04 scope pressure detected | Stop. | Wait explicit M-04. | Yes | Yes |
## 27. Normalization Verdict Model
| Verdict | Meaning |
| --- | --- |
| `normalization_complete_for_index_scope` | All W-02 conflicted metadata normalized for M-03 scope. |
| `normalization_complete_with_cautions` | Normalized, but future citation/security/lifecycle/governance review remains. |
| `normalization_blocked_by_missing_index` | W-02 absent. |
| `normalization_blocked_by_missing_classification` | Classification absent/unclear. |
| `normalization_blocked_by_security_risk` | Secret/credential/sensitive risk. |
| `normalization_blocked_by_local_only_risk` | Local-only exposure risk. |
| `normalization_blocked_by_raw_content_requirement` | Raw corpus content would be needed. |
| `normalization_blocked_by_governance_gap` | Decision path absent. |
| `normalization_inconclusive` | Evidence insufficient or conflicting. |
| `normalization_deferred` | Safe to postpone to M-04/product/external/archive/substrate decision later. |
Verdict is not migration approval.
## 28. Candidate Routing Model
| Route | Meaning |
| --- | --- |
| `ready_for_validation` | Future V-03 citation/source-status/coherence review. |
| `deferred_to_M-04` | Agent/context/runtime/provider/adapter migration planning. |
| `deferred_to_product` | Product-scoped material and `scope_limit`. |
| `deferred_to_external_review` | External evidence and provider/tool facts. |
| `deferred_to_substrate_decision` | Graph/substrate/representation choice. |
| `deferred_to_archive_lifecycle` | Future A-later retention/supersession/deprecation handling. |
| `rejected_for_current_scope` | Historical trace only for M-03. |
| `blocked` | Required action before use. |
## 29. Evidence Retention Rules
Retain safe metadata: source reference, W-02 classification, conflict class, normalized wording/posture, lifecycle posture, validation posture, blocker status, and future route.
Do not retain secrets, credentials, raw previous knowledge content, unsafe local-only content, raw product/external source, or generated-sensitive content without review.
## 30. Incident Handling
Incidents include secret/credential discovery, raw local-only content copied, wholesale previous knowledge migration, Graphify name promoted to current authority, graph selected by implication, graph projection treated as truth, product material promoted to root, external source treated as adopted, source copied from `previusknowledge/`, file movement attempted, Git staging attempted, or M-04/next ticket started.
Response: STOP, report safe metadata, do not continue adjacent work, and require human/security/governance decision.
## 31. M-03 Invariants
| ID | Invariant |
| --- | --- |
| M03-001 | Conflicted normalization is not migration execution. |
| M03-002 | Normalized candidate is not current authority. |
| M03-003 | Safe metadata is preferred over source content. |
| M03-004 | Previous knowledge remains local-only. |
| M03-005 | Secrets and credentials are never extracted. |
| M03-006 | Graphify remains evidence, not authority. |
| M03-007 | Graph remains a candidate only. |
| M03-008 | Product material remains product-scoped. |
| M03-009 | External material remains external-source scoped. |
| M03-010 | Validation evaluates; governance decides. |
| M03-011 | Lifecycle states are not executed by M-03. |
| M03-012 | No wholesale migration. |
| M03-013 | Git state is evidence, not promotion. |
| M03-014 | Context exposure is not migration. |
| M03-015 | M-03 stops before M-04. |
## 32. Anti-patterns
Anti-patterns: normalization by copy-paste; normalization by raw file read; normalization by folder move; normalization by search-and-replace only; normalization by old canonical label; normalization as authority; normalization as migration; normalization as publication; normalization as product activation; Graphify as current system name; graph as final substrate; graph projection as truth; external source as adopted dependency; generated output as source; lifecycle state as execution; Git commit as promotion; `git add .`; starting M-04 inside M-03.
## 33. Remaining Gaps
No migration executed; no migration batch; no raw source extraction; no actual source file normalization; no actual lifecycle state applied; no archive execution; no product activation; no external adoption; no implementation readiness; no validation registry implementation; no security/access enforcement; no final Cognitive Semantic System substrate decision; no M-04 started.
## 34. Readiness For M-04
M-04 - Agent / Context / Runtime / Provider / Adapter Migration is ready after explicit instruction if M-03 identifies agent/context/runtime/provider/adapter candidates or W-02 already contains such material, and if conflicted normalization, M-02 carry-forward, CSS-02 Graphify normalization, V-03 migration validation, and H-series harness boundaries remain preserved.
M-04 should classify and plan migration posture for agent, context, runtime, provider, and adapter material while still avoiding implementation, execution, dependency adoption, provider/API/MCP activation, raw local-only copying, product activation, external adoption, and substrate decision. Do not create M-04.
## 35. Final Verdict
| Question | Answer |
| --- | --- |
| What does M-03 normalize? | Six grouped normalization candidate records representing the 44 W-02 `conflicted` file-level records. |
| Did M-03 inspect raw previusknowledge deeply? | No. |
| Did M-03 copy previous knowledge content? | No. Safe metadata only. |
| Did M-03 migrate material? | No. |
| Did M-03 normalize actual files? | No. |
| Did M-03 apply lifecycle states? | No. |
| Did M-03 archive files? | No. |
| Did M-03 promote any candidate to current authority? | No. |
| What remains blocked? | Migration execution, raw content copying, source-file normalization, lifecycle execution, archive execution, M-04, product activation, external adoption, implementation, publication, staging, commit, and push. |
| Is M-04 ready after explicit instruction? | Yes, as a future migration-planning task only. |
Final M-03 statement:
```text
M-03 normalizes W-02 conflicted safe metadata into candidate records and stops.
It does not copy, migrate, normalize actual files, promote, archive, publish, or start M-04.
```
