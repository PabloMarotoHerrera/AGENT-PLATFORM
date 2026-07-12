# P12.C2 - AGENT PLATFORM Repository Topology Assessment and Hermes Product Placement

## 1. Document Header

| Field | Value |
| --- | --- |
| Project | P12 - Hermes Productization Foundation |
| Ticket | P12.C2 - AGENT PLATFORM Repository Topology Assessment and In-Repository Hermes Product Placement Redefinition |
| Type | Repository architecture / topology correction / product-placement decision |
| Date | 2026-07-12 |
| Status | Canonical topology decision; bounded P12.C3 remediation required before corrected P12.1 |
| Scope | Workspace-root repository topology and Hermes product placement |
| Authority | Topology decision only; no restructuring, source import, runtime, directory creation, or Git mutation |
| Canonical output | `0_architecture/governance/agent_platform_repository_topology_assessment_and_hermes_product_placement.md` |
| Durable document count | Exactly one |
| Authorized workspace | `C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM` |

Result markers:

```text
agent_platform_single_workspace_policy_confirmed
agent_platform_repository_topology_assessed
agent_platform_current_topology_verdict_recorded
agent_platform_target_topology_defined
agent_platform_directory_authority_boundaries_defined
hermes_in_repository_product_placement_selected
hermes_nested_git_repository_prohibited
hermes_external_product_root_prohibited
hermes_locked_upstream_product_separation_defined
repository_topology_remediation_decision_recorded
hermes_p12_1_reentry_decision_recorded
hermes_p12_2_reentry_sequenced
no_repository_restructure_executed
no_product_source_import
no_nested_git_created
no_runtime_execution
no_git_mutation
```

## 2. Purpose

This record assesses the actual AGENT PLATFORM repository topology, defines the
target authority classes for P12-P21, selects the exact internal location for
editable Hermes product source, and establishes the remediation and reentry
sequence. It does not assume the current physical tree or Git posture is correct.

P12.C2 performs documentation and bounded read-only inspection only. It creates
no directory, product source, nested Git repository, branch, remote, worktree,
submodule, generated state, runtime state, build output, package, or migration.

## 3. Executive Decision

```yaml
P12_C2_ExecutiveDecision:
  current_topology_classification: usable_with_bounded_structural_corrections
  repository_wide_migration_required: false
  bounded_remediation_required: true
  remediation_ticket: P12.C3
  selected_hermes_product_root: 2_products/hermes-agent
  selected_hermes_classification: hybrid_product_with_platform_adapters
  p12_1_reentry_now: false
  p12_1_reentry_after_P12_C3: true
  p12_2_reentry: only_after_corrected_P12_1
```

The numbered top-level model is coherent enough to retain. The decisive defect
is that `2_products/`, the correct product authority class, is ignored wholesale
while P12 now requires Hermes product source to be a tracked normal subtree of
the main repository. P12.C3 must establish an exact Hermes tracking exception
without exposing the other local-only product candidates. P12.C1 removed the
external topology, so no external or nested repository alternative is permitted.

## 4. P12.C1 Prerequisite Status

| Check | Observed result | Verdict |
| --- | --- | --- |
| Removed external root | `C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-HERMES` absent | Passed |
| Authorized root | `C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM` exists | Passed |
| Main Git root | Exact authorized root | Passed |
| P12.1 | `rolled_back_due_to_unauthorized_out_of_workspace_product_root` | Reopened |
| P12.2 | `rolled_back_due_to_invalid_product_root` | Reopened |
| Locked upstream | Exists at `4_external/sources/hermes-agent` | Passed |
| Locked upstream HEAD | `9de9c25f620ff7f1ce0fd5457d596052d5159596` | Exact match |
| Locked upstream status | Clean | Passed |
| P11.2 | SHA-256 `2797C043DE240776E6816D30E63C5E07080F64AD819255A575D75D2F5C57D6F9` | Unchanged from P12.C1 |

P12.C1 is complete. The invalid topology is not materially active.

## 5. Workspace Invariant

```yaml
AgentPlatformWorkspaceInvariant:
  root: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM
  root_name: AGENT PLATFORM
  normal_project_work_must_remain_inside_root: true
  sibling_project_repository_default: prohibited
  external_product_copy_default: prohibited
  nested_git_repository_default: prohibited
  git_worktree_default: prohibited
  submodule_default: prohibited
  external_runtime_workspace_default: temporary_only_when_exactly_gated
  permanent_external_path_requires_prior_human_authorization: true
```

Permanent project topology belongs inside AGENT PLATFORM. Temporary operating-
system runtime state may use an exact, pre-authorized temporary location when a
technical need cannot be met safely inside the existing ignored artifact class.
External immutable references remain inside `4_external/sources/` and do not
become editable internal source by proximity.

## 6. Inputs Consumed

Required P12/P11 inputs:

```text
0_architecture/governance/agent_platform_hermes_productization_authorization_and_boundary.md
0_architecture/governance/agent_platform_hermes_controlled_fork_repository_topology.md
0_architecture/governance/agent_platform_hermes_license_exclusion_notice_baseline.md
0_architecture/governance/agent_platform_hermes_misplaced_product_root_rollback.md
0_architecture/governance/agent_platform_hermes_integration_closure.md
0_architecture/governance/agent_platform_hermes_source_review_authorization.md
0_architecture/governance/agent_platform_hermes_interface_adapter_design.md
```

Repository architecture and policy inputs:

```text
README.md
.gitignore
0_architecture/workspace/agent_platform_workspace_charter.md
0_architecture/workspace/agent_platform_workspace_responsibility_map.md
0_architecture/workspace/agent_platform_workspace_topology.md
0_architecture/workspace/agent_platform_product_workspace_policy.md
0_architecture/workspace/agent_platform_external_source_handling_policy.md
0_architecture/workspace/agent_platform_canonical_documentation_structure.md
0_architecture/workspace/agent_platform_migration_plan.md
0_architecture/product_workspaces/agent_platform_product_git_posture_decision.md
0_architecture/product_workspaces/agent_platform_product_dependency_external_source_posture.md
0_architecture/governance/agent_platform_local_workspace_state_model.md
3_platform/_governed_skeleton/core/README.md
3_platform/_governed_skeleton/integrations/provider_adapter_layer/README.md
```

Current substantive content controls. No historical filename was restored.

## 7. Inspection Scope

Inspection was limited to:

```text
exact Git root and status metadata
immediate children of numbered major classes
one additional level where needed for products, platform, external sources,
artifacts, contract/schema placement, and Hermes candidate evaluation
top-level README and current canonical architecture/policy records
exact ignore-rule checks and tracked-path counts by class
locked-upstream read-only HEAD and clean-status metadata
```

No product or external source code was executed. No credentials, `.env` values,
API keys, OAuth state, browser state, user Hermes state, runtime database,
`.opencode` content, `AGENTS.md` content, root `graphify-out` content, or local
spreadsheet content was opened. Graphify was not used.

## 8. Current Repository Topology Inventory

The Git root is `C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM`. Current
tracked files occur at the root and under `0_architecture`, `1_research`,
`3_platform`, `5_workspace`, and `6_docs`. `2_products`,
`4_external/sources`, `7_datasets`, `8_models`, `9_artifacts`, and
`previusknowledge` are ignored by explicit root rules.

| Current class | Observed immediate shape | Git/authority observation |
| --- | --- | --- |
| Root | `.gitignore`, `.graphifyignore`, `README.md`, numbered classes, local ignored Office files | One main Git repository; README is an entry point, not complete topology authority |
| `0_architecture/` | 25 domain/governance/workspace/archive/implementation-oriented children | 135 tracked files; current human-readable authority is status-scoped, especially workspace and governance records |
| `1_research/` | `ai`, `digital twins`, `engineering`, `natural systems`, `papers` | Evidence class; one tracked `.gitkeep` observed |
| `2_products/` | six existing product candidates; only `omniverse-app` visibly populated at bounded depth | Correct product class but ignored wholesale by `.gitignore` |
| `3_platform/` | `_governed_skeleton` plus empty domain placeholders | 88 tracked files, all under `_governed_skeleton`; shared implementation class |
| `4_external/` | `datasets`, `licenses`, `sources`, `standarts` | External reference class; raw `sources` ignored; locked Hermes is separated here |
| `5_workspace/` | `.gitkeep` | Operational/context-projection placeholder, tracked |
| `6_docs/` | `.gitkeep` | Human documentation projection placeholder, tracked |
| `7_datasets/` | empty | Project data class, ignored/local by default |
| `8_models/` | empty | Model/checkpoint class, ignored/local by default |
| `9_artifacts/` | `gbrain_sandbox`, `graphify` generated/evidence trees | Existing suitable generated/artifact class, ignored/local |
| `10_scripts/` | empty | Reviewed automation target; no current tracked content |
| `11_tools/` | empty | Reviewed tooling target; no current tracked content |
| `12_tests/` | empty | Cross-project validation target; no current tracked content |
| `13_packages/` | empty | Package-definition/release-metadata target; no current tracked content |
| `14_sdk/` | empty | SDK/interface target; no current tracked content |
| `previusknowledge/` | `docs`, `research` | Historical migration corpus; ignored/local and non-authoritative |

No `1_contracts`, `2_schemas`, top-level `docs`, `src`, `packages`, `apps`, or
`tools` class exists under those unnumbered names. Contract/schema-named tracked
paths are split between normative governance records and domain-local platform
implementation under `3_platform/_governed_skeleton`.

## 9. Directory Responsibility Matrix

| Class | Current responsibility | Decision | Target authority boundary |
| --- | --- | --- | --- |
| `0_architecture` | Architecture, governance, decisions, policy, migration and implementation records | `retain_with_documentation_clarification` | Normative authority only when status/scope/currentness establish it; no executable product source or generated output |
| `1_research` | Investigation and evidence | `retain_with_documentation_clarification` | Evidence only until promoted |
| `2_products` | Product-specific source, docs, tests and behavior | `retain_with_local_reorganization` | Product-scoped editable source in the main repo only after per-product tracking governance |
| `3_platform` | Reusable platform implementation, contracts and integrations | `retain_with_documentation_clarification` | Shared cross-product implementation only; no complete product trees |
| `4_external` | Immutable external source and curated external metadata | `retain_with_documentation_clarification` | External evidence only; raw sources ignored and read-only by ticket |
| `5_workspace` | Operational projections, context packs and coordination | `retain_with_documentation_clarification` | Operational support, not canonical architecture or runtime dumps |
| `6_docs` | User/developer documentation projections | `retain_with_documentation_clarification` | Human-facing projections that cite source authority |
| `7_datasets` | Project-owned/local datasets and data evidence | `retain_with_documentation_clarification` | Ignored payloads by default; metadata requires explicit review |
| `8_models` | Models, checkpoints and embeddings | `retain_with_documentation_clarification` | Ignored/local model artifacts, never source authority |
| `9_artifacts` | Generated, build, test, runtime and retained evidence outputs | `retain_as_is` | Ignored/local generated state; promotion requires separate governance |
| `10_scripts` | Reviewed repeatable automation | `retain_with_documentation_clarification` | Tracked only after script review; no hidden policy |
| `11_tools` | Governed internal tooling | `retain_with_documentation_clarification` | Tracked only after trust/lifecycle review |
| `12_tests` | Cross-project/platform validation assets | `retain_with_documentation_clarification` | Shared validation only; product-local tests remain with product source |
| `13_packages` | Package definitions and release metadata | `retain_with_documentation_clarification` | Tracked definitions only; outputs belong in artifacts |
| `14_sdk` | Shared SDK interfaces/examples | `retain_with_documentation_clarification` | Cross-product public interfaces only, not product implementation |
| `previusknowledge` | Previous knowledge and migration evidence | `deprecated_or_historical` | Remains local historical evidence until explicit migration/archive action |

Numeric prefixes remain navigation aids, not authority rank. No top-level class
is renamed or moved by P12.C2.

## 10. Topology Problems and Risks

| Issue ID | Affected path/class | Observed conflict | Severity | Immediate remediation | Blocks Hermes? | Target responsibility / dependency |
| --- | --- | --- | --- | --- | --- | --- |
| `TOP-C2-001` | `.gitignore`, `2_products/` | Whole product class is ignored while Hermes must be tracked in the main repository | High | Yes, P12.C3 | Yes | Exact tracked exception for `2_products/hermes-agent`; preserve all other product candidates local-only |
| `TOP-C2-002` | `3_platform/` | Tracked implementation exists only in `_governed_skeleton` while same-domain sibling placeholders are empty | Medium | Documentation clarification; later local reorganization only if justified | No, if exact governed path is used | `_governed_skeleton` remains current shared implementation root pending a separate platform migration decision |
| `TOP-C2-003` | `0_architecture/` | Empty/near-empty overlapping names such as `decisions` and `decisions adr`, plus architecture-local implementation record naming, reduce navigation clarity | Medium | No immediate movement | No | Clarify current authority; consolidate/rename only through later migration |
| `TOP-C2-004` | `0_architecture/governance` and `3_platform/_governed_skeleton` | Normative contracts and executable contract/schema types are distributed without one explicit two-layer rule | Medium | Documentation clarification in this record | No | Normative contracts remain architecture/governance; executable schemas remain domain-local platform implementation |
| `TOP-C2-005` | `4_external/datasets`, `7_datasets` | External versus project-owned data distinction exists conceptually but is not obvious from root navigation | Medium | Documentation clarification | No | External data stays under `4_external`; project/local data stays under `7_datasets` |
| `TOP-C2-006` | `4_external/standarts` | Directory name is misspelled and does not clearly express standards metadata | Low | Rename candidate only | No | Preserve until exact migration updates paths/references |
| `TOP-C2-007` | `previusknowledge` | Historical misspelling and legacy corpus status reduce navigation clarity | Low | Historical/rename candidate only | No | Preserve as migration evidence; never rename casually |
| `TOP-C2-008` | `README.md` | Entry point describes key authority but not the complete numbered responsibility taxonomy or Hermes correction | Medium | Later documentation ticket | No | README should eventually project current canonical topology without becoming authority |
| `TOP-C2-009` | `10_scripts`-`14_sdk` | Empty filesystem placeholders have policy definitions but little physical navigation evidence | Low | No immediate action | No | Activate only through substantive tickets; avoid symmetry-only files |

Explicit problem-detection conclusions:

| Potential problem | Finding |
| --- | --- |
| Governance mixed with executable implementation | `0_architecture/implementation` contains implementation records, not the tracked executable platform source; naming is ambiguous but physical source separation remains intact |
| Source mixed with generated output | No material mixing found at assessed depth; `9_artifacts` and root ignore patterns provide a suitable generated class |
| Third-party source mixed with internal modifications | No current editable Hermes product exists; raw upstream remains isolated under `4_external/sources` |
| Product source under external class | None currently; prohibited for the selected topology |
| Duplicate product roots | No active duplicate Hermes root; `2_products` is the sole selected product class |
| Competing contract/schema locations | Two layers exist, but their normative-versus-executable boundary needed this explicit clarification |
| Ambiguous product/platform ownership | Present if Hermes were placed in `3_platform`; resolved by selecting `2_products/hermes-agent` |
| Runtime state inside canonical source | No current Hermes runtime state; future state is assigned to ignored/local classes |
| Build outputs tracked as source | No evidence at assessed depth |
| Historical records treated as current authority | P12.C1 corrected P12.1/P12.2; historical sections are explicitly superseded |
| External integrations coupled directly to core | No evidence; current provider/adapter layer is metadata-only and bounded |

## 11. Current Topology Verdict

```yaml
AgentPlatformCurrentTopologyVerdict:
  classification: usable_with_bounded_structural_corrections
  evidence_summary: numbered_authority_classes_are_coherent_but_product_tracking_conflicts_with_required_main_repo_Hermes_source
  hermes_placement_can_proceed_without_global_remediation: true
  bounded_remediation_blocks_current_P12_1_reentry: true
  repository_wide_migration_required: false
```

The topology must not be softened to `correct_as_is`: the ignore posture is a
real structural/Git conflict. It also does not justify a repository-wide
migration because architecture, product, platform, external and artifact classes
are already conceptually separated and the Hermes blocker is narrowly repairable.

## 12. Target Repository Topology

| Target class/location | Purpose and owner | Authority | Allowed content | Blocked content | Tracking/generated posture | Consumers | Migration requirement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `0_architecture/workspace`, `0_architecture/governance`, domain architecture paths | Workspace architecture and governance; workspace/governance owners | Normative when current, scoped and accepted | Policies, decisions, contracts, topology, migration and audit records | Product source, runtime state, build output | Track reviewed docs | All classes | Retain; clarify and consolidate only by migration ticket |
| `0_architecture/governance` normative contracts | Implementation-neutral contract authority | Canonical contract specification | Stable ports, authority boundaries, schemas as specifications | Hermes internals and provider-specific payloads | Track reviewed docs; never generated state | Platform and products | Retain |
| `3_platform/_governed_skeleton` domain-local executable contracts/schemas | Shared platform implementation owner | Executable representation subordinate to normative contracts | Domain contract types, validators, platform schemas | Product-owned behavior and upstream source | Normal main-repo source | Platform and products | Retain current implementation root; later naming cleanup optional |
| `3_platform/_governed_skeleton` | Shared platform implementation | Reusable cross-product code only | Agents, context, security, validation, tools, providers, runtime boundaries | Complete products, raw external source, local runtime state | Main-repo tracked source | Products and platform operations | Retain |
| `2_products/<product>` | Product/application implementation; product owner | Product-scoped source authority | UI, backend, CLI, config, product tests/docs and product-specific workflows | Root governance, shared contract authority, raw generated/runtime state | Per-product governed main-repo tracking | Product users and platform adapters | P12.C3 required for Hermes exception |
| `4_external/sources/<source>` | Immutable external references; external-source governance | External evidence only | Exact snapshots and upstream Git metadata | Internal edits, generated state, product patches | Ignored/local; read-only by exact ticket | Research, product import/review | Retain |
| `4_external/licenses` and future reviewed metadata paths | Curated external metadata | Evidence | Provenance, license, notices, source reviews | Raw source copies or approval by proximity | Track only reviewed metadata | Governance and products | Retain/clarify |
| `3_platform/_governed_skeleton/integrations/<integration>` | Shared integration implementation | Platform-owned mediation | Provider/product adapters and compatibility mapping | Stable contracts owned by a product; product source copy | Main-repo tracked after implementation gate | Platform consumers and products | Hermes path defined but not created here |
| `12_tests` | Cross-product/platform validation | Validation evidence | Shared conformance, boundary and integration tests | Product-only test suites or runtime output | Track reviewed tests; outputs local | Platform and products | Retain |
| `10_scripts`, `11_tools` | Developer automation/tooling | No architecture authority | Reviewed scripts and tools | Hidden policy, credentials, generated outputs | Track reviewed source; execution gated | Developers/validation | Retain |
| `6_docs` | Human-facing docs | Projection by default | User, developer, reference and operations guides | Competing root authority | Track reviewed docs | Humans | Retain |
| `9_artifacts/<scope>` | Generated/build/test/runtime/release evidence | Generated/local only | Builds, logs, reports, caches, temporary state and package outputs | Canonical source, contracts, secrets intended for persistence | Ignored/local | Validation and operators by exact ticket | Retain; no directory created now |
| `5_workspace` | Operational projections and coordination | Operational support | Reviewed process material and future context projections | Source trees, runtime dumps, hidden governance | Mixed reviewed tracking; generated projections local | Agents/humans | Retain |
| `7_datasets`, `8_models` | Project-owned local data/model payloads | Evidence only | Governed datasets/models after provenance review | Source authority, secrets, unlicensed payloads | Ignored/local by default | Research/products by exact ticket | Retain |
| `13_packages` | Package/release definitions | Release metadata only | Reviewed package definitions and release metadata | Build/package outputs | Definitions tracked; outputs in artifacts | Release tooling | Retain |
| `14_sdk` | Shared external-facing SDK surfaces | Shared interface authority after approval | SDK interfaces, compatibility docs and examples | Product internals and provider credentials | Track reviewed source/docs | External/internal developers | Retain |

No new top-level contract, schema, source, app, package, test, or docs class is
introduced merely for symmetry.

## 13. Candidate Hermes Placement Evaluation

| Candidate | Workspace/main Git | Product/platform fit | Upstream separation | Generated-state fit | Scalability | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| `3_platform/hermes` | Inside and normally trackable | Incorrectly classifies a broad UI/runtime product as shared platform code | Separate | Possible | Blurs future product boundaries | Reject |
| `3_platform/products/hermes` | Inside and trackable | Creates a second product taxonomy under platform | Separate | Possible | Competes with `2_products` | Reject |
| `3_platform/products/hermes-agent` | Inside and trackable | Same duplicate-taxonomy problem; name does not fix ownership | Separate | Possible | Competes with `2_products` | Reject |
| `3_platform/apps/hermes` | Inside and trackable | Introduces absent `apps` class inside platform and misclassifies product | Separate | Possible | Weak fit for GBrain/Paperclip coexistence | Reject |
| `4_external/products/hermes-agent` | Inside but external class | Places editable internal product under external evidence | Overlaps external authority conceptually | Poor | Creates source-custody ambiguity | Reject |
| New top-level product/application class | Could be inside/main Git | Duplicates existing `2_products` without necessity | Separate | Possible | Adds migration and navigation cost | Reject |
| `2_products/hermes-agent` | Inside; blocked only by current whole-class ignore | Exact existing product authority class for UI/backend/CLI/runtime product | Fully separate from `4_external/sources/hermes-agent` | Uses existing ignored artifact/local rules | Coexists with other products and shared platform | Select after P12.C3 |

## 14. Hermes Product Classification

Hermes is classified as:

```text
hybrid_product_with_platform_adapters
```

It is externally derived but becomes AGENT PLATFORM-owned editable product
source after controlled import. It is not a small shared library. Its upstream
surface includes frontend UI, dashboard, backend/runtime, CLI, agent loop,
configuration, tools, plugins, skills, sessions/state and product-facing
workflows. Product behavior belongs under `2_products`; reusable authority and
adapter contracts remain platform-owned.

## 15. Selected Exact Hermes Product Root

```yaml
HermesInRepositoryProductPlacementDecision:
  absolute_path: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\2_products\hermes-agent
  repository_relative_path: 2_products/hermes-agent
  exists_now: false
  creation_authorized_by_P12_C2: false
  inside_authorized_workspace: true
  main_repository_subtree: true_after_P12_C3_and_corrected_P12_1
  nested_git: false
  worktree: false
  submodule: false
  separate_remote: false
  overlaps_locked_upstream: false
  overlaps_generated_or_artifact_class: false
  current_ignore_conflict: true
  remediation_required_before_creation: P12.C3
```

The stable name is `hermes-agent`, matching the controlled source identity while
remaining clearly product-scoped under `2_products`.

## 16. Upstream, Product, Contracts and Adapter Relationship

```yaml
HermesSourceRelationship:
  immutable_upstream:
    path: 4_external/sources/hermes-agent
    role: read_only_reference_and_provenance_anchor
    editable: false

  editable_product:
    path: 2_products/hermes-agent
    role: agent_platform_owned_hermes_product_source
    git_repository: AGENT_PLATFORM_main_repository
    nested_git: false
    independently_pushed: false

  platform_contracts:
    role: implementation_neutral_AGENT_PLATFORM_contracts
    location: normative_0_architecture/governance_and_executable_domain_contracts_under_3_platform/_governed_skeleton
    hermes_must_depend_on_contracts_not_own_them: true

  integration_adapter:
    role: Hermes_specific_adapter_implementation
    location: 3_platform/_governed_skeleton/integrations/hermes
    stable_contract_owner: AGENT_PLATFORM
    created_by_P12_C2: false

  generated_state:
    role: local_generated_runtime_and_build_state
    primary_class: 9_artifacts/hermes
    conventional_product_local_ignored_paths_allowed: true
    tracked_as_product_source: false
```

The product subtree must not contain upstream `.git` metadata. P12.5 may later
define comparison/import synchronization using provenance metadata, but no
independent product remote, branch, repository, subtree mechanism, worktree or
submodule is permitted.

## 17. Generated and Runtime-State Topology

| State class | Target posture |
| --- | --- |
| Editable Hermes source | Tracked normal main-repository subtree at `2_products/hermes-agent` after gates |
| Python virtual environment | Ignored product-local `.venv` or exact approved local environment; never source |
| `node_modules` | Ignored product-local dependency state |
| Frontend build output | Generated/local; product-local ignored `dist`/build path or `9_artifacts/hermes` evidence projection |
| Python build output | Generated/local and ignored |
| Test caches/results | Caches ignored; retained reports under `9_artifacts/hermes` when exactly authorized |
| Runtime `HERMES_HOME` | Never canonical source; exact ignored `9_artifacts/hermes/runtime` or authorized OS temp location |
| Runtime workspace | Temporary/local and explicitly gated; not a durable project workspace |
| Logs | Local/generated-sensitive under ignored runtime/artifact class |
| SQLite/state database | Local/generated-sensitive; never tracked as product source |
| Model/provider cache | Local/generated-sensitive; no provider activation implied |
| Import/synchronization staging | Temporary exact scope under ignored artifact/temp class; remove or retain by ticket |
| Release/package output | Generated under `9_artifacts/hermes/releases`; package definitions may live in `13_packages` after approval |

`9_artifacts` is already a suitable generated/local-state class. P12.C2 does not
create `9_artifacts/hermes` or authorize runtime state.

## 18. Main-Repository Git Policy

```text
Hermes product source is tracked by the existing AGENT PLATFORM repository.
No nested .git.
No product-local branch.
No product-local origin or upstream remote.
No separate product commit history.
No worktree.
No submodule.
No subtree mechanism unless a later human authorization explicitly supersedes this policy.
All product changes are normal AGENT PLATFORM repository changes.
Stage exact paths only.
The human retains commit and push authority.
```

The upstream URL, release, tag and SHA remain provenance metadata and do not
become product Git remotes.

## 19. Repository-Wide Remediation Decision

Selected option:

```text
Option B - Bounded remediation required
```

Required ticket:

```text
P12.C3 - AGENT PLATFORM Repository Topology Remediation
```

P12.C3 must, at minimum:

1. Replace the whole-class `2_products/` ignore posture with an exact policy that
   keeps existing product candidates ignored while allowing only the future
   `2_products/hermes-agent` subtree to be tracked normally.
2. Update affected current product Git/topology policy records so the Hermes
   exception is explicit and does not imply activation or tracking approval for
   sibling products.
3. Validate that `2_products/hermes-agent` remains absent during remediation,
   is no longer blocked by the root ignore policy, and no sibling product path
   became newly visible or staged.
4. Preserve `4_external/sources/hermes-agent`, `9_artifacts`, local Office files,
   external sources, datasets, models, historical corpus and unrelated untracked
   paths.
5. Perform no product source import, directory creation, force-add, broad staging,
   commit, push or repository migration unless the P12.C3 ticket explicitly and
   separately authorizes its own exact action.

This is a bounded tracking-policy correction, not a repository-wide physical
migration. Empty placeholder cleanup, spelling renames and README expansion do
not block Hermes and must not be bundled without separate architectural scope.

## 20. Corrected P12.1 Responsibility

Corrected P12.1 remains blocked until accepted P12.C3 completes. It must then be
revised in place to:

```text
replace the invalid sibling-repository topology
adopt 2_products/hermes-agent as the exact product root
create only the normal in-repository product directory structure
not run git init
not create .git, branches, tags, remotes, worktrees or submodules
not copy Hermes source
confirm the root is a normal AGENT PLATFORM main-repository subtree
confirm the exact path is trackable without force-add
confirm no overlap with upstream, generated, artifact or local-only state
preserve the immutable upstream
hand the filtered source import to corrected P12.2
```

## 21. Corrected P12.2 Responsibility

After corrected P12.1 creates and validates the empty internal root, corrected
P12.2 must be revised and reexecuted in place to:

```text
import a fresh filtered snapshot only from the immutable locked upstream
never reuse content from the deleted external folder
exclude skills/productivity/powerpoint before import
exclude generated complete-skill documentation copies
remove exact registry/sidebar references
preserve applicable license and NOTICE materials
recreate provenance, import and exclusion manifests
record product paths relative to AGENT PLATFORM
create no nested Git metadata, branch, tag, remote, worktree or submodule
leave staging, commit and push to the human in the main repository
```

P12.2 cannot run before corrected P12.1 acceptance.

## 22. Migration and Rollback Boundary

P12.C2 performs no migration, so no filesystem rollback is needed. Any P12.C3
or later topology migration must require:

```text
exact before-state inventory
exact path and ignore-rule mapping
dependency and cross-reference analysis
read-only Git-history evidence where needed
one migration wave at a time
explicit rollback for each changed path or class
no broad wildcard move
no destructive Git reset or clean
README/navigation updates when they are in the approved migration scope
cross-reference repair
post-migration validation
human Git authority
```

No path may be moved merely to make the tree symmetrical.

## 23. Stop Rules

Stop if the removed sibling root reappears, the workspace root differs from the
exact path with the space, the selected product path would be outside AGENT
PLATFORM or overlap the upstream/artifact classes, a nested repository/worktree/
submodule is proposed, prohibited content inspection is required, P12.C3 has not
resolved the ignore conflict, source import or runtime is requested in this
ticket, Git mutation is required, or another durable Markdown appears necessary.

## 24. P12.1 Reentry Decision

```yaml
HermesP12_1ReentryDecision:
  may_reenter_now: false
  blocker: TOP-C2-001_whole_2_products_ignore_rule
  required_predecessor: P12.C3
  may_reenter_after_accepted_P12_C3: true
  exact_root_on_reentry: 2_products/hermes-agent
```

## 25. P12.2 Sequencing

```yaml
HermesP12_2Sequencing:
  may_reenter_now: false
  must_wait_for_P12_C3: true
  must_wait_for_corrected_P12_1: true
  imports_only_from_locked_upstream: true
  deleted_external_snapshot_reuse: prohibited
```

P12.C2 does not unlock P12.3, P12.4, P12.5 execution, P12.6, P12.7, P12.R,
P13, P14, provider/model execution, or runtime expansion.

## 26. Created, Modified and Not Created Register

Created:

```text
0_architecture/governance/agent_platform_repository_topology_assessment_and_hermes_product_placement.md
```

Modified:

```text
no pre-existing file
```

Not created, modified, moved, renamed, deleted, executed or activated:

```text
2_products/hermes-agent
any Hermes product source copy
any nested .git, branch, remote, worktree, submodule or symlink
any generated, runtime, build, test, package or release output
P12.1 or P12.2 canonical records
README.md
.gitignore
.graphifyignore
.opencode/
AGENTS.md
graphify-out/
4_external/sources/hermes-agent/**
Git index or history
```

## 27. Limitations

The assessment intentionally did not inspect product or external source code,
unrelated untracked content, credentials, environment values, runtime data, or
generated Graphify content. Empty directories are filesystem placeholders and
do not establish tracked topology. The exact P12.C3 ignore-rule implementation,
Hermes owner assignment, product source security review, and corrected source
import remain future decisions/actions.

## 28. Final Verdict

```yaml
P12_C2_RepositoryTopologyDecision:
  authorized_workspace_root: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM

  current_topology:
    classification: usable_with_bounded_structural_corrections
    global_remediation_required: false
    bounded_remediation_required: true
    documentation_clarification_required: true

  target_topology:
    defined: true
    major_authority_classes_defined: true
    source_generated_state_separated: true
    external_internal_source_separated: true
    product_platform_contract_boundaries_defined: true

  hermes:
    classification: hybrid_product_with_platform_adapters
    selected_product_root: 2_products/hermes-agent
    product_root_inside_agent_platform: true
    product_is_main_repo_subtree: true
    nested_git_repository: false
    separate_product_remote: false
    immutable_upstream_path: 4_external/sources/hermes-agent

  sequencing:
    topology_remediation_ticket_required: true
    P12_1_may_reenter: false
    P12_1_may_reenter_after_P12_C3: true
    P12_2_must_wait_for_corrected_P12_1: true
```

```text
agent_platform_single_workspace_policy_confirmed
agent_platform_repository_topology_assessed
agent_platform_current_topology_verdict_recorded
agent_platform_target_topology_defined
agent_platform_directory_authority_boundaries_defined
hermes_in_repository_product_placement_selected
hermes_nested_git_repository_prohibited
hermes_external_product_root_prohibited
hermes_locked_upstream_product_separation_defined
repository_topology_remediation_decision_recorded
hermes_p12_1_reentry_decision_recorded
hermes_p12_2_reentry_sequenced
no_repository_restructure_executed
no_product_source_import
no_nested_git_created
no_runtime_execution
no_git_mutation
```

## 29. Human Commit Commands

P12.C2 did not stage, commit or push. If the human accepts this record, the exact
main-repository commands are:

```powershell
git status --short
git add 0_architecture/governance/agent_platform_repository_topology_assessment_and_hermes_product_placement.md
git commit -m "P12.C2 - Assess topology and select Hermes product placement"
git push origin main
```

Never use `git add .`.
