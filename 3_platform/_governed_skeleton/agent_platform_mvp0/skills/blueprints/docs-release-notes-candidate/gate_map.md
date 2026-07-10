# Docs Release Notes Candidate Gate Map

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
| Candidate-only permissions | `SKILL_READ_DOCS`, `SKILL_READ_SOURCE_METADATA`, draft documentation candidate output, exact command candidate output. |
| Blocked permissions | `SKILL_WRITE_APPROVED_FILES`, `SKILL_RUN_LOCAL_COMMANDS`, `SKILL_RUN_TESTS`, `SKILL_USE_BROWSER`, `SKILL_USE_MCP`, `SKILL_USE_PROVIDER`, `SKILL_USE_CREDENTIALS`, `SKILL_WRITE_MEMORY`, `SKILL_REGISTER_HOOKS`, `SKILL_MODIFY_SETTINGS`, `SKILL_MUTATE_GIT`, `SKILL_DEPLOY`. |
| Required future gates | File-write gate for document writes, Git mutation gate for stage/commit/tag/push, deployment gate for release or publish. |

## Rollback And Incident Posture

Rollback requirement: drafts create no runtime state. Future file writes require diff review and rollback path; future release actions require deployment rollback owner.

Incident stop rules: stop on Git mutation, release tagging, deployment, CI, package publishing, provider calls, command execution without gate, generated-output promotion, or credential exposure.

Output classification: draft_documentation, command_candidate.

Memory posture: no_memory_write.

Git posture: blocked.
