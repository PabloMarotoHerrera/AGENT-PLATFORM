# P12.2 - Hermes License Exclusion and Notice Baseline

## Document Header

| Field | Value |
| --- | --- |
| Project | P12 - Hermes Productization Foundation |
| Ticket | P12.2 - License Exclusion and Notice Baseline |
| Type | Compliance / source import / license and provenance baseline |
| Date | 2026-07-13 |
| Status | `license_exclusion_notice_baseline_ready` |
| Canonical output | `0_architecture/governance/agent_platform_hermes_license_exclusion_notice_baseline.md` |
| Authorized workspace | `C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM` |
| Product root | `2_products/hermes-agent` |
| Upstream root | `4_external/sources/hermes-agent` |
| Git topology | Normal subtree of the main AGENT PLATFORM repository |
| Legal posture | Engineering compliance baseline only; not legal advice or distribution approval |

This record is the current P12.2 authority. It documents the completed corrected snapshot and supersedes all former external-root and stopped-attempt verdicts.

## Purpose

Establish the first legally filtered, provenance-controlled Hermes product-source baseline inside `2_products/hermes-agent`. The baseline imports only permitted regular blobs from the exact locked Git commit, excludes known restrictive and generated/cache material before writing, preserves applicable license and NOTICE files, records deterministic manifests, and leaves all Git staging and history mutation to the human.

## Correction History Summary

An earlier P12.2 execution imported a filtered snapshot into the unauthorized external root `C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES`. P12.C1 proved ownership and removed that complete result. No former product file was recovered, inspected or reused. Detailed incident evidence remains in `0_architecture/governance/agent_platform_hermes_misplaced_product_root_rollback.md`.

The first corrected pre-import attempt stopped correctly under the supplied fail-closed count contract. That contract incorrectly expected eight tracked files under `skills/index-cache/**`; the exact locked commit contains four. No product file was written during that attempt, no rollback was required, and its stopped verdict is superseded by this execution. The exact Git tree, not a historical count, is authoritative.

## P12.C1 Status

```yaml
P12_C1_Status:
  invalid_external_root_exists: false
  historical_P12_1_material_result_removed: true
  historical_P12_2_material_result_removed: true
  deleted_external_snapshot_reused: false
  P11_2_affected: false
  locked_upstream_unchanged: true
```

## P12.C2 Product Placement

```yaml
HermesProductPlacement:
  classification: hybrid_product_with_platform_adapters
  product_root: 2_products/hermes-agent
  product_root_inside_agent_platform: true
  product_is_main_repo_subtree: true
  nested_git_repository: false
  separate_product_remote: false
```

No alternative path or repository topology was used.

## P12.C3 Tracking Policy

The root policy remains:

```gitignore
/2_products/*
!/2_products/hermes-agent
!/2_products/hermes-agent/**
```

```yaml
P12_C3_Status:
  root_gitignore_sha256: E1A7238DB58ABFA93DA762EC87801DF8B74877CC573608ED0F83E55EC352C40A
  hermes_root_check_ignore_exit_before_import: 1
  hermes_descendant_check_ignore_exit_before_import: 1
  sibling_products_remain_ignored: true
  force_add_required_for_product_root: false
```

The root `.gitignore` was not modified.

## Corrected P12.1 Status

```yaml
Corrected_P12_1_Status:
  product_root: 2_products/hermes-agent
  product_root_created: true
  product_root_empty_before_import: true
  product_is_main_repository_subtree: true
  product_root_reparse_point: false
  nested_git_created: false
  product_branch_created: false
  product_remote_created: false
  source_import_performed_by_P12_1: false
  P12_2_reentry_accepted: true
```

The nearest Git root was `C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM`. Before import, no Hermes product path was tracked or staged. The OneDrive-managed `Escritorio` parent remained approved infrastructure; AGENT PLATFORM and every component below it were required to be non-reparse.

## Locked Upstream Identity

```yaml
HermesLockedUpstreamReference:
  absolute_path: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\4_external\sources\hermes-agent
  repository: https://github.com/NousResearch/hermes-agent
  observed_origin: https://github.com/nousresearch/hermes-agent.git
  normalized_origin_matches: true
  release: 0.18.2
  tag: v2026.7.7.2
  commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  head_matches: true
  tag_points_at_head: true
  status_clean_before_and_after: true
  posture: immutable_read_only_reference
```

Only local read-only Git metadata and object commands were used. No global Git configuration, upstream file or upstream Git state was modified.

## Deterministic Source Inventory

The exact commit was enumerated with `git ls-tree -r -z --full-tree`. Every entry was classified by mode, type, object ID and repository-relative UTF-8 path. Validation rejected absolute paths, `..`, NULs, Windows-invalid names, reserved device names, unsafe trailing dots/spaces, path escapes, case-insensitive collisions and Unicode-normalization collisions.

```yaml
HermesSourceImportCorrectedCounts:
  tracked_regular_files_considered: 6171
  excluded_restricted_powerpoint_files: 50
  excluded_generated_complete_skill_pages: 2
  excluded_tracked_skill_index_cache_files: 4
  total_excluded_files: 56
  total_imported_upstream_files: 6115
  p12_2_created_legal_provenance_files: 5
  final_product_file_count: 6120
```

```yaml
HermesSourceTreeSafety:
  non_regular_entries: 0
  symlinks: 0
  gitlinks: 0
  unsafe_paths: 0
  path_escapes: 0
  case_insensitive_collisions: 0
  unicode_normalization_collisions: 0
  executable_mode_imports: 59
  temporary_plan_sha256: 461148188C3434C5FC34E3D9860AD91A6D5B7A7E7B0D0CE78EA638C752CD6DFA
  temporary_hash_inventory_sha256: 34171DD0832D848C12E61DC1E8C74328043FA4FE4C454EFE911972607AD92A34
```

## Exact Exclusion Policy

| Exclusion class | Exact scope | Count |
| --- | --- | ---: |
| `restricted_powerpoint_subtree` | `skills/productivity/powerpoint/**` | 50 |
| `restricted_generated_complete_skill_page` | Exact English and Chinese generated pages | 2 |
| `tracked_generated_skill_index_cache` | `skills/index-cache/**` | 4 |
| Total | Excluded before import | 56 |

The exact cache paths were:

```text
skills/index-cache/anthropics_skills_skills_.json
skills/index-cache/claude_marketplace_anthropics_skills.json
skills/index-cache/lobehub_index.json
skills/index-cache/openai_skills_skills_.json
```

No exclusion was broadened and no path outside the exact locked Git tree was considered.

## Import Method

A temporary standard-library-only Python helper consumed the validated plan and read each locked blob through `git cat-file --batch`. For every permitted blob it:

1. Revalidated the repository-relative path and destination containment.
2. Created only required normal directories below the product root.
3. Wrote exact Git blob bytes to a new normal file.
4. Recorded upstream mode and object ID.
5. Computed source and product SHA-256.
6. Required exact hash equality before planned product modification.

No upstream worktree byte, external snapshot, clone, archive extraction, hardlink, symlink, junction, reparse point, submodule or network source was used. An initial helper invocation encountered pipe backpressure and timed out before its write loop; process absence and an empty product root were proven before the corrected one-object-at-a-time batch protocol ran.

## Imported Source Inventory

```yaml
HermesProductSnapshotInventory:
  imported_upstream_files: 6115
  p12_2_created_legal_provenance_files: 5
  total_product_files: 6120
  excluded_upstream_files: 56
  product_directories: 858
  nested_git_entries: 0
  reparse_points: 0
  hardlinks: 0
  unexplained_files: 0
  unexplained_directories: 0
```

The exact final file set equals the 6,115 import-manifest paths plus the five P12.2-created files.

## Product Source Modifications

Exactly one intended registration was removed from each file:

| Path | Exact modification |
| --- | --- |
| `website/docs/reference/skills-catalog.md` | Removed the English bundled `powerpoint` catalog row. |
| `website/i18n/zh-Hans/docusaurus-plugin-content-docs/current/reference/skills-catalog.md` | Removed the Chinese bundled `powerpoint` catalog row. |
| `website/sidebars.ts` | Removed the `productivity-powerpoint` bundled sidebar entry. |

Each locked source contained exactly one intended match before modification. Generic references to PowerPoint, `.pptx`, presentations, office formats and independent presentation support were not broadly removed.

## Tracking Compatibility

Initial batch validation found 39 upstream-tracked imports hidden by inherited ignore rules:

| Category | Count |
| --- | ---: |
| Infographic assets | 5 |
| Concept-diagram examples | 15 |
| Dashboard `dist` assets | 4 |
| P5.js export files | 2 |
| Web fonts | 7 |
| Secrets documentation pages | 5 |
| Website data file | 1 |
| Total | 39 |

The product-local `.gitignore` received exactly one delimited `AGENT PLATFORM P12.2 tracked-upstream compatibility` block with the required exact directory/file negations. The root `.gitignore` was not modified, no broad unignore was added, and no runtime, dependency or generated package output was activated.

```yaml
HermesTrackingCompatibility:
  initially_ignored_imported_paths: 39
  product_local_gitignore_modified: true
  root_gitignore_modified: false
  final_ignored_expected_paths: 0
  force_add_required: false
  product_gitignore_source_sha256: 48C1B21B96A29422AD211A000EAFC451CCB5771552B7866D3ED8DA8556B9A992
  product_gitignore_final_sha256: CC50D6A4E5789A08F19A4F17D306CE14CFDA4032B5EC248E2C1383106959CC30
```

## License Inventory

| Path | Classification | Source/product SHA-256 | Result |
| --- | --- | --- | --- |
| `LICENSE` | MIT, upstream Hermes project | `821556E6336796450AB852D375117B48A4887E71D255794FD6318D99982A5AB6` | Preserved exactly |
| `plugins/hermes-achievements/LICENSE` | MIT, plugin-specific | `5C6BBD852EEFF017E73830408977D26E4379C5F9BB6EDB03FCE171F81DB5FE43` | Preserved exactly |
| `skills/creative/humanizer/LICENSE` | MIT, subtree-specific | `4AC4810254AB36D45419141AEB8E69BF50652CFAFE5B2DAB947D06D44E5CBF96` | Preserved exactly |
| `plugins/security-guidance/LICENSE` | Apache License 2.0 | `CFC7749B96F63BD31C3C42B5C471BF756814053E847C10F3EB003417BC523D30` | Preserved exactly |
| `plugins/security-guidance/NOTICE` | Apache NOTICE | `ADC3DD09B90DD9240F56D5B9C782986028A312AB150C84A208DE1A5D2B948227` | Preserved exactly |
| `skills/productivity/powerpoint/LICENSE.txt` | Restrictive material | Exclusion manifest only | Excluded before import |

The complete product tree is not characterized as uniformly MIT. Imported lockfiles and manifests do not establish complete dependency-license clearance.

## Notice Inventory

Product `NOTICE` records product identity, exact upstream release/tag/commit, retained MIT and Apache-2.0/NOTICE materials, restrictive exclusions, the no-whole-tree-MIT boundary, and lack of redistribution/publication clearance.

```yaml
ProductNotice:
  path: NOTICE
  sha256: 4AC2353FC0B52C937B43BA6AE54D9D28CE3C4D400B87B7DD4894C2CC2026C145
```

## Third-Party Notice Baseline

`THIRD_PARTY_NOTICES.md` records known imported MIT and Apache-2.0 materials, nested NOTICE preservation, restrictive/generated/cache exclusions, dependency and asset unknowns, trademark review, SBOM requirements and blocked redistributability.

```yaml
ThirdPartyNoticeBaseline:
  path: THIRD_PARTY_NOTICES.md
  sha256: C3C564D96A3EF0E9EE9AFCCD44AE43785C311EF1A5262E5043C786DA8DF0E5AA
```

## Upstream Provenance

`UPSTREAM_PROVENANCE.md` records the official repository, release, tag, commit, immutable local source path, product target, import date, Git-object method, no-history/nested-Git boundary, corrected counts, source modifications and tracking-compatibility treatment.

```yaml
UpstreamProvenance:
  path: UPSTREAM_PROVENANCE.md
  sha256: 78DB7ACCCD38CACC1771792CA9C99CF3A063F60AC2E04D966E05CAE22C335B43
```

## Import Manifest

`SOURCE_IMPORT_MANIFEST.tsv` contains the required columns and exactly 6,115 data rows plus one header.

```yaml
HermesSourceImportManifest:
  path: SOURCE_IMPORT_MANIFEST.tsv
  sha256: 58A3392C7515EC2A8AAAF8E43530AE6299B2696957D095BE461DF51E8A080D5C
  data_rows: 6115
  imported_unmodified: 6111
  imported_modified_for_restricted_reference_removal: 3
  imported_modified_for_tracking_compatibility: 1
  initially_ignored_rows_with_rule_evidence: 39
  final_trackable_rows: 6115
```

Every unmodified row has equal source/product SHA-256. Every modified row has unequal hashes and an explicit reason.

## Exclusion Manifest

`SOURCE_EXCLUSIONS.tsv` contains the required columns and exactly 56 data rows plus one header.

```yaml
HermesSourceExclusionManifest:
  path: SOURCE_EXCLUSIONS.tsv
  sha256: 7A413310330E4625146BCAD9C73E62AF2634F5F3130530111A9B766DAF25D64E
  data_rows: 56
  restricted_powerpoint_subtree: 50
  restricted_generated_complete_skill_page: 2
  tracked_generated_skill_index_cache: 4
```

## Restricted-Content Validation

The following are absent:

```text
skills/productivity/powerpoint/**
website/docs/user-guide/skills/bundled/productivity/productivity-powerpoint.md
website/i18n/zh-Hans/docusaurus-plugin-content-docs/current/user-guide/skills/bundled/productivity/productivity-powerpoint.md
skills/index-cache/**
```

No bundled catalog or sidebar registration remains. No distinctive restrictive-license phrase was found in the product tree.

The 59 remaining exact `skills/productivity/powerpoint` or `productivity-powerpoint` matches were classified as 52 exclusion-manifest path rows, four permitted related-skill cross-references in OCR/finance documentation, and three notice/provenance/manifest statements. They are not restricted source copies or active catalog/sidebar registrations. The 77 broader PowerPoint/`.pptx` matches are permitted generic format handling, messaging, research, deliverable, OCR, independent finance-skill, test and legal/provenance references and were intentionally retained.

## Normal-Trackability Validation

```yaml
HermesNormalTrackability:
  expected_product_files: 6120
  ignored_expected_product_paths: 0
  status_untracked_product_paths: 6120
  status_non_untracked_product_paths: 0
  tracked_product_paths_before_human_staging: 0
  staged_product_paths: 0
  force_add_used: false
```

All authorized files are visible normally without staging or force-add.

## Sibling-Product Protection

The immediate siblings and synthetic descendants remained ignored with `git check-ignore` exit `0`; no sibling path appeared in status or the index, and sibling contents were not inspected or modified:

```text
2_products/backend-energyplus
2_products/cli
2_products/desktop
2_products/experimental
2_products/omniverse-app
2_products/web-platform
```

## Upstream No-Touch Validation

The locked upstream remained clean at the exact commit/tag/origin after import and validation. Root `.gitignore`, P12.C1, P12.C2, P12.C3, corrected P12.1, P11 records, README, workspace/product policies, `.graphifyignore`, `9_artifacts`, sibling products, `.opencode`, `AGENTS.md` and `graphify-out` were not modified by P12.2.

No network, provider, credential, package-manager, build, test or Hermes runtime operation occurred.

## Legal Unknowns and Human Review

The following remain unresolved:

```text
complete Python dependency SBOM not reviewed
complete npm dependency SBOM not reviewed
Rust/native/Nix/container dependency posture not cleared
fonts/images/templates/media provenance not fully cleared
documentation and generated-asset rights not fully reviewed
trademark and product-name use not cleared
hosted-service and commercial-distribution terms not decided
release package contents not validated
binary redistribution not authorized
```

This baseline is engineering evidence and not legal advice.

## Redistributability Boundary

```yaml
HermesProductRedistributability:
  source_snapshot_created: true
  engineering_notice_baseline_created: true
  restricted_known_subtree_excluded: true
  complete_legal_clearance: false
  complete_sbom_clearance: false
  redistribution_authorized: false
  publication_authorized: false
  hosted_production_release_authorized: false
```

## Rollback Procedure

If human review rejects this snapshot before commit:

1. Derive the exact 6,115 imported paths from `SOURCE_IMPORT_MANIFEST.tsv`.
2. Add only the five P12.2-created legal/provenance paths to that exact owned set.
3. Compare the actual product tree with the exact 6,120-file set.
4. Stop for human review if any unexplained path exists.
5. Remove only exact P12.2-created files and directories made empty by those removals.
6. Preserve the P12.1-created product root.
7. Revalidate sibling protection, root `.gitignore`, and locked upstream.

Never use Git clean/reset/restore/checkout, wildcard deletion, parent-directory deletion or broad recursive deletion without exact ownership proof. No rollback was required during corrected execution.

## P12.3 Readiness

```yaml
P12_3_Readiness:
  ready_after_human_acceptance_and_commit: true
  current_execution_started: false
  prerequisites:
    - P12.2 human acceptance
    - 6120 product files and this record committed in main repository
    - clean main repository status
```

P12.3 owns reproducible Python/Node environments, lockfile behavior, minimum development dependencies, cache/generated-state paths, developer commands and teardown. P12.2 installed nothing.

## P12.5 Design Readiness

```yaml
P12_5_DesignReadiness:
  design_ready_after_human_acceptance_and_commit: true
  synchronization_execution_authorized: false
```

P12.5 synchronization-policy design may consume the provenance and manifests after the same human commit. Fetch, merge, rebase, pull and push require a separate exact future gate.

## Created / Modified / Not Created Register

Created in the product root:

```text
6115 permitted upstream source files
NOTICE
THIRD_PARTY_NOTICES.md
UPSTREAM_PROVENANCE.md
SOURCE_IMPORT_MANIFEST.tsv
SOURCE_EXCLUSIONS.tsv
```

Modified from exact upstream bytes:

```text
.gitignore
website/docs/reference/skills-catalog.md
website/i18n/zh-Hans/docusaurus-plugin-content-docs/current/reference/skills-catalog.md
website/sidebars.ts
```

Modified in governance:

```text
0_architecture/governance/agent_platform_hermes_license_exclusion_notice_baseline.md
```

Not created or modified:

```text
restricted PowerPoint subtree, generated complete-skill pages or skills index cache
nested .git, product branch, product remote or independent history
worktree, submodule, subtree, symlink, hardlink or reparse point
dependency installation, build output, test output, runtime or generated state
adapter implementation or 9_artifacts/hermes
root .gitignore
P12.C1, P12.C2, P12.C3 or corrected P12.1
P11 records, README.md or workspace/product policy records
4_external/sources/hermes-agent/**
.opencode/**, AGENTS.md, graphify-out/** or sibling product contents
additional governance Markdown
```

## Validation Commands

Allowed operations were exact path/attribute checks, canonical-record searches, SHA-256 hashing, `git status`, `git diff --cached`, `git ls-files`, `git rev-parse`, `git check-ignore`, `git ls-tree`, `git cat-file --batch`, and read-only upstream status/tag/origin checks. A temporary standard-library-only helper performed inventory, import, hashing, manifest generation and exact-set validation and was kept outside the repository until final no-touch validation.

No Graphify command, package manager, install, build, test, lint, typecheck, Hermes runtime, provider/API/OAuth/MCP, credential inspection, network operation, staging, commit or push occurred.

## Final Verdict

```yaml
P12_2_CorrectedFinalVerdict:
  historical_external_snapshot_valid: false
  historical_external_snapshot_removed: true
  corrected_product_root: 2_products/hermes-agent
  corrected_snapshot_import_completed: true
  upstream_regular_file_count: 6171
  imported_upstream_file_count: 6115
  excluded_upstream_file_count: 56
  product_created_legal_provenance_file_count: 5
  final_product_file_count: 6120
  restricted_powerpoint_subtree_excluded: true
  restricted_generated_skill_pages_excluded: true
  restricted_registry_references_removed: true
  imported_paths_trackable_without_force_add: true
  sibling_products_remain_ignored: true
  nested_git_created: false
  upstream_reference_unchanged: true
  complete_legal_clearance: false
  redistribution_authorized: false
  git_staged_or_committed_by_agent: false
  P12_3_may_proceed_after_human_commit: true
  P12_5_design_may_proceed_after_human_commit: true
  final_verdict: license_exclusion_notice_baseline_ready
```

```text
hermes_license_exclusion_notice_baseline_ready
hermes_corrected_product_snapshot_imported
hermes_restricted_powerpoint_subtree_excluded
hermes_restricted_generated_skill_pages_excluded
hermes_restricted_registry_references_removed
hermes_mit_material_preserved
hermes_apache_2_material_preserved
hermes_apache_notice_preserved
hermes_third_party_notice_baseline_created
hermes_upstream_provenance_recorded
hermes_source_import_manifest_created
hermes_source_exclusion_manifest_created
hermes_imported_paths_trackable_without_force_add
hermes_locked_upstream_reference_unchanged
hermes_product_snapshot_ready_for_human_commit
hermes_P12_3_ready_after_human_commit
hermes_P12_5_design_ready_after_human_commit
product_redistributability_blocked_pending_clearance
no_deleted_external_snapshot_reuse
no_nested_git_created
no_installation
no_build_test_runtime
no_provider_activation
no_network_operation
no_git_index_or_history_mutation
```

## Human Commit Boundary

The agent did not stage, commit or push. After reviewing the complete baseline, the human may run:

```powershell
$ErrorActionPreference = "Stop"

$ProductRoot = "2_products/hermes-agent"
$Record = "0_architecture/governance/agent_platform_hermes_license_exclusion_notice_baseline.md"
$Manifest = Join-Path $ProductRoot "SOURCE_IMPORT_MANIFEST.tsv"

git status --short
git add -- $ProductRoot $Record

$ProductStaged = @(
    git diff --cached --name-only -- $ProductRoot |
        Sort-Object -Unique
)

if ($ProductStaged.Count -ne 6120) {
    throw "Unexpected staged product file count: $($ProductStaged.Count)"
}

$AllStaged = @(
    git diff --cached --name-only |
        Sort-Object -Unique
)

if ($AllStaged.Count -ne 6121) {
    throw "Unexpected total staged file count: $($AllStaged.Count)"
}

$Unexpected = @(
    $AllStaged |
        Where-Object {
            $_ -ne $Record -and
            -not $_.StartsWith(
                "$ProductRoot/",
                [System.StringComparison]::Ordinal
            )
        }
)

if ($Unexpected.Count -gt 0) {
    throw "Unexpected staged paths: $($Unexpected -join ', ')"
}

$ManifestRows = @(
    Import-Csv -LiteralPath $Manifest -Delimiter "`t"
)

if ($ManifestRows.Count -ne 6115) {
    throw "Unexpected import manifest row count: $($ManifestRows.Count)"
}

$ExecutablePaths = @(
    $ManifestRows |
        Where-Object { $_.upstream_mode -eq "100755" } |
        ForEach-Object {
            "$ProductRoot/$($_.path.Replace('\','/'))"
        } |
        Sort-Object -Unique
)

if ($ExecutablePaths.Count -ne 59) {
    throw "Unexpected executable path count: $($ExecutablePaths.Count)"
}

foreach ($ExecutablePath in $ExecutablePaths) {
    git update-index --chmod=+x -- $ExecutablePath
    if ($LASTEXITCODE -ne 0) {
        throw "Could not preserve executable mode: $ExecutablePath"
    }
}

git diff --cached --stat
git commit -m "P12.2 - Import Hermes baseline with license exclusions"
git push origin main
```

Before committing, verify that no sibling product, `.opencode`, `AGENTS.md`, `graphify-out` or `4_external/sources/hermes-agent` path is staged and that all excluded paths remain absent.

Never use `git add .`, `git add -A` or `git add -f`.
