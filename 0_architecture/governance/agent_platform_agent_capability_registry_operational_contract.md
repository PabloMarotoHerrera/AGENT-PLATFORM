# Agent Registry / Capability Registry Operational Contract

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | Agent Registry / Capability Registry Operational Contract |
| Ticket | P6.1 |
| Status | Accepted Agent Registry / Capability Registry operational contract |
| Date | 2026-07-05 |
| Scope | Metadata-only operational registry contract for AGENT PLATFORM / Siamese. |
| Authority | Metadata-only operational registry contract, not registry runtime, agent registration runtime, capability activation, agent execution, task execution, handoff execution, scheduler activation, orchestration activation, autonomous loop activation, tool execution, provider/auth/API/MCP activation, live connector activation, validation execution, source loading, source inspection, security enforcement activation, product activation, Graphify adoption, Codegraph execution, GBrain/Hermes/Cadence activation, persistence/database/event streaming, telemetry, vector DB implementation, graph DB implementation, generated output tracking, source tracking expansion, Cognitive Semantic System substrate selection, or publication. |
| Related documents | P5.R, P5.1, P5.2, P5.3, P5.4, P5.5, P5.6, P5.7, P3.BR, P3.3, P3.4, P3.5, P2.1, P2.2, P2.3, P1.4, P1.3, P1.2, P1.1, P1.5, P0.1, P0.2, P0.3, S-03, S-04, CSS ADR/audit. |
| Optional sibling inputs | P6.2, P6.3, P6.4, P6.5, and P6.6 are not yet available by path-only check and are future consumers only. |
| Output | Agent Registry / Capability Registry operational contract |

Operational planning is not activation. Registry is not runtime. Capability metadata is not capability execution. Agent metadata is not agent execution.

## 2. Purpose

P6 creates operational contracts, not active operations. P6.1 defines who and what can exist as metadata in an Agent Registry / Capability Registry.

P6.1 establishes metadata records for agents, capabilities, dependencies, boundaries, and runtime eligibility. P6.1 consumes P5.R and P5 skeletons as baseline evidence, P3-B activation decisions as activation posture, P2.1 vocabulary, P2.2 EvidenceRef, P2.3 audit/retention/rollback baseline, and P1 context/provider/tool/agent/Cognitive Semantic System boundaries.

P6.1 does not register live agents. P6.1 has no agent registration runtime. P6.1 has no registry runtime. P6.1 has no capability activation. P6.1 does not create registry runtime. P6.1 does not start P6.2, P6.3, P6.4, P6.5, P6.6, or P6.7.

## 3. Current Posture

| Area | Current state | P6.1 interpretation | Blocked interpretation |
| --- | --- | --- | --- |
| AGENT PLATFORM activation level | AL-1 metadata skeleton. | Operational registry can be specified as metadata contract. | Runtime activation. |
| P5.R skeleton audit | Present by path-only check. | Baseline audit evidence for registry metadata. | Audit is not activation. |
| P5.6 agent task/handoff skeleton | Present by path-only check. | Agent task and handoff capability metadata source. | Active agent runtime. |
| P5.4 tool sandbox skeleton | Present by path-only check. | Tool capability metadata source. | Active tool capability. |
| P5.5 provider adapter skeleton | Present by path-only check. | Provider capability metadata source. | Active provider capability. |
| P5.3 context assembly skeleton | Present by path-only check. | Context capability metadata source. | Source loading or context permission. |
| P5.7 audit/retention/rollback hooks | Present by path-only check. | Audit metadata capability source. | Persistence or event store. |
| P3.5 agent runtime decision | Present by path-only check. | Agent runtime remains constrained. | Agent execution. |
| P3.3 tool execution decision | Present by path-only check. | Tool execution remains constrained. | Tool execution. |
| P3.4 provider/auth/API/MCP decision | Present by path-only check. | Provider and MCP capabilities remain constrained. | Provider/API/MCP activation. |
| Agent Registry | Metadata contract only. | AgentRegistryRecord may exist as documentation-governance object. | live agent registry, runtime registry, registry daemon. |
| Capability Registry | Metadata contract only. | AgentCapabilityRecord may exist as documentation-governance object. | active capability or executable capability. |
| runtime eligibility | Metadata future-review posture. | RuntimeEligibilityRecord can state blockers and gates. | Runtime approval. |
| context capability | Metadata-only candidate. | Context refs only. | Source loading. |
| validation capability | Metadata-only skeleton. | Validation refs only. | Validation execution. |
| security dry-run capability | Metadata-only dry-run posture. | Security refs only. | Security enforcement. |
| tool metadata capability | Metadata-only. | ToolCapabilityRef only. | Tool execution. |
| provider metadata capability | Metadata-only. | ProviderCapabilityRef only. | Provider/auth/API/MCP activation. |
| task envelope capability | Metadata-only. | Agent task envelopes only. | Task execution active. |
| handoff metadata capability | Metadata-only. | Handoff envelope metadata only. | Handoff execution active. |
| audit metadata capability | Metadata-only. | Audit refs only. | Persistence or telemetry. |
| approval metadata capability | Metadata-only. | HumanApprovalCapabilityRef only. | active approval workflow. |
| monitoring metadata capability | Metadata-only. | Future P6.5 consumer. | active monitoring. |
| incident metadata capability | Metadata-only. | Incident refs only. | Incident automation. |
| executable capabilities | Blocked. | Must remain blockers until future exact activation review. | Executable capability by registry presence. |
| autonomous capabilities | Blocked. | No scheduler/orchestration/autonomous loop. | autonomous capability. |
| product-bound capabilities | Blocked until P4/GT-09. | Siamese remains product vision. | active product capability. |
| GBrain/Hermes/Cadence capabilities | Blocked / future inactive. | GBrain / Hermes / Cadence remain future and inactive. | active GBrain capability, active Hermes capability, active Cadence capability. |

AGENT PLATFORM remains AL-1 metadata skeleton. P6.1 is operational contract only. Registry is not runtime. Capability metadata is not capability execution. No agent/capability is live by P6.1.

## 4. Inputs Reviewed

| Input group | Document | Review mode | Registry use | Limitation |
| --- | --- | --- | --- | --- |
| P5.R audit | `agent_platform_minimal_active_agent_platform_audit.md` | governance_markdown_review | Baseline audit reference. | No activation inferred. |
| P5.1 validation runner skeleton | `agent_platform_validation_runner_minimal_implementation.md` | implementation_skeleton_review | Validation capability metadata. | No validation execution. |
| P5.2 security dry-run skeleton | `agent_platform_security_policy_dry_run_candidate.md` | implementation_skeleton_review | Security dry-run capability metadata. | No enforcement activation. |
| P5.3 context assembly skeleton | `agent_platform_context_assembly_runtime_candidate.md` | implementation_skeleton_review | Context capability metadata. | No source loading. |
| P5.4 tool sandbox skeleton | `agent_platform_tool_execution_sandbox_allowlist_candidate.md` | implementation_skeleton_review | Tool metadata capability. | No tool execution. |
| P5.5 provider adapter skeleton | `agent_platform_provider_adapter_runtime_candidate.md` | implementation_skeleton_review | Provider metadata capability. | No provider/API/MCP activation. |
| P5.6 agent task/handoff skeleton | `agent_platform_agent_task_runtime_handoff_candidate.md` | implementation_skeleton_review | Agent/task/handoff metadata. | No agent, task, or handoff execution. |
| P5.7 audit/retention/rollback hooks | `agent_platform_audit_retention_rollback_runtime_hooks.md` | implementation_skeleton_review | Audit/retention/rollback metadata. | No persistence or automation. |
| P3.3 tool execution decision | `agent_platform_tool_execution_activation_decision.md` | activation_decision_review | Tool capability constraint. | Deferred decisions remain deferred. |
| P3.4 provider/auth decision | `agent_platform_provider_auth_api_mcp_activation_decision.md` | activation_decision_review | Provider/MCP capability constraint. | Provider activation not inferred. |
| P3.5 agent runtime decision | `agent_platform_agent_runtime_activation_decision.md` | activation_decision_review | Agent capability constraint. | Agent execution not inferred. |
| P2.1 vocabulary | `agent_platform_shared_metadata_vocabulary_alignment.md` | metadata_contract_review | Naming alignment. | No runtime schema. |
| P2.2 EvidenceRef | `agent_platform_cross_lane_evidence_reference_contract.md` | metadata_contract_review | Evidence refs. | Evidence supports; it does not decide. |
| P2.3 audit/retention/rollback | `agent_platform_audit_retention_rollback_baseline.md` | metadata_contract_review | Retention, rollback, incident posture. | No automation. |
| P1.1 context boundary | `agent_platform_context_runtime_contract_hardening.md` | metadata_contract_review | Context boundary. | Context inclusion is not permission. |
| P1.2 provider boundary | `agent_platform_provider_adapter_metadata_contract_hardening.md` | metadata_contract_review | Provider boundary. | Provider metadata is not provider activation. |
| P1.3 tool boundary | `agent_platform_tool_execution_boundary_contract_hardening.md` | metadata_contract_review | Tool boundary. | Tool metadata is not tool execution. |
| P1.4 agent boundary | `agent_platform_agent_runtime_boundary_contract_hardening.md` | metadata_contract_review | Agent boundary. | Agent metadata is not agent execution. |
| P1.5 Cognitive Semantic System boundary | `agent_platform_cognitive_semantic_system_prototype_hardening.md` | metadata_contract_review | Substrate boundary. | Cognitive Semantic System substrate remains deferred. |
| S-03 / S-04 policies | Security policy records | policy_review | Secrets, credentials, shell, network, MCP constraints. | No enforcement activation. |
| optional P6 siblings | P6.2-P6.6 | not_reviewed_blocked | Future consumers only. | Not yet available by path-only check. |

## 5. Dependency Posture

| Dependency | Required for P6.1 | Current posture | Registry consequence | Blocker if missing |
| --- | --- | --- | --- | --- |
| P5.R minimal active agent platform audit | Yes | Present. | Registry baseline can be drafted. | Stop if absent. |
| P5.6 agent skeleton | Yes | Present. | Agent/task/handoff capability classes available as metadata. | Stop if absent. |
| P5.4 tool sandbox | Yes | Present. | Tool capability metadata can reference deny-by-default posture. | Stop if absent. |
| P5.5 provider adapter | Yes | Present. | Provider capability metadata can reference blocked/deferred posture. | Stop if absent. |
| P5.3 context assembly | Yes | Present. | Context capability metadata can reference context boundaries. | Stop if absent. |
| P5.7 audit hooks | Yes | Present. | Audit/retention/rollback metadata can be referenced. | Stop if absent. |
| P5.1 validation runner | Yes | Present. | Validation capability metadata can be referenced. | Stop if absent. |
| P5.2 security dry-run | Yes | Present. | Security capability metadata can be referenced. | Stop if absent. |
| P3.3 tool execution decision | Yes | Present. | Tool-bound capabilities remain blocked/deferred. | Stop if absent. |
| P3.4 provider/auth/API/MCP decision | Yes | Present. | Provider-bound capabilities remain blocked/deferred. | Stop if absent. |
| P3.5 agent runtime decision | Yes | Present. | Agent runtime eligibility remains future review only. | Stop if absent. |
| P2.1 vocabulary | Yes | Present. | Registry vocabulary defined. | Stop if absent. |
| P2.2 EvidenceRef | Yes | Present. | Evidence refs can be carried. | Stop if absent. |
| P2.3 retention/rollback/incident baseline | Yes | Present. | Retention/rollback/incident posture required. | Stop if absent. |
| P1.1-P1.5 boundaries | Yes | Present. | Context/provider/tool/agent/CSS boundaries constrain records. | Stop if absent. |
| S-03/S-04 | Yes | Present. | Secrets, credentials, shell, network, MCP blocked. | Stop if absent. |
| P6.2 protocol, if present | No | Not yet available. | Future protocol consumer only. | None for P6.1. |
| P6.3 context/evidence bus, if present | No | Not yet available. | Future bus consumer only. | None for P6.1. |
| P6.4 approval loop, if present | No | Not yet available. | Future approval consumer only. | None for P6.1. |
| P6.5 monitoring/incident, if present | No | Not yet available. | Future monitoring consumer only. | None for P6.1. |
| P6.6 substrate decision, if present | No | Not yet available. | Future substrate/defer consumer only. | None for P6.1. |

## 6. Operational Model

Agent Registry means a metadata registry contract for describing agents that may be reviewed later. Capability Registry means a metadata registry contract for describing capability classes, boundaries, blockers, dependencies, and future eligibility. Registry records are documentation-governance objects. Capabilities are declared metadata only. Capability boundaries are constraints. Dependencies are metadata refs. Runtime eligibility is future-review posture, not activation. Human approval is required for any future activation. Blocker propagation is mandatory.

| Operational component | Meaning | Current P6.1 status | Allowed use | Blocked use | Future consumer |
| --- | --- | --- | --- | --- | --- |
| Agent Registry | Metadata list of possible agent records. | Contract only. | Documentation governance. | Runtime registry, live agent registry. | P6.2, P6.7. |
| Capability Registry | Metadata list of possible capability records. | Contract only. | Capability classification. | Capability activation. | P6.3, P6.4, P6.5, P6.7. |
| Capability Boundary | Metadata constraints. | Required. | Propagate limits and blockers. | Bypass limits. | All P6 downstream. |
| Dependency Ref | Metadata dependency pointer. | Required. | Preserve P5/P3/P2/P1 refs. | Runtime dependency injection. | P6.7. |
| Runtime Eligibility | Future review posture. | Not eligible by default. | State required gates. | Runtime approval. | P6.7/P6 planning. |
| Approval Capability | Approval metadata refs. | Metadata only. | Human review package mapping. | active approval workflow. | P6.4. |
| Audit/Retention/Rollback capability | Metadata posture refs. | Metadata only. | Carry audit posture. | Persistence/database/event stream. | P6.5/P6.7. |
| Monitoring/Incident capability | Metadata incident refs. | Metadata only. | Future incident planning. | Monitoring runtime or incident automation. | P6.5. |

## 7. Object Model

These objects are registry metadata only. They are not runtime records, active registrations, executable capabilities, queues, dispatch records, persistence records, or approvals.

| Object | Meaning | Required fields | Forbidden fields | Allowed use | Blocked interpretation |
| --- | --- | --- | --- | --- | --- |
| `AgentRegistryRecord` | Metadata-only agent registry record. | `agent_registry_id`, `agent_label`, `agent_kind`, `operational_status`, `capability_refs`, `dependency_refs`, `context_refs`, `evidence_refs`, `validation_refs`, `security_refs`, `approval_refs`, `retention_refs`, `rollback_refs`, `incident_refs`, `blockers`, `limitations`, `runtime_eligibility_ref`, `review_required`. | Commands, callables, provider keys, credentials, queue names for live dispatch. | Describe agent candidates. | active agent registration. |
| `AgentCapabilityRecord` | Metadata-only capability registry record. | `capability_id`, `capability_label`, `capability_class`, `capability_status`, `capability_boundary`, `dependency_refs`, `required_gates`, `evidence_refs`, `validation_refs`, `security_refs`, `approval_refs`, `retention_posture`, `rollback_posture`, `incident_posture`, `blockers`, `limitations`, `review_required`. | Executable payloads, credentials, endpoints for live calls. | Classify capabilities. | active capability. |
| `CapabilityBoundary` | Boundary metadata for a capability. | `boundary_id`, `capability_ref`, `allowed_metadata_use`, `blocked_runtime_use`, `source_classification_limits`, `provider_limits`, `tool_limits`, `agent_execution_limits`, `product_limits`, `cadence_limits`, `substrate_limits`, `blockers`, `limitations`. | Runtime policy engine, enforcement hooks. | Preserve constraints. | Security enforcement activation. |
| `CapabilityStatus` | Capability status vocabulary. | status value and meaning. | Activation flags. | Describe status. | Capability execution. |
| `AgentOperationalStatus` | Agent operational status vocabulary. | status value and meaning. | Runtime health or daemon state. | Describe metadata posture. | Agent runtime state machine. |
| `AgentDependencyRef` | Metadata dependency reference. | dependency id, dependency type, required gate, blocker propagation. | Import path, executable dependency. | Map dependencies. | Runtime dependency injection. |
| `ToolCapabilityRef` | Tool capability metadata reference. | tool ref id, decision refs, blockers. | Tool command, callable, sandbox execution handle. | Link tool metadata. | Tool execution. |
| `ProviderCapabilityRef` | Provider capability metadata reference. | provider ref id, P3.4/P5.5 refs, blockers. | API key, endpoint invocation, SDK client. | Link provider metadata. | Provider activation. |
| `ContextCapabilityRef` | Context capability metadata reference. | context ref id, source classification refs, sensitivity, blockers. | Source path contents, traversal instructions. | Link context metadata. | Source loading. |
| `EvidenceCapabilityRef` | Evidence metadata reference. | evidence id, EvidenceRef, limitations. | Evidence authority flag. | Carry evidence. | Evidence deciding. |
| `HumanApprovalCapabilityRef` | Human approval metadata reference. | approval id, approver role, evidence package requirement, stop rule. | Approval token or automatic approval. | Describe approval requirement. | ApprovalRef is approval. |
| `RuntimeEligibilityRecord` | Future runtime eligibility metadata. | `eligibility_id`, `target_agent_ref`, `eligibility_status`, `required_gates`, `required_dependencies`, `required_human_approval`, `required_evidence_refs`, `required_validation_refs`, `required_security_refs`, `required_retention_refs`, `required_rollback_refs`, `required_incident_refs`, `blocked_until`, `limitations`. | Runtime activation switch, scheduler flag, daemon config. | Future review checklist. | Runtime approval. |

## 8. Status Vocabulary

No status value activates runtime, registers live agents, or enables capability execution.

| Vocabulary | Status value | Meaning | Allowed use | Blocked interpretation |
| --- | --- | --- | --- | --- |
| `CapabilityStatus` | `metadata_only` | Metadata record only. | Safe default. | Capability execution. |
| `CapabilityStatus` | `inactive` | Not active. | Non-execution posture. | Active capability. |
| `CapabilityStatus` | `blocked` | Blocked by boundary/gate. | Preserve blockers. | Workaround. |
| `CapabilityStatus` | `deferred` | Future review required. | Planning posture. | Activation. |
| `CapabilityStatus` | `candidate_for_future_review` | Review candidate only. | Future ticket input. | Approval. |
| `CapabilityStatus` | `requires_human_approval` | Approval needed. | Stop condition. | Approval granted. |
| `CapabilityStatus` | `requires_security_review` | Security review needed. | Stop condition. | Security approved. |
| `CapabilityStatus` | `requires_validation_review` | Validation review needed. | Stop condition. | Validation executed. |
| `CapabilityStatus` | `requires_runtime_gate` | Runtime gate needed. | Stop condition. | Runtime activated. |
| `CapabilityStatus` | `rejected_for_scope` | Out of scope. | Block. | Future reuse without review. |
| `CapabilityStatus` | `not_applicable` | Not relevant. | Clarify absence. | Hidden approval. |
| `CapabilityStatus` | `unknown` | Unknown posture. | Needs review. | Safe by default. |
| `AgentOperationalStatus` | `metadata_only` | Agent record only. | Safe default. | Agent execution. |
| `AgentOperationalStatus` | `not_registered_runtime` | No live registration. | Required default. | live registration. |
| `AgentOperationalStatus` | `inactive` | Not active. | Non-execution posture. | Active runtime. |
| `AgentOperationalStatus` | `blocked` | Blocked. | Preserve blockers. | Runtime bypass. |
| `AgentOperationalStatus` | `deferred` | Future review. | Planning posture. | Activation. |
| `AgentOperationalStatus` | `candidate_for_future_review` | Review candidate only. | Future ticket input. | Runtime eligibility. |
| `AgentOperationalStatus` | `requires_human_approval` | Human approval needed. | Stop condition. | Approval granted. |
| `AgentOperationalStatus` | `requires_dependency_alignment` | Dependencies not complete. | Stop condition. | Dependency bypass. |
| `AgentOperationalStatus` | `rejected_for_scope` | Out of scope. | Block. | Future reuse without review. |
| `AgentOperationalStatus` | `retired` | No longer candidate. | Decommission metadata. | Runtime deletion automation. |
| `AgentOperationalStatus` | `unknown` | Unknown. | Needs review. | Safe by default. |
| `RuntimeEligibilityStatus` | `not_eligible` | Not eligible for runtime. | Default. | Runtime approval. |
| `RuntimeEligibilityStatus` | `blocked` | Blocked by gate. | Preserve blockers. | Activation. |
| `RuntimeEligibilityStatus` | `deferred` | Future review. | Planning posture. | Activation. |
| `RuntimeEligibilityStatus` | `candidate_for_future_activation_review` | Future review candidate. | Future audit input. | Approval. |
| `RuntimeEligibilityStatus` | `requires_p6_audit` | P6 audit needed. | Stop condition. | Audit passed. |
| `RuntimeEligibilityStatus` | `requires_human_approval` | Human approval needed. | Stop condition. | Approval granted. |
| `RuntimeEligibilityStatus` | `requires_p4_product_readiness` | Product readiness needed. | Product blocker. | Product activation. |
| `RuntimeEligibilityStatus` | `requires_ext_review` | External review needed. | External blocker. | External adoption. |
| `RuntimeEligibilityStatus` | `requires_substrate_decision` | CSS substrate decision needed. | Substrate blocker. | Substrate selected. |
| `RuntimeEligibilityStatus` | `not_applicable` | Not relevant. | Clarify absence. | Hidden approval. |
| `RuntimeEligibilityStatus` | `unknown` | Unknown. | Needs review. | Safe by default. |

## 9. Capability Classification Matrix

| Capability class | Registry status | Allowed metadata use | Blocked runtime use | Required dependencies | Required gates | Blockers | Future consumer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| context capability | metadata-only candidate | ContextCapabilityRef and classification refs. | Source loading. | P5.3, P3.0, P1.1. | Future context review. | source_loading_blocker. | P6.3. |
| validation capability | metadata-only / runner skeleton | Validation refs and P5.1 posture. | Validation execution. | P5.1, P3.1. | GT-04 future. | validation_execution_blocker. | P6.7. |
| security dry-run capability | metadata-only / dry-run skeleton | Security refs and P5.2 posture. | Enforcement activation. | P5.2, P3.2, S-03/S-04. | Future security review. | security_enforcement_blocker. | P6.5/P6.7. |
| tool metadata capability | metadata-only | ToolCapabilityRef and P5.4 posture. | Tool execution. | P5.4, P3.3. | GT-07 future. | tool_execution_blocker. | P6.2/P6.7. |
| provider metadata capability | metadata-only | ProviderCapabilityRef and P5.5 posture. | Provider/auth/API/MCP activation. | P5.5, P3.4. | GT-08 future. | provider_auth_blocker. | P6.2/P6.7. |
| task envelope capability | metadata-only | P5.6 AgentTaskEnvelope metadata. | Task execution. | P5.6, P3.5. | Future agent gate. | agent_execution_blocker. | P6.2/P6.7. |
| handoff metadata capability | metadata-only | P5.6 AgentHandoffEnvelope metadata. | Handoff execution. | P5.6, P3.5. | Future handoff gate. | handoff_execution_blocker. | P6.2. |
| audit metadata capability | metadata-only | AuditRef, RetentionRef, RollbackRef, IncidentRef. | Persistence or telemetry. | P5.7, P2.3. | Future audit gate. | persistence_blocker. | P6.5/P6.7. |
| approval metadata capability | metadata-only | HumanApprovalCapabilityRef. | Approval automation. | P6.4 future. | Human approval gate. | approval_ref_not_approval. | P6.4. |
| monitoring metadata capability | metadata-only | Monitoring capability metadata. | Monitoring runtime. | P6.5 future. | Future monitoring review. | telemetry_blocker. | P6.5. |
| incident metadata capability | metadata-only | IncidentRef metadata. | Incident automation. | P6.5 future, P5.7. | Future incident review. | incident_automation_blocker. | P6.5. |
| executable capability | blocked | Blocker record only. | Execution. | Future exact activation. | Human approval plus relevant gate. | executable_capability_blocker. | P6.7. |
| autonomous capability | blocked | Blocker record only. | Scheduler/orchestration/autonomous loop. | Future exact activation. | GT-15/future runtime gate. | autonomous_loop_blocker. | P6.7. |
| provider-bound capability | blocked or deferred | Provider metadata only. | Provider calls. | P3.4, P5.5, S-03. | GT-08 future. | provider_auth_blocker. | P6.7. |
| tool-bound capability | blocked or deferred | Tool metadata only. | Tool execution. | P3.3, P5.4, S-04. | GT-07 future. | tool_execution_blocker. | P6.7. |
| product-bound capability | blocked until P4 / GT-09 | Product boundary metadata. | Product/Siamese source or actions. | P4 future, GT-09. | Product readiness gate. | product_blocker. | P4/P6.7. |
| live connector capability | blocked | Connector metadata only. | Connector polling/sync. | P3.4 future exact. | GT-08/GT-15 future. | live_connector_blocker. | P6.7. |
| GBrain/Hermes/Cadence capability | blocked / future inactive | External/cadence metadata only. | GBrain/Hermes/Cadence activation. | EXT review future. | EXT.GB/future cadence gate. | cadence_activation_blocker. | Future EXT. |
| Graphify/Codegraph capability | blocked as execution/adoption | Graphify evidence remains evidence only. | Graphify/Codegraph execution or authority. | Curated evidence only. | GT-11/future exact review. | graphify_codegraph_blocker. | P6.7. |
| Cognitive Semantic System relationship capability | metadata-only | Relationship metadata requirements. | Substrate selection or graph DB. | P1.5/P6.6 future. | Substrate decision gate if needed. | substrate_selection_blocker. | P6.6. |

## 10. Agent Registry Record Model

| Field | Required meaning | Allowed value pattern | Blocked value pattern |
| --- | --- | --- | --- |
| agent identity | Stable metadata id and label. | Human-readable id, no runtime handle. | Daemon id, queue name, socket id. |
| agent kind | Classification of agent candidate. | metadata-only, task-envelope, handoff-envelope. | Runtime executor. |
| operational status | AgentOperationalStatus. | metadata_only, blocked, deferred. | Active runtime. |
| capability refs | Metadata refs to capabilities. | Capability ids with blockers. | Executable capability pointers. |
| context refs | Context metadata refs. | Classified context references. | Source contents or traversal paths. |
| tool refs | Tool metadata refs. | ToolCapabilityRef only. | Tool callable or executor handle. |
| provider refs | Provider metadata refs. | ProviderCapabilityRef only. | API keys or clients. |
| evidence refs | EvidenceRef metadata. | Supporting refs. | Authority or truth engine. |
| validation refs | ValidationRef metadata. | Readiness/evaluation refs. | Validation execution proof. |
| security refs | SecurityRef metadata. | Constraint refs. | Enforcement approval. |
| approval refs | HumanApprovalCapabilityRef. | Required approval package. | Approval token. |
| retention/rollback/incident refs | P2.3 posture refs. | Required future posture. | Automation hooks. |
| runtime eligibility | RuntimeEligibilityRecord ref. | Future-review posture. | Runtime approval. |
| blockers | Mandatory blockers. | Propagated blocker ids. | Omitted blocker bypass. |
| limitations | Known limitations. | Metadata limitations. | Hidden approval. |

AgentRegistryRecord is not live registration. AgentRegistryRecord does not wake or schedule an agent. AgentRegistryRecord cannot call tools or providers. AgentRegistryRecord cannot grant runtime eligibility by itself. AgentRegistryRecord must preserve blockers and limitations.

## 11. Capability Registry Record Model

| Field | Required meaning | Allowed value pattern | Blocked value pattern |
| --- | --- | --- | --- |
| capability identity | Stable metadata id and label. | Capability id and label. | Runtime service id. |
| capability class | Classification from matrix. | context, validation, security, tool metadata, provider metadata, task, handoff, audit, approval, monitoring, incident. | executable by default. |
| capability status | CapabilityStatus. | metadata_only, blocked, deferred. | active capability. |
| boundary refs | CapabilityBoundary refs. | Explicit boundary ids. | Missing boundary. |
| dependency refs | AgentDependencyRef refs. | P5/P3/P2/P1/S refs. | Runtime dependency injection. |
| gate refs | Required gates. | Human approval and exact future gates. | Gate bypass. |
| evidence/validation/security refs | Supporting refs. | EvidenceRef, ValidationRef, SecurityRef metadata. | Execution approval. |
| approval refs | Approval metadata. | HumanApprovalCapabilityRef. | Approval granted. |
| retention/rollback/incident posture | P2.3-aligned posture. | Required future posture. | Persistence automation. |
| blockers | Blockers to propagate. | Explicit blockers. | Blocker omission. |
| limitations | Known limitations. | Metadata limitations. | Hidden activation. |

Capability presence is not capability activation. Capability presence is not user approval. Capability presence is not security approval. Capability presence is not validation approval. Capability presence is not source access approval.

## 12. Boundary Model

| Boundary | Registry rule | Blocked interpretation | Required future gate |
| --- | --- | --- | --- |
| runtime boundary | Registry metadata cannot start runtime. | Runtime registry or active agent registration. | P6.7/P6 activation review. |
| source boundary | Source classification refs only. | Source loading or source inspection. | GT-01/GT-05 future. |
| context boundary | Context inclusion is not permission. | Raw context/source loading. | P6.3/future context gate. |
| evidence boundary | Evidence supports; it does not decide. | Evidence authority. | Governance review. |
| validation boundary | Validation evaluates; governance decides. | Validation execution. | GT-04 future. |
| security boundary | Security constrains; it does not activate. | Security enforcement activation. | Security gate future. |
| tool boundary | Tool metadata is not tool execution. | Active tool capability. | GT-07/P3.3/P5.4 future. |
| provider/API/MCP boundary | Provider metadata is not provider activation. | Provider/API/MCP calls. | GT-08/P3.4/P5.5 future. |
| agent execution boundary | Agent metadata is not agent execution. | Agent/task/handoff execution. | P3.5/P5.6/P6.7 future. |
| approval boundary | ApprovalRef is not approval. | Active approval workflow. | P6.4/human approval. |
| audit/retention/rollback boundary | Refs only, no persistence. | Database/event store/logging runtime. | P5.7/P6.5 future. |
| monitoring/incident boundary | Metadata only. | Telemetry or incident automation. | P6.5 future. |
| product/Siamese boundary | Siamese is product vision. | Product source readable by default. | P4/GT-09 future. |
| GBrain/Hermes/Cadence boundary | Future inactive only. | Active cadence/runtime. | EXT/future exact review. |
| Graphify/Codegraph boundary | Evidence/tooling not authority. | Graphify Authority, Graphify truth engine, Graphify substrate, Codegraph authority. | GT-11/future exact review. |
| Cognitive Semantic System substrate boundary | Cognitive Semantic System substrate remains deferred. | Graph/vector substrate selected. | P6.6 if needed. |

## 13. Interfaces With P5 Skeletons

| P5 skeleton | Registry consumption | Capability class exposed as metadata | Blockers preserved | Blocked interpretation |
| --- | --- | --- | --- | --- |
| P5.1 validation runner skeleton | Validation capability refs. | validation capability. | validation_execution_blocker. | Active validation runner. |
| P5.2 security dry-run skeleton | Security capability refs. | security dry-run capability. | security_enforcement_blocker. | Runtime enforcement. |
| P5.3 context assembly skeleton | Context capability refs. | context capability. | source_loading_blocker. | Source loading. |
| P5.4 tool sandbox / allowlist skeleton | ToolCapabilityRef. | tool metadata capability. | tool_execution_blocker. | Calling sandbox as executor. |
| P5.5 provider adapter skeleton | ProviderCapabilityRef. | provider metadata capability. | provider_auth_blocker. | Provider/API/MCP activation. |
| P5.6 agent task/handoff skeleton | AgentRegistryRecord/task/handoff refs. | task envelope and handoff metadata capability. | agent_execution_blocker. | Agent execution. |
| P5.7 audit/retention/rollback hooks | Audit/retention/rollback refs. | audit metadata capability. | persistence_blocker. | Durable registry storage. |
| P5.R minimal active agent platform audit | Audit baseline refs. | runtime eligibility review metadata. | activation_blocker. | P5.R as activation. |

P6.1 can reference skeletons as metadata evidence. P6.1 cannot activate skeletons. P6.1 cannot convert skeletons into runtime services.

## 14. Interfaces With P3 Decisions

| P3 decision/readiness record | Registry consumption | Effect on capabilities | Blocked shortcut |
| --- | --- | --- | --- |
| P3.0 source classification readiness | SourceClassificationRef constraints. | Context/product/external/source capabilities constrained. | Source loading permission. |
| P3.1 validation execution readiness | ValidationRef constraints. | Validation capabilities remain non-executing. | Validation command execution. |
| P3.2 security enforcement readiness | SecurityRef constraints. | Security capabilities remain constraining metadata. | Enforcement activation. |
| P3.R activation readiness reconciliation | Readiness baseline. | Readiness remains non-activation. | Activation shortcut. |
| P3.3 tool execution activation decision | Tool execution baseline. | Tool-bound capabilities blocked/deferred. | Tool execution. |
| P3.4 provider/auth/API/MCP activation decision | Provider/MCP baseline. | Provider-bound capabilities blocked/deferred. | Provider/API/MCP activation. |
| P3.5 agent runtime activation decision | Agent runtime baseline. | Agent capabilities blocked/deferred. | Agent execution. |
| P3.BR activation decision reconciliation | P3-B reconciliation. | Deferred decisions remain deferred. | Broad activation. |

P3 decisions constrain registry capabilities. P3 decisions do not activate capabilities. Deferred P3 decisions remain deferred in P6.1.

## 15. Evidence / Validation / Security Interfaces

| Interface | Registry-carried refs | Required preservation rule | Blocked interpretation |
| --- | --- | --- | --- |
| EvidenceRef | evidence_refs, EvidenceCapabilityRef. | Preserve source and limitation. | Evidence deciding. |
| ValidationRef | validation_refs. | Preserve non-execution posture. | Validation execution. |
| SecurityRef | security_refs. | Preserve constraints. | Security activation. |
| SourceClassificationRef | source_classification_refs. | Preserve source class and sensitivity blockers. | Source loading. |
| ContextRef | context_refs, ContextCapabilityRef. | Preserve context inclusion limits. | Permission to read source. |
| ToolRef | ToolCapabilityRef. | Preserve P3.3/P5.4 blockers. | Tool execution. |
| ProviderRef | ProviderCapabilityRef. | Preserve P3.4/P5.5 blockers. | Provider activation. |
| AgentRef | AgentRegistryRecord refs. | Preserve P3.5/P5.6 blockers. | Agent execution. |
| ApprovalRef | HumanApprovalCapabilityRef. | Preserve human approval required. | Approval granted. |
| RetentionRef | retention_refs. | Preserve output/storage blockers. | Persistence approval. |
| RollbackRef | rollback_refs. | Preserve rollback requirements. | Rollback automation. |
| IncidentRef | incident_refs. | Preserve incident route requirement. | Incident automation. |
| AuditRef | audit_refs. | Preserve audit metadata. | Audit logging runtime. |

Evidence supports; it does not decide. Validation evaluates; governance decides. Security constrains; it does not activate. ApprovalRef is not approval. Registry refs do not authorize execution.

## 16. Retention / Rollback / Incident Posture

| Record type | Retention posture | Rollback posture | Incident route | Publication blocker | Source tracking blocker |
| --- | --- | --- | --- | --- | --- |
| registry metadata records | Metadata-only; no persistence automation. | Manual governance rollback only. | Manual incident route if boundary breached. | publication_blocker. | source_tracking_blocker. |
| capability metadata records | Metadata-only; no durable registry storage. | Manual governance rollback only. | Manual incident route. | publication_blocker. | source_tracking_blocker. |
| dependency refs | Retain as governance refs only. | Update by future governance patch. | Escalate if dependency misclassified. | publication_blocker. | source_tracking_blocker. |
| approval refs | Retain as approval requirements only. | Remove/revise by governance. | Escalate if treated as approval. | publication_blocker. | source_tracking_blocker. |
| audit refs | Retain as metadata refs only. | No audit log rollback automation. | Escalate if logging runtime requested. | publication_blocker. | source_tracking_blocker. |
| incident refs | Retain as required route metadata. | No automatic quarantine/deletion. | Manual route only. | publication_blocker. | source_tracking_blocker. |
| blocked capability records | Retain blocker and limitation metadata. | Manual governance update only. | Escalate attempted activation. | publication_blocker. | source_tracking_blocker. |
| deferred capability records | Retain future-review posture. | Manual governance update only. | Escalate premature activation. | publication_blocker. | source_tracking_blocker. |
| future eligibility records | Retain eligibility requirements only. | Manual governance update only. | Escalate if treated as approval. | publication_blocker. | source_tracking_blocker. |

P6.1 does not implement retention, rollback, incident, quarantine, deletion, logging, telemetry, or persistence automation.

## 17. Human Approval Requirements

| Approval event | Required approver role | Required evidence package | Stop rule if absent |
| --- | --- | --- | --- |
| Future agent activation | Human platform owner. | P6.7 audit, P3.5/P3.BR refs, P5.6 refs, blockers closure. | Stop. |
| Future capability activation | Human platform owner. | CapabilityBoundary, dependency refs, gates, blockers closure. | Stop. |
| Future tool-bound capability | Human platform owner plus security reviewer. | P3.3/P5.4/S-04 refs. | Stop. |
| Future provider-bound capability | Human platform owner plus security reviewer. | P3.4/P5.5/S-03 refs. | Stop. |
| Future product-bound capability | Product owner plus platform owner. | P4/GT-09 readiness package. | Stop. |
| Future live connector capability | Platform owner plus security reviewer. | P3.4/P6.5 refs and incident posture. | Stop. |
| Future autonomous capability | Platform owner plus governance reviewer. | Scheduler/orchestration risk package. | Stop. |
| Future registry-to-runtime transition | Platform owner. | Full activation package and P6.7 audit. | Stop. |

HumanApprovalCapabilityRef is metadata only and does not approve by itself.

## 18. Stop Rules

Stop on registry runtime request. Stop on live agent registration request. Stop on capability activation request. Stop on executable capability request. Stop on autonomous capability request. Stop on task execution request. Stop on handoff execution request. Stop on scheduler/orchestration request. Stop on tool execution request. Stop on provider/auth/API/MCP request. Stop on credential request. Stop on live connector request. Stop on source loading request. Stop on product source request. Stop on external source inspection request. Stop on GBrain/Hermes/Cadence activation request. Stop on Graphify/Codegraph adoption or execution request. Stop on validation execution request. Stop on security enforcement activation request. Stop on persistence/database/event stream request. Stop on telemetry request. Stop on generated output tracking request. Stop on source tracking expansion request. Stop on publication request. Stop on substrate selection request. Stop on unknown sensitivity.

## 19. Parallel P6 Alignment Rules

P6.2 must consume P6.1 registry metadata if present. P6.3 must consume P6.1 capability classes where context/evidence capabilities are referenced. P6.4 must consume P6.1 approval capability records and must not treat them as approval. P6.5 must consume P6.1 monitoring/incident capability metadata and must not activate monitoring. P6.6 must consume P6.1 registry/capability requirements only as metadata and must not select substrate by registry pressure. If downstream documents are absent, P6.1 records them as future consumers only. P6.1 does not start downstream tickets.

## 20. Future Validation Targets

Future validation targets, not executed:

| Target | Status |
| --- | --- |
| AgentRegistryRecord required field completeness. | Future only. |
| AgentCapabilityRecord required field completeness. | Future only. |
| CapabilityBoundary completeness. | Future only. |
| CapabilityStatus vocabulary conformance. | Future only. |
| AgentOperationalStatus vocabulary conformance. | Future only. |
| RuntimeEligibilityRecord completeness. | Future only. |
| Capability classification matrix completeness. | Future only. |
| P5 skeleton interface coverage. | Future only. |
| P3 decision interface coverage. | Future only. |
| P2.1 vocabulary conformance. | Future only. |
| P2.2 EvidenceRef conformance. | Future only. |
| P2.3 retention/rollback/incident conformance. | Future only. |
| Agent metadata is not agent execution invariant. | Future only. |
| Capability metadata is not capability execution invariant. | Future only. |
| Registry is not runtime invariant. | Future only. |
| ApprovalRef is not approval invariant. | Future only. |
| Provider metadata is not provider activation invariant. | Future only. |
| Tool metadata is not tool execution invariant. | Future only. |
| Context inclusion is not permission invariant. | Future only. |
| GBrain/Hermes/Cadence inactive invariant. | Future only. |
| Graphify/Codegraph non-adoption invariant. | Future only. |
| Product/Siamese inactive invariant. | Future only. |
| Cognitive Semantic System substrate-deferred invariant. | Future only. |
| No persistence/telemetry invariant. | Future only. |

## 21. Future Hardening Candidates

Future tickets, not started:

| Candidate | Description |
| --- | --- |
| REG-HARD-01 | Agent Registry Record Schema Candidate. |
| REG-HARD-02 | Capability Registry Record Schema Candidate. |
| REG-HARD-03 | Capability Boundary Matrix Hardening. |
| REG-HARD-04 | Runtime Eligibility Criteria Hardening. |
| REG-HARD-05 | Agent Dependency Ref Alignment. |
| REG-HARD-06 | Tool / Provider Capability Ref Alignment. |
| REG-HARD-07 | Human Approval Capability Ref Alignment. |
| REG-HARD-08 | Monitoring / Incident Capability Ref Alignment. |
| REG-HARD-09 | Registry No-Activation Invariant Checklist. |
| REG-HARD-10 | P6.7 Registry Audit Input. |

## 22. Created / Not Created Register

Created:

| File |
| --- |
| `0_architecture/governance/agent_platform_agent_capability_registry_operational_contract.md` |

Modified:

| Scope |
| --- |
| none |

Not created / not approved:

| Item | Posture |
| --- | --- |
| runtime activation | Not created or approved. |
| registry runtime | Not created or approved. |
| live agent registration | Not created or approved. |
| capability activation | Not created or approved. |
| agent execution | Not created or approved. |
| task execution | Not created or approved. |
| handoff execution | Not created or approved. |
| scheduler/orchestration/autonomous loop | Not created or approved. |
| tool execution | Not created or approved. |
| provider/auth/API/MCP activation | Not created or approved. |
| credential use | Not performed. |
| API calls | Not performed. |
| live connector activation | Not created or approved. |
| source loading | Not created or approved. |
| source inspection | Not performed. |
| product source inspection | Not performed. |
| external source inspection | Not performed. |
| GBrain/Hermes/Cadence activation | Not created or approved. |
| Graphify/Codegraph adoption or execution | Not created or approved. |
| validation execution | Not created or approved. |
| tests/CI/scripts/builds | Not run. |
| security enforcement activation | Not created or approved. |
| persistence/database/event stream | Not created or approved. |
| telemetry | Not created or approved. |
| vector DB / embeddings | Not created or approved. |
| graph DB / substrate implementation | Not created or approved. |
| generated output tracking | Not created or approved. |
| source tracking expansion | Not created or approved. |
| publication | Not created or approved. |
| Git mutation | Not performed. |

## 23. Recommended Next Ticket

After P6.1, the recommended queue is:

| Ticket | Sequence posture |
| --- | --- |
| P6.2 - Agent-to-Agent Communication Protocol | Recommended actual next ticket. |
| P6.3 - Shared Context / Evidence Bus | After or alongside P6.2 as governed planning only. |
| P6.4 - Human Approval / Review Loop | After registry/capability metadata exists. |
| P6.5 - Runtime Monitoring / Incident Handling | After approval and incident metadata planning. |
| P6.6 - Cognitive Semantic System Substrate Decision | Only if needed. |
| P6.7 - Operational Readiness Audit | After P6.1-P6.5 and P6.6 if created/deferred. |

Recommended actual: P6.2 - Agent-to-Agent Communication Protocol.

Do not start P6.2. Do not start P6.3. Do not start P6.4. Do not start P6.5. Do not start P6.6. Do not start P6.7.

## 24. Final Verdict

| Question | Answer |
| --- | --- |
| What did P6.1 create? | The canonical Agent Registry / Capability Registry operational contract. |
| What Agent Registry contract was defined? | A metadata-only registry contract for AgentRegistryRecord records, not runtime. |
| What Capability Registry contract was defined? | A metadata-only registry contract for AgentCapabilityRecord records, boundaries, dependencies, and eligibility. |
| What AgentRegistryRecord was defined? | Metadata-only agent record with identity, status, refs, blockers, limitations, and runtime eligibility ref. |
| What AgentCapabilityRecord was defined? | Metadata-only capability record with class, status, boundary, dependencies, gates, refs, blockers, limitations, and review requirement. |
| What CapabilityBoundary was defined? | Metadata boundary object with allowed metadata use, blocked runtime use, limits, blockers, and limitations. |
| What CapabilityStatus vocabulary was defined? | metadata_only, inactive, blocked, deferred, candidate_for_future_review, requires_human_approval, requires_security_review, requires_validation_review, requires_runtime_gate, rejected_for_scope, not_applicable, unknown. |
| What AgentOperationalStatus vocabulary was defined? | metadata_only, not_registered_runtime, inactive, blocked, deferred, candidate_for_future_review, requires_human_approval, requires_dependency_alignment, rejected_for_scope, retired, unknown. |
| What AgentDependencyRef was defined? | Metadata dependency reference preserving dependency type, gate, and blocker propagation. |
| What ToolCapabilityRef was defined? | Metadata-only tool capability reference; no tool execution. |
| What ProviderCapabilityRef was defined? | Metadata-only provider capability reference; no provider activation. |
| What ContextCapabilityRef was defined? | Metadata-only context capability reference; no source loading. |
| What EvidenceCapabilityRef was defined? | Metadata-only evidence reference; evidence is not authority. |
| What HumanApprovalCapabilityRef was defined? | Metadata-only approval requirement; ApprovalRef is not approval. |
| What RuntimeEligibilityRecord was defined? | Future-review metadata checklist; not runtime approval. |
| Which capability classes were classified? | Context, validation, security dry-run, tool metadata, provider metadata, task envelope, handoff metadata, audit metadata, approval metadata, monitoring metadata, incident metadata, executable, autonomous, provider-bound, tool-bound, product-bound, live connector, GBrain/Hermes/Cadence, Graphify/Codegraph, Cognitive Semantic System relationship. |
| Which capabilities remain metadata-only? | Context, validation, security dry-run, tool metadata, provider metadata, task envelope, handoff metadata, audit metadata, approval metadata, monitoring metadata, incident metadata, and Cognitive Semantic System relationship capabilities. |
| Which capabilities remain blocked? | Executable, autonomous, product-bound, live connector, GBrain/Hermes/Cadence, Graphify/Codegraph execution/adoption, and runtime-bound capability classes; provider-bound and tool-bound remain blocked or deferred. |
| Which dependencies were mapped? | P5.R, P5.1-P5.7, P3.3-P3.5/P3.BR/P3-A, P2.1-P2.3, P1.1-P1.5, P0/S-03/S-04, and future P6.2-P6.6. |
| How does P6.1 consume P5 skeletons? | As metadata evidence and capability class inputs only. |
| How does P6.1 consume P3 decisions? | As constraints on registry capabilities; deferred decisions remain deferred. |
| How are EvidenceRef / ValidationRef / SecurityRef preserved? | As registry-carried refs with non-decision, non-execution, non-activation semantics. |
| How are retention / rollback / incident postures preserved? | As metadata refs and required future posture; no automation. |
| What human approval requirements were defined? | Human approval is required before any future agent, capability, tool-bound, provider-bound, product-bound, live connector, autonomous, or registry-to-runtime transition. |
| What stop rules were defined? | Stop on runtime, registration, activation, execution, provider/MCP, credential, source/product/external inspection, Graphify/Codegraph, GBrain/Hermes/Cadence, validation/security activation, persistence, telemetry, tracking, publication, substrate, or unknown sensitivity requests. |
| Did P6.1 create registry runtime? | No. |
| Did P6.1 register live agents? | No. |
| Did P6.1 activate capabilities? | No. |
| Did P6.1 execute agents, tasks, or handoffs? | No. |
| Did P6.1 activate scheduler/orchestration/autonomous loops? | No. |
| Did P6.1 execute tools? | No. |
| Did P6.1 activate provider/auth/API/MCP? | No. |
| Did P6.1 activate live connectors? | No. |
| Did P6.1 load or inspect source? | No. |
| Did P6.1 inspect product source? | No. |
| Did P6.1 activate GBrain, Hermes, or Cadence? | No. |
| Did P6.1 adopt Graphify or Codegraph? | No. |
| Did P6.1 implement persistence, database, event stream, or telemetry? | No. |
| Did P6.1 select Cognitive Semantic System substrate? | No. |
| What is the next recommended ticket? | P6.2 - Agent-to-Agent Communication Protocol. |

Stop after P6.1. Do not start P6.2, P6.3, P6.4, P6.5, P6.6, or P6.7.
