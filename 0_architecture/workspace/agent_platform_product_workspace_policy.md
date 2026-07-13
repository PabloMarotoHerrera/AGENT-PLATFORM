# AGENT PLATFORM Product Workspace Policy

Status: Canonical W-12 workspace output  
Date: 2026-06-28  
Scope: Product workspace identification, activation, governance, validation, documentation, migration, Git posture, and retirement policy for AGENT PLATFORM  
Authority: Product workspace policy only. This document does not move product files, rename product folders, delete product folders, migrate product docs, edit product code, modify `.gitignore`, run product code, install dependencies, stage, commit, push, create W-13, or implement product architecture.

## Current P12.C3 Tracking Exception

P12.C3 supersedes the whole-class local-only wording in this historical W-12
baseline for one absent future root only: `2_products/hermes-agent`. Product
children remain ignored by default, all existing siblings remain ignored, and
the exception creates no source and grants no product activation. Hermes must be
a normal AGENT PLATFORM main-repository subtree with no nested Git, independent
history or remote. Every future product exception requires separate governance.

## 1. Purpose

This document defines how product workspaces are identified, activated, governed, validated, documented, migrated, tracked in Git, and retired inside AGENT PLATFORM.

Product policy comes after W-11 because W-11 defines the root governance and promotion model. Product activation, ownership, Git posture, product documentation status, product validation, external dependency adoption, and product retirement are governance-sensitive decisions.

Clarifications:

| Clarification | Rule |
| --- | --- |
| Products are contained workspaces. | Product scope can own product behavior and product meaning without defining root workspace authority. |
| Product folders do not define root authority. | A folder under `2_products/` is a candidate by location, not active authority. |
| Product source does not define AGENT PLATFORM architecture. | Source may implement product behavior inside product scope; architecture remains governed separately. |
| Product docs are product-scoped unless promoted. | Product docs do not override `0_architecture/workspace/` or root W-series authority. |
| Product generated outputs are not source by default. | Reports, builds, simulation outputs, logs, screenshots, exports, and generated docs need review before use. |
| Product activation is governed. | Activation requires owner, purpose, scope, Git posture, validation baseline, external dependency posture, security posture, and root-boundary statement. |

W-12 rule:

```text
Product workspaces are allowed to own product-specific behavior and evidence only
inside declared product scope. They do not become active, tracked, canonical, or
root-authoritative because folders exist.
```

## 2. Product Workspace Definition

A product workspace is a bounded workspace area for a user-facing, domain-facing, interface-facing, or implementation-facing product that consumes AGENT PLATFORM capabilities while preserving product-specific scope.

A product workspace may contain:

| Surface | Product workspace meaning |
| --- | --- |
| Product source | Implemented product behavior within declared product scope. |
| Product architecture | Product-scoped architecture after explicit product governance. |
| Product docs | Product-scoped docs, guides, references, and implementation notes. |
| Product validation | Evidence for product behavior, product readiness, product constraints, and product quality. |
| Product workflows | Product-specific workflows and operations after policy. |
| Product implementation plans | Product-scoped planning that depends on root architecture constraints. |
| Product generated outputs | Evidence or artifacts until reviewed and promoted inside product scope. |
| Product external references | External dependencies or domain sources after provenance, license, security, validation, and governance review. |

A product workspace is not:

| Not | Reason |
| --- | --- |
| Root authority | AGENT PLATFORM root authority lives in current workspace architecture and future governed semantic authority. |
| Platform architecture | Product design cannot define generic agent, context, adapter, provider, runtime, governance, validation, or security architecture by default. |
| The Cognitive Semantic System | Product scope cannot own accepted semantic truth for the workspace root. |
| A provider | Product code or UI is not automatically a provider or adapter target. |
| An external dependency | Product folders are internal candidates; external dependencies need separate review. |
| Automatically tracked in Git | Product children are ignored/local-only by default. P12.C3 grants only future `2_products/hermes-agent` a governed normal-tracking exception. |
| Automatically active | Folder existence is not activation. |
| A final architecture decision | Product material can inform proposals but does not decide root architecture. |

## 3. Current Product Candidate Inventory

W-12 inspected only the top-level `2_products/` inventory. No product source was inspected deeply and no product code was run.

| Product candidate | Observed role | Likely product type | Current activation state | Git posture | Risk posture | Recommended next handling |
| --- | --- | --- | --- | --- | --- | --- |
| `backend-energyplus/` | Product candidate named as a backend related to EnergyPlus. | Domain/backend integration candidate. | `candidate`, `deferred`, `local_only`. | Ignored/local-only under `.gitignore`. | High until EnergyPlus provenance, license/name-use, native execution, domain data, and validation posture are reviewed. | Keep local-only; future product charter and external dependency review before any code or docs migration. |
| `cli/` | Product candidate named as command-line interface. | Interface-facing product candidate. | `candidate`, `deferred`, `local_only`. | Ignored/local-only under `.gitignore`. | Medium until command behavior, dependency, execution, and user-facing scope are reviewed. | Keep local-only; future interface product review and docs-first charter. |
| `desktop/` | Product candidate named as desktop application. | Interface-facing product candidate. | `candidate`, `deferred`, `local_only`. | Ignored/local-only under `.gitignore`. | Medium-high until desktop runtime, packaging, credentials, local data, and update posture are reviewed. | Keep local-only; future product charter and security/packaging review. |
| `experimental/` | Product area explicitly named experimental. | Experimental sandbox or prototype area. | `experimental`, `blocked`, `local_only`. | Ignored/local-only under `.gitignore`. | High because experimental material can become active by proximity, contain unreviewed code, or blur product/root boundaries. | Keep local-only; do not activate without explicit product split, owner, and review. |
| `omniverse-app/` | Product candidate named as Omniverse application. | Visualization or domain application candidate. | `candidate`, `deferred`, `local_only`. | Ignored/local-only under `.gitignore`. | High until Omniverse/Kit material, SDK/license posture, runtime, packaging, GPU/local data, and product claims are reviewed. | Keep local-only; future product charter and external dependency/security review before activation. |
| `web-platform/` | Product candidate named as web platform. | Web/interface product candidate. | `candidate`, `deferred`, `local_only`. | Ignored/local-only under `.gitignore`. | Medium-high until frontend/backend boundaries, dependencies, auth, data, build, and deployment posture are reviewed. | Keep local-only; future product charter and implementation readiness review. |

Inventory verdict:

```text
W-12 identifies six product candidates. None are active products in W-12. All remain
local-only and ignored until product governance changes their state and Git posture.
```

## 4. Product Workspace States

Product states describe product maturity and governance posture. A product can carry multiple labels, such as `candidate` and `local_only`.

| State | Meaning | Authority posture | Required governance | Allowed agent behavior |
| --- | --- | --- | --- | --- |
| `candidate` | Product folder or concept exists but is not active. | No product authority beyond candidate evidence. | Product purpose, scope, owner, and state decision before activation. | Inventory, summarize, propose charter by explicit product task. |
| `active` | Product is approved for governed product work. | Product-scoped authority can exist after product docs/decisions are promoted. | Product Owner, scope, Git posture, validation baseline, security/access posture, and root-boundary statement. | Work only by product tickets; edits and validation scoped. |
| `experimental` | Prototype or sandbox product material. | Evidence/prototype only. | Explicit owner, isolation, no production claims, high-risk review before activation. | Read or edit only by experimental product ticket; do not promote by proximity. |
| `deferred` | Product candidate is intentionally postponed. | Evidence only. | Deferral reason, reconsideration trigger, owner if known. | Preserve inventory; do not edit or activate. |
| `archived` | Product material retained in archive for audit/reference. | Archive evidence only. | Archive policy, archive authorization, provenance, restoration rule. | Read only by archive/product task. |
| `retired` | Product is no longer active but may remain traceable. | Historical/product evidence. | Retirement reason, owner, replacement if any, retention posture. | No new implementation; cite as historical/product evidence. |
| `local_only` | Product material remains untracked/ignored. | Local evidence or candidate material. | Any change to Git posture requires governance. | Do not stage/commit; read/write only by product task. |
| `product_scoped_canonical` | Product doc or decision is canonical inside product scope. | Product authority only. | Product Owner approval, product scope, validation posture, root constraints. | Cite inside product scope; do not use as root authority. |
| `implementation_ready` | Product has enough policy, architecture, validation, and security posture to begin scoped implementation. | Product implementation readiness only. | Product charter, dependencies, validation baseline, security/access, Git posture, owner, implementation plan. | Implementation work only by explicit ticket. |
| `blocked` | Product cannot proceed due to unresolved risk or missing precondition. | No activation or promotion. | Blocker record and required resolution. | Report blocker; do not continue into product work. |

State rule:

```text
Folder existence creates at most candidate state. Active, canonical, implementation-ready,
tracked, archived, or retired states require governance.
```

## 5. Product Ownership Model

Product ownership defines who can propose, validate, approve inside product scope, and what remains prohibited.

| Role | Can propose | Can validate | Can approve inside product scope | Cannot do |
| --- | --- | --- | --- | --- |
| Product Owner | Product purpose, scope, activation, Git posture, roadmap, retirement. | May review product validation. | Yes, after root governance permits product activation and within product scope. | Override root authority, bypass security, publish secrets, or decide global architecture. |
| Product Architecture Owner | Product architecture, product boundaries, product docs, implementation readiness. | May validate architecture consistency. | Product architecture only after product governance. | Define generic platform architecture or Cognitive Semantic System authority. |
| Product Validation Owner | Product tests, acceptance evidence, quality gates, baseline validation. | Yes, for product scope. | Validation sufficiency only if delegated; not governance promotion by default. | Approve product activation alone or root authority. |
| Product Security Owner | Product secrets, credentials, data sensitivity, runtime/network/provider exposure. | Yes, for product security posture. | Security/access posture if delegated. | Casually override root security/access constraints. |
| Product External Dependency Owner | Product-specific external libraries, SDKs, engines, APIs, models, datasets. | May validate dependency evidence and risk. | Product dependency recommendation only; adoption needs governance. | Promote external dependency to root platform dependency. |
| Product Documentation Owner | Product docs, user guides, developer docs, product projections. | May validate docs against product/root constraints. | Product docs inside scope if delegated. | Override root architecture or publish unsupported product claims. |
| Product Migration Owner | Product doc/source migration planning and audit. | May validate migration readiness. | Product migration plan if governance delegates. | Move, copy, delete, archive, or commit product files without explicit ticket. |
| Product Agent Contributor | Drafts, reviews, summaries, plans, validation when scoped. | Yes, only when scoped. | No. | Approve, activate, promote, commit, run product code, install dependencies, or widen scope. |

Ownership rule:

```text
Product ownership is scoped ownership. No product role can approve root authority,
global governance, global validation, or global security changes by product authority alone.
```

## 6. Product Authority Boundary

Product workspaces may own the following only inside declared product scope:

| Product may own | Boundary |
| --- | --- |
| Product behavior | Implemented and validated behavior for that product. |
| Product source | Source authority for product behavior after Git/source posture is governed. |
| Product-specific architecture | Canonical only for product scope after promotion. |
| Product-specific docs | Product-scoped docs and projections. |
| Product validation evidence | Evidence for product behavior, not root truth. |
| Product workflows | Product-specific operations and workflows after review. |
| Product implementation plans | Product-scoped implementation plans constrained by root architecture. |
| Product generated outputs after review | Product evidence or artifacts after validation/governance. |
| Product external dependency decisions inside scope | Product-specific adoption decisions after provenance, license, security, validation, and governance. |

Product workspaces must never own:

| Must never own | Reason |
| --- | --- |
| AGENT PLATFORM root authority | Root authority belongs to workspace architecture and governance. |
| Workspace vocabulary | Shared vocabulary must remain root-governed. |
| Cognitive Semantic System authority | Accepted semantic truth remains future governed workspace authority. |
| Global governance | Product governance is scoped. |
| Global validation | Product validation evaluates product behavior only. |
| Global security | Product security cannot override root security/access constraints. |
| Generic provider/adapter/runtime architecture | Product needs can inform but not decide generic platform architecture. |
| External source authority | External dependencies remain externally owned and reviewed. |
| Git history without human approval | Product commits, staging, pushes, and publication require explicit approval. |
| Final cognitive substrate | Product scope cannot decide whether graph or any other substrate is final. |

Authority boundary rule:

```text
Product authority is strong only inside product scope and weak outside it. Root
architecture constrains product work; product work does not silently constrain root.
```

## 7. Product Git Posture

Current rule:

```text
`2_products/` remains ignored/local-only by default. The sole current governed exception is the absent future `2_products/hermes-agent` path selected by P12.C2 and enabled by P12.C3.
```

Current implications:

| Implication | Rule |
| --- | --- |
| No product commit in W-12. | W-12 creates only this policy document. |
| No product code staging in P12.C3. | Existing product files remain local-only; the absent Hermes exception creates and stages nothing. |
| No `git add .`. | Exact approved paths are required for any future staging. |
| Product Git posture requires governance. | Tracking product docs/source needs explicit product decision. |

Future Git posture options:

| Option | Description | Strengths | Risks | W-12 recommendation |
| --- | --- | --- | --- | --- |
| A | Keep product local-only. | Lowest risk now; preserves privacy and avoids premature product authority. | Product work remains unversioned in current repo. | Default for now. |
| B | Track selected product docs only. | Allows product charters/policies without code exposure. | Docs may drift from untracked source. | Good first future option after product charter. |
| C | Track selected product source inside this repo. | Simple monorepo-style product development. | Commits may include heavy/private/dependency material; root/product boundaries can blur. | Defer until product activation and validation. |
| D | Split product into separate repository. | Strong product boundary and independent lifecycle. | Requires repo strategy, links, access, CI, governance. | Strong option for mature products later. |
| E | Use submodule/subtree/reference-only. | Preserves separation while linking source. | Operational complexity and Git confusion. | Consider only after repository strategy. |
| F | Archive/defer product. | Reduces active surface and risk. | Requires archive/retirement policy. | Use for inactive or abandoned products later. |

Default posture:

```text
Keep product candidates local-only by default until each product has a charter,
owner, scope, validation baseline, external dependency posture, security posture,
and exact Git decision. P12.C3 records only the Hermes path-level exception and
does not activate or import it.
```

## 8. Product Documentation Policy

Product documentation uses W-09 documentation status and scope rules.

| Rule | Meaning |
| --- | --- |
| Product docs are `product_scoped` by default. | Product docs govern only declared product scope. |
| Product docs do not override root architecture. | Root W-series docs and future root decisions constrain product docs. |
| Product docs may become canonical only inside product scope. | Product Owner and governance approval are required. |
| Product user docs may later project into `6_docs/`. | Human-facing product docs must cite product and root source authority. |
| Product architecture must cite root workspace constraints. | Product architecture should reference root boundaries for agents, context, governance, validation, security, and external sources. |
| Product generated docs require provenance. | Generated product docs must cite generator/tool, inputs, date if available, and review status. |
| Product docs may migrate before code only if scoped. | Docs-only migration can happen before source tracking, but only by product documentation ticket. |

Product documentation rule:

```text
Product documentation can explain product behavior. It cannot rewrite root
architecture by being clearer, newer, or closer to implementation.
```

## 9. Product Validation Policy

Product validation evaluates product behavior, product readiness, and product-specific risk.

| Validation rule | Meaning |
| --- | --- |
| Product validation evaluates product behavior. | It checks product-specific claims, behavior, integration, dependencies, and readiness. |
| Product validation does not approve root authority. | Passing product tests does not promote root architecture or platform policy. |
| Product validation evidence must be retained. | Commands, results, scope, environment, limitations, and artifacts should be traceable when used for decisions. |
| Product validation can block activation. | Failed or missing validation can keep product state `blocked`, `candidate`, or `deferred`. |
| Product validation can support implementation readiness. | Passing scoped validation can support `implementation_ready` after governance. |
| Product validation must identify scope and limitations. | Validation should state what was tested, not tested, environment assumptions, and residual risk. |
| Product validation commands require scope. | W-12 does not run tests, builds, packages, Node, Python, EnergyPlus, OpenStudio, Omniverse, or product commands. |

Validation posture examples:

| Posture | Meaning |
| --- | --- |
| `not_validated` | No scoped validation has run. |
| `inventory_only` | Only top-level inventory was inspected. |
| `docs_reviewed` | Product docs were reviewed but code not executed. |
| `tests_defined` | Validation plan exists but has not run. |
| `validated_for_scope` | Specific checks passed for declared scope. |
| `failed` | Scoped validation failed. |
| `blocked` | Validation cannot proceed due to missing owner, environment, dependency, or policy. |

## 10. Product External Dependency Policy

Product external dependency handling uses W-03 external-source posture and W-11 governance rules.

| Dependency category | Product handling |
| --- | --- |
| EnergyPlus | Domain engine evidence only until product scope, license/name-use, native runtime, security, input/output, validation, and governance are reviewed. |
| OpenStudio | Domain SDK/tooling evidence only until product scope, license/name-use, native/package dependency, security, validation, and governance are reviewed. |
| Omniverse/Kit material | Product/domain visualization dependency candidate; requires license, SDK/runtime, packaging, GPU/local data, security, and publication review. |
| External SDKs | Require provenance, license, dependency graph, compatibility, security, validation, and product-scope decision. |
| External APIs | Require authentication policy, data retention, privacy, network, rate/availability, and provider terms review. |
| External models | Require provenance, license, safety, privacy, storage, runtime, and evaluation review. |
| External datasets | Require provenance, license, sensitivity, size, retention, and product use-scope review. |
| External harnesses | Evidence for product tooling only; no execution or adoption without security/dependency/provider review. |

Dependency governance rules:

| Rule | Meaning |
| --- | --- |
| Product dependency adoption requires review. | License, security, validation, provenance, and governance are mandatory. |
| Product-specific adoption does not promote root dependency. | A dependency accepted for one product is not a global platform dependency. |
| Domain engines stay product/domain scoped. | Energy, building simulation, visualization, and SDK dependencies do not define root platform architecture. |
| No external code execution by default. | External binaries, SDKs, scripts, package managers, and examples require explicit approval. |
| External instructions stay external. | External `AGENTS.md` or equivalent files are not active product or workspace instructions. |

## 11. Product Agent Access Policy

Product agent behavior uses W-10 operating rules.

| Agent behavior | Product rule |
| --- | --- |
| Read product folders only by product ticket. | Product inventory may be read at top level by policy task; deeper inspection requires scope. |
| Edit product files only by product ticket. | Root architecture tasks do not grant product write permission. |
| Do not run product code by default. | Product execution, builds, tests, packages, and scripts require explicit scope. |
| Do not inspect deeply unless scoped. | Avoid reading source trees, dependencies, generated outputs, or local data without product task. |
| Do not promote product docs to root. | Product docs remain product-scoped unless root governance promotes a bounded claim. |
| Do not stage product files unless explicitly instructed. | Product children are ignored by default; the Hermes exception still requires exact human Git authority after source exists. |
| Product subagents return evidence only. | Subagents do not own product activation, validation approval, Git posture, or promotion. |
| Report product uncertainty. | State when product source, docs, dependencies, validation, and risks were not inspected. |

Agent access rule:

```text
Product tasks require product scope. Product proximity does not grant agents deeper
read, edit, execute, validate, stage, or promotion permission.
```

## 12. Product Migration Policy

Product migration uses W-08 migration controls.

| Rule | Meaning |
| --- | --- |
| Product migration was blocked until product policy existed. | W-12 supplies the first product policy, but it does not execute migration. |
| After W-12, migration still requires specific ticket. | A product migration ticket must name product, source, target, status, validation, Git posture, and stop rule. |
| Product docs may migrate before code only if scoped. | Docs-first migration can create product charters or reviewed docs without code tracking. |
| Product code migration requires implementation readiness. | Code tracking/movement requires product activation, architecture, validation, security, dependency posture, and Git decision. |
| Product generated outputs stay local-only unless reviewed. | Generated outputs may become evidence only after provenance and validation review. |
| Product external dependencies remain external. | Dependency review precedes adoption or migration. |
| Migration audit is required. | Product migration should report source/target, status, citations, validation, Git posture, and residual risks. |

Product migration rule:

```text
Product migration should start with product charters and documentation posture, not
code movement or dependency adoption.
```

## 13. Product Activation Preconditions

Product activation requires all of the following preconditions or an explicit governed deferral/exception.

| Precondition | Required declaration |
| --- | --- |
| Product purpose declared | User-facing, domain-facing, interface-facing, or implementation-facing reason for product existence. |
| Product owner declared | Accountable owner for product scope and lifecycle. |
| Product scope declared | Boundaries, non-goals, root interactions, and product-specific authority. |
| Product state declared | Candidate, active, experimental, deferred, blocked, or other W-12 state. |
| Git posture declared | Local-only, docs-only tracked, source tracked, split repo, submodule/subtree/reference, or deferred/archive. |
| Documentation posture declared | Product docs status, source authority, projection path, and citation requirements. |
| Validation baseline declared | Minimum checks, evidence, limitations, and readiness gate. |
| External dependency posture declared | EnergyPlus/OpenStudio/Omniverse/SDK/API/model/dataset/harness dependencies and review status where relevant. |
| Security/access posture declared | Secrets, credentials, data, network, provider auth, local files, generated outputs, publication risk. |
| Root-boundary statement declared | Explicit statement that product does not define AGENT PLATFORM root authority. |
| Migration impact declared | Whether docs/source/generated outputs/dependencies need migration, retention, or archive handling. |

Activation rule:

```text
No product is active until owner, purpose, scope, Git posture, validation, external
dependency posture, security posture, root boundary, and governance posture are declared.
```

## 14. Product Risk Register

| Risk | Severity | Mitigation | Blocks activation? |
| --- | --- | --- | --- |
| Product-root collapse | High | Require root-boundary statement and product-scoped authority labels. | Yes. |
| Committing product code too early | High | Keep product children ignored/local-only until an exact Git posture decision; P12.C3 grants only the absent Hermes path exception. | Yes. |
| Product docs overriding root architecture | High | Use W-09 `product_scoped` status and cite root constraints. | Yes for canonical product docs. |
| Product generated output treated as source | Medium-high | Label generated output and require provenance/validation before use. | Yes when output affects decisions. |
| External domain engines adopted without review | High | Require W-03/W-11 license, security, validation, and governance review. | Yes. |
| License/name-use risk | High | Legal/license and notice review before claims, distribution, or reuse. | Yes. |
| Product data/model leakage | High | Security/access review, local-only handling, no publication by default. | Yes. |
| Hidden secrets | High | Stop, avoid exposure, use secure handling, never commit. | Yes. |
| Experimental product becoming active by proximity | Medium-high | Mark `experimental` as blocked for activation until reviewed. | Yes. |
| Product dependency lock-in | Medium-high | Require dependency alternatives and exit/rollback posture. | May block depending on scope. |
| Product implementation before architecture | High | Require product charter, architecture, validation baseline, and implementation readiness. | Yes. |

Risk rule:

```text
A high product risk blocks activation unless governance records a scoped exception
with owner, mitigation, validation, and review point.
```

## 15. Product Workspace Invariants

| ID | Invariant |
| --- | --- |
| PRODUCT-001 | Products are contained workspaces. |
| PRODUCT-002 | Product folder existence is not activation. |
| PRODUCT-003 | Product docs are product-scoped by default. |
| PRODUCT-004 | Product source does not define root architecture. |
| PRODUCT-005 | Product generated output is not source by default. |
| PRODUCT-006 | Product dependencies require review. |
| PRODUCT-007 | Product Git posture is governed. |
| PRODUCT-008 | Product validation does not approve root authority. |
| PRODUCT-009 | Product scope cannot decide Cognitive Semantic System substrate. |
| PRODUCT-010 | Product activation requires owner, scope, validation, and governance posture. |
| PRODUCT-011 | Product external dependencies remain external until reviewed inside product scope. |
| PRODUCT-012 | Product agents do not own activation, promotion, or Git history. |

Invariant rule:

```text
If product work violates a product invariant, the product remains blocked or
deferred until governance resolves the violation.
```

## 16. Product Anti-patterns

| Anti-pattern | Failure mode | Required correction |
| --- | --- | --- |
| Kit app template as root | Treats an Omniverse/Kit app structure as AGENT PLATFORM architecture. | Keep Omniverse/Kit material product-scoped. |
| Product-root collapse | Product needs override root platform boundaries. | Apply product/root authority boundary. |
| Product code before platform workspace policy | Implementation locks in unresolved root/product boundaries. | Require product charter and readiness first. |
| Product docs as root architecture | Product docs become de facto platform policy. | Use `product_scoped` status and cite root architecture. |
| Domain engine as platform dependency | EnergyPlus/OpenStudio or other engines become root dependencies by use. | Keep domain dependencies product/domain scoped. |
| Generated simulation output as truth | Simulation or product outputs become authority without validation. | Treat outputs as evidence until reviewed. |
| External SDK adoption by proximity | SDK or package presence becomes dependency approval. | Require external dependency governance. |
| Product activation by folder existence | Candidate folder is treated as active product. | Require activation preconditions. |
| Product commit by `git add .` | Local-only product code or artifacts are staged. | Prohibit broad staging; require explicit file list. |
| Experimental product becomes active accidentally | Prototype influences architecture or product roadmap without review. | Keep experimental state blocked until governed. |

Anti-pattern rule:

```text
Product drift starts when product convenience becomes product authority. W-12 keeps
product work useful without letting it govern the workspace root.
```

## 17. Current Product Recommendations

| Product candidate | Current treatment | Recommendation |
| --- | --- | --- |
| `backend-energyplus` | Candidate, deferred, local-only. | Keep local-only; future product charter; future EnergyPlus dependency/license/security review; future implementation readiness review before code tracking. |
| `cli` | Candidate, deferred, local-only. | Keep local-only; future interface product review; future docs-only charter; defer source tracking until command scope and validation are defined. |
| `desktop` | Candidate, deferred, local-only. | Keep local-only; future product charter; future packaging/runtime/security review; defer implementation review. |
| `experimental` | Experimental, blocked, local-only. | Keep local-only; do not activate by proximity; future split/cleanup/retirement review after archive/product policy. |
| `omniverse-app` | Candidate, deferred, local-only. | Keep local-only; future product charter; future Omniverse/Kit dependency and security review; likely separate product or repository review before activation. |
| `web-platform` | Candidate, deferred, local-only. | Keep local-only; future product charter; future web dependency/auth/data/deployment review; defer source tracking until product scope is clear. |

Current recommendation verdict:

```text
No current product candidate should be activated or committed in W-12. The safest
next product work is product-charter drafting by explicit product ticket, beginning
with the highest-priority candidate chosen by a human owner.
```

## 18. Readiness For W-13

Expected next ticket: `W-13 - External Source Handling Policy`.

W-13 can define deeper external-source handling after W-12 because W-12 defines product-specific external dependency posture and keeps domain engines product/domain scoped.

Readiness assessment:

| Area | Verdict | Reason |
| --- | --- | --- |
| Product boundary | Ready enough. | W-12 defines product scope and root-boundary rules. |
| Product external dependency posture | Ready enough for W-13. | W-12 identifies product-specific dependency review needs. |
| Product Git posture | Stable with one later exception. | Product children remain ignored/local-only by default; only future `2_products/hermes-agent` is excepted by P12.C3. |
| Product activation | Not active. | No product is activated in W-12. |
| External source handling | Ready for deeper policy. | W-03 registry and W-12 product dependency rules provide inputs. |
| Product implementation | Not ready. | Product charters, validation, security, and Git posture remain unresolved. |

W-13 should consume:

| Input | Why |
| --- | --- |
| W-03 external source registry | Source roles, license posture, risks, promotion status. |
| W-04 responsibility map | External and product local-only posture. |
| W-08 migration plan | External metadata migration and prohibition on source-code migration. |
| W-10 agent operating rules | Execution, dependency, authentication, and external-source boundaries. |
| W-11 governance model | External promotion, dependency adoption, security, and validation governance. |
| W-12 product policy | Product-specific dependency posture and domain-engine boundaries. |

Readiness verdict:

```text
W-12 makes AGENT PLATFORM ready for W-13 external source handling policy after
explicit instruction. It does not create W-13, activate products, inspect product
source deeply, run code, adopt dependencies, or change product Git posture.
```

## 19. Final Verdict

| Question | Answer |
| --- | --- |
| What is a product workspace? | A bounded workspace area for a user-facing, domain-facing, interface-facing, or implementation-facing product that consumes AGENT PLATFORM capabilities while preserving product-specific scope. |
| Which product candidates exist now? | `backend-energyplus/`, `cli/`, `desktop/`, `experimental/`, `omniverse-app/`, and `web-platform/`. |
| Are any products active now? | No. All six observed sibling products remain local-only; the absent Hermes tracking exception is not activation. |
| What remains local-only? | Every current sibling under `2_products/` remains ignored/local-only. Future `2_products/hermes-agent` alone is normally trackable after corrected P12.1, while generated outputs, dependencies and local data remain excluded. |
| Can product files be committed now? | No. Product files must not be staged or committed until a product-specific governance decision changes Git posture and identifies exact approved files. |
| What should W-13 consume? | W-03, W-04, W-08, W-10, W-11, and W-12, with focus on external-source provenance, license, security, validation, dependency adoption, execution, and product/domain boundaries. |

Final W-12 statement:

```text
AGENT PLATFORM product workspaces are contained, governed, product-scoped areas.
The current sibling folders under `2_products/` are candidates only and remain
local-only. P12.C3 later defines only the absent Hermes tracking exception. Product
activation, product Git posture, product validation, product documentation, product
external dependencies, and product retirement require explicit governance. W-12
stops at product workspace policy and does not start W-13.
```
