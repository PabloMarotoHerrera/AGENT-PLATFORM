# TicketSpec To WorkPacket Compiler

P17.0 adds the first governed WorkPacket contract for Pepper. It compiles an explicitly approved and logically published `TicketSpec` into an immutable, compile-only `WorkPacket` candidate for later P17 execution stages.

P17.0 requires P16.R closure at commit `92d1e790e70176ed542b1ae44d6e8af771be512b` with the closure verdict declared in `0_architecture/governance/agent_platform_pepper_ticket_factory_closure.md`.

## TicketSpec Versus WorkPacket

`TicketSpec` remains planning evidence. It describes project scope, tasks, validation text, dependencies and response requirements without execution authority.

`WorkPacket` is an execution-input candidate. It preserves the approved `TicketSpec`, projects its repository scope, compiles task and validation step records, records downstream runtime requirements and binds deterministic digest evidence. It is not execution-ready.

## Compile-Only Authority

The compiler is deterministic and in-memory. It validates P16 approval, publication, lint and dependency evidence, then returns immutable Pydantic models.

The compiler does not allocate a workspace, resolve a workspace path, grant tools, select a provider or model, assign an agent or worker, run validation commands, execute tickets, persist files, mutate Git, inspect the repository or claim production readiness.

## Compilation Authorization

Compilation requires a separate `WorkPacketCompilationAuthorization`. This authorization means a human explicitly authorizes compilation of the bound approved and logically published ticket into a compile-only candidate.

It does not authenticate identity and does not authorize runtime execution, workspace allocation, tool permissions, validation command execution or Git mutation.

The authorization binds project ID, ticket ID, publication ID, publication revision, approval digest, canonical ticket digest and publication artifact digest. The authorization digest algorithm is `agent-platform-work-packet-compilation-authorization-sha256-v1`.

## Approval And Publication Binding

The approval record must be approved, must have decision `approve`, must include an approved ticket and must bind fresh lint and planning evidence. Logical publication must be in state `published` and its canonical ticket must equal the approved ticket.

Publication alone is insufficient because logical publication is not persisted filesystem publication and does not grant execution authority. Approval alone is also insufficient because P17.0 requires publication identity and artifact binding.

## Shadow And Pilot Rejection

The compiler rejects shadow-only evidence. Approval reviewer IDs or compilation authorizer IDs beginning with `SHADOW-` are rejected, and pilot-only tickets `P16.SP0` and `P16.SP1` are rejected.

Canonical P16.8 shadow approval is not operational authority. The bounded rejection message is:

```text
shadow-only approval evidence cannot authorize WorkPacket compilation
```

## Repository Scope

`WorkPacketRepositoryScope` copies the source `TicketSpec.scope` without semantic expansion. Source order is preserved for allowed paths, forbidden paths, allowed actions and forbidden actions.

Executable allowed paths reject broad root patterns, absolute paths, Windows drive paths, backslashes, parent traversal and protected roots including `.git/**`, `.opencode/**`, `AGENTS.md`, `graphify-out/**`, `4_external/sources/**` and `2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json`.

Allowed actions reject Git mutation phrases including `git add`, `git commit`, `git push`, `git merge`, `git rebase`, `git reset`, `git clean`, `git stash`, `git switch`, `git checkout`, `git branch`, `git tag`, `git worktree` and `force push`.

Unsafe scope fails closed. The compiler does not reduce or expand scope automatically.

Repository-scope digest algorithm: `agent-platform-work-packet-repository-scope-sha256-v1`.

## Task Steps

Each source task compiles to one `WorkPacketTaskStep` in source order. IDs are contiguous: `TASK-001`, `TASK-002`, `TASK-003` and so on.

The compiler preserves exact task text. It does not merge, split, reorder, infer or execute task instructions.

Task-step digest algorithm: `agent-platform-work-packet-task-step-sha256-v1`.

## Validation Steps

Each source validation step compiles to one `WorkPacketValidationStep` in source order. A step with a command is classified as `command`; a step without a command is classified as `manual`.

Validation ID, description, command or null, expected result and required flag are preserved. `command_execution_authorized` is always false.

The compiler does not execute commands, parse shell syntax, normalize commands, split or join commands, expand environment variables, resolve executables or inspect command availability. P17.4 owns command execution.

Validation-step digest algorithm: `agent-platform-work-packet-validation-step-sha256-v1`.

## Fresh Lint Gate

The compiler reruns deterministic linting with one published ticket, the recomputed dependency plan and `collection_complete=False`.

Permitted lint dispositions are `pass` and `pass_with_warnings`. Warnings require `WorkPacketCompilationAuthorization.risk_acknowledgement`. The compiler does not auto-fix lint findings and does not execute validation commands.

## Dependency Eligibility

The approval record must include fresh planning evidence. The compiler recomputes the dependency plan from `approval_record.fresh_planning_evidence.planning_request` and requires it to equal the approved planning evidence.

The target ticket must be present, unblocked, included in topological order and included in a dependency-ready wave. A `ParallelWave` remains planning metadata, not runtime scheduling authority.

## Deterministic Identity

WorkPacket ID shape:

```text
WP-<NORMALIZED-TICKET-ID>-R<4-DIGIT-REVISION>-<12-LOWERCASE-HEX>
```

The suffix is the first twelve characters of `compilation_input_SHA256`. The compiler uses no random, clock or UUID generation.

## Digest Algorithms

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

## Downstream Requirements

The compiler always emits exactly seven downstream requirements in order:

| Capability | Owner |
| --- | --- |
| `workspace_allocation` | `P17.1` |
| `tool_permission_profile` | `P17.2` |
| `single_agent_execution` | `P17.3` |
| `validation_command_runner` | `P17.4` |
| `result_failure_cancellation_envelopes` | `P17.5` |
| `diff_artifact_review` | `P17.6` |
| `human_git_handoff` | `P17.7` |

Every requirement is required and unsatisfied by the compiler. Callers cannot supply alternate downstream requirements.

## JSON Boundary

All public models support Pydantic `model_dump`, `model_dump_json`, `model_validate`, `model_validate_json` and `model_json_schema`. JSON arrays validate back into immutable tuples.

P17.0 does not implement file serialization, YAML serialization, Markdown rendering, database persistence, filesystem persistence or Git persistence.

## Exceptions

`WorkPacketCompilerInputError` reports structural input failures. `WorkPacketCompilerAuthorizationError` reports missing or invalid compile authorization. `WorkPacketCompilerIntegrityError` reports digest or nested integrity failures.

Errors may include bounded identifiers and failed invariant names. They must not include complete specs, complete approval records, complete publication results, complete WorkPackets, credentials, personal paths, provider responses, raw prompts or reasoning traces.

## Synthetic Examples

Valid synthetic compile flow:

```text
Project P17, Ticket P17.0, approval reviewer reviewer.p17-0, publisher publisher.p17-0 and authorizer authorizer.p17-0 produce a compile-only WorkPacket with execution_ready=false.
```

Mismatched approval example:

```text
An authorization bound to approval digest A cannot compile a publication bound to approval digest B.
```

Shadow approval rejection example:

```text
The canonical P16.SP1 shadow approval is rejected with WorkPacketCompilerAuthorizationError.
```

Blocked dependency example:

```text
A target ticket listed in dependency_plan.blocked_ticket_ids is not eligible for WorkPacket compilation.
```

Unsafe scope example:

```text
allowed_paths=(".git/**",) is rejected instead of reduced.
```

Tampered WorkPacket example:

```text
Changing TASK-001 text without recomputing its digest causes validate_work_packet to raise WorkPacketCompilerIntegrityError.
```

## P17.1 Handoff

P17.1 may consume `WorkPacket`, `WorkPacketCompilationResult`, `WorkPacketRepositoryScope` and `WorkPacketDownstreamRequirement`.

P17.1 owns workspace allocation request, workspace allocation policy, repository identity binding, isolated workspace identity, workspace root validation, source branch and commit binding, read/write scope projection, collision prevention, workspace lifecycle, cleanup eligibility and allocation result digest.

P17.1 must not mutate the WorkPacket, infer additional scope, authorize tools, execute tickets, run validation commands, stage, commit or push. `execution_ready=false` is expected at the P17.1 boundary.
