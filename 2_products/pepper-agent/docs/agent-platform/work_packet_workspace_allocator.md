# WorkPacket Workspace Allocator

P17.1 adds the human-provisioned workspace allocation boundary for Pepper WorkPackets. It validates one existing linked Git worktree, binds it to one immutable P17.0 `WorkPacket`, and returns an immutable allocation result plus an updated in-memory registry.

P17.1 requires the P17.0 TicketSpec to WorkPacket compiler to be committed and pushed on the common P17 branch. P17.0 provides compile-only WorkPackets with `execution_ready=false`, human-only Git authority, and an unsatisfied `workspace_allocation` downstream requirement.

## Human-Provisioned Model

Pepper does not create the worktree. A human provisions the linked Git worktree before allocation, chooses the source commit and branch, and remains responsible for later removal.

P17.1 validates the supplied workspace root and Git identity, then reserves that existing workspace in a caller-supplied immutable registry. The registry is in memory only. It is not a filesystem lock, database lease, remote control-plane lease, or durable multi-process allocator.

## Allocation Authorization

`WorkspaceAllocationAuthorization` is explicit human evidence authorizing reservation of one already-provisioned workspace for one compile-only WorkPacket.

The authorization binds the WorkPacket ID, WorkPacket SHA-256, repository identity SHA-256, workspace root, workspace kind, and human-only Git authority. It does not authorize worktree creation, Git mutation, tool grants, agent execution, validation-command execution, cleanup, or production readiness.

Authorizers beginning with `SHADOW-` are rejected.

## Repository Identity

`WorkspaceRepositoryIdentity` binds:

| Field | Meaning |
| --- | --- |
| `repository_id` | Bounded repository identifier supplied by the caller. |
| `source_commit` | Expected 40-character lowercase Git commit. |
| `workspace_branch` | Expected named branch for the linked worktree. |
| `identity_SHA256` | Deterministic digest of the identity fields. |

Detached `HEAD` is not a valid workspace branch identity. Branch identifiers reject whitespace, leading hyphen, backslash, double-dot, `@{`, `~`, `^`, `:`, `?`, `*`, `[`, and control characters.

## Workspace Root Rules

Workspace roots are public strings, not `Path` fields. They must be absolute and use forward slashes in serialized form.

Rejected roots include relative paths, backslash paths, parent traversal, NUL characters, non-root trailing separators, paths inside `.git`, `.opencode`, `graphify-out`, `4_external/sources`, and the Pepper upstream baseline file.

The allocator checks filesystem metadata only for the supplied root: existence, directory posture, symlink posture, and canonical resolved root. It does not read repository file contents.

## Read-Only Git Inspection

P17.1 uses exactly these read-only Git command shapes:

```text
git --no-optional-locks -C <workspace-root> rev-parse --show-toplevel
git --no-optional-locks -C <workspace-root> rev-parse HEAD
git --no-optional-locks -C <workspace-root> branch --show-current
git --no-optional-locks -C <workspace-root> rev-parse --is-inside-work-tree
git --no-optional-locks -C <workspace-root> rev-parse --git-dir
git --no-optional-locks -C <workspace-root> rev-parse --git-common-dir
git --no-optional-locks -C <workspace-root> status --porcelain=v1 -uall
```

Execution uses `shell=False`, captures output, uses UTF-8 text decoding, disables optional Git locks, and has a fixed five-second timeout. Callers cannot append Git arguments.

The allocator does not run `git fetch`, `git pull`, `git clone`, `git checkout`, `git switch`, `git worktree`, `git add`, `git commit`, `git push`, `git merge`, `git rebase`, `git reset`, `git clean`, `git stash`, `git branch`, or `git tag`.

## Linked Worktree Verification

The supplied workspace must be inside a Git work tree, its top-level must equal the resolved workspace root, `HEAD` must equal the expected source commit, and the named branch must equal the expected workspace branch.

Linked-worktree verification uses the relationship between `--git-dir` and `--git-common-dir`. A primary checkout is rejected because its Git directory and common Git directory are the same.

The worktree must be clean. Any tracked or untracked status entry rejects allocation.

## Scope Projection

`WorkspaceScopeProjection` copies the WorkPacket repository scope exactly:

| Field | Projection |
| --- | --- |
| `allowed_paths` | Exact source tuple, order preserved. |
| `forbidden_paths` | Exact source tuple, order preserved. |
| `allowed_actions` | Exact source tuple, order preserved. |
| `forbidden_actions` | Exact source tuple, order preserved. |

`scope_enforcement_ready` is always false. P17.1 does not expand, reduce, reorder, infer, or enforce scope. Tool-level enforcement is deferred to P17.2.

## Registry And Collisions

`WorkspaceAllocationRegistry` is immutable and caller supplied. The empty registry has revision `0` and no reservations. An allocation returns an updated registry with revision incremented by one.

Reservations are sorted by allocation ID. Registry validation rejects duplicate allocation IDs, duplicate WorkPacket IDs, duplicate workspace roots, duplicate resolved workspace roots, duplicate workspace branches, and overlapping roots where one root is equal to, an ancestor of, or a descendant of another. Root comparison is conservatively case-insensitive.

Same source commit is allowed across different valid worktrees.

## Allocation Result

`allocate_workspace` returns `WorkspaceAllocationResult` with `disposition=allocated`, one `WorkspaceAllocation`, and an updated registry.

The allocation records dedicated isolation, exclusive reservation, workspace requirement satisfaction, execution readiness false, tool permissions readiness false, human-only Git authority, and cleanup eligibility `not_eligible`.

The allocation contains no tool profile, provider ID, model ID, agent ID, worker ID, process ID, execution ID, command result, diff, artifact contents, Git mutation command, or credentials.

## Deterministic Identity

Allocation ID shape:

```text
WS-<NORMALIZED-TICKET-ID>-R<4-DIGIT-REVISION>-<12-LOWERCASE-HEX>
```

The suffix is the first twelve characters of `allocation_input_SHA256`. The allocator uses no clock, UUID, random, or process-global registry state.

## Cleanup Eligibility

`assess_workspace_cleanup_eligibility` is an in-memory assessment only. Eligibility is `eligible` only when execution is inactive, unreviewed changes are absent, artifacts are preserved, and human Git handoff is complete.

The function does not delete files, remove directories, run `git worktree remove`, mutate a registry, or change an allocation lifecycle. Actual worktree removal remains human-controlled.

## Exceptions

| Exception | Use |
| --- | --- |
| `WorkspaceAllocatorInputError` | Structural input or binding failure. |
| `WorkspaceAllocatorAuthorizationError` | Invalid or missing allocation authorization. |
| `WorkspaceAllocatorInspectionError` | Rejected read-only workspace inspection. |
| `WorkspaceAllocatorCollisionError` | Registry collision or overlap. |
| `WorkspaceAllocatorIntegrityError` | Digest or nested integrity failure. |

Errors may identify bounded IDs, workspace-root categories, workspace branch, Git read-only operation name, failed invariant, or digest field. Errors do not include complete WorkPackets, complete compilation results, complete registries, unbounded Git stdout or stderr, environment values, credentials, provider responses, raw prompts, or reasoning traces.

## Digest Algorithms

| Evidence | Algorithm |
| --- | --- |
| Repository identity | `agent-platform-workspace-repository-identity-sha256-v1` |
| Allocation authorization | `agent-platform-workspace-allocation-authorization-sha256-v1` |
| Inspection evidence | `agent-platform-workspace-inspection-evidence-sha256-v1` |
| Scope projection | `agent-platform-workspace-scope-projection-sha256-v1` |
| Reservation | `agent-platform-workspace-reservation-sha256-v1` |
| Registry | `agent-platform-workspace-allocation-registry-sha256-v1` |
| Allocation input | `agent-platform-workspace-allocation-input-sha256-v1` |
| Allocation | `agent-platform-workspace-allocation-sha256-v1` |
| Allocation result | `agent-platform-workspace-allocation-result-sha256-v1` |
| Cleanup assessment | `agent-platform-workspace-cleanup-assessment-sha256-v1` |

## JSON Boundary

All public models support `model_dump`, `model_dump_json`, `model_validate`, `model_validate_json`, and `model_json_schema`. JSON arrays validate back into immutable tuples. P17.1 does not implement workspace record files, registry files, YAML serialization, Markdown rendering, database persistence, remote persistence, or Git persistence.

## Synthetic Examples

Valid allocation example:

```text
Repository pepper-agent, source commit aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa, branch p17/workspace-allocator, and workspace root C:/worktrees/pepper-p17-1 produce one allocated result from an empty registry when read-only Git inspection proves a clean linked worktree.
```

Dirty-worktree rejection example:

```text
status --porcelain=v1 -uall returning one entry rejects allocation before any registry update.
```

Wrong-commit rejection example:

```text
rev-parse HEAD returning a commit other than the repository identity source commit rejects allocation.
```

Wrong-branch rejection example:

```text
branch --show-current returning p17/other-workspace rejects allocation.
```

Primary-checkout rejection example:

```text
Equal git-dir and git-common-dir rejects the workspace as not linked.
```

Overlapping-workspace rejection example:

```text
An active reservation at C:/worktrees/pepper-p17-1 rejects C:/worktrees/pepper-p17-1/child.
```

Duplicate-WorkPacket rejection example:

```text
A registry that already reserves the WorkPacket ID rejects a second allocation request for that WorkPacket.
```

Tampered-allocation example:

```text
Changing workspace_root or allocation_SHA256 causes validate_workspace_allocation to raise WorkspaceAllocatorIntegrityError.
```

## Non-Actions

P17.1 creates no worktree, creates no directories, copies no files, writes no locks, persists no registry, grants no tools, selects no provider or model, assigns no agent or worker, executes no task, runs no validation command, reviews no diff or artifact, creates no Git handoff, mutates no WorkPacket, mutates no Git state, and claims no runtime or production readiness.

## P17.2 Handoff

P17.2 may consume `WorkPacket`, `WorkspaceAllocation`, `WorkspaceAllocationResult`, `WorkspaceScopeProjection`, `WorkspaceInspectionEvidence`, and `WorkspaceAllocationRegistry`.

P17.2 owns tool permission profile schema, tool category taxonomy, read/write/command permission projection, forbidden operation policy, workspace-root containment, repository-scope enforcement, validation-command separation, profile digest, and permission decision evidence.

P17.2 must preserve the allocated workspace root, preserve the WorkPacket scope, reject access outside the workspace, reject access outside allowed paths, retain forbidden paths, retain human-only Git authority, keep execution-ready false, and avoid running tools.

## Residual Limitations

The workspace is human-provisioned, linked-worktree posture is required, cleanliness is required, exclusivity is in-memory and caller-supplied, no durable registry exists, cleanup is assessment-only, scope enforcement is deferred, tool permissions are absent, runtime execution is absent, Git mutation remains human-controlled, Graphify output is not changed, and production readiness is not claimed.
