# P-03 - Backend EnergyPlus Product Charter
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Backend EnergyPlus Product Charter |
| Ticket | P-03 |
| Product candidate | `backend-energyplus` |
| Status | Accepted inactive Backend EnergyPlus product charter draft |
| Date | 2026-07-01 |
| Scope | Inactive charter draft for Siamese's energy-domain backend product candidate. |
| Authority | Product charter draft only, not product activation. |
| Related documents | P-00, P-01, P-02, M-A, M-07, M-06, W-12, V-04, W-13, V-05, S-series, CSS-series, H-series, Siamese Product Vision |

## 2. Purpose
P-00 selected `backend-energyplus` for charter drafting. P-01 defined the common product charter template and common gate. P-02 preserved the Omniverse/backend boundary. P-03 drafts the inactive `backend-energyplus` charter.

`backend-energyplus` is Siamese's energy-domain backend candidate. Its future role is to own energy model logic, validation, EnergyPlus compilation, simulation orchestration, result normalization, calibration preparation, batch simulation, dataset generation, surrogate handoff, API/SDK surfaces, and future control integration.

P-03 does not activate the product, inspect source deeply, run EnergyPlus/OpenStudio, adopt dependencies, change Git posture, create validation baselines, approve runtime, implement backend behavior, or start P-04. It prepares P-04 - CLI Product Charter for explicit future instruction only.

## 3. Product Candidate Summary
| Field | Value |
| --- | --- |
| product_id | PROD-001 / P00-SEL-002 |
| product_name | `backend-energyplus` |
| product_platform_name | Siamese |
| product_status | candidate/deferred/local_only/inactive |
| selection_source | P-00 |
| charter_template_source | P-01 |
| boundary_source | P-02 Omniverse/backend split |
| likely area | Backend/domain simulation |
| main risk | EnergyPlus/OpenStudio/native/license/data/validation |
| current verdict | draft_for_charter_review_with_blockers |
| blocked inference | Product activation, engine approval, source tracking, runtime approval, simulation behavior, implementation readiness. |

## 4. Product Vision Alignment
Siamese is a living energy twin platform for buildings. The backend should keep the energy model alive by connecting an internal energy model to real data, calibration, prediction, recommendation/control, and continuous operation.

The MVP backend direction is: internal energy model, EnergyPlus compilation/runner, normalized results, and real-data comparison/calibration readiness.

Boundary clarifications:
| Surface | Siamese role | P-03 boundary |
| --- | --- | --- |
| Backend Python | Energy domain, validation, simulation orchestration, calibration, datasets, surrogate handoff, APIs, future control. | Backend owns energy logic inside product scope after governance. |
| EnergyPlus | Physical solver. | Solver only; not internal model or source of truth. |
| IDF/epJSON | Solver input artifacts. | Generated artifacts; not platform source of truth. |
| OpenStudio | Possible SDK/tooling evidence. | External/domain dependency candidate only. |
| Omniverse app | Visual/operational interface. | Consumer of governed backend contracts only. |
| OpenUSD | Geometry/semantic representation and binding layer. | Not backend energy logic or heavy raw time-series store. |
| CLI/desktop/web-platform | Interfaces or operators. | Consumers of governed backend contracts only. |

## 5. Owner / Governance
Owner is not finalized because no accepted source declares a final owner. P-03 records an owner gap.

Governance must decide activation, Git posture, dependency adoption, publication, validation baseline acceptance, and implementation readiness. P-03 cannot assign final owner authority or approve product work.

## 6. Product Scope
Future `backend-energyplus` charter scope may include: internal energy model schema and validation; building/zone/system input normalization; EnergyPlus input generation; simulation job orchestration; result parsing and normalization; weather and schedule handling; real-data comparison preparation; calibration workflow preparation; batch simulation and dataset generation; surrogate-model handoff contracts; future recommendation/control integration; API/SDK surfaces for Omniverse, CLI, desktop, and web consumers; and provenance for generated solver artifacts.

Out of scope: activating EnergyPlus/OpenStudio/native binaries; adopting dependencies; proving current backend behavior; inspecting product source deeply; running simulations; committing product source; owning root architecture; deciding the Cognitive Semantic System substrate; visual UI ownership; CLI command ownership; desktop/web implementation; production deployment; provider/API/MCP/network/auth activation; and implementation readiness.

## 7. Non-Goals
Non-goals: do not treat EnergyPlus as internal platform model; do not treat IDF/epJSON as source of truth; do not treat simulation output as truth without validation; do not make Omniverse, OpenUSD, CLI, desktop, or web-platform own backend energy logic; do not adopt OpenStudio by relevance; do not make product dependency choices root dependency choices; do not activate runtime, package managers, native engines, APIs, or MCP surfaces.

## 8. Product / Root Boundary
`backend-energyplus` is product-scoped. It does not define AGENT PLATFORM root authority, root vocabulary, Cognitive Semantic System authority, validation truth, governance truth, Git posture, or dependency posture.

Product needs may inform future root proposals but cannot silently constrain root architecture. The Cognitive Semantic System remains root-governed, and graph remains a candidate only.

## 9. User / Domain / Interface Hypothesis
| Hypothesis | Expected use | Validation posture |
| --- | --- | --- |
| Energy engineer | Define, validate, simulate, compare, and calibrate building energy models. | Hypothesis only. |
| Facility/operator team | Use normalized backend outputs for diagnostics, predictions, and recommendations. | Hypothesis only. |
| Researcher/university | Run living-lab experiments, batch simulations, datasets, surrogate workflows, and control studies. | Hypothesis only. |
| Product interfaces | Omniverse, CLI, desktop, and web consume governed backend contracts. | Hypothesis only. |

These are product hypotheses, not validated market, behavior, or execution claims.

## 10. Current Local-only Posture
`backend-energyplus` source, if present under `2_products/`, remains local-only and ignored. P-03 does not inspect product source. P-03 uses safe metadata only.

Local sessions, configs, generated solver files, outputs, data, logs, reports, credentials, dependency folders, native binaries, models, datasets, and product artifacts remain excluded.

## 11. Security / Access Posture
Building geometry, location, weather, occupancy, schedules, HVAC systems, utility data, sensor time series, calibration datasets, operational states, control recommendations, logs, reports, and simulation outputs may be sensitive.

Secrets, credentials, provider auth, API keys, local sessions, telemetry configs, registry auth, building data, and private operational data are excluded. No network/provider/API/MCP/auth activation occurs. Unknown sensitivity blocks publication and context exposure.

## 12. Dependency / External Source Posture
EnergyPlus and OpenStudio are external/domain evidence only. EnergyPlus dependency posture is unresolved. OpenStudio SDK/tooling posture is unresolved. Native runtime, package, license/name-use, notice, weather/data, binary, and environment posture must be reviewed later.

External source presence is not adoption. Dependency references are not dependency approval. Product-specific dependency adoption would not become root dependency adoption. P-09 will handle Product Dependency / External Source Posture.

## 13. Provider / API / MCP Posture
`backend-energyplus` may later expose APIs, SDK functions, job queues, command surfaces, or integration contracts only after governance. No provider/API/MCP/network/auth surface is activated by P-03.

MCP availability is not MCP activation. Tool availability is not permission. Provider credentials are not provider permission. Interface products may call backend contracts only after contracts, validation, security, and governance exist.

## 14. Generated Output / Data / Model / Artifact Posture
Generated IDF, epJSON, weather-derived files, schedules, EnergyPlus outputs, CSV/SQL/ESO-style outputs, reports, logs, normalized results, calibration datasets, batch datasets, surrogate handoff artifacts, model exports, and diagnostic summaries are generated-sensitive by default.

Generated solver artifacts and simulation outputs are evidence, not source by default. Raw output remains local-only until reviewed. Publication requires product, security, validation, dependency, and governance review.

## 15. Git Posture
Product Git posture is not changed by P-03. `2_products/` remains ignored/local-only. `backend-energyplus` source tracking is deferred to P-08.

P-03 does not stage, commit, push, force-add, or publish. Future Git action must use exact paths only. No `git add .`.

## 16. Validation Baseline Needs
Future baseline needs under V-04/P-01: product charter completeness checks; internal model schema checks; input validation checks; generated solver artifact provenance checks; EnergyPlus/OpenStudio dependency/license checks; weather/data sensitivity checks; simulation orchestration checks; result normalization checks; real-vs-sim comparison checks; calibration readiness checks; generated-output checks; security/access checks; API contract checks; and tests/builds/execution only after explicit future approval.

P-03 does not create or execute validation baselines. P-10 handles Product Validation Baseline.

## 17. Activation Blockers
| blocker | reason | required future action | blocks activation? |
| --- | --- | --- | --- |
| owner missing or not final | No accepted final owner. | Assign governed owner. | Yes |
| scope not validated | Scope is draft only. | Product scope review. | Yes |
| root/product boundary requires review | Backend can blur root authority. | Product/root boundary review. | Yes |
| EnergyPlus posture unresolved | Native solver, license, binaries, environment, and input/output risks. | P-09/dependency/license/runtime review. | Yes |
| OpenStudio posture unresolved | SDK/tooling/native/package/license risks. | Dependency/security review. | Yes |
| weather/data posture unresolved | Weather, schedules, building and sensor data may be sensitive/licensed. | Data/security/license review. | Yes |
| generated-output review missing | Solver artifacts and results may leak data or be overclaimed. | Output/provenance review. | Yes |
| product Git posture deferred to P-08 | Source tracking not approved. | P-08 Git posture decision. | Yes |
| dependency posture deferred to P-09 | Adoption not approved. | P-09 dependency posture. | Yes |
| validation baseline deferred to P-10 | Baseline absent. | P-10 baseline. | Yes |
| security/access review missing | Sensitive building/product data possible. | Security review. | Yes |
| API/interface contracts missing | Consumers cannot rely on backend contracts. | Backend/API contract review. | Yes |
| no implementation readiness assessment | Readiness not evaluated. | Future IR review. | Yes |
| no product governance activation decision | Governance has not activated. | Activation decision. | Yes |

## 18. Implementation Readiness Blockers
No implementation readiness exists. Blockers include no owner, no accepted product architecture, no source tracking decision, no dependency/license/runtime review, no validation baseline, no EnergyPlus/OpenStudio approval, no data/security posture, no API contracts, no generated-output provenance model, no calibration baseline, no test/build/run approval, no deployment posture, and no governance activation decision.

## 19. Evidence / Source References
Future charter claims must cite P-00 for selection, P-01 for common gate, P-02 for Omniverse/backend and EnergyPlus solver boundaries, M-07 for product charter-prep posture, M-06/W-13/V-05 for dependency/external posture, W-12 for product policy, V-04 for product validation posture, S-series for local-only/security, CSS-series for substrate/naming, H-series/M-04 for runtime/tool/provider/MCP boundary, and Siamese Product Vision for strategic product context.

Evidence supports review; evidence does not approve activation.

## 20. Gate Checklist
| Gate | P-03 status | Note |
| --- | --- | --- |
| GATE-01 selected candidate exists in P-00 | pass | P-00 selected `backend-energyplus`. |
| GATE-02 owner declared or owner gap recorded | pass_with_caution | Owner gap recorded. |
| GATE-03 purpose declared | pass | Energy-domain backend candidate for Siamese. |
| GATE-04 scope declared | pass_with_caution | Draft scope; needs validation. |
| GATE-05 non-goals declared | pass | Solver/source-of-truth/runtime exclusions declared. |
| GATE-06 product/root boundary declared | pass | Product-scoped only. |
| GATE-07 local-only posture declared | pass | `2_products/` remains ignored/local-only. |
| GATE-08 security posture declared | pass_with_caution | Sensitive building/data/output risk. |
| GATE-09 dependency posture declared | blocked | EnergyPlus/OpenStudio/native/license unresolved. |
| GATE-10 external-source posture declared | pass_with_caution | External/domain evidence only. |
| GATE-11 Git posture declared or deferred to P-08 | pass_with_caution | Deferred to P-08. |
| GATE-12 validation baseline need declared | pass_with_caution | Deferred to P-10. |
| GATE-13 generated-output posture declared | pass_with_caution | Generated-sensitive by default. |
| GATE-14 provider/API/MCP posture declared | pass_with_caution | Future contracts only after governance. |
| GATE-15 activation blockers declared | pass | Blockers listed. |
| GATE-16 implementation-readiness blockers declared | pass | Blockers listed. |
| GATE-17 governance decision path declared | pass_with_caution | Governance required; owner gap remains. |
| GATE-18 stop rules declared | pass | Stop before P-04 and all forbidden actions. |

Final gate status: `gate_passed_with_cautions_for_charter_review_only`. This gate status does not activate the product.

## 21. Backend-specific Gate Overlay
| overlay item | current posture | blocker | future route |
| --- | --- | --- | --- |
| EnergyPlus solver | Unapproved external/domain evidence. | Native/runtime/license/input-output risk. | P-09 dependency/runtime review. |
| OpenStudio SDK/tooling | Unapproved external/domain evidence. | SDK/native/package/license risk. | Dependency/security review. |
| Internal energy model | Future product scope. | Schema/validation absent. | Product architecture review. |
| IDF/epJSON generation | Future generated artifact path. | Provenance/source-of-truth risk. | Artifact provenance baseline. |
| Simulation orchestration | Future backend capability. | Execution/job/output risk. | Runtime/security/validation review. |
| Result normalization | Future backend capability. | Accuracy/provenance risk. | Validation/data contract. |
| Real-data comparison | Future backend capability. | Sensor/data sensitivity. | Data/security/calibration review. |
| Calibration preparation | Future backend capability. | Baseline and method absent. | Product validation baseline. |
| Batch datasets | Future generated artifacts. | Data/model leakage and storage risk. | Dataset/artifact review. |
| Surrogate handoff | Future model interface. | Model/data provenance absent. | Model/artifact governance. |
| Control integration | Future only. | Safety/operational risk. | Control/security governance. |
| API/SDK contracts | Future only. | Consumer contracts absent. | Governed backend API review. |

## 22. Residual Risks
Residual risks: no active product owner, source review, dependency/license review, EnergyPlus/OpenStudio approval, native runtime review, internal model schema, API contract, validation baseline, weather/data posture, calibration method, generated-output publication policy, Git posture decision, implementation readiness, or product activation decision.

## 23. P-03 Invariants
| ID | Invariant |
| --- | --- |
| P03-001 | Backend EnergyPlus charter is not product activation. |
| P03-002 | Backend Python owns energy-domain logic inside future governed product scope. |
| P03-003 | EnergyPlus is solver, not internal model or source of truth. |
| P03-004 | IDF/epJSON are generated solver artifacts, not platform source of truth. |
| P03-005 | Omniverse app, CLI, desktop, and web-platform consume governed backend contracts only. |
| P03-006 | Product source remains local-only. |
| P03-007 | Product Git posture is not changed. |
| P03-008 | Product dependencies are not adopted. |
| P03-009 | Product validation baseline is not created. |
| P03-010 | Generated solver output is not source by default. |
| P03-011 | Product needs do not decide root architecture. |
| P03-012 | Product needs do not decide Cognitive Semantic System substrate. |
| P03-013 | Graph remains a candidate only. |
| P03-014 | Validation evaluates; governance decides. |
| P03-015 | P-03 stops before P-04. |

## 24. Anti-patterns
Anti-patterns: EnergyPlus as internal platform model; IDF/epJSON as source of truth; simulation output as truth without validation; OpenStudio adoption by proximity; native solver execution by curiosity; package install to inspect; backend product as root architecture; product dependency as root dependency; interface products owning backend energy logic; generated datasets or surrogate artifacts as source without review; product charter as activation; product source inspection by curiosity; starting P-04 inside P-03; `git add .`.

## 25. Readiness For P-04
P-04 - CLI Product Charter is ready after explicit instruction if P-03 Backend EnergyPlus Product Charter exists, `backend-energyplus` remains inactive, backend/interface boundaries are preserved, EnergyPlus solver boundary is preserved, product/local-only/Git/dependency/security boundaries are preserved, and no product activation, source tracking, dependency adoption, provider/API/MCP activation, publication, or implementation is implied.

Do not create P-04.

## 26. Final Verdict
| Question | Answer |
| --- | --- |
| What does P-03 create? | One inactive Backend EnergyPlus Product Charter draft. |
| What is backend-energyplus in Siamese? | The energy-domain backend candidate for internal energy modeling, EnergyPlus compilation/running, normalization, calibration readiness, datasets, API contracts, and future control integration. |
| Did P-03 activate backend-energyplus? | No. |
| Did P-03 inspect product source deeply? | No. |
| Did P-03 run EnergyPlus/OpenStudio or install dependencies? | No. |
| Did P-03 change product Git posture? | No. |
| Did P-03 adopt dependencies? | No. |
| Did P-03 create validation baselines? | No. |
| Did P-03 define interface product behavior? | No. Interface products consume governed backend contracts only. |
| What remains blocked? | Activation, source inspection, EnergyPlus/OpenStudio/native dependency adoption, runtime execution, package managers, product Git tracking, validation baselines, API contracts, generated-output publication, implementation readiness, provider/API/MCP/network/auth activation, staging, commit, push, and P-04. |
| Is P-04 ready after explicit instruction? | Yes, as CLI Product Charter drafting only; P-04 is not started. |

Stop after P-03 validation and report. Do not start P-04 or any later ticket.
