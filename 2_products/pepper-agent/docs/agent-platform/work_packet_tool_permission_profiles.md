# WorkPacket Tool Permission Profiles

P17.2 adds deterministic, deny-first tool permission profiles for Pepper WorkPackets. A profile binds one compiled P17.0 `WorkPacket`, one verified P17.1 `WorkspaceAllocation`, and one explicit human authorization for selected filesystem operations.

P17.2 is policy only. It creates immutable permission evidence and a pure evaluator. It does not invoke tools, inspect files, resolve symlinks, run commands, call Git, contact providers or models, assign agents or workers, review diffs or artifacts, create result envelopes, or claim runtime readiness.

## Prerequisites

P17.0 must provide a compiled WorkPacket with `execution_ready=false`, `git_authority=human_only`, and an unsatisfied `tool_permission_profile` downstream requirement.

P17.1 must provide an allocated, exclusive workspace allocation with `workspace_requirement_satisfied=true`, `execution_ready=false`, and `tool_permissions_ready=false`.

Allocation alone is insufficient. A workspace allocation only proves that a clean human-provisioned linked worktree has been reserved. P17.2 separately decides which tool operations may be attempted later inside that workspace.

## Human Authorization

`ToolPermissionProfileAuthorization` is explicit human evidence authorizing issuance of one bounded profile. It binds the WorkPacket ID and SHA-256, allocation ID and SHA-256, and nonempty grant requests.

The authorizer must not begin with `SHADOW-`. `profile_authorized` is fixed true, `synthetic` is fixed false, and the authorization digest is deterministic.

Mutating filesystem operations require non-null `risk_acknowledgement`:

| Operation | Risk Acknowledgement |
| --- | --- |
| `create_file` | Required |
| `replace_file` | Required |
| `delete_file` | Required |
| `create_directory` | Required |
| `delete_directory` | Required |

Read-only grants do not require risk acknowledgement.

## Operation Taxonomy

Grantable P17.2 operations are exactly seven filesystem operations:

| Operation | Meaning |
| --- | --- |
| `list_directory` | Permit a future tool adapter to list a directory after P17.3 target resolution. |
| `read_file` | Permit a future tool adapter to read a file after P17.3 target resolution. |
| `create_file` | Permit a future tool adapter to create a file after P17.3 target resolution. |
| `replace_file` | Permit a future tool adapter to replace a file after P17.3 target resolution. |
| `delete_file` | Permit a future tool adapter to delete a file after P17.3 target resolution. |
| `create_directory` | Permit a future tool adapter to create a directory after P17.3 target resolution. |
| `delete_directory` | Permit a future tool adapter to delete a directory after P17.3 target resolution. |

Never-grantable P17.2 operations are exactly ten:

```text
execute_command
validation_command
network_access
workspace_mutation
provider_call
model_call
agent_control
worker_control
```

These operations are always denied by the profile and evaluator.

## Grant Requests

`ToolPermissionGrantRequest` contains:

| Field | Requirement |
| --- | --- |
| `operation` | One of the seven grantable filesystem operations. |
| `source_allowed_action` | Exact member of the WorkPacket `allowed_actions`. |
| `rationale` | Bounded nonempty human rationale. |

Duplicate requested operations fail. References absent from `allowed_actions` fail. References also present in `forbidden_actions` fail. Never-grantable operations fail.

The builder normalizes grant request order to `ToolPermissionOperation` enum order.

## Scope Preservation

Every grant copies the P17.1 `WorkspaceScopeProjection` exactly:

| Grant Field | Source |
| --- | --- |
| `allowed_paths` | Exact WorkPacket allowed paths, order preserved. |
| `forbidden_paths` | Exact WorkPacket forbidden paths, order preserved. |

P17.2 does not expand, reduce, reorder, rewrite, infer, or enforce additional scope. Unsupported path grammar fails closed.

Supported WorkPacket path patterns are:

```text
exact repository-relative paths
subtree patterns ending in /**
```

Unsupported examples rejected by P17.2:

```text
foo/*/bar
foo/?.py
foo/[ab].py
**/file.py
```

Matching uses forward slashes and exact serialized case. Exact patterns match only the exact path. Subtree patterns match the directory itself or any descendant.

## Protected Paths

Profiles include the canonical protected paths tuple:

```text
.git/**
.opencode/**
.agents/**
AGENTS.md
4_external/sources/**
2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json
```

Protected paths always deny. Callers cannot override them, and grants cannot override them.

Forbidden WorkPacket paths also override every grant. Evaluation precedence is protected path first, then forbidden WorkPacket path, then operation grant, then allowed path.

## Profile Shape

`ToolPermissionProfile` records:

| Field | Posture |
| --- | --- |
| `state` | `issued` |
| `tool_permissions_ready` | true |
| `execution_ready` | false |
| `git_authority` | `human_only` |
| `grants` | Enum-ordered explicit filesystem grants. |
| `denied_operations` | Exact complement of granted operations across all operation enum members. |
| `protected_paths` | Exact canonical protected tuple. |

Profile ID shape:

```text
TP-<NORMALIZED-TICKET-ID>-R<4-DIGIT-REVISION>-<12-LOWERCASE-HEX>
```

The suffix is the first twelve characters of `profile_input_SHA256`. The builder uses no clock, UUID, random value, environment state, filesystem state, Git state, or process-global mutable registry.

Digest algorithms:

| Evidence | Algorithm |
| --- | --- |
| Authorization | `agent-platform-tool-permission-profile-authorization-sha256-v1` |
| Grant | `agent-platform-tool-permission-grant-sha256-v1` |
| Profile input | `agent-platform-tool-permission-profile-input-sha256-v1` |
| Profile | `agent-platform-tool-permission-profile-sha256-v1` |
| Profile result | `agent-platform-tool-permission-profile-result-sha256-v1` |
| Decision input | `agent-platform-tool-permission-decision-input-sha256-v1` |
| Decision | `agent-platform-tool-permission-decision-sha256-v1` |

## Permission Checks

`ToolPermissionCheckRequest` binds a profile, allocation, operation, workspace-relative path, resolved target path, and request reference.

`target_resolution_verified=true` is a future P17.3 adapter assertion. P17.2 does not physically resolve targets or establish symlink safety. It only checks the supplied strings against the profile and allocation bindings.

The pure evaluator performs these gates:

1. validate profile and allocation integrity;
2. validate profile-to-allocation binding;
3. reject invalid relative or absolute path syntax;
4. require resolved target to equal workspace root joined with the relative path;
5. require target under the resolved workspace root;
6. deny protected paths;
7. deny forbidden WorkPacket paths;
8. deny ungranted or never-grantable operations;
9. require allowed WorkPacket path match;
10. allow only when every gate passes.

Normal denials return `ToolPermissionDecisionEvidence`. Structural binding failures raise `ToolPermissionEvaluationError`.

Allow evidence uses:

```text
decision=allow
reason=allowed_by_explicit_grant
```

Deny reasons are:

```text
operation_not_granted
operation_explicitly_denied
```

Decision evidence contains no file contents, directory contents, command output, tool output, provider output, credentials, raw prompts, or reasoning traces.

## Synthetic Examples

Valid synthetic profile:

```text
WorkPacket WP-P17-0-R0001-faf01b3d1f0f and allocation WS-P17-0-R0001-df6d538eaf9e are bound to a human authorization for read_file and replace_file. The profile is issued, tool-permissions-ready, execution-not-ready, human-only Git authority, and deny-first for every ungranted operation.
```

Read-file allow:

```text
read_file on 2_products/pepper-agent/hermes_cli/agent_platform/work_packet/tool_permissions.py is allowed only when the operation is granted, the resolved target equals the allocated workspace root plus that relative path, and the path matches the WorkPacket allowed scope.
```

Command denial:

```text
execute_command is denied with operation_explicitly_denied even when the target path is otherwise in allowed scope.
```

Protected-path denial:

```text
read_file on .git/config is denied with target_in_protected_root.
```

Forbidden-path denial:

```text
read_file on a WorkPacket forbidden path is denied with target_in_forbidden_scope.
```

Outside-workspace denial:

```text
read_file is denied with target_outside_workspace when the supplied resolved target does not equal the allocated workspace root joined with the relative path.
```

Ungranted-delete denial:

```text
delete_file is denied with operation_not_granted when the profile grants read_file only.
```

Tampered-profile example:

```text
Changing profile_input_SHA256, profile_SHA256, a grant digest, denied_operations or protected_paths causes validation to fail. P17.2 does not repair the profile.
```

## JSON Boundary

All public models support `model_dump`, `model_dump_json`, `model_validate`, `model_validate_json`, and `model_json_schema`. JSON arrays validate back into immutable tuples.

P17.2 does not implement profile file serialization, decision log persistence, YAML serialization, Markdown rendering, database persistence, remote persistence, or Git persistence.

## Non-Actions

P17.2 performs no tool invocation, filesystem inspection, filesystem mutation, directory mutation, command execution, validation command execution, Git access, network access, provider call, model call, agent assignment, worker assignment, workspace allocation, workspace removal, result envelope creation, diff review, artifact review, Git handoff, staging, commit, push, merge, or production-readiness claim.

## P17.3 Handoff

P17.3 may consume `ToolPermissionProfile`, `ToolPermissionProfileResult`, `ToolPermissionCheckRequest`, `ToolPermissionDecisionEvidence`, and `evaluate_tool_permission`.

P17.3 owns physical target resolution, symlink-safe target resolution, tool adapter invocation, provider and model binding, agent and worker identity binding, execution lifecycle, per-tool decision capture, cancellation observation, and task-step progression.

P17.3 must call `evaluate_tool_permission` before every tool action. P17.3 must keep command execution, validation command execution, Git access, network access, provider calls, model calls, workspace mutation, staging, commit, and push outside the P17.2 profile authority unless a later governed ticket explicitly authorizes them.

## Residual Limitations

P17.2 is deterministic policy evidence only. Runtime target resolution is deferred to P17.3. Symlink safety is deferred to P17.3. Tool execution is absent. Agent and worker assignment are absent. Result, failure and cancellation envelopes are deferred to P17.5. Diff and artifact review are deferred to P17.6. Human Git handoff is deferred to P17.7. Production readiness is not claimed.
