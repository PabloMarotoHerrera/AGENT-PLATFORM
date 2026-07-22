# P15.U - Hermes 0.19.0, Desktop, Dashboard and Workspace Adoption Assessment

Status: P15.U adoption assessment amended and complete with constraints.

Final verdict: `hermes_0_19_workspace_adoption_assessment_ready_with_constraints`

## Authority

P15.U consumes the committed P15.U0 source lock in `0_architecture/governance/agent_platform_hermes_0_19_workspace_source_lock.md` and records one adoption decision for Hermes Agent 0.19.0, Hermes Desktop, Hermes Web Dashboard and Hermes Workspace 2.3.0.

P15.U creates only this governance record. It does not modify product code, manifests, lockfiles, tests, external source roots, Graphify output, runtime state, credentials, provider configuration, Docker state, WSL state, VPS infrastructure or Git history.

Forbidden actions preserved by this assessment:

- no dependency installation;
- no source execution;
- no Hermes Agent startup;
- no Hermes Desktop startup;
- no Hermes Web Dashboard startup;
- no Hermes Workspace startup;
- no Docker container startup;
- no OAuth flow;
- no credential read;
- no provider call;
- no inference;
- no Graphify generation, query, update or modification;
- no product, script, test, manifest, lockfile or register mutation;
- no staging, commit, push, stash, reset, clean or worktree command.

## Final Decision

selected_option: `Option 1 — Upgrade Current Product Only`.

Hermes_Agent_baseline: `0.19.0`.

baseline_strategy: `new editable baseline plus controlled forward-port`.

Selected adoption architecture: `controlled_hermes_agent_0_19_current_product_upgrade_with_desktop_and_workspace_reference`.

The current Pepper/Hermes product remains canonical. P13 product UI, P14 governed runtime-adapter boundaries and P15.0-P15.3 OpenAI Codex planning artifacts remain active constraints. Hermes Agent 0.19.0 should become the future editable baseline through a new controlled product baseline, then existing Pepper modifications should be forward-ported deliberately and audited through the modification register. This avoids trying to patch 0.19.0 into an old 0.18.2-derived tree file-by-file while also avoiding a wholesale upstream rebase that bypasses Pepper governance.

Hermes Desktop, Hermes Web Dashboard and Hermes Workspace 2.3.0 are not adopted as editable Pepper product sources by P15.U. They are architecture and UX references until separate tickets define exact governed adoption boundaries. Not adopted by P15.U does not mean permanently rejected.

Hermes_Desktop adopted: `false`; role: `future_human_local_client_candidate_after_backend_profile_packaging_update_plugin_and_credential_governance`.

Hermes_Workspace adopted: `false`; role: `future_adjacent_operations_surface_candidate_after_api_session_volume_secret_and_deployment_governance`.

Adoption roles:

| Surface | Adopted by P15.U | Role |
| --- | --- | --- |
| Hermes Agent 0.19.0 | `true` as future baseline, not as immediate code mutation | New editable baseline source for controlled forward-port and compatibility work |
| Hermes Web Dashboard | `false` | Reference for browser dashboard routes, gateway expectations and P13 UI reconciliation |
| Hermes Desktop | `false` | Candidate future human local client after backend, profile, packaging, update and credential boundaries are governed |
| Hermes Workspace 2.3.0 | `false` | Candidate adjacent operational surface and deployment reference, not primary Pepper shell |

UI target roles:

| Role | Decision |
| --- | --- |
| `local_UI` | Pepper P13 Web UI remains canonical now; Hermes Desktop for Windows is the preferred future local client when supported and governed |
| `future_remote_UI` | Pepper remote control-plane UI remains canonical; Workspace may become an optional adjacent operations surface behind a service boundary |
| Desktop/Workspace backend sharing | API sharing may be allowed only through a governed Hermes gateway with separate tokens/session stores; direct shared writable `HERMES_HOME`, credential stores, Workspace sessions, Docker volumes or source roots are disallowed until explicitly governed |

Immediate non-decisions:

- do not replace Pepper P13 UI with Hermes Web Dashboard;
- do not replace Pepper P13 UI with Hermes Desktop;
- do not replace Pepper P13 UI with Workspace 2.3.0;
- do not run the Workspace Compose stack as-is;
- do not resume P15.1A or P15.4 through this assessment.

## Locked Source Evidence

| Source root | Upstream identity | Tree SHA-256 | Files | Dirs | Bytes | Adoption posture |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `4_external/sources/hermes-agent` | NousResearch/hermes-agent `v2026.7.7.2`, version `0.18.2`, commit `9de9c25f620ff7f1ce0fd5457d596052d5159596` | `6038ff8d40235109dcf85ad8751b050700b31b9fcfb438915f437a91b3292849` | 6171 | 869 | 134815928 | Existing baseline reference |
| `4_external/sources/hermes-agent-v0.19.0` | NousResearch/hermes-agent `v2026.7.20`, version `0.19.0`, commit `3ef6bbd201263d354fd83ec55b3c306ded2eb72a` | `ca41c8c6c688f7a8e94c238cecb45cb60cbec6c37555ba5eeb92530674e39e07` | 6737 | 905 | 149140090 | Selected future Agent baseline source |
| `4_external/sources/hermes-workspace-v2.3.0` | outsourc-e/hermes-workspace `v2.3.0`, version `2.3.0`, commit `15fa9cd706f5c04e4db288fb958e21d10fc776da` | `f00b66d6e7dc5bef87602cb026bdf14e593314b9fd242e3e1af48c20704616b9` | 1057 | 142 | 100799318 | Reference-only candidate |

All three source roots remain local ignored immutable references under `.gitignore:14:4_external/sources/`. They are not tracked Git candidates and are not adopted as editable source roots by this record.

Hermes Desktop locked-source status: `desktop_present_in_locked_0_19_source`. Desktop is inside `4_external/sources/hermes-agent-v0.19.0/apps/desktop`; it is covered by the Hermes Agent 0.19.0 locked tree SHA and remains ignored, immutable and non-editable in P15.U.

## Current Pepper Baseline

| Area | Current posture | P15.U disposition |
| --- | --- | --- |
| Editable product | `2_products/hermes-agent` | Preserve unchanged in this ticket |
| Product tracked files | `6246` | Must remain unchanged |
| Modification register | `rows=128`, `cols=18`, `duplicate_ids=0`, `duplicate_paths=0`, `missing_fields=0`, `hash_mismatches=0` | Must remain unchanged |
| P13.R product UI | `hermes_product_ui_foundation_closed_experimental_with_constraints` | Retain as route, navigation and safe-settings authority |
| P14.R runtime adapter | `hermes_governed_runtime_adapter_closed_with_constraints` | Retain as runtime/process/env/readiness/rollback authority |
| P15.0 strategy | `openai-codex`, ChatGPT OAuth, `https://chatgpt.com/backend-api/codex`, `gpt-5.5` | Retain; reconcile with 0.19.0 Codex model catalog later |
| P15.1 credential boundary | `openai-codex.primary`, isolated Hermes auth-shaped store, no real host-store execution | Retain; compare to 0.19.0 auth deltas without reading credentials |
| P15.2 provider runtime profile | `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1`, endpoint pinned, overrides denied | Retain; update only through a future exact source candidate |
| P15.3 bounded worker profile | `worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1`, one request, no tools/MCP/streaming/retry/fallback | Retain; update bounded transport and error handling only through stubs |
| P15.1A | Paused | Remains paused |
| P15.4 | Paused | Remains paused |

## Hermes Agent 0.19.0 Evidence

Hermes Agent 0.19.0 is a material upstream runtime and provider update, not a cosmetic bump.

Relevant evidence:

- `4_external/sources/hermes-agent-v0.19.0/pyproject.toml:8-23` declares `name = "hermes-agent"`, `version = "0.19.0"`, Python `>=3.11,<3.14`, MIT license and `LICENSE` files.
- Bounded file inventory found `120` files only in 0.18.2, `686` files only in 0.19.0, `1201` changed files and `4850` unchanged files.
- `4_external/sources/hermes-agent-v0.19.0/hermes_cli/auth.py:86` defines `DEFAULT_CODEX_BASE_URL = "https://chatgpt.com/backend-api/codex"`.
- `4_external/sources/hermes-agent-v0.19.0/hermes_cli/auth.py:186-199` distinguishes `openai-codex` as `oauth_external` from `openai-api` as `api_key` at `https://api.openai.com/v1`.
- `4_external/sources/hermes-agent-v0.19.0/hermes_cli/auth.py:3312-3316` stores OpenAI Codex tokens in `~/.hermes/auth.json`, separate from `~/.codex/`, to avoid refresh-token rotation conflicts with Codex CLI or VS Code.
- `4_external/sources/hermes-agent-v0.19.0/hermes_cli/auth.py:3374-3416` avoids clobbering independent Codex accounts during credential-pool sync.
- `4_external/sources/hermes-agent-v0.19.0/hermes_cli/auth.py:3529-3569` distinguishes Codex token refresh quota errors from relogin-required credential failures.
- `4_external/sources/hermes-agent-v0.19.0/hermes_cli/auth.py:3662-3673` contains self-healing logic for cross-store refresh-token rotation when relogin is required.
- `4_external/sources/hermes-agent-v0.19.0/hermes_cli/codex_models.py:14-52` includes Codex GPT-5.6 Sol/Terra/Luna variants, pro variants, `gpt-5.5`, `gpt-5.4`, `gpt-5.3-codex` and Spark fallback handling.
- `4_external/sources/hermes-agent-v0.19.0/hermes_cli/codex_models.py:96-133` fetches visible models from `https://chatgpt.com/backend-api/codex/models?client_version=1.0.0` and preserves Codex-specific visibility semantics.
- `4_external/sources/hermes-agent-v0.19.0/agent/codex_responses_adapter.py:26-50` stamps Responses encrypted reasoning issuers to prevent replaying provider-sealed reasoning blobs against the wrong endpoint.
- `4_external/sources/hermes-agent-v0.19.0/agent/bounded_response.py:56-125` bounds streaming error-body reads by byte cap and hard wall-clock deadline.
- `4_external/sources/hermes-agent-v0.19.0/hermes_cli/commands.py` exposes `/subscription`, `/topup` and `/usage`; prior `/credits` and `/billing` surfaces are folded into `/topup` according to command comments.

Adoption impact: Agent 0.19.0 should become the compatibility baseline before P15.4 resumes. Its auth/runtime/model/transport deltas intersect P15.0-P15.3 directly and justify a new editable baseline plus controlled Pepper forward-port.

## Hermes Web Dashboard Evidence

Hermes Web Dashboard is the browser UI shipped in the Hermes Agent 0.19.0 source tree. It is separate from Hermes Desktop and separate from Hermes Workspace.

Relevant evidence:

- `4_external/sources/hermes-agent-v0.19.0/web/package.json:1-15` defines a private Vite/React web package with `dev`, `build`, `preview`, `typecheck`, `test` and `check` scripts.
- `4_external/sources/hermes-agent-v0.19.0/web/package.json:17-40` depends on `@hermes/shared`, `@nous-research/ui`, React 19, React Router 7, xterm, motion, QR code and dashboard UI libraries.
- `4_external/sources/hermes-agent-v0.19.0/web/src/App.tsx:133-153` defines built-in routes for sessions, files, analytics, models, logs, cron, skills, plugins, MCP, pairing, channels, webhooks, system, profiles, config, env and docs.
- `4_external/sources/hermes-agent-v0.19.0/web/src/App.tsx:163-200` defines navigation items for sessions, files, analytics, models, logs, cron, skills, plugins, MCP, channels, webhooks, pairing, profiles, config, keys, system and docs.
- `4_external/sources/hermes-agent-v0.19.0/hermes_cli/subcommands/dashboard.py:1-6` states `dashboard` is the browser web UI and `serve` is the same gateway headless for Desktop and remote clients.
- `4_external/sources/hermes-agent-v0.19.0/hermes_cli/main.py:12737-12756` calls `start_server(..., headless=_headless_backend)` for dashboard/serve.

Adoption impact: Web Dashboard has useful route and gateway evidence, but adopting it wholesale would bypass Pepper P13 product descriptors and safe-settings authority. It remains a comparison source for P13 route parity and dashboard aggregation.

## Hermes Desktop Evidence

Hermes Desktop is a first-class native shell inside the locked Hermes Agent 0.19.0 source tree.

Locked-source status:

| Field | Value |
| --- | --- |
| Source root | `4_external/sources/hermes-agent-v0.19.0/apps/desktop` |
| Lock coverage | Covered by Hermes Agent 0.19.0 tree SHA `ca41c8c6c688f7a8e94c238cecb45cb60cbec6c37555ba5eeb92530674e39e07` |
| Git posture | Ignored immutable source under `4_external/sources/`; no tracked product adoption |
| Package identity | `name: hermes`, `productName: Hermes`, `version: 0.17.0`, `private: true` |
| P15.U adoption | `false` for editable product source; `true` only as architecture and future client reference |

Architecture evidence:

- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/package.json:1-12` declares a native desktop shell for Hermes Agent with Electron main entry `dist/electron-main.mjs`.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/package.json:13-52` exposes dev, build, pack, platform distribution, desktop tests and check scripts.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/package.json:157-268` configures Electron Builder with app id `com.nousresearch.hermes`, protocol `hermes`, ASAR packaging, extra resources, macOS, Windows and Linux targets.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/package.json:201-218` configures macOS category, entitlements, hardened runtime and `dmg` plus `zip` targets.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/package.json:219-240` configures DMG installer layout.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/package.json:241-248` configures Windows `nsis` and `msi` targets.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/package.json:249-258` configures Linux `AppImage`, `deb` and `rpm` targets.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/README.md:88-117` describes the packaged app as Electron shell plus React chat surface, with Hermes Agent running as headless `hermes serve`; old runtimes may fall back to `dashboard --no-open` without embedding dashboard UI.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/AGENTS.md:11-25` defines Desktop as its own native chat surface, not the browser dashboard or TUI; Electron owns machine capabilities, renderer owns experience and backend owns agent work.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/AGENTS.md:27-46` scopes state ownership by authority and warns against cross-profile bleed.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/electron/connection-config.ts:1-19` defines remote gateway URL normalization, token authentication and OAuth WebSocket-ticket authentication.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/electron/connection-config.ts:75-149` builds WebSocket URLs for token and OAuth ticket modes and treats OAuth ticket mint failure as a real auth failure.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/src/contrib/runtime-loader.ts:1-28` loads runtime plugins from ESM code but explicitly says this is not a capability sandbox.

Update and packaging evidence:

- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/README.md:41-47` states the app checks for updates in the background and can also update through `hermes update`.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/README.md:77-87` documents platform installer builds: macOS DMG plus zip, Windows NSIS plus MSI and Linux AppImage plus deb plus rpm; signing/notarization happen only when credentials are present.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/electron/main.ts:2195-2205` reports Desktop self-update as unsupported when the resolved update root is not a Git checkout.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/electron/main.ts:2916-2940` runs `hermes update --yes` and then `hermes desktop --build-only` during source-install self-update.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/electron/main.ts:2953-3068` handles Linux GUI/backend skew and sandbox-blocked relaunch instead of claiming the GUI package was updated.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/electron/main.ts:3071-3137` handles macOS app bundle swap and relaunch through a detached script.
- `4_external/sources/hermes-agent-v0.19.0/apps/desktop/src/global.d.ts:323-353` models update outcomes including manual CLI update, backend-updated, GUI-skew, manual restart, sandbox-blocked and handoff states.

Adoption impact: Desktop is strategically attractive as the future human local client, especially on Windows against a WSL2 or remote Linux backend. It is not safe to adopt directly in P15.U because it has native process, filesystem, credential, update, plugin and profile authority that must be mapped into P14/P15 governance first.

## Hermes Workspace 2.3.0 Evidence

Workspace 2.3.0 is a substantial shell and deployment reference. It is not currently governance-compatible as a direct Pepper replacement.

Relevant evidence:

- `4_external/sources/hermes-workspace-v2.3.0/package.json:2-7` declares `hermes-workspace`, version `2.3.0`, MIT license and `private: true`.
- `4_external/sources/hermes-workspace-v2.3.0/package.json:10-28` exposes TanStack/Vite, managed companion, Electron and test/build scripts.
- `4_external/sources/hermes-workspace-v2.3.0/package.json:41-46` uses TanStack React Query, Router and Start; `package.json:61-62` uses React 19.
- `4_external/sources/hermes-workspace-v2.3.0/src/routes/__root.tsx:117-190` defines the TanStack root route and `WorkspaceShell` root composition.
- `4_external/sources/hermes-workspace-v2.3.0/src/routes/__root.tsx:360-393` wraps the app in `QueryClientProvider`, authentication/onboarding gates, global shortcuts, terminal shortcut listener, `WorkspaceShell`, search, usage and onboarding overlays.
- `4_external/sources/hermes-workspace-v2.3.0/src/components/workspace-shell.tsx:95-108` maps route paths to mobile tab order for dashboard, chat, files, terminal, jobs, swarm, memory, skills, MCP, profiles and settings.
- `4_external/sources/hermes-workspace-v2.3.0/src/components/workspace-shell.tsx:309-463` renders a persistent sidebar, terminal workspace, main route outlet, chat panel, mobile navigation and connection startup overlay.
- `4_external/sources/hermes-workspace-v2.3.0/src/server/gateway-capabilities.ts:1-17` probes Hermes gateway and dashboard services and persists runtime URL overrides.
- `4_external/sources/hermes-workspace-v2.3.0/src/server/gateway-capabilities.ts:65-76` resolves `HERMES_API_URL` and `HERMES_DASHBOARD_URL` with localhost defaults.
- `4_external/sources/hermes-workspace-v2.3.0/src/server/auth-middleware.ts:12-30` persists Workspace session tokens in `~/.hermes/workspace-sessions.json`.
- `4_external/sources/hermes-workspace-v2.3.0/src/server/auth-middleware.ts:140-158` resolves `HERMES_PASSWORD` with `CLAUDE_PASSWORD` fallback.
- `4_external/sources/hermes-workspace-v2.3.0/src/server/auth-middleware.ts:203-245` requires explicit `TRUST_PROXY` before honoring forwarded headers.
- `4_external/sources/hermes-workspace-v2.3.0/src/lib/tasks-api.ts:1-14` selects between `/api/hermes-tasks` and `/api/claude-tasks`, preferring the canonical Hermes task store when present.
- `4_external/sources/hermes-workspace-v2.3.0/docker-compose.yml:15-18` pulls mutable `nousresearch/hermes-agent:latest` and `ghcr.io/outsourc-e/hermes-workspace:latest` by default.
- `4_external/sources/hermes-workspace-v2.3.0/docker-compose.yml:47-67` passes provider keys and gateway auth variables from `.env` and documents the need for `API_SERVER_KEY` when gateway exposure changes.
- `4_external/sources/hermes-workspace-v2.3.0/docker-compose.yml:97-112` documents `HERMES_PASSWORD`, `COOKIE_SECURE`, `TRUST_PROXY` and binds Workspace to `127.0.0.1:3000`.
- `4_external/sources/hermes-workspace-v2.3.0/Dockerfile:13-23` builds on `node:22-slim`, enables Corepack, installs pnpm dependencies and builds the app.
- `4_external/sources/hermes-workspace-v2.3.0/Dockerfile:26-59` runs as non-root `workspace` UID `10010`, installs `python3` for terminal support, exposes port `3000`, defines a healthcheck and starts `server-entry.js`.

Adoption impact: Workspace can inform UX, route inventory, dashboard aggregation and deployment hardening. Direct adoption would bypass Pepper's existing product descriptors, product configuration, modification register, P13 safe settings, P14 containment and P15 credential/profile boundaries.

## Four-Surface Comparison

| Surface | Source | Primary value | Main authority problem | P15.U disposition |
| --- | --- | --- | --- | --- |
| Pepper P13 UI | `2_products/hermes-agent/web/src/agent-platform` | Current governed product shell with Runtime Overview, Projects/Tickets, Approval Inbox, Execution Inspector, Safe Settings and shell | Experimental but already governed by Pepper descriptors and register | Keep canonical |
| Hermes Web Dashboard | `4_external/sources/hermes-agent-v0.19.0/web` | Mature upstream browser dashboard routes for sessions, files, models, skills, MCP, profiles, config, logs and plugins | Wholesale adoption would bypass P13 route/config/safe-settings authority | Reference and reconcile route-by-route |
| Hermes Desktop | `4_external/sources/hermes-agent-v0.19.0/apps/desktop` | Native human client, local/remote backend modes, Electron process ownership, packaged installers and built-in update UX | Native machine/update/plugin/credential authority must be mapped to P14/P15 before use | Future local client candidate, not adopted now |
| Hermes Workspace 2.3.0 | `4_external/sources/hermes-workspace-v2.3.0` | Broad operational workspace, TanStack shell, mobile layout, tasks, terminal, jobs, swarm, memory and Compose deployment | Mutable images, `.env` secret posture, own auth/session store and broad shell authority conflict with Pepper governance | Adjacent operations reference, not adopted now |

Surface conclusion: Pepper P13 remains the product authority. Hermes Web Dashboard and Desktop are 0.19.0 upstream surfaces to mine for compatibility and UX. Workspace is an adjacent/ops reference, not a replacement shell.

## Option Taxonomy

The following taxonomy is the only option set considered by this amended assessment.

| Option | Label | Meaning | Score 0-5 | Decision |
| --- | --- | --- | ---: | --- |
| Option 1 | Upgrade Current Product Only | Create a new editable Hermes Agent 0.19.0 baseline, forward-port Pepper modifications, keep Pepper P13/P14/P15 governance, use Desktop/Web Dashboard/Workspace as references | 4.4 | Selected |
| Option 2 | Upgrade Hermes + Adopt Workspace UI | Upgrade to Agent 0.19.0 and replace Pepper P13 UI with Workspace as the main UI | 2.6 | Rejected because it bypasses P13 safe-settings/product authority and introduces Workspace auth/session/Compose risk |
| Option 3 | Workspace as Embedded/Adjacent Product | Keep Pepper but adopt Workspace as a governed adjacent operational product | 3.4 | Deferred because it may be useful later, but API/session/volume boundaries are not yet defined |
| Option 4 | Keep 0.18.2 Temporarily | Keep the existing 0.18.2-derived product and pause 0.19.0 adoption | 2.7 | Rejected because 0.19.0 contains material Codex/provider/runtime fixes relevant to P15 |
| Option 5 | Rebase Product Architecture | Rebase/rewrite Pepper around upstream Agent, Desktop, Dashboard and Workspace architecture | 2.2 | Rejected because it has the highest governance and rollback risk |

Selected exactly one: `Option 1 — Upgrade Current Product Only`.

Rationale: Option 1 captures the 0.19.0 provider/runtime value while preserving the product register, P13 route authority, P14 runtime adapter and P15 credential/provider/worker boundaries. It also keeps Desktop and Workspace available for future governed adoption without granting them immediate authority.

## Deployment Assessment

Read-only host observations on 2026-07-22:

| Check | Result |
| --- | --- |
| `where wsl` | `C:\Windows\System32\wsl.exe`; `C:\Users\pablo\AppData\Local\Microsoft\WindowsApps\wsl.exe` |
| `wsl --status` | Default distribution `Ubuntu`; default version `2` |
| `where docker` | Docker CLI present under `C:\Program Files\Docker\Docker\resources\bin` |
| `docker version` | Client `29.4.1`, context `desktop-linux`; daemon unavailable at `npipe:////./pipe/dockerDesktopLinuxEngine` |
| `docker compose version` | Docker Compose `v5.1.3` |

Deployment scoring uses scores from 0 to 5. Weighted total is also on a 0 to 5 scale.

| Criterion | Weight |
| --- | ---: |
| Hermes compatibility | 20 |
| Security and isolation | 20 |
| Reproducibility | 15 |
| Development ergonomics | 10 |
| 24/7 operability | 10 |
| Filesystem and credential semantics | 10 |
| Observability and recovery | 5 |
| Performance | 5 |
| Direct operating cost | 5 |

| Mode | Description | Hermes compatibility | Security and isolation | Reproducibility | Development ergonomics | 24/7 operability | Filesystem and credential semantics | Observability and recovery | Performance | Direct operating cost | Weighted total | Disposition |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| A | Windows Native | 2 | 3 | 2 | 4 | 1 | 2 | 2 | 3 | 5 | 2.50 | Source-editing and emergency inspection fallback only |
| B | WSL2 Native | 4 | 3 | 3 | 4 | 2 | 4 | 3 | 4 | 5 | 3.45 | Temporary validation fallback when Compose cannot be used |
| C | WSL2 plus Docker Compose | 4 | 4 | 4 | 3 | 3 | 3 | 3 | 4 | 4 | 3.65 | Selected strategic local development target |
| D | External Linux VPS plus Docker Compose | 5 | 4 | 4 | 2 | 5 | 4 | 4 | 4 | 2 | 4.00 | Future 24/7 target after deployment gates |

### Strategic Local Target

Human-selected strategic local target: `C - WSL2 plus Docker Compose`.

This target is strategically correct because it keeps repository state, runtime volumes, credentials and processes in Linux-native WSL filesystem semantics while preserving reproducibility and future deployment parity. Pepper P13 remains the initial UI; Hermes Desktop can become the future governed local client, and Workspace can become an optional adjacent operations surface after service boundaries are accepted.

### Current Host Readiness

Current host readiness is not the same as strategic architecture selection.

```yaml
current_host_readiness:
  WSL2: available
  Ubuntu: available
  Docker CLI: available
  Docker Compose: available
  Docker daemon: unavailable
  target_operational_now: false
```

The unavailable Docker daemon is host-readiness evidence only. It is not a strategic rejection of WSL2 plus Docker Compose.

### Required Enablement Steps

Before Mode C or D may run:

- approve execution explicitly in a future ticket;
- enable and verify Docker daemon access without mutating P15.U state;
- replace mutable `latest` image references with pinned digests or source-built immutable images;
- define `.env` and secret handling that does not leak provider credentials into unmanaged Workspace or Compose scope;
- define persistent volume ownership, backup and restore;
- define API auth, `API_SERVER_KEY`, `HERMES_PASSWORD`, `COOKIE_SECURE`, `TRUST_PROXY`, reverse proxy and TLS posture;
- define firewall, bind-address and tunnel rules;
- define healthchecks, logs, monitoring, alerting and recovery;
- define rollback, credential rotation and incident review.

### Deployment Targets

```yaml
local_development_target:
  mode: C
  UI:
    - Pepper P13 initially
    - Hermes Desktop as a future governed local-client candidate
    - Workspace as an optional future adjacent operations surface
  backend: Hermes Agent 0.19.0-derived Pepper baseline under WSL2 plus Docker Compose
  repository_location: Linux-native WSL filesystem
  runtime_volume_location: Linux-native WSL filesystem
  rationale: Linux compatibility, reproducibility, deployment parity and clean POSIX credential/process semantics

temporary_validation_fallback:
  mode: B - WSL2 Native
  role: source/runtime validation when Compose is unavailable or not yet hardened

windows_native_role:
  mode: A - Windows Native
  role: source-editing and emergency inspection fallback only

fallback_target:
  mode: B - WSL2 Native
  trigger_conditions:
    - Docker daemon unavailable
    - Compose hardening incomplete
    - image pinning incomplete
    - volume or secret boundary not accepted
  limitations:
    - no container-parity evidence
    - no Compose lifecycle validation
    - no production deployment equivalence

strategic_local_target:
  mode: C - WSL2 plus Docker Compose
  human_ui: Windows Hermes Desktop client when supported and governed
  backend: "Hermes Agent 0.19.0 editable baseline in WSL2; Compose only after daemon and hardening gates"
  workspace: "optional adjacent local operations surface after API/session/volume boundaries"

future_24_7_target:
  mode: "D - external Linux VPS plus Docker Compose"
  role: "remote Pepper control plane and long-running Hermes services"
  required_gates: "pinned artifacts, secrets, TLS/proxy, backups, monitoring, firewalling, rollback"

source_editing_and_emergency_inspection_fallback_only:
  mode: "A - Windows Native"
  runtime_limit: "no provider/OAuth/inference/container/runtime startup without a later gate"
```

## UI And Backend Combination Analysis

| # | UI/backend combination | Governance fit | Decision |
| ---: | --- | --- | --- |
| 1 | Pepper P13 UI plus current 0.18.2-derived Pepper backend | Highest current governance fit, but misses 0.19.0 provider/runtime fixes | Keep only as fallback/reference |
| 2 | Pepper P13 UI plus new Hermes Agent 0.19.0 editable baseline | Best fit for selected Option 1; preserves product authority while upgrading runtime source | Select as migration target |
| 3 | Hermes Web Dashboard plus Hermes Agent 0.19.0 backend | Upstream-compatible browser UI but bypasses P13 product descriptors and safe settings | Reference only |
| 4 | Hermes Desktop plus local managed Hermes Agent backend | Strong human local UX, but native update/plugins/profile/credential authority must be governed | Candidate after Desktop contract ticket |
| 5 | Hermes Desktop plus remote Pepper/Hermes backend | Good future local-client/remote-control split, but token/OAuth ticket, profile and state semantics need service boundaries | Candidate after remote client contract ticket |
| 6 | Workspace plus its Compose-managed Hermes Agent backend | Operationally attractive, but mutable images and `.env` secrets are not acceptable as-is | Reject as immediate deployment |
| 7 | Workspace as adjacent UI against governed Pepper/Hermes backend | Potentially useful operations surface if API-only, isolated sessions and no shared volumes | Defer to adjacent-product ticket |

Combination conclusion: combination 2 is the selected product migration path. Combinations 4, 5 and 7 are future UX/ops candidates. Combination 6 is not allowed as-is.

## Backend And State Sharing Contract

| Boundary | Allowed later | Disallowed until further governance |
| --- | --- | --- |
| Backend API | Desktop, Web Dashboard or Workspace may call a governed Hermes gateway after auth/version/profile compatibility is defined | Undocumented direct imports, direct process ownership by UI, or bypassing P14 runtime adapter |
| Filesystem state | Explicitly scoped project folders and read/write operations mediated by governed backend APIs | Shared writable source roots, shared unmanaged `HERMES_HOME`, shared Docker volumes or cross-profile bleed |
| Credentials | Separate token/session stores with explicit authority, expiration, revocation and audit | Reusing host credentials, reading real credential stores, OAuth execution or leaking provider keys into Workspace `.env` without a gate |
| Sessions | Backend-owned session truth cached by UI | UI-owned durable session truth that can conflict with Pepper/P14/P15 state |
| Updates | Future signed/pinned release pipeline with rollback | Desktop source self-update or Workspace mutable image update as a Pepper product update mechanism |
| Plugins | Local trusted code only after capability mapping | Treating Desktop runtime plugins as a sandbox or loading remote plugins through the current renderer pipeline |

Desktop and Workspace must therefore be separated by service boundaries. They may share a governed backend API later; they must not directly share mutable backend state, credentials or volumes now.

## P15 Dispositions

Allowed final disposition values are limited to the contractual value sets for each P15 item.

| Item | current_status | final_disposition | destination_ticket_or_workstream | reason |
| --- | --- | --- | --- | --- |
| `P15_0` | closed and active | `migrate` | `P15.M8 - P15 Provider and Credential Migration` | The selected `openai-codex`, ChatGPT OAuth endpoint `https://chatgpt.com/backend-api/codex` and `gpt-5.5` strategy remain valid, but the authoritative baseline moves to Hermes Agent 0.19.0. |
| `P15_1` | closed with compatibility follow-up | `migrate` | `P15.M8 - P15 Provider and Credential Migration` | Credential boundaries must be remapped onto the 0.19.0 auth store, token-pool and refresh behavior without reading credentials or running OAuth. |
| `P15_1A` | paused | `retain_for_windows_fallback` | `P15.M8 - P15 Provider and Credential Migration`; `P15.M11 - Tool-Free OAuth and Inference Revalidation` | The native Windows credential/OAuth pathway is not the strategic local target, but remains evidence for Windows Native source-editing and emergency inspection fallback. |
| `P15_2` | closed with compatibility follow-up | `migrate` | `P15.M8 - P15 Provider and Credential Migration` | Provider runtime profile authority must move to the 0.19.0-derived baseline while preserving endpoint pinning and override denial. |
| `P15_3` | closed with compatibility follow-up | `migrate` | `P15.M8 - P15 Provider and Credential Migration`; `P15.M15 - Pepper-Siamese Worker Integration` | Bounded worker constraints must move to the 0.19.0-derived baseline and later align with Siamese worker boundaries. |
| `P15_4` | paused | `replace` | `P15.M11 - Tool-Free OAuth and Inference Revalidation`; `P15.M12 - Pepper End-to-End Local Acceptance` | The old paused validation path is replaced by a new 0.19.0-derived, tool-free local OAuth/inference revalidation and complete local Pepper acceptance flow. |

Uncommitted P15.4 candidate disposition: `selectively_forward_port`.

The original dirty checkout remains untouched. The candidate is not approved or committable. Contract tests, security lessons, native-flow evidence and failure evidence may be mapped selectively. No source file is copied wholesale. Incompatible 0.18.2 assumptions are not carried forward.

## Pepper To Siamese Architecture

Accepted direction: Pepper should operate remotely as a control plane while selected Siamese work runs on local or specialized workers.

Answer: yes, Pepper should operate remotely as the control plane for policy, registry, UI authority, tickets, approvals, audit, provider profile selection and rollback, while Siamese workers execute selected work on local WSL2, specialized hardware, ephemeral containers or future VPS workers under narrow leases.

```yaml
Pepper control plane:
  placement: future Linux VPS
  owns:
    - tickets
    - approvals
    - registry
    - audit
    - coordination
    - Jobs and Tasks

Siamese source repository:
  canonical_source: canonical Git remote
  local_backend_common_code: Linux-native local working copy
  Omniverse_integration: specialized workstation working copy

EnergyPlus execution:
  local_development: WSL2/container worker during local development
  authorized_long_running_batches: remote Linux workers for long-running batches when authorized

Omniverse Kit execution:
  placement: GPU workstation
  VPS_assumption: not assumed to run on the general-purpose VPS

Artifact movement:
  required_controls:
    - explicit artifact manifests
    - checksums
    - bounded uploads/downloads
    - no unmanaged shared writable source volume

Worker authentication:
  required_controls:
    - short-lived worker identity or scoped token
    - no reuse of provider credential as worker identity

Human approval:
  boundary: retained by Pepper approval boundary
  rule: remote execution must not bypass Approval Inbox

Rollback:
  required_controls:
    - ticket-specific source rollback
    - worker termination
    - artifact quarantine
    - runtime/container rollback
    - credential rotation when exposure is suspected
```

Desktop fit: Hermes Desktop is the preferred future human local client for observing and controlling Pepper/Siamese workflows from Windows, but it must not own Pepper policy or directly mutate worker state outside governed APIs.

Workspace fit: Workspace may become an adjacent operational surface for observing fleets, terminals, jobs, memory and swarm-like views, but only if those views are API-mediated and do not become the source of authority.

Do not implement these mechanisms through P15.U. This assessment records placement and boundaries only.

## License And Redistribution Assessment

| Component | Evidence | Assessment | Constraint |
| --- | --- | --- | --- |
| Hermes Agent 0.19.0 | `pyproject.toml:21-23` declares Nous Research author, MIT license and `LICENSE` files | MIT source license is compatible with internal fork, modification and redistribution with notices | Provider APIs, ChatGPT OAuth, model access, hosted endpoints and credentials are separate contractual/operational concerns not granted by MIT |
| Hermes Desktop | Desktop README links MIT license, package is private, app id/product name are Hermes, installers target macOS/Windows/Linux | Desktop source appears under the Agent MIT source tree, but binary redistribution must preserve notices and third-party licenses | `Hermes` product name, icons, signing/notarization identities, installer distribution channels and Nous trademarks may require separate approval; package `private: true` means not intended for npm publishing |
| Hermes Workspace 2.3.0 | `package.json:2-7` declares MIT license and `private: true` | MIT source license is compatible with internal reference, modification and redistribution with notices | Container images, third-party dependencies, Electron builds, `private: true`, author attribution, marks and mutable image provenance need separate release review before distribution |

License conclusion: source-level internal review and controlled fork work are allowed by the observed MIT declarations, but P15.U does not authorize binary redistribution, public branding, hosted service exposure, provider account use, OAuth execution or container publication.

## Ticket-Level Roadmap

| Ticket | objective | scope | prerequisites | main deliverable | main prohibition | unlock condition |
| --- | --- | --- | --- | --- | --- | --- |
| `P15.M0 — Adoption Authorization` | Authorize Option 1 and the 0.19.0 baseline strategy | Governance approval for selected option, targets, P15 dispositions and source identities | Amended P15.U accepted by human | Adoption authorization record | No product, source, runtime, dependency, Docker, WSL, VPS, OAuth, provider or inference mutation | Human approval of this assessment |
| `P15.M1 — New Hermes 0.19 Product Baseline` | Create the new editable Hermes Agent 0.19.0-derived Pepper baseline | Product baseline creation, source identity carry-forward, inventory and register planning | P15.M0 | Controlled editable baseline with locked-source provenance | No source execution, dependency install or unregistered product mutation | Baseline inventory and register plan accepted |
| `P15.M2 — License and Notice Reconciliation` | Reconcile source, binary and notice obligations | Agent, Desktop, Web Dashboard, Workspace, third-party notices, package `private` flags, trademarks and redistribution limits | P15.M1 | License and notice matrix with redistribution constraints | No binary redistribution, public branding or container publication | License/notice record accepted |
| `P15.M3 — Dependency and Lock Reconciliation` | Reconcile Python, Node, Electron, Workspace and Compose dependency state | `pyproject`, Python locks, web/package manifests, Desktop manifests, Workspace manifests and image pinning plan | P15.M1 and P15.M2 | Dependency and lock migration plan | No install, build, lock regeneration or image pull without a later gate | Reproducible dependency plan accepted |
| `P15.M4 — Desktop and Workspace Productization Decision` | Decide Desktop and Workspace product roles after baseline creation | Desktop client, Web Dashboard, Workspace adjacent surface, service boundaries, packaging and update authority | P15.M1 through P15.M3 | Productization decision for Desktop, Dashboard and Workspace | No Desktop/Workspace build, start, install, update or Compose execution | Adopt/defer/reject roles accepted |
| `P15.M5 — Interaction Surface Baseline` | Establish the interaction surface baseline before migration | Pepper P13, Hermes Web Dashboard, Hermes Desktop and Workspace surface inventory, route ownership and safe-settings mapping | P15.M4 | Surface baseline and route authority map | No P13 route replacement or new UI authority | Surface map accepted |
| `P15.M6 — P13 Surface Migration` | Migrate or preserve Pepper P13 surfaces on the 0.19.0-derived baseline | Runtime Overview, Projects/Tickets, Approval Inbox, Execution Inspector, Safe Settings and shell descriptors | P15.M5 | P13 migration patch set and tests | No bypass of Pepper product descriptors or safe-settings authority | P13 parity and safety evidence accepted |
| `P15.M7 — P14 Runtime Migration` | Migrate the governed runtime adapter to the 0.19.0-derived baseline | Process/env/readiness/event/audit/rollback adapter, gateway compatibility and runtime containment | P15.M1 and P15.M6 | P14 runtime migration patch set and stub evidence | No runtime execution, WSL mutation or provider call | Runtime adapter evidence accepted |
| `P15.M8 — P15 Provider and Credential Migration` | Migrate P15 provider, credential and bounded worker contracts | P15_0, P15_1, P15_1A fallback evidence, P15_2 and P15_3 against 0.19.0 Codex auth/model/runtime changes | P15.M7 | Provider/credential/worker migration patch set with stub tests | No credential read, OAuth, live model-list, provider call or inference | P15 migration evidence accepted |
| `P15.M9 — WSL2 Development Architecture` | Define the local C-mode architecture without mutating WSL | Linux-native repository location, runtime volume location, path policy, credentials/process semantics and approval gates | P15.M8 | WSL2 development architecture record | No WSL mutation, runtime startup or Docker start | Architecture and command plan accepted |
| `P15.M10 — Docker Compose Local Pilot` | Pilot the selected C local target under controlled approval | WSL2 plus Docker Compose backend, pinned images/source builds, volumes, secrets, healthchecks and logs | P15.M9 | Local Compose pilot evidence | No Docker start before explicit pilot approval | Docker daemon readiness and hardening accepted |
| `P15.M11 — Tool-Free OAuth and Inference Revalidation` | Replace paused P15.4 with local 0.19.0-derived OAuth/inference revalidation | Tool-free single-request Codex OAuth/inference path, no tools, no MCP, no background workers, no fallback model | P15.M8 and approved local runtime gate | OAuth/inference revalidation evidence | No tools, MCP, streaming expansion, persistent workers or unapproved provider scope | Local OAuth/inference evidence accepted |
| `P15.M12 — Pepper End-to-End Local Acceptance` | Accept the complete local Pepper system | Pepper P13 UI, P14 runtime, P15 provider/credential/worker flow, C-mode local backend and fallback B behavior | P15.M10 and P15.M11 | End-to-end local acceptance report | No VPS deployment, production equivalence claim or unapproved Desktop/Workspace authority | Complete local acceptance accepted |
| `P15.M13 — VPS Security Baseline` | Define future D-mode VPS security without provisioning | Host hardening, firewall, TLS/proxy, secrets, backups, monitoring, logging, alerting and rollback design | P15.M12 | VPS security baseline design | No VPS provisioning, DNS changes, container startup or credential deployment | Security baseline accepted |
| `P15.M14 — VPS Deployment Pilot` | Run controlled D-mode deployment only after security acceptance | External Linux VPS plus Docker Compose pilot, pinned artifacts, secrets, volumes, proxy/TLS, monitoring and rollback | P15.M13 and explicit deployment approval | VPS pilot evidence and incident/rollback notes | No production cutover or unmanaged public exposure | VPS pilot evidence accepted |
| `P15.M15 — Pepper-Siamese Worker Integration` | Define and validate Pepper control-plane to Siamese worker boundaries | Worker identity, scoped tokens, EnergyPlus placement, Omniverse workstation placement, artifact manifests, checksums and approvals | P15.M12 and P15.M14 as applicable | Worker integration boundary and validation evidence | No provider credential reuse as worker identity and no unmanaged shared writable source volume | Worker boundary accepted |
| `P15.M16 — Rollback Rehearsal` | Rehearse rollback across source, runtime, container, worker and credential exposure scenarios | Ticket-specific source rollback, worker termination, artifact quarantine, runtime/container rollback and credential rotation criteria | P15.M15 | Rollback rehearsal report | No migration closure before rollback evidence is accepted | Rollback rehearsal accepted |
| `P15.MR — Migration Closure` | Close the migration after all required evidence is accepted | Final audit, register state, product inventory, deployment evidence, worker evidence, rollback evidence and residual-risk record | P15.M0 through P15.M16 accepted | Migration closure record | No new scope and no closure as merely a P15.4 restart gate | All required evidence accepted and human closure approved |

## Selected Architecture Contract

The selected architecture has these mandatory invariants:

- Pepper product remains the canonical editable product until P15.M1 creates the new 0.19.0 editable baseline.
- P13 product configuration remains the route and navigation authority.
- P14 runtime adapter remains the process, environment, readiness, event, audit and rollback authority.
- P15.1 remains the credential-store authority and continues to reject real credential reads or OAuth unless a future gate authorizes them.
- P15.2 remains the provider-runtime authority and continues to pin `https://chatgpt.com/backend-api/codex` with no caller, frontend, config, environment, proxy or aggregator endpoint authority.
- P15.3 remains the bounded worker authority and continues to reject tools, MCP, streaming, retry, fallback, persistent workers and background tasks.
- Hermes Agent 0.19.0 source is the selected future baseline source, not an immediate product mutation.
- Hermes Web Dashboard source is a route and UX comparison source until exact future candidate sets are approved.
- Hermes Desktop source is a future client reference until exact local/remote backend, update, plugin and credential boundaries are approved.
- Hermes Workspace 2.3.0 source is an adjacent operations and deployment reference until exact future candidate sets are approved.

## Rollback And Rejection Path

If this assessment is rejected before implementation, remove only this file. No product, source, runtime, credential, Docker, WSL, VPS, Graphify or Git state was intentionally changed by P15.U.

Future code migration rollback must be defined per ticket and must include exact changed paths, modification-register row changes, tests, product route/config restoration, credential-store preservation, runtime shutdown, source-root non-tracking verification and provider-call prohibition unless explicitly approved.

Future deployment rollback must include container stop/removal, volume backup or quarantine, credential rotation when exposed, DNS/proxy/TLS rollback, firewall closure, log retention policy and incident review.

## Final Validation

Read-only validation after amending this record produced these outcomes:

| Check | Result |
| --- | --- |
| Branch | `p15.u-hermes-adoption-assessment` |
| `HEAD` | `7b16d694844e895c8c118528675cbc0c656093df` |
| `origin/p15.u-hermes-adoption-assessment` | `7b16d694844e895c8c118528675cbc0c656093df` |
| `origin/main` | `fea7d3963a598b848768671e00d5bad8065a4421` |
| `origin/main` ancestor of `HEAD` | `true` |
| Tracked candidate count | `1` |
| Visible Git candidate count | `1` |
| Visible Git candidate set | Only `0_architecture/governance/agent_platform_hermes_0_19_workspace_adoption_assessment.md` |
| Unexpected task candidates | `0` |
| External source changes | `0` |
| Editable product changes | `0` |
| Register changes | `0` |
| Product tracked files | `6246` |
| Register rows | `128` |
| Register columns | `18` |
| Register hash mismatches | `0` |
| Register audit | `rows=128`, `cols=18`, `duplicate_ids=0`, `duplicate_paths=0`, `missing_fields=0`, `hash_mismatches=0` using LF-normalized content hashes |
| Tracked files under `4_external/sources` | `0` |
| Visible untracked files under `4_external/sources` | `0` |
| Source ignore evidence | `.gitignore:14:4_external/sources/` for all three source roots |
| Source root file/dir/byte counts | Match P15.U0 locked values for all three roots |
| Graphify files found | `0` |
| Graphify commands | `0` |
| Graphify modifications | `0` |
| Installs | `0` |
| Builds | `0` |
| Runtime executions | `0` |
| Docker starts | `0` |
| WSL mutations | `0` |
| VPS provisioning | `0` |
| OAuth/provider/inference | `0` |
| `git diff --check` | no whitespace errors |
| Assessment trailing whitespace | `0` lines |
| Git index | empty |
| Staged files | none |
| Commits | `0` |
| Pushes | `0` |
| Stashes, resets, cleans, worktree commands | `0` |

No install, build, source test, source execution, Hermes Agent startup, Hermes Desktop startup, Hermes Web Dashboard startup, Workspace startup, Docker container startup, OAuth, credential read, provider call, inference, Graphify command, staging, commit, push, stash, reset, clean or worktree command was run by this assessment.

## Final Boundaries

P15.U is an assessment and selection record only. It does not authorize implementation, source synchronization, dependency adoption, package installation, product execution, container startup, OAuth, credential reads, provider calls, inference, live runtime validation, VPS provisioning, Graphify refresh, staging, commit or push.

P15.1A remains paused. P15.4 remains paused. Live OAuth/provider/inference remains unauthorized.
