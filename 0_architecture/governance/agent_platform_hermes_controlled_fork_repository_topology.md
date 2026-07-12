# P12.1 - Hermes Controlled Fork and Repository Topology

## 0. Contexto obligatorio

P12 is **Hermes Productization Foundation**. P12.1 is the controlled product repository topology ticket and depends on accepted P12.0 substantive content.

P12.0 intentionally delegates the exact product-root, repository-mode, remote-policy and branch-policy decisions to P12.1. P12.1 owns those decisions under the P12.0 productization boundary; P12.0 was not required to predefine them.

P12.1 establishes an empty sibling Git repository at `C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES`. It preserves the P11.0-locked upstream source at `4_external/sources/hermes-agent` as an immutable read-only reference and imports no Hermes source. P12.2 owns the first controlled snapshot import, restrictive-subtree exclusion, notice baseline and provenance inventory.

P12.1 does not install, build, test or execute Hermes. It does not perform license exclusion, create product files, contact a remote, stage, commit, push, use `git add .`, touch `.opencode/` or `AGENTS.md`, modify P11/P12.0, or create additional Markdown.

Post-cleanup resolution uses current substantive canonical content rather than obsolete filename identity.

Document model:

```text
HermesControlledForkRepositoryTopology
HermesProductTopologyRecord
```

Result markers:

```text
hermes_controlled_fork_repository_topology_ready
hermes_product_root_created
hermes_product_repository_initialized
hermes_product_main_branch_initialized
hermes_upstream_remote_configured_without_network
hermes_origin_remote_deferred
hermes_source_snapshot_import_deferred_to_P12_2
hermes_locked_upstream_reference_unchanged
hermes_P12_2_ready
no_source_copy_created
no_product_commit_created
no_remote_network_operation
no_install_build_test_run
no_agent_platform_git_mutation
```

## 1. Tipo

```text
implementation / repository topology
```

Execution posture: exact bounded local repository-topology creation completed; source import and all product execution remain blocked.

## 2. Objetivo

P12.1:

- creates the exact empty sibling Hermes product repository topology;
- preserve the locked upstream reference;
- establish `HermesProductRoot`;
- establish `HermesProductRepositoryMode`;
- establish `HermesProductRemotePolicy`;
- establish `HermesProductBranchPolicy`;
- establish the upstream relationship, no-touch boundary and Git boundary;
- establish validation, cleanup and rollback posture;
- prepares P12.2, P12.3, P12.5 and P12.6 without starting them.

The selected topology is `sibling_fresh_git_repository` with `snapshot_import_without_upstream_git_history`. The product repository intentionally contains no source or product file before P12.2.

## 3. Inputs and Prerequisite Resolution

| Prerequisite | Expected current canonical path or content | Exact path found? | Substantive content found? | Status | Action |
| --- | --- | --- | --- | --- | --- |
| P12.0 productization authorization | Prompt historical path `agent_platform_hermes_productization_authorization_boundary.md`; current canonical `agent_platform_hermes_productization_authorization_and_boundary.md` | Historical path: No; current path: Yes | Yes; P12 phase and P12.1 topology-decision responsibility authorized | Accepted | Consume current canonical content; do not recreate historical filename. |
| Exact `HermesProductRoot` | P12.1-owned decision under P12.0 delegation | Yes, in this record | `C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES` | Accepted | Apply fail-closed preflight and create only if absent. |
| Exact `HermesProductRepositoryMode` | P12.1-owned decision | Yes | `sibling_fresh_git_repository`; snapshot import without upstream Git history | Accepted | Initialize empty repository only. |
| Exact `HermesProductRemotePolicy` | P12.1-owned decision | Yes | Metadata-only `upstream`; official fetch URL; push URL `DISABLED`; no `origin` | Accepted | Configure locally without network. |
| Exact `HermesProductBranchPolicy` | P12.1-owned decision | Yes | Initial branch `main`; no additional branches | Accepted | Initialize `main`; no commit or push. |
| Topology creation authorization | Current exact P12.1 instruction under P12.0 delegation | Yes | Empty sibling topology creation explicitly authorized | Accepted | No source copy or product file. |
| P11.0 source review authorization | `agent_platform_hermes_source_review_authorization.md` | Yes | Exact repository/release/tag/SHA/path and no-mutation boundary present | Accepted | Consume lock. |
| P11.8 controlled runtime gate | `agent_platform_hermes_controlled_runtime_gate_record.md` | Yes | Lifecycle substrate accepted with limitations; no productization permission | Accepted as evidence only | Do not execute runtime. |
| P11.R closure | `agent_platform_hermes_integration_closure.md` | Yes | `hermes_integration_ready_with_limitations` present | Accepted | Preserve limitations. |
| P12 roadmap context | P12 sequence in current P12.0 and this ticket | Yes | P12.1/P12.2 parallel readiness; later waves remain gated | Accepted | Do not start adjacent tickets. |
| Post-cleanup rule | Current substantive canonical content over historical filename identity | Applicable | Yes | Accepted | No restoration or marker-alignment file. |
| `.opencode/` and `AGENTS.md` | No-touch unrelated local paths | Present as pre-existing untracked paths | Not inspected as inputs | Excluded | Do not modify, stage, delete or include. |

P12.0 prerequisite conclusion:

```yaml
P12_0_PrerequisiteStatus:
  canonical_record_present: true
  substantive_productization_authorization_accepted: true
  p12_1_record_creation_allowed: true
  p12_0_delegates_exact_topology_to_p12_1: true
  exact_product_root_present_in_p12_1: true
  exact_repository_mode_present_in_p12_1: true
  exact_remote_policy_present_in_p12_1: true
  exact_branch_policy_present_in_p12_1: true
  empty_topology_creation_authorized_now: true
  executable_topology_status: completed
```

```yaml
HermesProductTopologyCreationAuthorization:
  source: P12.0 delegation plus current exact P12.1 instruction
  p12_1_record_creation_authorized: true
  product_root_creation_authorized: true
  source_copy_or_clone_authorized: false
  repository_initialization_authorized: true
  local_upstream_remote_metadata_authorized: true
  branch_creation_authorized: true_main_only
  fetch_pull_push_authorized: false
  source_import_authorized: false
  status: executed_within_exact_bounds
```

## 4. HermesLockedUpstreamReference

```yaml
HermesLockedUpstreamReference:
  upstream_repository: "https://github.com/NousResearch/hermes-agent"
  release: "0.18.2"
  tag: "v2026.7.7.2"
  immutable_commit: "9de9c25f620ff7f1ce0fd5457d596052d5159596"
  local_source_path: "4_external/sources/hermes-agent"
  source_status: "read_only_locked_reference"
  allowed_operations:
    - Test-Path
    - git rev-parse HEAD
    - git status --short
    - git remote -v
    - git tag --points-at HEAD
  blocked_operations:
    - edit
    - checkout
    - reset
    - clean
    - merge
    - rebase
    - stash
    - commit
    - push
    - source_patch
    - install
    - execute
```

Observed read-only metadata:

| Check | Result | Verdict |
| --- | --- | --- |
| Path exists | Yes | Match |
| HEAD | `9de9c25f620ff7f1ce0fd5457d596052d5159596` | Exact match |
| Status | Clean; no `status --short` output | Unchanged |
| Origin fetch/push metadata | `https://github.com/nousresearch/hermes-agent.git` | Equivalent expected origin; no remote action |
| Tag at HEAD | `v2026.7.7.2` | Exact match |

The first direct metadata attempt was rejected by Git's dubious-ownership safety check and made no change. The same read-only commands were repeated with a temporary per-command `safe.directory` override already established by the accepted P11/P12.0 identity-check posture. Global Git configuration was not modified.

## 5. HermesProductRoot

```yaml
HermesProductRoot:
  product_root: "C:\\Users\\pablo\\OneDrive\\Escritorio\\AGENT-PLATFORM-HERMES"
  source_of_authorization: P12.0 delegation plus current exact P12.1 instruction
  location_class: sibling_repository
  inside_agent_platform_repo: false
  is_nested_git_repo: false
  is_sibling_repo: true
  is_submodule: false
  is_worktree: false
  is_symlink_or_hardlink_target: false
  is_outside_locked_upstream: true
  is_outside_artifacts: true
  is_outside_opencode: true
  creation_status: created
  validation_status: passed
  limitations:
    - empty Git topology only
    - no Hermes source or product file imported
    - local and unpublished pending P12.2
```

Fail-closed preflight evidence:

| Check | Result |
| --- | --- |
| Platform root canonicalized | `C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM` |
| Locked upstream canonicalized | `C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\4_external\sources\hermes-agent` |
| Product root canonicalized | `C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES` |
| Absolute and non-empty | Passed |
| Parent exists | `C:\Users\pablo\OneDrive\Escritorio` exists |
| Product root pre-existed | No |
| Outside AGENT PLATFORM | Passed |
| Outside locked upstream | Passed |
| Outside `.opencode` | Passed |
| Outside `9_artifacts` | Passed |
| Outside `graphify-out` | Passed |

The root was created only after every check passed.

## 6. HermesProductRepositoryMode

| Mode | Authorized by P12.0? | Command shape | Risk | Selected? | Blocker if not selected |
| --- | --- | --- | --- | --- | --- |
| `sibling_fresh_git_repository` | Yes, by current P12.1 authority under P12.0 delegation | `New-Item` exact root; `git init -b main` | Empty topology must remain source-free until P12.2 | **Yes** | N/A |
| `local_no_hardlink_clone` | No | Not executed | Would inherit restricted content and upstream history before P12.2 | No | Snapshot import deliberately deferred |
| `local_copy_without_git_history` | No in P12.1 | No copy command | Legal exclusion and provenance baseline must be applied during P12.2 | No | P12.2 owns snapshot import |
| `nested_untracked_git_repository` | No | No command | Nested Git and AGENT PLATFORM tracking confusion | No | Exact sibling topology selected |
| `future_remote_fork_reference_only` | No | No command | Hosted-repo/network operation prohibited | No | No hosted remote creation |
| `submodule` | No | No command | Coupled Git workflow and upstream mutation risk | No | Submodules prohibited |

```yaml
HermesProductRepositoryMode:
  selected_mode: sibling_fresh_git_repository
  source_history_mode: snapshot_import_without_upstream_git_history
  product_repository_created: true
  source_imported: false
  hardlinks_used: false
  symlinks_used: false
  submodule_used: false
  status: initialized_empty
```

## 7. HermesProductRemotePolicy

```yaml
HermesProductRemotePolicy:
  upstream_remote_name: upstream
  upstream_remote_url: "https://github.com/NousResearch/hermes-agent"
  upstream_fetch_url: "https://github.com/NousResearch/hermes-agent.git"
  upstream_push_url: DISABLED
  product_remote_name: origin_reserved_not_configured
  product_remote_url: deferred_to_future_human_approval
  remote_creation_authorized: false_hosted_repository_only
  local_remote_metadata_authorized: true
  fetch_authorized: false
  pull_authorized: false
  push_authorized: false
  network_authorized: false
  hosted_repo_creation_authorized: false
  application_status: upstream_metadata_configured_origin_deferred
```

The local `upstream` remote metadata was configured without contacting GitHub. `origin` remains absent and reserved for a future human-approved writable product remote. No fetch, pull, push, `ls-remote` or other network operation occurred.

## 8. HermesProductBranchPolicy

```yaml
HermesProductBranchPolicy:
  baseline_commit: "9de9c25f620ff7f1ce0fd5457d596052d5159596"
  baseline_branch: main
  product_main_branch: main
  upstream_sync_branch: deferred_to_P12_5
  protected_branches: future_policy_not_applied
  branch_creation_authorized: true_main_only
  checkout_authorized_inside_product_repo_only: false_after_initialization
  commit_authorized: false
  push_authorized: false
  application_status: main_initialized_unborn_no_commits
```

`git init -b main` initialized only `main`. No additional branch, checkout, commit or push occurred. Future synchronization branches belong to P12.5.

## 9. HermesProductTopologyCreationPlan

This plan records exact commands that were permitted and executed, plus blocked steps for which no exact command can legally exist yet. It contains no executable placeholder.

| Step ID | Action | Exact command or disposition | Source | Expected result | Stop rule | Rollback if failed |
| --- | --- | --- | --- | --- | --- | --- |
| P12.1-01 | Main repo status | `git status --short` | AGENT PLATFORM root | Only expected unrelated paths before record creation | Stop on conflicting tracked mutation | Read-only; no rollback |
| P12.1-02 | Resolve P12.0 | `Test-Path '0_architecture/governance/agent_platform_hermes_productization_authorization_and_boundary.md'` plus read-only content searches | Current canonical P12.0 | Record exists and substantive content resolves historical path | Stop if absent | Read-only; no rollback |
| P12.1-03 | Check P11.0 lock record | `Test-Path '0_architecture/governance/agent_platform_hermes_source_review_authorization.md'` plus exact `Select-String` checks | P11.0 | Exact repository/tag/SHA/path present | Stop on contradiction | Read-only; no rollback |
| P12.1-04 | Check locked upstream metadata | Per-command safe-directory `git -C` metadata checks recorded in Section 4 | Locked upstream | Exact SHA/tag/origin and clean status | Stop on mismatch or dirty state | Read-only; no rollback |
| P12.1-05 | Product-root conflict check | Canonical fail-closed PowerShell preflight recorded below | Exact P12.1 root | Root absent and outside all blocked roots | Stop before write on any failed condition | Read-only; no rollback |
| P12.1-06 | Product topology creation | `New-Item -ItemType Directory` at exact root; `git init -b main` | Current P12.1 authorization | Empty sibling Git repository on `main` | Stop on any creation/init failure | Remove only if certainly created here and contains no unrelated content |
| P12.1-07 | Apply remote policy | `git remote add upstream` and `git remote set-url --push upstream DISABLED` | Current P12.1 authorization | Local metadata only; no network | Stop on mismatch; do not fetch or repair broadly | Remove root only under safe created-here rule |
| P12.1-08 | Apply branch policy | Branch initialized only by `git init -b main` | Current P12.1 authorization | Unborn `main`; no additional branch | Stop before checkout/commit/push | Remove root only under safe created-here rule |
| P12.1-09 | Product topology validation | Exact local Git metadata checks recorded below | Created product root | Exact root, `main`, no commit/files, expected remotes | Stop on any mismatch | Do not reset/clean; apply safe created-here rollback rule |
| P12.1-10 | Update P12.1 record | Revise this exact canonical Markdown with creation evidence | P12.1 | One durable successful topology record | Stop before extra Markdown | Revise only this record if correction is needed |
| P12.1-11 | Final no-touch verification | Read-only target marker checks and `git status --short` | AGENT PLATFORM root | Only P12.1 target added by this work | Stop on unexpected conflict | No automatic remediation |
| P12.1-12 | Final status report | Final response only | P12.1 | Report blockers and no-action posture | Stop after report | None |

Exact topology creation commands executed after preflight:

```powershell
$ProductRoot = "C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES"
New-Item -ItemType Directory -Path $ProductRoot -ErrorAction Stop | Out-Null
git -C $ProductRoot init -b main
git -C $ProductRoot remote add upstream "https://github.com/NousResearch/hermes-agent.git"
git -C $ProductRoot remote set-url --push upstream DISABLED
```

Exact read-only upstream metadata commands used after the direct forms were rejected by Git's ownership safety check:

```powershell
git -c safe.directory="C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM/4_external/sources/hermes-agent" -C "4_external/sources/hermes-agent" rev-parse HEAD
git -c safe.directory="C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM/4_external/sources/hermes-agent" -C "4_external/sources/hermes-agent" status --short
git -c safe.directory="C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM/4_external/sources/hermes-agent" -C "4_external/sources/hermes-agent" remote -v
git -c safe.directory="C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM/4_external/sources/hermes-agent" -C "4_external/sources/hermes-agent" tag --points-at HEAD
```

## 10. HermesProductRemoteRegister

| Remote name | Remote URL or path | Purpose | Configured? | Fetch allowed? | Pull allowed? | Push allowed? | Network allowed? | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Locked source path reference | `4_external/sources/hermes-agent` | Immutable local provenance/source reference | Not configured as a path remote | No | No | No | No | Read-only metadata only |
| `upstream` | `https://github.com/NousResearch/hermes-agent.git` fetch; `DISABLED` push | Metadata-only canonical upstream relationship | Yes | No | No | No | No | Configured locally; no contact performed |
| `origin` | Deferred | Future human-approved writable product remote | No | No | No | No | No | Name reserved; absent now |
| Future product remote | Deferred to future exact human approval | Future hosted product relationship | No | No | No | No | No | Hosted repository creation prohibited in P12.1 |

## 11. HermesProductUpstreamRelationship

```yaml
HermesProductUpstreamRelationship:
  baseline_commit: "9de9c25f620ff7f1ce0fd5457d596052d5159596"
  locked_reference_posture: immutable_read_only
  product_repository_posture: empty_sibling_repository_initialized
  source_history_policy: snapshot_import_without_upstream_git_history
  source_import_posture: deferred_to_P12_2
  future_editability: after_P12_2_snapshot_and_license_baseline
  stable_adapter_required: true
```

| Relationship surface | Owner ticket | P12.1 status | Future gate |
| --- | --- | --- | --- |
| Empty product repository topology | P12.1 | Completed on unborn `main`; no source or commit | P12.2 snapshot import |
| Initial source snapshot from immutable P11.0 commit | P12.2 | Deferred; no source imported | P12.2 legal/provenance baseline |
| Locked upstream reference | P11.0/P12.0 | Verified and unchanged | Read-only comparisons only |
| Product-source editability | P12.2 plus later source tickets | Repository exists but contains no source | P12.2 snapshot and license boundary |
| License exclusion/NOTICE baseline | P12.2 | Not performed | P12.2 acceptance |
| Development environment | P12.3 | Not started | P12.1/P12.2 inputs and exact package gate |
| Build/test/UI baseline | P12.4 | Not started | P12.3 environment and exact build/test gate |
| Upstream synchronization | P12.5 | Not configured | Exact remote/branch/sync policy |
| Extension/configuration seams | P12.6 | Not started | Controlled source and baseline evidence |
| Adapter implementation | P14 | Not started | Stable P11.5 contracts and later implementation gate |
| Provider-backed worker | P15 | Not started | Provider/security/runtime gates |
| WorkPacket execution | P17 | Not started | Adapter and worker readiness |

## 12. HermesProductNoTouchBoundary

```yaml
HermesProductNoTouchBoundary:
  paths_and_surfaces:
    - 4_external/sources/hermes-agent
    - .opencode/
    - AGENTS.md
    - all P11 documents
    - 0_architecture/governance/agent_platform_hermes_productization_authorization_and_boundary.md
    - .gitignore
    - .graphifyignore
    - credentials and secret stores
    - .env files
    - provider configuration
    - product/Siamese source
    - generated artifacts and runtime state
    - external tools outside exact P12.0 authorization
  modification_authorized: false
  content_inspection_authorized: false_except_governance_and_locked_git_metadata
```

No no-touch surface was modified. `.opencode/`, `AGENTS.md` and `graphify-out/` remained unrelated untracked paths and were not inspected or included.

## 13. HermesProductGitBoundary

```yaml
HermesProductGitBoundary:
  agent_platform_staging: prohibited
  agent_platform_commit: prohibited
  agent_platform_push: prohibited
  product_repository_staging: prohibited
  product_repository_commit: prohibited
  product_repository_push: prohibited
  force_add: prohibited
  git_add_dot: prohibited
  remote_network_operations: prohibited
  hosted_repository_creation: prohibited
  product_git_metadata_configuration: upstream_only_completed_without_network
  human_git_authority_required: true
```

No AGENT PLATFORM staging/history mutation occurred. Product-repository Git mutation was limited to authorized initialization of unborn `main` and local `upstream` metadata. No product file, index entry, commit, fetch, pull or push exists. Final human commit guidance covers only this canonical P12.1 record.

```text
Never use git add .
```

## 14. Rollback / Cleanup Posture

| Failure point | Required rollback/cleanup posture | Current result |
| --- | --- | --- |
| Product root already exists | Stop; classify ownership and contents by safe metadata; never overwrite or delete | Preflight confirmed absent |
| Product root partially created | Delete only if created by this ticket, exact path is known, ownership is certain and cleanup is authorized; otherwise stop for human review | Not applicable; topology completed successfully |
| Repository initialization fails | Preserve safe error metadata; do not retry with clone/copy/network alternatives | Initialization succeeded |
| Remote policy application fails | Stop; do not fetch/pull/push or invent remote repair | Local metadata applied successfully |
| Branch policy application fails | Stop; do not reset/clean/rebase/stash or commit | `main` initialized successfully |
| Validation mismatch | Stop; preserve metadata; do not repair source or history automatically | No mismatch observed |
| Unexpected product commit | Stop; do not checkout/reset/clean; require human review | Expected no-commit result confirmed |
| Product repo dirty after creation | Stop; do not stage/commit/clean; inventory safe status metadata | Status empty; no product files |
| Accidental blocked-path overlap | Stop before creation; never delete locked upstream, `.opencode/`, `AGENTS.md` or unrelated content | Preflight proved no overlap |

No rollback was required. If later correction is needed, the product root may be removed only when it remains certain that P12.1 created it and it contains no unrelated content; otherwise it must be quarantined for human review. No destructive Git remediation is authorized.

## 15. HermesProductTopologyValidation

```yaml
HermesProductTopologyValidation:
  locked_upstream_path_exists: true
  locked_upstream_head_matches: true
  locked_upstream_status_unchanged_clean: true
  locked_upstream_tag_matches: true
  locked_upstream_origin_matches: true
  product_root_exists: true
  product_root_exact_absolute_path: true
  product_root_outside_agent_platform: true
  product_root_outside_locked_upstream: true
  product_root_outside_opencode: true
  product_root_outside_artifacts: true
  product_root_outside_graphify: true
  product_repository_initialized: true
  current_branch: main
  repository_has_commit: false
  working_tree_has_product_file: false
  upstream_fetch_url_matches: true
  upstream_push_url_disabled: true
  origin_absent: true
  fetch_pull_push_occurred: false
  install_build_test_run_occurred: false
  git_staging_occurred: false
  opencode_changed: false
  agents_md_changed: false
  topology_validation_status: passed_ready_for_P12_2
```

Validation conclusion:

```text
locked upstream no-touch validation passed
product topology validation passed
main is an unborn branch with no commits
working tree contains no product file
upstream metadata configured without network; origin absent
```

## 16. P12.2 Handoff

P12.2 owns:

- restrictive `skills/productivity/powerpoint` exclusion or separate-clearance baseline;
- license exclusion rules;
- Apache-2.0 license and NOTICE preservation;
- third-party notice and attribution inventory;
- file/subtree compliance inventory;
- redistributability boundary.

P12.1 performed no source import, license exclusion, removal or license-file alteration. P12.2 owns the first controlled snapshot import together with restrictive-subtree exclusion, NOTICE/attribution baseline and provenance inventory. The empty product repository remains local, unpublished, unreleased and non-distributed.

```text
hermes_P12_2_ready
hermes_source_snapshot_import_deferred_to_P12_2
```

## 17. P12.3 / P12.4 / P12.5 / P12.6 Handoff

| Future ticket | Consumes from P12.1 | Remains blocked | Required input |
| --- | --- | --- | --- |
| P12.3 Reproducible Development Environment | Exact sibling root and empty repository mode | Package manager, venv, Node/Python/toolchain setup | P12.2 controlled snapshot/license baseline and exact dependency gate |
| P12.4 Baseline Build, Test and UI Snapshot | Controlled source identity and environment | Builds, tests, frontend bundles and snapshots | P12.3 reproducible environment and exact validation commands |
| P12.5 Upstream Synchronization Strategy | Metadata-only `upstream` remote and source-history policy | Fetch, merge, rebase, pull, push and sync execution | P12.2 snapshot provenance plus exact sync branches and human Git gates |
| P12.6 Product Extension and Configuration Seams | Controlled source and stable adapter boundary | UI/backend edits, adapter implementation and product integration | P12.2-P12.5 accepted inputs |
| P12.7 Clean Rebuild and Rollback Drill | Topology, license, environment, build and sync evidence | Drill execution | P12.1-P12.6 completion and exact rollback gate |
| P12.R Productization Foundation Closure | All P12 records | Closure claim | P12.1-P12.7 accepted evidence |

No future ticket was started by P12.1.

## 18. Acceptance Criteria

| Criterion | Status |
| --- | --- |
| P12.0 present and accepted by substantive content | Met |
| P12.0 delegates exact topology decisions to P12.1 | Met |
| Exact `HermesProductRoot` resolved by P12.1 | Met |
| Exact `HermesProductRepositoryMode` resolved by P12.1 | Met |
| Exact `HermesProductRemotePolicy` resolved by P12.1 | Met |
| Exact `HermesProductBranchPolicy` resolved by P12.1 | Met |
| Empty topology creation exactly authorized | Met |
| Locked upstream path exists | Met |
| Locked upstream HEAD matches immutable commit | Met |
| Locked upstream status remains clean | Met |
| Product root created only after fail-closed preflight | Met |
| Product root outside platform/upstream/opencode/artifacts/Graphify | Met |
| No hardlinks or symlinks | Met |
| No submodule | Met |
| No locked-upstream modification | Met |
| No license exclusion or PowerPoint removal | Met |
| No install/build/test/run or dependency installation | Met |
| No provider/API/OAuth/MCP or credentials | Met |
| No `.env` inspection | Met |
| No `.gitignore`, `.graphifyignore`, `.opencode/` or `AGENTS.md` change | Met |
| No staging/commit/push | Met |
| P12.1 canonical record exists | Met |
| Created / Not Created Register exists | Met |
| Final verdict explicit | Met |
| Commit guidance avoids `git add .` | Met |

P12.1 topology-readiness acceptance is satisfied. Source/legal baseline work remains deferred to P12.2.

## 19. Validation Required

Validation performed only through allowed read-only checks:

- main-repository `git status --short`;
- exact `Test-Path` checks for P12.1, current/historical P12.0, P11.0, P11.8, P11.R and locked upstream;
- read-only searches in current canonical governance records;
- exact source-lock `Select-String` checks;
- locked upstream `rev-parse`, `status`, `remote -v` and `tag --points-at HEAD` metadata checks;
- target document path and marker checks;
- final `git status --short`.

No test, script, package manager, Python, Node, build, Hermes, runtime, provider/API/OAuth/MCP, network, staging, commit or push command was run.

## 20. Created / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_hermes_controlled_fork_repository_topology.md
C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES\
  empty sibling Git repository topology only
```

Modified:

```text
no pre-existing AGENT PLATFORM file
C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES\.git\
  initialized unborn main branch
  configured metadata-only upstream remote
  configured upstream push URL as DISABLED
```

Not created, modified, removed, executed, activated or approved:

```text
no Hermes source copy, local clone, hosted repository, origin remote, additional branch,
   commit, tag, worktree, submodule, subtree, vendored tree, symlink, hardlink or source import
no P12.2-P12.R or P13-P21 document
no retry, safe-block, rerun, marker-alignment, naming-drift or diagnostic Markdown
no modification to 4_external/sources/hermes-agent and no upstream patch
no license exclusion, license-file alteration or PowerPoint skill removal
no install, dependency acquisition, package manager, build, test or runtime execution
no provider/API/OAuth/MCP activation, credential use or .env inspection
no product/Siamese, GBrain, GStack, Paperclip, ECC, OpenCode or Graphify source inspection
no adapter, UI, runtime, worker, Ticket Factory or WorkPacket execution implementation
no GBrain or Paperclip integration, database, vector DB, graph DB, embeddings,
   telemetry or event streaming
no .opencode/, AGENTS.md, .gitignore, .graphifyignore or P11/P12.0 modification
no AGENT PLATFORM or product-repository staging, commit, push, fetch, pull,
   network operation, force-add or publication
```

## 21. Limitations and Blockers

```yaml
HermesProductTopologyBlocker:
  active: false
  prior_interpretation: P12.0 had to predefine exact topology values
  correction: P12.0 delegates exact topology decisions to P12.1
  resolution: current P12.1 exact instruction selected and created the bounded empty topology
```

Limitations retained:

- the product repository contains no Hermes source and no commit;
- P12.2 must perform the first controlled snapshot import and legal baseline;
- `origin` and any hosted product repository remain deferred;
- fetch/pull/push and synchronization branches remain deferred to P12.5;
- mixed-license/SBOM posture, broader provider/catalog/update egress, app-level graceful shutdown, adapter conformance, WorkPacket execution and production readiness remain unresolved.

## 22. Recommended Next Ticket

Parallel P12 queue after this topology record:

```text
P12.2 - License Exclusion and Notice Baseline
P12.3 - Reproducible Development Environment, after P12.2 source/legal baseline
P12.5 - Upstream Synchronization Strategy, after P12.2 provenance baseline
```

Recommended actual next ticket:

```text
P12.2 - License Exclusion and Notice Baseline
```

P12.1 does not start P12.2, P12.3, P12.4, P12.5, P12.6, P12.7, P12.R or P13-P21.

## 23. HermesProductTopologyVerdict

```yaml
HermesProductTopologyVerdict:
  p12_0_present_and_substantively_accepted: true
  product_root_resolved: true
  product_root_created: true
  repository_mode: sibling_fresh_git_repository
  source_history_mode: snapshot_import_without_upstream_git_history
  default_branch: main
  upstream_remote_configured: true
  upstream_fetch_performed: false
  origin_configured: false
  source_import_performed: false
  product_commit_created: false
  locked_upstream_unchanged: true
  P12_2_may_proceed: true
  final_topology_verdict: ready_for_P12_2_snapshot_and_license_baseline
  locked_upstream_commit_used: "9de9c25f620ff7f1ce0fd5457d596052d5159596"
  locked_upstream_head_matches: true
  locked_upstream_remained_clean: true
  product_root_outside_locked_upstream: true
  product_root_outside_opencode: true
  product_root_outside_artifacts: true
  hardlinks_avoided: true
  symlinks_avoided: true
  submodule_created: false
  remote_network_operation_performed: false
  fetch_pull_push_performed: false
  license_exclusion_performed: false
  install_build_test_run_performed: false
  credentials_or_env_inspected: false
  opencode_modified: false
  agents_md_modified: false
  gitignore_modified: false
  graphifyignore_modified: false
  agent_platform_git_mutated: false
  product_repository_committed_or_pushed: false
  ready_marker_emitted: true
```

Final answers:

| Question | Answer |
| --- | --- |
| What did P12.1 create? | This canonical topology record and the exact empty sibling Git repository root. |
| Was P12.0 present and accepted by substantive content? | Yes, at the current canonical `...authorization_and_boundary.md` path. |
| What product root was resolved? | `C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES`. |
| What repository mode was selected? | `sibling_fresh_git_repository` with `snapshot_import_without_upstream_git_history`. |
| What remote policy was applied or deferred? | Local metadata-only `upstream` configured with official fetch URL and push URL `DISABLED`; `origin` deferred. |
| What branch policy was applied or deferred? | Unborn `main` initialized; no additional branch; sync branches deferred to P12.5. |
| Which P11.0 lock was used? | Hermes `0.18.2`, tag `v2026.7.7.2`, commit `9de9c25f620ff7f1ce0fd5457d596052d5159596`, path `4_external/sources/hermes-agent`. |
| Did locked upstream HEAD match? | Yes. |
| Did locked upstream remain unchanged? | Yes; status was clean. |
| Was product root created? | Yes, after fail-closed preflight. |
| Was product root outside blocked paths? | Yes, outside AGENT PLATFORM, locked upstream, `.opencode`, artifacts and Graphify. |
| Were hardlinks and symlinks avoided? | Yes; neither was created. |
| Was any submodule created? | No. |
| Was any remote network/fetch/pull/push performed? | No. |
| Was any license exclusion performed? | No; P12.2 owns it. |
| Was any install/build/test/run performed? | No. |
| Were credentials or `.env` inspected? | No. |
| Were `.opencode/`, `AGENTS.md`, `.gitignore` or `.graphifyignore` modified? | No. |
| Was AGENT PLATFORM Git mutated? | No. |
| Was a product repository committed or pushed? | No; the repository has no commits and no push occurred. |
| What remains for P12.2? | Restricted-skill exclusion, NOTICE/attribution baseline, compliance inventory and redistributability boundary. |
| What remains for P12.3-P12.6? | Environment, baseline build/test/UI evidence, synchronization policy and extension/configuration seams after topology resolution. |
| What is the final topology verdict? | Ready for P12.2 snapshot and license baseline. |
| What is next? | P12.2 License Exclusion and Notice Baseline. |

```text
hermes_controlled_fork_repository_topology_ready
hermes_product_root_created
hermes_product_repository_initialized
hermes_product_main_branch_initialized
hermes_upstream_remote_configured_without_network
hermes_origin_remote_deferred
hermes_source_snapshot_import_deferred_to_P12_2
hermes_locked_upstream_reference_unchanged
hermes_P12_2_ready
no_source_copy_created
no_product_commit_created
no_remote_network_operation
no_install_build_test_run
no_agent_platform_git_mutation
```

## Commit Commands

P12.1 did not stage, commit or push. If the human accepts this topology record, the human may run:

```powershell
git status --short

git add 0_architecture/governance/agent_platform_hermes_controlled_fork_repository_topology.md

git commit -m "P12.1 - Controlled Fork and Repository Topology"

git push origin main
```

Never use `git add .`.
