# AGENT PLATFORM Agent Access Profiles

Status: Canonical S-02 agent access profiles  
Date: 2026-06-28  
Scope: Concrete access profiles for agent roles operating inside AGENT PLATFORM  
Authority: Agent access profile architecture only. This document restricts agent behavior and maps role-specific access posture, but does not implement enforcement, create permission code, create scripts, hooks, tests, runtime guards, packages, SDKs, policies-as-code, access-control schemas, modify S-00/S-01, modify W-series docs, modify `.gitignore`, move files, rename folders, migrate previous knowledge, inspect product or external source code deeply, run code, install dependencies, authenticate, stage, commit, push, or create S-03.

## 1. Purpose

S-02 follows S-00 and S-01 because agent behavior needs concrete profile boundaries after the workspace security/access architecture and workspace access model exist.

| Prior document | Role in S-02 |
| --- | --- |
| S-00 Security / Access Architecture | Defines security/access concepts, sensitivity levels, blocked actions, execution rules, Git rules, and security/governance/validation boundaries. |
| S-01 Workspace Access Model | Defines access as actor, role, action, target surface, sensitivity, source status, scope, approval, validation, governance, and stop rule. |
| S-02 Agent Access Profiles | Converts the access model into agent-specific read, cite, write, validate, escalation, and stop postures. |

Clarifications:

| S-02 is | Meaning |
| --- | --- |
| Architecture only | It defines profiles and constraints. |
| Not enforcement | It does not create technical permissions, runtime guards, hooks, schemas, policy code, or access-control implementation. |
| Not autonomous authority | It does not grant agents approval, governance, promotion, Git, execution, migration, product activation, dependency adoption, publication, or substrate-decision authority. |
| Not scope expansion | The active ticket still controls actual access. Profiles restrict what an agent may do inside that ticket. |

## 2. Profile Model

An agent access profile is:

```text
agent role
+ allowed surfaces
+ allowed actions
+ prohibited actions
+ sensitivity ceiling
+ context requirements
+ citation requirements
+ validation permissions
+ Git posture
+ execution posture
+ escalation triggers
+ output obligations
+ stop rule
```

Profile rules:

| Rule | Meaning |
| --- | --- |
| Profiles restrict; they do not expand active-ticket scope. | A profile cannot make an unscoped file readable or editable. |
| Active ticket controls actual access. | The ticket objective, allowed scope, forbidden scope, validation, and stop rule remain primary. |
| Human approval gates authority-sensitive actions. | Stage, commit, push, migration execution, risky execution, publication, product activation, external adoption, and promotion require explicit approval. |
| Context inclusion is not permission. | Seeing material in a prompt, context pack, search result, or selected evidence set does not authorize editing, execution, Git, migration, publication, or promotion. |
| Sensitivity can narrow any profile. | Secret, credential, restricted, unknown, local-only, generated-sensitive, external-restricted, and product-restricted material can force stop/escalation. |

## 3. Global Agent Defaults

Allowed by default only when ticket-scoped:

| Action | Default posture |
| --- | --- |
| discover | Ticket-scoped only. |
| read | Ticket-scoped only. |
| summarize | Ticket-scoped only. |
| classify | Ticket-scoped only. |
| cite | Ticket-scoped only and source-status aware. |
| draft | Ticket-scoped only and named-target constrained. |
| propose | Ticket-scoped only; proposals are not decisions. |
| validate | Only when explicitly scoped, with allowed commands and expected outputs. |

Blocked by default for every agent:

| Blocked action | Default rule |
| --- | --- |
| execute | No code, scripts, tools, tests, products, external sources, native binaries, package commands, MCP, providers, or network calls without explicit approval. |
| install | No dependency/package/model/tool installation without approval. |
| authenticate | No provider, cloud, OAuth, SSH, cookie, registry, or service auth without approval. |
| network/API/provider call | No network/provider/API calls without approval. |
| MCP activation | No MCP activation without approval. |
| migrate | No movement, restatement, archive, or transition without migration ticket and governance. |
| delete/move/rename/archive | Explicit human/governance approval required. |
| stage/commit/push | Explicit human Git approval required. |
| publish/promote | Governance/security/publication approval required. |
| product activation | Product governance required. |
| external dependency adoption | External review, security, license, validation, and governance required. |
| substrate decision | Explicit Cognitive Semantic System decision required. |
| secret/credential handling | Stop and escalate; do not expose values. |

## 4. Agent Profile: Reader

| Field | Profile |
| --- | --- |
| Purpose | Answer questions, summarize scoped material, identify references, and report uncertainty without changing files. |
| Allowed surfaces | Active ticket, relevant `0_architecture/` docs, `README.md`, `.gitignore`, and explicitly scoped evidence. |
| Allowed actions | discover, read, cite, summarize. |
| Prohibited surfaces | Product folders, raw external sources, previous knowledge, datasets, models, artifacts, generated/runtime folders, secrets, credentials, and local-only material unless explicitly scoped. |
| Prohibited actions | write, edit, validate, execute, install, authenticate, migrate, stage, commit, push, publish, promote. |
| Citation requirements | Cite inspected paths and distinguish canonical, evidence, projection, generated, product-scoped, external, historical, or local-only status when relevant. |
| Output obligations | Provide concise answer, files inspected, uncertainty, and stop-rule compliance when relevant. |
| Escalation triggers | Need to edit, validate, run commands, inspect local-only/sensitive material, access secrets, or continue to next ticket. |
| Stop rule | Stop after answering. Do not transition into writer, validator, executor, migration, or Git role without explicit instruction. |

Expected posture: read-only, no writes, no execution, no Git actions, no migration, no promotion.

## 5. Agent Profile: Researcher

| Field | Profile |
| --- | --- |
| Purpose | Investigate scoped research/evidence and produce findings, comparisons, risks, uncertainty, and recommendations. |
| Research/evidence access | May inspect `1_research/` and selected evidence only when scoped. May use W-series/S docs for authority context. |
| Research citation requirements | Cite research paths, source status, freshness/uncertainty, and W-series/S authority when claims affect architecture/security/access/governance/product/external reuse. |
| External limits | Use W-03/W-13 registry and policy for external claims; raw external source reading requires explicit external-review scope. |
| Previous-knowledge limits | Use W-02/W-08 posture; prior material remains migration evidence and must be cited by path/classification. |
| Allowed research outputs | Findings, comparisons, hypotheses, risk notes, recommendation options, and research docs only by explicit research ticket. |
| Prohibited actions | Promote findings, implement, run code, install dependencies, authenticate, migrate, stage, commit, push, publish, adopt dependencies, or activate products. |

Expected posture: can inspect research/evidence when scoped; can create research docs only by explicit research ticket; cannot promote findings.

## 6. Agent Profile: Classifier

| Field | Profile |
| --- | --- |
| Purpose | Assign source class, status, sensitivity, authority posture, migration posture, and risk labels to scoped material. |
| Allowed classification targets | Explicitly named docs, evidence, previous-knowledge entries, external registry items, product candidates, generated outputs, or workspace areas. |
| Classification output rules | Output tables or classification docs only by explicit ticket; classifications are evidence/control inputs, not promotion by themselves. |
| Source-status handling | Preserve original source status; mark missing status as unclassified evidence. |
| Citation requirements | Cite W-02 for previous knowledge, W-03/W-13 for external sources, W-09 for status/scope labels, S-00/S-01 for sensitivity/access posture. |
| Prohibited actions | Promote, migrate, move, copy, delete, edit source evidence, run code, install, authenticate, stage, commit, push, or archive. |

Expected posture: can classify; cannot promote, migrate, move, or edit source evidence.

## 7. Agent Profile: Architect

| Field | Profile |
| --- | --- |
| Purpose | Draft canonical or proposal architecture by explicit ticket using current authority and cited evidence. |
| Architecture read scope | Current `0_architecture/` docs, S-series security docs, W-series workspace docs, and explicitly scoped evidence. |
| Architecture write scope | Only the named architecture file or target explicitly allowed by the active ticket. |
| Architecture citation rules | Cite canonical source docs, source-status model, governance/validation/security posture, and evidence paths for material claims. |
| Authority boundary | Architecture can constrain future work but cannot approve governance, validation, promotion, implementation, product activation, or external adoption by itself. |
| Prohibited implementation/product/external actions | No code implementation, product activation, product Git posture change, external dependency adoption, external source copy, provider auth, execution, package install, or publication. |
| Escalation triggers | Need code changes, migration execution, product source, raw external source, dependency decision, secret/credential handling, publication, or Cognitive Semantic System substrate decision. |

Expected posture: can draft architecture by explicit ticket; cannot implement; cannot decide substrate unless explicit decision ticket; cannot activate products or dependencies.

## 8. Agent Profile: Migration Planner

| Field | Profile |
| --- | --- |
| Purpose | Plan controlled migration without executing it. |
| Migration planning access | W-02, W-08, W-09, W-04/W-07, S-series access docs, and explicitly scoped previous knowledge or evidence. |
| Previous knowledge handling | Read by migration/classification/restatement scope only; cite original path and W-02 state; preserve originals. |
| Migration evidence rules | `carry_forward` requires restatement; `conflicted` requires normalization; prior canonical labels are historical only. |
| Allowed outputs | Migration plans, source/target maps, classification tables, blockers, validation plans, and governance preconditions. |
| Prohibited execution/movement | No move, copy, delete, rename, archive, wholesale migration, product movement, external movement, staging, commit, or push. |

Expected posture: can plan migration; cannot execute migration; cannot move/copy/delete/archive files; cannot migrate wholesale.

## 9. Agent Profile: Documentation Writer

| Field | Profile |
| --- | --- |
| Purpose | Create or update named documentation/projection artifacts under explicit docs/architecture scope. |
| Docs projection access | Source authority docs, selected evidence, W-09 status/scope/citation rules, and active ticket target. |
| Allowed docs outputs | Named docs, projections, guides, summaries, structure docs, and status/scope/citation updates only when scoped. |
| Status/scope/citation requirements | Declare status and scope where appropriate; cite source authority; identify projection vs canonical authority. |
| Projection boundaries | Human docs explain or project source authority; they do not override architecture by readability. |
| Prohibited authority changes | Cannot make docs canonical by writing them, override root architecture, publish sensitive material, migrate evidence, or promote claims. |

Expected posture: can write named docs by explicit ticket; cannot make docs canonical by writing them; cannot override architecture.

## 10. Agent Profile: External Source Reviewer

| Field | Profile |
| --- | --- |
| Purpose | Review external sources as evidence without adopting, executing, copying, or promoting them. |
| External registry access | May read W-03/W-13 and selected external metadata/review evidence. |
| Raw external source access limits | Raw external source reading requires explicit scoped review; avoid deep code inspection unless named. |
| Allowed review outputs | Source review, provenance notes, license posture, security risk, relevance, blockers, and metadata proposals. |
| License/security/provenance handling | Treat license as evidence, not approval; identify execution/dependency/credential/network/native risks. |
| Prohibited actions | Run external code, install dependencies, authenticate, call network/provider/API, copy source, edit raw external sources, approve dependency adoption, activate products, or decide substrate. |

Expected posture: can review external sources only when scoped; cannot run external code, install dependencies, authenticate, copy source, or approve dependency adoption.

## 11. Agent Profile: Product Reviewer

| Field | Profile |
| --- | --- |
| Purpose | Review product candidates as bounded product-scoped evidence without activating or publishing them. |
| Product access limits | Product material is read only by explicit product ticket; product source/code deep inspection requires explicit scope. |
| Allowed product review outputs | Product-scope findings, boundary risks, product evidence, root-impact notes, charter recommendations, blockers. |
| Product-scope boundaries | Product docs/claims are product-scoped and cannot define root AGENT PLATFORM authority by default. |
| Prohibited product actions | Activate products, run product code, stage/commit product files, change product Git posture, adopt product dependencies, publish product claims, or make product docs root authority. |

Expected posture: can inspect product candidates only by explicit product ticket; cannot activate products, stage/commit product files, make product docs root authority, or run product code.

## 12. Agent Profile: Implementation Planner

| Field | Profile |
| --- | --- |
| Purpose | Plan future implementation without writing code or executing tooling. |
| Implementation planning access | Current architecture, security/access, responsibility map, topology, docs structure, and validation/security blockers. |
| Allowed implementation-plan outputs | Implementation plans, readiness blockers, dependency maps, required tests, required security/validation decisions, risk registers. |
| Code-read limits | May read implementation candidates only if explicit planning task scopes the files; code presence does not define architecture. |
| Prohibited code/actions | No implementation code writes unless a later explicit implementation ticket exists; no installs, execution, builds, package/SDK changes, dependency adoption, product activation, staging, commit, or push. |

Expected posture: can plan implementation; cannot write implementation code unless later explicit implementation ticket exists; cannot install, execute, build, or adopt dependencies.

## 13. Agent Profile: Validator

| Field | Profile |
| --- | --- |
| Purpose | Evaluate scoped claims, files, commands, or artifacts and report evidence. |
| Validation access | Active validation task, specified files, expected commands, relevant canonical docs, and validation rules. |
| Allowed validation actions | Read scoped files, run explicitly allowed validation commands, inspect outputs, report results. |
| Validation output requirements | Include commands run, outputs, pass/fail posture, limitations, residual risks, and skipped/blocked validation. |
| Proof/evidence separation | Validation output is evidence; it does not approve governance, promotion, publication, Git, product activation, or security exceptions. |
| Prohibited governance actions | Cannot stage, commit, push, promote, publish, approve, migrate, adopt dependencies, or continue after passing validation. |

Expected posture: can run only explicitly allowed validation commands; validation evaluates and does not approve; cannot stage, commit, push, promote, or publish after passing validation.

## 14. Agent Profile: Executor

| Field | Profile |
| --- | --- |
| Purpose | Perform exact scoped actions when a task explicitly permits execution/write behavior. |
| Strict execution prerequisites | Exact task, exact files, exact command/action, working directory, side effects, sensitivity check, credential check, rollback/cleanup, validation output, human approval when risky. |
| Allowed write actions | Only files explicitly named or scoped by the task. |
| Command/action constraints | No adjacent commands, no implicit installs, no auth, no network/provider/API/MCP, no external/product execution unless explicitly approved. |
| Output/validation obligations | Report changed files, commands/actions run, validation results, uncertainty, side effects, skipped steps, and stop-rule compliance. |
| Stop rule | Stop after scoped action and validation. Do not continue to next ticket, commit, push, migrate, publish, or promote unless explicitly instructed. |

Expected posture: most restricted high-risk role; can execute only when exact task permits exact action; cannot infer adjacent permissions; cannot continue after task completion.

## 15. Agent Profile: Subagent

| Field | Profile |
| --- | --- |
| Purpose | Perform narrow delegated research/exploration/analysis under parent task constraints. |
| Inheritance rules | Subagents inherit all parent task restrictions and receive narrower scope than the parent. |
| Delegated scope | Must include specific question, allowed paths, forbidden paths, expected output, uncertainty, and stop rule. |
| Evidence-return requirements | Return findings, paths, uncertainty, conflicts, and validation notes. |
| Prohibited actions | Approve, promote, execute beyond scope, stage, commit, push, migrate, publish, adopt dependencies, activate products, handle secrets, or continue tickets. |
| Parent-agent merge responsibility | Parent agent must merge subagent evidence, preserve uncertainty, cite sources, and not treat subagent output as validation or governance. |

Expected posture: subagents receive narrower scope than parent; return evidence only; cannot approve, promote, execute beyond scope, stage, commit, push, or continue tickets.

## 16. Human / Agent Boundary

Only humans or delegated governance roles can approve:

| Approval area | Agent boundary |
| --- | --- |
| staging | Agents may propose exact files but cannot stage without approval. |
| commit | Agents may propose message/scope but cannot commit without approval. |
| push | Agents may report branch/remote but cannot push without approval. |
| delete | Agents cannot delete without explicit approval. |
| move | Agents cannot move files/folders without explicit approval. |
| rename | Agents cannot rename files/folders without explicit approval. |
| migration execution | Agents can plan; governance approves execution. |
| archive creation | Agents can identify candidates; governance/archive policy approves. |
| external execution | External execution requires security/environment/governance approval. |
| dependency adoption | Agents can review; governance approves adoption. |
| authentication | Provider/cloud/API/local auth requires explicit approval and secure handling. |
| network/provider/API calls | Agents cannot call by default; approval is exact-action-specific. |
| MCP activation | Agents cannot activate MCP by default. |
| product activation | Agents can review/propose; product/governance roles approve. |
| publication | Agents can draft; humans/governance approve publication. |
| authority promotion | Agents propose; governance promotes. |
| security exception | Security/governance roles decide; agents report risks. |
| final Cognitive Semantic System substrate decision | Requires explicit decision process; agents cannot infer from graph evidence. |

## 17. Profile Access Matrix

Values: `allowed_when_ticket_scoped`, `approval_required`, `prohibited`, `not_applicable`.

| Profile | read | cite | summarize | classify | draft | write | validate | execute | install | authenticate | network_call | migrate | stage | commit | push | publish | promote |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Reader | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | not_applicable | not_applicable | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited |
| Researcher | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | approval_required | approval_required | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited |
| Classifier | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | not_applicable | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited |
| Architect | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | approval_required | prohibited | prohibited | prohibited | prohibited | approval_required | prohibited | prohibited | prohibited | prohibited | approval_required |
| Migration Planner | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | approval_required | prohibited | prohibited | prohibited | prohibited | approval_required | prohibited | prohibited | prohibited | prohibited | prohibited |
| Documentation Writer | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | approval_required | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | approval_required | prohibited |
| External Source Reviewer | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | approval_required | approval_required | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited |
| Product Reviewer | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | approval_required | approval_required | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited |
| Implementation Planner | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | approval_required | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited |
| Validator | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | not_applicable | approval_required | allowed_when_ticket_scoped | approval_required | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited |
| Executor | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | approval_required | prohibited | prohibited | prohibited | prohibited | approval_required | approval_required | approval_required | approval_required | prohibited |
| Subagent | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | allowed_when_ticket_scoped | approval_required | approval_required | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited |

## 18. Workspace Surface Matrix By Profile

Values: `default_read_allowed`, `ticket_scoped_read`, `ticket_scoped_write`, `approval_required`, `prohibited`, `local_only`, `never_expose`.

| Surface | Reader | Researcher | Classifier | Architect | Migration Planner | Documentation Writer | External Source Reviewer | Product Reviewer | Implementation Planner | Validator | Executor | Subagent |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `0_architecture/` | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_write | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_write | ticket_scoped_read |
| `0_architecture/workspace/` | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_write | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_write | ticket_scoped_read |
| `0_architecture/security/` | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_write | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_write | ticket_scoped_read |
| `1_research/` | ticket_scoped_read | ticket_scoped_write | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_write | ticket_scoped_read |
| `2_products/` | prohibited | prohibited | approval_required | approval_required | approval_required | prohibited | prohibited | local_only | approval_required | approval_required | approval_required | prohibited |
| `3_platform/` | prohibited | prohibited | approval_required | approval_required | prohibited | prohibited | prohibited | prohibited | ticket_scoped_read | approval_required | approval_required | prohibited |
| `4_external/` | prohibited | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | approval_required | ticket_scoped_read |
| `4_external/sources/` | prohibited | approval_required | approval_required | approval_required | prohibited | prohibited | local_only | prohibited | prohibited | prohibited | approval_required | prohibited |
| `5_workspace/` | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_write | ticket_scoped_read |
| `6_docs/` | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_write | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_read | ticket_scoped_write | ticket_scoped_read |
| `7_datasets/` | prohibited | approval_required | approval_required | prohibited | prohibited | prohibited | prohibited | approval_required | prohibited | approval_required | approval_required | prohibited |
| `8_models/` | prohibited | approval_required | approval_required | prohibited | prohibited | prohibited | prohibited | approval_required | prohibited | approval_required | approval_required | prohibited |
| `9_artifacts/` | prohibited | approval_required | approval_required | approval_required | approval_required | approval_required | prohibited | approval_required | approval_required | local_only | local_only | approval_required |
| `10_scripts/` | prohibited | prohibited | prohibited | approval_required | prohibited | prohibited | prohibited | prohibited | ticket_scoped_read | approval_required | approval_required | prohibited |
| `11_tools/` | prohibited | prohibited | prohibited | approval_required | prohibited | prohibited | prohibited | prohibited | ticket_scoped_read | approval_required | approval_required | prohibited |
| `12_tests/` | prohibited | prohibited | prohibited | ticket_scoped_read | prohibited | prohibited | prohibited | prohibited | ticket_scoped_read | ticket_scoped_write | approval_required | prohibited |
| `13_packages/` | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | ticket_scoped_read | prohibited | approval_required | prohibited |
| `14_sdk/` | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | ticket_scoped_read | prohibited | approval_required | prohibited |
| `previusknowledge/` | prohibited | approval_required | ticket_scoped_read | approval_required | local_only | prohibited | prohibited | prohibited | prohibited | prohibited | approval_required | prohibited |
| secrets/credentials | never_expose | never_expose | never_expose | never_expose | never_expose | never_expose | never_expose | never_expose | never_expose | never_expose | never_expose | never_expose |
| generated/runtime folders | prohibited | approval_required | approval_required | approval_required | approval_required | approval_required | prohibited | approval_required | approval_required | local_only | local_only | approval_required |

## 19. Sensitivity Ceiling By Profile

No agent profile receives default secret or credential access. Unknown sensitivity requires stop/escalation. Local-only access requires explicit ticket scope. Sensitive/restricted access requires minimization and escalation.

| Profile | Maximum default sensitivity access | Local-only posture | Sensitive/restricted posture | Secret/credential posture |
| --- | --- | --- | --- | --- |
| Reader | internal | Escalate unless scoped. | Stop/escalate. | never_expose |
| Researcher | internal | Explicit research/evidence scope only. | Minimize and escalate. | never_expose |
| Classifier | internal | Explicit classification scope only. | Classify metadata; escalate details. | never_expose |
| Architect | internal | Explicit architecture evidence scope only. | Minimize and cite risk, not details. | never_expose |
| Migration Planner | local_only for scoped previous evidence | Explicit migration scope only. | Escalate. | never_expose |
| Documentation Writer | internal | Exclude unless docs ticket explicitly handles local evidence safely. | Do not include sensitive details. | never_expose |
| External Source Reviewer | external_restricted for scoped source evidence | Raw source scope only. | Escalate license/security risk. | never_expose |
| Product Reviewer | product_restricted for scoped product evidence | Product ticket only. | Escalate product-sensitive material. | never_expose |
| Implementation Planner | internal | Avoid unless implementation planning explicitly scopes evidence. | Escalate. | never_expose |
| Validator | generated_sensitive for scoped validation output | Validation/debug scope only. | Report safely and escalate. | never_expose |
| Executor | local_only only when explicitly scoped | Exact task only. | Stop unless approved. | never_expose |
| Subagent | Inherited but narrower than parent | Narrow delegated scope only. | Return safe metadata and uncertainty. | never_expose |

## 20. Context Requirements By Profile

| Profile | Minimum needed context | Required authority docs | Source-status labels | Exclusions | Stop/citation/sensitivity requirements |
| --- | --- | --- | --- | --- | --- |
| Reader | Active question and directly relevant docs. | Current architecture/security docs named by task. | Required when claims depend on source status. | Local-only, product, raw external, generated, secrets. | Stop on need to edit/validate/execute; cite inspected paths. |
| Researcher | Research question, scoped evidence, current authority constraints. | W-series/S docs relevant to claim. | Required for research/evidence/external/prior material. | Secrets, credentials, raw external unless scoped. | Cite uncertainty/freshness; filter sensitive material. |
| Classifier | Target source list and classification model. | W-02/W-03/W-09/S-00/S-01 as needed. | Core output requirement. | Source mutation and broad local-only dumps. | Stop on missing status or sensitive content. |
| Architect | Target architecture file, source authority, scoped evidence. | S-00/S-01, W-09/W-10/W-11 and domain inputs. | Required for all evidence. | Product/source/code/local-only unless scoped. | Cite authority and boundaries; stop on implementation/migration need. |
| Migration Planner | Migration objective, W-02 state, W-08 controls. | W-02/W-08/W-09/S-01. | Required for every source candidate. | Wholesale corpus, product movement, external movement. | Stop before movement/archive/Git. |
| Documentation Writer | Named doc target, source authority, docs status/scope. | W-09 plus source authority docs. | Required for projected claims. | Sensitive/local-only unless approved. | Cite sources; warn if projection/stale. |
| External Source Reviewer | Source-review scope and registry/policy posture. | W-03/W-13/S-00/S-01. | External reference/restricted required. | Execution, install, auth, source copy. | Cite provenance/license/risk; stop on adoption need. |
| Product Reviewer | Product task, selected product paths, root constraints. | W-12/S-00/S-01/W-04/W-07. | Product-restricted/product-scoped required. | Product execution, product Git, root promotion. | Cite product scope and root boundary; escalate activation. |
| Implementation Planner | Planning objective, architecture constraints, blocker list. | W-series/S docs and validation/security blockers. | Required for code/evidence references. | Code writes, installs, builds, external adoption. | Stop before implementation or execution. |
| Validator | Validation objective, allowed commands, expected outputs. | Validation-related W/S docs and task instructions. | Required for artifacts/outputs. | Unscoped commands, external/product execution. | Report commands/results/skips; passing does not approve. |
| Executor | Exact allowed files/actions/commands. | Active task and relevant constraints. | Required for touched surfaces. | Anything outside exact scope. | Report changes/validation; stop after task. |
| Subagent | Narrow question and allowed paths. | Minimal source docs needed for delegated task. | Required in returned evidence. | Anything outside delegation. | Return evidence only; parent merges and validates. |

Context requirements for all profiles:

| Requirement | Rule |
| --- | --- |
| Minimum context | Use the smallest sufficient context. |
| Authority docs | Include current canonical docs relevant to the task. |
| Source-status labels | Preserve status, scope, freshness, sensitivity, and uncertainty. |
| Exclusions | Exclude secrets, credentials, unrelated local-only material, raw external trees, product source, generated dumps, and stale context unless explicitly scoped. |
| Stale-context warning | Warn when evidence may be stale, partial, generated, external, or unreviewed. |
| Local-only handling | Treat local-only as no default publication and no default Git. |

## 21. Escalation Triggers

Universal escalation triggers:

| Trigger | Required response |
| --- | --- |
| Need outside-scope read | Stop and request scope. |
| Need outside-scope write | Stop and request exact target approval. |
| Need execution | Stop and request exact command approval. |
| Need install | Stop and request dependency review/approval. |
| Need auth | Stop and request secure handling/approval. |
| Need network/provider/API | Stop and request explicit network/provider approval. |
| Need MCP | Stop and request MCP risk review/approval. |
| Secret encountered | Stop; do not expose value. |
| Credential encountered | Stop; do not expose/use value. |
| Unknown sensitivity | Treat as sensitive; classify or escalate. |
| Local-only material needed | Stop unless explicit local-only scope exists. |
| Product source needed | Stop unless explicit product scope exists. |
| Raw external source needed | Stop unless explicit source-review scope exists. |
| Migration action needed | Stop and require migration ticket/governance. |
| Git action needed | Stop and require human approval. |
| Publication needed | Stop and require publication/security review. |
| Promotion needed | Stop and require governance. |
| Substrate decision implied | Stop and require explicit Cognitive Semantic System decision. |
| Policy conflict | Follow stricter current rule and escalate. |

Profile-specific escalation examples:

| Profile | Escalate when |
| --- | --- |
| Reader | Any write, validation, execution, Git, local-only, or sensitive need appears. |
| Researcher | Evidence requires external execution, product source, sensitive data, or promotion. |
| Classifier | Classification would mutate source or imply promotion/migration. |
| Architect | Architecture work requires implementation, product activation, dependency adoption, or substrate decision. |
| Migration Planner | Planning reaches movement, archive, deletion, copy, or first-batch execution. |
| Documentation Writer | Doc would expose sensitive/local-only material or imply canonical authority without governance. |
| External Source Reviewer | Review requires running, installing, authenticating, copying, or adopting source. |
| Product Reviewer | Review requires product execution, Git posture change, activation, or publication. |
| Implementation Planner | Plan requires code edit, build, package, SDK, or dependency install. |
| Validator | Validation command is unscoped, unsafe, networked, external/product execution, or produces sensitive output. |
| Executor | Any side effect, file, command, or next action exceeds exact scope. |
| Subagent | Delegated scope is too broad or asks for prohibited action. |

## 22. Output Obligations By Profile

Universal response/report obligations when relevant:

| Obligation | Requirement |
| --- | --- |
| Files inspected | Report files or surfaces inspected for architecture, review, validation, or edits. |
| Files created/modified | Report exact paths created/modified. |
| Commands run | Report commands run; do not hide skipped/blocked commands. |
| Validation results | Report pass/fail/skipped/blocked and residual risks. |
| Scope limits | State important allowed/forbidden scope boundaries. |
| Citations | Cite source authority or evidence for material claims. |
| Uncertainty | State uncertainty, stale evidence, partial inspection, or unresolved conflicts. |
| Blockers | Report blockers without bypassing them. |
| Prohibited actions avoided | State if relevant high-risk actions were intentionally not performed. |
| Stop-rule compliance | Confirm stop when ticket requires it. |
| Next-ticket recommendation | Provide only when useful; do not start next ticket. |

Profile output expectations:

| Profile | Expected output |
| --- | --- |
| Reader | Answer, summary, file references, uncertainty. |
| Researcher | Findings, comparisons, uncertainty, citations, recommendations. |
| Classifier | Classification table, source status, scope, risks, unresolved labels. |
| Architect | Architecture doc/proposal, rationale, constraints, citations, validation notes. |
| Migration Planner | Plan, source/target mapping, blockers, validation/governance preconditions. |
| Documentation Writer | Named doc/projection with status/scope/citations where applicable. |
| External Source Reviewer | Source review, provenance/license/security risk, blockers. |
| Product Reviewer | Product-scope findings, boundary risks, root-impact notes. |
| Implementation Planner | Implementation plan, dependencies, blockers, required validation/security. |
| Validator | Commands run, outputs, pass/fail posture, residual risks. |
| Executor | Completed scoped action, changed files, validation results, side effects, stop compliance. |
| Subagent | Evidence, paths, uncertainty, conflicts, validation notes. |

## 23. Agent Access Invariants

| Invariant | Rule |
| --- | --- |
| AGENT-ACCESS-001 | Profiles restrict; they do not expand scope. |
| AGENT-ACCESS-002 | Active ticket controls actual permissions. |
| AGENT-ACCESS-003 | Context is not permission. |
| AGENT-ACCESS-004 | Tool availability is not permission. |
| AGENT-ACCESS-005 | Read profile is not write profile. |
| AGENT-ACCESS-006 | Write profile is not execution profile. |
| AGENT-ACCESS-007 | Validator does not approve. |
| AGENT-ACCESS-008 | Executor does not govern. |
| AGENT-ACCESS-009 | Subagent output is evidence only. |
| AGENT-ACCESS-010 | Git history is human-gated. |
| AGENT-ACCESS-011 | Secrets and credentials require stop/escalation. |
| AGENT-ACCESS-012 | Product access is product-scoped only. |
| AGENT-ACCESS-013 | External source access is evidence-only. |
| AGENT-ACCESS-014 | Migration planning is not migration execution. |
| AGENT-ACCESS-015 | Cognitive substrate remains undecided. |

## 24. Agent Access Anti-patterns

| Anti-pattern | Why it is wrong |
| --- | --- |
| role means permission | Role describes posture; active ticket and approvals still control access. |
| context dump | Broad context exposes irrelevant, local-only, sensitive, or stale material. |
| subagent as approver | Subagents return evidence only. |
| validator as governance | Validation evaluates; governance decides. |
| executor as owner | Execution does not create ownership or approval. |
| reader edits because file is visible | Read visibility is not write permission. |
| architect implements | Architecture planning does not authorize code. |
| reviewer adopts dependency | Review evidence is not adoption approval. |
| product reviewer activates product | Product activation requires product/governance approval. |
| migration planner moves files | Planning is not execution. |
| external reviewer runs source code | External execution is blocked by default. |
| generated output as validation | Generated output is evidence, not proof by itself. |
| passing validation as commit approval | Passing checks does not authorize Git history. |
| git add . | Broad staging can include local-only or sensitive material. |
| previous canonical label as current authority | Prior status labels are historical until restated/promoted. |
| graph evidence as substrate decision | Graph evidence does not decide the Cognitive Semantic System substrate. |

## 25. Remaining Gaps

S-02 does not solve:

| Gap | Status |
| --- | --- |
| Enforcement engine | Not implemented. |
| Role-based access implementation | Not implemented. |
| Permission schemas | Not created. |
| Shell/network/MCP policy details | Not specialized beyond default blocks. |
| Secrets manager | Not implemented. |
| Provider auth implementation | Not implemented. |
| Validation registry | Not implemented. |
| Product charters | Not created. |
| External dependency approvals | None granted. |
| Implementation readiness | Not achieved. |
| Cognitive Semantic System implementation | Not implemented; substrate remains undecided. |

## 26. Readiness For S-03

Readiness assessment:

| Next phase | Readiness | Rationale |
| --- | --- | --- |
| `S-03 - Local-only / Secrets / Credentials Policy` | Ready after explicit instruction. | S-00 defines sensitivity/security, S-01 defines access surfaces/actions, and S-02 defines agent profile behavior. S-03 can specialize ignored files, local-only material, secrets, credentials, `.env` files, provider auth, sensitive files, and exposure minimization. |

S-03 should consume:

| Input | Why it matters |
| --- | --- |
| S-00 | Security/access definitions and sensitivity model. |
| S-01 | Workspace surfaces, access actions, local-only model, and escalation. |
| S-02 | Agent-specific behavior and role ceilings. |
| W-10 | Agent operating and stop rules. |
| W-05 | Context exclusions and sensitivity-aware context. |
| W-04/W-07 | Local-only topology and responsibility posture. |
| W-12/W-13 | Product and external-source local-only/security boundaries. |
| `.gitignore` | Current ignored secrets, credentials, products, external sources, datasets, models, artifacts, runtime, dependency, and previous-knowledge patterns. |

Do not create S-03 from this ticket.

## 27. Final Verdict

| Question | Answer |
| --- | --- |
| What agent profiles now exist? | Reader, Researcher, Classifier, Architect, Migration Planner, Documentation Writer, External Source Reviewer, Product Reviewer, Implementation Planner, Validator, Executor, and Subagent. |
| What is allowed by role? | Ticket-scoped discover/read/cite/summarize/classify/draft/propose/write/validate according to each role's profile and active task scope. |
| What is prohibited by role? | Unapproved execution, install, authentication, network/provider/API calls, MCP activation, migration execution, deletion, movement, rename, archive, broad reads, local-only exposure, product activation, external adoption, Git history changes, publication, promotion, and substrate decisions. |
| What requires escalation? | Any need outside scope, sensitive/local-only/unknown material, secrets/credentials, execution, install, auth, network/provider/API/MCP, migration action, product activation, external adoption, publication, promotion, Git action, policy conflict, or substrate implication. |
| What requires human approval? | Stage, commit, push, delete, move, rename, migration execution, archive creation, external execution, dependency adoption, authentication, network/provider/API calls, MCP activation, product activation, publication, authority promotion, security exceptions, and final Cognitive Semantic System substrate decision. |
| What should S-03 consume? | S-00, S-01, S-02, W-10, W-05, W-04/W-07, W-12, W-13, `.gitignore`, and current local-only/security findings. |

Final statement:

```text
S-02 defines concrete agent access profiles for AGENT PLATFORM. It restricts each
agent role by allowed surfaces, actions, sensitivity ceiling, context requirements,
citations, validation permissions, Git posture, execution posture, escalation,
outputs, and stop rules. It does not implement enforcement or authorize S-03,
execution, migration, implementation, product activation, external adoption,
publication, staging, commit, push, or substrate decisions.
```

Stop rule:

```text
After S-02, stop. Do not start S-03, S-04, S-A, V-00, implementation, migration,
product activation, external adoption, staging, commit, push, or any other next
ticket without explicit user instruction.
```
