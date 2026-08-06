# P17.7 - Human Git Handoff

P17.7 adds deterministic, non-executing human Git handoff contracts for one completed P17.6 `DiffArtifactReviewResult`. It converts exact reviewed candidates, human approval, verification steps, declarative command records, post-commit expectations, and bounded PowerShell text into immutable evidence without inspecting the filesystem, invoking Git, running subprocesses, reading environment variables, calling providers or models, staging files, committing, pushing, cleaning workspaces, rolling back changes, running Docker, or running Graphify.

Final verdict: hermes_0_19_pepper_human_git_handoff_ready_with_exact_review_bound_non_executing_human_only_git_authority

## Prerequisites

P17.7 consumes these governed contracts:

| Stage | Requirement |
| --- | --- |
| P17.0 | A compiled WorkPacket with exact repository mutation scope. |
| P17.1 | A bound human-provisioned workspace allocation and repository identity. |
| P17.2 | A deny-first tool permission profile bound to the same WorkPacket and allocation. |
| P17.5 | One terminal result, failure, or cancellation outcome envelope. |
| P17.6 | One completed diff and artifact review whose observed paths exactly match expected mutations. |

P17.7 never repairs prerequisite evidence and never modifies P17.0 through P17.6 contracts. It validates immutable prerequisite models, digest bindings, repository identity bindings, review posture, and human approval posture before building a handoff result.

## Human Approval

`GitHandoffApproval` is the only approval input. It must be explicitly human, `synthetic=false`, and issued by a non-shadow approver. It binds to the exact P17.6 review ID and review digest, the exact accepted candidate IDs, the exact warning finding IDs when the review required human review, the exact branch, the `origin` remote, the expected parent commit, and one bounded commit message.

Approval does not authorize automation. It records intent for a human to run the rendered handoff instructions outside the contract builder.

## Candidate Boundary

`build_git_handoff_candidates` derives candidates only from the reviewed P17.6 observed paths. Added and untracked observations become `added`; modified observations become `modified`; deleted observations become `deleted`. Candidate IDs are contiguous `GHCP-###`, sorted by repository-relative path, and each candidate carries a deterministic SHA-256 digest.

Candidate paths reject absolute paths, drive-letter paths, backslashes, traversal, Git metadata, environment files, and credential-shaped path components. Nondeleted candidates require content SHA-256 and byte-count evidence; deleted candidates must not carry content evidence.

## Handoff Package

`build_human_git_handoff` emits a `GitHandoffResult` with `authority=human_only`. The nested `GitHandoffPackage` contains:

| Evidence | Purpose |
| --- | --- |
| Candidates | Exact reviewed path set and status set. |
| Verification steps | Blocking pre-staging, candidate-set, staged-index, post-commit, post-push, and committed-integrity checks. |
| Commands | Declarative argv records for human execution only. |
| Post-commit expectation | Expected parent, branch, remote, commit message, path set, status counts, clean worktree, remote match, and Pepper integrity file count. |
| Rendered PowerShell digest | Deterministic digest of bounded handoff text returned in memory only. |

The package and result are deterministic integrity evidence, not signatures.

## Rendered PowerShell

`render_human_git_handoff_powershell` returns bounded PowerShell text for a human to review and run. It does not write the text to disk, launch PowerShell, spawn Git, or inspect the workspace.

The rendered text includes guarded checks for current branch, expected parent, remote parent, empty index, unstaged candidate set, staged candidate set, staged diff checks, commit parent, commit message, committed path set, remote head, clean worktree, and committed Pepper integrity. It rejects rendered forms containing destructive Git verbs, force push, amend, shell evaluation, nested shell launch, or wildcard staging.

## Authority Boundary

`Git_commands_executed` is always zero. `staging_performed`, `commit_performed`, `push_performed`, `automatic_cleanup_authorized`, `automatic_rollback_authorized`, `automatic_staging_authorized`, `automatic_commit_authorized`, and `automatic_push_authorized` are always `false`. Provider dispatch and model inference counts are always zero.

P17.7 imports no operational modules for filesystem, process, network, provider, workspace mutation, Git mutation, Docker, Graphify, random identity, time identity, or environment authority.

## Digest Algorithms

| Evidence | Algorithm |
| --- | --- |
| Candidate | `agent-platform-git-handoff-candidate-sha256-v1` |
| Approval | `agent-platform-git-handoff-approval-sha256-v1` |
| Verification step | `agent-platform-git-handoff-verification-step-sha256-v1` |
| Command | `agent-platform-git-handoff-command-sha256-v1` |
| Post-commit expectation | `agent-platform-git-handoff-post-commit-expectation-sha256-v1` |
| Package | `agent-platform-human-git-handoff-package-sha256-v1` |
| Handoff ID | `agent-platform-human-git-handoff-id-sha256-v1` |
| Result | `agent-platform-human-git-handoff-result-sha256-v1` |
| Rendered PowerShell | `agent-platform-human-git-handoff-powershell-sha256-v1` |

## Public Exceptions And JSON Boundary

The public policy ID is `pepper-exact-review-bound-non-executing-human-git-handoff-v1`.

Public exceptions are `HumanGitHandoffError`, `HumanGitHandoffInputError`, `HumanGitHandoffIntegrityError`, `HumanGitHandoffPolicyError`, `HumanGitHandoffStateError`, and `HumanGitHandoffValidationError`. Errors expose bounded invariant identifiers only.

All public models are immutable Pydantic models with forbidden extra fields and JSON round-trip support through `model_dump`, `model_dump_json`, `model_validate`, `model_validate_json`, and `model_json_schema`. P17.7 does not define YAML support, database persistence, session-file persistence, artifact persistence, process-handle serialization, thread-handle serialization, environment serialization, or log-file persistence.

## Residual Limitations

P17.7 is a human handoff package builder only. It does not prove semantic task correctness, does not inspect the workspace itself, does not complete manual validation IDs, does not create outcome envelopes, does not stage, commit or push, and does not verify that a human later ran the rendered instructions.
