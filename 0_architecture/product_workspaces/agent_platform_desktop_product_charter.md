# P-05 - Desktop Product Charter
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Desktop Product Charter |
| Ticket | P-05 |
| Product candidate | `desktop` |
| Status | Accepted inactive Desktop product charter draft |
| Date | 2026-07-01 |
| Scope | Inactive charter draft for Siamese's future local desktop/interface candidate. |
| Authority | Product charter draft only, not product activation. |
| Related documents | P-00, P-01, P-02, P-03, P-04, M-A, M-07, M-06, W-12, V-04, W-13, V-05, S-series, CSS-series, H-series, Siamese Product Vision |

## 2. Purpose
P-00 selected `desktop` for charter drafting. P-01 defined the common product charter template and common gate. P-02 preserved Omniverse/interface boundaries. P-03 preserved backend/interface boundaries. P-04 preserved CLI/shell/command boundaries. P-05 drafts the inactive `desktop` charter.

`desktop` is Siamese's future local desktop/interface candidate. Desktop is local interface/runtime candidate, not backend. It must consume governed backend contracts only and must not become Omniverse Kit, CLI, web-platform, a local daemon, a free runtime launcher, or a direct EnergyPlus runner.

P-05 does not activate the product, inspect source deeply, run desktop apps, install desktop frameworks/packages/SDKs/native tools/dependencies, change Git posture, create validation baselines, create runtime behavior, create implementation artifacts, or start P-06. It prepares P-06 - Web Platform Product Charter for explicit future instruction only.

## 3. Product Candidate Summary
| Field | Value |
| --- | --- |
| product_id | PROD-003 / P00-SEL-004 |
| product_name | `desktop` |
| product_platform_name | Siamese |
| product_status | candidate/deferred/local_only/inactive |
| selection_source | P-00 |
| charter_template_source | P-01 |
| boundary_sources | P-02 Omniverse App, P-03 Backend EnergyPlus, P-04 CLI |
| likely area | desktop/local runtime/interface |
| main risk | runtime/packaging/local-data/security/generated-output/Git/API/root-boundary |
| current verdict | draft_for_charter_review_with_blockers |
| blocked inference | Product activation, desktop runtime approval, installer approval, dependency approval, source tracking, implementation readiness, desktop behavior approval. |

## 4. Product Vision Alignment
Siamese is a living energy twin platform for buildings. Siamese keeps the energy model alive by connecting an internal energy model to real data, calibration, prediction, recommendation/control, and continuous operation.

`desktop` may later provide a local app surface for Siamese project work where a full Omniverse workflow is not required. Future workflows may include project opening, local workspace management, backend job/status/result views, diagnostics, settings, safe import/export requests, and report viewing. Desktop must remain decoupled from energy logic and must call governed backend contracts only.

Clarifications:
| Surface | Siamese role | P-05 boundary |
| --- | --- | --- |
| Desktop | Local packaged/interface candidate. | Product interface only; no backend ownership. |
| Backend Python | Energy-domain logic, validation, simulation orchestration, result normalization, calibration readiness, datasets, API/SDK, and future control integration. | Backend owns energy logic. |
| Omniverse App | Advanced visual/3D Omniverse interface. | Not desktop runtime by default. |
| CLI | Textual/operator interface. | Not desktop shell or replacement runtime. |
| Web Platform | Browser/deployed interface. | Not local desktop runtime. |
| Local storage/cache/config | Local app state. | Sensitive by default. |
| Desktop runtime/framework | Future stack decision. | Not accepted by charter. |

## 5. Owner / Governance
Owner is not finalized because no accepted source declares a final owner. P-05 records an owner gap.

Governance must decide activation, Git posture, dependency adoption, publication, desktop runtime stack, packaging, distribution, execution permission, and implementation readiness. P-05 cannot assign final owner authority or approve desktop product work.

## 6. Product Scope
Future `desktop` charter scope may include: desktop product purpose and local interface boundaries; future local project workspace UX; future backend job, status, and result interaction through governed API/SDK contracts; future diagnostics and validation request surfaces; future settings/configuration UI after security governance; future report/export viewing; future local cache/storage posture as design candidate only; future offline/edge mode as governed design candidate only; future notifications or background behavior as governed candidate only; future integration with `backend-energyplus` contracts; and future alignment with `omniverse-app`, `cli`, and `web-platform` boundaries.

Out of scope: backend energy logic; EnergyPlus direct runner; Omniverse Kit runtime; arbitrary CLI/shell execution; browser/deployed web behavior; local daemon implementation; installer/updater implementation; local database/cache implementation; OS service/background worker implementation; native packaging/distribution approval; dependency adoption; validation baseline execution; implementation readiness; and provider/API/network/MCP/auth activation.

## 7. Non-Goals
Non-goals: do not make desktop the backend; do not make desktop own energy-domain logic; do not make desktop a wrapper that bypasses backend contracts; do not make desktop a free local runtime launcher; do not make desktop a shell/CLI replacement; do not make desktop an Omniverse substitute by implication; do not adopt Electron/Tauri/Qt/PySide/.NET/native stack by relevance; do not approve installers, updaters, code signing, local services, or auto-start behavior; do not treat desktop local cache/output as source by default; do not activate runtime, package managers, APIs, MCP, hooks, or tools.

## 8. Product / Root Boundary
`desktop` is product-scoped. It does not define AGENT PLATFORM root authority, the Cognitive Semantic System, backend truth, validation truth, governance truth, Git truth, execution truth, dependency truth, local storage truth, or publication truth.

Product decisions can inform future root proposals but cannot silently constrain root architecture. Desktop runtime/packaging decisions remain product-scoped unless governed otherwise. Graph remains a candidate only.

## 9. User / Domain / Interface Hypothesis
| Hypothesis | Expected use | Validation posture |
| --- | --- | --- |
| Energy engineer | Local project review, diagnostics, result summaries, and report viewing. | Hypothesis only. |
| Facility/operator | Local status dashboard and recommendations if governed later. | Hypothesis only. |
| Researcher/university | Local living-lab workstation workflow after validation/security governance. | Hypothesis only. |
| Developer/operator | Local desktop wrapper for governed backend operations. | Hypothesis only. |
| Non-technical user | Simpler app surface than CLI or Omniverse where appropriate. | Hypothesis only. |

These are hypotheses, not validated behavior, execution, safety, usability, or market claims.

## 10. Current Local-only Posture
`desktop` source, if present under `2_products/`, remains local-only and ignored. P-05 does not inspect product source. P-05 uses safe metadata only.

Local sessions, configs, generated outputs, logs, credentials, dependency folders, build outputs, installers, caches, local DBs, crash dumps, reports, and product artifacts remain excluded unless governed later.

## 11. Security / Access Posture
Desktop project paths, local workspaces, backend URLs, building data, sensor data, reports, screenshots, logs, local DB/cache, config files, credentials, tokens, crash reports, telemetry, and generated exports may be sensitive.

Secrets, credentials, tokens, provider auth, package registry auth, local sessions, telemetry configs, API keys, Nucleus/cloud auth, and environment variables are excluded. No desktop runtime/provider/API/MCP/network/auth activation occurs. Unknown sensitivity blocks publication and context exposure. Local cache, logs, crash reports, generated reports, and desktop outputs are local-only by default.

## 12. Dependency / External Source Posture
Desktop framework/runtime dependency posture is unresolved. Electron/Tauri/Qt/PySide/.NET/native packaging posture is unresolved unless future governance selects a stack. Installer/updater/signing/notarization posture is unresolved. OS compatibility posture is unresolved. GPU/OpenUSD/Omniverse dependencies are unresolved if considered. External GUI/runtime/package libraries are not adopted.

Dependency references are not dependency approval. External source presence is not adoption. Product-specific dependency adoption would not become root dependency adoption. P-09 will handle Product Dependency / External Source Posture.

## 13. Provider / API / MCP Posture
`desktop` may later call backend APIs or SDK functions only after governed contracts exist. `desktop` may later use local IPC, local services, websocket, REST, or file watchers only after security and validation review. No provider/API/MCP/network/auth is activated by P-05.

MCP availability is not MCP activation. Tool availability is not permission. Local daemon availability is not execution approval. Provider credentials are not provider permission. Backend service modes are future scope.

## 14. Generated Output / Data / Model / Artifact Posture
Desktop screenshots, local caches, logs, diagnostics, validation summaries, simulation job summaries, report exports, downloaded files, JSON/CSV outputs, crash dumps, settings snapshots, installer artifacts, and generated documentation are generated-sensitive by default.

Generated output is evidence, not source by default. Raw output remains local-only until reviewed. Publication requires product, security, validation, dependency, and governance review.

## 15. Git Posture
Product Git posture is not changed by P-05. `2_products/` remains ignored/local-only. `desktop` source tracking is deferred to P-08.

P-05 does not stage, commit, push, force-add, or publish. Future Git action must use exact paths only. No `git add .`.

## 16. Validation Baseline Needs
Future baseline needs under V-04/P-01: product charter completeness checks; desktop UX/scope checks; local-only checks; dependency/package/license checks; generated-output checks; security/access checks; local storage/cache checks; installer/updater/signing checks; OS permission checks; backend/API contract checks; sensitive path/secret redaction checks; logging/crash-report checks; and launch/build/package tests only after explicit future approval.

P-05 does not create or execute validation baselines. P-10 handles Product Validation Baseline.

## 17. Activation Blockers
| blocker | reason | required future action | blocks activation? |
| --- | --- | --- | --- |
| owner missing or not final | No accepted final owner. | Assign governed owner. | Yes |
| scope not validated | Scope is draft only. | Product scope review. | Yes |
| root/product boundary requires review | Desktop interface can blur local authority. | Product/root boundary review. | Yes |
| desktop runtime/framework unresolved | Runtime stack is undecided. | P-09/dependency/runtime review. | Yes |
| packaging/installer/updater/signing unresolved | Distribution and update risk. | Packaging/security review. | Yes |
| local data/cache/storage posture unresolved | Local state may be sensitive. | Storage/security policy. | Yes |
| OS permissions/security posture unresolved | File-system, notifications, auto-start, sandbox risk. | OS/security review. | Yes |
| backend API contracts missing | Desktop cannot rely on backend contracts. | Backend/API contract review. | Yes |
| desktop generated-output policy missing | Logs/screens/reports may leak data. | Output/provenance review. | Yes |
| telemetry/crash-reporting posture unresolved | Local data may leave device later. | Telemetry/security decision. | Yes |
| product Git posture deferred to P-08 | Source tracking not approved. | P-08 Git posture decision. | Yes |
| dependency posture deferred to P-09 | Adoption not approved. | P-09 dependency posture. | Yes |
| validation baseline deferred to P-10 | Baseline absent. | P-10 baseline. | Yes |
| security/access review missing | Sensitive local/product data possible. | Security review. | Yes |
| no implementation readiness assessment | Readiness not evaluated. | Future IR review. | Yes |
| no product governance activation decision | Governance has not activated. | Activation decision. | Yes |

## 18. Implementation Readiness Blockers
No implementation readiness exists. Blockers include no owner, no accepted desktop UX/scope, no source tracking decision, no desktop framework/runtime selection, no package/installer/updater/signing posture, no backend API contract, no local storage/cache policy, no validation baseline, no security/access enforcement, no output handling policy, no tests/build/package/run posture, no installation/distribution posture, and no governance activation decision.

## 19. Evidence / Source References
Future charter claims must cite P-00 for selection, P-01 for common gate, P-02 for Omniverse interface separation, P-03 for backend/interface contract boundary, P-04 for CLI/shell/command boundary, M-07 for product charter-prep posture, M-06/W-13/V-05 for dependency/external posture, W-12 for product policy, V-04 for product validation posture, S-series for local-only/security, CSS-series for substrate/naming, H-series/M-04 for runtime/tool/provider/MCP boundary, and Siamese Product Vision for strategic product context.

Evidence supports review; evidence does not approve activation.

## 20. Gate Checklist
| Gate | P-05 status | Note |
| --- | --- | --- |
| GATE-01 selected candidate exists in P-00 | pass | P-00 selected `desktop`. |
| GATE-02 owner declared or owner gap recorded | pass_with_caution | Owner gap recorded. |
| GATE-03 purpose declared | pass | Local desktop/interface candidate for Siamese. |
| GATE-04 scope declared | pass_with_caution | Draft scope; needs validation. |
| GATE-05 non-goals declared | pass | Backend/runtime/packaging exclusions declared. |
| GATE-06 product/root boundary declared | pass | Product-scoped only. |
| GATE-07 local-only posture declared | pass | `2_products/` remains ignored/local-only. |
| GATE-08 security posture declared | pass_with_caution | Sensitive local data/output risk. |
| GATE-09 dependency posture declared | blocked | Desktop runtime/framework/package posture unresolved. |
| GATE-10 external-source posture declared | pass_with_caution | External/package evidence only. |
| GATE-11 Git posture declared or deferred to P-08 | pass_with_caution | Deferred to P-08. |
| GATE-12 validation baseline need declared | pass_with_caution | Deferred to P-10. |
| GATE-13 generated-output posture declared | pass_with_caution | Generated-sensitive by default. |
| GATE-14 provider/API/MCP posture declared | pass_with_caution | Future backend/API only after governance. |
| GATE-15 activation blockers declared | pass | Blockers listed. |
| GATE-16 implementation-readiness blockers declared | pass | Blockers listed. |
| GATE-17 governance decision path declared | pass_with_caution | Governance required; owner gap remains. |
| GATE-18 stop rules declared | pass | Stop before P-06 and all forbidden actions. |

Final gate status: `gate_passed_with_cautions_for_charter_review_only`. This gate status does not activate the product. Desktop runtime, packaging, local-data, and dependency risks remain activation-blocking.

## 21. Desktop-specific Gate Overlay
| overlay item | current posture | blocker | future route |
| --- | --- | --- | --- |
| desktop runtime/framework | Unapproved. | Stack and runtime risk. | P-09/runtime review. |
| packaging/installer | Unapproved. | Distribution risk. | Packaging governance. |
| auto-update mechanism | Unapproved. | Network/update/security risk. | Update/security review. |
| code signing/notarization | Unresolved. | Release trust risk. | Signing/notarization review. |
| OS permissions/file-system access | Unresolved. | Local data exposure risk. | OS security review. |
| local project workspace | Future only. | Scope/data policy absent. | UX/security review. |
| local cache/database | Design candidate only. | Source-of-truth and privacy risk. | Storage/cache policy. |
| settings/config handling | Future only. | Secret/config risk. | Security/config review. |
| secrets/tokens/redaction | Blocked. | Credential leakage risk. | Redaction/security review. |
| backend API/SDK invocation | Future only. | Contracts absent. | Governed backend API review. |
| offline/edge mode | Candidate only. | Sync/source-of-truth risk. | Offline governance review. |
| job/status/result UI | Future only. | Backend contract absent. | API/validation review. |
| generated exports/reports/screenshots | Generated-sensitive. | Publication/provenance risk. | Output policy review. |
| logging/crash reports/telemetry | Unresolved. | Local/private data risk. | Telemetry/security review. |
| notifications/tray/background service | Candidate only. | Auto-start/daemon risk. | OS/runtime review. |
| cross-platform compatibility | Unresolved. | OS/runtime dependency risk. | Compatibility review. |
| security sandboxing | Unresolved. | Desktop file/network risk. | Sandbox/security review. |
| installation/distribution | Not ready. | Package/release posture absent. | Distribution governance. |

## 22. Residual Risks
Residual risks: no active product owner, no product source review, no desktop framework/runtime choice, no packaging/installer/signing posture, no backend API contract, no local storage/cache policy, no output redaction/provenance policy, no telemetry/crash-reporting policy, no validation baseline, no Git posture decision, no implementation readiness, and no product activation decision.

## 23. P-05 Invariants
| ID | Invariant |
| --- | --- |
| P05-001 | Desktop charter is not product activation. |
| P05-002 | Desktop is local interface/runtime candidate, not backend. |
| P05-003 | Desktop does not own energy-domain logic. |
| P05-004 | Desktop consumes governed backend contracts only. |
| P05-005 | Desktop is not Omniverse Kit by default. |
| P05-006 | Desktop is not CLI or shell runner. |
| P05-007 | Product source remains local-only. |
| P05-008 | Product Git posture is not changed. |
| P05-009 | Product dependencies are not adopted. |
| P05-010 | Product validation baseline is not created. |
| P05-011 | Generated desktop output is not source by default. |
| P05-012 | Product needs do not decide root architecture. |
| P05-013 | Graph remains a candidate only. |
| P05-014 | Validation evaluates; governance decides. |
| P05-015 | P-05 stops before P-06. |

## 24. Anti-patterns
Anti-patterns: desktop as backend; desktop as free local runtime launcher; desktop as Omniverse replacement by implication; desktop as CLI/shell runner; product charter as activation; running desktop app inside charter work; installing desktop frameworks inside charter work; generated desktop output as source; local cache as source of truth; product source inspection by curiosity; backend API as permissionless surface; local daemon activation by desktop need; graph/product UI needs as substrate decision; starting P-06 inside P-05; `git add .`.

## 25. Readiness For P-06
P-06 - Web Platform Product Charter is ready after explicit instruction if P-05 Desktop Product Charter exists, `desktop` remains inactive, backend/interface boundaries are preserved, local runtime/packaging boundary is preserved, product/local-only/Git/dependency/security boundaries are preserved, and no product activation, source tracking, dependency adoption, provider/API/MCP activation, publication, or implementation is implied.

Do not create P-06.

## 26. Final Verdict
| Question | Answer |
| --- | --- |
| What does P-05 create? | One inactive Desktop Product Charter draft. |
| What is desktop in Siamese? | The future local packaged/interface candidate for governed Siamese project work and backend views. |
| Did P-05 activate desktop? | No. |
| Did P-05 inspect product source deeply? | No. |
| Did P-05 run desktop apps? | No. |
| Did P-05 install desktop frameworks, packages, or dependencies? | No. |
| Did P-05 change product Git posture? | No. |
| Did P-05 adopt dependencies? | No. |
| Did P-05 create validation baselines? | No. |
| Did P-05 define backend logic? | No. Backend-energyplus owns future energy-domain logic, validation, simulation orchestration, result normalization, calibration readiness, datasets, API/SDK contracts, and control integration. |
| What remains blocked? | Activation, source inspection, desktop app execution, local daemon execution, desktop runtime/framework/package dependency adoption, installer/updater/signing approval, product Git tracking, validation baselines, backend API contracts, local data/cache policy, generated-output publication, implementation readiness, provider/API/MCP/network/auth activation, staging, commit, push, and P-06. |
| Is P-06 ready after explicit instruction? | Yes, as Web Platform Product Charter drafting only; P-06 is not started. |

Stop after P-05 validation and report. Do not start P-06 or any later ticket.
