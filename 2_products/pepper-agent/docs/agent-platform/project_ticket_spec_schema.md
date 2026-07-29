# ProjectSpec and TicketSpec Schema

P16.0 defines the immutable planning contracts for future Pepper Ticket Factory work. The contracts are schema-only Pydantic models for `ProjectSpec` and `TicketSpec`; they do not generate tickets, render Markdown, persist specs, inspect repositories, schedule work, call providers, or execute validation commands.

## Planning Authority

`ProjectSpec` and `TicketSpec` describe planning intent. They are not `WorkPacket`, `ExecutionCommand`, `ExecutionRun`, `ApprovalRequest`, `CapabilityGrant`, `AgentAssignment`, `RuntimeProfile`, `ProviderRequest`, or `RepositoryMutation` records.

Ticket dependencies are declarative references only. A future planner may analyze them, but P16.0 does not resolve targets, calculate readiness, detect cycles, compute transitive dependencies, or topologically sort tickets.

ParallelizationHint is not execution authority. `serial` and `parallel_candidate` are author hints for future planner analysis, not claims that work can or must run in a lane.

Validation command text is inert. A `TicketValidationStepSpec.command` value records what a future human or later planner may consider, but P16.0 does not parse, sanitize, or run it.

Completion verdicts are expected report tokens. They are not human approval, governance approval, execution success authority, or merge authorization.

## Common Model Posture

All public models reject unknown fields, are frozen, validate defaults, and strip whitespace for bounded text fields. JSON arrays supplied to tuple fields are accepted by Pydantic and stored as tuples.

The only schema versions are `PROJECT_SPEC_SCHEMA_VERSION = 1` and `TICKET_SPEC_SCHEMA_VERSION = 1`. Each top-level model has `schema_version: Literal[1] = 1`, and other versions fail validation.

## ProjectSpec Fields

| Field | Type | Notes |
| --- | --- | --- |
| `schema_version` | `Literal[1]` | Defaults to `1`. |
| `project_id` | Project identifier | Matches `^P[1-9][0-9]{0,3}$`. |
| `title` | `ShortText` | Required bounded text. |
| `objective` | `LongText` | Required bounded text. |
| `summary` | `LongText` | Required bounded text. |
| `context` | tuple of `LongText` | Required, at least one entry, duplicates rejected. |
| `authority_references` | tuple of `AuthorityReferenceSpec` | May be empty, duplicate kind/value pairs rejected. |
| `scope` | `RepositoryScopeSpec` | Declarative repository scope text. |
| `constraints` | tuple of `LongText` | May be empty, duplicates rejected. |
| `non_goals` | tuple of `LongText` | May be empty, duplicates rejected. |
| `acceptance_criteria` | tuple of `LongText` | Required, at least one entry, duplicates rejected. |
| `completion_verdict` | `VerdictToken` | Expected report token only. |

`ProjectSpec` does not contain `tickets`, `ticket_specs`, `dependency_graph`, `agent_assignments`, `execution_state`, `approval_state`, or `runtime_state`. It is independent from `TicketSpec`; a later P16 contract will assemble project and ticket collections.

## TicketSpec Fields

| Field | Type | Notes |
| --- | --- | --- |
| `schema_version` | `Literal[1]` | Defaults to `1`. |
| `project_id` | Project identifier | Matches `^P[1-9][0-9]{0,3}$`. |
| `ticket_id` | Ticket identifier | Must start with `project_id + "."`. |
| `title` | `ShortText` | Required bounded text. |
| `ticket_type` | `TicketType` | Controlled enum. |
| `objective` | `LongText` | Required bounded text. |
| `context` | tuple of `LongText` | Required, at least one entry, duplicates rejected. |
| `authority_references` | tuple of `AuthorityReferenceSpec` | May be empty, duplicate kind/value pairs rejected. |
| `dependencies` | tuple of `TicketDependencySpec` | May be empty, self-dependencies and duplicate dependency IDs rejected. |
| `parallelization_hint` | `ParallelizationHint` | Defaults to `unspecified`; not execution authority. |
| `scope` | `RepositoryScopeSpec` | Declarative repository scope text. |
| `constraints` | tuple of `LongText` | May be empty, duplicates rejected. |
| `tasks` | tuple of `LongText` | Required, at least one entry, duplicates rejected. |
| `acceptance_criteria` | tuple of `LongText` | Required, at least one entry, duplicates rejected. |
| `validation_steps` | tuple of `TicketValidationStepSpec` | Required, at least one entry, duplicate validation IDs rejected. |
| `response_contract` | `TicketResponseContractSpec` | Expected response shape and completion verdict. |
| `recommended_commit_message` | `ShortText` or `None` | Defaults to `None`. |

## Nested Models

### AuthorityReferenceSpec

| Field | Type | Notes |
| --- | --- | --- |
| `kind` | `AuthorityReferenceKind` | Controlled enum. |
| `value` | `ShortText` | Bounded non-empty provenance value. |
| `rationale` | `ShortText` | Why the reference matters. |
| `required` | strict boolean | Defaults to `true`. |

Authority references are descriptive provenance only. P16.0 performs no reference resolution, repository access, or network access.

### TicketDependencySpec

| Field | Type | Notes |
| --- | --- | --- |
| `ticket_id` | Ticket identifier | Declarative target ID. |
| `kind` | `DependencyKind` | Controlled enum. |
| `scope` | `DependencyScope` | Internal or external project reference. |
| `rationale` | `ShortText` | Why the dependency is declared. |

### RepositoryScopeSpec

| Field | Type | Notes |
| --- | --- | --- |
| `allowed_paths` | tuple of `RepositoryPathPattern` | Duplicate entries rejected. |
| `forbidden_paths` | tuple of `RepositoryPathPattern` | Duplicate entries rejected. |
| `allowed_actions` | tuple of `ShortText` | Duplicate entries rejected. |
| `forbidden_actions` | tuple of `ShortText` | Duplicate entries rejected. |

At least one scope field must be non-empty. P16.0 performs no overlap resolution, glob matching, filesystem access, or path existence checks.

### TicketValidationStepSpec

| Field | Type | Notes |
| --- | --- | --- |
| `validation_id` | `ValidationIdentifier` | Matches `^V[1-9][0-9]*$`. |
| `description` | `ShortText` | Required bounded text. |
| `command` | `LongText` or `None` | Inert specification text. |
| `expected_result` | `LongText` | Required bounded text. |
| `required` | strict boolean | Defaults to `true`. |

### TicketResponseContractSpec

| Field | Type | Notes |
| --- | --- | --- |
| `required_sections` | tuple of `ShortText` | Required, non-empty, duplicates rejected. |
| `completion_verdict` | `VerdictToken` | Expected report token only. |
| `include_files_inspected` | strict boolean | Defaults to `true`. |
| `include_files_modified` | strict boolean | Defaults to `true`. |
| `include_commands_run` | strict boolean | Defaults to `true`. |
| `include_tests_run` | strict boolean | Defaults to `true`. |
| `include_limitations` | strict boolean | Defaults to `true`. |

## Controlled Enums

| Enum | Values |
| --- | --- |
| `TicketType` | `architecture`, `documentation`, `implementation`, `refactor`, `test`, `bugfix`, `integration`, `closure` |
| `DependencyKind` | `hard_prerequisite`, `soft_predecessor` |
| `DependencyScope` | `internal_project`, `external_project` |
| `ParallelizationHint` | `unspecified`, `serial`, `parallel_candidate` |
| `AuthorityReferenceKind` | `ticket`, `governance_record`, `repository_path`, `commit`, `external_source` |

## Identifier Rules

Project identifiers match `^P[1-9][0-9]{0,3}$`. Accepted synthetic examples: `P1`, `P16`, `P999`. Rejected examples: `p16`, `16`, `P0`, `P16.0`, `P-16`, `P16/`.

Ticket identifiers match `^P[1-9][0-9]{0,3}(?:\.[A-Z0-9]+)+$`. Accepted synthetic examples: `P16.0`, `P16.1`, `P16.0A`, `P16.R`, `P16.CR`, `P15.C3A`. Rejected examples: `P16`, `p16.0`, `P16.`, `P16..0`, `P16-0`, `P0.1`, `P16/0`.

Whitespace in identifiers is rejected rather than rewritten, and identifiers are not automatically uppercased.

## Text Rules

`ShortText` trims whitespace, rejects empty strings and NUL characters, and is bounded at 512 characters. `LongText` trims whitespace, rejects empty strings and NUL characters, and is bounded at 8192 characters.

`VerdictToken` matches `^[a-z0-9]+(?:_[a-z0-9]+)*$` and is bounded at 256 characters. Uppercase letters, spaces, and hyphens are rejected.

`ValidationIdentifier` matches `^V[1-9][0-9]*$`.

## Repository Path Patterns

Repository path patterns are descriptive planning data. Accepted examples include `README.md`, `0_architecture/governance/**`, `2_products/pepper-agent/hermes_cli/**`, and `.gitignore`.

Rejected examples include `C:\repo\file.py`, `/absolute/path`, `../outside`, `folder/../../outside`, `folder\file.py`, and `file:`0`. Forward slashes are required, absolute paths are rejected, Windows drive paths are rejected, parent traversal components are rejected, and glob characters are permitted as inert text.

## Serialization and JSON Schema

P16.0 relies only on standard Pydantic behavior: `model_dump()`, `model_dump_json()`, `model_validate()`, `model_validate_json()`, and `model_json_schema()`. JSON round-trip is supported through those APIs.

Generated JSON Schemas include named nested models, controlled enums, fixed schema version `1`, and `additionalProperties: false` for public models. Generated schema determinism is scoped to the same process and dependency version. P16.0 does not add generated schema snapshots, YAML support, Markdown rendering, canonical hashing, file loaders, file writers, or schema migration.

## Valid ProjectSpec Example

```python
from hermes_cli.agent_platform.ticket_factory import (
    AuthorityReferenceKind,
    AuthorityReferenceSpec,
    ProjectSpec,
    RepositoryScopeSpec,
)

project = ProjectSpec(
    project_id="P16",
    title="Synthetic planning project",
    objective="Define immutable planning contracts for a synthetic project.",
    summary="The project records planning intent without containing tickets.",
    context=("A synthetic context entry explains the planning boundary.",),
    authority_references=(
        AuthorityReferenceSpec(
            kind=AuthorityReferenceKind.GOVERNANCE_RECORD,
            value="0_architecture/governance/example.md",
            rationale="Synthetic provenance for the example.",
        ),
    ),
    scope=RepositoryScopeSpec(
        allowed_paths=("2_products/pepper-agent/hermes_cli/**",),
        forbidden_paths=("4_external/sources/**",),
        allowed_actions=("edit schema contracts",),
        forbidden_actions=("execute tickets",),
    ),
    constraints=("No runtime execution behavior is authorized.",),
    non_goals=("Ticket rendering is deferred.",),
    acceptance_criteria=("The schema validates local planning invariants.",),
    completion_verdict="synthetic_project_ready",
)
```

## Valid TicketSpec Example

```python
from hermes_cli.agent_platform.ticket_factory import (
    DependencyKind,
    DependencyScope,
    ParallelizationHint,
    TicketDependencySpec,
    TicketResponseContractSpec,
    TicketSpec,
    TicketType,
    TicketValidationStepSpec,
)

ticket = TicketSpec(
    project_id="P16",
    ticket_id="P16.0",
    title="Synthetic schema ticket",
    ticket_type=TicketType.IMPLEMENTATION,
    objective="Define immutable ticket planning data.",
    context=("A synthetic ticket context entry.",),
    authority_references=(),
    dependencies=(
        TicketDependencySpec(
            ticket_id="P16.1",
            kind=DependencyKind.SOFT_PREDECESSOR,
            scope=DependencyScope.INTERNAL_PROJECT,
            rationale="Synthetic declarative dependency.",
        ),
    ),
    parallelization_hint=ParallelizationHint.PARALLEL_CANDIDATE,
    scope=project.scope,
    constraints=("Validation commands remain inert text.",),
    tasks=("Create immutable schema contracts.",),
    acceptance_criteria=("The ticket validates without execution.",),
    validation_steps=(
        TicketValidationStepSpec(
            validation_id="V1",
            description="Inspect the synthetic schema behavior.",
            command=None,
            expected_result="The inspection reports the schema contract only.",
        ),
    ),
    response_contract=TicketResponseContractSpec(
        required_sections=("Summary", "Tests"),
        completion_verdict="synthetic_ticket_ready",
    ),
)
```

## Invalid Examples

The following fail validation: `project_id="p16"`, `project_id="P0"`, `ticket_id="P16"`, `ticket_id="P16-0"`, `completion_verdict="Synthetic Ready"`, duplicate context entries, duplicate authority kind/value pairs, duplicate dependency ticket IDs, self-dependencies, duplicate validation IDs, empty required collections, unknown fields, `allowed_paths=("../outside",)`, and boolean fields supplied as strings such as `"true"`.

## Deferred Behavior

P16.1 owns ProjectSpec collection validation, TicketSpec collection validation, internal dependency target validation, dependency cycle detection, topological ordering, canonical serialization, canonical hashing, stable collection identity, project-to-ticket association, and cross-ticket scope-conflict analysis.

P16.1 must consume the committed P16.0 contracts. Ticket generation remains absent, parallel planning remains absent, and WorkPacket execution remains deferred to P17.
