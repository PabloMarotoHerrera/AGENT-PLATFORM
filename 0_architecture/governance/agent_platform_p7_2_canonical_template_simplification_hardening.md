# Canonical Template Simplification / Hardening

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | Canonical Template Simplification / Hardening |
| Ticket | P7.2 |
| Status | Accepted canonical template simplification / hardening |
| Scope | Documentation-only simplification and hardening of the canonical manual OpenCode work packet interface. |
| Authority | Template simplification and hardening only, not second pilot execution, not runtime activation, not OpenCode integration, not tool execution, not provider/auth/API/MCP activation, not autonomous orchestration, not automatic dispatch, not automatic reviewer assignment, not automatic integration, not Git mutation. |
| Target files | `agent_platform_manual_agent_native_work_packet_interface_template.md`; `agent_platform_p7_2_canonical_template_simplification_hardening.md` |

## 2. Purpose

P7.2 simplifies and hardens the canonical manual OpenCode work packet interface created in P7.1-FIRST-PILOT.

P7.2 consumes P7.1.R audit findings and makes the interface easier to use for repeated manual documentation/governance tasks while preserving all safety boundaries.

P7.2 does not execute a second pilot and does not start P7.3.

## 3. Current Posture

| Area | Current posture | P7.2 interpretation | Blocked interpretation |
| --- | --- | --- | --- |
| Canonical interface | Complete but verbose. | Keep full schema as canonical reference and add compact modes. | Replace safety boundaries with informal prompts. |
| P7.1.R audit | Accepted simplification and hardening need. | Consume findings and mitigate overhead. | Treat audit as runtime readiness. |
| OpenCode | H0 user-operated harness only. | Improve manual package clarity. | OpenCode integration or adapter. |
| Reviewer mesh | Metadata-only review. | Add compact boundary drift checklist. | Automatic review. |
| Integrator | Manual synthesis and Git advice. | Add exact-path checklist. | Automatic integration or Git mutation. |

## 4. Inputs Reviewed

| Input | Evidence | P7.2 use | Limitation |
| --- | --- | --- | --- |
| `agent_platform_manual_agent_native_work_packet_interface_template.md` | Required path and template markers present. | Modified with compact modes and hardening addendum. | No runtime execution. |
| `agent_platform_p7_1_first_manual_agent_native_pilot_report.md` | Required path present. | Confirms first pilot output. | Not modified. |
| `agent_platform_p7_1_first_manual_pilot_audit_lessons_learned.md` | Required findings markers present. | Source for simplification/hardening decisions. | Not modified. |
| `agent_platform_manual_agentic_workflow_planning_closure.md` | Required path present. | Preserves P7.1 manual-only eligibility. | Not modified. |
| `agent_platform_manual_harness_opencode_hermes_boundary_strategy.md` | Required path present. | Preserves H0/H1/H2/H3 semantics. | Not modified. |
| `agent_platform_reviewer_mesh_immune_safeguards_contract.md` | Required path present. | Preserves reviewer mesh boundary. | Not modified. |
| `agent_platform_manual_integrator_commit_advisory_protocol.md` | Required path present. | Preserves CommitCandidate and exact-path Git boundary. | Not modified. |

## 5. Non-Action Statement

P7.2 does not start P7.3, execute a second pilot, start P8, start P4, modify P7.1 report, modify P7.1.R audit, modify P7.0.0 or P7.0.A-H, activate runtime, activate autonomous orchestration, create automatic dispatch, create automatic reviewer assignment, create automatic integration, activate OpenCode internally, create OpenCode adapter, activate Hermes runtime, activate GBrain runtime, activate Cadence, activate MCP, activate providers/auth/API, use credentials, call APIs/network/MCP, activate tools, execute agents, load source, inspect product/Siamese source, inspect external source, inspect GBrain source, inspect raw Graphify output, rerun/adopt Graphify, execute/adopt Codegraph, run validation/tests/CI/scripts/builds, activate security enforcement, create persistence/vector DB/graph DB, track generated outputs, expand source tracking, publish, stage/commit/push, mutate Git, recommend `git add .`, or select Cognitive Semantic System substrate.

## 6. P7.1.R Audit Findings Consumed

Consumed findings:

```text
canonical_work_packet_interface_usable_with_minor_simplification
template_hardening_required_before_second_pilot
manual workflow overhead: medium_to_high_but_acceptable_for_governance_tasks
P7.1-DRIFT-003 remains open for second pilot
P7.1-DRIFT-004 requires template simplification
```

## 7. Simplification Decisions Applied

| Decision | Applied change |
| --- | --- |
| Create compact WorkPacket view for simple tasks. | Added `Compact WorkPacket View For Documentation-Only Tasks`. |
| Create compact HarnessOutputPackage view for OpenCode summaries. | Added `Compact HarnessOutputPackage View For OpenCode Summaries`. |
| Keep full schema as canonical reference, but use compact mode for small documentation tickets. | Added `P7.2 Simplified Usage Modes` and usage mode matrix. |
| Allow irrelevant agent-native refs as `not_applicable_with_reason`. | Added field classification model. |
| Keep exact target files and blocked actions mandatory. | Preserved as mandatory fields. |
| Keep stop rules mandatory. | Preserved as mandatory fields. |
| Keep Git advisory exact-path only. | Added compact integrator exact-path checklist. |

## 8. Hardening Decisions Applied

| Decision | Applied change |
| --- | --- |
| Add required/optional field classification. | Added mandatory, conditional, optional, not-applicable, and blocked classifications. |
| Add minimal viable WorkPacket template. | Added compact WorkPacket view. |
| Add full WorkPacket template. | Preserved existing full canonical template. |
| Add OpenCode-specific output checklist. | Added compact HarnessOutputPackage checklist. |
| Add reviewer checklist for boundary drift. | Added compact reviewer boundary drift checklist. |
| Add integrator checklist for accepted/rejected files and exact Git advice. | Added compact integrator exact-path checklist. |
| Add examples for documentation-only governance tasks. | Added safe documentation-only example. |
| Add examples of rejected unsafe outputs. | Added rejected unsafe output example. |

## 9. Template Changes Summary

P7.2 modified `agent_platform_manual_agent_native_work_packet_interface_template.md` by adding:

- `P7.2 Simplified Usage Modes`
- Usage Mode Matrix
- Field Classification Model
- Compact WorkPacket View For Documentation-Only Tasks
- Compact HarnessInputPackage View For OpenCode H0
- Compact HarnessOutputPackage View For OpenCode Summaries
- Compact Reviewer Boundary Drift Checklist
- Compact Integrator Exact-Path Checklist
- safe documentation-only governance task example
- rejected unsafe output example

## 10. Compact Mode Definition

`compact_documentation_mode` is allowed for small documentation-only governance tickets with exact target files and no product/external/runtime/tool/provider scope.

Compact mode does not weaken boundaries. Exact target files, blocked files, blocked actions, stop rules, review requirement, integration requirement, and exact-path Git advice remain mandatory.

`blocked_high_risk_mode` requires stop instead of proceeding when blocked scope appears.

## 11. Field Classification Model

Field categories added:

```text
mandatory
conditional
optional
not_applicable_with_reason
blocked
```

Mandatory WorkPacket safety fields remain mandatory. Mandatory Git-related fields remain mandatory when commit advice is expected.

`not_applicable_with_reason` is allowed only when explicit and when omission does not hide scope, target files, blocked actions, review requirements, integration requirements, or Git boundaries.

## 12. Compact WorkPacket Readiness

Compact WorkPacket readiness verdict:

```text
ready_for_P7.3_manual_documentation_or_planning_pilot
```

The compact WorkPacket includes required target files, blocked files, allowed actions, blocked actions, required context, expected output, review, integration, stop rules, success criteria, and failure criteria.

## 13. Compact HarnessInputPackage Readiness

Compact HarnessInputPackage readiness verdict:

```text
opencode_h0_input_package_ready_for_second_pilot
```

The compact package keeps OpenCode H0 user-operated only and blocks automatic dispatch and OpenCode integration.

## 14. Compact HarnessOutputPackage Readiness

Compact HarnessOutputPackage readiness verdict:

```text
opencode_h0_output_checklist_ready
```

The compact output checklist covers summary, files, commands, decisions, assumptions, blockers, limitations, deviations, recommended next ticket, and commit advice candidate.

## 15. Compact Reviewer Checklist Readiness

Compact reviewer checklist readiness verdict:

```text
reviewer_boundary_drift_checklist_ready
```

The checklist covers scope, target files, blocked files, runtime, tool, provider/API/MCP, product/external source, GBrain/Hermes/Cadence, Graphify/Codegraph, persistence/vector/graph DB, validation, security, Git mutation, `git add .`, and review-not-Git-approval boundaries.

## 16. Compact Integrator Checklist Readiness

Compact integrator checklist readiness verdict:

```text
integrator_exact_path_checklist_ready
```

The checklist requires accepted exact paths, rejected file exclusion, drift register, review verdict, commit scope matching accepted files, exact `git add` paths, no `git add .`, and preserved user final Git authority.

## 17. Example Coverage

Example coverage added:

| Example | Coverage | Boundary |
| --- | --- | --- |
| Safe Documentation-Only Governance Task | Compact WorkPacket, HarnessInputPackage, HarnessOutputPackage, reviewer verdict, integrator checklist, and exact-path CommitCandidate. | No product/source/runtime/provider/API/MCP. |
| Rejected Unsafe Output | Blocked verdict, rejected output register, no CommitCandidate, rework/governance escalation. | Rejects `git add .`, product source, provider/API/MCP, runtime, Graphify, and GBrain/Hermes/Cadence. |

## 18. Drift Reconciliation

| Drift | Status after P7.2 | Reconciliation |
| --- | --- | --- |
| P7.1-DRIFT-003: template usability must be validated in a second pilot | ready_for_validation_in_P7.3 | Compact mode and checklists are ready for second pilot validation. |
| P7.1-DRIFT-004: manual workflow overhead may be high | mitigated_by_compact_mode_pending_P7.3_validation | Compact documentation mode reduces overhead, pending pilot validation. |
| P7.1R-DRIFT-001: full canonical schema needs compact mode for small documentation tickets | resolved_by_compact_mode | Compact WorkPacket, harness, reviewer, and integrator views added. |
| P7.1R-DRIFT-002: required vs optional fields are not yet classified | resolved_by_field_classification | Field classification model added. |

Final drift verdict:

```text
no_unresolved_p7_2_blocking_drift
```

## 19. Second Pilot Readiness

Second pilot readiness verdict:

```text
P7.3_second_manual_pilot_ready_as_manual_documentation_or_planning_pilot
```

P7.3 may use `compact_documentation_mode`.

P7.3 must remain manual.

P7.3 must not activate runtime or OpenCode integration.

P7.2 does not start P7.3.

## 20. Remaining Blockers

These blockers remain active:

| Blocker | Status |
| --- | --- |
| runtime activation remains blocked | Active. |
| autonomous orchestration remains blocked | Active. |
| OpenCode integration remains blocked | Active. |
| OpenCode adapter remains blocked | Active. |
| Hermes runtime remains blocked | Active. |
| GBrain runtime remains blocked | Active. |
| Cadence remains blocked | Active. |
| MCP remains blocked | Active. |
| provider/auth/API remains blocked | Active. |
| tool execution remains blocked | Active. |
| agent execution remains blocked | Active. |
| source loading remains blocked | Active. |
| product/Siamese source inspection remains blocked | Active. |
| external source inspection remains blocked | Active. |
| Graphify rerun/adoption remains blocked | Active. |
| Codegraph execution/adoption remains blocked | Active. |
| validation/tests/CI/scripts/builds remain blocked unless future ticket explicitly allows them | Active. |
| security enforcement remains blocked | Active. |
| persistence/vector DB/graph DB remains blocked | Active. |
| generated output tracking remains blocked | Active. |
| source tracking expansion remains blocked | Active. |
| publication remains blocked | Active. |
| Git mutation by agent remains blocked | Active. |
| Cognitive Semantic System substrate selection remains blocked/deferred | Active. |

## 21. Stop Rules

STOP if P7.2 attempts to start P7.3, execute a second pilot, start P8, start P4, modify P7.1 report, modify P7.1.R audit, modify P7.0.0 or P7.0.A-H, activate runtime, activate autonomous orchestration, create automatic dispatch, create automatic reviewer assignment, create automatic integration, activate OpenCode internally, create OpenCode adapter, activate Hermes runtime, activate GBrain runtime, activate Cadence, activate MCP, activate providers/auth/API, use credentials, call APIs/network/MCP, activate tools, execute agents, load source, inspect product/Siamese source, inspect external source, inspect GBrain source, inspect raw Graphify output, rerun/adopt Graphify, execute/adopt Codegraph, run validation/tests/CI/scripts/builds, activate security enforcement, create persistence/vector DB/graph DB, track generated outputs, expand source tracking, publish, stage/commit/push, mutate Git, recommend `git add .`, or select Cognitive Semantic System substrate.

## 22. Future Validation Targets

Future validation targets, not executed by P7.2:

| Target | Purpose |
| --- | --- |
| Compact documentation mode completeness | Validate required compact fields. |
| Required/conditional/optional classification completeness | Validate all major template families. |
| `not_applicable_with_reason` safety | Confirm omissions do not hide required boundaries. |
| Compact OpenCode output checklist usability | Validate returned H0 outputs can be parsed. |
| Reviewer boundary drift checklist usability | Validate compact review catches blocked scope. |
| Integrator exact-path checklist usability | Validate exact-path commit advice and rejected-file exclusion. |
| Safe example coverage | Validate safe example remains non-product and non-runtime. |
| Unsafe example coverage | Validate unsafe example blocks `git add .` and activation requests. |
| P7.3 second pilot readiness | Validate compact mode in a second manual pilot. |

## 23. Future Hardening Candidates

Future candidates, not started:

| Candidate | Purpose |
| --- | --- |
| P7.3-PILOT-01 - Second Manual Pilot | Validate compact documentation mode. |
| P7.3-PILOT-02 - Compact Reviewer Timing Audit | Measure reviewer overhead. |
| P7.3-PILOT-03 - Compact Integrator Timing Audit | Measure integration overhead. |
| P7.3-PILOT-04 - OpenCode Output Compliance Audit | Check how well H0 outputs follow compact checklist. |
| P7.3-PILOT-05 - Unsafe Output Rejection Drill | Validate blocked output handling. |

## 24. Created / Modified / Not Created Register

Created:

- `0_architecture/governance/agent_platform_p7_2_canonical_template_simplification_hardening.md`

Modified:

- `0_architecture/governance/agent_platform_manual_agent_native_work_packet_interface_template.md`

Not created / not approved:

- no P7.3
- no P8
- no P4
- no second pilot execution
- no runtime activation
- no autonomous orchestration
- no automatic dispatch
- no automatic reviewer assignment
- no automatic integration
- no OpenCode integration
- no OpenCode adapter
- no Hermes runtime
- no GBrain runtime
- no Cadence
- no MCP
- no provider/auth/API
- no tool execution
- no agent execution
- no source loading
- no product/Siamese source inspection
- no external source inspection
- no Graphify rerun/adoption
- no Codegraph execution/adoption
- no validation execution
- no security enforcement activation
- no persistence/vector DB/graph DB
- no generated output tracking
- no source tracking expansion
- no publication
- no Git mutation
- no Cognitive Semantic System substrate selection

## 25. Final Verdict

P7.2 creates the Canonical Template Simplification / Hardening record.

P7.2 modifies the canonical manual OpenCode work packet interface template.

Compact usage modes are added.

Required/conditional/optional/not-applicable field classification is added.

Compact WorkPacket view is added.

Compact HarnessInputPackage view is added.

Compact HarnessOutputPackage view is added.

Compact Reviewer Boundary Drift Checklist is added.

Compact Integrator Exact-Path Checklist is added.

Safe documentation-only example is added.

Rejected unsafe output example is added.

P7.1-DRIFT-003 is ready for validation in P7.3.

P7.1-DRIFT-004 is mitigated by compact mode pending P7.3 validation.

```text
no_unresolved_p7_2_blocking_drift
p7_2_canonical_template_simplified_and_hardened
compact_work_packet_interface_ready_for_second_pilot
required_optional_field_classification_complete
opencode_h0_output_checklist_ready
reviewer_integrator_compact_checklists_ready
P7.3_second_manual_pilot_ready_as_manual_documentation_or_planning_pilot
```

Recommended next ticket:

P7.3 - Second Manual Pilot Using The Simplified Template
