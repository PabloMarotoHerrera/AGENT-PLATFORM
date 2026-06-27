# AGENT PLATFORM Workspace Responsibility Map

Status: Canonical W-04 workspace output  
Date: 2026-06-27  
Scope: Current workspace top-level responsibility map before migration  
Authority: Responsibility, boundary, and access-posture guidance only. This document does not move, rename, delete, migrate, or implement anything.

## 1. Purpose

The workspace needs a responsibility map before migration because the current root already contains architecture, research, product candidates, platform-code candidates, external references, generated/data/model areas, local Office artifacts, previous knowledge, and future implementation placeholders. Without an explicit responsibility map, agents and humans may infer authority from folder names, numeric prefixes, recency, proximity, or prior repository conventions.

This map prevents folder confusion before any migration by defining what each top-level area owns, consumes, exposes, and must never own.

Core rules:

- Folders are projections of responsibility, not truth.
- Folders are not semantic authority by themselves.
- File location does not create authority, ownership, freshness, validation, or promotion.
- Product folders do not define the AGENT PLATFORM root.
- External folders do not define AGENT PLATFORM authority.
- Previous knowledge is migration evidence, not current root authority by default.
- Generated outputs, local files, spreadsheets, runtime state, and caches are not source by default.
- The future `Cognitive Semantic System` remains the neutral working name for semantic authority, and the final cognitive substrate is not decided. Graph remains a candidate substrate only.

## 2. Current Workspace Inventory

Top-level items observed in the workspace root:

| Item | Kind | Current classification | Evidence / notes |
| --- | --- | --- | --- |
| `.git/` | Folder | Ignored/local-only area | Git repository metadata. Not workspace content and not a committed artifact. |
| `.gitignore` | File | Active workspace control file | Defines ignored/local-only patterns including products, external sources, datasets, models, artifacts, Office files, and runtime/generated folders. |
| `~$DT.xlsx` | File | Ignored/local-only area; generated/runtime area | Office temporary lock file. Matches `.gitignore` pattern `~$*`. |
| `0_architecture/` | Folder | Active workspace area | Contains current canonical workspace architecture under `0_architecture/workspace/` plus architecture domain folders. |
| `1_research/` | Folder | Active workspace area | Contains research evidence areas: `ai/`, `digital twins/`, `engineering/`, `natural systems/`, `papers/`. |
| `10_scripts/` | Folder | Active workspace area; unclear / needs decision | Script area exists at root. Deep contents were not inspected in W-04. Execution policy is not defined yet. |
| `11_tools/` | Folder | Active workspace area; unclear / needs decision | Tooling area exists at root. Deep contents were not inspected in W-04. Execution and trust policy are not defined yet. |
| `12_tests/` | Folder | Active workspace area; unclear / needs decision | Test area exists at root. Deep contents were not inspected in W-04. Validation registry is not defined yet. |
| `13_packages/` | Folder | Active workspace area; unclear / needs decision | Package area exists at root. Deep contents were not inspected in W-04. Package ownership and release posture are not defined yet. |
| `14_sdk/` | Folder | Active workspace area; unclear / needs decision | SDK area exists at root. Deep contents were not inspected in W-04. SDK responsibility is not defined yet. |
| `2_products/` | Folder | Product workspace candidate; ignored/local-only area | Contains candidate product areas: `backend-energyplus/`, `cli/`, `desktop/`, `experimental/`, `omniverse-app/`, `web-platform/`. Ignored by `.gitignore`. |
| `3_platform/` | Folder | Active workspace area; unclear / needs decision | Platform implementation candidate exists at root. Deep contents were not inspected in W-04. Implementation authority is not defined yet. |
| `4_external/` | Folder | External reference area | Contains `datasets/`, `licenses/`, `sources/`, and `standarts/`. `4_external/sources/` is ignored by `.gitignore` and governed by W-03. |
| `5_workspace/` | Folder | Active workspace area | Workspace operations placeholder. Currently contains `.gitkeep` only. |
| `6_docs/` | Folder | Active workspace area | User/developer documentation placeholder. Currently contains `.gitkeep` only. |
| `7_datasets/` | Folder | Ignored/local-only area; generated/runtime area | Dataset area. Ignored by `.gitignore`. Not source by default. |
| `8_models/` | Folder | Ignored/local-only area; generated/runtime area | Model/checkpoint area. Ignored by `.gitignore`. Not source by default. |
| `9_artifacts/` | Folder | Ignored/local-only area; generated/runtime area | Artifact/output area. Ignored by `.gitignore`. Not source by default. |
| `desktop.ini` | File | Ignored/local-only area | OS metadata. Ignored by `.gitignore`. |
| `DT.xlsx` | File | Ignored/local-only area | Local spreadsheet. Matches `.gitignore` pattern `*.xlsx`. |
| `previusknowledge/` | Folder | Migration evidence | Previous knowledge corpus with `docs/` and `research/`. Not current root authority by default. Currently not made canonical by location. |
| `README.md` | File | Active workspace area | Minimal root descriptor for AGENT PLATFORM. Not a full authority document by itself. |

Inventory verdict:

```text
The current workspace structure is usable as a temporary responsibility projection.
It is not yet a complete authority, access, migration, or implementation model.
```

## 3. Responsibility Map

| Area | Purpose | Owns | Consumes | Exposes | Must never own | Authority posture | Git posture | Agent access posture | Migration posture |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `.git/` | Repository metadata managed by Git. | Commit graph, refs, index, Git internals. | Git commands and repository operations. | Repository state to Git tooling. | Workspace truth, architecture, source policy, product meaning, secrets. | No architecture authority. | Local-only; never committed as content. | Do not read or write directly except through approved Git commands. | Not migrated. |
| `.gitignore` | Declares local-only and ignored patterns. | Ignore rules for generated, product, external-source, Office, and dependency artifacts. | Workspace responsibility decisions and local artifact patterns. | Git exclusion behavior. | Architecture truth, product scope, security policy by itself. | Control file, not broad authority. | Commit-safe only by explicit ticket; W-04 does not modify it. | Read allowed; write only by explicit ticket and human approval. | May need future update after responsibility decisions. |
| `~$DT.xlsx` | Office temporary artifact. | Nothing durable. | Local Office process state. | Nothing intended for workspace consumers. | Source, evidence, authority, product data, architecture. | No authority. | Ignored/local-only by pattern. Must not be committed. | Write prohibited for agents; deletion only by explicit human request. | Not migrated. |
| `0_architecture/` | Current architecture surface for workspace, domains, decisions, and responsibility boundaries. | Canonical workspace architecture when marked canonical and scoped; architecture drafts and domain architecture evidence. | W-series inputs, previous knowledge evidence, external registry evidence, root inventory. | Human-readable architecture, boundaries, decisions, vocabulary, responsibility maps. | Runtime execution, generated outputs, product behavior, external source authority, secrets, unmanaged local state. | Highest current human-readable root authority lives in `0_architecture/workspace/`. | Commit-safe for reviewed architecture docs by ticket. | Read allowed; write allowed only by ticket. Human approval required for commits. | Receives promoted/restated architecture; should not receive wholesale previous knowledge dumps. |
| `1_research/` | Investigation and evidence area. | Research notes, comparisons, source reviews, hypotheses, findings. | External sources, papers, prior corpus, experiments, product/domain questions. | Evidence and recommendations. | Root authority, implementation approval, product truth, final security policy. | Evidence only until promoted into architecture or future semantic authority. | Commit-safe for non-sensitive research by ticket. | Read allowed; write allowed only by research ticket; human approval required for sensitive material. | May feed architecture after classification and promotion. |
| `10_scripts/` | Future script area for repeatable operations. | Approved helper scripts and task automation. | Architecture rules, tools, tests, workspace operations. | Script entrypoints and automation evidence. | Policy, authority, secrets, hidden execution behavior. | No authority by default. | Not ignored at root; commit-safe only after review. | Read allowed; write/run only by explicit ticket. Human approval required for risky execution. | Needs script governance before broad use. |
| `11_tools/` | Future internal tooling area. | Approved workspace tools, wrappers, and utilities. | Scripts, platform code, tests, external references after review. | Tool interfaces and helper capabilities. | Governance, semantic truth, external dependency approval, credentials. | No authority by default. | Not ignored at root; commit-safe only after review. | Read allowed; write/run only by explicit ticket; external tool use needs review. | Needs tool trust and lifecycle policy. |
| `12_tests/` | Future test and validation-support area. | Test suites, fixtures, validation helpers where approved. | Platform code, architecture acceptance criteria, product candidates. | Test results and validation evidence. | Governance approval, truth promotion, security permission. | Validation evidence only; not approval authority. | Not ignored at root; commit-safe for reviewed tests. | Read allowed; write/run only by ticket. | Needs validation registry and proof-level model. |
| `13_packages/` | Future package/distribution area. | Approved internal package definitions or packaging metadata. | Platform code, tools, SDK, release policy. | Package artifacts or metadata when governed. | Source-of-truth, unreviewed third-party packages, secrets, external registry trust. | No authority by default. | Not ignored at root; commit-safe only by package/release ticket. | Read allowed; write prohibited except explicit packaging ticket. | Needs package ownership and release posture. |
| `14_sdk/` | Future SDK area. | Approved SDK interfaces, examples, and integration contracts. | Platform implementation, docs, tests, product needs. | SDK-facing APIs and developer references when governed. | Root architecture authority, product behavior outside scope, provider authority. | No authority by default. | Not ignored at root; commit-safe only by SDK ticket. | Read allowed; write prohibited except explicit SDK ticket. | Needs SDK boundary and compatibility policy. |
| `2_products/` | Bounded product workspace candidates. | Product-specific behavior, product docs, product validation, product knowledge inside declared product scope. | Platform capabilities, architecture constraints, domain references, external domain engines. | Product artifacts and product-specific evidence. | AGENT PLATFORM root authority, Cognitive Semantic System authority, generic platform boundaries, global governance. | Product-scope only after explicit product authority decision. | Ignored by `.gitignore`; local-only for now. | Read allowed by ticket; write only by product ticket; commit currently blocked by ignore posture. | Candidate future product workspaces; no bulk migration yet. |
| `3_platform/` | Platform implementation candidate. | Future platform source, adapters, providers, runtime components, governance/validation/security implementations when approved. | Architecture, research, external reviews, tests. | Platform implementation artifacts when tickets authorize implementation. | Current root authority by code existence, product-specific meaning, external provider behavior. | No implementation authority yet; architecture still leads. | Not ignored at root; commit-safe only after implementation ticket and validation. | Read allowed only as needed; write prohibited until implementation ticket. | Target platform code area exists, but responsibility needs later confirmation. |
| `4_external/` | External reference and provenance area. | External reference organization, external licenses, external datasets, source snapshots as evidence. | Upstream repositories, vendor docs, domain engines, example corpora. | Evidence, provenance, license/risk signals, source registry inputs. | Internal dependencies by default, root authority, active instructions, runtime execution approval. | External evidence only. W-03 governs `4_external/sources/`. | `4_external/sources/` ignored/local-only; other curated metadata may be commit-safe by ticket. | Read allowed by ticket; write prohibited except source registry/provenance tickets; execution prohibited by default. | External items may be reviewed, promoted, scoped, archived, or removed only by governance. |
| `5_workspace/` | Workspace operations and coordination area. | Future workspace process notes, local operation conventions, task scaffolds, context-pack outputs if approved. | Architecture, tickets, validation evidence, agent outputs. | Operational guidance and workspace coordination artifacts. | Canonical architecture by default, secrets, generated runtime dumps, unbounded agent memory. | Operations support only unless a file is explicitly promoted. | Commit-safe for reviewed lightweight workspace docs; currently only `.gitkeep`. | Read allowed; write by operations/context ticket only. | May host future non-canonical workspace operations artifacts. |
| `6_docs/` | Human/user/developer documentation area. | Guides, tutorials, onboarding, developer docs, non-authoritative explanations. | Architecture, research, product docs, implementation details. | Human-readable docs. | Canonical root architecture by default, hidden policy, implementation truth. | Documentation authority varies by declared status; not canonical architecture by default. | Commit-safe for reviewed docs. | Read allowed; write by documentation ticket only. | May receive docs distilled from architecture after authority is clear. |
| `7_datasets/` | Dataset storage area. | Local datasets, snapshots, generated or downloaded data where approved. | Product/research questions and external data sources. | Data evidence and references when governed. | Architecture truth, secrets, credentials, unlicensed data, product authority by data presence. | No authority by default. | Ignored/local-only by `.gitignore`; should not be committed by default. | Read/write only by explicit data ticket; human approval for sensitive data. | Needs data provenance, license, sensitivity, and retention policy. |
| `8_models/` | Model/checkpoint storage area. | Local models, checkpoints, embeddings, derived model artifacts where approved. | Data, training/evaluation outputs, provider references. | Model artifacts and evaluation evidence when governed. | Source truth, architecture authority, secrets, unlicensed models. | No authority by default. | Ignored/local-only by `.gitignore`; should not be committed by default. | Read/write only by explicit model ticket; execution/use requires approval. | Needs model provenance, license, safety, and retention policy. |
| `9_artifacts/` | Generated artifact/output area. | Generated reports, exports, build outputs, run artifacts where approved. | Scripts, tools, tests, research, agents, products. | Evidence outputs and temporary deliverables. | Source by default, root authority, product truth, semantic truth. | Generated/evidence only until promoted. | Ignored/local-only by `.gitignore`; should not be committed by default. | Read/write only by explicit ticket; promotion requires review. | May preserve selected evidence elsewhere after validation and promotion. |
| `desktop.ini` | OS metadata. | Nothing durable. | Windows Explorer state. | Nothing intended for workspace consumers. | Source, authority, product data, architecture. | No authority. | Ignored/local-only by `.gitignore`. | Write prohibited; deletion only by explicit human request. | Not migrated. |
| `DT.xlsx` | Local spreadsheet artifact. | Local workbook data only. | Human local work. | Nothing canonical unless separately reviewed. | Source, root authority, product authority, data truth. | No authority by default. | Ignored/local-only by `.gitignore`. Must not be committed by default. | Read only by explicit ticket if needed; write prohibited by default. | May be classified later as data/evidence if explicitly requested. |
| `previusknowledge/` | Previous knowledge migration corpus. | Historical and prior-scope architecture/research evidence. | Old AgentLab/Digital Twin material and prior decisions. | Migration evidence for classification and carry-forward work. | Current root authority by default, direct replacement docs, implementation plan, product root. | Migration evidence unless explicitly restated/promoted. | Should remain local-only for now; do not commit wholesale without governance decision. | Read allowed by migration/classification tickets; write prohibited except explicit migration ticket. | May be classified, promoted, migrated, scoped, or archived later. |
| `README.md` | Root workspace descriptor. | Short workspace introduction. | Current workspace identity and canonical architecture references. | Entry-point description for humans. | Full authority model, product scope, external source approval, security policy. | Lightweight descriptive file; not canonical architecture by itself. | Commit-safe by documentation/workspace ticket. | Read allowed; write by explicit documentation/workspace ticket. | May be updated to point to canonical docs after W-series stabilizes. |

## 4. Canonical Workspace Areas

These are responsibility domains, not instructions to create or move folders.

| Domain | Intended responsibility | Current or likely folder projection | Authority posture |
| --- | --- | --- | --- |
| Architecture | Canonical principles, vocabulary, boundaries, responsibility maps, decisions, and architecture evidence. | `0_architecture/` | Canonical only when marked current, scoped, and authoritative. |
| Research | Investigations, comparisons, external/source analysis, hypotheses, and evidence. | `1_research/` | Evidence only until promoted. |
| Products | Bounded product workspaces with product behavior, product docs, product validation, and product knowledge. | `2_products/` | Product-scope only; no root authority by default. |
| Platform code | Platform implementation, adapters, providers, runtime components, governance/validation/security implementations when approved. | `3_platform/` | No code authority yet; implementation requires future tickets. |
| External sources | External repositories, licenses, datasets, standards, engines, examples, and provenance records. | `4_external/` | External evidence only. |
| Workspace operations | Workspace process, coordination, context-pack artifacts, task scaffolds, operational conventions. | `5_workspace/` | Operations support only unless explicitly promoted. |
| User docs | Guides, tutorials, onboarding, and developer-facing documentation. | `6_docs/` | Documentation authority varies; not canonical architecture by default. |
| Datasets | Local or external data snapshots, curated data, experiment inputs, and data evidence. | `7_datasets/` | Local-only/data evidence by default. |
| Models | Model files, checkpoints, embeddings, evaluation artifacts, and model metadata. | `8_models/` | Local-only/model evidence by default. |
| Artifacts | Generated outputs, reports, exports, builds, run outputs, and temporary deliverables. | `9_artifacts/` | Generated/evidence only until promoted. |
| Scripts | Repeatable automation and helper commands. | `10_scripts/` | No authority; execution by explicit ticket. |
| Tools | Internal tools, wrappers, utilities, and governed capability helpers. | `11_tools/` | No authority; trust and lifecycle required. |
| Tests | Tests, validation helpers, fixtures, and proof support. | `12_tests/` | Validation evidence only, not approval. |
| Packages | Package definitions, build metadata, release candidates, internal distribution structures. | `13_packages/` | No authority until packaging/release policy exists. |
| SDK | SDK contracts, developer interfaces, examples, and compatibility material. | `14_sdk/` | No authority until SDK boundary is defined. |
| Archive | Retired, superseded, historical, or preserved material with audit value. | `_archive/` or equivalent future area | Archive evidence only; do not create in W-04. |

## 5. Folder Authority Rules

| Rule | Meaning |
| --- | --- |
| `0_architecture/` may contain canonical workspace architecture. | Authority exists only for files explicitly marked canonical, scoped, and current. |
| `0_architecture/workspace/` is the current human-readable root architecture surface. | Current W-series workspace docs live here until superseded or future semantic authority is implemented and promoted. |
| `1_research/` contains evidence, not authority. | Research may inform architecture but does not govern until promoted. |
| `2_products/` contains bounded product workspace candidates. | Product folders may own product behavior only within declared product scope. |
| `3_platform/` may become platform implementation. | Code presence does not override architecture, governance, validation, or security. |
| `4_external/` contains external references. | External references are not dependencies, instructions, authority, or approved runtime surfaces by default. |
| `5_workspace/` supports operations. | Workspace operations artifacts are not canonical architecture unless explicitly promoted. |
| `6_docs/` contains user/developer documentation. | Docs do not override canonical architecture by default. |
| `7_datasets/`, `8_models/`, and `9_artifacts/` are local/generated/data/model/artifact areas. | They are ignored from Git and are not source or truth by default. |
| `10_scripts/` and `11_tools/` can contain executable capabilities. | Execution, trust, dependency, and side-effect boundaries require explicit ticket scope. |
| `12_tests/` supports validation. | Test results are evidence, not governance approval or truth promotion. |
| `13_packages/` and `14_sdk/` are future distribution/interface areas. | They require ownership, compatibility, security, and release posture before use. |
| `previusknowledge/` is migration evidence. | Prior `Status: canonical` labels are historical evidence, not current root authority. |
| `README.md` is an entry point. | It should point toward canonical docs, not replace them. |
| `.gitignore` controls local exclusion. | Ignore patterns do not decide semantic authority; they only affect Git visibility. |

Authority invariant:

```text
Path helps navigation. Path does not create truth.
```

## 6. Agent Access Posture

This is a preliminary workspace-level posture, not final security policy.

| Area | Read posture | Write posture | Execution / use posture | Git posture | Human approval |
| --- | --- | --- | --- | --- | --- |
| `.git/` | Avoid direct reads except via Git commands. | Write prohibited except approved Git operations. | Git commands only by explicit task. | Local-only. | Required for staging, commits, pushes, or history changes. |
| `.gitignore` | Read allowed. | Write only by explicit ticket. | Not executable. | Commit-safe if explicitly changed. | Required before modifying ignore policy. |
| `0_architecture/` | Read allowed. | Write allowed only by ticket. | Not executable by default. | Commit-safe for reviewed architecture docs. | Required for commits and authority-sensitive changes. |
| `1_research/` | Read allowed. | Write by research ticket only. | Experiments require explicit scope. | Commit-safe if non-sensitive and reviewed. | Required for sensitive or external-derived material. |
| `2_products/` | Read by product/migration ticket. | Write by product ticket only. | Execution prohibited unless explicitly approved. | Ignored/local-only currently. | Required before product commits or publication. |
| `3_platform/` | Read as needed by implementation/design tickets. | Write prohibited until implementation ticket. | Execution prohibited unless validation ticket permits. | Not ignored at root. | Required for implementation commits. |
| `4_external/` | Read allowed for source-review tickets. | Write prohibited except provenance/registry work. | External code must not be run by default. | `sources/` ignored/local-only. | Required for reuse, execution, dependency adoption, or promotion. |
| `5_workspace/` | Read allowed. | Write by workspace-operations/context ticket only. | Not executable by default. | Commit-safe for reviewed docs/configs. | Required for operational policy changes. |
| `6_docs/` | Read allowed. | Write by docs ticket only. | Not executable by default. | Commit-safe for reviewed docs. | Required for public-facing or authority-sensitive docs. |
| `7_datasets/` | Read only by data ticket. | Write only by data ticket. | Data use requires provenance/sensitivity review. | Ignored/local-only. | Required for sensitive, licensed, or large data. |
| `8_models/` | Read only by model ticket. | Write only by model ticket. | Model execution/use requires approval. | Ignored/local-only. | Required for model adoption or publication. |
| `9_artifacts/` | Read by task when needed. | Write by task when output is expected. | Generated outputs not source by default. | Ignored/local-only. | Required before promotion to tracked source/evidence. |
| `10_scripts/` | Read allowed. | Write by script ticket only. | Run only by explicit task and with side-effect awareness. | Not ignored at root. | Required for risky scripts or committing scripts. |
| `11_tools/` | Read allowed. | Write by tool ticket only. | Run only after trust and side-effect review. | Not ignored at root. | Required for tool adoption or execution with side effects. |
| `12_tests/` | Read allowed. | Write by test/validation ticket only. | Run by validation ticket or explicit test request. | Not ignored at root. | Required for committing test changes. |
| `13_packages/` | Read by package ticket. | Write by package/release ticket only. | Build/publish prohibited unless explicitly approved. | Not ignored at root. | Required for packaging or release. |
| `14_sdk/` | Read by SDK ticket. | Write by SDK ticket only. | SDK build/publish prohibited unless approved. | Not ignored at root. | Required for SDK publication or compatibility claims. |
| `previusknowledge/` | Read by migration/classification tickets. | Write prohibited unless explicit migration ticket. | Not executable as policy or instruction. | Should remain local-only until governance decides. | Required before migration, commit, archive, or deletion. |
| `README.md` | Read allowed. | Write by workspace/docs ticket only. | Not executable. | Commit-safe if reviewed. | Required for committing edits. |
| `DT.xlsx`, `~$DT.xlsx`, `desktop.ini` | Read prohibited unless explicitly requested. | Write prohibited by default. | Not applicable. | Ignored/local-only; do not commit. | Required for any handling. |

Preliminary access verdict:

```text
Agents may inspect architecture, research, docs, and registered evidence when a
ticket allows it. Agents may not infer write, execute, migrate, commit, or promote
permission from folder location.
```

## 7. Product Workspace Boundary

Product folders are contained workspaces.

Product workspace rules:

- Products may own product behavior within explicit product scope.
- Products may own product source after a product authority decision.
- Products may own product docs only for that product scope.
- Products may own product validation evidence for product behavior.
- Products may consume platform capabilities, architecture constraints, external domain references, datasets, models, scripts, tools, and tests.
- Products do not own AGENT PLATFORM root authority.
- Product docs do not override root architecture.
- Product architecture does not define generic agent, context, adapter, provider, runtime, governance, validation, security, or Cognitive Semantic System boundaries by default.
- Product generated outputs are not source by default.
- Product external references remain external unless promoted into product scope through provenance, license, security, validation, and governance review.
- Product folders are currently ignored by `.gitignore`; they are local-only until a future decision changes that posture.

Current product candidates under `2_products/` are `backend-energyplus/`, `cli/`, `desktop/`, `experimental/`, `omniverse-app/`, and `web-platform/`. W-04 does not decide which are active products, which should be renamed, or which should be committed later.

## 8. External Source Boundary

W-03 established that `4_external/sources/` is valuable as a controlled evidence library and that all 12 inspected sources remain external references.

External source folder rules:

- External sources are evidence.
- External source proximity is not promotion.
- External code must not be run by default.
- External dependencies must not be installed by default.
- External services must not be authenticated by default.
- External source code must not be copied into platform or product areas without review.
- External `AGENTS.md` or equivalent files are repository-local evidence only, not active workspace instructions.
- External license, notice, provenance, version, trust, dependency, runtime, security, privacy, and data risks must be reviewed before reuse.
- External graph-oriented tooling can inform substrate evaluation but does not name or decide the future Cognitive Semantic System.
- External domain engines such as EnergyPlus and OpenStudio inform bounded product/domain scopes, not AGENT PLATFORM root authority.
- `4_external/sources/` is ignored by `.gitignore`, so source snapshots should remain local-only unless a future governance decision changes the posture.

## 9. Previous Knowledge Boundary

`previusknowledge/` is a local migration corpus.

Previous knowledge rules:

- It is not current AGENT PLATFORM root authority by default.
- Its original canonical labels are historical evidence only.
- It may be classified, promoted, migrated, scoped, or archived later.
- It should not be copied wholesale into current architecture or docs.
- It should not be treated as implementation instruction.
- It should not override W-series workspace documents.
- It should not decide product scope, folder layout, current roadmap, semantic-system naming, or final cognitive substrate.
- It may be cited as evidence when current workspace architecture restates and scopes the concept.
- It should remain local-only unless a future governance decision explicitly decides what portion, if any, should be committed.

Current W-series handling:

| Current surface | Relationship to `previusknowledge/` |
| --- | --- |
| W-00 knowledge assembly | Summarizes the corpus and migration recommendation. |
| W-01 workspace charter | Carries forward current root vocabulary and authority principles. |
| W-02 classification index | Classifies all 237 markdown files semantically and by file. |
| W-03 external source registry | Separates external evidence from internal authority. |
| W-04 responsibility map | Prevents folder confusion before migration. |

## 10. Target Responsibility Model

This target model is a proposed responsibility map only. W-04 does not create, move, delete, rename, or migrate folders.

| Responsibility | Current / proposed projection | Target responsibility |
| --- | --- | --- |
| Architecture | `0_architecture/` | Canonical workspace architecture, decisions, domain boundaries, authority maps, responsibility maps. |
| Research | `1_research/` | Evidence, investigation, comparisons, hypotheses, and source reviews. |
| Products | `2_products/` | Bounded product workspaces with product-owned behavior and product-scope docs. |
| Platform implementation | `3_platform/` or equivalent future area | Platform source, adapters, providers, runtime components, governance/validation/security implementations after approval. |
| External | `4_external/` | External references, source snapshots, licenses, standards, datasets, provenance, and review evidence. |
| Workspace operations | `5_workspace/` | Operational conventions, context-pack artifacts, task coordination, workspace process support. |
| Human docs | `6_docs/` | User/developer documentation, guides, onboarding, and explanatory material. |
| Data/model/artifact areas | `7_datasets/`, `8_models/`, `9_artifacts/` | Local-only datasets, models, generated outputs, and retained evidence until reviewed/promoted. |
| Scripts | `10_scripts/` | Reviewable automation with explicit execution and side-effect boundaries. |
| Tools | `11_tools/` | Governed utilities and internal tools with trust and lifecycle controls. |
| Tests | `12_tests/` | Test suites and validation evidence support. |
| Packages | `13_packages/` | Future package metadata, build definitions, and release candidates. |
| SDK | `14_sdk/` | Future SDK interfaces, contracts, examples, and compatibility surfaces. |
| Archive | `_archive/` or equivalent future area | Historical, retired, superseded, or preserved material. Do not create in W-04. |

Target model verdict:

```text
The numbered folder model can be used temporarily as a projection of responsibility.
Later work may decide whether to keep, rename, archive, or split these areas.
```

## 11. Conflicts / Open Questions

| Conflict / question | Current status | Why it matters | Future handling |
| --- | --- | --- | --- |
| Numbered folder naming | Current root uses `0_` through `14_` prefixes. | Numeric ordering helps scanning but may encode premature lifecycle or priority assumptions. | Decide later whether numbered names remain. |
| Whether to rename folders later | No rename is approved. | Renames affect links, agent context, scripts, and human navigation. | Require migration plan and validation before rename. |
| Where previous knowledge should migrate | `previusknowledge/` remains migration evidence. | Wholesale migration would contaminate current authority. | Promote only scoped/restated concepts. |
| Where architecture vs user docs should live | `0_architecture/` and `6_docs/` are separate. | Docs may accidentally override architecture or duplicate it. | Define doc status and architecture-to-doc projection rules. |
| Where product docs should live | Product docs may belong inside product workspaces or `6_docs/` projections. | Product docs must not define root architecture. | Define product documentation policy. |
| Whether external sources should stay local-only | `4_external/sources/` is currently ignored. | Source snapshots are large, risky, and licensing-sensitive. | Keep local-only until governance approves any tracked subset. |
| How agent access should be enforced | W-04 only defines posture. | Policy without enforcement may drift. | Future security/access and context-pack work must define enforcement. |
| How the Cognitive Semantic System relates to folder projections | Future system is conceptual and unimplemented. | Semantic authority must not be confused with file paths. | Later tickets should define semantic authority, substrate evaluation, and projection/sync boundaries. |
| Product folders are ignored but active as candidates | `2_products/` exists and is ignored. | Product work may need versioned source later. | Decide product Git posture before product implementation. |
| Platform implementation area exists before implementation policy | `3_platform/` exists but has no current authority. | Code could be treated as architecture by proximity. | Require implementation tickets, tests, security, and governance before writes. |
| Scripts and tools can execute | `10_scripts/` and `11_tools/` exist. | Agents may run code with side effects. | Define execution posture and trust policy before broad use. |
| Data/model/artifact areas are ignored | `7_datasets/`, `8_models/`, `9_artifacts/` are local-only. | Useful evidence may be lost or untracked unless promoted deliberately. | Define evidence retention and promotion process. |
| Archive area does not exist | `_archive/` is only proposed. | Retired material needs a controlled place later. | Decide archive naming and policy before moving anything. |

Open-question rule:

```text
An unresolved responsibility question is a blocker for migration or promotion, not
permission to improvise structure.
```

## 12. Final Responsibility Verdict

| Question | Verdict |
| --- | --- |
| Is the current workspace structure usable temporarily? | Yes. It is usable as a provisional responsibility projection if agents obey authority, Git, access, and migration boundaries. |
| What is canonical now? | Current W-series workspace architecture under `0_architecture/workspace/`, especially the workspace charter, knowledge assembly, previous knowledge classification index, external source registry, and this responsibility map. Current ticket instructions also govern active task scope. |
| What must remain local-only? | `.git/`, Office temp/metadata files, `DT.xlsx`, `2_products/` for now, `4_external/sources/`, `7_datasets/`, `8_models/`, `9_artifacts/`, runtime/generated folders named in `.gitignore`, and `previusknowledge/` until governance decides otherwise. |
| What should not be committed? | External source snapshots, local product workspaces under current ignore posture, datasets, models, generated artifacts, Office spreadsheets/temp files, OS metadata, runtime outputs, caches, secrets, dependency directories, and the previous knowledge corpus wholesale without explicit governance. |
| What should W-05 address? | Agent Context Pack Strategy: task-scoped, authority-aware, freshness-aware, sensitivity-aware context packs that tell agents what to read, what not to read, what can be cited, what can be edited, and how evidence relates to authority. |

Final W-04 statement:

```text
AGENT PLATFORM can continue W-series architecture work with the current root layout,
but only if folders are treated as responsibility projections. Current root authority
lives in scoped canonical workspace architecture, not in folder names, product areas,
external sources, generated outputs, previous knowledge, or local files.
```
