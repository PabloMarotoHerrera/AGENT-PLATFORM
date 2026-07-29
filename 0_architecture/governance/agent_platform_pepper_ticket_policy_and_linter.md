# P16.4 Ticket Policy And Linter Governance Record

## P16.4 Authority

P16 is Ticket Factory and Parallel Planning. P16.4 adds only deterministic, immutable and non-mutating policy linting for Pepper `ProjectSpec`, `TicketSpec` collections and optional `TicketDependencyPlan` evidence.

The linter consumes one P16.0 `ProjectSpec`, a bounded collection of P16.0 `TicketSpec` objects, an optional P16.3 `TicketDependencyPlan`, an explicit collection-completeness declaration and the single canonical governed-standard policy profile. It produces typed diagnostics, ticket and collection summaries, a deterministic disposition and reproducible input/report digests.

P16.4 is not ticket generation, ticket repair, dependency-plan construction, parallel-wave mutation, proposal synthesis, human approval, canonical publication, prompt rendering, provider access, validation-command execution, repository scanning, worktree allocation or WorkPacket creation.

`TicketLintReport` is policy evidence, not approval or publication authority.

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
| Resolved P16.3 commit | `63389998ea1096f3f93291b60a9793ba140abc0b` |
| P16.3 commit message | `P16.3 Add dependency DAG and parallel wave planner` |
| HEAD at implementation | `63389998ea1096f3f93291b60a9793ba140abc0b` |
| Remote P16 at implementation | `63389998ea1096f3f93291b60a9793ba140abc0b` |
| P16.3 is ancestor of remote P16 | `true` |
| main at implementation | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| origin/main at implementation | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| Worktree at gate | clean |
| Index at gate | empty |
| Visible untracked at gate | `0` |
| Registered worktrees | `1` |
| Pepper root | present |
| Legacy Hermes root | absent |
| Omniverse tracked product files | `369` |

The P16.4 candidate remains uncommitted by instruction. No staging, commit, push, branch switch, reset, clean, stash, Docker command, dependency update, lockfile update, Graphify command or `graphify-out` modification was performed.

## Prerequisite Verdicts

| Prerequisite | Verdict |
| --- | --- |
| P16.0 | `hermes_0_19_pepper_project_ticket_spec_schema_ready_with_planning_only_authority` |
| P16.1 | `hermes_0_19_pepper_context_pack_assembler_ready_with_bounded_in_memory_authority` |
| P16.2 | `hermes_0_19_pepper_ticket_generator_agent_roles_ready_with_non_executing_proposal_authority` |
| P16.3 | `hermes_0_19_pepper_dependency_dag_parallel_wave_planner_ready_with_dependency_only_authority` |

Required public imports passed for `AuthorityReferenceKind`, `ProjectSpec`, `TicketDependencyPlan`, `TicketSpec`, `TicketType` and `WaveDisposition`.

P16.4 did not modify `specs.py`, `context_packs.py`, `generator_roles.py`, `dependency_planning.py`, or the accepted P16.0/P16.1/P16.2/P16.3 focused tests.

## Pre-Change Pepper Identity

Committed P16.3 Pepper identity before P16.4 implementation:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate | `6844` | `150263890` | `6b1bf7227c122be600b9ef17e2ccda4dc7db4bddb4344af2e3fa03fadd7a7dcd` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Pre-change governance integrity reported `14` tests, `0` failures and `0` errors.

## Post-Change Pepper Identity Projection

The integrity utility computes committed `HEAD` blob identity. Because P16.4 is not committed by the agent, the expected post-commit Pepper identity was computed with the same v2 record-stream algorithm over the current working-tree candidate set:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate post-commit projection | `6847` | `150392041` | `4587e01402f8c1677ad727c2bc4ecbb153c8f57b5288df96991990d39c857366` |
| Payload post-commit projection | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record post-commit projection | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Upstream payload changed: `false`. Baseline changed: `false`. New Pepper product files: `3`.

## Package Paths

| Path | Purpose |
| --- | --- |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py` | Public Ticket Factory export boundary extended additively for P16.4. |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/ticket_policy.py` | Immutable P16.4 ticket policy and linter contracts. |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/specs.py` | Unmodified P16.0 planning contracts consumed by P16.4. |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/dependency_planning.py` | Unmodified P16.3 dependency-plan contracts consumed by P16.4. |

No parent `agent_platform` initializer, runtime route, frontend source, provider code, credential code or dependency file was modified.

## Public Exports

P16.4 adds exactly these 15 public exports:

| Export |
| --- |
| `TICKET_POLICY_SCHEMA_VERSION` |
| `TicketPolicyProfileName` |
| `TicketLintSeverity` |
| `TicketLintScope` |
| `TicketLintDisposition` |
| `TicketLintRuleCode` |
| `TicketPolicyProfile` |
| `TicketLintRequest` |
| `TicketLintDiagnostic` |
| `TicketLintSummary` |
| `TicketLintReport` |
| `TicketPolicyError` |
| `TicketPolicyInputError` |
| `get_ticket_policy_profile` |
| `lint_ticket_collection` |

P16.0 exports preserved: `true`. P16.1 exports preserved: `true`. P16.2 exports preserved: `true`. P16.3 exports preserved: `true`. Duplicate exports: `0`. Private helpers exported: `0`. Import side effects: `0`.

## Schema Version And Enums

`TICKET_POLICY_SCHEMA_VERSION = 1`. `TicketPolicyProfile.schema_version` and `TicketLintReport.schema_version` are fixed to `Literal[1] = 1`. Alternative versions are rejected. Schema migration and runtime negotiation are absent.

| Enum | Values |
| --- | --- |
| `TicketPolicyProfileName` | `governed_standard_v1` |
| `TicketLintSeverity` | `info`, `warning`, `error` |
| `TicketLintScope` | `project`, `collection`, `ticket` |
| `TicketLintDisposition` | `pass`, `pass_with_warnings`, `blocked` |
| `TicketLintRuleCode` | `allowed_paths_required`, `forbidden_actions_required`, `scope_exact_contradiction`, `required_forbidden_action_missing`, `authority_reference_required`, `recommended_commit_message_required`, `rollback_constraint_required`, `required_response_section_missing`, `required_validation_step_missing`, `forbidden_validation_command`, `dependency_plan_required`, `dependency_blocked`, `soft_external_dependency_unresolved`, `scope_review_required`, `closure_ticket_required`, `multiple_closure_tickets`, `closure_identifier_type_mismatch`, `closure_identifier_suffix_invalid`, `closure_dependency_coverage`, `duplicate_ticket_title`, `duplicate_commit_message`, `duplicate_completion_verdict` |

Enum aliases: `0`. Unrestricted enum strings are rejected.

## Canonical Policy Profile

The single canonical profile is `governed_standard_v1`. Runtime profile registration, filesystem profile loading, plugin discovery and profile mutation are absent.

Required response sections: `Summary`, `Files inspected`, `Files modified`, `Tests/commands run`, `Decisions made`, `Limitations`.

Required forbidden-action markers: `git add`, `git commit`, `git push`, `git reset`, `git clean`, `git stash`, `git worktree`, `Graphify`.

Authority-required ticket types: `architecture`, `integration`, `closure`. Commit-message-required ticket types: `implementation`, `refactor`, `test`, `bugfix`, `integration`, `closure`. Rollback-required ticket types: `implementation`, `refactor`, `bugfix`, `integration`, `closure`.

Rollback markers: `rollback`, `restore`, `revert`, `remove only`. Forbidden validation-command markers: `git add`, `git commit`, `git push`, `git reset`, `git clean`, `git stash`, `git worktree add`, `git worktree remove`, `graphify update`, `graphify extract`, `graphify export`, `graphify cluster`, `graphify recluster`. Closure suffixes: `R`, `CR`.

Duplicate title severity: `warning`. Duplicate commit-message severity: `warning`. Duplicate completion-verdict severity: `error`.

## Policy Rules

Scope policy requires non-empty allowed paths, non-empty forbidden actions, exact syntactic allowed/forbidden path contradiction detection and all required forbidden-action markers. General glob intersection and mutation are absent.

Authority policy requires at least one `required=true` authority reference for architecture, integration and closure tickets. References are not resolved or verified.

Commit-message policy requires recommended commit messages for implementation, refactor, test, bugfix, integration and closure tickets. Git execution is absent.

Rollback policy scans `constraints`, `tasks` and `acceptance_criteria` for configured rollback markers. Operational correctness is not assessed.

Response policy requires all canonical response sections, with case-insensitive whitespace-normalized matching. Completion verdicts are not approval authority.

Validation-step policy requires at least one required validation step and detects forbidden Git-write and Graphify-mutation markers without command execution. Diagnostics identify validation IDs and markers while withholding full command text.

Dependency-plan policy requires a matching plan for multi-ticket collections. Blocked tickets become errors. Unresolved soft external dependencies become warnings. Scope-review waves become human-review warnings and do not claim actual conflicts or safe execution. Waves and plans are not mutated.

Closure policy enforces identifier/type consistency, complete-collection single-closure requirements and transitive hard internal dependency coverage into closure. Soft and external dependencies do not satisfy closure coverage, and closure coverage is not project approval.

Duplicate policy normalizes titles and recommended commit messages by stripping, casefolding and collapsing whitespace. Completion verdicts must be unique. Diagnostics are emitted for tickets after the first canonical ticket.

## Diagnostic, Summary And Disposition Contracts

`TicketLintDiagnostic` field order is `diagnostic_id`, `code`, `severity`, `scope`, `ticket_id`, `field_path`, `message`, `remediation`, `blocking`. Error diagnostics are blocking. Warnings and info diagnostics are nonblocking. Ticket scope requires a ticket ID; project and collection scope require null ticket ID.

Diagnostics are sorted by severity rank, scope rank, ticket ID with null first, rule-code enum order, field path and message. IDs are assigned after sorting as `LINT-0001`, `LINT-0002` and later values. Full specs, full validation commands, provider output, secrets and reasoning traces are absent from diagnostics.

`TicketLintSummary` field order is `ticket_count`, `diagnostic_count`, `error_count`, `warning_count`, `info_count`, `blocked_ticket_ids`, `warning_ticket_ids`, `collection_blocked`. Counts are nonnegative and diagnostic count equals the severity-count sum. Collection blocked is true when any error exists.

Disposition is `blocked` when errors exist, `pass_with_warnings` when warnings exist without errors, and `pass` when no errors or warnings exist.

## Digest Evidence

Input digest algorithm: `agent-platform-ticket-policy-input-sha256-v1`. The digest includes ProjectSpec, canonically ordered tickets, dependency plan or null, collection-complete flag, policy name and canonical profile using deterministic JSON. Ticket input permutation preserves it. Ticket content, dependency-plan content, collection-complete value and policy changes alter it.

Report digest algorithm: `agent-platform-ticket-lint-report-sha256-v1`. The digest includes schema version, project ID, policy name, ticket IDs, input digest, diagnostics, summary and disposition. It excludes `report_SHA256` itself. Diagnostic, summary and disposition changes alter it.

Digests are neither security signatures nor approval signatures and are not publication identities.

## Public Exceptions And Serialization

`TicketPolicyError` is the base exception. `TicketPolicyInputError` reports request inconsistency such as project mismatch or dependency-plan mismatch. Exception messages are bounded and omit full ProjectSpec content, full TicketSpec content, full validation commands and secrets.

Public Pydantic models are frozen, extra-forbid and use validated defaults. Unknown fields are rejected, mutable defaults are absent and strict booleans reject strings. Public fields contain no `typing.Any`, unrestricted mapping fields, object payloads, arbitrary metadata bags, `Path`, datetime, UUID, bytes, callable, provider object, agent object, worker object, worktree object, approval object or publication object.

Standard Pydantic `model_dump()`, `model_dump_json()`, `model_validate()`, `model_validate_json()` and `model_json_schema()` are supported. Filesystem serialization, YAML support, Markdown rendering, file loaders and file writers are absent.

## Non-Mutating Authority

P16.4 defines no AutoFix, TicketPatch, TicketRewrite, ApprovedTicket, PublishedTicket, CanonicalTicket, ProposalWinner, SynthesisResult, WorkPacket, ExecutionLane, AgentAssignment, WorkerAssignment or WorktreeAssignment public shape.

The linter does not repair diagnostics, mutate tickets, alter dependency edges, move tickets between waves, select proposals, approve reports, publish tickets or authorize execution.

## Tests

Focused P16.4 command from `2_products/pepper-agent`:

```text
python -m pytest -q tests/hermes_cli/test_agent_platform_ticket_factory_ticket_policy.py -p no:cacheprovider
```

Result: `217` passed, `0` failed, `0` errors, `0` unexpected skips, `0` warnings reported.

Focused combined P16.0/P16.1/P16.2/P16.3/P16.4 command from `2_products/pepper-agent`:

```text
python -m pytest -q tests/hermes_cli/test_agent_platform_ticket_factory_specs.py tests/hermes_cli/test_agent_platform_ticket_factory_context_packs.py tests/hermes_cli/test_agent_platform_ticket_factory_generator_roles.py tests/hermes_cli/test_agent_platform_ticket_factory_dependency_planning.py tests/hermes_cli/test_agent_platform_ticket_factory_ticket_policy.py -p no:cacheprovider
```

Result: `641` passed, `0` failed, `0` errors, `0` unexpected skips, `0` warnings reported. Constituent counts: P16.0 `96`, P16.1 `75`, P16.2 `120`, P16.3 `133`, P16.4 `217`.

Import smoke:

```text
TicketPolicyProfile TicketLintRequest TicketLintReport TicketLintDisposition lint_ticket_collection
```

Governance integrity command reported `14` tests, `0` failures and `0` errors.

## Static Validation

Ruff check over the three P16.4 Python candidates reported `0` lint errors. Ruff format check reported `3` files already formatted. `ty` availability: `false`; type check was not run because the tool is unavailable; dependency installation remained `0`.

AST static import and authority scan reported `P16_4_STATIC_IMPORT_AUTHORITY_SCAN_OK`. Forbidden imports and execution, filesystem, network, Git, provider, worker, agent, tool, worktree, environment, clock, randomness, ticket mutation, dependency-plan mutation and auto-fix references were absent.

## Modification Register

`2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` records exactly three new P16.4 product-addition rows: `P16.4-001`, `P16.4-002`, `P16.4-003`.

Existing row `P16.0-001` for `hermes_cli/agent_platform/ticket_factory/__init__.py` was preserved and updated to the additive P16.4 hash and description. Duplicate IDs: `0`. Duplicate paths: `0`. Missing destination paths: `0`. Hash mismatches for P16.4 rows and updated `P16.0-001`: `0`. Unrelated row edits: `0` by intended candidate scope.

## Import Manifest

`2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` records three new P16.4 product-addition rows for policy source, focused tests and documentation. Existing destination row `hermes_cli/agent_platform/ticket_factory/__init__.py` was updated to the additive P16.4 hash and rule. The governance record is not included in the Pepper import manifest.

Classification for new rows: `AGENT_PLATFORM_product_addition`. Included in upstream payload: `false`. Duplicate concrete destinations: `0`. Destination hash mismatches for P16.4 rows and updated `__init__.py`: `0`.

## Product File Hashes

| Path | SHA-256 |
| --- | --- |
| `hermes_cli/agent_platform/ticket_factory/__init__.py` | `7ff8d3fe997e1ad6b03f6358b2384421eee23a46a0eefd4d8eb9f717a502f134` |
| `hermes_cli/agent_platform/ticket_factory/ticket_policy.py` | `ed683fa0d83a409773ae699de0fb61db6dc2f6b2c1a97744a1b9ce27f52b7489` |
| `tests/hermes_cli/test_agent_platform_ticket_factory_ticket_policy.py` | `e863708ed8954c7e4f6fe41f1abc67313d31103582a0be033622e724baaf85e4` |
| `docs/agent-platform/ticket_policy_and_linter.md` | `ba38b697e15a7dc057e18b368efcccd00f48f4824017eed6cb4e295a31c05e69` |
| `AGENT_PLATFORM_MODIFICATIONS.tsv` | `d4dec401b6fe0358a4a5d081ee2060a633086cd025c4a93936a9e5dcb8bb95fe` |
| `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | `3fbf32baf061b6aae9835139233010b8322a07b40100b9bef530ef7eb5e2fcec` |

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
| dependency DAG construction | `0` |
| parallel wave mutation | `0` |
| proposal synthesis | `0` |
| human approval | `0` |
| canonical publishing | `0` |
| WorkPacket creation | `0` |
| validation command execution | `0` |
| ticket auto-fix | `0` |

Pydantic validation, deterministic text inspection, deterministic diagnostic construction, deterministic JSON encoding and SHA-256 hashing are the only runtime behaviors introduced by P16.4 product code.

## Secret Scan

Focused secret-shape scan across the seven P16.4 candidates reported `P16_4_SECRET_SHAPE_SCAN_OK`.

Real-value counts: access tokens `0`, refresh tokens `0`, authorization headers `0`, OAuth codes `0`, credential contents `0`, real auth file contents `0`, private keys `0`, API keys `0`, raw provider responses `0`, raw prompts `0`, reasoning traces `0` and personal absolute paths in product files `0`.

## Exact Candidate Set

Created Pepper product files:

| Status | Path |
| --- | --- |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/ticket_policy.py` |
| Added | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_ticket_factory_ticket_policy.py` |
| Added | `2_products/pepper-agent/docs/agent-platform/ticket_policy_and_linter.md` |

Modified Pepper product files:

| Status | Path |
| --- | --- |
| Modified | `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` |

Created governance record:

| Status | Path |
| --- | --- |
| Added | `0_architecture/governance/agent_platform_pepper_ticket_policy_and_linter.md` |

Candidate formula: `3` created Pepper product files plus `3` modified Pepper product files plus `1` created governance record equals `7` candidates. Created files: `4`. Modified files: `3`. Deleted files: `0`. Unexpected candidates: `0`. Specs candidate: `false`. Context packs candidate: `false`. Generator roles candidate: `false`. Dependency planning candidate: `false`. Prior test candidates: `0`. Frontend candidates: `0`. Backend runtime candidates: `0`. Provider candidates: `0`. Worker candidates: `0`. Omniverse candidates: `0`. External source candidates: `0`. Graphify candidates: `0`. Dependency file candidates: `0`.

## P16.5 Handoff

P16.5 owns independent TicketProposal collection contracts, proposal-set identity, proposal normalization, proposal comparison, field-level difference evidence, semantic conflict classification, agreement detection, dissent preservation, candidate synthesis, synthesis provenance, unresolved conflict reporting and review-ready synthesized proposals.

P16.5 must consume `ProjectSpec`, seed `TicketSpec`, `ContextPack`, `GeneratorAssignment` collections, validated `TicketProposal` collections, `TicketDependencyPlan` when relevant and `TicketLintReport` for each proposal. P16.5 must not own human approval, canonical ticket selection, canonical publishing or WorkPacket execution.

## Residual Constraints

| Item | State |
| --- | --- |
| TicketPolicyProfile immutable | `true` |
| canonical profiles | `1` |
| runtime configurable | `false` |
| TicketLintRequest persisted | `false` |
| TicketLintRequest executable | `false` |
| TicketLintDiagnostic evidence only | `true` |
| TicketLintDiagnostic auto-fix | `false` |
| TicketLintReport immutable | `true` |
| TicketLintReport deterministic | `true` |
| TicketLintReport approved | `false` |
| TicketLintReport canonical | `false` |
| TicketLintReport published | `false` |
| TicketLintReport executable | `false` |
| policy failures represented as diagnostics | `true` |
| input inconsistency represented as exception | `true` |
| validation commands inspected as text | `true` |
| validation commands executed | `false` |
| dependency plan consumed | `true` |
| dependency plan rebuilt | `false` |
| dependency plan mutated | `false` |
| scope globs expanded | `false` |
| filesystem access | absent |
| ticket rewrite | absent |
| auto-fix | absent |
| proposal synthesis | absent |
| human approval | absent |
| canonical publishing | absent |
| agent assignment | absent |
| worker assignment | absent |
| worktree assignment | absent |
| WorkPacket | absent |
| runtime routes | `0` |
| product UI | disabled |
| Graphify | frozen read-only; not run by P16.4 instruction |
| production readiness | not claimed |

Canonical verdict occurrences in this record: `1`. Alternative P16.4 verdict occurrences: `0`.

## Final Verdict

hermes_0_19_pepper_ticket_policy_linter_ready_with_deterministic_non_mutating_authority
