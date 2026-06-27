# AGENT PLATFORM Workspace Topology

Status: Canonical W-07 workspace output  
Date: 2026-06-27  
Scope: Topology proposal for the AGENT PLATFORM workspace as a projection of the cognitive model  
Authority: Physical workspace topology guidance only. This document does not move, rename, delete, migrate, implement, stage, commit, or push anything.

## 1. Purpose

Topology comes after W-04, W-05, and W-06 because physical folders should serve the workspace responsibility model, context strategy, and cognitive operating model.

W-04 defined what each workspace area owns, consumes, exposes, and must never own. W-05 defined how agents should receive selected context rather than reading the whole workspace. W-06 defined the cognitive model: goals, tasks, context, evidence, claims, constraints, capabilities, tools, memory, decisions, validation, governance, outputs, feedback, and learning.

W-07 turns those models into a topology proposal.

Clarifications:

- Topology serves cognition.
- Folders are projections.
- Folder location is not authority.
- Topology is not migration.
- Topology is not implementation.
- Topology is not a harness decision.
- Topology is not a cognitive substrate decision.
- The future `Cognitive Semantic System` remains the neutral temporary name for semantic authority.
- Graph remains a candidate substrate only.

Topology rule:

```text
Folders organize work so agents and humans can retrieve, scope, validate, govern,
and migrate safely. Folders do not decide what is true.
```

## 2. Topology Principles

| Principle | Rule |
| --- | --- |
| Agent-native first | Topology should help agents select context, cite evidence, avoid forbidden scope, and stop correctly. |
| Product-independent root | Root topology must not collapse into Digital Twin, Omniverse, EnergyPlus, OpenStudio, CLI, web, desktop, or any other product scope. |
| Evidence separated from authority | Architecture, research, previous knowledge, external references, generated outputs, and runtime evidence must stay distinguishable. |
| External sources isolated | External source snapshots stay under external boundaries and do not become dependencies by proximity. |
| Product workspaces contained | Products live in bounded product areas and cannot define root architecture by default. |
| Local-only heavy material excluded from Git | Product candidates, external source snapshots, datasets, models, artifacts, generated outputs, logs, credentials, and Office temp files stay local-only by default. |
| Context packs should be easy to assemble | Topology should make active authority, source classifications, external registry, and responsibility map easy to locate. |
| Canonical architecture should be easy to find | Current root architecture authority should remain under `0_architecture/workspace/` until superseded. |
| Implementation should not define architecture | Platform code, scripts, tools, packages, and SDKs must depend on architecture rather than replace it. |
| Folders must not override source status | A file remains canonical, evidence, external, generated, local-only, product-scoped, or implementation-scoped based on status and governance, not location alone. |

## 3. Current Topology Assessment

| Item | Observed contents / role | Classification | Current verdict |
| --- | --- | --- | --- |
| `0_architecture/` | Architecture domain folders and current W-series docs in `workspace/`. | Canonical architecture area. | Keep. Needs continued status discipline. |
| `1_research/` | Research areas for `ai/`, `digital twins/`, `engineering/`, `natural systems/`, and `papers/`. | Evidentiary area. | Keep. Needs research status policy. |
| `2_products/` | Product candidates: `backend-energyplus/`, `cli/`, `desktop/`, `experimental/`, `omniverse-app/`, `web-platform/`. | Product-scoped and local-only. | Keep temporarily. Needs product workspace policy. |
| `3_platform/` | Platform-domain implementation candidate folders: `adapters/`, `agents/`, `context/`, `federation/`, `graphify/`, `knowledge/`, `operations/`, `providers/`, `runtime/`, `security/`, `workflows/`. | Implementation-scoped. | Keep temporarily. Needs implementation policy and semantic naming review. |
| `4_external/` | `datasets/`, `licenses/`, `sources/`, `standarts/`. | External reference area. | Keep. Needs spelling/standards decision later; do not rename now. |
| `5_workspace/` | `.gitkeep` only. | Workspace operations placeholder. | Keep. Needs context-pack/workspace-operations policy. |
| `6_docs/` | `.gitkeep` only. | Human documentation placeholder. | Keep. Needs docs authority/status policy. |
| `7_datasets/` | Empty. | Local-only data area. | Keep temporarily. Local-only and ignored. Needs data policy. |
| `8_models/` | Empty. | Local-only model area. | Keep temporarily. Local-only and ignored. Needs model policy. |
| `9_artifacts/` | Empty. | Local-only generated/artifact area. | Keep temporarily. Local-only and ignored. Needs evidence-retention policy. |
| `10_scripts/` | Empty. | Script/automation area. | Keep. Needs execution and trust policy. |
| `11_tools/` | Empty. | Tooling area. | Keep. Needs tool lifecycle and trust policy. |
| `12_tests/` | Empty. | Test/validation support area. | Keep. Needs validation registry/proof policy. |
| `13_packages/` | Empty. | Package/release area. | Keep temporarily. Needs package ownership/release policy. |
| `14_sdk/` | Empty. | SDK/interface area. | Keep temporarily. Needs SDK boundary/compatibility policy. |
| `previusknowledge/` | Previous corpus with `docs/` and `research/`. | Migration evidence. | Keep temporarily. Migrate or archive later by explicit tickets. |
| `README.md` | Minimal workspace descriptor. | Entry-point documentation. | Keep. May later point to canonical docs. |
| `.gitignore` | Ignores Office files, `2_products/`, `4_external/sources/`, `7_datasets/`, `8_models/`, `9_artifacts/`, runtime/generated folders, dependency folders. | Git posture control file. | Keep. Do not modify in W-07. |

Current topology verdict:

```text
The current topology is usable as a provisional numbered projection. It should not
be treated as final, and no folder should be renamed or moved before a migration
plan exists.
```

## 4. Numbered Folder Model Decision

| Option | Description | Strengths | Risks | W-07 verdict |
| --- | --- | --- | --- | --- |
| A | Keep numeric prefixes. | Stable current paths, easy ordering, no migration risk now. | Numbers can imply priority or authority; long-term names may be less semantic. | Not final. Useful short-term. |
| B | Remove numeric prefixes. | Cleaner semantic names. | Requires broad rename/migration, link updates, agent retraining, and validation. | Not now. Too disruptive. |
| C | Hybrid: keep short-term, migrate later. | Preserves stability now while allowing future semantic cleanup. | Requires later migration plan and clear criteria. | Recommended. |
| D | Use semantic names plus ordering metadata. | Best long-term semantic clarity; order can move to metadata/context. | Requires metadata conventions and migration work. | Strong later candidate, not immediate. |

Recommendation: Option C, hybrid: keep numeric prefixes short-term and evaluate migration later.

Rationale:

- Current folders already exist and align with W-04 responsibility domains.
- Renaming before W-08 would violate the plan-before-migration posture.
- Numeric prefixes should be treated as navigation order only, not authority order.
- Later work can evaluate semantic names plus ordering metadata after migration criteria exist.

Decision rule:

```text
Keep the numbered folder model for now. Do not rename folders in W-07. Treat numeric
prefixes as provisional navigation aids, not authority or lifecycle ranking.
```

## 5. Target Topology Proposal

The current shape is close enough to the recommended target topology to preserve short-term. The target model adds policy clarity and an eventual archive area, not immediate physical changes.

| Proposed folder | Purpose | Authority posture | Git posture | Agent access posture | Context-pack relevance | Migration relevance |
| --- | --- | --- | --- | --- | --- | --- |
| `0_architecture/` | Canonical and candidate architecture, decisions, responsibility maps, cognitive model, topology, and domain boundaries. | Canonical only when file status, scope, and currency say so. | Track reviewed architecture docs. | Read allowed; write by ticket only. | Primary source for Workspace Architecture Packs. | Receives promoted/restated architecture, not wholesale dumps. |
| `1_research/` | Investigations, comparisons, papers, hypotheses, and source reviews. | Evidence only until promoted. | Track non-sensitive reviewed research by ticket. | Read allowed by task; write by research ticket. | Source for Research Packs and evidence sections. | Feeds architecture and product decisions after review. |
| `2_products/` | Bounded product workspaces and product-specific behavior. | Product-scoped only after product decision. | Currently ignored/local-only. | Read/write only by product ticket. | Source for Product Workspace Packs. | Product migration target only after policy. |
| `3_platform/` | Future platform implementation. | No architecture authority by code existence. | Track only after implementation tickets and validation. | Read by task; write prohibited until implementation ticket. | Source for Implementation Planning and Validation Packs after implementation begins. | May receive implementation after W-series readiness. |
| `4_external/` | External sources, external datasets, licenses, standards, and provenance. | External evidence only. | Track metadata/licenses selectively; keep `sources/` local-only. | Read by source-review task; write prohibited except provenance/registry work. | Source for External Source Review Packs through W-03 registry. | External material may be reviewed, promoted, scoped, or archived. |
| `5_workspace/` | Workspace operations, context-pack projections, task scaffolds, runbooks, and coordination artifacts. | Operational support only unless promoted. | Track reviewed lightweight operations docs; generated packs may be local-only. | Read allowed; write by workspace/context ticket. | Likely future home for physical context-pack projections. | May host migration process artifacts, not old corpus wholesale. |
| `6_docs/` | Human/user/developer documentation and guides. | Docs are not canonical architecture by default. | Track reviewed docs. | Read allowed; write by docs ticket. | Output target for human-facing projections from architecture. | Receives docs after authority source is clear. |
| `7_datasets/` | Data snapshots, curated datasets, and data evidence. | No authority by default. | Ignored/local-only by default. | Read/write only by data ticket. | Usually excluded from context packs unless explicitly scoped. | Needs data provenance policy before use. |
| `8_models/` | Models, checkpoints, embeddings, and model artifacts. | No authority by default. | Ignored/local-only by default. | Read/write/use only by model ticket. | Usually excluded from context packs. | Needs model provenance/safety policy. |
| `9_artifacts/` | Generated outputs, reports, exports, run/build artifacts. | Generated/evidence only until promoted. | Ignored/local-only by default. | Read/write by task only. | Validation Packs may cite selected artifacts. | Promoted evidence may be moved through explicit ticket later. |
| `10_scripts/` | Repeatable automation and helper scripts. | No authority by default. | Track only reviewed scripts. | Read allowed; run/write only by explicit ticket. | May support Validation or Agent Execution Packs. | Needs execution policy before broad use. |
| `11_tools/` | Internal tools, wrappers, and governed utilities. | No authority by default. | Track reviewed tools only. | Read allowed; run/write only by explicit ticket. | May support Tool/Capability context later. | Needs tool lifecycle policy. |
| `12_tests/` | Tests, validation helpers, fixtures, and proof support. | Validation evidence only. | Track reviewed tests. | Read/run/write by validation ticket. | Primary source for Validation Packs after implementation exists. | Needs validation registry and proof levels. |
| `13_packages/` | Package metadata, build definitions, release candidates. | No authority until release policy exists. | Track only reviewed package definitions. | Read/write/build only by package ticket. | Relevant for packaging/release context later. | Needs release policy. |
| `14_sdk/` | SDK interfaces, contracts, examples, and compatibility surfaces. | No authority until SDK boundary exists. | Track only reviewed SDK material. | Read/write/build only by SDK ticket. | Relevant for SDK/product integration packs later. | Needs SDK policy. |
| `_archive/` | Future retired, superseded, historical, or preserved material. | Archive evidence only. | Track only reviewed archive metadata/material. | Read by archive/migration task; write by archive ticket. | Supports migration trace and historical context. | Proposed only; do not create in W-07. |

Target topology recommendation:

```text
Keep the current numbered topology as the provisional target baseline, add no new
folders in W-07, and reserve `_archive/` as a future explicit migration target.
```

## 6. Cognitive Topology Mapping

| Cognitive primitive | May live physically | Must not live | Status posture |
| --- | --- | --- | --- |
| Goal | `0_architecture/`, `5_workspace/`, product docs under `2_products/` when product-scoped. | External source trees or generated artifacts as root authority. | Canonical only if accepted in scoped architecture/governance; otherwise intent/evidence. |
| Task | `5_workspace/` in future, ticket system, current user instruction, architecture docs when describing process. | Raw external source trees, datasets, models, artifacts. | Active task authority only for current scope. |
| Context | Future `5_workspace/context-packs/`, task prompts, selected W-series docs, future Cognitive Semantic System projections. | Whole workspace dumps, raw external trees by default. | Projection/evidence, not truth. |
| Evidence | `1_research/`, `previusknowledge/`, `4_external/`, `9_artifacts/`, validation outputs, selected product material. | Canonical architecture unless promoted/restated. | Evidence unless promoted. |
| Claim | Architecture docs, research docs, reports, validation summaries, user/task outputs. | Uncited memory as authority. | Claim until validated/governed. |
| Constraint | `0_architecture/`, user task instructions, `.gitignore`, governance/security docs when created. | Generated output or tool output as hidden policy. | Binding only from authoritative source. |
| Capability | `0_architecture/`, `3_platform/` after implementation, `10_scripts/`, `11_tools/`, external registry evidence. | External source presence as permission. | Ability description, not permission. |
| Tool | `10_scripts/`, `11_tools/`, `3_platform/` after implementation, external sources only after review. | Context packs or architecture docs as invocable mechanisms. | Tool output is evidence. |
| Memory | Future governed workspace/runtime area; future Cognitive Semantic System if implemented; local session state if explicitly scoped. | Canonical architecture by default, untracked local-only dumps as truth. | Working evidence until reviewed/promoted. |
| Decision | `0_architecture/decisions/`, `0_architecture/workspace/`, future governance records. | Research notes, generated summaries, external source claims. | Canonical only when accepted and scoped. |
| Validation | `12_tests/`, validation reports in `9_artifacts/`, future validation registry, architecture validation docs. | Governance records as a substitute for checks. | Evaluation evidence, not approval by itself. |
| Governance | Future governance docs under `0_architecture/` or `5_workspace/`, accepted decisions. | Agent output, tool output, subagent result, generated summary. | Approval/policy authority only when human-approved or governed. |
| Output | `9_artifacts/`, `6_docs/`, task responses, generated reports, product outputs under product scope. | Canonical root authority without promotion. | Generated/evidence until promoted. |
| Feedback | Task responses, review notes, issues, future `5_workspace/` process records. | Silent memory as policy. | Evidence until accepted. |
| Learning | Canonical architecture updates, reviewed process docs, future Cognitive Semantic System accepted knowledge. | Autonomous unreviewed memory mutation. | Accepted only after review/promotion. |

Mapping rule:

```text
A cognitive primitive may appear in many folders, but its authority posture follows
source status and governance, not location.
```

## 7. Context Pack Topology

| Option | Description | Strengths | Risks | W-07 recommendation |
| --- | --- | --- | --- | --- |
| `5_workspace/context-packs/` | Store task-scoped context-pack projections under workspace operations. | Keeps packs operational, separate from canonical architecture, easy for agents. | Could become stale or be mistaken for authority. | Recommended future physical home. Do not create yet. |
| `0_architecture/context/` | Store packs near architecture context concepts. | Close to architecture and status rules. | Context packs may be mistaken for canonical architecture. | Not recommended as default. |
| Generated local-only area | Store generated packs under `9_artifacts/` or local runtime output. | Keeps generated packs out of Git. | Harder to cite, reuse, and govern. | Useful for generated temporary packs only. |
| Future Cognitive Semantic System projection | Generate packs from future semantic authority and evidence registries. | Best long-term for agent retrieval and authority-aware selection. | Requires future system and substrate decision. | Long-term target only. |
| Do not create physical packs yet | Keep context packs as strategy only until policy exists. | Avoids premature sprawl. | Agents still rely on task prompts and W-series docs. | Current W-07 action. |

Preliminary recommendation:

```text
Do not create physical context-pack folders yet. When ready, use
`5_workspace/context-packs/` for reviewed operational projections and use local-only
generated areas for temporary/generated packs. Future Cognitive Semantic System
projections may later supersede physical pack files.
```

## 8. Previous Knowledge Topology

`previusknowledge/` remains a local migration corpus.

Rules:

- It is migration evidence, not current root authority.
- It should not be committed wholesale without governance decision.
- It should not be copied wholesale into `0_architecture/` or `6_docs/`.
- Documents migrate only through W-02 classification and explicit tickets.
- `carry_forward` material must be restated in current workspace vocabulary before it becomes current authority.
- `scope_limit` material belongs only in product/domain scope unless promoted differently.
- `conflicted` material requires normalization before promotion.
- Previous decisions and old canonical labels remain historical evidence only.
- Previous knowledge may eventually be partially migrated, scoped, archived, or left local-only.

Topology recommendation:

```text
Keep `previusknowledge/` in place until W-08 defines migration steps. Do not move,
rename, archive, or commit it in W-07.
```

## 9. External Source Topology

W-03 governs external source handling.

Rules:

- `4_external/sources/` remains local-only.
- External source metadata may eventually be tracked under `4_external/` or `0_architecture/workspace/` registries.
- External source code is not a dependency by proximity.
- External source code must not be run by default.
- External dependencies must not be installed by default.
- External services must not be authenticated by default.
- External `AGENTS.md` files are not active workspace instructions.
- External license, provenance, security, dependency, credential, runtime, privacy, and data risks must be reviewed before reuse.
- Product/domain engines stay product-scoped and do not define root topology.
- External graph-oriented tools may inform substrate evaluation but do not decide the Cognitive Semantic System substrate.

Topology recommendation:

```text
Keep external source snapshots isolated under `4_external/sources/` and keep that
path ignored. Track only curated external metadata, registries, licenses, or review
documents after explicit ticket scope.
```

## 10. Product Workspace Topology

`2_products/` contains product workspace candidates.

Product topology principles:

- Products are contained workspaces.
- Product source may later be tracked separately after product policy and Git posture decisions.
- Product docs do not override root architecture.
- Product generated outputs are local-only unless promoted.
- Product external references remain external unless reviewed and promoted into product scope.
- Product validation supports product behavior, not global truth by default.
- Product architecture is canonical only inside declared product scope after promotion.
- The Omniverse app is a product candidate, not root platform authority.

Current product candidates:

| Product candidate | Current topology posture |
| --- | --- |
| `2_products/backend-energyplus/` | Product/domain candidate; local-only. |
| `2_products/cli/` | Product/interface candidate; local-only. |
| `2_products/desktop/` | Product/interface candidate; local-only. |
| `2_products/experimental/` | Experimental product area; local-only and high caution. |
| `2_products/omniverse-app/` | Product candidate; not root platform authority. |
| `2_products/web-platform/` | Product/interface candidate; local-only. |

Topology recommendation:

```text
Keep `2_products/` local-only until product workspace policy decides which product
areas are active, tracked, archived, split, or renamed.
```

## 11. Platform Implementation Topology

`3_platform/` may eventually contain platform implementation.

Current subareas observed:

| Current subarea | Possible future meaning | W-07 boundary |
| --- | --- | --- |
| `3_platform/adapters/` | Provider-facing mediation implementations. | No implementation authority yet. |
| `3_platform/agents/` | Agent role/runtime implementations. | No implementation authority yet. |
| `3_platform/context/` | Context-pack or context-selection implementation. | No implementation authority yet. |
| `3_platform/federation/` | Future cross-workspace/federation implementation. | Needs architecture first. |
| `3_platform/graphify/` | Existing semantic-system-named implementation candidate folder. | Needs naming/substrate review; do not assume graph. |
| `3_platform/knowledge/` | Knowledge management implementation candidate. | Needs knowledge/authority model first. |
| `3_platform/operations/` | Operations implementation candidate. | Needs operations evidence lifecycle. |
| `3_platform/providers/` | Provider integration implementations. | Providers remain external capability owners. |
| `3_platform/runtime/` | Runtime implementation candidate. | Runtime does not own truth. |
| `3_platform/security/` | Security/access implementation candidate. | Needs access policy first. |
| `3_platform/workflows/` | Workflow implementation candidate. | Workflow is coordination posture until implementation ticket. |

Implementation rules:

- No implementation authority exists yet.
- No code should be added without an implementation ticket.
- Platform code must depend on architecture, not define it.
- Future subareas may include agents, context, adapters, providers, runtime, workflows, semantic system, governance, validation, and security.
- Existing implementation candidate folders should not force naming, substrate, or architecture decisions.

Topology recommendation:

```text
Keep `3_platform/` as an implementation-scoped placeholder. Do not add code or
rename semantic-system-related folders before architecture and migration tickets
authorize it.
```

## 12. Local-Only / Git Policy Topology

| Area or pattern | Git posture | Reason | Future handling |
| --- | --- | --- | --- |
| `0_architecture/` | Track reviewed architecture docs. | Current canonical workspace docs live here. | Commit by human approval only. |
| `1_research/` | Track reviewed non-sensitive research. | Research evidence can be useful. | Needs research status policy. |
| `previusknowledge/` | Keep local-only for now. | Migration corpus should not be committed wholesale. | W-08 should define migration/archive policy. |
| `2_products/` | Ignored/local-only. | Product candidates are not root authority and may be heavy/private. | Product policy must decide tracked subsets. |
| `3_platform/` | Track only after implementation ticket. | Implementation must not precede architecture. | Requires implementation planning and validation. |
| `4_external/sources/` | Ignored/local-only. | External source snapshots are risky, large, and licensing-sensitive. | Track metadata/reviews, not source snapshots by default. |
| `4_external/licenses/` | May be tracked after review. | License metadata can support provenance. | Needs external metadata policy. |
| `4_external/datasets/` | Treat as external data; likely local-only unless curated metadata. | Data can be large/licensed/sensitive. | Needs data policy. |
| `7_datasets/` | Ignored/local-only. | Data may be large, licensed, or sensitive. | Track only curated metadata after review. |
| `8_models/` | Ignored/local-only. | Models may be large, licensed, unsafe, or private. | Track only metadata after review. |
| `9_artifacts/` | Ignored/local-only. | Generated outputs are not source by default. | Promote selected evidence by ticket only. |
| Generated outputs | Ignore/local-only by default. | Outputs are evidence, not truth. | Promote only after validation/governance. |
| Secrets | Never commit. | Sensitive security material. | Use secure secret storage, not workspace files. |
| Credentials | Never commit. | Provider/API/account risk. | Use approved credential handling. |
| Office temp files | Ignore/local-only. | `~$*`, `*.xlsx`, `*.xls`, `desktop.ini`, `Thumbs.db` are local/OS/Office artifacts. | Do not commit by default. |
| Runtime logs | Ignore/local-only by default. | Logs can contain sensitive or partial evidence. | Retain/promote only by validation or governance ticket. |
| `10_scripts/` | Track reviewed scripts only. | Scripts can execute and mutate state. | Needs execution policy. |
| `11_tools/` | Track reviewed tools only. | Tools can affect trust and execution. | Needs tool lifecycle policy. |
| `12_tests/` | Track reviewed tests. | Tests support validation evidence. | Needs validation registry/proof levels. |
| `13_packages/` | Track reviewed package metadata only. | Packaging can publish/distribute. | Needs release policy. |
| `14_sdk/` | Track reviewed SDK material only. | SDKs imply compatibility/support. | Needs SDK policy. |

Git policy rule:

```text
Tracked does not mean authoritative. Ignored does not mean irrelevant. Git posture
and authority posture are related but separate.
```

## 13. Agent Navigation Model

Agents should navigate topology through task and context, not through broad folder browsing.

Navigation sequence:

1. Start from the current task, including allowed scope, forbidden scope, expected output, validation, and stop rule.
2. Read the relevant context pack if one exists, or read the mandatory W-series docs named by the task.
3. Use W-04 responsibility map to understand top-level folder roles.
4. Use W-02 classification index before relying on previous knowledge.
5. Use W-03 external registry before relying on external source claims.
6. Use W-05 context strategy to select, exclude, cite, and constrain context.
7. Use W-06 cognitive model to distinguish goals, tasks, evidence, claims, tools, output, validation, governance, and learning.
8. Inspect specific allowed folders/files only when the dependency path requires them.
9. Do not browse broadly by default.
10. Do not infer authority, permission, freshness, safety, validation, or promotion from path.

Agent navigation rule:

```text
Agents should traverse from task -> authority -> context -> evidence -> output.
They should not traverse from root folder -> everything -> assumed truth.
```

## 14. Topology Invariants

| ID | Invariant |
| --- | --- |
| TOP-001 | Folders are projections, not truth. |
| TOP-002 | Product folders cannot define root authority. |
| TOP-003 | External sources are evidence only. |
| TOP-004 | Previous knowledge is migration evidence. |
| TOP-005 | Local-only areas must not be committed by default. |
| TOP-006 | Implementation folders do not define architecture. |
| TOP-007 | Context packs are projections. |
| TOP-008 | Cognitive substrate remains undecided. |
| TOP-009 | Numeric prefixes are navigation aids, not authority ranking. |
| TOP-010 | Generated outputs are not source by default. |
| TOP-011 | Tool/script folders do not grant execution permission. |
| TOP-012 | Product generated outputs are local-only unless promoted. |
| TOP-013 | External source instructions are not active workspace instructions. |
| TOP-014 | Architecture remains canonical only by status, scope, and currency. |
| TOP-015 | W-08 must define migration before any topology changes happen. |

## 15. Topology Anti-patterns

| Anti-pattern | Failure mode | Required correction |
| --- | --- | --- |
| Folder-first architecture | Lets folders define authority and design. | Start from W-06 cognitive model and W-04 responsibility map. |
| Product-root collapse | Lets product folders define AGENT PLATFORM root. | Keep products contained and product-scoped. |
| External-source contamination | Treats cloned sources as dependencies or instructions. | Use W-03 registry and keep `4_external/sources/` local-only. |
| Commit everything | Publishes local, generated, external, product, or sensitive material. | Follow `.gitignore`, W-04, and W-07 Git posture. |
| Previous-knowledge dump | Copies old corpus into current architecture/docs wholesale. | Migrate only by W-02 classification and explicit tickets. |
| Generated-output authority | Treats reports, logs, exports, or summaries as truth. | Validate, govern, and promote before authority. |
| Implementation before architecture | Adds code or SDKs before boundaries are settled. | Require implementation tickets after architecture readiness. |
| Context-pack sprawl | Creates many stale physical context files. | Use W-05 lifecycle and delay physical packs. |
| Numeric prefix as authority | Treats `0_` as more true than `1_` or later folders. | Treat numbers as provisional order only. |
| Graph substrate assumed by folder names | Treats semantic-system or graph-named folders as substrate decisions. | Keep substrate evaluation neutral and use Cognitive Semantic System naming. |
| Scripts/tools as hidden policy | Lets executable helpers encode governance invisibly. | Document policy in architecture/governance, not only scripts. |
| Archive as trash | Moves unresolved material into archive to avoid decisions. | Archive only by explicit lifecycle/governance decision. |

## 16. Readiness For W-08

Expected next ticket: `W-08 - Migration Plan`.

Readiness assessment:

| Area | Verdict | Reason |
| --- | --- | --- |
| Responsibility model | Ready enough. | W-04 defines top-level area responsibilities and boundaries. |
| Context model | Ready enough. | W-05 defines context packs, source classes, exclusions, citations, and edit rules. |
| Cognitive topology | Ready enough. | W-06 defines cognitive primitives and folder projection relationship. |
| Physical topology proposal | Ready after W-07. | This document recommends keeping numbered topology short-term and migrating later by plan. |
| Previous knowledge migration | Ready for planning only. | W-02 classifies prior docs, but no file movement is approved. |
| External source migration | Ready for planning only. | W-03 isolates external source snapshots and promotion rules. |
| Product migration | Not ready for movement. | Product workspace policy and Git posture are unresolved. |
| Implementation migration | Not ready. | Implementation tickets and validation policy do not exist yet. |
| Archive migration | Not ready for movement. | `_archive/` is proposed only and should not be created until W-08 or later approves it. |

W-08 guidance:

```text
W-08 may define how to migrate files only after consuming W-07 target topology.
W-08 should not move files unless explicitly authorized by its own ticket.
```

## 17. Final Verdict

| Question | Answer |
| --- | --- |
| What is the recommended workspace topology? | Keep the current numbered top-level topology short-term as a provisional projection: `0_architecture/` through `14_sdk/`, with `_archive/` reserved as a future explicit migration target. |
| Is current topology usable? | Yes, temporarily, if folders are treated as projections and `.gitignore` local-only boundaries are respected. |
| Which folders are canonical now? | `0_architecture/workspace/` contains current canonical W-series workspace architecture. Other folders are evidentiary, product-scoped, local-only, implementation-scoped, operational, or placeholders unless explicitly promoted. |
| Which folders stay local-only? | `2_products/`, `4_external/sources/`, `7_datasets/`, `8_models/`, `9_artifacts/`, generated outputs, runtime logs, Office temp files, secrets, credentials, and `previusknowledge/` until governance decides otherwise. |
| What must W-08 consume? | W-00 through W-07, `.gitignore`, current root topology, W-02 classifications, W-03 external registry, W-04 responsibility map, W-05 context strategy, and W-06 cognitive model. |
| What must not be moved yet? | Everything. No folders, previous documents, products, external sources, generated artifacts, datasets, models, scripts, tools, tests, packages, SDKs, or archives should move before an explicit migration plan and approval. |

Final W-07 statement:

```text
The AGENT PLATFORM topology should remain stable while the workspace moves from
architecture toward migration planning. The current numbered folders are usable as
temporary projections, but cognitive authority lives in scoped canonical workspace
architecture and future governed semantic authority, not in folder paths.
```
