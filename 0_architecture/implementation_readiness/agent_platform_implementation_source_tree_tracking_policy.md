# IR-02 - Implementation Source Tree / Tracking Policy
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Implementation Source Tree / Tracking Policy |
| Ticket | IR-02 |
| Status | Accepted implementation source tree / tracking policy |
| Date | 2026-07-01 |
| Scope | Source tree and tracking posture for future AGENT PLATFORM / Siamese implementation planning after IR-01. |
| Authority | Source tree / tracking policy only, not source tracking approval. |
| Related documents | IR-00, IR-01, P-A, P-00 through P-10, M-A, W-series, V-series, S-series, CSS-series, H-series, `.gitignore`, `README.md`, Siamese Product Vision |
| Policy target | Future `3_platform` source tree and tracking posture |

## 2. Purpose
IR-00 found the platform not ready for implementation but ready for planning tickets. IR-01 reserved `3_platform` conceptually only and did not approve existing `3_platform` contents.

IR-02 defines source tree and tracking policy. It does not approve current source tracking, inspect or classify `3_platform` contents, create a source tree or skeleton, implement anything, activate products, adopt dependencies, execute validation, mutate Git, or modify `.gitignore`. IR-02 prepares IR-03 and does not start IR-03.

## 3. Implementation Source Tree / Tracking Policy Definition
An implementation source tree / tracking policy is a governance policy that defines which implementation-related paths may be considered for future tracking, which paths remain blocked, what evidence must exist before tracking, and what Git operations are forbidden until later exact approval.

Implementation source tree / tracking policy is not implementation. Policy is not source tree creation, source tracking approval, approval of existing contents, product activation, dependency adoption, validation execution, Git mutation, or `.gitignore` modification.

## 4. Policy Decision Summary
Trackable now: governance documentation under `0_architecture/implementation_readiness/` only, by exact path and human instruction.

Not trackable now: `3_platform` contents, product source, generated outputs, dependency folders, package manifests from unapproved source, tests/scripts/tools source, runtime source, providers/adapters/MCP, validation registry, security enforcement, Cognitive Semantic System prototype, local-only material, secrets, credentials, datasets, models, artifacts, and raw external sources.

`3_platform` remains reserved conceptually only. Existing `3_platform` contents remain unapproved, uninspected, unclassified, untracked, inactive, and non-authoritative. Source tracking is not approved now. Source tree creation is not approved now. `.gitignore` remains unchanged. IR-03 may assess scripts/tools/tests readiness only after explicit instruction.

## 5. Authority Boundary
| Layer | IR-02 boundary |
| --- | --- |
| Governance | Decides source tracking, source tree creation, exceptions, product activation, dependency adoption, publication, implementation, and lifecycle. |
| Validation | Evaluates tracking/readiness evidence; it does not approve tracking or implementation. |
| Security | Constrains local-only content, secrets, credentials, generated outputs, execution, providers, APIs, MCP, network/auth, and publication. |
| IR-02 | Defines policy only. |
| Git | Records artifacts but does not approve source status. |
| Agents | May prepare safe policy metadata but cannot inspect, implement, execute, activate, adopt, stage, commit, push, publish, or start IR-03. |

## 6. Source Boundary
IR-01 is the primary structure decision input. IR-00 is the readiness assessment input. P-08 controls product Git posture. P-09 controls dependency/external posture. P-10 controls validation baseline posture. P-A closes product workspace governance. W/V/S/H/CSS-series constrain workspace, validation, security, runtime, providers, tools, and substrate.

Raw `3_platform` contents are not inspected. Raw `2_products/` and `4_external/sources/` are not inspected. Safe metadata only.

## 7. Current Path Posture Table
| path or path class | current posture | trackable now? | allowed use | blocked use | future route |
| --- | --- | --- | --- | --- | --- |
| `0_architecture/implementation_readiness/` | IR governance docs. | Yes, docs only by exact instruction. | Read/write named IR docs. | Source approval. | Future IR docs. |
| `0_architecture/product_workspaces/` | Product governance docs. | Docs-only posture already defined. | Product governance evidence. | Product source approval. | Product governance. |
| `3_platform/` | Reserved conceptually; contents unknown. | No. | `Test-Path` existence metadata only. | Inspect, classify, track, approve, edit. | Future gates. |
| `2_products/` | Product source local-only. | No. | Safe metadata from docs only. | Product source tracking/copy. | Product governance. |
| `4_external/sources/` | Raw external sources local-only. | No. | Registry/review metadata only. | Raw source tracking/reuse. | External review. |
| `previusknowledge/` | Previous corpus local-only. | No. | Migration metadata only. | Wholesale staging/copying. | Migration governance. |
| `7_datasets/` | Dataset local-only. | No. | Metadata only after scope. | Tracking/use/publish. | Data review. |
| `8_models/` | Model local-only. | No. | Metadata only after scope. | Tracking/use/publish. | Model review. |
| `9_artifacts/` | Generated artifacts local-only. | No. | Evidence metadata if scoped. | Tracking as source. | Validation/security review. |
| `secrets/` | Secret material. | No. | None. | Read values, stage, publish. | Stop/security. |
| `credentials/` | Credential material. | No. | None. | Read/use/stage/publish. | Stop/security. |
| generated outputs / build outputs / caches | Generated-sensitive. | No. | Metadata only if scoped. | Tracking as source. | Output review. |
| dependency folders | Dependency/runtime material. | No. | Risk metadata only. | Track/adopt/install. | IR-04. |
| `.gitignore` | Current ignore evidence. | Not changed by IR-02. | Read as control. | Edit as shortcut. | Separate governance. |
| `README.md` | Root descriptor. | Unchanged unless separate exact governance. | Descriptor evidence. | Scope expansion. | Docs governance. |

## 8. 3_platform Tracking Posture
`3_platform` is the reserved future platform implementation root candidate. Its contents are not approved, not inspected, not trackable now, and not source by proximity. IR-02 creates no `3_platform` source tree.

`3_platform` source tracking is blocked pending future gates. Existing presence is evidence only, not approval. Any existing content remains quarantined by policy until exact classification governance.

## 9. Existing Content Classification Policy
Existing `3_platform` content cannot be inspected, reused, moved, deleted, staged, committed, copied, normalized, archived, transformed, or approved until a future exact classification ticket declares exact path scope, owner, purpose, source/provenance, sensitivity/security posture, generated-output risk, dependency/package risk, product-source contamination risk, secret/credential risk, license/provenance posture, Git/include-exclude posture, rollback/removal path, and governance decision.

IR-02 does not perform classification.

## 10. Future Source Tree Tracking Gate
Before any `3_platform` source tracking: IR-01 exists; IR-02 policy exists; exact path list exists; owner exists; purpose exists; source type is declared; provenance is declared; local-only/security review exists; secret/credential exclusion plan exists; generated-output exclusion plan exists; dependency/package manifest posture exists; validation plan exists; `.gitignore` impact is reviewed; include/exclude rules are declared; rollback/removal plan is declared; human governance approval exists.

IR-02 does not pass this gate.

## 11. Future Source Tree Creation Gate
Before creating any implementation source tree: IR-02 exists; IR-03 scripts/tools/tests readiness is assessed; IR-04 package/dependency readiness is assessed; IR-05 runtime/agent/context boundaries are assessed; IR-06 provider/adapter/MCP readiness is assessed; IR-07 CSS substrate gate is resolved or explicitly deferred; IR-08 validation/security enforcement readiness is assessed; IR-A audit is completed or explicit governance exception exists; I-00 exact skeleton scope is declared; exact paths are declared; no local-only leakage occurs; governance approval is recorded.

IR-02 does not pass this gate.

## 12. Trackable Now
Current trackable material means governance documentation only and eligibility for future exact-path staging after explicit human instruction. It does not approve source or implementation.

Trackable-now docs: `0_architecture/implementation_readiness/agent_platform_platform_implementation_readiness_assessment.md`, `0_architecture/implementation_readiness/agent_platform_3_platform_structure_decision.md`, `0_architecture/implementation_readiness/agent_platform_implementation_source_tree_tracking_policy.md`, and future IR-series governance docs under `0_architecture/implementation_readiness/` after exact instruction.

## 13. Not Trackable Now
Current non-trackable material: `3_platform/**`, `2_products/**`, product source, existing unclassified `3_platform` contents, generated outputs, build outputs, caches, logs, reports, screenshots, datasets, models, artifacts, package folders, dependency/vendor folders, native binaries, installers, deployment bundles, local sessions, secrets, credentials, tokens, auth material, raw external sources, previous knowledge corpus, validation outputs, and runtime outputs.

## 14. Conditional Future Tracking Categories
| category | example future path class | current status | required future gate | special blockers |
| --- | --- | --- | --- | --- |
| platform source | `3_platform/<core>` | blocked_not_trackable_now | IR-02 gate + I-00 | Owner/provenance. |
| validation registry source | registry code | blocked_not_trackable_now | IR-08 | Registry/enforcement gap. |
| security enforcement source | policy/runtime guards | blocked_not_trackable_now | IR-08 | Enforcement design absent. |
| context runtime source | context runtime | blocked_not_trackable_now | IR-05 | Runtime boundary. |
| provider/adapter source | adapters/providers | blocked_not_trackable_now | IR-06 | Provider/API/MCP activation. |
| agent runtime source | agents/handoff | blocked_not_trackable_now | IR-05 | Autonomy/security. |
| tool execution source | tool boundary | blocked_not_trackable_now | IR-03/IR-05 | Execution risk. |
| CSS prototype source | CSS prototype | blocked_not_trackable_now | IR-07 | Substrate undecided. |
| schemas/contracts | contracts/schemas | blocked_not_trackable_now | IR-08/I-00 | Authority/versioning. |
| tests | test source | blocked_not_trackable_now | IR-03/IR-08 | Execution approval. |
| scripts/tools | automation source | blocked_not_trackable_now | IR-03 | Tool safety. |
| package manifests | package files | blocked_not_trackable_now | IR-04 | Adoption confusion. |
| lockfiles | lock records | blocked_not_trackable_now | IR-04 | Transitive review. |
| fixtures/sample data | sample inputs | blocked_not_trackable_now | IR-03/IR-08 | Sensitivity/license. |
| documentation stubs | implementation docs | blocked_not_trackable_now | Later exact ticket | Implementation implication. |

## 15. .gitignore Policy
IR-02 does not modify `.gitignore`. Current ignore posture remains evidence only. `.gitignore` does not equal security. `.gitignore is not modified` by IR-02. `3_platform` tracking, if ever approved, may require future `.gitignore` impact review. Any `.gitignore` change requires separate exact governance. No force-add is authorized. Do not use `git add .`.

## 16. Git Operation Rules
Before any human Git action, run `git status --short`. Use exact paths only. Never use `git add .`. Never force-add ignored/local-only material without explicit governance. Never stage unclassified `3_platform` contents, `2_products/`, raw external sources, secrets, credentials, generated outputs, or dependency folders. Never commit wording that implies implementation started. Push/publication requires explicit human intent.

## 17. Product Source Separation Policy
`3_platform` is not `2_products/`. Product source remains local-only. Product charters do not become source. Product workspaces must not be copied into `3_platform`. Siamese product requirements may inform future platform requirements only through governance docs. Product activation and product source tracking remain blocked.

Siamese is a living energy twin platform for buildings. `omniverse-app` is visual/interface, not backend. `backend-energyplus` is an inactive energy-domain backend candidate. EnergyPlus remains solver, not internal model. `cli`, `desktop`, and `web-platform` are interface candidates only. `experimental` remains blocked/local-only.

## 18. Dependency Manifest Policy
Dependency manifests are not dependency adoption approval. Lockfiles are not dependency approval. Existing manifests under unapproved source are not trackable now. Package/runtime/SDK/native/provider/API/MCP/network/auth use remains blocked. Dependency readiness is deferred to IR-04. Any future manifest tracking requires license, provenance, security, package-script, and transitive review.

## 19. Generated Output / Data / Artifact Policy
Generated output is not source by default. Outputs, logs, reports, datasets, models, artifacts, caches, screenshots, solver outputs, USD layers, web bundles, crash reports, CLI stdout/stderr, validation outputs, and local databases remain blocked until reviewed. Sample/fixture data requires provenance, sensitivity, license, storage, retention, and exact-path approval.

## 20. Validation / Scripts / Tools / Tests Relationship
IR-02 does not create tests, scripts, tools, CI, runners, validation registry, or automation. Scripts/tools/tests readiness is deferred to IR-03. Test/build/run execution remains blocked. Future test/source tracking requires IR-03 and IR-08 posture plus exact path governance.

## 21. Runtime / Provider / MCP Relationship
IR-02 does not activate runtime, providers, adapters, tools, hooks, skills, agents, or MCP. Tool availability is not permission. Provider credentials are not provider permission. MCP availability is not MCP activation. Runtime/provider readiness is deferred to IR-05 and IR-06.

## 22. Cognitive Semantic System Relationship
Cognitive Semantic System is the accepted name. Substrate remains undecided. Graph remains a candidate only. Graphify remains evidence/historical/external/prohibited/candidate-evidence only, not authority. `3_platform` tracking policy does not imply a Cognitive Semantic System prototype. The CSS substrate gate is deferred to IR-07.

## 23. Source Tracking Status Model
Statuses: `docs_trackable_exact_path_only`, `source_tracking_not_approved`, `source_tree_not_created`, `existing_content_unclassified`, `existing_content_quarantined`, `local_only_blocked`, `generated_output_blocked`, `dependency_manifest_blocked`, `pending_IR03_scripts_tools_tests`, `pending_IR04_dependency_readiness`, `pending_IR08_validation_security`, `pending_IRA_audit`, and `rejected_for_tracking_now`.

Current status: `docs_trackable_exact_path_only` + `source_tracking_not_approved` + `existing_content_unclassified` + `existing_content_quarantined` + `source_tree_not_created`.

## 24. Readiness Gate Model
| gate | pass condition | current posture | blocker if missing |
| --- | --- | --- | --- |
| IR02-G01 IR-01 exists | Structure decision accepted. | Pass pending validation. | Cannot define policy. |
| IR02-G02 IR-00 exists | Readiness assessment accepted. | Pass pending validation. | Missing readiness input. |
| IR02-G03 `3_platform` reserved conceptually | Name reserved only. | Pass. | Structure ambiguity. |
| IR02-G04 existing contents unapproved/uninspected | No content inspection/approval. | Pass. | Approval by implication. |
| IR02-G05 docs-only tracking declared | IR docs only by exact path. | Pass. | Git ambiguity. |
| IR02-G06 source tracking blocked | No source approval. | Pass. | Tracking drift. |
| IR02-G07 `.gitignore` unchanged | No edit. | Pass. | Local-only drift. |
| IR02-G08 local-only roots preserved | Ignored/local-only roots remain blocked. | Pass. | Exposure risk. |
| IR02-G09 dependency posture preserved | No adoption. | Pass. | Supply-chain drift. |
| IR02-G10 validation/security posture preserved | No execution/enforcement. | Pass. | Unsafe readiness. |
| IR02-G11 IR-03 next scope declared | IR-03 named but not started. | Pass. | Next-ticket drift. |

## 25. Residual Risk Register
| risk_id | residual risk | source | severity | mitigation | route | blocks implementation? |
| --- | --- | --- | --- | --- | --- | --- |
| IR02-RISK-001 | Existing `3_platform` contents unknown. | IR-01/IR-02 | high | Keep quarantined. | Classification ticket | Yes |
| IR02-RISK-002 | Source tracking policy not yet executable. | IR-02 | high | Future exact approval. | IR-02 gate | Yes |
| IR02-RISK-003 | Content classification absent. | IR-01 | high | Classification governance. | Future ticket | Yes |
| IR02-RISK-004 | Secrets/credentials risk unknown. | S-series | high | Security review. | IR-08 | Yes |
| IR02-RISK-005 | Generated-output contamination risk. | V/S-series | high | Output review. | IR-08 | Yes |
| IR02-RISK-006 | Dependency manifest risk. | P-09 | high | Dependency review. | IR-04 | Yes |
| IR02-RISK-007 | Product source contamination risk. | P-08/P-A | high | Product separation. | Product governance | Yes |
| IR02-RISK-008 | `.gitignore` impact unknown. | P-08 | medium-high | Impact review. | Future Git governance | Yes |
| IR02-RISK-009 | Exact include/exclude list absent. | IR-02 | high | Exact path list. | Tracking gate | Yes |
| IR02-RISK-010 | Source owner absent. | IR-02 | high | Declare owner. | Tracking gate | Yes |
| IR02-RISK-011 | Validation/security enforcement absent. | V/S-series | high | IR-08. | IR-08 | Yes |
| IR02-RISK-012 | Script/test/tool readiness absent. | IR-02 | high | IR-03. | IR-03 | Yes |
| IR02-RISK-013 | Dependency readiness absent. | P-09 | high | IR-04. | IR-04 | Yes |
| IR02-RISK-014 | Runtime/provider readiness absent. | H-series | high | IR-05/IR-06. | IR-05/IR-06 | Yes |
| IR02-RISK-015 | CSS substrate undecided. | CSS-series | high | IR-07. | IR-07 | Yes |

## 26. Blocker Register
| blocker | stop behavior | required future action | blocks IR-02? | blocks implementation? |
| --- | --- | --- | --- | --- |
| Missing IR-01 | Stop. | Restore/create IR-01. | Yes | Yes |
| Missing IR-00 | Stop. | Restore IR-00. | Yes | Yes |
| Need to inspect `3_platform` contents | Stop. | Future classification ticket. | No | Yes |
| Need to approve source tracking | Stop. | Future exact governance. | Yes | Yes |
| Source tree creation implied | Stop. | I-00 after gates. | Yes | Yes |
| Existing content approval implied | Stop. | Classification governance. | Yes | Yes |
| `.gitignore` modification implied | Stop. | Separate Git/security governance. | Yes | Maybe |
| Product source tracking implied | Stop. | Product governance. | Yes | Yes |
| Dependency adoption implied | Stop. | IR-04. | Yes | Yes |
| Validation execution implied | Stop. | IR-03/IR-08 approval. | Yes | Yes |
| Scripts/tools/tests creation implied | Stop. | IR-03. | Yes | Yes |
| Provider/API/MCP activation implied | Stop. | IR-06/security review. | Yes | Yes |
| CSS substrate decision implied | Stop. | IR-07. | Yes | Yes |
| Git action implied | Stop. | Exact human Git instruction. | Yes | Maybe |
| IR-03 scope pressure detected | Stop adjacent work. | Wait explicit IR-03 instruction. | No | No |
| I-00 scope pressure detected | Stop adjacent work. | Wait future implementation approval. | No | No |

## 27. Incident Handling
Incidents include `3_platform` contents inspected deeply; existing `3_platform` contents approved by implication; source tree created; source tracking approved; source files staged/tracked; product source copied into `3_platform`; `.gitignore` modified; dependency installed/adopted; tests/scripts/tools created or executed; builds/products executed; provider/API/MCP/network/auth activated; final Cognitive Semantic System substrate selected; Git staging/commit/push attempted; or IR-03/I-00 started.

Response: STOP, report safe metadata only, do not continue adjacent work, and require human/security/governance decision.

## 28. IR-02 Invariants
| ID | Invariant |
| --- | --- |
| IR02-001 | Implementation source tree / tracking policy is not implementation. |
| IR02-002 | Source tree policy is not source tree creation. |
| IR02-003 | Tracking policy does not approve source tracking now. |
| IR02-004 | Existing 3_platform contents remain uninspected and unapproved. |
| IR02-005 | Existing 3_platform contents are not trackable now. |
| IR02-006 | Product source remains local-only. |
| IR02-007 | Product Git posture is not changed. |
| IR02-008 | `.gitignore` is not modified. |
| IR02-009 | Dependencies remain unadopted. |
| IR02-010 | Validation is not executed. |
| IR02-011 | Security policy is not security enforcement. |
| IR02-012 | Cognitive Semantic System substrate remains undecided. |
| IR02-013 | Graph remains a candidate only. |
| IR02-014 | Validation evaluates; governance decides. |
| IR02-015 | IR-02 stops before IR-03. |

## 29. Anti-patterns
Anti-patterns: tracking policy as source tracking approval; tracking policy as implementation; `3_platform` content as source by proximity; unclassified content as approved; source tree creation by policy pressure; `.gitignore` edit as approval shortcut; dependency manifest as adoption; lockfile as approval; generated output as source; product source copy into platform tree; source tracking by force-add; broad staging; starting IR-03 inside IR-02; starting I-00 inside IR-02; `git add .`.

## 30. Readiness For IR-03
IR-03 - Scripts / Tools / Tests Readiness is ready after explicit instruction if IR-02 source tree / tracking policy exists, source tracking remains not approved, `3_platform` contents remain uninspected and unapproved, source tree creation remains blocked, no implementation artifact is implied, no scripts/tools/tests are created or executed, and no dependency adoption, validation execution, product activation, provider/API/MCP activation, CSS substrate decision, publication, or Git mutation is implied.

Do not create IR-03.

## 31. Final Verdict
| Question | Answer |
| --- | --- |
| What does IR-02 decide? | It defines docs-only trackability and future gates for source tree/tracking decisions. |
| Is source tracking approved now? | No. Source tracking is not approved. |
| Is `3_platform` source tree created? | No. |
| Are existing `3_platform` contents inspected, classified, approved, or trackable? | No. |
| What is trackable now? | IR governance docs under `0_architecture/implementation_readiness/`, exact path and human instruction only. |
| What remains not trackable now? | `3_platform/**`, product source, raw external sources, previous knowledge corpus, generated outputs, dependencies, secrets, credentials, datasets, models, artifacts, runtime outputs, scripts/tools/tests/runtime/provider/MCP/security/CSS source. |
| Did IR-02 modify `.gitignore`? | No. |
| Did IR-02 stage, commit, push, or force-add? | No. |
| Did IR-02 activate products? | No. |
| Did IR-02 adopt dependencies? | No. |
| Did IR-02 execute validation/tests/builds? | No. |
| Did IR-02 activate providers/API/MCP? | No. |
| Did IR-02 decide CSS substrate? | No. |
| What remains blocked? | Source tracking, source tree/skeleton creation, existing content inspection/classification/approval/tracking, implementation, product activation, dependency adoption, validation execution, scripts/tools/tests creation, provider/API/MCP activation, security enforcement, validation registry, CSS substrate decision, publication, Git mutation, IR-03 execution, and I-00. |
| Is IR-03 ready after explicit instruction? | Yes, as scripts/tools/tests readiness only; IR-03 is not started. |

Stop after IR-02 validation and report. Do not start IR-03 or any later ticket.
