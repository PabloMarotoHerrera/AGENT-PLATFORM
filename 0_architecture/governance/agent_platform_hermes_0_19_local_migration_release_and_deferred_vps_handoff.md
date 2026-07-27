# Hermes 0.19 Local Migration Release And Deferred VPS Handoff

Date: 2026-07-27

Final verdict: `hermes_0_19_local_migration_release_and_deferred_vps_handoff_closed_with_constraints`

## Ticket Authority

P15.MR closes the local-only Hermes Agent 0.19.0-derived Pepper migration release after P15.M12 complete local runtime acceptance and P15.M13 external Linux VPS architecture definition.

This record promotes the accepted local Pepper baseline as the current governed local migration result, defers the external Linux VPS execution lane, records the local integration target, preserves product identity and validation evidence, and hands future product activation or implementation-readiness work back to the local Pepper roadmap.

This P15.MR is a governance release/handoff record only. It does not provision a VPS, contact a remote host, run SSH, transfer images, start Docker containers or networks, run OAuth, create a credential lease, call a provider, perform inference, run Graphify, stage files, commit, push, tag, merge, rebase, stash, reset, clean, or mutate product/runtime/source/test files.

## Repository Gate

| Field | Value |
| --- | --- |
| Repository root | `C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| Starting HEAD | `fff8e3627448c4c40018731759309c7661e86b91` |
| Upstream | `origin/p15.m-hermes-0.19-migration` |
| Upstream HEAD | `fff8e3627448c4c40018731759309c7661e86b91` |
| HEAD equals upstream | `true` |
| Index before P15.MR record | empty |
| Tracked worktree before P15.MR record | clean |
| Visible untracked task candidates before record | `0` |
| P15.MR record present before creation | `false` |

Resolved P15.M13 authority:

| Field | Value |
| --- | --- |
| P15.M13 commit | `fff8e3627448c4c40018731759309c7661e86b91` |
| P15.M13 commit message | `P15.M13 Define external Linux VPS architecture` |
| P15.M13 commit is ancestor of HEAD | `true` |
| HEAD equals P15.M13 commit | `true` |
| Post-P15.M13 commits before this record | `0` |
| P15.M13 committed verdict | `hermes_0_19_external_linux_vps_architecture_ready_with_constraints` |
| P15.M13 commit product mutations | `0` |
| P15.M13 commit governance files | `1` |

P15.M13 introduced exactly:

```text
0_architecture/governance/agent_platform_hermes_0_19_external_linux_vps_architecture.md
```

## Required Local Prerequisites

Each prerequisite record was tracked, committed, present in `HEAD`, locally unmodified, and unstaged before this record was created.

| Record | Required verdict |
| --- | --- |
| `agent_platform_hermes_0_19_migration_authorization.md` | `hermes_0_19_migration_authorized_with_constraints` |
| `agent_platform_hermes_0_19_workspace_adoption_assessment.md` | `hermes_0_19_workspace_adoption_assessment_ready_with_constraints` |
| `agent_platform_hermes_0_19_product_baseline.md` | local Hermes 0.19.0-derived Pepper product baseline defined |
| `agent_platform_hermes_0_19_product_baseline_commit_finalization.md` | committed baseline finalized |
| `agent_platform_hermes_0_19_license_notice_reconciliation.md` | license and notice reconciliation recorded |
| `agent_platform_hermes_0_19_dependency_lock_reconciliation.md` | dependency and lock reconciliation recorded |
| `agent_platform_hermes_0_19_desktop_workspace_productization_decision.md` | Desktop and Workspace productization decision recorded |
| `agent_platform_hermes_0_19_integrated_interaction_surface_reconciliation.md` | interaction surface reconciliation recorded |
| `agent_platform_hermes_0_19_pepper_product_identity_post_commit_integrity_closure.md` | `hermes_0_19_pepper_product_identity_post_commit_integrity_closed_with_constraints` |
| `agent_platform_hermes_0_19_governed_runtime_adapter_post_commit_integrity_closure.md` | `hermes_0_19_governed_runtime_adapter_post_commit_integrity_closed_with_constraints` |
| `agent_platform_hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closure.md` | `hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closed_with_constraints` |
| `agent_platform_hermes_0_19_wsl2_development_architecture.md` | `hermes_0_19_wsl2_development_architecture_ready_with_constraints` |
| `agent_platform_hermes_0_19_docker_desktop_loopback_port_publication_compatibility_assessment.md` | `hermes_0_19_docker_desktop_loopback_port_publication_compatibility_assessed_with_constraints` |
| `agent_platform_hermes_0_19_docker_compose_local_pilot.md` | `hermes_0_19_docker_compose_local_pilot_ready_with_constraints` |
| `agent_platform_hermes_0_19_openai_codex_streaming_tool_free_oauth_inference_revalidation.md` | `hermes_0_19_openai_codex_streaming_tool_free_oauth_inference_revalidated_with_constraints` |
| `agent_platform_hermes_0_19_complete_local_runtime_acceptance_closure.md` | `hermes_0_19_complete_local_runtime_acceptance_closed_with_constraints` |
| `agent_platform_hermes_0_19_external_linux_vps_architecture.md` | `hermes_0_19_external_linux_vps_architecture_ready_with_constraints` |

## Local Release Baseline

P15.MR accepts the following P15.M12 local-runtime baseline as the local migration release result.

| Baseline item | Accepted value |
| --- | --- |
| Strategic local mode | WSL2 plus Docker Compose |
| Fallback local mode | WSL2 native |
| Product | Pepper |
| Product version | `0.1.0-dev` |
| Upstream baseline | Hermes Agent `0.19.0` |
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

P15.MR does not rerun the accepted live local runtime. P15.MR preserves the P15.M12 evidence as accepted authority and runs only local regression/integrity validation.

## Canonical Product Integrity

Pre-record integrity utility result:

| Identity | Files | Bytes | SHA256 |
| --- | ---: | ---: | --- |
| Candidate | `6768` | `149234356` | `a71af0be624cb3f00b37d651248717c38f5bed18e460c6f159636c75a8875df3` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | n/a | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Command:

```text
python "10_scripts/governance/pepper_baseline_integrity.py"
```

Result: identities matched the accepted baseline.

Governance integrity command:

```text
python -m pytest -q "12_tests/governance/test_pepper_baseline_integrity.py" -p no:cacheprovider
```

Result: `14 passed in 0.05s`.

Canonical product authority:

| Path | Tracked files | P15.MR posture |
| --- | ---: | --- |
| `2_products/pepper-agent` | `6769` | canonical editable Pepper product source |
| `2_products/hermes-agent` | `6246` | predecessor/reference product source retained by existing repository history |
| `4_external/sources` | `0` | no tracked external-source authority |

The canonical product identity remains unchanged by P15.MR.

## Regression Validation

P15.MR refreshed the local unit and governance regression gates without live runtime startup, OAuth, provider dispatch, credential lease creation, remote access, Graphify, or product edits.

| Gate | Command posture | Result |
| --- | --- | --- |
| Product config regression | `python -m pytest -q tests/hermes_cli/test_agent_platform_product_config.py -p no:cacheprovider` | `10 passed in 0.31s` |
| Provider, credential and worker contracts | explicit `test_agent_platform_provider_*.py` file expansion plus `test_agent_platform_openai_codex_oauth_acquisition.py` | `119 passed, 3 warnings in 1.77s` |
| Runtime adapter targeted rerun after transient failures | two failing tests rerun by exact node IDs | `2 passed in 4.17s` |
| Runtime adapter full rerun | explicit `test_agent_platform_runtime_*.py` file expansion | `148 passed in 14.63s` |

The first current runtime refresh used a glob form that `cmd.exe` did not expand and therefore collected no tests. The corrected PowerShell-expanded full runtime refresh initially observed two transient process-termination observations: `PROCESS-001` reported `unexpected_exit_code` with `status=unknown` and `exit_code=None`, and one graceful-shutdown lifecycle assertion observed `FAILED` instead of `STOPPED`. The exact failing tests passed immediately on targeted rerun, and the full runtime suite then passed. P15.MR classifies this as the previously observed Windows process terminal-observation race, not a product mutation.

Expected provider warnings were limited to Pydantic protected namespace warnings for `model_id`, `model_policy`, and `model_list_calls_per_request_maximum`.

Runtime-adapter count reconciliation:

Canonical P15.M12 runtime-suite command:

```cmd
python -m pytest -q tests/hermes_cli/test_agent_platform_runtime_adapter_conformance.py tests/hermes_cli/test_agent_platform_runtime_adapter_contracts.py tests/hermes_cli/test_agent_platform_runtime_adapter_failure_conformance.py tests/hermes_cli/test_agent_platform_runtime_adapter_integration.py tests/hermes_cli/test_agent_platform_runtime_audit_normalization.py tests/hermes_cli/test_agent_platform_runtime_environment.py tests/hermes_cli/test_agent_platform_runtime_event_normalization.py tests/hermes_cli/test_agent_platform_runtime_lifecycle_control.py tests/hermes_cli/test_agent_platform_runtime_listener_discovery.py tests/hermes_cli/test_agent_platform_runtime_path_containment.py tests/hermes_cli/test_agent_platform_runtime_process_owner.py tests/hermes_cli/test_agent_platform_runtime_profiles.py tests/hermes_cli/test_agent_platform_runtime_readiness.py tests/hermes_cli/test_agent_platform_runtime_rollback.py tests/hermes_cli/test_agent_platform_runtime_workspace.py -p no:cacheprovider
```

P15.MR runtime-suite command:

```cmd
powershell -NoProfile -Command "$files = Get-ChildItem -Path 'tests/hermes_cli' -Filter 'test_agent_platform_runtime_*.py' | Sort-Object Name | ForEach-Object { $_.FullName }; python -m pytest -q @files -p no:cacheprovider"
```

Both commands collect the same 15 runtime test files: `test_agent_platform_runtime_adapter_conformance.py`, `test_agent_platform_runtime_adapter_contracts.py`, `test_agent_platform_runtime_adapter_failure_conformance.py`, `test_agent_platform_runtime_adapter_integration.py`, `test_agent_platform_runtime_audit_normalization.py`, `test_agent_platform_runtime_environment.py`, `test_agent_platform_runtime_event_normalization.py`, `test_agent_platform_runtime_lifecycle_control.py`, `test_agent_platform_runtime_listener_discovery.py`, `test_agent_platform_runtime_path_containment.py`, `test_agent_platform_runtime_process_owner.py`, `test_agent_platform_runtime_profiles.py`, `test_agent_platform_runtime_readiness.py`, `test_agent_platform_runtime_rollback.py`, and `test_agent_platform_runtime_workspace.py`.

| Runtime result | Passed | Skipped | Failed |
| --- | ---: | ---: | ---: |
| Canonical P15.M12 | `143` | `5` | `0` |
| P15.MR observed | `148` | `0` | `0` |

Previously skipped test IDs:

| Test ID | P15.M12 skip reason | P15.MR deterministic enabling condition |
| --- | --- | --- |
| `tests/hermes_cli/test_agent_platform_runtime_path_containment.py::test_trusted_base_root_rejects_symlink_and_reparse_point` | `host does not allow directory symlink creation` | Current host allowed the directory symlink creation used by the test setup, so the skip guard did not trigger and the containment assertion executed and passed. |
| `tests/hermes_cli/test_agent_platform_runtime_path_containment.py::test_symlink_redirect_rejected_even_when_target_is_inside_root` | `host does not allow directory symlink creation` | Current host allowed the directory symlink creation used by the test setup, so the skip guard did not trigger and the containment assertion executed and passed. |
| `tests/hermes_cli/test_agent_platform_runtime_rollback.py::test_oversized_and_symlink_marker_are_rejected_without_deleting` | `symlink creation unavailable` | Current host allowed the symlink marker creation used by the rollback test setup, so the skip guard did not trigger and the rollback assertion executed and passed. |
| `tests/hermes_cli/test_agent_platform_runtime_rollback.py::test_safe_preflight_rejects_redirects_special_files_depth_and_entry_bounds` | `symlink creation unavailable` | Current host allowed the symlink creation used by the safe-preflight test setup, so the skip guard did not trigger and the rollback preflight assertion executed and passed. |
| `tests/hermes_cli/test_agent_platform_runtime_workspace.py::test_workspace_paths_are_contained_and_symlink_workspace_root_rejected` | `host does not allow directory symlink creation` | Current host allowed the directory symlink creation used by the test setup, so the skip guard did not trigger and the workspace containment assertion executed and passed. |

Count-delta controls:

| Control | Value |
| --- | ---: |
| Product source changes | `0` |
| Test changes | `0` |
| Skip or xfail marker changes | `0` |
| Timeout changes | `0` |
| Expected-result changes | `0` |

Final runtime-count classification: `previously_skipped_cases_now_deterministically_executed`.

## Retained Image And Credential Posture

Retained local image authority from P15.M10 through P15.M12:

| Field | Value |
| --- | --- |
| Image tag | `pepper-agent:p15-m10-990d153cd370` |
| Image ID | `sha256:8e7d45adab5b5fa4b34a7c196929490521ac39d2d909e54d4866ddd772eebcfd` |
| Source commit | `990d153cd370f9f6289ff4ca61ff1a9f79e139dd` |
| Image OS/architecture | `linux/amd64` |
| Image rebuilds in P15.MR | `0` |
| Image pulls in P15.MR | `0` |
| Image pushes in P15.MR | `0` |

Post-image-source diff from `990d153cd370f9f6289ff4ca61ff1a9f79e139dd` to P15.M13 `HEAD` remained governance-only:

| Field | Value |
| --- | ---: |
| Commits after image source | `5` |
| Files changed | `5` |
| Insertions | `3126` |
| Product files changed | `0` |
| Test files changed | `0` |
| Runtime scripts tracked | `0` |

Those five files were exactly:

```text
0_architecture/governance/agent_platform_hermes_0_19_complete_local_runtime_acceptance_closure.md
0_architecture/governance/agent_platform_hermes_0_19_docker_compose_local_pilot.md
0_architecture/governance/agent_platform_hermes_0_19_docker_desktop_loopback_port_publication_compatibility_assessment.md
0_architecture/governance/agent_platform_hermes_0_19_external_linux_vps_architecture.md
0_architecture/governance/agent_platform_hermes_0_19_openai_codex_streaming_tool_free_oauth_inference_revalidation.md
```

The retained local credential root remains local-only:

```text
/home/pablo/.local/share/pepper/hermes-home/agent-platform/provider-credentials/openai-codex.primary
```

Secret-free metadata validated for this root before P15.MR record creation: configured `true`, durable store present and valid `true`, protection valid `true`, credential count `1`, token pair present `true`, directory mode `0700`, file mode `0600`, provider state present `false`, pool state present `true`, active provider matches `true`, source `manual device-code flow`, endpoint `https://chatgpt.com/backend-api/codex`, active leases `0`.

The P15.M11A/P15.M12 local credential is not remote deployment material and must not be copied to a VPS.

## Branch Integration Target

Local Git metadata resolves the integration target as `origin/main`.

| Field | Value |
| --- | --- |
| Remote default branch | `origin/main` |
| Local merge base | `fea7d3963a598b848768671e00d5bad8065a4421` |
| Merge-base commit message | `P15.3 Define bounded OpenAI Codex worker profile` |
| Commits ahead of `origin/main` | `34` |
| Integration action performed by P15.MR | `none` |

P15.MR records the target only. It does not merge, rebase, fast-forward, tag, stage, commit, push, open a PR, or mutate branch topology.

## Migration Delta Aggregates

Bounded local diff from `origin/main` to P15.M13 `HEAD`:

| Aggregate | Value |
| --- | ---: |
| Files changed | `6813` |
| Status `A` | `6812` |
| Status `M` | `1` |
| Text files in numstat | `6714` |
| Binary files in numstat | `99` |
| Insertions | `2454959` |
| Deletions | `0` |

Top-level path distribution:

| Path | Changed files |
| --- | ---: |
| `.gitattributes` | `1` |
| `.gitignore` | `1` |
| `0_architecture` | `38` |
| `10_scripts` | `2` |
| `12_tests` | `2` |
| `2_products` | `6769` |

The only modified existing file in the branch delta is `.gitignore`. All other branch-delta files are additions relative to `origin/main`.

## Deferred VPS Lane

P15.M13 defines Mode D as `External Linux VPS + Docker Compose`; P15.MR does not activate Mode D.

Deferred remote tickets:

| Ticket | Frozen scope | P15.MR disposition |
| --- | --- | --- |
| P15.M14 | External Linux VPS Provider-Null Infrastructure Pilot | deferred; blocked on human VPS/SSH facts and explicit remote-action authority |
| P15.M15 | Remote Governed Credential and Bounded Provider Worker Pilot | deferred; remote OAuth, remote credential, lease and provider dispatch not authorized |
| P15.M16 | Remote Recovery, Rollback and Local-to-Remote Acceptance Closure | deferred; no remote restart, reboot, rollback or 24/7 acceptance evidence claimed |

P15.M14 must not begin until the human supplies or confirms the VPS provider, public IP or hostname, Linux distribution and exact release, x86_64 architecture, administrative SSH username, SSH port, local private-key path or approved SSH-agent identity, expected host-key fingerprint through a trusted channel, authorized administration source IP or network, provider firewall availability, rescue-console availability, allocated vCPU, allocated RAM, allocated disk, and explicit remote-action authority.

VPS deployment is not required to accept the local Pepper migration release. The VPS lane remains required before declaring Pepper 24/7 operational.

## Update Lane Deferral

P15.M17, P15.M18, and P15.M19 remain future update-lifecycle work, deferred when supported by existing canonical migration authority, and are not started by P15.MR.

| Ticket | Scope | P15.MR disposition |
| --- | --- | --- |
| P15.M17 | Governed upstream synchronization engine | deferred; no engine implementation or Git mutation |
| P15.M18 | One-click Pepper update surface | deferred; no frontend endpoint, credential, or Git authority |
| P15.M19 | Update and rollback acceptance drill | deferred; no update application or rollback drill |

P15.MR does not claim unattended update readiness, automatic upstream synchronization readiness, one-click update readiness, or update rollback acceptance.

## Original P15 Roadmap Reconciliation

Correct historical sequence:

```text
P15.0-P15.3
-> P15.1A
-> P15.4 paused
-> P15.U0
-> P15.U
-> P15.M
```

P15.U fixed these dispositions:

| Original item | Disposition |
| --- | --- |
| `P15_0` | `migrate` |
| `P15_1` | `migrate` |
| `P15_1A` | `retain_for_windows_fallback` |
| `P15_2` | `migrate` |
| `P15_3` | `migrate` |
| `P15_4` | `replace` |
| `P15_4_candidate` | `selectively_forward_port` |

Corrected original-roadmap reconciliation:

| Ticket | Title | Status |
| --- | --- | --- |
| P15.0 | Provider and Model Strategy | completed and forward-ported |
| P15.1 | Credential Delivery Boundary | completed and forward-ported |
| P15.1A | Windows Credential Store Protection Backend Correction | retained for Windows fallback |
| P15.2 | Provider Runtime Profile | completed and forward-ported |
| P15.3 | Bounded Worker Profile | completed and forward-ported |
| P15.4 | Tool-Free Inference Gate | completed by replacement |
| P15.5 | Usage, Cost and Timeout Accounting | next active ticket |
| P15.6 | Provider Failure and Retry Policy | pending |
| P15.7 | Single Worker Controlled Gate | pending |
| P15.R | Secure Worker Enablement Closure | pending |

P15.1A correction posture:

| Field | Value |
| --- | --- |
| Title | Windows Credential Store Protection Backend Correction |
| Status | retained for Windows fallback |
| Superseded | `false` |
| Required by selected Mode C | `false` |
| Deletion authorized | `false` |

P15.4 replacement posture:

| Field | Value |
| --- | --- |
| Original ticket status | paused |
| Migration disposition | replace |
| Selective forward-port | completed |
| Final status | completed by replacement |
| Completing authority | P15.M8, P15.M11A, P15.M12 |
| Accepted outputs | `PEPPER_P15_M11_OK`, `PEPPER_P15_M12_OK` |
| Rerun original ticket required | `false` |

Migration conclusion:

| Field | Value |
| --- | --- |
| P15.M local Hermes 0.19 migration | closed with constraints |
| P15.1A retained for Windows fallback | `true` |
| P15.4 completed by replacement | `true` |
| Next ticket | P15.5 - Usage, Cost and Timeout Accounting |
| VPS dependency for P15.5 | none |

P15.MR hands control back to the original local Pepper roadmap at P15.5. P15.5 must define usage, cost and timeout accounting scope, evidence, validation, security posture, stop rules and Git posture before any implementation or runtime expansion.

## No-Execution Counters

P15.MR counters:

| Counter | Value |
| --- | ---: |
| Product/source implementation edits | `0` |
| Test edits | `0` |
| Manifest or lock edits | `0` |
| Docker containers started | `0` |
| Docker networks created | `0` |
| Docker image builds | `0` |
| Docker image pulls | `0` |
| Docker image pushes | `0` |
| OAuth attempts | `0` |
| Credential promotions | `0` |
| Temporary credential leases created | `0` |
| Provider dispatches | `0` |
| Inference calls | `0` |
| Tool calls | `0` |
| MCP calls | `0` |
| Remote hosts contacted | `0` |
| SSH connections | `0` |
| SCP/SFTP/rsync transfers | `0` |
| Cloud API calls | `0` |
| VPS purchases/provisioning actions | `0` |
| Graphify runs | `0` |
| Git staging operations | `0` |
| Git commits | `0` |
| Git pushes | `0` |
| Git tags | `0` |
| Git merges/rebases/stashes/resets/cleans/worktrees | `0` |

## Candidate Set And Repository Integrity

Created candidate:

```text
0_architecture/governance/agent_platform_hermes_0_19_local_migration_release_and_deferred_vps_handoff.md
```

Required candidate posture: candidate files `1`, unexpected candidates `0`, staged files `0`, modified tracked files `0`, product files modified `0`, tests modified `0`, modification register modified `false`, baseline JSON modified `false`, import manifest modified `false`, package manifests modified `0`, lockfiles modified `0`, Dockerfiles modified `0`, repository Compose modified `false`, runtime scripts tracked `0`, credential files tracked `0`, SSH files tracked `0`, Graphify modified `false`.

## Residual Constraints

P15.MR does not prove VPS availability, host hardening, SSH access, remote Docker availability, image transfer, remote dashboard readiness, remote browser acceptance, remote credential acquisition, provider reachability from a VPS, remote OpenAI Codex entitlement, remote recovery, remote rollback, unattended 24/7 safety, update-engine readiness, one-click update readiness, product activation readiness, implementation readiness, source tracking readiness, dependency adoption, publication readiness, or production readiness.

P15.MR is complete only as a local migration release and deferred handoff closure. Human review remains required before any Git integration, remote execution, local activation roadmap execution, or future product/runtime work.

## Final Verdict

`hermes_0_19_local_migration_release_and_deferred_vps_handoff_closed_with_constraints`
