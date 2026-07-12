# P12.C1 - Misplaced Hermes Product Root Rollback and Removal

## 1. Record Header

| Field | Value |
| --- | --- |
| Project | P12 - Hermes Productization Foundation |
| Ticket | P12.C1 - Misplaced Hermes Product Root Rollback and Removal |
| Type | Corrective action / rollback / incident containment |
| Date | 2026-07-12 |
| Status | Completed; misplaced root removed after exact ownership proof |
| Canonical output | `0_architecture/governance/agent_platform_hermes_misplaced_product_root_rollback.md` |
| Durable document count | Exactly one new corrective record |
| Runtime execution | None |
| Package installation | None |
| Network operations | None |
| Git history rewrite | None |

Result markers:

```text
hermes_misplaced_product_root_incident_recorded
hermes_p12_1_material_result_rolled_back
hermes_p12_2_material_result_rolled_back
hermes_external_product_root_removed
hermes_agent_platform_root_preserved
hermes_locked_upstream_reference_unchanged
hermes_topology_redefinition_required
no_git_history_rewrite
no_remote_network_operation
no_credentials_inspected
```

## 2. Incident Summary

P12.1 initialized a product Git repository at the unauthorized external sibling
path `C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES`. P12.2 then
placed a filtered Hermes snapshot and five legal/provenance files in that
repository. P12.C1 inventoried only authorized path, Git, manifest, filename,
size, hash and process metadata; proved that every file belonged to P12.2;
removed the exact misplaced root; and reopened P12.1 and P12.2.

No replacement topology was created. P12.C2 owns that decision.

## 3. Root-Cause Analysis

The incorrect sibling root was introduced by an assistant-generated topology
decision that was not grounded in the user's workspace policy.

The agent then executed that exact but incorrect authorization.

The execution agent did not independently violate its supplied scope.

The governance failure was the missing global invariant that all normal project
work must remain under AGENT-PLATFORM.

P11.2 did not cause or contribute to the incident.

## 4. Affected and Unaffected Tickets

Affected and reopened:

```text
P12.1 - Controlled Fork and Repository Topology
P12.2 - License Exclusion and Notice Baseline
```

Unaffected:

```text
P11.2 - Hermes Architecture Mapping
all P11 architecture and source-lock evidence
```

The SHA-256 of
`0_architecture/governance/agent_platform_hermes_architecture_mapping.md` was
`2797C043DE240776E6816D30E63C5E07080F64AD819255A575D75D2F5C57D6F9` before
and after P12.C1.

## 5. Root Identity and Clarification

| Role | Exact path | Result |
| --- | --- | --- |
| Protected AGENT PLATFORM root | `C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM` | Human-confirmed active authorized workspace; preserved |
| Misplaced product root | `C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES` | Exact P12.1-created path; removed |
| Locked upstream | `C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\4_external\sources\hermes-agent` | Preserved clean at locked SHA |

The ticket text initially named
`C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM` as the protected root.
Preflight established that this hyphenated path did not exist, while the active
Git root and all canonical inputs were under `AGENT PLATFORM`. Before any
destructive action, the human explicitly selected `AGENT PLATFORM` as the exact
root P12.C1 must preserve and use for locked-upstream validation. P12.C1 did not
create or invent another root.

Misplaced-root preflight:

```yaml
MisplacedRootPreflight:
  exists_before_deletion: true
  resolved_path_exact: true
  is_directory: true
  attributes: Directory
  is_reparse_point: false
  link_type: none
  link_target: none
  contains_git_directory: true
  outside_protected_agent_platform: true
  equals_user_profile: false
  equals_desktop: false
  parent_of_agent_platform: false
```

## 6. Safe Repository Inventory

```yaml
MisplacedRepositoryInventory:
  git_top_level: C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES
  current_branch: main
  head_exists: false
  head_sha: none
  commit_count: 0
  commit_subjects: none
  local_branch_refs: 0
  tags: 0
  refs: 0
  reflog_entries: 0
  status_entries: 6116
  status_kind: staged_addition
  index_entries: 6116
  remotes:
    upstream_fetch: https://github.com/NousResearch/hermes-agent.git
    upstream_push: DISABLED
    origin: absent
  file_count_outside_git: 6116
  bytes_outside_git: 134712779
  reparse_points_outside_git: 0
  worktree_count: 1_primary_only
  submodule_entries: 0
  gitmodules_present: false
  active_process_matches_at_deletion_gate: 0
```

The 6,116 staged additions contradict P12.2's prior statement that no staging
occurred. They created no commit or Git history. Their index path set exactly
matched the P12.2 manifest plus five documented legal/provenance files, and the
working files matched the index. P12.C1 removed the index with the invalid
repository and did not use reset, clean, restore, checkout, `git rm`, rebase,
amend or history rewrite.

Top-level directories observed without source execution or content inspection:

```text
.github
.plans
acp_adapter
acp_registry
agent
apps
assets
cron
hermes_cli
infographic
locales
nix
optional-mcps
optional-skills
packaging
plugins
providers
scripts
skills
tests
tools
tui_gateway
ui-tui
web
website
```

Top-level filenames observed:

```text
.dockerignore
.env.example
.envrc
.gitattributes
.gitignore
.hadolint.yaml
.mailmap
AGENTS.md
batch_runner.py
cli-config.yaml.example
cli.py
constraints-termux.txt
CONTRIBUTING.es.md
CONTRIBUTING.md
docker-compose.windows.yml
docker-compose.yml
Dockerfile
flake.lock
flake.nix
hermes
hermes-already-has-routines.md
hermes_bootstrap.py
hermes_constants.py
hermes_logging.py
hermes_state.py
hermes_time.py
LICENSE
MANIFEST.in
mcp_serve.py
mini_swe_runner.py
model_tools.py
NOTICE
package-lock.json
package.json
pyproject.toml
README.es.md
README.md
README.ur-pk.md
README.zh-CN.md
run_agent.py
SECURITY.es.md
SECURITY.md
setup-hermes.sh
setup.py
SOURCE_EXCLUSIONS.tsv
SOURCE_IMPORT_MANIFEST.tsv
THIRD_PARTY_NOTICES.md
toolsets.py
toolset_distributions.py
trajectory_compressor.py
UPSTREAM_PROVENANCE.md
utils.py
uv.lock
```

## 7. Legal and Provenance File Metadata

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `SOURCE_IMPORT_MANIFEST.tsv` | 1,508,338 | `AEBB672A7CC33C6FB93CD4B8D4A4CAFED1023B22E13ACDCE92D9248CB65D0E9A` |
| `SOURCE_EXCLUSIONS.tsv` | 9,733 | `20E1DDE4F73AF5EE4B67255D6C4B8CB265B4BC142C57806D3F98F9EC0440426C` |
| `UPSTREAM_PROVENANCE.md` | 2,941 | `3D3C3E48F4F0ABB88195FE9C1498ECE1CE3E1C76FA7E5E31B20C86D856CADAFC` |
| `NOTICE` | 1,504 | `F7CA844C0B23C2403D162D5ECD9748E68ADAD9A73A763339D8FB59AB16857412` |
| `THIRD_PARTY_NOTICES.md` | 4,988 | `07B127BB2C577B2F7B6EFBE985EED01734FC109B012CD8FDC2EA3DD1107C9FD3` |

No credential, `.env` value, token, browser state, provider configuration or
unrelated user content was printed or inspected. `.env.example` and `.envrc`
were observed only as manifest filenames and hash-validated files.

## 8. Manifest Comparison

```yaml
P12_2_ManifestComparison:
  source_import_manifest_rows: 6111
  source_exclusion_rows: 60
  legal_provenance_paths_added: 5
  expected_files: 6116
  actual_files: 6116
  index_files: 6116
  missing_files: 0
  additional_files: 0
  index_missing_files: 0
  index_additional_files: 0
  manifest_hash_mismatches: 0
  excluded_paths_present: 0
  unsafe_manifest_paths: 0
  duplicate_manifest_paths: 0
```

Every imported source path matched its recorded `product_sha256`. The complete
actual and index path sets equaled the 6,111 manifest paths plus
`SOURCE_IMPORT_MANIFEST.tsv`, `SOURCE_EXCLUSIONS.tsv`, `UPSTREAM_PROVENANCE.md`,
`NOTICE` and `THIRD_PARTY_NOTICES.md`. No wildcard assumption was used.

## 9. Commit and Remote Status

HEAD was unborn and commit count was zero, so there were no commit SHAs,
subjects or paths to classify. There were no branch refs, tags, remote-tracking
refs or reflog entries. The only remote was `upstream`, with the official fetch
URL and literal push URL `DISABLED`. `origin` and branch tracking were absent.

The absence of commits and refs, absence of a writable remote, disabled only
push URL and empty reflog provide no evidence of a successful push and no
locally pushable product history.

## 10. Ownership Proof

```yaml
P12_C1_OwnershipProof:
  exact_p12_1_created_root: true
  repository_initialization_matches_p12_1: true
  filesystem_matches_p12_2_manifest_and_legal_files: true
  index_matches_p12_2_manifest_and_legal_files: true
  imported_source_hashes_match_manifest: true
  unrelated_human_file_found: false
  unrelated_commit_found: false
  writable_origin_found: false
  successful_push_evidence_found: false
  linked_worktree_found: false
  submodule_found: false
  reparse_point_outside_git_found: false
  active_process_found_at_deletion_gate: false
  ownership_proof_marker: P12_C1_OWNERSHIP_PROVEN
  deletion_authorized: true
```

## 11. Deletion Decision and Command

All stop rules were false after the target, manifest, hash, index, Git,
worktree, submodule, reparse, process, protected-root and locked-upstream guards
were rerun in the same fail-closed deletion command. Deletion was authorized for
the exact literal root only.

```powershell
Remove-Item `
  -LiteralPath "C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES" `
  -Recurse `
  -Force `
  -ErrorAction Stop
```

No variable-based wildcard, parent deletion, `git clean`, reset, checkout,
restore or `git rm` was used.

## 12. Post-Deletion Validation

```yaml
P12_C1_PostDeletionValidation:
  misplaced_root_exists: false
  protected_agent_platform_exists: true
  protected_agent_platform_git_root: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM
  protected_agent_platform_git_root_unchanged: true
  locked_upstream_exists: true
  locked_upstream_head: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  locked_upstream_status: clean
  sibling_replacement_created: false
  alternative_product_root_created: false
  process_or_handle_match_for_removed_root: 0
```

## 13. Canonical-Record Corrections

P12.1 now has current status:

```text
rolled_back_due_to_unauthorized_out_of_workspace_product_root
```

Its sibling-root decision is invalid, its material repository topology is
removed, its upstream reference is unchanged, it is reopened and not accepted,
and P12.C2 must redefine the topology.

P12.2 now has current status:

```text
rolled_back_due_to_invalid_product_root
```

Its legal filtering logic remains useful evidence, but the material snapshot,
legal files and staged index were removed with the invalid root. No current
product snapshot or product legal baseline commit exists. P12.2 is reopened and
must be executed again after corrected P12.1.

Historical evidence remains in both records but readiness markers and current
verdicts that implied the external product root remained valid were superseded.

## 14. Upstream No-Touch Validation

Before and after deletion, the locked upstream existed at
`4_external/sources/hermes-agent`, HEAD equaled
`9de9c25f620ff7f1ce0fd5457d596052d5159596`, and `git status --short` was empty.
No checkout, reset, clean, merge, rebase, stash, commit, tag, fetch, pull, push
or source write occurred there.

## 15. Remaining Blockers and P12.C2 Readiness

P12.C2 may now define the corrected product topology within the human-authorized
workspace. P12.C1 does not define or create that topology.

Execution order is mandatory:

```text
P12.C2 corrected topology definition
corrected and reaccepted P12.1
reexecuted and reaccepted P12.2
only then P12.3 or later productization execution
```

Mixed-license, SBOM, asset, trademark, redistribution and publication blockers
recorded by P12.2 remain evidence for its future reexecution.

## 16. Created / Modified / Deleted Register

Created:

```text
0_architecture/governance/agent_platform_hermes_misplaced_product_root_rollback.md
```

Modified in place:

```text
0_architecture/governance/agent_platform_hermes_controlled_fork_repository_topology.md
0_architecture/governance/agent_platform_hermes_license_exclusion_notice_baseline.md
```

Deleted after ownership proof:

```text
C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES\
  complete invalid repository, .git metadata, 6111 imported files and 5 legal/provenance files
```

Not modified:

```text
0_architecture/governance/agent_platform_hermes_architecture_mapping.md
4_external/sources/hermes-agent/**
AGENT PLATFORM Git history and index
.opencode/
AGENTS.md
credentials, secrets, .env values, OAuth, browser state and provider configuration
```

No retry, safe-block, diagnostic or cleanup-report Markdown was created.

## 17. Final Verdict

```yaml
P12_C1_FinalVerdict:
  misplaced_root_identified: true
  ownership_proven: true
  unrelated_human_work_found: false
  writable_remote_or_push_found: false
  misplaced_root_removed: true
  agent_platform_preserved: true
  locked_upstream_unchanged: true
  p12_1_material_result_valid: false
  p12_2_material_result_valid: false
  p12_1_reopened: true
  p12_2_reopened: true
  p11_2_affected: false
  P12_C2_may_proceed: true
```

```text
hermes_misplaced_product_root_incident_recorded
hermes_p12_1_material_result_rolled_back
hermes_p12_2_material_result_rolled_back
hermes_external_product_root_removed
hermes_agent_platform_root_preserved
hermes_locked_upstream_reference_unchanged
hermes_topology_redefinition_required
no_git_history_rewrite
no_remote_network_operation
no_credentials_inspected
```
