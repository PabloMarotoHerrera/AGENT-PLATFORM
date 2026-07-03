# G-16 - Graphify Output Metadata Review

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Graphify Output Metadata Review |
| Ticket | G-16 |
| Status | Accepted Graphify output metadata review |
| Date | 2026-07-03 |
| Scope | Metadata-only review of generated-local Graphify output from the successful G-15 controlled root-ignore run. |
| Authority | Output metadata review only, not semantic curation, execution, source tracking, Graphify adoption, or Cognitive Semantic System substrate selection. |
| Related documents | G-09 through G-15, security/Cognitive Semantic System docs, `.gitignore`, `.graphifyignore`, README.md. |
| Review target | `9_artifacts/graphify/graphify_root_ignore_20260703_105306/graphify-out/` |

## 2. Purpose
G-15 succeeded as a controlled root-ignore run and produced generated output under the approved local-only artifact root. G-16 reviews generated output metadata only.

G-16 does not rerun Graphify. G-16 does not curate graph semantics. G-16 does not treat raw graph as authority. G-16 does not start G-17.

## 3. G-15 Run Summary
| Field | Result |
| --- | --- |
| run_id | `graphify_root_ignore_20260703_105306` |
| command | `graphify extract . --out 9_artifacts/graphify/graphify_root_ignore_20260703_105306` |
| result | Succeeded as one controlled root-ignore run. |
| files reported by Graphify | `6 code, 0 docs, 0 papers, 0 images` |
| output files created | `graph.json`, `.graphify_analysis.json`, `manifest.json`, `cache/` |
| absent output files | `GRAPH_REPORT.md`, `graph.html` |
| provider/auth status | No provider/auth/API-key prompt reported or configured. |
| cleanup status | Cleanup did not run. |
| `.graphifyignore` status | Kept; not modified by G-16. |

## 4. Metadata Review Boundary
Metadata review may inspect JSON structure and counts. Metadata review may inspect manifest file metadata and `.graphify_analysis.json` metadata. Metadata review may compare generated path metadata with approved source-file metadata.

Metadata review may not interpret nodes or edges as architectural truth. Metadata review may not curate output into a summary. Metadata review may not alter source files, generated files, `.graphifyignore`, or `.gitignore`.

## 5. Output Artifact Register
| Artifact | Exists? | Size | Classification | Content inspected? | Semantic curation? | Trackable? | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `graph.json` | True | 502034 bytes | Generated graph projection. | Structure/count only | No | No by default | Missing-file review or curation gate. |
| `.graphify_analysis.json` | True | 48656 bytes | Generated analysis metadata/projection. | Structure/count only | No | No by default | Metadata review only. |
| `manifest.json` | True | 1449 bytes | Generated file manifest metadata. | Metadata only | No | No by default | Used for 7-vs-6 comparison. |
| `cache/` | True | Directory | Generated cache. | Child names/sizes only | No | No | Leave local-only. |
| `cache/ast/` | True | Directory | Generated AST cache directory. | Name only | No | No | Leave local-only. |
| `cache/stat-index.json` | True | 1591 bytes | Generated cache index. | Metadata only | No | No | Leave local-only. |
| `GRAPH_REPORT.md` | False | Not applicable | Report absent. | No | No | No | None. |
| `graph.html` | False | Not applicable | Visualization absent. | No | No | No | None. |
| root `graphify-out/` | False | Not applicable | Forbidden root output absent. | No | No | No | None. |
| live source `graphify-out/` | False | Not applicable | Forbidden live-source output absent. | No | No | No | None. |
| assistant config paths | Absent | Not applicable | Integration artifacts absent. | No | No | No | None. |

## 6. JSON Structure Review
| File | Top-level keys | Notable metadata fields | Count fields | Limitation |
| --- | --- | --- | --- | --- |
| `graph.json` | `directed`, `multigraph`, `graph`, `nodes`, `links`, `hyperedges`, `built_at_commit` | Graph-level metadata only; no semantic interpretation. | `nodes`, `links`; no top-level `edges` or `communities`. | Node/link content not curated. |
| `manifest.json` | Six path keys under `3_platform/_governed_skeleton/...` | Each entry has `mtime`, `ast_hash`, `semantic_hash`. | Six manifest entries. | Hashes are metadata only, not source review. |
| `.graphify_analysis.json` | `communities`, `cohesion`, `gods`, `surprises`, `tokens` | Analysis structure only. | 7 community properties; 10 gods entries; 3 surprises entries. | Names/meaning not curated. |

## 7. Count Review
| Count source | Nodes | Edges/links | Communities | Files/code/docs/papers/images | Agreement with G-15 command output? | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| G-15 command output | 273 | 583 edges | 7 | 6 code, 0 docs, 0 papers, 0 images | Baseline | Terminal output only. |
| `graph.json` metadata | 273 | 583 links | No top-level community key; 7 distinct node community values. | Not available. | Matches nodes and edge/link count. | Uses `links`, not `edges`. |
| `.graphify_analysis.json` metadata | Not applicable | Not applicable | 7 community properties | Not applicable | Matches community count. | No semantic curation. |
| `manifest.json` metadata | Not applicable | Not applicable | Not applicable | 6 processed file entries | Matches 6 code files. | One approved `.py` absent. |
| Approved source baseline | Not applicable | Not applicable | Not applicable | `.py`: 7, `.md`: 32 | Does not fully match. | Markdown intended excluded; one `.py` omitted. |

## 8. `7 .py` vs `6 code` Discrepancy Review
| Approved source file | Allowed by `.graphifyignore`? | Appears in manifest metadata? | Likely processed? | Note |
| --- | --- | --- | --- | --- |
| `agents/runtime_boundary/agent_runtime_boundary.py` | Yes by Python allow rule. | Yes | Yes | Manifest entry exists. |
| `cognitive_semantic_system/prototype/cognitive_semantic_system_prototype.py` | Yes by Python allow rule. | Yes | Yes | Manifest entry exists. |
| `context/runtime/context_pack_runtime.py` | Yes by Python allow rule. | Yes | Yes | Manifest entry exists. |
| `integrations/provider_adapter_layer/provider_adapter_layer.py` | Conflicted: Python allow rule permits it, but `provider*` hard exclusion likely matches the provider-named path or file. | No | No | Likely explanation for 6 vs 7. |
| `security/access_enforcement/security_access_enforcement.py` | Yes by Python allow rule. | Yes | Yes | Manifest entry exists. |
| `tools/execution_boundary/tool_execution_boundary.py` | Yes by Python allow rule. | Yes | Yes | Manifest entry exists. |
| `validation/registry/validation_registry.py` | Yes by Python allow rule. | Yes | Yes | Manifest entry exists. |

Metadata can identify the missing approved file: `provider_adapter_layer.py`. The likely metadata-only explanation is that `.graphifyignore` included the hard exclusion `provider*`, which overrode or conflicted with the intended Python include for provider-named paths. G-16 does not modify `.graphifyignore` or rerun Graphify.

## 9. Ignore Boundary Review
`.graphifyignore` default-deny was kept. Intended included path is only `3_platform/_governed_skeleton/**/*.py`. Intended excluded paths remain blocked.

Manifest metadata shows no paths under `0_architecture/`, `2_products/`, `4_external/`, `previusknowledge/`, `7_datasets/`, `8_models/`, `9_artifacts/`, `.git/`, assistant config, root `graphify-out/`, or live-source `graphify-out/`. No excluded path incident is recorded.

The `provider*` exclusion likely excluded one intended provider-named `.py` file. This is a scope-completeness issue, not evidence that forbidden paths were scanned.

## 10. Output Containment Review
Output stayed under `9_artifacts/graphify/graphify_root_ignore_20260703_105306/`. Root `graphify-out/` is absent. Live source `3_platform/_governed_skeleton/graphify-out/` is absent. Assistant config paths are absent.

Output is generated/local-only and ignored by default through `9_artifacts/`.

## 11. Provider/Auth Boundary
No provider/auth/API key was requested. No `.env` was inspected. No credentials were inspected. No provider was activated. Future docs-inclusive runs still require a separate provider/auth decision.

## 12. Graphify Adoption Boundary
Graphify output is generated evidence, not authority. Output is not governance truth. Output is not source. Output is not Cognitive Semantic System substrate. Successful metadata review is not Graphify adoption.

## 13. Git / Source Tracking Boundary
Raw generated output remains untracked. `9_artifacts/` remains local-only. `.graphifyignore` may be tracked because G-15 kept it and it constrains future Graphify use, but only after human exact-path approval. The G-16 governance record may be tracked after human approval. Do not track generated output. No `git add .`. No force-add.

## 14. Cognitive Semantic System Boundary
Graphify output does not affect substrate decision yet. Graph remains candidate only. Cognitive Semantic System substrate remains deferred. No graph/vector/database/ontology runtime is adopted.

## 15. Created / Not Created Register
| Artifact/action | G-16 status | Reason |
| --- | --- | --- |
| governance document | Created | Required G-16 record. |
| output metadata reviewed | Completed | Metadata-only scope. |
| `graph.json` structure/count metadata reviewed | Completed | Top-level keys and counts only. |
| manifest metadata reviewed | Completed | File path/hash metadata only. |
| analysis metadata reviewed | Completed | Top-level keys and counts only. |
| output content semantically curated | Not performed | Blocked by G-16. |
| Graphify rerun | Not run | Prohibited. |
| provider/auth | Not configured | Blocked. |
| `.graphifyignore` | Not modified | Modification blocked. |
| `.gitignore` | Not modified | Modification blocked. |
| generated outputs staged/tracked | Not performed | Git/source tracking blocked. |
| G-17 | Not started | G-16 stops before G-17. |

## 16. Residual Risk Register
| Risk | Current handling |
| --- | --- |
| Metadata may be incomplete. | Treat review as metadata-only. |
| One approved `.py` was not processed. | Recommend missing-file metadata review before or alongside curation. |
| Graph may over-represent implementation details. | No semantic claims made. |
| Graph may under-represent architecture docs. | Expected; docs were excluded. |
| Raw graph may contain noisy nodes/edges. | Curation gate required. |
| Curation may find low value. | Keep non-Graphify fallback open. |
| Provider/auth route remains high risk for docs. | Separate decision required. |
| Repo-root broader scan remains blocked except through current ignore profile. | Preserve boundary. |
| Cognitive Semantic System substrate remains undecided. | No substrate selection. |

## 17. Blocker Register
Blockers retained: need semantic curation gate if metadata is accepted; need discrepancy resolution if missing provider adapter file matters; need cleanup policy for old mirror/failure artifacts; need source tracking decision for curated summary; need provider/auth decision for docs-inclusive Graphify use; need OpenCode integration decision before `/graphify .`; need Cognitive Semantic System substrate decision.

## 18. Incident Handling
Incidents include excluded paths appear in metadata; provider/auth evidence appears; assistant config appears; root output appears; live-source output appears; output content is curated; graph is treated as authority; generated output is staged; `.gitignore` is modified; `.graphifyignore` is broadened without approval; or G-17 is started.

Response: STOP, preserve safe metadata only, require governance/security decision.

## 19. G-16 Invariants
| ID | Invariant |
| --- | --- |
| G16-001 | Graphify Output Metadata Review is not semantic curation. |
| G16-002 | Graphify output is generated evidence, not authority. |
| G16-003 | Raw graph output is not architecture truth. |
| G16-004 | No Graphify rerun is authorized by G-16. |
| G16-005 | No provider/auth configuration is authorized by G-16. |
| G16-006 | `.graphifyignore` is not modified by G-16. |
| G16-007 | `.gitignore` is not modified by G-16. |
| G16-008 | Generated outputs are not trackable by default. |
| G16-009 | Repository root scan remains constrained by `.graphifyignore`. |
| G16-010 | OpenCode integration remains blocked. |
| G16-011 | Cognitive Semantic System substrate remains deferred. |
| G16-012 | Graphify remains evidence only, not authority. |
| G16-013 | Validation evaluates; governance decides. |
| G16-014 | G-16 stops before G-17. |

## 20. Anti-patterns
Anti-patterns: metadata review as semantic curation; node count as architecture quality; graph as truth; graph as source; generated output committed by convenience; `.graphifyignore` broadened by convenience; `/graphify .` by convenience; OpenCode integration by convenience; selecting graph substrate because Graphify succeeded; `git add .`; starting G-17 inside G-16.

## 21. Next Ticket Recommendation
| Condition | Recommendation |
| --- | --- |
| Metadata accepted and no excluded paths appear | `G-17 - Graphify Semantic Curation Gate` |
| One file is missing and needs resolution | `G-17 - Graphify Missing File Metadata Review` |
| Excluded paths appear | `G-17 - Graphify Root Ignore Incident Review` |
| Graph is low-value | `G-17 - Non-Graphify Parallel Work Packet Dependency Map` |

Actual recommendation: `G-17 - Graphify Missing File Metadata Review`, because metadata is structurally valid and contained, but one approved `.py` file is absent from the manifest and should be resolved before semantic curation is treated as complete.

G-16 does not start G-17.

## 22. Final Verdict
| Question | Answer |
| --- | --- |
| What output metadata was reviewed? | Top-level JSON keys, count-only graph metadata, manifest path/hash metadata, analysis top-level/count metadata, output file sizes, cache child metadata, and containment paths. |
| Which files exist? | `graph.json`, `.graphify_analysis.json`, `manifest.json`, `cache/`, `cache/ast/`, and `cache/stat-index.json`. |
| Which files are absent? | `GRAPH_REPORT.md`, `graph.html`, root `graphify-out/`, live-source `graphify-out/`, and assistant config paths. |
| What counts were confirmed? | 273 nodes, 583 links, 7 distinct node community values, 7 analysis community properties, 6 manifest file entries, and source baseline `.py`: 7 / `.md`: 32. |
| Did excluded paths appear? | No excluded paths appeared in manifest metadata. |
| Why did Graphify report 6 code files instead of 7 approved `.py` files? | Manifest metadata excludes `provider_adapter_layer.py`; `.graphifyignore` contains `provider*`, likely excluding that provider-named path despite the Python allow rule. |
| Was output contained? | Yes, under `9_artifacts/graphify/graphify_root_ignore_20260703_105306/graphify-out/`. |
| Was provider/auth involved? | No. |
| Was semantic curation performed? | No. |
| Was Graphify adopted? | No. |
| Was Cognitive Semantic System substrate selected? | No. |
| What remains blocked? | Graphify rerun, semantic curation, provider/auth, output tracking, `.graphifyignore` mutation, `.gitignore` mutation, OpenCode integration, broader root scan, graph authority, and Cognitive Semantic System substrate selection. |
| What is the recommended next ticket? | `G-17 - Graphify Missing File Metadata Review`, after explicit instruction only. |

G-16 stops here. G-17 is not started. Graphify was not rerun, `/graphify` was not used, `.graphifyignore` was not modified, `.gitignore` was not modified, provider/auth was not configured, secrets were not read, and no staging, commit, push, force-add, or publication occurred.
