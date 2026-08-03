# P16.6 Human Approval And Canonical Publishing

P16.6 adds explicit human-gated approval evidence and in-memory logical canonical publication evidence for P16 Ticket Factory candidates. It consumes P16.5 `TicketSynthesisReview` evidence, the originating `ProjectSpec` and seed `TicketSpec`, human approval evidence, optional human conflict resolutions, optional manual replacement evidence and optional fresh P16.3 dependency-planning evidence.

`TicketApprovalRecord`, `PublishedTicketArtifact`, `TicketSupersessionRecord` and `TicketPublicationResult` are evidence envelopes only. They do not write files, execute validation commands, allocate work, launch agents, mutate tickets, update Graphify, schedule WorkPackets or grant runtime authority.

## Relationship To P16.0 Through P16.5

P16.0 owns `ProjectSpec` and `TicketSpec`. P16.1 owns bounded in-memory `ContextPack` assembly. P16.2 owns non-executing generator-role assignments and proposal envelopes. P16.3 owns dependency DAG and parallel-wave planning. P16.4 owns deterministic non-mutating policy linting. P16.5 owns noncanonical multi-generator synthesis and conflict review.

P16.6 consumes those outputs and records a human decision. Approval requires explicit human evidence and validates the selected ticket with fresh P16.4 linting. If selected ticket dependencies or scope differ from the seed, P16.6 requires fresh P16.3 planning evidence and validates that it recomputes.

P16.6 does not generate proposals, call providers, render prompts, execute agents, rebuild plans implicitly, auto-resolve conflicts, persist canonical files, publish to a repository, run validation commands or create WorkPackets.

## Authority Boundary

P16.6 performs Pydantic validation, synthesis-review digest validation, conflict-resolution validation, manual replacement identity validation, fresh lint validation, fresh dependency-plan recomputation checks, deterministic JSON encoding and SHA-256 hashing.

P16.6 performs no filesystem access, network access, provider access, credential access, prompt rendering, agent invocation, worker invocation, tool invocation, shell execution, Git operation, Graphify operation, Docker operation, ticket persistence, runtime scheduling, WorkPacket creation, auto-fix or validation-command execution.

## Public Exports

P16.6 adds exactly 24 public names through `hermes_cli.agent_platform.ticket_factory`:

| Export | Purpose |
| --- | --- |
| `HUMAN_APPROVAL_PUBLISHING_SCHEMA_VERSION` | Fixed schema version, currently `1`. |
| `HumanApprovalDecision` | Human decision vocabulary: approve, reject or request revision. |
| `ConflictResolutionAction` | Human conflict resolution vocabulary. |
| `TicketApprovalState` | Resulting approval record state. |
| `CanonicalTicketSource` | Approved ticket source: synthesized candidate or manual replacement. |
| `TicketPublicationState` | Logical publication state vocabulary. |
| `TicketPublicationFormat` | Canonical artifact format vocabulary. |
| `HumanApprovalEvidence` | Human reviewer ID, decision reference and rationale. |
| `HumanConflictResolution` | Human resolution for one P16.5 conflict ID. |
| `ManualTicketReplacement` | Replacement `TicketSpec` plus human evidence. |
| `FreshDependencyPlanningEvidence` | Recomputable dependency-planning evidence. |
| `TicketApprovalRequest` | Approval input envelope. |
| `TicketApprovalRecord` | Immutable approval or nonapproval evidence. |
| `TicketPublicationEvidence` | Human publication evidence. |
| `TicketPublicationRequest` | Publication input envelope. |
| `PublishedTicketArtifact` | In-memory canonical ticket artifact evidence. |
| `TicketSupersessionRecord` | Logical supersession evidence for replacement publication. |
| `TicketPublicationResult` | Publication result plus input/result digests. |
| `TicketApprovalPublishingError` | Base approval/publication exception. |
| `TicketApprovalInputError` | Approval input inconsistency. |
| `TicketApprovalValidationError` | Invalid review, lint or planning evidence. |
| `TicketPublicationAuthorizationError` | Publication authorization failure. |
| `build_ticket_approval_record` | Deterministic in-memory approval record builder. |
| `publish_canonical_ticket` | Deterministic in-memory logical publication builder. |

Digest algorithm constants are intentionally not exported through the package root.

## Approval Request Contract

`TicketApprovalRequest` field order is `project_spec`, `seed_ticket`, `synthesis_review`, `decision`, `conflict_resolutions`, `approval_evidence`, `manual_replacement`, `fresh_planning_evidence`.

The project ID must match the seed ticket. The synthesis review project and ticket IDs must match the seed ticket. If the review contains a candidate, the candidate project and ticket IDs must also match the seed ticket, and the candidate ticket type must match the seed ticket type.

Manual replacements must preserve seed `schema_version`, `project_id`, `ticket_id` and `ticket_type`. They may change planning fields only through explicit human replacement evidence. Duplicate replacement evidence references are rejected.

## Approval Decisions

| Decision | Resulting State | Ticket Evidence |
| --- | --- | --- |
| `approve` | `approved` | Requires a selected ticket from the P16.5 candidate or a manual replacement. |
| `reject` | `rejected` | Records nonapproval evidence and no approved ticket. |
| `request_revision` | `revision_required` | Records revision-request evidence and no approved ticket. |

Nonapproval decisions must not include manual replacement evidence or fresh planning evidence. Nonapproval conflict resolutions may only acknowledge or reject conflicts.

Approval decisions require exactly one human resolution for every P16.5 conflict. Reject resolutions cannot be used with approval. Human-review conflicts cannot be merely acknowledged. Blocking conflicts require a manual replacement resolution and replacement ticket.

## Fresh Lint And Planning Gates

Approved tickets are linted again with P16.4 `lint_ticket_collection()` as a one-ticket incomplete collection with no dependency plan. A blocked lint report blocks approval. A warning lint report requires human policy-warning acknowledgement.

If the selected ticket dependencies or scope differ from the seed ticket, `fresh_planning_evidence` is required. The supplied `TicketDependencyPlan` must equal `build_ticket_dependency_plan(planning_request)`, contain the selected ticket, match the selected ticket content and not mark the selected ticket blocked.

Planning evidence with unresolved soft external dependencies or selected-ticket scope-review waves requires explicit human planning-warning acknowledgement.

## Approval Record

`TicketApprovalRecord` field order is `schema_version`, `project_id`, `ticket_id`, `synthesis_review_SHA256`, `decision`, `state`, `canonical_source`, `approved_ticket`, `approval_evidence`, `conflict_resolutions`, `approved_ticket_lint_report`, `fresh_planning_evidence`, `approval_input_SHA256`, `approval_SHA256`.

Approval records are immutable, extra-forbid and self-validating. `approval_SHA256` excludes itself. An approved record must include an approved ticket, canonical source and fresh lint report. A nonapproved record must not include an approved ticket, canonical source, lint report or planning evidence.

## Publication Request Contract

`TicketPublicationRequest` field order is `approval_record`, `publication_evidence`, `prior_publication`, `supersession_rationale`.

Only an approved `TicketApprovalRecord` can be published. The approval record digest is revalidated before publication. Rejected or revision-required records are not publication authority.

Publication is logical and in-memory. `publish_canonical_ticket()` returns a `TicketPublicationResult`; it does not save JSON, create files, update a repository, publish a package, update a registry or notify an external system.

## Published Artifact And Supersession

The first publication for a ticket has revision `1`, publication ID `PUB-<ticket-id-with-dashes>-0001` and no supersession. A later publication with a prior artifact uses the next revision and records a `TicketSupersessionRecord` that links the prior publication ID to the replacement publication ID.

Prior publications must validate, match the approval record project and ticket ID, and include a human supersession rationale. Publication IDs are derived from ticket ID and revision; caller-supplied publication IDs are not accepted.

`PublishedTicketArtifact` includes the canonical `TicketSpec`, deterministic canonical ticket JSON, canonical ticket digest, approval digest, optional superseded publication ID and artifact digest. It is evidence, not storage.

## Digest Evidence

Approval input digest algorithm: `agent-platform-ticket-approval-input-sha256-v1`. It includes project spec, seed ticket, synthesis review, decision, canonical conflict resolutions, approval evidence, optional manual replacement and optional fresh planning evidence.

Approval record digest algorithm: `agent-platform-ticket-approval-record-sha256-v1`. It includes schema version, project ID, ticket ID, synthesis review digest, decision, state, canonical source, approved ticket or null, approval evidence, conflict resolutions, lint report or null, planning evidence or null and approval input digest. It excludes `approval_SHA256` itself.

Canonical ticket digest algorithm: `agent-platform-canonical-ticket-sha256-v1`. It hashes deterministic canonical ticket JSON.

Published artifact digest algorithm: `agent-platform-published-ticket-artifact-sha256-v1`. It excludes `artifact_SHA256` itself.

Supersession digest algorithm: `agent-platform-ticket-supersession-sha256-v1`. It binds superseded publication, replacement publication, state, rationale and evidence reference.

Publication input digest algorithm: `agent-platform-ticket-publication-input-sha256-v1`. It includes approval record, publication evidence, optional prior publication and optional supersession rationale.

Publication result digest algorithm: `agent-platform-ticket-publication-result-sha256-v1`. It excludes `result_SHA256` itself.

Digests are provenance evidence only. They are not cryptographic signatures, authorization tokens, repository object IDs or deployment identifiers.

## Serialization

Standard Pydantic `model_dump()`, `model_dump_json()`, `model_validate()`, `model_validate_json()` and `model_json_schema()` are supported. Public models are frozen, extra-forbid and validate defaults. JSON arrays normalize to tuples.

Filesystem serialization, YAML support, Markdown rendering, file loaders and file writers are absent.

## Synthetic Examples

Unanimous approval example: a P16.5 review with a clean candidate and no conflicts can be approved with `HumanApprovalDecision.APPROVE`, producing an approved record sourced from `synthesized_candidate`.

Human-review conflict example: a split P16.5 field requires a human conflict resolution. `acknowledge` is insufficient for approval; `accept_candidate` records explicit human acceptance of the candidate evidence.

Blocking conflict example: a blocked candidate cannot be approved as-is. Approval requires a manual replacement, a `resolve_with_manual_replacement` resolution for each blocking conflict and fresh planning evidence when scope or dependencies changed.

Publication example: an approved record can produce a revision-one `PublishedTicketArtifact` in memory. A later publication for the same ticket supersedes the prior artifact and records supersession evidence.

## Deferred Responsibilities

P16.7 owns the historical regression corpus. P16.8 owns the shadow pilot. WorkPacket execution remains deferred to P17.

P16.6 does not claim production readiness.
