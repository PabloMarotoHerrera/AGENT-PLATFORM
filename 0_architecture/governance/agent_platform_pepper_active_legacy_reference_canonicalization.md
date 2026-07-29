# P15.C3B - Pepper Active Legacy Reference Canonicalization

## Document Header

| Field | Value |
| --- | --- |
| Project | P15 cleanup canonicalization |
| Ticket | P15.C3B |
| Status | Active legacy references canonicalized; historical evidence preserved |
| Date | 2026-07-29 |
| Branch | `p15.cleanup-canonicalization` |
| Starting HEAD | `8e8b1c17fbec45e8f27c053db084b1f9a8098684` |
| P15.C3A authority | `0_architecture/governance/agent_platform_pepper_legacy_frontend_capability_reconciliation.md` |

## Scope

P15.C3B removes active first-party dependency on the retained legacy product
root while preserving historical and provenance references. The retained legacy
product and canonical Pepper product are not modified.

Protected paths not modified:

```text
2_products/hermes-agent/**
2_products/pepper-agent/**
4_external/sources/**
.opencode/**
graphify-out/**
package manifests and lockfiles
```

Graphify, Docker, providers, OAuth, workers, dependency installation, staging,
commits, pushes, reset, clean, stash and product-root mutation were not run.

## Inventory Method

The pre-change exact scan used tracked files from `git ls-files`, excluding the
protected legacy product, external source, `.opencode` and `graphify-out` roots.
It searched exact active path forms and product control-file references.

Observed corrected P15.C3A HEAD inventory before mutation:

| Inventory item | Count |
| --- | ---: |
| Matched files with exact legacy path/control-file references | 62 |
| Exact matches at corrected P15.C3A HEAD | 679 |
| Exact active matches inside frozen blocker files | 109 |
| Additional split/name active product-root tokens inside frozen blocker files | 20 |
| Total active blocker references | 129 |
| Historical/provenance exact matches retained | 570 |
| Unclassified references | 0 |

The earlier ticket expectation of 903 exact matches was not used as a mutation
target because the corrected P15.C3A authority was already at HEAD. P15.C3B is
bound to the observed corrected-HEAD inventory above.

## Historical Preservation Classification

References retained in earlier governance records, Pepper control manifests and
legacy provenance files are historical or provenance evidence. They continue to
identify prior Hermes productization, import, migration, baseline, source-lock,
Graphify-scope, synchronization and Pepper forward-port evidence. They are not
active first-party execution or tracking dependencies after this change.

The superseded Graphify scope record remains historical evidence. The active
`.graphifyignore` file now preserves a frozen read-only posture: products remain
excluded and no active product refresh target is admitted.

## Frozen Blocker Set

The blocker set was frozen before edits. These 15 tracked files were the only
active blocker files and the only files authorized for mutation, plus this new
governance record.

| File | Pre active refs | Pre blob | Pre SHA-256 | Disposition |
| --- | ---: | --- | --- | --- |
| `.gitignore` | 2 | `fce3988f236d7a9c91b478bf91962d09f1ecaf04` | `f3e4ac2e89da57096c9d9a39d0b51627cd7bd0f5bd4918bd0ebdeb23f9a14723` | Replace complete product-root ignore with narrow product-neutral generated-artifact rules. |
| `.graphifyignore` | 2 | `2b521fbfdd6dc6015eb116f79886ee992420477a` | `95cc0ae3dfe1dc1b20b79c8eb3c560f0657af4fe69ae026dfc032687ec2d74f8` | Remove active product allowlist; keep frozen read-only product exclusion. |
| `10_scripts/graphify/refresh_hermes_graph.py` | 12 | `0adf3432664c2425363ec071baaaa0d4e7df95d3` | `f1ba45c6c9f8bfbf1a6dd35d791ce78c29a32ae6c3e93fcbe4ddf393ae4654b2` | Retire obsolete Graphify refresh regeneration utility. |
| `10_scripts/hermes/agent_platform_frontend_quality_gate.py` | 3 | `ed02192d60e71b6a805298f3f927405945951d2d` | `8a0d7230f82206b9100ad4f94fbd612a0db1389490dbde48d71b1ae765fd3c3e` | Resolve gate product root and evidence cwd to Pepper. |
| `10_scripts/hermes/agent_platform_runtime_adapter_lifecycle_gate.py` | 2 | `a487c0612bb1aad581018b9f54ddc64111e302ec` | `1922ff304cd1d74c7bca3fa8e820b1bf9b6326f33f025f45130c9b46e6480850` | Resolve lifecycle product root to Pepper. |
| `10_scripts/hermes/agent_platform_openai_codex_oauth_boundary.py` | 1 | `962861ab1cee25d5820b9c2670980ba88cdb4902` | `38020ce0f1c70a7ee6fc9f537ea18001a59241da59f5d81e95e09fce5ff7190c` | Resolve product root to Pepper and align planner call with Pepper contract. |
| `10_scripts/hermes/agent_platform_openai_codex_worker_profile.py` | 1 | `6e71d690c56dfdc8b3a1dfe048ac157134110072` | `0e9d478e2ab785567c11e5a5ec4f2cd8f8138fc2375b9ba07d22ac37f6a06b81` | Resolve product root to Pepper. |
| `10_scripts/hermes/agent_platform_openai_codex_provider_profile.py` | 1 | `4ca7e813dde79660ab3c346cbbc3564b47f92d73` | `2d86f1c9cfa69c17c7b7d3d901c196db50a94de38a3f354811cf0f686686eee2` | Resolve product root to Pepper. |
| `12_tests/graphify/test_refresh_hermes_graph.py` | 54 | `b988fe2380c24db9feae465c392a8621cd0d20a7` | `3f23fcf3c98f270392f74c566c9bdf21ce83b04c2b9c02ae9079470f9852adb5` | Retire obsolete refresh utility unit tests. |
| `12_tests/graphify/test_refresh_hermes_graph_integration.py` | 43 | `047e1f3dd97bb2b37b36a2da86884312260c02b0` | `86cea89b8bde547c9f512992b71411dbb05e8b97758d7cf786ba22a379782260` | Retire obsolete refresh utility integration tests. |
| `12_tests/hermes/test_agent_platform_frontend_quality_gate.py` | 2 | `5b1173af610526c48b48794795efeab140dc01c8` | `cbed4a531e843d7340f6f13e1c5c32a25578afec19f425ccbf1b69d538c7b026` | Switch active frontend gate fixtures to Pepper. |
| `12_tests/hermes/test_agent_platform_runtime_adapter_lifecycle_gate.py` | 3 | `26fa0d1e9108af44c03c04abd5744ba44d7cc017` | `d3c4bab3ed33a85d07a47098fc46ee7374dd603e77de648acb65c24eba4eef2a` | Switch active lifecycle fixtures to Pepper. |
| `12_tests/hermes/test_agent_platform_openai_codex_oauth_boundary.py` | 1 | `fb38d05dfd27dfba1e5ad174ff0283097cb398a4` | `77631be8c67d8a8dacab10ee14c067cbd60305508de54be000a0a0fed87df829` | Switch product root fixture to Pepper and match seven-key acquisition-plan contract. |
| `12_tests/hermes/test_agent_platform_openai_codex_worker_profile.py` | 1 | `f4c3293f77d73a2a7c00b6d94354a6aee0e4a53c` | `d1e056bd2fea7101bf49c1502358b519b70653d7e357da74d9e7e97d35279b21` | Switch product root fixture to Pepper. |
| `12_tests/hermes/test_agent_platform_openai_codex_provider_profile.py` | 1 | `8ef6ffdc419d2103efafd6e7ebd7f1b6f266b295` | `34330d75fbb80ee9ff017177efb4c8734f046bf196db4b828a85e3a4b5ec9bed` | Switch product root fixture to Pepper. |

## Post-Change Candidate State

| File | Status | Post active legacy refs | Post Pepper refs | Post blob | Post SHA-256 |
| --- | --- | ---: | ---: | --- | --- |
| `.gitignore` | `M` | 0 | 0 | `1b65fbf27d7987fd051529543d39ef150ea3ca9e` | `dd63b296f1cf6519c56329cb47ff543cd013e9f7c1db3dae11614f71a85878b8` |
| `.graphifyignore` | `M` | 0 | 0 | `83facd885a7164f10de789142cc7108a7fc1cb37` | `45e10b1dd6cef1fa654d4115195392f13ecb680045334b7a4fde674aff257caf` |
| `10_scripts/graphify/refresh_hermes_graph.py` | `D` | 0 | 0 | `deleted` | `deleted` |
| `10_scripts/hermes/agent_platform_frontend_quality_gate.py` | `M` | 0 | 3 | `e16aa6b364a9c6bd2b26e6bc0c20e7e46303dc1a` | `2dc665b0a7d0d2799ebe9115e8f3f17aa1b7c5136339c98d2bad2d98d42ed0f1` |
| `10_scripts/hermes/agent_platform_runtime_adapter_lifecycle_gate.py` | `M` | 0 | 2 | `2ffac5ad5d1b2d44d73c326b4a8e02dcdef629cb` | `5f53618f7eb8adb339363083ac0557187e91c28b4308c2a56f0dc0200baa72e7` |
| `10_scripts/hermes/agent_platform_openai_codex_oauth_boundary.py` | `M` | 0 | 1 | `1680260792d2d02dc9dadaa1fc1ad7d2af522d07` | `cf4c0fe84408bfea06f9e9be59f16fa0aeda945e278dec7c2ba8eea21fac2049` |
| `10_scripts/hermes/agent_platform_openai_codex_worker_profile.py` | `M` | 0 | 1 | `e0d27af1dca81d15d586d32a8a4398735be7f9db` | `5b90de4ef7bf981b37c068c6ea58917730587cebaa3977afa9253a80e30cd9a3` |
| `10_scripts/hermes/agent_platform_openai_codex_provider_profile.py` | `M` | 0 | 1 | `1d0461ecf22da0adc4452c29a82c53507364296f` | `0272a1650556773dbd5c674a848b856dfe59a7bdac5c5a5ab4fd1705e85ae62e` |
| `12_tests/graphify/test_refresh_hermes_graph.py` | `D` | 0 | 0 | `deleted` | `deleted` |
| `12_tests/graphify/test_refresh_hermes_graph_integration.py` | `D` | 0 | 0 | `deleted` | `deleted` |
| `12_tests/hermes/test_agent_platform_frontend_quality_gate.py` | `M` | 0 | 2 | `db2fb0c08518cb177a0d59c44a4996255e0a93c0` | `d886ab318c42d2ab9c37b717701b1d09b4935e7ba5b037085015d439197c89bc` |
| `12_tests/hermes/test_agent_platform_runtime_adapter_lifecycle_gate.py` | `M` | 0 | 3 | `f6ba289b25fe32ccde61a0b6ecec63185d9a27e9` | `6123da8a7d0eed719b2b482b47c3ce8f871e9cd03209a2f8c944fce4c2480944` |
| `12_tests/hermes/test_agent_platform_openai_codex_oauth_boundary.py` | `M` | 0 | 1 | `e0e769a7e270cf9e030d4af3787abdeb4d1e99bd` | `83fde61f2d5d52c12ff66fe7aeccfdc20effdf28cef8d22253c2a07d9c713673` |
| `12_tests/hermes/test_agent_platform_openai_codex_worker_profile.py` | `M` | 0 | 1 | `b9794e3c55c314ee34c983c2b428c140ed8b493a` | `b489a90e9ad24710472a956b96f1b127aec8bda53bcaf9e0b613885245342cd5` |
| `12_tests/hermes/test_agent_platform_openai_codex_provider_profile.py` | `M` | 0 | 1 | `b5bdc0f8ef04d06337a2cf78d7c8668f568a1dc8` | `88cf00366522822bc5fd2060ed7e0d7d6af2ee19e83b2f13f76e13b0d0dc46de` |

## Ignore Containment

The complete product-root ignore rule is absent. The active root `.gitignore`
contains only narrow product-neutral generated-artifact patterns for product
residue not already covered by existing generic ignore rules:

```text
/2_products/*/**/web_dist/
/2_products/*/**/*.egg-info/
/2_products/*/**/tsconfig.tsbuildinfo
/2_products/*/**/test_durations.json
/2_products/*/**/.pytest_cache/
/2_products/*/**/.mypy_cache/
/2_products/*/**/.ruff_cache/
```

Validation posture:

```yaml
complete_product_root_ignore_rule: absent
generated_artifact_rules: narrow_product_neutral_patterns
source_probe_ignored: false
test_probe_ignored: false
generated_probes_ignored: true
legacy_generated_residue_newly_visible: 0
legacy_generated_residue_deleted: 0
legacy_generated_residue_modified: 0
legacy_specific_product_name_tokens: 0
```

An unrelated pre-existing untracked product root under `2_products/omniverse-app`
became visible after removal of the broad product-root ignore. It is not part of
the scoped P15.C3B candidate set, remains untouched, and is excluded from P15.C3B
candidate accounting by explicit human clarification.

## Graphify Policy

```yaml
Graphify_policy: frozen_read_only
refresh_utility: retired
refresh_tests: retired
Pepper_refresh_target: absent
Graphify_commands: 0
graphify_out_modified: false
replacement_refresh_utility_created: false
replacement_refresh_tests_created: false
```

The retired files had only Graphify refresh-regeneration purpose. No external
active importers, active callers or active documented workflows remain outside
historical governance references.

## Validation

| Check | Result |
| --- | --- |
| Frozen candidate `hermes-agent` token scan | `0` remaining across the 12 retained active blocker files; retired Graphify files are deleted |
| Python syntax compilation | Passed for the 10 retained touched Python files with `python -B -m py_compile ...` |
| Focused non-Graphify unit tests | `39` tests passed with inherited Pydantic protected-namespace warnings |
| Governance integrity tests | `14` tests passed |
| Pepper product `git status` | clean |
| Legacy product `git status` | clean |
| Pepper candidate identity | `6831` files, `149941138` bytes, `2735cb45f0e087cc9dd2901ae5c1140e89ddcee886d526b0d2fbf253a13d9e50` |
| Pepper payload identity | `6681` files, `145409792` bytes, `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Pepper baseline record identity | `38693` bytes, `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |
| Legacy tracked-tree identity | `6246` files, `134403219` bytes, `2981fe08c44ec18646118a23ccbbaee5fdfb3450d6679b1a6ff45c52edfba5e1` |

Graphify tests, Graphify update and the retired refresh utility were not run
because P15.C3B explicitly prohibits Graphify execution.

## Candidate Set

Authorized scoped P15.C3B candidate files after this record:

```text
M  .gitignore
M  .graphifyignore
D  10_scripts/graphify/refresh_hermes_graph.py
M  10_scripts/hermes/agent_platform_frontend_quality_gate.py
M  10_scripts/hermes/agent_platform_openai_codex_oauth_boundary.py
M  10_scripts/hermes/agent_platform_openai_codex_provider_profile.py
M  10_scripts/hermes/agent_platform_openai_codex_worker_profile.py
M  10_scripts/hermes/agent_platform_runtime_adapter_lifecycle_gate.py
D  12_tests/graphify/test_refresh_hermes_graph.py
D  12_tests/graphify/test_refresh_hermes_graph_integration.py
M  12_tests/hermes/test_agent_platform_frontend_quality_gate.py
M  12_tests/hermes/test_agent_platform_openai_codex_oauth_boundary.py
M  12_tests/hermes/test_agent_platform_openai_codex_provider_profile.py
M  12_tests/hermes/test_agent_platform_openai_codex_worker_profile.py
M  12_tests/hermes/test_agent_platform_runtime_adapter_lifecycle_gate.py
?? 0_architecture/governance/agent_platform_pepper_active_legacy_reference_canonicalization.md
```

Candidate count is exactly 16 in the scoped P15.C3B candidate set: 12 modified
files, 3 deleted files and this one new governance record. No Pepper product,
legacy product or `graphify-out` candidate is authorized.

## Final Verdict

```text
hermes_0_19_pepper_active_legacy_references_canonicalized_with_historical_evidence_preserved
```
