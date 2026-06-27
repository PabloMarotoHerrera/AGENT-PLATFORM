# Agent Platform Previous Knowledge Classification Index

Status: canonical workspace classification index  
Ticket: W-02 - Previous Knowledge Classification Index  
Scope: semantic knowledge inventory and file-level migration classification for `previusknowledge/` markdown files  
Date: 2026-06-27

## 1. Purpose

This document maps the knowledge contained in `previusknowledge/` into canonical domains, principles, models, taxonomies, decisions, readiness posture, and conceptual gaps. It also preserves the file-level classification for every markdown file under `previusknowledge/` as supporting evidence.

It does not move files, delete files, edit previous documents, create W0, implement code, stage changes, commit, or push.

This index uses the W-01 vocabulary correction: the neutral working name for the future semantic authority is `Cognitive Semantic System`. Prior Graphify-labeled documents remain migration evidence and candidate-substrate input. They do not name the future system, and they do not decide that the final cognitive substrate must be graph-based.

W-02 revision rule:

```text
Agents navigate knowledge, not filenames.

The file inventory is retained for traceability, but the primary W-02 artifact is
the semantic inventory of domains, principles, models, taxonomies, decisions,
dependencies, readiness, and conceptual gaps.
```

## 2. Classification States

| State | Meaning |
| --- | --- |
| `carry_forward` | Principle or conceptual model remains useful for AGENT PLATFORM after restatement in current workspace architecture. |
| `scope_limit` | Useful only inside a product workspace, domain workspace, or bounded scope; not root workspace authority. |
| `migration_evidence` | Useful for history, rationale, sequencing, or comparison; not current authority. |
| `conflicted` | Contains naming, scope, authority, roadmap, or substrate assumptions that must be normalized before promotion. |
| `superseded` | Replaced by newer current authority after explicit decision. No file is assigned this state in W-02. |
| `external_reference` | Prior notes about external providers, tools, or harnesses; useful evidence without internal authority. |

## 3. Completeness Summary

| Group | Count |
| --- | ---: |
| Architecture documents classified | 224 |
| Research documents classified | 13 |
| Total previous markdown files classified | 237 |

Semantic inventory coverage:

| Inventory | Coverage |
| --- | --- |
| Canonical knowledge domains | Workspace, Cognitive Semantic System, cognitive substrate evaluation, architecture, agent, context, runtime, provider, adapter, workflow, product, knowledge, operations, security/access, governance, validation, research, external sources. |
| Canonical principle inventory | Workspace authority, evidence, approval, product independence, context, agents, providers, adapters, runtime, governance, validation, security, generated output, memory, skills, commands, hooks, MCP, planning, and cognitive substrate constraints. |
| Canonical model inventory | Workspace, authority, source-of-truth, semantic authority, cognitive substrate, agent, context, adapter, provider, workflow, runtime, governance, validation, security/access, knowledge, product, external source, operations, and taxonomy models. |
| Canonical taxonomy inventory | 23 explicit taxonomy documents plus ontology and metamodel candidate structures. |
| ADR inventory | 2 architectural decisions identified and semantically reclassified. |

| State | Count |
| --- | ---: |
| `carry_forward` | 91 |
| `scope_limit` | 45 |
| `migration_evidence` | 9 |
| `conflicted` | 44 |
| `external_reference` | 48 |
| `superseded` | 0 |
| Total | 237 |

## 4. Classification Rules

| Rule | Application |
| --- | --- |
| Previous `Status: canonical` labels are historical evidence only. | They do not automatically create AGENT PLATFORM root authority. |
| `carry_forward` requires restatement. | A previous document can inform current architecture only after being reframed in current workspace terms. |
| Product material is scope-limited. | Product and Digital Twin architecture can inform future product workspaces but cannot define root authority. |
| Prior Graphify-labeled material is conflicted. | It may contain strong semantic-authority ideas, but naming and substrate assumptions require a naming ADR and substrate evaluation. |
| Provider and harness studies are external references. | They inform adapters, providers, runtime posture, and risk analysis but do not define the platform. |
| Folder paths are not authority. | File location helps inventory but does not decide truth, lifecycle, ownership, or promotion. |

## 5. Canonical Knowledge Domains

The following domains are the conceptual domains hidden across the previous corpus. They are not folder names and they are not implementation modules.

| Domain | Current maturity | Current authority | Main source documents | Migration priority |
| --- | --- | --- | --- | --- |
| Workspace | Established at charter level. | Current authority lives in `agent_platform_workspace_charter.md`; prior repository/workspace material is evidence. | `repository_vision.md`, `repository_principles.md`, `source_of_truth_strategy.md`, `macrofolder_architecture.md`, `cross_layer_rules.md`, W-00, W-01. | Highest; workspace meaning controls all later migration. |
| Cognitive Semantic System | Conceptual and conflicted. | Neutral name is current W-01 authority; prior Graphify-labeled semantic-authority material is candidate evidence. | `graphify_canonical_semantic_model.md`, `graphify_semantic_authority_architecture.md`, `graphify_system_of_record.md`, `graphify_ontology.md`, `graphify_metamodel.md`, ADR files. | Highest; naming and authority boundary must stay neutral until ADR. |
| Cognitive substrate evaluation | Research-ready but undecided. | No final substrate authority. Graph is a strong candidate, not a decision. | `adr_002_why_graph.md`, `graphify_graph_database_strategy.md`, `graphify_metamodel.md`, `graphify_ontology.md`, external `graphify` review in W-00. | Highest for any semantic-system implementation; not a blocker for W-03. |
| Architecture | Mature prior corpus with current restatement required. | Current authority only after restatement in `0_architecture/workspace/`. | Final syntheses, foundations docs, `repository_principles.md`, `source_of_truth_strategy.md`, W-00, W-01. | High; all reusable concepts depend on current-scope restatement. |
| Agent | Mature conceptual architecture. | Carry-forward candidate; W-01 already canonicalizes agents as roles, not truth owners. | `agent_architecture_final_synthesis.md`, agent foundations, boundary, autonomy, execution, handoff, coordination, governance, security, taxonomy docs. | High; agents are primary workspace consumers and operators. |
| Context | Mature conceptual architecture. | Carry-forward candidate; W-01 already canonicalizes context as bounded exposure. | `context_architecture_final_synthesis.md`, context foundations, authority, lifecycle, selection, retrieval, assembly, taxonomy, governance, validation, security docs. | High; context packs are required for agent-native operation. |
| Runtime | Mature posture model, no implementation. | Carry-forward candidate; W-01 canonicalizes runtime as mediation/posture, not authority. | `runtime_final_synthesis.md`, `platform_runtime_foundations.md`, `execution_runtime.md`, `capability_exposure_runtime.md`, workflow runtime docs. | High; must stay implementation-independent. |
| Provider | Mature conceptual architecture. | Carry-forward candidate; providers remain external. | `provider_final_synthesis.md`, `provider_foundations.md`, `provider_taxonomy.md`, provider abstraction, capability, governance docs. | High; external systems and harnesses depend on provider neutrality. |
| Adapter | Mature conceptual architecture. | Carry-forward candidate; adapters mediate without authority transfer. | `adapter_final_synthesis.md`, `adapter_architecture_final_synthesis.md`, adapter foundations, boundary, capability, taxonomy, governance, security, validation docs. | High; provider-facing work depends on this boundary. |
| Workflow | Mature posture model, no engine. | Carry-forward candidate; workflow owns coordination posture only. | `workflow_final_synthesis.md`, `workflow_foundations.md`, `workflow_runtime.md`, `workflow_coordination.md`, `workflow_execution.md`. | Medium-high; useful after context/provider/adapter boundaries stay stable. |
| Product | Mature but scope-limited. | Product-scope candidate only; not root workspace authority. | Product final syntheses, product component/structure/realization docs, `repository_vision.md`. | Medium; promote only after product workspace boundaries exist. |
| Knowledge | Partial conceptual model. | Carry-forward candidate; knowledge is reviewed durable material, not truth by default. | `knowledge_layer.md`, `source_of_truth_strategy.md`, `product_knowledge_architecture.md`, `graphify_knowledge_research_coherence_audit.md`, W-00. | High; needed for semantic reuse and agent context selection. |
| Operations | Partial and mostly historical. | Migration evidence until current operations evidence model exists. | `operations_layer.md`, runtime docs, source-of-truth strategy, provider-specific reviews. | Medium; required before runtime/output evidence becomes durable. |
| Security/Access | Mature as constraints but no current policy. | W-01 has canonical constraint posture; prior detailed docs are carry-forward candidates. | Agent, context, adapter security docs; provider-specific GSV reviews; `governance_layer.md`; W-01. | High; agent-native workspace cannot expose context/tools safely without it. |
| Governance | Mature conceptual architecture but no current workflow. | W-01 canonicalizes governance as decision authority; detailed prior docs are carry-forward candidates. | `governance_layer.md`, agent/context/adapter/provider governance docs, semantic authority docs, source-of-truth strategy. | High; promotion, approval, and exception paths depend on it. |
| Validation | Mature conceptual architecture but no current registry. | W-01 canonicalizes validation as evidence and validity posture, not approval. | Context validation, adapter validation, semantic validation docs, provider validation mappings, source-of-truth strategy. | High; authority promotion requires validation evidence. |
| Research | Evidence-only. | No current authority unless promoted. | `previusknowledge/research/agents/`, external source reviews in W-00. | Medium; mine for patterns after provenance and scope are clear. |
| External Sources | Evidence-only. | W-00 and W-01 classify external sources as references only. | `4_external/sources/`, W-00 source review, provider-specific reviews, ECC research. | High for the next external registry, but no registry is created in this revision. |

Domain rule:

```text
A domain becomes canonical only when its meaning, authority boundary, dependencies,
and promotion path are expressed in current workspace architecture. Prior documents
can provide concepts, but they do not become root authority by file existence.
```

## 6. Canonical Principle Inventory

Principles are classified independently of document filenames.

| Principle | Status | Knowledge carried forward | Main evidence | Required handling |
| --- | --- | --- | --- | --- |
| Agent-native cognitive organization beats folder-first organization. | Canonical | Optimize for how agents reason, retrieve, relate, validate, evolve, and coordinate knowledge. | W-01, W-00, context and semantic authority docs. | Preserve as workspace design constraint. |
| Files are artifacts. | Canonical | Files carry content, source, evidence, or projections; path does not create truth. | `source_of_truth_strategy.md`, W-00, W-01. | Use in all migration and context rules. |
| Evidence is not truth. | Canonical | Evidence requires provenance, validation posture, governance posture, and promotion. | `source_of_truth_strategy.md`, semantic authority docs, W-01. | Preserve as authority-transition invariant. |
| Human approval gates commits and pushes. | Canonical | Repository history and publication remain human-governed unless policy changes. | `repository_principles.md`, `source_of_truth_strategy.md`, W-00. | Preserve as operational governance rule. |
| Product independence. | Canonical | Product workspaces do not define AGENT PLATFORM root authority by default. | `repository_vision.md`, product docs, W-00, W-01. | Scope product docs before promotion. |
| Context is bounded exposure. | Canonical | Context is selected, traceable, governed, security-constrained, and non-authoritative by default. | Context final synthesis, W-01. | Promote into context-pack strategy later. |
| Context is selected, not dumped. | Canonical | Context packages should be task-scoped by authority, freshness, sensitivity, lineage, and budget. | Context architecture docs, W-00, W-01. | Preserve for agent workflows. |
| Agents are roles. | Canonical | Agents reason, plan, execute permitted work, and produce evidence; they do not own truth. | Agent final synthesis, W-00, W-01. | Preserve for agent permission model. |
| Agent output is evidence. | Canonical | Summaries, plans, recommendations, and generated docs need validation and governance before becoming durable truth. | Agent docs, source-of-truth strategy, W-01. | Preserve for all agent-generated artifacts. |
| External sources remain external. | Canonical | Proximity under `4_external/sources/` does not promote an external source. | W-00, W-01, source-of-truth strategy. | Preserve for external registry. |
| Provider neutrality. | Canonical | Provider APIs, SDKs, tools, outputs, and behavior must not become platform architecture. | Provider final synthesis, adapter docs, W-01. | Preserve before provider-specific work. |
| Runtime does not own truth. | Canonical | Runtime hosts, mediates, exposes posture, and records trace; it does not approve, validate, govern, or own truth. | Runtime final synthesis, agent/context/workflow runtime docs, W-01. | Preserve in runtime implementation planning. |
| Adapters mediate providers. | Canonical | Adapters translate, project, prepare, expose, classify, and coordinate posture without authority transfer. | Adapter final synthesis, W-01. | Preserve in provider-facing work. |
| Governance decides. | Canonical | Approval, promotion, exceptions, policy, lifecycle, and ownership decisions require governance authority. | Governance docs, source-of-truth strategy, W-01. | Requires current governance workflow. |
| Validation evaluates. | Canonical | Validation provides evidence and validity posture; it does not approve or promote truth. | Validation docs, context synthesis, W-01. | Requires current validation registry. |
| Security/Access constrains exposure and action. | Canonical | Sensitivity, trust, permission, secret handling, and provider/tool exposure constrain all work. | Security docs, W-01. | Requires current access policy. |
| Generated output is not source by default. | Canonical | Generated graphs, reports, logs, context packs, exports, and runtime outputs require promotion to become source. | Source-of-truth strategy, W-00, W-01. | Preserve for outputs and external graphify projections. |
| Memory is governed evidence. | Canonical at principle level | Memory requires provenance, confidence, sensitivity, lifecycle, and promotion state. | Source-of-truth strategy, agent/context memory docs. | Detailed memory model still needs current design. |
| Skills are reusable capabilities. | Candidate | Skills package repeatable behavior but do not become authority by text alone. | Source-of-truth strategy, ECC research, external sources. | Needs skill identity, lifecycle, permission, and registry policy. |
| Commands are entrypoints. | Candidate | Commands trigger workflows or capabilities; commands are not architecture by themselves. | Source-of-truth strategy, ECC research. | Needs command boundary model if used. |
| Hooks observe and guard. | Candidate | Hooks may observe or enforce within declared boundaries but must not hide policy. | Source-of-truth strategy, ECC research. | Needs hook policy and audit model if used. |
| MCP is opt-in. | Candidate | MCP exposes external tool surfaces requiring explicit scope, risk, and provenance. | Source-of-truth strategy, ECC research, external source review. | Needs MCP/tool access policy. |
| Plan before build. | Canonical | Architecture and migration decisions precede implementation and restructuring. | W-00, W-01, source-of-truth strategy. | Preserve across W-series. |
| Cognitive substrate remains undecided. | Canonical | Graph is a strong candidate, but final representation may be graph, another complex-system organization, or hybrid. | W-01 clarification, ADR-002 as historical candidate evidence. | Blocks implementation decisions, not external registry work. |
| Prior Graphify naming as future-system name. | Conflicting | Prior documents used Graphify as semantic authority naming. | Prior Graphify-labeled architecture and ADR files. | Do not carry forward as current name; use `Cognitive Semantic System` until naming ADR. |

Principle rule:

```text
Canonical principles may govern future work now. Candidate principles require
current workspace restatement before they govern implementation. Conflicting
principles preserve evidence but block direct promotion.
```

## 7. Canonical Model Inventory

| Model | Decision | Current maturity | Main source knowledge | Required handling |
| --- | --- | --- | --- | --- |
| Workspace Model | Carry forward | Current charter-level model exists. | W-01, W-00, repository principles, macrofolder and ownership material. | Continue as root cognitive workspace model. |
| Authority Model | Merge | Strong but distributed. | Source-of-truth strategy, semantic authority docs, W-01 authority model. | Merge into one current authority architecture later. |
| Source-of-Truth and Promotion Model | Carry forward | Mature conceptual model. | `source_of_truth_strategy.md`, W-00, W-01. | Preserve evidence-to-truth transition. |
| Cognitive Semantic System Model | Rewrite | Strong semantic authority concepts, conflicted naming/substrate. | Graphify-labeled semantic model, authority, system-of-record, ontology, metamodel, storage, sync, projection docs. | Rewrite under neutral name and undecided substrate. |
| Cognitive Substrate Model | Rewrite | Rich graph argument exists, but final substrate undecided. | ADR-002, graph database strategy, metamodel, ontology, external graphify review. | Treat graph as candidate; evaluate alternatives and hybrids before implementation. |
| Agent Model | Carry forward | Mature conceptual model. | Agent final synthesis, foundations, boundaries, autonomy, decision, execution, handoff, coordination, approval, security docs. | Restate with neutral semantic authority naming. |
| Context Model | Carry forward | Mature conceptual model. | Context final synthesis, foundations, authority, lifecycle, taxonomy, retrieval, assembly, selection, governance, validation, security docs. | Convert into current context-pack strategy later. |
| Adapter Model | Carry forward | Mature provider-facing model. | Adapter final synthesis, boundary, capability, taxonomy, governance, security, validation docs. | Preserve provider-neutral mediation. |
| Provider Model | Carry forward | Mature provider-neutral model. | Provider final synthesis, foundations, taxonomy, abstraction, capability, governance docs. | Revalidate provider-specific facts before use. |
| Workflow Model | Carry forward | Mature posture model. | Workflow final synthesis, foundations, runtime, coordination, execution docs. | Keep as coordination posture, not engine design. |
| Runtime Model | Carry forward | Mature posture model. | Runtime final synthesis, platform runtime, execution runtime, capability exposure runtime docs. | Keep implementation-independent until runtime ticket. |
| Governance Model | Merge | Mature concepts, no current process. | Governance layer, governance docs across agent/context/adapter/provider, source-of-truth strategy. | Merge into current governance workflow later. |
| Validation Model | Merge | Mature concepts, no current registry. | Context validation, adapter validation, semantic validation docs, provider validation mappings. | Merge into validation registry later. |
| Security/Access Model | Merge | Strong constraints, no current policy. | Agent/context/adapter security docs, provider GSV reviews, W-01. | Merge into current access policy later. |
| Knowledge Model | Merge | Partial and distributed. | Knowledge layer, source-of-truth strategy, product knowledge, semantic coherence audit. | Define how durable knowledge, context, evidence, and authority interact. |
| Product Model | Rewrite | Mature old product architecture, root-conflicting. | Product final syntheses, product structure/component/realization docs, repository vision. | Scope-limit to future product workspaces. |
| External Source Model | Rewrite | Evidence posture exists, registry absent. | W-00 external review, provider reviews, external source directories. | External registry can be created after explicit instruction. |
| Operations Model | Rewrite | Historical and partial. | Operations layer, runtime and source-of-truth output/evidence concepts. | Define operations evidence and lifecycle later. |
| Taxonomy Model | Merge | Multiple mature taxonomies, inconsistent scope. | Agent, context, adapter, provider, product, entity, ontology, metamodel docs. | Create current taxonomy reconciliation before relying on types. |

Model rule:

```text
Carry-forward models can inform current architecture. Merge models require a new
workspace-level consolidation. Rewrite models contain valuable concepts but cannot
be promoted without scope, naming, or substrate correction. Archive is not used by
W-02 because no knowledge is discarded.
```

## 8. Canonical Taxonomy Inventory

The previous corpus contains 23 explicit taxonomy documents plus two candidate cognitive-structure documents that behave like taxonomy foundations: ontology and metamodel.

| Taxonomy or structure | Current maturity | Dependencies | Remains valid? |
| --- | --- | --- | --- |
| Agent Taxonomy Dimensions | Mature prior taxonomy. | Agent foundations, boundaries, autonomy, permission, context, memory. | Valid as candidate; requires current workspace restatement. |
| Agent Capability Taxonomy | Mature prior taxonomy. | Agent model and permission/security model. | Valid as candidate; needs permission policy alignment. |
| Agent Responsibility Taxonomy | Mature prior taxonomy. | Agent authority and responsibility boundaries. | Valid as candidate; ensure agents do not own truth. |
| Agent Taxonomy Synthesis | Mature prior synthesis. | Agent dimensions, capability, responsibility, derivation rules. | Valid as candidate; neutralize semantic-authority naming. |
| Agent Taxonomy Readiness Review | Readiness evidence. | Agent foundations and taxonomy inputs. | Valid as historical readiness evidence, not taxonomy authority. |
| Context Taxonomy Dimensions | Mature prior taxonomy. | Context foundations, authority model, lifecycle, governance, security. | Valid as candidate; high carry-forward value. |
| Context Source Taxonomy | Mature prior taxonomy. | Source classification and authority boundaries. | Valid as candidate; needs current source registry integration. |
| Context Consumer Taxonomy | Mature prior taxonomy. | Agent, validation, governance, execution, coordination, observability consumers. | Valid as candidate; useful for context-pack strategy. |
| Context Sensitivity Taxonomy | Mature prior taxonomy. | Security, governance, visibility, federation sensitivity. | Valid as candidate; requires current access policy. |
| Context Scope Taxonomy | Mature prior taxonomy. | Entity, relationship, substructure, case, domain, cross-domain, repository, system scopes. | Valid as candidate; avoid graph-only assumption where not needed. |
| Context Freshness Taxonomy | Mature prior taxonomy. | Lifecycle and source freshness. | Valid as candidate; useful for context eligibility. |
| Context Taxonomy Synthesis | Mature prior synthesis. | Context dimensions, profiles, candidates, derivation rules. | Valid as candidate; strong input for context-pack strategy. |
| Context Taxonomy Closure | Mature prior closure. | Full context taxonomy chain. | Valid as candidate; not current authority until restated. |
| Context Taxonomy Readiness Review | Readiness evidence. | Context foundations and taxonomy inputs. | Valid as historical readiness evidence. |
| Adapter Taxonomy | Mature prior taxonomy. | Adapter foundations, boundaries, capability model, provider neutrality. | Valid as candidate; needs current provider registry alignment. |
| Provider Taxonomy | Mature prior taxonomy. | Provider foundations, abstraction, capability, governance. | Valid as candidate; requires external-source registry and provider revalidation. |
| Product Application Taxonomy | Mature product taxonomy. | Product workspace boundary. | Valid only inside product workspace scope. |
| Product Component Taxonomy | Mature product taxonomy. | Product component model and ownership. | Valid only inside product workspace scope. |
| Product Package Taxonomy | Mature product taxonomy. | Product structure and packaging model. | Valid only inside product workspace scope. |
| Product Service Taxonomy | Mature product taxonomy. | Product service architecture. | Valid only inside product workspace scope. |
| Product Schema Taxonomy | Mature product taxonomy. | Product schema architecture. | Valid only inside product workspace scope. |
| Product Integration Taxonomy | Mature product taxonomy. | Product integration architecture and dependency model. | Valid only inside product workspace scope. |
| Graphify Entity Taxonomy | Conflicted semantic taxonomy. | Cognitive Semantic System naming ADR and substrate evaluation. | Partially valid as entity-candidate evidence; not current naming or substrate authority. |
| Graphify Ontology | Conflicted cognitive-structure foundation. | Naming ADR, metamodel, entity taxonomy, substrate evaluation. | Partially valid as ontology evidence; not final cognitive substrate. |
| Graphify Metamodel | Conflicted cognitive-structure foundation. | Naming ADR, ontology, schema, relationship strategy, substrate evaluation. | Partially valid as metamodel evidence; not final representation authority. |

Taxonomy rule:

```text
Taxonomies classify concepts; they do not create authority, permissions,
implementations, runtime types, provider contracts, or final cognitive substrate.
```

## 9. ADR Inventory

| Decision | Historical source | Current semantic verdict | Reason | Required handling |
| --- | --- | --- | --- | --- |
| `ADR-001` | `previusknowledge/docs/architecture/adr_001_graphify_authority_proof.md` | Requires revision. | The core distinction between generated repository projections and governed semantic authority remains valid, but the historical naming is no longer acceptable as current/future system naming. | Keep as evidence for why the future Cognitive Semantic System needs authority, provenance, lifecycle, validation, governance, and context eligibility. Rewrite naming through a future naming ADR. |
| `ADR-002` | `previusknowledge/docs/architecture/adr_002_why_graph.md` | Blocked by current research. | It argues for graph-first canonical representation, but W-01 now states that graph is a strong candidate, not an implementation decision. | Keep as graph-substrate evidence. Reopen the substrate question and compare graph, other complex-system organization, and hybrid models before implementation. |

ADR rule:

```text
The ADR files remain decision evidence from the old scope. They are not current
AGENT PLATFORM decisions where they conflict with W-01 naming or substrate rules.
```

## 10. Canonical Knowledge Map

This is the first conceptual navigation model for future agents. It maps knowledge dependencies, not files.

```text
Workspace
  -> Authority Principles
  -> Architecture Boundaries
  -> Cognitive Semantic System Concept
  -> Domain Models
  -> Taxonomies
  -> Context And Agent Operation
  -> Validation And Governance
  -> Product Workspaces
  -> External References
  -> Research Evidence
```

Dependency map:

| Knowledge area | Depends on | Feeds |
| --- | --- | --- |
| Workspace | Charter, vocabulary, authority boundaries. | All other domains. |
| Authority Principles | Workspace, source-of-truth strategy, governance, validation, security. | Cognitive Semantic System, context, agents, product workspaces, external registry. |
| Architecture Boundaries | Workspace, authority principles, previous domain syntheses. | Models and taxonomies. |
| Cognitive Semantic System Concept | Authority principles, semantic-authority evidence, naming/substrate constraints. | Context eligibility, knowledge reuse, validation/governance trace, future semantic navigation. |
| Domain Models | Architecture boundaries and specific syntheses. | Taxonomies, context packs, agent roles, provider/adapter/workflow/runtime posture. |
| Taxonomies | Domain models and authority boundaries. | Retrieval, classification, context selection, registry metadata, agent task routing. |
| Context And Agent Operation | Context model, agent model, security/access, governance, validation. | Agent-native work execution and knowledge navigation. |
| Validation And Governance | Authority principles, evidence model, security/access, domain models. | Promotion, decisions, exceptions, lifecycle, trust. |
| Product Workspaces | Workspace/product boundary, product models, domain references. | Product-specific architecture and validation without root authority collapse. |
| External References | External source provenance, provider/adapter model, security/access. | Registry evidence, provider revalidation, product/domain research. |
| Research Evidence | Questions, comparisons, source reviews, ADR evidence. | Candidate principles, models, taxonomies, and design alternatives. |

Agent navigation rule:

```text
Agents should begin from the workspace and authority principles, then traverse to
the specific domain model, taxonomy, evidence, and validation/governance status
needed for the task. Agents should not begin by browsing filenames as if path
order were semantic order.
```

## 11. Workspace Cognitive Readiness

| Readiness area | Assessment | Reason | Current verdict |
| --- | --- | --- | --- |
| Navigation readiness | Partial. | Domains, models, taxonomies, and file evidence are now semantically mapped, but no machine-queryable index or context-pack format exists. | Sufficient for human/agent guided navigation; not yet automated. |
| Context readiness | Partial. | Context architecture is mature, but current workspace context-pack schema and assembly rules are absent. | Not ready for autonomous broad agent context selection. |
| Authority readiness | Medium. | Core authority principles are canonical in W-01 and W-02, but governance workflow, validation registry, and Cognitive Semantic System implementation are absent. | Ready for architecture decisions; not ready for automated promotion. |
| Knowledge reuse readiness | Medium. | Carry-forward, scope-limited, conflicted, and external knowledge are separated at concept level. | Ready for controlled reuse; not ready for direct implementation reuse. |
| Migration readiness | Medium-high. | Previous knowledge is classified both by file and by concept. Product, external, substrate, and governance gaps remain. | Ready for next scoped canonical workspace document after explicit instruction. |

Readiness rule:

```text
The workspace is cognitively oriented enough to continue W-series architecture,
but not enough to allow autonomous restructuring, implementation, authority
promotion, or broad agent operation.
```

## 12. Remaining Conceptual Gaps

These are missing knowledge structures, not missing files.

| Gap | Why it matters | Blocks |
| --- | --- | --- |
| Cognitive Semantic System naming ADR | The neutral name is provisional. | Final naming and authority vocabulary. |
| Cognitive substrate evaluation | Graph is only a candidate. | Any semantic-system implementation or storage design. |
| Formal authority transition model | Evidence, candidates, validation, governance, accepted truth, and historical truth need current workflow semantics. | Automated promotion and semantic authority operations. |
| Context-pack strategy | Agents need bounded, task-scoped, authority-aware context. | Reliable agent-native operation. |
| External source registry semantics | External provenance, role, risk, freshness, license, and promotion status are not yet registered. | Controlled use of `4_external/sources/`. |
| Workspace responsibility map | Current numbered folders are not conceptually mapped. | Safe restructuring and agent navigation by workspace area. |
| Product workspace boundary policy | Product material is scope-limited but not yet assigned. | Digital Twin/product migration. |
| Governance workflow | Governance is conceptually clear but procedurally undefined. | Approval, promotion, exception, and lifecycle actions. |
| Validation registry | Validation concepts exist but current evidence retention and proof levels are undefined. | Evidence-based promotion and readiness checks. |
| Security/Access policy | Constraints exist but current permissions, secrets, shell, network, MCP, provider, and publication rules are undefined. | Safe agent/tool/provider operation. |
| Taxonomy reconciliation | Multiple mature taxonomies exist in old scope. | Stable current type system and context classification. |
| Agent permission profiles | Agent roles exist conceptually; concrete permissions do not. | Safe multi-agent execution. |
| Memory, skills, commands, hooks, and MCP lifecycle | Candidate principles exist but not current governance. | Durable capability reuse and tool exposure. |
| Operations evidence lifecycle | Runtime outputs, logs, incidents, and generated artifacts need current lifecycle semantics. | Operational evidence reuse and audit. |
| Semantic query/navigation patterns | Agents need conceptual routes through knowledge. | Machine-assisted retrieval and future cognitive workspace UX. |

Gap rule:

```text
A gap is not permission to improvise. A gap is a boundary that must stay visible
until a canonical workspace document resolves it.
```

## 13. Final Verdict

| Question | Answer |
| --- | --- |
| Is the previous knowledge now semantically classified? | Yes. W-02 now classifies the prior corpus by domains, principles, models, taxonomies, decisions, conceptual dependencies, readiness, gaps, and supporting file inventory. |
| Can W-03 safely start? | Yes, after explicit instruction. The semantic classification is sufficient to start an external source registry, but this revision does not create W-03. |
| What should be the next canonical workspace document? | If explicitly instructed to proceed with W-03, the next document should be an external source registry under `0_architecture/workspace/`. It should classify `4_external/sources/` by provenance, role, risk, freshness, license, relevance, and promotion status. |

Final semantic W-02 statement:

```text
The previous knowledge corpus is now classified semantically, not only by file.

Its reusable core is an agent-native authority posture: agents reason over
selected context, files and generated outputs are artifacts, evidence requires
promotion, providers remain external, runtime mediates without truth ownership,
and a future Cognitive Semantic System should own accepted semantic truth without
pre-deciding the final cognitive substrate.

W-02 is complete for semantic classification. No W-03 document is created here.
```

## Appendix A - Architecture Document Index

| Path | State | Current scope | Handling |
| --- | --- | --- | --- |
| `previusknowledge/docs/architecture/adapter_architecture_final_synthesis.md` | `carry_forward` | Adapter architecture | Restate adapter posture in current workspace terms. |
| `previusknowledge/docs/architecture/adapter_boundary_model.md` | `carry_forward` | Adapter architecture | Preserve provider-boundary distinctions. |
| `previusknowledge/docs/architecture/adapter_capability_model.md` | `carry_forward` | Adapter architecture | Reuse capability vocabulary after workspace reframing. |
| `previusknowledge/docs/architecture/adapter_final_synthesis.md` | `carry_forward` | Adapter architecture | Preserve as major synthesis input. |
| `previusknowledge/docs/architecture/adapter_foundations.md` | `carry_forward` | Adapter architecture | Preserve foundational adapter principles. |
| `previusknowledge/docs/architecture/adapter_governance.md` | `carry_forward` | Adapter governance | Reframe as governance boundary input. |
| `previusknowledge/docs/architecture/adapter_security.md` | `carry_forward` | Adapter security | Reframe as security/access input. |
| `previusknowledge/docs/architecture/adapter_taxonomy.md` | `carry_forward` | Adapter taxonomy | Reuse only after current taxonomy review. |
| `previusknowledge/docs/architecture/adapter_type_derivation_rules.md` | `carry_forward` | Adapter taxonomy | Preserve derivation logic as candidate rules. |
| `previusknowledge/docs/architecture/adapter_validation.md` | `carry_forward` | Adapter validation | Reframe as validation posture input. |
| `previusknowledge/docs/architecture/adr_001_graphify_authority_proof.md` | `conflicted` | Semantic authority candidate | Preserve as evidence; requires neutral naming and substrate review. |
| `previusknowledge/docs/architecture/adr_002_why_graph.md` | `conflicted` | Cognitive substrate candidate | Preserve as graph-hypothesis evidence, not a substrate decision. |
| `previusknowledge/docs/architecture/agent_approval_model.md` | `carry_forward` | Agent governance | Preserve approval boundaries. |
| `previusknowledge/docs/architecture/agent_architecture_closure.md` | `carry_forward` | Agent architecture | Preserve closure conclusions after workspace reframing. |
| `previusknowledge/docs/architecture/agent_architecture_final_synthesis.md` | `carry_forward` | Agent architecture | Preserve as major synthesis input. |
| `previusknowledge/docs/architecture/agent_architecture_foundations.md` | `carry_forward` | Agent architecture | Preserve foundational agent principles. |
| `previusknowledge/docs/architecture/agent_autonomy_model.md` | `carry_forward` | Agent autonomy | Preserve autonomy boundaries. |
| `previusknowledge/docs/architecture/agent_boundary_model.md` | `carry_forward` | Agent boundaries | Preserve agent authority limits. |
| `previusknowledge/docs/architecture/agent_capability_taxonomy.md` | `carry_forward` | Agent taxonomy | Reuse only after current taxonomy review. |
| `previusknowledge/docs/architecture/agent_context_boundary_model.md` | `carry_forward` | Agent context | Preserve context-boundary logic. |
| `previusknowledge/docs/architecture/agent_coordination_model.md` | `carry_forward` | Agent coordination | Preserve coordination concepts for agent-native workspace. |
| `previusknowledge/docs/architecture/agent_decision_model.md` | `carry_forward` | Agent decisions | Preserve distinction between recommendations and authority. |
| `previusknowledge/docs/architecture/agent_escalation_model.md` | `carry_forward` | Agent governance | Preserve escalation concepts. |
| `previusknowledge/docs/architecture/agent_execution_model.md` | `carry_forward` | Agent execution | Reframe as permitted execution posture. |
| `previusknowledge/docs/architecture/agent_governance_architecture.md` | `carry_forward` | Agent governance | Preserve governance interaction concepts. |
| `previusknowledge/docs/architecture/agent_governance_interaction_model.md` | `carry_forward` | Agent governance | Preserve interaction boundaries. |
| `previusknowledge/docs/architecture/agent_graphify_integration_model.md` | `conflicted` | Agent to semantic authority | Preserve intent; replace prior naming and avoid graph commitment. |
| `previusknowledge/docs/architecture/agent_handoff_model.md` | `carry_forward` | Agent coordination | Preserve handoff and trace concepts. |
| `previusknowledge/docs/architecture/agent_memory_boundary_model.md` | `carry_forward` | Agent memory | Preserve memory-as-evidence boundary. |
| `previusknowledge/docs/architecture/agent_orchestration_architecture.md` | `carry_forward` | Agent orchestration | Reframe as coordination posture, not implementation. |
| `previusknowledge/docs/architecture/agent_orchestration_pattern_catalog.md` | `carry_forward` | Agent orchestration | Preserve as pattern evidence for future selection. |
| `previusknowledge/docs/architecture/agent_organization_principles.md` | `carry_forward` | Agent organization | Preserve role and responsibility principles. |
| `previusknowledge/docs/architecture/agent_organizational_architecture.md` | `carry_forward` | Agent organization | Reframe under workspace authority. |
| `previusknowledge/docs/architecture/agent_permission_boundary_model.md` | `carry_forward` | Agent permissions | Preserve permission-boundary concepts. |
| `previusknowledge/docs/architecture/agent_responsibility_taxonomy.md` | `carry_forward` | Agent taxonomy | Reuse only after current taxonomy review. |
| `previusknowledge/docs/architecture/agent_runtime_architecture.md` | `carry_forward` | Agent runtime | Reframe as runtime posture, not implementation. |
| `previusknowledge/docs/architecture/agent_security_model.md` | `carry_forward` | Agent security | Preserve security/access constraints. |
| `previusknowledge/docs/architecture/agent_strategy.md` | `carry_forward` | Agent strategy | Preserve agent-native direction after workspace reframing. |
| `previusknowledge/docs/architecture/agent_taxonomy_dimensions.md` | `carry_forward` | Agent taxonomy | Preserve taxonomy dimensions as candidate model. |
| `previusknowledge/docs/architecture/agent_taxonomy_readiness_review.md` | `migration_evidence` | Agent taxonomy review | Use as readiness evidence only. |
| `previusknowledge/docs/architecture/agent_taxonomy_synthesis.md` | `carry_forward` | Agent taxonomy | Preserve synthesis as candidate taxonomy input. |
| `previusknowledge/docs/architecture/agent_type_derivation_rules.md` | `carry_forward` | Agent taxonomy | Preserve derivation logic as candidate rules. |
| `previusknowledge/docs/architecture/canonical_adapter_type_candidates.md` | `migration_evidence` | Adapter candidates | Candidate list only; not current taxonomy. |
| `previusknowledge/docs/architecture/canonical_agent_type_candidates.md` | `migration_evidence` | Agent candidates | Candidate list only; not current taxonomy. |
| `previusknowledge/docs/architecture/canonical_context_type_candidates.md` | `migration_evidence` | Context candidates | Candidate list only; not current taxonomy. |
| `previusknowledge/docs/architecture/capability_exposure_runtime.md` | `carry_forward` | Runtime posture | Preserve exposure concepts without implementation commitment. |
| `previusknowledge/docs/architecture/claude_adapter_final_synthesis.md` | `external_reference` | Claude provider evidence | Revalidate before any adapter decision. |
| `previusknowledge/docs/architecture/claude_delta_analysis_vs_codex.md` | `external_reference` | Claude provider evidence | Use as historical provider comparison. |
| `previusknowledge/docs/architecture/claude_divergent_gsv.md` | `external_reference` | Claude provider evidence | Use as governance/security/validation evidence. |
| `previusknowledge/docs/architecture/claude_provider_characterization.md` | `external_reference` | Claude provider evidence | Revalidate against current provider behavior. |
| `previusknowledge/docs/architecture/claude_runtime_differences.md` | `external_reference` | Claude provider evidence | Revalidate before runtime assumptions. |
| `previusknowledge/docs/architecture/codex_adapter_final_synthesis.md` | `external_reference` | Codex provider evidence | Revalidate before any adapter decision. |
| `previusknowledge/docs/architecture/codex_adapter_type_mapping.md` | `external_reference` | Codex provider evidence | Use as historical mapping evidence. |
| `previusknowledge/docs/architecture/codex_architectural_constraints.md` | `external_reference` | Codex provider evidence | Revalidate constraints before use. |
| `previusknowledge/docs/architecture/codex_capability_mapping.md` | `external_reference` | Codex provider evidence | Revalidate capabilities before use. |
| `previusknowledge/docs/architecture/codex_governance_mapping.md` | `external_reference` | Codex provider evidence | Use as governance comparison evidence. |
| `previusknowledge/docs/architecture/codex_provider_characterization.md` | `external_reference` | Codex provider evidence | Revalidate provider characterization. |
| `previusknowledge/docs/architecture/codex_provider_classification.md` | `external_reference` | Codex provider evidence | Use as historical classification evidence. |
| `previusknowledge/docs/architecture/codex_runtime_participation.md` | `external_reference` | Codex provider evidence | Revalidate runtime participation before use. |
| `previusknowledge/docs/architecture/codex_security_mapping.md` | `external_reference` | Codex provider evidence | Use as security comparison evidence. |
| `previusknowledge/docs/architecture/codex_validation_mapping.md` | `external_reference` | Codex provider evidence | Use as validation comparison evidence. |
| `previusknowledge/docs/architecture/context_architecture_final_synthesis.md` | `carry_forward` | Context architecture | Preserve as major synthesis input. |
| `previusknowledge/docs/architecture/context_architecture_foundations.md` | `carry_forward` | Context architecture | Preserve foundational context principles. |
| `previusknowledge/docs/architecture/context_assembly_architecture.md` | `carry_forward` | Context assembly | Reframe for future context packs. |
| `previusknowledge/docs/architecture/context_authority_model.md` | `carry_forward` | Context authority | Preserve non-authority and eligibility distinctions. |
| `previusknowledge/docs/architecture/context_boundary_model.md` | `carry_forward` | Context boundaries | Preserve boundary concepts. |
| `previusknowledge/docs/architecture/context_compression_architecture.md` | `carry_forward` | Context compression | Preserve as candidate context operation model. |
| `previusknowledge/docs/architecture/context_consumer_taxonomy.md` | `carry_forward` | Context taxonomy | Reuse only after current taxonomy review. |
| `previusknowledge/docs/architecture/context_expansion_architecture.md` | `carry_forward` | Context expansion | Preserve as candidate context operation model. |
| `previusknowledge/docs/architecture/context_federation_model.md` | `carry_forward` | Context federation | Preserve federation concepts. |
| `previusknowledge/docs/architecture/context_freshness_taxonomy.md` | `carry_forward` | Context taxonomy | Preserve freshness dimensions. |
| `previusknowledge/docs/architecture/context_governance_architecture.md` | `carry_forward` | Context governance | Preserve governance constraints. |
| `previusknowledge/docs/architecture/context_governance_model.md` | `carry_forward` | Context governance | Preserve governance model as candidate input. |
| `previusknowledge/docs/architecture/context_lifecycle_model.md` | `carry_forward` | Context lifecycle | Preserve lifecycle concepts. |
| `previusknowledge/docs/architecture/context_observability_model.md` | `carry_forward` | Context observability | Preserve observability concepts. |
| `previusknowledge/docs/architecture/context_retrieval_architecture.md` | `carry_forward` | Context retrieval | Preserve retrieval concepts for agent-native design. |
| `previusknowledge/docs/architecture/context_runtime_architecture.md` | `carry_forward` | Context runtime | Reframe as runtime posture, not implementation. |
| `previusknowledge/docs/architecture/context_scope_taxonomy.md` | `carry_forward` | Context taxonomy | Preserve scope dimensions. |
| `previusknowledge/docs/architecture/context_security_model.md` | `carry_forward` | Context security | Preserve sensitivity and exposure constraints. |
| `previusknowledge/docs/architecture/context_selection_architecture.md` | `carry_forward` | Context selection | Preserve selected-context model. |
| `previusknowledge/docs/architecture/context_sensitivity_taxonomy.md` | `carry_forward` | Context taxonomy | Preserve sensitivity dimensions. |
| `previusknowledge/docs/architecture/context_source_taxonomy.md` | `carry_forward` | Context taxonomy | Preserve source dimensions. |
| `previusknowledge/docs/architecture/context_taxonomy_closure.md` | `carry_forward` | Context taxonomy | Preserve closure conclusions as candidate input. |
| `previusknowledge/docs/architecture/context_taxonomy_dimensions.md` | `carry_forward` | Context taxonomy | Preserve taxonomy dimensions. |
| `previusknowledge/docs/architecture/context_taxonomy_readiness_review.md` | `migration_evidence` | Context taxonomy review | Use as readiness evidence only. |
| `previusknowledge/docs/architecture/context_taxonomy_synthesis.md` | `carry_forward` | Context taxonomy | Preserve synthesis as candidate taxonomy input. |
| `previusknowledge/docs/architecture/context_type_derivation_rules.md` | `carry_forward` | Context taxonomy | Preserve derivation logic as candidate rules. |
| `previusknowledge/docs/architecture/context_validation_model.md` | `carry_forward` | Context validation | Preserve validation posture concepts. |
| `previusknowledge/docs/architecture/cross_layer_rules.md` | `carry_forward` | Workspace boundaries | Preserve cross-boundary rules after workspace reframing. |
| `previusknowledge/docs/architecture/cursor_adapter_final_synthesis.md` | `external_reference` | Cursor provider evidence | Revalidate before any adapter decision. |
| `previusknowledge/docs/architecture/cursor_delta_analysis_vs_codex.md` | `external_reference` | Cursor provider evidence | Use as historical provider comparison. |
| `previusknowledge/docs/architecture/cursor_divergent_governance_security_validation.md` | `external_reference` | Cursor provider evidence | Use as governance/security/validation evidence. |
| `previusknowledge/docs/architecture/cursor_provider_characterization.md` | `external_reference` | Cursor provider evidence | Revalidate provider characterization. |
| `previusknowledge/docs/architecture/cursor_runtime_differences.md` | `external_reference` | Cursor provider evidence | Revalidate runtime assumptions. |
| `previusknowledge/docs/architecture/execution_runtime.md` | `carry_forward` | Runtime posture | Preserve execution posture without implementation commitment. |
| `previusknowledge/docs/architecture/external_layer.md` | `carry_forward` | External boundary | Preserve external-source boundary principles. |
| `previusknowledge/docs/architecture/governance_layer.md` | `carry_forward` | Governance | Preserve governance layer concepts after workspace reframing. |
| `previusknowledge/docs/architecture/graphify_agent_representation.md` | `conflicted` | Semantic authority candidate | Preserve as candidate input; neutralize naming and substrate assumptions. |
| `previusknowledge/docs/architecture/graphify_api_strategy.md` | `conflicted` | Semantic authority candidate | Preserve as candidate input; no API commitment. |
| `previusknowledge/docs/architecture/graphify_canonical_semantic_model.md` | `conflicted` | Semantic authority candidate | Preserve semantic-authority principles; neutralize naming and substrate assumptions. |
| `previusknowledge/docs/architecture/graphify_command_representation.md` | `conflicted` | Semantic authority candidate | Preserve as candidate input; no representation commitment. |
| `previusknowledge/docs/architecture/graphify_dependency_representation.md` | `conflicted` | Semantic authority candidate | Preserve relationship ideas; no graph-substrate decision. |
| `previusknowledge/docs/architecture/graphify_documentation_representation.md` | `conflicted` | Semantic authority candidate | Preserve projection ideas; neutralize naming. |
| `previusknowledge/docs/architecture/graphify_entity_taxonomy.md` | `conflicted` | Semantic authority candidate | Preserve entity concepts as candidate input. |
| `previusknowledge/docs/architecture/graphify_governance_schema_model.md` | `conflicted` | Semantic authority candidate | Preserve governance-schema ideas; no schema commitment. |
| `previusknowledge/docs/architecture/graphify_graph_database_strategy.md` | `conflicted` | Cognitive substrate candidate | Preserve as graph-database evidence, not a decision. |
| `previusknowledge/docs/architecture/graphify_harness_adapter_representation.md` | `conflicted` | Semantic authority candidate | Preserve adapter-representation ideas after neutral naming. |
| `previusknowledge/docs/architecture/graphify_hook_representation.md` | `conflicted` | Semantic authority candidate | Preserve as candidate input; no representation commitment. |
| `previusknowledge/docs/architecture/graphify_import_export_schema_model.md` | `conflicted` | Semantic authority candidate | Preserve import/export ideas; no schema commitment. |
| `previusknowledge/docs/architecture/graphify_infrastructure_architecture.md` | `conflicted` | Semantic authority candidate | Preserve as infrastructure evidence only. |
| `previusknowledge/docs/architecture/graphify_integration_strategy.md` | `conflicted` | Semantic authority candidate | Preserve integration ideas after naming ADR. |
| `previusknowledge/docs/architecture/graphify_knowledge_research_coherence_audit.md` | `conflicted` | Semantic authority candidate | Preserve audit findings as candidate evidence. |
| `previusknowledge/docs/architecture/graphify_lifecycle_schema_model.md` | `conflicted` | Semantic authority candidate | Preserve lifecycle ideas; no schema commitment. |
| `previusknowledge/docs/architecture/graphify_mcp_representation.md` | `conflicted` | Semantic authority candidate | Preserve MCP-representation ideas after neutral naming. |
| `previusknowledge/docs/architecture/graphify_memory_representation.md` | `conflicted` | Semantic authority candidate | Preserve memory-representation ideas after neutral naming. |
| `previusknowledge/docs/architecture/graphify_metamodel.md` | `conflicted` | Cognitive substrate candidate | Preserve metamodel ideas; no substrate commitment. |
| `previusknowledge/docs/architecture/graphify_node_schema_model.md` | `conflicted` | Cognitive substrate candidate | Preserve as graph-candidate evidence only. |
| `previusknowledge/docs/architecture/graphify_ontology.md` | `conflicted` | Cognitive substrate candidate | Preserve ontology ideas; no substrate commitment. |
| `previusknowledge/docs/architecture/graphify_projection_engine_strategy.md` | `conflicted` | Semantic authority candidate | Preserve projection strategy as candidate input. |
| `previusknowledge/docs/architecture/graphify_relationship_schema_model.md` | `conflicted` | Cognitive substrate candidate | Preserve relationship ideas; no graph-substrate decision. |
| `previusknowledge/docs/architecture/graphify_repository_representation.md` | `conflicted` | Semantic authority candidate | Preserve repository-representation ideas after workspace reframing. |
| `previusknowledge/docs/architecture/graphify_repository_strategy.md` | `conflicted` | Semantic authority candidate | Preserve repository strategy as historical evidence. |
| `previusknowledge/docs/architecture/graphify_repository_synchronization.md` | `conflicted` | Semantic authority candidate | Preserve sync ideas; no implementation commitment. |
| `previusknowledge/docs/architecture/graphify_runtime_architecture.md` | `conflicted` | Semantic authority candidate | Preserve runtime ideas as conceptual evidence only. |
| `previusknowledge/docs/architecture/graphify_schema_architecture.md` | `conflicted` | Semantic authority candidate | Preserve schema ideas; no schema commitment. |
| `previusknowledge/docs/architecture/graphify_schema_registry_strategy.md` | `conflicted` | Semantic authority candidate | Preserve registry ideas for later evaluation. |
| `previusknowledge/docs/architecture/graphify_schema_strategy.md` | `conflicted` | Semantic authority candidate | Preserve schema strategy as candidate evidence. |
| `previusknowledge/docs/architecture/graphify_semantic_authority_architecture.md` | `conflicted` | Semantic authority candidate | Preserve authority principles; neutralize naming and substrate assumptions. |
| `previusknowledge/docs/architecture/graphify_skill_representation.md` | `conflicted` | Semantic authority candidate | Preserve skill-representation ideas after neutral naming. |
| `previusknowledge/docs/architecture/graphify_storage_strategy.md` | `conflicted` | Semantic authority candidate | Preserve storage questions; no storage decision. |
| `previusknowledge/docs/architecture/graphify_synchronization_engine_strategy.md` | `conflicted` | Semantic authority candidate | Preserve sync questions; no engine decision. |
| `previusknowledge/docs/architecture/graphify_system_of_record.md` | `conflicted` | Semantic authority candidate | Preserve system-of-record concepts after neutral naming. |
| `previusknowledge/docs/architecture/graphify_ticket_representation.md` | `conflicted` | Semantic authority candidate | Preserve ticket-representation ideas after neutral naming. |
| `previusknowledge/docs/architecture/graphify_tool_representation.md` | `conflicted` | Semantic authority candidate | Preserve tool-representation ideas after neutral naming. |
| `previusknowledge/docs/architecture/graphify_validation_engine_strategy.md` | `conflicted` | Semantic authority candidate | Preserve validation-engine ideas; no implementation commitment. |
| `previusknowledge/docs/architecture/graphify_validation_schema_model.md` | `conflicted` | Semantic authority candidate | Preserve validation-schema ideas; no schema commitment. |
| `previusknowledge/docs/architecture/graphify_vocabulary.md` | `conflicted` | Semantic authority naming | Preserve as prior vocabulary evidence only. |
| `previusknowledge/docs/architecture/graphify_workflow_representation.md` | `conflicted` | Semantic authority candidate | Preserve workflow-representation ideas after neutral naming. |
| `previusknowledge/docs/architecture/hermes_agent_runtime_review.md` | `external_reference` | Hermes provider evidence | Use as external runtime evidence. |
| `previusknowledge/docs/architecture/hermes_comparative_architecture.md` | `external_reference` | Hermes provider evidence | Use as external comparison evidence. |
| `previusknowledge/docs/architecture/hermes_mcp_architecture_review.md` | `external_reference` | Hermes provider evidence | Use as MCP integration evidence. |
| `previusknowledge/docs/architecture/hermes_memory_context_review.md` | `external_reference` | Hermes provider evidence | Use as memory/context evidence. |
| `previusknowledge/docs/architecture/hermes_provider_plugin_review.md` | `external_reference` | Hermes provider evidence | Use as plugin/provider evidence. |
| `previusknowledge/docs/architecture/hermes_repository_survey.md` | `external_reference` | Hermes provider evidence | Use as external repository survey evidence. |
| `previusknowledge/docs/architecture/hermes_roadmap_impact_assessment.md` | `external_reference` | Hermes provider evidence | Use as historical roadmap evidence only. |
| `previusknowledge/docs/architecture/hermes_runtime_gateway_review.md` | `external_reference` | Hermes provider evidence | Use as runtime/gateway evidence. |
| `previusknowledge/docs/architecture/hermes_tool_architecture_review.md` | `external_reference` | Hermes provider evidence | Use as tool architecture evidence. |
| `previusknowledge/docs/architecture/knowledge_layer.md` | `carry_forward` | Knowledge layer | Preserve knowledge-boundary concepts after workspace reframing. |
| `previusknowledge/docs/architecture/layer_ownership.md` | `carry_forward` | Ownership | Preserve ownership principles after workspace reframing. |
| `previusknowledge/docs/architecture/macrofolder_architecture.md` | `migration_evidence` | Old folder model | Use as responsibility-domain evidence, not folder plan. |
| `previusknowledge/docs/architecture/modularity_goals.md` | `carry_forward` | Modularity | Preserve modularity goals after workspace reframing. |
| `previusknowledge/docs/architecture/monorepo_vs_multirepo_strategy.md` | `migration_evidence` | Repository strategy | Use as repository-boundary evidence only. |
| `previusknowledge/docs/architecture/opencode_adapter_final_synthesis.md` | `external_reference` | OpenCode provider evidence | Revalidate before any adapter decision. |
| `previusknowledge/docs/architecture/opencode_capability_mapping.md` | `external_reference` | OpenCode provider evidence | Revalidate capabilities before use. |
| `previusknowledge/docs/architecture/opencode_delta_analysis_vs_codex.md` | `external_reference` | OpenCode provider evidence | Use as historical provider comparison. |
| `previusknowledge/docs/architecture/opencode_divergent_gsv.md` | `external_reference` | OpenCode provider evidence | Use as governance/security/validation evidence. |
| `previusknowledge/docs/architecture/opencode_provider_characterization.md` | `external_reference` | OpenCode provider evidence | Revalidate provider characterization. |
| `previusknowledge/docs/architecture/opencode_runtime_differences.md` | `external_reference` | OpenCode provider evidence | Revalidate runtime assumptions. |
| `previusknowledge/docs/architecture/operations_layer.md` | `migration_evidence` | Operations layer | Use as old responsibility-domain evidence only. |
| `previusknowledge/docs/architecture/ownership_domains.md` | `carry_forward` | Ownership | Preserve ownership-domain concepts after workspace reframing. |
| `previusknowledge/docs/architecture/platform_architecture_audit.md` | `migration_evidence` | Platform audit | Use as historical audit evidence. |
| `previusknowledge/docs/architecture/platform_foundations.md` | `carry_forward` | Platform architecture | Preserve platform principles after workspace reframing. |
| `previusknowledge/docs/architecture/platform_layer.md` | `carry_forward` | Platform architecture | Preserve platform layer concepts after workspace reframing. |
| `previusknowledge/docs/architecture/platform_runtime_foundations.md` | `carry_forward` | Runtime posture | Preserve runtime foundation concepts without implementation commitment. |
| `previusknowledge/docs/architecture/product_agent_relationship_model.md` | `scope_limit` | Product workspace | Future product-scope input only. |
| `previusknowledge/docs/architecture/product_application_architecture.md` | `scope_limit` | Product workspace | Future product-scope input only. |
| `previusknowledge/docs/architecture/product_application_taxonomy.md` | `scope_limit` | Product workspace | Future product taxonomy input only. |
| `previusknowledge/docs/architecture/product_architectural_principles.md` | `scope_limit` | Product workspace | Future product principles input only. |
| `previusknowledge/docs/architecture/product_architecture_final_synthesis.md` | `scope_limit` | Product workspace | Major product-scope synthesis; not root authority. |
| `previusknowledge/docs/architecture/product_architecture_overview.md` | `scope_limit` | Product workspace | Product overview only. |
| `previusknowledge/docs/architecture/product_architecture_readiness_review.md` | `scope_limit` | Product workspace | Product readiness evidence only. |
| `previusknowledge/docs/architecture/product_boundaries.md` | `scope_limit` | Product workspace | Product boundary input only. |
| `previusknowledge/docs/architecture/product_building_blocks.md` | `scope_limit` | Product workspace | Product building-block input only. |
| `previusknowledge/docs/architecture/product_capability_architecture.md` | `scope_limit` | Product workspace | Product capability input only. |
| `previusknowledge/docs/architecture/product_collaboration_architecture.md` | `scope_limit` | Product workspace | Product collaboration input only. |
| `previusknowledge/docs/architecture/product_component_architecture_final_synthesis.md` | `scope_limit` | Product workspace | Product component synthesis only. |
| `previusknowledge/docs/architecture/product_component_dependency_model.md` | `scope_limit` | Product workspace | Product dependency input only. |
| `previusknowledge/docs/architecture/product_component_ownership.md` | `scope_limit` | Product workspace | Product ownership input only. |
| `previusknowledge/docs/architecture/product_component_relationships.md` | `scope_limit` | Product workspace | Product relationship input only. |
| `previusknowledge/docs/architecture/product_component_responsibilities.md` | `scope_limit` | Product workspace | Product responsibility input only. |
| `previusknowledge/docs/architecture/product_component_taxonomy.md` | `scope_limit` | Product workspace | Product taxonomy input only. |
| `previusknowledge/docs/architecture/product_context_relationship_model.md` | `scope_limit` | Product workspace | Product context input only. |
| `previusknowledge/docs/architecture/product_contract_architecture.md` | `scope_limit` | Product workspace | Product contract input only. |
| `previusknowledge/docs/architecture/product_decision_architecture.md` | `scope_limit` | Product workspace | Product decision input only. |
| `previusknowledge/docs/architecture/product_dependency_architecture.md` | `scope_limit` | Product workspace | Product dependency input only. |
| `previusknowledge/docs/architecture/product_experience_architecture.md` | `scope_limit` | Product workspace | Product experience input only. |
| `previusknowledge/docs/architecture/product_graphify_relationship_model.md` | `scope_limit` | Product workspace | Product-scope semantic relationship input; neutralize naming if reused. |
| `previusknowledge/docs/architecture/product_integration_architecture.md` | `scope_limit` | Product workspace | Product integration input only. |
| `previusknowledge/docs/architecture/product_integration_taxonomy.md` | `scope_limit` | Product workspace | Product taxonomy input only. |
| `previusknowledge/docs/architecture/product_intelligence_architecture.md` | `scope_limit` | Product workspace | Product intelligence input only. |
| `previusknowledge/docs/architecture/product_knowledge_architecture.md` | `scope_limit` | Product workspace | Product knowledge input only. |
| `previusknowledge/docs/architecture/product_layer.md` | `scope_limit` | Product workspace | Product layer input only. |
| `previusknowledge/docs/architecture/product_observability_architecture.md` | `scope_limit` | Product workspace | Product observability input only. |
| `previusknowledge/docs/architecture/product_ownership_model.md` | `scope_limit` | Product workspace | Product ownership input only. |
| `previusknowledge/docs/architecture/product_package_architecture.md` | `scope_limit` | Product workspace | Product package input only. |
| `previusknowledge/docs/architecture/product_package_taxonomy.md` | `scope_limit` | Product workspace | Product taxonomy input only. |
| `previusknowledge/docs/architecture/product_purpose.md` | `scope_limit` | Product workspace | Product purpose input only. |
| `previusknowledge/docs/architecture/product_realization_architecture_final_synthesis.md` | `scope_limit` | Product workspace | Product realization synthesis only. |
| `previusknowledge/docs/architecture/product_runtime_architecture.md` | `scope_limit` | Product workspace | Product runtime input only. |
| `previusknowledge/docs/architecture/product_schema_architecture.md` | `scope_limit` | Product workspace | Product schema input only. |
| `previusknowledge/docs/architecture/product_schema_taxonomy.md` | `scope_limit` | Product workspace | Product taxonomy input only. |
| `previusknowledge/docs/architecture/product_service_architecture.md` | `scope_limit` | Product workspace | Product service input only. |
| `previusknowledge/docs/architecture/product_service_taxonomy.md` | `scope_limit` | Product workspace | Product taxonomy input only. |
| `previusknowledge/docs/architecture/product_structure_architecture_final_synthesis.md` | `scope_limit` | Product workspace | Product structure synthesis only. |
| `previusknowledge/docs/architecture/product_structure_dependency_model.md` | `scope_limit` | Product workspace | Product dependency input only. |
| `previusknowledge/docs/architecture/product_structure_layers.md` | `scope_limit` | Product workspace | Product structure input only. |
| `previusknowledge/docs/architecture/product_structure_principles.md` | `scope_limit` | Product workspace | Product structure input only. |
| `previusknowledge/docs/architecture/product_vision.md` | `scope_limit` | Product workspace | Product vision input only. |
| `previusknowledge/docs/architecture/provider_abstraction.md` | `carry_forward` | Provider architecture | Preserve provider abstraction concepts. |
| `previusknowledge/docs/architecture/provider_capability_model.md` | `carry_forward` | Provider architecture | Preserve capability concepts after workspace reframing. |
| `previusknowledge/docs/architecture/provider_final_synthesis.md` | `carry_forward` | Provider architecture | Preserve as major synthesis input. |
| `previusknowledge/docs/architecture/provider_foundations.md` | `carry_forward` | Provider architecture | Preserve foundational provider principles. |
| `previusknowledge/docs/architecture/provider_governance.md` | `carry_forward` | Provider governance | Preserve governance boundary concepts. |
| `previusknowledge/docs/architecture/provider_taxonomy.md` | `carry_forward` | Provider taxonomy | Reuse only after current taxonomy review. |
| `previusknowledge/docs/architecture/repository_principles.md` | `carry_forward` | Workspace principles | Reframe repository principles as workspace principles. |
| `previusknowledge/docs/architecture/repository_vision.md` | `scope_limit` | Product/repository vision | Historical AgentLab/Digital Twin vision; not root authority. |
| `previusknowledge/docs/architecture/runtime_final_synthesis.md` | `carry_forward` | Runtime posture | Preserve as major synthesis input. |
| `previusknowledge/docs/architecture/scalability_goals.md` | `carry_forward` | Scalability | Preserve scalability goals after workspace reframing. |
| `previusknowledge/docs/architecture/source_of_truth_strategy.md` | `carry_forward` | Authority model | Preserve source-of-truth, evidence, and promotion model. |
| `previusknowledge/docs/architecture/workflow_coordination.md` | `carry_forward` | Workflow posture | Preserve coordination concepts. |
| `previusknowledge/docs/architecture/workflow_execution.md` | `carry_forward` | Workflow posture | Preserve execution posture without implementation commitment. |
| `previusknowledge/docs/architecture/workflow_final_synthesis.md` | `carry_forward` | Workflow posture | Preserve as major synthesis input. |
| `previusknowledge/docs/architecture/workflow_foundations.md` | `carry_forward` | Workflow posture | Preserve foundational workflow principles. |
| `previusknowledge/docs/architecture/workflow_runtime.md` | `carry_forward` | Workflow posture | Reframe as runtime posture, not implementation. |

## Appendix B - Research Document Index

| Path | State | Current scope | Handling |
| --- | --- | --- | --- |
| `previusknowledge/research/agents/ecc_agent_architecture_analysis.md` | `external_reference` | ECC research evidence | Use as external harness evidence only. |
| `previusknowledge/research/agents/ecc_architecture_analysis.md` | `external_reference` | ECC research evidence | Use as external harness evidence only. |
| `previusknowledge/research/agents/ecc_codex_integration_analysis.md` | `external_reference` | ECC research evidence | Use as external harness evidence only. |
| `previusknowledge/research/agents/ecc_commands_architecture_analysis.md` | `external_reference` | ECC research evidence | Use as commands evidence only. |
| `previusknowledge/research/agents/ecc_hooks_architecture_analysis.md` | `external_reference` | ECC research evidence | Use as hooks evidence only. |
| `previusknowledge/research/agents/ecc_mcp_architecture_analysis.md` | `external_reference` | ECC research evidence | Use as MCP evidence only. |
| `previusknowledge/research/agents/ecc_memory_architecture_analysis.md` | `external_reference` | ECC research evidence | Use as memory evidence only. |
| `previusknowledge/research/agents/ecc_opencode_integration_analysis.md` | `external_reference` | ECC research evidence | Use as OpenCode integration evidence only. |
| `previusknowledge/research/agents/ecc_reusable_patterns.md` | `external_reference` | ECC research evidence | Use as reusable-pattern evidence only. |
| `previusknowledge/research/agents/ecc_schemas_architecture_analysis.md` | `external_reference` | ECC research evidence | Use as schema evidence only. |
| `previusknowledge/research/agents/ecc_skills_architecture_analysis.md` | `external_reference` | ECC research evidence | Use as skills evidence only. |
| `previusknowledge/research/agents/ecc_strategic_conclusions.md` | `external_reference` | ECC research evidence | Use as strategic evidence only. |
| `previusknowledge/research/agents/ecc_vs_graphify_analysis.md` | `external_reference` | ECC and graphify research evidence | Use as external comparison evidence; neutralize future-system naming if reused. |

## Appendix C - File-Level Promotion Rules

| Rule | Consequence |
| --- | --- |
| `carry_forward` does not equal current authority. | Content must be restated in a current canonical workspace document before governing implementation. |
| `conflicted` blocks promotion. | Resolve naming, scope, authority, and substrate conflicts first. |
| `scope_limit` blocks root authority. | Product material can be promoted only inside an explicit product workspace boundary. |
| `external_reference` requires revalidation. | Provider and harness facts must be checked against current external sources before use. |
| `migration_evidence` preserves trace. | These files explain how the prior architecture evolved but do not direct new work. |

Appendix file-level statement:

```text
The previous knowledge corpus remains fully classified at file level as evidence
supporting the semantic W-02 inventory.

The strongest carry-forward value is the agent-native authority posture:
agents reason with selected context, evidence is promoted explicitly, providers
remain external, and a future Cognitive Semantic System should own accepted
semantic truth independently of its final substrate.

Graph remains a candidate cognitive substrate, not an implementation decision.
```
