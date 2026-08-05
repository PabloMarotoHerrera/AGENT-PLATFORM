# P17.4 - Governed Validation Command Runner

P17.4 adds a governed validation-command runner for one completed Pepper WorkPacket execution. It binds one compiled P17.0 `WorkPacket`, one P17.1 human-provisioned workspace allocation, one P17.2 deny-first permission profile, one completed P17.3 single-agent execution result, one explicit human validation authorization, and one current Python runtime binding.

The runner executes only exact command-validation steps already compiled into the WorkPacket. It never generates commands, invokes a shell, accepts ad hoc commands, grants P17.2 validation-command permission, calls providers or models, invokes Git directly, stages, commits, pushes, runs Docker, runs Graphify, or creates result/failure/cancellation envelopes.

Final verdict: hermes_0_19_pepper_validation_command_runner_ready_with_exact_human_authorized_shell_free_bounded_subprocess_authority

## Prerequisites

P17.4 consumes these governed contracts:

| Stage | Requirement |
| --- | --- |
| P17.0 | A compiled WorkPacket containing command validation steps. |
| P17.1 | An allocated exclusive linked worktree whose identity can be reinspected. |
| P17.2 | A deny-first tool permission profile where `validation_command` remains denied. |
| P17.3 | A completed single-agent execution result with zero provider dispatches and zero model inferences. |

P17.4 does not consume natural-language task text as executable input. The only executable inputs are WorkPacket `validation_steps` whose kind is `command` and whose command string survives the P17.4 parser.

Manual validation steps are not executed. Their validation IDs are carried as `manual_validation_ids_pending` in the runner session and result.

## Runtime Binding

`ValidationCommandRuntimeBinding` fixes the subprocess posture:

| Field | Value |
| --- | --- |
| `shell` | `false` |
| `stdin_disabled` | `true` |
| `environment_policy_id` | `pepper-minimal-validation-command-environment-v1` |
| `max_stdout_bytes` | `262144` |
| `max_stderr_bytes` | `262144` |
| `retained_stdout_bytes` | `65536` |
| `retained_stderr_bytes` | `65536` |
| `output_reader_threads` | `2` |
| `network_isolation_guaranteed` | `false` |
| `process_tree_isolation_guaranteed` | `false` |

The Python executable must be an absolute regular file, must not be a symlink, and must be the current interpreter path. The working directory is the allocated workspace root. The binding ID is `VCB-<NORMALIZED-TICKET-ID>-R<4-DIGIT-REVISION>-<12-LOWERCASE-HEX>`.

## Human Authorization

`ValidationCommandRunnerAuthorization` is explicit human evidence authorizing execution of the WorkPacket's exact command-validation steps. It binds the WorkPacket, allocation, tool permission profile, P17.3 single-agent result, runtime binding, and command specifications by digest.

Each command validation step requires one `ValidationCommandAuthorizationRequest` with the exact validation ID, timeout in seconds, and expected exit codes. Coverage must match command validation steps exactly. Duplicate requests fail. Manual validation IDs cannot be authorized as commands.

The authorizer must be explicit and non-shadow. `execution_authorized=true`, `synthetic=false`, and `risk_acknowledgement` is always required because subprocess execution is a bounded but real authority.

## Command Policy

P17.4 parses each source command with `shlex.split(..., posix=True)` only after rejecting control separators, shell markers, shell tokens, backslashes, and secret-shaped text.

Accepted source commands must use this shape:

```text
python -m <module> [args...]
```

Allowed executables are `python`, `python3`, `py`, or the current interpreter filename. Allowed modules are exactly:

| Module | Normalized execution |
| --- | --- |
| `pytest` | Current interpreter plus `-m pytest`; adds `-p no:cacheprovider` if absent. |
| `unittest` | Current interpreter plus `-m unittest`. |
| `ruff check` | Current interpreter plus `-m ruff check`; adds `--no-cache` if absent. |
| `ruff format --check` | Current interpreter plus `-m ruff format --check`. |

Unsupported examples fail closed:

```text
python script.py
pytest -q
python -c "print(1)"
python -m pip install package
python -m pytest tests && git status
python -m ruff check --fix
python -m ruff format src
```

The runner does not expand variables, run through `cmd.exe`, run through PowerShell, run through `/bin/sh`, read response files, accept environment assignments, accept absolute paths, accept parent traversal, or execute repository-relative commands directly.

## Subprocess Execution

`execute_validation_command` launches the normalized argv with `subprocess.Popen` using:

```text
shell=False
stdin=subprocess.DEVNULL
stdout=subprocess.PIPE
stderr=subprocess.PIPE
text=False
cwd=<allocated workspace root>
env=<minimal validation environment>
close_fds=True
```

The environment is fixed plus a small allowlist from the parent process. Fixed values include `NO_COLOR=1`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`, `PYTHONIOENCODING=utf-8`, `PYTHONNOUSERSITE=1`, and `PYTHONUTF8=1`.

Stdout and stderr are drained by two bounded reader threads. Exceeding either byte limit requests termination. Timeout requests termination. If the process remains alive after the bounded grace period, the runner requests a kill.

The runner does not claim network isolation or process-tree isolation. Those flags are explicit `false` values in runtime evidence.

## Workspace Reinspection

P17.4 reinspects the allocated workspace before preparing and around each subprocess execution through the P17.1 inspection seam with `require_clean_worktree=false` and `require_linked_worktree=true`.

The root, resolved root, Git top level, branch, `HEAD`, inside-worktree posture, and linked-worktree posture must still match the allocation. Dirty status is allowed because P17.3 may have created governed filesystem changes before validation commands run.

P17.4 inherits P17.1 read-only Git inspection only. It does not call Git directly and does not mutate Git state.

## Output Evidence

`ValidationCommandCapturedStream` stores bounded sanitized retained text only for the per-command execution result. It records raw byte count, retained byte count, raw SHA-256, truncation posture, redaction count, decode replacement count, and stream digest.

`ValidationCommandExecutionEvidence` stores counts, digests, disposition, failure reason, exit code, timeout, termination posture, and workspace inspection digests. It does not store retained stdout or stderr text.

Secret-shaped output is redacted from retained text. Raw stream SHA-256 is updated incrementally from observed stream bytes and remains a digest, not a plaintext log.

## Session State

`ValidationCommandRunnerSession` is immutable and caller-supplied on every transition. There is no process-global runner registry.

| State | Meaning |
| --- | --- |
| `prepared` | Bindings validated; first command is next. |
| `active` | At least one command may have executed and the runner can continue. |
| `blocked` | A command failed, timed out, exceeded output limits, or could not launch. |
| `cancelled` | Cancellation was requested before launching the next command. |
| `completed` | All command validation steps passed and completion evidence was produced. |

Command IDs are contiguous from `VCMD-001`. Commands run in WorkPacket validation-step order. A passed command advances `next_command_index`. A non-passed command records evidence and blocks the session.

## Completion Result

`complete_validation_command_runner` produces `ValidationCommandRunnerResult` only when every command evidence entry passed and the command sequence is complete.

Canonical completion posture:

| Capability | P17.4 status |
| --- | --- |
| Validation command runner requirement | satisfied |
| Result/failure/cancellation envelopes | deferred to P17.5 |
| Diff and artifact review | deferred to P17.6 |
| Human Git handoff | deferred to P17.7 |
| Provider dispatch | absent |
| Model inference | absent |
| Git mutation | absent |

The final result contains no provider responses, model responses, prompts, reasoning traces, Git output, staging evidence, commit evidence, push evidence, Docker evidence, Graphify evidence, or result envelope.

## Digest Algorithms

| Evidence | Algorithm |
| --- | --- |
| Runtime binding | `agent-platform-validation-command-runtime-binding-sha256-v1` |
| Command specification | `agent-platform-validation-command-specification-sha256-v1` |
| Authorization | `agent-platform-validation-command-runner-authorization-sha256-v1` |
| Captured stream | `agent-platform-validation-command-captured-stream-sha256-v1` |
| Execution evidence | `agent-platform-validation-command-execution-evidence-sha256-v1` |
| Session | `agent-platform-validation-command-runner-session-sha256-v1` |
| Execution result | `agent-platform-validation-command-execution-result-sha256-v1` |
| Runner result | `agent-platform-validation-command-runner-result-sha256-v1` |

Digests are deterministic integrity evidence, not signatures.

## Public Exceptions And JSON Boundary

Public exceptions are `ValidationCommandRunnerError`, `ValidationCommandRunnerInputError`, `ValidationCommandRunnerAuthorizationError`, `ValidationCommandRunnerIntegrityError`, `ValidationCommandPolicyError`, `ValidationCommandExecutionError`, and `ValidationCommandRunnerStateError`. Errors expose bounded invariant identifiers only.

All public models are immutable Pydantic models with forbidden extra fields and JSON round-trip support through `model_dump`, `model_dump_json`, `model_validate`, `model_validate_json`, and `model_json_schema`. P17.4 does not define YAML support, database persistence, session-file persistence, process-handle serialization, thread-handle serialization, environment serialization beyond policy evidence, or log-file persistence.

## Residual Limitations

Validation command execution is intentionally narrow. Only exact compiled command-validation steps can run. Shells, arbitrary executables, direct test-runner executables, package installers, write-mode formatters, provider dispatch, model inference, network authority, Git mutation, Docker, Graphify, diff review, artifact review, result envelopes, and human Git handoff remain outside P17.4.
