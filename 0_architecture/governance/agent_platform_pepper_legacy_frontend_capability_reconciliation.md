# P15.C3A - Pepper Legacy Frontend Capability Reconciliation

Status: P15.C3A committed, pushed and fully validated.

Final verdict: `hermes_0_19_pepper_legacy_frontend_capabilities_reconciled_with_disabled_activation`

## Authority

P15.C3A forward-ports the accepted P13 frontend presentation surfaces from the retained Hermes legacy product into canonical Pepper frontend source only. The committed Pepper product configuration remains disabled: `agent_platform.product_ui` is disabled and `extension_modules` is empty, so the compiled descriptors resolve zero routes and zero navigation entries.

No backend, gateway, plugin, cron, provider, OAuth, worker, package, lockfile, Docker, Graphify, staging, commit or push action was performed by the agent for this candidate. Frontend dependency installation occurred only in a temporary external validation workspace and left no repository dependency or build residue.

## Source And Product Context

| Field | Value |
| --- | --- |
| Canonical product | `2_products/pepper-agent` |
| Pepper upstream version | `Hermes Agent 0.19.0` |
| Pepper upstream commit | `3ef6bbd201263d354fd83ec55b3c306ded2eb72a` |
| Retained semantic source | `2_products/hermes-agent/web/src/agent-platform` |
| Retained source upstream version | `Hermes Agent 0.18.2` |
| Activation state | Product UI disabled, no selected extension modules |

## Forward-Ported Surfaces

| Surface | Destination | Runtime posture |
| --- | --- | --- |
| Runtime Overview | `web/src/agent-platform/runtime-overview/` | Read-only `/api/status` projection through bounded parser |
| Projects and Tickets | `web/src/agent-platform/projects-tickets/` | Read-only Hermes Kanban board/task projection with exact identity validation |
| Approval Inbox | `web/src/agent-platform/approval-inbox/` | Deliberately unavailable production HTTP source; no approval or rejection action |
| Execution Inspector | `web/src/agent-platform/execution-inspector/` | Board/task-qualified Kanban run evidence only; no execution controls |
| Safe Settings | `web/src/agent-platform/safe-settings/` | Strict read-only product, feature, extension and display preference projection |
| Extension registry | `web/src/agent-platform/extensions.ts` | Compiles accepted descriptors but resolves none from committed disabled config |

## Accepted Descriptor Set

| Descriptor | Descriptor ID | Route Pattern | Navigation |
| --- | --- | --- | --- |
| Runtime Overview | `agent_platform.ui.overview` | `/agent-platform/overview` | `Overview` |
| Projects | `agent_platform.ui.projects` | `/agent-platform/projects` | `Projects` |
| Project Detail | `agent_platform.ui.project_detail` | `/agent-platform/projects/:boardSlug` | none |
| Ticket Detail | `agent_platform.ui.ticket_detail` | `/agent-platform/projects/:boardSlug/tickets/:taskId` | none |
| Approval Inbox | `agent_platform.ui.approvals` | `/agent-platform/approvals` | `Approvals` |
| Approval Detail | `agent_platform.ui.approval_detail` | `/agent-platform/approvals/:approvalId` | none |
| Execution Inspector | `agent_platform.ui.executions` | `/agent-platform/executions` | `Executions` |
| Execution Detail | `agent_platform.ui.execution_detail` | `/agent-platform/executions/:executionId` | none |
| Safe Settings | `agent_platform.ui.settings` | `/agent-platform/settings` | `Settings` |

Committed activation posture:

| Field | Value |
| --- | ---: |
| Compiled descriptors | 9 |
| Selected modules | 0 |
| Resolved descriptors | 0 |
| Runtime routes | 0 |
| Navigation items | 0 |
| Product UI | disabled |
| Extension modules | `[]` |

## Boundary Decisions

| Area | Decision |
| --- | --- |
| Product activation | Product UI remains disabled and routes/navigation stay inert. |
| Dynamic plugins | `/agent-platform/*` remains protected from plugin manifest claims. |
| Approval Inbox | No dashboard endpoint was invented and no fallback to Kanban, chat, logs, providers, workers, OAuth or transient prompts was added. |
| Safe Settings | Pepper exposes trusted settings facts as read-only catalog facts; no setting write authority remains in the P15.C3A surface. |
| Execution Inspector | Only exact Kanban board/task/run source evidence is projected; API-server runs, cron sessions, logs, PIDs and process telemetry are not fallback sources. |
| Projects and Tickets | Kanban data is labeled provisional and does not become canonical Project, Ticket, WorkPacket, ApprovalRequest or governed execution authority. |

## Read-Only And Security Boundary

| Boundary | Result |
| --- | --- |
| HTTP GET sources | `/api/status`, `/api/plugins/kanban` |
| HTTP POST | 0 |
| HTTP PUT | 0 |
| HTTP PATCH | 0 |
| HTTP DELETE | 0 |
| Settings writes | 0 |
| Approval actions | 0 |
| Execution actions | 0 |
| Provider actions | 0 |
| OAuth actions | 0 |
| Credential actions | 0 |
| Worker actions | 0 |
| Tool actions | 0 |
| MCP actions | 0 |
| Sensitive values rendered | 0 |
| Raw source objects retained | false |
| Raw errors retained | false |

## Control Records

| File | Accepted evidence |
| --- | --- |
| `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` | `150` total rows; `40` P15.C3A attribution rows; `38` new P15.C3A IDs; `2` updated existing rows; `0` duplicate IDs; `0` duplicate paths; `0` hash mismatches. |
| `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | `6804` total rows; `40` P15.C3A attribution rows; classification `AGENT_PLATFORM_product_addition`; included in upstream payload `false`; `0` duplicate destinations; `0` hash mismatches. |

## Frontend Validation

Temporary validation workspace:

| Field | Result |
| --- | --- |
| Location | outside repository |
| Removed after validation | true |
| Runtime residue | 0 |

Dependency installation:

| Field | Result |
| --- | --- |
| Command | `npm ci --no-audit --no-fund` |
| Location | temporary workspace only |
| Repository `node_modules` created | false |
| Repository package manifest modified | false |
| Repository lockfile modified | false |

Focused tests:

| Field | Result |
| --- | ---: |
| Files | 6 |
| Passed | 105 |
| Failed | 0 |
| Errors | 0 |
| Unexpected skips | 0 |

Focused test files:

| Test file |
| --- |
| `src/agent-platform/extensions.test.ts` |
| `src/agent-platform/runtime-overview/runtime-overview.test.tsx` |
| `src/agent-platform/projects-tickets/projects-tickets.test.tsx` |
| `src/agent-platform/approval-inbox/approval-inbox.test.tsx` |
| `src/agent-platform/execution-inspector/execution-inspector.test.tsx` |
| `src/agent-platform/safe-settings/safe-settings.test.tsx` |

Complete frontend suite:

| Field | Result |
| --- | ---: |
| Files | 26 |
| Passed | 230 |
| Failed | 0 |
| Errors | 0 |
| Unexpected skips | 0 |

TypeScript:

| Field | Result |
| --- | --- |
| Result | passed |
| Errors | 0 |

ESLint:

| Field | Result |
| --- | ---: |
| Errors | 0 |
| Candidate warnings | 0 |
| Introduced warnings | 0 |
| Inherited noncandidate warnings | 24 |

Production build:

| Field | Result |
| --- | --- |
| Result | passed |
| Modules transformed | 553 |
| Large chunk warning | inherited |
| Repository build output modified | false |
| Retained product references in temporary bundle | 0 |

The existing `hermes_cli/agent_platform/product_config.py` file was copied only into the temporary validation workspace to satisfy an existing design-system test. The repository copy was not modified.

## Pepper Integrity

| Identity | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate | 6831 | 149941138 | `2735cb45f0e087cc9dd2901ae5c1140e89ddcee886d526b0d2fbf253a13d9e50` |
| Payload | 6681 | 145409792 | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | not applicable | 38693 | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

This documentation-only authority correction must not change Pepper identity.

## Runtime And Governance Non-Actions

| Action | Count |
| --- | ---: |
| Repository dependency installs | 0 |
| Temporary external `npm ci` | 1 |
| Temporary workspace removed | true |
| Graphify actions | 0 |
| Provider calls | 0 |
| OAuth flows | 0 |
| Worker starts | 0 |
| Docker actions | 0 |
| Git staging by agent | 0 |
| Git commits by agent | 0 |
| Git pushes by agent | 0 |

## P15.C3B Handoff

| Field | Value |
| --- | --- |
| P15.C3A implementation committed | true |
| P15.C3A validation complete | true |
| P15.C3A canonical authority corrected | true |
| P15.C3B | may begin after this correction is reviewed, committed and pushed |
| Legacy product | retained |
| P16 | blocked until P15.CR |
| Production readiness | not claimed |
