# Pepper P17.0 TicketSpec To WorkPacket Compiler Governance Record

## Decision

P17.0 adds a compile-only, deterministic, in-memory WorkPacket compiler for Pepper. The compiler accepts explicitly authorized, approved and logically published P16 TicketSpec evidence and returns immutable WorkPacket contracts for later P17 execution stages.

P17.0 is not runtime readiness. It authorizes no workspace allocation, tool profile resolution, provider or model selection, agent or worker assignment, validation command execution, result envelope creation, diff or artifact review, filesystem persistence, Git mutation, Docker command or Graphify command.

The P17.0 verdict is declared only in the final block.

## Authority

| Field | Value |
| --- | --- |
| Ticket | `P17.0` |
| Branch | `p17-governed-workpacket-execution-mvp` |
| HEAD at validation | `92d1e790e70176ed542b1ae44d6e8af771be512b` |
| Main / origin main at validation | `92d1e790e70176ed542b1ae44d6e8af771be512b` |
| Required P16.R commit | `92d1e790e70176ed542b1ae44d6e8af771be512b` |
| Required P16.R message | `P16.R Close Ticket Factory and parallel planning` |
| Required P16.R closure record | `0_architecture/governance/agent_platform_pepper_ticket_factory_closure.md` |
| Registered worktrees | `1` |
| Canonical product root | `2_products/pepper-agent` |
| Legacy Hermes product root present | false |
| Omniverse tracked files | `369` |

Authorized P17.0 candidate paths:

| Path | Role |
| --- | --- |
| `0_architecture/governance/agent_platform_pepper_ticket_spec_to_work_packet_compiler.md` | Human-readable P17.0 governance record only. |
| `2_products/pepper-agent/docs/agent-platform/ticket_spec_to_work_packet_compiler.md` | Product documentation for the compile-only compiler contract. |
| `2_products/pepper-agent/hermes_cli/agent_platform/work_packet/__init__.py` | Public WorkPacket compiler export boundary. |
| `2_products/pepper-agent/hermes_cli/agent_platform/work_packet/compiler.py` | Immutable contracts and deterministic compile-only implementation. |
| `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_work_packet_compiler.py` | Focused behavior and integrity test suite. |
| `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | Product-local import manifest rows for P17.0 additions. |
| `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` | Product-local modification register rows for P17.0 additions. |

## Pre-Change Pepper Identity

The authoritative pre-change Pepper identity is the P16.R committed Git tree at `92d1e790e70176ed542b1ae44d6e8af771be512b`.

| Projection | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate excluding baseline record | `6859` | `150872516` | `785f78a69268f8432f50b57a27593fad35dabb03a7830019b16e8a4546b15815` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

## Product Contract

P17.0 introduces the `hermes_cli.agent_platform.work_packet` package. It exports exactly twenty-five public names: three constants, six enums, nine immutable public models, four bounded exceptions and three pure functions.

The compiler binds these inputs:

| Input | Required Binding |
| --- | --- |
| `ProjectSpec` | Project ID must match approval, publication and authorization. |
| `TicketApprovalRecord` | State must be approved, decision must be approve and approved ticket must be present. |
| `TicketPublicationResult` | Logical publication must be published and canonical ticket must equal the approved ticket. |
| `WorkPacketCompilationAuthorization` | Human compile authorization must bind approval digest, canonical ticket digest, publication identity and artifact digest. |
| Fresh lint report | Recomputed in-memory; dispositions allowed are pass and pass with warnings. |
| Dependency plan | Recomputed from approved planning evidence; target ticket must be unblocked and dependency-ready. |

The compiler rejects shadow-only operational authority. Reviewer or authorizer identifiers beginning with `SHADOW-`, and pilot-only tickets `P16.SP0` and `P16.SP1`, cannot authorize compilation.

## Authority Boundary

P17.0 compiles data only. The compiled WorkPacket records `authority_boundary=compile_only`, `execution_ready=false`, `execution_mode=single_agent` and `git_authority=human_only`.

The compiler does not allocate workspaces, grant tool permissions, select providers, select models, assign workers, assign agents, run commands, mutate tickets, create result envelopes, review diffs, persist artifacts, read or write files, call network APIs, mutate Git, run Graphify or run Docker.

## Determinism And Digests

All P17.0 identities are deterministic SHA-256 records over canonical JSON with sorted keys and compact separators. The WorkPacket ID is derived from ticket ID, publication revision and the first twelve hex characters of the compilation-input digest.

| Evidence | Algorithm |
| --- | --- |
| Compilation authorization | `agent-platform-work-packet-compilation-authorization-sha256-v1` |
| Repository scope | `agent-platform-work-packet-repository-scope-sha256-v1` |
| Task step | `agent-platform-work-packet-task-step-sha256-v1` |
| Validation step | `agent-platform-work-packet-validation-step-sha256-v1` |
| Project spec | `agent-platform-work-packet-project-spec-sha256-v1` |
| Source ticket | `agent-platform-work-packet-source-ticket-sha256-v1` |
| Compilation input | `agent-platform-work-packet-compilation-input-sha256-v1` |
| Compilation evidence | `agent-platform-work-packet-compilation-evidence-sha256-v1` |
| WorkPacket | `agent-platform-work-packet-sha256-v1` |
| Compilation result | `agent-platform-work-packet-compilation-result-sha256-v1` |

## Downstream Handoff

The compiler emits exactly seven required downstream requirements. All are unsatisfied by the compiler.

| Capability | Owner |
| --- | --- |
| `workspace_allocation` | `P17.1` |
| `tool_permission_profile` | `P17.2` |
| `single_agent_execution` | `P17.3` |
| `validation_command_runner` | `P17.4` |
| `result_failure_cancellation_envelopes` | `P17.5` |
| `diff_artifact_review` | `P17.6` |
| `human_git_handoff` | `P17.7` |

P17.1 may consume the WorkPacket but must not mutate it, infer additional scope, authorize tools, execute tickets, run validation commands, stage, commit or push.

## Register And Manifest

| Check | Result |
| --- | --- |
| `AGENT_PLATFORM_MODIFICATIONS.tsv` data rows | `182` |
| `AGENT_PLATFORM_MODIFICATIONS.tsv` width | `18` |
| `AGENT_PLATFORM_MODIFICATIONS.tsv` malformed rows | `0` |
| `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` data rows | `6836` |
| `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` width | `8` |
| `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` malformed rows | `0` |
| P17.0 modification rows | `4` |
| P17.0 import manifest rows | `4` |
| P17.0 manifest hash mismatches | `0` |

P17.0 product destination inventory:

| Modification ID | Product path | Current product SHA-256 |
| --- | --- | --- |
| `P17.0-001` | `hermes_cli/agent_platform/work_packet/__init__.py` | `980d3a354697dc422c4d8e91076e65131735b4ec5a80eb6da50b0f89f4448914` |
| `P17.0-002` | `hermes_cli/agent_platform/work_packet/compiler.py` | `9a7205edd973c64f88c96d8e83dc10e864ae6dafb581466ed5fa6122f7c342d9` |
| `P17.0-003` | `tests/hermes_cli/test_agent_platform_work_packet_compiler.py` | `7c54ea1ce3418101fcee2fbcb4a49fa6ac3f2ec1eaeec4dec761735982df3d28` |
| `P17.0-004` | `docs/agent-platform/ticket_spec_to_work_packet_compiler.md` | `8d658a100b9408db7a47f7fbe3302b6184fdea64a8384094bda0ad63d5022c87` |

## Public API Closure

| Check | Result |
| --- | --- |
| Declared package exports | `25` |
| Unique declared package exports | `25` |
| Declared exports resolve on package root | true |
| Hidden names exported | false |

The public root contains the expected compile-only entry points: `build_work_packet_compilation_authorization`, `validate_work_packet` and `compile_ticket_spec_to_work_packet`.

## Runtime Authority Closure

Scoped authority scan covered `hermes_cli/agent_platform/work_packet`.

| Check | Result |
| --- | ---: |
| Forbidden filesystem, subprocess, network or path imports | `0` |
| Execution, filesystem, network, Git, Graphify or Docker API calls | `0` |
| Benign policy vocabulary matches | `26` |

The nonzero vocabulary matches are static digest algorithm names, protected-scope strings, forbidden Git action strings and downstream requirement text. They are not authority grants or calls.

## Validation Evidence

| Command Or Check | Result |
| --- | --- |
| `git branch --show-current` | `p17-governed-workpacket-execution-mvp` |
| `git rev-parse HEAD` | `92d1e790e70176ed542b1ae44d6e8af771be512b` |
| `git rev-parse main` | `92d1e790e70176ed542b1ae44d6e8af771be512b` |
| `git rev-parse origin/main` | `92d1e790e70176ed542b1ae44d6e8af771be512b` |
| `%USERPROFILE%\anaconda3\python.exe -m pytest -q tests/hermes_cli/test_agent_platform_work_packet_compiler.py -p no:cacheprovider` | `237 passed in 4.18s` |
| `%USERPROFILE%\anaconda3\python.exe -m ruff check hermes_cli/agent_platform/work_packet tests/hermes_cli/test_agent_platform_work_packet_compiler.py` | `All checks passed!` |
| `%USERPROFILE%\anaconda3\python.exe -m ruff format --check hermes_cli/agent_platform/work_packet tests/hermes_cli/test_agent_platform_work_packet_compiler.py` | `3 files already formatted` |
| WorkPacket import/export smoke | `25 25 True False` |
| P17.0 manifest hash check | `p17_rows=4 hash_mismatches=0` |
| `%USERPROFILE%\anaconda3\python.exe -m unittest 12_tests/governance/test_pepper_baseline_integrity.py` | `Ran 14 tests in 0.003s`; `OK` |

## Non-Actions

P17.0 performed no staging, commit, push, branch switch, merge, rebase, reset, clean, stash, worktree creation, dependency installation, lockfile update, Docker command or Graphify command.

Graphify remains intentionally not run under the explicit P17.0 constraint.

## Final Verdict

hermes_0_19_pepper_ticket_spec_to_work_packet_compiler_ready_with_compile_only_non_executing_authority
