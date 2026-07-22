# P15.M0 - Hermes 0.19 Migration Adoption Authorization

Status: P15.M0 migration authorization ready with constraints.

Final verdict: `hermes_0_19_migration_authorized_with_constraints`

## Ticket Authority

P15.M0 ratifies the accepted P15.U adoption assessment and establishes the binding migration authority for moving Pepper from its current Hermes Agent 0.18.2-derived product baseline to a new editable Hermes Agent 0.19.0 baseline.

P15.M0 is governance-only. It authorizes verification, ratification and one canonical authorization record only.

P15.M0 authorizes:

- verification of the committed P15.U0 source lock;
- verification of the committed P15.U adoption assessment;
- ratification of the selected migration architecture;
- freezing exact Hermes Agent 0.19.0 source identity;
- freezing migration workstream and dependency order;
- freezing local, fallback and future deployment targets;
- freezing P15.0 through P15.4 dispositions;
- defining current-product and migration-candidate authority;
- defining human approval and rollback gates;
- creating this canonical migration-authorization document.

P15.M0 does not authorize:

- creating the new editable product baseline;
- copying Hermes Agent 0.19.0 into `2_products`;
- modifying the current Pepper product;
- modifying the modification register;
- modifying external source trees;
- installing dependencies;
- modifying manifests or lockfiles;
- running builds or tests;
- starting Hermes Agent, Desktop, Dashboard or Workspace;
- starting Docker;
- mutating WSL;
- provisioning a VPS;
- running OAuth;
- reading credentials;
- calling a provider;
- performing inference;
- running Graphify;
- staging, committing or pushing.

Binding interpretation:

```text
hermes_0_19_migration_authorized_with_constraints

A ready verdict means the migration program is authorized and P15.M1 is unlocked.

It does not mean the new product baseline exists, Hermes 0.19.0 has been copied into the product, dependencies have been reconciled, Pepper has been executed, Desktop or Workspace has been adopted, Docker or WSL runtime validation has begun, OAuth or inference has been authorized, or Graphify has run.
```

## Worktree Authority

Authorized worktree:

```yaml
repository_root: C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15U
branch: p15.u-hermes-adoption-assessment
```

The historical checkout at `C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM` remains outside P15.M0 authority. It was not inspected, copied, modified, cleaned, reset, stashed, reconciled, removed or converted into a worktree by P15.M0.

The paused historical P15.4 candidate may be considered only through the already accepted disposition `selectively_forward_port`. No direct file copying is authorized.

## Instruction Precedence

P15.M0 task authority overrides generic workflow instructions where they conflict with this boundary.

Prohibited generic workflow categories:

- Graphify execution;
- dependency installation;
- source execution;
- broad product mutation;
- repository cleanup;
- Git staging;
- Git commits;
- Git pushes;
- worktree creation.

Graphify policy:

```yaml
Graphify_execution: prohibited
Graphify_evidence: read_only_when_present
Graphify_cache: non_authoritative
Graphify_commands_executed_by_P15_M0: 0
Graphify_modifications_by_P15_M0: 0
```

The following commands remain prohibited by P15.M0:

```text
graphify update
10_scripts/graphify/refresh_hermes_graph.py
```

## Dynamic Start State

Read-only Git validation used command-scoped `safe.directory` because Git reported the repository as dubious ownership for this Windows user. No global, local or repository Git configuration was changed.

```yaml
P15_M0_DynamicStartState:
  repository_root: C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15U
  branch: p15.u-hermes-adoption-assessment
  dynamic_start_SHA: 97f650c5d8dceeefd23d9b2dd5d38821ebedaa6c
  branch_remote: origin/p15.u-hermes-adoption-assessment
  branch_remote_SHA: 97f650c5d8dceeefd23d9b2dd5d38821ebedaa6c
  origin_main_SHA: fea7d3963a598b848768671e00d5bad8065a4421
  HEAD_equals_branch_remote: true
  origin_main_is_ancestor_of_HEAD: true
  index_empty: true
  staged_files: 0
  tracked_working_tree_clean: true
  status_porcelain_count_at_start: 0
```

P15.M0 does not require `HEAD == origin/main`. P15.U0 and P15.U are expected committed records on `p15.u-hermes-adoption-assessment`.

## Mandatory Prerequisites

Required prerequisite records:

| Prerequisite | Path | Required verdict | Last commit | Integrity |
| --- | --- | --- | --- | --- |
| P15.U0 source lock | `0_architecture/governance/agent_platform_hermes_0_19_workspace_source_lock.md` | `hermes_0_19_workspace_sources_locked` | `7b16d694844e895c8c118528675cbc0c656093df` | tracked, present in `HEAD`, unmodified, unstaged |
| P15.U adoption assessment | `0_architecture/governance/agent_platform_hermes_0_19_workspace_adoption_assessment.md` | `hermes_0_19_workspace_adoption_assessment_ready_with_constraints` | `97f650c5d8dceeefd23d9b2dd5d38821ebedaa6c` | tracked, present in `HEAD`, unmodified, unstaged |
| P12.5 update strategy | `0_architecture/governance/agent_platform_hermes_upstream_synchronization_strategy.md` | `upstream_synchronization_strategy_ready` | `dcc110229e2fbc7e45095a129ced3976793b5200` | tracked, present in `HEAD`, unmodified, unstaged |

Prerequisite verdicts were found exactly as required. P15.M0 is not blocked by source-lock absence, adoption-assessment absence or prerequisite integrity drift.

## Locked Source Authority

P15.M0 ratifies these exact external-source identities from P15.U0 and P15.U.

| Source | Repository | Version | Tag | Commit | Tree SHA-256 | Role |
| --- | --- | --- | --- | --- | --- | --- |
| Hermes Agent historical reference | `https://github.com/NousResearch/hermes-agent` | `0.18.2` | `v2026.7.7.2` | `9de9c25f620ff7f1ce0fd5457d596052d5159596` | `6038ff8d40235109dcf85ad8751b050700b31b9fcfb438915f437a91b3292849` | historical comparison and rollback evidence |
| Hermes Agent selected baseline source | `https://github.com/NousResearch/hermes-agent` | `0.19.0` | `v2026.7.20` | `3ef6bbd201263d354fd83ec55b3c306ded2eb72a` | `ca41c8c6c688f7a8e94c238cecb45cb60cbec6c37555ba5eeb92530674e39e07` | authoritative source for the future editable Pepper baseline |
| Hermes Workspace reference | `https://github.com/outsourc-e/hermes-workspace` | `2.3.0` | `v2.3.0` | `15fa9cd706f5c04e4db288fb958e21d10fc776da` | `f00b66d6e7dc5bef87602cb026bdf14e593314b9fd242e3e1af48c20704616b9` | reference-only adjacent operations and UX candidate |

All external source roots remain:

- local;
- ignored;
- immutable;
- non-editable;
- not Git commit candidates.

P15.M0 did not modify `.gitignore` and did not force-add any external source.

## Ratified Adoption Decision

P15.M0 ratifies exactly:

```yaml
selected_option: Option 1 -- Upgrade Current Product Only
Hermes_Agent_baseline: 0.19.0
baseline_strategy: new editable baseline plus controlled forward-port
```

Decision meaning:

- Hermes Agent 0.19.0 becomes the authoritative source baseline.
- The current 0.18.2-derived product is not upgraded in place.
- P15.M1 will create a separate new editable product baseline.
- Pepper modifications will be forward-ported deliberately.
- Every forward-ported modification requires source ownership, candidate path, register entry, compatibility evidence, tests and rollback evidence.
- The current product remains canonical until a later migration gate promotes the new baseline.
- No wholesale file overwrite from the old product is permitted.

Rejected interpretations:

- patch the current product in place;
- run `hermes update`;
- merge upstream `main`;
- copy the entire old product over the new baseline.

## Current Product Authority

Current canonical editable product:

```yaml
current_product:
  path: 2_products/hermes-agent
  canonical: true
  modified_by_P15_M0: false
```

Current committed baseline evidence:

```yaml
tracked_files: 6246
modification_register:
  path: 2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
  rows: 128
  columns: 18
  duplicate_ids: 0
  duplicate_paths: 0
  missing_fields: 0
  hash_mismatches: 0
```

Until a future promotion gate explicitly changes authority, `2_products/hermes-agent` remains canonical.

P15.M0 does not authorize:

- renaming the current product;
- deleting the current product;
- replacing the current product;
- synchronizing the current product;
- modifying the current product;
- reusing `2_products/hermes-agent` as the P15.M1 destination;
- altering the modification register.

Required product changes during P15.M0: `0`.

## Future Editable Baseline Boundary

P15.M1 is authorized in principle to create a separate editable product baseline from the exact locked Hermes Agent 0.19.0 source.

P15.M0 does not choose or create the final destination directory.

P15.M1 must define and validate one exact destination before copying any file. The destination must:

- be under `2_products`;
- be separate from `2_products/hermes-agent`;
- not overwrite any existing path;
- be tracked by Git after human approval;
- contain no nested `.git`;
- be derived only from the exact locked 0.19.0 source;
- preserve upstream license and notice material;
- receive its own baseline inventory;
- receive a controlled migration and register strategy;
- remain a candidate, not canonical, until promotion.

P15.M1 must stop before acquisition if the proposed destination:

- already exists;
- overlaps the current product;
- is ignored;
- contains prior residue;
- is not explicitly authorized by its ticket.

P15.M0 unlocks only the design and creation of this new baseline through P15.M1.

## Update Continuity

P15.M0 preserves and ratifies the existing canonical update authority:

```yaml
update_authority_record: 0_architecture/governance/agent_platform_hermes_upstream_synchronization_strategy.md
update_strategy: filtered_snapshot_three_way_reapplication
automatic_semantic_merge: prohibited
rollback: mandatory
```

P15.M0 does not replace this model with ordinary upstream merge, rebase, pull, in-place update or wholesale source copying.

Ratified P12.5 source model:

```text
A  = current locked upstream
B  = future locked upstream candidate
C  = current committed Pepper product
FA = filtered/compliance reconstruction of A
FB = filtered/compliance reconstruction of B
P  = registered Pepper product divergence from FA
D  = resolved future Pepper candidate built from FB plus P
```

Required invariants:

- upstream references remain immutable;
- every candidate uses an exact repository, tag and full commit;
- every update starts with a non-mutating dry run;
- exclusions and compliance transformations are revalidated;
- licenses, notices and provenance are regenerated;
- `AGENT_PLATFORM_MODIFICATIONS.tsv` remains semantic divergence authority;
- semantic auto-merge remains prohibited;
- dual-sided conflicts require human ownership;
- previously green validation lanes may not regress silently;
- product replacement is manifest-driven and journaled;
- rollback preimages and inverse operations are mandatory;
- the active Pepper product is not mutated until the plan is approved.

## Hermes Native Update Boundary

Hermes Agent and Hermes Desktop native update actions are not Pepper update authority.

The future Pepper product must not allow a UI action to directly call:

```text
hermes update
hermes desktop --build-only
package-manager update
git pull
git merge
git rebase
```

Any upstream update control exposed through Desktop, Dashboard or Pepper P13 must be disabled, intercepted or adapted to invoke the Pepper Update Orchestrator.

```yaml
native_Hermes_update_button: not_authoritative_for_Pepper
Pepper_update_target: one_click_operator_experience
Pepper_update_internal_model: prepared_governed_transaction
```

## One-Click Operator Contract

Target user experience:

```text
one visible Pepper update action
+
a multi-stage governed internal transaction
```

Required conceptual flow:

```text
release discovery
-> candidate identity lock
-> immutable source acquisition
-> filtered candidate reconstruction
-> three-way reapplication
-> conflict classification
-> license/dependency/security review
-> isolated build and regression validation
-> rollback preparation
-> plan digest
-> human one-click application
-> post-application health validation
-> promotion or exact rollback
```

One-click application is allowed only when:

- candidate identity is exact;
- plan digest is frozen;
- conflicts are zero or explicitly resolved;
- legal and dependency gates are accepted;
- required tests are accepted;
- rollback is prepared;
- the active product and index have not changed since planning.

When any condition is not met, the UI must present `review_required` and must not update the product.

## Update State Machine

Minimum ratified update states:

```text
IDLE
UPDATE_DISCOVERED
SOURCE_LOCKED
DRY_RUN_RUNNING
REVIEW_REQUIRED
PLAN_READY
APPLYING
VALIDATING
ACTIVE
BLOCKED_IDENTITY
BLOCKED_LICENSE
BLOCKED_DEPENDENCY
BLOCKED_CONFLICT
BLOCKED_REGRESSION
APPLY_FAILED
ROLLBACK_RUNNING
ROLLED_BACK
ROLLBACK_FAILED
```

No UI may represent `PLAN_READY` as `ACTIVE`.

Every future release must be classified as exactly one:

```text
compatible_snapshot_update
conflicted_snapshot_update
structural_baseline_migration
rejected_or_deferred_update
```

The current 0.18.2 to 0.19.0 migration is classified as `structural_baseline_migration`.

Future releases may use `compatible_snapshot_update` only when exact comparison proves that a new editable baseline migration is unnecessary.

Dual version authority:

```yaml
Pepper_product_version: independent
Hermes_upstream_version: exact_version_tag_and_commit
display_policy: show_both
Hermes_release_changes_Pepper_product_version_automatically: false
```

## Interaction Surface Decision

P15.M0 ratifies:

| Surface | Adopted by P15.M0 | Role |
| --- | --- | --- |
| Pepper P13 | `true` | current canonical product UI during migration |
| Hermes Web Dashboard | `false` | upstream route and UX comparison reference |
| Hermes Desktop | `false` | future governed local human-client candidate |
| Hermes Workspace | `false` | future adjacent operations-surface candidate |

Not adopted means not granted product authority by P15.M0. It does not mean permanently rejected.

Future adoption requires dedicated P15.M4 through P15.M6 workstreams.

Neither Desktop nor Workspace may directly own:

- Pepper policy;
- provider authority;
- credential authority;
- durable backend truth;
- product routing authority;
- worker authority;
- update authority;
- approval authority.

## Deployment Decision

P15.M0 ratifies exactly:

```yaml
local_development_target:
  mode: C - WSL2 plus Docker Compose
  repository_location: Linux-native WSL filesystem
  runtime_volume_location: Linux-native WSL filesystem
  initial_UI: Pepper P13
  future_UI_candidate: Hermes Desktop
  optional_operations_candidate: Hermes Workspace

fallback_target:
  mode: B - WSL2 Native
  trigger_conditions:
    - Docker daemon unavailable
    - Compose hardening incomplete
    - image pinning incomplete
    - volume boundary incomplete
    - secret boundary incomplete

future_24_7_target:
  mode: D - external Linux VPS plus Docker Compose
  role: Pepper control plane and long-running governed services
```

Current host readiness remains separate:

```yaml
WSL2: available
Ubuntu: available
Docker_CLI: available
Docker_Compose: available
Docker_daemon: unavailable
strategic_target_operational_now: false
```

P15.M0 does not authorize enabling or starting Docker. No host mutation is authorized or performed.

## P15 Dispositions

P15.M0 ratifies exactly:

| Item | Current status | Final disposition | Destination |
| --- | --- | --- | --- |
| P15.0 | closed and active | `migrate` | P15.M8 |
| P15.1 | closed with compatibility follow-up | `migrate` | P15.M8 |
| P15.1A | paused | `retain_for_windows_fallback` | P15.M8 and bounded Windows fallback evidence |
| P15.2 | closed with compatibility follow-up | `migrate` | P15.M8 |
| P15.3 | closed with compatibility follow-up | `migrate` | P15.M8 and P15.M15 |
| P15.4 | paused | `replace` | P15.M11 and P15.M12 |

Historical uncommitted candidate:

```yaml
P15_4_uncommitted_candidate:
  formal_disposition: selectively_forward_port
```

Rules:

- the original dirty checkout remains untouched;
- the candidate is not approved;
- the candidate is not committable;
- no file is copied wholesale;
- only separately inventoried evidence may be reused;
- 0.18.2-specific assumptions must not transfer implicitly;
- every forward-port requires exact future ticket authority.

## Pepper-To-Siamese Architecture

P15.M0 ratifies:

```yaml
Pepper:
  role: governed control plane
  future_location: external Linux VPS
  authorities:
    - tickets
    - approvals
    - registry
    - audit
    - coordination
    - Jobs
    - Tasks
    - rollback decisions

Siamese:
  role: governed downstream digital-twin development program
  domains:
    - EnergyPlus backend
    - OpenUSD and AEC
    - Omniverse Kit
    - simulation
    - calibration
    - datasets
    - surrogate models
    - control and optimization
```

Execution placement:

```yaml
Siamese_source:
  canonical_location: Git remote
  local_backend_working_copy: Linux-native WSL filesystem
  Omniverse_working_copy: specialized GPU workstation

EnergyPlus_execution:
  local: WSL2 or governed container worker
  future: authorized remote Linux workers

Omniverse_Kit_execution:
  location: specialized GPU workstation
  general_VPS_assumption: prohibited

Pepper_control_plane:
  location: future Linux VPS
  relationship: selected Siamese work executes on local or specialized workers
```

Binding answer: Pepper should operate remotely as the governed control plane while selected Siamese work executes on local, containerized, remote or specialized workers.

Required boundaries:

- explicit WorkPacket or equivalent bounded work unit;
- scoped worker identity;
- no provider credential reused as worker identity;
- bounded artifact manifests;
- checksums;
- human approval retained;
- no unmanaged shared writable source volume;
- worker termination and artifact quarantine on rollback.

P15.M0 does not implement these mechanisms.

## Migration Workstream

P15.M0 ratifies the following migration program.

| Ticket | Purpose | Main prohibition |
| --- | --- | --- |
| P15.M0 - Adoption Authorization | Ratify architecture and authorize the migration program | No product, source, dependency, runtime, Docker, WSL, VPS, OAuth, provider, inference, Graphify or Git mutation |
| P15.M1 - New Hermes 0.19 Product Baseline | Create a separate tracked editable baseline from the exact locked 0.19.0 source | Do not overwrite the current product |
| P15.M2 - License and Notice Reconciliation | Establish notices, attribution, plugin-license and redistribution obligations | No public redistribution authorization |
| P15.M3 - Dependency and Lock Reconciliation | Reconcile Python, Node, build and lock dependencies for the new baseline | No uncontrolled upgrade or floating dependency |
| P15.M4 - Desktop and Workspace Productization Decision | Define whether Desktop or Workspace enters Pepper as governed product, client or adjacent service | No Desktop or Workspace installation or startup |
| P15.M5 - Interaction Surface Baseline | Freeze the selected Pepper, Dashboard, Desktop and Workspace surface map | No route authority transfer |
| P15.M6 - P13 Surface Migration | Forward-port approved Pepper P13 surfaces | No unregistered UI mutation |
| P15.M7 - P14 Runtime Migration | Migrate process, environment, readiness, containment, audit, shutdown and rollback boundaries | No live provider or uncontrolled process execution |
| P15.M8 - P15 Provider and Credential Migration | Migrate P15.0 through P15.3 contracts to the Hermes Agent 0.19.0 baseline | No real credential read, OAuth, provider call or inference |
| P15.M9 - WSL2 Development Architecture | Define Linux-native repository, filesystem, permissions, secret and process topology | No WSL mutation |
| P15.M10 - Docker Compose Local Pilot | Validate hardened and pinned WSL2 plus Docker Compose Pepper deployment | No mutable latest images or unmanaged secrets |
| P15.M11 - Tool-Free OAuth and Inference Revalidation | Replace old P15.4 path with bounded 0.19.0-derived OAuth and inference validation | No tools, MCP, retry, fallback, background worker or unbounded streaming |
| P15.M12 - Pepper End-to-End Local Acceptance | Validate complete local Pepper workflow under selected target | No VPS or production promotion |
| P15.M13 - VPS Security Baseline | Define network, TLS, proxy, firewall, secrets, backup, monitoring and incident requirements | No provisioning |
| P15.M14 - VPS Deployment Pilot | Perform first controlled external Linux VPS deployment | No public unmanaged port exposure |
| P15.M15 - Pepper-Siamese Worker Integration | Define and validate governed control-plane-to-worker execution | No unmanaged remote execution or shared provider credentials |
| P15.M16 - Rollback Rehearsal | Rehearse product, runtime, container, worker, artifact and credential rollback | No simulated success without executable rollback evidence |
| P15.M17 - Governed Upstream Synchronization Engine | Implement the versioned offline successor to the deferred P12.5.1 helper | No semantic conflict decisions and no Git staging, commit or push |
| P15.M18 - One-Click Pepper Update Surface | Adapt Pepper P13 and future Desktop integration so update control invokes Pepper governance | No endpoint, credential or Git authority in the frontend |
| P15.M19 - Update and Rollback Acceptance Drill | Exercise controlled update through planner, application, validation and rollback lifecycle | No promotion until forward update and exact rollback are demonstrated |
| P15.MR - Migration Closure | Promote accepted baseline and close the Hermes 0.19.0 migration | No closure while any required gate remains open |

P15.M17 responsibilities:

- exact candidate identity verification;
- FA, FB, C and D reconstruction;
- exclusion and manifest regeneration;
- modification-register reapplication;
- deterministic conflict inventory;
- update plan digest;
- journal and rollback preparation;
- no semantic conflict decisions;
- no Git staging, commit or push.

P15.M18 responsibilities:

- update availability display;
- dual-version display;
- update-plan status;
- review-required state;
- one-click apply of an already accepted plan;
- progress and validation state;
- rollback status;
- no endpoint, credential or Git authority in the frontend.

P15.M19 responsibility: demonstrate both forward update and exact rollback before promotion.

## Dependency Graph

Minimum dependency order:

```text
P15.M0
`-- P15.M1
    |-- P15.M2
    |-- P15.M3
    `-- P15.M4
        `-- P15.M5
            `-- P15.M6

P15.M3
`-- P15.M7
    `-- P15.M8
        `-- P15.M9
            `-- P15.M10
                `-- P15.M11

P15.M6
P15.M7
P15.M8
P15.M10
P15.M11
`-- P15.M12

P15.M12
`-- P15.M13
    `-- P15.M14
        `-- P15.M15
            `-- P15.M16

P15.M17
`-- P15.M18
    `-- P15.M19

P15.M16
P15.M17
P15.M18
P15.M19
`-- P15.MR
```

Additional rules:

- P15.M2 and P15.M3 may proceed in parallel after P15.M1.
- P15.M4 may inspect source and architecture after P15.M1 but may not authorize implementation before P15.M2 and P15.M3 constraints are known.
- P15.M6 and P15.M7 may proceed in parallel after their own prerequisites.
- P15.M11 requires accepted P15.M8 and P15.M10.
- P15.M12 requires accepted UI, runtime, provider and local deployment evidence.
- P15.M14 requires accepted P15.M13.
- P15.M15 requires accepted local and VPS control-plane baselines.
- P15.M17, P15.M18 and P15.M19 must be accepted before P15.MR.
- P15.MR requires all mandatory preceding tickets accepted.

P15.M0 unlocks only P15.M1. It does not pre-authorize later execution tickets.

## Promotion Gates

The current product remains canonical until all required promotion gates are accepted.

Minimum gates:

| Gate | Requirement |
| --- | --- |
| 1 | Exact 0.19.0 baseline created |
| 2 | License and notices reconciled |
| 3 | Dependencies and locks reconciled |
| 4 | P13 surfaces migrated |
| 5 | P14 runtime boundaries migrated |
| 6 | P15 provider and credential contracts migrated |
| 7 | Local WSL2 plus Docker Compose pilot accepted |
| 8 | Tool-free OAuth and inference revalidated |
| 9 | Complete local Pepper acceptance passed |
| 10 | Rollback rehearsal passed |
| 11 | Governed upstream synchronization engine accepted |
| 12 | One-click Pepper update surface accepted |
| 13 | Update and rollback acceptance drill passed |
| 14 | Migration closure approved by the human |

A future VPS deployment is not required to promote the local 0.19.0 Pepper baseline unless P15.MR explicitly makes it a closure requirement.

The VPS lane remains required before declaring Pepper 24/7 operational.

## Human Approval Gates

Human approval is required before:

- creating the P15.M1 tracked product baseline;
- selecting its final destination;
- installing dependencies;
- changing package manifests or lockfiles;
- building Desktop or Workspace;
- starting any runtime;
- enabling or starting Docker;
- mutating WSL configuration;
- running OAuth;
- reading or promoting credentials;
- calling a provider;
- performing inference;
- provisioning a VPS;
- exposing a network service;
- promoting the new product baseline;
- deleting or archiving the previous product;
- touching the historical P15.4 candidate;
- applying any governed update plan;
- rolling back a product update after application begins.

No later ticket inherits execution authority merely because P15.M0 exists.

## Branch And Worktree Strategy

P15.M0 runs only in:

```text
C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15U
```

Recommended future branch:

```text
p15.m-hermes-0.19-migration
```

Recommended future worktree:

```text
C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M
```

P15.M0 may recommend these names but must not create the branch or worktree.

P15.M1 may begin only after the human:

- commits and pushes P15.M0;
- creates the migration branch and worktree from the accepted P15.M0 commit;
- verifies the new worktree is clean;
- reacquires or reconstructs the locked ignored external sources when needed;
- verifies their exact tree hashes.

Because `4_external/sources/**` is ignored and worktree-local, source presence must not be assumed in a future worktree.

Do not copy ignored source roots from the dirty original checkout.

## P15.M1 Continuity Requirements

P15.M1 must preserve all information required for later automated updates:

- exact upstream identity;
- filtered import manifest;
- exclusion manifest;
- notices and provenance;
- product modification register;
- product-owned path inventory;
- baseline tree digest;
- dependency and lock identity;
- adapter compatibility profile;
- rollback target.

The new Hermes 0.19.0 baseline must not be created in a way that prevents future P12.5-style updates.

## Exact Candidate Set

Authorized creation:

```text
0_architecture/governance/agent_platform_hermes_0_19_migration_authorization.md
```

Authorized modifications: `none`.

Required candidate state:

```yaml
candidate_count: 1
unexpected_tracked_candidates: 0
unexpected_visible_untracked_task_candidates: 0
```

P15.M0 must not modify:

- `2_products/**`;
- `3_platform/**`;
- `4_external/sources/**`;
- `AGENT_PLATFORM_MODIFICATIONS.tsv`;
- `10_scripts/**`;
- `12_tests/**`;
- `AGENTS.md`;
- `.graphifyignore`;
- `graphify-out/**`;
- package manifests;
- lockfiles.

## Register And Inventory Policy

Required current product state:

```yaml
product_tracked_files: 6246
register_rows: 128
register_columns: 18
duplicate_ids: 0
duplicate_paths: 0
missing_fields: 0
hash_mismatches: 0
```

P15.M0 adds:

```yaml
product_files: 0
register_rows: 0
register_modifications: 0
```

If the current baseline differs materially, P15.M0 must stop with `P15.M0-PRODUCT-BASELINE-BLOCKED`. The current baseline matched, so P15.M0 is not blocked.

## Rollback And Rejection Rules

If P15.M0 is rejected before commit, remove only:

```text
0_architecture/governance/agent_platform_hermes_0_19_migration_authorization.md
```

Do not remove or modify:

- P15.U0;
- P15.U;
- source roots;
- current product;
- modification register;
- original dirty P15.4 candidate.

If a future migration ticket fails:

- current canonical product remains available;
- new candidate baseline remains non-canonical;
- failed candidates are isolated;
- no automatic fallback provider is permitted;
- no credentials are copied backward;
- no source root is modified;
- no migration closure is implied.

Governed update rollback remains mandatory. Rollback must use exact preimages, inverse operations, artifact quarantine where needed and human-reviewed recovery evidence. It must not use broad reset, clean, wildcard deletion, history rewrite or automatic force push.

## Validation Requirements

Required final validation state:

```yaml
P15_U0_tracked_and_committed: true
P15_U_tracked_and_committed: true
P15_U0_verdict_present: true
P15_U_verdict_present: true
HEAD_unchanged_from_dynamic_start: true
branch_remote_unchanged: true
origin_main_unchanged: true
index_empty: true
staged_files: none
candidate_count: 1
unexpected_candidates: 0
editable_product_changes: 0
register_changes: 0
product_inventory: 6246
register_rows: 128
register_columns: 18
register_hash_mismatches: 0
external_source_changes: 0
Graphify_commands: 0
Graphify_modifications: 0
dependency_installations: 0
builds: 0
tests: 0
runtime_executions: 0
Docker_starts: 0
WSL_mutations: 0
VPS_provisioning: 0
OAuth_flows: 0
credential_reads: 0
provider_calls: 0
inference_calls: 0
git_diff_check: clean
assessment_source_lock_prerequisite_files_unchanged: true
trailing_whitespace_lines_in_this_record: 0
```

P15.M0 performs no Git staging, commit or push. The human performs all repository Git mutations.

## Stop Conditions

P15.M0 must stop with `P15.M0-AUTHORIZATION-BLOCKED` if the ticket requires:

- source modification;
- product modification;
- register modification;
- dependency installation;
- runtime execution;
- Docker startup;
- WSL mutation;
- VPS provisioning;
- OAuth;
- credential access;
- provider call;
- inference;
- Graphify;
- Git mutation.

P15.M0 must stop with `P15.M0-DECISION-DRIFT-BLOCKED` if any accepted decision differs from P15.U for:

- Option 1;
- Hermes Agent baseline 0.19.0;
- new editable baseline plus controlled forward-port;
- local target C;
- fallback B;
- future target D;
- Desktop not adopted yet;
- Workspace not adopted yet;
- P15.0 migrate;
- P15.1 migrate;
- P15.1A retain_for_windows_fallback;
- P15.2 migrate;
- P15.3 migrate;
- P15.4 replace;
- P15.4 candidate selectively_forward_port.

No decision drift was observed.

## Required Final State

```yaml
verdict: hermes_0_19_migration_authorized_with_constraints

current_product:
  path: 2_products/hermes-agent
  canonical: true
  modified: false

future_baseline:
  source_version: 0.19.0
  source_commit: 3ef6bbd201263d354fd83ec55b3c306ded2eb72a
  strategy: new editable baseline plus controlled forward-port
  created_by_P15_M0: false

deployment:
  local_target: C - WSL2 plus Docker Compose
  fallback: B - WSL2 Native
  future_24_7: D - external Linux VPS plus Docker Compose

interaction_surfaces:
  Pepper_P13: canonical_now
  Hermes_Desktop: future_candidate
  Hermes_Workspace: future_adjacent_candidate

migration:
  unlocked_ticket: P15.M1
  later_tickets_authorized_for_execution: false

candidate_set:
  candidates: 1
  unexpected_candidates: 0

Git:
  staged_files: 0
  commits_by_agent: 0
  pushes_by_agent: 0
```

## Final Verdict

```text
hermes_0_19_migration_authorized_with_constraints
```

P15.M0 is ready for human review and commit. P15.M1 is unlocked only after P15.M0 is committed. P15.M2 through P15.MR remain dependency-gated. P15.1A remains paused and retained only for Windows fallback. P15.4 remains replaced by P15.M11 and P15.M12. Live OAuth, provider calls and inference remain unauthorized.
