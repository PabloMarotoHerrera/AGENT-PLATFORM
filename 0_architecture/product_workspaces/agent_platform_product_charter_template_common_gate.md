# P-01 - Product Charter Template / Common Product Gate
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Product Charter Template / Common Product Gate |
| Ticket | P-01 |
| Status | Accepted product charter template and common gate |
| Date | 2026-07-01 |
| Scope | Canonical template and mandatory common gate for future AGENT PLATFORM product charters. |
| Authority | Template/gate planning only, not product activation. |
| Related documents | P-00, M-A, M-07, M-06, W-12, V-04, W-13, V-05, S-series, CSS-series, H-series |

## 2. Purpose
P-00 selected future product charter routes: `omniverse-app`, `backend-energyplus`, `cli`, `desktop`, and `web-platform` for future charter drafting, and `experimental` for disposition review.

P-01 defines the common product charter template and common product gate every future product charter must satisfy before activation, Git tracking, dependency adoption, validation baseline execution, implementation readiness, or publication can be considered.

P-01 does not create individual charters, activate products, create validation baselines, change Git posture, adopt dependencies, inspect product source, or start P-02. It prepares P-02 - Omniverse App Product Charter for explicit future instruction only.

## 3. Product Charter Template Definition
A product charter template is a governed documentation structure for describing a product candidate's purpose, scope, owner, non-goals, root/product boundary, security posture, dependency posture, Git posture, validation baseline needs, activation blockers, and future readiness gates.

Product charter template is not product activation. The template is not an accepted charter, implementation readiness, dependency approval, product Git tracking, or publication approval.

## 4. Common Product Gate Definition
The common product gate is a mandatory review gate that every future product charter must pass before product activation, source tracking, dependency adoption, validation baseline execution, implementation readiness, or publication can be considered.

The gate defines conditions only. It does not approve activation, execute validation, authorize code inspection, authorize dependency adoption, or authorize Git tracking. Common gate is not charter acceptance.

## 5. Authority Boundary
| Layer | P-01 rule |
| --- | --- |
| Governance | Decides product activation, charter acceptance, owners, Git posture, dependency adoption, publication, and exceptions. |
| Validation | Evaluates readiness, evidence, proof posture, blockers, and residual risk. |
| Security | Constrains local-only handling, secrets, credentials, execution, provider/API/MCP/network/auth, Git, and publication. |
| Product charters | Remain product-scoped and cannot define root authority by implication. |
| Agents | May prepare safe metadata but cannot activate, inspect deeply, execute, adopt dependencies, stage, commit, push, or publish. |

## 6. Source Boundary
| Source | P-01 use |
| --- | --- |
| P-00 | Product selection source. |
| M-07 | Product charter-preparation source. |
| W-12 | Product workspace policy source. |
| V-04 | Product validation model source. |
| M-06/W-13/V-05 | External/domain dependency posture controls. |
| M-A | Migration phase closure audit; does not approve implementation readiness. |
| S/CSS/H series | Security, naming/substrate, and harness/runtime boundaries. |

Raw `2_products/` is not deeply inspected. Product candidate names and accepted posture may be retained as safe metadata only.

## 7. Product Charter Required Fields
| field | required? | meaning | acceptable value | blocker if missing |
| --- | --- | --- | --- | --- |
| product_id | Yes | Stable product candidate ID. | P00/P-charter ID. | Product not governable. |
| product_name | Yes | Candidate name. | P-00 selected name. | Unknown product. |
| product_status | Yes | Current product state. | candidate/deferred/local_only/etc. | State ambiguity. |
| selection_source | Yes | Selection evidence. | P-00 citation. | Not selected. |
| purpose | Yes | Why product exists. | Concise product purpose. | Purpose missing. |
| user/domain/interface hypothesis | Yes | Expected audience/surface. | Hypothesis with uncertainty. | Scope weak. |
| owner | Yes or gap | Responsible owner. | Named owner or owner gap. | Activation blocked. |
| scope | Yes | Included product work. | Product-scoped boundary. | Scope missing. |
| non_goals | Yes | Explicit exclusions. | Short exclusion list. | Scope creep. |
| product/root boundary | Yes | Root authority limits. | Product is not root authority. | Root collapse. |
| current local-only posture | Yes | Local-only handling. | `2_products/` ignored/local-only. | Exposure risk. |
| Git posture | Yes or P-08 | Tracking decision. | Local-only or deferred to P-08. | Git posture blocked. |
| validation baseline need | Yes | Future baseline need. | Need/gap/defer to P-10. | Validation gap. |
| security/access posture | Yes | Sensitivity/access constraints. | S-series posture. | Security blocked. |
| dependency posture | Yes | Package/SDK/native posture. | Blocked/review-needed. | Adoption risk. |
| external-source posture | Yes | External/domain relation. | Evidence only; cite M-06/W-13/V-05. | External risk. |
| provider/API/MCP posture | Yes | Runtime/network/auth surfaces. | Blocked unless governed later. | Activation risk. |
| generated-output posture | Yes | Logs/reports/builds/screens. | Local-only/generated-sensitive. | Output risk. |
| data/model/artifact posture | Yes | Data/model/artifact use. | Local-only/review-needed. | Sensitive use risk. |
| runtime/execution posture | Yes | Product execution state. | Not executed; blocked by default. | Execution risk. |
| implementation-readiness blockers | Yes | IR gaps. | Listed blockers. | Readiness overclaim. |
| activation blockers | Yes | Activation gaps. | Listed blockers. | Activation overclaim. |
| evidence/citations | Yes | Source support. | P-00/W-12/V-04/S/etc. | Uncited claim. |
| residual risks | Yes | Remaining uncertainty. | Risk list. | Hidden risk. |
| governance decision path | Yes | Who decides next. | Governance route or gap. | No decision path. |
| stop rules | Yes | When to stop. | Explicit stop conditions. | Unsafe continuation. |

## 8. Common Gate Checklist
| Gate | purpose | pass condition | caution condition | fail/block condition |
| --- | --- | --- | --- | --- |
| GATE-01 selected candidate exists in P-00 | Confirm route. | Candidate selected. | Disposition only. | Not in P-00. |
| GATE-02 owner declared or owner gap recorded | Expose accountability. | Owner named. | Owner gap recorded. | Owner absent and unrecorded. |
| GATE-03 purpose declared | State reason. | Purpose clear. | Purpose tentative. | Purpose missing. |
| GATE-04 scope declared | Bound work. | Scope clear. | Scope broad. | Scope missing. |
| GATE-05 non-goals declared | Prevent creep. | Non-goals clear. | Partial. | Missing. |
| GATE-06 product/root boundary declared | Prevent root collapse. | Boundary explicit. | Needs review. | Boundary missing. |
| GATE-07 local-only posture declared | Preserve safety. | Local-only stated. | Unknown sensitivity. | Exposure required. |
| GATE-08 security posture declared | Apply S-series. | Risks stated. | Review pending. | Secret/access risk. |
| GATE-09 dependency posture declared | Block adoption drift. | Blocked/reviewed posture. | Unclear package/SDK. | Adoption implied. |
| GATE-10 external-source posture declared | Control external evidence. | M-06/W-13/V-05 cited. | Relevance only. | External adoption implied. |
| GATE-11 Git posture declared or deferred to P-08 | Avoid tracking drift. | Local-only/deferred. | Path split unclear. | Tracking implied. |
| GATE-12 validation baseline need declared | Prepare V-04/P-10. | Need/gap stated. | Baseline later. | Baseline assumed. |
| GATE-13 generated-output posture declared | Control outputs. | Local-only/review-needed. | Unknown outputs. | Output as source. |
| GATE-14 provider/API/MCP posture declared | Block runtime surfaces. | Blocked by default. | Future review. | Activation implied. |
| GATE-15 activation blockers declared | Avoid activation. | Blockers listed. | Minor gaps. | No blockers despite gaps. |
| GATE-16 implementation-readiness blockers declared | Avoid IR overclaim. | Blockers listed. | Partial list. | Ready implied. |
| GATE-17 governance decision path declared | Set decision route. | Path stated. | Owner gap. | No path. |
| GATE-18 stop rules declared | Enforce boundaries. | Stop rules explicit. | Narrow. | Missing. |

## 9. Gate Status Model
Statuses: `gate_not_started`, `gate_ready_for_draft`, `gate_draft_complete`, `gate_passed_for_charter_review`, `gate_passed_with_cautions`, `gate_blocked_missing_owner`, `gate_blocked_missing_scope`, `gate_blocked_missing_boundary`, `gate_blocked_security_risk`, `gate_blocked_dependency_risk`, `gate_blocked_git_posture`, `gate_blocked_validation_gap`, `gate_blocked_activation_pressure`, `gate_rejected_for_current_phase`.

No gate status means active product status is not established. No gate status, passed gate status, or caution status activates a product.

## 10. Common Product Charter Template
Reusable skeleton only; do not instantiate it in P-01:
```markdown
# [P-XX] - [Product Name] Product Charter
## Document Header
Title, ticket, status, date, scope, authority, related documents.
## Purpose
Product purpose and P-00 selection route.
## Product Candidate Summary
product_id, product_name, product_status, selection_source.
## Owner / Governance
Owner or owner gap, governance path.
## Product Scope
In-scope product work only.
## Non-Goals
Out-of-scope items and blocked inferences.
## Product / Root Boundary
Product authority limits and root constraints.
## User / Domain / Interface Hypothesis
Expected users, domain, or interface surface.
## Current Local-only Posture
Ignored/local-only status and safe metadata limits.
## Security / Access Posture
Secrets, credentials, local data, access, execution limits.
## Dependency / External Source Posture
Product, domain, SDK, package, license, and external evidence posture.
## Provider / API / MCP Posture
Provider, network, auth, API, and MCP blocked/default posture.
## Generated Output / Data / Model / Artifact Posture
Output sensitivity, retention, and review needs.
## Git Posture
Current posture or P-08 deferral.
## Validation Baseline Needs
Need/gap for future P-10 baseline; no baseline execution.
## Activation Blockers
All blockers before activation can be considered.
## Implementation Readiness Blockers
All blockers before implementation readiness can be considered.
## Evidence / Source References
P-00, W-12, V-04, S-series, CSS-series, H-series, M-06/W-13/V-05 as relevant.
## Residual Risks
Open risks and revalidation triggers.
## Gate Checklist
GATE-01 through GATE-18 status.
## Final Charter Verdict
Draft verdict only; governance still decides.
```
The template is inert until used by future P-02 through P-07 tickets.

## 11. Product-specific Gate Overlays
| candidate | future ticket | overlay focus | mandatory cautions | blocked inference |
| --- | --- | --- | --- | --- |
| `omniverse-app` | P-02 | SDK/runtime/GPU/license/output/security/Git/root-boundary. | Omniverse/SDK unresolved; output/security review required. | SDK approval or product runtime. |
| `backend-energyplus` | P-03 | EnergyPlus/OpenStudio/native/data/license/validation. | Domain engine/native/license/data blockers. | Engine adoption or backend behavior. |
| `cli` | P-04 | command/shell/user-data/execution-safety. | Commands, packages, and user data blocked. | CLI safe to run. |
| `desktop` | P-05 | packaging/local-data/runtime/security/generated-output. | Desktop runtime, local data, packaging risks. | Release readiness. |
| `web-platform` | P-06 | auth/data/build/deploy/package/security. | Auth, build, deploy, package risks. | Web behavior or deploy approval. |
| `experimental` | P-07 | Disposition overlay, not product charter by default. | Split/defer/archive/reject before charter. | Roadmap priority or activation. |

## 12. Non-Activation Rules
P-01 does not activate products, accept charters, assign final product owners, approve source tracking, approve execution, approve dependencies, approve external source reuse, approve publication, or approve implementation readiness.

## 13. Product / Root Boundary Rules
Product charters cannot define root authority by implication. Product needs may inform future proposals only. Product docs remain product-scoped. Product source remains local-only unless governed later. Product dependency choices do not become root dependency choices. Product runtime decisions do not define root runtime decisions. Product output is evidence, not source by default.

## 14. Product Git Boundary
`2_products/` remains ignored/local-only. Product Git posture decision is deferred to P-08. P-01 does not change product Git posture. Product Git posture is not changed by P-01.

P-01 does not stage, commit, push, force-add, or publish. Future Git actions must use exact paths only. No `git add .`.

## 15. Dependency / External Source Boundary
External source presence is not adoption. EnergyPlus/OpenStudio relevance remains product/domain evidence only. Omniverse/SDK posture remains unresolved. Package references are not dependency approval. Provider/API/MCP references are not activation. P-09 will handle Product Dependency / External Source Posture. P-01 records required fields only.

## 16. Validation Boundary
P-01 does not create product validation baselines. P-10 will define Product Validation Baseline. P-01 defines what every charter must declare about validation needs. Proof level does not approve activation. Validation evaluates; governance decides.

## 17. Security / Local-only Boundary
Product secrets, credentials, configs, local sessions, data, models, artifacts, logs, and generated outputs are excluded or local-only by default. Unknown sensitivity blocks use. P-01 performs no product source inspection, product execution, provider/API/MCP/network/auth activation, or publication.

## 18. Cognitive Semantic System Boundary
Product charters cannot define the Cognitive Semantic System. The final Cognitive Semantic System substrate remains undecided. Graph remains a candidate only. Product visualization or graph needs may inform criteria but cannot decide root substrate.

## 19. Harness / Runtime Boundary
H-series and M-04 keep product runtime, harness, tool, provider, adapter, command, hook, skill, and MCP material as evidence only. No runtime activation or tool activation occurs. OpenCode/operator behavior is not platform authority.

## 20. Evidence / Citation Rules
Every future charter must cite P-00 selection status and W-12 product policy. Dependency/external claims must cite M-06/W-13/V-05. Validation claims must cite V-04. Security/local-only claims must cite S-series. CSS/substrate claims must cite CSS-series. Harness/runtime claims must cite H-series/M-04. Evidence supports charter review; evidence is not approval.

Minimum evidence for charter review: source path, source status, scope, sensitivity posture, cited claim, limitation, residual risk, and stop rule. Evidence cannot approve activation, dependency adoption, Git tracking, validation execution, implementation readiness, or publication.

## 21. Blocker Register
| blocker | stop behavior | required future action | blocks charter draft? | blocks charter acceptance? | blocks activation? |
| --- | --- | --- | --- | --- | --- |
| missing P-00 | Stop route claim. | Restore selection source. | Yes | Yes | Yes |
| missing W-12 | Stop product policy claim. | Restore policy. | Yes | Yes | Yes |
| missing M-07 | Stop prep claim. | Restore charter-prep source. | Yes | Yes | Yes |
| missing V-04 | Stop validation claim. | Restore product validation model. | Yes | Yes | Yes |
| product not selected | Do not draft. | Selection/disposition decision. | Yes | Yes | Yes |
| owner missing | Record gap. | Assign owner. | No | Yes | Yes |
| purpose missing | Stop charter claim. | Define purpose. | Yes | Yes | Yes |
| scope missing | Stop scope claim. | Define scope. | Yes | Yes | Yes |
| non-goals missing | Qualify scope. | Add exclusions. | No | Usually | Usually |
| root boundary missing | Stop authority claim. | Add root boundary. | Yes | Yes | Yes |
| local-only posture missing | Stop exposure. | Add local-only posture. | Yes | Yes | Yes |
| Git posture missing | Keep local-only. | P-08 decision or deferral. | No | Yes | Yes |
| validation baseline need missing | Stop readiness. | P-10 need statement. | No | Yes | Yes |
| security posture missing | Stop exposure/action. | Security review. | Yes | Yes | Yes |
| dependency posture missing | Stop adoption framing. | P-09/dependency review. | Yes | Yes | Yes |
| external-source posture missing | Stop external claim. | M-06/W-13/V-05 review. | Yes | Yes | Yes |
| generated-output posture missing | Exclude outputs. | Output review. | No | Yes | Yes |
| provider/API/MCP posture missing | Stop runtime path. | Security/governance review. | No | Yes | Yes |
| product source inspection required | Stop P-01. | Future exact product scope. | Yes | Yes | Yes |
| product activation implied | Stop. | Governance activation ticket. | Yes | Yes | Yes |
| dependency adoption implied | Stop. | Dependency governance. | Yes | Yes | Yes |
| external adoption implied | Stop. | External review/governance. | Yes | Yes | Yes |
| product Git tracking implied | Stop Git path. | P-08 decision. | Yes | Yes | Yes |
| publication implied | Stop publication path. | Publication/security review. | Yes | Yes | Yes |
| implementation readiness implied | Stop IR claim. | Future IR governance. | Yes | Yes | Yes |
| substrate decision pressure | Stop CSS claim. | Future CSS decision. | Yes | Yes | Yes |
| P-02 scope pressure detected | Stop adjacent work. | Wait explicit P-02 instruction. | No | No | No |

## 22. Residual Risk Register
No individual product charters yet. No accepted product charters, product owners, final product scopes, validation baselines, product Git posture decision, dependency approvals, external-source approvals, product security reviews, generated-output reviews, or implementation readiness exists. `experimental` still awaits disposition.

## 23. P-01 Invariants
| ID | Invariant |
| --- | --- |
| P01-001 | Product charter template is not product activation. |
| P01-002 | Common gate is not charter acceptance. |
| P01-003 | Selected product remains inactive until governed. |
| P01-004 | Product source remains local-only. |
| P01-005 | Product Git posture is not changed. |
| P01-006 | Product dependencies are not adopted. |
| P01-007 | Product validation baselines are not created. |
| P01-008 | Product charters are not created by P-01. |
| P01-009 | External/domain metadata is evidence only. |
| P01-010 | Product needs do not decide root architecture. |
| P01-011 | Graph remains a candidate only. |
| P01-012 | Validation evaluates; governance decides. |
| P01-013 | P-01 stops before P-02. |

## 24. Anti-patterns
Anti-patterns: template as accepted charter; gate as activation approval; charter by folder existence; charter by enthusiasm; product source inspection by curiosity; product Git tracking by implication; dependency adoption by relevance; external source reuse by proximity; validation baseline assumed from template; product output as source; graph/product visualization as substrate decision; starting P-02 inside P-01; `git add .`.

## 25. Readiness For P-02
P-02 - Omniverse App Product Charter is ready after explicit instruction if P-01 common template/gate exists, P-00 selected `omniverse-app` for charter drafting, product/local-only/Git/dependency/security boundaries are preserved, and no product activation, source tracking, dependency adoption, publication, provider/API/MCP activation, or implementation is implied.

Do not create P-02.

## 26. Final Verdict
| Question | Answer |
| --- | --- |
| What does P-01 create? | The canonical Product Charter Template / Common Product Gate document. |
| Did P-01 create individual product charters? | No. |
| Did P-01 activate products? | No. |
| Did P-01 inspect product source deeply? | No. |
| Did P-01 change product Git posture? | No. |
| Did P-01 adopt dependencies? | No. |
| Did P-01 create validation baselines? | No. |
| What remains blocked? | Individual charters, activation, source inspection, execution, tests/builds, package managers, dependency adoption, external adoption, product Git tracking, validation baselines, publication, provider/API/MCP/network/auth activation, implementation readiness, staging, commit, push, and P-02. |
| Is P-02 ready after explicit instruction? | Yes, as Omniverse App Product Charter drafting only; P-02 is not started. |

Stop after P-01 validation and report. Do not start P-02 or any later ticket.
