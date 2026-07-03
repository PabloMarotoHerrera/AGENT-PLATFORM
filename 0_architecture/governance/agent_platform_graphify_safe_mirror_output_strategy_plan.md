# G-11 - Graphify Safe Mirror / Output Strategy Plan

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Graphify Safe Mirror / Output Strategy Plan |
| Ticket | G-11 |
| Status | Accepted Graphify safe mirror / output strategy plan |
| Date | 2026-07-03 |
| Scope | Plan a future code-only safe mirror and output containment strategy for possible Graphify use in AGENT PLATFORM / Siamese. |
| Authority | Strategy only, not mirror creation, file copying, Graphify execution, provider/auth, output curation, source tracking, or Cognitive Semantic System substrate selection. |
| Related documents | G-07 through G-10, I-A, I-06, I-07, S-series, CSS-series, `.gitignore`, README.md. |
| Strategy target | Future safe mirror materialization and output isolation under `9_artifacts/graphify/`. |

## 2. Purpose
G-10 selected a safe mirror code-only route as the preferred first planning route because repo-root scanning remains too broad, architecture Markdown can trigger provider/auth, `.graphifyignore` behavior is not execution proof, and default Graphify output placement remains unresolved.

G-11 defines the future mirror topology, input selection, output containment checks, stop conditions, and required next gate. G-11 does not create a safe mirror. G-11 does not copy files. G-11 does not run Graphify. G-11 does not create `.graphifyignore`. G-11 does not modify `.gitignore`. G-11 does not configure provider/auth. G-11 does not inspect product source, Hermes source, Graphify implementation source, or existing `3_platform` siblings outside `_governed_skeleton`.

## 3. Evidence Basis
| Evidence | G-11 use |
| --- | --- |
| G-07 recorded the G-06 failure as `provider_auth_required_by_graphify` for 87 document files. | Future route must avoid documentation inputs and provider/auth assumptions. |
| G-08 found no confirmed general no-LLM/offline full extraction switch from CLI help. | Do not rely on a no-LLM flag. |
| G-09 local documentation review confirmed code-only AST extraction can avoid API calls if the corpus is code-only. | A code-only mirror is a plausible future route. |
| G-09 also confirmed default `graphify-out/` behavior and partial output relocation evidence only. | Output containment needs its own plan and path checks. |
| G-10 recommended safe mirror code-only containment before any rerun. | G-11 plans that route without materializing it. |
| `.gitignore` exists and ignores product, external source, previous knowledge, datasets, models, artifacts, secrets, credentials, and token-like files. | Existing ignore posture helps but is not the safety boundary. |
| `.graphifyignore` is absent. | No Graphify ignore file is applied by G-11. |
| repo-root `graphify-out/` is absent. | Root output remains forbidden and currently absent. |
| `AGENTS.md`, `.agents/`, `.claude/`, and `.codex/` are absent. | Assistant integration remains blocked and currently absent. |

## 4. Current Metadata Snapshot
G-11 collected only allowed metadata. No file contents under `3_platform/_governed_skeleton/` were opened.

| Path / check | Result |
| --- | --- |
| `.gitignore` | Exists. |
| README.md | Exists. |
| `.graphifyignore` | Absent. |
| G-11 target file before creation | Absent. |
| G-10 strategy document | Exists. |
| `0_architecture/` | Exists. |
| `3_platform/_governed_skeleton/` | Exists. |
| `9_artifacts/` | Exists. |
| repo-root `graphify-out/` | Absent. |
| `3_platform/_governed_skeleton/graphify-out/` | Absent. |
| `AGENTS.md` | Absent. |
| `.agents/` | Absent. |
| `.claude/` | Absent. |
| `.codex/` | Absent. |
| `9_artifacts/graphify/graphify_safe_run_20260702_153000/` | Exists. |
| `9_artifacts/graphify/graphify_safe_run_20260702_153000/architecture/` | Exists. |
| `9_artifacts/graphify/graphify_safe_run_20260702_153000/architecture/graphify-out/` | Absent. |

`3_platform/_governed_skeleton/` extension counts: `.md` 32 and `.py` 7.

## 5. Candidate Code-Only Input Set
The future mirror input set is limited to the observed Python files below. The table records metadata only. It does not approve content semantics, source tracking, execution, or Graphify adoption.

| FullName | Name | Extension | Length |
| --- | --- | --- | --- |
| `3_platform/_governed_skeleton/agents/runtime_boundary/agent_runtime_boundary.py` | `agent_runtime_boundary.py` | `.py` | 22878 |
| `3_platform/_governed_skeleton/cognitive_semantic_system/prototype/cognitive_semantic_system_prototype.py` | `cognitive_semantic_system_prototype.py` | `.py` | 19796 |
| `3_platform/_governed_skeleton/context/runtime/context_pack_runtime.py` | `context_pack_runtime.py` | `.py` | 16657 |
| `3_platform/_governed_skeleton/integrations/provider_adapter_layer/provider_adapter_layer.py` | `provider_adapter_layer.py` | `.py` | 18368 |
| `3_platform/_governed_skeleton/security/access_enforcement/security_access_enforcement.py` | `security_access_enforcement.py` | `.py` | 11942 |
| `3_platform/_governed_skeleton/tools/execution_boundary/tool_execution_boundary.py` | `tool_execution_boundary.py` | `.py` | 26205 |
| `3_platform/_governed_skeleton/validation/registry/validation_registry.py` | `validation_registry.py` | `.py` | 6577 |

Markdown files under `_governed_skeleton` are deliberately excluded from the first future Graphify mirror route because documentation inputs can trigger semantic extraction and provider/auth requirements. Architecture Markdown is also excluded from the next Graphify attempt.

## 6. Recommended Future Run ID
Future safe mirror runs should use this convention:

```text
graphify_safe_mirror_<YYYYMMDD_HHMMSS>
```

The run ID must be selected by the future materialization gate. G-11 does not allocate or create a concrete run directory.

## 7. Unapplied Safe Mirror Topology
The preferred future topology is below. It is a plan only. No directories or files are created by G-11.

```text
9_artifacts/graphify/<run_id>/
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

The mirror preserves enough relative path context to keep Graphify evidence interpretable while avoiding a scan of the live source tree. It intentionally contains only copied `.py` files from the approved metadata set and no Markdown, docs, datasets, models, product files, external sources, secrets, credentials, generated artifacts, assistant config, or existing `3_platform` siblings.

## 8. Future Materialization Rules
G-12 should be a materialization gate, not a Graphify execution gate, unless governance explicitly changes that boundary.

Future materialization should:

| Rule | Requirement |
| --- | --- |
| Parent path | Only under `9_artifacts/graphify/<run_id>/`. |
| Input source | Only the seven `.py` files listed in Section 5. |
| Input exclusion | Exclude all `.md`, `.rst`, `.txt`, notebooks, images, PDFs, datasets, models, product files, external source files, generated outputs, secrets, credentials, env files, and assistant config. |
| Tree shape | Preserve relative paths under `3_platform/_governed_skeleton/` inside the mirror. |
| Local notice | Add only a local-only notice such as `README.local-only.txt` if G-12 authorizes it. |
| Verification | Count files and extensions in the mirror before any execution ticket. |
| No execution | Do not run Graphify during G-12 unless a later instruction explicitly redefines G-12 as execution. |

If any expected source file is missing, duplicated, unexpectedly renamed, or has an unexpected extension during future materialization, stop and require a governance decision.

## 9. Output Containment Strategy
Default Graphify output uses `graphify-out/`. Root `graphify-out/` is forbidden. Output under live source directories is undesirable. Output under `9_artifacts/graphify/<run_id>/` is the required containment objective.

Preferred future execution working directory, if a later gate approves execution:

```text
9_artifacts/graphify/<run_id>/work/
```

Expected output containment checks after any future approved execution:

| Path | Required posture |
| --- | --- |
| `graphify-out/` at repo root | Must remain absent. |
| `3_platform/_governed_skeleton/graphify-out/` | Must remain absent. |
| `9_artifacts/graphify/<run_id>/work/graphify-out/` | Acceptable generated-local output location if Graphify writes to cwd. |
| `9_artifacts/graphify/<run_id>/input/governed_skeleton_code_only/graphify-out/` | Acceptable generated-local output location only if Graphify writes next to input. |
| Any output outside `9_artifacts/graphify/<run_id>/` | Incident; stop and require governance/security decision. |

Future output files, if any are produced, remain local-only, generated-sensitive evidence. They are not source. They are not authority. They are not trackable by default. They are not Cognitive Semantic System substrate.

## 10. Future Execution Shape, Not Authorization
The following command shape is recorded only so a later execution gate has an exact candidate to review. It is not authorized by G-11 and must not be run by G-11.

```powershell
Push-Location 9_artifacts/graphify/<run_id>/work
graphify ../input/governed_skeleton_code_only --no-viz
Pop-Location
```

Safety must come from code-only mirror containment, not from `--no-viz`. If any provider/auth prompt, API-key request, model backend request, host-agent semantic extraction path, network activation prompt, or credential lookup appears in a future run, the required response is a hard stop.

## 11. `.graphifyignore` and `.gitignore` Posture
G-11 does not create `.graphifyignore`. G-11 does not modify `.gitignore`. The preferred safe mirror route does not depend on `.graphifyignore` because input containment is achieved by copying only the approved code-only set in a future gate.

Bounded `.gitignore` review found existing coverage for `2_products/`, `4_external/sources/`, `previusknowledge/`, `7_datasets/`, `8_models/`, `9_artifacts/`, `.env`, `.env.*`, secrets, credentials, and token-like patterns. It did not show root `graphify-out/`, `3_platform`, `AGENTS.md`, `.agents/`, `.claude/`, or `.codex/` entries. G-11 does not add them.

Ignore files are useful guardrails, not the primary safety boundary for this route. The primary boundary is the future mirror containing only the approved `.py` files under `9_artifacts/graphify/<run_id>/input/`.

## 12. Repository Root and Integration Posture
Repository root scan remains blocked. `/graphify .` remains blocked. `graphify .` remains blocked. Scanning `0_architecture/` remains blocked for the next attempt because Markdown can trigger provider/auth. Scanning live `3_platform/_governed_skeleton/` remains blocked until output placement and docs exclusion are proven by a later gate.

OpenCode integration remains blocked. `graphify opencode install` remains blocked. `AGENTS.md`, `.agents/`, `.claude/`, `.codex/`, hooks, watch mode, MCP, Neo4j/FalkorDB export, URL ingestion, and always-on behavior remain blocked.

## 13. Provider / Auth Boundary
G-11 does not approve API key usage. G-11 does not inspect `.env`. G-11 does not inspect credentials, provider configs, browser auth, local credential stores, environment variables, token stores, keychains, or model endpoint configuration.

No provider/auth workaround is permitted. A future code-only mirror route must either avoid provider/auth entirely or stop. If documentation or semantic extraction is desired later, that requires a separate Provider/Auth Activation Decision and security gate.

## 14. Cognitive Semantic System Boundary
Graphify remains a candidate evidence-producing local tool only. Graphify output is not authority. Graphify repo map is not Cognitive Semantic System substrate. Graph remains candidate only. Cognitive Semantic System substrate remains deferred.

Siamese governance remains the decision layer. Validation evaluates; governance decides. No graph, vector database, ontology database, runtime, memory substrate, or Cognitive Semantic System storage layer is selected or created by G-11.

## 15. Future Gate Sequence
| Gate | Recommended role |
| --- | --- |
| G-12 - Graphify Safe Mirror Materialization Gate | Create only the safe mirror and local-only notice under `9_artifacts/graphify/<run_id>/`, then verify file counts and extension counts. No Graphify execution by default. |
| G-13 or later - Graphify Safe Mirror Execution Gate | If G-12 succeeds and governance explicitly approves execution, run the candidate command from the contained `work/` directory and stop on any provider/auth prompt or output escape. |
| Later curation gate | Review only generated output metadata first, then decide whether any summary can be curated and tracked. |
| Fallback gate | Create a non-Graphify static dependency map if Graphify remains too risky or too narrow. |

G-11 recommends `G-12 - Graphify Safe Mirror Materialization Gate` as the next ticket. G-11 does not start G-12.

## 16. Decision Matrix
| Route | Input containment | Output containment | Provider/auth risk | G-11 recommendation |
| --- | --- | --- | --- | --- |
| Repo-root `/graphify .` | Weak. | Weak. | High. | Blocked. |
| Root `.graphifyignore` default-deny | Potentially strong, but unproven. | Still unresolved. | Medium if only code enters; high if docs leak. | Defer. |
| Live `_governed_skeleton` docs-off | Moderate, depends on ignore behavior. | Unresolved near source tree. | Medium. | Defer behind mirror route. |
| Safe mirror code-only | Strong, if materialized exactly. | Strong, if cwd and post-run checks stay under artifacts. | Low if corpus remains code-only. | Preferred future route. |
| Provider/auth docs route | Broad docs possible. | Unresolved. | High by design. | Not recommended now. |
| Non-Graphify static map | Exact manual/static scope. | No Graphify output. | None. | Safe fallback. |

## 17. Created / Not Created Register
| Artifact/action | G-11 status | Reason |
| --- | --- | --- |
| Safe mirror / output strategy document | Created | Required G-11 artifact. |
| Safe mirror | Not created | Creation belongs to a future materialization gate. |
| File copying | Not performed | Copying is outside G-11. |
| Graphify command | Not run | Execution is outside G-11. |
| `/graphify .` or `graphify .` | Not run | Repository root scan remains blocked. |
| `.graphifyignore` | Not created | Ignore file creation remains blocked. |
| `.gitignore` | Not modified | Git ignore mutation remains blocked. |
| Provider/auth/API key | Not configured | Provider/auth remains blocked. |
| Partial outputs | Not read or curated | G-06 artifacts remain local-only and generated-sensitive. |
| OpenCode integration | Not installed | Assistant integration remains blocked. |
| Source tracking | Not expanded | Git/source tracking requires a later decision. |
| Cognitive Semantic System substrate | Not selected | Substrate decision remains deferred. |
| G-12 | Not started | G-11 stops before the next ticket. |

## 18. Residual Risk Register
| Risk | Current handling |
| --- | --- |
| Graphify may still require provider/auth for unexpected input classification. | Future run must stop on any prompt or API-key requirement. |
| Graphify may write output somewhere other than expected. | Future execution gate must perform pre/post path checks and treat output escape as incident. |
| Safe mirror may omit useful architecture context. | Accepted for first proof because code-only containment is safer. |
| Code-only output may be too narrow for Siamese architecture governance. | Use it as evidence only, or use non-Graphify fallback for architecture maps. |
| `.graphifyignore` remains unproven by execution. | Mirror route avoids depending on ignore behavior for first proof. |
| Generated output may be sensitive. | Keep under ignored `9_artifacts/`, local-only, and untracked by default. |
| Existing `3_platform` siblings remain unknown. | They remain uninspected and unapproved. |
| Cognitive Semantic System substrate pressure may bias interpretation. | Keep Graphify evidence-only and substrate deferred. |

## 19. Blocker Register
Blockers retained: need safe mirror materialization gate; need future output preflight; need Graphify execution gate if still desired; need provider/auth decision if docs are included; need output curation gate; need source tracking decision for any curated summary; need repo-root scan approval before any root scan; need OpenCode integration decision before any assistant integration; need Cognitive Semantic System substrate decision.

## 20. Incident Handling
Incidents include G-11 creates a safe mirror; copies files; runs Graphify; runs `/graphify .`; runs `graphify .`; creates `.graphifyignore`; modifies `.gitignore`; configures provider/auth; inspects `.env`; reads secrets or credentials; reads product source; reads Hermes source; reads Graphify implementation source; opens `_governed_skeleton` file contents; inspects existing `3_platform` siblings; reads, parses, summarizes, curates, deletes, or tracks Graphify partial outputs; creates OpenCode integration files; adopts Graphify as authority; selects Cognitive Semantic System substrate; attempts Git mutation; or starts G-12.

Response: STOP, preserve safe metadata only, require governance/security decision.

## 21. G-11 Invariants
| ID | Invariant |
| --- | --- |
| G11-001 | Graphify Safe Mirror / Output Strategy Plan is not Graphify execution. |
| G11-002 | No safe mirror is created by G-11. |
| G11-003 | No files are copied by G-11. |
| G11-004 | No Graphify command is run by G-11. |
| G11-005 | No `.graphifyignore` file is created by G-11. |
| G11-006 | `.gitignore` is not modified by G-11. |
| G11-007 | Repository root scan remains blocked. |
| G11-008 | `/graphify .` remains blocked. |
| G11-009 | `graphify .` remains blocked. |
| G11-010 | No provider/auth configuration is authorized by G-11. |
| G11-011 | Partial artifacts remain local-only and unread. |
| G11-012 | Graphify remains evidence only, not authority. |
| G11-013 | Graphify repo map is not Cognitive Semantic System substrate. |
| G11-014 | Graph remains candidate only. |
| G11-015 | Cognitive Semantic System substrate remains deferred. |
| G11-016 | Existing 3_platform siblings remain uninspected and unapproved. |
| G11-017 | Product source remains local-only. |
| G11-018 | External sources remain local-only evidence. |
| G11-019 | Hermes is not inspected or adopted. |
| G11-020 | Validation evaluates; governance decides. |
| G11-021 | G-11 stops before G-12. |

## 22. Anti-patterns
Anti-patterns: treating a plan as execution approval; copying files during a strategy gate; using `--no-viz` as no-LLM control; scanning repo root by convenience; relying on ignore files as the only safety boundary; placing `graphify-out/` at repo root; placing output under live source; reading partial artifacts before a curation gate; committing raw generated output; treating Graphify as authority; treating Graphify repo map as Cognitive Semantic System substrate; selecting graph substrate because Graphify exists; starting G-12 inside G-11.

Rejected/prohibited/historical examples only: `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth`. No such string is accepted as a current AGENT PLATFORM, Siamese, or Cognitive Semantic System name.

## 23. Final Verdict
| Question | Answer |
| --- | --- |
| What did G-11 create? | This safe mirror / output strategy plan only. |
| Was a safe mirror created? | No. |
| Were files copied? | No. |
| Was Graphify run? | No. |
| Was `/graphify .` or `graphify .` run? | No. |
| Was `.graphifyignore` created? | No. |
| Was `.gitignore` modified? | No. |
| Was provider/auth configured? | No. |
| Were partial outputs read or curated? | No. |
| Is repo-root scan approved? | No. Repository root scan remains blocked. |
| What is the preferred next route? | `G-12 - Graphify Safe Mirror Materialization Gate`, creating only the contained code-only mirror if explicitly approved. |
| Is the first actual Graphify rerun approved? | No. It should remain G-13 or later unless a later governance gate explicitly changes that. |
| Was Graphify adopted? | No. Graphify remains evidence only, not authority. |
| Was Cognitive Semantic System substrate selected? | No. Cognitive Semantic System substrate remains deferred. |

G-11 stops here. No mirror is created, no files are copied, no Graphify command is run, no provider/auth is configured, partial outputs remain unread and uncurated, and G-12 is not started.
