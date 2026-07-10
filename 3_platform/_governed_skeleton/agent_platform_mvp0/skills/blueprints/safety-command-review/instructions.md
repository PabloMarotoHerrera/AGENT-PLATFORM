# Safety Command Review Instructions

This is inactive guidance.
This file is not a runnable skill.
This file does not authorize tool calls.
This file does not authorize command execution.
This file does not authorize file writes.
This file does not authorize memory writes.
This file does not authorize Git mutation.

## Review Guidance

Use this blueprint only to review command candidates before any future execution gate.

Check command candidates for:

| Risk | Guidance |
| --- | --- |
| Destructive actions | Identify deletion, reset, force, overwrite, deploy, or publication behavior. |
| Credential exposure | Stop if a command could inspect secrets, tokens, cookies, environment secrets, or provider configs. |
| Runtime activation | Stop if a command starts GStack, browser, MCP, provider, GBrain, Graphify, tests, builds, scripts, or CI. |
| Source boundary | Stop if the command scans broad or forbidden paths. |
| Git posture | Never recommend broad staging or `git add .`. |
| Memory posture | Stop if the command writes, syncs, reindexes, promotes, or cleans memory. |

This blueprint is advisory only and does not enforce hooks or settings.
