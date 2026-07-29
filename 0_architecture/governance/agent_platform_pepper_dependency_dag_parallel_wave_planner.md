# P16.3 Dependency DAG And Parallel Wave Planner Governance Record

## P16.3 Authority

P16 is Ticket Factory and Parallel Planning. P16.3 adds only deterministic, immutable and in-memory dependency planning for Pepper `TicketSpec` collections.

The planner consumes one P16.0 `ProjectSpec`, a bounded collection of P16.0 `TicketSpec` objects, explicit caller-supplied external dependency resolutions and an immutable parallel-planning policy. It produces dependency edges, a hard-prerequisite DAG, deterministic topological ordering, external dependency blockers, declared-scope collision evidence, dependency-ready waves and reproducible digests.

P16.3 is not ticket execution, runtime parallel safety proof, ticket policy linting, proposal synthesis, human approval, canonical publication, agent assignment, worker assignment, worktree allocation, prompt rendering, provider access, repository scanning or WorkPacket creation.

## Common P16 Branch Model

| Item | Value |
| --- | --- |
| P16 branch model | one common branch |
| Common branch | `p16-ticket-factory-and-parallel-planning` |
| Commit model | one reviewed commit per P16 ticket |
| Ticket-specific branches | absent |
| Agent branch creation | `0` |
| Agent staging, commit or push | `0` |

## Repository And Branch State

| Item | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM` |
| Branch | `p16-ticket-factory-and-parallel-planning` |
| Resolved P16.2 commit | `d6e1124658cfe191ca8bdc51db5e8ac24731fdbd` |
| P16.2 commit message | `P16.2 Add ticket generator agent roles` |
| HEAD at implementation | `d6e1124658cfe191ca8bdc51db5e8ac24731fdbd` |
| Remote P16 at implementation | `d6e1124658cfe191ca8bdc51db5e8ac24731fdbd` |
| P16.2 is ancestor of remote P16 | `true` |
| main at implementation | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| origin/main at implementation | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| Worktree at gate | clean |
| Index at gate | empty |
| Visible untracked at gate | `0` |
| Registered worktrees | `1` |
| Pepper root | present |
| Legacy Hermes root | absent |
| Omniverse tracked files | `369` |

The P16.3 candidate remains uncommitted by instruction. No staging, commit, push, branch switch, reset, clean, stash, Docker command, dependency update, lockfile update, Graphify command or `graphify-out` modification was performed.

## Prerequisite Verdicts

| Prerequisite | Verdict |
| --- | --- |
| P16.0 | `hermes_0_19_pepper_project_ticket_spec_schema_ready_with_planning_only_authority` |
| P16.1 | `hermes_0_19_pepper_context_pack_assembler_ready_with_bounded_in_memory_authority` |
| P16.2 | `hermes_0_19_pepper_ticket_generator_agent_roles_ready_with_non_executing_proposal_authority` |

Required public imports passed for `DependencyKind`, `DependencyScope`, `ParallelizationHint`, `ProjectSpec` and `TicketSpec`.

P16.3 did not modify `specs.py`, `context_packs.py`, `generator_roles.py`, or the accepted P16.0/P16.1/P16.2 focused tests.

## Pre-Change Pepper Identity

Committed P16.2 Pepper identity before P16.3 implementation:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate | `6841` | `150155984` | `6bc2ddf83cfade21e166e320ad8149bb50a33355e6edd4164e6b47808dcd0662` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Pre-change governance integrity reported `14` tests, `0` failures and `0` errors.

## Post-Change Pepper Identity Projection

The existing integrity utility computes committed `HEAD` blob identity. Because P16.3 is not committed by the agent, the expected post-commit Pepper identity was computed with the same v2 record-stream algorithm over the current working-tree candidate set:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate post-commit projection | `6844` | `150263890` | `6b1bf7227c122be600b9ef17e2ccda4dc7db4bddb4344af2e3fa03fadd7a7dcd` |
| Payload post-commit projection | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record post-commit projection | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Upstream payload changed: `false`. Baseline changed: `false`. New Pepper product files: `3`.

## Package Paths

| Path | Purpose |
| --- | --- |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py` | Public Ticket Factory export boundary extended additively for P16.3. |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/dependency_planning.py` | Immutable P16.3 dependency DAG and parallel-wave planning contracts. |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/specs.py` | Unmodified P16.0 planning contracts consumed by P16.3. |

No parent `agent_platform` initializer, runtime route, frontend source, provider code, credential code or dependency file was modified.

## Public Exports

P16.3 adds exactly these 17 public exports:

| Export |
| --- |
| `DEPENDENCY_PLAN_SCHEMA_VERSION` |
| `ExternalDependencyState` |
| `ScopeCollisionKind` |
| `TicketBlockerKind` |
| `WaveDisposition` |
| `ExternalDependencyResolution` |
| `DependencyEdge` |
| `ScopeCollision` |
| `TicketBlocker` |
| `ParallelPlanningPolicy` |
| `TicketPlanningRequest` |
| `ParallelWave` |
| `TicketDependencyPlan` |
| `DependencyPlanningError` |
| `DependencyCollectionValidationError` |
| `DependencyCycleError` |
| `build_ticket_dependency_plan` |

P16.0 exports preserved: `true`. P16.1 exports preserved: `true`. P16.2 exports preserved: `true`. Duplicate exports: `0`. Private helpers exported: `0`. Import side effects: `0`.

## Schema Version

`DEPENDENCY_PLAN_SCHEMA_VERSION = 1`. `TicketDependencyPlan.schema_version` is fixed to `Literal[1] = 1`. Alternative plan schema versions are rejected. Schema migration and runtime negotiation are absent.

## Controlled Enums

| Enum | Values |
| --- | --- |
| `ExternalDependencyState` | `satisfied`, `unresolved`, `blocked` |
| `ScopeCollisionKind` | `exact_pattern`, `recursive_prefix`, `global_pattern`, `ambiguous_glob` |
| `TicketBlockerKind` | `external_unresolved`, `external_blocked`, `upstream_blocked` |
| `WaveDisposition` | `dependency_ready`, `serial`, `scope_review_required` |

Enum aliases: `0`. Unrestricted enum strings are rejected. `WaveDisposition` is planning evidence only.

## ExternalDependencyResolution

Field order: `ticket_id`, `state`, `evidence_reference`, `rationale`.

`satisfied` requires bounded `evidence_reference`. `unresolved` may omit evidence. `blocked` validates with bounded rationale. Resolutions are caller-supplied planning evidence only and perform no external lookup, network access, repository lookup or external work.

## DependencyEdge

Field order: `prerequisite_ticket_id`, `dependent_ticket_id`, `kind`, `scope`, `blocks_readiness`.

Edge direction is prerequisite to dependent. `hard_prerequisite` maps to `blocks_readiness=true`; `soft_predecessor` maps to `blocks_readiness=false`. Inconsistent caller-constructed edge records are rejected.

## ScopeCollision

Field order: `collision_id`, `left_ticket_id`, `right_ticket_id`, `left_path_pattern`, `right_path_pattern`, `kind`, `blocks_same_wave`.

Ticket pairs are canonical. Collision IDs are assigned after canonical sorting as `SCOPE-001`, `SCOPE-002` and later values. Exact, recursive-prefix and global-pattern collisions block same-wave placement. Ambiguous glob evidence does not block same-wave placement but requires review disposition when present in a wave.

## TicketBlocker

Field order: `ticket_id`, `blocked_by_ticket_id`, `kind`, `direct`, `rationale`.

Direct blockers originate from unresolved or blocked hard external dependencies. Inherited blockers propagate through hard internal dependencies. Soft predecessor edges do not propagate blockers.

## ParallelPlanningPolicy

Field order: `max_wave_size`, `separate_serial_tickets`, `separate_known_scope_collisions`, `ambiguous_glob_requires_review`.

Defaults: `max_wave_size=32`, `separate_serial_tickets=true`, `separate_known_scope_collisions=true`, `ambiguous_glob_requires_review=true`. `max_wave_size` is bounded from `1` through `64`. The three safety booleans are `Literal[true]` and cannot be disabled in schema version `1`. Runtime concurrency, worker limits, agent limits, worktree limits and provider limits are absent.

## TicketPlanningRequest And Collection Validation

Field order: `project_spec`, `tickets`, `external_dependency_resolutions`, `policy`.

Ticket bounds: minimum `1`, maximum `512`. External resolution maximum: `512`. Ticket IDs must be unique. All ticket project IDs and ticket prefixes must match `project_spec.project_id`. Internal dependencies must use the current project prefix and target a ticket in the collection. External dependencies must not use the current project prefix. External resolutions must be unique and target declared external dependencies.

The planner does not rewrite dependency scopes and does not infer missing internal dependencies as external.

## Hard-Prerequisite DAG

Only hard internal dependencies form the blocking DAG. The planner constructs prerequisite-to-dependent adjacency, rejects hard multi-node cycles and returns no partial plan after cycle failure. Cycle witnesses are deterministic and bounded to ticket IDs. Soft-only cycles are permitted as advisory metadata. External dependencies are excluded from the internal DAG.

## Soft-Predecessor Boundary

Soft predecessor is advisory ordering evidence, not a readiness gate.

Soft edges remain in `edges` with `blocks_readiness=false`; they do not create hard DAG edges, propagate blockers, force separate waves or fail the plan when soft-only cycles exist. P16.4 owns later semantic linting.

## External Dependency Resolution And Blockers

Hard external `satisfied` dependencies may become ready when hard internal prerequisites are ready. Hard external `unresolved`, `blocked` or missing resolutions directly block the dependent ticket. Soft external unresolved or blocked state never blocks readiness and is retained as advisory unresolved-soft evidence.

Direct blockers propagate through hard internal dependents and downstream hard internal dependents. Propagation is deterministic and deduplicated. Blockers do not propagate across soft edges. Blocked tickets stay in `ticket_ids`, `topological_order`, `blocked_ticket_ids` and `blockers`, but are absent from waves.

## Canonical Ticket Ordering

Ticket IDs are ordered by project number, suffix segments, numeric tokens as integers, alphabetic tokens by uppercase ordinal value and shorter equal-prefix sequences first. This prevents `P16.10` from sorting before `P16.2`. Input order, filesystem order and locale sorting are not authority.

## Topological Ordering

Hard prerequisites precede dependents. All tickets appear exactly once, including blocked tickets. Soft edges do not force hard order. Ties use canonical ticket order. The topological order is planning evidence, not an execution queue.

## Declared-Scope Collision Algorithm

The planner inspects only `TicketSpec.scope.allowed_paths`. It performs no filesystem access, no glob expansion and no path existence checks.

Recognized known collisions are exact pattern equality, recursive-prefix containment such as `docs/**` containing `docs/file.md`, and global pattern `**`. Known collisions conservatively prevent same-wave placement. Ambiguous glob evidence is recorded when nontrivial glob syntax cannot be proven or disproven by bounded syntactic rules. Ambiguous evidence does not claim actual write conflict and does not claim safety.

## ParallelWave And Wave Calculation

Field order: `wave_index`, `wave_id`, `ticket_ids`, `disposition`, `scope_collision_ids`.

Wave indexes start at `1`; wave IDs are `WAVE-001`, `WAVE-002` and later values. Waves are non-empty and respect `max_wave_size`. Readiness is calculated from hard internal prerequisites only. Serial-hint tickets are isolated into one-ticket waves. Known scope collisions are separated. Ambiguous same-wave glob evidence sets `scope_review_required`. Blocked tickets are excluded. Parallel waves have no runtime execution authority.

## TicketDependencyPlan

Field order: `schema_version`, `project_id`, `ticket_ids`, `planning_input_SHA256`, `edges`, `scope_collisions`, `blockers`, `topological_order`, `waves`, `blocked_ticket_ids`, `unresolved_soft_external_dependency_ids`, `policy`, `plan_SHA256`.

Plan invariants reject duplicate ticket IDs, nondeterministic edge/collision/blocker order, incomplete topological coverage, duplicate wave membership, blocked/waved overlap, incomplete wave-plus-blocked coverage, hard prerequisites not in earlier waves, known same-wave collisions and digest mismatch.

The plan contains no agent identity, worker identity, worktree path, provider, model, prompt, execution command, approval, publication, WorkPacket or runtime state.

## Digest Evidence

Planning input digest algorithm: `agent-platform-ticket-dependency-input-sha256-v1`.

The input digest includes `ProjectSpec`, canonically ordered tickets, canonically ordered external resolutions and policy. Ticket and resolution permutations preserve it. Ticket content, resolution content and policy changes alter it.

Plan digest algorithm: `agent-platform-ticket-dependency-plan-sha256-v1`.

The plan digest includes schema version, project ID, ticket IDs, input digest, edges, scope collisions, blockers, topological order, waves, blocked ticket IDs, unresolved soft external dependency IDs and policy. It excludes `plan_SHA256` itself. DAG, blocker, scope-collision and wave changes alter it. Digests are neither security signatures nor approval signatures.

## Public Exceptions

`DependencyPlanningError` is the base exception. `DependencyCollectionValidationError` reports invalid collections. `DependencyCycleError` reports hard cycles with bounded ordered ticket IDs. Messages exclude full ProjectSpec content, full TicketSpec content, validation command content and secrets.

## Forbidden Public Shapes And Serialization

Public Pydantic models are frozen, extra-forbid and use validated defaults. Unknown fields are rejected, mutable defaults are absent, strict booleans reject strings and safety booleans cannot be disabled.

Public fields contain no `typing.Any`, unrestricted mapping fields, object payloads, arbitrary metadata bags, `Path`, datetime, UUID, bytes, callable, graph-library object, provider object, agent object, worker object, worktree object, execution command, approval object or WorkPacket object.

Standard Pydantic `model_dump()`, `model_dump_json()`, `model_validate()`, `model_validate_json()` and `model_json_schema()` are supported. Filesystem serialization, YAML support, Markdown rendering, file loaders and file writers are absent.

## Tests

Focused P16.3 command from `2_products/pepper-agent`:

```text
python -m pytest -q tests/hermes_cli/test_agent_platform_ticket_factory_dependency_planning.py -p no:cacheprovider
```

Result: `133` passed, `0` failed, `0` errors, `0` unexpected skips, `0` warnings reported.

Focused combined P16.0/P16.1/P16.2/P16.3 command from `2_products/pepper-agent`:

```text
python -m pytest -q tests/hermes_cli/test_agent_platform_ticket_factory_specs.py tests/hermes_cli/test_agent_platform_ticket_factory_context_packs.py tests/hermes_cli/test_agent_platform_ticket_factory_generator_roles.py tests/hermes_cli/test_agent_platform_ticket_factory_dependency_planning.py -p no:cacheprovider
```

Result: `424` passed, `0` failed, `0` errors, `0` unexpected skips, `0` warnings reported. Constituent counts: P16.0 `96`, P16.1 `75`, P16.2 `120`, P16.3 `133`.

Import smoke:

```text
TicketPlanningRequest ParallelWave TicketDependencyPlan DependencyCycleError build_ticket_dependency_plan
```

Governance integrity command reported `14` tests, `0` failures and `0` errors.

## Static Validation

Ruff check over the three P16.3 Python candidates reported `0` lint errors. Ruff format check reported `3` files already formatted. `ty` availability: `false`; type check was not run because the tool is unavailable; dependency installation remained `0`.

AST static import and authority scan reported `P16_3_STATIC_IMPORT_AUTHORITY_SCAN_OK`. Forbidden imports and execution, filesystem, network, Git, provider, worker, agent, tool and worktree references were absent.

## Modification Register

`2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` records exactly three new P16.3 product-addition rows: `P16.3-001`, `P16.3-002`, `P16.3-003`.

Existing row `P16.0-001` for `hermes_cli/agent_platform/ticket_factory/__init__.py` was preserved and updated to the additive P16.3 hash and description. Duplicate IDs: `0`. Duplicate paths: `0`. Missing destination paths: `0`. Hash mismatches for P16.3 rows and updated `P16.0-001`: `0`. Unrelated row edits: `0` by intended candidate scope.

## Import Manifest

`2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` records three new P16.3 product-addition rows for the dependency-planning source, focused tests and documentation. Existing destination row `hermes_cli/agent_platform/ticket_factory/__init__.py` was updated to the additive P16.3 hash and rule. The governance record is not included in the Pepper import manifest.

Classification for new rows: `AGENT_PLATFORM_product_addition`. Included in upstream payload: `false`. Duplicate concrete destinations: `0`. Destination hash mismatches for P16.3 rows and updated `__init__.py`: `0`.

## Product File Hashes

| Path | SHA-256 |
| --- | --- |
| `hermes_cli/agent_platform/ticket_factory/__init__.py` | `13039568ca18507a6a33910dcc463176e6f089736b348d1c4930e651d275c5a3` |
| `hermes_cli/agent_platform/ticket_factory/dependency_planning.py` | `2975350fa4694decc25e19a75f0b50c591b657cc2457d1ff7e4a8fd5d415e027` |
| `tests/hermes_cli/test_agent_platform_ticket_factory_dependency_planning.py` | `ed9b0aeb14c39ebbc2704ddf01d67cc3bae1642c494067a75512c88aa62a2fc1` |
| `docs/agent-platform/dependency_dag_parallel_wave_planner.md` | `f8d8c7c05ea35aa9503ff8cce78e4375ae8770c384f631a60ab9d49530c31986` |
| `AGENT_PLATFORM_MODIFICATIONS.tsv` | `f3d208cbe0c90f5b7db7c79261fcc141279ee140829ee8482ec61a1259572b22` |
| `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | `3ab43ac1d8c9d0fa4714ff92636cf2fa436c67dadf5bfb70ccd561a83c057601` |

## Operational Counters

| Counter | Value |
| --- | ---: |
| filesystem reads by product code | `0` |
| filesystem writes by product code | `0` |
| subprocesses by product code | `0` |
| shell execution by product code | `0` |
| network calls by product code | `0` |
| provider calls by product code | `0` |
| OAuth actions by product code | `0` |
| credential access by product code | `0` |
| worker actions by product code | `0` |
| runtime agent actions by product code | `0` |
| tool actions by product code | `0` |
| Git actions by product code | `0` |
| Graphify actions | `0` |
| Docker actions | `0` |
| branch actions | `0` |
| worktree actions | `0` |
| ticket generation | `0` |
| prompt rendering | `0` |
| ticket linting | `0` |
| proposal synthesis | `0` |
| human approval | `0` |
| canonical publishing | `0` |
| WorkPacket creation | `0` |
| runtime parallel execution | `0` |

Pydantic validation, deterministic graph construction, bounded syntactic scope analysis, deterministic JSON encoding and SHA-256 hashing are the only runtime behaviors introduced by P16.3 product code.

## Secret Scan

Focused secret-shape scan across the seven P16.3 candidates reported `P16_3_SECRET_SHAPE_SCAN_OK`.

Real-value counts: access tokens `0`, refresh tokens `0`, authorization headers `0`, OAuth codes `0`, credential contents `0`, real auth file contents `0`, private keys `0`, API keys `0`, raw provider responses `0`, raw prompts `0`, reasoning traces `0` and personal absolute paths in product files `0`.

## Exact Candidate Set

Created Pepper product files:

| Status | Path |
| --- | --- |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/dependency_planning.py` |
| Added | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_ticket_factory_dependency_planning.py` |
| Added | `2_products/pepper-agent/docs/agent-platform/dependency_dag_parallel_wave_planner.md` |

Modified Pepper product files:

| Status | Path |
| --- | --- |
| Modified | `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` |

Created governance record:

| Status | Path |
| --- | --- |
| Added | `0_architecture/governance/agent_platform_pepper_dependency_dag_parallel_wave_planner.md` |

Candidate formula: `3` created Pepper product files plus `3` modified Pepper product files plus `1` created governance record equals `7` candidates. Created files: `4`. Modified files: `3`. Deleted files: `0`. Unexpected candidates: `0`. Specs candidate: `false`. Context packs candidate: `false`. Generator roles candidate: `false`. Prior test candidates: `0`. Frontend candidates: `0`. Backend runtime candidates: `0`. Provider candidates: `0`. Worker candidates: `0`. Omniverse candidates: `0`. External source candidates: `0`. Graphify candidates: `0`. Dependency file candidates: `0`.

## P16.4 Handoff

P16.4 owns ticket policy profiles, collection-level policy rules, required-section policy, authority-boundary linting, scope-policy validation, forbidden action detection, validation-command policy, response-contract policy, roadmap sequencing policy, deterministic lint diagnostics, lint severity and blocking posture.

P16.4 must consume `ProjectSpec`, `TicketSpec` and `TicketDependencyPlan`. P16.4 must not own multi-generator proposal synthesis, semantic conflict resolution, human approval, canonical publishing or WorkPacket execution.

## Residual Constraints

| Item | State |
| --- | --- |
| TicketDependencyPlan immutable | `true` |
| TicketDependencyPlan deterministic | `true` |
| TicketDependencyPlan persisted | `false` |
| TicketDependencyPlan executable | `false` |
| TicketDependencyPlan approved | `false` |
| hard dependency DAG constructed | `true` |
| hard dependency DAG execution authority | `false` |
| soft predecessors advisory only | `true` |
| external dependency resolutions caller supplied | `true` |
| external dependency resolutions independently verified | `false` |
| ParallelWave dependency-ready metadata | `true` |
| ParallelWave runtime schedule | `false` |
| ParallelWave execution lane | `false` |
| ParallelWave worktree allocation | `false` |
| scope collision syntactic evidence only | `true` |
| actual write conflict proven | `false` |
| glob expansion | absent |
| filesystem access | absent |
| ticket policy linter | absent |
| proposal synthesis | absent |
| human approval | absent |
| canonical publishing | absent |
| agent assignment | absent |
| worker assignment | absent |
| worktree assignment | absent |
| WorkPacket | absent |
| runtime routes | `0` |
| product UI | disabled |
| Graphify | frozen read-only; not run by P16.3 instruction |
| production readiness | not claimed |

Canonical verdict occurrences in this record: `1`. Alternative P16.3 verdict occurrences: `0`.

## Final Verdict

hermes_0_19_pepper_dependency_dag_parallel_wave_planner_ready_with_dependency_only_authority
