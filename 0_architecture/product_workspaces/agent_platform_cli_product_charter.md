# P-04 - CLI Product Charter
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | CLI Product Charter |
| Ticket | P-04 |
| Product candidate | `cli` |
| Status | Accepted inactive CLI product charter draft |
| Date | 2026-07-01 |
| Scope | Inactive charter draft for Siamese's future operator/scriptable interface candidate. |
| Authority | Product charter draft only, not product activation. |
| Related documents | P-00, P-01, P-02, P-03, M-A, M-07, M-06, W-12, V-04, W-13, V-05, S-series, CSS-series, H-series, Siamese Product Vision |

## 2. Purpose
P-00 selected `cli` for charter drafting. P-01 defined the common product charter template and common gate. P-02 preserved visual/backend separation. P-03 preserved backend/interface boundaries. P-04 drafts the inactive `cli` charter.

`cli` is Siamese's future operator/scriptable interface candidate. CLI is operator/scriptable interface, not backend. It must consume governed backend contracts only and must not become a free shell runner, shell permission surface, package wrapper, or direct EnergyPlus runner.

P-04 does not activate the product, inspect source deeply, run CLI or shell commands, install dependencies, change Git posture, create validation baselines, approve command execution, create shell/tool execution behavior, implement anything, or start P-05. It prepares P-05 - Desktop Product Charter for explicit future instruction only.

## 3. Product Candidate Summary
| Field | Value |
| --- | --- |
| product_id | PROD-002 / P00-SEL-003 |
| product_name | `cli` |
| product_platform_name | Siamese |
| product_status | candidate/deferred/local_only/inactive |
| selection_source | P-00 |
| charter_template_source | P-01 |
| boundary_source | P-03 Backend EnergyPlus Product Charter |
| likely area | CLI/operator interface |
| main risk | command/shell/package/user-data/output/security/Git/API/root-boundary |
| current verdict | draft_for_charter_review_with_blockers |
| blocked inference | Product activation, command approval, shell permission, dependency approval, source tracking, implementation readiness, CLI behavior approval. |

## 4. Product Vision Alignment
Siamese is a living energy twin platform for buildings. Siamese keeps the energy model alive by connecting an internal energy model to real data, calibration, prediction, recommendation/control, and continuous operation.

`cli` may later provide a scriptable/operator surface for safe backend actions. Future workflows may include project inspection, validation requests, simulation job submission, status queries, result summaries, diagnostics, export requests, and governed automation. CLI must remain decoupled from energy logic and must call governed backend contracts only.

Clarifications:
| Surface | Siamese role | P-04 boundary |
| --- | --- | --- |
| CLI | Textual/operator interface. | Product interface only; no backend ownership. |
| Backend Python | Energy-domain logic, validation, simulation orchestration, result normalization, calibration readiness, datasets, API/SDK, and future control integration. | Backend owns energy logic. |
| EnergyPlus | Physical solver. | Not directly owned or run by CLI without governed backend contract. |
| Omniverse App | Visual/operational interface. | Not CLI runtime. |
| Shell | External execution surface. | Availability is not permission. |
| Commands | Future product UX contracts. | Documentation candidates, not implementation or permission. |

## 5. Owner / Governance
Owner is not finalized because no accepted source declares a final owner. P-04 records an owner gap.

Governance must decide activation, Git posture, dependency adoption, publication, command scope, execution permission, and implementation readiness. P-04 cannot assign final owner authority or approve CLI product work.

## 6. Product Scope
Future `cli` charter scope may include: CLI product purpose and command-surface boundaries; future command taxonomy as documentation only; future operator workflows for Siamese; future backend job, status, and result interaction through governed API/SDK contracts; future diagnostics and validation request surfaces; future local project metadata inspection after explicit governance; future safe output formatting and report request surface; future automation hooks only as governed design candidates; future integration with `backend-energyplus` contracts; and future integration with product validation/security posture.

Out of scope: shell execution implementation; arbitrary command runner; package manager wrapper; backend energy logic; direct EnergyPlus runner; Omniverse UI behavior; desktop/web behavior; agent runtime; MCP server/client activation; provider/API/network/auth activation; dependency adoption; validation baseline execution; and implementation readiness.

## 7. Non-Goals
Non-goals: do not make `cli` a free shell interface; do not treat CLI command presence as execution approval; do not bypass backend contracts; do not make CLI own backend energy logic; do not run EnergyPlus directly from charter scope; do not install or adopt packages; do not use CLI to inspect local-only product source; do not treat CLI output as source by default; do not make CLI command needs define root architecture; do not activate runtime, package managers, APIs, MCP, hooks, or tools.

## 8. Product / Root Boundary
`cli` is product-scoped. It does not define AGENT PLATFORM root authority, the Cognitive Semantic System, backend truth, validation truth, governance truth, Git truth, execution truth, dependency truth, command permission, or shell permission.

Product decisions can inform future root proposals but cannot silently constrain root architecture. Command/runtime decisions remain product-scoped unless governed otherwise. Graph remains a candidate only.

## 9. User / Domain / Interface Hypothesis
| Hypothesis | Expected use | Validation posture |
| --- | --- | --- |
| Energy engineer | Request validation, simulation jobs, diagnostics, and summaries. | Hypothesis only. |
| Developer/operator | Inspect safe project metadata and orchestrate governed workflows. | Hypothesis only. |
| Researcher/university | Script reproducible requests for batch workflows after governance. | Hypothesis only. |
| CI/future automation | May call safe CLI contracts after validation, security, and Git posture exists. | Hypothesis only. |
| Other product interfaces | May share backend contracts but not CLI internals. | Hypothesis only. |

These are hypotheses, not validated behavior, execution, safety, or market claims.

## 10. Current Local-only Posture
`cli` source, if present under `2_products/`, remains local-only and ignored. P-04 does not inspect product source. P-04 uses safe metadata only.

Local sessions, command history, configs, generated outputs, logs, credentials, dependency folders, build outputs, reports, and product artifacts remain excluded unless governed later.

## 11. Security / Access Posture
CLI arguments, command histories, project paths, building IDs, output paths, backend URLs, tokens, logs, local configs, validation reports, simulation summaries, and generated exports may be sensitive.

Secrets, credentials, tokens, provider auth, package registry auth, local sessions, telemetry configs, API keys, and environment variables are excluded. No shell/provider/API/MCP/network/auth activation occurs. Unknown sensitivity blocks publication and context exposure. Command logs and generated CLI outputs are local-only by default.

## 12. Dependency / External Source Posture
CLI package/runtime dependency posture is unresolved. Python/Node/Rust/Go/native packaging posture is unresolved unless future governance selects a stack. Shell/platform compatibility posture is unresolved. External command, parser, package, runtime, and formatting libraries are not adopted.

Dependency references are not dependency approval. External source presence is not adoption. Product-specific dependency adoption would not become root dependency adoption. P-09 will handle Product Dependency / External Source Posture.

## 13. Provider / API / MCP Posture
`cli` may later call backend APIs or SDK functions only after governed contracts exist. `cli` may later expose command surfaces only after security and validation review. No provider/API/MCP is activated by P-04.

MCP availability is not MCP activation. Tool availability is not permission. Shell availability is not command approval. Provider credentials are not provider permission. Backend service modes are future scope.

## 14. Generated Output / Data / Model / Artifact Posture
Command outputs, logs, diagnostics, validation summaries, simulation job summaries, result exports, reports, JSON/CSV outputs, stdout/stderr captures, config snapshots, and generated documentation are generated-sensitive by default.

Generated output is evidence, not source by default. Raw output remains local-only until reviewed. Publication requires product, security, validation, dependency, and governance review.

## 15. Git Posture
Product Git posture is not changed by P-04. `2_products/` remains ignored/local-only. `cli` source tracking is deferred to P-08.

P-04 does not stage, commit, push, force-add, or publish. Future Git action must use exact paths only. No `git add .`.

## 16. Validation Baseline Needs
Future baseline needs under V-04/P-01: product charter completeness checks; command taxonomy checks; command safety checks; local-only checks; dependency/package/license checks; generated-output checks; security/access checks; shell boundary checks; backend/API contract checks; argument/input validation checks; output provenance checks; sensitive path/secret redaction checks; CLI help/docs checks; and tests/builds/execution only after explicit future approval.

P-04 does not create or execute validation baselines. P-10 handles Product Validation Baseline.

## 17. Activation Blockers
| blocker | reason | required future action | blocks activation? |
| --- | --- | --- | --- |
| owner missing or not final | No accepted final owner. | Assign governed owner. | Yes |
| scope not validated | Scope is draft only. | Product scope review. | Yes |
| root/product boundary requires review | CLI can blur root execution authority. | Product/root boundary review. | Yes |
| command scope unresolved | Command taxonomy and permissions are absent. | Command scope governance. | Yes |
| shell boundary unresolved | Shell availability must not become permission. | Shell/security boundary review. | Yes |
| CLI package/runtime posture unresolved | Runtime stack and package posture are undecided. | P-09/dependency/runtime review. | Yes |
| backend API contracts missing | CLI cannot rely on backend contracts. | Backend/API contract review. | Yes |
| product Git posture deferred to P-08 | Source tracking not approved. | P-08 Git posture decision. | Yes |
| dependency posture deferred to P-09 | Adoption not approved. | P-09 dependency posture. | Yes |
| validation baseline deferred to P-10 | Baseline absent. | P-10 baseline. | Yes |
| security/access review missing | CLI inputs/outputs may expose sensitive data. | Security review. | Yes |
| generated-output review missing | Logs and command output may leak data. | Output/provenance review. | Yes |
| argument/input validation absent | Unsafe inputs or paths could be accepted later. | Input validation design. | Yes |
| output redaction/provenance absent | CLI output could expose secrets or be overclaimed. | Redaction/provenance policy. | Yes |
| no implementation readiness assessment | Readiness not evaluated. | Future IR review. | Yes |
| no product governance activation decision | Governance has not activated. | Activation decision. | Yes |

## 18. Implementation Readiness Blockers
No implementation readiness exists. Blockers include no owner, no accepted CLI command taxonomy, no source tracking decision, no package/runtime readiness, no shell boundary policy, no backend API contract, no validation baseline, no security/access enforcement, no output handling policy, no tests/build/run posture, no installation/distribution posture, and no governance activation decision.

## 19. Evidence / Source References
Future charter claims must cite P-00 for selection, P-01 for common gate, P-03 for backend/interface contract boundary, P-02 for product/interface separation where relevant, M-07 for product charter-prep posture, M-06/W-13/V-05 for dependency/external posture, W-12 for product policy, V-04 for product validation posture, S-series for local-only/security, CSS-series for substrate/naming, H-series/M-04 for runtime/tool/provider/MCP boundary, and Siamese Product Vision for strategic product context.

Evidence supports review; evidence does not approve activation.

## 20. Gate Checklist
| Gate | P-04 status | Note |
| --- | --- | --- |
| GATE-01 selected candidate exists in P-00 | pass | P-00 selected `cli`. |
| GATE-02 owner declared or owner gap recorded | pass_with_caution | Owner gap recorded. |
| GATE-03 purpose declared | pass | Operator/scriptable interface candidate for Siamese. |
| GATE-04 scope declared | pass_with_caution | Draft scope; needs validation. |
| GATE-05 non-goals declared | pass | Shell/backend/runtime exclusions declared. |
| GATE-06 product/root boundary declared | pass | Product-scoped only. |
| GATE-07 local-only posture declared | pass | `2_products/` remains ignored/local-only. |
| GATE-08 security posture declared | pass_with_caution | Sensitive command/input/output risk. |
| GATE-09 dependency posture declared | blocked | CLI package/runtime/dependency posture unresolved. |
| GATE-10 external-source posture declared | pass_with_caution | Evidence only. |
| GATE-11 Git posture declared or deferred to P-08 | pass_with_caution | Deferred to P-08. |
| GATE-12 validation baseline need declared | pass_with_caution | Deferred to P-10. |
| GATE-13 generated-output posture declared | pass_with_caution | Generated-sensitive by default. |
| GATE-14 provider/API/MCP posture declared | pass_with_caution | Future backend/API only after governance. |
| GATE-15 activation blockers declared | pass | Blockers listed. |
| GATE-16 implementation-readiness blockers declared | pass | Blockers listed. |
| GATE-17 governance decision path declared | pass_with_caution | Governance required; owner gap remains. |
| GATE-18 stop rules declared | pass | Stop before P-05 and all forbidden actions. |

Final gate status: `gate_passed_with_cautions_for_charter_review_only`. This gate status does not activate the product. Command execution and dependency risks remain activation-blocking.

## 21. CLI-specific Gate Overlay
| overlay item | current posture | blocker | future route |
| --- | --- | --- | --- |
| command taxonomy | Documentation candidate only. | Commands undefined. | Command-scope review. |
| command parser/runtime | Unapproved. | Package/runtime risk. | Dependency/runtime review. |
| shell boundary | Blocked by default. | Shell permission risk. | S-series command review. |
| package/runtime dependency | Unapproved. | Stack and package posture absent. | P-09 dependency review. |
| backend API/SDK invocation | Future only. | Contracts absent. | Governed backend API review. |
| validation command surface | Future only. | Validation baseline absent. | P-10 validation baseline. |
| simulation job command surface | Future only. | Backend contract and safety absent. | Backend/API/security review. |
| results/diagnostics output | Generated-sensitive. | Redaction/provenance absent. | Output policy review. |
| config/env handling | Blocked. | Secret/env risk. | Security/config review. |
| secrets/tokens/redaction | Blocked. | Credential leakage risk. | Redaction/security review. |
| user/project path handling | Unapproved. | Local path and data exposure risk. | Input validation review. |
| stdout/stderr/logging | Generated-sensitive. | Log sensitivity risk. | Logging/output review. |
| generated report/export handling | Local-only by default. | Publication/provenance risk. | Product/security review. |
| CI/future automation usage | Future only. | Git/execution posture absent. | Validation/security/Git review. |
| MCP/tool integration | Blocked. | MCP/tool permission risk. | Governed MCP/tool review. |
| installation/distribution | Not ready. | Package/release posture absent. | Packaging/dependency review. |

## 22. Residual Risks
Residual risks: no active product owner, no product source review, no CLI command taxonomy, no shell boundary policy, no package/runtime dependency review, no backend API contract, no output redaction/provenance policy, no validation baseline, no Git posture decision, no implementation readiness, and no product activation decision.

## 23. P-04 Invariants
| ID | Invariant |
| --- | --- |
| P04-001 | CLI charter is not product activation. |
| P04-002 | CLI is operator/scriptable interface, not backend. |
| P04-003 | CLI does not own energy-domain logic. |
| P04-004 | CLI consumes governed backend contracts only. |
| P04-005 | Shell availability is not command approval. |
| P04-006 | Tool availability is not permission. |
| P04-007 | MCP availability is not MCP activation. |
| P04-008 | Product source remains local-only. |
| P04-009 | Product Git posture is not changed. |
| P04-010 | Product dependencies are not adopted. |
| P04-011 | Product validation baseline is not created. |
| P04-012 | Generated CLI output is not source by default. |
| P04-013 | Product needs do not decide root architecture. |
| P04-014 | Graph remains a candidate only. |
| P04-015 | P-04 stops before P-05. |

## 24. Anti-patterns
Anti-patterns: CLI as free shell runner; CLI command as execution approval; shell availability as permission; CLI bypassing backend contracts; CLI owning backend energy logic; product charter as activation; running CLI inside charter work; installing packages inside charter work; generated CLI output as source; product source inspection by curiosity; backend API as permissionless surface; MCP/tool activation by CLI need; graph/product automation needs as substrate decision; starting P-05 inside P-04; `git add .`.

## 25. Readiness For P-05
P-05 - Desktop Product Charter is ready after explicit instruction if P-04 CLI Product Charter exists, `cli` remains inactive, backend/interface boundaries are preserved, shell/command boundary is preserved, product/local-only/Git/dependency/security boundaries are preserved, and no product activation, source tracking, dependency adoption, provider/API/MCP activation, publication, or implementation is implied.

Do not create P-05.

## 26. Final Verdict
| Question | Answer |
| --- | --- |
| What does P-04 create? | One inactive CLI Product Charter draft. |
| What is cli in Siamese? | The future textual/operator/scriptable interface candidate for safe governed backend workflows. |
| Did P-04 activate cli? | No. |
| Did P-04 inspect product source deeply? | No. |
| Did P-04 run CLI commands or shell commands? | No. |
| Did P-04 install packages or dependencies? | No. |
| Did P-04 change product Git posture? | No. |
| Did P-04 adopt dependencies? | No. |
| Did P-04 create validation baselines? | No. |
| Did P-04 define backend logic? | No. Backend-energyplus owns future energy-domain logic, validation, simulation orchestration, result normalization, calibration readiness, datasets, API/SDK contracts, and control integration. |
| What remains blocked? | Activation, source inspection, CLI/shell command execution, command approval, package/runtime dependency adoption, product Git tracking, validation baselines, backend API contracts, generated-output publication, implementation readiness, provider/API/MCP/network/auth activation, staging, commit, push, and P-05. |
| Is P-05 ready after explicit instruction? | Yes, as Desktop Product Charter drafting only; P-05 is not started. |

Stop after P-04 validation and report. Do not start P-05 or any later ticket.
