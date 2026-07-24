# P15.M5A - Hermes Workspace 2.3.0 Source Integrity Canonicalization

Status: P15.M5A Workspace source-integrity canonicalization ready with constraints.

Final verdict: `hermes_workspace_2_3_0_source_integrity_canonicalized_with_constraints`

## Ticket Authority

P15.M5A resolves the P15.M5P blocker by replacing the unavailable historical Workspace `agent-platform-tree-sha256-v1` authority with committed, reproducible, standard-library integrity tooling and a per-file source manifest for Hermes Workspace 2.3.0.

Authorized P15.M5A candidates:

| Path | Disposition |
| --- | --- |
| `10_scripts/governance/external_source_tree_integrity.py` | created canonical external-source integrity utility |
| `12_tests/governance/test_external_source_tree_integrity.py` | created dedicated utility tests |
| `0_architecture/governance/agent_platform_hermes_workspace_2_3_0_source_manifest.tsv` | created 12-column per-file Workspace source manifest |
| `0_architecture/governance/agent_platform_hermes_workspace_2_3_0_source_integrity_canonicalization.md` | created canonicalization record |
| `0_architecture/governance/agent_platform_hermes_0_19_workspace_source_lock.md` | updated Workspace 2.3.0 source-integrity authority only |
| `0_architecture/governance/agent_platform_hermes_0_19_desktop_workspace_productization_decision.md` | updated Workspace source-integrity authority and P15.M5 sequencing only |

P15.M5A does not approve Workspace adoption, import, startup, deployment, dependency installation, Docker or Compose execution, OAuth, credential access, provider calls, inference, Graphify, Desktop enablement, route authority transfer or Workspace shell replacement.

No product source, product manifest, lockfile, package manifest, Graphify artifact, `.gitignore` file or `.gitattributes` file is modified.

## Worktree Gate

| Field | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| Dynamic HEAD | `5cc9c5eeb8de7dd3919c3fc78eab4575b86c773e` |
| Branch remote | `origin/p15.m-hermes-0.19-migration` |
| Branch remote SHA | `5cc9c5eeb8de7dd3919c3fc78eab4575b86c773e` |
| HEAD equals branch remote | `true` |
| Tracked worktree clean at start | `true` |
| Index empty at start | `true` |
| Existing P15.M5A tracked candidates at start | `0` |
| Required P15.M4R verdict present | `hermes_0_19_parallel_lane_integration_closed_with_constraints` |

Ignored source target gate:

| Check | Result |
| --- | --- |
| Target | `4_external/sources/hermes-workspace-v2.3.0` |
| Target present at start | `false` |
| Effective ignore rule | `.gitignore:16:4_external/sources/` |
| Tracked files under `4_external/sources` at start | `0` |

## Canonical Algorithms

Utility:

```text
10_scripts/governance/external_source_tree_integrity.py
```

Record stream shared by both current algorithms:

```text
path-utf8-nul-byte-count-nul-content-sha256-lf
```

Each regular file contributes exactly:

```text
<repository-relative-or-source-root-relative UTF-8 path bytes> NUL <decimal byte count> NUL <lowercase SHA-256 of file bytes> LF
```

Records are sorted by raw UTF-8 path bytes. Paths must be relative, UTF-8, TSV-safe and free of empty, `.`, `..`, absolute, backslash, NUL, tab, CR and LF segments. Directory counts are metadata and are not part of the aggregate stream.

| Algorithm | Source of bytes | Accepted source boundary |
| --- | --- | --- |
| `agent-platform-git-source-tree-sha256-v2` | regular Git blob bytes from the exact peeled commit, enumerated with `git ls-tree -r -t -z --full-tree` and read with `git cat-file --batch` | symlinks `0`; submodules `0`; special entries `0`; nested `.git` entries `0`; Git LFS pointer files `0` |
| `agent-platform-materialized-source-tree-sha256-v1` | regular filesystem file bytes under the ignored source root after canonical archive extraction | symlinks `0`; reparse points `0`; special entries `0`; nested `.git` entries `0`; Git LFS pointer files `0` |

The historical `agent-platform-tree-sha256-v1` value remains retained as prior evidence only. It is not current authority because no byte-exact implementation is committed in this repository.

## Independent Acquisition

Temporary acquisition root:

```text
C:/Users/pablo/AppData/Local/Temp/opencode/p15m5a-workspace-v230-acq
```

Temporary acquisition root retained after validation: `false`.

Allowed Git operations used in the temporary acquisition root: `git init`, `git remote add`, `git fetch`, `git rev-parse`, `git cat-file`, `git ls-tree`, `git show`, and `git archive`.

Source identity:

| Field | Value |
| --- | --- |
| Repository | `https://github.com/outsourc-e/hermes-workspace.git` |
| Version | `2.3.0` |
| Tag | `v2.3.0` |
| Tag object type | `tag` |
| Tag object SHA | `0218dbafce50fa69ba9ce045e2c8a3f5383bd1db` |
| Peeled object type | `commit` |
| Peeled commit SHA | `15fa9cd706f5c04e4db288fb958e21d10fc776da` |
| Expected commit SHA | `15fa9cd706f5c04e4db288fb958e21d10fc776da` |
| Commit match | `true` |

Repository metadata evidence:

| Check | Result |
| --- | --- |
| `.gitmodules` | absent |
| `.gitattributes` | absent |
| `package.json` name | `hermes-workspace` |
| `package.json` version | `2.3.0` |
| `package.json` private | `true` |

## EOL Canonicalization

The first archive observation used ambient Git archive export behavior and reproduced the historical P15.U0 archive bytes:

| Archive mode | Bytes | SHA-256 | Disposition |
| --- | ---: | --- | --- |
| ambient Git archive export | `101693440` | `10119f375ee7632443353fd7d2f1e45ca613caa971123f0f72c3890c8dc3c438` | historical/superseded evidence only |

That ambient export materialized `1057` regular files, `142` directories and `100799318` regular-file bytes, but did not match raw Git blob bytes. P15.M5A rejects ambient EOL conversion as current authority.

Canonical archive extraction used command-scoped, non-mutating EOL settings:

```text
git -c core.autocrlf=false -c core.eol=lf -C C:\Users\pablo\AppData\Local\Temp\opencode\p15m5a-workspace-v230-acq archive --format=tar --output=C:\Users\pablo\AppData\Local\Temp\opencode\p15m5a-workspace-v230-acq\hermes-workspace-v2.3.0.canonical.tar 15fa9cd706f5c04e4db288fb958e21d10fc776da
```

Canonical archive identity:

| Field | Value |
| --- | --- |
| Format | `tar` |
| Bytes | `101201920` |
| SHA-256 | `12684835e4d0bf3acff0e6e8e044dde7fab3c2fa1ce91c50d9e377a0282c24c6` |
| Retained in repository | `false` |

## Current Workspace Integrity

Exact utility command:

```text
python 10_scripts/governance/external_source_tree_integrity.py --git-repo C:\Users\pablo\AppData\Local\Temp\opencode\p15m5a-workspace-v230-acq --commit 15fa9cd706f5c04e4db288fb958e21d10fc776da --source-root 4_external\sources\hermes-workspace-v2.3.0 --repository https://github.com/outsourc-e/hermes-workspace.git --tag v2.3.0 --manifest-output 0_architecture\governance\agent_platform_hermes_workspace_2_3_0_source_manifest.tsv --mode all --format json
```

Current canonical results:

| Scope | Algorithm | Files | Directories | Bytes | SHA-256 |
| --- | --- | ---: | ---: | ---: | --- |
| Git source tree | `agent-platform-git-source-tree-sha256-v2` | 1057 | 142 | 100314437 | `6a16ebca192555e6afa95fe6bcd701c2d50e57440de4766cdf58e07a2054c394` |
| Materialized source tree | `agent-platform-materialized-source-tree-sha256-v1` | 1057 | 142 | 100314437 | `6a16ebca192555e6afa95fe6bcd701c2d50e57440de4766cdf58e07a2054c394` |

Comparison result:

| Check | Result |
| --- | --- |
| Status | `match` |
| SHA-256 match | `true` |
| Files match | `true` |
| Bytes match | `true` |
| Directories match | `true` |
| Missing materialized files | `0` |
| Extra materialized files | `0` |
| Different files | `0` |
| Symlinks | `0` |
| Reparse points | `0` |
| Submodules | `0` |
| Special entries | `0` |
| Nested `.git` entries | `0` |
| Git LFS pointer files | `0` |

Source manifest:

| Field | Value |
| --- | --- |
| Path | `0_architecture/governance/agent_platform_hermes_workspace_2_3_0_source_manifest.tsv` |
| Data rows | `1057` |
| Columns | `12` |
| Bytes | `370995` |
| SHA-256 | `dfdbbd8e6eb1595661fec1dadb4392b6026863cfefbc66716795d07c572525ec` |
| Non-exact verification statuses | `0` |

## Source-Lock Supersession

P15.M5A supersedes only the Workspace 2.3.0 source-tree integrity authority in `0_architecture/governance/agent_platform_hermes_0_19_workspace_source_lock.md`.

Historical evidence retained but not current authority:

| Historical field | Value | Current disposition |
| --- | --- | --- |
| Algorithm | `agent-platform-tree-sha256-v1` | superseded; implementation absent from committed repository |
| Tree SHA-256 | `f00b66d6e7dc5bef87602cb026bdf14e593314b9fd242e3e1af48c20704616b9` | prior evidence only |
| Regular files | `1057` | agrees with current count |
| Directories | `142` | agrees with current count |
| Regular-file bytes | `100799318` | ambient archive export evidence only; not current raw-source authority |

## Validation

Dedicated utility tests:

```text
python -m unittest discover -s 12_tests/governance -p test_external_source_tree_integrity.py
```

Result:

```yaml
tests_run: 25
failures: 0
errors: 0
result: OK
```

Required Pepper V2 utility remains unchanged and authoritative for Pepper product integrity:

```text
python 10_scripts/governance/pepper_baseline_integrity.py --repo-root . --product-root 2_products/pepper-agent --mode all --format json
```

Required Pepper V2 identities remain:

| Scope | Algorithm | Files | Bytes | SHA-256 |
| --- | --- | ---: | ---: | --- |
| Candidate | `agent-platform-git-tree-sha256-v2` | 6684 | 148145642 | `fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b` |
| Payload | `agent-platform-git-tree-sha256-v2` | 6681 | 145406255 | `3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073` |
| Baseline record | `sha256-git-blob-v1` | not_applicable | 25333 | `5aa7d9582e8036e66a9a81be772aa75b3cb930a978c0128bc0a6b2585baa0fea` |

## P15.M5 Handoff

P15.M5 may restart static Desktop/Workspace/Pepper surface inventory after P15.M5A is reviewed and committed. Workspace remains ignored, untracked, reference-only source at `4_external/sources/hermes-workspace-v2.3.0`; no Workspace product authority is granted by P15.M5A.
