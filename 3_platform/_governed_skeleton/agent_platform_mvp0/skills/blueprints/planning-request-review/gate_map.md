# Planning Request Review Gate Map

Runtime profile: S1

Execution allowed: false
Git mutation allowed: false
Memory write allowed: false
Provider use allowed: false
MCP use allowed: false
Browser use allowed: false

## Permission Mapping

| Class | Posture |
| --- | --- |
| Allowed-now permissions | `SKILL_READ_DOCS`, `SKILL_READ_SOURCE_METADATA` after source review. |
| Candidate-only permissions | None. |
| Blocked permissions | `SKILL_WRITE_APPROVED_FILES`, `SKILL_RUN_LOCAL_COMMANDS`, `SKILL_RUN_TESTS`, `SKILL_USE_BROWSER`, `SKILL_USE_MCP`, `SKILL_USE_PROVIDER`, `SKILL_USE_CREDENTIALS`, `SKILL_WRITE_MEMORY`, `SKILL_REGISTER_HOOKS`, `SKILL_MODIFY_SETTINGS`, `SKILL_MUTATE_GIT`, `SKILL_DEPLOY`. |
| Required future gates | None for review-support output; future gates required for any S3+ action. |

## Rollback And Incident Posture

Rollback requirement: no runtime state is created. Any future file changes require file-level rollback and human review.

Incident stop rules: stop on credential access, provider use, browser/MCP use, memory write, Git mutation, product source access, GStack setup, or command execution.

Output classification: review_support.

Memory posture: no_memory_write.

Git posture: blocked.
