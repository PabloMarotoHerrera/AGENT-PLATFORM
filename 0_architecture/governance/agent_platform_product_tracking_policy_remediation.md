# P12.C3 - AGENT PLATFORM Product Tracking Policy Remediation

## 1. Document Header

| Field | Value |
| --- | --- |
| Project | P12 - Hermes Productization Foundation |
| Ticket | P12.C3 - AGENT PLATFORM Product Tracking Policy Remediation |
| Type | Repository policy / Git tracking remediation |
| Date | 2026-07-13 |
| Status | Product tracking policy remediated; corrected P12.1 reentry ready after acceptance |
| Execution class | Bounded configuration and documentation change |
| Canonical output | `0_architecture/governance/agent_platform_product_tracking_policy_remediation.md` |
| Authorized workspace | `C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM` |
| Future Hermes root | `2_products/hermes-agent` |
| Product root created | No |
| Source import | None |
| Git index/history mutation | None |

Result markers:

```text
agent_platform_product_tracking_policy_remediated
hermes_product_tracking_exception_defined
hermes_product_root_trackable_without_force_add
sibling_products_remain_ignored
whole_class_product_ignore_replaced_with_fail_closed_policy
hermes_p12_1_reentry_ready
hermes_p12_2_remains_sequenced_after_corrected_p12_1
no_hermes_product_root_created
no_product_source_import
no_force_add
no_nested_git_created
no_runtime_execution
no_git_mutation_by_agent
```

## 2. Purpose

P12.C3 resolves only `TOP-C2-001`: the root `.gitignore` rule that ignored the
complete `2_products` class and prevented the future Hermes product from being
tracked normally by the main AGENT PLATFORM repository.

The remediation preserves fail-closed sibling products, creates no product
directory or source, uses no force-add, and grants no product activation,
runtime, dependency, publication, staging, commit or push authority.

## 3. P12.C2 Prerequisite Status

| Prerequisite | Observed result | Verdict |
| --- | --- | --- |
| P12.C2 canonical record | Present | Passed |
| Current topology classification | `usable_with_bounded_structural_corrections` | Match |
| Selected root | `2_products/hermes-agent` | Exact match |
| Required remediation | `P12.C3` | Exact match |
| P12.1 before remediation | Reentry blocked | Confirmed |
| P12.2 sequencing | Must wait for corrected P12.1 | Confirmed |
| Authorized root | Exact path with space exists and is the main Git root | Passed |
| Invalid external root | `C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES` absent | Passed |
| Future Hermes root | Absent | Passed |
| Locked upstream | Clean at `9de9c25f620ff7f1ce0fd5457d596052d5159596` | Passed |

No P12.C2 contradiction was found.

## 4. Current Ignore Policy

Pre-remediation `.gitignore` SHA-256:

```text
7CF93862570B82A70C756822CB7699FD4E2042CC9BE30C45ADE21F0EFFAA7562
```

The exact original product policy was:

```gitignore
# Ignore products for now
2_products/
```

The source was `.gitignore:8-9`. `git check-ignore -v` showed line 9 ignoring:

```text
2_products
2_products/hermes-agent
2_products/hermes-agent/.tracking-probe
```

Before remediation, no product path was tracked, visible in short status, or
staged. No probe file was created.

## 5. Current Product-Class Inventory

Only immediate child names were inspected:

```text
backend-energyplus
cli
desktop
experimental
omniverse-app
web-platform
```

`hermes-agent` was absent. Sibling contents were not inspected. Pre-change
tracked, visible and staged path counts under `2_products` were all zero.

## 6. Selected Tracking Semantics

```yaml
AgentPlatformProductTrackingPolicy:
  product_class_root: 2_products
  default_product_tracking: ignored
  explicitly_trackable_products:
    - 2_products/hermes-agent
  sibling_product_default: ignored
  force_add_required_for_hermes: false
  nested_git_allowed: false
  independent_product_remote_allowed: false
  product_tracking_authority: explicit_per_product_governance
```

The policy is fail-closed. New immediate product children match the default
ignore rule automatically. An exception requires its own exact governance and
`.gitignore` policy change.

## 7. Exact `.gitignore` Change

The whole-directory rule was replaced with:

```gitignore
# Ignore products by default; exceptions require explicit product governance
/2_products/*
!/2_products/hermes-agent
!/2_products/hermes-agent/**
```

The root-anchored `*` permits Git to traverse `2_products` while ignoring every
immediate child by default. The first negation is intentionally path-type-
neutral so the currently absent `hermes-agent` token validates as not ignored.
The second negation allows future descendants.

An initial candidate used `!/2_products/hermes-agent/`. Validation showed that
descendants were trackable but the nonexistent directory token itself still
matched the default rule because Git could not classify an absent path as a
directory. That candidate was corrected before policy documentation was edited.
No filesystem path or probe was created.

Post-remediation `.gitignore` SHA-256:

```text
E1A7238DB58ABFA93DA762EC87801DF8B74877CC573608ED0F83E55EC352C40A
```

No non-product ignore rule changed.

## 8. Sibling-Product Protection

Exit-code-aware `git check-ignore -q` results:

| Sibling | Directory token | Synthetic descendant | Result |
| --- | ---: | ---: | --- |
| `backend-energyplus` | `0` | `0` | Ignored |
| `cli` | `0` | `0` | Ignored |
| `desktop` | `0` | `0` | Ignored |
| `experimental` | `0` | `0` | Ignored |
| `omniverse-app` | `0` | `0` | Ignored |
| `web-platform` | `0` | `0` | Ignored |

Verbose output attributed every sibling and descendant to:

```text
.gitignore:9:/2_products/*
```

No sibling became untracked-visible in `git status --short -- 2_products`.

## 9. Hermes Trackability Validation

| Future path | `git check-ignore -q` exit | Interpretation |
| --- | ---: | --- |
| `2_products/hermes-agent` | `1` | Not ignored |
| `2_products/hermes-agent/.tracking-probe` | `1` | Not ignored |

Verbose output identified the two negation rules, while the quiet command's
nonzero status established that neither path is ignored. `Test-Path` remained
false. No `git add -f` or normal `git add` was executed; force-add is unnecessary.

## 10. Tracked / Visible / Staged Safety Checks

| Check | Before | After |
| --- | --- | --- |
| `git ls-files -- "2_products/**"` | Empty | Empty |
| `git status --short -- "2_products"` | Empty | Empty |
| `git diff --cached --name-only -- "2_products"` | Empty | Empty |
| `2_products/hermes-agent` exists | No | No |
| Sibling visible in status | No | No |
| Product path staged | No | No |

The exception changes only future path eligibility. It does not create or track
content.

## 11. Policy Documents Updated

Modified because their present-tense whole-class statements materially
conflicted with the exact exception:

```text
0_architecture/product_workspaces/agent_platform_product_git_posture_decision.md
0_architecture/workspace/agent_platform_product_workspace_policy.md
0_architecture/workspace/agent_platform_workspace_topology.md
0_architecture/workspace/agent_platform_workspace_responsibility_map.md
```

Each now states that product children remain ignored by default,
`2_products/hermes-agent` is the sole current governed tracking exception, the
exception creates and activates nothing, Hermes belongs to the main repository
without nested Git or an independent remote, and every future exception needs
separate governance.

Pre-ticket SHA-256 values:

| Policy record | Pre-ticket SHA-256 |
| --- | --- |
| Product Git posture | `EE393A76AC306B3A1CF6A153D98F0BADF028A577C6EF88053E2432B93EF9F957` |
| Product workspace policy | `3402128097254591877C0E927CAEEC72CDCF9FC519FFA42C1EFBFCB74AA7D84A` |
| Workspace topology | `FF107BE09F96A6745EE8293EB8F5402E431DAB6E38492FF2B6F2247ED9F436C8` |
| Workspace responsibility map | `06E134B4DA5A0B8EAC995914020744E3BEA7794D02AF1547DAED3092A2A835CD` |

Post-ticket SHA-256 values:

| Policy record | Post-ticket SHA-256 |
| --- | --- |
| Product Git posture | `B8C96DC425FAD0276FAFF65C121E3E35098A204EDDEEAC39C0F1177872C0F218` |
| Product workspace policy | `F8E7A7ABA4D8BA7161660294FE4812B96EAEF3F2EFE17B021944CFCE28617FD3` |
| Workspace topology | `2FF0506203010343A0020259A45E9E965FD86955D9E3F02DEE7E3A0B24D4B0BE` |
| Workspace responsibility map | `D33270E25E1CCBAFB4E8225689973A5FC48CA377EDA928D453AE87452389407D` |

Evaluated but not modified:

```text
0_architecture/product_workspaces/agent_platform_product_dependency_external_source_posture.md
README.md
```

P-09 is scoped to the six inactive Siamese candidates and does not govern the
new P12 Hermes exception. README contains no product tracking statement that
became false.

## 12. No-Touch Validation

```yaml
P12_C3_NoTouchValidation:
  invalid_external_root_absent: true
  future_hermes_root_absent: true
  product_source_created: false
  sibling_product_contents_modified: false
  locked_upstream_head: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  locked_upstream_clean: true
  nested_git_created: false
  branch_created: false
  remote_created: false
  worktree_created: false
  submodule_created: false
  symlink_created: false
  graphify_used: false
  runtime_or_package_command_run: false
  network_operation_run: false
  credential_or_env_value_inspected: false
  product_path_staged: false
  git_index_or_history_mutated: false
```

`.opencode`, `AGENTS.md`, root `graphify-out`, `.graphifyignore`,
`9_artifacts`, P12.1, P12.2, P11 records, product contents and locked upstream
source contents were not modified or included.

## 13. Rollback Procedure

No rollback was required because final validation passed. If this policy must be
reversed under human direction:

1. Verify the current `.gitignore` hash is the recorded post-ticket hash.
2. Replace only the three P12.C3 product lines and comment with the exact original
   two lines recorded in Section 4.
3. Reverse only the P12.C3 correction blocks and changed rows in the four policy
   records, then verify their exact pre-ticket hashes from Section 11.
4. Remove this new record only if explicitly human-directed.
5. Verify all six siblings and both Hermes synthetic paths return to the original
   line-9 whole-class ignore rule.
6. Verify the Git index remains unchanged.

Do not use `git reset`, `git checkout`, `git restore`, `git clean`, broad
wildcard deletion or force-add for rollback.

## 14. P12.1 Reentry Decision

```yaml
HermesP12_1Reentry:
  may_reenter: true
  exact_root: 2_products/hermes-agent
  root_must_be_absent_before_reentry: true
  create_normal_directory_only: true
  nested_git: prohibited
  source_import: prohibited
  remote_or_branch_creation: prohibited
  main_repository_tracking: required
```

Corrected P12.1 may reenter only after human acceptance of P12.C3. It must create
and validate an empty normal directory, not initialize a repository or import
source.

## 15. P12.2 Sequencing

```yaml
HermesP12_2Sequencing:
  may_reenter_after_corrected_P12_1: true
  may_reenter_before_corrected_P12_1: false
  source_import_from_locked_upstream_only: true
  reuse_deleted_external_snapshot: prohibited
  nested_git_creation: prohibited
  independent_commit_history: prohibited
  human_main_repo_git_authority: retained
```

P12.C3 does not unlock P12.3, P12.4, P12.5 execution, P12.6, P12.7, P12.R,
P13 or P14.

## 16. Created / Modified / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_product_tracking_policy_remediation.md
```

Modified:

```text
.gitignore
0_architecture/product_workspaces/agent_platform_product_git_posture_decision.md
0_architecture/workspace/agent_platform_product_workspace_policy.md
0_architecture/workspace/agent_platform_workspace_topology.md
0_architecture/workspace/agent_platform_workspace_responsibility_map.md
```

Not created or modified:

```text
2_products/hermes-agent
any product source or sibling product content
temporary probe file
nested .git
branch, remote, worktree, submodule or symlink
build, runtime, dependency, package or generated state
P12.1 or P12.2 canonical records
P11 records
4_external/sources/hermes-agent/**
README.md
.graphifyignore
.opencode/**
AGENTS.md
graphify-out/**
retry, safe-block, diagnostic or marker-alignment Markdown
```

## 17. Validation Commands and Notes

Read-only validation used `git status --short`, `git check-ignore -q/-v` for the
exact product paths, `git ls-files`, `git diff --cached --name-only`, exact
`Test-Path`/`if exist` checks, Git-root metadata, locked-upstream `rev-parse` and
status, file hashes, bounded directory-name listing, and exact content searches.

Two initial PowerShell metadata aggregations were parsed by `cmd.exe` and failed
without changing state; both were rerun explicitly through PowerShell. One direct
`Test-Path` command was also parsed by `cmd.exe`; the absence check was rerun with
`if exist`. No prohibited fallback was used.

No Graphify, package manager, build, test, Hermes, runtime, provider/API/OAuth/
MCP, fetch, network, credential, `git add`, force-add, commit or push command ran.

## 18. Final Verdict

```yaml
P12_C3_ProductTrackingPolicyVerdict:
  current_ignore_conflict_resolved: true
  product_class_default_ignore_retained: true
  hermes_tracking_exception_active: true
  hermes_product_root_exists: false
  hermes_path_trackable_without_force_add: true
  sibling_products_remain_ignored: true
  sibling_products_visible_in_status: false
  product_paths_staged: false
  nested_git_created: false
  product_remote_created: false
  locked_upstream_unchanged: true
  P12_1_may_reenter: true
  P12_2_must_wait_for_corrected_P12_1: true
```

```text
agent_platform_product_tracking_policy_remediated
hermes_product_tracking_exception_defined
hermes_product_root_trackable_without_force_add
sibling_products_remain_ignored
whole_class_product_ignore_replaced_with_fail_closed_policy
hermes_p12_1_reentry_ready
hermes_p12_2_remains_sequenced_after_corrected_p12_1
no_hermes_product_root_created
no_product_source_import
no_force_add
no_nested_git_created
no_runtime_execution
no_git_mutation_by_agent
```

## 19. Human Commit Commands

P12.C3 did not stage, commit or push. If the human accepts the remediation, use
only these exact main-repository commands:

```powershell
git status --short
git add .gitignore
git add 0_architecture/product_workspaces/agent_platform_product_git_posture_decision.md
git add 0_architecture/workspace/agent_platform_product_workspace_policy.md
git add 0_architecture/workspace/agent_platform_workspace_topology.md
git add 0_architecture/workspace/agent_platform_workspace_responsibility_map.md
git add 0_architecture/governance/agent_platform_product_tracking_policy_remediation.md
git commit -m "P12.C3 - Remediate Hermes product tracking policy"
git push origin main
```

Never use `git add .`.
