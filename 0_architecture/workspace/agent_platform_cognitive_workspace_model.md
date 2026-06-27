# AGENT PLATFORM Cognitive Workspace Model

Status: Canonical W-06 workspace output  
Date: 2026-06-27  
Scope: Cognitive operating model for AGENT PLATFORM as an agent-native workspace  
Authority: Cognitive model, primitives, flow, invariants, anti-patterns, and substrate-evaluation guidance only. This document is not a folder topology, implementation plan, harness decision, or substrate decision.

## 1. Purpose

AGENT PLATFORM needs a cognitive workspace model because agents, humans, and automated processes need a shared way to coordinate around goals, context, evidence, constraints, tools, memory, validation, coordination, and learning without turning files, folders, runtime state, external sources, generated outputs, or model confidence into truth.

The workspace is not a folder tree. Folders are useful projections for navigation and responsibility, but folder location does not create authority.

The workspace is not a product repository. Product workspaces can own product behavior within product scope, but they do not define AGENT PLATFORM root authority.

The workspace is not a single harness. OpenCode, Codex-style agents, Pi-style harnesses, Tau-style harnesses, ACP-style clients, and future agent systems may consume or project context, but no external harness defines the platform cognitive model.

The workspace is not a memory store. Memory may support continuity, but memory is not truth, approval, validation, or governance.

The workspace is not a documentation dump. Documents, research, previous knowledge, external references, generated summaries, and reports are source classes with different authority postures.

AGENT PLATFORM is a cognitive operating environment: a governed workspace where humans and agents coordinate work through selected context, explicit authority, evidence handling, constraints, capabilities, validation, governance, and learning.

This document keeps four boundaries explicit:

- It is not a folder topology document.
- It is not an implementation plan.
- It is not a harness decision.
- It is not a substrate decision.

The neutral working name for future semantic authority remains `Cognitive Semantic System`. The final cognitive substrate is not decided. Graph is one candidate substrate only.

## 2. Cognitive Workspace Definition

The cognitive workspace is the environment where agents and humans coordinate around:

| Coordination object | Workspace meaning |
| --- | --- |
| Goals | Desired outcomes that justify tasks and decisions. |
| Tasks | Scoped units of work with allowed scope, forbidden scope, deliverables, validation, and stop rules. |
| Context | Selected exposure of relevant information for bounded reasoning. |
| Evidence | Source material, outputs, observations, logs, documents, tests, and findings that can support claims. |
| Constraints | Boundaries that limit visibility, action, authority, security, product scope, external-source use, and output. |
| Capabilities | Abilities agents or systems may have, subject to permission and governance. |
| Decisions | Accepted choices made through authority paths. |
| Validation | Evaluation of evidence, checks, and validity posture. |
| Governance | Approval, promotion, exception, policy, lifecycle, and ownership decisions. |
| Outputs | Produced artifacts, summaries, edits, reports, generated files, and recommendations. |
| Learning | Reviewed updates to future behavior, context selection, evidence handling, and authority models. |

Cognitive workspace rule:

```text
The cognitive workspace organizes how work becomes understandable, traceable,
bounded, validated, governed, and reusable. It does not make every artifact true.
```

## 3. Cognitive Primitives

These primitives are the basic cognitive objects agents operate with. They are not implementation classes and not folder names.

| Primitive | Definition | Role | Default authority | What it is not |
| --- | --- | --- | --- | --- |
| Goal | A desired outcome or direction that motivates work. | Sets purpose and prioritization for tasks. | Intent signal until accepted by governance or current task scope. | Not a task, implementation, approval, or proof. |
| Task | A scoped unit of work with objective, allowed scope, forbidden scope, expected output, validation, and stop rule. | Converts goals into bounded action. | Active task instructions govern current execution scope. | Not permanent authority, not permission beyond stated scope, not a next-ticket grant. |
| Question | A request for clarification, investigation, decision support, or uncertainty reduction. | Guides evidence selection and reasoning. | No authority by itself. | Not an answer, decision, or validation. |
| Context | Selected exposure of information for a task. | Enables bounded reasoning. | Non-authoritative by default; authority depends on source class. | Not truth, memory, permission, approval, or full workspace access. |
| Evidence | Material that can support or challenge claims. | Grounds reasoning, validation, and decisions. | Evidence only until promoted. | Not truth, governance, or validation by itself. |
| Claim | A statement that may be supported, disputed, validated, or promoted. | Connects evidence to reasoning and outputs. | Unaccepted until validated and governed where needed. | Not truth because it is plausible or confidently stated. |
| Constraint | A boundary on visibility, action, authority, sensitivity, scope, or tools. | Prevents unsafe or invalid work. | Binding when from user task, canonical workspace architecture, governance, security/access, or validation scope. | Not optional guidance when marked mandatory. |
| Capability | An ability an agent, human, tool, provider, or workspace area may have. | Describes what could be done. | No permission by default. | Not tool access, approval, or authority. |
| Tool | An invocable mechanism that can inspect, transform, execute, retrieve, validate, or produce output. | Enables action under constraints. | No authority; output is evidence. | Not a decision-maker, source of truth, or governance actor. |
| Memory | Retained continuity material from prior interactions, outputs, traces, or learned preferences. | Supports continuity and recall. | Working evidence until reviewed and promoted. | Not knowledge, truth, context, validation, or permission. |
| Decision | An accepted choice within a declared scope. | Stabilizes future work and resolves alternatives. | Authoritative only when made through the proper authority path and scope. | Not a suggestion, model answer, output, or unreviewed summary. |
| Validation | Evaluation of evidence, behavior, checks, tests, or claims. | Establishes validity posture. | Evidence and verdict posture, not approval by itself. | Not governance, truth, permission, or publication approval. |
| Governance | Approval, promotion, exception, lifecycle, ownership, and policy authority. | Decides authority-sensitive outcomes. | Highest when human-approved or otherwise accepted by future governance process. | Not validation execution, tool output, or model confidence. |
| Output | Produced artifact such as a report, edit, summary, generated file, plan, or recommendation. | Captures agent or process work. | Evidence or artifact until validated and promoted. | Not truth, source, approval, or decision by default. |
| Feedback | Response to output, action, process, or result. | Improves future work and resolves misalignment. | Evidence until accepted. | Not automatic policy or permanent memory. |
| Learning | Durable improvement to behavior, context selection, models, rules, or knowledge after review. | Converts feedback and evidence into better future operation. | Accepted only after review/promotion. | Not raw memory, unreviewed adaptation, or autonomous self-authorization. |

Primitive rule:

```text
Every cognitive primitive carries a role and authority posture. No primitive becomes
truth because it is nearby, recent, generated, confident, or frequently repeated.
```

## 4. Cognitive Flow

The standard workspace cognition flow is:

```text
Goal
-> Task
-> Context Pack
-> Evidence
-> Claim
-> Action / Recommendation
-> Output
-> Validation
-> Governance
-> Promotion / Rejection
-> Learning
```

Flow semantics:

| Step | Meaning | Required boundary |
| --- | --- | --- |
| Goal -> Task | A desired outcome becomes scoped work. | Scope, deliverable, validation, and stop rule must be explicit. |
| Task -> Context Pack | Work receives selected information. | Context is selected exposure, not full workspace access. |
| Context Pack -> Evidence | Agent inspects allowed sources. | Source class, authority, freshness, sensitivity, and relevance must be preserved. |
| Evidence -> Claim | Agent forms statements from material. | Claims must keep uncertainty and source lineage. |
| Claim -> Action / Recommendation | Agent proposes or performs allowed work. | Action requires permission; recommendation requires rationale. |
| Action / Recommendation -> Output | Work produces an artifact or result. | Output is evidence/artifact, not truth by default. |
| Output -> Validation | Checks or review evaluate output. | Validation evaluates; it does not approve or promote by itself. |
| Validation -> Governance | Validity posture informs decision. | Governance decides authority-sensitive outcomes. |
| Governance -> Promotion / Rejection | Material becomes accepted, rejected, deferred, scoped, or archived. | Promotion requires explicit authority path. |
| Promotion / Rejection -> Learning | Reviewed outcomes improve future behavior. | Learning must preserve provenance and not rewrite history. |

No transition is automatic. A strong claim does not automatically become a decision. A passing validation does not automatically become governance approval. A generated report does not automatically become knowledge. A repeated memory does not automatically become truth.

## 5. Agent Operating Loop

The abstract operating loop for agents is:

| Loop step | Required behavior |
| --- | --- |
| Receive task | Parse objective, allowed scope, forbidden scope, expected output, validation, and stop rule. |
| Identify authority level | Determine which current canonical workspace docs, user instructions, governance decisions, and source classes apply. |
| Request or consume context pack | Use the smallest sufficient context pack; do not read broadly by default. |
| Inspect allowed sources | Read only sources permitted by the task and context pack. Preserve source status and uncertainty. |
| Reason within constraints | Apply authority, evidence, security/access, product, external-source, and migration boundaries. |
| Use allowed tools | Invoke only tools allowed by task, role, and risk posture. Treat tool output as evidence. |
| Produce evidence/output | Create the requested artifact, recommendation, summary, edit, or validation result. |
| Report uncertainty/conflicts | Explicitly state incomplete evidence, conflicts, blockers, and assumptions. |
| Stop at stop rule | Do not continue to next ticket, adjacent migration, implementation, commit, push, or external action. |
| Await human/governance decision | Authority-sensitive outcomes require human or governance decision. |

Agent loop invariant:

```text
Agents may reason, inspect, edit when allowed, validate, summarize, and recommend.
Agents do not own truth, approval, promotion, governance, or publication by default.
```

## 6. Human Role

Humans remain central actors in the cognitive workspace.

| Human role | Responsibility |
| --- | --- |
| Scope owner | Defines or confirms objectives, allowed scope, forbidden scope, deliverables, and stop rules. |
| Approval gate | Authorizes staging, commits, pushes, publication, risky execution, external integration, and authority-sensitive changes. |
| Conflict resolver | Resolves naming, scope, product, migration, external-source, access, validation, governance, and substrate conflicts. |
| Governance actor | Approves, rejects, defers, promotes, demotes, scopes, supersedes, or archives material. |
| Validation reviewer | Reviews validation evidence, sufficiency, gaps, and residual risks. |
| Migration decision-maker | Decides what previous knowledge is carried forward, scope-limited, rewritten, archived, or left as evidence. |
| Product/domain authority | Owns product-specific or domain-specific decisions where product scope is declared. |

Human role rule:

```text
Human approval is not replaced by agent confidence, generated output, external
source claims, validation commands, or context pack inclusion.
```

## 7. Memory vs Context vs Knowledge

| Concept | Definition | Supports | Default authority | Required boundary |
| --- | --- | --- | --- | --- |
| Memory | Retained continuity material from prior interactions, outputs, traces, preferences, or observations. | Recall, continuity, and reduced repetition. | Working evidence only. | Must preserve provenance, confidence, sensitivity, freshness, and lifecycle. |
| Context | Current selected exposure for bounded reasoning. | Task execution and reasoning. | Depends on source class; context itself is not authority. | Must be task-scoped, bounded, traceable, and permission-aware. |
| Knowledge | Durable reviewed material, decisions, explanations, classifications, models, and evidence summaries. | Reuse, teaching, search, migration, validation, and governance. | Only authoritative when promoted and scoped. | Must distinguish reviewed knowledge from raw evidence and generated summaries. |
| Authority | Accepted truth, policy, decision, or boundary within declared scope. | Stable coordination and constraint. | Requires promotion through authority path. | Must preserve provenance, validation, governance, ownership, lifecycle, and scope. |

Clarifications:

- Memory supports continuity.
- Context supports current bounded reasoning.
- Knowledge is durable reviewed material.
- Authority requires promotion.
- None of memory, context, or knowledge is truth by default.

## 8. Evidence and Claim Model

Agents must distinguish evidence from claims and claims from truth.

| Evidence type | How agents should treat it | Claim boundary |
| --- | --- | --- |
| Previous documents | Use as migration evidence through W-02 classification. | Prior canonical labels do not create current authority. |
| External sources | Use through W-03 registry posture unless explicit source review is requested. | External source claims are not platform truth and do not approve reuse or execution. |
| Generated outputs | Treat as projections or evidence. | Generated material is not source or truth unless promoted. |
| Code | Treat as implemented behavior only within its declared scope after inspection and validation. | Code presence does not define root architecture or governance. |
| Runtime logs | Treat as operational evidence with sensitivity and freshness concerns. | Logs are not decisions and may be partial or misleading. |
| User messages | Treat as active task scope when current; treat older material as conversation evidence. | User instruction grants only the stated scope. |
| Model outputs | Treat as agent evidence, suggestions, or generated analysis. | Model confidence is not authority or validation. |
| Research findings | Treat as evidence, hypothesis, or recommendation. | Research requires promotion before becoming architecture. |

Claim handling rules:

- A claim should cite evidence when it affects decisions or recommendations.
- A claim should state uncertainty when evidence is indirect, incomplete, stale, generated, external, or uninspected.
- A claim should not collapse evidence, validation, and governance into one step.
- A claim becomes truth only through an authority path.

Authority path:

```text
Evidence -> Claim -> Validation posture -> Governance posture -> Accepted truth
```

## 9. Capability and Tool Model

Agents must separate capability from tool permission.

| Concept | Meaning | Boundary |
| --- | --- | --- |
| Capability | Ability to perform a kind of work, such as reading, editing, searching, validating, summarizing, planning, or running a command. | Capability does not grant permission. |
| Tool | Invocable mechanism that performs an action or returns information. | Tool access requires task scope and risk posture. |
| Tool output | Result produced by a tool. | Evidence only until interpreted, validated, and governed. |
| External tool | Tool or source outside AGENT PLATFORM control. | Requires source, license, trust, dependency, security, privacy, and runtime review before adoption or execution. |
| Harness capability | Ability exposed by an agent harness or provider. | Harness behavior does not define platform authority. |

Tool rules:

- Access to context does not imply tool permission.
- Tool permission does not imply edit permission.
- Tool output is evidence.
- External tools require source and risk review.
- Shell, network, MCP, provider, package, native binary, credential, and external-source actions require explicit scope and approval.
- A tool must not silently become policy, governance, validation, or truth.

## 10. Coordination Model

Multiple agents or subagents may cooperate, but authority remains external to the agents unless explicitly delegated by governance.

| Coordination element | Required behavior |
| --- | --- |
| Orchestration | Split work by task, source class, risk, and output expectation. Preserve the parent task authority. |
| Delegation | Give subagents narrow prompts, allowed scope, forbidden scope, evidence expectations, and stop rules. |
| Subtask boundaries | Keep each subtask scoped to a bounded question or source set. Do not let subagents roam. |
| Evidence return | Subagents return findings, paths, uncertainty, conflicts, and validation notes, not authority decisions. |
| Merge step | Parent agent or human reconciles subagent findings, conflicts, and citations before output. |
| Conflict reporting | Conflicts must be preserved and escalated, not smoothed over. |
| Authority boundary | No subagent owns truth, governance, approval, validation authority, or promotion by default. |

OpenCode-style subagents are a useful observed pattern for bounded exploration and parallel source review. That pattern is not platform authority. The cognitive model remains provider-neutral and harness-neutral.

Coordination invariant:

```text
Delegation can distribute investigation. It cannot distribute away authority,
governance, validation responsibility, or human approval boundaries.
```

## 11. Cognitive Substrate Options

The cognitive workspace needs future substrate evaluation, but W-06 does not decide the substrate.

Possible substrates:

| Substrate option | Strengths to evaluate | Risks to evaluate |
| --- | --- | --- |
| Graph | Relationship reasoning, dependency traversal, provenance edges, authority transitions, multi-hop context paths. | Premature graph-first assumptions, schema complexity, synchronization, overfitting to visualization. |
| Relational | Structured records, constraints, transactions, reporting, maturity, query reliability. | Weakness for fluid relationships, graph-like traversal cost, rigid schema pressure. |
| Document | Human readability, flexible authoring, Git compatibility, low implementation cost. | Weak structured querying, drift, duplicated claims, folder/path authority confusion. |
| Vector | Semantic retrieval, fuzzy matching, similarity search, context discovery. | Weak authority semantics, provenance ambiguity, hallucinated relevance, poor deterministic trace. |
| Event-sourced | Historical trace, lifecycle, replay, auditability, state transitions. | Query complexity, storage growth, projection drift, operational burden. |
| Hybrid | Combines documents, structured metadata, relationships, vectors, events, and projections. | Integration complexity, synchronization, governance burden, unclear source of accepted truth. |
| Biological/complex-system-inspired | Adaptive organization, feedback loops, resilience, networked cognition, emergent coordination patterns. | Metaphor drift, hard validation, implementation ambiguity, risk of vague architecture. |

Evaluation criteria:

| Criterion | Evaluation question |
| --- | --- |
| Retrieval quality | Can agents find the right material with minimal irrelevant context? |
| Relationship reasoning | Can the system represent dependencies, conflicts, ownership, authority, and lineage? |
| Provenance | Can every claim and transition trace back to source material? |
| Authority transitions | Can evidence, candidates, validation posture, governance posture, accepted truth, and historical truth be represented distinctly? |
| Context reduction | Can the system generate small, task-scoped context packs? |
| Multi-agent coordination | Can it support delegation, evidence return, merge, conflict reporting, and role boundaries? |
| Validation/governance traceability | Can validation and governance stay separate but linked? |
| Scalability | Can it handle more products, sources, agents, outputs, and decisions? |
| Implementation cost | Can it be built and maintained without overwhelming the workspace? |

Substrate rule:

```text
The cognitive substrate is undecided. Graph is a candidate, not an implementation
decision. The Cognitive Semantic System should be designed around authority needs
before storage or representation is chosen.
```

## 12. Folder Projection Relationship

Folders relate to cognition as projections, not as the cognitive model itself.

| Folder relationship | Meaning |
| --- | --- |
| Folders are projections | They organize artifacts for humans, Git, and simple navigation. |
| Folder location helps retrieval | Path can be a useful hint for source class and responsibility. |
| Folder location does not create authority | Authority depends on status, scope, governance, validation, and promotion. |
| Context packs are cognitive projections | They select information for tasks and preserve source status. |
| Future semantic navigation may be folder-independent | The Cognitive Semantic System may later provide retrieval and relationship navigation independent of file paths. |
| Folder topology should follow cognitive topology | W-07 may define folders after W-06 defines cognitive responsibilities and flows. |

Folder projection rule:

```text
Folders can help agents find artifacts. They cannot decide what is true, current,
valid, approved, promoted, safe, or editable.
```

## 13. Cognitive Invariants

| ID | Invariant |
| --- | --- |
| COG-001 | Agents operate on selected context, not the whole workspace. |
| COG-002 | Evidence is not truth. |
| COG-003 | Context inclusion is not edit permission. |
| COG-004 | External source presence is not promotion. |
| COG-005 | Folder location is not authority. |
| COG-006 | Subagents do not own authority. |
| COG-007 | Output requires validation/governance before promotion. |
| COG-008 | Cognitive substrate is undecided. |
| COG-009 | Memory is not knowledge by default. |
| COG-010 | Validation evaluates but does not approve by itself. |
| COG-011 | Governance decides authority-sensitive outcomes. |
| COG-012 | Product scope does not define platform root. |
| COG-013 | Harness behavior does not define platform cognition. |
| COG-014 | Tool output is evidence. |
| COG-015 | Human approval gates commits, pushes, risky external integration, and publication. |

Invariant rule:

```text
If an action would violate a cognitive invariant, the agent must stop, report the
conflict, and ask for explicit scope or governance direction.
```

## 14. Cognitive Anti-patterns

| Anti-pattern | Failure mode | Required correction |
| --- | --- | --- |
| Folder tree equals cognition | Treats paths as authority and loses semantic relationships. | Use folders as projections only. |
| Read everything | Bloats context and increases risk exposure. | Use the smallest sufficient context pack. |
| Latest output equals truth | Confuses recency with authority. | Require validation and governance. |
| Agent confidence equals authority | Confuses model certainty with decision authority. | Cite evidence and authority path. |
| External harness defines platform | Lets provider behavior decide local architecture. | Keep provider and harness neutrality. |
| Memory equals knowledge | Treats continuity notes as reviewed durable material. | Preserve memory as evidence until promoted. |
| Context equals permission | Lets selected material imply write or tool authority. | Separate read, cite, edit, run, validate, and approve permissions. |
| Generated summary equals decision | Treats synthesis as governance. | Require explicit decision and scope. |
| Subagent result equals validation | Treats delegation output as proof. | Merge, review, and validate subagent findings. |
| Graph equals implementation decision | Treats a candidate substrate as accepted design. | Keep substrate evaluation neutral. |
| External source proximity equals promotion | Treats cloned sources as internal dependencies. | Use W-03 registry and promotion rules. |
| Product material defines root | Lets product scope collapse platform scope. | Keep product workspaces bounded. |
| Tool availability equals tool permission | Runs available tools without task authorization. | Require explicit allowed tool scope. |

Anti-pattern rule:

```text
Cognitive shortcuts are allowed only when they preserve authority, provenance,
validation, governance, security/access, and task scope. Otherwise they are drift.
```

## 15. Readiness For W-07

Expected next ticket: `W-07 - Workspace Topology`.

Readiness assessment:

| Area | Verdict | Reason |
| --- | --- | --- |
| Cognitive topology | Ready enough for W-07. | W-06 defines primitives, flow, operating loop, evidence/claim model, coordination, substrate neutrality, and folder projection rules. |
| Folder topology | Ready for architecture proposal only. | W-04 maps responsibility, but no movement or rename has been approved. |
| Context topology | Ready enough. | W-05 defines context packs and source classes. |
| Authority posture | Ready enough for topology. | W-01 through W-06 establish that files/folders are not truth and that authority is explicit and scoped. |
| Migration posture | Ready for guarded topology. | W-02 and W-04 define previous knowledge and workspace area boundaries. |
| External-source posture | Ready for guarded topology. | W-03 defines external references and local-only boundaries. |
| Implementation readiness | Not ready. | W-07 should define topology, not implement code. |
| Substrate readiness | Not ready for decision. | W-07 should not choose graph, relational, document, vector, event-sourced, hybrid, or any other substrate. |

W-07 guidance:

```text
W-07 may define folder topology only after consuming W-06 cognitive topology.
It should make folders serve cognition, context, authority, evidence, validation,
governance, product boundaries, and external-source boundaries.
```

## 16. Final Verdict

| Question | Answer |
| --- | --- |
| What is the cognitive workspace? | The governed operating environment where humans and agents coordinate goals, tasks, context, evidence, constraints, capabilities, decisions, validation, governance, outputs, and learning. |
| What does it optimize for? | Bounded retrieval, selected context, evidence separation, authority preservation, safe tool use, explicit validation, governance traceability, multi-agent coordination, migration control, and future semantic navigation. |
| What must agents never infer? | Agents must never infer truth, permission, approval, promotion, validation, product authority, platform authority, freshness, safety, license clearance, or substrate decision from file location, context inclusion, memory, recency, generated output, external source presence, tool output, or model confidence. |
| What should W-07 consume? | W-01 workspace authority, W-02 semantic classification, W-03 external source boundary, W-04 responsibility map, W-05 context pack strategy, and this W-06 cognitive workspace model. |

Final W-06 statement:

```text
AGENT PLATFORM is a cognitive operating environment before it is a folder topology,
implementation, harness, or substrate. Its agents operate through selected context,
bounded capabilities, explicit evidence, validation, governance, and human approval
without letting artifacts become truth by default.
```
