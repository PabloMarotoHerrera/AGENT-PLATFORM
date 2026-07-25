# P15.M10 - Docker Compose Local Pilot

Status: P15.M10 Docker Compose local pilot ready with constraints.

Final verdict: `hermes_0_19_docker_compose_local_pilot_ready_with_constraints`

## Ticket Authority

P15.M10 completes the local WSL2 plus Docker Compose pilot after two isolated
blockers were closed by dedicated continuation records.

First blocker:

```text
P15.M10-IMAGE-BUILD-BLOCKED
```

Cause: a TypeScript readonly consumer mismatch in `App.tsx` during the frontend
production build.

Resolution authority: P15.M10A and P15.M10AR.

Second blocker:

```text
P15.M10-LOOPBACK-PUBLICATION-BOUNDARY-BLOCKED
```

Cause: Docker Desktop did not materialize Windows host-port publication from the
Compose `internal: true` bridge network used by the blocked retry.

Resolution authority: P15.M10B.

The human P15.M10 continuation request explicitly authorized this bounded pilot.
No further interactive confirmation was requested.

P15.M10 now adopts exactly:

```text
one non-internal Compose bridge network
plus Windows loopback-only port publication
plus bounded runtime-only raw TCP loopback publication adapter
plus dashboard loopback bind
```

The verdict means Docker Desktop loopback publication worked through the
accepted topology, backend and browser UI readiness passed, the container
remained stable, shutdown and residue validation passed, and P15.M11 receives a
validated local runtime gate.

The verdict does not mean OAuth succeeded, real credentials exist, GPT-5.5
entitlement is verified, provider reachability is verified, inference succeeded,
complete local Pepper acceptance is closed, Desktop or Workspace is adopted, or
VPS deployment is authorized.

## Repository State

| Check | Result |
| --- | --- |
| Repository root | `<WINDOWS_REPOSITORY_ROOT>` |
| Branch | `p15.m-hermes-0.19-migration` |
| Starting HEAD | `5eef2423718663ab5b86a873616a4489faee35b0` |
| `origin/p15.m-hermes-0.19-migration` | `5eef2423718663ab5b86a873616a4489faee35b0` |
| HEAD equals branch remote | `true` |
| Index empty at start | `true` |
| Staged files at start | `0` |
| Tracked worktree clean at start | `true` |
| Visible untracked task candidates at start | `0` |
| P15.M10 governance record present at start | `false` |
| P15.M10 product changes at start | `0` |

Resolved P15.M10B commit:

| Field | Value |
| --- | --- |
| Commit | `5eef2423718663ab5b86a873616a4489faee35b0` |
| Commit message | `P15.M10B Assess Docker Desktop loopback publication` |
| Commit is ancestor of HEAD | `true` |
| HEAD equals P15.M10B commit | `true` |
| Post-P15.M10B commits | `0` |

P15.M10B authority:

| Field | Value |
| --- | --- |
| Verdict | `hermes_0_19_docker_desktop_loopback_port_publication_compatibility_assessed_with_constraints` |
| Classification | `Docker_Desktop_internal_network_host_publication_incompatibility` |
| Selected disposition | do not publish from an internal-only network |

## Required Prerequisites

| Record | Required verdict | State |
| --- | --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_migration_authorization.md` | `hermes_0_19_migration_authorized_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_workspace_adoption_assessment.md` | `hermes_0_19_workspace_adoption_assessment_ready_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_pepper_product_identity_post_commit_integrity_closure.md` | `hermes_0_19_pepper_product_identity_post_commit_integrity_closed_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_governed_runtime_adapter_post_commit_integrity_closure.md` | `hermes_0_19_governed_runtime_adapter_post_commit_integrity_closed_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closure.md` | `hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closed_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_wsl2_development_architecture.md` | `hermes_0_19_wsl2_development_architecture_ready_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repair.md` | `hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repaired_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_dashboard_readonly_plugin_manifest_build_post_commit_integrity_closure.md` | `hermes_0_19_dashboard_readonly_plugin_manifest_build_post_commit_integrity_closed_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_docker_desktop_loopback_port_publication_compatibility_assessment.md` | `hermes_0_19_docker_desktop_loopback_port_publication_compatibility_assessed_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |

## Prior Blockers

P15.M9 established the WSL2 development architecture with the verdict
`hermes_0_19_wsl2_development_architecture_ready_with_constraints`.

P15.M10 first stopped at image build time with:

```text
P15.M10-IMAGE-BUILD-BLOCKED
```

P15.M10A repaired the readonly plugin manifest compatibility issue by changing
three `App.tsx` helper parameter annotations from mutable `PluginManifest[]` to
`readonly PluginManifest[]`. It did not change runtime behavior.

P15.M10AR closed post-commit integrity for the P15.M10A repair and recorded the
current candidate, payload and baseline identities.

The retried P15.M10 image build then passed, but readiness stopped with:

```text
P15.M10-LOOPBACK-PUBLICATION-BOUNDARY-BLOCKED
```

P15.M10B proved this matrix:

| Case | Windows HTTP publication | Result |
| --- | --- | --- |
| Docker CLI default bridge | `127.0.0.1:19119` | passed |
| Compose bridge `internal: false` | `127.0.0.1:19119` | passed |
| Compose bridge `internal: true` | `127.0.0.1:19119` | failed |

P15.M10B rejected listener-enumeration false negative, general Docker host
publication failure and general Compose publication failure. The exact committed
classification consumed by this pilot is:

```text
Docker_Desktop_internal_network_host_publication_incompatibility
```

## Canonical Product Integrity

Windows and Linux canonical identities matched before runtime work and again

| Identity | Algorithm | Files | Bytes | SHA-256 |
| --- | --- | ---: | ---: | --- |
| Candidate | `agent-platform-git-tree-sha256-v2` | `6768` | `149234356` | `a71af0be624cb3f00b37d651248717c38f5bed18e460c6f159636c75a8875df3` |
| Payload | `agent-platform-git-tree-sha256-v2` | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | `sha256-git-blob-v1` | n/a | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Committed App identity:

| Field | Value |
| --- | --- |
| Path | `2_products/pepper-agent/web/src/App.tsx` |
| Bytes | `44709` |
| SHA-256 | `fcb51f78c1912f836cdc2bbf9db4483210db9f2ce30af7a882cfc8ba5f6b1fb2` |

Governance integrity suite:

| Location | Command | Result |
| --- | --- | --- |
| Windows checkout | `python -m unittest discover -s "12_tests/governance" -p "test_pepper_baseline_integrity.py"` | `Ran 14 tests`; `OK` |
| Linux checkout | `python3 -m unittest discover -s 12_tests/governance -p test_pepper_baseline_integrity.py` | `Ran 14 tests`; `OK` |

## Docker And WSL

Docker environment:

| Check | Result |
| --- | --- |
| Docker CLI | available |
| Docker client version | `29.4.1` |
| Docker server engine version | `29.4.1` |
| Docker Compose version | `v5.1.3` |
| Docker context | `desktop-linux` |
| Docker daemon | running |
| Docker engine OS | `linux` |
| Docker engine architecture | `x86_64` |

Resource collision gate:

| Check | Result |
| --- | ---: |
| Existing P15.M10 containers | `0` |
| Existing P15.M10 networks | `0` |
| Host `127.0.0.1:19119` listeners | `0` |
| Host `0.0.0.0:19119` listeners | `0` |

WSL and Linux checkout:

| Check | Result |
| --- | --- |
| Distribution | `Ubuntu`, reused/running for authorized pilot work |
| Linux checkout | `<PEPPER_SOURCE_ROOT>` |
| Filesystem | Linux-native |
| Under `/mnt` | `false` |
| Inside Windows cloud-sync path | `false` |
| Is Git repository | `true` |
| Origin matches Windows remote | `true` |
| Branch | `p15.m-hermes-0.19-migration` |
| Fast-forward sync | `990d153cd370f9f6289ff4ca61ff1a9f79e139dd` to `5eef2423718663ab5b86a873616a4489faee35b0` |
| HEAD equals Windows HEAD | `true` |
| HEAD equals origin branch | `true` |
| Index and tracked worktree clean | `true` |
| Unexpected untracked files | `0` |

Only the authorized WSL checkout synchronization commands were used: `git fetch
origin` and `git merge --ff-only origin/p15.m-hermes-0.19-migration`.

## Retained Image

| Field | Value |
| --- | --- |
| Tag | `pepper-agent:p15-m10-990d153cd370` |
| Image ID | `sha256:8e7d45adab5b5fa4b34a7c196929490521ac39d2d909e54d4866ddd772eebcfd` |
| Source commit | `990d153cd370f9f6289ff4ca61ff1a9f79e139dd` |
| Image OS | `linux` |
| Image architecture | `amd64` |
| Python path | `/opt/hermes/.venv/bin/python` |
| `hermes_cli` package | present |
| Product smoke | `pepper` |
| Image rebuilds | `0` |
| Image pulls | `0` |
| Image pushes | `0` |

The retained image remained reusable because P15.M10B changed governance only,
the current product identity and App identity remained unchanged, current HEAD is
a governance-only descendant of the image source commit, and the exact retained
image ID still matched.

## Runtime Root And Relay Adapter

Runtime evidence was created outside Git under:

```text
<PEPPER_RUNTIME_ROOT>/pilots/p15-m10-non-internal-publication-5eef24237186
```

Directory and file modes:

| Path kind | Mode |
| --- | --- |
| Pilot root | `0700` |
| `evidence` | `0700` |
| `logs` | `0700` |
| Runtime files | `0600` |

Relay adapter:

| Field | Value |
| --- | --- |
| Description | bounded runtime-only raw TCP loopback publication adapter |
| Path | `<PILOT_ROOT>/loopback_relay.py` |
| Bytes | `4191` |
| SHA-256 | `64daf4dfed3a585e6d67cadc9e40dec0e3c563275012ddc4dee814274813a228` |
| Interpreter | `/opt/hermes/.venv/bin/python` |
| Dashboard child command | `/opt/hermes/.venv/bin/python -m hermes_cli.main dashboard --host 127.0.0.1 --port 9120 --no-open --skip-build` |
| Relay listen | `0.0.0.0:9119` |
| Relay upstream | `127.0.0.1:9120` |
| Protocol | raw bidirectional TCP |
| Syntax validation | passed inside retained image as non-root runtime user |
| HTTP parsing | `false` |
| HTTP rewriting | `false` |
| Header logging | `false` |
| Body logging | `false` |
| Cookie logging | `false` |
| URL logging by relay | `false` |
| Auth authority | `false` |
| Provider authority | `false` |
| Credential authority | `false` |
| External dependencies | `0` |

The adapter launches exactly one dashboard child, waits for bounded direct TCP
readiness, binds one TCP listener, forwards bytes without parsing HTTP, supports
WebSocket upgrades transparently, logs lifecycle metadata only, handles SIGTERM,
terminates the dashboard child, and exits non-zero if the dashboard exits
unexpectedly.

## Corrected Publication Topology

Required topology validated by this pilot:

```text
Windows browser
127.0.0.1:19119
        |
        v
Docker Desktop host publication
127.0.0.1:19119 -> container 9119
        |
        v
bounded raw TCP relay
0.0.0.0:9119 -> 127.0.0.1:9120
        |
        v
Hermes dashboard
127.0.0.1:9120
```

Compose contract:

| Field | Value |
| --- | --- |
| Compose project | `pepper-p15m10` |
| Service | `pepper_dashboard` |
| Service count | `1` |
| Network key | `publication` |
| Runtime network name | `pepper-p15m10_publication` |
| Network driver | `bridge` |
| Network internal | `false` |
| Host network | `false` |
| Host bind | `127.0.0.1:19119` |
| Relay bind | `0.0.0.0:9119` |
| Dashboard bind | `127.0.0.1:9120` |
| Dashboard public bind | `false` |
| Host public exposure | `false` |
| LAN exposure | `false` |
| Internet exposure | `false` |
| Dashboard auth guard bypassed | `false` |
| Dashboard loopback policy preserved | `true` |

The non-internal network is used only because P15.M10B proved Docker Desktop
publication compatibility requires avoiding `internal: true` for this published
port. Network capability is not provider authority.

Pre-start Compose validation:

| Check | Result |
| --- | --- |
| `docker compose config --quiet` | passed |
| Runtime `compose.yaml` bytes | `1660` |
| Rendered Compose bytes | `1718` |
| Source contract `internal: false` | present |
| Rendered `internal: true` | absent |
| Published host IP | `127.0.0.1` |
| Published host port | `19119` |
| Container port | `9119` |
| Source checkout mounts | `0` |
| Docker socket mounts | `0` |
| Windows mounts | `0` |
| `.env` file created | `false` |
| Provider credential environment values | `0` |
| Host port `19119` free before start | `true` |

Docker publication materialization after container creation:

| Check | Result |
| --- | --- |
| `HostConfig.PortBindings` present | `true` |
| `NetworkSettings.Ports` publication present | `true` |
| `docker ps` mapping present | `true` |
| Mapping | `127.0.0.1:19119->9119/tcp` |
| Windows listener enumeration | `1` loopback listener, `0` wildcard listeners |
| Runtime network internal | `false` |

## Readiness

Bounded readiness passed on the first poll.

| Endpoint | Status | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Direct dashboard `http://127.0.0.1:9120/api/status` | `200` | `623` | `e5da370985238cb721a23f212c161c5f694ddad2e3f90275623158312d03cbe5` |
| Relayed `http://127.0.0.1:9119/api/status` | `200` | `623` | `e5da370985238cb721a23f212c161c5f694ddad2e3f90275623158312d03cbe5` |
| Windows host `http://127.0.0.1:19119/api/status` | `200` | `623` | `e5da370985238cb721a23f212c161c5f694ddad2e3f90275623158312d03cbe5` |

Readiness state:

| Check | Result |
| --- | --- |
| Dashboard/relay body match | `true` |
| Dashboard/host body match | `true` |
| Response length match | `true` |
| Container state | running |
| Container health | healthy |
| Relay process | running |
| Dashboard process | running |
| Restart count | `0` |

Dashboard bind validation:

| Listener | Result |
| --- | --- |
| Dashboard listener | `127.0.0.1:9120` |
| Relay listener | `0.0.0.0:9119` |
| Dashboard `0.0.0.0:9120` listener | `false` |
| Host `0.0.0.0:19119` listener | `false` |
| Host loopback reachability | `true` |

## Backend Acceptance

Host backend endpoint:

| Check | Result |
| --- | --- |
| Endpoint | `GET http://127.0.0.1:19119/api/status` |
| HTTP status | `200` |
| Response is JSON | `true` |
| Response size | `623` bytes |

Product configuration inside the container:

| Field | Value |
| --- | --- |
| Product ID | `pepper` |
| Product display name | `Pepper` |
| Product version | `0.1.0-dev` |
| Upstream version | `0.19.0` |
| Upstream commit | `3ef6bbd201263d354fd83ec55b3c306ded2eb72a` |
| Product UI | disabled via `agent_platform.product_ui` feature flag |
| Extension modules | `[]` |

No Pepper extension descriptors were enabled.

## Browser UI Acceptance

Root shell:

| Check | Result |
| --- | --- |
| Endpoint | `GET http://127.0.0.1:19119/` |
| HTTP status | `200` |
| HTML non-empty | `true` |
| HTML size | `721` bytes |
| Application root present | `true` |
| Blank or unstyled shell | `false` |

Asset metadata only was retained; bundles were not stored.

| Asset | Status | Content type | Bytes | SHA-256 |
| --- | ---: | --- | ---: | --- |
| `/assets/index-e15jtuxO.js` | `200` | `text/javascript; charset=utf-8` | `1994674` | `4721ffc61b5d4afaa0579011ddfb57ef95a63164c044f9772be01893469e75be` |
| `/assets/index-ZdPF3DBY.css` | `200` | `text/css; charset=utf-8` | `117800` | `7a97f3d3da6a4d924ea3c2d8d3470507236ad8ed5387f15be9ca1e6d9c546fe7` |

## Process Topology

Allowed process topology observed:

| Process class | Count |
| --- | ---: |
| Docker init | `1` |
| Loopback relay/supervisor | `1` |
| Hermes dashboard child | `1` |
| Provider processes | `0` |
| Worker processes | `0` |
| Agent worker processes | `0` |
| OAuth processes | `0` |
| Gateway processes | `0` |
| Vite dev or preview processes | `0` |

Forbidden process classes were absent: `gateway run`, provider worker, agent
worker, OAuth browser, Codex CLI, model-list process, usage process, MCP server,
tool worker, Vite dev server and Vite preview server.

## Container Security

| Check | Result |
| --- | --- |
| Configured user | `1000:1000` |
| Effective user is root | `false` |
| Relay user is root | `false` |
| Dashboard user is root | `false` |
| Privileged | `false` |
| Read-only root filesystem | `true` |
| Network mode is host | `false` |
| Docker socket mounted | `false` |
| Host PID namespace | `false` |
| Host IPC namespace | `false` |
| Capabilities | `cap-drop ALL` |
| `no-new-privileges` | `true` |
| Device mounts | `0` |
| GPU access | `false` |
| Restart policy | `no` |
| PIDs limit | `256` |
| Memory limit | `4294967296` bytes |
| CPU limit | `4.0` CPUs |

Mount inventory:

| Mount | Target | Access | Source boundary |
| --- | --- | --- | --- |
| Runtime home | `/opt/data` | writable bind | Linux-native runtime root |
| Relay script | `/opt/pilot/loopback_relay.py` | read-only bind | outside repository |

Forbidden mounts:

| Check | Result |
| --- | ---: |
| Source checkout mounts | `0` |
| Windows mounts | `0` |
| Docker socket mounts | `0` |
| Anonymous volumes | `0` |

Network inventory:

| Check | Result |
| --- | --- |
| Network | `pepper-p15m10_publication` |
| Driver | `bridge` |
| Internal | `false` |
| Services connected | `1` |
| Host bind | `127.0.0.1` |
| Public LAN exposure | `false` |
| Public Internet exposure | `false` |

## Environment And Provider Boundary

Compose-supplied environment present:

```text
HOME
HERMES_HOME
XDG_CACHE_HOME
XDG_STATE_HOME
TZ
PYTHONUNBUFFERED
PYTHONDONTWRITEBYTECODE
```

Forbidden environment variables absent:

```text
OPENAI_API_KEY
OPENAI_BASE_URL
HERMES_CODEX_BASE_URL
GITHUB_TOKEN
GH_TOKEN
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AZURE_CLIENT_SECRET
GOOGLE_APPLICATION_CREDENTIALS
SSH_AUTH_SOCK
API_SERVER_KEY
HERMES_DASHBOARD_OAUTH_CLIENT_ID
```

Environment boundary counters:

| Check | Result |
| --- | --- |
| Host environment dumped | `false` |
| Secret values logged | `false` |
| Caller endpoint override | `false` |
| Caller model override | `false` |

Provider and OAuth non-activity:

| Check | Result |
| --- | ---: |
| Credential mounts | `0` |
| Real credentials read | `0` |
| Real credentials written | `0` |
| Live OAuth attempts | `0` |
| Browser open attempts | `0` |
| Device code requests | `0` |
| Token exchange requests | `0` |
| Provider calls | `0` |
| Inference calls | `0` |
| Model list calls | `0` |
| Usage calls | `0` |
| Provider worker starts | `0` |
| Agent worker starts | `0` |
| Gateway starts | `0` |
| Auth JSON created | `false` |
| Provider credential store created | `false` |
| Credential lease created | `false` |

The non-internal network does not authorize provider egress, OAuth,
model-list calls, inference, credential access, arbitrary outbound traffic,
additional services or public exposure.

## Log Safety

Accepted-runtime relay and dashboard logs were bounded and scanned.

| Finding | Count |
| --- | ---: |
| Access tokens | `0` |
| Refresh tokens | `0` |
| Authorization headers | `0` |
| Cookies | `0` |
| Session tokens | `0` |
| OAuth device codes | `0` |
| Verification URLs | `0` |
| Account identifiers | `0` |
| Credential paths | `0` |
| Environment dumps | `0` |
| Raw provider responses | `0` |
| Reasoning traces | `0` |
| Real user prompts | `0` |
| Request bodies from relay | `0` |
| Response bodies from relay | `0` |
| HTTP headers from relay | `0` |
| Startup errors in accepted runtime | `0` |
| Unhandled tracebacks | `0` |
| Provider errors | `0` |
| Credential errors | `0` |
| Healthcheck failures after ready | `0` |

Relay lifecycle events retained:

```text
relay_event=dashboard_child_started
relay_event=direct_dashboard_tcp_ready
relay_event=relay_listening
relay_event=shutdown_requested
relay_event=dashboard_child_terminated
relay_event=relay_exit code=0
```

## Five-Minute Stability

Required stability window:

| Field | Value |
| --- | ---: |
| Configured duration | `300` seconds |
| Observed elapsed time including probe overhead | `308` seconds |
| Poll interval | `15` seconds |
| Expected poll count | `20` |
| Actual poll count | `20` |

Stability result:

| Check | Result |
| --- | ---: |
| Failed polls | `0` |
| Health failures | `0` |
| Status failures | `0` |
| Restart failures | `0` |
| Provider activity total | `0` |
| OAuth activity total | `0` |
| Worker activity total | `0` |

Each poll verified container running, container healthy, direct dashboard 200,
relay 200, Windows host 200, relay process alive, dashboard process alive,
restart count 0, provider activity 0, OAuth activity 0 and worker activity 0.

## Shutdown And Residue

Controlled shutdown:

| Check | Result |
| --- | --- |
| `docker compose stop --timeout 15` | passed |
| SIGTERM before SIGKILL | `true` |
| Relay graceful shutdown | `true` |
| Dashboard graceful shutdown | `true` |
| Forced kill required | `false` |
| Container exit clean | `true` |
| `docker compose down --remove-orphans --timeout 15` | passed |
| Volume deletions | `0` |
| Docker prune commands | `0` |
| Local image retained | `true` |
| Linux checkout retained | `true` |
| Prior evidence retained | `true` |
| Current evidence retained | `true` |

Residue validation:

| Check | Result |
| --- | ---: |
| P15.M10 containers | `0` |
| P15.M10 networks | `0` |
| Host port `19119` listeners | `0` |
| Relay processes | `0` |
| Dashboard processes | `0` |
| Provider processes | `0` |
| Worker processes | `0` |
| Agent processes | `0` |
| OAuth processes | `0` |
| Credential leases | `0` |
| Temporary auth stores | `0` |
| Runtime socket residue | `0` |
| Unexpected runtime files | `0` |
| Unexpected pilot directories | `0` |
| Bad runtime file modes | `0` |
| Credential-like runtime names | `0` |

Allowed retained state: clean Linux checkout, local Pepper pilot image, current
P15.M10 evidence, previous P15.M10 failure evidence, P15.M10B diagnostic
evidence, non-credential Hermes home content and bounded BuildKit cache.

## Runtime Evidence Manifest

Created outside Git:

```text
<PILOT_ROOT>/runtime-manifest.json
```

Manifest fields included schema version 1, ticket `P15.M10`, continuation after
`P15.M10B`, source HEAD, retained image tag and ID, publication classification,
network internal false, dashboard/relay/host binds, relay script SHA-256, relay
authority counters, backend/UI/stability status passed, provider calls 0, OAuth
attempts 0, credential operations 0, worker starts 0 and shutdown status
completed. The manifest does not include personal paths or secrets.

## Repository Integrity

No product, test or implementation path changed.

| Change class | Count |
| --- | ---: |
| Product changes | `0` |
| Test changes | `0` |
| Manifest changes | `0` |
| Lockfile changes | `0` |
| Dockerfile changes | `0` |
| Repository Compose changes | `0` |
| Runtime adapter changes | `0` |
| Provider implementation changes | `0` |
| Provider runtime changes | `0` |
| Provider worker changes | `0` |
| Product configuration changes | `0` |
| Web server changes | `0` |
| Frontend changes | `0` |
| Auth source changes | `0` |
| Credential pool changes | `0` |
| Codex transport changes | `0` |
| Workspace changes | `0` |
| Desktop changes | `0` |
| Dependency manifest changes | `0` |
| Graphify commands | `0` |
| Graphify changes | `0` |

Repository validation after this governance record was created is recorded in the
final validation section before handoff. The only intended Git candidate is this
governance record:

```text
0_architecture/governance/agent_platform_hermes_0_19_docker_compose_local_pilot.md
```

No modification-register row is required.

## Final Repository Validation

Final validation after governance record creation:

| Check | Result |
| --- | --- |
| `git diff --check` | clean |
| `git status --short` | exactly this untracked governance record |
| Candidate files | `1` |
| Unexpected candidates | `0` |
| Modified tracked files | `0` |
| Index empty | `true` |
| Staged files | `0` |
| Markdown trailing whitespace | `0` |
| Unexpected binary files | `0` |
| New executable files inside repository | `0` |
| `node_modules` candidate paths | `0` |
| `dist` candidate paths | `0` |
| `coverage` candidate paths | `0` |
| `__pycache__` candidate paths | `0` |
| `.pytest_cache` candidate paths | `0` |
| Governance tests | `Ran 14 tests`; `OK` |
| P15.M10 containers after validation | `0` |
| P15.M10 networks after validation | `0` |
| Port `19119` listeners after validation | `0` |

Canonical candidate and payload identities remained unchanged because the
governance utility hashes committed `HEAD` product blobs and this record is an
untracked governance candidate outside the Pepper product root.

## Residual Risks

| Risk | State |
| --- | --- |
| Live OAuth | not attempted |
| Real credentials | absent |
| GPT-5.5 entitlement | unverified |
| Provider reachability | unverified |
| Inference | not attempted |
| Complete local Pepper acceptance | not claimed |
| Desktop | disabled |
| Workspace | disabled |
| VPS deployment | unauthorized |

## P15.M11 Handoff

P15.M11 may begin only after P15.M10 is accepted, staged by the human, committed
and pushed.

P15.M11 prerequisites produced by this pilot:

| Field | Value |
| --- | --- |
| P15.M10 verdict | `hermes_0_19_docker_compose_local_pilot_ready_with_constraints` |
| Local runtime mode | WSL2 plus Docker Compose |
| Publication classification | `Docker_Desktop_internal_network_host_publication_incompatibility` |
| Publication network internal | `false` |
| Host bind | `127.0.0.1:19119` |
| Dashboard bind | `127.0.0.1:9120` |
| Relay bind | `0.0.0.0:9119` |
| Local image ID | `sha256:8e7d45adab5b5fa4b34a7c196929490521ac39d2d909e54d4866ddd772eebcfd` |
| Backend readiness | passed |
| UI acceptance | passed |
| Stability | passed |
| Shutdown | passed |
| Residue | zero |
| Real credentials configured | `false` |
| Live OAuth attempts | `0` |
| Provider calls | `0` |
| Inference calls | `0` |

P15.M11 remains the sole owner of first live OAuth, real credential acquisition,
token validation, GPT-5.5 entitlement validation, provider reachability, first
tool-free inference, cancellation, provider cleanup and credential rollback.

P15.M11 must explicitly account for the non-internal publication network and
must not treat it as provider authority.

## P15.M12 Boundary

| Field | Value |
| --- | --- |
| P15.M10 claims complete local acceptance | `false` |
| P15.M12 authority preserved | `true` |

P15.M12 remains responsible for complete end-to-end local Pepper acceptance.

## Final Verdict

```text
hermes_0_19_docker_compose_local_pilot_ready_with_constraints
```
