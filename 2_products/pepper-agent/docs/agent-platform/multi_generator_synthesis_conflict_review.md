# P16.5 Multi-Generator Synthesis Conflict Review

P16.5 adds deterministic, immutable and noncanonical review evidence for comparing independently supplied ticket-generator proposals. It consumes a P16.2 `TicketGenerationRequest`, the exact deterministic `GeneratorAssignment` collection, one reviewed `TicketProposal` per assignment, each proposal's P16.4 `TicketLintReport`, and an optional P16.3 `TicketDependencyPlan` for stale-plan checks.

`TicketSynthesisReview` and `SynthesizedTicketCandidate` are review evidence only. They are not approval records, canonical tickets, publication records, execution queues or WorkPackets.

## Relationship To P16.0 Through P16.4

P16.0 owns `ProjectSpec` and `TicketSpec`. P16.1 owns bounded in-memory `ContextPack` assembly. P16.2 owns non-executing generator-role assignments and proposal envelopes. P16.3 owns dependency DAG and parallel-wave planning. P16.4 owns deterministic non-mutating policy linting.

P16.5 consumes those outputs and produces one review envelope. It does not generate proposals, call providers, render prompts, execute agents, rebuild dependency plans, lint with mutable policy, approve tickets, publish tickets or allocate work.

## Authority Boundary

P16.5 performs Pydantic validation, deterministic proposal binding checks, lint-report binding checks, field-value digest comparison, conservative in-memory candidate construction, deterministic conflict evidence construction, deterministic JSON encoding and SHA-256 hashing.

P16.5 performs no filesystem access, network access, provider access, credential access, prompt rendering, agent invocation, worker invocation, tool invocation, shell execution, Git operation, Graphify operation, Docker operation, ticket persistence, auto-fix, canonical selection, approval, publication or WorkPacket creation.

## Public Exports

P16.5 adds exactly 18 public names through `hermes_cli.agent_platform.ticket_factory`:

| Export | Purpose |
| --- | --- |
| `MULTI_GENERATOR_SYNTHESIS_SCHEMA_VERSION` | Fixed schema version, currently `1`. |
| `TicketSynthesisField` | Field vocabulary compared across proposals. |
| `ProposalAgreementLevel` | `unanimous`, `strict_majority`, `split`. |
| `FieldResolutionKind` | `adopt_unanimous`, `adopt_strict_majority`, `preserve_seed`. |
| `ProposalConflictKind` | Conflict taxonomy for lint exclusions, field disagreement, stale plans and blocked candidates. |
| `ProposalConflictSeverity` | `info`, `warning`, `human_review_required`, `blocking`. |
| `TicketSynthesisDisposition` | Overall review disposition. |
| `ReviewedTicketProposal` | One proposal plus its lint report. |
| `TicketSynthesisRequest` | Synthesis input envelope. |
| `ProposalVariantEvidence` | Per-field value variant support evidence. |
| `FieldSynthesisDecision` | Per-field agreement and resolution evidence. |
| `ProposalConflict` | Deterministic conflict record. |
| `SynthesizedTicketCandidate` | Noncanonical candidate ticket evidence. |
| `TicketSynthesisReview` | Top-level review envelope. |
| `TicketSynthesisError` | Base synthesis exception. |
| `TicketSynthesisInputError` | Assignment, proposal-set or plan input inconsistency. |
| `TicketSynthesisValidationError` | Invalid proposal or lint-report digest evidence. |
| `build_ticket_synthesis_review` | Deterministic in-memory review builder. |

Digest algorithm constants are intentionally not exported through the package root.

## Request Contract

`TicketSynthesisRequest` field order is `generation_request`, `assignments`, `reviewed_proposals`, `dependency_plan`. The assignment and proposal counts are bounded from `2` through `6`.

Assignments must exactly match `prepare_ticket_generator_assignments(generation_request)`. Assignment IDs and roles must be unique. Reviewed proposals must match assignments one-to-one. Each proposal is revalidated with `validate_ticket_generator_proposal()` against the generation request.

Each `ReviewedTicketProposal` requires a `TicketLintReport` covering exactly the proposal project and ticket ID. The report digest is revalidated. Lint reports with disposition `pass` or `pass_with_warnings` are eligible to vote. Lint reports with disposition `blocked` exclude the proposal from voting and create warning conflict evidence.

At least two lint-eligible proposals are required to build a candidate. With fewer than two eligible proposals, the review is `blocked` and no candidate or field decisions are emitted.

## Field Comparison

`TicketSynthesisField` covers the mutable planning fields from `TicketSpec`: `title`, `objective`, `context`, `authority_references`, `dependencies`, `parallelization_hint`, `scope`, `constraints`, `tasks`, `acceptance_criteria`, `validation_steps`, `response_contract` and `recommended_commit_message`.

Each field value is serialized using deterministic JSON and hashed with SHA-256. Exact value equality is represented by matching field-value digests. P16.5 does not perform semantic merging, natural-language similarity, provider scoring or hidden tie-breaking.

## Resolution Rules

For every field:

| Agreement | Condition | Resolution |
| --- | --- | --- |
| `unanimous` | All eligible proposals have one field-value digest. | Adopt the unanimous value. |
| `strict_majority` | One field-value digest has more than half of eligible proposals. | Adopt the strict-majority value and retain dissent evidence. |
| `split` | No digest has strict majority. | Preserve the seed `TicketSpec` value and require human resolution. |

Variant evidence includes the value digest, support count, supporting proposal digests and supporting roles. Variants are sorted by descending support count and then digest. Roles use the canonical P16.2 role order.

P16.5 never edits a proposal. The synthesized candidate is built by applying selected field values to the seed ticket in memory and validating the resulting `TicketSpec`.

## Conflict Semantics

Conflict IDs are assigned after deterministic sorting as `CONFLICT-0001`, `CONFLICT-0002` and later values.

| Kind | Severity | Meaning |
| --- | --- | --- |
| `lint_blocked_proposal` | `warning` | A proposal's lint report blocked it from voting. |
| `field_dissent` | `warning` | A strict-majority field had dissenting eligible proposals. |
| `field_split` | `human_review_required` | No strict majority existed, so the seed value was preserved. |
| `dependency_plan_stale` | `human_review_required` | Candidate dependencies differ from the seed while a dependency plan was supplied. |
| `scope_plan_stale` | `human_review_required` | Candidate scope differs from the seed while a dependency plan was supplied. |
| `candidate_lint_blocked` | `blocking` | The synthesized candidate's P16.4 lint report is blocked. |
| `insufficient_eligible_proposals` | `blocking` | Fewer than two non-blocked proposals were available. |

Warning conflicts can still yield `review_ready_with_dissent`. Human-review conflicts yield `human_resolution_required` unless a blocking conflict exists. Blocking conflicts yield `blocked`.

## Candidate Linting

After candidate construction, P16.5 runs P16.4 `lint_ticket_collection()` on the candidate as a one-ticket incomplete collection with no dependency plan. This is non-mutating policy evidence. If the candidate lint report is blocked, P16.5 emits `candidate_lint_blocked` and the review disposition is `blocked`.

Candidate linting does not approve a candidate and does not publish it.

## Dependency Plan Staleness

If a `TicketDependencyPlan` is supplied, it must match the request project and contain the seed ticket ID. P16.5 does not rebuild or mutate the plan.

If candidate dependencies differ from the seed dependencies, the supplied plan may be stale and `dependency_plan_stale` is emitted. If candidate scope differs from the seed scope, wave and scope-collision evidence may be stale and `scope_plan_stale` is emitted.

Staleness conflicts require human review and a later dependency-planning rebuild outside P16.5.

## Digest Evidence

Synthesis input digest algorithm: `agent-platform-ticket-synthesis-input-sha256-v1`. It includes the generation request, canonical assignments, canonical reviewed proposals and optional dependency plan.

Candidate digest algorithm: `agent-platform-synthesized-ticket-candidate-sha256-v1`. It includes schema version, candidate ID, project ID, ticket ID, synthesized ticket, source proposal digests, excluded proposal digests, field decisions, unresolved conflict IDs and candidate lint report. It excludes `candidate_SHA256` itself.

Review digest algorithm: `agent-platform-ticket-synthesis-review-sha256-v1`. It includes schema version, project ID, ticket ID, synthesis input digest, proposal digests, eligible proposal digests, excluded proposal digests, field decisions, conflicts, candidate or null, and disposition. It excludes `review_SHA256` itself.

Digests are provenance evidence only. They are not security signatures, approval signatures or publication identities.

## Dispositions

| Disposition | Meaning |
| --- | --- |
| `review_ready` | Candidate exists and no conflicts remain. |
| `review_ready_with_dissent` | Candidate exists with nonblocking warning evidence. |
| `human_resolution_required` | Candidate exists but human review is required before any downstream decision. |
| `blocked` | No candidate exists or a blocking conflict exists. |

No disposition is approval authority.

## Serialization

Standard Pydantic `model_dump()`, `model_dump_json()`, `model_validate()`, `model_validate_json()` and `model_json_schema()` are supported. Public models are frozen, extra-forbid and validate defaults. JSON arrays normalize to tuples.

Filesystem serialization, YAML support, Markdown rendering, file loaders and file writers are absent.

## Synthetic Examples

Unanimous example: three eligible proposals with identical fields produce a `review_ready` review and a candidate with unanimous field decisions.

Strict-majority example: two eligible proposals choose one title and a third chooses another title. The candidate uses the majority title and the review records `field_dissent`.

Split example: two eligible proposals choose different objectives. The candidate preserves the seed objective and the review records `field_split` with `human_resolution_required`.

Blocked-proposal example: one proposal has a blocked lint report. That proposal is excluded from voting, preserved in `excluded_proposal_SHA256s`, and reported as `lint_blocked_proposal`.

Stale-plan example: candidate dependencies differ from the seed while a dependency plan is supplied. The review records `dependency_plan_stale` and does not rebuild the plan.

## Deferred Responsibilities

P16.6 owns human approval and canonical publishing. P16.7 owns the historical regression corpus. P16.8 owns the shadow pilot. WorkPacket execution remains deferred to P17.

P16.5 does not claim production readiness.
