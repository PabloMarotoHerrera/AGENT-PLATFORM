# Agent-to-Agent Communication Protocol

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | Agent-to-Agent Communication Protocol |
| Ticket | P6.2 |
| Status | Accepted agent-to-agent communication protocol contract |
| Date | 2026-07-05 |
| Scope | Define the metadata-only Agent-to-Agent Communication Protocol operational contract for AGENT PLATFORM / Siamese. |
| Authority | metadata-only agent-to-agent communication protocol contract, not message dispatch, queue, broker, websocket, network, MCP, provider call, agent wake-up, scheduler activation, orchestration activation, handoff execution, runtime activation, validation execution, security enforcement activation, source loading, product source inspection, provider/auth/API/MCP activation, credential use, tool execution, agent execution, live connector activation, GBrain/Hermes/Cadence activation, Graphify/Codegraph adoption or execution, persistence/database/event stream, telemetry, vector DB implementation, embedding generation, graph DB implementation, generated output tracking, source tracking expansion, publication, Git mutation, or Cognitive Semantic System substrate selection. |
| Related documents | P5.R, P5.6, P5.7, P5.3, P5.4, P5.5, P5.2, P3.BR, P3.3, P3.4, P3.5, P3.R, P3.0, P3.1, P3.2, P2.2, P2.3, P2.1, P1.4, P1.3, P1.2, P1.1, P0.1-P0.3, S-03, S-04, CSS ADR/audit, README.md, `.gitignore`, `.graphifyignore`, P6.1/P6.3/P6.4/P6.5/P6.6 if present. |
| Output | agent-to-agent communication protocol contract |

Protocol is not message dispatch. Agent-to-agent communication remains non-active.

## 2. Purpose

P6 defines operational contracts without activation. P6.2 defines the metadata-only protocol by which agents would communicate in a future controlled runtime.

P6.2 defines AgentMessageEnvelope, AgentMessageType, SenderRef, ReceiverRef, ConversationRef, HandoffRef, ContextRef, EvidenceRef binding, ValidationRef binding, SecurityRef binding, ApprovalRef binding, MessageDeliveryStatus, and MessageDispatchDecision metadata.

P6.2 consumes or anticipates P6.1, P6.3, P6.4, and P6.5. If peer P6 documents are absent, P6.2 records pending alignment markers. P6.2 consumes P5.6 agent task/handoff skeleton and P5.7 audit/retention/rollback hooks.

P6.2 does not send messages. P6.2 does not create dispatch. P6.2 does not create queue, broker, websocket, network, MCP, provider call, agent wake-up, scheduler, orchestration loop, or handoff execution. P6.2 does not start P6.7.

## 3. Current Posture

| Area | Current posture |
| --- | --- |
| AGENT PLATFORM | AGENT PLATFORM remains AL-1 metadata skeleton. |
| Operational planning | Operational planning is not activation. |
| Protocol | Protocol is not message dispatch. |
| Agent metadata | Agent metadata is not agent execution. |
| HandoffRef | HandoffRef is not handoff execution. |
| ApprovalRef | ApprovalRef is not approval. |
| Context | Context inclusion is not permission. |
| Evidence | Evidence supports; it does not decide. |
| Validation | Validation evaluates; governance decides. |
| Security | Security constrains; it does not activate. |
| P5.6 | P5.6 agent task/handoff skeleton remains non-executing. |
| P5.7 | P5.7 audit/retention/rollback hooks remain non-automated. |
| Tools | Tool execution remains blocked. |
| Providers | Provider/auth/API/MCP activation remains blocked. |
| Live connectors | Live connectors remain blocked. |
| GBrain / Hermes / Cadence | GBrain / Hermes / Cadence remain future and inactive. |
| Graphify | Graphify evidence is supporting generated evidence only, not authority. |
| Cognitive Semantic System | Cognitive Semantic System substrate remains deferred unless P6.6 creates a decision record. |
| Siamese | Siamese is product vision, not product activation. |

## 4. Inputs Reviewed

Inputs are reviewed as governance/architecture metadata only. P6.2 does not load source, inspect product source, inspect external source contents, inspect GBrain/Hermes/Graphify contents, inspect secrets, inspect credentials, inspect provider configs, inspect token stores, inspect browser auth, inspect local credential stores, inspect API keys, or inspect raw generated outputs.

| input | present | consumed_as | protocol_relevance | limitations | pending_alignment |
| --- | --- | --- | --- | --- | --- |
| P5.R minimal active agent platform audit | yes | P5 baseline closure | Confirms P6 planning eligibility and no unresolved P5 runtime skeleton drift. | Planning eligibility only, no activation. | none |
| P5.6 agent task/handoff skeleton | yes | agent task/handoff baseline | Supplies AgentTaskEnvelope and AgentHandoffEnvelope reference posture. | No agent, task, or handoff execution. | none |
| P5.7 audit/retention/rollback hooks | yes | retention/rollback/incident baseline | Supplies retention, rollback, incident, and no-persistence posture. | No audit sink, persistence, rollback automation, or incident automation. | none |
| P5.3 context assembly skeleton | yes | context baseline | Supplies ContextRef and SourceRef no-source-loading posture. | No source loading or source inspection. | none |
| P5.4 tool sandbox / allowlist skeleton | yes | tool boundary baseline | Supplies tool metadata and blocked execution posture. | No tool execution. | none |
| P5.5 provider adapter skeleton | yes | provider boundary baseline | Supplies provider metadata and blocked provider/auth/API/MCP posture. | No provider call, auth, network, MCP, or live connector activation. | none |
| P5.2 security dry-run skeleton | yes | security dry-run baseline | Supplies SecurityRef constraints and dry-run posture. | Security dry-run is not enforcement. | none |
| P3.BR activation decision reconciliation closure | yes | activation decision baseline | Confirms P3-B decisions are canonical and non-executing. | Decision is not execution. | none |
| P3.3 tool execution activation decision | yes | tool decision | Tool execution remains deferred or exact-scope only. | No tool execution approval. | none |
| P3.4 provider/auth/API/MCP activation decision | yes | provider decision | Provider/auth/API/MCP activation remains blocked/deferred. | No provider, API, network, MCP, credential, or live connector activation. | none |
| P3.5 agent runtime activation decision | yes | agent decision | Agent runtime activation remains blocked/deferred. | No runtime launch, no agent execution. | none |
| P3.R activation readiness reconciliation closure | yes | readiness closure | Readiness context for future activation decisions. | Readiness is not activation. | none |
| P3.0 source classification readiness | yes | source classification baseline | Source, sensitivity, product, external, generated, and local-only blockers. | Classification is not source loading. | none |
| P3.1 validation execution readiness | yes | validation readiness baseline | ValidationRef posture and no-validation-execution boundary. | No validation execution. | none |
| P3.2 security enforcement readiness | yes | security readiness baseline | SecurityRef posture and enforcement blocker. | No security enforcement activation. | none |
| P2.1 shared metadata vocabulary | yes | vocabulary baseline | Canonical shared metadata terms for refs, blockers, status, source, and sensitivity. | No schema enforcement. | none |
| P2.2 EvidenceRef contract | yes | evidence contract | EvidenceRef, SourceRef, ValidationRef, SecurityRef, GraphifyRef, ProductRef semantics. | Evidence supports; it does not decide. | none |
| P2.3 audit/retention/rollback baseline | yes | retention baseline | Retention, rollback, quarantine, publication, source tracking, generated output, and incident blockers. | No persistence or automation. | none |
| P1.4 agent runtime boundary contract | yes | agent boundary contract | Agent metadata, task metadata, handoff metadata, approval refs, and execution blockers. | Agent metadata is not agent execution. | none |
| P1.3 tool execution boundary contract | yes | tool boundary contract | Tool metadata and ToolRef blocker semantics. | Tool metadata is not tool execution. | none |
| P1.2 provider adapter metadata contract | yes | provider boundary contract | Provider metadata, CredentialRef, auth, network, and MCP blockers. | Provider metadata is not provider activation. | none |
| P1.1 context runtime contract | yes | context boundary contract | ContextPack, SourceRef, local-only, product, external, and generated-output constraints. | Context inclusion is not permission. | none |
| P0.1-P0.3 control plane | yes | gate control plane | Activation gate, validation gate, and security hardening posture. | Gate refs are not approvals. | none |
| S-03 local-only/secrets/credentials policy | yes | local-only/security policy | Secret, credential, `.env`, provider auth, local-only, and generated-output blockers. | No secret or credential inspection. | none |
| S-04 tool/shell/network/MCP policy | yes | execution policy | Tool, shell, network, provider/API, MCP, package, build, test, CI, Git, and execution blockers. | No execution. | none |
| Cognitive Semantic System ADR/audit | yes | naming/substrate baseline | Accepted Cognitive Semantic System name and deferred substrate posture. | No substrate selection. | none |
| README.md | yes | workspace orientation | Root workspace orientation. | No runtime effect. | none |
| `.gitignore` | yes | boundary posture | Local-only/generated/secret/provider-auth Git hygiene posture. | Not modified; not a security system. | none |
| `.graphifyignore` | yes | Graphify boundary posture | Graphify input hygiene and generated evidence boundary. | Not modified; not Graphify permission. | none |
| P6.1 agent/capability registry if present | no | optional peer | Would align SenderRef, ReceiverRef, and capability refs. | Not created or modified. | `pending_P6.1_agent_registry_alignment` |
| P6.3 shared context/evidence bus if present | no | optional peer | Would align ContextRef and EvidenceRef bindings. | Not created or modified. | `pending_P6.3_context_evidence_bus_alignment` |
| P6.4 human approval/review loop if present | no | optional peer | Would align ApprovalRef binding and approval review posture. | Not created or modified. | `pending_P6.4_human_approval_alignment` |
| P6.5 runtime monitoring/incident handling if present | no | optional peer | Would align IncidentRef, monitoring refs, and delivery status. | Not created or modified. | `pending_P6.5_monitoring_incident_alignment` |
| P6.6 Cognitive Semantic System substrate decision if present | no | optional peer | Not required for P6.2 protocol creation. | No substrate selected. | `substrate_decision_not_required_by_P6.2` |
| `external/sources/gbrain-master` as path/class metadata only | no | optional path metadata | Would remain external source/cadence reference candidate if present. | Contents not inspected. | absent_path_metadata_only |

## 5. Dependency Posture

| dependency | required_for_protocol | consumed_posture | protocol_implication | blocker_if_absent |
| --- | --- | --- | --- | --- |
| P6.1 agent/capability registry | preferred, not blocking | absent | SenderRef and ReceiverRef use protocol-local metadata pending registry alignment. | `pending_P6.1_agent_registry_alignment` |
| P6.3 shared context/evidence bus | preferred, not blocking | absent | ContextRef and EvidenceRef bindings use P2/P5 posture pending bus alignment. | `pending_P6.3_context_evidence_bus_alignment` |
| P6.4 human approval/review loop | preferred, not blocking | absent | ApprovalRef binding records metadata only pending review-loop alignment. | `pending_P6.4_human_approval_alignment` |
| P6.5 monitoring/incident handling | preferred, not blocking | absent | IncidentRef and delivery status use protocol-local posture pending monitoring alignment. | `pending_P6.5_monitoring_incident_alignment` |
| P5.6 agent task/handoff skeleton | yes | present, non-executing | AgentMessageEnvelope may reference task and handoff envelopes without execution. | Stop if missing from future reconciliation. |
| P5.7 audit/retention/rollback hooks | yes | present, no-op/non-persistent | Message envelopes must include retention, rollback, and incident posture without persistence. | Stop if missing from future reconciliation. |
| P2.2 EvidenceRef contract | yes | present, support-only | EvidenceRef binding remains support-only and cannot approve dispatch. | Evidence posture unresolved. |
| P2.3 audit/retention/rollback baseline | yes | present, metadata-only | RetentionRef, RollbackRef, IncidentRef, publication, and tracking blockers propagate. | Retention posture unresolved. |
| P3.BR activation decision reconciliation | yes | present, non-executing | P6.2 cannot override P3-B decisions. | Activation-decision baseline unresolved. |
| P1.4 agent runtime boundary contract | yes | present, metadata-only | Agent metadata, task metadata, handoff metadata, and approval refs remain non-executing. | Agent boundary unresolved. |
| S-03 local-only/secrets/credentials policy | yes | present, blocked defaults | Messages must exclude secrets, credentials, `.env`, provider auth, token stores, browser auth, local credential stores, and API keys. | Security/local-only posture unresolved. |
| S-04 tool/shell/network/MCP policy | yes | present, blocked defaults | Protocol must not create execution, network, MCP, provider/API calls, queues, brokers, or runtime buses. | Execution policy unresolved. |

P6.2 may proceed with pending markers because P6.1 through P6.5 may run in parallel. Pending alignment is not a blocker for creating the P6.2 contract, but must be reconciled by P6.7.

## 6. Operational Model

The Agent-to-Agent Communication Protocol is a metadata-only protocol model that describes how future agent messages would be represented, constrained, reviewed, audited, and blocked before any dispatch occurs.

| Rule | Required posture |
| --- | --- |
| Protocol is not runtime. | No runtime surface is created. |
| Protocol is not dispatch. | No message dispatch is created or approved. |
| Protocol is not queue. | No queue is created or approved. |
| Protocol is not broker. | No broker is created or approved. |
| Protocol is not websocket. | No websocket is created or approved. |
| Protocol is not network. | No network protocol or channel is created or approved. |
| Protocol is not MCP. | No MCP channel, server, resource, or tool activation is created or approved. |
| Protocol is not provider call. | No provider/API/model call is created or approved. |
| Protocol is not agent wake-up. | No agent is woken, scheduled, invoked, or executed. |
| Protocol is not scheduler. | No scheduler is created or activated. |
| Protocol is not orchestration. | No orchestration loop or autonomous loop is created or activated. |
| Protocol is not handoff execution. | Handoff metadata remains blocked. |
| Protocol is not persistence. | No database, event store, file log, or persistence layer is created. |
| Protocol is not telemetry. | No telemetry pipeline or event stream is created. |
| Protocol envelopes are records, not active messages. | Envelopes are documentation metadata. |
| MessageDispatchDecision is a decision record, not dispatch execution. | Dispatch remains false by default. |
| MessageDeliveryStatus is status metadata, not delivery telemetry. | Status does not prove delivery. |

## 7. Object Model

| object | meaning | required fields | forbidden fields/content | activation boundary | retention/security posture |
| --- | --- | --- | --- | --- | --- |
| AgentMessageEnvelope | Canonical metadata envelope for future agent-to-agent message representation. | message_id, message_type, sender_ref, receiver_refs, refs, posture, delivery_status, dispatch_decision, blockers, limitations | Raw source, secrets, credentials, provider outputs, tool outputs, agent execution outputs, raw generated outputs | Record only, no message dispatch. | Metadata-only retention; secret/credential blockers propagate. |
| AgentMessageType | Canonical message type vocabulary. | type value | Executable commands or dispatch permission | Type is metadata only. | Unknown types block future dispatch eligibility. |
| SenderRef | Canonical sender reference object. | sender_ref_id, sender_kind, posture, refs, blockers | Live runtime handles, tokens, sessions | Does not wake or invoke sender. | Registry alignment pending if P6.1 absent. |
| ReceiverRef | Canonical receiver reference object. | receiver_ref_id, receiver_kind, posture, refs, blockers | Live runtime handles, tokens, sessions | Does not dispatch to receiver. | Registry alignment pending if P6.1 absent. |
| ConversationRef | Canonical conversation metadata object. | conversation_ref_id, scope, status, refs, posture, blockers | Chat runtime, queue state, websocket channel, thread store | Metadata only, no active conversation runtime. | Retention/rollback/incident posture required. |
| HandoffRef | Canonical handoff reference object. | handoff_ref_id, source, target, task_ref, refs, status, execution_posture, blockers | Handoff triggers, executable tasks, scheduler handles | HandoffRef is not handoff execution. | P5.6 blockers and P5.7 posture propagate. |
| ContextRef | Canonical context reference object. | context_ref_id, pack/item/source refs, scope, posture, sensitivity, blockers | Raw source content, product source, external content, secrets, credentials | ContextRef is not source loading. | SourceRef, sensitivity, local-only, product, external, generated-output blockers propagate. |
| EvidenceRefBinding | EvidenceRef binding for messages. | evidence_ref_id, scope, kind, authority_posture, retention_posture, blockers | Raw evidence payloads or authority claims | Evidence cannot approve dispatch. | Supporting evidence only. |
| ValidationRefBinding | ValidationRef binding for messages. | validation_ref_id, scope, status, execution_posture, output_posture, blockers | Validation command output as approval | Validation cannot approve dispatch. | Validation output generated-sensitive unless gated. |
| SecurityRefBinding | SecurityRef binding for messages. | security_ref_id, scope, status, sensitivity, blockers, incident requirements | Security approval by citation, secret values | Security cannot activate dispatch. | Unknown security posture blocks future dispatch eligibility. |
| ApprovalRefBinding | ApprovalRef binding for messages. | approval_ref_id, scope, reviewer_ref, status, conditions, expiry, blockers | Auto-approval, self-approval, broad approval | ApprovalRef is not approval. | Human exact-scope approval required before future dispatch. |
| RetentionRefBinding | Retention metadata binding. | retention_ref_id, scope, retention_posture, blockers | Raw retained sensitive content | No persistence approval. | Metadata-only retention. |
| RollbackRefBinding | Rollback metadata binding. | rollback_ref_id, owner, trigger, impacted refs, routes, limitations | Rollback automation commands | No rollback automation. | Future rollback route only. |
| IncidentRefBinding | Incident metadata binding. | incident_ref_id, trigger, stop/quarantine/review fields, limitations | Incident automation or payload repetition | No incident automation. | Stop, quarantine review, and safe metadata only. |
| MessageDeliveryStatus | Canonical delivery status object. | status value | Delivery telemetry or proof | Status is metadata only. | Defaults to not_dispatched or dispatch_blocked. |
| MessageDispatchDecision | Canonical dispatch decision object. | decision_id, message_id, status, allowed flag, gates, refs, blocked actions | Dispatch commands or runtime handles | Decision is not dispatch execution. | dispatch_allowed false by default. |
| MessageLimitation | Message limitation object. | limitation_id, scope, description, blocked inference, required review | Limitation removal by implication | Limitations block promotion. | Must travel downstream. |
| MessageBlocker | Message blocker object. | blocker_id, blocker_scope, blocker_reason, required_gate, stop_behavior, status | Bypass instructions or hidden exceptions | Blockers stop future dispatch eligibility. | Security and governance blockers remain binding. |

## 8. AgentMessageEnvelope Contract

AgentMessageEnvelope required fields:

| Field | Required meaning |
| --- | --- |
| message_id | Stable metadata identifier for the message envelope. |
| message_type | AgentMessageType value. |
| sender_ref | SenderRef metadata reference. |
| receiver_refs | One or more ReceiverRef metadata references. |
| conversation_ref | ConversationRef metadata reference. |
| handoff_ref | HandoffRef metadata reference or none. |
| context_refs | ContextRef metadata references. |
| evidence_refs | EvidenceRef binding references. |
| validation_refs | ValidationRef binding references. |
| security_refs | SecurityRef binding references. |
| approval_refs | ApprovalRef binding references. |
| retention_refs | RetentionRef binding references. |
| rollback_refs | RollbackRef binding references. |
| incident_refs | IncidentRef binding references. |
| message_intent | Safe metadata statement of intent, not executable instruction. |
| message_payload_metadata | Safe metadata about payload class, not payload content. |
| payload_content_posture | Whether content is metadata-only, blocked, local-only, generated-sensitive, product-restricted, external, secret, credential, or unknown. |
| source_classification | Highest inherited source classification. |
| sensitivity | Highest inherited sensitivity. |
| local_only_posture | Local-only posture and publication/provider-transmission blockers. |
| generated_output_posture | Generated-output posture and tracking blockers. |
| product_posture | Product/Siamese posture and product-bound blockers. |
| provider_auth_posture | Provider/auth/API/MCP posture and credential blockers. |
| tool_execution_posture | Tool execution posture and GT-07 blockers. |
| agent_execution_posture | Agent execution, task execution, and handoff execution blockers. |
| delivery_status | MessageDeliveryStatus value, default not_dispatched or dispatch_blocked. |
| dispatch_decision | MessageDispatchDecision metadata record. |
| human_review_required | Whether human review is required; true for any future dispatch. |
| blockers | MessageBlocker refs. |
| limitations | MessageLimitation refs. |
| pending_alignment_refs | P6 peer and substrate alignment markers. |

AgentMessageEnvelope must never embed raw source content, product source, external source content, live connector payloads, secrets, credentials, API keys, provider configs, token store content, browser auth, local credential store content, raw generated outputs, raw Graphify outputs, provider outputs, tool outputs, or agent execution outputs.

## 9. AgentMessageType Vocabulary

| AgentMessageType | Meaning |
| --- | --- |
| metadata_notice | General metadata notice. |
| context_reference_notice | Notice that references context metadata. |
| evidence_reference_notice | Notice that references EvidenceRef metadata. |
| validation_reference_notice | Notice that references ValidationRef metadata. |
| security_reference_notice | Notice that references SecurityRef metadata. |
| approval_request_reference | Metadata reference to a future approval request. |
| approval_decision_reference | Metadata reference to an approval decision record. |
| handoff_request_metadata | Metadata-only handoff request reference. |
| handoff_response_metadata | Metadata-only handoff response reference. |
| task_status_metadata | Metadata-only task status reference. |
| limitation_notice | Limitation metadata notice. |
| blocker_notice | Blocker metadata notice. |
| incident_reference_notice | IncidentRef metadata notice. |
| rollback_reference_notice | RollbackRef metadata notice. |
| retention_reference_notice | RetentionRef metadata notice. |
| monitoring_reference_notice | Monitoring reference notice, not monitoring runtime. |
| registry_reference_notice | Registry reference notice, not runtime. |
| capability_reference_notice | Capability reference notice, not capability execution. |
| unknown_message_type | Unknown type; blocks future dispatch eligibility. |

Message type is metadata only. Message type is not dispatch permission. Handoff request metadata is not handoff execution. Approval request reference is not active workflow. Incident reference notice is not incident automation. Monitoring reference notice is not monitoring runtime. Capability reference notice is not capability execution.

## 10. SenderRef / ReceiverRef Contract

SenderRef fields:

| Field | Required meaning |
| --- | --- |
| sender_ref_id | Stable sender metadata identifier. |
| sender_kind | Sender kind value. |
| sender_registry_ref | P6.1 AgentRegistryRecord ref when available, otherwise pending alignment. |
| sender_agent_ref | Agent metadata ref. |
| sender_capability_refs | Capability metadata refs. |
| sender_runtime_posture | Runtime posture, default metadata_only or blocked. |
| sender_activation_posture | Activation posture, default AL-1/non-active. |
| evidence_refs | EvidenceRef binding refs. |
| validation_refs | ValidationRef binding refs. |
| security_refs | SecurityRef binding refs. |
| blockers | Active sender blockers. |
| limitations | Sender limitations. |

ReceiverRef fields:

| Field | Required meaning |
| --- | --- |
| receiver_ref_id | Stable receiver metadata identifier. |
| receiver_kind | Receiver kind value. |
| receiver_registry_ref | P6.1 AgentRegistryRecord ref when available, otherwise pending alignment. |
| receiver_agent_ref | Agent metadata ref. |
| receiver_capability_refs | Capability metadata refs. |
| receiver_runtime_posture | Runtime posture, default metadata_only or blocked. |
| receiver_activation_posture | Activation posture, default AL-1/non-active. |
| evidence_refs | EvidenceRef binding refs. |
| validation_refs | ValidationRef binding refs. |
| security_refs | SecurityRef binding refs. |
| blockers | Active receiver blockers. |
| limitations | Receiver limitations. |

Allowed sender/receiver kinds: `agent_registry_record`, `agent_task_envelope`, `handoff_metadata_record`, `human_reviewer_ref`, `audit_record_ref`, `system_metadata_ref`, `unknown_ref`.

Blocked sender/receiver kinds: `live_agent_runtime`, `active_scheduler`, `active_orchestrator`, `live_connector`, `provider_runtime`, `MCP_runtime`, `product_runtime`, `GBrain_runtime`, `Hermes_runtime`, `Cadence_runtime`.

SenderRef and ReceiverRef are metadata references only. They do not wake agents, dispatch tasks, invoke tools, call providers, activate live connectors, or execute handoffs.

## 11. ConversationRef Contract

ConversationRef fields:

| Field | Required meaning |
| --- | --- |
| conversation_ref_id | Stable conversation metadata identifier. |
| conversation_scope | Exact metadata scope. |
| conversation_status | Conversation status value. |
| participating_refs | SenderRef, ReceiverRef, human reviewer, audit, or system metadata refs. |
| context_refs | ContextRef bindings. |
| evidence_refs | EvidenceRef bindings. |
| validation_refs | ValidationRef bindings. |
| security_refs | SecurityRef bindings. |
| approval_refs | ApprovalRef bindings. |
| retention_posture | Conversation retention posture. |
| rollback_posture | Conversation rollback posture. |
| incident_posture | Conversation incident posture. |
| blockers | Active blockers. |
| limitations | Known limitations. |

Conversation status values: `metadata_only`, `pending_alignment`, `blocked`, `deferred`, `closed_metadata_only`, `rejected_for_scope`, `unknown`.

ConversationRef is not a chat runtime, queue, thread store, websocket channel, or persistence layer.

## 12. HandoffRef Contract

HandoffRef fields:

| Field | Required meaning |
| --- | --- |
| handoff_ref_id | Stable handoff metadata identifier. |
| source_agent_ref | Source agent metadata ref. |
| target_agent_ref | Target agent metadata ref. |
| task_ref | AgentTaskEnvelope or task metadata ref. |
| context_refs | ContextRef bindings. |
| evidence_refs | EvidenceRef bindings. |
| validation_refs | ValidationRef bindings. |
| security_refs | SecurityRef bindings. |
| approval_refs | ApprovalRef bindings. |
| retention_refs | RetentionRef bindings. |
| rollback_refs | RollbackRef bindings. |
| incident_refs | IncidentRef bindings. |
| handoff_status | Handoff status value. |
| execution_posture | Handoff execution posture, default blocked. |
| blockers | Active handoff blockers. |
| limitations | Known handoff limitations. |

Handoff status values: `handoff_metadata_only`, `handoff_execution_blocked`, `handoff_pending_human_review`, `handoff_deferred`, `handoff_rejected_for_scope`, `unknown_handoff_status`.

HandoffRef is not handoff execution. HandoffRef is not task execution. HandoffRef is not scheduler activation. HandoffRef is not orchestration. HandoffRef must preserve context, evidence, validation, security, approval, retention, rollback, incident, product, tool, provider, and source-loading blockers.

## 13. ContextRef Binding Contract

ContextRef binding fields:

| Field | Required meaning |
| --- | --- |
| context_ref_id | Stable context metadata identifier. |
| context_pack_ref | ContextPack metadata ref. |
| context_item_refs | Context item metadata refs. |
| source_refs | SourceRef metadata refs. |
| context_scope | Exact context metadata scope. |
| context_inclusion_posture | Inclusion posture, not permission. |
| source_loading_posture | Source loading posture, default blocked. |
| sensitivity | Highest inherited sensitivity. |
| local_only_posture | Local-only blockers. |
| product_posture | Product/Siamese blockers. |
| external_posture | External source blockers. |
| generated_output_posture | Generated-output blockers. |
| blockers | Context blockers. |
| limitations | Context limitations. |

Context inclusion is not permission. ContextRef is not source loading. ContextRef is not provider-bound transmission approval. ContextRef is not product source inspection. ContextRef must preserve SourceRef, sensitivity, local-only, product, external, generated-output, secret, and credential blockers.

## 14. EvidenceRef / ValidationRef / SecurityRef Binding Contract

EvidenceRef binding fields:

| Field | Required meaning |
| --- | --- |
| evidence_ref_id | Stable EvidenceRef identifier. |
| evidence_scope | Exact evidence scope. |
| evidence_kind | Evidence kind. |
| authority_posture | Supporting evidence only unless governance says otherwise; GraphifyRef is not authority. |
| retention_posture | Evidence retention posture. |
| blockers | Evidence blockers. |
| limitations | Evidence limitations. |

ValidationRef binding fields:

| Field | Required meaning |
| --- | --- |
| validation_ref_id | Stable ValidationRef identifier. |
| validation_scope | Exact validation metadata scope. |
| validation_status | Validation status. |
| validation_execution_posture | Not executed or future-gated posture. |
| output_posture | Generated-sensitive unless future gates approve. |
| blockers | Validation blockers. |
| limitations | Validation limitations. |

SecurityRef binding fields:

| Field | Required meaning |
| --- | --- |
| security_ref_id | Stable SecurityRef identifier. |
| security_scope | Exact security metadata scope. |
| security_status | Security status. |
| sensitivity | Highest inherited sensitivity. |
| security_blockers | Security blockers. |
| incident_requirements | Required incident route metadata. |
| publication_blockers | Publication blockers. |
| limitations | Security limitations. |

Evidence supports; it does not decide. Validation evaluates; governance decides. Security constrains; it does not activate. EvidenceRef cannot approve dispatch. ValidationRef cannot approve dispatch. SecurityRef cannot activate dispatch. Unknown security posture blocks dispatch eligibility.

## 15. ApprovalRef Binding Contract

ApprovalRef binding fields:

| Field | Required meaning |
| --- | --- |
| approval_ref_id | Stable ApprovalRef metadata identifier. |
| approval_scope | Exact approval metadata scope. |
| reviewer_ref | Human reviewer or governance reviewer metadata ref. |
| approval_status | Approval status value. |
| approval_conditions | Exact conditions and remaining blockers. |
| approval_expiry | Expiry timestamp or metadata expiry condition. |
| denied_actions | Explicit denied actions. |
| human_review_required | Whether human review is required; true for future dispatch. |
| blockers | Approval blockers. |
| limitations | Approval limitations. |

Approval status values: `approval_not_requested`, `approval_required`, `approval_pending`, `approval_metadata_recorded`, `approval_denied`, `approval_expired`, `approval_blocked`, `unknown_approval_status`.

ApprovalRef is not approval. ApprovalRef is not active workflow. ApprovalRef is not auto-approval. Passing validation is not approval. Security dry-run is not approval. Evidence is not approval. Registry presence is not approval. User intent without exact scope is not approval. Dispatch eligibility must require explicit human approval before any future active protocol.

## 16. MessageDeliveryStatus Contract

MessageDeliveryStatus values:

| Value | Meaning |
| --- | --- |
| not_dispatched | No message was dispatched. |
| dispatch_blocked | Dispatch is blocked. |
| dispatch_deferred | Dispatch is deferred to future gate review. |
| pending_human_review | Human review is required before future dispatch review. |
| pending_peer_alignment | P6 peer alignment is pending. |
| metadata_recorded | Envelope exists as documentation metadata only. |
| rejected_for_scope | Scope rejected. |
| expired_metadata | Metadata expired. |
| superseded_metadata | Metadata superseded. |
| unknown_delivery_status | Unknown status; blocks future dispatch eligibility. |

Delivery status is metadata only. `metadata_recorded` means the envelope exists as documentation metadata, not that a message was delivered. P6.2 default delivery status must be `not_dispatched` or `dispatch_blocked`.

## 17. MessageDispatchDecision Contract

MessageDispatchDecision fields:

| Field | Required meaning |
| --- | --- |
| decision_id | Stable dispatch decision metadata identifier. |
| message_id | AgentMessageEnvelope identifier. |
| decision_status | Dispatch decision status value. |
| decision_reason | Safe metadata reason. |
| dispatch_allowed | Boolean; required default false. |
| runtime_activation_required | Boolean; true for any future dispatch. |
| human_approval_required | Boolean; true for any future dispatch. |
| required_gates | Future exact gates required. |
| required_validation_refs | Required ValidationRef metadata. |
| required_security_refs | Required SecurityRef metadata. |
| required_approval_refs | Required ApprovalRef metadata. |
| required_retention_refs | Required RetentionRef metadata. |
| required_rollback_refs | Required RollbackRef metadata. |
| required_incident_refs | Required IncidentRef metadata. |
| blocked_actions | Explicit blocked actions. |
| side_effect_profile | Side effects; none for P6.2. |
| limitations | Decision limitations. |

Decision status values: `dispatch_not_allowed`, `dispatch_deferred`, `dispatch_blocked`, `metadata_only_recorded`, `candidate_for_future_exact_dispatch_review`, `rejected_for_scope`, `unknown_dispatch_decision`.

Required defaults: `dispatch_allowed` = false. `runtime_activation_required` = true for any future dispatch. `human_approval_required` = true for any future dispatch. Side effects = none for P6.2.

MessageDispatchDecision is not dispatch execution. Any future dispatch requires separate exact-scope activation gate approval.

## 18. Boundary Model

| boundary | expected_posture | protocol_rule | blocked_current_behavior | required_future_gate |
| --- | --- | --- | --- | --- |
| runtime activation boundary | AL-1 metadata skeleton | Protocol contract only. | Runtime activation. | Future exact activation gate. |
| agent execution boundary | blocked | Agent metadata is not agent execution. | Agent execution. | GT-06 or successor exact gate. |
| task execution boundary | blocked | Task refs remain metadata. | Task execution. | Future exact runtime/task approval. |
| handoff execution boundary | blocked | HandoffRef is not handoff execution. | Handoff execution. | Future exact handoff approval. |
| message dispatch boundary | blocked | no message dispatch by P6.2. | Dispatching messages. | Future exact dispatch activation gate. |
| queue/broker/websocket boundary | blocked | Protocol creates no queue, broker, websocket, network channel, or runtime bus. | Queue, broker, websocket runtime. | Future exact transport/runtime gate. |
| scheduler/orchestration/autonomous loop boundary | blocked | Protocol creates no scheduler, orchestration, or loop. | Scheduler, orchestration, autonomous loop. | Future exact scheduler/orchestration gate. |
| tool execution boundary | blocked | Tool refs remain metadata. | Tool execution. | GT-07 or successor exact gate. |
| provider/auth/API/MCP boundary | blocked | Provider refs remain metadata and cannot transmit context. | Provider calls, auth, API, MCP. | GT-08 or successor exact gate. |
| credential/API key boundary | blocked | Secrets, credentials, API keys, token stores, browser auth, provider configs, and local credential stores are excluded. | Credential use or inspection. | Secure exact approval and incident posture. |
| live connector boundary | blocked | Live connector refs are metadata only. | Live connector activation. | Future exact connector/provider gate. |
| source loading boundary | blocked | ContextRef and SourceRef are metadata only. | Source loading. | Future exact source gate. |
| product source boundary | blocked | ProductRef is readiness metadata only. | Product/Siamese source inspection. | P4/GT-09 or successor exact product gate. |
| external source boundary | blocked | External refs are metadata only. | External source content inspection or adoption. | EXT.* and exact source gate. |
| GBrain/Hermes/Cadence boundary | future inactive | Protocol cannot adopt or activate them. | GBrain/Hermes/Cadence activation. | EXT.* plus exact runtime gates. |
| Graphify/Codegraph boundary | supporting only | GraphifyRef is generated supporting evidence only. | Graphify rerun/adoption or Codegraph execution. | EXT.CODEGRAPH/Graphify exact review. |
| persistence/database/event stream boundary | blocked | Protocol metadata does not create persistence or event stream. | Database, persistence, event streaming. | Future exact persistence/state gate. |
| telemetry boundary | blocked | MessageDeliveryStatus is not telemetry. | Telemetry pipeline. | Future exact telemetry/privacy gate. |
| vector DB / embeddings boundary | blocked | No retrieval substrate is implemented. | Vector DB, embeddings generation. | Future Cognitive Semantic System/substrate gate. |
| graph DB / ontology runtime boundary | blocked | No graph DB or ontology runtime is implemented. | Graph DB, ontology runtime. | Future Cognitive Semantic System/substrate gate. |
| generated output tracking boundary | blocked | Generated-output posture is metadata only. | Generated output tracking. | GT-12/GT-15 or successor exact gate. |
| source tracking / publication boundary | blocked | Source tracking and publication remain blocked. | Source tracking expansion, publication, Git mutation. | GT-02/GT-12 and exact human approval. |
| Cognitive Semantic System substrate boundary | deferred | P6.2 does not select substrate. | Substrate selection or persistence. | P6.6 if needed plus exact substrate gate. |

## 19. Interfaces With P5 Skeletons

P5.6 interface:

| Rule | P6.2 posture |
| --- | --- |
| AgentMessageEnvelope may reference AgentTaskEnvelope. | Allowed as metadata reference only. |
| HandoffRef may reference AgentHandoffEnvelope. | Allowed as metadata reference only. |
| AgentExecutionDecision blockers must propagate. | Required. |
| No agent execution is approved. | Preserved. |
| No task execution is approved. | Preserved. |
| No handoff execution is approved. | Preserved. |

P5.7 interface:

| Rule | P6.2 posture |
| --- | --- |
| Message envelopes must include retention, rollback, and incident posture. | Required. |
| Protocol metadata must not activate audit sinks. | Preserved. |
| No event logging runtime is approved. | Preserved. |
| No persistence is approved. | Preserved. |
| No incident automation is approved. | Preserved. |

P5.3 interface:

| Rule | P6.2 posture |
| --- | --- |
| ContextRef bindings must preserve ContextPack / ContextSourceRef limitations. | Required. |
| No source loading is approved. | Preserved. |
| Unknown sensitivity blocks future dispatch eligibility. | Required. |

P5.4 interface:

| Rule | P6.2 posture |
| --- | --- |
| Tool refs in messages remain metadata only. | Required. |
| Tool metadata is not tool execution. | Preserved. |
| Messages cannot invoke tools. | Required. |

P5.5 interface:

| Rule | P6.2 posture |
| --- | --- |
| Provider refs in messages remain metadata only. | Required. |
| Provider metadata is not provider activation. | Preserved. |
| Messages cannot call providers or transmit context to providers. | Required. |

P5.2 interface:

| Rule | P6.2 posture |
| --- | --- |
| Security dry-run refs may constrain messages. | Allowed. |
| Security dry-run is not enforcement. | Preserved. |
| Security dry-run cannot approve dispatch. | Required. |

## 20. Interfaces With P3 Decisions

| P3 decision | Interface rule | P6.2 posture |
| --- | --- | --- |
| P3.3 | Tool execution activation decision remains deferred or exact-scope only. | Protocol must not create tool execution; any message referring to tool capability must preserve tool blockers. |
| P3.4 | Provider/auth/API/MCP activation decision remains deferred or exact-scope only. | Protocol must not create provider calls, auth, network, MCP, or live connector activity; provider-bound context transmission remains blocked. |
| P3.5 | Agent runtime activation decision remains constrained by P3.3/P3.4 alignment. | Protocol must not activate agent runtime; protocol may define future communication metadata only. |
| P3.BR | P3-B activation decisions remain canonical. | P6.2 must not override P3-B decisions; decision is not execution. |

## 21. Interfaces With P6.1 / P6.3 / P6.4 / P6.5

| Peer | Interface rule | Current posture |
| --- | --- | --- |
| P6.1 | SenderRef and ReceiverRef should align with AgentRegistryRecord when P6.1 exists. Capability references should align with AgentCapabilityRecord when P6.1 exists. | P6.1 absent; mark `pending_P6.1_agent_registry_alignment`. |
| P6.3 | ContextRef and EvidenceRef bindings should align with Shared Context / Evidence Bus contract when P6.3 exists. | P6.3 absent; mark `pending_P6.3_context_evidence_bus_alignment`. |
| P6.4 | ApprovalRef binding should align with Human Approval / Review Loop contract when P6.4 exists. | P6.4 absent; mark `pending_P6.4_human_approval_alignment`. |
| P6.5 | IncidentRef, monitoring references, and delivery status should align with Runtime Monitoring / Incident Handling contract when P6.5 exists. | P6.5 absent; mark `pending_P6.5_monitoring_incident_alignment`. |

## 22. Evidence / Validation / Security Interfaces

Evidence interface:

| Rule | P6.2 posture |
| --- | --- |
| Every message envelope must preserve EvidenceRef posture. | Required. |
| Evidence supports; it does not decide. | Preserved. |
| GraphifyRef is supporting generated evidence only, not authority. | Preserved. |
| ProductRef is product-readiness metadata only. | Preserved. |

Validation interface:

| Rule | P6.2 posture |
| --- | --- |
| ValidationRef may be attached to message metadata. | Allowed. |
| ValidationRef cannot approve dispatch. | Required. |
| ValidationRef cannot approve agent execution. | Required. |
| ValidationRef cannot approve handoff execution. | Required. |
| Validation output remains generated-sensitive unless future gates approve. | Required. |

Security interface:

| Rule | P6.2 posture |
| --- | --- |
| SecurityRef must constrain message eligibility. | Required. |
| Security constrains; it does not activate. | Preserved. |
| Secret/credential-related messages are blocked. | Required. |
| Unknown sensitivity blocks future dispatch eligibility. | Required. |
| Security dry-run metadata cannot become active enforcement by being referenced. | Required. |

## 23. Retention / Rollback / Incident Posture

Protocol retention posture fields:

| Field | Required meaning |
| --- | --- |
| message_retention_posture | Metadata-only retention posture for the envelope. |
| context_ref_retention_posture | Retention posture for ContextRef bindings. |
| evidence_retention_posture | Retention posture for EvidenceRef bindings. |
| approval_ref_retention_posture | Retention posture for ApprovalRef bindings. |
| generated_output_retention_posture | Generated-output retention and tracking blocker posture. |
| local_only_retention_posture | Local-only retention and publication blocker posture. |
| publication_posture | Publication posture, default blocked. |
| source_tracking_posture | Source tracking posture, default not approved. |

Rollback posture fields:

| Field | Required meaning |
| --- | --- |
| rollback_ref_id | Stable RollbackRef metadata identifier. |
| rollback_owner | Accountable owner. |
| rollback_trigger | Trigger condition. |
| impacted_message_refs | Message metadata refs impacted. |
| dispatch_reversal_required | Whether future dispatch reversal would be required. |
| metadata_supersession_route | Route to supersede metadata. |
| publication_reversal_route | Route to reverse publication if ever approved later. |
| source_tracking_reversal_route | Route to reverse source tracking if ever approved later. |
| limitations | Rollback limitations. |

Incident posture fields:

| Field | Required meaning |
| --- | --- |
| incident_ref_id | Stable IncidentRef metadata identifier. |
| incident_trigger | Incident trigger value. |
| immediate_stop_required | Whether immediate stop is required. |
| quarantine_required | Whether quarantine/removal review is required. |
| unsafe_content_repetition_blocked | Whether unsafe content repetition is blocked. |
| governance_review_required | Whether governance review is required. |
| security_review_required | Whether security review is required. |
| validation_review_required | Whether validation review is required. |
| recovery_conditions | Conditions before recovery or future review. |
| limitations | Incident limitations. |

Incident triggers: `secret_exposure`, `credential_exposure`, `API_key_exposure`, `provider_config_exposure`, `token_store_exposure`, `browser_auth_exposure`, `local_credential_store_exposure`, `product_source_exposure`, `raw_generated_output_exposure`, `live_connector_payload_exposure`, `unauthorized_dispatch`, `unauthorized_handoff_execution`, `unauthorized_agent_execution`, `unauthorized_tool_execution`, `unauthorized_provider_call`, `unauthorized_MCP_call`, `unauthorized_network_call`, `unauthorized_scheduler_activation`, `unauthorized_orchestration_activation`, `unauthorized_Cadence_activation`, `generated_output_tracking_violation`, `source_tracking_violation`, `publication_violation`.

## 24. Human Approval Requirements

Any future active message dispatch requires explicit human approval.

Human approval requirements:

| Requirement | Meaning |
| --- | --- |
| exact sender | SenderRef must be exact. |
| exact receiver | ReceiverRef set must be exact. |
| exact message type | AgentMessageType must be exact. |
| exact conversation scope | ConversationRef scope must be exact. |
| exact handoff scope, if any | HandoffRef scope must be exact. |
| exact context refs | ContextRef set must be exact. |
| exact evidence refs | EvidenceRef binding set must be exact. |
| exact validation refs | ValidationRef binding set must be exact. |
| exact security refs | SecurityRef binding set must be exact. |
| exact approval refs | ApprovalRef binding set must be exact. |
| exact data sent | Data sent must be exact and safe. |
| exact data received | Expected data received must be exact. |
| exact retention posture | Retention posture must be exact. |
| exact rollback posture | Rollback posture must be exact. |
| exact incident route | Incident route must be exact. |
| exact side effect profile | Side effects must be exact. |
| exact stop rules | Stop rules must be exact. |
| explicit expiry | Approval expiry must be explicit. |
| emergency stop owner | Emergency stop owner must be explicit. |

ApprovalRef is not approval. Human approval must be exact-scope. Broad approval is blocked. AI self-approval is blocked. Implicit approval from refs is blocked. Approval by validation/security/evidence/registry presence is blocked.

## 25. Stop Rules

| Stop rule | Required action |
| --- | --- |
| Stop if any message would be dispatched. | Stop and report blocker. |
| Stop if any queue, broker, websocket, network channel, MCP channel, or runtime bus would be created. | Stop and report blocker. |
| Stop if any agent would be woken, scheduled, invoked, or executed. | Stop and report blocker. |
| Stop if any task or handoff would execute. | Stop and report blocker. |
| Stop if any scheduler/orchestration/autonomous loop would be activated. | Stop and report blocker. |
| Stop if any tool would execute. | Stop and report blocker. |
| Stop if any provider/API/network/MCP call would occur. | Stop and report blocker. |
| Stop if any credential, API key, token, `.env`, provider config, token store, browser auth, or local credential store would be accessed. | Stop and report safe metadata only. |
| Stop if any live connector would activate. | Stop and report blocker. |
| Stop if any source loading would occur. | Stop and report blocker. |
| Stop if any product/Siamese source would be inspected. | Stop and report blocker. |
| Stop if any external source content would be inspected. | Stop and report blocker. |
| Stop if GBrain/Hermes/Cadence would activate, execute, import, configure, or be adopted. | Stop and report blocker. |
| Stop if Graphify/Codegraph would run or be adopted. | Stop and report blocker. |
| Stop if validation/tests/CI/scripts/builds would run. | Stop and report blocker. |
| Stop if security enforcement would activate. | Stop and report blocker. |
| Stop if persistence/database/event streaming/telemetry would be created. | Stop and report blocker. |
| Stop if vector DB, embeddings, graph DB, ontology runtime, or substrate would be implemented. | Stop and report blocker. |
| Stop if generated output tracking, source tracking expansion, publication, or Git mutation would occur. | Stop and report blocker. |
| Stop if any task exceeds metadata-only protocol scope. | Stop and report blocker. |

## 26. Future Validation Targets

Future validation targets, not executed:

| Target | Purpose |
| --- | --- |
| AgentMessageEnvelope required fields completeness | Check required envelope fields. |
| AgentMessageType vocabulary conformance | Check message type values. |
| SenderRef / ReceiverRef schema conformance | Check sender and receiver refs. |
| ConversationRef schema conformance | Check conversation refs. |
| HandoffRef non-execution invariant | Check handoff ref cannot execute. |
| ContextRef no-source-loading invariant | Check no source loading. |
| EvidenceRef binding support-only invariant | Check evidence cannot decide. |
| ValidationRef no-approval invariant | Check validation cannot approve. |
| SecurityRef no-activation invariant | Check security cannot activate. |
| ApprovalRef is not approval invariant | Check approval metadata boundary. |
| MessageDeliveryStatus non-dispatch invariant | Check status is metadata only. |
| MessageDispatchDecision dispatch_allowed_false invariant | Check dispatch_allowed false. |
| no queue/broker/websocket/network/MCP invariant | Check no transport/runtime creation. |
| no scheduler/orchestration/autonomous loop invariant | Check no loop activation. |
| no provider/tool/agent execution invariant | Check execution blockers. |
| no persistence/event stream/telemetry invariant | Check no persistence or telemetry. |
| no secret/no-credential message content invariant | Check no secret or credential content without scanning values. |
| local-only/product/external blockers propagation | Check blockers travel downstream. |
| retention/rollback/incident posture completeness | Check posture fields. |
| P6.1 registry alignment check | Future peer alignment. |
| P6.3 context/evidence bus alignment check | Future peer alignment. |
| P6.4 human approval alignment check | Future peer alignment. |
| P6.5 monitoring/incident alignment check | Future peer alignment. |
| P6.7 operational readiness reconciliation check | Future reconciliation only. |

## 27. Future Hardening Candidates

Future tickets, not started:

| Candidate | Purpose |
| --- | --- |
| MSG-HARD-01 - AgentMessageEnvelope Schema Alignment | Align canonical envelope schema. |
| MSG-HARD-02 - SenderRef / ReceiverRef Registry Alignment | Align sender/receiver refs with registry. |
| MSG-HARD-03 - HandoffRef Non-Execution Boundary Contract | Harden handoff non-execution boundary. |
| MSG-HARD-04 - MessageDispatchDecision Gate Contract | Harden dispatch decision gates. |
| MSG-HARD-05 - ApprovalRef Binding / Human Review Alignment | Align approval binding with human review. |
| MSG-HARD-06 - ContextRef / EvidenceRef Message Binding Contract | Harden context/evidence bindings. |
| MSG-HARD-07 - Message Retention / Rollback / Incident Posture Contract | Harden safety posture. |
| MSG-HARD-08 - No-Dispatch / No-Queue / No-Broker Validation Target Design | Define future validation targets. |
| MSG-HARD-09 - Cross-P6 Protocol Reconciliation Hardening | Reconcile P6 peer contracts. |
| MSG-HARD-10 - Future Active Messaging Gate Design | Define future active messaging gate only if explicitly approved. |

## 28. Created / Not Created Register

Created:

| Artifact | Status |
| --- | --- |
| `0_architecture/governance/agent_platform_agent_to_agent_communication_protocol.md` | Created. |

Not created / not approved:

| Item | Posture |
| --- | --- |
| runtime activation | no runtime activation |
| agent execution | no agent execution |
| task execution | no task execution |
| handoff execution | no handoff execution |
| message dispatch | no message dispatch |
| queue | no queue |
| broker | no broker |
| websocket | no websocket |
| network | no network |
| MCP | no MCP |
| provider call | no provider call |
| agent wake-up | no agent wake-up |
| scheduler activation | no scheduler activation |
| orchestration activation | no orchestration activation |
| autonomous loop activation | no autonomous loop activation |
| tool execution | no tool execution |
| provider/auth/API/MCP activation | no provider/auth/API/MCP activation |
| credential use | no credential use |
| API calls | no API calls |
| live connector activation | no live connector activation |
| source loading | no source loading |
| source inspection | no source inspection |
| product source inspection | no product source inspection |
| external source inspection | no external source inspection |
| GBrain source inspection | no GBrain source inspection |
| Hermes source inspection | no Hermes source inspection |
| GBrain/Hermes/Cadence activation | no GBrain/Hermes/Cadence activation |
| Graphify/Codegraph adoption or execution | no Graphify/Codegraph adoption or execution |
| validation execution | no validation execution |
| tests / CI / scripts / builds executed | no tests / CI / scripts / builds executed |
| security enforcement activation | no security enforcement activation |
| persistence/database/event stream | no persistence/database/event stream |
| telemetry | no telemetry |
| vector DB / embeddings | no vector DB / embeddings |
| graph DB / substrate implementation | no graph DB / substrate implementation |
| generated output tracking | no generated output tracking |
| source tracking expansion | no source tracking expansion |
| publication | no publication |
| Git mutation | no Git mutation |
| P6.1 file created | no P6.1 file created |
| P6.3 file created | no P6.3 file created |
| P6.4 file created | no P6.4 file created |
| P6.5 file created | no P6.5 file created |
| P6.6 file created | no P6.6 file created |
| P6.7 file created | no P6.7 file created |
| P4/P7/EXT.* file created | no P4/P7/EXT.* file created |

## 29. Recommended Next Tickets

After P6.2:

| Ticket | Recommendation |
| --- | --- |
| P6.1 - Agent Registry / Capability Registry | Complete if not already completed. |
| P6.3 - Shared Context / Evidence Bus | Complete after or alongside P6.1 alignment. |
| P6.4 - Human Approval / Review Loop | Complete after protocol and approval binding review. |
| P6.5 - Runtime Monitoring / Incident Handling | Complete after incident/delivery posture alignment. |
| P6.6 - Cognitive Semantic System Substrate Decision | Only if needed. |
| P6.7 - Operational Readiness Audit | Only after P6.1-P6.5 are complete and P6.6 is created or explicitly deferred. |

Recommended actual: P6.3 - Shared Context / Evidence Bus, if P6.1 is already running or complete. Otherwise: P6.1 - Agent Registry / Capability Registry.

Do not start P6.3, P6.4, P6.5, P6.6, or P6.7 from this ticket.

## 30. Final Verdict

| Question | Answer |
| --- | --- |
| What did P6.2 create? | `0_architecture/governance/agent_platform_agent_to_agent_communication_protocol.md`. |
| What agent-to-agent communication protocol was defined? | A metadata-only Agent-to-Agent Communication Protocol for future agent message envelopes, refs, bindings, delivery status, dispatch decisions, blockers, retention, rollback, and incident posture. |
| What AgentMessageEnvelope fields are required? | message_id, message_type, sender_ref, receiver_refs, conversation_ref, handoff_ref, context_refs, evidence_refs, validation_refs, security_refs, approval_refs, retention_refs, rollback_refs, incident_refs, message_intent, message_payload_metadata, payload_content_posture, source_classification, sensitivity, local_only_posture, generated_output_posture, product_posture, provider_auth_posture, tool_execution_posture, agent_execution_posture, delivery_status, dispatch_decision, human_review_required, blockers, limitations, pending_alignment_refs. |
| What AgentMessageType values were defined? | metadata_notice, context_reference_notice, evidence_reference_notice, validation_reference_notice, security_reference_notice, approval_request_reference, approval_decision_reference, handoff_request_metadata, handoff_response_metadata, task_status_metadata, limitation_notice, blocker_notice, incident_reference_notice, rollback_reference_notice, retention_reference_notice, monitoring_reference_notice, registry_reference_notice, capability_reference_notice, unknown_message_type. |
| What SenderRef and ReceiverRef rules were defined? | SenderRef and ReceiverRef are metadata references only; allowed kinds are metadata refs; live runtimes, schedulers, orchestrators, connectors, providers, MCP, product, GBrain, Hermes, and Cadence runtimes are blocked. |
| What ConversationRef rules were defined? | ConversationRef is metadata only and not a chat runtime, queue, thread store, websocket channel, or persistence layer. |
| What HandoffRef rules were defined? | HandoffRef is metadata only and not handoff execution, task execution, scheduler activation, or orchestration. |
| What ContextRef binding rules were defined? | ContextRef is not source loading, provider-bound transmission approval, or product source inspection; SourceRef, sensitivity, local-only, product, external, generated-output, secret, and credential blockers must propagate. |
| What EvidenceRef / ValidationRef / SecurityRef binding rules were defined? | Evidence supports but does not decide; Validation evaluates but governance decides; Security constrains but does not activate; none can approve or activate dispatch. |
| What ApprovalRef binding rules were defined? | ApprovalRef is not approval, active workflow, or auto-approval; future dispatch requires exact human approval. |
| What MessageDeliveryStatus values were defined? | not_dispatched, dispatch_blocked, dispatch_deferred, pending_human_review, pending_peer_alignment, metadata_recorded, rejected_for_scope, expired_metadata, superseded_metadata, unknown_delivery_status. |
| What MessageDispatchDecision values were defined? | dispatch_not_allowed, dispatch_deferred, dispatch_blocked, metadata_only_recorded, candidate_for_future_exact_dispatch_review, rejected_for_scope, unknown_dispatch_decision. |
| What boundaries were preserved? | Runtime, agent, task, handoff, dispatch, queue/broker/websocket, scheduler/orchestration, tool, provider/auth/API/MCP, credential, live connector, source, product, external, GBrain/Hermes/Cadence, Graphify/Codegraph, persistence, telemetry, vector/embedding, graph/substrate, generated-output tracking, source tracking, publication, and Cognitive Semantic System substrate boundaries. |
| How does P6.2 interface with P5.6 and P5.7? | It may reference P5.6 task/handoff envelopes and must propagate P5.6 execution blockers; it must include P5.7 retention, rollback, and incident posture without activating sinks, persistence, or automation. |
| How does P6.2 interface with P3 decisions? | It preserves P3.3 tool, P3.4 provider/auth/API/MCP, P3.5 agent runtime, and P3.BR canonical non-execution decisions. |
| How does P6.2 interface with P6.1, P6.3, P6.4, and P6.5? | It anticipates alignment with registry, context/evidence bus, human approval loop, and monitoring/incident contracts when those peer docs exist. |
| What pending alignment markers were recorded? | `pending_P6.1_agent_registry_alignment`, `pending_P6.3_context_evidence_bus_alignment`, `pending_P6.4_human_approval_alignment`, `pending_P6.5_monitoring_incident_alignment`, `substrate_decision_not_required_by_P6.2`. |
| Did P6.2 dispatch messages? | No. |
| Did P6.2 create a queue, broker, websocket, network, MCP, or runtime bus? | No. |
| Did P6.2 wake agents? | No. |
| Did P6.2 activate scheduler or orchestration? | No. |
| Did P6.2 execute handoffs? | No. |
| Did P6.2 execute tools? | No. |
| Did P6.2 call providers or APIs? | No. |
| Did P6.2 activate live connectors? | No. |
| Did P6.2 load source? | No. |
| Did P6.2 inspect product source? | No. |
| Did P6.2 activate GBrain/Hermes/Cadence? | No. |
| Did P6.2 adopt Graphify/Codegraph? | No. |
| Did P6.2 run validation/tests/CI/scripts/builds? | No. |
| Did P6.2 activate security enforcement? | No. |
| Did P6.2 create persistence/database/event streaming/telemetry? | No. |
| Did P6.2 implement vector DB, embeddings, graph DB, or substrate? | No. |
| Did P6.2 approve generated output tracking or source tracking expansion? | No. |
| Does AGENT PLATFORM remain AL-1? | Yes. |
| What is the recommended next ticket? | P6.1 - Agent Registry / Capability Registry, unless P6.1 is already running or complete; then P6.3 - Shared Context / Evidence Bus. |

Stop after P6.2. Do not start P6.1, P6.3, P6.4, P6.5, P6.6, P6.7, P4, P7, EXT.*, runtime code, activation, dispatch, queues, brokers, websockets, network channels, MCP channels, runtime buses, agent wake-up, scheduler/orchestration/autonomous loops, task execution, handoff execution, tool execution, provider/auth configuration, provider/API/network/MCP calls, credential use, secret inspection, source loading, product source inspection, external source content inspection, GBrain/Hermes/Graphify content inspection, validation, tests, CI, scripts, builds, security enforcement, persistence/database/event streaming/telemetry, vector DB, embeddings, graph DB, Cognitive Semantic System persistence, substrate selection, generated output tracking, source tracking expansion, publication, staging, commit, push, force-add, or publication.
