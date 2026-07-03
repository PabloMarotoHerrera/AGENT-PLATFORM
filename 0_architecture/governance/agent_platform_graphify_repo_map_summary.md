# Graphify Repo Map Summary

## 1. Summary Header
| Field | Value |
| --- | --- |
| Title | Graphify Repo Map Summary |
| Source | G-17 Graphify output under `9_artifacts/graphify/graphify_missing_file_fix_20260703_120853/graphify-out/` |
| Status | Curated generated evidence |
| Authority posture | Not authority, not source, not architecture truth, not Cognitive Semantic System substrate. |

## 2. Input Coverage
Processed generated-output coverage includes seven `.py` files:

| Component | Processed file |
| --- | --- |
| Agent runtime boundary | `3_platform/_governed_skeleton/agents/runtime_boundary/agent_runtime_boundary.py` |
| Cognitive Semantic System prototype | `3_platform/_governed_skeleton/cognitive_semantic_system/prototype/cognitive_semantic_system_prototype.py` |
| Context runtime | `3_platform/_governed_skeleton/context/runtime/context_pack_runtime.py` |
| Provider adapter layer | `3_platform/_governed_skeleton/integrations/provider_adapter_layer/provider_adapter_layer.py` |
| Security access enforcement | `3_platform/_governed_skeleton/security/access_enforcement/security_access_enforcement.py` |
| Tool execution boundary | `3_platform/_governed_skeleton/tools/execution_boundary/tool_execution_boundary.py` |
| Validation registry | `3_platform/_governed_skeleton/validation/registry/validation_registry.py` |

Architecture Markdown, component Markdown, product source, external source, artifacts-as-input, secrets, credentials, and assistant config were excluded. The graph is therefore code-only evidence and does not include full governance rationale.

## 3. Curated Component Map
| Component | Curated signal |
| --- | --- |
| Validation registry | Separate proof/status/evidence record component; likely supports validation posture for other packets. |
| Security access enforcement | Separate access request/decision/sensitivity component; likely gates execution, provider, context, and source-loading work. |
| Context runtime | Separate context pack/item/source-ref component; likely coordinates with security and validation boundaries. |
| Provider adapter layer | Separate provider/adapter/capability metadata component; activation/auth remains blocked. |
| Agent runtime boundary | Dense agent/capability/task/handoff metadata component; should coordinate with tool/context/security concepts. |
| Tool execution boundary | Dense tool/capability/request/decision component; should coordinate with security and validation before any execution upgrade. |
| Cognitive Semantic System prototype | Semantic entity/claim/relation/substrate-candidate metadata component; substrate remains deferred. |

## 4. Curated Dependency Signals
| Signal | Planning use |
| --- | --- |
| Each major component forms a mostly distinct generated community. | Work packets can be assigned by component with limited file overlap. |
| Shared enum/status/rationale patterns bridge all components. | Define shared metadata vocabulary before broad implementation hardening. |
| Security and validation are conceptually cross-cutting even if graph edges are mostly local. | Treat security and validation as review gates for runtime/provider/tool/context work. |
| Agent and tool boundaries have high centrality. | Coordinate agent/tool packets to avoid activation or permission drift. |
| Provider adapter layer is now represented after the G-17 fix. | Provider metadata can be planned, but provider/auth activation remains separate. |
| Cognitive Semantic System prototype is central but generated evidence only. | CSS work can proceed as metadata/substrate-neutral planning, not substrate adoption. |

## 5. Parallel Work Planning Signals
| Planning question | Curated signal |
| --- | --- |
| What can be worked in parallel? | Validation registry, security access enforcement, context runtime, provider adapter layer, agent boundary, tool boundary, and CSS prototype can be planned as separate work packets. |
| What likely depends on another component? | Tool, provider, agent, and context work should depend on security and validation review before any activation. |
| Where are governance/security/validation boundaries visible? | Repeated status, blocker, limitation, evidence, validation, security, and review-required patterns appear across generated components. |
| Where should coordination happen? | Shared metadata contracts, activation statuses, evidence refs, validation refs, security refs, and review-required semantics. |
| What should not be inferred? | No runtime readiness, provider permission, source tracking approval, or Cognitive Semantic System substrate selection. |

## 6. Limitations
This is a code-only graph. It excludes architecture Markdown and therefore misses much of the accepted governance intent. It excludes product and external source. It is generated evidence only, not decision authority. Node count and centrality are not architecture quality. Shared `Enum`/`str` and dataclass/helper patterns create noise.

## 7. Recommended Use
Use this summary as supporting evidence for `G-19 - Hybrid Graphify + Manual Parallel Work Packet Dependency Map`.

Do not use it as the sole source. Do not treat it as Graphify authority. Do not use it to select Cognitive Semantic System substrate. Do not use it to approve provider/auth, OpenCode integration, product activation, repo-root broadening, source tracking, staging, or publication.
