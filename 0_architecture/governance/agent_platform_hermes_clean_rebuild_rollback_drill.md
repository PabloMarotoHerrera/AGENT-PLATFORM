# P12.7 - Hermes Clean Rebuild and Rollback Drill

## Document Header

| Field | Value |
| --- | --- |
| Project | P12 - Hermes Productization Foundation |
| Ticket | P12.7 - Hermes Clean Rebuild and Rollback Drill |
| Status | `clean_rebuild_and_rollback_drill_passed` |
| Date | 2026-07-13 |
| Canonical output | `0_architecture/governance/agent_platform_hermes_clean_rebuild_rollback_drill.md` |
| Product root | `2_products/hermes-agent` |
| Upstream reference | `4_external/sources/hermes-agent` |
| Drill artifact root | `9_artifacts/hermes/p12.7` |
| P12.6 commit | `d5dfba5edcfff052150d173531539f7a392b0f57` |
| P12.6 parent | `dcc110229e2fbc7e45095a129ced3976793b5200` |
| Pre-P12.6 product tree | `07bc27d2cc3b015b3865d62d7fdbc7dfe0ab6fb7` |
| Post-P12.6 product tree | `274527e686fa50a320a92a5738e8c8c083669b24` |
| Execution actor | OpenCode agent under human commit control |

## Purpose

P12.7 proves that the committed Hermes product can be rebuilt from frozen
dependency authority and that the complete P12.6 product divergence can be
removed and reapplied mechanically in an isolated ignored projection.

The drill removes only exact generated roots. It never rewrites the actual
tracked product source for rollback simulation. It performs no provider/model
request, credential use, OAuth, MCP startup, gateway startup, worker execution,
agent task, upstream synchronization, staging, commit or push.

## P12.6 Prerequisite Status

| Gate | Evidence | Result |
| --- | --- | --- |
| P12.6 record exists and is committed | Commit `d5dfba5edcfff052150d173531539f7a392b0f57` | Pass |
| P12.6 status | `product_extension_configuration_seams_ready` | Pass |
| P12.6 record and product paths share history | Same commit, with 15 product paths | Pass |
| Current branch | `main` | Pass |
| Accepted main | `HEAD == origin/main == d5dfba5edcfff052150d173531539f7a392b0f57` | Pass |
| Index | Zero staged paths | Pass |
| Product status | Zero status paths | Pass |
| Product tracked count | 6,132 | Pass |
| Product tree | `274527e686fa50a320a92a5738e8c8c083669b24` | Pass |
| Nested product Git | Absent | Pass |
| P12.2 controls | Accepted hashes matched | Pass |
| P12.3 manifests/locks | Accepted hashes matched | Pass |
| P12.6 modification register | 18 columns, 14 rows, zero hash mismatch | Pass |
| Locked upstream | Clean at `9de9c25f620ff7f1ce0fd5457d596052d5159596` | Pass |
| Candidate checkout | Absent | Pass |
| Synchronization workspace | Absent | Pass |

The only unrelated untracked paths were `.opencode/`, `AGENTS.md` and
`graphify-out/`. They were not modified or staged. Graphify was not used.

## Secret-Scanning Gate

The two P12.2 import alerts were verified through explicit human confirmation.
No GitHub credential was used and no fixture value was read, copied, printed or
retained by P12.7.

```yaml
HermesSecretScanningGate:
  openai_fixture_alert_reviewed: true
  openai_fixture_alert_disposition: used_in_tests
  telegram_fixture_alert_reviewed: true
  telegram_fixture_alert_disposition: used_in_tests
  recognized_as_real_user_credential: false
  imported_unchanged_from_locked_upstream: true
  human_disposition_recorded: true
  active_unresolved_secret_alerts_for_P12_scope: false
  github_credential_used_by_agent: false
```

The human confirmed that both alerts represent unchanged locked-upstream test
fixtures, not active user credentials, and that no unresolved P12 secret alert
remains.

## Initial Repository and Product Identity

```yaml
P12_7_InitialState:
  branch: main
  head: d5dfba5edcfff052150d173531539f7a392b0f57
  head_matches_origin_main: true
  index_empty: true
  product_status_clean: true
  product_tree: 274527e686fa50a320a92a5738e8c8c083669b24
  product_tracked_files: 6132
  nested_git_present: false
  source_drift_detected: false
  lockfile_drift_detected: false
  modification_register_sha256: 8fd06e54ff4fb6f1b3368dd366783808da620a32cf5d6721a4315d567afbcaab
```

Initial committed inventory:

- `committed-product-ls-tree-before.txt`: 6,132 mode/blob/path rows, SHA-256
  `ca7b88950eaf6c82c38381ba4f922c6109c895ef617cb8a794d643f2cf8c0224`;
- `actual-product-sha256-before.tsv`: 6,132 path/hash/size rows, SHA-256
  `ad0ee1c37bf2e161debf76f8c48785adfa9a5b9f17cc20fe8aa2efad34d470af`.

## Generated-State Inventory

Every root was checked for existence, ignore posture, tracked/staged paths,
root reparse status and contained reparse entries before deletion.

| Root | Exists before | Ignored | Tracked | Staged | Root reparse | Contained reparse | Ownership | Delete | Recreate |
| --- | --- | --- | ---: | ---: | --- | ---: | --- | --- | --- |
| `.venv` | Yes | Yes | 0 | 0 | No | 0 | P12.3 | Yes | Yes |
| `node_modules` | Yes | Yes | 0 | 0 | No | 6 | P12.3 | Yes | Yes |
| `hermes_agent.egg-info` | Yes | Yes | 0 | 0 | No | 0 | P12.3 | Yes | Yes |
| `.pytest_cache` | Yes | Yes | 0 | 0 | No | 0 | P12.4/P12.6 | Yes | Produced by validation |
| `hermes_cli/web_dist` | Yes | Yes | 0 | 0 | No | 0 | P12.4/P12.6 | Yes | Yes |
| `ui-tui/dist` | Yes | Yes | 0 | 0 | No | 0 | P12.4 | Yes | Yes |
| `ui-tui/packages/hermes-ink/dist` | Yes | Yes | 0 | 0 | No | 0 | P12.4 | Yes | Yes |
| `apps/desktop/dist` | Yes | Yes | 0 | 0 | No | 0 | P12.4 | Yes | Yes |
| `apps/desktop/build` | Yes | Yes | 0 | 0 | No | 0 | P12.4 | Yes | Yes |
| `.ruff_cache` | Yes | Root not ignored; contents self-ignore | 0 | 0 | No | 0 | P12.4/P12.6 | No | Not required |
| `.mypy_cache` | No | N/A | 0 | 0 | No | 0 | N/A | No | No |
| `.ty_cache` | No | N/A | 0 | 0 | No | 0 | N/A | No | No |
| `coverage` | No | N/A | 0 | 0 | No | 0 | N/A | No | No |

No additional source-tree `__pycache__`, Ruff, mypy, ty or coverage root was
found outside the declared generated roots. `9_artifacts/hermes/p12.7` was
created as a new ignored, untracked, unstaged P12.7 evidence root.

Before deletion, `.venv` contained 15,642 files, `node_modules` contained
93,322 ordinary files, and all six `node_modules` reparse entries were the
expected workspace junctions:

```text
node_modules/@hermes/bootstrap-installer
node_modules/@hermes/ink
node_modules/@hermes/shared
node_modules/hermes
node_modules/hermes-tui
node_modules/web
```

Every target resolved to a tracked workspace inside the product root. External
reparse target count was zero.

## Generated-State Removal

The exact removal set was:

```text
2_products/hermes-agent/.venv
2_products/hermes-agent/node_modules
2_products/hermes-agent/hermes_agent.egg-info
2_products/hermes-agent/.pytest_cache
2_products/hermes-agent/hermes_cli/web_dist
2_products/hermes-agent/ui-tui/dist
2_products/hermes-agent/ui-tui/packages/hermes-ink/dist
2_products/hermes-agent/apps/desktop/dist
2_products/hermes-agent/apps/desktop/build
```

The standard-library inline deletion routine used `os.scandir`, inspected
Windows reparse attributes and `os.path.isjunction`, refused external targets,
removed reparse entries without traversal and accepted only the exact root
allowlist.

The first pass removed `.venv`, three workspace junctions and part of
`node_modules`, then Windows denied deletion of a native Tailwind module loaded
by VS Code PID 6276. The agent did not terminate the unrelated editor. Human
restart released the module. The same contained retry removed the remaining
three junctions and all remaining allowlisted roots.

Deletion evidence:

```yaml
HermesGeneratedStateRemoval:
  exact_roots_expected: 9
  exact_roots_absent_after_retry: 9
  expected_workspace_junctions: 6
  workspace_junctions_removed_without_target_traversal: 6
  external_reparse_targets: 0
  tracked_paths_removed: 0
  staged_paths_removed: 0
  product_status_paths_after_removal: 0
  product_tracked_files_after_removal: 6132
  product_sha_inventory_unchanged: true
```

The 6,132-row source inventory after removal was byte-identical to the initial
inventory.

## Python Environment Reconstruction

The exact authority was Python `3.12.3`, temporary uv `0.11.6`, `pyproject.toml`,
`uv.lock`, and extras `all` plus `dev`.

Executed sequence:

```text
C:/Users/pablo/anaconda3/python.exe -m venv C:/Users/pablo/AppData/Local/Temp/opencode/p12_7_uv_bootstrap
<bootstrap>/Scripts/python.exe -m pip install --disable-pip-version-check --no-input --index-url https://pypi.org/simple uv==0.11.6
<bootstrap>/Scripts/uv.exe lock --check
<bootstrap>/Scripts/uv.exe sync --frozen --python C:/Users/pablo/anaconda3/python.exe --extra all --extra dev
<bootstrap>/Scripts/uv.exe sync --frozen --check --python .venv/Scripts/python.exe --extra all --extra dev
```

All five commands exited 0. The rebuild prepared and installed 107 locked
packages plus the editable product. The recreated environment reports Python
`3.12.3` and 108 installed distributions. `hermes_agent.egg-info` contains six
generated files.

The uv environment intentionally has no standalone `pip.exe` or executable
`pip.__main__`. The direct `python -m pip check` form is therefore unavailable.
The lock-authority equivalent `uv pip check --python .venv/Scripts/python.exe`
checked all 107 packages and reported all installed packages compatible.

## Node Environment Reconstruction

The exact authority was Node `24.12.0`, npm `11.6.2`, `package.json`,
`package-lock.json` and `npm ci` from the product root.

The child process environment was cleared. npm used an empty P12.7 user config,
the explicit public registry `https://registry.npmjs.org/`, disabled audit/fund
side requests, and reused the standard external npm cache without purging it.

```yaml
HermesNodeReconstruction:
  node_version: 24.12.0
  npm_version: 11.6.2
  npm_ci_exit: 0
  packages_added: 1300
  npm_ls_exit: 0
  npm_query_exit: 0
  npm_query_entries: 1301
  workspace_junctions: 6
  external_junction_targets: 0
```

The known five optional/platform packages remain reported as extraneous by
`npm ls`, matching the P12.3 fingerprint. npm also repeated upstream deprecation
warnings for `inflight`, `rimraf@2`, `glob@7`, `boolean` and `rcedit`; these did
not fail installation or change the lock.

## Frozen Environment Verification

```yaml
HermesFrozenEnvironmentVerification:
  python_environment_ready: true
  node_environment_ready: true
  uv_lock_check_passed: true
  uv_frozen_check_passed: true
  uv_pip_check_passed: true
  python_distribution_count: 108
  npm_dependency_check_passed: true
  npm_query_succeeded: true
  source_modified: false
  lockfiles_modified: false
```

`uv lock --check` resolved 233 packages and exited 0. The final frozen check
checked 107 packages and reported `Would make no changes`.

## Package Sources Contacted

Only previously authorized public package sources were configured:

```text
https://pypi.org/simple
https://files.pythonhosted.org
https://registry.npmjs.org/
```

The uv bootstrap and frozen sync logs explicitly report downloads from the
configured public Python index/file host. The Python sync downloaded/prepared
107 packages. npm output does not distinguish cache hits from registry fetches;
the only configured registry was the public npm registry, and installation
added 1,300 packages in approximately one minute. No private registry, Git
dependency, package credential, provider endpoint or model endpoint was used.

## Clean Build Reconstruction

All selected output roots were absent before these commands ran:

```text
npm run --prefix web build
npm run --prefix ui-tui/packages/hermes-ink build
npm run --prefix ui-tui build
npm run --prefix apps/desktop build
```

| Output root | Files | Aggregate SHA-256 | Result |
| --- | ---: | --- | --- |
| `hermes_cli/web_dist` | 21 | `77c564a33037935c9a73266e88e1ed46191ffbfa68064207c1b2f0a28db53c2a` | Pass |
| `ui-tui/packages/hermes-ink/dist` | 1 | `6cce96627a5087a523cec495cdc0c92873ae233e94d2913a36c3bf6585d5d537` | Pass |
| `ui-tui/dist` | 1 | `1dd4f22e3923689e4d2b5c4c0e83d18cb631f20efb07281f5745036227fa4893` | Pass |
| `apps/desktop/build` | 201 | `8e246534bbaac3c2b2e41fdaf9fda6edc8052dd3d51764f4eb7a6d7cd66708cc` | Pass |
| `apps/desktop/dist` | 80 | `01dec0f356c85b438d52e576ec01d6d956e0b7c48c43cdaa94020155f6bff340` | Pass |

All roots are ignored, untracked and unstaged. Dashboard and desktop repeated
their accepted large-bundle warnings; desktop also repeated one generated-CSS
warning and large icon-barrel warning. Desktop `assert-dist-built` passed.

## Targeted P12.6 Validation

| Lane | Result |
| --- | --- |
| P12.6 Python schema/route tests | 16 passed |
| P12.6 focused frontend tests | 13 passed |
| Full dashboard tests | 8 files, 46 tests passed |
| Dashboard typecheck | Pass |
| Affected frontend ESLint | Pass, zero findings |
| Dashboard production build | Pass |
| Ruff on affected Python scope | Pass |
| Windows-footgun scanner | Pass, 755 files scanned |

The Python tests ran in a cleared environment with isolated temporary HOME and
`HERMES_HOME`; no provider or user state was inherited.

## P12.4 Green-Anchor Comparison

| P12.4 anchor | P12.7 result | Classification |
| --- | --- | --- |
| Frozen Python dependency validation | Lock, frozen and compatibility checks pass | Unchanged |
| Root npm dependency integrity | `npm ls --all --depth=0` exits 0 | Unchanged |
| `ui-tui` typecheck | Pass | Unchanged |
| Dashboard `web` typecheck | Pass | Unchanged |
| Bootstrap installer typecheck | Pass | Unchanged |
| Desktop typecheck | Pass | Unchanged |
| Shared package typecheck | Pass | Unchanged |
| Dashboard tests | 46 passed | Unchanged green result; expanded P12.6 coverage |
| Dashboard build | Pass | Unchanged |
| Hermes Ink build | Pass | Unchanged |
| TUI build | Pass | Unchanged |
| Desktop frontend build | Pass | Unchanged |
| Provider-null readiness | Pass | Unchanged |
| Source/lock drift absence | Pass | Unchanged |

Known P12.4 non-green Python, full-project lint and desktop test lanes were not
rerun or reclassified because clean environment reconstruction did not alter
their tracked inputs.

## Provider-Null Runtime Reconstruction

The rebuilt dashboard ran with a fully cleared child environment and isolated
P12.7 HOME, APPDATA, LOCALAPPDATA, TEMP, shared-auth and Hermes-home roots.
A current synthetic update-check cache prevented an update network request.
Only a synthetic dashboard session token was present.

```yaml
HermesProviderNullRuntimeReconstruction:
  command: .venv/Scripts/python.exe -m hermes_cli.main dashboard --host 127.0.0.1 --port 0 --no-open --skip-build
  controller_pid: 27432
  dashboard_pid: 15424
  bound_port: 55630
  started_utc: 2026-07-13T19:05:20.796520+00:00
  ready_utc: 2026-07-13T19:05:23.506886+00:00
  root_http: 200
  root_bytes: 707
  status_http: 200
  product_configuration_http: 200
  unauthenticated_product_configuration_http: 401
  gateway_running: false
  active_agents: 0
  isolated_hermes_home_confirmed: true
  browser_opened: false
  provider_request_attempted: false
  model_request_attempted: false
  oauth_attempted: false
  mcp_started: false
  worker_started: false
  agent_task_started: false
```

Product configuration response:

```yaml
product_id: agent-platform-hermes
product_version: 0.1.0-dev
upstream_version: 0.18.2
agent_platform.product_ui: disabled
extension_modules_count: 0
```

No visible shell changed from P12.4, so no manual browser inspection was
required. No Chrome probe, browser automation or screenshot acquisition ran.

## Shutdown Validation

```yaml
HermesP12_7Shutdown:
  shutdown_requested_utc: 2026-07-13T19:05:24.442136+00:00
  graceful_ctrl_break_sent: true
  graceful_exit_within_20_seconds: true
  exact_owned_tree_fallback_used: false
  dashboard_exit_code: 3
  dashboard_process_remaining: false
  child_process_remaining: false
  port_55630_listening_after_cleanup: false
  unmanaged_process_terminated: false
```

Exit code 3 is the Windows control-break termination status. The graceful path
completed within the allowed interval, so no force fallback was needed.

## Modification-Register Reconciliation

```yaml
HermesModificationRegisterReconciliation:
  path: 2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
  sha256: 8fd06e54ff4fb6f1b3368dd366783808da620a32cf5d6721a4315d567afbcaab
  required_columns: 18
  observed_columns: 18
  expected_rows: 14
  observed_rows: 14
  registered_hash_mismatches: 0
  invalid_change_classes: 0
  owner_ticket_mismatches: 0
  empty_rollback_targets: 0
  empty_reapplication_predicates: 0
  empty_validation_lane_ids: 0
  modified_preimage_object_mismatches: 0
```

P12.6 commit reconciliation:

```yaml
P12_6_CommitReconciliation:
  commit: d5dfba5edcfff052150d173531539f7a392b0f57
  parent: dcc110229e2fbc7e45095a129ced3976793b5200
  changed_product_paths: 15
  product_additions_including_self_exempt_register: 12
  upstream_derived_modifications: 3
  product_deletions: 0
  unregistered_paths_excluding_self_exempt_register: 0
  canonical_record_in_same_commit: true
```

## Pre-P12.6 Product Reconstruction

The product subtree was enumerated with `git ls-tree -rz` from the parent tree
and every byte was read with `git cat-file --batch`. No mutable product working
tree byte was copied.

```yaml
HermesPreP12_6Projection:
  source_commit: dcc110229e2fbc7e45095a129ced3976793b5200
  expected_product_tree: 07bc27d2cc3b015b3865d62d7fdbc7dfe0ab6fb7
  computed_product_tree: 07bc27d2cc3b015b3865d62d7fdbc7dfe0ab6fb7
  expected_files: 6120
  actual_files: 6120
  mode_100644_files: 6061
  mode_100755_files: 59
  path_set_matches: true
  modes_match: true
  hashes_match: true
  nested_git: false
  reparse_points: 0
  inventory_sha256: 171204e54c39bb11db7e221a18967b2a9f626dd4d75ccd992da5ccdd7ed4d990
```

## Post-P12.6 Product Reconstruction

```yaml
HermesPostP12_6Projection:
  source_commit: d5dfba5edcfff052150d173531539f7a392b0f57
  expected_product_tree: 274527e686fa50a320a92a5738e8c8c083669b24
  computed_product_tree: 274527e686fa50a320a92a5738e8c8c083669b24
  expected_files: 6132
  actual_files: 6132
  mode_100644_files: 6073
  mode_100755_files: 59
  path_set_matches: true
  modes_match: true
  hashes_match: true
  nested_git: false
  reparse_points: 0
  inventory_sha256: 55a5da7cfe4ee5e5f1f9be59048be50b5262a3babb3cc034fb6bf9af2c78c9d7
```

The initial materializer encountered one path beyond the legacy Windows
260-character API limit. The two exact projection roots were removed and the
same object algorithm was rerun with Windows extended-length prefixes. No path
was omitted or shortened.

## Isolated Rollback Drill

The rollback operation was derived from the exact P12.6 commit diff and register,
not filename guesses. Starting from a byte-identical post-P12.6 projection, it:

1. removed the exact 12 commit additions, including the self-exempt register;
2. restored the exact three modified paths from parent-commit projection bytes;
3. applied the parent Git modes;
4. pruned only empty directories created by removed P12.6 additions;
5. recomputed every blob and the complete Git tree hash.

```yaml
HermesIsolatedRollbackResult:
  rollback_paths_expected: 15
  rollback_paths_applied: 15
  actual_files: 6120
  unexplained_paths: 0
  path_set_differences: 0
  directory_set_differences: 0
  hash_mismatches: 0
  mode_mismatches: 0
  reparse_points: 0
  nested_git: false
  computed_tree: 07bc27d2cc3b015b3865d62d7fdbc7dfe0ab6fb7
  pre_P12_6_tree_reached: true
```

## Isolated Reapplication Drill

Starting only from the verified rolled-back projection, the forward operation
created/replaced all 15 P12.6 paths from committed P12.6 bytes and modes.

```yaml
HermesIsolatedReapplicationResult:
  reapplication_paths_expected: 15
  reapplication_paths_applied: 15
  actual_files: 6132
  unexplained_paths: 0
  path_set_differences: 0
  directory_set_differences: 0
  hash_mismatches: 0
  mode_mismatches: 0
  reparse_points: 0
  nested_git: false
  computed_tree: 274527e686fa50a320a92a5738e8c8c083669b24
  post_P12_6_tree_reached: true
```

No semantic patching or merge decision occurred.

## Helper Boundary and Integrity

All transformation helpers were Python 3.12 standard-library scripts supplied
inline with `C:/Users/pablo/anaconda3/python.exe -c <inline-script>`. No helper
file was created in or outside the repository, so removal was immediate by
construction. Helpers had no network code, no product working-tree mutation and
no Git write operation.

| Helper | SHA-256 | Scope |
| --- | --- | --- |
| Initial generated-state deletion | `f92cec008c50e6c62bed725d08b3e84527038ea310ae52efbf55b658ec92ff07` | Exact nine-root deletion; stopped on loaded DLL |
| Deletion retry | `d1c014d5d4318d85167ca3593013ad90db8e8e0b9fe5a48718c2e5d207951634` | Complete remaining exact roots after human lock release |
| Projection cleanup after long-path failure | `29b030a70a22610cbcb401315c4488b9dea9195ff0732e200192ecfba5f30c04` | Remove two exact incomplete projection roots |
| Extended-path Git object materializer | `01b9e800ecfc359159b62ca47dc09ab32cca4483a2b089d19aa8d6b87f3959e2` | Materialize and recompute pre/post trees |
| Rollback/reapplication helper | `beb29060c44d32983f941094d92729d31c55ce0329106635831b2180ed0f990d` | Exact inverse, forward apply and tree verification |
| Provider-null runtime controller | `291295de9f8f5907abb9555a3100a23a599061a1bffefee994a417d5928dfed3` | Launch, probe and graceful shutdown |
| Projection/runtime/bootstrap cleanup | `ed82fb9b50522a88e954260e5fb65563afcf000fd3a6b1392e25dc8abc86f2d4` | Exact transient-root cleanup |
| Final generated-state inventory | `3107fcbc2f447c8c77fdf960c064055f4460057596b57801293a7bf24b0d0546` | Reparse-safe final generated inventory |

The failed legacy-path materializer had SHA-256
`400045b9b5f5ed7f7af22fb0515e481680f61f5dae4c115dee5aef7d9c7f251f`;
it did not complete or provide accepted projection evidence.

## Actual Product No-Touch Validation

```yaml
HermesActualProductNoTouch:
  tracked_files_before: 6132
  tracked_files_after: 6132
  status_paths_before: 0
  status_paths_after: 0
  staged_paths_before: 0
  staged_paths_after: 0
  product_tree_before: 274527e686fa50a320a92a5738e8c8c083669b24
  product_tree_after: 274527e686fa50a320a92a5738e8c8c083669b24
  initial_sha_inventory: ad0ee1c37bf2e161debf76f8c48785adfa9a5b9f17cc20fe8aa2efad34d470af
  final_sha_inventory: ad0ee1c37bf2e161debf76f8c48785adfa9a5b9f17cc20fe8aa2efad34d470af
  complete_inventory_equal: true
  lockfiles_unchanged: true
  P12_2_controls_unchanged: true
  P12_6_register_unchanged: true
```

Protected final hashes:

| Path | SHA-256 |
| --- | --- |
| `pyproject.toml` | `7f0180b23c28ea3f7a32e037bcfb1d986fa1925d0a9331112bdce82ef1bfbf45` |
| `uv.lock` | `92d8153c76379a4d427eaf37cd77cedef9dc093c6c44c1386abd4546578f709a` |
| `package.json` | `07b1b0c8d196c93cc4876092907e7350cfc8b04db18ce34debb522aead4ad1c0` |
| `package-lock.json` | `bc11d099f043e142764e66f60f2b558add882948649101645d56319d188861df` |
| `UPSTREAM_PROVENANCE.md` | `78db7acccd38cacc1771792ca9c99cf3a063f60ac2e04d966e05cae22c335b43` |
| `SOURCE_IMPORT_MANIFEST.tsv` | `58a3392c7515ec2a8aaaf8e43530ae6299b2696957d095be461df51e8a080d5c` |
| `SOURCE_EXCLUSIONS.tsv` | `7a413310330e4625146bcad9c73e62af2634f5f3130530111a9b766daf25d64e` |
| `NOTICE` | `4ac2353fc0b52c937b43ba6ae54d9d28ce3c4d400b87b7dd4894c2cc2026c145` |
| `THIRD_PARTY_NOTICES.md` | `c3c564d96a3ef0e9ee9afccd44ae43785c311ef1a5262e5043c786da8df0e5aa` |
| `.gitignore` | `cc50d6a4e5789a08f19a4f17d306ce14cfda4032b5ec248e2c1383106959cc30` |

## Artifact Cleanup

Removed after verification:

```text
9_artifacts/hermes/p12.7/rollback/base-pre-P12.6
9_artifacts/hermes/p12.7/rollback/current-post-P12.6
9_artifacts/hermes/p12.7/rollback/rollback-working
9_artifacts/hermes/p12.7/rollback/reapplied-working
9_artifacts/hermes/p12.7/runtime
C:/Users/pablo/AppData/Local/Temp/opencode/p12_7_uv_bootstrap
```

Retained under ignored `9_artifacts/hermes/p12.7`:

```yaml
P12_7_RetainedEvidence:
  inventory_files: 15
  package_log_files: 12
  total_files: 27
  total_bytes: 8496288
  aggregate_manifest_sha256: 77221fe306ef39d42ee1202d5d6d7d6f5cabb73200a9fc4fde761f03fb8e55fb
  rollback_directory_entries: 0
  tracked_files: 0
  staged_files: 0
  ignored: true
```

Retained product-local generated state for P12.R/P13:

```text
.venv
node_modules
hermes_agent.egg-info
.pytest_cache
hermes_cli/web_dist
ui-tui/packages/hermes-ink/dist
ui-tui/dist
apps/desktop/build
apps/desktop/dist
.ruff_cache
```

The final generated-state inventory reports ten existing roots, six internal
workspace junctions and zero external reparse targets.

## Failure Inventory

Every non-zero or aborted command received a primary classification. All were
resolved without tracked source modification.

| Phase | Classification | Blocking for P12.R | Evidence and disposition |
| --- | --- | --- | --- |
| Generated-state inventory | `unknown` | No | Initial summary print had a quoting-related `NameError` after the JSON evidence was fully written; evidence was read and validated directly. |
| Generated-state removal | `windows_platform_limitation` | No | VS Code PID 6276 held one Tailwind native module; no unrelated process was killed. Human restart released it and exact retry passed. |
| Generated-state removal | `unknown` | No | Retry summary print had a quoting-related `NameError` after all roots and evidence completed; independent absence and source-hash checks passed. |
| Frozen verification | `environment_rebuild_failure` | No | Direct `python -m pip check` is unavailable in a uv-created environment without pip executable metadata; authoritative `uv pip check` passed all 107 packages. |
| Build inventory | `unknown` | No | First inline inventory expression had a quoting syntax error and made no change; corrected read-only inventory passed. |
| Post-P12.6 reconstruction | `windows_platform_limitation` | No | Legacy path API rejected one deep documentation path; exact projection cleanup and extended-length retry produced the expected tree. |

No accepted validation lane failed. Failure count blocking P12.R is zero.

## Operational Rollback Procedure

Future pre-merge rollback of P12.6 must use this exact object-driven procedure:

1. Require clean `main`, empty index, valid 14-row register and exact P12.6
   commit/parent identities.
2. Inventory the actual product and stop on any path outside the 15-path P12.6
   commit diff.
3. In a separate ignored non-Git projection, materialize the committed current
   product from Git objects.
4. Remove exactly the 12 P12.6 additions derived from the commit diff.
5. Restore exactly the three modified paths from parent commit blob objects and
   modes recorded by the register.
6. Require path, directory, byte, mode and computed tree equality with
   `07bc27d2cc3b015b3865d62d7fdbc7dfe0ab6fb7`.
7. Reapply all 15 P12.6 paths from commit objects and require tree
   `274527e686fa50a320a92a5738e8c8c083669b24` before authorizing any real change.
8. For an uncommitted real rollback, use exact-path preimages under human
   control only after projection proof and approval.
9. After a committed P12.6 history point, use an explicit human-created revert
   commit; do not reset or rewrite history.

Never use Git clean, hard reset, broad restore, wildcard deletion, worktrees,
nested Git, semantic patching or inferred rename logic for this rollback.

## P12.R Handoff

P12.R may proceed after human acceptance and commit of this one governance
record, with clean main, the recreated environments retained, the P12.6
register valid and no unresolved P12 security alert.

P12.R receives proof of:

- controlled and byte-stable editable product source;
- unchanged legal/provenance and dependency authority;
- clean Python/Node environment reconstruction;
- reproducible selected build/test/runtime anchors;
- exact P12.6 register reconciliation;
- exact pre/post Git-object reconstruction;
- exact isolated rollback and forward reapplication;
- complete actual-product no-touch behavior.

Marker: `hermes_P12_R_ready`.

P13 remains blocked until P12.R accepts the full P12 foundation.

## Created / Modified / Generated / Removed / Not Created Register

Durable created:

```text
0_architecture/governance/agent_platform_hermes_clean_rebuild_rollback_drill.md
```

Tracked modified: none.

Ignored removed and recreated:

```text
2_products/hermes-agent/.venv/**
2_products/hermes-agent/node_modules/**
2_products/hermes-agent/hermes_agent.egg-info/**
2_products/hermes-agent/.pytest_cache/**
2_products/hermes-agent/hermes_cli/web_dist/**
2_products/hermes-agent/ui-tui/dist/**
2_products/hermes-agent/ui-tui/packages/hermes-ink/dist/**
2_products/hermes-agent/apps/desktop/dist/**
2_products/hermes-agent/apps/desktop/build/**
```

Ignored generated/retained: compact P12.7 inventories/logs and rebuilt outputs.

Transient and removed: uv bootstrap, isolated runtime/controller state, four
full product projections and all inline helper source text.

Not created:

```text
additional governance Markdown
Git worktree
nested .git
branch
submodule
candidate checkout
synchronization workspace
real .env
browser profile
provider, OAuth, MCP, gateway, worker or agent state
```

Not modified:

```text
2_products/hermes-agent tracked source and tests
AGENT_PLATFORM_MODIFICATIONS.tsv
P12.2 legal/provenance records
SOURCE_IMPORT_MANIFEST.tsv
SOURCE_EXCLUSIONS.tsv
pyproject.toml
uv.lock
package.json
package-lock.json
root and product .gitignore
locked upstream
sibling products
P12.3/P12.4/P12.5/P12.6 governance records
.opencode/**
AGENTS.md
graphify-out/**
```

## Limitations

- The clean Python environment is uv-managed and intentionally omits a
  standalone pip command; compatibility was checked with `uv pip check`.
- npm does not report per-package cache-versus-network resolution in normal
  `npm ci` output, so only its exclusive public-registry configuration and
  successful locked installation are recorded.
- Windows loaded-module semantics required a human editor restart before exact
  node_modules deletion could finish.
- Windows legacy path APIs required extended-length prefixes for one deep
  projection path.
- Known upstream npm deprecation and frontend bundle-size warnings remain.
- Known P12.4 non-green lanes remain baseline debt and were not reclassified.
- Secret-scanning dispositions are human-confirmed because querying GitHub
  alert metadata would require a credential prohibited by this ticket.

## Result Markers

```text
hermes_clean_rebuild_rollback_drill_passed
hermes_generated_state_inventory_verified
hermes_python_environment_recreated
hermes_node_environment_recreated
hermes_frozen_lock_rebuild_verified
hermes_product_configuration_reproduced
hermes_targeted_validation_reproduced
hermes_provider_null_startup_reproduced
hermes_modification_register_reconciled
hermes_pre_P12_6_tree_reconstructed
hermes_P12_6_divergence_rolled_back_in_isolation
hermes_P12_6_divergence_reapplied_in_isolation
hermes_post_P12_6_tree_reconstructed
hermes_actual_product_source_unchanged
hermes_exact_rollback_proven
hermes_P12_R_ready
no_provider_activation
no_credentials_used
no_upstream_sync
no_git_index_or_history_mutation
```

## Final Verdict

```yaml
P12_7_CleanRebuildRollbackDrillVerdict:
  p12_6_committed: true
  initial_repository_clean: true
  secret_scanning_gate_passed: true
  generated_state_inventory_complete: true
  generated_state_removed_safely: true
  python_environment_recreated: true
  node_environment_recreated: true
  frozen_lock_rebuild_verified: true
  lockfiles_unchanged: true
  product_build_outputs_recreated: true
  targeted_P12_6_validation_passed: true
  P12_4_green_anchors_preserved: true
  provider_null_startup_reproduced: true
  product_configuration_reproduced: true
  controlled_shutdown_completed: true
  modification_register_reconciled: true
  pre_P12_6_tree_reconstructed: true
  isolated_P12_6_rollback_passed: true
  isolated_P12_6_reapplication_passed: true
  post_P12_6_tree_reconstructed: true
  actual_product_source_unchanged: true
  credentials_used: false
  provider_activation_performed: false
  upstream_sync_performed: false
  git_mutated_by_agent: false
  P12_R_may_proceed: true
  final_verdict: clean_rebuild_and_rollback_drill_passed
```

## Human Commit Boundary

The human commit contains only:

```text
0_architecture/governance/agent_platform_hermes_clean_rebuild_rollback_drill.md
```

```powershell
$ErrorActionPreference = "Stop"

$Record = "0_architecture/governance/agent_platform_hermes_clean_rebuild_rollback_drill.md"
$ProductRoot = "2_products/hermes-agent"

if (-not (Test-Path -LiteralPath $Record -PathType Leaf)) {
    throw "Missing P12.7 record: $Record"
}
if ((git branch --show-current) -ne "main") {
    throw "P12.7 must be committed from main"
}
if ((git rev-parse HEAD) -ne (git rev-parse origin/main)) {
    throw "main does not match origin/main"
}
if (@(git diff --cached --name-only).Count -ne 0) {
    throw "Git index is not empty"
}
if (@(git status --short -- $ProductRoot).Count -ne 0) {
    throw "Hermes product drift detected"
}
if (@(git ls-files -- "$ProductRoot/**").Count -ne 6132) {
    throw "Unexpected Hermes tracked-file count"
}
if (Test-Path -LiteralPath (Join-Path $ProductRoot ".git")) {
    throw "Nested product Git metadata detected"
}

$Rows = @(Import-Csv -LiteralPath "$ProductRoot/AGENT_PLATFORM_MODIFICATIONS.tsv" -Delimiter "`t")
if ($Rows.Count -ne 14) {
    throw "Unexpected modification-register row count"
}
foreach ($Row in $Rows) {
    $Path = Join-Path $ProductRoot $Row.path
    $Hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
    if ($Hash -ne $Row.current_product_sha256_or_none) {
        throw "Modification-register hash mismatch: $Path"
    }
}

git status --short
git add -- $Record

$Staged = @(
    git diff --cached --name-only |
        ForEach-Object { $_.Replace("\", "/") } |
        Sort-Object -Unique
)
if ($Staged.Count -ne 1 -or $Staged[0] -ne $Record) {
    throw "Unexpected staged paths: $($Staged -join ', ')"
}

git diff --cached --check
if ($LASTEXITCODE -ne 0) {
    throw "git diff --cached --check failed"
}

git diff --cached --stat
git commit -m "P12.7 - Validate Hermes clean rebuild and rollback"
git push origin main
git status --short
```

The executing agent did not stage, commit or push.
