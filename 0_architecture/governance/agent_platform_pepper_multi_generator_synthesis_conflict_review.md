# P16.5 Multi-Generator Synthesis Conflict Review Governance Record

## P16.5 Authority

P16 is Ticket Factory and Parallel Planning. P16.5 adds deterministic, immutable and noncanonical review evidence for comparing independently supplied P16.2 ticket-generator proposals after P16.4 lint review.

The synthesis builder consumes one `TicketGenerationRequest`, the exact deterministic `GeneratorAssignment` collection, one reviewed `TicketProposal` per assignment, each proposal's `TicketLintReport`, and an optional `TicketDependencyPlan` for stale-plan checks. It produces field-level synthesis decisions, conflict evidence, an optional synthesized candidate ticket, candidate lint evidence, a deterministic disposition and reproducible digests.

P16.5 is not proposal generation, provider execution, prompt rendering, agent execution, dependency-plan rebuilding, human approval, canonical ticket selection, canonical publication, runtime scheduling, validation-command execution, repository scanning, worktree allocation or WorkPacket creation.

`TicketSynthesisReview` and `SynthesizedTicketCandidate` are review evidence, not approval or publication authority.

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
| Resolved P16.4 commit | `3c43c0db8833487ed10d4f8568e2b9413cf5f2ac` |
| P16.4 commit message | `P16.4 Add ticket policy and linter` |
| HEAD at implementation | `3c43c0db8833487ed10d4f8568e2b9413cf5f2ac` |
| Remote P16 at implementation | `3c43c0db8833487ed10d4f8568e2b9413cf5f2ac` |
| P16.4 is ancestor of remote P16 | `true` |
| main at implementation | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| origin/main at implementation | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| Worktree at gate | exactly 7 expected P16.5 candidates |
| Index at gate | empty |
| Visible untracked at gate | `4` |
| Omniverse tracked product files | `369` |

The P16.5 candidate remains uncommitted by instruction. No staging, commit, push, branch switch, reset, clean, stash, Docker command, dependency update, lockfile update, Graphify command or `graphify-out` modification was performed.

## Prerequisite Verdicts

| Prerequisite | Verdict |
| --- | --- |
| P16.0 | `hermes_0_19_pepper_project_ticket_spec_schema_ready_with_planning_only_authority` |
| P16.1 | `hermes_0_19_pepper_context_pack_assembler_ready_with_bounded_in_memory_authority` |
| P16.2 | `hermes_0_19_pepper_ticket_generator_agent_roles_ready_with_non_executing_proposal_authority` |
| P16.3 | `hermes_0_19_pepper_dependency_dag_parallel_wave_planner_ready_with_dependency_only_authority` |
| P16.4 | `hermes_0_19_pepper_ticket_policy_linter_ready_with_deterministic_non_mutating_authority` |

P16.5 did not modify `specs.py`, `context_packs.py`, `generator_roles.py`, `dependency_planning.py`, `ticket_policy.py` or the accepted P16.0/P16.1/P16.2/P16.3/P16.4 focused tests.

## Pre-Change Pepper Identity

Committed P16.4 Pepper identity before P16.5 implementation:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate | `6847` | `150392041` | `4587e01402f8c1677ad727c2bc4ecbb153c8f57b5288df96991990d39c857366` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Pre-change governance integrity reported `14` tests, `0` failures and `0` errors.

## Package Paths

| Path | Purpose |
| --- | --- |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py` | Public Ticket Factory export boundary extended additively for P16.5 while preserving the P16.4 final export block. |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/proposal_synthesis.py` | Immutable P16.5 multi-generator synthesis and conflict-review contracts. |
| `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_ticket_factory_proposal_synthesis.py` | Focused P16.5 synthesis and conflict-review contract tests. |
| `2_products/pepper-agent/docs/agent-platform/multi_generator_synthesis_conflict_review.md` | P16.5 operator and contract documentation. |

No parent `agent_platform` initializer, runtime route, frontend source, provider code, credential code, dependency file, prior P16 contract or prior P16 test was modified.

## Public Exports

P16.5 adds exactly these 18 public exports:

| Export |
| --- |
| `MULTI_GENERATOR_SYNTHESIS_SCHEMA_VERSION` |
| `TicketSynthesisField` |
| `ProposalAgreementLevel` |
| `FieldResolutionKind` |
| `ProposalConflictKind` |
| `ProposalConflictSeverity` |
| `TicketSynthesisDisposition` |
| `ReviewedTicketProposal` |
| `TicketSynthesisRequest` |
| `ProposalVariantEvidence` |
| `FieldSynthesisDecision` |
| `ProposalConflict` |
| `SynthesizedTicketCandidate` |
| `TicketSynthesisReview` |
| `TicketSynthesisError` |
| `TicketSynthesisInputError` |
| `TicketSynthesisValidationError` |
| `build_ticket_synthesis_review` |

P16.0 exports preserved: `true`. P16.1 exports preserved: `true`. P16.2 exports preserved: `true`. P16.3 exports preserved: `true`. P16.4 exports preserved: `true`. P16.4 final-block compatibility preserved: `true`. Duplicate exports: `0`. Private digest constants exported through package root: `0`. Import side effects: `0`.

## Schema Version And Enums

`MULTI_GENERATOR_SYNTHESIS_SCHEMA_VERSION = 1`. `SynthesizedTicketCandidate.schema_version` and `TicketSynthesisReview.schema_version` are fixed to `Literal[1] = 1`. Alternative versions are rejected. Schema migration and runtime negotiation are absent.

| Enum | Values |
| --- | --- |
| `TicketSynthesisField` | `title`, `objective`, `context`, `authority_references`, `dependencies`, `parallelization_hint`, `scope`, `constraints`, `tasks`, `acceptance_criteria`, `validation_steps`, `response_contract`, `recommended_commit_message` |
| `ProposalAgreementLevel` | `unanimous`, `strict_majority`, `split` |
| `FieldResolutionKind` | `adopt_unanimous`, `adopt_strict_majority`, `preserve_seed` |
| `ProposalConflictKind` | `lint_blocked_proposal`, `field_dissent`, `field_split`, `dependency_plan_stale`, `scope_plan_stale`, `candidate_lint_blocked`, `insufficient_eligible_proposals` |
| `ProposalConflictSeverity` | `info`, `warning`, `human_review_required`, `blocking` |
| `TicketSynthesisDisposition` | `review_ready`, `review_ready_with_dissent`, `human_resolution_required`, `blocked` |

Enum aliases: `0`. Unrestricted enum strings are rejected.

## Synthesis Rules

Assignments must exactly match `prepare_ticket_generator_assignments(generation_request)`. Reviewed proposals must match assignments one-to-one. Proposals are revalidated against the generation request. Lint reports are revalidated and must cover exactly the proposal project and ticket ID.

Lint-disposition `pass` and `pass_with_warnings` proposals are eligible to vote. Lint-disposition `blocked` proposals are excluded from voting and recorded as warning conflicts. Fewer than two eligible proposals blocks candidate construction.

Every `TicketSynthesisField` is compared by deterministic JSON value digest. Unanimous fields adopt the unanimous value. Strict-majority fields adopt the majority value and preserve dissent evidence. Split fields preserve the seed `TicketSpec` value and require human resolution.

The synthesized candidate is built in memory from the seed ticket and selected field values, then linted as a one-ticket incomplete collection with no dependency plan. Candidate lint blocking produces a blocking conflict. A supplied dependency plan is not rebuilt; dependency or scope changes from seed to candidate produce stale-plan human-review conflicts.

## Conflict, Candidate And Review Contracts

`ProposalConflict` field order is `conflict_id`, `kind`, `severity`, `field`, `proposal_SHA256`, `related_proposal_SHA256s`, `message`, `remediation`, `blocking`. Conflict IDs are sequential after deterministic sorting. Blocking severity requires `blocking=true`; nonblocking severities require `blocking=false`.

`SynthesizedTicketCandidate` field order is `schema_version`, `candidate_id`, `project_id`, `ticket_id`, `synthesized_ticket`, `source_proposal_SHA256s`, `excluded_proposal_SHA256s`, `field_decisions`, `unresolved_conflict_ids`, `candidate_lint_report`, `candidate_SHA256`.

`TicketSynthesisReview` field order is `schema_version`, `project_id`, `ticket_id`, `synthesis_input_SHA256`, `proposal_SHA256s`, `eligible_proposal_SHA256s`, `excluded_proposal_SHA256s`, `field_decisions`, `conflicts`, `candidate`, `disposition`, `review_SHA256`. Eligible and excluded proposals partition proposals. Candidate evidence must match review project, ticket, source proposals, excluded proposals, field decisions and unresolved conflict IDs.

## Digest Evidence

Input digest algorithm: `agent-platform-ticket-synthesis-input-sha256-v1`. Candidate digest algorithm: `agent-platform-synthesized-ticket-candidate-sha256-v1`. Review digest algorithm: `agent-platform-ticket-synthesis-review-sha256-v1`.

The input digest includes the generation request, canonical assignments, canonical reviewed proposals and optional dependency plan. The candidate digest excludes `candidate_SHA256` itself. The review digest excludes `review_SHA256` itself.

Digests are neither security signatures nor approval signatures and are not publication identities.

## Noncanonical Review Authority

P16.5 defines no ProposalSynthesizer runtime, ProposalWinner, ApprovalRequest, ApprovalDecision, PublishedTicket, CanonicalTicket, WorkPacket, ExecutionLane, AgentAssignment, WorkerAssignment, WorktreeAssignment, generator runner, validation-command runner, file loader, file writer or Graphify operation public shape.

The builder does not mutate generation requests, assignments, proposals, lint reports, dependency plans, seed tickets or candidate source proposals.

## Tests

Focused P16.5 command from `2_products/pepper-agent`:

```text
python -m pytest -q tests/hermes_cli/test_agent_platform_ticket_factory_proposal_synthesis.py -p no:cacheprovider
```

Result: `161` passed, `0` failed, `0` errors.

Focused combined P16.0/P16.1/P16.2/P16.3/P16.4/P16.5 command from `2_products/pepper-agent`:

```text
python -m pytest -q tests/hermes_cli/test_agent_platform_ticket_factory_specs.py tests/hermes_cli/test_agent_platform_ticket_factory_context_packs.py tests/hermes_cli/test_agent_platform_ticket_factory_generator_roles.py tests/hermes_cli/test_agent_platform_ticket_factory_dependency_planning.py tests/hermes_cli/test_agent_platform_ticket_factory_ticket_policy.py tests/hermes_cli/test_agent_platform_ticket_factory_proposal_synthesis.py -p no:cacheprovider
```

Result: `802` passed, `0` failed, `0` errors. Constituent counts: P16.0 `96`, P16.1 `75`, P16.2 `120`, P16.3 `133`, P16.4 `217`, P16.5 `161`.

The direct validation commands used the active Windows Python with pytest. No dependency installation was performed.

Import smoke:

```text
TicketSynthesisRequest ProposalConflict SynthesizedTicketCandidate TicketSynthesisReview TicketSynthesisDisposition build_ticket_synthesis_review
```

## Static Validation

Ruff check over the three P16.5 Python candidates reported `0` lint errors. Ruff format check reported `3` files already formatted. `ty` availability: `false`; type check was not run because the tool is unavailable and no dependency installation was performed.

Static import and authority scans for `proposal_synthesis.py` reported no forbidden provider, agent, tool, filesystem, network, subprocess, Git, Docker, Graphify, WorkPacket, approval, publication, canonical-ticket or generator-execution imports or call terms.

## Modification Register

`2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` records exactly three new P16.5 product-addition rows: `P16.5-001`, `P16.5-002`, `P16.5-003`.

Existing row `P16.0-001` for `hermes_cli/agent_platform/ticket_factory/__init__.py` was preserved and updated to the additive P16.5 hash and description. Duplicate IDs: `0`. Missing destination paths: `0`. Unrelated row edits: `0` by intended candidate scope.

## Import Manifest

`2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` records three new P16.5 product-addition rows for synthesis source, focused tests and documentation. Existing destination row `hermes_cli/agent_platform/ticket_factory/__init__.py` was updated to the additive P16.5 hash and rule. The governance record is not included in the Pepper import manifest.

Classification for new rows: `AGENT_PLATFORM_product_addition`. Included in upstream payload: `false`.

## Product File Hashes

| Path | SHA-256 |
| --- | --- |
| `hermes_cli/agent_platform/ticket_factory/__init__.py` | `75b5c5db0f1f7d3d3790727b5b60dfa1edd4367f6ddbb0118c54dcd01da62027` |
| `hermes_cli/agent_platform/ticket_factory/proposal_synthesis.py` | `80b55e9da540526a461057db6e5e64f65d8b9f626a3856d91e2eafad90bd92d4` |
| `tests/hermes_cli/test_agent_platform_ticket_factory_proposal_synthesis.py` | `833bb17378bf538a4f08dc1e05ac56f396d9516fc91c9ea30893e01c54851e06` |
| `docs/agent-platform/multi_generator_synthesis_conflict_review.md` | `772b909a3e6185e51f2d232e41fe59bcef8f14e549d9b73eca700d2da9f18fdb` |
| `AGENT_PLATFORM_MODIFICATIONS.tsv` | `27c3999dfd401b59d0911be8b07fb2b773560d5314ae8a7edd1f1ac8c92de87f` |
| `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | `4c97a05f49907d27295ad8dc9ec93b75603e967c63cca6585b5873ac9d135072` |

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
| proposal generation | `0` |
| provider/model execution | `0` |
| prompt rendering | `0` |
| dependency DAG construction | `0` |
| dependency plan mutation | `0` |
| ticket linting mutation | `0` |
| human approval | `0` |
| canonical publishing | `0` |
| WorkPacket creation | `0` |
| validation command execution | `0` |
| ticket auto-fix | `0` |

Pydantic validation, proposal/lint binding checks, deterministic field-value comparison, deterministic conflict construction, candidate lint evidence and SHA-256 hashing are the only runtime behaviors introduced by P16.5 product code.

## Exact Candidate Set

Created Pepper product files:

| Status | Path |
| --- | --- |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/proposal_synthesis.py` |
| Added | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_ticket_factory_proposal_synthesis.py` |
| Added | `2_products/pepper-agent/docs/agent-platform/multi_generator_synthesis_conflict_review.md` |

Modified Pepper product files:

| Status | Path |
| --- | --- |
| Modified | `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` |

Created governance record:

| Status | Path |
| --- | --- |
| Added | `0_architecture/governance/agent_platform_pepper_multi_generator_synthesis_conflict_review.md` |

Candidate formula: `3` created Pepper product files plus `3` modified Pepper product files plus `1` created governance record equals `7` candidates. Created files: `4`. Modified files: `3`. Deleted files: `0`. Unexpected candidates: `0`. Prior P16 contract candidates: `0`. Prior P16 test candidates: `0`. Frontend candidates: `0`. Backend runtime candidates: `0`. Provider candidates: `0`. Worker candidates: `0`. Omniverse candidates: `0`. External source candidates: `0`. Graphify candidates: `0`. Dependency file candidates: `0`.

## P16.6 Handoff

P16.6 owns human approval and canonical publishing. P16.5 hands off `TicketSynthesisReview` evidence with candidate, field decisions, conflicts, eligible/excluded proposal digests and digest provenance. P16.6 must not treat P16.5 dispositions as approval or publication authority.

## Residual Constraints

| Item | State |
| --- | --- |
| synthesis review immutable | `true` |
| synthesized candidate immutable | `true` |
| canonical candidate | `false` |
| approved candidate | `false` |
| published candidate | `false` |
| executable candidate | `false` |
| proposal generation | absent |
| provider/model execution | absent |
| prompt rendering | absent |
| agent execution | absent |
| worker assignment | absent |
| worktree assignment | absent |
| WorkPacket | absent |
| dependency plan rebuilt | `false` |
| dependency plan mutated | `false` |
| candidate lint mutates ticket | `false` |
| filesystem access | absent |
| network access | absent |
| Git access | absent |
| Graphify | frozen read-only; not run by P16.5 instruction |
| Docker | absent |
| production readiness | not claimed |

Canonical verdict occurrences in this record: `1`. Alternative P16.5 verdict occurrences: `0`.

## Final Verdict

hermes_0_19_pepper_multi_generator_synthesis_conflict_review_ready_with_noncanonical_review_authority
