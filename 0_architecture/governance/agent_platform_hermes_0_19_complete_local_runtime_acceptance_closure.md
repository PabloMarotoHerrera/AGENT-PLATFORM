# Hermes 0.19 Complete Local Runtime Acceptance Closure

Date: 2026-07-26

Final verdict: `hermes_0_19_complete_local_runtime_acceptance_closed_with_constraints`

## Ticket Authority

P15.M12 was authorized as the complete local-runtime acceptance closure after P15.M10, P15.M10B, and P15.M11A.

P15.M12 authorized one local dashboard/SPA/browser acceptance run, one restart acceptance run, one retained-image Docker Compose lifecycle, exactly one additional temporary OpenAI Codex credential lease, exactly one additional provider dispatch, one tool-free GPT-5.5 inference returning `PEPPER_P15_M12_OK`, lease cleanup, shutdown cleanup, residue validation, and exactly one governance record.

P15.M12 did not authorize product source changes, test changes, manifest changes, lock changes, Dockerfile changes, repository Compose changes, additional OAuth attempts, credential promotion, model-list calls, usage calls, tool calls, MCP calls, automatic retries, automatic fallback, staging, commits, pushes, image rebuilds, image pulls, or image pushes.

## Repository State

| Field | Value |
| --- | --- |
| Repository root | `C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| HEAD | `87d8a6996555f383d01699a601dc2673f19a7d2f` |
| Upstream | `origin/p15.m-hermes-0.19-migration` |
| Upstream HEAD | `87d8a6996555f383d01699a601dc2673f19a7d2f` |
| HEAD equals upstream | `true` |
| Tracked worktree before record | clean |
| Staged files before record | `0` |

Required prerequisite records were present in `HEAD`, tracked, locally unmodified, and unstaged before this closure record was created.

| Record | Required verdict |
| --- | --- |
| `agent_platform_hermes_0_19_migration_authorization.md` | `hermes_0_19_migration_authorized_with_constraints` |
| `agent_platform_hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closure.md` | `hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closed_with_constraints` |
| `agent_platform_hermes_0_19_wsl2_development_architecture.md` | `hermes_0_19_wsl2_development_architecture_ready_with_constraints` |
| `agent_platform_hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repair.md` | `hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repaired_with_constraints` |
| `agent_platform_hermes_0_19_dashboard_readonly_plugin_manifest_build_post_commit_integrity_closure.md` | `hermes_0_19_dashboard_readonly_plugin_manifest_build_post_commit_integrity_closed_with_constraints` |
| `agent_platform_hermes_0_19_docker_desktop_loopback_port_publication_compatibility_assessment.md` | `hermes_0_19_docker_desktop_loopback_port_publication_compatibility_assessed_with_constraints` |
| `agent_platform_hermes_0_19_docker_compose_local_pilot.md` | `hermes_0_19_docker_compose_local_pilot_ready_with_constraints` |
| `agent_platform_hermes_0_19_openai_codex_streaming_tool_free_oauth_inference_revalidation.md` | `hermes_0_19_openai_codex_streaming_tool_free_oauth_inference_revalidated_with_constraints` |

## Pre-Runtime Gates

Canonical integrity before live activity:

| Identity | Files | Bytes | SHA256 |
| --- | ---: | ---: | --- |
| Candidate | `6768` | `149234356` | `a71af0be624cb3f00b37d651248717c38f5bed18e460c6f159636c75a8875df3` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | n/a | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Regression gates before live activity:

| Gate | Result |
| --- | --- |
| Governance integrity tests | `14` tests, `0` failures, `0` errors |
| Product config regression | `10 passed` |
| Provider contract regression | `119 passed`, expected `3` warnings |
| Runtime-adapter targeted rerun | `PROCESS-001` passed |
| Runtime-adapter full rerun | `143 passed`, `5 skipped` |

The initial runtime-adapter run observed one transient `PROCESS-001` terminal observation failure: `unexpected_exit_code`, `status=unknown`, `exit_code=None`. Lifecycle-probe residue before rerun was `0`; the targeted rerun and full suite rerun passed. P15.M12 classifies this as `transient_process_terminal_observation_race`, not a product mutation.

Post-image diff from retained image source commit `990d153cd370f9f6289ff4ca61ff1a9f79e139dd` to P15.M12 `HEAD` was governance-only. Product, test, manifest, register, lock, and Dockerfile changes in that diff were `0`.

## Retained Runtime Foundation

| Field | Value |
| --- | --- |
| Image tag | `pepper-agent:p15-m10-990d153cd370` |
| Image ID | `sha256:8e7d45adab5b5fa4b34a7c196929490521ac39d2d909e54d4866ddd772eebcfd` |
| Image OS/architecture | `linux/amd64` |
| Docker client/server | `29.4.1` |
| Docker Compose | `5.1.3` |
| Docker context | `desktop-linux` |
| Image rebuilds/pulls/pushes | `0` / `0` / `0` |

Linux-native checkout `/home/pablo/src/pepper/agent-platform` was clean at `87d8a6996555f383d01699a601dc2673f19a7d2f` and matched origin.

## Runtime Root And Files

P15.M12 runtime root was created outside Git:

```text
/home/pablo/.local/share/pepper/pilots/p15-m12-87d8a6996555
```

Directories `scripts`, `evidence`, `logs`, `leases`, and `dashboard-home` were `0700`; runtime files were `0600`.

| File | Bytes | SHA256 |
| --- | ---: | --- |
| `scripts/loopback_relay.py` | `4191` | `64daf4dfed3a585e6d67cadc9e40dec0e3c563275012ddc4dee814274813a228` |
| `scripts/tool_free_worker.py` | `18837` | `99e6ca7cba492497f50a24ae1eefec6d7215c63ac963b7923e28ba122954e9d8` |
| `scripts/browser_acceptance.py` | `3733` | `554d7d9540df148d58c306cd43534a6d379678299532801c4fb7bd56b0d70cb8` |
| `scripts/stability_probe.py` | `5014` | `06ec89f85b6cf2f44a090618800620921f70dd29569746a12d4f7a5aff0df0b8` |
| `compose.yaml` | `1673` | `3fdb54bf05f39f807bfd668df1f7d401112b9acb2ece769c4f6773ea1869fbbe` |

The relay script was copied from the accepted P15.M10 runtime artifact to preserve the governed byte stream and SHA-256 exactly.

## Compose And Dashboard Contract

`docker compose config --quiet` passed.

| Field | Value |
| --- | --- |
| Compose project | `pepper-p15m12` |
| Service | `pepper_dashboard` |
| Image | `pepper-agent:p15-m10-990d153cd370` |
| Pull policy | `never` |
| Host bind | `127.0.0.1:19120` |
| Relay topology | `0.0.0.0:9119 -> 127.0.0.1:9120` |
| Dashboard bind | `127.0.0.1:9120` |
| Network | `pepper-p15m12_publication`, bridge, `internal: false` |
| Host network | `false` |
| Dashboard public bind | `false` |
| Host public exposure | `false` |
| Source checkout mounts | `0` |
| Docker socket mounts | `0` |
| Windows mounts | `0` |
| Credential mounts into dashboard | `0` |

Container security posture: `user=1000:1000`, `read_only=true`, `privileged=false`, `cap_drop=ALL`, `no-new-privileges=true`, `restart=no`, `pids_limit=256`, `mem_limit=4294967296`, and `cpus=4.0`.

Compose-supplied environment keys were limited to `HOME`, `HERMES_HOME`, `XDG_CACHE_HOME`, `XDG_STATE_HOME`, `TZ`, `PYTHONUNBUFFERED`, and `PYTHONDONTWRITEBYTECODE`. Provider credential environment values were `0`.

## Dashboard And Browser Acceptance

Cycle-one readiness passed.

| Endpoint | Status | Bytes | SHA256 |
| --- | ---: | ---: | --- |
| Direct dashboard `http://127.0.0.1:9120/api/status` | `200` | `623` | `e5da370985238cb721a23f212c161c5f694ddad2e3f90275623158312d03cbe5` |
| Relayed `http://127.0.0.1:9119/api/status` | `200` | `623` | `e5da370985238cb721a23f212c161c5f694ddad2e3f90275623158312d03cbe5` |
| Windows host `http://127.0.0.1:19120/api/status` | `200` | `623` | `e5da370985238cb721a23f212c161c5f694ddad2e3f90275623158312d03cbe5` |

Cycle-one browser/SPA acceptance through `http://127.0.0.1:19120` passed: `/api/status` returned `200`, root `/` returned `200` and `721` HTML bytes, the application root was present, and two assets were fetched successfully. Asset bodies were not retained.

| Asset | Status | Content type | Bytes | SHA256 |
| --- | ---: | --- | ---: | --- |
| `/assets/index-ZdPF3DBY.css` | `200` | `text/css; charset=utf-8` | `117800` | `7a97f3d3da6a4d924ea3c2d8d3470507236ad8ed5387f15be9ca1e6d9c546fe7` |
| `/assets/index-e15jtuxO.js` | `200` | `text/javascript; charset=utf-8` | `1994674` | `4721ffc61b5d4afaa0579011ddfb57ef95a63164c044f9772be01893469e75be` |

Container health during cycle one was `running/healthy` with restart count `0`. Host listener enumeration showed one loopback listener on `127.0.0.1:19120` and no wildcard host listener.

## Credential Preflight And Lease

The retained governed durable credential root was checked in a no-network retained-image control container through `read_openai_codex_credential_status`.

| Field | Value |
| --- | --- |
| Provider | `openai-codex` |
| Credential store ID | `openai-codex.primary` |
| Endpoint | `https://chatgpt.com/backend-api/codex` |
| Model | `gpt-5.5` |
| Transport | `codex_responses` |
| Configured | `true` |
| Durable store present/valid | `true` / `true` |
| Protection valid | `true` |
| Provider state present | `false` |
| Pool state present | `true` |
| Token pair present | `true` |
| Credential count | `1` |
| Active provider matches | `true` |
| Expiry known | `true` |
| Usable for bounded lease | `true` |
| Active leases before P15.M12 lease | `0` |
| OAuth attempts in preflight | `0` |
| Provider dispatches in preflight | `0` |

Exactly one temporary credential lease was created.

| Field | Value |
| --- | --- |
| Lease ID | `lease.c2ac15e88e314276b3e930a183450bc5` |
| TTL | `300000` ms |
| Active leases before create | `0` |
| Active leases after create | `1` |
| Projected auth file present | `true` |
| Projected credential count | `1` |
| Environment keys delivered | `HERMES_HOME` |
| Durable store mounted into inference worker | `false` |
| Automatic refresh | `false` |
| Refresh writeback | `false` |
| Provider dispatches during create | `0` |

Resolved committed-code profile facts:

| Field | Value |
| --- | --- |
| Provider profile | `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1` |
| Worker profile | `worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1` |
| Worker binding state | `ready_for_inference_gate` |
| Provider | `openai-codex` |
| Authentication | `chatgpt_oauth` |
| Transport | `codex_responses` |
| Tools, hosted tools, MCP | disabled |
| Application streaming | disabled |

## Tool-Free GPT-5.5 Inference

The inference child ran in a separate one-shot container with only the temporary lease root mounted. The durable credential store was not mounted into the inference worker.

Required request:

```text
System: Return only the exact literal requested by the user message. Do not add punctuation, explanation, Markdown or any other text. Do not call tools.
User: Reply with exactly: PEPPER_P15_M12_OK
```

Request posture:

| Field | Value |
| --- | --- |
| Model | `gpt-5.5` |
| Stream argument | `true` |
| Store argument | `false` |
| Maximum output token bound | `64` |
| Wire `max_output_tokens` present | `false` |
| Tools present | `false` |
| Tool choice present | `false` |
| Conversation history present | `false` |
| Images/files present | `false` / `false` |

The runtime-only worker used the source-native event consumer and made exactly one corrected streaming dispatch:

```python
stream_kwargs = dict(api_kwargs)
stream_kwargs["stream"] = True
event_stream = client.responses.create(**stream_kwargs)
final = _consume_codex_event_stream(event_stream, model="gpt-5.5")
```

Single-call enforcement:

| Counter | Value |
| --- | ---: |
| `client.responses.create` calls | `1` |
| Provider dispatches | `1` |
| Inference calls | `1` |
| Automatic retries | `0` |
| Fallback calls | `0` |
| Model-list calls | `0` |
| Usage endpoint calls | `0` |
| Tool calls | `0` |
| MCP calls | `0` |
| Provider-wire events consumed | `true` |
| Provider-wire event count | `15` |
| Event stream closed | `true` |

Result validation:

| Field | Value |
| --- | --- |
| Result state | `completed` |
| Terminal status | `completed` |
| Output kind | `text` |
| Output text | `PEPPER_P15_M12_OK` |
| Exact trimmed match | `true` |
| Request duration | `2916` ms |
| Cancellation armed/triggered | `true` / `false` |
| Stream chunks exposed to external caller | `0` |
| Partial text persisted | `false` |
| Raw terminal response persisted | `false` |
| Reasoning trace persisted | `false` |
| Provider headers retained | `false` |

After result validation, the lease was released through `release_openai_codex_credential_lease`.

| Field | Value |
| --- | --- |
| Active leases before release | `1` |
| Release status | `released` |
| Removed item count | `15` |
| Residue item count | `0` |
| Active leases after release | `0` |
| Projected auth files after cleanup | `0` |

## Stability

The dashboard remained running after the leased inference and lease release. A 300-second stability window was run against the local dashboard runtime.

| Field | Value |
| --- | ---: |
| Configured duration | `300` seconds |
| Observed elapsed time | `306` seconds |
| Poll interval | `15` seconds |
| Expected poll count | `20` |
| Actual poll count | `20` |
| Failed polls | `0` |

Each poll verified container running, container health `healthy`, restart count `0`, direct dashboard status `200`, relay status `200`, Windows host status `200`, and matching status-body hashes across direct, relay, and host endpoints. Provider activity, OAuth activity, and worker activity during stability were all `0`.

## Shutdown, Restart, And Residue

Cycle-one controlled shutdown passed with `docker compose stop --timeout 15`, relay graceful shutdown, dashboard child termination, `relay_exit code=0`, and `docker compose down --remove-orphans --timeout 15`.

Cycle-one residue after `down`: P15.M12 containers `0`, P15.M12 networks `0`, host port `19120` listeners `0`, and active credential leases `0`.

Restart cycle passed from clean residue: `docker compose up -d`, container `running/healthy`, restart count `0`, host status `200`, and browser/SPA acceptance passed again through `http://127.0.0.1:19120`. The restart-cycle browser probe fetched the same CSS and JavaScript asset hashes as cycle one.

Final controlled shutdown after restart passed with `docker compose stop --timeout 15`, relay graceful shutdown, dashboard child termination, `relay_exit code=0`, and `docker compose down --remove-orphans --timeout 15`.

Final residue:

| Check | Count |
| --- | ---: |
| P15.M12 containers | `0` |
| P15.M12 networks | `0` |
| Host port `19120` listeners | `0` |
| Active credential leases | `0` |
| Projected auth files | `0` |
| Bad runtime directory modes | `0` |
| Repository tracked changes before governance record | `0` |

## Runtime Evidence

Secret-free runtime evidence was retained outside Git under the P15.M12 runtime root.

| Evidence file | Purpose |
| --- | --- |
| `runtime-manifest.json` | P15.M12 runtime summary and hashes |
| `evidence/credential_preflight.json` | secret-free durable credential status |
| `evidence/lease_create.json` | lease creation and profile resolution |
| `evidence/lease_ref.json` | pathless lease reference used for cleanup |
| `evidence/streaming_inference.json` | single streaming inference result |
| `evidence/lease_release.json` | lease cleanup result |
| `evidence/browser_acceptance.json` | cycle-one browser/SPA acceptance |
| `evidence/stability.json` | 300-second stability window |
| `evidence/browser_acceptance_restart.json` | restart-cycle browser/SPA acceptance |
| `evidence/shutdown_residue.json` | shutdown, restart, and residue facts |

All retained P15.M12 JSON evidence parsed successfully. No runtime `auth.json` remained under the P15.M12 runtime root after lease cleanup. Targeted token-shaped scans over retained P15.M12 `evidence` and `scripts` found `0` JWTs, bearer-token values, concrete `access_token` values, concrete `refresh_token` values, verification URLs, device codes, user codes, cookies, session tokens, or Cloudflare clearance values.

A broad scan of `dashboard-home` found packaged static skill documentation containing placeholder authorization examples such as `$GITHUB_TOKEN`, `$AIRTABLE_API_KEY`, and `sk-xxxxxxxxxxxxxxxxxxxx`. These are static non-runtime documentation examples, not P15.M12 secrets, not retained evidence, and not credential material.

## Counters

P15.M12 counters:

| Counter | Value |
| --- | ---: |
| Additional OAuth attempts | `0` |
| Additional OAuth completions | `0` |
| Credential promotions | `0` |
| Temporary credential leases created | `1` |
| Temporary credential leases released | `1` |
| Provider dispatches | `1` |
| Successful inferences | `1` |
| Automatic retries | `0` |
| Automatic fallback calls | `0` |
| Model-list calls | `0` |
| Usage endpoint calls | `0` |
| Tool calls | `0` |
| MCP calls | `0` |
| Image rebuilds | `0` |
| Image pulls | `0` |
| Image pushes | `0` |

Cumulative accepted OpenAI Codex live inference history after P15.M12:

| Counter | Value |
| --- | ---: |
| P15.M11 provider dispatches | `1` |
| P15.M11 successful inferences | `0` |
| P15.M11A provider dispatches | `1` |
| P15.M11A successful inferences | `1` |
| P15.M12 provider dispatches | `1` |
| P15.M12 successful inferences | `1` |

## Closure

P15.M12 proves at validation time that the retained Pepper Hermes 0.19 local runtime can start through Docker Compose, publish the dashboard only on Windows loopback, serve the SPA/browser shell and assets, run a bounded 300-second stability window, complete exactly one leased tool-free GPT-5.5 OpenAI Codex streaming inference returning `PEPPER_P15_M12_OK`, release the lease, shut down cleanly, restart from clean residue, and finish with no P15.M12 Docker, port, lease, or projected credential residue.

P15.M12 does not prove future provider entitlement, future quota, future token refresh, remote revocation status outside the validated request, multi-request worker behavior, tools, MCP, public-network exposure, or VPS deployment readiness.

No product, test, implementation, dependency, Dockerfile, repository Compose, manifest, modification-register, baseline, workspace, or desktop source file was changed by P15.M12. The only tracked repository change authorized by this closure is this governance record.
