# P16.4 Ticket Policy And Linter

P16.4 adds deterministic, immutable and non-mutating policy linting for Pepper Ticket Factory collections. It consumes a `ProjectSpec`, a bounded `TicketSpec` collection, an optional `TicketDependencyPlan`, a collection-completeness flag and the canonical governed-standard policy profile.

`TicketLintReport` is policy evidence, not approval or publication authority.

## Relationship To P16.0 Through P16.3

P16.0 owns `ProjectSpec` and `TicketSpec` schema validation. P16.1 owns bounded in-memory context-pack assembly. P16.2 owns non-executing generator-role and proposal envelopes. P16.3 owns dependency DAG construction and parallel-wave planning.

P16.4 does not modify those inputs, rebuild dependency plans, generate tickets, synthesize proposals, approve tickets, publish tickets or execute validation commands.

P16 uses one common branch, `p16-ticket-factory-and-parallel-planning`, with one reviewed commit per ticket. P16.4 begins only after committed and pushed P16.3.

## Authority Boundary

P16.4 performs Pydantic validation, deterministic text inspection, deterministic diagnostic construction, deterministic JSON encoding and SHA-256 hashing. It performs no filesystem access, glob expansion, Git inspection, network access, provider call, model selection, prompt rendering, agent invocation, worker invocation, tool invocation, ticket repair, WorkPacket creation or runtime execution.

## Schema Version

`TICKET_POLICY_SCHEMA_VERSION = 1`. `TicketPolicyProfile.schema_version` and `TicketLintReport.schema_version` are fixed to `Literal[1] = 1`. Alternative versions are rejected. Schema migration and runtime negotiation are absent.

## Enums

| Enum | Values |
| --- | --- |
| `TicketPolicyProfileName` | `governed_standard_v1` |
| `TicketLintSeverity` | `info`, `warning`, `error` |
| `TicketLintScope` | `project`, `collection`, `ticket` |
| `TicketLintDisposition` | `pass`, `pass_with_warnings`, `blocked` |
| `TicketLintRuleCode` | `allowed_paths_required`, `forbidden_actions_required`, `scope_exact_contradiction`, `required_forbidden_action_missing`, `authority_reference_required`, `recommended_commit_message_required`, `rollback_constraint_required`, `required_response_section_missing`, `required_validation_step_missing`, `forbidden_validation_command`, `dependency_plan_required`, `dependency_blocked`, `soft_external_dependency_unresolved`, `scope_review_required`, `closure_ticket_required`, `multiple_closure_tickets`, `closure_identifier_type_mismatch`, `closure_identifier_suffix_invalid`, `closure_dependency_coverage`, `duplicate_ticket_title`, `duplicate_commit_message`, `duplicate_completion_verdict` |

Enum aliases are absent and unrestricted enum strings are rejected.

## Canonical Governed-Standard Profile

There is exactly one built-in policy profile: `governed_standard_v1`. Runtime profile registration, filesystem profile loading, plugin discovery and profile mutation are absent.

Required response sections are `Summary`, `Files inspected`, `Files modified`, `Tests/commands run`, `Decisions made` and `Limitations`. Matching is case-insensitive and ignores surrounding whitespace. The linter does not rewrite response sections.

Required forbidden-action markers are `git add`, `git commit`, `git push`, `git reset`, `git clean`, `git stash`, `git worktree` and `Graphify`. A marker is satisfied when a normalized `forbidden_actions` entry contains it case-insensitively.

Required authority references apply to `architecture`, `integration` and `closure` tickets. The linter checks that at least one authority reference is marked `required=true`; it does not resolve or verify the reference.

Recommended commit messages are required for `implementation`, `refactor`, `test`, `bugfix`, `integration` and `closure` tickets. The linter never executes Git and never validates that a commit exists.

Rollback evidence is required for `implementation`, `refactor`, `bugfix`, `integration` and `closure` tickets. The markers are `rollback`, `restore`, `revert` and `remove only`. The linter scans `constraints`, `tasks` and `acceptance_criteria` case-insensitively and does not assess operational correctness.

Forbidden validation-command markers are `git add`, `git commit`, `git push`, `git reset`, `git clean`, `git stash`, `git worktree add`, `git worktree remove`, `graphify update`, `graphify extract`, `graphify export`, `graphify cluster` and `graphify recluster`. Commands are inspected only as text and are never executed, parsed by a shell or rewritten.

Closure suffixes are `R` and `CR`. Duplicate-title and duplicate-commit-message diagnostics are warnings. Duplicate completion-verdict diagnostics are errors.

## Request Contract

`TicketLintRequest` field order is `project_spec`, `tickets`, `dependency_plan`, `collection_complete`, `policy_name`. Ticket count is bounded from `1` through `512`. Ticket IDs must be unique. Ticket project IDs and ID prefixes must match the request `ProjectSpec`. A dependency plan, when present, must have the same project ID and ticket set. Ticket input order is not diagnostic or digest authority.

Input inconsistency raises `TicketPolicyInputError` from the public linter and no partial report is produced. Policy failures are diagnostics, not exceptions.

## Scope Policy

Every ticket requires non-empty `scope.allowed_paths` and non-empty `scope.forbidden_actions`. The same normalized path pattern in `allowed_paths` and `forbidden_paths` is an exact contradiction error. P16.4 does not attempt general glob intersection, path existence checks or glob expansion.

Every required forbidden-action marker must be present. Missing markers are deterministic errors. Tickets are not mutated.

## Authority, Commit And Rollback Policy

Authority-reference diagnostics do not resolve referenced tickets, commits, paths or external sources. Commit-message diagnostics do not call Git. Rollback diagnostics scan only declared text fields and do not claim the rollback instructions are sufficient.

## Response Policy

Every ticket must contain all canonical response sections. Missing sections are errors. Section matching is case-insensitive and whitespace-normalized. Completion verdicts are linted as ticket outcome identifiers and are not approval authority.

## Validation Policy

Every ticket must contain at least one validation step with `required=true`. Optional-only validation steps are errors. Non-null command text is scanned for forbidden Git-write and Graphify-mutation markers. Diagnostics identify validation IDs and matched markers but withhold full command text.

Command execution, shell parsing, command rewriting and command-safety claims are absent.

## Dependency And Scope Review Policy

Collections with more than one ticket require a matching `TicketDependencyPlan`. One-ticket collections may omit it. P16.4 does not rebuild, repair or alter the plan.

Every `blocked_ticket_ids` entry becomes a ticket-level error. Deterministic blocker identifiers may be summarized, but full dependency objects are not duplicated in diagnostics. The linter never attempts to satisfy or override blockers.

Every `unresolved_soft_external_dependency_ids` entry becomes a nonblocking collection warning. Soft dependencies remain advisory and are not converted to hard blockers.

Every wave with disposition `scope_review_required` becomes a collection warning. The warning states that ambiguous declared-scope evidence requires human review. It does not claim an actual write conflict, safe parallel execution or runtime isolation.

## Closure Policy

A closure identifier is any ticket ID whose final segment is `R` or `CR`. Such an identifier requires `ticket_type=closure`. A closure ticket must use an `R` or `CR` suffix. The linter does not rename tickets.

When `collection_complete=true`, exactly one closure ticket is required. Zero closure tickets and multiple closure tickets are collection errors. Incomplete collections may omit closure tickets.

When a complete collection has exactly one closure ticket and a dependency plan, every non-closure ticket must be a transitive hard internal prerequisite of the closure ticket. Direct dependencies are not required when transitive coverage exists. Soft and external dependencies do not satisfy coverage. The rule is sequencing evidence only and does not approve project closure.

## Duplicate Policy

Titles and recommended commit messages normalize by stripping, casefolding and collapsing consecutive whitespace. Duplicate diagnostics are emitted for every ticket after the first ticket in canonical ticket order. Titles and messages are not rewritten.

Completion verdicts use their validated token form. A duplicate completion verdict is an error because the verdict must uniquely identify one ticket outcome within the linted collection. The verdict remains non-approval evidence.

## Diagnostic Contract

`TicketLintDiagnostic` field order is `diagnostic_id`, `code`, `severity`, `scope`, `ticket_id`, `field_path`, `message`, `remediation`, `blocking`.

Diagnostic IDs are assigned after canonical sorting as `LINT-0001`, `LINT-0002` and later values. Errors are blocking. Warnings and info diagnostics are nonblocking. Ticket-scope diagnostics require `ticket_id`; project and collection diagnostics require `ticket_id=null`.

Diagnostics are sorted by severity rank, scope rank, ticket ID with null first, rule-code enum order, field path and message. Input ticket order, filesystem order and locale are not authority. Diagnostics do not contain full specs, full validation commands, provider output, secrets or reasoning traces.

## Summary And Disposition

`TicketLintSummary` field order is `ticket_count`, `diagnostic_count`, `error_count`, `warning_count`, `info_count`, `blocked_ticket_ids`, `warning_ticket_ids`, `collection_blocked`. Counts are nonnegative and diagnostic count equals the severity-count sum. Blocked and warning ticket IDs are unique and canonical.

`TicketLintDisposition` is `blocked` when any error exists, `pass_with_warnings` when no errors and at least one warning exist, and `pass` when no errors or warnings exist. A collection-level error can block a report without adding a ticket to `blocked_ticket_ids`.

## Digest Evidence

Lint input digest algorithm: `agent-platform-ticket-policy-input-sha256-v1`. The digest includes `ProjectSpec`, canonically ordered tickets, `TicketDependencyPlan` or null, `collection_complete`, `policy_name` and the canonical policy profile using deterministic JSON.

Lint report digest algorithm: `agent-platform-ticket-lint-report-sha256-v1`. The digest includes schema version, project ID, policy name, ticket IDs, input digest, diagnostics, summary and disposition. It excludes `report_SHA256` itself.

Digests are provenance evidence only. They are not security signatures, approval signatures or publication identities.

## Examples

Passing example: one implementation ticket with allowed paths, all required forbidden-action markers, a recommended commit message, rollback evidence, all response sections and at least one required validation step produces `pass`.

Passing-with-warnings example: a ticket with an unresolved soft external dependency in a supplied dependency plan produces `pass_with_warnings` and no hard blocker.

Blocked example: a ticket with empty allowed paths or a missing required response section produces `blocked`.

Closure-coverage failure example: a complete collection with a closure ticket that lacks transitive hard internal prerequisite coverage for an implementation ticket produces `closure_dependency_coverage`.

Forbidden validation-command example: a validation step containing a forbidden marker such as `git commit` or `graphify update` produces `forbidden_validation_command`; the command is not executed and the full command text is withheld.

## Serialization

Standard Pydantic `model_dump()`, `model_dump_json()`, `model_validate()`, `model_validate_json()` and `model_json_schema()` are supported. Enum values round trip and tuple immutability is retained. Filesystem serialization, YAML support, Markdown rendering, file loaders and file writers are absent.

Serialization is not canonical ticket publication.

## Deferred Responsibilities

P16.5 owns multi-generator proposal synthesis and conflict review. P16.6 owns human approval and canonical publishing. P16.7 owns historical regression corpus. P16.8 owns the shadow pilot. WorkPacket execution remains deferred to P17.

P16.4 does not claim production readiness.
