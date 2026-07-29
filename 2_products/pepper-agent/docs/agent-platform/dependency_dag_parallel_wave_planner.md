# Dependency DAG And Parallel Wave Planner

P16.3 adds a deterministic, immutable and in-memory dependency planner for Pepper Ticket Factory planning. It consumes one P16.0 `ProjectSpec`, a bounded collection of P16.0 `TicketSpec` objects, explicit caller-supplied external dependency resolutions and an immutable `ParallelPlanningPolicy`.

The planner produces dependency edges, a hard-prerequisite DAG, deterministic topological ordering, external dependency blockers, conservative declared-scope collision evidence, dependency-ready waves and a reproducible dependency-plan digest. It does not execute tickets and does not prove runtime parallel safety.

## Relationship To P16.0, P16.1 And P16.2

P16.0 owns immutable `ProjectSpec`, `TicketSpec`, `TicketDependencySpec`, `DependencyKind`, `DependencyScope` and `ParallelizationHint` contracts. P16.1 owns bounded `ContextPack` assembly. P16.2 owns non-executing generator-role assignments and independent proposal envelopes.

P16.3 consumes P16.0 planning specs only. It does not consume `ContextPack`, invoke ticket-generator roles, synthesize proposals, approve proposals or publish tickets.

P16 uses one common branch, `p16-ticket-factory-and-parallel-planning`, with one reviewed commit per ticket. P16.3 starts only after the committed and pushed P16.2 parent.

## Dependency-Only Authority

P16.3 performs Pydantic validation, deterministic graph construction, bounded syntactic scope analysis, deterministic JSON encoding and SHA-256 hashing. It performs no filesystem reads, filesystem writes, repository scans, Git calls, glob expansion, network calls, provider calls, model selection, prompt rendering, agent assignment, worker assignment, worktree allocation, runtime concurrency control, approval, publication or WorkPacket creation.

`ParallelWave` is dependency-ready planning metadata, not execution authority.

## Controlled Enums

| Enum | Values |
| --- | --- |
| `ExternalDependencyState` | `satisfied`, `unresolved`, `blocked` |
| `ScopeCollisionKind` | `exact_pattern`, `recursive_prefix`, `global_pattern`, `ambiguous_glob` |
| `TicketBlockerKind` | `external_unresolved`, `external_blocked`, `upstream_blocked` |
| `WaveDisposition` | `dependency_ready`, `serial`, `scope_review_required` |

Enum aliases are absent. `WaveDisposition` is planning evidence only and is not execution authorization.

## ExternalDependencyResolution

Field order: `ticket_id`, `state`, `evidence_reference`, `rationale`.

An external dependency resolution is caller-supplied planning evidence. `ticket_id` uses the same bounded ticket identifier shape as P16.0. `state` is an `ExternalDependencyState`. `evidence_reference` is bounded text or `None`, defaulting to `None`. `rationale` is bounded non-empty text.

`satisfied` requires an `evidence_reference`. `unresolved` may omit evidence. `blocked` is valid with a bounded rationale. P16.3 does not verify external systems, perform network lookup, inspect repositories or execute external work.

## DependencyEdge

Field order: `prerequisite_ticket_id`, `dependent_ticket_id`, `kind`, `scope`, `blocks_readiness`.

Edges are created deterministically from `TicketSpec.dependencies`. The edge direction is prerequisite to dependent. `hard_prerequisite` maps to `blocks_readiness=True`. `soft_predecessor` maps to `blocks_readiness=False`. Caller-constructed edges with inconsistent `blocks_readiness` are rejected.

Internal and external dependencies both remain present in `TicketDependencyPlan.edges`. Only hard internal dependencies form the hard-prerequisite DAG.

## ScopeCollision

Field order: `collision_id`, `left_ticket_id`, `right_ticket_id`, `left_path_pattern`, `right_path_pattern`, `kind`, `blocks_same_wave`.

Collision ticket pairs are canonical. Collision identifiers are deterministic and assigned after canonical sorting as `SCOPE-001`, `SCOPE-002` and so on. Known collision kinds set `blocks_same_wave=True`; ambiguous glob evidence sets `blocks_same_wave=False`.

Scope collisions are conservative syntactic evidence over declared `TicketSpec.scope.allowed_paths`. They do not prove actual write conflicts.

## TicketBlocker

Field order: `ticket_id`, `blocked_by_ticket_id`, `kind`, `direct`, `rationale`.

Direct blockers originate from unresolved or blocked hard external dependencies. Inherited blockers propagate through hard internal dependency edges. Soft predecessor edges do not propagate blockers.

`blocked_by_ticket_id` identifies the external dependency ticket or hard internal prerequisite responsible for the blocker. Error and blocker rationale text is bounded and does not include full ticket content.

## ParallelPlanningPolicy

Field order: `max_wave_size`, `separate_serial_tickets`, `separate_known_scope_collisions`, `ambiguous_glob_requires_review`.

Defaults: `max_wave_size=32`, `separate_serial_tickets=True`, `separate_known_scope_collisions=True`, `ambiguous_glob_requires_review=True`.

`max_wave_size` is bounded from `1` through `64` and limits planning output only. The three safety booleans are fixed to `true` in schema version `1` and cannot be disabled. The policy contains no runtime concurrency, worker limit, agent limit, worktree limit or provider limit.

## TicketPlanningRequest

Field order: `project_spec`, `tickets`, `external_dependency_resolutions`, `policy`.

The request requires one `ProjectSpec`, one to 512 `TicketSpec` objects, zero to 512 external dependency resolutions and one planning policy. `external_dependency_resolutions` defaults to an empty tuple. `policy` defaults to `ParallelPlanningPolicy()`.

Collection validation rejects duplicate ticket IDs, tickets from another project, internal dependency targets missing from the ticket collection, internal dependencies with a foreign project prefix, external dependencies with the current project prefix, duplicate external resolutions and external resolutions for undeclared external dependencies. Dependency scopes are not rewritten or inferred.

Ticket input order is not graph or wave authority.

## Hard-Prerequisite DAG

Only internal dependencies whose kind is `hard_prerequisite` form the blocking DAG. The edge direction is prerequisite to dependent. Hard internal cycles are rejected with `DependencyCycleError` and deterministic ordered ticket IDs.

External dependencies are not inserted into the internal DAG. Soft predecessor dependencies remain advisory metadata and do not create hard DAG edges.

## Soft-Predecessor Semantics

Soft predecessor is advisory ordering evidence, not a readiness gate.

Soft predecessor edges remain present in `TicketDependencyPlan.edges` with `blocks_readiness=False`. They do not block readiness, do not create hard DAG edges, do not propagate blockers, do not force separate waves and do not make soft-only cycles fail. P16.4 may later lint whether a soft dependency is semantically appropriate.

## External Dependency Boundary

For a hard external prerequisite, a `satisfied` resolution allows the dependent ticket to become ready if its hard internal prerequisites are also ready. `unresolved`, `blocked` or missing resolution directly blocks the dependent ticket.

For an external soft predecessor, resolution state never blocks readiness. Missing, unresolved or blocked soft external dependencies are retained in `unresolved_soft_external_dependency_ids` as advisory evidence.

## Blocker Propagation

A direct external blocker propagates from the directly blocked ticket to hard internal dependents, then to downstream hard internal dependents. Propagation is deterministic and deduplicated. It does not cross soft predecessor edges.

Blocked tickets remain present in `ticket_ids`, `topological_order`, `blocked_ticket_ids` and `blockers`. Blocked tickets do not appear in waves.

## Deterministic Ticket Ordering

Ticket ordering is based on deterministic ticket-ID tokens, not raw lexicographic ordering, filesystem order, locale sorting or input order. Project numbers sort numerically. Suffix segments are tokenized so numeric tokens sort as integers and alphabetic tokens sort by uppercase ordinal value. Shorter equal-prefix token sequences sort first.

For example, `P16.2`, `P16.3`, `P16.10`, `P16.C1`, `P16.R` sorts in that order.

## Topological Ordering

The planner produces deterministic topological ordering over hard internal dependencies. All tickets appear exactly once, including blocked tickets. Hard prerequisites precede dependents. Soft predecessors are not required to precede dependents. Ties use canonical ticket order.

The topological order is planning evidence. It is not an execution queue.

## Declared-Scope Collision Algorithm

The planner inspects only `TicketSpec.scope.allowed_paths`. It does not access the filesystem, expand glob patterns or check path existence.

Known collisions:

| Kind | Evidence | Same Wave |
| --- | --- | --- |
| `exact_pattern` | same path pattern in two tickets | separated |
| `recursive_prefix` | `prefix/**` syntactically contains another declared pattern | separated |
| `global_pattern` | one side is `**` | separated |

Ambiguous glob evidence is recorded when nontrivial glob syntax is present and the bounded rules cannot prove or disprove intersection. Ambiguous glob evidence does not claim safety and does not force separation, but a wave containing the ambiguous pair has disposition `scope_review_required`.

General glob equivalence and semantic scope policy are deferred to P16.4 or later.

## ParallelWave

Field order: `wave_index`, `wave_id`, `ticket_ids`, `disposition`, `scope_collision_ids`.

Wave indexes start at `1`. Wave IDs are deterministic as `WAVE-001`, `WAVE-002` and so on. `ticket_ids` is a non-empty unique tuple. `scope_collision_ids` is unique and used only for `scope_review_required` waves.

Serial waves contain exactly one ticket. Known scope collisions are never present within the same wave. Ambiguous scope evidence may be present within a wave only with review disposition.

## Wave Calculation

The planner excludes blocked tickets, calculates readiness from hard internal prerequisites, selects ready tickets in canonical order, isolates serial-hint tickets into one-ticket waves, fills non-serial waves up to `max_wave_size`, separates known scope collisions and marks ambiguous same-wave glob evidence for review.

`parallel_candidate` and `unspecified` hints do not prove parallel safety. A dependency-ready wave is not approved to execute.

## TicketDependencyPlan

Field order: `schema_version`, `project_id`, `ticket_ids`, `planning_input_SHA256`, `edges`, `scope_collisions`, `blockers`, `topological_order`, `waves`, `blocked_ticket_ids`, `unresolved_soft_external_dependency_ids`, `policy`, `plan_SHA256`.

`schema_version` is fixed to `1`. The plan validates deterministic edge, collision and blocker order; all-ticket topological coverage; unique wave membership; blocked/waved separation; complete coverage by waves plus blocked tickets; hard prerequisite topological and wave order; known-collision separation; and plan digest equality.

The plan contains no agent identity, worker identity, worktree path, provider, model, prompt, execution command, approval, publication, WorkPacket or runtime state.

## Input Digest

The planning input digest algorithm is `agent-platform-ticket-dependency-input-sha256-v1`.

The digest record includes the `ProjectSpec`, canonically ordered `TicketSpec` collection, canonically ordered external dependency resolutions and `ParallelPlanningPolicy`, serialized with deterministic JSON using `model_dump(mode="json")`, `ensure_ascii=False`, compact separators and sorted keys.

The same semantic request has the same input digest regardless of ticket or resolution input order. Ticket content, resolution content and policy changes alter the digest. The digest is provenance evidence only.

## Plan Digest

The plan digest algorithm is `agent-platform-ticket-dependency-plan-sha256-v1`.

The digest record includes schema version, project ID, ticket IDs, planning input digest, edges, scope collisions, blockers, topological order, waves, blocked ticket IDs, unresolved soft external dependency IDs and policy. It excludes `plan_SHA256` itself.

The plan digest changes when DAG, blocker state, scope collision evidence or wave partition changes. It is not a security signature, approval signature, execution identity or publication identity.

## Public Exceptions

`DependencyPlanningError` is the base error. `DependencyCollectionValidationError` reports invalid planning collections. `DependencyCycleError` reports hard internal cycles and may expose bounded ordered cycle ticket IDs.

Exceptions may identify project IDs, ticket IDs, dependency ticket IDs, cycle IDs and failed invariant names. They do not include full `ProjectSpec` content, full `TicketSpec` content, validation command content or secret values.

## JSON Behavior

Standard Pydantic `model_dump()`, `model_dump_json()`, `model_validate()`, `model_validate_json()` and `model_json_schema()` are supported. JSON arrays are normalized to tuples. Filesystem serialization, YAML support, Markdown rendering, file loaders and file writers are absent.

Public models are frozen and reject unknown fields. Generated JSON Schemas set `additionalProperties: false` on public object models.

## Synthetic Linear DAG Example

```python
request = TicketPlanningRequest(
    project_spec=project_spec,
    tickets=(ticket_p16_1, ticket_p16_2),
)
plan = build_ticket_dependency_plan(request)
```

If `ticket_p16_2` has a hard internal dependency on `P16.1`, the topological order and waves place `P16.1` before `P16.2`.

## Synthetic Parallel-Wave Example

Two independent non-serial tickets with non-overlapping declared paths can share one `dependency_ready` wave. This is dependency-ready metadata only; it is not runtime execution approval.

## External Blocker Example

A ticket with a hard external dependency on `P15.9` and no resolution is directly blocked. A hard internal dependent of that ticket receives an inherited `upstream_blocked` blocker and is also excluded from waves.

## Cycle Failure Example

If `P16.1` hard-depends on `P16.2` and `P16.2` hard-depends on `P16.1`, the planner raises `DependencyCycleError` with deterministic cycle ticket IDs and no full ticket content.

## Declared-Scope Collision Example

If `P16.1` and `P16.2` both declare `src/shared.py`, the planner records an `exact_pattern` collision and separates them into different waves when both are otherwise ready.

## Ambiguous-Glob Example

If one ticket declares `src/*.py` and another declares `src/a.py`, the planner records `ambiguous_glob` evidence. The tickets may share a wave, but that wave has `scope_review_required` disposition.

## Deferred P16 Responsibilities

P16.4 owns ticket policy and linting, including semantic scope policy, full ticket policy profiles, required-section policy, authority-boundary linting, validation-command policy and deterministic lint diagnostics. P16.5 owns multi-generator synthesis and conflict review. P16.6 owns human approval and canonical publishing. P16.7 owns the historical regression corpus. P16.8 owns the shadow pilot. WorkPacket execution remains deferred to P17.
