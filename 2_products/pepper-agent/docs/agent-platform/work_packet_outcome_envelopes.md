# P17.5 - Result, Failure And Cancellation Envelopes

P17.5 adds deterministic WorkPacket outcome envelopes for already-terminal P17.3/P17.4 evidence. It produces one bounded result, failure or cancellation envelope without executing agents, tools, validation commands, Git, Docker, Graphify, providers or models.

Final verdict: hermes_0_19_pepper_result_failure_cancellation_envelopes_ready_with_deterministic_bounded_terminal_outcome_authority

## Prerequisites

P17.5 consumes these governed contracts:

| Stage | Requirement |
| --- | --- |
| P17.3 | A completed, blocked or cancelled single-agent execution session/result. |
| P17.4 | A completed, blocked or cancelled validation-command runner session/result when validation has started. |

The module never repairs prerequisite evidence and never modifies P17.3 or P17.4 contracts. It validates the supplied immutable models, checks digest bindings where both sides are provided, and then projects terminal evidence into one envelope.

## Envelope Kinds

P17.5 exposes exactly three outcome kinds:

| Kind | Model | Source terminal state |
| --- | --- | --- |
| `result` | `ResultEnvelope` | Completed P17.4 runner result plus the bound P17.3 execution result. |
| `failure` | `FailureEnvelope` | Blocked P17.3 session or blocked P17.4 runner session. |
| `cancellation` | `CancellationEnvelope` | Cancelled P17.3 session or cancelled P17.4 runner session. |

`OutcomeEnvelope` wraps exactly one of those envelopes. `OutcomeEnvelopeRequest` and `build_outcome_envelope` select the correct terminal envelope from supplied evidence. Non-terminal prepared/active sessions are rejected.

## Terminal Mapping

P17.5 uses the actual P17.3/P17.4 public terminal contracts:

| Prerequisite evidence | P17.5 projection |
| --- | --- |
| `SingleAgentExecutionState.BLOCKED` with denied action evidence | `single_agent_action_denied` failure. |
| `SingleAgentExecutionState.CANCELLED` | `single_agent_cancelled` cancellation. |
| `ValidationCommandRunnerState.BLOCKED` with `NONZERO_EXIT` | `validation_command_nonzero_exit` failure. |
| `ValidationCommandRunnerState.BLOCKED` with `TIMEOUT` | `validation_command_timeout` failure. |
| `ValidationCommandRunnerState.BLOCKED` with `OUTPUT_LIMIT` | `validation_command_output_limit` failure. |
| `ValidationCommandRunnerState.BLOCKED` with `LAUNCH_ERROR` | `validation_command_launch_error` failure. |
| `ValidationCommandRunnerState.CANCELLED` | `validation_command_cancelled` cancellation. |
| `ValidationCommandRunnerResult` completed | `result` envelope. |

P17.3 does not define `SingleAgentActionFailureReason` or `SingleAgentActionState`; P17.5 therefore maps from the committed public `SingleAgentActionDisposition` and session state fields.

## Bounded Evidence

`WorkPacketTerminalEvidence` records only deterministic identifiers, digests, terminal source, terminal state, terminal disposition, and failure/cancellation reason. It does not retain file contents, directory listings, stdout/stderr retained text, prompts, reasoning traces, provider payloads, process handles, thread handles, Git output, Docker output or Graphify output.

Result envelopes include completed task IDs, bounded path sets already present in the P17.3 result, passed validation IDs, manual validation IDs still pending, and prerequisite result digests. Failure and cancellation envelopes include the terminal action or command identifiers when available.

All outcome envelopes preserve this downstream posture:

| Capability | P17.5 status |
| --- | --- |
| Outcome envelope requirement | satisfied |
| Diff and artifact review | deferred to P17.6 |
| Human Git handoff | deferred to P17.7 |
| Provider dispatch | absent |
| Model inference | absent |
| Git mutation | absent |

## Digest Algorithms

| Evidence | Algorithm |
| --- | --- |
| Terminal evidence | `agent-platform-work-packet-terminal-outcome-evidence-sha256-v1` |
| Result envelope | `agent-platform-work-packet-result-envelope-sha256-v1` |
| Failure envelope | `agent-platform-work-packet-failure-envelope-sha256-v1` |
| Cancellation envelope | `agent-platform-work-packet-cancellation-envelope-sha256-v1` |
| Outcome wrapper | `agent-platform-work-packet-outcome-envelope-sha256-v1` |
| Projection result | `agent-platform-work-packet-outcome-projection-result-sha256-v1` |

Digests are deterministic integrity evidence, not signatures.

## Public Exceptions And JSON Boundary

The public policy ID is `pepper-deterministic-bounded-terminal-outcome-envelopes-v1`.

Public exceptions are `OutcomeEnvelopeError`, `OutcomeEnvelopeInputError`, `OutcomeEnvelopeIntegrityError`, `OutcomeEnvelopePolicyError`, `OutcomeEnvelopeStateError`, and `OutcomeEnvelopeValidationError`. Errors expose bounded invariant identifiers only.

All public models are immutable Pydantic models with forbidden extra fields and JSON round-trip support through `model_dump`, `model_dump_json`, `model_validate`, `model_validate_json`, and `model_json_schema`. P17.5 does not define YAML support, database persistence, session-file persistence, artifact persistence, process-handle serialization, thread-handle serialization, environment serialization or log-file persistence.

## Residual Limitations

P17.5 is a terminal projection layer only. It does not prove semantic task success beyond P17.3/P17.4 evidence, does not execute missing validation, does not retry failed commands, does not resume cancelled sessions, does not inspect or write files, does not review diffs or artifacts, does not stage, commit or push, and does not claim production readiness.
