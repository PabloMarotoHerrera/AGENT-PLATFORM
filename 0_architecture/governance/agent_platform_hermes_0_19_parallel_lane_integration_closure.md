# P15.M4R - Hermes 0.19 Parallel-Lane Integration Closure

Status: P15.M4R parallel-lane integration closed with constraints.

Final verdict: `hermes_0_19_parallel_lane_integration_closed_with_constraints`

## Ticket Authority

P15.M4R validates and closes the integration of three parallel migration lanes:

- P15.M2 and P15.M2A licensing and V2 re-attestation;
- P15.M3 dependency and lock reconciliation;
- P15.M4 Desktop and Workspace productization decision.

P15.M4R is an integration-governance ticket. It verifies the integrated branch, source-branch ancestry, exact integrated artifact set, canonical V2 integrity, the dedicated integrity tests, the three TSV manifests, cross-document authority consistency and repository integrity.

Authorized P15.M4R candidate:

| Path | Disposition |
| --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_parallel_lane_integration_closure.md` | created durable integration-closure record |

P15.M4R does not modify any existing P15.M2A, P15.M3 or P15.M4 artifact. It does not modify either product, manifests, lockfiles, scripts, tests, external sources, Graphify output or runtime state.

Forbidden actions preserved:

- no dependency installation;
- no registry query;
- no lockfile regeneration;
- no product build, lint, typecheck or product test;
- no Pepper, Desktop or Workspace startup;
- no Docker or Compose startup;
- no WSL mutation;
- no VPS provisioning;
- no OAuth flow;
- no credential read;
- no provider call;
- no inference;
- no Graphify command;
- no staging, commit, push, stash, reset, clean, worktree, merge or rebase command by OpenCode.

The canonical integrity utility and dedicated governance test suite are authorized validation and are not product execution.

## Integration Worktree

| Field | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| Dynamic integration HEAD | `114c88a9c8b33d48ef14b5c93f1754cac0b47b45` |
| Branch remote | `origin/p15.m-hermes-0.19-migration` |
| Branch remote HEAD | `114c88a9c8b33d48ef14b5c93f1754cac0b47b45` |
| HEAD equals branch remote | `true` |
| Index empty at start | `true` |
| Staged files at start | `0` |
| Tracked worktree clean at start | `true` |
| Visible untracked task candidates at start | `0` |

Required common P15.M1D baseline:

```text
525e1a13a0199e7648ccc332c1c06103bc269aaf
```

## Source Branch Heads And Ancestry

| Source branch | Remote head | Contains P15.M1D | Is ancestor of integration HEAD |
| --- | --- | --- | --- |
| `origin/p15.m2-license-notice` | `d1c5f52c2dc5cb48361412f059c3d4520ec83b33` | `true` | `true` |
| `origin/p15.m3-dependency-lock` | `2f74cc3064ac475f85c3831d446be1800e0d06f2` | `true` | `true` |
| `origin/p15.m4-desktop-workspace-decision` | `204204c60f0918cec26228ca7cea053804fba6d6` | `true` | `true` |

Merge ancestry result: `all_parallel_lanes_integrated`.

## Integrated Artifacts

P15.M2A licensing artifacts:

| Path | Status |
| --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_license_manifest.tsv` | tracked, committed in HEAD, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_license_notice_reconciliation.md` | tracked, committed in HEAD, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_license_notice_v2_reattestation.md` | tracked, committed in HEAD, locally unmodified, unstaged |

P15.M3 dependency artifacts:

| Path | Status |
| --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_dependency_lock_manifest.tsv` | tracked, committed in HEAD, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_dependency_lock_reconciliation.md` | tracked, committed in HEAD, locally unmodified, unstaged |

P15.M4 Desktop and Workspace artifacts:

| Path | Status |
| --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_desktop_workspace_manifest.tsv` | tracked, committed in HEAD, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_desktop_workspace_productization_decision.md` | tracked, committed in HEAD, locally unmodified, unstaged |

Integrated artifact set validation:

| Check | Result |
| --- | --- |
| Required integrated artifacts | `7` |
| Actual integrated artifacts since P15.M1D | `7` |
| Missing integrated artifacts | `0` |
| Unexpected integrated artifacts | `0` |
| Diff under protected non-governance paths since P15.M1D | `0` |

The exact integrated set since P15.M1D is limited to the seven governance artifacts above.

## Canonical V2 Integrity

Canonical utility:

```text
10_scripts/governance/pepper_baseline_integrity.py
```

Exact command used:

```text
python 10_scripts/governance/pepper_baseline_integrity.py --repo-root . --product-root 2_products/pepper-agent --mode all --format json
```

Result:

| Scope | Algorithm | Files | Bytes | SHA-256 |
| --- | --- | ---: | ---: | --- |
| Candidate | `agent-platform-git-tree-sha256-v2` | 6684 | 148145642 | `fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b` |
| Payload | `agent-platform-git-tree-sha256-v2` | 6681 | 145406255 | `3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073` |
| Baseline record | `sha256-git-blob-v1` | not_applicable | 25333 | `5aa7d9582e8036e66a9a81be772aa75b3cb930a978c0128bc0a6b2585baa0fea` |

Dedicated integrity tests:

```text
python -m unittest discover -s 12_tests/governance -p test_pepper_baseline_integrity.py
```

Result:

```yaml
tests_run: 14
failures: 0
errors: 0
result: OK
```

## Manifest Validation

Manifest validation used committed HEAD blob bytes for SHA-256 identity. This avoids checkout EOL realization differences and matches the integrated governance identities.

| Manifest | Data rows | Columns | SHA-256 | Duplicate IDs | Blank mandatory fields | Invalid classifications |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| `0_architecture/governance/agent_platform_hermes_0_19_license_manifest.tsv` | 30 | 17 | `5643d432579493a467aec17c0caf742f19d0f5bb9d9e54119b3c67c0845605fb` | 0 | 0 | 0 |
| `0_architecture/governance/agent_platform_hermes_0_19_dependency_lock_manifest.tsv` | 3920 | 25 | `a2e9c734494a294b65c3785edf5c06c5f3e1939fa7b084d6b1d9681cc1c368f5` | 0 | 0 | 0 |
| `0_architecture/governance/agent_platform_hermes_0_19_desktop_workspace_manifest.tsv` | 80 | 25 | `bee425d12235fccc49d12d755852100be4ccd3a9e7fd6b6f548ead689e3f3747` | 0 | 0 | 0 |

Desktop and Workspace manifest-specific validation:

| Check | Result |
| --- | ---: |
| invalid overlap classifications | 0 |
| invalid adoption dispositions | 0 |
| adopt_now rows | 0 |
| unclassified Desktop surfaces | 0 |
| unclassified Workspace surfaces | 0 |
| unclassified route overlaps | 0 |
| unclassified current assets | 0 |
| unclassified promotion blockers | 0 |

## Cross-Document Authority Matrix

Required integrated authority is consistent across P15.M2A, P15.M3 and P15.M4.

| Authority | Integrated disposition |
| --- | --- |
| Pepper P13 | `canonical_product_UI` |
| Hermes Web Dashboard | `route_by_route_reference_only` |
| Hermes Desktop | `disabled_future_governed_local_client_candidate` |
| Hermes Workspace | `ignored_reference_only_future_adjacent_operations_candidate` |
| P13 replacement | `rejected` |
| Workspace import | `unauthorized` |
| Desktop enablement | `unauthorized` |
| Desktop binary distribution | `unauthorized` and `blocked_pending_review` |
| Workspace deployment | `unauthorized` |
| Container publication | `unauthorized` and `blocked_pending_review` |
| Public Pepper branding | `blocked_pending_trademark_review` |
| Dependency installation | `unauthorized` |
| Lock regeneration | `unauthorized` |
| Native Hermes updater | `non_authoritative`; future adaptation required |
| Future update authority | `P15.M17_and_P15.M18` |
| Provider and OAuth terms | `separate_and_not_authorized` |
| Contradictions | `0` |

## Preserved Licensing Restrictions

| Restriction | Integrated disposition |
| --- | --- |
| internal source development | `ready` |
| modified source redistribution | `ready_with_notices` |
| Desktop binary redistribution | `blocked_pending_review` |
| Dashboard built asset redistribution | `blocked_pending_review` |
| container image publication | `blocked_pending_review` |
| public Pepper branding | `blocked_pending_trademark_review` |
| provider and OAuth terms | `separate_terms_required` |

No `THIRD_PARTY_NOTICES.md` is created by P15.M4R. Product notice application remains dependency-gated.

## Preserved Dependency Restrictions

| Restriction | Integrated disposition |
| --- | --- |
| dependency installation authorized | `false` |
| lockfile regeneration authorized | `false` |
| package registry queries | `0` |
| dependency or lock application | `unauthorized` |
| native Hermes updater | `non_authoritative`; adapt to governed updater later |
| generated bundle rebuild | `unauthorized` |
| container realization | `blocked_pending_digest_pinning_and_P15.M10` |

## Preserved Desktop And Workspace Dispositions

| Surface | Integrated disposition |
| --- | --- |
| Pepper P13 | remains canonical product UI |
| Hermes Web Dashboard | route-by-route reference only |
| Hermes Desktop | disabled; future governed local-client candidate only |
| Hermes Workspace 2.3.0 | ignored and reference-only future adjacent-operations candidate |
| Desktop enablement | unauthorized |
| Workspace import | unauthorized |
| Workspace shell replacement | rejected and unauthorized |
| Workspace deployment | unauthorized |

## Repository Integrity

Protected path diff since P15.M1D:

| Scope | Changes |
| --- | ---: |
| Pepper product | 0 |
| Pepper register and baseline metadata | 0 |
| Current product | 0 |
| Current register and baseline metadata | 0 |
| External source tracked files | 0 |
| Dependency and lock files | 0 |
| `3_platform` | 0 |
| `10_scripts` | 0 |
| `12_tests` | 0 |
| `AGENTS.md` | 0 |
| `graphify-out` | 0 |
| `9_artifacts` | 0 |

Runtime and external actions by P15.M4R:

| Action | Count |
| --- | ---: |
| Graphify commands | 0 |
| dependency installations | 0 |
| registry queries | 0 |
| builds | 0 |
| product tests | 0 |
| Desktop starts | 0 |
| Workspace starts | 0 |
| Docker or Compose starts | 0 |
| WSL mutations | 0 |
| OAuth flows | 0 |
| credential reads | 0 |
| provider calls | 0 |
| inference calls | 0 |

## P15.M5 Entry Conditions

P15.M5 may start only after this P15.M4R closure record is reviewed, committed and pushed by the human.

P15.M5 entry conditions preserved by P15.M4R:

- P15.M2A, P15.M3 and P15.M4 are integrated into `p15.m-hermes-0.19-migration`;
- all seven integrated artifacts are present and committed;
- canonical V2 product identity remains unchanged;
- the three TSV manifests validate;
- Pepper P13 remains product UI authority;
- Desktop remains disabled;
- Workspace remains unimported;
- dependency and lock application remains unauthorized;
- public binary and container distribution remain unauthorized;
- live OAuth, provider calls and inference remain unauthorized.

## Rollback And Rejection

If P15.M4R is rejected, the rejection is limited to this closure record unless a human separately reopens the manual integration commits.

Rollback posture:

- do not revert P15.M2A, P15.M3 or P15.M4 artifacts automatically;
- do not mutate products or source roots;
- do not stage, commit or push by agent;
- re-run the same ancestry, artifact-set, V2, manifest and authority checks after any human correction;
- stop with the named blocker if any gate fails.

## Final Validation

| Check | Result |
| --- | --- |
| Markdown trailing whitespace | `0` expected for this record at final validation |
| `git diff --check` | clean expected at final validation |
| Candidate files | exactly `1` authorized untracked closure record expected |
| Unexpected candidate files | `0` expected |
| Index | empty expected |
| Staged files | `0` expected |
| Commits by OpenCode | `0` |
| Pushes by OpenCode | `0` |

P15.M4R is ready for human review and commit.
