# IR-04 - Package / SDK / Dependency Readiness
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Package / SDK / Dependency Readiness |
| Ticket | IR-04 |
| Status | Accepted package / SDK / dependency readiness assessment |
| Date | 2026-07-02 |
| Scope | Readiness assessment for future packages, SDKs, dependencies, runtimes, native binaries, registries, manifests, lockfiles, and supply-chain controls for AGENT PLATFORM / Siamese after IR-03. |
| Authority | Readiness assessment only, not package installation, dependency adoption, source tracking, execution, product activation, or implementation. |
| Related documents | IR-00, IR-01, IR-02, IR-03, P-A, P-00 through P-10, M-A, M-06, W-series, V-series, S-series, CSS-series, H-series, `.gitignore`, `README.md`, Siamese Product Vision |
| Assessment target | Future package / SDK / dependency posture |

## 2. Purpose
IR-00 found the platform not ready for implementation but ready for planning tickets. IR-01 reserved `3_platform` conceptually only. IR-02 blocked source tracking except named readiness governance documents. IR-03 blocked scripts/tools/tests creation and execution.

IR-04 assesses package, SDK, dependency, manifest, lockfile, runtime, registry, supply-chain, license, and native binary readiness. It does not install packages, adopt dependencies, create manifests or lockfiles, run package managers, inspect product or external source trees deeply, approve source tracking, activate products, execute solvers or SDKs, or start IR-05.

## 3. Readiness Definition
Package / SDK / dependency readiness is a governance assessment of dependency classes, risks, evidence needs, and gates required before future dependency adoption or execution.

Readiness is not adoption. A candidate package is not approved. A discovered manifest is not authoritative. A lockfile is not approval. A runtime on the machine is not execution approval. A package manager command is not safe by default. An SDK reference is not integration approval. A license indication is not reuse approval.

## 4. Decision Summary
No package is installed. No dependency is adopted. No SDK is adopted. No native binary is approved. No package manager is run. No manifest or lockfile is created. No dependency folder is tracked. No provider, API, MCP, network, auth, solver, dev server, build, or test execution is approved.

All package, SDK, dependency, and runtime items remain candidate-only or blocked evidence. Future adoption requires exact dependency scope, source/provenance, license, security, supply-chain, execution, validation, rollback, Git, and governance approval.

## 5. Authority Boundary
| Layer | IR-04 boundary |
| --- | --- |
| Governance | Decides dependency adoption, manifests, lockfiles, registries, execution, exceptions, publication, source tracking, and implementation. |
| Validation | Evaluates dependency evidence and future results; it does not approve adoption. |
| Security | Constrains secrets, credentials, local-only content, package scripts, native binaries, network, auth, providers, APIs, MCP, generated outputs, and publication. |
| IR-04 | Assesses package / SDK / dependency readiness only. |
| Git | Records artifacts but does not approve dependency status. |
| Agents | May prepare safe readiness metadata but cannot install, run, adopt, authenticate, create manifests/lockfiles, stage, commit, push, publish, or start IR-05. |

## 6. Source Boundary
IR-02 controls source tracking. IR-03 controls scripts/tools/tests readiness. P-09 controls product dependency and external-source posture. P-10 controls validation baseline posture. M-06, W-03, W-13, and V-05 control external source metadata. S-series controls execution/security/local-only posture. H-series controls runtime, tool, provider, and MCP boundaries. CSS-series controls Cognitive Semantic System naming and substrate neutrality.

Raw `3_platform`, `2_products/`, `4_external/sources/`, `previusknowledge/`, datasets, models, artifacts, secrets, and credentials are not inspected or approved by IR-04.

## 7. Current Readiness Posture
| Area | Current posture | Status | Blocked now | Future route |
| --- | --- | --- | --- | --- |
| Packages | Candidate-only. | blocked_not_adopted | Install/adopt/track. | Dependency adoption gate. |
| SDKs | Candidate-only. | blocked_not_adopted | Integrate/execute. | SDK gate. |
| Native binaries | Evidence-only. | blocked_not_executed | Install/run/load. | Native binary gate. |
| Package managers | Not approved for execution. | blocked_not_executed | `pip`, `npm`, `pnpm`, `yarn`, `poetry`, `uv`, `cargo`, `conan`, installers. | Package manager gate. |
| Manifests | Not approved for creation/tracking. | blocked_not_created | Create or treat as source. | Manifest gate. |
| Lockfiles | Not approved for creation/tracking. | blocked_not_created | Generate, update, track. | Lockfile gate. |
| Registries | No trusted registry approved. | blocked_not_adopted | Pull/publish. | Registry trust gate. |
| Source tracking | IR docs only. | blocked_for_source | Stage dependency source. | IR-02 future gate. |
| Execution | No install/build/test/solver/dev-server. | blocked_not_executed | Any dependency execution. | Execution gate. |

## 8. Dependency Class Catalog
| Class | Meaning | Planning use | Blocked use | Required future evidence |
| --- | --- | --- | --- | --- |
| language_runtime_dependency | Python, Node, Rust, Go, .NET, Java, or shell runtime. | Stack comparison. | Runtime adoption/execution. | Version, provenance, support, security, rollback. |
| package_manager_dependency | Tool that resolves/downloads/builds packages. | Supply-chain risk framing. | Install/audit/build/update. | Registry, scripts, lock policy, cache/output policy. |
| application_package_dependency | Library/framework package. | Candidate design input. | Import/use/track. | License, provenance, transitive graph, maintenance. |
| domain_solver_dependency | EnergyPlus-style solver/engine. | Domain capability framing. | Run/adopt as internal model. | License, native runtime, input/output, sandbox. |
| domain_sdk_dependency | OpenStudio-style domain SDK. | Integration risk framing. | SDK integration/execution. | License, package/native graph, API boundaries. |
| visualization_runtime_dependency | Omniverse Kit/GPU/rendering stack. | Interface risk framing. | Launch/install/integrate. | SDK terms, drivers, auth, output policy. |
| geometry_format_dependency | OpenUSD-style representation. | Representation planning. | Source of truth or heavy time-series store. | Data limits, versioning, conversion rules. |
| desktop_runtime_dependency | Electron/Tauri/Qt/PySide/native shell. | Desktop risk framing. | Runtime/installer/updater. | Package, signing, OS permissions, local data. |
| web_runtime_dependency | Framework/build/deploy stack. | Web risk framing. | Dev server/build/deploy. | Package graph, auth, hosting, privacy. |
| cli_dependency | Parser/shell/terminal dependency. | CLI risk framing. | Shell command execution. | Command safety, output policy, user data handling. |
| provider_api_dependency | Cloud/API/model/service endpoint. | Boundary planning. | Network calls/auth. | Terms, endpoint, data, cost, auth, retention. |
| MCP_tool_dependency | MCP server/tool/resource. | Interface candidate. | Activation. | Server scope, tools, resources, network/auth review. |
| dataset_model_artifact_dependency | Dataset, model, generated artifact. | Risk framing. | Use/train/publish/track. | Provenance, sensitivity, license, storage. |
| unknown_experimental_dependency | Unclassified prototype dependency. | Blocker metadata. | Adoption/inference. | Classification, owner, purpose, security. |

## 9. Product Dependency Matrix
| Product route | Candidate dependency classes | Current posture | Primary blockers | Future route |
| --- | --- | --- | --- | --- |
| `omniverse-app` | Visualization runtime, geometry format, collaboration assets, GPU/drivers, SDK/name-use. | Candidate only. | SDK terms, native runtime, auth, GPU, generated visuals. | Product dependency/license/runtime/security review. |
| `backend-energyplus` | Domain solver, domain SDK, Python packages, weather/data formats, parsers. | Candidate only. | Native solver, license, IO, data, generated outputs. | Solver/SDK/license/runtime/security review. |
| `cli` | Language runtime, CLI parser, shell boundary, package manager, backend API client. | Candidate only. | Command execution, package scripts, user data. | Command-safety/dependency review. |
| `desktop` | Desktop runtime, installer/updater/signing, local DB/cache, backend API client. | Candidate only. | Packaging, OS permissions, local data, updates. | Desktop runtime/packaging review. |
| `web-platform` | Web framework, build tooling, auth/session, hosting/CDN/domain/TLS, analytics. | Candidate only. | Build/dev server, deploy, auth, provider/data risk. | Web dependency/auth/deploy review. |
| `experimental` | Unknown prototype dependencies. | Blocked local-only. | Unclassified source and dependency posture. | Split/classification/security review. |

## 10. External Source Dependency Posture
External source records remain metadata-only. External source names may inform risk patterns, but no source code, setup instruction, package manifest, dependency graph, provider config, runtime, or license text from raw external source trees is adopted.

The external source inventory remains local-only evidence. It cannot become a package source, registry trust source, SDK authority, implementation source, product dependency, or Cognitive Semantic System substrate decision without future exact review.

## 11. Package Manager Posture
Package managers are blocked for execution. This includes install, add, update, audit, resolve, lock, build, publish, script, cache priming, environment creation, and post-install actions.

Future approval must name the manager, version, command, working directory, registry, network posture, script policy, lockfile policy, output/cache paths, rollback, and allowed evidence.

## 12. Manifest Posture
No `package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`, `.csproj`, `conanfile`, installer config, extension manifest, or equivalent manifest is created or approved by IR-04.

Any future manifest must have exact path, owner, product/platform scope, dependency purpose, license/provenance review, script review, source tracking gate, and removal plan before tracking.

## 13. Lockfile Posture
No lockfile is generated, modified, or approved. Lockfiles are not harmless metadata because they can encode registry, transitive dependency, platform, checksum, and supply-chain state.

Future lockfile approval must declare generator, platform, registry, update cadence, review process, checksum policy, reproducibility expectation, and rollback path.

## 14. Registry And Source Trust Posture
No registry is trusted. Public package registries, vendor feeds, container registries, plugin marketplaces, extension catalogs, MCP indexes, Git URLs, local folders, and external source snapshots remain untrusted until reviewed.

Future registry approval must cover namespace ownership, typosquat risk, package provenance, maintainer risk, malicious script risk, transport/auth, mirroring/cache policy, allowed scopes, and publication prohibition or approval.

## 15. SDK And Runtime Posture
SDKs and runtimes remain candidate-only. Omniverse Kit, OpenUSD tooling, EnergyPlus, OpenStudio, language runtimes, desktop runtimes, web runtimes, CLI runtimes, provider SDKs, and MCP servers are not adopted or executed.

Future SDK approval must separate interface use from backend authority, document version and license, define permitted APIs, restrict generated outputs, and pass security and validation gates.

## 16. Native Binary Posture
Native binaries, installers, DLLs, drivers, GPU tooling, solver executables, shell tools, and platform-specific packages are blocked for install and execution.

Future native approval must include provenance, checksum/signature, license, sandbox, side effects, filesystem/network behavior, output paths, uninstallation, and incident response.

## 17. Transitive Dependency Posture
Transitive dependencies are not approved by approving a top-level candidate. Dependency graphs, optional dependencies, peer dependencies, build dependencies, post-install dependencies, native extensions, and plugin discovery remain blocked evidence.

Future review must include full graph capture, license aggregation, vulnerability posture, maintainer health, update risk, reproducibility, and generated-output handling.

## 18. License And Notice Posture
License indications are evidence only. They do not approve copying, reuse, package adoption, binary execution, name-use, redistribution, publication, product branding, or generated-output distribution.

Future license approval must include license text source, compatibility, attribution/notice duties, redistribution limits, SDK/vendor terms, trademark/name-use, data terms, and product-specific obligations.

## 19. Supply-Chain Security Posture
Supply-chain risk is unresolved. Risks include typosquatting, dependency confusion, compromised maintainers, malicious scripts, native payloads, binary downloads, poisoned caches, unpinned versions, unreviewed transitive graphs, and hidden network/auth flows.

Future supply-chain approval must define pinned versions, hashes where applicable, registry allowlist, script policy, vulnerability review, update process, provenance evidence, and removal/rollback plan.

## 20. Execution And Build Posture
No install, build, test, dev server, solver run, SDK launch, package script, codegen, migration, container, or automation command is approved by IR-04.

Execution remains blocked until exact command, directory, inputs, outputs, environment, network/auth, secrets handling, cleanup, and validation/security owner are approved.

## 21. Provider / API / MCP / Network / Auth Posture
Provider SDKs, APIs, MCP servers, network calls, credentials, login flows, OAuth/session flows, telemetry, analytics, hosting, deployment, and publication are not activated.

Future activation requires endpoint scope, data classification, credential storage, least privilege, retention, cost, terms, audit trail, revocation, network boundary, and explicit governance.

## 22. Data / Model / Artifact Dependency Posture
Datasets, models, generated artifacts, caches, build outputs, solver outputs, logs, screenshots, USD files, IDF/epJSON, and reports are not dependencies, source, or tracked implementation material by default.

Future use requires provenance, sensitivity, license, retention, storage, reproducibility, generated-output classification, and publication review.

## 23. Cognitive Semantic System Posture
The Cognitive Semantic System remains the canonical AGENT PLATFORM cognitive/semantic system name. Its substrate is undecided. Graph is a candidate substrate or projection pattern only, not truth authority.

No package, graph library, database, vector store, ontology engine, external source, or projection tool is adopted as the Cognitive Semantic System substrate by IR-04.

## 24. Product Vision Alignment
Siamese product routes may require rich interfaces, simulation backends, CLI workflows, desktop packaging, and web platform services, but product need does not override readiness gates.

Product interfaces consume governed backend contracts only. EnergyPlus remains a solver, not the internal model. Omniverse Kit remains an interface candidate, not the backend or authority.

## 25. Source Tracking And Git Posture
IR-04 creates only this governance document. Source tracking remains blocked for `3_platform`, product source, external source, dependency folders, manifests, lockfiles, scripts, tools, tests, runtime source, providers, adapters, MCP, validation registry, security enforcement, and generated outputs.

Git staging, commit, push, force-add, publication, and `.gitignore` changes are not authorized by IR-04.

## 26. Package / SDK / Dependency Gate
Before any dependency adoption: exact dependency name, class, purpose, owner, consumer, path, version policy, registry/source, license, provenance, transitive graph, security posture, execution needs, outputs, validation plan, rollback plan, Git posture, and human governance approval must exist.

IR-04 does not pass this gate.

## 27. Manifest / Lockfile Gate
Before any manifest or lockfile creation/tracking: exact path, source-tree approval, package manager approval, dependency list, script policy, registry policy, lock strategy, generated-output policy, review owner, removal plan, and human governance approval must exist.

IR-04 does not pass this gate.

## 28. SDK / Native / Solver Gate
Before any SDK, native binary, or solver use: license/vendor terms, platform/runtime requirements, provenance, checksum/signature where applicable, sandbox, command/API surface, input/output policy, generated artifacts, security owner, validation baseline, and rollback must exist.

IR-04 does not pass this gate.

## 29. Provider / API / MCP Gate
Before any provider, API, MCP, network, or auth activation: endpoint/server scope, tool/resource list, credentials handling, data classification, network policy, retention, cost, terms, audit logging, revocation, test plan, and governance approval must exist.

IR-04 does not pass this gate.

## 30. Validation Requirements
Future dependency validation must be evidence-first and non-authorizing. It should evaluate declared dependency scope, package graph, license/provenance, supply-chain risk, security posture, execution outputs, generated files, and rollback evidence.

Validation evaluates; governance decides. Passing validation does not automatically approve adoption, tracking, execution, provider activation, or implementation.

## 31. Security Requirements
Future dependency work must preserve local-only boundaries, exclude secrets and credentials, block unapproved network/auth, prevent package script surprises, control generated outputs, and avoid publishing unreviewed source or artifacts.

Any secret exposure, credential request, unexpected network need, native binary ambiguity, package script ambiguity, or local-only boundary violation must stop the work for security review.

## 32. Risks And Blockers
Primary blockers: no source tree approval, no dependency adoption approval, no package manager approval, no manifest/lockfile policy approval, no trusted registry, no license aggregation, no supply-chain review, no native runtime review, no provider/API/MCP activation, no validation/security enforcement implementation, and no implementation readiness approval.

These blockers prevent implementation, not governance planning.

## 33. Anti-Patterns
Do not treat candidate dependency lists as adoption. Do not run installs to learn the graph. Do not create manifests as placeholders. Do not track lockfiles before source approval. Do not trust raw external source package files. Do not infer approval from ignored or existing files. Do not use product urgency to bypass license/security/supply-chain gates. Do not activate providers, APIs, MCP, network, auth, solvers, SDKs, dev servers, builds, or tests under dependency-readiness scope.

Do not rename the Cognitive Semantic System based on a candidate substrate. Do not treat graph tooling as semantic truth.

## 34. IR-05 Readiness
IR-05 may proceed only after explicit human instruction and only as the next bounded readiness/planning assessment. IR-05 must inherit IR-04 blockers: no dependency adoption, no package manager execution, no manifests/lockfiles, no source tracking, no runtime/provider/API/MCP activation, no product activation, and no implementation.

IR-04 does not start IR-05.

## 35. Final Verdict
IR-04 is complete as a readiness assessment. AGENT PLATFORM / Siamese package, SDK, dependency, runtime, manifest, lockfile, registry, license, supply-chain, and native binary posture is documented but not approved for adoption or execution.

The platform remains not implementation-ready. Future implementation remains blocked until later exact governance passes dependency gates, source tracking gates, validation/security gates, runtime/provider gates, and implementation readiness approval.
