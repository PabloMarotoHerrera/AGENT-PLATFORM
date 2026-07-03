# G-12 - Graphify Safe Mirror Materialization Gate

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Graphify Safe Mirror Materialization Gate |
| Ticket | G-12 |
| Status | Accepted Graphify safe mirror materialization gate |
| Date | 2026-07-03 |
| Scope | Materialize a local-only generated code-only mirror for possible future Graphify evidence use in AGENT PLATFORM / Siamese. |
| Authority | Safe mirror materialization only, not Graphify execution, provider/auth, output curation, source tracking, or Cognitive Semantic System substrate selection. |
| Related documents | G-00 through G-11, I-A, I-06, I-07, S-series, CSS-series, `.gitignore`, README.md. |
| Materialization target | Local-only code-only mirror under `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/`. |

## 2. Purpose
G-11 planned the safe mirror topology and output containment strategy. G-12 materializes the mirror only. G-12 copies only the seven approved `.py` files from `3_platform/_governed_skeleton/` into a generated local-only input mirror under `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/input/`.

G-12 does not run Graphify. G-12 does not create Graphify outputs. G-12 does not create `graphify-out/`. G-12 does not configure provider/auth. G-12 does not create `.graphifyignore`. G-12 does not modify `.gitignore`. G-12 does not start G-13.

## 3. Evidence Basis
| Evidence | G-12 use |
| --- | --- |
| G-09 confirmed code-only AST extraction can avoid API calls if the corpus is code-only. | Mirror input is limited to Python code files only. |
| G-10 recommended safe mirror containment as the preferred first route. | Materialization uses `9_artifacts/graphify/<run_id>/`. |
| G-11 selected exactly seven `.py` files and planned mirror topology. | G-12 copied exactly that source set. |
| G-11 kept Graphify execution for G-13 or later. | G-12 performs no Graphify command. |
| `.gitignore` ignores `9_artifacts/`. | Mirror remains local-only and not trackable by default. |
| G-06 failed on provider/auth for document files. | G-12 excludes Markdown and other non-code inputs. |

## 4. Materialization Boundary
A Graphify safe mirror materialization gate creates a local-only generated copy of explicitly approved files for future possible execution, while preserving original source directories and avoiding any Graphify run.

Materialization is not execution. The mirror is not source. The mirror is not authority. The mirror is not source tracking expansion. The mirror is not output curation. The mirror is not Graphify adoption. The mirror is not Cognitive Semantic System substrate.

## 5. Run ID / Mirror Record
| Field | Value |
| --- | --- |
| run_id | `graphify_safe_mirror_20260703_120000` |
| mirror_root | `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/` |
| input_root | `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/input/governed_skeleton_code_only/` |
| work_root | `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/work/` |
| output_check_root | `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/output_check/` |
| local_notice_path | `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/README.local-only.txt` |
| source_set | Seven approved `.py` files from `3_platform/_governed_skeleton/`. |
| copied_file_count | 7 |
| expected_extension_set | `.py` only |
| graphify_execution_status | Not run by G-12. |
| provider_auth_status | Not configured; not activated. |
| output_status | No Graphify output created; no `graphify-out/` created. |
| source_tracking_status | Not expanded; mirror is ignored/local-only under `9_artifacts/`. |
| decision_status | Materialization accepted; execution remains blocked until G-13 or later. |

## 6. Approved Source Set
No source file contents were opened for G-12. Metadata only was used.

| Source path | Target path | Extension | Source length | Target exists? | Copied? |
| --- | --- | --- | --- | --- | --- |
| `3_platform/_governed_skeleton/agents/runtime_boundary/agent_runtime_boundary.py` | `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/input/governed_skeleton_code_only/3_platform/_governed_skeleton/agents/runtime_boundary/agent_runtime_boundary.py` | `.py` | 22878 | True | True |
| `3_platform/_governed_skeleton/cognitive_semantic_system/prototype/cognitive_semantic_system_prototype.py` | `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/input/governed_skeleton_code_only/3_platform/_governed_skeleton/cognitive_semantic_system/prototype/cognitive_semantic_system_prototype.py` | `.py` | 19796 | True | True |
| `3_platform/_governed_skeleton/context/runtime/context_pack_runtime.py` | `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/input/governed_skeleton_code_only/3_platform/_governed_skeleton/context/runtime/context_pack_runtime.py` | `.py` | 16657 | True | True |
| `3_platform/_governed_skeleton/integrations/provider_adapter_layer/provider_adapter_layer.py` | `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/input/governed_skeleton_code_only/3_platform/_governed_skeleton/integrations/provider_adapter_layer/provider_adapter_layer.py` | `.py` | 18368 | True | True |
| `3_platform/_governed_skeleton/security/access_enforcement/security_access_enforcement.py` | `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/input/governed_skeleton_code_only/3_platform/_governed_skeleton/security/access_enforcement/security_access_enforcement.py` | `.py` | 11942 | True | True |
| `3_platform/_governed_skeleton/tools/execution_boundary/tool_execution_boundary.py` | `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/input/governed_skeleton_code_only/3_platform/_governed_skeleton/tools/execution_boundary/tool_execution_boundary.py` | `.py` | 26205 | True | True |
| `3_platform/_governed_skeleton/validation/registry/validation_registry.py` | `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/input/governed_skeleton_code_only/3_platform/_governed_skeleton/validation/registry/validation_registry.py` | `.py` | 6577 | True | True |

Exactly seven Python files were copied.

## 7. Materialized Mirror Topology
```text
9_artifacts/graphify/graphify_safe_mirror_20260703_120000/
  README.local-only.txt
  input/
    governed_skeleton_code_only/
      3_platform/
        _governed_skeleton/
          agents/runtime_boundary/agent_runtime_boundary.py
          cognitive_semantic_system/prototype/cognitive_semantic_system_prototype.py
          context/runtime/context_pack_runtime.py
          integrations/provider_adapter_layer/provider_adapter_layer.py
          security/access_enforcement/security_access_enforcement.py
          tools/execution_boundary/tool_execution_boundary.py
          validation/registry/validation_registry.py
  work/
  output_check/
```

`work/` exists only as a future cwd candidate. `output_check/` exists only as a future metadata/check location if later approved.

## 8. Mirror Validation
| Check | Result |
| --- | --- |
| Extension count under input mirror | `.py`: 7 |
| Total file count under input mirror | 7 |
| Expected `.py` count | 7 |
| Forbidden file type check result | No files returned; non-Python file count 0. |
| `.md`, `.rst`, `.txt` under input mirror | Absent. |
| `.json`, `.yaml`, `.toml`, `.env` under input mirror | Absent. |
| `.pyc`, cache, output files under input mirror | Absent. |
| Dataset, model, product, external, assistant config, or credential files under input mirror | Absent. |
| repo-root `graphify-out/` | Absent. |
| live `3_platform/_governed_skeleton/graphify-out/` | Absent. |
| mirror input `graphify-out/` | Absent. |
| mirror `work/graphify-out/` | Absent. |
| `.graphifyignore` | Absent. |
| `AGENTS.md`, `.agents/`, `.claude/`, `.codex/` | Absent. |

Safe mirror is local-only generated input materialization.

## 9. Local-Only Notice
`README.local-only.txt` states that the directory is a local-only generated Graphify safe mirror materialized by G-12. It states the mirror is not source, not authority, not source tracking expansion, not Cognitive Semantic System substrate, must not be committed, must not be consumed by agents as source, and that Graphify has not been run by G-12.

The first notice creation attempt failed due command-shell here-string quoting. The second and final allowed `Set-Content` attempt succeeded. No second creation failure occurred.

## 10. Output Containment Preflight
G-12 creates no Graphify output. `work/` exists only as a future cwd candidate. `output_check/` exists only as future metadata/check location.

No `graphify-out/` exists at repo root. No `graphify-out/` exists under live source. No `graphify-out/` exists under mirror input or mirror work roots before execution. Future G-13 must stop if output escapes `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/`.

## 11. Graphify Execution Boundary
No Graphify command is run by G-12. No `/graphify .` is run by G-12. No repo-root scan is approved. No safe-root scan is approved. No mirror execution is approved by G-12. G-13 or later must authorize any execution explicitly.

Repository root scan remains blocked.

## 12. Provider / Auth Boundary
No API key usage is approved. No `.env` is inspected. No credentials are inspected. No provider/auth/model endpoint is activated. Future execution must stop on any provider/auth/API-key/model prompt.

## 13. Git / Source Tracking Boundary
The mirror is under `9_artifacts/`, local-only by default, and ignored by `.gitignore`. The mirror must not be committed. Graphify outputs must not be committed. G-12 does not force-add ignored files. Only the G-12 governance record may be considered for exact-path commit after human approval. `git add .` remains prohibited.

## 14. Partial Artifact Boundary
G-06 partial artifacts remain local-only. G-12 does not read or curate partial outputs. G-12 does not delete partial artifacts. G-12 does not track partial artifacts.

## 15. Cognitive Semantic System Boundary
Safe mirror materialization does not affect Cognitive Semantic System substrate decision. Graph remains candidate only. Graphify remains evidence only, not authority. Cognitive Semantic System substrate remains deferred. No graph, vector database, ontology database, or runtime is created.

## 16. Created / Not Created Register
| Artifact/action | G-12 status | Reason |
| --- | --- | --- |
| governance document | Created | Required G-12 record. |
| run root | Created | Required mirror root. |
| `README.local-only.txt` | Created | Required local-only notice. |
| input mirror | Created | Required code-only mirror. |
| `work/` dir | Created | Future cwd candidate only. |
| `output_check/` dir | Created | Future metadata/check location only. |
| exactly seven `.py` files copied | Completed | Approved source set only. |
| Graphify | Not run | Execution prohibited by G-12. |
| `/graphify .` | Not run | Repository root scan remains blocked. |
| `graphify-out/` | Not created | Outputs prohibited by G-12. |
| `.graphifyignore` | Not created | Ignore config creation blocked. |
| `.gitignore` | Not modified | Git ignore mutation blocked. |
| provider/auth | Not configured | Provider/auth blocked. |
| API key | Not added | Credential use blocked. |
| partial outputs | Not read | G-06 artifacts remain unread. |
| output curation | Not performed | Curation gate required later. |
| cleanup | Not executed | Cleanup policy deferred. |
| OpenCode integration | Not installed | Assistant integration blocked. |
| source tracking | Not expanded | Git/source tracking gate required. |
| G-13 | Not started | G-12 stops before G-13. |

## 17. Residual Risk Register
| Risk | Current handling |
| --- | --- |
| Mirror may become stale relative to source. | Future execution gate must re-check source metadata or rematerialize. |
| Code-only mirror omits architecture Markdown context. | Accepted for no-provider first proof; use fallback if too narrow. |
| Graphify may still unexpectedly request provider/auth. | Future execution must hard stop. |
| Output behavior remains unproven until execution. | G-13 must prove containment. |
| Raw future output may be sensitive. | Generated/local-only by default. |
| No curated summary exists. | Curation gate required after any valid output. |
| No parallel dependency map exists. | Non-Graphify fallback remains available. |
| Provider/auth route remains high risk. | Deferred. |
| Repo-root scan remains blocked. | No root scan approval by G-12. |

## 18. Blocker Register
Blockers retained: need Graphify safe mirror execution gate; need output containment proof; need output curation gate; need source tracking decision for any curated summary; need cleanup policy for mirror/artifacts; need provider/auth if docs are included; need repo-root scan approval; need OpenCode integration decision; need Cognitive Semantic System substrate decision.

## 19. Incident Handling
Incidents include G-12 runs Graphify; runs `/graphify .`; creates `graphify-out/`; copies any file outside the seven approved `.py` files; copies docs, secrets, products, external sources, Hermes source, Graphify source, datasets, models, caches, or assistant config; creates `.graphifyignore`; modifies `.gitignore`; configures provider/auth; inspects `.env`; reads secrets or credentials; reads product source; reads Hermes source; reads Graphify implementation source; opens existing `3_platform` sibling contents; reads, parses, summarizes, curates, deletes, or tracks Graphify partial outputs; installs OpenCode integration; adopts Graphify as authority; selects Cognitive Semantic System substrate; attempts Git mutation; or starts G-13.

Response: STOP, preserve safe metadata only, require governance/security decision.

## 20. G-12 Invariants
| ID | Invariant |
| --- | --- |
| G12-001 | Graphify Safe Mirror Materialization Gate is not Graphify execution. |
| G12-002 | Safe mirror is local-only generated input materialization. |
| G12-003 | Exactly seven Python files were copied. |
| G12-004 | No non-Python files were copied under the input mirror. |
| G12-005 | No Graphify command is run by G-12. |
| G12-006 | No `graphify-out/` is created by G-12. |
| G12-007 | `.graphifyignore` is not created by G-12. |
| G12-008 | `.gitignore` is not modified by G-12. |
| G12-009 | Repository root scan remains blocked. |
| G12-010 | `/graphify .` remains blocked. |
| G12-011 | No provider/auth configuration is authorized by G-12. |
| G12-012 | No OpenCode integration is authorized by G-12. |
| G12-013 | Partial artifacts remain local-only and unread. |
| G12-014 | Graphify remains evidence only, not authority. |
| G12-015 | Graphify repo map is not Cognitive Semantic System substrate. |
| G12-016 | Graph remains candidate only. |
| G12-017 | Cognitive Semantic System substrate remains deferred. |
| G12-018 | Existing 3_platform siblings remain uninspected and unapproved. |
| G12-019 | Product source remains local-only. |
| G12-020 | External sources remain local-only evidence. |
| G12-021 | Hermes is not inspected or adopted. |
| G12-022 | Validation evaluates; governance decides. |
| G12-023 | G-12 stops before G-13. |

## 21. Anti-patterns
Anti-patterns: mirror as source; materialization as execution approval; copied files as source tracking expansion; running Graphify by convenience after mirror creation; treating code-only mirror as architecture map; using `--no-viz` as no-LLM control; placing `graphify-out/` at repo root; placing output under live source; reading partial artifacts before curation gate; committing mirror or raw generated output; treating Graphify as authority; treating Graphify repo map as Cognitive Semantic System substrate; selecting graph substrate because Graphify exists; `git add .`; starting G-13 inside G-12.

Rejected/prohibited/historical examples only: `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth`. No such string is accepted as a current AGENT PLATFORM, Siamese, or Cognitive Semantic System name.

## 22. Next Ticket Recommendation
Preferred: `G-13 - Graphify Safe Mirror Code-Only Run`.

Fallback: `G-13 - Non-Graphify Parallel Work Packet Dependency Map`.

Alternative if materialization is later judged invalid: `G-13 - Graphify Safe Mirror Materialization Failure Review`.

G-12 does not start G-13.

## 23. Final Verdict
| Question | Answer |
| --- | --- |
| What did G-12 create? | The G-12 governance record, run root, local-only notice, input mirror, `work/`, and `output_check/`. |
| What run ID was used? | `graphify_safe_mirror_20260703_120000`. |
| Where is the mirror? | `9_artifacts/graphify/graphify_safe_mirror_20260703_120000/`. |
| Which files were copied? | The seven approved `.py` files listed in Section 6. |
| How many files were copied? | 7. |
| Were any non-Python files copied under input? | No. |
| Was Graphify run? | No. |
| Was `/graphify .` run? | No. |
| Was `graphify-out/` created? | No. |
| Was `.graphifyignore` created? | No. |
| Was `.gitignore` modified? | No. |
| Was provider/auth configured? | No. |
| Were partial outputs read or curated? | No. |
| Was Graphify adopted? | No. |
| Was Cognitive Semantic System substrate selected? | No. |
| What remains blocked? | Graphify execution, repo-root scan, provider/auth, output curation, source tracking expansion, OpenCode integration, partial output review, product/Hermes/sibling inspection, graph adoption, Graphify authority, and Cognitive Semantic System substrate selection. |
| What is the recommended next ticket? | `G-13 - Graphify Safe Mirror Code-Only Run`, after explicit instruction only. |

G-12 stops here. The safe mirror is materialized as local-only generated input. No Graphify command is run, no `/graphify .` command is run, no `graphify-out/` is created, no provider/auth is configured, no partial outputs are read or curated, and G-13 is not started.
