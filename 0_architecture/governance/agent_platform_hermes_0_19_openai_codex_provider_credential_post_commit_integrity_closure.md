# P15.M8R - OpenAI Codex Provider Credential Post-Commit Integrity Closure

Status: P15.M8R post-commit OpenAI Codex provider credential integrity closed with constraints.

Final verdict: `hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closed_with_constraints`

## Authority

P15.M8R closes the post-commit integrity transition created by P15.M8 after the
accepted P15.M8 implementation and the accepted P15.M8A metadata-only manifest
hash reconciliation. The original P15.M8 commit remains the only product,
test, modification-register and application-manifest mutation commit.

P15.M8R modifies only the self-excluded Pepper baseline JSON and creates this
closure record. It does not modify provider credential implementation, provider
runtime implementation, bounded worker implementation, tests, modification
register rows, the P15.M8 application manifest, runtime adapter files, product
configuration, web server, frontend files, package manifests, lockfiles,
Desktop, Workspace, Graphify output or prior governance records.

Authorized P15.M8R candidates:

| Path | Disposition |
| --- | --- |
| `2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json` | updates self-excluded current baseline integrity metadata |
| `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closure.md` | records the P15.M8R closure evidence |

## Repository Gate

| Check | Result |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| HEAD at start | `61c072eb0573b5bf07b169aaaf01fdd02ff385dc` |
| origin/p15.m-hermes-0.19-migration | `61c072eb0573b5bf07b169aaaf01fdd02ff385dc` |
| HEAD equals remote at start | `true` |
| Index empty at start | `true` |
| Tracked worktree clean at start | `true` |
| P15.M8 verdict present | `hermes_0_19_openai_codex_provider_credential_oauth_application_ready_with_constraints` |
| P15.M8A verdict present | `hermes_0_19_openai_codex_provider_credential_manifest_hash_reconciled` |

## Commit History Rule

| Field | Value |
| --- | --- |
| P15.M8 implementation commit | `a1d189bedb8b69df9307b52865b75697557dc7cc` |
| P15.M8 commit message | `P15.M8 Apply OpenAI Codex provider credential boundaries` |
| P15.M8 commit is ancestor of HEAD | `true` |
| Authorized post-P15.M8 repair commit | `61c072eb0573b5bf07b169aaaf01fdd02ff385dc` |
| Authorized repair commit message | `P15.M8A Reconcile provider credential manifest hash` |
| Post-P15.M8 commits | `1` |
| Post-P15.M8 commit status | `exactly_one_authorized_governance_metadata_repair` |
| Post-P15.M8 product, test, register or manifest mutation commits | `0` |
| Unexpected post-P15.M8 paths | `0` |

Authorized post-P15.M8 paths:

| Path | Commit disposition |
| --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_credential_oauth_application.md` | P15.M8A metadata-only manifest identity reconciliation |
| `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_credential_manifest_hash_reconciliation.md` | P15.M8A durable repair record |

P15.M8R validates the current amended P15.M8 governance record. It does not
require the amended governance record blob to equal the original P15.M8 commit.

## P15.M8 Commit Set

| Check | Result |
| --- | ---: |
| P15.M8 committed files | `32` |
| Product implementation and test files | `29` |
| Modification register control files | `1` |
| Governance files | `2` |
| Forbidden files | `0` |

The P15.M8 file set contains no product configuration, web server, frontend,
package manifest, lockfile, Desktop, Workspace, runtime adapter or Graphify
mutation outside the governed provider credential, provider runtime and bounded
worker boundary.

## Application Manifest

| Check | Result |
| --- | --- |
| Path | `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_credential_manifest.tsv` |
| Manifest commit | `a1d189bedb8b69df9307b52865b75697557dc7cc` |
| Content basis | exact `HEAD` Git blob bytes, LF checkout realization observed |
| Rows | `29` |
| Columns | `23` |
| Bytes | `28938` |
| SHA-256 | `71a3fcf959f31eba1f1a4a6f5107b5f87ddaa9d85a9db0c8bded587f9130985a` |
| Provider credential rows | `11` |
| Provider runtime rows | `8` |
| Provider worker rows | `10` |
| Duplicate record IDs | `0` |
| Duplicate product paths | `0` |
| Register-manifest hash mismatches | `0` |
| Unverified records | `0` |
| Live OAuth claim violations | `0` |
| Manifest hash recorded in amended P15.M8 governance | `true` |
| P15.M8A reconciliation record present | `true` |

The manifest content was not modified by P15.M8A or P15.M8R.

## Modification Register

| Check | Result |
| --- | ---: |
| Register path | `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` |
| Register bytes | `106416` |
| Register SHA-256 | `0e3492ab2db68659d21d9bbccd1edf08c0642187a2febe0199adc578c0f55084` |
| Register rows | `87` |
| Register columns | `18` |
| P15.M8 rows | `29` |
| Checked current-product SHA rows | `87` |
| Missing committed product blobs | `0` |
| HEAD blob hash mismatches | `0` |
| Duplicate P15.M8 IDs | `0` |
| Duplicate P15.M8 product paths | `0` |

All registered `current_product_sha256_or_none` values match exact current
`HEAD` Git blob SHA-256 values, including all 29 P15.M8 rows.

## Canonical Integrity

Canonical command run twice with matching output:

```cmd
python 10_scripts/governance/pepper_baseline_integrity.py --repo-root . --product-root 2_products/pepper-agent --mode all --format json
```

Current post-P15.M8 candidate identity:

| Field | Value |
| --- | --- |
| Algorithm | `agent-platform-git-tree-sha256-v2` |
| Representation | `canonical_committed_candidate_except_baseline_record` |
| Content basis | exact current `HEAD` Git blob bytes |
| Scope | all tracked files under `2_products/pepper-agent` except `AGENT_PLATFORM_UPSTREAM_BASELINE.json` |
| Excluded path | `AGENT_PLATFORM_UPSTREAM_BASELINE.json` |
| Files | `6768` |
| Bytes | `149234329` |
| SHA-256 | `f0dceedbe9ae1b6b0738c00b0d643678d8bc5acd2b9766729f7adcb238c08e59` |

Current post-P15.M8 payload identity:

| Field | Value |
| --- | --- |
| Algorithm | `agent-platform-git-tree-sha256-v2` |
| Scope | included and transformed upstream payload rows from `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` |
| Files | `6681` |
| Bytes | `145409765` |
| SHA-256 | `56a538886ac9cc98050be853f173e631e8f568495a6c5aeef27a2128981524e7` |

Baseline record identity:

| Field | Value |
| --- | --- |
| Baseline record path | `2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json` |
| Baseline record bytes before P15.M8R | `30860` |
| Baseline record SHA-256 before P15.M8R | `ce0c1875182b9aae46448102ed285f1cf9343b96724cf522a0503fc9f3873719` |
| Projected baseline record bytes after P15.M8R | `34254` |
| Projected baseline record SHA-256 after P15.M8R | `478f1cd5279806e808b562193a993f391f98a4e8513ef4ee8d41e35a0d7c4dda` |
| Stored inside baseline JSON itself | `false` |
| External record for projected post-P15.M8R hash | this P15.M8R closure record |

The Pepper payload identity is unchanged from P15.M7. The candidate identity
changed because P15.M8 added the governed provider credential, runtime profile
and bounded worker product files and tests.

## Baseline JSON Update

`2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json` was updated to
record:

| Field | Result |
| --- | --- |
| `payload_integrity.status` | `committed_post_P15_M8` |
| `candidate_integrity.status` | `committed_post_P15_M8` |
| `candidate_integrity.file_count` | `6768` |
| `candidate_integrity.byte_count` | `149234329` |
| `candidate_integrity.SHA256` | `f0dceedbe9ae1b6b0738c00b0d643678d8bc5acd2b9766729f7adcb238c08e59` |
| `pre_P15_M8_candidate_integrity` | preserved post-P15.M7 candidate identity |
| `pre_P15_M8_payload_integrity` | preserved post-P15.M7 payload identity |
| `provider_credential_state` | recorded P15.M8/P15.M8A bounded provider credential state |
| `baseline_record_integrity.post_P15_M8R_external_record` | this P15.M8R closure record |

## Provider Suite Validation

Exact 12-file P15.M8 provider suite command:

```cmd
python -m pytest -q tests/hermes_cli/test_agent_platform_openai_codex_oauth_acquisition.py tests/hermes_cli/test_agent_platform_provider_client_tokens.py tests/hermes_cli/test_agent_platform_provider_credential_contracts.py tests/hermes_cli/test_agent_platform_provider_credential_delivery.py tests/hermes_cli/test_agent_platform_provider_credential_store.py tests/hermes_cli/test_agent_platform_provider_runtime_contracts.py tests/hermes_cli/test_agent_platform_provider_runtime_profiles.py tests/hermes_cli/test_agent_platform_provider_runtime_resolution.py tests/hermes_cli/test_agent_platform_provider_worker_contracts.py tests/hermes_cli/test_agent_platform_provider_worker_profiles.py tests/hermes_cli/test_agent_platform_provider_worker_protocol.py tests/hermes_cli/test_agent_platform_provider_worker_resolution.py -p no:cacheprovider
```

| Result field | Value |
| --- | ---: |
| Passed | `119` |
| Warnings | `3` |
| Failed | `0` |
| Errors | `0` |

Warning classification:

| Warning class | Count |
| --- | ---: |
| `credential_or_token_leak_warning` | `0` |
| `security_boundary_warning` | `0` |
| `unhandled_resource_warning` | `0` |
| `unexpected_deprecation_warning` | `0` |
| `warnings_affecting_acceptance` | `0` |

The three warnings are the expected bounded Pydantic protected-namespace
warnings for `model_id`, `model_policy` and
`model_list_calls_per_request_maximum`.

## Runtime Adapter Regression

Exact 15-file P15.M7 runtime-adapter suite command:

```cmd
python -m pytest -q tests/hermes_cli/test_agent_platform_runtime_adapter_conformance.py tests/hermes_cli/test_agent_platform_runtime_adapter_contracts.py tests/hermes_cli/test_agent_platform_runtime_adapter_failure_conformance.py tests/hermes_cli/test_agent_platform_runtime_adapter_integration.py tests/hermes_cli/test_agent_platform_runtime_audit_normalization.py tests/hermes_cli/test_agent_platform_runtime_environment.py tests/hermes_cli/test_agent_platform_runtime_event_normalization.py tests/hermes_cli/test_agent_platform_runtime_lifecycle_control.py tests/hermes_cli/test_agent_platform_runtime_listener_discovery.py tests/hermes_cli/test_agent_platform_runtime_path_containment.py tests/hermes_cli/test_agent_platform_runtime_process_owner.py tests/hermes_cli/test_agent_platform_runtime_profiles.py tests/hermes_cli/test_agent_platform_runtime_readiness.py tests/hermes_cli/test_agent_platform_runtime_rollback.py tests/hermes_cli/test_agent_platform_runtime_workspace.py -p no:cacheprovider
```

| Result field | Value |
| --- | ---: |
| Passed | `143` |
| Skipped | `5` |
| Failed | `0` |
| Errors | `0` |
| First-run `PROCESS-001` transient failure | `false` |
| Full-suite rerun required | `false` |

Skipped test IDs and bounded reasons:

| Test ID | Reason |
| --- | --- |
| `tests/hermes_cli/test_agent_platform_runtime_path_containment.py::test_trusted_base_root_rejects_symlink_and_reparse_point` | `host does not allow directory symlink creation` |
| `tests/hermes_cli/test_agent_platform_runtime_path_containment.py::test_symlink_redirect_rejected_even_when_target_is_inside_root` | `host does not allow directory symlink creation` |
| `tests/hermes_cli/test_agent_platform_runtime_rollback.py::test_oversized_and_symlink_marker_are_rejected_without_deleting` | `symlink creation unavailable` |
| `tests/hermes_cli/test_agent_platform_runtime_rollback.py::test_safe_preflight_rejects_redirects_special_files_depth_and_entry_bounds` | `symlink creation unavailable` |
| `tests/hermes_cli/test_agent_platform_runtime_workspace.py::test_workspace_paths_are_contained_and_symlink_workspace_root_rejected` | `host does not allow directory symlink creation` |

## Product Configuration And Routes

| Check | Result |
| --- | --- |
| `python -m pytest -q tests/hermes_cli/test_agent_platform_product_config.py -p no:cacheprovider` | `10 passed` |
| Product config failed | `0` |
| Product config errors | `0` |
| `fastapi_available` | `false` |
| `product_route_regression` | `blocked_by_unprepared_environment` |

No dependency installation was performed, so product route tests were not run.

## Static Python Validation

Static checks ran against all 29 P15.M8 Python files.

| Check | Result |
| --- | ---: |
| Ruff check errors | `0` |
| Ruff format check | `29 files already formatted` |
| `py_compile` syntax errors | `0` |
| Windows footgun inspected files | `821` |
| Windows footguns | `0` |

`py_compile` bytecode output was directed outside the workspace through
`PYTHONPYCACHEPREFIX`; no workspace cache residue was created.

## Import And Public Surface Smoke

| Check | Result |
| --- | --- |
| `provider_credentials` import | passed |
| `provider_runtime` import | passed |
| `provider_worker` import | passed |
| `provider_credentials` root export count | `21` |
| `provider_runtime` root export count | `19` |
| `provider_worker` root export count | `21` |
| Dry-run OAuth `execution_attempted` | `false` |
| Dry-run OAuth `completed` | `false` |
| Dry-run OAuth fixed argv | `true` |
| Live OAuth attempts | `0` |

The import smoke emitted the same three expected bounded Pydantic
protected-namespace warnings as the provider suite.

## Static Security Validation

Static source checks and synthetic in-memory contract serialization produced
the following counts. No real credential values were inspected.

| Boundary | Count |
| --- | ---: |
| `raw_token_logging` | `0` |
| `raw_token_serialization` | `0` |
| `raw_token_public_exports` | `0` |
| `credential_path_public_exports` | `0` |
| `account_identifier_public_exports` | `0` |
| `OPENAI_API_KEY_authority` | `0` |
| `OPENAI_BASE_URL_authority` | `0` |
| `HERMES_CODEX_BASE_URL_override_authority` | `0` |
| `arbitrary_endpoint_authority` | `0` |
| `multiple_account_acceptance` | `0` |
| `credential_rotation` | `0` |
| `automatic_refresh` | `0` |
| `browser_token_storage` | `0` |
| `provider_HTTP_calls` | `0` |
| `inference_calls` | `0` |
| `model_list_calls` | `0` |
| `usage_calls` | `0` |
| `worker_process_starts` | `0` |
| `agent_starts` | `0` |
| `tool_execution` | `0` |
| `MCP_execution` | `0` |

## Real Credential Non-Access

| Boundary | Result |
| --- | --- |
| `real_auth_stores_inspected` | `0` |
| `real_credentials_read` | `0` |
| `real_credentials_written` | `0` |
| `real_OAuth_attempts` | `0` |
| `real_token_refreshes` | `0` |
| `real_lease_operations` | `0` |
| `provider_calls` | `0` |
| `inference_calls` | `0` |
| `P15_M11_authority_preserved` | `true` |

Provider, product and runtime validations used dry-run, static, synthetic or
test-harness-only paths. P15.M11 remains the owner of live OAuth, credential
remote validation and first tool-free inference revalidation. P15.M8R is an
integrity closure only.

## Dependency And Lock Boundary

| Boundary | Count |
| --- | ---: |
| `new_external_runtime_dependencies` | `0` |
| `new_external_test_dependencies` | `0` |
| `undeclared_imports` | `0` |
| `package_manifest_changes` | `0` |
| `lockfile_changes` | `0` |
| `dependency_installations` | `0` |
| `registry_queries` | `0` |

The P15.M8 source imports are stdlib, local Pepper modules or existing
`pydantic` only.

## Import Manifest Drift

| Check | Result |
| --- | ---: |
| `included_import_rows` | `6681` |
| `missing_import_destinations` | `0` |
| `duplicate_import_destinations` | `0` |
| `unsupported_import_classifications` | `0` |
| `P15_M8_product_owned_files_outside_import_manifest` | `29` |
| `P15_M8_product_owned_files_inside_import_manifest` | `0` |
| `new_P15_M8_import_destination_mismatches` | `0` |
| `unexplained_destination_hash_mismatches` | `0` |
| `destination_mismatches_without_modification_row` | `0` |

Known import destination hash mismatches remain `3`, all pre-existing and
registered to P15.M6 product-owned modified files.

## Candidate And Residue Audit

| Check | Result |
| --- | --- |
| Modified candidate | `2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json` |
| Created candidate | `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closure.md` |
| `candidate_files` | `2` |
| `unexpected_candidates` | `0` |
| `git_diff_check` | passed |
| `trailing_whitespace` | `0` |
| `unexpected_binary_files` | `0` |
| `new_executable_files` | `0` |
| `__pycache__` | `0` |
| `.pytest_cache` | `0` |
| `temporary_OAuth_residue` | `0` |
| `credential_lease_residue` | `0` |
| `provider_process_residue` | `0` |
| `index_empty` | `true` |
| `staged_files` | `0` |
| Staging performed by agent | `0` |
| Commits performed by agent | `0` |
| Pushes performed by agent | `0` |

## Governance Utility Validation

| Command or check | Result |
| --- | --- |
| `python -m json.tool 2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json > $null` | passed |
| `python -m unittest discover -s 12_tests/governance -p test_pepper_baseline_integrity.py` | `Ran 14 tests in 0.003s`; `OK` |
| Canonical integrity command | ran twice with matching candidate and payload output |
| Manifest rows and columns | `29` rows, `23` columns |
| Register committed-blob hash verification | `87` checked, `0` mismatches |

## Final Verdict

`hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closed_with_constraints`
