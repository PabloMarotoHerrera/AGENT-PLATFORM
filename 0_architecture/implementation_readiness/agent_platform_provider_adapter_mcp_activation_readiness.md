# IR-06 - Provider / Adapter / MCP Activation Readiness
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Provider / Adapter / MCP Activation Readiness |
| Ticket | IR-06 |
| Status | Accepted provider / adapter / MCP activation readiness assessment |
| Date | 2026-07-02 |
| Scope | Activation-readiness assessment for future providers, adapters, APIs, MCP servers/tools/resources, network, auth, credentials, and gates for AGENT PLATFORM / Siamese after IR-05. |
| Authority | Activation-readiness assessment only, not provider/adapter/MCP activation. |
| Related documents | IR-00 through IR-05, P-A, P-00 through P-10, M-A, M-04, M-06, W-series, V-series, S-series, CSS-series, H-series, `.gitignore`, `README.md`, Siamese Product Vision |
| Assessment target | Future providers, adapters, APIs, MCP servers/tools/resources, network, auth, credentials, and gates |

## 2. Purpose
IR-00 found the platform not ready for implementation but ready for planning tickets. IR-01 reserved `3_platform` conceptually only. IR-02 blocked source tracking/source tree creation. IR-03 blocked scripts/tools/tests creation and execution. IR-04 blocked dependency adoption and package manager execution. IR-05 blocked runtime, agents, context engine, tool execution, memory/state, and provider/API/MCP activation.

IR-06 assesses provider / adapter / MCP activation readiness. It does not activate providers, adapters, MCP, APIs, network, auth, tools, runtime, or agents. IR-06 prepares IR-07 after instruction and does not start IR-07.

## 3. Provider / Adapter / MCP Activation Readiness Definition
Activation readiness is a governance assessment of needed provider, adapter, API, network, auth, credential, tool, and MCP capabilities, their risks, and gates before activation, implementation, execution, tracking, or publication.

Readiness is not activation, authentication approval, network approval, API call approval, provider permission, MCP activation, adapter implementation, tool execution, dependency adoption, source tracking, or product activation.

## 4. Decision Summary
No provider is activated. No adapter is created or activated. No MCP server is activated. No MCP tool or resource is invoked. No API call is made. No network call is made. No authentication flow is started. No credential is used, inspected, copied, summarized, or validated. No provider config is created.

No runtime/tool execution is approved. No dependencies are adopted. No source tracking is approved. No `3_platform` contents are inspected or approved. Governance docs under `0_architecture/implementation_readiness/` remain trackable as docs only by exact path and instruction. IR-07 may assess Cognitive Semantic System substrate decision gate after explicit instruction.

## 5. Authority Boundary
| Layer | IR-06 boundary |
| --- | --- |
| Governance | Decides provider activation, adapter activation, MCP activation, API/network/auth use, credential use, tool execution, source tracking, publication, exceptions, implementation, and lifecycle. |
| Validation | Evaluates provider/adapter/MCP evidence and future activation results. |
| Security | Constrains secrets, credentials, local-only material, data exposure, network/auth, provider terms, MCP resources, generated outputs, logs, telemetry, and publication. |
| IR-06 | Assesses activation readiness only. |
| Git | Records artifacts but does not approve provider/adapter/MCP status. |
| Agents | May prepare safe readiness metadata but cannot authenticate, call, execute, activate, adopt, stage, commit, push, publish, or start IR-07. |

## 6. Source Boundary
IR-05 controls runtime/agent/context/tool boundaries. IR-04 controls dependency readiness. IR-03 controls scripts/tools/tests readiness. IR-02 controls source tree/tracking. P-08/P-09/P-10 control product Git/dependency/validation. M-04 controls agent/context/runtime/provider/adapter migration. M-06/W-13/V-05 control external-source metadata and validation. H-series controls harness/provider/tool/MCP. S-series controls credential, access, execution, network, local-only, and publication. V-series controls evidence/proof/validation.

Raw `3_platform`, `2_products`, and `4_external/sources` are not inspected. Secrets and credentials are not inspected. Safe metadata only.

## 7. Current Activation Posture
| area | current posture | readiness status | blocked action | future route |
| --- | --- | --- | --- | --- |
| provider activation | Evidence only. | blocked_not_activated | Activate provider. | Provider gate. |
| adapter creation | Conceptual only. | blocked_not_created | Create adapter. | Adapter gate. |
| adapter activation | Not approved. | blocked_not_activated | Route calls. | Adapter gate. |
| API calls | Blocked. | blocked_not_executed | Call endpoint. | API/network/auth gate. |
| network calls | Blocked. | blocked_not_executed | Send/receive. | Network gate. |
| authentication flows | Blocked. | blocked_not_authenticated | Login/token/session. | Auth gate. |
| credential use | Excluded. | blocked_not_authenticated | Inspect/use credential. | Security gate. |
| provider config | Not created. | blocked_not_created | Config/provider file. | Provider gate. |
| MCP server activation | Blocked. | blocked_not_activated | Start/connect server. | MCP gate. |
| MCP tool invocation | Blocked. | blocked_not_executed | Invoke tool. | MCP gate. |
| MCP resource access | Blocked. | blocked_not_executed | Read resource. | MCP gate. |
| tool execution | Not approved. | blocked_not_executed | Run tool/shell. | IR-05/IR-08. |
| runtime/provider bridge | No runtime. | blocked_pending_IR07/IR08/I00 | Build bridge. | Runtime gate. |
| provider SDK/package | Candidate only. | planning_only | Adopt/install SDK. | IR-04 gate. |
| logs/telemetry | Sensitive by default. | planning_only | Emit/retain. | IR-08/security. |
| generated outputs | Local-only by default. | planning_only | Publish/track. | Output review. |
| product provider integration | Products inactive. | blocked_not_activated | Integrate products. | Product governance. |
| `3_platform` contents | Unknown/uninspected. | blocked_pending_IR07/IR08/I00 | Infer/use/track. | Future classification. |

## 8. Provider Class Catalog
| provider class | meaning | current status | activation risk | required future gate | blocked now |
| --- | --- | --- | --- | --- | --- |
| LLM_provider | Model/API service. | candidate_only | prompt/data/cost/retention. | Provider gate. | Calls/auth. |
| cloud_provider | Cloud compute/storage/service. | candidate_only | account/data/cost. | Provider gate. | Auth/network. |
| storage_provider | Object/file/database storage. | candidate_only | data retention/exposure. | Provider gate. | Read/write. |
| identity_auth_provider | OAuth/session/identity. | candidate_only | credentials/privacy. | Auth gate. | Login/session. |
| package_registry_provider | Package index/registry. | candidate_only | supply-chain/auth. | IR-04/provider gate. | Resolve/publish. |
| telemetry_analytics_provider | Monitoring/analytics. | candidate_only | tracking/privacy. | Provider/security gate. | Telemetry. |
| hosting_deployment_provider | CDN/domain/TLS/hosting. | candidate_only | publication/provider lock-in. | Provider/product gate. | Deploy. |
| simulation_solver_provider | External/domain solver service. | candidate_only | data/native/license. | Product/provider gate. | Solver use. |
| Omniverse_Nucleus_provider | Collaboration/assets provider. | candidate_only | auth/storage/terms. | Product/provider gate. | Nucleus auth. |
| data_ingestion_provider | Sensor/import/data feed. | candidate_only | building/user data. | Data/security gate. | Ingest. |
| notification_provider | Email/SMS/webhook. | candidate_only | PII/spam/cost. | Provider gate. | Send. |
| local_service_provider | Local DB/daemon/service. | candidate_only | local state/ports. | Runtime/security gate. | Start/connect. |
| unknown_provider | Unclassified provider. | blocked | unknown risk. | Classification. | Any use. |

## 9. Adapter Class Catalog
| adapter class | meaning | current status | authority limit | required future gate | blocked now |
| --- | --- | --- | --- | --- | --- |
| provider_API_adapter | Mediates API/provider calls. | conceptual_only | No calls. | Adapter/provider gate. | Implementation. |
| local_tool_adapter | Wraps local tool. | conceptual_only | No execution. | Tool/security gate. | Tool use. |
| shell_command_adapter | Mediates shell. | conceptual_only | Exact command only later. | Tool gate. | Shell. |
| file_system_adapter | Mediates file access. | conceptual_only | No local-only widening. | Security gate. | Broad reads. |
| Git_adapter | Mediates Git. | conceptual_only | No mutation approval. | Git governance. | Stage/commit. |
| validation_adapter | Links validation. | conceptual_only | Cannot approve. | IR-08. | Registry. |
| security_adapter | Links security policy. | conceptual_only | Cannot enforce yet. | IR-08. | Enforcement. |
| product_backend_adapter | Connects products/backend. | conceptual_only | Product-scope only. | Product gate. | Activation. |
| Omniverse_adapter | Interface adapter candidate. | conceptual_only | Interface only. | Product/provider gate. | Kit/Nucleus. |
| EnergyPlus_adapter | Solver adapter candidate. | conceptual_only | Solver not model. | Product/provider gate. | Solver run. |
| web_platform_adapter | Web/auth/deploy bridge. | conceptual_only | No deploy/auth. | Product/provider gate. | Web activation. |
| desktop_adapter | Desktop/local bridge. | conceptual_only | No installer/daemon. | Product gate. | Runtime. |
| CLI_adapter | CLI/command bridge. | conceptual_only | No shell approval. | Tool/product gate. | Commands. |
| MCP_adapter | MCP mediation. | conceptual_only | No MCP activation. | MCP gate. | Server/tool/resource. |
| unknown_adapter | Unclassified adapter. | blocked | No authority. | Classification. | Any use. |

## 10. MCP Class Catalog
| MCP class | meaning | current status | activation risk | required future gate | blocked now |
| --- | --- | --- | --- | --- | --- |
| MCP_server | Server process/endpoint. | candidate_only | file/network/tool exposure. | MCP gate. | Start/connect. |
| MCP_tool | Callable capability. | candidate_only | mutation/execution. | MCP/tool gate. | Invoke. |
| MCP_resource | Exposed data/resource. | candidate_only | data leakage. | MCP/security gate. | Access. |
| MCP_prompt | Prompt template/input. | candidate_only | authority confusion. | MCP/context gate. | Treat as policy. |
| MCP_transport | stdio/http/socket transport. | candidate_only | network/process/auth. | MCP/network gate. | Connect. |
| MCP_auth | Auth mechanism. | candidate_only | credentials/session. | Auth/security gate. | Authenticate. |
| MCP_filesystem_scope | File access boundary. | candidate_only | local-only exposure. | MCP/security gate. | File access. |
| MCP_network_scope | Network boundary. | candidate_only | data egress. | MCP/network gate. | Network. |
| MCP_provider_bridge | Provider bridge via MCP. | candidate_only | provider/cost/data. | MCP/provider gate. | Bridge. |
| MCP_audit_log | MCP trace/log evidence. | conceptual_only | sensitive logs. | IR-08/security. | Logging runtime. |
| unknown_MCP_capability | Unclassified MCP capability. | blocked | unknown risk. | Classification. | Any use. |

## 11. Provider Authority Rules
Provider credentials are not provider permission. Provider availability is not activation approval. Provider docs are not terms approval. Provider SDK presence is not integration approval. Provider API compatibility is not call approval. Provider status is evidence only until governance approves activation. Providers cannot override governance, validation, security, or product boundaries.

## 12. Adapter Authority Rules
Adapter existence is not adapter activation. Adapter design is not implementation. An adapter can mediate only approved scopes, cannot widen permissions, cannot convert local-only data into publishable data, cannot turn a provider into root authority, and produces evidence unless governance decides otherwise.

## 13. MCP Authority Rules
MCP availability is not MCP activation. MCP server listing is not permission. MCP tool discovery is not invocation approval. MCP resource discovery is not data access approval. MCP prompts are not authority. MCP transport availability is not network approval. MCP can operate only under exact future scope, permissions, logging, and governance.

## 14. Credential / Secret / Auth Boundary
Secrets, credentials, tokens, cookies, OAuth flows, API keys, provider sessions, registry auth, browser auth, Nucleus auth, cloud auth, and local auth stores are excluded. IR-06 does not read, copy, summarize, validate, test, or use credential values. Unknown credential presence is a stop condition.

Future auth use requires least privilege, rotation, revocation, storage, redaction, logging, retention, user consent, and security review.

## 15. Network / API Boundary
Network access is blocked by default. API calls are blocked by default. Remote metadata calls are blocked by default. Telemetry, analytics, update checks, package registry calls, provider calls, cloud calls, Nucleus calls, hosting calls, and MCP transport calls are blocked.

Future network/API use requires endpoint, method, payload, data classification, auth posture, cost, terms, retention, rate limits, timeout, failure behavior, and rollback.

## 16. Data Exposure Boundary
Provider/API/MCP activation can expose prompts, context, product metadata, building/sensor data, local paths, logs, generated outputs, source snippets, secrets, credentials, and user data. Local-only data, product source, and raw external source remain local-only. Context inclusion is not permission to transmit data. Future transfer requires classification, minimization, redaction, retention, publication posture, and governance approval.

## 17. Logging / Telemetry / Audit Boundary
No logging or telemetry runtime is created by IR-06. Provider/API/MCP activation may create logs, traces, request IDs, cost records, telemetry, caches, or audit artifacts. Generated logs are sensitive by default. Future activation requires logging, redaction, retention, auditability, storage, access-control, and deletion policy.

## 18. Cost / Quota / Terms Boundary
Provider/API/MCP use may incur cost, quotas, rate limits, account restrictions, data/privacy/license terms, export limits, and publication constraints. IR-06 performs no terms approval. Future activation requires cost owner, quota limits, terms/data-use review, cancellation/revocation path, and monitoring policy.

## 19. Product Relationship
Products remain inactive. Product source remains local-only. Product provider integrations are not approved. Omniverse/Nucleus, EnergyPlus/OpenStudio solver/provider execution, web auth/deploy/hosting, and desktop/CLI provider or shell integration are not approved. Product activation remains blocked.

## 20. 3_platform Relationship
`3_platform` remains conceptually reserved only. Existing `3_platform` contents remain uninspected and unapproved. Provider configs, adapter code, MCP configs, credentials, or runtime hints cannot be inferred from it. No `3_platform` source is approved or tracked by IR-06.

## 21. Git / Source Tracking Relationship
IR-06 does not approve source tracking, change product Git posture, or modify `.gitignore`. Provider/adapter/MCP source or config is not trackable now. Governance docs only are trackable by exact path and human instruction. No force-add is authorized. No `git add .` is authorized.

## 22. Dependency Relationship
Provider/adapter/MCP activation may require packages, SDKs, CLIs, native tools, servers, credentials, or registry access. None are adopted by IR-06. Dependency readiness remains candidate-only. Provider SDK/package adoption requires IR-04 gates and future exact governance.

## 23. Runtime / Agent / Context Relationship
No runtime exists to safely execute provider/adapter/MCP behavior. Agents cannot self-authorize provider/API/MCP use. Context inclusion is not permission to transmit context. Tool execution is not approved. Runtime/agent/context boundaries remain planning-only.

## 24. Validation / Security Relationship
IR-06 does not create validation registry, security enforcement, access controls, credential vault, policy runtime, audit logging runtime, or provider sandbox. Future activation must be testable, auditable, least-privilege, reversible, and security-reviewed. Validation evaluates; governance decides.

## 25. Cognitive Semantic System Relationship
Cognitive Semantic System is the accepted name. Substrate remains undecided. Graph remains a candidate only. Graphify remains evidence/historical/external/prohibited/candidate-evidence only, not authority. Provider/API/MCP needs do not decide CSS substrate, and availability cannot become semantic truth. CSS substrate gate is deferred to IR-07.

## 26. Provider Activation Gate
Before provider activation: provider name, purpose, owner, endpoint/scope, auth/credential posture, data classes, input/output behavior, network behavior, logging/telemetry/cost behavior, terms/license/privacy review, dependency/SDK posture, validation plan, security review, rollback/revocation path, and governance approval must be recorded.

IR-06 does not pass this gate.

## 27. Adapter Activation Gate
Before adapter creation or activation: adapter purpose, provider/product/runtime scope, authority limits, exact path/source posture, dependency posture, data transformation rules, error/failure behavior, logging/audit behavior, security review, validation plan, rollback/removal path, and governance approval must be recorded.

IR-06 does not pass this gate.

## 28. MCP Activation Gate
Before MCP server/tool/resource activation: server name, transport, tool/resource list, permission scope, filesystem/network scope, auth posture, data exposure posture, logging/audit posture, dependency/runtime posture, security review, validation plan, rollback/revocation path, and governance approval must be recorded.

IR-06 does not pass this gate.

## 29. API / Network / Auth Gate
Before API/network/auth use: exact endpoint/command/flow, method/payload, working context, auth material handling, data classification, expected response, side effects, cost/quota, logs/telemetry, timeout/failure behavior, rollback/revocation, and human approval must be recorded.

IR-06 does not pass this gate.

## 30. Readiness Status Model
Statuses: readiness_documented, provider_not_activated, adapter_not_created, adapter_not_activated, MCP_not_activated, API_calls_blocked, network_blocked, auth_not_started, credentials_not_used, tool_execution_not_approved, dependency_review_pending, security_review_pending, validation_registry_pending, source_tracking_not_approved, implementation_not_started, rejected_for_activation_now.

Current status: readiness_documented + provider_not_activated + adapter_not_created + MCP_not_activated + API_calls_blocked + network_blocked + auth_not_started.

## 31. Readiness Gate Model
| Gate | pass condition | current posture | blocker if missing |
| --- | --- | --- | --- |
| IR06-G01 IR-05 exists | IR-05 boundary doc exists. | Present. | Runtime/tool posture unknown. |
| IR06-G02 no runtime/tool execution approved | No execution approval. | Preserved. | Stop/security. |
| IR06-G03 no dependencies adopted | No adoption/install. | Preserved. | Stop. |
| IR06-G04 no providers/adapters/MCP activated | No activation. | Preserved. | Stop. |
| IR06-G05 no API/network/auth calls occurred | No calls/auth. | Preserved. | Stop/security. |
| IR06-G06 credentials not inspected/used | Values not inspected/used. | Preserved. | Stop/security. |
| IR06-G07 source tracking remains blocked | IR-02 preserved. | Preserved. | Stop/governance. |
| IR06-G08 `3_platform` contents uninspected/unapproved | Existence metadata only. | Preserved. | Stop/classification. |
| IR06-G09 security/local-only posture preserved | S-series preserved. | Preserved. | Stop/security. |
| IR06-G10 CSS substrate remains undecided | No substrate selected. | Preserved. | Stop/CSS. |
| IR06-G11 IR-07 next scope declared | Next gate only. | Ready after instruction. | Do not start. |

## 32. Residual Risk Register
| risk_id | residual risk | source | severity | mitigation | route | blocks implementation? |
| --- | --- | --- | --- | --- | --- | --- |
| R-01 | No provider activation model implemented. | IR-06 | High | Provider gate. | IR-08/I00. | Yes |
| R-02 | No adapter implementation. | M-04 | High | Adapter gate. | I00 later. | Yes |
| R-03 | No MCP permission model. | H/S | High | MCP gate. | IR-08/I00. | Yes |
| R-04 | No credential storage/revocation model. | S-03 | High | Security design. | IR-08. | Yes |
| R-05 | No network policy implementation. | S-04 | High | Policy runtime. | IR-08. | Yes |
| R-06 | No provider sandbox. | S/H | High | Sandbox review. | IR-08/I00. | Yes |
| R-07 | No audit logging runtime. | V/S/H | Medium | Audit gate. | IR-08. | Yes |
| R-08 | No cost/quota model. | Provider risk | Medium | Owner/limits. | Provider gate. | Yes |
| R-09 | No terms/privacy review process. | Legal/security | High | Review process. | Governance. | Yes |
| R-10 | No validation registry. | V-series | High | IR-08. | IR-08. | Yes |
| R-11 | No security enforcement. | S-series | High | IR-08. | IR-08. | Yes |
| R-12 | Dependencies unadopted. | IR-04 | High | IR-04 gates. | Future governance. | Yes |
| R-13 | Source tracking blocked. | IR-02 | High | Tracking gate. | IR-A/I00. | Yes |
| R-14 | Existing `3_platform` contents unknown. | IR-01/IR-02 | High | Classification. | Future gate. | Yes |
| R-15 | CSS substrate undecided. | CSS | Medium | IR-07. | IR-07. | Yes |
| R-16 | Product integrations inactive. | P-series | High | Product governance. | Product route. | Yes |

## 33. Blocker Register
| blocker | stop behavior | required future action | blocks IR-06? | blocks implementation? |
| --- | --- | --- | --- | --- |
| missing IR-05 | Stop. | Complete IR-05. | Yes | Yes |
| missing H/S/V controls | Stop. | Restore controls. | Yes | Yes |
| need to activate provider | Stop. | Provider gate. | No | Yes |
| need to create adapter | Stop. | Adapter gate. | No | Yes |
| need to activate MCP | Stop. | MCP gate. | No | Yes |
| need to call API/network | Stop. | API/network gate. | No | Yes |
| need to authenticate | Stop. | Auth gate. | No | Yes |
| need to inspect credentials | Stop. | Secure auth review. | No | Yes |
| need to execute tools | Stop. | Tool approval. | No | Yes |
| need to adopt dependency | Stop. | IR-04 gate. | No | Yes |
| need to inspect `3_platform` contents | Stop. | Classification scope. | No | Yes |
| source tracking implied | Stop. | IR-02 future gate. | No | Yes |
| product activation implied | Stop. | Product governance. | No | Yes |
| CSS substrate decision implied | Stop. | IR-07. | No | Yes |
| validation/security enforcement implied | Stop. | IR-08. | No | Yes |
| Git action implied | Stop. | Human Git approval. | No | Yes |
| IR-07 scope pressure detected | Stop. | Finish/report IR-06. | No | No |
| I-00 scope pressure detected | Stop. | Later explicit ticket. | No | Yes |

## 34. Incident Handling
Incidents include: provider activated; adapter created or activated; MCP server/tool/resource activated; API/network call made; auth flow started; credential inspected/used; provider config created; tool execution approved or run; dependency installed/adopted; source tracking approved; `3_platform` contents inspected; product source inspected/copied; validation/security enforcement implemented; final Cognitive Semantic System substrate selected; Git staging/commit/push attempted; IR-07 or I-00 started.

Response: STOP, report safe metadata only, do not continue adjacent work, and require human/security/governance decision.

## 35. IR-06 Invariants
| ID | Invariant |
| --- | --- |
| IR06-001 | Provider / adapter / MCP activation readiness is not activation. |
| IR06-002 | No provider is activated. |
| IR06-003 | No adapter is created or activated. |
| IR06-004 | No MCP server/tool/resource is activated. |
| IR06-005 | No API or network call is made. |
| IR06-006 | No authentication flow is started. |
| IR06-007 | No credentials are inspected or used. |
| IR06-008 | Tool execution is not approved. |
| IR06-009 | Source tracking is not approved. |
| IR06-010 | Existing `3_platform` contents remain uninspected and unapproved. |
| IR06-011 | Dependencies remain unadopted. |
| IR06-012 | Product source remains local-only. |
| IR06-013 | Product Git posture is not changed. |
| IR06-014 | Cognitive Semantic System substrate remains undecided. |
| IR06-015 | Graph remains a candidate only. |
| IR06-016 | Validation evaluates; governance decides. |
| IR06-017 | IR-06 stops before IR-07. |

## 36. Anti-patterns
Anti-patterns: readiness as activation; credential presence as permission; provider credentials as provider permission; MCP availability as MCP activation; API docs as call approval; network availability as network approval; adapter design as adapter activation; tool availability as permission; context inclusion as permission to transmit; provider need as dependency adoption; product integration as product activation; graph/provider/MCP as semantic truth; starting IR-07 inside IR-06; starting I-00 inside IR-06; `git add .`.

## 37. Readiness For IR-07
IR-07 - Cognitive Semantic System Substrate Decision Gate is ready after explicit instruction if IR-06 provider / adapter / MCP activation readiness exists; no providers, adapters, MCP, APIs, network, auth, or credentials were activated or used; dependencies remain unadopted; source tracking remains not approved; `3_platform` contents remain uninspected and unapproved; and no product activation, CSS substrate decision, publication, Git mutation, or implementation is implied.

IR-06 does not create IR-07.

## 38. Final Verdict
IR-06 assesses future provider, adapter, MCP, API, network, auth, credential, data exposure, logging, telemetry, cost, terms, and activation gates for AGENT PLATFORM / Siamese.

Providers were not activated. Adapters were not created or activated. MCP was not activated. API/network calls were not made. Authentication was not started. Credentials were not inspected or used. Tool execution was not approved. Source tracking was not approved. Dependencies were not adopted. Existing `3_platform` contents were not inspected or approved. Product source remains local-only. CSS substrate was not decided.

Blocked items remain: provider activation, adapter implementation/activation, MCP activation, API/network/auth use, credential use, tool execution, runtime bridge, dependency adoption, source tracking, validation/security enforcement, audit logging, provider sandbox, product integration, CSS substrate decision, and implementation. IR-07 is ready after explicit instruction only.
