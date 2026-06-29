# AGENT PLATFORM Product Validation Model

Status: Canonical V-04 product validation model  
Date: 2026-06-29  
Scope: Product validation architecture for AGENT PLATFORM.  
Authority: Architecture only. This document validates product readiness evidence; it does not activate products, approve product work, run product code/tests/builds, change product Git posture, adopt dependencies, publish product material, or promote product docs to root authority.

## 1. Purpose

V-04 specializes product validation after V-00 registry architecture, V-01 proof levels, V-02 evidence, and V-03 migration validation. It defines how AGENT PLATFORM validates product candidates, charters, scope, activation readiness, validation baselines, tests, generated outputs, dependency posture, security posture, Git posture, and product-root boundaries.

V-04 validates product readiness evidence. It does not activate products, approve product work, execute product tests/code/builds, run package managers, change product Git posture, stage/commit product files, adopt dependencies, publish product material, or promote product docs to root authority.

## 2. Product Validation Definition

Product validation is evaluation of whether a product candidate, charter, scope, validation baseline, generated output, dependency posture, security posture, Git posture, or activation candidate satisfies declared criteria inside product scope.

| Boundary | Rule |
| --- | --- |
| Product validation evaluates. | It checks product-scoped criteria, evidence, proof, blockers, and residual risk. |
| Governance decides. | Activation, approval, dependency adoption, Git posture, publication, and promotion require governance. |
| Security constrains. | S-series sensitivity, local-only, secret, credential, execution, provider, and network rules can block validation. |
| Evidence supports. | V-02 evidence supports readiness but does not approve action. |
| Proof is scoped. | V-01 proof applies only to product target, criterion, evidence, freshness, and limitations. |
| Product proof is product-scoped. | Product proof does not validate root authority. |
| Product validation does not activate products. | Activation is a governance decision. |
| Product tests do not prove root authority. | Test output is product-scoped evidence only. |

## 3. Product Validation Object Model

Conceptual fields for a product validation target:

```text
product candidate + product path/reference + product state + product owner
+ product scope + product charter + root-boundary statement + validation baseline
+ dependency posture + security/access posture + generated-output posture
+ Git posture + evidence record + proof level + validation verdict + blocker
+ residual risk + governance posture + stop rule
```

Invalidity rule: activation-supporting product validation is invalid if owner, scope, root boundary, validation baseline, security/access posture, Git posture, dependency posture, evidence, limitations, or stop rule are missing.

## 4. Product Candidate Classes

| Candidate | Validation focus | Default state | Local-only posture | Main risks | Can check now | Cannot infer |
| --- | --- | --- | --- | --- | --- | --- |
| backend-energyplus | Domain/backend charter and engine dependency posture. | candidate/deferred/local_only. | `2_products/` ignored. | Native/domain engine, data, license/name-use. | Metadata, charter need, dependency blockers. | Engine approval or backend behavior. |
| cli | Interface scope, command behavior plan, execution baseline. | candidate/deferred/local_only. | Ignored. | Command execution, packages, user data. | Charter/scope/Git posture. | CLI works or is safe to run. |
| desktop | Desktop runtime, packaging, local data/security. | candidate/deferred/local_only. | Ignored. | Native app, updater, local files, credentials. | Readiness criteria. | Desktop app behavior. |
| experimental | Isolation, owner, blocked/experimental posture. | experimental/blocked/local_only. | Ignored. | Prototype leakage, root confusion. | Blockers and scope needs. | Activation or roadmap priority. |
| omniverse-app | Visualization/product dependency posture. | candidate/deferred/local_only. | Ignored. | SDK/runtime/GPU/local data/license. | Charter and dependency blockers. | Visualization runtime approval. |
| web-platform | Web/interface scope, auth/data/build posture. | candidate/deferred/local_only. | Ignored. | Frontend/backend, auth, builds, deploy. | Baseline/security/Git needs. | Web behavior or deployment readiness. |

No product source was inspected deeply for V-04.

## 5. Product State Validation

| State | Criteria | Evidence required | Allowed next posture | Prohibited inference | Blocker |
| --- | --- | --- | --- | --- | --- |
| candidate | Path/reference and product idea exist. | Inventory/path evidence. | Charter proposal. | Active product. | Missing purpose. |
| active | Governance approved product work. | Decision, owner, scope, baseline. | Product-scoped work by ticket. | Root authority. | Missing governance. |
| experimental | Prototype/sandbox declared. | Owner, isolation, risk notes. | Defer or charter. | Production readiness. | Boundary risk. |
| deferred | Reconsideration postponed. | Deferral reason/trigger. | Reopen later. | Rejection or activation. | No trigger/owner. |
| blocked | Blocking risk/precondition exists. | Blocker record. | Resolve or reject. | Safe to proceed. | Unresolved blocker. |
| archived | Retained under archive policy. | Archive authorization. | Historical reference. | Deletion/cleanup. | No archive policy. |
| retired | No longer active. | Retirement reason. | Historical reference. | Active product. | Missing lifecycle record. |
| local_only | Ignored/untracked product material. | Git ignore/local-only evidence. | Governed Git decision later. | Commit-safe. | Staged local-only. |
| product_scoped_canonical | Product doc accepted inside scope. | Product decision, citations, root boundary. | Product-scoped authority. | Root authority. | Missing root boundary. |
| implementation_ready | Preconditions met for implementation ticket. | Charter, baseline, security, dependency, Git, governance. | Explicit implementation ticket. | Implementation approval by V-04. | Missing baseline/security. |

## 6. Product Charter Validation

Charter criteria: product purpose declared; users/domain/interface declared; owner declared; scope declared; non-goals declared; root relationship declared; product authority boundary declared; product state declared; Git posture declared; validation baseline declared; security/access posture declared; external dependency posture declared; generated-output posture declared; root-boundary statement declared; migration impact declared; governance posture declared.

Missing owner, scope, root boundary, validation baseline, security posture, dependency posture, or governance posture blocks activation-supporting validation.

## 7. Product Scope / Root Boundary Validation

Validation must confirm: product docs are product-scoped; product source does not define root architecture; product behavior does not define AGENT PLATFORM root; product validation does not approve root authority; product dependencies do not become root dependencies; product generated outputs are not source by default; product scope cannot decide Cognitive Semantic System substrate; product needs can inform proposals but not silently constrain root.

## 8. Product Activation Readiness Validation

Activation readiness criteria: charter present; owner present; scope present; state decision present; Git posture present; validation baseline present; security/access posture present; dependency posture present; generated-output posture present; product/root boundary present; product governance path present; blockers listed; residual risks listed.

Activation readiness validation is not activation. Governance must still decide.

## 9. Product Validation Baseline Model

Baseline components: acceptance criteria; product target behavior; non-goals; test strategy; manual review strategy; generated-output handling; security checks; local-only checks; dependency checks; data/model/artifact checks; evidence retention; proof level target; revalidation triggers; known limitations.

Baseline rule: a baseline defines what future validation would check. It does not approve product execution, tests, builds, dependencies, activation, or publication.

## 10. Product Test / Build / Execution Validation

Product tests, code execution, builds, package managers, servers, notebooks, native/domain tools, and product scripts are blocked by default. Tests require exact future command approval under S-04: command, working directory, product scope, expected output, side effects, dependency/network/auth posture, output handling, and stop rule.

Test/build/runtime output is product-scoped evidence. Passing tests does not activate a product and does not promote root authority. Failed, skipped, blocked, partial, or stale tests must remain visible.

## 11. Product Generated Output Validation

| Output | Required validation | Default posture | Proof limit | Publication blocker |
| --- | --- | --- | --- | --- |
| reports | Inputs, generator, citations, sensitivity. | generated-sensitive/local-only. | PL-2/PL-4. | Until reviewed. |
| screenshots | Source screen, data exposure, claims. | generated-sensitive. | PL-2/PL-4. | Privacy/license review. |
| simulation outputs | Engine/input/version/provenance. | local-only. | PL-2/PL-5 later. | Domain validation needed. |
| logs | Command/process/source, redaction. | local-only. | PL-1/PL-5 later. | Secret/credential risk. |
| exports | Source, format, contents, sensitivity. | local-only. | PL-2/PL-4. | Data/license review. |
| generated docs | Generator, inputs, source status. | generated-sensitive. | PL-3/PL-4. | Projection review. |
| build outputs | Build command/env/artifacts. | local-only. | PL-5/PL-6 later. | Build approval absent. |
| product artifacts | Artifact provenance and retention. | local-only. | PL-2/PL-4. | Product/security review. |

## 12. Product Dependency Posture Validation

Validate: dependency identity; product scope; provenance; license/notice posture; security posture; dependency graph; package manager risk; network/auth/provider risk; native/domain engine risk; product data/model/artifact interaction; exact version/source; exit/rollback posture; governance path.

Dependency validation does not approve dependency adoption. Product-specific adoption is not root adoption. External/domain dependencies remain external until governed inside product scope.

## 13. Product Security / Local-only Validation

Validate: `2_products/` remains local-only; product secrets/credentials are never exposed; product `.env`, config, provider auth, registry auth, and local sessions are excluded; product data/models/artifacts are local-only by default; product logs/generated outputs may be sensitive; unknown sensitivity escalates; safe metadata is preferred; product material is not included in context by default.

## 14. Product Git Validation

V-04 does not change product Git posture. `2_products/` remains ignored/local-only. `git status`, `git diff`, and `git check-ignore` can be evidence. Product files must not be staged by default. Product docs/source tracking requires explicit product governance. Product local-only staged is a blocker. Product secret staged is a blocker.

## 15. Product Proof Level Model

| Proof level | Product use |
| --- | --- |
| PL-1 | Metadata/path/local-only/Git ignore checks. |
| PL-2 | Product state, source-status, scope, sensitivity checks. |
| PL-3 | Charter citations and product scope/root references. |
| PL-4 | Charter, scope, root-boundary, dependency, security, and coherence review. |
| PL-5 | Scoped Git/path/naming checks. |
| PL-6 | Product tests only after exact future approval. |
| PL-7 | Product readiness audit. |
| PL-8 | Reproduced product validation/audit. |

## 16. Product Evidence Model

Evidence types: product inventory evidence; product path evidence; product state evidence; product charter evidence; product owner evidence; product scope evidence; root-boundary evidence; validation baseline evidence; dependency posture evidence; security/access posture evidence; generated-output evidence; Git posture evidence; blocker evidence; readiness audit evidence; governance reference evidence.

Retention: product-scoped references over copied content; safe metadata over product source content; generated outputs local-only by default; no secret/credential values; audit trace retained safely.

## 17. Product Verdict Model

| Verdict | Meaning |
| --- | --- |
| `product_ready_for_governance_review` | Criteria satisfied enough for governance review. |
| `product_ready_with_cautions` | Ready only with residual risks. |
| `product_blocked_by_missing_charter` | Charter absent or incomplete. |
| `product_blocked_by_missing_owner` | Owner absent. |
| `product_blocked_by_missing_scope` | Scope absent or unclear. |
| `product_blocked_by_missing_root_boundary` | Root boundary absent. |
| `product_blocked_by_missing_validation_baseline` | Baseline absent. |
| `product_blocked_by_security_access` | Security/access posture unresolved. |
| `product_blocked_by_secret_or_credential_risk` | Secret/credential risk requires stop. |
| `product_blocked_by_dependency_posture` | Dependency posture unresolved. |
| `product_blocked_by_generated_output_risk` | Output provenance/sensitivity unresolved. |
| `product_blocked_by_git_posture` | Git/local-only/staging posture unsafe. |
| `product_blocked_by_product_root_collapse` | Product claim risks root authority. |
| `product_blocked_by_missing_governance` | Governance path absent. |
| `product_inconclusive` | Evidence insufficient or conflicting. |
| `product_deferred` | Safe to postpone pending later ticket/decision. |

Verdict is not activation approval.

## 18. Product Blocker Register

| Blocker | Stop behavior | Required next action | Blocks activation? | Blocks promotion? |
| --- | --- | --- | --- | --- |
| missing charter | Stop readiness claim. | Draft/locate charter. | Yes | Yes |
| missing owner | Stop activation path. | Assign owner. | Yes | Yes |
| missing scope | Stop validation use. | Define scope/non-goals. | Yes | Yes |
| missing non-goals | Qualify scope. | Add non-goals. | Usually | Usually |
| missing product state | Stop state claim. | Declare state. | Yes | Yes |
| missing Git posture | Stop Git claim. | Declare governed posture. | Yes | Yes |
| missing validation baseline | Stop readiness. | Define baseline. | Yes | Yes |
| missing security/access posture | Stop exposure/action. | Security review. | Yes | Yes |
| missing dependency posture | Stop adoption/readiness. | Dependency review. | Yes | Yes |
| missing root-boundary statement | Stop authority claim. | Add root boundary. | Yes | Yes |
| product-root collapse | Stop scope expansion. | Re-scope product claim. | Yes | Yes |
| secret/credential risk | Stop immediately. | Secure handling. | Yes | Yes |
| product local-only leak | Stop exposure/Git. | Redact/safe metadata. | Yes | Yes |
| generated output treated as source | Stop source claim. | Label/review generated output. | Yes | Yes |
| product test treated as root proof | Correct proof scope. | Product-only evidence. | Yes | Yes |
| dependency adoption implied | Stop adoption claim. | Governance review. | Yes | Yes |
| native/domain engine risk unresolved | Stop execution/adoption. | License/security/runtime review. | Yes | Yes |
| missing governance | Stop activation framing. | Define governance path. | Yes | Yes |
| proof insufficient/stale | Stop current support. | Revalidate or defer. | Yes | Yes |

## 19. Product Readiness Audit Model

Audit fields: `product_id`, product candidate, product path/reference, product state, owner, scope, charter reference, root-boundary statement, validation baseline, dependency posture, security/access posture, Git posture, generated-output posture, proof level, evidence retained, verdict, blockers, residual risks, governance posture, reviewer/date, revalidation trigger, stop rule.

Product readiness audit is evidence, not activation approval.

## 20. Matrices

### Matrix A. Product Candidate Vs Validation Focus

| Candidate | charter | dependencies | security | generated outputs | execution risk | activation blocker |
| --- | --- | --- | --- | --- | --- | --- |
| backend-energyplus | High | Domain engine | High | Sim/logs | Native/domain | Dependency/security |
| cli | High | Package/command | Medium | Logs | Command | Scope/baseline |
| desktop | High | Runtime/package | High | Screens/logs | Native/desktop | Security/packaging |
| experimental | Very high | Unknown | High | Unknown | Unknown | Experimental state |
| omniverse-app | High | SDK/runtime | High | Visual/artifacts | Native/GPU | Dependency/license |
| web-platform | High | Web packages/API | High | Build/logs | Build/server | Auth/deploy/security |

### Matrix B. Product State Vs Allowed Validation Outcome

| State | validate | propose | defer | block | activate? |
| --- | --- | --- | --- | --- | --- |
| candidate | Yes | Charter | Yes | If missing basics | No |
| active | Yes | Scope work | Maybe | If posture stale | Needs governance |
| experimental | Limited | Isolation | Yes | Often | No |
| deferred | Metadata | Reopen trigger | Yes | No | No |
| blocked | Blocker only | Fix plan | Yes | Yes | No |
| archived | Historical | Restore proposal | Yes | If no policy | No |
| retired | Historical | Replacement | Yes | No | No |
| local_only | Metadata/Git | Git decision | Yes | If staged | No |
| product_scoped_canonical | Scope/citation | Product update | Maybe | If root leak | No root activation |
| implementation_ready | Readiness audit | Implementation ticket | Maybe | If stale | Needs governance |

### Matrix C. Product Blocker Vs Required Action

| Group | stop | fix | defer | govern | reject |
| --- | --- | --- | --- | --- | --- |
| charter | Yes | Draft charter | Yes | For acceptance | If invalid |
| owner/scope | Yes | Assign/scope | Yes | Required | If unowned |
| security | Yes | Review/redact | Yes | Security decision | If unsafe |
| dependency | Yes | Provenance/license/security | Yes | Adoption decision | If unacceptable |
| Git | Yes | Review status/ignore | Yes | Git posture decision | If secret staged |
| generated output | Yes | Provenance/sensitivity | Yes | Publication decision | If unsafe |
| root boundary | Yes | Re-scope | Yes | Root governance | If collapse persists |
| governance | Yes | Define path | Yes | Required | If no owner/path |

## 21. Product Incidents

Incidents: product local-only content copied into root docs; product secret/credential copied into output; product test treated as root proof; product generated output treated as source; product dependency treated as approved; product code executed without approval; product files staged; product docs promoted to root; product activation implied by validation; product material published without review.

Response: STOP, report safe metadata, do not continue adjacent work, do not expose values, do not stage/commit/push, and require human/product/security/governance decision.

## 22. Product Validation Invariants

| ID | Invariant |
| --- | --- |
| PRODVAL-001 | Product validation evaluates; governance decides. |
| PRODVAL-002 | Product validation does not activate products. |
| PRODVAL-003 | Product tests do not approve products. |
| PRODVAL-004 | Product proof is product-scoped. |
| PRODVAL-005 | Product source does not define root architecture. |
| PRODVAL-006 | Product docs do not override root authority. |
| PRODVAL-007 | Product generated output is not source by default. |
| PRODVAL-008 | Product dependencies require review. |
| PRODVAL-009 | Product-specific dependency is not root dependency. |
| PRODVAL-010 | Product local-only means no default publication. |
| PRODVAL-011 | Product secrets and credentials are never exposed. |
| PRODVAL-012 | Product Git posture is governed. |
| PRODVAL-013 | Product activation requires owner, scope, validation, security, dependency posture, root boundary, and governance. |
| PRODVAL-014 | Cognitive substrate remains undecided. |
| PRODVAL-015 | No product-root collapse. |

## 23. Anti-patterns

Anti-patterns: activation by folder existence; activation by validation; activation by passing tests; product-root collapse; product docs as root architecture; product source as platform authority; product generated output as source; product dependency as root dependency; product test as root proof; local-only product leakage; product execution by curiosity; product build to inspect; package install to validate; product commit by `git add .`; product screenshots/reports published without review; product scope missing; product owner missing; proof level inflation; validation audit as activation approval.

## 24. Remaining Gaps

V-04 does not solve: no product activation, no product charters created, no product validation baselines created, no product tests executed, no product dependency approvals, no product Git posture change, no product source tracking, no product implementation readiness, no external source validation specialization, no validation audit, no registry implementation, no schemas, no CI, no tests, no enforcement, and no Cognitive Semantic System implementation.

## 25. Readiness For V-05

V-05 - External Source Validation Model is ready after explicit instruction. V-05 should specialize external source provenance, license posture, source review, runtime risk, dependency risk, instruction status, network/auth risk, external metadata, allowed/blocked use, execution/adoption blockers, and substrate-evidence boundaries.

Do not create V-05 from V-04.

## 26. Final Verdict

| Question | Answer |
| --- | --- |
| What is product validation? | Scoped evaluation of product candidates, charters, scope, baselines, outputs, dependencies, security, Git posture, and activation readiness inside product scope. |
| What product targets can now be validated? | Six W-12 candidates, product states, charters, scope/root boundaries, readiness, baselines, generated outputs, dependencies, security, Git posture, blockers, and audits. |
| What proof levels apply? | PL-1 through PL-8, with PL-6 only for future explicitly approved product tests. |
| What evidence is required? | Product inventory/path/state, charter, owner, scope, root boundary, baseline, dependency, security, generated-output, Git, blocker, audit, and governance reference evidence. |
| What blocks product activation? | Missing charter/owner/scope/baseline/root boundary/security/dependency/Git/governance posture, secret risk, local-only leak, root collapse, implied dependency adoption, stale proof, or unsafe generated output. |
| Does V-04 authorize product activation? | No. V-04 validates readiness only. |
| Is V-05 ready after explicit instruction? | Yes. |

Stop rule: after completing V-04, STOP. Do not start V-05, activate products, stage, commit, push, execute product code, run product tests/builds, inspect product source deeply, change product Git posture, or start any next ticket.
