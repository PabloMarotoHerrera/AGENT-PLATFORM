# G-10 - Graphify Ignore / Exclusion Strategy

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Graphify Ignore / Exclusion Strategy |
| Ticket | G-10 |
| Status | Accepted Graphify ignore / exclusion strategy |
| Date | 2026-07-02 |
| Scope | Design an exact governed exclusion strategy for possible future Graphify use in AGENT PLATFORM / Siamese. |
| Authority | Strategy only, not ignore-file creation, execution, adoption, provider/auth, source tracking, or Cognitive Semantic System substrate selection. |
| Related documents | G-00 through G-09, I-A, I-06, I-07, S-series, CSS-series, `.gitignore`, README.md. |
| Strategy target | Future Graphify input exclusion and output safety. |

## 2. Purpose
G-09 confirmed `.graphifyignore`, `.gitignore` respect, and code-only offline behavior in local Graphify documentation. G-10 designs a safe exclusion strategy before any future Graphify execution.

G-10 does not create `.graphifyignore`. G-10 does not modify `.gitignore`. G-10 does not run Graphify. G-10 does not approve `/graphify .`. G-10 does not configure provider/auth. G-10 does not start G-11.

## 3. Evidence Basis
| G-09 evidence | G-10 use |
| --- | --- |
| `.graphifyignore` is documented. | Candidate ignore profiles can be designed. |
| `.graphifyignore` uses `.gitignore` syntax. | Drafts use gitignore-style patterns. |
| `!` negation is supported. | Default-deny profiles can be proposed, not applied. |
| `.gitignore` is respected automatically. | Existing root exclusions remain part of the model. |
| `.graphifyignore` is evaluated after `.gitignore`. | Do not treat `.gitignore` exclusions as safely re-includable. |
| CLI `--ignore`, `--exclude`, and `--include` are not confirmed. | Do not depend on path-filter flags. |
| Extension filtering is feasible through ignore patterns. | Docs-off/code-only profiles can be proposed. |
| Code-only AST extraction can avoid API calls. | A code-only governed skeleton route is candidate. |
| Docs/Markdown can trigger provider/model route. | Architecture Markdown stays out of next Graphify attempt. |
| `--no-viz` is visualization-related. | Do not use it as no-LLM control. |
| Default output uses `graphify-out/`. | Output containment remains unresolved. |
| OpenCode integration can create `AGENTS.md`. | Integration remains blocked. |
| Repo-root scan remains blocked. | Ignore support does not change that. |

## 4. Strategy Boundary
A Graphify ignore / exclusion strategy is a pre-execution design artifact that specifies what future Graphify inputs must include, what they must exclude, how ignore rules should be drafted, how output side effects should be contained, and what future proof gate is required before execution.

This strategy is not execution. It is not `.graphifyignore` creation. It is not config creation. It is not repo-root scan approval. It is not OpenCode integration. It is not provider/auth approval. It is not Graphify adoption. It is not Cognitive Semantic System substrate selection.

## 5. Threat / Exclusion Model
| category | example paths | risk | required posture | proposed exclusion method |
| --- | --- | --- | --- | --- |
| Product workspaces | `2_products/` | Local-only product source exposure. | Excluded. | `.gitignore` plus future `.graphifyignore`. |
| External sources | `4_external/`, `4_external/sources/graphify/`, `4_external/sources/hermes-agent` | External raw source, license, instruction, and adoption confusion. | Excluded. | Future `.graphifyignore`; do not scan. |
| Previous knowledge | `previusknowledge/` | Historical/local-only migration corpus leakage. | Excluded. | Existing `.gitignore` plus future deny rule. |
| Datasets | `7_datasets/` | Data sensitivity and provenance risk. | Excluded. | Existing `.gitignore` plus future deny rule. |
| Models | `8_models/` | Model/license/safety risk. | Excluded. | Existing `.gitignore` plus future deny rule. |
| Generated artifacts | `9_artifacts/`, `graphify-out/` | Generated-sensitive outputs and feedback loops. | Excluded as input. | Existing `.gitignore` for `9_artifacts`; explicit `graphify-out/` rule. |
| Secrets/credentials | `.env*`, `secrets/`, `credentials/`, tokens, provider configs | Secret exposure or auth leakage. | Never read. | Existing `.gitignore`; explicit deny patterns. |
| Unapproved platform siblings | `3_platform/*` except `_governed_skeleton` | Unknown source posture. | Excluded. | Default deny plus explicit allow path only. |
| Git internals | `.git/` | History, config, hooks, refs. | Excluded. | Explicit deny rule. |
| Dependencies/vendors | `node_modules/`, `.venv/`, `venv/`, vendor dirs | Large, third-party, generated or installed code. | Excluded. | Existing `.gitignore` plus future deny rules. |
| Runtime caches | `cache/`, `.cache/`, `tmp/`, `temp/`, `__pycache__/` | Stale/generated data. | Excluded. | Existing `.gitignore` plus future deny rules. |
| Assistant config | `AGENTS.md`, `.agents/`, `.claude/`, `.codex/` | Persistent instruction mutation and tool behavior changes. | Excluded and not created. | Explicit deny rule and integration block. |
| Architecture docs | `0_architecture/**/*.md` | Markdown can trigger provider/model route. | Excluded from next Graphify attempt. | Do not scan `0_architecture/` next. |
| LLM-triggering docs | `*.md`, `*.rst`, `*.txt` | Non-code semantic extraction may need provider/auth. | Excluded for code-only proof route. | Docs-off future ignore profile. |

Observed path metadata: listed local-only and external surfaces exist; repo-root `graphify-out/`, `AGENTS.md`, `.agents/`, `.claude/`, and `.codex/` are absent. Current extension counts are `0_architecture/`: `.md 90`, `.gitkeep 3`; `3_platform/_governed_skeleton/`: `.md 32`, `.py 7`.

## 6. Input Strategy Options
| option | analysis | G-10 posture |
| --- | --- | --- |
| A - Repo-root `/graphify .` with root `.graphifyignore` | Desirable for broad map but high risk: root scan, many exclusions, output uncertainty, and possible docs/provider route. | Not approved. Requires ignore file gate, output strategy, dry proof, and incident guard. |
| B - Safe-root `3_platform/_governed_skeleton/` with docs excluded | Lower scope; likely code-only if Markdown/RST/TXT are excluded; preserves sibling quarantine. | Candidate preferred route after exact proof. |
| C - Safe mirror under `9_artifacts/graphify/<run_id>/input/` | Strongest containment; can include only approved files and keep output local-only, but requires copying/materialization gate. | Preferred planning route, not created by G-10. |
| D - Non-Graphify dependency map | Safest fallback with no Graphify execution or provider/auth. | Always acceptable fallback. |
| E - Provider/Auth route | Could process docs but requires API/key/data exposure review. | High risk; deferred unless governance explicitly chooses it. |

## 7. Recommended Strategy
Do not use repo-root `/graphify .` yet. Do not create root `.graphifyignore` yet. Keep architecture Markdown out of the next Graphify execution attempt. Keep product, external, datasets, models, artifacts, secrets, and unapproved platform siblings excluded. Keep OpenCode integration blocked. Keep provider/auth blocked.

Preferred future route: a code-only safe route using either a temporary `.graphifyignore` strategy scoped to `3_platform/_governed_skeleton/`, or a safe mirror containing only approved `.py` files from `3_platform/_governed_skeleton/`. Because G-10 cannot create ignore files, copy files, or run Graphify, the next gate should decide containment and output strategy before any execution proof.

## 8. Candidate Ignore Profile A - Root Default-Deny Draft
This block is a proposed text block inside this governance document. It is not written to `.graphifyignore`. It is not execution proof. It must not be used until G-11 or later approves file creation and behavior proof.

```gitignore
# G-10 UNAPPLIED DRAFT - do not create by this ticket.
# Purpose: future code-only Graphify candidate.

# Default deny.
*

# Allow path traversal to the governed skeleton only.
!3_platform/
!3_platform/_governed_skeleton/
!3_platform/_governed_skeleton/**/

# Allow Python source only.
!3_platform/_governed_skeleton/**/*.py

# Explicitly keep sensitive/local/generated areas excluded.
2_products/
4_external/
previusknowledge/
7_datasets/
8_models/
9_artifacts/
graphify-out/
.git/
.env*
secrets/
credentials/
tokens/
provider*
*credential*
*secret*
*token*
AGENTS.md
.agents/
.claude/
.codex/
```

Limitations: exact Graphify interpretation of negation must be proven later; `.gitignore` may already exclude paths and cannot be overridden safely; default-deny behavior must be tested only in a future proof gate; Repository root scan remains blocked.

## 9. Candidate Ignore Profile B - Safe-Root Docs-Off Draft
This block is an unapplied draft intended only for a future governed skeleton code-only test. It is not written to any file by G-10.

```gitignore
# G-10 UNAPPLIED DRAFT - safe-root docs-off profile.
# Intended only for future governed_skeleton code-only test.

*.md
*.rst
*.txt
graphify-out/
cache/
__pycache__/
*.pyc
.env*
secrets/
credentials/
tokens/
*credential*
*secret*
*token*
```

Limitations: if non-code files remain, the LLM route may still trigger; exact input must be proven by metadata before execution; no provider/auth fallback is allowed by this strategy.

## 10. Candidate Ignore Profile C - Do-Not-Use Broad Repo Profile
A broad repo-root profile that only excludes local-only folders is explicitly not recommended for the next run. It may still scan architecture documentation, trigger LLM/provider behavior, create a broad graph, miss unknown-sensitive material, and encourage over-trust.

This profile is a prohibited anti-pattern for G-10 planning. Ignore support is not repo-root scan approval.

## 11. Output Strategy
Default Graphify output uses `graphify-out/`. Root `graphify-out/` is forbidden. Output under source directories is undesirable. Output under `9_artifacts/graphify/<run_id>/` is preferred but unproven. A safe mirror may be the cleanest approach because both input and output can stay under `9_artifacts/`, subject to a future copy/materialization gate.

G-10 creates no outputs. Future G-11 must prove where Graphify writes outputs before any real run. If output cannot be isolated, Graphify execution remains blocked. Raw outputs remain local-only/generated-sensitive and not trackable by default.

## 12. `/graphify .` and OpenCode Posture
`/graphify .` remains blocked. `graphify .` remains blocked. OpenCode integration remains blocked. `graphify opencode install` remains blocked. `AGENTS.md` creation remains blocked. Hooks, watch, MCP, Neo4j push, URL ingestion, and always-on behavior remain blocked.

A future `/graphify .` may only be considered after an ignore file is created by exact gate, output location is proven, root scan is separately approved, product/external/secrets/artifacts are blocked by proof, provider/auth posture is decided, and Graphify output remains evidence only.

## 13. Provider / Auth Boundary
G-10 does not approve API key usage. G-10 does not inspect `.env`. G-10 does not inspect credentials. G-10 does not activate providers, APIs, auth, network, model endpoints, local model servers, MCP, or cloud services.

The strategy must avoid provider/auth requirements through input containment. It must not silently work around provider/auth by relying on existing keys, environment, browser auth, local credential stores, hosted agents, or local model endpoints.

## 14. Git / Source Tracking Boundary
G-10 does not create `.graphifyignore`. G-10 does not modify `.gitignore`. G-10 does not track Graphify outputs. G-10 does not force-add ignored files. Only this G-10 governance record may be considered for exact-path commit after human approval. `git add .` remains prohibited.

Bounded `.gitignore` review confirmed existing ignore coverage for `2_products/`, `4_external/sources/`, `previusknowledge/`, `7_datasets/`, `8_models/`, `9_artifacts/`, `.env*`, secrets, credentials, and token-like patterns. It did not show root `graphify-out/`, `3_platform`, or assistant config paths as ignored; G-10 does not modify `.gitignore` to add them.

## 15. Partial Artifact Boundary
G-06 partial artifacts remain local-only. G-10 does not read or curate partial outputs. G-10 does not delete partial artifacts. G-10 does not track partial artifacts.

## 16. Cognitive Semantic System Boundary
Ignore strategy does not affect Cognitive Semantic System substrate decision. Graph remains candidate only. Graphify remains evidence only, not authority. Cognitive Semantic System substrate remains deferred. No graph/vector/database/ontology runtime is created.

## 17. Feasibility Decision Matrix
| route | input containment | output containment | no-LLM likelihood | risk | recommendation | required next gate |
| --- | --- | --- | --- | --- | --- | --- |
| repo-root `/graphify .` | Weak until root ignore is proven. | Weak until root output is proven absent or contained. | Low due docs. | High | Do not use. | Root scan approval plus ignore/output proof. |
| root `.graphifyignore` default-deny code-only | Potentially strong if negation works. | Still weak unless output isolated. | High if only `.py` included. | Medium-high | Defer; not first choice. | Ignore File Creation Gate plus proof. |
| safe-root docs-off | Moderate; narrower root and docs excluded. | Unproven if output lands near input. | High if metadata proves code-only. | Medium | Candidate. | Reduced-scope and output proof gate. |
| safe mirror code-only | Strongest; only approved `.py` files copied later. | Strongest if cwd/output stay in artifact area. | High. | Medium-low | Preferred first safe planning route. | Graphify Safe Mirror / Output Strategy Plan. |
| provider/auth docs run | Broad docs possible. | Unproven output plus provider exposure. | Not no-LLM. | High | Defer. | Provider/Auth Activation Decision. |
| non-Graphify map | Exact human/static scope. | No Graphify output. | No LLM required. | Low | Safe fallback. | Non-Graphify dependency map ticket. |

## 18. Recommended Next Gate
Preferred next gate: `G-11 - Graphify Safe Mirror / Output Strategy Plan`.

Alternative if governance wants a real ignore file first: `G-11 - Graphify Ignore File Creation Gate`.

Fallback if Graphify remains too risky: `G-11 - Non-Graphify Parallel Work Packet Dependency Map`.

G-10 does not start G-11. G-11 must still not run Graphify unless explicitly designed as execution proof. The first actual rerun should remain at G-12 or later.

## 19. Created / Not Created Register
| artifact/action | G-10 status | reason |
| --- | --- | --- |
| ignore/exclusion strategy document | Created | Required G-10 artifact. |
| `.gitignore` reviewed | Bounded review only | Relevant patterns checked; no modification. |
| extension counts | Checked | Metadata-only counts for `0_architecture/` and `_governed_skeleton/`. |
| `.graphifyignore` | Not created | Creation blocked by G-10. |
| `.gitignore` | Not modified | Modification blocked by G-10. |
| Graphify | Not run | Execution prohibited. |
| `/graphify .` | Not run | Explicitly prohibited. |
| safe mirror | Not created | Copy/materialization blocked. |
| provider/auth | Not configured | Blocked. |
| API key | Not added | Blocked. |
| partial outputs | Not read | G-06 raw output content remains unread. |
| output curation | Not performed | Not in scope. |
| cleanup | Not executed | Requires explicit future decision. |
| OpenCode integration | Not installed | Assistant integration blocked. |
| source tracking | Not expanded | Git/source gate required. |
| next ticket | Not started | G-10 stops before G-11. |

## 20. Residual Risk Register
| risk | current handling |
| --- | --- |
| `.graphifyignore` behavior is documented but not executed. | Future proof gate required. |
| Negation behavior may not match expectation in all cases. | Test only under future exact approval. |
| `.gitignore` merge behavior may block re-inclusion. | Do not treat ignored files as safely re-includable. |
| Output relocation remains unproven. | Recommend output strategy before execution. |
| Safe mirror not created. | Future materialization gate needed. |
| Code-only route may be too narrow. | Accept limitation or choose fallback. |
| Architecture docs remain unmapped by Graphify. | Avoid provider/auth for next attempt. |
| Provider/auth route remains high risk. | Defer unless governance explicitly chooses it. |
| No curated summary exists. | Future curation gate required after any valid run. |
| No parallel dependency map exists. | Non-Graphify fallback remains available. |

## 21. Blocker Register
Blockers retained: need ignore file creation gate; need output strategy proof; need safe mirror decision; need Graphify rerun; need output curation; need source tracking decision for any curated summary; need provider/auth if docs are included; need repo-root scan approval; need OpenCode integration decision; need Cognitive Semantic System substrate decision.

## 22. Incident Handling
Incidents include G-10 creates `.graphifyignore`; modifies `.gitignore`; runs Graphify; runs `/graphify .`; creates safe mirror; configures API key; activates provider/auth; inspects `.env`; reads Graphify source code beyond docs already reviewed; reads product/Hermes/secrets/existing `3_platform` siblings; reads partial output content; installs OpenCode integration; adopts Graphify as authority; selects Cognitive Semantic System substrate; attempts Git mutation; or starts next ticket.

Response: STOP, preserve safe metadata only, require governance/security decision.

## 23. G-10 Invariants
| ID | Invariant |
| --- | --- |
| G10-001 | Graphify Ignore / Exclusion Strategy is not Graphify execution. |
| G10-002 | No .graphifyignore file is created by G-10. |
| G10-003 | `.gitignore` is not modified by G-10. |
| G10-004 | Ignore support is not repo-root scan approval. |
| G10-005 | Repository root scan remains blocked. |
| G10-006 | `/graphify .` remains blocked. |
| G10-007 | No provider/auth configuration is authorized by G-10. |
| G10-008 | No OpenCode integration is authorized by G-10. |
| G10-009 | Partial artifacts remain local-only and unread. |
| G10-010 | Graphify remains evidence only, not authority. |
| G10-011 | Graphify repo map is not Cognitive Semantic System substrate. |
| G10-012 | Graph remains candidate only. |
| G10-013 | Cognitive Semantic System substrate remains deferred. |
| G10-014 | Existing 3_platform siblings remain uninspected and unapproved. |
| G10-015 | Product source remains local-only. |
| G10-016 | External sources remain local-only evidence. |
| G10-017 | Hermes is not inspected or adopted. |
| G10-018 | Validation evaluates; governance decides. |
| G10-019 | G-10 stops before G-11. |

## 24. Anti-patterns
Anti-patterns: `.graphifyignore` support as scan approval; default-deny draft as execution proof; ignore file as security boundary; `/graphify .` by convenience; repo-root scan by convenience; docs-off assumption without proof; Graphify output as authority; Graphify repo map as Cognitive Semantic System substrate; raw graph committed; existing `3_platform` as approved source; `git add .`; starting next ticket inside G-10.

Rejected/prohibited/historical examples only: `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth`. No such string is accepted as a current AGENT PLATFORM or Cognitive Semantic System name.

## 25. Next Ticket Recommendation
| Condition | Recommendation |
| --- | --- |
| Safe mirror is selected | `G-11 - Graphify Safe Mirror / Output Strategy Plan` |
| Root ignore file must be created first | `G-11 - Graphify Ignore File Creation Gate` |
| Graphify remains too risky | `G-11 - Non-Graphify Parallel Work Packet Dependency Map` |
| Provider/auth route is selected by governance | `G-11 - Graphify Provider/Auth Activation Decision` |

Preferred actual recommendation: `G-11 - Graphify Safe Mirror / Output Strategy Plan`.

G-10 does not start G-11.

## 26. Final Verdict
| Question | Answer |
| --- | --- |
| What did G-10 design? | A governed ignore/exclusion and containment strategy for possible future Graphify use. |
| Was `.graphifyignore` created? | No. |
| Was `.gitignore` modified? | No. |
| Was Graphify run? | No. |
| Was `/graphify .` run? | No. |
| Is repo-root scan approved? | No. Repository root scan remains blocked. |
| What is the recommended exclusion strategy? | Avoid repo-root; prefer code-only governed skeleton containment via safe mirror or future docs-off ignore proof. |
| What is the recommended first safe route? | Plan a safe mirror/output strategy before any execution. |
| What is still blocked? | Graphify execution, `.graphifyignore` creation, `.gitignore` mutation, safe mirror creation, repo-root scan, provider/auth, OpenCode integration, hooks/watch/MCP/Neo4j/URL ingestion, output curation, source tracking, product/Hermes/sibling inspection, and Cognitive Semantic System substrate selection. |
| Was provider/auth configured? | No. |
| Were partial outputs read or curated? | No. |
| Was Graphify adopted? | No. |
| Was Cognitive Semantic System substrate selected? | No. |
| Recommended next ticket? | `G-11 - Graphify Safe Mirror / Output Strategy Plan`, after explicit instruction only. |

G-10 stops here. No `.graphifyignore` file is created, `.gitignore` is not modified, no Graphify command is run, no provider/auth is configured, partial outputs remain unread and uncurated, and no next ticket is started.
