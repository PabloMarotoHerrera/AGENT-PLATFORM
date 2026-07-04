# P2.K1 - Four Cs / Five Levels Mapping

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Four Cs / Five Levels Mapping |
| Ticket | P2.K1 |
| Status | Accepted Four Cs / Five Levels mapping |
| Date | 2026-07-04 |
| Scope | Map AGENT PLATFORM / Siamese against the Four Cs model and the five-level second brain / AIOS model as documentation-only knowledge architecture alignment. |
| Authority | Knowledge/retrieval architecture mapping only, not runtime activation, source loading, validation execution, vector DB implementation, embedding generation, graph DB implementation, Graphify adoption, GBrain implementation, Hermes activation, provider/auth approval, tool execution approval, agent execution approval, product activation, generated output tracking approval, source tracking approval, Cognitive Semantic System substrate selection, Cadence activation, or publication. |
| Related documents | P2.R, P2.1, P2.2, P2.3, P1.1, P1.2, P1.3, P1.4, P1.5, P0.1, P0.2, P0.3, G-19, Graphify Repo Map Summary, S-03, S-04, CSS ADR/audit, `.gitignore`, `.graphifyignore`. |
| Optional conceptual inputs | No local second-brain / AIOS video transcript, notes, or screenshots were present in the checked optional paths; the P2.K1 project brief is the conceptual source for Four Cs, five levels, second brain, AIOS, GBrain, Hermes, and Cadence terminology. |
| Output | Four Cs / Five Levels mapping. |

P2.K1 is architecture alignment only. AGENT PLATFORM remains pre-active at AL-1.

## 2. Purpose
P2 completed cross-lane integration readiness. P2.R closed P2 reconciliation and left no unresolved P2 drift. P2.K is a pre-P3 bridge for knowledge/retrieval architecture alignment.

P2.K1 maps AGENT PLATFORM against Four Cs and five retrieval/AIOS levels. It clarifies where the system is strong now, what remains candidate, and what remains blocked.

P2.K1 prepares inputs for P2.K2, P2.K3, P2.K4, and P2.KR. P2.K1 does not activate runtime. P2.K1 does not implement vector search. P2.K1 does not implement graph storage. P2.K1 does not activate GBrain, Hermes, or Cadence. P2.K1 does not start P2.K2, P2.K3, P2.K4, P2.KR, P3.0, P3.1, or P3.2.

## 3. Current Posture
| Area | Current state | P2.K1 interpretation | Blocked interpretation |
| --- | --- | --- | --- |
| AGENT PLATFORM activation level | Pre-active AL-1 metadata skeleton. | Architecture and governance records only. | Runtime activation. |
| P2 integration status | P2.1, P2.2, P2.3, and P2.R exist. | Integrated P2 metadata baseline. | P3 execution approval. |
| P2.R drift status | `no_unresolved_p2_drift`. | P2 baseline is reconciled for knowledge mapping. | Retroactive rewrite of P2 outputs. |
| Markdown governance memory | Current canonical governance/contracts surface. | Level 1/Level 2 documentation memory. | Runtime memory, source loading, or publication approval. |
| Context metadata | P1.1 and P2 contracts define safe context refs and metadata. | Strong Context surface. | Context inclusion as permission. |
| Evidence references | P2.2 defines EvidenceRef relationships. | Strong Connections surface. | Evidence as authority. |
| Audit/retention/rollback baseline | P2.3 defines metadata-only audit, retention, rollback, incident records. | Safety boundary for future retrieval/memory. | Runtime audit, persistence, rollback automation, or incident automation. |
| Graphify evidence | Graphify Repo Map Summary is curated generated supporting evidence. | Relationship evidence input only. | Graphify authority, truth engine, substrate, or adoption. |
| Cognitive Semantic System | Naming and substrate decisions remain governed and deferred. | Candidate semantic/relationship surface. | Substrate selection or ontology runtime. |
| Providers | Provider metadata exists. | Capability described as metadata only. | Provider/auth/API activation. |
| Tools | Tool boundary metadata exists. | Capability described as metadata only. | Tool execution. |
| Agents | Agent runtime boundary metadata exists. | Capability described as metadata only. | Agent runtime activation. |
| Product/Siamese | Siamese is product vision. | Product-readiness context only. | Product activation or product source inspection. |
| Vector search | Not implemented. | Level 3 candidate only. | Vector DB as default memory. |
| Graph/relationship layer | Graph-like relationships can be modeled as metadata. | Level 4 candidate/evidence only. | Graph as selected substrate. |
| Live connectors | Not active. | Future Connections/Cadence candidate only. | Connector ingestion or provider/API/MCP activation. |
| GBrain/Hermes/Cadence | Not active. | Future Level 5 Cadence candidate only. | Always-on brain OS behavior. |

AGENT PLATFORM remains pre-active at AL-1. P2.K1 is architecture alignment only. Current strength is Context and Connections metadata. Capabilities remain inactive. Cadence remains inactive. No retrieval mode becomes runtime approval through P2.K1.

## 4. Four Cs Model Definition
| C | Definition | AGENT PLATFORM examples | Current status | Allowed P2.K1 treatment | Blocked treatment | Relevant gates |
| --- | --- | --- | --- | --- | --- | --- |
| Context | Stable, curated, task-usable knowledge, governance records, contracts, decisions, and canonical summaries. | P0/P1/P2/P2.R governance docs, accepted contracts, roadmap records, curated summaries, markdown canonical memory. | Strong as documentation. | Map as canonical metadata/documentation memory. | Treating context inclusion as source loading or permission. | GT-01, GT-05, GT-12 if scope expands. |
| Connections | Relationships between records, refs, gates, evidence, lanes, blockers, decisions, and source classifications. | SourceRef, EvidenceRef, ValidationRef, SecurityRef, blockers, lane dependencies, Graphify evidence relationships. | Strong as metadata relationships. | Model relationships and propagation rules. | Selecting graph as substrate or treating relationships as authority. | GT-10, GT-11, GT-12, GT-13 if implementation/tracking expands. |
| Capabilities | Executable or callable actions such as tools, providers, agents, validation commands, API/MCP calls, workflows, and product operations. | Provider/auth/API calls, tool execution, validation execution, agent runtime, product operations. | Metadata-only and inactive. | Describe boundaries and required gates. | Execution, auth configuration, source loading, or product activation. | GT-04, GT-06, GT-07, GT-08, GT-09, S-04. |
| Cadence | Recurring, always-on, event-driven, scheduled, monitoring, memory-refresh, notification, or autonomous OS behavior. | GBrain-style memory, Hermes-style cadence, scheduled checks, live connector polling, autonomous routing. | Future-only and inactive. | Map future boundary and risk. | Always-on behavior, connector ingestion, scheduling, autonomous loops. | GT-06, GT-08, GT-13, GT-15, security/retention/audit gates. |

Context and Connections may be modeled as metadata. Capabilities and Cadence remain blocked until future gates.

## 5. Five Levels Model Definition
| Level | Definition | Retrieval pattern | Suitable data | AGENT PLATFORM current status | Allowed P2.K1 treatment | Blocked treatment | Future gate dependency |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Level 1 - routing files / folder navigation | File and folder routes that point readers or harnesses to canonical context. | Deterministic navigation. | README, governance folders, future manifests, future harness routing docs. | Present as repository documentation structure. | Document routing strategy. | Runtime routing or execution. | GT-01/GT-12 if routing expands source tracking. |
| Level 2 - markdown wiki / MOC / Obsidian-style memory | Full markdown canonical docs, maps of content, indexes, decision records. | Human and agent full-document reading with links. | Governance docs, architecture contracts, accepted roadmap, curated summaries. | Current canonical governance memory pattern. | Preserve markdown as canonical for decisions/contracts. | Publication, source loading, provider calls, tool calls, agent execution. | GT-12 if publishing or tracking expands. |
| Level 3 - semantic search / vector DB RAG | Embedding-based fuzzy retrieval over suitable corpora. | Similarity search and retrieval augmentation. | Large research corpus, video transcripts, large docs, lookup-like rule catalogs where retention permits. | Candidate only. | Identify candidate data types and blockers. | Embeddings, vector DB, semantic indexing, RAG runtime. | Future retrieval gate plus security/retention review. |
| Level 4 - knowledge graph / relationship graph / Graphify-like evidence | Explicit relationship graph across entities, refs, gates, decisions, and blockers. | Relationship traversal and dependency analysis. | Lane dependencies, SourceRef to EvidenceRef links, validation/security refs, blocker propagation, curated Graphify evidence. | Candidate/evidence only. | Model graph-like relationships as metadata. | Graph DB implementation, graph as canonical substrate, Graphify authority. | GT-10, GT-11, GT-12, GT-13. |
| Level 5 - always-on brain OS / GBrain / Hermes-style Cadence | Always-on memory OS, event ingestion, scheduled actions, notifications, autonomous routing. | Continuous monitoring, refresh, routing, and action cadence. | Future live connectors, task streams, notification streams, governance-approved runtime events. | Future-only and blocked. | Define readiness boundaries. | Always-on brain OS activation, Hermes/Cadence runtime, autonomous loops. | Runtime, provider/API/MCP, security, audit, retention, rollback, incident gates. |

Higher levels are not automatically better. Retrieval mode must depend on how the data will be queried and governed.

## 6. Current Four Cs Placement
| AGENT PLATFORM surface | Primary C | Secondary C | Current maturity | Evidence/source | Limitations | Activation boundary |
| --- | --- | --- | --- | --- | --- | --- |
| P0 activation gates | Context | Connections | Accepted governance metadata. | P0.1, P0.2, P0.3, G-01. | Gate docs only. | Do not activate runtime. |
| P1 context contract | Context | Connections | Accepted metadata contract. | P1.1. | Context inclusion is not permission. | No source loading. |
| P1 provider contract | Capabilities | Connections | Metadata-only boundary. | P1.2. | Provider metadata is not provider activation. | No provider/auth/API/MCP. |
| P1 tool contract | Capabilities | Connections | Metadata-only boundary. | P1.3. | Tool metadata is not tool execution. | No shell/tool execution. |
| P1 agent contract | Capabilities | Connections | Metadata-only boundary. | P1.4. | Agent metadata is not agent execution. | No agent runtime. |
| P1 Cognitive Semantic System contract | Connections | Context | Metadata-only semantic candidate. | P1.5 and CSS ADR/audit. | Substrate remains deferred. | No graph/vector/ontology runtime. |
| P2 shared vocabulary | Context | Connections | Canonical vocabulary. | P2.1. | Naming is not permission. | No activation. |
| P2 evidence contract | Connections | Context | Canonical evidence relationship contract. | P2.2. | Evidence supports; it does not decide. | No validation/source/tool/provider approval. |
| P2 audit/retention/rollback baseline | Context | Connections | Metadata-only safety baseline. | P2.3. | No runtime logging, persistence, rollback, or incident automation. | No storage/runtime activation. |
| P2.R reconciliation closure | Context | Connections | P2 drift closed. | P2.R. | Closure layer only. | Does not start P3 execution. |
| Graphify Repo Map Summary | Connections | Context | Curated generated supporting evidence. | Graphify Repo Map Summary. | Generated/local-only constraints remain. | No Graphify rerun/adoption/authority. |
| Markdown governance docs | Context | Connections | Current canonical memory. | Governance folder and README. | Must be read fully when precision matters. | No publication or source loading approval. |
| Source refs | Connections | Context | Metadata refs. | P2.1/P2.2. | Refs are not raw source access. | No source loading. |
| Evidence refs | Connections | Context | Canonical relationship refs. | P2.2 reconciled by P2.R. | Evidence is not authority. | No decision/activation. |
| Validation refs | Connections | Context | Validation posture refs. | P2.1/P2.2. | Validation evaluates; governance decides. | No validation execution. |
| Security refs | Connections | Context | Constraint refs. | P2.1/P2.2/S-03/S-04. | Security constrains; it does not activate. | No runtime enforcement. |
| Blockers | Connections | Context | Canonical stop conditions. | P2.1/P2.3. | Must propagate. | No bypass. |
| Retention records | Context | Connections | Metadata-only retention posture. | P2.3. | No persistence approval. | No raw retention/tracking. |
| Future provider/auth | Capabilities | Cadence | Future candidate only. | P1.2/S-03/S-04. | Credentials/auth blocked. | GT-08 required. |
| Future tool execution | Capabilities | Cadence | Future candidate only. | P1.3/S-04. | Execution blocked. | GT-07 required. |
| Future agent execution | Capabilities | Cadence | Future candidate only. | P1.4. | Runtime blocked. | GT-06 required. |
| Future Hermes/GBrain/Cadence | Cadence | Capabilities | Future candidate only. | P2.K conceptual brief. | Always-on risk. | Runtime/security/retention gates required. |
| Future live connectors | Cadence | Connections | Future candidate only. | P2.K conceptual brief/S-04. | Provider/API/MCP and retention risks. | GT-08/GT-13/GT-15 required. |

AGENT PLATFORM is currently strongest in Context and Connections metadata. Capabilities and Cadence remain explicitly inactive.

## 7. Current Five-Level Placement
| AGENT PLATFORM surface | Current level | Candidate future level | Current status | Future condition | Blocked inference |
| --- | --- | --- | --- | --- | --- |
| Governance documents | Level 1 + Level 2 | Level 3/4 for discovery only. | Canonical markdown memory. | Future retrieval review. | Vector or graph output replacing canonical docs. |
| P1/P2/P2.R contracts | Level 2 | Level 4 relationship metadata. | Canonical full-read contracts. | Future relationship mapping. | Partial search result as full decision. |
| Routing manifests | Level 1 candidate. | Level 1/2 formal manifest. | Not created by P2.K1. | P2.K3. | Runtime routing. |
| README / AGENTS.md / CLAUDE.md future projections | Level 1 candidate. | Harness routing docs. | README exists; AGENTS.md and CLAUDE.md absent in checks. | P2.K3. | Harness runtime activation. |
| Markdown MOC/wikis | Level 2 candidate. | Level 2 canonical index. | Not created by P2.K1. | P2.K3 or future MOC ticket. | Replacing source contracts. |
| Large research corpus | Not loaded. | Level 3 candidate. | Blocked unless scoped. | Retention/security/source review. | Vector indexing by default. |
| Video transcripts | Not present in checked paths. | Level 2 or Level 3 candidate. | Absent. | Optional notes/transcript supplied and governed. | Treating absent video claims as authority. |
| Meeting transcripts | Not loaded. | Level 3 candidate. | Blocked by default. | Retention and privacy review. | Permanent memory by default. |
| Rule catalogs | Level 2 as docs. | Level 3 if large/lookup-like. | Documentation only. | Retrieval mode decision. | Embedding without governance. |
| Entity/relation metadata | Level 2/metadata. | Level 4 candidate. | Cognitive Semantic System candidate metadata. | Substrate decision gates. | Ontology runtime or graph DB. |
| Graphify Repo Map Summary | Level 4-style evidence. | Level 4 relationship evidence. | Curated generated supporting evidence. | Future review if reused. | Authority/substrate/truth engine. |
| Raw Graphify outputs | Not loaded. | None by default. | Generated/local-only and blocked. | Exact future gate. | Raw output inclusion/tracking. |
| Live connector data | Not active. | Level 5 candidate. | Blocked. | Provider/API/MCP/security/retention readiness. | Connector ingestion now. |
| Slack/email/task data | Not active. | Level 5 candidate. | Blocked. | Connector, privacy, retention gates. | Permanent always-on memory by default. |
| GitHub issues | Not active. | Level 3/4/5 candidate depending scope. | Not ingested. | Source classification and connector gates. | Live connector activation. |
| Product/Siamese source | Not inspected. | None until GT-09. | Blocked. | Product gate and source classification. | Product activation/source loading. |
| Secrets/credentials | Not inspected. | No memory level. | Excluded. | Secure incident route only. | Indexing, summarizing, or retaining values. |
| Hermes/GBrain/Cadence candidates | Not active. | Level 5 candidate. | Future-only. | Full runtime/security/audit/retention readiness. | Always-on brain OS behavior. |

Current canonical level is Level 1 plus Level 2-style markdown governance. Level 3 vector search is candidate only. Level 4 graph/relationship evidence is candidate/evidence only. Level 5 always-on brain OS is future Cadence and blocked.

## 8. Context Mapping
| Context artifact type | Canonical storage/retrieval level | Why it belongs to Context | Allowed use | Blocked use | Retention posture |
| --- | --- | --- | --- | --- | --- |
| Governance decisions | Level 2 markdown. | Stable decisions guide future work. | Read as canonical governance memory. | Runtime activation or publication approval. | Metadata-only governance retention. |
| Activation gates | Level 2 markdown with Level 1 routing. | Gates define permitted transitions. | Cite constraints and blockers. | Gate bypass. | Governance metadata. |
| P1 contracts | Level 2 markdown. | Lane-specific metadata contracts. | Full-read contract context. | Source loading or activation. | Metadata-only. |
| P2 contracts | Level 2 markdown. | Cross-lane vocabulary, evidence, and retention baselines. | Integrated baseline. | Runtime memory or execution approval. | Metadata-only. |
| P2.R reconciliation closure | Level 2 markdown. | Closes temporal drift. | Interpret P2 as integrated. | Rewriting P2 docs. | Metadata-only. |
| P2.K documents | Level 2 markdown. | Knowledge architecture alignment. | Pre-P3 architecture bridge. | Implementation. | Metadata-only. |
| Stable architecture contracts | Level 2 markdown. | Need precision and full context. | Read complete docs when decisions matter. | Search snippet as authority. | Metadata-only. |
| Accepted roadmap records | Level 2 markdown. | Define planned sequence. | Roadmap context. | Starting downstream work without instruction. | Metadata-only. |
| Curated summaries | Level 2 markdown. | Summaries aid navigation. | Supporting context. | Replacing canonical sources. | Curated metadata retention. |
| Curated Graphify summaries as evidence only | Level 4-style evidence represented in Level 2 markdown. | Relationship evidence can support mapping. | Supporting generated evidence. | Authority, substrate, truth engine, raw output loading. | Generated-sensitive/local-only unless curated and governed. |
| Safe metadata refs | Level 2/relationship metadata. | Point to governed records without raw content. | Cross-reference context. | Raw source access. | Metadata-only. |
| Markdown canonical memory | Level 1 + Level 2. | Current canonical memory surface. | Governance/contracts memory. | Vector/graph/runtime replacement by default. | Metadata-only. |

Context inclusion is not permission. Markdown is currently canonical for governance/contracts.

## 9. Connections Mapping
| Connection type | Canonical representation | Current status | Allowed use | Blocked use | Downstream consumer |
| --- | --- | --- | --- | --- | --- |
| SourceRef relationships | `source_refs` / SourceRef metadata. | Canonical refs. | Source classification and scope metadata. | Raw source loading approval. | P2.K2, P2.K3, P3 source classification. |
| EvidenceRef relationships | `evidence_refs` / EvidenceRef. | Canonical P2.2 contract. | Evidence linkage and limitations. | Evidence as decision/authority. | P2.K2, P3.1, P3.2. |
| ValidationRef relationships | `validation_refs` / ValidationRef. | Canonical posture refs. | Validation target/posture mapping. | Validation execution or approval. | P3.1. |
| SecurityRef relationships | `security_refs` / SecurityRef. | Canonical constraints. | Security blocker propagation. | Runtime enforcement or permission grant. | P3.2. |
| Blocker propagation | P2.1 canonical blocker names. | Required invariant. | Preserve stop conditions. | Bypass by retrieval mode. | P2.K2, P2.K4, P3. |
| Sensitivity propagation | P2.1 sensitivity classes. | Required invariant. | Preserve memory/retrieval limits. | Treat unknown as safe. | P2.K2, P3.0. |
| Source classification propagation | P2.1 source classifications. | Required invariant. | Classify retrieval candidates. | Source expansion approval. | P2.K2, P3.0. |
| Lane dependency relationships | G-19 and P2.R. | Documented metadata. | Roadmap dependency mapping. | Parallel execution override. | P2.KR, P3 readiness. |
| Graphify evidence relationships | Graphify Repo Map Summary and `graphify_refs`. | Curated generated evidence only. | Supporting relationship evidence. | Raw output, authority, substrate, truth. | P2.K2/P2.K4 as limited evidence. |
| Cognitive Semantic System candidate relations | Semantic refs and substrate posture. | Candidate metadata. | Describe possible relations. | Graph/ontology runtime. | Future CSS decisions. |
| Product-readiness relationships | ProductRef/product posture. | Metadata-only. | Siamese product vision context. | Product source or activation. | Product gate planning. |
| Future audit/retention/rollback/incident refs | P2.3 refs. | Metadata baseline. | Future safety interfaces. | Runtime audit/persistence/rollback/incident automation. | P3.2 and future readiness tickets. |

Connections can be modeled as metadata and evidence relationships. Connections do not select graph as substrate.

## 10. Capabilities Mapping
| Capability surface | Current status | Required gate | Why blocked now | Allowed metadata representation | Blocked activation interpretation |
| --- | --- | --- | --- | --- | --- |
| Provider/auth/API calls | Metadata-only. | GT-08 plus S-03/S-04. | Auth/config/network not approved. | ProviderDescriptor, AuthRequirement, provider_auth_posture. | Provider activation or API call. |
| MCP calls | Metadata-only. | GT-08/GT-07 plus S-04. | MCP not approved. | MCP requirement metadata. | MCP activation. |
| Tool execution | Metadata-only. | GT-07. | Tool execution blocked. | ToolDescriptor, ToolRequest, ToolDecision metadata. | Shell/tool execution approval. |
| Shell/subprocess/filesystem/network/package-manager/build/test/CI/Git execution | Blocked. | GT-07 and exact future approval. | Side-effect and boundary risk. | Tool risk metadata and blockers. | Running commands or approving side effects. |
| Validation command execution | Blocked. | GT-04. | Validation readiness not active. | ValidationRef and validation_status. | Running validation/tests. |
| Agent runtime execution | Metadata-only. | GT-06. | Agent runtime inactive. | AgentRuntimeRef, AgentTaskRecord, AgentHandoffRecord metadata. | Agent execution or handoff execution. |
| Scheduler/orchestration/autonomous loops | Future-only. | Runtime/security/audit/retention gates. | Always-on behavior not approved. | Cadence candidate metadata. | Autonomous operation. |
| Product operations | Blocked. | GT-09. | Siamese product not activated. | ProductRef/product_posture. | Product activation or source inspection. |
| Source loading | Blocked. | GT-01/GT-05 and exact scope. | Context refs are not permission. | SourceRef metadata. | Reading raw local-only/product/external source. |
| Generated output tracking | Blocked. | GT-12/GT-15. | Generated outputs are sensitive/local-only by default. | generated_output_posture. | Tracking raw generated outputs. |
| Source tracking expansion | Blocked. | GT-02/GT-12. | Git/publication boundaries remain. | tracking_posture/source_tracking_blocker. | Staging, committing, force-adding, or publishing. |

Capabilities remain inactive. Metadata about a capability is not capability activation.

## 11. Cadence Mapping
| Cadence surface | Current status | Future required gates | Retention/rollback/incident needs | Noise/over-ingestion risk | Allowed P2.K1 representation | Blocked interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| Recurring checks | Future-only. | GT-04/GT-06/GT-15. | Audit, retention, rollback, incident routes. | Alert fatigue and stale state. | Candidate cadence metadata. | Scheduled execution now. |
| Always-on monitoring | Blocked. | Runtime/security/provider gates. | Retention minimization and incident handling. | Excessive surveillance and persistence. | Future boundary. | Always-on behavior. |
| Event-driven ingestion | Blocked. | Provider/API/MCP/security gates. | Source classification and quarantine routes. | Noisy or sensitive data ingestion. | Future connector boundary. | Live ingestion. |
| Automatic memory refresh | Future-only. | Memory/runtime/security gates. | Rollback and audit posture. | Overwriting canonical decisions. | Candidate risk. | Runtime memory mutation. |
| Automatic summarization | Future-only. | Source/retention/security gates. | Redaction and quarantine routes. | Summarizing forbidden content. | Candidate boundary. | Summary automation. |
| Automatic connector polling | Blocked. | Provider/API/MCP gates. | Retention and incident routes. | Provider payload over-ingestion. | Future connector classification. | Polling activation. |
| Automatic notifications | Future-only. | Runtime/provider gates. | Audit and incident routing. | Notification noise. | Candidate cadence metadata. | Notification runtime. |
| Autonomous task routing | Future-only. | Agent/runtime/tool/provider gates. | Rollback/audit/incident routes. | Misrouting and over-action. | Future GBrain/Hermes boundary. | Agent activation. |
| GBrain-style always-on memory | Future candidate. | Full Level 5 readiness. | Persistent memory retention and rollback. | Permanent memory pollution. | Future Cadence candidate. | Active system. |
| Hermes-style cadence/runtime | Future candidate. | Full runtime/security/provider readiness. | Audit, rollback, incident handling. | Unbounded automation. | Future Cadence candidate. | Hermes activation. |
| Scheduled validation/security checks | Future-only. | GT-04, GT-06, security readiness. | Audit and incident routes. | False confidence from scheduled checks. | Readiness candidate. | Running validation/security enforcement. |
| Live connector watches | Blocked. | Provider/API/MCP/source/security gates. | Retention, rollback, incident handling. | Sensitive/live stream ingestion. | Future connection/cadence boundary. | Connector activation. |

Cadence remains inactive. Always-on behavior requires runtime, provider/API/MCP, security, retention, rollback, incident, and audit readiness.

## 12. Level 1 - Routing Files / Folder Navigation
Level 1 means deterministic routing through files, folders, and future manifests so humans and harnesses can find canonical context without activating runtime behavior.

| Routing surface | Current status | Allowed use | Must not do |
| --- | --- | --- | --- |
| README | Present. | Workspace-level orientation. | Runtime activation. |
| Governance folder | Present. | Locate P0/P1/P2/P2.R/P2.K governance docs. | Source loading or execution. |
| Security folder | Present. | Locate S-03/S-04 constraints. | Security enforcement runtime. |
| cognitive_semantic_system folder | Present. | Locate naming/substrate ADR and decision audit. | Substrate selection. |
| Future memory manifest | Candidate. | Route to canonical docs. | Implement memory runtime. |
| Future AGENTS.md projection | Candidate; absent in checks. | Harness-agnostic routing idea for P2.K3. | Agent activation. |
| Future CLAUDE.md projection | Candidate; absent in checks. | Harness-specific routing projection if governed. | Provider/tool activation. |
| Future Codex/OpenCode routing | Candidate. | Map docs to harness instructions. | Runtime routing or execution. |

Level 1 routing helps harnesses find canonical context. Level 1 routing is allowed as documentation. It is not runtime routing or execution.

## 13. Level 2 - Markdown Wiki / MOC / Obsidian-Style Memory
Level 2 means canonical markdown memory, maps of content, and wiki/MOC-style organization over full governance documents.

| Markdown memory surface | Current or candidate status | Allowed use | Must not do |
| --- | --- | --- | --- |
| Governance docs | Current canonical memory. | Full-read governance and architecture context. | Replace with generated snippets when precision matters. |
| Architecture contracts | Current canonical memory. | Preserve exact wording and gates. | Convert to lossy permanent summaries. |
| Accepted roadmap records | Current/candidate. | Sequencing and dependency context. | Start downstream work without instruction. |
| Curated summaries | Current/candidate. | Navigation and evidence support. | Override canonical contracts. |
| Decision indexes | Candidate. | Improve findability. | Create decisions by index. |
| `memory.md` future candidate | Candidate. | Route to stable canonical memory. | Runtime memory implementation. |
| `decisions.md` future candidate | Candidate. | Index accepted decisions. | Replace decision records. |
| Routing docs future candidate | Candidate. | Harness-agnostic navigation. | Runtime routing. |

Governance/contracts should remain full markdown canonical because decisions, contracts, gates, and architecture records require precision. Future MOCs can organize canonical docs without replacing them. Secrets, credentials, provider auth material, product source before GT-09, raw local-only outputs, raw generated Graphify outputs, and unclassified sensitive content must not be moved into permanent markdown memory.

Markdown wiki/MOC is current canonical governance memory pattern. It does not authorize source loading, provider calls, tool calls, agent execution, or publication.

## 14. Level 3 - Semantic Search / Vector DB Candidate
Level 3 means semantic search / vector DB RAG over suitable, governed corpora. It is useful for fuzzy discovery across large text sets, not for replacing canonical governance reads.

| Data type | Candidate status | Useful when | Not suitable when | Boundary |
| --- | --- | --- | --- | --- |
| Large research corpus | Candidate. | Fuzzy lookup and topic discovery are needed. | Source rights, sensitivity, or retention are unclear. | Requires future source/security/retention review. |
| Video transcripts | Candidate if supplied and governed. | Concepts need fuzzy retrieval. | Transcript absent or ungoverned. | Optional materials absent in P2.K1 checks. |
| Large documentation corpus | Candidate. | Many docs need discovery support. | Decisions require exact full-read context. | Markdown remains canonical. |
| Rule catalogs if large and lookup-like | Candidate. | Rules are numerous and lookup-heavy. | Rule precision needs exact citation. | Future conformance checks required. |
| Meeting transcripts | Candidate only when fuzzy lookup is needed and retention permits. | Historical discovery is useful. | Private/volatile or retention-sensitive. | Privacy/retention gate required. |
| Technical references if licensed and scoped | Candidate. | Reference lookup is permitted. | Licensing/scope is unclear. | External-source review required. |
| Secrets | Blocked. | Never. | Always. | No memory/indexing. |
| Credentials | Blocked. | Never. | Always. | No memory/indexing. |
| Product source before GT-09 | Blocked. | Not before gate. | Current state. | Product source remains blocked. |
| Local-only raw outputs | Blocked by default. | Only exact future governed scope. | Current state. | Local-only remains local-only. |
| Raw Graphify outputs | Blocked by default. | Only exact future governed scope. | Current state. | Graphify raw output remains local-only. |
| Provider auth material | Blocked. | Never by default. | Current state. | S-03/GT-08. |
| Customer/private volatile data by default | Blocked. | Only exact governed scope. | Current state. | Privacy/retention gates. |
| Unclassified sensitive content | Blocked. | Not until classified. | Current state. | Unknown sensitivity blocks. |

Not everything should go into vector DB. Full-read markdown remains necessary for decisions and architecture contracts. Vector DB is candidate only. No embeddings, vector index, semantic search runtime, or RAG runtime is approved by P2.K1.

## 15. Level 4 - Knowledge Graph / Relationship Graph Candidate
Level 4 means relationship graph metadata across entities, refs, gates, evidence, blockers, and decisions. It can support dependency discovery but does not select a runtime substrate.

| Candidate relationship | Current representation | Why graph-like metadata may help | Boundary |
| --- | --- | --- | --- |
| Lane dependencies | G-19 and roadmap docs. | Shows sequencing and cross-lane constraints. | No orchestration runtime. |
| Gate dependencies | P0/G-01 docs. | Shows required approvals. | No gate bypass. |
| SourceRef -> EvidenceRef | P2.2/P2.1 refs. | Shows source/evidence relationships. | No raw source loading. |
| EvidenceRef -> ValidationRef | P2.2 refs. | Shows validation posture support. | No validation execution. |
| EvidenceRef -> SecurityRef | P2.2 refs. | Shows security constraints. | No permission grant. |
| Blocker propagation | P2.1/P2.3. | Shows stop-condition inheritance. | No blocker bypass. |
| Sensitivity propagation | P2.1/P2.3. | Shows memory/retrieval constraints. | Unknown never safe by default. |
| Object relationships across context/provider/tool/agent/Cognitive Semantic System | P1/P2 docs. | Shows cross-lane dependencies. | No runtime activation. |
| Roadmap dependencies | G-19/P2.R. | Shows ticket sequencing. | No downstream ticket start. |
| Product-readiness dependencies | ProductRef/product_posture. | Shows Siamese readiness constraints. | No product activation. |

Graph is useful for dependencies and relationship evidence, but graph is not selected as Cognitive Semantic System substrate. Graphify remains evidence only. Graph/relationship layer is candidate/evidence only. Graph remains candidate only. Graphify evidence cannot select graph as substrate.

## 16. Level 5 - Always-On Brain OS / GBrain / Hermes-Style Cadence Candidate
Level 5 means always-on brain OS behavior: persistent cadence, live ingestion, automatic memory refresh, event-driven routing, and autonomous or semi-autonomous action loops.

| Future requirement | Why required before Level 5 |
| --- | --- |
| Runtime gates | Always-on behavior is runtime behavior. |
| Provider/API/MCP gates | Live data and connector calls need explicit approval. |
| Security enforcement | Sensitive data, auth, tool use, and source access require constraints. |
| Retention posture | Live ingestion can over-retain data. |
| Rollback posture | Automated memory/actions require safe rollback paths. |
| Incident handling | Boundary breaches require safe incident routes. |
| Audit posture | Cadence needs auditability before activation. |
| Source classification | Live inputs must be classified before memory use. |
| Connector boundaries | Slack/email/tasks/issues and similar sources need exact scope. |
| Validation/security readiness | Readiness must precede runtime. |
| Human governance approval | Always-on behavior changes platform posture. |

Always-on ingestion can create noise and retention risk. Live connector data should not enter permanent memory by default. GBrain / always-on / Hermes cadence is future Cadence. P2.K1 does not activate Cadence.

## 17. Four Cs x Five Levels Matrix
| Four Cs row | Level 1 - routing files | Level 2 - markdown wiki | Level 3 - semantic search/vector DB | Level 4 - knowledge graph/relationship graph | Level 5 - always-on brain OS |
| --- | --- | --- | --- | --- | --- |
| Context | Current: strong folder/doc routing. Allowed: route to canonical docs. Candidate: memory manifest. Blocked: runtime routing. | Current: strongest canonical governance memory. Allowed: full-read docs/MOCs. Candidate: indexes. Blocked: replacing contracts. | Current: not active. Allowed: candidate analysis. Candidate: large research/video/docs. Blocked: embeddings/RAG now. | Current: relationship metadata only. Allowed: evidence relationships. Candidate: dependency graph. Blocked: graph substrate. | Current: inactive. Allowed: future boundary. Candidate: governed memory OS. Blocked: always-on behavior. |
| Connections | Current: doc links and refs. Allowed: SourceRef/EvidenceRef routing. Candidate: manifest links. Blocked: source loading. | Current: refs in markdown. Allowed: evidence/security/validation refs. Candidate: MOC relationship maps. Blocked: ref as permission. | Current: not active. Allowed: candidate retrieval by relation-heavy corpus. Candidate: discovery only. Blocked: vector as authority. | Current: candidate/evidence only. Allowed: graph-like metadata. Candidate: dependency traversal. Blocked: graph DB/substrate. | Current: inactive. Allowed: connector boundary mapping. Candidate: live relation updates. Blocked: live ingestion. |
| Capabilities | Current: capability docs route to blockers. Allowed: metadata navigation. Candidate: readiness routes. Blocked: execution. | Current: capability contracts in markdown. Allowed: describe required gates. Candidate: readiness docs. Blocked: activation by documentation. | Current: inactive. Allowed: candidate retrieval of capability docs. Candidate: search over approved docs. Blocked: tool/provider execution. | Current: inactive as runtime. Allowed: dependency metadata. Candidate: readiness graph. Blocked: orchestration runtime. | Current: blocked. Allowed: future risk mapping. Candidate: governed automation. Blocked: active tools/providers/agents. |
| Cadence | Current: absent/inactive. Allowed: route to future boundary docs. Candidate: P2.K4. Blocked: schedule execution. | Current: documented future only. Allowed: cadence risks in markdown. Candidate: readiness checklist. Blocked: active memory refresh. | Current: inactive. Allowed: candidate analysis. Candidate: retrieval for historical cadence docs. Blocked: automated indexing. | Current: inactive. Allowed: relationship model for future events. Candidate: event graph. Blocked: live graph runtime. | Current: future-only and blocked. Allowed: readiness boundary. Candidate: GBrain/Hermes-style future Cadence. Blocked: always-on brain OS. |

Context is currently Level 1/Level 2 strong. Connections are currently metadata-level and evidence-level; Level 4 is candidate only. Capabilities are metadata-described but not active. Cadence is future-only and blocked. Level 3 and Level 4 can support retrieval/relationship discovery later, but they do not replace markdown canonical governance memory. Level 5 requires future runtime and security readiness.

## 18. Current Position Verdict
| Question | Verdict |
| --- | --- |
| Current C emphasis | Context and Connections. |
| Current level emphasis | Level 1 and Level 2. |
| Candidate future levels | Level 3 and Level 4. |
| Blocked future level | Level 5 until Cadence readiness. |
| Capabilities status | Metadata-only, not active. |
| Cadence status | Inactive, future gated. |
| Graphify status | Generated supporting evidence only. |
| Cognitive Semantic System substrate | Deferred. |
| Product/Siamese status | Product vision, not activation. |

AGENT PLATFORM is a governed documentation/memory architecture at AL-1, not an activated AIOS runtime.

## 19. Interfaces With P2.1 / P2.2 / P2.3
| Upstream document | What P2.K1 consumes | Mapping impact | Downstream rule |
| --- | --- | --- | --- |
| P2.1 shared metadata vocabulary | Canonical statuses, blockers, sensitivity, source classifications, posture fields, refs, aliases, deprecated/prohibited terms. | Controls all P2.K1 naming. | P2.K1 must use P2.1 canonical vocabulary. |
| P2.2 EvidenceRef contract | EvidenceRef, ValidationRef, SecurityRef, SourceRef, GraphifyRef, ProductRef relationships and evidence boundaries. | Defines Connections and evidence-level mappings. | P2.K1 must preserve P2.2 evidence principle: evidence supports; it does not decide. |
| P2.3 audit/retention/rollback baseline | Retention, rollback, quarantine, publication, source tracking, incident, and generated-output boundaries. | Defines memory/retrieval safety boundaries. | P2.K1 must preserve P2.3 retention, rollback, quarantine, publication, source tracking, and incident boundaries. |
| P2.R reconciliation closure | `no_unresolved_p2_drift` and integrated P2 baseline. | Lets P2.K1 consume P2.1/P2.2/P2.3 as reconciled. | P2.K1 must preserve P2.R no-unresolved-drift status. |

## 20. Interfaces With P2.K2 / P2.K3 / P2.K4 / P2.KR
| Downstream ticket | What it should consume from P2.K1 | Unresolved item if any | Stop rule |
| --- | --- | --- | --- |
| P2.K2 - Hybrid Retrieval Mode Decision Matrix | Five-level mapping and data-type suitability. | None in P2.K1. | P2.K1 does not start P2.K2. |
| P2.K3 - Harness-Agnostic Routing / Memory Manifest Strategy | Four Cs and Level 1/2 mapping. | Future routing format not selected. | P2.K1 does not start P2.K3. |
| P2.K4 - Live Connections / Cadence Boundary Strategy | Cadence and live-connection boundaries. | Future live connector scope not selected. | P2.K1 does not start P2.K4. |
| P2.KR - Knowledge Architecture Reconciliation Closure | P2.K1 mapping plus future P2.K2-P2.K4 outputs. | Pending downstream tickets. | P2.K1 does not start P2.KR. |

P2.K2 should use the level mapping to decide retrieval mode by data type. P2.K3 should use Four Cs and Level 1/2 mapping to design harness-agnostic routing. P2.K4 should use Cadence and live-connection boundaries from this mapping. P2.KR should reconcile P2.K1-P2.K4 and prepare P3. P2.K1 does not start downstream tickets.

## 21. Boundaries And Non-Activation Rules
| Boundary | Rule |
| --- | --- |
| Markdown memory | Markdown memory is not source loading permission. |
| Wiki/MOC links | Wiki/MOC links are not source loading permission. |
| Vector search | Vector search candidate status is not vector DB approval. |
| Graph candidate | Graph candidate status is not graph DB approval. |
| Graphify evidence | Graphify evidence is not authority. |
| Cognitive Semantic System relations | Cognitive Semantic System relations are not substrate selection. |
| Live connector boundary | Live connector boundary is not connector activation. |
| GBrain/Hermes/Cadence candidate status | GBrain/Hermes/Cadence candidate status is not runtime activation. |
| Capabilities metadata | Capabilities metadata is not capability activation. |
| Product/Siamese references | Product/Siamese references are not product activation. |
| Security | Security constrains; it does not activate. |
| Validation | Validation evaluates; governance decides. |
| Evidence | Evidence supports; it does not decide. |

Graphify evidence is supporting generated evidence only, not authority. Cognitive Semantic System substrate remains deferred.

## 22. Future Validation Targets
These are future validation targets only and are not executed by P2.K1.

| Future validation target | Purpose |
| --- | --- |
| Four Cs coverage completeness | Check Context, Connections, Capabilities, and Cadence coverage. |
| Five levels coverage completeness | Check all five levels are mapped. |
| P2.1 vocabulary conformance | Check canonical vocabulary use. |
| P2.2 evidence principle preservation | Check evidence supports but does not decide. |
| P2.3 retention/rollback/incident boundary preservation | Check safety boundaries remain. |
| Context/Connections/Capabilities/Cadence classification consistency | Check surface classification. |
| Level 1/2 markdown canonical memory invariant | Check markdown remains canonical for governance. |
| Level 3 vector-candidate-only invariant | Check vector remains candidate only. |
| Level 4 graph-candidate-only invariant | Check graph remains candidate only. |
| Level 5 Cadence-blocked invariant | Check Cadence remains inactive. |
| Graphify evidence-only invariant | Check Graphify evidence remains supporting only. |
| Cognitive Semantic System substrate-deferred invariant | Check substrate remains deferred. |
| Capabilities-not-active invariant | Check capabilities remain inactive. |
| Cadence-not-active invariant | Check Cadence remains inactive. |
| Product-inactive invariant | Check Siamese remains product vision only. |
| Live connector non-ingestion invariant | Check live connectors remain inactive. |
| No-secret/no-credential memory invariant | Check memory/retrieval excludes secret and credential content. |

## 23. Future Hardening Candidates
These are future candidates only and are not started by P2.K1.

| Candidate ticket | Purpose | P2.K1 status |
| --- | --- | --- |
| P2.K-HARD-01 - Four Cs Classification Schema Candidate | Convert classification into a future schema candidate. | Not started. |
| P2.K-HARD-02 - Five Levels Retrieval Readiness Checklist | Define future checks by retrieval level. | Not started. |
| P2.K-HARD-03 - Markdown Canonical Memory Index / MOC Candidate | Prepare future MOC/index design. | Not started. |
| P2.K-HARD-04 - Vector Search Candidate Criteria | Define what may enter semantic search/vector DB. | Not started. |
| P2.K-HARD-05 - Graph Relationship Candidate Criteria | Define graph/relationship candidate criteria. | Not started. |
| P2.K-HARD-06 - Cadence Readiness Pre-Gate | Define pre-gate needs for Cadence. | Not started. |
| P2.K-HARD-07 - GBrain / Hermes Boundary Review | Review future GBrain/Hermes boundaries. | Not started. |
| P2.K-HARD-08 - Harness Routing Projection Readiness | Prepare harness routing projections. | Not started. |
| P2.K-HARD-09 - P3 Source Classification Mapping From Four Cs | Map Four Cs to P3 source classification readiness. | Not started. |
| P2.K-HARD-10 - Live Connector Classification Checklist | Define connector classification criteria. | Not started. |

## 24. Created / Not Created Register
| Artifact or action | P2.K1 status |
| --- | --- |
| `0_architecture/governance/agent_platform_four_cs_five_levels_mapping.md` | Created. |
| Four Cs / Five Levels mapping document | Created. |
| P2.R document | Not modified. |
| P2.1 document | Not modified. |
| P2.2 document | Not modified. |
| P2.3 document | Not modified. |
| P1 documents | Not modified. |
| P0 documents | Not modified. |
| Runtime code | Not modified. |
| Context runtime code | Not modified. |
| Provider adapter implementation | Not modified. |
| Tool execution implementation | Not modified. |
| Agent runtime implementation | Not modified. |
| Cognitive Semantic System implementation | Not modified. |
| Validation registry implementation | Not modified. |
| Security implementation | Not modified. |
| `3_platform/_governed_skeleton/` | Not modified. |
| Source loading | Not approved. |
| Product source | Not inspected. |
| Hermes source | Not inspected. |
| Graphify implementation source | Not inspected. |
| External source | Not inspected. |
| Secrets | Not inspected. |
| Credentials | Not inspected. |
| `.env` | Not inspected. |
| Provider/auth | Not configured. |
| Tool execution | Not approved. |
| Agent execution | Not approved. |
| Validation command | Not executed. |
| Tests | Not executed. |
| Vector DB | Not implemented. |
| Embeddings | Not generated. |
| Semantic search | Not implemented. |
| Graph DB | Not implemented. |
| Ontology runtime | Not implemented. |
| GBrain | Not implemented. |
| Hermes | Not activated. |
| Cadence | Not activated. |
| Always-on behavior | Not activated. |
| Graphify | Not rerun. |
| `/graphify` | Not run. |
| Graphify as authority | Not adopted. |
| Graphify as truth engine | Not adopted. |
| `.graphifyignore` | Not modified. |
| `.gitignore` | Not modified. |
| Generated outputs | Not modified or tracked. |
| Source tracking expansion | Not approved. |
| Publication | Not approved. |
| Product activation | Not approved. |
| Cognitive Semantic System substrate | Not selected. |
| Graph substrate | Not selected. |
| P2.K2 | Not started. |
| P2.K3 | Not started. |
| P2.K4 | Not started. |
| P2.KR | Not started. |
| P3.0 | Not started. |
| P3.1 | Not started. |
| P3.2 | Not started. |
| P3.R | Not started. |
| Git staging/commit/push/force-add/publication | Not authorized or performed. |

## 25. Recommended Next Tickets
After P2.K1, the recommended queue is:

| Ticket | Recommendation |
| --- | --- |
| P2.K2 - Hybrid Retrieval Mode Decision Matrix | Recommended actual next ticket after explicit instruction. |
| P2.K3 - Harness-Agnostic Routing / Memory Manifest Strategy | Follow after P2.K2 or as governed sequence allows. |
| P2.K4 - Live Connections / Cadence Boundary Strategy | Follow after P2.K2/P2.K3 or as governed sequence allows. |
| P2.KR - Knowledge Architecture Reconciliation Closure | Only after P2.K1-P2.K4 are complete. |
| P3.0 - Controlled Source Classification Readiness | Only after P2.KR is complete and explicitly approved. |
| P3.1 - Validation Execution Readiness | Only after P2.KR/P3.0 as governed. |
| P3.2 - Security Enforcement Readiness | Only after P2.KR/P3.0 as governed. |

Recommended actual: P2.K2 - Hybrid Retrieval Mode Decision Matrix.

Do not start P2.K2. Do not start P2.K3. Do not start P2.K4. Do not start P2.KR. Do not start P3.0. Do not start P3.1. Do not start P3.2. Do not start P3.R.

## 26. Final Verdict
| Question | Answer |
| --- | --- |
| What did P2.K1 create? | The Four Cs / Five Levels Mapping document. |
| What did P2.K1 map? | AGENT PLATFORM / Siamese governance state against Context, Connections, Capabilities, Cadence and five retrieval/AIOS levels. |
| Which Four Cs were defined? | Context, Connections, Capabilities, and Cadence. |
| Which five levels were defined? | Routing files, markdown wiki/MOC, semantic search/vector DB, knowledge graph/relationship graph, and always-on brain OS. |
| Where is AGENT PLATFORM currently strongest? | Context and Connections metadata. |
| Which C surfaces are currently metadata-only? | Context, Connections, and capability/cadence descriptions. |
| Which C surfaces remain inactive? | Capabilities and Cadence remain inactive. |
| Which levels are currently covered by documentation? | Level 1 routing/folder navigation and Level 2 markdown governance memory. |
| Which levels are candidates only? | Level 3 semantic search/vector DB and Level 4 knowledge graph/relationship graph. |
| Which level remains blocked? | Level 5 always-on brain OS / GBrain / Hermes-style Cadence. |
| Did P2.K1 implement vector search? | No. |
| Did P2.K1 implement graph storage? | No. |
| Did P2.K1 activate GBrain, Hermes, or Cadence? | No. |
| Did P2.K1 activate runtime? | No. |
| Did P2.K1 execute validation? | No. |
| Did P2.K1 approve provider/auth? | No. |
| Did P2.K1 approve tool/agent execution? | No. |
| Did P2.K1 inspect product source? | No. |
| Did P2.K1 rerun or adopt Graphify? | No. |
| Did P2.K1 approve generated output tracking or source tracking expansion? | No. |
| Did P2.K1 select Cognitive Semantic System substrate? | No. Cognitive Semantic System substrate remains deferred. |
| What is the next recommended ticket? | P2.K2 - Hybrid Retrieval Mode Decision Matrix, after explicit instruction only. |

Stop rule: After completing P2.K1, STOP. Do not start P2.K2. Do not start P2.K3. Do not start P2.K4. Do not start P2.KR. Do not start P3.0. Do not start P3.1. Do not start P3.2. Do not start P3.R. Do not implement code. Do not implement routing runtime. Do not implement memory runtime. Do not implement vector DB. Do not generate embeddings. Do not implement semantic search. Do not implement graph DB. Do not implement ontology runtime. Do not implement GBrain. Do not activate Hermes. Do not activate Cadence. Do not activate always-on behavior. Do not run validation. Do not run tests. Do not inspect secrets. Do not inspect credentials. Do not inspect `.env`. Do not configure provider/auth. Do not execute tools. Do not activate agents. Do not activate runtime behavior. Do not load source. Do not inspect product source. Do not inspect Hermes source. Do not inspect Graphify implementation source. Do not rerun Graphify. Do not modify generated outputs. Do not approve generated output tracking. Do not approve source tracking expansion. Do not modify `.gitignore`. Do not modify `.graphifyignore`. Do not select Cognitive Semantic System substrate. Do not select graph as substrate. Do not adopt Graphify as authority. Do not treat Graphify as truth engine. Do not stage, commit, push, force-add, or publish.
