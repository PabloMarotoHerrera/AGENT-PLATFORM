# P17.3 - Governed Single-Agent WorkPacket Execution

P17.3 adds an externally driven execution controller for one Pepper WorkPacket. It binds one compiled P17.0 `WorkPacket`, one P17.1 human-provisioned exclusive workspace allocation, one P17.2 deny-first tool permission profile, one explicit human execution authorization, one fixed single-agent runtime binding, and one caller-supplied action plan.

The controller executes only bounded filesystem actions. It does not generate plans, render prompts, call a provider, invoke a model, run shell commands, run validation commands, invoke Git, review diffs, review artifacts, stage, commit, push, or create result/failure/cancellation envelopes.

Final verdict: hermes_0_19_pepper_single_agent_work_packet_execution_ready_with_externally_driven_permission_gated_filesystem_only_authority

## Prerequisites

P17.3 consumes these governed contracts:

| Stage | Requirement |
| --- | --- |
| P17.0 | A compile-only `WorkPacket`; `execution_ready=false`. |
| P17.1 | A clean initial human-provisioned linked worktree allocation; `exclusive=true`; Git authority remains `human_only`. |
| P17.2 | A deny-first `ToolPermissionProfile`; `tool_permissions_ready=true`; `execution_ready=false`. |

P17.3 also records fixed OpenAI Codex provider/model identity values from the accepted P15 provider-worker gate identity profile. Recording these identities is not dispatch authority. `provider_dispatch_authorized=false` and `model_inference_authorized=false` are fixed runtime-binding values.

## P17.1 Compatibility Repair

P17.3 requires clean initial allocation followed by execution-time reinspection after filesystem mutation. That later reinspection can observe a dirty linked worktree created by the controller's own completed filesystem actions.

The narrow P17.1 compatibility repair changes `WorkspaceInspectionEvidence.clean` from a literal `true` posture to a strict boolean with this invariant:

| `status_entry_count` | `clean` |
| --- | --- |
| `0` | `true` |
| positive count | `false` |

This repair does not authorize dirty allocation. `allocate_workspace` still requires `require_clean_worktree=true`, clean evidence, zero status entries, a linked worktree, matching branch, matching `HEAD`, canonical root, and unchanged repository identity. It does not mutate Git or the workspace.

## Runtime Binding

`SingleAgentRuntimeBinding` fixes:

| Field | Value |
| --- | --- |
| `provider` | `openai-codex` |
| `model_id` | `gpt-5.5` |
| `provider_runtime_profile_id` | `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1` |
| `worker_profile_id` | `worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1` |
| `externally_driven` | `true` |
| `maximum_concurrent_agents` | `1` |
| `maximum_concurrent_workers` | `1` |
| `provider_dispatch_authorized` | `false` |
| `model_inference_authorized` | `false` |

Agent and worker identifiers are explicit, bounded, non-shadow, credential-free, and distinct. The binding ID is `SAB-<NORMALIZED-TICKET-ID>-R<4-DIGIT-REVISION>-<12-LOWERCASE-HEX>`. Its digest algorithm is `agent-platform-single-agent-runtime-binding-sha256-v1`.

## Action Plan Boundary

The action source is exactly `externally_supplied_single_agent_plan`. P17.3 never infers filesystem actions from WorkPacket task text and never parses natural language into tools.

A `SingleAgentExecutionPlan` contains 1 to 64 ordered actions. Action IDs must be contiguous from `ACTION-001`. Every action references one real WorkPacket task step. Every task step must be covered, task-step coverage follows WorkPacket task order, and execution cannot return to an earlier task step after advancing.

The plan digest algorithm is `agent-platform-single-agent-execution-plan-sha256-v1`. The runner does not alter, reorder, append, remove, or infer actions.

## Human Execution Authorization

`SingleAgentExecutionAuthorization` binds the exact WorkPacket, allocation, permission profile, runtime binding, and plan digests. The authorizer is explicit and non-shadow. The authorization is declarative evidence, not authentication.

Risk acknowledgement is mandatory when the plan contains any mutating filesystem action: create file, replace file, delete file, create directory, or delete directory. Authorization does not permit provider/model dispatch, commands, validation commands, Git, staging, commit, push, or review.

## Filesystem Operations

P17.3 supports exactly seven operations:

| Operation | Semantics |
| --- | --- |
| `list_directory` | Existing non-symlink directory; immediate sorted entries only; max 512 entries; no recursion. |
| `read_file` | Existing non-symlink regular UTF-8 file; max 262144 bytes; transient text observation. |
| `create_file` | Absent target; existing non-symlink parent directory; exclusive create; bounded UTF-8 content. |
| `replace_file` | Existing non-symlink regular UTF-8 file; expected SHA-256 must match; no upsert. |
| `delete_file` | Existing non-symlink regular UTF-8 file; expected SHA-256 must match; no directory deletion. |
| `create_directory` | Absent target; existing non-symlink parent directory; creates exactly one directory. |
| `delete_directory` | Existing non-symlink empty directory; no recursive deletion. |

Unsupported operations include command execution, validation commands, Git read or mutation, network access, workspace mutation outside these adapters, provider calls, model calls, agent control, worker control, chmod, chown, ACL mutation, symlink creation, hard-link creation, mount operations, recursive copy, recursive delete, and binary-file editing.

## Workspace Reinspection

`prepare_single_agent_execution` validates all bindings, validates nested digests, and reinspects the workspace with `require_clean_worktree=true` and `require_linked_worktree=true`.

Before each action, `execute_single_agent_tool_action` reinspects with `require_clean_worktree=false` and `require_linked_worktree=true`. Clean or dirty reinspection evidence is accepted only when the root, resolved root, Git top level, branch, `HEAD`, inside-worktree posture, and linked-worktree posture still match the allocation. Dirty state alone is not an execution error after previous governed filesystem actions.

P17.3 does not call Git directly. It inherits P17.1 read-only workspace inspection only.

## Target Resolution

Each action target is a serialized repository-relative path. P17.3 rejects absolute paths, Windows drive-relative paths, backslashes, parent traversal, empty components, `.`, `..`, workspace-root targets, protected roots, symlink parents, symlink targets, and resolved targets outside the allocated root.

Target resolution records `SingleAgentTargetResolutionEvidence` with candidate and resolved target paths, target kind, existence, parent existence, under-workspace posture, symlink safety, optional preexisting file SHA-256, and digest. The digest algorithm is `agent-platform-single-agent-target-resolution-sha256-v1`.

Kernel-level race-free path resolution is not claimed across every platform. The controller minimizes time-of-check/time-of-use exposure by resolving and rechecking target preconditions immediately before the filesystem adapter runs.

## Permission Evaluation

For every non-cancelled action, the ordering is:

1. physical target resolution;
2. P17.2 `ToolPermissionCheckRequest` construction;
3. `evaluate_tool_permission`;
4. `validate_tool_permission_decision`;
5. immediate target recheck;
6. one filesystem adapter invocation.

Denied decisions block the session without executing a filesystem adapter, without mutating the target, and without automatic privilege escalation. Executed actions require one matching allow decision.

## Observations And Evidence

`SingleAgentToolObservation` is transient caller-facing output. Mutations return `none`, reads return bounded text, and directory listing returns bounded names. Observations are not copied into `SingleAgentExecutionSession` or `SingleAgentExecutionResult`; the session stores only observation digests.

`SingleAgentActionEvidence` records action ID, task step, operation, disposition, permission decision, target resolution digest, post-action target kind, post-action SHA-256, execution flag, mutation flag, rollback flag, observation digest, and evidence digest. It never stores raw file contents or directory listing contents.

## Rollback

P17.3 provides current-action rollback when an error occurs after a filesystem mutation but before valid action evidence is returned:

| Operation | Rollback |
| --- | --- |
| `create_file` | Remove the new file when safe. |
| `replace_file` | Restore original bytes when safe. |
| `delete_file` | Restore original bytes when safe. |
| `create_directory` | Remove the new empty directory when safe. |
| `delete_directory` | Recreate the removed empty directory when safe. |

Cross-action rollback is absent. Original bytes are held only transiently in memory and are not embedded in models, logs, exceptions, or digest evidence.

## Session State And Progression

`SingleAgentExecutionSession` is immutable and caller-supplied on every transition. There is no process-global session registry.

| State | Meaning |
| --- | --- |
| `prepared` | Bindings validated, initial workspace clean, next action index `0`, execution active. |
| `active` | At least one action may have executed; execution remains active. |
| `blocked` | Permission denial or state blocker; execution inactive. |
| `cancelled` | Cancellation observed before target resolution; execution inactive. |
| `completed` | Completion evidence produced; execution inactive; only single-agent requirement satisfied. |

Task completion is deterministic but limited: a task step is marked complete only after all externally supplied actions for that task step have executed successfully. The controller does not prove the semantic truth of natural-language task completion beyond the explicit action plan.

## Completion Result

`complete_single_agent_execution` produces `SingleAgentExecutionResult` only for a fully executed active session. The result records completed action count, completed task IDs, touched paths, read paths, created paths, replaced paths, deleted paths, and downstream readiness flags.

Canonical completion posture:

| Capability | P17.3 status |
| --- | --- |
| Single-agent execution requirement | satisfied |
| Validation command runner | deferred to P17.4 |
| Result/failure/cancellation envelopes | deferred to P17.5 |
| Diff and artifact review | deferred to P17.6 |
| Human Git handoff | deferred to P17.7 |
| Provider dispatch | absent |
| Model inference | absent |
| Git mutation | absent |

The final result contains no raw file content, directory listing content, credentials, provider responses, prompts, reasoning traces, Git output, rollback bytes, result envelope, diff review, artifact review, staging evidence, commit evidence, or push evidence.

## Digest Algorithms

| Evidence | Algorithm |
| --- | --- |
| Runtime binding | `agent-platform-single-agent-runtime-binding-sha256-v1` |
| Tool action | `agent-platform-single-agent-tool-action-sha256-v1` |
| Execution plan | `agent-platform-single-agent-execution-plan-sha256-v1` |
| Execution authorization | `agent-platform-single-agent-execution-authorization-sha256-v1` |
| Target resolution | `agent-platform-single-agent-target-resolution-sha256-v1` |
| Tool observation | `agent-platform-single-agent-tool-observation-sha256-v1` |
| Action evidence | `agent-platform-single-agent-action-evidence-sha256-v1` |
| Session | `agent-platform-single-agent-execution-session-sha256-v1` |
| Action result | `agent-platform-single-agent-action-result-sha256-v1` |
| Execution result | `agent-platform-single-agent-execution-result-sha256-v1` |

Digests are deterministic integrity evidence, not signatures.

## Public Exceptions And JSON Boundary

Public exceptions are `SingleAgentExecutionError`, `SingleAgentExecutionInputError`, `SingleAgentExecutionAuthorizationError`, `SingleAgentExecutionIntegrityError`, `SingleAgentTargetResolutionError`, `SingleAgentToolExecutionError`, and `SingleAgentExecutionStateError`. Errors expose bounded invariant identifiers only.

All public models are immutable Pydantic models with forbidden extra fields and JSON round-trip support through `model_dump`, `model_dump_json`, `model_validate`, `model_validate_json`, and `model_json_schema`. P17.3 does not define YAML support, database persistence, session-file persistence, provider payload storage, credential storage, or filesystem handle serialization.

## Residual Limitations

The action plan remains externally supplied. Provider/model identity is recorded but not dispatched. Commands are absent. Validation commands are deferred. Failure and cancellation envelopes are deferred. Diff and artifact review are deferred. Human Git handoff is deferred. Cross-action rollback is absent. Semantic task-completion verification is absent. Production readiness is not claimed.
