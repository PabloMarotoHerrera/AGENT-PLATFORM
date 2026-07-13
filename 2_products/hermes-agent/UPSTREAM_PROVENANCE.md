# Upstream Provenance

## Source Identity

| Field | Value |
| --- | --- |
| Official repository | `https://github.com/NousResearch/hermes-agent` |
| Release | `0.18.2` |
| Tag | `v2026.7.7.2` |
| Commit | `9de9c25f620ff7f1ce0fd5457d596052d5159596` |
| Immutable local reference | `4_external/sources/hermes-agent` |
| Product target | `2_products/hermes-agent` |
| Import date | `2026-07-13` |

## Import Method

The exact locked commit was enumerated with local read-only Git object metadata.
Every selected regular blob was read through `git cat-file --batch`, validated
for safe destination containment, written as a new normal file at its original
repository-relative path, and verified by source/product SHA-256 equality before
planned product modifications.

No upstream worktree bytes, deleted external snapshot, clone, archive extraction,
hardlink, symlink, junction, reparse point, submodule, network operation or
upstream Git history was imported. The product root contains no nested `.git`.

## Inventory

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

## Product Modifications

Exactly one restricted bundled-skill registration was removed from each of:

- `website/docs/reference/skills-catalog.md`
- `website/i18n/zh-Hans/docusaurus-plugin-content-docs/current/reference/skills-catalog.md`
- `website/sidebars.ts`

The imported product-local `.gitignore` received one delimited compatibility
block with exact negations for 39 upstream-tracked files that inherited ignore
rules. No root `.gitignore` change or force-add is required.

`SOURCE_IMPORT_MANIFEST.tsv` records all imported paths, upstream modes, blob
IDs, source/product hashes, modifications, initial ignore evidence and final
trackability. `SOURCE_EXCLUSIONS.tsv` records every excluded path and reason.
