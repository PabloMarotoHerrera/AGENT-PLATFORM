# Pepper P17.1 WorkPacket Workspace Allocator Governance Record

## Decision

P17.1 adds a human-provisioned workspace allocator for Pepper WorkPackets. The allocator validates one existing linked Git worktree, binds it to one immutable P17.0 `WorkPacket`, and returns immutable allocation evidence plus an updated caller-supplied in-memory registry.

P17.1 is not runtime readiness. It authorizes no worktree creation, Git mutation, tool permission profile, provider or model selection, agent or worker assignment, validation command execution, result envelope creation, diff or artifact review, filesystem persistence, durable lease, cleanup action, Docker command or Graphify command.

The P17.1 verdict is declared only in the final block.

## Authority

| Field | Value |
| --- | --- |
| Ticket | `P17.1` |
| Branch | `p17-governed-workpacket-execution-mvp` |
| HEAD at validation | `de525c0943c7f1f500dfca5972b28c127502f880` |
| Remote P17 branch at validation | `de525c0943c7f1f500dfca5972b28c127502f880` |
| Main / origin main at validation | `92d1e790e70176ed542b1ae44d6e8af771be512b` |
| Required P17.0 commit | `de525c0943c7f1f500dfca5972b28c127502f880` |
| Required P17.0 message | `P17.0 Add TicketSpec to WorkPacket compiler` |
| Required P17.0 closure record | `0_architecture/governance/agent_platform_pepper_ticket_spec_to_work_packet_compiler.md` |
| Registered worktrees | `1` |
| Canonical product root | `2_products/pepper-agent` |
| Legacy Hermes product root present | false |
| Omniverse tracked files | `369` under `2_products/omniverse-app` |

Authorized P17.1 candidate paths:

| Path | Role |
| --- | --- |
| `0_architecture/governance/agent_platform_pepper_work_packet_workspace_allocator.md` | Human-readable P17.1 governance record only. |
| `2_products/pepper-agent/docs/agent-platform/work_packet_workspace_allocator.md` | Product documentation for the human-provisioned allocator contract. |
| `2_products/pepper-agent/hermes_cli/agent_platform/work_packet/__init__.py` | Public WorkPacket export boundary, preserving the P17.0 export prefix. |
| `2_products/pepper-agent/hermes_cli/agent_platform/work_packet/workspace_allocator.py` | Immutable contracts and deterministic workspace allocation implementation. |
| `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_work_packet_compiler.py` | P17.0 regression suite updated only for additive export compatibility. |
| `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_work_packet_workspace_allocator.py` | Focused P17.1 behavior and authority test suite. |
| `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | Product-local import manifest rows for P17.1 additions and updated destinations. |
| `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` | Product-local modification register rows for P17.1 additions and updated destinations. |

## Pre-Change Pepper Identity

The authoritative pre-change Pepper identity is the committed P17.0 Git tree at `de525c0943c7f1f500dfca5972b28c127502f880`.

| Projection | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate excluding baseline record | `6863` | `150981136` | `110b22ff1e1cbdf995647d71bf66a4726ea64a5fd4281011d23193cdc309af3d` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

## Product Contract

P17.1 adds the `hermes_cli.agent_platform.work_packet.workspace_allocator` module and exactly thirty-one additive public package exports. The first twenty-five P17.0 package exports remain an exact prefix, so P17.0 callers keep the same import surface.

The allocator binds these inputs:

| Input | Required Binding |
| --- | --- |
| `WorkPacketCompilationResult` | Must be compiled, validated, compile-only, execution-not-ready, human-only Git authority, and still require `workspace_allocation`. |
| `WorkspaceRepositoryIdentity` | Repository ID, 40-character source commit, named workspace branch, and repository identity digest. |
| `WorkspaceAllocationAuthorization` | Human authorization binding WorkPacket ID, WorkPacket SHA-256, repository identity SHA-256, workspace root, workspace kind and human-only Git authority. |
| `WorkspaceAllocationRegistry` | Caller-supplied immutable in-memory registry with revision and reservation digest. |
| Human-provisioned linked worktree | Existing clean linked Git worktree whose top-level, branch and `HEAD` match the requested identity. |

Shadow-only authorizers are rejected. Authorizer identifiers beginning with `SHADOW-` cannot authorize workspace allocation.

## Authority Boundary

P17.1 reserves data only. Allocations record `workspace_requirement_satisfied=true`, `execution_ready=false`, `tool_permissions_ready=false`, `git_authority=human_only`, `isolation_level=dedicated`, `exclusive=true` and `cleanup_eligibility=not_eligible`.

The allocator does not create worktrees, create directories, copy files, write locks, persist registries, mutate WorkPackets, grant tools, select providers, select models, assign workers, assign agents, run task commands, run validation commands, create result envelopes, review diffs or artifacts, remove worktrees, mutate Git, call network APIs, run Graphify or run Docker.

P17.1 uses exactly seven bounded read-only Git inspection command shapes. Each uses `git --no-optional-locks`, `shell=False`, captured output, UTF-8 text decoding and a fixed five-second timeout:

| Git Shape |
| --- |
| `rev-parse --show-toplevel` |
| `rev-parse HEAD` |
| `branch --show-current` |
| `rev-parse --is-inside-work-tree` |
| `rev-parse --git-dir` |
| `rev-parse --git-common-dir` |
| `status --porcelain=v1 -uall` |

P17.1 invokes no Git mutation or remote command shapes.

## Workspace Rules

The supplied workspace root must be absolute, serialized with forward slashes, non-symlink, existing, a directory, equal to the Git top-level after resolution, and outside protected components such as `.git`, `.opencode`, `graphify-out`, `4_external/sources`, and the Pepper upstream baseline file.

Linked-worktree verification uses the relationship between `--git-dir` and `--git-common-dir`. A primary checkout is rejected because its Git directory and common Git directory are the same. A dirty worktree is rejected when `status --porcelain=v1 -uall` returns any entry.

The registry is in memory only. Registry validation rejects duplicate allocation IDs, duplicate WorkPacket IDs, duplicate workspace roots, duplicate resolved workspace roots, duplicate workspace branches, and overlapping roots where one root is equal to, an ancestor of, or a descendant of another.

## Determinism And Digests

All P17.1 identities are deterministic SHA-256 records over canonical JSON with sorted keys and compact separators. The allocation ID is derived from ticket ID, registry revision and the first twelve hex characters of the allocation-input digest. The allocator uses no clock, UUID, random value, process-global mutable allocator state or persisted counter.

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

## Downstream Handoff

P17.1 satisfies only the P17.0 downstream requirement `workspace_allocation`. All other P17.0 downstream requirements remain unsatisfied.

| Capability | Owner | P17.1 Status |
| --- | --- | --- |
| `workspace_allocation` | `P17.1` | Satisfied by a human-provisioned exclusive allocation. |
| `tool_permission_profile` | `P17.2` | Not satisfied. |
| `single_agent_execution` | `P17.3` | Not satisfied. |
| `validation_command_runner` | `P17.4` | Not satisfied. |
| `result_failure_cancellation_envelopes` | `P17.5` | Not satisfied. |
| `diff_artifact_review` | `P17.6` | Not satisfied. |
| `human_git_handoff` | `P17.7` | Not satisfied. |

P17.2 may consume `WorkPacket`, `WorkspaceAllocation`, `WorkspaceAllocationResult`, `WorkspaceScopeProjection`, `WorkspaceInspectionEvidence` and `WorkspaceAllocationRegistry`, but must retain execution-not-ready posture and avoid running tools.

## Register And Manifest

| Check | Result |
| --- | --- |
| `AGENT_PLATFORM_MODIFICATIONS.tsv` data rows | `185` |
| `AGENT_PLATFORM_MODIFICATIONS.tsv` width | `18` |
| `AGENT_PLATFORM_MODIFICATIONS.tsv` malformed rows | `0` |
| `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` data rows | `6839` |
| `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` width | `8` |
| `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` malformed rows | `0` |
| New P17.1 modification rows | `3` |
| Existing modification rows updated for P17.1 | `2` |
| New P17.1 manifest rows | `3` |
| Existing manifest rows updated for P17.1 | `2` |
| Duplicate modification IDs | `0` |
| Duplicate modification paths | `0` |
| Duplicate concrete manifest destinations | `0` |
| Missing destination paths | `0` |
| Destination hash mismatches | `0` |
| P17.1 rows included in upstream payload | false |

P17.1 product destination inventory:

| Modification ID | Product path | Current product SHA-256 |
| --- | --- | --- |
| `P17.0-001` | `hermes_cli/agent_platform/work_packet/__init__.py` | `5d53f3b48d4555d30e72caf48baebfd249b8d3e84517ae6313fc1b9840f7327c` |
| `P17.0-003` | `tests/hermes_cli/test_agent_platform_work_packet_compiler.py` | `eeec02109253057e520e0714987a355990fbd2302c7543845cfcaf01a70be2eb` |
| `P17.1-001` | `hermes_cli/agent_platform/work_packet/workspace_allocator.py` | `394848bc76acab1635a591e6e467e0fdd3d203e18ddacb2adcb04c5e632ad1ec` |
| `P17.1-002` | `tests/hermes_cli/test_agent_platform_work_packet_workspace_allocator.py` | `37be534e992bd2a7b4a8dc1155e146198851fd24bcb30381089ab9b62c7bbbde` |
| `P17.1-003` | `docs/agent-platform/work_packet_workspace_allocator.md` | `d59213bff82218726bb51b8a64fac5fba5c49410d9a06e8f556b4ed087dd7066` |

## Public API Closure

| Check | Result |
| --- | --- |
| Declared package exports | `56` |
| Unique declared package exports | `56` |
| P17.0 first twenty-five exports preserved as exact prefix | true |
| Declared exports resolve on package root | true |
| Hidden names exported | false |
| `WorkspaceCreation` exported | false |
| `WorkspaceExecution` exported | false |
| `WorkspaceToolProfile` exported | false |

The public root contains the expected P17.1 entry points: `build_workspace_repository_identity`, `build_workspace_allocation_authorization`, `get_empty_workspace_allocation_registry`, `inspect_human_provisioned_workspace`, `allocate_workspace`, `validate_workspace_allocation`, `validate_workspace_allocation_registry` and `assess_workspace_cleanup_eligibility`.

## Runtime Authority Closure

Scoped authority scan covered `hermes_cli/agent_platform/work_packet/__init__.py` and `hermes_cli/agent_platform/work_packet/workspace_allocator.py`.

| Check | Result |
| --- | ---: |
| Forbidden imports | `0` |
| Filesystem metadata reads | `4` |
| Repository file content reads | `0` |
| Filesystem writes | `0` |
| Directory creations | `0` |
| Directory deletions | `0` |
| File copies | `0` |
| Network calls | `0` |
| Provider calls | `0` |
| Model calls | `0` |
| Agent calls | `0` |
| Worker calls | `0` |
| Tool calls | `0` |
| Validation command executions | `0` |
| Runtime ticket executions | `0` |
| Git read-only command shapes | `7` |
| Git mutation command shapes | `0` |
| Git remote command shapes | `0` |
| `shell=True` calls | `0` |
| Workspace creations | `0` |
| Worktree creations | `0` |
| Persistent registry writes | `0` |
| Automatic cleanup actions | `0` |
| Input mutations | `0` |

The nonzero filesystem metadata reads are limited to `Path.exists`, `Path.is_dir`, `Path.is_symlink` and `Path.resolve` for the supplied workspace root. They are not repository content reads or writes.

## Post-Change Pepper Identity

P17.1 adds three product files and modifies four product files. The upstream payload and baseline record remain unchanged.

| Projection | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate excluding baseline record | `6866` | `151101743` | `14de42b9e808b7bf93ab8ff79024bd3df268e8c032640d8f884149f40718914b` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

## Validation Evidence

| Command Or Check | Result |
| --- | --- |
| `git branch --show-current` | `p17-governed-workpacket-execution-mvp` |
| `git rev-parse HEAD` | `de525c0943c7f1f500dfca5972b28c127502f880` |
| `git rev-parse origin/p17-governed-workpacket-execution-mvp` | `de525c0943c7f1f500dfca5972b28c127502f880` |
| `git rev-parse main` | `92d1e790e70176ed542b1ae44d6e8af771be512b` |
| `git rev-parse origin/main` | `92d1e790e70176ed542b1ae44d6e8af771be512b` |
| `%USERPROFILE%\anaconda3\python.exe -m pytest -q tests/hermes_cli/test_agent_platform_work_packet_workspace_allocator.py -p no:cacheprovider` | `274 passed in 5.48s` |
| `%USERPROFILE%\anaconda3\python.exe -m pytest -q tests/hermes_cli/test_agent_platform_work_packet_compiler.py -p no:cacheprovider` | `237 passed in 4.19s` |
| P17.0 plus P17.1 combined focused suite | `511 passed in 8.78s` |
| Full P16 plus P17 suite | `2015 tests passed` |
| `%USERPROFILE%\anaconda3\python.exe -m ruff check hermes_cli/agent_platform/work_packet tests/hermes_cli/test_agent_platform_work_packet_compiler.py tests/hermes_cli/test_agent_platform_work_packet_workspace_allocator.py` | `All checks passed!` |
| `%USERPROFILE%\anaconda3\python.exe -m ruff format --check hermes_cli/agent_platform/work_packet tests/hermes_cli/test_agent_platform_work_packet_compiler.py tests/hermes_cli/test_agent_platform_work_packet_workspace_allocator.py` | `5 files already formatted` |
| WorkPacket import/export smoke | `56 56 True False False False` |
| Workspace allocator function smoke | `build_workspace_repository_identity build_workspace_allocation_authorization get_empty_workspace_allocation_registry inspect_human_provisioned_workspace allocate_workspace validate_workspace_allocation assess_workspace_cleanup_eligibility` |
| P17.0 shadow rejection smoke | `WorkPacketCompilerAuthorizationError shadow-only approval evidence cannot authorize WorkPacket compilation` |
| Deterministic allocation smoke | `same_input_same_result: true` |
| Deterministic allocation ID | `WS-P17-0-R0001-df6d538eaf9e` |
| Deterministic allocation input SHA-256 | `df6d538eaf9ea0ef53bc30aeec17bc408a77835c0e0e1858689a4554a8ed5403` |
| Deterministic allocation SHA-256 | `1f144cc9400006200dd75cd8ba9507f3dd26c83c2e59fc65d5e3282ae13dc805` |
| Deterministic allocation result SHA-256 | `1d8e3f5937580c8e1cdcd104a45a9f379ef00c0da45f3f4e274031946428ac47` |
| Primary-checkout rejection smoke | `WorkspaceAllocatorInspectionError workspace must be a human-provisioned linked Git worktree` |
| `%USERPROFILE%\anaconda3\python.exe -m unittest 12_tests/governance/test_pepper_baseline_integrity.py` | `Ran 14 tests in 0.003s`; `OK` |
| `ty` type checker | unavailable; dependency installation intentionally not performed |

## Non-Actions

P17.1 performed no staging, commit, push, branch switch, merge, rebase, reset, clean, stash, worktree creation, dependency installation, lockfile update, Docker command or Graphify command.

Graphify remains intentionally not run under the explicit P17.1 constraint.

## Final Verdict

hermes_0_19_pepper_work_packet_workspace_allocator_ready_with_human_provisioned_exclusive_non_executing_authority
