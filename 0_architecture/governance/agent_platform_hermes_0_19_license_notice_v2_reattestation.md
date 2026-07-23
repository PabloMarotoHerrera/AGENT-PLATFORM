# P15.M2A - Hermes 0.19 License and Notice V2 Integrity Re-attestation

Status: P15.M2A license and notice integrity re-attested with constraints.

Final verdict: `hermes_0_19_license_notice_reconciliation_v2_reattested_with_constraints`

## Ticket Authority

P15.M2A performs a bounded integrity re-attestation of the accepted P15.M2 license and notice reconciliation against the canonical `agent-platform-git-tree-sha256-v2` authority established by P15.M1D.

P15.M2A does not repeat or alter the substantive P15.M2 license analysis. It does not modify the license manifest, any path under `2_products`, import or exclusion manifests, modification registers, dependency manifests, lockfiles, utility code, tests, Graphify output or external sources.

Authorized P15.M2A candidates:

| Path | Disposition |
| --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_license_notice_reconciliation.md` | integrity-authority and sequencing update only |
| `0_architecture/governance/agent_platform_hermes_0_19_license_notice_v2_reattestation.md` | created durable re-attestation record |

## Branch Integration State

| Field | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M2` |
| Branch | `p15.m2-license-notice` |
| Dynamic HEAD | `5534d38a9af363f91767e4582e048b9c46787188` |
| Branch remote | `origin/p15.m2-license-notice` |
| Branch remote SHA | `5534d38a9af363f91767e4582e048b9c46787188` |
| Migration head | `525e1a13a0199e7648ccc332c1c06103bc269aaf` |
| HEAD equals branch remote | `true` |
| Migration head is ancestor of HEAD | `true` |
| P15.M1D commit is ancestor of HEAD | `true` |
| Required P15.M1D commit | `525e1a13a0199e7648ccc332c1c06103bc269aaf` |
| Index empty at start | `true` |
| Staged files at start | `0` |
| Tracked working tree clean at start | `true` |

## Committed Prerequisites

| Path | Required state | Last commit |
| --- | --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_license_notice_reconciliation.md` | tracked, committed in HEAD, locally unmodified, unstaged | `b6fa5b5d9d89aec710fe04e24bc904512e5102c7` |
| `0_architecture/governance/agent_platform_hermes_0_19_license_manifest.tsv` | tracked, committed in HEAD, locally unmodified, unstaged | `b6fa5b5d9d89aec710fe04e24bc904512e5102c7` |
| `0_architecture/governance/agent_platform_hermes_0_19_integrity_algorithm_canonicalization.md` | tracked, committed in HEAD, locally unmodified, unstaged | `525e1a13a0199e7648ccc332c1c06103bc269aaf` |
| `10_scripts/governance/pepper_baseline_integrity.py` | tracked, committed in HEAD, locally unmodified, unstaged | `525e1a13a0199e7648ccc332c1c06103bc269aaf` |
| `12_tests/governance/test_pepper_baseline_integrity.py` | tracked, committed in HEAD, locally unmodified, unstaged | `525e1a13a0199e7648ccc332c1c06103bc269aaf` |

Required verdicts present:

- `hermes_0_19_license_notice_reconciliation_ready_with_constraints`;
- `hermes_0_19_baseline_integrity_algorithm_canonicalized`.

## Original P15.M2 Artifacts

Original P15.M2 governance artifact:

```yaml
path: 0_architecture/governance/agent_platform_hermes_0_19_license_notice_reconciliation.md
originating_commit: b6fa5b5d9d89aec710fe04e24bc904512e5102c7
exact_HEAD_blob_bytes_before_P15_M2A: 22589
exact_HEAD_blob_SHA256_before_P15_M2A: 8fc54fc09bda04969f5aade207f2430f3dc957966caebb7b63286486ebf993ad
```

License manifest artifact:

```yaml
path: 0_architecture/governance/agent_platform_hermes_0_19_license_manifest.tsv
originating_commit: b6fa5b5d9d89aec710fe04e24bc904512e5102c7
exact_HEAD_blob_bytes: 15674
exact_HEAD_blob_SHA256: 5643d432579493a467aec17c0caf742f19d0f5bb9d9e54119b3c67c0845605fb
```

## Canonical Utility And Exact CLI

Canonical utility:

```text
10_scripts/governance/pepper_baseline_integrity.py
```

Exact CLI used:

```text
python 10_scripts/governance/pepper_baseline_integrity.py --repo-root . --product-root 2_products/pepper-agent --mode all --format json
```

The utility operates on repository `HEAD` and uses exact committed Git blob bytes.

## Dedicated Utility Test Result

Authorized test command:

```text
python -m unittest discover -s "12_tests/governance" -p "test_pepper_baseline_integrity.py"
```

Result:

```text
Ran 14 tests in 0.003s
OK
```

Required outcome:

```yaml
tests_run: 14
failures: 0
errors: 0
golden_vector_match: true
```

## Canonical V2 Identity

Candidate:

```yaml
algorithm: agent-platform-git-tree-sha256-v2
files: 6684
bytes: 148145642
SHA256: fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b
match: true
```

Imported payload:

```yaml
algorithm: agent-platform-git-tree-sha256-v2
files: 6681
bytes: 145406255
SHA256: 3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073
match: true
```

Baseline record:

```yaml
algorithm: sha256-git-blob-v1
path: 2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json
bytes: 25333
SHA256: 5aa7d9582e8036e66a9a81be772aa75b3cb930a978c0128bc0a6b2585baa0fea
match: true
```

## License Manifest Validation

The license manifest was inspected from the exact committed Git blob and remains unchanged.

| Check | Result |
| --- | ---: |
| Rows | 30 |
| Columns | 17 |
| Duplicate record IDs | 0 |
| Blank mandatory fields | 0 |
| Invalid classifications | 0 |
| Unresolved rows without explicit status | 0 |
| Trailing whitespace lines | 0 |

Required preservation:

```yaml
license_manifest_modified: false
license_manifest_blob_hash_before_equals_after: true
license_manifest_changes: 0
license_evidence_changes: 0
```

## Historical Integrity Classification

| Digest | Classification | Status |
| --- | --- | --- |
| `27b457b65d8a89bb5c39041bc43b82e6f46c4924c1554f5a1c0fcc7682c19bf7` | `superseded_ambiguous` | historical P15.M1C candidate aggregate, not current authority |
| `03295db99b2204ac962619251289e145432fe32946ee7efad6201dd0742e4ce6` | `superseded_ambiguous` | historical P15.M1C payload aggregate, not current authority |
| `92b15fb828d105dbd144599c0a49fcef454646667b53b6de227c9716e1aa234c` | `superseded_baseline_record` | pre-P15.M1D baseline-record hash |

Unexplained identities: `0`.

## Preserved Component Decisions

The following P15.M2 decisions remain present and unchanged:

| Decision | Status |
| --- | --- |
| internal source development | `ready` |
| modified source redistribution | `ready_with_notices` |
| Desktop binary redistribution | `blocked_pending_review` |
| Dashboard built asset redistribution | `blocked_pending_review` |
| container image publication | `blocked_pending_review` |
| public Pepper branding | `blocked_pending_trademark_review` |
| provider service use | `separate_terms_required` |
| PowerPoint skill | `remain_excluded` |

Preserved restrictions and evidence:

- `258` incomplete dependency-license evidence records remain recorded;
- future notice path remains `2_products/pepper-agent/THIRD_PARTY_NOTICES.md`;
- future notice remains subject to later modification-register entry;
- Nous Research and Hermes trademark restrictions remain active;
- public binary distribution remains unauthorized;
- container publication remains unauthorized;
- provider and OAuth terms remain separate from source-license permission.

## Future Notice Contract

The future `2_products/pepper-agent/THIRD_PARTY_NOTICES.md` contract remains unchanged. P15.M2A does not create it, does not register it and does not alter its required sections. Future notice application remains dependency-gated and must preserve the P15.M2 distribution restrictions.

## Downstream Integration Consequence

P15.M3 may restart using the V2 candidate, payload and baseline-record identities. P15.M4 may proceed using V2. P15.M5 remains gated pending integration of the parallel lanes.

Public binary distribution, public container publication, live OAuth, provider calls and inference remain unauthorized.

## Rollback And Rejection

If P15.M2A is rejected before commit, remove only:

```text
0_architecture/governance/agent_platform_hermes_0_19_license_notice_v2_reattestation.md
```

and revert only the P15.M2A integrity-authority addendum in:

```text
0_architecture/governance/agent_platform_hermes_0_19_license_notice_reconciliation.md
```

Do not modify the license manifest, `2_products/**`, utility code, tests, external sources, dependency manifests or lockfiles.

## Final Integrity

```yaml
candidate_before_equals_after: true
payload_before_equals_after: true
baseline_record_before_equals_after: true
Pepper_product_changes: 0
Pepper_register_changes: 0
current_product_changes: 0
license_manifest_changes: 0
dependency_or_lock_changes: 0
external_source_tracked_changes: 0
Graphify_commands: 0
dependency_installations: 0
registry_queries: 0
builds: 0
product_tests: 0
runtime_starts: 0
Docker_starts: 0
WSL_mutations: 0
OAuth_flows: 0
credential_reads: 0
provider_calls: 0
inference_calls: 0
```

Final verdict:

```text
hermes_0_19_license_notice_reconciliation_v2_reattested_with_constraints
```
