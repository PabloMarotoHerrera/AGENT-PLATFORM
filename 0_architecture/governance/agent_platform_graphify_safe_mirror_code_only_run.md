# G-13 - Graphify Safe Mirror Code-Only Run

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Graphify Safe Mirror Code-Only Run |
| Ticket | G-13 |
| Status | Accepted Graphify safe mirror code-only run |
| Date | 2026-07-03 |
| Scope | Execute exactly one bounded Graphify run against the G-12 code-only safe mirror for AGENT PLATFORM / Siamese. |
| Authority | Exact mirror execution only, not repo-root scan, provider/auth, output curation, source tracking, Graphify adoption, or Cognitive Semantic System substrate selection. |
| Related documents | G-00 through G-12, I-A, I-06, I-07, S-series, CSS-series, `.gitignore`, README.md. |
| Execution target | G-12 safe mirror under `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/`. |

## 2. Purpose
G-12 materialized a code-only safe mirror with exactly seven Python files. G-13 executes Graphify only against that mirror from the contained `work/` directory.

G-13 does not run repo-root scan. G-13 does not run `/graphify .`. G-13 does not run `graphify .`. G-13 does not scan live source paths. G-13 does not configure provider/auth. G-13 does not read or curate generated outputs. G-13 does not start G-14.

## 3. Evidence Basis
| Evidence | G-13 use |
| --- | --- |
| G-06 failed on provider/auth for documentation files. | G-13 avoids docs and provider/auth. |
| G-09 confirmed code-only AST extraction can avoid API calls if corpus is code-only. | G-13 uses only the code-only mirror. |
| G-12 validated exactly seven `.py` files and zero non-Python files under the mirror input. | G-13 preflight repeats that validation before execution. |
| G-12 fixed run ID `graphify_safe_mirror_20260703_120000`. | G-13 uses the same run ID and creates no new run ID. |
| G-12 created no `graphify-out/`. | G-13 checks output creation after the run. |

## 4. Execution Boundary
A Graphify safe mirror code-only run is an exact one-time execution against a local-only generated code mirror, with strict preflight validation, output containment checks, no provider/auth, and no output curation.

Execution is not Graphify adoption. Execution is not repo-root scan. Execution is not `/graphify .`. Execution is not OpenCode integration. Execution is not provider/auth approval. Execution is not output curation. Execution is not source tracking expansion. Execution is not Cognitive Semantic System substrate selection.

## 5. Run Record
| Field | Value |
| --- | --- |
| run_id | `graphify_safe_mirror_20260703_120000` |
| command | `graphify ../input/governed_skeleton_code_only --no-viz` |
| cwd | `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/work/` |
| input_path | `../input/governed_skeleton_code_only` |
| input_origin | G-12 local-only generated code mirror. |
| input_file_count | 7 |
| input_extension_set | `.py` only |
| non_python_file_count | 0 |
| graphify_version | `graphify 0.9.5` |
| provider_auth_status | No provider/auth/API-key/model prompt observed; no provider/auth configured. |
| execution_status | Completed as contained execution, but extraction was empty: Graphify reported `found 0 code, 0 docs, 0 papers, 0 images` and `graph is empty`. |
| output_location | Empty `input/governed_skeleton_code_only/graphify-out/` directory created. No work output directory. |
| output_escape_status | No output observed outside `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/`. |
| assistant_config_status | `AGENTS.md`, `.agents/`, `.claude/`, and `.codex/` absent. |
| curation_status | No output content read, parsed, summarized, or curated. |
| source_tracking_status | Not expanded; mirror and raw generated outputs remain local-only under ignored `9_artifacts/`. |
| decision_status | Contained empty-extraction run recorded; no rerun authorized. |

## 6. Preflight Validation
| Check | Result |
| --- | --- |
| mirror root exists | True |
| `README.local-only.txt` exists | True |
| input root exists | True |
| work root exists | True |
| output_check root exists | True |
| input extension count | `.py`: 7 |
| input file count | 7 |
| non-Python file check result | No files returned; count 0. |
| repo-root `graphify-out/` absent | True |
| live source `3_platform/_governed_skeleton/graphify-out/` absent | True |
| mirror input `graphify-out/` absent before execution | True |
| mirror work `graphify-out/` absent before execution | True |
| assistant config files absent | True |

Preflight passed before Graphify execution.

## 7. Command Execution Log
| Field | Result |
| --- | --- |
| exact command | `Push-Location 9_artifacts/graphify/graphify_safe_mirror_20260703_120000/work`; `graphify ../input/governed_skeleton_code_only --no-viz`; `Pop-Location` |
| exact working directory | `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/work/` |
| result | Completed as a contained command with empty extraction/no graph nodes. |
| provider/auth/API-key prompt | None observed. |
| mirror-only scan | Stdout identified scan path as `.../input/governed_skeleton_code_only`. |
| output containment | Output stayed under the G-12 run tree; no repo-root or live-source output observed. |
| unexpected artifacts | Empty `input/governed_skeleton_code_only/graphify-out/` directory was created; allowed alternate output location. |
| safe stdout/stderr summary | Graphify scanned the mirror input, reported `found 0 code, 0 docs, 0 papers, 0 images`, and reported `graph is empty - extraction produced no nodes`. |
| raw output handling | No long raw output retained; no generated output content opened. |

The empty extraction is not a useful repository map. A likely follow-up is failure/empty-extraction review or non-Graphify fallback, not an automatic rerun.

## 8. Output Artifact Register
| Path | Exists? | Classification | Content inspected? | Trackable? | Next review |
| --- | --- | --- | --- | --- | --- |
| `work/graphify-out/` | False | No work output directory. | No | No | None. |
| `work/graphify-out/GRAPH_REPORT.md` | False | Generated report absent. | No | No | None. |
| `work/graphify-out/graph.json` | False | Generated graph absent. | No | No | None. |
| `work/graphify-out/cache/` | False | Cache absent. | No | No | None. |
| `work/graphify-out/graph.html` | False | Visualization absent, expected possible with `--no-viz`. | No | No | None. |
| `input/governed_skeleton_code_only/graphify-out/` | True | Generated-local empty output directory. | No | No | G-14 decision. |
| `input/governed_skeleton_code_only/graphify-out/GRAPH_REPORT.md` | False | Generated report absent. | No | No | None. |
| `input/governed_skeleton_code_only/graphify-out/graph.json` | False | Generated graph absent. | No | No | None. |
| `input/governed_skeleton_code_only/graphify-out/cache/` | False | Cache absent. | No | No | None. |
| `input/governed_skeleton_code_only/graphify-out/graph.html` | False | Visualization absent, expected possible with `--no-viz`. | No | No | None. |
| repo-root `graphify-out/` | False | Forbidden output absent. | No | No | None. |
| live source `3_platform/_governed_skeleton/graphify-out/` | False | Forbidden live-source output absent. | No | No | None. |
| `AGENTS.md`, `.agents/`, `.claude/`, `.codex/` | False | Assistant config absent. | No | No | None. |

Generated output metadata checks for both possible output directories returned no child entries.

## 9. Output Classification
All Graphify outputs are local-only. All Graphify outputs are generated-sensitive by default. Raw outputs are not source. Raw outputs are not authority. Raw outputs are not trackable by default. Raw outputs are not Cognitive Semantic System substrate. Raw outputs must not be consumed by agents until curated. G-14 must decide curation, containment review, failure review, cleanup, or fallback.

Graphify output is generated evidence, not authority.

## 10. Provider / Auth Boundary
No API key usage is approved. No `.env` is inspected. No credentials are inspected. No provider/auth/model endpoint is activated. No provider/auth configuration is authorized by G-13.

If Graphify had requested provider/auth/API-key/model setup, the run would be classified as stopped and no retry would be authorized. G-13 success as a bounded execution is valid only because no provider/auth prompt was observed.

## 11. Graphify Adoption Boundary
Graphify remains evidence only. Graphify is not authority. Graphify output is not truth. Graphify output is not source. Graphify output is not governance. Graphify execution does not approve broader Graphify use.

## 12. Repository Root / OpenCode Boundary
Repository root scan remains blocked. `/graphify .` remains blocked. `graphify .` remains blocked. OpenCode integration remains blocked. `AGENTS.md` creation remains blocked. `.agents/`, `.claude/`, and `.codex/` remain blocked. Hooks, watch mode, MCP, Neo4j push, URL ingestion, and always-on behavior remain blocked.

## 13. Git / Source Tracking Boundary
Raw outputs remain untracked. The mirror remains untracked. `9_artifacts/` remains local-only by default. No force-add is authorized. Only the G-13 governance record may be considered for exact-path commit after human approval. `git add .` remains prohibited.

## 14. Partial Artifact Boundary
G-06 partial artifacts remain local-only. G-13 does not read or curate G-06 partial outputs. G-13 does not delete G-06 partial artifacts. G-13 does not track G-06 partial artifacts.

## 15. Cognitive Semantic System Boundary
Graphify execution does not affect Cognitive Semantic System substrate decision. Graph remains candidate only. Graphify remains evidence only, not authority. Cognitive Semantic System substrate remains deferred. No graph, vector database, ontology database, or runtime is created or adopted.

## 16. Created / Not Created Register
| Artifact/action | G-13 status | Reason |
| --- | --- | --- |
| governance document | Created | Required G-13 record. |
| Graphify executed once against mirror | Completed | One allowed command only. |
| Graphify run against repo root | Not run | Blocked. |
| `/graphify .` | Not run | Blocked. |
| live source scanned | Not scanned | Input was mirror path only. |
| product/external/Hermes/secrets scanned | Not scanned | Outside scope. |
| provider/auth | Not configured | Blocked and not requested. |
| API key | Not added | Blocked. |
| output generated | Empty `input/.../graphify-out/` directory only. | Contained but no graph/report files. |
| output content read | Not read | Content review blocked. |
| output curation | Not performed | G-14 or later. |
| `.graphifyignore` | Not created | Blocked. |
| `.gitignore` | Not modified | Blocked. |
| OpenCode integration | Not installed | Blocked. |
| source tracking | Not expanded | Git/source tracking gate required. |
| G-14 | Not started | G-13 stops before G-14. |

## 17. Residual Risk Register
| Risk | Current handling |
| --- | --- |
| Output may be narrow because mirror is code-only. | Accepted limitation. |
| Output may omit architecture documentation. | Expected due provider/auth avoidance. |
| Graphify interpretation may be incomplete. | Empty extraction shows no useful map from this run. |
| Future output curation may find low value. | Recommend failure/empty-extraction review or fallback. |
| Output behavior may differ between versions. | Record version `0.9.5`. |
| Raw output may be sensitive. | Treat generated output as local-only even when empty. |
| Mirror may become stale. | Future reruns require new gate. |
| Provider/auth route remains high risk for docs. | Still blocked. |
| Repo-root scan remains blocked. | No change. |
| No curated summary exists yet. | G-14 decision required. |

## 18. Blocker Register
Blockers retained: need output curation gate if useful output ever exists; need failure/empty-extraction review for this run; need source tracking decision for any curated summary; need cleanup policy for mirror/artifacts; need provider/auth if docs are included later; need repo-root scan approval before root scan; need OpenCode integration decision before assistant integration; need Cognitive Semantic System substrate decision.

## 19. Incident Handling
Incidents include Graphify scans repo root; scans live source; scans product, external, Hermes, or secrets; requests API key/provider/auth/model endpoint; creates output outside allowed artifact tree; creates repo-root `graphify-out/`; creates live source `graphify-out/`; creates assistant config files; installs OpenCode integration; output content is read or curated; raw output is tracked; `.graphifyignore` is created; `.gitignore` is modified; package/provider/auth command is executed; Graphify is adopted as authority; Cognitive Semantic System substrate is selected; Git mutation is attempted; or G-14 is started.

Response: STOP, preserve safe metadata only, require governance/security decision.

## 20. G-13 Invariants
| ID | Invariant |
| --- | --- |
| G13-001 | Graphify Safe Mirror Code-Only Run is exact mirror execution only. |
| G13-002 | Graphify is run at most once by G-13. |
| G13-003 | Repository root scan remains blocked. |
| G13-004 | `/graphify .` remains blocked. |
| G13-005 | Live source paths are not scanned. |
| G13-006 | No provider/auth configuration is authorized by G-13. |
| G13-007 | Graphify output is generated evidence, not authority. |
| G13-008 | Raw Graphify output is not curated by G-13. |
| G13-009 | Raw Graphify output is not trackable by default. |
| G13-010 | `.graphifyignore` is not created by G-13. |
| G13-011 | `.gitignore` is not modified by G-13. |
| G13-012 | OpenCode integration is not authorized by G-13. |
| G13-013 | Graphify repo map is not Cognitive Semantic System substrate. |
| G13-014 | Graph remains candidate only. |
| G13-015 | Cognitive Semantic System substrate remains deferred. |
| G13-016 | Existing 3_platform siblings remain uninspected and unapproved. |
| G13-017 | Product source remains local-only. |
| G13-018 | External sources remain local-only evidence. |
| G13-019 | Hermes is not inspected or adopted. |
| G13-020 | Validation evaluates; governance decides. |
| G13-021 | G-13 stops before G-14. |

## 21. Anti-patterns
Anti-patterns: successful run as Graphify adoption; output as authority; output as source; output as governance truth; code-only output as architecture map; `--no-viz` as no-LLM control; rerun by convenience; repo-root scan by convenience; `/graphify .` by convenience; OpenCode integration by convenience; raw graph committed; mirror committed; Graphify repo map as Cognitive Semantic System substrate; selecting graph substrate because Graphify exists; `git add .`; starting G-14 inside G-13.

Rejected/prohibited/historical examples only: `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth`. No such string is accepted as a current AGENT PLATFORM, Siamese, or Cognitive Semantic System name.

## 22. Next Ticket Recommendation
Conditional recommendations:

| Condition | Recommendation |
| --- | --- |
| Run succeeds and output is contained | `G-14 - Graphify Output Metadata Review` |
| Run succeeds but output location is unexpected but contained | `G-14 - Graphify Output Containment Review` |
| Run fails, requests provider/auth, or produces empty extraction from valid mirror input | `G-14 - Graphify Safe Mirror Run Failure Review` |
| Graphify remains low-value | `G-14 - Non-Graphify Parallel Work Packet Dependency Map` |

Actual recommendation: `G-14 - Graphify Safe Mirror Run Failure Review`, because preflight confirmed seven `.py` files but Graphify reported zero code and produced no graph/report files.

G-13 does not start G-14.

## 23. Final Verdict
| Question | Answer |
| --- | --- |
| What did G-13 run? | One Graphify command against the G-12 safe mirror only. |
| What command was used? | `graphify ../input/governed_skeleton_code_only --no-viz`. |
| What cwd was used? | `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/work/`. |
| Was the input mirror code-only before execution? | Yes: seven `.py` files and zero non-Python files. |
| Did Graphify request provider/auth/API key? | No. |
| Did the command succeed, fail, or stop? | It completed as a contained command but produced empty extraction/no nodes; no rerun authorized. |
| Where did outputs appear? | Empty `input/governed_skeleton_code_only/graphify-out/` directory only. |
| Did any output escape allowed artifact tree? | No. |
| Was repo root scanned? | No. |
| Was live source scanned? | No. |
| Was `/graphify .` run? | No. |
| Was OpenCode integration installed? | No. |
| Were output contents read or curated? | No. |
| Was Graphify adopted? | No. |
| Was Cognitive Semantic System substrate selected? | No. |
| What remains blocked? | Rerun, repo-root scan, live-source scan, provider/auth, output curation, source tracking, OpenCode integration, partial output review, product/Hermes/sibling inspection, graph adoption, Graphify authority, and Cognitive Semantic System substrate selection. |
| What is the recommended next ticket? | `G-14 - Graphify Safe Mirror Run Failure Review`, after explicit instruction only. |

G-13 stops here. Graphify was run exactly once against the mirror. Repository root was not scanned, `/graphify .` was not run, live source was not scanned, no provider/auth was configured, output content was not read or curated, and G-14 was not started.
