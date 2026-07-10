# Debug Investigation Instructions

This is inactive guidance.
This file is not a runnable skill.
This file does not authorize tool calls.
This file does not authorize command execution.
This file does not authorize file writes.
This file does not authorize memory writes.
This file does not authorize Git mutation.

## Investigation Guidance

Use this blueprint only to structure an investigation plan and, when useful, propose exact command candidates for separate human and gate review.

An investigation plan should identify:

| Check | Guidance |
| --- | --- |
| Symptom | State the observed behavior without claiming root cause too early. |
| Scope | Identify exact allowed files or records. |
| Risks | Identify credential, DB-internal, broad-scan, runtime, provider, browser, MCP, memory, and Git risks. |
| Command candidates | If commands are proposed, describe exact command text, working directory, inputs, expected outputs, and why a future gate is required before execution. |
| Stop conditions | Stop if the investigation needs blocked sources, credentials, runtime execution, memory writes, or Git mutation. |

Do not execute any command candidate.
