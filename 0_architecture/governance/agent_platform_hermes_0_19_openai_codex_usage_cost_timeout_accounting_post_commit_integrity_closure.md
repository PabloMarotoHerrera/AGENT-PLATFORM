# AGENT PLATFORM Hermes 0.19 OpenAI Codex Usage Cost Timeout Accounting Post-Commit Integrity Closure

Status: P15.5R post-commit integrity validation closed with constraints.

Final verdict: `hermes_0_19_openai_codex_usage_cost_timeout_accounting_post_commit_integrity_closed_with_constraints`.

Verdict meaning: the committed P15.5 usage, cost and timeout accounting addition was revalidated after commit and push. This record is governance-only and does not claim live provider execution, real usage retrieval, billing retrieval, quota retrieval, worker execution, runtime activation, credential reads, persistence integration, dashboard rendering or production readiness.

## Repository Authority

| Gate | Result |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| Local HEAD | `777c9d02c6f6d347f36c473f6e11c2f727e6d5cf` |
| Remote branch HEAD | `777c9d02c6f6d347f36c473f6e11c2f727e6d5cf` |
| P15.5 commit message | `P15.5 Add usage cost and timeout accounting` |
| P15.5 parent | `f3dfebf7f63d0d6bb3b79d021ec358b186ba9336` |
| P15.MR ancestor check | passed |
| P15.5 governance verdict | `hermes_0_19_openai_codex_usage_cost_timeout_accounting_ready_with_constraints` |
| P15.MR prerequisite verdict | `hermes_0_19_local_migration_release_and_deferred_vps_handoff_closed_with_constraints` |

## Ticket Expectation Correction

```yaml
ticket_expectation_correction:
  original_expected_conflict_owner:
    AGENT_PLATFORM_secure_provider_worker_owner
  committed_canonical_conflict_owner:
    AGENT_PLATFORM_provider_accounting_owner
  repository_defect:
    false
  committed_file_correction_required:
    false
```

Interpretation:

- `AGENT_PLATFORM_provider_accounting_owner` owns conflicts in the dedicated P15.5 provider-accounting package, tests and documentation.
- `AGENT_PLATFORM_secure_provider_worker_owner` remains responsible for broader secure worker enablement but is not the file-level conflict owner for these accounting additions.
- No repository correction is required.
- The mismatch originated in the P15.5R ticket expectation, not in the P15.5 commit.

## Commit Path Set

P15.5 introduced exactly the expected committed path set: 9 added paths and 2 modified product governance TSV files.

| Status | Path |
| --- | --- |
| Added | `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_usage_cost_timeout_accounting.md` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` |
| Added | `2_products/pepper-agent/docs/agent-platform/provider_usage_cost_timeout_accounting.md` |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/provider_accounting/__init__.py` |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/provider_accounting/accounting.py` |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/provider_accounting/contracts.py` |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/provider_accounting/enums.py` |
| Added | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_accounting_contracts.py` |
| Added | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_accounting_normalization.py` |
| Added | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_timeout_accounting.py` |

## Modification Register Closure

```yaml
P15_5_rows: 8
required_IDs:
  - P15.5-001
  - P15.5-002
  - P15.5-003
  - P15.5-004
  - P15.5-005
  - P15.5-006
  - P15.5-007
  - P15.5-008
conflict_owner: AGENT_PLATFORM_provider_accounting_owner
mixed_conflict_owners: 0
duplicate_modification_IDs: 0
duplicate_P15_5_paths: 0
committed_blob_SHA256_matches: true
all_other_required_row_fields: unchanged_and_valid
```

Required row-field values remained valid for all eight P15.5 rows: `owner_ticket=P15.5`, `change_class=AGENT_PLATFORM_product_addition`, `baseline_upstream_commit=3ef6bbd201263d354fd83ec55b3c306ded2eb72a`, `baseline_source_object_or_none=none`, `baseline_source_sha256_or_none=none`, `upstream_disposition=retain_product_divergence`, `rollback_target=delete_path` and `status=implemented_pending_human_approval`.

## Import Manifest Closure

```yaml
P15_5_manifest_rows: 8
paths_match: true
classification: AGENT_PLATFORM_product_addition
payload_inclusion: false
source_fields_not_applicable: true
destination_SHA256_matches: true
duplicate_P15_5_manifest_paths: 0
```

The P15.5 import-manifest rows are product-local additions with no upstream source object and remain excluded from the payload identity calculation.

## Product Identity

| Identity | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Pre-P15.5 candidate | `6768` | `149234356` | `a71af0be624cb3f00b37d651248717c38f5bed18e460c6f159636c75a8875df3` |
| Post-P15.5 candidate | `6776` | `149294378` | `38545fecd8dbf5c8823c4efec47d0c9dca4e5cc0666a72283f9797ded5d2fd08` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Candidate identity changed only by the governed P15.5 product additions. Payload identity and baseline-record identity remained unchanged.

## Semantic Closure

| Gate | Result |
| --- | --- |
| Usage semantics | passed |
| Cost semantics | passed |
| Timeout semantics | passed |
| Accounting identity | passed |
| Worker-result linkage | passed |

Usage accounting accepts synthetic Codex Responses and synthetic Codex app-server usage shapes, normalizes token buckets into bounded non-secret counters, records explicit provider-omitted evidence for missing usage and excludes raw request bodies, raw response bodies, provider headers and credential metadata.

Cost accounting remains `subscription_included`, records `amount_usd=0` for the included marginal request posture, marks exact marginal request cost unavailable and performs no pricing, usage, quota or billing lookup.

Timeout accounting uses injected UTC timestamps, fixed timeout budgets and deterministic elapsed-time evidence. Timed-out records require a timeout stage, while completed, failed and cancelled records cannot carry timeout-stage evidence.

Accounting identity remains fixed to `accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1`, `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1`, `worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1`, model `gpt-5.5` and one provider call maximum per accounting record.

Worker-result linkage validates `usage_record_id`, `request_id`, `runtime_id` and `correlation_id` between a `ProviderAccountingRecord` and a `BoundedProviderWorkerResult`. Successful links produce bounded matched-link evidence; mismatches raise bounded errors without raw output text.

## Validation Evidence

| Gate | Command summary | Result |
| --- | --- | --- |
| Governance integrity tests | `python -m unittest discover -s 12_tests/governance -p test_pepper_baseline_integrity.py` | `14 passed` |
| Isolated accounting suite | `python -m pytest -p no:cacheprovider` on the three P15.5 accounting test files | `19 passed, 3 warnings` |
| Combined accounting and worker contracts | `python -m pytest -p no:cacheprovider` on accounting tests plus `test_agent_platform_provider_worker_contracts.py` | `31 passed, 3 warnings` |
| Prior provider/credential/worker regression | `python -m pytest -p no:cacheprovider` on the P15.M8 provider, credential and worker regression inventory | `119 passed, 3 warnings` |
| Ruff check | `python -m ruff check` on the seven P15.5 Python files | passed |
| Ruff format check | `python -m ruff format --check` on the seven P15.5 Python files | passed |
| Ty availability | `python -m ty check` and `where ty` | unavailable: `No module named ty`, no executable found |
| Operational-authority scan | Provider-accounting source scan for provider, network, subprocess, filesystem write, credential and billing authority tokens | `0` matches |
| Secret scan | P15.5 source, tests and documentation scan for secret-like literals or assignments | `0` matches |

Warning classification: all three warnings are the inherited P15.M8 Pydantic protected-namespace warnings for `model_id`, `model_policy` and `model_list_calls_per_request_maximum`. P15.5 provider-accounting contracts set `protected_namespaces=()` and introduced `0` new P15.5 warnings.

## No-Execution Gate

| Counter | Value |
| --- | ---: |
| Docker containers started | `0` |
| OAuth attempts | `0` |
| Real credentials read | `0` |
| Credential leases created | `0` |
| Provider dispatches | `0` |
| Inference calls | `0` |
| Model-list calls | `0` |
| Usage API calls | `0` |
| Quota API calls | `0` |
| Billing API calls | `0` |
| Worker starts | `0` |
| Tool calls | `0` |
| MCP calls | `0` |
| Remote hosts contacted | `0` |
| Graphify runs | `0` |
| Git staging operations | `0` |
| Git commits | `0` |
| Git pushes | `0` |

## Repository Mutation Closure

No committed product source, product tests, product documentation, P15.5 governance record, TSV register, import manifest, baseline record, dependency file or committed repository file was modified during P15.5R.

Expected final P15.5R candidate state after this governance-only record is created:

```yaml
candidate_files: 1
unexpected_candidates: 0
tracked_changes: 0
staged_files: 0
```

The single candidate file is `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_usage_cost_timeout_accounting_post_commit_integrity_closure.md`.

## Residual Constraints

P15.5R does not add runtime wiring, persistent storage, dashboard rendering, live provider execution, usage retrieval, quota retrieval, billing retrieval, model pricing, credential access, Docker activity, remote activity, Graphify execution or production activation. P15.6 remains blocked until this P15.5R governance-only closure is reviewed and integrated by a human.
