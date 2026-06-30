# AGENT PLATFORM Harness Strategy Decision

## 1. Document Header
Title: AGENT PLATFORM Harness Strategy Decision  
Ticket: H-00  
Status: Accepted strategy decision  
Date: 2026-06-30  
Scope: Harness strategy before migration, implementation, runtime design, provider integration, MCP integration, product activation, or external adoption  
Authority: strategy decision only, not implementation authorization  
Related documents: W-series, S-series, V-series, CSS-series

## 2. Purpose
H-00 follows CSS-A. Workspace, Security/Access, Validation, and CSS decision framing are complete at document level. H-00 decides the harness strategy before runtime, implementation, migration, or product work. H-00 does not implement or execute harnesses, adopt external tools or dependencies, or start H-01, H-02, or H-A.

## 3. Harness Definition
A harness is the governed orchestration surface that may later coordinate agents, context packs, validation, tool execution, provider adapters, command boundaries, handoffs, runtime policies, and output generation.

Harness is not the Cognitive Semantic System, governance, validation, security, product runtime, external source authority, or implementation by default.

## 4. Problem Statement
AGENT PLATFORM has prior and external harness-related material, but no governed strategy deciding whether that material should be retained, replaced, bounded, deferred, or used only as evidence.

Risks: importing old assumptions, external harness adoption by proximity, treating OpenCode or other tools as platform authority, confusing agent runtime with governance, bypassing Security/Access or Validation, hard-coding providers/MCP/shell/network/package managers, coupling harness strategy to graph substrate, product-root collapse, and implementation before readiness.

## 5. Strategy Decision
Accepted strategy:

| Decision | H-00 result |
| --- | --- |
| Existing harness-related material | Retain as bounded evidence only. |
| Existing harness authority | Do not adopt any as AGENT PLATFORM runtime authority. |
| Harness execution | Do not execute harness material. |
| H-00 implementation | Do not implement harness in H-00. |
| Future path | H-01 Existing Harness Boundary Review, then H-02 Semantic Meta-Harness Architecture. |
| Audit | H-A Harness Strategy Audit before implementation readiness. |

H-00 selects a strategy path, not a harness implementation.

## 6. Decision Drivers
Drivers: preserve AGENT PLATFORM root authority; preserve Cognitive Semantic System substrate neutrality; prevent external harness adoption by proximity; prevent old harness authority leakage; preserve Security/Access, Validation, and Governance boundaries; allow harness concepts as evidence; avoid implementation before IR-00; avoid provider/network/MCP/package-manager lock-in; support future local-first controlled implementation.

## 7. Harness Strategy Options Considered
| Option | Decision | Reason | Risk | Consequence |
| --- | --- | --- | --- | --- |
| A. Adopt existing harness material as runtime foundation now. | Rejected | Too early; imports unreviewed execution/dependency/provider assumptions. | High authority/security risk. | No runtime adoption. |
| B. Reject all prior/external harness material. | Rejected | Discards useful evidence. | Loss of patterns. | Retain evidence instead. |
| C. Retain harness material as bounded evidence and defer implementation. | Accepted | Preserves value while blocking unsafe adoption. | Requires later review. | Current H-00 strategy. |
| D. Design a semantic meta-harness later after boundary review. | Accepted as future path | Fits cognitive workspace and governance model. | Premature if done before H-01. | H-02 after H-01. |
| E. Use product-specific harnesses first. | Rejected current scope | Product-root collapse risk. | Root strategy could fragment. | Products remain scoped. |
| F. Let OpenCode or external tools define platform harness behavior. | Rejected | Operator tools and external sources are evidence, not authority. | External authority contamination. | Platform strategy remains governed. |

## 8. Harness Boundary Model
| Layer | Role | Harness boundary |
| --- | --- | --- |
| Governance | Decides. | Harness does not approve. |
| Security | Constrains. | Harness cannot bypass S-series. |
| Validation | Evaluates. | Harness output is evidence. |
| Evidence | Supports. | Evidence is not authority. |
| Cognitive Semantic System | May later provide semantic authority/context eligibility. | Harness must not decide CSS substrate. |
| Harness | May later orchestrate scoped operations. | Orchestration is not governance. |
| Agents | Propose/execute only within approved scope. | No autonomous authority. |
| Tools | Capabilities. | Tool availability is not permission. |
| Providers/MCP/network | Blocked by default. | Activation requires governance/security. |
| Git | Records artifacts. | Git is not semantic truth. |
| Products | Product-scoped. | Product harnesses do not define root. |
| External sources | Evidence. | Not internal authority. |

## 9. Existing Harness Material Posture
Current posture: previous harness material is historical/evidence only; external harness sources are external evidence only; product harness code is product-scoped/local-only; generated harness outputs are generated evidence; OpenCode usage is operator tool usage, not AGENT PLATFORM authority; MCP references, provider adapters, and shell/tool execution are blocked unless governed later or exact approval exists.

## 10. External Harness Source Handling
Under W-13 and V-05: external harness code is not adopted; external instructions are inactive evidence; README/setup commands are not executable instructions; dependency graphs are not approved; package install, provider/API/network/MCP use, source-code copying, and external name adoption are blocked. Pattern extraction requires citation, abstraction, validation, and governance.

## 11. Agent Runtime Boundary
Future agent runtime constraints: no autonomous execution by default; active ticket controls scope; agent profile constrains access; context inclusion is not permission; shell/network/provider/MCP availability is not permission; execution, write, migration, product activation, external adoption, and Git actions require approval; agent outputs require validation/governance before promotion.

## 12. Tool / Provider / MCP Boundary
Tool availability is not permission. Shell availability is not command approval. Network availability is not network permission. Provider credentials are not provider permission. MCP availability is not MCP activation. Package manager availability is not dependency adoption. Harness strategy must gate every tool/provider/MCP surface explicitly.

## 13. Relationship To Cognitive Semantic System
Cognitive Semantic System is the future semantic authority concept. Harness is a future orchestration/runtime strategy. Harness must not decide CSS substrate or store truth by itself. Harness may later consume CSS records, context packs, validation states, and governance decisions. CSS substrate remains undecided. Graph remains a candidate only. Rejected/prohibited naming examples such as Platform Graphify, Graphify Authority, and Graphify owns truth remain rejected/prohibited examples only.

## 14. Relationship To Validation
Harness outputs are evidence, not approval. Harness execution results require command metadata. Harness validations must map to V-series proof/evidence/verdict models. Failed, skipped, and blocked actions remain visible. Harness cannot elevate proof level by assertion. H-A audit is required before implementation readiness.

## 15. Relationship To Security / Access
S-series dominates harness behavior: no execution by default; no secret/credential exposure; unknown sensitivity escalates; local-only has no default publication; product/external/local-only surfaces use safe metadata by default; harness must support incident handling and stop rules.

## 16. Relationship To Governance
Harness does not approve actions, promote artifacts, decide authority, activate products, or adopt dependencies. Harness can prepare evidence for governance. Governance decisions remain explicit and human-owned.

## 17. Relationship To Migration
Harness strategy does not execute migration. Prior harness material may inform later migration only through V-03 and CSS-02 controls. No wholesale migration, file movement, copy, rename, delete, archive, or previous knowledge rewrite occurs. H-00 does not start M-02.

## 18. Relationship To Products
Product harness code remains product-scoped. Product needs may inform harness criteria but cannot define root harness. Product execution/tests/builds, product activation, and product dependencies remain blocked unless later governed.

## 19. Relationship To External Sources
External harnesses remain external evidence. External harness names do not become internal names. External instructions remain inactive. External execution/adoption remains blocked. Pattern extraction requires H-01, V-05, and governance.

## 20. Harness Decision Matrix
| Material | Current status | Allowed use | Blocked use | Evidence requirement | Next ticket |
| --- | --- | --- | --- | --- | --- |
| Prior internal harness material | Historical/evidence. | Cite/restatement planning. | Current authority/migration. | W-02/W-08/V-03/CSS-02. | H-01. |
| OpenCode/operator usage | Operator tool usage. | Observed pattern evidence. | Platform authority. | W-10/S-04/V-05. | H-01. |
| External harness projects | External evidence. | Pattern review. | Execute/install/adopt/copy. | W-03/W-13/V-05. | H-01. |
| MCP references | Blocked candidate. | Risk/architecture evidence. | Activation/config authority. | S-04/V-05. | H-01/H-02. |
| Provider/adapter references | Blocked candidate. | Boundary evidence. | Provider lock-in/auth use. | S-04/W-13/V-05. | H-01/H-02. |
| Product harness code | Product-scoped/local-only. | Product evidence only. | Root harness. | W-12/V-04/S-series. | H-01. |
| Generated harness outputs | Generated evidence. | Reviewed summaries. | Truth/source. | V-02 provenance. | H-01. |
| Future semantic meta-harness | Future strategy path. | Architecture after H-01. | Implementation now. | H-01 findings. | H-02. |

## 21. Harness Risk Register
| Risk | Severity | Current control | Required mitigation | Blocker? |
| --- | --- | --- | --- | --- |
| External harness adoption by proximity | High | W-13/V-05 | H-01 review and governance | Yes |
| Operator tool mistaken as authority | High | W-06/W-10 | Boundary statement | Yes |
| Provider/API lock-in | High | S-04 | Provider-neutral H-02 | Yes |
| MCP activation by config | High | S-04 | Explicit MCP policy path | Yes |
| Package-manager execution | High | S-04/W-13 | Dependency review | Yes |
| Product-root collapse | High | W-12/V-04 | Product boundary review | Yes |
| Graph/substrate coupling | High | CSS-00/CSS-01/CSS-A | Substrate-neutral H-02 | Yes |
| Migration by harness | High | W-08/V-03 | Migration ticket only | Yes |
| Validation bypass | High | V-series | Harness evidence mapping | Yes |
| Security bypass | High | S-series | Enforcement/readiness later | Yes |
| Governance bypass | High | W-11 | Decision workflow | Yes |
| Local-only leakage | High | `.gitignore`/S-03 | Safe metadata and stop rules | Yes |
| Secret/credential exposure | High | S-03/S-04 | No value handling | Yes |
| Generated output treated as truth | Medium-high | V-02 | Provenance labels | Yes |
| Agent autonomy before approval | High | W-10/S-02 | Explicit scope gates | Yes |

## 22. Harness Blocker Register
| Blocker | Status | Blocks implementation? | Required next action |
| --- | --- | --- | --- |
| Missing H-01 boundary review | Open | Yes | Create H-01 after instruction. |
| Missing H-02 architecture | Open | Yes | Wait for H-01. |
| Missing H-A audit | Open | Yes | Wait for H-01/H-02. |
| Missing Security/Access enforcement | Open | Yes | Future IR/security work. |
| Missing Validation implementation | Open | Yes | Future validation implementation. |
| Missing governance workflow | Open | Yes | Future governance implementation. |
| Missing provider/MCP policy implementation | Open | Yes | Future architecture/IR work. |
| Missing dependency approval registry | Open | Yes | Future dependency governance. |
| Missing product boundary review | Open | Yes for product use | Product ticket later. |
| Missing external source review | Open | Yes for adoption | H-01/V-05 review. |
| Missing implementation readiness assessment | Open | Yes | IR-00 later. |
| Substrate assumption | Blocked if present | Yes | Preserve neutrality. |
| Local-only/secret risk | Stop condition | Yes | Safe metadata/security handling. |

## 23. Harness Readiness Model
| State | Meaning | Allowed use | Blocked use | Next action |
| --- | --- | --- | --- | --- |
| unreviewed_harness_material | Mentioned but not classified. | Gap only. | Use/adoption. | H-01 classify. |
| bounded_evidence | Source/status known. | Cite as evidence. | Authority. | H-01 review. |
| pattern_candidate | Abstracted idea. | Compare/validate. | Code reuse. | H-01/H-02. |
| strategy_accepted | H-00 decision. | Guide next tickets. | Implementation. | H-01. |
| boundary_review_ready | H-01 can start. | Review approved docs. | Execution/adoption. | Explicit instruction. |
| architecture_ready | H-02 completed later. | Audit input. | Runtime start. | H-A. |
| audit_ready | H-01/H-02 done. | Audit coherence. | Implementation alone. | H-A. |
| implementation_blocked | Default now. | Blocker record. | Runtime build. | Resolve blockers. |
| implementation_candidate_later | Possible after audits/IR. | Plan only. | Code now. | IR-00 later. |
| rejected_for_current_use | Unsafe/currently invalid. | Historical trace. | Current strategy. | Reconsider only by governance. |

## 24. H-01 Readiness
H-01 - Existing Harness Boundary Review is ready after explicit instruction. H-01 should inventory existing harness-related architecture references from approved docs, classify prior/internal/external/product/generated harness evidence, define current boundary status, identify retainable pattern evidence, identify rejected/deferred material, preserve local-only and external-source boundaries, and avoid execution/adoption. Do not create H-01.

## 25. H-02 Readiness
H-02 - Semantic Meta-Harness Architecture is not ready until H-01 completes. H-02 should later define target harness architecture; interactions among agents, context, validation, governance, tools, providers, MCP, shell, Git, products, and external evidence; substrate neutrality; and implementation-free architecture unless later governed. Do not create H-02.

## 26. H-A Readiness
H-A - Harness Strategy Audit is not ready until H-01 and H-02 complete. H-A should later audit strategy consistency, boundary review findings, architecture coherence, security/access alignment, validation alignment, governance alignment, and implementation readiness implications. Do not create H-A.

## 27. H-00 Decision Record
| Decision item | Final H-00 decision |
| --- | --- |
| Harness material | Retained as bounded evidence only. |
| Existing harness authority | No existing harness becomes AGENT PLATFORM runtime authority. |
| External harness adoption | No external harness is adopted. |
| Harness execution | No harness is executed. |
| Provider/MCP/network/package surfaces | Not activated. |
| Product harness material | Not promoted to root. |
| Future path | H-01, then H-02, then H-A. |
| Implementation | Blocked. |
| Recommended next ticket | H-01 after explicit instruction. |

## 28. H-00 Invariants
| ID | Invariant |
| --- | --- |
| H00-001 | Harness strategy is not harness implementation. |
| H00-002 | Harness does not govern. |
| H00-003 | Harness does not validate by itself. |
| H00-004 | Harness outputs are evidence, not approval. |
| H00-005 | Tool availability is not permission. |
| H00-006 | External harnesses remain external evidence. |
| H00-007 | Existing harness material is bounded evidence only. |
| H00-008 | Product harness material remains product-scoped. |
| H00-009 | Provider credentials are not provider permission. |
| H00-010 | MCP availability is not MCP activation. |
| H00-011 | Package manager availability is not dependency approval. |
| H00-012 | Cognitive Semantic System substrate remains undecided. |
| H00-013 | Graph remains a candidate only. |
| H00-014 | Governance decides. |
| H00-015 | Implementation remains blocked. |

## 29. Anti-patterns
Anti-patterns: harness by external clone; harness by README; harness by setup script; harness by OpenCode behavior; harness by MCP config; harness by provider credential; harness by package install; harness by graph substrate assumption; harness by product code; harness by generated output; harness by migration side effect; harness as governance; harness as validation authority; harness as security bypass; harness implementation by strategy document; `git add .`.

## 30. Remaining Gaps
No H-01 boundary review, H-02 meta-harness architecture, H-A audit, harness implementation, runtime model, provider adapter strategy, MCP activation strategy, tool execution implementation, validation registry implementation, security enforcement implementation, dependency approval registry, product activation, external adoption, implementation readiness, or final Cognitive Semantic System substrate decision exists.

## 31. Final Verdict
| Question | Answer |
| --- | --- |
| What does H-00 decide? | Retain harness material as bounded evidence, reject current adoption/execution, and follow H-01 -> H-02 -> H-A. |
| Does H-00 implement a harness? | No. |
| Are existing harnesses adopted? | No. |
| Are external harnesses adopted? | No. |
| Is OpenCode platform authority? | No; operator usage is evidence/tool usage only. |
| Are providers/MCP/package managers activated? | No. |
| Does H-00 select Cognitive Semantic System substrate? | No; substrate remains undecided and Graph remains a candidate only. |
| What remains blocked? | H-01/H-02/H-A until instructed, implementation, execution, provider/MCP/network/package activation, migration, product activation, external adoption, Git actions, and IR-00. |
| Is H-01 ready after explicit instruction? | Yes. |

Stop rule: after H-00 validation and report, stop. Do not start H-01, H-02, H-A, M-02, P-00, IR-00, implementation, migration, product activation, external adoption, dependency installation, authentication, provider/API/network/MCP activity, Git staging, commit, push, local-only deep inspection, or any next ticket.
