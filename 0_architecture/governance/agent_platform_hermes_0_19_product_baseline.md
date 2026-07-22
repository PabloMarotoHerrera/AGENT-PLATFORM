# P15.M1 - Hermes 0.19 Product Baseline

Status: P15.M1 new editable product baseline ready with constraints.

Final verdict: `hermes_0_19_product_baseline_ready_with_constraints`

## Ticket Authority

P15.M1 creates a separate tracked editable Pepper product baseline derived from the exact locked Hermes Agent 0.19.0 upstream source ratified by P15.M0.

P15.M1 does not make the new baseline canonical, does not forward-port Pepper implementation divergence, does not approve dependencies, does not prove build or runtime readiness, does not adopt Desktop or Workspace, and does not authorize OAuth, credentials, providers or inference.

Forbidden actions preserved by P15.M1:

- no current canonical product mutation;
- no P13, P14 or P15 implementation forward-port;
- no historical P15.4 candidate file copying;
- no dependency installation or lock regeneration;
- no source build, test, lint, typecheck or runtime startup;
- no Hermes Agent, Desktop, Dashboard or Workspace startup;
- no Docker start;
- no WSL mutation;
- no OAuth, credential read, provider call or inference;
- no Graphify execution or modification;
- no Git staging, commit or push.

## Worktree And Prerequisite

| Field | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| Dynamic start SHA | `34467064ddf6b06a6212ef5a57f8b5d50a102188` |
| Branch remote | `origin/p15.m-hermes-0.19-migration` |
| Branch remote SHA | `34467064ddf6b06a6212ef5a57f8b5d50a102188` |
| Required P15.M0 commit | `34467064ddf6b06a6212ef5a57f8b5d50a102188` |
| P15.M0 is ancestor of HEAD | `true` |
| HEAD equals branch remote at start | `true` |
| Index empty at start | `true` |
| Staged files at start | `0` |

Required committed prerequisite:

| Path | Required verdict | Status |
| --- | --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_migration_authorization.md` | `hermes_0_19_migration_authorized_with_constraints` | tracked, committed in HEAD, locally unmodified, unstaged |

P15.M0 accepted decisions used by P15.M1:

```yaml
selected_option: Option 1 -- Upgrade Current Product Only
Hermes_Agent_baseline: 0.19.0
baseline_strategy: new editable baseline plus controlled forward-port
current_product: 2_products/hermes-agent
current_product_canonical: true
P15_M1: unlocked
later_tickets: dependency_gated
```

## Ignore Policy Amendment

P15.M1 initially stopped with `P15.M1-DESTINATION-CONFLICT-BLOCKED` because `2_products/pepper-agent` was covered by the deny-by-default product rule:

```text
.gitignore:9:/2_products/*
```

The accepted ignore-policy amendment authorized exactly two root `.gitignore` exceptions. The broad deny-by-default rule remains in place, and only `pepper-agent` gained product tracking eligibility.

Exact `.gitignore` product block after amendment:

```text
/2_products/*
!/2_products/hermes-agent
!/2_products/hermes-agent/**
!/2_products/pepper-agent
!/2_products/pepper-agent/**
```

Ignore validation:

| Probe | Required result | Observed rule/effect |
| --- | --- | --- |
| `2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` | not ignored | effective `ignored=false` |
| `2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json` | not ignored | effective `ignored=false` |
| `2_products/another-unapproved-product/probe` | ignored | `.gitignore:9:/2_products/*` |
| `4_external/sources/hermes-agent-v0.19.0/probe` | ignored | `.gitignore:16:4_external/sources/` |

No `git add -f` was used. No wildcard product exception was added. No `4_external/sources` ignore rule was changed.

## Current Canonical Product Integrity

Current canonical product:

```yaml
path: 2_products/hermes-agent
canonical: true
modified_by_P15_M1: false
tracked_files: 6246
```

Current-product deterministic tree digest, using `agent-platform-tree-sha256-v1`:

| Moment | Digest | Files | Dirs | Bytes | Zero-byte files | Reparse points |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Pre-ticket | `74f98240d937d300c6532b0284ce756d12da218f430501054744e3a5ef5e1d91` | 6246 | 872 | 136653052 | 35 | 0 |
| Post-baseline | `74f98240d937d300c6532b0284ce756d12da218f430501054744e3a5ef5e1d91` | 6246 | 872 | 136653052 | 35 | 0 |

Current product result: `current_product_tree_unchanged: true`.

Current modification register:

```yaml
path: 2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
rows: 128
columns: 18
duplicate_ids: 0
duplicate_paths: 0
missing_fields: 0
hash_mismatches: 0
status_entries: 0
```

## Destination

Authorized new product destination:

```yaml
path: 2_products/pepper-agent
canonical: false
migration_candidate: true
initial_exists: false
initial_tracked_entries: 0
initial_ignored_after_amendment: false
initial_status_entries: 0
```

No alternate destination was used.

## Source Reacquisition

Hermes Agent 0.19.0 was independently reacquired from upstream into a temporary acquisition root outside the repository. No source was copied from another worktree, the dirty original checkout, the P15.U worktree or the current Pepper product.

Allowed temporary Git operations used: `init`, `fetch`, `rev-parse`, `cat-file`, and `archive`.

Source acquisition evidence:

| Field | Value |
| --- | --- |
| Repository | `https://github.com/NousResearch/hermes-agent` |
| Version | `0.19.0` |
| Tag | `v2026.7.20` |
| Tag object type | `tag` |
| Tag object SHA | `c7d08de287556b3d339df336b180a39d4980ebd7` |
| Peeled commit | `3ef6bbd201263d354fd83ec55b3c306ded2eb72a` |
| Commit object type | `commit` |
| Archive format | `tar` |
| Archive byte count | `154808320` |
| Archive SHA-256 | `5b1db2e6642f6aee669951a8440aab03ec76b1d2832cbf3062ab49754aec3ba0` |
| Deterministic tree SHA-256 | `ca41c8c6c688f7a8e94c238cecb45cb60cbec6c37555ba5eeb92530674e39e07` |
| Regular file count | `6737` |
| Directory count | `905` |
| Total regular-file bytes | `149140090` |
| Zero-byte file count | `37` |
| Reparse-point count | `0` |
| Nested `.git` directories | `0` |
| Nested `.git` files | `0` |
| `.gitmodules` | `absent` |
| `.gitattributes` | `present` |
| Git LFS filters declared | `false` |
| Git LFS pointer count | `0` |
| Temporary acquisition residue | `0` |

Version declaration evidence:

| Path | Evidence |
| --- | --- |
| `pyproject.toml` | `version = "0.19.0"` |
| `hermes_cli/__init__.py` | `__version__ = "0.19.0"`; `__release_date__ = "2026.7.20"` |
| `acp_registry/agent.json` | `"version": "0.19.0"`; `"package": "hermes-agent[acp]==0.19.0"` |

Ignored immutable source destination:

```yaml
path: 4_external/sources/hermes-agent-v0.19.0
ignored: true
tracked_files: 0
visible_status_entries: 0
modified: false
```

## Canonical Filtered-Import Authority

P15.M1 uses the surviving canonical model:

```yaml
update_strategy: filtered_snapshot_three_way_reapplication
B: exact locked Hermes Agent 0.19.0 source
FB: filtered/compliance reconstruction of B
D0: new unmodified Pepper baseline candidate derived from FB
P: not applied in P15.M1
```

Policy sources resolved:

| Source | Role |
| --- | --- |
| `0_architecture/governance/agent_platform_hermes_upstream_synchronization_strategy.md` | P12.5 source model, exclusion revalidation, compliance transformations, tracking compatibility and register schema authority |
| `2_products/hermes-agent/SOURCE_IMPORT_MANIFEST.tsv` | historical import classification and P12.2 transformation evidence |
| `2_products/hermes-agent/SOURCE_EXCLUSIONS.tsv` | historical exclusion classes and reasons |
| `2_products/hermes-agent/UPSTREAM_PROVENANCE.md` | source provenance and import method evidence |
| `0_architecture/governance/agent_platform_hermes_0_19_migration_authorization.md` | P15.M0 baseline-creation authority and migration sequencing |
| `0_architecture/governance/agent_platform_hermes_0_19_workspace_source_lock.md` | locked 0.19.0 source identity and source inventory evidence |

Applied canonical policy:

- excluded `skills/productivity/powerpoint/**` because the restrictive PowerPoint skill license remains uncleared;
- excluded `skills/index-cache/**` because tracked generated/cache material remains excluded from product source;
- excluded the two generated complete PowerPoint skill pages because they reproduce the restricted skill definition;
- removed exactly one `productivity-powerpoint` row from each skills catalog when the predicate matched once;
- removed exactly one `productivity-powerpoint` item from `website/sidebars.ts` when the predicate matched once;
- rederived a product-local `.gitignore` compatibility block for exactly 44 upstream-committed payload files hidden by root or product ignore rules.

No other exclusions or transformations were applied.

## Import Classification

Every upstream regular file is classified exactly once in `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv`.

| Classification | Count |
| --- | ---: |
| `included_byte_exact` | 6677 |
| `transformed_by_canonical_compliance_rule` | 4 |
| `excluded_by_canonical_policy` | 56 |
| `blocked_unresolved` | 0 |
| Total upstream regular files | 6737 |

Manifest validation:

| Check | Result |
| --- | ---: |
| duplicate source paths | 0 |
| duplicate included destination paths | 0 |
| missing classifications | 0 |
| included hash mismatches | 0 |

Exclusion/transformation manifest:

| File | Rows |
| --- | ---: |
| `2_products/pepper-agent/AGENT_PLATFORM_EXCLUSIONS.tsv` | 60 |

The 60 rows are 56 exclusions plus 4 compliance transformations. No transformed file lacks a canonical rule.

## Byte Preservation

All `included_byte_exact` files match source bytes exactly. Evidence for every upstream file is recorded in `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` with source path, destination path, source byte length, source SHA-256, destination SHA-256, classification, canonical rule and reason.

```yaml
included_byte_exact_files: 6677
included_hash_mismatches: 0
transformed_files: 4
blocked_unresolved: 0
```

## Baseline Construction

Construction sequence:

1. Built filtered payload in a temporary candidate directory under `C:/Users/pablo/AppData/Local/Temp/opencode`.
2. Applied only canonical exclusions and transformations.
3. Verified destination still absent.
4. Moved the candidate to `2_products/pepper-agent`.
5. Revalidated trackability and derived the exact product-local `.gitignore` compatibility block.
6. Generated metadata overlay files and recalculated digests.
7. Removed temporary candidate residue.

```yaml
temporary_candidate_roots: 0
nested_git_entries: 0
node_modules_created_by_P15_M1: 0
virtual_environments_created_by_P15_M1: 0
Python_caches_created_by_P15_M1: 0
build_outputs_created_by_P15_M1: 0
running_source_processes: 0
Docker_containers: 0
```

## Product Governance Metadata

Created Pepper-owned metadata overlay files:

| Path | Classification |
| --- | --- |
| `2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json` | `baseline_governance_overlay` |
| `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | `baseline_governance_overlay` |
| `2_products/pepper-agent/AGENT_PLATFORM_EXCLUSIONS.tsv` | `baseline_governance_overlay` |
| `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` | `baseline_governance_overlay` |

The four `AGENT_PLATFORM_*` files are not upstream files and are not counted as upstream-imported payload.

Post-reconciliation TSV validation:

| File | Rows | Columns | Bad column rows | Trailing tab rows | Blank field rows |
| --- | ---: | ---: | ---: | ---: | ---: |
| `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | 6737 | 8 | 0 | 0 | 0 |
| `2_products/pepper-agent/AGENT_PLATFORM_EXCLUSIONS.tsv` | 60 | 7 | 0 | 0 | 0 |
| `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` | 0 | 18 | 0 | 0 | 0 |

Excluded-row non-applicable destination/replacement fields use `not_applicable`; no trailing tabs remain.

New modification register:

```yaml
schema_source: 2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv header
columns: 18
data_rows: 0
duplicate_ids: 0
duplicate_paths: 0
missing_fields: 0
hash_mismatches: 0
implementation_rows: 0
```

## Deterministic Integrity

Original source, filtered-payload and current-product rows use `agent-platform-tree-sha256-v1`.

| Tree | Digest | Files | Dirs | Bytes | Zero-byte files | Reparse points |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| locked source tree | `ca41c8c6c688f7a8e94c238cecb45cb60cbec6c37555ba5eeb92530674e39e07` | 6737 | 905 | 149140090 | 37 | 0 |
| upstream filtered payload | `6378effd082a4bc8210007f0a952adc0b287c444cb3bd39b677403c4bb551fd2` | 6681 | 894 | 147798105 | 35 | 0 |
| complete candidate product before whitespace reconciliation | `d0dd419275bed370033dd4f8bafe5d3a48e7e457abe2597fe044c21556b5b00d` | 6685 | 894 | 149892539 | 35 | 0 |
| current product pre/post | `74f98240d937d300c6532b0284ce756d12da218f430501054744e3a5ef5e1d91` | 6246 | 872 | 136653052 | 35 | 0 |

Post-reconciliation complete candidate product inventory digest:

| Tree | Digest | Algorithm | Files | Dirs | Bytes | Zero-byte files | Reparse points |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| complete candidate product after whitespace reconciliation | `3c6f155eba3f01ad4ee924ba62c462de1cdb10fdc1f3099daa8ed1d82a9b912d` | `sorted_path_sha256_bytes_lf` | 6685 | 894 | 149895563 | 35 | 0 |

`sorted_path_sha256_bytes_lf` hashes UTF-8 records sorted by product-root-relative path, formatted as `path<TAB>file_sha256<TAB>byte_length<LF>`. It is recorded here because the original `agent-platform-tree-sha256-v1` helper implementation is not present in the repository, while the metadata-only reconciliation changed the complete candidate byte count.

Upstream filtered payload digest remains `6378effd082a4bc8210007f0a952adc0b287c444cb3bd39b677403c4bb551fd2` because no upstream byte-exact or transformed payload file changed during whitespace reconciliation.

## License And Notice Preservation

| Path | Source present | Product candidate present | Preservation |
| --- | --- | --- | --- |
| `LICENSE` | true | true | byte-identical |
| `plugins/hermes-achievements/LICENSE` | true | true | byte-identical |
| `plugins/security-guidance/LICENSE` | true | true | byte-identical |
| `plugins/security-guidance/NOTICE` | true | true | byte-identical |
| `skills/creative/humanizer/LICENSE` | true | true | byte-identical |
| `skills/productivity/powerpoint/LICENSE.txt` | true | false | explicitly recorded in exclusion manifest under `P12_restricted_powerpoint_subtree` |

P15.M1 performs source preservation and evidence recording only. P15.M2 remains required before promotion, redistribution or release.

## Dependency And Lock Boundary

Dependency manifests and committed lockfiles included by policy were preserved byte-for-byte when classified as `included_byte_exact`.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docker-compose.yml` | 3530 | `df314eea77ea70e2580c96c532ebf33c9da1d8b191150852fcbebd6a0452530e` |
| `Dockerfile` | 20681 | `25b3ec8a3726324f0cdfe9a95ad68eacb30d9d0e0b47fe7f884ee57ec0a2df15` |
| `package-lock.json` | 733260 | `45ac4d939b5d5226f295f9a4b318afc77876aa15038899448e304e1c0b85ac92` |
| `package.json` | 1550 | `9c02d27204afe4054697ceab1de1bcfd55f5460a29612a35c78b24112d83f76f` |
| `pyproject.toml` | 21734 | `5ba57adbbb7b90587bc959384cb6f08d4ff05e8a477f224e93ff7f2362983b8e` |
| `uv.lock` | 665936 | `97aee767bf5b7b9574995fddcbea5f6a4a536260ee0cc749458e7f514a3a137d` |
| `apps/bootstrap-installer/package.json` | 1910 | `0c8f725df481fa0ca31a9958c695906766c442bd9ff2853635cd8e489d58e64a` |
| `apps/desktop/package.json` | 9677 | `801b62b7322e8c7c4769abf0e2cf75d383bf507bfc7542ef46cc0b657b624f73` |
| `apps/shared/package.json` | 702 | `710ecbd328b32ab84464fb7a8a33363ca78439ee2e32e980caa5702cc26fff9c` |
| `optional-skills/finance/dcf-model/requirements.txt` | 122 | `c46e897bd9b37b6da13a8a96f9f5c4a1247e2489821ddb52884fc03a8a0973c7` |
| `plugins/platforms/photon/sidecar/package-lock.json` | 71055 | `79e7de916eb9c287a850dfc98e8bf7eeae672e2501a68a3ba303df3da738618f` |
| `plugins/platforms/photon/sidecar/package.json` | 711 | `4d07c1824d1b5715dc08af214a5346bc98631c36e611210811b4672a695fc91f` |
| `scripts/whatsapp-bridge/package-lock.json` | 79172 | `4eefee7aa6a6105d064d755b37720ccd203b5c7840babb2c31742ee01352ff78` |
| `scripts/whatsapp-bridge/package.json` | 436 | `3eb579923317f616eb3e07299dbdb19eb144e87340da8d07a520dbdd5280cd97` |
| `tests/e2e/matrix_xsign_bootstrap/docker-compose.yml` | 880 | `77dfcf6097e9e1e3b588f292c01d4cbdbdaa4004d00945edbfaaf5be0c5678e7` |
| `tests-js/package.json` | 485 | `a5865d5bc12de1efb12983c49a4c5d5960c3867eef8db7ef04d068210caebb4e` |
| `ui-tui/package.json` | 1571 | `1475f388cf57194055c940bd9e8003baa6073d729ae53bdae469e3906d721cb0a` |
| `ui-tui/packages/hermes-ink/package.json` | 1577 | `749b0ab9bd65dfd72eed3667bb8b53f672db86801da43f4582b688eecb97cb0a` |
| `web/package.json` | 1718 | `4a6699510879addead42860cfdeb153d1f1af01343d25231fb0bdb4bebc81136` |
| `website/package-lock.json` | 772305 | `fc855080475fda41273c63b5050265d9f7e4838c722b970d028c0010a9ab9ffd` |
| `website/package.json` | 1607 | `8bdc6037cc3f420a42317fddfe9876abe5bc74e4f37a3f99bde76add963d9872` |

P15.M3 owns dependency and lock reconciliation. P15.M1 did not run package managers, installers, lock regeneration, builds or tests.

## Desktop And Dashboard Boundary

Hermes Agent 0.19.0 includes upstream Desktop and Web Dashboard source. P15.M1 preserves included files as part of the upstream baseline where not excluded by canonical policy.

```yaml
Hermes_Desktop_adopted_by_P15_M1: false
Hermes_Web_Dashboard_adopted_by_P15_M1: false
native_Hermes_updater:
  present_in_source_when_applicable: true
  authorized_for_Pepper: false
Pepper_update_strategy: filtered_snapshot_three_way_reapplication
future_one_click_update: prepared_governed_transaction
```

The imported native Hermes update logic is non-authoritative for Pepper.

## No Forward-Port Boundary

P15.M1 did not forward-port:

- P13 product UI;
- P14 runtime adapter;
- P15 provider and credential contracts;
- current modification-register rows;
- current product descriptors;
- current Pepper-specific routes;
- historical uncommitted P15.4 candidate files.

Expected Pepper implementation divergence in the new baseline: `0` rows.

## Candidate State

```yaml
new_product:
  path: 2_products/pepper-agent
  canonical: false
  migration_candidate: true
  upstream_version: 0.19.0
  upstream_commit: 3ef6bbd201263d354fd83ec55b3c306ded2eb72a
  complete_file_count: 6685
  complete_byte_count: 149895563
  complete_product_digest: 3c6f155eba3f01ad4ee924ba62c462de1cdb10fdc1f3099daa8ed1d82a9b912d
  complete_product_digest_algorithm: sorted_path_sha256_bytes_lf
  pre_reconciliation_complete_product_digest: d0dd419275bed370033dd4f8bafe5d3a48e7e457abe2597fe044c21556b5b00d
  nested_git_entries: 0
  ignored_candidate_files: 0
```

Tracked candidate roots after P15.M1:

1. `.gitignore`
2. `2_products/pepper-agent/**`
3. `0_architecture/governance/agent_platform_hermes_0_19_product_baseline.md`

Tracked candidate root count: `3`.

Unexpected candidate roots: `0`.

Local ignored source roots: `1` newly reacquired root for P15.M1, plus no tracked external-source candidates.

## Whitespace Reconciliation

The earlier broad `git diff --check clean` interpretation was incomplete because the full candidate product is untracked before staging, and unstaged diff checks do not inspect untracked candidate payload files. P15.M1 therefore uses an explicit product-tree whitespace scanner joined to `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` for full candidate evidence.

Full candidate whitespace inventory after reconciliation:

| Classification | Files with findings | Trailing-whitespace lines | Disposition |
| --- | ---: | ---: | --- |
| `included_byte_exact` | 153 | 2854 | preserved as upstream source evidence |
| `transformed_by_canonical_compliance_rule` | 0 | 0 | clean |
| `baseline_governance_overlay` | 0 | 0 | clean after TSV normalization |
| unknown/unclassified | 0 | 0 | none |

Validation model:

```yaml
full_candidate_git_diff_check: expected_nonzero_due_to_preserved_upstream_whitespace
pepper_owned_and_transformed_candidate_whitespace_check: required_clean
byte_exact_upstream_whitespace: preserved
automatic_upstream_whitespace_cleanup: prohibited
included_byte_exact_files_modified_by_correction: 0
included_hash_mismatches: 0
```

Transformed-file whitespace review:

| Source path | Destination path | Rule | Source SHA-256 | Destination SHA-256 | Whitespace status |
| --- | --- | --- | --- | --- | --- |
| `.gitignore` | `.gitignore` | `P12_tracking_compatibility_rederived_for_candidate` | `7975849d496ed2f6b6a21466cc45858578d484d779cbbddab76a738aed255c34` | `bc2d006f3ff5267ee633f5ce4b5c045b326804af55f54d6beb361a2c1bf18c32` | clean |
| `website/docs/reference/skills-catalog.md` | `website/docs/reference/skills-catalog.md` | `P12_restricted_powerpoint_catalog_reference_removal` | `ac3d90913cf4ec258d48bc646ae85410d6eea991cb38cdab0d5592b939771a3e` | `36d0c05bd2f94b5717d4d152c64183ffd7a3d4049f043a20167f6c63ff7b243b` | clean |
| `website/i18n/zh-Hans/docusaurus-plugin-content-docs/current/reference/skills-catalog.md` | `website/i18n/zh-Hans/docusaurus-plugin-content-docs/current/reference/skills-catalog.md` | `P12_restricted_powerpoint_catalog_reference_removal` | `8d6e26a39021936c95dda717d04275cd3b2312687d12d92abb0f767250f4c2c4` | `fa4d58e87c24df69965162d7e70953bc577b044ba2a7b2ece195e153334f749e` | clean |
| `website/sidebars.ts` | `website/sidebars.ts` | `P12_restricted_powerpoint_sidebar_reference_removal` | `d79cd704442e892e82d51bb6bcfb47bd6075f6cbb0dccf89175e616a053d9b48` | `b16ac5bc3dcb4a34317eb2c669f1992ac09f70bdc38444c371fc91f10d324e46` | clean |

Explicit byte-exact examples stayed unchanged: `.env.example`, `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/PULL_REQUEST_TEMPLATE.md` and `.plans/streaming-support.md` all remain byte-identical to the locked source.

## Rollback Target

Before human commit, rollback is deletion of only these P15.M1 candidates:

- remove the two `pepper-agent` exceptions from root `.gitignore`;
- remove `2_products/pepper-agent/**`;
- remove `0_architecture/governance/agent_platform_hermes_0_19_product_baseline.md`;
- remove ignored local source root `4_external/sources/hermes-agent-v0.19.0` if the P15.M1 reacquisition is rejected.

Current canonical product rollback is not required because `2_products/hermes-agent` was unchanged.

## Final Validation

| Check | Result |
| --- | --- |
| `.gitignore` modified | `true` |
| `.gitignore` unrelated changes | `0` |
| `2_products/hermes-agent` remains not ignored | `true` |
| `2_products/pepper-agent` ignored | `false` |
| unapproved `2_products` children remain ignored | `true` |
| `4_external/sources` remains ignored | `true` |
| force-add used | `false` |
| current product modified files | `0` |
| current product tracked files | `6246` |
| current product register rows | `128` |
| current product register columns | `18` |
| current product register hash mismatches | `0` |
| current product tree unchanged | `true` |
| new product nested Git entries | `0` |
| new product ignored candidate files | `0` |
| new product complete files | `6685` |
| new product complete bytes after reconciliation | `149895563` |
| new product post-reconciliation digest | `3c6f155eba3f01ad4ee924ba62c462de1cdb10fdc1f3099daa8ed1d82a9b912d` |
| post-reconciliation digest algorithm | `sorted_path_sha256_bytes_lf` |
| manifest included hash mismatches | `0` |
| import manifest blank field rows | `0` |
| import manifest trailing tab rows | `0` |
| exclusions manifest blank field rows | `0` |
| exclusions manifest trailing tab rows | `0` |
| full candidate whitespace findings | `2854`, all `included_byte_exact` |
| preserved upstream whitespace files | `153` |
| Pepper-owned whitespace findings | `0` |
| transformed payload whitespace findings | `0` |
| unclassified whitespace findings | `0` |
| full candidate Git diff whitespace check | `expected_nonzero_due_to_preserved_upstream_whitespace` |
| Pepper-owned and transformed whitespace check | `required_clean_passed` |
| byte-exact upstream whitespace | `preserved` |
| automatic upstream whitespace cleanup | `prohibited` |
| temporary clones | `0` |
| temporary archives | `0` |
| temporary extraction roots | `0` |
| temporary candidate roots | `0` |
| node_modules created by P15.M1 | `0` |
| virtual environments created by P15.M1 | `0` |
| Python caches created by P15.M1 | `0` |
| build outputs created by P15.M1 | `0` |
| Graphify commands | `0` |
| Graphify modifications | `0` |
| dependency installations | `0` |
| builds/tests/runtime executions | `0` |
| OAuth/credential/provider/inference | `0` |
| Docker/WSL/VPS actions | `0` |
| Git index | empty |
| staged files | none |
| commits by agent | `0` |
| pushes by agent | `0` |

## Final Boundaries

P15.M1 is ready for human review and commit. The current product remains canonical. The new Pepper baseline remains non-canonical. P15.M2, P15.M3 and P15.M4 become eligible only after P15.M1 is committed. Later migration tickets remain dependency-gated. Live OAuth, provider calls and inference remain unauthorized.

Final verdict: `hermes_0_19_product_baseline_ready_with_constraints`
