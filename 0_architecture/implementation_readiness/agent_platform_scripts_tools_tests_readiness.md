# IR-03 - Scripts / Tools / Tests Readiness
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Scripts / Tools / Tests Readiness |
| Ticket | IR-03 |
| Status | Accepted scripts / tools / tests readiness assessment |
| Date | 2026-07-02 |
| Scope | Readiness assessment for future scripts, tools, tests, runners, CI, and validation/execution support for AGENT PLATFORM / Siamese after IR-02. |
| Authority | Readiness assessment only, not script/tool/test creation or execution. |
| Related documents | IR-00, IR-01, IR-02, P-A, P-00 through P-10, M-A, W-series, V-series, S-series, CSS-series, H-series, `.gitignore`, `README.md`, Siamese Product Vision |
| Assessment target | Future scripts, tools, tests, runners, CI, and validation/execution support |

## 2. Purpose
IR-00 found the platform not ready for implementation but ready for planning tickets. IR-01 reserved `3_platform` conceptually only. IR-02 defined source tree/tracking policy and did not approve source tracking.

IR-03 assesses scripts/tools/tests readiness. It does not create or execute scripts/tools/tests, create CI, runners, validation registry, or automation, approve source tracking, inspect `3_platform`, or implement anything. IR-03 prepares IR-04 and does not start IR-04.

## 3. Scripts / Tools / Tests Readiness Definition
Scripts/tools/tests readiness is a governance assessment of what future scripts, tools, tests, runners, and automation may be needed, what risks they carry, and what gates must pass before creation, tracking, execution, or publication.

Scripts/tools/tests readiness is not script/tool/test creation. Scripts/tools/tests readiness is not execution approval. Readiness is not validation pass, source tracking approval, dependency adoption, implementation, product activation, provider/API/MCP activation, or CI approval.

## 4. Decision Summary
No scripts are created. No tools are created. No tests are created. No CI/runners/automation are created. No scripts/tools/tests are executed. No source tracking is approved. No `3_platform` contents are inspected or approved. Scripts/tools/tests source is not trackable now.

Governance docs under `0_architecture/implementation_readiness/` remain trackable as docs only by exact path and human instruction. Future scripts/tools/tests require IR-03 gates, IR-04 dependency readiness, IR-08 validation/security enforcement readiness, and explicit governance.

## 5. Authority Boundary
| Layer | IR-03 boundary |
| --- | --- |
| Governance | Decides script/tool/test creation, tracking, execution, CI, automation, publication, exceptions, implementation, and lifecycle. |
| Validation | Evaluates evidence and future test results. |
| Security | Constrains execution, local-only material, secrets, credentials, generated outputs, network, providers, APIs, MCP, auth, and publication. |
| IR-03 | Assesses readiness only. |
| Git | Records artifacts but does not approve scripts/tools/tests. |
| Agents | May prepare safe readiness metadata but cannot create, execute, activate, adopt, stage, commit, push, publish, or start IR-04. |

## 6. Source Boundary
IR-02 controls source tree/tracking posture. IR-01 controls `3_platform` conceptual reservation. IR-00 controls implementation readiness assessment. P-08 controls product Git posture. P-09 controls dependency/external posture. P-10 controls validation baseline posture. V-series controls proof/evidence/validation posture. S-series controls execution/security/local-only posture. H-series controls runtime/tool/provider/MCP boundaries. CSS-series controls naming/substrate boundary.

Raw `3_platform` contents are not inspected. Raw `2_products/` and `4_external/sources/` are not inspected. Safe metadata only.

## 7. Current Readiness Posture
| area | current posture | readiness status | blocked action | future route |
| --- | --- | --- | --- | --- |
| script creation | No script target approved. | blocked_not_created | Create scripts. | IR-03 gate + later governance. |
| tool creation | No tool target approved. | blocked_not_created | Create/adopt tools. | IR-04/IR-08. |
| test creation | No test target approved. | blocked_not_created | Create tests. | IR-03 gate + IR-08. |
| CI/runners | No runner approved. | blocked_not_created | Create CI/runners. | CI gate. |
| validation registry | Architecture only. | planning_only | Build registry. | IR-08. |
| security enforcement checks | Policy only. | planning_only | Build enforcement. | IR-08. |
| source tracking | Not approved. | blocked_not_trackable_now | Stage/track source. | IR-02 future gate. |
| test execution | No command approved. | blocked_not_executed | Run tests. | Execution approval gate. |
| build execution | No command approved. | blocked_not_executed | Run builds. | IR-04/IR-08. |
| package manager execution | No dependency review. | blocked_not_executed | Install/run package manager. | IR-04. |
| provider/API/MCP/network checks | Activation blocked. | blocked_not_executed | Calls/auth/MCP. | IR-05/IR-06. |
| product behavior checks | Products inactive. | blocked_not_executed | Product tests/runs. | Product governance. |
| generated-output handling | Policy only. | planning_only | Retain/publish outputs. | IR-08. |
| `3_platform` contents | Unknown/uninspected. | blocked_not_trackable_now | Inspect/classify/use. | Future classification. |

## 8. Script / Tool / Test Category Catalog
| category | meaning | current status | required future gate | blocked now |
| --- | --- | --- | --- | --- |
| governance_check_script | Checks governance docs. | conceptual_only | Script gate. | Create/run. |
| path_hygiene_check_script | Checks paths/allowed roots. | conceptual_only | Script gate. | Create/run. |
| git_status_check_script | Wraps Git status checks. | conceptual_only | Script gate/Git approval. | Create/run/stage. |
| check_ignore_script | Checks ignore posture. | conceptual_only | Script gate. | Create/run. |
| documentation_lint_script | Checks docs formatting. | conceptual_only | Script gate. | Create/run. |
| security_scan_tool | Scans security posture. | conceptual_only | Tool gate/IR-08. | Adopt/run. |
| secret_scan_tool | Detects secrets safely. | conceptual_only | Tool gate/IR-08. | Adopt/run. |
| dependency_review_tool | Reviews dependencies. | conceptual_only | IR-04/tool gate. | Adopt/run. |
| license_notice_check_tool | Reviews license/notice. | conceptual_only | IR-04/tool gate. | Adopt/run. |
| validation_registry_tool | Manages validation evidence. | conceptual_only | IR-08. | Create/run. |
| proof_evidence_check_tool | Checks proof/evidence records. | conceptual_only | IR-08. | Create/run. |
| unit_test | Tests isolated code. | conceptual_only | Test gate/I-00. | Create/run. |
| smoke_test | Checks basic startup. | conceptual_only | Test/execution gate. | Create/run. |
| integration_test | Tests components together. | conceptual_only | Test/execution gate. | Create/run. |
| end_to_end_test | Tests whole flow. | conceptual_only | Test/execution gate. | Create/run. |
| solver_test | Tests EnergyPlus/OpenStudio route. | conceptual_only | Product/IR-04 gates. | Execute solver. |
| UI_test | Tests web/desktop/Omniverse UI. | conceptual_only | Product/runtime gates. | Run UI. |
| API_contract_test | Tests backend/API contracts. | conceptual_only | IR-05/IR-06. | Call APIs. |
| provider_adapter_test | Tests providers/adapters. | conceptual_only | IR-06. | Provider calls. |
| MCP_tool_test | Tests MCP tools. | conceptual_only | IR-06. | MCP activation. |
| performance_test | Measures runtime performance. | conceptual_only | Execution gate. | Run workload. |
| generated_output_check | Reviews outputs/artifacts. | conceptual_only | IR-08. | Treat output as source. |
| data_fixture_check | Checks fixtures/sample data. | conceptual_only | Test gate/security. | Use data. |
| CI_runner | Automated CI runner. | conceptual_only | CI/runner gate. | Create/activate. |
| local_runner | Local task runner. | conceptual_only | CI/runner gate. | Create/activate. |

## 9. Current Trackable / Non-trackable Posture
Using IR-02, trackable now means IR governance docs under `0_architecture/implementation_readiness/` only, exact path and human instruction.

Not trackable now: `scripts/**`, `tools/**`, `tests/**`, CI/runners, automation source, validation registry source, security enforcement source, `3_platform/**`, product source, package manifests from unapproved source, generated outputs, runtime outputs, secrets/credentials, dependency folders, and raw external sources.

## 10. Script Creation Gate
Before any script may be created: script purpose, owner, exact path, source tracking posture, dependency/runtime posture, input/output behavior, generated-output handling, local-only/security review, secret/credential handling, network/provider/API/MCP behavior, dry-run/no-side-effect posture where possible, rollback/removal path, validation criterion, and governance approval must be declared.

IR-03 does not pass this gate.

## 11. Tool Creation Gate
Before any tool may be created or adopted: tool class, owner, exact path/source, dependency/runtime/native/package posture, license/provenance, execution side effects, network/auth/provider/MCP behavior, data/output handling, security posture, validation method, rollback/removal path, and governance approval must be declared.

IR-03 does not pass this gate.

## 12. Test Creation Gate
Before any test may be created: test target, product/platform scope, proof level target, fixture/data posture, dependency/runtime posture, command/execution posture, expected output, generated-output handling, local-only/security review, exact path, and governance approval must be declared.

IR-03 does not pass this gate.

## 13. Execution Approval Gate
Before any script/tool/test may be executed: exact command, working directory, purpose, expected output, side effects, files read/written, dependency/runtime/package posture, network/auth/provider/MCP behavior, secret/credential exposure risk, generated-output storage, cleanup/rollback, timeout, failure behavior, and human approval must be recorded.

IR-03 does not pass this gate.

## 14. CI / Runner / Automation Gate
Before CI, runners, scheduled tasks, hooks, pre-commit, GitHub Actions, local watchers, or automation may be created or activated: trigger, permissions, secrets/credentials posture, network/provider behavior, dependency install behavior, artifact/log retention, branch/publication behavior, failure behavior, security review, and governance approval must be recorded.

IR-03 does not pass this gate.

## 15. Validation / Proof Relationship
Using V-series and P-10: tests are evidence producers, not approval. Passing tests does not activate products. PL-6 requires exact future execution approval. PL-7/PL-8 audit/reproduction remain future. IR-03 defines readiness only. No validation registry or automation is created. Validation evaluates; governance decides.

## 16. Security / Local-only Relationship
Using S-series: scripts/tools/tests can expose secrets, credentials, paths, local data, generated outputs, product source, sensor/building data, package registry auth, provider tokens, and environment variables. Unknown sensitivity blocks creation and execution. Local-only means no default publication. No secret/credential values may be read, copied, summarized, logged, or retained. Execution is blocked without exact approval.

## 17. Git / .gitignore Relationship
Using IR-02: IR-03 does not modify `.gitignore`. Scripts/tools/tests are not trackable now. Future tracking requires exact paths and governance. No force-add is authorized. No staging, commit, push, or publication occurs. Do not use `git add .`. Git status is evidence only.

## 18. Dependency / Package Relationship
Using P-09 and the IR-04 route: scripts/tools/tests often imply dependencies. Dependency manifests are not adoption approval. Lockfiles are not approval. Package manager execution is blocked. Native binaries/tools are blocked. Dependency readiness is deferred to IR-04. IR-03 does not install or adopt anything.

## 19. Runtime / Provider / MCP Relationship
Using H-series: tool availability is not permission. Provider credentials are not provider permission. MCP availability is not MCP activation. Scripts/tools/tests must not activate providers, adapters, MCP, APIs, auth, network, hooks, skills, agents, or runtime behavior. Readiness for these routes is deferred to IR-05 and IR-06.

## 20. Product Relationship
Product behavior tests are not approved. Product source remains local-only. Products remain inactive. Product tests cannot be created or run by IR-03. EnergyPlus/OpenStudio/Omniverse/web/desktop/CLI tests are future only after exact gates. Product activation remains blocked.

Siamese is a living energy twin platform for buildings. `omniverse-app` is visual/interface, not backend. `backend-energyplus` is an inactive energy-domain backend candidate. EnergyPlus remains solver, not internal model. `cli`, `desktop`, and `web-platform` are interface candidates only. `experimental` remains blocked/local-only.

## 21. 3_platform Relationship
`3_platform` remains reserved conceptually only. Existing 3_platform contents remain uninspected and unapproved. Scripts/tools/tests must not be inferred from `3_platform` contents. No `3_platform` source, scripts, tools, tests, runners, or automation are approved or tracked by IR-03.

## 22. Cognitive Semantic System Relationship
Cognitive Semantic System is the accepted name. Substrate remains undecided. Graph remains a candidate only. Graphify remains evidence/historical/external/prohibited/candidate-evidence only, not authority. CSS prototype tests/tools are not approved. CSS substrate gate is deferred to IR-07.

## 23. Readiness Status Model
Statuses: `readiness_documented`, `creation_not_approved`, `execution_not_approved`, `tracking_not_approved`, `dependency_review_pending`, `security_review_pending`, `validation_registry_pending`, `CI_runner_pending`, `provider_MCP_review_pending`, `source_tree_pending`, `implementation_not_started`, `rejected_for_creation_now`, and `rejected_for_execution_now`.

Current status: `readiness_documented` + `creation_not_approved` + `execution_not_approved` + `tracking_not_approved` + `dependency_review_pending` + `security_review_pending`.

## 24. Readiness Gate Model
| gate | pass condition | current posture | blocker if missing |
| --- | --- | --- | --- |
| IR03-G01 IR-02 exists | Source tracking policy exists. | Pass pending validation. | Cannot assess readiness. |
| IR03-G02 source tracking remains blocked | No source approval. | Pass. | Tracking drift. |
| IR03-G03 no scripts/tools/tests created | None created by IR-03. | Pass. | Creation incident. |
| IR03-G04 no execution occurred | No scripts/tests/builds run. | Pass. | Execution incident. |
| IR03-G05 `.gitignore` unchanged | No edit. | Pass. | Git posture drift. |
| IR03-G06 dependency posture preserved | No adoption/install. | Pass. | Supply-chain drift. |
| IR03-G07 security/local-only posture preserved | No exposure/execution. | Pass. | Security drift. |
| IR03-G08 validation proof posture preserved | No test pass claimed. | Pass. | Proof inflation. |
| IR03-G09 `3_platform` contents uninspected/unapproved | No deep inspection. | Pass. | Content approval drift. |
| IR03-G10 IR-04 next scope declared | IR-04 named but not started. | Pass. | Next-ticket drift. |

## 25. Residual Risk Register
| risk_id | residual risk | source | severity | mitigation | route | blocks implementation? |
| --- | --- | --- | --- | --- | --- | --- |
| IR03-RISK-001 | No scripts exist/approved. | IR-03 | medium-high | Future script gate. | Later governance | Yes |
| IR03-RISK-002 | No tools exist/approved. | IR-03 | medium-high | Future tool gate. | IR-04/IR-08 | Yes |
| IR03-RISK-003 | No tests exist/approved. | IR-03 | high | Future test gate. | IR-08/I-00 | Yes |
| IR03-RISK-004 | No CI/runners approved. | IR-03 | medium-high | CI gate. | IR-08 | Yes |
| IR03-RISK-005 | No validation registry. | V-series | high | Registry readiness. | IR-08 | Yes |
| IR03-RISK-006 | No execution approval gate executed. | S-series | high | Exact approval. | Future execution | Yes |
| IR03-RISK-007 | Dependency readiness absent. | P-09 | high | Dependency review. | IR-04 | Yes |
| IR03-RISK-008 | Security enforcement absent. | S-series | high | Enforcement readiness. | IR-08 | Yes |
| IR03-RISK-009 | Generated-output handling not implemented. | V/S-series | high | Output policy implementation. | IR-08 | Yes |
| IR03-RISK-010 | Product behavior untested. | P-10 | high | Product validation later. | Product governance | Yes |
| IR03-RISK-011 | Source tracking blocked. | IR-02 | high | Future tracking gate. | IR-02/I-00 | Yes |
| IR03-RISK-012 | Existing `3_platform` contents unknown. | IR-01/IR-02 | high | Classification governance. | Future ticket | Yes |
| IR03-RISK-013 | Provider/API/MCP behavior unreviewed. | H-series | high | Readiness review. | IR-06 | Yes |
| IR03-RISK-014 | CSS substrate undecided. | CSS-series | high | Substrate gate. | IR-07 | Yes |

## 26. Blocker Register
| blocker | stop behavior | required future action | blocks IR-03? | blocks implementation? |
| --- | --- | --- | --- | --- |
| Missing IR-02 | Stop. | Restore/create IR-02. | Yes | Yes |
| Missing V/S/H controls | Stop readiness claim. | Restore controls. | Yes | Yes |
| Need to create scripts/tools/tests | Stop. | Future creation gate. | Yes | Yes |
| Need to execute scripts/tools/tests | Stop. | Execution approval gate. | Yes | Yes |
| Need to run package manager | Stop. | IR-04 and execution approval. | Yes | Yes |
| Need to inspect `3_platform` contents | Stop. | Future classification ticket. | No | Yes |
| Source tracking implied | Stop. | Future source tracking gate. | Yes | Yes |
| `.gitignore` modification implied | Stop. | Separate Git/security governance. | Yes | Maybe |
| Dependency adoption implied | Stop. | IR-04. | Yes | Yes |
| Product activation implied | Stop. | Product governance. | Yes | Yes |
| Provider/API/MCP activation implied | Stop. | IR-06/security review. | Yes | Yes |
| Validation pass implied | Stop. | Future execution/evidence review. | Yes | Yes |
| CI/runner creation implied | Stop. | CI/runner gate. | Yes | Yes |
| CSS substrate decision implied | Stop. | IR-07. | Yes | Yes |
| Git action implied | Stop. | Exact human Git instruction. | Yes | Maybe |
| IR-04 scope pressure detected | Stop adjacent work. | Wait explicit IR-04 instruction. | No | No |
| I-00 scope pressure detected | Stop adjacent work. | Wait future implementation approval. | No | No |

## 27. Incident Handling
Incidents include scripts/tools/tests created; scripts/tools/tests executed; CI/runners/hooks created or activated; package manager run; dependency installed/adopted; product tests run; provider/API/MCP/network/auth activated; `3_platform` contents inspected; source files staged/tracked; `.gitignore` modified; validation pass claimed; product activated by test wording; final Cognitive Semantic System substrate selected; Git staging/commit/push attempted; or IR-04/I-00 started.

Response: STOP, report safe metadata only, do not continue adjacent work, and require human/security/governance decision.

## 28. IR-03 Invariants
| ID | Invariant |
| --- | --- |
| IR03-001 | Scripts/tools/tests readiness is not script/tool/test creation. |
| IR03-002 | Scripts/tools/tests readiness is not execution approval. |
| IR03-003 | No scripts, tools, tests, CI, runners, or automation are created. |
| IR03-004 | No scripts, tools, tests, builds, package managers, or products are executed. |
| IR03-005 | Source tracking is not approved. |
| IR03-006 | Existing 3_platform contents remain uninspected and unapproved. |
| IR03-007 | Product source remains local-only. |
| IR03-008 | Product Git posture is not changed. |
| IR03-009 | `.gitignore` is not modified. |
| IR03-010 | Dependencies remain unadopted. |
| IR03-011 | Provider/API/MCP activation remains blocked. |
| IR03-012 | Cognitive Semantic System substrate remains undecided. |
| IR03-013 | Graph remains a candidate only. |
| IR03-014 | Validation evaluates; governance decides. |
| IR03-015 | IR-03 stops before IR-04. |

## 29. Anti-patterns
Anti-patterns: readiness as creation; readiness as execution approval; tests as product activation; passing tests as governance approval; script existence as permission; tool availability as permission; package manager run by curiosity; CI by convenience; pre-commit hook by cleanup pressure; source tracking by test need; generated output as source; product behavior inferred from charter; `3_platform` contents inferred as test inventory; starting IR-04 inside IR-03; starting I-00 inside IR-03; `git add .`.

## 30. Readiness For IR-04
IR-04 - Package / SDK / Dependency Readiness is ready after explicit instruction if IR-03 scripts/tools/tests readiness exists, no scripts/tools/tests were created, no scripts/tools/tests were executed, no package manager was run, dependencies remain unadopted, source tracking remains not approved, `3_platform` contents remain uninspected and unapproved, and no product activation, provider/API/MCP activation, CSS substrate decision, publication, Git mutation, or implementation is implied.

Do not create IR-04.

## 31. Final Verdict
| Question | Answer |
| --- | --- |
| What does IR-03 assess? | Readiness gates, risks, and blockers for future scripts, tools, tests, runners, CI, and automation. |
| Were scripts created? | No. |
| Were tools created? | No. |
| Were tests created? | No. |
| Were CI/runners/automation created? | No. |
| Were scripts/tools/tests executed? | No. |
| Was source tracking approved? | No. |
| Were existing `3_platform` contents inspected or approved? | No. |
| Was `.gitignore` modified? | No. |
| Were products activated? | No. |
| Were dependencies adopted? | No. |
| Were providers/API/MCP activated? | No. |
| Was CSS substrate decided? | No. |
| What remains blocked? | Script/tool/test creation and execution, CI/runners/automation, validation registry, security enforcement, source tracking, source tree/skeleton creation, `3_platform` inspection/approval, product activation, dependency adoption, provider/API/MCP activation, CSS substrate decision, publication, Git mutation, IR-04 execution, and I-00. |
| Is IR-04 ready after explicit instruction? | Yes, as package/SDK/dependency readiness only; IR-04 is not started. |

Stop after IR-03 validation and report. Do not start IR-04 or any later ticket.
