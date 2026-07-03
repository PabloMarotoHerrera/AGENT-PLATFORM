# G-15 - Graphify Root Ignore Controlled Run

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Graphify Root Ignore Controlled Run |
| Ticket | G-15 |
| Status | Accepted controlled root-ignore Graphify run with contained output |
| Date | 2026-07-03 |
| Scope | Create root `.graphifyignore`, run one controlled root Graphify extraction, review output metadata only, and retain or clean up by result. |
| Authority | Controlled root-ignore Graphify run only, not OpenCode integration, provider/auth, output curation, source tracking expansion, Graphify adoption, or Cognitive Semantic System substrate selection. |
| Related documents | G-09 through G-14, security/Cognitive Semantic System docs, `.gitignore`, README.md. |
| Run ID | `graphify_root_ignore_20260703_105306` |

## 2. Purpose
G-14 classified the G-13 safe mirror result as `contained_empty_extraction` and identified the ignored `9_artifacts/` mirror as the leading root-cause hypothesis. G-15 tests a practical root execution with a root `.graphifyignore` default-deny profile so Graphify can discover the approved source path while excluding unwanted folders.

G-15 is a controlled proof. G-15 does not install OpenCode integration. G-15 does not configure provider/auth. G-15 does not curate generated output content. G-15 does not start G-16.

## 3. `.graphifyignore` Record
| Field | Result |
| --- | --- |
| `.graphifyignore` created? | Yes. |
| Strategy | Default deny with `*`, then traversal allow rules for `3_platform/_governed_skeleton/`, then allow only `3_platform/_governed_skeleton/**/*.py`. |
| Explicit forbidden folders | `0_architecture/`, `2_products/`, `4_external/`, `previusknowledge/`, `7_datasets/`, `8_models/`, `9_artifacts/`, `graphify-out/`, `.git/`. |
| Explicit forbidden material | `.env*`, secrets, credentials, tokens, provider material, generated/cache/dependency material, assistant config, docs, images, video, JSON/YAML/TOML/CSV/XLSX/Parquet. |
| Boundary marker verification | `Default-deny profile`, `!3_platform/_governed_skeleton/**/*.py`, `4_external/`, `9_artifacts/`, `.env*`, and `AGENTS.md` were found. |
| Kept or deleted? | Kept. |
| Reason | Run succeeded and output stayed contained; cleanup conditions were not triggered. |

## 4. Run Record
| Field | Value |
| --- | --- |
| run_id | `graphify_root_ignore_20260703_105306` |
| command | `graphify extract . --out 9_artifacts/graphify/graphify_root_ignore_20260703_105306` |
| cwd | Repository root. |
| output root | `9_artifacts/graphify/graphify_root_ignore_20260703_105306/` |
| graphify version | `graphify 0.9.5` |
| provider/auth status | No API-key/provider/auth/model endpoint prompt observed; no provider/auth configured. |
| execution status | Succeeded as one controlled root-ignore execution. |
| cleanup status | Cleanup did not run. |
| output status | Contained `graphify-out/` with `graph.json`, `.graphify_analysis.json`, `manifest.json`, and `cache/` by metadata only. |
| assistant config status | `AGENTS.md`, `.agents/`, `.claude/`, `.codex/` absent. |
| decision status | Controlled root-ignore proof succeeded; output curation remains blocked until G-16 or later. |

## 5. Input Boundary
Intended included input: only `.py` files under `3_platform/_governed_skeleton/`.

Intended excluded inputs: `0_architecture/`, `2_products/`, `4_external/`, `previusknowledge/`, `7_datasets/`, `8_models/`, `9_artifacts/`, `.git/`, secrets, credentials, provider material, assistant config, docs, and non-code files.

Preflight metadata showed `.py`: 7 and `.md`: 32 under `3_platform/_governed_skeleton/`. Markdown files existed but were intended to be excluded by `.graphifyignore`.

`.graphifyignore` is a practical filter, not authority. Governance remains authority; Validation evaluates.

## 6. Command Execution Log
| Field | Result |
| --- | --- |
| exact command | `graphify extract . --out 9_artifacts/graphify/graphify_root_ignore_20260703_105306` |
| exact working directory | Repository root. |
| stdout/stderr safe summary | Graphify scanned the repository root under `.graphifyignore`, reported `found 6 code, 0 docs, 0 papers, 0 images`, ran AST extraction on 6 code files, wrote `graph.json` with 273 nodes, 583 edges, and 7 communities, wrote `.graphify_analysis.json`, and suggested `cluster-only`; that suggestion was not run. |
| provider/auth requested? | No. |
| forbidden paths appeared? | No forbidden child path was reported as an input. The command used approved controlled root input with `.graphifyignore`. |
| output created? | Yes, under approved output root only. |
| cleanup ran? | No. |
| raw output handling | No long raw terminal dump retained; generated output contents were not opened. |

Graphify found 6 code files while preflight saw 7 `.py` files. This discrepancy is retained as metadata risk for G-16; it does not change the contained-success classification.

## 7. Output Artifact Register
| Path | Exists? | Classification | Content inspected? | Trackable? | Next review |
| --- | --- | --- | --- | --- | --- |
| `9_artifacts/graphify/graphify_root_ignore_20260703_105306/graphify-out/` | True | Generated local-only output root. | No | No by default | G-16 metadata review. |
| `GRAPH_REPORT.md` | False | Report absent; cluster-only was not run. | No | No | None. |
| `graph.json` | True, length 502034 bytes. | Generated graph projection. | No | No by default | G-16 metadata/content gate. |
| `cache/` | True | Generated cache directory. | No | No | Cleanup/metadata gate later. |
| `graph.html` | False | Visualization absent. | No | No | None. |
| `.graphify_analysis.json` | True, length 48656 bytes. | Generated analysis metadata/projection. | No | No by default | G-16 metadata review. |
| `manifest.json` | True, length 1449 bytes. | Generated manifest. | No | No by default | G-16 metadata review. |
| root `graphify-out/` | False | Forbidden root output absent. | No | No | None. |
| live source `3_platform/_governed_skeleton/graphify-out/` | False | Forbidden live-source output absent. | No | No | None. |
| assistant config paths | Absent | Integration artifacts absent. | No | No | None. |

## 8. Output Classification
Output is local-only/generated-sensitive. Raw output is not source. Raw output is not authority. Raw output is not trackable by default. Output is not Cognitive Semantic System substrate. Output curation requires G-16 or later explicit approval.

## 9. Provider/Auth Boundary
No API key is approved. No provider/auth was configured. No `.env` was inspected. No credentials were inspected. Any provider/auth/API-key/model endpoint request would have caused failure and cleanup, but no such request appeared.

## 10. Graphify Adoption Boundary
Graphify remains evidence only. A successful run is not Graphify adoption. Output is not governance truth. Graphify output is not source. Graphify repo map is not Cognitive Semantic System substrate.

## 11. Repository Root / OpenCode Boundary
`/graphify .` was not run. `graphify .` was not run. OpenCode integration was not installed. Assistant config files were not created. Root scan was allowed only through controlled `.graphifyignore` and documented `graphify extract . --out ...`; it is not general precedent for uncontrolled root scans.

## 12. Git / Source Tracking Boundary
Generated output must not be staged. `.graphifyignore` may be staged only if the run succeeds and a human approves exact-path staging. This governance document may be staged after human approval. No `git add .`. No force-add. No generated artifact tracking by default.

## 13. Cleanup Record
Cleanup did not run. Nothing was removed.

Remaining artifacts: `.graphifyignore` and `9_artifacts/graphify/graphify_root_ignore_20260703_105306/graphify-out/` remain local-only. Root `graphify-out/`, live-source `graphify-out/`, and assistant config paths remain absent.

## 14. Final Verdict
| Question | Answer |
| --- | --- |
| Was `.graphifyignore` created? | Yes. |
| Was Graphify run? | Yes, exactly once. |
| What command was used? | `graphify extract . --out 9_artifacts/graphify/graphify_root_ignore_20260703_105306`. |
| Did provider/auth appear? | No. |
| Did forbidden paths appear? | No forbidden child input paths were reported; Graphify reported root scan under the approved controlled `.graphifyignore` plan. |
| Did Graphify produce useful output files? | Yes: `graph.json` exists with command-reported nodes/edges/communities; generated content was not opened. |
| Was cleanup executed? | No. |
| Was `/graphify .` run? | No. |
| Was OpenCode integration installed? | No. |
| Was Graphify adopted? | No. |
| Was Cognitive Semantic System substrate selected? | No. |
| What is the recommended next ticket? | `G-16 - Graphify Output Metadata Review`, after explicit instruction only. |

Conditional next-ticket posture: if run succeeds and output files exist, use `G-16 - Graphify Output Metadata Review`; if output is empty, use `G-16 - Graphify Empty Output Review`; if failure or cleanup runs, use `G-16 - Graphify Root Ignore Run Failure Review`; if Graphify remains low-value, use `G-16 - Non-Graphify Parallel Work Packet Dependency Map`.

G-15 stops here. G-16 is not started. Generated output content was not read or curated. No staging, commit, push, force-add, or publication occurred.
