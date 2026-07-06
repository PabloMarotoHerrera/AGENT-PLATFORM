# MVP Interaction Surface Architecture

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | MVP Interaction Surface Architecture |
| Ticket | P8.2 |
| Status | Accepted MVP interaction surface architecture |
| Date | 2026-07-06 |
| Scope | Documentation / architecture design only for the MVP-0 local interaction surface of AGENT PLATFORM / Siamese. |
| Authority | Interaction surface architecture only, not CLI/TUI/web implementation, not Hermes UI activation, not Hermes runtime activation, not adapter implementation, not provider/auth/API/MCP activation, not credential use, not API calls, not MCP calls, not tool execution, not agent execution, not live connector activation, not Graphify execution/rerun/adoption, not GBrain/GStack/Hermes/OpenCode execution, not product/Siamese source inspection, not source loading, not persistence, not vector DB implementation, not embedding generation, not graph DB implementation, not generated output tracking, not source tracking expansion, not publication, not Git mutation, and not Cognitive Semantic System substrate selection. |
| Related documents | P8.0, P8.1 if present, P8.3 if present, P8.4 if present, P8.5 if present, P7.R, P7.0.A-P7.0.G, P6.7, P6.1-P6.6, P5.R, P3.BR, P2.KR, P2.2, P2.3, S-03, S-04, README.md, `.gitignore`, `.graphifyignore`. |
| Output | MVP interaction surface architecture. |
| Output posture | `mvp_interaction_surface_architecture_ready`; `mvp0_interaction_surface_decision_recorded`; `local_manual_interaction_loop_defined`; `no_runtime_activation`. |

## 2. Purpose

P8 transforms the validated P7 manual workflow into a local interactive MVP path.

P8.2 defines how the user interacts with AGENT PLATFORM in MVP-0. It evaluates local CLI, local TUI, local web, Hermes-provided interface candidate, Hermes-like interface inspiration, and hybrid markdown-first interface options.

P8.2 decides the MVP-0 interaction surface posture and defines required user-facing surfaces for objective intake, WorkPacket generation, HarnessInputPackage generation, HarnessOutputPackage intake, review checklist rendering, integrator checklist rendering, and CommitCandidate rendering.

P8.2 preserves user manual control over external harnesses and Git. P8.2 does not implement the interface. P8.2 does not activate Hermes, OpenCode, adapters, runtime, providers, tools, agents, or product behavior. P8.2 does not start P8.6-P8.9, P8.10, or implementation tickets.

## 3. Current Posture

P8.0 defines MVP scope and external integration boundary. P8.2 consumes P8.0.

MVP-0 is local, interactive, and manual. MVP-0 is not autonomous runtime. MVP-0 is not product generator. MVP-0 does not dispatch work automatically. MVP-0 does not assign reviewers automatically. MVP-0 does not integrate automatically. MVP-0 does not mutate Git.

MVP-0 does not execute OpenCode. MVP-0 does not execute Graphify. MVP-0 does not activate GBrain, GStack, Hermes, providers, MCP, tools, agents, live connectors, vector DB, graph DB, or persistence.

Product/Siamese source remains deferred. User remains final execution and Git authority.

## 4. Inputs Reviewed

Inputs are consumed as governance/architecture metadata only. P8.2 does not inspect external candidate source contents, product source, raw generated outputs, secrets, credentials, configs, token stores, browser auth, local credential stores, API keys, or runtime state.

| Input | Present | Consumed_as | Interaction_surface_relevance | Limitations | Pending_alignment |
| --- | --- | --- | --- | --- | --- |
| P8.0 Platform MVP Scope / External Integration Boundary | Yes | Required boundary posture | Defines MVP-0, P8 boundaries, candidate classes, Git/user authority, and no-runtime posture. | No P8.0 modification. | none |
| P8.1 External Source Inventory / Classification if present | Yes | Optional peer metadata | Aligns external candidate labels for Graphify, GBrain, GStack, Hermes, and OpenCode. | Path/class metadata only. | none |
| P8.3 Core Workflow Schema Candidates if present | No | Optional peer metadata | Would align WorkPacket, HarnessInputPackage, HarnessOutputPackage, ReviewVerdictPackage, IntegrationSummary, and CommitCandidate schemas. | P8.2 defines field candidates only, not schemas. | `pending_P8.3_schema_candidates_alignment` |
| P8.4 Local Workspace / State Model if present | Yes | Optional peer metadata | Aligns InteractionSession and local-only state posture. | No state files created. | none |
| P8.5 Security / Activation Gate Model if present | Yes | Optional peer metadata | Aligns blocked actions, P8-L0/P8-L2 posture, and GitMutationBoundary. | Gate model is not enforcement. | none |
| P7.R Manual Agentic Workflow Planning Closure | Yes | Manual workflow closure | Confirms manual workflow baseline and repeated-use posture. | No runtime readiness implied. | none |
| P7.0.A Manual Lead Agent / User Gateway Contract | Yes | User gateway metadata | Supplies user objective and manual authority posture. | Lead/user gateway is not runtime orchestration. | none |
| P7.0.B Roadmap Generation / Work Breakdown Contract | Yes | Work breakdown metadata | Supplies roadmap, task graph, and WorkPacket projection. | Roadmap is not execution. | none |
| P7.0.C Parallel Agent Lane / Work Packet Taxonomy | Yes | Manual lane metadata | Supplies manual lane and work packet structure. | Manual lane is not agent runtime. | none |
| P7.0.D Manual Context / Memory Manifest Strategy | Yes | Context/memory metadata | Supplies context, memory, evidence refs, and freshness posture. | No live retrieval or persistent memory. | none |
| P7.0.E Manual Harness Strategy / OpenCode-Hermes Boundary | Yes | Harness boundary metadata | Supplies H0/H1/H2/H3 harness level model and OpenCode/Hermes boundary. | No harness execution. | none |
| P7.0.F Reviewer Mesh / Immune Safeguards | Yes | Review boundary metadata | Supplies review checklist and immune safeguard concepts. | No automatic reviewer assignment. | none |
| P7.0.G Integrator / Reconciliation / Commit Advisory Protocol | Yes | Integration and Git advisory metadata | Supplies accepted/rejected output, drift, exact-path Git advice, and manual Git authority. | No Git mutation. | none |
| P6.7 Operational Readiness Audit | Yes | Operational posture | Preserves no-runtime readiness posture. | No operational activation. | none |
| P6.4 Human Approval / Review Loop | Yes | Approval metadata | Aligns human decision points and approval boundaries. | ApprovalRef is not approval. | none |
| P6.6 Cognitive Semantic System Substrate Decision / Defer Record | Yes | CSS substrate posture | Preserves Cognitive Semantic System substrate deferral. | No substrate selection. | none |
| P5.R Minimal Active Agent Platform Audit | Yes | Skeleton baseline | Preserves non-activation of skeleton records. | No implementation activation. | none |
| P3.BR Activation Decision Reconciliation Closure | Yes | Activation decision posture | Preserves provider/tool/agent runtime blockers. | Decision is not execution. | none |
| P2.2 EvidenceRef Contract | Yes | Evidence metadata | Aligns EvidenceRef semantics. | Evidence supports; it does not decide. | none |
| P2.3 Audit / Retention / Rollback Baseline | Yes | Lifecycle metadata | Aligns retention, rollback, generated output, source tracking blockers. | No automation or persistence. | none |
| S-03 Local-only / Secrets / Credentials Policy | Yes | Security metadata | Preserves local-only, secrets, credentials, generated-output, and provider-auth boundaries. | No secrets or credentials inspected. | none |
| S-04 Tool / Shell / Network / MCP Execution Policy | Yes | Execution policy metadata | Preserves no tool/shell/network/MCP execution defaults. | No execution run. | none |
| README.md | Yes | Workspace orientation metadata | Confirms repository orientation only. | No runtime effect. | none |
| `.gitignore` | Yes | Boundary metadata | Confirms ignored/local-only posture by presence only. | Not modified. | none |
| `.graphifyignore` | Yes | Graphify boundary metadata | Confirms Graphify boundary by presence only. | Not modified; not permission to run Graphify. | none |

## 5. Interaction Surface Decision Model

`MVPInteractionSurface` is the canonical architecture object for the MVP-0 interaction surface.

| Field | Meaning |
| --- | --- |
| `interaction_surface_id` | Stable surface identifier. |
| `interaction_surface_name` | Human-readable surface name. |
| `interaction_mode` | `InteractionMode` value. |
| `decision_status` | Architecture decision status. |
| `intended_user` | Expected user/operator. |
| `local_only_posture` | Local-only and no-network posture. |
| `manual_control_posture` | Human control and manual execution posture. |
| `supported_user_actions` | Actions the surface may help the user perform manually. |
| `blocked_user_actions` | Actions the surface must block or warn on. |
| `required_surfaces` | Required MVP-0 sub-surfaces. |
| `optional_surfaces` | Optional future sub-surfaces. |
| `schema_dependencies` | P8.3 schema alignment dependencies. |
| `state_dependencies` | P8.4 state alignment dependencies. |
| `security_gate_dependencies` | P8.5 gate alignment dependencies. |
| `external_candidate_dependencies` | P8.1 and P8.6-P8.9 external candidate dependencies. |
| `harness_dependencies` | P7.0.E and P8.9 harness dependencies. |
| `review_dependencies` | Reviewer mesh and checklist dependencies. |
| `integration_dependencies` | Integration checklist and drift dependencies. |
| `commit_advice_dependencies` | CommitCandidate and exact-path Git advice dependencies. |
| `retention_posture` | Future retention posture only. |
| `rollback_posture` | Future rollback posture only. |
| `incident_posture` | Future incident posture only. |
| `evidence_refs` | EvidenceRef-compatible governance refs. |
| `validation_refs` | ValidationRef-compatible future refs. |
| `security_refs` | SecurityRef-compatible policy refs. |
| `limitations` | Known limitations and non-goals. |
| `pending_alignment_refs` | Pending peer alignment refs. |

`decision_status` values:

| decision_status | Meaning |
| --- | --- |
| `selected_for_mvp0_architecture` | Selected architecture posture for MVP-0. |
| `candidate_for_mvp0` | Viable candidate, not selected as baseline. |
| `deferred_to_later_mvp` | Deferred until later gates or maturity. |
| `blocked_for_mvp0` | Blocked for MVP-0. |
| `rejected_for_scope` | Rejected because it exceeds scope. |
| `pending_alignment` | Waiting for P8 peer or upstream alignment. |
| `unknown` | Not enough evidence to classify. |

`MVPInteractionSurface` is an architecture record. It is not implementation and not runtime activation.

## 6. InteractionMode Vocabulary

| InteractionMode | Meaning | Boundary |
| --- | --- | --- |
| `local_cli_candidate` | Future local CLI candidate. | CLI candidate is not command execution. |
| `local_tui_candidate` | Future local TUI candidate. | TUI candidate is not implementation. |
| `local_web_candidate` | Future local web candidate. | Local web candidate is not network exposure. |
| `hermes_provided_interface_candidate` | Future Hermes-provided interface candidate. | Hermes-provided interface candidate is not Hermes activation. |
| `hermes_like_interface_inspiration` | UX inspiration from Hermes-like patterns. | Inspiration is not import, configuration, or runtime. |
| `hybrid_markdown_first_interface` | Markdown-first artifacts with later local interactive helper. | Markdown-first interface is not persistent memory. |
| `markdown_only_manual_interface` | Manual markdown-only fallback. | Fallback is less interactive but safe. |
| `future_desktop_ui_candidate` | Future local desktop UI candidate. | Deferred; not MVP-0 baseline. |
| `future_hosted_ui_candidate` | Future hosted UI candidate. | Blocked for MVP-0 due network/product/security scope. |
| `blocked_runtime_interface` | Runtime or autonomous interface class. | Blocked. |
| `unknown_interaction_mode` | Unclassified mode. | Requires future review. |

`InteractionMode` is not implementation. `InteractionMode` is not interface activation.

## 7. Interaction Option Evaluation Matrix

| Option | Description | Strengths | Weaknesses | MVP-0 fit | Implementation_complexity | Safety_posture | Blocked_interpretations | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CLI local | Local command-line candidate for guided prompts and rendering. | Simple, local, exact-path friendly, scriptable later. | Less visual; can be confused with command execution. | Strong candidate after P8.10/P8.11. | Low to medium. | Safe if non-executing and no shell delegation. | Command execution, provider calls, Git mutation. | `candidate_for_mvp0` |
| TUI local | Local terminal UI candidate for structured steps. | Better navigation than CLI, still local. | More implementation complexity than CLI. | Future UX improvement. | Medium. | Safe if non-executing and local-only. | Runtime UI, background workers, execution. | `deferred_to_later_mvp` |
| web local | Local browser UI candidate. | Familiar UX and forms. | Security/state/network confusion; hosting boundary needs care. | Deferred until boundaries are clearer. | Medium to high. | Requires strict local-only and no-network gate. | Hosted UI, live connectors, provider/API calls. | `deferred_to_later_mvp` |
| Hermes-provided interface candidate | Future interface supplied or inspired by Hermes candidate. | Could align with longer-term interface/runtime vision. | Hermes runtime/Cadence risks and external dependency uncertainty. | Candidate only until P8.8 and future gates. | Unknown. | Candidate-only. | Hermes activation, Hermes source inspection, Cadence. | `deferred_to_later_mvp` |
| Hermes-like interface inspiration | UX patterns inspired by Hermes-like workflows without using Hermes. | Can improve workflow clarity without dependency. | Must avoid implying Hermes adoption. | Useful as design inspiration only. | Low for design, unknown for implementation. | Safe as design reference only. | Hermes import/configuration/runtime. | `candidate_for_mvp0` |
| hybrid markdown-first interface | Markdown-first artifacts plus future local interactive helper. | Preserves current manual workflow, traceability, exact-path review, and low activation risk. | Less polished than full UI. | Best MVP-0 architecture baseline. | Low initially; can evolve. | Strongest safety posture. | Persistent memory, source loading, runtime automation. | `selected_for_mvp0_architecture` |
| markdown-only manual interface | Plain markdown templates and manual steps only. | Safest and already familiar. | Less interactive; more copy/paste overhead remains. | Good fallback. | Low. | Very safe. | Claiming it is the full MVP interaction layer. | `candidate_for_mvp0` |

## 8. MVP-0 Recommended Interaction Surface

MVP-0 should use a hybrid markdown-first local interaction architecture, with a later implementation candidate likely to start as local CLI or simple local TUI, depending on P8.10/P8.11.

MVP-0 interaction surface is local, manual, file/artifact traceable, exact-path oriented, harness-agnostic, non-autonomous, non-executing, non-provider-bound, non-product-bound, and Git-manual.

This recommendation does not implement CLI/TUI/web. It only selects architecture posture.

Decision record:

```text
MVPInteractionSurface:
  interaction_surface_id: mvp0_interaction_surface
  interaction_surface_name: MVP-0 local manual interaction surface
  interaction_mode: hybrid_markdown_first_interface
  decision_status: selected_for_mvp0_architecture
  local_only_posture: local_manual_non_executing
  manual_control_posture: user_final_execution_and_git_authority
  output_markers:
    - mvp_interaction_surface_architecture_ready
    - mvp0_interaction_surface_decision_recorded
    - local_manual_interaction_loop_defined
    - no_runtime_activation
```

## 9. Required MVP-0 Surfaces

| Surface | Purpose | Input objects | Output objects | Required boundaries | Later implementation dependency |
| --- | --- | --- | --- | --- | --- |
| `UserObjectiveInputSurface` | Capture user objective and constraints. | User text, boundary prompts, EvidenceRef metadata. | `UserObjectiveInput`. | No execution, no source loading, no product source, no Git permission. | P8.10/P8.11. |
| `WorkPacketBuilderSurface` | Guide WorkPacket generator output. | `UserObjectiveInput`, roadmap refs, scope refs. | `WorkPacket`. | WorkPacket generation is not dispatch. | P8.3 schema alignment and P8.13 if authorized. |
| `HarnessInputPackageBuilderSurface` | Generate H0 harness package. | `WorkPacket`, context refs, stop rules. | `HarnessInputPackage`. | User manually copies package; no OpenCode execution. | P8.3/P8.9/P8.13 if authorized. |
| `HarnessOutputIntakeSurface` | Accept manual pasted harness output. | User-pasted output, claimed files, claimed commands. | `HarnessOutputPackage`. | Intake is not trust or acceptance. | P8.3/P8.14 if authorized. |
| `ReviewChecklistSurface` | Render review checklist. | Harness output, reviewer mesh refs, security refs. | Review checklist and future `ReviewVerdictPackage`. | No auto-review or reviewer assignment. | P8.14 if authorized. |
| `IntegrationChecklistSurface` | Render integrator checklist. | Review verdicts, accepted/rejected refs, drift refs. | Integration checklist and future `IntegrationSummary`. | No automatic integration. | P8.15 if authorized. |
| `CommitCandidateSurface` | Render exact-path commit candidate advice. | Integration summary, created/modified paths, blockers. | `CommitCandidate`. | Advice only; no Git mutation. | P8.15 if authorized. |
| `CommitCommandBlockRenderer` | Render exact-path Git command text. | `CommitCandidate`. | `CommitCommandBlock`. | Exact paths only; Never recommend git add . | P8.15 if authorized. |
| `SessionSummarySurface` | Summarize session decisions and limits. | Interaction session records. | Session summary. | Metadata only; no persistence implementation. | P8.4/P8.10/P8.11. |
| `DriftRegisterSurface` | Capture drift and blockers. | Review/integration markers. | DriftRegister. | No automatic remediation. | P8.3/P8.4/P8.15. |
| `AcceptedRejectedOutputRegisterSurface` | Record accepted and rejected outputs. | Review verdicts, integration decisions. | AcceptedOutputRegister, RejectedOutputRegister. | Explicit human acceptance required. | P8.3/P8.15. |
| `AuditMetadataSurface` | Capture refs for audit posture. | EvidenceRef, ValidationRef, SecurityRef, ApprovalRef, RetentionRef, RollbackRef, IncidentRef. | Audit metadata. | No audit log implementation. | P8.4/P8.5/P8.10/P8.11. |

## 10. UserObjectiveInputSurface Contract

Required fields:

| Field | Meaning |
| --- | --- |
| `objective_title` | Short objective label. |
| `objective_description` | User objective details. |
| `requested_outcome` | Desired deliverable or decision. |
| `scope_boundary` | Allowed scope. |
| `non_goals` | Explicit non-goals. |
| `target_artifact_type` | Document, schema candidate, checklist, package, or other architecture artifact type. |
| `expected_harness` | H0 external harness expected, if any. |
| `product_related` | Whether the request touches Siamese product vision or product-bound surfaces. |
| `external_source_related` | Whether external candidate surfaces are involved. |
| `security_sensitive` | Whether security-sensitive surfaces are implicated. |
| `source_loading_requested` | Whether user requested source loading. |
| `git_action_requested` | Whether user requested Git action. |
| `human_decision_points` | Required human choices. |
| `evidence_refs` | EvidenceRef-compatible refs. |
| `limitations` | Known limits and blocked assumptions. |

Rules:

- User objective input is not execution approval.
- User objective input is not source loading permission.
- User objective input is not product source permission.
- User objective input is not provider/auth permission.
- User objective input is not Git permission.
- Sensitive or blocked surfaces must trigger warning / blocked posture in future implementation.

## 11. WorkPacketBuilderSurface Contract

Required fields:

| Field | Meaning |
| --- | --- |
| `user_objective_ref` | Ref to `UserObjectiveInput`. |
| `roadmap_ref` | Roadmap or work breakdown ref if applicable. |
| `work_packet_title` | Work packet title. |
| `work_packet_objective` | Work packet objective. |
| `target_document_or_artifact` | Target output path or artifact label. |
| `allowed_scope` | Explicit allowed work. |
| `blocked_scope` | Explicit blocked work. |
| `mandatory_inputs` | Required input docs or refs. |
| `optional_inputs` | Optional input docs or refs. |
| `stop_rules` | Stop conditions. |
| `acceptance_criteria` | Required success criteria. |
| `output_format` | Expected response/document format. |
| `required_reviewers` | Manual reviewer expectations. |
| `integration_requirements` | Manual integration expectations. |
| `commit_advice_requirements` | Exact-path commit advice requirements. |
| `evidence_refs` | EvidenceRef-compatible refs. |
| `validation_refs` | ValidationRef-compatible refs. |
| `security_refs` | SecurityRef-compatible refs. |
| `limitations` | Known limits. |

Rules:

- WorkPacket generator output is not dispatch.
- WorkPacket generation is not dispatch.
- WorkPacket readiness is not execution.
- WorkPacket assignment is manual.
- User manually copies/runs ticket in external harness.

## 12. HarnessInputPackageBuilderSurface Contract

Required fields:

| Field | Meaning |
| --- | --- |
| `harness_input_package_id` | Stable package id. |
| `target_harness` | Target H0 harness name. |
| `harness_level` | H0/H1/H2/H3 classification. |
| `work_packet_ref` | Ref to WorkPacket. |
| `prompt_body` | User-copyable prompt body. |
| `mandatory_context_refs` | Required context refs. |
| `forbidden_context_refs` | Forbidden context refs. |
| `allowed_paths` | Exact allowed paths when applicable. |
| `blocked_paths` | Blocked paths and surfaces. |
| `expected_outputs` | Expected harness outputs. |
| `stop_rules` | Stop conditions for external harness operator. |
| `reporting_format` | Required harness output format. |
| `no_runtime_activation_statement` | Explicit no-runtime statement. |
| `no_git_mutation_statement` | Explicit no-Git-mutation statement. |
| `limitations` | Known limits. |

Harness levels:

| Harness level | Meaning | MVP-0 posture |
| --- | --- | --- |
| `H0_user_operated_harness` | User manually operates external harness. | Allowed for package generation and manual copy/paste. |
| `H1_metadata_adapter_design` | Metadata-only adapter design. | Design posture only. |
| `H2_controlled_execution_adapter_blocked` | Controlled execution adapter. | Blocked. |
| `H3_autonomous_orchestration_adapter_blocked` | Autonomous orchestration adapter. | Blocked. |

Rules:

- MVP-0 may generate H0 HarnessInputPackage.
- MVP-0 may design H1 metadata posture.
- MVP-0 must not execute H2/H3.
- MVP-0 must not run OpenCode.
- MVP-0 must not activate Hermes.
- MVP-0 must not call MCP/provider/API.

## 13. HarnessOutputIntakeSurface Contract

Required fields:

| Field | Meaning |
| --- | --- |
| `harness_output_package_id` | Stable output package id. |
| `source_harness` | Harness named by user. |
| `pasted_output` | User-provided pasted output. |
| `output_summary` | Safe summary. |
| `claimed_files_created` | Files claimed created. |
| `claimed_files_modified` | Files claimed modified. |
| `claimed_commands_run` | Commands claimed by harness. |
| `claimed_tests_run` | Tests claimed by harness. |
| `claimed_decisions` | Decisions claimed by harness. |
| `claimed_limitations` | Limitations claimed by harness. |
| `claimed_next_ticket` | Claimed next ticket. |
| `declared_not_created_register` | Register of non-actions claimed. |
| `unsafe_content_flag` | Unsafe content marker. |
| `product_boundary_flag` | Product boundary marker. |
| `source_loading_flag` | Source loading marker. |
| `credential_secret_flag` | Secret/credential marker. |
| `generated_output_flag` | Generated output marker. |
| `review_required` | Review required flag. |
| `limitations` | Known limits. |

Rules:

- HarnessOutput intake is manual paste/intake.
- HarnessOutputPackage intake is not trust.
- Intake is not acceptance.
- Claimed commands are not assumed true without review.
- Unsafe content must be safely summarized and not repeated.
- Secrets/credentials must not be retained.
- Product/source boundary violations must trigger blocked review posture.
- MVP-0 must not auto-apply harness output.

## 14. ReviewChecklistSurface Contract

Required fields:

| Field | Meaning |
| --- | --- |
| `review_checklist_id` | Stable checklist id. |
| `review_input_package_ref` | Ref to harness output or review package. |
| `reviewer_mesh_refs` | Reviewer mesh refs. |
| `checklist_items` | Manual checklist items. |
| `immune_checks` | Immune safeguard checks. |
| `anomaly_markers` | Anomaly markers. |
| `drift_markers` | Drift markers. |
| `contradiction_markers` | Contradiction markers. |
| `evidence_conflict_markers` | Evidence conflict markers. |
| `unsafe_output_markers` | Unsafe output markers. |
| `source_boundary_checks` | Source boundary checks. |
| `security_boundary_checks` | Security boundary checks. |
| `product_boundary_checks` | Product boundary checks. |
| `harness_boundary_checks` | Harness boundary checks. |
| `review_verdict_options` | Manual verdict options. |
| `rework_options` | Rework options. |
| `escalation_options` | Escalation options. |
| `limitations` | Known limits. |

Rules:

- Review checklist rendering is not auto-review.
- Reviewer verdict is not Git approval.
- ApprovalRef is not approval.
- Security review constrains but does not activate.
- Validation review evaluates but does not decide governance.

## 15. IntegrationChecklistSurface Contract

Required fields:

| Field | Meaning |
| --- | --- |
| `integration_checklist_id` | Stable integration checklist id. |
| `accepted_output_refs` | Accepted output refs. |
| `rejected_output_refs` | Rejected output refs. |
| `review_verdict_refs` | Review verdict refs. |
| `drift_register_ref` | Drift register ref. |
| `blocker_register_ref` | Blocker register ref. |
| `integration_summary_fields` | Required integration summary fields. |
| `unresolved_drift_checks` | Checks for unresolved drift. |
| `accepted_output_register_fields` | Accepted output register fields. |
| `rejected_output_register_fields` | Rejected output register fields. |
| `commit_candidate_requirements` | CommitCandidate requirements. |
| `rollback_note_requirements` | Rollback note requirements. |
| `human_decision_required` | Human decision marker. |
| `limitations` | Known limits. |

Rules:

- Integration checklist rendering is not automatic integration.
- Integrator acceptance is not final user approval.
- Unresolved drift blocks final commit advice.
- Accepted/rejected outputs must be explicit.

## 16. CommitCandidateSurface / CommitCommandBlockRenderer Contract

Required `CommitCandidate` fields:

| Field | Meaning |
| --- | --- |
| `commit_candidate_id` | Stable commit candidate id. |
| `integration_summary_ref` | Ref to integration summary. |
| `accepted_paths` | Exact accepted paths. |
| `rejected_paths` | Rejected paths. |
| `modified_paths` | Modified paths. |
| `created_paths` | Created paths. |
| `excluded_paths` | Excluded paths. |
| `drift_status` | Drift status. |
| `blocker_status` | Blocker status. |
| `commit_message_candidate` | Candidate commit message. |
| `exact_git_add_commands` | Exact-path advisory commands. |
| `commit_command` | Candidate commit command. |
| `push_command` | Candidate push command. |
| `rollback_note` | Rollback note. |
| `human_git_authority_required` | Human Git authority marker. |
| `limitations` | Known limits. |

Rules:

- CommitCandidate is advice only.
- Agent never mutates Git.
- User commits and pushes manually.
- Exact paths are required.
- Never recommend `git add .`.
- If paths are unknown, do not generate git add command.
- Product/source/generated-output blockers must be preserved.
- Commit advice comes after review and integration, not before.

## 17. Session Flow Model

MVP-0 session flow:

1. Start local interaction session.
2. Capture UserObjective.
3. Select or create roadmap/work packet posture.
4. Generate WorkPacket.
5. Generate HarnessInputPackage.
6. User manually copies HarnessInputPackage to external harness.
7. User manually pastes HarnessOutputPackage or raw output.
8. MVP-0 structures HarnessOutputPackage.
9. MVP-0 renders review checklist.
10. User/reviewer performs manual review.
11. MVP-0 records ReviewVerdictPackage.
12. MVP-0 renders integration checklist.
13. User/integrator performs manual integration.
14. MVP-0 records IntegrationSummary / DriftRegister / AcceptedOutputRegister / RejectedOutputRegister.
15. MVP-0 renders CommitCandidate / CommitCommandBlock.
16. User manually runs Git if they choose.
17. MVP-0 records final manual decision metadata only.

This is an interaction model, not an implementation.

Canonical loop:

```text id="p82-loop"
AGENT PLATFORM local MVP
-> captures UserObjective
-> generates WorkPacket / HarnessInputPackage
-> records context / memory / evidence refs
-> user manually runs OpenCode or another external harness
-> user pastes harness output
-> AGENT PLATFORM structures HarnessOutputPackage
-> AGENT PLATFORM renders review checklist
-> AGENT PLATFORM renders integration checklist
-> AGENT PLATFORM renders exact-path CommitCandidate
-> user manually decides and executes Git
```

## 18. MVP-0 Screen / Command / Step Architecture

| Screen/step | Purpose | Inputs | Outputs | Blocked actions | Required warnings | Future implementation notes |
| --- | --- | --- | --- | --- | --- | --- |
| Objective Intake | Capture objective, boundaries, and human decision points. | User text, boundary prompts. | `UserObjectiveInput`. | Source loading, product source, Git permission. | Objective is not approval. | Local CLI/TUI/web candidate after P8.10/P8.11. |
| Roadmap / WorkPacket Draft | Draft work packet posture. | Objective, roadmap refs. | WorkPacket draft. | Dispatch, agent execution. | WorkPacket is not execution. | Align with P8.3. |
| Harness Package Preview | Preview H0 package for copy/paste. | WorkPacket, context refs. | HarnessInputPackage. | OpenCode execution, provider/API/MCP calls. | User manually operates harness. | Align with P8.9. |
| Harness Output Intake | Accept pasted output. | User-pasted output. | HarnessOutputPackage candidate. | Automatic ingestion or apply. | Intake is not trust. | Safety flags needed. |
| Review Checklist | Render manual review checklist. | Harness output, reviewer refs. | Review checklist. | Auto-review, reviewer assignment. | Reviewer verdict is not Git approval. | Align with P7.0.F/P8.5. |
| Review Verdict | Capture manual review verdict. | Review checklist, human input. | ReviewVerdictPackage candidate. | Approval inference. | ApprovalRef is not approval. | Align with P8.3. |
| Integration Checklist | Render integration checks. | Verdicts, output refs, drift refs. | Integration checklist. | Automatic integration. | Unresolved drift blocks commit advice. | Align with P7.0.G/P8.15. |
| Integration Summary | Capture accepted/rejected outputs and drift. | Integrator decisions. | IntegrationSummary, DriftRegister. | Auto-acceptance. | Accepted/rejected outputs must be explicit. | Align with P8.3/P8.4. |
| Commit Candidate | Render exact-path advice. | Integration summary, paths. | CommitCandidate, CommitCommandBlock. | Git mutation, `git add .`. | User owns Git. | Align with P8.5/P8.15. |
| Session Summary | Summarize decisions, limitations, and next ticket. | Session metadata. | Session summary. | Persistence automation. | Metadata only. | Align with P8.4. |

## 19. Hermes Interface Candidate Boundary

Hermes may be an interface/runtime candidate. Hermes UI feasibility may be evaluated later in P8.8.

P8.2 may record Hermes-provided interface as candidate only. P8.2 may use Hermes-like UX inspiration. P8.2 does not activate Hermes. P8.2 does not inspect Hermes source. P8.2 does not configure Hermes. P8.2 does not start Hermes runtime. P8.2 does not activate Cadence.

## 20. OpenCode H0 Interaction Boundary

OpenCode remains H0 user-operated harness.

MVP-0 may generate HarnessInputPackage for manual OpenCode use. User manually copies the package to OpenCode. User manually pastes OpenCode output back. AGENT PLATFORM does not execute OpenCode. AGENT PLATFORM does not automate OpenCode. AGENT PLATFORM does not create OpenCode adapter execution.

Future H1/H2/H3 decisions belong to P8.9 and later gates.

## 21. Graphify / GBrain / GStack Boundary

Graphify may inform future evidence display. Graphify remains generated supporting evidence only. There is no rerun, no authority, and no repo-state writing.

GBrain may inform future memory UX. GBrain remains candidate only. There is no runtime, no persistent memory, and no automatic retrieval.

GStack may inform future skill stack UX. GStack remains candidate only. There is no execution, no adoption, and no runtime.

P8.2 does not depend on activating these candidates.

## 22. Local-Only / Security / Product Boundary

MVP-0 interaction must be local-first. MVP-0 must not expose local data to providers. MVP-0 must not include secrets/credentials in packages. MVP-0 must not ingest product/Siamese source by default. MVP-0 must not load source automatically.

MVP-0 must preserve local-only, generated-output, source, product, external, provider/auth, and Git blockers. MVP-0 must warn or block when requested action exceeds allowed boundaries. Security posture depends on P8.5.

## 23. Interfaces With P8.1 / P8.3 / P8.4 / P8.5

| Peer | Interface | P8.2 posture |
| --- | --- | --- |
| P8.1 | External inventory informs Hermes/OpenCode/Graphify/GBrain/GStack candidate labels. | Present; no pending P8.1 alignment. |
| P8.3 | Surface object fields must align with schema candidates. WorkPacket / HarnessInputPackage / HarnessOutputPackage / ReviewVerdictPackage / IntegrationSummary / CommitCandidate must be schema-aligned later. | Absent; record `pending_P8.3_schema_candidates_alignment`. |
| P8.4 | Interaction session and local artifacts require state model alignment. | Present; no pending P8.4 alignment. |
| P8.5 | Blocked actions and activation levels require gate model alignment. | Present; no pending P8.5 alignment. |

## 24. Evidence / Validation / Security Interfaces

Evidence interface:

- Interaction decisions should cite EvidenceRef-compatible governance metadata.
- Harness outputs are evidence candidates only after review.
- GraphifyRef is supporting generated evidence only.
- Evidence supports; it does not decide.

Validation interface:

- P8.2 does not run validation.
- Future validation may check surface completeness, flow completeness, no-Git-mutation invariant, and no-runtime-activation invariant.
- Validation evaluates; governance decides.

Security interface:

- P8.2 does not activate enforcement.
- Security boundaries must be visible in the interaction model.
- Secrets and credentials must be blocked from packages.
- Source/product/external/live/provider boundaries must be visible.
- Security constrains; it does not activate.

## 25. Retention / Rollback / Incident Posture

P8.2 creates no runtime state. P8.2 creates no persistence. P8.2 creates no audit log implementation. P8.2 defines future retention needs only.

Harness outputs must not be trusted or retained as authority by default. Unsafe content must be summarized safely and not repeated. Secret/credential exposure must trigger incident route. Product/source boundary violations must trigger blocked review posture. Commit candidates must preserve rollback notes.

## 26. Human Approval Requirements

Human user remains final authority.

User manually decides whether to run external harnesses. User manually decides whether to accept review verdicts. User manually decides whether to integrate outputs. User manually decides whether to run Git commands.

ApprovalRef is not approval. ReviewVerdict is not approval. CommitCandidate is not Git mutation. Broad approval is blocked. Exact-scope approval is required for future execution gates.

## 27. Stop Rules

| Stop condition | Required response |
| --- | --- |
| P8.0 boundary document is missing. | Stop and report `p8_0_missing_boundary`. |
| Interaction design requires CLI/TUI/web implementation. | Stop and keep P8.2 design-only. |
| Interaction design requires Hermes activation. | Stop and report Hermes activation blocked. |
| Interaction design requires OpenCode execution from AGENT PLATFORM. | Stop and report OpenCode execution blocked. |
| Interaction design requires adapter implementation. | Stop and report adapter implementation blocked. |
| Interaction design requires provider/auth/API/MCP activation. | Stop and report provider/auth/API/MCP blocked. |
| Interaction design requires credential use. | Stop and report credentials blocked. |
| Interaction design requires API/MCP calls. | Stop and report API/MCP calls blocked. |
| Interaction design requires tool execution. | Stop and report tool execution blocked. |
| Interaction design requires agent execution. | Stop and report agent execution blocked. |
| Interaction design requires automatic dispatch. | Stop and report automatic dispatch blocked. |
| Interaction design requires automatic reviewer assignment. | Stop and report automatic reviewer assignment blocked. |
| Interaction design requires automatic integration. | Stop and report automatic integration blocked. |
| Interaction design requires automatic Git mutation. | Stop and report Git mutation blocked. |
| Interaction design requires recommending `git add .`. | Stop and report broad Git staging blocked. |
| Interaction design requires Graphify rerun/adoption. | Stop and report Graphify rerun/adoption blocked. |
| Interaction design requires GBrain/GStack/Hermes runtime activation. | Stop and report runtime activation blocked. |
| Interaction design requires Cadence. | Stop and report Cadence blocked. |
| Interaction design requires product/Siamese source inspection. | Stop and report product/Siamese source blocked. |
| Interaction design requires source loading. | Stop and report source loading blocked. |
| Interaction design requires raw generated output inspection. | Stop and report raw generated output inspection blocked. |
| Interaction design requires secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, or API keys. | Stop and report secret/credential boundary. |
| Interaction design requires validation execution, tests, CI, scripts, or builds. | Stop and report validation/execution blocked. |
| Interaction design requires persistence, vector DB, graph DB, embeddings, or substrate selection. | Stop and report storage/substrate blocked. |
| Interaction design requires generated output tracking, source tracking expansion, publication, or Git mutation. | Stop and report tracking/publication/Git blocker. |
| Interaction design exceeds architecture/design scope. | Stop and report scope exceeded. |

## 28. Future Validation Targets

Future validation targets are proposed, not executed:

- MVPInteractionSurface required fields completeness.
- InteractionMode vocabulary conformance.
- Interaction option matrix completeness.
- MVP-0 recommended surface decision present.
- UserObjectiveInputSurface completeness.
- WorkPacketBuilderSurface completeness.
- HarnessInputPackageBuilderSurface completeness.
- HarnessOutputIntakeSurface completeness.
- ReviewChecklistSurface completeness.
- IntegrationChecklistSurface completeness.
- CommitCandidateSurface completeness.
- CommitCommandBlockRenderer exact-path invariant.
- No `git add .` invariant.
- No automatic Git invariant.
- No OpenCode execution invariant.
- No Hermes activation invariant.
- No provider/auth/API/MCP invariant.
- No tool/agent execution invariant.
- No product source invariant.
- No source loading invariant.
- No persistence/vector/graph DB invariant.
- P8.1/P8.3/P8.4/P8.5 alignment checks.
- P8.10 synthesis readiness check.

## 29. Future Hardening Candidates

Future tickets are proposed, not started:

- MVPUI-HARD-01 - MVPInteractionSurface Schema Alignment.
- MVPUI-HARD-02 - UserObjectiveInput Surface Contract Hardening.
- MVPUI-HARD-03 - WorkPacket Builder Surface Contract.
- MVPUI-HARD-04 - HarnessInputPackage Builder Surface Contract.
- MVPUI-HARD-05 - HarnessOutput Intake Safety Contract.
- MVPUI-HARD-06 - Review / Integration Checklist Surface Contract.
- MVPUI-HARD-07 - CommitCandidate Exact-Path Rendering Contract.
- MVPUI-HARD-08 - Hermes-Like UX Boundary Contract.
- MVPUI-HARD-09 - OpenCode H0 Interaction Loop Contract.
- MVPUI-HARD-10 - MVP-0 Interaction Flow Validation Targets.

## 30. Created / Modified / Not Created Register

Created:

- `0_architecture/governance/agent_platform_mvp_interaction_surface_architecture.md`

Modified:

- none

Not created / not approved:

- no P8.0 file created by P8.2
- no P8.1 file created by P8.2
- no P8.3 file created by P8.2
- no P8.4 file created by P8.2
- no P8.5 file created by P8.2
- no P8.6 file created
- no P8.7 file created
- no P8.8 file created
- no P8.9 file created
- no P8.10 file created
- no P8.11 file created
- no P8.12+ file created
- no P8.R file created
- no P9/P4/EXT.* file created
- no runtime implementation
- no CLI implementation
- no TUI implementation
- no web implementation
- no Hermes UI activation
- no Hermes runtime activation
- no adapter implementation
- no executable adapter
- no OpenCode execution from AGENT PLATFORM
- no OpenCode adapter execution
- no automatic dispatch to OpenCode
- no Graphify execution/rerun/adoption
- no GBrain execution/import/configuration/adoption/runtime
- no GStack execution/import/configuration/adoption/runtime
- no Hermes execution/import/configuration/adoption/runtime
- no provider/auth/API/MCP activation
- no credential use
- no API calls
- no MCP calls
- no tool execution
- no agent execution
- no live connector activation
- no source loading
- no source inspection
- no product/Siamese source inspection
- no raw generated output inspection
- no secrets inspected
- no credentials inspected
- no `.env` inspected
- no provider configs inspected
- no token stores inspected
- no browser auth inspected
- no local credential stores inspected
- no API keys inspected
- no validation execution
- no tests / CI / scripts / builds executed
- no security enforcement activation
- no persistence DB
- no vector DB / embeddings
- no graph DB / substrate selection
- no telemetry
- no event streaming
- no generated output tracking
- no source tracking expansion
- no publication
- no Git mutation

## 31. Recommended Next Ticket

After P8.2, if P8.3-P8.5 are not complete, continue Round 1:

- P8.3 - Core Workflow Schema Candidates
- P8.4 - Local Workspace / State Model
- P8.5 - Security / Activation Gate Model

Recommended actual: P8.3 - Core Workflow Schema Candidates, because P8.1, P8.4, and P8.5 are present while P8.3 is absent.

After P8.1 and P8.5 are complete, proceed to Round 2:

- P8.6 - Graphify Read-Only Evidence Boundary
- P8.7 - GBrain / GStack Memory Compatibility Boundary
- P8.8 - Hermes Interface / Runtime Candidate Boundary
- P8.9 - OpenCode Harness Upgrade Boundary

Do not start P8.3, P8.4, P8.5, P8.6-P8.9, P8.10, or implementation tickets from this ticket.

## 32. Final Verdict

| Question | Answer |
| --- | --- |
| What did P8.2 create? | The canonical MVP Interaction Surface Architecture document. |
| What MVP interaction surface architecture was defined? | A local, manual, non-executing, hybrid markdown-first MVPInteractionSurface for MVP-0. |
| Which interaction options were evaluated? | CLI local, TUI local, web local, Hermes-provided interface candidate, Hermes-like interface inspiration, hybrid markdown-first interface, and markdown-only manual interface. |
| Which interaction surface was recommended for MVP-0? | `hybrid_markdown_first_interface`, with possible later local CLI or simple local TUI implementation after P8.10/P8.11. |
| How is CLI local classified? | `local_cli_candidate`, strong future MVP-0 implementation candidate after authorization. |
| How is TUI local classified? | `local_tui_candidate`, future UX improvement. |
| How is web local classified? | `local_web_candidate`, deferred until security/state boundaries are clearer. |
| How is Hermes-provided interface candidate classified? | Candidate-only until P8.8 and later gates. |
| How is hybrid markdown-first interface classified? | `selected_for_mvp0_architecture`. |
| What required MVP-0 surfaces were defined? | UserObjectiveInputSurface, WorkPacketBuilderSurface, HarnessInputPackageBuilderSurface, HarnessOutputIntakeSurface, ReviewChecklistSurface, IntegrationChecklistSurface, CommitCandidateSurface, CommitCommandBlockRenderer, SessionSummarySurface, DriftRegisterSurface, AcceptedRejectedOutputRegisterSurface, AuditMetadataSurface. |
| What UserObjectiveInputSurface fields are required? | Objective, requested outcome, scope, non-goals, target artifact type, harness, product/external/security/source/Git flags, human decisions, evidence refs, limitations. |
| What WorkPacketBuilderSurface fields are required? | Objective ref, roadmap ref, title, objective, target artifact, allowed/blocked scope, inputs, stop rules, acceptance criteria, output format, reviewers, integration, commit advice, evidence/validation/security refs, limitations. |
| What HarnessInputPackageBuilderSurface fields are required? | Package id, target harness, harness level, WorkPacket ref, prompt body, context refs, path boundaries, expected outputs, stop rules, reporting format, no-runtime/no-Git statements, limitations. |
| What HarnessOutputIntakeSurface fields are required? | Output id, source harness, pasted output, summary, claimed files/commands/tests/decisions/limitations, flags, review requirement, limitations. |
| What ReviewChecklistSurface fields are required? | Checklist id, input ref, reviewer mesh refs, checklist items, immune checks, markers, boundary checks, verdict options, rework/escalation options, limitations. |
| What IntegrationChecklistSurface fields are required? | Checklist id, accepted/rejected refs, verdict refs, drift/blocker refs, summary fields, drift checks, registers, commit requirements, rollback notes, human decision, limitations. |
| What CommitCandidateSurface / CommitCommandBlockRenderer rules were defined? | Advice only, exact paths required, no agent Git mutation, no `git add .`, no command if paths unknown, blockers preserved. |
| What session flow was defined? | Objective capture through WorkPacket, HarnessInputPackage, manual harness use, pasted output intake, review, integration, CommitCandidate, and manual user Git. |
| How is Hermes handled? | Candidate-only and inspiration-only; no activation, source inspection, configuration, runtime, or Cadence. |
| How is OpenCode H0 handled? | User-operated manual harness; AGENT PLATFORM may render package and accept pasted output later, but does not execute or automate OpenCode. |
| How are Graphify / GBrain / GStack handled? | Future UX/evidence/memory/skill-stack candidates only; no activation, adoption, runtime, rerun, authority, persistent memory, or execution. |
| How are security/local-only/product boundaries handled? | Local-first, no provider exposure, no secrets/credentials, no product source by default, no source loading, blockers visible. |
| What P8 peer alignments are pending? | `pending_P8.3_schema_candidates_alignment`. |
| Did P8.2 implement CLI/TUI/web? | No. |
| Did P8.2 activate Hermes? | No. |
| Did P8.2 execute OpenCode? | No. |
| Did P8.2 implement adapters? | No. |
| Did P8.2 activate provider/auth/API/MCP? | No. |
| Did P8.2 execute tools or agents? | No. |
| Did P8.2 mutate Git? | No. |
| Did P8.2 inspect product/Siamese source? | No. |
| Did P8.2 approve source loading? | No. |
| Did P8.2 create persistence/vector DB/graph DB/substrate? | No. |
| What is the recommended next ticket? | P8.3 - Core Workflow Schema Candidates. |
