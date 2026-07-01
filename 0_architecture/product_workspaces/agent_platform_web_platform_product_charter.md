# P-06 - Web Platform Product Charter
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Web Platform Product Charter |
| Ticket | P-06 |
| Product candidate | `web-platform` |
| Status | Accepted inactive Web Platform product charter draft |
| Date | 2026-07-01 |
| Scope | Inactive charter draft for Siamese's future browser/deployed interface candidate. |
| Authority | Product charter draft only, not product activation. |
| Related documents | P-00, P-01, P-02, P-03, P-04, P-05, M-A, M-07, M-06, W-12, V-04, W-13, V-05, S-series, CSS-series, H-series, Siamese Product Vision |

## 2. Purpose
P-00 selected `web-platform` for charter drafting. P-01 defined the common product charter template and common gate. P-02 preserved Omniverse/interface boundaries. P-03 preserved backend/interface boundaries. P-04 preserved CLI/shell/command boundaries. P-05 preserved desktop/runtime/packaging boundaries. P-06 drafts the inactive `web-platform` charter.

`web-platform` is Siamese's future browser/deployed interface candidate. Web Platform is browser/deployed interface candidate, not backend. It must consume governed backend contracts only and must not become Omniverse Kit, CLI, desktop, a deployment approval, or an auth/provider/API permission surface.

P-06 does not activate the product, inspect source deeply, run web apps, start dev servers, run builds, run package managers, deploy anything, change Git posture, create validation baselines, create web runtime behavior, create implementation artifacts, or start P-07. It prepares P-07 - Experimental Workspace Disposition for explicit future instruction only.

## 3. Product Candidate Summary
| Field | Value |
| --- | --- |
| product_id | PROD-006 / P00-SEL-005 |
| product_name | `web-platform` |
| product_platform_name | Siamese |
| product_status | candidate/deferred/local_only/inactive |
| selection_source | P-00 |
| charter_template_source | P-01 |
| boundary_sources | P-02 Omniverse App, P-03 Backend EnergyPlus, P-04 CLI, P-05 Desktop |
| likely area | web/browser/deployed interface |
| main risk | auth/data/build/deploy/package/security/generated-output/Git/API/root-boundary |
| current verdict | draft_for_charter_review_with_blockers |
| blocked inference | Product activation, web runtime approval, deploy approval, auth approval, dependency approval, source tracking, implementation readiness, web behavior approval. |

## 4. Product Vision Alignment
Siamese is a living energy twin platform for buildings. Siamese keeps the energy model alive by connecting an internal energy model to real data, calibration, prediction, recommendation/control, and continuous operation.

`web-platform` may later provide browser-based access to Siamese project information, dashboards, reports, diagnostics, status, and governed backend outputs. It may later support stakeholder-facing workflows where Omniverse, desktop, or CLI are not appropriate. Web Platform must remain decoupled from energy logic and must call governed backend contracts only.

Clarifications:
| Surface | Siamese role | P-06 boundary |
| --- | --- | --- |
| Web Platform | Browser/deployed interface candidate. | Product interface only; no backend ownership. |
| Backend Python | Energy-domain logic, validation, simulation orchestration, result normalization, calibration readiness, datasets, API/SDK, and future control integration. | Backend owns energy logic. |
| Omniverse App | Advanced visual/3D Omniverse interface. | Not web runtime. |
| Desktop | Local packaged/interface candidate. | Not web deployment. |
| CLI | Textual/operator interface. | Not web automation. |
| Web auth/session/user/tenant data | Future web identity and access data. | Sensitive by default. |
| Web deployment/hosting/CDN/domain/TLS | Future release surfaces. | Not accepted by charter. |

## 5. Owner / Governance
Owner is not finalized because no accepted source declares a final owner. P-06 records an owner gap.

Governance must decide activation, Git posture, dependency adoption, publication, web runtime stack, deployment, auth, hosting, data handling, execution permission, and implementation readiness. P-06 cannot assign final owner authority or approve web-platform product work.

## 6. Product Scope
Future `web-platform` charter scope may include: web product purpose and browser/deployed interface boundaries; future stakeholder-facing dashboards; future project, status, result, and diagnostic views through governed backend API contracts; future report viewing and controlled export request surfaces; future user/session/auth posture as design candidate only; future tenant/account/workspace posture as design candidate only; future web data/cache/storage posture as design candidate only; future browser-side visualization posture as design candidate only; future admin/settings UI after security governance; future integration with `backend-energyplus` contracts; and future alignment with `omniverse-app`, `cli`, and `desktop` boundaries.

Out of scope: backend energy logic; EnergyPlus direct runner; Omniverse Kit runtime; desktop/local runtime behavior; arbitrary CLI/shell execution; web app implementation; local dev server execution; hosting/deploy implementation; auth/session/user management implementation; database/cache implementation; CDN/domain/TLS/email implementation; API gateway implementation; native packaging/distribution approval; dependency adoption; validation baseline execution; implementation readiness; and provider/API/network/MCP/auth activation.

## 7. Non-Goals
Non-goals: do not make web-platform the backend; do not make web-platform own energy-domain logic; do not make web-platform bypass backend contracts; do not make web-platform a deployment or hosting approval; do not make web-platform an auth/user/tenant system by implication; do not make web-platform a public publication surface by default; do not adopt React/Next/Vite/Node/cloud/hosting stack by relevance; do not approve domains, TLS, CDN, email, cookies, sessions, tracking, telemetry, or analytics; do not treat web cache/output as source by default; do not activate runtime, package managers, APIs, MCP, hooks, tools, providers, or deployment.

## 8. Product / Root Boundary
`web-platform` is product-scoped. It does not define AGENT PLATFORM root authority, the Cognitive Semantic System, backend truth, validation truth, governance truth, Git truth, execution truth, dependency truth, auth truth, deployment truth, publication truth, or data-retention truth.

Product decisions can inform future root proposals but cannot silently constrain root architecture. Web runtime, deploy, and auth decisions remain product-scoped unless governed otherwise. Graph remains a candidate only.

## 9. User / Domain / Interface Hypothesis
| Hypothesis | Expected use | Validation posture |
| --- | --- | --- |
| Energy engineer | Browser access to summaries, diagnostics, project state, and reports. | Hypothesis only. |
| Facility/operator | Dashboard-style status, alerts, predictions, and recommendations if governed later. | Hypothesis only. |
| Building owner/stakeholder | Reviewed energy evidence, savings, comfort, and sustainability views. | Hypothesis only. |
| Researcher/university | Web-accessible living-lab dashboards after governance. | Hypothesis only. |
| Admin/operator | Future user, workspace, and admin interface after security/deployment governance. | Hypothesis only. |

These are hypotheses, not validated behavior, execution, security, usability, deployment, or market claims.

## 10. Current Local-only Posture
`web-platform` source, if present under `2_products/`, remains local-only and ignored. P-06 does not inspect product source. P-06 uses safe metadata only.

Local sessions, configs, generated outputs, logs, credentials, dependency folders, build outputs, deployment bundles, caches, local DBs, screenshots, reports, and product artifacts remain excluded unless governed later.

## 11. Security / Access Posture
Web project paths, backend URLs, building data, sensor data, reports, screenshots, logs, browser caches, cookies, sessions, user/account/tenant data, auth configs, generated exports, API responses, dashboard views, and deployment configs may be sensitive.

Secrets, credentials, tokens, provider auth, package registry auth, local sessions, telemetry configs, API keys, Nucleus/cloud auth, OAuth secrets, cookie secrets, TLS material, and environment variables are excluded. No web runtime/provider/API/MCP/network/auth activation occurs. Unknown sensitivity blocks publication and context exposure. Web logs, browser cache, generated reports, dashboard screenshots, and exports are local-only by default.

## 12. Dependency / External Source Posture
Web framework/runtime dependency posture is unresolved. React/Vue/Svelte/Next/Vite/Node/Python/native packaging posture is unresolved unless future governance selects a stack. Hosting, CDN, domain, TLS, email, auth, analytics, monitoring, and deployment posture are unresolved. Browser compatibility and accessibility posture are unresolved. External web, UI, auth, API, charting, storage, and hosting libraries are not adopted.

Dependency references are not dependency approval. External source presence is not adoption. Product-specific dependency adoption would not become root dependency adoption. P-09 will handle Product Dependency / External Source Posture.

## 13. Provider / API / MCP Posture
`web-platform` may later call backend APIs or SDK functions only after governed contracts exist. `web-platform` may later use REST, websocket, GraphQL, local API, remote API, auth provider, storage provider, or analytics provider only after security and validation review. No provider/API/MCP/network/auth is activated by P-06.

MCP availability is not MCP activation. Tool availability is not permission. Provider credentials are not provider permission. Backend service modes are future scope.

## 14. Generated Output / Data / Model / Artifact Posture
Web screenshots, browser caches, logs, diagnostics, validation summaries, simulation job summaries, report exports, downloaded files, JSON/CSV outputs, dashboard exports, static build artifacts, deployment bundles, settings snapshots, and generated documentation are generated-sensitive by default.

Generated output is evidence, not source by default. Raw output remains local-only until reviewed. Publication requires product, security, validation, dependency, privacy, and governance review.

## 15. Git Posture
Product Git posture is not changed by P-06. `2_products/` remains ignored/local-only. `web-platform` source tracking is deferred to P-08.

P-06 does not stage, commit, push, force-add, or publish. Future Git action must use exact paths only. No `git add .`.

## 16. Validation Baseline Needs
Future baseline needs under V-04/P-01: product charter completeness checks; web UX/scope checks; local-only checks; dependency/package/license checks; generated-output checks; security/access checks; auth/session/cookie checks; privacy/data-retention checks; deployment/hosting checks; accessibility/browser compatibility checks; backend/API contract checks; sensitive path/secret redaction checks; logging/telemetry checks; and launch/build/package/deploy tests only after explicit future approval.

P-06 does not create or execute validation baselines. P-10 handles Product Validation Baseline.

## 17. Activation Blockers
| blocker | reason | required future action | blocks activation? |
| --- | --- | --- | --- |
| owner missing or not final | No accepted final owner. | Assign governed owner. | Yes |
| scope not validated | Scope is draft only. | Product scope review. | Yes |
| root/product boundary requires review | Web interface can blur deployed authority. | Product/root boundary review. | Yes |
| web runtime/framework unresolved | Runtime stack is undecided. | P-09/dependency/runtime review. | Yes |
| package/build tooling unresolved | Build and package posture absent. | Build/dependency review. | Yes |
| hosting/deploy/domain/TLS unresolved | Deployment and public surface risk. | Deploy/security review. | Yes |
| auth/session/user/tenant posture unresolved | Identity and account data risk. | Auth/security/privacy review. | Yes |
| data/privacy/retention posture unresolved | Web data may be sensitive. | Data/privacy policy. | Yes |
| browser/cache/storage posture unresolved | Browser state may leak data. | Storage/cache policy. | Yes |
| backend API contracts missing | Web cannot rely on backend contracts. | Backend/API contract review. | Yes |
| web generated-output policy missing | Logs/screens/exports may leak data. | Output/provenance review. | Yes |
| telemetry/analytics posture unresolved | User/product data may leave environment. | Telemetry/security decision. | Yes |
| product Git posture deferred to P-08 | Source tracking not approved. | P-08 Git posture decision. | Yes |
| dependency posture deferred to P-09 | Adoption not approved. | P-09 dependency posture. | Yes |
| validation baseline deferred to P-10 | Baseline absent. | P-10 baseline. | Yes |
| security/access review missing | Sensitive web/product data possible. | Security review. | Yes |
| no implementation readiness assessment | Readiness not evaluated. | Future IR review. | Yes |
| no product governance activation decision | Governance has not activated. | Activation decision. | Yes |

## 18. Implementation Readiness Blockers
No implementation readiness exists. Blockers include no owner, no accepted web UX/scope, no source tracking decision, no web framework/runtime selection, no package/build/deploy posture, no backend API contract, no auth/session/user/tenant policy, no privacy/data-retention policy, no validation baseline, no security/access enforcement, no output handling policy, no tests/build/deploy posture, no hosting/distribution posture, and no governance activation decision.

## 19. Evidence / Source References
Future charter claims must cite P-00 for selection, P-01 for common gate, P-02 for Omniverse interface separation, P-03 for backend/interface contract boundary, P-04 for CLI/shell/command boundary, P-05 for desktop/runtime/packaging boundary, M-07 for product charter-prep posture, M-06/W-13/V-05 for dependency/external posture, W-12 for product policy, V-04 for product validation posture, S-series for local-only/security, CSS-series for substrate/naming, H-series/M-04 for runtime/tool/provider/MCP boundary, and Siamese Product Vision for strategic product context.

Evidence supports review; evidence does not approve activation.

## 20. Gate Checklist
| Gate | P-06 status | Note |
| --- | --- | --- |
| GATE-01 selected candidate exists in P-00 | pass | P-00 selected `web-platform`. |
| GATE-02 owner declared or owner gap recorded | pass_with_caution | Owner gap recorded. |
| GATE-03 purpose declared | pass | Browser/deployed interface candidate for Siamese. |
| GATE-04 scope declared | pass_with_caution | Draft scope; needs validation. |
| GATE-05 non-goals declared | pass | Backend/deploy/auth/runtime exclusions declared. |
| GATE-06 product/root boundary declared | pass | Product-scoped only. |
| GATE-07 local-only posture declared | pass | `2_products/` remains ignored/local-only. |
| GATE-08 security posture declared | pass_with_caution | Sensitive web/auth/user/output risk. |
| GATE-09 dependency posture declared | blocked | Web runtime/framework/package/deploy posture unresolved. |
| GATE-10 external-source posture declared | pass_with_caution | External/package evidence only. |
| GATE-11 Git posture declared or deferred to P-08 | pass_with_caution | Deferred to P-08. |
| GATE-12 validation baseline need declared | pass_with_caution | Deferred to P-10. |
| GATE-13 generated-output posture declared | pass_with_caution | Generated-sensitive by default. |
| GATE-14 provider/API/MCP posture declared | pass_with_caution | Future backend/API only after governance. |
| GATE-15 activation blockers declared | pass | Blockers listed. |
| GATE-16 implementation-readiness blockers declared | pass | Blockers listed. |
| GATE-17 governance decision path declared | pass_with_caution | Governance required; owner gap remains. |
| GATE-18 stop rules declared | pass | Stop before P-07 and all forbidden actions. |

Final gate status: `gate_passed_with_cautions_for_charter_review_only`. This gate status does not activate the product. Web runtime, auth, deploy, data, and dependency risks remain activation-blocking.

## 21. Web-specific Gate Overlay
| overlay item | current posture | blocker | future route |
| --- | --- | --- | --- |
| web runtime/framework | Unapproved. | Stack and runtime risk. | P-09/runtime review. |
| package/build tooling | Unapproved. | Package/script/build risk. | Build/dependency review. |
| local dev server | Blocked. | Server/process risk. | Execution/security review. |
| hosting/deployment | Unapproved. | Public deployment risk. | Deploy governance. |
| CDN/domain/TLS | Unresolved. | Trust, privacy, routing risk. | Hosting/security review. |
| auth/session/cookies | Design candidate only. | Credential/session risk. | Auth/security review. |
| user/account/tenant model | Design candidate only. | Privacy/isolation risk. | Product/security review. |
| privacy/data retention | Unresolved. | Legal and user-data risk. | Privacy governance. |
| browser cache/storage | Unresolved. | Source-of-truth and leakage risk. | Storage/cache policy. |
| backend API/SDK invocation | Future only. | Contracts absent. | Governed backend API review. |
| websocket/realtime updates | Future only. | Network/auth/state risk. | API/security review. |
| dashboard/report views | Future only. | Data/provenance risk. | UX/validation review. |
| generated exports/screenshots | Generated-sensitive. | Publication/provenance risk. | Output policy review. |
| logging/telemetry/analytics | Unresolved. | Local/private data risk. | Telemetry/security review. |
| accessibility/browser compatibility | Unresolved. | UX/compliance risk. | Compatibility baseline. |
| admin/settings surface | Future only. | Privilege/config risk. | Security/admin review. |
| security headers/CORS/CSRF | Unresolved. | Web security risk. | Security architecture review. |
| installation/distribution | Not ready. | Release posture absent. | Distribution governance. |

## 22. Residual Risks
Residual risks: no active product owner, no product source review, no web framework/runtime choice, no package/build/deploy posture, no backend API contract, no auth/session/user/tenant policy, no data/privacy/retention policy, no output redaction/provenance policy, no telemetry/analytics policy, no validation baseline, no Git posture decision, no implementation readiness, and no product activation decision.

## 23. P-06 Invariants
| ID | Invariant |
| --- | --- |
| P06-001 | Web Platform charter is not product activation. |
| P06-002 | Web Platform is browser/deployed interface candidate, not backend. |
| P06-003 | Web Platform does not own energy-domain logic. |
| P06-004 | Web Platform consumes governed backend contracts only. |
| P06-005 | Web Platform is not Omniverse Kit, Desktop, or CLI. |
| P06-006 | Web deployment is not approved. |
| P06-007 | Auth/session/provider availability is not activation. |
| P06-008 | Product source remains local-only. |
| P06-009 | Product Git posture is not changed. |
| P06-010 | Product dependencies are not adopted. |
| P06-011 | Product validation baseline is not created. |
| P06-012 | Generated web output is not source by default. |
| P06-013 | Product needs do not decide root architecture. |
| P06-014 | Graph remains a candidate only. |
| P06-015 | P-06 stops before P-07. |

## 24. Anti-patterns
Anti-patterns: web-platform as backend; web-platform as deployment approval; web-platform as auth/user system by implication; web-platform as public publication surface by default; product charter as activation; running web app inside charter work; installing web frameworks inside charter work; generated web output as source; browser cache as source of truth; product source inspection by curiosity; backend API as permissionless surface; provider/auth activation by web need; graph/product dashboard needs as substrate decision; starting P-07 inside P-06; `git add .`.

## 25. Readiness For P-07
P-07 - Experimental Workspace Disposition is ready after explicit instruction if P-06 Web Platform Product Charter exists, `web-platform` remains inactive, backend/interface boundaries are preserved, web runtime/auth/deploy boundary is preserved, product/local-only/Git/dependency/security boundaries are preserved, and no product activation, source tracking, dependency adoption, provider/API/MCP activation, publication, deploy, or implementation is implied.

Do not create P-07.

## 26. Final Verdict
| Question | Answer |
| --- | --- |
| What does P-06 create? | One inactive Web Platform Product Charter draft. |
| What is web-platform in Siamese? | The future browser/deployed interface candidate for governed Siamese project information, dashboards, reports, diagnostics, status, and backend outputs. |
| Did P-06 activate web-platform? | No. |
| Did P-06 inspect product source deeply? | No. |
| Did P-06 run web apps, dev servers, builds, or deploys? | No. |
| Did P-06 install web frameworks, packages, or dependencies? | No. |
| Did P-06 change product Git posture? | No. |
| Did P-06 adopt dependencies? | No. |
| Did P-06 create validation baselines? | No. |
| Did P-06 define backend logic? | No. Backend-energyplus owns future energy-domain logic, validation, simulation orchestration, result normalization, calibration readiness, datasets, API/SDK contracts, and control integration. |
| What remains blocked? | Activation, source inspection, web app/dev-server/build/deploy execution, web runtime/framework/package dependency adoption, auth/session/user/tenant behavior, hosting/domain/TLS approval, product Git tracking, validation baselines, backend API contracts, web data/cache policy, generated-output publication, implementation readiness, provider/API/MCP/network/auth activation, staging, commit, push, and P-07. |
| Is P-07 ready after explicit instruction? | Yes, as Experimental Workspace Disposition only; P-07 is not started. |

Stop after P-06 validation and report. Do not start P-07 or any later ticket.
