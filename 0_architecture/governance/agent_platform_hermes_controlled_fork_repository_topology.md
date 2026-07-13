# P12.1 - Hermes Controlled Fork and Repository Topology

## Document Header

| Field | Value |
| --- | --- |
| Project | P12 - Hermes Productization Foundation |
| Ticket | P12.1 - Controlled Fork and Repository Topology |
| Type | Repository topology implementation |
| Execution class | Bounded directory creation and validation |
| Status | Corrected topology ready for human acceptance |
| Canonical record | `0_architecture/governance/agent_platform_hermes_controlled_fork_repository_topology.md` |
| Authorized workspace | `C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM` |
| Product root | `2_products/hermes-agent` |
| Repository mode | `main_repository_normal_subtree` |
| Source import owner | P12.2 |

This record is the current P12.1 authority. The historical sibling-repository evidence retained in the final appendix is non-operative and cannot authorize a product root, nested Git repository, product branch, product remote or independent history.

## Purpose

Correct P12.1 in place by creating only the empty internal Hermes product root as a normal subtree of the existing AGENT PLATFORM repository. This execution consumes P12.C1, P12.C2 and P12.C3, preserves the immutable upstream reference, creates no product file or Git metadata, and hands the first controlled source import to P12.2.

The term `controlled fork` means an editable, provenance-controlled Hermes-derived product subtree inside AGENT PLATFORM. It does not mean a GitHub fork, separate repository, nested repository, separate branch history or sibling workspace.

## Correction History

| Record | Current effect |
| --- | --- |
| Historical P12.1 | Created an invalid external sibling repository at `C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES`; this topology is invalid and superseded. |
| P12.C1 | Proved ownership, removed the invalid material result, reopened P12.1/P12.2 and preserved the locked upstream. |
| P12.C2 | Classified Hermes as `hybrid_product_with_platform_adapters` and selected only `2_products/hermes-agent`. |
| P12.C3 | Replaced the whole-class product ignore with a fail-closed Hermes-only tracking exception. |
| Corrected P12.1 | Created the selected empty internal product root without nested Git, product branch, product remote, independent history or source import. |

## P12.C1 Status

```yaml
P12_C1_Status:
  invalid_external_root: C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES
  invalid_external_root_exists: false
  historical_material_result_removed: true
  P12_1_reopened: true
  P12_2_reopened: true
  locked_upstream_unchanged: true
  P11_2_affected: false
```

The invalid external root was absent before and after corrected execution.

## P12.C2 Topology Decision

```yaml
HermesPlacement:
  classification: hybrid_product_with_platform_adapters
  product_root: 2_products/hermes-agent
  product_root_inside_agent_platform: true
  product_is_main_repo_subtree: true
  nested_git_repository: false
  separate_product_remote: false
  alternative_candidate_authorized: false
```

## P12.C3 Tracking Policy Status

Current fail-closed policy:

```gitignore
/2_products/*
!/2_products/hermes-agent
!/2_products/hermes-agent/**
```

```yaml
P12_C3_Status:
  current_ignore_conflict_resolved: true
  product_class_default_ignore_retained: true
  hermes_tracking_exception_active: true
  hermes_root_check_ignore_exit: 1
  hermes_descendant_check_ignore_exit: 1
  force_add_required: false
  sibling_products_remain_ignored: true
  product_paths_staged: false
  gitignore_sha256: E1A7238DB58ABFA93DA762EC87801DF8B74877CC573608ED0F83E55EC352C40A
```

The `.gitignore` file was not modified by corrected P12.1.

## Locked Upstream Identity

```yaml
HermesLockedUpstreamReference:
  path: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\4_external\sources\hermes-agent
  repository: https://github.com/NousResearch/hermes-agent
  observed_origin: https://github.com/nousresearch/hermes-agent.git
  normalized_origin_matches: true
  release: 0.18.2
  tag: v2026.7.7.2
  commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  head_matches: true
  tag_points_at_head: true
  status_clean: true
  posture: immutable_read_only_reference
```

Only read-only Git metadata checks were performed. No fetch, pull, checkout, reset, clean, branch, tag, commit, push, install, build or execution occurred.

## Corrected Product Root

```yaml
HermesProductRoot:
  absolute_path: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\2_products\hermes-agent
  repository_relative_path: 2_products/hermes-agent
  authorized_workspace: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM
  initially_absent: true
  exists_after_execution: true
  exact_path_used: true
```

No alternate path or name was created.

## Path Preflight

| Check | Result |
| --- | --- |
| `git rev-parse --show-toplevel` | `C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM` |
| Selected target is absolute and non-empty | Passed |
| Parent `2_products` exists | Passed |
| Target initially absent | Passed |
| Target contained within AGENT PLATFORM | Passed |
| Target outside locked upstream | Passed |
| Target outside `.opencode`, `graphify-out`, `9_artifacts`, `4_external` and `.git` | Passed |
| AGENT PLATFORM and `2_products` reparse checks | Neither is a reparse point |
| Target ignored | No; exact and descendant checks returned `1` |
| Existing tracked target paths | `0` |
| Existing staged target paths | `0` |

Windows reports the mandated parent `C:\Users\pablo\OneDrive\Escritorio` as a OneDrive-managed reparse point. Execution stopped before writing and the human explicitly approved that parent as authorized infrastructure. The enforced boundary therefore requires AGENT PLATFORM and every component below it to be non-reparse; both AGENT PLATFORM and `2_products` passed before creation, and the created root also passed afterward.

```yaml
HermesPathPreflight:
  workspace_git_root_matches: true
  selected_path_canonicalized: true
  locked_upstream_canonicalized: true
  parent_exists: true
  target_initially_absent: true
  target_inside_workspace: true
  target_inside_locked_upstream: false
  target_overlaps_blocked_root: false
  approved_onedrive_parent_infrastructure: C:\Users\pablo\OneDrive\Escritorio
  workspace_downward_reparse_count_before_creation: 0
  target_ignored: false
  tracked_target_path_count: 0
  staged_target_path_count: 0
  final_result: passed
```

## Corrected Repository Topology

```yaml
HermesProductRepositoryTopology:
  mode: main_repository_normal_subtree
  product_root: 2_products/hermes-agent
  main_git_repository: AGENT PLATFORM
  nested_git: false
  product_branch: none
  product_remote: none
  independent_history: false
  worktree: false
  submodule: false
  subtree_mechanism: false
  source_import_owner: P12.2
```

The historical sibling-repository mode and its product `.git`, branch, remote and independent-history claims are superseded and have no active authority.

## Directory Creation

Exactly one filesystem object was created:

```text
C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\2_products\hermes-agent
```

Creation used `New-Item -ItemType Directory` only after the complete preflight passed. No file, placeholder or child directory was created.

```yaml
HermesEmptyRootValidation:
  root_exists: true
  attributes: Directory
  reparse_point: false
  child_count: 0
  file_count: 0
  child_directory_count: 0
  hidden_child_count: 0
  nested_git_exists: false
```

## Nested Git Validation

`2_products/hermes-agent/.git` does not exist. No `git init`, clone, remote, branch, checkout, worktree, submodule or subtree command was run.

```yaml
HermesNestedGitValidation:
  nested_git_created: false
  product_branch_created: false
  product_remote_created: false
  independent_history_created: false
  worktree_created: false
  submodule_created: false
  subtree_mechanism_created: false
```

## Main-Repository Ownership Validation

Read-only validation from the new directory returned:

```text
C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM
```

The directory is a normal subtree owned by the existing AGENT PLATFORM Git repository. It has no product-specific Git metadata, branch, remote or history.

## Trackability Validation

| Exact path | `git check-ignore -q` exit | Meaning |
| --- | ---: | --- |
| `2_products/hermes-agent` | `1` | Not ignored |
| `2_products/hermes-agent/.tracking-probe` | `1` | Descendants are not ignored |

No `.tracking-probe` was created. Force-add is not required and `git add -f` was not used. The empty directory is intentionally absent from Git status because Git does not track empty directories.

## Sibling Product Protection

Only immediate sibling names were inspected. Contents were not inspected.

| Sibling | Root ignored | Synthetic descendant ignored | Visible in status | Staged | Modified by P12.1 |
| --- | --- | --- | --- | --- | --- |
| `backend-energyplus` | Yes | Yes | No | No | No |
| `cli` | Yes | Yes | No | No | No |
| `desktop` | Yes | Yes | No | No | No |
| `experimental` | Yes | Yes | No | No | No |
| `omniverse-app` | Yes | Yes | No | No | No |
| `web-platform` | Yes | Yes | No | No | No |

All sibling root and synthetic-descendant checks returned exit `0`, meaning ignored. `git status --short -- "2_products"` and `git diff --cached --name-only -- "2_products"` returned no paths.

## Git Boundary

P12.1 did not stage the empty directory and created no `.gitkeep`, placeholder, README or empty-root commit. No `git add`, `git add -A`, `git add -f`, commit or push command was run. Git index and history remain human-controlled.

```text
Never use git add .
```

## Upstream / Product / Adapter / Generated-State Relationship

```yaml
HermesSourceRelationship:
  immutable_upstream:
    path: 4_external/sources/hermes-agent
    editable: false
    tracked_by_main_repo: false
  editable_product:
    path: 2_products/hermes-agent
    editable: true_after_P12_2
    tracked_by_main_repo: true_after_source_import
    nested_git: false
  integration_adapter:
    future_path: 3_platform/_governed_skeleton/integrations/hermes
    created_now: false
  generated_state:
    future_primary_class: 9_artifacts/hermes
    created_now: false
```

The product root contains no copied upstream `.git` metadata and no source content.

## P12.2 Handoff

Corrected P12.1 is ready for human acceptance. After acceptance, P12.2 may import fresh source directly from the immutable upstream and owns restricted-content exclusion, generated complete-skill documentation exclusion, registry/sidebar cleanup, MIT and Apache-2.0 preservation, NOTICE and third-party notices, provenance and exclusion manifests, deterministic source/hash inventory, and the redistributability boundary.

P12.2 must not reuse the deleted external snapshot, create nested Git, create a product branch or remote, or stage/commit/push as the agent. Paths must be recorded relative to AGENT PLATFORM.

```text
hermes_P12_2_reentry_ready
```

## Rollback Procedure

If a later validation proves this P12.1 creation invalid:

1. Confirm the target is exactly `C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\2_products\hermes-agent`.
2. Confirm corrected P12.1 created it.
3. Confirm it remains empty, non-reparse and contains no `.git`.
4. Remove only that exact empty directory with `Remove-Item -LiteralPath <exact-path> -Force`, without `-Recurse`.
5. Revalidate sibling protection, unchanged `.gitignore`, and clean locked upstream.

If the root is not empty, stop for human review. Never use `git clean`, reset, restore, checkout, wildcard deletion or parent-directory deletion.

No rollback was required because all post-creation validation passed.

## Created / Modified / Not Created Register

Created:

```text
C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\2_products\hermes-agent
```

Modified:

```text
0_architecture/governance/agent_platform_hermes_controlled_fork_repository_topology.md
```

Not created or modified by corrected P12.1:

```text
any file inside 2_products/hermes-agent
.gitkeep, README, LICENSE, NOTICE, source file or placeholder
nested .git, product branch, product remote or independent history
worktree, submodule, subtree, symlink, hardlink or reparse point
build output, runtime state, dependency directory or environment
3_platform/_governed_skeleton/integrations/hermes
9_artifacts/hermes
additional Markdown
.gitignore, .graphifyignore, README.md, P12.2 record or P11 records
workspace/product policy records
4_external/sources/hermes-agent/**
.opencode/**, AGENTS.md or graphify-out/**
sibling product contents
```

## Validation and No-Touch Record

Validation used only exact path existence/attribute checks, immediate sibling-name enumeration, `git status`, `git rev-parse`, `git check-ignore`, `git ls-files`, `git diff --cached`, file hashing, canonical document inspection and read-only locked-upstream Git metadata.

No Graphify, source inspection/import, package manager, build, test, Hermes runtime, provider/API/OAuth/MCP, credential inspection, network operation, Git initialization/mutation, staging, commit or push occurred.

## Limitations

- The empty directory cannot be represented in a Git commit; P12.2 will make the subtree visible when it creates the first authorized files.
- Immediate sibling names and ignore/status metadata were checked; sibling contents were intentionally not inspected.
- The OneDrive-managed `Escritorio` parent is an explicitly human-approved infrastructure reparse point; the workspace and all components below it remain subject to the no-reparse requirement.
- P12.2 may reenter only after human acceptance of corrected P12.1.
- Later source, environment, build, synchronization and product-extension work remains outside P12.1.

## Final Verdict

```yaml
P12_1_CorrectedTopologyVerdict:
  historical_external_topology_valid: false
  historical_external_root_removed: true
  authorized_workspace_root: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM
  product_root: 2_products/hermes-agent
  product_root_created: true
  product_root_empty: true
  product_root_trackable_without_force_add: true
  product_is_main_repository_subtree: true
  nested_git_created: false
  product_branch_created: false
  product_remote_created: false
  independent_history_created: false
  source_import_performed: false
  sibling_products_remain_ignored: true
  locked_upstream_unchanged: true
  P12_2_may_reenter: true
  final_topology_verdict: ready_for_corrected_P12_2_source_import
```

```text
hermes_controlled_product_topology_ready
hermes_internal_product_root_created
hermes_product_root_is_main_repository_subtree
hermes_product_root_trackable_without_force_add
hermes_nested_git_not_created
hermes_product_remote_not_created
hermes_product_branch_not_created
hermes_source_import_deferred_to_P12_2
hermes_locked_upstream_reference_unchanged
hermes_P12_2_reentry_ready
no_external_product_root
no_source_copy_created
no_install_build_test_run
no_runtime_execution
no_agent_git_mutation
```

## Human Commit Commands

The empty directory cannot and must not be staged. After reviewing this corrected record, the human may run:

```powershell
git status --short
git add -- "0_architecture/governance/agent_platform_hermes_controlled_fork_repository_topology.md"
git commit -m "P12.1 - Correct Hermes product repository topology"
git push origin main
```

Never use `git add .`.

## Historical Correction Summary

- An earlier P12.1 execution created the unauthorized sibling root `C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES`.
- P12.C1 proved ownership and removed that root.
- P12.C2 selected `2_products/hermes-agent` as the authorized product root.
- P12.C3 enabled the exact fail-closed tracking exception for `2_products/hermes-agent`.
- All old sibling-repository commands, branches, remotes, history and readiness claims are superseded and non-authoritative.
- Detailed incident evidence is available in `0_architecture/governance/agent_platform_hermes_misplaced_product_root_rollback.md`, the P12.C1 canonical record.
