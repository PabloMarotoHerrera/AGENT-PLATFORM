# AGENT PLATFORM Existing Harness Boundary Review

## 1. Document Header
Title: AGENT PLATFORM Existing Harness Boundary Review  
Ticket: H-01  
Status: Accepted boundary review  
Date: 2026-06-30  
Scope: Existing harness-related references in approved architecture documents before H-02 Semantic Meta-Harness Architecture  
Authority: boundary review only, not implementation authorization  
Related documents: H-00, W-series, S-series, V-series, CSS-series

## 2. Purpose
H-01 follows H-00. H-00 selected the harness strategy path: retain harness material as bounded evidence, do not adopt or execute existing harnesses, and prepare H-02 after boundary review. H-01 reviews existing harness boundaries, prepares H-02, and does not implement, execute, adopt, or start H-02.

## 3. Review Scope
| Scope class | In scope | Out of scope |
| --- | --- | --- |
| Sources | Approved architecture documents only. | Source-code review and local-only deep inspection. |
| References | Harness, orchestration, agent-runtime, handoff, tool/provider/MCP, OpenCode/operator-tool, external/product/generated/migration references. | Runtime design or implementation design. |
| Boundaries | Validation, security, governance, migration, product, external-source, CSS substrate neutrality. | Execution, adoption, provider/MCP activation, product activation, migration execution, dependency install. |

## 4. Review Method
Method: bounded read-only document inspection, bounded keyword search in approved architecture directories, source-status classification, boundary classification, evidence retention classification, blocker classification, and H-02 readiness assessment.

Boundary review evidence is evidence, not approval.

## 5. Harness Reference Definition
A harness reference is any approved-document mention of harness, orchestration, agent runtime, subagent, handoff, command execution, tool execution, provider adapter, MCP, shell/network boundary, OpenCode/operator-tool usage, external harness source, product harness code, runtime policy, context assembly runtime, validation execution surface, or generated harness output.

A reference is not adoption, authority, execution permission, or implementation readiness.

## 6. Discovery Terms
Discovery terms: harness, orchestration, runtime, agent runtime, subagent, handoff, OpenCode, opencode, MCP, provider, adapter, tool execution, shell, command boundary, context pack, context assembly, validation execution, generated output, external harness, semantic meta-harness.

## 7. Existing Harness Reference Inventory
| Reference group | Source document/path | Source status | Observed meaning | Boundary classification | Allowed use | Blocked use | Evidence requirement | H-02 relevance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H-00 strategy | `0_architecture/harness/agent_platform_harness_strategy_decision.md` | Accepted strategy | Retain evidence, defer implementation, H-01 -> H-02 -> H-A. | strategy_reference | Guide H-02 scope. | Runtime adoption. | H-00 citation. | Primary input. |
| W-series agent/context | W-06, W-10, W-11, W-14 | Canonical workspace | Agents, context packs, subagents, handoff, coordination, stop rules. | pattern_candidate | Architecture requirements. | Authority or execution. | W citations. | High. |
| S-series execution | S-00 through S-04, S-A | Canonical security/access | Tool, shell, provider, API, MCP, package, execution gates. | security_constraint | H-02 constraints. | Permission by availability. | S citations. | High. |
| V-series validation | V-00, V-02, V-05, V-A | Canonical validation | Command output, evidence, verdict, external-source validation. | validation_constraint | Evidence model. | Approval by output. | V citations. | High. |
| CSS-series | CSS-00, CSS-01, CSS-02, CSS-A | Accepted CSS architecture | Cognitive Semantic System name and substrate neutrality. | governance_reference | Keep substrate-neutral. | Harness selects substrate. | CSS citations. | High. |
| External harness refs | W-03, W-13, V-05 | External evidence | `opencode`, `pi`, `tau`, `ECC-main`, `hermes-agent`, gateways. | external_reference | Pattern review only. | Execute/install/copy/adopt. | W-03/W-13/V-05. | High, bounded. |
| Product harness refs | W-12, V-04 | Product policy/evidence | Product-specific tooling or dependencies. | product_scoped_reference | Requirements signal. | Root harness authority. | W-12/V-04. | Medium. |
| OpenCode/operator usage | H-00, W-06, W-10, W-03, W-14 | Operator/external evidence | Useful observed coding-agent/operator pattern. | operator_tool_reference | Bounded requirements evidence. | Platform authority. | Source-status citation. | Medium-high. |
| Generated outputs | V-02, W-11, W-14, S-04 | Generated evidence | Logs, command output, reports, projections, tool output. | generated_evidence | Provenance-aware evidence. | Truth/source. | V-02 metadata. | High. |
| Prior harness refs | W-02, W-08 | Migration evidence | Prior provider/harness research and conflicted semantic refs. | bounded_evidence | Cite safe metadata. | Migration/current authority. | W-02/W-08. | Medium. |

## 8. Boundary Classification Model
| Classification | Meaning | Allowed use | Blocked use | Next action |
| --- | --- | --- | --- | --- |
| bounded_evidence | Source/status known evidence. | Cite as support. | Authority/adoption. | H-02 input. |
| pattern_candidate | Abstracted useful idea. | Compare/design later. | Code reuse. | H-02 evaluate. |
| strategy_reference | Accepted strategy statement. | Constrain H-02. | Implementation. | Preserve. |
| governance_reference | Decision/authority boundary. | Decision constraint. | Runtime approval. | Preserve. |
| security_constraint | S-series blocker/gate. | H-02 requirement. | Bypass. | Preserve. |
| validation_constraint | V-series evidence/proof rule. | Evidence model. | Approval. | Preserve. |
| external_reference | External source evidence. | Pattern review. | Adopt/copy/run. | H-02 cite only. |
| product_scoped_reference | Product-only evidence. | Product requirement signal. | Root authority. | Defer product. |
| generated_evidence | Output/projection/log. | Review with provenance. | Truth/source. | Retain summary. |
| operator_tool_reference | Operator/tool behavior evidence. | Requirements signal. | Platform authority. | Bound in H-02. |
| blocked_execution_surface | Execution mentioned. | Risk model. | Run now. | S-04 gate. |
| blocked_dependency_surface | Package/dependency mentioned. | Risk model. | Install/adopt. | Dependency review later. |
| blocked_provider_surface | Provider/API/auth mentioned. | Boundary model. | Provider use. | Provider policy later. |
| blocked_mcp_surface | MCP mentioned. | Boundary model. | Activation. | MCP policy later. |
| blocked_migration_surface | Migration implied. | Blocker record. | Migrate. | V-03/CSS-02 later. |
| rejected_for_current_use | Unsafe as current posture. | Historical trace. | Current use. | Reconsider by governance. |
| deferred_to_H-02 | Architecture topic. | H-02 input. | Build now. | H-02. |
| deferred_to_IR-00 | Implementation topic. | Readiness blocker. | Implementation now. | IR-00 later. |

## 9. Prior / Internal Harness Material Boundary
Prior/internal harness material is historical or bounded evidence only. No prior harness becomes platform runtime authority, is migrated by H-01, is executed, or overrides H-00. Useful concepts may become pattern candidates after citation and boundary classification.

## 10. OpenCode / Operator Tool Boundary
OpenCode usage is operator-tool usage. OpenCode behavior is not AGENT PLATFORM authority. Loops, failures, prompts, and tickets can be operational evidence, but they are not runtime architecture and do not define governance, validation, security, or harness behavior. OpenCode may inform H-02 only as bounded evidence.

## 11. External Harness Boundary
Under W-13 and V-05, external harnesses remain external evidence. External code is not copied. Setup guides and external AGENTS.md or equivalent instructions are inactive evidence. Dependency graphs are not approved. External names do not name AGENT PLATFORM systems. Pattern extraction requires abstraction, citation, validation, security review, and governance.

## 12. Product Harness Boundary
Under W-12 and V-04, product harness code remains product-scoped/local-only. Product behavior does not define root harness. Product tests/builds/execution remain blocked. Product dependencies remain product-scoped. Product generated outputs are generated evidence. Product needs may inform H-02 requirements but cannot decide root architecture.

## 13. Tool / Provider / MCP Boundary
Under S-04: tool availability is not permission; shell availability is not command approval; provider credentials are not provider permission; network availability is not network permission; MCP availability is not MCP activation; package manager availability is not dependency approval. Future harness must treat these as gated surfaces.

## 14. Agent Runtime / Handoff Boundary
Agents may propose within scope. Active ticket controls scope. Agent profile constrains access. Context inclusion is not permission. Handoff is not approval. Agent coordination is not governance. Autonomous execution is blocked by default. Future runtime architecture must preserve stop rules.

## 15. Context / Validation Boundary
Context packs expose selected material only and do not grant execution/read/write authority. Harness output is evidence. Command output requires metadata and sensitivity review. Validation evaluates harness outputs. Proof cannot be inflated by harness assertion. Failed, skipped, and blocked actions must remain visible.

## 16. Cognitive Semantic System Boundary
Cognitive Semantic System is the future semantic authority concept. Harness is orchestration strategy. Harness does not decide CSS substrate. Graph remains a candidate only. Harness may later consume CSS records, context, validation, and governance states, while staying substrate-neutral until governed otherwise.

## 17. Governance Boundary
Harness does not approve actions, promote artifacts, decide authority, activate products, or adopt dependencies. Harness can prepare evidence for governance. Governance decisions remain explicit and human-owned.

## 18. Migration Boundary
H-01 does not execute migration. There is no file movement, copy, rename, delete, archive, previous knowledge rewrite, or wholesale migration. Harness-related material may inform later migration only through V-03/CSS-02 controls. M-02 is not started.

## 19. Evidence Retention Model
Using V-02: prefer references over copied content, safe metadata over local-only material, no secret/credential values, bounded summaries over raw outputs, scoped external/product/local-only references, and clear limitations. Discovery findings are evidence, not approval.

## 20. Harness Boundary Matrix
| Reference | Current boundary | Allowed use | Blocked use | Required evidence | Next ticket |
| --- | --- | --- | --- | --- | --- |
| Prior/internal harness material | bounded_evidence | Cited concepts | Authority/migration | W-02/W-08/CSS-02 | H-02 input |
| OpenCode/operator usage | operator_tool_reference | Requirements signal | Platform authority | H-00/W-10/W-03 | H-02 input |
| External harness projects | external_reference | Pattern candidate | Execute/install/adopt/copy | W-03/W-13/V-05 | H-02 input |
| MCP references | blocked_mcp_surface | Risk model | Activation | S-04/V-05 | H-02 constraint |
| Provider/adapter references | blocked_provider_surface | Boundary model | Auth/provider lock-in | W-01/S-04/W-13 | H-02 constraint |
| Tool/shell/command refs | blocked_execution_surface | Command policy | Run commands | S-04/V-00/V-02 | H-02 constraint |
| Agent handoff/runtime refs | pattern_candidate | Stop-rule design | Approval/autonomy | W-06/W-10/S-02 | H-02 input |
| Context assembly refs | validation_constraint | Context requirements | Permission | W-05/W-06/V-02 | H-02 input |
| Validation execution refs | validation_constraint | Evidence model | Approval/proof inflation | V-series/S-04 | H-02 input |
| Product harness code | product_scoped_reference | Product signal | Root harness | W-12/V-04 | Defer product |
| Generated harness outputs | generated_evidence | Reviewed evidence | Truth/source | V-02 | H-02 caveat |
| Future semantic meta-harness | deferred_to_H-02 | Architecture planning | Implementation | H-00/H-01 | H-02 |

## 21. Pattern Candidate Register
| ID | Pattern | Source reference | Why useful | Required caveat | H-02 relevance | Blocker |
| --- | --- | --- | --- | --- | --- | --- |
| PC-001 | Harness/session/frontend separation | W-03/W-13/H-00 | Separates runtime, UI, and session evidence. | External evidence only. | High | Source review. |
| PC-002 | Event/command result as evidence contract | W-03/V-00/V-02/S-04 | Supports traceable execution evidence. | No execution now. | High | Command policy. |
| PC-003 | Provider-neutral adapter boundary | W-01/W-13/S-04 | Avoids provider lock-in. | No provider activation. | High | Provider policy. |
| PC-004 | Context pack as selected exposure | W-05/W-06/W-14 | Keeps context from becoming permission. | Context not authority. | High | Context format later. |
| PC-005 | Subagent/handoff returns evidence only | W-06/W-10/S-02/W-11 | Preserves stop rules and authority. | Handoff not approval. | High | Governance workflow. |
| PC-006 | Semantic meta-harness path | H-00 | Future target architecture concept. | Not implementation. | Primary | H-02 required. |

## 22. Rejected / Deferred Register
| Topic | Reason | Future ticket | Blocker status |
| --- | --- | --- | --- |
| Existing harness as current authority | Violates H-00 and governance. | None unless reopened | Rejected. |
| Execution surfaces | S-04 blocks by default. | IR/security later | Blocked. |
| External adoption | W-13/V-05 require review. | External review/governance | Blocked. |
| Full meta-harness design | Belongs to H-02. | H-02 | Deferred. |
| Runtime implementation | Requires IR-00 and audits. | IR-00 | Deferred. |
| Provider/MCP activation | Requires policy and approval. | Future provider/MCP ticket | Blocked. |
| Product harness promotion | Product-root collapse risk. | Product ticket | Blocked. |
| Migration of prior material | Requires V-03/CSS-02 controls. | M-02 or later | Blocked. |

## 23. Risk Register
| Risk | Severity | Current control | Required mitigation | Blocker? |
| --- | --- | --- | --- | --- |
| External harness adoption by proximity | High | H-00/W-13/V-05 | H-02 citations only | Yes |
| Operator tool mistaken as authority | High | W-06/W-10/H-00 | Operator boundary | Yes |
| Provider/API lock-in | High | S-04/W-13 | Provider-neutral architecture | Yes |
| MCP activation by config | High | S-04 | MCP gate | Yes |
| Package-manager execution | High | S-04/W-13 | Dependency review | Yes |
| Product-root collapse | High | W-12/V-04 | Product boundary | Yes |
| Graph/substrate coupling | High | CSS-series | Substrate neutrality | Yes |
| Migration by harness | High | W-08/V-03 | Migration ticket only | Yes |
| Validation bypass | High | V-series | Evidence model | Yes |
| Security bypass | High | S-series | Stop rules | Yes |
| Governance bypass | High | W-11 | Human-owned decisions | Yes |
| Local-only leakage | High | S-03/.gitignore | Safe metadata | Yes |
| Secret/credential exposure | High | S-03/S-04 | Stop/escalate | Yes |
| Generated output as truth | Medium-high | V-02 | Provenance labels | Yes |
| Agent autonomy before approval | High | W-10/S-02 | Scope gates | Yes |
| Prompt/ticket text as runtime behavior | Medium-high | W-10/H-00 | Strategy vs runtime boundary | Yes |

## 24. Blocker Register
| Blocker | Stop behavior | Required action | Blocks H-02? | Blocks implementation? |
| --- | --- | --- | --- | --- |
| Unclassified harness reference | Do not use. | Classify in H-02 input notes. | Maybe | Yes |
| Missing source reference | Do not cite. | Add citation or defer. | Maybe | Yes |
| External adoption implied | Stop claim. | Restore external evidence posture. | Yes | Yes |
| Execution implied | Stop action. | S-04 approval path later. | No | Yes |
| Dependency install implied | Stop action. | Dependency review later. | No | Yes |
| Provider/network/API implied | Stop action. | Provider policy later. | No | Yes |
| MCP activation implied | Stop action. | MCP policy later. | No | Yes |
| Product-root collapse | Stop claim. | Scope to product. | Yes | Yes |
| Local-only leakage | Stop exposure. | Safe metadata. | Yes | Yes |
| Secret/credential risk | Stop immediately. | Secure handling. | Yes | Yes |
| Validation bypass | Stop verdict. | V-series mapping. | Yes | Yes |
| Governance bypass | Stop authority claim. | Governance decision path. | Yes | Yes |
| Substrate assumption | Stop design claim. | Restore neutrality. | Yes | Yes |
| Implementation implied | Stop scope. | Defer to IR-00. | No | Yes |
| Migration implied | Stop scope. | V-03/CSS-02/M-ticket later. | Maybe | Yes |

## 25. H-02 Input Requirements
H-02 may consume: H-00 strategy, H-01 boundary classifications, pattern candidates, blocker register, security constraints, validation/evidence requirements, governance boundaries, and CSS substrate-neutrality constraints.

H-02 must not consume as authority: external harness code, product code, OpenCode behavior, raw generated outputs, unclassified prior material, local-only content beyond safe metadata, provider/MCP configs, or dependency manifests as adoption approval.

## 26. H-02 Readiness Assessment
H-02 - Semantic Meta-Harness Architecture is ready after explicit instruction because H-01 classified existing references, no blocker prevents architecture planning, no execution/adoption/implementation is implied, strategy remains substrate-neutral, and security/validation/governance boundaries remain intact. Do not create H-02.

## 27. H-A Readiness Assessment
H-A is not ready until H-02 completes. Do not create H-A.

## 28. Boundary Review Verdict
| Question | Verdict |
| --- | --- |
| What existing harness material was reviewed? | Approved-doc references in H, W, S, V, CSS architecture docs plus `.gitignore`/README posture. |
| Boundary status? | Bounded evidence, pattern candidates, constraints, or blocked/deferred surfaces. |
| Are existing harnesses adopted? | No. |
| Is OpenCode platform authority? | No. |
| Are external harnesses adopted? | No. |
| Are provider/MCP/package-manager surfaces activated? | No. |
| Are product harnesses promoted to root? | No. |
| Was any harness implemented or executed? | No. |
| Is H-02 ready after explicit instruction? | Yes, as architecture only. |

## 29. H-01 Invariants
| ID | Invariant |
| --- | --- |
| H01-001 | Boundary review is not harness implementation. |
| H01-002 | Boundary review is evidence, not approval. |
| H01-003 | Existing harness material is bounded evidence only. |
| H01-004 | External harnesses remain external evidence. |
| H01-005 | OpenCode is not platform authority. |
| H01-006 | Product harness material remains product-scoped. |
| H01-007 | Tool availability is not permission. |
| H01-008 | Provider credentials are not provider permission. |
| H01-009 | MCP availability is not MCP activation. |
| H01-010 | Package manager availability is not dependency approval. |
| H01-011 | Harness does not govern. |
| H01-012 | Harness outputs are evidence. |
| H01-013 | Cognitive Semantic System substrate remains undecided. |
| H01-014 | Graph remains a candidate only. |
| H01-015 | Implementation remains blocked. |

## 30. Anti-patterns
Anti-patterns: adopting harness by mention, external clone, README, OpenCode behavior, MCP config, provider credential, or package manifest; implementing harness inside boundary review; treating handoff as approval; treating agent coordination as governance; product harness as root harness; generated output as truth; validation bypass by harness; security bypass by harness; migration by boundary review; graph substrate assumption; `git add .`.

## 31. Remaining Gaps
No H-02 meta-harness architecture, H-A audit, harness implementation, runtime model, provider adapter strategy, MCP activation strategy, tool execution implementation, validation registry implementation, security enforcement implementation, dependency approval registry, product activation, external adoption, implementation readiness, or final Cognitive Semantic System substrate decision exists.

## 32. Recommended Next Step
Recommended next ticket only: H-02 - Semantic Meta-Harness Architecture.

H-02 should define the target harness architecture using H-00 and H-01 outputs while preserving Security/Access, Validation, Governance, CSS substrate neutrality, product boundaries, and external-source boundaries. Do not create H-02.

## 33. Final Stop Rule
After completing H-01, stop. Do not start H-02, H-A, implementation, migration, product activation, external adoption, dependency installation, authentication, network/provider/API/MCP activity, Git staging, commit, push, local-only deep inspection, or any next ticket.
