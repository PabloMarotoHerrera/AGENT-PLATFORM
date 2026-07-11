# P3.3 - Tool Execution Activation Decision

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Tool Execution Activation Decision |
| Ticket | P3.3 |
| Status | Accepted tool execution activation decision |
| Date | 2026-07-04 |
| Scope | Decide whether any narrow future exact tool execution scope may become an activation candidate while preserving that P3.3 is a governance decision record only. |
| Authority | Tool execution activation decision only, not tool execution, shell execution, subprocess execution, filesystem execution, network execution, package-manager execution, build execution, test execution, CI execution, Git execution, validation execution, source loading, source inspection, security enforcement implementation, provider/auth/API/MCP activation, agent execution, product activation, live connector activation, Graphify adoption, GBrain adoption, Hermes activation, Cadence activation, generated output tracking, source tracking expansion, Cognitive Semantic System substrate selection, or publication. |
| Related documents | P3.R, P3.0, P3.1, P3.2, P2.KR, P2.R, P2.1, P2.2, P2.3, P1.3, P1.1, P1.2, P1.4, P1.5, P0.1, P0.2, P0.3, G-19, S-03, S-04, Graphify Repo Map Summary, CSS ADR/audit, `.gitignore`, `.graphifyignore`. |
| Optional dependency | P3.4 Provider/Auth/API/MCP Activation Decision is absent in P3.3 posture checks; provider-bound tool scopes carry `pending_P3.4_provider_auth_decision_alignment`. |
| Output | Tool Execution Activation Decision. |

P3.3 is activation-decision only. Decision is not execution. Readiness is not activation. AGENT PLATFORM remains pre-active at AL-1.

## 2. Purpose
P3-A closed readiness: source classification, validation readiness, security readiness, and activation readiness reconciliation. P3-B is activation-decision only.

P3.3 decides whether any future exact tool execution scope can become an activation candidate. P3.3 consumes P3.0 source classification, P3.1 validation readiness, P3.2 security readiness, P3.R reconciliation, P2.3 audit/retention/rollback, P2.2 EvidenceRef, P2.1 vocabulary, P1.3 tool boundary, P0 gates, S-03, and S-04.

P3.3 default posture is `tool_execution_activation_deferred`. P3.3 may define exact future tool activation criteria. P3.3 may mark narrow metadata-only/documentation conformance tooling as `candidate_for_future_exact_activation` only if all blockers, gates, input/output surfaces, retention, rollback, incident, and human approval requirements are preserved.

P3.3 does not execute tools. P3.3 does not approve broad tool execution. P3.3 does not start P3.4, P3.5, P3.BR, P4, or P5.

## 3. Current Posture
| Area | Current state | P3.3 decision interpretation | Blocked interpretation |
| --- | --- | --- | --- |
| AGENT PLATFORM activation level | AL-1 metadata skeleton. | Decision metadata only. | Runtime activation. |
| P3.R readiness status | Mandatory input present. | P3.3 is eligible as decision record. | Tool execution approval. |
| P3.0 source classification | Mandatory input present. | Source classifications constrain future tool inputs. | Source loading permission. |
| P3.1 validation readiness | Mandatory input present. | Validation readiness informs gates and refs. | Validation execution. |
| P3.2 security readiness | Mandatory input present. | Security readiness constrains candidates. | Security enforcement runtime. |
| P1.3 tool metadata contract | Metadata-only tool boundary. | Tool metadata is not tool execution. | Executable tool metadata. |
| S-04 tool/shell/network/MCP policy | Execution-constraining policy. | Blocks shell, network, MCP, tools until gates. | Permission grant. |
| S-03 local-only/secrets/credentials policy | Secrets/credentials/local-only constraints. | Blocks unsafe inputs/outputs. | Secret/credential handling. |
| documentation-only checks | Future exact candidate class only. | Possible candidate for future exact activation. | Immediate execution. |
| metadata-only checks | Future exact candidate class only. | Possible candidate for future exact activation. | Broad tool approval. |
| validation command candidates | Deferred. | Future GT-04 and exact proposal required. | Running validation. |
| shell/subprocess | Blocked. | Future exact review only. | shell commands or subprocess execution. |
| filesystem reads/writes | Blocked except future exact approved metadata-doc reads. | No broad filesystem reads/writes. | Broad filesystem reads/writes. |
| network calls | Blocked. | Requires P3.4/GT-08 if ever scoped. | Network execution. |
| package-manager commands | Blocked. | No future candidate in P3.3. | Package execution. |
| build/test/CI commands | Blocked. | Validation/test/build/CI remain gated. | Build/test/CI execution. |
| Git commands | Blocked. | No Git mutation approval. | Git execution. |
| Graphify commands | Blocked. | No rerun or adoption. | Graphify authority/substrate. |
| Codegraph commands | Deferred or blocked pending external tool review. | Separate exact review required. | Codegraph-like tooling execution. |
| MCP tool calls | Blocked. | Pending P3.4 and GT-08/GT-07. | MCP active. |
| live connector tools | Blocked. | Connector gates required. | Live connector activation. |
| product tools | Blocked. | GT-09 and future exact decision required. | Product activation. |
| generated-output tools | Blocked. | Output tracking/retention gates required. | Generated output tracking. |
| provider-bound tools | Blocked or pending P3.4. | `pending_P3.4_provider_auth_decision_alignment`. | Provider/auth activation. |
| agent-bound tools | Blocked until P3.5. | Future P3.5 interface only. | Agent runtime activation. |

AGENT PLATFORM remains pre-active at AL-1. P3.3 is decision only. Decision is not execution. No tool class becomes executable by P3.3. No broad tool execution is approved.

## 4. Inputs Reviewed
| Input group | Document | Review mode | Decision use | Limitation |
| --- | --- | --- | --- | --- |
| P2.3 audit/retention/rollback baseline | `agent_platform_audit_retention_rollback_baseline.md` | metadata_contract_review | Retention, rollback, incident posture. | No automation. |
| P2.2 EvidenceRef contract | `agent_platform_cross_lane_evidence_reference_contract.md` | metadata_contract_review | Evidence boundaries. | Evidence does not decide. |
| P2.1 shared vocabulary | `agent_platform_shared_metadata_vocabulary_alignment.md` | governance_markdown_review | Canonical vocabulary. | No schema runtime. |
| P1.3 tool execution boundary contract | `agent_platform_tool_execution_boundary_contract_hardening.md` | metadata_contract_review | Tool boundary input. | Metadata-only. |
| P1.1 context contract | `agent_platform_context_runtime_contract_hardening.md` | metadata_contract_review | Context input boundaries. | Context inclusion is not permission. |
| P1.2 provider contract | `agent_platform_provider_adapter_metadata_contract_hardening.md` | metadata_contract_review | Provider-bound tool blockers. | Provider metadata is not activation. |
| P1.4 agent contract | `agent_platform_agent_runtime_boundary_contract_hardening.md` | metadata_contract_review | Agent-bound tool blockers. | Agent metadata is not execution. |
| P1.5 Cognitive Semantic System contract | `agent_platform_cognitive_semantic_system_prototype_hardening.md` | metadata_contract_review | Substrate blockers. | Substrate deferred. |
| P0.1 activation gates | `agent_platform_activation_gate_enforcement_map.md` | governance_markdown_review | Gate mapping. | Gate refs are not approvals. |
| P0.2 validation gate design | `agent_platform_validation_execution_gate_design.md` | governance_markdown_review | GT-04 boundary. | No validation run. |
| P0.3 security hardening | `agent_platform_security_enforcement_hardening_plan.md` | governance_markdown_review | Security hardening input. | No enforcement. |
| S-04 tool/shell/network/MCP policy | `agent_platform_tool_shell_network_mcp_execution_policy.md` | policy_review | Tool/shell/network/MCP constraints. | No execution. |
| S-03 local-only/secrets/credentials policy | `agent_platform_local_only_secrets_credentials_policy.md` | policy_review | Secret/local-only constraints. | No secret inspection. |
| CSS ADR/audit | CSS ADR/audit docs. | governance_markdown_review | Substrate-deferred context. | No substrate selection. |
| `.gitignore` | Root ignore policy. | policy_review | Tracking boundary context. | Not modified. |
| `.graphifyignore` | Root Graphify boundary. | policy_review | Graphify/source boundary context. | Not modified. |
| README | Root workspace documentation. | governance_markdown_review | Orientation. | No runtime effect. |

Only governance, readiness, metadata, policy, and curated evidence documents are reviewed. P3.3 does not inspect source, secrets, credentials, products, generated outputs, tools, providers, agents, or external source contents.

## 5. Dependency Posture
| Dependency | Required for P3.3 | Current posture | Decision consequence | Blocker if missing |
| --- | --- | --- | --- | --- |
| P3.0 source classification | Yes. | Present. | Tool inputs must follow P3.0 classes. | pending_P3.0_source_classification_alignment. |
| P3.1 validation readiness | Yes. | Present. | Validation refs/gates inform candidates. | pending_P3.1_validation_alignment. |
| P3.2 security readiness | Yes. | Present. | Security refs/blockers constrain candidates. | pending_P3.2_security_alignment. |
| P3.R reconciliation | Yes. | Present. | P3-A drift closure consumed. | P3.3 blocked if absent. |
| P2.3 retention/rollback/incident baseline | Yes. | Present. | Retention/rollback/incident required. | retention_review_blocker. |
| P2.2 EvidenceRef contract | Yes. | Present. | Evidence refs required. | evidence_alignment_blocker. |
| P2.1 vocabulary | Yes. | Present. | Decision status vocabulary applied. | vocabulary_alignment_blocker. |
| P1.3 tool execution boundary | Yes. | Present. | Tool boundary preserved. | tool_execution_blocker. |
| S-04 tool/shell/network/MCP policy | Yes. | Present. | Execution surfaces constrained. | security_review_blocker. |
| S-03 local-only/secrets/credentials policy | Yes. | Present. | Secret/local-only blockers preserved. | secret_exposure_blocker. |
| P3.4 provider/auth decision | Optional for P3.3, required for provider-bound tools. | Absent. | Provider/network/API/MCP-bound tools remain blocked or pending. | pending_P3.4_provider_auth_decision_alignment. |

P3.3 can decide tool execution posture without P3.4, but provider-bound, network-bound, API-bound, MCP-bound, live-connector-bound, or auth-bound tools must remain blocked or pending P3.4. If P3.4 is absent, mark provider/auth dependency as `pending_P3.4_provider_auth_decision_alignment` for any provider-bound tool scope. P3.3 must not assume provider/auth approval.

## 6. ToolExecutionActivationDecision Object
| Field | Meaning |
| --- | --- |
| `decision_id` | Stable decision record ID. |
| `decision_status` | P3.3 decision posture. |
| `candidate_tool_scope` | Exact future scope if any. |
| `allowed_future_tool_classes` | Future candidate classes only. |
| `blocked_tool_classes` | Tool classes blocked by P3.3. |
| `deferred_tool_classes` | Tool classes deferred to future gates. |
| `rejected_tool_classes` | Tool classes rejected for scope. |
| `required_gates` | Future gates required before activation. |
| `required_validation_refs` | Validation refs required for future review. |
| `required_security_refs` | Security refs required for future review. |
| `required_evidence_refs` | Evidence refs required for future review. |
| `source_classification_requirements` | P3.0 source class constraints. |
| `input_surface_requirements` | Exact allowed/blocked inputs. |
| `output_surface_requirements` | Exact output/retention/tracking constraints. |
| `side_effect_profile` | Side effect classification. |
| `filesystem_profile` | Filesystem read/write posture. |
| `network_profile` | Network posture. |
| `provider_dependency_profile` | Provider/auth/API posture. |
| `mcp_dependency_profile` | MCP posture. |
| `generated_output_profile` | Generated output posture. |
| `product_boundary` | Product/Siamese boundary. |
| `graphify_boundary` | Graphify command/evidence boundary. |
| `gbrain_hermes_cadence_boundary` | GBrain/Hermes/Cadence boundary. |
| `retention_posture` | Required retention posture. |
| `rollback_posture` | Required rollback posture. |
| `incident_posture` | Required incident posture. |
| `audit_posture` | Required audit posture. |
| `human_approval_required` | Human approval flag. |
| `stop_rules` | Stop rules that must terminate future activation. |
| `limitations` | Non-activation limitations. |
| `review_required` | Required future review. |
| `created_at` | Decision creation date. |

The ToolExecutionActivationDecision is a governance decision record. It is not an executor, runtime config, allowlist implementation, tool registry mutation, policy engine, CI rule, or command approval.

## 7. Decision Status Vocabulary
| decision_status | Meaning | Allowed P3.3 use | Blocked interpretation |
| --- | --- | --- | --- |
| `tool_execution_activation_deferred` | Default tool execution activation decision is deferred. | Baseline posture. | Execution approval. |
| `activation_blocked` | Tool class is blocked. | Preserve stop condition. | Workaround permission. |
| `candidate_for_future_exact_activation` | Narrow future exact scope may be reviewed later. | Metadata-only/documentation checks only if exact and gated. | Current execution approval. |
| `eligible_for_later_implementation_ticket` | Future implementation ticket may be considered. | Planning only. | Implementation approval. |
| `rejected_for_scope` | Scope unsafe or too broad. | Stop and rescope. | Adjacent approval. |
| `pending_alignment` | Dependency not resolved. | Carry P3.4/P3.5 alignment needs. | Silent approval. |
| `not_applicable` | Not a tool activation concept. | Avoid false status. | Hidden approval. |
| `unknown` | Unknown posture. | Block/review. | Safe default. |

Mandatory default: `tool_execution_activation_deferred`.

No `decision_status` value in P3.3 executes tools or approves broad tool execution.

## 8. Candidate Activation Scope Model
| Scope requirement | Required value | Rationale | Blocker if absent |
| --- | --- | --- | --- |
| Exact tool class | One bounded class. | Prevents broad activation. | tool_execution_blocker. |
| Exact purpose | One governance/metadata purpose. | Prevents drift. | rejected_for_scope. |
| Exact command/action proposal format | Future ticket must specify exact action. | Human review requires exactness. | tool_execution_blocker. |
| Exact cwd, if command-like | Exact future working directory. | Prevents broad filesystem scope. | source_loading_blocker. |
| Exact input surfaces | Approved governance/metadata docs only. | Protects source classes. | source_loading_blocker. |
| Exact output surfaces | No output or exact safe metadata report. | Controls generated output. | generated_output_tracking_blocker. |
| No secret/credential exposure | Required. | S-03 boundary. | secret_exposure_blocker. |
| No product source | Required. | GT-09 boundary. | product_source_blocker. |
| No external source contents | Required. | GT-11 boundary. | external_source_blocker. |
| No generated output tracking | Required. | GT-12 boundary. | generated_output_tracking_blocker. |
| No source tracking expansion | Required. | GT-02/GT-12 boundary. | source_tracking_blocker. |
| No publication | Required. | Publication remains gated. | publication_blocker. |
| No Git mutation | Required. | Git remains blocked. | source_tracking_blocker. |
| No network | Required for P3.3 candidates. | Avoid provider/API/MCP activation. | provider_network_blocker. |
| No provider/auth | Required unless future P3.4 allows exact scope. | P3.4 absent. | pending_P3.4_provider_auth_decision_alignment. |
| No MCP | Required unless future P3.4/GT-08/GT-07 allow exact scope. | MCP activation risk. | provider_mcp_blocker. |
| No live connectors | Required. | Connector activation blocked. | live_connector_activation_blocker. |
| No broad filesystem reads | Required. | Source loading boundary. | source_loading_blocker. |
| No filesystem writes except future exact approved output | Required. | Prevents mutation. | generated_output_tracking_blocker. |
| No runtime source loading | Required. | Source classification is not source loading. | source_loading_blocker. |
| validation refs | Required before future review. | P3.1 alignment. | validation_execution_blocker. |
| security refs | Required before future review. | P3.2 alignment. | security_review_blocker. |
| evidence refs | Required before future review. | P2.2 alignment. | evidence_alignment_blocker. |
| retention posture | Required. | P2.3 boundary. | retention_review_blocker. |
| rollback posture | Required. | Safe failure handling. | rollback_readiness_blocker. |
| incident route | Required. | Safe incident handling. | incident_route_blocker. |
| human approval | Required. | Final gate discipline. | human_approval_blocker. |

A candidate scope must be exact. Generic tool execution remains blocked.

## 9. Tool Class Decision Matrix
| Tool class | Current P3.3 decision | Allowed future candidate use | Blocked use | Required gates | Validation requirements | Security requirements | Source classification requirements | Input/output requirements | Side effect profile | Retention/rollback/incident posture |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| documentation-only checks | `candidate_for_future_exact_activation` | Exact metadata-doc conformance candidate only. | Current execution. | GT-04/GT-05/GT-07 as applicable. | ValidationRef proposal required. | SecurityRef required. | Governance metadata only. | Exact docs; no writes or no exact safe output. | No side effect. | Metadata-only retention; rollback/incident routes required. |
| metadata-only checks | `candidate_for_future_exact_activation` | Exact bounded metadata checks. | Broad scans/source loading. | GT-04/GT-05/GT-07. | ValidationRef required. | SecurityRef required. | Governance/metadata only. | Exact input/output. | No side effect. | Metadata-only retention. |
| governance document section checks | `candidate_for_future_exact_activation` | Exact section presence checks in approved docs. | Reading restricted source. | GT-04/GT-05/GT-07. | ValidationRef required. | SecurityRef required. | governance_metadata. | Exact documents. | No side effect. | Metadata-only. |
| vocabulary conformance checks | `candidate_for_future_exact_activation` | Exact P2.1/P3 vocabulary checks. | Auto-rewrite or execution. | GT-04/GT-05/GT-07. | ValidationRef required. | SecurityRef required. | governance_metadata. | Exact docs; no mutation. | No side effect. | Metadata-only. |
| EvidenceRef schema checks | `candidate_for_future_exact_activation` | Exact schema/conformance candidate. | Runtime schema enforcement. | GT-04/GT-05/GT-07. | ValidationRef required. | SecurityRef required. | governance_metadata. | Exact docs. | No side effect. | Metadata-only. |
| blocker propagation checks | `candidate_for_future_exact_activation` | Exact metadata propagation checks. | Bypass blockers. | GT-04/GT-05/GT-07. | ValidationRef required. | SecurityRef required. | governance_metadata. | Exact docs. | No side effect. | Metadata-only. |
| source classification completeness checks | `candidate_for_future_exact_activation` | Exact P3.0 matrix checks. | Source inspection. | GT-04/GT-05/GT-07. | ValidationRef required. | SecurityRef required. | P3.0 governance metadata only. | Exact docs. | No side effect. | Metadata-only. |
| no-secret/no-credential metadata invariant checks | `candidate_for_future_exact_activation` | Metadata-only invariant check, no secret scanning. | Secret scanning or value inspection. | GT-04/GT-05/GT-07. | ValidationRef required. | SecurityRef required. | governance metadata only. | Exact docs; no sensitive paths. | No side effect. | Incident route required. |
| Graphify evidence-only invariant checks | `candidate_for_future_exact_activation` | Check governance text only. | Graphify rerun/raw output loading. | GT-04/GT-05/GT-07. | ValidationRef required. | SecurityRef required. | curated governance/evidence docs only. | Exact docs. | No side effect. | Metadata-only. |
| Cognitive Semantic System substrate-deferred checks | `candidate_for_future_exact_activation` | Check governance text only. | Substrate selection. | GT-04/GT-05/GT-07. | ValidationRef required. | SecurityRef required. | governance metadata only. | Exact docs. | No side effect. | Metadata-only. |
| generated output tracking blocked checks | `candidate_for_future_exact_activation` | Check governance text only. | Generated output tracking. | GT-04/GT-05/GT-07. | ValidationRef required. | SecurityRef required. | governance metadata only. | Exact docs. | No side effect. | Metadata-only. |
| product source blocked checks | `candidate_for_future_exact_activation` | Check governance text only. | Product source inspection. | GT-04/GT-05/GT-07. | ValidationRef required. | SecurityRef required. | governance metadata only. | Exact docs. | No side effect. | Product incident route. |
| validation command candidates | `activation_deferred` | Future exact GT-04 candidate only. | Running validation. | GT-04/GT-05/GT-07. | Exact validation proposal required. | SecurityRef required. | No blocked source classes. | Exact inputs/outputs. | Potential side effect unless proven none. | Full P2.3 posture required. |
| shell commands | `activation_blocked` | None by P3.3. | shell commands. | GT-07/S-04/GT-15. | ValidationRef required later. | Security review required. | Exact safe scope required later. | Exact command/cwd/output later. | Side effects likely. | Full rollback/incident required. |
| subprocess execution | `activation_blocked` | None by P3.3. | subprocess execution. | GT-07/S-04. | Required later. | Required later. | Exact scope later. | Exact command later. | Side effects likely. | Full rollback/incident required. |
| filesystem reads | `activation_blocked` | Future exact governance doc reads only if approved. | Broad filesystem reads. | GT-01/GT-05/GT-07. | Required later. | Required later. | governance_metadata only unless gated. | Exact paths only. | Read side effect risk. | Retention limits required. |
| filesystem writes | `activation_blocked` | Future exact safe output only if approved. | Writes/mutations. | GT-07/GT-12/GT-15. | Required later. | Required later. | Output class exact. | Exact output path. | Write side effect. | Rollback/incident required. |
| network calls | `activation_blocked` | None by P3.3. | network calls. | P3.4/GT-08/GT-07. | Required later. | Required later. | No provider/auth by P3.3. | Exact endpoint later. | External side effect. | Full incident required. |
| package-manager commands | `activation_blocked` | None. | install/update/resolve. | GT-07/GT-05. | Required later. | Required later. | External/source risk. | Exact command later. | High side effect. | Rollback required. |
| build commands | `activation_blocked` | None. | build execution. | GT-07. | Required later. | Required later. | Source/runtime risk. | Exact command later. | Side effect. | Rollback required. |
| test commands | `activation_blocked` | None. | test execution. | GT-04/GT-07. | Required later. | Required later. | Exact classified inputs. | Exact command later. | Side effect. | Retention required. |
| CI commands | `activation_blocked` | None. | CI execution. | GT-07/GT-12/GT-15. | Required later. | Required later. | Source/tracking risk. | Exact CI scope later. | Side effect. | Incident required. |
| Git commands | `activation_blocked` | None. | Git commands or mutation. | GT-02/GT-12. | Not applicable until scoped. | Security review. | Exact paths only later. | No broad staging. | Mutating side effect. | Rollback required. |
| Graphify commands | `activation_blocked` | None. | Graphify commands, rerun, adoption. | GT-11/GT-12/GT-15. | Required later. | Required later. | No raw outputs. | No output tracking. | Generated output side effect. | Output incident route. |
| Codegraph commands, if considered later | `activation_deferred` | Separate external tool review only. | Codegraph-like tooling execution. | GT-07/GT-11/GT-05. | Required later. | Required later. | Exact source scope. | Exact outputs. | Unknown. | Full posture required. |
| MCP tool calls | `activation_blocked` | None by P3.3. | MCP tool calls. | P3.4/GT-08/GT-07. | Required later. | Required later. | Provider/MCP classes. | Exact server/tool later. | External side effect. | Incident required. |
| live connector tools | `activation_blocked` | None. | Connector read/sync/poll. | P3.4/GT-08/GT-15. | Required later. | Required later. | live_connector_class blocked. | Exact connector later. | External side effect. | Full retention/incident. |
| product tools | `activation_blocked` | None. | Product operations/source. | GT-09/GT-07. | Required later. | Required later. | product_restricted blocked. | Exact product scope later. | Product side effect. | Product incident route. |
| generated-output tools | `activation_blocked` | None unless future exact retention/tracking gates. | Output generation/tracking. | GT-12/GT-15/GT-07. | Required later. | Required later. | generated_local_only constraints. | Exact output later. | Generated side effect. | Retention/incident required. |
| provider-bound tools | `pending_alignment` | Pending P3.4 only. | Provider/API/auth use. | P3.4/GT-08/GT-07. | Required later. | Required later. | provider_auth_material blocked. | Exact provider later. | External side effect. | Full incident required. |
| agent-bound tools | `activation_blocked` | None until P3.5. | Agent runtime/handoff tool use. | P3.5/GT-06/GT-07. | Required later. | Required later. | agent_metadata only. | Exact agent scope later. | Runtime side effect. | Rollback/incident required. |
| GBrain/Hermes/Cadence tools | `activation_blocked` | None. | GBrain/Hermes/Cadence activation. | EXT.GB-01/GT-06/GT-08/GT-15 as scoped. | Required later. | Required later. | cadence_reference_candidate blocked. | Exact future scope. | Always-on risk. | Full posture required. |

## 10. Default Decision
| Default decision | Rationale | Allowed candidate exception | Required gates | Blockers preserved |
| --- | --- | --- | --- | --- |
| `tool_execution_activation_deferred` | P3-B may define exact future criteria, but it must not execute tools or approve broad tool execution. | Narrow metadata-only/documentation checks as future candidates only. | GT-04, GT-05, GT-07, plus GT-08/GT-09/GT-11/GT-12/GT-15 as applicable. | source_loading, tool_execution, validation_execution, security_review, generated_output_tracking, source_tracking, publication, provider/auth, product, live connector, Graphify, Cadence, incident, rollback blockers. |

No broad tool execution is approved by P3.3.

## 11. Candidate Future Exact Activation
Candidate:

`candidate_for_future_exact_activation: metadata-only validation/check tooling`

Allowed only for future exact-scope candidates such as documentation conformance checks, metadata schema checks, vocabulary conformance checks, EvidenceRef shape checks, blocker propagation checks, source classification completeness checks, and invariant text checks over governance metadata documents.

Required constraints: exact command/action proposal in a future ticket; exact input document list; exact output path or no output; no source loading beyond approved governance/metadata docs; no product source; no external source contents; no secrets; no credentials; no provider auth material; no network; no MCP; no live connectors; no package manager; no build/test/CI; no Git mutation; no Graphify rerun; no generated output tracking; no source tracking expansion; no publication; human approval required; rollback route required; incident route required; retention posture required; GT-04 / GT-05 / GT-07 as applicable.

Candidate status is not execution approval. Candidate status only makes a future exact implementation/activation ticket eligible for review.

## 12. Blocked Tool Classes
| Blocked class | Blocker | Required future gate | Reason | Future review route |
| --- | --- | --- | --- | --- |
| shell commands | tool_execution_blocker | GT-07/S-04/GT-15 | Shell execution has broad side effects. | Future exact tool activation review. |
| subprocess execution | tool_execution_blocker | GT-07/S-04 | Subprocess execution is runtime execution. | Future exact tool activation review. |
| filesystem broad reads | source_loading_blocker | GT-01/GT-05/GT-07 | Broad reads can inspect restricted source. | Source classification and tool review. |
| filesystem writes | generated_output_tracking_blocker | GT-07/GT-12/GT-15 | Writes mutate workspace or outputs. | Output/rollback review. |
| network calls | provider_network_blocker | P3.4/GT-08/GT-07 | Network implies provider/API risk. | P3.4 then exact tool review. |
| package-manager commands | tool_execution_blocker | GT-07/GT-05 | Dependency and environment mutation risk. | Future dependency/tool review. |
| build commands | tool_execution_blocker | GT-07 | Build side effects and source loading risk. | Future exact review. |
| test commands | validation_execution_blocker | GT-04/GT-07 | Tests are validation execution. | P3.1/GT-04 route. |
| CI commands | tool_execution_blocker | GT-07/GT-12/GT-15 | CI can publish, mutate, or leak outputs. | Future CI readiness review. |
| Git commands | source_tracking_blocker | GT-02/GT-12 | Git mutation/tracking not approved. | Source tracking gate. |
| Graphify commands | graphify_raw_output_blocker | GT-11/GT-12/GT-15 | Rerun/adoption/output tracking not approved. | Graphify gate if proposed. |
| Codegraph commands unless separately reviewed | external_source_blocker | GT-07/GT-11/GT-05 | External tool/source risk. | Separate exact external tool review. |
| MCP tool calls | provider_mcp_blocker | P3.4/GT-08/GT-07 | MCP activation not approved. | P3.4 then exact review. |
| live connector tools | live_connector_activation_blocker | GT-08/GT-05/GT-15 | Connector access not approved. | Live connector review. |
| product tools | product_source_blocker | GT-09/GT-07 | Product source/operations blocked. | Product gate. |
| generated-output tools | generated_output_tracking_blocker | GT-12/GT-15/GT-07 | Output handling/tracking not approved. | Retention/output review. |
| provider-bound tools without P3.4 | pending_P3.4_provider_auth_decision_alignment | P3.4/GT-08 | Provider/auth absent. | P3.4. |
| agent-bound tools without P3.5 | agent_execution_blocker | P3.5/GT-06/GT-07 | Agent runtime not approved. | P3.5. |
| GBrain/Hermes/Cadence tools | cadence_activation_blocker | EXT.GB-01/GT-06/GT-15 | Future inactive candidates only. | Future exact gate. |

## 13. Required Gates
| Gate | Applies to | Required before | Evidence needed | Blocker if absent |
| --- | --- | --- | --- | --- |
| GT-01 scope/source review | Filesystem/source inputs. | Any source review beyond approved docs. | Exact path/scope. | source_loading_blocker. |
| GT-02 source tracking posture | Git/source tracking. | Tracking/staging changes. | Exact tracking plan. | source_tracking_blocker. |
| GT-04 validation execution | Validation command candidates. | Validation commands. | ValidationRef and output plan. | validation_execution_blocker. |
| GT-05 security review | Sensitive/tool input/output classes. | Security-sensitive candidate review. | SecurityRef and risk posture. | security_review_blocker. |
| GT-06 runtime/agent activation | Agent-bound/runtime tools. | Runtime or agent tool use. | Runtime scope and rollback. | runtime_activation_blocker. |
| GT-07 tool execution | Any tool execution. | Any actual tool activation. | ToolDecision, exact scope, S-04 review. | tool_execution_blocker. |
| GT-08 provider/auth/API/MCP | Network/provider/MCP-bound tools. | Provider/API/MCP/auth use. | P3.4 decision and auth/security refs. | provider_auth_blocker. |
| GT-09 product/Siamese source/product activation | Product tools. | Product source/operation. | ProductRef and security posture. | product_source_blocker. |
| GT-10 Cognitive Semantic System substrate | Semantic substrate tools. | Substrate selection. | Substrate decision evidence. | substrate_selection_blocker. |
| GT-11 external source review | External tools/sources. | External source/tool review. | Source/license/security refs. | external_source_blocker. |
| GT-12 publication/source tracking/generated output tracking | Outputs, Git, publication. | Tracking/publishing generated or source outputs. | Exact artifact/path review. | publication_blocker. |
| GT-13 state/persistence/substrate storage | State/persistence tools. | Persistent state. | Persistence and rollback design. | rollback_readiness_blocker. |
| GT-15 incident/rollback/publication safety | Any side-effecting/sensitive tool. | Activation with rollback/incident risk. | Retention, rollback, incident refs. | incident_route_blocker. |

Gate references are not approvals. Gate references indicate future prerequisites only.

## 14. Evidence / Validation / Security Interfaces
| Interface | Required refs | P3.3 use | Blocked interpretation | Downstream consumer |
| --- | --- | --- | --- | --- |
| EvidenceRef from P2.2 | EvidenceRef, source_refs, limitations. | Support decision rationale. | Evidence as approval. | P3.BR/future tool tickets. |
| ValidationRef from P3.1 | ValidationRef and validation_status. | Future validation readiness input. | Validation execution approval. | Future exact activation review. |
| SecurityRef from P3.2 | SecurityRef and blockers. | Security constraints. | Permission grant. | Future exact activation review. |
| SourceClassificationRef from P3.0 | source_classification, sensitivity. | Input/output eligibility. | Source loading permission. | Future tool tickets. |
| RetentionRecord from P2.3 | retention_posture. | Output handling constraints. | Persistence approval. | Future tool tickets. |
| RollbackRecord from P2.3 | rollback refs. | Rollback readiness. | Rollback automation. | Future tool tickets. |
| IncidentRecord from P2.3 | incident refs. | Incident route. | Incident automation. | Future tool tickets. |
| ToolBoundaryRef from P1.3 | Tool boundary refs. | Preserve tool metadata boundary. | Tool execution approval. | P3.BR. |
| ProviderDecisionRef from future/P3.4 where provider-bound | P3.4 decision refs. | Provider-bound gating. | Provider/auth approval by P3.3. | P3.4/P3.BR. |
| AgentDecisionRef from future/P3.5 where agent-bound | P3.5 decision refs. | Agent-bound gating. | Agent activation by P3.3. | P3.5/P3.BR. |

Evidence supports; it does not decide. Validation evaluates; governance decides. Security constrains; it does not activate. Source classification is not source loading permission. Tool metadata is not tool execution.

## 15. Source Classification Interfaces
| Source/data class | P3.0 classification | Tool decision consequence | Blocked input | Required gate |
| --- | --- | --- | --- | --- |
| Governance metadata | `governance_metadata` | Only future metadata/documentation checks may use exact docs. | Broad reads or mutation. | GT-04/GT-05/GT-07 for toolized checks. |
| Implementation metadata | `implementation_metadata` | Metadata posture only. | Live code/source execution. | GT-01/GT-07. |
| Path-only source surfaces | path-only classes. | Presence metadata only. | Content inspection. | GT-01/GT-05. |
| External source candidates | `external_source_candidate` | Blocked by default. | External source contents. | GT-11. |
| GBrain candidate | `external_source_candidate` + `cadence_reference_candidate` | Blocked, not adopted. | Source, install, run, import. | EXT.GB-01/GT-11 if approved. |
| Hermes candidate | `cadence_reference_candidate` | Blocked, inactive. | Hermes runtime/source. | Future exact gate. |
| Graphify curated evidence | `generated_graphify_evidence` | Evidence only. | Graphify commands/raw output. | GT-11/GT-12/GT-15 if expanding. |
| Raw Graphify outputs | `generated_local_only` | Blocked. | Raw output loading. | GT-12/GT-15. |
| Generated outputs | `generated_local_only` | Blocked unless future exact output gate. | Tracking/publication. | GT-12/GT-15. |
| Product-restricted source | `product_restricted` | Blocked. | Product/Siamese source. | GT-09. |
| Secrets/credentials | `secret_value` / `credential_reference` | Never input. | Secret/credential content. | Secure incident route. |
| Provider auth material | `provider_auth_material` | Never input. | Tokens/config/session/auth. | GT-08/S-03. |
| Live connector classes | `live_connector_class` | Blocked. | Raw connector payloads. | GT-08/GT-15. |
| Datasets/models | `dataset_model_artifact` | Blocked by default. | Contents/models/data. | GT-01/GT-05/GT-12/GT-15. |
| Vector/graph candidates | Candidate metadata. | No implementation/substrate. | DB/index/persistence. | GT-10/GT-13. |
| Runtime state | `runtime_state` | Blocked. | Logs/state/cache. | GT-06/GT-13/GT-15. |

P3.3 must not approve tool inputs from blocked, unknown, secret, credential, product-restricted, external-source, generated-output, GBrain/Hermes, Graphify raw output, live connector, or runtime-state surfaces unless future gates approve exact scope.

## 16. Input Surface Requirements
| Input surface type | Allowed for future candidate? | Required gate | Blocker | Limitation |
| --- | --- | --- | --- | --- |
| Approved governance/metadata docs | Yes, only exact future scope. | GT-04/GT-05/GT-07 if toolized. | tool_execution_blocker until approved. | No mutation. |
| Implementation metadata docs | Maybe, exact scope only. | GT-01/GT-05/GT-07. | source_loading_blocker. | Metadata docs only. |
| Live implementation source | No. | GT-01/GT-07. | source_loading_blocker. | Not by P3.3. |
| Product source | No. | GT-09. | product_source_blocker. | Not input. |
| External source contents | No. | GT-11. | external_source_blocker. | Not input. |
| Generated outputs/raw Graphify outputs | No. | GT-12/GT-15. | generated_output_tracking_blocker. | Not input. |
| Secrets/credentials | No. | Secure incident route. | secret_exposure_blocker. | Never input. |
| Provider auth material | No. | GT-08/S-03. | provider_auth_material_blocker. | Never input. |
| Live connector data | No. | GT-08/GT-15. | live_connector_activation_blocker. | Not input. |
| Datasets/models | No. | GT-01/GT-05. | unknown_sensitivity_blocker. | Not input. |

Only approved governance/metadata docs may be considered for future documentation/metadata check candidates. No raw source, product source, secrets, credentials, provider auth material, live connector data, raw generated outputs, or external source contents are allowed by P3.3.

## 17. Output Surface Requirements
| Output surface type | Current P3.3 decision | Required retention posture | Required rollback posture | Required incident posture | Tracking posture | Blocker |
| --- | --- | --- | --- | --- | --- | --- |
| No output | Preferred for future metadata checks. | `not_applicable` or `metadata_only`. | Not applicable. | Stop route if unexpected output. | `not_applicable`. | none until toolized. |
| Safe metadata report | Future exact candidate only. | `metadata_only`. | Removal/rollback route. | Incident route if sensitive. | `tracking_blocked` unless GT-12. | generated_output_tracking_blocker. |
| Bounded generated report | Deferred. | `generated_sensitive`. | Rollback/removal route. | Generated output incident route. | `tracking_blocked`. | generated_output_tracking_blocker. |
| Generated output retention | Blocked by default. | Future exact review. | Required. | Required. | `tracking_blocked`. | retention_review_blocker. |
| Generated output tracking | Blocked. | Future GT-12/GT-15. | Required. | Required. | `future_gt12_required`. | generated_output_tracking_blocker. |
| Publication | Blocked. | Publication review. | Required. | Required. | `publication_blocked`. | publication_blocker. |
| Source tracking | Blocked. | Exact path review. | Required. | Required. | `tracking_blocked`. | source_tracking_blocker. |

P3.3 does not approve generated output tracking, source tracking expansion, or publication. Any future output must be exact, bounded, retained according to P2.3, and not tracked/published without GT-12.

## 18. Side Effect Profile
| Side effect type | P3.3 posture | Required future gate | Rollback need | Incident need |
| --- | --- | --- | --- | --- |
| No side effect | Only acceptable future candidate posture. | GT-04/GT-05/GT-07 if toolized. | Minimal. | Stop if unexpected. |
| Read-only governance metadata access | Future exact candidate only. | GT-04/GT-05/GT-07. | Not normally needed. | Required if sensitive content appears. |
| Filesystem read | Blocked except future exact governance docs. | GT-01/GT-05/GT-07. | Not normally needed. | Required for boundary breach. |
| Filesystem write | Blocked. | GT-07/GT-12/GT-15. | Required. | Required. |
| Generated output creation | Blocked/deferred. | GT-12/GT-15/GT-07. | Required. | Required. |
| Source tracking | Blocked. | GT-02/GT-12. | Required. | Required. |
| Git mutation | Blocked. | GT-02/GT-12. | Required. | Required. |
| Network transmission | Blocked. | P3.4/GT-08/GT-07. | Required. | Required. |
| Provider/API call | Blocked. | P3.4/GT-08. | Required. | Required. |
| MCP call | Blocked. | P3.4/GT-08/GT-07. | Required. | Required. |
| Product mutation | Blocked. | GT-09. | Required. | Required. |
| Runtime state mutation | Blocked. | GT-06/GT-13/GT-15. | Required. | Required. |
| Persistent state creation | Blocked. | GT-13/GT-15. | Required. | Required. |

The only future candidate posture may be no-side-effect or tightly bounded metadata read/check behavior. Any write, mutation, network, provider, MCP, Git, product, runtime, or persistence side effect remains blocked.

## 19. Retention / Rollback / Incident Posture
| Tool class | Retention posture | Rollback posture | Incident route | Quarantine trigger | Publication blocker | Source tracking blocker |
| --- | --- | --- | --- | --- | --- | --- |
| documentation-only checks | `metadata_only` or no output. | Removal route for unexpected output. | Incident route for sensitive exposure. | Unexpected restricted content. | publication_blocker. | source_tracking_blocker. |
| metadata-only checks | `metadata_only` or no output. | Removal route for unexpected output. | Incident route for sensitive exposure. | Unknown sensitivity. | publication_blocker. | source_tracking_blocker. |
| validation command candidates | `generated_sensitive` unless proven metadata-only. | Required. | Validation output incident route. | Sensitive output. | publication_blocker. | generated_output_tracking_blocker. |
| generated output tools | `generated_sensitive`. | Required. | Generated output incident route. | Raw output creation. | publication_blocker. | generated_output_tracking_blocker. |
| Graphify tools | `generated_sensitive` / local-only. | Required. | Graphify output incident route. | Raw Graphify output. | publication_blocker. | graphify_raw_output_blocker. |
| Git tools | Not applicable until gated. | Required. | Source tracking incident route. | Unapproved mutation. | publication_blocker. | source_tracking_blocker. |
| network/provider tools | Generated/provider-sensitive. | Required. | Provider/network incident route. | Provider payload/auth exposure. | publication_blocker. | provider_auth_blocker. |
| MCP tools | Generated/provider-sensitive. | Required. | MCP incident route. | MCP activation/payload exposure. | publication_blocker. | provider_mcp_blocker. |
| live connector tools | Unknown/live-sensitive. | Required. | Connector incident route. | Raw connector access. | publication_blocker. | live_connector_activation_blocker. |
| product tools | `product_restricted`. | Required. | Product source incident route. | Product source interaction. | publication_blocker. | product_source_blocker. |
| GBrain/Hermes/Cadence tools | `metadata_only` until exact gate. | Required if ever activated. | Cadence incident route. | Runtime/always-on attempt. | publication_blocker. | cadence_activation_blocker. |
| secret/credential risk | `incident_route_required`. | Credential/security route. | Secret/credential incident route. | Any exposure risk. | publication_blocker. | secret_exposure_blocker. |

P3.3 does not implement retention, rollback, quarantine, or incident automation. It only records required posture.

## 20. Human Approval Requirements
| Approval event | Required approver role | Required evidence | Stop rule if absent |
| --- | --- | --- | --- |
| Any future exact tool activation | Human governance approver. | ToolExecutionActivationDecision, gates, refs, exact scope. | Stop; remain deferred. |
| Before command execution | Human governance/security approver. | Exact command/action, cwd, inputs, outputs. | Stop; no execution. |
| Before filesystem writes | Human governance/security approver. | Exact path, rollback, retention. | Stop; no writes. |
| Before generated output creation | Human governance/security approver. | Output path, retention, incident route. | Stop; no output. |
| Before Git mutation | Human governance approver. | Exact paths, tracking posture, GT-12. | Stop; no Git mutation. |
| Before provider/network/MCP | Human governance/security approver. | P3.4 decision, auth/security refs. | Stop; no provider/network/MCP. |
| Before product source access | Human product/governance approver. | GT-09 scope and security refs. | Stop; no product access. |
| Before external source review | Human governance/security approver. | GT-11 scope, license/security refs. | Stop; no external source review. |
| Before Graphify rerun | Human governance/security approver. | Exact Graphify gate, output/retention plan. | Stop; no Graphify. |
| Before persistent state | Human governance/security approver. | GT-13/GT-15, rollback/incident/audit. | Stop; no persistence. |

No future candidate can be implemented or executed without explicit human approval and exact-scope gate review.

## 21. Stop Rules
| Stop condition | Required action | Affected tool class | Incident route |
| --- | --- | --- | --- |
| Secret/credential exposure risk | Stop; do not repeat content. | All tools. | Secret/credential incident route. |
| `.env` or token store interaction | Stop. | Filesystem/provider tools. | Credential incident route. |
| Product source interaction | Stop. | Product/filesystem tools. | Product source incident route. |
| External source content interaction | Stop. | External/Codegraph/GBrain tools. | External source incident route. |
| Live connector access | Stop. | Live connector tools. | Connector incident route. |
| Provider/auth/API/MCP dependency | Stop pending P3.4. | Provider/MCP/network tools. | Provider/auth incident route. |
| Graphify rerun request | Stop. | Graphify tools. | Graphify output incident route. |
| Generated output tracking request | Stop. | Generated-output tools. | Generated output incident route. |
| Source tracking expansion request | Stop. | Git/filesystem tools. | Source tracking incident route. |
| Git mutation request | Stop. | Git tools. | Source tracking incident route. |
| Filesystem write request | Stop. | Filesystem/generated-output tools. | Output mutation incident route. |
| Network request | Stop. | Network/provider tools. | Network/provider incident route. |
| Package/build/test/CI request | Stop. | Package/build/test/CI tools. | Tool execution incident route. |
| Runtime activation request | Stop. | Runtime/Cadence tools. | Runtime incident route. |
| Agent execution request | Stop. | Agent-bound tools. | Agent incident route. |
| GBrain/Hermes/Cadence activation request | Stop. | GBrain/Hermes/Cadence tools. | Cadence incident route. |
| Substrate selection request | Stop. | Semantic/graph tools. | Substrate incident route. |
| Unknown sensitivity | Stop and classify first. | All tools. | Unknown sensitivity incident route. |

## 22. Decision Record
| Field | Value |
| --- | --- |
| `decision_id` | `P3.3-tool-execution-activation-decision` |
| `decision_status` | `tool_execution_activation_deferred` |
| `candidate_tool_scope` | Exact future metadata-only/documentation conformance checks, if all gates and constraints are met. |
| `allowed_future_tool_classes` | Narrow metadata-only/documentation checks as future candidates only. |
| `blocked_tool_classes` | Shell, subprocess, filesystem broad read/write, network, package-manager, build, test, CI, Git, Graphify, Codegraph unless separately reviewed, MCP, live connector, product, generated-output, provider-bound without P3.4, agent-bound without P3.5, GBrain/Hermes/Cadence. |
| `deferred_tool_classes` | Validation command candidates and Codegraph-like candidates pending exact future review. |
| `rejected_tool_classes` | Any broad, generic, unbounded, source-loading, secret-exposing, product-touching, provider/auth, live connector, agent-runtime, or Cadence scope. |
| `required_gates` | GT-04, GT-05, GT-07, plus GT-08/GT-09/GT-11/GT-12/GT-15 as applicable. |
| `required_validation_refs` | P3.1 ValidationRef for exact future proposal. |
| `required_security_refs` | P3.2 SecurityRef for exact future proposal. |
| `required_evidence_refs` | P2.2 EvidenceRef with limitations and source classifications. |
| `source_classification_requirements` | P3.0 source classes must allow only exact governance/metadata docs for candidate checks. |
| `input_surface_requirements` | Exact approved governance/metadata docs only; no raw source, product, external, secret, credential, provider auth, live connector, raw generated output, or runtime state. |
| `output_surface_requirements` | No output preferred; otherwise exact safe metadata report with retention, rollback, incident, and no tracking/publication without GT-12. |
| `side_effect_profile` | No side effect required for any candidate. |
| `filesystem_profile` | No broad reads/writes; exact future metadata-doc reads only if gated. |
| `network_profile` | Network blocked. |
| `provider_dependency_profile` | Provider-bound tools pending P3.4 and blocked by default. |
| `mcp_dependency_profile` | MCP blocked pending P3.4/GT-08/GT-07. |
| `generated_output_profile` | Generated outputs blocked unless exact future output posture and GT-12/GT-15. |
| `product_boundary` | Product/Siamese source and tools blocked until GT-09 and future exact decision. |
| `graphify_boundary` | Graphify commands blocked; Graphify evidence only supporting generated evidence. |
| `gbrain_hermes_cadence_boundary` | GBrain/Hermes/Cadence tools blocked; future inactive candidates only. |
| `retention_posture` | Metadata-only or generated-sensitive as future exact output requires. |
| `rollback_posture` | Required before any future activation. |
| `incident_posture` | Required before any future activation. |
| `audit_posture` | Required before any future activation. |
| `human_approval_required` | true |
| `stop_rules` | All stop rules in section 21 preserved. |
| `limitations` | No execution, no broad activation, no hidden runtime behavior. |
| `review_required` | Future exact gate and human review required. |
| `created_at` | 2026-07-04 |

## 23. P3.4 Interface
P3.4 decides provider/auth/API/MCP activation decision. P3.3 does not decide provider/auth/API/MCP. Provider-bound, network-bound, API-bound, MCP-bound, model-provider-bound, live-connector-bound, telemetry-bearing, cost-bearing, or auth-bearing tools remain blocked or pending P3.4. If P3.4 is absent, use `pending_P3.4_provider_auth_decision_alignment`. If P3.4 later blocks provider/auth/API/MCP, P3.3 candidate scope must exclude those dependencies. P3.3 does not start P3.4.

## 24. P3.5 Interface
P3.5 decides agent runtime activation decision after P3.3 and P3.4. P3.3 provides tool decision input to P3.5. P3.3 does not activate agents. Agent-bound tools remain blocked until P3.5. Agent runtime cannot execute tools merely because P3.3 defines candidate future tool criteria. P3.3 does not start P3.5.

## 25. Future Implementation Eligibility
| Future implementation candidate | Required P3.3 decision state | Required gates | Required inputs | Blocked shortcut |
| --- | --- | --- | --- | --- |
| Metadata-only conformance checker | `candidate_for_future_exact_activation` | GT-04/GT-05/GT-07. | Exact docs, refs, human approval. | Running without exact gate. |
| Documentation section checker | `candidate_for_future_exact_activation` | GT-04/GT-05/GT-07. | Exact section/docs list. | Broad filesystem reads. |
| EvidenceRef schema checker | `candidate_for_future_exact_activation` | GT-04/GT-05/GT-07. | P2.2 refs, exact docs. | Schema enforcement runtime. |
| Blocker propagation checker | `candidate_for_future_exact_activation` | GT-04/GT-05/GT-07. | P2.1/P2.3 blockers. | Bypassing blockers. |
| Validation candidate proposal checker | `activation_deferred` | GT-04/GT-05/GT-07. | P3.1 proposal and safe inputs. | Running validation. |
| Tool allowlist implementation | `eligible_for_later_implementation_ticket` after future exact decision only. | GT-07/GT-05/GT-15. | Exact policy design. | Implementing from P3.3 alone. |
| Tool policy dry-run | `eligible_for_later_implementation_ticket` after future exact decision only. | GT-04/GT-05/GT-07. | Exact dry-run scope. | Executing tools. |
| Tool execution runtime | `activation_blocked` until future exact activation records. | GT-06/GT-07/GT-15 and others as applicable. | Full runtime/security/rollback/audit. | Runtime from candidate status. |

P3.3 may make a future exact metadata-only checker eligible for review, but not execution. Tool execution runtime remains blocked until future explicit gates and decision records approve exact scope.

## 26. Tool Execution Activation Decision Invariants
| ID | Invariant |
| --- | --- |
| TOOLDEC-001 | P3.3 is activation-decision only. |
| TOOLDEC-002 | Decision is not execution. |
| TOOLDEC-003 | Readiness is not activation. |
| TOOLDEC-004 | AGENT PLATFORM remains pre-active at AL-1. |
| TOOLDEC-005 | Tool metadata is not tool execution. |
| TOOLDEC-006 | No broad tool execution is approved. |
| TOOLDEC-007 | Default posture is `tool_execution_activation_deferred`. |
| TOOLDEC-008 | Only exact future metadata-only/documentation checks may be candidate scopes. |
| TOOLDEC-009 | Shell execution remains blocked. |
| TOOLDEC-010 | Subprocess execution remains blocked. |
| TOOLDEC-011 | Broad filesystem reads/writes remain blocked. |
| TOOLDEC-012 | Network calls remain blocked. |
| TOOLDEC-013 | Package-manager/build/test/CI commands remain blocked. |
| TOOLDEC-014 | Git commands remain blocked. |
| TOOLDEC-015 | Graphify commands remain blocked. |
| TOOLDEC-016 | MCP tool calls remain blocked without P3.4 and future gates. |
| TOOLDEC-017 | Live connector tools remain blocked. |
| TOOLDEC-018 | Product tools remain blocked until GT-09 and future exact decision. |
| TOOLDEC-019 | Provider-bound tools remain blocked or pending P3.4. |
| TOOLDEC-020 | Agent-bound tools remain blocked until P3.5 and future runtime gates. |
| TOOLDEC-021 | GBrain/Hermes/Cadence tools remain future and inactive. |
| TOOLDEC-022 | Source classification is not source loading permission. |
| TOOLDEC-023 | Path presence is not content inspection permission. |
| TOOLDEC-024 | Evidence supports; it does not decide. |
| TOOLDEC-025 | Validation evaluates; governance decides. |
| TOOLDEC-026 | Security constrains; it does not activate. |
| TOOLDEC-027 | Generated output tracking, source tracking expansion, and publication remain separately gated. |
| TOOLDEC-028 | Cognitive Semantic System substrate remains deferred. |
| TOOLDEC-029 | Graphify evidence is supporting generated evidence only, not authority. |
| TOOLDEC-030 | P3.3 does not start P3.4, P3.5, P3.BR, P4, or P5. |

## 27. Future Validation Targets
These validation targets are proposed only and are not executed by P3.3.

| Future validation target | Purpose |
| --- | --- |
| ToolExecutionActivationDecision required fields completeness | Check decision object completeness. |
| Tool class decision matrix completeness | Check all tool classes are represented. |
| P3.0 source classification consumption | Check input class constraints. |
| P3.1 validation readiness consumption | Check ValidationRef readiness use. |
| P3.2 security readiness consumption | Check SecurityRef readiness use. |
| P3.R readiness reconciliation consumption | Check P3-A closure use. |
| P2.1 vocabulary conformance | Check canonical terms. |
| P2.2 EvidenceRef boundary conformance | Check evidence boundaries. |
| P2.3 retention/rollback/incident posture conformance | Check safety posture. |
| P1.3 tool boundary conformance | Check tool metadata boundary. |
| S-04 tool/shell/network/MCP policy conformance | Check execution policy boundaries. |
| S-03 no-secret/no-credential conformance | Check secret/credential exclusions. |
| No broad tool execution approval invariant | Check no broad approval exists. |
| Candidate exact scope boundedness invariant | Check candidate scopes are exact. |
| Shell/subprocess blocked invariant | Check shell/subprocess remain blocked. |
| Filesystem broad access blocked invariant | Check broad filesystem access remains blocked. |
| Network/provider/API/MCP blocked invariant | Check provider/network/MCP blocked. |
| Package/build/test/CI blocked invariant | Check commands remain blocked. |
| Git mutation blocked invariant | Check Git remains blocked. |
| Graphify command blocked invariant | Check Graphify command blocked. |
| Product tool blocked invariant | Check product tools blocked. |
| Live connector tool blocked invariant | Check connector tools blocked. |
| GBrain/Hermes/Cadence inactive invariant | Check future inactive posture. |
| Generated output tracking blocked invariant | Check output tracking blocked. |
| Source tracking expansion blocked invariant | Check source tracking blocked. |
| Publication blocked invariant | Check publication blocked. |
| Cognitive Semantic System substrate-deferred invariant | Check substrate deferred. |
| Human approval required invariant | Check human approval required. |
| P3.4 dependency marking for provider-bound tools | Check pending alignment. |
| P3.5 dependency marking for agent-bound tools | Check agent-bound blockers. |

## 28. Future Hardening Candidates
These future tickets are not started by P3.3.

| Candidate ticket | Purpose | P3.3 status |
| --- | --- | --- |
| TOOLDEC-HARD-01 - Exact Metadata-Only Tool Candidate Schema | Define schema for future metadata-only candidates. | Not started. |
| TOOLDEC-HARD-02 - Tool Input Surface Eligibility Matrix | Refine input eligibility. | Not started. |
| TOOLDEC-HARD-03 - Tool Output Surface Retention Matrix | Refine output/retention rules. | Not started. |
| TOOLDEC-HARD-04 - Tool Side-Effect Classification Matrix | Refine side-effect classes. | Not started. |
| TOOLDEC-HARD-05 - Tool Human Approval Checklist | Define human approval checks. | Not started. |
| TOOLDEC-HARD-06 - Tool Stop Rule Checklist | Define stop-rule checks. | Not started. |
| TOOLDEC-HARD-07 - Tool Dry-Run Policy Candidate | Future dry-run policy candidate. | Not started. |
| TOOLDEC-HARD-08 - Tool Allowlist Candidate Design | Future allowlist candidate. | Not started. |
| TOOLDEC-HARD-09 - Documentation Conformance Checker Candidate | Future checker candidate. | Not started. |
| TOOLDEC-HARD-10 - EvidenceRef Schema Checker Candidate | Future EvidenceRef checker candidate. | Not started. |
| TOOLDEC-HARD-11 - Blocker Propagation Checker Candidate | Future blocker checker candidate. | Not started. |
| TOOLDEC-HARD-12 - P3.5 Tool Dependency Handoff Review | Future P3.5 handoff review. | Not started. |

## 29. Created / Not Created Register
| Artifact or action | P3.3 status |
| --- | --- |
| `0_architecture/governance/agent_platform_tool_execution_activation_decision.md` | Created. |
| Tool Execution Activation Decision document | Created. |
| ToolExecutionActivationDecision record | Created. |
| P3.R document | Not modified. |
| P3.0 document | Not modified. |
| P3.1 document | Not modified. |
| P3.2 document | Not modified. |
| P2.KR document | Not modified. |
| P2.R document | Not modified. |
| P2.1 document | Not modified. |
| P2.2 document | Not modified. |
| P2.3 document | Not modified. |
| P1.3 document | Not modified. |
| P1 documents | Not modified. |
| P0 documents | Not modified. |
| S-03/S-04 documents | Not modified. |
| Runtime code | Not modified. |
| Tool execution implementation | Not modified. |
| Source loading | Not implemented. |
| Source content | Not loaded. |
| Source inspection | Not performed. |
| Product source | Not inspected. |
| Hermes source | Not inspected. |
| GBrain source | Not inspected. |
| Graphify implementation source | Not inspected. |
| External source contents | Not inspected. |
| Existing `3_platform` sibling contents | Not inspected. |
| `3_platform/_governed_skeleton` live source files | Not inspected. |
| Generated output contents | Not inspected. |
| Datasets/models contents | Not inspected. |
| Secrets | Not inspected. |
| Credentials | Not inspected. |
| `.env` | Not inspected. |
| Provider configs | Not inspected. |
| Token stores | Not inspected. |
| Browser auth | Not inspected. |
| Local credential stores | Not inspected. |
| API keys | Not inspected. |
| Security enforcement | Not implemented. |
| Validation command | Not executed. |
| Tests | Not executed. |
| CI | Not executed. |
| Scripts | Not executed. |
| Shell commands | Not approved or executed. |
| Subprocess execution | Not approved or executed. |
| Filesystem broad reads/writes | Not approved or executed. |
| Network calls | Not approved or executed. |
| Package-manager commands | Not approved or executed. |
| Build commands | Not approved or executed. |
| Test commands | Not approved or executed. |
| CI commands | Not approved or executed. |
| Git commands | Not approved or executed. |
| Provider/auth/API/MCP | Not configured or activated. |
| Live connectors | Not activated. |
| MCP tools/resources/servers | Not activated. |
| Tool execution | Not approved broadly. |
| Agent execution | Not approved. |
| Agent runtime | Not launched. |
| Scheduler/orchestration/autonomous loops | Not activated. |
| Vector DB | Not implemented. |
| Embeddings | Not generated. |
| Semantic search | Not implemented. |
| Graph DB | Not implemented. |
| Ontology runtime | Not implemented. |
| Relationship persistence | Not implemented. |
| GBrain | Not implemented. |
| GBrain adoption | Not adopted. |
| GBrain execution | Not executed. |
| GBrain dependency approval | Not dependency-approved. |
| Hermes | Not activated. |
| Cadence | Not activated. |
| Always-on behavior | Not activated. |
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
| Graph substrate | Not selected. |
| Vector search substrate | Not selected. |
| P3.4 | Not started. |
| P3.5 | Not started. |
| P3.BR | Not started. |
| P4 | Not started. |
| P5 | Not started. |
| Git staging/commit/push/force-add/publication | Not authorized or performed. |

## 30. Recommended Next Tickets
After P3.3, the recommended queue is:

| Ticket | Recommendation |
| --- | --- |
| P3.4 - Provider/Auth/API/MCP Activation Decision | Recommended actual next ticket after explicit instruction. |
| P3.5 - Agent Runtime Activation Decision | Only after P3.3 and P3.4 are complete or with pending alignment markers. |
| P3.BR - Activation Decision Reconciliation Closure | Only after P3.3-P3.5 are complete. |
| P4 - Siamese Product Integration Readiness | Only if P3.BR recommends product-readiness sequencing. |
| P5 - Controlled Runtime Implementation | Only if P3.BR declares exact implementation eligibility. |

Recommended actual: P3.4 - Provider/Auth/API/MCP Activation Decision.

Do not start P3.4. Do not start P3.5. Do not start P3.BR. Do not start P4. Do not start P5.

## 31. Final Verdict
| Question | Answer |
| --- | --- |
| What did P3.3 create? | The Tool Execution Activation Decision document. |
| What ToolExecutionActivationDecision was created? | `P3.3-tool-execution-activation-decision`. |
| What is the default decision posture? | `tool_execution_activation_deferred`. |
| Which tool classes were considered? | Documentation-only checks, metadata-only checks, validation command candidates, shell/subprocess/filesystem/network/package/build/test/CI/Git/Graphify/Codegraph/MCP/live connector/product/generated-output/provider-bound/agent-bound/GBrain/Hermes/Cadence tools. |
| Which tool classes are blocked? | Shell, subprocess, broad filesystem, network, package-manager, build, test, CI, Git, Graphify, MCP, live connector, product, generated-output, provider-bound without P3.4, agent-bound without P3.5, GBrain/Hermes/Cadence tools. |
| Which tool classes are deferred? | Validation command candidates and Codegraph-like tools pending exact future review. |
| Which tool classes, if any, are candidate_for_future_exact_activation? | Narrow metadata-only/documentation conformance checks only, as future exact candidates. |
| What exact future candidate scope was defined? | Metadata-only validation/check tooling over exact approved governance/metadata docs with no side effects and all gates preserved. |
| What gates are required before any future tool activation? | GT-04, GT-05, GT-07, plus GT-08/GT-09/GT-11/GT-12/GT-15 and others as applicable. |
| What validation refs are required? | P3.1 ValidationRef for any future exact proposal. |
| What security refs are required? | P3.2 SecurityRef for any future exact proposal. |
| What source classification requirements were defined? | P3.0 source classifications must allow only exact governance/metadata docs for candidate checks. |
| What input surface requirements were defined? | Exact approved governance/metadata docs only; no raw source, product source, external contents, secrets, credentials, provider auth material, live connector data, raw generated outputs, or runtime state. |
| What output surface requirements were defined? | No output preferred; exact safe metadata report only if future retention, rollback, incident, and tracking constraints are approved. |
| What side-effect profile was defined? | No-side-effect or tightly bounded metadata read/check behavior only for future candidate scope. |
| What retention, rollback, and incident posture was defined? | Metadata-only retention preferred; rollback and incident routes required for any future output or side effect. |
| What human approval requirements were defined? | Explicit human approval and exact-scope gate review required before any future implementation or execution. |
| What stop rules were defined? | Stop on secret/credential, `.env`, product, external source, live connector, provider/API/MCP, Graphify rerun, generated output tracking, source tracking, Git, filesystem write, network, package/build/test/CI, runtime, agent, GBrain/Hermes/Cadence, substrate, or unknown sensitivity request. |
| How does P3.3 interface with P3.4? | Provider/auth/API/MCP-bound tools remain blocked or carry `pending_P3.4_provider_auth_decision_alignment`; P3.3 does not start P3.4. |
| How does P3.3 interface with P3.5? | Agent-bound tools remain blocked until P3.5; P3.3 does not activate agents or start P3.5. |
| Did P3.3 approve broad tool execution? | No. |
| Did P3.3 execute tools? | No. |
| Did P3.3 run shell/subprocess/filesystem/network/package/build/test/CI/Git commands? | No. |
| Did P3.3 run validation or tests? | No. |
| Did P3.3 implement security enforcement? | No. |
| Did P3.3 load or inspect source? | No. |
| Did P3.3 inspect product source? | No. |
| Did P3.3 inspect secrets, credentials, or `.env`? | No. |
| Did P3.3 configure provider/auth/API/MCP? | No. |
| Did P3.3 activate live connectors? | No. |
| Did P3.3 activate agents? | No. |
| Did P3.3 activate GBrain, Hermes, or Cadence? | No. |
| Did P3.3 rerun or adopt Graphify? | No. |
| Did P3.3 approve generated output tracking, source tracking expansion, or publication? | No. |
| Did P3.3 select Cognitive Semantic System substrate? | No. Cognitive Semantic System substrate remains deferred. |
| What is the next recommended ticket? | P3.4 - Provider/Auth/API/MCP Activation Decision, after explicit instruction only. |

Stop rule: After completing P3.3, STOP. Do not start P3.4. Do not start P3.5. Do not start P3.BR. Do not start P4. Do not start P5. Do not implement code. Do not implement tool execution. Do not execute tools. Do not execute shell commands. Do not execute subprocesses. Do not approve broad filesystem reads. Do not approve filesystem writes. Do not call network. Do not run package-manager commands. Do not run build commands. Do not run test commands. Do not run CI commands. Do not run Git commands. Do not run Graphify. Do not run `/graphify`. Do not run Codegraph. Do not activate MCP tools/resources/servers. Do not activate live connector tools. Do not activate product tools. Do not activate generated-output tools. Do not run validation. Do not run tests. Do not run scripts. Do not run scanners. Do not inspect secrets. Do not inspect credentials. Do not inspect `.env`. Do not inspect provider configs. Do not inspect token stores. Do not inspect browser auth. Do not inspect local credential stores. Do not inspect API keys. Do not implement security enforcement. Do not configure provider/auth. Do not call APIs. Do not activate MCP. Do not execute agents. Do not launch agent runtime. Do not activate scheduler/orchestration/autonomous loops. Do not activate runtime behavior. Do not activate live connectors. Do not implement source loading. Do not load source. Do not inspect source contents. Do not inspect product source. Do not inspect Hermes source. Do not inspect GBrain source. Do not inspect Graphify implementation source. Do not inspect existing `3_platform` sibling contents. Do not read live source files under `3_platform/_governed_skeleton/`. Do not inspect external source contents. Do not inspect generated output contents. Do not inspect datasets/models contents. Do not implement vector DB. Do not generate embeddings. Do not implement semantic search. Do not implement graph DB. Do not implement ontology runtime. Do not implement relationship persistence. Do not implement GBrain. Do not adopt GBrain. Do not dependency-approve GBrain. Do not activate Hermes. Do not activate Cadence. Do not activate always-on behavior. Do not modify generated outputs. Do not approve generated output tracking. Do not approve source tracking expansion. Do not modify `.gitignore`. Do not modify `.graphifyignore`. Do not select Cognitive Semantic System substrate. Do not select graph as substrate. Do not select vector search as substrate. Do not adopt Graphify as authority. Do not treat Graphify as truth engine. Do not stage, commit, push, force-add, or publish.
