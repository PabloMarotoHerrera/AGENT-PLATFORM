# G-18 - Graphify Semantic Curation Gate

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Graphify Semantic Curation Gate |
| Ticket | G-18 |
| Status | Accepted Graphify semantic curation gate |
| Date | 2026-07-03 |
| Scope | Semantic curation of generated Graphify evidence from the successful G-17 run for AGENT PLATFORM / Siamese parallel planning. |
| Authority | Semantic curation of generated Graphify evidence only; not architecture truth, source tracking approval, Graphify adoption, or Cognitive Semantic System substrate selection. |
| Related documents | G-15, G-16, G-17, `.graphifyignore`, `.gitignore`, Cognitive Semantic System docs. |
| Review target | `9_artifacts/graphify/graphify_missing_file_fix_20260703_120853/graphify-out/` |

## 2. Purpose
G-17 produced complete metadata with all seven approved `.py` files. G-18 semantically curates the generated graph enough to decide whether it is useful evidence for future parallel work packet planning.

G-18 does not rerun Graphify. G-18 does not treat graph output as truth. G-18 creates a curated repo-map summary because the output is useful as generated evidence, with limitations.

## 3. Evidence Boundary
Graphify output is generated evidence. Generated evidence may inform planning. Generated evidence does not decide governance. Generated evidence is not source. Generated evidence is not architecture truth. Generated evidence is not Cognitive Semantic System substrate.

## 4. Coverage Review
| Area | Curated finding |
| --- | --- |
| Processed files | Seven approved `.py` files under `3_platform/_governed_skeleton/`. |
| Generated counts | 317 nodes, 686 links, 8 analysis communities, 10 central-node entries, 2 generated surprises. |
| Docs excluded | Markdown/docs were excluded by `.graphifyignore`; no docs/papers/images were processed. |
| Architecture docs excluded | Architecture governance records were not part of this graph. |
| Code-only limitation | The graph reflects implementation skeleton shapes and local AST relationships, not full architecture intent. |

## 5. Community / Cluster Review
| Community | Likely component focus | Notable generated entities | Planning implication | Confidence | Limitation |
| --- | --- | --- | --- | --- | --- |
| 0 | Tool execution boundary helpers and validation routines. | Tool validation helpers, required-text/ref checks, tool boundary values. | Tool boundary work can be planned as its own work packet with security review hooks. | Medium | Community labels are inferred from generated IDs, not curated source review. |
| 1 | Shared status/enumeration/rationale layer across components. | Enum/str-derived status classes, rationale nodes across agent, CSS, context, provider, security, tool, validation. | Shared metadata vocabulary needs coordination across all component packets. | Medium | This may overstate coupling because Enum/str inheritance creates artificial bridges. |
| 2 | Agent runtime boundary. | AgentRuntimeBoundary, descriptors, capabilities, task envelopes, handoff records. | Agent packet can proceed in parallel but must coordinate with tool/context/security concepts. | High | Generated graph sees internal structure, not runtime readiness. |
| 3 | Cognitive Semantic System prototype. | CognitiveSemanticSystemPrototype, CognitiveEntity, SemanticClaim, SemanticRelation, SubstrateCandidateRecord. | CSS packet should remain substrate-neutral and coordinate with validation/security evidence records. | High | Does not select graph or any final substrate. |
| 4 | Provider adapter layer. | ProviderAdapterLayer, ProviderDescriptor, AdapterDescriptor, AdapterCapability, ActivationStatus. | Provider packet is separate and should stay blocked on auth/network activation gates. | High | Provider naming does not imply provider activation. |
| 5 | Context runtime. | ContextPackRuntime, ContextPack, ContextItem, ContextSourceRef. | Context packet depends conceptually on source/sensitivity and should coordinate with security/access rules. | High | Code-only graph omits architecture context policy rationale. |
| 6 | Security access enforcement. | SecurityAccessEnforcer, AccessRequest, AccessDecision, SensitivityLevel. | Security packet is a gating dependency for any future tool/provider/context activation. | High | Generated edges do not enforce policy. |
| 7 | Validation registry. | ValidationRegistry, ValidationRecord, ProofLevel, ValidationStatus. | Validation packet supports proof/evidence posture for other packets. | High | Validation evaluates; governance still decides. |

## 6. Central Node / Hub Review
| Node/entity | Why it appears central | Related component | Likely interpretation | Confidence | Limitation |
| --- | --- | --- | --- | --- | --- |
| CognitiveSemanticSystemPrototype | Highest generated centrality among named domain nodes. | Cognitive Semantic System prototype | CSS has broad internal record/registration methods and should be handled carefully. | High | Centrality is implementation shape, not substrate authority. |
| AgentRuntimeBoundary | High degree in generated analysis. | Agent runtime boundary | Agent registration, capability, task, and handoff records form a dense component. | High | No agent execution is approved. |
| ToolExecutionBoundary | High degree in generated analysis. | Tool execution boundary | Tool descriptors, requests, decisions, and capabilities are structurally rich. | High | Tool execution remains blocked. |
| ContextPackRuntime | Central generated runtime class. | Context runtime | Context pack/source/item operations are a distinct dependency surface. | High | Does not approve source loading. |
| ProviderAdapterLayer | Central after G-17 inclusion fix. | Provider adapter layer | Provider/adapter records are now represented and can be planned separately. | High | No provider/auth activation. |
| SemanticRelation and SubstrateCandidateRecord | Central internal CSS records. | Cognitive Semantic System prototype | CSS work should separate relation modeling from substrate selection. | Medium | Generated evidence only. |
| ContextItem, ToolCapabilityDescriptor, AgentCapabilityDescriptor | Repeated descriptor-style hubs. | Context, tool, agent | Capability/item records are likely work-packet boundaries. | Medium | Common dataclass shape may inflate centrality. |

## 7. Surprise / Relationship Review
| Relationship | Why it may matter | Should influence planning? | Confidence | Limitation |
| --- | --- | --- | --- | --- |
| SemanticRecordStatus inherits from `str` and bridges shared status community to CSS community. | Indicates CSS uses the same enum/string status pattern as other metadata modules. | Yes, as a consistency signal for metadata conventions. | Medium | Bridge is mostly implementation convention, not architecture dependency. |
| ActivationStatus inherits from `str` and bridges shared status community to provider adapter community. | Confirms provider activation posture is represented as metadata, not runtime activation. | Yes, for provider packet boundary language. | Medium | Does not imply provider activation. |
| Relation distribution: `calls`, `method`, `contains`, `references`, `rationale_for`, `inherits`, `indirect_call`, `imports_from`. | Graph is AST-heavy and method-structure-heavy. | Yes, use for code organization planning, not governance truth. | High | Relationship names are generated extraction categories. |

## 8. Cross-Component Dependency Review
| Component | Curated dependency signal | Planning interpretation |
| --- | --- | --- |
| Validation registry | Separate registry component with proof/status records. | Can be a parallel packet, but downstream packets should align evidence/proof status naming. |
| Security access enforcement | Distinct request/decision/sensitivity component. | Should gate any future execution, provider, context, or source-loading packet. |
| Context runtime | Distinct context pack/item/source ref component. | Can be parallel but must coordinate with security and validation boundaries. |
| Provider adapter layer | Distinct provider/adapter/capability component. | Can be parallel as metadata; activation/auth remains blocked. |
| Agent runtime boundary | Dense agent/task/capability/handoff component. | Can be parallel but depends conceptually on tool/context/security contracts. |
| Tool execution boundary | Dense tool/request/decision/capability component. | Should coordinate with security and validation before any execution upgrade. |
| Cognitive Semantic System prototype | Semantic records, relations, claims, and substrate candidates. | Can be parallel as metadata; final substrate remains deferred. |

These are generated planning signals only. They are not binding architecture decisions.

## 9. Noise / Quality Review
The graph appears useful for parallel planning because it cleanly separates the seven implementation components and shows descriptor/runtime/record clusters. It is implementation-heavy by design and under-represents architecture intent because Markdown governance docs were excluded. Shared `Enum`/`str` inheritance and repeated dataclass/helper patterns create noisy centrality and bridges.

Semantic curation should continue only as supporting evidence for a work-packet dependency map. A non-Graphify fallback remains useful for governance-level dependencies not visible in code.

## 10. Curation Verdict
`curation_useful_but_limited`

Rationale: the generated graph is complete for the seven approved Python files and useful for identifying component-local workstreams, shared metadata conventions, and planning dependencies. It is limited because it excludes architecture docs and cannot decide governance, source tracking, activation, or Cognitive Semantic System substrate.

## 11. Recommended Next Ticket
Recommended: `G-19 - Hybrid Graphify + Manual Parallel Work Packet Dependency Map`.

Conditional posture: if useful, use `G-19 - Graphify-Curated Parallel Work Packet Dependency Map`; if useful but limited, use `G-19 - Hybrid Graphify + Manual Parallel Work Packet Dependency Map`; if low-value, use `G-19 - Non-Graphify Parallel Work Packet Dependency Map`; if output quality issue, use `G-19 - Graphify Curation Quality Review`.

## 12. Created / Not Created Register
| Artifact/action | G-18 status | Reason |
| --- | --- | --- |
| curation gate document | Created | Required G-18 artifact. |
| repo map summary | Created | Required planning-safe curated summary. |
| graph output semantically curated | Completed | Generated output only. |
| Graphify rerun | Not run | Prohibited by G-18. |
| provider/auth | Not configured | Blocked. |
| `.graphifyignore` | Not modified | Blocked. |
| `.gitignore` | Not modified | Blocked. |
| generated outputs staged/tracked | Not performed | Blocked. |
| Cognitive Semantic System substrate | Not selected | Deferred. |
| G-19 | Not started | G-18 stops before G-19. |

## 13. Invariants
| ID | Invariant |
| --- | --- |
| G18-001 | Graphify Semantic Curation Gate curates generated evidence only. |
| G18-002 | Graphify output is generated evidence, not authority. |
| G18-003 | Raw graph output is not architecture truth. |
| G18-004 | Cognitive Semantic System substrate remains deferred. |
| G18-005 | Graph remains candidate only. |
| G18-006 | Graphify remains evidence only, not authority. |
| G18-007 | Validation evaluates; governance decides. |
| G18-008 | G-18 stops before G-19. |

G-18 stops here. G-19 is not started.
