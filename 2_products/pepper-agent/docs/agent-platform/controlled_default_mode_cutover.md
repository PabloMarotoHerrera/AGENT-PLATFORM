# P18.8 Controlled Default-Mode Cutover

P18.8 moves Pepper's normal workflow-control surface from external chat and manual OpenCode transfer into the authenticated Pepper dashboard. The cutover is controlled: it exposes approval, execution, worker-handoff preparation and workflow-control state through product routes while preserving human Git authority.

P18.8 does not stage, commit or push Git changes. It does not run Docker, Graphify, G-Brain, Paperclip, providers, models, direct workers, validation commands, retry execution, rollback execution or production deployment. It also does not start P18.R.

## Parent Gate

P18.8 was applied only after the P18.7 commit/push gate was satisfied:

| Gate | Value |
| --- | --- |
| Branch | `p18-manual-to-hermes-workflow-migration` |
| Required HEAD | `661f1362a7d019c1629e73ad04e4a70e966e394c` |
| Required origin branch | `661f1362a7d019c1629e73ad04e4a70e966e394c` |
| Required subject | `P18.7 Add manual versus Hermes shadow run` |

P18.7 produced four cutover blockers:

| Gap | P18.7 Blocker | P18.8 Disposition |
| --- | --- | --- |
| `P18-8-GAP-001` | Approval UI/backend not operational. | Closed by authenticated approval list, detail and decision routes plus Approval Inbox approve/reject UI. |
| `P18-8-GAP-002` | Governed execution UI/backend not operational. | Closed by authenticated execution collection, detail and start-preparation routes plus Execution Inspector controlled handoff UI. |
| `P18-8-GAP-003` | Workflow control/context still depends on external chat. | Closed by the workflow-control API and Runtime Overview card showing default-mode state, next action and blockers. |
| `P18-8-GAP-004` | Manual OpenCode ticket/result transfer still required. | Closed for the normal product path by controlled worker handoff preparation over the accepted P15/P17 substrate. Dispatch remains explicit and governed; Git stays human-only. |

## Product Runtime Surface

P18.8 adds `hermes_cli/agent_platform/product_runtime.py` as a thin adapter over existing Hermes/Pepper runtime facts. It does not create a second approval engine, executor, review engine or Git authority path.

The adapter exposes:

| Surface | Source | Boundary |
| --- | --- | --- |
| Approval inbox | Hermes staged-write approval store. | Bounded summaries only; raw pending payloads are not returned. |
| Approval detail | One exact staged-write approval ID. | Evidence summaries only; approve/reject remain explicit human dashboard actions. |
| Approval decision | Existing `tools.write_approval` apply/discard path. | Approve invokes the existing memory/skill write-approval handler; reject discards only that pending record. |
| Execution collection | Hermes Kanban task-run rows. | Universal bounded collection across boards; raw logs, claim locks, PIDs, metadata and paths are withheld. |
| Execution detail | One exact board/task/run projection. | Source-local run facts plus workflow, validation, review and Git-handoff metadata. |
| Start preparation | Accepted P15/P17 worker substrate identifiers. | Builds a deterministic request digest and handoff identity with `dispatch_performed: false`. |
| Workflow control | P18.7 gap evidence plus P18.8 cutover state. | Shows controlled default mode and remaining human smoke gate. |

## Dashboard Routes

P18.8 adds these protected routes in `hermes_cli/web_server.py` under the existing dashboard authentication boundary:

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/api/agent-platform/approvals` | List bounded pending approvals. |
| `GET` | `/api/agent-platform/approvals/{approval_id}` | Load one exact approval detail. |
| `POST` | `/api/agent-platform/approvals/{approval_id}/decision` | Apply an explicit human approve/reject decision. |
| `GET` | `/api/agent-platform/executions` | List universal execution records, or qualified board/task records when `board` and `task` are passed together. |
| `GET` | `/api/agent-platform/executions/{execution_id}` | Load one exact board/task/run source record. |
| `POST` | `/api/agent-platform/executions/start` | Prepare a controlled worker handoff without dispatching or automating Git. |
| `GET` | `/api/agent-platform/workflow-control` | Return controlled default-mode state and remaining cutover blockers. |

Profile scoping is handled through the existing dashboard `_profile_scope` mechanism. Execution route qualifiers must be exact; process telemetry, logs, transient chat state and unqualified current-board fallbacks are not used.

## Frontend Cutover

The product UI now consumes the live product routes instead of placeholder unavailable sources:

| Surface | P18.8 Change |
| --- | --- |
| Approval Inbox | Loads from `/api/agent-platform/approvals`; detail pages can approve or reject through the product decision route. |
| Execution Inspector | Loads universal and exact execution records from `/api/agent-platform/executions`; exposes controlled handoff preparation. |
| Runtime Overview | Fetches `/api/agent-platform/workflow-control` alongside `/api/status` and renders Pepper Workflow Control state. |

The UI remains bounded to source summaries and control metadata. It does not display raw provider payloads, credentials, raw prompts, raw transcripts, executable payloads, source paths, claim locks, process IDs or Git commands.

## Pepper Chat Bridge

Follow-up inspection identified `P18-8-GAP-005`: the inherited `/chat` surface still launched the generic Hermes TUI/provider setup path instead of a Pepper Lead Agent conversation bound to the governed P18 authority model.

The P18.8 bridge keeps the existing PTY/TUI transport and session rendering, but scopes the dashboard-spawned chat child into Pepper mode:

| Bridge Piece | P18.8 Behavior |
| --- | --- |
| Dashboard PTY child | `_resolve_chat_argv()` injects an internal Pepper chat-mode marker only for dashboard `/chat`. |
| Gateway agent factory | Pepper mode brands the TUI as `Pepper Lead Agent`, appends stable Pepper lead-agent instructions and pins platform/source to `pepper-dashboard`. |
| Provider/runtime binding | Pepper mode resolves only `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1` through the governed `openai-codex.primary` credential store with model `gpt-5.5` and transport `codex_responses`. |
| Worker authority | The bridge names `worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1` as the governed handoff substrate without dispatching workers. |
| Tool authority | Pepper mode passes `enabled_toolsets=[]`, disables model fallback propagation and ignores session model/provider override parameters. |
| Setup UX | Pepper setup messaging points to `hermes agent-platform auth add openai-codex.primary` and does not present generic `/model`, `/setup`, `hermes setup` or `hermes auth add openai-codex` actions. |
| Sidebar UX | The dashboard Chat sidebar renders a read-only Pepper Lead Agent authority card instead of the generic model picker, reasoning picker or duplicate sidecar session. |

The bridge does not create a second chat state machine, approval engine, execution engine, provider registry, workflow store, retry path, rollback path or Git authority. It also does not add arbitrary shell/file tools to Pepper Chat. Pepper Chat does not use `HERMES_HOME/auth.json`, API-key provider fallbacks or generic provider setup for Codex readiness.

## Worker And Git Boundary

P18.8 accepts the P18.7 worker/runtime finding:

OpenCode is a manual development tool, not the accepted runtime worker for the cutover. P18.8 reuses the accepted P15/P17 substrate and does not introduce a new executor.

Accepted substrate identifiers surfaced by start preparation:

| Identifier |
| --- |
| `build_provider_worker_gate_request` |
| `run_controlled_worker_request` |
| `run_openai_codex_single_dispatch` |
| `prepare_single_agent_execution` |
| `execute_single_agent_tool_action` |
| `complete_single_agent_execution` |

Start preparation returns `dispatch_performed: false`. A later governed dispatch operation may consume the prepared handoff, but P18.8 does not call providers, models or direct workers in tests or documentation.

Human Git authority is preserved:

| Git Action | P18.8 Authority |
| --- | --- |
| `git add` | Human only. |
| `git commit` | Human only. |
| `git push` | Human only. |
| rollback Git mutation | Not performed by P18.8. |

## Workflow-Control Verdict

The workflow-control snapshot reports:

| Field | Value |
| --- | --- |
| `mode` | `controlled_default` |
| `default_mode_enabled` | `true` |
| `manual_chat_control_required` | `false` |
| `manual_opencode_ticket_copy_required` | `false` |
| `manual_opencode_result_copy_required` | `false` |
| `human_git_authority` | `preserved_manual_git_add_commit_push_only` |
| `automatic_git_add` | `false` |
| `automatic_git_commit` | `false` |
| `automatic_git_push` | `false` |

The Pepper Chat bridge closes the `/chat` authority gap and the required live human smoke evidence has been recorded.

The machine-verifiable P18.7 gaps are closed by code and tests. READY is backed by the human dashboard smoke token:

`HUMAN_P18_8_CUTOVER_SMOKE_PASS`

The canonical P18.8 final verdict is:

`hermes_0_19_pepper_controlled_default_mode_cutover_ready_with_operational_product_workflow_zero_manual_executor_copy_and_preserved_human_git_authority`

## Validation Evidence

Focused validation for the candidate used no providers, no Docker, no Graphify and no Git mutation.

| Command | Result |
| --- | --- |
| `bash scripts/run_tests.sh tests/hermes_cli/test_agent_platform_product_routes.py -q` | Blocked by missing local `.venv`/`venv` wrapper environment. |
| `python -m pytest tests/hermes_cli/test_agent_platform_product_routes.py -q` | `9 passed` |
| `npm test -- src/agent-platform/approval-inbox/approval-inbox.test.tsx src/agent-platform/execution-inspector/execution-inspector.test.tsx src/agent-platform/runtime-overview/runtime-overview.test.tsx` | `3 passed`, `62 passed` |
| `npm run typecheck` | Passed |
| `bash scripts/run_tests.sh tests/hermes_cli/test_web_server.py::TestPtyWebSocket::test_resolve_chat_argv_uses_dashboard_scroll_env tests/test_tui_gateway_server.py::test_pepper_lead_agent_resolve_skin_overrides_branding tests/test_tui_gateway_server.py::test_pepper_lead_agent_setup_status_uses_governed_codex tests/test_tui_gateway_server.py::test_pepper_lead_agent_make_agent_uses_governed_runtime tests/test_tui_gateway_server.py::test_pepper_lead_agent_session_create_ignores_model_params -q` | Blocked by missing local `.venv`/`venv` wrapper environment. |
| `python -c "import ast, pathlib; ..."` | Python AST parse passed for touched Python files. |
| `npm run test --workspace ui-tui -- src/__tests__/setupContent.test.ts` | `1 passed`, `2 passed`. |
| `npm run test --workspace web -- src/lib/chat-sidebar-session-params.test.ts` | `1 passed`, `1 passed`. |
| `npm run typecheck --workspace ui-tui` | Passed. |
| `npm run typecheck --workspace web` | Passed. |
| `npm run build --workspace ui-tui` | Passed. |
| `npm run build --workspace web` | Passed with existing Vite large-chunk warning only. |

## Residual Limitations

P18.8 is not P18.R closure. It does not certify production deployment, critical-ticket support, broad multi-agent automation, G-Brain, Paperclip, automatic Git, rollback execution, direct worker dispatch, provider/model invocation or final migration retirement.

There are no remaining P18.8 blockers after `HUMAN_P18_8_CUTOVER_SMOKE_PASS`. P18.R is ready for explicit human authorization, but this document does not begin P18.R.
