# Ticket Generator Agent Roles

P16.2 adds non-executing ticket-generator role contracts for Pepper Ticket Factory planning. It builds on the P16.0 `ProjectSpec` and `TicketSpec` contracts and the P16.1 `ContextPack` contract to prepare deterministic in-memory generator assignments and validate independently supplied ticket proposals.

P16.2 does not run agents, call providers, render prompts, synthesize canonical tickets, lint tickets, approve proposals, publish tickets, resolve dependency DAGs, create WorkPackets, inspect repositories, read files, write files, fetch URLs or schedule work.

## Relationship To P16.0 And P16.1

P16.0 owns the immutable planning specs. P16.1 owns bounded in-memory context-pack assembly. P16.2 consumes one `ProjectSpec`, one `TicketSpec` and one `ContextPack` that all refer to the same project and ticket.

P16.2 adds `generator_roles.py` under the existing `ticket_factory` package and extends the package export boundary additively. It does not modify the P16.0 schema module or the P16.1 context-pack module.

## Non-Executing Authority

The P16.2 product code accepts already-materialized planning inputs. It creates immutable role profiles, request records, assignment records and proposal records in memory. It validates identity and digest binding between those records.

The product code does not generate proposal content. `build_ticket_proposal()` packages externally supplied proposal content into a bounded `TicketProposal`. `validate_ticket_generator_proposal()` checks that the proposal binds to the request, assignment and included context evidence. It does not judge quality, approve, publish or execute the proposal.

## Public Exports

P16.2 adds these public exports:

| Export | Purpose |
| --- | --- |
| `TICKET_GENERATOR_ROLE_SCHEMA_VERSION` | Fixed schema version, currently `1`. |
| `TicketGeneratorRole` | Canonical generator-role enum. |
| `GeneratorRoleProfile` | Immutable canonical role-profile contract. |
| `TicketGenerationRequest` | Input bundle for assignment preparation. |
| `GeneratorAssignment` | Deterministic role assignment bound to one request digest. |
| `TicketProposal` | Independent proposal envelope bound to one assignment. |
| `TicketGeneratorRoleError` | Base bounded role-contract error. |
| `TicketGeneratorCompatibilityError` | Role and ticket-type compatibility error. |
| `TicketProposalValidationError` | Proposal binding validation error. |
| `get_ticket_generator_role_profile()` | Return one canonical profile. |
| `list_ticket_generator_role_profiles()` | Return all canonical profiles in canonical order. |
| `prepare_ticket_generator_assignments()` | Build deterministic in-memory assignments. |
| `build_ticket_proposal()` | Package externally supplied proposal content. |
| `validate_ticket_generator_proposal()` | Validate proposal binding against a request. |

Digest algorithm constants and private helpers are not public exports.

## Role Taxonomy

`TicketGeneratorRole` values are ordered canonically as:

| Role | Primary Ticket Types | Supported Ticket Types |
| --- | --- | --- |
| `architecture` | `architecture`, `refactor` | `architecture`, `documentation`, `implementation`, `refactor`, `integration` |
| `implementation` | `implementation`, `bugfix` | `implementation`, `refactor`, `test`, `bugfix`, `integration` |
| `validation` | `test` | `implementation`, `test`, `bugfix`, `integration`, `closure` |
| `integration` | `integration` | `architecture`, `implementation`, `test`, `integration`, `closure` |
| `governance` | `closure` | `architecture`, `documentation`, `test`, `integration`, `closure` |
| `documentation` | `documentation` | `architecture`, `documentation`, `integration`, `closure` |

Each role has one immutable `GeneratorRoleProfile` with a title, objective, focus areas, required checks, prohibited claims, primary ticket types and supported ticket types. Profile collection fields reject duplicates. Primary ticket types must be a subset of supported ticket types.

## TicketGenerationRequest

Field order: `project_spec`, `ticket_spec`, `context_pack`, `roles`.

The request requires matching identifiers across its inputs:

| Relationship | Required Match |
| --- | --- |
| `project_spec.project_id` | `ticket_spec.project_id` |
| `context_pack.project_id` | `ticket_spec.project_id` |
| `context_pack.ticket_id` | `ticket_spec.ticket_id` |

`roles` is a tuple of one to six `TicketGeneratorRole` values. Duplicate roles are rejected. Every requested role must support the request ticket type, and at least one requested role must list that ticket type as primary.

Request construction is validation only. It does not allocate workers, start agents or render prompts.

## GeneratorAssignment

Field order: `schema_version`, `assignment_id`, `role`, `project_id`, `ticket_id`, `ticket_type`, `input_SHA256`, `role_profile`, `assignment_SHA256`.

`prepare_ticket_generator_assignments(request)` sorts requested roles by canonical role order and returns one assignment per role. Input role order is not assignment-order authority.

`assignment_id` is deterministic and uses the form `GEN-<ticket_id-with-dots-replaced-by-dashes>-<ROLE>`. Example: `P16.2` with `implementation` becomes `GEN-P16-2-IMPLEMENTATION`.

`input_SHA256` is a SHA-256 digest over a deterministic JSON record containing the `ProjectSpec`, `TicketSpec` and `ContextPack`. It is shared by all assignments from the same request and changes when any request input changes.

`assignment_SHA256` is a SHA-256 digest over the assignment identity, role, ticket identity, ticket type, input digest and canonical role profile. It is role-specific and changes across role assignments.

Assignment digests are reproducibility evidence only. They are not approval signatures, publication identities, execution identities or security signatures.

## TicketProposal

Field order: `schema_version`, `assignment_id`, `assignment_SHA256`, `role`, `project_id`, `ticket_id`, `proposed_ticket`, `rationale`, `evidence_source_ids`, `assumptions`, `risks`, `unresolved_questions`, `proposal_SHA256`.

`build_ticket_proposal()` accepts one `GeneratorAssignment`, one externally supplied `TicketSpec`, a rationale, one or more context evidence source IDs and optional assumption, risk and unresolved-question tuples.

The proposed ticket must match the assignment project ID, ticket ID and ticket type. The assignment role must support that ticket type. Duplicate evidence IDs, assumptions, risks and unresolved questions are rejected.

`proposal_SHA256` is a SHA-256 digest over the proposal binding fields and proposal content. It excludes `proposal_SHA256` itself.

P16.2 does not require the proposed ticket to differ from the input `TicketSpec`. It packages and binds external proposal content; it does not synthesize or improve that content.

## Proposal Validation

`validate_ticket_generator_proposal(request, proposal)` verifies:

| Check | Boundary |
| --- | --- |
| requested role | proposal role must be one of `request.roles` |
| assignment ID | assignment must exist for the request |
| assignment digest | proposal assignment digest must match the request assignment |
| project and ticket IDs | proposal identity must match the request ticket identity |
| proposed ticket identity | proposed ticket project and ticket IDs must match the proposal |
| ticket type | proposed ticket type must match the request ticket type |
| role support | proposal role must support the proposed ticket type |
| context evidence | every evidence source ID must be included in the `ContextPack` |
| proposal digest | proposal digest must match the proposal record |

Validation errors report bounded identifiers and categories. They do not echo ticket objective text, context content, proposal rationale or source content.

Proposal validation is not a linter, reviewer, approver, publisher, dependency analyzer, conflict resolver or WorkPacket creator.

## JSON Behavior

Standard Pydantic `model_dump()`, `model_dump_json()`, `model_validate()`, `model_validate_json()` and `model_json_schema()` are supported. JSON arrays are normalized to tuples. Filesystem serialization, YAML support, Markdown rendering, file loaders and file writers are absent.

Public models are frozen and reject unknown fields. Generated JSON Schemas set `additionalProperties: false` on public object models.

## Synthetic Example

```python
from hermes_cli.agent_platform.ticket_factory import (
    TicketGenerationRequest,
    TicketGeneratorRole,
    build_ticket_proposal,
    prepare_ticket_generator_assignments,
    validate_ticket_generator_proposal,
)

request = TicketGenerationRequest(
    project_spec=project_spec,
    ticket_spec=ticket_spec,
    context_pack=context_pack,
    roles=(TicketGeneratorRole.IMPLEMENTATION,),
)
assignment = prepare_ticket_generator_assignments(request)[0]

proposal = build_ticket_proposal(
    assignment=assignment,
    proposed_ticket=proposed_ticket,
    rationale="Synthetic externally supplied rationale.",
    evidence_source_ids=("CTX-PROJECT-SPEC",),
)

validated = validate_ticket_generator_proposal(request, proposal)
```

The example assumes `project_spec`, `ticket_spec`, `context_pack` and `proposed_ticket` were constructed by the caller. P16.2 does not load them from disk or generate them from a prompt.

## Deferred P16 Responsibilities

P16.3 owns dependency DAGs, cycle detection, topological ordering and parallel wave planning. P16.4 owns ticket policy and linting. P16.5 owns multi-generator synthesis and conflict review. P16.6 owns human approval and canonical publishing. WorkPacket execution remains deferred to P17.
