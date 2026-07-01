# M-05 - Research Evidence Migration
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Research Evidence Migration |
| Ticket | M-05 |
| Status | Accepted research-evidence migration planning |
| Date | 2026-07-01 |
| Scope | Safe-metadata curation plan for prior research, external-reference research, provider/harness/tool evidence, and substrate evidence relevant to AGENT PLATFORM |
| Authority | Planning only; not migration execution, source copying, external adoption, provider/API/MCP activation, dependency adoption, product activation, lifecycle execution, implementation, staging, commit, push, publication, or M-06 start |
| Related documents | M-02, M-03, M-04, W-02, W-03, W-08, W-11, W-12, W-13, V-01, V-02, V-03, V-05, A-00, A-01, CSS-02, H-series, S-series |

## 2. Purpose
M-05 follows M-04 and creates a bounded planning record for research evidence that may inform later architecture, validation, external review, provider/adapter review, harness review, product/domain review, or Cognitive Semantic System substrate evaluation.
M-05 does not migrate files, inspect raw local-only sources deeply, copy research content, adopt external claims, implement anything, or start M-06.

## 3. Research Evidence Definition
Research evidence is prior or external-reference material that may support a claim, comparison, pattern, risk, hypothesis, blocker, or future review after source status, provenance, uncertainty, validation posture, security posture, and governance posture are explicit.
Research evidence is not truth, authority, dependency approval, execution approval, product activation, substrate selection, or implementation readiness.

## 4. Authority Boundary
| Layer | M-05 boundary |
| --- | --- |
| Governance | Decides promotion, adoption, execution, dependency use, product activation, lifecycle, publication, and substrate decisions. |
| Validation | Evaluates evidence readiness; V-03 and V-05 apply, but validation does not approve. |
| Evidence | Supports curated claims only when source status, scope, sensitivity, and limits are visible. |
| Security | Blocks secrets, credentials, local-only exposure, external execution, provider/API/MCP activation, network/auth use, and unsafe publication. |
| W-02 | Primary safe metadata for previous research and previous-knowledge classification. |
| W-03/W-13/V-05 | Control external-source evidence, metadata, license, execution, dependency, instruction, product, and substrate boundaries. |
| M-02/M-03/M-04 | Provide grouped safe-metadata inputs; they are not embedded or re-executed. |
| CSS-02 | Controls prior Graphify naming, authority, projection, and substrate neutrality. |
| H-series | Keeps harness/operator/tool/provider/MCP material as bounded evidence only. |
| Agents | May curate safe metadata and blockers; they cannot approve, promote, adopt, execute, or start adjacent tickets. |

## 5. Source Boundary
W-02 is the primary source metadata for prior research evidence, especially Appendix B research records and Appendix A external-reference/provider records.
M-02, M-03, and M-04 are inputs by reference only. W-03, W-13, and V-05 supply external-source handling rules. Raw `previusknowledge/`, `4_external/sources/`, `2_products/`, datasets, models, artifacts, secrets, credentials, and local-only source trees are not deeply inspected or copied.

## 6. Scope
| In scope | Out of scope |
| --- | --- |
| Safe metadata, W-02 class, source reference, evidence class, target area, allowed use, blocked use, validation posture, lifecycle posture, security posture, route, and blockers | Raw previous-knowledge content, research-note content, papers, raw external source content, product source, generated artifacts, secrets, credentials, implementation, execution, code, scripts, schemas, registries, APIs, tests, packages, adapters, providers, MCP components, migration execution, lifecycle execution, staging, commit, push |

## 7. Research Evidence Class Catalog
| Class | Meaning | Allowed handling | Blocked inference |
| --- | --- | --- | --- |
| `prior_research_external_reference` | W-02 Appendix B research metadata under `previusknowledge/research/agents/`. | Curate as evidence-only research candidates. | Current authority or adoption. |
| `provider_harness_reference` | Prior provider, coding-agent, harness, tool, runtime, or MCP research. | Revalidate through W-03/W-13/V-05/H-series before use. | Provider facts, tool policy, runtime authority. |
| `pattern_candidate_evidence` | Abstract design idea worth later review. | Restate internally after source review. | Code/source reuse or dependency approval. |
| `command_hook_skill_mcp_evidence` | Evidence about capability surfaces. | Use as risk and pattern evidence. | Activation, registry, permission, or MCP server creation. |
| `semantic_projection_evidence` | Graph/projection/substrate-related research. | Treat as candidate substrate/projection evidence. | Cognitive Semantic System naming, truth, or final substrate. |
| `product_domain_evidence` | Domain engine, SDK, or product-scope research. | Keep product-scoped until product governance exists. | Root authority or product activation. |
| `migration_rationale_evidence` | Historical rationale and audit trail. | Retain for trace and future validation. | Current governing rule. |
| `unknown_research_evidence` | Missing source status, classification, or sensitivity. | Block pending classification. | Any promotion-quality use. |

## 8. Non-Research Handling
| Source state | M-05 handling | Blocked use |
| --- | --- | --- |
| `carry_forward` | Use only through M-02/M-04 grouped safe metadata when it supports research context. | Direct promotion. |
| `conflicted` | Use only through M-03 normalized posture and CSS-02 caveats. | Current authority before normalization. |
| `scope_limit` | Product/domain evidence only. | Root authority or product activation. |
| `migration_evidence` | Historical trace only. | Governing rule by itself. |
| `external_reference` | External evidence only; W-13/V-05 controls. | Adoption, execution, dependency approval. |
| `superseded` or unknown | Historical/gap handling only. | Current authority. |

## 9. Status Model
| Status | Meaning | Next action |
| --- | --- | --- |
| `m05_evidence_candidate` | Safe metadata is relevant to research-evidence curation. | Review citations and limits. |
| `m05_ready_for_validation_review` | Source/class/status are sufficient for future V-03/V-05 review. | Validate later. |
| `m05_deferred_to_external_review` | External/provide/harness/tool fact requires W-13/V-05 review. | External review ticket. |
| `m05_deferred_to_css_substrate_review` | Substrate/projection pressure exists. | Future CSS substrate evaluation. |
| `m05_deferred_to_product_review` | Product/domain scope controls. | Product governance. |
| `m05_deferred_to_security` | Exposure/action/sensitivity uncertain. | Security review. |
| `m05_deferred_to_governance` | Promotion or accepted-use decision is missing. | Governance review. |
| `m05_blocked` | Source, citation, classification, sensitivity, or governance blocker exists. | Stop candidate use. |

## 10. Record Model
Conceptual fields: `candidate_id`, source reference, W-02 class or external status, safe label, evidence class, target area, allowed use, blocked use, validation posture, lifecycle posture, security/local-only posture, CSS caveat, product/external caveat, blocker, route, reviewer/date, and stop rule.
This is not a schema, registry, database, file format, API, script, or implementation.

## 11. Input Summary
| Input | M-05 use |
| --- | --- |
| W-02 | Primary classification metadata; 237 files classified, including 13 research records as `external_reference`. |
| M-02 | Seven grouped `carry_forward` records; useful context only, not embedded content. |
| M-03 | Six grouped `conflicted` records; normalization caveats for semantic and representation evidence. |
| M-04 | Material map for agent/context/runtime/provider/adapter/workflow/tool/MCP evidence. |
| W-03/W-13/V-05 | External source evidence, license, runtime, dependency, instruction, product, and substrate validation boundaries. |
| A-00/A-01 | Retention/lifecycle language only; no lifecycle state applied. |
| CSS-02 | Current naming, rejected prior Graphify wording, substrate neutrality, projection-as-evidence rules. |
| H-series/S-series | Harness/operator/tool/provider/MCP, local-only, execution, secret, credential, network, provider, and Git stop rules. |

## 12. W-02 Research Document Catalog
W-02 Appendix B classifies 13 prior research documents as `external_reference`; M-05 retains only safe metadata.
| Candidate | Source reference / safe label | W-02 class | Handling |
| --- | --- | --- | --- |
| M05-RE-001 | W-02 lines 580-582, ECC agent/architecture/Codex integration research | `external_reference` | External harness evidence only. |
| M05-RE-002 | W-02 lines 583-585, ECC commands/hooks/MCP research | `external_reference` | Capability-surface evidence only. |
| M05-RE-003 | W-02 line 586, ECC memory research | `external_reference` | Memory-as-evidence review input only. |
| M05-RE-004 | W-02 line 587, ECC OpenCode integration research | `external_reference` | Provider/harness integration evidence only. |
| M05-RE-005 | W-02 line 588, ECC reusable patterns | `external_reference` | Pattern candidate evidence only. |
| M05-RE-006 | W-02 lines 589-590, ECC schemas and skills research | `external_reference` | Schema/skill evidence only; no registry or schema adoption. |
| M05-RE-007 | W-02 line 591, ECC strategic conclusions | `external_reference` | Strategic evidence only. |
| M05-RE-008 | W-02 line 592, ECC vs graphify comparison | `external_reference` | External comparison evidence; neutralize naming if reused. |

## 13. Architecture External-Reference Inputs
M-04 groups prior architecture `external_reference` records as M04-MAT-008, covering W-02 provider, harness, MCP, memory, tool, OpenCode, Codex, Claude, Cursor, Hermes, and ECC evidence.
M-05 may cite M04-MAT-008 as safe metadata for future research curation, but any provider, tool, runtime, or harness fact must be revalidated before use.

## 14. Carry-Forward Context Inputs
| Input | M-05 use | Blocked inference |
| --- | --- | --- |
| M02-CF-001 | Adapter mediation, governance, security, validation vocabulary as research context. | Adapter implementation or provider adoption. |
| M02-CF-003 | Context selection, lifecycle, sensitivity, retrieval, validation, and governance context. | Context-pack generator or permission. |
| M02-CF-006 | Source-of-truth, ownership, governance, platform principles, and scalability context. | Governance approval by evidence. |
| M02-CF-007 | Knowledge-boundary concepts for Cognitive Semantic System research context. | Substrate decision. |

## 15. Conflicted-Normalization Context Inputs
| Input | M-05 use | Blocked inference |
| --- | --- | --- |
| M03-CS-003 | Substrate, ontology, metamodel, node, and relationship material as candidate evidence. | Final graph substrate. |
| M03-CS-005 | API, projection, repository, integration, runtime, and engine ideas as bounded research evidence. | API/runtime implementation. |
| M03-CS-006 | Agent, command, dependency, adapter, hook, MCP, memory, repository, skill, ticket, tool, and workflow representations as neutral candidates. | Tool/MCP/permission adoption. |

## 16. M-04 Planning Inputs
M-04 keeps agent, context, runtime, provider, adapter, workflow, tool, command, hook, skill, MCP, and representation material as migration-planning evidence.
M-05 uses M-04 for grouping only: M04-MAT-006 and M04-MAT-007 feed implementation-adjacent research cautions; M04-MAT-008 feeds external/provider/harness evidence; none authorize implementation, activation, adoption, or migration execution.

## 17. External Source Boundary
External source presence is not adoption. W-03 classifies all 12 external sources as not promoted external evidence. W-13 keeps all current sources observed, classified external references, local-only, not promoted, execution-blocked, dependency-blocked, and instruction-blocked.
V-05 validates external-source readiness but does not approve execution, dependency adoption, source reuse, product dependency adoption, active instructions, source copying, or substrate decisions.

## 18. Cognitive Semantic System Boundary
The accepted current name is `Cognitive Semantic System`.
`Platform Graphify`, `Graphify Authority`, and `Graphify owns truth` may appear only as rejected, prohibited, historical, or candidate-evidence context. Graph, graph databases, graph reports, and graph projections remain candidate evidence only; graph is not selected as final substrate, source of truth, validation authority, governance authority, or implementation prerequisite.

## 19. Product And Domain Boundary
Product/domain evidence remains product-scoped unless governance creates a declared product scope, owner, validation baseline, security posture, Git posture, and root-boundary statement.
EnergyPlus/OpenStudio-style domain evidence, product research, and product-generated outputs cannot define AGENT PLATFORM root authority or activate products.

## 20. Harness, Tool, Command, Skill, Hook, And MCP Boundary
Harness and operator-tool evidence may inform future architecture only as bounded evidence. Tool availability is not permission; shell availability is not command approval; provider credentials are not provider permission; MCP availability is not MCP activation; package-manager availability is not dependency approval.
M-05 creates no harness runtime, command, hook, skill registry, tool policy, MCP server, provider adapter, or package/dependency registry.

## 21. Validation And Proof Posture
Default M-05 proof posture is PL-1 for path/status checks, PL-2 for source classification and sensitivity, PL-3 for citation/provenance review, and PL-4 for later coherence or external review.
No proof level approves research adoption, migration execution, implementation, provider/API/MCP activation, dependency adoption, product activation, publication, Git action, or substrate decision.

## 22. Lifecycle And Retention Posture
Default lifecycle posture for M-05 candidates is `retain_migration_context`, `retain_safe_metadata_only`, `retain_external_reference`, and `retain_historical_trace` where applicable.
A-00/A-01 lifecycle states are not applied. No archive, supersession, deprecation, retention execution, movement, deletion, or archive storage is created.

## 23. Git And Publication Boundary
Git state is artifact evidence only. M-05 does not stage, commit, push, force-add, amend, reset, clean, publish, or treat Git history as truth.
Local-only staged material, secret/credential staged material, or broad staging would be a stop condition.

## 24. Research Evidence Planning Table
| Candidate | Source reference | Evidence class | Target area | Allowed use | Blocker / next action |
| --- | --- | --- | --- | --- | --- |
| M05-PLAN-001 | M05-RE-001 to M05-RE-008 | `prior_research_external_reference` | harness/agents/context | Future research review and pattern comparison. | Revalidate; no raw content copy. |
| M05-PLAN-002 | M04-MAT-008 | `provider_harness_reference` | provider/adapter/harness | External/provider evidence routing. | W-13/V-05 review before facts are used. |
| M05-PLAN-003 | M03-CS-003; CSS-02 | `semantic_projection_evidence` | Cognitive Semantic System | Candidate substrate/projection evidence. | Future substrate evaluation; no graph decision. |
| M05-PLAN-004 | M03-CS-005; M04-MAT-006 | `pattern_candidate_evidence` | runtime/API/projection | Implementation-adjacent research cautions. | No API/runtime/schema/engine implementation. |
| M05-PLAN-005 | M02-CF-001; M04-MAT-001 | `pattern_candidate_evidence` | adapter/provider | Adapter mediation and validation context. | No adapter code or provider adoption. |
| M05-PLAN-006 | M02-CF-003; M04-MAT-003 | `migration_rationale_evidence` | context/retrieval | Context selection and lifecycle research context. | No context generator or permission grant. |
| M05-PLAN-007 | M02-CF-006; W-11/V-02 | `migration_rationale_evidence` | governance/validation | Evidence-to-claim-to-decision framing. | Governance decision still required. |
| M05-PLAN-008 | W-03/W-13/V-05 graphify source posture | `semantic_projection_evidence` | external/CSS | External projection source as candidate evidence. | No source name, dependency, execution, or substrate adoption. |
| M05-PLAN-009 | W-03/W-12/W-13 domain source posture | `product_domain_evidence` | product/domain | Domain evidence retained for future product review. | Product scope/governance absent. |

## 25. Target Grouping
| Target area | Candidate inputs | Target posture |
| --- | --- | --- |
| Research evidence index later | M05-RE-001 to M05-RE-008 | Future reviewed metadata only. |
| Agent/harness architecture | M05-PLAN-001, M05-PLAN-002 | Pattern evidence, not runtime. |
| Context/session/privacy | M05-PLAN-001, M05-PLAN-006 | Evidence for later context review. |
| Provider/adapter architecture | M05-PLAN-002, M05-PLAN-005 | Provider-neutral review only. |
| Runtime/tool/MCP boundary | M05-PLAN-004 | Security/governance blocker evidence. |
| Cognitive Semantic System | M05-PLAN-003, M05-PLAN-008 | Substrate-neutral evidence only. |
| Product/domain review | M05-PLAN-009 | Product-scoped future review only. |
| Governance/validation | M05-PLAN-007 | Evidence lifecycle and promotion context. |

## 26. Citation Rules
Future research restatement must cite W-02 source reference and classification, M-02/M-03/M-04 grouped candidate when applicable, W-03/W-13/V-05 for external posture, W-08/V-03 for migration posture, W-11 for governance, S-series for security/access, CSS-02 for naming/substrate, and H-series for harness/tool/MCP posture.
Citation is provenance, not truth. Missing source reference, stale external fact, missing sensitivity posture, missing review limits, or missing governance path blocks promotion-quality use.

## 27. Allowed Future Outputs
After explicit future instruction, M-05 candidates may support reviewed research summaries, evidence packs, external-source review records, substrate-evaluation inputs, provider/adapter/harness pattern reviews, product/domain research notes, or governance decision inputs.
Those future outputs must remain scoped, cited, validation-backed, security-reviewed, and governance-bound. M-05 creates none of them.

## 28. Blocker Register
| Blocker | Stop behavior | Required action |
| --- | --- | --- |
| Missing W-02 classification or source reference | Stop candidate use. | Classify or cite safe metadata. |
| Raw content required | Stop curation. | Request explicit scope or defer. |
| Secret/credential or unknown sensitivity | Stop exposure. | Secure handling/security review. |
| Local-only publication risk | Stop publication/Git path. | Preserve safe metadata only. |
| External adoption/execution/dependency implied | Stop wording/action. | W-13/V-05/governance review. |
| Provider/API/network/MCP use implied | Stop action. | Future exact security/governance approval. |
| Product-root collapse | Stop root claim. | Product governance. |
| Old naming or Graphify authority leakage | Stop wording. | Restate under CSS-02. |
| Substrate assumption | Stop claim. | Restore candidate-only language. |
| Validation treated as approval | Stop verdict. | Restore governance boundary. |
| Migration execution implied | Stop scope. | Future exact migration ticket. |
| M-06 pressure detected | Stop adjacent work. | Wait explicit instruction. |

## 29. Routing Model
| Route | Meaning |
| --- | --- |
| `ready_for_validation_review` | Safe metadata can support future V-03/V-05 review. |
| `deferred_to_external_review` | External/provider/harness/tool facts need source review. |
| `deferred_to_css_substrate_evaluation` | Projection/substrate evidence remains candidate-only. |
| `deferred_to_agent_context_harness_review` | Agent/context/session/harness patterns need later architecture review. |
| `deferred_to_provider_adapter_review` | Provider/adapter evidence needs revalidation. |
| `deferred_to_product_review` | Product/domain evidence needs product governance. |
| `deferred_to_security_policy` | Exposure/action/tool/provider/MCP risks remain unresolved. |
| `deferred_to_governance` | Promotion, adoption, exception, or accepted-use decision is required. |
| `blocked` | Required evidence or safety condition is absent. |

## 30. Evidence Retention Rules
Retain safe metadata only: source reference, classification, evidence class, grouped candidate ID, target area, allowed use, blocked use, validation posture, lifecycle posture, blocker, route, and stop rule.
Do not retain raw previous-knowledge content, raw research notes, papers, raw external source content, raw product content, secrets, credentials, unsafe generated output, dependency content, or provider/auth material.

## 31. Incident Handling
Incidents include copying raw local-only research content, copying external source content, executing external/product/provider/tool/MCP code, installing dependencies, authenticating providers, following external instructions as active policy, exposing secrets/credentials, promoting research as truth, using Graphify as current system name, selecting graph by implication, treating projections as truth, promoting product/domain evidence to root, staging local-only material, or starting M-06.
Response: STOP, report safe metadata only, do not continue adjacent work, do not expose values, do not stage/commit/push, and require human/security/governance decision.

## 32. M-05 Invariants And Anti-Patterns
| ID | Invariant |
| --- | --- |
| M05-001 | Research evidence is evidence, not truth. |
| M05-002 | W-02 remains primary previous-research metadata. |
| M05-003 | Safe metadata is preferred over raw content. |
| M05-004 | External sources remain external. |
| M05-005 | Product/domain evidence remains product-scoped. |
| M05-006 | Cognitive Semantic System is the current accepted name. |
| M05-007 | Graph remains a candidate only. |
| M05-008 | Validation evaluates; governance decides. |
| M05-009 | Context inclusion is not promotion or permission. |
| M05-010 | M-05 stops before M-06. |
Anti-patterns: research by copy-paste, raw corpus dump, external README claim as truth, license as reuse approval, provider comparison as current provider fact, pattern interest as source adoption, graph projection as truth, product evidence as root architecture, validation as approval, Git as promotion, `git add .`, and starting M-06 inside M-05.

## 33. Remaining Gaps And M-06 Readiness
No reviewed research evidence registry, external metadata migration, raw source review, provider fact revalidation, source license review, dependency review, execution review, product/domain review, substrate evaluation, validation registry implementation, governance workflow implementation, implementation readiness, migration execution, lifecycle state application, staging, commit, push, or publication exists.
M-06 - External Metadata Migration is ready only after explicit future instruction and only as metadata-curation planning. It must not copy external source code, run external code, install dependencies, authenticate, activate providers/APIs/MCP, adopt dependencies, activate products, decide substrate, stage, commit, push, or publish.

## 34. Final Verdict
| Question | Answer |
| --- | --- |
| What does M-05 create? | One safe-metadata research-evidence migration-planning document. |
| Did M-05 inspect raw previous knowledge, external sources, or product folders deeply? | No. |
| Did M-05 copy prior research, papers, raw external source, or product content? | No. Safe metadata only. |
| Did M-05 migrate, implement, execute, adopt, activate, archive, or apply lifecycle states? | No. |
| Is the Cognitive Semantic System substrate selected? | No. Graph remains a candidate only. |
| Are providers, tools, MCP, APIs, networks, packages, products, or external sources adopted? | No. |
| What remains blocked? | Migration execution, raw content copying, implementation, lifecycle execution, product activation, external adoption, provider/API/MCP activation, dependency adoption, publication, staging, commit, push, and M-06. |
Final M-05 statement:
```text
M-05 curates research evidence as safe metadata and grouped planning records only.
It stops before migration execution, raw-source review, implementation, adoption,
activation, lifecycle action, publication, Git actions, and M-06.
```
