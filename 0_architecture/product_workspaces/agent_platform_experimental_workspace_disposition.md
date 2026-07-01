# P-07 - Experimental Workspace Disposition
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Experimental Workspace Disposition |
| Ticket | P-07 |
| Product candidate | `experimental` |
| Status | Accepted experimental workspace disposition |
| Date | 2026-07-01 |
| Scope | Disposition review for the ambiguous `experimental` workspace candidate after P-02 through P-06 inactive charter drafts. |
| Authority | Disposition planning only, not product activation or archive execution. |
| Related documents | P-00, P-01, P-02 through P-06, M-A, M-07, M-06, M-08, W-12, V-04, W-13, V-05, S-series, CSS-series, H-series, Siamese Product Vision |

## 2. Purpose
P-00 selected `experimental` for disposition review, not product charter drafting. P-01 defined the common product gate. P-02 through P-06 drafted inactive charters for `omniverse-app`, `backend-energyplus`, `cli`, `desktop`, and `web-platform`.

P-07 decides the current disposition posture for `experimental`: blocked local-only sandbox pending future split or archive review. P-07 does not activate `experimental`, convert it into a charter by default, inspect source deeply, move/split/archive files, change product Git posture, adopt dependencies, create validation baselines, create implementation artifacts, create P-08, or start P-08.

## 3. Experimental Workspace Disposition Definition
Disposition is a governed planning decision that classifies an ambiguous product workspace candidate into a safe future route such as blocked sandbox, split review, deferred review, archive-candidate review, reject-for-current-phase, or future-charter candidate after evidence.

Disposition is not activation, charter acceptance, archive execution, file split, deletion, source tracking, source movement, implementation readiness, dependency adoption, or publication.

## 4. Product Candidate Summary
| Field | Value |
| --- | --- |
| product_id | PROD-004 / P00-SEL-006 |
| product_name | `experimental` |
| product_platform_name | Siamese |
| product_status | experimental/blocked/local_only/inactive |
| selection_source | P-00 |
| charter_template_source | P-01 |
| prior posture | selected_for_disposition_review |
| likely area | prototype/sandbox/ambiguous product material |
| main risk | unclear scope, root leakage, dependency ambiguity, local-only exposure, Git posture, activation by proximity |
| current disposition | blocked_local_only_sandbox_pending_future_split_or_archive_review |
| blocked inference | product activation, product charter, roadmap priority, source tracking, archive execution, implementation readiness |

## 5. Disposition Decision
`experimental` remains a blocked local-only sandbox and is not selected for product charter drafting in the current phase.

Recommended disposition: retain safe metadata only; keep inactive; keep local-only; do not inspect source deeply; do not track product source; do not activate; do not archive now; do not split now; route future useful material to exact scoped split review; route obsolete or unsafe material to future archive-candidate review under M-08/A-series; reject `experimental` as a current product charter candidate.

## 6. Rationale
`experimental` has no accepted owner, final purpose, final scope, product/root boundary, validation baseline, dependency posture, Git posture, classification of internal material, security review, archive eligibility review, or implementation readiness assessment.

It could mix prototypes, generated outputs, product remnants, external ideas, scratch work, dependency manifests, local data, or obsolete material. Converting it to a product charter by proximity would violate P-00/P-01 and could leak ambiguous material into AGENT PLATFORM root architecture or Siamese product architecture.

## 7. Disposition Status Model
| Status | Meaning |
| --- | --- |
| blocked_local_only_sandbox | Current safe posture: inactive, untracked, local-only, and blocked. |
| selected_for_split_review_later | Future exact scoped review may split useful material. |
| deferred_pending_owner | Owner missing blocks use. |
| deferred_pending_scope | Scope missing blocks use. |
| deferred_pending_classification | Internal material class unknown. |
| deferred_pending_security_review | Sensitivity or access posture unknown. |
| archive_candidate_later | Future metadata posture for possible M-08/A-series review. |
| reject_for_current_phase | Not a current product charter route. |
| future_charter_candidate_after_split | Possible only after split evidence shows a distinct product candidate. |
| incident_restricted | Stop state for secret, credential, local-only, or unsafe exposure risk. |

No status means active product, source tracking approval, archive execution, file movement, dependency adoption, or implementation readiness.

## 8. Disposition Route Table
| route | meaning | allowed future use | blocked use | required evidence |
| --- | --- | --- | --- | --- |
| retain_blocked_sandbox_metadata | Keep safe metadata only. | Disposition trace. | Source use, activation. | P-00/W-12/V-04 status. |
| split_review_later | Exact scoped review may isolate useful material. | Future split packet. | Splitting now. | Class, owner, scope, sensitivity. |
| defer_pending_classification | Wait for evidence before route. | Gap tracking. | Chartering by proximity. | Source class and risk metadata. |
| archive_candidate_later | Possible lifecycle review later. | Metadata-only candidate. | Archive execution now. | M-08/A-series exact scope. |
| reject_for_current_phase | Not current charter candidate. | Preserve rationale. | Roadmap priority claim. | Owner/scope gaps. |
| future_charter_candidate_after_split | New candidate only after split. | Future P-style charter path. | Direct experimental charter. | Product fit and isolated scope. |
| incident_restricted | Unsafe exposure suspected. | Safe blocker report. | Continued inspection/use. | Security review. |

## 9. Product / Root Boundary
`experimental` cannot define AGENT PLATFORM root authority, Siamese product architecture by proximity, the Cognitive Semantic System, backend behavior, Omniverse behavior, CLI behavior, desktop behavior, or web-platform behavior.

Experimental material may inform future proposals only after exact scoped review. Product decisions remain product-scoped unless governed otherwise. Graph remains a candidate only.

## 10. Relationship To Existing Product Charters
| product area | existing charter | experimental relationship | blocked inference |
| --- | --- | --- | --- |
| omniverse-app | P-02 | Separate inactive product charter. | No merge, override, SDK approval, or activation. |
| backend-energyplus | P-03 | Separate backend/domain charter. | No backend ownership or energy logic claim. |
| cli | P-04 | Separate operator/scriptable interface charter. | No shell/command permission. |
| desktop | P-05 | Separate local desktop/interface charter. | No desktop runtime or packaging approval. |
| web-platform | P-06 | Separate browser/deployed interface charter. | No web/auth/deploy approval. |

`experimental` does not override, merge, extend, or activate any existing charter.

## 11. Current Local-only Posture
`experimental` source, if present under `2_products/`, remains local-only and ignored. P-07 does not inspect product source. P-07 uses safe metadata only.

Local sessions, configs, generated outputs, logs, credentials, dependency folders, build outputs, caches, reports, prototypes, and product artifacts remain excluded unless governed later.

## 12. Security / Access Posture
`experimental` may contain sensitive or ambiguous material. Unknown sensitivity blocks use. Secrets, credentials, tokens, provider auth, package registry auth, local sessions, telemetry configs, API keys, cloud auth, local paths, and environment variables are excluded.

No provider/API/MCP/network/auth activation occurs. No source content is exposed. Publication is blocked by default.

## 13. Dependency / External Source Posture
Dependency posture is unknown. External-source posture is unknown. Package/runtime posture is unknown. External source presence is not adoption. Dependency references are not dependency approval. Product-specific dependency adoption would not become root dependency adoption.

P-09 handles dependency/external posture later, not P-07.

## 14. Archive / Lifecycle Posture
Using M-08/A-series: P-07 does not archive `experimental`, create `_archive/`, move, copy, delete, rename, transform, or apply lifecycle states to actual files.

P-07 may mark `experimental` as `archive_candidate_later` only as metadata posture. Archive execution and deletion require future exact-scope governance.

## 15. Generated Output / Data / Model / Artifact Posture
Experimental outputs, logs, prototypes, reports, screenshots, datasets, models, generated docs, build artifacts, and local experiments are generated-sensitive by default.

Generated output is evidence, not source by default. Raw output remains local-only until reviewed. Publication requires product, security, validation, dependency, and governance review.

## 16. Git Posture
Product Git posture is not changed by P-07. `2_products/` remains ignored/local-only. `experimental` source tracking is not approved. Product Git posture decision is deferred to P-08.

P-07 does not stage, commit, push, force-add, move, split, publish, or use `git add .`. Future Git action must use exact paths only.

## 17. Validation Baseline Needs
Future baseline needs under V-04/P-01: disposition completeness checks, local-only checks, classification checks, owner/scope checks, product/root boundary checks, security/access checks, generated-output checks, dependency/external posture checks, archive/lifecycle eligibility checks, split-review checks, and reject/defer/archive-candidate evidence checks.

P-07 does not create or execute validation baselines. P-10 handles Product Validation Baseline.

## 18. Disposition Blockers
| blocker | reason | required future action | blocks charter? | blocks activation? | blocks Git tracking? |
| --- | --- | --- | --- | --- | --- |
| owner missing | No accountable owner. | Assign owner. | Yes | Yes | Yes |
| purpose missing | No accepted reason. | Define purpose. | Yes | Yes | Yes |
| scope missing | No safe boundary. | Define scope/non-goals. | Yes | Yes | Yes |
| product/root boundary missing | Root leakage risk. | Boundary review. | Yes | Yes | Yes |
| classification missing | Internal material unknown. | Exact classification. | Yes | Yes | Yes |
| source sensitivity unknown | Exposure risk. | Security review. | Yes | Yes | Yes |
| generated-output posture unknown | Output may be sensitive. | Output review. | Yes | Yes | Maybe |
| dependency posture unknown | Adoption risk. | P-09 review. | Yes | Yes | Yes |
| external-source posture unknown | Reuse risk. | External review. | Yes | Yes | Yes |
| Git posture deferred to P-08 | Tracking not approved. | P-08 decision. | Maybe | Yes | Yes |
| validation baseline deferred to P-10 | Baseline absent. | P-10 baseline. | Yes | Yes | Maybe |
| security/access review missing | Unsafe exposure possible. | Security review. | Yes | Yes | Yes |
| archive eligibility unknown | Lifecycle route unclear. | M-08/A-series review. | Maybe | Yes | Maybe |
| split criteria absent | Cannot isolate useful material. | Split criteria review. | Yes | Yes | Yes |
| no implementation readiness assessment | No readiness evidence. | Future IR review. | Yes | Yes | Yes |
| no governance activation decision | No approval path. | Governance decision. | Yes | Yes | Yes |

## 19. Split Review Criteria
Future split review requires: exact material class known, product alignment known, owner proposed, scope isolated, source sensitivity known, dependency posture known, generated-output posture known, product/root boundary clear, target product or new candidate declared, and validation/security/governance route exists.

P-07 does not perform split review or create split artifacts.

## 20. Archive Candidate Criteria
Future archive-candidate review requires: obsolete or superseded experimental material identified, no current product value, no active ticket dependency, no secret/credential risk, no audit/provenance need unresolved, restoration or non-restoration path declared, exact scope declared, and M-08/A-series governance applies.

P-07 does not execute archive.

## 21. Rejection / Deferral Criteria
Use `reject_for_current_phase` if material has no current product route, no owner, or root-leakage risk.

Use `defer_pending_classification` if safe metadata is insufficient. Use `future_charter_candidate_after_split` only if future exact evidence shows a distinct product candidate with owner, scope, boundary, security, dependency, Git, validation, and governance route.

## 22. P-07 Gate Checklist
| item | status | note |
| --- | --- | --- |
| experimental selected for disposition in P-00 | pass | P-00 lists P00-SEL-006. |
| no product charter created | pass | Disposition only. |
| owner gap recorded | pass_with_caution | No owner accepted. |
| purpose gap recorded | pass_with_caution | No final purpose. |
| scope gap recorded | pass_with_caution | No final scope. |
| local-only posture declared | pass | `2_products/` remains ignored/local-only. |
| security posture declared | pass_with_caution | Unknown sensitivity blocks use. |
| dependency posture unknown and blocked | blocked | Deferred to P-09. |
| Git posture deferred to P-08 | pass_with_caution | No tracking approval. |
| validation baseline deferred to P-10 | pass_with_caution | No baseline created. |
| archive execution not performed | pass | No `_archive/`, movement, copy, or deletion. |
| split not performed | pass | No split artifacts. |
| activation blockers declared | pass | Blockers listed. |
| stop rules declared | pass | Stop before P-08. |

Final disposition status: `blocked_local_only_sandbox_pending_future_split_or_archive_review`.

## 23. Residual Risks
Residual risks: no active product owner, no purpose, no final scope, no classification of internal material, no product source review, no dependency review, no generated-output review, no security review, no Git posture decision, no validation baseline, no split/reject/archive execution, no implementation readiness, and no product activation decision.

## 24. P-07 Invariants
| ID | Invariant |
| --- | --- |
| P07-001 | Experimental disposition is not product activation. |
| P07-002 | Experimental is not selected for product charter drafting in the current phase. |
| P07-003 | Experimental remains blocked/local-only. |
| P07-004 | Product source remains local-only. |
| P07-005 | Product Git posture is not changed. |
| P07-006 | Product dependencies are not adopted. |
| P07-007 | Product validation baseline is not created. |
| P07-008 | Archive candidate posture is not archive execution. |
| P07-009 | Split review is not performed by P-07. |
| P07-010 | Experimental does not define root architecture. |
| P07-011 | Experimental does not decide Cognitive Semantic System substrate. |
| P07-012 | Graph remains a candidate only. |
| P07-013 | Validation evaluates; governance decides. |
| P07-014 | P-07 stops before P-08. |

## 25. Anti-patterns
Anti-patterns: experimental as product by proximity; disposition as activation; disposition as charter; disposition as archive execution; disposition as deletion; disposition as source split; disposition by folder curiosity; product source inspection by curiosity; experimental source as root authority; generated experimental output as source; dependency adoption by prototype presence; Git tracking by cleanup pressure; starting P-08 inside P-07; `git add .`.

## 26. Readiness For P-08
P-08 - Product Git Posture Decision is ready after explicit instruction if P-07 Experimental Workspace Disposition exists, all six product candidates have charter/disposition records, products remain inactive, product source remains local-only, no product Git posture has been changed, and no product activation, source tracking, dependency adoption, archive execution, publication, or implementation is implied.

Do not create P-08.

## 27. Final Verdict
| Question | Answer |
| --- | --- |
| What does P-07 decide? | `experimental` remains a blocked local-only sandbox pending future split or archive review. |
| What is experimental in Siamese? | Not a named Siamese product surface; an ambiguous sandbox/prototype candidate unless future exact evidence proves otherwise. |
| Did P-07 create an Experimental Product Charter? | No. |
| Did P-07 activate experimental? | No. |
| Did P-07 inspect experimental source deeply? | No. |
| Did P-07 split, move, archive, delete, or transform files? | No. |
| Did P-07 change product Git posture? | No. |
| Did P-07 adopt dependencies? | No. |
| Did P-07 create validation baselines? | No. |
| What remains blocked? | Product activation, product chartering, source inspection, source tracking, split, archive execution, deletion, movement, dependency adoption, validation baselines, implementation readiness, publication, provider/API/MCP/network/auth activation, staging, commit, push, and P-08. |
| Is P-08 ready after explicit instruction? | Yes, as Product Git Posture Decision only; P-08 is not started. |

Stop after P-07 validation and report. Do not start P-08 or any later ticket.
