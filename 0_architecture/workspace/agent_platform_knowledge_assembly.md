# Agent Platform Knowledge Assembly

Status: W-00 assembly output  
Ticket: W-00 - Agent Platform Knowledge Assembly & Source Audit  
Scope: previous-knowledge audit, external-source review, workspace implications, migration recommendation  
Date: 2026-06-27

## 0. Purpose

This document assembles the prior architecture material in `previusknowledge/` and the external reference repositories in `4_external/sources/` into a single workspace-level starting point for AGENT PLATFORM.

It does not create W0, implement code, move files, delete previous documents, rewrite previous architecture, stage, commit, or push.

Core conclusion:

```text
The previous knowledge base is valuable migration evidence, not direct root authority.

The new root is AGENT PLATFORM: an agent-native workspace, not the old AgentLab
Digital Twin product repository.

A governed cognitive semantic authority remains the strongest canonical
principle: one future Cognitive Semantic System should own accepted semantic
truth; files, harness configs, agent outputs, external repositories, generated
artifacts, and runtime state are evidence or projections until explicitly
promoted.
```

## 1. Inputs Reviewed

### Previous Knowledge

Primary previous-knowledge root:

| Path | Observed role | Assembly classification |
| --- | --- | --- |
| `previusknowledge/docs/architecture/` | Main prior architecture corpus, including repository vision, principles, macrofolder architecture, Graphify, agent, context, adapter, provider, workflow, runtime, and product architecture documents. | Migration corpus with many canonical-in-old-scope documents. |
| `previusknowledge/research/agents/` | Smaller research corpus focused on agent-related inputs. | Supporting research evidence. |

Observed previous-knowledge markdown inventory:

| Group | Count | Meaning |
| --- | ---: | --- |
| Architecture documents | 224 | Prior AgentLab and platform architecture chain. |
| Research documents | 13 | Supporting research notes. |
| Total markdown files | 237 | Evidence base for W-00. |

### External Sources

Primary external source root:

| Path | Observed role | Assembly classification |
| --- | --- | --- |
| `4_external/sources/` | External repositories, tools, engines, harnesses, and reference corpora. | Reference evidence only. |

Observed external source directories:

| Source | Primary review target | Assembly classification |
| --- | --- | --- |
| `acpx` | ACP client CLI for structured agent-to-agent communication. | Platform/protocol reference. |
| `ai-cookbook-main` | AI examples organized by agents, context, knowledge, MCP, models, patterns, roadmaps, tools. | Pattern corpus, non-authoritative. |
| `clawhub` | Public skill registry and OpenClaw package catalog. | Registry/catalog reference. |
| `ECC-main` | Cross-harness agent workflow system with agents, skills, hooks, rules, MCP configs, commands. | Harness-operator reference. |
| `EnergyPlusV24-2-0` | Building-energy simulation engine distribution and documentation. | Product/domain reference, not platform authority. |
| `graphify` | External graphify skill/library producing project knowledge graphs. | Graph tooling reference with naming conflict. |
| `hermes-agent` | Personal AI agent with memory, skills, plugins, gateways, delegation, scheduling. | Agent product and runtime reference. |
| `openclaw` | Personal AI assistant with gateway, plugins, skills, package/catalog relationships. | Agent product/plugin reference. |
| `opencode` | Open-source AI coding agent with agents, session runtime, context model, tools, permissions. | Harness/runtime reference. |
| `openstudio` | SDK/tooling for building energy modeling using EnergyPlus and Radiance. | Product/domain reference. |
| `pi` | Agent harness with agent core, coding agent CLI, TUI, provider package. | Minimal coding-agent harness reference. |
| `tau` | Python teaching implementation of Pi-like coding-agent architecture. | Clean-layer educational reference. |

## 2. Previous Knowledge Grouping

The prior corpus is not one flat documentation set. It contains several architectural generations and scopes that must be separated before migration.

| Group | Representative files | Carry-forward value | Migration caution |
| --- | --- | --- | --- |
| Root vision and principles | `repository_vision.md`, `repository_principles.md`, `source_of_truth_strategy.md`, `cross_layer_rules.md` | Strong source-of-truth, evidence, promotion, approval, layer-boundary principles. | Written as AgentLab repository architecture for a Digital Twin product direction. Must be reframed as workspace authority. |
| Macrofolder and ownership architecture | `macrofolder_architecture.md`, layer and ownership documents | Useful responsibility model: product, platform, knowledge, operations, external, governance, Graphify, Security/Access. | Physical folder names and repository assumptions are stale for the current root. |
| Graphify-labeled architecture | `graphify_canonical_semantic_model.md`, `graphify_semantic_authority_architecture.md` | Strongest durable authority model: identity, relationships, evidence, truth, lifecycle, validation, governance, context eligibility, audit. | Needs neutral naming because external `graphify` is also present and because graph-based representation is a candidate hypothesis, not an implementation decision. |
| Agent architecture | `agent_architecture_final_synthesis.md`, agent taxonomy and related documents | Strong model for agents as bounded participants that consume truth and produce support material. | Conceptual architecture only; do not assume implemented runtime or concrete agents. |
| Context architecture | `context_architecture_final_synthesis.md`, `context_taxonomy_synthesis.md` | Strong model for bounded, selected, traceable, governed, security-constrained context. | Must not be collapsed into prompt files, memory, or provider context mechanics. |
| Adapter/provider/workflow/runtime architecture | `adapter_final_synthesis.md`, `adapter_architecture_final_synthesis.md`, `provider_final_synthesis.md`, `workflow_final_synthesis.md`, `runtime_final_synthesis.md` | Useful provider-neutral, adapter-mediated, posture-first boundary model. | It is deliberately implementation-independent. Do not treat it as a code design or runtime engine. |
| Provider-specific adapter architecture | `opencode_adapter_final_synthesis.md`, Codex/Claude/Cursor adapter syntheses | Useful precedent for external harnesses as providers and delta specializations. | Specific provider conclusions need revalidation against current source versions. |
| Product architecture | `product_architecture_final_synthesis.md` and product component/structure/realization syntheses | Useful for future Digital Twin or product-workspace architecture. | Product-specific scope must not define the AGENT PLATFORM root. |
| Research agent notes | `previusknowledge/research/agents/` | Supporting evidence for agent/harness choices. | Research is not canonical without promotion. |

## 3. Document Classifications

The prior documents should be classified by current AGENT PLATFORM usefulness, not by their original status labels alone.

| Classification | Meaning | Documents or groups |
| --- | --- | --- |
| Preserve as canonical principle | Principle remains valid at workspace level after renaming/reframing. | Governed semantic authority owns truth, `Files are artifacts`, explicit source-of-truth status, evidence promotion, human approval before commits and pushes, external material is not internal truth by proximity. |
| Preserve as canonical conceptual architecture | Concept remains valid but should be restated in new workspace documents before it governs implementation. | Graphify semantic model, Graphify semantic authority, Agent architecture, Context architecture, Adapter/Provider/Workflow/Runtime posture architecture. |
| Preserve as migration evidence | Content explains the previous architecture and should inform migration decisions but not directly govern the new root. | `repository_vision.md`, `macrofolder_architecture.md`, old layer documents, old roadmap-oriented docs. |
| Scope-limit to product workspaces | Valuable for Digital Twin/Product work but not for workspace control-plane authority. | Product architecture syntheses, EnergyPlus/OpenStudio product-domain references, old Digital Twin repository vision. |
| Treat as external evidence | Useful to compare patterns, risks, and vocabulary but not authoritative. | All repositories under `4_external/sources/`. |
| Treat as unresolved/conflicting | Requires a normalization ticket before promotion. | Graphify naming, future cognitive-system naming, repository vs workspace, old macrofolders vs current numeric workspace folders, old roadmap vs current roadmap, external graphify tool vs future Cognitive Semantic System. |

Current rule:

```text
Original `Status: canonical` labels remain evidence of prior intent.
They do not automatically make a document canonical for AGENT PLATFORM root.
```

## 4. Canonical Principles To Carry Forward

The following principles should be promoted into new AGENT PLATFORM workspace architecture.

| Principle | Current AGENT PLATFORM interpretation |
| --- | --- |
| Governed semantic authority owns truth. | Cross-artifact identity, relationships, lifecycle, provenance, validation posture, governance posture, context eligibility, and drift state require one governed semantic authority independent of its final internal representation. |
| Files are artifacts. | Files may be source for narrow content or implementation, but file placement does not define global truth, ownership, lifecycle, or authority. |
| Harness adapters are projections. | OpenCode, Codex, Claude, Cursor, Pi, Tau, Hermes, OpenClaw, ACP, and future harness surfaces adapt to the platform; none define the platform. |
| Skills are reusable capabilities. | Skills package repeatable agent behavior, but skill text is not authority unless promoted and governed. |
| Agents are roles. | Agents consume context, reason, plan, execute permitted work, and produce evidence; they do not own truth or governance decisions. |
| Commands are entrypoints. | Commands trigger workflows or capabilities; they are not architecture by themselves. |
| Hooks observe and guard. | Hooks may enforce or observe within declared boundaries; hooks should not hide policy or become source-of-truth. |
| Memory is governed evidence. | Memory must retain provenance, confidence, sensitivity, lifecycle, and promotion state. Memory is not truth by default. |
| MCP is opt-in. | MCP tools are external capability surfaces requiring explicit approval, scope, risk, and provenance. |
| Plan before build. | Architecture and migration decisions should precede implementation or restructuring. |
| Human approval is required before commits and pushes. | Agents may prepare work, but repository history and publication remain human-governed unless a future policy says otherwise. |
| Evidence is not truth until promoted. | Logs, tests, external docs, generated reports, agent summaries, and provider outputs remain evidence until accepted through authority path. |
| Generated/runtime state is not source unless promoted. | Generated outputs, local caches, session state, run outputs, and tool artifacts are operations evidence by default. |
| External material does not become internal truth by proximity. | Cloned repositories and installed engines under `4_external/sources/` remain references unless promoted through provenance, license, validation, governance, and security review. |
| Security/Access may restrict any interaction. | Context, tools, providers, external sources, generated artifacts, publication, and agent operations must respect sensitivity and permission constraints. |

## 5. Unresolved Conflicts

These conflicts should be preserved explicitly rather than papered over.

| Conflict | Evidence | Risk | Recommended handling |
| --- | --- | --- | --- |
| Graphify naming conflict | Prior docs use Graphify as semantic authority. External `4_external/sources/graphify` is a graph-generation skill/library. | Agents may confuse a tool output with the platform authority. | Use `Cognitive Semantic System` as the neutral future-system name until a naming ADR exists; classify external `graphify` as an external tool until renamed or bounded. |
| External graphify tool vs future Cognitive Semantic System | External graphify produces `graphify-out/graph.json`, `GRAPH_REPORT.md`, and visualization outputs. Prior docs used Graphify as the truth-owner name. | Generated graph files may be mistaken for canonical truth or may prematurely make graph the substrate decision. | Treat external graphify outputs as evidence/projections until promoted into the future Cognitive Semantic System authority. |
| Repository vs workspace | Prior docs repeatedly say repository and AgentLab. Current root is AGENT PLATFORM workspace. | Workspace architecture could inherit product-repository assumptions. | New workspace documents must use `workspace` for root authority and reserve `repository` for concrete Git repositories or product repos. |
| AgentLab/Digital Twin vs AGENT PLATFORM | Earlier vision centers Digital Twin Platform, Omniverse, EnergyPlus, and product repo layers. | Product scope could accidentally define the platform root. | Move Digital Twin material into future product-workspace scope; do not let it own root platform architecture. |
| Docs vs knowledge vs architecture | Prior docs use `knowledge/docs/architecture`, while current root has `0_architecture/`. | Agents may not know which path owns current architecture. | Declare `0_architecture/workspace/` as current workspace architecture authority surface until a broader workspace map exists. |
| Old macrofolders vs current workspace layout | Prior target was `product/`, `platform/`, `knowledge/`, `operations/`, `external/`, `governance/`; current root uses numbered top-level areas such as `0_architecture/` and `4_external/`. | Bulk restructuring could break the intended new workspace organization. | Treat old macrofolders as responsibility domains, not immediate folder names. |
| Old roadmap vs current roadmap | Prior documents cite Proyecto/RS/P-series/G-series tickets from old architecture sequence. | Agents may resume stale roadmap order. | Keep old tickets as provenance only; create new W-series workspace roadmap. |
| Schema/runtime docs before new G-series | Some platform architecture documents predate or sit beside newer Graphify-labeled semantic authority docs. | Later implementation could use older wording that weakens semantic authority or overcommits to graph representation. | Use the semantic-authority principles as precedence for truth/evidence/context/promotion language while keeping naming and substrate open. |
| Human folder hierarchy vs agent-native workspace | Old docs emphasize macrofolders for humans and agents. Agent-native workspace needs context packs, authority metadata, and provider adapters. | Folder-first design could recreate drift. | Define folder areas as projections of workspace responsibility, not authority itself. |

## 6. External Source Review

External sources were reviewed as evidence, references, and pattern libraries. None are authoritative for AGENT PLATFORM root.

| Source | Relevant findings | Useful for | Not authoritative for |
| --- | --- | --- | --- |
| `opencode` | Open-source AI coding agent. Root docs identify built-in `build` and read-only `plan` agents. `CONTEXT.md` defines durable session history, system context, context sources, context epochs, safe provider-turn boundaries, prompt promotion, provider turns, tool output projection, and embedded/network client boundary. | Session runtime vocabulary, agent modes, context-source model, provider-turn boundary, generated-client/API boundary, tool-output projection. | AGENT PLATFORM truth model, workspace governance, folder layout, or provider abstraction. |
| `acpx` | Headless CLI client for Agent Client Protocol. Emphasizes structured ACP messages instead of PTY scraping, persistent/named sessions, prompt queueing, cancel, reconnect, status, history, import/export, sandboxed file/terminal methods, auth handshake, and compare/flow patterns. | Agent-to-agent protocol reference, structured delegation, session queueing, adapter-facing CLI, workflow isolation. | Platform orchestration authority, truth ownership, or registry model. |
| `openclaw` | Personal AI assistant with gateway, channels, skills, plugins, MCP/local surfaces, package/plugin ownership boundaries, and strong config/runtime storage policies. | Plugin boundaries, channel/gateway separation, compatibility/migration caution, skills and package ecosystem, core-vs-plugin ownership. | AGENT PLATFORM product definition or root workspace policy. |
| `clawhub` | Public skill registry for OpenClaw and package catalog for plugins. Supports publish/version/search, moderation hooks, vector search, package metadata, installs, pinning, rename/merge aliases, soft delete/restore, and specs as durable intent. | Future skill/package registry, moderation, install pinning, canonical slug handling, docs-vs-specs split. | Direct registry implementation or authority model. |
| `graphify` | External skill/library maps a project into `graphify-out/graph.html`, `GRAPH_REPORT.md`, and `graph.json`. Architecture pipeline is `detect -> extract -> build_graph -> cluster -> analyze -> report -> export`; extraction schema includes nodes, edges, source files, source locations, relation confidence. | Graph extraction/projection tooling, evidence generation, visualization, confidence labels, project-scoped graph reports. | Cognitive Semantic System authority. Its outputs are evidence/projections only. |
| `hermes-agent` | Personal AI agent with CLI, TUI, desktop, messaging gateway, memory, skills, plugins, delegation, cron, ACP adapter, terminal backends, and learning loop. Strong ideas include narrow core, skills/plugins at edges, prompt caching constraints, profile-isolated state, and memory/skill lifecycle. | Agent lifecycle, memory and skill management, plugin surfaces, gateway/channel design, scheduler/delegation patterns. | AGENT PLATFORM governance, product direction, or default implementation stack. |
| `ECC-main` | Cross-harness operator system with agents, skills, commands, hooks, rules, MCP configs, and multi-harness workflows. Readme frames it as a harness-native operator system for Codex, Claude Code, Cursor, OpenCode, Gemini, Zed, GitHub Copilot, and others. | Cross-harness packaging, skills-first workflow surface, hooks/rules/commands as harness projections, security-first operator posture. | Platform authority model or direct folder template. |
| `pi` | Agent harness with `pi-ai`, `pi-agent-core`, `pi-coding-agent`, and `pi-tui`. Explicitly notes no built-in permission sandbox; recommends containerization/sandboxing for stronger boundaries. | Minimal package split, provider/agent/coding/TUI separation, supply-chain hardening, external sandboxing caution. | Security model, workspace authority, or final agent platform structure. |
| `tau` | Python teaching implementation inspired by Pi. Clear boundary: `AgentHarness = reusable agent brain`, `AgentSession = coding-agent environment`, `TUI = one possible frontend`; packages split into `tau_ai`, `tau_agent`, and `tau_coding`; events are provider-neutral contract. | Clean conceptual layering, event-contract pattern, teaching/reference implementation, durable session clarity. | Production architecture or platform authority. |
| `ai-cookbook-main` | Loose example corpus with folders for agents, context, knowledge, MCP, models, patterns, roadmaps, and tools. | Pattern examples and tutorial references. | Architecture, governance, or implementation decisions. |
| `EnergyPlusV24-2-0` | EnergyPlus 24.2.0 distribution. Readme describes a stand-alone building energy simulation engine, text input/output, C API/Python bindings, library mode, and thread-safe simulation state. Docs include EnergyPlus Essentials, Engineering Reference, Input Output Reference, Interface Developer, Module Developer, External Interfaces, and examples. | Digital Twin product/domain simulation evidence, future product workspaces, EnergyPlus integration strategy. | Agent platform control plane, workspace architecture, or Cognitive Semantic System authority. |
| `openstudio` | SDK/tooling for whole-building energy modeling using EnergyPlus and Radiance; supports C++, Ruby, Python, and C#. | Digital Twin product/domain modeling reference and SDK precedent. | Agent platform root or general workspace governance. |

External-source verdict:

```text
External repositories provide useful patterns, terminology, risks, and domain
evidence. None should be copied as the AGENT PLATFORM architecture. The platform
must represent external systems through provenance, authority boundaries,
adapter posture, validation, governance, and security classification.
```

## 7. Agent-Native Workspace Implications

The new root should be designed as an agent-native workspace rather than a single product repository.

| Implication | Required posture |
| --- | --- |
| Workspace root is broader than any product. | Product-specific material, such as Digital Twin, EnergyPlus, OpenStudio, Omniverse, or simulation work, should live as product/workspace content under a declared boundary. |
| Context must be selected, not dumped. | Agents should receive task-scoped context packs assembled from authority status, freshness, sensitivity, source lineage, and budget. |
| External sources require provenance. | Cloned repositories, docs, engines, and examples must remain references until reviewed and promoted. |
| Harnesses are providers/adapters. | OpenCode, Codex, Claude, Cursor, Pi, Tau, Hermes, OpenClaw, ACP, and similar systems should be represented as external providers or adapter targets, not as root architecture owners. |
| Agent output is evidence. | Agent summaries, plans, reviews, and generated docs require validation and governance before becoming durable truth. |
| Folder layout is a projection. | Current paths like `0_architecture/` and `4_external/` are workspace artifacts. They need authority metadata and migration rules before broad restructuring. |
| Skills are capabilities. | Skills can encode workflows, but the platform needs a governed model for skill identity, ownership, versioning, installation, permissions, and lifecycle. |
| Commands and hooks need boundaries. | Commands are entrypoints and hooks guard/observe. They should not silently own policy. |
| MCP/tool usage must be explicit. | Tool, shell, network, MCP, and provider access need declared scope, risk, approval, validation, and trace. |
| Human approval remains central. | Commits, pushes, authority promotion, risky external integration, and publication require explicit human or governance approval. |

The workspace should optimize for these questions:

| Question | Needed workspace capability |
| --- | --- |
| What is true? | Future Cognitive Semantic System authority and promoted architecture docs. |
| What is evidence? | Evidence registry or conventions for validation output, source reviews, generated reports, and external references. |
| What can this agent see? | Context eligibility, permission, sensitivity, and task-scope model. |
| What can this agent do? | Role, capability, command, hook, MCP, shell, and provider permission model. |
| What changed and why? | Decision, ticket, validation, promotion, and trace linkage. |
| What is product-specific? | Product workspace boundaries and ownership model. |
| What is external? | External source provenance, license, trust, freshness, and promotion model. |

## 8. Proposed Migration Model

The migration should be explicit, incremental, and authority-preserving.

| Step | Action | Output |
| --- | --- | --- |
| 1 | Preserve `previusknowledge/` as migrated evidence. | No deletion or rewriting of old docs. |
| 2 | Declare AGENT PLATFORM workspace authority in `0_architecture/workspace/`. | A new workspace charter and vocabulary document. |
| 3 | Normalize names before moving content. | Clear distinctions for AGENT PLATFORM, AgentLab, Digital Twin product, future Cognitive Semantic System, external graphify tool, workspace, repository, product workspace. |
| 4 | Promote durable principles. | New concise workspace principles document derived from prior canonical principles. |
| 5 | Classify prior docs. | Keep/adapt/scope-limit/supersede/archive map for the 237 markdown files. |
| 6 | Register external sources. | External source inventory with provenance, role, license/risk placeholders, freshness, relevance, promotion status. |
| 7 | Define context-pack strategy. | Agent-readable context model driven by authority status, freshness, sensitivity, and task type. |
| 8 | Define workspace map. | Current numbered workspace areas and future responsibility domains mapped without bulk restructuring. |
| 9 | Only then create implementation tickets. | W-series roadmap with validation and approval gates. |

Suggested migration states for previous documents:

| State | Meaning |
| --- | --- |
| `carry_forward` | Principle or conceptual model remains valid and should be restated in current workspace docs. |
| `scope_limit` | Valid only inside a product/workspace scope, not root platform authority. |
| `migration_evidence` | Useful for understanding history and decisions but not current authority. |
| `conflicted` | Contains naming, scope, or authority conflict requiring normalization. |
| `superseded` | Replaced by newer G-series or workspace-level architecture after explicit decision. |
| `external_reference` | Useful source material with provenance but no internal authority. |

## 9. Roadmap Recommendation

Recommended next ticket:

```text
W-01 - Agent Platform Workspace Charter & Vocabulary Normalization
```

Recommended scope:

| Include | Exclude |
| --- | --- |
| Define AGENT PLATFORM root purpose. | Implement code. |
| Normalize workspace vs repository vocabulary. | Move old docs. |
| Resolve AgentLab/Digital Twin naming scope. | Create product architecture. |
| Resolve future Cognitive Semantic System vs external graphify tool naming. | Build the cognitive semantic system. |
| Declare current authority of `0_architecture/workspace/`. | Change external repositories. |
| Define source classification labels for migrated docs. | Stage, commit, or push. |

Recommended follow-up tickets:

| Ticket | Purpose |
| --- | --- |
| W-02 - Previous Knowledge Classification Index | Map all 237 markdown files to migration states. |
| W-03 - External Source Registry | Create governed inventory for `4_external/sources/`. |
| W-04 - Workspace Responsibility Map | Define current numbered folders and target responsibility domains. |
| W-05 - Agent Context Pack Strategy | Define task-scoped, authority-aware context packs. |
| W-06 - Cognitive Semantic System Naming & Authority Boundary | Create naming ADR and resolve semantic authority/substrate boundaries before implementation. |

Do not begin implementation or restructuring before W-01 and W-02 settle naming and authority.

## 10. Final Verdict

The W-00 audit supports this verdict:

```text
Proceed with an agent-native workspace architecture.

Do not revive the old AgentLab repository architecture as-is.
Do not let the Digital Twin product scope define the root.
Do not let external harnesses or source repositories define the platform.
Do not treat external graphify output as Cognitive Semantic System truth.

Carry forward the authority model, evidence model, promotion model,
agent/context/adapter/provider/runtime boundaries, and human-governed approval
principles into new AGENT PLATFORM workspace documents.
```

Current source-of-truth posture after W-00:

| Surface | Current authority posture |
| --- | --- |
| This document | W-00 assembly output and recommendation. |
| `previusknowledge/` | Historical/migration evidence with many prior canonical-in-old-scope docs. |
| `4_external/sources/` | External reference evidence only. |
| `0_architecture/workspace/` | Current workspace architecture staging area. |
| Product/Digital Twin docs | Product-scope input, not root authority. |
| Future Cognitive Semantic System | Conceptual semantic authority to preserve and design, not yet implemented here. |
