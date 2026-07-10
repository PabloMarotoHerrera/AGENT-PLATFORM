# Debug Investigation Gate Map

Runtime profile: S2

Execution allowed: false
Git mutation allowed: false
Memory write allowed: false
Provider use allowed: false
MCP use allowed: false
Browser use allowed: false

## Permission Mapping

| Class | Posture |
| --- | --- |
| Allowed-now permissions | None. |
| Candidate-only permissions | `SKILL_READ_DOCS`, `SKILL_READ_SOURCE_METADATA`, exact command candidate output. |
| Blocked permissions | `SKILL_WRITE_APPROVED_FILES`, `SKILL_RUN_LOCAL_COMMANDS`, `SKILL_RUN_TESTS`, `SKILL_USE_BROWSER`, `SKILL_USE_MCP`, `SKILL_USE_PROVIDER`, `SKILL_USE_CREDENTIALS`, `SKILL_WRITE_MEMORY`, `SKILL_REGISTER_HOOKS`, `SKILL_MODIFY_SETTINGS`, `SKILL_MUTATE_GIT`, `SKILL_DEPLOY`. |
| Required future gates | Local tool execution gate before any command is run. |

## Rollback And Incident Posture

Rollback requirement: command candidates create no state. Any future command execution must define cleanup and rollback before approval.

Incident stop rules: stop on command execution request without gate, DB-internal access, credential access, broad filesystem scan, provider/MCP/browser use, memory write, Git mutation, or product source access.

Output classification: review_support, command_candidate.

Memory posture: no_memory_write.

Git posture: blocked.
