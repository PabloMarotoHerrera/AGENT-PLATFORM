# P2.1 - Shared Metadata Vocabulary Alignment

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Shared Metadata Vocabulary Alignment |
| Ticket | P2.1 |
| Status | Accepted shared metadata vocabulary alignment |
| Date | 2026-07-04 |
| Scope | Align shared metadata vocabulary across P1.1 through P1.5 metadata-only contracts for AGENT PLATFORM / Siamese. |
| Authority | Cross-lane metadata vocabulary alignment only, not runtime activation, source loading, source tracking approval, generated output tracking approval, provider/auth approval, tool execution approval, agent execution approval, validation execution approval, product activation, Graphify adoption, Cognitive Semantic System substrate selection, or publication. |
| Related documents | P0.1, P0.2, P0.3, G-19, P1.1, P1.2, P1.3, P1.4, P1.5, I-A, I-01, I-02, I-03, I-04, I-05, I-06, I-07, S-03, S-04, CSS ADR/audit, Graphify Repo Map Summary, `.gitignore`, `.graphifyignore`. |
| Output | Shared metadata vocabulary alignment. |

P2.1 is vocabulary alignment only. It creates canonical vocabulary, alias guidance, deprecated term guidance, and downstream consumption rules without modifying P1 documents.

## 2. Purpose
P1 hardened lane-specific metadata contracts for context, providers, tools, agents, and Cognitive Semantic System records. P2.1 aligns the common vocabulary across P1.1-P1.5 so future cross-lane records use consistent names for status, blocker, sensitivity, source classification, posture, and reference fields.

P2.1 resolves drift between parallel agent outputs by choosing canonical terms and recording aliases/deprecated terms. It prepares vocabulary input for P2.2 and P2.3.

P2.1 does not activate runtime. P2.1 does not execute validation. P2.1 does not approve source loading. P2.1 does not start P2.2, P2.3, P3.1, or P3.2.

AGENT PLATFORM remains pre-active at AL-1.

## 3. Current Cross-Lane Posture
| Lane | Source document | Current posture | Integration need | P2.1 result |
| --- | --- | --- | --- | --- |
| P1.1 Context | `agent_platform_context_runtime_contract_hardening.md` | Metadata-only context contract. | Align context refs, source refs, sensitivity, blockers, retention, and evidence terms. | Canonical context-related vocabulary mapped. |
| P1.2 Provider | `agent_platform_provider_adapter_metadata_contract_hardening.md` | Metadata-only provider/adapter contract. | Align provider/auth/network/MCP, credential refs, blockers, and provider refs. | Canonical provider_auth_posture and provider blocker terms mapped. |
| P1.3 Tool | `agent_platform_tool_execution_boundary_contract_hardening.md` | Metadata-only tool boundary contract. | Align tool risk, execution status, tool blockers, generated output, and audit expectations. | Canonical execution_status and tool blocker terms mapped. |
| P1.4 Agent | `agent_platform_agent_runtime_boundary_contract_hardening.md` | Metadata-only agent runtime boundary contract. | Align agent refs, task/handoff metadata, approval metadata, execution posture, and output posture. | Canonical agent metadata and execution blocker vocabulary mapped. |
| P1.5 Cognitive Semantic System | `agent_platform_cognitive_semantic_system_prototype_hardening.md` | Metadata-only semantic prototype contract. | Align semantic refs, substrate posture, Graphify evidence, and semantic retention terms. | Canonical substrate_posture and semantic ref vocabulary mapped. |

All P1 lanes remain metadata-only. AGENT PLATFORM remains pre-active at AL-1. P2.1 is vocabulary alignment only. No P1 contract becomes activation approval through P2.1.

## 4. Alignment Method
| Step | Method |
| --- | --- |
| Collect observed terms | Read P1.1-P1.5 terms for statuses, blockers, source classes, sensitivity classes, posture fields, and reference fields. |
| Group equivalent terms | Group terms by shared concept even when lane-specific names differ. |
| Choose canonical term | Select a term that is clear, cross-lane, and preserves gate discipline. |
| Preserve stricter safety meaning | When terms differ, keep the stronger non-activation, security, retention, or review meaning. |
| Record aliases | Keep lane terms as compatibility aliases where safe. |
| Mark deprecated terms | Mark ambiguous or permission-implying terms as deprecated or prohibited. |
| Record drift rationale | Explain why a canonical term was chosen. |
| Preserve lane-specific prefixes | Keep names such as `ContextEvidenceRef` or `SemanticEvidenceRef` when clarity requires lane context. |
| Standardize shared fields | Prefer shared fields such as `evidence_refs`, `validation_refs`, `security_refs`, `blockers`, `limitations`, and `retention_posture`. |
| Default mixed terms strictly | Unknown or mixed terms default to blocked or needs review. |
| Avoid retroactive edits | P2.1 does not modify P1 documents. |
| Prepare downstream vocabulary | P2.2 and P2.3 should consume this alignment. |

If two terms conflict, choose the term that preserves the stricter gate, security, retention, or non-activation interpretation.

## 5. Canonical Vocabulary Principles
| Principle | Rule |
| --- | --- |
| Canonical terms | Naming standards, not permissions. |
| Aliases | Compatibility notes, not new concepts. |
| Deprecated terms | Historical only unless listed in a register. |
| Status fields | Never grant execution authority by themselves. |
| Posture fields | Describe governance state, not runtime state. |
| Evidence terms | Do not create authority. Evidence supports; it does not decide. |
| Validation terms | Do not create governance decisions. Validation evaluates; governance decides. |
| Security terms | Constrain actions; they do not activate actions. |
| Source classifications | Preserve sensitivity and access posture. |
| Generated-output terms | Preserve local-only/generated-sensitive posture. |
| Product terms | Preserve product inactivity and GT-09 boundary. |
| Substrate terms | Preserve deferral. Cognitive Semantic System substrate remains deferred. |
| Graphify terms | Preserve supporting-evidence-only status. Graphify evidence is supporting generated evidence only, not authority. |

## 6. Canonical Status Vocabulary
### record_status
| Canonical value | Meaning | Allowed current P2 use | Blocked interpretation | Aliases/deprecated terms | Source lanes observed |
| --- | --- | --- | --- | --- | --- |
| `draft` | Incomplete metadata record. | Planning state. | Approval or activation. | proposed draft | P1.1-P1.5 |
| `metadata_only` | Safe metadata record only. | Cross-lane non-runtime posture. | Runtime readiness. | approved_metadata_only, metadata_only_allowed | P1.1-P1.5 |
| `accepted_metadata_contract` | Accepted documentation contract. | Contract-level acceptance. | Runtime activation. | accepted hardening | P1.1-P1.5 |
| `blocked` | Stop condition active. | Preserve blocker. | Workaround permission. | blocked_by_security, blocked_by_validation | P1.2-P1.4 |
| `needs_review` | Review required. | Route to governance/security/validation. | Approval. | requires_review | P1.1-P1.5 |
| `deferred` | Future review required. | Preserve open state. | Silent approval. | activation_deferred | P1.3-P1.5 |
| `rejected_for_scope` | Scope unsafe or wrong. | Stop and rescope. | Adjacent approval. | rejected | P1.1-P1.5 |
| `superseded` | Replaced by newer record. | Historical trace. | Current authority. | replaced | P1.1-P1.5 |
| `retired` | No current use. | Historical trace. | Current authority. | inactive historical | P1.1-P1.5 |
| `unknown` | Unknown state. | Treat as blocked or needs review. | Safe default. | unspecified | P1.1-P1.5 |

### activation_status
| Canonical value | Meaning | Allowed current P2 use | Blocked interpretation | Aliases/deprecated terms | Source lanes observed |
| --- | --- | --- | --- | --- | --- |
| `not_activated` | Runtime or behavior inactive. | Default for P1/P2. | Activation. | inactive | P1.1-P1.5 |
| `pre_active_al1` | AL-1 metadata skeleton. | Current platform ceiling. | AL promotion. | AL-1 metadata skeleton | P1.1-P1.5 |
| `activation_blocked` | Gate blocker active. | Preserve blocker. | Activation readiness. | blocked_by_missing_approval | P1.2-P1.5 |
| `activation_deferred` | Future gate may review. | Planning only. | Approval to activate. | deferred | P1.3-P1.5 |
| `future_gate_required` | Explicit gate needed. | Route to GT. | Approval by reference. | requires_future_activation_gate | P1.2-P1.5 |
| `readiness_candidate` | Candidate for future review. | Readiness planning. | Runtime readiness. | candidate | P1.2-P1.5 |
| `not_applicable` | Not an activation concept. | Avoid false activation semantics. | Hidden approval. | none | All lanes |
| `unknown` | Unknown activation state. | Block or review. | Safe default. | unspecified | All lanes |

No P1 or P2 document may use activation status as runtime activation approval.

### validation_status
| Canonical value | Meaning | Allowed current P2 use | Blocked interpretation | Aliases/deprecated terms | Source lanes observed |
| --- | --- | --- | --- | --- | --- |
| `not_executed` | Validation not run. | Current default. | Evidence execution. | not run | P1.1-P1.5 |
| `proposed` | Future validation proposed. | Planning only. | Approval to run. | command_proposed | P0.2, P1 lanes |
| `blocked` | Validation blocked. | Preserve stop rule. | Passed check. | blocked_by_validation | P1.3-P1.4 |
| `needs_review` | Validation review needed. | Review routing. | Accepted evidence. | requires_validation_review | P1.3-P1.4 |
| `accepted_as_metadata_evidence` | Metadata accepted as evidence only. | Documentation support. | Governance approval. | accepted evidence | P1.2-P1.5 |
| `rejected_for_scope` | Validation scope invalid. | Stop/rescope. | Usable evidence. | rejected | P1 lanes |
| `future_gt04_required` | GT-04 needed before validation execution. | Gate reference. | Command approval. | validation evidence must cite GT-04 | P1.1-P1.5 |
| `not_applicable` | Validation not relevant. | Avoid false proof. | Hidden approval. | none | All lanes |
| `unknown` | Unknown validation posture. | Needs review. | Safe proof. | unspecified | All lanes |

Validation status records proof posture only. Validation evaluates; governance decides.

### security_status
| Canonical value | Meaning | Allowed current P2 use | Blocked interpretation | Aliases/deprecated terms | Source lanes observed |
| --- | --- | --- | --- | --- | --- |
| `metadata_only` | Security posture record only. | Document constraints. | Runtime guard. | security metadata | P1.1-P1.5 |
| `constraining` | Security limits action. | Preserve blockers. | Permission grant. | security refs constrain | P1.1-P1.5 |
| `blocked` | Security stop active. | Stop condition. | Approval. | blocked_by_security | P1.4 |
| `needs_review` | Security review needed. | Review route. | Safe default. | requires_security_review | P1.2-P1.4 |
| `future_security_review_required` | Future security review required. | Gate readiness. | Current approval. | security review required | P1.1-P1.5 |
| `incident_route_required` | Incident route needed. | Escalation. | Remediation approval. | incident required | P1.1-P1.5 |
| `not_applicable` | Not security relevant. | Avoid false blocker. | Permission grant. | none | All lanes |
| `unknown` | Unknown security status. | Block or review. | Safe default. | unspecified | All lanes |

Security status constrains actions and does not grant activation by itself.

### execution_status
| Canonical value | Meaning | Allowed current P2 use | Blocked interpretation | Aliases/deprecated terms | Source lanes observed |
| --- | --- | --- | --- | --- | --- |
| `not_executed` | No execution occurred. | Current default. | Dry run or test. | not run | P1.3-P1.4 |
| `execution_blocked` | Execution blocked. | Preserve GT-07/GT-06 blockers. | Execution approval. | blocked_by_tool_gate, blocked_by_provider_gate | P1.3-P1.4 |
| `execution_deferred` | Future execution review possible. | Planning only. | Approval. | deferred | P1.3-P1.4 |
| `future_gt07_required` | Tool execution gate required. | Gate route. | Tool permission. | tool use requires GT-07 | P1.1-P1.5 |
| `metadata_only` | Execution concept recorded as metadata only. | Non-runtime state. | Runtime state. | approved metadata only | P1.3-P1.4 |
| `not_applicable` | Execution not relevant. | Avoid false status. | Hidden approval. | none | All lanes |
| `unknown` | Unknown execution posture. | Block or review. | Safe default. | unknown risk | P1.3 |

Execution status cannot approve tool, agent, shell, subprocess, filesystem, network, package-manager, build, test, CI, Git, provider, API, or MCP execution.

### review_status and decision_status
| Field | Canonical values | Meaning | Blocked interpretation |
| --- | --- | --- | --- |
| `review_status` | `not_reviewed`, `needs_review`, `reviewed_metadata_only`, `blocked`, `rejected_for_scope`, `not_applicable`, `unknown` | Review posture only. | Governance approval or activation. |
| `decision_status` | `draft`, `blocked`, `needs_evidence`, `needs_security_review`, `needs_validation_review`, `approved_metadata_only`, `rejected_for_scope`, `superseded`, `retired`, `unknown` | Decision metadata only. | Runtime permission, source tracking, publication, or activation. |

## 7. Canonical Blocker Names
| Canonical blocker name | Meaning | Required gate or review | Applies to lanes | Aliases/deprecated terms | Preservation rule |
| --- | --- | --- | --- | --- | --- |
| `runtime_activation_blocker` | Runtime/service/loop is not active. | GT-06, GT-15 | Agent, CSS, Tool | runtime blocker | Must travel to activation records. |
| `source_loading_blocker` | Raw source loading blocked. | GT-01, GT-05 | Context, Tool, Agent, CSS | source loader blocker | Must travel to refs and inputs. |
| `context_permission_blocker` | Context does not grant permission. | Context/security review | Context, Provider, Tool, Agent, CSS | source ref permission deprecated | Preserve with context refs. |
| `provider_auth_blocker` | Provider auth blocked. | GT-08, S-03/S-04 | Provider, Tool, Agent, CSS | auth_not_approved | Preserve with provider refs. |
| `provider_network_blocker` | Network/API blocked. | GT-08 | Provider, Tool, Agent | network_not_approved | Preserve with provider/network refs. |
| `provider_mcp_blocker` | MCP activation blocked. | GT-08, GT-07 | Provider, Tool, Agent | mcp_not_approved | Preserve with MCP refs. |
| `tool_execution_blocker` | Tool execution blocked. | GT-07 | Tool, Agent, CSS | tool_execution_not_approved | Preserve with tool refs. |
| `agent_execution_blocker` | Agent runtime/task/handoff blocked. | GT-06 and related gates | Agent, Tool, CSS | agent_execution_not_approved | Preserve with agent refs. |
| `validation_execution_blocker` | Validation execution blocked. | GT-04 | All lanes | validation command blocker | Preserve with validation_refs. |
| `security_review_blocker` | Security review missing. | GT-05/security review | All lanes | missing_security_review | Preserve with security_refs. |
| `source_tracking_blocker` | Tracking/staging/commit/push blocked. | GT-02, GT-12 | All lanes | source_tracking_not_approved | Preserve with tracking_posture. |
| `generated_output_tracking_blocker` | Generated output tracking blocked. | GT-12, GT-15 | Context, Tool, CSS, Graphify | generated_output_boundary | Preserve with generated_output_posture. |
| `publication_blocker` | Publication blocked. | GT-12 | All lanes | publication blocked | Preserve with retention records. |
| `local_only_blocker` | Local-only content blocked. | GT-01, GT-05 | All lanes | local_only_boundary | Preserve with sensitivity. |
| `product_source_blocker` | Product source blocked. | GT-09 | Context, Tool, Agent, CSS, Provider | product source exclusion | Preserve with product refs. |
| `product_activation_blocker` | Product activation blocked. | GT-09 | Product-related lanes | product_access_not_approved | Preserve with product_posture. |
| `external_source_blocker` | External source blocked. | GT-11 | Context, Tool, Agent, CSS | external_source_blocker | Preserve with source classification. |
| `secret_exposure_blocker` | Secret value blocked. | S-03, GT-15 | All lanes | secret_blocker | Values never propagate. |
| `credential_exposure_blocker` | Credential value/use blocked. | S-03, GT-08 | All lanes | credential_blocker | Refs only; values never propagate. |
| `unknown_sensitivity_blocker` | Unknown sensitivity blocks. | GT-01/security review | All lanes | unknown_risk_blocker | Defaults to blocked/needs review. |
| `graphify_authority_blocker` | Graphify authority inference blocked. | Governance review | Graphify/CSS/all | Graphify Authority prohibited | Preserve evidence-only boundary. |
| `graphify_raw_output_blocker` | Raw Graphify output blocked. | GT-12/Graphify gate | Graphify/CSS/Tool/Context | raw output blocker | Preserve local-only status. |
| `substrate_selection_blocker` | Substrate decision blocked. | GT-10, GT-13 | CSS/all | graph_substrate_selection_blocker | Preserve deferral. |
| `graph_substrate_selection_blocker` | Graph cannot be selected by default. | GT-10 | CSS/Graphify | selected graph substrate prohibited | Preserve graph candidate only. |
| `retention_review_blocker` | Retention review required. | GT-15/security review | All lanes | retention blocker | Preserve with retention_posture. |
| `rollback_readiness_blocker` | Rollback readiness missing. | GT-15 | Activation lanes | rollback blocker | Preserve before readiness. |
| `incident_route_blocker` | Incident route required. | GT-15/security review | All lanes | incident requirement | Preserve with incident_refs. |

Blockers must travel downstream through context packs, provider refs, tool refs, agent handoffs, semantic records, evidence refs, retention records, and future audit records.

## 8. Canonical Sensitivity Classes
| Canonical sensitivity class | Meaning | Allowed P2 use | Blocked use | Required gate or review | Aliases/deprecated terms |
| --- | --- | --- | --- | --- | --- |
| `public_governance_metadata` | Public-safe governance metadata. | Cite metadata. | Activation inference. | Active scope. | public metadata |
| `internal_governance_metadata` | Internal governance metadata. | Cite with limitations. | Publication by default. | GT-12 if publishing. | governance_metadata |
| `implementation_metadata` | Implementation records, not live code. | Cite posture. | Reading live source or execution. | GT-01/GT-07 if expanding. | implementation records |
| `generated_sensitive` | Generated output with sensitivity risk. | Metadata only. | Authority or publication. | GT-05/GT-12/GT-15. | generated-sensitive |
| `generated_graphify_evidence` | Curated Graphify evidence. | Supporting evidence only. | Authority/substrate. | GT-11/GT-12 if tracking. | Graphify summary |
| `generated_local_only` | Raw/generated local artifacts. | Safe metadata only. | Raw inclusion/tracking. | GT-12/GT-15. | generated raw output |
| `local_only` | Local-only material. | Metadata only when scoped. | Raw content inclusion. | GT-01/GT-05. | local_only_source |
| `product_restricted` | Product source/output or product-sensitive material. | Product readiness metadata. | Product source inspection/activation. | GT-09. | product_restricted_source |
| `external_restricted` | External raw source or external-sensitive material. | External metadata only. | Source copying/execution. | GT-11. | external_source |
| `credential_reference` | Redacted credential need metadata. | Metadata marker only. | Credential value/use. | GT-08, S-03. | credential refs |
| `secret_value` | Secret value or secret-bearing content. | None. | Any exposure/retention. | Secure incident route, GT-15. | secret |
| `provider_auth_material` | Auth configs, sessions, tokens, browser auth. | None by default. | Auth use/inspection. | GT-08 secure approval. | auth material |
| `runtime_state` | Runtime logs/process/state/caches. | Excluded by default. | Runtime inspection/persistence. | GT-06/GT-13/GT-15. | state/logs |
| `unknown_sensitivity` | Unclassified or mixed sensitivity. | Mark blocked/needs review. | Treating as safe. | GT-01/security review. | unknown risk |

Unknown sensitivity defaults to blocked. Secret values are never metadata content. Credential references are metadata only. Generated outputs remain generated-sensitive unless curated and governed. Product-restricted material remains blocked until GT-09. Local-only material remains local-only unless future governance changes exact scope.

## 9. Canonical Source Classifications
| Canonical source classification | Meaning | Examples | Allowed P2 use | Blocked use | Required gate or review | Aliases/deprecated terms |
| --- | --- | --- | --- | --- | --- | --- |
| `governance_metadata` | Governance/control docs. | P0/P1/P2 docs. | Cite and align. | Activation inference. | Active scope. | governance document |
| `implementation_metadata` | Implementation records. | I-01-I-07 docs. | Cite posture. | Live source reads/execution. | GT-01/GT-07 if expanding. | implementation record |
| `validation_metadata` | Validation posture records. | P0.2, ValidationRef. | Proof posture. | Validation execution approval. | GT-04. | proof refs deprecated when evidence_refs intended |
| `security_metadata` | Security posture records. | P0.3, SecurityRef. | Constraints. | Permission grants. | GT-05/security review. | permission_refs deprecated |
| `context_metadata` | Context refs/items/packs. | P1.1 records. | Source ref metadata. | Source loading. | GT-01/GT-05. | context inclusion as permission deprecated |
| `provider_metadata` | Provider/adapter refs. | P1.2 records. | Provider posture. | Provider activation. | GT-08. | activated provider metadata prohibited |
| `tool_metadata` | Tool descriptors/requests/decisions. | P1.3 records. | Tool posture. | Tool execution. | GT-07. | executable tool metadata prohibited |
| `agent_metadata` | Agent/task/handoff refs. | P1.4 records. | Agent posture. | Agent execution. | GT-06. | executable agent metadata prohibited |
| `semantic_metadata` | Semantic entities/claims/relations. | P1.5 records. | Semantic posture. | Truth/substrate/runtime. | GT-10/GT-13 if substrate/state. | truth engine terms prohibited |
| `generated_graphify_evidence` | Curated Graphify summary. | Repo Map Summary. | Supporting evidence. | Authority/substrate. | GT-11/GT-12 if tracking. | Graphify Authority prohibited |
| `generated_local_only` | Raw generated artifacts. | `9_artifacts/` outputs. | Safe metadata if scoped. | Raw inclusion/tracking. | GT-12/GT-15. | raw generated output |
| `local_only_source` | Local-only source or artifacts. | previous corpus, datasets, models. | Safe metadata if scoped. | Raw loading/publication. | GT-01/GT-05. | local-only |
| `product_restricted` | Siamese product source/output. | product workspaces. | Product readiness metadata. | Product activation/source loading. | GT-09. | product source |
| `external_source` | Raw external source or metadata. | external snapshots. | External metadata if scoped. | Source copy/execution. | GT-11. | external raw source |
| `credential_reference` | Credential need marker. | CredentialRef. | Redacted metadata. | Values/use. | GT-08. | credential refs |
| `secret_value` | Secret content. | tokens, keys. | None. | Any exposure. | Incident route. | secret |
| `provider_auth_material` | Provider auth configs/sessions. | OAuth, browser auth, token stores. | None by default. | Inspection/use. | GT-08. | auth material |
| `runtime_state` | Runtime state/logs. | logs, caches, process state. | Excluded. | Runtime use/persistence. | GT-06/GT-13. | state |
| `unknown_sensitivity` | Unclassified source. | unclear path/ref. | Block/review. | Treat as safe. | GT-01/security review. | unknown |

Source classification records origin and access posture. It does not authorize raw source reads.

## 10. Canonical Posture Vocabulary
### provider_auth_posture
| Canonical value | Meaning | Allowed current P2 use | Blocked interpretation | Required gate or review | Aliases/deprecated terms |
| --- | --- | --- | --- | --- | --- |
| `not_configured` | Provider/auth not configured. | Current default. | Auth approval. | GT-08 for future auth. | no auth configured |
| `auth_blocked` | Auth blocked. | Preserve blocker. | Use credentials. | GT-08/S-03. | auth_not_approved |
| `credential_ref_metadata_only` | Redacted credential ref only. | Safe metadata marker. | Credential value/use. | GT-08 secure approval. | CredentialRef |
| `network_blocked` | Network/API blocked. | Preserve blocker. | Network permission. | GT-08. | network_not_approved |
| `mcp_blocked` | MCP blocked. | Preserve blocker. | MCP activation. | GT-08/GT-07. | mcp_not_approved |
| `provider_transmission_blocked` | Provider-bound context/semantic transmission blocked. | Preserve blocker. | Transmission approval. | GT-08/security review. | context_transmission_not_approved |
| `future_gt08_required` | GT-08 needed. | Gate route. | Approval by reference. | GT-08. | provider gate required |
| `not_applicable` | No provider/auth relation. | Avoid false blocker. | Hidden approval. | none | none |
| `unknown` | Unknown auth posture. | Block/review. | Safe default. | security review. | unspecified |

### tracking_posture
| Canonical value | Meaning | Allowed current P2 use | Blocked interpretation | Required gate or review | Aliases/deprecated terms |
| --- | --- | --- | --- | --- | --- |
| `not_tracked` | Not tracked. | Current default for generated/local-only. | Source approval. | GT-12 if tracking. | untracked |
| `tracking_blocked` | Tracking blocked. | Preserve blocker. | Tracking approval. | GT-02/GT-12. | source_tracking_not_approved |
| `local_only` | Local-only Git/publication posture. | Preserve local-only. | Publication. | GT-12/security review. | ignored/local-only |
| `exact_path_future_review` | Exact future path review needed. | Planning only. | Staging approval. | GT-12 and human approval. | exact-path review |
| `future_gt12_required` | GT-12 needed. | Gate route. | Approval by reference. | GT-12. | publication gate required |
| `publication_blocked` | Publication blocked. | Preserve blocker. | Publication. | GT-12. | publish blocked |
| `not_applicable` | No tracking relevance. | Avoid false blocker. | Hidden approval. | none | none |
| `unknown` | Unknown tracking posture. | Block/review. | Safe default. | source tracking review. | unspecified |

### retention_posture
| Canonical value | Meaning | Allowed current P2 use | Blocked interpretation | Required gate or review | Aliases/deprecated terms |
| --- | --- | --- | --- | --- | --- |
| `metadata_only` | Retain metadata only. | Current preferred posture. | Raw content retention. | Review if sensitive. | safe metadata |
| `generated_sensitive` | Generated output sensitive. | Preserve generated-output caution. | Authority/publication. | GT-05/GT-12. | generated-sensitive |
| `local_only` | Retain local-only if scoped. | Preserve local-only. | Publication. | security review. | local-only retention |
| `quarantine` | Quarantine required. | Incident containment. | Cleanup approval. | GT-15/security review. | quarantined |
| `deletion_candidate` | Deletion review needed. | Future cleanup candidate. | Delete without approval. | GT-15. | removal candidate |
| `publication_blocked` | Publication blocked. | Preserve blocker. | Publication approval. | GT-12. | publish blocked |
| `incident_route_required` | Incident route needed. | Escalate safely. | Remediation approval. | GT-15/security. | incident required |
| `not_applicable` | No retention relevance. | Avoid false state. | Hidden retention approval. | none | none |
| `unknown` | Unknown retention posture. | Block/review. | Safe retention. | retention review. | unspecified |

### generated_output_posture
| Canonical value | Meaning | Allowed current P2 use | Blocked interpretation | Required gate or review | Aliases/deprecated terms |
| --- | --- | --- | --- | --- | --- |
| `not_generated` | Not generated output. | Ordinary metadata. | Generated authority. | none | none |
| `generated_sensitive` | Generated output sensitive. | Evidence with limitations. | Authority. | validation/security review. | generated-sensitive |
| `curated_metadata_only` | Curated summary only. | Supporting evidence. | Raw output approval. | GT-04/GT-12 if tracking. | curated Graphify summary |
| `local_only_raw_output` | Raw generated output local-only. | Excluded by default. | Context/semantic inclusion. | GT-12/GT-15. | raw Graphify output |
| `authority_blocked` | Authority inference blocked. | Preserve evidence-only posture. | Truth/governance. | governance review. | output as truth deprecated |
| `tracking_blocked` | Generated output tracking blocked. | Preserve blocker. | Tracking approval. | GT-12. | generated output tracking blocker |
| `publication_blocked` | Publication blocked. | Preserve blocker. | Publication. | GT-12. | publish blocked |
| `not_applicable` | No generated-output relevance. | Avoid false state. | Hidden approval. | none | none |
| `unknown` | Unknown generated posture. | Block/review. | Safe default. | output review. | unspecified |

### product_posture
| Canonical value | Meaning | Allowed current P2 use | Blocked interpretation | Required gate or review | Aliases/deprecated terms |
| --- | --- | --- | --- | --- | --- |
| `product_inactive` | Product inactive. | Current default. | Product activation. | GT-09. | inactive product |
| `product_restricted` | Product-restricted material. | Product readiness metadata. | Source inspection. | GT-09. | product source |
| `product_readiness_metadata_only` | Product readiness record only. | Planning only. | Product activation. | GT-09. | readiness-only |
| `product_source_blocked` | Product source blocked. | Preserve blocker. | Product source loading. | GT-09/security. | product source exclusion |
| `future_gt09_required` | GT-09 needed. | Gate route. | Approval by reference. | GT-09. | product gate required |
| `publication_blocked` | Product publication blocked. | Preserve blocker. | Publication. | GT-12/GT-09. | product publish blocked |
| `not_applicable` | No product relation. | Avoid false blocker. | Hidden approval. | none | none |
| `unknown` | Unknown product posture. | Block/review. | Safe default. | product/security review. | unspecified |

### substrate_posture
| Canonical value | Meaning | Allowed current P2 use | Blocked interpretation | Required gate or review | Aliases/deprecated terms |
| --- | --- | --- | --- | --- | --- |
| `substrate_deferred` | Final substrate deferred. | Current CSS default. | Substrate selection. | GT-10. | substrate remains deferred |
| `candidate_only` | Candidate metadata only. | Compare later. | Selection. | GT-10. | candidate |
| `not_selected` | Explicitly not selected. | Preserve neutrality. | Hidden adoption. | GT-10. | unselected |
| `selection_blocked` | Selection blocked. | Preserve blocker. | Selection approval. | GT-10/GT-13. | substrate_selection_blocker |
| `graph_candidate_only` | Graph remains candidate only. | Graph evidence discussion. | Graph selected. | GT-10. | graph remains candidate only |
| `future_gt10_required` | GT-10 required. | Gate route. | Substrate approval. | GT-10. | substrate gate required |
| `future_gt13_required` | GT-13 required for state/persistence. | Gate route. | Persistence approval. | GT-13. | persistence gate required |
| `not_applicable` | No substrate relevance. | Avoid false blocker. | Hidden selection. | none | none |
| `unknown` | Unknown substrate posture. | Block/review. | Safe default. | CSS governance review. | unspecified |

No posture field grants permission to activate runtime, read source, transmit to providers, execute tools, execute agents, publish, track generated outputs, expand source tracking, or select substrate.

## 11. Canonical Reference Field Naming
| Canonical field name | Singular object name | Plural field name | Meaning | Allowed lane prefixes | Aliases/deprecated terms | Blocked interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| `source_refs` | `SourceRef` | `source_refs` | Metadata refs to source surfaces. | ContextSourceRef, Semantic source refs | source_ref_id | Raw source loading approval. |
| `context_refs` | `ContextRef` | `context_refs` | Context metadata refs. | ContextRef, AgentContextRef, SemanticContextRef | context requirement refs | Context permission. |
| `evidence_refs` | `EvidenceRef` | `evidence_refs` | Supporting evidence refs. | ContextEvidenceRef, ProviderEvidenceRef, ToolEvidenceRef, AgentEvidenceRef, SemanticEvidenceRef | proof_refs deprecated | Authority or decision. |
| `validation_refs` | `ValidationRef` | `validation_refs` | Validation posture refs. | ContextValidationRef, ProviderValidationRef, ToolValidationRef, AgentValidationRef, SemanticValidationRef | test_refs deprecated | Validation execution or governance approval. |
| `security_refs` | `SecurityRef` | `security_refs` | Security posture refs. | ContextSecurityRef, ProviderSecurityRef, ToolSecurityRef, AgentSecurityRef, SemanticSecurityRef | permission_refs deprecated | Permission grant. |
| `provider_refs` | `ProviderRef` | `provider_refs` | Provider metadata refs. | AgentProviderRef, SemanticProviderRef | provider requirement refs | Provider activation. |
| `tool_refs` | `ToolRef` | `tool_refs` | Tool metadata refs. | AgentToolRef, SemanticToolRef | tool requirement refs | Tool execution. |
| `agent_refs` | `AgentRef` | `agent_refs` | Agent metadata refs. | SemanticAgentRef | runtime refs | Agent execution. |
| `semantic_refs` | `SemanticRef` | `semantic_refs` | Semantic metadata refs. | SemanticEntity/Claim/Relation refs | CSS refs | Truth or substrate selection. |
| `graphify_refs` | `GraphifyRef` | `graphify_refs` | Curated Graphify evidence metadata refs. | SemanticGraphifyRef | raw graphify refs deprecated | Raw output loading or authority. |
| `product_refs` | `ProductRef` | `product_refs` | Product-readiness metadata refs. | SemanticProductRef | product source refs deprecated | Product source access. |
| `governance_refs` | `GovernanceRef` | `governance_refs` | Governance decision/gate refs. | Gate refs | approval refs when ambiguous | Runtime approval without exact scope. |
| `audit_refs` | `AuditRef` | `audit_refs` | Future audit metadata refs. | ToolAuditRequirement refs | log refs | Audit runtime. |
| `retention_refs` | `RetentionRef` | `retention_refs` | Retention posture refs. | Context/Provider/Agent/Semantic retention refs | retention posture refs | Retention of unsafe content. |
| `rollback_refs` | `RollbackRef` | `rollback_refs` | Rollback posture refs. | AgentApprovalRecord, future P2.3 | rollback posture | Automatic rollback execution. |
| `incident_refs` | `IncidentRef` | `incident_refs` | Incident route refs. | Future P2.3 | incident route | Incident automation or remediation approval. |

Use plural field names for arrays of refs. Use singular object names for individual ref records. Use lane-specific object names only when needed for clarity, such as `ContextEvidenceRef`, `ProviderEvidenceRef`, `ToolEvidenceRef`, `AgentEvidenceRef`, or `SemanticEvidenceRef`. Use canonical shared field names inside lane-specific objects whenever possible. Use `evidence_refs`, not `proof_refs`, when pointing to supporting evidence. Use `validation_refs`, not `test_refs`, when pointing to validation posture. Use `security_refs`, not `permission_refs`, when pointing to security posture. Use `graphify_refs` only for curated Graphify evidence metadata, not raw Graphify output. Use `product_refs` only for product-readiness metadata, not product source. Ref fields are metadata and do not authorize raw source loading, execution, provider transmission, publication, or substrate selection.

## 12. Evidence / Validation / Security Naming Alignment
| Canonical object | Lane-specific allowed aliases | Required minimum fields | Blocked interpretations | Downstream use in P2.2 and P2.3 |
| --- | --- | --- | --- | --- |
| `EvidenceRef` | ContextEvidenceRef, ProviderEvidenceRef, ToolEvidenceRef, AgentEvidenceRef, SemanticEvidenceRef | `evidence_ref_id`, `evidence_type`, `evidence_scope`, `source_refs`, `validation_refs`, `security_refs`, `limitations`, `sensitivity`, `retention_posture`, `review_required` | Authority, truth, approval, publication, source tracking. | P2.2 canonical evidence object; P2.3 evidence retention input. |
| `ValidationRef` | ContextValidationRef, ProviderValidationRef, ToolValidationRef, AgentValidationRef, SemanticValidationRef | `validation_ref_id`, `validation_scope`, `proof_target`, `validation_status`, `gate_ref`, `limitations`, `blockers`, `review_required` | Validation execution, governance approval, activation. | P2.2 canonical validation object; P2.3 validation evidence retention input. |
| `SecurityRef` | ContextSecurityRef, ProviderSecurityRef, ToolSecurityRef, AgentSecurityRef, SemanticSecurityRef | `security_ref_id`, `security_scope`, `security_status`, `sensitivity`, `blocked_actions`, `blockers`, `limitations`, `review_required` | Permission grant, runtime guard, activation. | P2.2 canonical security object; P2.3 incident/retention input. |

Evidence supports; it does not decide. Validation evaluates; governance decides. Security constrains; it does not grant activation by itself. P2.2 must consume this naming unless it explicitly marks a term as `pending_P2.1_alignment`.

## 13. Cross-Lane Object Naming Alignment
| Concept | Canonical name | Lane-specific names observed | Allowed aliases | Deprecated terms | Notes |
| --- | --- | --- | --- | --- | --- |
| context pack | `ContextPack` | ContextPack | none | context permission | Metadata bundle only. |
| context item | `ContextItem` | ContextItem | none | raw context item | Safe summary/metadata only. |
| context source ref | `ContextSourceRef` | ContextSourceRef | SourceRef when generic | source ref permission | Metadata only. |
| provider descriptor | `ProviderDescriptor` | ProviderDescriptor | provider metadata record | live provider instance | Not activation. |
| adapter descriptor | `AdapterDescriptor` | AdapterDescriptor | adapter metadata record | runtime adapter | Not activation. |
| provider capability | `ProviderCapability` | ProviderCapability | capability metadata | callable capability | Not call approval. |
| auth requirement | `AuthRequirement` | AuthRequirement | auth metadata | auth approval | Not auth approval. |
| network requirement | `NetworkRequirement` | NetworkRequirement | network metadata | network permission | Not network approval. |
| MCP requirement | `MCPRequirement` | MCPRequirement | mcp metadata | MCP activation | Not MCP activation. |
| credential ref | `CredentialRef` | CredentialRef | credential reference | credential value | Metadata only. |
| tool descriptor | `ToolDescriptor` | ToolDescriptor | tool metadata record | executable tool metadata | Not execution. |
| tool capability | `ToolCapability` | ToolCapability | capability metadata | active tool capability | Not execution. |
| tool request | `ToolRequest` | ToolRequest | tool proposal | tool run | Proposal only. |
| tool decision | `ToolDecision` | ToolDecision | decision metadata | execution authorization | Metadata only. |
| tool risk level | `ToolRiskLevel` | ToolRiskLevel | risk classification | execution approval | Classification only. |
| agent descriptor | `AgentRuntimeRef` | AgentRuntimeRef, agent descriptor | AgentRef | executable agent metadata | Metadata only. |
| agent capability | `AgentCapabilityRef` | AgentCapabilityRef | capability ref | active agent capability | Not activation. |
| agent task envelope | `AgentTaskRecord` | AgentTaskRecord, task metadata | task envelope | task execution | Metadata only. |
| agent handoff record | `AgentHandoffRecord` | AgentHandoffRecord | handoff metadata | handoff execution | Metadata only. |
| agent coordination ref | `AgentCoordinationRef` | Handoff/coordination metadata | AgentHandoffRecord | orchestration runtime | Future alias for coordination only. |
| semantic entity | `SemanticEntity` | SemanticEntity | entity record | truth record | Metadata only. |
| semantic claim | `SemanticClaim` | SemanticClaim | claim record | truth claim | Not truth by default. |
| semantic relation | `SemanticRelation` | SemanticRelation | relation record | graph edge as substrate | Does not require graph. |
| substrate candidate record | `SubstrateCandidateRecord` | SubstrateCandidateRecord | candidate record | selected substrate | Candidate only. |
| substrate decision blocker | `SubstrateDecisionBlocker` | SubstrateDecisionBlocker | substrate blocker | substrate approval | Blocks selection. |
| audit event | `AuditEvent` | ToolAuditRequirement prep, future audit refs | audit record | runtime logging | P2.3 prep only. |
| retention record | `RetentionRecord` | ContextRetentionRecord, ProviderRetentionRecord, AgentRetentionRecord, SemanticRetentionRecord | RetentionRef | unsafe retention | Metadata posture only. |
| rollback record | `RollbackRecord` | rollback_refs, rollback posture | RollbackRef | rollback automation | P2.3 prep only. |
| incident record | `IncidentRecord` | incident_refs, incident route | IncidentRef | incident automation | P2.3 prep only. |

## 14. Lane-Specific Drift Register
| drift_id | concept | P1.1 term | P1.2 term | P1.3 term | P1.4 term | P1.5 term | canonical P2.1 term | aliases preserved | deprecated terms | decision rationale | safety impact | downstream consumer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DRIFT-001 | Evidence refs | ContextEvidenceRef | ProviderEvidenceRef | ToolEvidenceRef | AgentEvidenceRef | SemanticEvidenceRef | EvidenceRef / `evidence_refs` | Lane prefixes allowed | proof_refs | Shared field with lane-specific object names. | Prevents evidence as authority. | P2.2/P2.3 |
| DRIFT-002 | Validation refs | ContextValidationRef | ProviderValidationRef | ToolValidationRef | AgentValidationRef | SemanticValidationRef | ValidationRef / `validation_refs` | Lane prefixes allowed | test_refs | Preserves validation posture. | Blocks validation-as-approval. | P2.2 |
| DRIFT-003 | Security refs | ContextSecurityRef | ProviderSecurityRef | ToolSecurityRef | AgentSecurityRef | SemanticSecurityRef | SecurityRef / `security_refs` | Lane prefixes allowed | permission_refs | Security constrains, not grants. | Blocks permission drift. | P2.2/P2.3 |
| DRIFT-004 | Execution state | not applicable | activation state | execution_status | execution_status | runtime activation blocked | `execution_status` | activation_state where provider-specific | executable metadata | Execution status separated from activation. | Blocks runtime activation inference. | P3 readiness |
| DRIFT-005 | Activation state | context not activated | activation_state | tool execution activation | agent activation | runtime activation | `activation_status` | activation_level retained | readiness as activation | One cross-lane activation field. | Preserves AL-1. | P3 readiness |
| DRIFT-006 | Generated output | generated-output flags | generated provider output | tool output | agent output | Graphify/generated output | `generated_output_posture` | generated_output_related | output authority | Captures local-only/generated-sensitive posture. | Blocks generated authority. | P2.3 |
| DRIFT-007 | Product posture | product_related | product_refs | product_access_profile | product_bound_action | product_related | `product_posture` | product_related retained | product activation | Separates readiness metadata from activation. | Preserves GT-09. | Product readiness |
| DRIFT-008 | Substrate posture | CSS substrate deferred | CSS substrate deferred | substrate deferred | substrate deferred | substrate candidate/blocker | `substrate_posture` | candidate_status retained | selected graph substrate | Keeps substrate deferred and candidate-only. | Blocks graph lock-in. | CSS/P3 |
| DRIFT-009 | Credential refs | credential_related | CredentialRef | credential_reference | credential_reference | credential_related | `credential_reference` / CredentialRef | CredentialRef retained | credential value | Separates metadata refs from values. | Blocks secret leakage. | Security/P2.3 |
| DRIFT-010 | Blockers | blockers | activation_blockers | ToolExecutionBlocker | AgentExecutionBlocker | SubstrateDecisionBlocker | canonical blocker names | lane blockers retained | bypass terms | Common blocker vocabulary plus lane-specific objects. | Preserves downstream stop rules. | All lanes |
| DRIFT-011 | Context permission | Context inclusion is not permission | context requirements | context-derived requests | agent context refs | context refs | `context_permission_blocker` | context_refs retained | source ref permission | Makes non-permission explicit. | Blocks source loading. | Context/P2.2 |
| DRIFT-012 | No drift baseline | no_drift_detected | no_drift_detected | no_drift_detected | no_drift_detected | no_drift_detected | `blockers`, `limitations`, `review_required` | none | none | Shared terms already aligned. | Preserves safety. | All lanes |

If no drift is found for a concept, record `no_drift_detected`.

## 15. Deprecated / Alias Term Register
| alias_or_deprecated_term | canonical_term | status | source lane | reason | migration guidance | blocked interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| Platform Graphify | Graphify as historical/generated evidence only | prohibited | CSS/Graphify | Rejected current name. | Use only in prohibited register. | Current system name. |
| Graphify Authority | graphify_authority_blocker | prohibited | CSS/Graphify | Graphify is not authority. | Use Graphify evidence only. | Authority. |
| Graphify owns truth | graphify_authority_blocker | prohibited | CSS/Graphify | Truth claim rejected. | Use evidence-only wording. | Truth engine. |
| Graphify truth engine | graphify_authority_blocker | prohibited | CSS/Graphify | Truth engine rejected. | Use prohibited register only. | Truth engine. |
| Graphify substrate | substrate_selection_blocker | prohibited | CSS/Graphify | Graphify is not substrate. | Use graphify_refs as evidence refs. | Substrate. |
| Graphify system of record for AGENT PLATFORM | graphify_authority_blocker | prohibited | CSS/Graphify | System-of-record claim rejected. | Use governance refs. | Root authority. |
| selected graph substrate | graph_substrate_selection_blocker | prohibited | CSS | Graph remains candidate only. | Use `graph_candidate_only`. | Graph selected. |
| activated provider metadata | ProviderDescriptor metadata only | deprecated | Provider | Metadata cannot activate. | Use `provider_metadata` and `activation_status`. | Provider activation. |
| executable tool metadata | ToolDescriptor metadata only | deprecated | Tool | Metadata cannot execute. | Use `tool_metadata` and `execution_status`. | Tool execution. |
| executable agent metadata | AgentRuntimeRef metadata only | deprecated | Agent | Metadata cannot execute. | Use `agent_metadata`. | Agent execution. |
| source ref permission | ContextSourceRef metadata only | deprecated | Context | Source refs are metadata. | Use `context_permission_blocker`. | Source loading. |
| validation approval | ValidationRef metadata only | deprecated | Validation | Validation evaluates. | Use `validation_status`. | Governance approval. |
| security permission grant | SecurityRef constraining metadata | deprecated | Security | Security constrains. | Use `security_status`. | Permission grant. |
| proof_refs | `evidence_refs` | alias/deprecated | Mixed | Evidence refs are canonical. | Use `evidence_refs`. | Proof as authority. |
| test_refs | `validation_refs` | deprecated | Mixed | Tests are execution; validation posture is broader. | Use `validation_refs`. | Test execution approval. |
| permission_refs | `security_refs` | deprecated | Mixed | Security refs constrain, not grant. | Use `security_refs`. | Permission grant. |

## 16. Cross-Lane Propagation Rules
| Propagation rule | Required behavior |
| --- | --- |
| Sensitivity propagation | Sensitivity must propagate from source refs to evidence refs, context records, provider refs, tool refs, agent handoffs, semantic records, audit records, retention records, and incident records. |
| Blocker propagation | Blockers must propagate downstream. |
| Limitation propagation | Limitations must propagate downstream. |
| Local-only propagation | Local-only flags must propagate downstream. |
| Generated-output propagation | generated_output_posture must propagate downstream. |
| Product posture propagation | product_posture must propagate downstream. |
| Provider/auth propagation | provider/auth blockers must propagate to provider-bound context, semantic, agent, and evidence records. |
| Tool execution propagation | tool execution blockers must propagate to tool-bound context, semantic, agent, and evidence records. |
| Agent execution propagation | agent execution blockers must propagate to handoff and coordination records. |
| Substrate blocker propagation | substrate blockers must propagate to Cognitive Semantic System records. |
| Publication blocker propagation | publication blockers must propagate to evidence, retention, audit, rollback, and incident records. |
| Unknown sensitivity downgrade | Unknown sensitivity must downgrade to blocked or needs review. |
| Alias safety | Aliases must not override canonical blockers. |
| Deprecated term ban | Deprecated terms must not be used in new P2/P3 documents except in alias/deprecated registers. |

## 17. P2.2 Consumption Rules
P2.2 must consume P2.1 canonical vocabulary.

| P2.2 rule | Required behavior |
| --- | --- |
| Ref naming | Use `EvidenceRef`, `evidence_refs`, `ValidationRef`, `validation_refs`, `SecurityRef`, and `security_refs` as canonical naming. |
| Graphify evidence | Treat Graphify evidence as generated supporting evidence only. |
| Generated/local posture | Preserve generated-output and local-only posture. |
| Unresolved dependencies | Mark any unresolved vocabulary dependency as `pending_P2.1_alignment` only if P2.1 is not yet finalized. |
| New synonyms | Once P2.1 exists, do not introduce new synonyms without registering them as aliases or deferred drift. |

## 18. P2.3 Consumption Rules
P2.3 must consume P2.1 canonical vocabulary.

| P2.3 rule | Required behavior |
| --- | --- |
| Canonical blockers | Use the canonical blocker names from P2.1. |
| Posture values | Use retention_posture, generated_output_posture, product_posture, and tracking_posture values from P2.1. |
| Ref names | Use canonical `audit_refs`, `retention_refs`, `rollback_refs`, and `incident_refs`. |
| Blocker preservation | Preserve publication blockers, source tracking blockers, local-only blockers, secret/credential blockers, product-source blockers, provider/auth blockers, tool-execution blockers, agent-execution blockers, Graphify raw-output blockers, and substrate-selection blockers. |
| Unresolved dependencies | Mark unresolved vocabulary dependency as `pending_P2.1_alignment` only if P2.1 is not yet finalized. |

## 19. Validation / Security / Governance Interface
| Interface | P2.1 rule |
| --- | --- |
| Validation | May later evaluate vocabulary completeness, drift resolution, alias coverage, deprecated term use, and blocker propagation. P2.1 does not execute validation. |
| Validation status | Does not approve governance decisions. Validation evaluates; governance decides. |
| Security | Constrains vocabulary where terms could imply permission. Security status does not grant runtime activation. |
| Governance | Decides acceptance of canonical terms, downstream adoption, readiness progression, and future activation. |
| P0 gates | P2.1 vocabulary does not override P0 gates. |
| P1 contracts | P2.1 vocabulary does not rewrite P1 contracts retroactively. |

## 20. Graphify / Cognitive Semantic System / Siamese Boundaries
| Boundary | Rule |
| --- | --- |
| Graphify | Graphify is supporting generated evidence only. Graphify evidence is not authority. Graphify labels are not governance labels. Graphify raw output remains local-only. Graphify evidence cannot select graph as substrate. |
| Cognitive Semantic System | Cognitive Semantic System substrate remains deferred. Graph remains candidate only. |
| Siamese | Siamese is the living energy twin product vision, not product activation. Product source remains blocked until GT-09. Product pressure cannot decide substrate or vocabulary authority. |
| Drift resolution | Any Graphify/product/substrate terminology drift must be resolved toward stricter non-activation language. |

## 21. Audit / Retention / Rollback Vocabulary Preparation
| Preliminary P2.3 name | Meaning | P2.1 posture |
| --- | --- | --- |
| `AuditEvent` | Future audit event metadata. | Name only; no audit runtime. |
| `RetentionRecord` | Future retention metadata. | Name only; no persistence. |
| `RollbackRecord` | Future rollback metadata. | Name only; no automation. |
| `IncidentRecord` | Future incident metadata. | Name only; no incident automation. |
| `QuarantineRecord` | Future quarantine metadata. | Name only; no quarantine automation. |
| `PublicationBlocker` | Publication stop condition. | Vocabulary only. |
| `SourceTrackingBlocker` | Source tracking stop condition. | Vocabulary only. |
| `GeneratedOutputRetention` | Generated-output retention posture. | Vocabulary only. |
| `LocalOnlyRetention` | Local-only retention posture. | Vocabulary only. |
| `SecretCredentialIncident` | Secret/credential incident category. | Vocabulary only. |
| `ProductSourceIncident` | Product source incident category. | Vocabulary only. |
| `ProviderAuthIncident` | Provider/auth incident category. | Vocabulary only. |
| `ToolExecutionIncident` | Tool execution incident category. | Vocabulary only. |
| `AgentExecutionIncident` | Agent execution incident category. | Vocabulary only. |
| `GraphifyOutputIncident` | Graphify output incident category. | Vocabulary only. |
| `SubstrateSelectionIncident` | Substrate selection incident category. | Vocabulary only. |

These names prepare P2.3 vocabulary only. P2.1 does not create audit runtime, logging runtime, telemetry, persistence, rollback automation, quarantine automation, or incident automation.

## 22. Shared Vocabulary Invariants
| ID | Invariant |
| --- | --- |
| VOCAB-001 | P2.1 is vocabulary alignment only. |
| VOCAB-002 | AGENT PLATFORM remains pre-active at AL-1. |
| VOCAB-003 | Canonical terms are not runtime permissions. |
| VOCAB-004 | Context inclusion is not permission. |
| VOCAB-005 | Provider metadata is not provider activation. |
| VOCAB-006 | Tool metadata is not tool execution. |
| VOCAB-007 | Agent metadata is not agent execution. |
| VOCAB-008 | Evidence supports; it does not decide. |
| VOCAB-009 | Validation evaluates; governance decides. |
| VOCAB-010 | Security constrains; it does not activate. |
| VOCAB-011 | Source refs are metadata, not raw source loading approval. |
| VOCAB-012 | Source tracking remains separately gated. |
| VOCAB-013 | Publication remains separately gated. |
| VOCAB-014 | Generated outputs remain generated-sensitive/local-only unless curated and governed. |
| VOCAB-015 | Product source remains blocked until GT-09. |
| VOCAB-016 | Graphify evidence is supporting generated evidence only, not authority. |
| VOCAB-017 | Cognitive Semantic System substrate remains deferred. |
| VOCAB-018 | Graph remains candidate only. |
| VOCAB-019 | Unknown sensitivity defaults to blocked or needs review. |
| VOCAB-020 | Blockers and limitations must propagate downstream. |
| VOCAB-021 | Deprecated terms must not be used in new P2/P3 contracts except in alias/deprecated registers. |
| VOCAB-022 | P2.1 does not start P2.2, P2.3, P3.1, or P3.2. |

## 23. Future Validation Targets
These are future validation targets only. P2.1 does not execute validation.

| Future validation target | Purpose | Required future gate |
| --- | --- | --- |
| P1.1-P1.5 vocabulary coverage | Check all P1 lanes are represented. | GT-04 |
| Canonical status vocabulary completeness | Check status fields and values. | GT-04 |
| Blocker name coverage | Check canonical blocker list coverage. | GT-04 |
| Sensitivity class coverage | Check sensitivity class list. | GT-04 |
| Source classification coverage | Check source classification list. | GT-04 |
| Posture field coverage | Check posture fields and values. | GT-04 |
| Evidence/validation/security ref naming coverage | Check canonical ref naming. | GT-04 |
| Alias/deprecated register completeness | Check aliases/prohibited terms. | GT-04 |
| Prohibited term detection | Check terms appear only in register context. | GT-04 |
| Blocker propagation rule completeness | Check propagation rules exist. | GT-04 |
| Unknown sensitivity blocking rule completeness | Check unknown defaults to blocked/needs review. | GT-04 |
| Graphify authority boundary invariant | Check evidence-only posture. | GT-04/GT-11 |
| Substrate deferral invariant | Check substrate remains deferred. | GT-04/GT-10 |
| Product inactivity invariant | Check product remains inactive. | GT-04/GT-09 |
| Source tracking blocker invariant | Check tracking remains gated. | GT-04/GT-12 |
| Generated output tracking blocker invariant | Check generated output tracking remains blocked. | GT-04/GT-12 |
| Publication blocker invariant | Check publication remains blocked. | GT-04/GT-12 |
| P2.2 consumption readiness | Check P2.2 can consume vocabulary. | GT-04 |
| P2.3 consumption readiness | Check P2.3 can consume vocabulary. | GT-04 |

## 24. Future Hardening Candidates
These are future candidates only and are not started by P2.1.

| Candidate ticket | Purpose | P2.1 status |
| --- | --- | --- |
| VOCAB-HARD-01 - P2 Vocabulary Schema Extraction | Extract canonical terms into future schema candidate. | Not started. |
| VOCAB-HARD-02 - Deprecated Term Detection Rules | Define future checks for deprecated/prohibited terms. | Not started. |
| VOCAB-HARD-03 - Cross-Lane Blocker Propagation Matrix | Expand blocker propagation rules into matrix. | Not started. |
| VOCAB-HARD-04 - Cross-Lane Status Transition Matrix | Define future status transition semantics. | Not started. |
| VOCAB-HARD-05 - Sensitivity / Source Classification Propagation Model | Expand source and sensitivity propagation rules. | Not started. |
| VOCAB-HARD-06 - P2.2 Evidence Ref Vocabulary Conformance Review | Review future P2.2 against this alignment. | Not started. |
| VOCAB-HARD-07 - P2.3 Retention / Rollback Vocabulary Conformance Review | Review future P2.3 against this alignment. | Not started. |
| VOCAB-HARD-08 - P3 Validation/Security Readiness Vocabulary Gate | Prepare future P3 vocabulary gate. | Not started. |

## 25. Created / Not Created Register
| Artifact or action | P2.1 status |
| --- | --- |
| `0_architecture/governance/agent_platform_shared_metadata_vocabulary_alignment.md` | Created. |
| Shared metadata vocabulary alignment document | Created. |
| P1.1 source document | Not modified. |
| P1.2 source document | Not modified. |
| P1.3 source document | Not modified. |
| P1.4 source document | Not modified. |
| P1.5 source document | Not modified. |
| Context runtime code | Not modified. |
| Provider adapter implementation | Not modified. |
| Tool execution implementation | Not modified. |
| Agent runtime implementation | Not modified. |
| Cognitive Semantic System implementation | Not modified. |
| Validation registry implementation | Not modified. |
| Security implementation | Not modified. |
| `3_platform/_governed_skeleton/` | Not modified. |
| Source loading | Not approved. |
| Product source | Not inspected. |
| Hermes source | Not inspected. |
| Graphify implementation source | Not inspected. |
| External source | Not inspected. |
| Secrets | Not inspected. |
| Credentials | Not inspected. |
| `.env` | Not inspected. |
| Provider/auth | Not configured. |
| Tool execution | Not approved. |
| Agent execution | Not approved. |
| Validation command | Not executed. |
| Tests | Not executed. |
| Graphify | Not rerun. |
| `/graphify` | Not run. |
| Graphify as authority | Not adopted. |
| Graphify as truth engine | Not adopted. |
| `.graphifyignore` | Not modified. |
| `.gitignore` | Not modified. |
| Generated outputs | Not modified or tracked. |
| Source tracking expansion | Not approved. |
| Publication | Not approved. |
| Product activation | Not approved. |
| Cognitive Semantic System substrate | Not selected. |
| Graph as substrate | Not selected. |
| P2.2 | Not started. |
| P2.3 | Not started. |
| P3.1 | Not started. |
| P3.2 | Not started. |
| Git staging/commit/push/force-add/publication | Not authorized or performed. |

## 26. Recommended Next Tickets
After P2.1, the recommended queue is:

| Ticket | Recommendation |
| --- | --- |
| P2.2 - Cross-Lane Evidence Reference Contract | Recommended actual next ticket after explicit instruction. |
| P2.3 - Audit / Retention / Rollback Baseline | Follow after P2.2 or as governed sequence allows. |
| P3.1 - Validation Execution Readiness | Only after P2.1-P2.3 are complete and explicitly approved. |
| P3.2 - Security Enforcement Readiness | Only after P2.1-P2.3 are complete and explicitly approved. |

Recommended actual: P2.2 - Cross-Lane Evidence Reference Contract.

Do not start P2.2. Do not start P2.3. Do not start P3.1. Do not start P3.2.

## 27. Final Verdict
| Question | Answer |
| --- | --- |
| What did P2.1 create? | The canonical Shared Metadata Vocabulary Alignment document. |
| What vocabulary did P2.1 align? | Statuses, blockers, sensitivity classes, source classifications, activation posture, validation posture, security posture, execution posture, provider/auth posture, tracking posture, retention posture, generated-output posture, product posture, substrate posture, and reference field names. |
| Which P1 lanes were consumed? | P1.1 context, P1.2 provider, P1.3 tool, P1.4 agent, and P1.5 Cognitive Semantic System. |
| Which canonical status fields were defined? | `record_status`, `activation_status`, `validation_status`, `security_status`, `execution_status`, `review_status`, and `decision_status`. |
| Which blocker names were canonicalized? | Runtime, source loading, context permission, provider/auth/network/MCP, tool execution, agent execution, validation execution, security review, source tracking, generated output tracking, publication, local-only, product, external, secret, credential, unknown sensitivity, Graphify authority/raw output, substrate, graph substrate, retention, rollback, and incident blockers. |
| Which sensitivity classes were canonicalized? | Public governance metadata, internal governance metadata, implementation metadata, generated sensitive, generated Graphify evidence, generated local-only, local-only, product restricted, external restricted, credential reference, secret value, provider auth material, runtime state, and unknown sensitivity. |
| Which source classifications were canonicalized? | Governance, implementation, validation, security, context, provider, tool, agent, semantic, generated Graphify evidence, generated local-only, local-only source, product restricted, external source, credential reference, secret value, provider auth material, runtime state, and unknown sensitivity. |
| Which posture fields were canonicalized? | `provider_auth_posture`, `tracking_posture`, `retention_posture`, `generated_output_posture`, `product_posture`, and `substrate_posture`. |
| Which evidence/validation/security ref names were canonicalized? | `EvidenceRef`, `evidence_refs`, `ValidationRef`, `validation_refs`, `SecurityRef`, and `security_refs`. |
| Which aliases or deprecated terms were registered? | Lane-specific ref aliases were preserved; `proof_refs`, `test_refs`, and `permission_refs` were deprecated; Graphify authority/truth/substrate terms and executable metadata terms were prohibited or deprecated. |
| Which drift decisions were made? | P2.1 chose shared field names where safe, preserved lane-specific object prefixes for clarity, and resolved permission-implying drift toward stricter blocker/non-activation terms. |
| Did P2.1 modify P1 documents? | No. |
| Did P2.1 activate runtime? | No. |
| Did P2.1 execute validation? | No. |
| Did P2.1 approve provider/auth? | No. |
| Did P2.1 approve tool/agent execution? | No. |
| Did P2.1 inspect product source? | No. |
| Did P2.1 rerun or adopt Graphify? | No. |
| Did P2.1 approve generated output tracking or source tracking expansion? | No. |
| Did P2.1 select Cognitive Semantic System substrate? | No. Cognitive Semantic System substrate remains deferred. |
| What is the next recommended ticket? | P2.2 - Cross-Lane Evidence Reference Contract, after explicit instruction only. |

Stop rule: After completing P2.1, STOP. Do not start P2.2. Do not start P2.3. Do not start P3.1. Do not start P3.2. Do not implement code. Do not run validation. Do not run tests. Do not inspect secrets. Do not inspect credentials. Do not inspect `.env`. Do not configure provider/auth. Do not execute tools. Do not activate agents. Do not activate runtime behavior. Do not load source. Do not inspect product source. Do not inspect Hermes source. Do not inspect Graphify implementation source. Do not rerun Graphify. Do not modify generated outputs. Do not approve generated output tracking. Do not approve source tracking expansion. Do not modify `.gitignore`. Do not modify `.graphifyignore`. Do not select Cognitive Semantic System substrate. Do not select graph as substrate. Do not adopt Graphify as authority. Do not treat Graphify as truth engine. Do not stage, commit, push, force-add, or publish.
