# G-02 - Graphify Read-only Repo Map Gate

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Graphify Read-only Repo Map Gate |
| Ticket | G-02 |
| Status | Accepted governance/tool-use gate; execution blocked until future exact approval |
| Date | 2026-07-02 |
| Scope | Define the only acceptable future path for a bounded, read-only Graphify repository map evidence run for AGENT PLATFORM. |
| Authority | Governance and tool-use gate only; not Graphify execution, installation, adoption, integration, dependency approval, source tracking approval, or Cognitive Semantic System substrate selection. |
| Related documents | G-00, G-01, I-A, I-00 through I-07, IR-A, W-10, W-13, S-03, S-04, CSS-series, `.gitignore`, README.md |
| Decision target | Future read-only Graphify repo-map evidence gate |

## 2. Purpose
G-02 defines how a future Graphify-assisted repository map could be considered without turning Graphify into authority, runtime, dependency, source tracker, OpenCode configuration, or Cognitive Semantic System substrate.

G-02 exists because Graphify may be useful as a graph-oriented semantic projection tool, but its usefulness also creates risks: installation pressure, generated-truth confusion, broad repo scanning, generated artifacts, cache output, assistant-rule mutation, hooks, watch mode, MCP serving, dependency adoption, and graph lock-in.

G-02 does not run Graphify. It does not install Graphify. It does not inspect Graphify source. It does not create outputs. It does not approve G-03.

## 3. Current Posture
| Area | Current posture after G-02 |
| --- | --- |
| Activation ceiling | AL-1 metadata skeleton remains the ceiling. |
| Graphify | Evidence candidate only; not adopted, installed, run, integrated, or authoritative. |
| Graph | Candidate representation only; not selected as final substrate. |
| Cognitive Semantic System | Accepted name; final substrate remains deferred. |
| Tool execution | Blocked except exact future command approval through gates. |
| Dependency posture | No Graphify or `graphifyy` dependency adopted. |
| OpenCode integration | Not approved; no assistant config, rules, or slash-command setup. |
| Generated outputs | None created by G-02. Future outputs are local-only/generated-sensitive by default. |
| Source tracking | Not expanded. Only this G-02 file may be considered for exact-path review after human approval. |
| Existing `3_platform` siblings | Still uninspected and unapproved. |
| Product/external/secrets | Product source, external source code, secrets, credentials, and local-only material remain out of scope. |

## 4. Decision Summary
G-02 accepts a gate model for a possible future read-only repo-map evidence run using Graphify. It does not approve the run.

A future Graphify repo-map request must be a one-time, exact-scope, local-only, no-install, no-integration, no-watch, no-hook, no-MCP, no-provider, no-auth, no-product, no-external-source, no-secret, no-broad-scan action unless separate gates explicitly approve every exception.

The future output, if ever approved, is evidence only. It cannot decide truth, governance, source tracking, activation level, implementation direction, product activation, dependency adoption, or Cognitive Semantic System substrate.

## 5. Graphify Factual Posture
| Fact | G-02 handling |
| --- | --- |
| Graphify is an open-source knowledge graph skill for AI coding assistants that builds queryable graphs from code, docs, papers, and diagrams. | Useful as candidate evidence only. |
| Official package name is `graphifyy`; CLI command remains `graphify`. | Package/CLI fact only; not dependency approval or command approval. |
| Standard outputs include `graph.html`, `GRAPH_REPORT.md`, `graph.json`, and cache output. | Generated-sensitive/local-only if ever produced; not trackable by default. |
| Graphify supports OpenCode. | OpenCode integration is specifically not approved by G-02. |
| OpenCode integration may write `AGENTS.md` or assistant rules. | Prohibited for G-02 and for any future read-only repo map unless separately approved. |
| Graphify can be used with hooks, watch mode, MCP serving, project install, Neo4j/export modes, or always-on assistant integration. | Out of scope and blocked. |

## 6. Gate Record
| Field | G-02 value |
| --- | --- |
| gate_id | `G-02-GRAPHIFY-READ-ONLY-REPO-MAP` |
| gate_type | GT-07 Tool Execution Gate with GT-03, GT-04, GT-11, GT-12, GT-13, and GT-15 dependencies as needed. |
| title | Future Graphify read-only repo-map evidence gate. |
| owner | Future human/governance owner required before any execution. |
| requester | Current G-02 record only; future execution requester must be named. |
| target_paths | Current target is this governance file only. Future scan paths must be exact and separately approved. |
| excluded_paths | Product source, external source code, secrets, credentials, datasets, models, artifacts except approved output path, `.git`, dependency folders, caches, existing `3_platform` siblings, and local-only material. |
| activation_level_from | AL-1. |
| activation_level_to | AL-1; no promotion. |
| current_status | Gate defined; Graphify execution blocked. |
| requested_status | Future candidate may request exact read-only evidence run. |
| source_posture | Internal governance metadata only. Raw Graphify source remains external/local-only/uninspected. |
| git_posture | Exact-path review only for this document; generated outputs and caches are not trackable by default. |
| dependency_posture | None adopted. `graphifyy` remains unapproved. |
| validation_posture | G-02 file validation only; Graphify validation execution is future gated work. |
| security_posture | No secrets, credentials, provider auth, network, MCP, product, external source, or local-only inspection. |
| product_posture | No product activation or product source inspection. Siamese remains product vision context only. |
| external_source_posture | Graphify evidence only; external source code not inspected. |
| CSS_substrate_impact | None; Cognitive Semantic System substrate remains deferred. |
| evidence_refs | G-00, G-01, I-00 through I-07, I-A, S-03, S-04, W-10, W-13, CSS-series. |
| proof_level_target | Governance consistency only for G-02; future run must name proof target. |
| limitations | No Graphify output, no dependency review, no command execution, no source classification beyond allowed metadata. |
| blockers | No owner, no exact future command, no dependency/security/license review, no output handling decision, no source classification for broad scan. |
| rollback_plan | For G-02, remove only this document if rejected by governance. For future run, delete/quarantine outputs and caches under exact paths. |
| stop_rules | Stop on install/run pressure, broad scan, assistant config mutation, generated artifact tracking, secret/local-only risk, or next-ticket drift. |
| validation_commands_allowed | G-02 document checks only; no Graphify commands. |
| incident_response | STOP, preserve safe metadata, report breached surface, require governance/security decision. |
| decision_status | Accepted gate model; execution not approved. |
| decision_authority | Governance/human authority required for any future run. |
| created_at | 2026-07-02. |
| review_required | Future validation, security, dependency/license, source classification, and Git posture review before execution. |

## 7. Current Allowed Actions
| Action | Allowed by G-02? | Boundary |
| --- | --- | --- |
| Create this governance file | Yes | Exact target only. |
| Read allowed governance/security/implementation inputs | Yes | Bounded docs only. |
| Check target path and safe path existence metadata | Yes | No content inspection of forbidden areas. |
| Validate line count, character count, and bounded text posture | Yes | G-02 file only or explicitly allowed docs. |
| Run Graphify | No | Future exact gate required. |
| Install Graphify or `graphifyy` | No | Dependency gate required. |
| Configure Graphify for OpenCode | No | Assistant config mutation blocked. |
| Create generated graph outputs or caches | No | Future output gate required. |
| Start G-03 | No | Explicit instruction required. |

## 8. Prohibited Actions
| Prohibited action | Reason |
| --- | --- |
| Run `/graphify` | Slash-command execution/integration not approved. |
| Run `graphify` | CLI execution not approved. |
| Run `graphify install` | Install/config mutation not approved. |
| Run `graphify opencode install` | OpenCode assistant-rule mutation not approved. |
| Install package `graphifyy` | Dependency adoption and package execution not approved. |
| Create `AGENTS.md`, `.agents/`, `.claude/`, or `.codex/` | Assistant instruction/config mutation not approved. |
| Create hooks, watch mode, MCP server, or always-on integration | Runtime/tool/provider/MCP activation blocked. |
| Create `graphify-out/`, cache, `graph.html`, `GRAPH_REPORT.md`, or `graph.json` | Generated artifacts not approved by G-02. |
| Inspect Graphify source or Hermes source | External source code inspection not in scope. |
| Inspect product source, secrets, credentials, `.env`, provider configs, or local credential stores | Local-only/security boundaries. |
| Inspect existing `3_platform` sibling contents | Source classification gate required. |
| Modify `.gitignore`, package manifests, lockfiles, scripts, tests, CI, OpenCode config, or README.md | Out of G-02 scope. |
| Stage, commit, push, force-add, publish, or use `git add .` | Human/Git gate required. |

## 9. Future Read-only Repo-map Candidate Scope
If a future ticket requests Graphify execution, the request must define exact include and exclude paths before any command is considered.

Candidate include scope may be no broader than reviewed canonical architecture/control documents and the approved governed skeleton subroot. Existing `3_platform` siblings are not included by parent-folder proximity.

Candidate exclusions must include at minimum: `2_products/`, `4_external/sources/`, `7_datasets/`, `8_models/`, prior corpus, `.git/`, `.env*`, secrets, credentials, provider configs, dependency folders, runtime caches, generated outputs, local Office/OS files, and any unknown-sensitivity path.

Read-only means source inputs are not mutated. It does not mean no outputs exist. Any generated outputs, reports, HTML, JSON, caches, exports, or temporary files must have exact local-only output paths, cleanup rules, and Git exclusion posture before execution.

## 10. Future Execution Preconditions
| Precondition | Required before any Graphify command |
| --- | --- |
| Human owner | Named accountable owner and rollback owner. |
| Exact command | Full command, cwd, arguments, input paths, output paths, environment, expected outputs, and stop rule. |
| Dependency posture | `graphifyy` package/source/version/provenance/license/security/dependency review or approved already-available tool posture. |
| No install by default | If Graphify is unavailable, stop; do not install as part of repo-map execution unless a dependency gate approves it. |
| No OpenCode integration | Future repo map must not write assistant rules, slash commands, config, hooks, or agent files. |
| Source classification | Exact include/exclude paths classified for sensitivity and source posture. |
| Secret/local-only protection | Confirm command cannot read secret/credential/local-only excluded paths. |
| Output handling | Exact output directory, generated-sensitive label, retention, cleanup, and no-default-Git posture. |
| Network/auth posture | No provider, API, network, registry, MCP, or credential use unless separately approved. |
| Validation plan | How outputs are checked as evidence without treating them as truth. |
| Rollback | Delete/quarantine outputs and caches; record incident if unexpected mutation occurs. |

## 11. Future Output Rules
| Output type | Future handling |
| --- | --- |
| `graph.html` | Generated-sensitive evidence; not source, not truth, not trackable by default. |
| `GRAPH_REPORT.md` | Generated report evidence; must cite generator, inputs, date, and limitations if reviewed. |
| `graph.json` | Generated machine projection; local-only until reviewed. |
| Cache output | Local-only/cache; cleanup or quarantine required. |
| Any extra export | Blocked unless exact output path and purpose are approved before execution. |

Graphify outputs may be stale immediately after source changes. A graph edge, node, cluster, report paragraph, or query result is a projection, not a governance decision or validated semantic truth.

## 12. OpenCode Integration Boundary
G-02 does not authorize any OpenCode integration. Graphify support for OpenCode is a capability fact, not permission.

Future repo mapping must not use assistant integration if the goal is read-only evidence. Assistant integration can write instructions or rules, change agent behavior, create persistent command surfaces, or blur evidence with authority.

Any future OpenCode/Graphify integration would require separate gates for assistant config mutation, instruction risk, tool execution, dependency adoption, generated output handling, rollback, and human approval.

## 13. Cognitive Semantic System Boundary
Cognitive Semantic System is the accepted name. Graph remains a candidate representation only. Graphify remains evidence only, not authority.

G-02 does not choose graph, vector, relational, document, ontology, event-sourced, memory-only, hybrid, or any other final substrate. G-02 does not create graph runtime, vector runtime, database, ontology, persistence, reasoning engine, semantic truth store, or substrate migration.

Any future Graphify evidence may support CSS substrate evaluation only after validation, security, dependency, provenance, and governance review. Validation evaluates; governance decides.

## 14. Source Tracking And Git Boundary
G-02 does not approve source tracking expansion. It does not modify `.gitignore`. It does not stage, commit, push, force-add, publish, or approve broad source tracking.

Only `0_architecture/governance/agent_platform_graphify_read_only_repo_map_gate.md` may be considered for exact-path Git review after explicit human approval.

Future Graphify outputs, caches, generated reports, and HTML/JSON artifacts are local-only/generated-sensitive by default. They must not be staged or force-added unless a future Git/source tracking gate names exact paths and rationale.

## 15. Bounded Metadata Observations
| Surface | G-02 handling |
| --- | --- |
| `3_platform/_governed_skeleton/` | Approved implementation subroot exists from I-series; not expanded by G-02. |
| Existing `3_platform` siblings | Uninspected and unapproved. |
| `4_external/sources/graphify` | External snapshot path may exist as metadata; source not inspected. |
| `4_external/sources/hermes-agent` | External snapshot path may exist as metadata; source not inspected. |
| `9_artifacts/` | Local-only generated artifact area; no G-02 output created. |
| `graphify-out/` | Must not be created by G-02. |
| `AGENTS.md`, `.agents/`, `.claude/`, `.codex/` | Must not be created by G-02. |

These observations are safe metadata only. They do not approve content inspection, reuse, execution, integration, generated outputs, or source tracking.

## 16. Validation Model
G-02 validation may check only this document and bounded safe metadata. No Graphify validation command is allowed by G-02.

Allowed G-02 validation classes: target path existence, line count, character count, bounded text search for required/prohibited posture, optional safe path existence checks, and read-only Git status for reporting.

Passing validation does not approve Graphify execution, dependency adoption, source tracking, generated output tracking, G-03, or any activation-level promotion.

## 17. Created / Not Created Register
| Artifact/action | G-02 status | Reason |
| --- | --- | --- |
| G-02 governance file | Created | Required active ticket artifact. |
| Graphify install | Not created/run | Dependency and tool gates required. |
| Graphify CLI run | Not run | Future exact execution gate required. |
| OpenCode integration | Not created | Assistant config mutation blocked. |
| Generated graph outputs | Not created | Output gate required. |
| Graphify cache | Not created | Generated/cache output not approved. |
| Hooks/watch/MCP | Not created | Runtime/MCP activation blocked. |
| Package manifests/lockfiles | Not created | Dependency adoption blocked. |
| Tests/scripts/CI | Not created | Test/CI gates required. |
| Source tracking expansion | Not approved | Git/source tracking gate required. |
| G-03 | Not started | Explicit instruction required. |

## 18. Residual Risks
| Risk | Current handling |
| --- | --- |
| Future Graphify command may read too broadly | Require exact include/exclude paths and source classification. |
| Future output may look authoritative | Label generated projection evidence only. |
| OpenCode integration may mutate assistant behavior | Block integration in G-02. |
| Package install may add dependency and network risk | Dependency gate required; no install by default. |
| Cache/output may become tracked accidentally | Local-only/generated-sensitive; future Git gate required. |
| Graph evidence may bias CSS substrate decision | Preserve substrate neutrality and multi-candidate evaluation. |
| Existing `3_platform` siblings remain unknown | Keep uninspected until source classification gate. |

## 19. Stop Rules
Stop immediately if the work requires Graphify execution, package installation, source inspection, broad repo scanning, OpenCode integration, assistant config mutation, hooks, watch mode, MCP, provider/API/network/auth use, generated graph outputs, cache creation, source tracking, `.gitignore` mutation, product/external/secrets inspection, existing `3_platform` sibling inspection, Git staging/commit/push, or starting G-03.

Response to stop condition: preserve safe metadata only, state the blocked action, and require exact governance/security/human approval.

## 20. G-02 Invariants
| ID | Invariant |
| --- | --- |
| G02-001 | G-02 is a governance/tool-use gate only. |
| G02-002 | Graphify is not run, installed, adopted, integrated, or made authoritative by G-02. |
| G02-003 | `graphifyy` package fact is not dependency approval. |
| G02-004 | Future Graphify output is generated evidence only. |
| G02-005 | OpenCode integration is blocked by G-02. |
| G02-006 | No assistant config, `AGENTS.md`, `.agents/`, `.claude/`, or `.codex/` is created. |
| G02-007 | Hooks, watch mode, MCP serving, and always-on behavior are blocked. |
| G02-008 | Cognitive Semantic System remains the accepted name. |
| G02-009 | Final Cognitive Semantic System substrate remains deferred. |
| G02-010 | Graph remains candidate only. |
| G02-011 | Existing `3_platform` siblings remain uninspected and unapproved. |
| G02-012 | Validation evaluates; governance decides. |
| G02-013 | Source tracking is not expanded. |
| G02-014 | G-02 stops before G-03. |

## 21. Anti-patterns
Anti-patterns: Graphify evidence as authority; generated graph as truth; graph candidate as substrate selection; package name as dependency approval; CLI availability as command approval; read-only label as output-free guarantee; OpenCode support as integration permission; assistant rule creation as harmless; hooks as validation; watch mode as passive; MCP serving as documentation; generated report as governance; output cache as trackable source; broad repo scan as safe because it is local; existing `3_platform` as approved by parent path; `git add .`; starting G-03 inside G-02.

Rejected/prohibited/historical examples only: `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth`. No such string is accepted as a current AGENT PLATFORM or Cognitive Semantic System name.

## 22. Final Verdict
G-02 accepts the governance/tool-use gate for a possible future Graphify read-only repo-map evidence run.

G-02 does not approve or perform Graphify execution, installation, package adoption, OpenCode integration, assistant-rule creation, hooks, watch mode, MCP, generated graph outputs, cache creation, source tracking expansion, dependency adoption, provider/API/network/auth use, product activation, external source inspection, existing `3_platform` sibling inspection, final Cognitive Semantic System substrate selection, Git staging, commit, push, publication, or G-03.

Any future Graphify repo-map action requires a new exact-scope gate record with owner, command, paths, exclusions, dependency/security/license review, output handling, rollback, validation posture, and human/governance approval.
