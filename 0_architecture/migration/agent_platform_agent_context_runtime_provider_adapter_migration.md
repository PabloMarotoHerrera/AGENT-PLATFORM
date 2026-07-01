# M-04 - Agent / Context / Runtime / Provider / Adapter Migration
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Agent / Context / Runtime / Provider / Adapter Migration |
| Ticket | M-04 |
| Status | Accepted migration-planning record |
| Date | 2026-07-01 |
| Scope | Safe-metadata planning for agent, context, runtime, workflow, provider, adapter, tool, MCP, and representation migration candidates |
| Authority | Planning only; not migration execution, implementation, provider/API/MCP activation, dependency adoption, product activation, external adoption, lifecycle execution, staging, commit, push, publication, or M-05 start |
| Related documents | M-02, M-03, W-02, W-08, A-00, A-01, V-03, CSS-02, H-series, S-series |
## 2. Purpose
M-04 follows M-02 carry-forward extraction and M-03 conflicted semantic normalization.
It creates a compact migration-planning map for high-value agent, context, runtime, provider, adapter, workflow, tool, MCP, and representation material.
M-04 does not migrate prior files, copy raw previous knowledge, normalize actual files, execute lifecycle states, or create implementation artifacts.
## 3. Source Authority
W-02 is the primary source metadata for previous-knowledge classification.
M-02 and M-03 are grouped safe-metadata inputs that preserve W-02 classifications without copying raw `previusknowledge/` content.
W-08 controls migration principles, target posture, and stop rules.
CSS-02 controls prior Graphify-related naming, authority, and substrate boundaries.
V-03 controls migration validation posture.
A-00 and A-01 control lifecycle language without lifecycle execution.
H-series controls harness, tool, provider, MCP, and runtime-boundary posture.
S-series controls local-only, secret, credential, execution, provider, network, MCP, and Git constraints.
## 4. Source Boundary
M-04 retains safe metadata only: source references, W-02 classification, grouped candidate IDs, target areas, limits, blockers, validation posture, lifecycle posture, and routing.
Raw `previusknowledge/` files remain local-only and were not deeply inspected.
Raw product folders, raw external source trees, generated outputs, datasets, models, artifacts, secrets, credentials, provider state, dependency manifests, and tool configs are not used as source authority.
## 5. Non-Action Statement
M-04 does not create agents, context packs, runtimes, providers, adapters, APIs, schemas, registries, MCP servers, tools, hooks, commands, SDKs, packages, tests, CI, scanners, enforcement, storage, or runtime components.
M-04 does not install dependencies, authenticate, call providers/APIs/networks/MCP, run external/product code, move/copy/delete/rename/archive files, stage, commit, push, publish, or start M-05.
## 6. Migration Definition
Migration in M-04 means planning the future restatement route from classified previous-knowledge metadata into possible current AGENT PLATFORM architecture.
It is not file movement, direct promotion, source copying, implementation, execution, provider adoption, or final authority.
M-04 candidates remain evidence until validation and governance decide future use.
## 7. Classification Coverage
| W-02 class | M-04 handling |
| --- | --- |
| `carry_forward` | May become restatement candidate after citation, current vocabulary, validation, security review, and governance. |
| `conflicted` | May become normalized candidate only after naming, authority, scope, and substrate leakage are neutralized. |
| `external_reference` | External evidence only; provider/harness/tool facts require revalidation and cannot be adopted. |
| `migration_evidence` | Historical trace only; cannot govern current architecture by itself. |
| `scope_limit` | Product/domain-scoped only; cannot define root platform behavior. |
| `superseded` or unknown | Historical/gap handling only until classified and governed. |
## 8. M-02 Input Summary
M-02 extracted 91 W-02 `carry_forward` file-level records as seven grouped candidate records.
M-04 uses only grouped safe metadata and source line references from M-02.
Relevant groups are M02-CF-001 adapter, M02-CF-002 agent, M02-CF-003 context, M02-CF-004 external/provider, and M02-CF-005 runtime/workflow.
## 9. M-03 Input Summary
M-03 normalized 44 W-02 `conflicted` file-level records as six grouped candidate records.
M-04 uses M03-CS-005 API/projection/repository/runtime and M03-CS-006 agent/command/dependency/adapter/hook/MCP/memory/repository/skill/ticket/tool/workflow representation clusters.
These are planning inputs only and do not authorize APIs, runtime engines, repository sync, tools, MCP, hooks, or adapters.
## 10. W-02 Domain Inputs
W-02 classifies Agent, Context, Runtime, Provider, Adapter, and Workflow as mature prior conceptual domains requiring current restatement before authority.
W-02 principles preserve: agents are roles, context is bounded exposure, runtime does not own truth, providers remain external, adapters mediate providers, governance decides, validation evaluates, security constrains, and cognitive substrate remains undecided.
## 11. CSS Boundary
The accepted current name is `Cognitive Semantic System`.
Historical Graphify material is candidate evidence only, external label only, or rejected/prohibited naming context only.
`Platform Graphify`, `Graphify Authority`, and `Graphify owns truth` are prohibited historical examples and not current authority.
Graph remains a candidate substrate only; M-04 does not select graph, graph database, files, vectors, relational storage, hybrid storage, or any other final substrate.
## 12. Harness Boundary
H-series keeps existing harness material as bounded evidence only.
OpenCode/operator-tool behavior is not AGENT PLATFORM authority.
Harness output is evidence, not approval.
Tool availability is not permission; provider credentials are not provider permission; MCP availability is not MCP activation; package-manager availability is not dependency approval.
M-04 may preserve these boundaries as migration constraints, but it creates no harness runtime.
## 13. Security / Local-only Boundary
`previusknowledge/`, `2_products/`, `4_external/sources/`, datasets, models, artifacts, generated outputs, dependency folders, secrets, and credentials remain local-only or restricted by default.
Secrets and credentials are never copied, summarized, transformed, tested, retained, staged, committed, or published as migration evidence.
Unknown sensitivity blocks use beyond safe metadata.
## 14. Validation Boundary
V-03 validates migration readiness and evidence only.
Default M-04 proof posture is PL-1 for path/status metadata, PL-2 for source classification and sensitivity, PL-3 for citation/provenance review, and PL-4 for future restatement coherence.
No proof level approves migration, implementation, provider adoption, MCP activation, product activation, external adoption, Git action, or substrate decision.
## 15. Lifecycle Boundary
A-00 and A-01 allow retention, supersession, deprecation, and archive language only as governed lifecycle posture.
M-04 assigns candidate retention posture but does not apply lifecycle state to files, create archive storage, move material, or mark previous knowledge superseded/deprecated/retained.
## 16. Governance Boundary
Governance decides promotion, rejection, deferral, exceptions, lifecycle changes, provider adoption, MCP activation, product activation, external adoption, implementation readiness, publication, and substrate decisions.
M-04 prepares evidence and blockers only.
## 17. Candidate Record Model
Conceptual fields: candidate ID, source reference, W-02 class, grouped source, current topic, target area, allowed use, blocked use, lifecycle posture, validation posture, security posture, blocker, route, and stop rule.
This is not a schema, registry, database, file format, API, or implementation model.
## 18. Candidate Status Model
| Status | Meaning | Blocked inference |
| --- | --- | --- |
| `m04_planning_candidate` | Safe metadata is relevant to M-04 scope. | Current authority. |
| `m04_ready_for_validation` | Source/class/status are sufficient for future V-03 review. | Migration execution. |
| `m04_deferred_to_css` | Naming, authority, or substrate risk remains. | Direct restatement. |
| `m04_deferred_to_external_review` | Provider/tool/harness fact needs external review. | Adoption or execution. |
| `m04_deferred_to_security` | Exposure, action, provider, MCP, or credential posture is unclear. | Permission. |
| `m04_deferred_to_governance` | Decision path is missing. | Promotion. |
| `m04_blocked` | Required source, citation, classification, or sensitivity evidence is missing. | Any migration use. |
## 19. Material Catalog
| ID | Source reference | W-02 class | Current topic | M-04 handling |
| --- | --- | --- | --- | --- |
| M04-MAT-001 | M02-CF-001; W-02 lines 351-360 | `carry_forward` | Adapter mediation, capability, taxonomy, governance, security, validation | Restatement candidate; no adapter implementation. |
| M04-MAT-002 | M02-CF-002; W-02 lines 363-392 | `carry_forward` | Agent role, autonomy, execution, memory, handoff, orchestration, permission, security, taxonomy | Restatement candidate; no agent authority or runtime. |
| M04-MAT-003 | M02-CF-003; W-02 lines 412-438 | `carry_forward` | Context assembly, authority, lifecycle, retrieval, selection, sensitivity, validation | Restatement candidate; no context-pack generator. |
| M04-MAT-004 | M02-CF-004; W-02 lines 446 and 559-564 | `carry_forward` | External boundary and provider abstraction | Provider-neutral candidate; no provider adoption. |
| M04-MAT-005 | M02-CF-005; W-02 lines 396, 445, 514, 567, 570-574 | `carry_forward` | Runtime and workflow posture | Coordination/runtime candidate; no engine. |
| M04-MAT-006 | M03-CS-005; W-02 lines 449, 453, 460-461, 469, 472-474, 481, 485 | `conflicted` | API, projection, repository, integration, runtime, engine ideas | Bounded evidence; no API/runtime implementation. |
| M04-MAT-007 | M03-CS-006; W-02 lines 377, 448, 451-452, 457-458, 464-465, 471, 479, 483-484, 488 | `conflicted` | Agent, command, dependency, adapter, hook, MCP, memory, repository, skill, ticket, tool, workflow representations | Neutral migration candidate; no tool/MCP/permission adoption. |
| M04-MAT-008 | W-02 lines 397-411, 440-444, 489-497, 503-508, 580-592 | `external_reference` | Provider, harness, MCP, memory, tool, OpenCode, Codex, Claude, Cursor, Hermes, ECC evidence | External evidence only; revalidate before use. |
## 20. Agent Planning Model
Agent material may inform a future agent architecture restatement about roles, task scope, permission boundaries, memory-as-evidence, handoff, coordination, escalation, and reporting.
Blocked: agent truth ownership, autonomous unscoped execution, governance replacement, context overread, local-only exposure, tool/provider use by availability, and implementation.
## 21. Context Planning Model
Context material may inform a future context architecture restatement about selected exposure, source status, sensitivity, lifecycle, freshness, retrieval, assembly, compression, expansion, validation, governance, and observability.
Blocked: context as permission, context as truth, broad dumps, local-only publication, raw previous-knowledge copying, and context-pack generator implementation.
## 22. Runtime Planning Model
Runtime material may inform future runtime posture: mediation, execution evidence, capability exposure, coordination with workflows, trace, constraints, and stop rules.
Blocked: runtime truth ownership, execution engine design, command runner creation, provider/API/network activation, tests/builds, package actions, and implementation readiness claims.
## 23. Provider Planning Model
Provider material may inform provider-neutral architecture: external status, capability characterization, abstraction, governance posture, validation posture, and revalidation need.
Blocked: provider adoption, credentials use, API/network calls, provider lock-in, current provider facts without revalidation, and dependency adoption.
## 24. Adapter Planning Model
Adapter material may inform adapter-neutral architecture: mediation, translation, projection, capability mapping, security, governance, validation, and provider boundary protection.
Blocked: adapter code, SDK/package selection, provider-specific runtime integration, source-code reuse, and authority transfer from provider to platform.
## 25. Workflow Planning Model
Workflow material may inform coordination posture: sequencing, handoff, execution posture, runtime participation, evidence capture, and governance-visible state.
Blocked: workflow engine implementation, hidden automation, product process activation, command execution, and treating workflow state as approval.
## 26. Tool / Command / Hook / Skill / MCP Planning Model
Representation material may inform future capability-surface architecture for tools, commands, hooks, skills, MCP, memory, tickets, repositories, and dependencies.
Blocked: command approval, hook installation, skill registry creation, MCP server/config/resource activation, dependency registry creation, repository synchronization, memory store creation, and hidden permission grants.
## 27. Target Grouping
| Target area | Candidate inputs | Target posture |
| --- | --- | --- |
| Agent architecture | M04-MAT-002, M04-MAT-007 | Future restatement only. |
| Context architecture | M04-MAT-003, M04-MAT-007 | Future selected-exposure model only. |
| Runtime/workflow posture | M04-MAT-005, M04-MAT-006, M04-MAT-007 | Future posture model only. |
| Provider architecture | M04-MAT-004, M04-MAT-008 | Provider-neutral, external-evidence-aware planning only. |
| Adapter architecture | M04-MAT-001, M04-MAT-007 | Mediation model only. |
| Harness/tool/MCP boundary | M04-MAT-006, M04-MAT-007, M04-MAT-008 | Boundary and blocker model only. |
| Cognitive Semantic System | M04-MAT-006, M04-MAT-007 | Candidate representation evidence only; substrate undecided. |
## 28. Candidate Migration Table
| Candidate | Planning output | Required future validation | Required future governance |
| --- | --- | --- | --- |
| Agent restatement | Current agent roles and boundaries. | PL-3 citations; PL-4 coherence/security. | Agent authority and permission scope. |
| Context restatement | Current context exposure and lifecycle posture. | PL-3 citations; PL-4 context/security review. | Context-pack status and publication rules. |
| Runtime/workflow restatement | Runtime does not own truth; workflow coordinates evidence. | PL-4 policy review. | Execution and implementation readiness decision. |
| Provider restatement | Providers remain external and neutral. | PL-3/PL-4 provider fact revalidation. | Any provider/API/network use. |
| Adapter restatement | Adapters mediate without authority transfer. | PL-3/PL-4 adapter boundary review. | Adapter implementation scope. |
| Tool/MCP representation restatement | Capability surfaces remain gated. | PL-4 S-series/V-series review. | Tool/MCP activation policy. |
## 29. Source Citation Rules
Every future restatement must cite W-02 source reference, W-02 classification, M-02 or M-03 grouped candidate when applicable, W-08 migration boundary, V-03 validation posture, S-series security posture, CSS-02 naming/substrate posture, and H-series harness/tool/provider/MCP boundaries when relevant.
Citation is provenance, not truth.
Missing source reference, stale external fact, missing classification, or missing sensitivity posture blocks promotion-quality use.
## 30. External / Provider Revalidation Rules
External provider, harness, MCP, tool, OpenCode, Codex, Claude, Cursor, Hermes, ECC, gateway, plugin, runtime, or memory claims remain external or historical evidence.
Any future use requires source freshness, provenance, license/notice posture, runtime/dependency/network/auth risk review, security review, validation plan, and governance.
M-04 performs none of those adoption or execution steps.
## 31. Product Boundary
Product-scoped material remains product-scoped and local-only.
Product agent, context, runtime, integration, dependency, or semantic-system material cannot define AGENT PLATFORM root architecture by proximity.
Product activation, product Git posture changes, product execution, product dependency adoption, and product publication remain blocked.
## 32. Git / Publication Boundary
Git state is artifact evidence only.
M-04 does not stage, commit, push, force-add, amend, reset, clean, publish, or treat Git history as semantic truth.
Local-only staged material, secret/credential staged material, or broad staging would be a stop condition.
## 33. Retention Rules
Retain safe metadata: source reference, classification, grouped candidate ID, target area, current topic, lifecycle posture, validation posture, blocker, route, and stop rule.
Do not retain raw local-only content, secrets, credentials, raw product source, raw external source, unsafe generated output, or dependency content.
Default lifecycle posture for M-04 candidates is `retain_migration_context` and `retain_safe_metadata_only` until governance decides otherwise.
## 34. Blocker Register
| Blocker | Stop behavior | Required action |
| --- | --- | --- |
| Missing W-02 classification or source reference | Stop candidate use. | Classify or cite safe metadata. |
| Raw content required | Stop extraction. | Request explicit scope or defer. |
| Secret/credential or unknown sensitivity | Stop exposure. | Secure handling/security review. |
| Local-only publication risk | Stop publication/Git path. | Preserve safe metadata only. |
| Old naming or Graphify authority leakage | Stop wording. | Restate under CSS-02. |
| Substrate assumption | Stop claim. | Restore candidate-only language. |
| Provider/API/network/MCP use implied | Stop action. | Future exact security/governance approval. |
| Tool/command/hook/dependency adoption implied | Stop action. | Future policy and approval. |
| Product-root collapse | Stop root claim. | Product governance. |
| Validation treated as approval | Stop verdict. | Restore governance boundary. |
| Migration execution implied | Stop scope. | Future exact migration ticket. |
## 35. Routing Model
| Route | Meaning |
| --- | --- |
| `ready_for_validation_review` | Safe metadata can support future V-03 review. |
| `deferred_to_agent_context_architecture` | Future domain restatement may use the candidate. |
| `deferred_to_provider_adapter_architecture` | Future provider-neutral boundary work may use the candidate. |
| `deferred_to_runtime_workflow_architecture` | Future runtime/workflow posture work may use the candidate. |
| `deferred_to_security_policy` | Action/exposure/tool/provider/MCP permission remains unresolved. |
| `deferred_to_external_review` | Provider/harness/tool facts need external-source validation. |
| `deferred_to_css_substrate_decision` | Representation/substrate pressure remains open. |
| `deferred_to_governance` | Promotion, exception, implementation, or adoption decision is required. |
| `blocked` | Required evidence or safety condition is absent. |
## 36. M-04 Invariants
| ID | Invariant |
| --- | --- |
| M04-001 | M-04 planning is not migration execution. |
| M04-002 | Candidate material is evidence, not current authority. |
| M04-003 | W-02 classification remains visible. |
| M04-004 | Safe metadata is preferred over raw content. |
| M04-005 | Previous knowledge remains local-only. |
| M04-006 | Providers remain external. |
| M04-007 | Adapters mediate without authority transfer. |
| M04-008 | Runtime does not own truth. |
| M04-009 | Context inclusion is not permission. |
| M04-010 | Agents are scoped roles, not truth owners. |
| M04-011 | MCP availability is not activation. |
| M04-012 | Tool availability is not permission. |
| M04-013 | Cognitive Semantic System is the current accepted name. |
| M04-014 | Graph remains a candidate only. |
| M04-015 | Governance decides; validation evaluates. |
## 37. Remaining Gaps
No agent architecture restatement, context-pack strategy implementation, runtime/workflow engine, provider policy implementation, adapter implementation, tool policy implementation, MCP activation policy, dependency approval registry, validation automation, governance workflow implementation, product activation, external adoption, archive execution, lifecycle state application, final substrate decision, or implementation readiness exists.
No source file migration, previous-knowledge rewrite, raw content extraction, product movement, external metadata migration, staging, commit, push, or publication occurred.
## 38. Readiness For M-05
M-05 - Research Evidence Migration is ready only after explicit user instruction and only as evidence-curation planning.
M-05 must preserve M-04 boundaries: no raw local-only overread, no external adoption, no execution, no provider/API/MCP activation, no dependency adoption, no product activation, no substrate decision, no implementation, no staging, no commit, and no push.
Do not start M-05 from M-04.
## 39. Final Verdict
| Question | Answer |
| --- | --- |
| What does M-04 create? | One safe-metadata migration-planning document for agent/context/runtime/provider/adapter and adjacent representation material. |
| Did M-04 inspect raw previous knowledge deeply? | No. |
| Did M-04 migrate, copy, move, archive, normalize actual files, implement, or activate anything? | No. |
| Are providers, tools, MCP, APIs, networks, packages, products, or external sources adopted? | No. |
| Is the Cognitive Semantic System substrate selected? | No; graph remains a candidate only. |
| What remains blocked? | Migration execution, implementation, lifecycle execution, product activation, external adoption, provider/API/MCP activation, dependency adoption, publication, staging, commit, push, and M-05. |
Final M-04 statement:
```text
M-04 maps W-02/M-02/M-03 safe metadata into agent, context, runtime, provider, adapter, workflow, tool, MCP, and representation migration-planning candidates.
It stops before migration execution, implementation, activation, adoption, lifecycle action, publication, Git actions, and M-05.
```
