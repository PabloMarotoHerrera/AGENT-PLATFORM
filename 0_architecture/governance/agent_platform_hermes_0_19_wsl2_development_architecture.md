# P15.M9 - WSL2 Development Architecture

Status: P15.M9 WSL2 development architecture ready with constraints.

Final verdict: `hermes_0_19_wsl2_development_architecture_ready_with_constraints`

## Ticket Authority

P15.M9 defines the local development architecture for the Hermes Agent
0.19.0-derived Pepper product. P15.M9 converts the accepted deployment direction
into an exact architecture and future execution plan:

```text
Windows host
to WSL2 Linux development environment
to Linux-native repository and runtime storage
to Docker Compose local control-plane pilot
to Pepper P13 local UI
```

Strategic target: Mode C, WSL2 + Docker Compose.

Fallback target: Mode B, WSL2 Native.

Future deployment target: Mode D, external Linux VPS + Docker Compose.

P15.M9 is architecture and planning only. It did not mutate WSL, install or
update a distribution, move or clone the repository, create Linux runtime
directories, change Git configuration, start Docker Desktop, start or enable a
Docker daemon, pull or build images, run containers, run Compose, create volumes
or networks, install dependencies, create virtual environments, execute Pepper,
start the dashboard, start a provider worker, run OAuth, read or write
credentials, call providers, run inference, modify product code, modify
manifests or lockfiles, modify the modification register, modify the baseline
JSON, run Graphify, stage, commit or push.

The verdict means the architecture is defined, the future command plan is
bounded, WSL2 and Docker readiness are classified, and P15.M10 may be planned
after human approval. It does not mean a Linux-native checkout exists, Docker is
running, images have been built, Compose has started, Pepper runs under WSL2,
OAuth works, GPT-5.5 is reachable or local acceptance is complete.

## Repository And Branch State

| Check | Result |
| --- | --- |
| Repository root | `<WINDOWS_REPOSITORY_ROOT>` |
| Branch | `p15.m-hermes-0.19-migration` |
| HEAD | `f0db7ef2011aa68910dbcf8d839db66e1ff832c2` |
| `origin/p15.m-hermes-0.19-migration` | `f0db7ef2011aa68910dbcf8d839db66e1ff832c2` |
| HEAD equals branch remote | `true` |
| Index empty at start | `true` |
| Staged files at start | `0` |
| Tracked worktree clean at start | `true` |
| Visible untracked task candidates at start | `0` |

P15.M8R was accepted, committed and pushed before P15.M9 began. The committed
P15.M8R verdict is
`hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closed_with_constraints`.

## Committed Prerequisites

| Record | Required verdict | State |
| --- | --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_migration_authorization.md` | `hermes_0_19_migration_authorized_with_constraints` | tracked, committed in HEAD, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_workspace_adoption_assessment.md` | `hermes_0_19_workspace_adoption_assessment_ready_with_constraints` | tracked, committed in HEAD, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_pepper_product_identity_post_commit_integrity_closure.md` | `hermes_0_19_pepper_product_identity_post_commit_integrity_closed_with_constraints` | tracked, committed in HEAD, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_governed_runtime_adapter_post_commit_integrity_closure.md` | `hermes_0_19_governed_runtime_adapter_post_commit_integrity_closed_with_constraints` | tracked, committed in HEAD, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closure.md` | `hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closed_with_constraints` | tracked, committed in HEAD, locally unmodified, unstaged |

Required product state:

| Field | Value |
| --- | --- |
| Product ID | `pepper` |
| Product version | `0.1.0-dev` |
| Upstream version | `0.19.0` |
| Upstream commit | `3ef6bbd201263d354fd83ec55b3c306ded2eb72a` |
| Product UI | `disabled` |
| Extension modules | `0` |

Required provider state:

| Field | Value |
| --- | --- |
| Provider | `openai-codex` |
| Authentication | `chatgpt_oauth` |
| Model | `gpt-5.5` |
| Provider profile | `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1` |
| Worker profile | `worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1` |
| Real credentials configured | `false` |
| Live OAuth attempts | `0` |
| Provider calls | `0` |
| Inference calls | `0` |

## Canonical Pepper Identity

Canonical command:

```powershell
python "10_scripts/governance/pepper_baseline_integrity.py" --repo-root "." --product-root "2_products/pepper-agent" --mode all --format json
```

| Identity | Algorithm | Files | Bytes | SHA-256 |
| --- | --- | ---: | ---: | --- |
| Candidate | `agent-platform-git-tree-sha256-v2` | `6768` | `149234329` | `f0dceedbe9ae1b6b0738c00b0d643678d8bc5acd2b9766729f7adcb238c08e59` |
| Payload | `agent-platform-git-tree-sha256-v2` | `6681` | `145409765` | `56a538886ac9cc98050be853f173e631e8f568495a6c5aeef27a2128981524e7` |
| Baseline record | `sha256-git-blob-v1` | not applicable | `34254` | `478f1cd5279806e808b562193a993f391f98a4e8513ef4ee8d41e35a0d7c4dda` |

Governance integrity tests:

| Command | Result |
| --- | --- |
| `python -m unittest discover -s "12_tests/governance" -p "test_pepper_baseline_integrity.py"` | `Ran 14 tests`; `OK` |

P15.M9 did not update the baseline JSON.

## Read-Only Host Inspection

Allowed Windows-side commands executed with bounded timeouts:

| Command | Sanitized result |
| --- | --- |
| `wsl.exe --status` | WSL command available; default distribution `Ubuntu`; default version `2` |
| `wsl.exe --version` | WSL version `2.6.1.0`; kernel version `6.6.87.2-1` |
| `wsl.exe --list --verbose` | `Ubuntu` installed as WSL version `2`, currently stopped; `docker-desktop` observed stopped as WSL version `2` |
| `docker version` | Windows Docker CLI `29.4.1` available; daemon connection failed because Docker Desktop engine pipe was not present/running |
| `docker compose version` | Docker Compose `v5.1.3` available |
| `docker context show` | Docker context `desktop-linux` |
| `docker context inspect` | Context inspect succeeded; personal filesystem paths and analytics endpoint details redacted from this record |

Selected-distribution shell inspection was not executed because the selected WSL2
distribution was stopped. Running `wsl.exe -d Ubuntu -- sh -lc ...` would start
the distribution and violate the P15.M9 no-WSL-mutation boundary.

Required command-boundary results:

| Field | Value |
| --- | ---: |
| Indefinite waits | `0` |
| Polling loops | `0` |
| Host mutations | `0` |
| WSL mutations | `0` |
| Docker mutations | `0` |
| Credential inspections | `0` |

No Windows username, Linux username, hostname, IP address, credential path,
machine identifier or secret is recorded.

## Host Readiness Classification

| HostCapability field | Classification | Evidence |
| --- | --- | --- |
| `WSL_command_available` | `available` | `wsl.exe --status` and `wsl.exe --version` returned successfully |
| `WSL_version` | `available` | `2.6.1.0` |
| `selected_distribution` | `available` | `Ubuntu` |
| `selected_distribution_state` | `installed_not_running` | `wsl.exe --list --verbose` reported stopped |
| `selected_distribution_WSL_version` | `available` | `2` |
| `Linux_kernel` | `available` | WSL kernel `6.6.87.2-1` from `wsl.exe --version`; selected distro `uname` not run |
| `Linux_distribution` | `not_inspected` | distro shell inspection skipped to avoid starting WSL |
| `Linux_home_filesystem` | `not_inspected` | distro shell inspection skipped to avoid starting WSL |
| `Docker_CLI_Windows` | `available` | Docker CLI `29.4.1` |
| `Docker_Compose_Windows` | `available` | Docker Compose `v5.1.3` |
| `Docker_context` | `available` | `desktop-linux` |
| `Docker_daemon_Windows` | `installed_not_running` | daemon pipe unavailable; Docker Desktop engine not running |
| `Docker_CLI_WSL` | `not_inspected` | WSL shell inspection skipped |
| `Docker_Compose_WSL` | `not_inspected` | WSL shell inspection skipped |
| `Docker_daemon_WSL` | `not_inspected` | WSL shell inspection skipped |

Architecture-ready is distinct from runtime-ready:

| Field | Value |
| --- | --- |
| `architecture_ready` | `true_with_constraints` |
| `runtime_ready` | `false` |
| `strategic_mode_C_operational_now` | `false` |
| `fallback_mode_B_architecturally_available` | `true` |

WSL2 foundation is viable because WSL2 is installed and a WSL2 distribution is
available. Runtime readiness is false because the selected distribution is not
running, selected-distro Linux details were not inspected, and the Docker daemon
is not running.

## Responsibility Boundary

Windows host owns:

| Responsibility |
| --- |
| Human terminal and editor |
| Human browser |
| Windows desktop integration |
| WSL lifecycle controlled by the human |
| Docker Desktop lifecycle controlled by the human when used |
| Manual approval |
| Manual Git staging, commit and push |

WSL2 owns:

| Responsibility |
| --- |
| Linux-native Pepper source checkout |
| Linux Python and Node execution |
| Docker CLI and Compose execution |
| Runtime filesystem |
| Logs |
| Artifacts |
| Temporary workspaces |
| Future governed credential root |
| Local service networking |
| Process lifecycle |

Containers own:

| Responsibility |
| --- |
| Bounded service processes |
| Service-local temporary files |
| Service-local dependency runtime |
| Internal networking |
| Healthchecks |
| Stdout and stderr |

Git remote owns:

| Responsibility |
| --- |
| Canonical source publication |
| Branch identity |
| Commit identity |
| Cross-host source synchronization |

Required prohibitions:

| Boundary | Posture |
| --- | --- |
| Windows OneDrive checkout as Linux runtime source | prohibited |
| `/mnt/c` source execution | prohibited |
| Shared writable Windows source mount | prohibited |
| Container mutation of canonical Git source | prohibited |
| Unmanaged source synchronization | prohibited |

## Linux-Native Repository Placement

Future logical source root:

```text
<PEPPER_SOURCE_ROOT> = <WSL_HOME>/src/pepper/agent-platform
```

The exact expanded path must be selected during P15.M10 or a dedicated preflight
and was not created by P15.M9.

Required source-root properties:

| Property | Value |
| --- | --- |
| Inside WSL Linux filesystem | `true` |
| Under `/mnt/c` | `false` |
| Under `/mnt/d` | `false` |
| Inside OneDrive | `false` |
| Inside Docker volume | `false` |
| Shared writable with Windows checkout | `false` |
| Filesystem | `Linux_native` |
| Canonical source | `Git_remote` |
| Checkout type | `independent_clean_clone_or_worktree_from_canonical_remote` |

Future acquisition sequence:

```text
Git clone or exact Git-native reconstruction
branch checkout
exact commit verification
clean status verification
```

Recursive copy from `/mnt/c` is prohibited.

## Git And Line-Ending Policy

Future Linux checkout policy:

| Setting | Required value |
| --- | --- |
| `core.autocrlf` | `false` |
| `core.eol` | `lf` |
| Filemode | preserved |
| Symlinks | Linux semantics |
| Repository encoding | UTF-8 |
| Canonical content authority | exact Git blob bytes |

P15.M9 defined but did not change Git configuration.

Future validation:

| Check | Required value |
| --- | --- |
| Branch | `p15.m-hermes-0.19-migration_or_future_promoted_branch` |
| HEAD equals expected remote | `true` |
| Index empty | `true` |
| Tracked worktree clean | `true` |
| Unexpected untracked files | `0` |

Windows working-tree CRLF normalization must not become Linux source authority.

## Runtime Filesystem Architecture

Future logical runtime root:

```text
<PEPPER_RUNTIME_ROOT> = <WSL_HOME>/.local/share/pepper
```

Logical subroots:

| Root | Purpose |
| --- | --- |
| `<PEPPER_RUNTIME_ROOT>/state` | Durable local service state |
| `<PEPPER_RUNTIME_ROOT>/artifacts` | Manifested local artifacts |
| `<PEPPER_RUNTIME_ROOT>/logs` | Bounded logs |
| `<PEPPER_RUNTIME_ROOT>/workspaces` | Runtime workspaces |
| `<PEPPER_RUNTIME_ROOT>/run` | Runtime sockets and transient run state |
| `<PEPPER_RUNTIME_ROOT>/hermes-home` | Future logical `HERMES_HOME` |
| `<WSL_HOME>/.cache/pepper` | Cache root |

Required separation:

| Boundary | Value |
| --- | --- |
| Runtime data inside repository | `false` |
| Credentials inside repository | `false` |
| Logs inside repository | `false` |
| Generated artifacts inside source | `false` |
| Durable data under `/tmp` | `false` |
| Shared writable source and runtime root | `false` |

Future directory modes:

| Path class | Mode |
| --- | --- |
| Runtime root | `0700` |
| Credential parent directories | `0700` |
| Credential files | `0600` |

P15.M9 did not create these directories.

## Hermes Home And Credential Placement

Future logical runtime home:

```text
HERMES_HOME = <PEPPER_RUNTIME_ROOT>/hermes-home
```

The P15.M8 credential store would resolve internally beneath:

```text
<HERMES_HOME>/agent-platform/provider-credentials/openai-codex.primary
```

This is a logical architecture description only.

| Boundary | Value |
| --- | --- |
| Real store created | `false` |
| Real credentials configured | `false` |
| OAuth executed | `false` |
| Credential path exposed to UI | `false` |
| Credential path exposed to callers | `false` |
| Credential values in Compose environment | `false` |
| Credential values in `.env` | `false` |
| Credential values in repository | `false` |

Future credential rules:

| Rule |
| --- |
| Credentials are created only by the P15.M11 governed OAuth flow |
| A provider credential is not a worker identity |
| Services do not share a broadly writable `HERMES_HOME` |
| Workers receive only bounded lease projections |
| No permanent provider token is copied into an image |
| No token is passed as a Compose command-line argument |
| No credential value appears in logs or healthchecks |

## Local Service Topology

Minimum P15.M10 logical topology:

```text
Pepper P13 UI
to local Pepper backend/gateway
to provider-null runtime profile
```

P15.M10 minimum services:

| Service | Required | Enabled | Role |
| --- | --- | --- | --- |
| `pepper_backend` | `true` | `true` | Governed headless backend and API |
| `pepper_ui` | `true` | `true` | Pepper P13 browser UI |
| `provider_worker` | `false` | `false` | Disabled until P15.M11 or later authority |
| `OAuth_service` | `false` | `false` | Disabled until P15.M11 |
| `agent_worker` | `false` | `false` | Disabled |
| `Workspace` | `false` | `false` | Disabled |
| `Desktop` | `false` | `false` | Disabled |

P15.M10 must not include a live provider worker. P15.M11 owns the first

## Container Security Posture

Required future P15.M10 posture where compatible:

| Control | Required posture |
| --- | --- |
| Run as non-root | `true` |
| Privileged | `false` |
| Host network | `false` |
| Docker socket mount | `false` |
| Host PID namespace | `false` |
| Host IPC namespace | `false` |
| Additional capabilities | `none` |
| `cap_drop` | `all` |
| `no_new_privileges` | `true` |
| Read-only root filesystem | preferred and required when compatible |
| Temporary filesystem | bounded tmpfs when compatible |
| Device mounts | `none` |
| GPU access | `none` |
| Container restart policy | no automatic infinite restart during pilot |

Any exception must be explicitly identified, justified, reviewed, bounded to one
service and recorded in P15.M10 evidence.

## Build And Image Policy

P15.M9 did not build or pull images.

P15.M10 must require:

| Policy | Required posture |
| --- | --- |
| Base image | exact tag and digest or exact source build authority |
| Mutable `latest` tag | prohibited |
| Unreviewed remote image | prohibited |
| Image build context | Linux-native source root |
| Credentials in build args | prohibited |
| Credentials in layers | prohibited |
| Source repository write from build | prohibited |
| SBOM or dependency inventory | required when supported |
| License notices | preserved |
| Public image publication | not authorized |

## Compose Network Policy

Required future topology: one private internal Compose network.

Host exposure:

| Service class | Exposure |
| --- | --- |
| Pepper UI | loopback only |
| Pepper backend | loopback only or internal only |
| Provider worker | no host port |
| Database or state service | internal only |
| Debug ports | disabled by default |

Required network prohibitions:

| Boundary | Value |
| --- | --- |
| `0.0.0.0` bindings | `0_unless_explicitly_reviewed` |
| Public LAN exposure | `false` |
| Public Internet exposure | `false` |
| Host network mode | `false` |
| Automatic UPnP | `false` |

Exact host ports must be selected and recorded by P15.M10. P15.M9 did not
reserve or open ports.

## Provider Egress Policy

P15.M9 and P15.M10 do not authorize provider access.

Required before P15.M11:

| Boundary | Value |
| --- | ---: |
| OpenAI Codex inference egress | `disabled_or_unused` |
| OAuth egress | `disabled_or_unused` |
| Model-list calls | `0` |
| Provider calls | `0` |
| Inference calls | `0` |

Dependency acquisition egress is distinct from provider runtime egress. P15.M10
may require approved dependency or image acquisition egress, but that does not
grant provider authority.

## Volume Architecture

Future volume classes:

| Class | Policy |
| --- | --- |
| Source | Linux-native source checkout; read-only to runtime services where practical; never broadly shared writable |
| Runtime state | Service-owned, outside repository, explicitly named, bounded, backed up or disposable by class |
| Logs | Bounded, rotated, secret-filtered, outside repository |
| Artifacts | Manifested, checksummed, outside repository, no implicit promotion into source |
| Credentials | Outside repository, not generic shared volume, read/write only by credential owner, projected to worker by bounded lease |

Required prohibitions:

| Boundary | Posture |
| --- | --- |
| Anonymous untracked volumes | prohibited |
| Shared writable repository volume | prohibited |
| Docker socket volume | prohibited |
| Host root mount | prohibited |
| Windows OneDrive mount | prohibited |
| Credential volume shared by all services | prohibited |

## Environment Policy

Compose environment must use an explicit allowlist.

Allowed categories:

| Category |
| --- |
| Runtime identity |
| Product identity |
| Bounded internal service URLs |
| Logging level |
| Timezone |
| Non-secret feature flags |
| Internal ports |
| `HERMES_HOME` logical root |

Prohibited environment inheritance:

| Prohibited source |
| --- |
| `OPENAI_API_KEY` |
| `OPENAI_BASE_URL` |
| `HERMES_CODEX_BASE_URL` |
| Git credentials |
| GitHub tokens |
| Cloud credentials |
| SSH agent sockets |
| Windows environment wholesale |
| Host proxy credentials |
| Arbitrary `PATH` injection |
| Caller-selected endpoint |
| Caller-selected model |

Required posture:

| Boundary | Value |
| --- | --- |
| Environment pass-through | allowlist only |
| Host environment dump | prohibited |
| Secrets in environment evidence | prohibited |
| Container timezone | `TZ=UTC` unless a service-specific display exception is approved |
| Operational timestamps | UTC |

Endpoint and model override denial remains part of the P15.M8 provider-runtime
and bounded worker profile.

## Healthcheck And Readiness Architecture

Future backend healthcheck:

| Evidence |
| --- |
| HTTP response from the accepted Pepper status endpoint |
| Expected status code |
| Bounded response body |
| Product identity equals `pepper` |
| Product UI posture preserved |

Future UI healthcheck:

| Evidence |
| --- |
| HTTP 200 from the root page |
| Main JavaScript asset retrievable |
| Main stylesheet asset retrievable when applicable |
| No blank unstyled shell |

Required polling:

| Field | Value |
| --- | --- |
| Interval | approximately 1 second |
| Maximum total wait | bounded, 60 seconds or less |
| Infinite wait | `false` |
| Process exit wait | not used for long-running readiness |

A long-running server is considered ready by health evidence, not by process
termination. Historical unbounded loopback waiting loops are prohibited without
bounded timeout and stdout/stderr inspection.

## Process Ownership And Shutdown

P15.M10 must preserve P15.M7 process authority.

| Control | Required posture |
| --- | --- |
| Compose project name | explicit |
| Service identity | explicit |
| Process tree ownership | bounded |
| Startup timeout | bounded |
| Shutdown timeout | bounded |
| SIGTERM before SIGKILL | `true` |
| Orphan containers | prohibited |
| Unowned background processes | prohibited |
| Restart forever during pilot | prohibited |

Default pilot shutdown:

```text
docker compose stop
bounded wait
```

Prohibited default rollback:

```text
docker compose down -v
```

Volume deletion requires separate human approval.

## Logging And Diagnostics

Required future service evidence:

| Evidence |
| --- |
| Startup timestamp |
| Service identity |
| Image identity |
| Configuration digest |
| Healthcheck result |
| Bounded stdout |
| Bounded stderr |
| Exit status when stopped |
| Shutdown result |
| Residue result |

Logs must not contain:

| Prohibited log content |
| --- |
| Access tokens |
| Refresh tokens |
| Authorization headers |
| OAuth device codes |
| Verification URLs after completion |
| Credential paths |
| Environment dumps |
| Account identifiers |

Required log policy:

| Field | Value |
| --- | --- |
| Rotation | enabled |
| Maximum size | bounded |
| Retention | bounded |
| Raw provider response | prohibited |
| Reasoning trace | prohibited |

## Artifact And Source Movement Policy

Canonical source moves through Git only:

```text
Windows checkout: no recursive copy into WSL
Git remote: Linux-native clean checkout
Runtime output: artifact manifest plus checksum
Artifact promotion into source: explicit ticket and review
```

Required artifact controls:

| Control | Value |
| --- | --- |
| Manifest | required |
| SHA-256 | required |
| Source path | normalized |
| Destination path | normalized |
| Maximum size | bounded |
| Unexpected files | rejected |
| Automatic source write | `false` |

No unmanaged shared writable source volume is allowed between Pepper and future
Siamese workers.

## WSL2 Native Fallback Architecture

Fallback Mode B uses the same Linux-native source root, runtime root,
`HERMES_HOME`, credential boundary, provider profile, worker profile,
environment allowlist, loopback-only networking, readiness checks, logging,
shutdown and residue validation.

Fallback differences:

| Field | Value |
| --- | --- |
| Container runtime | absent |
| Python runtime | WSL-local virtual environment |
| Node runtime | WSL-local toolchain |
| Process owner | `P15_M7_runtime_adapter` |
| Service network | WSL loopback |
| Dependency installation | separately approved and lock-governed |

Mode B may be selected when the Docker daemon is unavailable, Compose hardening
is incomplete, image pinning is incomplete, volume boundaries are incomplete or
secret boundaries are incomplete. Fallback selection must be explicit and
recorded. P15.M9 did not create a fallback virtual environment and performed no
fallback execution.

## Windows Native Emergency Posture

Windows Native is not the strategic local runtime. It may remain only for source
editing, read-only emergency inspection, bounded compatibility evidence and the
human browser/desktop host.

| Boundary | Posture |
| --- | --- |
| Windows native provider execution | not selected |
| Windows native OAuth | not selected by P15.M9 |
| Windows native worker | not selected |
| P15.1A evidence | retained only |

P15.M9 did not resume P15.1A.

## P15.M10 Future Command Plan

P15.M9 records this future command plan but does not execute it:

1. Human pilot approval.
2. Revalidate P15.M9 committed authority.
3. Revalidate WSL2 distribution and filesystem.
4. Revalidate Docker CLI, Compose and daemon.
5. Select the exact Linux-native source root.
6. Acquire an exact clean Git checkout.
7. Verify branch, HEAD, remote and clean state.
8. Apply approved Linux checkout Git settings.
9. Create runtime roots with approved permissions.
10. Validate Compose files before execution.
11. Validate image identities and build inputs.
12. Validate volume, network and secret boundaries.
13. Start only backend and Pepper P13 UI.
14. Run bounded readiness checks.
15. Verify provider, OAuth and worker activity remains zero.
16. Capture bounded logs and service evidence.
17. Stop services cleanly.
18. Verify no containers, listeners or process residue.
19. Preserve approved state volumes unless rollback authorizes deletion.
20. Record pilot verdict and rollback evidence.

No stage may run automatically from P15.M9.

## P15.M10 Unlock Gate

P15.M10 remains blocked until:

| Gate | Required value |
| --- | --- |
| `P15_M9_committed` | `true` |
| `P15_M9_pushed` | `true` |
| Architecture verdict | `hermes_0_19_wsl2_development_architecture_ready_with_constraints` |
| Human pilot approval | explicit |
| WSL2 distribution | available and version 2 |
| Linux-native source path | selected |
| Linux-native runtime path | selected |
| Docker daemon | ready or explicit Mode B fallback selected |
| Compose files | reviewed before start |
| Image identity | pinned or source build exact |
| Volume policy | accepted |
| Secret policy | accepted |
| Network policy | accepted |
| Healthchecks | bounded |
| Shutdown plan | accepted |
| Rollback plan | accepted |

P15.M10 must stop before runtime startup if any gate is absent.

## P15.M11 Boundary

P15.M11 remains sole owner of first live OAuth, real credential acquisition,
real token metadata validation, provider reachability, GPT-5.5 entitlement
validation, first tool-free inference, live cancellation, live provider shutdown
and live credential rollback evidence.

Required before P15.M11:

| Gate | Value |
| --- | --- |
| Approved local runtime gate | `true` |
| P15.M9 architecture | committed |
| P15.M10 Compose pilot or approved Mode B gate | accepted |

P15.M9 preserved:

| Boundary | Value |
| --- | --- |
| Live OAuth attempts | `0` |
| Real credentials configured | `false` |
| Provider calls | `0` |
| Inference calls | `0` |
| P15.M11 authority preserved | `true` |

Provider reachability and GPT-5.5 entitlement remain unverified.

## Rollback And Rejection

If P15.M9 is rejected, remove only the uncommitted P15.M9 governance record. Do
not revert P15.M8 or P15.M8R, alter WSL, alter Docker, remove distributions,
change Git configuration, inspect credentials or modify product code.

Required post-rollback state:

| Boundary | Value |
| --- | --- |
| Tracked product matches HEAD | `true` |
| Candidate files | `0` |
| WSL mutations | `0` |
| Docker mutations | `0` |
| Credential operations | `0` |

## Candidate Set

| Check | Result |
| --- | --- |
| Created candidate | `0_architecture/governance/agent_platform_hermes_0_19_wsl2_development_architecture.md` |
| Candidate files | `1` |
| Unexpected candidates | `0` |
| Product files modified | `0` |
| Tests modified | `0` |
| Modification register modified | `false` |
| Baseline JSON modified | `false` |
| Application manifests modified | `0` |
| Package manifests modified | `0` |
| Lockfiles modified | `0` |
| WSL state modified | `false` |
| Docker state modified | `false` |
| Git configuration modified | `false` |
| Graphify modified | `false` |

No modification-register row is required because P15.M9 creates no product file.

## Validation And Hygiene

Required repository validation:

| Check | Result |
| --- | --- |
| `git diff --check` | clean |
| Candidate files | `1` |
| Unexpected candidates | `0` |
| Index empty | `true` |
| Staged files | `0` |

Required governance-content checks:

| Check | Result |
| --- | --- |
| Strategic Mode C | present |
| Fallback Mode B | present |
| Future Mode D | present |
| Linux-native repository | required |
| Linux-native runtime storage | required |
| `/mnt/c` runtime | prohibited |
| OneDrive runtime | prohibited |
| Provider worker enabled | `false` |
| OAuth enabled | `false` |
| Provider calls | `0` |
| Inference calls | `0` |
| Docker started | `false` |
| WSL mutated | `false` |
| P15.M10 gate | present |
| P15.M11 authority | preserved |

Required hygiene:

| Check | Result |
| --- | --- |
| Markdown trailing whitespace | `0` |
| Unexpected binary files | `0` |
| New executable files | `0` |
| `__pycache__` | `0` |
| `.pytest_cache` | `0` |

No product test suite is required because no product code changed. The 14
canonical governance tests passed to prove current product integrity remains
unchanged.

## Repository Integrity

| Boundary | Count |
| --- | ---: |
| P15.M8 implementation changes | `0` |
| P15.M8R changes | `0` |
| Runtime adapter changes | `0` |
| Provider credential changes | `0` |
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
| Dependency changes | `0` |
| Lock changes | `0` |
| Docker files created | `0` |
| Compose files created | `0` |
| WSL files created | `0` |
| Runtime directories created | `0` |
| Graphify commands | `0` |
| Graphify changes | `0` |
| OAuth attempts | `0` |
| Credential reads | `0` |
| Credential writes | `0` |
| Provider calls | `0` |
| Inference calls | `0` |
| Worker starts | `0` |
| Agent starts | `0` |

Only this P15.M9 governance record may change.

## Required Final State

| Field | Value |
| --- | --- |
| Verdict | `hermes_0_19_wsl2_development_architecture_ready_with_constraints` |
| Worktree | `<WINDOWS_REPOSITORY_ROOT>` |
| Branch | `p15.m-hermes-0.19-migration` |
| Strategic local target | `WSL2_plus_Docker_Compose` |
| Fallback local target | `WSL2_native` |
| Future target | `external_Linux_VPS_plus_Docker_Compose` |
| Source root | Linux native required |
| Runtime root | Linux native required |
| Windows OneDrive runtime | prohibited |
| Docker started | `false` |
| Compose started | `false` |
| WSL mutated | `false` |
| Repository moved | `false` |
| Runtime directories created | `false` |
| Provider worker enabled | `false` |
| Real credentials configured | `false` |
| Live OAuth attempts | `0` |
| Provider calls | `0` |
| Inference calls | `0` |
| P15.M10 | architecture gate defined |
| P15.M11 | live OAuth authority preserved |
| Candidate files | `1` |
| Git index empty | `true` |
| Staged files | `0` |
| Commits by agent | `0` |
| Pushes by agent | `0` |

## Final Verdict

`hermes_0_19_wsl2_development_architecture_ready_with_constraints`
