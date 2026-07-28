# P15.C2 - Pepper Canonical Credential Store Root Repair

Status: P15.C2 canonical credential-store root repair ready with legacy compatibility.

Final verdict: `hermes_0_19_pepper_canonical_credential_store_root_ready_with_legacy_compatibility`

## Authority

P15.C2 repairs the default Pepper OpenAI Codex credential-store root from the duplicated legacy layout to the canonical one-level layout while preserving discoverability for an already materialized legacy-only duplicated store.

P15.C2 performs no automatic migration, credential inspection, credential copy, credential move, credential deletion, credential refresh, credential rotation, OAuth, provider call, worker start, Docker execution, remote-host access, Graphify command, dependency installation, Git staging, commit or push.

## Repository State

| Field | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM` |
| Branch | `p15.cleanup-canonicalization` |
| P15.C1 commit | `f5d6ffb935064db8e3e3d8afdaee047d09e2b20a` |
| P15.C1 message | `P15.C1 Port Windows credential protection to Pepper` |
| P15.C1 files | `7` |
| P15.C1 verdict | `hermes_0_19_pepper_windows_credential_store_protection_port_ready_with_constraints` |
| P15.C1 native smoke verdict | `pepper_windows_credential_store_protection_smoke_passed` |

## Canonical Product Authority

| Field | Value |
| --- | --- |
| Canonical product | `2_products/pepper-agent` |
| Upstream | `Hermes Agent 0.19.0` |
| Upstream commit | `3ef6bbd201263d354fd83ec55b3c306ded2eb72a` |
| Legacy product | `2_products/hermes-agent` |
| Legacy product authoritative | `false` |
| Legacy product removal owner | `P15.C3` |

## Pre-Change Integrity

| Scope | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Committed post-P15.C1 candidate | 6792 | 149538112 | `3cc062bc3c0571cf06ededf1fff54d9d7a2dd3f526af16bbafa534d459b09b0a` |
| Upstream payload | 6681 | 145409792 | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | not_applicable | 38693 | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Governance integrity tests: `Ran 14 tests`; failures `0`; errors `0`.

## Caller Inventory

All repository callers of `default_openai_codex_credential_store_root` were inspected without Graphify:

| Path | Use |
| --- | --- |
| `hermes_cli/agent_platform/provider_credentials/store.py` | public helper and export |
| `hermes_cli/agent_platform/provider_worker_gate/runtime.py` | worker-gate default root selection in `main()` |
| `tests/hermes_cli/test_agent_platform_provider_credential_store.py` | root contract and credential-store tests |
| `0_architecture/governance/agent_platform_pepper_windows_credential_store_protection_port.md` | P15.C1 deferred repair reference |

Status, promotion, clear and delivery operations continue to accept explicit trusted store roots. The default resolver only selects the root path; store validation and P15.C1 protection remain separate. Real credential access during caller inspection: `0`.

## Layout Contract

Canonical root:

```text
<HERMES_HOME>/agent-platform/provider-credentials/openai-codex.primary
```

Legacy duplicated root:

```text
<HERMES_HOME>/agent-platform/provider-credentials/agent-platform/provider-credentials/openai-codex.primary
```

Canonical segment counts: `agent-platform=1`, `provider-credentials=1`, `openai-codex.primary=1`. The canonical and legacy paths are distinct and both remain contained below the supplied Hermes home. The resolver adds no parent traversal, environment expansion or home fallback when explicit root input is supplied.

## Resolution Matrix

| Canonical | Legacy duplicated | Result |
| --- | --- | --- |
| absent | absent | canonical |
| present | absent | canonical |
| absent | present | legacy duplicated compatibility |
| present | present | fail closed |

Dual-root conflict category: `ambiguous_canonical_and_legacy_credential_store_roots`.

The resolver inspects root path presence only. A present directory, file, symlink or reparse-point root is treated as present and later rejected by store validation when malformed.

## Compatibility Boundary

Legacy compatibility preserves discoverability of an already materialized duplicated root only when the canonical root is absent. The legacy root is not canonical, is not created by the resolver, is not migrated by the resolver and is not claimed as permanent.

## P15.C1 Preservation

P15.C2 preserves P15.C1 Windows protection semantics: Windows DACL application, Windows DACL validation, typed WinAPI signatures, 64-bit HANDLE and pointer safety, protected DACL, current-user/System/Administrators allow policy and broad-principal rejection. P15.C1 native smoke remains part of validation.

## Candidate Files

Modified:

```text
2_products/pepper-agent/hermes_cli/agent_platform/provider_credentials/store.py
2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_credential_store.py
2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv
```

Created:

```text
2_products/pepper-agent/docs/agent-platform/canonical_credential_store_root_layout.md
10_scripts/hermes/agent_platform_pepper_credential_store_root_layout_smoke.py
12_tests/hermes/test_agent_platform_pepper_credential_store_root_layout_smoke.py
0_architecture/governance/agent_platform_pepper_canonical_credential_store_root_repair.md
```

## Validation Evidence

| Check | Result |
| --- | --- |
| Targeted credential-store tests | `16 passed`; failures `0`; errors `0` |
| Provider and credential regression | `126 passed`; failures `0`; errors `0`; new P15.C2 warnings `0` |
| Accounting regression | `19 passed`; failures `0`; errors `0` |
| Failure-policy regression | `56 passed`; failures `0`; errors `0` |
| Controlled-gate regression | `22 passed`; failures `0`; errors `0`; live provider calls `0` |
| P15.C1 Windows smoke pytest | `4 passed`; failures `0`; errors `0` |
| P15.C1 native Windows smoke | verdict `pepper_windows_credential_store_protection_smoke_passed` |
| Root-layout smoke pytest | `5 passed`; failures `0`; errors `0` |
| Root-layout smoke JSON | verdict `pepper_credential_store_root_layout_smoke_passed` |
| Root-layout smoke text | pathless text verdict emitted |
| Ruff lint and format | `All checks passed`; `4 files already formatted` |
| `ty` | unavailable; type check not run; dependency installation `0` |

## Register and Manifest

`P15.1-003` and `P15.1-007` are reconciled for the modified store and test. `P15.C2-001` records the product documentation addition. Import-manifest rows for the store and test are updated, and one product-addition row is added for the documentation file. All target rows classify as product additions with no upstream source object.

## Operational Authority

| Action | Count |
| --- | ---: |
| Real credential reads | 0 |
| Real credential writes | 0 |
| Credential leases | 0 |
| Credential refreshes | 0 |
| Credential rotations | 0 |
| Credential copies | 0 |
| Credential moves | 0 |
| Credential deletes | 0 |
| OAuth attempts | 0 |
| Provider dispatches | 0 |
| Provider streams | 0 |
| Workers | 0 |
| Docker | 0 |
| Remote hosts | 0 |
| Graphify commands | 0 |
| Git stage | 0 |
| Git commit | 0 |
| Git push | 0 |

Synthetic temporary directories are created and removed only by the bounded smoke.

## Handoff

P15.C3 owns legacy Hermes product removal after P15.C2 is reviewed, committed and pushed. P15.C3 must not delete `2_products/pepper-agent`, `4_external/sources`, durable credential stores or retained Docker images.

Residual constraints: real legacy store migrated `false`; real canonical store created `false`; legacy-only compatibility retained; dual-store state fail-closed; automatic store migration absent; credential refresh disabled; credential rotation disabled; provider fallback disabled; automatic retry disabled; legacy Hermes product retained until P15.C3; P16 blocked until P15.CR; production readiness not claimed.
