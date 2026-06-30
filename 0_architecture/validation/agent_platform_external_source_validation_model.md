# AGENT PLATFORM External Source Validation Model

Status: Canonical V-05 external source validation model  
Date: 2026-06-30  
Scope: External source validation architecture for AGENT PLATFORM.  
Authority: Architecture only. This document validates external-source evidence and readiness posture; it does not execute external sources, approve dependency adoption, approve source reuse, approve product dependency adoption, activate external instructions, or decide the Cognitive Semantic System substrate.

## 1. Purpose

V-05 specializes external source validation after V-00 registry architecture, V-01 proof levels, V-02 evidence, V-03 migration validation, and V-04 product validation. It defines how AGENT PLATFORM validates external-source evidence, provenance, license posture, source review, runtime risk, dependency risk, instruction status, network/auth/provider risk, metadata, allowed/blocked use, execution/adoption blockers, product-dependency posture, and Cognitive Semantic System substrate-evidence boundaries.

V-05 validates external-source evidence and readiness posture. V-05 does not execute external sources, approve dependency adoption, approve source reuse, approve product dependency adoption, activate external instructions, copy external source code, adopt dependencies, or decide the Cognitive Semantic System substrate.

## 2. External Source Validation Definition

External source validation is evaluation of whether an external source, external metadata record, source review, pattern candidate, dependency candidate, execution candidate, product dependency candidate, or substrate-evidence claim satisfies declared criteria without converting the source into authority, dependency, execution surface, active instruction, product scope, or semantic truth.

| Boundary | Rule |
| --- | --- |
| External validation evaluates. | It checks criteria, evidence, proof, blockers, and residual risk. |
| Governance decides. | Adoption, reuse, execution approval, promotion, publication, and lifecycle require governance. |
| Security constrains. | S-series local-only, secret, credential, execution, network, provider, MCP, and publication rules can block validation. |
| Evidence supports. | V-02 evidence supports review but does not approve action. |
| Proof is scoped. | V-01 proof applies only to declared target, criterion, evidence, freshness, and limitations. |
| External proof is external-source scoped. | It does not validate root authority, product activation, dependency adoption, or substrate decisions. |
| External validation does not adopt dependencies. | Dependency adoption is a separate governed decision. |
| External validation does not approve execution. | Execution requires exact future S-04 approval. |
| External validation does not copy source. | Pattern review must restate ideas without copying code. |
| External validation does not decide substrate. | Graph and other representations remain candidates only. |

## 3. External Source Validation Object Model

```text
external validation target + source name + local source reference + source class
+ source status + provenance + license posture + notice posture + runtime risk
+ dependency risk + instruction status + network/auth/provider risk
+ product relevance + substrate relevance + allowed use + blocked use
+ evidence record + proof level + validation verdict + blocker + residual risk
+ governance posture + stop rule
```

Invalidity rule: adoption-supporting or execution-supporting external validation is invalid if provenance, source status, license/notice posture, runtime/dependency/network/auth risk, instruction status, scope, evidence, limitations, governance posture, or stop rule is missing.

## 4. External Source Classes

| Class | Validation can check | Cannot infer | Default proof | Execution risk | Dependency risk | Product risk | Substrate/naming risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| agent harness / coding-agent reference | Harness/session/tool/provider/context patterns and risks. | Runtime authority or tool policy. | PL-2/PL-4. | High. | High. | Medium. | Names/tool models may contaminate. |
| assistant / gateway / protocol integration | Adapter/channel/protocol boundary evidence. | Active gateway, auth path, or trusted bridge. | PL-2/PL-4. | Medium-high. | High. | Medium. | Source names not internal names. |
| registry / catalog | Trust labels, package/skill metadata, supply-chain patterns. | Trusted registry or approved extension source. | PL-2/PL-4. | Medium. | High. | Medium. | Registry vocabulary not authority. |
| cookbook / example corpus | Example taxonomy and documentation patterns. | Validated implementation or safe example execution. | PL-2/PL-3. | Medium. | Medium-high. | Medium. | Examples not canonical docs. |
| domain simulation / SDK reference | Product/domain engine posture and license/name-use risk. | Root dependency or product integration readiness. | PL-2/PL-4. | High/native. | High. | High. | Domain names not root scope. |
| semantic projection / candidate substrate reference | Projection, provenance, generated artifact, substrate tradeoff evidence. | Cognitive Semantic System name, truth, or final substrate. | PL-2/PL-4. | Medium. | Medium. | Low-medium. | Highest graph/naming risk. |

## 5. Current External Source Inventory Validation

| Source | Validation focus | Current status | Highest risk | Allowed validation now | Blocked inference |
| --- | --- | --- | --- | --- | --- |
| acpx | ACP/protocol client boundary. | observed/classified/local_only/not_promoted/blocked. | Protocol bridge/session/network risk. | Metadata and adapter-boundary review. | Approved adapter or execution. |
| ai-cookbook-main | Example taxonomy and integration recipes. | observed/classified/local_only/not_promoted/blocked. | API/credentialed examples. | Example/documentation pattern review. | Validated examples or security guidance. |
| clawhub | Registry/catalog metadata and trust patterns. | observed/classified/local_only/not_promoted/blocked. | Supply-chain/package trust. | Registry metadata review. | Trusted registry or package source. |
| ECC-main | Agent OS/harness orchestration evidence. | observed/classified/local_only/not_promoted/blocked. | Authority/runtime collapse. | Harness pattern/risk review. | Runtime or governance authority. |
| EnergyPlusV24-2-0 | Domain simulation engine reference. | observed/classified/local_only/not_promoted/blocked. | Native binary and domain license/name-use. | Product/domain dependency blocker review. | Root dependency or execution approval. |
| graphify | Graph-oriented semantic projection evidence. | observed/classified/local_only/not_promoted/blocked. | Projection mistaken for truth/substrate decision. | Substrate-neutral projection review. | System naming, truth, or final substrate. |
| hermes-agent | Self-improvement and lifecycle risk evidence. | observed/classified/local_only/not_promoted/blocked. | Self-modification/dependency risk. | Risk-first harness review. | Self-improvement adoption. |
| openclaw | Assistant/gateway and skill packaging evidence. | observed/classified/local_only/not_promoted/blocked. | Credentials/user data/skill execution. | Gateway/skill boundary review. | Active assistant gateway. |
| opencode | Coding-agent session/tool/context evidence. | observed/classified/local_only/not_promoted/blocked. | File/shell/provider/session risk. | Context/tool pattern review. | Workspace agent config or execution policy. |
| openstudio | Building-energy SDK/tooling reference. | observed/classified/local_only/not_promoted/blocked. | SDK/native/package/license risk. | Product/domain blocker review. | Root SDK or product integration. |
| pi | Coding-agent harness/provider/tool evidence. | observed/classified/local_only/not_promoted/blocked. | Provider/file/shell/session risk. | Harness/session pattern review. | Active harness or provider config. |
| tau | Minimal coding-agent harness and instruction-risk evidence. | observed/classified/local_only/not_promoted/blocked; license unresolved for reuse. | Credentials, `AGENTS.md`, license gap. | License/instruction/harness review. | Active instructions or source reuse. |

## 6. External Source Status Validation

| Status | Criteria | Evidence required | Allowed next posture | Prohibited inference | Blocker condition |
| --- | --- | --- | --- | --- | --- |
| observed_snapshot | Local snapshot reference exists. | Path/inventory metadata. | Classification. | Approval. | Missing reference. |
| classified_external_reference | W-03/W-13 class assigned. | Registry/policy citation. | Metadata review. | Authority. | Unknown class. |
| local_only | Raw source remains ignored/local. | `.gitignore`/Git evidence. | Governed review later. | Commit-safe. | Raw source staged. |
| not_promoted | No accepted use/authority. | Governance/status evidence. | Review candidate. | Adoption. | Promotion implied. |
| execution_blocked | Execution prohibited by default. | S-04/W-13 policy. | Execution candidate later. | Safe to run. | Command proposed without approval. |
| dependency_blocked | Install/adoption prohibited. | Dependency policy. | Dependency candidate later. | Approved dependency. | Adoption implied. |
| instruction_blocked | External instructions inactive. | Instruction review. | Pattern evidence. | Agent rule. | Instruction followed. |
| metadata_candidate | Metadata may be curated. | Review ticket/scope. | Metadata review. | Approval. | Scope absent. |
| metadata_reviewed | Provenance/license/risk recorded. | Review record. | Pattern/dependency/execution candidate. | Adoption/execution. | Missing fields. |
| pattern_candidate | Abstract pattern proposed. | Source citation/restatement. | Governance review. | Code reuse. | Source copy/name import. |
| pattern_adopted | Internal restated pattern accepted for scope. | Decision/governance ref. | Scoped use. | Dependency adoption. | No governance/scope. |
| dependency_candidate | Dependency under evaluation. | Owner/scope/review plan. | Governance review. | Approved dependency. | License/security/deps absent. |
| dependency_approved | Dependency approved for declared scope. | Governance/security/license/validation. | Scoped use. | Root adoption if product-scoped. | Scope/version missing. |
| execution_candidate | Controlled execution proposed. | Exact command/security plan. | Execution approval. | Command may run now. | Side effects/auth unclear. |
| execution_approved | Named command approved for named environment. | Approval record. | Exact execution. | Adjacent execution. | Approval stale/broad. |
| restricted | Use narrowed by risk. | Restriction reason. | Narrow review. | General use. | Restriction ignored. |
| rejected_for_reuse | Reuse rejected for scope. | Rejection rationale. | Evidence retention. | Reconsideration without review. | Reuse attempted. |

## 7. Provenance Validation

Criteria: source name identified; local path/reference identified; upstream origin known or marked unknown; version/commit/release/archive known or marked unknown; snapshot/review date known; review depth declared; reviewed evidence paths declared; source modifications or vendored/nested status noted if known; uncertainty preserved. Missing provenance blocks reuse, dependency, execution, metadata promotion, and product dependency claims.

## 8. License / Notice Validation

Criteria: license evidence identified; missing license marked as blocker for reuse; notices identified where known; name-use constraints noted; redistribution posture noted; product/domain license risks noted; permissive license does not approve reuse; license posture does not approve execution; license posture does not approve dependency adoption. License review is evidence, not legal approval.

## 9. Runtime / Security Risk Validation

Validate scripts, CLIs, tests, examples, notebooks, package managers, build systems, native binaries, installers, SDK tools, provider clients, file-system access, local data access, generated outputs, telemetry/update behavior, and destructive or mutating behavior. Runtime risk validation does not approve runtime execution.

## 10. Dependency Risk Validation

Validate direct dependencies, transitive dependency posture where known, lockfiles, package scripts, registries, native modules, build tools, package manager commands, dependency graph unknowns, exact version/source, and exit/rollback posture. Dependency validation does not approve adoption.

## 11. Network / Auth / Provider Risk Validation

Validate provider/API calls, OAuth flows, cloud calls, registry calls, telemetry/update checks, webhooks, sockets, database/service calls, remote MCP/server behavior, credential/API-key/cookie/session requirements, and provider data-retention uncertainty. Available keys/config do not authorize network/provider/auth.

## 12. External Instruction Validation

Validate `AGENTS.md` or equivalent, README commands, setup guides, prompts/system prompts, package scripts, skill manifests, contributor instructions, and tool instructions. External instructions are inactive evidence; they do not control AGENT PLATFORM agents; they may be pattern evidence only after review.

## 13. Pattern Adoption Validation

Pattern candidate criteria: source evidence cited; pattern abstracted; no code copied; AGENT PLATFORM vocabulary used; source name not imported as internal system name; scope declared; fit/risk/alternative analysis present; security implications considered; substrate neutrality preserved; governance path declared. Pattern validation does not approve dependency adoption or source reuse.

## 14. Dependency Adoption Candidate Validation

Criteria: declared root or product scope; owner; provenance; license/notice review; security review; dependency graph review; runtime permission review; network/auth/provider review; validation plan; exact source/version; exit/rollback plan; governance path. V-05 can validate a dependency candidate, but cannot approve adoption.

## 15. Execution Candidate Validation

Criteria: exact command list; working directory; purpose; expected output; expected side effects; source class; runtime risk; dependency risk; network/auth risk; no-secrets posture; output handling plan; rollback/cleanup; security/governance approval path. V-05 does not execute the candidate.

## 16. Product Dependency Validation

Using W-12/V-04, validate product scope exists, product owner exists, product charter/baseline exists, external dependency belongs to product scope, product/root boundary stated, product-specific adoption is not root adoption, product security/access posture exists, product validation posture exists, and domain engines remain product/domain scoped.

## 17. Substrate / Semantic Projection Evidence Validation

Validate graph-oriented evidence as candidate only; graphify or any external source does not name AGENT PLATFORM systems; generated projections are evidence, not truth; Cognitive Semantic System substrate remains undecided; alternatives remain open: graph, relational, document, vector, event-sourced, hybrid, other; substrate decision requires explicit future ADR/governance.

## 18. External Source Proof Level Model

| Proof level | External source use |
| --- | --- |
| PL-1 | Metadata/path/source existence checks. |
| PL-2 | Source status, class, sensitivity, blocked/default posture. |
| PL-3 | Citation/provenance/license reference review. |
| PL-4 | External review, coherence, license/runtime/dependency/instruction/network risk review. |
| PL-5 | Scoped metadata/Git/path checks only. |
| PL-6 | Only future explicitly approved tests/execution. |
| PL-7 | Structured external source audit. |
| PL-8 | Reproduced external review/audit. |

## 19. External Source Evidence Model

Evidence types: source inventory evidence; source path/reference evidence; source status evidence; provenance evidence; license/notice evidence; runtime risk evidence; dependency risk evidence; instruction status evidence; network/auth risk evidence; product relevance evidence; substrate relevance evidence; blocked-use evidence; external review evidence; governance reference evidence.

Retention: metadata/review references over raw source content; no source code copying by default; no secret/credential values; raw external source local-only by default; audit trace retained safely.

## 20. External Source Verdict Model

| Verdict | Meaning |
| --- | --- |
| `external_ready_for_metadata_review` | Enough evidence to create/review metadata. |
| `external_ready_with_cautions` | Usable only with residual risks. |
| `external_ready_for_governance_review` | Candidate ready for governance review, not approval. |
| `external_blocked_by_missing_provenance` | Identity/origin/version/review depth missing. |
| `external_blocked_by_missing_license_review` | License/notice/name-use unresolved. |
| `external_blocked_by_runtime_risk` | Execution/native/tool risk unresolved. |
| `external_blocked_by_dependency_risk` | Dependency graph/package risk unresolved. |
| `external_blocked_by_network_auth_risk` | Network/provider/auth risk unresolved. |
| `external_blocked_by_instruction_risk` | External instructions may leak or conflict. |
| `external_blocked_by_product_scope` | Product owner/scope/baseline absent. |
| `external_blocked_by_substrate_assumption` | Graph/projection/source assumed as substrate/truth. |
| `external_blocked_by_secret_or_credential_risk` | Secret/credential risk requires stop. |
| `external_blocked_by_missing_governance` | Decision path absent. |
| `external_inconclusive` | Evidence insufficient or conflicting. |
| `external_deferred` | Safe to postpone. |
| `external_rejected_for_reuse` | Reuse rejected for declared scope. |

Verdict is not adoption approval.

## 21. External Source Blocker Register

| Blocker | Stop behavior | Required next action | Blocks execution? | Blocks adoption? | Blocks promotion? |
| --- | --- | --- | --- | --- | --- |
| missing provenance/status/review depth | Stop current claim. | Complete metadata review. | Yes | Yes | Yes |
| missing license/notice review | Stop reuse/adoption. | License/notice/name-use review. | Usually | Yes | Yes |
| unknown dependency graph/package scripts | Stop dependency framing. | Dependency/lockfile/script review. | Yes | Yes | Yes |
| runtime/native binary risk | Stop execution. | Runtime/security review. | Yes | Yes | Yes |
| network/provider/API risk | Stop network/auth path. | Provider/network review. | Yes | Yes | Yes |
| credential/auth risk | Stop immediately. | Secure handling approval. | Yes | Yes | Yes |
| external instruction leakage | Stop instruction use. | Mark inactive/review pattern. | Maybe | Maybe | Yes |
| source-copy risk/adoption implied | Stop reuse claim. | Restate pattern or govern reuse. | Maybe | Yes | Yes |
| product scope/root collapse/domain root risk | Stop product dependency claim. | Product scope/governance review. | Yes | Yes | Yes |
| generated projection as truth/substrate assumption/source name as internal name | Stop semantic claim. | Restore substrate/name neutrality. | No | Maybe | Yes |
| governance missing/proof insufficient/stale evidence | Stop readiness claim. | Add owner, proof, or revalidate. | Yes | Yes | Yes |

## 22. External Source Audit Model

Audit fields: `external_review_id`, source name, source class, local reference, upstream provenance, version/snapshot, review depth, license posture, notice posture, runtime risk, dependency risk, network/auth risk, instruction status, product relevance, substrate relevance, allowed use, blocked use, proof level, evidence retained, verdict, blockers, residual risks, security/access posture, governance posture, reviewer/date, revalidation trigger, stop rule.

External source audit is evidence, not adoption approval.

## 23. Matrices

### Matrix A. Source Class Vs Validation Focus

| Class | provenance | license | runtime | dependency | network/auth | instruction | product | substrate | default blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent harness | High | High | High | High | High | Medium | Medium | Medium | execution/dependency/auth |
| assistant/gateway | High | High | High | High | High | Medium | Medium | Low | network/auth/gateway |
| registry/catalog | High | High | Medium | High | Medium | High | Medium | Low | supply-chain/trust |
| cookbook | Medium | Medium | Medium | Medium | High | Medium | Medium | Low | examples/credentials |
| domain simulation/SDK | High | High | High | High | Medium | Low | High | Low | native/license/product |
| semantic projection | High | Medium | Medium | Medium | Low | Medium | Low | High | substrate/truth/naming |

### Matrix B. Current Source Vs Highest Validation Risk

| Source | Class | Highest risk | Allowed validation now | Blocked inference |
| --- | --- | --- | --- | --- |
| acpx | assistant/gateway | protocol bridge/network/auth | metadata + boundary review | adapter/execution approval |
| ai-cookbook-main | cookbook | credentialed examples | example taxonomy review | validated examples |
| clawhub | registry/catalog | package trust/supply chain | registry metadata review | trusted registry |
| ECC-main | agent harness | runtime/authority collapse | harness pattern review | agent OS authority |
| EnergyPlusV24-2-0 | domain simulation/SDK | native/license/name-use | product/domain blocker review | root dependency |
| graphify | semantic projection | graph/truth/naming confusion | projection/substrate-neutral review | substrate decision |
| hermes-agent | agent harness | self-improvement/dependencies | risk-first review | self-improvement adoption |
| openclaw | assistant/gateway | gateway credentials/user data | channel/skill boundary review | active gateway |
| opencode | agent harness | file/shell/provider/session | context/tool pattern review | workspace execution policy |
| openstudio | domain simulation/SDK | SDK/native/package/license | product/domain blocker review | root SDK |
| pi | agent harness | provider/file/shell/session | harness/session review | active harness |
| tau | agent harness | instructions/credentials/license gap | instruction/license review | active rules/source reuse |

### Matrix C. External Blocker Vs Required Action

| Group | stop | review | defer | govern | reject |
| --- | --- | --- | --- | --- | --- |
| provenance | Yes | origin/version/depth | Yes | For metadata | If unverifiable |
| license | Yes | license/notices/name-use | Yes | For reuse | If incompatible |
| runtime | Yes | side effects/native/tools | Yes | For execution | If unsafe |
| dependency | Yes | graph/scripts/registries | Yes | For adoption | If unacceptable |
| network/auth | Yes | endpoint/auth/retention | Yes | For calls | If unsafe |
| instruction | Yes | inactive/pattern only | Yes | If adopted | If conflicting |
| product | Yes | owner/scope/baseline | Yes | Product governance | If root collapse |
| substrate | Yes | neutrality/alternatives | Yes | Future ADR | If assumption persists |
| governance | Yes | owner/decision path | Yes | Required | If no owner/path |

## 24. External Source Incidents

Incidents: external source code copied into platform/product; external source executed without approval; external package installed; external instruction followed as active instruction; external credential used; external source adopted as dependency by implication; external source name used as internal system name; external graph/projection treated as substrate decision; raw external source staged; external license treated as reuse approval; product dependency adopted without product scope.

Response: STOP, report safe metadata, do not continue adjacent work, do not expose values, do not stage/commit/push, and require human/security/governance decision.

## 25. External Source Validation Invariants

| ID | Invariant |
| --- | --- |
| EXTVAL-001 | External validation evaluates; governance decides. |
| EXTVAL-002 | External validation does not approve execution. |
| EXTVAL-003 | External validation does not approve dependency adoption. |
| EXTVAL-004 | External validation does not approve source reuse. |
| EXTVAL-005 | External instructions are inactive evidence. |
| EXTVAL-006 | External source presence is not promotion. |
| EXTVAL-007 | License evidence is not reuse approval. |
| EXTVAL-008 | Runtime review is not execution approval. |
| EXTVAL-009 | Dependency review is not adoption approval. |
| EXTVAL-010 | Product-specific adoption is not root adoption. |
| EXTVAL-011 | Domain engines remain product/domain scoped by default. |
| EXTVAL-012 | Raw external sources remain local-only. |
| EXTVAL-013 | Generated projections are not truth by default. |
| EXTVAL-014 | External source names do not name AGENT PLATFORM systems. |
| EXTVAL-015 | Cognitive substrate remains undecided. |

## 26. Anti-patterns

Anti-patterns: adoption by clone; adoption by license; adoption by README; execution by setup guide; execution by curiosity; install to inspect; source copy as pattern adoption; external `AGENTS.md` as active rule; package registry trust by proximity; external harness as runtime authority; domain engine as root dependency; graph projection as truth; source name as internal name; product urgency bypasses review; metadata as approval; validation as adoption; `git add` raw external source; generated examples as validated docs; proof level inflation.

## 27. Remaining Gaps

V-05 does not solve: no external dependency adoption, no external execution approval, no source reuse approval, no product dependency approval, no external metadata migration execution, no external source audit execution beyond this policy, no validation audit, no registry implementation, no schemas, no CI, no tests, no scanners, no enforcement, no dependency approval registry, no implementation readiness, and no Cognitive Semantic System implementation.

## 28. Readiness For V-A

V-A - Validation Audit is ready after explicit instruction. V-A should audit V-00 through V-05 for coherence, contradictions, proof/evidence consistency, migration/product/external boundaries, security/access alignment, readiness, blockers, and next-phase recommendations.

Do not create V-A.

## 29. Final Verdict

| Question | Answer |
| --- | --- |
| What is external source validation? | Scoped evaluation of external source evidence, metadata, reviews, patterns, dependency candidates, execution candidates, product dependency candidates, and substrate-evidence claims without converting them into authority, dependency, execution, instruction, product scope, or truth. |
| What external targets can now be validated? | W-03/W-13 source classes, all 12 current sources, statuses, provenance, license/notice, runtime, dependency, network/auth/provider, instruction, pattern, dependency, execution, product dependency, substrate evidence, verdicts, blockers, and audits. |
| What proof levels apply? | PL-1 through PL-8, with PL-6 only for future explicitly approved tests/execution. |
| What evidence is required? | Inventory/path/status, provenance, license/notice, runtime/dependency/instruction/network/auth/product/substrate relevance, blocked-use, review, and governance reference evidence. |
| What blocks external adoption or execution? | Missing provenance/license/governance, unresolved runtime/dependency/network/auth/instruction/product/substrate/secret risk, stale proof, product scope gap, source-copy risk, or implied adoption. |
| Does V-05 authorize dependency adoption, execution, or source reuse? | No. V-05 validates readiness only. |
| Is V-A ready after explicit instruction? | Yes. |

Stop rule: after completing V-05, STOP. Do not start V-A, stage, commit, push, execute external code, install dependencies, authenticate, call network/provider/API/MCP, inspect external source code deeply, copy source, adopt dependencies, approve reuse, activate products, or start any next ticket.
