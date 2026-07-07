# External Tool Execution Gate Model

## Document Header

| Field | Value |
| --- | --- |
| Title | External Tool Execution Gate Model |
| Ticket | P9.4 |
| Status | Accepted external tool execution gate model |
| Date | 2026-07-07 |
| Scope | Governance and security gate model for future exact-scope external tool execution eligibility under AGENT PLATFORM / Siamese. |
| Authority | External tool execution gate model only, not external tool execution, runtime activation, tool execution approval, provider/auth/API/MCP activation, credential use, API calls, MCP activation, source loading, source inspection, product source inspection, external source inspection, Graphify rerun/adoption, Hermes runtime activation, GBrain/GStack execution, ECC-main execution, Codegraph execution, OpenCode execution, adapter runtime, sandbox runtime, live connector activation, validation execution, security enforcement activation, persistence/database/event streaming, telemetry, vector DB, embeddings, graph DB, substrate implementation, generated output tracking, source tracking expansion, publication, Git mutation, or Cognitive Semantic System substrate selection. |
| Related documents | P8.R, P9.0, P9.1, P9.2, P9.3, P9.5, P9.6, P3.BR, P3.3, P3.4, P3.5, P3.R, P3.0, P3.1, P3.2, P6.7, P6.4, P7.0.G, P7.0.D, P2.1, P2.2, P2.3, P1.1, P1.2, P1.3, P1.4, P1.5, P0.1, P0.2, P0.3, S-03, S-04, CSS ADR/audit, README, `.gitignore`, `.graphifyignore`. |
| P9.0 path normalization | Accepted P9.0 path is `0_architecture/governance/agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md`. |
| Output | external tool execution gate model |
| Target file | `0_architecture/governance/agent_platform_external_tool_execution_gate_model.md` |

P9.4 posture marker: `external_tool_execution_gate_model_ready_for_P9R`.

## Purpose

P8 closed MVP-0 manual / non-executing.

P9 opens the external integration foundation.

P9.0 authorizes the adopt-not-rebuild policy.

Adopt / adapt / wrap validated MIT tools when they fit.

Not default: rebuild from scratch.

P9.4 defines how future external tool execution can be evaluated.

P9.4 does not execute external tools.

P9.4 does not approve broad execution.

P9.4 establishes that every external tool execution must be exact-scope and gated.

P9.4 defines execution surfaces, required inputs, approval requirements, security requirements, validation requirements, source classification requirements, adapter requirements, rollback requirements, incident requirements, stop rules, and future evidence expectations.

P9.4 prepares P10-P14 to request future execution under controlled gates.

P9.4 does not start P10-P14.

## Current Posture

AGENT PLATFORM remains governed.

Post-P8 external integration is allowed only under gates.

External tools may become integrable under gate.

External tools are not executable by default.

External source path presence is not source inspection permission.

External source inspection is separate from external tool execution.

External tool availability is not external tool execution permission.

Tool availability is not tool execution permission.

License trust is not execution permission.

Source review is not execution permission.

Dependency review is not execution permission.

Adapter design is not execution permission.

Execution permission must be exact-scope.

Human approval is required for future execution.

Validation evaluates; governance decides.

Security constrains; it does not activate.

Evidence supports; it does not decide.

Cognitive Semantic System substrate remains deferred.

Siamese is product vision, not product activation.

P9.1, P9.2, P9.3, P9.5, and P9.6 were not synthesized by P9.4; their missing paths are recorded as pending sibling alignment until those parallel P9 foundation tickets are completed.

Canonical external source root: `4_external/sources`.

Legacy path note: `external/sources` is legacy path terminology only and is not canonical for new integration decisions.

Known GStack path: `4_external/sources/gstack-main` as path/class metadata only, not source inspection permission, adoption, execution, runtime, or dependency approval.

## External Tool Execution Gate Definition

An External Tool Execution Gate is a governance/security/validation control record that decides whether one exact external tool action may be executed in the future under a declared scope, with declared inputs, declared outputs, declared side effects, declared working directory, declared source classification, declared dependency posture, declared adapter boundary, declared retention posture, declared rollback posture, declared incident route, declared human approval, and declared stop rules.

External tool execution gate model is not external tool execution.

Gate eligibility is not execution.

Candidate status is not execution approval.

Execution permission must be exact-scope.

Broad execution is blocked.

Generic CLI access is blocked.

Generic shell access is blocked.

Generic network access is blocked.

Generic Git access is blocked.

Generic package-manager access is blocked.

Generic provider/API/MCP access is blocked.

Tool output is generated evidence unless governed otherwise.

## External Tool Execution Decision Object Model

| object | meaning | required fields | forbidden fields | security posture | validation posture | activation posture |
| --- | --- | --- | --- | --- | --- | --- |
| ExternalToolExecutionGate | Exact-scope gate record for one possible future action. | gate_id, tool refs, command spec, surfaces, boundaries, approvals, stop rules | broad family approval, generic shell approval | security refs required | validation refs required where applicable | no execution in P9.4 |
| ExternalToolExecutionRequest | Request to evaluate one exact action. | request_id, requested_action, requester, scope, evidence refs | ambiguous action, recurring action by default | must declare sensitivity | must declare expected validation | request only |
| ExternalToolIdentityRef | Identifies the candidate tool. | tool_name, class, version_or_commit_ref | accepted authority claims | identity only | not validation | metadata only |
| ExternalToolSourceRef | Source location metadata. | canonical_root, path_or_uri, source_classification_ref | source contents, loaded source excerpts | no source loading | not validation | metadata only |
| ExternalToolDependencyRef | Dependency posture metadata. | dependency_review_ref, transitive_risk_ref | unchecked dependency execution | supply-chain risk required | dependency validation ref required | blocked by default |
| ExternalToolLicenseTrustRef | License/trust posture. | license_ref, trust_ref, limitations | execution approval | trust risk required | not validation approval | blocked by default |
| ExternalToolAdapterBoundaryRef | Boundary for direct/manual/wrapper/adapter/sandbox options. | boundary_id, mode, allowed surfaces, blocked surfaces | unrestricted repo access | boundary review required | adapter validation required | not runtime |
| ExternalToolCommandSpec | Exact command/action specification. | command_template, allowed_arguments, cwd, timeout, resource limits | wildcards, generic shell, broad args | command risk review required | exact validation required | no execution in P9.4 |
| ExternalToolInputSurface | Declared inputs. | input_paths, data classes, sensitivity, allowed refs | secrets, credentials, unknown-sensitive material | sensitivity review required | input validation required | not execution |
| ExternalToolOutputSurface | Declared outputs. | output_paths, generated evidence classification, retention | authority by default, untracked generated output | output risk review required | output validation required | not tracking approval |
| ExternalToolSideEffectProfile | Side effects. | read/write/network/Git/provider/MCP profile | undeclared side effects | side-effect review required | side-effect test plan required | blocked if incomplete |
| ExternalToolWorkingDirectoryRef | Working directory boundary. | exact cwd, allowed paths, blocked paths | repo-wide unrestricted cwd | cwd risk required | cwd validation required | not execution |
| ExternalToolEnvironmentRef | Environment boundary. | allowed env names, forbidden env names | `.env`, provider config, credential vars | environment review required | environment validation required | not execution |
| ExternalToolCredentialBoundary | Credential prohibition or credential-ref route if future-approved. | credential_allowed=false by default, credential refs if future gate exists | raw credentials, token stores, API keys | credential exposure review required | credential validation requires future gate | blocked by default |
| ExternalToolNetworkBoundary | Network posture. | network_allowed=false by default, endpoints if future gate exists | broad internet access | network risk review required | network validation requires future gate | blocked by default |
| ExternalToolFilesystemBoundary | Filesystem posture. | read/write paths, blocked paths, generated output class | repo-wide read/write | filesystem risk review required | filesystem validation required | exact-scope only |
| ExternalToolMCPBoundary | MCP posture. | mcp_allowed=false by default, server refs if future gate exists | broad MCP access | MCP risk review required | MCP validation requires future gate | blocked by default |
| ExternalToolGitBoundary | Git posture. | git_mutation_allowed=false by default | stage, commit, push, force-add, publish | Git risk review required | Git validation requires future gate | blocked by default |
| ExternalToolGeneratedOutputBoundary | Generated output handling. | output class, retention, tracking posture | tracking by default | output exposure review required | classification validation required | not tracking approval |
| ExternalToolHumanApprovalRef | Human exact-scope approval reference. | approver, scope, expiration, stop rules | broad approval, implied approval | human approval required | approval evidence required | not execution alone |
| ExternalToolValidationRef | Validation posture. | validation plan, exact command refs, expected evidence | validation as authority | validation risk required | validation evaluates | not governance decision |
| ExternalToolSecurityRef | Security posture. | security review refs, risks, mitigations | security as activation | security constrains | not validation alone | not activation |
| ExternalToolRollbackRef | Rollback posture. | rollback plan, owner, feasibility | no rollback for mutating action | rollback risk required | rollback validation required | blocked if missing |
| ExternalToolIncidentRef | Incident posture. | incident route, severity, contacts | no incident route | incident readiness required | incident drill ref if needed | blocked if missing |
| ExternalToolStopRule | Stop condition. | trigger, action, owner | ignored stop rules | stop rules required | stop-rule validation required | blocks execution |
| ExternalToolDecisionRecord | Final future gate decision record. | decision, basis, limitations, expiration | broad future approval | decision risk recorded | validation evidence cited | no P9.4 execution |

## External Tool Execution Gate Contract

ExternalToolExecutionGate fields:

- gate_id
- gate_title
- tool_identity_ref
- tool_source_ref
- tool_class
- tool_version_or_commit_ref
- license_trust_ref
- dependency_review_ref
- source_inspection_permission_ref
- adapter_boundary_ref
- requested_action
- execution_scope
- execution_status
- command_spec_ref
- working_directory_ref
- input_surface_refs
- output_surface_refs
- side_effect_profile
- environment_requirements
- credential_boundary
- network_boundary
- filesystem_boundary
- mcp_boundary
- git_boundary
- provider_api_boundary
- generated_output_boundary
- source_classification_refs
- sensitivity
- local_only_posture
- product_boundary_posture
- external_source_boundary_posture
- retention_posture
- rollback_posture
- incident_posture
- validation_refs
- security_refs
- evidence_refs
- human_approval_ref
- required_gates
- allowed_actions
- blocked_actions
- stop_rules
- limitations
- decision_expiration_policy

Every external tool execution gate must be exact-scope.

No gate may approve generic future execution.

No gate may approve tool families broadly.

No gate may approve repeated execution unless recurrence / Cadence gates are separately approved.

No gate may approve Git mutation unless explicit future Git automation gate exists.

No gate may approve source tracking expansion unless exact tracking gate exists.

No gate may approve generated output tracking unless exact tracking gate exists.

## Execution Status Model

P9.4 defines these statuses:

- external_tool_execution_deferred_by_default
- blocked_pending_P9.0_charter
- blocked_pending_source_root_normalization
- blocked_pending_license_trust_review
- blocked_pending_source_inspection_permission
- blocked_pending_dependency_review
- blocked_pending_adapter_boundary
- blocked_pending_security_review
- blocked_pending_validation_readiness
- blocked_pending_human_approval
- blocked_pending_retention_rollback_incident
- blocked_pending_exact_command_spec
- blocked_pending_input_output_surface
- blocked_pending_side_effect_profile
- blocked_pending_credential_boundary
- blocked_pending_network_boundary
- blocked_pending_filesystem_boundary
- blocked_pending_mcp_boundary
- blocked_pending_git_boundary
- blocked_pending_generated_output_boundary
- candidate_for_future_exact_execution_gate
- approved_for_future_exact_execution_review
- rejected_for_scope
- deferred
- expired
- executed_out_of_scope_for_P9_4_prohibited

No P9.4 status may execute a tool.

No P9.4 status may approve broad execution.

No P9.4 status may activate runtime.

## External Tool Class Matrix

| external_tool_class | examples | default posture | possible future candidate posture | blocked behavior | required gates |
| --- | --- | --- | --- | --- | --- |
| documentation-only check tool | markdown/report checks | external_tool_execution_deferred_by_default | exact non-executing posture check | source loading, runtime | P9.0, exact scope, human approval |
| metadata-only check tool | path posture checks | external_tool_execution_deferred_by_default | exact metadata check | content inspection | P9.0, source root posture, human approval |
| validation command candidate | test or validator command | external_tool_execution_deferred_by_default | future validation execution gate | tests without gate | validation/security/human gates |
| Graphify command | Graphify repo analysis or rerun | external_tool_execution_deferred_by_default | future exact Graphify gate | rerun/adoption/authority | P10 gates, source/security/validation/human gates |
| Hermes command | Hermes shell/runtime command | external_tool_execution_deferred_by_default | future Hermes local spike gate | runtime/Cadence | source/dependency/runtime/Cadence/security gates |
| GBrain command | memory/runtime command | external_tool_execution_deferred_by_default | future memory sandbox gate | persistent memory runtime | storage/security/retention gates |
| GStack command | skill/bootstrap command | external_tool_execution_deferred_by_default | future skill bootstrap gate | execution/adoption | source/dependency/skill authority/security gates |
| ECC-main command | component/runtime command | external_tool_execution_deferred_by_default | future controlled component spike | autonomous runtime | source/dependency/orchestration/security gates |
| Codegraph command | code graph analysis | external_tool_execution_deferred_by_default | future controlled analysis spike | source inspection without gate | source/tool/security/validation gates |
| OpenCode command | harness CLI/API | external_tool_execution_deferred_by_default | future exact integration gate | internal runtime adoption | harness/security/provider/MCP gates if implicated |
| shell command | generic shell | external_tool_execution_deferred_by_default | exact future command only | generic shell access | exact command/security/human gate |
| subprocess execution | subprocess call | external_tool_execution_deferred_by_default | exact future command only | generic subprocess | exact command/security/human gate |
| filesystem read tool | read command | external_tool_execution_deferred_by_default | exact path-scoped read gate | source/product/external content inspection | source classification/security gate |
| filesystem write tool | write command | external_tool_execution_deferred_by_default | exact path-scoped write gate | generated output tracking by default | filesystem/rollback/incident gate |
| network call tool | curl/API client | external_tool_execution_deferred_by_default | future exact network gate | broad network | provider/API/network/security gate |
| package-manager command | npm/pip/etc. | external_tool_execution_deferred_by_default | future exact dependency gate | installs/lockfile changes by default | dependency/supply-chain/security gate |
| build command | build tool | external_tool_execution_deferred_by_default | future exact build gate | broad build | dependency/output/security gate |
| test command | test runner | external_tool_execution_deferred_by_default | future exact test gate | broad test suite | validation/security/output gate |
| CI command | CI runner | external_tool_execution_deferred_by_default | future exact CI gate | remote runner activation | CI/security/provider gate |
| Git command | Git mutation | external_tool_execution_deferred_by_default | future Git governance only | stage/commit/push/force-add | Git automation gate |
| MCP tool call | MCP server/tool | external_tool_execution_deferred_by_default | future exact MCP gate | broad MCP activation | provider/auth/API/MCP gate |
| provider/API tool call | LLM/provider/API call | external_tool_execution_deferred_by_default | future exact provider gate | credentials/network/API | provider/auth/security/cost gate |
| live connector tool | Slack/email/CRM/etc. | external_tool_execution_deferred_by_default | future connector gate | polling/scheduling/live integration | connector/privacy/security gate |
| product-bound tool | Siamese/product tooling | external_tool_execution_deferred_by_default | future product gate | product source inspection/execution | P4/GT-09 equivalent gate |
| generated-output tool | output generator | external_tool_execution_deferred_by_default | future generated-output gate | tracking by default | output classification/tracking gate |
| adapter wrapper command | wrapper/adapter command | external_tool_execution_deferred_by_default | future adapter gate | unrestricted repo access | P9.5 adoption mode + adapter/security gate |
| local sandbox command | sandboxed command | external_tool_execution_deferred_by_default | future sandbox gate | unrestricted sandbox runtime | sandbox/security/resource gate |

Graphify rerun requires a future exact execution gate.

Hermes runtime requires a future exact execution gate.

GBrain / GStack execution requires a future exact execution gate.

ECC-main execution requires a future exact execution gate.

Codegraph execution requires a future exact execution gate.

OpenCode execution requires a future exact execution gate.

Provider/API/MCP use requires future exact provider/auth/API/MCP gate.

Git mutation remains blocked.

Package-manager commands remain blocked.

Network commands remain blocked.

Product-bound tools remain blocked.

Generated-output tracking remains blocked.

## External Tool Action Scope Model

Exact action scope fields:

- tool_name
- tool_path_or_identifier
- tool_version_or_commit
- action_name
- command_template
- allowed_arguments
- forbidden_arguments
- working_directory
- input_paths
- output_paths
- read_paths
- write_paths
- environment_variables_allowed
- environment_variables_forbidden
- network_allowed
- mcp_allowed
- provider_api_allowed
- credentials_allowed
- git_mutation_allowed
- generated_output_tracking_allowed
- source_tracking_allowed
- publication_allowed
- timeout_policy
- resource_limits
- expected_outputs
- failure_behavior
- rollback_behavior
- incident_behavior

Any missing exact action scope field blocks future execution.

## Adapter Boundary Requirements

Every external tool execution candidate must declare whether it uses:

- direct_manual_execution
- manual_command_block_only
- wrapper_script_candidate
- adapter_candidate
- sandbox_candidate
- vendor_code_candidate
- fork_candidate
- submodule_candidate
- runtime_integration_candidate

P9.4 does not choose vendor/fork/wrapper/submodule adoption mode.

P9.5 owns adoption mode.

P9.4 must require an adapter boundary before future execution.

No external tool may execute directly against unrestricted repository surfaces.

No external tool may execute against product/Siamese source without product gate.

No external tool may execute against secrets, credentials, provider configs, token stores, browser auth, local credential stores, or API keys.

## Source Classification Interface

Source classification is not source loading permission.

Path presence is not source inspection permission.

External source inspection must be authorized separately by P9.3 or a future exact source review ticket.

External tool execution cannot imply source inspection.

External tool execution cannot imply product source inspection.

External tool execution cannot imply external source loading.

External tool execution cannot imply generated output tracking.

Canonical source root is 4_external/sources.

legacy external/sources is not canonical for new integration.

## License / Trust Interface

License trust is required but not sufficient for execution.

MIT license presence does not approve execution.

Dependency trust is required but not sufficient for execution.

Runtime entrypoint review is required before execution.

Side-effect review is required before execution.

Supply-chain risk must be recorded.

Transitive dependency risk must be recorded.

Generated output risk must be recorded.

Provider/API/MCP risk must be recorded when implicated.

## Security Interface

Security constrains; it does not activate.

Future external tool execution requires security refs.

Security review must cover:

- secret / credential exposure
- environment access
- filesystem access
- network access
- provider/API/MCP access
- Git mutation risk
- generated output risk
- source tracking risk
- product source risk
- external source risk
- local-only material risk
- customer data risk
- runtime persistence risk
- incident response
- rollback feasibility

Unknown sensitivity blocks execution.

Secrets and credentials are never tool input.

Provider auth material is never tool input unless future exact provider/auth gate approves a credential-ref-only route.

## Validation Interface

Validation evaluates; governance decides.

Validation readiness does not execute tools.

Validation command candidates require their own execution gate.

Validation outputs are generated evidence by default.

Validation refs must not become execution approval by themselves.

Future validation must cite exact command, input, output, cwd, side effects, retention, rollback, incident route, and stop rules.

## Human Approval Interface

Human approval is required before future external tool execution.

ApprovalRef is not approval.

Reviewer approval is not Git approval.

User remains final authority.

Human approval must be exact-scope.

Human approval must include allowed actions, blocked actions, evidence refs, validation refs, security refs, retention posture, rollback posture, incident posture, expiration policy, and stop rules.

Broad human approval is blocked.

Ambiguous user intent is blocked.

## Git / Source Tracking Interface

The agent never mutates Git.

The user commits and pushes manually unless a future explicit Git automation gate exists.

Never recommend `git add .`.

External tool execution must not stage, commit, push, force-add, or publish.

Generated output tracking remains blocked unless exact future tracking gate approves it.

Source tracking expansion remains blocked unless exact future tracking gate approves it.

External tool outputs must be classified before any tracking recommendation.

## Generated Output Interface

External tool outputs are generated evidence by default.

Generated evidence supports; it does not decide.

Generated outputs are not authority.

Generated outputs must be classified.

Generated outputs must have retention posture.

Generated outputs must have rollback posture.

Generated outputs must have incident posture when sensitive.

Generated outputs must not be tracked unless exact tracking gate approves.

Raw Graphify outputs remain generated evidence / local-only unless curated.

## Product / Siamese Interface

Siamese is product vision, not product activation.

Product/Siamese source remains blocked.

Product-bound external tool execution requires future exact product gate.

Product-bound external tool execution requires security review, validation posture, source classification, adapter boundary, rollback, incident route, and human approval.

P9.4 does not inspect product source.

P9.4 does not activate product behavior.

## Cognitive Semantic System Interface

Cognitive Semantic System substrate remains deferred.

External tool execution cannot select substrate.

Graphify output cannot become Cognitive Semantic System authority through execution.

GBrain/GStack execution cannot become Cognitive Semantic System substrate through P9.4.

Codegraph execution cannot become Cognitive Semantic System substrate through P9.4.

Graph / vector / memory runtime remains blocked unless future exact substrate and runtime gates approve it.

## External Tool Family Boundary

Graphify:

Graphify may become controlled repo evidence tooling only after P10 gates.

Graphify rerun requires future exact execution gate.

Graphify outputs are generated evidence, not authority.

Hermes:

Hermes requires source review, dependency audit, architecture mapping, runtime/Cadence boundary decision, adoption mode decision, adapter design, local spike approval, safety review, and controlled runtime gate.

Hermes runtime remains blocked in P9.4.

GBrain / GStack:

GBrain and GStack require source review, license/dependency/storage/skill audit, memory authority model, skill authority boundary, adoption decisions, integration designs, sandbox spikes, and retention/rollback/incident hardening.

GStack path is 4_external/sources/gstack-main.

GBrain/GStack execution remains blocked in P9.4.

ECC-main:

ECC-main requires source review, license/dependency/runtime audit, architecture mapping, overlap analysis, autonomy/orchestration boundary, adoption decision, and controlled component spike if adopted.

ECC-main runtime remains blocked in P9.4.

Codegraph:

Codegraph remains candidate only until exact source review, license/dependency audit, tool boundary, execution gate, and adoption decision exist.

OpenCode:

OpenCode remains manual external development harness unless future exact integration gate approves otherwise.

OpenCode execution is not internal runtime adoption.

MCP / Provider tools:

MCP/provider/API tools require provider/auth/API/MCP activation decision, credential model, data exposure review, cost/telemetry review, security review, validation posture, rollback, incident route, and human approval.

## External Tool Execution Gate Decision Matrix

| decision area | required evidence | required security posture | required validation posture | required human approval | default decision | future eligibility condition |
| --- | --- | --- | --- | --- | --- | --- |
| documentation-only external tool | exact scope and non-execution evidence | no source or secret exposure | marker/path posture only | exact-scope approval | deferred | P9 gate record complete |
| metadata-only external tool | path metadata and classification | no content inspection | posture validation only | exact-scope approval | deferred | exact path and output boundary |
| Graphify rerun | P10 gate, source/tool boundary, output plan | generated output and repo safety review | exact command validation plan | explicit human approval | blocked | future exact Graphify execution gate |
| Hermes local shell spike | source/dependency/runtime review | runtime/Cadence safety review | exact spike validation plan | explicit human approval | blocked | future Hermes runtime/Cadence gate |
| GBrain memory sandbox spike | memory/storage authority evidence | persistence/retention/security review | sandbox validation plan | explicit human approval | blocked | future memory/storage/security gate |
| GStack skill bootstrap spike | skill/source/dependency evidence | skill authority and filesystem review | bootstrap validation plan | explicit human approval | blocked | future exact GStack gate |
| ECC-main controlled component spike | component/source/dependency evidence | autonomy/orchestration review | component validation plan | explicit human approval | blocked | future controlled component gate |
| Codegraph controlled analysis spike | source review permission and tool boundary | source inspection safety review | analysis validation plan | explicit human approval | blocked | future exact Codegraph gate |
| OpenCode internal adapter candidate | harness boundary and integration evidence | provider/MCP/credential review if implicated | adapter validation plan | explicit human approval | blocked | future OpenCode integration gate |
| provider/API/MCP tool candidate | provider/auth/API/MCP decision refs | credential/network/data review | exact call validation plan | explicit human approval | blocked | future provider/auth/API/MCP gate |
| live connector tool candidate | connector/data/notification evidence | privacy/network/live system review | connector validation plan | explicit human approval | blocked | future live connector gate |
| product-bound tool candidate | product gate and source classification | product source/security review | product validation plan | explicit human approval | blocked | P4/GT-09 or equivalent gate |
| Git mutation candidate | future Git governance evidence | Git safety and rollback review | exact Git validation plan | explicit user approval | blocked | future Git automation gate if ever considered |
| package-manager command candidate | dependency/supply-chain evidence | package install risk review | exact command validation plan | explicit human approval | blocked | future dependency execution gate |
| network command candidate | network/provider evidence | network and data exposure review | exact network validation plan | explicit human approval | blocked | future network/provider gate |
| generated-output tracking candidate | output classification evidence | generated output exposure review | tracking validation plan | explicit human approval | blocked | future exact tracking gate |

## External Tool Stop Rules

STOP if P9.0 is missing.

STOP if source root posture is unresolved.

STOP if license/trust posture is missing.

STOP if source inspection permission is missing where source review is required.

STOP if dependency review is missing.

STOP if adapter boundary is missing.

STOP if exact command/action scope is missing.

STOP if working directory is missing.

STOP if input/output surfaces are missing.

STOP if side-effect profile is missing.

STOP if security refs are missing.

STOP if validation refs are missing where required.

STOP if human approval is missing.

STOP if retention posture is missing.

STOP if rollback posture is missing.

STOP if incident posture is missing.

STOP if secrets or credentials would be read, passed, transformed, logged, or exposed.

STOP if provider configs, token stores, browser auth, local credential stores, .env, or API keys are implicated.

STOP if product/Siamese source would be inspected without product gate.

STOP if external source contents would be inspected without source review gate.

STOP if generated outputs would be tracked without tracking gate.

STOP if source tracking would expand without exact tracking gate.

STOP if Git mutation is attempted.

STOP if network/API/MCP is attempted without provider/auth gate.

STOP if package-manager/build/test/CI command is attempted without exact future execution gate.

STOP if Graphify/Hermes/GBrain/GStack/ECC/Codegraph/OpenCode execution is attempted without exact future execution gate.

STOP if runtime activation, autonomous orchestration, scheduler, Cadence, live connector activation, persistence, telemetry, vector DB, graph DB, or substrate selection is implied.

## Required P9.4 Invariants

EXTEXEC-001 P9.4 creates an external tool execution gate model only.

EXTEXEC-002 External tool execution gate model is not external tool execution.

EXTEXEC-003 External tool availability is not execution permission.

EXTEXEC-004 Source review is not execution permission.

EXTEXEC-005 License trust is not execution permission.

EXTEXEC-006 Dependency review is not execution permission.

EXTEXEC-007 Adapter design is not execution permission.

EXTEXEC-008 Execution permission must be exact-scope.

EXTEXEC-009 Broad external tool execution is blocked.

EXTEXEC-010 Generic shell/subprocess execution is blocked.

EXTEXEC-011 Generic network/API/MCP execution is blocked.

EXTEXEC-012 Generic package-manager/build/test/CI execution is blocked.

EXTEXEC-013 Generic Git mutation is blocked.

EXTEXEC-014 Human approval is required for future execution.

EXTEXEC-015 Validation evaluates; governance decides.

EXTEXEC-016 Security constrains; it does not activate.

EXTEXEC-017 Evidence supports; it does not decide.

EXTEXEC-018 Generated outputs are evidence by default, not authority.

EXTEXEC-019 Generated output tracking requires future exact tracking gate.

EXTEXEC-020 Source tracking expansion requires future exact tracking gate.

EXTEXEC-021 Path presence is not source inspection permission.

EXTEXEC-022 4_external/sources is the canonical external source root.

EXTEXEC-023 legacy external/sources is not canonical for new decisions.

EXTEXEC-024 Graphify rerun requires a future exact execution gate.

EXTEXEC-025 Hermes runtime requires a future exact execution gate.

EXTEXEC-026 GBrain / GStack execution requires a future exact execution gate.

EXTEXEC-027 ECC-main execution requires a future exact execution gate.

EXTEXEC-028 Codegraph execution requires a future exact execution gate.

EXTEXEC-029 Provider/API/MCP use requires future exact provider/auth/API/MCP gate.

EXTEXEC-030 Product-bound execution requires future exact product gate.

EXTEXEC-031 Cognitive Semantic System substrate remains deferred.

EXTEXEC-032 P9.4 does not start P10-P14.

## Future Validation Targets

- ExternalToolExecutionGate required fields completeness
- ExternalToolCommandSpec exact-scope completeness
- ExternalToolInputSurface completeness
- ExternalToolOutputSurface completeness
- ExternalToolSideEffectProfile completeness
- ExternalToolWorkingDirectoryRef completeness
- ExternalToolCredentialBoundary completeness
- ExternalToolNetworkBoundary completeness
- ExternalToolFilesystemBoundary completeness
- ExternalToolMCPBoundary completeness
- ExternalToolGitBoundary completeness
- ExternalToolGeneratedOutputBoundary completeness
- license/trust posture presence
- dependency review posture presence
- source inspection permission linkage
- adapter boundary linkage
- security ref linkage
- validation ref linkage
- human approval linkage
- retention / rollback / incident completeness
- no-secret/no-credential execution invariant
- no-product-source-inspection invariant
- no-external-source-inspection-without-gate invariant
- no-generated-output-tracking-without-gate invariant
- no-source-tracking-expansion-without-gate invariant
- no-Git-mutation invariant
- Graphify future exact execution gate check
- Hermes future exact execution gate check
- GBrain/GStack future exact execution gate check
- ECC-main future exact execution gate check
- provider/API/MCP future exact gate check
- P9.R closure readiness check

No future validation target is executed by P9.4.

## Future Hardening Candidates

- EXTEXEC-HARD-01 - External Tool CommandSpec Schema Alignment
- EXTEXEC-HARD-02 - External Tool Input / Output Surface Contract
- EXTEXEC-HARD-03 - External Tool Side-Effect Profile Contract
- EXTEXEC-HARD-04 - External Tool Sandbox Boundary Contract
- EXTEXEC-HARD-05 - External Tool Generated Output Handling Contract
- EXTEXEC-HARD-06 - External Tool Human Approval Checklist
- EXTEXEC-HARD-07 - External Tool Execution Incident Playbook
- EXTEXEC-HARD-08 - External Tool Gate Validation Checklist

These are candidates only. P9.4 does not start them.

## Created / Not Created Register

Created:

- external tool execution gate model document created
- ExternalToolExecutionGate model created
- ExternalToolExecutionRequest model created
- ExternalToolIdentityRef model created
- ExternalToolSourceRef model created
- ExternalToolDependencyRef model created
- ExternalToolLicenseTrustRef model created
- ExternalToolAdapterBoundaryRef model created
- ExternalToolCommandSpec model created
- ExternalToolInputSurface model created
- ExternalToolOutputSurface model created
- ExternalToolSideEffectProfile model created
- ExternalToolWorkingDirectoryRef model created
- ExternalToolEnvironmentRef model created
- ExternalToolCredentialBoundary model created
- ExternalToolNetworkBoundary model created
- ExternalToolFilesystemBoundary model created
- ExternalToolMCPBoundary model created
- ExternalToolGitBoundary model created
- ExternalToolGeneratedOutputBoundary model created
- ExternalToolHumanApprovalRef model created
- ExternalToolValidationRef model created
- ExternalToolSecurityRef model created
- ExternalToolRollbackRef model created
- ExternalToolIncidentRef model created
- ExternalToolStopRule model created

Not created / not approved:

- no external tool executed
- no internal tool executed
- no Graphify rerun
- no Hermes execution
- no GBrain execution
- no GStack execution
- no ECC-main execution
- no Codegraph execution
- no OpenCode execution
- no provider/auth/API/MCP activation
- no credential use
- no API calls
- no MCP activation
- no live connector activation
- no runtime activation
- no agent execution
- no autonomous orchestration
- no validation execution
- no tests / CI / scripts / builds
- no security enforcement activation
- no package-manager command
- no shell/subprocess execution beyond allowed checks
- no source loading
- no source inspection
- no 4_external/sources content inspection
- no legacy external/sources content inspection
- no product source inspection
- no external source inspection
- no secrets inspected
- no credentials inspected
- no .env inspected
- no provider configs inspected
- no token stores inspected
- no browser auth inspected
- no local credential stores inspected
- no API keys inspected
- no Graphify adoption
- no Hermes runtime activation
- no GBrain/GStack runtime activation
- no ECC-main runtime activation
- no Codegraph adoption
- no wrapper code created
- no adapter runtime created
- no sandbox runtime created
- no vendor/fork/submodule change created
- no persistence/database/event stream
- no telemetry
- no vector DB / embeddings
- no graph DB / substrate implementation
- no generated output tracking approved
- no source tracking expansion approved
- no publication
- no Git mutation
- no .gitignore modified
- no .graphifyignore modified
- no generated outputs modified/tracked
- no Cognitive Semantic System substrate selected
- no P9.5 started
- no P9.6 started
- no P9.R started
- no P10/P11/P12/P13/P14 started

## Recommended Next Tickets

P9.4 is one parallel P9 foundation ticket after P9.0.

Parallel P9 tickets after P9.0:

- P9.1 - External Source Root Normalization
- P9.2 - External Source License / Trust Intake Model
- P9.3 - External Source Inspection Permission Gate
- P9.4 - External Tool Execution Gate Model
- P9.5 - Vendor / Fork / Wrapper / Submodule Decision Model
- P9.6 - External Integration Rollback / Incident Protocol

After P9.1-P9.6:

- P9.R - External Integration Foundation Closure

Recommended actual: Continue remaining P9.1-P9.6 foundation tickets until the parallel batch is complete.

If P9.1-P9.6 are complete, proceed to P9.R - External Integration Foundation Closure.

Do not start P9.R inside P9.4.

## Final Verdict

What did P9.4 create? `0_architecture/governance/agent_platform_external_tool_execution_gate_model.md`.

What external tool execution gate model was defined? A governance/security/validation exact-scope gate model for future external tool execution eligibility.

What is an ExternalToolExecutionGate? A control record that may decide whether one exact external tool action can be eligible for future execution after declared scope, source classification, dependency, security, validation, adapter, rollback, incident, and human approval gates.

What is an ExternalToolExecutionRequest? A request to evaluate one exact external tool action against the gate model.

What is an ExternalToolCommandSpec? The exact command/action specification including command template, allowed arguments, cwd, inputs, outputs, side effects, timeout, and resource constraints.

What input/output/side-effect fields are required? Declared input paths, output paths, read paths, write paths, environment variables, network/MCP/provider/API posture, credential posture, Git posture, generated output tracking posture, source tracking posture, publication posture, timeout policy, resource limits, expected outputs, failure behavior, rollback behavior, and incident behavior.

What execution statuses are defined? The P9.4 status set includes `external_tool_execution_deferred_by_default`, all blocked_pending_* statuses, `candidate_for_future_exact_execution_gate`, `approved_for_future_exact_execution_review`, `rejected_for_scope`, `deferred`, `expired`, and `executed_out_of_scope_for_P9_4_prohibited`.

What external tool classes are covered? Documentation-only tools, metadata-only tools, validation commands, Graphify, Hermes, GBrain, GStack, ECC-main, Codegraph, OpenCode, shell/subprocess, filesystem read/write, network, package-manager, build, test, CI, Git, MCP, provider/API, live connector, product-bound, generated-output, adapter wrapper, and local sandbox commands.

What is the default execution posture? `external_tool_execution_deferred_by_default`.

Does P9.4 execute any external tool? No.

Does P9.4 approve broad tool execution? No.

Does P9.4 approve Graphify rerun? No.

Does P9.4 approve Hermes runtime? No.

Does P9.4 approve GBrain / GStack execution? No.

Does P9.4 approve ECC-main execution? No.

Does P9.4 approve Codegraph execution? No.

Does P9.4 approve OpenCode execution? No.

Does P9.4 approve provider/auth/API/MCP? No.

Does P9.4 inspect external source contents? No.

Does P9.4 inspect product/Siamese source? No.

Does P9.4 use credentials? No.

Does P9.4 approve generated output tracking? No.

Does P9.4 approve source tracking expansion? No.

Does P9.4 mutate Git? No.

What is the canonical external source root? `4_external/sources`.

Is legacy external/sources canonical? No.

What is the next ticket? Continue remaining P9.1-P9.6 foundation tickets; after all are complete, proceed to P9.R.

Final declaration: `external_tool_execution_gate_model_ready_for_P9R`.
