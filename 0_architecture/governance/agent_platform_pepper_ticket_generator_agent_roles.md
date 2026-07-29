# P16.2 Ticket Generator Agent Roles Governance Record

## P16.2 Authority

P16 is Ticket Factory and Parallel Planning. P16.2 adds only immutable, non-executing ticket-generator role contracts for Pepper planning specs.

The P16.2 contracts consume one P16.0 `ProjectSpec`, one P16.0 `TicketSpec`, one P16.1 `ContextPack` and explicit requested generator roles. They prepare deterministic in-memory `GeneratorAssignment` records and validate independently supplied `TicketProposal` envelopes.

P16.2 is not a prompt renderer, provider request, agent runner, generated canonical ticket, dependency DAG, ticket linter, proposal synthesizer, approval record, publication record, WorkPacket, runtime adapter, repository scanner or execution plan.

## Repository and Branch State

| Item | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM` |
| Branch | `p16.2-ticket-generator-agent-roles` |
| Required parent | `583eae1560d56360efd1cf43459cce9823310034` |
| Parent message | `P16.1 Add bounded Context Pack assembler` |
| HEAD at implementation | `583eae1560d56360efd1cf43459cce9823310034` |
| main at implementation | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| origin/main at implementation | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| Registered worktrees | `1` |

The P16.2 candidate remains uncommitted by instruction. No staging, commit, push, branch switch, reset, clean, stash, Docker command, dependency update, lockfile update, Graphify command or `graphify-out` modification was performed.

## P16.0 And P16.1 Dependencies

| Item | Value |
| --- | --- |
| P16.0 verdict | `hermes_0_19_pepper_project_ticket_spec_schema_ready_with_planning_only_authority` |
| P16.1 commit | `583eae1560d56360efd1cf43459cce9823310034` |
| P16.1 verdict | `hermes_0_19_pepper_context_pack_assembler_ready_with_bounded_in_memory_authority` |
| P16.0 schema module modified by P16.2 | `false` |
| P16.1 context-pack module modified by P16.2 | `false` |
| P16.0 tests modified by P16.2 | `false` |
| P16.1 tests modified by P16.2 | `false` |

P16.2 consumes P16.0 and P16.1 through public imports only. It does not change `specs.py`, `context_packs.py`, or their focused tests.

## Canonical Pepper Identity

Pre-change P16.2 Pepper identity matched the committed P16.1 parent projection:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate | `6838` | `150069044` | `b5b134c74aad812e37774743823733354ac3d8a9305f02247c6c37c0afa0bb45` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

The existing integrity utility computes committed `HEAD` blob identity. Because P16.2 is not committed by the agent, the expected post-commit Pepper identity was computed with the same v2 record-stream algorithm over the current working-tree candidate set:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate post-commit projection | `6841` | `150155984` | `6bc2ddf83cfade21e166e320ad8149bb50a33355e6edd4164e6b47808dcd0662` |
| Payload post-commit projection | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record post-commit projection | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Upstream payload changed: `false`. Baseline changed: `false`. New Pepper product files: `3`.

## Product Boundary

P16.2 adds no runtime routes, frontend code, provider configuration, credentials, workers, tools, MCP servers, scheduler entries, repository mutation authority, dependency graph authority, ticket linting authority, proposal synthesis authority, approval authority, publication authority or WorkPacket authority.

All proposal content is supplied by the caller to `build_ticket_proposal()`. The product code packages and validates proposal binding only. It does not ask a model for proposal content, improve proposal content, choose a winner, merge proposals or publish a canonical ticket.

## Public Package Paths

| Path | Purpose |
| --- | --- |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py` | Public Ticket Factory export boundary extended additively for P16.2. |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/generator_roles.py` | Immutable P16.2 role, assignment and proposal contracts. |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/specs.py` | Unmodified P16.0 ProjectSpec and TicketSpec contracts consumed by P16.2. |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/context_packs.py` | Unmodified P16.1 ContextPack contracts consumed by P16.2. |

`2_products/pepper-agent/hermes_cli/agent_platform/__init__.py` was not modified. No import-time registration or runtime discovery was added.

## P16.2 Public Exports

The P16.2 exports are additive and preserve relative order within the P16.2 subset:

| Export |
| --- |
| `TICKET_GENERATOR_ROLE_SCHEMA_VERSION` |
| `TicketGeneratorRole` |
| `GeneratorRoleProfile` |
| `TicketGenerationRequest` |
| `GeneratorAssignment` |
| `TicketProposal` |
| `TicketGeneratorRoleError` |
| `TicketGeneratorCompatibilityError` |
| `TicketProposalValidationError` |
| `get_ticket_generator_role_profile` |
| `list_ticket_generator_role_profiles` |
| `prepare_ticket_generator_assignments` |
| `build_ticket_proposal` |
| `validate_ticket_generator_proposal` |

Duplicate exports: `0`. Private helpers exported: `0`. Import side effects: `0`.

## Schema Version

`TICKET_GENERATOR_ROLE_SCHEMA_VERSION = 1`. `GeneratorAssignment.schema_version` and `TicketProposal.schema_version` are fixed to `Literal[1] = 1`. Alternative generator-role schema versions are rejected. No version negotiation or migration exists.

## Role Taxonomy

| Role | Primary Ticket Types | Supported Ticket Types |
| --- | --- | --- |
| `architecture` | `architecture`, `refactor` | `architecture`, `documentation`, `implementation`, `refactor`, `integration` |
| `implementation` | `implementation`, `bugfix` | `implementation`, `refactor`, `test`, `bugfix`, `integration` |
| `validation` | `test` | `implementation`, `test`, `bugfix`, `integration`, `closure` |
| `integration` | `integration` | `architecture`, `implementation`, `test`, `integration`, `closure` |
| `governance` | `closure` | `architecture`, `documentation`, `test`, `integration`, `closure` |
| `documentation` | `documentation` | `architecture`, `documentation`, `integration`, `closure` |

Role enum aliases: `0`. Canonical profiles: `6`. Every P16.0 `TicketType` has at least one primary generator role.

## GeneratorRoleProfile Contract

Field order: `role`, `title`, `objective`, `focus_areas`, `required_checks`, `prohibited_claims`, `primary_ticket_types`, `supported_ticket_types`.

Profiles are frozen, extra-forbid Pydantic models. Focus areas, required checks, prohibited claims, primary ticket types and supported ticket types reject duplicates. Primary ticket types must be a subset of supported ticket types.

## TicketGenerationRequest Contract

Field order: `project_spec`, `ticket_spec`, `context_pack`, `roles`.

`project_spec.project_id` must equal `ticket_spec.project_id`. `context_pack.project_id` must equal `ticket_spec.project_id`. `context_pack.ticket_id` must equal `ticket_spec.ticket_id`.

`roles` is bounded to one through six roles. Duplicate roles are rejected. Every requested role must support the request ticket type, and at least one requested role must be primary for the request ticket type.

Pydantic wraps model-validator compatibility errors as `ValidationError`. The underlying compatibility error type remains bounded under `TicketGeneratorRoleError` for direct compatibility checks and proposal validation paths.

## GeneratorAssignment Contract

Field order: `schema_version`, `assignment_id`, `role`, `project_id`, `ticket_id`, `ticket_type`, `input_SHA256`, `role_profile`, `assignment_SHA256`.

`prepare_ticket_generator_assignments(request)` returns assignments in canonical role order, not caller input order. One role creates one assignment. Role permutations produce the same assignment sequence and digests.

`assignment_id` uses the deterministic form `GEN-<ticket_id-with-dots-replaced-by-dashes>-<ROLE>`. The assignment validates ticket/project prefix, canonical role profile equality, ticket-type support and assignment digest equality.

## TicketProposal Contract

Field order: `schema_version`, `assignment_id`, `assignment_SHA256`, `role`, `project_id`, `ticket_id`, `proposed_ticket`, `rationale`, `evidence_source_ids`, `assumptions`, `risks`, `unresolved_questions`, `proposal_SHA256`.

`build_ticket_proposal()` accepts externally supplied proposal content. The proposed ticket must match the assignment project ID, ticket ID and ticket type. Duplicate evidence IDs, assumptions, risks and unresolved questions are rejected. Evidence IDs must match the bounded `CTX-...` context-source identifier contract.

`TicketProposal` is an independent envelope. It has no approved, published, canonical, execution, WorkPacket, prompt, provider, model, worker or scheduler fields.

## Proposal Validation Boundary

`validate_ticket_generator_proposal(request, proposal)` verifies requested role membership, request assignment identity, assignment digest, project ID, ticket ID, proposed ticket identity, proposed ticket type, role support, context-pack evidence source membership and proposal digest.

Validation does not lint ticket semantics, approve proposals, publish proposals, synthesize a merged ticket, inspect files, fetch evidence, run commands, create WorkPackets or call providers.

Validation errors report bounded identifiers and categories only. Ticket objective text, context source content, proposal rationale and raw evidence content are not echoed in errors.

## Digest Boundary

The input digest algorithm is `agent-platform-ticket-generator-input-sha256-v1`. The assignment digest algorithm is `agent-platform-ticket-generator-assignment-sha256-v1`. The proposal digest algorithm is `agent-platform-ticket-proposal-sha256-v1`.

All digests are lowercase SHA-256 hex strings over deterministic JSON records. Input digests cover `ProjectSpec`, `TicketSpec` and `ContextPack`. Assignment digests cover assignment identity, role, ticket identity, ticket type, input digest and canonical role profile. Proposal digests cover proposal binding fields and proposal content and exclude `proposal_SHA256` itself.

These digests are reproducibility evidence only. They are not canonical published ticket identities, approval signatures, execution identities or security signatures.

## Serialization Boundary

Allowed serialization behavior is standard Pydantic only: `model_dump()`, `model_dump_json()`, `model_validate()`, `model_validate_json()` and `model_json_schema()`.

Filesystem serialization, YAML support, Markdown rendering, file loaders and file writers are absent.

## Tests

Focused P16.2 command from `2_products/pepper-agent`:

```text
python -m pytest -q tests/hermes_cli/test_agent_platform_ticket_factory_generator_roles.py -p no:cacheprovider
```

Result: `120` passed, `0` failed, `0` errors, `0` unexpected skips, `0` warnings reported.

Focused combined P16.0/P16.1/P16.2 command from `2_products/pepper-agent`:

```text
python -m pytest -q tests/hermes_cli/test_agent_platform_ticket_factory_specs.py tests/hermes_cli/test_agent_platform_ticket_factory_context_packs.py tests/hermes_cli/test_agent_platform_ticket_factory_generator_roles.py -p no:cacheprovider
```

Result: `291` passed, `0` failed, `0` errors, `0` unexpected skips, `0` warnings reported.

Governance integrity command from repository root:

```text
python -B -m unittest discover -s "12_tests/governance" -p "test_pepper_baseline_integrity.py" -v
```

Result: `14` tests, `0` failures, `0` errors.

Import smoke from `2_products/pepper-agent`:

```text
ProjectSpec TicketSpec ContextPack TicketGeneratorRole TicketProposal prepare_ticket_generator_assignments
```

## Ruff Validation

| Command | Result |
| --- | --- |
| `python -m ruff format ...` | `2` P16.2 Python files reformatted and `1` file left unchanged |
| `python -m ruff check ...` | `0` lint errors |
| `python -m ruff format --check ...` | `0` format errors |

Type validation: `ty_available: false`, `type_check: not_run_tool_unavailable`, `type_errors: not_asserted`, `dependency_installation: 0`.

## Static Boundary Scan

Focused scan of P16.2 product code found no imports of `subprocess`, `socket`, `requests`, `httpx`, `openai`, `Path`, `os.environ`, `shutil`, `docker`, `git`, provider runtime modules, worker runtime modules or agent runtime modules.

Focused public-surface tests found no callable file loader, file writer, command executor, scheduler, publisher, WorkPacket, execution, runtime, provider request, prompt template, agent assignment, dependency graph, ticket linter, proposal synthesizer, approval or publication surface.

File reads from P16.2 product code: `0`. File writes from P16.2 product code: `0`. Network calls: `0`. Subprocess calls: `0`. Git calls: `0`. Provider calls: `0`. Worker calls: `0`.

## Secret Scan

Focused secret-shape scan across the six P16.2 product candidates reported `P16_2_SECRET_SHAPE_SCAN_OK` with candidate findings `0`.

No real API keys, provider tokens, bearer headers, refresh tokens, private keys, raw provider responses, raw prompts, reasoning traces or credential contents were introduced by P16.2.

## Product File Hashes

| Path | SHA-256 |
| --- | --- |
| `hermes_cli/agent_platform/ticket_factory/__init__.py` | `d397b895421ae1e1bfdc1ea2162e934e2fe0cc6ca82f8b6aff1a0b5cca366414` |
| `hermes_cli/agent_platform/ticket_factory/generator_roles.py` | `9cdca9ff7ddbd1424d8e97e6dbd9edd2f43822bd0018d40c140776c220d89752` |
| `tests/hermes_cli/test_agent_platform_ticket_factory_generator_roles.py` | `190f42dbded0f0b01a3a1a7e59ba5bcf2eb368d8b9c7dc8639643986d1fcb9cd` |
| `docs/agent-platform/ticket_generator_agent_roles.md` | `0772254d4c10eb917f864634caacd4994670b519b8aaf391ae5317bd28623733` |
| `AGENT_PLATFORM_MODIFICATIONS.tsv` | `f0f4d5628ddbeff1f95e3f5d8983a8f6af1a5a4caa51e6f4b930c8971eb12085` |
| `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | `9dc4c1cc8faa36b3c4a274325d415fdbd8ab9c9e47c5d189567a072c23019415` |

## Modification Register

`2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` records three P16.2 product-addition rows: `P16.2-001`, `P16.2-002`, `P16.2-003`.

Existing P16.0 row `P16.0-001` for `hermes_cli/agent_platform/ticket_factory/__init__.py` was updated to the current hash and additive P16.2 export intent. Duplicate modification IDs: `0`. Missing destination paths: `0`. Hash mismatches for P16.2 rows and the updated `P16.0-001` row: `0`.

## Import Manifest

`2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` records three new P16.2 product-addition rows for the generator-role source, test and documentation files.

Existing manifest row for `hermes_cli/agent_platform/ticket_factory/__init__.py` was updated to the current destination hash and additive P16.2 export rule. The governance record is not included in the Pepper import manifest. Duplicate concrete destinations: `0`. Hash mismatches for P16.2 rows and the updated `__init__.py` row: `0`.

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
| agent actions by product code | `0` |
| tool actions by product code | `0` |
| WorkPacket creation by product code | `0` |
| approval actions by product code | `0` |
| publication actions by product code | `0` |
| Git actions by product code | `0` |
| Graphify actions | `0` |
| Docker actions | `0` |

Pydantic validation, deterministic JSON materialization, in-memory sorting and SHA-256 calculation are the only runtime behaviors introduced by P16.2 product code.

## Exact Candidate Set

Created Pepper product files:

| Status | Path |
| --- | --- |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/generator_roles.py` |
| Added | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_ticket_factory_generator_roles.py` |
| Added | `2_products/pepper-agent/docs/agent-platform/ticket_generator_agent_roles.md` |

Modified Pepper product files:

| Status | Path |
| --- | --- |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` |
| Modified | `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py` |

Created governance record:

| Status | Path |
| --- | --- |
| Added | `0_architecture/governance/agent_platform_pepper_ticket_generator_agent_roles.md` |

Candidate formula: `3` created Pepper product files plus `3` modified Pepper product files plus `1` created governance record equals `7` candidates. Created files: `4`. Modified files: `3`. Deleted files: `0`. Unexpected candidates: `0`. Frontend candidates: `0`. Backend runtime candidates: `0`. Provider candidates: `0`. Worker candidates: `0`. Omniverse candidates: `0`. External source candidates: `0`. Graphify candidates: `0`. Dependency candidates: `0`.

## Deferred Responsibilities

P16.3 owns dependency DAGs, cycle detection, topological ordering and parallel wave planning. P16.4 owns ticket policy and linting. P16.5 owns multi-generator synthesis and conflict review. P16.6 owns human approval and canonical publishing. WorkPacket execution remains deferred to P17.

## Residual Constraints

| Item | State |
| --- | --- |
| ProjectSpec modified | `false` |
| TicketSpec modified | `false` |
| ContextPack modified | `false` |
| ContextPack persisted | `false` |
| generator roles executable | `false` |
| proposal content generated by product code | `false` |
| prompt rendering | absent |
| provider access | absent |
| agent execution | absent |
| repository file loading | absent |
| URL fetching | absent |
| semantic search | absent |
| dependency graph | absent |
| parallel planner | absent |
| ticket linter | absent |
| proposal synthesizer | absent |
| human approval | absent |
| canonical publication | absent |
| WorkPacket | absent |
| credential access | absent |
| runtime routes | `0` |
| product UI | disabled |
| Graphify | not run by P16.2 instruction |
| production readiness | not claimed |

Canonical verdict occurrences in this record: `1`. Alternative P16.2 verdict occurrences: `0`.

## Final Verdict

hermes_0_19_pepper_ticket_generator_agent_roles_ready_with_non_executing_proposal_authority
