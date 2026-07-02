# G-05 - Graphify Dependency Adoption Gate

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Graphify Dependency Adoption Gate |
| Ticket | G-05 |
| Status | Accepted Graphify dependency adoption gate |
| Date | 2026-07-02 |
| Scope | Exact local tool dependency installation gate for Graphify availability for AGENT PLATFORM / Siamese. |
| Authority | Exact local tool dependency installation gate only, not Graphify execution. |
| Related documents | G-00, G-01, G-02, G-03, G-04, I-A, I-06, I-07, S-series, CSS-series, `.gitignore`, README.md |
| Decision target | Install `graphifyy` only if needed, then verify CLI availability. |

## 2. Purpose
G-04 found Graphify unavailable: no PATH entry, no runnable version command, and no `graphifyy` package metadata.

G-05 determines whether to install `graphifyy` as a local tool dependency for future repo-map evidence. G-05 allows one exact install command: `python -m pip install graphifyy`.

G-05 does not run Graphify against any repo path. G-05 does not install OpenCode integration. G-05 does not create outputs. G-05 does not start the safe run.

## 3. Current Graphify Status Before G-05
| G-04 observation | Status before G-05 |
| --- | --- |
| `graphify` on PATH | Not found. |
| `graphify --version` | Not runnable. |
| `graphifyy` package | Not installed in checked Python environment. |
| Availability classification | `unavailable`. |
| Safe run | Blocked. |

## 4. Dependency Adoption Gate Definition
A bounded dependency adoption gate is an exact-scope decision allowing a named package to be installed for a named purpose, with command, environment, evidence, rollback, limitations, and non-goals recorded.

Graphify dependency adoption gate is not Graphify execution. Package installation is not Graphify authority. Package installation is not Cognitive Semantic System substrate selection. Package installation is not source tracking approval. Package installation is not OpenCode integration. Package installation is not project dependency manifest adoption. Package installation is not product activation.

graphifyy installation is local tool availability, not Graphify authority.

## 5. Authority Boundary
| Layer | G-05 boundary |
| --- | --- |
| Governance | Authorizes the exact installation command only. |
| Security | Constrains package-manager behavior, network/auth, local environment mutation, generated outputs, and secrets. |
| Validation | Records install evidence and CLI availability as evidence only. |
| Git | May record only this G-05 document after human approval. |
| AI agents | Cannot approve broader dependency adoption, execution, provider activation, source tracking, or G-06. |

## 6. Exact Installation Scope
| Item | G-05 scope |
| --- | --- |
| Allowed package | `graphifyy` |
| Allowed install command | `python -m pip install graphifyy` |
| Allowed purpose | Make `graphify` CLI available for a future G-06 safe-root repo-map run. |
| Actual result | Installed and CLI available. |

Explicitly not included: project manifest dependency, lockfile, production dependency, runtime dependency, OpenCode integration, Graphify source adoption, Graphify as authority, Graphify output creation, repo scan, or Cognitive Semantic System substrate selection.

## 7. Allowed Command Set
| Command | Purpose | Expected output | Allowed failure | Forbidden inference |
| --- | --- | --- | --- | --- |
| `git status --short` | Pre-install Git posture. | Short status or no output. | Unexpected status is reportable. | Git output is not staging approval. |
| `python -m pip show graphifyy` before install | Determine if install is needed. | Package metadata or not found. | Not found means install may proceed. | Absence is not broad install approval. |
| `python -m pip install graphifyy` | One exact local tool install. | Successful install or failure. | Auth/privilege/private index requirement blocks. | Install is not run approval. |
| `python -m pip show graphifyy` after install | Record package metadata. | Name, version, summary, location, dependencies, license. | Missing metadata after success is ambiguous. | Metadata is not authority. |
| `where.exe graphify` | Verify CLI entry point on PATH. | Executable path or not found. | Not found gives CLI-unavailable result. | PATH presence is not repo scan approval. |
| `graphify --version` | Verify CLI can run version query. | Version text. | Failure blocks safe run. | Version query is not path execution. |
| Path checks | Confirm expected/no forbidden artifact paths. | Boolean results. | Unexpected true/false is evidence. | Path checks are not content inspection. |
| Target checks | Confirm required G-05 boundary text. | Match results. | Missing match blocks acceptance. | Text matches are not execution approval. |

## 8. Forbidden Command Set
Forbidden commands and command families: `pip install graphifyy`; `pip install graphify`; `python -m pip install graphify`; `python -m pip install --upgrade graphifyy`; `python -m pip uninstall graphifyy`; `pip freeze`; `pip list`; package index/search/download/wheel commands; `graphify .`; `/graphify .`; `graphify .\0_architecture`; `graphify .\3_platform\_governed_skeleton`; `graphify install`; `graphify opencode install`; `graphify --watch`; MCP, hooks, Neo4j push, URL ingestion, OpenCode install, project install, and root scan commands.

No `--upgrade`, `--force-reinstall`, or `--user` was used.

## 9. Installation Result Model
| Status | Meaning | Consequence |
| --- | --- | --- |
| `install_success_cli_available` | Package installed and CLI version works. | Recommend G-06 — Graphify Safe Run. |
| `install_success_cli_unavailable` | Package installed but CLI not found or not runnable. | Recommend G-06 Graphify Entry Point Resolution Gate. |
| `install_failed` | Install command failed. | Recommend G-06 Graphify Install Failure Review. |
| `install_blocked_auth_or_privilege` | Auth, private credentials, or elevated privileges required. | Stop and require security/governance review. |
| `install_blocked_network_or_registry` | Registry/network posture blocked. | Stop and require dependency/security review. |
| `install_ambiguous` | Result cannot be classified safely. | Stop and require review. |
| `package_already_available_before_install` | Package was already available before install. | Record and verify CLI. |

Actual G-05 status: `install_success_cli_available`.

## 10. Dependency Posture Model
Because installation succeeded, Graphify becomes a local tool dependency candidate for the checked environment only.

It is not added to AGENT PLATFORM project dependencies. It is not added to any manifest. It is not pinned. It is not locked. It is not a production dependency. It is not a product dependency. It is not a Cognitive Semantic System dependency.

Future reproducible adoption requires a separate package, version, registry, lock, license, security, and rollback strategy.

## 11. Version / Metadata Evidence
| Metadata field | Safe summary |
| --- | --- |
| Package name | `graphifyy` |
| Installed version | `0.9.5` |
| Summary | AI coding assistant skill that turns folders of code, docs, papers, images, or videos into a queryable knowledge graph. |
| Location | Checked Python environment under local Anaconda `Lib/site-packages`; exact local path not needed for authority. |
| License field | `MIT License` |
| Required-by | None listed. |
| Dependencies | `networkx`, `numpy`, `rapidfuzz`, `tree-sitter`, and tree-sitter language packages for bash, C, C#, C++, Elixir, Fortran, Go, Groovy, Java, JavaScript, JSON, Julia, Kotlin, Lua, ObjC, PHP, PowerShell, Python, Ruby, Rust, Scala, Swift, TypeScript, Verilog, and Zig. |

Install side effect: `networkx` was changed from `3.3` to `3.6.1` by the approved install command's dependency resolution. This is a local environment mutation, not AGENT PLATFORM project dependency adoption.

## 12. CLI Availability Evidence
| Check | Result |
| --- | --- |
| `where.exe graphify` | Found `graphify.exe` in the local Anaconda Scripts directory. |
| `graphify --version` | `graphify 0.9.5` |
| CLI posture | Available for future exact approval only. |

If CLI had been unavailable, G-05 would not attempt alternate execution paths without a future gate.

## 13. OpenCode Integration Boundary
No `graphify opencode install`. No `/graphify` slash-command execution. No assistant config mutation. No `AGENTS.md`. No `.agents/`, `.claude/`, or `.codex/`. No always-on Graphify behavior. No hooks, watch mode, or MCP.

OpenCode integration remains a separate future gate.

## 14. Graphify Execution Boundary
Graphify is not run against any path by G-05.

No repo-map run, safe-root scan, repo-root scan, product scan, external scan, Hermes scan, Graphify source scan, existing `3_platform` sibling scan, graph output, or graph cache is created by G-05.

Graphify repo map is not CSS substrate. CSS in this sentence means Cognitive Semantic System.

## 15. Output Boundary
G-05 creates no Graphify repo-map outputs.

No `graphify-out/`. No `graph.html`. No `GRAPH_REPORT.md`. No `graph.json`. No cache. Command stdout/stderr may be summarized as safe metadata in this document. Generated outputs remain future G-06/G-07 scope.

## 16. Security Boundary
Package installation may contact the public package registry. The observed install downloaded package metadata and wheels and did not require private registry credentials, authentication prompts, elevated privileges, or non-standard package index configuration.

No secrets or credentials are inspected. No `.env` is inspected. No provider configs are inspected. No local-only source is scanned. No product or external source is scanned. Existing `3_platform` siblings are not inspected.

If install had requested elevated permissions or private auth, G-05 would have stopped.

## 17. Rollback Boundary
G-05 records rollback strategy but does not uninstall unless explicitly instructed by future incident handling.

Candidate rollback command for future explicit approval:

```powershell
python -m pip uninstall graphifyy
```

Do not run uninstall in G-05 by default. If installation had partially failed, G-05 would record safe metadata and stop.

## 18. Relation To Cognitive Semantic System
Graphify installation is not Cognitive Semantic System substrate selection. Graphify CLI availability is not graph adoption. Graphify remains evidence only, not authority. Cognitive Semantic System substrate remains deferred.

Future Graphify output, if any, remains generated evidence only. Validation evaluates; governance decides.

## 19. Relation To Future Graphify Safe Run
G-05 may make G-06 possible because the CLI is available. G-05 does not authorize G-06 execution.

G-06 must still use the G-03 safe-root strategy. G-06 must not use repo-root scan. G-06 must not install OpenCode integration. G-06 must not scan product, external, secrets, or existing `3_platform` sibling contents.

## 20. Created / Not Created Register
| Artifact/action | G-05 status | Reason |
| --- | --- | --- |
| Dependency adoption gate document | Created | Required G-05 target artifact. |
| Exact install command | Run because needed | `graphifyy` was absent before install. |
| Graphify package metadata | Checked | Pre- and post-install metadata evidence. |
| Graphify CLI availability | Checked | PATH and version evidence. |
| Graphify repo-map | Not run | Execution not authorized. |
| Outputs | Not created | Output creation blocked. |
| Cache | Not created | Repo-map not run. |
| Safe mirror | Not created | Copying files blocked. |
| OpenCode integration | Not installed | Assistant config mutation blocked. |
| `AGENTS.md` | Not created | Integration blocked. |
| Hooks/watch/MCP | Not created | Runtime/tool behavior blocked. |
| Project manifests/lockfiles | Not created | Project dependency adoption blocked. |
| Source tracking | Not expanded | Git gate required. |
| G-06 | Not started | Explicit instruction required. |

## 21. Command Evidence Register
| Command | Result category | Key observation | Safe inference | Forbidden inference |
| --- | --- | --- | --- | --- |
| Pre-install `python -m pip show graphifyy` | Not installed | `Package(s) not found: graphifyy`. | Install was needed. | Absence approved no other package command. |
| `python -m pip install graphifyy` | Install succeeded | Installed `graphifyy 0.9.5` and transitive dependencies; `networkx` changed from `3.3` to `3.6.1`. | Local tool availability dependency now present. | Install does not approve repo scan or authority. |
| Post-install `python -m pip show graphifyy` | Metadata present | Name `graphifyy`, version `0.9.5`, MIT license, dependencies listed. | Package metadata available in checked environment. | Metadata is not project manifest adoption. |
| `where.exe graphify` | CLI found | `graphify.exe` found in local Anaconda Scripts directory. | CLI entry point exists on PATH. | PATH presence is not execution approval. |
| `graphify --version` | CLI runnable | `graphify 0.9.5`. | CLI and package are available. | Version query is not a repo-map run. |

## 22. Residual Risk Register
| Risk | Current handling |
| --- | --- |
| Installed version is not pinned | Future package/lock strategy required. |
| Installed dependency set may change in future | Reproducible adoption deferred. |
| Local environment may differ from other machines | Availability applies only to checked environment. |
| Package provenance/license review is limited to available metadata | Future deeper dependency review required for broader adoption. |
| Future run still requires execution gate | G-06 must approve exact command and paths. |
| Future output may be sensitive | Generated-sensitive/local-only by default. |
| No curated summary yet | Future curation gate required. |
| No workstream dependency map yet | Future dependency-map gate required. |

## 23. Blocker Register
| Blocker | Current G-05 status |
| --- | --- |
| Install failed | Not current; install succeeded. |
| CLI unavailable after install | Not current; CLI available. |
| Package metadata missing | Not current; metadata present. |
| Private registry/auth required | Not observed. |
| Elevated permissions required | Not observed. |
| Dependency review insufficient for production | Still blocked. |
| Need safe run | Still blocked; future G-06 required. |
| Need output directory | Still blocked; future output approval required. |
| Need output curation | Still blocked. |
| Need OpenCode integration | Still blocked. |
| Need repo-root scan | Blocked and not recommended. |
| Need raw output tracking | Blocked. |
| Need CSS substrate decision | Blocked/deferred. |
| Need Graphify adoption | Blocked; Graphify remains evidence only. |

## 24. Incident Handling
Incidents include command outside allowed set run; install prompts for credentials; install uses private registry unexpectedly; install mutates repo files; package manifest or lockfile created; Graphify repo-map run during G-05; Graphify output created; OpenCode integration installed; `AGENTS.md` or assistant config created; hooks/watch/MCP activated; product/external/secrets scanned; existing `3_platform` sibling inspected; Graphify adopted as authority; CSS substrate selected; Git mutation attempted; G-06 started.

Response: STOP, report safe metadata only, require governance/security decision.

No G-05 incident is recorded. The `networkx` environment change is a dependency-resolution side effect of the single approved install command and is recorded as residual dependency risk.

## 25. G-05 Invariants
| ID | Invariant |
| --- | --- |
| G05-001 | Graphify dependency adoption gate is not Graphify execution. |
| G05-002 | graphifyy installation is local tool availability, not Graphify authority. |
| G05-003 | Package installation is not CSS substrate selection. |
| G05-004 | Package installation is not graph adoption. |
| G05-005 | Package installation is not OpenCode integration. |
| G05-006 | Graphify is not run against any path by G-05. |
| G05-007 | Graphify output is not created by G-05. |
| G05-008 | OpenCode Graphify integration is not installed. |
| G05-009 | Project package manifests and lockfiles are not created. |
| G05-010 | Existing 3_platform siblings remain uninspected and unapproved. |
| G05-011 | Product source remains local-only. |
| G05-012 | External sources remain local-only. |
| G05-013 | Hermes is not inspected or adopted. |
| G05-014 | Graphify remains evidence only, not authority. |
| G05-015 | Cognitive Semantic System substrate remains deferred. |
| G05-016 | No broad source tracking is approved. |
| G05-017 | Validation evaluates; governance decides. |
| G05-018 | G-05 stops before G-06. |

## 26. Anti-patterns
Anti-patterns: package install as repo-map execution permission; installed CLI as architecture authority; dependency availability as graph adoption; Graphify usefulness as Graphify adoption; package installation as project dependency manifest adoption; install and run combined by convenience; OpenCode install by convenience; generated output consumed without curation; raw graph committed; existing `3_platform` as approved source; `git add .`; starting G-06 inside G-05.

Rejected/prohibited/historical examples only: `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth`. No such string is accepted as a current AGENT PLATFORM or Cognitive Semantic System name.

## 27. Next Ticket Recommendation
Conditional next ticket:

| Result | Recommendation |
| --- | --- |
| `install_success_cli_available` | G-06 — Graphify Safe Run. |
| `install_success_cli_unavailable` | G-06 — Graphify Entry Point Resolution Gate. |
| `install_failed` | G-06 — Graphify Install Failure Review. |
| `install_blocked_auth_or_privilege` | G-06 — Graphify Security / Environment Review. |
| Dependency adoption rejected | Defer Graphify and proceed with non-Graphify repo map strategy. |

Actual recommendation: G-06 — Graphify Safe Run, after explicit instruction only.

G-05 does not start G-06.

## 28. Final Verdict
| Question | Answer |
| --- | --- |
| Was `graphifyy` installed? | Yes, `graphifyy 0.9.5` was installed with the one approved command. |
| Is Graphify CLI available? | Yes, `graphify --version` returns `graphify 0.9.5`. |
| What version/package metadata was observed? | Name `graphifyy`, version `0.9.5`, MIT license field, dependencies summarized above. |
| Was Graphify run against any path? | No. |
| Was OpenCode integration installed? | No. |
| Were outputs created? | No. |
| Were manifests/lockfiles created? | No. |
| Was Graphify adopted as authority? | No. |
| Was CSS substrate selected? | No; Cognitive Semantic System substrate remains deferred. |
| What is the dependency posture? | Local tool dependency candidate in the checked environment only; not project, product, production, locked, pinned, or CSS dependency. |
| What remains blocked? | Graphify repo-map execution, safe-root scan, repo-root scan, OpenCode integration, outputs/cache, safe mirror, source tracking expansion, product/external/secrets/3_platform sibling inspection, Hermes adoption, Graphify authority, final CSS substrate, staging, commit, push, publication, and G-06. |
| What is the recommended next ticket? | G-06 — Graphify Safe Run, only after explicit instruction. |
