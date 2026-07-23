# P15.M1D - Hermes 0.19 Integrity Algorithm Canonicalization

Status: P15.M1D canonicalization complete with constraints.

Final verdict: `hermes_0_19_baseline_integrity_algorithm_canonicalized`

## Ticket Authority

P15.M1D resolves the P15.M3 integrity blocker `P15.M1D-CANONICALIZATION-CONTRACT-INCOMPLETE` by creating one canonical executable aggregate algorithm for the Hermes Agent 0.19.0-derived Pepper baseline.

P15.M1D is authorized to create and update exactly these paths:

| Path | Role |
| --- | --- |
| `10_scripts/governance/pepper_baseline_integrity.py` | final canonical utility authority |
| `12_tests/governance/test_pepper_baseline_integrity.py` | final canonical unit-test authority |
| `0_architecture/governance/agent_platform_hermes_0_19_integrity_algorithm_canonicalization.md` | this governance record |
| `2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json` | baseline metadata update only |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline.md` | downstream-authority addendum |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline_storage_reconciliation.md` | downstream-authority addendum |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline_commit_finalization.md` | downstream-authority addendum |

P15.M1D removes the rejected uncommitted paths:

```text
10_scripts/hermes/agent_platform_git_tree_integrity_v2.py
12_tests/hermes/test_agent_platform_git_tree_integrity_v2.py
0_architecture/governance/agent_platform_hermes_0_19_product_baseline_integrity_algorithm_v2.md
```

No compatibility wrappers or duplicate implementations remain.

## P15.M3 Blocker

P15.M3 reproduced the P15.M1C candidate and payload file counts and byte counts, and reproduced the pre-correction baseline-record SHA-256. P15.M3 did not reproduce the P15.M1C aggregate candidate and payload SHA-256 values.

The blocker was correctly classified as aggregate-algorithm ambiguity, not product payload drift:

| Scope | P15.M1C files | P15.M1C bytes | P15.M3 files | P15.M3 bytes | Count/byte result |
| --- | ---: | ---: | ---: | ---: | --- |
| Candidate excluding baseline record | 6684 | 148145642 | 6684 | 148145642 | matched |
| Included/transformed payload | 6681 | 145406255 | 6681 | 145406255 | matched |
| Baseline record | not_applicable | 20517 | not_applicable | 20517 | matched |

## Historical Divergence Diagnosis

The exact cause of both aggregate divergences is an underspecified historical aggregate contract. P15.M1C recorded aggregate SHA-256 values under `agent-platform-git-tree-sha256-v1` labels but did not commit a canonical executable implementation that fixed all byte-stream choices.

The missing choices were material:

- product-relative path basis;
- exact UTF-8 Git path bytes;
- no Unicode normalization;
- no case folding;
- unsigned raw path-byte lexical ordering;
- exact NUL field separators;
- exact LF record terminators;
- no additional final terminator.

P15.M1D fixes those choices. The historical file and byte counts remain valid evidence. The historical aggregate SHA-256 values are no longer downstream authority.

## Canonical V2 Specification

Algorithm identifier:

```text
agent-platform-git-tree-sha256-v2
```

Required inputs:

- exact committed Git blob bytes;
- product-relative UTF-8 Git path bytes;
- no Unicode normalization;
- no case folding;
- unsigned raw path-byte lexical ordering;
- lowercase SHA-256 hex.

Record format:

```text
path_bytes + NUL + byte_count_ascii + NUL + lowercase_content_SHA256_ascii + LF
```

There is one LF record terminator per record and no additional final terminator.

Candidate scope excludes only:

```text
AGENT_PLATFORM_UPSTREAM_BASELINE.json
```

Payload scope is selected from the committed `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` blob. Included payload classifications are exactly:

```text
included_byte_exact
included_canonical_text_lf
transformed_by_canonical_compliance_rule
```

Excluded rows are omitted. Duplicate included destination paths and missing included destinations are hard failures.

## Final Utility

Final utility authority:

```text
10_scripts/governance/pepper_baseline_integrity.py
```

The utility uses only Python standard-library modules and read-only Git commands. It does not import Pepper or Hermes product modules and does not read checked-out product files for identity.

Required command shape:

```text
python 10_scripts/governance/pepper_baseline_integrity.py --repo-root <repo> --product-root 2_products/pepper-agent --format json
```

## Test Map

Final test authority:

```text
12_tests/governance/test_pepper_baseline_integrity.py
```

Exact required command:

```text
python -m unittest discover -s 12_tests/governance -p test_pepper_baseline_integrity.py
```

Result:

```text
Ran 14 tests in 0.005s
OK
```

Required behavior map:

| Required behavior | Test method |
| --- | --- |
| golden record-stream vector | `test_01_golden_record_stream_vector` |
| product-root prefix exclusion | `test_02_product_root_prefix_exclusion` |
| raw byte lexical ordering | `test_03_raw_byte_lexical_ordering` |
| case sensitivity | `test_04_case_sensitivity` |
| exact NUL and LF delimiters | `test_05_exact_nul_and_lf_delimiters` |
| no extra final terminator | `test_06_no_extra_final_terminator` |
| candidate baseline-record exclusion | `test_07_candidate_baseline_record_exclusion` |
| payload manifest selection | `test_08_payload_manifest_selection` |
| excluded-row omission | `test_09_excluded_row_omission` |
| duplicate destination rejection | `test_10_duplicate_destination_rejection` |
| missing destination rejection | `test_11_missing_destination_rejection` |
| checkout EOL independence | `test_12_checkout_eol_independence` |
| different absolute worktree paths produce identical output | `test_13_different_absolute_worktree_paths_produce_identical_output` |
| working-tree modifications do not affect HEAD-based identity | `test_14_working_tree_modifications_do_not_affect_head_identity` |

Golden vector:

```yaml
expected: 54618ecd1f0557162c91e8f1a0e4851176d75e2f3385157ef8aabd8fceb9cd8c
actual: 54618ecd1f0557162c91e8f1a0e4851176d75e2f3385157ef8aabd8fceb9cd8c
result: matched
```

## Cross-Worktree Validation

The final utility was run read-only against the same committed `HEAD` in three worktrees.

| Worktree | HEAD | Candidate files | Candidate bytes | Candidate SHA-256 | Payload files | Payload bytes | Payload SHA-256 | Pre-update baseline-record SHA-256 |
| --- | --- | ---: | ---: | --- | ---: | ---: | --- | --- |
| `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M` | `02598c0b737d54e688e74a58ff4fb0d39d4bbd8c` | 6684 | 148145642 | `fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b` | 6681 | 145406255 | `3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073` | `92b15fb828d105dbd144599c0a49fcef454646667b53b6de227c9716e1aa234c` |
| `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M3` | `02598c0b737d54e688e74a58ff4fb0d39d4bbd8c` | 6684 | 148145642 | `fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b` | 6681 | 145406255 | `3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073` | `92b15fb828d105dbd144599c0a49fcef454646667b53b6de227c9716e1aa234c` |
| `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M4` | `02598c0b737d54e688e74a58ff4fb0d39d4bbd8c` | 6684 | 148145642 | `fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b` | 6681 | 145406255 | `3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073` | `92b15fb828d105dbd144599c0a49fcef454646667b53b6de227c9716e1aa234c` |

Cross-worktree candidate match: `true`.

Cross-worktree payload match: `true`.

Cross-worktree baseline-record match: `true`.

## Final V2 Identities

Candidate:

```yaml
algorithm: agent-platform-git-tree-sha256-v2
files: 6684
bytes: 148145642
SHA256: fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b
excluded_paths:
  - AGENT_PLATFORM_UPSTREAM_BASELINE.json
```

Payload:

```yaml
algorithm: agent-platform-git-tree-sha256-v2
files: 6681
bytes: 145406255
SHA256: 3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073
```

Baseline-record hashes:

```yaml
old_baseline_record_SHA256: 92b15fb828d105dbd144599c0a49fcef454646667b53b6de227c9716e1aa234c
new_candidate_baseline_record_SHA256: 5aa7d9582e8036e66a9a81be772aa75b3cb930a978c0128bc0a6b2585baa0fea
new_candidate_baseline_record_bytes: 25333
stored_inside_record: false
```

The new baseline-record SHA-256 is a pre-commit content hash for the final candidate metadata update and is recorded externally only. It is not stored inside `AGENT_PLATFORM_UPSTREAM_BASELINE.json`.

## Historical Digest Classification

| Digest | Classification | Explanation |
| --- | --- | --- |
| `27b457b65d8a89bb5c39041bc43b82e6f46c4924c1554f5a1c0fcc7682c19bf7` | `superseded_ambiguous` | Historical P15.M1C candidate aggregate with matching files and bytes but no canonical executable byte-stream contract. |
| `fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b` | `reproduced_by_v2` | Final v2 candidate aggregate reproduced across P15M, P15M3 and P15M4. |
| `03295db99b2204ac962619251289e145432fe32946ee7efad6201dd0742e4ce6` | `superseded_ambiguous` | Historical P15.M1C payload aggregate with matching files and bytes but no canonical executable byte-stream contract. |
| `3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073` | `reproduced_by_v2` | Final v2 payload aggregate reproduced across P15M, P15M3 and P15M4. |
| `0eec7b33f97ba13f66b59d1b2cf3e1a66a26c7d90bfbd0ee5d88a8587cefc727` | `explained_legacy_variant` | Pre-commit projection before final Git LF normalization of the header-only modification register. |
| `3c6f155eba3f01ad4ee924ba62c462de1cdb10fdc1f3099daa8ed1d82a9b912d` | `explained_legacy_variant` | Historical checkout-realization digest based on working-tree bytes, not committed Git blob bytes. |

Unexplained digest count: `0`.

## Downstream Re-Attestation

After P15.M1D is committed, downstream lanes must verify:

```yaml
committed_baseline_record_SHA256: 5aa7d9582e8036e66a9a81be772aa75b3cb930a978c0128bc0a6b2585baa0fea
candidate_integrity_v2_SHA256: fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b
payload_integrity_v2_SHA256: 3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073
```

P15.M2, P15.M3 and P15.M4 must not use P15.M1C v1 aggregate digests as current authority. P15.M17 owns future governed upstream update-planner use, enforcement and revision of this utility.

## Preservation

| Boundary | Result |
| --- | ---: |
| implementation payload changes | 0 |
| import manifest changes | 0 |
| exclusion manifest changes | 0 |
| modification register changes | 0 |
| dependency or lock changes | 0 |
| current product changes | 0 |
| external source changes | 0 |
| Graphify commands | 0 |
| product runtime executions | 0 |
| Docker, WSL or VPS actions | 0 |
| OAuth, provider or inference actions | 0 |
| Git staging, commits or pushes by agent | 0 |

## Final Candidate Set

Required final candidate paths:

```text
10_scripts/governance/pepper_baseline_integrity.py
12_tests/governance/test_pepper_baseline_integrity.py
0_architecture/governance/agent_platform_hermes_0_19_integrity_algorithm_canonicalization.md
2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json
0_architecture/governance/agent_platform_hermes_0_19_product_baseline.md
0_architecture/governance/agent_platform_hermes_0_19_product_baseline_storage_reconciliation.md
0_architecture/governance/agent_platform_hermes_0_19_product_baseline_commit_finalization.md
```

Candidate files: `7`.

Unexpected candidates: `0`.

Forbidden rejected paths remaining: `0`.

## Final Validation

```yaml
canonical_utility_syntax: valid
all_required_test_behaviors_covered: true
test_failures: 0
test_errors: 0
golden_vector_match: true
cross_worktree_candidate_match: true
cross_worktree_payload_match: true
cross_worktree_baseline_record_match: true
JSON_valid: true
Markdown_trailing_whitespace: 0
Python_trailing_whitespace: 0
git_diff_check: clean
index_empty: true
staged_files: none
commits_by_agent: 0
pushes_by_agent: 0
```

Final verdict:

```text
hermes_0_19_baseline_integrity_algorithm_canonicalized
```
