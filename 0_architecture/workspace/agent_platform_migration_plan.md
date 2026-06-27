# AGENT PLATFORM Migration Plan

Status: Canonical W-08 workspace output  
Date: 2026-06-28  
Scope: Migration sequencing, safeguards, readiness, and validation rules for AGENT PLATFORM  
Authority: Migration planning guidance only. This document does not move, copy, delete, rename, archive, implement, stage, commit, or push anything.

## 1. Purpose

This document defines how AGENT PLATFORM should migrate architecture, previous knowledge, product candidates, external-source metadata, and future archive material without contaminating authority, losing provenance, or turning local evidence into current root truth.

W-08 exists because W-07 determined that the current numbered topology is usable temporarily, but no folder or document should move before a migration plan exists.

Inputs consumed:

| Input | W-08 use |
| --- | --- |
| `0_architecture/workspace/agent_platform_knowledge_assembly.md` | Baseline source audit and migration recommendation. |
| `0_architecture/workspace/agent_platform_workspace_charter.md` | Workspace identity, vocabulary, authority precedence, and Cognitive Semantic System naming rule. |
| `0_architecture/workspace/agent_platform_previous_knowledge_classification_index.md` | Semantic and file-level classification for `previusknowledge/`. |
| `0_architecture/workspace/agent_platform_external_source_registry.md` | External source roles, risks, license posture, and promotion requirements. |
| `0_architecture/workspace/agent_platform_workspace_responsibility_map.md` | Folder responsibilities, Git posture, access posture, and local-only boundaries. |
| `0_architecture/workspace/agent_platform_context_pack_strategy.md` | Source classes, context selection, citation, exclusion, and edit rules. |
| `0_architecture/workspace/agent_platform_cognitive_workspace_model.md` | Cognitive primitives, evidence-to-authority flow, substrate neutrality, and invariants. |
| `0_architecture/workspace/agent_platform_workspace_topology.md` | Provisional topology, local-only topology, and W-08 guidance. |
| `.gitignore` | Current Git/local-only policy for products, external sources, datasets, models, artifacts, runtime outputs, dependency folders, and Office files. |
| `README.md` | Minimal root descriptor. |
| `previusknowledge/` | Previous architecture and research migration corpus. |
| `4_external/sources/` | External source snapshots, all external evidence only. |
| `2_products/` | Product workspace candidates, local-only for now. |

W-08 rule:

```text
Migration is a governed transition from evidence to current workspace authority,
product scope, research scope, external metadata, archive state, or local-only
retention. Migration is not copying files into nicer folders.
```

## 2. Migration Principles

| Principle | Rule |
| --- | --- |
| Plan before movement | No file movement, copy, rename, deletion, archive creation, or implementation before explicit migration tickets. |
| Authority before location | A target path does not make content canonical. Status, scope, validation, governance, and promotion decide authority. |
| Restate before promote | Previous knowledge can govern current work only after it is restated in current AGENT PLATFORM vocabulary. |
| Evidence stays evidence | Prior docs, research, external sources, generated outputs, tool output, context packs, and agent summaries remain evidence until promoted. |
| Product scope stays bounded | Product material may become product workspace authority only inside declared product boundaries, not root authority by default. |
| External sources stay external | External repositories, engines, harnesses, examples, and tools do not become dependencies, instructions, or architecture by proximity. |
| Local-only stays local-only | Ignored areas remain out of Git by default until a later governance decision changes posture. |
| Validate each transition | Every migration step needs source class, target scope, authority posture, validation evidence, and rollback or retention posture. |
| Preserve provenance | Migrated or restated material must cite original sources and classification state. |
| Do not pre-decide substrate | The future Cognitive Semantic System remains neutral; graph and other substrates remain candidates only. |
| Human approval gates history | Staging, commits, pushes, publication, risky execution, external reuse, and authority promotion require explicit human or governance approval. |

Migration anti-principles:

| Anti-principle | Why prohibited |
| --- | --- |
| Bulk migration | It carries old scope, stale labels, product assumptions, and naming conflicts into current authority. |
| Folder-first promotion | It lets path override source status and governance. |
| External-source copy-in | It risks license, supply-chain, security, and authority contamination. |
| Product-root collapse | It lets product-specific behavior define the root platform. |
| Archive as trash | It hides unresolved decisions instead of preserving lifecycle and provenance. |
| Git as approval | A commit records a state; it does not prove authority, validation, or governance by itself. |

## 3. Migration Source Classes

| Source class | Current examples | Default status | Migration handling |
| --- | --- | --- | --- |
| Canonical workspace architecture | W-01 through W-08 under `0_architecture/workspace/` | Current human-readable workspace authority when marked canonical and scoped. | Preserve in place; future documents may reorganize references, not rewrite history casually. |
| Assembly and registry evidence | W-00, W-02, W-03 | Evidence and classification authority for their declared scope. | Cite as migration control inputs; do not collapse into a single undifferentiated doc. |
| Previous knowledge corpus | `previusknowledge/docs/`, `previusknowledge/research/` | Migration evidence with W-02 classification. | Mine by classification, restate useful concepts, preserve original paths as evidence. |
| Conflicted prior semantic-authority material | Prior semantic-authority and substrate documents classified as `conflicted` | Valuable evidence with naming, scope, or substrate conflict. | Normalize through current Cognitive Semantic System vocabulary before any promotion. |
| Product-scope previous material | Product architecture docs classified as `scope_limit` | Product/domain evidence only. | Defer until product workspace policy exists. |
| External source snapshots | `4_external/sources/*` | External reference evidence only. | Keep isolated and local-only; migrate metadata or review summaries only after ticketed review. |
| Product workspace candidates | `2_products/*` | Product candidates, local-only. | Keep local-only; define product workspace policy before tracking or moving. |
| Research areas | `1_research/`, selected prior research | Evidence only until promoted. | Migrate only curated, cited findings into architecture or docs after review. |
| Platform implementation candidates | `3_platform/` and future code areas | No implementation authority yet. | Do not migrate code in W-08; require implementation tickets later. |
| Generated/data/model/artifact areas | `7_datasets/`, `8_models/`, `9_artifacts/`, logs, runs, outputs | Local-only evidence or generated material. | Exclude from migration by default; promote selected evidence only after validation and governance. |
| Git/control files | `.gitignore`, `README.md` | Control or entry-point artifacts, not full authority. | Change only by explicit ticket. W-08 does not modify them. |

Source-class invariant:

```text
Every migration candidate must be classified before action. If a source lacks a
known class, stop and classify before migrating.
```

## 4. Migration Target Areas

Target areas are responsibility destinations, not permissions to create folders or move files in W-08.

| Target area | Future role | Migration eligibility | W-08 action |
| --- | --- | --- | --- |
| `0_architecture/workspace/` | Current workspace-level canonical architecture and migration control documents. | Restated current root principles, boundaries, policies, and migration decisions. | Keep W-series docs here; create only this W-08 plan. |
| `0_architecture/decisions/` or equivalent future decision area | Future accepted decisions and ADRs. | Decisions with explicit status, scope, rationale, alternatives, validation, and governance. | Proposed target only; do not create now. |
| `0_architecture/` domain areas | Future domain architecture such as agents, context, providers, adapters, runtime, governance, validation, and security. | Restated, current-scope architecture after source classification and review. | Proposed migration target family only. |
| `1_research/` | Reviewed investigations and evidence. | Research notes, comparisons, source reviews, and hypotheses with source status. | No movement now. |
| `2_products/` | Bounded product workspaces. | Product-specific source/docs only after product policy and Git posture decision. | Keep local-only; no product migration. |
| `3_platform/` | Future platform implementation. | Code and implementation artifacts only after architecture, implementation tickets, and validation. | No code migration. |
| `4_external/` metadata areas | Curated external metadata, licenses, standards, source reviews, and provenance. | Metadata and review summaries, not raw external source trees by default. | No movement now. |
| `5_workspace/` | Workspace operations, future context-pack projections, task scaffolds, and process artifacts. | Operational material that is not canonical architecture unless promoted. | No physical context-pack folder creation now. |
| `6_docs/` | Human-facing guides and documentation projections. | Docs generated from current authority with status labels and source citations. | No documentation projection now. |
| `7_datasets/`, `8_models/`, `9_artifacts/` | Local-only data, models, generated outputs, and retained evidence. | Only task-specific, local-only material unless later promoted. | Excluded from W-08 migration. |
| `10_scripts/`, `11_tools/`, `12_tests/` | Automation, tools, and validation support. | Reviewed executable or validation assets after policy. | No script/tool/test migration now. |
| `13_packages/`, `14_sdk/` | Future packaging and SDK surfaces. | Release or SDK material only after policy. | No package or SDK migration now. |
| `_archive/` or equivalent future archive area | Historical, superseded, retired, or preserved material. | Only after archive policy and lifecycle decision. | Reserved only; do not create in W-08. |

Target-area rule:

```text
The first migration target is usually a current-scope restatement, not a moved file.
```

## 5. Previous Knowledge Migration Plan

`previusknowledge/` remains the primary previous-knowledge migration corpus. W-02 classified 237 markdown files and must be used before any previous document influences current authority.

Classification handling:

| W-02 state | Migration posture | Allowed future output | Blocked action |
| --- | --- | --- | --- |
| `carry_forward` | Useful concept or principle. | Restated current workspace architecture, cited from original source. | Direct copy as current authority. |
| `scope_limit` | Product, domain, or bounded-scope material. | Product workspace input after product policy. | Root platform authority. |
| `migration_evidence` | Historical rationale or sequence evidence. | Migration notes, audit references, or rationale citations. | Current governing rule by itself. |
| `conflicted` | Useful but blocked by naming, scope, authority, roadmap, or substrate conflict. | Normalized proposal using Cognitive Semantic System vocabulary and substrate neutrality. | Promotion before normalization. |
| `external_reference` | Prior provider, harness, or tool analysis. | Revalidated research or adapter/provider evidence. | Current provider facts without revalidation. |
| `superseded` | Replaced material if later assigned. | Historical citation or archive candidate. | Current authority. |

Previous knowledge migration flow:

```text
Select candidate by W-02 state
-> inspect only needed source documents
-> extract claim and evidence
-> normalize vocabulary and scope
-> state current target authority or evidence status
-> validate against W-01 through W-08
-> create new current artifact only if ticket permits
-> preserve original as historical evidence
```

First safe previous-knowledge candidates for future migration are not files to move. They are concepts to restate:

| Candidate concept | Source class | Why safe first | Required target posture |
| --- | --- | --- | --- |
| Source-of-truth and promotion principles | `carry_forward` | Already reinforced by W-01 through W-06. | Current authority model or governance workflow, not raw copy. |
| Workspace/repository principles after vocabulary normalization | `carry_forward` | Useful for Git, authority, evidence, and approval posture. | Workspace-level principles using current vocabulary. |
| Cross-boundary responsibility rules | `carry_forward` | Supports migration validation and folder responsibility. | Responsibility or governance rules, not old folder names. |
| Agent role and permission boundaries | `carry_forward` | Needed before broad agent operation. | Agent model and access policy, not implementation. |
| Context selection, lifecycle, and sensitivity concepts | `carry_forward` | Directly supports context packs. | Context architecture and pack policy. |
| Adapter/provider/runtime/workflow posture syntheses | `carry_forward` | High-value conceptual boundaries. | Provider-neutral architecture; no code or provider adoption. |
| Prior semantic-authority principles | `conflicted` | High-value truth/evidence/lifecycle ideas. | Normalize to Cognitive Semantic System and keep substrate undecided. |

Previous knowledge prohibitions:

| Prohibition | Reason |
| --- | --- |
| Do not copy the corpus wholesale into `0_architecture/` or `6_docs/`. | It would import stale scope and old authority labels. |
| Do not preserve prior current/future names for semantic authority. | W-01 requires the neutral Cognitive Semantic System name until a naming ADR exists. |
| Do not treat product-oriented previous docs as root authority. | Product material is scope-limited. |
| Do not update old documents in place. | Original evidence should remain stable unless a specific migration ticket says otherwise. |
| Do not commit `previusknowledge/` wholesale. | It remains local migration evidence until governance decides otherwise. |

## 6. Canonical Architecture Migration

Current human-readable root authority lives under `0_architecture/workspace/`. The W-series documents should stay stable and traceable as the canonical architecture seed.

Canonical architecture migration goals:

| Goal | Handling |
| --- | --- |
| Keep current W-series authority discoverable. | Preserve W-00 through W-08 in place unless a later topology or documentation ticket explicitly supersedes them. |
| Reduce duplication later. | Future documents should synthesize and reference W-series docs rather than copying them repeatedly. |
| Separate architecture from docs. | `0_architecture/` remains authority-oriented; `6_docs/` should receive human-facing projections only after source authority is clear. |
| Separate decisions from evidence. | Future decision records should cite evidence and validation separately from accepted outcome. |
| Separate domain architecture from implementation. | Agent, context, adapter, provider, runtime, workflow, governance, validation, security, and semantic-authority docs should precede code. |

Potential future canonical architecture families:

| Family | Purpose | Depends on |
| --- | --- | --- |
| Workspace authority | Root identity, vocabulary, authority, governance, validation, security, and promotion boundaries. | W-01 through W-08. |
| Cognitive Semantic System architecture | Accepted semantic authority concept, lifecycle, provenance, context eligibility, and promotion mechanics. | Naming ADR, substrate evaluation, governance/validation model. |
| Context architecture | Context source classes, eligibility, pack generation, lifecycle, sensitivity, and projections. | W-05, W-06, W-08. |
| Agent architecture | Agent roles, permissions, handoff, execution boundaries, memory, coordination, and reporting. | W-01, W-05, W-06, previous carry-forward evidence. |
| Adapter/provider architecture | Provider-neutral mediation, capability mapping, external provider revalidation, and risk posture. | W-03, W-04, previous carry-forward and external-reference evidence. |
| Runtime/workflow architecture | Participation and coordination posture without hidden authority transfer. | W-06, previous carry-forward evidence, implementation policy. |
| Governance/validation/security architecture | Promotion, decisions, proof levels, evidence retention, access, secrets, shell/network/MCP/provider constraints. | W-01 through W-08. |

Canonical architecture rule:

```text
Future architecture documents should carry forward concepts, not old documents.
They must cite source evidence, declare status and scope, and avoid implementation
commitments unless the ticket explicitly authorizes them.
```

## 7. Product Workspace Migration

`2_products/` contains product workspace candidates and is ignored by `.gitignore`. W-08 does not inspect deeply, migrate, track, copy, or modify product material.

Current product posture:

| Area | Current posture | Migration rule |
| --- | --- | --- |
| `2_products/backend-energyplus/` | Product/domain candidate, local-only. | Defer until product policy. |
| `2_products/cli/` | Product/interface candidate, local-only. | Defer until product policy. |
| `2_products/desktop/` | Product/interface candidate, local-only. | Defer until product policy. |
| `2_products/experimental/` | Experimental product candidate, local-only. | High caution; no root authority. |
| `2_products/omniverse-app/` | Product candidate, local-only. | Product-scoped only; no root authority. |
| `2_products/web-platform/` | Product/interface candidate, local-only. | Defer until product policy. |

Product migration must define before movement:

| Required decision | Why required |
| --- | --- |
| Active product list | Avoids migrating experiments as active products. |
| Product authority boundary | Prevents product docs or source from defining root workspace architecture. |
| Git posture | `2_products/` is currently ignored; tracking requires explicit decision. |
| Product source policy | Determines what code, docs, generated outputs, and local dependencies can be tracked. |
| Product external-source policy | Controls domain engines, SDKs, examples, and license/security review. |
| Product validation policy | Separates product behavior evidence from root platform validation. |
| Product archive/retirement rule | Handles inactive candidates without deletion or ambiguity. |

Product migration rule:

```text
No product workspace should be migrated, committed, renamed, split, deleted, or used
as root authority until a product workspace policy exists.
```

## 8. External Source Migration

`4_external/sources/` contains 12 external source directories classified by W-03. All remain external references and not promoted.

External migration posture:

| External material | Current status | Future migration path |
| --- | --- | --- |
| Raw source snapshots | Local-only external evidence. | Keep isolated; do not copy into platform or products by default. |
| External project docs | External claims and source-local meaning. | Cite through W-03 or source-review tickets; do not treat as internal policy. |
| External instructions | Repository-local evidence only. | Never active AGENT PLATFORM instructions by proximity. |
| Licenses and notices | Legal/reuse evidence, not approval. | Curate metadata only after review. |
| Generated external projections | Evidence or projections only. | Promote only after validation/governance if useful. |
| Harness/provider facts | Historical or source-specific evidence. | Revalidate against current sources before adapter/provider decisions. |
| Domain engines and SDKs | Product/domain references. | Defer until bounded product policy and legal/security review. |

External metadata migration can happen later without source-code migration. Candidate metadata includes source name, origin URL, version or commit, license, role, relevance, risk, promotion status, reviewed evidence paths, and review date.

External migration prohibitions:

| Prohibition | Reason |
| --- | --- |
| Do not run external code. | Runtime, credential, native binary, network, and supply-chain risks are unresolved. |
| Do not install external dependencies. | Dependency trust and license posture are unresolved. |
| Do not authenticate external services. | Credential and privacy controls are unresolved. |
| Do not copy external source into `3_platform/` or `2_products/`. | Reuse requires provenance, license, security, validation, and governance. |
| Do not treat external source names as AGENT PLATFORM naming authority. | Workspace vocabulary comes from current canonical architecture. |
| Do not treat graph-oriented external material as substrate decision. | The Cognitive Semantic System substrate remains undecided. |

External source rule:

```text
Migrate metadata and reviewed claims before considering any source reuse. Do not
migrate external code as a shortcut for architecture or implementation.
```

## 9. Archive Strategy

`_archive/` is reserved as a future explicit migration target only. W-08 does not create it.

Archive purpose:

| Archive state | Meaning |
| --- | --- |
| `historical` | Preserved past material that remains useful for trace. |
| `superseded` | Replaced by newer current authority. |
| `deprecated` | Known but discouraged for new work. |
| `retired` | No longer active but retained for audit. |
| `rejected` | Considered and explicitly not accepted. |
| `external_snapshot_reference` | External source snapshot retained as evidence, not internal truth. |

Archive policy requirements before creation:

| Requirement | Reason |
| --- | --- |
| Archive target naming | Avoids premature `_archive/` creation or inconsistent archive folders. |
| Lifecycle states | Distinguishes historical, superseded, deprecated, retired, rejected, and retained evidence. |
| Provenance metadata | Preserves source path, prior status, classification, reason, date, and approving decision. |
| Link update policy | Prevents broken citations and hidden authority drift. |
| Git posture | Defines whether archive content is tracked, local-only, or metadata-only. |
| Restoration rule | Allows material to be reconsidered without rewriting history. |
| Deletion rule | Requires explicit governance for any deletion. |

Archive rule:

```text
Archive is a lifecycle state with evidence and governance. It is not a dumping
ground and not a deletion substitute.
```

## 10. Commit Strategy

W-08 does not stage, commit, amend, push, or create a pull request.

Future commit hygiene principles:

| Principle | Rule |
| --- | --- |
| Commit only reviewed intentional changes | Stage only files explicitly included in the current human-approved commit scope. |
| Keep local-only areas out | Do not stage `2_products/`, `4_external/sources/`, datasets, models, artifacts, Office files, logs, dependency folders, secrets, or caches. |
| Do not commit previous knowledge wholesale | `previusknowledge/` remains migration evidence until governance decides otherwise. |
| Inspect before commit | Review `git status`, `git diff`, and recent history before staging. |
| Preserve unrelated user changes | Do not revert or stage unrelated work. |
| Separate architecture from migration batches | Commit W-series docs separately from any later migration output. |
| Human approval required | Agent-prepared commits require explicit human instruction. |

Recommended future commit units:

| Unit | Contents | Conditions |
| --- | --- | --- |
| Workspace canonical docs | W-series docs under `0_architecture/workspace/`. | Human approval after validation. |
| Documentation projections | Human-facing docs under `6_docs/`. | Only after source authority and projection status are clear. |
| Previous knowledge restatements | New current architecture docs derived from prior evidence. | Source classification, citations, validation, governance. |
| External metadata | Curated source registry or review metadata. | License/security/provenance fields included; no raw source snapshots. |
| Product policy | Product workspace policy docs. | Product scope and Git posture decided. |
| Implementation/test changes | Code, scripts, tools, tests, packages, SDKs. | Implementation ticket and validation policy exist. |

Commit rule:

```text
A clean commit records reviewed workspace state. It does not replace validation,
governance, promotion, or human approval.
```

## 11. Migration Validation Rules

Every future migration batch must satisfy these rules before and after action.

Pre-migration checks:

| Check | Required evidence |
| --- | --- |
| Ticket scope | Active instruction names the migration batch and allowed files. |
| Source classification | W-02, W-03, W-04, W-05, W-06, or current policy classifies the source. |
| Target responsibility | W-04/W-07 target area matches the source class and intended authority. |
| Authority posture | Output status declares canonical, research, evidence, product-scoped, external metadata, generated, or archived. |
| Citation plan | Original source paths and classification states will be cited. |
| Local-only check | Ignored/private/heavy/generated areas are excluded unless explicitly scoped. |
| External risk check | License, security, execution, dependency, network, credential, and instruction risks are reviewed for external material. |
| Product boundary check | Product material stays inside product scope. |
| Naming/substrate check | Cognitive Semantic System vocabulary is used and no final substrate is assumed. |
| Stop rule | The batch says where the agent must stop. |

Post-migration checks:

| Check | Required evidence |
| --- | --- |
| File list | Exact files created, edited, moved, archived, or intentionally untouched. |
| Diff review | Summary of content changes and absence of unintended local-only material. |
| Source citations | Migrated/restated claims cite source paths and classification. |
| Status labels | New artifacts declare status, scope, authority, and limitations. |
| Link integrity | Referenced paths are valid or explicitly historical. |
| No hidden execution | No external code, scripts, tools, package installs, or service auth unless approved. |
| Git posture | `git status --short` shows only intended changes. |
| Validation output | Commands or checks run and their results. |
| Residual risks | Remaining blockers and uncertainty are reported. |

Minimum W-series validation for W-08 itself:

| Command | Purpose |
| --- | --- |
| `git status --short` | Verify worktree visibility and confirm no staging/commit action. |
| `Test-Path .gitignore` | Confirm Git/local-only policy file exists. |
| `Test-Path README.md` | Confirm root descriptor exists. |
| `Test-Path 0_architecture/workspace/agent_platform_knowledge_assembly.md` | Confirm W-00 input exists. |
| `Test-Path 0_architecture/workspace/agent_platform_workspace_charter.md` | Confirm W-01 input exists. |
| `Test-Path 0_architecture/workspace/agent_platform_previous_knowledge_classification_index.md` | Confirm W-02 input exists. |
| `Test-Path 0_architecture/workspace/agent_platform_external_source_registry.md` | Confirm W-03 input exists. |
| `Test-Path 0_architecture/workspace/agent_platform_workspace_responsibility_map.md` | Confirm W-04 input exists. |
| `Test-Path 0_architecture/workspace/agent_platform_context_pack_strategy.md` | Confirm W-05 input exists. |
| `Test-Path 0_architecture/workspace/agent_platform_cognitive_workspace_model.md` | Confirm W-06 input exists. |
| `Test-Path 0_architecture/workspace/agent_platform_workspace_topology.md` | Confirm W-07 input exists. |
| `Test-Path previusknowledge` | Confirm previous knowledge corpus exists. |
| `Test-Path 4_external/sources` | Confirm external source snapshot root exists. |
| `Test-Path 2_products` | Confirm product candidate root exists. |
| `Test-Path 0_architecture/workspace/agent_platform_migration_plan.md` | Confirm W-08 output exists. |
| `Get-Item 0_architecture/workspace/agent_platform_migration_plan.md` | Confirm W-08 output metadata. |

Validation rule:

```text
Validation evaluates whether migration followed declared scope. It does not by
itself approve authority promotion, commit, publication, or next-ticket execution.
```

## 12. Migration Risk Register

| Risk ID | Risk | Impact | Control |
| --- | --- | --- | --- |
| MIG-01 | Previous canonical labels treated as current authority. | Old scope contaminates root architecture. | Use W-02 classification and restate before promotion. |
| MIG-02 | Bulk copy of previous corpus. | Duplicated stale docs and authority confusion. | Prohibit wholesale copy; migrate concepts by ticket. |
| MIG-03 | Product material defines root platform. | Product/root collapse. | Scope-limit product material and require product policy. |
| MIG-04 | External source treated as dependency or instruction. | Security, license, and authority contamination. | Use W-03 registry and external promotion rules. |
| MIG-05 | Local-only material accidentally committed. | Privacy, size, license, or generated-output leakage. | Respect `.gitignore`, inspect status, stage only approved files. |
| MIG-06 | Archive hides unresolved conflicts. | Loss of provenance and premature disposal. | Define archive lifecycle policy before moving anything. |
| MIG-07 | Graph or another substrate assumed too early. | Premature implementation architecture. | Keep Cognitive Semantic System substrate undecided until evaluation. |
| MIG-08 | Current W-series docs become duplicated inconsistently. | Divergent authority and stale copies. | Synthesize and cite; do not copy repeatedly. |
| MIG-09 | Agent reads too broadly during migration. | Context bloat and sensitive evidence exposure. | Use W-05 context selection and smallest sufficient source set. |
| MIG-10 | Validation confused with governance. | Passing checks become false approval. | Keep validation evidence separate from authority promotion. |
| MIG-11 | Implementation starts before migration readiness. | Code locks in unresolved architecture. | Block implementation until explicit implementation tickets. |
| MIG-12 | README or docs become competing authority. | Human-facing docs override architecture accidentally. | Status-label docs and point to canonical sources. |
| MIG-13 | Provider/harness historical facts become current facts. | Adapter/provider design based on stale behavior. | Revalidate external facts before use. |
| MIG-14 | User or agent modifies unrelated local work. | Loss of parallel user changes. | Inspect diffs, modify only scoped files, never revert unrelated changes. |
| MIG-15 | Migration continues into next ticket automatically. | Scope creep and unapproved changes. | Stop at ticket boundary and wait for explicit instruction. |

Risk rule:

```text
If a migration risk cannot be controlled within the active ticket, stop and report
the blocker instead of widening scope.
```

## 13. Migration Sequence

The following sequence defines future migration work. W-08 does not execute any step.

| Step | Name | Purpose | Allowed future actions | Explicitly not allowed in W-08 |
| --- | --- | --- | --- | --- |
| M-01 | M-01 — Workspace Canonical Docs Commit Hygiene | Prepare a clean human-approved commit posture for W-series architecture docs. | Inspect status/diff/history, identify intended W-series files, exclude local-only areas, request human commit approval. | Stage, commit, amend, push, or modify `.gitignore`. |
| M-02 | M-02 — Previous Knowledge Carry-Forward Extraction | Extract durable principles and models from `carry_forward` documents. | Read selected W-02 sources, write restated current-scope architecture by explicit ticket, cite source paths. | Move/copy old files wholesale or edit old corpus. |
| M-03 | M-03 — Conflicted Semantic Authority Material Normalization | Normalize conflicted prior semantic-authority material under Cognitive Semantic System vocabulary. | Produce neutral naming, authority, lifecycle, and substrate-evaluation docs. | Use old names as current/future authority or decide final substrate. |
| M-04 | M-04 — Agent/Context/Runtime/Provider/Adapter Synthesis Migration | Restate high-value architecture syntheses into current domain architecture. | Create scoped domain architecture docs after W-09 structure if approved. | Implement code, adopt providers, or treat runtime as truth owner. |
| M-05 | M-05 — Research Evidence Migration | Move reviewed research claims into evidence or architecture surfaces. | Curate findings with uncertainty, citations, and status. | Promote research without validation/governance. |
| M-06 | M-06 — External Metadata Migration | Curate external source metadata and review summaries without source-code migration. | Create/update metadata records, license notes, risk notes, and provenance summaries by ticket. | Copy external source code, run external code, install dependencies, or authenticate services. |
| M-07 | M-07 — Product Workspace Migration Policy | Define how product candidates become active, tracked, archived, or retained local-only. | Create product policy, product status labels, Git posture, validation, and boundary rules. | Move or commit product files before policy. |
| M-08 | M-08 — Archive Policy | Define archive lifecycle, path, metadata, and restoration/deletion rules. | Create archive policy and, if approved later, archive target. | Create `_archive/` or move material in W-08. |
| M-09 | M-09 — First Controlled Migration Batch | Execute the first small approved migration batch after policies are ready. | Migrate one narrow concept set with citations, validation, and status labels. | Bulk migration, product code migration, external source migration, or next-ticket sprawl. |
| M-A | M-A — Migration Audit | Audit migrated material for provenance, authority, links, Git posture, and residual risks. | Compare source classifications, target status, citations, validation results, and worktree state. | Treat audit as approval without governance. |

Recommended order:

1. M-01 - establish clean W-series commit hygiene after explicit human request.
2. W-09 - define canonical documentation structure after explicit instruction.
3. M-02 - extract a small carry-forward principle set into current vocabulary.
4. M-03 - normalize conflicted semantic-authority material without substrate decision.
5. M-04 - migrate agent/context/adapter/provider/runtime/workflow syntheses by domain.
6. M-05 - curate research evidence where it supports active architecture questions.
7. M-06 - migrate external metadata only, not source code.
8. M-07 - define product workspace migration policy before product action.
9. M-08 - define archive policy before creating archive paths.
10. M-09 - execute one controlled migration batch.
11. M-A - audit the batch and update readiness.

First controlled migration batch criteria:

| Criterion | Requirement |
| --- | --- |
| Small scope | One concept family or one documentation family only. |
| Clear source class | W-02 or W-03 classification exists. |
| Current vocabulary | Uses AGENT PLATFORM, workspace, Cognitive Semantic System, and current authority terms. |
| No movement required | Prefer new restated current document over moving previous files. |
| No external code | External code and dependencies remain untouched. |
| No product code | Product candidates remain local-only unless product policy exists. |
| Validated output | File status, citations, links, and Git posture are checked. |
| Human stop point | Agent stops after the approved batch and audit summary. |

Migration sequence rule:

```text
The first real migration should be boring: small, cited, validated, reversible in
understanding, and unable to change product code or external dependencies.
```

## 14. Readiness For W-09

Expected next ticket after W-08: `W-09 - Canonical Documentation Structure`.

W-09 can begin only after explicit instruction. W-08 does not start it.

Readiness assessment:

| Area | Verdict | Reason |
| --- | --- | --- |
| Workspace authority | Ready enough. | W-01 through W-08 define identity, source classes, context, cognition, topology, and migration controls. |
| Documentation structure | Ready for planning. | W-08 defines migration sequence and target-area constraints. |
| Previous knowledge migration | Ready for controlled extraction planning, not movement. | W-02 classification and W-08 migration rules exist. |
| External source migration | Ready for metadata planning only. | W-03 registry and W-08 external migration rules exist. |
| Product migration | Not ready for movement. | Product workspace policy and Git posture remain unresolved. |
| Archive migration | Not ready for movement. | Archive policy is not created and `_archive/` remains future-only. |
| Implementation | Not ready. | Implementation tickets, validation registry, security/access policy, and product policy are absent. |
| Cognitive Semantic System implementation | Not ready. | Naming remains provisional and substrate remains undecided. |
| Governance automation | Not ready. | Governance workflow is conceptual, not procedural or automated. |
| Validation automation | Not ready. | Validation rules exist, but no full validation registry or proof-level model exists. |

W-09 should define:

| W-09 topic | Required boundary |
| --- | --- |
| Canonical documentation structure | Organize future docs without moving old corpus by default. |
| Status labels | Distinguish canonical, draft, research, evidence, projection, historical, superseded, archived, and product-scoped docs. |
| Architecture-to-doc projection | Define how `6_docs/` can receive human-facing docs without becoming competing authority. |
| Decision record structure | Define how ADRs or decisions cite evidence, validation, and governance. |
| Migration-ready targets | Identify where future restated documents should go. |
| Stop rule | Do not migrate files unless W-09 explicitly authorizes a scoped action. |

Readiness verdict:

```text
W-08 makes AGENT PLATFORM ready for W-09 documentation-structure planning after
explicit instruction. It does not make the workspace ready for bulk migration,
product migration, external source reuse, archive movement, implementation, or
semantic-authority implementation.
```

## 15. Final Verdict

| Question | Verdict |
| --- | --- |
| Did W-08 migrate files? | No. It only defines future migration sequence and controls. |
| What is the core migration model? | Classify source, restate concepts in current vocabulary, validate, govern, then promote or retain evidence. |
| What is the safest first future migration? | A narrow carry-forward extraction of authority/evidence/promotion principles into current architecture, not a file move. |
| What remains local-only? | `2_products/`, `4_external/sources/`, `7_datasets/`, `8_models/`, `9_artifacts/`, generated outputs, runtime logs, Office files, secrets, credentials, dependency folders, and `previusknowledge/` until governance decides otherwise. |
| What is blocked? | Bulk migration, product movement, external code reuse, archive creation, implementation, final substrate choice, and commits without explicit approval. |
| Is W-09 ready to start? | Yes, for documentation-structure planning only, after explicit user instruction. |

Final W-08 statement:

```text
AGENT PLATFORM can proceed from topology to documentation-structure planning, but
migration must remain classified, cited, incremental, validation-backed, and
governance-bound. The current W-series docs are the human-readable authority seed;
previous knowledge, product candidates, external sources, generated outputs, and
local-only areas remain evidence or scoped material until explicitly promoted.
```
