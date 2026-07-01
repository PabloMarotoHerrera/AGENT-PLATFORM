# P-10 - Product Validation Baseline
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Product Validation Baseline |
| Ticket | P-10 |
| Status | Accepted product validation baseline definition |
| Date | 2026-07-01 |
| Scope | Canonical validation baseline for inactive Siamese product workspaces after P-00 through P-09. |
| Authority | Baseline definition only; not validation execution, automation, product activation, dependency adoption, source tracking, publication, or implementation readiness. |
| Related documents | P-00 through P-09, M-07, W-11, W-12, W-13, V-01, V-02, V-04, V-05, V-A, S-series, H-series, CSS-series, `.gitignore`, `README.md`, Siamese Product Vision |

## 2. Purpose
P-10 defines what future product validation must check before any Siamese product can request activation, implementation readiness, source tracking, dependency adoption, publication, or product validation execution.

This document closes the validation-baseline gap recorded in P-00 through P-09. It does not run product tests, builds, package managers, products, solvers, servers, providers, APIs, MCP, network calls, installs, or validation automation.

## 3. Product Validation Baseline Definition
A product validation baseline is a product-scoped checklist of future validation criteria, evidence, proof targets, blockers, limitations, revalidation triggers, and stop rules.

The baseline defines what validation would evaluate. It does not prove product behavior, approve activation, approve dependency adoption, authorize execution, change Git posture, or make product docs root authority.

## 4. Scope And Non-scope
| In scope | Out of scope |
| --- | --- |
| Baseline criteria for `omniverse-app`, `backend-energyplus`, `cli`, `desktop`, `web-platform`, and `experimental`. | Product source inspection, execution, tests, builds, package-manager actions, installs, provider/API/MCP/network/auth use, deploys, simulations, or native binaries. |
| Evidence and proof mapping for future validation. | Validation registry, schemas, runners, CI, automation, scripts, enforcement, implementation artifacts, or generated outputs. |
| Blockers, incidents, matrices, and readiness gates. | Product activation, product Git/source tracking approval, dependency adoption, external-source adoption, publication, staging, commit, push, or P-A start. |

## 5. Authority Boundary
| Layer | P-10 rule |
| --- | --- |
| Governance | Decides activation, implementation readiness, source tracking, dependency adoption, publication, exceptions, and lifecycle. |
| Validation | Evaluates scoped criteria and evidence; it does not approve action. |
| Security | Blocks unsafe access, secrets, credentials, local-only exposure, execution, provider/API/MCP/network/auth, and publication. |
| Evidence | Supports review only when source status, sensitivity, scope, method, freshness, limitations, and stop rule are explicit. |
| Product charters | Remain product-scoped and cannot define AGENT PLATFORM root authority. |
| Agents | May define this baseline; cannot run products, inspect source deeply, adopt dependencies, mutate Git, publish, activate products, or start P-A. |

## 6. Source Boundary
P-10 uses accepted documentation only: P-00 through P-09, M-07, W-11, W-12, W-13, V-series product/external/proof/evidence models, V-A, S-series, H-series, CSS-series, `.gitignore`, `README.md`, and Siamese Product Vision statements already captured in product charters.

Raw `2_products/`, raw `4_external/sources/`, `previusknowledge/`, datasets, models, artifacts, generated outputs, product logs, secrets, credentials, dependency folders, and runtime state are not inspected. Product names, states, and blockers are retained as safe metadata only.

## 7. Input Baseline
| Input | Current P-10 use |
| --- | --- |
| P-00 | Product route and selection evidence. |
| P-01 | Common gate fields and GATE-01 through GATE-18. |
| P-02 through P-06 | Inactive product charter drafts and per-product baseline needs. |
| P-07 | `experimental` blocked local-only disposition. |
| P-08 | Product governance docs may be trackable as docs only; product source remains local-only. |
| P-09 | Dependencies and external sources remain candidate/evidence only; no adoption. |
| V-04 | Product validation model, proof use, blockers, incidents, and baseline components. |
| V-01/V-02/V-05/V-A | Proof, evidence, external-source, and audit constraints. |
| W/S/H/CSS-series | Governance, product policy, external handling, security, execution, harness, naming, and substrate boundaries. |

## 8. Product Inventory And State
| Product | Siamese role | Current state | Baseline posture | Current activation posture |
| --- | --- | --- | --- | --- |
| `omniverse-app` | Visual/operational Omniverse Kit interface. | candidate/deferred/local_only/inactive | Baseline defined; execution blocked. | Blocked. |
| `backend-energyplus` | Energy-domain backend candidate. | candidate/deferred/local_only/inactive | Baseline defined; solver execution blocked. | Blocked. |
| `cli` | Operator/scriptable interface. | candidate/deferred/local_only/inactive | Baseline defined; command execution blocked. | Blocked. |
| `desktop` | Local packaged/interface candidate. | candidate/deferred/local_only/inactive | Baseline defined; desktop runtime blocked. | Blocked. |
| `web-platform` | Browser/deployed interface candidate. | candidate/deferred/local_only/inactive | Baseline defined; build/deploy/auth blocked. | Blocked. |
| `experimental` | Ambiguous sandbox/prototype candidate. | experimental/blocked/local_only/inactive | Baseline defined for disposition only. | Blocked. |

## 9. Product Vision And Root Boundary
Siamese is the product vision context: a living energy twin platform for buildings connecting an energy model to real data, calibration, prediction, recommendation/control, and continuous operation.

Siamese product validation remains product-scoped. AGENT PLATFORM root authority, governance, validation architecture, security policy, and the Cognitive Semantic System remain root-governed. Product needs may inform proposals but cannot decide root architecture. Graph remains a candidate substrate only.

## 10. Validation Layers
| Layer | Required future check | P-10 posture |
| --- | --- | --- |
| L0 route/state | Candidate selected or dispositioned and inactive state preserved. | Defined. |
| L1 charter/common gate | P-01 required fields and product charter gaps reviewed. | Defined. |
| L2 scope/root boundary | Product scope, non-goals, and root boundary coherent. | Defined. |
| L3 security/local-only | Secrets, credentials, sensitivity, access, generated output, and local-only posture reviewed. | Defined. |
| L4 Git posture | Product docs/source/generated output tracking posture checked against P-08. | Defined; no Git change. |
| L5 dependency/external | Candidate dependencies reviewed against P-09 and V-05 without adoption. | Defined. |
| L6 data/model/artifact | Product data, models, artifacts, logs, reports, and outputs handled as local-only/generated-sensitive. | Defined. |
| L7 interface/contracts | Backend/API/command/UI/runtime contracts checked as future governance targets. | Defined. |
| L8 execution/test | Exact future tests/builds/runs only after explicit command approval. | Blocked now. |
| L9 readiness audit | Structured product readiness audit after evidence exists. | Future only. |

## 11. Evidence Requirements
Future product validation evidence must include product ID, source document references, source status, sensitivity, scope, owner posture, charter status, root-boundary statement, dependency posture, security/access posture, generated-output posture, Git posture, validation method, result, limitations, residual risks, blockers, reviewer/date, revalidation trigger, and stop rule.

Use references and safe summaries over copied content. Do not retain secret or credential values. Do not copy raw product source, raw external source code, generated logs, datasets, models, artifacts, or local-only material into root docs.

## 12. Proof Level Mapping
| Proof level | Product baseline use | Current P-10 ceiling |
| --- | --- | --- |
| PL-0 | Missing evidence or explicit blocker. | Allowed as gap state. |
| PL-1 | Path, file, Git, ignore, or metadata checks. | Allowed for bounded document/path validation. |
| PL-2 | Product state, source status, sensitivity, local-only posture. | Allowed through document review. |
| PL-3 | Charter citations and provenance references. | Allowed through document review. |
| PL-4 | Coherence review across charters, validation, security, Git, dependency, and governance rules. | Target for this baseline definition. |
| PL-5 | Exact bounded metadata/Git/naming commands. | Allowed only for P-10 document validation. |
| PL-6 | Product tests/builds/execution for named scope. | Not used by P-10; future exact approval only. |
| PL-7 | Structured product readiness audit. | Future only. |
| PL-8 | Reproduced product readiness audit or validation. | Future only. |

No proof level approves activation, dependency adoption, source tracking, implementation, publication, execution, or root authority.

## 13. Common Baseline Checklist
| Check | Required future evidence | Blocks if missing now? |
| --- | --- | --- |
| Candidate route | P-00 selection or P-07 disposition. | Yes. |
| Owner | Named owner or owner gap with governance path. | Yes for activation. |
| Purpose/scope/non-goals | Product charter fields and limitations. | Yes for activation. |
| Root boundary | Product cannot define AGENT PLATFORM root or Cognitive Semantic System. | Yes. |
| Local-only posture | `2_products/` ignored/local-only and product material excluded. | Yes. |
| Security/access | Secrets, credentials, local data, unknown sensitivity, generated output risks. | Yes. |
| Dependency/external | P-09 candidate-only posture and future review route. | Yes. |
| Git posture | P-08 docs-only/source-local-only posture. | Yes. |
| Generated output | Generated-sensitive, not source by default. | Yes. |
| API/provider/MCP/network/auth | Blocked unless future governed approval exists. | Yes. |
| Test/build/run strategy | Exact future command approval required. | Yes for execution. |
| Governance path | Approver/decision route declared. | Yes. |

## 14. Acceptance Criteria Model
Future acceptance criteria must be product-specific, scoped, observable, cited, and paired with limitations. They must state what passes, what fails, what remains untested, what evidence is retained, and what future governance decision the evidence may support.

P-10 itself accepts only that the baseline exists, is coherent with P-00 through P-09 and V-04, preserves blockers, and avoids execution or posture changes.

## 15. Target Behavior And Non-goals
Future validation may define target behavior only as a candidate to be checked later. Target behavior cannot be inferred from folder existence, charter text, dependency relevance, generated output, or product vision.

Non-goals for every product baseline: no root authority, no product activation, no source tracking, no dependency adoption, no external source adoption, no publication, no implementation readiness, no execution, no provider/API/MCP/network/auth activation, and no Cognitive Semantic System substrate decision.

## 16. Test, Build, And Execution Strategy
The current strategy is documentation-only baseline definition. Product tests, builds, launches, simulations, package managers, dev servers, desktop runtimes, CLI commands, web deploys, native binaries, notebooks, and generated commands are blocked now.

Future execution requires exact command, working directory, purpose, expected output, side effects, dependency/network/auth posture, product scope, output handling, rollback/cleanup, validation criteria, and explicit approval. Passing future tests would remain product-scoped evidence only.

## 17. Manual Review Strategy
Future manual review must compare each product against P-01 gates, its charter/disposition, P-08 Git posture, P-09 dependency posture, V-04 product validation, V-05 external-source validation, S-series security, H-series runtime/tool boundaries, and CSS-series naming/substrate neutrality.

Manual review must record files reviewed, files not reviewed, criteria, findings, uncertainty, contradictions, blockers, residual risks, and revalidation triggers.

## 18. Generated Output Baseline
Generated product outputs are generated-sensitive by default: screenshots, USD layers, heatmaps, IDF/epJSON, solver outputs, logs, CLI stdout/stderr, reports, caches, desktop crash dumps, web bundles, dashboard exports, datasets, model artifacts, and generated docs.

Generated output is evidence, not source by default. Publication or tracking requires product, security, validation, dependency, Git, and governance review.

## 19. Security And Local-only Baseline
`2_products/` remains local-only. Product source, product docs outside governed architecture docs, product generated outputs, dependencies, logs, configs, local sessions, datasets, models, artifacts, secrets, credentials, tokens, provider auth, registry auth, and environment files remain excluded by default.

Unknown sensitivity blocks exposure, context inclusion, publication, execution, and Git tracking. Secret and credential values must never be retained, copied, summarized, validated, or used.

## 20. Dependency And External Baseline
P-09 remains in force: no product dependency, external source, source reuse, package, runtime, SDK, native tool, provider, API, MCP, network, or auth use is adopted by this baseline.

Future dependency validation must identify product scope, owner, dependency class, exact version/source, provenance, license/notice/name-use, security posture, transitive dependencies, package scripts, runtime behavior, network/auth/provider/MCP behavior, data/output posture, rollback/removal path, validation plan, and governance decision.

## 21. Data, Model, And Artifact Baseline
Building data, sensor data, occupancy, schedules, weather, utility data, operational state, calibration datasets, batch datasets, surrogate artifacts, local caches, browser storage, desktop local DBs, reports, screenshots, and exports are sensitive until reviewed.

Data/model/artifact validation must prove provenance, license, sensitivity, intended use, retention, storage, publication posture, and product scope before any use, training, execution, publication, or tracking can be considered.

## 22. Git Baseline
P-08 remains in force. Product governance docs under `0_architecture/product_workspaces/` may be trackable as docs only after exact human approval. Product source under `2_products/` remains ignored/local-only and not trackable now.

Git status, diff, and check-ignore output may be evidence only. P-10 does not modify `.gitignore`, stage, commit, push, force-add, publish, or approve product source tracking. Broad staging and `git add .` remain blocked.

## 23. Provider, API, MCP, Network, And Auth Baseline
Provider/API/MCP/network/auth availability is not permission. Backend contracts, Omniverse/Nucleus auth, web auth, desktop IPC/services, CLI command surfaces, hosting, telemetry, analytics, package registries, cloud services, OAuth, cookies, TLS, and deployment providers are future governance targets only.

No provider, API, MCP server, network call, authentication flow, credential use, dev server, local daemon, or service connection is activated by P-10.

## 24. Per-product Baseline: `omniverse-app`
Future validation must check charter completeness, visual/operational interface scope, backend/API boundary, Omniverse Kit as interface only, OpenUSD as geometry/semantic representation only, no heavy time-series in USD by default, generated visual-output provenance, SDK/license/name-use posture, GPU/runtime/Nucleus/auth posture, building-data sensitivity, and packaging/publication blockers.

Current verdict: baseline defined for future review; Kit launch, SDK install, Nucleus/auth use, GPU/runtime execution, backend calls, product source tracking, generated-output publication, activation, and implementation readiness remain blocked.

## 25. Per-product Baseline: `backend-energyplus`
Future validation must check charter completeness, internal energy model scope, input normalization, EnergyPlus input artifact provenance, result normalization, weather/data sensitivity, real-vs-sim comparison criteria, calibration readiness, API/SDK contract posture, EnergyPlus/OpenStudio license/runtime/native posture, and generated solver output handling.

Current verdict: baseline defined for future review; EnergyPlus/OpenStudio execution, solver adoption, package/native runtime adoption, simulations, API activation, source tracking, activation, and implementation readiness remain blocked. EnergyPlus is solver, not internal model.

## 26. Per-product Baseline: `cli`
Future validation must check charter completeness, command taxonomy, shell boundary, argument/path validation, backend contract use, output redaction/provenance, command history/log sensitivity, config/env handling, package/runtime posture, help/docs accuracy, and generated report/export handling.

Current verdict: baseline defined for future review; CLI execution, shell commands, package managers, backend calls, MCP/tool activation, source tracking, activation, and implementation readiness remain blocked. Shell availability is not command approval.

## 27. Per-product Baseline: `desktop`
Future validation must check charter completeness, desktop UX/scope, runtime/framework posture, installer/updater/signing/notarization posture, OS permissions, local storage/cache policy, logs/crash reports/telemetry, backend API contracts, local data sensitivity, generated screenshots/reports, and packaging/distribution blockers.

Current verdict: baseline defined for future review; desktop app execution, local daemon/service activation, framework/package adoption, installer/updater/signing approval, source tracking, activation, and implementation readiness remain blocked.

## 28. Per-product Baseline: `web-platform`
Future validation must check charter completeness, browser/deployed interface scope, package/build/runtime posture, backend API contracts, auth/session/cookie posture, user/account/tenant privacy, browser cache/storage, hosting/CDN/domain/TLS/email posture, telemetry/analytics, accessibility/browser compatibility, security headers/CORS/CSRF, generated exports/screenshots, and deployment blockers.

Current verdict: baseline defined for future review; dev server, build, package manager, deploy, auth/session, hosting, provider/API/network use, source tracking, activation, and implementation readiness remain blocked.

## 29. Per-product Baseline: `experimental`
Future validation must check disposition completeness, owner/purpose/scope gaps, classification, product/root boundary, local-only posture, security/access risk, generated-output posture, dependency/external posture, split-review criteria, archive-candidate criteria, rejection/deferral criteria, and incident restrictions.

Current verdict: baseline defined for disposition review only; product chartering, source inspection, split, archive execution, deletion, movement, dependency adoption, source tracking, activation, and implementation readiness remain blocked.

## 30. Readiness Gates
| Gate | Pass condition | Current posture |
| --- | --- | --- |
| PVG-01 baseline exists | P-10 document accepted. | Defined by this file. |
| PVG-02 candidate documented | P-00 route or P-07 disposition exists. | Satisfied for safe metadata. |
| PVG-03 owner final | Product owner accepted. | Blocking gap. |
| PVG-04 scope accepted | Product scope/non-goals/root boundary accepted. | Draft only; blocking. |
| PVG-05 Git posture safe | P-08 preserved and no product source staged/tracked. | Local-only; activation still blocked. |
| PVG-06 dependency posture safe | P-09 candidate-only posture preserved. | Adoption blocked. |
| PVG-07 security reviewed | Product security/access posture reviewed for exact scope. | Blocking gap. |
| PVG-08 generated output reviewed | Output provenance/sensitivity accepted. | Blocking gap. |
| PVG-09 execution approval | Exact future commands approved if needed. | Not approved. |
| PVG-10 governance decision | Activation/readiness/source/adoption decision recorded. | Not approved. |

## 31. Matrices
### Matrix A. Product Vs Highest Validation Risk
| Product | Highest current risk | Future validation focus |
| --- | --- | --- |
| `omniverse-app` | SDK/runtime/GPU/license/output. | Interface, OpenUSD binding, generated visuals, backend contract. |
| `backend-energyplus` | Native solver/license/data/output. | Energy model, solver artifact provenance, calibration/API readiness. |
| `cli` | Command/shell/package/user data. | Command safety, argument validation, output redaction. |
| `desktop` | Runtime/packaging/local data. | Local storage, OS permissions, signing/update posture. |
| `web-platform` | Auth/data/build/deploy. | Auth/privacy/deploy/build/security posture. |
| `experimental` | Ambiguous scope/source/sensitivity. | Classification, disposition, split/archive eligibility. |

### Matrix B. Baseline Area Vs Proof Target
| Area | Minimum future proof | P-10 limitation |
| --- | --- | --- |
| Route/state/Git/local-only | PL-1/PL-2/PL-5 when bounded. | Metadata only. |
| Charter/scope/root boundary | PL-3/PL-4. | Draft coherence only. |
| Security/dependency/generated output | PL-4, PL-7 before high-risk decisions. | No adoption or execution. |
| Product behavior | PL-6 only after exact future approval. | Not tested. |
| Readiness audit | PL-7/PL-8 later. | Not performed. |

## 32. Blocker Register
| Blocker | Stop behavior | Required future action |
| --- | --- | --- |
| Owner missing or not final | Stop activation/readiness claim. | Assign governed owner. |
| Scope/root boundary draft only | Stop product authority claim. | Accept scope, non-goals, and root boundary. |
| Product source local-only | Stop source tracking or publication. | Future exact Git/source governance. |
| Dependency/external posture blocked | Stop adoption/install/runtime claim. | Future product dependency review. |
| Security/access review missing | Stop exposure, execution, publication, or context expansion. | Product security review. |
| Generated-output posture missing | Stop output use/publication. | Provenance/sensitivity review. |
| API/contract missing | Stop interface behavior claim. | Governed backend/API/command contracts. |
| Execution approval missing | Stop tests/builds/runs. | Exact future command approval. |
| Implementation readiness absent | Stop implementation path. | Future IR governance. |
| Product activation decision absent | Stop activation. | Product governance decision. |
| P-A scope pressure | Stop adjacent work. | Wait explicit P-A instruction after P-10 report. |

## 33. Incident Handling
Incidents include product or external source execution, package install, solver/native/web/desktop/CLI runtime launch, dev server/build/deploy, provider/API/MCP/network/auth use, credential exposure, deep product/external source inspection, source copying, dependency adoption by wording, product source staging, `.gitignore` modification, generated output treated as source, product activation implied, or P-A started.

Response: STOP, preserve safe metadata only, do not continue adjacent work, do not expose secrets or local-only content, do not stage/commit/push, and require human/security/product/governance decision.

## 34. Invariants And Anti-patterns
| ID | Invariant |
| --- | --- |
| P10-001 | Product validation baseline is not validation execution. |
| P10-002 | Validation evaluates; governance decides. |
| P10-003 | Product proof is product-scoped. |
| P10-004 | Product source remains local-only. |
| P10-005 | Product dependencies and external sources are not adopted. |
| P10-006 | Product generated output is not source by default. |
| P10-007 | Product needs do not decide AGENT PLATFORM root authority or Cognitive Semantic System substrate. |
| P10-008 | Graph remains a candidate only. |
| P10-009 | No product activation, implementation readiness, publication, Git mutation, or P-A start occurs in P-10. |

Anti-patterns: baseline as activation; baseline as test pass; charter as behavior proof; dependency relevance as adoption; license evidence as reuse approval; Git ignore as security proof; Git tracking as product readiness; generated output as source; CLI command as shell permission; web charter as deploy approval; desktop charter as installer approval; EnergyPlus as internal model; Omniverse Kit as backend; graph/product visualization as substrate decision; broad staging; `git add .`; starting P-A inside P-10.

## 35. P-A Readiness And Stop Rule
P-A is ready after explicit instruction only if this P-10 baseline exists, product source remains local-only, P-08 Git posture remains unchanged, P-09 dependency/external posture remains candidate-only, no product validation execution occurred, no dependencies were adopted, no products were activated, and no implementation readiness or publication was approved.

P-10 final verdict: the canonical Product Validation Baseline is defined for future review. Product activation, source tracking, validation execution, tests, builds, package managers, installs, providers, APIs, MCP, network/auth use, dependency adoption, external-source adoption, implementation readiness, publication, staging, commit, push, and P-A remain blocked.

Stop after P-10 validation and report. Do not start P-A or any later ticket.
