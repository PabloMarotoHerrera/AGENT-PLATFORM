# P1.4 - Agent Runtime Boundary Contract Hardening

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Agent Runtime Boundary Contract Hardening |
| Ticket | P1.4 |
| Status | Accepted agent runtime boundary contract hardening |
| Date | 2026-07-04 |
| Scope | Harden the agent runtime boundary metadata contract for AGENT PLATFORM / Siamese so future agent records, task records, handoff records, approval records, context records, tool records, provider records, validation records, security records, Graphify evidence records, and Cognitive Semantic System records can reference agent runtime metadata safely. |
| Authority | Agent runtime boundary metadata contract hardening only, not agent runtime activation, task execution, handoff execution, approval workflow activation, provider/auth approval, tool execution approval, product activation, source loading, source tracking approval, Graphify adoption, or Cognitive Semantic System substrate selection. |
| Related documents | P0.1, P0.2, P0.3, P1.1, P1.2, P1.3, G-19, I-A, I-03, I-01, I-02, I-04, I-05, I-06, I-07, S-03, S-04, CSS ADR/audit, Graphify Repo Map Summary, `.gitignore`, `.graphifyignore`. |
| Output | Agent runtime boundary contract hardening. |

This document is the Agent Runtime Boundary Contract Hardening record for AGENT PLATFORM / Siamese. Agent runtime boundary contract hardening is not agent runtime activation.

## 2. Purpose
P0.1 mapped activation gates and confirmed that AGENT PLATFORM remains gated by exact-scope governance controls.

P0.2 defined validation execution gate design without running validation.

P0.3 defined security enforcement hardening without implementing runtime enforcement.

P1.1 hardened context runtime contract boundaries without activating context runtime behavior or loading source.

P1.2 hardened provider adapter metadata contract boundaries without configuring provider/auth behavior.

P1.3 hardened tool execution boundary contracts without approving tool execution.

P1.4 hardens the agent runtime boundary contract so future lanes can reference agent runtime metadata safely without treating agent metadata, task metadata, handoff metadata, approval metadata, context availability, tool availability, provider availability, generated evidence, or Cognitive Semantic System records as permission to execute agents, activate runtime behavior, call tools, call providers, access product source, load raw source, or select a Cognitive Semantic System substrate.

P1.4 does not activate agent runtime. P1.4 does not execute agent tasks. P1.4 does not execute agent handoffs. P1.4 does not approve provider/auth. P1.4 does not approve tool execution. P1.4 does not load source. P1.4 does not start P1.5 or P2.1.

## 3. Current Agent Runtime Posture
| Area | Current posture | P1.4 result |
| --- | --- | --- |
| Activation level | AGENT PLATFORM remains pre-active at AL-1 metadata skeleton. | No promotion. |
| Agent runtime | Metadata-only and pre-active by current accepted governance. | Contract hardening only. |
| Agent runtime records | Agent runtime records are not permission to act. | Non-permission semantics preserved. |
| Agent task records | Agent task records are not execution approval. | Task records remain metadata. |
| Agent handoff records | Agent handoff records are not handoff execution approval. | Handoff records remain metadata. |
| Agent capability records | Agent capability records are not runtime capability activation. | Capability refs remain blocked metadata. |
| Agent context references | Agent context references are metadata, not source loading approval. | Context blockers must travel downstream. |
| Agent tool references | Agent tool references are metadata, not tool execution approval. | GT-07 remains required. |
| Agent provider references | Agent provider references are metadata, not provider/auth approval. | GT-08 remains required. |
| Agent output references | Agent output references are generated evidence, not authority. | Generated-output posture preserved. |
| Validation | Validation may evaluate later but cannot decide activation. | No validation execution. |
| Security | Security constrains agent metadata and future readiness. | Blockers remain binding. |
| Cognitive Semantic System | Metadata prototype and accepted name only. | Cognitive Semantic System substrate remains deferred. |
| Graphify | Curated generated evidence only. | Not authority. |
| Siamese | Living energy twin product vision only. | No product activation. |

No agent execution is approved by P1.4.

## 4. Agent Runtime Boundary Contract Definition
An agent runtime boundary contract is a metadata contract that defines how agent runtime refs, agent capability refs, agent task records, agent instruction records, agent plan records, agent handoff records, agent approval records, agent execution intents, context refs, tool refs, provider refs, evidence refs, validation refs, security refs, blockers, limitations, and retention posture are represented without authorizing agent runtime activation, task execution, handoff execution, tool execution, provider calls, raw source loading, product access, or publication.

| Clarification | Rule |
| --- | --- |
| Agent runtime boundary contract hardening is not agent runtime activation. | P1.4 hardens metadata semantics only. |
| Agent runtime refs are metadata. | They identify a boundary record, not an executable runtime. |
| Agent metadata is not permission to act. | Metadata cannot create action authority. |
| Agent task metadata is not execution approval. | Task records describe proposed or blocked work only. |
| Agent handoff metadata is not handoff execution approval. | Handoff records preserve transfer intent and blockers only. |
| Agent capability metadata is not runtime capability activation. | Capability refs cannot activate runtime, tools, providers, products, or context loading. |
| Agent plan metadata is not execution. | Plans are proposed reasoning artifacts and must remain non-operative. |
| Agent approval metadata is not approval unless explicitly approved by the accepted governance route. | Approval refs cannot self-authorize. |
| Agent context refs are not source loading approval. | GT-01, GT-05, GT-09, and context gates still apply by source class. |
| Agent tool refs are not tool execution approval. | Tool use from agents requires GT-07. |
| Agent provider refs are not provider/auth approval. | Provider/auth for agents requires GT-08. |
| Agent output metadata is not authority. | Agent output is generated evidence unless curated by governance. |
| Agent metadata is not product activation. | Product-bound agent action requires GT-09. |
| Agent metadata is not Cognitive Semantic System substrate selection. | Cognitive Semantic System substrate remains deferred. |

## 5. Agent Runtime Object Model
| Object | Meaning | Required fields | Forbidden fields | Security posture | Validation posture |
| --- | --- | --- | --- | --- | --- |
| AgentRuntimeBoundary | Top-level metadata boundary for agent runtime posture. | `boundary_id`, `runtime_scope`, `activation_level`, `execution_status`, `agent_refs`, `security_refs`, `validation_refs`, `blockers`, `limitations`, `retention_posture`, `review_required` | Runtime entrypoints, schedulers, queues, workers, executable code, secrets, credentials | Preserve AL-1 inactive posture and all blockers. | Future completeness validation only. |
| AgentRuntimeRef | Metadata reference to a possible agent runtime surface. | `agent_ref_id`, `agent_name_or_identifier`, `agent_family`, `runtime_scope`, `activation_level`, `execution_status`, `security_refs`, `validation_refs`, `blockers` | Callable handles, process IDs, commands, tokens, live sessions | Must never imply permission to activate or execute agents. | Future ref-field validation only. |
| AgentCapabilityRef | Metadata reference to a capability an agent may need in the future. | `capability_ref_id`, `agent_ref_id`, `capability_name`, `capability_scope`, `required_gates`, `tool_refs`, `provider_refs`, `blockers`, `limitations` | Active capability flags, executable payloads, prompts with secrets | Capability metadata is not runtime capability activation. | Future blocker-preservation validation only. |
| AgentTaskRecord | Metadata record for proposed, blocked, deferred, or review-only work. | `agent_task_id`, `requested_action`, `request_owner`, `agent_role`, `input_refs`, `output_refs`, `context_refs`, `tool_refs`, `provider_refs`, `execution_status`, `blockers` | Task execution payloads, secret values, raw source, live runtime state | Task records cannot execute work. | Future task completeness and no-execution invariant validation only. |
| AgentInstructionRecord | Metadata record for instruction scope and restrictions. | `instruction_ref_id`, `agent_ref_id`, `instruction_scope`, `allowed_use`, `forbidden_use`, `required_gates`, `security_refs`, `limitations`, `review_required` | Instructions to bypass gates, secret-bearing instructions, provider auth values | Instructions must preserve security and governance blockers. | Future boundary invariant validation only. |
| AgentPlanRecord | Metadata record for a proposed plan. | `plan_ref_id`, `agent_ref_id`, `task_refs`, `plan_summary`, `dependencies`, `required_gates`, `blockers`, `limitations`, `retention_posture` | Executable steps treated as approved actions, raw source dumps, credentials | Plan metadata is not execution. | Future plan posture validation only. |
| AgentHandoffRecord | Metadata record for proposed handoff between agents or lanes. | `agent_handoff_id`, `handoff_source`, `handoff_target`, `handoff_reason`, `context_refs`, `evidence_refs`, `security_refs`, `validation_refs`, `blockers`, `limitations` | Handoff execution triggers, secret-bearing context, unscoped instructions | Handoff metadata is not handoff execution approval. | Future handoff blocker preservation validation only. |
| AgentApprovalRecord | Metadata record for claimed, requested, blocked, or accepted approval posture. | `approval_ref_id`, `approval_subject`, `approval_scope`, `approval_owner`, `approval_status`, `approval_gate`, `allowed_actions`, `forbidden_actions`, `security_refs`, `validation_refs` | Self-granted approvals, broad approval text, approval without owner/gate, secrets | Approval metadata cannot override gates or blockers. | Future approval completeness validation only. |
| AgentExecutionIntent | Metadata declaration that execution may be desired later. | `intent_id`, `agent_ref_id`, `requested_action`, `required_approval_gate`, `required_tool_gate`, `required_provider_gate`, `required_product_gate`, `blockers`, `review_required` | Runtime start commands, tool commands, provider calls, auth material | Execution intent is blocked until gates approve exact scope. | Future readiness evaluation only. |
| AgentExecutionBlocker | Explicit stop condition for agent metadata. | `blocker_id`, `target_ref`, `reason`, `required_gate`, `stop_behavior`, `review_required`, `status` | Bypass instructions, hidden exceptions, broad approvals | Blockers must travel downstream. | Future blocker-retention validation only. |
| AgentContextRef | Metadata reference to context packs or context source refs. | `context_ref_id`, `context_pack_id`, `source_classification`, `sensitivity`, `local_only`, `blockers`, `retention_posture`, `security_refs` | Raw source content, product source, secrets, credentials, raw generated output | Context refs are not source loading permission. | Future context-to-agent blocker validation only. |
| AgentToolRef | Metadata reference to required or candidate tools. | `tool_ref_id`, `tool_name_or_identifier`, `tool_scope`, `required_tool_gate`, `risk_level`, `blockers`, `security_refs`, `validation_refs` | Executable commands, shell payloads, package manager commands, Git mutation commands | Tool refs cannot authorize tool execution. | Future GT-07 blocker validation only. |
| AgentProviderRef | Metadata reference to required or candidate providers. | `provider_ref_id`, `provider_name_or_identifier`, `provider_scope`, `auth_posture`, `network_posture`, `required_provider_gate`, `blockers` | API keys, tokens, endpoint credentials, provider configs, live sessions | Provider refs cannot authorize provider/auth. | Future GT-08 blocker validation only. |
| AgentEvidenceRef | Metadata evidence reference for agent records. | `evidence_ref_id`, `evidence_type`, `evidence_source`, `evidence_scope`, `limitations`, `retention_posture`, `generated_output_related` | Raw local-only output, secrets, credential values, raw Graphify output by default | Evidence supports; it does not decide. | Future evidence-boundary validation only. |
| AgentValidationRef | Metadata reference to validation posture. | `validation_ref_id`, `validation_gate`, `validation_target`, `validation_status`, `proof_level`, `limitations`, `blockers`, `not_executed_reason` | Unapproved command output as authority, secret-bearing validation output | Validation refs do not approve activation or execution. | Must cite GT-04 for future execution evidence. |
| AgentSecurityRef | Metadata reference to security posture. | `security_ref_id`, `security_policy`, `security_scope`, `sensitivity`, `approval_status`, `blocked_actions`, `blockers`, `incident_requirements` | Secret values, credential values, provider auth material | Security refs constrain and can block; they do not grant permission. | Future sensitivity and blocker validation only. |
| AgentOutputRef | Metadata reference to agent-generated output. | `output_ref_id`, `agent_ref_id`, `output_classification`, `source_classification`, `sensitivity`, `generated_output_related`, `validation_refs`, `security_refs`, `limitations`, `retention_posture` | Published output by default, secret values, credential values, raw product or external source | Agent outputs are generated evidence, not authority by default. | Future generated-evidence invariant validation only. |
| AgentRetentionRecord | Metadata for retention, redaction, quarantine, deletion, and publication posture. | `retention_id`, `target_ref`, `retention_class`, `redaction_required`, `quarantine_trigger`, `publication_blocker`, `tracking_requirement`, `incident_route` | Retained secrets, credential values, raw local-only dumps | Retention must minimize exposure. | Future retention field validation only. |
| AgentLimitation | Metadata record for constrained or uncertain use. | `limitation_id`, `target_ref`, `description`, `impact`, `review_route`, `created_at` | Claims of final authority or unrestricted readiness | Limitations remain attached downstream. | Future limitation-preservation validation only. |

## 6. Agent Runtime Reference Contract
Every agent runtime ref must contain the fields below before it can be used in downstream metadata records.

| Field | Required meaning |
| --- | --- |
| `agent_ref_id` | Stable identifier for the agent runtime metadata reference. |
| `agent_name_or_identifier` | Human-readable name or metadata identifier without implying activation. |
| `agent_family` | Agent family, lane, or role category such as governance, validation, security, context, provider, tool, product-readiness, implementation, review, orchestration, or unknown. |
| `runtime_scope` | Exact metadata scope for the agent runtime reference. |
| `activation_level` | Current activation level; default is AL-1 metadata skeleton unless governed otherwise. |
| `execution_status` | Metadata-only execution posture such as proposed, blocked, deferred, or approved metadata only. |
| `capability_refs` | AgentCapabilityRef IDs or `none`. |
| `task_refs` | AgentTaskRecord IDs or `none`. |
| `handoff_refs` | AgentHandoffRecord IDs or `none`. |
| `context_refs` | AgentContextRef IDs or `none`; not source loading approval. |
| `tool_refs` | AgentToolRef IDs or `none`; not tool execution approval. |
| `provider_refs` | AgentProviderRef IDs or `none`; not provider/auth approval. |
| `approval_refs` | AgentApprovalRecord IDs or `none`; not approval unless governance explicitly grants it. |
| `validation_refs` | AgentValidationRef IDs or `none`. |
| `security_refs` | AgentSecurityRef IDs or `none`. |
| `evidence_refs` | AgentEvidenceRef IDs or `none`. |
| `input_contract_refs` | Metadata refs describing allowed future input classes. |
| `output_contract_refs` | Metadata refs describing output classification and retention posture. |
| `handoff_contract_refs` | Metadata refs describing handoff constraints. |
| `source_classification` | Governance metadata, implementation metadata, generated evidence, local-only, product-restricted, external, credential reference, secret value, provider auth material, runtime state, or unknown sensitivity. |
| `sensitivity` | Current sensitivity label and highest inherited sensitivity. |
| `local_only` | Whether the ref is local-only or local-only-derived. |
| `product_related` | Whether product source, product output, or product action is implicated. |
| `external_related` | Whether external source, external service, or external output is implicated. |
| `generated_output_related` | Whether generated evidence or output is implicated. |
| `credential_related` | Whether credential material or credential need is implicated. |
| `secret_related` | Whether secret material or secret risk is implicated. |
| `allowed_use` | Exact metadata-only use allowed for review. |
| `forbidden_use` | Explicit forbidden uses including activation, execution, provider calls, tool calls, source loading, publication, source tracking, and product activation. |
| `tracking_posture` | Trackable, ignored, local-only, blocked, exact-path future review, or unknown. |
| `retention_posture` | Metadata-only, generated-sensitive, local-only, quarantine, deletion candidate, or unknown. |
| `review_required` | Required review state; defaults to true. |
| `blockers` | Blocking conditions that must travel with the ref. |
| `limitations` | Known uncertainty and restricted-use notes. |

Agent runtime refs must never imply permission to activate or execute agents. Agent runtime refs are metadata.

## 7. Agent Task And Handoff Metadata Contract
Agent task and handoff metadata may describe proposed work, but must not execute work.

| Field | Required meaning |
| --- | --- |
| `agent_task_id` | Stable identifier for a task metadata record. |
| `agent_handoff_id` | Stable identifier for a handoff metadata record when handoff is implicated. |
| `requested_action` | Proposed action or work description, not an executable approval. |
| `request_owner` | Accountable owner or `unknown` with blocker. |
| `agent_role` | Agent role or lane without implying active runtime. |
| `agent_capability_refs` | Capability refs required or proposed for the task. |
| `input_refs` | Metadata refs for inputs; not raw source loading approval. |
| `output_refs` | Metadata refs for outputs; generated evidence by default. |
| `context_refs` | Context refs; not context source loading approval. |
| `tool_refs` | Tool refs; not tool execution approval. |
| `provider_refs` | Provider refs; not provider/auth approval. |
| `required_approval_gate` | Governance gate required before any action. |
| `required_tool_gate` | GT-07 when tool use is implicated. |
| `required_provider_gate` | GT-08 when provider/auth/network/MCP is implicated. |
| `required_product_gate` | GT-09 when product source, product output, or product behavior is implicated. |
| `validation_requirements` | Future validation posture and GT-04 requirements. |
| `security_requirements` | Security posture, sensitivity, blockers, and incident requirements. |
| `source_tracking_posture` | GT-02/GT-12 posture for any tracking, staging, commit, push, force-add, or publication impact. |
| `product_scope` | Product relationship, if any, without product activation. |
| `execution_status` | Metadata-only status; no P1.4 status may imply execution. |
| `handoff_source` | Source agent, lane, or record for handoff metadata. |
| `handoff_target` | Target agent, lane, or record for handoff metadata. |
| `handoff_reason` | Reason for proposed handoff. |
| `rollback_posture` | Future rollback requirement before any execution approval. |
| `retention_posture` | Retention, redaction, quarantine, deletion, publication, and tracking posture. |
| `review_required` | Required review; defaults to true. |
| `blockers` | Stop conditions that must remain attached. |
| `limitations` | Uncertainty and restricted-use statements. |

Agent task metadata is not execution approval. Agent handoff metadata is not handoff execution approval.

## 8. Agent Runtime Classification Model
| Classification | Examples | Allowed AL-1 agent use | Blocked use | Required gate |
| --- | --- | --- | --- | --- |
| `agent_metadata` | Agent descriptors and runtime refs. | Metadata citation, safe summary, blocker retention. | Agent activation, runtime readiness inference. | GT-06 for runtime activation. |
| `agent_capability_metadata` | Capability refs and capability summaries. | Describe possible future capabilities and blockers. | Runtime capability activation, tool/provider/product use. | GT-06 plus GT-07/GT-08/GT-09 as applicable. |
| `agent_task_metadata` | Task records and proposed work items. | Proposed or blocked work description. | Task execution, source loading, tool/provider calls. | Runtime and relevant action gates. |
| `agent_instruction_metadata` | Instruction scope and forbidden-use records. | Bound instruction metadata to allowed/forbidden scope. | Bypass instructions, self-approval, secret-bearing instructions. | Governance/security review. |
| `agent_plan_metadata` | Plan summaries and dependencies. | Planning evidence with limitations. | Treating a plan as execution approval. | Runtime/tool/provider/product gates as applicable. |
| `agent_handoff_metadata` | Handoff records and reason metadata. | Preserve handoff intent, sensitivity, blockers, and limitations. | Handoff execution, context leakage, blocker removal. | Runtime and handoff approval route. |
| `agent_approval_metadata` | Approval refs, requested approvals, blocked approvals. | Record approval posture and required gates. | Self-granted approval, overriding security/validation. | Accepted governance route. |
| `dormant_runtime_config_ref` | Inactive runtime config reference or runtime candidate. | Safe metadata marker with blockers. | Runtime startup, daemon, queue, scheduler, worker. | GT-06, GT-13, GT-15. |
| `tool_bound_agent_intent` | Agent task that would need a tool. | Mark GT-07 blocker and exact future requirements. | Tool execution, shell/subprocess, filesystem/network/Git action. | GT-07 plus security/validation review. |
| `provider_bound_agent_intent` | Agent task that would need provider/API/MCP/auth. | Mark GT-08 blocker and credential/auth posture. | Provider calls, auth, network, MCP activation, context transmission. | GT-08 plus security/validation review. |
| `product_bound_agent_action` | Agent action involving Siamese product source, product outputs, or product behavior. | Product readiness metadata only. | Product source inspection, execution, activation, product Git posture change. | GT-09 plus security/validation/source tracking review. |
| `generated_agent_output` | Agent summary, plan, draft, proposed output. | Generated evidence with limitations and retention posture. | Authority, publication, raw source inclusion, next-action approval. | GT-04/GT-05/GT-12/GT-15 as applicable. |
| `generated_graphify_evidence` | Curated Graphify Repo Map Summary. | Supporting curated generated evidence only. | Raw output promotion, Graphify authority, substrate selection. | GT-04/GT-11/GT-12/GT-08 if rerun/provider/tracking. |
| `runtime_state` | Logs, caches, process state, state stores. | Excluded by default; safe metadata only if scoped. | Runtime inspection, persistence, publication, authority. | GT-06/GT-13/GT-15. |
| `credential_reference` | Redacted credential need metadata. | Blocked marker only. | Credential values, auth, testing, context inclusion, publication. | GT-08 plus secure approval. |
| `secret_value` | API key, password, token, private key. | None. | Any exposure, summary, transform, validation, retention. | Secure incident route and GT-15. |
| `provider_auth_material` | OAuth sessions, browser auth, token stores, provider configs. | None by default; safe category only if explicitly scoped. | Inspection, auth, provider call, context transmission. | GT-08 plus secure approval. |
| `local_only_source` | Previous knowledge, datasets, models, artifacts, logs. | Excluded by default; safe metadata only if scoped. | Raw content loading, context dump, publication. | GT-01/GT-05 and exact review gate. |
| `product_restricted_source` | Siamese product source or product-generated output. | Product readiness gate metadata only. | Product source loading, product execution, tracking, activation. | GT-09 plus security/validation/source tracking review. |
| `external_source` | Raw external source, external instructions, external examples. | External metadata only when scoped. | Raw source copying, execution, instruction adoption. | GT-11 plus security/license review. |
| `unknown_sensitivity` | Unclassified path, mixed source, unclear artifact. | Exclude or mark blocked. | Inclusion as safe agent metadata or execution-ready input. | GT-01 and security review. |

## 9. Agent Boundary Rules
| Rule | Required behavior |
| --- | --- |
| Record only metadata-approved agent runtime boundary information. | Include only records whose metadata posture is in scope. |
| Preserve source classification. | Do not collapse governance, implementation, generated, product, external, local-only, secret, credential, or unknown classes. |
| Preserve sensitivity. | Agent records inherit highest sensitivity or stricter. |
| Preserve local-only flags. | Local-only status must travel with refs, tasks, handoffs, approvals, outputs, and retention records. |
| Preserve generated-output flags. | Generated outputs remain generated-sensitive unless curated and governed. |
| Preserve product/external/secret/credential blockers. | Blockers cannot be stripped during task, plan, handoff, or output handling. |
| Include limitations. | Every record with uncertainty must carry limitations downstream. |
| Include evidence refs. | Evidence refs are metadata references, not copied source contents. |
| Include security refs. | Security refs constrain use and must be treated as blockers when restrictive. |
| Include validation refs. | Validation refs record posture only; they do not approve action. |
| Never convert agent refs into runtime activation permission. | Agent refs are metadata. |
| Never convert agent task records into execution approval. | Agent task metadata is not execution approval. |
| Never convert agent handoff records into handoff execution approval. | Agent handoff metadata is not handoff execution approval. |
| Never convert agent capability refs into active runtime capabilities. | Capability metadata is not runtime capability activation. |
| Never include secrets or credentials in agent instructions, context, task records, handoff records, or outputs. | Secrets and credentials are never agent content. |
| Never include product source unless GT-09 approves exact scope. | Product source remains blocked by default. |
| Never call providers unless GT-08 approves exact scope. | Provider/auth is blocked by default. |
| Never execute tools unless GT-07 approves exact scope. | Tool execution is blocked by default. |
| Never treat Graphify summary as truth. | Graphify evidence is supporting generated evidence only, not authority. |
| Never treat generated agent output as authority. | Agent output is generated evidence unless accepted by governance. |
| Never use agent metadata to bypass source tracking. | GT-02 and GT-12 still govern tracking, staging, commit, push, force-add, and publication. |
| Never use agent metadata to bypass security review. | Security blockers remain binding. |
| Never use agent metadata to bypass validation posture. | Validation evaluates; governance decides. |

## 10. Agent Activation Rules
| Activation rule | Required posture |
| --- | --- |
| Agent runtime remains inactive at AL-1. | AGENT PLATFORM remains pre-active at AL-1 metadata skeleton. |
| Agent runtime activation requires the accepted agent runtime activation gate. | Future runtime activation must cite GT-06, security posture, validation posture, rollback, and exact scope. |
| Agent execution requires explicit governance approval. | Security posture, validation posture, allowed input scope, allowed output scope, retention posture, and rollback posture are required. |
| Agent task execution must never be inferred from task metadata. | Task records remain proposed, blocked, deferred, or metadata-only. |
| Agent handoff execution must never be inferred from handoff metadata. | Handoff records preserve intent and blockers only. |
| Agent approval metadata must preserve approval status and cannot self-approve. | Approval requires accepted governance route and owner. |
| Agent runtime must not activate provider/auth through metadata. | Provider/auth for agents requires GT-08. |
| Agent runtime must not activate tool execution through metadata. | Tool use from agents requires GT-07. |
| Agent runtime must not activate product behavior through metadata. | Product-bound agent action requires GT-09. |
| Agent runtime must not activate Cognitive Semantic System substrate selection through metadata. | Cognitive Semantic System substrate remains deferred. |

## 11. Agent Task Status Model
No P1.4 status value may imply actual execution.

| Status | Meaning | Execution implication |
| --- | --- | --- |
| `proposed_metadata_only` | Proposed task or handoff exists as metadata. | None. |
| `blocked_by_security` | Security blocker prevents readiness. | None. |
| `blocked_by_validation` | Validation posture or evidence is missing. | None. |
| `blocked_by_governance` | Governance approval is missing or scope is not accepted. | None. |
| `blocked_by_missing_approval` | Required approval gate is absent. | None. |
| `blocked_by_tool_gate` | Tool use would require GT-07. | None. |
| `blocked_by_provider_gate` | Provider/auth/network/MCP would require GT-08. | None. |
| `blocked_by_product_gate` | Product source, output, or behavior would require GT-09. | None. |
| `deferred` | Future review may reconsider. | None. |
| `rejected` | Scope is rejected, unsafe, broad, or premature. | None. |
| `approved_metadata_only` | Metadata record is acceptable for documentation use only. | None. |
| `approved_for_future_execution_gate_review` | Record may be reviewed by a future execution gate. | None. |
| `executed_out_of_scope_for_p1_4_prohibited` | Marker for incident classification if execution occurred outside P1.4 scope. | Prohibited; not a valid P1.4 action. |

## 12. Agent Approval Contract
Approval records are metadata unless the accepted governance route explicitly grants approval.

| Field | Required meaning |
| --- | --- |
| `approval_ref_id` | Stable metadata identifier for the approval record. |
| `approval_subject` | Agent, task, handoff, output, provider use, tool use, context use, or product-bound action under review. |
| `approval_scope` | Exact scope of the approval metadata. |
| `approval_owner` | Human/governance owner; missing owner blocks approval. |
| `approval_status` | Draft, requested, blocked, rejected, approved metadata only, approved for exact scope, superseded, or retired. |
| `approval_gate` | Required gate such as GT-06, GT-07, GT-08, GT-09, GT-12, or GT-15. |
| `approval_date` | Date of approval metadata, or `none` when not granted. |
| `allowed_actions` | Exact allowed actions if a governance record explicitly grants them. |
| `forbidden_actions` | Actions still forbidden, including runtime activation, task execution, handoff execution, tool execution, provider/auth, product access, source loading, and publication unless exact gate says otherwise. |
| `security_refs` | Security posture and blockers. |
| `validation_refs` | Validation posture and blockers. |
| `evidence_refs` | Evidence supporting the approval posture. |
| `rollback_refs` | Rollback and incident posture refs. |
| `retention_posture` | Retention, redaction, quarantine, deletion, and publication posture. |
| `review_required` | Required review state. |
| `blockers` | Blocking conditions that cannot be bypassed by approval metadata. |
| `limitations` | Restricted-use statements and uncertainty. |

Approval metadata must not be self-granted by an agent. Approval metadata must not override security blockers. Approval metadata must not override validation blockers. Approval metadata must not override product/source/provider/tool gates.

## 13. Agent / Context Interface
Agent metadata may reference context packs. Context pack reference is not source loading permission.

| Rule | Contract consequence |
| --- | --- |
| Context inclusion is not permission for agents. | Agents cannot execute tools, call providers, inspect sources, or publish because context exists. |
| Context availability is not permission to act. | Context refs must preserve sensitivity, blockers, source classification, local-only posture, generated-output posture, product posture, external posture, and retention posture. |
| Agents must consume context blockers as blockers, not permissions. | Restrictive context security refs remain binding. |
| Agent tasks must not silently include product, external, secrets, or generated raw outputs. | Such refs must be excluded or marked blocked. |
| Agent handoff must preserve context sensitivity and blockers. | Handoff records must carry evidence refs, security refs, validation refs, limitations, and retention posture. |

## 14. Agent / Security Interface
Security constrains agent runtime refs, task records, handoff records, instruction records, context refs, tool refs, provider refs, generated outputs, retention, and publication.

| Security rule | Agent contract consequence |
| --- | --- |
| Unknown sensitivity blocks agent inclusion and execution readiness. | Unknown or mixed sensitivity must be excluded or marked blocked. |
| Secrets and credentials are never agent content. | Values, partial values, hashes, fingerprints, examples from real values, and transformed values are prohibited. |
| Provider auth material is never agent content. | API keys, tokens, cookies, OAuth data, endpoint credentials, provider configs, and auth material are prohibited. |
| Product source remains blocked. | Product context and product-bound agent action require GT-09 and security review. |
| External source remains blocked unless scoped. | External metadata may be cited; raw source remains excluded by default. |
| Generated output remains local-only unless curated. | Generated artifacts are not agent authority. |
| Agent runtime must consume security refs as blockers, not permissions. | Security refs can constrain or block; they cannot grant runtime access by themselves. |
| Security blockers cannot be overridden by agent task metadata. | Task metadata cannot convert a blocked action into approved execution. |

## 15. Agent / Validation Interface
Validation may evaluate agent metadata completeness in the future. Validation may evaluate agent boundary invariants in the future. Validation may evaluate proposed execution readiness in the future.

| Validation rule | Agent contract consequence |
| --- | --- |
| Validation cannot approve agent runtime activation. | Runtime activation remains governed by GT-06 and accepted governance route. |
| Validation cannot approve agent task execution. | Task execution remains blocked unless future exact gate approves. |
| Validation cannot approve agent handoff execution. | Handoff execution remains blocked unless future exact gate approves. |
| Validation cannot approve context source loading. | Source loading still requires relevant source, context, security, and product gates. |
| Validation cannot approve provider/auth. | Provider/auth for agents requires GT-08. |
| Validation cannot approve tool execution. | Tool use from agents requires GT-07. |
| Validation evidence must cite GT-04. | Future validation execution must cite exact gate, command, input, output, retention, and stop rules. |
| Validation evaluates; governance decides. | No validation status activates agent runtime or approves execution. |

## 16. Agent / Provider Interface
Agent provider refs may describe provider metadata needs, but provider/auth is not approved.

| Provider rule | Agent contract consequence |
| --- | --- |
| Agent runtime must not contain provider secrets, API keys, tokens, endpoint credentials, or auth material. | Provider refs and credential refs are metadata only. |
| Provider-bound agent execution requires GT-08 and security review. | Auth, network, MCP, provider calls, cost, data exposure, and retention must be reviewed. |
| Provider-bound context transmission requires GT-08 and security review. | Context cannot be transmitted by agent/provider metadata reference alone. |
| Provider summaries are generated evidence, not authority. | Generated provider summaries need evidence refs, limitations, security refs, validation refs, and retention posture. |
| Provider availability is not provider execution permission. | Provider metadata cannot authorize task execution, tool execution, auth, network, MCP, or context transmission. |

Provider/auth for agents requires GT-08.

## 17. Agent / Tool Interface
Agent tool refs may describe required or candidate tools, but tool execution is not approved.

| Tool rule | Agent contract consequence |
| --- | --- |
| Tool use from agents requires GT-07. | Exact command/action, cwd, inputs, outputs, side effects, rollback, and sensitivity handling are required before execution. |
| Agent metadata does not authorize tool inputs. | Tool input construction from agent metadata requires future GT-07 posture. |
| Agent-derived tool requests require GT-07, security review, validation posture, input scope, output scope, and retention posture. | Request records remain metadata until exact scope is approved. |
| Tool output into agent context requires generated-output classification, validation/security review, and retention posture. | Tool output cannot enter agent context as authority by default. |
| Tool availability is not tool execution permission. | Tool refs cannot authorize shell, subprocess, filesystem, network, package, build, test, Git, or MCP actions. |

## 18. Agent / Cognitive Semantic System Interface
Cognitive Semantic System may reference agent metadata as evidence or claim support.

| Cognitive Semantic System rule | Agent contract consequence |
| --- | --- |
| Agent evidence is not truth by default. | Semantic records require evidence, validation, security refs, blockers, and limitations. |
| Agent output is generated evidence, not authority. | Agent output cannot become truth through semantic inclusion. |
| Agent metadata cannot select substrate. | Cognitive Semantic System substrate remains deferred. |
| Graph remains candidate only. | Agent-derived graph or semantic records cannot choose graph as final substrate. |
| Agent-derived semantic records require evidence, validation, and security refs. | Records must preserve agent source classification, sensitivity, blockers, and limitations. |
| Cognitive Semantic System records must preserve agent source classification, sensitivity, blockers, and limitations. | Semantic records cannot strip local-only, product, external, generated-output, secret, credential, provider, tool, or validation blockers. |

Rejected/prohibited/historical examples only: `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth`. No such string is accepted as a current AGENT PLATFORM or Cognitive Semantic System name.

## 19. Agent / Graphify Interface
Graphify repo map summary is curated generated evidence only.

| Graphify rule | Agent contract consequence |
| --- | --- |
| Raw Graphify output under `9_artifacts/` is local-only. | Raw graph files, visuals, labels, and generated artifacts are excluded by default. |
| Graphify labels are not agent roles. | Generated labels cannot define runtime agent roles. |
| Graphify labels are not governance labels. | Generated labels cannot approve architecture, authority, or governance status. |
| Graphify evidence cannot approve agent execution. | Agent runtime and task execution require future gates. |
| Graphify evidence cannot approve source loading. | Context/source gates remain required. |
| Graphify evidence cannot approve provider/auth. | GT-08 remains required. |
| Graphify evidence cannot approve tool execution. | GT-07 remains required. |
| `.graphifyignore` constrains Graphify input but is not permission. | It is input hygiene, not source approval, security approval, or rerun permission. |
| Agent metadata may reference curated Graphify summaries, not raw outputs by default. | Graphify evidence remains generated, local-only/supporting, and limited. |
| Graphify evidence cannot become authority through agent metadata inclusion. | Governance decisions override generated projections. |

Graphify evidence is supporting generated evidence only, not authority.

## 20. Agent / Siamese Product Interface
Siamese is product vision, not product activation.

| Product rule | Agent contract consequence |
| --- | --- |
| Product source cannot be loaded into agent context by default. | Product source remains product-restricted and local-only. |
| Product-bound agent action requires GT-09. | Security review, validation posture, source tracking posture, and rollback are required. |
| Product readiness planning may reference product gate requirements. | Readiness records may list blockers and future gate prerequisites. |
| Omniverse/EnergyPlus planning remains readiness-only. | Native/domain execution, product dependencies, product adapters, and generated outputs remain blocked. |
| Product agent context requires GT-09, security review, validation posture, source tracking posture, and rollback. | Product-derived context cannot define root AGENT PLATFORM authority. |
| Agent runtime metadata must not activate product behavior. | Product activation remains a future exact governance decision. |

## 21. Agent Input / Output Contract
| Contract area | Rule |
| --- | --- |
| Agent inputs | Agent inputs are metadata refs, not raw source loading approval. |
| Agent outputs | Agent outputs are generated evidence unless explicitly curated by governance. |
| Source classification | Agent outputs must preserve source classification. |
| Sensitivity | Agent outputs must preserve sensitivity. |
| Blockers | Agent outputs must preserve local-only, generated-output, product, external, secret, and credential blockers. |
| Validation refs | Agent outputs must include validation refs when evaluated. |
| Security refs | Agent outputs must include security refs when constrained. |
| Limitations | Agent outputs must include limitations. |
| Retention posture | Agent outputs must include retention posture. |
| Publication | Agent outputs must not be published if publication blockers exist. |
| Authority boundary | Agent outputs must not become authority through inclusion in context, Graphify, or Cognitive Semantic System records. |

## 22. Agent Retention And Output Handling
| Retention area | Contract rule |
| --- | --- |
| Agent runtime metadata retention posture | Retain metadata fields, blockers, limitations, evidence refs, validation refs, security refs, and review posture only. |
| Agent task record retention posture | Retain proposed action metadata, gate requirements, blockers, limitations, and status; never retain executable payloads or secret material. |
| Agent handoff record retention posture | Retain handoff reason, source/target refs, context refs, blockers, limitations, and sensitivity posture. |
| Agent approval record retention posture | Retain approval metadata, owner, scope, gate, allowed/forbidden actions, security refs, validation refs, rollback refs, limitations, and blockers. |
| Agent generated output retention posture | Treat as generated-sensitive unless curated by a future gate; preserve evidence refs and limitations. |
| Local-only retention posture | Local-only material remains excluded by default; safe metadata only when exact future scope allows. |
| Redaction rules | Omit unsafe content entirely; do not reveal partial secrets, hashes, fingerprints, prefixes, suffixes, or transformed credential values. |
| Deletion/quarantine triggers | Forbidden material, secret/credential exposure, product source inclusion, raw external inclusion, raw generated-output inclusion, unknown sensitivity, or unapproved local-only material triggers quarantine/removal review. |
| Publication blockers | Local-only, generated-sensitive, product, external, secret, credential, unknown, unreviewed, provider-auth-related, or tool-execution-related material blocks publication. |
| Source tracking requirements | GT-02 and GT-12 are required before tracking agent metadata derivatives, generated summaries, curated outputs, staging, commit, push, force-add, or publication. |
| Incident response if agent metadata includes forbidden material | STOP, avoid repeating content, report safe metadata only, preserve evidence refs, quarantine/remove through governance/security route. |
| Incident response if agent task metadata attempts to bypass gates | STOP, mark blocker, retain safe metadata, require governance/security/validation review. |
| Incident response if agent output includes secrets, credentials, product source, external source, or raw generated output | STOP, do not publish or include in context, report safe category only, quarantine/remove through incident route and GT-15. |

## 23. Agent Runtime Contract Invariants
| ID | Invariant |
| --- | --- |
| AGT-001 | Agent runtime boundary contract hardening is not agent runtime activation. |
| AGT-002 | Agent runtime refs are metadata. |
| AGT-003 | Agent metadata is not permission to act. |
| AGT-004 | Agent task metadata is not execution approval. |
| AGT-005 | Agent handoff metadata is not handoff execution approval. |
| AGT-006 | Agent capability metadata is not runtime capability activation. |
| AGT-007 | No agent execution is approved by P1.4. |
| AGT-008 | AGENT PLATFORM remains pre-active at AL-1. |
| AGT-009 | Context inclusion is not permission for agents. |
| AGT-010 | Tool use from agents requires GT-07. |
| AGT-011 | Provider/auth for agents requires GT-08. |
| AGT-012 | Product-bound agent action requires GT-09. |
| AGT-013 | Secrets and credentials are never agent content. |
| AGT-014 | Validation evaluates; governance decides. |
| AGT-015 | Cognitive Semantic System substrate remains deferred. |
| AGT-016 | Graphify evidence is supporting evidence only, not authority. |
| AGT-017 | Agent outputs are generated evidence, not authority by default. |
| AGT-018 | Approval refs are not approval unless accepted governance records explicitly grant approval. |
| AGT-019 | Agent metadata cannot bypass source tracking posture. |
| AGT-020 | Agent metadata cannot bypass security blockers. |

## 24. Future Validation Targets
These are future validation targets only. P1.4 does not execute validation.

| Future validation target | Purpose | Required future gate |
| --- | --- | --- |
| agent runtime required fields completeness | Check required AgentRuntimeBoundary and AgentRuntimeRef fields. | GT-04 |
| agent ref sensitivity propagation | Check sensitivity carries into tasks, handoffs, approvals, and outputs. | GT-04 plus GT-05 if sensitive |
| agent task blocker preservation | Check task records retain security, validation, tool, provider, product, source, and retention blockers. | GT-04 |
| agent handoff blocker preservation | Check handoff records preserve context sensitivity and downstream blockers. | GT-04 |
| agent approval metadata completeness | Check approval fields, owner, scope, gate, allowed/forbidden actions, blockers, and limitations. | GT-04 |
| no-agent-execution invariant | Check P1.4 records do not imply execution. | GT-04 plus GT-06 if runtime requested |
| no-secret/no-credential agent invariant | Check metadata records prohibit secret/credential content. | GT-04 plus GT-05; no secret scanning by value |
| provider-bound agent blocker invariant | Check provider-bound agent refs require GT-08 and security review. | GT-04 plus GT-08 |
| tool-bound agent blocker invariant | Check tool-bound agent refs require GT-07 and security review. | GT-04 plus GT-07 |
| product-bound agent blocker invariant | Check product-bound actions remain blocked until GT-09. | GT-04 plus GT-09 |
| context-to-agent blocker invariant | Check context refs remain metadata and preserve context blockers. | GT-04 plus GT-05 if sensitive |
| agent output generated-evidence invariant | Check outputs remain generated evidence unless curated by governance. | GT-04 plus GT-12/GT-15 if tracking/publication requested |
| Graphify evidence boundary invariant | Check Graphify evidence remains supporting generated evidence only. | GT-04/GT-11 |
| Cognitive Semantic System substrate-deferred invariant | Check agent metadata cannot select substrate. | GT-04 plus GT-10/GT-13 if substrate/state requested |
| source tracking posture invariant | Check agent metadata does not approve tracking, staging, commit, push, force-add, or publication. | GT-04 plus GT-12 if tracking requested |
| retention posture invariant | Check agent records include retention, redaction, quarantine, publication blockers, and incident route. | GT-04 plus GT-15 |

## 25. Future Hardening Candidates
These are future candidates only and are not started by P1.4.

| Candidate ticket | Purpose | P1.4 status |
| --- | --- | --- |
| AGT-HARD-01 - Agent Runtime Ref Schema Alignment | Align AgentRuntimeRef fields across context, validation, security, tool, provider, Cognitive Semantic System, Graphify, and product-readiness records. | Not started. |
| AGT-HARD-02 - Agent Task / Handoff Metadata Contract | Harden task and handoff fields, blocker propagation, source posture, and review states. | Not started. |
| AGT-HARD-03 - Agent Approval / Rollback Contract | Harden approval metadata, rollback refs, incident routing, and non-self-approval semantics. | Not started. |
| AGT-HARD-04 - Agent Capability / Tool / Provider Boundary Model | Refine capability refs and tool/provider gate inheritance. | Not started. |
| AGT-HARD-05 - Agent Output Retention & Redaction Contract | Define generated agent output retention, redaction, quarantine, publication blockers, and tracking posture. | Not started. |

## 26. Created / Not Created Register
| Artifact or action | P1.4 status |
| --- | --- |
| Agent runtime boundary contract hardening document | Created. |
| `0_architecture/governance/agent_platform_agent_runtime_boundary_contract_hardening.md` | Created. |
| Agent runtime code | Not modified. |
| Agent runtime | Not activated. |
| Agent task | Not executed. |
| Agent handoff | Not executed. |
| Approval workflow | Not activated. |
| Source loading | Not approved. |
| Product source | Not inspected. |
| External source | Not inspected. |
| Secrets | Not inspected. |
| Credentials | Not inspected. |
| Provider/auth | Not configured. |
| Tool execution | Not approved. |
| Validation command | Not executed. |
| Graphify | Not rerun. |
| `.graphifyignore` | Not modified. |
| `.gitignore` | Not modified. |
| Generated outputs | Not modified or tracked. |
| Cognitive Semantic System substrate | Not selected. |
| P1.5 | Not started. |
| P2.1 | Not started. |
| Git staging/commit/push/force-add/publication | Not authorized or performed. |

## 27. Recommended Next Tickets
After P1.4:

| Ticket | Recommendation |
| --- | --- |
| P1.5 - Cognitive Semantic System Prototype Hardening | Recommended actual next ticket after explicit instruction. |
| P2.1 - Shared Metadata Vocabulary Alignment | Follow after enough P1 contracts exist. |

Recommended actual: P1.5 - Cognitive Semantic System Prototype Hardening.

Do not start P1.5. Do not start P2.1.

## 28. Final Verdict
| Question | Answer |
| --- | --- |
| What did P1.4 create? | The canonical Agent Runtime Boundary Contract Hardening document. |
| What agent runtime boundary contract was hardened? | AgentRuntimeBoundary, AgentRuntimeRef, AgentCapabilityRef, AgentTaskRecord, AgentInstructionRecord, AgentPlanRecord, AgentHandoffRecord, AgentApprovalRecord, AgentExecutionIntent, AgentExecutionBlocker, AgentContextRef, AgentToolRef, AgentProviderRef, AgentEvidenceRef, AgentValidationRef, AgentSecurityRef, AgentOutputRef, AgentRetentionRecord, and AgentLimitation metadata contracts. |
| What agent runtime ref fields are required? | `agent_ref_id`, `agent_name_or_identifier`, `agent_family`, `runtime_scope`, `activation_level`, `execution_status`, `capability_refs`, `task_refs`, `handoff_refs`, `context_refs`, `tool_refs`, `provider_refs`, `approval_refs`, `validation_refs`, `security_refs`, `evidence_refs`, `input_contract_refs`, `output_contract_refs`, `handoff_contract_refs`, `source_classification`, `sensitivity`, `local_only`, `product_related`, `external_related`, `generated_output_related`, `credential_related`, `secret_related`, `allowed_use`, `forbidden_use`, `tracking_posture`, `retention_posture`, `review_required`, `blockers`, and `limitations`. |
| What agent task and handoff metadata fields are required? | `agent_task_id`, `agent_handoff_id`, `requested_action`, `request_owner`, `agent_role`, `agent_capability_refs`, `input_refs`, `output_refs`, `context_refs`, `tool_refs`, `provider_refs`, `required_approval_gate`, `required_tool_gate`, `required_provider_gate`, `required_product_gate`, `validation_requirements`, `security_requirements`, `source_tracking_posture`, `product_scope`, `execution_status`, `handoff_source`, `handoff_target`, `handoff_reason`, `rollback_posture`, `retention_posture`, `review_required`, `blockers`, and `limitations`. |
| What agent classifications are defined? | Agent metadata, capability metadata, task metadata, instruction metadata, plan metadata, handoff metadata, approval metadata, dormant runtime config refs, tool-bound intent, provider-bound intent, product-bound action, generated agent output, generated Graphify evidence, runtime state, credential reference, secret value, provider auth material, local-only source, product-restricted source, external source, and unknown sensitivity. |
| What interfaces were hardened? | Agent/context, agent/security, agent/validation, agent/provider, agent/tool, agent/Cognitive Semantic System, agent/Graphify, and agent/Siamese product interfaces. |
| Did P1.4 activate agent runtime? | No. Agent runtime boundary contract hardening is not agent runtime activation. |
| Did P1.4 execute agent tasks? | No. Agent task metadata is not execution approval. |
| Did P1.4 execute agent handoffs? | No. Agent handoff metadata is not handoff execution approval. |
| Did P1.4 modify runtime code? | No. |
| Was provider/auth configured? | No. Provider/auth for agents requires GT-08. |
| Was product source inspected? | No. Product-bound agent action requires GT-09. |
| Was tool execution approved? | No. Tool use from agents requires GT-07. |
| Was Cognitive Semantic System substrate selected? | No. Cognitive Semantic System substrate remains deferred. |
| What is the next ticket? | P1.5 - Cognitive Semantic System Prototype Hardening, after explicit instruction only. |

Stop rule: After completing P1.4, STOP. Do not start P1.5. Do not start P2.1. Do not implement code. Do not run validation. Do not inspect secrets. Do not configure provider/auth. Do not load source. Do not execute tools. Do not activate agents. Do not execute agent tasks. Do not execute agent handoffs. Do not rerun Graphify. Do not modify generated outputs. Do not stage, commit, push, force-add, or publish.
