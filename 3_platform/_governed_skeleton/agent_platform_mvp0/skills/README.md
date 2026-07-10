# AGENT PLATFORM Static Skill Skeleton

This directory is an inactive governed skill skeleton.

It is not a runtime.
It is not a registry executor.
It does not authorize skill execution.
It does not write memory.
It does not call providers.
It does not mutate Git.

## Purpose

This skeleton records the first project-local skill metadata for AGENT PLATFORM under P12.10. It contains an inactive static registry and six seed SkillBlueprint records.

The skeleton represents:

| Represents | Posture |
| --- | --- |
| Static internal skill metadata | Allowed. |
| Inactive registry | Allowed. |
| Review/planning blueprints | S1 only. |
| Command-candidate blueprints | S2 only; no execution. |
| Source refs and gate mappings | Required. |

The skeleton does not represent:

| Does not represent | Boundary |
| --- | --- |
| Active runtime | Not created. |
| Slash commands | Not created. |
| Host skill registration | Not created. |
| GStack setup | Not performed. |
| Tool runner | Not created. |
| Agent dispatcher | Not created. |
| Provider interface | Not created. |
| MCP server | Not created. |
| Browser runtime | Not created. |
| Memory writer | Not created. |
| Git automation | Not created. |
| Deployment system | Not created. |

## Governance Boundary

This skeleton is governed by:

| Governance source | Marker |
| --- | --- |
| `0_architecture/governance/agent_platform_skill_stack_bootstrap_design.md` | `skill_stack_bootstrap_design_ready` |
| `0_architecture/governance/agent_platform_skill_authority_execution_boundary.md` | `skill_authority_execution_boundary_ready` |
| `0_architecture/governance/agent_platform_gstack_adoption_decision.md` | `gstack_adoption_decision_ready` |
| `0_architecture/governance/agent_platform_memory_store_integration_design.md` | `memory_store_integration_design_ready` |
| `0_architecture/governance/agent_platform_retention_rollback_incident_hardening.md` | `retention_rollback_incident_hardening_ready` |

## Seed Blueprints

| Skill ID | Profile | Output posture | Runtime posture |
| --- | --- | --- | --- |
| `skill.planning.request_review` | S1 | `review_support` | Execution blocked. |
| `skill.review.architecture` | S1 | `review_support` | Execution blocked. |
| `skill.debug.investigation` | S2 | `review_support`, `command_candidate` | Execution blocked. |
| `skill.safety.command_review` | S2 | `review_support`, `command_candidate` | Execution blocked. |
| `skill.docs.release_notes_candidate` | S2 | `draft_documentation`, `command_candidate` | Execution blocked. |
| `skill.memory.update_request` | S1 | `memory_update_request`, `review_support` | Execution blocked. |

## Invariants

Skills are not authority.
Skills are not memory authority.
Skills require explicit execution gates.
A skill can recommend; governance approves; execution gates execute.
Browser, MCP, provider, runtime, Git, and memory-write surfaces are blocked by default.
Generated files and runtime outputs are not authority by default.
Skill runtime rollback must exist before future execution.
