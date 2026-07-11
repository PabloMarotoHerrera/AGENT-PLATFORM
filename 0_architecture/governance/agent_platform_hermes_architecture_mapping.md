# Hermes Architecture Mapping

## Document Header

| Field | Value |
| --- | --- |
| Title | Hermes Architecture Mapping |
| Ticket | P11.2 |
| Status | completed_static_source_mapping |
| Date | 2026-07-11 |
| Scope | Static architecture mapping from P11.0-authorized Hermes source only. |
| Authority | Read-only source inspection only. No Hermes installation, import, execution, configuration, provider/API/MCP activation, dashboard/proxy/channel startup, Kanban execution, adapter implementation, adoption approval, source modification, or Git mutation. |
| Source root | `4_external/sources/hermes-agent` |
| Output | `0_architecture/governance/agent_platform_hermes_architecture_mapping.md` |
| Related documents | `0_architecture/governance/agent_platform_hermes_source_review_authorization.md`; optional alignment with `0_architecture/governance/agent_platform_hermes_license_dependency_runtime_audit.md`; P9/P10/P8/P7/P6/P5 governance context. |

Readiness markers:

```text
hermes_architecture_mapping_ready
hermes_component_role_matrix_ready
hermes_kanban_swarm_mapping_ready
hermes_adoption_classification_ready_for_P11.3_P11.4
```

## Summary

P11.2 completed a static source mapping of the P11.0-locked Hermes candidate. The earlier blocked placeholder is superseded because the local source identity now verifies against the P11.0 immutable lock when Git is invoked with a per-command safe-directory override.

Identity consumed:

| Check | Required / accepted | Observed | Result |
| --- | --- | --- | --- |
| Local path | `4_external/sources/hermes-agent` | `4_external/sources/hermes-agent` | Pass |
| Origin | `https://github.com/NousResearch/hermes-agent` or `.git` variant | `https://github.com/nousresearch/hermes-agent.git` | Pass, case-only owner spelling difference |
| HEAD | `9de9c25f620ff7f1ce0fd5457d596052d5159596` | `9de9c25f620ff7f1ce0fd5457d596052d5159596` | Pass |
| Tag at HEAD | `v2026.7.7.2` when locally available | `v2026.7.7.2` | Pass |
| Work tree status | clean | empty `status --short` output | Pass |
| Git safe-directory posture | no persistent Git config mutation | plain Git rejected dubious ownership; per-command `-c safe.directory=...` succeeded | Pass for metadata read only |

Source-level conclusion:

| Area | Finding |
| --- | --- |
| Runtime core | Hermes has a central `AIAgent` facade with initialization and conversation loop factored into `agent/agent_init.py` and `agent/conversation_loop.py`. |
| Tool system | Tools self-register through `tools.registry.ToolRegistry`; `model_tools.py` discovers tools, composes tool schemas, gates availability, and dispatches function calls. |
| Kanban swarm | Hermes has a real SQLite-backed multi-agent work queue with tasks, dependencies, comments, events, attempts/runs, attachments, notifications, dispatcher, heartbeat, reclaim, retries, and worker-scoped tools. |
| Memory | Hermes separates session transcript storage (`hermes_state.SessionDB`) from pluggable memory providers (`agent.memory_provider.MemoryProvider`, `agent.memory_manager.MemoryManager`). |
| Providers | Inference providers are declarative `ProviderProfile` registrations discovered lazily from bundled/user model-provider plugins. |
| Gateway/channels | `GatewayRunner` hosts platform adapters, per-session agent orchestration, authorization/redaction surfaces, notifier loops, and optionally the embedded Kanban dispatcher. |
| Shell/workspaces | Terminal execution is a tool surface with local, Docker, Modal, managed Modal, SSH, Singularity, and Daytona environment backends. |
| Cron/cadence | Cron is a scheduler subsystem with per-job toolset resolution and protected disabled toolsets for non-interactive runs. |
| Dashboard/UI | Hermes includes a FastAPI dashboard backend and React/Vite frontend with chat, sessions, config, channels, files, logs, analytics, plugins, profiles, cron, models, and other operational pages. |

P11.2 does not approve adoption. It prepares source-based classifications for P11.3/P11.4. AGENT PLATFORM remains the authority for ontology, policy, permissions, common contracts, integration state, security posture, and approval. Hermes remains a replaceable candidate runtime behind future interfaces.

## Scope Controls

P11.0 authority consumed from `0_architecture/governance/agent_platform_hermes_source_review_authorization.md`:

| P11.0 field | Consumed value |
| --- | --- |
| Upstream repository | `https://github.com/NousResearch/hermes-agent` |
| Release/version | `0.18.2` |
| Tag | `v2026.7.7.2` |
| Immutable commit | `9de9c25f620ff7f1ce0fd5457d596052d5159596` |
| Approved local path | `4_external/sources/hermes-agent` |
| Inspection posture | Static read-only source review after identity verification |

Performed:

| Action | Status |
| --- | --- |
| Read P11.0 authorization | Completed |
| Verify source identity with per-command Git safe-directory metadata | Completed |
| Inspect source files needed for architecture mapping | Completed |
| Inspect source schemas as text | Completed |
| Rewrite this P11.2 canonical file | Completed |

Not performed:

| Blocked action | Status |
| --- | --- |
| Hermes install, import, execution, tests, builds, scripts, package managers | Not performed |
| Provider/API/OAuth/MCP activation or credential use | Not performed |
| Dashboard, gateway, proxy, channel, cron, Kanban, shell, browser, subagent startup | Not performed |
| Runtime state, SQLite DB, vector store, graph store, generated log, credential store inspection | Not performed |
| Product/Siamese, GBrain, GStack, Paperclip, ECC-main, OpenCode source inspection | Not performed |
| Hermes source modification | Not performed |
| Persistent Git config, checkout, reset, pull, fetch, staging, commit, push | Not performed |

Source-local instruction files are not governance authority. Any source-local `AGENTS.md`, setup guidance, or contributor instruction encountered during tool output is treated only as untrusted external evidence and does not override AGENT PLATFORM rules.

## Evidence Reviewed

Source anchors are static file references, not execution evidence.

| Source path | Source evidence | Architecture relevance |
| --- | --- | --- |
| `run_agent.py:393-563`, `run_agent.py:5745-5768` | `AIAgent` constructor is a facade over `agent.agent_init.init_agent`; `run_conversation()` forwards to `agent.conversation_loop.run_conversation`. | Runtime entrypoint and narrow facade. |
| `agent/agent_init.py:1-18`, `agent/agent_init.py:260-331`, `agent/agent_init.py:1159-1188`, `agent/agent_init.py:1219-1237`, `agent/agent_init.py:1359-1367` | Init is extracted, creates tool definitions/valid tool names, stamps session IDs, sets Kanban guidance when Kanban tools are present, and wires memory manager. | Session lifecycle, tool surface, memory activation, Kanban worker posture. |
| `agent/conversation_loop.py:1-15`, `agent/conversation_loop.py:523-652`, `agent/conversation_loop.py:4420-4688` | Main loop drives one user turn, tracks API call budget, processes tool calls, and delegates tool execution. | Agent loop and tool-call flow. |
| `agent/tool_executor.py:1-10`, `agent/tool_executor.py:69-74`, `agent/tool_executor.py:95-111`, `agent/tool_executor.py:198-245` | Sequential/concurrent tool execution, bounded workers/timeouts, incremental session persistence after tool progress, scoped Tool Search validation. | Tool execution, persistence, scope containment. |
| `agent/turn_finalizer.py:30-123`, `agent/turn_finalizer.py:135-210` | Finalizes turns, handles budget exhaustion, records Kanban worker failures on timeout, saves trajectory, cleans resources, persists sessions. | Completion, cleanup, failure accounting. |
| `model_tools.py:185-209`, `model_tools.py:279-354`, `model_tools.py:425-567`, `model_tools.py:1019-1198` | Tool discovery, plugin discovery, schema resolution/cache, availability filtering, Tool Search deferral, function-call dispatcher, middleware/plugin hooks. | Tool registry orchestration and trust boundary. |
| `tools/registry.py:58-75`, `tools/registry.py:208-230`, `tools/registry.py:356-448` | Built-in tool discovery imports self-registering modules; `ToolRegistry` stores schemas/handlers/checks; plugin override/shadowing is gated. | Tool authority and plugin override controls. |
| `toolsets.py:31-80`, `toolsets.py:95-240`, `toolsets.py:260-277`, `toolsets.py:342-418` | Core tool list, category toolsets, Kanban toolset, coding/API toolsets. | Toolset composition and exposure. |
| `tools/kanban_tools.py:1593-1672` | Registers `kanban_show`, `kanban_list`, `kanban_complete`, `kanban_block`, `kanban_heartbeat`, `kanban_comment`, `kanban_create`, `kanban_unblock`, `kanban_link`. | Worker/orchestrator task lifecycle tools. |
| `hermes_cli/kanban_db.py:1-69`, `hermes_cli/kanban_db.py:1095-1275` | SQLite board, multi-board isolation, WAL/CAS strategy, task/task_links/comment/event/run/attachment/notification schema. | Kanban control plane and state ownership. |
| `gateway/kanban_watchers.py:115-133`, `gateway/kanban_watchers.py:744-875`, `gateway/kanban_watchers.py:1117-1264` | Gateway notifier polls task events; embedded dispatcher is gated by config/env, singleton-locked, interval-based, failure-limited, and auto-decomposes with config caps. | Dispatcher, notifier, heartbeat/reclaim/retry loop. |
| `hermes_state.py:1-15`, `hermes_state.py:123-130` | SQLite `state.db` with WAL and FTS5 session/message search; stores session metadata/history/model config. | Session persistence and recall. |
| `agent/memory_manager.py:1-24`, `agent/memory_manager.py:100-145`, `agent/memory_manager.py:163-168` | Memory manager orchestrates providers, injects provider tool schemas, and scrubs injected memory context from visible output. | Procedural/episodic memory layer boundary. |
| `agent/memory_provider.py:1-32`, `agent/memory_provider.py:53-150` | Memory provider ABC defines availability, initialize, prompt block, prefetch, sync, tool schemas/calls, shutdown, and optional hooks. | Replaceable memory-provider interface. |
| `providers/base.py:1-10`, `providers/base.py:38-90`, `providers/base.py:111-160` | `ProviderProfile` declaratively describes auth, endpoints, quirks, model caps, preprocessing, and extra request fields. | Provider/model routing abstraction. |
| `providers/__init__.py:1-23`, `providers/__init__.py:53-73`, `providers/__init__.py:140-171` | Provider registry lazily discovers bundled/user model-provider plugins; user profiles may override bundled names. | Provider plugin surface and credential boundary. |
| `gateway/run.py:2774-2933`, `gateway/run.py:6590-6769`, `gateway/run.py:7226-7229`, `gateway/run.py:13100`, `gateway/run.py:17958` | `GatewayRunner` controls adapters, sessions, delivery, running agents, startup warnings/redaction/allowlists, and creates `AIAgent` instances. | Channel gateway and session orchestration. |
| `gateway/platform_registry.py:1-29`, `gateway/platform_registry.py:38-160` | Platform adapters self-register through `PlatformEntry`, including config validation, allowlist envs, message limits, cron delivery, and standalone senders. | Channel/plugin architecture. |
| `gateway/platforms/base.py:2253-2347`, `gateway/platforms/base.py:2863-2888`, `gateway/platforms/base.py:3911-5426` | Base platform adapter interface and active/pending session guards. | Messaging concurrency and interrupt/queue boundary. |
| `cron/scheduler.py:1-8`, `cron/scheduler.py:116-136`, `cron/scheduler.py:170-200`, `cron/scheduler.py:202-230` | Scheduler tick loop with lock; cron disables protected toolsets; resolves per-job/platform toolsets; defines delivery platforms. | Cadence and scheduled job boundary. |
| `tools/terminal_tool.py:1-18`, `tools/terminal_tool.py:152-200`, `tools/environments/base.py:1-7`, `tools/environments/base.py:82-94`, `tools/environments/local.py:61-160` | Terminal tool supports multiple backends, approval/sudo callback scoping, sandbox root, spawn-per-call execution, safe CWD fallback, provider-env blocklist. | Shell/workspace execution surface. |
| `tools/environments/*.py` | Environment backends include `local`, `docker`, `modal`, `managed_modal`, `ssh`, `singularity`, `daytona`, and shared file sync/utilities. | Replaceable workspace backend layer. |
| `hermes_cli/web_server.py:4-121`, `hermes_cli/web_server.py:255-276`, `hermes_cli/web_server.py:455-600`, `hermes_cli/web_server.py:1718-2265` | FastAPI dashboard backend, event channels, auth/host/token middleware, file/git/session/status APIs. | Dashboard/API surface and local web risk boundary. |
| `web/src/App.tsx`, `web/src/pages/ChatPage.tsx`, `web/src/pages/*`, `web/src/components/*` | React/Vite dashboard routes for chat, sessions, cron, config, profiles, channels, models, MCP, logs, files, env, analytics, plugins, auth widgets, model pickers. | UI/observability and management surface. |

## Architecture Overview

Hermes is structured as a runtime product with a narrow agent core and many edge capabilities.

Static runtime flow:

```text
CLI / Gateway / TUI / Dashboard / Cron
  -> AIAgent facade in run_agent.py
  -> agent_init initializes provider/session/tools/memory/context
  -> conversation_loop runs provider calls and tool-call iterations
  -> tool_executor executes model-selected tools
  -> model_tools dispatches to ToolRegistry entries or agent-loop-owned tools
  -> tool implementations mutate their own allowed runtime surfaces
  -> turn_finalizer persists session, cleans resources, records failures
```

Static gateway flow:

```text
Platform adapter or plugin adapter
  -> GatewayRunner authorization/session/routing/redaction
  -> per-session AIAgent instance
  -> platform delivery router / adapter send
  -> optional Kanban notifier and dispatcher watcher loops
```

Static Kanban flow:

```text
CLI / dashboard / agent Kanban tool
  -> hermes_cli.kanban_db SQLite board
  -> task dependency promotion and CAS claim state
  -> gateway embedded dispatcher or external daemon
  -> worker AIAgent with HERMES_KANBAN_TASK / board env scope
  -> kanban_* tools update task, run, comment, heartbeat, and event state
  -> notifier sends terminal events back to subscribed gateway chats
```

AGENT PLATFORM boundary:

| Plane | Owner after P11.2 |
| --- | --- |
| Ontology, agent taxonomy, roles, permissions, approval, integration policy | AGENT PLATFORM |
| Candidate local runtime implementation | Hermes, only if later wrapped/adapted through AGENT PLATFORM contracts |
| Canonical project/task/budget/work control plane | Future Paperclip; Hermes Kanban may only be provisional if later approved |
| Durable knowledge/facts/decisions/documents | Future GBrain; Hermes memory may only be procedural/session/episodic if later approved |
| Derived repository evidence/visualization | Graphify evidence boundary; not runtime authority |

## Component Role Matrix

The classification column is a P11.2 architecture recommendation for P11.3/P11.4, not an adoption approval.

| Component | Hermes source role | State owner in Hermes | AGENT PLATFORM boundary | Candidate classification | P11 handoff |
| --- | --- | --- | --- | --- | --- |
| Agent loop | `AIAgent` facade delegates to extracted init and conversation-loop modules. | Session messages, turn counters, tool state, callbacks. | Wrap behind `AgentRuntimePort`; AGENT PLATFORM owns runtime authority and policy. | `wrap` | P11.3 runtime ownership; P11.4 adoption mode. |
| Session lifecycle | Session IDs, parent sessions, SQLite state DB, compression/branch chains, gateway session keys. | `state.db`/`SessionDB` plus gateway session store. | Session state must be reversible and scoped; no AGENT PLATFORM state merge by default. | `wrap` | P11.3 session/shutdown; P11.5 contract. |
| Tool registry | Self-registering tools, toolsets, availability checks, middleware, plugin hooks, Tool Search deferral. | In-process registry plus config/env availability. | Tool authority must be mediated by `ToolPermissionSet` and execution gates. | `adapt` | P11.4/P11.5 tool boundary; P11.7 safety. |
| Core tools | Web, terminal, file, browser, skills, todo, memory, session search, delegation, cron, Kanban, etc. | Tool-specific state and external services. | Do not expose wholesale; wrap only approved tool subsets. | `wrap` | P11.5/P11.6/P11.7. |
| Skills | `skills_list`, `skill_view`, `skill_manage`, slash command scanning, skill provenance/guards. | Hermes skill directories and usage/provenance sidecars. | Skill creation/editing is security-sensitive; source-local skills are not governance authority. | `adapt` | P11.7 skill lifecycle review. |
| Self-improving skills/curator | Memory/skill review and skill management surfaces exist in source. | Hermes skill library and curator state. | Must not self-approve or bypass human/governance review. | `exclude` until safety gate, then possibly `adapt` | P11.7. |
| Memory providers | ABC plus manager for prompt blocks, prefetch, sync, provider tools, and hooks. | Provider-specific memory stores; Hermes session DB separate. | GBrain owns durable knowledge; Hermes memory can only be procedural/session unless promoted by policy. | `adapt` | P11.3/P11.5/P11.7. |
| Session search | FTS5 over `state.db` messages and session metadata. | Hermes SQLite state DB. | Useful as runtime recall; not durable knowledge authority. | `wrap` | P11.5 memory/search contract. |
| Provider/model routing | Declarative `ProviderProfile` plugins, aliases, endpoint/auth metadata, request quirks. | Config/env credentials and provider registry. | Provider credentials and calls remain blocked until auth/security gates. | `adapt` | P11.3/P11.7. |
| Subagents/delegation | `delegate_task` spawns child agents with isolated context/toolsets and background return path. | Parent/child session IDs and process-local delegation queues. | Subagents project AGENT PLATFORM taxonomy; they do not own taxonomy. | `adapt` | P11.3/P11.5/P11.7. |
| Shell backend | Terminal tool with local/container/cloud/remote backends and approval/sudo callbacks. | Backend process/session state, sandboxes, optional persistent filesystem. | High-risk execution surface; must be wrapped by `ExecutionContext` and rollback controls. | `wrap` | P11.6/P11.7/P11.8 only. |
| Workspace environments | `tools/environments` backends and sandbox root. | Hermes home/sandbox dirs and backend-specific state. | Workspace cleanup, isolation, and residual-state rules required. | `wrap` | P11.6/P11.7. |
| Gateway/channels | `GatewayRunner`, platform adapters, authorization mixin, delivery router, active session guards. | Gateway session store, platform adapter state. | Network/channel activation remains blocked; allowlists/auth are not AGENT PLATFORM policy by themselves. | `wrap` | P11.3/P11.7/P11.8. |
| Platform plugin registry | `PlatformEntry` factories, env/config bridges, allowlist metadata, standalone senders. | In-process registry plus plugin packages. | Plugin platform activation needs explicit channel and credential review. | `adapt` | P11.7. |
| Cron/cadence | Scheduler tick loop, job store, per-job toolsets, protected disabled toolsets, delivery targets. | Hermes cron job store/output. | Cadence ownership must be decided by P11.3; no always-on runtime approved here. | `wrap` | P11.3. |
| Dashboard/FastAPI backend | REST/WS API, auth/host/token middleware, file/git/session/status endpoints, PTY/chat surface. | Dashboard process state, session token/auth state, APIs. | Localhost UI cannot become approval/task authority without AGENT PLATFORM/Paperclip design. | `wrap` | P11.4/P11.7. |
| React dashboard | Operational UI for chat, sessions, config, channels, cron, models, files, logs, plugins, analytics. | Browser/local UI state and backend APIs. | Observability/management UI only unless later promoted behind authority contracts. | `adapt` | P11.4. |
| Kanban planner/decomposition | Tasks can carry dependencies, skills, model override, workflow fields, goal mode; dispatcher can auto-decompose. | Hermes Kanban DB. | Must not become permanent Paperclip replacement; provisional only behind adapter. | `replace_later` for canonical task authority; `wrap` for MVP runtime queue | P11.3/P11.4. |
| Kanban dispatcher | Gateway-hosted or external loop reclaims, promotes, claims, spawns, limits failures/concurrency. | Hermes Kanban DB and worker processes. | Runtime dispatch policy belongs to AGENT PLATFORM/Cadence gates. | `wrap` | P11.3/P11.7/P11.8. |
| Kanban heartbeat/reclaim/retry | Claim TTL, heartbeat stale detection, failure limit, attempts/runs, timeout accounting. | Hermes Kanban DB. | Liveness/retry cannot be unbounded; policies must be externalized. | `adapt` | P11.3/P11.5. |
| Task/event storage | `tasks`, `task_links`, `task_comments`, `task_events`, `task_runs`, `task_attachments`, `kanban_notify_subs`. | Hermes Kanban SQLite boards. | Paperclip should own canonical work state; Hermes store can be temporary adapter state only. | `replace_later` | P11.4/Paperclip migration. |
| Human review states | Kanban `blocked`, `review`, comments, notifier subscriptions, approval/sudo prompts elsewhere. | Hermes local runtime state. | Human/governance approval remains AGENT PLATFORM; Hermes cannot self-approve. | `replace_later` for canonical approval | P11.3/P11.7. |
| Security controls | Tool checks, plugin override gating, redaction, allowlist warnings, host/auth middleware, env blocklists. | Distributed across Hermes modules. | Treat as candidate controls; P11.7 must verify statically and with controlled runtime evidence later. | `adapt` | P11.7. |

## Agent Loop Mapping

Hermes presents `run_agent.AIAgent` as the main runtime facade. The constructor forwards to `agent.agent_init.init_agent`, while `run_conversation()` forwards to `agent.conversation_loop.run_conversation`. This makes `run_agent.py` a compatibility boundary over extracted modules rather than the only implementation location.

Observed static loop features:

| Feature | Source evidence | Mapping |
| --- | --- | --- |
| Iteration budget | `conversation_loop.py` tracks `api_call_count`, `agent.max_iterations`, and `agent.iteration_budget`. | Runtime loop is bounded by counters, but policy values must remain AGENT PLATFORM-controlled if adopted. |
| Tool calls | `conversation_loop.py` branches on `assistant_message.tool_calls` and calls `agent._execute_tool_calls(...)`. | Model-selected tool execution is central to the runtime. |
| Interrupt/failure handling | Conversation loop and finalizer handle interrupts, retries, empty responses, and finalization. | Candidate runtime has recovery paths, but P11.2 did not execute them. |
| Cleanup/persistence | `turn_finalizer.finalize_turn()` saves trajectory, cleans task resources, persists session, and records diagnostics. | Wrap with `RuntimeEvent`, `FailureEnvelope`, and rollback policy. |
| Kanban timeout handling | Finalizer records budget exhaustion as Kanban task failure when `HERMES_KANBAN_TASK` is set. | Strong evidence of worker/runtime coupling to Kanban control plane. |

AGENT PLATFORM should not call Hermes runtime directly. If P11.4 selects Hermes as a candidate runtime, route it through `AgentRuntimePort` with explicit lifecycle methods for start, turn, interrupt, checkpoint, shutdown, and cleanup.

## Tool Registry Mapping

Hermes tool exposure is a composition of four layers:

| Layer | Source role | Boundary |
| --- | --- | --- |
| Tool module registration | Tool files call `registry.register(...)` at import time. | Registration is source/runtime metadata, not AGENT PLATFORM permission. |
| `ToolRegistry` | Stores schemas, handlers, `check_fn`, env requirements, async flag, descriptions, result caps, schema overrides. | Useful seam for an adapter, but must be filtered by AGENT PLATFORM policy. |
| `toolsets.py` | Defines core, category, posture, platform, Kanban, and safe toolsets. | Candidate vocabulary for capability profiles. |
| `model_tools.py` | Discovers tools/plugins, resolves schemas, filters availability, handles middleware/hooks, dispatches function calls. | Candidate dispatcher; must be wrapped to prevent scope expansion. |

Security-relevant observations:

| Observation | Source evidence | P11 implication |
| --- | --- | --- |
| Tool availability is dynamic | Registry uses `check_fn`; `model_tools` filters unavailable tools. | Adapter must capture resolved tool surface per turn/session. |
| Plugin override/shadowing is gated | `ToolRegistry.register()` rejects cross-toolset shadowing unless explicit override; plugin override needs operator opt-in. | Good candidate control, still requires P11.7 review. |
| Tool Search can defer non-core tools | `model_tools` assembles deferred tool search/describe/call when configured. | Must not allow restricted sessions to reach out-of-scope tools. Source includes scoped checks. |
| Some tools are agent-loop-owned | `todo`, `memory`, `session_search`, `delegate_task` are intercepted by the agent loop. | Adapter must preserve special handling or replace with AGENT PLATFORM equivalents. |

## Skill Loading Mapping

Hermes includes built-in skill tools (`skills_list`, `skill_view`, `skill_manage`) in core toolsets. Skill commands are also part of agent/gateway/CLI behavior through the broader skill command modules. P11.2 did not execute skill loading or inspect user skill state.

P11 classification:

| Skill concern | Mapping | Classification |
| --- | --- | --- |
| Listing/viewing source skills | Useful as read-only capability if scoped. | `adapt` |
| Skill creation/editing/management | Directly mutates instruction-bearing files and must be safety-reviewed. | `exclude` until P11.7, then possibly `adapt` |
| Source-local instructions | Evidence only, never governance authority. | `exclude` as authority |
| Curator/self-improvement | Potentially useful for personal runtime learning, but high-risk. | `exclude` until explicit self-modification gate |

## Memory Layer Mapping

Hermes has two distinct memory/state layers:

| Layer | Source evidence | Role | Boundary |
| --- | --- | --- | --- |
| Session state | `hermes_state.py` defines SQLite `state.db` with session metadata, messages, model config, WAL, FTS5. | Runtime transcript and local recall. | Wrap; not durable knowledge authority. |
| Memory providers | `MemoryProvider` ABC plus `MemoryManager` for prompt blocks, prefetch, sync, provider tools, optional hooks. | Procedural/episodic/personal recall plugin seam. | Adapt only behind `KnowledgeMemoryPort`; no GBrain merge. |

GBrain invariant: GBrain owns durable knowledge, facts, decisions, documents, hybrid retrieval, provenance, and promotion policy. Hermes memory may remain a runtime memory layer only if future gates define retention, provenance, opt-in writes, rollback, and conflict resolution.

## Subagent Mechanism Mapping

Hermes exposes delegation through `delegate_task` and related agent-loop handling. Static source indicates child agents can run with isolated context/toolsets and background result re-entry. This is a useful candidate for AGENT PLATFORM taxonomy projection, not taxonomy ownership.

Required future contract:

| Contract item | Reason |
| --- | --- |
| `AgentCapabilityProfile` | Bind child role/profile to AGENT PLATFORM taxonomy. |
| `ExecutionContext` | Scope tools, workspace, model, credentials, timeouts. |
| `FailureEnvelope` | Normalize child failures/timeouts/partial results. |
| `RuntimeEvent` | Audit delegation start/progress/end. |
| `CheckpointReference` | Support rollback/resume where applicable. |

Classification: `adapt`.

## Shell And Workspace Mapping

Hermes terminal execution is a broad tool surface, not a simple subprocess helper. The source maps local execution plus Docker, Modal, managed Modal, SSH, Singularity, Daytona, and shared file-sync/environment abstractions.

Security-relevant static findings:

| Concern | Source evidence | Mapping |
| --- | --- | --- |
| Backend breadth | `terminal_tool.py` docstring and `tools/environments/*.py`. | Multiple runtime backends require backend-specific approval. |
| Process model | `tools/environments/base.py` describes spawn-per-call with session snapshot and CWD persistence. | Good wrapper seam, but runtime behavior not validated. |
| Sandbox root | `get_sandbox_dir()` defaults to `{HERMES_HOME}/sandboxes`. | State location must be inventoried before runtime. |
| Sudo/approval callbacks | Terminal tool keeps per-session/thread callback scope. | Candidate control, requires P11.7 controlled validation. |
| Provider env blocklist | `local.py` derives provider/tool/gateway credential blocklist. | Candidate credential containment, not sufficient as adoption approval. |
| Safe CWD fallback | `local.py` falls back to nearest existing ancestor/temp dir if CWD is missing. | Useful resilience; can surprise workspace isolation if not wrapped. |

Classification: `wrap`. No shell execution is approved by P11.2.

## Provider And Model Routing Mapping

Provider profiles are declarative metadata (`ProviderProfile`) and are discovered lazily from bundled/user `plugins/model-providers` directories plus legacy modules. Profiles describe provider identity, auth type, env vars, endpoints, model catalog, request quirks, and message preprocessing.

P11 boundary:

| Surface | Mapping |
| --- | --- |
| Provider metadata | `adapt`; useful declarative schema. |
| Credentials/env vars/OAuth/token stores | Not inspected; not activated; future P11.7 gate. |
| Live model fetch/calls | Not executed; not authorized. |
| User provider plugins overriding bundled profiles | Security-sensitive; requires explicit governance if used. |

## Gateway, Channels, Proxy, And Dashboard Mapping

Hermes gateway architecture centers on `GatewayRunner`, which owns platform adapters, session store, delivery router, running agents, pending/queued messages, startup warnings, redaction posture, allowlist checks, and background watcher loops.

Channel/plugin model:

| Component | Source role | Boundary |
| --- | --- | --- |
| `GatewayRunner` | Main controller for adapters and message-to-agent routing. | Wrap only behind explicit service lifecycle controls. |
| `BasePlatformAdapter` | Abstract platform interface with active-session and pending-message guards. | Good adapter seam; no channel activation approved. |
| `PlatformRegistry` | Plugin adapters self-register factories, config checks, allowlist env names, message limits, standalone senders. | Plugin platform activation needs security review. |
| Gateway redaction/allowlists | Startup logs warn about redaction and missing allowlists. | Candidate controls; AGENT PLATFORM owns final policy. |
| Dashboard backend | FastAPI REST/WS, auth/host/token middleware, file/git/session/status APIs. | High-risk local service surface; no startup approved. |
| Dashboard frontend | React/Vite management UI and embedded chat/PTY surfaces. | UI/observability only unless later authority contracts exist. |

Classification: gateway/channel service `wrap`; dashboard UI `adapt` for observability/management patterns; network activation deferred to P11.7/P11.8.

## Cron And Cadence Mapping

Hermes cron provides due-job ticking, a lock file, job execution, per-job/platform toolset resolution, delivery targets, and protected disabled toolsets. Static source disables `cronjob`, `messaging`, and `clarify` for cron-spawned agents, then layers user disabled toolsets.

P11 boundary:

| Concern | Mapping |
| --- | --- |
| Scheduled runtime | Candidate cadence implementation only; no always-on approval. |
| Non-interactive tools | Useful denylist pattern; must be enforced externally if adapted. |
| Delivery platforms | Channel delivery crosses credential/network boundaries; future gate required. |
| Job store/output | Hermes runtime state only; must be inventoried before activation. |

Classification: `wrap` pending P11.3 cadence decision.

## Kanban Swarm Mapping

Hermes Kanban is a substantial work-control subsystem, not just a UI board. It overlaps with future Paperclip authority and therefore must not become permanent canonical task state.

Kanban architecture:

| Concern | Source evidence | Observed mechanism | AGENT PLATFORM/Paperclip boundary | Classification |
| --- | --- | --- | --- | --- |
| Board identity | `kanban_db.py` docstring | Default board plus per-board directories, env/path overrides, board-specific DB/workspaces/logs. | Board state is Hermes-local/provisional only. | `wrap` |
| Task schema | `tasks` table | Title/body/assignee/status/priority/workspace/project/claim/tenant/result/failure/heartbeat/workflow/skills/model/session/block fields. | Canonical work packet belongs to Paperclip later. | `replace_later` |
| Dependencies | `task_links` | Parent-child dependency edges; child promotion waits for parents. | Map to future Paperclip dependencies. | `replace_later` |
| Comments | `task_comments` | Human/agent comment thread. | Future Paperclip audit/comment plane. | `replace_later` |
| Events | `task_events` | Event log with kind/payload/run_id/created_at. | Can be adapted into `RuntimeEvent`; not approval authority. | `adapt` |
| Attempts/runs | `task_runs` | Run status/outcome/PID/heartbeat/runtime/error/summary. | Useful for `FailureEnvelope`; Paperclip may own canonical attempts. | `adapt` |
| Attachments | `task_attachments` | Metadata rows with on-disk stored paths. | Artifact policy and cleanup required. | `wrap` |
| Notifications | `kanban_notify_subs` | Gateway source subscription to task terminal/status events. | UI/channel notification only, not task authority. | `wrap` |
| Worker tools | `kanban_*` tool registrations | show/list/complete/block/heartbeat/comment/create/unblock/link. | Tool exposure must be worker-scoped. | `wrap` |
| Dispatcher | `gateway/kanban_watchers.py` | Embedded gateway dispatcher with config/env gate, singleton lock, interval, failure limits, concurrency caps. | Runtime dispatch belongs to AGENT PLATFORM/Cadence decision. | `wrap` |
| Heartbeat/reclaim | Claim TTL, stale heartbeat, PID/run tracking. | Reclaims stale/wedged/crashed workers. | Policy must be externalized and bounded. | `adapt` |
| Retry/circuit breaker | Consecutive failure counters and `failure_limit`. | Blocks after repeated non-success. | Useful pattern; approval/rollback separate. | `adapt` |
| Human review/blocking | `blocked`, `review`, `block_kind`, comments, notifier. | Human-facing states exist. | Hermes review cannot self-approve; Paperclip/AGENT PLATFORM owns approval. | `replace_later` |
| Auto-decompose | Dispatcher reads `kanban.auto_decompose` and per-tick caps. | Can fan out tasks. | High authority risk; disabled or strictly wrapped unless P11.3/P11.4 approve. | `exclude` until gate |

Kanban MVP posture:

| Use mode | P11.2 posture |
| --- | --- |
| Permanent canonical task/project/budget authority | Not acceptable; classify as `replace_later` by Paperclip. |
| Provisional MVP work queue behind adapter | Possible later if P11.3/P11.4 approve and migration plan exists. |
| Worker liveness/attempt telemetry | Useful to adapt into AGENT PLATFORM runtime events. |
| Dispatcher activation | Not approved by P11.2; needs runtime/cadence and safety gates. |
| Dashboard Kanban authority | Not approved; UI cannot be authority by default. |

Required Paperclip migration invariant: no permanent dual authority for task state. If Hermes Kanban is used provisionally, all canonical fields must be mapped to `WorkPacket`/`WorkControlPlanePort`, and migration/rollback must be designed before runtime activation.

## Task And Event Storage Mapping

Hermes state stores observed statically:

| Store | Source | Purpose | P11 posture |
| --- | --- | --- | --- |
| `state.db` | `hermes_state.SessionDB` | Sessions, messages, model config, FTS5 search. | Runtime session store only; wrap. |
| `kanban.db` / board DBs | `hermes_cli.kanban_db` | Tasks, dependencies, comments, events, runs, attachments, notifications. | Provisional only; Paperclip replaces canonical task authority. |
| Cron store/output | `cron/jobs.py`/`cron/scheduler.py` by reference | Scheduled jobs and outputs. | Cadence state; wrap only after P11.3. |
| Skill/memory sidecars | Skill/memory modules by source references | Skill usage, provider memory, lifecycle state. | Security-sensitive; no merge with AGENT PLATFORM/GBrain by default. |

No SQLite database files were opened. P11.2 only read schema/source definitions as static text.

## Human Review And Security Controls Mapping

Source-observed candidate controls:

| Control area | Evidence | Limit |
| --- | --- | --- |
| Gateway allowlists | Startup checks for platform allowlist/allow-all envs and policies. | Env/config values not inspected; runtime not validated. |
| Secret redaction | Gateway logs redaction enabled/disabled posture. | No runtime proof of complete redaction. |
| Tool plugin override gate | Registry rejects shadowing unless operator opt-in. | Static only; plugin runtime not exercised. |
| Tool availability checks | `check_fn` filtering and TTL cache. | Availability can drift; adapter must snapshot. |
| Terminal approval/sudo callbacks | Per-thread/session callback scoping. | High-risk; controlled runtime test required. |
| Dashboard auth/host/token middleware | FastAPI middleware references. | No server started; web auth behavior not validated. |
| Kanban failure circuit breaker | Consecutive failure counters and dispatcher `failure_limit`. | Policy values must be externalized. |
| Cron denylist | Protected disabled toolsets for cron. | Useful pattern; not a full approval model. |

P11.7 must perform a separate security review before any runtime activation. P11.2 does not certify these controls.

## AGENT PLATFORM Responsibility Mapping

| Hermes capability | AGENT PLATFORM contract needed | Authority owner | Runtime owner if later approved | Adapter required | Classification |
| --- | --- | --- | --- | --- | --- |
| Agent loop | `AgentRuntimePort` | AGENT PLATFORM | Hermes candidate | Yes | `wrap` |
| Tool registry/tools | `ToolPermissionSet`, `ExecutionContext` | AGENT PLATFORM | Hermes candidate tools | Yes | `adapt`/`wrap` |
| Skills | `SkillCapabilityProfile`, provenance/review policy | AGENT PLATFORM | Hermes skill mechanisms only if gated | Yes | `adapt`; self-improvement `exclude` pending P11.7 |
| Memory | `KnowledgeMemoryPort`, `MemoryWriteCandidate` | AGENT PLATFORM/GBrain boundary | Hermes procedural layer only | Yes | `adapt` |
| Providers | `ProviderRoute`, credential boundary | AGENT PLATFORM | Hermes provider profiles | Yes | `adapt` |
| Subagents | `AgentCapabilityProfile`, `FailureEnvelope` | AGENT PLATFORM | Hermes delegate runtime | Yes | `adapt` |
| Shell/workspace | `ExecutionContext`, `WorkspaceReference` | AGENT PLATFORM | Hermes backend only if gated | Yes | `wrap` |
| Gateway/channels | `ChannelRuntimePort`, `RuntimeEvent` | AGENT PLATFORM | Hermes gateway only if gated | Yes | `wrap` |
| Cron/cadence | `CadenceRuntimePort` | AGENT PLATFORM | Hermes scheduler only if gated | Yes | `wrap` |
| Kanban/task state | `WorkControlPlanePort`, `WorkPacket` | Paperclip future plane | Hermes provisional queue only | Required | `replace_later` canonical, `wrap` provisional |
| Dashboard/UI | `ObservabilityPort`, management UI contract | AGENT PLATFORM/Paperclip depending surface | Hermes UI only if gated | Yes | `adapt`/`wrap` |

## Paperclip Boundary Mapping

| Hermes Kanban capability | Future Paperclip equivalent | Conflict risk | Provisional use posture | Migration route |
| --- | --- | --- | --- | --- |
| Task records | Work packets/tasks | High | Only behind adapter | Map `tasks` fields to `WorkPacket`. |
| Dependencies | Work graph/dependency model | High | Only behind adapter | Map `task_links`. |
| Comments/events | Audit/comment/event stream | Medium/high | Adapter can mirror events | Convert `task_comments` and `task_events` to canonical audit events. |
| Attempts/runs | Work attempts/executions | Medium/high | Useful runtime telemetry | Map `task_runs` to attempts/failures. |
| Dispatcher | Work assignment/execution queue | High | P11.3/P11.4 decision only | Replace with Paperclip dispatcher or keep Hermes as worker runtime only. |
| Review/block states | Approval/review workflow | High | Hermes cannot self-approve | Paperclip/AGENT PLATFORM owns approval states. |
| Attachments | Artifacts/evidence | Medium | Requires cleanup/provenance | Map file references with provenance and retention policy. |

Invariant: no permanent dual task authority.

## GBrain Boundary Mapping

| Hermes memory/session capability | GBrain boundary | Classification |
| --- | --- | --- |
| Runtime transcript/session recall | May remain Hermes runtime-local; can be queried through adapter. | `wrap` |
| Procedural/user preference memory provider | Candidate runtime layer with opt-in writes and provenance. | `adapt` |
| Durable facts/decisions/documents | GBrain owns this; Hermes must not become durable knowledge authority. | `replace_later` |
| Memory provider tool schemas | Could be exposed only through AGENT PLATFORM memory policy. | `adapt` |
| Dream/maintenance/self-improvement loops | Not approved. | `exclude` pending future gate |

## Graphify Boundary Mapping

Graphify remains evidence and visualization only. At the start of this P11.2 continuation, `graphify-out/graph.json` was absent, so no existing graph query was available before source inspection and direct static source review was used. After this mapping was rewritten, `graphify update .` was run and generated/updated `graphify-out/graph.json`, `graphify-out/graph.html`, and `graphify-out/GRAPH_REPORT.md`. The update reported a code graph refresh only; semantic doc/paper/image updates would require a separate `/graphify --update` run.

## Adoption Classification Matrix

P11.2 classification terms are recommendations for later tickets only: `adopt`, `adapt`, `wrap`, `replace_later`, `exclude`, `unknown_pending_followup`.

| Component | Classification | Rationale | Required future ticket |
| --- | --- | --- | --- |
| Agent loop | `wrap` | Candidate runtime core, but AGENT PLATFORM owns authority. | P11.3/P11.4/P11.5 |
| Session lifecycle | `wrap` | Useful local session implementation; must remain reversible and scoped. | P11.3/P11.5 |
| Tool registry/schema system | `adapt` | Good metadata/dispatch seam; permissions must be external. | P11.4/P11.5/P11.7 |
| Tool implementations | `wrap` | Tool effects are high-risk and must be selectively exposed. | P11.5-P11.8 |
| Skill listing/viewing | `adapt` | Useful instruction-library read surface. | P11.5/P11.7 |
| Skill management/self-improvement | `exclude` | Mutates instruction-bearing files; requires safety gate first. | P11.7 |
| Memory manager/providers | `adapt` | Good pluggable memory abstraction; durable knowledge excluded. | P11.5/P11.7 |
| Durable knowledge ownership | `replace_later` | Reserved for GBrain. | GBrain/P11.5 alignment |
| Provider profiles | `adapt` | Declarative metadata useful; credentials/calls still blocked. | P11.7 |
| Delegation/subagents | `adapt` | Useful worker pattern; taxonomy must be external. | P11.3/P11.5/P11.7 |
| Terminal/workspace backends | `wrap` | High-risk runtime execution; needs strict gates. | P11.6/P11.7/P11.8 |
| Gateway/platform channels | `wrap` | Network/channel runtime needs explicit service activation. | P11.3/P11.7/P11.8 |
| Cron scheduler | `wrap` | Candidate cadence only; ownership undecided. | P11.3 |
| Dashboard backend | `wrap` | Local service and API surface; auth/security review required. | P11.4/P11.7 |
| Dashboard frontend | `adapt` | Useful management/observability design. | P11.4 |
| Kanban worker tools | `wrap` | Useful worker lifecycle hooks if scoped. | P11.3/P11.5/P11.7 |
| Kanban task DB | `replace_later` | Future Paperclip canonical work state should replace permanent Hermes authority. | P11.4/Paperclip |
| Kanban dispatcher | `wrap` | Runtime queue/worker dispatcher may be provisional only. | P11.3/P11.4/P11.7 |
| Kanban auto-decompose | `exclude` pending gate | Planner authority/fan-out risk. | P11.3/P11.4/P11.7 |
| Human review/approval states | `replace_later` | AGENT PLATFORM/Paperclip owns approval. | P11.3/P11.4 |
| Security controls | `adapt` | Candidate controls only; no runtime certification. | P11.7 |

No component is marked `adopt` by P11.2.

## Interfaces Required

Future interfaces, not implemented by P11.2:

```text
AgentRuntimePort
AgentTurnRequest
AgentTurnResult
RuntimeProfile
AgentCapabilityProfile
ExecutionContext
ToolPermissionSet
ToolInvocationRequest
ToolInvocationResult
KnowledgeMemoryPort
MemoryWriteCandidate
WorkControlPlanePort
WorkPacket
TaskEvent
RuntimeEvent
FailureEnvelope
CheckpointReference
WorkspaceReference
ProviderRoute
ChannelRuntimePort
CadenceRuntimePort
ObservabilityPort
ApprovalRequest
ApprovalDecision
```

## Known Limitations

| Limitation | Impact |
| --- | --- |
| Static source review only | Runtime behavior, performance, actual auth behavior, cleanup, and failure recovery are not validated. |
| No dependency/license audit consumed as authority | P11.1 alignment remains separate. |
| No provider config or credentials inspected | Provider routing and auth surfaces are mapped structurally only. |
| No database/user state opened | Schema mapping is from source strings only. |
| No dashboard/gateway/cron/Kanban started | Service, port, scheduler, and dispatcher risks are not runtime-tested. |
| Large upstream codebase | Mapping prioritizes P11.0-authorized architecture surfaces; detailed hardening needs follow-up. |
| Initial Graphify graph absent | No graph query could be used before source inspection; graphify output was generated only after the mapping rewrite. |

## Risk Notes

| Risk | Note | Route |
| --- | --- | --- |
| Hermes Kanban conflicts with Paperclip | Real task control plane exists in source. | P11.3/P11.4 must decide provisional vs disabled; Paperclip migration required. |
| Tool registry could expand authority | Toolsets/plugins/MCP/Tool Search can alter available tool surface. | P11.5/P11.7 tool permission model. |
| Shell/workspace execution is broad | Multiple local/cloud/container/remote backends. | P11.6/P11.7/P11.8 only. |
| Provider/plugin surfaces touch credentials | Profiles and plugins are declarative but link to auth/env concepts. | P11.7 credential boundary review. |
| Dashboard exposes file/git/API surfaces | Local web server has many management endpoints. | P11.7 service/web review. |
| Memory provider writes may conflict with GBrain | Pluggable memory sync/prefetch/tools exist. | P11.5 memory contract and GBrain boundary. |
| Auto-decompose planner fan-out | Dispatcher can create fan-out work under config. | Exclude until explicit planning authority decision. |

## P11.3 Handoff

P11.3 should decide runtime/cadence ownership using this mapping.

Required P11.3 decisions:

| Decision | Input from P11.2 |
| --- | --- |
| Is Hermes runtime a candidate primary local agent runtime? | `AIAgent` loop and gateway/CLI/cron integrations are source-mapped. |
| Who owns cadence/background loops? | Cron scheduler and gateway-hosted Kanban dispatcher exist. |
| Is Kanban dispatcher disabled, provisional, or externally owned? | Dispatcher has config/env gate, singleton lock, failure/concurrency settings. |
| What is the shutdown/checkpoint posture? | Turn finalizer/session DB/resource cleanup exist but are untested. |
| How are subagents and workers scoped? | `delegate_task` and Kanban worker tools require capability profiles. |

## P11.4 Handoff

P11.4 should choose adoption mode after P11.3 boundary decisions.

Recommended P11.4 posture:

| Topic | Recommendation |
| --- | --- |
| Overall Hermes runtime | `wrap`, not direct adopt. |
| Tool registry concepts | `adapt` behind AGENT PLATFORM permissions. |
| Tool implementations | Selective `wrap`; no wholesale toolset exposure. |
| Kanban | Disable as canonical task state; optionally provisional `wrap` only with Paperclip migration. |
| Dashboard | `adapt` UI patterns and maybe `wrap` service after security review. |
| Memory | `adapt` provider seam; reserve durable knowledge for GBrain. |
| Skills/self-improvement | Read/list may adapt; mutation/self-improvement excluded until P11.7. |
| Shell/workspaces | Runtime spike only after P11.6/P11.7/P11.8. |

## Future Hardening Targets

```text
HERMES-MAP-HARD-01 - Kanban Store Schema Deep Map
HERMES-MAP-HARD-02 - Tool Registry Permission And Tool Search Scope Map
HERMES-MAP-HARD-03 - Skill Lifecycle And Self-Improvement Security Map
HERMES-MAP-HARD-04 - Workspace Backend Isolation And Cleanup Map
HERMES-MAP-HARD-05 - Provider Profile And Credential Boundary Map
HERMES-MAP-HARD-06 - Dashboard API/Auth/Host Boundary Map
HERMES-MAP-HARD-07 - Memory Provider Write/Promotion Policy Map
HERMES-MAP-HARD-08 - Delegation/Subagent Isolation Map
HERMES-MAP-HARD-09 - Gateway Channel Authorization And Redaction Map
HERMES-MAP-HARD-10 - Cron/Cadence State And Delivery Map
```

## Created / Not Created Register

Created/updated:

```text
0_architecture/governance/agent_platform_hermes_architecture_mapping.md
graphify-out/graph.json
graphify-out/graph.html
graphify-out/GRAPH_REPORT.md
graphify-out/manifest.json
```

Not created / not approved:

```text
no Hermes installation
no Hermes execution
no Hermes import
no package manager run
no test/build/script run
no provider/API/OAuth/MCP activation
no credential inspection
no .env inspection
no provider config inspection
no runtime state DB inspection
no dashboard/proxy/gateway/channel startup
no cron startup
no Kanban dispatcher or worker startup
no shell/workspace execution
no browser/computer-use execution
no source modification under 4_external/sources/hermes-agent
no adapter implementation
no adoption approval
no Git checkout/reset/fetch/pull/stage/commit/push
```

## Stop Rules Preserved

Stop immediately on future attempts to:

| Stop condition | Rule |
| --- | --- |
| Inspect credentials, `.env`, token stores, OAuth material, provider configs, browser auth, private user state | Stop without reading values. |
| Open runtime SQLite/vector/graph stores or generated credential-bearing logs | Stop unless separately authorized. |
| Execute, import, install, test, build, configure, or activate Hermes | Stop until exact future runtime gate. |
| Start dashboard, gateway, proxy, channels, cron, Kanban, shell, browser, computer-use, MCP | Stop until exact future runtime gate. |
| Modify Hermes source | Stop unless separately authorized. |
| Expand into product/Siamese or other external source | Stop. |
| Mutate Git state | Stop unless explicitly requested and authorized. |

## Final Verdict

| Question | Answer |
| --- | --- |
| Did P11.2 map Hermes architecture from verified source? | Yes, statically and read-only. |
| Was source identity valid? | Yes: `9de9c25f620ff7f1ce0fd5457d596052d5159596`, tag `v2026.7.7.2`, clean status, origin lower-case `.git` variant. |
| Was Hermes installed/executed/imported/configured? | No. |
| Were credentials or provider configs inspected? | No. |
| Was any runtime state DB opened? | No. |
| Was the Hermes source modified? | No. |
| Was Git mutated? | No. |
| What is Hermes architecturally? | A candidate local agent runtime product with core agent loop, tool registry, memory/provider seams, delegation, gateway/channels, cron, dashboard, shell/workspace backends, and a substantial Kanban work-control subsystem. |
| Can AGENT PLATFORM adopt it directly? | Not from P11.2. Recommendation is wrap/adapt selectively behind contracts. |
| What is the biggest boundary issue? | Hermes Kanban overlaps future Paperclip canonical task/work authority. |
| What is the memory boundary issue? | Hermes memory/session recall must not become GBrain durable knowledge authority. |
| What is the next decision route? | P11.3 runtime/cadence boundary, then P11.4 adoption mode, then P11.5 adapter design and P11.7 safety review before any runtime gate. |

Final markers:

```text
hermes_architecture_mapping_ready
hermes_component_role_matrix_ready
hermes_kanban_swarm_mapping_ready
hermes_adoption_classification_ready_for_P11.3_P11.4
```
