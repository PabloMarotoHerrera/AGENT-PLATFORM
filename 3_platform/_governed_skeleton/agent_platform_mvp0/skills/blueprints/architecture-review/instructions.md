# Architecture Review Instructions

This is inactive guidance.
This file is not a runnable skill.
This file does not authorize tool calls.
This file does not authorize command execution.
This file does not authorize file writes.
This file does not authorize memory writes.
This file does not authorize Git mutation.

## Review Guidance

Use this blueprint only to review architecture and governance consistency.

Review for:

| Check | Guidance |
| --- | --- |
| Authority alignment | Confirm the proposed work does not treat skills, outputs, or memory as authority. |
| Boundary conflicts | Identify conflicts with no-runtime, no-provider, no-browser, no-MCP, no-memory-write, and no-Git rules. |
| Source posture | Confirm referenced sources are allowed and exact. |
| Output posture | Keep findings as review support until promoted by governance. |

Do not decide acceptance, edit source, run validation, inspect credentials, write memory, or mutate Git.
