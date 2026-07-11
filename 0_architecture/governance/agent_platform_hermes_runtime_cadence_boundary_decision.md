# Hermes Runtime / Cadence Boundary Decision

## Document Header

| Field | Value |
| --- | --- |
| Title | Hermes Runtime / Cadence Boundary Decision |
| Ticket | P11.3 |
| Status | Accepted Hermes runtime / Cadence boundary decision |
| Date | 2026-07-11 |
| Scope | Documentation-only ownership decision for Hermes runtime mechanics, execution lifecycle, Cadence, workspaces, task projections, recovery, shutdown, checkpoints, and provisional Kanban responsibilities within AGENT PLATFORM / Siamese. |
| Authority | Hermes runtime / Cadence boundary decision only, not Hermes execution, Hermes installation, Hermes runtime activation, Kanban Swarm activation, cron activation, dispatcher activation, worker activation, retry/reclaim/heartbeat loop activation, provider/auth/API/MCP activation, credential use, API calls, MCP activation, source loading, source inspection outside approved P11 source-review scope, product source inspection, external source inspection outside approved P11 scope, validation execution, security enforcement activation, persistence/database/event streaming, telemetry, vector DB, embeddings, graph DB, substrate implementation, publication, Git mutation, Paperclip activation, GBrain/GStack activation, Graphify adoption as authority, or Cognitive Semantic System substrate selection. |
| Related documents | P11.0, P11.1, P11.2, P10.R, P10.7, P10.6, P9.R, P9.4, P8.R, P3.BR, P3.3, P3.4, P3.5, P6.7, P6.1, P6.2, P6.3, P6.4, P6.5, P7 manual workflow documents, P2.1, P2.2, P2.3, P1.1, P1.2, P1.3, P1.4, P1.5, P0.1, P0.2, P0.3, S-03, S-04, Cognitive Semantic System ADR/audit, README, `.gitignore`, `.graphifyignore` |
| Output | Hermes runtime / Cadence boundary decision |

Final declaration:

```text
hermes_runtime_cadence_boundary_ready_for_P11_4
```

This declaration means P11.3 is complete as a governance input. It does not authorize P11.4 implementation, Hermes adoption, installation, execution, or runtime activation.

## Purpose

P11 integrates Hermes as a real, local, controlled, replaceable runtime candidate rather than as an independent application with superficial links.

P11.1 audited the locked Hermes source for license, dependencies, installation footprint, runtime footprint, persistent state, providers, channels, plugins, dashboard, computer use, shell backends, and network surfaces. P11.2 mapped the agent loop, sessions, tools, skills, memory, subagents, shell, workspaces, providers, Kanban planner, dispatcher, heartbeat, retry, reclaim, task/event storage, human review, and static security controls.

P11.3 decides:

- which runtime and execution-lifecycle mechanics Hermes may own behind adapters;
- which policy and authority surfaces AGENT PLATFORM retains;
- which work-control surfaces are reserved for the future Paperclip control plane;
- which durable knowledge surfaces are reserved for GBrain;
- the Cadence boundary for schedulers, dispatchers, workers, retries, reclaim, and maintenance cycles;
- the provisional MVP posture for Hermes Kanban;
- the migration boundary from provisional Hermes Kanban state to Paperclip;
- the interface constraints P11.5 must preserve;
- the execution constraints P11.6 must obey.

P11.3 informs P11.4, P11.5, and P11.6. It does not start any of them. P11.3 does not activate, execute, install, configure, or modify Hermes.

## Current Posture

| Area | Current decision posture |
| --- | --- |
| Hermes review | Hermes is under real integration review at the P11.3 boundary-decision stage. |
| P11.0 | Source review was authorized for one exact repository, release, tag, commit, and path. |
| P11.1 | Static audit is complete and ready for downstream governance; license, supply-chain, state, network, and operations blockers remain binding. |
| P11.2 | Static architecture mapping is complete and ready for P11.3/P11.4; runtime behavior remains unvalidated. |
| Adoption | Hermes is not yet adopted. P11.4 owns adoption mode. |
| Runtime | Hermes is not active. Agent runtime activation remains deferred. |
| Tools/shell | Tool and shell execution remain blocked pending future exact gates. |
| Providers | Provider/auth/API/MCP activation remains deferred and blocked. |
| Hermes Kanban | Hermes Kanban is not canonical task authority. |
| Memory | Hermes Memory and GBrain remain separate layers. |
| Work control | Paperclip is the intended future canonical work control plane. |
| Authority | AGENT PLATFORM retains authority, policy, permissions, ontology, taxonomy, contracts, security, memory boundaries, integration state, and unified observability. |
| Graphify | Graphify remains an evidence map only and owns no authority. |
| Siamese | Siamese is product vision, not product activation. |
| Cognitive Semantic System | Cognitive Semantic System is the accepted name; substrate selection remains deferred. |

## Inputs Reviewed

P11.3 consumes governance records, not Hermes source. Missing legacy filenames are recorded as limitations rather than silently treated as present. Only P11.0, P11.1, and P11.2 are serial hard-stop prerequisites for this ticket.

| Input | Expected role | Present / missing | P11.3 use | Blocking consequence if missing |
| --- | --- | --- | --- | --- |
| P11.0 Hermes Source Review Authorization | Exact source and authority boundary | Present | Fixes the P11 scope and preliminary runtime/Kanban/memory/reversibility boundaries. | Stop P11.3. |
| P11.1 Hermes License / Dependency / Runtime Audit | Runtime, state, dependency, network, and license evidence | Present | Supplies high-privilege runtime, state, network, lazy-install, license, and shutdown risks. | Stop P11.3. |
| P11.2 Hermes Architecture Mapping | Component and lifecycle mapping | Present | Supplies agent, tool, shell, workspace, memory, provider, cron, Kanban, and adapter seams. | Stop P11.3. |
| P10.R Graphify Evidence Integration Closure | Graphify evidence posture | Missing at exact listed path | Current Graphify posture is instead carried conservatively by README, `.graphifyignore`, current Graphify remediation records, and P11.2: evidence-only, non-authoritative. | No Graphify authority inference; future promotion remains blocked. |
| P10.7 Graphify Evidence Import Boundary | Import boundary | Missing at exact listed path | No operational Graphify import is assumed. | Graphify import/authority remains blocked. |
| P10.6 Graphify Markdown Evidence Refresh Report | Generated evidence limitations | Missing at exact listed path | P11.3 does not consume raw generated Graphify output. | No Graphify evidence promotion. |
| P9.R External Integration Foundation Closure | External integration closure | Missing at exact listed path | Current P9 charter and P9.1-P9.6 records supply the surviving gate posture. | External runtime remains conservative and gated. |
| P9.4 External Tool Execution Gate Model | Exact execution gate model | Present | Requires exact command, scope, inputs, outputs, side effects, retention, rollback, incident, security, and human approval. | No future external execution eligibility. |
| P9 adopt-not-rebuild charter | Reuse-before-rebuild policy | Present at current canonical `agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md`; legacy listed filename absent | Preserves adopt/adapt/wrap-before-rebuild under gates. | No ad hoc adoption. |
| P9.1 External Source Root Normalization | Canonical external root | Present | Fixes `4_external/sources` and prevents path presence from becoming permission. | Source scope becomes ambiguous; stop source-dependent decisions. |
| P9.2 License / Trust Intake Model | License and supply-chain model | Present | Keeps license/trust/dependency evidence separate from adoption approval. | Adoption implementation remains blocked. |
| P9.3 Source Inspection Permission Gate | Source review gate | Present | Confirms source review is exact-scope and distinct from execution/adoption. | No source-derived decision expansion. |
| P9.5 Vendor/Fork/Wrapper/Submodule model | Adoption-mode vocabulary | Present at corrected `agent_platform_external_tool_vendor_fork_wrapper_submodule_decision_model.md`; listed filename absent | Constrains P11.4 options and favors isolation/reversibility. | P11.4 cannot claim implementation-ready mode. |
| P9.6 Rollback / Incident Protocol | Rollback and incident posture | Present | Supplies STOP, containment, safe metadata, human escalation, and no-automatic-remediation rules. | Any future activation remains blocked. |
| P3.BR Activation Decision Reconciliation Closure | Reconciled activation posture | Missing at exact listed path | P3.3-P3.5 directly record accepted deferred decisions and P3.5 records reconciliation. | No activation inference; defer to direct decisions. |
| P3.3 Tool Execution Activation Decision | Tool execution posture | Present | Tool execution is deferred; metadata and availability are not permission. | Tool execution blocked. |
| P3.4 Provider/Auth/API/MCP Activation Decision | Provider/network posture | Present | Provider/auth/API/MCP activation remains deferred. | Provider/model runtime blocked. |
| P3.5 Agent Runtime Activation Decision | Agent runtime posture | Present | Agent runtime, scheduler, orchestration, tasks, and autonomous loops remain deferred. | Runtime activation blocked. |
| P6.7 Operational Readiness Audit | Operational closure | Missing at exact listed path | P6.1-P6.5 direct contracts are consumed; no unique P6.7 closure claim is made. | Future operational activation requires fresh reconciliation. |
| P6.1 Agent Registry / Capability Registry | Agent/capability metadata boundary | Present | AGENT PLATFORM owns taxonomy, capabilities, eligibility, and blockers. | No agent registration/runtime inference. |
| P6.2 Agent-to-Agent Communication Protocol | Message/handoff boundary | Present | Protocol metadata is not dispatch; Hermes subagent mechanics must conform later. | No autonomous message/handoff runtime. |
| P6.3 Shared Context / Evidence Bus | Context/evidence boundary | Present | Context and evidence remain refs; no bus runtime or authority. | No automatic context movement or persistence. |
| P6.4 Human Approval / Review Loop | Approval semantics | Present | ApprovalRef is not approval; exact human decision remains mandatory. | No approval-dependent execution. |
| P6.5 Runtime Monitoring / Incident Handling | Observation/incident boundary | Present | Monitoring and incident objects remain metadata; telemetry/automation are not inferred. | No active monitoring or incident automation. |
| P2.1 Shared Metadata Vocabulary | Shared names/statuses | Present | Supplies blocker, ref, source, sensitivity, decision, and lifecycle vocabulary. | Record remains terminology-limited. |
| P2.2 EvidenceRef Contract | Evidence semantics | Present | Evidence supports; it does not decide or activate. | No evidence-based authority claim. |
| P2.3 Audit / Retention / Rollback Baseline | Lifecycle controls | Present | Requires retention, rollback, incident, publication, and tracking posture. | Future stateful runtime blocked. |
| P1.4 Agent Runtime Boundary | Agent/task/handoff metadata boundary | Present | Agent metadata is not agent execution. | No runtime activation. |
| P1.3 Tool Execution Boundary | Tool metadata boundary | Present | Tool availability is not permission. | No tool/shell activation. |
| P1.2 Provider Adapter Metadata Boundary | Provider metadata boundary | Present | Provider metadata is not provider activation. | No provider route activation. |
| P1.1 Context Runtime Boundary | Context/source boundary | Present | Context inclusion is not permission. | No source loading. |
| P1.5 Cognitive Semantic System hardening | Semantic/substrate boundary | Present | Preserves substrate-neutral, non-runtime posture. | No substrate implementation. |
| P0.1/P0.2/P0.3 control-plane records | Activation, validation, security gates | Present | Gate maps/designs constrain but do not activate. | Higher activation levels remain blocked. |
| S-03 Local-Only / Secrets / Credentials Policy | Sensitive/local state policy | Present | Blocks secret, credential, `.env`, provider config, auth, and local-state access. | Stop on sensitive material. |
| S-04 Tool / Shell / Network / MCP Policy | Execution policy | Present | Requires exact future approval for every execution/network/server surface. | No execution. |
| Cognitive Semantic System ADR/audit | Naming/substrate posture | ADR present; listed decision-audit filename missing | Uses accepted name and deferred substrate. | No substrate selection or implementation. |
| README / `.gitignore` / `.graphifyignore` | Repository and local/generated-source boundaries | Present | Confirms metadata-only platform, ignored external/product/artifact roots, and Graphify evidence boundary. | No source/tracking/Graphify expansion. |

Absent non-P11 historical filenames do not grant permission and do not invalidate the direct P11 evidence. Their absence requires the stricter interpretation: no activation, no authority promotion, no generated-output import, and no implementation-ready claim.

## Dependency Posture

- P11.3 depends serially on accepted P11.0, P11.1, and P11.2. All are present.
- P11.3 does not synthesize or replace P11.1 or P11.2.
- P11.1's license, SBOM, lazy-install, high-privilege tool, sensitive state, network, and unverified shutdown blockers remain active.
- P11.2's static-only, unvalidated runtime, broad shell, provider, dashboard, plugin, memory, and Kanban findings remain active.
- Those findings do not prevent a conservative ownership decision; they prevent adoption implementation and runtime activation.
- P11.4 owns adoption mode and must carry all P11.1/P11.2/P11.3 blockers.
- P11.5 owns interface design and cannot alter P11.3 authority allocations.
- P11.6 owns any separately authorized local shell spike and must obey P11.3 constraints.

## Decision Summary

The accepted strategic split is:

```text
Hermes owns worker runtime and execution lifecycle.
AGENT PLATFORM owns policy, permissions and cross-tool authority.
Paperclip will own canonical project and task state.
GBrain owns durable knowledge and hybrid retrieval.
Graphify remains evidence-only.
```

Every Hermes ownership statement is conditional on a future exact controlled-runtime gate and a stable adapter. Nothing is active now.

Kanban provisional decision:

```text
hermes_kanban_provisional_control_plane
```

This selection permits a future, local, adapter-isolated Hermes runtime queue as a temporary MVP execution projection. Hermes Kanban is not canonical task authority. It may not own projects, organizational tasks, approvals, budgets, taxonomy, policy, or durable audit truth. Its state must be replaceable, exportable, inventory-tracked, and migratable to Paperclip.

## Decision Model

Ownership categories:

| Category | Meaning |
| --- | --- |
| `hermes_owns` | Conditional ownership of internal worker/session execution mechanics after a future gate. |
| `agent_platform_owns` | Canonical policy, permission, contract, authority, security, observability, and lifecycle-rule ownership. |
| `paperclip_future_owns` | Future canonical project/work/task/control-plane ownership. |
| `gbrain_future_owns` | Durable knowledge, cited memory, and hybrid retrieval ownership. |
| `graphify_evidence_only` | Derived repository evidence and visualization only. |
| `shared_under_adapter` | Hermes mechanics governed through AGENT PLATFORM contracts and ports. |
| `provisional_mvp_only` | Replaceable temporary implementation with mandatory migration/removal path. |
| `blocked` | Not permitted without a new exact gate. |
| `deferred` | Decision reserved for a later named ticket. |
| `unknown_pending_followup` | Evidence insufficient; no permissive inference. |

| Surface | Recommended owner | Allowed MVP status | Blocked interpretation | Future migration requirement |
| --- | --- | --- | --- | --- |
| Agent session | `shared_under_adapter` | Hermes may run one bounded session after future gate. | Hermes owns agent policy or taxonomy. | Session contract remains runtime-portable. |
| Tool invocation | `agent_platform_owns` policy; Hermes mechanism | Disabled now; selective future allowlist only. | Hermes registry grants permission. | Tool decisions remain platform contracts. |
| Worker process | `hermes_owns` mechanics | Future controlled worker only. | Unsupervised or autonomous worker. | Worker can be stopped/replaced through adapter. |
| Task heartbeat | Hermes emits; AGENT PLATFORM defines semantics | Runtime-health metadata only after gate. | Heartbeat changes canonical task status by itself. | Paperclip later consumes normalized liveness. |
| Dispatcher cadence | `shared_under_adapter` | Bounded provisional dispatch after gate. | Dispatcher chooses organizational priorities or creates authority. | Paperclip supplies canonical assignments later. |
| Cron | `blocked` | None. | General scheduling authority. | Separate exact Cadence gate required. |
| Retry | Hermes attempt-level mechanics; platform policy | Bounded retry inside one approved attempt after gate. | Unbounded task re-execution. | Paperclip owns task-level retry/requeue policy. |
| Reclaim | Hermes detection; platform/Paperclip decision | Bounded abandoned-worker recovery after gate. | Hermes reassigns canonical tasks autonomously. | Paperclip owns canonical claim transition. |
| Task timeout | `agent_platform_owns` policy; Hermes enforcement | Explicit deadline per approved attempt. | Hermes invents timeout policy. | Paperclip stores canonical deadline later. |
| Session timeout | `shared_under_adapter` | Explicit bounded session timeout. | Persistent unattended session. | Runtime-neutral timeout contract. |
| Workspace lifecycle | `shared_under_adapter` | Temporary exact-scope workspace after gate. | Hermes owns user workspace or mutates user Git. | WorkspaceReference remains portable. |
| Shutdown | `shared_under_adapter` | Mandatory before any future run. | Best-effort-only or hidden processes. | ShutdownRollbackPort. |
| Checkpoint | AGENT PLATFORM policy; Hermes mechanism | Explicit ephemeral checkpoint only after gate. | Checkpoint becomes durable task/knowledge authority. | Portable CheckpointReference. |
| Task state | `paperclip_future_owns` | Hermes projection only. | Hermes task DB as permanent truth. | Full schema and ID migration. |
| Event state | AGENT PLATFORM policy; Paperclip future work audit | Runtime events may be emitted after gate. | Local events become authority. | RuntimeEvent mapping and retention. |
| Log state | `agent_platform_owns` policy | Minimal bounded runtime evidence after gate. | Logs as authority or unrestricted telemetry. | Unified observability ingestion contract. |
| Provider/model routing | `agent_platform_owns` route authority; Hermes mechanism deferred | None now. | Model selection as authority routing. | ProviderRoute adapter after exact gate. |
| Skill execution | `agent_platform_owns` capability authority | Disabled now. | Skill files override governance. | SkillCapabilityProfile if later approved. |
| Subagent execution | `shared_under_adapter` | Disabled now; bounded children only after gate. | Child agents own taxonomy or spawn recursively without limits. | AgentCapabilityProfile and FailureEnvelope. |
| Memory write | AGENT PLATFORM policy; GBrain durable authority | Hermes runtime memory disabled for initial spike. | Hermes writes durable facts/decisions. | MemoryWriteCandidate promotion route. |
| Memory read | GBrain future durable read; Hermes local session read | Session-local only after gate. | Hermes memory replaces GBrain. | KnowledgeMemoryPort. |
| Human review | `agent_platform_owns` semantics; Paperclip future workflow state | Manual exact review only. | Hermes review status equals approval. | ApprovalBoundaryPort and Paperclip mapping. |
| Approval state | AGENT PLATFORM/human now; Paperclip future workflow | No Hermes canonical approval state. | ApprovalRef or Hermes status grants permission. | Approval mapping to Paperclip. |
| Project state | `paperclip_future_owns` | None in Hermes. | Hermes board/project as canonical. | Paperclip-only canonical project IDs. |
| Budget state | `paperclip_future_owns` under platform policy | Attempt resource cap only, not canonical budget. | Hermes usage counters authorize spend. | Budget references map to Paperclip. |
| Dependency state | `paperclip_future_owns` for work dependencies | Hermes task-link projection only if provisional. | Hermes dependency graph is organizational truth. | Dependency edge migration. |
| Audit state | AGENT PLATFORM policy; Paperclip future work audit | Safe runtime evidence only. | Hermes logs/events self-approve. | Canonical audit mapping and retention. |

## Ownership Boundary Matrix

| Runtime or state surface | Hermes ownership decision | AGENT PLATFORM ownership decision | Paperclip ownership decision | GBrain ownership decision | Graphify posture | Allowed MVP posture | Blocked posture | Required adapter boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Agent session lifecycle | Run bounded session mechanics after gate. | Defines profile, capabilities, limits, interruption, retention. | References work attempt later. | No ownership. | Evidence-only. | One controlled session candidate. | Autonomous/persistent session. | `AgentRuntimePort` |
| Worker runtime lifecycle | Start/observe/stop worker mechanics after gate. | Authorizes worker and defines resource/scope policy. | Supplies assigned work later. | No ownership. | Evidence-only. | Replaceable local worker. | Unsupervised worker fleet. | `AgentRuntimePort` |
| Tool invocation lifecycle | Dispatch only approved calls. | Owns tool permissions, risk, approval, exact scope. | May reference task-authorized capability later. | No ownership. | Evidence-only. | Future one-tool allowlist. | Wholesale Hermes toolset. | `ApprovalBoundaryPort` plus tool contract |
| Shell command lifecycle | Execute only exact approved command after later gate. | Owns command gate, cwd, environment, timeout, output, rollback. | May associate command with work attempt. | No ownership. | Evidence-only. | Not allowed by P11.3. | Generic shell, sudo, packages, Git mutation. | `WorkspaceBoundaryPort` and execution contract |
| Workspace allocation | Allocate isolated workspace after gate. | Owns allowed root, source class, sensitivity, mount and cleanup rules. | Associates workspace with work item later. | No ownership. | Evidence-only. | Temporary exact-scope candidate. | User/product/external workspace expansion. | `WorkspaceBoundaryPort` |
| Workspace cleanup | Perform adapter-requested cleanup. | Defines evidence retention and cleanup acceptance. | Records work closure later. | No ownership. | Evidence-only. | Mandatory after future run. | Residual unknown files. | `ShutdownRollbackPort` |
| Temporary workspace state | Runtime-local and disposable. | Owns classification and retention. | References artifact metadata later. | No ownership. | Evidence-only. | Ephemeral only. | Silent persistence. | `WorkspaceBoundaryPort` |
| Persistent workspace state | No default ownership. | Governs any future exception. | Owns canonical work/artifact refs later. | Owns durable knowledge only after promotion. | Evidence-only. | None. | Hermes-owned durable workspace. | Deferred contract |
| Subagent lifecycle | Child-process/context mechanics after gate. | Owns role, capability, depth, concurrency, permissions. | Links child attempt to task later. | No ownership. | Evidence-only. | Disabled for initial spike. | Recursive autonomous swarm. | `AgentRuntimePort` |
| Skill loading | Load only approved immutable skill refs after gate. | Owns provenance, trust, capability, instruction priority. | No direct ownership. | May own cited knowledge, not executable instruction. | Evidence-only. | Disabled initially. | Source-local skills as authority. | Capability registry contract |
| Skill execution | Mechanism only after separate gate. | Owns permission and review. | May associate skill with work packet later. | No ownership. | Evidence-only. | None now. | Self-improvement or mutation. | `ApprovalBoundaryPort` |
| Provider/model routing | Route only a platform-approved ProviderRoute after gate. | Owns provider selection, credentials boundary, data, cost, retention. | May carry budget/policy refs later. | No ownership. | Evidence-only. | None now. | Provider config/auth use. | Future provider adapter |
| Session memory | Runtime-local transcript/recall mechanics. | Owns retention, redaction, access, deletion. | May reference attempt metadata. | No canonical ownership. | Evidence-only. | Ephemeral session only after gate. | Durable factual truth. | `KnowledgeMemoryPort` |
| Procedural memory | Candidate runtime layer only after explicit policy. | Owns write eligibility and promotion review. | No direct ownership. | May receive promoted durable knowledge through future contract. | Evidence-only. | Disabled initially. | Autonomous self-modification. | `KnowledgeMemoryPort` |
| Durable knowledge memory | No ownership. | Owns boundary and promotion policy. | May reference project/task knowledge. | Canonical owner. | Evidence visualization only. | None in Hermes. | Hermes as durable knowledge authority. | `KnowledgeMemoryPort` |
| Task planning | May return proposal evidence. | Owns planning authority and permission semantics. | Future canonical plan/task owner. | Supplies knowledge only. | Evidence-only. | Manual proposal only. | Auto-decompose as authority. | `WorkControlPlanePort` |
| Task state | Provisional runtime projection only. | Defines allowed projection fields. | Future canonical owner. | No ownership. | Evidence-only. | Adapter-isolated temporary state. | Permanent Hermes task truth. | `WorkControlPlanePort` |
| Task dependencies | Temporary projection if needed. | Defines semantics. | Future canonical owner. | No ownership. | Evidence-only. | Migration-ready projection. | Competing dependency graph. | `WorkControlPlanePort` |
| Task assignment | Execute supplied assignment only. | Owns assignment policy until Paperclip. | Future canonical owner. | No ownership. | Evidence-only. | Manual/platform-approved assignment. | Hermes selects organizational assignee. | `WorkControlPlanePort` |
| Task heartbeat | Emit worker liveness only. | Defines schema, TTL, privacy, incident thresholds. | Future canonical consumer/owner of work status. | No ownership. | Evidence-only. | Runtime metadata after gate. | Heartbeat equals task approval/completion. | `RuntimeEventPort` |
| Task retry | Retry a failed worker attempt within explicit cap. | Defines cap, backoff, retryability, approval escalation. | Future task-level retry owner. | No ownership. | Evidence-only. | Disabled until exact gate. | Unbounded autonomous retry. | `WorkControlPlanePort` |
| Task reclaim | Detect and report abandoned runtime claim. | Defines reclaim policy and authorization. | Future canonical claim owner. | No ownership. | Evidence-only. | Disabled until exact gate. | Hermes silently reassigns canonical task. | `WorkControlPlanePort` |
| Task timeout | Enforce supplied attempt timeout. | Owns timeout policy and exception approval. | Future canonical task deadline owner. | No ownership. | Evidence-only. | Explicit finite limit. | Hermes-defined policy. | `AgentRuntimePort` |
| Dispatcher cadence | Run bounded assignment polling/tick only after gate. | Owns cadence, input queue, concurrency, stop and incident policy. | Future assignment source/owner. | No ownership. | Evidence-only. | Provisional local mechanism. | Autonomous planning/priority authority. | `WorkControlPlanePort` |
| Cron/scheduled jobs | No approved ownership. | Owns future exact schedule gate. | May own scheduled work records later. | No ownership. | Evidence-only. | None. | Cron or unattended scheduling. | Future `CadenceRuntimePort` only |
| Approval state | Runtime prompt can request approval, not decide it. | Canonical human/governance authority. | Future workflow-state owner. | No ownership. | Evidence-only. | Manual external decision. | Hermes self-approval. | `ApprovalBoundaryPort` |
| Human review state | May emit review request/result evidence. | Owns review semantics and acceptance. | Future canonical workflow state. | No ownership. | Evidence-only. | Metadata only. | Local review flag as canonical approval. | `ApprovalBoundaryPort` |
| Event logs | Emit normalized runtime events after gate. | Owns schema, sensitivity, retention, aggregation. | Future work-event/audit owner. | No ownership. | May visualize curated evidence. | Minimal safe events. | Raw logs as authority/telemetry. | `RuntimeEventPort` |
| Runtime logs | Produce bounded diagnostics after gate. | Owns redaction, retention, incident, access, unified observability. | May reference work attempt logs. | No ownership. | Evidence-only summaries. | Warning/error minimum. | Unlimited transcript/tool logging. | `RuntimeEventPort` |
| Audit logs | No canonical ownership. | Owns audit policy. | Future canonical work audit. | Knowledge citations separate. | Evidence-only. | Safe metadata refs. | Hermes-generated audit as truth. | `RuntimeEventPort` |
| Dashboard state | Local UI state only if later approved. | Owns management authority and auth policy. | Future task/project UI authority. | No ownership. | Visualization only. | Disabled. | Dashboard grants authority. | Deferred UI adapter |
| Proxy state | No approved ownership. | Owns network/security policy. | No default ownership. | No ownership. | Evidence-only. | Disabled. | Proxy/service activation. | Future service gate |
| External messaging channels | Delivery mechanism only if later approved. | Owns channel, identity, allowlist, content, retention. | May own notification refs later. | No ownership. | Evidence-only. | Disabled. | Messaging as command authority. | Future channel port |
| Computer use | Mechanism only if future gate. | Owns permission and safety. | May associate with attempt later. | No ownership. | Evidence-only. | Disabled. | Desktop control. | Future exact tool adapter |
| Browser tooling | Mechanism only if future gate. | Owns URL, data, auth, download, state policy. | May associate with attempt later. | No ownership. | Evidence-only. | Disabled. | OAuth/browser-auth use. | Future exact tool adapter |
| Shutdown | Execute deterministic stop procedure. | Owns acceptance criteria and kill authority. | Records attempt termination later. | No ownership. | Evidence-only. | Mandatory. | Orphan processes/services. | `ShutdownRollbackPort` |
| Checkpoint | Create/restore only explicit portable checkpoint after gate. | Owns format, retention, validity, security, restore approval. | May reference attempt checkpoint later. | Durable knowledge excluded. | Evidence-only. | Ephemeral candidate only. | Hidden durable state. | `ShutdownRollbackPort` |
| Resume | Resume only from approved checkpoint and work assignment. | Owns resume policy. | Future task/attempt owner. | No ownership. | Evidence-only. | Disabled initially. | Automatic replay. | `AgentRuntimePort` |
| Cancellation | Cancel worker/session/tool/subagent mechanics. | Owns cancellation authority and deadlines. | Future task cancellation owner. | No ownership. | Evidence-only. | Mandatory interface. | Best-effort-only cancellation. | `ShutdownRollbackPort` |
| Failure envelope | Produce normalized failure evidence. | Owns severity, disclosure, retryability, incident routing. | Future attempt/failure owner. | No ownership. | Evidence-only. | Required. | Raw sensitive exception dump. | `RuntimeEventPort` |

## Runtime Boundary

Hermes may own runtime mechanics only behind stable adapters and only after a future controlled runtime gate.

Hermes may later:

- instantiate and stop bounded agent sessions;
- supervise approved worker processes;
- enforce supplied iteration, time, resource, and cancellation limits;
- dispatch only platform-approved tool invocations;
- allocate and clean exact-scope temporary workspaces;
- run bounded subagent mechanics under platform-defined roles and limits;
- create runtime-local checkpoints under explicit policy;
- emit normalized runtime events, failures, liveness, and shutdown results.

Hermes must not:

- define AGENT PLATFORM policy, ontology, taxonomy, permissions, or cross-tool authority;
- decide canonical projects, tasks, dependencies, assignments, approvals, budgets, or audit truth;
- decide provider/auth/API/MCP authority;
- become durable knowledge authority;
- turn source-local tools, skills, plugins, dashboards, or statuses into permission;
- start any worker, shell, tool, service, listener, scheduler, dispatcher, or loop from P11.3.

## Cadence Boundary

Cadence surfaces include cron, scheduled tasks, background workers, always-on agents, watchers, heartbeats, dispatcher loops, retry loops, reclaim loops, Dream/maintenance cycles, memory maintenance, dashboard refresh, event streaming, provider polling, and external message channels.

Cadence is not broadly approved.

| Cadence surface | P11.3 decision |
| --- | --- |
| Worker heartbeat | Future candidate only as bounded runtime-health metadata for one approved worker attempt. It cannot approve, complete, assign, or prioritize a task. |
| Task heartbeat | Canonical semantics belong to AGENT PLATFORM and future Paperclip. Hermes may emit liveness through `RuntimeEventPort`. |
| Dispatcher cadence | Future candidate only as an adapter-bounded mechanism that consumes approved assignments. Cadence, concurrency, tick interval, stop, and failure policy remain external. |
| Retry loop | Future candidate only inside one approved work attempt with finite retries, classified errors, bounded backoff, and escalation. |
| Reclaim loop | Future candidate only to detect and recover abandoned worker execution; canonical task reassignment requires platform/Paperclip decision. |
| Task timeout | Platform-defined finite timeout enforced by Hermes. |
| Session timeout | Platform-defined finite timeout enforced by Hermes. |
| Cron | Blocked until a separate exact schedule and Cadence gate. |
| Scheduled tasks | Blocked until canonical work ownership, approval, retention, and incident policy exist. |
| Always-on agents | Blocked. |
| Watchers/background services | Blocked except a future exact runtime-health mechanism. |
| Dream/maintenance cycles | Blocked until memory authority, review, provenance, write, retention, and rollback policies approve exact behavior. |
| Memory maintenance | Blocked. |
| Dashboard refresh | No authority; dashboard remains inactive. |
| Event streaming/telemetry | Blocked. Future bounded event emission is not a streaming approval. |
| Provider polling/model catalog refresh | Blocked. |
| External messaging cadence | Blocked. |

Retry and reclaim are recovery mechanics, not autonomous task authority. Any policy value embedded in Hermes must be overridden or constrained by adapter input before future use.

## Kanban Provisional Decision

Selected posture:

```text
hermes_kanban_provisional_control_plane
```

The term `provisional_control_plane` means a temporary local execution queue implementation behind `WorkControlPlanePort`. It does not mean canonical organizational authority.

Decision criteria:

| Criterion | Decision |
| --- | --- |
| Competes with Paperclip future authority | Yes if exposed directly; therefore direct/canonical use is prohibited. |
| Isolatable behind `WorkControlPlanePort` | Yes according to P11.2 mapping; required before use. |
| Migratable/replaceable state | Possible if IDs, states, dependencies, assignments, attempts, events, approvals, failures, and archives are mapped first. |
| AGENT PLATFORM authority preserved | Yes only if policy/permissions remain outside Hermes. |
| Paperclip can later become canonical | Yes only with no permanent dual authority and a tested cutover/rollback contract. |
| Can be disabled/bypassed | Required. P11.5 must provide bypass and no-Kanban path. |
| Can avoid unsafe Cadence | Yes only with auto-decompose, cron, gateway embedding, and autonomous loops disabled by default. |
| Can avoid provider/auth exposure | Yes for queue mechanics; provider-dependent planning remains blocked. |
| Can avoid product source access | Yes; product/Siamese source remains excluded. |

Allowed future MVP use after all later gates:

- a single-host, local, bounded execution queue;
- projection of already approved work packets;
- worker attempt, liveness, failure, cancellation, and completion mechanics;
- temporary task dependencies needed to sequence approved runtime work;
- normalized runtime events and comments as evidence;
- explicit, bounded dispatcher operation only after P11.7/P11.8 approval.

Blocked use:

- canonical project, task, budget, approval, taxonomy, or organizational audit authority;
- autonomous task creation or auto-decomposition;
- unrestricted dispatcher, retry, reclaim, heartbeat, cron, or always-on loops;
- external messaging, dashboard, provider/model planning, browser, computer-use, or product integration;
- permanent task DB, permanent dual authority, or direct consumers coupled to Hermes schemas;
- treating comments, events, review status, heartbeats, or attempts as canonical truth.

Required operating conditions before any provisional use:

- complete state-location inventory;
- dedicated local data root;
- schema/version identification;
- exact retention and deletion policy;
- backup and rollback route;
- deterministic shutdown and kill switch;
- cleanup and residual-state verification;
- incident route;
- no hidden service or public port;
- no direct UI/client dependency on Hermes Kanban schemas;
- export and Paperclip migration contract accepted before activation.

## Kanban Swarm Boundary

- The planner may propose plans as evidence; AGENT PLATFORM governs whether work exists and may proceed.
- The dispatcher may assign a supplied approved work packet to a Hermes worker only after a future exact gate.
- Heartbeats report worker liveness only.
- Retries recover one bounded worker attempt only under external policy.
- Reclaim detects abandoned runtime work and requests a controlled state transition; it does not autonomously reassign canonical work.
- The Hermes Kanban database is provisional runtime state, never permanent canonical task storage.
- SQLite tasks, comments, events, runs, attachments, and notifications require inventory, retention, backup, rollback, cleanup, and migration controls.
- Kanban comments, events, attempts, and failure records are runtime evidence, not organizational truth by default.
- Auto-decomposition and recursive worker fan-out remain blocked.

## Workspace Boundary

Hermes workspace handling is a candidate isolated-execution mechanism, not workspace authority.

Requirements:

- allocation occurs only through `WorkspaceBoundaryPort`;
- every workspace has an exact root, source class, owner, purpose, lifetime, sensitivity, and cleanup plan;
- temporary workspaces are preferred and must be deleted or quarantined according to reviewed retention policy;
- persistent workspaces require a separate explicit gate and retention contract;
- workspace paths must not broaden through fallback behavior;
- no user Git mutation, branch/worktree creation, checkout, reset, staging, commit, push, or cleanup command without a future exact Git gate;
- residual files, caches, logs, checkpoints, process files, browser state, and mounted paths must be inventoried;
- no secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, or API keys may enter workspace state;
- no product/Siamese source may enter a Hermes workspace without a future product gate;
- no external source outside exact authorized scope may enter the workspace.

Workspace cleanup is part of successful execution, not optional maintenance.

## Shutdown / Checkpoint Boundary

Hermes runtime must be reversible. Any future activation requires:

| Requirement | Boundary |
| --- | --- |
| Shutdown procedure | Deterministically stop session, worker, tools, child processes, and adapter-owned services. |
| Kill switch | AGENT PLATFORM-controlled immediate stop independent of Hermes task state. |
| Worker cancellation | Finite grace period followed by controlled termination and incident evidence. |
| Session cancellation | Interrupt loop and reject new work. |
| Tool cancellation | Cancel or terminate approved tool invocation without starting adjacent actions. |
| Subagent cancellation | Recursively stop approved children within bounded depth. |
| Workspace cleanup | Close handles, stop processes, inventory and remove/quarantine residual state. |
| Checkpoint creation | Explicit, versioned, scoped, sensitive-data-reviewed, and optional. |
| Checkpoint retention | Time-bounded with owner, reason, deletion, and incident posture. |
| Checkpoint restore | Separate approval; validate runtime/source/config compatibility before use. |
| Checkpoint invalidation | Invalidate on version, policy, capability, provider, schema, or source-scope drift. |
| Provider revocation | Required posture if a later runtime ever uses providers; not exercised here. |
| State inventory | List every state root, file class, DB, log, cache, process, service, and port. |
| Residual-state inventory | Required after shutdown and uninstall. |
| Rollback route | Disable adapter, stop runtime, restore pre-run state, preserve safe evidence, remove/quarantine residuals. |
| Incident route | P6.5/P9.6-aligned human/security/governance escalation. |

Checkpoint is not task authority, approval, durable knowledge, or guaranteed resume. A future checkpoint format must remain replaceable and portable through `CheckpointReference`.

## Memory Boundary

Hermes Memory and GBrain remain separate layers.

| Memory class | Owner and boundary |
| --- | --- |
| Session transcript/context | Hermes runtime-local mechanism after gate; AGENT PLATFORM controls retention, redaction, access, and deletion. |
| Collaboration context | Hermes may hold ephemeral runtime context after gate. |
| Preferences/procedural learning | Future candidate only with opt-in write, provenance, review, rollback, and promotion policy. |
| Runtime experience | Evidence candidate, not fact authority. |
| Durable facts/decisions/documents | GBrain owns durable knowledge. |
| Project/person/world knowledge | GBrain owns durable cited knowledge and hybrid retrieval. |
| Factual single source of truth | Hermes memory is prohibited from this role. |
| Physical database fusion | Prohibited by P11.3. |
| Hermes-to-GBrain write | Future `MemoryWriteCandidate` contract required; no direct write. |
| GBrain-to-Hermes read | Future `KnowledgeMemoryPort` with provenance, scope, freshness, and permission required. |
| Dream/maintenance cycles | Blocked pending explicit authority, review, retention, and Cadence gates. |

Hermes procedural memory is not durable world knowledge. GBrain durable knowledge is not physically fused with Hermes memory by P11.3.

## Provider / Model Boundary

- Hermes provider/model routing is architecturally useful but not approved by P11.3.
- AGENT PLATFORM owns provider route policy, model eligibility, auth scope, data exposure, cost, retention, and revocation.
- Provider/auth/API/MCP remains blocked until an exact future gate.
- P11.3 does not inspect or store provider configuration or credentials.
- Model routing is not authority routing.
- Provider/model output is generated evidence unless separately governed.
- P11.5 may design a future provider-neutral reference boundary but may not configure or call a provider.

## Tool / Shell Boundary

- Hermes tool execution is not approved by P11.3.
- Hermes shell execution is not approved by P11.3.
- Tool invocation requires AGENT PLATFORM permission contracts and exact capability allowlists.
- Shell invocation requires exact command, cwd, environment, input/output, timeout, side-effect, retention, rollback, incident, and human approval gates.
- Dangerous and destructive commands remain blocked.
- `sudo`, package managers, builds, tests, scripts, network calls, service startup, and Git mutation remain blocked unless a future exact gate explicitly approves one action.
- Tool availability, registration, plugin discovery, or model request is not permission.

## Computer Use / Browser Boundary

- Computer use remains blocked.
- Browser automation remains blocked.
- OAuth, browser auth, cookies, profiles, downloads, and browser credential state remain blocked.
- External messaging remains blocked.
- Dashboard browsing or UI presence does not approve runtime activation.
- Any future browser/computer-use request requires its own exact tool, network, credential, workspace, privacy, output, shutdown, and incident gates.

## Human Review / Approval Boundary

- Hermes may later present an approval request, but AGENT PLATFORM owns approval authority.
- `ApprovalRef` is not approval.
- Hermes human-review, blocked, review, comment, or prompt state is runtime evidence, not canonical approval.
- P6.4 remains authoritative for exact-scope human approval semantics.
- Paperclip may later own canonical approval workflow state, while AGENT PLATFORM retains approval policy and human/governance authority.
- No Hermes component may self-approve, infer approval from task state, or continue after approval expiration/denial.

## Observability Boundary

- Hermes runtime events and logs may later supply useful execution evidence.
- AGENT PLATFORM owns unified observability policy, event schema, sensitivity, redaction, retention, access, incident, and publication posture.
- Runtime logs are generated evidence, not authority.
- Hermes events must cross `RuntimeEventPort`; consumers must not depend directly on internal log/DB schemas.
- Paperclip may later own canonical work-attempt/audit events.
- Graphify may visualize curated repository evidence only; it is not a runtime observability authority.
- Telemetry, external observability backends, event streaming, polling, and remote analytics remain blocked.

## Migration Boundary To Paperclip

If Hermes Kanban is used, it must be adapter-isolated and its state must remain provisional. Paperclip is the target canonical project/task/work state owner.

Migration contract requirements:

| State class | Required mapping |
| --- | --- |
| Task IDs | Stable platform/Paperclip ID plus temporary Hermes projection ID; no Hermes-only IDs exposed as permanent API. |
| Task state | Explicit state-machine mapping with invalid/unmapped state handling. |
| Dependencies | Direction, type, blocking semantics, cycles, and deleted-edge behavior. |
| Assignments | Agent/profile identity mapping to AGENT PLATFORM registry and Paperclip assignees. |
| Heartbeats | Runtime-liveness event mapping; never approval or canonical completion. |
| Comments/events | Provenance, actor, timestamp, sensitivity, retention, and authority classification. |
| Attempts/retries | Attempt identity, outcome, retry reason, retry budget, failure envelope, and cancellation. |
| Approval | No automatic mapping from Hermes review state; canonical approval must be re-bound to P6.4/Paperclip workflow. |
| Audit | Safe event mapping with evidence refs, retention, rollback, and incident refs. |
| Failures | FailureEnvelope, retryability, incident severity, residual state, and final disposition. |
| Rollback | Cut back to previous control plane without losing accepted canonical state. |
| Archive/deprecation | Freeze writes, export, validate counts/relationships, archive or remove provisional DB, disable adapter route. |

Hard boundary:

```text
No permanent dual task authority is allowed.
```

During cutover, one system must be designated canonical for every field and transition. Hermes Kanban and Paperclip task databases must not remain concurrent writable sources of truth.

## Interface Requirements For P11.5

P11.5 must design, but not implement, at least these stable ports:

| Port | Required responsibility |
| --- | --- |
| `AgentRuntimePort` | Start bounded session/worker, submit one turn/work attempt, interrupt, cancel, report status, checkpoint reference, shutdown. |
| `KnowledgeMemoryPort` | Read scoped cited knowledge; submit reviewed memory-write candidates; prevent physical DB fusion. |
| `WorkControlPlanePort` | Receive approved work packets/assignments and project provisional execution state without exposing Hermes schemas. |
| `RuntimeEventPort` | Emit normalized lifecycle, liveness, tool, failure, cancellation, shutdown, and residual-state evidence. |
| `ApprovalBoundaryPort` | Request and consume exact human/governance decisions without self-approval. |
| `WorkspaceBoundaryPort` | Allocate exact-scope workspace, declare mounts/sources, inventory writes, clean/quarantine residuals. |
| `ShutdownRollbackPort` | Stop runtime, cancel descendants, invoke kill switch, inventory state, rollback adapter route, and report incidents. |

P11.5 must ensure Hermes can be updated, patched, replaced, disabled, or bypassed. It must preserve AGENT PLATFORM ownership of policy and authority, Paperclip's future work-state ownership, GBrain's durable knowledge ownership, and Graphify's evidence-only posture.

## Constraints For P11.6 Local Shell Spike

P11.6 remains separately gated and may proceed only if its own ticket authorizes execution.

Maximum candidate scope:

```text
one minimal local isolated install candidate
one bounded session
one inert or safe task
one low-risk tool only if an exact tool gate permits it
one temporary exact-scope workspace
bounded local log capture
deterministic clean shutdown
```

P11.6 must not include:

- GBrain or Paperclip integration;
- external messaging, dashboard, proxy, browser automation, or computer use;
- cron, Cadence, scheduler, autonomous dispatcher, retries, reclaim, or heartbeat loops;
- persistent Kanban authority;
- hosted production deployment;
- product/Siamese source;
- credentials, `.env`, provider configuration, OAuth, API, or MCP;
- package mutation or network access unless the exact P11.6 gate explicitly and safely authorizes it;
- Git mutation.

P11.6 must measure processes, child processes, ports/listeners, filesystem writes, state locations, workspace residuals, logs, shutdown behavior, kill-switch behavior, cleanup, unexpected provider/network calls, and error/failure behavior. It must stop on any boundary violation.

## Evidence / Validation / Security Interfaces

- Evidence supports; it does not decide.
- Validation evaluates; governance decides.
- Security constrains; it does not activate.
- P11.1/P11.2 are evidence inputs, not runtime approval.
- P2.2 `EvidenceRef` semantics remain binding.
- P2.3 retention, rollback, incident, source-tracking, generated-output, and publication semantics remain binding.
- S-03 and S-04 remain binding.
- Architecture mapping does not become execution approval.
- A passing future validation does not expand permission beyond its exact gate.

## Retention / Rollback / Incident Posture

| Surface | Retention posture | Rollback posture | Incident route |
| --- | --- | --- | --- |
| Hermes runtime state | Minimum necessary, time-bounded, dedicated root | Stop adapter/runtime and restore pre-run state | Runtime/security/governance review |
| Workspace state | Temporary by default; inventory all writes | Cleanup or quarantine exact workspace | Workspace boundary incident |
| Hermes task state | Provisional and migration-ready | Disable writes, export, restore prior canonical route | Work-control authority incident |
| Event logs | Safe normalized metadata only | Stop emission and quarantine unsafe records | Observability/security review |
| Runtime logs | Bounded, redacted, local-only, short retention | Remove/quarantine after preserving safe incident metadata | Logging/data exposure incident |
| Session memory | Ephemeral for minimum profile | Delete/invalidate session state | Memory/privacy incident |
| Procedural memory | Disabled by default | Disable provider/write route and restore prior state | Memory-authority incident |
| Skill state | Immutable/disabled initially | Remove provisional skill changes and invalidate cache | Instruction/supply-chain incident |
| Plugin state | Disabled initially | Disable plugin and remove/quarantine state | Plugin lifecycle incident |
| Provider state | Not permitted by P11.3 | Revoke/disable route if future provider implicated | Credential/provider incident |
| Dashboard/proxy state | Not permitted | Stop service, close port, remove session state | Network/service incident |
| Hermes Kanban SQLite state | Dedicated provisional store only after gate | Freeze, export, restore/disable, archive/remove | Dual-authority/persistence incident |
| Checkpoint state | Optional, versioned, short-lived | Invalidate/remove; never silently replay | Resume/state exposure incident |
| Residual files | Zero unknown residuals accepted | Remove or quarantine after inventory | Cleanup/unknown persistence incident |

Every future Hermes runtime surface requires retention, rollback, and incident posture before activation. Local execution must remain reversible through shutdown, rollback, uninstall, workspace cleanup, state-location inventory, provider revocation if applicable, and kill switch.

## Incident Triggers

Incident triggers include:

- unexpected global install or dependency mutation;
- unexpected persistent service, daemon, watcher, worker, scheduler, or public port;
- shell-profile or system configuration modification;
- unreviewed plugin or lifecycle script execution;
- workspace creation or access outside exact scope;
- destructive command, package-manager action, sudo, or Git mutation;
- secret, credential, `.env`, provider config, token store, browser auth, local credential store, or API key exposure;
- product/Siamese source access;
- external source access outside the P11 gate;
- unexpected network listener, provider/API/MCP call, telemetry, or live connector;
- unexpected persistence, database, event stream, checkpoint, memory write, or residual state;
- Hermes Kanban state competing with Paperclip or AGENT PLATFORM authority;
- unauthorized cron, Cadence, dispatcher, heartbeat, retry, reclaim, Dream, maintenance, or autonomous loop;
- failure to stop, cancel children, close ports, clean workspace, or inventory residuals.

Required response:

1. STOP.
2. Do not repeat unsafe content.
3. Preserve safe metadata only.
4. If a future runtime is active under another ticket, invoke its approved shutdown/kill route.
5. Revoke or disable provider access if implicated.
6. Quarantine residual state without inspecting prohibited content.
7. Record rollback requirement and incident route.
8. Route to human, security, and governance review.
9. Block P11.4/P11.5/P11.6 implementation or execution progression while the incident is unresolved.

## Stop Rules

STOP if:

- P11.0, P11.1, or P11.2 is missing;
- source identity/review scope becomes ambiguous;
- a runtime surface cannot be mapped to an owner and adapter boundary;
- Kanban state cannot be separated from future Paperclip authority;
- Hermes would become project, task, approval, budget, taxonomy, policy, or durable knowledge authority;
- runtime/Cadence ownership cannot be adapter-isolated;
- provider/auth/API/MCP or credentials are required to make this decision;
- secrets, `.env`, provider config, token stores, browser auth, local credential stores, or API keys are implicated;
- product/Siamese source or external source outside P11 authorization is implicated;
- execution, installation, service/shell/dashboard/proxy/worker/dispatcher startup, cron, retry, reclaim, heartbeat, Kanban, tools, subagents, browser, computer use, providers, network, MCP, telemetry, persistence, database, event stream, vector DB, graph DB, embeddings, substrate selection, generated-output tracking, source-tracking expansion, publication, or Git mutation is attempted;
- the PowerPoint license exception, dependency/SBOM blockers, or runtime safety blockers are incorrectly treated as resolved.

## Required P11.3 Invariants

| Invariant | Requirement |
| --- | --- |
| HERMES-CAD-001 | P11.3 creates a Hermes runtime / Cadence boundary decision only. |
| HERMES-CAD-002 | P11.3 does not execute Hermes. |
| HERMES-CAD-003 | P11.3 does not install Hermes. |
| HERMES-CAD-004 | P11.3 does not activate Hermes runtime. |
| HERMES-CAD-005 | P11.3 does not activate Kanban Swarm. |
| HERMES-CAD-006 | P11.3 does not activate Cadence. |
| HERMES-CAD-007 | P11.3 does not start P11.4. |
| HERMES-CAD-008 | Hermes owns worker runtime and execution lifecycle. |
| HERMES-CAD-009 | AGENT PLATFORM owns policy, permissions and cross-tool authority. |
| HERMES-CAD-010 | Paperclip will own canonical project and task state. |
| HERMES-CAD-011 | Hermes Kanban is not canonical task authority. |
| HERMES-CAD-012 | No permanent dual task authority is allowed. |
| HERMES-CAD-013 | Hermes Memory and GBrain remain separate layers. |
| HERMES-CAD-014 | Hermes procedural memory is not durable world knowledge. |
| HERMES-CAD-015 | GBrain durable knowledge is not physically fused with Hermes memory by P11.3. |
| HERMES-CAD-016 | Graphify remains evidence-only. |
| HERMES-CAD-017 | Approval authority remains with AGENT PLATFORM and human approval contracts. |
| HERMES-CAD-018 | Tool execution requires a future exact gate. |
| HERMES-CAD-019 | Provider/auth/API/MCP requires a future exact gate. |
| HERMES-CAD-020 | Product/Siamese source remains blocked. |
| HERMES-CAD-021 | Cron, always-on, Dream, and maintenance cycles require future exact gates. |
| HERMES-CAD-022 | Runtime state requires retention, rollback, and incident posture. |
| HERMES-CAD-023 | Local execution must be reversible. |
| HERMES-CAD-024 | Cognitive Semantic System substrate remains deferred. |
| HERMES-CAD-025 | The agent never mutates Git. |
| HERMES-CAD-026 | Never recommend `git add .`. |

## Future Validation Targets

Proposed only, not executed:

- Hermes runtime ownership matrix completeness;
- Hermes cadence boundary completeness;
- Kanban provisional decision completeness;
- Hermes/Paperclip task authority separation invariant;
- Hermes Memory/GBrain separation invariant;
- AGENT PLATFORM authority preservation invariant;
- worker runtime ownership boundary;
- dispatcher cadence boundary;
- heartbeat/retry/reclaim boundary;
- workspace lifecycle boundary;
- shutdown/checkpoint boundary;
- provider/model boundary;
- tool/shell boundary;
- computer-use/browser boundary;
- human review/approval boundary;
- observability boundary;
- migration-to-Paperclip completeness;
- P11.5 adapter boundary conformance;
- P11.6 spike constraint conformance;
- retention/rollback/incident completeness;
- no-runtime, no-Kanban, no-Cadence, no-provider/auth, no-product-source, and no-Git-mutation invariants.

## Future Hardening Candidates

These are proposals only and are not started:

```text
HERMES-CAD-HARD-01 - Hermes Runtime Ownership Matrix Validation
HERMES-CAD-HARD-02 - Hermes Kanban / Paperclip Migration Contract
HERMES-CAD-HARD-03 - Hermes Workspace Lifecycle Boundary Contract
HERMES-CAD-HARD-04 - Hermes Shutdown / Checkpoint / Rollback Contract
HERMES-CAD-HARD-05 - Hermes Runtime Event / Observability Boundary Contract
HERMES-CAD-HARD-06 - Hermes Memory / GBrain Read-Write Policy Contract
HERMES-CAD-HARD-07 - Hermes Cadence / Cron / Dream Safety Checklist
HERMES-CAD-HARD-08 - Hermes Local Spike Constraint Checklist
```

## Created / Not Created Register

Created:

- Hermes runtime / Cadence boundary decision document;
- runtime ownership and decision-model matrices;
- Cadence boundary;
- Kanban provisional decision and Kanban Swarm boundary;
- workspace lifecycle boundary;
- shutdown/checkpoint/reversibility boundary;
- Hermes Memory/GBrain boundary;
- provider/model, tool/shell, computer-use/browser, human-review/approval, and observability boundaries;
- migration boundary to Paperclip;
- P11.5 interface requirements;
- P11.6 local shell spike constraints;
- retention/rollback/incident posture and incident triggers.

Not created, activated, inspected, executed, or modified:

```text
no Hermes execution or installation
no Hermes shell, dashboard, service, proxy, worker, dispatcher, or Kanban start
no Kanban Swarm, cron, scheduler, orchestration, Cadence, autonomous loop, or subagent activation
no tool or shell execution
no provider/auth/API/MCP activation, credentials, API calls, MCP, or live connectors
no Paperclip, GBrain, GStack, Graphify, Codegraph, or OpenCode execution
no Graphify adoption as authority
no source loading or source inspection outside approved P11 records
no product/Siamese source inspection
no external source inspection outside P11 authorization
no secret, credential, .env, provider config, token store, browser auth,
   local credential store, or API key inspection
no validation, tests, CI, scripts, builds, package managers, or security enforcement
no persistence, database, event stream, SQLite state, workspace state, or telemetry
no vector DB, embeddings, graph DB, ontology runtime, or substrate implementation
no generated output tracking or source tracking expansion approval
no publication or Git mutation
no .gitignore or .graphifyignore modification
no generated-output modification or tracking
no Cognitive Semantic System substrate selection
no P11.4, P11.5, P11.6, P11.7, P11.8, P11.R, P12, P13, or P14 start
```

## Recommended Next Tickets

After P11.3, the next ticket is:

```text
P11.4 - Hermes Adoption Mode Decision
```

P11.4 must consume P11.1, P11.2, and P11.3 and decide among external CLI, Python package, separate service, adapter over Hermes, controlled fork, concrete component extraction, compatible-interface reimplementation, defer after audit, or reject for boundary mismatch.

After P11.4, P11.5 may design interfaces and P11.6 may be considered only under its own exact execution authorization. P11.3 starts none of these tickets.

## Final Verdict

| Question | Answer |
| --- | --- |
| What did P11.3 create? | One canonical documentation-only Hermes runtime / Cadence ownership decision. |
| What boundary was decided? | Hermes may own replaceable worker/session execution mechanics behind adapters; authority, policy, canonical work, and durable knowledge remain outside Hermes. |
| What does Hermes own? | Conditionally, worker runtime and execution lifecycle mechanics after a future exact gate. |
| What does AGENT PLATFORM own? | Policy, permissions, ontology, taxonomy, cross-tool authority, security, contracts, memory boundaries, integration state, approval semantics, and unified observability. |
| What will Paperclip own? | Canonical project, task, dependency, assignment, status, approval-workflow, budget, heartbeat/work-attempt, and organizational audit state. |
| What does GBrain own? | Durable cited knowledge and hybrid retrieval. |
| What is Graphify's posture? | Derived repository evidence map and visualization only; no authority. |
| Is Hermes Kanban canonical task authority? | No. |
| What Kanban decision was selected? | `hermes_kanban_provisional_control_plane`, strictly adapter-isolated and replaceable. |
| What migration is required? | Full ID/state/dependency/assignment/heartbeat/event/attempt/approval/audit/failure/rollback mapping and one canonical writer during Paperclip cutover. |
| What Cadence remains blocked? | Cron, scheduled work, always-on agents, broad watchers, autonomous planning, unbounded retry/reclaim, Dream/memory maintenance, provider polling, event streaming, telemetry, and external messaging cadence. |
| What runtime may Hermes own behind adapters? | Sessions, workers, bounded tool dispatch, temporary workspaces, bounded subagents, checkpoints, failures, liveness, cancellation, cleanup, and shutdown mechanics after later gates. |
| What remains AGENT PLATFORM-owned? | Every policy, permission, authority, contract, lifecycle rule, security decision, approval decision, provider route decision, and observability policy. |
| What is reserved for Paperclip? | Canonical project/task/work-control-plane state. |
| What memory boundary applies? | Hermes may hold ephemeral/session/procedural runtime memory; GBrain owns durable facts, decisions, documents, project/person/world knowledge, and hybrid retrieval. No physical fusion. |
| What reversibility is required? | Deterministic shutdown, kill switch, cancellation, cleanup, state/residual inventory, checkpoint invalidation, rollback, uninstall, provider revocation posture, and incident route. |
| What must P11.5 consume? | The seven required ports and every ownership/non-authority boundary in this record. |
| What must P11.6 obey? | Minimal isolated one-session scope, temporary workspace, exact future tool gate, measurement and clean shutdown, with no integrations, Cadence, product source, credentials, providers, browser, messaging, or Git mutation. |
| Did P11.3 execute or install Hermes? | No. |
| Did P11.3 activate runtime, Kanban Swarm, or Cadence? | No. |
| Did P11.3 execute tools or shell commands? | No, beyond the explicitly allowed initial posture and prerequisite path checks. |
| Did P11.3 configure provider/auth/API/MCP? | No. |
| Did P11.3 inspect product/Siamese source or use credentials? | No. |
| Did P11.3 mutate Git? | No. |
| What is next? | P11.4 Hermes Adoption Mode Decision, not started here. |

```text
hermes_runtime_cadence_boundary_ready_for_P11_4
```
