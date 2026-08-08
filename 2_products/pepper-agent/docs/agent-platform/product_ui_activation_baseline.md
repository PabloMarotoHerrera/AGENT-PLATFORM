# Pepper Product UI Activation Baseline

P18.UI-A activates the already-ported Pepper product UI descriptors that were
kept inert during the Hermes 0.19 migration. The activation happens inside the
existing Pepper web application by changing the tracked product configuration;
it does not introduce a second shell, router, extension system, Projects
backend, Tickets backend, or Kanban store.

## Prior State

P15.M6 and P15.C3A intentionally compiled the accepted P13 frontend descriptors
while keeping runtime activation fail-closed. The tracked product configuration
served `agent_platform.product_ui` as `disabled` and selected no
`extension_modules`, so `web/src/agent-platform/extensions.ts` resolved no
product routes or navigation entries.

That inert state was correct for the Hermes 0.19 migration because Pepper needed
the descriptors available for review without exposing product routes before a
governed activation milestone.

## P18 Activation

P18.UI-A changes the product UI feature state to `enabled` because these
descriptors are now part of the current Pepper activation baseline. The earlier
P13 experimental posture is superseded by this P18 product milestone; no P18
contract requires the feature to remain experimental.

The activated extension modules are exactly:

| Descriptor ID | Route | Navigation | Source |
| --- | --- | --- | --- |
| `agent_platform.ui.overview` | `/agent-platform/overview` | Overview | `/api/status` |
| `agent_platform.ui.projects` | `/agent-platform/projects` | Projects | `/api/plugins/kanban/boards` |
| `agent_platform.ui.project_detail` | `/agent-platform/projects/:boardSlug` | none | `/api/plugins/kanban/board` |
| `agent_platform.ui.ticket_detail` | `/agent-platform/projects/:boardSlug/tickets/:taskId` | none | `/api/plugins/kanban/tasks/{taskId}` |
| `agent_platform.ui.approvals` | `/agent-platform/approvals` | Approvals | unavailable read-only projection until P18.3 |
| `agent_platform.ui.approval_detail` | `/agent-platform/approvals/:approvalId` | none | unavailable read-only projection until P18.3 |
| `agent_platform.ui.executions` | `/agent-platform/executions` | Executions | task-qualified Kanban run projection |
| `agent_platform.ui.execution_detail` | `/agent-platform/executions/:executionId` | none | task-qualified Kanban run projection |
| `agent_platform.ui.settings` | `/agent-platform/settings` | Settings | validated product configuration and safe local catalogs |

The frontend resolver still enforces all gates. A descriptor resolves only when
its ID appears in `extension_modules` and its `featureId` resolves to `enabled`,
or to `experimental` for descriptors that explicitly allow experimental
visibility. Unknown IDs remain inert. Duplicate descriptor IDs and route
collisions still fail closed.

## Projects And Tickets

Projects and Tickets reuse the existing Kanban dashboard plugin API. The
Projects list reads `/api/plugins/kanban/boards?include_archived=false`, project
detail reads `/api/plugins/kanban/board?board=<slug>&include_archived=false`, and
ticket detail reads `/api/plugins/kanban/tasks/<taskId>?board=<slug>`. The UI
uses board-qualified and task-qualified routes to avoid falling back to a
process-current board.

Tickets remain nested under Projects by existing design. There is no separate
Tickets sidebar item in P18.UI-A.

Kanban is reused as an operational source only. Kanban SQLite is not the
irreversible long-term Pepper work-control authority; P20 Paperclip remains the
future durable work-control boundary.

## Boundaries

Pepper remains a Hermes-derived customized product, not an external wrapper and
not a parallel runtime. Inherited Hermes dashboard surfaces such as Chat,
Sessions, Files, Models, Skills, Plugins, MCP, Config, Keys, and System remain
Pepper capabilities.

Activating product UI does not make upstream setup Pepper authority. Generic
Hermes `auth.json`, provider setup, the dashboard model picker, model inference,
provider dispatch, credentials, G-Brain memory, and Paperclip calls remain
outside P18.UI-A.

G-Brain is not available in this ticket and receives no calls. Paperclip is not
available in this ticket and receives no calls. WorkPacket execution, Ticket
Factory runtime integration, approval workflow integration, and production
cutover remain deferred to later P18/P20 work.

## Build Posture

The frontend build command is owned by `web/package.json` and is `npm run build`
from `2_products/pepper-agent/web`. The build emits ignored local output under
`hermes_cli/web_dist`; that directory remains a runtime artifact and is not a
Git candidate. Dependency installation and lockfile regeneration are outside
this ticket.

## P18.2 Handoff

P18.2 may resume only after P18.UI-A is reviewed, committed, pushed, and the
post-commit Pepper integrity values are recorded as the new P18 authority.

Final verdict: hermes_0_19_pepper_product_ui_activation_baseline_ready_with_approved_projects_ticket_surfaces_and_existing_kanban_runtime_reuse
