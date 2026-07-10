# Safety Command Review Gate Map

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
| Required future gates | Local tool execution gate for command execution, hook registration gate for enforcement, settings mutation gate for settings changes. |

## Rollback And Incident Posture

Rollback requirement: advisory review creates no runtime state. Any future enforcement hook or settings change requires a backup and restore path.

Incident stop rules: stop on enforcement hook request, settings mutation, command execution, credential access, provider/MCP/browser use, memory write, Git mutation, broad staging, or destructive command without gate.

Output classification: review_support, command_candidate.

Memory posture: no_memory_write.

Git posture: blocked.
