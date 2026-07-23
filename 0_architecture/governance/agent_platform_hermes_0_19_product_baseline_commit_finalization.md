# P15.M1C - Hermes 0.19 Product Baseline Commit Finalization

Status: P15.M1C post-commit portable integrity finalized with constraints.

Final verdict: `hermes_0_19_product_baseline_committed_integrity_finalized`

## P15.M1D Canonical Integrity Addendum

P15.M1D does not change the P15.M1C diagnosis that the one-byte pre-commit drift was final Git LF normalization of `AGENT_PLATFORM_MODIFICATIONS.tsv`. P15.M1D separately resolves the later P15.M3 aggregate-algorithm ambiguity.

P15.M1D establishes `agent-platform-git-tree-sha256-v2` as the only downstream aggregate authority. The v2 algorithm is executable at `10_scripts/governance/pepper_baseline_integrity.py` and is tested by `12_tests/governance/test_pepper_baseline_integrity.py`.

Downstream gates must use:

```yaml
candidate_integrity_v2:
  files: 6684
  bytes: 148145642
  SHA256: fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b

payload_integrity_v2:
  files: 6681
  bytes: 145406255
  SHA256: 3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073

baseline_record_integrity:
  old_SHA256: 92b15fb828d105dbd144599c0a49fcef454646667b53b6de227c9716e1aa234c
  new_candidate_SHA256_recorded_externally: 5aa7d9582e8036e66a9a81be772aa75b3cb930a978c0128bc0a6b2585baa0fea
```

The P15.M1C candidate digest `27b457b65d8a89bb5c39041bc43b82e6f46c4924c1554f5a1c0fcc7682c19bf7` and payload digest `03295db99b2204ac962619251289e145432fe32946ee7efad6201dd0742e4ce6` are preserved as `superseded_ambiguous`, not current authority. The pre-commit digest `0eec7b33f97ba13f66b59d1b2cf3e1a66a26c7d90bfbd0ee5d88a8587cefc727` remains an `explained_legacy_variant` caused by final Git LF normalization.

After P15.M1D is committed, downstream lanes must verify the committed blob SHA-256 for `2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json` equals `5aa7d9582e8036e66a9a81be772aa75b3cb930a978c0128bc0a6b2585baa0fea` before using the candidate.

## Ticket Authority

P15.M1C finalizes the Hermes Agent 0.19.0-derived Pepper baseline candidate identity after P15.M1B was committed at `4b69f99b029a677f619b29b5c96a23e2131e1a38`.

P15.M1C does not change imported implementation payload, does not change the current canonical product, does not forward-port Pepper functionality, does not install dependencies, does not build or run source, does not run Graphify, and does not stage, commit or push.

Authorized update paths:

| Path | Disposition |
| --- | --- |
| `2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json` | updated candidate integrity metadata only |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline.md` | updated portable integrity evidence |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline_storage_reconciliation.md` | updated with post-commit addendum |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline_commit_finalization.md` | created durable P15.M1C record |

## Start Gate

| Field | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| Start HEAD | `4b69f99b029a677f619b29b5c96a23e2131e1a38` |
| Branch remote SHA | `4b69f99b029a677f619b29b5c96a23e2131e1a38` |
| HEAD equals branch remote at start | `true` |
| Index empty at start | `true` |
| Tracked working tree clean at start | `true` |
| P15.M1B verdict present | `hermes_0_19_product_baseline_portable_integrity_ready` |
| Pepper `.gitattributes` rule present | `2_products/pepper-agent/** text=auto eol=lf` |

## One-Byte Diagnosis

P15.M2 correctly blocked because the P15.M1B candidate integrity value was computed before final commit propagation. The only identified difference was the committed storage of the header-only Pepper modification register.

| Field | Value |
| --- | --- |
| Path | `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` |
| Blob OID | `20fc02c10a5b953d7fd6e23ee596b1f6c17f8794` |
| Committed blob bytes | 348 |
| Committed blob SHA-256 | `7f941e9cd6bad0defe6aa7c397727182395575452727824cec2f1cd1f27a9592` |
| Worktree bytes | 349 |
| Worktree SHA-256 | `d6a45a7dc4b509a47f1b1ec91835395d6a8231b4c82b3082860dcb13cd75a13d` |
| Line count | 1 |
| Data rows | 0 |
| Columns | 18 |
| Committed header equals worktree header | `true` |
| Committed last bytes | `65 66 65 72 65 6e 63 65 09 73 74 61 74 75 73 0a` |
| Worktree last bytes | `66 65 72 65 6e 63 65 09 73 74 61 74 75 73 0d 0a` |
| Effective attributes | `text: auto`, `eol: lf`, `working-tree-encoding: unspecified` |
| `git ls-files --eol` | `i/lf w/crlf attr/text=auto eol=lf` |

Conclusion: the one-byte difference is final-line EOL normalization only. There is no semantic, schema, or data-row difference. The manifests and product payload must not be modified to correct it.

## Final Candidate Integrity

Committed-final portable candidate identity:

| Field | Value |
| --- | --- |
| Status | `committed_final` |
| Representation | `canonical_committed_candidate_except_baseline_record` |
| Content basis | exact HEAD Git blob bytes |
| Algorithm | `agent-platform-git-tree-sha256-v1-excluding-baseline-record` |
| Scope | all committed blobs under `2_products/pepper-agent` except `AGENT_PLATFORM_UPSTREAM_BASELINE.json` |
| Excluded self-referential path | `AGENT_PLATFORM_UPSTREAM_BASELINE.json` |
| File count | 6684 |
| Byte count | 148145642 |
| SHA-256 | `27b457b65d8a89bb5c39041bc43b82e6f46c4924c1554f5a1c0fcc7682c19bf7` |
| Authoritative | `true` |
| Portable across worktrees | `true` |

The candidate integrity was recomputed twice from Git objects before metadata update:

| Method | Files | Bytes | SHA-256 | Match |
| --- | ---: | ---: | --- | --- |
| batch | 6684 | 148145642 | `27b457b65d8a89bb5c39041bc43b82e6f46c4924c1554f5a1c0fcc7682c19bf7` | `true` |
| per_blob | 6684 | 148145642 | `27b457b65d8a89bb5c39041bc43b82e6f46c4924c1554f5a1c0fcc7682c19bf7` | `true` |

Superseded pre-commit candidate identity:

| Field | Value |
| --- | --- |
| Authority | `provisional` |
| File count | 6684 |
| Byte count | 148145643 |
| SHA-256 | `0eec7b33f97ba13f66b59d1b2cf3e1a66a26c7d90bfbd0ee5d88a8587cefc727` |
| Supersession reason | computed before final index/commit LF normalization of `AGENT_PLATFORM_MODIFICATIONS.tsv` |

## Payload Integrity

The payload identity is unchanged by P15.M1C.

| Field | Value |
| --- | --- |
| Algorithm | `agent-platform-git-tree-sha256-v1` |
| Scope | included and transformed upstream payload rows only |
| Metadata included | `false` |
| File count | 6681 |
| Byte count | 145406255 |
| SHA-256 | `03295db99b2204ac962619251289e145432fe32946ee7efad6201dd0742e4ce6` |
| Missing destinations | 0 |
| Destination hash mismatches | 0 |

## Baseline Record Hash

The baseline JSON record is excluded from candidate integrity to avoid self-reference. Its exact file hash is stored only in governance.

| Field | Value |
| --- | --- |
| Baseline record path | `2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json` |
| Baseline record SHA-256 before P15.M1C | `7318f257f086a6f09be077eed3ec4f493ce72d0d9dc16fe313f6e33096613848` |
| Baseline record SHA-256 after P15.M1C | `92b15fb828d105dbd144599c0a49fcef454646667b53b6de227c9716e1aa234c` |
| Stored inside itself | `false` |

## Manifest Counts

| Field | Value |
| --- | ---: |
| Import manifest rows | 6737 |
| `included_byte_exact` | 160 |
| `included_canonical_text_lf` | 6517 |
| `transformed_by_canonical_compliance_rule` | 4 |
| `excluded_by_canonical_policy` | 56 |
| `blocked_unresolved` | 0 |
| Duplicate source paths | 0 |
| Duplicate destination paths | 0 |

## Preservation

| Boundary | Result |
| --- | ---: |
| imported implementation payload files modified | 0 |
| current canonical product changes | 0 |
| `.gitattributes` changes | 0 |
| import manifest changes | 0 |
| exclusion manifest changes | 0 |
| modification register changes | 0 |
| dependency manifest changes | 0 |
| lockfile changes | 0 |
| external source changes | 0 |
| Graphify commands | 0 |
| dependency installations | 0 |
| builds, tests, lint or runtime starts | 0 |
| Docker, WSL or VPS actions | 0 |
| OAuth, credential, provider or inference actions | 0 |
| Git staging, commits or pushes by agent | 0 |

## Downstream Consequence

P15.M2, P15.M3 and P15.M4 remain paused until P15.M1C is accepted, committed, pushed and fast-forwarded into their worktrees.

Downstream prerequisite gates must use:

```yaml
candidate_integrity_file_count: 6684
candidate_integrity_byte_count: 148145642
candidate_integrity_sha256: 27b457b65d8a89bb5c39041bc43b82e6f46c4924c1554f5a1c0fcc7682c19bf7
candidate_integrity_algorithm: agent-platform-git-tree-sha256-v1-excluding-baseline-record
```

Downstream lanes must not use the superseded P15.M1B pre-commit projection `0eec7b33f97ba13f66b59d1b2cf3e1a66a26c7d90bfbd0ee5d88a8587cefc727`.

## Final Validation

| Check | Result |
| --- | --- |
| JSON valid | `true` |
| Baseline record hash stored outside itself | `true` |
| Committed-final candidate digest recorded | `true` |
| Superseded pre-commit digest retained | `true` |
| Payload digest unchanged | `true` |
| Manifest counts unchanged | `true` |
| Candidate metadata-only scope | `true` |
| Current canonical product unchanged | `true` |
| Runtime boundary preserved | `true` |

Final verdict: `hermes_0_19_product_baseline_committed_integrity_finalized`
