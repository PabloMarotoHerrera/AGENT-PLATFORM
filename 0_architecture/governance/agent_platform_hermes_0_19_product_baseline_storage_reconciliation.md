# P15.M1B - Hermes 0.19 Product Baseline Storage Reconciliation

Status: P15.M1B canonical Git storage correction ready with P15.M1C post-commit finalization addendum.

Final verdict: `hermes_0_19_product_baseline_portable_integrity_ready`

## P15.M1D Canonical Integrity Addendum

P15.M1D resolves the aggregate-algorithm ambiguity discovered by P15.M3. The P15.M1B and P15.M1C file counts and byte counts remain valid, but the P15.M1C aggregate SHA-256 values are not downstream authority.

Only this algorithm is authoritative for downstream gates:

```text
agent-platform-git-tree-sha256-v2
```

The executable authority is:

```text
10_scripts/governance/pepper_baseline_integrity.py
```

Canonical v2 identities:

| Scope | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate excluding `AGENT_PLATFORM_UPSTREAM_BASELINE.json` | 6684 | 148145642 | `fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b` |
| Included/transformed payload | 6681 | 145406255 | `3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073` |
| Pre-correction baseline record | not_applicable | 20517 | `92b15fb828d105dbd144599c0a49fcef454646667b53b6de227c9716e1aa234c` |
| P15.M1D candidate baseline record | not_applicable | 25333 | `5aa7d9582e8036e66a9a81be772aa75b3cb930a978c0128bc0a6b2585baa0fea` |

The old P15.M1C candidate digest `27b457b65d8a89bb5c39041bc43b82e6f46c4924c1554f5a1c0fcc7682c19bf7` and payload digest `03295db99b2204ac962619251289e145432fe32946ee7efad6201dd0742e4ce6` are `superseded_ambiguous`. They are retained only as historical evidence that lacked a canonical executable byte-stream contract. The pre-commit and checkout-realization digests remain `explained_legacy_variant` evidence.

Downstream lanes must re-attest with v2 after the P15.M1D commit. P15.M17 owns future use of this utility in the governed upstream synchronization engine.

P15.M1C addendum verdict: `hermes_0_19_product_baseline_committed_integrity_finalized`

## Ticket Authority

P15.M1B establishes a deterministic Git-storage integrity model for the Hermes Agent 0.19.0-derived Pepper baseline created by P15.M1.

P15.M1B does not change imported implementation payload, does not change the current canonical product, does not forward-port Pepper functionality, does not install dependencies, does not build or run source, does not run Graphify, and does not stage, commit or push.

Authorized candidate paths:

| Path | Disposition |
| --- | --- |
| `.gitattributes` | created with narrow Pepper-only EOL policy |
| `2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json` | updated metadata authority |
| `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | reconciled destination hashes and classifications |
| `2_products/pepper-agent/AGENT_PLATFORM_EXCLUSIONS.tsv` | updated four transformation replacement hashes |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline.md` | updated baseline governance evidence |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline_storage_reconciliation.md` | created durable P15.M1B record |

## Start State

| Field | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| Start HEAD | `26b6d3a5b37f32661d8d17ab6ac703760ff8223f` |
| Branch remote | `origin/p15.m-hermes-0.19-migration` |
| Branch remote SHA | `26b6d3a5b37f32661d8d17ab6ac703760ff8223f` |
| HEAD equals branch remote | `true` |
| Index empty | `true` |
| Tracked working tree clean | `true` |

P15.M2, P15.M3 and P15.M4 remain paused until this correction is accepted, committed, pushed and propagated to their branches.

## P15.M1A Blocker

P15.M1A stopped correctly because P15.M1 had treated checked-out filesystem bytes as portable product identity. A clean P15.M2 worktree produced different checked-out bytes while the same commit produced the same committed Git blobs.

Observed P15.M1A evidence:

| Check | Count |
| --- | ---: |
| destination rows checked | 6681 |
| recorded destination hash mismatches against committed blobs | 6521 |
| invalid `included_byte_exact` classifications against committed blobs | 6517 |
| transformed destination hash mismatches against committed blobs | 4 |
| missing committed destinations | 0 |

The mismatch was caused by Git text normalization. Raw source/worktree files in the P15.M1 lane retained CRLF or mixed EOL realization, while Git stored text blobs with LF.

## EOL Diagnosis

| Evidence | Value |
| --- | --- |
| `core.autocrlf` | `file:C:/Program Files/Git/etc/gitconfig true` |
| `core.eol` | unset |
| Prior root `.gitattributes` | absent |
| Product `.gitattributes` | present, only script and Docker LF rules |
| Prior `.gitignore` effective attributes | `text`, `eol`, `working-tree-encoding` unspecified |
| Prior `.gitignore` EOL in P15M | `i/lf w/mixed` |
| `.gitignore` committed blob SHA-256 | `7cbca4bd2ef10871faab08ebd0c5feb8333c2b7bf78cff5dc1f3074deb055d30` |
| `.gitignore` P15M worktree SHA-256 | `bc2d006f3ff5267ee633f5ce4b5c045b326804af55f54d6beb361a2c1bf18c32` |
| `.gitignore` P15M2 worktree SHA-256 | `78836d313ecc08dd4318ae3090972134158fb6f2386c434b6c0a1e446a48044d` |
| `.gitignore` committed blob bytes | 7858 |
| `.gitignore` P15M worktree bytes | 8013 |
| `.gitignore` P15M2 worktree bytes | 8082 |

The P15M to P15M2 checkout difference is explained by EOL materialization. It is no longer used as product identity.

## Storage Policy

P15.M1B creates the explicit repository-controlled policy:

```gitattributes
2_products/pepper-agent/** text=auto eol=lf
```

Policy effects:

| Scope | Decision |
| --- | --- |
| Pepper text | canonical LF in index and checkout |
| Pepper binary | no content conversion when Git classifies as binary |
| Current canonical product | unchanged |
| External sources | unchanged |
| Repository-wide `* text=auto` | not set |
| Deeper product attributes | compatible; existing product rules already use LF for scripts and Docker files |

No Git global or local configuration was changed.

## Representation Model

| Representation | Content basis | Authority |
| --- | --- | --- |
| raw upstream source | exact archive/source bytes | upstream identity and provenance |
| canonical committed payload | exact committed Git blob bytes | portable product/update comparison |
| checkout realization | local filesystem bytes | non-authoritative diagnostic only |

Destination hashes in `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` now mean exact committed Git blob SHA-256. Working-tree hashes are not stored as product authority.

## Manifest Reconciliation

All destination rows were reconciled against raw source bytes and committed Git blob bytes.

| Classification | Count | Meaning |
| --- | ---: | --- |
| `included_byte_exact` | 160 | raw source SHA-256 equals committed Git blob SHA-256 |
| `included_canonical_text_lf` | 6517 | raw source bytes equal committed Git blob bytes after deterministic CRLF-to-LF canonicalization |
| `transformed_by_canonical_compliance_rule` | 4 | existing P12 semantic transformations with committed LF storage |
| `excluded_by_canonical_policy` | 56 | unchanged exclusions |
| `blocked_unresolved` | 0 | none |

Validation counts:

| Check | Result |
| --- | ---: |
| import manifest rows | 6737 |
| destination rows checked | 6681 |
| missing destinations | 0 |
| duplicate source paths | 0 |
| duplicate destination paths | 0 |
| source hash mismatches | 0 |
| destination hash mismatches after correction | 0 |
| non-EOL content mismatches | 0 |
| transformed rows without canonical rule | 0 |
| blank mandatory fields | 0 |

The four transformed rows now use combined canonical rules in the import manifest:

| Destination | Rule |
| --- | --- |
| `.gitignore` | `P12_tracking_compatibility_rederived_for_candidate+P15_M1B_GIT_TEXT_LF_CANONICALIZATION` |
| `website/docs/reference/skills-catalog.md` | `P12_restricted_powerpoint_catalog_reference_removal+P15_M1B_GIT_TEXT_LF_CANONICALIZATION` |
| `website/i18n/zh-Hans/docusaurus-plugin-content-docs/current/reference/skills-catalog.md` | `P12_restricted_powerpoint_catalog_reference_removal+P15_M1B_GIT_TEXT_LF_CANONICALIZATION` |
| `website/sidebars.ts` | `P12_restricted_powerpoint_sidebar_reference_removal+P15_M1B_GIT_TEXT_LF_CANONICALIZATION` |

`AGENT_PLATFORM_EXCLUSIONS.tsv` remains limited to exclusions and substantive P12 transformations. Its four replacement hashes now point at committed Git blob bytes.

## Portable Integrity

Payload integrity:

| Field | Value |
| --- | --- |
| Algorithm | `agent-platform-git-tree-sha256-v1` |
| Scope | included and transformed upstream payload rows only |
| Metadata included | `false` |
| File count | 6681 |
| Byte count | 145406255 |
| SHA-256 | `03295db99b2204ac962619251289e145432fe32946ee7efad6201dd0742e4ce6` |

Candidate integrity:

| Field | Value |
| --- | --- |
| Status | `committed_final` |
| Algorithm | `agent-platform-git-tree-sha256-v1-excluding-baseline-record` |
| Scope | all tracked files below `2_products/pepper-agent` except `AGENT_PLATFORM_UPSTREAM_BASELINE.json` |
| Excluded self-referential path | `AGENT_PLATFORM_UPSTREAM_BASELINE.json` |
| File count | 6684 |
| Byte count | 148145642 |
| SHA-256 | `27b457b65d8a89bb5c39041bc43b82e6f46c4924c1554f5a1c0fcc7682c19bf7` |

Superseded pre-commit candidate integrity:

| Field | Value |
| --- | --- |
| Authority | `provisional` |
| File count | 6684 |
| Byte count | 148145643 |
| SHA-256 | `0eec7b33f97ba13f66b59d1b2cf3e1a66a26c7d90bfbd0ee5d88a8587cefc727` |
| Supersession reason | final committed Git blob for `AGENT_PLATFORM_MODIFICATIONS.tsv` normalized the header-only file from CRLF to LF, reducing candidate bytes by one |

Baseline record hash handling:

| Field | Value |
| --- | --- |
| Baseline record path | `2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json` |
| Baseline record SHA-256 after P15.M1B update | `7318f257f086a6f09be077eed3ec4f493ce72d0d9dc16fe313f6e33096613848` |
| Baseline record SHA-256 after P15.M1C update | `92b15fb828d105dbd144599c0a49fcef454646667b53b6de227c9716e1aa234c` |
| Stored inside itself | `false` |
| Storage location | `0_architecture/governance/agent_platform_hermes_0_19_product_baseline_commit_finalization.md` |

Superseded checkout digests:

| Worktree | Digest | Bytes | Authority |
| --- | --- | ---: | --- |
| P15M legacy checkout | `3c6f155eba3f01ad4ee924ba62c462de1cdb10fdc1f3099daa8ed1d82a9b912d` | 149895563 | non-authoritative |
| P15M2 clean checkout | `511fffdc2f575506cdcba49b63de3324519b201a6146d680e8a6513f5b5551a6` | 149895745 | non-authoritative |

## Preservation

| Boundary | Result |
| --- | ---: |
| imported implementation payload files modified | 0 |
| current canonical product changes | 0 |
| modification register rows added | 0 |
| dependency manifest changes | 0 |
| lockfile changes | 0 |
| external source changes | 0 |
| new exclusions | 0 |
| silent policy changes | 0 |

PowerPoint exclusion and generated-cache exclusions remain unchanged.

## Runtime Boundary

| Action | Count |
| --- | ---: |
| Graphify commands | 0 |
| dependency installations | 0 |
| package registry queries | 0 |
| builds | 0 |
| source tests | 0 |
| runtime starts | 0 |
| Docker starts | 0 |
| WSL mutations | 0 |
| OAuth flows | 0 |
| credential reads | 0 |
| provider calls | 0 |
| inference calls | 0 |
| commits by agent | 0 |
| pushes by agent | 0 |

## Downstream Consequence

P15.M2, P15.M3 and P15.M4 must not continue from the paused branches until P15.M1C is accepted, committed, pushed and propagated. Their prerequisite gates must use the committed-final `candidate_integrity.SHA256` from `AGENT_PLATFORM_UPSTREAM_BASELINE.json`, not the superseded checkout digest or the superseded P15.M1B pre-commit projection.

P15.M2 license reconciliation restarts after branch update. P15.M3 dependency reconciliation and P15.M4 Desktop/Workspace work remain parallel-lane tasks after propagation.

## Final Validation

| Check | Result |
| --- | --- |
| Pepper text policy explicit | `true` |
| Pepper text EOL | `lf` |
| Pepper binary policy | `byte_exact` |
| conflicting deeper attributes | `0` |
| destination hash mismatches | `0` |
| non-EOL content mismatches | `0` |
| blocked unresolved rows | `0` |
| committed-final candidate digest | `27b457b65d8a89bb5c39041bc43b82e6f46c4924c1554f5a1c0fcc7682c19bf7` |
| superseded pre-commit candidate digest | `0eec7b33f97ba13f66b59d1b2cf3e1a66a26c7d90bfbd0ee5d88a8587cefc727` |
| TSV exact column counts | `true` |
| TSV trailing whitespace | `0` |
| JSON valid | `true` |
| Markdown trailing whitespace | `0` |
| unexpected candidate paths | `0` |

Final verdict: `hermes_0_19_product_baseline_portable_integrity_ready`
