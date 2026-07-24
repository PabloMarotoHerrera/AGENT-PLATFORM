# P15.M6R - Pepper Product Identity Post-Commit Integrity Closure

Status: P15.M6R post-commit Pepper product identity integrity closed with constraints.

Final verdict: `hermes_0_19_pepper_product_identity_post_commit_integrity_closed_with_constraints`

## Authority

P15.M6R closes the post-commit integrity record for the P15.M6 Pepper product
identity foundation after the authorized P15.M6A metadata repair was committed
and pushed. The original P15.M6 commit remains the only product-mutation commit.

P15.M6R modifies no product implementation files, modification register rows,
import manifest rows, exclusion manifest rows, third-party notice text, branding
manifest rows or prior governance records.

Authorized P15.M6R candidates:

| Path | Disposition |
| --- | --- |
| `2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json` | updates self-excluded current baseline integrity metadata |
| `0_architecture/governance/agent_platform_hermes_0_19_pepper_product_identity_post_commit_integrity_closure.md` | records the P15.M6R closure evidence |

## Start Gate

| Check | Result |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| Start HEAD | `d472b8fe32510bd917828625f98c132dca1731d5` |
| origin/p15.m-hermes-0.19-migration | `d472b8fe32510bd917828625f98c132dca1731d5` |
| HEAD equals branch remote at start | `true` |
| Index empty at start | `true` |
| Tracked worktree clean at start | `true` |
| P15.M6 verdict present | `hermes_0_19_pepper_product_identity_application_ready_with_constraints` |
| P15.M6A verdict present | `hermes_0_19_pepper_product_identity_register_hashes_reconciled` |

## Commit History Rule

| Field | Value |
| --- | --- |
| P15.M6 product-mutation commit | `ab2ec5dd6415c02bbac5f55edc8c6cd747763391` |
| P15.M6 commit message | `P15.M6 Apply Pepper product identity and branding foundation` |
| Post-P15.M6 commits | `1` |
| Authorized post-P15.M6 repair commit | `d472b8fe32510bd917828625f98c132dca1731d5` |
| Authorized repair commit message | `P15.M6A Reconcile committed Pepper register hashes` |
| Post-P15.M6 commit status | `exactly_one_authorized_register_metadata_repair` |
| Post-P15.M6 product implementation mutation commits | `0` |
| Unexpected post-P15.M6 paths | `0` |

Authorized post-P15.M6 paths:

| Path | Commit disposition |
| --- | --- |
| `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` | P15.M6A metadata-only register hash reconciliation |
| `0_architecture/governance/agent_platform_hermes_0_19_pepper_product_identity_register_hash_reconciliation.md` | P15.M6A durable repair record |

P15.M6R validates the modification register from current `HEAD`; it does not
require the register blob to match the original P15.M6 commit.

## Product Identity

| Field | Value |
| --- | --- |
| Product ID | `pepper` |
| Product display name | `Pepper` |
| Product version | `0.1.0-dev` |
| Upstream product name | `Hermes Agent` |
| Upstream version | `0.19.0` |
| Upstream tag | `v2026.7.20` |
| Upstream commit | `3ef6bbd201263d354fd83ec55b3c306ded2eb72a` |
| Product UI feature flag | `agent_platform.product_ui = disabled` |
| Extension modules | `[]` |

`upstream_tag` remains governance and notice evidence only. It is not a backend,
frontend or API runtime field.

## Current Register Validation

The current `HEAD` register is the P15.M6A-repaired register.

| Check | Result |
| --- | --- |
| Register path | `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` |
| Register bytes | `20217` |
| Register SHA-256 | `21a9bcc29f35c13212852ce04f7122ef96875659754e69a56fc745471e39d8a4` |
| P15.M6 rows | `22` |
| Columns | `18` |
| Duplicate IDs | `0` |
| Duplicate paths | `0` |
| Blank mandatory fields | `0` |
| Invalid classifications | `0` |
| Missing committed blobs | `0` |
| Committed-blob hash mismatches | `0` |
| Notice register hash match | `true` |

P15.M6A reconciled exactly these register rows to exact current `HEAD` Git blob
SHA-256 values:

| Modification ID | Product path | Exact current HEAD Git blob SHA-256 |
| --- | --- | --- |
| `P15.M6-002` | `hermes_cli/web_server.py` | `d08e29db31bb044f248e1593ddb06db486e6b04f9f05144f6daba421fc04c46e` |
| `P15.M6-020` | `web/src/main.tsx` | `fc83d0f55f392c936231725731ff55deabb6f70b624c5aa6b5ff9cbb8bfd3dc9` |
| `P15.M6-021` | `web/src/App.tsx` | `8ca66b772754824ac4ecada6f11c20ea8af518657bb3d272daef7d86d4987972` |

## Canonical Integrity

Canonical command run twice with matching output:

```cmd
python 10_scripts/governance/pepper_baseline_integrity.py --repo-root . --product-root 2_products/pepper-agent --mode all --format json
```

Current post-P15.M6A candidate identity:

| Field | Value |
| --- | --- |
| Algorithm | `agent-platform-git-tree-sha256-v2` |
| Representation | `canonical_committed_candidate_except_baseline_record` |
| Content basis | exact current `HEAD` Git blob bytes |
| Scope | all tracked files under `2_products/pepper-agent` except `AGENT_PLATFORM_UPSTREAM_BASELINE.json` |
| Excluded path | `AGENT_PLATFORM_UPSTREAM_BASELINE.json` |
| Files | `6703` |
| Bytes | `148235965` |
| SHA-256 | `1897e20d93858c7125ad5ddee6ac5e56fe808b154c6e786ce42a204730a14146` |

Current post-P15.M6A payload identity:

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
| Baseline record bytes before P15.M6R | `25333` |
| Baseline record SHA-256 before P15.M6R | `5aa7d9582e8036e66a9a81be772aa75b3cb930a978c0128bc0a6b2585baa0fea` |
| Projected baseline record bytes after P15.M6R | `28119` |
| Projected baseline record SHA-256 after P15.M6R | `dfbab65b5b5b960cba50c209ad3e18dc21c06b4a028322945b73f9b325633543` |
| Stored inside baseline JSON itself | `false` |
| External record for projected post-P15.M6R hash | this P15.M6R closure record |

Historical evidence preserved in the baseline JSON:

| Evidence | Files | Bytes | SHA-256 | Classification |
| --- | ---: | ---: | --- | --- |
| P15.M1D candidate v2 | `6684` | `148145642` | `fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b` | `reproduced_by_v2` |
| P15.M1D payload v2 | `6681` | `145406255` | `3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073` | `reproduced_by_v2` |
| P15.M6 pre-register-repair candidate v2 | `6703` | `148235965` | `803fa9a9dfa6b3b27c3f184e44a424d77d66d56fa0a805d4352a4010820866de` | `superseded_by_P15_M6A_register_metadata_repair` |
| P15.M6 pre-register-repair payload v2 | `6681` | `145409765` | `56a538886ac9cc98050be853f173e631e8f568495a6c5aeef27a2128981524e7` | `reproduced_after_P15_M6A_register_metadata_repair` |

## Static Product Contract Validation

| Check | Result |
| --- | --- |
| Backend ProductConfiguration runtime fields | exact `11` fields |
| Frontend accepted runtime field set | exact product configuration key set |
| `upstream_tag` backend runtime field | `false` |
| `upstream_tag` frontend runtime field | `false` |
| Credential field exposure in ProductConfiguration | `0` |
| Runtime/worker field exposure in ProductConfiguration | `0` |
| Protected route literal | `GET /api/agent-platform/product-configuration` |
| Route response model | `ProductConfiguration` |
| Route response source | `load_product_configuration()` |
| Route in `PUBLIC_API_PATHS` | `false` |
| Additional backend `/api/agent-platform/**` routes | `0` |
| Empty extension registry | `true` |
| Production product descriptors | `0` |
| Production product route activations | `0` |

## Branding, Notice And Import Validation

| Check | Result |
| --- | --- |
| Branding manifest rows | `16` |
| Branding manifest columns | `17` |
| Branding manifest SHA-256 | `fc691e10c3d53c6dbc20f35ef9090dd0c2e64b14e60a4f9d5302b97380bc23d2` |
| Branding records missing register IDs | `0` |
| Branding duplicate record IDs | `0` |
| Branding duplicate path/dimension pairs | `0` |
| Third-party notice bytes | `4756` |
| Third-party notice SHA-256 | `95366ecc9d0388e6d1be17d7eda0b65a9bfdfde58b8c7a352987131b3500f68f` |
| Third-party notice required missing sections | `0` |
| Included import rows | `6681` |
| Destination hash matches | `6678` |
| Authorized P15.M6 destination mismatches | `3` |
| Unexplained destination hash mismatches | `0` |
| Missing import destinations | `0` |
| Unsupported import classifications | `0` |
| Modification rows with invalid baseline references | `0` |
| New P15.M6 product-owned files not in import manifest | `19` authorized additions |

The three authorized import destination mismatches are the P15.M6 modified
payload files `hermes_cli/web_server.py`, `web/src/main.tsx` and
`web/src/App.tsx`. P15.M6A changed only register metadata and did not change
payload identity.

## Executable Validation

| Command | Result |
| --- | --- |
| `python -c "import py_compile; ..."` | passed for `product_config.py` and `web_server.py` |
| `set PYTHONDONTWRITEBYTECODE=1&& pytest -q tests/hermes_cli/test_agent_platform_product_config.py -p no:cacheprovider` | `10 passed in 0.59s` |
| `python -m unittest discover -s 12_tests/governance -p test_pepper_baseline_integrity.py` | `Ran 14 tests in 0.003s`; `OK` |
| Route integration tests | blocked: `fastapi_available=False` |
| Frontend typecheck | blocked: local `node_modules/.bin/tsc.cmd` unavailable |
| Frontend Vitest targeted suite | blocked: local `node_modules/.bin/vitest.cmd` unavailable |

No dependency installation was performed.

## Final Repository Hygiene

| Check | Result |
| --- | --- |
| `python -m json.tool 2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json` | passed |
| Canonical candidate after P15.M6R baseline edit | unchanged: `6703` files, `148235965` bytes, `1897e20d93858c7125ad5ddee6ac5e56fe808b154c6e786ce42a204730a14146` |
| Canonical payload after P15.M6R baseline edit | unchanged: `6681` files, `145409765` bytes, `56a538886ac9cc98050be853f173e631e8f568495a6c5aeef27a2128981524e7` |
| Projected baseline record after P15.M6R edit | `28119` bytes, `dfbab65b5b5b960cba50c209ad3e18dc21c06b4a028322945b73f9b325633543` |
| `git diff --check` | clean |
| Tracked diff paths | `2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json` only |
| Untracked candidate paths | `0_architecture/governance/agent_platform_hermes_0_19_pepper_product_identity_post_commit_integrity_closure.md` only |
| Index empty | `true` |
| Staged files | `0` |

## Runtime Boundary

| Action | Count |
| --- | ---: |
| Product implementation file changes by P15.M6R | 0 |
| Modification register changes by P15.M6R | 0 |
| Import manifest changes by P15.M6R | 0 |
| Exclusion manifest changes by P15.M6R | 0 |
| Third-party notice changes by P15.M6R | 0 |
| Branding artifact changes by P15.M6R | 0 |
| Prior governance record changes by P15.M6R | 0 |
| Package or lockfile changes | 0 |
| Desktop or Workspace activation | 0 |
| Graphify actions | 0 |
| Dependency installations | 0 |
| Builds | 0 |
| Runtime service starts | 0 |
| OAuth flows | 0 |
| Provider calls | 0 |
| Credential reads | 0 |
| Inference calls | 0 |
| Git staging by agent | 0 |
| Git commits by agent | 0 |
| Git pushes by agent | 0 |

## Final Statement

P15.M6R closes the post-commit integrity record using the current P15.M6A-repaired
register as the authoritative metadata state. The current candidate and payload
identities are portable Git-blob identities, the baseline JSON remains
self-excluded from candidate integrity, and the projected post-P15.M6R baseline
record hash is stored externally in this closure record only.
