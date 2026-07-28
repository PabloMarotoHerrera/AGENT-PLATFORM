# P15.C3A - Pepper Legacy Frontend Capability Reconciliation

Status: P15.C3A candidate prepared for human review.

Final verdict: `pepper_legacy_frontend_capability_reconciled_product_ui_inert`

## Authority

P15.C3A forward-ports the accepted P13 frontend presentation surfaces from the legacy Hermes product into canonical Pepper frontend source only. The committed Pepper product configuration remains disabled: `agent_platform.product_ui` is disabled and `extension_modules` remains empty, so the compiled descriptors resolve zero routes and zero navigation entries.

No backend, gateway, plugin, cron, provider, OAuth, worker, package, lockfile, Docker, Graphify, staging, commit or push action is part of this candidate.

## Source And Product Context

| Field | Value |
| --- | --- |
| Canonical product | `2_products/pepper-agent` |
| Pepper upstream version | `Hermes Agent 0.19.0` |
| Pepper upstream commit | `3ef6bbd201263d354fd83ec55b3c306ded2eb72a` |
| Legacy semantic source | `2_products/hermes-agent/web/src/agent-platform` |
| Legacy upstream version | `Hermes Agent 0.18.2` |
| Activation state | Product UI disabled, no selected extension modules |

## Forward-Ported Surfaces

| Surface | Destination | Runtime posture |
| --- | --- | --- |
| Runtime Overview | `web/src/agent-platform/runtime-overview/` | Read-only `/api/status` projection through bounded parser |
| Projects and Tickets | `web/src/agent-platform/projects-tickets/` | Read-only Hermes Kanban board/task projection with exact identity validation |
| Approval Inbox | `web/src/agent-platform/approval-inbox/` | Deliberately unavailable production HTTP source; no approval/rejection action |
| Execution Inspector | `web/src/agent-platform/execution-inspector/` | Board/task-qualified Kanban run evidence only; no execution controls |
| Safe Settings | `web/src/agent-platform/safe-settings/` | Strict read-only product, feature, extension and display preference projection |
| Extension registry | `web/src/agent-platform/extensions.ts` | Compiles accepted descriptors but resolves none from committed disabled config |

## Accepted Descriptor Set

| Descriptor ID | Route Pattern | Navigation |
| --- | --- | --- |
| `agent_platform.ui.overview` | `/agent-platform/overview` | `Overview` |
| `agent_platform.ui.projects` | `/agent-platform/projects` | `Projects` |
| `agent_platform.ui.project_detail` | `/agent-platform/projects/:boardSlug` | none |
| `agent_platform.ui.ticket_detail` | `/agent-platform/projects/:boardSlug/tickets/:taskId` | none |
| `agent_platform.ui.approvals` | `/agent-platform/approvals` | `Approvals` |
| `agent_platform.ui.approval_detail` | `/agent-platform/approvals/:approvalId` | none |
| `agent_platform.ui.executions` | `/agent-platform/executions` | `Executions` |
| `agent_platform.ui.execution_detail` | `/agent-platform/executions/:executionId` | none |
| `agent_platform.ui.settings` | `/agent-platform/settings` | `Settings` |

Expected committed posture remains:

| Field | Value |
| --- | ---: |
| Compiled descriptors | 9 |
| Selected modules | 0 |
| Resolved descriptors | 0 |
| Registered routes | 0 |
| Registered navigation entries | 0 |

## Boundary Decisions

| Area | Decision |
| --- | --- |
| Product activation | Product UI remains disabled and routes/navigation stay inert. |
| Dynamic plugins | `/agent-platform/*` remains protected from plugin manifest claims. |
| Approval Inbox | No dashboard endpoint was invented and no fallback to Kanban, chat, logs, providers, workers, OAuth or transient prompts was added. |
| Safe Settings | Legacy write paths were removed for Pepper; theme, font and locale are displayed as trusted read-only catalog facts. |
| Execution Inspector | Only exact Kanban board/task/run source evidence is projected; API-server runs, cron sessions, logs, PIDs and process telemetry are not fallback sources. |
| Projects and Tickets | Kanban data is labeled provisional and does not become canonical Project, Ticket, WorkPacket, ApprovalRequest or governed execution authority. |

## Control Records

| File | Change |
| --- | --- |
| `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` | Updated `P15.M6-018` and `P15.M6-019`; added `P15.C3A-001` through `P15.C3A-038`. |
| `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | Added 40 legacy-source attribution rows for registry, tests and forwarded module files. |

## Verification

| Check | Result |
| --- | --- |
| `Test-Path -LiteralPath "node_modules"` in `2_products/pepper-agent/web` | `False` |
| `npm run typecheck` in `2_products/pepper-agent/web` | Blocked: `tsc` is not available because local dependencies are absent |
| Targeted `npx vitest run ...` | Blocked: cannot resolve `vitest/config`, `@vitejs/plugin-react` or package `vitest` |
| Modification register validation | `150` rows, `38` new P15.C3A rows, `0` bad column counts, `0` duplicate IDs, `0` duplicate paths, `0` hash mismatches |
| Import manifest validation | `6804` rows, `40` P15.C3A source attribution rows, `0` bad column counts, `0` source/destination hash mismatches |
| LF canonical text check | `43` touched files checked, `0` files with CR bytes |
| `git diff --check` | clean |
| Safe Settings write/storage/reload grep | clean for forwarded Safe Settings module |
| Approval/Execution source-text test grep | clean for forwarded Approval Inbox and Execution Inspector modules |
| P13.5/P13.6/P13.7/P13.R user-facing copy grep | clean in forwarded Pepper frontend modules |

Blocked frontend verification is classified as dependency absence, not a product behavior failure. No install was performed because dependency installation was outside P15.C3A authority.

## Runtime And Governance Non-Actions

| Action | Count |
| --- | ---: |
| Backend changes | 0 |
| Provider calls | 0 |
| OAuth flows | 0 |
| Worker starts | 0 |
| Docker actions | 0 |
| Dependency installs | 0 |
| Graphify actions | 0 |
| Git staging by agent | 0 |
| Git commits by agent | 0 |
| Git pushes by agent | 0 |

## Human Review Notes

Human review should focus on whether compiling these descriptors while committed configuration remains disabled is acceptable for P15.C3A, and whether the dependency-blocked frontend checks should be rerun after restoring `web/node_modules` through the normal project dependency workflow.
