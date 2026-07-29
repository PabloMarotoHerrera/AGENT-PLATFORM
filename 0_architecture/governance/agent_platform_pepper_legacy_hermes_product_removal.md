# P15.C3 - Legacy Hermes Product Removal

## Authority

| Field | Value |
| --- | --- |
| Ticket | P15.C3 |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM` |
| Branch | `p15.cleanup-canonicalization` |
| HEAD at execution | `808eae5b587ce0c437e24852ffb4f4c7b550cc16` |
| Remote head | `808eae5b587ce0c437e24852ffb4f4c7b550cc16` |
| P15.C3B commit | `808eae5b587ce0c437e24852ffb4f4c7b550cc16` |
| P15.C3B message | `P15.C3B Canonicalize active legacy product references` |
| P15.C3B verdict | `hermes_0_19_pepper_active_legacy_references_canonicalized_with_historical_evidence_preserved` |
| P15.C3B candidate files | `16` |
| Index state | empty before deletion; no staged files |

P15.C3 removes the retained legacy product root from the current working tree
after P15.C3B canonicalized active first-party references. Historical and
provenance records remain intact and continue to provide Git recoverability and
audit context.

## Canonical Product Authority

| Field | Value |
| --- | --- |
| Canonical product | `2_products/pepper-agent` |
| Canonical upstream | Hermes Agent 0.19.0 |
| Canonical upstream tag | `v2026.7.20` |
| Canonical upstream commit | `3ef6bbd201263d354fd83ec55b3c306ded2eb72a` |
| Legacy product removed | `2_products/hermes-agent` |
| Legacy upstream | Hermes Agent 0.18.2 |
| Legacy upstream tag | `v2026.7.7.2` |
| Legacy upstream commit | `9de9c25f620ff7f1ce0fd5457d596052d5159596` |
| Legacy current authority | false |
| Legacy execution target | false |
| Legacy test target | false |
| Legacy build target | false |
| Removal authority | P15.C3 |

## Pepper Integrity

Pre-change and post-deletion Pepper identity matched exactly:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate | `6831` | `149941138` | `2735cb45f0e087cc9dd2901ae5c1140e89ddcee886d526b0d2fbf253a13d9e50` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | n/a | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Pepper root remained present and had zero status entries after deletion.

## Legacy Tracked Inventory

| Field | Value |
| --- | --- |
| Tracked files | `6246` |
| Tracked bytes | `134403219` |
| Tracked SHA-256 | `2981fe08c44ec18646118a23ccbbaee5fdfb3450d6679b1a6ff45c52edfba5e1` |
| Product-relative SHA-256 | `486490b0b8e6ee2fe4e7a262d5a9ea8b036259c669bb6ee99ba6fe3f546b16d0` |
| Git tree object | `206d700d688c4130434c145b61c7e8a286632516` |
| First tracked path | `2_products/hermes-agent/.dockerignore` |
| Last tracked path | `2_products/hermes-agent/website/tsconfig.json` |
| Paths outside legacy root | `0` |
| Duplicate tracked paths | `0` |
| Missing tracked files before deletion | `0` |

## Git Recoverability

| Field | Value |
| --- | --- |
| Legacy tree present in HEAD | true |
| Legacy tree files in HEAD | `6246` |
| Legacy tree object resolvable | true |
| P15.C3B parent history resolvable | true |
| Origin P15M history resolvable | `da5deea2db860e8b50c805a9d2b8ed27495c5627` |
| P15.1A history resolvable | `fea7d3963a598b848768671e00d5bad8065a4421` |
| External backup required for tracked recovery | false |

Tracked recovery remains available from Git history with a scoped restore of the
legacy product path before human staging, if rollback is required. No backup
branch, tag, repository ZIP or duplicate product copy was created.

## Residue Inventory

| Field | Value |
| --- | ---: |
| Physical file count, including internal reparse alias paths | `115222` |
| Non-following regular file entries | `115217` |
| Internal reparse alias file paths | `5` |
| Physical bytes | `1832615457` |
| Tracked files | `6246` |
| Visible untracked files | `0` |
| Ignored untracked files | `108976` |
| Untracked and ignored residue count | `108976` |
| Accounting formula matched | true |
| Temporary manifest path | outside repository under `C:/Users/pablo/AppData/Local/Temp/opencode/p15c3-inventory-808eae5` |
| Manifest rows | `108976` |
| Manifest algorithm | `agent-platform-legacy-residue-path-size-sha256-v1` |
| Manifest SHA-256 | `89a286de59754cf82ce35bf204a88095ce470cc467c2bbdbd3490487ff85cb39` |

Residue classification counts:

| Classification | Files |
| --- | ---: |
| `frontend_dependency` | `94378` |
| `virtual_environment_dependency` | `13252` |
| `Python_bytecode_or_cache` | `1064` |
| `tool_cache` | `137` |
| `generated_desktop_distribution` | `80` |
| `generated_desktop_build` | `28` |
| `generated_web_bundle` | `21` |
| `test_cache_or_duration_output` | `7` |
| `generated_package_metadata` | `6` |
| `other_generated_artifact` | `2` |
| `TypeScript_build_state` | `1` |
| `unknown` | `0` |

Safety classification:

| Field | Value |
| --- | ---: |
| Classified residue files | `108976` |
| Unknown files | `0` |
| Untracked user-authored source outside generated roots | `0` |
| Untracked governance files | `0` |
| Untracked product configuration outside generated roots | `0` |

## Credential And User-Data Safety

Suspicious path-name matches were evaluated by path and generated-root location
only. Secret-shaped contents were not printed, and no real `auth.json` was
inspected.

| Field | Value |
| --- | ---: |
| Suspicious path matches | `522` |
| Matches inside generated roots | `522` |
| Matches outside generated roots | `0` |
| Real auth files | `0` |
| Real credential files | `0` |
| Real private keys | `0` |
| Real session databases | `0` |
| Real user databases | `0` |
| Real user documents | `0` |

## Reparse Safety

Six directory reparse entries were found. All normalized targets resolve inside
the exact legacy root.

| Path | Target inside legacy root |
| --- | --- |
| `2_products/hermes-agent/node_modules/hermes` | true |
| `2_products/hermes-agent/node_modules/hermes-tui` | true |
| `2_products/hermes-agent/node_modules/web` | true |
| `2_products/hermes-agent/node_modules/@hermes/bootstrap-installer` | true |
| `2_products/hermes-agent/node_modules/@hermes/ink` | true |
| `2_products/hermes-agent/node_modules/@hermes/shared` | true |

| Field | Value |
| --- | ---: |
| Reparse points | `6` |
| Reparse points resolving outside legacy root | `0` |
| Parent traversal targets | `0` |
| Repository root targets | `0` |
| Pepper targets | `0` |
| Omniverse targets | `0` |
| External worktree targets | `0` |

## Deletion

| Field | Value |
| --- | --- |
| Exact target | `C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM/2_products/hermes-agent` |
| Direct parent | `C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM/2_products` |
| Target was repository child | true |
| Target equaled repository root | false |
| Target equaled products root | false |
| Target equaled Pepper root | false |
| Target equaled Omniverse root | false |
| Target was reparse point | false |
| Deletion method | bounded recursive filesystem deletion of the exact literal path |

Post-deletion state:

| Field | Value |
| --- | ---: |
| Legacy root exists | false |
| Legacy files remaining | `0` |
| Legacy directories remaining | `0` |
| Tracked legacy paths present on disk | `0` |
| Visible legacy untracked files | `0` |
| Ignored legacy untracked files | `0` |
| Tracked files deleted | `6246` |
| Residue files deleted | `108976` |
| Pepper root present | true |
| Omniverse root present | true |
| Products root present | true |

## Active Reference Posture

Pre-deletion active-reference scan outside the removed legacy product, external
source, `.opencode`, `graphify-out` and unrelated Omniverse roots reported:

| Category | Count |
| --- | ---: |
| Active executable references | `0` |
| Active test references | `0` |
| Active configuration references | `0` |
| Active ignore-rule references | `0` |
| Active build or quality-gate references | `0` |
| Active Graphify refresh references | `0` |
| Unclassified references | `0` |
| Historical governance references | `440` |
| Historical product provenance references | `127` |
| Read-only migration history references | `18` |

Historical and provenance references are retained. Graphify remains frozen and
was not executed.

## Regression Evidence

| Suite | Result |
| --- | --- |
| Root focused quality-gate suite | `39` passed, `0` failed, `0` errors |
| Runtime lifecycle gate subset | `11` included in root suite, `0` failed, `0` errors |
| Pepper provider, credential, accounting, failure and controlled-gate suite | `219` passed, `0` failed, `0` errors |
| P15.C1/P15.C2 smoke tests | `9` passed, `0` failed, `0` errors |
| Native Windows credential protection smoke | `pepper_windows_credential_store_protection_smoke_passed` |
| Native credential-store root layout smoke | `pepper_credential_store_root_layout_smoke_passed` |
| Governance integrity tests | `14` passed, `0` failed, `0` errors |

Inherited Pydantic protected-namespace warnings remained in the root/provider
test output. No new warning class was introduced by deletion.

## Omniverse Non-Mutation

The unrelated `2_products/omniverse-app` source remains untracked, unresolved
and preserved for P15.CR.

| Field | Value |
| --- | ---: |
| Frozen visible untracked files before deletion | `369` |
| Inventory files after deletion | `369` |
| Inventory paths pre equals post | true |
| File hashes pre equals post | true |
| Files modified | `0` |
| Files deleted | `0` |
| Files created | `0` |
| Files staged | `0` |
| Inventory SHA-256 | `150dac7affdc39c8014cb4365d37bf85590fce4fa7ef286748c14dcdb0e2602a` |

## Auxiliary Worktrees

| Worktree | State |
| --- | --- |
| P15.1A HEAD | `fea7d3963a598b848768671e00d5bad8065a4421` |
| P15.1A candidate count | `6` |
| P15.1A candidate set unchanged | true |
| P15.1A source hash mismatches | `0` from P15.C1 authority |
| P15.1A legacy root exists | true |
| P15M HEAD | `da5deea2db860e8b50c805a9d2b8ed27495c5627` |
| P15M worktree clean | true |
| Files modified outside primary worktree by P15.C3 | `0` |
| Commits outside primary branch | `0` |
| Pushes outside primary branch | `0` |

## Operational And Secret Safety

| Counter | Value |
| --- | ---: |
| Real credential reads | `0` |
| Real credential writes | `0` |
| Credential leases | `0` |
| Credential refreshes | `0` |
| Credential rotations | `0` |
| Credential copies | `0` |
| Credential moves | `0` |
| Credential deletes | `0` |
| OAuth attempts | `0` |
| Provider dispatches | `0` |
| Provider streams | `0` |
| Worker dispatches | `0` |
| Real runtime starts | `0` |
| Docker actions | `0` |
| Remote host actions | `0` |
| Graphify commands | `0` |
| Graphify output changes | `0` |
| Git stage | `0` |
| Git commit | `0` |
| Git push | `0` |

Retained real secret category counts in P15.C3 candidates are all zero:
access tokens, refresh tokens, authorization headers, OAuth codes, credential
contents, real auth-file contents, private keys, raw provider responses, raw
prompts and reasoning traces.

## Candidate Formula

Authorized P15.C3 candidate formula:

```text
6246 tracked deletions
+ 1 governance file
= 6247 scoped candidates
```

All tracked deletions begin with `2_products/hermes-agent/`. There are no
authorized Pepper, Omniverse, external source, Graphify output, script, test or
ignore-file candidates. The 369 Omniverse files are frozen unrelated content and
not P15.C3 candidates.

## P15.CR Handoff

P15.CR begins only after human review, commit and push of P15.C3. P15.CR owns
cleanup closure, main integration, confirmation that Pepper is the only tracked
editable Hermes-derived product, auxiliary worktree disposition after main
integration, and resolution of the unrelated Omniverse source before declaring
the primary worktree operationally clean. P16 remains blocked until P15.CR.

## Residual Constraints

| Field | Value |
| --- | --- |
| Legacy Hermes product | removed from current working tree |
| Legacy Hermes history | retained in Git |
| Pepper canonical product | true |
| Product UI | disabled |
| Extension modules | `[]` |
| Runtime routes | `0` |
| Navigation items | `0` |
| Graphify | frozen read-only |
| Graphify refresh utility | absent |
| P15.1A worktree | retained until P15.CR and main integration |
| P15M worktree | retained until P15.CR and main integration |
| Omniverse app | pre-existing untracked source, retained, unresolved until P15.CR |
| Real legacy credential store migrated | false |
| Legacy credential root compatibility | retained |
| Automatic store migration | absent |
| Credential refresh | disabled |
| Credential rotation | disabled |
| Provider fallback | disabled |
| Automatic retry | disabled |
| Tools | disabled |
| MCP | disabled |
| Cleanup integrated into main | false |
| P16 | blocked until P15.CR |
| Production readiness | not claimed |

## Final Verdict

```text
hermes_0_19_pepper_legacy_product_removed_with_canonical_authority_preserved
```
