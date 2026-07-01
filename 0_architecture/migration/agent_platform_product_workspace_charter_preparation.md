# M-07 - Product Workspace Charter Preparation
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Product Workspace Charter Preparation |
| Ticket | M-07 |
| Status | Accepted product workspace charter preparation |
| Date | 2026-07-01 |
| Scope | Safe-metadata preparation records for AGENT PLATFORM product workspace candidates |
| Authority | Charter-preparation planning only, not product activation, active charter acceptance, product source review, product execution, dependency adoption, product Git posture change, publication, migration execution, archive execution, implementation, staging, commit, push, or M-08 start |
| Related documents | M-06, M-04, M-05, V-04, W-12, W-13, A-00, A-01, V-03, CSS-series, H-series, S-series |

## 2. Purpose
M-07 follows M-06. M-06 captured external metadata posture, including product/domain dependency blockers for external sources.
M-07 prepares product workspace charter metadata for the six W-12 product candidates. It does not activate products, create active product charters, inspect product source deeply, execute product code/tests/builds, adopt dependencies, change Git posture, publish product material, or start M-08.
M-07 prepares M-08 - Archive Execution Policy by preserving product/local-only/lifecycle blockers before archive policy work.

## 3. Product Workspace Charter Preparation Definition
Product workspace charter preparation is a controlled safe-metadata planning step that identifies product candidates, charter gaps, root-boundary requirements, validation baseline needs, dependency posture, security posture, generated-output posture, Git posture, lifecycle posture, and governance blockers before any product activation or product migration work.
Product charter preparation is not product activation. It is also not charter acceptance, product execution, dependency adoption, product Git tracking, publication, or current authority.

## 4. Authority Boundary
| Layer | M-07 boundary |
| --- | --- |
| Governance | Decides product activation, charter acceptance, publication, product Git posture, dependency adoption, retirement, migration, lifecycle, and exceptions. |
| Validation | V-04 evaluates product readiness, baseline needs, gaps, blockers, and proof posture. |
| Evidence | Supports charter preparation only when source status, scope, sensitivity, and limitations are visible. |
| Security | S-series constrains local-only handling, secrets, credentials, execution, provider/API/MCP/network use, generated output, and publication. |
| W-12 | Primary product workspace policy and product/root boundary source. |
| M-06/W-13/V-05 | External/domain metadata and dependency posture only. |
| A-00/A-01 | Lifecycle language only; no lifecycle state is applied to files. |
| Agents | May prepare safe metadata but cannot activate products, approve charters, adopt dependencies, change Git posture, or continue to M-08. |

## 5. Source Boundary
W-12 product workspace policy is the primary product boundary source. V-04 product validation model is the primary validation source. M-06 provides external/domain metadata context. M-04 provides runtime/provider/adapter planning context.
Raw `2_products/` remains local-only and is not deeply inspected. Product source code, configs, generated outputs, data, models, artifacts, logs, secrets, credentials, package manifests, and local sessions are not copied or used as authority. Product candidate names and W-12 policy posture may be retained as safe metadata.

## 6. Product Candidate Inventory
| product_id | Product candidate | Current posture | Likely purpose area | Dependency/domain risk | Local-only posture | Charter preparation need | Blocked inference |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PROD-001 | `backend-energyplus` | candidate/deferred/local_only | Backend/domain simulation | High: EnergyPlus/native/license/data | Ignored under `2_products/` | Domain charter, owner, scope, dependency posture | Backend behavior or engine approval. |
| PROD-002 | `cli` | candidate/deferred/local_only | CLI/operator interface | Medium: commands/packages/user data | Ignored under `2_products/` | Interface charter and command boundary | CLI works or is safe to run. |
| PROD-003 | `desktop` | candidate/deferred/local_only | Desktop/local runtime | Medium-high: runtime/packaging/local data | Ignored under `2_products/` | Desktop charter, packaging/security posture | Desktop app behavior or release readiness. |
| PROD-004 | `experimental` | experimental/blocked/local_only | Prototype/sandbox | High: unclear source, root leakage | Ignored under `2_products/` | Split, owner, isolation, defer/archive route | Roadmap priority or activation. |
| PROD-005 | `omniverse-app` | candidate/deferred/local_only | Omniverse/visualization | High: SDK/runtime/GPU/license/output | Ignored under `2_products/` | Visualization charter and external dependency review | Product claim or SDK approval. |
| PROD-006 | `web-platform` | candidate/deferred/local_only | Web/interface | Medium-high: auth/data/build/deploy | Ignored under `2_products/` | Web charter, auth/data/build posture | Web behavior or deploy readiness. |

## 7. Product Charter Scope
Future product charter preparation fields: product candidate, purpose, user/domain/interface hypothesis, owner status, scope status, non-goals status, product/root boundary status, product state, Git posture, validation baseline need, security/access posture, dependency posture, generated-output posture, external-source posture, lifecycle posture, activation blockers, governance path, and stop rule.
This is not an active product charter, schema, registry, product file, API, test, script, or implementation.

## 8. Product State Preparation Model
| State | Meaning | Allowed preparation use | Blocked use | Evidence required | Future route |
| --- | --- | --- | --- | --- | --- |
| candidate | Product folder/concept exists. | Identify charter gaps. | Active product. | Inventory/path/status. | Charter draft later. |
| active | Approved for governed product work. | List preconditions only. | Activation by M-07. | Owner/scope/baseline/governance. | Governance decision. |
| experimental | Prototype/sandbox. | Isolation and blocker review. | Production claim. | Owner/isolation/risk notes. | Split, defer, archive, or charter. |
| deferred | Postponed candidate. | Record gap/reopen trigger. | Rejection or activation. | Deferral reason. | Governance review later. |
| blocked | Missing precondition or risk. | Preserve blocker. | Proceeding as ready. | Blocker record. | Resolve or reject. |
| archived | Retained under archive policy. | Future lifecycle candidate only. | Archive execution. | A-00/A-01 plus approval. | M-08/later archive policy. |
| retired | No longer active. | Historical posture only. | Active product. | Retirement reason/owner. | Lifecycle review later. |
| local_only | Ignored/untracked material. | Git/local-only evidence. | Commit-safe inference. | `.gitignore`/Git evidence. | Git governance later. |
| product_scoped_canonical | Product doc accepted inside scope. | Define future charter target. | Root authority. | Product decision/root boundary. | Product governance. |
| implementation_ready | Preconditions met for implementation ticket. | Gap target only. | Implementation approval. | Charter/baseline/security/deps/Git. | IR later. |

## 9. Charter Gap Model
| Gap | Stop behavior | Required future action | Blocks activation? | Blocks migration? |
| --- | --- | --- | --- | --- |
| missing purpose | Stop charter acceptance. | State product reason and outcomes. | Yes | Yes |
| missing owner | Stop activation path. | Assign owner/roles. | Yes | Yes |
| missing scope | Stop validation use. | Define boundaries/interactions. | Yes | Yes |
| missing non-goals | Qualify scope. | Add exclusions. | Usually | Usually |
| missing root-boundary statement | Stop authority claim. | State product is not root authority. | Yes | Yes |
| missing product state | Stop state claim. | Declare W-12 state. | Yes | Yes |
| missing Git posture | Stop Git/source tracking claim. | Govern local-only/docs/source/split posture. | Yes | Yes |
| missing validation baseline | Stop readiness. | Define baseline fields under V-04. | Yes | Yes |
| missing security/access posture | Stop exposure/action. | Security review. | Yes | Yes |
| missing dependency posture | Stop adoption/readiness. | Dependency/domain review. | Yes | Yes |
| missing generated-output posture | Stop output use. | Provenance/sensitivity handling. | Yes | Yes |
| missing external-source posture | Stop external dependency claim. | M-06/W-13/V-05 review. | Yes | Yes |
| missing governance path | Stop acceptance/promotion. | Define approver/decision route. | Yes | Yes |
| product-root collapse risk | Stop root claim. | Re-scope to product. | Yes | Yes |
| activation implied | Stop wording/action. | Restore preparation-only status. | Yes | Yes |
| implementation implied | Stop implementation path. | Defer to IR/implementation ticket. | Yes | Yes |

## 10. Product / Root Boundary Rules
Product candidates do not define AGENT PLATFORM root authority. Product docs remain product-scoped. Product source remains local-only. Product needs may inform root proposals but cannot silently constrain root.
Product storage, runtime, dependency, validation, and Git decisions are product-scoped unless governed otherwise. Product generated outputs are evidence, not source by default. Product activation requires explicit governance.

## 11. Product Validation Baseline Preparation
Future baseline fields: acceptance criteria, product target behavior, non-goals, test strategy, manual review strategy, generated-output handling, security checks, local-only checks, dependency checks, data/model/artifact checks, evidence retention, proof level target, revalidation triggers, and known limitations.
M-07 identifies baseline needs only. It does not create executable baselines, tests, commands, builds, product validators, CI, or active product authority.

## 12. Product Security / Local-only Rules
`2_products/` remains local-only. Product secrets, credentials, `.env`, config, provider auth, registry auth, local sessions, data, models, artifacts, logs, and generated outputs are excluded. Unknown sensitivity escalates. Safe metadata is preferred. Product material is not included in context by default. M-07 does not inspect product source deeply.

## 13. Product Dependency Posture Rules
Dependency references are not adoption approval. Product-specific dependency is not root dependency. External/domain SDK relevance remains product/domain scoped. Native/domain engine risk requires product governance. License/notice posture requires future review. Provider/API/network/MCP dependency risks remain blocked. Package manager actions remain blocked.

## 14. Product Generated Output Rules
Screenshots, reports, simulation outputs, logs, exports, generated docs, build outputs, and product artifacts are generated-sensitive by default. Generated output is not source by default. Raw output remains local-only unless reviewed. Publication requires security, validation, product governance, and root-boundary review. M-07 does not inspect or generate outputs.

## 15. Product Git Posture Rules
M-07 does not change product Git posture. Product Git posture is not changed by M-07. `2_products/` remains ignored/local-only. Product files must not be staged by default. Product docs/source tracking requires explicit product governance. Product local-only staged material, product secret staged material, broad staging, or `git add .` is a blocker. Git status is evidence only.

## 16. External / Domain Source Relationship
| External/domain source | Product relationship | M-07 handling |
| --- | --- | --- |
| `EnergyPlusV24-2-0` | Backend/domain/product evidence only. | Relevant to `backend-energyplus`; no execution, license approval, dependency adoption, or product claim. |
| `openstudio` | Backend/domain/product evidence only. | Future building-energy product review only; no SDK adoption. |
| `graphify` | CSS/substrate evidence only. | Not product authority, product dependency, or CSS name. |
| `opencode`, `pi`, `ECC-main`, `hermes-agent`, `openclaw`, `acpx`, `clawhub`, `ai-cookbook-main`, `tau` | Harness/tool/provider/external evidence only. | No product tooling, provider/API/MCP activation, registry trust, package install, or adoption by proximity. |
External relevance does not activate product dependency.

## 17. Cognitive Semantic System Boundary
`Cognitive Semantic System` is the accepted current name. Product candidates cannot name or define it. The final Cognitive Semantic System substrate remains undecided. Graph remains a candidate only.
Graph/product visualization evidence is not a substrate decision. Product needs may inform future criteria but cannot decide root substrate. `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth` may appear only as rejected/prohibited/historical/candidate-evidence examples.

## 18. Harness / Runtime Boundary
H-series and M-04 keep harness, runtime, provider, adapter, tool, command, hook, skill, and MCP material as bounded evidence only. Product harness/runtime material remains product-scoped. OpenCode/operator usage is not product authority. No product runtime is implemented, no product execution is authorized, and no provider/API/MCP activation occurs.

## 19. Lifecycle Posture Mapping
| Posture | M-07 use | Boundary |
| --- | --- | --- |
| `retain_product_scoped` | Preserve product-only relevance. | Not root authority. |
| `retain_safe_metadata_only` | Retain candidate name, posture, gaps, blockers. | No raw product content. |
| `retain_migration_context` | Preserve charter-preparation route. | No migration execution. |
| `retain_historical_trace` | Keep prior/product rationale later. | Not active. |
| `retain_audit_evidence` | Retain gap/blocker evidence. | Evidence only. |
| `retain_external_reference` | Preserve M-06 domain references. | No adoption. |
| `blocked_unknown` | Missing status/security/scope. | Stop use. |
| `incident_restricted` | Secret/local-only exposure risk. | Stop and secure handling. |
M-07 does not apply lifecycle state to actual product files.

## 20. Validation Posture Mapping
| Proof target | M-07 use | Limitation |
| --- | --- | --- |
| PL-1 | Product inventory/path/Git ignore metadata. | Existence only. |
| PL-2 | Product state/source-status/sensitivity. | No behavior proof. |
| PL-3 | Charter/source references. | Citation, not approval. |
| PL-4 | Future charter/root-boundary/coherence review. | No execution. |
| PL-5 | Future scoped metadata/Git checks only. | Command checks are narrow. |
| PL-6 | Future explicitly approved product tests only. | Not used by M-07. |
| PL-7 | Future product readiness audit. | Audit, not activation. |
| PL-8 | Future reproduced product audit. | Still scoped. |
No proof level approves product activation, execution, dependency adoption, product Git tracking, publication, or migration.

## 21. Migration Boundary
M-07 prepares product charter metadata only. It performs no product migration, file movement, source copying, source rewriting, archive execution, wholesale migration, product promotion, implementation, staging, commit, push, or publication. M-08 handles archive execution policy later after explicit instruction.

## 22. Context Boundary
Product charter-preparation records may inform future context packs only if safe, scoped, cited, and labeled as product preparation records. Context inclusion is not product activation, publication, permission, validation approval, or Git approval. Raw product content remains excluded by default.

## 23. Preparation Method
Method: read W-12; read V-04; read M-06 for product/domain relevance; read M-04 for runtime/provider/adapter boundaries; retain only safe metadata; list product candidates; identify charter gaps and blockers; assign product preparation IDs; assign lifecycle, validation, security/local-only posture; identify future route; stop before product activation, product source review, implementation, publication, or M-08.
If product detail is insufficient, record a blocker, do not inspect `2_products/` deeply, and do not invent product facts.

## 24. Product Charter Preparation Table
| prep_id | Product candidate | Likely product area | Current posture | Charter gaps | Dependency/domain relevance | Validation posture | Blocker / next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M07-PREP-001 | `backend-energyplus` | backend/domain simulation | candidate/deferred/local_only | purpose, owner, scope, non-goals, root boundary, baseline, security, Git | EnergyPlus and OpenStudio domain evidence; no adoption | PL-1/PL-2 metadata only | Future product charter plus domain dependency review. |
| M07-PREP-002 | `cli` | CLI/operator interface | candidate/deferred/local_only | purpose, owner, command scope, non-goals, baseline, security, Git | Harness/tool evidence only; no package/provider activation | PL-1/PL-2 metadata only | Future interface charter and command-safety review. |
| M07-PREP-003 | `desktop` | desktop/local runtime | candidate/deferred/local_only | purpose, owner, scope, packaging, local data, baseline, Git | Runtime/package/security evidence only | PL-1/PL-2 metadata only | Future desktop charter and security/packaging review. |
| M07-PREP-004 | `experimental` | experimental/prototype | experimental/blocked/local_only | owner, isolation, scope, non-goals, split/defer/archive decision | Unknown; do not infer | PL-1/PL-2 blocker metadata | Decide split, retire, archive route, or charter later. |
| M07-PREP-005 | `omniverse-app` | Omniverse/visualization | candidate/deferred/local_only | purpose, owner, visualization scope, SDK/license, output, security, Git | Omniverse/SDK dependency posture unresolved | PL-1/PL-2 metadata only | Future visualization charter and dependency/security review. |
| M07-PREP-006 | `web-platform` | web/interface | candidate/deferred/local_only | purpose, owner, auth/data/build/deploy scope, baseline, Git | Web packages/API/auth risks unresolved | PL-1/PL-2 metadata only | Future web charter and validation/security review. |

## 25. Target Area Grouping
| Target area | Product candidates or inputs | Preparation posture |
| --- | --- | --- |
| backend/domain simulation | `backend-energyplus`; EnergyPlus/OpenStudio evidence | Product/domain charter later. |
| CLI/operator interface | `cli`; M-04/H boundaries | Command/interface charter later. |
| desktop/local runtime | `desktop` | Runtime/packaging/security charter later. |
| experimental/prototype | `experimental` | Isolation, split, defer, archive, or reject later. |
| Omniverse/visualization | `omniverse-app` | Visualization charter and SDK review later. |
| web/interface | `web-platform` | Web/auth/data/build charter later. |
| product governance | W-12/W-11 | Owner/scope/Git/state decisions later. |
| product validation | V-04/V-03/V-01 | Baseline/readiness review later. |
| product dependency posture | M-06/W-13/V-05 | External/domain review later. |
| product security/local-only | S-series/.gitignore | Local-only and secret posture later. |
| implementation-readiness later | IR later | Not ready in M-07. |

## 26. Blocker Register
| Blocker | Stop behavior | Required action | Blocks charter acceptance? | Blocks activation? | Blocks migration? |
| --- | --- | --- | --- | --- | --- |
| W-12 missing | Stop M-07. | Restore product policy. | Yes | Yes | Yes |
| V-04 missing | Stop readiness claims. | Restore validation model. | Yes | Yes | Yes |
| product candidate unknown | Stop candidate use. | Classify candidate. | Yes | Yes | Yes |
| missing product purpose | Stop charter acceptance. | Define purpose. | Yes | Yes | Yes |
| missing owner | Stop activation. | Assign owner. | Yes | Yes | Yes |
| missing scope | Stop validation. | Define boundaries. | Yes | Yes | Yes |
| missing non-goals | Qualify charter. | Add exclusions. | Usually | Usually | Usually |
| missing root-boundary statement | Stop authority claim. | Add root boundary. | Yes | Yes | Yes |
| missing product state | Stop status claim. | Declare W-12 state. | Yes | Yes | Yes |
| missing Git posture | Stop tracking claim. | Govern Git posture. | Yes | Yes | Yes |
| missing validation baseline | Stop readiness. | Define baseline. | Yes | Yes | Yes |
| missing security/access posture | Stop exposure/action. | Security review. | Yes | Yes | Yes |
| missing dependency posture | Stop adoption/readiness. | Dependency review. | Yes | Yes | Yes |
| missing generated-output posture | Stop output use. | Review output policy. | Yes | Yes | Yes |
| missing governance path | Stop promotion. | Define approval route. | Yes | Yes | Yes |
| product source inspection required | Stop curation. | Request explicit product scope. | Maybe | Yes | Yes |
| product execution implied | Stop action. | Future exact approval. | Yes | Yes | Yes |
| dependency adoption implied | Stop wording/action. | Governance/dependency review. | Yes | Yes | Yes |
| product-root collapse | Stop root claim. | Re-scope to product. | Yes | Yes | Yes |
| product local-only leak | Stop exposure/Git. | Safe metadata/security review. | Yes | Yes | Yes |
| external/domain license risk | Stop reuse/adoption. | License/name-use review. | Yes | Yes | Yes |
| provider/API/MCP activation implied | Stop activation. | Security/governance approval. | Yes | Yes | Yes |
| publication implied | Stop publication path. | Product/security/governance review. | Yes | Yes | Yes |
| M-08 scope pressure detected | Stop adjacent work. | Wait explicit M-08 instruction. | No | No | Yes |

## 27. Product Preparation Verdict Model
Verdicts: `product_preparation_complete_for_policy_scope`, `product_preparation_complete_with_cautions`, `product_blocked_by_missing_policy`, `product_blocked_by_missing_owner`, `product_blocked_by_missing_scope`, `product_blocked_by_missing_root_boundary`, `product_blocked_by_security_risk`, `product_blocked_by_dependency_posture`, `product_blocked_by_generated_output_risk`, `product_blocked_by_product_root_collapse`, `product_blocked_by_governance_gap`, `product_inconclusive`, and `product_deferred`.
A verdict is not product activation approval.

## 28. Candidate Routing Model
| Route | Meaning |
| --- | --- |
| `ready_for_charter_draft_later` | Future product charter task may draft scoped charter metadata. |
| `deferred_to_product_governance` | Owner, scope, state, Git posture, or activation decision needed. |
| `deferred_to_product_validation` | Baseline/readiness review needed. |
| `deferred_to_dependency_review` | Dependency/domain review needed. |
| `deferred_to_security_review` | Local-only/secret/provider/data posture needed. |
| `deferred_to_external_review` | External/domain metadata review needed. |
| `deferred_to_IR` | Implementation readiness later only. |
| `deferred_to_archive_lifecycle` | A/M-08 later lifecycle handling only. |
| `blocked` | Required action before use. |

## 29. Evidence Retention Rules
Retain safe metadata: product candidate name, product class/posture, charter gap summary, dependency/domain relevance, validation posture, lifecycle posture, security/local-only posture, blocker status, and future route.
Do not retain secrets, credentials, raw product source, raw product generated output, raw external source, unsafe local-only content, dependency content, provider/auth material, local sessions, or copied product artifacts.

## 30. Incident Handling
Incidents include product source copied, product code executed, product tests/builds run, product generated output copied, product secret/credential discovered, product local-only material staged, product dependency adopted, product activated by implication, product docs promoted to root, external/domain source treated as adopted, provider/API/MCP activated, file movement attempted, Git staging attempted, or M-08/next ticket started.
Response: STOP, report safe metadata, do not continue adjacent work, and require human/security/product/governance decision.

## 31. M-07 Invariants
| ID | Invariant |
| --- | --- |
| M07-001 | Product charter preparation is not product activation. |
| M07-002 | Product preparation record is not an accepted charter. |
| M07-003 | Product proof is product-scoped. |
| M07-004 | Product material remains local-only by default. |
| M07-005 | Product source is not inspected deeply. |
| M07-006 | Product dependencies are not adopted. |
| M07-007 | Product generated output is not source. |
| M07-008 | Product Git posture is not changed. |
| M07-009 | Product needs do not decide root architecture. |
| M07-010 | Product needs do not decide Cognitive Semantic System substrate. |
| M07-011 | Graph remains a candidate only. |
| M07-012 | Validation evaluates; governance decides. |
| M07-013 | External/domain metadata is evidence only. |
| M07-014 | Context exposure is not activation. |
| M07-015 | M-07 stops before M-08. |

## 32. Anti-patterns
Anti-patterns: charter by folder existence; charter by product enthusiasm; activation by preparation; product source as root authority; product docs as root architecture; product dependency as root dependency; domain SDK as root dependency; generated output as source; product test as root proof; product local-only leakage; product commit by `git add .`; product source tracking by implication; external source as product dependency by proximity; provider/API/MCP activation by product need; product scope invented without evidence; starting M-08 inside M-07.

## 33. Remaining Gaps
No accepted product charters, product activation, product owners, finalized product scopes, validation baselines, dependency approvals, product Git posture changes, product source tracking, product tests/builds/execution, generated-output review, external/domain dependency adoption, implementation readiness, archive execution policy, or M-08 artifact exists.

## 34. Readiness For M-08
M-08 - Archive Execution Policy is ready after explicit instruction if M-07 captures product charter preparation posture, A-00/A-01 archive and lifecycle policies remain preserved, product/local-only/external/security boundaries remain preserved, M-02 through M-07 safe-metadata boundaries remain preserved, and no file movement, archive execution, product activation, product source tracking, external adoption, dependency adoption, publication, or implementation is implied.
M-08 should define how archive execution would be governed later while still avoiding actual archive execution unless explicitly authorized in a future scoped batch. Do not create M-08.

## 35. Final Verdict
| Question | Answer |
| --- | --- |
| What does M-07 prepare? | Safe product workspace charter-preparation metadata and blocker/routing records for six W-12 product candidates. |
| Did M-07 create active product charters? | No. |
| Did M-07 inspect product source deeply? | No. |
| Did M-07 activate products? | No. |
| Did M-07 change product Git posture? | No. |
| Did M-07 adopt dependencies? | No. |
| Did M-07 publish product material? | No. |
| Did M-07 select substrate? | No. The Cognitive Semantic System substrate remains undecided; graph remains a candidate only. |
| What remains blocked? | Product activation, charter acceptance, source inspection, execution, tests/builds, dependency adoption, product Git changes, publication, migration, archive execution, implementation, provider/API/MCP activation, staging, commit, push, and M-08. |
| Is M-08 ready after explicit instruction? | Yes, as archive execution policy planning only; M-08 is not started. |
M-07 final verdict:
```text
M-07 is complete as product workspace charter preparation only.
M-07 prepares product workspace charter metadata as safe planning evidence only. It
keeps product candidates local-only, inactive, product-scoped, dependency-blocked,
Git-unchanged, substrate-neutral, and stops before activation, migration, archive
execution, implementation, publication, Git actions, and M-08.
```
