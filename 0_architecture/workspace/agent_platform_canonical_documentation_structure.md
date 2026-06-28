# AGENT PLATFORM Canonical Documentation Structure

Status: Canonical W-09 workspace output  
Date: 2026-06-28  
Scope: Documentation structure, status model, scope model, citation rules, projections, and future migration targets for AGENT PLATFORM  
Authority: Documentation-structure guidance only. This document does not move, copy, rename, delete, archive, migrate, implement, stage, commit, push, or create folders.

## 1. Purpose

This document defines how future AGENT PLATFORM documentation should be organized, classified, status-labeled, cited, projected, and migrated.

Documentation structure comes after W-04, W-05, W-06, W-07, and W-08 because documentation cannot be structured safely until workspace responsibilities, context selection, cognitive flow, topology, and migration controls are explicit.

| Prior work | Why W-09 depends on it |
| --- | --- |
| W-04 Responsibility Map | Defines what top-level areas own, consume, expose, and must never own. Documentation structure must follow responsibility, not folder intuition. |
| W-05 Context Pack Strategy | Defines source classes, citation behavior, exclusions, and edit rules. Documentation structure must preserve context and authority boundaries. |
| W-06 Cognitive Workspace Model | Defines goals, tasks, context, evidence, claims, validation, governance, output, and learning. Documentation structure must support those cognitive primitives. |
| W-07 Workspace Topology | Defines current numbered topology as a provisional projection and reserves future target areas without moving files. |
| W-08 Migration Plan | Defines migration as classified, cited, incremental, validation-backed, and governance-bound. Documentation structure must not become migration by another name. |

Clarifications:

| Clarification | Rule |
| --- | --- |
| Documentation structure is not migration. | W-09 defines where future documents should belong. It does not move, copy, rename, or archive anything. |
| Documentation structure is not authority by itself. | Authority depends on declared status, scope, validation posture, governance posture, and currency. |
| Documentation status determines authority posture. | A file in an architecture folder is not canonical unless its status and scope say so. |
| Docs are artifacts. | Documents carry claims, evidence, decisions, projections, and guidance. They are not truth by path or filename. |
| Human docs are projections unless explicitly canonical. | `6_docs/` can explain canonical architecture, but it must not override `0_architecture/` unless a future governance decision explicitly says otherwise. |

W-09 rule:

```text
Documentation becomes useful to agents and humans only when status, scope,
citations, authority posture, validation posture, governance posture, and lifecycle
are explicit. Folder location alone does not make documentation true.
```

## 2. Documentation Principles

| Principle | Rule |
| --- | --- |
| Status before location | A document's status governs how it may be used before its folder is considered. |
| Scope before authority | A document must declare the scope where it may be authoritative. |
| Evidence before claim | Material claims should identify supporting evidence before they constrain future work. |
| Citation before promotion | Restated, migrated, external, generated, or product claims require citations before promotion. |
| Architecture before implementation | Implementation notes, code, scripts, tools, packages, and SDKs must follow architecture rather than define it. |
| Research remains evidence | Research can support architecture and decisions, but it does not govern by itself. |
| Previous knowledge must be restated before promotion | Prior documents remain migration evidence until their concepts are rewritten in current workspace vocabulary and reviewed. |
| Product docs stay product-scoped | Product documentation may be canonical only inside declared product scope. It cannot define root platform authority by default. |
| External reviews stay evidence | External source reviews inform decisions but do not promote dependencies, execution, or provider behavior. |
| No canonical by filename or folder | A document does not become canonical because it is named `canonical`, placed under `0_architecture/`, or referenced often. |
| Human docs cite source authority | Guides and tutorials should cite the architecture or decision records they project. |
| Generated docs are not source | Generated documentation, summaries, and reports remain projections or evidence until reviewed and promoted. |
| Current vocabulary is mandatory | Use `Cognitive Semantic System` for the future semantic authority concept. Do not assume the final substrate is graph-based; graph remains a candidate only. |

Principle invariant:

```text
If a document lacks status, scope, and provenance, agents should treat it as
unclassified evidence until a current authority document classifies it.
```

## 3. Documentation Status Model

Status labels describe a document's authority posture. They are not Git status, lifecycle status alone, or folder names.

| Status | Meaning | Authority posture | Allowed location | Citation requirement | Promotion path | Edit rule |
| --- | --- | --- | --- | --- | --- | --- |
| `canonical` | Accepted authority within declared scope. | Governs only its declared scope while current and not superseded. | `0_architecture/workspace/`, future `0_architecture/<domain>/`, future decisions area, product scope if product policy allows. | Must cite evidence, decisions, prior docs, or validation where material claims depend on them. | Human or governance approval after evidence, validation, and scope review. | Edit only by explicit architecture, decision, product, or governance ticket. |
| `draft` | Work-in-progress material not ready for decision or reliance. | Not authoritative. | Architecture drafts, research, docs, workspace operations, product drafts. | Cite sources for claims that may later be promoted. | Review, revise, validate, then promote to `proposal` or `canonical`. | Editable by explicit ticket within scope. |
| `proposal` | Candidate decision, structure, policy, or architecture. | Recommendation only; not binding until accepted. | `0_architecture/`, `5_workspace/`, future decision area. | Must cite evidence and alternatives. | Decision or governance process accepts, rejects, defers, or supersedes it. | Editable by explicit proposal or architecture ticket. |
| `research` | Investigation, comparison, analysis, or hypothesis. | Evidence only. | `1_research/`, selected `0_architecture/` evidence sections, future research docs. | Must cite sources, methods, uncertainty, and date/freshness when relevant. | Can inform proposal or canonical architecture after review. | Editable by research ticket; cannot be edited to imply authority. |
| `evidence` | Supporting material, observations, reviews, outputs, or references. | Evidence only until promoted. | `1_research/`, `4_external/` metadata/reviews, `9_artifacts/` local-only outputs, architecture appendices if curated. | Must cite source path, command, registry, review, or origin. | Reviewed evidence can support decisions or canonical docs. | Edit only to correct provenance, add review notes, or curate by ticket. |
| `projection` | Derived view for humans, agents, providers, or tools. | Not source authority by default. | `6_docs/`, `5_workspace/context-packs/` later, generated/local-only areas. | Must cite source authority and generation/projection method where applicable. | Can become canonical only after independent review and governance. | Regenerate or edit by docs/context ticket; must not silently change source meaning. |
| `migration_evidence` | Historical input preserved for migration analysis. | Historical evidence only. | `previusknowledge/`, migration notes, audit references. | Must cite original path and W-02 classification where used. | Restate selected concepts into current docs after review. | Do not edit original corpus unless explicit migration ticket permits it. |
| `external_reference` | Third-party source, provider, harness, engine, example, or review material. | External evidence only. | `4_external/sources/` local-only, `4_external/reviews/` later, `1_research/external-sources/` later. | Cite W-03 registry, external source path if inspected, license/provenance where relevant. | Promotion requires provenance, license, security, validation, and governance review. | Do not edit raw external sources; review docs editable by source-review ticket. |
| `product_scoped` | Product-specific documentation or architecture. | Authoritative only inside declared product scope after product policy. | `2_products/<product>/` later, product docs projections in `6_docs/` later. | Cite product scope, product source, product decisions, and root architecture constraints. | Product governance can promote inside product scope; root promotion requires separate root decision. | Edit only by product ticket; root-impact changes require architecture review. |
| `implementation_note` | Notes about code, scripts, tools, runtime behavior, packages, SDKs, or technical details. | Descriptive evidence or guidance; not architecture by default. | `3_platform/`, `10_scripts/`, `11_tools/`, `12_tests/`, `13_packages/`, `14_sdk/`, `6_docs/` later. | Cite source files, tests, commands, and architecture constraints. | Can inform architecture only after validation and review. | Edit by implementation or docs ticket; must not override architecture. |
| `generated` | Produced by tools, agents, scripts, reports, exports, or model output. | Generated evidence/projection only. | `9_artifacts/`, local outputs, future generated docs areas, context-pack projections. | Cite generator, input sources, command, timestamp if available, and uncertainty. | Review, validate, and promote selected content into non-generated docs if accepted. | Regenerate by task only; do not manually treat as source. |
| `historical` | Preserved past state or historical record. | Historical evidence only. | `previusknowledge/`, future archive area, decision history. | Cite original source and reason retained. | May inform current docs through restatement. | Preserve unless governance approves update, archive, or replacement. |
| `superseded` | Replaced by newer accepted authority. | Not current authority except for historical trace. | Original location with status update later, future archive area, decision history. | Must cite superseding document or decision. | Reconsider only through new proposal or governance. | Edits should be minimal and lifecycle-focused. |
| `deprecated` | Known material discouraged for new work due to risk, age, or replacement. | Not recommended; may still be cited for history or compatibility. | Original location, future archive, implementation notes, docs. | Must cite deprecation reason and replacement if one exists. | Can be superseded, archived, restored, or removed only by governance. | Edit only to clarify risk, replacement, or lifecycle. |
| `archived` | Retired and retained for audit/reference. | Archive evidence only. | Future `_archive/` or equivalent only after archive policy. | Must cite original path, archive reason, date, and decision. | Restoration or reuse requires governance review. | Read-only by default; edits require archive policy. |

Status rules:

| Rule | Meaning |
| --- | --- |
| Status is explicit. | Future docs should declare one primary status in the metadata header. |
| Status is scoped. | `canonical` without scope is invalid for authority-sensitive use. |
| Status can change. | Promotion, supersession, deprecation, and archive transitions must preserve provenance. |
| Missing status is evidence-only. | If status is absent, agents should not infer authority from filename, folder, or recency. |

## 4. Documentation Scope Model

Scope labels declare where a document may apply. A document may have one primary scope and additional related scopes, but authority must remain explicit.

| Scope | Owner | Allowed authority | Default folder | What it must never own |
| --- | --- | --- | --- | --- |
| `workspace_root` | Workspace architecture and governance. | Root identity, vocabulary, authority boundaries, documentation structure, migration controls, topology, and cross-workspace rules. | `0_architecture/workspace/` | Product behavior, external source truth, implementation behavior, provider behavior, raw generated output, secrets. |
| `architecture_domain` | Domain architecture owner or workspace architecture. | Domain principles and boundaries for agents, context, adapters, providers, runtime, workflows, governance, validation, security, and Cognitive Semantic System concepts. | Future `0_architecture/<domain>/` | Source code authority, product-specific behavior, external provider behavior, final substrate decision without explicit decision record. |
| `product_workspace` | Product owner or product governance. | Product architecture, product docs, product behavior explanations, product validation evidence inside declared product scope. | Future `2_products/<product>/docs/` or product projection in `6_docs/` | AGENT PLATFORM root authority, generic platform architecture, global governance, provider truth. |
| `research_scope` | Research owner or investigator. | Evidence, hypotheses, comparisons, findings, and recommendations. | `1_research/` | Decisions, promotions, product authority, root policy, implementation approval. |
| `external_source` | External source review owner. | External provenance, role, license posture, risk, reviewed claims, and relevance evidence. | Future `4_external/reviews/`, `4_external/licenses/`, `1_research/external-sources/` | Internal dependency approval, active instructions, root architecture, execution permission. |
| `migration_scope` | Migration owner or workspace architecture. | Migration plan, source classification, target mapping, audit references, and transition rules. | `0_architecture/workspace/` and future migration/audit docs | Bulk movement approval by itself, product migration before policy, archive movement without archive policy. |
| `operational_scope` | Workspace operations owner. | Process notes, context-pack projections, runbooks, task scaffolds, and operational coordination. | Future `5_workspace/process/` and `5_workspace/context-packs/` | Canonical root architecture by default, hidden policy, secrets, validation approval. |
| `implementation_scope` | Implementation owner after implementation tickets exist. | Implementation notes, code-facing docs, tests, scripts, tool behavior, package/SDK notes. | `3_platform/`, `10_scripts/`, `11_tools/`, `12_tests/`, `13_packages/`, `14_sdk/` | Architecture by code existence, root governance, product acceptance, external dependency approval. |
| `human_docs` | Documentation owner. | Human-facing explanations, user guides, developer guides, tutorials, references, and operations guides. | `6_docs/` | Canonical architecture unless explicitly marked canonical and governed, hidden source of policy, root truth by readability. |
| `local_only` | Local workspace owner or task owner. | Local evidence, generated outputs, datasets, models, artifacts, and private work-in-progress. | `2_products/` for now, `4_external/sources/`, `7_datasets/`, `8_models/`, `9_artifacts/`, runtime output folders | Commit-ready source, public docs, root authority, secrets exposure, dependency approval. |

Scope rule:

```text
The broadest visible audience of a document does not define its authority. Declared
scope, status, and governance define its authority.
```

## 5. Target Documentation Areas

The following target areas define the intended documentation structure. W-09 does not create these folders.

| Target area | Intended documentation | Default status posture | Notes |
| --- | --- | --- | --- |
| `0_architecture/workspace/` | Workspace-root architecture, W-series docs, documentation structure, migration controls, topology, context strategy, cognitive model. | `canonical`, `proposal`, or `draft` depending on header. | Current W-series root authority surface. |
| `0_architecture/decisions/` | Future decision records and ADRs. | `canonical`, `proposal`, `superseded`, `deprecated`, `historical`. | Do not create ADRs in W-09. |
| `0_architecture/agents/` | Agent role, permission, coordination, memory, handoff, output, and operating rules architecture. | Usually `canonical` or `draft`. | W-10 is expected to consume W-09 before defining agent rules. |
| `0_architecture/context/` | Context model, source classes, pack generation, lifecycle, sensitivity, projections, retrieval, and eligibility. | Usually `canonical` or `draft`. | Builds on W-05 and W-06. |
| `0_architecture/adapters/` | Adapter mediation posture, provider-facing translation, compatibility, projection, and risk boundaries. | Usually `canonical` or `draft`. | Must remain provider-neutral. |
| `0_architecture/providers/` | Provider abstraction, capability classification, external provider boundaries, and revalidation rules. | Usually `canonical` or `draft`. | Provider facts require current evidence. |
| `0_architecture/runtime/` | Runtime participation, execution posture, trace, exposure, and mediation architecture. | Usually `canonical` or `draft`. | Runtime does not own truth. |
| `0_architecture/workflows/` | Workflow coordination posture, task flow, orchestration, handoff, and validation linkage. | Usually `canonical` or `draft`. | Workflow is not an engine decision by default. |
| `0_architecture/governance/` | Promotion, approval, exception, ownership, lifecycle, and policy architecture. | Usually `canonical` or `proposal`. | Governance decides authority-sensitive outcomes. |
| `0_architecture/validation/` | Proof levels, validation registry concepts, evidence retention, check posture, and validity rules. | Usually `canonical` or `proposal`. | Validation evaluates, not approves. |
| `0_architecture/security/` | Access, sensitivity, secrets, provider/tool exposure, shell/network/MCP constraints, and publication safety. | Usually `canonical` or `proposal`. | Security constrains action and context. |
| `0_architecture/cognitive-semantic-system/` or equivalent future neutral path | Cognitive Semantic System authority concept, lifecycle, provenance, context eligibility, substrate evaluation, projections, sync, and accepted semantic truth. | Usually `canonical`, `proposal`, or `research`. | Name remains provisional; final substrate is undecided. |
| `1_research/` | Research evidence, investigations, comparisons, hypotheses, papers, and source studies. | `research` or `evidence`. | Current inventory includes `ai/`, `digital twins/`, `engineering/`, `natural systems/`, and `papers/`. |
| `4_external/reviews/` | Future external source reviews, provenance summaries, risk notes, and relevance assessments. | `external_reference`, `evidence`, or `research`. | Reviews may be tracked; raw sources remain local-only. |
| `4_external/licenses/` | Curated license and notice metadata. | `evidence` or `external_reference`. | Legal approval is not implied. |
| `5_workspace/context-packs/` | Future task-scoped context-pack projections. | `projection`, `generated`, or operational evidence. | Context packs are not truth or permission. |
| `5_workspace/process/` | Workspace process notes, task scaffolds, migration process, and operational conventions. | `operational_scope`, `draft`, `projection`, or `canonical` only if promoted. | Should not hide governance policy. |
| `6_docs/user-guide/` | Future user-facing guides. | Usually `projection`. | Must cite source architecture or product docs. |
| `6_docs/developer-guide/` | Future developer-facing guides. | Usually `projection` or `implementation_note`. | Must not override architecture or code validation. |
| `6_docs/tutorials/` | Future tutorials and walkthroughs. | Usually `projection`. | Examples need status and source citations. |
| `6_docs/reference/` | Future reference docs derived from architecture, implementation, SDKs, or APIs. | `projection`, `implementation_note`, or `canonical` only if governed. | Must identify source of truth. |
| `6_docs/operations/` | Human-facing operations guides and runbooks. | `projection` or `operational_scope`. | Operational docs must cite policy and architecture sources. |
| `_archive/` later only | Future archived, superseded, retired, or historical material. | `archived`, `historical`, `superseded`, or `deprecated`. | Do not create until archive policy exists. |

Target area rules:

| Rule | Meaning |
| --- | --- |
| Existing target areas are not automatically active. | Some target paths are future-only and must not be created in W-09. |
| Documentation areas are projections of responsibility. | They organize docs; they do not decide truth. |
| `6_docs/` is explanation-first. | It should project current authority for humans, not compete with it. |
| `0_architecture/` is authority-oriented. | It may contain canonical architecture when status, scope, and currency are explicit. |

## 6. Architecture Documentation Structure

Canonical architecture docs should be organized by authority scope and domain responsibility.

| Architecture family | Intended home | Content | Authority rule |
| --- | --- | --- | --- |
| Workspace architecture | `0_architecture/workspace/` | Root identity, vocabulary, responsibility, context strategy, cognitive model, topology, migration, documentation structure, and future W-series root policies. | Current W-series docs here remain the human-readable root authority surface. |
| Domain architecture | Future `0_architecture/<domain>/` | Agents, context, adapters, providers, runtime, workflows, governance, validation, security, and Cognitive Semantic System domains. | Canonical only when marked `canonical`, scoped, current, cited, and reviewed. |
| Decision records | Future `0_architecture/decisions/` | ADRs, accepted options, supersession, deprecation, and governance-sensitive choices. | Decisions must cite evidence and state impact. |
| Governance, validation, and security architecture | Future `0_architecture/governance/`, `0_architecture/validation/`, `0_architecture/security/` | Promotion workflow, proof levels, evidence retention, access, sensitivity, secrets, tool/network/provider constraints. | These constrain migration, implementation, context, and docs after promotion. |
| Semantic authority architecture | Future neutral Cognitive Semantic System area | Accepted semantic truth concept, provenance, lifecycle, context eligibility, drift, projections, and substrate evaluation. | Do not assume graph or any other final substrate. |
| Migration architecture | `0_architecture/workspace/` and future migration docs | Migration sequence, source classification, target mapping, restatement rules, and audit requirements. | Defines process, not movement by itself. |
| Implementation readiness architecture | Future architecture and validation docs | Readiness criteria before code, scripts, tools, tests, packages, SDKs, or product implementation. | Implementation code must not define architecture. |

Architecture documentation rules:

| Rule | Required behavior |
| --- | --- |
| Keep W-series visible. | `0_architecture/workspace/` remains the current W-series root authority surface until superseded. |
| Split by domain only after structure is clear. | Future domain docs may live under `0_architecture/<domain>/`, but W-09 does not create folders. |
| Avoid architecture duplication. | Later docs should synthesize and cite W-series docs, not copy them wholesale. |
| Preserve implementation independence. | Architecture can describe readiness and boundaries before implementation exists. |
| Keep semantic authority neutral. | Use Cognitive Semantic System terminology and keep substrate options open. |

## 7. Decision / ADR Structure

Decision records should capture accepted choices, rejected alternatives, evidence, validation impact, governance impact, security impact, migration impact, and lifecycle.

Do not create ADRs in W-09.

Future decision record format:

| Field | Required content |
| --- | --- |
| Decision title | Short name of the decision. |
| Status | `proposal`, `canonical`, `superseded`, `deprecated`, `historical`, or other status from the W-09 model. |
| Scope | One or more scope labels such as `workspace_root`, `architecture_domain`, `product_workspace`, or `external_source`. |
| Context | Problem, constraints, prior decisions, and why the decision is needed. |
| Options considered | Alternatives, including do-nothing and deferral where relevant. |
| Decision | The selected option and precise boundary of acceptance. |
| Rationale | Why the selected option is preferred, including tradeoffs. |
| Evidence references | W-series docs, previous knowledge paths, research, external registry entries, source reviews, validation output, or product evidence. |
| Validation impact | Checks required, proof level affected, evidence retention, and validation gaps. |
| Governance impact | Approval path, owner, lifecycle, exceptions, promotion/demotion effect. |
| Security impact | Access, sensitivity, secrets, shell/network/MCP/provider exposure, privacy, and publication concerns. |
| Migration impact | Files or concepts affected, restatement needs, supersession, archive implications, local-only boundaries. |
| Supersession / deprecation | What this decision supersedes, deprecates, or leaves in place. |
| Owner | Human or governance owner for the decision. |
| Date | Creation and acceptance dates where applicable. |
| Stop rule / follow-up | What this decision authorizes, what it explicitly does not authorize, and required next ticket. |

Decision rules:

| Rule | Meaning |
| --- | --- |
| Decisions are scoped. | A product decision does not decide root architecture unless explicitly stated. |
| Decisions cite evidence. | A decision without evidence references is a proposal at most. |
| Decisions separate validation and governance. | Passing checks can inform but does not replace approval. |
| Decisions preserve alternatives. | Rejected options remain useful historical evidence. |
| Decisions can be superseded. | Supersession must point to the replacing decision and preserve old rationale. |

## 8. Research Documentation Structure

Research documentation is evidence. It may support claims, proposals, architecture, product work, external reviews, and decisions, but it does not govern by itself.

Research rules:

| Rule | Meaning |
| --- | --- |
| Research is evidence. | It can inform but cannot approve, promote, implement, or define authority alone. |
| Research must cite sources. | Claims must identify source material, method, freshness, and uncertainty where relevant. |
| Research can be promoted only through architecture or decision path. | Promotion requires restatement, validation posture, governance posture, and status/scope declaration. |
| Research uncertainty is mandatory. | Stale, incomplete, generated, external, or indirect evidence must be labeled. |
| Research should not hide product or external limits. | Product/domain and external-source findings must keep their scope. |

Suggested future research areas, not created by W-09:

| Area | Intended use | Default status |
| --- | --- | --- |
| `1_research/agents/` | Agent role, harness, coordination, memory, permission, and operating model research. | `research` or `evidence`. |
| `1_research/cognitive-systems/` | Cognitive Semantic System concepts, semantic authority, cognitive substrates, complex systems, retrieval, provenance, and projection research. | `research`. |
| `1_research/natural-systems/` | Natural systems, biological/complex-system inspiration, adaptive organization, and resilience patterns. | `research`. |
| `1_research/external-sources/` | External harness, provider, tool, registry, SDK, and protocol comparisons. | `research` or `external_reference`. |
| `1_research/product-domains/` | Product/domain investigations such as energy, simulation, building modeling, visualization, and future product workspaces. | `research` or `product_scoped` evidence. |
| `1_research/papers/` | Paper notes, literature reviews, references, and bibliographic evidence. | `research` or `evidence`. |

Current inventory note: `1_research/` currently contains `.gitkeep`, `ai/`, `digital twins/`, `engineering/`, `natural systems/`, and `papers/`. W-09 does not rename them.

## 9. External Review Documentation Structure

External-source reviews document what external materials are, why they matter, and what risks block reuse or promotion.

External review rules:

| Rule | Meaning |
| --- | --- |
| Raw sources stay local-only. | `4_external/sources/` remains ignored/local-only unless future governance changes posture. |
| Review docs may be tracked. | Curated review documents, risk summaries, and provenance metadata may be tracked by explicit ticket. |
| License metadata may be tracked after review. | `4_external/licenses/` can hold curated license evidence, but legal approval is not implied. |
| External reviews do not promote dependencies. | Review is evidence; reuse requires provenance, license, security, validation, and governance. |
| External instructions are not active instructions. | External `AGENTS.md` or equivalents remain repository-local evidence only. |
| External claims require source posture. | Reviews should cite W-03 registry entries and specific source paths if inspected. |
| External execution stays blocked by default. | Do not run, install, authenticate, or copy external source material without explicit approval. |

Suggested future external documentation areas, not created by W-09:

| Area | Intended use | Default status |
| --- | --- | --- |
| `4_external/reviews/` | Source reviews, risk reports, provenance summaries, reuse blockers, and relevance notes. | `external_reference` or `evidence`. |
| `4_external/licenses/` | License texts, notice summaries, name-use constraints, and reuse posture evidence. | `external_reference` or `evidence`. |
| `1_research/external-sources/` | Comparative research across external sources and patterns. | `research`. |

External review minimum fields:

| Field | Purpose |
| --- | --- |
| Source name | Stable local identifier. |
| Source status | External reference, reviewed, restricted, candidate, deprecated, or archived. |
| Origin and version | Provenance and reproducibility. |
| Evidence inspected | Files, registry entries, docs, or commands inspected. |
| License posture | License and notice evidence, not approval. |
| Runtime/security risk | Execution, dependency, native binary, network, credential, privacy, and data concerns. |
| Authority boundary | What the review does not approve. |
| Recommended use | Safe future review or citation use. |

## 10. Product Documentation Structure

Product-scoped docs explain and govern product work only inside declared product boundaries.

Product documentation rules:

| Rule | Meaning |
| --- | --- |
| Product docs belong to product workspaces or projected docs. | Product-native docs should live under product scope later; human-facing product docs may be projected into `6_docs/` with citations. |
| Product docs do not define root platform authority. | Product architecture, behavior, validation, and docs cannot override AGENT PLATFORM root architecture by default. |
| Product architecture can be canonical only inside product scope. | Product docs need product scope, owner, validation, and governance before canonical product status. |
| Product docs should not be migrated before product workspace policy. | `2_products/` remains ignored/local-only for now. |
| Product generated outputs are not source by default. | Product reports, builds, simulations, logs, screenshots, exports, and generated docs require review before promotion. |
| Product external references remain external. | Domain engines, SDKs, examples, and external docs require product-specific provenance, license, security, and validation review. |

Future product doc categories, not created by W-09:

| Category | Intended content | Authority posture |
| --- | --- | --- |
| Product charter | Product purpose, users, outcomes, constraints, and relationship to AGENT PLATFORM. | Product-scoped only. |
| Product architecture | Product components, services, interfaces, data, validation, operations, and dependencies. | Canonical only inside product scope after policy. |
| Product user docs | User-facing product guides projected from product authority. | Projection unless explicitly canonical. |
| Product developer docs | Developer setup, implementation notes, API references, tests, and troubleshooting. | Product-scoped or implementation note. |
| Product validation docs | Product test evidence, acceptance criteria, domain validation, and known limits. | Validation evidence, not global approval. |

Product rule:

```text
No product documentation migration should happen until product workspace policy
defines active products, Git posture, authority boundaries, and validation rules.
```

## 11. Human Documentation Projection

`6_docs/` is the future human-facing documentation area. It should make AGENT PLATFORM easier to use without becoming a competing authority layer.

Human documentation projection rules:

| Rule | Meaning |
| --- | --- |
| `6_docs/` is human-facing. | It should contain user guides, developer guides, tutorials, references, and operations docs after explicit documentation tickets. |
| Human docs cite source architecture. | Docs derived from architecture must cite the canonical architecture or decision records they explain. |
| Projection status is default. | Human docs should carry `projection` status unless explicitly promoted. |
| Human docs must not override `0_architecture/`. | If a guide conflicts with canonical architecture, the architecture wins until corrected or superseded. |
| Human docs can simplify, not alter. | They can translate architecture into readable guidance, but cannot change policy, scope, or authority silently. |
| Human docs should expose uncertainty. | If source authority is draft, proposal, research, or evidence, the guide must say so. |
| Generated human docs need generator provenance. | Generated docs cite source docs, generator/tool, date, and review status. |

Suggested future `6_docs/` projections, not created by W-09:

| Area | Intended use | Required citation posture |
| --- | --- | --- |
| `6_docs/user-guide/` | Human-facing use and navigation. | Cite workspace architecture and product docs where relevant. |
| `6_docs/developer-guide/` | Developer onboarding, implementation-facing explanations, and technical references. | Cite architecture, implementation notes, tests, and decision records. |
| `6_docs/tutorials/` | Walkthroughs and learning paths. | Cite source authority and mark examples as examples. |
| `6_docs/reference/` | Stable references projected from architecture, SDKs, APIs, or policies. | Cite canonical source and version/freshness. |
| `6_docs/operations/` | Human-readable operations procedures and runbooks. | Cite governance, validation, security, and process source docs. |

Projection invariant:

```text
If `6_docs/` says something different from current canonical architecture, treat the
human doc as stale projection evidence and correct it through a documentation ticket.
```

## 12. Previous Knowledge Restatement Rules

Previous knowledge is migration evidence. It can inform current documentation only through controlled restatement.

Restatement rules:

| Rule | Required behavior |
| --- | --- |
| Never copy previous docs wholesale. | Extract principles, models, decisions, and evidence; do not import old scope and labels. |
| Extract principles and models. | Carry forward durable concepts, not the old document as a current artifact. |
| Cite original path. | Every restated claim should cite the original `previusknowledge/` path and W-02 classification when material. |
| Normalize vocabulary. | Use AGENT PLATFORM, workspace, Cognitive Semantic System, product workspace, external reference, and current W-series terms. |
| Remove obsolete names. | Do not use prior prohibited semantic-authority names as current/future terms. |
| Preserve uncertainty. | State when evidence is historical, conflicted, product-scoped, external, stale, or unvalidated. |
| Declare status and scope. | Derived material needs its own current status and scope before use. |
| Mark current only after review. | Restated material becomes current only after review, validation posture, governance posture, and promotion where required. |
| Keep product material product-scoped. | Product docs classified `scope_limit` cannot become root authority by restatement. |
| Normalize substrate assumptions. | Prior graph-oriented material may provide candidate evidence, but no final substrate is decided. |

Restatement flow:

```text
Select W-02 classified source
-> extract claim/principle/model
-> identify current scope
-> normalize vocabulary
-> cite source and uncertainty
-> assign status and authority posture
-> validate against W-series docs
-> promote only through review/governance path
```

Restatement output types:

| Output type | Status before review | Status after approval |
| --- | --- | --- |
| Architecture restatement | `draft` or `proposal` | `canonical` within declared scope. |
| Research synthesis | `research` or `evidence` | Evidence for later proposal or decision. |
| Human guide projection | `projection` | Usually remains projection unless governed otherwise. |
| Product restatement | `product_scoped` draft or proposal | Product-scoped canonical only after product policy. |
| Migration note | `migration_evidence` or `evidence` | Audit or migration reference, not root authority by default. |

## 13. Documentation Metadata Header

Future docs should carry a consistent metadata header. W-09 defines the concept only and does not enforce a schema.

Required header fields:

| Field | Meaning |
| --- | --- |
| Title | Human-readable document title. |
| Status | One status label from the W-09 status model. |
| Scope | One or more scope labels from the W-09 scope model. |
| Authority | What this document can and cannot govern. |
| Source class | Canonical architecture, previous knowledge evidence, research, external reference, product-scoped, generated, implementation note, projection, or other current class. |
| Owner | Person, role, governance body, or placeholder owner. |
| Created date | Date the document was created. |
| Updated date | Date of latest substantive update. |
| Depends on | Documents, decisions, evidence, policies, or source classes required to interpret this document. |
| Supersedes | Prior documents or decisions replaced by this document. |
| Superseded by | Newer authority replacing this document, if any. |
| Related decisions | Decision records or ADRs tied to the document. |
| Validation status | Not evaluated, evidence-only, validated for scope, failed, stale, partial, or not applicable. |
| Governance status | Proposed, reviewed, approved, rejected, deferred, exception, or not applicable. |
| Security status | Public, internal, sensitive, restricted, contains no secrets, not reviewed, or other future access label. |
| Migration status | Native current doc, restated from previous knowledge, migration evidence, migrated, superseded, archived, local-only, or not applicable. |

Example conceptual header shape:

```text
Title: <document title>
Status: <status label>
Scope: <scope label>
Authority: <what this document governs and does not govern>
Source class: <source class>
Owner: <owner>
Created date: <YYYY-MM-DD>
Updated date: <YYYY-MM-DD>
Depends on: <paths or decisions>
Supersedes: <paths or decisions>
Superseded by: <paths or decisions>
Related decisions: <decision IDs or paths>
Validation status: <validation posture>
Governance status: <governance posture>
Security status: <security posture>
Migration status: <migration posture>
```

Metadata rule:

```text
The header is not decoration. It is the first authority boundary agents should read
before using a document.
```

## 14. Citation and Provenance Rules

Documentation claims must preserve provenance so agents and humans can distinguish evidence, claims, validation, governance, and authority.

Citation requirements:

| Claim type | Required citation |
| --- | --- |
| Migrated or restated claim | Original source document path, W-02 classification where applicable, and current restatement target. |
| External claim | W-03 registry entry, external review doc if present, source path if inspected, license/provenance posture where relevant. |
| Product claim | Product workspace path, product scope, product decision or product policy, and root architecture constraints. |
| Generated material | Generator/tool/agent, input sources, command or method if relevant, date if available, and review status. |
| Decision claim | Evidence references, options considered, rationale, validation impact, and governance impact. |
| Research claim | Source, method, date/freshness, uncertainty, and scope limits. |
| Architecture claim | Source architecture, prior decision, validation/governance posture, or explicit rationale if newly proposed. |
| Implementation claim | Source files, tests, commands, observed behavior, version, and architecture boundary. |
| Security/access claim | Security source doc, user instruction, access policy, risk review, or explicit uncertainty. |
| Uncertainty | Explicit statement of what is unknown, stale, generated, external, historical, or unvalidated. |

Provenance rules:

| Rule | Meaning |
| --- | --- |
| Cite material sources, not memory. | Conversation memory can guide continuity, but durable docs need file or decision references. |
| Separate evidence from conclusion. | Evidence supports claims; it is not automatically the claim. |
| Cite source status. | A prior `canonical` label in previous knowledge is historical evidence, not current authority. |
| Cite validation separately. | Validation output should be linked as evaluation evidence, not approval. |
| Cite governance separately. | Approval, promotion, exception, and lifecycle decisions need their own references. |
| Cite projections as projections. | Context packs, generated docs, and human docs should point back to source authority. |

Citation invariant:

```text
A claim that materially affects architecture, migration, product scope, external
reuse, validation, governance, or security must be traceable to evidence or clearly
marked as a proposal.
```

## 15. Documentation Lifecycle

Documentation lifecycle describes maturity and retention. It is not Git status.

| Lifecycle state | Meaning | Allowed transition |
| --- | --- | --- |
| `proposed` | Idea, outline, or candidate document structure. | Draft, reject, defer, or supersede. |
| `drafted` | Written but not reviewed or accepted. | Review, revise, reject, defer, or promote to proposal/canonical. |
| `reviewed` | Checked for scope, citations, authority posture, and risks. | Promote, revise, reject, deprecate, or supersede. |
| `canonical` | Accepted and current within declared scope. | Supersede, deprecate, archive, revise by ticket. |
| `superseded` | Replaced by newer authority. | Archive, retain historical, or reconsider by new proposal. |
| `deprecated` | Discouraged due to risk, age, replacement, or changed direction. | Supersede, archive, restore by governance, or retain with warning. |
| `archived` | Retired and retained for audit/reference. | Restore or cite only by archive/governance process. |

Lifecycle clarifications:

| Clarification | Rule |
| --- | --- |
| Lifecycle is not Git status. | A file can be untracked and canonical, tracked and obsolete, or ignored and useful evidence. Git does not decide authority. |
| Archive is not trash. | Archive retains provenance, reason, date, and decision. It is not deletion or concealment. |
| Supersession preserves provenance. | Superseded docs should identify the replacing authority and remain traceable. |
| Deprecation explains risk or replacement. | Deprecated docs should state why new work should avoid them and what to use instead if known. |
| Canonical can become stale. | Current authority needs review when dependencies, decisions, source evidence, or workspace policy change. |

Lifecycle rule:

```text
Lifecycle transitions must be explicit because stale authority is more dangerous
than obvious draft material.
```

## 16. Documentation Anti-patterns

| Anti-pattern | Failure mode | Required correction |
| --- | --- | --- |
| Docs folder equals authority | Treats `6_docs/` or any docs path as truth by location. | Use status, scope, citations, and source authority. |
| README equals architecture | Treats root `README.md` as full authority. | Use README as entry point and cite canonical architecture. |
| Copy old docs wholesale | Imports stale scope, old labels, and conflicts. | Restate selected concepts with citations and current vocabulary. |
| Product docs define root | Lets product-specific needs override platform architecture. | Keep product docs product-scoped. |
| Research becomes decision | Treats findings as accepted choices. | Route through proposal, validation, and governance. |
| External README becomes truth | Treats external source claims as internal architecture. | Use W-03 and external reviews as evidence only. |
| Generated docs become source | Treats generated summaries as current authority. | Label generated material and promote only after review. |
| Status missing | Agents infer authority from path or tone. | Require metadata status and treat missing status as evidence-only. |
| Scope missing | A local claim becomes global accidentally. | Require scope labels and authority limits. |
| No citations | Claims cannot be validated or audited. | Add source, evidence, validation, and governance references. |
| Stale docs remain canonical | Old current docs continue to govern after dependencies changed. | Review, supersede, deprecate, or archive explicitly. |
| Canonical by filename | A file named `canonical_*` is treated as authority. | Use declared status, scope, and governance instead. |
| Human guide overrides architecture | Readable docs drift from source authority. | Treat guide as stale projection and correct it. |
| Implementation note becomes policy | Code-facing notes silently define governance. | Move policy into architecture/governance docs. |
| Substrate by folder name | A semantic-system path implies graph or another storage choice. | Keep Cognitive Semantic System substrate undecided until decision. |

Anti-pattern rule:

```text
Documentation drift starts when readers stop asking status, scope, citation, and
authority questions. W-09 makes those questions mandatory.
```

## 17. Migration Targets For Future Work

W-09 maps future migration targets. It does not migrate anything.

| Source classification | Future target | Target status before review | Promotion condition | W-09 action |
| --- | --- | --- | --- | --- |
| `carry_forward` principles | Current architecture docs under `0_architecture/workspace/` or future `0_architecture/<domain>/`. | `draft` or `proposal`. | Restated in current vocabulary, cited, reviewed, validated, and governed. | Define target only. |
| `scope_limit` product docs | Future product workspace docs or product projections in `6_docs/`. | `product_scoped` draft/proposal. | Product workspace policy, product owner, validation, and product governance. | Defer movement. |
| `conflicted` semantic material | Future neutral Cognitive Semantic System architecture docs. | `proposal`, `research`, or `draft`. | Naming normalized, substrate not pre-decided, validation/governance path defined. | Define target only. |
| `external_reference` docs | External review docs, research docs, adapter/provider evidence docs. | `external_reference`, `research`, or `evidence`. | Current source revalidation, provenance, license/security posture, and scope. | Define target only. |
| `migration_evidence` | Migration notes, audit references, or historical citations. | `migration_evidence` or `evidence`. | Useful trace retained with original path and reason. | Define target only. |
| Generated outputs | Evidence/projection areas only after review. | `generated`, `projection`, or `evidence`. | Source/generator provenance, validation, governance if promoted. | Exclude by default. |
| Current W-series docs | `0_architecture/workspace/` current authority surface. | Already status-labeled by each document. | Future supersession only through explicit architecture decision. | Preserve in place. |
| External source metadata | Future `4_external/reviews/` or registry metadata docs. | `external_reference` or `evidence`. | Provenance, license, risk, and review metadata. | Do not copy raw sources. |
| Product candidates | Future product workspace docs after policy. | `product_scoped` or local-only evidence. | Product policy and Git posture decision. | Do not move or commit. |

Future first documentation migration candidate:

| Candidate | Why first | Required guard |
| --- | --- | --- |
| Carry-forward source-of-truth, evidence, promotion, and documentation status principles | Low implementation risk and already aligned with W-01 through W-09. | Create a new current architecture doc by explicit ticket; cite previous sources; do not move old files. |

Migration target rule:

```text
Future documentation migration should create small current-scope restatements with
citations. It should not move old documents just to make folders look complete.
```

## 18. Readiness For W-10

Expected next ticket: `W-10 - Agent Operating Rules`.

W-10 can define agent rules after W-09 because agents need documentation status, scope, citations, and target areas before they can safely decide what to read, cite, edit, project, validate, or ignore.

Readiness assessment:

| Area | Verdict | Reason |
| --- | --- | --- |
| Documentation status model | Ready enough for W-10. | Agents can distinguish canonical, draft, proposal, research, evidence, projection, migration evidence, external reference, product-scoped, implementation note, generated, historical, superseded, deprecated, and archived docs. |
| Documentation scope model | Ready enough for W-10. | Agents can identify workspace root, architecture domain, product, research, external, migration, operational, implementation, human docs, and local-only scopes. |
| Citation/provenance rules | Ready enough for W-10. | Agents can be instructed to cite evidence, source status, validation, governance, and uncertainty. |
| Human documentation projection | Ready enough for W-10. | Agents can treat `6_docs/` as projection-first and avoid competing authority. |
| Previous knowledge restatement | Ready enough for W-10. | Agents can use W-02 and W-09 rules to restate rather than copy. |
| External review handling | Ready enough for W-10. | Agents can keep external reviews evidentiary and raw sources local-only. |
| Product documentation handling | Not ready for product migration. | Product workspace policy remains unresolved. |
| Archive handling | Not ready for archive movement. | Archive policy and folder do not exist. |
| Implementation handling | Not ready for code work. | Implementation tickets, validation registry, and security/access policy remain absent. |
| Agent permissions | Ready for architecture rules only. | W-10 can define operating rules, but not grant broad permissions or implement enforcement by itself. |

W-10 should consume:

| W-10 input | Why |
| --- | --- |
| W-01 workspace charter | Root identity, authority precedence, and agent boundaries. |
| W-04 responsibility map | Folder access and ownership posture. |
| W-05 context pack strategy | Context selection, exclusion, citation, edit rules, and stop behavior. |
| W-06 cognitive workspace model | Agent operating loop, evidence/claim model, and tool/capability distinction. |
| W-07 topology | Folder projection and local-only topology. |
| W-08 migration plan | Migration prohibitions and future sequence. |
| W-09 documentation structure | Documentation status, scope, citations, lifecycle, and projection rules. |

Readiness verdict:

```text
W-09 makes the workspace ready for W-10 agent operating rules at the architecture
level. It does not authorize implementation, broad agent permissions, product
migration, archive movement, external source reuse, staging, commits, or pushes.
```

## 19. Final Verdict

| Question | Answer |
| --- | --- |
| What is the canonical documentation structure? | Current root authority remains in `0_architecture/workspace/`; future architecture domains may live under `0_architecture/<domain>/`; decisions may live under a future decisions area; research remains under `1_research/`; external reviews may live under future `4_external/reviews/`; human docs may live under future `6_docs/` projections; archive remains future-only. |
| What is canonical now? | Current canonical W-series workspace architecture under `0_architecture/workspace/`, scoped by each document's status and authority header. |
| What remains evidence? | Previous knowledge, research, external sources and reviews, generated outputs, validation output, implementation notes, human doc projections, and product materials until promoted in scope. |
| What may be migrated later? | Carry-forward principles into current architecture docs, product-scope material into product docs after policy, conflicted semantic material into neutral Cognitive Semantic System docs, external references into reviews/research, and migration evidence into audit notes. |
| What must not be moved yet? | Previous documents, product workspaces, external source snapshots, generated outputs, datasets, models, artifacts, archive material, implementation code, docs projections, and any current W-series docs without explicit future ticket scope. |
| What should W-10 consume? | W-01 through W-09, especially W-04 access posture, W-05 context rules, W-06 agent/cognitive model, W-08 migration controls, and W-09 documentation status/scope/citation rules. |

Final W-09 statement:

```text
AGENT PLATFORM documentation must be status-labeled, scoped, cited, lifecycle-aware,
and projection-aware. Canonical architecture currently lives in
`0_architecture/workspace/`. Future docs may be organized by architecture domain,
decision record, research scope, external review, product scope, operations, or
human-facing projection, but no document becomes authoritative by folder, filename,
readability, generation, recency, or proximity. W-09 stops at structure definition
and does not start W-10.
```
