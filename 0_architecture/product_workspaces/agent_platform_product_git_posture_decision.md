# P-08 - Product Git Posture Decision
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Product Git Posture Decision |
| Ticket | P-08 |
| Status | Accepted product Git posture decision |
| Date | 2026-07-01 |
| Scope | Git posture for AGENT PLATFORM product governance documentation and local-only Siamese product workspaces after P-00 through P-07. |
| Authority | Git posture governance only; not staging, commit, push, publication, product activation, or source tracking action. |
| Related documents | P-00 through P-07, M-A, M-07, M-06, M-08, W-12, W-11, W-03, W-13, V-01, V-02, V-04, V-05, S-series, CSS-series, H-series, Siamese Product Vision |

## 2. Purpose
P-08 decides the current Git posture for product work after the product workspace selection, common gate, five inactive product charter drafts, and experimental disposition.

P-08 allows product governance documentation under `0_architecture/product_workspaces/` to be trackable as documentation only. P-08 does not track product source, inspect product source deeply, activate products, adopt dependencies, create validation baselines, modify `.gitignore`, stage, commit, push, force-add, publish, or start P-09.

## 3. Product Git Posture Decision Definition
Product Git posture is the governed decision about what product-related material may be versioned, what must remain local-only, what Git actions are blocked, and what future evidence is required before changing posture.

Git posture is not product activation, implementation readiness, dependency approval, validation approval, publication approval, or root authority.

## 4. Decision Summary
| Area | P-08 decision | Boundary |
| --- | --- | --- |
| Product governance docs | Trackable as docs only under `0_architecture/product_workspaces/`. | No activation or source approval. |
| Product source | Not trackable now. `2_products/` remains ignored/local-only. | No force-add or exception. |
| Generated/local/sensitive material | Not trackable now. | Exclude outputs, data, models, artifacts, logs, caches, secrets, credentials, sessions, and dependency folders. |
| `.gitignore` | Unchanged. | No ignore-rule edit in P-08. |
| Git actions | No staging, commit, push, force-add, amend, reset, clean, or publication. | Future Git action requires explicit approval and exact paths only. |
| Next posture work | P-09 dependency/external posture after explicit instruction only. | P-08 stops before P-09. |

## 5. Authority Boundary
| Layer | P-08 rule |
| --- | --- |
| Governance | Decides Git posture, exceptions, activation, publication, and future source tracking. |
| Validation | Evaluates Git/local-only evidence; validation does not approve tracking or activation. |
| Security | Blocks local-only leaks, secrets, credentials, unsafe execution, provider/API/MCP/network/auth exposure, and publication. |
| Product docs | Product-scoped governance evidence only. |
| Product source | Local-only candidate material until future exact governance changes posture. |
| Agents | May create this decision document; cannot stage, commit, push, force-add, run product code, install dependencies, or activate products. |

## 6. Source Boundary
P-08 uses accepted architecture and governance documents only. Raw `2_products/`, product generated outputs, `4_external/sources/`, and `previusknowledge/` are not deeply inspected.

Safe metadata from P-00 through P-07, W-12, V-04, S-series, CSS-series, and H-series is sufficient for this docs-only Git posture decision.

## 7. Existing Product Governance Inputs
| Input | P-08 use |
| --- | --- |
| P-00 | Product workspace routes for six candidates. |
| P-01 | Common product charter gate and Git posture field. |
| P-02 through P-06 | Inactive charters for `omniverse-app`, `backend-energyplus`, `cli`, `desktop`, and `web-platform`. |
| P-07 | `experimental` disposition as blocked local-only sandbox. |
| W-12 | Product workspace policy and Git posture options. |
| V-04 | Product validation and product Git validation boundaries. |
| S-series | Local-only, secrets, credentials, execution, access, and Git safety boundaries. |
| CSS-series | Cognitive Semantic System naming and substrate boundary. |
| H-series | Harness/runtime/provider/tool/MCP boundary. |

## 8. Current Product Candidate State
| Product candidate | Siamese role | Current state | Product source tracking decision |
| --- | --- | --- | --- |
| `omniverse-app` | Advanced visual/3D Omniverse interface candidate. | Inactive charter draft with blockers. | Not trackable now. |
| `backend-energyplus` | Future energy-domain backend candidate. | Inactive charter draft with blockers. | Not trackable now. |
| `cli` | Operator/scriptable interface candidate. | Inactive charter draft with blockers. | Not trackable now. |
| `desktop` | Local desktop/interface candidate. | Inactive charter draft with blockers. | Not trackable now. |
| `web-platform` | Browser/deployed interface candidate. | Inactive charter draft with blockers. | Not trackable now. |
| `experimental` | Ambiguous sandbox/prototype candidate. | Blocked local-only disposition. | Not trackable now. |

No candidate is active. No candidate receives implementation readiness, dependency adoption, validation baseline, publication approval, or product source tracking approval from P-08.

## 9. Current Local-only Git Evidence
`.gitignore` keeps `2_products/` ignored/local-only. It also ignores external sources, previous knowledge corpus, datasets, models, artifacts, generated/runtime folders, dependency folders, secrets, credentials, provider auth, and local caches.

Git state is evidence, not authority. `git status`, `git diff`, and `git check-ignore` may support review, but they do not activate products or approve tracking.

## 10. Trackable Now
Trackable now means eligible for future exact-path staging after explicit human approval; P-08 itself does not stage anything.

| Material | Trackable posture | Reason |
| --- | --- | --- |
| `0_architecture/product_workspaces/agent_platform_product_workspace_selection.md` | Trackable as product governance documentation. | P-00 route decision. |
| `0_architecture/product_workspaces/agent_platform_product_charter_template_common_gate.md` | Trackable as product governance documentation. | P-01 common gate. |
| `0_architecture/product_workspaces/agent_platform_omniverse_app_product_charter.md` | Trackable as product governance documentation. | P-02 inactive charter draft. |
| `0_architecture/product_workspaces/agent_platform_backend_energyplus_product_charter.md` | Trackable as product governance documentation. | P-03 inactive charter draft. |
| `0_architecture/product_workspaces/agent_platform_cli_product_charter.md` | Trackable as product governance documentation. | P-04 inactive charter draft. |
| `0_architecture/product_workspaces/agent_platform_desktop_product_charter.md` | Trackable as product governance documentation. | P-05 inactive charter draft. |
| `0_architecture/product_workspaces/agent_platform_web_platform_product_charter.md` | Trackable as product governance documentation. | P-06 inactive charter draft. |
| `0_architecture/product_workspaces/agent_platform_experimental_workspace_disposition.md` | Trackable as product governance documentation. | P-07 disposition decision. |
| `0_architecture/product_workspaces/agent_platform_product_git_posture_decision.md` | Trackable as product governance documentation. | P-08 Git posture decision. |

These files are architecture evidence only. Tracking them does not track product source and does not activate any product.

## 11. Not Trackable Now
| Material | P-08 posture | Reason |
| --- | --- | --- |
| `2_products/` source and product internals | Not trackable now. | Local-only, inactive, source sensitivity and readiness unresolved. |
| Product generated outputs | Not trackable now. | Output provenance and sensitivity unresolved. |
| Product logs, runs, outputs, temp, cache | Not trackable now. | Runtime/generated-sensitive. |
| Product datasets, models, artifacts | Not trackable now. | Data/model/artifact review absent. |
| Product dependency folders and build outputs | Not trackable now. | Dependency/build posture unresolved. |
| Secrets, credentials, tokens, keys, provider auth, local sessions | Never track by default. | Security blocker. |
| `4_external/sources/` raw external sources | Not trackable now. | External-source governance remains separate. |
| `previusknowledge/` corpus material | Not trackable now. | Migration corpus remains local-only. |

## 12. Product Governance Documentation Rule
Product governance documentation under `0_architecture/product_workspaces/` may be tracked because it records safe metadata, decisions, blockers, and boundaries without exposing product source.

Tracked product governance documentation remains product-scoped and architecture-scoped evidence. It cannot override root architecture, root governance, validation rules, security rules, or the Cognitive Semantic System.

## 13. Product Source Rule
`2_products/` remains ignored/local-only. Product source is not approved for tracking, force-adding, staging, commit, publication, or context inclusion by P-08.

Future source tracking requires a separate exact-scope governance decision after product owner, purpose, scope, non-goals, root boundary, dependency posture, security/access posture, generated-output posture, validation baseline, repository strategy, and exact include/exclude list are accepted.

## 14. Generated, Local, and Sensitive Material Rule
Generated output is not source by default. Local data is not safe by default. Unknown sensitivity blocks tracking and publication.

Excluded material includes reports, screenshots, simulations, logs, exports, build outputs, caches, datasets, models, artifacts, local databases, browser state, desktop state, CLI logs, Omniverse artifacts, EnergyPlus outputs, web bundles, credentials, tokens, keys, environment files, provider auth, package registry auth, and local sessions.

## 15. `.gitignore` Rule
P-08 does not modify `.gitignore`. The current ignore rules remain valid evidence for local-only posture.

Future `.gitignore` changes for product source, if ever needed, require separate governance, exact paths, security review, source classification, and explicit human approval. P-08 grants no such change.

## 16. Force-add and Broad Staging Rule
Force-adding ignored local-only material is blocked. Broad staging is blocked.

Do not use `git add .`. Do not use `git add -f` for product source, external sources, previous knowledge corpus, generated outputs, secrets, credentials, dependency folders, local sessions, or ignored local-only material.

## 17. Exact-path Future Git Rule
If a future human-approved Git action occurs for product governance documentation, it must use exact intended paths only. Approval for one path does not imply approval for sibling paths, product source, ignored roots, generated outputs, or later tickets.

P-08 does not execute any Git mutation. No staging, commit, push, amend, reset, clean, release, deploy, publication, or force-add occurs here.

## 18. Product Activation Boundary
Tracking product governance documentation does not activate products. Product activation still requires owner, accepted charter, scope, non-goals, root boundary, Git posture, dependency posture, security/access posture, validation baseline, generated-output posture, governance path, and residual risk review.

All six product candidates remain inactive or blocked after P-08.

## 19. Dependency and External Boundary
P-08 does not adopt EnergyPlus, OpenStudio, Omniverse/Kit, web frameworks, CLI packages, desktop runtimes, SDKs, APIs, providers, datasets, models, or external source material.

Product Dependency / External Source Posture is deferred to P-09 after explicit instruction only. P-08 does not start P-09.

## 20. Validation Boundary
Validation evaluates; governance decides. P-08 does not create or execute product validation baselines, run product tests, run builds, run package managers, start servers, execute simulations, or validate product behavior.

Product Validation Baseline remains deferred to P-10 after explicit instruction only.

## 21. Security and Local-only Boundary
Secrets, credentials, auth material, provider configs, tokens, local sessions, local data, and generated-sensitive outputs remain excluded. Unknown sensitivity blocks tracking, context exposure, publication, and runtime action.

No provider/API/MCP/network/auth activation occurs. No product code, product tests, product builds, package managers, external/native tools, deployment, or publication is run by P-08.

## 22. Cognitive Semantic System Boundary
Siamese product needs do not decide the Cognitive Semantic System. The Cognitive Semantic System remains root-governed and not product-owned.

Graph remains a candidate substrate only. Product visualization, dashboard, simulation, or reporting needs may inform future criteria but cannot decide semantic truth, root authority, or final substrate.

## 23. Harness, Runtime, and Provider Boundary
Harness, runtime, provider, adapter, tool, hook, skill, and MCP material remains evidence only unless separately governed. Tool availability is not permission. Provider credentials are not provider permission. MCP availability is not MCP activation.

P-08 does not activate runtime behavior or implementation artifacts.

## 24. Future Posture Preconditions
Future product source tracking cannot be considered until the target product has: accepted owner, accepted scope, non-goals, root/product boundary, dependency/external posture, security/access posture, generated-output posture, validation baseline, source classification, secret/credential review, exact include/exclude list, repository strategy, rollback/removal strategy, and explicit governance approval.

Future source tracking must also decide whether the product remains in this repository, moves to a separate repository, uses a submodule/reference strategy, or remains local-only.

## 25. Future Posture Options
| Option | Current P-08 status | Notes |
| --- | --- | --- |
| Keep product source local-only | Accepted now. | Default for all product source. |
| Track product governance docs only | Accepted now. | Applies to exact docs under `0_architecture/product_workspaces/`. |
| Track selected product source in this repo | Blocked now. | Requires later exact governance and review. |
| Split product into separate repository | Deferred. | Candidate for mature products after repository strategy. |
| Submodule/subtree/reference-only | Deferred. | Requires operational policy. |
| Archive/defer product material | Deferred. | Requires archive/lifecycle governance; P-08 does not archive. |

## 26. Blocker and Residual Risk Register
| Risk or blocker | Current posture | Required future action |
| --- | --- | --- |
| Product owners not finalized | Blocks activation and source tracking. | Assign governed owners. |
| Product source sensitivity unknown | Blocks tracking and publication. | Exact security/source review. |
| Dependency posture unresolved | Blocks activation and source tracking. | P-09 or later dependency review. |
| Validation baselines absent | Blocks activation and readiness. | P-10 or later baseline. |
| Generated-output posture incomplete | Blocks output tracking/publication. | Output provenance and sensitivity policy. |
| Product implementation readiness absent | Blocks implementation. | Future IR governance. |
| Experimental remains ambiguous | Blocks charter/source tracking. | Future split/archive/defer review. |
| `.gitignore` exceptions absent | Preserves local-only posture. | Separate future exact governance if needed. |

## 27. P-08 Invariants and Anti-patterns
| ID | Invariant |
| --- | --- |
| P08-001 | Product Git posture decision is not Git action. |
| P08-002 | Product governance docs are trackable as docs only. |
| P08-003 | Product source under `2_products/` is not trackable now. |
| P08-004 | `.gitignore` is unchanged. |
| P08-005 | No broad staging or force-add is authorized. |
| P08-006 | Product activation remains blocked. |
| P08-007 | Product dependencies are not adopted. |
| P08-008 | Product validation baselines are not created. |
| P08-009 | Git state is evidence, not authority. |
| P08-010 | Validation evaluates; governance decides. |
| P08-011 | Graph remains a candidate substrate only. |
| P08-012 | P-08 stops before P-09. |

Anti-patterns: Git tracking as activation; docs-only tracking as source approval; product source force-add by cleanup pressure; broad staging; product source inspection by curiosity; generated output as source; dependency adoption by repository proximity; validation baseline by implication; `.gitignore` edit as posture shortcut; Git history as semantic truth; product need deciding the Cognitive Semantic System; starting P-09 inside P-08; `git add .`.

## 28. Final Verdict and Stop Rule
| Question | Answer |
| --- | --- |
| What does P-08 decide? | Product governance documentation under `0_architecture/product_workspaces/` is trackable as documentation only; product source remains local-only and not trackable now. |
| Did P-08 approve source tracking under `2_products/`? | No. |
| Did P-08 modify `.gitignore`? | No. |
| Did P-08 authorize force-adds or broad staging? | No. |
| Did P-08 stage, commit, push, or publish? | No. |
| Did P-08 activate any Siamese product? | No. |
| Did P-08 adopt dependencies or activate providers/API/MCP/network/auth? | No. |
| Did P-08 create validation baselines or implementation artifacts? | No. |
| What remains blocked? | Product source tracking, product activation, dependency adoption, validation baselines, implementation readiness, publication, generated-output tracking, force-adds, broad staging, commits, pushes, and P-09. |
| Is P-09 ready after explicit instruction? | Yes, as Product Dependency / External Source Posture only; P-09 is not started. |

Stop after P-08 validation and report. Do not start P-09 or any later ticket.
