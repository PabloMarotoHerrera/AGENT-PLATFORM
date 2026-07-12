# P12.2 - Hermes License Exclusion and Notice Baseline

## 1. Document Header

| Field | Value |
| --- | --- |
| Project | P12 - Hermes Productization Foundation |
| Ticket | P12.2 - License Exclusion and Notice Baseline |
| Type | Compliance / license / controlled product patch |
| Date | 2026-07-12 |
| Status | `rolled_back_due_to_invalid_product_root` |
| Canonical output | `0_architecture/governance/agent_platform_hermes_license_exclusion_notice_baseline.md` |
| Product root | Historical invalid root `C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES`; removed by P12.C1 |
| Upstream reference | `C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\4_external\sources\hermes-agent` |
| Legal posture | Engineering compliance baseline only; not legal advice or distribution approval |

Result markers:

```text
hermes_p12_2_material_result_rolled_back
hermes_external_product_root_removed
hermes_p12_2_reopened
upstream_locked_reference_untouched
hermes_topology_redefinition_required
no_current_product_snapshot
no_product_legal_baseline_commit
no_installation
no_hermes_execution
no_provider_activation
no_git_history_rewrite
```

## 2. Purpose

P12.2 historically created the first controlled Hermes product-source snapshot
in the sibling repository then treated as P12.1-authorized. P12.C1 determined
that root was outside the human-authorized workspace and removed the complete
material snapshot and repository after ownership proof. The historical work
applied the restrictive PowerPoint exclusion before material entered the
product repository, preserved applicable MIT and Apache-2.0 materials, created
product NOTICE and third-party notice baselines, recorded deterministic import
and exclusion inventories, and retained unresolved license questions for
human/legal review.

The legal filtering logic, manifests and conclusions in this canonical record
remain useful evidence, but no current product snapshot or product legal
baseline exists. P12.2 is reopened and must be executed again only after P12.C2
and corrected P12.1 establish an authorized product topology. All historical
ready or completed statements below are superseded by this correction.

P12.C1 did not install, build, test or execute Hermes. It did not contact a
remote, activate providers/API/OAuth/MCP, inspect credentials, stage, commit,
push, publish, release, host, deploy or grant redistributability.

## 3. Current Posture

```yaml
P12_2_CurrentPosture:
  status: rolled_back_due_to_invalid_product_root
  product_root_authorized: false
  product_root_exists: false
  repository_mode: undefined_pending_P12_C2
  source_history_mode: undefined_pending_P12_C2
  source_snapshot_imported: false_removed_by_P12_C1
  source_snapshot_committed: false
  restricted_powerpoint_skill_included: not_applicable_no_current_snapshot
  top_level_mit_license_preserved: historical_evidence_only
  apache_2_license_preserved: historical_evidence_only
  apache_notice_preserved: historical_evidence_only
  third_party_notice_baseline_created: false_current_material_removed
  complete_sbom_license_clearance: false
  redistribution_authorized: false
  publication_authorized: false
  runtime_authorized: false
```

No product repository currently exists. Before deletion P12.C1 found no commit,
tag, ref, additional branch, `origin` or writable remote, but found all 6,116
P12.2 files staged in the unborn repository index. This corrects the historical
statement that no staging occurred. The staged index was removed with the
invalid repository; no Git history existed or was rewritten.

## 4. Historical Prerequisite Resolution - Superseded

This table records the prerequisite view used during historical P12.2
execution. P12.C1 supersedes its P12.1 acceptance and readiness conclusions.

| Prerequisite | Current canonical resolution | Result |
| --- | --- | --- |
| P12.0 historical expected filename | Current file is `agent_platform_hermes_productization_authorization_and_boundary.md` | Accepted; productization and P12.2 baseline authorized |
| P12.1 topology | `agent_platform_hermes_controlled_fork_repository_topology.md` | Superseded; invalid root removed, P12.1 reopened, P12.C2 required |
| P11 closure | `agent_platform_hermes_integration_closure.md` | Accepted; integration ready with limitations |
| P11 source lock | `agent_platform_hermes_source_review_authorization.md` | Accepted; exact upstream repository/release/tag/SHA/path retained |
| P11 license audit | `agent_platform_hermes_license_dependency_runtime_audit.md` | Accepted with mixed-license and SBOM blockers retained |

The prior P12.2 safe stop created no Markdown or product file because P12.1 and
an exact product root were then absent. After P12.1 created and validated the
root, this same ticket re-entered without creating a blocked, retry, rerun,
safe-block, diagnostic, readiness or marker-alignment document.

## 5. Inputs Reviewed

Governance and policy inputs:

```text
agent_platform_hermes_productization_authorization_and_boundary.md
agent_platform_hermes_controlled_fork_repository_topology.md
agent_platform_hermes_integration_closure.md
agent_platform_hermes_source_review_authorization.md
agent_platform_hermes_license_dependency_runtime_audit.md
applicable P9/S-00-S-04 boundaries already incorporated by P12.0/P12.1
```

Read-only upstream license/source metadata:

```text
LICENSE
plugins/hermes-achievements/LICENSE
plugins/security-guidance/LICENSE
plugins/security-guidance/NOTICE
skills/creative/humanizer/LICENSE
skills/productivity/powerpoint/LICENSE.txt
the exact restricted PowerPoint subtree tracked-path inventory
the two generated complete-skill documentation pages
the exact English/Chinese catalog rows and sidebar registration
tracked-file modes, blob identities and source hashes
```

No credential, `.env` value, provider configuration, user state, runtime DB,
product/Siamese source, Graphify output, Paperclip source or GBrain source was
inspected.

## 6. P12.0 Authorization Status

P12.0 is present at the current canonical path and authorizes P12 productization
planning and the P12.2 legal/notice baseline. It requires an immutable upstream,
a separately controlled lineage, exclusion or separate clearance of the
PowerPoint subtree, preservation of Apache-2.0/NOTICE obligations, no whole-tree
MIT claim, human Git authority, and no runtime or provider activation.

```text
P12.0 substantive authorization: accepted
P12.2 historical readiness marker: superseded_by_P12_C1
P12.0 product root assignment: delegated to P12.1
```

## 7. Historical P12.1 Product Root / Topology Status - Superseded

P12.1 historically created and validated the following topology. P12.C1 later
invalidated and removed it:

```yaml
HermesProductRoot:
  path: C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES
  repository_mode: sibling_fresh_git_repository
  source_history_mode: snapshot_import_without_upstream_git_history
  default_branch: main
  current_commit: none
  source_before_P12_2: none
  upstream_fetch_url: https://github.com/NousResearch/hermes-agent.git
  upstream_push_url: DISABLED
  origin: absent
  network_operations_authorized: false
```

P12.1 explicitly assigns the first controlled snapshot import, restrictive
subtree exclusion, notice/attribution baseline and provenance inventory to
P12.2. The root being outside AGENT PLATFORM was the governance defect. No
current product root is defined; P12.C2 owns the replacement decision.

## 8. Upstream Locked Reference

```yaml
HermesLockedUpstreamReference:
  repository: https://github.com/NousResearch/hermes-agent
  release: 0.18.2
  tag: v2026.7.7.2
  commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  path: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\4_external\sources\hermes-agent
  posture: immutable_read_only
```

Pre-import and post-import metadata checks matched the required HEAD and tag,
the official origin URL, and an empty `git status --short`. Per-command
`safe.directory` was used only for read-only metadata because Git rejected one
direct inventory attempt on ownership safety grounds. No global Git config was
changed.

## 9. Historical Product Root - Removed

```text
C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES (removed by P12.C1)
```

The root initially contained only `.git`. P12.2 copied a sorted allowlist of
tracked regular files into matching source-relative paths. It did not copy
upstream `.git` or history. It did not use hardlinks, symlinks, submodules,
clone, archive extraction, fetch, pull or network access.

Historical pre-removal product file inventory:

```text
upstream tracked files considered: 6171
upstream tracked files imported: 6111
upstream tracked files excluded: 60
P12.2-created legal/provenance files: 5
total product files outside .git: 6116
reparse points outside .git: 0
```

## 10. License Inventory

| Product path | Classification | Preservation result | SHA-256 |
| --- | --- | --- | --- |
| `LICENSE` | MIT, Nous Research | Exact upstream bytes preserved | `E29DFAF6905A8D396A58EA4BD84AD27057756BBD9599B5BEC0971AE34D2A2118` |
| `plugins/hermes-achievements/LICENSE` | MIT, Hermes Achievements contributors | Exact upstream bytes preserved | `D40010024938B643E3D5E304A17563A2EEC1815B8686726474DC00B3F797EDC0` |
| `skills/creative/humanizer/LICENSE` | MIT, Siqi Chen | Exact upstream bytes preserved | `CAA1BE9CBA41C1AFB88FE730AB1A4E04728295EA5B29AC2EE9F003A4FFBE3A77` |
| `plugins/security-guidance/LICENSE` | Apache License 2.0 | Exact upstream bytes preserved | `3DDF9BE5C28FE27DAD143A5DC76EEA25222AD1DD68934A047064E56ED2FA40C5` |
| `skills/productivity/powerpoint/LICENSE.txt` | Restrictive Anthropic service-linked terms | Not imported; entire subtree excluded | N/A |

The complete imported tree is not uniformly MIT. No transitive dependency,
asset, font, image, template, documentation or toolchain license is represented
as cleared merely because a lockfile, manifest or source file was imported.

## 11. Notice Inventory

| Notice surface | Upstream status | Product status | Decision |
| --- | --- | --- | --- |
| Top-level `NOTICE` | Absent | Created | Product notice identifies upstream, Apache attribution and exclusion baseline |
| `plugins/security-guidance/NOTICE` | Present | Present, exact upstream bytes | Required Anthropic source attribution preserved |
| `THIRD_PARTY_NOTICES.md` | Absent | Created | Engineering inventory, exclusions, unknowns and redistributability boundary recorded |
| MIT copyright/permission/disclaimer | Present in license files | Preserved | Must remain with copies or substantial portions as applicable |

The nested Apache notice hash matches upstream:

```text
152C0F404A6BFCC9430CF90269FD05A984B92F2F971EEEC7E6F1C4DC100A53AF
```

## 12. Third-Party Notice Baseline

Created:

```text
C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES\THIRD_PARTY_NOTICES.md
```

It records the exact Hermes upstream identity, MIT and Apache-2.0 materials,
Apache NOTICE obligations, PowerPoint exclusion, generated/cache exclusion,
dependency and asset uncertainty, human/legal review items, and the explicit
no-redistribution/no-publication posture.

## 13. Restricted PowerPoint Skill Identification

The exact restricted source is:

```text
skills/productivity/powerpoint/**
```

Git tracked 50 regular files under that subtree. Its `LICENSE.txt` states that
the materials may not be extracted or retained outside Anthropic services,
reproduced, copied, used for derivative works, distributed, sublicensed or
transferred except as allowed by the applicable agreement. P12.2 treats the
entire subtree as restricted and makes no legal-clearance inference.

Two tracked generated documentation pages reproduced the complete skill
definition and were therefore classified as restricted generated copies:

```text
website/docs/user-guide/skills/bundled/productivity/productivity-powerpoint.md
website/i18n/zh-Hans/docusaurus-plugin-content-docs/current/user-guide/skills/bundled/productivity/productivity-powerpoint.md
```

The inventory found no tracked symlink or submodule. Generic references to
PowerPoint as a file format, application, optional independent skill or prose
concept are not classified as copies of the restricted subtree. They remain
subject to human product-quality and trademark review.

## 14. Restricted PowerPoint Skill Exclusion

The restricted subtree and two generated complete-skill pages were excluded
from the tracked-file allowlist before copying. No wildcard deletion occurred,
and no restricted path was first copied and then removed.

Verification:

```text
skills/productivity/powerpoint exists in product: False
English generated complete-skill page exists: False
Chinese generated complete-skill page exists: False
restricted proprietary license phrases found in product: none
```

Exact exclusion paths, Git modes, upstream blob identities and reasons are in:

```text
SOURCE_EXCLUSIONS.tsv
```

## 15. Registry / Index Reference Changes

Only three imported source files were modified:

| Product file | Exact change |
| --- | --- |
| `website/docs/reference/skills-catalog.md` | Removed the exact bundled `powerpoint` catalog row. |
| `website/i18n/zh-Hans/docusaurus-plugin-content-docs/current/reference/skills-catalog.md` | Removed the exact translated bundled `powerpoint` catalog row. |
| `website/sidebars.ts` | Removed the exact `productivity-powerpoint` sidebar entry. |

The tracked `skills/index-cache/` directory was excluded as cache material,
including external catalog cache entries that mention PowerPoint. Final checks
found no `productivity-powerpoint` or exact ``productivity/powerpoint`` entry in
the product skill catalogs or sidebar.

## 16. Product Files Created / Modified / Deleted

Created inside the product root:

```text
6111 permitted upstream tracked source files at preserved relative paths
NOTICE
THIRD_PARTY_NOTICES.md
UPSTREAM_PROVENANCE.md
SOURCE_IMPORT_MANIFEST.tsv
SOURCE_EXCLUSIONS.tsv
```

Modified after import:

```text
website/docs/reference/skills-catalog.md
website/i18n/zh-Hans/docusaurus-plugin-content-docs/current/reference/skills-catalog.md
website/sidebars.ts
```

Deleted inside the product root:

```text
none
```

The 60 excluded upstream paths never entered the product repository.

## 17. Upstream Files Read / Not Modified

P12.2 read only the authorized upstream legal files, exact restricted-skill
metadata/content needed for classification, exact catalog/sidebar references,
tracked path/mode/blob inventory, and source bytes needed for deterministic hash
verification.

P12.2 did not modify, stage, commit, checkout, reset, clean, merge, rebase,
stash, tag, fetch, pull or push the upstream repository. Final upstream status
remained clean at the locked commit and tag.

## 18. License Obligations Preserved

| Obligation | Baseline |
| --- | --- |
| Top-level MIT | Preserve Nous Research copyright, permission notice, warranty disclaimer and liability disclaimer. |
| Nested MIT | Preserve the Hermes Achievements and Siqi Chen notices for their applicable materials. |
| Apache-2.0 | Preserve license, applicable copyright/patent/trademark/attribution notices, NOTICE and modification notices when required. |
| Restricted PowerPoint materials | Excluded; no right to retain, modify, reproduce or distribute is claimed. |
| Whole-tree classification | Do not label the inherited product tree uniformly MIT. |
| Dependency/asset clearance | Require reviewed SBOM and license/asset inventory before distribution, release, packaging, hosting or publication. |
| Trademark/name use | Requires separate human/legal review; copyright licenses do not decide trademark permission. |

## 19. License Unknowns / Human Review Items

- Complete Python, npm, Rust, Nix, container and native dependency license/SBOM
  clearance has not been performed.
- Fonts, images, templates, documentation, generated assets and other media need
  explicit provenance and license review before distribution.
- Thirty upstream-tracked files are ignored by the imported `.gitignore`,
  including fonts, images, examples, data and scripts. They are present and
  inventoried, but any future staging must use the exact manifest and receive a
  separate human tracking decision.
- Generic PowerPoint references remain in unrelated code/docs; human review must
  decide product-quality, branding and trademark treatment.
- Any future change in `plugins/security-guidance/` must satisfy Apache-2.0
  prominent modification-notice requirements where applicable.
- Distribution model, jurisdictions, product naming, hosted use and commercial
  terms remain human/legal decisions.

## 20. Historical Compliance Evidence - No Current Product Baseline

```yaml
HermesProductComplianceBaseline:
  current_material_baseline_exists: false
  legal_filtering_logic_retained_as_evidence: true
  source_provenance_recorded: true
  deterministic_import_manifest_created: true
  deterministic_exclusion_manifest_created: true
  restricted_powerpoint_subtree_absent: true
  restricted_generated_skill_pages_absent: true
  exact_powerpoint_catalog_sidebar_entries_absent: true
  top_level_mit_preserved: true
  nested_mit_notices_preserved: true
  apache_2_license_preserved: true
  apache_notice_preserved: true
  third_party_notice_created: true
  tree_uniformly_mit: false
  complete_sbom_ready: false
  legal_clearance_complete: false
  redistributable: false_pending_human_legal_and_sbom_clearance
```

`SOURCE_IMPORT_MANIFEST.tsv` contains 6,111 data entries plus a header. Every
unmodified import has matching source/product SHA-256. Exactly three entries are
marked `imported_modified_for_p12_2`; no undeclared content mismatch exists.
`SOURCE_EXCLUSIONS.tsv` contains 60 entries plus a header.

## 21. No-Execution / No-Install Boundary

```text
no installation
no Hermes execution
no package manager
no dependency resolution
no build
no test
no lint or typecheck
no dashboard, gateway, worker or runtime
no provider/model/API/OAuth/MCP
no credentials, secrets or .env values
no Graphify, Paperclip or GBrain
no fetch, pull, push or other remote network operation
no commit; P12.C1 later found 6116 staged index entries in the invalid unborn repository
```

One initial direct `git ls-files` inventory attempt was rejected by Git's
dubious-ownership guard and produced no file change. The read-only inventory was
repeated with a per-command `safe.directory` override. A shell `rg` attempt was
unavailable and produced no file change; exact tracked-reference searches used
read-only Git grep instead. No unsafe fallback was used.

## 22. Stop Rules

Stop productization progression if:

```text
the locked upstream identity or clean status changes
the restricted PowerPoint subtree or complete generated copies reappear
an exact exclusion or provenance record becomes ambiguous
MIT, Apache-2.0 or applicable NOTICE material is removed or obscured
the complete tree is represented as uniformly MIT
an unknown dependency, asset, font, template or documentation license is treated as cleared
redistribution, publication, release or hosting is proposed before human/legal and SBOM clearance
source import requires hardlinks, symlinks, submodules or upstream history
the product root overlaps the immutable upstream
package manager, build, test, runtime, provider, credential, MCP or network activity is required
Git staging, commit or push is requested without exact human approval
```

## 23. Rollback Result

P12.C1 executed the complete repository rollback after proving that the exact
filesystem set consisted only of the 6,111 manifest paths and five documented
legal/provenance files. The invalid root, its staged index and all material
P12.2 outputs were removed. The locked upstream remained unchanged. The
historical procedure below is retained only as prior evidence and is not a
current instruction.

1. Require explicit human approval and identify whether rollback covers only
   legal/provenance records, the three catalog/sidebar edits, or the complete
   snapshot import.
2. Preserve the current `SOURCE_IMPORT_MANIFEST.tsv` and
   `SOURCE_EXCLUSIONS.tsv` as the exact path inventories before any action.
3. Restore the three modified catalog/sidebar files only from their exact paths
   in the still-locked upstream reference, then verify their hashes.
4. Restore prior product `NOTICE` and `THIRD_PARTY_NOTICES.md` only from a
   reviewed product commit or approved retained copy when one exists.
5. For complete snapshot rollback before the first product commit, remove only
   paths enumerated in `SOURCE_IMPORT_MANIFEST.tsv` plus the five exact
   P12.2-created legal/provenance files. Preserve product `.git` and P12.1 remote
   metadata. Remove empty directories only after exact path review.
6. Restore the restricted PowerPoint subtree or its exact registry references
   only after a new explicit legal clearance and product authorization. If
   restored, update all notices, manifests and redistributability decisions.
7. Verify the immutable upstream remains clean at the locked SHA/tag.
8. Never use broad reset, clean, wildcard deletion or repository removal.

## 24. Future Validation Targets - Blocked

P12.3 and all later execution remain blocked until P12.C2 and corrected
P12.1/P12.2 complete.

- Validate the manifest-driven initial product commit under separate exact human
  Git approval, including the 30 upstream-tracked files hidden by `.gitignore`.
- Produce a complete dependency and asset SBOM/license inventory before release.
- Verify reproducible environment creation only in P12.3.
- Run baseline build/test/UI validation only in P12.4.
- Define and validate upstream synchronization only in P12.5.
- Re-run restricted-content and notice checks after every upstream update.
- Validate Apache modification notices if the security-guidance subtree changes.
- Validate package/release contents separately from source-repository contents.

## 25. Future Hardening Candidates

```text
P12-LIC-HARD-01 - Dependency and Asset SBOM License Review
P12-LIC-HARD-02 - Font Image Template and Documentation Provenance Review
P12-LIC-HARD-03 - Restricted Content Regression Gate
P12-LIC-HARD-04 - NOTICE and Attribution Packaging Validation
P12-LIC-HARD-05 - Product Trademark and Naming Review
P12-LIC-HARD-06 - Manifest-Driven Initial Commit Review
P12-LIC-HARD-07 - Release Redistributability Decision
```

These are candidate scopes only and no additional Markdown was created.

## 26. Historical Created / Modified / Deleted / Not Touched Register

Created in AGENT PLATFORM:

```text
0_architecture/governance/agent_platform_hermes_license_exclusion_notice_baseline.md
```

Historically created in the product root and removed by P12.C1:

```text
6111 permitted imported source files
NOTICE
THIRD_PARTY_NOTICES.md
UPSTREAM_PROVENANCE.md
SOURCE_IMPORT_MANIFEST.tsv
SOURCE_EXCLUSIONS.tsv
```

Historically modified in the product root and removed by P12.C1:

```text
website/docs/reference/skills-catalog.md
website/i18n/zh-Hans/docusaurus-plugin-content-docs/current/reference/skills-catalog.md
website/sidebars.ts
```

Deleted by P12.C1:

```text
C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES in full after exact ownership proof; restricted material had been excluded before import
```

Not touched:

```text
4_external/sources/hermes-agent/** by write or Git mutation
.opencode/
AGENTS.md
graphify-out/
.gitignore
.graphifyignore
product .git history; P12.C1 found and removed the P12.2-staged index
product remote network state
credentials, secrets, .env values, OAuth, browser auth, provider configs
product/Siamese, GBrain, GStack, Paperclip, ECC and OpenCode source
P12.0, P12.3-P12.R and P13-P21 documents; P12.C1 later corrected P12.1
```

## 27. Required Next Ticket

```text
P12.C2 - Corrected Hermes Product Topology Definition
```

P12.C1 does not create a replacement topology. P12.2 is reopened and must run
again only after corrected P12.1. P12.3 and later execution are blocked.

## 28. Final Verdict

```yaml
P12_2_FinalVerdict:
  verdict: rolled_back_due_to_invalid_product_root
  product_root_resolved: false_pending_P12_C2
  snapshot_import_completed: false_current_material_removed
  historical_imported_tracked_file_count: 6111
  historical_excluded_tracked_file_count: 60
  legal_filtering_logic_retained_as_evidence: true
  current_product_snapshot_exists: false
  product_legal_baseline_commit_exists: false
  p12_2_reopened: true
  corrected_p12_1_required: true
  P12_3_and_later_blocked: true
  upstream_reference_untouched: true
  notice_baseline_preserved: historical_evidence_only
  third_party_notice_baseline_created: false_current_material_removed
  license_unknowns_flagged: true
  complete_redistribution_clearance: false
  installation_performed: false
  hermes_executed: false
  provider_activated: false
  graphify_used: false
  historical_staging_found_by_P12_C1: true_6116_index_entries
  git_commit_created: false
```

```text
hermes_p12_2_material_result_rolled_back
hermes_external_product_root_removed
hermes_p12_2_reopened
upstream_locked_reference_untouched
hermes_topology_redefinition_required
no_current_product_snapshot
no_product_legal_baseline_commit
no_installation
no_hermes_execution
no_provider_activation
no_git_history_rewrite
```

## 29. Commit Recommendation Boundary

P12.C1 found that all 6,116 product files had been staged in the invalid unborn
repository despite the historical no-staging claim. No commit, ref or push
existed. The complete repository and index were removed without rewriting Git
history. No product-repository commit is currently possible because no product
repository exists.

Never use or recommend `git add .`.
