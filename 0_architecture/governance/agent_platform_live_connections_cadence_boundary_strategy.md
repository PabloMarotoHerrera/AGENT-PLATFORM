# P2.K4 - Live Connections / Cadence Boundary Strategy

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Live Connections / Cadence Boundary Strategy |
| Ticket | P2.K4 |
| Status | Accepted architecture alignment strategy |
| Date | 2026-07-04 |
| Scope | Define metadata-only boundaries for future live connections, volatile connector data, on-demand retrieval, curated summaries, never-persist material, and future Cadence posture for AGENT PLATFORM / Siamese. |
| Authority | Architecture alignment only, not runtime activation, connector activation, provider/auth approval, API approval, MCP activation, polling, source loading, persistence, permanent memory, tool execution, agent execution, product activation, Graphify rerun/adoption, generated output tracking, source tracking approval, publication, or Cognitive Semantic System substrate selection. |
| Related documents | P2.R, P2.1, P2.2, P2.3, P1.1-P1.5, P0.1-P0.3, G-01, G-19, S-03, S-04, CSS ADR/audit, Graphify Repo Map Summary, `.gitignore`, `.graphifyignore`, README.md. |
| Output | Live connection and future Cadence boundary strategy. |

P2.K4 is architecture alignment only. AGENT PLATFORM remains pre-active at AL-1.

## 2. Purpose
Future AGENT PLATFORM work may need to reason about live connector surfaces such as Slack, email, GitHub issues, customer data, calendars, support queues, product telemetry, or other changing streams. Those surfaces have different memory, retention, evidence, security, validation, and governance properties than accepted evergreen architecture records.

P2.K4 defines the boundary strategy before any connector exists. It separates evergreen context, volatile live connector data, on-demand retrieval, curated summaries, never-persist material, and future Cadence so later tickets cannot confuse availability with activation or transient access with permanent memory.

P2.K4 does not activate cadence. P2.K4 does not create connectors. P2.K4 does not approve live data access. P2.K4 does not start P2.KR or P3.0.

## 3. Current Cross-Lane Posture
| Area | Current posture | P2.K4 result |
| --- | --- | --- |
| Activation level | AGENT PLATFORM remains pre-active at AL-1. | No promotion. |
| Live connectors | No live connector is approved or active. | Availability is recorded as future metadata only. |
| Cadence | No runtime, loop, process lifecycle, or review rhythm is active. | Future Cadence is defined as a candidate governance concept only. |
| Context | P1.1 context records are metadata and safe summaries only. | Context inclusion remains non-permission. |
| Providers/auth | P1.2 provider descriptors are metadata only. | Provider/API/MCP/auth gates remain required. |
| Tools | P1.3 tool records are metadata only. | No connector tool execution. |
| Agents | P1.4 agent records are metadata only. | No agent task, handoff, or connection monitoring. |
| Cognitive Semantic System | P1.5 semantic records are metadata and substrate neutral. | Cognitive Semantic System substrate remains deferred. |
| Evidence | P2.2 EvidenceRef contract supports claims but does not decide. | Live evidence refs remain metadata only. |
| Audit / retention / rollback | P2.3 defines metadata baselines only. | Connector retention inherits metadata-only posture. |
| Security | S-03 and S-04 block local-only, secrets, credentials, auth, provider calls, network calls, and execution by default. | Live connector inputs inherit blocked defaults. |

Live connector availability is not live connector activation. Live connectors are gate-controlled. Volatile data is not permanent memory by default.

## 4. Boundary Definitions
| Boundary class | Definition | Allowed P2.K4 use | Blocked inference | Required future gate or review |
| --- | --- | --- | --- | --- |
| Evergreen context | Stable governance, security, validation, architecture, and accepted metadata records intended for durable reference. | Cite accepted metadata with EvidenceRef, limitations, and blockers. | Evergreen status as runtime permission. | Relevant gate only if activation, publication, or source expansion is requested. |
| Volatile / live connector data | Changing data from a live or future-live system, including Slack, email, GitHub issues, customer data, support tools, calendars, provider outputs, or product telemetry. | Record safe metadata categories and blockers. | Treating fresh data as permanent memory, source truth, or activation approval. | GT-08, GT-05, GT-04, GT-12, GT-15, and product/source gates as applicable. |
| On-demand retrieval | A future exact-scope request to retrieve a bounded item when a governed task needs it. | Define metadata requirements and stop rules. | Background access, general sync, broad source loading, or retention. | Exact connector/provider/source/security approval before retrieval. |
| Curated summary | A reviewed, safe, scoped summary derived from volatile data without raw payloads, secrets, credentials, or restricted content. | Candidate evidence after review with limitations. | Raw connector content approval, permanent memory, or authority. | Security, validation, governance, retention, and tracking review. |
| Never-persist material | Data classes that must not become durable memory, evidence content, context, logs, summaries, or generated output by default. | Safe metadata marker only. | Retention, transformation, publication, provider transmission, or model memory. | Secure incident route or exact future secure handling gate. |
| Future Cadence | A candidate governed rhythm for later review, refresh, escalation, or expiry of connector-derived metadata. | Define non-runtime readiness language only. | Scheduler, worker, daemon, polling, monitoring, always-on behavior, or autonomous loop. | Future runtime, provider/auth, security, validation, rollback, and governance gates. |

GBrain / always-on / Hermes cadence is future Cadence. These terms may appear only as future, blocked, or candidate vocabulary and never as active AGENT PLATFORM runtime, active memory, active connector behavior, or current Cognitive Semantic System substrate.

## 5. Live Connector Availability Boundary
Connector availability means a connector type could exist in the broader ecosystem or be named as a future candidate. It does not mean AGENT PLATFORM may connect, authenticate, read, write, subscribe, transmit, store, summarize, monitor, or classify live data.

| Connector surface | P2.K4 classification | Allowed current handling | Blocked current handling |
| --- | --- | --- | --- |
| Slack | Volatile / live connector candidate. | Safe metadata category only. | Workspace connection, channel read, message sync, user lookup, bot install, token use, or permanent memory. |
| email | Volatile / live connector candidate. | Safe metadata category only. | Mailbox read, send, search, attachment access, credential use, thread sync, or permanent memory. |
| GitHub issues | Volatile / live connector candidate unless exact public metadata is separately scoped. | Safe metadata category only. | API calls, issue sync, comment ingestion, token use, webhook setup, or source tracking approval. |
| customer data | Restricted volatile data by default. | Safe metadata category only. | Raw customer record access, copying, summarization, retention, provider transmission, or product activation. |
| Support / CRM / ticketing | Restricted volatile data by default. | Safe metadata category only. | Connector activation, account lookup, ticket sync, customer content ingestion, or retention. |
| Calendar / scheduling | Volatile personal or organizational data by default. | Safe metadata category only. | Calendar read/write, invite creation, attendee extraction, or reminder loops. |
| Product telemetry | Product-restricted and generated-sensitive by default. | Product-readiness metadata only. | Product source/output inspection, telemetry ingestion, execution, tracking, or activation. |

Every future live connector request must first define owner, exact connector, exact account or workspace boundary, data sent, data received, auth posture, local-only posture, retention posture, security refs, validation refs, evidence refs, rollback refs, incident refs, blockers, limitations, and decision authority.

## 6. Context And Memory Classification Rules
| Class | Memory posture | Retention posture | Evidence posture | Example safe use |
| --- | --- | --- | --- |
| Evergreen context | Durable metadata allowed when already governed. | Metadata-only or accepted governance retention. | EvidenceRef can cite the exact governance record. | P0/P1/P2 architecture docs, gate records, policy docs. |
| Live connector snapshot | Volatile and non-durable by default. | No raw retention by default. | Candidate evidence only after exact review. | A future reviewed issue metadata record with no raw customer content. |
| On-demand retrieved item | Task-scoped and expiry-bound by default. | Must declare review cycle and deletion/quarantine triggers. | Evidence only after curation. | Future exact request for one issue title and status after gate approval. |
| Curated connector summary | Durable only if governance accepts it for exact scope. | Retain curated summary only, never raw payload, unless future gate says otherwise. | Supporting evidence with limitations. | Safe trend summary with source class and sensitivity preserved. |
| Never-persist data | No memory. | Omit or quarantine by metadata route. | Not evidence content. | Secret values, credential values, raw auth material, raw customer payloads, raw product source, raw local-only dumps. |
| Future Cadence state | No state by P2.K4. | Future gate required before any state or persistence. | Not applicable by P2.K4. | Candidate review rhythm description only. |

Memory must be explicit, scoped, and reversible. A live item does not become evergreen context by being current, available, useful, referenced, retrieved, summarized, or attached to a task. A curated summary does not erase original sensitivity, local-only posture, product posture, generated-output posture, connector provenance, blockers, or limitations.

## 7. On-Demand Retrieval Boundary
On-demand retrieval is a future exact-scope action. It is not a standing connection, general sync, monitoring permission, durable memory grant, or provider/auth approval.

| Required future field | Meaning |
| --- | --- |
| `retrieval_request_id` | Stable future metadata identifier. |
| `connector_ref` | Connector metadata ref, not active connector handle. |
| `retrieval_scope` | Exact item, field class, account/workspace boundary, and time boundary. |
| `request_owner` | Accountable owner; missing owner blocks retrieval. |
| `data_sent` | Exact metadata or query data that would be transmitted. |
| `data_received` | Exact expected response classes and sensitivity. |
| `auth_posture` | Credential absence, need, blocker, or exact future secure approval route. |
| `source_classification` | Governance, connector metadata, product-restricted, customer-restricted, external, local-only, generated, secret, credential, or unknown. |
| `retention_posture` | Metadata-only, curated-summary-only, local-only, quarantine, deletion review, or blocked. |
| `security_refs` | Security constraints and blockers. |
| `validation_refs` | Validation posture; no execution by default. |
| `evidence_refs` | Evidence metadata refs, not raw payloads. |
| `rollback_refs` | Future rollback/cleanup route if any data is exposed or retained. |
| `incident_refs` | Incident route for secrets, credentials, customer data, product data, unknown sensitivity, or unauthorized access. |
| `decision_status` | Draft, blocked, needs review, rejected for scope, or future exact approval. |

If any field is unknown, retrieval remains blocked or needs review. Approval for one retrieval would not approve another retrieval, continuous sync, live subscription, connector activation, permanent memory, provider transmission, publication, or source tracking.

## 8. Curated Summary Boundary
A curated summary is a governed derivative, not a dump of live connector content. It can only be considered after exact future review confirms that raw connector data, secrets, credentials, customer data, local-only data, product source, provider auth material, restricted external data, and generated-sensitive material are excluded or handled through approved secure routes.

| Summary rule | Requirement |
| --- | --- |
| Preserve provenance | Identify connector class, source classification, and retrieval gate without embedding raw payload. |
| Preserve sensitivity | Carry highest sensitivity and unknown-sensitivity blockers. |
| Preserve limitations | Record staleness, incompleteness, sampling, human curation, generated-output, and source-unread limitations. |
| Preserve blockers | Keep provider/auth, source loading, product, local-only, customer data, publication, tracking, validation, and security blockers. |
| Retain minimally | Prefer curated metadata only; never retain forbidden raw content. |
| Review before reuse | Validation evaluates; governance decides. |

A curated summary may support a future claim, but it cannot become authority by citation. Evidence supports; it does not decide. Security constrains; it does not activate.

## 9. Never-Persist Rules
Never-persist means the content must not become durable memory, evidence content, context content, connector cache, generated summary, semantic claim body, audit payload, tool output, agent output, publication artifact, or Git-tracked material by default.

| Never-persist class | P2.K4 handling |
| --- | --- |
| Secret values | Stop; safe metadata only; secure incident route. |
| Credential values and auth material | Stop; safe metadata only; no testing, use, refresh, or partial reveal. |
| Provider auth sessions, tokens, cookies, local auth state | Stop; safe metadata only; GT-08 and secure approval required for any future handling. |
| Raw customer data | Treat as restricted volatile data; no raw retention, copying, publication, or permanent memory by default. |
| Raw product source or product outputs | Product source remains blocked until GT-09; no product activation by summary. |
| Raw local-only material | Excluded unless exact future local-only/security scope approves safe metadata handling. |
| Raw external source content | External evidence only; no adoption, execution, or copying by P2.K4. |
| Raw generated outputs or raw Graphify output | Local-only/generated-sensitive; no authority, publication, tracking, or inclusion by default. |
| Unknown sensitivity data | Block or needs review; do not treat as safe. |

Never-persist material may be represented only by safe metadata such as category, blocked status, source class, required review, and content-not-inspected posture.

## 10. Future Cadence Boundary
Cadence is a future governed concept for how connector-derived metadata might be reviewed, refreshed, expired, escalated, or revalidated. It is not active behavior.

| Future Cadence concern | P2.K4 boundary |
| --- | --- |
| Review rhythm | Candidate governance design only; no active loop. |
| Refresh / expiry | Future metadata fields only; no retrieval or automatic update. |
| Escalation | Future incident/rollback route only; no automation. |
| Memory promotion | Governance decision required; no automatic promotion from volatile to evergreen. |
| Always-on language | Future/candidate vocabulary only; no active monitoring or runtime. |
| GBrain / Hermes cadence language | Future/candidate vocabulary only; no adoption, connector, or runtime. |
| Runtime/state | GT-06, GT-13, GT-15, GT-05, GT-04, and governance would be required before any future active design. |

P2.K4 does not create Cadence records that run, poll, schedule, subscribe, monitor, store state, trigger agents, call tools, call providers, or update memory. P2.K4 only defines the language that later tickets must preserve if future Cadence is proposed.

## 11. Evidence, Validation, Security, And Governance Interfaces
| Interface | Rule |
| --- | --- |
| Evidence | Connector references use EvidenceRef metadata only. Evidence supports; it does not decide. |
| Validation | Validation evaluates; governance decides. Validation may later evaluate completeness, staleness, safety, blocker propagation, and summary quality but cannot activate connectors. |
| Security | Security constrains connector access, auth, customer data, local-only material, product data, generated outputs, retention, publication, and incident handling. |
| Governance | Governance decides whether any exact connector, retrieval, curated summary, retention, memory promotion, or Cadence move is accepted. |
| Context | Context inclusion is not permission. Connector-derived context must preserve source class, sensitivity, blockers, limitations, and retention posture. |
| Providers/auth | Provider metadata is not provider activation. Connector auth requires future GT-08 and secure handling. |
| Tools | Tool metadata is not tool execution. Connector actions that use tools require future GT-07 and S-04 approval. |
| Agents | Agent metadata is not agent execution. Connector-derived task or handoff metadata does not execute agents. |
| Cognitive Semantic System | Cognitive Semantic System substrate remains deferred. Connector-derived semantic records are metadata only and not truth by default. |
| Graphify | Graphify evidence remains supporting generated evidence only, not authority and not substrate. |
| Siamese | Siamese remains the living energy twin product vision, not product activation. Product source and product data remain GT-09 gated. |

## 12. Gate Mapping For Future Work
| Future action | Required route before consideration |
| --- | --- |
| Classify a connector path/account/workspace | GT-01 plus security/source classification review. |
| Track connector-derived output or summary | GT-02 and GT-12 plus generated-output/security review. |
| Adopt connector dependency or SDK | GT-03 plus security/license/provenance review. |
| Run connector validation | GT-04 with exact command/data/output scope. |
| Enforce connector security policy | GT-05 plus rollback and incident route. |
| Activate a connector runtime or Cadence loop | GT-06 plus GT-08/GT-15 and any required state gate. |
| Execute connector tools or generated commands | GT-07 plus S-04 exact action approval. |
| Use provider/API/MCP/auth/network | GT-08 plus S-03/S-04 secure approval. |
| Use product source, product data, or product telemetry | GT-09 plus product/security/validation/source-tracking review. |
| Treat connector-derived semantic data as substrate evidence | GT-10 governance review; substrate remains deferred unless future decision accepts it. |
| Persist connector state | GT-13 plus security, retention, rollback, and incident review. |
| Publish connector-derived material | GT-12 plus security, validation, governance, source, product, customer data, and retention review. |
| Roll back or respond to a connector incident | GT-15 or exact incident route. |

No gate is approved by P2.K4. This table only maps future prerequisites.

## 13. P2.KR And P3.0 Boundary
P2.K4 prepares vocabulary and boundary alignment only. P2.KR may later reconcile P2.K4 with the broader P2 knowledge-readiness closure if explicitly requested. P3.0 may later define activation-readiness framing if explicitly requested.

P2.K4 does not start P2.KR. P2.K4 does not start P3.0. References to P2.KR and P3.0 are handoff markers only, not work authorization.

## 14. Live Connection Boundary Invariants
| ID | Invariant |
| --- | --- |
| LCB-001 | P2.K4 is architecture alignment only. |
| LCB-002 | AGENT PLATFORM remains pre-active at AL-1. |
| LCB-003 | Live connector availability is not live connector activation. |
| LCB-004 | Live connectors are gate-controlled. |
| LCB-005 | Slack, email, GitHub issues, customer data, support, calendar, and product telemetry connector classes remain volatile or restricted by default. |
| LCB-006 | Volatile data is not permanent memory by default. |
| LCB-007 | Evergreen context must come from governed metadata, accepted records, or curated summaries with retained limitations. |
| LCB-008 | On-demand retrieval is exact-scope future action, not standing access or sync. |
| LCB-009 | Curated summaries are supporting evidence only and do not authorize raw connector retention. |
| LCB-010 | Never-persist classes must not become memory, context, evidence content, logs, generated output, publication, or Git-tracked material by default. |
| LCB-011 | Evidence supports; it does not decide. |
| LCB-012 | Validation evaluates; governance decides. |
| LCB-013 | Security constrains; it does not activate. |
| LCB-014 | Context inclusion is not permission. |
| LCB-015 | Provider metadata is not provider activation. |
| LCB-016 | Tool metadata is not tool execution. |
| LCB-017 | Agent metadata is not agent execution. |
| LCB-018 | Generated outputs remain generated-sensitive/local-only unless curated and governed. |
| LCB-019 | Graphify evidence is supporting generated evidence only, not authority. |
| LCB-020 | Cognitive Semantic System substrate remains deferred. |
| LCB-021 | GBrain / always-on / Hermes cadence is future Cadence. |
| LCB-022 | P2.K4 does not activate cadence, connectors, runtime, provider/auth, tools, agents, source loading, persistence, tracking, publication, product work, or substrate selection. |
| LCB-023 | P2.KR and P3.0 are future handoff markers only and are not started by P2.K4. |
| LCB-024 | Audit, retention, rollback, quarantine, redaction, publication blockers, source tracking blockers, and incident routes inherit P2.3 metadata-only posture. |

## 15. Created / Not Created Register
| Artifact or action | P2.K4 status |
| --- | --- |
| `0_architecture/governance/agent_platform_live_connections_cadence_boundary_strategy.md` | Created. |
| Live Connections / Cadence Boundary Strategy | Created. |
| Runtime code | Not created or modified. |
| Live connector | Not created, configured, connected, authenticated, started, subscribed, or monitored. |
| Slack connector | Not activated. |
| email connector | Not activated. |
| GitHub issues connector | Not activated. |
| customer data connector | Not activated. |
| Provider/auth/API/MCP | Not configured or approved. |
| Cadence | Not activated. |
| GBrain / always-on / Hermes cadence | Future/candidate vocabulary only. |
| Permanent memory | Not created. |
| Persistence/state store | Not created. |
| Source loading | Not approved. |
| Product source or product data | Not inspected or activated. |
| Tool execution | Not approved. |
| Agent execution | Not approved. |
| Validation execution | Not performed by this document. |
| Graphify rerun/adoption | Not performed or approved. |
| Generated outputs | Not modified or tracked. |
| `.gitignore` | Not modified. |
| `.graphifyignore` | Not modified. |
| Git staging, commit, push, force-add, or publication | Not performed or approved. |
| P2.KR | Not started. |
| P3.0 | Not started. |

## 16. Future Validation Targets
These are future validation targets only. P2.K4 does not execute validation.

| Future validation target | Purpose | Required future gate |
| --- | --- | --- |
| Connector availability non-activation phrase check | Confirm connector availability is not activation. | GT-04 if command-based. |
| Volatile vs evergreen classification check | Confirm live connector data is classified separately from evergreen context. | GT-04. |
| Never-persist class preservation check | Confirm secrets, credentials, customer data, product data, local-only, raw generated output, and unknown sensitivity are not persisted by default. | GT-04 plus GT-05. |
| Curated summary blocker propagation check | Confirm source class, sensitivity, blockers, limitations, and retention posture travel downstream. | GT-04. |
| Future Cadence non-runtime check | Confirm Cadence language does not imply runtime, connector, or memory activation. | GT-04 plus GT-06 if activation is proposed. |
| P2.KR / P3.0 boundary check | Confirm handoff markers do not start later tickets. | GT-04. |

## 17. Final Decision
P2.K4 accepts the Live Connections / Cadence Boundary Strategy as metadata-only architecture alignment.

Live connector availability is not live connector activation. Volatile data is not permanent memory by default. Live connectors are gate-controlled. GBrain / always-on / Hermes cadence is future Cadence. P2.K4 does not activate cadence.

Validation evaluates; governance decides. Cognitive Semantic System substrate remains deferred. AGENT PLATFORM remains pre-active at AL-1. P2.K4 stops before P2.KR and P3.0.
