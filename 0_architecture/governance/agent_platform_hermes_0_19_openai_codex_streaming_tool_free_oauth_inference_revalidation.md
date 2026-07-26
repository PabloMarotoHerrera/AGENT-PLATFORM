# Hermes 0.19 OpenAI Codex Streaming Tool-Free OAuth Inference Revalidation

Date: 2026-07-26

Final verdict: `hermes_0_19_openai_codex_streaming_tool_free_oauth_inference_revalidated_with_constraints`

## Ticket Authority

P15.M11A was authorized as a runtime-only corrective continuation after the accepted P15.M11 blocker `P15.M11-TRANSPORT-PROTOCOL-BLOCKED`.

P15.M11A authorized exactly one fresh OpenAI Codex device-code OAuth acquisition, one governed credential promotion, one temporary credential lease, one corrected `stream=true` Codex Responses dispatch, one tool-free GPT-5.5 inference, lease cleanup, and retention of one protected durable credential for P15.M12.

P15.M11A did not authorize product source changes, test changes, manifest changes, lock changes, Dockerfile changes, Compose changes, modification-register changes, baseline JSON changes, extra OAuth attempts, extra provider dispatches, automatic retries, fallback calls, tool execution, MCP calls, model-list calls, usage calls, staging, commits, or pushes.

## Repository State

| Field | Value |
| --- | --- |
| Repository root | `C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| HEAD | `06f22f759e156c56cff6ac68fb9ea6d8adb0eda1` |
| Remote | `origin/p15.m-hermes-0.19-migration` |
| Remote HEAD | `06f22f759e156c56cff6ac68fb9ea6d8adb0eda1` |
| HEAD equals remote | `true` |
| Index | empty before record creation |
| Tracked worktree | clean before record creation |
| Visible untracked task candidates | `0` before record creation |

Required P15.M10 prerequisite record:

`0_architecture/governance/agent_platform_hermes_0_19_docker_compose_local_pilot.md`

Required P15.M10 verdict:

`hermes_0_19_docker_compose_local_pilot_ready_with_constraints`

No P15.M11 success governance record existed before P15.M11A. No P15.M11A governance record existed before this record was created.

## Required Prerequisites

The following committed records were present in `HEAD`, tracked, locally unmodified, and unstaged:

| Record | Required verdict |
| --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_migration_authorization.md` | `hermes_0_19_migration_authorized_with_constraints` |
| `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closure.md` | `hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closed_with_constraints` |
| `0_architecture/governance/agent_platform_hermes_0_19_wsl2_development_architecture.md` | `hermes_0_19_wsl2_development_architecture_ready_with_constraints` |
| `0_architecture/governance/agent_platform_hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repair.md` | `hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repaired_with_constraints` |
| `0_architecture/governance/agent_platform_hermes_0_19_dashboard_readonly_plugin_manifest_build_post_commit_integrity_closure.md` | `hermes_0_19_dashboard_readonly_plugin_manifest_build_post_commit_integrity_closed_with_constraints` |
| `0_architecture/governance/agent_platform_hermes_0_19_docker_desktop_loopback_port_publication_compatibility_assessment.md` | `hermes_0_19_docker_desktop_loopback_port_publication_compatibility_assessed_with_constraints` |
| `0_architecture/governance/agent_platform_hermes_0_19_docker_compose_local_pilot.md` | `hermes_0_19_docker_compose_local_pilot_ready_with_constraints` |

## Canonical Product Integrity

The canonical integrity utility was run before live activity:

```text
python "10_scripts/governance/pepper_baseline_integrity.py" --repo-root "." --product-root "2_products/pepper-agent" --mode all --format json
```

Required identities matched:

| Identity | Files | Bytes | SHA256 |
| --- | ---: | ---: | --- |
| Candidate | `6768` | `149234356` | `a71af0be624cb3f00b37d651248717c38f5bed18e460c6f159636c75a8875df3` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | n/a | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

The governance integrity test suite was run before live activity:

```text
python -m unittest discover -s "12_tests/governance" -p "test_pepper_baseline_integrity.py"
```

Result: `14` tests, `0` failures, `0` errors.

## Prior P15.M11 Failure

Retained bounded secret-free P15.M11 failure evidence was inspected from:

`/home/pablo/.local/share/pepper/pilots/p15-m11-06f22f759e15/evidence/transport_protocol_blocked_rollback.json`

Accepted P15.M11 history:

| Counter | Value |
| --- | ---: |
| OAuth attempts | `2` |
| OAuth completions | `1` |
| Provider dispatches | `1` |
| Successful inferences | `0` |
| Automatic retries | `0` |
| Additional provider calls | `0` |

Accepted P15.M11 failure:

| Field | Value |
| --- | --- |
| HTTP status | `400` |
| Safe provider message | `Stream must be set to true` |
| Failure class | `transport_protocol` |
| Recorded provider error class | `http_400_stream_must_be_true` |
| Blocker | `P15.M11-TRANSPORT-PROTOCOL-BLOCKED` |

Accepted P15.M11 rollback:

| Field | Value |
| --- | --- |
| Governed credential store present after rollback | `false` |
| Active leases after rollback | `0` |
| Success governance record created | `false` |
| Secret material retained in evidence | `false` |

Conclusion: the P15.M11 OAuth credential was valid enough to reach the Codex backend. The request was rejected before inference because the runtime-only probe did not use the required streaming transport. P15.M11 did not prove GPT-5.5 entitlement.

## Source-Native Streaming Authority

Committed source inspected:

`2_products/pepper-agent/agent/codex_runtime.py`

Required source facts were present:

| Source fact | Evidence |
| --- | --- |
| `run_codex_stream` sets `stream=True` | `stream_kwargs = dict(api_kwargs)` then `stream_kwargs["stream"] = True` |
| Responses dispatch uses corrected kwargs | `event_stream = active_client.responses.create(**stream_kwargs)` |
| Source-native event consumer | `_consume_codex_event_stream(...)` |
| Terminal event handling | `response.completed`, `response.incomplete`, and `response.failed` handled |
| Event stream close | `close_fn = getattr(event_stream, "close", None)` then `close_fn()` when callable |

P15.M11A did not modify this source.

P15.M11A used provider-wire streaming. Application-level streaming remained disabled: no stream chunks were exposed to an external caller, no partial output was persisted, and only the final bounded text was retained.

## Retained Runtime Foundation

Required retained image:

| Field | Value |
| --- | --- |
| Tag | `pepper-agent:p15-m10-990d153cd370` |
| Image ID | `sha256:8e7d45adab5b5fa4b34a7c196929490521ac39d2d909e54d4866ddd772eebcfd` |
| OS | `linux` |
| Architecture | `amd64` |

Image rebuilds: `0`. Image pulls: `0`. Image pushes: `0`.

Linux-native checkout:

| Field | Value |
| --- | --- |
| Path | `/home/pablo/src/pepper/agent-platform` |
| Filesystem | Linux-native |
| Branch | `p15.m-hermes-0.19-migration` |
| HEAD | `06f22f759e156c56cff6ac68fb9ea6d8adb0eda1` |
| Origin | `06f22f759e156c56cff6ac68fb9ea6d8adb0eda1` |
| HEAD equals Windows HEAD | `true` |
| HEAD equals origin | `true` |
| Tracked worktree | clean |

## Runtime Root And Collision Gate

P15.M11A runtime root:

`/home/pablo/.local/share/pepper/pilots/p15-m11a-06f22f759e15`

Required runtime directories were created with mode `0700`:

`scripts`, `evidence`, `logs`, `acquisition`, and `leases`.

Governed credential parent:

`/home/pablo/.local/share/pepper/hermes-home/agent-platform/provider-credentials`

Required collision state before the new OAuth attempt:

| Field | Value |
| --- | --- |
| Governed store present | `false` |
| Acquisition store present | `false` |
| Active leases | `0` |
| P15.M11 containers | `0` |
| P15.M11A containers | `0` |
| P15.M11 networks | `0` |
| P15.M11A networks | `0` |

No Codex CLI state, VS Code credentials, browser storage, Windows Credential Manager, or unrelated Hermes profiles were inspected.

## Human OAuth Authorization

P15.M11A OAuth attempt count: `1`.

Cumulative OAuth attempt number: `3`.

The fixed command was used:

```text
python -m hermes_cli.main auth add openai-codex --type oauth
```

The acquisition used no shell, no custom endpoint, no custom client ID, no custom scope, no custom redirect, and no API key.

The verification URL and short-lived device code were displayed in the human-visible execution surface, followed by:

```text
P15.M11A HUMAN ACTION REQUIRED
```

The OAuth flow completed successfully. The verification URL, device code, account identity, browser cookies, authorization headers, access token, and refresh token were not written to tracked files, evidence files, the runtime manifest, or this governance record.

## Acquisition And Governed Promotion

The isolated acquisition store was validated in memory and promoted through:

`promote_openai_codex_oauth_credential`

Required acquisition facts:

| Field | Value |
| --- | --- |
| Provider | `openai-codex` |
| Credential count | `1` |
| Auth type | `oauth` |
| Source | `manual:device_code` |
| Base URL | `https://chatgpt.com/backend-api/codex` |
| Access-token presence metadata | `true` |
| Refresh-token presence metadata | `true` |
| Expiry known | `true` |
| Acquisition root removed after promotion | `true` |
| Acquisition removed item count | `17` |
| Staging residue | `0` |

Required governed shape:

| Field | Value |
| --- | --- |
| Active provider | `openai-codex` |
| Providers object | empty |
| Credential pool provider | `openai-codex` |
| Credential count | `1` |
| Credential ID | `openai-codex.primary` |
| Label | `AGENT PLATFORM OpenAI Codex OAuth` |
| Source | `manual:device_code` |
| Base URL | `https://chatgpt.com/backend-api/codex` |

Promotion posture: exclusive create `true`; merge `false`; overwrite `false`.

Credential protection after success:

| Path role | Mode |
| --- | --- |
| Governed store directory | `0700` |
| Governed auth file | `0600` |

## Provider And Worker Profiles

Resolved provider profile:

`provider.openai-codex.chatgpt-oauth.gpt-5.5.v1`

Resolved worker profile:

`worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1`

Required profile facts:

| Field | Value |
| --- | --- |
| Provider | `openai-codex` |
| Authentication | `chatgpt_oauth` |
| Endpoint | `https://chatgpt.com/backend-api/codex` |
| Model | `gpt-5.5` |
| Transport | `codex_responses` |
| Tools | disabled |
| Hosted tools | disabled |
| MCP | disabled |
| Automatic retry | disabled |
| Automatic fallback | disabled |
| Persistent memory | disabled |
| Conversation history | disabled |
| Application streaming | disabled |

Provider-wire streaming was required and verified; this does not contradict the application-streaming prohibition.

## Credential Lease

Exactly one temporary credential lease was created.

| Field | Value |
| --- | --- |
| TTL | `300000` ms |
| Active leases before | `0` |
| Active leases during inference | `1` |
| Credential count in projection | `1` |
| Durable store mounted into worker | `false` |
| Automatic refresh | `false` |
| Refresh writeback | `false` |

The inference worker received only the temporary projected `HERMES_HOME`, not the durable store.

After successful result validation, the lease was released through `release_openai_codex_credential_lease`.

Lease cleanup:

| Field | Value |
| --- | --- |
| Release status | `released` |
| Removed item count | `4` |
| Residue item count | `0` |
| Active leases after cleanup | `0` |
| Projected auth files after cleanup | `0` |

## Corrected Tool-Free Request

Required system instruction:

```text
Return only the exact literal requested by the user message. Do not add punctuation, explanation, Markdown or any other text. Do not call tools.
```

Required user content:

```text
Reply with exactly: PEPPER_P15_M11_OK
```

Request posture:

| Field | Value |
| --- | --- |
| Model | `gpt-5.5` |
| Stream | `true` |
| Store | `false` |
| Maximum output token bound | `64` |
| Tools | absent |
| Tool choice | absent |
| Conversation history | absent |
| Images | absent |
| Files | absent |
| Fallback | absent |
| Custom model | absent |
| Custom endpoint | absent |

The committed Codex backend transport omits a wire `max_output_tokens` field for this backend; P15.M11A enforced the `64` output-token bound at the worker/request-policy level and made no additional provider dispatch.

## Corrected Single-Call Seam

The runtime-only corrected seam used the source-native pattern without calling the retry-capable `run_codex_stream` helper:

```python
stream_kwargs = dict(api_kwargs)
stream_kwargs["stream"] = True
event_stream = client.responses.create(**stream_kwargs)
final = _consume_codex_event_stream(
    event_stream,
    model="gpt-5.5",
)
```

Single-call enforcement:

| Field | Value |
| --- | --- |
| `client.responses.create` calls | `1` |
| `stream` argument | `true` |
| Provider dispatches | `1` |
| Inference calls | `1` |
| Automatic retries | `0` |
| Fallback dispatches | `0` |
| Model-list calls | `0` |
| Usage endpoint calls | `0` |
| Tool calls | `0` |
| MCP calls | `0` |
| Provider-wire events consumed | `true` |
| Terminal status | `completed` |
| Finish reason | `stop` |
| Event stream closed | `true` |

No `responses.create` call was made without `stream=true`. No second `responses.create` call was made. No `responses.stream`, `chat.completions.create`, model-list endpoint, or usage endpoint was called.

## Result Validation

Required result:

| Field | Value |
| --- | --- |
| State | `completed` |
| Output kind | `text` |
| Output text | `PEPPER_P15_M11_OK` |
| Exact trimmed match | `true` |
| Tool calls | `0` |
| Failure | none |
| Raw provider response retained | `false` |
| Reasoning trace retained | `false` |
| Provider headers retained | `false` |
| Request duration | `2330` ms |
| Cancellation armed | `true` |
| Cancellation triggered | `false` |

Exact comparison passed:

```text
trimmed output == PEPPER_P15_M11_OK
```

## Live Conclusions

P15.M11A proves only the following at validation time:

| Conclusion | Value |
| --- | --- |
| OAuth device authorization | successful |
| Local token pair | valid for governed promotion |
| Remote token validity | verified for this request |
| Provider reachability | verified at validation time |
| Endpoint | `https://chatgpt.com/backend-api/codex` |
| Transport | `codex_responses_streaming` |
| Provider-wire streaming | verified |
| Application streaming | disabled |
| Model | `gpt-5.5` |
| Model entitlement | verified for the authenticated account at validation time |
| Tool-free inference | passed |

P15.M11A does not prove future entitlement, future quota, token refresh, remote revocation, multi-request worker behavior, tools, MCP, complete Pepper local acceptance, or VPS deployment readiness.

## Counters

P15.M11 history:

| Counter | Value |
| --- | ---: |
| OAuth attempts | `2` |
| OAuth completions | `1` |
| Provider dispatches | `1` |
| Successful inferences | `0` |
| Blocker | `P15.M11-TRANSPORT-PROTOCOL-BLOCKED` |

P15.M11A:

| Counter | Value |
| --- | ---: |
| OAuth attempts | `1` |
| OAuth completions | `1` |
| Provider dispatches | `1` |
| Successful inferences | `1` |
| Stream | `true` |
| Result | `PEPPER_P15_M11_OK` |

Cumulative:

| Counter | Value |
| --- | ---: |
| OAuth attempts | `3` |
| OAuth completions | `2` |
| Provider dispatches | `2` |
| Successful inferences | `1` |

## Secret Safety

Retained governance/evidence counts:

| Secret-bearing material | Retained count |
| --- | ---: |
| Access tokens | `0` |
| Refresh tokens | `0` |
| Authorization headers | `0` |
| Verification URLs | `0` |
| Device codes | `0` |
| Account identifiers | `0` |
| JWT claims | `0` |
| Provider headers | `0` |
| Raw provider responses | `0` |
| Encrypted reasoning | `0` |
| Reasoning traces | `0` |

Allowed retained result:

```text
PEPPER_P15_M11_OK
```

The durable governed credential is intentionally retained for P15.M12 in the protected store. It is not reproduced in evidence, logs, this record, or tracked repository content.

## Cleanup And Retained State

Successful cleanup state:

| Field | Value |
| --- | --- |
| OAuth containers after | `0` |
| Inference containers after | `0` |
| P15.M11A networks after | `0` |
| Worker/provider processes after | `0` |
| Acquisition root after | absent |
| Active leases after | `0` |
| Projected auth files after | `0` |
| Projected `HERMES_HOME` after | absent |

Retained:

| Item | State |
| --- | --- |
| Protected governed durable credential | retained |
| Retained Pepper image | retained |
| Linux checkout | clean |
| Secret-free evidence and runtime manifest | retained outside Git |

Runtime manifest created outside Git:

`/home/pablo/.local/share/pepper/pilots/p15-m11a-06f22f759e15/runtime-manifest.json`

## Repository Candidate Set

Created tracked candidate:

```text
0_architecture/governance/agent_platform_hermes_0_19_openai_codex_streaming_tool_free_oauth_inference_revalidation.md
```

Candidate set constraints:

| Field | Value |
| --- | --- |
| Candidate files | `1` |
| Unexpected candidates | `0` |
| Product files modified | `0` |
| Tests modified | `0` |
| Modification register modified | `false` |
| Baseline modified | `false` |
| Manifests modified | `0` |
| Locks modified | `0` |
| Dockerfile modified | `false` |
| Repository Compose modified | `false` |
| Runtime scripts tracked | `0` |
| Graphify modified | `false` |

No modification-register row is required.

## Residual Constraints

Desktop remains disabled. Workspace remains disabled. VPS deployment remains unauthorized. Tools remain unvalidated. MCP remains unvalidated. Credential refresh remains unexercised. Remote revocation remains unsupported or unverified. Future GPT-5.5 entitlement and quota are not guaranteed.

## P15.M12 Handoff

P15.M12 may begin only after P15.M11A is accepted, staged by the human, committed, and pushed.

P15.M12 must create a new temporary credential lease and must not mount the durable store directly into general services.

P15.M12 remains the complete local acceptance gate.
