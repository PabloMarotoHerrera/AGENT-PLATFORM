# P16.0 ProjectSpec and TicketSpec Schema Governance Record

## P16.0 Authority

P16 is Ticket Factory and Parallel Planning. P16.0 establishes only immutable planning contracts for `ProjectSpec` and `TicketSpec` in the canonical Pepper product.

These contracts are planning artifacts. They are not `WorkPacket`, `ExecutionCommand`, `ExecutionRun`, `ApprovalRequest`, `CapabilityGrant`, `AgentAssignment`, `RuntimeProfile`, `ProviderRequest`, or `RepositoryMutation` records.

## Repository and Branch State

| Item | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM` |
| Branch | `p16.0-project-ticket-spec-schema` |
| Required parent | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| Parent message | `P15.CR Close cleanup and authorize main integration` |
| HEAD at gate | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| main at gate | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| origin/main at gate | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| Worktree at gate | clean |
| Index at gate | empty |
| Visible untracked at gate | `0` |
| Registered worktrees | `1` |

## P15.CR Authority

| Item | Value |
| --- | --- |
| P15.CR commit | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| P15.CR verdict | `hermes_0_19_pepper_p15_cleanup_closed_with_main_fast_forward_authorized` |
| P15.CR is ancestor of HEAD | `true` |
| Pepper canonical product | `2_products/pepper-agent` |
| Legacy product root | absent |
| P16 unblocked | `true` |

## Canonical Pepper Identity

Pre-change Pepper integrity matched the required P15.CR parent identity:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate | `6831` | `149941138` | `2735cb45f0e087cc9dd2901ae5c1140e89ddcee886d526b0d2fbf253a13d9e50` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

The governance integrity suite reported `14` tests, `0` failures and `0` errors before implementation and after implementation.

The existing integrity utility computes committed `HEAD` blob identity. Because P16.0 is not committed by the agent, the expected post-commit Pepper identity was computed with the same v2 record-stream algorithm over the current working-tree candidate set:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate post-commit projection | `6835` | `149992431` | `ff1f82524d64b86e5bc0a76f71a16144570fb83dc0d49ef6b5e61dfa271c419b` |
| Payload post-commit projection | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record post-commit projection | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Upstream payload changed: `false`. Baseline changed: `false`. New Pepper product files: `4`.

## Schema-Only Boundary

P16.0 does not generate tickets, render Markdown, load or save specs from disk, discover repository files, inspect Git state from product code, resolve dependency graphs, detect cycles, sort tickets, assign agents, select lanes, schedule work, create or execute WorkPackets, start agents, call providers, perform OAuth, access credentials, call tools, run validation commands, modify approvals, promote capabilities, add runtime routes, modify frontend code, modify product configuration, modify dependencies, run Docker, run Graphify, modify `graphify-out`, modify `4_external/sources`, or modify Omniverse product source.

## Public Package Paths

| Path | Purpose |
| --- | --- |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py` | Public schema export boundary. |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/specs.py` | Immutable Pydantic v2 schema contracts. |

`2_products/pepper-agent/hermes_cli/agent_platform/__init__.py` was not modified. No import-time registration or runtime discovery was added.

## Public Exports

`ticket_factory.__all__` exposes exactly:

| Export |
| --- |
| `PROJECT_SPEC_SCHEMA_VERSION` |
| `TICKET_SPEC_SCHEMA_VERSION` |
| `TicketType` |
| `DependencyKind` |
| `DependencyScope` |
| `ParallelizationHint` |
| `AuthorityReferenceKind` |
| `AuthorityReferenceSpec` |
| `TicketDependencySpec` |
| `RepositoryScopeSpec` |
| `TicketValidationStepSpec` |
| `TicketResponseContractSpec` |
| `ProjectSpec` |
| `TicketSpec` |

Duplicate exports: `0`. Private helpers exported: `0`. Import side effects: `0`.

## Schema Versions

`PROJECT_SPEC_SCHEMA_VERSION = 1` and `TICKET_SPEC_SCHEMA_VERSION = 1`. `ProjectSpec.schema_version` and `TicketSpec.schema_version` are `Literal[1] = 1`. Alternative schema versions are rejected and no runtime negotiation or migration exists.

## Identifier Contracts

Project identifiers match `^P[1-9][0-9]{0,3}$`. Accepted examples: `P1`, `P16`, `P999`. Rejected examples: `p16`, `16`, `P0`, `P16.0`, `P-16`, `P16/`.

Ticket identifiers match `^P[1-9][0-9]{0,3}(?:\.[A-Z0-9]+)+$`. Accepted examples: `P16.0`, `P16.1`, `P16.0A`, `P16.R`, `P16.CR`, `P15.C3A`. Rejected examples: `P16`, `p16.0`, `P16.`, `P16..0`, `P16-0`, `P0.1`, `P16/0`.

Identifier lengths are bounded. Whitespace is rejected without rewriting. Automatic uppercasing is absent.

## Enum Contracts

| Enum | Values |
| --- | --- |
| `TicketType` | `architecture`, `documentation`, `implementation`, `refactor`, `test`, `bugfix`, `integration`, `closure` |
| `DependencyKind` | `hard_prerequisite`, `soft_predecessor` |
| `DependencyScope` | `internal_project`, `external_project` |
| `ParallelizationHint` | `unspecified`, `serial`, `parallel_candidate` |
| `AuthorityReferenceKind` | `ticket`, `governance_record`, `repository_path`, `commit`, `external_source` |

Enum aliases: `0`. Unrestricted string fields for enum values: `0`.

## Text Contracts

`ShortText` trims whitespace, rejects empty values and NUL characters, and is bounded at `512` characters. `LongText` trims whitespace, rejects empty values and NUL characters, and is bounded at `8192` characters.

`VerdictToken` matches `^[a-z0-9]+(?:_[a-z0-9]+)*$` and is bounded at `256` characters. Uppercase, spaces and hyphens are rejected.

`ValidationIdentifier` matches `^V[1-9][0-9]*$`.

## Repository Path Pattern Contract

`RepositoryPathPattern` is inert planning text. Accepted examples include `README.md`, `0_architecture/governance/**`, `2_products/pepper-agent/hermes_cli/**`, and `.gitignore`.

Rejected examples include `C:\repo\file.py`, `/absolute/path`, `../outside`, `folder/../../outside`, `folder\file.py`, and `file:`0`.

Forward slashes are required. Absolute paths, Windows drive paths, parent traversal components, NUL characters and backticks are rejected. Glob characters are permitted as inert text. Filesystem resolution and path-existence checks: `0`.

## AuthorityReferenceSpec

Field order: `kind`, `value`, `rationale`, `required`.

| Field | Type |
| --- | --- |
| `kind` | `AuthorityReferenceKind` |
| `value` | bounded non-empty text |
| `rationale` | `ShortText` |
| `required` | strict boolean, default `true` |

Duplicate kind/value pairs are rejected by containing models. Reference resolution, repository access and network access are absent.

## TicketDependencySpec

Field order: `ticket_id`, `kind`, `scope`, `rationale`.

| Field | Type |
| --- | --- |
| `ticket_id` | ticket identifier contract |
| `kind` | `DependencyKind` |
| `scope` | `DependencyScope` |
| `rationale` | `ShortText` |

Dependencies are declarative only. Target existence checks, readiness calculation, cycle detection, transitive dependency calculation and parallel inference are absent.

## RepositoryScopeSpec

Field order: `allowed_paths`, `forbidden_paths`, `allowed_actions`, `forbidden_actions`.

| Field | Type |
| --- | --- |
| `allowed_paths` | tuple of `RepositoryPathPattern` |
| `forbidden_paths` | tuple of `RepositoryPathPattern` |
| `allowed_actions` | tuple of `ShortText` |
| `forbidden_actions` | tuple of `ShortText` |

Duplicate entries per field are rejected. At least one scope field must be non-empty. Overlap resolution, glob matching and filesystem access are absent.

## TicketValidationStepSpec

Field order: `validation_id`, `description`, `command`, `expected_result`, `required`.

| Field | Type |
| --- | --- |
| `validation_id` | `ValidationIdentifier` |
| `description` | `ShortText` |
| `command` | `LongText` or `None` |
| `expected_result` | `LongText` |
| `required` | strict boolean, default `true` |

`command` may be `None`. Command text is inert. Subprocess execution, shell execution, command parsing and command-sanitization claims are absent.

## TicketResponseContractSpec

Field order: `required_sections`, `completion_verdict`, `include_files_inspected`, `include_files_modified`, `include_commands_run`, `include_tests_run`, `include_limitations`.

| Field | Type |
| --- | --- |
| `required_sections` | tuple of `ShortText` |
| `completion_verdict` | `VerdictToken` |
| `include_files_inspected` | strict boolean, default `true` |
| `include_files_modified` | strict boolean, default `true` |
| `include_commands_run` | strict boolean, default `true` |
| `include_tests_run` | strict boolean, default `true` |
| `include_limitations` | strict boolean, default `true` |

`required_sections` must be non-empty and duplicate-free. The completion verdict is an expected report token only.

## ProjectSpec

Field order: `schema_version`, `project_id`, `title`, `objective`, `summary`, `context`, `authority_references`, `scope`, `constraints`, `non_goals`, `acceptance_criteria`, `completion_verdict`.

Required non-empty collections: `context`, `acceptance_criteria`. Collections that may be empty: `authority_references`, `constraints`, `non_goals`.

Local invariants reject duplicate context entries, authority references, constraints, non-goals and acceptance criteria.

Forbidden fields: `tickets`, `ticket_specs`, `dependency_graph`, `agent_assignments`, `execution_state`, `approval_state`, `runtime_state`.

## TicketSpec

Field order: `schema_version`, `project_id`, `ticket_id`, `title`, `ticket_type`, `objective`, `context`, `authority_references`, `dependencies`, `parallelization_hint`, `scope`, `constraints`, `tasks`, `acceptance_criteria`, `validation_steps`, `response_contract`, `recommended_commit_message`.

Required non-empty collections: `context`, `tasks`, `acceptance_criteria`, `validation_steps`. Collections that may be empty: `authority_references`, `dependencies`, `constraints`.

Defaults: `parallelization_hint = unspecified`, `recommended_commit_message = None`.

Local invariants reject project-prefix mismatch, self-dependency, duplicate dependency ticket IDs, duplicate authority references, duplicate context entries, duplicate constraints, duplicate tasks, duplicate acceptance criteria and duplicate validation IDs. `project_id` is not inferred or rewritten from `ticket_id`.

## Planning-Only Parallelization Hint

ParallelizationHint is not execution authority.

`unspecified` makes no parallelization claim. `serial` records an author request for serial planning. `parallel_candidate` records a candidate for future planner analysis.

No execution lane assignment, safety proof, write-scope comparison, path-conflict detection, dependency resolution, worktree creation, agent creation or scheduling exists in P16.0.

## Serialization Boundary

Allowed serialization behavior is standard Pydantic only: `model_dump()`, `model_dump_json()`, `model_validate()`, `model_validate_json()` and `model_json_schema()`.

JSON round-trip is supported. Filesystem serialization, YAML support, Markdown rendering, canonical hashing and schema migration are absent.

## JSON Schema Evidence

Focused tests generated `ProjectSpec` and `TicketSpec` JSON Schema successfully. Public model schemas expose `additionalProperties: false`, named nested models, controlled enums, fixed schema version `1`, required fields and no unrestricted object payload. Schema generation was deterministic within the same process.

## Forbidden Schema Shapes

Public schema annotations contain zero `typing.Any`, unrestricted mapping fields, opaque payload fields, runtime object payloads, `Callable`, `Path`, `datetime`, `UUID` or bytes payload fields.

## Tests

Focused command from `2_products/pepper-agent`:

```text
python -B -m pytest -q tests/hermes_cli/test_agent_platform_ticket_factory_specs.py -p no:cacheprovider
```

Result: `96` passed, `0` failed, `0` errors, `0` unexpected skips, `0` warnings reported.

Import smoke:

```text
ProjectSpec TicketSpec
```

Governance integrity command:

```text
python -B -m unittest discover -s "12_tests/governance" -p "test_pepper_baseline_integrity.py" -v
```

Result: `14` tests, `0` failures, `0` errors.

## Static Import Scan

AST scan of `hermes_cli/agent_platform/ticket_factory/specs.py` found no imports of `subprocess`, `socket`, `requests`, `httpx`, `openai`, `pathlib.Path`, `os.environ`, `shutil`, `docker`, `git`, provider runtime modules, worker runtime modules or agent runtime modules.

File reads: `0`. File writes: `0`. Network calls: `0`. Subprocess calls: `0`. Git calls: `0`. Provider calls: `0`. Worker calls: `0`.

Ruff validation:

| Command | Result |
| --- | --- |
| `python -B -m ruff check ...` | `0` lint errors |
| `python -B -m ruff format --check ...` | `0` format errors |

Type validation: `ty_available: false`, `type_check: not_run_tool_unavailable`, `type_errors: not_asserted`, `dependency_installation: 0`.

## Modification Register

`2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` has exactly four P16.0 rows: `P16.0-001`, `P16.0-002`, `P16.0-003`, `P16.0-004`.

| ID | Destination | Recorded SHA-256 |
| --- | --- | --- |
| `P16.0-001` | `hermes_cli/agent_platform/ticket_factory/__init__.py` | `283527e194567165159b880e2262a493c7c47e674f2a1972274967ac5d56f4c1` |
| `P16.0-002` | `hermes_cli/agent_platform/ticket_factory/specs.py` | `3d80fe5013eeee46021fc575c2c723ad82a6263a3a5e77b9338defbdacee1e88` |
| `P16.0-003` | `tests/hermes_cli/test_agent_platform_ticket_factory_specs.py` | `7a998e1c3724c9d929b7a393ee18179812c19980d2f003dc9a6ffd47af1571e4` |
| `P16.0-004` | `docs/agent-platform/project_ticket_spec_schema.md` | `ec4dcfe62016ba9400cdcdf194b38b132968b62c5a06b90d1eb3426d992e5d22` |

Required authority fields match: `true`. Duplicate IDs: `0`. Duplicate paths: `0`. Missing destination paths: `0`. Hash mismatches: `0`. Unrelated row edits: `0` by intended candidate scope.

## Import Manifest

`2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` has exactly four P16.0 product-addition rows for the same four product files.

Classification: `AGENT_PLATFORM_product_addition`. Included in upstream payload: `false`. Destination hash mismatches: `0`. Duplicate concrete destinations: `0`. The governance record is not included in the Pepper import manifest.

## Operational Counters

Created Python source scan:

| Counter | Value |
| --- | ---: |
| filesystem reads | `0` |
| filesystem writes | `0` |
| subprocesses | `0` |
| shell execution | `0` |
| network calls | `0` |
| provider calls | `0` |
| OAuth actions | `0` |
| credential access | `0` |
| worker actions | `0` |
| agent actions | `0` |
| tool actions | `0` |
| WorkPacket creation | `0` |
| Git actions | `0` |
| Graphify actions | `0` |
| Docker actions | `0` |

Pydantic validation is the only runtime behavior introduced by product code.

## Secret Scan

Expected real-value counts across all seven candidates: access tokens `0`, refresh tokens `0`, authorization headers `0`, OAuth codes `0`, credential contents `0`, real auth file contents `0`, private keys `0`, API keys `0`, raw provider responses `0`, raw prompts `0`, reasoning traces `0`, personal absolute paths in product files `0`.

## Exact Candidate Set

Created product files:

| Status | Path |
| --- | --- |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py` |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/specs.py` |
| Added | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_ticket_factory_specs.py` |
| Added | `2_products/pepper-agent/docs/agent-platform/project_ticket_spec_schema.md` |

Modified product control files:

| Status | Path |
| --- | --- |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` |

Created governance record:

| Status | Path |
| --- | --- |
| Added | `0_architecture/governance/agent_platform_pepper_project_ticket_spec_schema.md` |

Candidate formula: `4` created Pepper product files plus `2` modified Pepper control files plus `1` created governance record equals `7` candidates. Created files: `5`. Modified files: `2`. Deleted files: `0`. Unexpected candidates: `0`. Frontend candidates: `0`. Backend runtime candidates: `0`. Provider candidates: `0`. Worker candidates: `0`. Omniverse candidates: `0`. External source candidates: `0`. Graphify candidates: `0`. Dependency candidates: `0`.

## P16.1 Handoff

P16.1 owns ProjectSpec collection validation, TicketSpec collection validation, internal dependency target validation, dependency cycle detection, topological ordering, canonical serialization, canonical hashing, stable collection identity, project-to-ticket association and cross-ticket scope-conflict analysis.

P16.1 must consume the committed P16.0 contracts. P16.1 must not execute tickets or create WorkPackets.

## Residual Constraints

| Item | State |
| --- | --- |
| `ProjectSpec.immutable` | `true` |
| `ProjectSpec.persisted` | `false` |
| `ProjectSpec.contains_TicketSpecs` | `false` |
| `TicketSpec.immutable` | `true` |
| `TicketSpec.persisted` | `false` |
| `TicketSpec.executable` | `false` |
| dependency graph | absent |
| parallel planner | absent |
| ticket renderer | absent |
| ticket factory generation | not implemented |
| WorkPacket | absent |
| agent assignment | absent |
| provider access | absent |
| credential access | absent |
| runtime routes | `0` |
| product UI | disabled |
| Graphify | not run by P16.0 instruction |
| P16 status | started |
| production readiness | not claimed |

Canonical verdict occurrences in this record: `1`. Alternative P16.0 verdict occurrences: `0`.

## Final Verdict

hermes_0_19_pepper_project_ticket_spec_schema_ready_with_planning_only_authority
