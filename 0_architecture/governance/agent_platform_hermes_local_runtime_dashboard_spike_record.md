# P11.6 - Hermes Local Runtime and Dashboard Spike Record

## Document Header

| Field | Value |
| --- | --- |
| Title | Hermes Local Runtime and Dashboard Spike Record |
| Ticket | P11.6 |
| Status | Completed bounded local runtime/dashboard spike |
| Date | 2026-07-12 |
| Scope | One disposable local installation, frontend build, dashboard launch, manual administrative UI inspection, shutdown, residual inventory, and cleanup for the exact P11.0-locked Hermes source. |
| Authority | P11.6 spike record only. No source modification, fork creation, UI customization, provider credential configuration, model execution, MCP activation, gateway activation, cron/Kanban dispatcher activation, product/Siamese source access, publication, or Git mutation. |
| Canonical output | `0_architecture/governance/agent_platform_hermes_local_runtime_dashboard_spike_record.md` |

Result markers:

```text
hermes_local_runtime_dashboard_spike_completed
hermes_dashboard_admin_ui_verified
hermes_frontend_build_verified_in_temp_source_copy
hermes_shutdown_cleanup_completed
hermes_spike_ready_for_P11_7_safety_review
```

## Executive Result

P11.6 completed one bounded local Hermes runtime/dashboard spike against a disposable copy of the exact P11.0-locked Hermes source.

The administrative dashboard loaded successfully at:

```text
http://127.0.0.1:9119
```

Manual administrative UI inspection completed successfully for:

```text
Sessions
Models
Logs
```

Observed successful dashboard facts:

| Check | Result |
| --- | --- |
| Hermes version | `0.18.2` |
| Release date / tag surface | `2026.7.7.2` |
| Dashboard listener | `127.0.0.1:9119` only |
| `/api/status` | HTTP 200 |
| `/` | HTTP 200, actual dashboard HTML after frontend build |
| Frontend asset | `/assets/index-BeEPWuxw.js`, HTTP 200 |
| Gateway | Off / not running |
| Active sessions | `0` |
| Active agents | `0` |
| Temporary `HERMES_HOME` | Used |
| Normal user Hermes profile | Not used |
| `.env` in temporary `HERMES_HOME` | Not present |
| Provider credentials configured | No |
| MCP configured or activated | No |
| Git mutation | No |

P11.7 may proceed as a Hermes Adapter Safety / Rollback Review input. P11.7 must treat this as local spike evidence only, not as authorization for P11.8 controlled runtime activation.

## Inputs Consumed

| Input | Status | P11.6 use |
| --- | --- | --- |
| P11.0 Hermes Source Review Authorization | Present | Source identity, repository, tag, commit, and no-Git/no-source-mutation boundary. |
| P11.1 Hermes License / Dependency / Runtime Audit | Present | License/dependency/runtime risks, `.[web]` dashboard dependency posture, lazy-install blocker, persistent-state inventory, shutdown risk. |
| P11.2 Hermes Architecture Mapping | Present | Dashboard, runtime, tool, memory, provider, Kanban, workspace, and adapter seams. |
| P11.3 Runtime / Cadence Boundary Decision | Present | P11.6 minimal isolated session/dashboard constraints and shutdown/cleanup requirements. |
| P11.4 Adoption Mode Decision | Present | Phase A `wrap_existing_source` strategy and exact local spike constraints. |
| P11.5 Interface Adapter Design | Present | Temporary `HERMES_HOME`, workspace, shutdown, runtime event, and rollback expectations. |

No Graphify update or rerun was performed for P11.6.

## Source Identity

Locked upstream reference:

```text
path: 4_external/sources/hermes-agent
origin: https://github.com/nousresearch/hermes-agent.git
HEAD: 9de9c25f620ff7f1ce0fd5457d596052d5159596
working tree: clean
```

Identity commands used a temporary per-command `safe.directory` override only:

```powershell
git -c safe.directory="C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM/4_external/sources/hermes-agent" -C "4_external/sources/hermes-agent" remote get-url origin
git -c safe.directory="C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM/4_external/sources/hermes-agent" -C "4_external/sources/hermes-agent" rev-parse HEAD
git -c safe.directory="C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM/4_external/sources/hermes-agent" -C "4_external/sources/hermes-agent" tag --points-at HEAD
git -c safe.directory="C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM/4_external/sources/hermes-agent" -C "4_external/sources/hermes-agent" status --short
```

No global Git configuration was changed.

## Temporary Runtime Layout

Disposable root:

```text
C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_6-hermes
```

Created subdirectories:

```text
source-work
venv
hermes-home
workspace
logs
quarantine
```

The upstream source remained unchanged. Runtime, build, dependency, cache, log, and state writes were confined to the disposable temporary root before cleanup.

Temporary copy command shape:

```powershell
robocopy <locked-upstream> <temp-root>\source-work /E /XD .git skills\productivity\powerpoint __pycache__ .pytest_cache .mypy_cache .ruff_cache node_modules .venv venv dist build web_dist .turbo .next cache caches /XF .env .env.*
```

Copy validation:

| Check | Result |
| --- | --- |
| `.git` excluded | Yes |
| `skills/productivity/powerpoint` excluded | Yes |
| `pyproject.toml` present | Yes |
| `package.json` present | Yes |
| `package-lock.json` present | Yes |
| `web/package.json` present | Yes |
| Upstream source modified | No |

## Python Environment And Install

Python environment:

```text
base interpreter: C:\Users\pablo\AppData\Local\Programs\Python\Python313\python.exe
base version: 3.13.2
venv: C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_6-hermes\venv
venv interpreter: C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_6-hermes\venv\Scripts\python.exe
```

Install command:

```powershell
python -m pip install --no-cache-dir --disable-pip-version-check ".[web]"
```

Install result:

| Check | Result |
| --- | --- |
| Package installed | `hermes-agent 0.18.2` |
| Dashboard extra | `.[web]` |
| `[all]` extra | Not installed |
| Messaging extras | Not installed intentionally |
| Memory-provider extras | Not installed intentionally |
| Browser/computer-use extras | Not installed intentionally |
| MCP extras | Not installed intentionally |
| Remote execution extras | Not installed intentionally |
| Voice/media extras | Not installed intentionally |
| PowerPoint skill | Excluded from temporary source copy |
| Runtime lazy installs | Disabled in config and env |

Temporary config included:

```yaml
security:
  allow_lazy_installs: false
mcp_servers: {}
model: ""
providers: {}
fallback_providers: []
plugins:
  enabled: []
cron:
  provider: ""
kanban:
  dispatch_in_gateway: false
  auto_decompose: false
logging:
  level: WARNING
```

Correction note: an initial PowerShell variable-name error attempted to write this temporary config to `C:\Users\pablo\config.yaml`. The file content was verified as the P11.6 temp config and removed immediately. The intended temp config was then written to `C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_6-hermes\hermes-home\config.yaml`. No residual `C:\Users\pablo\config.yaml` remained.

## Dashboard Execution History

### Initial Backend-Only Launch

Authorized command:

```powershell
hermes dashboard --host 127.0.0.1 --port 9119 --no-open
```

Observed backend result:

| Check | Result |
| --- | --- |
| `/api/status` | HTTP 200 |
| Hermes version | `0.18.2` |
| Temporary `HERMES_HOME` | `C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_6-hermes\hermes-home` |
| Gateway | Not running |
| Active agents | `0` |
| Listener | `127.0.0.1:9119` only |
| Root UI | `Frontend not built. Run: cd web && npm run build` |

This established that the backend could start under the isolated temporary profile, but the dashboard frontend assets were absent from the source copy.

### Authorized Frontend Build Continuation

The P11.6 continuation authorized the omitted Node frontend build inside the existing disposable source copy only:

```text
C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_6-hermes\source-work
```

Preconditions:

| Check | Result |
| --- | --- |
| Previous dashboard process stopped | Yes |
| Port 9119 closed before build | Yes |
| Node.js available | `v24.12.0` |
| npm available | `11.6.2` |
| Node.js >= 20 | Yes |
| `package.json` present | Yes |
| `package-lock.json` present | Yes |
| `web/package.json` present | Yes |
| Temp `package-lock.json` hash matched upstream before build | Yes, SHA-256 `5683D49882DDF555378F5180E6DE899A6A1BDCED12743509E3C2066E582A65E1` |

npm controls:

```text
npm cache: C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_6-hermes\logs\npm-cache
npm audit: disabled
npm fund: disabled
npm update notifier: disabled
global install: not used
PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
PUPPETEER_SKIP_DOWNLOAD=1
CYPRESS_INSTALL_BINARY=0
```

Authorized Node commands:

```powershell
npm ci --workspace web --include-workspace-root=false
npm run build --workspace web
```

Build script confirmed from locked `web/package.json`:

```text
tsc -b && vite build
```

Node results:

| Check | Result |
| --- | --- |
| `npm ci --workspace web --include-workspace-root=false` | Exit 0, 488 packages added |
| `npm run build --workspace web` | Exit 0 |
| Package lock modified | No |
| Non-generated source hash diff | `0` |
| Desktop `node_modules` created | No |
| TUI `node_modules` created | No |
| Browser/Playwright execution | Not observed |
| Electron/Tauri packaging | Not observed |
| Documentation build | Not run |

Frontend output note:

The continuation requested validation of `web/dist`, but the locked Vite config in `web/vite.config.ts` sets:

```text
build.outDir = ../hermes_cli/web_dist
```

Therefore the actual locked output was:

```text
C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_6-hermes\source-work\hermes_cli\web_dist
```

Output validation:

| Check | Result |
| --- | --- |
| Requested `web/dist` path | Absent, because locked config writes elsewhere |
| Actual locked output dir `hermes_cli/web_dist` | Present |
| `hermes_cli/web_dist/index.html` | Present |
| Generated assets | 9 files |
| Generated JS assets | 1 file, `index-BeEPWuxw.js` |
| Generated CSS assets | 1 file, `index-DBf7hUZx.css` |

### Second Dashboard Launch With Built Frontend

Authorized command:

```powershell
hermes dashboard --host 127.0.0.1 --port 9119 --no-open --skip-build
```

First `--skip-build` attempt:

| Check | Result |
| --- | --- |
| Command | Same authorized command |
| Result | Exited before listener startup |
| Cause | Console entrypoint resolved `PROJECT_ROOT` to the venv `site-packages`, where `hermes_cli/web_dist` was absent |
| Listener opened | No |

Successful `--skip-build` relaunch:

```powershell
$env:HERMES_WEB_DIST="C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_6-hermes\source-work\hermes_cli\web_dist"
hermes dashboard --host 127.0.0.1 --port 9119 --no-open --skip-build
```

Relaunch result:

| Check | Result |
| --- | --- |
| `/api/status` | HTTP 200 |
| `/` | HTTP 200 |
| Frontend-not-built message | Absent |
| Asset path checked | `/assets/index-BeEPWuxw.js` |
| Asset HTTP status | 200 |
| Listener | `127.0.0.1:9119` only |
| Process tree listener count | 1 |
| Forbidden process match count | 0 |

Observed process tree during successful dashboard launch:

```text
cmd.exe launcher
conhost.exe child
hermes.exe child
python.exe child
python.exe dashboard listener process
```

Process tree listener:

```text
127.0.0.1:9119 pid=6740
```

The user manually opened and inspected the administrative UI at `http://127.0.0.1:9119`.

## Pages And Assets Observed

Manual pages observed:

```text
Sessions
Models
Logs
```

Automated HTTP observations:

```text
GET http://127.0.0.1:9119/api/status -> 200
GET http://127.0.0.1:9119/ -> 200
GET http://127.0.0.1:9119/assets/index-BeEPWuxw.js -> 200
```

The dashboard administrative UI was available. The spike did not execute an agent chat/model task.

Native Windows Chat limitation:

```text
The embedded Chat tab requires a POSIX PTY and may report that WSL2 is required on native Windows.
This limitation is accepted for P11.6 and does not fail the administrative dashboard spike.
WSL2 was not installed.
```

## Network And Provider Observations

Dashboard listener observations:

| Surface | Result |
| --- | --- |
| Approved listener | `127.0.0.1:9119` |
| Public listener | Not observed |
| Process-tree listener count | 1 while running |
| Established external TCP connections at safe metadata sample | 0 |
| Loopback dashboard/browser connections | Observed |
| Gateway process | Not observed |
| Cron/Kanban/MCP/browser/computer-use process | Not observed |

Logs page/provider warnings observed:

```text
Auxiliary: marking openrouter unhealthy for 60s (payment / credit error).
Auxiliary Nous client unavailable: no Nous authentication found (run: hermes auth).
Auxiliary: marking nous unhealthy for 60s (payment / credit error).
```

Classification from available safe evidence:

| Warning class | Classification | Basis |
| --- | --- | --- |
| Nous authentication warning | Local provider-health/auth initialization | Log says no Nous authentication found; no credentials were configured or inspected. |
| OpenRouter unhealthy/payment-credit warning | Unknown from available evidence | Log records auxiliary provider unhealthy marking, but safe process/network metadata sampled no established external TCP connection for the P11.6 process tree. No credential/provider configuration was performed. |
| Nous unhealthy/payment-credit warning after auth warning | Local provider-health initialization with unknown downstream classification | It followed local missing-auth detection; no established external TCP provider connection was observed at metadata sample. |

No provider credentials, API keys, OAuth tokens, `.env`, browser auth, or provider configuration were inspected or configured during P11.6.

## Shutdown Result

Shutdown sequence:

| Step | Result |
| --- | --- |
| Final safe process/network metadata captured before shutdown | Completed |
| Graceful close attempted | Yes |
| Windows closeable main window available | No; hidden console process had `main_window=0` for all recorded P11.6 processes |
| Targeted descendant termination used | Yes, only for recorded P11.6 process tree |
| Remaining recorded P11.6 processes after termination | 0 |
| Port 9119 listener after shutdown | 0 |
| Remaining port 9119 entries | Loopback `TIME_WAIT` only |

Recorded shutdown P11.6 tree before termination:

```text
24712 cmd
2040 conhost
14644 hermes
32616 python
6740 python
```

Targeted termination result:

```text
terminated_p11_6_pid: 6740
terminated_p11_6_pid: 2040
remaining_after_termination_count: 0
port_9119_listeners_after_shutdown: 0
```

This is accepted as deterministic shutdown for native Windows under the observed hidden-console limitation.

## Residual Inventory Before Cleanup

Temporary root before cleanup:

```text
C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_6-hermes
```

Frontend/build residuals:

| Item | Result |
| --- | --- |
| Actual web output | `source-work/hermes_cli/web_dist` |
| Actual web output asset count | 9 |
| JS assets | 1 |
| CSS assets | 1 |
| `node_modules` | Present under temp source root/web workspace resolution |
| desktop `node_modules` | Absent |
| TUI `node_modules` | Absent |
| package lock final hash | `5683D49882DDF555378F5180E6DE899A6A1BDCED12743509E3C2066E582A65E1` |
| package lock still matched upstream | Yes |

npm/log residuals before cleanup:

| Item | Result |
| --- | --- |
| npm cache path | `logs/npm-cache` |
| npm cache file count | 948 |
| npm cache bytes | 66,159,022 |
| P11.6 log file count including npm cache logs | 968 |
| P11.6 log bytes including npm cache | 67,561,034 |

Temporary `HERMES_HOME` residuals before cleanup:

| Item | Result |
| --- | --- |
| Temporary `HERMES_HOME` file count | 15 |
| Temporary `HERMES_HOME` bytes | 27,849,956 |
| `.env` present | No |
| Workspace file count | 0 |

Temporary `HERMES_HOME` files observed by safe path/name inventory:

```text
.update_check
cache/model_catalog.json
config.yaml
logs/.__agent.lock
logs/.__errors.lock
logs/agent.log
logs/errors.log
models_dev_cache.json
ollama_cloud_models_cache.json
skills/.hub/index-cache/hermes-index.json
SOUL.md
state.db
state.db-shm
state.db-wal
```

No user/private Hermes profile, user `.env`, user sessions, user memories, provider credentials, OAuth state, browser credentials, or product/Siamese source was inspected.

## Cleanup / Quarantine Result

Cleanup action:

```powershell
Remove-Item -LiteralPath "$env:TEMP\agent-platform-p11_6-hermes" -Recurse -Force
```

Cleanup result:

| Check | Result |
| --- | --- |
| Disposable runtime root exists after cleanup | No |
| Port 9119 listener after cleanup | 0 |
| Upstream source modified | No |
| Git mutated | No |

Safe metadata retained only in this canonical P11.6 record.

## Blockers And Limitations

P11.6 completed its administrative dashboard spike, but the following limitations remain for P11.7/P11.8:

| Limitation | Consequence |
| --- | --- |
| Native Windows Chat/PTY limitation | Embedded Chat tab may require WSL2/POSIX PTY; not a dashboard-admin failure. |
| Frontend build output path differs from requested `web/dist` | Locked Vite config writes to `hermes_cli/web_dist`; future automation must use the source config or set `HERMES_WEB_DIST`. |
| Dashboard startup generated local caches/state | Future adapter must explicitly bound model catalog, skills index, SQLite state, and cache behavior. |
| Auxiliary provider warnings appeared | Future safety review must disable or bound provider-health initialization before runtime gates. |
| Shutdown on native Windows required targeted termination | Future adapter must define a first-class stop/kill route and verify descendant cleanup. |
| No agent chat/model execution performed | P11.6 validates administrative dashboard availability, not agent task execution. |
| No provider credentials configured | Provider/model execution remains unvalidated and blocked. |

## Created / Modified / Not Created Register

Created as final canonical output:

```text
0_architecture/governance/agent_platform_hermes_local_runtime_dashboard_spike_record.md
```

Removed from working tree as obsolete placeholder:

```text
0_architecture/governance/agent_platform_hermes_local_shell_spike_record.md
```

Temporary runtime artifacts were created only under:

```text
C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_6-hermes
```

and were removed during cleanup.

Not created, activated, modified, or used:

```text
no upstream Hermes source modification
no fork creation
no UI customization
no product/Siamese source access
no normal user Hermes profile access
no credential, .env, token, OAuth, browser-auth, or provider-config inspection
no provider credential configuration
no model/agent chat execution
no gateway activation
no messaging channel activation
no proxy activation
no API server or webhook activation beyond the authorized dashboard backend routes
no cron or persistent scheduler activation
no Kanban dispatcher or auto-decompose activation
no subagent activation
no browser automation
no computer use
no MCP activation
no GBrain or Paperclip integration
no Graphify update or rerun
no publication
no Git mutation
```

## P11.7 Readiness Decision

```yaml
P11_7_readiness:
  may_proceed: true
  scope: safety_rollback_review_only
  basis:
    - exact P11.0 source identity verified
    - disposable source copy and temporary HERMES_HOME used
    - minimum Python dashboard package install succeeded
    - authorized web workspace npm install/build succeeded
    - package-lock unchanged
    - non-generated temp source hashes unchanged
    - dashboard backend returned /api/status 200
    - administrative dashboard UI loaded with built frontend
    - Sessions, Models, and Logs pages manually observed
    - listener was loopback-only on 127.0.0.1:9119
    - no gateway, cron, Kanban dispatcher, MCP, browser, computer-use, or messaging process observed
    - shutdown and cleanup completed
  retained_limitations:
    - native Windows Chat PTY limitation
    - provider-warning behavior requires safety review
    - dashboard local cache/state writes require adapter containment
    - Windows shutdown needed targeted process-tree termination
    - no agent/model execution validated
  does_not_authorize:
    - P11.8 controlled runtime activation
    - provider/model execution
    - adapter implementation
    - source modification or fork creation
```

## Final Verdict

| Question | Answer |
| --- | --- |
| Did P11.6 perform the authorized local runtime/dashboard spike? | Yes. |
| Was the exact source identity verified first? | Yes. |
| Was the upstream source modified? | No. |
| Was a disposable temp source copy used? | Yes. |
| Was a dedicated temporary `HERMES_HOME` used? | Yes. |
| Was `.[web]` installed in an isolated venv? | Yes. |
| Was the authorized web workspace build run? | Yes. |
| Did the dashboard load after frontend build? | Yes. |
| Was the listener loopback-only? | Yes, `127.0.0.1:9119`. |
| Were Sessions, Models, and Logs observed? | Yes. |
| Were provider credentials configured? | No. |
| Was Git mutated? | No. |
| Was cleanup completed? | Yes. |
| May P11.7 proceed? | Yes, as safety/rollback review only. |

```text
hermes_local_runtime_dashboard_spike_completed
```
