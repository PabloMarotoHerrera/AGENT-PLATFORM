# IR-01 - 3_platform Structure Decision
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | 3_platform Structure Decision |
| Ticket | IR-01 |
| Status | Accepted 3_platform structure decision |
| Date | 2026-07-01 |
| Scope | Structure posture for `3_platform` as a future AGENT PLATFORM / Siamese implementation root candidate after IR-00. |
| Authority | Structure decision only, not source tree creation. |
| Related documents | IR-00, P-A, P-00 through P-10, M-A, W-series, V-series, S-series, CSS-series, H-series, `.gitignore`, `README.md`, Siamese Product Vision |
| Decision target | `3_platform` structure posture |

## 2. Purpose
IR-00 found AGENT PLATFORM not ready for implementation, but allowed FASE 5 planning tickets to continue. IR-00 noted a pre-existing `3_platform` directory and did not inspect, approve, track, or activate it.

IR-01 decides structure posture only. IR-01 does not create `3_platform`, does not approve existing `3_platform` contents, prepares IR-02, and does not start IR-02.

## 3. 3_platform Structure Decision Definition
A `3_platform` structure decision is a governance decision that reserves or rejects a platform-level implementation root concept and defines its boundaries before any source tree creation, tracking, implementation, dependency adoption, or runtime activation.

In plain terms, 3_platform structure decision is not implementation, and 3_platform structure decision is not source tree creation. Structure decision is not source tracking approval, product activation, dependency adoption, validation execution, Git mutation, or approval of pre-existing contents.

## 4. Decision Summary
Decision: `3_platform` is accepted as the reserved future platform implementation root candidate. IR-01 approves the name and conceptual boundary only.

Existing `3_platform`, if present, remains unapproved, uninspected, untracked, inactive, and non-authoritative. IR-01 does not approve contents, source tracking, implementation, source tree creation, skeleton creation, product activation, dependency adoption, validation execution, provider/API/MCP activation, publication, or Git mutation.

IR-01 requires IR-02 before any source tree or tracking policy can be accepted. I-00 remains blocked.

## 5. Authority Boundary
| Layer | IR-01 boundary |
| --- | --- |
| Governance | Decides future source tree creation, source tracking, implementation, product activation, publication, exceptions, and lifecycle. |
| Validation | Evaluates readiness evidence and does not approve structure, tracking, or implementation. |
| Security | Constrains local-only content, secrets, credentials, execution, providers, APIs, MCP, network/auth, generated outputs, and publication. |
| IR-01 | Decides structure posture only. |
| Git | Records artifacts but does not approve structure or contents. |
| Agents | May prepare safe structure metadata but cannot inspect, implement, execute, activate, adopt, stage, commit, push, publish, or start IR-02. |

## 6. Source Boundary
IR-00 is the primary readiness input. P-A is the FASE 4 closure input. P-08 controls product Git posture. P-09 controls dependency/external posture. P-10 controls validation baseline posture. W-series controls workspace structure and governance. V/S/H/CSS-series constrain validation, security, runtime, providers, tools, and substrate.

Raw `3_platform` contents are not inspected. Raw `2_products/` and `4_external/sources/` are not inspected. Safe metadata only.

## 7. Existing 3_platform Posture
| item | observed status | IR-01 decision | allowed use | blocked use | future route |
| --- | --- | --- | --- | --- | --- |
| `3_platform` directory existence | May be observed by `Test-Path` only; IR-00 observed pre-existing directory. | Existing directory is not approval. | Existence metadata. | Listing, deep inspection, edit, approval. | IR-02 classification policy. |
| `3_platform` contents | Unknown. | Unapproved and uninspected. | None in IR-01. | Reuse, copy, move, delete, normalize, transform, tracking. | Existing content classification gate. |
| `3_platform` as implementation root name | Candidate name. | Reserved conceptually. | Future planning reference. | Implementation claim. | IR-02, then later I-00 only after gates. |
| `3_platform` as tracked source | Not approved. | Tracking blocked. | None. | Stage, commit, force-add, publish. | IR-02 source tracking policy. |
| `3_platform` as product source | Not product workspace. | Product source remains separate/local-only. | Boundary marker. | Product source copy or activation. | Product governance. |
| `3_platform` as runtime | Not active. | Runtime blocked. | Boundary discussion. | Agents, providers, adapters, MCP, tools. | IR-05/IR-06. |
| `3_platform` as authority | Not authority. | Governance remains authority. | Evidence target only. | Root override by existence. | W/V/S/CSS governance. |

## 8. Reserved Structure Meaning
`3_platform` means a future root-level implementation area candidate for platform implementation artifacts, distinct from architecture documentation, product workspaces, external sources, datasets, models, artifacts, previous knowledge, secrets, credentials, generated outputs, and local-only material.

`3_platform` may later contain platform code only if approved by later exact governance. It does not currently contain approved source by IR-01.

## 9. Reserved Structure Non-meaning
`3_platform` does not mean implementation has started, existing content is approved, source tracking is approved, product source is approved, products are active, dependencies are adopted, validation execution is approved, runtime/provider/API/MCP is active, the Cognitive Semantic System substrate is decided, a skeleton exists, or I-00 is ready.

## 10. Conceptual Future Structure Categories
| category | meaning | current status | required future gate | blocked action |
| --- | --- | --- | --- | --- |
| core platform domain | Shared platform logic. | conceptual only | IR-02/I-00 | Create code. |
| validation registry | Validation/proof metadata implementation. | conceptual only | IR-08 | Build registry. |
| security/access enforcement | Runtime/policy enforcement. | conceptual only | IR-08 | Build enforcement. |
| context pack runtime | Context selection/execution support. | conceptual only | IR-05 | Implement runtime. |
| provider/adapter layer | Provider/API adapter boundaries. | conceptual only | IR-06 | Activate providers/adapters. |
| agent runtime boundary | Agent lifecycle and handoff boundary. | conceptual only | IR-05 | Create agents. |
| tool execution boundary | Shell/tool safety surface. | conceptual only | IR-03/IR-05 | Run or implement tools. |
| Cognitive Semantic System prototype | Future CSS experiment. | conceptual only | IR-07 then later ticket | Prototype or select substrate. |
| product integration interfaces | Governed product/backend contracts. | conceptual only | Product governance/IR-02 | Copy product source. |
| tests/harnesses | Future validation/runtime checks. | conceptual only | IR-03/IR-08 | Create or run tests. |
| scripts/tools | Future automation utilities. | conceptual only | IR-03 | Create scripts/tools. |
| schemas/contracts | Future typed contracts. | conceptual only | IR-02/IR-08 | Create schemas. |
| documentation stubs | Future implementation docs. | conceptual only | Later exact ticket | Create implementation docs. |

## 11. Relationship To Product Workspaces
`3_platform` is not `2_products/`. Product source remains local-only. Product charters do not become implementation source. Siamese product surfaces may inform future requirements only.

`omniverse-app` is visual/interface, not backend. `backend-energyplus` is an inactive energy-domain backend candidate. EnergyPlus remains solver, not internal model. `cli`, `desktop`, and `web-platform` are interface candidates only. `experimental` remains blocked/local-only. Product activation and product source tracking remain blocked. Product-specific source must not be copied into `3_platform` by IR-01.

## 12. Relationship To Root Architecture
`3_platform` is subordinate to governance. It cannot override W/V/S/H/CSS/P-series decisions, define root authority by existence, decide the Cognitive Semantic System substrate, or make product requirements root authority.

Graph remains a candidate only. Validation evaluates; governance decides.

## 13. Relationship To Git / Source Tracking
P-08 remains in force. IR-01 does not change product Git posture, approve `3_platform` tracking, stage, commit, push, force-add, publish, or modify `.gitignore`. Existing `3_platform`, if ignored or untracked, remains unapproved. Source tracking is not approved. Source tracking policy is deferred to IR-02.

Future tracking requires exact paths, include/exclude policy, `.gitignore` impact review, security review, validation route, and governance approval. Do not use `git add .`.

## 14. Relationship To Dependencies / External Sources
P-09 remains in force. `3_platform` does not adopt dependencies or external sources. Dependency manifests, if ever present, are not adoption approval. No package/runtime/SDK/native/provider/API/MCP/network/auth use is approved. Dependency readiness is deferred to IR-04.

## 15. Relationship To Validation / Security
P-10, V-series, and S-series remain in force. A `3_platform` structure decision does not execute validation. No tests, builds, runners, CI, registry, or enforcement are created. Security policy is not security enforcement. Validation/security enforcement readiness is deferred to IR-08.

Any future platform source must preserve local-only, secrets, credentials, generated-output, execution, network, and publication rules.

## 16. Relationship To Runtime / Agent / Provider / MCP
H-series remains in force. `3_platform` does not activate runtime, agents, providers, adapters, tools, hooks, skills, or MCP. Tool availability is not permission. Provider credentials are not provider permission. MCP availability is not MCP activation. Runtime boundaries are deferred to IR-05 and IR-06.

## 17. Relationship To Cognitive Semantic System
Cognitive Semantic System is the accepted name. Substrate remains undecided. Graph remains a candidate only. Graphify remains evidence/historical/external/prohibited/candidate-evidence only, not authority.

`3_platform` does not imply a Cognitive Semantic System prototype. The CSS substrate gate is deferred to IR-07.

## 18. Future Source Tree Gate
Before any `3_platform` source tree approval: IR-01 structure decision exists; IR-02 source tree/tracking policy exists; security/local-only review exists; dependency posture remains controlled; validation baseline and future checks exist; exact include/exclude paths are declared; generated-output policy is declared; `.gitignore` impact is reviewed; existing `3_platform` contents are classified or excluded; source ownership is declared; rollback/removal plan is declared; governance approval is recorded.

IR-01 does not pass this gate.

## 19. Existing Content Classification Gate
Before any existing `3_platform` content may be inspected, approved, tracked, deleted, moved, or reused: exact scope is declared; purpose is declared; owner is declared; sensitivity/security review is declared; generated-output risk is reviewed; dependency/package risk is reviewed; source/origin/provenance is reviewed; Git status is reviewed; include/exclude posture is declared; governance approval is recorded.

IR-01 does not inspect or classify contents.

## 20. Future Structure Options
| option | current decision | allowed now | blocked now | future route |
| --- | --- | --- | --- | --- |
| Reserve `3_platform` as future implementation root | Recommended and accepted conceptually. | Name/concept reference. | Skeleton/source approval. | IR-02 then later I-00. |
| Reject `3_platform` as implementation root | Not selected now. | Reconsider later. | Use rejection to delete content. | Future governance. |
| Quarantine pre-existing contents | Contents remain unapproved/inactive. | Safe metadata only. | Inspect, move, delete, approve. | Classification gate. |
| Split future implementation into separate repo | Deferred option. | Discuss conceptually. | Create repo/source. | IR-02/repo strategy. |
| Keep implementation local-only | Deferred option. | Discuss conceptually. | Implement now. | IR-02. |
| Create source skeleton later | Blocked now. | None. | Create folders/files. | I-00 after gates. |
| Track source later | Blocked now. | None. | Stage/commit/force-add. | IR-02. |
| Archive/delete existing contents later | Deferred. | None. | Archive/delete now. | Classification/lifecycle governance. |

## 21. Readiness Gate Model
| gate | pass condition | current posture | blocker if missing |
| --- | --- | --- | --- |
| IR01-G01 IR-00 exists | IR-00 assessment accepted. | Pass pending validation. | Cannot make IR-01 decision. |
| IR01-G02 P-A exists | Product audit exists. | Pass pending validation. | FASE 4 closure missing. |
| IR01-G03 `3_platform` name decision made | Name reserved or rejected. | Reserved. | Structure ambiguity. |
| IR01-G04 existing contents unapproved | Contents not inspected/approved. | Pass. | Approval by implication. |
| IR01-G05 no source tree created | IR-01 creates no folders/source. | Pass. | Implementation incident. |
| IR01-G06 no tracking approved | Source tracking remains blocked. | Pass. | Git posture drift. |
| IR01-G07 local-only posture preserved | Ignored/local-only roots unchanged. | Pass. | Exposure risk. |
| IR01-G08 dependency posture preserved | No adoption. | Pass. | Dependency drift. |
| IR01-G09 validation/security posture preserved | No execution/enforcement. | Pass. | Unsafe readiness claim. |
| IR01-G10 IR-02 next scope declared | IR-02 named but not started. | Pass. | Next-ticket drift. |

## 22. Structure Decision Status Model
Statuses: `structure_name_reserved`, `existing_directory_detected_unapproved`, `contents_uninspected_unapproved`, `source_tree_not_created`, `source_tracking_not_approved`, `implementation_not_started`, `blocked_pending_IR02_tracking_policy`, `blocked_pending_existing_content_classification`, `blocked_pending_security_review`, `blocked_pending_dependency_readiness`, `blocked_pending_validation_security_enforcement`, `blocked_pending_I00_skeleton`, and `rejected_for_implementation_now`.

Current status: `structure_name_reserved` + `existing_directory_detected_unapproved` + `implementation_not_started` + `blocked_pending_IR02_tracking_policy`.

## 23. Residual Risk Register
| risk_id | residual risk | source | severity | mitigation | route | blocks implementation? |
| --- | --- | --- | --- | --- | --- | --- |
| IR01-RISK-001 | Pre-existing `3_platform` mistaken as approved source. | IR-00/IR-01 | high | Label unapproved. | IR-02 | Yes |
| IR01-RISK-002 | Contents unknown. | Safe metadata only | high | Classification gate. | IR-02 | Yes |
| IR01-RISK-003 | Source tracking policy absent. | P-08/IR-00 | high | Exact policy. | IR-02 | Yes |
| IR01-RISK-004 | Existing content provenance unknown. | IR-01 | high | Provenance review. | Classification gate | Yes |
| IR01-RISK-005 | Dependency manifests may exist but are unapproved. | P-09 | high | Dependency review. | IR-04 | Yes |
| IR01-RISK-006 | Generated outputs may exist but are unreviewed. | S/V/P-series | high | Generated-output policy. | IR-02/IR-08 | Yes |
| IR01-RISK-007 | Secrets/credentials risk unknown. | S-series | high | Security review. | IR-08 | Yes |
| IR01-RISK-008 | Product source may be mixed accidentally. | P-08/P-A | high | Keep product boundary. | IR-02/Product governance | Yes |
| IR01-RISK-009 | `.gitignore` impact unknown. | P-08 | medium-high | Impact review. | IR-02 | Yes |
| IR01-RISK-010 | Implementation pressure before IR-02. | IR roadmap | high | Stop before IR-02. | Governance | Yes |
| IR01-RISK-011 | Product/root boundary leakage. | P/W-series | high | Boundary review. | IR-02 | Yes |
| IR01-RISK-012 | CSS substrate pressure. | CSS-series | high | IR-07 gate. | IR-07 | Yes |
| IR01-RISK-013 | Validation/security enforcement absent. | V/S-series | high | Enforcement readiness. | IR-08 | Yes |

## 24. Blocker Register
| blocker | stop behavior | required future action | blocks IR-01? | blocks implementation? |
| --- | --- | --- | --- | --- |
| Missing IR-00 | Stop. | Restore/create IR-00. | Yes | Yes |
| Missing P-A | Stop. | Restore P-A. | Yes | Yes |
| Need to inspect `3_platform` contents | Stop. | Exact classification ticket. | No | Yes |
| Need to approve existing contents | Stop. | Classification and governance approval. | Yes | Yes |
| Source tree creation implied | Stop. | Future I-00 after gates. | Yes | Yes |
| Source tracking implied | Stop. | IR-02. | Yes | Yes |
| Dependency adoption implied | Stop. | IR-04. | Yes | Yes |
| Validation execution implied | Stop. | IR-03/IR-08 approval. | Yes | Yes |
| Product activation implied | Stop. | Product governance. | Yes | Yes |
| Provider/API/MCP activation implied | Stop. | IR-06/security review. | Yes | Yes |
| CSS substrate decision implied | Stop. | IR-07. | Yes | Yes |
| Git action implied | Stop. | Exact human Git instruction. | Yes | Maybe |
| I-00 scope pressure detected | Stop adjacent work. | Wait explicit later instruction. | No | No |
| IR-02 scope pressure detected | Stop adjacent work. | Wait explicit IR-02 instruction. | No | No |

## 25. Incident Handling
Incidents include `3_platform` created by IR-01; `3_platform` contents inspected deeply; existing `3_platform` contents approved by implication; source tree created; source files staged/tracked; product source copied into `3_platform`; dependencies installed/adopted; tests/builds/products executed; provider/API/MCP/network/auth activated; final Cognitive Semantic System substrate selected; `.gitignore` modified; Git staging/commit/push attempted; or IR-02/I-00 started.

Response: STOP, report safe metadata only, do not continue adjacent work, and require human/security/governance decision.

## 26. IR-01 Invariants
| ID | Invariant |
| --- | --- |
| IR01-001 | `3_platform` structure decision is not implementation. |
| IR01-002 | `3_platform` structure decision is not source tree creation. |
| IR01-003 | `3_platform` structure decision does not approve existing contents. |
| IR01-004 | Existing `3_platform` contents remain uninspected and unapproved. |
| IR01-005 | Product source remains local-only. |
| IR01-006 | Product Git posture is not changed. |
| IR01-007 | Source tracking is not approved. |
| IR01-008 | Dependencies remain unadopted. |
| IR01-009 | Validation is not executed. |
| IR01-010 | Security policy is not security enforcement. |
| IR01-011 | Cognitive Semantic System substrate remains undecided. |
| IR01-012 | Graph remains a candidate only. |
| IR01-013 | Validation evaluates; governance decides. |
| IR01-014 | IR-01 stops before IR-02. |

## 27. Anti-patterns
Anti-patterns: structure decision as implementation; structure decision as skeleton creation; `3_platform` existence as approval; `3_platform` contents as source by proximity; source tree creation by readiness pressure; source tracking by path reservation; product source copy into `3_platform`; dependency adoption by manifest presence; generated output as source; Git tracking as readiness; `.gitignore` edit as shortcut; CSS substrate decision by structure pressure; starting IR-02 inside IR-01; starting I-00 inside IR-01; `git add .`.

## 28. Readiness For IR-02
IR-02 - Implementation Source Tree / Tracking Policy is ready after explicit instruction if IR-01 structure decision exists, `3_platform` is reserved conceptually only, existing `3_platform` contents remain unapproved and uninspected, no source tree creation is implied, no source tracking is implied, no implementation artifact is implied, and no dependency adoption, validation execution, product activation, provider/API/MCP activation, CSS substrate decision, publication, or Git mutation is implied.

Do not create IR-02.

## 29. Final Verdict
| Question | Answer |
| --- | --- |
| What does IR-01 decide? | It reserves `3_platform` as a future platform implementation root candidate and defines boundaries. |
| Is `3_platform` reserved as future implementation root candidate? | Yes, conceptually only. |
| Did IR-01 create `3_platform`? | No. |
| Did IR-01 inspect or approve existing `3_platform` contents? | No. Existing contents remain uninspected and unapproved. |
| Did IR-01 create a source tree or skeleton? | No. |
| Did IR-01 approve source tracking? | No. Source tracking is not approved. |
| Did IR-01 activate products? | No. |
| Did IR-01 adopt dependencies? | No. |
| Did IR-01 execute validation/tests/builds? | No. |
| Did IR-01 activate providers/API/MCP? | No. |
| Did IR-01 decide CSS substrate? | No. |
| What remains blocked? | Implementation, source tree/skeleton creation, source tracking, existing content classification/approval, product activation, dependency adoption, validation execution, security enforcement, validation registry, provider/API/MCP activation, CSS substrate decision, publication, Git mutation, IR-02 execution, and I-00. |
| Is IR-02 ready after explicit instruction? | Yes, as source tree/tracking policy only; IR-02 is not started. |

Stop after IR-01 validation and report. Do not start IR-02 or any later ticket.
