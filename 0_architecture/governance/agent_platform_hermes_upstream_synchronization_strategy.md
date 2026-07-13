# P12.5 - Hermes Upstream Synchronization Strategy

## Document Header

| Field | Value |
| --- | --- |
| Project | P12 - Hermes Productization Foundation |
| Ticket | P12.5 - Hermes Upstream Synchronization Strategy |
| Type | Source synchronization architecture / provenance / governance |
| Date | 2026-07-13 |
| Status | `upstream_synchronization_strategy_ready` |
| Canonical output | `0_architecture/governance/agent_platform_hermes_upstream_synchronization_strategy.md` |
| Durable governance document count | Exactly one |
| Product root | `2_products/hermes-agent` |
| Current immutable reference | `4_external/sources/hermes-agent` |
| Preferred future candidate reference | `4_external/sources/hermes-agent-candidate` |
| Execution class | Documentation plus bounded read-only baseline verification |
| Network operation | Prohibited and not performed |
| Synchronization execution | Prohibited and not performed |
| Product/upstream source modification | Prohibited and not performed |
| Git staging / commit / push | Prohibited and not performed |

## Purpose

Define the authoritative, deterministic and human-gated method for evaluating and integrating a future Hermes upstream commit into the AGENT PLATFORM-owned product subtree without performing an update now.

This strategy preserves the immutable upstream-reference model, P12.2 restricted-content and legal boundaries, P12.3 environment authority, P12.4 baseline comparability, explicit AGENT PLATFORM product divergence, main-repository ownership, exact rollback and human Git authority. It rejects pull/merge/rebase-based product synchronization, blind filesystem overwrite, semantic auto-merge, product-local Git history, product remotes, nested repositories and long-lived synchronization branches.

## Prerequisite Status

```yaml
P12_5_PrerequisiteStatus:
  p12_2_record_committed: true
  p12_2_commit: e3455d9135096e1901f563359d7911abbf3d4bbc
  p12_3_record_committed: true
  p12_3_commit: 0b5ea15bc2ce8d36b0218eb3d03639944637ffb7
  p12_4_record_committed: true
  p12_4_commit: a7328ac6ce67227243a9daad43d65c424fe22565
  main_branch: main
  main_head: a7328ac6ce67227243a9daad43d65c424fe22565
  origin_main_matches_head: true
  staged_path_count: 0
  product_status_path_count: 0
  product_tracked_file_count: 6120
  product_nested_git_present: false
  baseline_hash_mismatch_count: 0
  locked_upstream_clean: true
  locked_upstream_commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  locked_upstream_tag: v2026.7.7.2
  candidate_path_exists: false
  synchronization_workspace_exists: false
  invalid_external_product_root_exists: false
  prerequisite_result: pass
```

Only `.opencode/`, `AGENTS.md` and `graphify-out/` were present as permitted unrelated untracked paths. They were not inspected, modified or staged. Read-only upstream identity commands used command-scoped `safe.directory`; no global Git configuration changed.

## Current Baseline Identity

```yaml
HermesCurrentSynchronizationBaseline:
  upstream_repository: https://github.com/NousResearch/hermes-agent
  observed_upstream_origin: https://github.com/nousresearch/hermes-agent.git
  upstream_release: 0.18.2
  upstream_tag: v2026.7.7.2
  upstream_commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  product_root: 2_products/hermes-agent
  imported_upstream_files: 6115
  imported_unmodified_files: 6111
  compliance_modified_imports: 4
  excluded_upstream_files: 56
  product_created_control_files: 5
  final_product_files: 6120
  initially_ignored_imported_files: 39
  P12_2_commit: e3455d9135096e1901f563359d7911abbf3d4bbc
  P12_3_commit: 0b5ea15bc2ce8d36b0218eb3d03639944637ffb7
  P12_4_commit: a7328ac6ce67227243a9daad43d65c424fe22565
  P12_2_product_tree: 07bc27d2cc3b015b3865d62d7fdbc7dfe0ab6fb7
  P12_4_product_tree: 07bc27d2cc3b015b3865d62d7fdbc7dfe0ab6fb7
  product_paths_changed_between_P12_2_and_P12_4: 0
  current_post_P12_2_product_delta: empty
  P12_4_verdict: baseline_usable_with_known_failures
```

Current exclusion classes are historical facts, not future expected counts:

| Class | Current count |
| --- | ---: |
| `restricted_powerpoint_subtree` | 50 |
| `restricted_generated_complete_skill_page` | 2 |
| `tracked_generated_skill_index_cache` | 4 |
| Total | 56 |

Current compliance-modified imported paths are `.gitignore`, the English and Chinese generated skills catalogs, and `website/sidebars.ts`. The five product-owned control files are `UPSTREAM_PROVENANCE.md`, `SOURCE_IMPORT_MANIFEST.tsv`, `SOURCE_EXCLUSIONS.tsv`, `NOTICE` and `THIRD_PARTY_NOTICES.md`.

## Synchronization Principles

```yaml
HermesSynchronizationPrinciples:
  upstream_reference_is_immutable: true
  product_is_main_repository_subtree: true
  product_has_no_independent_git_history: true
  synchronization_is_snapshot_based: true
  synchronization_is_manifest_driven: true
  candidate_is_locked_before_comparison: true
  restricted_content_is_excluded_before_import: true
  compliance_transformations_are_candidate_specific: true
  product_changes_are_preserved_explicitly: true
  automatic_semantic_conflict_resolution: prohibited
  human_review_required: true
  dry_run_required: true
  baseline_regression_comparison_required: true
  rollback_must_be_exact: true
  publication_authorized: false
```

The strategy never relies on `git pull`, product-root merge/rebase, an upstream remote attached to the product, nested Git, submodule/subtree machinery, a floating branch name, archive trust without commit proof, worktree-byte copying or uncontrolled incremental overwrite.

## Source Model

```yaml
HermesUpstreamSourceModel:
  current_reference:
    path: 4_external/sources/hermes-agent
    role: immutable_reference_for_current_baseline_A
    commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
    editable: false
  future_candidate_reference:
    preferred_path: 4_external/sources/hermes-agent-candidate
    role: detached_read_only_candidate_B
    permanence: temporary_until_rejected_removed_or_explicitly_promoted
    repository_mode: isolated_external_source_reference
    editable: false
  product:
    path: 2_products/hermes-agent
    role: AGENT_PLATFORM_owned_editable_product_C
    repository: AGENT_PLATFORM_main_repository
    nested_git: false
    product_remote: false
  construction_workspace:
    path_template: 9_artifacts/hermes/synchronization/<candidate-full-sha>
    role: ignored_offline_projection_comparison_and_transaction_evidence
```

The default acquisition model is a separate read-only candidate Git checkout under `4_external/sources`. It remains inside AGENT PLATFORM, outside `2_products`, outside `9_artifacts`, and disjoint from the current immutable reference. A temporary bare/object repository or verified source archive is a non-default exception requiring an explicit future architecture decision and equivalent commit/tree identity proof.

Only one candidate may occupy the preferred candidate path at a time. Candidate rejection removes only that exact owned path after a separate cleanup gate. Candidate acceptance does not silently mutate the current reference. Any promotion/rotation of `4_external/sources/hermes-agent-candidate` into the next canonical immutable reference is a separately approved external-source operation performed only after integration and rollback acceptance.

## Candidate Identity Contract

```yaml
HermesUpstreamCandidateIdentity:
  repository_url: exact_official_url
  normalized_repository_identity: exact_expected_owner_and_repository
  release: exact_release_or_none
  tag: exact_tag_or_none
  tag_object_id: exact_object_or_none
  peeled_tag_commit: exact_full_sha_or_none
  commit: exact_full_sha
  commit_object_type: commit
  object_format: sha1_or_declared_future_format
  commit_reachable_from_official_origin: true
  descendant_of_current_baseline: true_or_exceptionally_human_approved
  signed_tag_or_commit_status: verified_or_not_available
  signature_policy_and_key_identity: recorded
  source_tree_object_id: exact_tree_object_id
  object_completeness_verified: true
  acquisition_timestamp: exact_timestamp
  acquired_by: exact_human_or_authorized_agent
  candidate_path: exact_local_path
  detached_head: true
  branch_name: none
  worktree_clean: true
```

`main`, `master`, `latest`, `develop`, release labels and tags are discovery metadata only. No floating name is candidate authority. An annotated tag must record both tag object and peeled commit. A missing signature is recorded as `not_available`, not silently represented as verified. Origin mismatch, missing object, incomplete tree, ambiguous tag resolution or unapproved non-descendant history rejects the candidate before source projection.

File identity is `(presence, Git mode, Git object ID, SHA-256 of exact blob bytes)`. Comparison does not use timestamps, OneDrive metadata, filesystem line-ending conversion or worktree executable inference. The future helper must read candidate bytes from Git objects.

## Candidate Acquisition Boundary

Candidate acquisition is a separate network/source gate and is not executed by P12.5.

Required preconditions:

```text
human explicitly authorizes exact network commands
official repository URL is normalized and verified
exact candidate SHA is approved
candidate path is absent and contained under 4_external/sources
current product, index and immutable reference are clean
no credentials or private registry are required
all network commands and expected objects are listed before execution
rollback/removal ownership for the candidate path is explicit
```

Permitted future shape, subject to that gate:

```powershell
git clone --no-checkout `
  "https://github.com/NousResearch/hermes-agent" `
  "4_external/sources/hermes-agent-candidate"

git -C "4_external/sources/hermes-agent-candidate" `
  checkout --detach "<exact-full-sha>"
```

The future execution record must list actual commands, refs and objects; verify official-origin reachability, commit/tree/tag identity, signatures when available, detached HEAD and clean status; prohibit push; avoid global Git configuration mutation; and create no branch. If command-scoped safe-directory trust is needed, the exact path and read-only use must be approved and recorded.

Candidate acquisition does not authorize package installation, source import, product replacement, test/build/runtime execution, staging, commit, push or reference promotion.

## Product Change Classification

```yaml
HermesProductChange:
  path: exact_normalized_repository_relative_path
  baseline_upstream_commit: exact_full_sha
  baseline_source_object: exact_object_or_none
  baseline_source_sha256: exact_hash_or_none
  accepted_filtered_base_sha256: exact_hash_or_none
  current_product_sha256: exact_hash_or_none
  change_class:
    - unchanged_upstream_file
    - P12_2_compliance_modification
    - AGENT_PLATFORM_product_modification
    - AGENT_PLATFORM_product_addition
    - AGENT_PLATFORM_product_deletion
    - product_owned_control_file
    - generated_local_state
  owner_ticket: exact_ticket
  reapplication_required: true_or_false
  conflict_owner: exact_owner
  validation_obligations: exact_lane_ids
```

Classification authority order:

1. `SOURCE_IMPORT_MANIFEST.tsv` maps current upstream-derived paths and the four P12.2 compliance transformations.
2. `SOURCE_EXCLUSIONS.tsv` maps the current exclusion policy result.
3. The five product-owned control files define the current provenance/legal namespace.
4. Main-repository Git objects and history define subsequent byte changes.
5. The future product modification register defines semantic intent for intentional long-lived divergence.
6. Ignored P12.3/P12.4 environments, builds, logs, caches and runtime evidence are generated state and never product delta.

Current post-P12.2 product delta is empty because the product tree object is identical at P12.2 and P12.4.

## Product Modification Register Decision

Selected model: hybrid.

```yaml
HermesProductModificationRegisterDecision:
  byte_authority: main_repository_Git_objects_and_history
  semantic_authority: concise_explicit_register
  future_path: 2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
  create_in_P12_5: false
  creation_trigger: first_intentional_long_lived_P12_6_product_divergence
  P12_2_compliance_metadata_source: SOURCE_IMPORT_MANIFEST.tsv
  generated_state_included: false
```

Git-only derivation is insufficient because it cannot reliably preserve intent, reapplication conditions or conflict ownership after substantial product changes. A full duplicate hash ledger would drift against Git and manifests. The hybrid register therefore records semantic divergence only; Git remains byte truth.

Required future fields:

```text
modification_id
path
change_class
owner_ticket
baseline_upstream_commit
baseline_source_object_or_none
baseline_source_sha256_or_none
current_product_sha256_or_none
intent
reapplication_predicate
conflict_owner
security_or_compatibility_impact
validation_lane_ids
upstream_disposition
rollback_target
retirement_condition
approval_reference
status
```

P12.2 compliance transformations remain in the import manifest and compliance layer rather than being duplicated as ordinary product patches. P12.6 must create the register in the same reviewed change as the first intentional product divergence. The register itself becomes a product-owned control file; a future candidate path collision is a human-required conflict.

## Three-Way Comparison Model

Required symbols:

```text
A = raw current locked upstream commit
B = raw future locked upstream candidate commit
C = current committed AGENT PLATFORM product at exact synchronization-start commit
FA = FilteredCompliance(A), the accepted P12.2 filtered/compliance base
FB = FilteredCompliance(B), reconstructed for the candidate
P = ProductDelta = diff(FA, C)
D = human-resolved product snapshot produced from FB plus P
```

Conceptual operations:

```text
UpstreamDelta = diff(A, B)
ProductDelta = diff(FA, C)
NewBase = FB
CandidateProduct = resolve(NewBase, ProductDelta) = D
```

The current initial `FA` is the product subtree at P12.2 commit `e3455d9...`; current `C` at P12.4 commit `a7328ac...` has the same tree object, so `P` is empty now. Later P12.6/P13 changes make `P` non-empty.

Per-path mechanical rule, after exclusions and protected-control rules:

| Condition | Proposed D result |
| --- | --- |
| `C == FA` | Take `FB`, including candidate deletion |
| `FB == FA` | Preserve `C`, including product deletion/addition |
| `C == FB` | Take the shared result |
| Otherwise | Conflict; no automatic result |

Equality includes presence, mode and bytes. Rename detection is advisory only; the authoritative model treats rename as delete/add until a human maps logical continuity. Exclusion policy overrides ordinary preservation: restricted content cannot survive because it was locally added or registered.

## Filtered Candidate Reconstruction

Future reconstruction sequence:

1. Verify the complete candidate identity contract.
2. Enumerate the exact candidate commit with `git ls-tree -r -z --full-tree`.
3. Validate object type, mode and normalized path for every entry.
4. Stop on absolute paths, `..`, NUL, unsafe Windows names, trailing dots/spaces, path escapes, case-insensitive collisions, Unicode-normalization collisions or file/directory collisions.
5. Accept ordinary blobs with modes `100644` and `100755`; separately stop/review symlinks, gitlinks, LFS pointers, custom filters, unexpected modes or nested-repository assumptions.
6. Read exact blob bytes with `git cat-file --batch`; do not copy candidate worktree bytes.
7. Inventory every license, NOTICE, dependency, executable, workflow, install hook, provider, OAuth, MCP, browser, updater and external-download surface before build/install.
8. Apply the revalidated exclusion policy to the complete tree, not only changed paths.
9. Materialize permitted blobs into `candidate-tree/` and `filtered-candidate/` under the ignored synchronization workspace.
10. Generate provisional candidate import/exclusion manifests with object IDs and SHA-256 hashes.
11. Apply candidate-specific compliance transformations only after exact predicates pass.
12. Regenerate the five legal/provenance control files for candidate identity and policy results.
13. Re-derive the minimal product-local tracking-compatibility block.
14. Validate the exact candidate product path set, modes, hashes, containment, normal-directory posture and expected trackability.
15. Compare `FA`, `FB` and `C`; classify every path and conflict.
16. Construct `D` only from approved mechanical rules and recorded human resolutions.
17. Produce a proposed exact diff, manifest, conflict inventory, rollback journal plan and plan digest.

The product root remains unchanged throughout reconstruction and dry run.

## Exclusion Revalidation

Every candidate re-evaluates the complete source tree. Counts `56`, `50`, `2`, `4` and `39` are current evidence, never future invariants.

Mandatory review includes:

```text
skills/productivity/powerpoint/**
generated complete-skill pages in every locale/path
skills/index-cache/** and relocated generated indexes
catalog/sidebar/plugin registrations
new bundled and optional skills
all new/changed/removed LICENSE, NOTICE and copyright files
new restricted, source-available, noncommercial or service-linked terms
generated copies or semantic reproductions of excluded content
renamed/moved restricted material
```

Required outcome classes:

```text
unchanged_exclusion
path_moved
path_renamed
content_materially_changed
new_restricted_subtree
upstream_removed_restricted_material
restriction_removed_with_separate_legal_evidence
unknown_requires_human_legal_review
```

The current restrictive policy remains active until a separate human/legal record changes it. A changed license text alone does not clear previously restricted content. If upstream removes the subtree, the transformation retires only after relocated/generated copies and active registrations are proven absent. Unknown classification aborts synchronization.

## License and Notice Refresh

Every accepted candidate must atomically refresh in `D`:

```text
NOTICE
THIRD_PARTY_NOTICES.md
UPSTREAM_PROVENANCE.md
SOURCE_IMPORT_MANIFEST.tsv
SOURCE_EXCLUSIONS.tsv
```

Refresh requirements:

- record exact new repository/release/tag/commit/tree/candidate path identity;
- record complete candidate import and exclusion sets with new hashes;
- record all candidate-specific compliance transformations;
- classify every added, changed, moved or removed license/NOTICE surface;
- preserve top-level MIT and applicable nested MIT/Apache-2.0 license/NOTICE obligations;
- assess Apache modification-notice obligations when relevant content changes;
- retain whole-tree-not-uniformly-MIT language and unresolved SBOM/asset/trademark/release blockers;
- reject stale control files that still identify `9de9c25...` after candidate integration;
- stop if upstream introduces a path colliding with a product-owned control file until namespace and ownership are resolved.

The helper may generate evidence but cannot make a legal determination. Candidate source acceptance does not authorize redistribution, publication, hosted production, binary release or trademark use.

## Compliance Modification Reapplication

Current known transformations:

| Path | Candidate rule |
| --- | --- |
| `website/docs/reference/skills-catalog.md` | Remove only one exact logical restricted PowerPoint registration when the restriction remains active and the match is unambiguous |
| `website/i18n/zh-Hans/docusaurus-plugin-content-docs/current/reference/skills-catalog.md` | Apply the same exact predicate for the Chinese registration |
| `website/sidebars.ts` | Remove only the exact logical `productivity-powerpoint` registration when present once |
| `.gitignore` compatibility block | Re-derive from the candidate; never replay the historical 39-path block blindly |

For each textual transformation:

```text
target absent and registration absent -> no patch, record retired_or_not_applicable
multiple or structurally changed matches -> human compliance conflict and stop
generic PowerPoint/PPTX references -> do not broadly delete
```

Each applied transformation records preimage object/hash, exact predicate, postimage hash and rationale in the candidate import manifest. Compliance transformations are not ordinary AGENT PLATFORM feature patches.

## Tracking Compatibility Strategy

The tracked product-local `.gitignore` remains the reproducible compatibility location. `.git/info/exclude` is invalid because it is local, untracked, absent in CI/other developer clones and the product has no nested `.git`.

Future derivation:

1. Remove the prior delimited compatibility block from the candidate `.gitignore` derivation input.
2. Evaluate every permitted candidate tracked path against candidate ignore rules and effective main-repository product rules.
3. Derive the exact set hidden despite being expected tracked product source.
4. Generate one minimal delimited block with exact directory traversal and file negations.
5. Remove obsolete exceptions and add only newly required exact exceptions.
6. Remove the block entirely if no path requires it.
7. Validate NUL-safe paths and require zero ignored expected product paths.
8. Prohibit broad unignore rules, `.git/info/exclude`, force-add and manual hidden-path exceptions.

The historical 39 hidden files and 52 directory/file negation lines are comparison evidence only. Candidate structure determines the new result.

## Conflict Classification

```yaml
HermesSynchronizationConflict:
  path: exact_normalized_path
  baseline_FA_identity: exact_presence_mode_hash
  candidate_FB_identity: exact_presence_mode_hash
  product_C_identity: exact_presence_mode_hash
  class:
    - upstream_modified_product_unchanged
    - upstream_unchanged_product_modified
    - upstream_and_product_both_modified
    - upstream_deleted_product_modified
    - upstream_renamed_product_modified
    - differing_add_add
    - product_owned_control_collision
    - unregistered_product_drift
    - compliance_exclusion_conflict
    - license_notice_conflict
    - lockfile_or_dependency_conflict
    - generated_path_conflict
    - platform_specific_conflict
    - security_boundary_conflict
    - unknown
  resolution_owner:
    - automatic_safe_rule
    - product_owner
    - compliance_owner
    - security_owner
    - architecture_owner
    - human_required
  automatic_resolution_allowed: true_or_false
  resolution_identity: exact_mode_and_hash_or_none
  rationale: exact_record
  approval_reference: exact_human_gate_or_none
```

Unregistered product drift and control-file collision are stop conditions, not changes to preserve automatically. Dual-sided changes, deletes/renames involving product work, license/NOTICE changes, dependency migrations and architecture/security changes default to human resolution.

## Automatic and Human Resolution Boundaries

Narrow deterministic cases may be proposed automatically:

| Case | Mechanical proposal |
| --- | --- |
| Candidate adds permitted file with no product collision | Add candidate blob/mode |
| Candidate modifies file unchanged by product | Take candidate blob/mode |
| Candidate deletes file unchanged by product | Delete path |
| Product modifies/adds/deletes while candidate equals `FA` | Preserve registered product result |
| Product and candidate converge to identical result | Take common result and consider retiring local patch |
| Exact compliance predicate has one match | Apply exact transformation |
| Manifests/notices | Regenerate from approved identities and decisions |
| Tracking compatibility | Derive minimal exact block |

Every mechanical proposal still appears in the dry-run report and requires human approval before product modification.

Human review is mandatory for:

```text
same logical path modified upstream and by AGENT PLATFORM
upstream deletion/rename of product-modified path
new or changed license/NOTICE/restricted content
product-owned control-path collision
dependency manager, package root or lockfile migration
provider/authentication/OAuth/MCP/network model change
runtime, dashboard/backend entrypoint, schema or API change
security boundary, updater or external-download change
unknown/unregistered product drift
any semantic content merge or rename mapping
```

No helper may select a semantic merge. A human resolution becomes deterministic only after exact output presence/mode/hash, owner, rationale and approval are recorded and the plan digest is recomputed.

## Temporary Synchronization Workspace

```text
9_artifacts/hermes/synchronization/<candidate-full-sha>/
  candidate-tree/
  filtered-candidate/
  resolved-product-D/
  comparison/
  conflicts/
  reports/
  manifests/
  logs/
  rollback/
  transaction/
```

Requirements:

```yaml
HermesSynchronizationWorkspace:
  inside_AGENT_PLATFORM: true
  ignored: true
  unstaged: true
  normal_directory: true
  reparse_root: false
  nested_git: false
  credentials: false
  personal_hermes_state: false
  product_overwrite_during_dry_run: false
  source_of_bytes: verified_Git_objects
```

The candidate Git repository belongs under `4_external/sources`, not inside this workspace. The workspace contains projections/evidence only. It must stop on unexplained paths, reparse points, unsafe links or collisions. Aborted work removes only exact owned temporary paths after containment proof; the current product and main index remain unchanged.

## Replacement Strategy

Selected model: manifest-driven exact-set replacement of resolved snapshot `D`, implemented as a journaled per-path transaction. "Transactional" means complete preimages, an ordered apply journal, post-write verification and an exact inverse operation; it does not claim an atomic whole-directory swap on Windows/OneDrive.

Future authorized sequence:

1. Require exact synchronization-start main commit, clean product and empty index.
2. Quiesce Hermes processes, tests, editors and package managers affecting the product.
3. Record exact current tracked product path/mode/blob/hash set and product tree object.
4. Classify all ignored/generated roots and stop on unexplained product-local state.
5. Construct and validate complete `D` under the ignored workspace.
6. Record exact `D` path/mode/hash set, conflict resolutions and plan digest.
7. Run candidate validation in isolation where authorized before touching the product.
8. Obtain all pre-application human approvals.
9. Capture exact preimage bytes/modes for every product path changed or deleted.
10. Prepare same-directory temporary files for changed/additional paths; verify bytes before rename.
11. Move exact deleted paths into transaction quarantine; do not delete unknown paths.
12. Replace only exact planned tracked paths and preserve unaffected tracked paths.
13. Re-enumerate product paths/modes/hashes after OneDrive settles and require exact equality with `D`.
14. Revalidate legal/provenance manifests, trackability, no nested Git/reparse paths and empty index.
15. Invalidate and later recreate only exact approved generated environments when authoritative lockfiles changed; never assume old `.venv`/`node_modules` remain valid.
16. Run the separately authorized post-application baseline comparison.
17. Human stages only exact synchronization paths and reviews staged modes/blobs/deletions.
18. Human commits, reviews, merges and pushes under the selected main-repository workflow.
19. Retain rollback evidence until acceptance; clean only exact owned temporary state afterward.

Rejected models:

| Model | Decision | Reason |
| --- | --- | --- |
| In-place unjournaled patching | Reject | Partial state and ambiguous rollback on failure |
| Whole-directory swap | Reject | Open handles, OneDrive rename behavior and approved ignored environments make root swap unsafe |
| Blind candidate mirror | Reject | Would lose product divergence and product-owned control files |
| Git merge/rebase in product | Reject | Product has no independent history or upstream remote |
| Journaled manifest exact set | Select | Explicit ownership, reviewable Git diff and exact inverse rollback |

## Baseline Regression Comparison

Every candidate compares against committed P12.4 `a7328ac...` using the same authorized environment and command identities where possible.

Current green anchors:

```text
uv lock and frozen environment checks
Ruff
Windows-footgun scanner
npm dependency integrity exit 0
five TypeScript package checks
Hermes Ink build
TUI build
desktop frontend build
provider-null localhost dashboard readiness and UI shell
source/lock drift absence
```

Current known non-green anchors:

```text
Ty: 10889 diagnostics and incomplete-analysis warning
Python representative tests: 5535 passed, 198 failed, 41 skipped
dashboard lint: 28 errors, 3 warnings
TUI lint: 1 error, 14 warnings
TUI tests: 756 passed, 3 failed, 5 skipped, 32 import-failed suites
desktop renderer tests: 1148 passed, 27 failed
desktop platform tests: 300 passed, 9 failed
Windows dashboard graceful shutdown: failed; exact-tree fallback required
```

Each future lane result is classified as:

```text
improved
unchanged
regressed
newly_applicable
removed
not_comparable
```

A previously green lane becoming non-green is a default rejection. Historic non-green counts are not an allowlist for new failures. Compare normalized test IDs and diagnostic fingerprints when retained; because P12.4 durable evidence does not contain every failure fingerprint, rerun the accepted baseline and candidate side-by-side under the same authorized environment before claiming no regression where exact identity is unavailable. New failures require exact ownership and human acceptance. Legitimate source updates need not reproduce historical build artifact hashes.

Website, WhatsApp, Photon, Rust/Tauri packaging, Nix, containers, provider integrations and Electron application launch remain outside the accepted baseline unless separately activated. Desktop Git-fixture tests must use temporary repositories outside every parent Git worktree.

Candidate verdicts:

```text
candidate_rejected_identity_or_compliance
candidate_rejected_regression
candidate_ready_with_known_regressions
candidate_ready_for_human_merge
candidate_integrated_and_validated
```

Only a human can authorize `candidate_integrated_and_validated`.

## Versioning Policy

Selected model: dual version.

```yaml
HermesProductVersioning:
  upstream_version: preserved_exactly
  upstream_commit: preserved_exactly
  upstream_tag: preserved_exactly_or_none
  AGENT_PLATFORM_product_version: independent
  display_policy: show_both_where_relevant
  synchronization_updates_product_version_automatically: false
  implementation_in_P12_5: false
```

Example display:

```text
Hermes upstream: 0.18.2 @ 9de9c25
AGENT PLATFORM Hermes product: 0.1.0-dev
```

P12.6 or a separately authorized versioning ticket establishes the first independent product version and exact metadata/display surfaces. Upstream package metadata is not silently rewritten during synchronization, and product version changes require their own product-modification/register entry.

## Git Workflow

The product always remains a normal subtree of the AGENT PLATFORM main repository.

Allowed future workflow:

```text
human-approved short-lived main-repository synchronization branch from exact C
no product-local branch
no nested .git
no product remote
no upstream remote attached to product root
no independent product history
no long-lived synchronization branch
```

If main advances after the dry-run start commit, do not rebase or merge automatically. Abort the plan and recompute `C`, `ProductDelta`, conflicts, `D` and the plan digest from the new exact start commit.

Recommended commit sequence for a substantial update:

```text
Commit 1: human-approved candidate identity and synchronization plan
Commit 2: filtered candidate exact-set import plus refreshed provenance/legal manifests
Commit 3+: explicit human conflict resolutions and registered product reapplications
Commit final: baseline comparison and synchronization closure
```

A single atomic commit is permitted only when the diff is manageable, conflicts are absent, legal/provenance refresh is complete, validation evidence is complete and a human approves that granularity.

Future staging includes only exact planned `2_products/hermes-agent/**` paths, exact synchronization governance records and an authorized modification register. It excludes `4_external/sources/**`, `9_artifacts/**`, candidate checkout, runtime/build/log/screenshot output, `.opencode/**`, `AGENTS.md` and `graphify-out/**`. `git add .`, `git add -A` and `git add -f` are always prohibited.

## Human Approval Gates

```yaml
HermesSynchronizationApprovalGates:
  gate_1_candidate_acquisition:
    human_required: true
    approves: exact_network_commands_candidate_path_and_cleanup_owner
  gate_2_candidate_identity_acceptance:
    human_required: true
    approves: repository_commit_tree_tag_signature_and_history_posture
  gate_3_exclusion_and_license_policy:
    human_required: true
    approves: complete_filter_legal_notice_and_control_file_plan
  gate_4_conflict_resolution_plan:
    human_required: true
    approves: every_nonmechanical_resolution_and_D_identity
  gate_5_candidate_product_diff:
    human_required: true
    approves: exact_path_mode_hash_plan_and_transaction_digest
  gate_6_baseline_regression_acceptance:
    human_required: true
    approves: green_lane_preservation_and_every_new_or_changed_failure
  gate_7_product_application_and_git_staging:
    human_required: true
    approves: source_mutation_then_exact_staged_paths_modes_blobs_and_deletions
  gate_8_commit_merge_and_push:
    human_required: true
    approves: commits_merge_push_reference_promotion_and_cleanup
```

No helper, CI job, package script or agent may bypass or infer approval. Gates are sequential; later approval does not retroactively authorize an earlier omitted gate.

## Rollback Strategy

Before application, capture:

```text
exact main synchronization-start commit
current product tree object
current tracked path/mode/blob/SHA-256 inventory
current five control files and manifests
candidate identity and candidate product manifest
resolved D manifest and plan digest
all conflict decisions and approvals
exact changed/deleted path preimages
ordered apply and inverse journal
```

Rollback states:

| State | Exact response |
| --- | --- |
| Before product application | Remove only exact temporary owned state; product/index remain unchanged |
| During application | Stop processes, replay inverse journal, restore exact preimage bytes/modes, verify original tree inventory |
| After application before staging | Replay inverse journal and verify start-commit product tree; index remains empty |
| After staging before commit | Human unstages only exact synchronization paths, then inverse journal restores preimages |
| On short-lived branch before merge | Human abandons/reverts branch changes; main remains unchanged |
| After merge/push | New explicit human-reviewed revert commit; preserve shared history |

Rollback must never use broad reset, clean, wildcard deletion, parent-directory deletion, history rewrite or automatic force push. Unknown/unowned files stop rollback for human review rather than being removed.

## Abort Rules

Abort before product mutation when:

```text
candidate identity, tree, reachability or official origin cannot be proven
candidate path or workspace escapes approved roots
candidate tree contains unsafe paths/types/modes/collisions
current product/index/reference baseline is dirty or changed
P12.2 manifests/control hashes cannot reconstruct FA
product divergence is unregistered or cannot be classified
restricted content or generated copies cannot be conclusively excluded
license/NOTICE classification or refresh is incomplete
compliance transformation predicate is ambiguous
candidate collides with a product-owned control path
expected candidate product path remains ignored or requires force-add
dual-sided conflict lacks exact human resolution
dependency/security hotspot lacks a separate approval gate
lockfile is regenerated merely to resolve a conflict
previously green baseline lane regresses without explicit acceptance
provider credentials, OAuth or uncontrolled external service become required
candidate introduces nested Git/submodule assumptions into the product
exact rollback set, preimages or inverse journal cannot be proven
main advances after the plan start commit
an additional durable Markdown or scope expansion appears necessary
```

An abort leaves the current product, main index, locked reference and history unchanged; stops any owned process; removes only exact temporary owned state after containment checks; and records the blocker in the same future synchronization record. No retry/safe-block Markdown is created automatically.

## Automation Helper Decision

Decision: implement a versioned offline helper later, but not in P12.5.

Suggested future ticket:

```text
P12.5.1 - Hermes Synchronization Planner and Dry-Run Tool
```

Permitted helper scope:

```text
read already-acquired local Git objects and committed main-repository trees
validate paths/types/modes/collisions
apply approved exclusion predicates
generate deterministic FA/FB/C/D inventories and manifests
classify mechanical conflicts
materialize filtered/resolved candidate projections
produce exact review reports, fingerprints and plan digests
prepare per-path transaction preimages and inverse journal
verify or roll back only an explicitly authorized transaction
```

Prohibited helper scope:

```text
network access or candidate acquisition
legal or semantic conflict decisions
product mutation without gate 7
branch/worktree/remote/tag/index creation
staging, commit, merge, rebase, push or publication
dependency installation or lock regeneration
build, test, provider, OAuth, MCP, worker or runtime activation
```

The helper must be committed and reviewed outside both Hermes source roots before first use, and its exact version/hash must be part of every plan digest.

## Dry-Run Requirement

Every real candidate integration requires an offline main-repository dry run after candidate acquisition and identity acceptance.

Dry run must:

```text
consume exact A, B and C identities
construct complete FA and FB from Git objects and policy
generate provisional legal/provenance manifests
derive ProductDelta and the modification-register obligations
classify every conflict
construct proposed D without touching the product
derive tracking compatibility
produce exact proposed add/modify/delete/mode inventory
produce preimage/rollback requirements and transaction plan
estimate dependency/security and P12.4 baseline impact
record helper/policy/input/output hashes and plan digest
leave product, index, history and locked current reference unchanged
```

Required dry-run verdict:

```text
dry_run_ready_for_human_review
```

A separate execution gate is required after dry-run approval. Dry-run filesystem writes are limited to the approved ignored synchronization workspace; "dry run" means no main product/index/history mutation, not zero temporary evidence.

## Security and Dependency Gates

Before any candidate installation, build, test or runtime, statically compare and classify:

```text
pyproject.toml and uv.lock
root and workspace package.json/package-lock.json files
new package roots, registries, Git dependencies and lockfile formats
setup/build/bootstrap/update/release/package lifecycle scripts
npm postinstall and native dependency behavior
Cargo, Nix and container declarations
GitHub workflows and third-party actions
provider/model integrations and external endpoints
credential/.env/auth/OAuth changes
MCP servers and worker/dispatcher behavior
browser automation, telemetry and self-update behavior
state schemas, migrations, persistence and listeners
new executable modes, binaries, fonts, images, templates and media
```

Dependency changes require acceptance before package-manager execution. No lockfile regeneration is allowed merely to resolve a merge/conflict. If authoritative locks change, P12.3 `.venv` and `node_modules` become stale evidence; a separately authorized clean frozen environment must be created without trusting or mutating old generated state.

Candidate UI/runtime comparison must explicitly inspect `web/src/main.tsx`, `hermes_cli/web_server.py`, dashboard routes, TUI entrypoints, desktop renderer entrypoints, provider-null startup and shutdown behavior. No provider credential, model request, OAuth, MCP, external worker or production service is authorized by synchronization.

## P12.6 Handoff

P12.6 may proceed after human acceptance of this record.

P12.6 must consume:

```text
filtered snapshot plus three-way reapplication model
FA/FB/C/D identity and conflict rules
hybrid product modification register decision
candidate-specific compliance predicates
tracking compatibility re-derivation
dual version policy
synchronization-sensitive source/control paths
P12.4 regression comparison contract
human approval and exact rollback boundaries
```

P12.6 changes should use extension/configuration seams and avoid unnecessary edits to high-conflict upstream files. The first intentional long-lived product divergence must create and populate `AGENT_PLATFORM_MODIFICATIONS.tsv` in the same reviewed commit. Every modification must identify reapplication/retirement conditions and affected validation lanes.

```text
hermes_P12_6_ready
```

## P13 Handoff

P13 UI work must register:

```text
every modified upstream UI path
route/component ownership
branding-only versus behavioral change
backend/API/schema dependencies
extension-seam location
reapplication predicate
upstream contribution/retirement posture
targeted build/test/UI lanes
```

The current browser-dashboard baseline is `web` plus `hermes_cli.web_server`, with `/sessions` human-observed in P12.4. Dashboard, TUI and desktop files are synchronization-sensitive. P13 should isolate AGENT PLATFORM behavior behind explicit components/configuration seams where practical so future upstream UI changes can be compared and reapplied without broad dual-sided conflicts.

## Created / Modified / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_hermes_upstream_synchronization_strategy.md
```

Modified:

```text
none
```

Not created, modified or executed:

```text
4_external/sources/hermes-agent-candidate
candidate Git objects or checkout
9_artifacts/hermes/synchronization
candidate/filtered/resolved product trees
candidate reports, manifests or provenance files
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
synchronization helper
2_products/hermes-agent/**
4_external/sources/hermes-agent/**
root or product-local .gitignore
P12.2, P12.3 or P12.4 records
dependency manifests or lockfiles
branch, remote, worktree, submodule or nested .git
fetch, pull, merge, rebase, cherry-pick or checkout
staging, commit or push
provider, OAuth, MCP, worker, test, build or runtime process
additional durable Markdown
```

## Limitations

- No future candidate was selected, acquired, inspected, filtered, compared, built, tested or integrated; this record defines strategy only.
- Candidate origin reachability, ancestry, tag/signature and object completeness remain future candidate-specific evidence.
- The current immutable reference remains the P12.2 anchor; reference promotion/rotation requires a separate exact approval after integration.
- P12.2 counts `56` exclusions and `39` initially ignored files cannot be reused as candidate expectations.
- The current import manifest is initial-source authority, not a complete semantic register for future product divergence.
- No modification register exists yet because post-P12.2 product delta is empty; P12.6 must create it with the first divergence.
- P12.4 durable evidence records failure counts but not every normalized failure fingerprint; side-by-side rerun is required where exact regression identity is unavailable.
- Windows/OneDrive makes whole-root atomic swap unreliable; the selected transaction is exact-set, journaled and per-path.
- Existing ignored `.venv`, `node_modules`, workspace junctions and build/runtime outputs require explicit generated-state handling during future replacement.
- Candidate dependency changes may invalidate P12.3 environments and require a separate clean frozen setup gate.
- Legal/SBOM/asset/trademark/publication/redistribution blockers remain open regardless of successful source synchronization.
- Independent product version metadata and display are selected conceptually but not implemented.
- The offline synchronization helper and dry-run report format remain future implementation work.

## Final Verdict

```yaml
P12_5_UpstreamSynchronizationStrategyVerdict:
  p12_4_baseline_committed: true
  current_baseline_identity_resolved: true
  synchronization_mode: filtered_snapshot_three_way_reapplication
  candidate_identity_contract_defined: true
  candidate_acquisition_human_gated: true
  product_change_classification_defined: true
  product_modification_register_model_selected: true
  three_way_comparison_defined: true
  exclusion_revalidation_required: true
  license_notice_refresh_required: true
  tracking_compatibility_rederived: true
  conflict_classification_defined: true
  semantic_auto_merge_prohibited: true
  exact_set_replacement_selected: true
  baseline_regression_comparison_required: true
  rollback_defined: true
  dry_run_required: true
  product_nested_git_required: false
  product_remote_required: false
  network_operation_performed: false
  source_modified: false
  git_mutated_by_agent: false
  P12_6_may_proceed: true
  final_verdict: upstream_synchronization_strategy_ready
```

Required result markers:

```text
hermes_upstream_synchronization_strategy_ready
hermes_upstream_candidate_identity_contract_defined
hermes_synchronization_preflight_defined
hermes_filtered_snapshot_reconstruction_defined
hermes_three_way_comparison_model_defined
hermes_product_patch_reapplication_defined
hermes_license_exclusion_revalidation_defined
hermes_notice_provenance_refresh_defined
hermes_conflict_classification_defined
hermes_baseline_regression_comparison_defined
hermes_synchronization_rollback_defined
hermes_human_approval_gates_defined
hermes_no_product_remote_required
hermes_no_nested_git_required
hermes_P12_6_ready
no_upstream_sync_executed
no_network_operation
no_source_modification
no_git_mutation_by_agent
```

## Human Commit Boundary

The agent did not stage, commit or push. The intended human commit contains only this canonical record:

```powershell
$ErrorActionPreference = "Stop"

$Record = "0_architecture/governance/agent_platform_hermes_upstream_synchronization_strategy.md"

if (-not (Test-Path -LiteralPath $Record -PathType Leaf)) {
    throw "Missing P12.5 record: $Record"
}

$ProductDrift = @(git status --short -- "2_products/hermes-agent")
if ($ProductDrift.Count -ne 0) {
    throw "Unexpected Hermes drift: $($ProductDrift -join ', ')"
}

$StagedBefore = @(git diff --cached --name-only)
if ($StagedBefore.Count -ne 0) {
    throw "Paths already staged: $($StagedBefore -join ', ')"
}

git status --short
git add -- $Record

$Staged = @(
    git diff --cached --name-only |
        ForEach-Object { $_.Replace("\", "/") } |
        Sort-Object -Unique
)

if ($Staged.Count -ne 1 -or $Staged[0] -ne $Record) {
    throw "Unexpected staging: $($Staged -join ', ')"
}

git diff --cached --check
if ($LASTEXITCODE -ne 0) {
    throw "git diff --cached --check failed"
}

git diff --cached --stat
git commit -m "P12.5 - Define Hermes upstream synchronization strategy"
git push origin main
```

Never use `git add .`, `git add -A` or `git add -f`.
