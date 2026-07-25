# P15.M10B - Docker Desktop Loopback Port Publication Compatibility Assessment

Status: P15.M10B Docker Desktop loopback port publication compatibility assessed with constraints.

Final verdict: `hermes_0_19_docker_desktop_loopback_port_publication_compatibility_assessed_with_constraints`

## Ticket Authority

P15.M10B is a diagnostic and governance-only continuation after the blocked
P15.M10 Docker Compose local pilot retry. It isolates the host-publication
failure that occurred after the retained Pepper image, dashboard process and
in-container relay had already become internally ready.

Accepted prior blocker:

```text
P15.M10-READINESS-BLOCKED
P15.M10-LOOPBACK-PUBLICATION-BOUNDARY-BLOCKED
```

Proven P15.M10 boundary:

```text
dashboard 127.0.0.1:9120
to raw TCP relay 0.0.0.0:9119
to both available inside container
```

Unproven P15.M10 boundary:

```text
Docker published port
to Windows 127.0.0.1:19119
```

P15.M10B used a non-Pepper static HTTP process from the already-retained local
image to classify whether the failure was general Docker Desktop publication,
general Compose publication, an `internal: true` network behavior, listener
enumeration unreliability, a transient condition or another bounded Docker
Desktop incompatibility.

No product source, tests, modification register, baseline JSON, Dockerfile,
repository Compose file, Docker Desktop setting, firewall rule, WSL networking
configuration, provider credential, OAuth flow, inference path, worker, agent,
gateway, Desktop or Workspace process was modified or started.

No image build, pull, push, Graphify run, staging operation, commit or push was
performed.

## Repository And Branch State

| Check | Result |
| --- | --- |
| Repository root | `<WINDOWS_REPOSITORY_ROOT>` |
| Branch | `p15.m-hermes-0.19-migration` |
| HEAD | `990d153cd370f9f6289ff4ca61ff1a9f79e139dd` |
| `origin/p15.m-hermes-0.19-migration` | `990d153cd370f9f6289ff4ca61ff1a9f79e139dd` |
| HEAD equals branch remote | `true` |
| Index empty at start | `true` |
| Staged files at start | `0` |
| Tracked worktree clean at start | `true` |
| Visible untracked task candidates at start | `0` |
| P15.M10 governance record present | `false` |

The P15.M10 governance record remained absent:

```text
0_architecture/governance/agent_platform_hermes_0_19_docker_compose_local_pilot.md
```

## Required Prerequisites

| Record | Required verdict | State |
| --- | --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_wsl2_development_architecture.md` | `hermes_0_19_wsl2_development_architecture_ready_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repair.md` | `hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repaired_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_dashboard_readonly_plugin_manifest_build_post_commit_integrity_closure.md` | `hermes_0_19_dashboard_readonly_plugin_manifest_build_post_commit_integrity_closed_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |

Canonical Pepper identity from `HEAD`:

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

## Prior P15.M10 Boundary Evidence

| Field | Value |
| --- | --- |
| Source commit | `990d153cd370f9f6289ff4ca61ff1a9f79e139dd` |
| Retained image tag | `pepper-agent:p15-m10-990d153cd370` |
| Retained image ID | `sha256:8e7d45adab5b5fa4b34a7c196929490521ac39d2d909e54d4866ddd772eebcfd` |
| Internal dashboard endpoint | `http://127.0.0.1:9120/api/status` |
| Internal dashboard result | `HTTP_200` |
| Internal relay endpoint | `http://127.0.0.1:9119/api/status` |
| Internal relay result | `HTTP_200` |
| Internal response bytes | `623` |
| Internal direct/relay SHA match | `true` |
| Requested host publication | `127.0.0.1:19119` |
| Docker `HostConfig.PortBindings` present | `true` |
| Windows host HTTP publication | unavailable |
| Windows listener enumeration | absent |
| Compose cleanup | completed |
| Remaining P15.M10 containers | `0` |
| Remaining P15.M10 networks | `0` |
| Remaining host port `19119` listeners | `0` |
| P15.M10 governance record | absent |
| Tracked repository changes | `0` |
| Provider or OAuth activity | `0` |

## Docker Environment

| Check | Result |
| --- | --- |
| Docker CLI | available |
| Docker client version | `29.4.1` |
| Docker server engine version | `29.4.1` |
| Docker Compose | available |
| Docker Compose version | `v5.1.3` |
| Docker context | `desktop-linux` |
| Docker daemon | running |
| Docker engine OS | `linux` |
| Docker engine architecture | `x86_64` |

Retained image gate:

| Check | Result |
| --- | --- |
| Required tag | `pepper-agent:p15-m10-990d153cd370` |
| Tag resolves to required image ID | `true` |
| Image ID | `sha256:8e7d45adab5b5fa4b34a7c196929490521ac39d2d909e54d4866ddd772eebcfd` |
| Image OS | `linux` |
| Image architecture | `amd64` |
| Python path | `/opt/hermes/.venv/bin/python` |
| Python path exists | `true` |
| Image default user | `root` |
| Image default volume declaration | `/opt/data` |
| Image rebuilds | `0` |
| Image pulls | `0` |
| Image pushes | `0` |

## Diagnostic Runtime

Diagnostic evidence was created outside Git under:

```text
<PEPPER_RUNTIME_ROOT>/pilots/p15-m10b-port-publication-990d153cd370
```

Directory modes:

| Directory | Mode |
| --- | --- |
| Diagnostic root | `0700` |
| `evidence` | `0700` |
| `logs` | `0700` |

Diagnostic files retained outside Git:

| File | Mode | Size bytes |
| --- | ---: | ---: |
| `default-bridge-result.json` | `0600` | `3868` |
| `compose-bridge.yaml` | `0600` | `592` |
| `compose-bridge.rendered.yaml` | `0600` | `685` |
| `compose-bridge-result.json` | `0600` | `4266` |
| `compose-internal.yaml` | `0600` | `593` |
| `compose-internal.rendered.yaml` | `0600` | `708` |
| `compose-internal-result.json` | `0600` | `3857` |
| `windows-probe-result.json` | `0600` | `4522` |
| `docker-inspect-result.json` | `0600` | `6953` |
| `matrix-result.json` | `0600` | `3651` |
| `cleanup-result.json` | `0600` | `696` |

All diagnostic files were bounded below 2 MiB. No complete HTTP bodies were
recorded.

Diagnostic process for every matrix case:

```text
/opt/hermes/.venv/bin/python -m http.server 9119 --bind 0.0.0.0
```

Diagnostic process properties:

| Property | Result |
| --- | ---: |
| Pepper dashboard started | `false` |
| Pepper product code imported | `false` |
| Provider code executed | `false` |
| OAuth code executed | `false` |
| Credential paths mounted | `0` |
| Source checkout mounted | `0` |
| Windows paths mounted | `0` |
| Docker socket mounted | `false` |
| External dependencies | `0` |

## Probe Authority

Authoritative host-publication probe:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:19119/" -TimeoutSec 5
```

Supplementary probes:

```powershell
Test-NetConnection -ComputerName 127.0.0.1 -Port 19119 -InformationLevel Detailed
Get-NetTCPConnection -LocalPort 19119 -State Listen -ErrorAction SilentlyContinue
netstat -ano
```

Interpretation rule: the Windows HTTP request is authoritative. Listener
enumeration and filtered `netstat` evidence are supplementary. A missing listener
entry must not override a successful Windows HTTP result.

## Case A - Docker CLI Default Bridge

Configuration:

| Field | Value |
| --- | --- |
| Container | `pepper-p15m10b-default` |
| Network | Docker default bridge |
| Image | `pepper-agent:p15-m10-990d153cd370` |
| Entrypoint | `/opt/hermes/.venv/bin/python` |
| Command | `-m http.server 9119 --bind 0.0.0.0` |
| Host publication | `127.0.0.1:19119:9119` |
| Read-only root | `true` |
| Capabilities | `cap-drop ALL` |
| `no-new-privileges` | `true` |
| PIDs limit | `64` |
| Memory limit | `256m` |
| CPUs | `1.0` |
| Restart policy | `no` |

Result:

| Evidence | Result |
| --- | --- |
| Container created | `true` |
| Internal readiness attempts | `1` |
| Container internal HTTP | `200` |
| Internal response bytes | `3612` |
| Internal response SHA-256 | `85edb9f747abcb083b736d355c9d59423bfd3667b1c9769ce298f9f138cc2fee` |
| Docker API `HostConfig.PortBindings` present | `true` |
| Docker API `NetworkSettings.Ports` present | `true` |
| `docker ps` port mapping present | `true` |
| Windows HTTP attempted | `true` |
| Windows HTTP status | `200` |
| Windows response bytes | `3612` |
| Windows response SHA-256 | `85edb9f747abcb083b736d355c9d59423bfd3667b1c9769ce298f9f138cc2fee` |
| Windows request duration | `22 ms` |
| `Test-NetConnection` TCP result | `true` |
| `Get-NetTCPConnection` listeners | `1` on `127.0.0.1` |
| Filtered `netstat` entries | `5` matching, `1` listening |
| Cleanup containers remaining | `0` |
| Cleanup host `19119` listeners | `0` |

Case A passed.

## Case B - Compose Non-Internal Bridge

Configuration:

| Field | Value |
| --- | --- |
| Compose project | `pepper-p15m10b-bridge` |
| Service | `probe` |
| Network driver | `bridge` |
| Network `internal` | `false` |
| Image | `pepper-agent:p15-m10-990d153cd370` |
| Pull policy | `never` |
| Entrypoint | `/opt/hermes/.venv/bin/python` |
| Command | `-m http.server 9119 --bind 0.0.0.0` |
| Host publication | `127.0.0.1:19119:9119` |
| Read-only root | `true` |
| Privileged | `false` |
| Capabilities | `cap-drop ALL` |
| `no-new-privileges` | `true` |
| PIDs limit | `64` |
| Memory limit | `256m` |
| CPUs | `1.0` |
| Restart policy | `no` |

Result:

| Evidence | Result |
| --- | --- |
| Compose config validation | passed |
| Container created | `true` |
| Network internal | `false` |
| Internal readiness attempts | `1` |
| Container internal HTTP | `200` |
| Internal response bytes | `3612` |
| Internal response SHA-256 | `85edb9f747abcb083b736d355c9d59423bfd3667b1c9769ce298f9f138cc2fee` |
| Docker API `HostConfig.PortBindings` present | `true` |
| Docker API `NetworkSettings.Ports` present | `true` |
| `docker ps` port mapping present | `true` |
| Windows HTTP attempted | `true` |
| Windows HTTP status | `200` |
| Windows response bytes | `3612` |
| Windows response SHA-256 | `85edb9f747abcb083b736d355c9d59423bfd3667b1c9769ce298f9f138cc2fee` |
| Windows request duration | `22 ms` |
| `Test-NetConnection` TCP result | `true` |
| `Get-NetTCPConnection` listeners | `1` on `127.0.0.1` |
| Filtered `netstat` entries | `3` matching, `1` listening |
| Cleanup containers remaining | `0` |
| Cleanup networks remaining | `0` |
| Cleanup host `19119` listeners | `0` |

Case B passed.

## Case C - Compose Internal Bridge

Configuration:

| Field | Value |
| --- | --- |
| Compose project | `pepper-p15m10b-internal` |
| Service | `probe` |
| Network driver | `bridge` |
| Network `internal` | `true` |
| Image | `pepper-agent:p15-m10-990d153cd370` |
| Pull policy | `never` |
| Entrypoint | `/opt/hermes/.venv/bin/python` |
| Command | `-m http.server 9119 --bind 0.0.0.0` |
| Host publication requested | `127.0.0.1:19119:9119` |
| Read-only root | `true` |
| Privileged | `false` |
| Capabilities | `cap-drop ALL` |
| `no-new-privileges` | `true` |
| PIDs limit | `64` |
| Memory limit | `256m` |
| CPUs | `1.0` |
| Restart policy | `no` |

Result:

| Evidence | Result |
| --- | --- |
| Compose config validation | passed |
| Container created | `true` |
| Network internal | `true` |
| Internal readiness attempts | `1` |
| Container internal HTTP | `200` |
| Internal response bytes | `3612` |
| Internal response SHA-256 | `85edb9f747abcb083b736d355c9d59423bfd3667b1c9769ce298f9f138cc2fee` |
| Docker API `HostConfig.PortBindings` present | `true` |
| Docker API `NetworkSettings.Ports` present | `false` |
| `docker ps` port mapping present | `false` |
| `docker ps` port text | `9119/tcp` |
| Windows HTTP attempted | `true` |
| Windows HTTP status | `0` |
| Windows response bytes | `0` |
| Windows request duration | `2055 ms` |
| Windows HTTP error class | `WebException` |
| `Test-NetConnection` TCP result | `false` |
| `Get-NetTCPConnection` listeners | `0` |
| Filtered `netstat` entries | `2` matching, `0` listening |
| Cleanup containers remaining | `0` |
| Cleanup networks remaining | `0` |
| Cleanup host `19119` listeners | `0` |

Case C failed only at the Docker Desktop host-publication boundary. The static
HTTP process remained internally ready inside the container.

## Matrix Classification

Exact classification:

```text
Docker_Desktop_internal_network_host_publication_incompatibility
```

Evidence mapping:

| Case | Windows HTTP | Internal HTTP | Network |
| --- | --- | --- | --- |
| A - Docker CLI default bridge | passed | passed | default bridge |
| B - Compose non-internal bridge | passed | passed | `internal: false` |
| C - Compose internal bridge | failed | passed | `internal: true` |

Rejected classifications:

| Classification | Reason rejected |
| --- | --- |
| `prior_probe_or_transient_failure` | Case C failed while Cases A and B passed in the same sequential matrix. |
| `Compose_port_publication_incompatibility` | Compose Case B passed with `internal: false`. |
| `Docker_Desktop_host_publication_environment_blocked` | Docker CLI Case A and Compose Case B both published to Windows loopback. |
| `listener_enumeration_false_negative` | No case had successful Windows HTTP with absent listener enumeration; Case C failed both HTTP and listener checks. |

Selected disposition:

```text
P15.M10 must not publish a host port directly from an internal-only network.
Select a bounded publication-adapter topology through a dedicated P15.M10
continuation contract. Do not weaken dashboard loopback binding.
```

P15.M10 continuation requirements:

| Requirement | State |
| --- | --- |
| P15.M10B must be accepted, committed and pushed before P15.M10 continues | required |
| P15.M10 continuation must consume this exact classification | required |
| Selected topology must derive only from the committed classification | required |
| Dashboard loopback binding may be weakened | `false` |
| OAuth, provider credentials or inference become authorized by P15.M10B | `false` |
| P15.M11 remains blocked until P15.M10 passes | `true` |
| P15.M11 remains owner of live OAuth and first inference | `true` |

## Security And Provider Boundary

Security posture across all cases:

| Check | Result |
| --- | --- |
| Effective user | `root`, exact retained image default |
| Privileged | `false` |
| Read-only root | `true` |
| Capabilities | `cap-drop ALL` |
| `no-new-privileges` | `true` |
| Docker socket mounted | `false` |
| Host network | `false` |
| Source mounts | `0` |
| Credential mounts | `0` |
| Windows mounts | `0` |
| Forbidden mounts detected | `0` |
| Windows host bind | `127.0.0.1` |
| Public Windows host bind | `false` |

Provider and credential boundary:

| Check | Result |
| --- | ---: |
| Credential mounts | `0` |
| Real credentials read | `0` |
| Real credentials written | `0` |
| OAuth attempts | `0` |
| Provider calls | `0` |
| Inference calls | `0` |
| Model list calls | `0` |
| Usage calls | `0` |
| Worker starts | `0` |
| Agent starts | `0` |
| Gateway starts | `0` |
| Real user prompts | `0` |

The non-internal bridge test did not authorize Pepper provider egress. No Pepper
runtime process was started.

## Cleanup Evidence

| Check | Result |
| --- | ---: |
| P15.M10 containers remaining | `0` |
| P15.M10 networks remaining | `0` |
| P15.M10B containers remaining | `0` |
| P15.M10B networks remaining | `0` |
| Host `127.0.0.1:19119` listeners after cleanup | `0` |
| Host `0.0.0.0:19119` listeners after cleanup | `0` |
| Compose diagnostic labeled volumes remaining | `0` |
| Volumes deleted | `0` |
| Images deleted | `0` |
| Docker prune commands | `0` |
| Unrelated containers modified | `0` |
| Unrelated images modified | `0` |
| Retained image still present | `true` |
| Docker settings mutated | `false` |
| Windows Firewall mutated | `false` |
| WSL networking mutated | `false` |

Diagnostic evidence remains outside Git for review. The retained Pepper pilot
image was preserved.

## Repository Integrity And Candidate Set

Created tracked candidate:

```text
0_architecture/governance/agent_platform_hermes_0_19_docker_desktop_loopback_port_publication_compatibility_assessment.md
```

Candidate constraints:

| Check | Result |
| --- | ---: |
| Candidate files | `1` |
| Unexpected candidates | `0` |
| Modified tracked files | `0` |
| Product files modified | `0` |
| Tests modified | `0` |
| Modification register modified | `false` |
| Baseline JSON modified | `false` |
| Dockerfile modified | `false` |
| Repository Compose modified | `false` |
| Package or lock changes | `0` |
| Graphify modified | `false` |
| Modification-register row required | `false` |

Validation commands:

| Command | Result |
| --- | --- |
| `git diff --check` | clean |
| `git status --short` | exactly this untracked governance record |
| Staged files after validation | `0` |
| Index empty after validation | `true` |
| `python -m unittest discover -s "12_tests/governance" -p "test_pepper_baseline_integrity.py"` | `Ran 14 tests`; `OK` |
| Canonical candidate identity | unchanged |
| Canonical payload identity | unchanged |

Git restrictions observed:

| Operation | Count |
| --- | ---: |
| `git add` | `0` |
| `git commit` | `0` |
| `git push` | `0` |
| `git stash` | `0` |
| `git reset` | `0` |
| `git clean` | `0` |
| `git worktree` | `0` |
| `git merge` | `0` |
| `git rebase` | `0` |

## Rollback

If P15.M10B is rejected before commit, remove only this uncommitted governance
record. Preserve the diagnostic evidence outside Git, the retained Pepper image
and the Linux checkout. Do not modify Docker Desktop settings, Windows Firewall,
WSL networking, product files, tests, baseline JSON or the modification register.

Rollback target:

| Check | Value |
| --- | --- |
| Repository clean after removing this record | `true` |
| P15.M10 image preserved | `true` |
| Linux checkout preserved | `true` |
| Docker settings mutated | `false` |
| Windows Firewall mutated | `false` |

## Final Verdict

```text
hermes_0_19_docker_desktop_loopback_port_publication_compatibility_assessed_with_constraints
```
