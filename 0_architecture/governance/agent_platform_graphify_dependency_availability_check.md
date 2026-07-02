# G-04 - Graphify Dependency / Availability Check

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Graphify Dependency / Availability Check |
| Ticket | G-04 |
| Status | Accepted availability check; Graphify unavailable in current environment |
| Date | 2026-07-02 |
| Scope | Check whether Graphify is already available without installation, adoption, repository scanning, output creation, or OpenCode integration. |
| Authority | Governance/availability evidence only; not execution approval, dependency adoption, or Cognitive Semantic System substrate selection. |
| Related documents | G-00, G-01, G-02, G-03, I-A, I-06, I-07, S-series, CSS-series, `.gitignore`, README.md |
| Decision target | Current local Graphify CLI/package availability posture |

## 2. Purpose
G-04 answers one narrow question: is Graphify already available in this local environment without installing or adopting anything?

G-04 does not run Graphify against any path. G-04 does not install Graphify or `graphifyy`. G-04 does not create graph outputs, cache, safe mirror, assistant config, package manifests, lockfiles, tests, scripts, CI, or source-tracking changes.

## 3. Availability Result
| Surface | Result |
| --- | --- |
| CLI discovery | `graphify` was not found on PATH. |
| CLI version command | `graphify --version` was not executable because `graphify` is not recognized. |
| Python package metadata | `graphifyy` was not installed for the checked Python environment. |
| Fallback check | `py -m pip show graphifyy` was not run because `python -m pip show graphifyy` executed successfully as a metadata query. |
| Availability classification | `unavailable` |
| Run eligibility | Not eligible; no Graphify run can proceed from G-04. |

## 4. Command Evidence
The following commands were the only availability commands run for G-04.

| Command | Safe result | Interpretation |
| --- | --- | --- |
| `git status --short` | No output. | Pre-file-creation repository status check returned no short-status entries. |
| `where.exe graphify` | `INFORMACION: no se pudo encontrar ningun archivo para los patrones dados.` | No `graphify` executable was found on PATH. |
| `graphify --version` | PowerShell reported that `graphify` was not recognized as a cmdlet, function, script file, or executable program. | CLI is not runnable. |
| `python -m pip show graphifyy` | `WARNING: Package(s) not found: graphifyy` | Package metadata is absent in the checked Python environment. |

These failures are availability evidence, not incidents. They do not authorize install, dependency adoption, package-manager resolution, or alternate discovery commands.

## 5. Classification Logic
| Condition | Observed? |
| --- | --- |
| CLI path found | No |
| CLI version available | No |
| `graphifyy` package metadata found | No |
| Python unavailable | No |
| Ambiguous package/CLI mismatch | No |
| Install required to proceed | Yes, but install is not approved by G-04. |

Classification: `unavailable`.

Rationale: both the executable surface and the package metadata surface are absent. No evidence supports `available_cli_only`, `available_package_only`, or `available_cli_and_package`.

## 6. Gate Record
| Field | G-04 value |
| --- | --- |
| gate_id | `G-04-GRAPHIFY-DEPENDENCY-AVAILABILITY-CHECK` |
| gate_type | GT-07 Tool Execution Gate evidence with GT-03 Dependency Adoption Gate dependency if future install is requested. |
| title | Graphify local dependency and CLI availability check. |
| owner | Future human/governance owner required before any install, run, or adoption. |
| requester | Current G-04 record only. |
| target_paths | This governance file only. No Graphify input paths are authorized. |
| excluded_paths | Repo root as Graphify input; `2_products/`; `4_external/sources/`; `previusknowledge/`; `7_datasets/`; `8_models/`; `9_artifacts/` except future approved output; `.git/`; `.env*`; secrets; credentials; provider configs; dependency folders; runtime caches; existing `3_platform` siblings; product source; external source; Hermes source; Graphify source. |
| activation_level_from | AL-1 |
| activation_level_to | AL-1; no promotion. |
| current_status | Graphify unavailable. |
| requested_status | Availability check complete; execution remains blocked. |
| source_posture | Internal governance metadata only. |
| git_posture | Exact-path review only for this G-04 file after human approval; no generated outputs trackable by default. |
| dependency_posture | No dependency adopted. `graphifyy` not installed in checked environment. |
| validation_posture | Availability command evidence only; no repo-map validation. |
| security_posture | No secrets, credentials, product source, external source, provider auth, network, MCP, or OpenCode integration used. |
| product_posture | No product activation. Siamese remains product vision context only. |
| external_source_posture | Graphify and Hermes source remain uninspected and unadopted. |
| CSS_substrate_impact | None; Cognitive Semantic System substrate remains deferred. |
| evidence_refs | G-00 through G-03, I-A, I-06, I-07, S-series, CSS-series. |
| proof_level_target | Safe local availability evidence only. |
| limitations | Checks cover the current PATH and checked Python environment only; they do not prove registry availability, alternate environments, or future install safety. |
| blockers | Graphify unavailable; no owner; no dependency review; no install approval; no run approval; no output handling approval. |
| rollback_plan | No runtime or dependency mutation occurred. If this file is rejected, remove only this file under exact human approval. |
| stop_rules | Stop on install pressure, package-manager resolution, broad scan, Graphify run, OpenCode integration, generated output creation, source inspection, or G-05 drift. |
| validation_commands_allowed | G-04 availability commands only; no Graphify path scan. |
| incident_response | STOP, preserve safe metadata, report breached surface, require governance/security decision. |
| decision_status | Accepted availability check; unavailable result. |
| decision_authority | Governance/human authority required for any future dependency or execution action. |
| created_at | 2026-07-02 |
| review_required | Future dependency/license/security review if install is requested; future execution gate if run is requested. |

## 7. Dependency Boundary
`graphifyy` is the package name fact. `graphify` is the CLI command fact. Neither fact is dependency adoption.

G-04 did not install, upgrade, uninstall, sync, lock, freeze, list, search, index, download, or wheel any package. G-04 did not create or modify package manifests or lockfiles.

If a future ticket needs Graphify, it must use a separate dependency adoption gate that addresses package source, version, license, provenance, transitive dependencies, scripts, network behavior, rollback, and security review.

## 8. Execution Boundary
G-04 did not execute Graphify against any repository path.

No safe-root scan was run for `0_architecture/`. No safe-root scan was run for `3_platform/_governed_skeleton/`. No repo-root scan was run. No product, external source, Hermes, Graphify source, secrets, credentials, existing `3_platform` siblings, or generated artifact paths were scanned.

Because Graphify is unavailable, the G-03 future candidate run strategy remains blocked.

## 9. Output Boundary
G-04 created no Graphify outputs.

| Output/artifact | G-04 status |
| --- | --- |
| `graph.html` | Not created |
| `GRAPH_REPORT.md` | Not created |
| `graph.json` | Not created |
| Graphify cache | Not created |
| `graphify-out/` | Not created by G-04 |
| Safe mirror | Not created |
| Curated Graphify summary | Not created |
| Workstream dependency map | Not created |

Any future generated output remains local-only/generated-sensitive by default and not trackable unless an exact Git/source-tracking gate approves it.

## 10. OpenCode Boundary
G-04 did not install or configure Graphify for OpenCode.

No `graphify opencode install`, slash-command execution, assistant-rule mutation, `AGENTS.md`, `.agents/`, `.claude/`, `.codex/`, hooks, watch mode, MCP serving, project install, or always-on assistant behavior was approved or created.

OpenCode support remains a capability fact only, not permission.

## 11. Cognitive Semantic System Boundary
Cognitive Semantic System remains the accepted name. Graph remains a candidate representation only. Graphify remains evidence only, not authority.

G-04 does not choose graph, vector, relational, document, ontology, event-sourced, memory-only, hybrid, or any other final substrate. Availability evidence cannot select or bias the final Cognitive Semantic System substrate.

Validation evaluates; governance decides.

## 12. Relation To G-03
G-03 defined a future safe execution plan. G-04 checked local availability before any run.

G-04 result blocks the G-03 future run path because the tool is unavailable. This does not convert G-04 into a dependency approval ticket. The next decision, if any, must choose between stopping, opening a dependency adoption gate, or deferring Graphify entirely.

## 13. Created / Not Created Register
| Artifact/action | G-04 status | Reason |
| --- | --- | --- |
| G-04 governance file | Created | Required target artifact. |
| Availability commands | Run | Exact allowed commands only. |
| Graphify install | Not run | Dependency adoption blocked. |
| Graphify execution | Not run | Tool unavailable and execution not approved. |
| Graphify output | Not created | Output creation blocked. |
| Safe mirror | Not created | Copying files blocked. |
| OpenCode integration | Not installed | Assistant config mutation blocked. |
| Package manifests/lockfiles | Not created | Dependency posture unchanged. |
| Source tracking expansion | Not approved | Git gate required. |
| G-05 | Not started | Explicit instruction required after G-04. |

## 14. Residual Risks
| Risk | Current handling |
| --- | --- |
| Alternate Python environment could contain `graphifyy` | Not assumed; current checked environment is the only evidence. |
| Future install may introduce supply-chain risk | Requires GT-03 dependency gate. |
| Future run may scan too broadly | Requires exact G-03-style execution approval and exclusions. |
| Generated output may be over-trusted | Evidence-only posture retained. |
| OpenCode integration may mutate instructions | Remains blocked. |
| CSS substrate pressure may recur | Substrate remains deferred. |

## 15. Blocker Register
Blockers: Graphify unavailable; no dependency owner; no package/version/license/security review; no install approval; no exact run approval; no output directory approval; no generated artifact retention approval; no OpenCode integration approval; no source classification for broader paths; no source tracking approval; no Cognitive Semantic System substrate decision.

## 16. Stop Rules
Stop immediately if the work requires installing Graphify, adopting `graphifyy`, using package-manager resolution, running Graphify against any path, scanning repo root, scanning product/external/secrets/existing `3_platform` siblings, creating graph outputs, creating assistant config, creating hooks/watch/MCP behavior, modifying `.gitignore`, staging/committing/pushing, or starting G-05.

Response to stop condition: preserve safe metadata only, state the blocked action, and require exact governance/security/human approval.

## 17. G-04 Invariants
| ID | Invariant |
| --- | --- |
| G04-001 | Availability is not permission. |
| G04-002 | CLI discovery is not tool execution approval. |
| G04-003 | Package presence would not be dependency adoption; package absence is not install approval. |
| G04-004 | Graphify is unavailable in the checked environment. |
| G04-005 | Graphify is not run by G-04. |
| G04-006 | Graphify is not installed by G-04. |
| G04-007 | Graphify output is not created by G-04. |
| G04-008 | OpenCode Graphify integration is not installed. |
| G04-009 | Existing `3_platform` siblings remain uninspected and unapproved. |
| G04-010 | Product source and external source remain out of scope. |
| G04-011 | Hermes remains uninspected and unadopted. |
| G04-012 | Cognitive Semantic System substrate remains deferred. |
| G04-013 | Validation evaluates; governance decides. |
| G04-014 | G-04 stops before G-05. |

## 18. Anti-patterns
Anti-patterns: treating failed availability as install approval; treating package metadata as adoption; treating CLI presence as run approval; treating G-03 candidate commands as approved by G-04; using availability checks to justify broad repo scans; creating outputs before output handling approval; installing OpenCode integration by convenience; committing raw generated graph artifacts; treating Graphify output as truth; treating graph as final substrate; starting G-05 inside G-04.

Rejected/prohibited/historical examples only: `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth`. No such string is accepted as a current AGENT PLATFORM or Cognitive Semantic System name.

## 19. Final Verdict
| Question | Answer |
| --- | --- |
| Is Graphify available on PATH? | No. |
| Is `graphify --version` runnable? | No. |
| Is `graphifyy` installed in the checked Python environment? | No. |
| What is the availability classification? | `unavailable`. |
| Does G-04 install or adopt Graphify? | No. |
| Does G-04 run Graphify against any path? | No. |
| Does G-04 create outputs or cache? | No. |
| Does G-04 approve OpenCode integration? | No. |
| Does G-04 select Cognitive Semantic System substrate? | No. |
| What remains blocked? | Install, dependency adoption, Graphify execution, repo-map scans, generated outputs, OpenCode integration, source tracking expansion, product/external/secrets/3_platform sibling inspection, Graphify adoption, Hermes adoption, CSS substrate selection, staging, commit, push, publication, and G-05. |
