# GRAPHIFY-SCOPE-01 - Hermes Product Graph Scope

## Document Header

| Field | Value |
| --- | --- |
| Ticket | GRAPHIFY-SCOPE-01 |
| Status | Superseded by accepted GRAPHIFY-SCALE-01 pipeline |
| Date | 2026-07-18 |
| Scope root | Repository root (`.`) |
| Newly admitted root | `2_products/hermes-agent/**` |
| Locked external root | `4_external/sources/hermes-agent/**` |
| Graphify version | `0.9.5` |
| Authorized tracked changes | `.graphifyignore` and this record only |
| Generated outputs | `graphify-out/**` (local and untracked) |
| Evidence class | Local generated supporting evidence; non-authoritative |

## Purpose

GRAPHIFY-SCOPE-01 expands the existing fail-closed Graphify input boundary to
admit the active Hermes product at `2_products/hermes-agent/**`. It does not
admit any sibling or future product, any external-source checkout, dependency
tree, generated bundle, cache, local environment, credential, provider secret,
runtime output, binary, media artifact or dependency lockfile.

The candidate refresh is an AST-only Graphify source, document and
package-manifest graph update produced by a custom wrapper around installed
Graphify internals. It does not modify the Hermes product, execute Hermes,
invoke a provider or model, perform semantic extraction, authorize runtime use,
promote Graphify to authority, stage files, commit or push.

GRAPHIFY-SCOPE-01-CLOSE superseded the earlier acceptance statement in this
record at the time of closure. Its fallback verdict is retained below as
historical evidence. GRAPHIFY-SCALE-01 now supersedes that limitation with an
accepted maintained, deterministic and baseline-preserving pipeline.

## Scope Decision

The selected boundary is an anchored default-deny product rule followed by one
explicit product exception:

```gitignore
/2_products/
/2_products/**
!/2_products/
!/2_products/hermes-agent/
!/2_products/hermes-agent/**
```

Dependency, environment, generated, sensitive and binary exclusions are
reasserted after the allow rule. Those exclusions use unanchored directory or
file names so Graphify applies them at every depth within Hermes without
opening another product root.

| Path class | Decision |
| --- | --- |
| `2_products/hermes-agent/**` first-party source | Admit |
| `2_products/hermes-agent/**` first-party docs | Admit |
| `2_products/hermes-agent/**` product configuration schemas | Admit |
| Other direct children of `2_products/` | Deny |
| Future direct children of `2_products/` | Deny by default |
| `4_external/sources/**` and `external/sources/**` | Deny |
| Dependency and environment trees | Deny |
| Cache, generated, build and runtime output | Deny |
| Credentials, secrets, tokens and local environment files | Deny |
| Compiled, binary, database, media and archive files | Deny |
| Dependency lockfiles | Deny |

The seven observed direct product directories are `backend-energyplus`, `cli`,
`desktop`, `experimental`, `hermes-agent`, `omniverse-app` and `web-platform`.
Only `hermes-agent` is opened.

## Installed Parser Evidence

Installed Graphify source was inspected before changing the policy. In
Graphify 0.9.5:

- `.gitignore` is loaded before `.graphifyignore`;
- rules are evaluated in order with last-match-wins behavior;
- `!` negation reopens an excluded path;
- excluded ancestors must also be reopened;
- a leading `/` anchors a rule to its ignore-file directory;
- built-in noise-directory pruning still applies before extraction;
- `graphify update .` performs local AST extraction with no LLM requirement.

An installed-parser simulation against the final rule order produced the
following result:

| Representative | Expected ignored | Observed ignored | Result |
| --- | ---: | ---: | --- |
| `2_products/hermes-agent/hermes_constants.py` | false | false | Pass |
| `2_products/hermes-agent/apps/shared/src/index.ts` | false | false | Pass |
| `2_products/hermes-agent/docs/session-lifecycle.md` | false | false | Pass |
| `2_products/hermes-agent/pyproject.toml` | false | false | Pass |
| `2_products/hermes-agent/hermes_cli/agent_platform/product_config.py` | false | false | Pass |
| `2_products/hermes-agent/plugins/model-providers/anthropic/plugin.yaml` | false | false | Pass |
| `2_products/backend-energyplus/example.py` | true | true | Pass |
| `2_products/cli/example.py` | true | true | Pass |
| `4_external/sources/hermes-agent/hermes_constants.py` | true | true | Pass |
| Hermes `node_modules/pkg/index.js` | true | true | Pass |
| Hermes `.venv/Lib/site-packages/pkg.py` | true | true | Pass |
| Hermes plugin `dist/index.js` | true | true | Pass |
| Hermes `.env.example` | true | true | Pass |
| Hermes `website/docs/user-guide/secrets/index.md` | true | true | Pass |
| Hermes `credentials/config.json` | true | true | Pass |
| Hermes `outputs/run.json` | true | true | Pass |
| Hermes `package-lock.json` | true | true | Pass |
| Hermes `assets/logo.png` | true | true | Pass |

## Preflight Evidence

Preflight was captured on 2026-07-16 before the refresh:

```yaml
GRAPHIFY_SCOPE_01_Preflight:
  branch: main
  head: a42768937432c3e609c516208ef1184058f6dcc2
  origin_main: a42768937432c3e609c516208ef1184058f6dcc2
  head_matches_origin_main: true
  graphify_processes: 0
  graphify_version: 0.9.5
  locked_upstream_clean: true
  locked_upstream_commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  hermes_tracked_files: 6172
  tracked_dependency_paths: 0
  authorized_tracked_modification: .graphifyignore
  allowed_unrelated_untracked:
    - .opencode/
    - AGENTS.md
    - graphify-out/
```

No product source was modified. The locked upstream remains detached and clean.

## Candidate Inventory

The tracked Hermes inventory contains 6,172 files. Pre-refresh classification
identified these bounded Graphify-relevant signals:

| Candidate class | Count |
| --- | ---: |
| Graphify-supported code candidates | 4,390 |
| Documentation candidates | 1,416 |
| YAML/TOML configuration candidates | 143 |
| Tracked dependency/environment paths | 0 |
| Tracked generated/binary/runtime exclusion candidates | 22 |
| Tracked sensitive-name exclusion candidates | 7 |

Major supported code-extension counts were 2,911 Python, 809 TypeScript, 434
TSX, 82 CommonJS, 74 JSON, 33 ES modules, 23 shell, 11 JavaScript and nine
Rust files. The inventory is a candidate count, not a claim that every file
must produce one or more nodes.

Local ignored trees include root and web `node_modules`, root `.venv`, and
`hermes_cli/web_dist`. The `node_modules/@hermes/shared` junction must remain
untraversed; first-party `apps/shared` remains eligible through its canonical
product path.

## Baseline Graph

The pre-refresh graph was generated from the current commit and contained no
product or external-source nodes:

```yaml
GRAPHIFY_SCOPE_01_Baseline:
  built_at_commit: a42768937432c3e609c516208ef1184058f6dcc2
  nodes: 5674
  relationships: 6693
  communities: 214
  labels: 214
  labels_sha256: cd303de3b5e5f5408565e504339d54332eb0a942fbbdefac48fa72b9653cbd61
  manifest_entries: 236
  product_nodes: 0
  hermes_nodes: 0
  sibling_product_nodes: 0
  external_nodes: 0
  graph_json_bytes: 6031930
  graph_html_bytes: 131479
```

A preliminary read-only full candidate-detection attempt reached its 300-second
execution bound before returning. It was terminated, left no Graphify process,
and changed no graph artifact. The policy was then consolidated to remove
redundant depth-specific rules before the authorized refresh.

## Refresh and Rollback Contract

Before refresh, the complete current `graphify-out/` directory must be copied
to a temporary directory outside the repository. The required primary command
is:

```powershell
graphify update .
```

The command receives a 300-second execution bound. If it fails, times out,
produces an invalid graph, admits an unauthorized source path, or leaves an
ambiguous partial state, the process must be terminated and the complete
pre-refresh `graphify-out/` backup restored. A tightly scoped local AST refresh
may be considered only after that rollback point and may not weaken the source
policy.

The refresh is accepted only if all of these gates pass:

1. `graph.json`, `GRAPH_REPORT.md`, `manifest.json` and `graph.html` exist.
2. The graph is valid JSON and every relationship endpoint resolves.
3. Representative Hermes Python, TypeScript and configuration sources appear.
4. Hermes contributes nodes through `2_products/hermes-agent/**`.
5. No sibling product contributes a node.
6. No `4_external/**` or `external/**` source contributes a node.
7. No dependency, environment, generated, sensitive or runtime path contributes a node.
8. The locked upstream commit and clean status remain unchanged.
9. The Hermes product worktree remains unchanged.
10. Canonical community HTML is regenerated from the accepted graph.
11. No Graphify process or temporary rollback artifact remains.

## Execution Evidence

### Rollback baseline

The complete pre-refresh `graphify-out/` directory was copied outside the
repository before execution. The backup contained 241 files and matched the
source directory byte for byte.

```yaml
GRAPHIFY_SCOPE_01_RollbackBaseline:
  files: 241
  exact_match: true
  graph_json_sha256: 30ebf4a956faf334d918734b5d6809b97b610e8f0f642df23b9648ed8e415705
  labels_sha256: cd303de3b5e5f5408565e504339d54332eb0a942fbbdefac48fa72b9653cbd61
```

### Primary command and rollback

The required primary command ran with the 300-second bound:

```powershell
graphify update .
```

Graphify completed per-file AST extraction for 5,915 files but did not reach a
graph write or validation result before timeout. The command was terminated,
zero worker processes remained, and the complete rollback baseline was restored.
The restore returned all 241 files to an exact byte-for-byte match. No partial
graph, report, manifest or cache state was accepted.

Hermes-only `_rebuild_code` attempts also completed their per-file work but
exceeded the same bound in root-wide detection or cross-file processing. Each
failed attempt was treated as non-authoritative and followed by a complete
baseline restore. Completed per-file AST cache entries were retained only in the
temporary external execution area and reused as acceleration for the bounded
fallback.

### Bounded AST fallback

The provisional fallback avoided the repeatedly timed-out root word-count scan. It
selected Git-tracked files under `2_products/hermes-agent`, applied Graphify
0.9.5's installed ignore parser, sensitive-path test and extractor dispatch,
and processed 5,687 eligible files in twelve bounded subsystem batches.
Each batch:

1. ran Graphify AST extraction only on its eligible paths;
2. asserted that every newly emitted source path was under Hermes;
3. normalized and merged with the existing graph;
4. preserved every baseline node ID;
5. used `build_from_json` to normalize endpoints and prune expected external or standard-library dangling references;
6. rejected graph shrinkage or unresolved final endpoints;
7. replaced `graph.json` atomically only after validation.

| Batch | Eligible files | Extracted node records | Total nodes after merge | Relationships after merge |
| --- | ---: | ---: | ---: | ---: |
| Core runtime and adapters | 584 | 23,152 | 28,749 | 57,334 |
| Extensions and packages | 592 | 10,536 | 39,202 | 78,257 |
| TUI | 378 | 2,960 | 42,156 | 85,113 |
| Desktop application | 718 | 5,722 | 47,874 | 101,346 |
| Gateway tests | 556 | 20,079 | 67,907 | 131,167 |
| CLI tests | 641 | 20,688 | 88,575 | 158,314 |
| Logic tests | 627 | 26,047 | 114,594 | 191,773 |
| Other tests | 185 | 5,923 | 120,510 | 199,956 |
| Website documentation | 663 | 16,779 | 137,289 | 216,615 |
| Optional-skill documentation | 376 | 6,873 | 144,162 | 223,201 |
| Skill documentation | 308 | 6,796 | 150,958 | 229,717 |
| Other documentation and manifests | 59 | 893 | 151,851 | 230,557 |

Extracted node-record counts are pre-build records, not net graph growth. Normal
Graphify ID reconciliation and deduplication can merge records before the total
is written.

### Clustering and HTML

`graphify cluster-only .` completed inside the execution bound and generated
7,624 communities, a fresh report, graph JSON, labels and membership signatures.
Graphify 0.9.5's stock HTML path then encountered a size edge case: the
151,851-node graph aggregated to 7,624 community nodes, still above the
recursive 5,000-node default. The same installed `to_html` exporter was rerun
with a temporary 10,000-node limit for the already-aggregated community graph.
The result contains 7,624 community nodes and 10,310 cross-community edges.

Graphify wrote the absolute output path into the generated HTML title. That
single presentation field was sanitized to `graphify - AGENT PLATFORM`; final
checks found no absolute workspace path in graph JSON, report or HTML. The
dated internal Graphify safety copy was removed after validation.

### Final measurements

```yaml
GRAPHIFY_SCOPE_01_Final:
  completed_at: 2026-07-16T14:20:46+02:00
  built_at_commit: a42768937432c3e609c516208ef1184058f6dcc2
  nodes: 151851
  relationships: 230557
  communities: 7624
  labels: 7624
  hermes_nodes: 144443
  hermes_source_files_represented: 5643
  manifest_entries: 5923
  hermes_manifest_entries: 5687
  baseline_ids_retained: 5674_of_5674
  unresolved_relationships: 0
  new_out_of_scope_sources: 0
  sibling_product_sources: 0
  external_sources: 0
  forbidden_source_paths: 0
  forbidden_manifest_paths: 0
  absolute_source_paths: 0
  graph_json_bytes: 186248814
  graph_html_bytes: 5662008
  graph_report_bytes: 2687646
  manifest_bytes: 1174143
```

Final artifact hashes:

```text
graph.json              cb04d5dfdb1414bc40977233c10564c5ab3687400a3ce14e96c1e0c984122d86
graph.html              61d01c48b69906dbffe5d140cb8cfecab5e113e5e43bfdb9df86ed2c48fc28bf
GRAPH_REPORT.md         aa904e6cc7ae25430669a53e3007e0680b78697f2ac7f06439f4e229f882b500
manifest.json           09457740c197a0ace10040c7b567792572d73cee0ee4946ab7590f3f316e26fb
.graphify_labels.json   21382d94f541f0cfce057b64cd44f690d82e30b04c57d7ccb4776b3d1cc12fbe
labels signature        f45ecdaff35b437bf1dc867c235e3b6d4668c6c29f5859c0b2cdf14b4ce77318
```

### Pre-closure checks (insufficient for acceptance)

| Gate | Result |
| --- | --- |
| Required canonical files exist | Pass |
| JSON parses and all relationship endpoints resolve | Pass |
| Node IDs are unique | Pass |
| Hermes Python, TypeScript, Markdown, TOML and JSON representatives appear | Pass |
| All 5,674 baseline node IDs remain | Pass |
| Sibling product source nodes | 0, pass |
| External source nodes | 0, pass |
| Dependency/generated/sensitive/runtime source nodes | 0, pass |
| Dependency/generated/sensitive/runtime manifest paths | 0, pass |
| Absolute local source or presentation paths | 0, pass |
| Report node/edge/community counts match graph | Pass |
| Labels and membership signatures match 7,624 communities | Pass |
| Aggregated canonical HTML exists | Pass |
| Hermes product worktree | Clean, pass |
| Hermes product tree | `e430b3af1d0907761691f16e8f6ce2221e5673b1` |
| Locked upstream | Clean at `9de9c25f620ff7f1ce0fd5457d596052d5159596`, tag `v2026.7.7.2` |
| `HEAD == origin/main` | Pass at `a42768937432c3e609c516208ef1184058f6dcc2` |
| Installed-parser representative cases | 18/18 pass |
| Graphify extraction/update/cluster/export processes | 0 after completion |

A user-owned VS Code terminal started a local `python -m http.server` preview of
`graphify-out/` after output generation. It was not started, used or terminated
by this ticket and is not a Graphify mutation process.

## GRAPHIFY-SCOPE-01-CLOSE

### Closure decision

Final closure verdict:

```text
graphify_hermes_scope_fallback_unproven
```

The current `.graphifyignore`, this governance record and `graphify-out/**`
remain unstaged. The generated output is retained because it is structurally
readable and contains no detected sensitive or unauthorized path, but it is
provisional, experimental and noncanonical. It must not be represented as a
supported or reproducible Graphify refresh.

### Exact fallback provenance

Common historical execution context:

```yaml
executable: C:\Users\pablo\anaconda3\python.exe
graphify_executable: C:\Users\pablo\anaconda3\Scripts\graphify.exe
graphify_version: 0.9.5
working_directory: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM
wrapper: C:\Users\pablo\AppData\Local\Temp\opencode\graphify-scope-01-targeted-refresh.py
canonical_output: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\graphify-out\graph.json
atomic_output: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\graphify-out\.graph.scope-01.tmp.json
ast_cache: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\graphify-out\cache
batch_timeout_ms: 300000
stdout_stderr: captured together by the OpenCode shell tool
redirection_or_log_file: none
```

Every accepted input was an absolute path corresponding to a Git-tracked path
under `2_products/hermes-agent/**`. No per-batch graph artifact was retained;
each successful command atomically replaced the same `graph.json`. This missing
intermediate-output ledger is a material provenance limitation.

The exact twelve successful commands, in execution order, were:

```text
"C:\Users\pablo\anaconda3\python.exe" "C:\Users\pablo\AppData\Local\Temp\opencode\graphify-scope-01-targeted-refresh.py" core
"C:\Users\pablo\anaconda3\python.exe" "C:\Users\pablo\AppData\Local\Temp\opencode\graphify-scope-01-targeted-refresh.py" extensions
"C:\Users\pablo\anaconda3\python.exe" "C:\Users\pablo\AppData\Local\Temp\opencode\graphify-scope-01-targeted-refresh.py" ui-tui
"C:\Users\pablo\anaconda3\python.exe" "C:\Users\pablo\AppData\Local\Temp\opencode\graphify-scope-01-targeted-refresh.py" apps-desktop
"C:\Users\pablo\anaconda3\python.exe" "C:\Users\pablo\AppData\Local\Temp\opencode\graphify-scope-01-targeted-refresh.py" tests-gateway
"C:\Users\pablo\anaconda3\python.exe" "C:\Users\pablo\AppData\Local\Temp\opencode\graphify-scope-01-targeted-refresh.py" tests-cli
"C:\Users\pablo\anaconda3\python.exe" "C:\Users\pablo\AppData\Local\Temp\opencode\graphify-scope-01-targeted-refresh.py" tests-logic
"C:\Users\pablo\anaconda3\python.exe" "C:\Users\pablo\AppData\Local\Temp\opencode\graphify-scope-01-targeted-refresh.py" tests-other
"C:\Users\pablo\anaconda3\python.exe" "C:\Users\pablo\AppData\Local\Temp\opencode\graphify-scope-01-targeted-refresh.py" docs-website
"C:\Users\pablo\anaconda3\python.exe" "C:\Users\pablo\AppData\Local\Temp\opencode\graphify-scope-01-targeted-refresh.py" docs-optional-skills
"C:\Users\pablo\anaconda3\python.exe" "C:\Users\pablo\AppData\Local\Temp\opencode\graphify-scope-01-targeted-refresh.py" docs-skills
"C:\Users\pablo\anaconda3\python.exe" "C:\Users\pablo\AppData\Local\Temp\opencode\graphify-scope-01-targeted-refresh.py" docs-other
```

All twelve used a 300,000 ms timeout and returned exit code 0. Their complete,
untruncated combined output was retained in the OpenCode session database; no
stdout/stderr log file was written. Earlier precursor commands were not accepted:

| Wrapper | Command | Result |
| --- | --- | --- |
| Version 1 | no batch argument, twice | timeout after per-file extraction; no numeric exit code |
| Version 2 | `core`, twice | timeout; no numeric exit code |
| Version 3 | `core` | exit 1; rejected 3,895 unresolved relationships |

### Temporary-wrapper hashes

Read-only forensic reconstruction from the OpenCode SQLite session recovered
the exact UTF-8, no-BOM, LF bytes after every edit:

| File/version | Bytes | SHA-256 | Use |
| --- | ---: | --- | --- |
| Targeted refresh v1 | 888 | `c06268899e5cac0330931d68c35b945f829db3a1bdd09c59a168076cade97c70` | Two timed-out full-Hermes precursors |
| Targeted refresh v2 | 2,674 | `29bfa5fb412ebedf75df4c02d1f058410bb92d3d85bb3db79c8d949f41861ed3` | Batch listing and two timed-out core precursors |
| Targeted refresh v3 | 5,607 | `0cc51c1b326700218e2a3b124bfab7043c54fbf7eeb25f86338176057429055c` | Rejected unresolved-edge attempt |
| Targeted refresh v4 | 5,994 | `94d67088f435e805da97c954a0e8c8361407bd84841a5f1ea0a1271441758d95` | Eight accepted code batches; later exact replay wrapper |
| Targeted refresh v5 | 6,353 | `ae2e108995c4641b72da535f2f116d91a8873b9fffdac592c0ee2e65507c2d7b` | Four accepted Markdown/manifest batches |
| Targeted refresh v6 | 6,704 | `3999a9059c30faa545cecc31fd6ab7b83f0f28fe90fd5ae35cee504e7667b1f8` | Manifest save |
| Targeted refresh v7 | 7,885 | `2e80c4266644173d760bbe5d9a8ae7d09718d6005e3877a149f84b6ca735e2ba` | Aggregated HTML export |
| Validator v1 | 7,472 | `d249a26f7f6e8e000836e5a8f3a077d6e12f76356a4aa1c1e9a89bef93714ff9` | Failed absolute-title check |
| Validator v2 | 7,742 | `bc353886bc1ef46396039b4bb8a5660dc1df17b56d4e0dded1111995080c5e1a` | Prior passing structural check |
| Closure metrics v1 | 5,107 | `abb862b0ff4664c5b5a60db3e993f3a86ddb757aeaac94568fbf45fe752e3578` | Initial clone-input comparison |
| Closure metrics v2 | 5,610 | `dfdf275559e9ec7be02b9e057d023b99bde0f07599c7904cfa1c663ab2ec6dc7` | Exact-input sync and determinism metrics |

The original wrapper and validator were deleted on 2026-07-16 and their absence
checks returned exit 0. The closure replay directory, reconstructed wrapper,
metrics helper, cloned inputs, caches and graph copies were deleted after the
comparison. No temporary stdout/stderr logs were created.

### Official internals and custom logic boundary

The fallback did invoke Graphify 0.9.5's own AST and graph machinery:

| Installed source | Module and entry point | Fallback use |
| --- | --- | --- |
| `C:\Users\pablo\anaconda3\Lib\site-packages\graphify\detect.py` | `graphify.detect.CODE_EXTENSIONS`, `_load_graphifyignore`, `_is_ignored`, `_is_sensitive` | Extension, ignore and sensitivity filtering |
| `C:\Users\pablo\anaconda3\Lib\site-packages\graphify\extract.py` | `graphify.extract._get_extractor`, `extract` | Official per-file AST extraction and within-batch cross-file resolution |
| `C:\Users\pablo\anaconda3\Lib\site-packages\graphify\ids.py` | `normalize_id`, `make_id` through extractors | Official node-ID generation |
| `C:\Users\pablo\anaconda3\Lib\site-packages\graphify\watch.py` | `_relativize_source_files` | Repository-relative source paths |
| `C:\Users\pablo\anaconda3\Lib\site-packages\graphify\build.py` | `_norm_source_file`, `dedupe_nodes`, `dedupe_edges`, `build_from_json` | Normalization, deduplication, endpoint resolution and graph build |
| `C:\Users\pablo\anaconda3\Lib\site-packages\graphify\export.py` | `to_json`, later `to_html` | Official NetworkX node-link serialization and aggregated HTML |
| `C:\Users\pablo\anaconda3\Lib\site-packages\graphify\cluster.py` | `cluster` through `graphify cluster-only .` | Community recalculation |

`extract` generated declarations, containment, imports, calls, stubs, node IDs
and relationship dictionaries. `make_id` performs Unicode-aware normalization
of path and symbol components. Ordinary Graphify relationships have no stable
`id`; the installed schema identifies them by endpoints and relation during
`dedupe_edges`, while the final non-multigraph can retain only one relationship
attribute record per endpoint pair. `build_from_json` resolves aliases, prunes
unresolved endpoints and stores original direction in `_src`/`_tgt` before
`to_json` restores it.

The wrapper nevertheless implemented custom behavior. It defined `_batch_for`,
selected files outside a supported CLI command, interpreted the `nodes`,
`links`/`edges`, `hyperedges`, `id` and `source_file` fields, removed selected
source-owned nodes and relationships, manually concatenated preserved and new
records, and constructed the candidate extraction dictionary. It did not use
Graphify's supported `graphify update` path or `build_merge`. It did not create
custom AST nodes, edges, IDs or semantic relation types, but it did implement
custom merge logic and custom schema handling. It therefore must not be called
a supported Graphify command.

Stale Hermes records were removed only for files present in each batch's
`selected_sources` set and for colliding `new_ids`. A deleted, newly ignored or
newly unsupported file was not necessarily included in that set, unlike the
supported update path's deleted-source pruning. Duplicate dictionaries were
resolved through official `dedupe_nodes`, `dedupe_edges` and
`build_from_json`, but wrapper ordering still controlled which attributes
entered those functions.

### Twelve-batch boundary verification

The deterministic batch order and reconstructed inventory are:

| Batch | Included category | Tracked | Extractor-supported | Accepted | Parser ignored | Sensitive skip | Unsupported |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Core | Root non-doc files; `acp_adapter`, `acp_registry`, `agent`, `cron`, `datagen-config-examples`, `gateway`, `hermes_cli`, `providers`, `tools`, `tui_gateway` | 623 | 593 | 584 | 7 | 8 | 24 |
| Extensions | Residual non-doc paths including bootstrap/shared apps, Docker, optional skills, packaging, plugins, scripts, skills, web and website | 905 | 598 | 592 | 82 | 2 | 229 |
| TUI | `ui-tui/**` excluding documentation | 380 | 378 | 378 | 0 | 0 | 2 |
| Desktop | `apps/desktop/**` excluding documentation | 830 | 719 | 718 | 21 | 3 | 88 |
| Gateway tests | `tests/{gateway,cron,docker,tui_gateway,acp,acp_adapter}/**` | 558 | 558 | 556 | 0 | 2 | 0 |
| CLI tests | `tests/{hermes_cli,cli,run_agent}/**` | 644 | 644 | 641 | 0 | 3 | 0 |
| Logic tests | `tests/{agent,tools,plugins,providers}/**` | 630 | 630 | 627 | 0 | 3 | 0 |
| Other tests | Remaining non-document `tests/**` | 189 | 188 | 185 | 0 | 3 | 1 |
| Website docs | `.md`/`.mdx` under `website/**` | 670 | 670 | 663 | 5 | 2 | 0 |
| Optional-skill docs | `.md`/`.mdx` under `optional-skills/**` | 376 | 376 | 376 | 0 | 0 | 0 |
| Skill docs | `.md`/`.mdx` under `skills/**` | 308 | 308 | 308 | 0 | 0 | 0 |
| Other docs/manifests | Remaining Markdown plus `pyproject.toml` | 59 | 59 | 59 | 0 | 0 | 0 |
| **Total** |  | **6,172** | **5,721** | **5,687** | **115** | **26** | **344** |

The 115 parser-ignored files comprise 103 generated paths, five lockfiles, two
environment files and five sensitive-directory paths. Tracked dependency and
cache paths were zero. The 26 sensitivity skips were otherwise non-ignored
paths rejected by Graphify's filename heuristic. Every accepted file was under
`2_products/hermes-agent/**`; batch inputs were bounded by `git ls-files` for
that exact root, so sibling, external, artifact and graph-output candidates were
zero before extraction.

Historical batch stdout contained no worker-failure warning, but the wrapper did
not persist per-file error results or a parse-failure ledger. Exact historical
`parsing_failures` per batch is therefore **not recorded**, not proven zero.
This is a closure defect.

Net graph growth by historical batch was:

| Batch | Extracted node records | Net nodes | Net relationships | Exit |
| --- | ---: | ---: | ---: | ---: |
| Core | 23,152 | 23,075 | 50,641 | 0 |
| Extensions | 10,536 | 10,453 | 20,923 | 0 |
| TUI | 2,960 | 2,954 | 6,856 | 0 |
| Desktop | 5,722 | 5,718 | 16,233 | 0 |
| Gateway tests | 20,079 | 20,033 | 29,821 | 0 |
| CLI tests | 20,688 | 20,668 | 27,147 | 0 |
| Logic tests | 26,047 | 26,019 | 33,459 | 0 |
| Other tests | 5,923 | 5,916 | 8,183 | 0 |
| Website docs | 16,779 | 16,779 | 16,659 | 0 |
| Optional-skill docs | 6,873 | 6,873 | 6,586 | 0 |
| Skill docs | 6,796 | 6,796 | 6,516 | 0 |
| Other docs/manifests | 893 | 893 | 840 | 0 |

Net values are differences between successive graph totals. They are not a
substitute for the missing per-batch raw extraction artifacts.

### Structural integrity closure

The retained `graph.json` has SHA-256
`cb04d5dfdb1414bc40977233c10564c5ab3687400a3ce14e96c1e0c984122d86`.
The installed `graphify.validate.validate_extraction` returned zero errors.

| Check | Result |
| --- | ---: |
| Node records | 151,851 |
| Relationship records | 230,557 |
| Unique nonempty node IDs | 151,851 |
| Duplicate node IDs | 0 |
| Missing or empty node IDs | 0 |
| Relationships carrying an `id` | 0 |
| Unique relationship IDs | 0 |
| Duplicate relationship IDs | 0 |
| Unique unordered endpoint pairs | 230,557 |
| Duplicate endpoint pairs | 0 |
| Dangling relationship sources | 0 |
| Dangling relationship targets | 0 |
| Relationships with both endpoints missing | 0 |
| Invalid nodes under executable 0.9.5 schema | 0 |
| Invalid relationships under executable 0.9.5 schema | 0 |
| Absolute source paths | 0 |
| Unresolved nonempty source paths | 0 |
| `graphify-out/**` self-ingestion paths | 0 |
| Relationships with missing or empty `source_file` | 0 |
| Self-loops | 5 |
| Hyperedges | 0 |

Ordinary relationships intentionally have no stable relationship ID in
Graphify 0.9.5. The executable validator requires `source`, `target`,
`relation`, `confidence` and `source_file`, not an edge `id`. Duplicate
relationship IDs are therefore zero because no such IDs exist; endpoint-pair
and full-record duplicates are also zero.

Graphify's executable schema has no relationship-type whitelist. All thirteen
observed types are emitted or consumed by installed Graphify structural code:
`contains`, `calls`, `method`, `rationale_for`, `references`, `imports`,
`imports_from`, `uses`, `indirect_call`, `inherits`, `re_exports`, `defines`
and `implements`. Unsupported executable relationship types are therefore zero.

There are 1,748 official AST sourceless reference stubs. All have a present but
empty `source_file`, `_origin: ast`, `file_type: code`, at least one incident
relationship and no missing endpoint. Graphify deliberately emits these for
unresolved external, internal-shadow or ambiguous references, and its validator
requires field presence rather than nonempty provenance. Of these stubs, 1,297
have no sourced definition candidate, 407 have one and 44 have multiple. They
are schema-valid but remain a provenance limitation.

There are 7,023 non-ASCII Markdown AST IDs. Installed
`graphify.ids.normalize_id` intentionally preserves Unicode word characters;
all 7,023 round-trip through `normalize_id` and `make_id` and pass the executable
validator. They differ from the narrower ASCII-only semantic prompt, but are
not invalid under installed 0.9.5 behavior.

The five self-loops are four `imports_from` and one `contains` relationship.
The validator and `build_from_json` permit equal endpoints; installed extraction
and alias-remapping paths can produce them. They are structural artifacts, not
dangling or malformed records.

### Baseline preservation closure

Before the original rollback backup was deleted, validator version 2 loaded the
5,674-node baseline and final graph, compared exact ID sets and asserted
`baseline_ids <= final_ids`. The recorded result was `5,674/5,674`. This was a
direct set comparison, not a count-only comparison.

That validation did **not** persist the baseline ID list, node dictionaries,
source-path map or endpoint/relation set. The raw baseline was subsequently
deleted during the prior cleanup. Consequently:

| Baseline question | Closure result |
| --- | --- |
| Baseline node ID set retained | Previously compared directly: 5,674/5,674 |
| Baseline relationship IDs retained | Not applicable; Graphify relationships have no IDs |
| Baseline endpoint/relation set retained | Unproven; raw baseline no longer available |
| Baseline nodes unexpectedly changed | Unproven; prior validator compared IDs only |
| Baseline nodes unexpectedly removed | No missing ID observed in prior direct set check |
| Baseline source-path changes | Unproven; prior source attributes were not retained |
| Exact baseline/Hermes ID duplicates | 0 in final graph, but attribute overwrite cannot be ruled out from the retained evidence |
| Community reassignment | Derived metadata only; `cluster-only` does not rewrite node IDs |

The inability to reproduce node attributes, source ownership and baseline
relationships means the broad claim "all baseline nodes retained unchanged" is
not proven. This independently blocks Condition A.

### Representative Hermes coverage

Incident relationships count each final relationship once when either endpoint
belongs to the selected source nodes. No raw source content was copied into this
record.

| Area and source selector | Present files | Nodes | Incident relationships | Bounded structural examples | Dimensions present |
| --- | ---: | ---: | ---: | --- | --- |
| `hermes_cli/web_server.py` | 1 | 766 | 3,419 | `uses`, `calls`, `contains`, `imports_from` | Imports, calls, definitions, containment |
| `gateway/platforms/api_server.py` | 1 | 207 | 558 | `calls`, `method`, `contains`, `imports_from` | Imports, calls, definitions, containment |
| `plugins/kanban/dashboard/plugin_api.py` | 1 | 121 | 263 | `calls`, `contains`, `references`, `imports_from` | Imports, calls, definitions, containment |
| Runtime Overview: `web/src/agent-platform/runtime-overview/**` | 6 | 30 | 77 | `contains`, `re_exports`, `imports`, `calls` | Imports, calls, definitions, containment |
| Projects and Tickets: `web/src/agent-platform/projects-tickets/**` | 9 | 110 | 376 | `calls`, `contains`, `imports`, `indirect_call` | Imports, calls, definitions, containment |
| Approval Inbox: `web/src/agent-platform/approval-inbox/**` | 8 | 90 | 235 | `contains`, `calls`, `imports`, `re_exports` | Imports, calls, definitions, containment |
| Execution Inspector: `web/src/agent-platform/execution-inspector/**` | 8 | 87 | 260 | `calls`, `contains`, `imports`, `re_exports` | Imports, calls, definitions, containment |
| Shared package: `apps/shared/**` | 5 | 63 | 98 | `contains`, `re_exports`, `calls`, `imports` | Imports, calls, definitions, containment |
| Frontend routing: `web/src/App.tsx`, `main.tsx`, `agent-platform/extensions.ts`, `agent-platform/shell/navigation.ts` | 4 | 53 | 178 | `imports_from`, `contains`, `imports`, `calls` | Imports, calls, definitions, containment |
| Current root tests: `tests/**` | 2,011 | 72,077 | 98,617 | `method`, `calls`, `contains`, `imports_from` | Imports, calls, definitions, containment |

The canonical `apps/shared/**` source supplied shared-package evidence. The
ignored `node_modules/@hermes/shared` junction supplied none.

### Relationship density and connectivity

The retained graph is not primarily isolated syntax nodes, but its connectivity
does not cure the provenance and determinism failures.

```yaml
nodes: 151851
relationships: 230557
relationships_per_node: 1.5183107124747286
mean_undirected_degree: 3.036621424949457
isolated_nodes: 77
zero_degree_nodes: 77
connected_components: 1913
largest_component_nodes: 102499
largest_component_relationships: 177852
largest_component_node_share_percent: 67.49972012038117
intra_file_relationships: 191331
inter_file_relationships: 29041
unclassified_empty_endpoint_source: 10185
intra_subsystem_relationships: 213776
cross_subsystem_relationships: 6596
hermes_to_platform_baseline_relationships: 0
```

Subsystem is the first component after `2_products/hermes-agent/`; non-Hermes
sources form the platform-baseline subsystem. All 6,596 classified
cross-subsystem relationships connect different Hermes top-level components.

Relationship counts by type:

| Rank | Relation | Count |
| ---: | --- | ---: |
| 1 | `contains` | 74,350 |
| 2 | `calls` | 55,293 |
| 3 | `method` | 35,856 |
| 4 | `rationale_for` | 33,681 |
| 5 | `references` | 10,394 |
| 6 | `imports` | 8,133 |
| 7 | `imports_from` | 6,999 |
| 8 | `uses` | 2,520 |
| 9 | `indirect_call` | 2,036 |
| 10 | `inherits` | 662 |
| 11 | `re_exports` | 505 |
| 12 | `defines` | 126 |
| 13 | `implements` | 2 |

### Three-batch determinism check

The exact 5,994-byte version 4 wrapper was reconstructed with SHA-256
`94d67088f435e805da97c954a0e8c8361407bd84841a5f1ea0a1271441758d95`
and run only in
`C:\Users\pablo\AppData\Local\Temp\opencode\graphify-scope-01-close-20260717\repo-longpaths`.
The isolated clone used transient `core.longpaths=true`; the first clone that
failed Windows long-path checkout was quarantined and never used for extraction.
Selected source files were synchronized byte-for-byte from the workspace before
replay. The current graph was copied as an immutable seed. Every replay used
Graphify 0.9.5, the same Python executable, same rule file, same wrapper,
300,000 ms timeout and exit code 0.

Exact input hashes:

| Batch | Files | Input SHA-256 |
| --- | ---: | --- |
| Backend Python `core` | 584 | `c7bdf5cd3b564d0e92bf0e346be25fd14ee32e3b37a3fbd3e05cefc1e8ca61cf` |
| Frontend `apps-desktop` | 718 | `5adda7377a6765c3d0f5746f613ff1abe7f707579990030fc4eebeebece3fa69` |
| Extension/test `tests-logic` | 627 | `6e09676bebde886b120bb4245e7beca42c2c84ccce5e3fdd4a4e720db5e418a6` |

Determinism comparison:

| Batch/result | Selected nodes | Node-ID-set SHA-256 | Owned relationships | Endpoint/type-set SHA-256 | Normalized content SHA-256 | Full graph SHA-256 |
| --- | ---: | --- | ---: | --- | --- | --- |
| `core` accepted graph | 22,365 | `3ba6bf33b64be9e548bbf7d6a5c59f96a713aa5e6add50d9356253700dba173b` | 50,641 | `465013b3f2fadffe2b9778c070f19014b16aaa630b3a6158764334513cbacae5` | `43204f1f9214f5818ad115ee1e6da91ca90fbec3280b73bb5b620a2c4aa33128` | `cb04d5dfdb1414bc40977233c10564c5ab3687400a3ce14e96c1e0c984122d86` |
| `core` replay A | 22,365 | `c3e5995c4b0c8294c8acba0e6c1156db0dda02a256619703a2d63f8b101d444d` | 50,804 | `130d2b9246179741b08d18becdf6b0e6a2d3b4edeed43b2cae56560e91a76bda` | `0bcadd658c8e593d8a06ee38e57e703101ad1ab6fd2bda22e82755be822be451` | `9a7f5f8f350c5373fb205bc6d3648e3d6f7729fe39530f3d6e59e1301b8bd583` |
| `core` replay B | 22,365 | `c3e5995c4b0c8294c8acba0e6c1156db0dda02a256619703a2d63f8b101d444d` | 50,804 | `a2f7144fdf9b2c4d8f838b62470f02b6fcc990c70ef7a1b76995d39309520087` | `f5a3040e65d0ca6b8277bf409e8cb90e62b0a4994c5bfe69b3a122185b016eed` | `ca52a2b7c632c89e9b9cab25ff1ace3d1cd8aa3ed8bd9969eac163a2c38a7cfa` |
| `apps-desktop` accepted graph | 5,718 | `dd9bd0fbd63879d748411655da701494888b13af86397af29572ab3176ce0ef5` | 16,233 | `da41ec6cfea015c87f8caef5ca81103704a1abab80b7b39ac8993e8f3f56acd1` | `cfdfdb46c7ba705177e7109408576a52db485fa4ee5dd2b19b32b5a29ba68cea` | `cb04d5dfdb1414bc40977233c10564c5ab3687400a3ce14e96c1e0c984122d86` |
| `apps-desktop` replay A | 5,718 | `dd9bd0fbd63879d748411655da701494888b13af86397af29572ab3176ce0ef5` | 16,233 | `e475718a4629ddbb93621c869ac84d891ead36c5c63df96be17f4915e5354b80` | `f60d55d5c08e9903a5c008c2af0b8f6bf916950cac183a5db9d095633166e4ac` | `9cc8203240cd48b14a909592253c484a5dfddc14ea0200bd36724528b341a895` |
| `apps-desktop` replay B | 5,718 | `dd9bd0fbd63879d748411655da701494888b13af86397af29572ab3176ce0ef5` | 16,233 | `e475718a4629ddbb93621c869ac84d891ead36c5c63df96be17f4915e5354b80` | `f60d55d5c08e9903a5c008c2af0b8f6bf916950cac183a5db9d095633166e4ac` | `9cc8203240cd48b14a909592253c484a5dfddc14ea0200bd36724528b341a895` |
| `tests-logic` accepted graph | 25,869 | `b2f8227cc8ce895c339552ed4266634279c634a095f5d1601f1278806c5803fc` | 33,459 | `da723ea619a66701b37cf33230774c695e99f1491c8e73dacddaaee5c7736e04` | `8d65362ca2d54be6c387ff247948aef72edd3907b189a49fcfb30e6766a6a054` | `cb04d5dfdb1414bc40977233c10564c5ab3687400a3ce14e96c1e0c984122d86` |
| `tests-logic` replay A | 25,869 | `b2f8227cc8ce895c339552ed4266634279c634a095f5d1601f1278806c5803fc` | 33,459 | `98d6f43f724b583ac83c9425380c9792d3acc325bccdbbebee4559b457c0ce29` | `12e80b186ccb2f753b12079292e524f510f9d0c4d7cb48d7cfda737b82f50daf` | `3c2176ddb53a227b89ed7403a80d6ddde47456390df4aa03c9acdb8b29a0d31b` |
| `tests-logic` replay B | 25,869 | `b2f8227cc8ce895c339552ed4266634279c634a095f5d1601f1278806c5803fc` | 33,459 | `2ee9b893d93cd4a6f3790ef6ba2ca5405b40fbc08d49d2bf76d752492ac74a42` | `3b45da04d54c2166995f16302e6a8ef0794d271018ace2e5c65726defb9b856a` | `b70ec63a0293e8b20be36b0713e19e7e5d65d4097a450ddad932d872f7c2e694` |

`apps-desktop` replay A and B are equal to each other, but their relationship
and normalized hashes do not equal the accepted graph. `core` and `tests-logic`
fail equality between replay A and B. A third warm-cache `core` replay also
produced a third relationship and normalized hash. Node counts alone therefore
conceal relationship nondeterminism. Required deterministic equality fails for
two of three batches, and no replay exactly reproduces the accepted relationship
subset in any of the three areas.

The workspace `graphify-out/graph.json` remained byte-identical at
`cb04d5dfdb1414bc40977233c10564c5ab3687400a3ce14e96c1e0c984122d86`
throughout replay. The complete temporary closure directory was deleted and no
replay process or temporary output remains.

### Ignore-policy closure

Before GRAPHIFY-SCOPE-01, the final relevant rules were:

```gitignore
4_external/sources/**
9_artifacts/**
graphify-out/**
2_products/**
product/**
products/**
```

The candidate appends ordered last-match rules:

```gitignore
/2_products/
/2_products/**
!/2_products/
!/2_products/hermes-agent/
!/2_products/hermes-agent/**
```

It then reasserts unanchored dependency, environment, cache, build, generated,
runtime, credential, sensitive, binary/media and lockfile exclusions. Installed
Graphify 0.9.5 loads `.gitignore` first and `.graphifyignore` second, evaluates
all rules in order with last match winning, and requires excluded parent paths
to be reopened. Eighteen representative installed-parser checks passed.

Current direct-product admission:

| Direct child | Manifest | Node sources | Relationship sources |
| --- | ---: | ---: | ---: |
| `backend-energyplus` | 0 | 0 | 0 |
| `cli` | 0 | 0 | 0 |
| `desktop` | 0 | 0 | 0 |
| `experimental` | 0 | 0 | 0 |
| `hermes-agent` | 5,687 | 144,443 | 223,864 |
| `omniverse-app` | 0 | 0 | 0 |
| `web-platform` | 0 | 0 | 0 |

Final graph and manifest checks also found zero `4_external/**`,
`9_artifacts/**`, `graphify-out/**`, `node_modules/**`, `.venv/**`, generated
bundle, runtime-state, credential, `.env*`, cache or local-database source paths.

### Future refresh procedure

The custom twelve-batch wrapper is not an approved future refresh procedure.
A separate ticket is required:

```text
GRAPHIFY-SCALE-01 - Supported Scalable Hermes Extraction and Provenance Pipeline
```

That ticket must either make the official `graphify update .` command complete
within the governed bound or establish an upstream-supported scalable interface.
It must use official detection and sensitive filtering, official extraction,
`build_merge` or another supported source-replacement path, deleted-source
pruning, explicit cache-state controls and official serialization. It must
persist the authorized file manifest, per-batch raw extraction artifacts,
parser-failure ledger, exact stdout/stderr and exit status, baseline graph,
baseline node/source/relationship sets, merge-order evidence, normalized
determinism hashes and rollback copy until closure is accepted.

Future acceptance requires at least two cold and two warm deterministic runs,
stable node IDs and endpoint/relation sets, stable output after documented
normalization, zero unauthorized paths, direct baseline attribute/source/edge
comparison, and no custom interpretation that bypasses Graphify source
replacement semantics.

The current fallback parsed Markdown headings and links through Graphify's
deterministic `extract_markdown` AST path. It did **not** run the full Markdown
semantic/LLM extraction pipeline. Ordinary YAML, text, CSS, CommonJS `.cjs` and
other unsupported or semantic-only inputs were not semantically refreshed.
`graph.html` remains a community-aggregated view; the structured graph, not the
HTML node count, was used for this closure audit.

## Evidence Classification and Limitations

The resulting graph remains local generated supporting evidence. It is not a
source of truth, architecture authority, semantic-memory substrate, approval
authority, runtime input, provider input or deployment artifact. AST extraction
can omit unsupported syntax, lose semantic intent, deduplicate identities or
produce incomplete cross-file relationships. Scope admission proves only that
eligible first-party files may be scanned; it does not prove complete source or
concept coverage.

The 5,687 Hermes manifest entries produced 5,643 represented source paths; 44
eligible files produced no source-attributed node. The fallback performs
cross-file resolution within each bounded subsystem batch, but inferred
relationships across batch boundaries may be incomplete. The report was
generated in cluster-only mode, so its corpus section does not carry full file
statistics. Community labels are deterministic hub labels, not semantic LLM
labels. These are recorded limitations for local exploratory evidence only.

No authority is granted for Hermes execution, provider/model use, credentials,
network calls, autonomous agents, WorkPacket/Paperclip/GBrain integration,
publication, redistribution, production deployment, staging, commit or push.

## Final Decision

GRAPHIFY-SCOPE-01 is **not accepted for commit**. The candidate ignore policy
correctly opens only `2_products/hermes-agent/**`, and the retained graph passes
the executable structural and scope checks, but the fallback is custom and
unproven. Two of three required replay batches failed relationship determinism;
all three accepted-graph relationship subsets differed from replay; per-batch
parse/error and intermediate-output evidence was not persisted; and the deleted
raw baseline prevents complete baseline attribute, source and relationship
comparison.

`.graphifyignore` and this governance record remain unstaged candidate changes.
`graphify-out/**` remains local provisional experimental evidence and is
noncanonical. No product, runtime, provider, publication, authority, staging,
commit or push posture changes. Future refresh acceptance is blocked on
GRAPHIFY-SCALE-01.

Result marker:

```text
graphify_hermes_scope_fallback_unproven
```

## GRAPHIFY-SCALE-01 Supersession

GRAPHIFY-SCALE-01 completed on 2026-07-18 and supersedes the fallback limitation
recorded above. The maintained Graphify 0.9.5 adapter at
`10_scripts/graphify/refresh_hermes_graph.py` passed a governed baseline run,
two cold runs, two warm runs, exact structural determinism, direct baseline
node/relationship preservation, current source-inventory checks, official
manifest coverage, zero-node fresh extraction audits, official clustering and
HTML export, provenance generation and atomic promotion with retained rollback.

The accepted graph contains 151,132 nodes, 263,635 relationships and 5,257
communities. No sibling product, external source, dependency tree, generated
output, sensitive path, absolute path, noncanonical path or unmanifested source
was admitted. The final `graph.json` SHA-256 is
`02e3e4c8b32e77e6e71d8f6fdfb5cc647309b55713a3327c2534c2dace0291a2`.

The prior twelve-batch temporary wrapper remains prohibited. Future refreshes
must use the maintained adapter and retain its evidence, determinism,
provenance, promotion and rollback gates. Full details are recorded in
`agent_platform_graphify_scalable_refresh_pipeline.md`.

Current result marker:

```text
graphify_hermes_scope_supported_pipeline_accepted
```
