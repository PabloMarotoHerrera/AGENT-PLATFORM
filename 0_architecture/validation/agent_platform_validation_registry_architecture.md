# AGENT PLATFORM Validation Registry Architecture

Status: Canonical V-00 validation registry architecture  
Date: 2026-06-29  
Scope: Conceptual validation registry architecture for AGENT PLATFORM before migration execution, implementation, product activation, external dependency adoption, provider integration, runtime work, or Cognitive Semantic System implementation  
Authority: Validation architecture only. This document defines concepts, objects, statuses, evidence, methods, registry-entry fields, retention principles, blockers, incidents, matrices, and readiness for later validation phases. It does not implement a registry, create schemas, create code, create tests, create scripts, create tools, create CI, create hooks, create scanners, create runtime guards, create packages, create SDKs, modify S-series docs, modify W-series docs, modify `.gitignore`, run project/product/external code, install dependencies, authenticate, call providers/APIs/networks/registries/cloud/package indexes/local daemons/MCP servers, stage, commit, push, create V-01 through V-05, create V-A, start implementation, execute migration, activate products, adopt external dependencies, or decide the Cognitive Semantic System substrate.

## 1. Purpose

V-00 defines the validation registry architecture for AGENT PLATFORM.

It follows Proyecto W because W-00 through W-14 established the workspace identity, source classes, topology, context strategy, migration controls, documentation model, agent operating rules, governance model, product policy, external-source policy, and final workspace synthesis.

It follows W-A because W-A confirmed the workspace architecture is coherent but not ready for migration execution or implementation, and identified validation registry architecture as a blocker for first migration batches, implementation, product activation, external adoption, and authority promotion.

It follows GIT-01 because GIT-01 hardened `.gitignore` for previous knowledge, products, external sources, datasets, models, artifacts, generated outputs, secrets, credentials, provider auth, local auth, and caches. V-00 must treat Git/local-only posture as validation evidence, not as security enforcement or authority.

It follows S-00 through S-04 because validation must operate inside the security/access constraint layer, workspace access model, agent profile ceilings, local-only/secrets/credentials policy, and tool/shell/network/MCP execution policy.

It follows S-A because S-A audited S-00 through S-04, found no blocking contradictions, and made V-00 ready after explicit instruction while keeping migration execution, implementation, product activation, external adoption, provider/API/network/MCP calls, authentication, publication, Git history changes, and substrate selection blocked.

Clarifications:

| V-00 is not | Meaning |
| --- | --- |
| Implementation | It does not create a registry database, service, code module, tool, package, SDK, scanner, runtime guard, hook, or automation. |
| A test suite | It does not define or run project tests, product tests, external tests, integration tests, builds, or runtime checks. |
| CI | It does not create CI workflows, checks, gates, badges, or automated policy enforcement. |
| Proof-level specialization | It reserves proof-level specialization for V-01 and does not finalize sufficiency thresholds. |
| Validation execution | It defines how validation should be recorded; it does not authorize unlisted validation commands or execution. |
| Governance approval | It does not approve promotion, product activation, external adoption, publication, Git history, or exceptions. |
| Migration or implementation authorization | It does not authorize migration execution, implementation, product activation, external adoption, provider calls, network calls, package managers, MCP, staging, commit, push, or publication. |

V-00 rule:

```text
Validation evaluates whether evidence supports a scoped claim, target, artifact,
behavior, or readiness posture. It records validity posture. It does not approve
authority, publish, promote, commit, migrate, activate products, adopt dependencies,
or execute implementation.
```

## 2. Validation Definition

Validation in AGENT PLATFORM is the evaluation of evidence, claims, artifacts, files, commands, outputs, behavior, constraints, source status, readiness, or lifecycle posture against declared criteria inside an explicit scope.

Validation can evaluate:

| Subject | Example validation question |
| --- | --- |
| Evidence | Does the evidence support the claim, and what are its limits? |
| Claim | Is the claim supported by current source authority and citations? |
| Artifact | Does the file or output match expected status, scope, source class, and policy? |
| File | Does the required path exist, and is it in the expected location? |
| Command | Did the explicitly scoped command run, and what did it prove or fail to prove? |
| Output | Is the output complete, sensitive, stale, generated, partial, or usable as evidence? |
| Behavior | Does observed behavior satisfy declared criteria, without implying broader permission? |
| Constraint | Does the proposed action obey security, access, context, Git, product, external, and governance constraints? |
| Source status | Is the source canonical, evidence, external, generated, product-scoped, migration evidence, or unknown? |
| Readiness | Is a target ready for the next architecture phase, or still blocked? |
| Lifecycle posture | Is validation current, stale, superseded, invalidated, blocked, deferred, or excepted? |

Validation boundaries:

| Boundary | Rule |
| --- | --- |
| Validation evaluates. | It checks evidence against scoped criteria and reports status, result, verdict, limitations, blockers, and residual risk. |
| Governance decides. | Governance accepts, rejects, defers, promotes, excepts, owns, and manages lifecycle. |
| Security constrains. | Security can block validation targets, methods, evidence retention, output handling, or publication. |
| Access scopes. | Active task, source class, sensitivity, role, and approval posture determine what may be inspected or validated. |
| Execution produces evidence. | Commands, tests, builds, tools, providers, products, external sources, and MCP outputs are evidence only when explicitly approved and scoped. |
| Git records. | Git status/diff/history can be evidence; Git does not create validation proof or semantic truth by itself. |
| Context exposes. | Context packs expose selected validation-relevant material; they do not grant permission or authority. |
| Agents propose. | Agents can prepare validation records or findings; they do not approve governance by default. |
| Generated output is evidence. | Generated summaries, logs, reports, tests, and artifacts require review and do not become source by generation. |
| Passing validation does not approve promotion. | Promotion still requires governance, security/access posture, ownership, scope, evidence, and blocker handling. |
| Failed validation does not delete evidence. | Failed, blocked, stale, skipped, partial, and inconclusive evidence remains auditable. |

## 3. Validation Registry Definition

The validation registry is the conceptual authority surface for tracking validation targets, checks, methods, evidence, results, verdicts, limitations, blockers, freshness, revalidation triggers, and relationships to governance decisions.

The registry answers:

| Registry question | Expected answer |
| --- | --- |
| What was validated? | Target, target class, path, source status, sensitivity, and scope. |
| Why was it validated? | Claim, question, criterion, readiness need, promotion precondition, or blocker. |
| How was it validated? | Method, check, command if any, non-command review, reviewer, and limitations. |
| What evidence was produced or inspected? | Evidence type, location/reference, freshness, sensitivity, and retention posture. |
| What was the result? | Result summary, verdict, residual risks, blockers, and revalidation triggers. |
| What can be inferred? | Only the scoped verdict and limitations, never approval or broad permission. |
| What governance does it support? | Related decision, ticket, promotion candidate, deferral, rejection, or exception reference. |

Clarifications:

| Clarification | Rule |
| --- | --- |
| The registry is conceptual in V-00. | V-00 defines architecture only. |
| No implementation is chosen. | No database, schema, graph, document format, table, JSON, YAML, code, or storage substrate is selected. |
| Future semantic representation is possible. | The future Cognitive Semantic System may consume, represent, project, or validate registry records after its own architecture and substrate decision. |
| The registry is not semantic truth by itself. | A validation record is evidence about a target; it does not make the target true or promoted. |
| The registry does not govern. | It supports governance with traceable validation evidence. Governance decides. |
| The registry does not bypass security. | Registry content must preserve sensitivity and must not store secrets or unsafe raw output. |

Registry invariant:

```text
A validation registry entry records scoped validation evidence and interpretation.
It does not approve the validated target, authorize action, or decide authority.
```

## 4. Validation Objects

Validation objects define what V-00 expects future records to distinguish. They are conceptual and not schemas.

| Object | Definition | Default authority posture | Required metadata | Governance relation | Security/access relation | Execution-policy relation |
| --- | --- | --- | --- | --- | --- | --- |
| Validation Target | Artifact, claim, file, source, output, action, readiness state, or lifecycle item being evaluated. | Target remains in its original authority state. | Target name, path if any, class, status, scope, sensitivity. | May be candidate evidence for decision or promotion. | Access to target must be scoped; sensitive targets may restrict evidence. | Executable targets cannot be run without S-04 approval. |
| Validation Claim | Statement being evaluated against evidence. | Claim until validated and governed. | Claim text, source, scope, cited evidence, owner. | Can support, block, or qualify governance. | Claims involving sensitive/local-only material require minimization. | Claims about execution require command/evidence provenance. |
| Validation Question | The question validation is intended to answer. | Question only, not result. | Question, target, criterion, expected answer type. | Helps governance understand relevance. | Must not request forbidden inspection. | Must not imply unapproved command execution. |
| Validation Criterion | Declared condition used to judge evidence. | Criterion controls validation scope only. | Criterion, source authority, acceptance threshold, exclusions. | Missing criterion blocks promotion-quality validation. | Criterion must respect security/access constraints. | Criterion cannot require unapproved commands. |
| Validation Method | Approach used to evaluate target. | Method is evidence procedure, not proof by itself. | Method name, command/review type, approval need, limitations. | Method strength informs governance. | Method may be blocked by sensitivity or access. | Execution method must follow S-04. |
| Validation Check | Concrete check performed or planned. | Check output is evidence. | Check name, target, method, expected result, actual result. | Check can support or block decision. | Check must avoid secret/local-only leakage. | Command checks are scoped execution. |
| Validation Command | Exact command used for validation. | Command output is evidence only. | Full command, working directory, risk level, expected output, result, side effects. | Does not approve governance, Git, promotion, or next action. | Must avoid secrets/local-only unless approved. | Governed by S-04 validation command policy. |
| Validation Review | Non-command evaluation by reading, comparing, checking citations, or assessing coherence. | Review notes are evidence. | Reviewer, files inspected, method, findings, limitations. | Can support/block governance. | Must cite inputs and preserve sensitivity. | No execution unless separately approved. |
| Validation Evidence | Source material, output, note, metadata, command result, review finding, or reference used to evaluate target. | Evidence only. | Evidence type, location/reference, source status, sensitivity, freshness, retention. | Evidence can support decisions but does not decide. | Must not expose secrets; local-only evidence needs handling. | Execution-derived evidence needs command metadata. |
| Validation Result | Factual outcome of a check or review. | Result is evidence summary. | Result text, pass/fail/blocked/partial/inconclusive details, scope. | May feed verdict or governance. | Sensitive results must be summarized safely. | Command results require output handling. |
| Validation Verdict | Scoped interpretation of result against criterion. | Verdict is not approval. | Verdict type, scope, limitations, residual risk, blocker if any. | Can support, block, defer, or require governance decision. | Security/access blockers override favorable verdicts. | Execution success does not expand permission. |
| Validation Limitation | Known constraint on what validation did or did not prove. | Limitation narrows validity. | Limitation, affected scope, missing evidence, uncertainty. | Governance must consider before promotion. | May involve access restrictions or secret handling. | May result from unapproved execution. |
| Validation Residual Risk | Risk remaining after validation. | Risk remains open until governed or mitigated. | Risk, severity, mitigation, owner, revalidation trigger. | May block or qualify decision. | Security risks may block action. | Execution risks may require S-04 approval. |
| Validation Blocker | Missing condition that prevents validation or use of validation for promotion. | Blocker stops or defers validation/decision. | Blocker category, target, required next action, owner. | Usually blocks promotion until resolved or excepted. | Security/access blockers must be escalated. | Missing execution approval blocks command validation. |
| Validation Exception | Governed acceptance of bounded validation gap or deviation. | Exception is governance artifact, not validation proof. | Scope, owner, risk acceptance, expiry/review point, mitigation. | Requires governance approval. | Cannot expose secrets or bypass safety casually. | Cannot authorize adjacent execution unless exact. |
| Validation Reference | Link/reference to evidence, command output, review note, decision, or prior validation. | Reference only, not evidence if target unavailable. | Reference type, path/id, source status, freshness. | Helps trace governance support. | Must not point to unsafe secret-bearing content without controls. | Execution reference needs command metadata. |
| Revalidation Trigger | Event requiring validation to be reviewed, rerun, or marked stale. | Trigger changes freshness state. | Trigger type, affected target, date/source, required action. | Can block current promotion until revalidated. | Security/policy changes can invalidate evidence. | Command/environment changes can require rerun. |
| Validation Registry Entry | Conceptual record combining target, method, evidence, result, verdict, limitations, blockers, and relationships. | Entry is validation evidence/control record. | See Section 10 fields. | Supports governance but does not govern. | Must preserve sensitivity and access posture. | Must record command risk if any. |
| Validation Audit Entry | Review of registry completeness, consistency, freshness, and policy compliance. | Audit evidence only. | Audit scope, entries reviewed, findings, gaps, residual risk. | Can support governance about validation sufficiency. | Must not expose sensitive registry data. | Audit commands follow S-04 if used. |

## 5. Validation Target Classes

Validation target classes define what can be evaluated and what cannot be inferred.

| Target class | What can be validated | What cannot be inferred | Default validation posture | Required evidence | Common blockers |
| --- | --- | --- | --- | --- | --- |
| Workspace architecture document | Status, scope, citations, coherence with W-series/S-series, naming, stop rules. | That implementation or migration is approved. | Reviewable at architecture stage. | Source docs, cited inputs, path checks, coherence review. | Missing citations, contradiction, stale policy. |
| Security/access policy document | Alignment with S-series, risk controls, sensitivity, execution boundaries, Git/local-only posture. | That enforcement exists. | Reviewable at architecture stage. | S-series docs, S-A, bounded checks. | Security conflict, missing access boundary, secret leakage. |
| Validation policy document | Validation definitions, status/verdict/evidence/method coverage, governance/security boundaries. | That a registry is implemented. | Reviewable at architecture stage. | V-series docs, S/W inputs, matrix review. | Missing criterion, proof-level overreach, schema creep. |
| Documentation projection | Source authority citation, projection status, freshness, no authority drift. | That projection is source authority. | Reviewable, but not source proof. | Source architecture, docs metadata, citation review. | Missing source, stale projection, local-only leakage. |
| Research evidence | Source, method, uncertainty, freshness, evidence quality. | That research is accepted decision. | Evidence review only. | Research paths, sources, uncertainty notes. | Missing source, stale evidence, overclaim. |
| Previous knowledge restatement | Fidelity to source concept, current vocabulary, citation, scope, no old authority import. | That old documents became current authority. | Requires migration-style review. | W-02 state, original path, restated target. | Missing classification, wholesale copy, naming conflict. |
| External source metadata | Identity, provenance, license posture, risk, allowed/blocked use, review limits. | Dependency approval, execution approval, or source reuse approval. | Non-execution review only by default. | W-03/W-13, metadata review notes. | Missing license, missing provenance, execution risk. |
| Product charter | Product purpose, owner, scope, activation state, root boundary, Git posture. | Product activation by itself. | Product policy review only. | W-12, charter draft, owner/scope evidence. | Missing owner, missing security, missing validation baseline. |
| Product validation baseline | Declared checks, scope, product behavior criteria, limitations, evidence retention. | Root platform validation. | Placeholder until V-04. | Product scope, validation plan, security posture. | Product inactive, missing dependencies, missing execution approval. |
| Migration batch | Source classification, target status, citations, local-only posture, diff, audit trail. | Migration approval by validation alone. | Placeholder until V-03. | W-08 controls, source/target mapping, status/diff. | Missing scope, missing source classification, wholesale migration. |
| Implementation plan | Alignment with architecture, security, validation needs, dependencies, blocked work. | Code implementation approval. | Planning review only. | Architecture docs, S/V constraints, risk register. | Missing validation plan, dependency review, security posture. |
| Code artifact | Static/source review, tests if approved, architecture alignment, security posture. | Runtime safety or deployment approval. | Future only; not V-00 execution. | Source path, criteria, command approvals if any. | Implementation not ready, tests unapproved, secrets. |
| Script/tool/test artifact | Purpose, source review, trust state, side effects, command approval readiness. | Permission to run. | Future review; execution blocked by default. | S-04 trust policy, source review, exact command proposal. | Unreviewed side effects, package/network/auth risk. |
| Package/SDK artifact | Metadata, release posture, dependency review, compatibility, publication readiness. | Build/install/publish approval. | Future only. | Package/SDK plan, dependency/security review. | Missing dependency approval, registry risk, release policy absent. |
| Dataset | Metadata, provenance, license, sensitivity, retention, intended use. | Data use or publication approval. | Metadata review only by default. | Dataset metadata, source, sensitivity. | Privacy/license unknown, local-only, unknown sensitivity. |
| Model | Metadata, provenance, license, safety, privacy, storage, use scope. | Model execution/use approval. | Metadata review only by default. | Model metadata, source, risk review. | License/safety unknown, local-only, large file. |
| Generated artifact | Generator/source/command provenance, sensitivity, freshness, review status. | Source truth. | Generated-sensitive until reviewed. | Generator info, inputs, command if any, review notes. | Sensitive output, stale output, missing provenance. |
| Runtime log | Command/process/source, sensitivity, secret risk, relevance. | Safe publication or authority. | Local-only/generated-sensitive. | Safe excerpts or metadata, output handling. | Secrets/credentials, local-only data, unclear process. |
| Command output | Exact command, working directory, result, limitations, side effects. | Approval for follow-up command. | Evidence only. | Command metadata, output summary, sensitivity review. | Unlisted command, sensitive output, unclear side effects. |
| Git diff/status | Worktree/index state, intended file visibility, local-only/staged risk. | Semantic truth, validation sufficiency, commit approval. | Read-only validation evidence. | `git status`, diff summary when scoped. | Local-only staged, secrets staged, broad staging. |
| Context pack | Source selection, status labels, exclusions, freshness, stop rule. | Source authority or permission. | Projection review. | Pack content/metadata, source refs, W-05 rules. | Stale context, local-only inclusion, missing status. |
| Governance decision candidate | Preconditions, evidence, validation posture, owner, scope, blockers. | Approval before governance acts. | Governance-readiness review. | W-11 preconditions, evidence, validation status. | Missing owner, missing validation, security blocker. |
| Publication candidate | Sensitivity, citations, license/product/external/security posture. | Publication approval. | Review only; publication blocked. | Candidate content, source refs, security/license review. | Sensitive data, license risk, product claim, external reuse. |
| Cognitive Semantic System candidate record | Source status, lifecycle, provenance, validation relation, substrate neutrality. | Final substrate or semantic truth. | Future conceptual review only. | Candidate record concept, source refs, governance posture. | Substrate assumed, source/projection confusion, access model missing. |

## 6. Validation Status Model

Validation statuses describe lifecycle and usability of validation evidence.

| Status | Meaning | Allowed use | Authority posture | Governance implication | Revalidation implication |
| --- | --- | --- | --- | --- | --- |
| `not_validated` | No validation exists for the scoped target/claim. | Mark gap or blocker. | No validation support. | Promotion normally blocked unless validation not required or exception exists. | Validate before current use. |
| `validation_not_required` | Governance or policy says validation is not applicable for the scoped target. | Record rationale and scope. | Scoped non-requirement only. | Governance may proceed if other preconditions satisfied. | Revisit if scope/criteria changes. |
| `validation_planned` | Validation method/criteria are proposed but not performed. | Planning evidence. | No result yet. | Cannot support promotion except as plan. | Perform or defer. |
| `validation_scoped` | Target, criteria, method, and allowed evidence are defined. | Ready to validate. | Scope control only. | Supports readiness to run/review. | Run/review when allowed. |
| `validation_running` | Validation is in progress. | Temporary operational state. | No final verdict. | Governance should wait. | Complete or mark blocked/failed/skipped. |
| `validation_passed` | Target satisfied criteria for declared scope. | Support proposal or decision with limitations. | Evidence, not approval. | Can support governance; does not approve. | Revalidate on trigger. |
| `validation_failed` | Target did not satisfy criteria. | Block, fix within scope, reject, or defer. | Failure evidence. | Blocks promotion unless exception or narrowed scope. | Revalidate after change. |
| `validation_blocked` | Validation could not proceed due to missing scope, evidence, access, security, owner, or approval. | Blocker record. | No verdict on target. | Blocks promotion-quality use. | Resolve blocker or record exception. |
| `validation_skipped` | Validation was intentionally not run. | Must be visible with reason. | No validation support. | May block or require governance acceptance. | Run later if needed. |
| `validation_partial` | Some checks passed or completed, but coverage is incomplete. | Scoped support with limitations. | Partial evidence only. | May support limited proposal; usually blocks promotion. | Complete missing checks. |
| `validation_inconclusive` | Evidence does not support pass/fail. | Record uncertainty. | No definitive support. | Usually defer or require more evidence. | Revalidate with better criteria/evidence. |
| `validation_stale` | Validation may no longer reflect current target or criteria. | Historical evidence. | Not current proof. | Cannot support current promotion without review. | Revalidate or mark superseded. |
| `validation_invalidated` | Later change or incident makes validation unusable for current claim. | Historical warning. | Invalid for current use. | Blocks promotion using that evidence. | New validation required. |
| `validation_superseded` | Newer validation replaces prior validation. | Historical trace. | Replaced evidence. | Governance should cite newer record. | No rerun unless target changes again. |
| `validation_deferred` | Validation postponed due to missing dependency or timing. | Planning/blocker record. | No result. | Governance may defer decision. | Resume when dependency resolves. |
| `validation_exception` | Governance accepts a bounded validation gap or deviation. | Exception trace only. | Not proof. | Requires owner, risk, mitigation, expiry/review point. | Review at expiry or trigger. |

## 7. Validation Verdict Model

A validation verdict is the scoped interpretation of validation evidence against declared criteria.

Verdict types:

| Verdict | Meaning | Typical implication |
| --- | --- | --- |
| `pass_for_scope` | Criteria satisfied for declared scope. | Can support governance with limitations. |
| `fail_for_scope` | Criteria not satisfied for declared scope. | Blocks or requires fix/deferral/rejection. |
| `blocked_by_security` | Security policy blocks validation, evidence handling, or action. | Stop and escalate. |
| `blocked_by_access` | Active scope/access model does not permit target, method, or evidence. | Stop and request scope or adjust target. |
| `blocked_by_missing_evidence` | Required evidence is absent. | Gather evidence or defer. |
| `blocked_by_missing_owner` | No accountable owner exists. | Assign owner before promotion-quality validation. |
| `blocked_by_missing_criteria` | Criteria are undefined. | Define criteria before validation. |
| `blocked_by_missing_dependency_review` | Dependency risk is unresolved. | Perform dependency review before adoption/build/test. |
| `blocked_by_missing_product_scope` | Product boundary/owner/state is missing. | Product validation cannot support activation. |
| `blocked_by_missing_external_review` | External provenance/license/security review missing. | External use/adoption remains blocked. |
| `blocked_by_missing_execution_approval` | Required command/test/build/runtime validation lacks exact approval. | Do not execute; request approval or use non-command review. |
| `partial_pass` | Some criteria satisfied; gaps remain. | Limited support only; record gaps. |
| `inconclusive` | Evidence cannot support pass or fail. | More evidence or different method required. |
| `stale` | Evidence may be outdated. | Historical only until revalidated. |
| `not_applicable` | Criterion does not apply to target/scope. | Record rationale; no proof implied. |
| `deferred` | Verdict postponed. | Decision should wait or record deferral. |
| `requires_governance_decision` | Evidence exists but a decision is outside validation authority. | Governance must decide. |

Verdict rules:

| Rule | Meaning |
| --- | --- |
| A verdict is not approval. | It can support or block governance but cannot approve promotion, commit, push, publication, migration, product activation, external adoption, or substrate decisions. |
| A verdict must be scoped. | A product verdict is not root proof; an architecture verdict is not implementation proof. |
| A verdict must identify limitations. | Missing evidence, stale evidence, partial coverage, unrun commands, and security limits must remain visible. |
| A favorable verdict does not expand access. | Passing validation does not authorize adjacent reads, writes, commands, or Git actions. |

## 8. Validation Evidence Model

Validation evidence is the material used to support or refute a validation verdict.

| Evidence type | Safe retention posture | Sensitivity posture | Source status | Freshness requirement | Citation requirement | Limitations |
| --- | --- | --- | --- | --- | --- | --- |
| Command output | Retain summary and command metadata; avoid raw dumps if sensitive. | Generated-sensitive until reviewed. | Execution evidence. | Rerun/review on command/env/target change. | Cite command, working directory, date, scope. | Can be partial, environment-specific, or sensitive. |
| Git status/diff output | Retain summary or exact bounded output if safe. | May reveal paths; review local-only/secret risk. | Git evidence, not truth. | Fresh to branch/worktree. | Cite command and scope. | Does not approve Git history. |
| Path existence checks | Retain boolean/path summary. | Usually low, but path can be sensitive. | Metadata evidence. | Fresh to filesystem state. | Cite checked path and command. | Existence does not prove content correctness. |
| File metadata | Retain path, size/date if useful. | Usually low, can reveal local details. | Metadata evidence. | Fresh to file state. | Cite file path and metadata command. | Metadata does not prove semantics. |
| Content review notes | Retain notes, citations, and limits. | Depends on content; avoid sensitive quotes. | Review evidence. | Fresh to file version. | Cite inspected paths/sections. | Human/agent review can miss issues. |
| Citation review | Retain missing/valid citation findings. | Usually internal. | Provenance evidence. | Fresh to referenced files. | Cite source/target paths. | Citation existence does not prove claim truth. |
| Matrix alignment review | Retain table findings and conflicts. | Internal policy evidence. | Architecture review evidence. | Fresh to source matrices. | Cite docs compared. | Depends on reviewer interpretation. |
| Policy coherence review | Retain contradiction/tension register. | Internal. | Architecture review evidence. | Fresh to policy set. | Cite policy docs. | Coherence is not enforcement. |
| Security/access review | Retain safe findings and blockers. | Potentially sensitive. | Security evidence. | Fresh to S-series/security posture. | Cite security docs and safe paths. | Must not expose secrets. |
| Non-execution external source review | Retain metadata and risk notes only. | External-restricted. | External evidence. | Fresh to source version. | Cite W-03/W-13 and reviewed paths if scoped. | Does not approve execution/adoption. |
| Product scope review | Retain product-scope findings and blockers. | Product-restricted/local-only. | Product evidence. | Fresh to product state. | Cite product policy and scoped material. | Does not activate product. |
| Migration source/target review | Retain mapping, status, citations, blockers. | May include local-only references. | Migration evidence. | Fresh to source/target files. | Cite W-02/W-08/source paths. | Does not execute migration. |
| Generated artifact review | Retain metadata, safe excerpts, provenance. | Generated-sensitive/local-only by default. | Generated evidence. | Fresh to generation inputs. | Cite generator/input/method. | Generated is not source. |
| Dataset/model metadata review | Retain metadata, provenance, risk. | Local-only/sensitive possible. | Data/model evidence. | Fresh to artifact version. | Cite metadata/source. | Does not approve use/execution. |
| Test output | Retain command, scope, result summary, logs if safe. | Generated-sensitive until reviewed. | Test evidence. | Fresh to code/env/tests. | Cite command and target. | Tests are not governance. |
| Build output | Retain summary and artifact metadata if safe. | Generated-sensitive. | Build evidence. | Fresh to source/deps/env. | Cite command and outputs. | Build success does not approve release. |
| Runtime output | Retain safe summary and environment metadata. | High sensitivity risk. | Runtime evidence. | Fresh to runtime/env/state. | Cite command/process and scope. | Runtime behavior may be environment-specific. |
| Manual review | Retain reviewer, inputs, findings, limits. | Depends on reviewed material. | Review evidence. | Fresh to input versions. | Cite files and review date. | Subjective; may require corroboration. |
| Human approval reference | Retain reference to approval, not secret/sensitive content. | Governance-sensitive. | Governance evidence. | Fresh to decision scope. | Cite decision/approval source. | Approval is not validation by itself. |
| Governance decision reference | Retain decision reference and scope. | Governance-sensitive. | Decision evidence. | Fresh to lifecycle. | Cite decision path/id. | Decision can be superseded. |

## 9. Validation Method Taxonomy

Validation methods describe how evidence is produced or reviewed. V-00 classifies methods but does not execute unapproved methods.

| Method | Command execution needed? | Approval needed? | Architecture-stage use? | Future phase fit |
| --- | --- | --- | --- | --- |
| Path existence validation | Yes, low-risk metadata command. | Active ticket scope. | Yes. | V-00/V-02. |
| Git worktree validation | Yes, read-only Git command. | Active ticket scope. | Yes. | V-00/V-02. |
| Git diff validation | Yes, read-only Git command when scoped. | Active ticket scope; Git mutation still human-gated. | Sometimes, if explicit. | V-02/V-03. |
| Citation validation | Usually no; may use bounded search/path checks. | Scope and content sensitivity. | Yes. | V-01/V-02/V-03. |
| Status/scope metadata validation | Usually no; may use file reads/path checks. | Scope. | Yes. | V-00/V-02. |
| Naming validation | Optional bounded search. | Scope; no sensitive search. | Yes. | V-00/V-02. |
| Matrix alignment validation | No command required; review method. | Scope. | Yes. | V-00/V-02. |
| Policy coherence validation | No command required; review method. | Scope. | Yes. | V-00/V-02. |
| Local-only/Git ignore validation | Yes, `git check-ignore` if scoped. | Active ticket scope. | Yes. | V-00/V-02. |
| Secret/credential posture validation | Usually metadata/non-exposure review only. | Security scope; never value inspection. | Yes as policy review. | V-02. |
| Execution-policy validation | No command needed unless checking allowed command metadata. | Security/execution scope. | Yes as policy review. | V-02/V-05. |
| External-source non-execution review | No execution; content/metadata review only when scoped. | External review scope. | Yes at policy level. | V-05. |
| Product-boundary review | No execution by default. | Product scope. | Yes at policy level. | V-04. |
| Migration-readiness review | No execution by default; may inspect scoped diffs/status later. | Migration scope. | Placeholder only in V-00. | V-03. |
| Documentation projection review | Usually no command; citation/status/content review. | Docs scope. | Yes. | V-02. |
| Command-result validation | Yes. | Exact command approval and S-04 posture. | Only for listed low-risk commands in V-00. | V-02/V-03/V-04/V-05. |
| Test validation | Yes, runs tests. | Explicit test command approval. | No for V-00 except not run. | V-02/V-04/future implementation. |
| Build validation | Yes, build/package execution. | Explicit build/dependency approval. | No. | Future V-02/V-04/release phases. |
| Runtime validation | Yes, runtime/server/process execution. | Explicit runtime/security approval. | No. | Future implementation/product phases. |
| Data/model provenance review | Usually metadata review; no model/data execution. | Data/model scope. | Yes as placeholder. | V-02/V-04/future data/model policy. |
| Generated-artifact review | Review metadata/content safely; no generation unless approved. | Artifact/output scope. | Yes if artifact is scoped. | V-02/V-03/V-04. |
| Manual governance-readiness review | No command. | Governance scope. | Yes. | V-00/V-01/V-02. |

## 10. Validation Registry Entry Model

A validation registry entry is a conceptual record. V-00 does not create JSON, YAML, database schemas, tables, graph nodes, code, templates, or files beyond this architecture document.

Conceptual fields:

| Field | Meaning |
| --- | --- |
| `validation_id` | Stable identifier for the validation entry when a registry exists. |
| `title` | Human-readable validation entry title. |
| `status` | Validation status from Section 6. |
| `target` | Target name or description. |
| `target_path` | File/folder/path/ref if applicable. |
| `target_class` | Validation target class from Section 5 or future extension. |
| `claim_or_question` | Claim or validation question being evaluated. |
| `criterion` | Declared criterion used to judge the target. |
| `method` | Validation method from Section 9 or future extension. |
| `evidence_type` | Evidence type from Section 8. |
| `evidence_location` | Path, reference, summary location, or decision reference. |
| `command_if_any` | Exact command when validation used command execution. |
| `working_directory_if_any` | Working directory for command validation. |
| `execution_risk_level_if_any` | S-04 risk level or equivalent if command/execution occurred. |
| `result` | Factual result summary. |
| `verdict` | Verdict from Section 7. |
| `limitations` | What was not checked or what cannot be inferred. |
| `residual_risk` | Remaining risks after validation. |
| `blocker` | Blocking condition if any. |
| `source_status` | Canonical, evidence, research, external, product-scoped, generated, migration evidence, historical, unknown, or equivalent. |
| `sensitivity` | Public, internal, local-only, sensitive, restricted, secret, credential, external-restricted, product-restricted, generated-sensitive, unknown, or equivalent. |
| `security_access_posture` | Security/access constraints, approvals, or blockers. |
| `governance_posture` | Proposed, under review, approved, rejected, deferred, exception, not applicable, or equivalent. |
| `owner` | Accountable owner or placeholder. |
| `reviewer` | Human/role/agent contributor who performed or recorded validation. |
| `date` | Validation date or record date. |
| `freshness` | Current, stale, superseded, invalidated, unknown, or date-bound. |
| `revalidation_trigger` | Trigger that requires review/rerun. |
| `supersedes` | Prior validation record replaced by this one. |
| `superseded_by` | Later validation record replacing this one. |
| `related_decision` | Governance, promotion, exception, or decision reference. |
| `related_ticket` | Active or historical ticket/task reference. |
| `stop_rule` | Point where validation must stop and not continue to next work. |

Entry model rule:

```text
The registry-entry model is conceptual only. Future implementation may choose a
representation, but V-00 does not choose storage, schema, serialization, graph,
database, code, or runtime behavior.
```

## 11. Validation Command Policy

Validation commands are scoped execution under S-04.

Command rules:

| Rule | Requirement |
| --- | --- |
| Commands are execution. | Even low-risk validation commands inspect state and must be scoped. |
| Low-risk commands must still be declared. | Command, path, purpose, and expected output must be known. |
| Command output is evidence. | It does not approve governance, Git, publication, promotion, product activation, or next actions. |
| Command output may be sensitive. | Stop or summarize safely if secrets, credentials, local-only content, restricted paths, or generated-sensitive output appears. |
| Commands must be bounded by path. | Avoid broad workspace traversal and forbidden/local-only surfaces. |
| Commands must be reported. | Final output must list commands run and relevant results. |
| Commands must not imply approval. | Passing commands do not authorize staging, commit, push, publication, product activation, migration, external adoption, or implementation. |
| Failing commands must not be hidden. | Failed, partial, blocked, skipped, or inconclusive results must be visible. |

Allowed in V-00 only if listed by this ticket:

| Command family | V-00 allowed use |
| --- | --- |
| `git status --short` | Worktree visibility and no-staging reporting. |
| `Test-Path` | Required path existence validation. |
| `Get-Item` | Target file metadata validation. |
| `git check-ignore` | Representative local-only/secret/credential ignore posture checks. |
| Bounded `Select-String` or `findstr` naming checks | Search only allowed validation docs for prohibited legacy naming if needed. |

Explicitly not allowed in V-00:

| Not allowed | Reason |
| --- | --- |
| Tests | V-00 is architecture only and not a test suite. |
| Package managers/builds | Dependency/build execution is blocked. |
| Product code | Products are inactive/local-only. |
| External code | External sources are evidence-only. |
| Network/API/provider calls | Network/provider/API execution is blocked. |
| Authentication | Credential use is blocked. |
| MCP activation | MCP execution is blocked. |

## 12. Non-command Validation Policy

Non-command validation is evidence-producing review without running commands, tests, builds, products, external sources, providers, networks, package managers, or MCP.

Non-command validation methods:

| Method | What it checks | Required reporting |
| --- | --- | --- |
| Document consistency review | Claims, sections, status, scope, and boundaries across docs. | Files inspected, findings, contradictions, limitations. |
| Source-status review | Whether sources are canonical, evidence, external, product-scoped, generated, historical, or unknown. | Source classes, uncertainty, blockers. |
| Citation review | Whether material claims cite required authority/evidence. | Missing/adequate citations and affected claims. |
| Matrix review | Whether matrices align across policies. | Rows/columns compared, conflicts, interpretation. |
| Policy coverage review | Whether required categories and blockers are addressed. | Coverage gaps and residual risks. |
| Contradiction review | Whether documents conflict or only create expected tensions. | Contradiction register and severity. |
| Local-only posture review | Whether ignored/local-only/security posture aligns with policy. | Local-only findings, no content exposure. |
| External source posture review | Whether sources remain evidence-only and blocked for execution/adoption. | Review limits and blocked uses. |
| Product boundary review | Whether product scope/root boundary is preserved. | Product-scope findings and blockers. |
| Governance-readiness review | Whether owner, scope, evidence, validation, security, and blockers are known. | Readiness verdict and missing preconditions. |
| Security-readiness review | Whether security/access constraints block or permit a validation path. | Security posture and escalation needs. |
| Validation-readiness review | Whether criteria, method, evidence, and retention are ready. | Planned status or blocker. |

Non-command validation rule:

```text
Manual or agent review is validation evidence only when it cites inputs, states
scope, reports limitations, preserves sensitivity, and avoids converting judgment
into governance approval.
```

## 13. Validation / Governance Boundary

Validation uses W-11 governance boundaries.

| Boundary | V-00 rule |
| --- | --- |
| Validation can support governance. | Passing scoped validation can be cited as evidence. |
| Validation can block governance. | Failed, stale, missing, partial, or blocked validation can block or qualify a decision. |
| Validation can qualify promotion. | Verdicts and limitations can narrow what governance may promote. |
| Validation cannot approve. | Approval requires human or delegated governance authority. |
| Validation cannot promote. | Promotion is a governance transition. |
| Validation cannot publish. | Publication requires governance/security/source/license/product review. |
| Validation cannot stage/commit/push. | Git history is human-gated. |
| Validation cannot decide product activation. | Product activation requires product/governance approvals. |
| Validation cannot decide external adoption. | External adoption requires provenance, license, security, validation, and governance. |
| Validation cannot decide final Cognitive Semantic System substrate. | Substrate selection requires explicit decision process and multi-candidate evaluation. |

Boundary statement:

```text
Validation supplies a validity posture. Governance decides what, if anything, to do
with that posture.
```

## 14. Validation / Security Boundary

Validation uses S-00 through S-A security/access boundaries.

| Security/access rule | Validation consequence |
| --- | --- |
| Security can block validation. | Unsafe validation target, method, evidence, output, command, or retention must stop or be narrowed. |
| Access can restrict validation targets. | Active ticket, role, source class, sensitivity, and approvals define what can be validated. |
| Secrets/credentials cannot be validated by exposure. | Do not print, quote, copy, hash, transform, test, or use secret/credential values. |
| Local-only material requires scoped handling. | Use safe metadata and explicit scope; do not include local-only content by default. |
| Execution validation requires S-04 posture. | Exact command, working directory, side effects, sensitivity, rollback/output handling, and approval are required when execution exceeds listed low-risk commands. |
| Validation evidence must preserve sensitivity labels. | Evidence must remain public/internal/local-only/sensitive/restricted/secret/credential/external/product/generated/unknown as applicable. |
| Validation outputs may be generated-sensitive. | Logs, stdout, reports, artifacts, test output, runtime output, and generated docs require review. |
| Registry must not store secrets. | Registry entries may store safe metadata and blockers, not values. |

Security boundary statement:

```text
Validation cannot make unsafe evidence safe. Security/access posture controls what
validation may inspect, run, retain, cite, or expose.
```

## 15. Validation / Context Boundary

Validation context uses W-05 and S-02/S-03.

| Context rule | Validation consequence |
| --- | --- |
| Context packs expose validation-relevant sources. | They can include source authority, target paths, criteria, evidence references, allowed commands, forbidden scope, and stop rules. |
| Context inclusion is not permission. | A validation pack does not grant read-beyond-scope, write, execute, Git, migration, publication, or promotion rights. |
| Validation evidence in context must preserve source status. | Canonical, evidence, external, product-scoped, generated, local-only, historical, secret, credential, and unknown labels must remain visible. |
| Stale validation evidence must be labeled. | Stale evidence can remain historical but cannot support current promotion without review. |
| Local-only validation evidence is excluded by default. | Use safe metadata unless explicit local-only scope exists. |
| Secret/credential validation is metadata-only. | Do not include values in validation packs or registry entries. |
| Validation packs are projections. | They select evidence for a task; they are not source authority or proof by themselves. |

## 16. Validation / Git Boundary

Git can provide validation evidence but does not validate authority by itself.

| Git surface | Validation boundary |
| --- | --- |
| Git status/diff | Can be validation evidence for worktree/index/file changes when scoped. |
| Git commit | Not validation, not governance, not semantic truth. |
| Git staging | Not validation and requires explicit human approval. |
| Git push | Publication, not validation, and requires explicit human approval. |
| Staged files | Validation may need to check staged files before a proposed commit. |
| Local-only or secret staged | Validation must stop and report safe blocker. |
| Exact file staging | Remains human-gated and cannot be approved by passing validation. |
| Registry references to Git state | Can cite Git status/diff/hash when useful, but Git state does not make records true. |

Git boundary statement:

```text
Git records state. Validation interprets evidence. Governance decides. These are
separate layers.
```

## 17. Documentation Validation Policy

Documentation validation checks whether a document is safe and usable inside its declared scope.

Documentation validation checks:

| Check | Requirement |
| --- | --- |
| Metadata header presence | Status, scope, authority, and related posture should be clear where expected. |
| Status/scope/authority clarity | Document must not rely on path, filename, readability, or recency for authority. |
| Citation adequacy | Material claims cite source authority or evidence; uncertainty is labeled. |
| Source-class clarity | Canonical, research, evidence, external, product-scoped, generated, migration evidence, or projection status is preserved. |
| Naming compliance | Use AGENT PLATFORM and Cognitive Semantic System terminology; avoid prohibited legacy authority naming. |
| Stop-rule compliance | Document must not start next tickets or authorize adjacent work. |
| No prohibited naming | Bounded naming check may be used where scoped. |
| No secret exposure | No secrets, credentials, values, partial values, hashes, or auth state. |
| No local-only leakage | Local-only material is excluded or referenced safely by metadata. |
| No ungoverned authority claim | Drafts/proposals/reviews do not become canonical without governance. |
| No product-root collapse | Product docs remain product-scoped unless root governance explicitly decides. |
| No external-source promotion by proximity | External sources remain evidence unless governed. |
| No substrate decision by wording | Graph and other representations remain candidate substrates only. |
| Link/path existence where applicable | Path checks can validate referenced current files when scoped. |

## 18. Architecture Validation Policy

Architecture validation checks coherence and boundaries of architecture artifacts.

Architecture validation checks:

| Check | Requirement |
| --- | --- |
| Coherence with W-series | Architecture should align with workspace identity, topology, context, migration, docs, agents, governance, product, external, and synthesis posture. |
| Coherence with S-series | Security/access, local-only, secret, execution, Git, product, and external constraints must be preserved. |
| Explicit scope | Architecture must state what it governs and what it does not. |
| Source citations | Material claims cite current authority and evidence. |
| Contradiction check | Hard contradictions and expected tensions are separated. |
| Matrix alignment | Action/surface/profile/status/evidence matrices should not conflict. |
| Boundaries preserved | Validation/governance/security/access/context/Git/product/external layers remain separate. |
| No implementation leakage | Architecture does not imply code, CI, tests, tools, packages, SDKs, runtime, or enforcement exists. |
| No governance automation claims | Conceptual governance is not implementation. |
| No validation-as-approval claims | Passing checks never approve promotion or Git. |
| No security override | Validation cannot override blocked security/access posture. |
| No premature substrate decision | Cognitive Semantic System representation remains undecided. |

## 19. Migration Validation Policy Placeholder

Migration validation must later be specialized in V-03. V-00 defines only the architectural placeholder.

At V-00, migration validation must check:

| Migration validation element | V-00 placeholder requirement |
| --- | --- |
| Source classification | Source has W-02/W-03/current policy class. |
| Source path | Original source path is identified. |
| Target path | Target path is explicit and responsibility-aligned. |
| Target status | Target declares status, scope, authority, and lifecycle posture. |
| Restatement fidelity | Current wording preserves concept without importing stale authority. |
| Citation coverage | Source classifications and original paths are cited. |
| Local-only posture | Local-only and ignored material is not exposed or committed by default. |
| Security/access posture | Sensitive, restricted, secret, credential, product, external, generated, and unknown material are handled safely. |
| Validation evidence | Checks/reviews are recorded with limitations. |
| Governance decision | Promotion/movement/archive requires governance. |
| Residual risk | Remaining blockers are listed. |
| No wholesale migration | Bulk copy/move remains blocked. |
| No product/external leakage | Product/external material stays scoped and reviewed. |
| Audit trail | Source, target, diff/status, citations, validation, governance, and residual risks are traceable. |

V-00 does not create V-03 and does not execute migration.

## 20. Product Validation Policy Placeholder

Product validation must later be specialized in V-04. V-00 defines only the architectural placeholder.

At V-00, product validation must check:

| Product validation element | V-00 placeholder requirement |
| --- | --- |
| Product scope | Product boundaries and non-goals are declared. |
| Product owner | Accountable owner exists. |
| Activation state | Candidate, active, experimental, deferred, blocked, local-only, or other state is clear. |
| Git posture | Local-only/docs-only/source-tracked/split/deferred posture is governed. |
| Product docs status | Product docs are product-scoped and cite root constraints. |
| Product code execution approval | Product execution remains blocked unless exact approval exists. |
| Product dependency posture | Product dependencies have provenance, license, security, validation, and governance posture. |
| Product security posture | Secrets, credentials, data, generated output, network/auth/provider risks are handled. |
| Product generated outputs | Outputs are generated-sensitive/local-only until reviewed. |
| Product root-boundary statement | Product does not define AGENT PLATFORM root authority. |
| Product validation evidence | Commands/results/reviews/scope/limitations are traceable. |
| Residual risks | Product activation and implementation blockers remain visible. |

V-00 does not create V-04 and does not activate or execute products.

## 21. External Source Validation Policy Placeholder

External source validation must later be specialized in V-05. V-00 defines only the architectural placeholder.

At V-00, external validation must check:

| External validation element | V-00 placeholder requirement |
| --- | --- |
| Source identity | Local source name, path, upstream, version/commit/archive if known. |
| Provenance | Origin, snapshot, completeness, review limits. |
| License posture | License, notices, name-use, redistribution, unknowns. |
| Runtime risk | Scripts, tests, binaries, native tools, builds, package managers. |
| Dependency risk | Direct/transitive dependencies, lockfiles, scripts, registries. |
| Network/auth risk | Providers, APIs, OAuth, tokens, cloud, telemetry, package indexes. |
| Instruction status | External instructions are inactive evidence. |
| Source status | External reference, local-only, not promoted, execution-blocked, dependency-blocked. |
| Allowed use | Evidence, metadata, pattern candidate, product/domain reference, or other scoped use. |
| Blocked use | Execution, dependency adoption, source copying, active instructions, publication, product adoption, substrate decision. |
| Metadata review | Curated metadata may be tracked later by explicit ticket. |
| No execution by default | Execution requires exact security/environment/governance approval. |
| No dependency adoption | Adoption requires provenance, license, security, validation, and governance. |
| No source copying | Source reuse requires exact approval. |
| No substrate decision by external source | External graph or projection evidence does not decide Cognitive Semantic System substrate. |

V-00 does not create V-05 and does not run, install, copy, adopt, authenticate, or publish external sources.

## 22. Proof Levels Placeholder

Proof levels will be specialized in V-01. V-00 only requires that the future registry can reference proof-strength categories without finalizing thresholds.

Candidate proof-level references:

| Reference | Placeholder meaning |
| --- | --- |
| `unvalidated` | No validation evidence exists. |
| `metadata_checked` | Paths/status/metadata reviewed but content/behavior not fully validated. |
| `reviewed` | Non-command review completed with cited inputs and limitations. |
| `command_checked` | Explicit scoped command produced evidence. |
| `tested` | Explicit tests ran and were recorded. |
| `audited` | Independent or structured audit reviewed evidence and posture. |
| `reproduced` | Result was independently rerun or reproduced under declared conditions. |
| `governed_reference` | Governance accepted the validation reference for a decision, without making validation approval. |

Proof-level placeholder rule:

```text
V-00 requires proof-level references to be scoped and limited, but V-01 must define
the real proof levels, sufficiency thresholds, evidence strength, applicability,
and limitations.
```

V-00 does not create V-01.

## 23. Validation Evidence Retention

Validation evidence retention must make verdicts auditable without leaking sensitive material.

Retention principles:

| Principle | Requirement |
| --- | --- |
| Retain enough evidence to audit the verdict. | Preserve target, method, criteria, evidence reference, result, verdict, limitations, reviewer, and date. |
| Avoid storing secrets. | Never store secret/credential values in validation records. |
| Avoid storing sensitive raw outputs. | Prefer summaries, safe metadata, or local-only references. |
| Prefer references over dumps. | Cite paths, command metadata, evidence refs, and safe summaries instead of copying large/raw content. |
| Preserve command metadata. | Retain command, working directory, scope, date, result, limitations, and output handling. |
| Mark stale evidence. | Stale does not disappear but cannot support current promotion without review. |
| Preserve failed evidence. | Failure must remain visible for audit and blocker handling. |
| Preserve blocked evidence. | Blocked validation explains missing preconditions. |
| Preserve skipped evidence. | Skipped validation must include reason and implication. |
| Preserve superseded evidence. | Supersession preserves history and points to replacement. |
| Retain generated artifacts as local-only unless reviewed. | Generated reports/logs/artifacts are not safe or commit-ready by default. |
| Do not publish validation evidence by default. | Publication requires security, source, license, product, external, and governance review. |

## 24. Freshness / Staleness / Revalidation

Validation freshness describes whether evidence still applies to the current target, criteria, environment, policy, and governance posture.

Revalidation triggers:

| Trigger | Revalidation implication |
| --- | --- |
| Source file changed | Recheck affected validations. |
| Dependency changed | Revalidate dependency/build/test/runtime claims. |
| Policy changed | Reassess affected criteria, verdicts, and blockers. |
| Security/access changed | Recheck evidence retention, commands, access, and exposure. |
| Validation criteria changed | Prior verdict may become stale or invalid. |
| Command changed | Prior command result does not apply to new command. |
| Environment changed | Test/build/runtime results may be stale. |
| Product state changed | Product validation baseline and activation posture need review. |
| External source version changed | External metadata/license/runtime/dependency review must refresh. |
| Generated output regenerated | Prior generated artifact review may be stale. |
| Git branch changed | Git status/diff evidence may not apply. |
| Incident occurred | Mark affected validation invalidated or blocked until reviewed. |
| Governance decision superseded | Related validation support must point to current decision. |
| Context pack stale | Validation context cannot support current conclusion without refresh. |
| Cognitive Semantic System substrate decision affects target | Reassess validation records that depend on representation, lifecycle, or access assumptions. |

Stale handling:

| Rule | Meaning |
| --- | --- |
| Stale validation does not disappear. | Keep it as historical evidence. |
| Stale validation cannot support current promotion without review. | Governance must require revalidation or explicit exception. |
| Stale validation can remain useful. | It can explain prior decisions, regressions, or supersession. |

## 25. Validation Blockers

Validation blockers prevent validation completion or prevent validation from supporting promotion.

| Blocker | Stop behavior | Required next action | Blocks promotion? | Blocks V-00 closure? |
| --- | --- | --- | --- | --- |
| Missing source | Stop target validation. | Locate source, cite absence, or defer. | Yes. | No, if recorded as future blocker. |
| Missing citation | Stop promotion-quality claim. | Add citation or mark claim as proposal. | Yes for authority claims. | No. |
| Missing owner | Stop promotion/exception path. | Assign owner or defer. | Yes. | No. |
| Missing scope | Stop validation use. | Define target scope. | Yes. | No. |
| Missing criteria | Stop verdict. | Define criteria. | Yes. | No. |
| Missing validation method | Stop validation plan. | Select method and approval posture. | Usually. | No. |
| Missing security/access posture | Stop unsafe validation. | Apply S-series posture. | Yes. | No. |
| Missing governance posture | Stop promotion interpretation. | Route to W-11 governance. | Yes for promotion. | No. |
| Missing product scope | Stop product validation. | Define product charter/scope/owner. | Yes for product activation. | No. |
| Missing external review | Stop external use/adoption validation. | Perform scoped non-execution review. | Yes for adoption/reuse. | No. |
| Missing dependency approval | Stop install/build/adoption validation. | Perform dependency review/governance. | Yes. | No. |
| Missing execution approval | Do not run command/test/build/runtime. | Request exact approval or use non-command review. | Yes for execution-dependent claim. | No. |
| Missing secret handling | Stop value handling. | Secure instruction/incident path. | Yes. | No. |
| Missing local-only decision | Stop publication/Git/context inclusion. | Decide scoped local-only handling. | Yes for publication/Git. | No. |
| Failed command | Stop or fix only if scoped. | Report failure, blocker, residual risk. | Usually yes. | No. |
| Failed policy check | Stop promotion/use. | Correct policy issue or defer. | Yes. | No. |
| Conflicting evidence | Stop definitive verdict. | Reconcile, scope, or mark inconclusive. | Usually yes. | No. |
| Stale evidence | Stop current proof use. | Revalidate or mark historical. | Yes for current promotion. | No. |
| Generated-sensitive output | Stop raw retention/publication. | Review/redact/summarize safely. | Yes until reviewed. | No. |
| Unknown sensitivity | Treat as sensitive and stop exposure. | Classify or escalate. | Yes until classified. | No. |

## 26. Validation Incident Handling

Validation incidents require safe reporting, no compounding action, and human/security/governance direction where needed.

| Incident | Stop behavior | Safe reporting | Required human action | Agents must not do |
| --- | --- | --- | --- | --- |
| Validation command exposes secret | Stop reading/copying output. | Report command category and safe path/category only. | Secure incident review and possible rotation. | Do not quote, hash, redact by repeating, test, or store value. |
| Validation command reads local-only material unexpectedly | Stop command sequence. | Report surface/category and that content was not further inspected. | Decide local-only handling/cleanup/revalidation. | Do not summarize content or continue broad inspection. |
| Validation output contains credentials | Stop output handling. | Report credential class without values. | Secure handling and incident review. | Do not print, test, copy, or use credentials. |
| Validation output generates sensitive artifact | Stop publication/Git/context use. | Report artifact path/category and sensitivity risk. | Review retention/redaction/deletion/promotion. | Do not paste artifact content. |
| Validation passes but scope was wrong | Mark validation invalidated or not applicable. | Report wrong scope and affected target. | Decide revalidation or exception. | Do not cite as current proof. |
| Validation command mutates files unexpectedly | Stop. | Report command and safe affected paths/categories. | Review diff/status and remediation. | Do not revert/delete without approval. |
| Validation command calls network unexpectedly | Stop. | Report command category/service class without payload. | Security/privacy/provider review. | Do not continue network calls or retry. |
| Validation command uses auth unexpectedly | Stop. | Report auth class/action without values. | Secure auth incident review. | Do not test/revoke by improvisation or continue. |
| Validation evidence stored in wrong place | Stop publication/Git use. | Report path/category and sensitivity if safe. | Decide relocation/redaction/retention. | Do not move/delete without approval. |
| Validation result cited as approval | Correct interpretation and stop promotion. | Report citation misuse. | Governance review if decision was affected. | Do not treat validation as governance. |
| Stale validation used as current proof | Mark stale/invalid for current purpose. | Report stale source and needed revalidation. | Decide rerun/review/exception. | Do not continue promotion based on stale proof. |

## 27. Registry Relationship To Future Cognitive Semantic System

Registry records may later be represented, indexed, projected, or consumed by the future Cognitive Semantic System.

V-00 constraints:

| Constraint | Requirement |
| --- | --- |
| No storage/substrate choice. | V-00 does not choose graph, relational, document, vector, event-sourced, hybrid, or any other final substrate. |
| Graph remains candidate only. | Graph-oriented representation may be evaluated later but is not selected. |
| Provenance must survive representation. | Source paths, statuses, criteria, evidence, limitations, and decisions must remain traceable independent of substrate. |
| Lifecycle must survive representation. | Current, stale, invalidated, superseded, deferred, blocked, and exception states must be represented distinctly. |
| Source status must survive representation. | Validation evidence, generated output, product-scoped material, external evidence, and accepted authority must not collapse. |
| Projections are not truth. | Generated views, reports, graphs, summaries, and context packs remain projections unless governed. |
| Validation evidence differs from accepted authority. | Future semantic records must distinguish evidence about a claim from a governed accepted claim. |

## 28. Validation Matrices

### Matrix A. Source Class Vs Validation Method

Values: `allowed_when_scoped`, `review_only`, `approval_required`, `future_only`, `blocked`, `local_only`, `not_applicable`.

| Source class | metadata review | content review | citation review | command validation | test validation | security review | governance readiness | publication readiness | default posture |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| architecture docs | allowed_when_scoped | allowed_when_scoped | allowed_when_scoped | allowed_when_scoped | not_applicable | review_only | review_only | approval_required | Reviewable architecture evidence. |
| security docs | allowed_when_scoped | allowed_when_scoped | allowed_when_scoped | allowed_when_scoped | not_applicable | review_only | review_only | approval_required | Security architecture evidence. |
| validation docs | allowed_when_scoped | allowed_when_scoped | allowed_when_scoped | allowed_when_scoped | not_applicable | review_only | review_only | approval_required | Validation architecture evidence. |
| research docs | allowed_when_scoped | allowed_when_scoped | allowed_when_scoped | approval_required | future_only | review_only | review_only | approval_required | Evidence only. |
| previous knowledge | allowed_when_scoped | approval_required | allowed_when_scoped | blocked | blocked | review_only | approval_required | blocked | Local-only migration evidence. |
| external metadata | allowed_when_scoped | allowed_when_scoped | allowed_when_scoped | approval_required | blocked | review_only | review_only | approval_required | External evidence only. |
| raw external sources | allowed_when_scoped | approval_required | allowed_when_scoped | blocked | blocked | approval_required | approval_required | blocked | Local-only, execution-blocked. |
| product docs | allowed_when_scoped | approval_required | allowed_when_scoped | approval_required | future_only | review_only | approval_required | approval_required | Product-scoped/local-only. |
| product code | allowed_when_scoped | approval_required | approval_required | blocked | blocked | approval_required | approval_required | blocked | Product execution blocked by default. |
| migration outputs | allowed_when_scoped | allowed_when_scoped | allowed_when_scoped | approval_required | not_applicable | review_only | approval_required | approval_required | Future V-03 specialization. |
| implementation plans | allowed_when_scoped | allowed_when_scoped | allowed_when_scoped | approval_required | future_only | review_only | approval_required | approval_required | Planning only. |
| scripts/tools/tests | allowed_when_scoped | approval_required | approval_required | approval_required | approval_required | approval_required | approval_required | approval_required | Execution not implied. |
| datasets | allowed_when_scoped | approval_required | approval_required | blocked | future_only | approval_required | approval_required | blocked | Local-only metadata first. |
| models | allowed_when_scoped | approval_required | approval_required | blocked | future_only | approval_required | approval_required | blocked | Local-only metadata first. |
| artifacts | allowed_when_scoped | approval_required | approval_required | blocked | not_applicable | review_only | approval_required | approval_required | Generated-sensitive/local-only. |
| generated outputs | allowed_when_scoped | approval_required | approval_required | blocked | not_applicable | review_only | approval_required | approval_required | Generated evidence only. |
| Git state | allowed_when_scoped | not_applicable | not_applicable | allowed_when_scoped | not_applicable | review_only | review_only | approval_required | Evidence, not approval. |
| context packs | allowed_when_scoped | allowed_when_scoped | allowed_when_scoped | approval_required | not_applicable | review_only | review_only | approval_required | Projection, not authority. |

### Matrix B. Validation Status Vs Governance Implication

| Validation status | can support proposal? | can support promotion? | blocks promotion? | requires revalidation? | requires governance? | notes |
| --- | --- | --- | --- | --- | --- | --- |
| not_validated | Limited as gap evidence | No | Usually yes | Yes | If promotion desired | Marks absence. |
| passed | Yes | Yes, if scoped and sufficient | No by itself | On trigger | Yes for promotion | Evidence, not approval. |
| failed | Yes as blocker evidence | No | Yes | After fix/change | For reject/defer/exception | Must be visible. |
| blocked | Yes as blocker evidence | No | Yes | After blocker resolved | Often | No target verdict. |
| skipped | Yes as limitation evidence | Usually no | Usually yes | If needed | May require acceptance | Must state reason. |
| partial | Yes | Limited only | Often | Yes for missing parts | Yes if used | Scope must be narrow. |
| inconclusive | Yes as uncertainty | No | Usually yes | Yes | Usually defer | Needs better evidence. |
| stale | Historical only | No current support | Yes for current promotion | Yes | If current use desired | Preserve trace. |
| invalidated | Historical warning | No | Yes | Yes | If decision affected | Do not reuse as proof. |
| not_applicable | Yes if rationale cited | Not proof; may remove criterion | No for non-applicable criterion | If scope changes | May need governance acceptance | Scope-specific. |

### Matrix C. Validation Evidence Vs Retention Posture

| Evidence | retain? | safe to commit? | local-only? | sensitive risk? | citation requirement | freshness requirement |
| --- | --- | --- | --- | --- | --- | --- |
| command output | Summary and metadata | Only if reviewed/safe | Often | High | Command, scope, date | Command/env/target changes. |
| Git status/diff | Summary or bounded output | Usually if safe | No, unless paths reveal local-only | Medium | Command and scope | Branch/worktree changes. |
| path checks | Boolean/path summary | Usually if path safe | No | Low-medium | Path and command | File state changes. |
| review notes | Yes | If non-sensitive | Depends | Medium | Inputs and reviewer | Source/policy changes. |
| generated artifacts | Metadata by default | No by default | Yes by default | High | Generator/input/method | Regeneration/input changes. |
| logs | Safe metadata only | No by default | Yes by default | High | Command/process/scope | Runtime/env changes. |
| test output | Summary and command metadata | Only if reviewed/safe | Often | Medium-high | Command, target, env | Code/test/env changes. |
| external review | Metadata/risk notes | Yes if curated and scoped | Raw sources remain local-only | Medium-high | W-03/W-13/source refs | Source/version changes. |
| product review | Product-scope notes | Usually no until product Git decision | Yes by default | Medium-high | W-12/product scope refs | Product state changes. |
| migration audit | Audit summary and refs | Yes if scoped/sanitized | Source may be local-only | Medium | Source/target/status refs | Source/target/policy changes. |
| manual review | Findings and limitations | If non-sensitive | Depends | Medium | Inputs/reviewer/date | Input/policy changes. |

## 29. Validation Invariants

| ID | Invariant |
| --- | --- |
| VAL-001 | Validation evaluates; governance decides. |
| VAL-002 | Validation evidence is not approval. |
| VAL-003 | Passing validation does not authorize commit, push, publication, migration, product activation, external adoption, or promotion. |
| VAL-004 | Failed validation must be visible. |
| VAL-005 | Blocked validation must be visible. |
| VAL-006 | Validation scope must be explicit. |
| VAL-007 | Validation criteria must be explicit. |
| VAL-008 | Validation commands are scoped execution. |
| VAL-009 | Validation output may be sensitive. |
| VAL-010 | Validation records must preserve limitations. |
| VAL-011 | Stale validation cannot support current promotion without review. |
| VAL-012 | Generated validation artifacts are not source by default. |
| VAL-013 | Product validation is product-scoped. |
| VAL-014 | External source validation does not approve dependency adoption. |
| VAL-015 | Migration validation does not execute migration. |
| VAL-016 | Cognitive substrate remains undecided. |

Invariant rule:

```text
If a validation invariant conflicts with convenience, follow the invariant and
record the blocker or limitation.
```

## 30. Validation Anti-patterns

| Anti-pattern | Failure mode | Correction |
| --- | --- | --- |
| tests passed so approved | Confuses validation with governance. | Route through governance. |
| validation output as governance | Lets evidence approve itself. | Keep verdict and approval separate. |
| Git commit as proof | Treats history as validation. | Use status/scope/evidence criteria. |
| command ran so safe | Treats execution success as security. | Review side effects and scope. |
| no output means success | Assumes silence is pass. | Require explicit criteria/result. |
| skipped validation hidden | Conceals gaps. | Record skipped reason and impact. |
| failed validation hidden | Conceals blockers. | Preserve failure evidence. |
| stale validation reused as current | Uses old evidence for current claim. | Revalidate or mark historical. |
| broad validation command | Overreads local-only/sensitive surfaces. | Bound commands by path and scope. |
| validation by generated summary | Treats generated projection as proof. | Cite source evidence and review. |
| validation by subagent agreement | Treats multiple agent opinions as proof. | Use scoped evidence and criteria. |
| validating secrets by printing them | Exposes credentials/secrets. | Use safe metadata only. |
| external README as validation | Treats external claim as internal proof. | Use W-13 review and governance. |
| product tests as root proof | Collapses product scope into root. | Keep product validation product-scoped. |
| migration audit as migration approval | Lets audit execute/approve movement. | Governance approves migration. |
| proof level without criteria | Labels evidence without standard. | Define criteria in V-01. |
| context inclusion as validation | Treats selected exposure as proof. | Validate against source authority. |
| graph projection as truth | Treats representation/projection as semantic authority. | Preserve substrate neutrality and governance. |
| green check without evidence | Hides method and limitations. | Record evidence, result, verdict, scope, and limits. |

## 31. Remaining Gaps

V-00 does not solve:

| Gap | Status after V-00 |
| --- | --- |
| Proof levels finalized | Not solved; V-01 target. |
| Validation evidence model specialization | Not solved; future V-series specialization. |
| Migration validation specialization | Not solved; V-03 target. |
| Product validation specialization | Not solved; V-04 target. |
| External source validation specialization | Not solved; V-05 target. |
| Validation audit | Not created; future V-A target. |
| Registry implementation | Not implemented. |
| Schemas | Not created. |
| CI | Not created. |
| Tests | Not created. |
| Scanners | Not created. |
| Command allowlist implementation | Not created. |
| Enforcement | Not implemented. |
| Context-pack validation generator | Not created. |
| Product validation baselines | Not created. |
| Dependency approval registry | Not created. |
| Cognitive Semantic System implementation | Not implemented; substrate remains undecided. |

Blocked until later phases:

| Later phase | Must specialize |
| --- | --- |
| V-01 | Proof levels, sufficiency thresholds, evidence strength, applicability, limitations. |
| V-02 | General validation evidence and command/review record specialization. |
| V-03 | Migration validation and audit trail specialization. |
| V-04 | Product validation baseline and product-readiness specialization. |
| V-05 | External source validation, dependency/adoption/execution review specialization. |
| V-A | Validation audit across V-series and active validation records. |

## 32. Readiness For V-01

V-01 target: Proof Levels.

Readiness assessment:

| Area | Readiness | Rationale |
| --- | --- | --- |
| Validation definition | Ready. | V-00 defines validation as scoped evaluation of evidence against criteria. |
| Registry object model | Ready. | V-00 defines targets, claims, questions, criteria, methods, evidence, results, verdicts, blockers, and entries. |
| Status/verdict model | Ready. | V-00 defines statuses and verdicts that proof levels must reference. |
| Evidence model | Ready enough. | V-00 classifies evidence types, retention, sensitivity, freshness, citations, and limitations. |
| Method taxonomy | Ready enough. | V-00 classifies command and non-command validation methods. |
| Governance/security boundaries | Ready. | V-00 preserves validation/governance/security/access/execution separation. |
| Proof-level finalization | Not done. | V-01 must define real sufficiency thresholds and evidence-strength semantics. |

V-01 should specialize:

| V-01 topic | Required coverage |
| --- | --- |
| Proof levels | Names, meanings, minimum evidence, scope, applicability, limitations. |
| Sufficiency thresholds | What level supports proposal, promotion, migration, product activation, external adoption, implementation, or publication. |
| Evidence strength | How command output, review, tests, audits, reproduction, and governance references compare. |
| Limits | What each proof level does not prove. |
| Cross-domain use | Architecture, migration, product, external source, implementation, security, and documentation claims. |

Do not create V-01 from V-00.

## 33. Final Verdict

| Question | Answer |
| --- | --- |
| What is the validation registry architecture? | A conceptual architecture for recording validation targets, criteria, methods, evidence, results, verdicts, limitations, blockers, freshness, retention, and governance/security relationships without implementing a registry. |
| What does it track? | Validation targets, claims/questions, criteria, methods, checks, commands, reviews, evidence, results, verdicts, limitations, residual risks, blockers, exceptions, references, revalidation triggers, registry entries, and audit entries. |
| What is validation evidence? | Command output, Git state, path checks, metadata, review notes, citations, matrices, policy reviews, security/access reviews, external/product/migration reviews, generated artifact reviews, test/build/runtime output when approved, manual review, and governance/approval references. |
| What is a validation verdict? | A scoped interpretation of validation evidence against criteria, such as pass, fail, blocked, partial, inconclusive, stale, deferred, not applicable, or requires governance. It is not approval. |
| What does validation not approve? | Promotion, publication, staging, commit, push, migration execution, product activation, external dependency adoption, provider/API/network/MCP calls, authentication, implementation, or final Cognitive Semantic System substrate selection. |
| What remains blocked? | V-01 through V-05/V-A, registry implementation, schemas, CI, tests, scanners, enforcement, migration execution, product activation, external adoption, implementation, package managers, provider/network/auth/MCP activity, staging, commit, push, publication, and substrate decision. |
| Is V-01 ready after explicit instruction? | Yes. V-00 defines enough validation architecture for V-01 proof-level specialization. |
| What should V-01 consume? | V-00, S-00 through S-04, S-A, W-A, W-10, W-11, W-05, W-08, W-09, W-12, W-13, GIT-01, `.gitignore`, and current active-task constraints. |

V-00 validation record:

| Validation category | Status |
| --- | --- |
| Git worktree check | Completed. `git status --short` reported `?? 0_architecture/validation/`, consistent with the newly created V-00 folder/file and no staging, commit, or push. |
| Required input existence checks | Passed. Individual scoped `Test-Path` checks returned `True` for `.gitignore`, `README.md`, required S-series files, required W-series files, GIT-01, and the V-00 target file. |
| Target file metadata check | Passed. Scoped `Get-Item 0_architecture/validation/agent_platform_validation_registry_architecture.md` returned file metadata successfully. |
| Optional `.gitignore` representative checks | Passed. Individual `git check-ignore` checks returned the expected ignored paths for `previusknowledge/`, `2_products/`, `4_external/sources/`, `7_datasets/`, `8_models/`, `9_artifacts/`, `.env`, `.env.local`, `secrets/test.txt`, and `credentials/test.txt`. |
| Optional prohibited legacy naming check | Passed. Bounded `Select-String` over `0_architecture/validation/*.md` for the prohibited legacy authority phrases returned no matches. |
| Validation command anomaly | An initial aggregated PowerShell path-check command failed due command-line quoting; it produced no validation verdict and was superseded by the individual `Test-Path` checks above. |

Final V-00 statement:

```text
V-00 defines the AGENT PLATFORM validation registry architecture as a conceptual
recording and interpretation layer for validation evidence. It preserves the core
boundary: validation evaluates, governance decides, security constrains, access
scopes, execution produces evidence, Git records, context exposes, agents propose,
and generated output remains evidence until reviewed and governed.
```

Stop rule:

```text
After completing V-00, STOP. Do not start V-01, V-02, V-03, V-04, V-05, V-A,
implementation, migration, product activation, external adoption, staging, commit,
push, publication, provider/API/network/MCP activity, authentication, or any later
ticket unless explicitly instructed.
```
