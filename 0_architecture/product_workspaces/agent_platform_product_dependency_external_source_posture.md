# P-09 - Product Dependency / External Source Posture
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Product Dependency / External Source Posture |
| Ticket | P-09 |
| Status | Accepted product dependency and external source posture |
| Date | 2026-07-01 |
| Scope | Current dependency and external-source posture for inactive Siamese product workspaces after P-00 through P-08. |
| Authority | Dependency/external posture only, not dependency adoption. |
| Related documents | P-00 through P-08, M-A, M-06, W-03, W-12, W-13, V-04, V-05, S-series, CSS-series, H-series, Siamese Product Vision |

## 2. Purpose
P-00 selected product routes. P-01 defined the common gate. P-02 through P-06 drafted inactive product charters. P-07 blocked `experimental` as a local-only sandbox. P-08 decided docs-only Git posture and blocked product source tracking.

P-09 decides dependency/external-source posture for all product workspaces. It does not adopt dependencies, install, execute, inspect source deeply, activate products, change Git posture, create validation baselines, or start P-10. It prepares P-10 - Product Validation Baseline after explicit instruction only.

## 3. Dependency / External Source Posture Definition
Dependency/external posture is a governance decision describing which dependencies, SDKs, runtimes, external sources, providers, protocols, packages, native tools, hosting services, and domain tools are relevant to product candidates, and what review gates must pass before future adoption.

Siamese dependency needs do not decide the Cognitive Semantic System. Graph remains a candidate only.

Relevance is not adoption. Source presence is not trust. License evidence is not reuse approval. Package reference is not dependency approval. Runtime availability is not execution approval. Provider credentials are not provider permission. MCP availability is not MCP activation. Product dependency is not root dependency.

## 4. Decision Summary
No product dependency is adopted by P-09. No external source is adopted by P-09. No source reuse is approved. No package, runtime, SDK, native tool, provider, API, MCP, network, or auth use is approved.

All dependencies remain candidates or blocked evidence. Product-specific dependency review is deferred to future exact product/dependency tickets. P-10 may use this posture as validation input only.

## 5. Authority Boundary
| Layer | P-09 boundary |
| --- | --- |
| Governance | Decides dependency adoption, source reuse, provider/API/MCP activation, product activation, publication, and exceptions. |
| Validation | Evaluates dependency/source readiness; it does not approve adoption. |
| Security | Constrains secrets, credentials, runtime execution, network, auth, local-only data, generated outputs, and publication. |
| Product charters | Identify candidate dependencies only. |
| Agents | May prepare safe metadata; cannot install, execute, adopt, authenticate, stage, commit, push, or publish. |

## 6. Source Boundary
P-02 through P-06 contain product-specific dependency risks. P-08 controls Git posture. M-06, W-03, W-13, and V-05 control external-source metadata and validation posture. W-12 and V-04 control product posture.

Raw `2_products/` and `4_external/sources/` are not deeply inspected. P-09 uses safe metadata only.

## 7. External Source Inventory Posture
| Source | Current posture | Product relevance | Allowed use | Blocked use | Future route |
| --- | --- | --- | --- | --- | --- |
| `acpx` | External evidence only; local-only; not adopted; execution/dependency/instruction blocked. | Protocol/adapter evidence. | Adapter-boundary metadata. | Active bridge, auth, protocol dependency. | Adapter/protocol review. |
| `ai-cookbook-main` | External evidence only; local-only; not adopted; execution/dependency/instruction blocked. | Example/documentation evidence. | Example taxonomy metadata. | Running examples or provider calls. | Example review. |
| `clawhub` | External evidence only; local-only; not adopted; execution/dependency/instruction blocked. | Registry/catalog evidence. | Trust-pattern metadata. | Trusted registry or package source. | Registry trust review. |
| `ECC-main` | External evidence only; local-only; not adopted; execution/dependency/instruction blocked. | Harness evidence. | Harness-pattern metadata. | Runtime/governance authority. | Harness review. |
| `EnergyPlusV24-2-0` | External evidence only; local-only; not adopted; execution/dependency/instruction blocked. | Backend/domain solver evidence. | Product/domain blocker metadata. | Solver execution or product dependency. | Product/domain review. |
| `graphify` | External evidence only; local-only; not adopted; execution/dependency/instruction blocked. | Substrate/projection evidence. | Substrate-neutral metadata. | Naming authority or graph truth. | CSS substrate evaluation. |
| `hermes-agent` | External evidence only; local-only; not adopted; execution/dependency/instruction blocked. | Harness risk evidence. | Self-improvement risk metadata. | Self-modification adoption. | Governance safety review. |
| `openclaw` | External evidence only; local-only; not adopted; execution/dependency/instruction blocked. | Gateway/skill evidence. | Gateway boundary metadata. | Active gateway or auth path. | Gateway/skill review. |
| `opencode` | External evidence only; local-only; not adopted; execution/dependency/instruction blocked. | Agent/session evidence. | Context/tool metadata. | Workspace execution policy. | Agent context review. |
| `openstudio` | External evidence only; local-only; not adopted; execution/dependency/instruction blocked. | Backend/domain SDK evidence. | Product/domain blocker metadata. | Root SDK or product integration. | Product/domain review. |
| `pi` | External evidence only; local-only; not adopted; execution/dependency/instruction blocked. | Harness/provider evidence. | Harness/provider metadata. | Active harness or provider config. | Harness provider review. |
| `tau` | External evidence only; local-only; not adopted; execution/dependency/instruction blocked. | Harness/instruction evidence. | Instruction/license metadata. | Active instructions or source reuse. | Instruction/license review. |

## 8. Product Dependency Candidate Table
| Product | Candidate dependency classes | Current posture | Major risks | Future route | Blocked inference |
| --- | --- | --- | --- | --- | --- |
| `omniverse-app` | Omniverse Kit, OpenUSD, Nucleus, NVIDIA SDK/name-use, GPU/runtime/drivers, visualization/output stack. | Candidate only; blocked. | SDK/runtime/license/GPU/auth/output. | Dependency/license/runtime/security review. | Kit, SDK, or runtime approval. |
| `backend-energyplus` | EnergyPlus, OpenStudio, Python packages, native solver/runtime, weather/data formats, result parsers. | Candidate only; blocked. | Native solver, license/name-use, input/output, data. | Solver/license/runtime/security review. | Engine adoption or backend behavior. |
| `cli` | CLI runtime/language, parser, shell boundary, package manager, backend API/SDK client. | Candidate only; blocked. | Command/shell/package/user data. | Command-safety/dependency review. | CLI works or shell is approved. |
| `desktop` | Desktop framework/runtime, installer/updater/signing, local DB/cache, OS permissions, backend API/SDK client. | Candidate only; blocked. | Packaging/local data/update/permissions. | Desktop runtime/packaging review. | Desktop runtime or installer approval. |
| `web-platform` | Web framework/runtime, build tooling, auth/session, hosting/CDN/domain/TLS, analytics/telemetry, backend API client. | Candidate only; blocked. | Auth/build/deploy/provider/data. | Web dependency/auth/deploy review. | Web runtime or deploy approval. |
| `experimental` | Unknown dependencies pending classification/split/archive review. | Unknown; blocked/local-only. | Ambiguous source, leakage, unknown dependency posture. | Split/classification/security review. | Prototype dependency approval. |

## 9. Dependency Class Catalog
| Class | Meaning | Allowed planning use | Blocked use | Required future evidence |
| --- | --- | --- | --- | --- |
| `physical_solver_dependency` | Solver/engine such as EnergyPlus. | Domain risk framing. | Run/adopt as model. | Provenance, license, native runtime, IO/security. |
| `domain_sdk_dependency` | SDK/tooling such as OpenStudio. | Product-domain evidence. | SDK integration. | License, package/native graph, scope. |
| `visualization_runtime_dependency` | Omniverse/Kit/GPU runtime. | Interface risk framing. | Launch/install. | SDK license, runtime, GPU, security. |
| `geometry_semantic_format_dependency` | OpenUSD-style representation. | Binding/representation planning. | Source of truth or heavy time-series store. | Format governance and data limits. |
| `collaboration_asset_dependency` | Nucleus/assets/collaboration services. | Collaboration risk framing. | Auth/network/storage use. | Auth, provider, data, retention review. |
| `language_runtime_dependency` | Python/Node/Rust/Go/.NET runtimes. | Stack candidate only. | Runtime adoption. | Version/source/security/rollback. |
| `package_manager_dependency` | pip/npm/yarn/pnpm/poetry/uv/conan. | Supply-chain risk framing. | Install/audit/build. | Registry, scripts, lock, transitive graph. |
| `native_binary_dependency` | Binaries, DLLs, drivers, installers. | Native-risk evidence. | Execute/install. | Binary provenance, sandbox, side effects. |
| `web_framework_dependency` | React/Vue/Svelte/Next/Vite/etc. | Web stack candidate. | Dev server/build/deploy. | Package/license/build/security. |
| `desktop_framework_dependency` | Electron/Tauri/Qt/PySide/native. | Desktop stack candidate. | Runtime/installer/updater. | Package/native/signing/OS review. |
| `cli_framework_dependency` | Parser/command/runtime libs. | Command UX candidate. | Command execution. | Command safety, packages, output policy. |
| `hosting_deployment_dependency` | CDN/domain/TLS/email/hosting. | Deployment risk framing. | Deploy/publication. | Provider, terms, auth, privacy. |
| `auth_identity_dependency` | OAuth/session/cookie/identity. | Auth risk framing. | Login/session use. | Credential, privacy, retention, threat review. |
| `provider_api_dependency` | Provider/API/cloud/model endpoints. | Provider boundary evidence. | Calls/auth/network. | Endpoint, terms, data, auth, cost. |
| `MCP_tool_dependency` | MCP server/tool/resource dependency. | MCP boundary candidate. | Activation. | Server, tools, access, network/auth review. |
| `dataset_model_artifact_dependency` | Datasets/models/artifacts. | Data/model risk framing. | Use/train/publish. | Provenance, license, sensitivity, storage. |
| `unknown_experimental_dependency` | Unclassified prototype dependency. | Blocker metadata. | Inference/adoption. | Classification, owner, scope, security. |

## 10. Per-product Posture: omniverse-app
Omniverse Kit, OpenUSD, Nucleus, GPU, NVIDIA SDK, and name-use are candidates only. No SDK, runtime, license, or name-use approval exists. No Kit launch, extension install, Nucleus/auth, GPU/runtime use, or package installation occurs.

OpenUSD is geometry/semantic representation, not heavy time-series storage. Generated visual outputs remain sensitive. Future route: dependency/license/runtime/security review before implementation readiness.

## 11. Per-product Posture: backend-energyplus
EnergyPlus and OpenStudio are domain/solver evidence only. EnergyPlus is solver, not internal model. IDF and epJSON remain generated artifacts, not source of truth.

No EnergyPlus, OpenStudio, native binary, Python package, weather/data dependency, or result parser is adopted. No solver is run. Future route: solver/license/runtime/input-output/security review.

## 12. Per-product Posture: cli
CLI language, runtime, parser, package, shell, and backend client dependencies are candidates only. Shell availability is not command approval. CLI consumes governed backend contracts only.

No shell, command, package manager, backend call, or CLI runtime is activated. Future route: command-safety/dependency/security review.

## 13. Per-product Posture: desktop
Electron, Tauri, Qt, PySide, .NET, and native desktop stacks are candidates only. Installer, updater, signing, local cache, local DB, and OS permission dependencies remain unresolved.

No desktop runtime, local daemon, installer, updater, package manager, or framework is adopted. Future route: desktop runtime/packaging/security review.

## 14. Per-product Posture: web-platform
React, Vue, Svelte, Next, Vite, Node, Python, web build, auth, hosting, analytics, and monitoring stacks are candidates only. Hosting, CDN, domain, TLS, email, auth, analytics, monitoring, and deployment providers remain unapproved.

No dev server, build, package manager, deploy, auth, or hosting provider is activated. Future route: web dependency/auth/deploy/security review.

## 15. Per-product Posture: experimental
Dependency posture is unknown. `experimental` remains blocked/local-only. No dependency inference is allowed from prototype proximity.

No source inspection, split, archive, dependency adoption, or tracking occurs. Future route: split/classification/security review before any dependency discussion.

## 16. License / Notice / Name-use Rules
License evidence is not reuse approval. Missing license or notice posture blocks adoption. NVIDIA, Omniverse, OpenUSD, Nucleus, EnergyPlus, OpenStudio, and name-use claims require future review.

Package licenses, binary licenses, model/data licenses, and hosting terms require future review. P-09 performs no legal or license approval.

## 17. Runtime / Native / Package Execution Rules
Runtime availability is not execution approval. Native binaries, package scripts, build tools, installers, updaters, package managers, solver execution, dev servers, daemons, tests, and builds are blocked unless future exact approval exists.

P-09 runs none of them.

## 18. Provider / API / Network / Auth / MCP Rules
Provider/API/network/auth use is blocked. OAuth values, API keys, cookies, sessions, tokens, and credentials are excluded. Provider credentials are not provider permission. MCP availability is not MCP activation. Tool availability is not permission.

Remote services, telemetry, update checks, registries, hosting, analytics, and cloud calls require future governance.

## 19. Data / Generated Output / Artifact Rules
Dependency-generated outputs are generated-sensitive. Build outputs, solver outputs, logs, reports, screenshots, datasets, models, caches, lockfiles, package caches, downloaded binaries, and deployment bundles are blocked by default.

Generated output is evidence, not source by default. Publication requires product, security, validation, and governance review.

## 20. Git Relationship
P-08 remains in force: product governance docs remain trackable as docs only and product source remains local-only. Product Git posture is not changed by P-09.

Dependency manifests from unapproved source are not adoption approval. Lockfiles are not dependency adoption approval. Vendor folders are blocked. `.gitignore` remains unchanged. No staging, commit, push, force-add, or publication occurs.

## 21. Dependency Review Gate
Future dependency gates require: product owner, product scope, dependency name, dependency class, exact version/source, upstream provenance, license/notice/name-use, security posture, runtime/execution posture, package scripts/build scripts, transitive dependency posture, network/auth/provider/MCP behavior, data/output behavior, Git/include-exclude posture, validation plan, rollback/removal plan, and governance decision.

P-09 does not pass this gate.

## 22. External Source Review Gate
Future external-source gates require: source name, source class, source relevance, whether content is required, whether reuse is requested, whether instructions are active, whether execution is requested, provenance/license/security, dependency relationship, product relationship, substrate/naming relationship, validation evidence, and governance decision.

P-09 does not pass this gate.

## 23. Product Dependency Matrix
| Product | Dependency posture | Source posture | License posture | Runtime posture | Network/auth posture | Git posture | Activation blocker |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `omniverse-app` | Omniverse/OpenUSD/Nucleus candidates blocked. | External evidence only. | NVIDIA/name-use unreviewed. | Kit/GPU blocked. | Nucleus/auth blocked. | P-08 local-only source. | SDK/runtime/security. |
| `backend-energyplus` | EnergyPlus/OpenStudio candidates blocked. | Domain evidence only. | Domain/name-use unreviewed. | Native solver blocked. | Provider/API blocked. | P-08 local-only source. | Solver/license/data. |
| `cli` | Runtime/parser/package candidates blocked. | External/package evidence only. | Package licenses unreviewed. | Shell/CLI blocked. | Backend/API blocked. | P-08 local-only source. | Command safety. |
| `desktop` | Framework/installer candidates blocked. | External/package evidence only. | Package/signing unreviewed. | Desktop runtime blocked. | Update/API blocked. | P-08 local-only source. | Packaging/security. |
| `web-platform` | Web/build/auth candidates blocked. | External/package evidence only. | Package/hosting terms unreviewed. | Dev server/build blocked. | Auth/deploy blocked. | P-08 local-only source. | Auth/deploy/data. |
| `experimental` | Unknown; blocked. | Safe metadata only. | Unknown. | Unknown; blocked. | Unknown; blocked. | P-08 local-only source. | Classification/scope. |

## 24. Validation Posture
Using V-04, V-05, V-02, and V-01: PL-1 applies to source/path/status metadata; PL-2 to dependency/source class and local-only posture; PL-3 to provenance/license reference review; PL-4 to dependency/source coherence review; PL-5 only to future exact metadata checks; PL-6 only to future explicitly approved tests/execution; PL-7 to future product workspace audit; PL-8 only to reproduced audit.

Validation does not approve adoption, execution, installation, source reuse, product activation, Git tracking, publication, or implementation.

## 25. Security / Local-only Posture
S-series rules apply. Secrets and credentials are never retained. Unknown sensitivity blocks use. Local-only means no default publication. Product/external raw content is excluded.

Dependency review must account for local paths, auth, environment variables, package registries, telemetry, generated outputs, and sensitive building data.

## 26. Blocker Register
| Blocker | Stop behavior | Required future action | Blocks dependency adoption? | Blocks product activation? |
| --- | --- | --- | --- | --- |
| Missing P-08 | Stop Git/source claim. | Restore Git posture decision. | Yes | Yes |
| Missing M-06/W-13/V-05 | Stop external claim. | Restore external posture inputs. | Yes | Yes |
| Missing product charter | Stop product dependency claim. | Draft/accept charter later. | Yes | Yes |
| Product owner missing | Stop adoption path. | Assign owner. | Yes | Yes |
| Dependency name/version/source unknown | Stop dependency framing. | Exact dependency record. | Yes | Yes |
| License/notice unknown | Stop reuse/adoption. | License/notice/name-use review. | Yes | Yes |
| Provenance unknown | Stop trust claim. | Upstream/source/version review. | Yes | Yes |
| Transitive dependency unknown | Stop package adoption. | Dependency graph review. | Yes | Yes |
| Package scripts unknown | Stop install/build path. | Script/build review. | Yes | Yes |
| Native/runtime risk | Stop execution. | Runtime/security review. | Yes | Yes |
| Network/auth/provider risk | Stop activation. | Provider/security review. | Yes | Yes |
| MCP/tool risk | Stop MCP/tool use. | MCP/tool review. | Yes | Yes |
| Generated-output risk | Stop publication/use. | Output review. | Maybe | Yes |
| Data/privacy risk | Stop data use. | Data/security/privacy review. | Yes | Yes |
| Source reuse implied | Stop reuse claim. | Exact reuse governance. | Yes | Yes |
| External instruction implied | Stop instruction use. | Mark inactive/review pattern. | Maybe | Maybe |
| Dependency adoption implied | Stop wording/action. | Dependency governance. | Yes | Yes |
| Execution/install implied | Stop action. | Exact future approval. | Yes | Yes |
| Git tracking implied | Stop Git path. | Future Git governance. | Maybe | Yes |
| Product activation implied | Stop. | Product activation governance. | Yes | Yes |
| P-10 scope pressure detected | Stop adjacent work. | Wait explicit P-10 instruction. | No | No |

## 27. Incident Handling
Incidents include package install attempted; solver/native/web/desktop/CLI/runtime executed; external source inspected deeply; source code copied; license text copied as approval; dependency adopted by wording; provider/API/MCP activated; credentials exposed; product source staged; dependency folder staged; `.gitignore` modified; product activated by dependency posture; or P-10 started.

Response: STOP, report safe metadata only, do not continue adjacent work, and require human/security/governance decision.

## 28. P-09 Invariants
| ID | Invariant |
| --- | --- |
| P09-001 | Product dependency posture is not dependency adoption. |
| P09-002 | External source posture is not source adoption. |
| P09-003 | Dependency relevance is not trust. |
| P09-004 | License evidence is not reuse approval. |
| P09-005 | Runtime availability is not execution approval. |
| P09-006 | Package manifest is not dependency approval. |
| P09-007 | Provider credentials are not provider permission. |
| P09-008 | MCP availability is not MCP activation. |
| P09-009 | Product source remains local-only. |
| P09-010 | Product Git posture is not changed. |
| P09-011 | Product validation baseline is not created. |
| P09-012 | Product activation remains blocked. |
| P09-013 | Graph remains a candidate only. |
| P09-014 | Validation evaluates; governance decides. |
| P09-015 | P-09 stops before P-10. |

## 29. Anti-patterns
Anti-patterns: dependency posture as adoption; external source as dependency; license as approval; package manifest as adoption; lockfile as approval; package install by curiosity; solver run by curiosity; source inspection by curiosity; dependency relevance as product activation; external instruction as active policy; provider/API/MCP activation by need; product source tracking by dependency need; generated outputs as source; graph/source relevance as substrate decision; starting P-10 inside P-09; `git add .`.

## 30. Readiness For P-10
P-10 - Product Validation Baseline is ready after explicit instruction if P-09 dependency/external posture exists, dependency and external candidates remain unadopted, product source remains local-only, product Git posture remains unchanged, and no package install, execution, provider/API/MCP activation, publication, product activation, or implementation is implied.

Do not create P-10.

## 31. Final Verdict
| Question | Answer |
| --- | --- |
| What does P-09 decide? | Product dependencies and external sources are candidates or evidence only; all adoption is blocked pending future exact review. |
| Did P-09 adopt dependencies? | No. |
| Did P-09 adopt external sources? | No. |
| Did P-09 install or execute anything? | No. |
| Did P-09 inspect product or external source deeply? | No. |
| Did P-09 activate products? | No. |
| Did P-09 change Git posture? | No. |
| Did P-09 create validation baselines? | No. |
| What remains blocked? | Dependency adoption, external source adoption, source reuse, installs, execution, providers/API/network/auth/MCP, product activation, source tracking, publication, validation baselines, implementation, staging, commit, push, and P-10. |
| Is P-10 ready after explicit instruction? | Yes, as Product Validation Baseline only; P-10 is not started. |

Stop after P-09 validation and report. Do not start P-10 or any later ticket.
