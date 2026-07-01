# P-A - Product Workspace Audit
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Product Workspace Audit |
| Ticket | P-A |
| Status | Accepted product workspace audit |
| Date | 2026-07-01 |
| Scope | Audit of FASE 4 - Product Workspace Governance for AGENT PLATFORM / Siamese. |
| Authority | Audit only, not product activation or implementation readiness. |
| Related documents | P-00 through P-10, M-A, M-06, M-07, W-11, W-12, W-13, V-01, V-02, V-04, V-05, V-A, S-series, CSS-series, H-series, `.gitignore`, `README.md`, Siamese Product Vision |
| Audit target | FASE 4 - Product Workspace Governance |

## 2. Purpose
P-00 selected product routes. P-01 defined the common product gate. P-02 through P-06 drafted inactive product charters. P-07 dispositioned `experimental` as blocked local-only sandbox. P-08 decided docs-only Git posture. P-09 decided dependency/external posture without adoption. P-10 defined validation baseline without validation execution.

P-A audits the complete product workspace governance phase. It does not activate products, approve implementation readiness, execute validation, change Git posture, adopt dependencies, publish, or start IR-00.

## 3. Product Workspace Audit Definition
A product workspace audit is a controlled review of product governance artifacts, product states, charter completeness, gate posture, local-only posture, Git posture, dependency posture, validation baseline, blockers, residual risks, and readiness constraints across P-00 through P-10.

Audit is not governance approval, product activation, implementation readiness, validation execution, source tracking approval, dependency adoption, publication approval, or next-phase authorization.

## 4. Audit Authority Boundary
| Layer | P-A boundary |
| --- | --- |
| Governance | Decides activation, source tracking, dependency adoption, publication, exceptions, implementation readiness, and next-phase transition. |
| Validation | Evaluates evidence and coherence. |
| Audit | Reports findings, blockers, and residual risks. |
| Security | Constrains local-only, secrets, credentials, execution, providers, APIs, MCP, network/auth, generated outputs, and publication. |
| Git | Records artifacts but does not approve product state. |
| Agents | May audit safe metadata; cannot execute, activate, adopt, stage, commit, push, publish, or start IR-00. |

## 5. Exact Audit Scope
| audit_id | artifact | exact path | expected role | audit question | expected posture | blocked inference |
| --- | --- | --- | --- | --- | --- | --- |
| PA-SCOPE-001 | P-00 Product Workspace Selection | `0_architecture/product_workspaces/agent_platform_product_workspace_selection.md` | Route selection | Were candidates routed? | Planning only. | Activation. |
| PA-SCOPE-002 | P-01 Common Product Gate | `0_architecture/product_workspaces/agent_platform_product_charter_template_common_gate.md` | Gate/template | Are common fields/gates defined? | Inert gate. | Charter acceptance. |
| PA-SCOPE-003 | P-02 Omniverse App Charter | `0_architecture/product_workspaces/agent_platform_omniverse_app_product_charter.md` | Inactive charter | Is visual interface scoped? | Draft with blockers. | Kit/runtime approval. |
| PA-SCOPE-004 | P-03 Backend EnergyPlus Charter | `0_architecture/product_workspaces/agent_platform_backend_energyplus_product_charter.md` | Inactive charter | Is backend/domain scope bounded? | Draft with blockers. | Solver adoption. |
| PA-SCOPE-005 | P-04 CLI Charter | `0_architecture/product_workspaces/agent_platform_cli_product_charter.md` | Inactive charter | Is command surface bounded? | Draft with blockers. | Shell permission. |
| PA-SCOPE-006 | P-05 Desktop Charter | `0_architecture/product_workspaces/agent_platform_desktop_product_charter.md` | Inactive charter | Is local runtime bounded? | Draft with blockers. | Desktop runtime approval. |
| PA-SCOPE-007 | P-06 Web Charter | `0_architecture/product_workspaces/agent_platform_web_platform_product_charter.md` | Inactive charter | Is web/deploy/auth bounded? | Draft with blockers. | Deploy/auth approval. |
| PA-SCOPE-008 | P-07 Experimental Disposition | `0_architecture/product_workspaces/agent_platform_experimental_workspace_disposition.md` | Disposition | Is sandbox blocked? | Blocked local-only. | Product charter/activation. |
| PA-SCOPE-009 | P-08 Git Posture | `0_architecture/product_workspaces/agent_platform_product_git_posture_decision.md` | Git posture | Is docs-only/source-local-only preserved? | No Git change. | Source tracking. |
| PA-SCOPE-010 | P-09 Dependency Posture | `0_architecture/product_workspaces/agent_platform_product_dependency_external_source_posture.md` | Dependency posture | Are dependencies unadopted? | Candidate only. | Adoption. |
| PA-SCOPE-011 | P-10 Validation Baseline | `0_architecture/product_workspaces/agent_platform_product_validation_baseline.md` | Baseline | Is validation defined but not run? | Documentation only. | Test/build execution. |
| PA-SCOPE-012 | W-12 Product Policy | `0_architecture/workspace/agent_platform_product_workspace_policy.md` | Product policy | Are activation preconditions preserved? | Product-scoped. | Root authority. |
| PA-SCOPE-013 | V-04 Product Validation | `0_architecture/validation/agent_platform_product_validation_model.md` | Validation model | Does validation evaluate only? | Evidence only. | Approval. |
| PA-SCOPE-014 | S-series Security | `0_architecture/security/` | Security boundary | Are local-only/execution constraints intact? | Blocking layer. | Permission. |
| PA-SCOPE-015 | `.gitignore` / `README.md` | `.gitignore`, `README.md` | Root controls | Are root hygiene files present? | Evidence only. | Approval. |

## 6. Exact Target Scope
Target: `0_architecture/product_workspaces/agent_platform_product_workspace_audit.md`.

This file is the only target artifact. No source file is modified. No product source is inspected or tracked. No product is activated. No Git action is performed. No next-phase artifact is created.

## 7. Audit Method
Method: read accepted product governance documents only; confirm P-00 through P-10 exist; confirm all product candidates have charter/disposition records; confirm all products remain inactive; confirm product source remains local-only; confirm P-08 Git posture remains unchanged; confirm P-09 dependency posture remains candidate-only; confirm P-10 baseline is documentation-only; confirm no product validation execution occurred; record findings, residual risks, blockers, and phase closure verdict; stop before IR-00.

No product source, external source, generated output, secret, credential, package tree, provider state, or runtime output was deeply inspected.

## 8. Artifact Existence Audit
| artifact | expected path | exists? | role | audit status | blocker if missing |
| --- | --- | --- | --- | --- | --- |
| P-00 | `0_architecture/product_workspaces/agent_platform_product_workspace_selection.md` | pending_command_validation | Selection. | observed | Blocks phase audit. |
| P-01 | `0_architecture/product_workspaces/agent_platform_product_charter_template_common_gate.md` | pending_command_validation | Common gate. | observed | Blocks charter audit. |
| P-02 | `0_architecture/product_workspaces/agent_platform_omniverse_app_product_charter.md` | pending_command_validation | Inactive charter. | observed | Blocks product coverage. |
| P-03 | `0_architecture/product_workspaces/agent_platform_backend_energyplus_product_charter.md` | pending_command_validation | Inactive charter. | observed | Blocks product coverage. |
| P-04 | `0_architecture/product_workspaces/agent_platform_cli_product_charter.md` | pending_command_validation | Inactive charter. | observed | Blocks product coverage. |
| P-05 | `0_architecture/product_workspaces/agent_platform_desktop_product_charter.md` | pending_command_validation | Inactive charter. | observed | Blocks product coverage. |
| P-06 | `0_architecture/product_workspaces/agent_platform_web_platform_product_charter.md` | pending_command_validation | Inactive charter. | observed | Blocks product coverage. |
| P-07 | `0_architecture/product_workspaces/agent_platform_experimental_workspace_disposition.md` | pending_command_validation | Disposition. | observed | Blocks experimental audit. |
| P-08 | `0_architecture/product_workspaces/agent_platform_product_git_posture_decision.md` | pending_command_validation | Git posture. | observed | Blocks Git audit. |
| P-09 | `0_architecture/product_workspaces/agent_platform_product_dependency_external_source_posture.md` | pending_command_validation | Dependency posture. | observed | Blocks dependency audit. |
| P-10 | `0_architecture/product_workspaces/agent_platform_product_validation_baseline.md` | pending_command_validation | Validation baseline. | observed | Blocks baseline audit. |
| W/V/S/CSS/H controls | Required directories and named docs | pending_command_validation | Boundaries. | observed | Blocks closure if missing. |

## 9. Product Governance Phase Ledger
| phase_record_id | artifact | contribution | boundary preserved | residual risk | audit verdict |
| --- | --- | --- | --- | --- | --- |
| P-A-REC-001 | P-00 selection | Routed six candidates. | Planning only. | Owners/scopes absent. | pass |
| P-A-REC-002 | P-01 common gate | Defined template and GATE-01..18. | Gate not acceptance. | Individual gaps remain. | pass |
| P-A-REC-003 | P-02 `omniverse-app` | Inactive visual interface charter. | Omniverse Kit interface, not backend. | SDK/runtime/output blockers. | pass_with_caution |
| P-A-REC-004 | P-03 `backend-energyplus` | Inactive backend charter. | EnergyPlus solver, not internal model. | Native/data/API blockers. | pass_with_caution |
| P-A-REC-005 | P-04 `cli` | Inactive CLI charter. | Interface, not shell permission. | Command/package blockers. | pass_with_caution |
| P-A-REC-006 | P-05 `desktop` | Inactive desktop charter. | Interface, not runtime approval. | Packaging/local-data blockers. | pass_with_caution |
| P-A-REC-007 | P-06 `web-platform` | Inactive web charter. | Interface, not deploy/auth approval. | Auth/build/deploy blockers. | pass_with_caution |
| P-A-REC-008 | P-07 experimental | Blocked sandbox disposition. | No charter/activation. | Ambiguity remains. | pass_with_caution |
| P-A-REC-009 | P-08 Git posture | Docs-only/source-local-only decision. | No Git mutation. | Future source strategy absent. | pass |
| P-A-REC-010 | P-09 dependency posture | Candidate-only dependency posture. | No adoption. | Reviews absent. | pass |
| P-A-REC-011 | P-10 validation baseline | Baseline definition. | No validation execution. | Execution/readiness absent. | pass |

## 10. Product Inventory Audit
| product | governance record | current state | activation status | source tracking status | dependency status | validation status | audit verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `omniverse-app` | P-02 | candidate/deferred/local_only/inactive | blocked | blocked | adoption blocked | execution blocked | inactive with blockers |
| `backend-energyplus` | P-03 | candidate/deferred/local_only/inactive | blocked | blocked | adoption blocked | execution blocked | inactive with blockers |
| `cli` | P-04 | candidate/deferred/local_only/inactive | blocked | blocked | adoption blocked | execution blocked | inactive with blockers |
| `desktop` | P-05 | candidate/deferred/local_only/inactive | blocked | blocked | adoption blocked | execution blocked | inactive with blockers |
| `web-platform` | P-06 | candidate/deferred/local_only/inactive | blocked | blocked | adoption blocked | execution blocked | inactive with blockers |
| `experimental` | P-07 | experimental/blocked/local_only/inactive | blocked | blocked | unknown/adoption blocked | disposition-only baseline | blocked sandbox |

## 11. Product Selection Audit
P-00 routed six candidates: five selected for charter drafting and `experimental` selected for disposition review. No activation occurred. No Git, source, dependency, publication, provider/API/MCP/network/auth, validation baseline, or implementation posture changed. Selection remained planning only.

## 12. Common Gate Audit
P-01 defined the common product charter template and GATE-01 through GATE-18. The template is inert. The common gate is not charter acceptance. P-01 created no individual charters, validation baselines, product activation, dependency adoption, Git tracking, publication, or implementation readiness.

## 13. Product Charter Audit
P-02 through P-06 each provide an inactive charter draft. All preserve product/root boundary, record owner gaps or blockers, declare local-only posture, defer Git posture to P-08, defer dependency posture to P-09, defer validation baseline to P-10, keep activation blocked, and keep implementation readiness blocked.

| product | gate status | highest blocker | preserved boundary | audit verdict |
| --- | --- | --- | --- | --- |
| `omniverse-app` | gate_passed_with_cautions_for_charter_review_only | Omniverse/SDK/runtime/license/output | Interface, not backend. | pass_with_caution |
| `backend-energyplus` | gate_passed_with_cautions_for_charter_review_only | EnergyPlus/OpenStudio/native/data | EnergyPlus solver, not internal model. | pass_with_caution |
| `cli` | gate_passed_with_cautions_for_charter_review_only | Command/shell/package/user data | Operator interface, not shell permission. | pass_with_caution |
| `desktop` | gate_passed_with_cautions_for_charter_review_only | Runtime/packaging/local data | Local interface, not backend/runtime approval. | pass_with_caution |
| `web-platform` | gate_passed_with_cautions_for_charter_review_only | Auth/data/build/deploy | Browser interface, not deploy/auth approval. | pass_with_caution |

## 14. Experimental Disposition Audit
P-07 keeps `experimental` outside current product charter drafting. It remains blocked/local-only. No split, archive execution, source inspection, Git posture change, dependency adoption, validation execution, movement, deletion, publication, or activation occurred. Future split, archive, defer, reject, or charter routes remain metadata only.

## 15. Git Posture Audit
P-08 allows product governance docs to be trackable as docs only after exact human instruction. Product source under `2_products/` remains local-only and not trackable now. `.gitignore` is unchanged. No force-add, staging, commit, push, publication, or source tracking approval occurred. Tracking docs does not activate products.

## 16. Dependency / External Source Audit
P-09 adopted no dependency and no external source. No install or execution occurred. External sources remain evidence only. Per-product dependency classes are candidates only. License evidence is not reuse approval. Provider/API/MCP/network/auth remains blocked.

## 17. Validation Baseline Audit
P-10 defined the validation baseline. The baseline is not validation execution. No tests, builds, package managers, products, solvers, dev servers, providers, APIs, MCP, network calls, or installs were run. No product reaches activation readiness, source tracking readiness, dependency adoption readiness, or implementation readiness. P-A proceeds only because explicit instruction was given.

## 18. Security / Local-only Audit
Using S-series, P-08, and P-10: `2_products/` remains local-only; product source was not deeply inspected; secrets and credentials remain excluded; generated outputs remain generated-sensitive; unknown sensitivity blocks use; no local-only material was published; no provider/API/MCP/network/auth activation occurred.

## 19. Product / Root Boundary Audit
Product docs remain product-scoped. Product charters do not define AGENT PLATFORM root authority. Product needs do not decide root architecture or Cognitive Semantic System substrate. Graph remains a candidate only. Siamese product vision informs product context but does not override governance.

## 20. Interface / Backend Boundary Audit
`omniverse-app` is interface, not backend. `backend-energyplus` is an inactive energy-domain backend candidate. `cli` is an operator/scriptable interface, not shell permission. `desktop` is a local interface candidate, not backend or runtime approval. `web-platform` is a browser/deployed interface candidate, not deploy/auth approval. `experimental` overrides no product boundary. Interfaces consume governed backend contracts only.

## 21. Generated Output / Data / Artifact Audit
Generated product outputs are not source by default. Screenshots, logs, reports, datasets, models, caches, solver outputs, CLI outputs, desktop crash reports, web bundles, and USD visual layers remain sensitive until reviewed. No generated output was tracked or published by FASE 4. Output review remains future work.

## 22. Git / Publication Audit
Git state is evidence only. No `git add .`, broad staging, product source tracking, force-add, publication, staging, commit, push, amend, reset, clean, or release occurred. Product governance docs may be staged later only by exact human instruction. P-A does not perform any Git mutation.

## 23. Validation / Proof Audit
Using V-01, V-02, V-04, and V-05: proof levels are evidence posture only. PL-1 through PL-4 support documentation and coherence review. PL-6 remains future-only after exact execution approval. PL-7 applies to this structured P-A audit. Validation did not become approval.

## 24. Audit Finding Model
| severity | meaning | required response | blocks phase closure? | blocks IR-00? |
| --- | --- | --- | --- | --- |
| pass | Expected posture satisfied. | Retain evidence. | No | No |
| pass_with_caution | Satisfied with residual risk. | Carry risk forward. | No | Maybe |
| observation | Relevant fact. | Track if useful. | No | No |
| minor_gap | Non-critical missing detail. | Resolve later. | No | Maybe |
| major_gap | Material readiness gap. | Governed follow-up. | Maybe | Yes |
| blocker | Stop condition. | Resolve before action. | Yes if in P-A inputs | Yes |
| incident | Unsafe or prohibited action. | Stop and escalate. | Yes | Yes |

## 25. Audit Findings Table
| finding_id | area | observation | evidence source | severity | residual risk | required action | closure status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PA-FIND-001 | Coverage | P-00 through P-10 cover FASE 4 sequence. | P-series | pass | None material. | Retain audit. | closed |
| PA-FIND-002 | Product state | Products remain inactive. | P-02..P-07/P-10 | pass | Activation blockers remain. | Future governance. | closed |
| PA-FIND-003 | Local-only | Product source remains local-only. | P-08/P-10/S-series | pass | Enforcement is policy/Git hygiene. | Maintain boundaries. | closed |
| PA-FIND-004 | Git | Product Git posture preserved. | P-08 | pass | Future exact staging needed for docs. | Human exact paths only. | closed |
| PA-FIND-005 | Dependencies | Dependencies remain unadopted. | P-09 | pass | Reviews absent. | Future dependency review. | closed |
| PA-FIND-006 | Validation | Baseline defined but not executed. | P-10/V-04 | pass | Behavior untested. | Future exact validation. | closed |
| PA-FIND-007 | Implementation | No implementation readiness. | P-10/M-A/H-A | major_gap | IR cannot approve implementation yet. | IR-00 assessment only. | open |
| PA-FIND-008 | Experimental | `experimental` remains blocked/local-only. | P-07 | pass_with_caution | Ambiguous material remains. | Future split/archive review. | open |
| PA-FIND-009 | Root/CSS | Product/root and CSS boundary preserved. | CSS-series/P-series | pass | Substrate undecided. | Future CSS governance. | closed |
| PA-FIND-010 | Next phase | IR-00 requires explicit instruction. | P-10/P-A | pass | Scope pressure possible. | Stop before IR-00. | closed |

## 26. Residual Risk Register
| risk_id | residual risk | source | severity | mitigation | owner/route | phase closure impact |
| --- | --- | --- | --- | --- | --- | --- |
| PA-RISK-001 | No active product owners. | P-02..P-07 | high | Assign owners later. | Product governance | Audit-complete with risk. |
| PA-RISK-002 | No activation decisions. | P-series | high | Future activation tickets. | Governance | Blocks activation. |
| PA-RISK-003 | No source tracking approval. | P-08 | high | Exact Git/source review. | Git governance | Blocks source tracking. |
| PA-RISK-004 | No dependency adoption approval. | P-09 | high | Dependency review. | Product/dependency governance | Blocks adoption. |
| PA-RISK-005 | No validation execution. | P-10 | high | Future exact commands. | Validation/security | Blocks behavior proof. |
| PA-RISK-006 | No product security reviews. | S-series/P-10 | high | Product security review. | Security | Blocks activation/IR. |
| PA-RISK-007 | No generated-output reviews. | P-10 | medium-high | Output provenance review. | Product validation | Blocks publication. |
| PA-RISK-008 | No backend/API contracts. | P-03/P-10 | high | Contract governance. | Product architecture | Blocks interfaces. |
| PA-RISK-009 | No implementation readiness. | P-A | high | IR-00 assessment only. | Governance | Blocks implementation. |
| PA-RISK-010 | No product source review. | P-08/P-10 | high | Future scoped product review. | Product governance | Blocks source tracking. |
| PA-RISK-011 | Experimental still ambiguous. | P-07 | medium-high | Split/archive/defer review. | Product/lifecycle | Audit-complete with risk. |
| PA-RISK-012 | No product audit automation. | V-series | medium | Future validation tooling. | Validation | Does not block audit. |
| PA-RISK-013 | IR-00 not started. | Stop rule | none | Await explicit instruction. | Human/governance | Required stop. |

## 27. Blocker Register
| blocker | stop behavior | required future action | blocks P-A? | blocks IR-00? |
| --- | --- | --- | --- | --- |
| Missing P-00 through P-10 | Stop phase audit. | Restore missing artifact. | Yes | Yes |
| Missing V-04/S-series/W-12 | Stop validation/security/product claims. | Restore controls. | Yes | Yes |
| Product source inspection required | Stop P-A. | Future exact product scope. | No | Yes |
| Product activation implied | Stop wording/action. | Activation governance. | Yes | Yes |
| Source tracking implied | Stop Git path. | Source tracking decision. | Yes | Yes |
| Dependency adoption implied | Stop adoption claim. | Dependency governance. | Yes | Yes |
| Validation execution implied | Stop execution. | Exact validation approval. | Yes | Yes |
| Implementation readiness implied | Stop IR claim. | IR-00 assessment. | Yes | Yes |
| Provider/API/MCP activation implied | Stop activation. | Security/governance review. | Yes | Yes |
| Publication implied | Stop publication path. | Publication/security review. | Yes | Yes |
| Git action implied | Stop Git mutation. | Exact human Git instruction. | Yes | Maybe |
| Final CSS substrate decision implied | Stop substrate claim. | Future CSS decision. | Yes | Yes |
| IR-00 scope pressure detected | Stop adjacent work. | Wait explicit IR-00 instruction. | No | No |

## 28. Incident Handling
Incidents include product source inspected deeply; product or external source executed; product test/build/package manager run; dependency installed/adopted; product source staged; `.gitignore` modified; product activated by audit wording; implementation readiness approved by audit wording; provider/API/MCP/network/auth activated; generated output treated as source; secret/credential exposed; or IR-00/next phase started.

Response: STOP, report safe metadata only, do not continue adjacent work, and require human/security/product/governance decision.

## 29. P-A Invariants
| ID | Invariant |
| --- | --- |
| PA-001 | Product workspace audit is not product activation. |
| PA-002 | Audit verdict is not implementation readiness. |
| PA-003 | Audit does not execute validation. |
| PA-004 | Audit does not approve source tracking. |
| PA-005 | Audit does not adopt dependencies. |
| PA-006 | Audit does not publish product material. |
| PA-007 | Product source remains local-only. |
| PA-008 | Product Git posture is not changed. |
| PA-009 | Validation evaluates; governance decides. |
| PA-010 | Graph remains a candidate only. |
| PA-011 | P-A stops before IR-00. |

## 30. Anti-patterns
Anti-patterns: audit as activation; audit as implementation readiness; audit as validation execution; audit as dependency adoption; audit as source tracking approval; audit as publication approval; audit by source inspection; audit by running tests; audit by installing packages; audit hiding residual risks; audit starting IR-00; `git add .`.

## 31. Phase Closure Statement
FASE 4 - Product Workspace Governance may be considered audit-complete at documentation/governance level only if P-00 through P-10 exist, all product candidates have charter/disposition/posture/baseline records, products remain inactive, product source remains local-only, product Git posture remains unchanged, dependencies remain unadopted, validation execution did not occur, no source tracking/publication/activation occurred, residual risks are recorded, and human governance accepts the audit outcome.

Audit-complete does not mean implementation-ready.

## 32. Readiness For IR-00
IR-00 - Platform Implementation Readiness Assessment is ready after explicit instruction only if P-A exists, FASE 4 is audit-complete at documentation level, product activation remains blocked, source tracking remains blocked, dependency adoption remains blocked, validation execution remains blocked, implementation readiness remains unapproved, and IR-00 is scoped as assessment only, not implementation.

Do not create IR-00.

## 33. Final Verdict
| Question | Answer |
| --- | --- |
| What does P-A audit? | The complete FASE 4 product workspace governance phase, P-00 through P-10. |
| Did P-A activate products? | No. |
| Did P-A execute validation tests? | No. |
| Did P-A inspect product source deeply? | No. |
| Did P-A change Git posture? | No. |
| Did P-A adopt dependencies? | No. |
| Did P-A approve source tracking? | No. |
| Did P-A approve implementation readiness? | No. |
| Did P-A start IR-00? | No. |
| What is the audit verdict? | Pass for document-level FASE 4 audit, with continuing blockers and residual risks. |
| What remains blocked? | Product activation, product source tracking, dependency/external adoption, validation execution, implementation readiness, publication, Git mutation, provider/API/MCP/network/auth, and IR-00 start. |
| Is FASE 4 audit-complete? | Yes, at documentation/governance audit level after bounded validation, subject to human governance acceptance. |
| Is IR-00 ready after explicit instruction? | Yes, as assessment only; IR-00 is not started. |

Stop after P-A validation and report. Do not start IR-00 or any later ticket.
