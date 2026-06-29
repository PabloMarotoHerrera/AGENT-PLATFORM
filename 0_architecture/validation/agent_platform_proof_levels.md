# AGENT PLATFORM Proof Levels

Status: Canonical V-01 proof levels model  
Date: 2026-06-29  
Scope: Proof-level architecture for AGENT PLATFORM validation before validation evidence specialization, migration execution, product activation, external dependency adoption, implementation readiness, publication, provider/network/auth/MCP activity, registry implementation, or Cognitive Semantic System implementation  
Authority: Validation architecture only. This document defines proof levels, proof strength, proof sufficiency, proof scope, proof limitations, proof transitions, proof interactions, and proof matrices. It does not implement proof-level enforcement, implement the validation registry, create schemas, create JSON/YAML registry files, create code, create tests, create scripts, create tools, create CI, create hooks, create scanners, create runtime guards, create packages, create SDKs, modify V-00, modify S-series docs, modify W-series docs, modify `.gitignore`, run project/product/external code, install dependencies, authenticate, call providers/APIs/networks/registries/cloud/package indexes/local daemons/MCP servers, activate MCP, stage, commit, push, create V-02 through V-05, create V-A, start implementation, execute migration, activate products, adopt external dependencies, publish, or decide the Cognitive Semantic System substrate.

## 1. Purpose

V-01 defines the canonical proof levels model for AGENT PLATFORM validation.

V-01 follows V-00 because V-00 defines the validation registry architecture: validation targets, claims, questions, criteria, methods, evidence, results, verdicts, limitations, residual risks, blockers, freshness, retention, status, and governance/security relationships. V-00 explicitly reserved proof-level finalization for V-01.

V-01 specializes proof levels without implementing a registry or automation.

| Boundary | V-01 rule |
| --- | --- |
| V-00 defines validation registry architecture. | V-00 remains the source for validation objects, status, verdicts, evidence categories, method taxonomy, registry-entry fields, blockers, retention, and freshness. |
| V-01 defines proof levels. | V-01 defines proof strength labels, sufficiency posture, target applicability, limitations, transitions, matrices, and interactions with V-00 statuses/verdicts. |
| V-01 is not registry implementation. | It creates no database, storage, schema, graph, document store, registry file, service, or runtime. |
| V-01 is not a test suite. | It defines when tests can contribute proof later; it does not create or run tests. |
| V-01 is not CI. | It creates no workflow, gate, hook, status check, badge, or automation. |
| V-01 is not proof automation. | It defines semantics for humans and later systems; it does not compute proof levels automatically. |
| V-01 is not governance approval. | Proof can support, block, or qualify governance; governance still decides. |
| V-01 does not authorize adjacent work. | It does not authorize migration, implementation, product activation, external adoption, provider calls, execution, staging, commit, push, publication, or any next ticket. |

V-01 consumes these mandatory inputs:

| Input | V-01 use |
| --- | --- |
| `0_architecture/validation/agent_platform_validation_registry_architecture.md` | Source for validation objects, status, verdicts, evidence, methods, retention, blockers, and V-01 readiness. |
| S-00 through S-04 | Security/access, local-only, secret, credential, execution, command, network, MCP, product, external, Git, and publication boundaries. |
| S-A | Coherence audit confirming S-series readiness for validation architecture. |
| W-A | Workspace audit confirming W-series coherence and next-phase blockers. |
| W-10 | Agent active-ticket, scope, execution, validation, Git, product, external, citation, and stop rules. |
| W-05 | Context pack source classes, exclusions, citation, projection, and context-not-permission rules. |
| W-11 | Governance/promotion boundary and promotion preconditions. |
| W-04 and W-07 | Responsibility and topology boundaries for source classes, product/external/local-only areas, implementation, tests, datasets, models, artifacts, and context. |
| W-12 | Product scope, product validation, activation preconditions, and product-local-only posture. |
| W-13 | External source review, metadata, dependency, pattern, execution, instruction, and substrate-neutrality posture. |
| W-09 | Documentation status, scope, citation, lifecycle, projection, and metadata posture. |
| W-08 | Migration source classes, restatement, validation, Git, and audit requirements. |
| `.gitignore` | Git/local-only posture evidence for products, external sources, previous knowledge, datasets, models, artifacts, generated outputs, secrets, credentials, provider auth, dependencies, and caches. |
| `README.md` | Minimal root descriptor; not full authority. |

V-01 rule:

```text
Proof levels classify how strong scoped validation evidence is. They do not make a
claim true, approve a decision, override security, promote authority, or authorize
execution or Git actions.
```

## 2. Proof Level Definition

A proof level is a scoped label for the strength, method, evidence quality, reproducibility, freshness, and limitations of validation evidence for a specific claim, target, artifact, behavior, or decision candidate.

Proof levels answer:

| Question | Answer type |
| --- | --- |
| What evidence exists? | Metadata, source status, citations, coherence review, command output, tests, audit, or reproduction. |
| How direct is the evidence? | Indirect metadata, source/citation evidence, review evidence, command evidence, behavioral test evidence, audit evidence, or reproduced evidence. |
| What method produced it? | Non-command review, bounded command, tests, structured audit, independent rerun, or repeated validation. |
| How fresh is it? | Current, stale, superseded, invalidated, date-bound, or unknown. |
| What can it support? | Explanation, proposal, governance review, scoped promotion support, or blocker handling. |
| What can it not support? | Approval, broad truth, publication, product activation, dependency adoption, migration execution, implementation, or substrate decision. |

Clarifications:

| Proof level is not | Rule |
| --- | --- |
| Truth | A proof level is evidence-strength posture, not semantic truth. |
| Governance | Governance decides acceptance, rejection, deferral, exception, promotion, and lifecycle. |
| Approval | Proof can support approval review; it does not approve. |
| Git state | Git status, diff, commit, or push can be evidence, not proof by itself. |
| Model confidence | Confidence scores, agent confidence, or model agreement are not proof levels. |
| Context inclusion | Being included in a context pack does not elevate proof. |
| Unscoped label | Every proof level applies only to declared scope, target, criterion, evidence, and limitations. |
| Unlimited support | Every proof level has limitations and residual risk. |
| Permanent | Proof can become stale, superseded, invalidated, blocked, partial, inconclusive, or failed. |

Proof-level invariant:

```text
No proof level is valid without scope, criterion, evidence, and limitations.
```

## 3. Proof Model

Proof in AGENT PLATFORM is a structured validation posture made from the following elements:

```text
claim or target
+ criterion
+ method
+ evidence
+ result
+ limitation
+ scope
+ freshness
+ sensitivity
+ source status
+ reviewer
+ revalidation trigger
+ proof level
```

Required proof elements:

| Element | Requirement |
| --- | --- |
| Claim or target | The exact claim, artifact, file, command, output, behavior, readiness state, or decision candidate being evaluated. |
| Criterion | The declared condition used to judge the target. |
| Method | The validation method: metadata check, source-status review, citation review, coherence review, command check, test, audit, or reproduction. |
| Evidence | The material, output, review note, path metadata, citation, command output, test output, audit finding, or reproduction evidence used. |
| Result | Factual outcome of the method. |
| Limitation | What the evidence does not prove, what was not inspected, and which risks remain. |
| Scope | The area where the proof applies. |
| Freshness | Currentness and revalidation triggers. |
| Sensitivity | Public, internal, local-only, sensitive, restricted, secret, credential, external-restricted, product-restricted, generated-sensitive, or unknown. |
| Source status | Canonical, proposal, research, evidence, migration evidence, external reference, product-scoped, generated, historical, implementation note, or unknown. |
| Reviewer | Human, role, or agent contributor who performed or recorded validation. |
| Revalidation trigger | Change that requires proof review or rerun. |
| Proof level | PL-0 through PL-8 from Section 4. |

Invalid proof conditions:

| Missing element | Consequence |
| --- | --- |
| Missing scope | Proof level invalid; cannot support promotion-quality use. |
| Missing criterion | Proof level invalid; evidence has no standard for interpretation. |
| Missing evidence | Proof level invalid; label is unsupported. |
| Missing limitation | Proof level invalid; overclaims are uncontrolled. |
| Missing source status | At most PL-1 unless source status is clearly not needed. |
| Missing sensitivity | Proof cannot be safely retained, cited, or exposed. |
| Missing reviewer/date | Proof may be usable as working evidence but weak for governance support. |
| Missing revalidation trigger | Proof freshness cannot be governed reliably. |

## 4. Proof Level Catalog

Canonical proof levels:

| Level | Name | Definition | Evidence required | Method type | Command required? | Execution risk | Applicable targets | Insufficient uses | Limitations | Freshness risk | Can support proposal? | Can support promotion? | Governance still required? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PL-0 | `unvalidated` | No scoped validation evidence exists for the target or claim. | None, or explicit absence/gap record. | None or gap classification. | No. | None. | Any target as a gap state. | Cannot support promotion, implementation readiness, migration execution, product activation, dependency adoption, publication, or substrate decision. | Absence of validation says nothing about correctness. | Immediate; any target/source change keeps it unvalidated. | Yes, only as uncertainty or gap evidence. | No. | Yes for any decision that proceeds by exception or deferral. |
| PL-1 | `metadata_checked` | Path, file metadata, existence, ignore posture, worktree visibility, or basic record metadata was checked. | Path check, file metadata, Git status/check-ignore, or safe metadata summary. | Metadata validation. | Sometimes, for `Test-Path`, `Get-Item`, `git status --short`, or `git check-ignore`. | R0/R2 when scoped. | Files, docs, Git state, local-only posture, registry references, generated artifact metadata. | Content correctness, citation quality, semantic coherence, behavior, security safety, promotion. | Confirms existence/posture only, not meaning. | High; paths and worktree state change quickly. | Yes, for inventory/proposal context. | Usually no; may support a small governance precondition only when combined with higher proof. | Yes. |
| PL-2 | `source_status_checked` | Source class, status, sensitivity, scope, and authority posture were reviewed. | Status/scope/sensitivity/source-class evidence with cited authority. | Source-status review. | No by default. | R1 read-only review; optional R2 metadata checks if scoped. | Docs, research, previous knowledge, external metadata, product material, generated artifacts, datasets, models, context packs. | Claim truth, behavioral validation, promotion by itself. | Classification can be wrong, stale, or incomplete. | Medium; status/policy/source changes can stale it. | Yes. | No by itself; required input for promotion support. | Yes. |
| PL-3 | `citation_reviewed` | Material claims cite appropriate source authority or evidence and missing citations are identified. | Citation map, source paths, cited status, uncertainty notes, missing-citation findings. | Citation/provenance review. | Usually no; bounded search/path checks optional if scoped. | R1/R2 if commands are used. | Architecture docs, validation docs, security docs, projections, research, previous restatements, external reviews, product docs. | Runtime behavior, implementation correctness, dependency approval, product activation, publication by itself. | Citation presence does not prove cited claim is true. | Medium; citations and source files can change. | Yes. | Conditional support for governance review; not sufficient alone for most promotion. | Yes. |
| PL-4 | `coherence_reviewed` | Claims, criteria, citations, source status, boundaries, matrices, and policy interactions were reviewed for consistency within declared scope. | Review findings, compared inputs, contradiction/tension register, limitations, residual risks. | Coherence, matrix, contradiction, policy review. | No by default; bounded naming/path checks optional if scoped. | R1/R2 if commands are used. | Architecture, security/access, validation policy, documentation projections, migration plans, product charters, external metadata. | Runtime behavior, tested implementation, dependency safety, product execution, publication approval. | Coherence is not enforcement and can miss hidden defects. | Medium; policy or input changes stale it. | Yes. | May support architecture/documentation/security promotion when criteria fit and no blockers remain; not approval. | Yes. |
| PL-5 | `command_checked` | Explicit scoped command(s) produced expected validation evidence for the declared target. | Exact command, working directory, expected result, actual output summary, side effects, sensitivity review, limitations. | Command-result validation. | Yes. | R0-R12 depending command; V-01 validation uses only listed low-risk commands. | Path checks, Git checks, bounded naming checks, metadata checks, future build/test/runtime evidence if approved. | Broad correctness, adjacent command approval, promotion, security override, implementation readiness by itself. | Command proves only what it checks in its environment. | High; command, environment, target, and worktree can change. | Yes. | Conditional support if command is appropriate and combined with source/status/limitations; not enough for high-risk promotion alone. | Yes. |
| PL-6 | `tested_for_scope` | Approved tests passed for a named target, scope, environment, and criteria. | Exact test command, test scope, environment, output summary, artifacts, failures/skips, sensitivity handling, limitations. | Test validation. | Yes. | Usually R4 or higher; product/external/package/network tests can be R5-R10. | Future implementation code, product behavior, scripts/tools/tests, packages/SDKs, selected runtime behaviors. | Global correctness, security approval, product activation, publication, root authority, dependency adoption. | Tests cover only named cases and environment. | High; code, tests, dependencies, env, and product state change. | Yes. | Can support implementation/product governance only after specialized validation exists; not V-01 alone. | Yes. |
| PL-7 | `audited_for_scope` | A structured audit reviewed required evidence, status, criteria, methods, blockers, limitations, residual risk, and policy alignment for scope. | Audit scope, files/evidence reviewed, matrix results, contradiction register, blocker register, residual risks, reviewer/date. | Structured audit. | Not necessarily; may include scoped commands. | R1/R2 unless audit includes approved execution. | Architecture docs, security docs, validation docs, migration plans/batches later, product readiness later, external metadata later, publication candidates. | Perfect safety, zero residual risk, governance approval, implementation, migration execution, product activation by itself. | Audit quality depends on scope, reviewer, and evidence completeness. | Medium; audit stales when inputs/policies/targets change. | Yes. | Strong support for governance review and scoped promotion when specialized requirements are satisfied. | Yes. |
| PL-8 | `reproduced_for_scope` | Independent or repeated validation reproduced the evidence/result for the same declared scope and criteria. | Original proof reference, reproduction method, reproducer/reviewer, environment, repeated results, differences, limitations, residual risk. | Reproduction or independent rerun/review. | Sometimes; depends on what is reproduced. | Inherits reproduced method risk. | High-impact claims, implementation behavior, product behavior, external metadata/dependency evidence, migration audit, critical architecture/security claims. | Absolute truth, approval, future correctness, security override, substrate decision by itself. | Reproduction can still share assumptions, stale inputs, or environmental bias. | Medium-high; reproduction stales with source/env/policy changes. | Yes. | Strongest support for governance, but still scoped and never automatic approval. | Yes. |

Governance linkage is not a proof level:

| Concept | V-01 decision |
| --- | --- |
| `governed_reference` | This is not proof of correctness. It is a governance linkage or registry relation indicating that governance accepted, cited, or used a validation reference for a decision. It can strengthen traceability, but it does not become PL-9 and does not validate the target by itself. |
| Governance approval | Approval is a decision posture, not validation proof. Approval may require proof, accept a proof limitation by exception, reject proof as insufficient, or request revalidation. |

## 5. Proof Level Semantics

| Level | What it can mean | What it cannot mean |
| --- | --- | --- |
| PL-0 `unvalidated` | No proof exists; target is a gap, uncertainty, or blocker. | Target is false, safe, unsafe, correct, incorrect, approved, or irrelevant. |
| PL-1 `metadata_checked` | Path, metadata, Git/ignore posture, or basic record presence was checked. | Content is correct, source is authoritative, citations are adequate, behavior works, or promotion is allowed. |
| PL-2 `source_status_checked` | Source class, status, sensitivity, and scope are known enough for the declared review. | Claims are true, evidence is sufficient, content is coherent, or the source can be promoted. |
| PL-3 `citation_reviewed` | Material claims cite appropriate sources or missing citations are visible. | Cited sources prove the claim, citations are current forever, or runtime behavior is validated. |
| PL-4 `coherence_reviewed` | Internal and cross-document consistency was reviewed for declared scope. | Enforcement exists, runtime behavior is correct, tests passed, or governance approved. |
| PL-5 `command_checked` | Specific scoped commands passed or produced recorded evidence for exact criteria. | Adjacent commands are approved, broad correctness is proven, output is safe by default, or promotion is approved. |
| PL-6 `tested_for_scope` | Tests passed for named scope, environment, and criteria. | Global correctness, security safety, product activation, dependency adoption, release, or publication is approved. |
| PL-7 `audited_for_scope` | A structured audit found no blockers or identified blockers for its declared scope. | Residual risk is eliminated, future changes remain valid, or governance has approved. |
| PL-8 `reproduced_for_scope` | Evidence/result was independently or repeatedly reproduced for scope and criteria. | Truth is absolute, future drift is impossible, security/access is overridden, or governance is unnecessary. |

Semantics rule:

```text
Each proof level describes evidence strength and method. It does not replace status,
verdict, governance posture, security posture, or source authority.
```

## 6. Proof Strength Dimensions

Proof strength is the combined quality of the validation evidence, method, scope, freshness, and controls. Higher proof levels usually require stronger dimensions, but proof strength is still scoped and limited.

| Dimension | Stronger posture | Weak posture | Required handling |
| --- | --- | --- | --- |
| Source availability | Source path/reference available and stable. | Source missing, inaccessible, or only summarized. | Mark missing source as blocker or limitation. |
| Source status clarity | Canonical/evidence/research/external/product/generated/local-only status known. | Unknown or conflicting status. | Classify before promotion-quality use. |
| Citation quality | Claims cite direct, current, scoped sources. | Vague, stale, indirect, missing, or source-status-blind citations. | Add citations or lower proof. |
| Criteria clarity | Criteria are explicit and relevant. | Criteria missing, implicit, or too broad. | Proof invalid until criteria exist. |
| Method appropriateness | Method directly tests/reviews the claim. | Method checks nearby metadata or unrelated behavior. | State limitation or choose better method. |
| Evidence directness | Evidence directly supports the claim. | Evidence is circumstantial, generated, stale, or inferred. | Lower proof or mark inconclusive. |
| Reproducibility | Method can be repeated with known inputs/environment. | One-off output or undocumented method. | Record method, command, environment, inputs. |
| Independence | Independent reviewer/rerun or structured audit exists. | Same agent/output repeated without new evidence. | Do not inflate proof by agreement alone. |
| Freshness | Evidence current to target, policy, environment, and criteria. | Source, policy, env, or target changed. | Mark stale or revalidate. |
| Sensitivity handling | Secrets/local-only/sensitive outputs minimized and labeled. | Raw sensitive content exposed or retained. | Stop, classify, summarize safely, or invalidate handling. |
| Security/access compliance | S-series posture followed. | Access, execution, local-only, secret, or auth policy unresolved. | Security can block proof elevation. |
| Execution policy compliance | Commands exact, scoped, approved, reported. | Unapproved or broad command; unclear side effects. | Proof is blocked or invalidated. |
| Reviewer qualification | Reviewer role/profile fits target and scope. | Unqualified or unspecified reviewer. | Record limitation and require review. |
| Residual risk clarity | Remaining risk visible and owned. | Risk hidden or claimed eliminated. | Proof invalid for promotion support until limits recorded. |
| Revalidation triggers | Triggers declared. | No freshness model. | Add triggers or mark weak proof. |
| Governance linkage | Related decision/review candidate recorded. | No owner or decision relation. | Cannot support promotion without governance path. |

Proof strength rules:

| Rule | Meaning |
| --- | --- |
| Higher proof level does not override security/access. | A PL-8 result can still be blocked by secret exposure, local-only policy, access limits, or execution policy. |
| Higher proof level does not remove governance. | PL-8 supports governance; it does not approve. |
| Proof level is not a score. | A higher number is not globally better if the method does not fit the target. |
| Target fit matters. | Architecture docs may not need tests; code behavior may require tests or reproduction. |

## 7. Proof Scope Model

Proof scope defines where a proof level applies and what cannot be inferred beyond it.

| Scope | What proof can apply | What proof cannot infer | Required source status | Required limitation statement |
| --- | --- | --- | --- | --- |
| `workspace_root` | Root architecture, vocabulary, governance, validation, security, topology, and cross-area boundaries. | Product behavior, external dependency approval, implementation correctness, final substrate. | Canonical/proposal workspace architecture or governed decision evidence. | State root-only scope and excluded product/external/implementation surfaces. |
| `architecture_domain` | Domain architecture claims and cross-doc coherence. | Runtime behavior, code correctness, product activation, dependency adoption. | Canonical/proposal architecture with cited evidence. | State domain, dependent docs, and implementation gap. |
| `security_access` | Security/access policy alignment, sensitivity, execution, local-only, secrets, credentials. | Technical enforcement exists or risk is eliminated. | Canonical S-series/security evidence. | State architecture-only and enforcement gap. |
| `validation_policy` | Validation/proof/status/verdict/evidence policy coherence. | Registry implementation, automation, tests, or CI exists. | Canonical V-series validation architecture. | State conceptual-only and future specialization gaps. |
| `documentation_projection` | Projection fidelity, citations, status/scope, no authority drift. | Projection is source authority or current if source changed. | Projection plus source authority refs. | State projection status and source dependency. |
| `research_scope` | Research method, citations, uncertainty, evidence usefulness. | Accepted decision or authority. | Research/evidence status. | State uncertainty, method limits, freshness. |
| `migration_scope` | Source classification, restatement fidelity, target posture, audit readiness. | Migration execution or promotion by itself. | Migration evidence, W-02/W-08 classification, target status. | State no movement/execution and V-03 dependency. |
| `product_workspace` | Product charter, product-scope docs, product validation evidence, activation blockers. | Root authority or product activation by proof alone. | Product-scoped/candidate/local-only/product evidence. | State product scope and root-boundary limit. |
| `external_source` | Metadata, provenance, license posture, risk, pattern evidence, blocked uses. | Dependency adoption, source reuse, execution approval, substrate decision. | External reference/metadata/review evidence. | State external evidence-only and V-05 dependency. |
| `implementation_scope` | Implementation plan/readiness, code/test evidence when approved later. | Implementation approval, release, deployment, runtime safety. | Implementation note/code evidence after scoped ticket. | State current implementation gap and required future validation. |
| `data_scope` | Dataset metadata, provenance, license, sensitivity, retention. | Data use, publication, training, or privacy safety by itself. | Data evidence/local-only metadata. | State local-only/sensitivity and use prohibition. |
| `model_scope` | Model metadata, provenance, license, safety, storage, use scope. | Model execution, deployment, or safety approval. | Model evidence/local-only metadata. | State execution/use gap and safety limits. |
| `artifact_scope` | Generated artifact provenance, generator/input, review status. | Source truth or publication safety. | Generated/generated-sensitive/evidence status. | State generated-output limit and review need. |
| `context_pack_scope` | Context source selection, status labels, freshness, exclusions, stop rules. | Context is proof, permission, or authority. | Projection/context/evidence status. | State context-not-proof and source dependency. |
| `publication_scope` | Publication candidate safety, citations, local-only exclusion, license/security checks. | Publication approval by proof alone. | Reviewed projection/candidate evidence. | State governance/publication approval remains required. |
| `governance_candidate` | Evidence sufficiency, proof posture, blockers, owner, decision readiness. | Decision outcome. | Candidate/proposal/evidence/governance refs. | State governance still decides. |
| Cognitive Semantic System candidate scope | Candidate semantic record/projection/substrate evidence, provenance, lifecycle, neutrality. | Final substrate, semantic truth, or implemented system. | Candidate/proposal/research/evidence status. | State substrate undecided and graph remains only a candidate representation. |

## 8. Proof Sufficiency Model

Proof sufficiency asks whether a proof level and supporting posture are strong enough for a specific use.

| Use | Minimum proof posture | Governance required? | Security/access required? | Future specialized V-ticket required? |
| --- | --- | --- | --- | --- |
| Answer/support explanation | PL-1 if only metadata; PL-2/PL-3 when source/status/citations matter; uncertainty explicit. | No, unless answer makes authority claim. | Yes, for sensitive/local-only/source exposure. | No. |
| Create proposal | PL-2 minimum; PL-3 preferred for cited claims; PL-4 for architecture/security/validation proposals. | Not to draft; yes to accept. | Yes. | Usually no, unless target is migration/product/external/implementation. |
| Create canonical policy draft | PL-3 minimum; PL-4 preferred; PL-7 for high-impact architecture/security/validation policy. | Yes to promote to canonical. | Yes. | V-02 may be needed for evidence specialization later. |
| Support governance review | PL-4 for architecture/policy; PL-5 if command evidence matters; PL-7 for high-impact review. | Yes. | Yes. | Sometimes, based on domain. |
| Support promotion | PL-4 plus complete source/status/citations/security for low-risk docs; PL-7 preferred; PL-8 for high-risk claims. | Yes. | Yes. | Often V-02; V-03/V-04/V-05 for specialized domains. |
| Support migration planning | PL-3/PL-4 for plan and restatement readiness. | Yes for plan acceptance. | Yes. | V-03 for execution/audit specialization. |
| Support migration execution | PL-7-like migration readiness plus V-03 criteria; PL-5 for exact path/Git checks where scoped. | Yes. | Yes. | Yes, V-03. |
| Support product activation | Product-specific proof with owner/scope/security/dependency baseline; likely PL-7/PL-8 for activation-critical evidence. | Yes. | Yes. | Yes, V-04. |
| Support external dependency adoption | External provenance/license/security/dependency/validation proof; likely PL-7/PL-8 for adoption. | Yes. | Yes. | Yes, V-05. |
| Support implementation readiness | PL-4 for plans; PL-5/PL-6/PL-7 later for code/test/build/runtime evidence. | Yes. | Yes. | V-02 plus later implementation readiness architecture. |
| Support execution approval | PL-2/PL-3 for target/source status, plus exact S-04 command preconditions; PL-5 only after command runs. | Yes for risky execution. | Yes. | V-02 for evidence model; domain-specific ticket for execution. |
| Support publication | PL-4/PL-7 publication review: source authority, projection fidelity, no secrets/local-only leakage, license/product/external/security review. | Yes. | Yes. | V-02 and domain-specific reviews as needed. |
| Support Cognitive Semantic System substrate decision | PL-7/PL-8 across multiple substrate candidates, plus explicit ADR/governance. | Yes. | Yes. | Future substrate decision process beyond V-01. |

Sufficiency rules:

| Rule | Meaning |
| --- | --- |
| Proposal can use lower proof if uncertainty is explicit. | PL-1/PL-2 can support inventory or hypothesis proposals, not acceptance. |
| Promotion needs stronger proof and governance. | Minimum proof depends on target class and risk; governance remains mandatory. |
| Insufficient proof can still be useful. | PL-0/PL-1/PL-2 can identify gaps and blockers. |
| Specialized domains need specialized validation. | Migration execution needs V-03; product activation needs V-04; external adoption needs V-05. |
| Substrate decision is not a proof-level side effect. | It requires explicit ADR/governance and multi-candidate evaluation. |

## 9. Target Class Minimum Proof Matrix

| Target class | Minimum proof for proposal | Minimum proof for promotion/support | Specialized validation needed? | Security/access review needed? | Governance needed? | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Workspace architecture doc | PL-3 | PL-4, PL-7 for high-impact canonical promotion | V-02 later for evidence specialization | Yes | Yes for promotion | Architecture proof does not implement. |
| Security/access doc | PL-3 | PL-4 plus security coherence; PL-7 for audit-quality support | V-02 later | Yes | Yes | Enforcement remains absent. |
| Validation doc | PL-3 | PL-4; PL-7 for cross-series audit support | V-02/V-A later | Yes | Yes | No registry implementation implied. |
| Documentation projection | PL-3 | PL-4 projection fidelity; PL-7 for publication candidate | V-02 for evidence details | Yes for publication/local-only | Yes for promotion/publication | Projection cannot exceed source authority. |
| Research evidence | PL-2 | PL-3/PL-4 as evidence support | V-02 later | Yes if sensitive/external/local-only | Yes if promoted | Research remains evidence. |
| Previous knowledge restatement | PL-3 | PL-4 plus migration classification; V-03 for migration batch | Yes, V-03 for migration execution | Yes | Yes | Prior canonical labels are historical. |
| External source metadata | PL-2 | PL-4 metadata review; PL-7 for adoption candidate | Yes, V-05 for adoption/execution | Yes | Yes | Metadata is not dependency approval. |
| Raw external source claim | PL-2 for classification | PL-4 non-execution review; PL-7/PL-8 with V-05 for high-risk use | Yes, V-05 | Yes | Yes | Execution/copy/adoption blocked. |
| Product charter | PL-3 | PL-4; PL-7 for activation support | Yes, V-04 for activation baseline | Yes | Yes | Product scope only. |
| Product validation baseline | PL-3 | PL-7 with V-04 | Yes, V-04 | Yes | Yes | Product tests do not prove root authority. |
| Migration plan | PL-3 | PL-4; PL-7 for migration readiness | Yes, V-03 for execution | Yes | Yes | Plan does not execute migration. |
| Migration batch | PL-3 planning | PL-7 with V-03 audit; PL-5 for exact checks | Yes, V-03 | Yes | Yes | No bulk migration. |
| Implementation plan | PL-3 | PL-4; PL-7 for readiness later | V-02 plus implementation readiness | Yes | Yes | Planning only. |
| Code artifact | PL-2/PL-3 for review proposal | PL-6/PL-7 later, maybe PL-8 for critical behavior | V-02 plus future implementation validation | Yes | Yes | Code proof not ready in V-01. |
| Script/tool/test artifact | PL-2/PL-3 | PL-5/PL-6/PL-7 after trust/execution approval | V-02 plus execution policy | Yes | Yes | Running is separate approval. |
| Package/SDK artifact | PL-2/PL-3 | PL-7/PL-8 after dependency/release review | V-02 plus package/SDK policy | Yes | Yes | Build/install/publish blocked. |
| Dataset | PL-2 metadata | PL-4 metadata/provenance; PL-7 for use/publication candidate | V-02/future data policy | Yes | Yes | Local-only/sensitivity likely. |
| Model | PL-2 metadata | PL-4 metadata/safety/use-scope; PL-7 for use candidate | V-02/future model policy | Yes | Yes | Model use/execution blocked. |
| Generated artifact | PL-1/PL-2 | PL-4 review; PL-5 if command provenance matters | V-02 for evidence retention | Yes | Yes if promoted/published | Generated is not source. |
| Runtime log | PL-1/PL-2 safe metadata | PL-4 safe review; PL-5 if command provenance exists | V-02/future runtime validation | Yes | Yes if used | Sensitive/local-only by default. |
| Command output | PL-5 | PL-5 plus PL-3/PL-4 context; PL-7 for high-impact use | V-02 | Yes | Yes if used for decision | Command output is evidence only. |
| Git status/diff | PL-1/PL-5 | PL-5 for Git-state claim; not enough for semantic promotion | V-02 for records | Yes for local-only/secret risk | Yes for Git actions | Git is not proof of correctness. |
| Context pack | PL-2/PL-3 | PL-4 projection/source-selection review | V-02 later | Yes | Yes if accepted/promoted | Context inclusion is not proof. |
| Publication candidate | PL-3 | PL-7 publication review, possibly PL-8 for high-risk claims | V-02 plus domain reviews | Yes | Yes | Proof supports review but does not publish. |
| Cognitive Semantic System candidate record | PL-3 | PL-7/PL-8 for decision support | Future substrate decision process | Yes | Yes | Substrate remains undecided. |

## 10. Proof Level Transition Model

Nominal proof elevation path:

| Transition | Meaning |
| --- | --- |
| `unvalidated` -> `metadata_checked` | Required path, metadata, or basic Git/ignore posture was checked. |
| `metadata_checked` -> `source_status_checked` | Source class, status, sensitivity, and scope became known. |
| `source_status_checked` -> `citation_reviewed` | Claims were tied to source authority or evidence references. |
| `citation_reviewed` -> `coherence_reviewed` | Claims, citations, criteria, boundaries, and policy interactions were reviewed. |
| `coherence_reviewed` -> `command_checked` | Exact scoped commands produced evidence. |
| `command_checked` -> `tested_for_scope` | Approved tests passed for named scope and environment. |
| `tested_for_scope` -> `audited_for_scope` | A structured audit reviewed evidence, methods, blockers, and residual risks. |
| `audited_for_scope` -> `reproduced_for_scope` | Independent or repeated validation reproduced the evidence/result. |

Non-linear transitions:

| Transition | Meaning |
| --- | --- |
| Any level -> `stale` | Target, source, policy, environment, criteria, command, context, or governance changed. |
| Any level -> `invalidated` | Incident, wrong scope, unsafe evidence handling, or contradictory later evidence makes proof unusable for current claim. |
| Any level -> `superseded` | Newer proof replaces older proof. |
| Any level -> `blocked` | Security, access, missing evidence, missing criteria, missing owner, missing approval, local-only, secret, product, external, or dependency blocker prevents use. |
| Any level -> `failed` | Criteria were not satisfied. |
| Any level -> `partial` | Some checks completed but coverage is incomplete. |
| Any level -> `inconclusive` | Evidence cannot support pass or fail. |
| Any level -> `deferred` | Validation or sufficiency decision is postponed. |

Transition clarifications:

| Clarification | Rule |
| --- | --- |
| Proof levels are not always sequential. | A target can move directly from PL-0 to PL-4 if a coherence review includes status and citation review, but missing lower-layer elements must still be recorded. |
| Some targets should not reach command/test proof. | Architecture docs may be sufficiently validated through citation, coherence, matrix alignment, contradiction audit, naming check, and security/access review. |
| Some targets require command/test proof. | Code, runtime behavior, scripts, packages, products, and implementation claims may need PL-5/PL-6/PL-7 later. |
| Higher level can be unusable. | A PL-8 reproduction with secret exposure or wrong scope can be blocked or invalidated. |

## 11. Proof Status Interaction

V-00 separates validation status from proof level. Proof level describes strength/type; validation status describes current state; verdict describes result; governance posture describes decision.

| V-00 status | Proof interaction |
| --- | --- |
| `not_validated` | Usually PL-0. Marks absence, gap, or blocker. |
| `validation_not_required` | No proof level may be needed for that criterion; record rationale and scope. |
| `validation_planned` | Planned proof target, but current proof remains PL-0 or existing historical level. |
| `validation_scoped` | Scope/criteria/method ready; proof level not achieved until evidence exists. |
| `validation_running` | Interim state; do not assign final proof level until complete. |
| `validation_passed` | Proof level can be assigned if criteria/evidence/limitations are complete. |
| `validation_failed` | Proof level may describe method strength, but verdict blocks use for support. |
| `validation_blocked` | Existing proof may be unusable; blocker dominates sufficiency. |
| `validation_skipped` | No new proof gained; record reason and implication. |
| `validation_partial` | Assign maximum achieved proof only for completed scope and mark partial. |
| `validation_inconclusive` | Method may have a proof level, but result cannot support pass/fail. |
| `validation_stale` | Historical proof remains, but cannot support current promotion without review. |
| `validation_invalidated` | Proof cannot support current claim; new validation required. |
| `validation_superseded` | Older proof preserved as trace; newer proof controls current use. |
| `validation_deferred` | Proof not current or not complete; decision waits or accepts deferral. |
| `validation_exception` | Governance accepts a bounded gap; exception is not proof. |

Separation rule:

```text
Proof level, validation status, verdict, and governance posture must be recorded as
separate concepts. Combining them hides blockers and creates false approval.
```

## 12. Proof Verdict Interaction

A verdict interprets evidence against criteria. A proof level states evidence strength/method. A high proof level can still have a blocking verdict.

| V-00 verdict | Proof interaction |
| --- | --- |
| `pass_for_scope` | Proof may support the declared scope if status is current and limitations are recorded. |
| `fail_for_scope` | Proof method may be strong, but result blocks support unless fixed, rescoped, or excepted. |
| `blocked_by_security` | Security blocks proof use or elevation regardless of proof level. |
| `blocked_by_access` | Access limits block proof use/elevation regardless of evidence strength. |
| `blocked_by_missing_evidence` | Proof cannot reach claimed level; lower proof or PL-0 applies. |
| `blocked_by_missing_owner` | Proof may exist but cannot support promotion-quality governance. |
| `blocked_by_missing_criteria` | Proof level invalid until criteria exist. |
| `blocked_by_missing_dependency_review` | External/package/product adoption proof cannot support adoption. |
| `blocked_by_missing_product_scope` | Product proof cannot support activation/readiness. |
| `blocked_by_missing_external_review` | External proof cannot support reuse/adoption/execution. |
| `blocked_by_missing_execution_approval` | Command/test/runtime proof cannot be produced by unapproved execution. |
| `partial_pass` | Proof applies only to completed criteria; unsupported areas remain gaps. |
| `inconclusive` | Method evidence exists but cannot support pass/fail. |
| `stale` | Historical proof cannot support current promotion without review. |
| `not_applicable` | Criterion removed for scope; no proof of that criterion is implied. |
| `deferred` | Proof/evaluation postponed; no promotion-quality support until resumed. |
| `requires_governance_decision` | Proof may be strong, but decision is outside validation authority. |

Verdict rule:

```text
A high proof level with a blocking verdict is still blocked.
```

## 13. Proof Evidence Requirements

| Evidence category | Required fields | Allowed safe retention | Sensitivity handling | Local-only handling | Citation requirement | Freshness requirement | Limitation requirement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Metadata checked evidence | Path/ref, command if any, result, date, reviewer, source/sensitivity if known. | Boolean/path/metadata summary. | Avoid revealing sensitive paths/details if unsafe. | Use safe metadata only unless scoped. | Cite path and command/review. | Recheck when path/Git/file state changes. | State metadata does not prove content. |
| Source status evidence | Source class, status, scope, sensitivity, authority posture, source doc used. | Classification table or summary. | Treat unknown as sensitive. | Preserve local-only label. | Cite status authority. | Recheck when source/policy/status changes. | State classification does not validate claims. |
| Citation review evidence | Claims reviewed, citations present/missing, source status, review date. | Citation findings and missing-citation list. | Avoid quoting sensitive source content. | Cite local-only by metadata/path only if safe. | Cite sources and target doc. | Recheck when target/source citations change. | State citations do not prove truth. |
| Coherence review evidence | Inputs compared, criteria, contradictions/tensions, matrices, residual risks. | Review notes, tables, safe excerpts. | Avoid sensitive excerpts. | Use safe summaries for local-only inputs. | Cite all compared docs. | Recheck when any compared input changes. | State review may miss issues and is not enforcement. |
| Command output evidence | Exact command, working directory, expected/actual result, output summary, side effects, risk level. | Summary and command metadata; raw output only if safe. | Stop on secrets/credentials/sensitive output. | Do not dump local-only output; safe metadata only. | Cite command, target, date. | Recheck when command/env/target changes. | State command proves only exact check. |
| Test output evidence | Exact test command, target, environment, pass/fail/skips, artifacts, logs, limitations. | Summary and metadata; logs only if reviewed. | Treat logs as generated-sensitive. | Product/local outputs remain local-only. | Cite command, target, env/date. | Recheck when code/tests/deps/env change. | State test coverage limits. |
| Audit evidence | Audit scope, entries/files reviewed, method, findings, gaps, residual risks, reviewer/date. | Audit report or safe summary. | Avoid exposing sensitive details. | Use safe metadata for local-only evidence. | Cite inputs and audit target. | Recheck when audited inputs/policies change. | State audit scope and remaining risk. |
| Reproduction evidence | Original proof ref, reproducer, method, environment, repeated result, differences, date. | Reproduction summary and references. | Same sensitivity rules as reproduced method. | Same local-only handling as original evidence. | Cite original and reproduction evidence. | Recheck when source/env/criteria change. | State shared assumptions and reproduction limits. |

Evidence rule:

```text
Evidence must be retained enough to audit the proof, but not enough to leak secrets,
credentials, local-only content, or unsafe raw output.
```

## 14. Proof Limitations

No proof level is valid without explicit limitations.

| Limitation type | Required statement |
| --- | --- |
| Scope limitation | The exact scope where proof applies and what is excluded. |
| Method limitation | What the method can and cannot show. |
| Source limitation | Missing, stale, external, product-scoped, generated, historical, local-only, or uncertain source posture. |
| Freshness limitation | Date/currentness and revalidation triggers. |
| Sensitivity limitation | Sensitive/local-only/secret/credential restrictions and exposure minimization. |
| Execution limitation | Whether execution occurred, was blocked, was not applicable, or needs S-04 approval. |
| Environment limitation | OS, shell, dependencies, runtime, product state, local machine, or configuration assumptions. |
| Product limitation | Product-scope boundary and no root-authority inference. |
| External-source limitation | External evidence-only boundary and no reuse/adoption/execution approval. |
| Migration limitation | No movement/promotion/execution by proof alone; V-03 needed for migration execution. |
| Governance limitation | Proof supports decisions but cannot approve. |
| Generated-output limitation | Generated material is not source by default and may be sensitive/stale. |
| Reproducibility limitation | Whether result was not reproduced, partially reproduced, or reproduced with shared assumptions. |

Limitation invariant:

```text
If limitations are missing, the proof level is inflated and invalid for promotion
support.
```

## 15. Proof Freshness / Revalidation

Proof must be revalidated when any of the following occur:

| Trigger | Revalidation consequence |
| --- | --- |
| Target changes | Recheck proof for affected target. |
| Source changes | Recheck source-dependent claims, citations, and status. |
| Citation changes | Re-run citation/source review. |
| Policy changes | Reassess criteria, sufficiency, blockers, and limitations. |
| Security/access posture changes | Recheck exposure, retention, local-only, secret, credential, access, and execution posture. |
| Execution policy changes | Reassess command/test/build/runtime proof eligibility. |
| Dependency changes | Revalidate implementation/product/package/build/test claims. |
| Product state changes | Recheck product proof, scope, activation, validation baseline, and Git posture. |
| External source version changes | Recheck provenance, license, runtime, dependency, network/auth, and review limits. |
| Validation criteria change | Prior proof may be stale, invalid, or not applicable. |
| Command changes | Prior command result does not apply to new command. |
| Environment changes | Test/build/runtime proof may no longer apply. |
| Generated output changes | Re-review generated artifact provenance and content. |
| Incident occurs | Mark affected proof blocked or invalidated pending review. |
| Governance decision supersedes prior posture | Update related proof references and currentness. |
| Context pack becomes stale | Context-based proof support cannot be current without source refresh. |
| Cognitive Semantic System substrate decision affects target | Reassess representation/lifecycle/access assumptions. |

Freshness rules:

| Rule | Meaning |
| --- | --- |
| Stale proof remains historical evidence. | It explains past decisions and prior state. |
| Stale proof cannot support current promotion without review. | Revalidate, supersede, or record a governed exception. |
| Stale proof may support historical reasoning. | Use for trace, regressions, prior decisions, and supersession analysis. |

## 16. Proof / Security Boundary

V-01 uses S-series security/access boundaries.

| Security rule | Proof consequence |
| --- | --- |
| Security can block proof elevation. | Unsafe target, method, evidence, output, command, retention, or publication stops proof use. |
| Secret/credential exposure invalidates proof handling. | Do not store, quote, transform, hash, test, or validate secret/credential values. |
| Local-only evidence may limit proof portability. | Proof can be local-only and unusable for public/committed/published support. |
| Validation outputs may be generated-sensitive. | Command output, logs, test output, reports, screenshots, and artifacts require review. |
| Proof records must not store secrets. | Store safe metadata and blockers only. |
| Execution-based proof requires S-04 compliance. | Exact command, working directory, risk, side effects, output handling, approval, and stop rule are required. |
| Provider/network/auth/MCP proof requires explicit approval. | Availability of credentials, network, providers, or MCP tools is not permission. |
| Proof cannot override access restrictions. | Active ticket, source status, sensitivity, role, and approval posture control access. |

Security boundary statement:

```text
Proof cannot make unsafe evidence safe. Security/access posture controls what proof
may inspect, execute, retain, cite, expose, or use.
```

## 17. Proof / Governance Boundary

V-01 uses W-11 governance boundaries.

| Governance relation | V-01 rule |
| --- | --- |
| Proof supports governance. | Proof can provide evidence strength and sufficiency posture for a decision. |
| Proof can block governance. | Failed, stale, partial, missing, or blocked proof can block or qualify promotion. |
| Proof can qualify decisions. | Limitations and residual risks narrow what governance may accept. |
| Proof cannot approve. | Approval requires governance authority. |
| Proof cannot promote. | Promotion is a governance transition. |
| Proof cannot publish. | Publication requires governance, security, source, license, product/external, and local-only review. |
| Proof cannot activate products. | Product activation requires product/governance preconditions and V-04 later. |
| Proof cannot adopt external dependencies. | Adoption requires provenance, license, security, validation, dependency, and governance review, with V-05 later. |
| Proof cannot decide final Cognitive Semantic System substrate. | Substrate decision requires explicit ADR/governance and multi-candidate evaluation. |
| Proof cannot authorize Git actions. | Staging, commit, push, history mutation, and publication remain human-gated. |

Governance boundary statement:

```text
Proof supplies evidence-strength posture. Governance decides what to do with that
posture.
```

## 18. Proof / Context Boundary

V-01 uses W-05 and S-series context boundaries.

| Context rule | Proof consequence |
| --- | --- |
| Proof evidence included in context must preserve status and sensitivity. | Context must label canonical, evidence, research, external, product-scoped, generated, local-only, stale, secret, credential, and unknown material. |
| Local-only proof evidence is excluded by default. | Use safe metadata unless explicit local-only scope exists. |
| Secret/credential proof evidence is never included. | Values are never context material. |
| Generated proof evidence is labeled generated. | Generated outputs remain evidence/projection until reviewed and governed. |
| Stale proof is labeled stale. | Historical proof cannot appear as current proof in context. |
| Context inclusion is not validation. | Selection does not evaluate evidence against criteria. |
| Context inclusion is not proof elevation. | Being in a pack does not move PL-0 to PL-1 or higher. |

Context statement:

```text
Context can expose proof-relevant material. It does not create proof.
```

## 19. Proof / Git Boundary

Git can support proof as bounded evidence but is never proof by itself.

| Git surface | Proof boundary |
| --- | --- |
| Git status/diff | Can support PL-1/PL-5 Git-state proof when scoped. |
| Git commit | Not proof, not validation, not governance, not semantic truth. |
| Git push | Publication action, not proof. |
| Git staging | Not proof and requires explicit human approval. |
| Clean worktree | Does not prove correctness, safety, or validation. |
| Committed document | Not validated by being committed. |
| Proof records referencing Git | May cite status/diff/hash as evidence only. |
| Git actions | Remain human-gated and cannot be authorized by proof. |

Git statement:

```text
Git records state. Proof interprets scoped evidence. Governance decides.
```

## 20. Architecture Proof Levels

Architecture proof evaluates architecture documents, claims, boundaries, matrices, and policy relationships.

Expected architecture proof levels:

| Architecture proof component | Typical proof level |
| --- | --- |
| Path/status metadata | PL-1. |
| Source status/scope/sensitivity | PL-2. |
| Citations and provenance | PL-3. |
| Coherence, matrix alignment, contradiction review, boundary review | PL-4. |
| Bounded naming/path/Git checks | PL-5. |
| Structured architecture audit | PL-7. |
| Independent repeated architecture audit | PL-8. |

Architecture proof rules:

| Rule | Meaning |
| --- | --- |
| Architecture claims often rely on PL-2 through PL-7. | Metadata, status, citations, coherence, scoped commands, and audit are the main proof sources. |
| Runtime PL-6 tests may not apply. | Architecture docs usually validate through review/audit, not code tests. |
| Coherence is central. | Citation, matrix alignment, contradiction audit, naming check, and security/access review are key. |
| Architecture proof does not implement anything. | It cannot create runtime enforcement, code, schemas, CI, or registry behavior. |
| Architecture proof does not approve governance. | Governance must accept, promote, reject, defer, or except. |

## 21. Documentation Projection Proof Levels

Documentation projection proof evaluates whether human-facing or context-facing documentation faithfully projects source authority.

| Projection concern | Proof requirement |
| --- | --- |
| Source authority citation | PL-3 minimum for material claims. |
| Projection fidelity | PL-4 review against source authority. |
| Stale projection risk | Freshness trigger when source changes. |
| Local-only/secret leakage | Security/access review; proof blocked if unsafe. |
| Projection overriding architecture | Must be blocked; projections cannot outrank source authority. |
| Generated projection | Generator/input/review status required; generated output is not source. |

Projection rules:

| Rule | Meaning |
| --- | --- |
| Proof level cannot exceed source authority without additional review. | A projection with PL-4 fidelity cannot make a PL-2 source claim stronger. |
| Human docs can simplify, not alter. | Changes in meaning require source architecture update or governance decision. |
| Projection proof supports docs review. | It does not publish or promote by itself. |

## 22. Research Proof Levels

Research proof evaluates source quality, method, freshness, uncertainty, and relevance.

| Research use | Proof posture |
| --- | --- |
| Support explanation | PL-2/PL-3 with uncertainty. |
| Support proposal | PL-3/PL-4 when claims cite sources and method/freshness are clear. |
| Support decision | Requires governance review and usually PL-4 or higher depending impact. |
| External research/source claims | Need provenance, source status, license/risk awareness where relevant. |

Research rules:

| Rule | Meaning |
| --- | --- |
| Research can support proposals. | It is useful evidence when citations, method, and uncertainty are clear. |
| Research freshness matters. | Stale research must be labeled and may need revalidation. |
| Research is not decision. | Governance accepts, rejects, defers, or promotes. |
| Research proof may be evidence-strength, not authority-strength. | Strong research can still remain evidence only. |

## 23. Previous Knowledge Restatement Proof Levels

Previous knowledge restatement proof evaluates current restatements derived from historical material.

Required proof components:

| Component | Requirement |
| --- | --- |
| W-02 classification | Prior material must have classification before use. |
| Original source citation | Cite original path and classification state when material. |
| Restatement fidelity | Review whether current wording preserves concept without importing stale scope. |
| Current vocabulary normalization | Use AGENT PLATFORM and Cognitive Semantic System vocabulary. |
| Conflict normalization | Conflicted naming/scope/substrate claims require resolution before promotion. |
| No wholesale migration | Restate concepts; do not copy prior docs wholesale. |
| Current governance | Promotion requires current status, validation, and governance. |

Restatement proof rules:

| Rule | Meaning |
| --- | --- |
| Prior canonical labels are historical. | They do not create current authority. |
| PL-3 is a minimum for cited restatement. | PL-4 is needed for fidelity/coherence support. |
| Migration execution remains out of scope. | V-03 must specialize migration validation. |

## 24. Migration Proof Levels Placeholder

V-01 defines only general proof rules for migration. Migration validation will be specialized in V-03.

| Migration item | V-01 proof posture |
| --- | --- |
| Migration plan | PL-3/PL-4 can support planning and governance review. |
| Migration source classification | PL-2 minimum, PL-3 when cited. |
| Migration restatement | PL-3/PL-4 for citations and fidelity. |
| Migration execution support | Requires stronger proof and V-03. |
| Migration audit | Likely PL-7 when V-03 defines audit trail requirements. |

Migration placeholder rules:

| Rule | Meaning |
| --- | --- |
| Proof does not execute migration. | File movement, copying, archive, rename, deletion, and promotion remain blocked. |
| Migration execution requires V-03. | V-01 cannot authorize first batches. |
| Migration proof must preserve local-only posture. | Previous knowledge and product/external/data/model/artifact surfaces remain controlled. |

Do not create V-03 from V-01.

## 25. Product Proof Levels Placeholder

V-01 defines only general proof rules for products. Product proof will be specialized in V-04.

| Product item | V-01 proof posture |
| --- | --- |
| Product charter | PL-3/PL-4 can support charter proposal and product-scope review. |
| Product validation baseline | Needs V-04 for baseline structure and sufficiency. |
| Product activation | Requires product-specific proof, security/access, dependency posture, owner/scope, governance, and V-04. |
| Product tests | Product-scoped; likely PL-6 or higher after exact test approval. |
| Product generated outputs | Generated/product-restricted evidence until reviewed. |

Product placeholder rules:

| Rule | Meaning |
| --- | --- |
| Product proof does not prove root authority. | Product proof is product-scoped. |
| Product tests do not activate products. | Activation requires governance and V-04. |
| Product folders remain local-only candidates. | Existing product folders are not active by proof or proximity. |

Do not create V-04 from V-01.

## 26. External Source Proof Levels Placeholder

V-01 defines only general proof rules for external sources. External source validation will be specialized in V-05.

| External item | V-01 proof posture |
| --- | --- |
| External metadata | PL-2/PL-3 for status/provenance/citations; PL-4 for metadata coherence review. |
| Raw external source execution | Blocked; no execution proof without explicit future approval. |
| License evidence | Evidence only, not reuse approval. |
| Source review | Evidence for relevance/risk, not dependency adoption. |
| Graph-oriented external evidence | Candidate substrate evidence only; it does not decide the Cognitive Semantic System substrate. |

External placeholder rules:

| Rule | Meaning |
| --- | --- |
| External proof does not approve dependency adoption. | Adoption requires V-05, security/license/dependency review, and governance. |
| External proof does not approve source copying. | Source reuse needs exact governed approval. |
| External instructions remain inactive. | They do not instruct AGENT PLATFORM agents. |

Do not create V-05 from V-01.

## 27. Implementation Proof Levels Placeholder

Implementation proof is not ready in V-01.

| Implementation area | V-01 posture |
| --- | --- |
| Implementation plans | PL-3/PL-4 can support planning, constraints, and readiness discussion. |
| Code artifact proof | Later may require source review, tests, builds, runtime evidence, audit, or reproduction. |
| Package/dependency proof | Requires dependency review, provenance, license, security, exact versions, and governance. |
| Scripts/tools/tests | Require trust state, source review, side-effect review, S-04 execution posture, and exact approval before running. |
| Implementation readiness | Remains blocked until later architecture/readiness work and validation specialization. |

Implementation rule:

```text
V-01 can classify future implementation proof needs. It cannot start implementation
or approve code, tests, builds, packages, SDKs, or runtime work.
```

## 28. Data / Model / Artifact Proof Levels

| Target | Required proof concerns | V-01 posture |
| --- | --- | --- |
| Dataset | Provenance, license, sensitivity, privacy, retention, intended use, local-only posture. | PL-2/PL-4 metadata/provenance review; no use/publication approval. |
| Model | Provenance, license, safety, privacy, storage, use scope, execution posture. | PL-2/PL-4 metadata/safety/use-scope review; no execution/use approval. |
| Generated artifact | Generator, inputs, command/method, review status, sensitivity, freshness. | PL-1/PL-4 depending evidence; generated is not source by default. |
| Runtime log | Command/process/source, sensitivity, secret risk, relevance, environment. | Safe metadata by default; raw content local-only/generated-sensitive. |
| Local-only evidence | Safe metadata, source/sensitivity labels, no default context/Git/publication. | Proof may be local-only and not commit-safe. |

Data/model/artifact rules:

| Rule | Meaning |
| --- | --- |
| Datasets require provenance/license/sensitivity proof. | Metadata proof is not data-use approval. |
| Models require provenance/license/safety/use-scope proof. | Metadata proof is not model execution approval. |
| Artifacts require generator/input/review proof. | Generated artifacts are evidence, not source. |
| Logs may be sensitive. | Retain safe summaries unless explicit review permits more. |
| Local-only proof evidence may not be commit-safe. | Proof can exist without being publishable. |

## 29. Publication Proof Levels

Publication candidates require proof that publication would not expose unsafe content and that claims project source authority correctly.

Publication proof requirements:

| Requirement | Minimum proof posture |
| --- | --- |
| Source authority proof | PL-3/PL-4 source/citation/coherence review. |
| Projection fidelity proof | PL-4 against source authority. |
| No secrets/credentials | Security review; any secret/credential exposure blocks publication. |
| Local-only exclusion proof | PL-1/PL-5 ignore/status checks where scoped plus content/source review. |
| Product/external/license check | Product/external/license/security review; V-04/V-05 where needed. |
| Security/access review | Required. |
| Governance approval | Required and separate from proof. |

Publication rule:

```text
Proof supports publication review. Proof does not publish.
```

## 30. Proof Level Matrices

### Matrix A. Proof Level Vs Evidence Requirement

| Level | source status required | citations required | command required | test required | audit required | reproduction required | security/access required | governance still required | can support proposal | can support promotion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PL-0 | No | No | No | No | No | No | For gap handling if sensitive | Yes if used for decision | Limited gap proposal | No |
| PL-1 | Helpful | No | Sometimes | No | No | No | Yes for paths/local-only | Yes | Yes | Usually no |
| PL-2 | Yes | Usually | No | No | No | No | Yes | Yes | Yes | No by itself |
| PL-3 | Yes | Yes | Usually no | No | No | No | Yes | Yes | Yes | Conditional, weak alone |
| PL-4 | Yes | Yes | Optional | No | No | No | Yes | Yes | Yes | Conditional for architecture/docs/policy |
| PL-5 | Yes for target | Yes if claims involved | Yes | No | No | No | Yes, including S-04 | Yes | Yes | Conditional, target-specific |
| PL-6 | Yes | Yes | Yes | Yes | No | No | Yes, including execution output | Yes | Yes | Conditional after specialized validation |
| PL-7 | Yes | Yes | Optional | Optional | Yes | No | Yes | Yes | Yes | Strong support if scope fits |
| PL-8 | Yes | Yes | Optional | Optional | Usually | Yes | Yes | Yes | Yes | Strongest support, still not approval |

### Matrix B. Target Class Vs Minimum Useful Proof Level

| Target | proposal | support/promotion | specialized V-ticket needed | governance needed | notes |
| --- | --- | --- | --- | --- | --- |
| architecture docs | PL-3 | PL-4/PL-7 | V-02 later | Yes | Tests usually not applicable. |
| security docs | PL-3 | PL-4/PL-7 | V-02 later | Yes | Enforcement not implied. |
| validation docs | PL-3 | PL-4/PL-7 | V-02/V-A later | Yes | Registry not implemented. |
| docs projections | PL-3 | PL-4/PL-7 for publication | V-02 later | Yes | Projection fidelity key. |
| research | PL-2/PL-3 | PL-3/PL-4 | V-02 later | If promoted | Evidence only. |
| previous knowledge restatements | PL-3 | PL-4 plus V-03 for migration | V-03 | Yes | Historical labels not current. |
| migration plans | PL-3 | PL-4/PL-7 | V-03 for execution | Yes | Plan only. |
| migration execution | PL-4 planning | PL-7 with V-03 | V-03 | Yes | Not authorized by V-01. |
| product charters | PL-3 | PL-4 | V-04 for activation | Yes | Product-scoped. |
| product activation | PL-4 planning | PL-7/PL-8 with V-04 | V-04 | Yes | Activation blocked. |
| external metadata | PL-2/PL-3 | PL-4/PL-7 | V-05 for adoption/execution | Yes | Metadata only. |
| external dependency adoption | PL-4 planning | PL-7/PL-8 with V-05 | V-05 | Yes | Adoption blocked. |
| implementation plans | PL-3 | PL-4/PL-7 later | V-02/future readiness | Yes | Planning only. |
| implementation code | PL-2/PL-3 | PL-6/PL-7/PL-8 later | V-02/future implementation validation | Yes | Not ready. |
| scripts/tools/tests | PL-2/PL-3 | PL-5/PL-6/PL-7 later | V-02/future execution controls | Yes | Execution separate. |
| datasets | PL-2 | PL-4/PL-7 for use candidate | V-02/future data policy | Yes | Local-only likely. |
| models | PL-2 | PL-4/PL-7 for use candidate | V-02/future model policy | Yes | Use/execution blocked. |
| generated artifacts | PL-1/PL-2 | PL-4/PL-5 if command provenance | V-02 | Yes if promoted | Not source. |
| context packs | PL-2/PL-3 | PL-4 | V-02 later | Yes if accepted | Context is projection. |
| publication candidates | PL-3 | PL-7 | V-02 plus domain reviews | Yes | Publication blocked until approval. |
| Cognitive Semantic System candidate records | PL-3 | PL-7/PL-8 | Future substrate decision process | Yes | Substrate undecided. |

### Matrix C. Proof Level Vs Validation Status/Verdict

| Level | possible statuses | possible verdicts | stale handling | blocker handling | limitation requirement |
| --- | --- | --- | --- | --- | --- |
| PL-0 | not_validated, planned, scoped, skipped, blocked, deferred | blocked_by_missing_evidence, blocked_by_missing_criteria, deferred, not_applicable | Already no current proof; mark gap date. | Record blocker. | State no validation evidence. |
| PL-1 | passed, failed, partial, stale, superseded, invalidated | pass_for_scope, fail_for_scope, partial_pass, stale | Recheck metadata/path/Git state. | Missing path/status blocks. | Metadata only. |
| PL-2 | passed, failed, partial, stale, superseded | pass_for_scope, fail_for_scope, inconclusive, stale | Recheck status/sensitivity/source. | Unknown source/sensitivity blocks. | Classification only. |
| PL-3 | passed, failed, partial, stale, inconclusive | pass_for_scope, fail_for_scope, partial_pass, inconclusive | Recheck citations and sources. | Missing citation/source blocks. | Citation does not prove truth. |
| PL-4 | passed, failed, partial, stale, invalidated | pass_for_scope, fail_for_scope, partial_pass, requires_governance_decision | Reaudit when inputs/policies change. | Contradictions/security blockers dominate. | Coherence not enforcement. |
| PL-5 | passed, failed, blocked, partial, stale, invalidated | pass_for_scope, fail_for_scope, blocked_by_missing_execution_approval, stale | Rerun or review command/env/target. | Missing approval/output sensitivity blocks. | Exact command only. |
| PL-6 | passed, failed, blocked, partial, stale, invalidated | pass_for_scope, fail_for_scope, partial_pass, blocked_by_security | Rerun tests on code/test/env/dependency change. | Unapproved tests/deps/env blocks. | Test coverage/env limits. |
| PL-7 | passed, failed, partial, stale, superseded | pass_for_scope, fail_for_scope, requires_governance_decision, stale | Reaudit when audited set changes. | Audit gaps/blockers visible. | Audit scope/residual risk. |
| PL-8 | passed, failed, partial, stale, superseded, invalidated | pass_for_scope, fail_for_scope, requires_governance_decision, stale | Reproduce again when triggers occur. | Shared assumptions/security blockers visible. | Reproduction scope/assumptions. |

### Matrix D. Proof Level Vs Residual Risk

| Level | residual risk expected | escalation required | revalidation trigger | insufficient for |
| --- | --- | --- | --- | --- |
| PL-0 | Unknown and high. | Yes if decision depends on target. | Any use beyond gap statement. | Promotion, activation, adoption, implementation, publication. |
| PL-1 | High for semantics/content. | If used beyond metadata. | Path/Git/file state change. | Content correctness, claims, behavior. |
| PL-2 | Medium-high for claim correctness. | If promoted or sensitive. | Status/source/policy change. | Claim truth and promotion alone. |
| PL-3 | Medium; citation gaps may remain. | If citations missing/stale. | Citation/source change. | Runtime behavior and approval. |
| PL-4 | Medium; review may miss issues. | If contradictions/security risks remain. | Input/policy/criteria change. | Runtime/code/product/external execution proof. |
| PL-5 | Medium-high outside command scope. | If output sensitive or command high risk. | Command/env/target change. | Global correctness and adjacent execution. |
| PL-6 | Medium; coverage/env gaps remain. | If tests fail/skip or output sensitive. | Code/test/dependency/env change. | Global correctness, security, release approval. |
| PL-7 | Lower for audited scope; residual risk still present. | If audit finds blockers or high-impact gaps. | Audited input/policy/target change. | Absolute safety and approval by itself. |
| PL-8 | Lowest for reproduced scope; not zero. | If reproduction differs or high-impact decision follows. | Source/env/criteria/policy change. | Truth without governance, future correctness. |

## 31. Proof Invariants

| ID | Invariant |
| --- | --- |
| PROOF-001 | Proof is scoped. |
| PROOF-002 | Proof is not truth by itself. |
| PROOF-003 | Proof is not governance. |
| PROOF-004 | Proof is not approval. |
| PROOF-005 | Proof level requires criteria. |
| PROOF-006 | Proof level requires evidence. |
| PROOF-007 | Proof level requires limitations. |
| PROOF-008 | Higher proof does not override security. |
| PROOF-009 | Higher proof does not remove governance. |
| PROOF-010 | Passing tests does not approve promotion. |
| PROOF-011 | Git commit is not proof. |
| PROOF-012 | Context inclusion is not proof. |
| PROOF-013 | Generated output is not proof unless validated. |
| PROOF-014 | Stale proof cannot support current promotion without review. |
| PROOF-015 | Product proof is product-scoped. |
| PROOF-016 | External proof does not approve dependency adoption. |
| PROOF-017 | Migration proof does not execute migration. |
| PROOF-018 | Cognitive substrate remains undecided. |

Invariant rule:

```text
If a proof invariant conflicts with convenience, the invariant controls and the
blocker or limitation must be recorded.
```

## 32. Proof Anti-patterns

| Anti-pattern | Failure mode | Correction |
| --- | --- | --- |
| High proof level without criteria | Label has no standard. | Define criteria or lower/void proof. |
| High proof level without limitations | Overclaims evidence. | Add explicit limitations. |
| Proof by confidence | Confuses model/agent confidence with evidence. | Require criteria and evidence. |
| Proof by Git commit | Treats history as correctness. | Use validation evidence. |
| Proof by passing test only | Hides scope/security/governance limits. | Record scope, coverage, environment, residual risk. |
| Proof by generated summary | Treats projection as source. | Cite source evidence and review. |
| Proof by subagent agreement | Treats agreement as evidence. | Use independent source/method evidence. |
| Proof by context inclusion | Treats selected exposure as validation. | Validate against source and criteria. |
| Proof by README | Treats descriptor or external instructions as authority. | Cite current authority and review. |
| Proof by external source presence | Treats local snapshot as adoption. | Use external review and governance. |
| Proof by product test as root truth | Collapses product scope into root. | Keep product proof product-scoped. |
| Proof by migration audit as migration approval | Lets audit approve movement. | Governance approves migration. |
| Proof by clean worktree | Treats no visible changes as correctness. | Validate target claims directly. |
| Proof by no output | Assumes silence means pass. | Require expected result and explicit interpretation. |
| Proof by old canonical label | Imports historical authority. | Restate and govern in current scope. |
| Proof by graph projection | Treats representation/projection as truth or substrate decision. | Preserve substrate neutrality and governance. |
| Proof by unreviewed artifact | Treats output/log/report as source. | Review provenance, sensitivity, freshness, and limits. |
| Proof level inflation | Assigns higher PL than evidence supports. | Lower proof or gather missing evidence. |
| Stale proof reused as current | Uses historical evidence for current promotion. | Revalidate or record exception. |

## 33. Remaining Gaps

V-01 does not solve:

| Gap | Status after V-01 |
| --- | --- |
| Validation evidence model specialization | Not solved; V-02 target. |
| Migration validation specialization | Not solved; V-03 target. |
| Product validation specialization | Not solved; V-04 target. |
| External source validation specialization | Not solved; V-05 target. |
| Validation audit | Not solved; V-A target. |
| Registry implementation | Not implemented. |
| Schemas | Not created. |
| CI | Not created. |
| Tests | Not created or run. |
| Scanners | Not created. |
| Enforcement | Not implemented. |
| Context-pack validation generator | Not created. |
| Product validation baselines | Not created. |
| Dependency approval registry | Not created. |
| Implementation readiness | Not approved or created. |
| Cognitive Semantic System implementation | Not implemented; substrate remains undecided. |

Blocked until later phases:

| Later phase | Must specialize |
| --- | --- |
| V-02 | Validation evidence types, retention, evidence locations, sensitivity, citations, freshness, generated outputs, command outputs, review notes, and evidence usability. |
| V-03 | Migration validation, source/target mapping, restatement fidelity, local-only posture, Git posture, and audit trail. |
| V-04 | Product validation baseline, product tests, product readiness, activation proof, product security/dependencies, and product-scope limits. |
| V-05 | External source validation, provenance, license, dependency/adoption/execution review, source-copy review, and substrate-evidence limits. |
| V-A | Validation audit across V-series and active validation records. |

## 34. Readiness For V-02

V-02 target: Validation Evidence Model.

Readiness assessment:

| Area | Readiness | Rationale |
| --- | --- | --- |
| Proof levels | Ready. | V-01 defines PL-0 through PL-8. |
| Evidence requirements | Ready enough. | V-01 defines evidence categories and minimum fields by proof level. |
| Status/verdict separation | Ready. | V-01 maps proof levels to V-00 statuses and verdicts while keeping them separate. |
| Security/access boundary | Ready. | V-01 preserves S-series constraints and safe retention posture. |
| Governance boundary | Ready. | V-01 preserves proof-as-support, not approval. |
| Evidence specialization | Not done. | V-02 must define detailed evidence types, retention, locations, sensitivity, citations, freshness, generated outputs, command outputs, review notes, and evidence usability. |

V-02 should specialize:

| V-02 topic | Required coverage |
| --- | --- |
| Evidence types | Command output, review notes, metadata, citations, tests, audits, generated artifacts, logs, Git state, external/product/migration/data/model evidence. |
| Retention | What to store, summarize, omit, redact, or keep local-only. |
| Evidence locations | Path refs, registry refs, decision refs, artifact refs, safe metadata refs. |
| Sensitivity | Public/internal/local-only/sensitive/restricted/secret/credential/external/product/generated/unknown handling. |
| Citations | How evidence cites sources, source status, commands, reviewers, and limits. |
| Freshness | Revalidation triggers and stale/superseded/invalidated evidence handling. |
| Generated outputs | Generator/input/provenance/review status and source limitations. |
| Command outputs | Exact command, working directory, risk, side effects, output handling, and limitations. |
| Review notes | Reviewer, method, files inspected, findings, uncertainty, and residual risk. |
| Evidence usability | What evidence can support explanation, proposal, governance review, promotion support, or blocker handling. |

Do not create V-02 from V-01.

## 35. Final Verdict

| Question | Answer |
| --- | --- |
| What proof levels now exist? | PL-0 `unvalidated`, PL-1 `metadata_checked`, PL-2 `source_status_checked`, PL-3 `citation_reviewed`, PL-4 `coherence_reviewed`, PL-5 `command_checked`, PL-6 `tested_for_scope`, PL-7 `audited_for_scope`, and PL-8 `reproduced_for_scope`. |
| What does each proof level mean? | Each level describes the method and strength of scoped validation evidence, from no validation through metadata/status/citation/coherence/command/test/audit/reproduction evidence. |
| What is proof sufficiency? | Whether a proof level and its evidence, criteria, scope, limitations, freshness, sensitivity, and source status are strong enough for a declared use. |
| What can proof support? | Explanations, proposals, governance review, scoped promotion support, blocker handling, freshness review, and future specialized validation. |
| What can proof never approve? | Governance approval, promotion, publication, staging, commit, push, migration execution, product activation, external dependency adoption, provider/API/network/MCP calls, authentication, implementation, or final Cognitive Semantic System substrate selection. |
| What remains blocked? | V-02 through V-05/V-A, registry implementation, schemas, CI, tests, scanners, enforcement, migration execution, product activation, external adoption, implementation, package managers, provider/network/auth/MCP activity, staging, commit, push, publication, and substrate decision. |
| Is V-02 ready after explicit instruction? | Yes. V-01 defines enough proof-level architecture for V-02 validation evidence specialization. |
| What should V-02 consume? | V-00, V-01, S-00 through S-04, S-A, W-A, W-10, W-11, W-05, W-08, W-09, W-12, W-13, `.gitignore`, `README.md`, and current active-task constraints. |

V-01 validation record:

| Validation category | Status |
| --- | --- |
| Git worktree check | Completed. `git status --short` reported `?? 0_architecture/validation/agent_platform_proof_levels.md`, consistent with the newly created V-01 file and no staging, commit, or push. |
| Required input existence checks | Passed. Individual scoped `Test-Path` checks returned `True` for `.gitignore`, `README.md`, V-00, V-01, required S-series files, and required W-series files named in the validation command list. |
| Target file metadata check | Passed. Scoped `Get-Item 0_architecture/validation/agent_platform_proof_levels.md` returned file metadata successfully. |
| Optional `.gitignore` representative checks | Passed. Individual `git check-ignore` checks returned the expected ignored paths for `previusknowledge/`, `2_products/`, `4_external/sources/`, `7_datasets/`, `8_models/`, `9_artifacts/`, `.env`, `.env.local`, `secrets/test.txt`, and `credentials/test.txt`. |
| Optional prohibited legacy naming check | Passed. Bounded `Select-String` over `0_architecture/validation/*.md` for the prohibited legacy authority phrases returned no matches. |

Final V-01 statement:

```text
V-01 defines AGENT PLATFORM proof levels as scoped evidence-strength labels. Proof
levels help determine whether validation evidence can support explanations,
proposals, governance review, or promotion support, while preserving the boundary:
proof evaluates evidence strength, governance decides, security constrains, access
scopes, context exposes, Git records, generated output remains evidence, and the
Cognitive Semantic System substrate remains undecided.
```

Stop rule:

```text
After completing V-01, STOP. Do not start V-02, V-03, V-04, V-05, V-A,
implementation, migration, product activation, external adoption, staging, commit,
push, publication, provider/API/network/MCP activity, authentication, or any later
ticket unless explicitly instructed.
```
