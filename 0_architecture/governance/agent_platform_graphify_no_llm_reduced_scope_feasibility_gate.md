# G-08 - Graphify No-LLM / Reduced-Scope Feasibility Gate

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Graphify No-LLM / Reduced-Scope Feasibility Gate |
| Ticket | G-08 |
| Status | Accepted Graphify no-LLM / reduced-scope feasibility gate |
| Date | 2026-07-02 |
| Scope | Determine whether a future Graphify route can avoid provider/auth by using no-LLM, offline, code-only, reduced-scope, or fallback methods. |
| Authority | Feasibility review only, not rerun, provider activation, or output curation. |
| Related documents | G-00 through G-07, I-A, I-06, I-07, S-series, CSS-series, `.gitignore`, README.md. |
| Review target | Feasibility of future Graphify no-LLM or reduced-scope route. |

## 2. Purpose
G-06 failed because Graphify required an LLM API key. G-07 reviewed that failure. G-08 evaluates whether a safer path exists without provider/auth. G-08 does not rerun Graphify, configure provider/auth, read partial output, curate output, or start G-09.

## 3. Prior Failure Summary
| Field | Prior fact |
| --- | --- |
| run_id | `graphify_safe_run_20260702_153000` |
| attempted command | `graphify ../../../../0_architecture --no-viz` |
| working directory | `9_artifacts/graphify/graphify_safe_run_20260702_153000/architecture` |
| result | Failed. |
| failure reason | Graphify required an LLM API key for 87 document files and no approved provider/auth key was available. |
| `--no-viz` result | Did not avoid LLM requirement. |
| governed skeleton scan | Not run. |
| repo root scan | Not run. |
| partial outputs | Not curated. |
| provider/auth | Not configured. |
| G-07 classification | `provider_auth_required_by_graphify`. |

## 4. Feasibility Gate Definition
A no-LLM / reduced-scope feasibility gate determines whether future Graphify usage can avoid provider/auth by using CLI-supported no-LLM/offline/code-only options or by reducing input scope to file types that do not trigger LLM processing.

This feasibility gate is not a rerun, provider activation, API key approval, output curation, Graphify adoption, or Cognitive Semantic System substrate selection.

## 5. Authority Boundary
Governance decides whether to attempt another Graphify route. Security constrains provider/auth avoidance and output handling. Validation evaluates CLI/help/metadata evidence only. Git records only the G-08 document after human approval. Agents cannot approve rerun, provider/auth, output curation, or source tracking.

## 6. CLI Capability Review
Observed commands: `graphify --version` returned `graphify 0.9.5`; `graphify --help` succeeded. Fallback `graphify -h` was not run.

| Capability question | Help evidence | G-08 interpretation |
| --- | --- | --- |
| no-LLM/offline full extraction listed? | No explicit no-LLM or offline full-extract switch observed. | Not confirmed. |
| include/exclude controls listed for extraction? | No include/exclude or extension-filter switch observed in help. | Not confirmed. |
| mode controls listed? | `extract <path>` lists `--mode deep`; no shallow/no-doc mode shown. | Deep mode exists; no safe mode confirmed. |
| output directory controls listed? | `extract <path>` lists `--out DIR`; other commands use `--graph` or output paths. | Future output isolation may be possible, but not run authorization. |
| API key requirement suggested for docs? | `extract <path>` is described as `AST + semantic LLM`; `--backend` defaults to API-key-backed provider detection. | Provider/auth risk remains for document-heavy inputs. |
| code-only or docs-off switch listed? | `update <path>` says re-extract code files and update graph with no LLM; no docs-off initial extraction switch observed. | Code update path may exist, but initial code-only extraction remains ambiguous without a future exact gate. |
| `--no-viz` semantics | Help lists `--no-viz` as skipping `graph.html` generation for `cluster-only`. | Visualization-related only; not a no-LLM guarantee. |

Do not infer unsupported features from help output. CLI help evidence is not execution approval.

## 7. Input Shape Review
Extension counts were collected as metadata only; no file contents were opened.

| Root | Extension counts | Shape interpretation |
| --- | --- | --- |
| `0_architecture/` | `.md`: 88; `.gitkeep`: 3 | Architecture root is document-heavy and likely to trigger semantic LLM processing. |
| `3_platform/_governed_skeleton/` | `.md`: 32; `.py`: 7 | Governed skeleton contains Python modules and Markdown docs. |

A code-only scope might exist because governed skeleton has `.py` files. However, direct reduced-root scanning remains risky because the same tree also has Markdown docs and help did not show include/exclude filtering. Excluding docs would make Graphify less useful for architecture governance because much of the system authority is documented in Markdown.

## 8. Feasibility Options
| Option | Analysis | G-08 posture |
| --- | --- | --- |
| A - No-LLM / offline Graphify mode | Feasible only if CLI help confirms it; no explicit no-LLM/offline full extraction option observed. | Not feasible on current evidence. |
| B - Include/exclude or code-only Graphify mode | Include/exclude filtering was not shown. Code-only might be possible only with a future exact code-only input strategy or clarified CLI behavior. | Maybe feasible, ambiguous. |
| C - Reduced safe root: governed skeleton only | Lower risk than architecture docs but still includes 32 Markdown files and may trigger LLM processing. | Maybe feasible only after stronger plan. |
| D - Manual/static dependency map without Graphify | Controlled fallback with no provider/auth and no generated graph. Slower but safe. | Feasible. |
| E - Provider/Auth Gate for Graphify LLM | Highest risk; requires API key/provider/data exposure review. | Deferred, not recommended immediately. |

## 9. Feasibility Decision Matrix
| option | evidence | feasibility | risk | required next gate | recommendation |
| --- | --- | --- | --- | --- | --- |
| No-LLM/offline full extraction | No explicit help support observed. | not_feasible | Medium if assumed. | CLI clarification if pursued. | Do not plan rerun from this evidence. |
| Include/exclude filtering | No include/exclude or extension filter observed. | not_feasible | Medium. | CLI clarification. | Do not rely on filtering. |
| Code-only scope | Governed skeleton has 7 `.py` files; help says `update` code re-extraction needs no LLM. | maybe_feasible | Medium. | CLI capability clarification or reduced-scope plan after exact evidence. | Clarify before run. |
| Governed skeleton reduced root | 32 `.md` and 7 `.py` under safe root. | maybe_feasible | Medium-high due docs. | Reduced-scope safe run plan only if docs are excluded or no-LLM confirmed. | Do not run yet. |
| Non-Graphify static map | Needs no Graphify/provider/auth. | feasible | Low. | Non-Graphify map ticket. | Safe fallback. |
| Provider/auth LLM route | Prior failure required API key. | blocked | High. | Provider/API/MCP activation gate plus security review. | Defer. |

## 10. Recommended Route
Evidence is ambiguous: CLI help does not confirm a safe no-LLM full extraction or include/exclude filter, but it does show a code re-extraction path that claims no LLM. Recommended next ticket: `G-09 - Graphify CLI Capability Clarification`.

Alternative if governance wants to stop spending effort on Graphify: `G-09 - Non-Graphify Parallel Work Packet Dependency Map`. Provider/Auth route is not recommended unless governance explicitly chooses it after safer options fail.

## 11. Provider / Auth Boundary
LLM API key requirement is not provider activation approval. No API key may be configured by G-08. No provider credentials may be inspected. No environment variables may be read. No `.env` may be inspected. No auth flow may be started. Provider/auth route requires a separate gate.

## 12. Graphify Execution Boundary
No Graphify repo-map command is authorized by G-08. No alternate Graphify run is authorized. No no-LLM run is authorized. No reduced-scope run is authorized. No governed skeleton run is authorized. No repo-root scan is authorized. No OpenCode integration is authorized.

## 13. Partial Artifact Boundary
Partial artifacts from G-06 remain local-only. G-08 does not read or curate partial outputs, delete partial artifacts, or track partial artifacts. Partial artifacts remain generated-sensitive by default.

## 14. Security Review
No secrets/credentials were inspected. No product/external source was inspected. No existing `3_platform` siblings were inspected. No provider/auth was configured. CLI help output is safe metadata unless it reveals local secrets; no such exposure was observed. Extension counts are metadata-only and not content review.

## 15. Validation Review
G-08 validates only feasibility evidence. G-08 does not validate Graphify graph output, create a curated summary, or create a parallel dependency map. Missing no-LLM support blocks Graphify rerun unless provider/auth gate is approved.

## 16. Cognitive Semantic System Boundary
Graphify feasibility does not affect Cognitive Semantic System substrate decision. Graph remains candidate only. Graphify remains evidence only, not authority. Cognitive Semantic System substrate remains deferred. No graph/vector/database/ontology runtime is created.

## 17. Created / Not Created Register
| artifact/action | G-08 status | reason |
| --- | --- | --- |
| feasibility document | Created | Required G-08 artifact. |
| Graphify help | Checked | Allowed CLI metadata command. |
| extension counts | Checked | Metadata-only input shape review. |
| Graphify repo-map | Not rerun | Not authorized by G-08. |
| provider/auth | Not configured | Blocked. |
| API key | Not added | Blocked. |
| partial outputs | Not read | Raw output consumption blocked. |
| output curation | Not performed | Not in scope. |
| cleanup | Not executed | Requires future explicit decision. |
| safe mirror | Not created | Not in scope. |
| OpenCode integration | Not installed | Blocked. |
| source tracking | Not expanded | Git/source gate required. |
| next ticket | Not started | G-08 stops before G-09. |

## 18. Residual Risk Register
| Risk | Current handling |
| --- | --- |
| CLI help may be insufficient | Recommend CLI capability clarification. |
| Graphify no-LLM mode may not exist | Treat as not confirmed. |
| Include/exclude may not exist | Treat as not confirmed. |
| Reduced scope may make Graphify less useful | Preserve as limitation. |
| Code-only graph may miss documentation dependencies | Preserve as limitation. |
| Provider/auth route remains high risk | Defer. |
| No curated summary exists | Future curation still blocked. |
| No parallel dependency map exists | Future ticket required. |
| Partial artifacts remain local-only | Keep generated-sensitive posture. |

## 19. Blocker Register
Blockers retained: need Graphify rerun; need no-LLM mode; need reduced-scope mode; need provider/auth; need API key; need output curation; need partial cleanup; need non-Graphify fallback; need parallel dependency map; need Cognitive Semantic System substrate decision.

## 20. Incident Handling
Incidents include G-08 reruns Graphify against a path; API key configured; provider/auth activated; `.env` inspected; partial output content parsed/curated; product/external/secrets scanned; existing `3_platform` sibling inspected; raw output tracked; partial output published; OpenCode integration installed; Graphify adopted as authority; Cognitive Semantic System substrate selected; Git mutation attempted; next ticket started.

Response: STOP, preserve safe metadata only, require governance/security decision.

## 21. G-08 Invariants
| ID | Invariant |
| --- | --- |
| G08-001 | Graphify No-LLM / Reduced-Scope Feasibility Gate is not a rerun. |
| G08-002 | No provider/auth configuration is authorized by G-08. |
| G08-003 | No API key use is authorized by G-08. |
| G08-004 | No Graphify repo-map command is authorized by G-08. |
| G08-005 | CLI help evidence is not execution approval. |
| G08-006 | Extension counts are not content inspection. |
| G08-007 | Partial artifacts remain local-only. |
| G08-008 | Partial artifacts are not curated by G-08. |
| G08-009 | Graphify remains evidence only, not authority. |
| G08-010 | Graphify repo map is not Cognitive Semantic System substrate. |
| G08-011 | Graph remains candidate only. |
| G08-012 | Cognitive Semantic System substrate remains deferred. |
| G08-013 | Existing 3_platform siblings remain uninspected and unapproved. |
| G08-014 | Product source remains local-only. |
| G08-015 | External sources remain local-only. |
| G08-016 | Hermes is not inspected or adopted. |
| G08-017 | Validation evaluates; governance decides. |
| G08-018 | G-08 stops before the next ticket. |

## 22. Anti-patterns
Anti-patterns: help output as run approval; no-LLM mention as rerun authorization; extension count as source review; reduced scope as permission; failure as permission to add API key; Graphify output as authority; Graphify repo map as Cognitive Semantic System substrate; raw graph committed; existing `3_platform` as approved source; `git add .`; starting next ticket inside G-08.

Rejected/prohibited/historical examples only: `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth`. No such string is accepted as a current AGENT PLATFORM or Cognitive Semantic System name.

## 23. Next Ticket Recommendation
If no-LLM/reduced-scope is feasible after clarification: `G-09 - Graphify Reduced-Scope Safe Run Plan`.

If not feasible: `G-09 - Non-Graphify Parallel Work Packet Dependency Map`.

If ambiguous, as current evidence indicates: `G-09 - Graphify CLI Capability Clarification`.

If provider/auth route is selected by governance: `G-09 - Graphify Provider/Auth Activation Gate`.

G-08 does not start G-09.

## 24. Final Verdict
| Question | Answer |
| --- | --- |
| What did G-08 review? | CLI help/version metadata, allowed path checks, and extension-count metadata for `0_architecture/` and `_governed_skeleton/`. |
| Does Graphify support no-LLM/offline mode? | No explicit no-LLM/offline full-extraction mode was confirmed by help. |
| Does Graphify support include/exclude/code-only reduced scope? | Include/exclude was not confirmed; code-only remains ambiguous because help mentions no-LLM code update but not initial filtered extraction. |
| Is reduced-scope Graphify feasible? | Maybe feasible only after CLI capability clarification or an exact code-only strategy; not safe to run yet. |
| Was Graphify rerun? | No. |
| Was provider/auth configured? | No. |
| Were partial outputs read or curated? | No. |
| Was product/external/secrets/3_platform sibling content inspected? | No. |
| Was Graphify adopted? | No. |
| Was Cognitive Semantic System substrate selected? | No. |
| What remains blocked? | Graphify repo-map run, no-LLM run, reduced-scope run, governed skeleton scan, repo-root scan, provider/auth/API key setup, output curation, cleanup, source tracking, Graphify authority, Hermes adoption, and Cognitive Semantic System substrate selection. |
| Recommended next ticket? | `G-09 - Graphify CLI Capability Clarification`, after explicit instruction only. |

G-08 records feasibility evidence and stops here. No rerun occurred, no provider/auth was configured, partial outputs were not read or curated, and no next ticket was started.
