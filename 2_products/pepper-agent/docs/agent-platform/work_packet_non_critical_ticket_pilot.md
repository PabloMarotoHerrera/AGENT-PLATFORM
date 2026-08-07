# P17.8 - Non-Critical Ticket Pilot

P17.8 adds a deterministic, non-executing non-critical ticket pilot contract for one human-selected WorkPacket chain that has already passed P17.0 through P17.7. It binds existing evidence, validates policy posture, summarizes stage readiness, and emits an accepted or rejected pilot result without inspecting the filesystem, invoking Git, running subprocesses, calling providers or models, staging files, committing, pushing, cleaning workspaces, rolling back changes, running Docker, or running Graphify.

Final verdict: hermes_0_19_pepper_non_critical_ticket_pilot_ready_with_complete_governed_work_packet_chain_and_human_only_git_handoff_evidence

## Prerequisites

P17.8 consumes these governed contracts:

| Stage | Requirement |
| --- | --- |
| P17.0 | A compiled WorkPacket with exact repository mutation scope. |
| P17.1 | A bound human-provisioned workspace allocation and repository identity. |
| P17.2 | A deny-first tool permission profile bound to the same WorkPacket and allocation. |
| P17.3 | A completed single-agent execution result with zero provider and model authority. |
| P17.4 | A completed validation-command runner result with exact validation command evidence. |
| P17.5 | One terminal result outcome envelope. |
| P17.6 | One completed diff and artifact review. |
| P17.7 | One completed human-only Git handoff result with zero Git commands executed. |

P17.8 never repairs prerequisite evidence and never modifies P17.0 through P17.7 contracts. `validate_non_critical_ticket_pilot_request` is strict and rejects invalid prerequisite state. `build_non_critical_ticket_pilot` can produce a rejected result from blocked or unsafe downstream evidence so the pilot verdict remains deterministic and bounded.

## Ticket Selection

`PilotTicketSelection` records the human-selected ticket identity, revision, title, expected candidate paths, expected validation IDs, non-critical risk class, selection rationale, and criticality acknowledgement. It requires `selected_by_human=true`, `synthetic=false`, immutable tuples, unique candidate paths, unique validation IDs, deterministic `selection_id`, and deterministic `selection_SHA256`.

The selected ticket must bind back to the P17.0 WorkPacket ticket ID, title, and publication revision. Candidate paths must match the P17.7 handoff candidate set. Validation IDs must match P17.4 passed validation IDs plus preserved manual validation IDs.

## Eligibility Policy

`build_pilot_eligibility_policy` returns the fixed non-critical pilot policy. The policy allows at most ten changed files, at most five created files, at most ten modified files, zero deleted files, untracked file evidence, exact validation commands, completed diff review, and completed human Git handoff.

The policy forbids dependency changes, lockfile changes, credentials, network access, provider dispatch, model inference, Docker, Graphify, Git mutation, branch mutation, database migration, production deployment, and destructive actions.

## Pilot Result

`build_non_critical_ticket_pilot` emits a `NonCriticalTicketPilotResult` with eight `PilotStageEvidence` records in exact P17.0 through P17.7 order, deterministic `PilotFinding` records, and one `PilotAcceptanceSummary`.

Accepted pilots require all stage requirements to be satisfied, zero blocking findings, zero Git commands executed, zero provider dispatches, zero model inferences, and no automatic authority. Rejected pilots are blocked, do not satisfy the WorkPacket execution MVP, and do not mark P17 closure ready.

P17.8 never claims production readiness. `production_readiness_claimed` is always `false`.

## Authority Boundary

P17.8 records only bounded metadata, enum states, path identifiers, validation IDs, stage summaries, counts, and deterministic SHA-256 digests. It does not record raw diffs, file contents, directory listings, stdout/stderr bodies, prompts, reasoning traces, provider payloads, Git output, Docker output, Graphify output, environment variables, absolute user paths, credentials, or shell commands.

`Git_commands_executed`, provider dispatch count, and model inference count must remain zero for acceptance. Automatic retry, fallback, cleanup, rollback, staging, commit, and push authorization remain false in the acceptance summary.

## Digest Algorithms

| Evidence | Algorithm |
| --- | --- |
| Eligibility policy | `agent-platform-non-critical-pilot-eligibility-policy-sha256-v1` |
| Ticket selection | `agent-platform-non-critical-pilot-ticket-selection-sha256-v1` |
| Stage evidence | `agent-platform-non-critical-pilot-stage-evidence-sha256-v1` |
| Finding | `agent-platform-non-critical-pilot-finding-sha256-v1` |
| Acceptance summary | `agent-platform-non-critical-pilot-acceptance-summary-sha256-v1` |
| Pilot ID | `agent-platform-non-critical-ticket-pilot-id-sha256-v1` |
| Pilot result | `agent-platform-non-critical-ticket-pilot-result-sha256-v1` |

Digests are deterministic integrity evidence, not signatures.

## Public Exceptions And JSON Boundary

The public policy ID is `pepper-complete-governed-non-critical-ticket-pilot-v1`.

Public exceptions are `NonCriticalTicketPilotError`, `NonCriticalTicketPilotInputError`, `NonCriticalTicketPilotIntegrityError`, `NonCriticalTicketPilotPolicyError`, `NonCriticalTicketPilotStateError`, and `NonCriticalTicketPilotValidationError`. Errors expose bounded invariant identifiers only.

All public models are immutable Pydantic models with forbidden extra fields and JSON round-trip support through `model_dump`, `model_dump_json`, `model_validate`, `model_validate_json`, and `model_json_schema`. P17.8 does not define YAML support, database persistence, session-file persistence, artifact persistence, process-handle serialization, thread-handle serialization, environment serialization, or log-file persistence.

## Residual Limitations

P17.8 is a pilot evidence binder only. It does not execute the selected ticket, prove semantic task correctness, inspect the workspace itself, complete manual validation IDs, create outcome envelopes, perform review, render Git handoff instructions, stage, commit, push, deploy, or authorize production use.
