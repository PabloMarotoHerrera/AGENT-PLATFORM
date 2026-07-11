# P11.5 - Hermes Interface Adapter Design

## 1. Document Header

| Field | Value |
| --- | --- |
| Project | PROYECTO 11 - Hermes Real Integration |
| Ticket | P11.5 - Hermes Interface Adapter Design |
| Type | Architecture / interface design |
| Date | 2026-07-12 |
| Status | Design ready; implementation and runtime inactive |
| Authority | P11.0 source lock, P11.1 audit, P11.2 mapping, P11.3 authority decision, P11.4 staged adoption decision |
| Target | `0_architecture/governance/agent_platform_hermes_interface_adapter_design.md` |
| Scope | Stable contracts only; no code, install, execution, source modification, provider/API/MCP activation, credential access, or Git mutation |

Result markers:

```text
hermes_interface_adapter_design_ready
agent_runtime_port_defined
knowledge_memory_port_defined
work_control_plane_port_defined
adapter_contracts_defined
paperclip_boundary_preserved
gbrain_boundary_preserved
graphify_boundary_preserved
no_adapter_implementation
no_hermes_execution
no_provider_activation
no_git_mutation
```

## 2. Purpose

P11.5 defines the stable, provider-neutral and model-neutral interface boundary between AGENT PLATFORM and a replaceable Hermes runtime. It converts accepted P11.1-P11.4 evidence into explicit ports, shared objects, lifecycle semantics, authority checks, rollback hooks, and future validation targets.

This record is design only. It neither implements an adapter nor authorizes a runtime, dashboard, shell, tool, workspace, provider, API, MCP, Paperclip, GBrain, or Graphify action.

## 3. Current Posture

```yaml
HermesInterfaceAdapterPosture:
  adapter_implemented: false
  hermes_installed: false
  hermes_executed: false
  source_modified: false
  fork_created: false
  provider_activated: false
  api_called: false
  mcp_activated: false
  credentials_inspected: false
  product_source_inspected: false
  git_mutated: false
  p11_6_started: false
  p11_7_started: false
```

Hermes is a replaceable runtime candidate. All ownership statements about Hermes mechanics are conditional on later exact gates and conformance to this interface.

## 4. Post-Cleanup Prerequisite Resolution

Current substantive canonical content is authoritative after the accepted Markdown rationalization. Historical filename identity and obsolete result-marker names are not authority.

| Prerequisite | Current canonical resolution | Substantive result | P11.5 decision |
| --- | --- | --- | --- |
| P11.0 | `agent_platform_hermes_source_review_authorization.md` | Exact repository, release, tag, SHA, local path, and source-review-only boundary present | Accepted |
| P11.1 | `agent_platform_hermes_license_dependency_runtime_audit.md` | License, dependency, install, runtime, state, network, provider, minimum/full profile evidence present | Accepted with blockers retained |
| P11.2 | `agent_platform_hermes_architecture_mapping.md` | Agent loop, tools, skills, shell, workspace, provider, memory, subagent, event, dashboard, and Kanban seams present | Accepted |
| P11.3 | `agent_platform_hermes_runtime_cadence_boundary_decision.md` | Runtime ownership, provisional Kanban, Paperclip, GBrain, workspace, shutdown, rollback, and incident boundaries present | Accepted |
| P11.4 | `agent_platform_hermes_adoption_mode_decision.md` | Phase A wrapper, stable adapter, and Phase B controlled-fork productization strategy present | Accepted |
| P10.R | Concurrent/pending | Graphify evidence-only posture is already sufficient | Non-blocking |

No historical document was restored or recreated. No marker-alignment, retry, readiness, rerun, or safe-block document was needed.

## 5. Inputs Reviewed

| Input | Content consumed |
| --- | --- |
| P11.0 | Hermes 0.18.2, tag `v2026.7.7.2`, commit `9de9c25f620ff7f1ce0fd5457d596052d5159596`, path `4_external/sources/hermes-agent`; no install/execution/credentials/Git mutation |
| P11.1 | Mixed-license findings, dependency classes, broad runtime/tool/state/network surface, minimum profile, unverified shutdown and kill switch |
| P11.2 | Stable wrapping/adaptation seams and required contract vocabulary; no component was directly adopted as authority |
| P11.3 | Hermes runtime mechanics; AGENT PLATFORM policy; Paperclip work authority; GBrain durable knowledge; Graphify evidence-only; provisional Kanban |
| P11.4 | `wrap_existing_source` for Phase A, stable adapter for both phases, `controlled_fork_with_stable_adapter` for future productization |
| Current governance corpus | Existing WorkPacket, evidence, approval, rollback, incident, workspace, and no-Git-authority semantics |

Hermes source, product/Siamese source, GBrain source, Paperclip source, GStack source, ECC source, generated outputs, and raw Graphify outputs were not inspected.

## 6. Dependency Posture

P11.5 depends serially on accepted P11.1-P11.4. It does not resolve their blockers.

| Blocker | Adapter-design consequence |
| --- | --- |
| `HERMES-LIC-001` | Exclude or separately clear `skills/productivity/powerpoint`; no whole-tree reuse or redistribution assumption |
| `HERMES-LIC-002` | Preserve Apache-2.0 license and NOTICE obligations for `plugins/security-guidance` |
| `HERMES-DEP-001` | Runtime profile must reference an approved dependency/SBOM set before execution |
| `HERMES-DEP-002` | `security.allow_lazy_installs=false`; runtime dependency mutation is blocked |
| `HERMES-DEP-003` | Native/bootstrap reproducibility remains unproven |
| `HERMES-RUN-001` | Tool surface is deny-by-default and contract-filtered |
| `HERMES-STATE-001` | Every state root and residual must be inventoried |
| `HERMES-NET-001` | Network and listeners are deny-by-default; exact loopback exception requires a later gate |
| `HERMES-OPS-001` | Deterministic shutdown, cleanup, kill switch, and rollback require runtime evidence |

The inherited tree must not be described as uniformly MIT. P11.5 authorizes no redistribution or publication.

## 7. Adoption Mode Consumed

P11.5 consumes two independent P11.4 dimensions:

```yaml
HermesAdoptionStrategyConsumed:
  phase_a_source_relationship: exact P11.0-pinned upstream checkout, immutable and read-only
  phase_a_mode: wrap_existing_source
  runtime_integration_shape: stable AGENT PLATFORM adapter over an isolated local Hermes process/service
  phase_b_source_relationship: controlled_fork_with_stable_adapter
  phase_b_status: planned, not created or authorized by P11.5
  upstream_reference: 4_external/sources/hermes-agent
  consumer_rule: no AGENT PLATFORM consumer couples to upstream or fork internals
```

Conceptual source/workspace topology:

```text
immutable upstream reference
  4_external/sources/hermes-agent @ 9de9c25...
       |
       | Phase A: read-only runtime source after exact gate
       v
stable AGENT PLATFORM adapter ports
       ^
       | Phase B: same contracts after exact fork-creation gate
future controlled integration source
  exact path intentionally unresolved until authorization
       |
       +-- frontend/backend product patches
       +-- provenance and upstream synchronization record
       +-- patch ownership and rollback metadata

runtime workspace and HERMES_HOME
  separate from both source trees; temporary by default
```

P11.5 topology rules:

- the upstream checkout remains immutable and read-only;
- the future controlled integration source must use a separately authorized exact path;
- no runtime state, workspace output, patch, cache, dependency, or generated asset may be written into the upstream reference;
- upstream synchronization/rebase is human-reviewed, provenance-preserving, conflict-reviewed, license-reviewed, and never automatic;
- compatibility is negotiated through an adapter compatibility record containing adapter contract version, source mode, upstream SHA, fork SHA when applicable, required capabilities, schema versions, migration requirements and rollback target.

| Zone | Purpose | Required rule |
| --- | --- | --- |
| Upstream reference zone | Provenance and Phase A source | Exact P11.0 path/SHA; immutable, read-only and never patched |
| Controlled integration source zone | Future Phase B frontend/backend productization | Exact path only after creation gate; preserve provenance, license disposition, patch ownership, synchronization and rollback metadata |
| Runtime workspace zone | Bounded execution inputs and outputs | Separate from both source zones; represented by `WorkspaceReference`; temporary and exact-scope by default |
| Runtime state zone | Hermes profile/session/process state | Dedicated temporary `HERMES_HOME` for P11.6; inventory, retention, shutdown and cleanup required |

Upstream synchronization policy:

- synchronization/rebase is a separately authorized source action, never an automatic runtime behavior;
- every synchronization records upstream repository, tag, commit, fork base, resulting fork commit, adapter contract version, license delta, conflict disposition, and human approval;
- upstream changes enter the controlled source only through reviewed commits; the immutable reference is never patched;
- security updates do not bypass compatibility, license, review, or rollback gates;
- adapter compatibility must be proven before changing the active source version.

Version compatibility contract:

```text
AdapterCompatibilityProfile:
  adapter_contract_version
  source_mode
  upstream_commit
  controlled_fork_commit_if_any
  required_capabilities
  blocked_capabilities
  state_schema_versions
  event_schema_version
  checkpoint_format_versions
  known_incompatibilities
  migration_requirements
  rollback_target
  evidence_refs
  approval_refs
```

Each product patch requires an owner, rationale, affected frontend/backend surface, upstream provenance, license classification, security impact, compatibility impact, validation obligation, upstream-contribution disposition, rollback commit, and retirement condition. Rollback must permit adapter-level return to a compatible pinned upstream or prior approved fork without changing AGENT PLATFORM consumer contracts.

## 8. Interface Design Principles

1. Hermes is a replaceable runtime candidate.
2. AGENT PLATFORM owns authority and policy.
3. Hermes does not own canonical project/task state.
4. Hermes does not own durable world knowledge.
5. Hermes does not own canonical agent taxonomy.
6. Paperclip will own canonical work/task control-plane state.
7. GBrain will own durable knowledge and hybrid retrieval.
8. Graphify remains generated evidence and visualization.
9. Contracts expose stable platform semantics, never Hermes internal schemas.
10. Every effect is deny-by-default, exact-scope, finite, observable, cancellable where technically possible, and rollback-aware.
11. Evidence supports decisions but never grants authority or approval.
12. A reference is not permission: profile, capability, workspace, memory, checkpoint, provider, and approval references must resolve through their authoritative owner.
13. Provider and model identity must not alter authority, permission, state ownership, or error semantics.
14. Phase A and Phase B source relationships must remain interchangeable behind compatibility negotiation.

## 9. Adapter Boundary Model

```text
AGENT PLATFORM authority, policy, profiles, approvals, security, integration state
  |
  +-- AgentRuntimePort ------> stable Hermes runtime adapter
  +-- KnowledgeMemoryPort ---> GBrain authority boundary / Hermes runtime memory boundary
  +-- WorkControlPlanePort --> Paperclip authority boundary / provisional Hermes projection
  |
  +-- supporting boundary contracts:
      RuntimeEventPort
      ApprovalBoundaryPort
      WorkspaceBoundaryPort
      ShutdownRollbackPort
  |
  +-- Phase A runtime source: immutable P11.0-pinned upstream checkout
  +-- Phase B runtime source: future authorized controlled fork
```

| Boundary | Owner | Adapter responsibility | Prohibited leakage |
| --- | --- | --- | --- |
| `AgentRuntimePort` | AGENT PLATFORM contract; Hermes mechanics | Normalize lifecycle, work, tool, subagent, event, status, checkpoint, resume, and result operations | Hermes classes, process IDs as authority, raw exceptions, provider-specific payloads |
| `KnowledgeMemoryPort` | AGENT PLATFORM/GBrain contract | Scoped cited retrieval and governed write-candidate routing | Raw GBrain DB, direct Hermes durable writes, uncited facts |
| `WorkControlPlanePort` | AGENT PLATFORM now; Paperclip future canonical owner | Approved assignment projection and normalized work outcomes | Hermes Kanban schema/IDs as permanent API, dual writable state |
| `RuntimeEventPort` | AGENT PLATFORM observability | Normalize bounded redacted lifecycle evidence | Raw logs, credentials, prompts, internal DB rows |
| `ApprovalBoundaryPort` | Human/AGENT PLATFORM; Paperclip future workflow state | Request and consume exact decisions | Hermes status or reference treated as approval |
| `WorkspaceBoundaryPort` | AGENT PLATFORM | Allocate, validate, inventory, clean, quarantine | Path fallback, implicit mounts, source-scope expansion |
| `ShutdownRollbackPort` | AGENT PLATFORM kill authority | Cancel descendants, stop processes/services/listeners, inventory state, invoke kill switch and rollback route | Best-effort-only stop, hidden descendants, runtime-defined kill authority |

## 10. AgentRuntimePort

`AgentRuntimePort` controls runtime mechanics only after future exact runtime gates. In P11.5 every method is a design contract and is inactive.

| Method | Purpose | Input contract | Output contract | Authority boundary | Idempotency/correlation | Timeout/cancellation/retry | Failure/audit | Blocked side effects and security/rollback |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `start_session` | Start one bounded isolated runtime session | `RuntimeProfile`, `AgentCapabilityProfile`, `ExecutionContext`, compatibility ref, approval refs | opaque session ref, effective profile/capability snapshot, process/listener/state inventory | AGENT PLATFORM authorizes profile and source version; Hermes owns only session mechanics | Required key creates at most one session; root correlation begins here | Finite startup deadline; cancellable; retry only after proof no session/process/listener exists | requested/allowed/blocked/started/failed events plus `FailureEnvelope` | No provider, network, tool, shell, workspace write, daemon, child or listener unless explicitly allowed; stop/kill and state inventory hooks mandatory |
| `stop_session` | Reject new work and deterministically stop a session and descendants | session ref, stop mode, grace deadline, reason | stopped status, process/port/state/residual inventory | Platform owns stop/kill authority regardless of Hermes task state | Repeated calls return terminal stop result; retain correlation chain | Finite grace then approved kill route; cancellation cannot cancel the kill switch; retry status/kill safely | stop-requested/draining/stopped/kill-invoked/residual events plus failure | No hidden daemon or listener; quarantine unknown residuals and raise incident |
| `submit_work` | Submit one approved `WorkPacket` to an active session | session ref, `WorkPacket`, `ExecutionContext` | attempt ref, accepted/rejected status, effective limits | Work existence and permission remain external; Hermes executes supplied scope only | Required key scoped to work packet and attempt; payload mismatch is conflict | Supplied finite deadline; cancellable; retry only under explicit attempt policy | submit/accept/reject/start events and `FailureEnvelope` | No task creation, scope expansion, auto-decomposition, provider/tool use, or source access outside contracts; cancel and rollback attempt |
| `cancel_work` | Cancel one work attempt and descendants | attempt ref, reason, cancellation deadline | cancellation disposition, stopped descendants, residual refs | Platform/Paperclip future plane owns canonical cancellation; Hermes enforces mechanics | Idempotent terminal cancellation; preserve original and cancel correlations | Mandatory finite response; escalate to session stop/kill; no autonomous retry | cancel-requested/acknowledged/completed/escalated events | Must not start adjacent work, retry, reclaim, or mutate canonical state; incident on incomplete cancellation |
| `invoke_tool` | Invoke one exact allowed tool operation | session/attempt refs, tool ID, validated arguments, `ToolPermissionSet`, `ExecutionContext`, approval refs | invocation ref, bounded output metadata, side-effect inventory | Platform permission is authoritative; Hermes registry is discovery only | Required key for any possible side effect; duplicate safety declared by tool class | Exact timeout; cancellable where supported; no retry after uncertain side effects | invocation requested/allowed/blocked/started/completed/failed events and failure | Deny shell, filesystem, network, provider, MCP, browser, computer use, sudo, destructive action, product source, credentials, and Git unless an exact future gate permits the specific action; invoke rollback hook |
| `spawn_subagent` | Start one bounded child runtime under projected platform taxonomy | parent refs, child `WorkPacket`, `AgentCapabilityProfile`, depth/concurrency limits | child session/attempt ref and effective capability snapshot | Platform owns role/taxonomy; Hermes owns only child mechanics | Required key scoped to parent and child packet; correlation remains in parent tree | Finite startup/runtime deadlines; recursive cancellation; retry disabled by default | child requested/started/progress/completed/cancelled/failed events | No recursive unbounded fan-out, inherited excess capability, self-assigned role, provider escalation, or hidden background child; parent cancellation cascades |
| `stream_events` | Read normalized event sequence without granting streaming authority | session/attempt refs, cursor, event allowlist, retention window | ordered `RuntimeEvent` page/stream and next cursor | Platform owns schema, access, redaction, retention; events are evidence | Cursor/request identity; correlation filters are immutable | Finite poll/stream window; consumer cancellation closes stream; reconnect from cursor | stream opened/closed/gap events; gap yields failure | No raw log/database stream, telemetry, external sink, secret payload, or event-as-approval; disable route and quarantine unsafe records |
| `get_status` | Read bounded runtime health and lifecycle status | session/attempt refs, requested fields | normalized status, liveness timestamp, effective version/capabilities | Status is runtime evidence, not task/approval authority | Read request ID and correlation; safe repeat | Short finite timeout; cancellable; bounded read retry allowed | status-read/timeout/failure audit metadata | No internal DB exposure, canonical task transitions, or side effects; stale status is explicit |
| `checkpoint` | Request an optional portable, scoped checkpoint | session/attempt refs, scope, retention, sensitivity policy, approval refs | `CheckpointReference` or rejection | Platform owns eligibility, format policy, retention and restore approval | Required key; same scope/version returns same ref or explicit supersession | Finite; cancellable before commit; no blind retry after uncertain persistence | checkpoint requested/created/rejected/failed/invalidation events | No durable knowledge/task authority, hidden state, credentials, or indefinite retention; delete/invalidate on failure or drift |
| `resume` | Resume approved work from a compatible checkpoint | `CheckpointReference`, `WorkPacket`, `ExecutionContext`, compatibility and approval refs | new attempt ref, restore report, invalidation status | Platform authorizes resume; Hermes validates mechanics only | Required key creates at most one resumed attempt | Finite restore deadline; cancellable; retry disabled unless restore is proven side-effect-free | resume requested/validated/started/rejected/failed events | No automatic replay, stale-policy restore, changed scope, provider/source drift, or checkpoint-as-approval; invalidate and route to safe baseline |
| `collect_result` | Collect the normalized terminal or partial result | attempt ref, output allowlist, review policy | `ExecutionResult` and linked `FailureEnvelope`/events | Result is evidence requiring external review; it cannot approve or mutate canonical state | Read identity plus terminal result version; same version is stable | Finite collection; cancellable; bounded read retry | result-collected/partial/unavailable events | No raw secret output, implicit artifact publication, Git action, memory promotion, or task completion; quarantine unsafe artifacts |

## 11. KnowledgeMemoryPort

`KnowledgeMemoryPort` defines the future semantic boundary; it does not implement or activate GBrain, Hermes memory providers, MCP, or any physical store.

| Method | Purpose and input | Output | Read/write authority and GBrain posture | Hermes boundary | Approval, citation, retention | Rollback/incident | Blocked side effects |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `retrieve_context` | Retrieve scoped durable context using query, scope, purpose, freshness, permission and limit | cited context records, provenance, freshness, omissions | GBrain is canonical read owner; port is transport-neutral | Hermes may consume results in ephemeral execution context only | Read authorization required; every durable claim carries source citations; request/result retention explicit | Revoke context, invalidate caches, report over-broad or uncited response | No bulk export, raw DB access, provider call, silent persistence, or authority transfer |
| `search_decisions` | Search accepted decisions by query, scope, status and time boundary | cited decision summaries and canonical refs | GBrain/governance corpus owns decision truth | Hermes cannot reinterpret result as permission | Exact scope and citations mandatory; cache short-lived | Invalidate stale result; incident on missing provenance or policy leakage | No decision write, approval inference, unrestricted corpus traversal, or source expansion |
| `write_candidate_memory` | Submit `MemoryWriteCandidate` derived from runtime evidence | candidate receipt, validation status, review route | AGENT PLATFORM policy accepts proposal; GBrain decides durable intake | Hermes proposes only; session/procedural memory remains separate | Candidate is not approval; evidence/citations required; retention pending review | Withdraw/reject candidate; quarantine sensitive content; memory incident route | No direct durable write, auto-promotion, fact assertion without evidence, or DB fusion |
| `write_approved_memory` | Transmit a separately approved candidate with verified approval ref | durable record ref or rejected disposition | GBrain owns final validation/write; adapter verifies external approval but never creates it | Hermes has no direct write authority and receives only safe receipt metadata | Exact unexpired approval, evidence, citations, retention and rollback policy required | Compensating correction/tombstone through GBrain policy; incident on approval mismatch | No self-approval, overwrite-by-default, uncited write, physical DB access, or provider memory mirror |
| `cite_sources` | Resolve evidence refs to safe citation metadata | canonical citation set, unresolved refs, access classification | Evidence owner/GBrain supplies citations; adapter preserves identity | Hermes may attach citations but not mint canonical provenance | Permission and retention follow source classification | Revoke inaccessible citations; incident on fabricated or leaked source | No source-content expansion, credential disclosure, publication, or authority inference |
| `request_maintenance` | Propose deduplication, expiration, conflict review or reindex work | maintenance request receipt and external decision state | GBrain governance owns maintenance; no maintenance runs through this method | Hermes may identify a concern only | Human/governance approval required before action; evidence and retention explicit | Cancel request; record incident for destructive or autonomous behavior | No Dream cycle, autonomous rewrite/delete, scheduler activation, compaction, or provider call |

Memory layer invariant:

```text
Hermes: conversation/session/procedural collaboration memory
GBrain: durable cited knowledge, decisions, documents, facts and hybrid retrieval
No physical database fusion. No uncited or autonomous durable write.
```

## 12. WorkControlPlanePort

`WorkControlPlanePort` defines future Paperclip-compatible work semantics. It does not implement Paperclip and prevents provisional Hermes Kanban from becoming permanent task authority.

| Method | Purpose and input | Output | Paperclip and task-state authority | Provisional Hermes boundary | Approval and audit | Timeout/heartbeat/failure | Rollback/incident and blocked effects |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `claim_task` | Request/accept one externally approved assignment using task/work packet, worker profile, lease request | canonical/projection refs, bounded lease, attempt ref, disposition | Paperclip future plane owns canonical claim; AGENT PLATFORM owns policy before Paperclip | Hermes may create temporary projection only | Claim event with actor, policy and approval refs | Finite claim timeout; no implicit retry; `FailureEnvelope` on conflict | Release/freeze projection; no self-assignment, priority choice, task creation, or permanent Hermes-only ID |
| `heartbeat` | Report worker liveness for claim/attempt with sequence and observed health | accepted/stale status and next expected interval | Paperclip future plane defines canonical liveness interpretation | Hermes emits runtime metadata only | Normalized heartbeat event; never approval/completion | Finite TTL supplied externally; gaps raise evidence, not automatic canonical transition | Stop heartbeat loop on cancel; no task completion, reassignment, reclaim, or authority from heartbeat |
| `report_progress` | Report bounded progress, evidence refs and limitations | receipt and projected status | Canonical progress/workflow state belongs to Paperclip | Hermes projection may display status only | Actor, timestamp, evidence, sensitivity and retention required | Finite call; retry only with idempotency key; failure normalized | Freeze projection on mismatch; no scope expansion, approval inference, or organizational truth |
| `block_task` | Request/report a block with reason, dependency/evidence and required decision | canonical decision pending or projection receipt | Paperclip/AGENT PLATFORM owns canonical block transition | Hermes local block is evidence only | Human/approval route explicit; audit event required | Finite; duplicate block idempotent; failure envelope | Roll back projection; no self-approval, permanent deadlock, or hidden dependency creation |
| `complete_task` | Submit completion proposal with `ExecutionResult`, artifact/evidence refs and review needs | accepted-for-review/rejected/canonical completion disposition | Paperclip/human workflow owns canonical completion | Hermes may mark local attempt terminal but not canonical task complete | Review/approval requirements verified externally; full event chain | Finite; no retry after ambiguous canonical transition without idempotency reconciliation | Revert/freeze projection and incident on dual write; no auto-approval, publication, merge, or Git action |
| `fail_task` | Report terminal/nonterminal attempt failure with `FailureEnvelope` | recorded failure, external retry/review decision | Paperclip future plane owns task-level failure/requeue policy | Hermes records attempt evidence only | Failure and incident events; human route by severity | Finite; retry of report is idempotent, not retry of work | Freeze attempt; no autonomous requeue, retry budget creation, blame assignment, or secret dump |
| `request_approval` | Request exact human/governance decision for a bounded action | external request ref and pending/approved/denied/expired status | AGENT PLATFORM/human owns semantics; Paperclip may store future workflow state | Hermes may pause and display evidence only | Request is not approval; expiry, scope and decision provenance mandatory | Finite wait/poll policy; cancellation closes request; no repeated pressure loop | Denial/expiry stops action; no self-approval, inferred approval, or broader permission |
| `read_dependencies` | Read canonical dependency projection for one work item | normalized dependency refs, states, blocking semantics, version | Paperclip owns dependency graph | Hermes may consume a temporary projection | Read audit and provenance refs | Finite read; bounded retry; stale version explicit | Invalidate projection on mismatch; no edge creation, traversal expansion, or scheduling authority |
| `publish_artifact` | Register artifact metadata/evidence for external review; not public publication | artifact ref, retention/classification, review disposition | Paperclip future plane owns work-artifact record; governance owns publication | Hermes supplies generated artifact metadata only | Approval, provenance, sensitivity, retention and review required | Finite; idempotent by content/evidence identity; failure normalized | Quarantine/retract metadata; no public upload, Git commit, source tracking, credential content, or acceptance inference |

## 13. Shared Contract Object Model

All contract objects are versioned, serializable without implementation-specific classes, reject unknown authority-bearing fields, and carry only references to sensitive or external state.

### WorkPacket

| Field | Semantics |
| --- | --- |
| `work_packet_id` | Stable platform/Paperclip-compatible identity; never a permanent Hermes-only ID |
| `objective` | Bounded desired outcome, not permission by itself |
| `allowed_scope` | Explicitly permitted paths, actions, data and runtime surfaces |
| `blocked_scope` | Explicit prohibitions that override inferred capability |
| `required_context_refs` | Approved context references with access classification |
| `harness_or_runtime_target` | Abstract runtime target; does not authorize activation |
| `tool_permission_set_ref` | Exact `ToolPermissionSet` identity and version |
| `expected_outputs` | Required artifacts/results and safe formats |
| `review_requirements` | Human/reviewer checks before acceptance |
| `approval_requirements` | Exact actions requiring external approval |
| `rollback_requirements` | Required reversal, cleanup and restore outcomes |
| `incident_requirements` | Triggers, containment and escalation route |
| `correlation_id` | Root trace identity across ports and descendants |
| `limitations` | Known uncertainty, exclusions and non-authority statements |

`WorkPacket` is approved work projection, not automatic dispatch, Git approval, provider approval, source-inspection expansion, or task-state authority.

## 14. RuntimeProfile Design

| Field | Semantics |
| --- | --- |
| `runtime_profile_id` | Immutable profile identity and version |
| `runtime_mode` | Phase/source/process mode, such as isolated upstream spike; no free-form activation |
| `allowed_capabilities` | Positive capability allowlist |
| `blocked_capabilities` | Denylist with precedence over allowlist |
| `provider_policy` | Provider-neutral disabled/default or future approved route refs; no credentials |
| `network_policy` | Deny-by-default egress/listener policy and exact future exceptions |
| `shell_policy` | Disabled by default; exact future command gate semantics |
| `workspace_policy` | Exact root, source class, isolation, write and cleanup constraints |
| `memory_policy` | Session retention and GBrain read/write-candidate boundaries |
| `tool_policy` | Tool set, risk classes, approvals and side-effect rules |
| `subagent_policy` | Disabled/default or bounded depth, count, capabilities and cancellation |
| `cadence_policy` | No cron/always-on; bounded future heartbeat/retry/reclaim only |
| `logging_policy` | Normalized, redacted, bounded local evidence and retention |
| `shutdown_policy` | Grace, kill, process/port closure and residual acceptance criteria |
| `rollback_policy` | Adapter disable, source compatibility fallback, state restore/quarantine and incident route |

The effective profile is snapshotted at session start. Runtime defaults cannot broaden it.

## 15. AgentCapabilityProfile Design

| Field | Semantics |
| --- | --- |
| `capability_profile_id` | Stable versioned platform profile identity |
| `agent_type` | Reference to AGENT PLATFORM taxonomy; never Hermes-owned taxonomy |
| `allowed_tools` | Exact tool IDs and operation/risk scopes |
| `blocked_tools` | Explicit denial with precedence |
| `allowed_runtime_surfaces` | Session/tool/subagent/workspace surfaces permitted by future gate |
| `blocked_runtime_surfaces` | Providers, channels, cron, browser, computer use and other denied surfaces |
| `provider_requirements` | Abstract route requirements only; no provider secrets or activation |
| `workspace_requirements` | Isolation, source class, mounts, write and cleanup requirements |
| `memory_requirements` | Session context, cited durable reads and candidate-write rules |
| `approval_requirements` | Exact external approvals required by capability/risk class |
| `escalation_routes` | Human, security, governance and incident destinations |
| `limitations` | Depth, concurrency, data, model, tool, time and authority limits |

Child profiles must be equal to or narrower than the parent and current policy intersection.

## 16. ExecutionContext Design

| Field | Semantics |
| --- | --- |
| `execution_context_id` | Immutable invocation/attempt context identity |
| `work_packet_ref` | Exact approved work projection |
| `runtime_profile_ref` | Effective runtime policy identity/version |
| `workspace_ref` | Exact `WorkspaceReference`; never arbitrary CWD |
| `context_refs` | Authorized contextual inputs |
| `evidence_refs` | Evidence supporting work and decisions |
| `source_refs` | Exact source classes/paths allowed; product and unapproved external source excluded |
| `memory_refs` | Scoped memory reads/candidates; no raw database refs |
| `approval_refs` | External decision references; references alone are not approval until verified |
| `security_refs` | Security policy/gate identities |
| `timeout_policy` | Finite startup, operation, idle and total deadlines |
| `cancellation_policy` | Authority, cascade, grace and kill semantics |
| `retry_policy` | Error classes, attempt cap, backoff and no-retry side effects |
| `correlation_id` | Root trace identity |
| `idempotency_key` | Mutation deduplication key bound to request digest |

The context is immutable for an attempt. Any scope or policy change requires a new context and authorization.

## 17. ToolPermissionSet Design

| Field | Semantics |
| --- | --- |
| `permission_set_id` | Stable versioned policy identity |
| `allowed_tools` | Exact allowlist; empty by default |
| `blocked_tools` | Explicit denylist with precedence |
| `shell_allowed` | `false` by default; does not replace exact command approval |
| `filesystem_allowed` | `false` by default or exact workspace operations only |
| `network_allowed` | `false` by default or exact endpoint/listener policy only |
| `provider_allowed` | `false` by default; route approval remains separate |
| `MCP_allowed` | `false` by default; transport activation remains separate |
| `browser_allowed` | `false` by default |
| `computer_use_allowed` | `false` by default |
| `destructive_commands_blocked` | Always `true` unless a future exceptional exact gate supersedes |
| `sudo_blocked` | Always `true` by default |
| `product_source_blocked` | `true` unless a future exact product-source gate exists |
| `credential_access_blocked` | `true`; credentials never enter this contract |

The effective tool set is the intersection of platform policy, work packet, capability profile, runtime profile, execution context, and current approval. Hermes registration cannot expand it.

## 18. RuntimeEvent Design

| Field | Semantics |
| --- | --- |
| `event_id` | Globally unique event identity |
| `event_type` | Controlled lifecycle/tool/work/memory/shutdown/incident vocabulary |
| `timestamp` | UTC event time plus ordering caveat if clock confidence is limited |
| `correlation_id` | Root trace identity |
| `source_port` | Stable boundary that emitted the event |
| `work_packet_ref` | Optional approved work identity |
| `session_ref` | Opaque adapter session identity |
| `workspace_ref` | Safe workspace metadata reference |
| `severity` | Controlled diagnostic/notice/warning/error/critical classification |
| `payload_metadata` | Redacted bounded metadata; no raw secret or unrestricted transcript |
| `evidence_refs` | Supporting immutable evidence references |
| `incident_refs` | Linked incident/containment references |
| `retention_policy` | Owner, duration, access, deletion and publication posture |

Runtime events are generated evidence. They are not permission, approval, canonical task state, durable knowledge, or organizational audit truth.

## 19. ExecutionResult Design

| Field | Semantics |
| --- | --- |
| `result_id` | Stable result identity and version |
| `work_packet_ref` | Work projection that constrained execution |
| `runtime_session_ref` | Opaque session reference |
| `status` | Controlled terminal/partial/cancelled/failed disposition |
| `produced_artifacts` | Safe artifact refs with provenance, classification and retention |
| `changed_paths_metadata` | Inventoried path metadata, never implied Git approval |
| `stdout_summary` | Bounded redacted summary, not unrestricted output |
| `stderr_summary` | Bounded redacted diagnostic summary |
| `event_refs` | Complete relevant normalized event chain |
| `failure_ref` | Linked `FailureEnvelope` when applicable |
| `review_required` | External review requirement |
| `approval_required` | Remaining external approval before any downstream action |
| `limitations` | Missing evidence, uncertainty, partial behavior and exclusions |

A successful result does not complete a canonical task, approve an artifact, write memory, publish content, or mutate Git.

## 20. FailureEnvelope Design

| Field | Semantics |
| --- | --- |
| `failure_id` | Stable failure identity |
| `failure_type` | Controlled timeout/cancel/policy/runtime/tool/state/network/security/compatibility class |
| `severity` | Controlled severity tied to incident policy |
| `failed_method` | Stable port method name |
| `failed_contract` | Contract identity/version and validation stage |
| `correlation_id` | Root trace identity |
| `safe_summary` | Redacted explanation without secrets or unsafe repetition |
| `blocked_repetition` | Whether automatic/manual repetition is prohibited pending review |
| `incident_required` | Whether incident routing is mandatory |
| `rollback_required` | Required rollback/cleanup class |
| `retry_allowed` | Policy-derived boolean/class, never inferred from exception alone |
| `human_review_required` | Required reviewer/authority route |
| `limitations` | Unknown cause, missing evidence and disclosure constraints |

Raw exceptions, logs, provider payloads, credentials, and prohibited content do not cross the boundary.

## 21. CheckpointReference Design

| Field | Semantics |
| --- | --- |
| `checkpoint_id` | Opaque stable identity |
| `runtime_session_ref` | Source session identity |
| `workspace_ref` | Exact workspace identity/version |
| `created_at` | UTC creation time |
| `checkpoint_scope` | Explicit included/excluded state classes |
| `resumable` | Current compatibility/approval status, not a guarantee |
| `rollback_ref` | Required rollback/invalidation route |
| `retention_policy` | Owner, duration, sensitivity, deletion and access |
| `limitations` | Version, source, provider, policy, schema and portability constraints |

Checkpoints invalidate on source, adapter contract, state schema, provider, capability, policy, workspace, or approval drift.

## 22. WorkspaceReference Design

| Field | Semantics |
| --- | --- |
| `workspace_id` | Stable workspace identity |
| `workspace_type` | Temporary isolated, quarantine, or separately gated persistent class |
| `path_metadata` | Safe normalized root metadata, not unrestricted path traversal input |
| `persistent_or_temporary` | Temporary by default |
| `isolation_policy` | Root, mount, process, environment, sensitivity and escape controls |
| `cleanup_policy` | Stop, close, inventory, delete/quarantine and acceptance rules |
| `git_policy` | No Git mutation by default; exact future gate required per action |
| `source_scope` | Exact source classes/refs allowed in workspace |
| `product_source_blocked` | `true` by default |
| `external_source_blocked` | `true` outside exact P11-authorized refs |
| `limitations` | Backend, platform, filesystem, retention and validation unknowns |

Runtime fallback behavior must never broaden `path_metadata` or `source_scope`. Workspace cleanup is part of successful execution.

## 23. MemoryWriteCandidate Design

| Field | Semantics |
| --- | --- |
| `memory_candidate_id` | Stable proposal identity |
| `source_event_ref` | Runtime event/evidence origin |
| `content_summary` | Bounded non-authoritative proposed memory summary |
| `target_memory_layer` | Explicit session/procedural/GBrain candidate target |
| `write_authority` | External authority required; Hermes never grants it |
| `approval_required` | Exact review/approval policy and current state |
| `evidence_refs` | Evidence supporting the proposal |
| `citation_refs` | Canonical provenance required for durable claims |
| `retention_policy` | Pending-candidate and accepted/rejected retention |
| `rollback_policy` | Withdrawal, correction, tombstone and incident route |
| `limitations` | Uncertainty, scope, sensitivity, conflicts and non-factual status |

A candidate is not durable memory, fact, decision, permission, or self-improvement authorization.

## 24. Idempotency / Correlation / Timeout / Cancellation Semantics

| Concern | Required semantics |
| --- | --- |
| Idempotency | Every mutating call carries a caller-generated key and canonical request digest. Reuse with the same digest returns the prior disposition; reuse with different content returns an idempotency conflict. Keys are scoped by contract version, method, authority domain and target identity. |
| Correlation | One root `correlation_id` persists across ports; each child call has a `causation_id`. Retries retain correlation and add attempt identity. No runtime may replace the root trace. |
| Timeouts | Startup, operation, idle, approval wait and total deadlines are finite, monotonic where possible, and supplied by policy. Timeout never implies success or permission to continue. |
| Cancellation | Cancellation is idempotent, hierarchical, externally authoritative, deadline-bound, and observable. It stops new work, cascades to tools/subagents, then escalates to the approved kill route. |
| Ambiguous outcome | A timeout or transport loss after possible side effects yields `outcome_unknown`, blocks blind retry, inventories state, and routes reconciliation/incident handling. |
| Terminal state | Completed, failed, cancelled, killed and rolled-back states are monotonic except through an explicit new attempt/resume contract. |

## 25. Retry / Reclaim / Heartbeat Semantics

- Retry is permitted only for policy-classified transient failures within one approved attempt.
- Retry count, backoff, jitter, total deadline, retryable classes and approval escalation are external inputs.
- Tool, shell, filesystem, network, provider, memory-write, publication and canonical-state operations are not retried after uncertain side effects.
- Task-level requeue/retry belongs to future Paperclip; Hermes may not create a new canonical attempt autonomously.
- Reclaim detects an abandoned runtime attempt and reports evidence. Canonical claim reassignment requires AGENT PLATFORM/Paperclip decision.
- Heartbeat reports liveness only. It cannot approve, complete, fail, prioritize, assign, reclaim, or extend a task by itself.
- Missing heartbeat triggers a normalized stale-liveness event and controlled review/cancellation policy, not autonomous reassignment.
- Retry, reclaim and heartbeat loops are inactive until separately gated and must have finite cadence, concurrency and stop conditions.

## 26. Provider / Model Independence

- Ports and shared contracts use abstract policy/route/capability references, not provider SDK types, endpoint shapes, credentials, API keys, OAuth tokens, model-specific message classes, or MCP objects.
- AGENT PLATFORM owns provider eligibility, model eligibility, data scope, cost, retention, credential boundary and revocation.
- Hermes provider/model routing is an optional future mechanism, not authority routing.
- No provider is required to construct, validate, serialize, store, replay, test, or audit these contracts.
- A model/provider change cannot alter authority, tool permissions, work scope, memory ownership, approval, workspace, retry, shutdown, or event semantics.
- Provider absence or denial yields a structured blocked disposition; it does not trigger fallback to another provider.

## 27. Workspace Isolation Boundary

Every future workspace must define exact root, owner, purpose, source class, sensitivity, lifetime, mounts, allowed writes, blocked paths, process boundary, environment boundary, cleanup, quarantine, rollback and incident route.

Mandatory defaults:

- temporary workspace and dedicated temporary `HERMES_HOME`;
- source trees mounted/read only where possible;
- no writes into `4_external/sources/hermes-agent`;
- no user home, broad repository root, product/Siamese source, unrelated external source, credentials, `.env`, provider config, tokens, browser state, or local credential stores;
- no path fallback to a broader existing ancestor;
- no branch, worktree, checkout, reset, staging, commit, push, clean, or other Git mutation;
- no package, dependency, browser binary, plugin, skill, cache, checkpoint or state mutation outside exact roots;
- complete write/process/port/state/residual inventory;
- deterministic cleanup or quarantine before success.

## 28. Paperclip Boundary

Paperclip will own canonical project, task, dependency, assignment, workflow status, approval-workflow state, budget, claim, task-level retry/requeue, work attempt, artifact and organizational audit state.

Migration-compatible identity requires a stable platform/Paperclip ID plus an optional temporary Hermes projection ID. Internal Hermes-only IDs and enums never appear as permanent consumer APIs.

Required mappings cover task state machine, dependencies, assignments, heartbeats, comments, events, attempts, retries, failures, approvals, artifacts, rollback, archive and deprecation. Unknown or unmapped values block migration.

```text
No permanent dual task authority is allowed.
```

Cutover design requires one canonical writer per field/transition, frozen provisional writes, export, count/relationship validation, canonical import, adapter-route switch, rollback checkpoint, archive/removal of provisional state, and no consumer schema change.

## 29. GBrain Boundary

GBrain owns durable cited facts, decisions, documents, entities, project/person/world knowledge, provenance, promotion policy and hybrid retrieval.

Hermes may retain bounded session transcript, collaboration context and future separately governed procedural memory. Durable reads cross `KnowledgeMemoryPort` with scope, permissions, freshness and citations. Durable writes begin as `MemoryWriteCandidate` and require independent approval and GBrain validation.

No physical database fusion, shared tables, raw database access, uncited write, autonomous promotion, provider-memory mirror, Dream loop, destructive maintenance, or Hermes durable-truth role is permitted.

## 30. Graphify Boundary

Graphify remains generated repository evidence and visualization only.

- Graphify output is not runtime context by default, policy, permission, approval, ontology authority, task state, durable world knowledge, security decision, or adapter configuration.
- A future curated Graphify evidence reference may cross contracts only through normal evidence classification, provenance, scope, retention and review.
- Hermes does not read raw Graphify outputs through this design.
- Runtime events do not automatically update Graphify or become repository evidence.
- P11.5 performs no Graphify authority expansion and creates no generated-output tracking obligation.

## 31. Kanban Swarm Provisional Boundary

P11.5 consumes `hermes_kanban_provisional_control_plane` as a temporary adapter-isolated execution projection, not canonical authority.

| Concern | Required adapter mapping |
| --- | --- |
| Task identity/state | Stable external ID plus temporary projection ID; explicit state map and invalid-state stop |
| Dependencies | Direction/type/blocking/cycle/deletion mapping to Paperclip model |
| Assignment | Execute supplied assignment only; no Hermes organizational assignment |
| Events/comments | Normalized evidence with actor, timestamp, provenance, sensitivity and retention |
| Heartbeat | Worker liveness only through normalized events |
| Retry | One bounded attempt under external policy; no task-level requeue authority |
| Reclaim | Detection/request only; canonical reassignment external |
| Human review | Hermes review/block status is evidence; approval remains external |
| Failure | `FailureEnvelope`, residual state, retryability and incident mapping |
| Migration | Export, validate, freeze, cut over to one writer, rollback, archive/remove provisional DB |

Auto-decomposition, autonomous task creation, unrestricted dispatcher, cron, always-on workers, recursive fan-out, external messaging, provider planning, permanent Kanban state, and direct UI/client coupling to Hermes schemas remain blocked. A bypass/no-Kanban runtime path is mandatory.

## 32. Security / Credential / Provider Boundary

The contracts contain no credential values and grant no credential access.

Default prohibitions:

```text
no credentials in adapter contracts
no API keys
no .env
no OAuth tokens
no provider config values
no browser auth, cookies, or profiles
no local credential store access
no sudo
no destructive shell commands
no public ports
no hosted providers
no computer use
no browser automation
no product/Siamese source
no external source traversal outside exact scope
no Git mutation
no lazy package installation
no MCP
```

Security checks intersect all supplied policies and may only narrow permission. A blocked security decision returns `FailureEnvelope`; it never falls back, retries through another mechanism, reveals the blocked value, or becomes activation authority.

## 33. Rollback / Incident Compatibility

| Surface | Disable/rollback requirement | Incident trigger |
| --- | --- | --- |
| Adapter route | Immediate platform-controlled disable/bypass; consumers retain stable contracts | Bypass unavailable or consumer coupled to Hermes internals |
| Runtime/session | Stop new work, cancel descendants, grace then kill, verify process/port closure | Failure to stop, hidden child, daemon or listener |
| Source mode/version | Compatibility check and route to approved upstream/prior fork without consumer change | Version/schema/capability drift or unowned patch |
| Workspace/state | Inventory, restore pre-run state, delete/quarantine residuals | Unknown write, path escape, sensitive state or failed cleanup |
| Tool/shell | Stop invocation, prevent adjacent actions, inventory effects, invoke action-specific rollback | Destructive command, sudo, package manager, Git or uncertain side effect |
| Work control | Freeze projection, stop writes, preserve canonical state, disable provisional route | Dual authority, unmapped state, autonomous transition |
| Memory | Disable read/write route, withdraw candidate, correct/tombstone through GBrain policy | Uncited/direct write, DB fusion, privacy or authority breach |
| Provider/network | Block/revoke exact route if ever enabled; close listeners | Unexpected provider/API/MCP call, egress, telemetry or public bind |
| Evidence/logs | Stop emission, preserve safe metadata, quarantine unsafe records | Secret/raw sensitive payload, unrestricted telemetry, authority claim |

Incident response is STOP, do not repeat unsafe content, preserve safe metadata only, invoke approved shutdown/kill if active, revoke implicated routes, quarantine without prohibited inspection, record rollback, and route to human/security/governance review.

## 34. Observability / Audit Event Model

Minimum normalized event families:

```text
adapter.requested / adapter.allowed / adapter.blocked
session.starting / session.started / session.stopping / session.stopped / session.killed
work.submitted / work.started / work.progress / work.cancelled / work.completed / work.failed
tool.requested / tool.allowed / tool.blocked / tool.started / tool.completed / tool.failed
subagent.requested / subagent.started / subagent.stopped / subagent.failed
workspace.allocated / workspace.write_observed / workspace.cleaned / workspace.quarantined
checkpoint.created / checkpoint.invalidated / resume.rejected
memory.read / memory.candidate_submitted / memory.write_rejected
workcontrol.claim / workcontrol.heartbeat / workcontrol.transition_requested
approval.requested / approval.approved / approval.denied / approval.expired
rollback.started / rollback.completed / rollback.failed
incident.triggered / incident.contained / residual.detected
```

Events carry safe metadata, correlation/causation, actor/port, authority classification, evidence refs, retention and incident refs. AGENT PLATFORM owns schema, redaction, aggregation, access and publication. Paperclip may later own canonical work audit. Raw Hermes logs and local events remain non-authoritative.

## 35. P11.6 Local Shell Spike Interface Expectations

The current P11.4 practical objective is `P11.6 - Hermes Local Runtime and Dashboard Spike`; any shell/tool action remains separately and exactly gated.

P11.6 should prove from the interface perspective:

- Phase A uses the exact unmodified P11.0-pinned upstream source through the stable adapter boundary;
- one isolated local Hermes environment and dedicated temporary `HERMES_HOME`;
- only the minimum backend required by the UI;
- dashboard bound only to `127.0.0.1` on one exact authorized local port;
- complete frontend/backend/child process and listener inventory;
- start/status/stop behavior for one bounded session;
- one inert or safe `WorkPacket` only if its exact runtime/tool scope is separately authorized;
- temporary workspace allocation with no product source, credentials or unauthorized external source;
- normalized event capture and `ExecutionResult`/`FailureEnvelope` production;
- no public listener, external channels, cron, autonomous dispatcher, browser/computer use, MCP, GBrain or Paperclip integration;
- no provider call unless separately required and exactly authorized;
- no unauthorized network, package mutation, persistent daemon, source modification, fork creation, UI customization or Git mutation;
- deterministic shutdown, kill-switch evidence, process/port closure, state-location inventory and residual-file inventory.

P11.6 must reconcile the P11.3 dashboard restriction through its own exact listener/security gate. P11.5 does not run or authorize the spike.

## 36. P11.7 Safety / Rollback Review Inputs

P11.7 must consume at least:

| Review input | P11.5 requirement |
| --- | --- |
| Dangerous methods | `invoke_tool`, `spawn_subagent`, `checkpoint`, `resume`, memory writes, work transitions, runtime start/stop/kill |
| Command boundary | Exact executable/action, arguments, cwd, environment, stdin, outputs, timeout, side effects, approval, rollback and incident route |
| Workspace isolation | Root/mount/source/path fallback/write/cleanup/quarantine verification |
| Provider/credential boundary | No credential values in contracts; no environment inheritance; route revocation and egress checks |
| Plugin/skill boundary | Disabled by default; provenance, immutable allowlist, override prevention, lifecycle and self-modification review |
| Browser/computer use | Blocked; separate exact gate if ever proposed |
| Persistent state | Full `HERMES_HOME`, DB, logs, caches, backups, processes, checkpoints and external provider state inventory |
| Kill switch/circuit breaker | Platform-controlled, independent of Hermes task state, finite and testable |
| Adapter disable route | Bypass/no-Hermes and no-Kanban paths with stable consumer contracts |
| Rollback hooks | Runtime, source version, workspace, work projection, memory route, provider route and event route |
| Incident triggers | Scope escape, credential exposure, provider/network/MCP, Git, destructive action, public listener, dual authority, failed shutdown/cleanup |

P11.7 must validate that internal Hermes checks supplement but never replace platform enforcement.

## 37. Stop Rules

STOP interface progression if:

- P11.0 identity or P11.4 staged adoption becomes absent, contradictory or unresolved;
- a surface cannot be mapped to one authority owner and stable boundary;
- Hermes must become authority for policy, taxonomy, projects, tasks, dependencies, approvals, budgets, durable knowledge or Git;
- consumers must couple to upstream/fork internals, Hermes schemas, logs, databases, paths or statuses;
- the immutable upstream reference would be written or a fork/source workspace would be created without an exact gate;
- required contract data includes credentials, `.env`, tokens, API keys, browser auth, provider values or raw credential-store data;
- implementation, installation, execution, dashboard/service startup, shell/tool execution, package management, provider/API/MCP, network, source modification, product source, tests/builds/scripts, Git mutation, publication or redistribution is required;
- timeout, cancellation, kill, residual inventory, rollback or incident semantics cannot be made deterministic;
- provisional Kanban cannot be bypassed/migrated or creates dual task authority;
- GBrain separation, citations, write approval or no-DB-fusion cannot be preserved;
- mixed-license constraints are treated as resolved or the inherited tree is labeled uniformly MIT.

## 38. Future Validation Targets

Proposed only, not executed:

- schema completeness and unknown-field rejection for every shared contract;
- method matrix completeness for all three primary ports;
- idempotency same-key/same-digest and conflict behavior;
- correlation/causation continuity through child calls and retries;
- finite timeout and hierarchical cancellation conformance;
- ambiguous-side-effect no-retry behavior;
- provider/model independence and credential-free serialization;
- effective tool-permission intersection and runtime-default narrowing;
- workspace path, source, write and cleanup enforcement;
- process/port/state/residual inventory completeness;
- deterministic shutdown and platform kill-switch conformance;
- upstream/fork adapter compatibility and source-version rollback;
- Paperclip ID/state/dependency/attempt/approval/failure migration completeness;
- no permanent dual task authority;
- GBrain citations, candidate-write approval and no-DB-fusion invariants;
- Graphify evidence-only and no-raw-output boundary;
- P11.6 interface evidence completeness;
- P11.7 dangerous-method and incident-trigger coverage.

## 39. Future Hardening Candidates

```text
HERMES-ADAPTER-HARD-01 - Contract Schema And Version Compatibility Specification
HERMES-ADAPTER-HARD-02 - Runtime Lifecycle Idempotency And Cancellation Conformance
HERMES-ADAPTER-HARD-03 - Tool Permission Intersection And Side-Effect Classification
HERMES-ADAPTER-HARD-04 - Workspace Isolation And Residual Inventory Conformance
HERMES-ADAPTER-HARD-05 - Upstream/Fork Topology And Synchronization Runbook
HERMES-ADAPTER-HARD-06 - Paperclip Migration And Single-Writer Cutover Contract
HERMES-ADAPTER-HARD-07 - GBrain Citation And Memory Promotion Contract
HERMES-ADAPTER-HARD-08 - Runtime Event Redaction And Retention Schema
HERMES-ADAPTER-HARD-09 - Kill Switch, Adapter Bypass And Source Rollback Drill
HERMES-ADAPTER-HARD-10 - Dashboard Loopback Process And Listener Safety Profile
```

These are candidates, not additional tickets started or Markdown created by P11.5.

## 40. Created / Modified / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_hermes_interface_adapter_design.md
```

Modified:

```text
no pre-existing file
```

Not created, implemented, inspected, executed, activated, or authorized:

```text
no adapter, runtime, provider, MCP, API, CLI, shell, service, dashboard or source code
no Hermes installation, execution, shell, dashboard, proxy, gateway, channel, worker,
   subagent, Kanban Swarm, cron, scheduler, dispatcher, retry, reclaim or heartbeat loop
no provider/model call, API/OAuth/MCP activation, credential or secret inspection
no product/Siamese, GBrain, GStack, Paperclip, ECC or unrelated external source inspection
no Hermes source inspection or modification; no controlled fork or source workspace
no dependency installation, package manager, test, build, lint, typecheck, script or CI
no state database, workspace, checkpoint, persistence, telemetry or public listener
no raw Graphify/generated-output inspection or Graphify authority expansion
no publication, redistribution, source-tracking expansion, staging, commit, push or Git mutation
no modification of .opencode/, AGENTS.md, .gitignore or .graphifyignore
no P11.6, P11.7, P11.8, P11.R, P12, P13, P14 or EXT.* document
no retry, diagnostic, readiness, marker-drift, naming-drift, rerun or safe-block Markdown
```

## 41. Recommended Next Ticket

If P11.6 is not complete:

```text
P11.6 - Hermes Local Runtime and Dashboard Spike
```

If a separately authorized P11.6 is already complete:

```text
P11.7 - Hermes Adapter Safety / Rollback Review
```

P11.5 starts neither ticket.

## 42. Final Verdict

| Question | Answer |
| --- | --- |
| What was created? | One canonical documentation-only Hermes Interface Adapter Design. |
| Were P11.0-P11.4 substantively present? | Yes; all exact current canonical paths and required content were present. |
| What adoption strategy was consumed? | Phase A `wrap_existing_source`, one stable adapter across phases, and future `controlled_fork_with_stable_adapter` productization after exact authorization. |
| What are the primary ports? | `AgentRuntimePort`, `KnowledgeMemoryPort`, and `WorkControlPlanePort`. |
| Is Hermes replaceable? | Yes; consumers bind only to stable contracts and the adapter supports disable, bypass, source-version rollback and replacement. |
| Who owns runtime mechanics? | Hermes conditionally, after future gates, behind `AgentRuntimePort`. |
| Who owns authority and policy? | AGENT PLATFORM. |
| Who owns canonical work state? | Future Paperclip. Hermes Kanban is provisional and bypassable only. |
| Who owns durable knowledge? | GBrain, with cited reads and governed candidate writes; no physical DB fusion. |
| What is Graphify's role? | Generated evidence and visualization only. |
| Are providers/models embedded in contracts? | No; contracts are provider/model independent and contain no credentials. |
| Was the adapter implemented? | No. |
| Was Hermes installed or executed? | No. |
| Was a provider, API, OAuth or MCP activated? | No. |
| Was source modified or a fork created? | No. |
| Was Git mutated? | No. |
| What is next? | P11.6 Local Runtime and Dashboard Spike if not complete; otherwise P11.7 Safety / Rollback Review. |

```text
hermes_interface_adapter_design_ready
agent_runtime_port_defined
knowledge_memory_port_defined
work_control_plane_port_defined
adapter_contracts_defined
paperclip_boundary_preserved
gbrain_boundary_preserved
graphify_boundary_preserved
no_adapter_implementation
no_hermes_execution
no_provider_activation
no_git_mutation
```

## Commit Commands

If the human accepts this decision, the human may run:

```powershell
git status --short

git add 0_architecture/governance/agent_platform_hermes_interface_adapter_design.md

git commit -m "P11.5 - Hermes Interface Adapter Design"

git push origin main
```

Never use `git add .`.
