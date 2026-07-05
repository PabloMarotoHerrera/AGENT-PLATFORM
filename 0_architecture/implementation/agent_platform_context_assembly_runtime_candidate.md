# Agent Platform Context Assembly Runtime Candidate

## Ticket
P5.3 context assembly runtime candidate.

## Status
Created as an inert implementation skeleton only. This record does not activate a context runtime, source loading, provider/API/MCP behavior, tool execution, agent execution, validation execution, scheduler behavior, persistence, or publication.

## Guard statements
- context inclusion is not permission
- source refs are metadata only
- no source loading
- implementation skeleton is not activation

## Scope
This candidate defines metadata-only structures for a future context assembly decision surface. It is product-independent and remains governed by the activation gate.

The skeleton can model a request, selection policy, plan, pack, source reference, item, blockers, limitations, sensitivity, classification, and decision. It cannot load source content or grant permission to use source content.

## Created files
- `3_platform/_governed_skeleton/context/__init__.py`
- `3_platform/_governed_skeleton/context/assembly.py`
- `0_architecture/implementation/agent_platform_context_assembly_runtime_candidate.md`

## Implementation surface
- `ContextAssemblyRequest`
- `ContextAssemblyPlan`
- `ContextPack`
- `ContextItem`
- `ContextSourceRef`
- `ContextSelectionPolicy`
- `ContextAssemblyDecision`
- `ContextAssemblyStatus`
- `ContextItemStatus`
- `ContextSourceClassification`
- `ContextSensitivity`
- `ContextBlocker`
- `ContextLimitation`
- `build_context_assembly_decision(request: ContextAssemblyRequest, policy: ContextSelectionPolicy) -> ContextAssemblyDecision`

## Metadata-only behavior
- Unknown sensitivity blocks inclusion when `block_unknown_sensitivity` is enabled.
- Secret, credential, and provider-auth sensitivity block inclusion when `block_secret_or_credential` is enabled.
- Product source classification blocks inclusion when `block_product_source` is enabled.
- External source content classification blocks inclusion when `block_external_source_content` is enabled.
- Generated raw output classification blocks inclusion when `block_generated_raw_output` is enabled.
- Raw Graphify output classification blocks inclusion when `block_graphify_raw_output` is enabled.
- Local-only content classification or sensitivity blocks inclusion when `block_local_only_content` is enabled.
- Safe source references can only enter a metadata-only pack when no blocker applies.
- Limitations propagate from defaults, policy, request, source ref, and item into evaluated items and decisions.

## Governance dependencies
- P3.BR activation decision reconciliation closure remains the controlling reconciliation posture.
- P3.3 tool execution activation decision remains inactive for tool execution.
- P3.4 provider/auth/API/MCP activation decision remains inactive for provider, auth, API, and MCP behavior.
- P3.5 agent runtime activation decision remains inactive for agent runtime behavior.
- P3.R, P3.0, P3.1, and P3.2 remain readiness inputs only.
- P2.KR, P2.R, P2.1, P2.2, and P2.3 remain knowledge, integration, evidence, metadata, audit, retention, and rollback inputs only.
- P1.1 through P1.5 remain contract hardening inputs only.
- P0.1 through P0.3 and the Activation Gate Charter remain gate inputs only.
- S-03 and S-04 remain security constraints only.
- Cognitive Semantic System substrate selection remains deferred.

## Pending alignment
- pending_P5.1_validation_runner_alignment
- pending_P5.2_security_policy_dry_run_alignment
- pending_P5.7_audit_retention_rollback_hooks_alignment

## Explicit non-activation
- No context runtime activation.
- No source loading.
- No product source inspection.
- No external source content inspection.
- No GBrain, Hermes, Cadence, or Graphify source adoption.
- No raw Graphify output loading.
- No secrets or credentials inspection.
- No provider, auth, API, or MCP activation.
- No tool execution.
- No agent execution.
- No scheduler or orchestration activation.
- No validation execution.
- No tests, scripts, build, lint, typecheck, CI, package-manager command, generated output tracking, source tracking expansion, publication, or Git mutation.
- No Cognitive Semantic System substrate selection.

## Boundary handling
`ContextSourceRef` is metadata-only. A source reference may identify a candidate source, classification, sensitivity, and limitations, but it is not permission to read, import, execute, transform, validate, persist, or publish source content.

Graphify evidence remains supporting generated evidence only and not authority. Raw generated output and raw Graphify output are blocked from inclusion by classification.

External sources, product sources, local-only content, secret material, credentials, and provider-auth material remain blocked or metadata-only with blockers preserved.

## Created / Not Created Register
Created:
- Metadata-only context package marker.
- Metadata-only context assembly dataclasses and enums.
- Pure metadata-only decision helper.
- P5.3 implementation record.

Not created:
- Runtime activation.
- Source loader.
- Product adapter.
- Provider/auth/API/MCP adapter.
- Tool runner.
- Agent runner.
- Scheduler or orchestrator.
- Validation runner.
- Security policy executor.
- Audit, retention, or rollback runtime hook.
- Generated artifacts.
- Tests or CI wiring.

## Final verdict
P5.3 is present as a governed, inert, metadata-only runtime candidate skeleton. It is not activated and does not expand platform permissions.
