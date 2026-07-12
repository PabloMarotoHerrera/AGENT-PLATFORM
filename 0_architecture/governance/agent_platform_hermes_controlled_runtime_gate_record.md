# P11.8 - Hermes Controlled Runtime Lifecycle Gate

## 0. Context

P11 is **Hermes Real Integration**. P11.8 records one bounded Hermes local process lifecycle gate behind AGENT PLATFORM safety boundaries.

This record corrects the stale blocked interpretation that P11.7 had to provide the exact runtime command. P11.7 defines safety, rollback, stop, cleanup, path-containment, provider, network, and residual-state requirements. P11.8 owns the exact controlled-runtime execution profile and records whether those requirements can be satisfied for one lifecycle substrate run.

P11.8 scope is lifecycle substrate only.

Out of scope and not claimed:

```text
adapter conformance
WorkPacket submission
Hermes agent worker execution
provider/model execution
MCP activation
external messaging
Kanban dispatch
Paperclip task authority
GBrain write-back
Git mutation
production deployment
```

Result markers:

```text
hermes_controlled_runtime_lifecycle_gate_recorded
hermes_lifecycle_substrate_exercised_once
hermes_lifecycle_substrate_accepted_with_limitations
hermes_adapter_conformance_deferred
hermes_workpacket_execution_deferred
hermes_agent_worker_execution_deferred
no_provider_activation
no_model_execution
no_mcp_activation
no_paperclip_task_authority
no_gbrain_write_back
no_git_mutation
```

## 1. Source Lock

Locked Hermes source identity observed for this gate:

| Field | Value |
| --- | --- |
| Source path | `4_external/sources/hermes-agent` |
| Origin | `https://github.com/nousresearch/hermes-agent.git` |
| HEAD | `9de9c25f620ff7f1ce0fd5457d596052d5159596` |
| Tag at HEAD | `v2026.7.7.2` |
| Upstream worktree | Clean when checked before P11.8 execution |

The upstream source tree was not modified. Runtime work used a disposable temp copy under `C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_8-hermes\source-work`, later removed during cleanup.

## 2. Controlled Runtime Profile

```yaml
HermesControlledRuntimeLifecycleProfile:
  profile_id: P11.8-HERMES-LIFECYCLE-001
  source_mode: wrap_existing_source
  runtime_scope: one local Hermes headless backend lifecycle only
  command: hermes serve --host 127.0.0.1 --port 9120 --no-open --skip-build
  stop_primary: hermes serve --stop
  stop_fallback: targeted process-tree termination for only P11.8 descendants
  listener: 127.0.0.1:9120
  temp_root: C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_8-hermes
  hermes_home: temp_root\hermes-home
  workspace: temp_root\workspace
  logs: temp_root\logs
  install_profile: .[web] inside isolated venv
  safe_mode: HERMES_SAFE_MODE=1
  project_plugins: disabled
  mcp_servers: {}
  bundled_skill_seeding: skipped by temp .no-bundled-skills marker
  model_catalog: disabled in temp config and not invoked
  browser_open: disabled
  provider_credentials: not inherited into runtime environment
  runtime_budget_seconds: below Nous keepalive initial delay
```

Runtime environment was sanitized through `System.Diagnostics.ProcessStartInfo` with an explicit environment. It set only the temp `HERMES_HOME`, temp `TEMP`/`TMP`, temp `USERPROFILE`/`LOCALAPPDATA`/`APPDATA`, venv path, Windows system variables needed to start the process, `HERMES_SAFE_MODE=1`, `HERMES_ENABLE_PROJECT_PLUGINS=0`, `HERMES_TUI=0`, `HERMES_DESKTOP=0`, `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`, `CUA_DRIVER_RS_TELEMETRY_ENABLED=0`, and loopback proxy exclusions.

No user `.env`, provider config, OAuth browser auth, normal Hermes profile, product source, `.opencode`, `AGENTS.md`, Graphify output, or Git state was passed into the runtime environment.

## 3. Startup Egress Review

Static startup-egress review was performed against the locked/temp Hermes source before runtime start.

| Surface | P11.8 control | Evidence and limitation |
| --- | --- | --- |
| Update checks | `hermes serve` path does not enter chat/version banner update-check flow. | `check_for_updates()` and `prefetch_update_check()` remain network-capable surfaces, but were not reached by this lifecycle command. |
| Plugins | `HERMES_SAFE_MODE=1`. | Runtime `agent.log` recorded `HERMES_SAFE_MODE=1 - plugin discovery skipped`. Bundled dashboard plugin API mounts still occur at `web_server` import time; reviewed APIs were local-state surfaces. |
| MCP | Temp `config.yaml` contained `mcp_servers: {}`. | `mcp_startup._has_configured_mcp_servers()` returns false for empty raw config, so dashboard MCP discovery does not start. |
| Skills | Temp `.no-bundled-skills` marker present. | Bundled skill seeding was skipped; `skills/` remained an empty temp residual directory. |
| Provider/model/catalog | No provider endpoint or model/catalog route was invoked. `model_catalog.enabled: false` was set in temp config. | Provider catalog/model code remains network-capable when operator routes are called. P11.8 did not call those routes. |
| Nous auth keepalive | `start_nous_auth_keepalive()` has a 60 second initial delay. | Total runtime was `28.192` seconds and temp `HERMES_HOME` contained no Nous auth state. |
| Browser/UI | `--no-open` and `serve` headless path. | No browser launch or SPA build. |

Runtime startup egress is treated as bounded for this lifecycle run only. This is not approval for provider/model/catalog/update routes, chat, dashboard UI actions, MCP, or long-lived Hermes service operation.

## 4. Path Containment

P11.8 used a fail-closed path containment helper before writing runtime config, markers, logs, and cleanup evidence.

Accepted contained write targets:

```text
C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_8-hermes\hermes-home\config.yaml
C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_8-hermes\hermes-home\.no-bundled-skills
C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_8-hermes\logs\hermes-serve-stdout.log
C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_8-hermes\logs\hermes-serve-stderr.log
C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_8-hermes\logs\hermes-stop-stdout.log
C:\Users\pablo\AppData\Local\Temp\agent-platform-p11_8-hermes\logs\hermes-stop-stderr.log
```

Contained pre-write rejection:

| Field | Value |
| --- | --- |
| Classification | `contained_boundary_rejection` |
| Rejected target | `C:\Users\pablo\config.yaml` |
| Cause | PowerShell variable-name collision with reserved `$HOME` during the first P11.8 config write attempt. |
| Guard result | Rejected before write with `out_of_root_target=C:\Users\pablo\config.yaml`. |
| Verification | `unexpected_config_exists=False`. |
| Credential/state exposure | None observed; no user Hermes state, `.env`, credential file, or provider config was read. |

This validates P11.7's fail-closed path containment requirement for the P11.8 writes performed here. It also preserves the limitation that any future automation must avoid reserved PowerShell variable names and must keep containment checks before every write.

## 5. Execution Evidence

### Install

The isolated venv was created under the temp root and Hermes was installed from the temp source copy with the approved web profile.

```text
venv_python: Python 3.12.3
install_command: python -m pip install --no-cache-dir --disable-pip-version-check ".[web]"
install_result: success
installed_package: hermes-agent-0.18.2
```

The install step downloaded Python dependencies from PyPI. That was package-install egress under the approved install profile, not Hermes runtime/provider/model execution.

### Preflight

```text
port9120_listener_count=0
hermes_dashboard_or_serve_process_count=0
console_entrypoint_exists=True
```

### Runtime Start

```text
runtime_command=hermes serve --host 127.0.0.1 --port 9120 --no-open --skip-build
runtime_pid=14280
started_at=2026-07-12T02:24:47.0567799+02:00
stdout=HERMES_BACKEND_READY port=9120
stderr=<empty>
runtime_budget_seconds=28.192
```

The backend-ready sentinel is printed only after `uvicorn.Server.startup()` binds the socket and the server reads the actual bound port. P11.8 therefore accepts the headless lifecycle startup as reached.

Limitation: the runtime was launched through the Windows `hermes.exe` console entrypoint. The parent launcher PID was not the long-lived server process owner, so the polling expression filtered by the launcher PID did not capture the live listener owner before stop. The sentinel and post-stop residual checks are retained as evidence; this record does not claim a separate successful `/api/status` probe.

No HTTP API route was called during the lifecycle run.

### Stop

```text
primary_stop_command=hermes serve --stop
primary_stop_exit_code=0
primary_stop_stdout=No hermes dashboard processes running.
primary_stop_effective=false
targeted_descendant_cleanup_used=true
targeted_descendant_pids=30036,8268,11416
runtime_exit_code=-1
listener_after_stop_count=0
runtime_process_exists_after_stop=0
post_run_hermes_dashboard_or_serve_process_count=0
```

Application-level graceful shutdown was not proven. The primary stop command did not find the console-entrypoint child process. P11.8 therefore accepts only the bounded targeted descendant cleanup as the demonstrated stop route for this lifecycle substrate gate.

## 6. Residual Inventory

Observed temp `HERMES_HOME` residuals before cleanup:

```text
.no-bundled-skills
config.yaml
SOUL.md
logs\agent.log
logs\gui.log
logs\.__agent.lock
logs\.__gui.lock
audio_cache\
cron\
hooks\
image_cache\
logs\curator\
memories\
pairing\
sessions\
skills\
```

Observed outer P11.8 evidence logs before cleanup:

```text
logs\hermes-serve-stdout.log
logs\hermes-serve-stderr.log
logs\hermes-stop-stdout.log
logs\hermes-stop-stderr.log
```

Observed workspace residuals:

```text
workspace_empty=true
```

Runtime logs captured safe metadata only:

```text
agent.log: HERMES_SAFE_MODE=1 - plugin discovery skipped
agent.log: Mounted plugin API routes: /api/plugins/hermes-achievements/
agent.log: Mounted plugin API routes: /api/plugins/kanban/
gui.log: Mounted plugin API routes: /api/plugins/hermes-achievements/
gui.log: Mounted plugin API routes: /api/plugins/kanban/
```

Cleanup result:

```text
temp_root_exists_after_cleanup=False
post_cleanup_port9120_listener_count=0
post_cleanup_hermes_dashboard_or_serve_process_count=0
```

## 7. Blocker Disposition

| Blocker | P11.8 disposition |
| --- | --- |
| `HERMES-P11.8-BLOCK-001` startup/provider/catalog/update egress | Contained for this lifecycle run only through safe mode, temp home, empty MCP config, skipped skill seeding, no provider/model/catalog/API route invocation, no chat, no browser, and runtime shorter than Nous keepalive initial delay. Not cleared for broader Hermes operation. |
| `HERMES-P11.8-BLOCK-002` graceful shutdown | App-level graceful shutdown not proven. Bounded targeted descendant cleanup was proven and accepted for this lifecycle substrate gate only. |
| `HERMES-P11.8-BLOCK-003` fail-closed path containment | Proven for P11.8 writes. One out-of-root target was rejected before write and absence was verified. Runtime residuals stayed under the temp root and the temp root was removed. |

## 8. Verdict

P11.8 verdict:

```text
hermes_lifecycle_substrate_exercised_once
hermes_lifecycle_substrate_accepted_with_limitations
```

Accepted facts:

```text
Hermes can be installed in an isolated temp venv from the locked source copy.
Hermes headless backend can reach its local ready sentinel on 127.0.0.1:9120.
Hermes can be bounded to temp HERMES_HOME and temp workspace for this lifecycle run.
Hermes safe mode suppresses general plugin discovery on this path.
Empty mcp_servers config prevents dashboard MCP startup on this path.
No provider/model/WorkPacket/agent execution occurred.
No product source, upstream source, Graphify output, .opencode, AGENTS.md, or Git state was modified.
Disposable runtime state was inventoried and removed.
```

Retained limitations:

```text
No adapter conformance was tested.
No WorkPacket was submitted.
No Hermes worker was run.
No model/provider route was activated.
No /api/status probe was claimed.
No app-level graceful stop was proven.
Primary hermes serve --stop did not find the Windows console-entrypoint child process.
Future runtime gates should launch with a process-owner strategy that lets stop/listener inventory target the long-lived child directly.
```

P11.8 authorizes no further Hermes runtime expansion by itself. Any later adapter, WorkPacket, worker, provider/model, MCP, dashboard UI, Kanban, cron, external messaging, or productionization gate must define a new exact execution profile and safety evidence.
