# 01AH - Governed WorkPacket Autonomy

01AH adds a governed task-local autonomy layer for Pepper workers. It lets a worker classify a missing non-privileged capability, create a task-local helper inside the already-approved WorkPacket scope, evaluate a bounded command for that helper, run it with `shell=false`, and continue with immutable lineage evidence.

Final verdict: `READY_FOR_GOVERNED_AUTONOMY_ACTIVATION`

## Boundary

01AH preserves the rule `CAPABILITY != AUTHORITY`.

The autonomy envelope binds one compiled `WorkPacket`, one allocated workspace, one deny-first tool permission profile, and one completed single-agent execution result. The envelope records `live_lineage_activation_authorized=false`; repository support is ready, but live failed-run recovery still requires explicit human activation.

01AH does not approve tickets, mutate Kanban state, dispatch providers or models, call Git, stage, commit, push, run Docker, run Graphify, install packages, acquire credentials, change WorkPacket scope, or bypass Human Git Handoff.

## Reuse Matrix

| Component | Disposition | 01AH Use |
| --- | --- | --- |
| `workpacket.file_guard` | `HERMES_REUSED` | Reuses governed WorkPacket file confinement, including `node_modules/**` and `package-lock.json` protection. |
| `workpacket.tool_permissions` | `HERMES_REUSED` | Reuses deny-first filesystem grants and pure permission decisions before helper materialization or helper input reads. |
| `workpacket.workspace_allocation` | `HERMES_REUSED` | Reuses the existing allocated workspace binding; 01AH creates no workspace allocator. |
| `workpacket.single_agent_result` | `HERMES_REUSED` | Requires completed single-agent execution evidence before autonomy can continue. |
| `validation_command.subprocess_pattern` | `HERMES_ADAPTED` | Adapts bounded, shell-free subprocess capture for task-local helper commands instead of exact human-authorized validation commands. |
| Hermes global dynamic surfaces | `HERMES_ADAPTED` | Assesses registry, plugin, skill, MCP, and code-execution surfaces but does not expose them to Pepper workers. |
| Pepper autonomy envelope and lineage | `PEPPER_NEW` | Adds Pepper-specific gap, contract, candidate, command, materialization, and continuation evidence. |

## Positive Path

1. `build_governed_autonomy_envelope` validates and binds WorkPacket, workspace, profile, and completed single-agent evidence.
2. `classify_capability_gap` distinguishes repairable task-local gaps from authority-required requests.
3. `build_task_local_capability_contract` fixes the helper language, implementation path, WorkPacket path scope, and explicit non-authority booleans.
4. `build_tool_candidate` records bounded source and rejects dependency requests or secret-shaped text.
5. `materialize_task_local_tool` writes the helper only after file-guard and tool-permission approval.
6. `propose_autonomy_command` and `evaluate_autonomy_command` convert a source command into bounded argv or deterministic denial.
7. `execute_autonomy_command` launches only an allowed helper command with `shell=false`, disabled stdin, bounded streams, redacted retained output, and zero provider/model counts.
8. `advance_governed_autonomy_continuation` records progress, budget use, no-progress posture, and authority revalidation.

## Denied By Default

These requests produce human-authority-required gaps or denied command evaluations:

```text
git status
python -m pip install pytest
curl https://example.invalid/data.json
Authorization: Bearer <token>
```

TypeScript helpers can be materialized as task-local artifacts, but 01AH does not add a TypeScript runtime bridge, `tsx`, `ts-node`, `npx`, or package-install authority. Frontend fixtures are supported through existing WorkPacket path scope and bounded helper validation.

## Continuation Controls

`AutonomyContinuationLineage` carries immutable counters for repair attempts, candidates, command evaluations, successful commands, no-progress iterations, and continuation count. A continuation blocks on budget exhaustion, no-progress exhaustion, command failure, terminal lineage replay, or envelope mismatch.

Authority is revalidated on every continuation by checking the envelope digest and nested allocation/profile evidence. A worker cannot carry a continuation across WorkPacket IDs, profile digests, allocation digests, or tampered WorkPacket SHA-256 values.

## Verification

The focused 01AH suite covers:

- public export contract appended after P17.R;
- immutable JSON-round-trippable public models;
- exact `HERMES_REUSED`, `HERMES_ADAPTED`, and `PEPPER_NEW` reuse matrix;
- Python self-repair helper materialization, validation command execution, and continuation;
- frontend-path fixture validation inside WorkPacket scope;
- Git, credential, network, package install, Docker, and Graphify denial;
- file-guard protection for `node_modules`, `package-lock.json`, and `graphify-out`;
- no-progress, budget exhaustion, and authority-envelope tamper rejection.
