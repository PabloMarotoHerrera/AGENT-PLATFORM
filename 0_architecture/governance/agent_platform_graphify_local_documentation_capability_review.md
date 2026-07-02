# G-09 - Graphify Local Documentation Capability Review

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Graphify Local Documentation Capability Review |
| Ticket | G-09 |
| Status | Accepted Graphify local documentation capability review |
| Date | 2026-07-02 |
| Scope | Review local Graphify documentation for ignore, exclusion, no-LLM, code-only, output, safe-root, and integration capabilities relevant to AGENT PLATFORM / Siamese. |
| Authority | Documentation capability review only, not execution, adoption, provider/auth, source tracking, or Cognitive Semantic System substrate selection. |
| Related documents | G-00 through G-08, I-A, I-06, I-07, S-series, CSS-series, `.gitignore`, README.md. |
| Review target | Local Graphify documentation under `4_external/sources/graphify/`. |

## 2. Purpose
G-08 left Graphify no-LLM and reduced-scope feasibility ambiguous because CLI help did not confirm full no-LLM extraction or include/exclude filtering. The user identified local Graphify documentation under `4_external/sources/graphify/` that may document safe capability boundaries.

G-09 reviews local documentation only to clarify ignore, exclusion, no-LLM, code-only, docs-off, output, and assistant-integration behavior. G-09 does not run Graphify, inspect Graphify implementation source, configure provider/auth, read partial G-06 output, or start G-10.

## 3. Documentation Review Boundary
Allowed scope was local documentation files only: root README/architecture/security/change docs, docs markdown, skill markdown, reference markdown, and worked-example explanatory markdown. Forbidden scope remained Graphify implementation source code, tests, package internals, build scripts, package lockfiles, generated caches, partial G-06 artifacts, product source, Hermes source, secrets, credentials, `.env`, and existing `3_platform` siblings.

Documentation evidence is not authority. Documentation evidence may inform future gates only. External Graphify documentation remains local-only evidence and is not Graphify adoption, source adoption, execution approval, or source tracking approval.

## 4. Prior State Summary
| Prior ticket | State carried forward |
| --- | --- |
| G-06 | Attempted `graphify ../../../../0_architecture --no-viz`; failed because Graphify required an LLM API key for 87 document files. |
| G-07 | Classified the failure as `provider_auth_required_by_graphify`; no rerun, provider/auth, curation, or cleanup authorized. |
| G-08 | CLI help found no confirmed no-LLM full extraction, no confirmed include/exclude filtering, and ambiguous code-only behavior. |
| G-09 need | Clarify whether local docs support ignore/exclude/config/no-LLM/code-only/output control. |

## 5. Capability Questions
| question | documentation evidence | answer | confidence | future implication |
| --- | --- | --- | --- | --- |
| Does Graphify support `.graphifyignore` or equivalent? | README `Ignoring files` says create `.graphifyignore` with `.gitignore` syntax and `!` negation. | Yes. | High | Future gate can design exact ignore strategy. |
| Does Graphify respect `.gitignore`? | README says `.gitignore` is respected automatically and merged with `.graphifyignore`. | Yes. | High | Current repo `.gitignore` may reduce accidental broad scan, but ignored is not security. |
| Does Graphify support `--ignore`? | No path-filter `--ignore` option found in reviewed docs. | Not confirmed. | Medium | Do not rely on CLI `--ignore`. |
| Does Graphify support `--exclude`? | Only unrelated `--exclude-hubs` for clustering was documented. | Not for path exclusion. | Medium | Use ignore files, not `--exclude`, unless later CLI proof says otherwise. |
| Does Graphify support `--include`? | No path-filter `--include` option found; `.graphifyignore` supports `!` negation. | Not as CLI option. | Medium | Inclusion must be modeled through ignore rules or exact safe roots. |
| Does Graphify support extension filtering? | README lists supported extensions; ignore examples include extension patterns. | Via ignore patterns only. | Medium | Docs can be excluded by pattern if future gate approves ignore file. |
| Does Graphify support no-LLM mode? | README and how-it-works state code files use local AST; code-only corpus needs no API key. | Code-only yes; general no-LLM no. | High | A future code-only path may be possible only after exclusions. |
| Does Graphify support offline mode? | README privacy says code-only `graphify extract` runs fully offline. | Code-only offline yes; full mixed corpus no. | High | Architecture docs still trigger model route. |
| Does Graphify support code-only initial extraction? | README privacy and skill docs say a code-only corpus skips semantic extraction. | Yes if corpus contains only code. | High | `_governed_skeleton` must exclude Markdown before this is safe. |
| Does Graphify support docs-off / Markdown exclusion? | No docs-off flag found; `.graphifyignore` can exclude `*.md`. | Via ignore file only. | Medium | Needs exact ignore strategy. |
| Does Graphify support output directory control? | Docs assume `graphify-out/`; export/callflow and merge commands have output flags; direct subfolder extract writes inside scanned path. | Partial. | Medium | Safe `9_artifacts` output needs separate proof. |
| Can Graphify avoid `graphify-out/` in cwd? | Skill docs write `graphify-out/` in cwd; direct `graphify extract ./core/` docs place output under scanned path. | Partially, by run topology; not fully confirmed. | Medium | Output strategy remains required before run. |
| Does Graphify support config files? | `.graphifyignore`, `.gitignore`, assistant config, hooks, and MCP configs are documented. | Yes for ignore/integration; no general config confirmed. | Medium | Config mutation remains blocked by G-09. |
| Does Graphify require API keys for docs? | README says docs/PDF/images use model APIs for headless extract; skill can use host agent or configured backend. | Headless docs generally need provider/model route. | High | G-06 architecture docs remain blocked without approved route. |
| Does Graphify have a static-only mode? | AST-only behavior exists for code-only corpus; no named static-only full mode found. | Code-only static path only. | Medium | Do not infer full static documentation extraction. |
| Does Graphify support update without LLM? | Reference update docs say code-only changes skip semantic extraction and need no LLM. | Yes for code-only changes. | High | Useful after an initial code graph exists; not enough alone for first mixed run. |
| Does Graphify support OpenCode integration that writes `AGENTS.md`? | README lists `graphify opencode install` and says persistent instructions use `AGENTS.md`. | Yes, optional and risky. | High | Integration remains prohibited. |
| Does Graphify support hooks/watch/MCP/Neo4j/URL ingestion? | README and reference docs document hook, watch, MCP, Neo4j/FalkorDB, and URL add flows. | Yes. | High | All remain blocked unless separately gated. |

## 6. Evidence Register
| evidence_id | documentation file | matched term / section | paraphrased finding | confidence | limitation |
| --- | --- | --- | --- | --- | --- |
| G09-E01 | `README.md` | `Ignoring files` | `.graphifyignore` exists, uses `.gitignore` syntax, supports `!` negation, and merges after `.gitignore`. | High | Documentation only; behavior not executed. |
| G09-E02 | `README.md` | `What files it handles` | Code, docs, PDFs, images, video, configs, and manifests are supported input classes. | High | Support list is not safe-scan approval. |
| G09-E03 | `README.md` | `Privacy` | Code is processed locally; docs/PDF/images use model extraction; code-only extract can be fully offline. | High | Mixed architecture docs still need semantic path. |
| G09-E04 | `docs/how-it-works.md` | `Pass 1`, `Pass 3` | Tree-sitter handles code without API calls; docs/papers/images use Claude subagents and token cost. | High | Host-agent behavior may differ from headless CLI. |
| G09-E05 | `graphify/skill.md` | `Step 3` | Code-only corpus skips semantic extraction; docs/papers/images go through semantic extraction. | High | Skill instructions are external documentation, not AGENT PLATFORM instruction. |
| G09-E06 | `graphify/skills/opencode/references/update.md` | `code_only` | Incremental update can skip semantic extraction when changed files are all code. | High | Applies after a graph/manifest exists. |
| G09-E07 | `README.md` | `graphify-out/` | Default outputs are `graph.html`, `GRAPH_REPORT.md`, and `graph.json` under `graphify-out/`. | High | Initial output relocation remains partial. |
| G09-E08 | `README.md` / reference exports | `--mcp`, `--neo4j`, `--watch`, `add` | Integration, serving, database export, watch, and URL ingestion are documented. | High | These are blocked capabilities, not permissions. |
| G09-E09 | `README.md` | `graphify opencode install` | OpenCode integration and persistent instruction files are documented. | High | G-09 does not install or create them. |
| G09-E10 | `worked/rsl-siege-manager/review.md` | `.graphifyignore` | Worked review says excluding tests and migrations via `.graphifyignore` changes graph results. | Medium | Worked example is illustrative and not execution proof here. |
| G09-E11 | `ARCHITECTURE.md` | `graphify-out/` | Architecture doc says stages have no side effects outside `graphify-out/`. | Medium | Architecture doc references implementation modules but no source code was inspected. |
| G09-E12 | `README.md` | environment variables | Provider/backend variables are documented for headless extraction. | High | References to keys are evidence only; no values inspected. |

Reviewed documentation included root `README.md`, `ARCHITECTURE.md`, `docs/how-it-works.md`, `graphify/skill.md`, selected OpenCode reference markdown, and worked-example explanatory markdown. Discovery metadata listed broader candidates, but G-09 did not content-inspect Graphify `.py`, tests, lockfiles, build scripts, vendored dependencies, or G-06 partial outputs.

## 7. Ignore / Exclusion Findings
A Graphify ignore concept exists. Local docs confirm `.graphifyignore` in the project root, `.gitignore` syntax, `!` negation, automatic `.gitignore` respect, and merge behavior where `.graphifyignore` is evaluated last while never re-including files excluded by `.gitignore`.

Command-line path exclusion was not confirmed. No path `--ignore`, path `--exclude`, or path `--include` option was found in reviewed docs. Extension filtering appears feasible through ignore patterns, not through a documented CLI extension filter.

This is enough to justify a future ignore/exclusion strategy gate. It is not enough to approve a repo-root scan. Repo-root scan remains blocked because ignored is not security, output strategy is still incomplete, and any future behavior must be proven by exact gate before execution.

## 8. No-LLM / Offline Findings
The docs confirm local AST extraction for code and no API calls for a code-only corpus. They do not confirm a universal no-LLM/offline full extraction mode for mixed code/docs/papers/images. Docs, PDFs, and images are documented as semantic extraction inputs that use the host agent, configured provider, or local model backend.

`--no-viz` remains unrelated to no-LLM; it skips visualization. Provider/auth is still needed or otherwise substituted for document-heavy architecture docs in headless CLI paths. G-06 architecture docs therefore remain blocked without either exact exclusions, host-agent semantics explicitly approved, local model/provider gate, or non-Graphify fallback.

## 9. Output Control Findings
Documentation consistently describes `graphify-out/` as the default output folder containing `graph.html`, `GRAPH_REPORT.md`, `graph.json`, cache, cost, manifest, memory, converted sidecars, and temporary extraction files. Exports have some output controls, such as callflow `--output`, Obsidian `--obsidian-dir`, and merge `--out`, but local docs do not fully establish a clean initial extraction output directory strategy for `9_artifacts/graphify/`.

A safe output path under `9_artifacts/graphify/` may be possible by controlling working directory, exact input path, or a future verified output flag, but G-09 does not prove it. Output strategy remains a required future gate.

## 10. OpenCode / Assistant Integration Findings
Docs confirm OpenCode integration exists and can write persistent assistant instructions, including `AGENTS.md` and OpenCode-related hooks/plugins. Docs also confirm manual CLI/headless commands exist separately from assistant integration, so OpenCode integration is optional.

G-09 does not install integration, create `AGENTS.md`, create `.agents/`, create `.claude/`, create `.codex/`, enable hooks, enable watch mode, start MCP, or create always-on behavior. The external `AGENTS.md` guidance surfaced from the Graphify snapshot is local external-source evidence only and is not AGENT PLATFORM instruction.

## 11. Feasibility Decision Matrix
| route | documentation support | feasibility | risk | required next gate | recommendation |
| --- | --- | --- | --- | --- | --- |
| repo-root scan with ignore/exclusions | `.graphifyignore` and `.gitignore` confirmed. | Not approved. | High | Source classification, ignore strategy, output strategy, dry metadata proof. | Do not run; repo root remains blocked. |
| safe-root scan with output dir | Path arguments and `graphify-out/` behavior documented; output relocation partial. | Maybe feasible. | Medium | Graphify Ignore / Exclusion Strategy plus Output Strategy. | Candidate only. |
| governed skeleton code-only scan | Code-only offline path confirmed if docs excluded. | Maybe feasible. | Medium | Ignore strategy to exclude Markdown and exact code-only safe run plan. | Candidate only. |
| no-LLM/offline run | Code-only offline confirmed; mixed docs not confirmed. | Partial. | Medium | Reduced-scope safe run plan if code-only corpus can be guaranteed. | Candidate only. |
| provider/auth run | Docs confirm provider/backend paths for semantic extraction. | Feasible technically, not approved. | High | Provider/Auth Activation Decision plus security review. | Defer unless governance insists. |
| non-Graphify static map | Does not depend on Graphify. | Feasible. | Low | Non-Graphify map ticket. | Safe fallback. |

## 12. Recommended Route
Recommended next ticket: `G-10 - Graphify Ignore / Exclusion Strategy`.

Rationale: local documentation now confirms `.graphifyignore` and automatic `.gitignore` respect, and it confirms code-only extraction can avoid LLM/API use. The missing piece is a governed ignore/exclusion and output strategy that proves the input can be made code-only or otherwise safe before any run. If that strategy cannot produce a safe route, fall back to `G-10 - Non-Graphify Parallel Work Packet Dependency Map`.

## 13. Provider / Auth Boundary
G-09 does not approve API key usage. G-09 does not inspect `.env`. G-09 does not inspect credentials. G-09 does not activate providers, APIs, auth, network, model endpoints, local model servers, MCP, or cloud services.

Documentation references to API keys, backend variables, OAuth, IAM, local model endpoints, or provider names are evidence only. They do not authorize key setup, secret inspection, provider activation, or credential tests.

## 14. Graphify Execution Boundary
No Graphify rerun is authorized by G-09. No repo-root scan is authorized. No safe-root scan is authorized. No governed skeleton scan is authorized. No OpenCode integration is authorized. No ignore file is created by G-09. No config file is created by G-09. No Graphify repo-map command is authorized by G-09.

## 15. Partial Artifact Boundary
G-09 does not read or curate partial outputs. G-09 does not delete partial artifacts. G-09 does not parse, summarize, consume, track, or publish raw Graphify outputs from G-06.

Partial artifacts remain local-only and generated-sensitive by default. Bounded path checks only observed that the G-06 run root and architecture directory exist, while `architecture/graphify-out/` and repo-root `graphify-out/` are absent.

## 16. Security Review
No secrets or credentials were inspected. No `.env` was inspected. No product source was inspected. No Hermes source was inspected. No existing `3_platform` siblings were inspected. No provider/auth was configured. No network/API/MCP/model endpoint was activated.

External Graphify docs are local-only evidence. Documentation review does not approve external source adoption, dependency adoption, execution, source tracking, publication, or assistant instruction adoption.

## 17. Validation Review
G-09 validates only documentation capability evidence. G-09 does not validate actual Graphify behavior by execution. Any future execution must test documented behavior through an exact gate with named command, cwd, input paths, ignore posture, output paths, rollback, and security review.

Validation evaluates; governance decides.

## 18. Cognitive Semantic System Boundary
Graphify docs do not affect Cognitive Semantic System substrate decision. Graph remains candidate only. Graphify remains evidence only, not authority. Cognitive Semantic System substrate remains deferred.

No graph/vector/database/ontology runtime is created. No Graphify repo map is adopted as Cognitive Semantic System substrate.

## 19. Created / Not Created Register
| artifact/action | G-09 status | reason |
| --- | --- | --- |
| documentation capability review | Created | Required G-09 artifact. |
| docs searched | Completed | Local documentation files only; forbidden source/tests/build internals not content-inspected. |
| Graphify run | Not run | Execution prohibited. |
| Graphify source code inspection | Not performed | Documentation review only. |
| provider/auth configuration | Not configured | Blocked. |
| API key | Not added | Blocked. |
| partial outputs | Not read | G-06 output content remains unread. |
| output curation | Not performed | Not in scope. |
| cleanup | Not executed | Requires explicit future decision. |
| ignore/config file | Not created | Future strategy gate required. |
| OpenCode integration | Not installed | Assistant integration blocked. |
| source tracking | Not expanded | Git/source gate required. |
| next ticket | Not started | G-09 stops before G-10. |

## 20. Residual Risk Register
| risk | current handling |
| --- | --- |
| Documentation may be outdated relative to installed `graphifyy 0.9.5`. | Future gate must verify exact installed behavior before run. |
| Documentation may omit edge cases. | Do not treat docs as execution proof. |
| Documented ignore behavior may need execution proof. | Future G-10 should prove ignore strategy before scan. |
| No actual Graphify rerun performed. | Execution remains blocked. |
| No output curation. | Raw output remains unused. |
| No parallel dependency map. | Future ticket still needed if Graphify is deferred. |
| Provider/auth route remains high risk. | Defer unless governance explicitly chooses it. |
| Graphify may still require LLM for docs if exclusions are wrong. | Exact docs-off/code-only proof required. |

## 21. Blocker Register
Blockers retained: need Graphify rerun; need ignore strategy; need output strategy; need no-LLM proof; need reduced-scope proof; need provider/auth if no safe route exists; need output curation; need parallel dependency map; need source tracking if summaries are created; need Cognitive Semantic System substrate decision.

## 22. Incident Handling
Incidents include G-09 runs Graphify; configures API key; activates provider/auth; inspects `.env`; reads Graphify source code beyond docs; reads product/Hermes/secrets/existing `3_platform` siblings; reads partial output content; creates ignore/config files; installs OpenCode integration; adopts Graphify as authority; selects Cognitive Semantic System substrate; attempts Git mutation; or starts next ticket.

Response: STOP, preserve safe metadata only, require governance/security decision.

## 23. G-09 Invariants
| ID | Invariant |
| --- | --- |
| G09-001 | Graphify local documentation review is not Graphify execution. |
| G09-002 | Graphify documentation evidence is not Graphify authority. |
| G09-003 | No Graphify rerun is authorized by G-09. |
| G09-004 | No provider/auth configuration is authorized by G-09. |
| G09-005 | Graphify source code is not inspected by G-09. |
| G09-006 | Partial artifacts remain local-only and unread. |
| G09-007 | Graphify repo map is not Cognitive Semantic System substrate. |
| G09-008 | Graph remains candidate only. |
| G09-009 | Cognitive Semantic System substrate remains deferred. |
| G09-010 | Existing 3_platform siblings remain uninspected and unapproved. |
| G09-011 | Product source remains local-only. |
| G09-012 | External sources remain local-only evidence. |
| G09-013 | Hermes is not inspected or adopted. |
| G09-014 | Validation evaluates; governance decides. |
| G09-015 | G-09 stops before G-10. |

## 24. Anti-patterns
Anti-patterns: documentation as execution proof; documentation as authority; option name as run authorization; ignore support as repo-root scan approval; no-LLM mention as rerun authorization; Graphify output as authority; Graphify repo map as Cognitive Semantic System substrate; raw graph committed; existing `3_platform` as approved source; `git add .`; starting next ticket inside G-09.

Rejected/prohibited/historical examples only: `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth`. No such string is accepted as a current AGENT PLATFORM or Cognitive Semantic System name.

## 25. Next Ticket Recommendation
Conditional next ticket posture:

| Condition | Next ticket |
| --- | --- |
| Ignore/exclusion is confirmed | `G-10 - Graphify Ignore / Exclusion Strategy` |
| No-LLM/code-only path becomes exact | `G-10 - Graphify Reduced-Scope Safe Run Plan` |
| Docs are inconclusive | `G-10 - Non-Graphify Parallel Work Packet Dependency Map` |
| Provider/auth is the only viable route | `G-10 - Graphify Provider/Auth Activation Decision` |

Actual G-09 recommendation: `G-10 - Graphify Ignore / Exclusion Strategy`, after explicit instruction only.

G-09 does not start G-10.

## 26. Final Verdict
| Question | Answer |
| --- | --- |
| What did G-09 review? | Mandatory governance/security/Cognitive Semantic System docs, root `.gitignore`, root README, and local Graphify documentation files only. |
| Was Graphify documentation reviewed? | Yes. |
| Was Graphify source code inspected? | No. |
| Does documentation confirm ignore/exclusion support? | Yes: `.graphifyignore` and `.gitignore` behavior are documented. |
| Does documentation confirm `.graphifyignore` or `.gitignore` behavior? | Yes: `.graphifyignore` uses `.gitignore` syntax and `.gitignore` is respected automatically. |
| Does documentation confirm no-LLM/offline/code-only support? | Yes for code-only AST extraction; no for full mixed documentation extraction. |
| Does documentation confirm output directory control? | Partial only; default `graphify-out/` is clear, full safe output relocation remains unproven. |
| Does documentation confirm OpenCode integration risk? | Yes: optional integration can write persistent assistant files such as `AGENTS.md`. |
| Was Graphify rerun? | No. |
| Was provider/auth configured? | No. |
| Were partial outputs read or curated? | No. |
| Was Graphify adopted? | No. |
| Was Cognitive Semantic System substrate selected? | No. |
| What remains blocked? | Graphify rerun, repo-root scan, safe-root scan, ignore/config creation, output strategy, provider/auth/API keys, OpenCode integration, hooks/watch/MCP/Neo4j/URL ingestion, partial output curation, source tracking, product/Hermes/sibling inspection, Graphify authority, graph adoption, and Cognitive Semantic System substrate selection. |
| Recommended next ticket? | `G-10 - Graphify Ignore / Exclusion Strategy`, after explicit instruction only. |

G-09 stops here. No Graphify execution occurred, no provider/auth was configured, Graphify source code was not inspected, partial outputs were not read or curated, and no next ticket was started.
