# P12.4 - Hermes Baseline Build, Test and UI Snapshot

## Document Header

| Field | Value |
| --- | --- |
| Project | P12 - Hermes Productization Foundation |
| Ticket | P12.4 - Baseline Build, Test and UI Snapshot |
| Type | Validation / build / test / controlled runtime evidence |
| Date | 2026-07-13 |
| Status | `baseline_usable_with_known_failures` |
| Canonical output | `0_architecture/governance/agent_platform_hermes_baseline_build_test_ui_snapshot.md` |
| Durable governance document count | Exactly one |
| Product root | `2_products/hermes-agent` |
| Source baseline | Upstream `0.18.2`, tag `v2026.7.7.2`, commit `9de9c25f620ff7f1ce0fd5457d596052d5159596` |
| Environment authority | Committed P12.3 record at main-repository commit `0b5ea15bc2ce8d36b0218eb3d03639944637ffb7` |
| Runtime boundary | Provider-null, credential-free, localhost-only Hermes dashboard |
| Git staging / commit / push | Not performed |

## Purpose

Characterize the imported Hermes product before AGENT PLATFORM source modifications begin. This record captures authoritative command resolution, frozen-environment validation, Python and Node checks, selected frontend builds, provider-null dashboard lifecycle evidence, human-captured UI evidence, generated-state containment, failure ownership, and final source-drift checks.

This is a baseline characterization, not a source-fix ticket. Non-green upstream lanes were retained and classified. No source, test, manifest, dependency, lockfile, tracked ignore rule, provider configuration, credential, upstream reference, release artifact, or deployment target was changed.

## P12.3 Prerequisite Status

```yaml
P12_3_PrerequisiteStatus:
  canonical_record: 0_architecture/governance/agent_platform_hermes_reproducible_development_environment.md
  record_status: reproducible_development_environment_ready
  record_commit: 0b5ea15bc2ce8d36b0218eb3d03639944637ffb7
  record_committed: true
  main_branch: main
  main_head_before_validation: 0b5ea15bc2ce8d36b0218eb3d03639944637ffb7
  product_tracked_files: 6120
  product_status_paths_before_validation: 0
  product_staged_paths_before_validation: 0
  total_staged_paths_before_validation: 0
  nested_product_git: false
  python_environment_exists: true
  node_environment_exists: true
  editable_metadata_exists: true
  generated_roots_ignored: true
  prerequisite_result: pass
```

Environment verification observed:

| Surface | Result |
| --- | --- |
| `.venv` | Normal directory, Python `3.12.3`, Hermes `0.18.2` |
| Python tools | pytest `9.0.2`, ruff `0.15.10`, ty `0.0.21` |
| `node_modules` | Normal directory, Node `24.12.0`, npm `11.6.2` |
| `hermes_agent.egg-info` | Present, ignored, untracked and unstaged |
| `uv lock --check` | Exit `0`; resolved 233 packages |
| Frozen environment check | Exit `0`; checked 107 packages; would make no changes |

The P12.3-selected hashes matched before execution. P12.2 legal/provenance hashes also matched their committed baseline.

## Baseline Profile

```yaml
HermesP12_4BaselineProfile:
  python_core:
    enabled: true
  root_node_workspace:
    enabled: true
  dashboard_frontend:
    enabled: true
  tui:
    enabled: true
  desktop_frontend:
    enabled: true
  bootstrap_installer_frontend:
    enabled_for_typecheck_only: true
  docs_website:
    enabled: false
  whatsapp_bridge:
    enabled: false
  photon_sidecar:
    enabled: false
  rust_tauri_packaging:
    enabled: false
  nix:
    enabled: false
  containers:
    enabled: false
  provider_or_model_execution:
    enabled: false
```

The selected representative profile covers frozen Python integrity, blocking Python lint, advisory Python type analysis, provider-independent representative Python tests, root npm integrity, all five CI TypeScript packages, declared lint and unit-test lanes for dashboard/TUI/desktop, production dashboard/TUI/desktop frontend builds, and one controlled local dashboard lifecycle.

## Validation-Lane Inventory

| ID | Ecosystem | Command authority | Purpose | Required | Provider independent | Credentials | Generated paths | Decision and rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `python_lock` | Python | `.github/workflows/uv-lockfile-check.yml` | Lock consistency | Yes | Yes | No | uv cache only | Run; blocking CI authority |
| `python_frozen_environment` | Python | P12.3 recipe and `uv.lock` | Existing environment consistency | Yes | Yes | No | None expected | Run with `--frozen --check` |
| `python_ruff` | Python | `.github/workflows/lint.yml` | Blocking lint | Yes | Yes | No | redirected Ruff cache | Run |
| `python_format` | Python | No declared command | Formatting baseline | Yes | Yes | No | N/A | Defer; no authoritative `ruff format --check`, Black or isort lane exists |
| `python_windows_footguns` | Python | `.github/workflows/lint.yml` | Windows path/encoding regression scan | Yes | Yes | No | None | Run |
| `python_ty` | Python | `.github/workflows/lint.yml` | Advisory whole-tree type diagnostics | Yes | Yes | No | artifact log | Run with upstream `--exit-zero` posture |
| `python_unit_representative` | Python | `pyproject.toml`, `scripts/run_tests.sh`, CI | Core agent/dashboard/TUI gateway/metadata behavior | Yes | Yes under sanitized environment | No | `.pytest_cache`, isolated temp | Run representative selection |
| `python_full_ci_wrapper` | Python | `scripts/run_tests.sh` | Full per-file isolated suite | No for this host | Intended yes | No | test durations/cache | Defer; wrapper expects POSIX venv paths and shell semantics unavailable to the native Windows P12.3 environment |
| `python_integration_provider` | Python | pytest `integration` marker | Real provider/network integration | No | No | Yes or provider state | Various | Prohibit |
| `python_e2e_gateway` | Python | `.github/workflows/tests.yml` | Dedicated local gateway E2E | No | Yes | No | pytest cache | Defer; representative baseline already selected |
| `python_docker` | Python/container | `.github/workflows/docker.yml` | Container behavior | No | Yes | No | Docker images/containers | Defer outside selected profile |
| `node_dependency` | Node | P12.3 and root lock | Installed workspace integrity | Yes | Yes | No | None | Run `npm ls --all --depth=0` |
| `node_typecheck_matrix` | Node | `.github/workflows/typecheck.yml` | TypeScript validity for five packages | Yes | Yes | No | possible ignored TypeScript cache | Run all five package scripts |
| `dashboard_lint` | Frontend | `web/package.json` | Dashboard ESLint baseline | Yes | Yes | No | None | Run |
| `tui_lint` | TUI | `ui-tui/package.json` | TUI ESLint baseline | Yes | Yes | No | None | Run |
| `desktop_lint` | Desktop | `apps/desktop/package.json` | Desktop ESLint baseline | Yes | Yes | No | None | Run |
| `dashboard_test` | Frontend | `web/package.json` | Dashboard Vitest baseline | Yes | Yes | No | Vitest transient state | Run |
| `tui_test` | TUI | `ui-tui/package.json` | TUI/Ink Vitest baseline | Yes | Yes | No | Vitest transient state | Run before builds to characterize declared script from clean generated state |
| `desktop_ui_test` | Desktop | `apps/desktop/package.json` | Desktop renderer Vitest baseline | Yes | Yes | No | jsdom/Vitest transient state | Run |
| `desktop_platform_test` | Desktop | `apps/desktop/package.json` | Desktop Node platform baseline | Yes | Intended yes | No | temporary Git fixtures | Run once; unsafe parent-repository discovery found and contained |
| `dashboard_build` | Frontend | `web/package.json`, release workflow | Browser dashboard production build | Yes | Yes | No | `hermes_cli/web_dist` | Run |
| `tui_ink_build` | TUI | `ui-tui/packages/hermes-ink/package.json` | Build local Ink dependency | Yes | Yes | No | `ui-tui/packages/hermes-ink/dist` | Run |
| `tui_build` | TUI | `ui-tui/package.json`, release workflow | TUI production bundle | Yes | Yes | No | `ui-tui/dist` | Run |
| `desktop_build` | Desktop | `.github/workflows/typecheck.yml`, package script | Electron renderer production build | Yes | Yes | No | `apps/desktop/build`, `apps/desktop/dist` | Run; native packaging remains deferred |
| `bootstrap_native_tauri` | Desktop/native | package scripts only | Rust/Tauri package | No | Yes at compile time | No | Cargo target/bundles | Defer; no tracked Cargo lock or CI authority |
| `website_build` | Frontend/docs | docs CI | Docusaurus build | No | Not strictly; prebuild can fetch | No | tracked/generated docs plus build | Defer outside selected profile |
| `whatsapp_runtime` | Other | bridge package | Messaging bridge | No | No | Pairing state | session/log state | Prohibit |
| `photon_runtime` | Other | sidecar package | Photon bridge | No | No | Project/device credentials | sidecar state | Prohibit |
| `dashboard_launch` | Runtime | dashboard parser and `hermes_cli.main` | Local UI readiness/lifecycle | Yes | Yes with empty isolated home | No | isolated runtime state/logs | Run with prebuilt assets and localhost only |
| `interactive_cli_or_tui` | Runtime/TUI | CLI entrypoints | Agent conversation | No | No | Provider normally required | sessions/logs | Prohibit |

## Command Authority

Authority order was CI, package scripts, project tool configuration, then upstream development documentation. No dependency-update, autofix, format-write, snapshot-update, coverage-upload, provider integration, release, deployment, or publication command ran.

All selected commands ran from `2_products/hermes-agent` unless shown otherwise. Foreground commands used a cleared environment with only OS/runtime essentials and exact P12.4 state roots. Provider keys, tokens, proxy credentials, real Hermes config, real `.env`, OAuth state, MCP config and personal Hermes state were not inherited.

Executed command set, shown in canonical form:

```powershell
# Exact P12.3 uv bootstrap was temporary and later removed.
& "C:\Users\pablo\anaconda3\python.exe" -m venv `
  "9_artifacts\hermes\p12.4\bootstrap\uv-env"
& "9_artifacts\hermes\p12.4\bootstrap\uv-env\Scripts\python.exe" `
  -m pip install --disable-pip-version-check --no-input uv==0.11.6

& "9_artifacts\hermes\p12.4\bootstrap\uv-env\Scripts\uv.exe" lock --check
& "9_artifacts\hermes\p12.4\bootstrap\uv-env\Scripts\uv.exe" sync `
  --frozen --check --python ".venv\Scripts\python.exe" --extra all --extra dev

& ".venv\Scripts\ruff.exe" check .
& ".venv\Scripts\python.exe" scripts\check-windows-footguns.py --all
& ".venv\Scripts\ty.exe" check --output-format gitlab --exit-zero

& ".venv\Scripts\python.exe" -m pytest --collect-only -q `
  tests\agent tests\dashboard tests\tui_gateway `
  tests\test_lint_config.py tests\test_project_metadata.py `
  tests\test_packaging_metadata.py tests\ci\test_classify_changes.py
& ".venv\Scripts\python.exe" -m pytest -q `
  tests\agent tests\dashboard tests\tui_gateway `
  tests\test_lint_config.py tests\test_project_metadata.py `
  tests\test_packaging_metadata.py tests\ci\test_classify_changes.py

npm ls --all --depth=0
npm run --prefix ui-tui typecheck
npm run --prefix web typecheck
npm run --prefix apps/bootstrap-installer typecheck
npm run --prefix apps/desktop typecheck
npm run --prefix apps/shared typecheck
npm run --prefix web lint
npm run --prefix ui-tui lint
npm run --prefix apps/desktop lint
npm run --prefix web test
npm run --prefix ui-tui test
npm run --prefix apps/desktop test:ui
npm run --prefix apps/desktop test:desktop:platforms
npm run --prefix web build
npm run --prefix ui-tui/packages/hermes-ink build
npm run --prefix ui-tui build
npm run --prefix apps/desktop build

& ".venv\Scripts\python.exe" -m hermes_cli.main dashboard `
  --host 127.0.0.1 --port 0 --no-open --skip-build
```

On Windows, npm was implemented as the installed `node.exe` plus npm's `npm-cli.js` entrypoint so the sanitized process launcher could execute it directly. The npm subcommands and package scripts were unchanged.

Timeouts were 120 seconds for lock/lint/tool checks, 600 seconds for collection and Node build/test commands, 1,800 seconds for the selected Python tests, 20 seconds per localhost HTTP probe, and 20 seconds for graceful dashboard shutdown before exact-tree fallback.

## Python Lint and Format Baseline

| Lane | Result | Evidence |
| --- | --- | --- |
| Ruff | Pass, exit `0` | `All checks passed!`; one warning for an invalid `# noqa` directive at `run_agent.py:107` |
| Windows-footgun scanner | Pass, exit `0` | 752 Python files scanned; no Windows footguns found |
| Formatting | Validly deferred | No authoritative Python format-check command or tool configuration exists |

No autofix, format-write or source rewrite command ran.

## Python Type Baseline

The upstream advisory command completed with exit `0` because CI explicitly uses `--exit-zero`.

```yaml
HermesPythonTypeBaseline:
  tool: ty 0.0.21
  command: ty check --output-format gitlab --exit-zero
  exit_code: 0
  diagnostics_recorded: 10889
  fatal_analysis_warning_count: 1
  complete_project_analysis: false
  blocking_ci_gate: false
  classification: known_upstream_advisory_limitation
```

Diagnostics include unresolved optional imports and many invalid type/attribute/assignment findings. Ty also reported that a fatal error prevented analysis of some files. The raw output is retained only under ignored P12.4 logs. This is recorded as non-green advisory type evidence, not represented as a clean type baseline.

## Python Test Baseline

The native Windows P12.3 environment cannot execute the authoritative POSIX wrapper as written because `scripts/run_tests.sh` resolves `.venv/bin/python`, uses POSIX shell activation and relies on per-file subprocess behavior. A sanitized direct pytest selection was therefore used to characterize core agent, dashboard backend, TUI gateway, metadata, packaging and CI classification behavior without provider or credential state.

```yaml
HermesPythonTestBaseline:
  selection:
    - tests/agent
    - tests/dashboard
    - tests/tui_gateway
    - tests/test_lint_config.py
    - tests/test_project_metadata.py
    - tests/test_packaging_metadata.py
    - tests/ci/test_classify_changes.py
  collected: 5774
  executed: 5774
  passed: 5535
  failed: 198
  skipped: 41
  deselected: 0
  errors: 0
  timeout: false
  duration_seconds: 787.57
  exit_code: 1
```

The failure set is not an import/exclusion regression. Dominant evidence includes Windows path separator and shell assumptions, provider/config mocks affected by direct single-process module state, and behavior that the authoritative wrapper isolates by running each test file in a fresh process. No real provider request was allowed; failures that report `No LLM provider configured` demonstrate that the provider-null boundary remained active.

Integration-provider, integration-network, Docker, browser-supervisor, stress, manual and real external-service suites were not selected. They are outside the bounded profile and are neither passed nor accepted by this record.

## Node Dependency Baseline

```yaml
HermesNodeDependencyBaseline:
  node_version: 24.12.0
  npm_version: 11.6.2
  command: npm ls --all --depth=0
  exit_code: 0
  root_workspace_links_present: 6
  extraneous_optional_platform_packages: 5
  lockfile_modified: false
```

The five existing optional/platform-support packages labeled extraneous are `@emnapi/core`, `@emnapi/runtime`, `@emnapi/wasi-threads`, `@napi-rs/wasm-runtime` and `@tybys/wasm-util`. This matches the P12.3 limitation and did not invalidate the workspace.

## Node Lint and Type Baseline

All five CI TypeScript checks passed:

| Package | Command | Exit |
| --- | --- | --- |
| `ui-tui` | `npm run --prefix ui-tui typecheck` | `0` |
| `web` | `npm run --prefix web typecheck` | `0` |
| `apps/bootstrap-installer` | `npm run --prefix apps/bootstrap-installer typecheck` | `0` |
| `apps/desktop` | `npm run --prefix apps/desktop typecheck` | `0` |
| `apps/shared` | `npm run --prefix apps/shared typecheck` | `0` |

Declared lint scripts produced:

| Package | Result | Baseline |
| --- | --- | --- |
| `web` | Exit `1` | 28 errors and 3 warnings, primarily React hooks/compiler and fast-refresh rules |
| `ui-tui` | Exit `1` | 1 error and 14 warnings; the blocking error is a `curly` rule finding in `bundleNoAsyncEsmDeadlock.test.ts` |
| `apps/desktop` | Exit `0` | No errors; one `react-hooks/exhaustive-deps` warning |

Frontend lint does not run in current upstream CI. These declared-script failures are preserved as upstream baseline debt.

## Node Test Baseline

| Surface | Files | Tests | Result |
| --- | --- | --- | --- |
| Dashboard `web` | 6 passed | 33 passed | Exit `0` |
| TUI | 72 passed, 34 failed, 1 skipped | 756 passed, 3 failed, 5 skipped | Exit `1` |
| Desktop renderer `test:ui` | 133 passed, 49 failed | 1,148 passed, 27 failed | Exit `1` |
| Desktop Node platform suite | Node runner aggregate | 300 passed, 9 failed, 0 skipped | Exit `1` |

The TUI test script does not prebuild its local `@hermes/ink` package. Thirty-two suites could not import `packages/hermes-ink/dist/entry-exports.js` from a clean generated state. Three executed tests also failed on Windows path/terminal assumptions. The later authoritative Ink and TUI build commands succeeded; tests were not rerun to erase the clean-state characterization.

The desktop `test:ui` script includes CommonJS Node test files in Vitest, producing 36 `No test suite found` failures, plus 27 renderer failures involving stale mocks/assertions, jsdom behavior and timeouts. The separate explicit Node platform script passed 300 tests and failed 9, mainly on Windows path length, Bash path translation and temporary Git-repository isolation.

## Frontend Build Baseline

Primary browser dashboard:

```yaml
HermesDashboardBuild:
  package_root: 2_products/hermes-agent/web
  build_tool: TypeScript project build plus Vite 8.1.0
  html_entry: web/index.html
  source_entry: web/src/main.tsx
  command: npm run --prefix web build
  exit_code: 0
  output: 2_products/hermes-agent/hermes_cli/web_dist
  output_index_bytes: 510
  output_index_sha256: F742FE2D710524436469F0B2462867C0675F09F5AF5E7F3B8591180E594E1F01
  provider_required: false
  credentials_required: false
  ignored: true
  tracked_or_staged: false
```

The build transformed 482 modules and produced the SPA index, local fonts, CSS and a JavaScript bundle. Vite reported a non-blocking chunk-size warning. No secret or provider value was embedded by P12.4.

## TUI Baseline

```yaml
HermesTUIBaseline:
  package_root: 2_products/hermes-agent/ui-tui
  local_ink_package: 2_products/hermes-agent/ui-tui/packages/hermes-ink
  typecheck: pass
  lint: fail_with_1_error_and_14_warnings
  tests: fail_with_756_passed_3_failed_5_skipped_and_32_import_failed_suites
  ink_build: pass
  tui_bundle_build: pass
  ink_output_sha256: 278BA0A06FA7CE66673B7591DC07DD73D45CC60A2C7847E93A68771FCDABE6C1
  tui_output_bytes: 3470591
  tui_output_sha256: 7CF175DF253AE9FEE9257CE23F62989CDD1C7B00F59B6D22E542B558FD3C5CEE
  interactive_agent_session_started: false
```

The TUI production bundle is build-ready. An interactive TUI was prohibited because that surface can create agent/provider sessions. Native Windows dashboard embedded chat remains limited because the stock PTY bridge is POSIX/WSL-oriented.

## Desktop Baseline

```yaml
HermesDesktopBaseline:
  package_root: 2_products/hermes-agent/apps/desktop
  surface: Electron renderer frontend
  typecheck: pass
  lint: pass_with_1_warning
  renderer_tests: fail_with_1148_passed_and_27_failed
  platform_tests: fail_with_300_passed_and_9_failed
  production_build: pass
  output: 2_products/hermes-agent/apps/desktop/dist
  output_index_bytes: 1779
  output_index_sha256: BB7F87C9DDE00ACCDCD42E83CB5B89795EE587755F56F3CA8369925DB58875A6
  build_stamp_sha256: 955FA18573C92D7FDFF993837DC1E6E5F879E3F7312CC0F80D5BF51D1C932239
  electron_application_launched: false
  native_packaging_executed: false
```

The desktop build wrote the ignored install stamp for main-repository commit `0b5ea15`, staged the declared native dependency closure into ignored build output, compiled TypeScript, built the Vite renderer and passed `assert-dist-built`. It emitted non-blocking CSS and large-bundle warnings.

The platform test exposed an upstream fixture-isolation defect. Because its temporary root was under ignored `9_artifacts` inside the AGENT PLATFORM worktree, Git discovered the parent repository. The test transiently created branches `feature`, `rawr`, `wt`, and `cool/feature`, switched the checkout to `rawr`, registered `.worktrees/cool-feature`, and created an untracked literal `%SystemDrive%` tree. Every created ref pointed to unchanged commit `0b5ea15`. P12.4 removed only those demonstrated test-owned refs/worktree/trees and restored `main`; no source, index, commit or remote changed. Future execution of this suite must use an OS temporary root outside any parent Git worktree.

## Deferred Surface Register

| Surface | Status | Reason |
| --- | --- | --- |
| Website/docs | Not exercised, not failed, not accepted | Separate dependency root; prebuild can fetch and rewrite tracked generated docs |
| WhatsApp bridge | Not exercised, not failed, not accepted | Requires separate dependencies and pairing/session state |
| Photon sidecar | Not exercised, not failed, not accepted | Requires separate dependencies and real Photon credentials |
| Rust/Tauri packaging | Not exercised, not failed, not accepted | No tracked Cargo lock and no authoritative native CI lane |
| Nix | Not exercised, not failed, not accepted | Unavailable on native Windows and outside baseline |
| Containers | Not exercised, not failed, not accepted | Docker build/test is outside selected baseline |
| Optional skill environments | Not exercised, not failed, not accepted | Not needed for selected core/UI profile |
| Provider integration tests | Prohibited | Real provider/network/credential dependency |
| OAuth/MCP/workers | Prohibited | Outside provider-null lifecycle boundary |
| Electron app launch/package | Not exercised, not failed, not accepted | Browser dashboard is the selected UI baseline; native packaging remains deferred |

## Runtime Isolation

```yaml
HermesRuntimeIsolation:
  artifact_root: 9_artifacts/hermes/p12.4
  hermes_home: 9_artifacts/hermes/p12.4/runtime/dashboard-home
  shared_auth: 9_artifacts/hermes/p12.4/runtime/dashboard-shared-auth
  home: 9_artifacts/hermes/p12.4/runtime/dashboard-home-dir
  appdata: 9_artifacts/hermes/p12.4/runtime/dashboard-appdata
  localappdata: 9_artifacts/hermes/p12.4/runtime/dashboard-localappdata
  temp: 9_artifacts/hermes/p12.4/runtime/dashboard-temp
  logs: 9_artifacts/hermes/p12.4/logs
  web_dist: 2_products/hermes-agent/hermes_cli/web_dist
  tui_dir: 2_products/hermes-agent/ui-tui
  project_plugins_enabled: false
  inherited_user_config: false
  inherited_real_env: false
  personal_browser_automation_profile_created: false
```

The process environment was cleared before adding only OS/runtime essentials and exact isolation variables. A fresh update-check cache with version `0.18.2`, `behind: 0`, null revision and a current timestamp prevented the dashboard/TUI update checker from fetching. No real `.env` or `config.yaml` was created.

One PowerShell preseed command reused the reserved case-insensitive `$HOME` variable and created `C:\Users\pablo\.update_check` instead of the intended isolated path. Metadata and exact non-secret content proved the file was created by that command at that instant. It was removed immediately, verified absent, and recreated under the isolated dashboard home using `$dashboardHome`. No prior personal file was overwritten and no credential or personal Hermes state was read.

## Provider-Null Boundary

```yaml
HermesProviderNullBoundary:
  real_api_key_present: false
  real_env_loaded: false
  provider_configuration_loaded: false
  provider_request_attempted: false
  model_request_attempted: false
  oauth_attempted: false
  mcp_started: false
  external_worker_started: false
  gateway_started: false
  agent_task_started: false
  chat_prompt_submitted: false
```

`/api/status` reported no gateway, no active agents, no active sessions, no auth requirement and no auth providers. The UI was inspected on the Sessions route only. Navigation labels for Keys, MCP, Channels and other capabilities were visible but none was activated.

A separate Chrome capability probe using `chrome.exe --version` behaved unexpectedly on this host: it launched Chrome instead of returning a version and attempted Chrome background service traffic before the shell timed it out. Those processes exited and were verified absent. This was not a Hermes, provider or model request, but it violated the desired strict browser-isolation posture. Automated screenshot acquisition was therefore stopped permanently for this ticket. The human performed the UI capture manually as subsequently directed.

## Controlled Launch

The authoritative controlled launch was:

```text
command: .venv\Scripts\python.exe -m hermes_cli.main dashboard --host 127.0.0.1 --port 0 --no-open --skip-build
working_directory: 2_products/hermes-agent
controller_pid: 6840
dashboard_pid: 21340
started: 2026-07-13T17:02:46.941451+02:00
bound_host: 127.0.0.1
bound_port: 52124
readiness_file: 9_artifacts/hermes/p12.4/runtime/dashboard-ready.json
stdout: 9_artifacts/hermes/p12.4/logs/dashboard.stdout.log
stderr: 9_artifacts/hermes/p12.4/logs/dashboard.stderr.log
```

The launch used prebuilt ignored dashboard and TUI outputs. No dependency install, source write, lock update, browser open, provider request, chat session, gateway, worker, MCP server or OAuth flow occurred.

An earlier launch reached the readiness sentinel on port `62587`, but the tool execution host reaped the detached controller and dashboard when its launching shell returned. No process remained and no HTTP claim was retained for that attempt. The same owned controller was relaunched through Windows process management, after which port `52124` remained live for human inspection and final evidence.

## Dashboard Readiness

```yaml
HermesDashboardReadiness:
  url: http://127.0.0.1:52124/
  ready_sentinel: HERMES_DASHBOARD_READY port=52124
  api_status_http_code: 200
  root_http_code: 200
  root_response_bytes: 721
  version: 0.18.2
  release_date: 2026.7.7.2
  hermes_home_matches_isolated_path: true
  gateway_running: false
  active_agents: 0
  active_sessions: 0
  auth_required: false
  auth_providers: []
  gateway_health_url: null
```

The root SPA and public status endpoint were reachable only on localhost. The status response identified the exact isolated Hermes home and config/env paths under P12.4 artifacts.

## UI Snapshot Evidence

```yaml
HermesUISnapshotEvidence:
  capture_actor: human
  automation_used: false
  retained_file: false
  retention: clipboard_only_conversation_attachment
  evidence_identifier: Image 1
  timestamp_window: 2026-07-13T17:02:46+02:00 to 2026-07-13T17:03:47+02:00
  route: /sessions
  capture_pixel_dimensions: 915x1006
  application_state: provider_null_empty_sessions
  observed_result: dashboard_shell_loaded
```

The human-captured image shows:

- Hermes Agent product identity and version `v0.18.2`;
- the Sessions page and complete left navigation shell;
- zero total, active, archived and message counts;
- `No sessions yet` empty state;
- gateway status `Off` and active sessions `0`;
- no provider data, credential prompt, OAuth prompt or visible fatal startup error.

The screenshot remained clipboard-only and was attached to the execution conversation as `Image 1`. No screenshot file was created, committed or retained under `9_artifacts`.

## Shutdown Validation

```yaml
HermesDashboardShutdown:
  shutdown_requested: 2026-07-13T17:03:47.669252+02:00
  graceful_ctrl_break_sent: true
  graceful_exit_within_20_seconds: false
  exact_owned_tree_fallback_used: true
  dashboard_exit_code: 1
  finished: 2026-07-13T17:04:08.399534+02:00
  dashboard_pid_remaining: false
  controller_pid_remaining: false
  owned_child_processes_remaining: 0
  port_52124_listening_after_cleanup: false
  unmanaged_process_remaining: false
```

Ctrl+Break was attempted first. The dashboard did not exit within 20 seconds, so the controller used exact PID-tree termination. This repeats the known Windows graceful-stop limitation from P11.8. The listener was released; only transient localhost FIN-WAIT/TIME-WAIT sockets from manual inspection remained, with no listening socket.

## Generated Artifact Register

| Path | Producer | Retained | Ignored | Tracked/staged |
| --- | --- | --- | --- | --- |
| `2_products/hermes-agent/.pytest_cache` | pytest | Yes | Yes | No |
| `2_products/hermes-agent/hermes_cli/web_dist` | dashboard Vite build | Yes | Yes | No |
| `2_products/hermes-agent/ui-tui/dist` | TUI build | Yes | Yes | No |
| `2_products/hermes-agent/ui-tui/packages/hermes-ink/dist` | Ink build | Yes | Yes | No |
| `2_products/hermes-agent/apps/desktop/dist` | desktop Vite build | Yes | Yes | No |
| `2_products/hermes-agent/apps/desktop/build` | desktop stamp/native staging | Yes | Yes | No |
| `9_artifacts/hermes/p12.4/logs` | validation/runtime logs | Yes | Yes | No |
| `9_artifacts/hermes/p12.4/runtime` | sanitized test/dashboard state | Yes | Yes | No |
| `9_artifacts/hermes/p12.4/cache` | redirected npm/Ruff caches | Yes | Yes | No |
| `9_artifacts/hermes/p12.4/run-sanitized.ps1` | bounded command runner | Yes | Yes | No |
| `9_artifacts/hermes/p12.4/dashboard_lifecycle.py` | process owner/controller | Yes | Yes | No |
| `9_artifacts/hermes/p12.4/bootstrap/uv-env` | exact uv bootstrap | Removed | Yes | No |
| Conversation `Image 1` | human clipboard capture | Conversation only | N/A | No file |

Transient test-owned `.worktrees`, `%SystemDrive%`, branch and worktree state was removed after exact ownership was established. P12.3 `.venv`, `node_modules` and editable metadata remain available and unchanged.

## Failure Inventory

```yaml
HermesBaselineFailures:
  - lane: python_type_advisory
    command: ty check --output-format gitlab --exit-zero
    exit_code: 0
    classification: upstream_source_failure
    blocking_for_P12_6: false
    blocking_for_P13: false
    evidence: 10889 diagnostics and one fatal incomplete-analysis warning; upstream command is advisory by design
  - lane: python_representative_tests
    command: python -m pytest -q <selected paths>
    exit_code: 1
    classification: windows_platform_limitation
    blocking_for_P12_6: false
    blocking_for_P13: false
    evidence: 5535 passed, 198 failed, 41 skipped; native Windows direct process lacks authoritative POSIX per-file isolation
  - lane: dashboard_lint
    command: npm run --prefix web lint
    exit_code: 1
    classification: upstream_source_failure
    blocking_for_P12_6: false
    blocking_for_P13: false
    evidence: 28 errors and 3 warnings from declared ESLint rules; build, typecheck and tests still pass
  - lane: tui_lint
    command: npm run --prefix ui-tui lint
    exit_code: 1
    classification: upstream_source_failure
    blocking_for_P12_6: false
    blocking_for_P13: false
    evidence: 1 error and 14 warnings
  - lane: tui_tests
    command: npm run --prefix ui-tui test
    exit_code: 1
    classification: optional_surface_missing
    blocking_for_P12_6: false
    blocking_for_P13: false
    evidence: clean generated state lacks the unchained hermes-ink dist prebuild; 756 tests passed and 3 Windows-sensitive tests failed
  - lane: desktop_renderer_tests
    command: npm run --prefix apps/desktop test:ui
    exit_code: 1
    classification: upstream_source_failure
    blocking_for_P12_6: false
    blocking_for_P13: false
    evidence: 1148 passed, 27 failed; Vitest also treats 36 CommonJS node:test files as empty suites
  - lane: desktop_platform_tests
    command: npm run --prefix apps/desktop test:desktop:platforms
    exit_code: 1
    classification: windows_platform_limitation
    blocking_for_P12_6: false
    blocking_for_P13: false
    evidence: 300 passed, 9 failed; Windows path length/Bash conversion and parent-Git fixture isolation; transient test-created refs/worktree fully reversed
  - lane: browser_capability_probe
    command: chrome.exe --version
    exit_code: timeout
    classification: environment_mismatch
    blocking_for_P12_6: false
    blocking_for_P13: false
    evidence: Chrome unexpectedly launched background services; all processes exited; automation prohibited and human evidence substituted
  - lane: first_dashboard_detachment
    command: python -m hermes_cli.main dashboard --host 127.0.0.1 --port 0 --no-open --skip-build
    exit_code: host_reaped
    classification: environment_mismatch
    blocking_for_P12_6: false
    blocking_for_P13: false
    evidence: first launch reached port 62587 but execution host reaped detached descendants; Windows process-management relaunch passed
  - lane: dashboard_shutdown
    command: CTRL_BREAK_EVENT then exact taskkill PID tree fallback
    exit_code: 1
    classification: windows_platform_limitation
    blocking_for_P12_6: false
    blocking_for_P13: false
    evidence: graceful signal did not exit within 20 seconds; exact owned tree stopped and port/listener/children cleared
  - lane: runtime_preseed_path
    command: PowerShell update-cache preseed
    exit_code: 0_with_nonterminating_error
    classification: environment_mismatch
    blocking_for_P12_6: false
    blocking_for_P13: false
    evidence: reserved $HOME collision created one known non-secret file outside isolation; exact file immediately removed and verified absent
```

No failure was classified as `imported_snapshot_regression` or `exclusion_policy_regression`. The source manifests and all imported baseline hashes remained valid.

## Source Drift Validation

Before/after SHA-256 comparison:

| Input | SHA-256 | Match |
| --- | --- | --- |
| `pyproject.toml` | `7F0180B23C28EA3F7A32E037BCFB1D986FA1925D0A9331112BDCE82EF1BFBF45` | Yes |
| `uv.lock` | `92D8153C76379A4D427EAF37CD77CEDEF9DC093C6C44C1386ABD4546578F709A` | Yes |
| `package.json` | `07B1B0C8D196C93CC4876092907E7350CFC8B04DB18CE34DEBB522AEAD4AD1C0` | Yes |
| `package-lock.json` | `BC11D099F043E142764E66F60F2B558ADD882948649101645D56319D188861DF` | Yes |
| `UPSTREAM_PROVENANCE.md` | `78DB7ACCCD38CACC1771792CA9C99CF3A063F60AC2E04D966E05CAE22C335B43` | Yes |
| `SOURCE_IMPORT_MANIFEST.tsv` | `58A3392C7515EC2A8AAAF8E43530AE6299B2696957D095BE461DF51E8A080D5C` | Yes |
| `SOURCE_EXCLUSIONS.tsv` | `7A413310330E4625146BCAD9C73E62AF2634F5F3130530111A9B766DAF25D64E` | Yes |
| `NOTICE` | `4AC2353FC0B52C937B43BA6AE54D9D28CE3C4D400B87B7DD4894C2CC2026C145` | Yes |
| `THIRD_PARTY_NOTICES.md` | `C3C564D96A3EF0E9EE9AFCCD44AE43785C311EF1A5262E5043C786DA8DF0E5AA` | Yes |
| Product `.gitignore` | `CC50D6A4E5789A08F19A4F17D306CE14CFDA4032B5EC248E2C1383106959CC30` | Yes |
| `web/vite.config.ts` | `AE93313111185ABE5884374B9218B23F85D54BB88ABE04098372FBA191B85588` | Yes |
| `web/package.json` | `BD0EA5B445157F29B48021A50191F8DD5DC844C521492E1013F187F6AF9F08F7` | Yes |
| `ui-tui/package.json` | `FD9A6B0E5D5C70624E0C29EF3E5AB066FD442B561511DF8BB9F0CFF07EAFD555` | Yes |
| `ui-tui/scripts/build.mjs` | `152E99169E36953638AC09F86E7CD0E1CE73620AF3568A3085D2BF732A0CC76E` | Yes |
| `apps/desktop/package.json` | `3AD38970DE6B859E0A19600E95085F9CC50A8F53776095A45CAE22AA70FEC10E` | Yes |
| `apps/desktop/vite.config.ts` | `E64D827E1D32C44638517E72029AC096181A10E1F78FE78BFE8704A7C3B6A7FE` | Yes |

Final source/Git facts before creating this record:

```yaml
HermesSourceDriftValidation:
  main_branch: main
  main_head: 0b5ea15bc2ce8d36b0218eb3d03639944637ffb7
  product_tracked_files: 6120
  product_status_paths: 0
  product_staged_paths: 0
  total_staged_paths: 0
  hash_mismatch_count: 0
  source_drift_detected: false
  lockfile_drift_detected: false
  product_gitignore_modified: false
  root_gitignore_sha256: E1A7238DB58ABFA93DA762EC87801DF8B74877CC573608ED0F83E55EC352C40A
  nested_git_present: false
  upstream_head: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  upstream_tag: v2026.7.7.2
  upstream_status_paths: 0
  upstream_sync_performed: false
```

At durable handoff, the only main-repository work created by P12.4 is this canonical record. `.opencode/`, `AGENTS.md` and `graphify-out/` remain unrelated pre-existing untracked paths and were not inspected, modified or staged by P12.4 execution.

## Baseline Capability Statement

The controlled Hermes snapshot can be validated, built and launched locally on this Windows host with known failures.

Accepted usable subset:

- frozen Python and npm dependency environments are valid;
- Python lock, Ruff and Windows-footgun lanes pass;
- all five selected TypeScript package checks pass;
- dashboard tests pass 33/33;
- dashboard, Ink/TUI and Electron renderer production builds pass;
- the provider-null dashboard binds an ephemeral localhost port;
- `/api/status` and the SPA root return HTTP 200;
- the human-observed Sessions shell renders with product identity and empty isolated state;
- exact process ownership and fallback cleanup leave no listener or child process;
- no imported source or lockfile drift exists.

Not accepted as green:

- advisory Python Ty analysis;
- representative native-Windows Python tests;
- dashboard and TUI lint;
- TUI tests from clean unbuilt Ink output;
- desktop renderer and platform tests;
- application-level graceful shutdown on Windows;
- embedded dashboard chat on native Windows;
- any deferred optional/provider/native/deployment surface.

Final capability classification:

```text
baseline_usable_with_known_failures
```

## P12.5 Handoff

P12.5 may consume:

- exact validation/build commands and package roots;
- P12.3 environment versions and Windows-specific behavior;
- the green lock, typecheck, dashboard test and production build lanes;
- the Python, lint, TUI and desktop failure inventory;
- generated output paths and hashes;
- the temporary-Git-fixture containment defect;
- dashboard startup/readiness and exact-tree shutdown behavior;
- the fact that P12.4 changed no source relative to the P12.2 baseline.

P12.4 performed no fetch, pull, merge, rebase, upstream update, publication or push. P12.5 remains synchronization-strategy design unless separately authorized.

## P12.6 Handoff

P12.6 may proceed after human acceptance because the final verdict is not an import regression and the main dashboard/TUI/desktop frontend builds are usable.

P12.6 must preserve:

- the P12.2 provenance/exclusion baseline and all lockfiles;
- the provider-null, credential-free startup boundary;
- the known generated output paths;
- dashboard entry `web/src/main.tsx` and backend `hermes_cli/web_server.py`;
- TUI entry `ui-tui/src/entry.tsx` and gateway boundary `tui_gateway`;
- desktop renderer entry `apps/desktop/src/main.tsx` and headless backend relationship;
- the failure baseline rather than treating it as newly introduced by product extensions.

Any P12.6 change must run targeted affected tests in appropriate isolation. The desktop Git-fixture suite must not be run with temporary repositories nested under the main worktree. Graceful Windows shutdown requires explicit follow-up rather than assuming Ctrl+Break works.

```yaml
P12_6_Readiness:
  imported_product_sufficiently_usable: true
  baseline_invalid_due_to_import_regression: false
  known_green_lanes_recorded: true
  known_failing_lanes_recorded: true
  source_modification_baseline_exact: true
  provider_null_boundary_known: true
  may_proceed_after_acceptance: true
```

## P13 Readiness Implications

The current product UI baseline is the browser dashboard owned by `2_products/hermes-agent/web`, served by `hermes_cli.web_server`, with the human-observed route `/sessions`.

Safe extension seams for later authorized work include the React route/page/navigation shell under `web/src`, shared transport primitives under `apps/shared`, and the existing FastAPI dashboard APIs. The dashboard production build and root/status serving are green.

The screenshot confirms the current Sessions shell, navigation, empty-state layout, gateway-off status and product identity. It does not validate chat, provider setup, Keys, MCP, Channels, OAuth or worker behavior. Native Windows embedded chat remains blocked by the POSIX/WSL PTY boundary. The Electron renderer is a separate UI surface: it builds successfully but its current declared test lanes are not green. P13 may use the browser dashboard as the initial usable shell while retaining those limitations.

## Rollback and Cleanup

Completed cleanup:

- stopped the dashboard and lifecycle controller;
- removed every exact owned dashboard child process;
- confirmed port `52124` has no listening socket;
- removed the temporary uv `0.11.6` bootstrap environment;
- removed test-created branches `feature`, `rawr`, `wt` and `cool/feature` after proving exact ownership and unchanged commit identity;
- removed the test-created registered worktree and empty `.worktrees` parent;
- removed the test-created literal `%SystemDrive%` product tree;
- removed the accidental personal-root `.update_check` and verified absence;
- preserved P12.3 `.venv`, root `node_modules` and editable package metadata;
- retained only ignored logs, caches, runtime state and selected build outputs needed for review.

Optional later artifact cleanup, after human review, may remove only exact ignored P12.4 paths and selected generated build outputs after containment and ignore checks. Git clean/reset/restore, wildcard deletion and parent-directory deletion are prohibited.

## Created / Modified / Generated / Not Created Register

Created durable:

```text
0_architecture/governance/agent_platform_hermes_baseline_build_test_ui_snapshot.md
```

Modified tracked product/governance files:

```text
none
```

Generated and ignored:

```text
2_products/hermes-agent/.pytest_cache/**
2_products/hermes-agent/hermes_cli/web_dist/**
2_products/hermes-agent/ui-tui/dist/**
2_products/hermes-agent/ui-tui/packages/hermes-ink/dist/**
2_products/hermes-agent/apps/desktop/dist/**
2_products/hermes-agent/apps/desktop/build/**
9_artifacts/hermes/p12.4/**
```

Transient and removed:

```text
9_artifacts/hermes/p12.4/bootstrap/uv-env
.worktrees/cool-feature
.worktrees
2_products/hermes-agent/%SystemDrive%
refs/heads/feature
refs/heads/rawr
refs/heads/wt
refs/heads/cool/feature
C:\Users\pablo\.update_check
all owned dashboard/controller processes and listener
```

Not created, modified or activated:

```text
root or product-local .gitignore
pyproject.toml, uv.lock, package.json or package-lock.json
source code or tests
P12.2 legal/provenance files
P12.3 or earlier governance records
real .env, provider credentials, OAuth state or MCP configuration
provider/model request, agent task, worker or gateway
website/docs environment
WhatsApp or Photon environment/runtime
Rust/Tauri package, Nix environment or container
release, publication or deployment artifact
upstream source or upstream Git state
staging, commit or push
additional durable Markdown
retained screenshot file
```

## Limitations

- Python `3.12.3` and Node `24.12.0` satisfy declared constraints but differ from primary CI versions Python `3.11` and Node `22`.
- The full authoritative Python wrapper is POSIX-oriented and was not reproducible from the selected native-Windows `.venv`; direct broad pytest execution loses its per-file process isolation.
- Ty is advisory and incomplete, with 10,889 diagnostics and one fatal analysis warning.
- Dashboard and TUI declared lint scripts are non-green even though their builds/typechecks pass.
- TUI tests require an undeclared prebuilt local Ink output for full collection from clean generated state.
- Desktop `test:ui` mixes Vitest with CommonJS `node:test` files and retains stale renderer assertions/mocks.
- Desktop platform tests are unsafe when their temporary Git fixtures are nested inside a parent worktree and also encounter Windows path-length/Bash translation failures.
- A Chrome capability probe unexpectedly used Chrome background services. No browser automation was attempted afterward; UI evidence is human-captured.
- The screenshot is a clipboard-only conversation attachment, not a retained artifact file.
- Dashboard Ctrl+Break shutdown was not graceful; exact-tree fallback was required, as in the prior P11.8 Windows lifecycle.
- The dashboard Sessions shell is usable, but native Windows embedded chat PTY behavior remains unaccepted.
- No provider, model, OAuth, MCP, external worker, gateway, chat task or real user state was exercised.
- Deferred website, optional bridge, Rust/Tauri, Nix and container surfaces remain unaccepted.
- P12.2 legal, SBOM, asset, trademark, redistribution, publication and release blockers remain unchanged.

## Final Verdict

```yaml
P12_4_BaselineBuildTestUISnapshotVerdict:
  p12_3_environment_committed: true
  product_baseline_clean_before_validation: true
  validation_lane_inventory_complete: true
  python_lint_baseline_recorded: true
  python_type_baseline_recorded: true
  python_test_baseline_recorded: true
  node_dependency_baseline_recorded: true
  node_validation_baseline_recorded: true
  frontend_build_baseline_recorded: true
  tui_baseline_recorded: true
  desktop_baseline_recorded: true
  controlled_ui_launch_attempted: true
  ui_snapshot_evidence_recorded: true
  controlled_shutdown_completed: true
  graceful_shutdown_succeeded: false
  exact_owned_tree_cleanup_succeeded: true
  failures_classified: true
  imported_snapshot_regression_detected: false
  exclusion_policy_regression_detected: false
  source_drift_detected: false
  lockfiles_unchanged: true
  credentials_used: false
  provider_request_performed: false
  model_request_performed: false
  generated_artifacts_ignored: true
  P12_5_may_proceed: true
  P12_6_may_proceed: true
  final_verdict: baseline_usable_with_known_failures
```

Required result markers:

```text
hermes_baseline_build_test_ui_snapshot_complete
hermes_python_validation_baseline_recorded
hermes_node_validation_baseline_recorded
hermes_frontend_build_baseline_recorded
hermes_test_failure_inventory_recorded
hermes_controlled_ui_launch_evidence_recorded
hermes_dashboard_lifecycle_evidence_recorded
hermes_application_startup_boundary_preserved
hermes_provider_boundary_preserved
hermes_source_drift_absent
hermes_lockfiles_unchanged
hermes_baseline_artifacts_isolated
hermes_P12_5_ready
hermes_P12_6_ready_after_acceptance
no_credentials_used
no_provider_request
no_upstream_sync
no_git_mutation_by_agent
```

`no_git_mutation_by_agent` means no retained agent-created Git state and no agent staging, commit, push, remote change or upstream synchronization. It does not conceal the transient branch/worktree mutation caused by the declared desktop platform test; that failure is explicitly inventoried and its exact test-owned state was reversed before handoff.

## Human Commit Boundary

The agent did not stage, commit or push. After review, the intended commit contains only this record:

```powershell
$ErrorActionPreference = "Stop"

$Record = "0_architecture/governance/agent_platform_hermes_baseline_build_test_ui_snapshot.md"
$Allowed = @($Record)

git status --short
git add -- $Allowed

$Expected = @(
    $Allowed |
        ForEach-Object { $_.Replace("\", "/") } |
        Sort-Object -Unique
)

$Staged = @(
    git diff --cached --name-only |
        ForEach-Object { $_.Replace("\", "/") } |
        Sort-Object -Unique
)

$Unexpected = @(
    Compare-Object -ReferenceObject $Expected -DifferenceObject $Staged |
        Where-Object SideIndicator -eq "=>" |
        ForEach-Object InputObject
)

$Missing = @(
    Compare-Object -ReferenceObject $Expected -DifferenceObject $Staged |
        Where-Object SideIndicator -eq "<=" |
        ForEach-Object InputObject
)

if ($Unexpected.Count -gt 0) {
    throw "Unexpected staged paths: $($Unexpected -join ', ')"
}

if ($Missing.Count -gt 0) {
    throw "Required paths not staged: $($Missing -join ', ')"
}

$ProductDrift = @(git status --short -- "2_products/hermes-agent")
if ($ProductDrift.Count -gt 0) {
    throw "Unexpected product drift: $($ProductDrift -join ', ')"
}

git diff --cached --check
if ($LASTEXITCODE -ne 0) {
    throw "git diff --cached --check failed"
}

git diff --cached --stat
git commit -m "P12.4 - Record Hermes build test and UI baseline"
git push origin main
```

Never use `git add .`, `git add -A` or `git add -f`.
