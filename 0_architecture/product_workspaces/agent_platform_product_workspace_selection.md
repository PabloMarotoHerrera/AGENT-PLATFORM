# P-00 - Product Workspace Selection
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Product Workspace Selection |
| Ticket | P-00 |
| Status | Accepted product workspace selection |
| Date | 2026-07-01 |
| Scope | Selection of AGENT PLATFORM product workspace candidates for future charter drafting or disposition review during FASE 4 - Product Workspace Governance |
| Authority | Selection planning only, not product activation |
| Related documents | M-A, M-07, M-06, W-12, V-04, W-13, V-05, S-series, CSS-series, H-series |

## 2. Purpose
M-A closed the controlled migration phase at audit-only level. It did not approve product activation or implementation readiness.

M-07 prepared product workspace charter metadata for six product candidates. P-00 selects which candidates move to future charter drafting, which candidate needs disposition review, and what order future product governance tickets should follow.

P-00 does not activate products, create active charters, approve implementation, or start P-01. It prepares P-01 - Product Charter Template / Common Product Gate after explicit instruction only.

## 3. Product Workspace Selection Definition
Product workspace selection is a governance planning step that assigns product candidates to future charter drafting, deferral, disposition, or blocked status based on documented metadata, risk posture, local-only posture, validation gaps, dependency posture, Git posture, and governance readiness.

Selection is not activation. `selected_for_charter_drafting` is not active, not implementation-ready, not dependency approval, not product Git tracking, and not publication approval.

## 4. Authority Boundary
| Layer | P-00 boundary |
| --- | --- |
| Governance | Decides final product activation, owners, product Git posture, dependency adoption, publication, and lifecycle. |
| Validation | Evaluates product readiness only; proof does not approve activation. |
| Security | Constrains local-only handling, secrets, credentials, execution, provider/API/MCP/network, Git, and publication. |
| Product selection | Routes candidates only. |
| Agents | May prepare safe metadata but cannot activate, inspect deeply, execute, adopt dependencies, stage, commit, push, or publish. |

## 5. Source Boundary
W-12 is the primary product policy source. M-07 is the primary product charter-preparation source. M-A is the phase-closure audit source. M-06, W-13, and V-05 control external/domain dependency posture. V-04 controls product validation posture.

Raw `2_products/` is not deeply inspected. Product candidate names and posture from accepted documents may be retained as safe metadata only.

## 6. Product Candidate Inventory
| candidate_id | product candidate | current posture | likely area | main risk | selection status | rationale | blocked inference |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PROD-001 | `backend-energyplus` | candidate/deferred/local_only | Backend/domain simulation | EnergyPlus/native/license/data | `selected_for_charter_drafting` | High domain value; blockers need early charter exposure. | Engine approval or backend behavior. |
| PROD-002 | `cli` | candidate/deferred/local_only | CLI/operator interface | Commands/packages/user data | `selected_for_charter_drafting` | Interface surface needs scoped command boundary. | CLI works or is safe to run. |
| PROD-003 | `desktop` | candidate/deferred/local_only | Desktop/local runtime | Runtime/packaging/local data | `selected_for_charter_drafting` | Runtime and packaging risks need charter gate. | Desktop app behavior or release readiness. |
| PROD-004 | `experimental` | experimental/blocked/local_only | Prototype/sandbox | Unclear source/root leakage | `selected_for_disposition_review` | Should not become a charter by default. | Roadmap priority or activation. |
| PROD-005 | `omniverse-app` | candidate/deferred/local_only | Omniverse/visualization | SDK/runtime/GPU/license/output | `selected_for_charter_drafting` | High strategic visualization value with heavy blockers. | Product claim or SDK approval. |
| PROD-006 | `web-platform` | candidate/deferred/local_only | Web/interface | Auth/data/build/deploy | `selected_for_charter_drafting` | Interface/deployment surface needs scope and baseline. | Web behavior or deploy readiness. |

## 7. Selection Criteria
| Criterion | Meaning | Selection impact | Blocker condition |
| --- | --- | --- | --- |
| Strategic relevance | Fits likely product direction. | Raises drafting priority. | No purpose signal. |
| Architecture relevance | Exposes root/product boundary needs. | Select if charter clarifies architecture. | Root collapse risk unresolved. |
| Dependency risk | External/domain/package risk level. | High risk can justify early charter. | Adoption implied. |
| External-source risk | W-13/V-05 source posture. | Keep review fields explicit. | Source reuse/execution implied. |
| Local-only/security risk | Secrets, configs, sessions, outputs. | Require safe metadata only. | Unknown sensitivity. |
| Validation baseline feasibility | Can future baseline be stated. | Select if gaps are nameable. | Baseline impossible or absent. |
| Product/root boundary clarity | Product can remain scoped. | Select if boundary can be written. | Product defines root. |
| Git posture clarity | Future tracking can be governed. | Select docs-first only. | Git posture assumed. |
| Implementation sequencing value | Charter helps later order. | Raises priority. | Implementation implied. |
| Inactive during drafting | Can stay inactive. | Required for selection. | Activation pressure. |

## 8. Selection Status Model
| Status | Meaning | Boundary |
| --- | --- | --- |
| `selected_for_charter_drafting` | Candidate should receive a future product charter draft. | Not active. |
| `selected_for_disposition_review` | Candidate needs split/defer/archive/reject review before chartering. | Not active. |
| `deferred_pending_owner` | Owner absent blocks progress. | No activation. |
| `deferred_pending_scope` | Scope/non-goals absent. | No activation. |
| `deferred_pending_dependency_review` | Dependency/domain posture unresolved. | No adoption. |
| `deferred_pending_security_review` | Security/local-only posture unresolved. | Safe metadata only. |
| `deferred_pending_git_posture` | Tracking decision missing. | No Git change. |
| `blocked_for_activation` | Activation preconditions missing. | Cannot activate. |
| `rejected_for_current_phase` | Not suitable for FASE 4. | Retain evidence only. |

No status means active product.

## 9. Proposed Charter Drafting Order
1. P-01 Product Charter Template / Common Product Gate.
2. P-02 Omniverse App Product Charter.
3. P-03 Backend EnergyPlus Product Charter.
4. P-04 CLI Product Charter.
5. P-05 Desktop Product Charter.
6. P-06 Web Platform Product Charter.
7. P-07 Experimental Workspace Disposition.

P-01 comes first because every product charter needs common gate fields. Omniverse and backend are high strategic/domain value but dependency-heavy, so charters must expose blockers early. CLI, desktop, and web are interface/runtime surfaces and must remain inactive until scoped. Experimental should not become a charter by default; it needs disposition.

## 10. Product Selection Table
| selection_id | candidate | selected route | reason | required future charter/disposition fields | major blockers | next ticket |
| --- | --- | --- | --- | --- | --- | --- |
| P00-SEL-001 | `omniverse-app` | Charter drafting | Strategic visualization candidate. | Purpose, owner, SDK/license, output, security, Git, root boundary. | SDK/runtime/GPU/license. | P-02 |
| P00-SEL-002 | `backend-energyplus` | Charter drafting | Core domain/backend candidate. | Purpose, owner, EnergyPlus/OpenStudio posture, data, validation, Git. | Native/domain/license/data. | P-03 |
| P00-SEL-003 | `cli` | Charter drafting | Operator/interface candidate. | Purpose, owner, command scope, execution rules, validation, Git. | Command/package/user-data risk. | P-04 |
| P00-SEL-004 | `desktop` | Charter drafting | Local runtime/interface candidate. | Purpose, owner, packaging, local data, security, generated outputs. | Desktop runtime/local credentials. | P-05 |
| P00-SEL-005 | `web-platform` | Charter drafting | Web/interface candidate. | Purpose, owner, auth/data/build/deploy, validation, dependency posture. | Web packages/auth/deploy. | P-06 |
| P00-SEL-006 | `experimental` | Disposition review | Sandbox should not activate by proximity. | Owner, isolation, split/defer/archive/reject path, root boundary. | Unclear scope and leakage risk. | P-07 |

## 11. Non-Activation Rules
P-00 does not activate any product, assign product owners as final authority, approve product source tracking, approve execution, approve dependencies, approve external source reuse, approve publication, or approve implementation readiness.

## 12. Product Git Boundary
`2_products/` remains ignored/local-only. Product source remains untracked unless future governance changes posture. Product Git posture decision is deferred to P-08. Product Git posture is not changed by P-00.

P-00 does not stage, commit, push, force-add, or publish. Future Git actions must use exact paths only. No `git add .`.

## 13. Dependency / External Boundary
EnergyPlus and OpenStudio relevance remains product/domain evidence only. Omniverse/SDK dependency posture remains unresolved. Web, CLI, and Desktop packages remain unapproved.

External source presence is not adoption. Dependency references are not dependency approval. Provider/API/MCP references are not activation.

## 14. Validation Boundary
Product validation baselines do not exist yet. P-00 does not create baselines. P-10 will define Product Validation Baseline. P-00 records validation gaps only. Proof level does not approve activation.

## 15. Security / Local-only Boundary
Product secrets, credentials, configs, local sessions, data, models, artifacts, logs, and generated outputs are excluded. Generated outputs remain local-only by default. Unknown sensitivity blocks use.

P-00 performs no product source inspection, product execution, product tests/builds/package-manager actions, provider/API/MCP/network/auth activation, or publication.

## 16. Cognitive Semantic System Boundary
Product candidates do not define the Cognitive Semantic System. The final Cognitive Semantic System substrate remains undecided. Graph remains a candidate only.

Product visualization or graph needs may inform future criteria but cannot decide root substrate.

## 17. Harness / Runtime Boundary
H-series and M-04 keep product runtime, harness, tool, provider, and MCP material as evidence only. No runtime or tool activation occurs. OpenCode/operator behavior is not platform authority.

## 18. Blocker Register
| blocker | stop behavior | required future action | blocks selection? | blocks charter drafting? | blocks activation? |
| --- | --- | --- | --- | --- | --- |
| missing W-12 | Stop selection. | Restore product policy. | Yes | Yes | Yes |
| missing M-07 | Stop selection. | Restore charter-prep source. | Yes | Yes | Yes |
| missing M-A | Stop phase claim. | Restore audit source. | Yes | Yes | Yes |
| missing V-04 | Stop validation claims. | Restore validation model. | Yes | Yes | Yes |
| product candidate unknown | Do not route. | Classify candidate. | Yes | Yes | Yes |
| product owner missing | Record gap. | Assign future owner. | No | Maybe | Yes |
| product scope missing | Record gap. | Define scope/non-goals. | No | Maybe | Yes |
| product/root boundary missing | Stop authority claim. | Add root boundary. | No | Yes | Yes |
| product Git posture missing | Keep local-only. | P-08 Git posture decision. | No | No | Yes |
| validation baseline missing | Record gap. | P-10 baseline. | No | No | Yes |
| dependency posture unresolved | Stop adoption. | Dependency review. | No | Maybe | Yes |
| security posture unresolved | Safe metadata only. | Security review. | No | Maybe | Yes |
| generated-output posture unresolved | Exclude outputs. | Output review. | No | Maybe | Yes |
| product source inspection required | Stop P-00. | Future exact product scope. | No | Maybe | Yes |
| product activation implied | Stop. | Governance activation ticket. | Yes | Yes | Yes |
| dependency adoption implied | Stop. | Dependency governance. | Yes | Yes | Yes |
| external adoption implied | Stop. | External review/governance. | Yes | Yes | Yes |
| provider/API/MCP activation implied | Stop. | Security/governance approval. | Yes | Yes | Yes |
| substrate decision pressure | Stop. | Future CSS decision. | Yes | Yes | Yes |
| P-01 scope pressure detected | Stop adjacent work. | Wait explicit instruction. | No | No | No |

## 19. Residual Risk Register
| Risk | Status |
| --- | --- |
| No accepted product charters | Open. |
| No product owners | Open. |
| No final product scopes | Open. |
| No validation baselines | Open. |
| No product Git posture decision | Open; P-08 later. |
| No dependency approvals | Open. |
| No product security review | Open. |
| No generated-output review | Open. |
| No implementation readiness | Open. |
| Experimental workspace unclear | Open; P-07 disposition later. |

## 20. P-00 Invariants
| ID | Invariant |
| --- | --- |
| P00-001 | Product selection is not product activation. |
| P00-002 | Selected for charter does not mean active. |
| P00-003 | Product source remains local-only. |
| P00-004 | Product Git posture is not changed. |
| P00-005 | Product dependencies are not adopted. |
| P00-006 | Product validation baselines are not created. |
| P00-007 | Product charters are not accepted by P-00. |
| P00-008 | External/domain metadata is evidence only. |
| P00-009 | Product needs do not decide root architecture. |
| P00-010 | Graph remains a candidate only. |
| P00-011 | Validation evaluates; governance decides. |
| P00-012 | P-00 stops before P-01. |

## 21. Anti-patterns
Anti-patterns: selection as activation; selection as implementation readiness; selection by folder existence; selection by product enthusiasm; product source inspection by curiosity; product Git tracking by implication; dependency adoption by proximity; external source reuse by relevance; validation baseline assumed from selection; graph/product visualization as substrate decision; starting P-01 inside P-00; `git add .`.

## 22. Readiness For P-01
P-01 - Product Charter Template / Common Product Gate is ready after explicit instruction if P-00 exists, all six candidates have selection status, selected candidates remain inactive, product/local-only/Git/dependency/security boundaries are preserved, and no product activation, source tracking, dependency adoption, publication, or implementation is implied.

Do not create P-01.

## 23. Final Verdict
| Question | Answer |
| --- | --- |
| What did P-00 select? | Product routes for future charter drafting or disposition review. |
| Which candidates move to charter drafting? | `omniverse-app`, `backend-energyplus`, `cli`, `desktop`, and `web-platform`. |
| Which candidate moves to disposition review? | `experimental`. |
| Did P-00 activate products? | No. |
| Did P-00 inspect product source deeply? | No. |
| Did P-00 change product Git posture? | No. |
| Did P-00 adopt dependencies? | No. |
| Did P-00 create accepted product charters? | No. |
| What remains blocked? | Product activation, accepted charters, source inspection, execution, tests/builds, dependency adoption, external adoption, product Git changes, publication, provider/API/MCP activation, implementation readiness, staging, commit, push, and P-01. |
| Is P-01 ready after explicit instruction? | Yes, as Product Charter Template / Common Product Gate only. |

Stop after P-00 validation and report. Do not start P-01 or any later ticket.
