# P-02 - Omniverse App Product Charter
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Omniverse App Product Charter |
| Ticket | P-02 |
| Product candidate | `omniverse-app` |
| Status | Accepted inactive Omniverse App product charter draft |
| Date | 2026-07-01 |
| Scope | Inactive charter draft for Siamese's Omniverse visual and operational interface. |
| Authority | Product charter draft only, not product activation. |
| Related documents | P-00, P-01, M-A, M-07, M-06, W-12, V-04, W-13, V-05, S-series, CSS-series, H-series, Siamese Product Vision |

## 2. Purpose
P-00 selected `omniverse-app` for charter drafting. P-01 defined the common product charter template and common gate. P-02 drafts the inactive `omniverse-app` charter.

`omniverse-app` is Siamese's visual/operational Omniverse Kit interface. Omniverse Kit is interface, not backend. The app is not the backend, not the EnergyPlus domain model, not the calibration engine, and not the surrogate training/control engine.

P-02 does not activate the product, inspect source deeply, adopt Omniverse/SDK dependencies, change Git posture, create validation baselines, approve runtime, or start P-03. It prepares P-03 - Backend EnergyPlus Product Charter for explicit future instruction only.

## 3. Product Candidate Summary
| Field | Value |
| --- | --- |
| product_id | PROD-005 / P00-SEL-001 |
| product_name | `omniverse-app` |
| product_platform_name | Siamese |
| product_status | candidate/deferred/local_only/inactive |
| selection_source | P-00 |
| charter_template_source | P-01 |
| likely area | Omniverse/visualization/operational interface |
| main risk | SDK/runtime/GPU/license/output/security/Git/root-boundary |
| current verdict | draft_for_charter_review_with_blockers |
| blocked inference | Product activation, runtime approval, SDK approval, source tracking, implementation readiness. |

## 4. Product Vision Alignment
Siamese is a living energy twin platform for buildings. Siamese keeps the energy model alive by connecting an energy design model to real data, calibration, prediction, recommendation/control, and continuous operation.

`omniverse-app` should make the living energy twin visible and operable. The MVP visual direction is: model + real data + calibration + visualization. Future visual surfaces may show model state, real sensor data, simulated results, calibrated model state, prediction, recommendations, uncertainty, and operational dashboards.

Boundary clarifications:
| Surface | Siamese role | P-02 boundary |
| --- | --- | --- |
| Omniverse Kit | Interface, viewport, UX, panels, visualization, commands, collaboration surface. | Product UI only; no backend ownership. |
| Backend Python | Energy domain, validation, EnergyPlus compilation, simulation, calibration, datasets, surrogate models, control, API/SDK. | Backend owns energy logic. |
| OpenUSD | Geometry/semantic representation and binding layer. | Not heavy raw time-series storage. |
| Time-series storage | External optimized storage for sensor/sim/prediction series. | Referenced or bound from USD, not embedded by default. |
| EnergyPlus | Physical solver. | EnergyPlus is solver, not internal model or source of truth. |

## 5. Owner / Governance
Owner is not finalized because no accepted source declares a final owner. P-02 records an owner gap.

Governance must decide activation, Git posture, dependency adoption, publication, and implementation readiness. P-02 cannot assign final owner authority or approve product work.

## 6. Product Scope
Future `omniverse-app` charter scope may include: Omniverse Kit application shell/UI surface; viewport and visual workspace for Siamese; OpenUSD stage interaction and semantic scene visualization; panels for energy model status, zones, sensors, results, and diagnostics; future visualization of real vs simulated vs predicted data; future thermal maps, sensor overlays, HVAC state overlays, uncertainty, and recommendations; future command surfaces that call governed backend/API commands; and future collaboration/asset workflow surfaces if governed later.

Out of scope: EnergyPlus backend implementation; energy domain model ownership; calibration algorithms; dataset generation engine; surrogate training or inference engine; control/optimization engine; sensor ingestion backend; time-series database; dependency adoption; SDK/runtime installation; production Nucleus deployment; MCP/provider/API activation; and implementation readiness.

## 7. Non-Goals
Non-goals: do not make Omniverse Kit the backend; do not bind the product directly to IDF/epJSON as internal model; do not store heavy time-series in USD; do not treat visual layers as source of truth; do not treat screenshots/reports/visual outputs as source; do not treat product needs as root architecture decisions; do not use product visualization needs to decide the Cognitive Semantic System substrate; do not activate runtime or dependencies.

## 8. Product / Root Boundary
`omniverse-app` is product-scoped. It does not define AGENT PLATFORM root authority, the Cognitive Semantic System, backend truth, validation truth, governance truth, or source truth.

Product decisions can inform future root proposals but cannot silently constrain root architecture. Product runtime decisions remain product-scoped unless governed otherwise.

## 9. User / Domain / Interface Hypothesis
| Hypothesis | Expected use | Validation posture |
| --- | --- | --- |
| Energy engineer | Model, simulate, compare, visualize, diagnose. | Hypothesis only. |
| Facility manager | Understand current state, alerts, predictions, recommendations. | Hypothesis only. |
| Researcher/university | Living lab, datasets, calibration, control experiments. | Hypothesis only. |
| Building owner/operator | Energy savings, comfort, sustainability evidence. | Hypothesis only. |

These are hypotheses, not validated market claims.

## 10. Current Local-only Posture
`omniverse-app` source, if present under `2_products/`, remains local-only and ignored. P-02 does not inspect product source. P-02 uses safe metadata only.

Local sessions, configs, generated outputs, data, logs, screenshots, credentials, dependency folders, build outputs, and product artifacts remain excluded.

## 11. Security / Access Posture
Building data, sensor data, occupancy, operational schedules, HVAC states, screenshots, logs, USD layers, and generated reports may be sensitive.

Secrets, credentials, tokens, provider auth, Nucleus auth, cloud auth, local sessions, telemetry configs, and API keys are excluded. No network/provider/API/MCP/auth activation occurs. Unknown sensitivity blocks publication and context exposure.

## 12. Dependency / External Source Posture
Omniverse Kit dependency posture is unresolved. OpenUSD/Nucleus dependency posture is unresolved. GPU/runtime/driver dependency posture is unresolved. NVIDIA SDK/license/name-use posture must be reviewed later.

External source presence is not adoption. Dependency references are not dependency approval. P-09 will handle Product Dependency / External Source Posture.

## 13. Provider / API / MCP Posture
`omniverse-app` may later call backend APIs or commands only after contracts and governance. No provider/API/MCP is activated by P-02.

MCP availability is not MCP activation. Tool availability is not permission. Provider credentials are not provider permission. Backend connection modes are future scope.

## 14. Generated Output / Data / Model / Artifact Posture
Visual captures, screenshots, USD layers, heatmaps, reports, simulation overlays, logs, sensor overlays, dashboard exports, and generated documentation are generated-sensitive by default.

Generated output is evidence, not source by default. Raw output remains local-only until reviewed. Publication requires product, security, validation, and governance review.

## 15. Git Posture
Product Git posture is not changed by P-02. `2_products/` remains ignored/local-only. `omniverse-app` source tracking is deferred to P-08.

P-02 does not stage, commit, push, force-add, or publish. Future Git action must use exact paths only. No `git add .`.

## 16. Validation Baseline Needs
Future baseline needs under V-04/P-01: product charter completeness checks; UI/product scope checks; local-only checks; dependency/license checks; generated-output checks; security/access checks; backend/API boundary checks; OpenUSD semantic binding checks; visualization provenance checks; launch/build/test checks only after explicit future approval.

P-02 does not create or execute validation baselines. P-10 handles Product Validation Baseline.

## 17. Activation Blockers
| blocker | reason | required future action | blocks activation? |
| --- | --- | --- | --- |
| owner missing or not final | No accepted final owner. | Assign governed owner. | Yes |
| scope not validated | Scope is draft only. | Product scope review. | Yes |
| root/product boundary requires review | Visual interface can blur root authority. | Product/root boundary review. | Yes |
| Omniverse Kit/SDK/license unresolved | Runtime, SDK, and name-use risks. | P-09/dependency/license review. | Yes |
| OpenUSD/Nucleus posture unresolved | Scene/collaboration dependencies unclear. | Dependency/security review. | Yes |
| GPU/runtime posture unresolved | Driver/runtime/host constraints unknown. | Runtime/security review. | Yes |
| product Git posture deferred to P-08 | Source tracking not approved. | P-08 Git posture decision. | Yes |
| dependency posture deferred to P-09 | Adoption not approved. | P-09 dependency posture. | Yes |
| validation baseline deferred to P-10 | Baseline absent. | P-10 baseline. | Yes |
| security/access review missing | Sensitive building/product data possible. | Security review. | Yes |
| generated-output review missing | Visual outputs may leak data. | Output review. | Yes |
| backend API contracts missing | UI/backend boundary undefined. | Backend/API contract. | Yes |
| time-series storage strategy missing | USD must not carry heavy series by default. | Storage/binding strategy. | Yes |
| no implementation readiness assessment | Readiness not evaluated. | Future IR review. | Yes |
| no product governance activation decision | Governance has not activated. | Activation decision. | Yes |

## 18. Implementation Readiness Blockers
No implementation readiness exists. Blockers include no source tree tracking decision, package/SDK readiness, build/test/launch posture, backend API contract, OpenUSD schema/binding contract, visualization data contract, security enforcement, validation registry implementation, or deployment/packaging readiness.

## 19. Evidence / Source References
Future charter claims must cite P-00 for selection, P-01 for common gate, M-07 for product charter-prep posture, M-06/W-13/V-05 for dependency/external posture, W-12 for product policy, V-04 for product validation posture, S-series for local-only/security, CSS-series for substrate/naming, H-series/M-04 for runtime/tool/provider/MCP boundary, and Siamese Product Vision for strategic product context.

Evidence supports review; evidence does not approve activation.

## 20. Gate Checklist
| Gate | P-02 status | Note |
| --- | --- | --- |
| GATE-01 selected candidate exists in P-00 | pass | P-00 selected `omniverse-app`. |
| GATE-02 owner declared or owner gap recorded | pass_with_caution | Owner gap recorded. |
| GATE-03 purpose declared | pass | Visual/operational Siamese interface. |
| GATE-04 scope declared | pass_with_caution | Draft scope; needs validation. |
| GATE-05 non-goals declared | pass | Backend/solver/control excluded. |
| GATE-06 product/root boundary declared | pass | Product-scoped only. |
| GATE-07 local-only posture declared | pass | `2_products/` remains ignored/local-only. |
| GATE-08 security posture declared | pass_with_caution | Sensitive building/output risk. |
| GATE-09 dependency posture declared | blocked | Omniverse/OpenUSD/Nucleus/GPU unresolved. |
| GATE-10 external-source posture declared | pass_with_caution | Evidence only. |
| GATE-11 Git posture declared or deferred to P-08 | pass_with_caution | Deferred to P-08. |
| GATE-12 validation baseline need declared | pass_with_caution | Deferred to P-10. |
| GATE-13 generated-output posture declared | pass_with_caution | Generated-sensitive by default. |
| GATE-14 provider/API/MCP posture declared | pass_with_caution | Future backend/API only after governance. |
| GATE-15 activation blockers declared | pass | Blockers listed. |
| GATE-16 implementation-readiness blockers declared | pass | Blockers listed. |
| GATE-17 governance decision path declared | pass_with_caution | Governance required; owner gap remains. |
| GATE-18 stop rules declared | pass | Stop before P-03 and all forbidden actions. |

Final gate status: `gate_passed_with_cautions_for_charter_review_only`. This gate status does not activate the product.

## 21. Omniverse-specific Gate Overlay
| overlay item | current posture | blocker | future route |
| --- | --- | --- | --- |
| Omniverse Kit runtime | Unapproved. | Runtime/install risk. | Dependency/runtime review. |
| OpenUSD semantic scene | Candidate representation. | Schema/binding absent. | Product schema/binding review. |
| Nucleus/collaboration | Unapproved. | Auth/network/storage risk. | Security/governance review. |
| GPU/driver/runtime | Unapproved. | Host/runtime constraints. | Runtime/security review. |
| USD layers and generated visual outputs | Generated-sensitive. | Publication/data leakage. | Output review. |
| backend API connection | Future only. | No contract. | P-03/P-later API contract. |
| sensor/time-series visualization | Future only. | Storage/binding absent. | Data/storage strategy. |
| real/sim/predicted comparison | Future only. | Provenance/validation absent. | Validation/data contract. |
| thermal visualization | Future only. | Accuracy/provenance risk. | Visualization validation. |
| commands/tool surfaces | Blocked. | Execution/API risk. | Governed command contracts. |
| packaging/distribution | Not ready. | SDK/license/build risk. | Packaging/dependency review. |
| license/name-use | Unreviewed. | NVIDIA/Omniverse claims risk. | License/name-use review. |

## 22. Residual Risks
Residual risks: no active product owner, product source review, SDK/license review, backend contract, OpenUSD schema contract, time-series storage contract, generated-output publication policy, validation baseline, Git posture decision, implementation readiness, or product activation decision.

## 23. P-02 Invariants
| ID | Invariant |
| --- | --- |
| P02-001 | Omniverse App charter is not product activation. |
| P02-002 | Omniverse Kit is interface, not backend. |
| P02-003 | EnergyPlus is solver, not internal model. |
| P02-004 | OpenUSD is geometry/semantic representation, not heavy time-series storage. |
| P02-005 | Product source remains local-only. |
| P02-006 | Product Git posture is not changed. |
| P02-007 | Product dependencies are not adopted. |
| P02-008 | Product validation baseline is not created. |
| P02-009 | Generated visual output is not source by default. |
| P02-010 | Product needs do not decide root architecture. |
| P02-011 | Product needs do not decide Cognitive Semantic System substrate. |
| P02-012 | Graph remains a candidate only. |
| P02-013 | Validation evaluates; governance decides. |
| P02-014 | P-02 stops before P-03. |

## 24. Anti-patterns
Anti-patterns: Omniverse app as full Siamese backend; Omniverse Kit as energy logic owner; USD visual layer as source of truth; EnergyPlus IDF as internal platform model; heavy time-series stored directly in USD by default; SDK reference as dependency approval; product charter as activation; product source inspection by curiosity; generated visuals as source; graph/product visualization as substrate decision; starting P-03 inside P-02; `git add .`.

## 25. Readiness For P-03
P-03 - Backend EnergyPlus Product Charter is ready after explicit instruction if P-02 Omniverse App Product Charter exists, `omniverse-app` remains inactive, backend boundary is preserved, EnergyPlus solver boundary is preserved, product/local-only/Git/dependency/security boundaries are preserved, and no product activation, source tracking, dependency adoption, provider/API/MCP activation, publication, or implementation is implied.

Do not create P-03.

## 26. Final Verdict
| Question | Answer |
| --- | --- |
| What does P-02 create? | One inactive Omniverse App Product Charter draft. |
| What is omniverse-app in Siamese? | The visual/operational Omniverse Kit interface for the living energy twin. |
| Did P-02 activate omniverse-app? | No. |
| Did P-02 inspect product source deeply? | No. |
| Did P-02 run Omniverse Kit or install SDKs? | No. |
| Did P-02 change product Git posture? | No. |
| Did P-02 adopt dependencies? | No. |
| Did P-02 create validation baselines? | No. |
| Did P-02 define backend logic? | No. Backend Python owns energy logic, validation, simulation orchestration, calibration, datasets, surrogate models, APIs, and control. |
| What remains blocked? | Activation, source inspection, Omniverse/SDK/OpenUSD/Nucleus/GPU dependency adoption, runtime execution, Kit launch, product Git tracking, validation baselines, backend/API contracts, generated-output publication, implementation readiness, provider/API/MCP/network/auth activation, staging, commit, push, and P-03. |
| Is P-03 ready after explicit instruction? | Yes, as Backend EnergyPlus Product Charter drafting only; P-03 is not started. |

Stop after P-02 validation and report. Do not start P-03 or any later ticket.
