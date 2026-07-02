# G-03 - Graphify Safe Execution Plan

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Graphify Safe Execution Plan |
| Ticket | G-03 |
| Status | Accepted Graphify safe execution plan |
| Date | 2026-07-02 |
| Scope | Future exact safe execution plan for bounded Graphify read-only repo-map evidence for AGENT PLATFORM / Siamese. |
| Authority | Future execution plan only, not Graphify execution. |
| Related documents | G-00, G-01, G-02, I-A, I-06, I-07, W-series, V-series, S-series, CSS-series, `.gitignore`, README.md |
| Decision target | Future exact Graphify safe run plan |

## 2. Purpose
G-02 defined the Graphify read-only repo-map gate. G-03 defines the exact future execution plan required before a run can be considered.

G-03 does not run Graphify. G-03 does not install Graphify. G-03 does not create outputs. G-03 does not start G-04.

## 3. Current Graphify Status
| Status item | Current G-03 posture |
| --- | --- |
| Installation | Graphify is not installed by this ticket. |
| Execution | Graphify is not run by this ticket. |
| Adoption | Graphify is not adopted. |
| OpenCode integration | Graphify OpenCode integration is not installed. |
| Outputs | No Graphify output exists from G-03. |
| Output authority | Future Graphify output remains generated evidence only. |
| Gate bypass | Graphify cannot bypass gates. |

## 4. Safe Execution Plan Definition
A Graphify safe execution plan is a governance document that names the future owner, command candidates, allowed input roots, excluded paths, cwd, output path, generated artifact posture, cleanup plan, validation checks, and stop rules required before any Graphify command can be executed.

The execution plan is not execution. It is not installation, dependency adoption, OpenCode integration, source tracking approval, Cognitive Semantic System substrate selection, or Graphify adoption.

## 5. Execution Authority Boundary
| Authority layer | Boundary |
| --- | --- |
| Governance | Must approve any future Graphify run. |
| Security | Must approve input, exclusion, and output posture. |
| Validation | Evaluates generated outputs as evidence only. |
| Git | Does not track raw outputs by default. |
| Human owner | Mandatory before any run. |
| AI agents | Cannot be sole final approver. |
| Graphify output | Cannot authorize edits, activation, source tracking, or substrate selection. |

## 6. Recommended Future Run Strategy
Preferred strategy: safe-root one-shot scans, not repo-root scan.

Future candidate runs are: scan `0_architecture/` as one safe root; scan `3_platform/_governed_skeleton/` as one safe root; do not scan repo root; do not scan `3_platform/` parent; do not scan `4_external/sources/`; do not scan `2_products/`.

Safe mirror strategy is deferred because it requires copying files. Safe roots are simpler and lower risk. G-03 does not perform either strategy.

## 7. Future Candidate Commands
Every command in this section is NOT AUTHORIZED BY G-03 — FOR FUTURE G-04 ONLY.

Candidate architecture safe-root command:

```powershell
graphify .\0_architecture --no-viz
```

Candidate governed-skeleton safe-root command:

```powershell
graphify .\3_platform\_governed_skeleton --no-viz
```

Forbidden commands:

```powershell
graphify .
```

```powershell
/graphify .
```

```powershell
graphify install
```

```powershell
graphify opencode install
```

```powershell
graphify . --watch
```

Any MCP, Neo4j push, hooks, URL ingestion, OpenCode install, project install, or root scan command is forbidden by G-03.

## 8. Future Working Directory Plan
Future commands must be launched from repo root only if command paths are exact safe roots. Future commands must not use repo root as Graphify input. CWD must be recorded in the future run record.

Environment must be recorded as no-provider/no-auth/no-network unless explicitly approved. No environment variables may be read or used by G-03. If Graphify requires provider credentials or external model calls, the future run must STOP unless separately approved.

## 9. Safe Input Scope
Approved future candidate input roots: `0_architecture/` and `3_platform/_governed_skeleton/`.

Approved file only: `README.md`, only if future G-04 explicitly includes it.

Excluded paths: repo root as direct input; `2_products/`; `4_external/sources/`; `previusknowledge/`; `7_datasets/`; `8_models/`; `9_artifacts/` except approved output path; `.git/`; `.env`; `.env*`; secrets; credentials; provider configs; dependency folders; runtime caches; existing `3_platform` siblings outside `_governed_skeleton`; product source; external source; Hermes source; Graphify source; unknown-sensitivity paths.

## 10. Future Output Plan
Future output root: `9_artifacts/graphify/<run_id>/`.

Run ID patterns: `graphify_architecture_<YYYYMMDD_HHMMSS>` and `graphify_governed_skeleton_<YYYYMMDD_HHMMSS>`.

Expected future outputs: `graph.html`, `GRAPH_REPORT.md`, `graph.json`, and `cache/`.

Output posture: local-only; generated-sensitive by default; not trackable by default; not source; not truth; not governance decision; not CSS substrate; not input to agents until curated.

## 11. Future Curated Summary Plan
Future curated summary target: `0_architecture/governance/agent_platform_graphify_repo_map_summary.md`.

Rules: created only after Graphify output review; human-reviewed; no raw graph dump; no secrets; no local-only raw content; no product source; no external source; no unapproved `3_platform` sibling content; exact-path review required before tracking; summary remains evidence, not authority.

## 12. Future Workstream Dependency Map Plan
Possible future target: `0_architecture/governance/agent_platform_parallel_workstream_dependency_map.md`.

Purpose: identify workstreams, path ownership, dependencies, and collision risks, and support OpenCode parallel sessions.

Rules: curated from reviewed evidence; cannot be raw Graphify output; cannot assign authority automatically; cannot authorize edits automatically.

## 13. Future Execution Record Template
| Field | Current G-03 value |
| --- | --- |
| run_id | Not approved; pending G-04. |
| owner | Not approved; pending G-04. |
| requester | Not approved; pending G-04. |
| purpose | Not approved; pending G-04. |
| command | Not approved; pending G-04. |
| cwd | Not approved; pending G-04. |
| input_paths | Not approved; pending G-04. |
| excluded_paths | Not approved; pending G-04. |
| output_path | Not approved; pending G-04. |
| expected_outputs | Not approved; pending G-04. |
| dependency_posture | Not approved; pending G-04. |
| network_posture | Not approved; pending G-04. |
| auth_posture | Not approved; pending G-04. |
| assistant_integration_posture | Not approved; pending G-04. |
| generated_artifact_posture | Not approved; pending G-04. |
| validation_plan | Not approved; pending G-04. |
| security_review | Not approved; pending G-04. |
| rollback_plan | Not approved; pending G-04. |
| decision_status | Not approved; pending G-04. |

## 14. Pre-run Checklist For G-04
Required before any future run: human owner named; Graphify availability known without install or dependency gate approved; exact command approved; exact cwd approved; exact input paths approved; exact exclusions approved; output path approved; no repo-root scan; no OpenCode integration; no `AGENTS.md`; no hooks; no watch; no MCP; no external source scan; no product source scan; no secrets/credentials scan; no existing `3_platform` sibling scan; rollback plan exists; validation plan exists; security review exists.

## 15. Post-run Checklist For G-04
Required after any future run: command log captured; actual output path recorded; unexpected files checked; no `AGENTS.md` created; no `.agents/`, `.claude/`, or `.codex/` created; no `graphify-out/` at repo root; no forbidden paths included; generated outputs quarantined/local-only; no Git staging; no publication; output reviewed before use.

## 16. Rollback / Cleanup Plan
If a future run is invalid, delete or quarantine the future output directory. Delete unexpected `graphify-out/` only under the future approved cleanup scope. Delete unexpected assistant config artifacts only after human approval.

Record an incident if forbidden paths were scanned or outputs include sensitive material. Do not modify `.gitignore` in G-03. Do not run cleanup commands in G-03.

## 17. Security Review Plan
Generated outputs are sensitive until reviewed. No secrets or credentials are allowed in inputs. Product, external, and raw local-only source are not allowed. Unknown sensitivity blocks.

Outputs must be reviewed before agent consumption. Publication is blocked. Raw output tracking is blocked.

## 18. Validation Plan
Allowed future validation classes: path existence checks, output file existence checks, command log review, output location review, forbidden artifact existence checks, curated summary review, and no semantic truth validation by Graphify alone.

G-03 runs no validation beyond document/path metadata checks. G-04 may run exact validation checks if approved.

## 19. Dependency / Installation Boundary
G-03 does not install Graphify. If Graphify is not available, a future run stops unless a dependency gate approves install.

The `graphifyy` package fact is not adoption. Existing global availability is not permission. Package managers are not run by G-03. Graphify dependency review remains separate unless already approved.

## 20. OpenCode Integration Boundary
No `graphify opencode install`. No `/graphify` slash-command execution. No assistant config mutation. No `AGENTS.md`. No `.agents/`, `.claude/`, or `.codex/`. No always-on Graphify behavior.

Initial run must be terminal-style CLI only if future G-04 approves it. OpenCode Graphify integration is not installed. OpenCode integration remains a separate future gate.

## 21. Relation To Cognitive Semantic System
Graphify repo map is not CSS substrate. Graphify output is not semantic memory. Graph remains candidate only. Graphify remains evidence only, not authority. Cognitive Semantic System substrate remains deferred.

Future CSS gate may consider curated Graphify findings as evidence only.

## 22. Relation To Parallel OpenCode Sessions
Graphify may later support parallelization by producing dependency evidence. Agents consume curated summaries, not raw graph dumps. Graphify evidence may inform work packets and path ownership.

Graphify evidence cannot assign path ownership automatically. Path ownership requires governance/work-packet decision. No parallel session is started by G-03.

## 23. Relation To Hermes
Hermes is not inspected. Hermes is not scanned. Hermes is not adopted. Graphify must not scan Hermes in the first safe run. Hermes evaluation remains a separate gate.

## 24. Relation To Existing 3_platform
Existing `3_platform` siblings remain uninspected and unapproved. A future Graphify run must not scan siblings. Scanning `_governed_skeleton/` does not approve siblings. Sibling classification remains a separate gate.

## 25. Relation To Product And External Source
Product source remains local-only. External source remains local-only. A future Graphify run must not scan product or external source. Product or external inclusion requires separate gates.

## 26. Created / Not Created Register
| Artifact/action | G-03 status | Reason |
| --- | --- | --- |
| Safe execution plan | Created | Required G-03 artifact. |
| Graphify install | Not installed | Dependency boundary. |
| Graphify run | Not run | Execution not authorized. |
| Graphify output | Not created | Output creation blocked. |
| Graphify cache | Not created | Cache output blocked. |
| Safe mirror | Not created | Copying files blocked. |
| OpenCode integration | Not installed | Assistant config mutation blocked. |
| `AGENTS.md` | Not created | Integration blocked. |
| Hooks/watch/MCP | Not created | Runtime/MCP behavior blocked. |
| Source tracking | Not expanded | Git gate required. |
| G-04 | Not started | Explicit instruction required. |

## 27. Residual Risk Register
| Risk | Current handling |
| --- | --- |
| Graphify availability unknown | Future G-04 or dependency gate must decide. |
| Graphify may require dependency review | Install remains blocked. |
| Future output may be sensitive | Local-only/generated-sensitive by default. |
| Future command may scan too broadly if path wrong | Safe-root exact command approval required. |
| Future output may be over-trusted | Evidence-only labels required. |
| No curated summary yet | G-05 candidate only. |
| No workstream dependency map yet | G-06 candidate only. |
| No parallel session ownership model yet | Governance/work-packet decision required. |
| No G-04 execution approval yet | Graphify remains not executable. |

## 28. Blocker Register
Blockers: need to run Graphify; need to install Graphify; need dependency review; need exact owner; need exact command approval; need output directory creation; need safe mirror creation; need output curation; need OpenCode integration; need repo-root scan; need product scan; need external scan; need existing `3_platform` sibling scan; need raw output tracking; need CSS substrate decision; need Graphify adoption.

## 29. Incident Handling
Incidents include Graphify run during G-03; Graphify install during G-03; output created during G-03; safe mirror created during G-03; repo-root scan performed; forbidden path scanned; OpenCode integration installed; `AGENTS.md` or assistant config created; hooks/watch/MCP activated; product/external/secrets scanned; existing `3_platform` sibling inspected; Graphify adopted as authority; CSS substrate selected; Git mutation attempted; G-04 started.

Response: STOP, report safe metadata only, require governance/security decision.

## 30. G-03 Invariants
| ID | Invariant |
| --- | --- |
| G03-001 | Graphify safe execution plan is not Graphify execution. |
| G03-002 | Graphify is not installed by G-03. |
| G03-003 | Graphify is not run by G-03. |
| G03-004 | Graphify output is not created by G-03. |
| G03-005 | Safe mirror is not created by G-03. |
| G03-006 | OpenCode Graphify integration is not installed. |
| G03-007 | Future Graphify output is generated evidence, not authority. |
| G03-008 | Graphify repo map is not CSS substrate. |
| G03-009 | Graph remains candidate only. |
| G03-010 | Graphify remains evidence only, not authority. |
| G03-011 | Cognitive Semantic System substrate remains deferred. |
| G03-012 | Existing 3_platform siblings remain uninspected and unapproved. |
| G03-013 | Product source remains local-only. |
| G03-014 | External sources remain local-only. |
| G03-015 | Hermes is not inspected or adopted. |
| G03-016 | No broad source tracking is approved. |
| G03-017 | Validation evaluates; governance decides. |
| G03-018 | G-03 stops before G-04. |

## 31. Anti-patterns
Anti-patterns: plan as execution; candidate command as authorization; Graphify output as authority; Graphify repo map as CSS substrate; Graphify usefulness as Graphify adoption; safe-root scan expanded to repo-root scan; safe mirror created without gate; OpenCode install by convenience; generated output consumed without curation; raw graph committed; existing `3_platform` as approved source; `git add .`; starting G-04 inside G-03.

Rejected/prohibited/historical examples only: `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth`. No such string is accepted as a current AGENT PLATFORM or Cognitive Semantic System name.

## 32. Next Ticket Recommendation
Recommended next ticket: G-04 — Graphify Safe Run.

Alternative: G-04 — Graphify Dependency / Availability Check, if Graphify availability is unknown and dependency posture must be separated before run.

Recommended sequence: 1. G-02 Graphify Read-only Repo Map Gate; 2. G-03 Graphify Safe Execution Plan; 3. G-04 Graphify Safe Run; 4. G-05 Graphify Output Curation; 5. G-06 Parallel Work Packet Dependency Map; 6. G-A Governance / Graphify Audit.

G-03 does not start G-04.

## 33. Final Verdict
| Question | Answer |
| --- | --- |
| What does G-03 define? | The future safe execution plan for exact Graphify repo-map runs. |
| Does G-03 run Graphify? | No. |
| Does G-03 install Graphify? | No. |
| Does G-03 create output? | No. |
| Does G-03 create a safe mirror? | No. |
| Does G-03 install OpenCode integration? | No. |
| Does G-03 authorize repo-root scan? | No. |
| Does G-03 inspect product/external/secrets/3_platform siblings? | No. |
| Does G-03 adopt Graphify? | No. |
| Does G-03 select CSS substrate? | No. |
| What remains blocked? | Graphify execution, install, dependency adoption, output creation, safe mirror, OpenCode integration, repo-root scan, forbidden path scans, raw output tracking, source tracking expansion, product/external/secrets/3_platform sibling inspection, Graphify adoption, Hermes adoption, CSS substrate selection, staging, commit, push, publish, and G-04. |
| What is the next recommended ticket? | G-04 — Graphify Safe Run, or dependency/availability check first if needed. |
