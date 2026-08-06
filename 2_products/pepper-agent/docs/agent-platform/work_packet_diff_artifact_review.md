# P17.6 - Deterministic Diff And Artifact Review

P17.6 adds deterministic, human-observed diff and artifact review for one terminal P17.5 `OutcomeEnvelope`. It classifies caller-supplied observations against the compiled WorkPacket mutation policy without inspecting the filesystem, invoking Git, running subprocesses, calling providers or models, staging files, cleaning workspaces, rolling back changes, committing, pushing, running Docker, or running Graphify.

Final verdict: hermes_0_19_pepper_diff_and_artifact_review_ready_with_deterministic_human_observed_non_mutating_candidate_and_artifact_authority

## Prerequisites

P17.6 consumes these governed contracts:

| Stage | Requirement |
| --- | --- |
| P17.0 | A compiled WorkPacket with repository scope and allowed mutation actions. |
| P17.1 | A bound human-provisioned workspace allocation and repository identity. |
| P17.2 | A deny-first tool permission profile bound to the same WorkPacket and allocation. |
| P17.5 | One terminal result, failure, or cancellation outcome envelope. |

P17.6 never repairs prerequisite evidence and never modifies P17.0 through P17.5 contracts. It validates immutable prerequisite models, checks digest and identity bindings, then builds a bounded review result from the supplied human observation.

## Human Observation

`DiffArtifactReviewObservation` is the only source of diff and artifact evidence. It must be explicitly human-observed with `synthetic=false`, a non-shadow `human_observer_id`, an empty index, zero staged files, and repository identity fields matching the P17.1 allocation.

Observed paths are repository-relative, sorted, contiguous by `OPATH-###`, and never staged. Path validation rejects absolute paths, drive-letter paths, backslashes, traversal, Git metadata, environment files, and credential-shaped components.

P17.6 records only bounded path status, byte counts, content SHA-256 values, artifact metadata, finding summaries, and deterministic digests. It does not record raw diffs, file contents, directory listings, stdout/stderr bodies, prompts, reasoning traces, provider payloads, Git output, Docker output, or Graphify output.

## Expected Mutations

`build_review_expected_mutations` derives expected mutation records from WorkPacket `repository_scope.allowed_actions` using exact action strings:

| Action | Allowed observed status |
| --- | --- |
| `create_file:<path>|<kind>` | `added` or `untracked` |
| `modify_file:<path>|<kind>` | `modified` |
| `replace_file:<path>|<kind>` | `modified` |
| `delete_file:<path>|<kind>` | `deleted` |

Artifact kinds are `source`, `test`, `documentation`, `configuration`, `manifest`, `generated`, `log`, `report`, `binary`, `cache`, `temporary`, and `unknown`. Duplicate expected mutation paths fail closed.

## Review Verdicts

P17.6 emits three verdict surfaces:

| Verdict | Values |
| --- | --- |
| `DiffReviewVerdict` | `accepted`, `requires_human_review`, `blocked` |
| `ArtifactReviewVerdict` | `accepted`, `requires_human_review`, `blocked` |
| `AggregateReviewState` | `completed`, `blocked` |

Missing expected paths, unexpected observed paths, unmerged paths, path-policy violations, unexpected artifacts, prohibited artifacts, unknown artifact origins, missing artifact hashes, non-terminal outcomes, and inconsistent diff stats produce blocking findings. Review-required artifact kinds produce warning findings when they match the WorkPacket's expected artifact kind.

`human_git_handoff_ready`, `automatic_cleanup_authorized`, `automatic_rollback_authorized`, and `automatic_staging_authorized` are always `false`. Provider dispatch and model inference counts are always zero.

## Digest Algorithms

| Evidence | Algorithm |
| --- | --- |
| Expected mutation | `agent-platform-review-expected-mutation-sha256-v1` |
| Observed path | `agent-platform-review-observed-path-sha256-v1` |
| Diff stat | `agent-platform-review-diff-stat-sha256-v1` |
| Artifact observation | `agent-platform-review-artifact-observation-sha256-v1` |
| Finding | `agent-platform-review-finding-sha256-v1` |
| Human observation | `agent-platform-diff-artifact-review-observation-sha256-v1` |
| Review ID | `agent-platform-diff-artifact-review-id-sha256-v1` |
| Review result | `agent-platform-diff-artifact-review-result-sha256-v1` |

Digests are deterministic integrity evidence, not signatures.

## Public Exceptions And JSON Boundary

The public policy ID is `pepper-human-observed-deterministic-diff-artifact-review-v1`.

Public exceptions are `DiffArtifactReviewError`, `DiffArtifactReviewInputError`, `DiffArtifactReviewIntegrityError`, `DiffArtifactReviewPolicyError`, `DiffArtifactReviewStateError`, and `DiffArtifactReviewValidationError`. Errors expose bounded invariant identifiers only.

All public models are immutable Pydantic models with forbidden extra fields and JSON round-trip support through `model_dump`, `model_dump_json`, `model_validate`, `model_validate_json`, and `model_json_schema`. P17.6 does not define YAML support, database persistence, session-file persistence, artifact persistence, process-handle serialization, thread-handle serialization, environment serialization, or log-file persistence.

## Residual Limitations

P17.6 is a non-mutating review layer only. It does not prove semantic task correctness beyond observed path and artifact policy, does not inspect the workspace itself, does not run validation, does not create outcome envelopes, does not stage, commit or push, and does not grant human Git handoff authority.
