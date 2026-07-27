# Hermes 0.19 External Linux VPS Architecture

Date: 2026-07-27

Final verdict: `hermes_0_19_external_linux_vps_architecture_ready_with_constraints`

## Ticket Authority

P15.M13 defines the governed external Linux VPS architecture that follows the accepted Pepper local-runtime baseline. It is architecture-only and does not provision, connect to, mutate, or inspect any remote host.

Accepted local baseline:

```text
Windows development control
-> Linux-native WSL2 checkout
-> Docker Desktop Linux engine
-> Docker Compose
-> loopback-only Pepper dashboard
-> isolated provider worker
-> temporary credential lease
-> OpenAI Codex GPT-5.5
```

Target remote baseline:

```text
human-controlled administration workstation
-> key-authenticated SSH management boundary
-> external Linux VPS
-> root-owned deployment authority
-> Docker Engine + Docker Compose
-> loopback-only Pepper dashboard
-> isolated provider worker network
-> remote governed credential store
-> temporary worker credential leases
-> OpenAI Codex GPT-5.5
```

This verdict means the target remote topology, host boundaries, process boundaries, network boundaries, credential strategy, image-delivery strategy, readiness, shutdown, recovery, rollback, update posture, evidence posture, and P15.M14 prerequisites are defined. It does not mean a VPS exists, a vendor has been selected, a subscription has been purchased, a remote host has been accessed, Pepper has been deployed remotely, a remote credential exists, remote inference has been tested, long-running workers are enabled, remote recovery has been exercised, or production deployment is accepted.

## Repository Gate

| Field | Value |
| --- | --- |
| Required branch | `p15.m-hermes-0.19-migration` |
| Starting HEAD | `64b1bf2df484e059a1ce3f2fb6cceba39c520283` |
| Branch remote | `origin/p15.m-hermes-0.19-migration` |
| Remote HEAD | `64b1bf2df484e059a1ce3f2fb6cceba39c520283` |
| HEAD equals remote | `true` |
| Index before P15.M13 record | empty |
| Tracked worktree before P15.M13 record | clean |
| Visible untracked task candidates before record | `0` |
| P15.M13 record present before creation | `false` |

Resolved P15.M12 authority:

| Field | Value |
| --- | --- |
| P15.M12 commit | `64b1bf2df484e059a1ce3f2fb6cceba39c520283` |
| P15.M12 commit message | `P15.M12 Close complete local runtime acceptance` |
| P15.M12 commit is ancestor of HEAD | `true` |
| HEAD equals P15.M12 commit | `true` |
| Post-P15.M12 commits | `0` |
| P15.M12 committed verdict | `hermes_0_19_complete_local_runtime_acceptance_closed_with_constraints` |
| P15.M12 commit product mutations | `0` |
| P15.M12 commit governance files | `1` |

P15.M12 introduced exactly:

```text
0_architecture/governance/agent_platform_hermes_0_19_complete_local_runtime_acceptance_closure.md
```

## Required Committed Prerequisites

Each prerequisite record was tracked, committed, present in `HEAD`, locally unmodified, and unstaged before this record was created.

| Record | Required verdict |
| --- | --- |
| `agent_platform_hermes_0_19_migration_authorization.md` | `hermes_0_19_migration_authorized_with_constraints` |
| `agent_platform_hermes_0_19_workspace_adoption_assessment.md` | `hermes_0_19_workspace_adoption_assessment_ready_with_constraints` |
| `agent_platform_hermes_0_19_pepper_product_identity_post_commit_integrity_closure.md` | `hermes_0_19_pepper_product_identity_post_commit_integrity_closed_with_constraints` |
| `agent_platform_hermes_0_19_governed_runtime_adapter_post_commit_integrity_closure.md` | `hermes_0_19_governed_runtime_adapter_post_commit_integrity_closed_with_constraints` |
| `agent_platform_hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closure.md` | `hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closed_with_constraints` |
| `agent_platform_hermes_0_19_wsl2_development_architecture.md` | `hermes_0_19_wsl2_development_architecture_ready_with_constraints` |
| `agent_platform_hermes_0_19_docker_desktop_loopback_port_publication_compatibility_assessment.md` | `hermes_0_19_docker_desktop_loopback_port_publication_compatibility_assessed_with_constraints` |
| `agent_platform_hermes_0_19_docker_compose_local_pilot.md` | `hermes_0_19_docker_compose_local_pilot_ready_with_constraints` |
| `agent_platform_hermes_0_19_openai_codex_streaming_tool_free_oauth_inference_revalidation.md` | `hermes_0_19_openai_codex_streaming_tool_free_oauth_inference_revalidated_with_constraints` |
| `agent_platform_hermes_0_19_complete_local_runtime_acceptance_closure.md` | `hermes_0_19_complete_local_runtime_acceptance_closed_with_constraints` |

## Canonical Product Integrity

Pre-record integrity utility result:

| Identity | Files | Bytes | SHA256 |
| --- | ---: | ---: | --- |
| Candidate | `6768` | `149234356` | `a71af0be624cb3f00b37d651248717c38f5bed18e460c6f159636c75a8875df3` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | n/a | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Pre-record governance integrity tests: `14` tests, `0` failures, `0` errors.

## Accepted Local Baseline

P15.M13 preserves the following P15.M12 local-runtime authority unless a stricter remote boundary is explicitly defined.

| Baseline item | Accepted value |
| --- | --- |
| Strategic mode | WSL2 plus Docker Compose |
| Fallback mode | WSL2 native |
| Product | Pepper |
| Product version | `0.1.0-dev` |
| Upstream | Hermes Agent `0.19.0` |
| Product UI | disabled |
| Extension modules | `[]` |
| Dashboard | loopback only |
| Dashboard acceptance | passed |
| SPA and browser acceptance | passed |
| Provider | `openai-codex` |
| Authentication | ChatGPT OAuth |
| Model | `gpt-5.5` |
| Transport | `codex_responses` |
| Provider-wire streaming | `true` |
| Application streaming | `false` |
| Credential delivery | temporary lease |
| Tool-free inference | passed, `PEPPER_P15_M12_OK` |
| Tools | disabled |
| MCP | disabled |
| Automatic retries | disabled |
| Automatic fallback | disabled |
| Dashboard restart | passed |
| Clean shutdown | passed |
| Runtime residue | zero |
| Durable local credential | retained and protected locally |

The local P15.M11A/P15.M12 credential remains local and is not remote deployment material.

## Remote Mode Classification

Mode D is frozen as:

```text
External Linux VPS + Docker Compose
```

| Mode | Classification |
| --- | --- |
| Mode C | WSL2 plus Docker Compose; local development baseline |
| Mode D | External Linux VPS plus Docker Compose; remote operational baseline |
| Mode B | WSL2 native; local fallback only |

Required relationship:

| Question | Answer |
| --- | --- |
| Mode D replaces Mode C for local development | `false` |
| Mode D is production authority | `false` |
| Mode D is initial 24/7 operational target | `true` |
| Mode D requires separate acceptance | `true` |

P15.M13 defines Mode D but does not activate it.

## VPS Provider Boundary

P15.M13 is provider-neutral. No vendor, region, price, account, plan, subscription, or commercial commitment is selected or endorsed.

Required VPS provider capabilities:

| Capability | Requirement |
| --- | --- |
| Virtualization | full VM |
| Architecture | x86_64 |
| Public IP | required for SSH ingress |
| Console or rescue access | required |
| Disk persistence | required |
| Snapshot or image capability | recommended |
| Provider firewall | required, or host firewall equivalent |
| Reverse DNS | optional |
| GPU | not required |
| Managed Kubernetes | not required |
| Managed database | not required |
| Object storage | optional |
| Load balancer | not required for initial pilot |

Rejected hosting classes: shared web hosting, serverless-only runtimes, container platforms without host control, Windows Server, ARM-only hosts for the initial pilot, public Docker API exposure, and Docker daemon access over the network.

Provider-evaluation checklist for the human before P15.M14: full VM control, x86_64 confirmation, public IP or hostname, rescue console availability, firewall capability, persistent disk, snapshot capability when available, supported Linux server images, Docker support, outbound network policy, resource sizing facts, and documented recovery channel.

## Host Operating-System Baseline

Supported host class:

| Field | Requirement |
| --- | --- |
| Kernel | Linux |
| Architecture | x86_64 |
| Distribution class | maintained server distribution |
| Init system | systemd |
| Package updates | security updates supported |
| Container runtime | Docker Engine |
| Compose | Docker Compose plugin |
| Time synchronization | required |
| Persistent filesystem | required |
| Swap | explicitly assessed |
| GPU driver | absent |
| Desktop environment | absent |

Distribution selection criteria: active security support, official Docker support, systemd support, x86_64 packages, predictable security updates, documented upgrade path, and provider rescue compatibility. The exact distribution and release are deferred to the human before P15.M14 and must be recorded by P15.M14.

## Remote Host Identity And Paths

Placeholders:

```text
<PEPPER_VPS_HOST>
<PEPPER_VPS_PUBLIC_IP>
<PEPPER_VPS_ADMIN_USER>
<PEPPER_VPS_SSH_PORT>
<PEPPER_VPS_DEPLOYMENT_ROOT>
<PEPPER_VPS_RUNTIME_ROOT>
<PEPPER_VPS_LOG_ROOT>
<PEPPER_VPS_CREDENTIAL_ROOT>
```

Canonical host paths:

| Role | Path |
| --- | --- |
| Deployment root | `/opt/pepper` |
| Runtime root | `/var/lib/pepper` |
| Log root | `/var/log/pepper` |
| Credential root | `/var/lib/pepper/credentials/openai-codex.primary` |
| Deployment releases | `/opt/pepper/releases` |
| Active release link | `/opt/pepper/current` |

Required path posture: deployment root outside user homes, runtime root outside source checkout, credential root outside source checkout, logs outside source checkout, OneDrive not applicable, Windows mounts `0`.

## Administrative Access Boundary

Initial management ingress is key-authenticated SSH only.

| Control | Posture |
| --- | --- |
| Root SSH login | disabled |
| Password authentication | disabled |
| SSH key authentication | required |
| Interactive cloud password | prohibited |
| SSH private key on VPS | `false` |
| SSH private key in repository | `false` |
| SSH private key in runtime evidence | `false` |
| Agent forwarding | disabled by default |
| Public application ports | `0` |
| Public Docker socket | `false` |
| Public Docker API | `false` |
| SSH source restriction | provider firewall or host firewall |
| Human operator | required |
| Automation key | deferred |
| Persistent CI access | deferred |

P15.M13 does not create, inspect, copy, register, or validate any SSH key.

## Host Privilege Model

| Boundary | Requirement |
| --- | --- |
| Host administration | human-authorized sudo |
| Deployment authority | root-owned systemd and deployment files |
| Application processes | non-root containers |
| Pepper application user | non-root |
| Docker daemon | not exposed to application |
| Docker socket mounted into application | `false` |
| Privileged containers | `false` |
| Host PID namespace | `false` |
| Host network | `false` |
| Host device mounts | `0` |
| Capabilities | drop `ALL` |
| no-new-privileges | `true` |

Docker daemon administration remains host-root-equivalent authority and must not be granted to the Pepper application process. The runtime application user must not be placed in the Docker group merely to simplify container control. A future systemd deployment unit may invoke Docker as root while application containers remain non-root and capability-restricted.

## Firewall And Ingress Architecture

Ingress is deny-by-default.

| Public ingress | Posture |
| --- | --- |
| SSH | allowed from authorized administration sources |
| HTTP | denied |
| HTTPS | denied |
| Pepper dashboard | denied |
| Docker API | denied |
| Provider worker | denied |
| Metrics | denied |
| Database | denied |

Required egress:

| Egress class | Posture |
| --- | --- |
| OS security updates | allowed |
| Container image delivery | allowed when required |
| OpenAI Codex endpoint | allowed only for provider worker |
| DNS | allowed |
| Time synchronization | allowed |
| Arbitrary dashboard egress | not required |

No firewall command is authorized by P15.M13.

## Dashboard Access Architecture

Initial remote-dashboard access is:

```text
VPS loopback publication
+
human SSH local-port forwarding
```

Required VPS topology:

```text
Pepper dashboard:       127.0.0.1:9120 inside container
runtime relay:          0.0.0.0:9119 inside container
Docker host publication: 127.0.0.1:19120:9119
```

Operator access path:

```text
operator localhost
-> SSH local port forward
-> VPS 127.0.0.1:19120
-> container relay 0.0.0.0:9119
-> dashboard 127.0.0.1:9120
```

Required posture: VPS public dashboard listener `false`, public reverse proxy absent, public TLS endpoint absent, DNS name not required, browser auth boundary is the SSH tunnel, dashboard provider credentials absent, and dashboard provider authority `false`. P15.M13 does not authorize a public reverse proxy. Public or overlay-network access requires a separate ticket.

## Docker Network Architecture

Required networks:

| Network | Purpose | Internal | Provider egress | Dashboard connected |
| --- | --- | --- | --- | --- |
| Publication network | dashboard relay and host loopback publication | `false` | `false` | `true` |
| Provider egress network | isolated OpenAI Codex worker egress | `false` | `true` | `false` |

Required isolation: dashboard and worker do not share a network, worker is not connected to publication network, dashboard is not connected to provider network, provider credentials are not in dashboard, durable credential store is not in dashboard, and Docker socket is absent from every service.

Initial remote pilot service ceilings: dashboard services `1`, provider workers `0` in P15.M14, provider workers `1` maximum in P15.M15, concurrent provider workers `1` maximum, agent workers `0` until separately authorized.

## Container Security Baseline

Required controls:

| Control | Requirement |
| --- | --- |
| Read-only root filesystem | `true` |
| Non-root user | `true` |
| Cap drop | `ALL` |
| Security opt | `no-new-privileges:true` |
| Privileged | `false` |
| Restart policy | `no` for pilot; bounded policy required before 24/7 |
| Host network | `false` |
| Host PID | `false` |
| Host IPC | `false` |
| Docker socket | absent |
| Source checkout mount | absent |
| Windows mount | absent |
| Arbitrary host root mount | absent |
| Temporary filesystems | explicitly declared |
| Memory limit | required |
| CPU limit | required |
| PID limit | required |
| Healthcheck | required |
| Logging limits | required |

Initial remote pilot and future unattended 24/7 operation are distinct states. Automatic restart must not be enabled before recovery behavior is validated.

## Deployment Artifact And Release Layout

Each deployment uses one immutable release directory:

```text
/opt/pepper/releases/<release-id>
```

Required release contents: `compose.yaml`, `deployment-manifest.json`, `image-manifest.json`, bounded runtime scripts, checksums, and operator instructions. The active release is `/opt/pepper/current`.

Release ownership and contents: owner `root`, group `root`, directory mode `0755` or stricter, secret files `0`, credential files `0`, SSH keys `0`.

Required release identity: exact source commit, exact product candidate SHA-256, exact product payload SHA-256, exact image digest or image ID, exact deployment manifest SHA-256, and exact Compose SHA-256. A mutable source checkout must not be used as the live deployment directory.

## Image Distribution Strategy

Initial P15.M14 pilot strategy is frozen as:

```text
exact image archive transferred through authenticated SSH
+
pre-transfer SHA-256
+
post-transfer SHA-256
+
post-load image identity validation
```

Initial-pilot posture: public registry not required, registry credentials `0`, `latest` tag prohibited, mutable tag as only authority prohibited, image archive allowed for initial pilot, authenticated SSH archive transport, archive checksum required, loaded image ID required, loaded repo digest recorded when available, source commit recorded, and product identity recorded.

Archive handling: archive inside repository `false`, archive committed `false`, archive retention after success optional and bounded, archive secret-bearing `false`. Long-term private OCI registry delivery remains deferred. P15.M13 does not create or transfer an image archive.

## Source And Build Boundary

Frozen initial-pilot boundary:

| Action | Posture |
| --- | --- |
| Build on VPS | `false` |
| Source checkout required on VPS | `false` |
| Live container source mount | `false` |
| `npm install` on VPS | `false` |
| `pip install` on VPS | `false` |
| Editable install on VPS | `false` |
| Native Hermes updater | non-authoritative |
| Untracked remote source modification | prohibited |

Initial deployment authority is a locally validated immutable image plus an exact remote deployment bundle. Any remote image rebuild requires separate authorization.

## Remote Credential Architecture

The local P15.M11A/P15.M12 credential must remain local.

Prohibited actions: copy local durable credential to VPS, mount local credential over SSH, synchronize local `auth.json`, import Codex CLI credentials, import VS Code credentials, and reuse browser storage.

Required future remote credential strategy:

```text
fresh remote device-code OAuth
-> remote acquisition store
-> governed remote promotion
-> protected remote durable store
-> temporary per-worker lease
```

Remote credential root:

```text
/var/lib/pepper/credentials/openai-codex.primary
```

Protection requirements: directory mode `0700`, file mode `0600`, owner dedicated governed runtime identity, credential count `1`, providers object empty, source `manual:device_code`, endpoint `https://chatgpt.com/backend-api/codex`. Remote OAuth is deferred to P15.M15. P15.M14 remains provider-null and credential-free.

## Credential Lease Boundary

Remote credential delivery is frozen as:

| Field | Requirement |
| --- | --- |
| Durable store mounted into dashboard | `false` |
| Durable store mounted into worker | `false` |
| Temporary projection | required |
| Active leases maximum | `1` |
| Credentials per lease | `1` |
| Lease TTL maximum | `900000` ms |
| Automatic refresh | `false` |
| Refresh writeback | `false` |
| Lease release | mandatory |
| Lease residue | zero |

Worker authority is one temporary projected `HERMES_HOME`, one bounded provider request, one result, and lease release. Long-running workers must not hold permanent direct access to the durable credential store.

## Remote OAuth And Refresh Boundary

Remote OAuth owner is P15.M15. Device-code display is a transient human-visible channel. Verification URL retention, device code retention, account identity retention, automatic OAuth retry, and credential refresh are prohibited by P15.M13. Remote revocation remains unsupported or unverified.

When a future remote credential is expired or too close to expiry, the system must stop, classify `refresh-required`, preserve the credential, and require separate authorization. Silent refresh is prohibited.

## Systemd And Lifecycle Architecture

Future host lifecycle units:

```text
pepper-dashboard.service
pepper-runtime-cleanup.service
```

Potential future worker units remain deferred.

Required dashboard unit characteristics: owner `root`, start action `docker compose up`, stop action `docker compose down`, working directory `/opt/pepper/current`, bounded start timeout, bounded stop timeout, restart disabled during initial pilot, dependency on `docker.service`, explicit network-online dependency, no credential dependency, and no provider authority.

Required lifecycle order:

```text
validate deployment
-> validate resource collision
-> start
-> bounded readiness
-> stable operation
-> graceful shutdown
-> bounded forced cleanup only when required
-> residue verification
```

P15.M14 may use transient manual lifecycle commands. Permanent systemd installation requires explicit P15.M14 authority.

## Readiness Architecture

Readiness layers: container running, container health, direct dashboard status, relay status, VPS loopback status, SSH-forwarded status, SPA root, JavaScript assets, stylesheet assets, and headless browser render. A live process is not sufficient readiness evidence.

Required timeout policy: container start timeout bounded, backend readiness timeout `60` seconds maximum for pilot, browser readiness timeout bounded, poll interval explicit, infinite wait prohibited.

## Shutdown And Residue Architecture

Required shutdown sequence:

```text
stop accepting new work
-> stop provider worker
-> release temporary lease
-> stop dashboard
-> remove project containers
-> remove project networks
-> verify host listeners
-> verify processes
-> preserve durable credential
-> preserve active release
```

Required final residue: containers `0`, networks `0`, host application listeners `0`, provider worker processes `0`, dashboard processes `0`, relay processes `0`, active leases `0`, temporary auth files `0`.

Allowed retained state: active deployment release, previous rollback release, protected remote durable credential, bounded secret-free logs, exact image, and deployment manifests.

## Recovery Architecture

Common failure policy for every class below: automatic retry is prohibited unless later authorized, cleanup is bounded, credential preservation is explicit, rollback is explicit for deployment-impacting failures, and human escalation is required when the bounded path cannot restore the accepted safe state.

| Failure class | Detection | Cleanup | Credential preservation | Rollback |
| --- | --- | --- | --- | --- |
| `host_unreachable` | SSH/connectivity probe fails | none beyond local abort | preserve | not applicable |
| `SSH_authentication_failure` | SSH auth refusal | none beyond local abort | preserve | not applicable |
| `host_identity_mismatch` | host-key fingerprint mismatch | abort | preserve | not applicable |
| `firewall_misconfiguration` | expected SSH or loopback path unavailable | revert only authorized firewall delta | preserve | possible |
| `Docker_daemon_unavailable` | Docker command or service health fails | stop deployment attempt | preserve | possible |
| `image_transfer_failure` | transfer exits non-zero | remove incomplete archive | preserve | prior release remains |
| `image_checksum_mismatch` | SHA mismatch | delete suspect archive | preserve | prior release remains |
| `image_load_failure` | image load exits non-zero | remove failed load artifacts when safe | preserve | prior release remains |
| `deployment_manifest_mismatch` | manifest/checksum validation fails | do not start | preserve | prior release remains |
| `resource_collision` | listener/container/network/path collision | do not start; bounded cleanup only if owned | preserve | prior release remains |
| `dashboard_readiness_failure` | status probes fail | stop dashboard project | preserve | prior release start |
| `SPA_asset_failure` | asset metadata/fetch/render failure | stop dashboard project | preserve | prior release start |
| `browser_render_failure` | headless render fails | stop dashboard project | preserve | prior release start |
| `credential_missing` | credential status absent | do not start worker | preserve absent state | no provider rollback |
| `credential_expired` | expiry metadata out of bounds | stop worker path | preserve | no refresh |
| `lease_creation_failure` | lease API fails | remove partial projection if owned | preserve durable store | no provider call |
| `provider_reachability_failure` | bounded provider request fails by reachability | release lease | preserve durable store | stop worker |
| `provider_entitlement_failure` | provider safe error classification | release lease | preserve durable store | stop worker |
| `provider_quota_failure` | quota/rate safe classification | release lease | preserve durable store | stop worker |
| `provider_transport_failure` | transport/protocol safe classification | release lease | preserve durable store | stop worker |
| `worker_timeout` | bounded timeout expires | terminate worker, release lease | preserve durable store | stop worker |
| `lease_cleanup_failure` | release reports residue | stop further work, preserve residue evidence | preserve durable store | human action |
| `shutdown_failure` | stop/down timeout or process residue | bounded forced cleanup if owned | preserve durable store | human action if unresolved |
| `runtime_residue` | residue validation non-zero | bounded cleanup if owned | preserve durable store | human action if unresolved |
| `disk_pressure` | disk threshold exceeded | stop new deployments/work | preserve durable store | possible cleanup/rollback |
| `memory_pressure` | memory threshold exceeded | stop worker, stop dashboard if needed | preserve durable store | possible rollback |

## Rollback Architecture

Release rollback is frozen as:

```text
current release
-> graceful shutdown
-> verify zero temporary leases
-> move current symlink to prior accepted release
-> start prior release
-> bounded readiness
-> verify exact prior image
-> record rollback
```

Rollback state: previous release retained `true`, previous image retained `true`, mutable latest dependency `false`, database migration dependency absent for initial scope, credential format migration prohibited without separate ticket, rollback requires provider call `false`, rollback requires new OAuth `false`.

Fail-safe: when both forward deployment and rollback fail, leave Pepper stopped, preserve the durable credential, close application listeners, and require human action.

## Update Architecture

Governed update flow:

```text
new source authority
-> local product integrity
-> local tests
-> local image build
-> exact image identity
-> deployment bundle
-> human approval
-> remote transfer
-> checksum verification
-> controlled deployment
-> readiness
-> stability
-> acceptance or rollback
```

Native Hermes updater unauthorized, automatic latest pull prohibited, automatic source pull on VPS prohibited, automatic dependency upgrade prohibited, unattended product upgrade prohibited, host security updates separately governed, application update immutable-release based.

## Logging And Evidence Architecture

Retained evidence classes: deployment identity, image identity, source commit, start and stop timestamps, readiness results, HTTP status metadata, asset metadata, browser pass/fail metadata, resource usage summary, provider call counters, safe inference result when explicitly authorized, lease lifecycle status, cleanup status, and rollback status.

Forbidden evidence classes: access tokens, refresh tokens, authorization headers, device codes, verification URLs, account identity, JWT claims, raw environment dumps, raw provider responses, reasoning traces, browser cookies, complete HTML, complete JavaScript bundles, SSH private keys, cloud API credentials.

Log controls: rotation required, maximum size bounded, retention bounded, secret scanning required, governed-worker prompt logging disabled, Docker logging size and file-count limited, journald retention assessed.

## Backup Boundary

Runtime container backup unnecessary, temporary lease backup prohibited, temporary auth backup prohibited, OAuth token plaintext backup prohibited, source checkout backup unnecessary for runtime, deployment manifest backup required, active and previous release metadata required, credential recovery is reacquire-under-explicit-authority, provider snapshot optional as host recovery aid.

A provider VPS snapshot must not be treated as a safe credential-export mechanism without separate assessment.

## Resource Sizing Framework

Sizing is derived from measurement, not guessed.

| Class | Workload |
| --- | --- |
| Initial provider-null pilot | dashboard only |
| Operational provider worker | dashboard plus one bounded provider worker |

Required measured inputs: local image size, dashboard idle memory, dashboard peak memory, worker peak memory, CPU peak, disk usage, log growth, restart behavior, network egress.

Required sizing outputs: derived minimum vCPU, derived minimum RAM, explicit recommended RAM headroom, minimum disk equal to image plus two releases plus logs plus headroom, explicit swap policy, explicit disk alert threshold, explicit memory alert threshold. GPU is not required for Pepper. Omniverse and GPU-bound Siamese workloads are outside the Pepper VPS scope.

## Monitoring Boundary

Minimum monitoring: host reachability, disk usage, memory usage, load average, Docker daemon, container health, dashboard status, restart count, host listener posture, active lease count. Credential secret values and provider token values are never monitored. External monitoring services are not selected by P15.M13. Public monitoring endpoints are prohibited in the initial architecture.

## Local-To-Remote Parity Matrix

Required parity:

| Boundary | Local accepted value | Remote required value |
| --- | --- | --- |
| Product source | same commit authority | same commit authority |
| Product candidate identity | same algorithm | same algorithm |
| Product payload identity | same algorithm | same algorithm |
| Image | exact local identity | exact digest or image identity |
| Compose model | governed Compose topology | same topology class |
| Dashboard bind | loopback | loopback |
| Relay | required | required |
| Dashboard provider authority | none | none |
| Provider network | isolated | isolated |
| Credential store | governed | governed |
| Credential delivery | temporary lease | temporary lease |
| Provider | `openai-codex` | `openai-codex` |
| Model | `gpt-5.5` | `gpt-5.5` |
| Transport | `codex_responses` | `codex_responses` |
| Provider-wire streaming | `true` | `true` |
| Application streaming | `false` | `false` |
| Tools | disabled | disabled |
| MCP | disabled | disabled |
| Automatic retries | disabled | disabled |
| Fallback | disabled | disabled |
| Readiness | bounded | bounded |
| Shutdown | bounded | bounded |
| Residue | zero | zero |

Allowed differences: Windows/WSL2 control becomes external Linux, Docker Desktop becomes native Docker Engine, local loopback becomes SSH-forwarded loopback, user-local runtime roots become FHS host paths, transient local lifecycle becomes root-owned remote service lifecycle, local image becomes verified archive transfer.

No security boundary may be weaker remotely than locally.

## Threat Model

| Threat | Asset | Entry point | Preventive control | Detective control | Recovery control | Residual risk |
| --- | --- | --- | --- | --- | --- | --- |
| Public dashboard exposure | dashboard/session surface | public listener or proxy | loopback bind, deny public HTTP/HTTPS | listener scan, readiness metadata | stop service, close listener | SSH host compromise can still expose tunnel |
| SSH credential theft | host admin authority | stolen private key/agent | key-only, source restriction, no key on VPS/repo/evidence | SSH logs, provider console alerts | revoke key, rotate host access | operator endpoint security remains external |
| Host compromise | full VPS | OS exploit or stolen admin | patched server OS, least services, firewall | host monitoring, log review | isolate, snapshot forensics, rebuild | host root can read local remote secrets |
| Docker socket exposure | host root-equivalent Docker API | socket mount/API | no socket in app, no public API | mount inspection, listener scan | stop containers, rotate host | root-controlled deployment still uses Docker |
| Malicious image replacement | runtime image | archive or load tamper | SHA and image identity validation | manifest comparison | reject image, rollback | local build chain must stay trusted |
| Mutable-tag substitution | image authority | `latest` or mutable tag | exact digest/image ID required | deployment manifest check | reject deployment | registry metadata may be absent for archive |
| Deployment-bundle tampering | Compose/scripts/manifests | transfer or filesystem tamper | checksums, root-owned release | manifest verification | reject release, rollback | root compromise can tamper post-check |
| Credential-file disclosure | OAuth tokens | filesystem read/logging | `0700`/`0600`, dedicated owner, no release secrets | secret scan, permission audit | stop worker, revoke/reacquire under authority | host root can read credential |
| Credential mounted into dashboard | provider credential | bad Compose mount | dashboard mount denylist | Compose/rendered mount inspection | stop, remove project | human review error possible |
| Credential mounted permanently into worker | provider credential | bad worker mount | temporary projection only | mount and lease audit | stop worker, release lease | active lease exposure during request |
| Provider-token leakage through logs | OAuth token | logs/errors/env dumps | forbidden evidence, prompt/env logging disabled | secret scans | purge logs, rotate/reacquire | third-party library errors may drift |
| Remote source drift | source authority | mutable checkout/pull | no live checkout, immutable release | release manifest verification | redeploy exact release | remote root can mutate files |
| Unbounded restart loop | availability/cost | restart policy | restart disabled in pilot | restart count monitor | stop unit, inspect | later 24/7 policy needs validation |
| Failed shutdown leaving listeners | network exposure | stop failure | bounded stop/down, residue checks | listener/process scans | forced cleanup if owned | kernel/Docker bugs may require human action |
| Orphaned credential lease | credential projection | crash during worker | lease TTL, release mandatory | active lease count | cleanup projection, stop work | cleanup may fail under filesystem errors |
| Disk exhaustion | host availability | logs/images/releases | sizing, log rotation, disk thresholds | disk monitor | stop new work, prune only authorized owned artifacts | provider storage outage remains external |
| Memory exhaustion | host availability | dashboard/worker usage | memory limits, sizing headroom | memory monitor, container health | stop worker/dashboard, rollback | kernel OOM behavior may kill services |
| Unauthorized automatic update | product integrity | updater/pull/cron | updater unauthorized, no auto pulls | manifest/source/image drift checks | rollback to accepted release | OS security updates separately governed |
| Rollback to unverified image | runtime integrity | bad previous release | retain exact previous image/manifest | prior image identity check | leave stopped if mismatch | previous release can be missing if retention violated |

## P15.M14 Human Prerequisites

P15.M14 must not begin until the human supplies or confirms: VPS provider selected, VPS purchased or provisioned, public IP or hostname, Linux distribution and exact release, x86_64 architecture, administrative SSH username, SSH port, local private-key path or approved SSH-agent identity, expected host-key fingerprint through a trusted channel, authorized administration source IP or network, provider firewall availability, rescue-console availability, allocated vCPU, allocated RAM, and allocated disk.

Required explicit P15.M14 authorizations: connect to the named VPS, verify the host key, inspect the host, apply bounded security configuration, install or validate Docker, create Pepper directories, transfer the exact provider-null image and deployment bundle, start the provider-null dashboard, perform readiness validation, and perform shutdown validation.

P15.M13 does not ask for these values during execution.

## P15.M14 Scope Boundary

P15.M14 is frozen as:

```text
External Linux VPS Provider-Null Infrastructure Pilot
```

P15.M14 may later authorize remote SSH, host inventory, bounded host hardening, Docker installation or validation, image archive transfer, provider-null dashboard, and SSH-tunnel browser acceptance. P15.M14 must not authorize remote OAuth, remote credential creation, provider dispatch, or long-running worker execution.

Required P15.M14 final posture: public application ports `0`, remote credentials `0`, remote provider calls `0`, dashboard provider authority `false`, provider-null remote pilot accepted or rolled back.

## P15.M15 Scope Boundary

P15.M15 is frozen as:

```text
Remote Governed Credential and Bounded Provider Worker Pilot
```

Potential P15.M15 authority: one explicit remote device-code OAuth attempt, one remote governed credential, one temporary lease, one provider dispatch, model `gpt-5.5`, tools `0`, MCP `0`, dashboard provider authority `false`.

P15.M13 and P15.M14 must not exercise P15.M15 scope.

## P15.M16 Scope Boundary

P15.M16 is frozen as:

```text
Remote Recovery, Rollback and Local-to-Remote Acceptance Closure
```

Potential P15.M16 coverage: remote restart, host reboot survival, controlled failure injection, worker timeout recovery, orphan prevention, credential-lease cleanup, forward deployment, rollback to previous release, local-to-remote parity, longer stability window, final remote residue, and operational handoff.

P15.M16 does not automatically imply production readiness.

## Architecture Decision Matrix

| Decision | Status |
| --- | --- |
| Remote mode | accepted: Mode D external Linux VPS plus Docker Compose |
| Provider selection | deferred to human |
| Public dashboard | rejected |
| Initial access | SSH local port forward |
| Public reverse proxy | deferred |
| Host application ports | loopback only |
| Host privilege | root-owned deployment, non-root containers |
| Docker socket in application | rejected |
| Live source checkout | rejected |
| Build on VPS | rejected for initial pilot |
| Initial image delivery | checksum-verified SSH archive |
| Mutable latest | rejected |
| Remote credential | fresh remote device-code OAuth |
| Copy local credential | rejected |
| Durable store in dashboard | rejected |
| Durable store directly in worker | rejected |
| Temporary worker lease | required |
| Automatic refresh | rejected until separate validation |
| Automatic product update | rejected |
| Automatic restart | deferred until recovery validation |
| Remote provider pilot owner | P15.M15 |
| Rollback closure owner | P15.M16 |

## No-Execution Counters

| Counter | Value |
| --- | ---: |
| VPS purchases | `0` |
| Cloud API calls | `0` |
| Remote hosts contacted | `0` |
| SSH connections | `0` |
| SCP transfers | `0` |
| SFTP transfers | `0` |
| rsync transfers | `0` |
| DNS changes | `0` |
| Firewall changes | `0` |
| Remote packages installed | `0` |
| Remote Docker actions | `0` |
| Images transferred | `0` |
| Images pushed | `0` |
| Images pulled | `0` |
| Remote containers started | `0` |
| Remote networks created | `0` |
| Remote OAuth attempts | `0` |
| Remote credentials created | `0` |
| Remote credential leases | `0` |
| Remote provider dispatches | `0` |
| Local provider dispatches | `0` |

## Candidate Set And Repository Integrity

Created candidate:

```text
0_architecture/governance/agent_platform_hermes_0_19_external_linux_vps_architecture.md
```

Required candidate posture: candidate files `1`, unexpected candidates `0`, modified tracked files `0`, product files modified `0`, tests modified `0`, modification register modified `false`, baseline JSON modified `false`, import manifest modified `false`, package manifests modified `0`, lockfiles modified `0`, Dockerfiles modified `0`, repository Compose modified `false`, runtime scripts tracked `0`, credential files tracked `0`, SSH files tracked `0`, Graphify modified `false`.

Repository integrity boundaries: P15.M12 changes `0`, product changes `0`, runtime-adapter changes `0`, provider changes `0`, credential changes `0`, worker changes `0`, dashboard changes `0`, frontend changes `0`, Dockerfile changes `0`, Compose changes `0`, dependency changes `0`, lockfile changes `0`, modification-register changes `0`, baseline changes `0`, Graphify commands `0`, Graphify changes `0`.

## Residual Constraints

P15.M13 does not prove VPS availability, host hardening, SSH access, remote Docker availability, image transfer, remote dashboard readiness, remote browser acceptance, remote credential acquisition, provider reachability from the VPS, remote OpenAI Codex entitlement, remote recovery, remote rollback, unattended 24/7 safety, or production readiness.

P15.M14 remains blocked until P15.M13 is accepted by the human reviewer, committed, pushed to `origin/p15.m-hermes-0.19-migration`, and the human supplies the required VPS and SSH facts with explicit remote-action authority.

## Final Verdict

`hermes_0_19_external_linux_vps_architecture_ready_with_constraints`
