# P15.M4 - Hermes Desktop and Workspace Productization Decision

Status: P15.M4 Desktop and Workspace productization decision ready with constraints.

Final verdict: `hermes_0_19_desktop_workspace_productization_decision_ready_with_constraints`

## Ticket Authority

P15.M4 statically decides whether Hermes Desktop or Hermes Workspace 2.3.0 enter Pepper as governed product surface, local client or adjacent service during the Hermes 0.19.0 migration.

P15.M4 creates exactly these tracked candidates:

| Path | Disposition |
| --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_desktop_workspace_productization_decision.md` | created governance decision record |
| `0_architecture/governance/agent_platform_hermes_0_19_desktop_workspace_manifest.tsv` | created machine-readable static surface manifest |

No product code, source root, dependency declaration, lockfile, package manifest, script, test, Graphify artifact, `.gitattributes` file or `.gitignore` file is modified by P15.M4.

Forbidden actions preserved by P15.M4:

- no Desktop installation, startup, packaging, build or test;
- no Workspace installation, startup, Compose run, Docker build or test;
- no Pepper, Desktop or Workspace module import or execution;
- no dependency installation, registry query or lock regeneration;
- no OAuth flow, credential read, provider call or inference;
- no runtime process, WSL, Docker, Compose, VPS or Graphify mutation;
- no route authority transfer, Workspace shell replacement or Desktop enablement;
- no shared writable `HERMES_HOME`, Workspace session store, credential store, Docker volume or source-root promotion;
- no staging, commit, push, stash, reset, clean or worktree mutation.

## Parallel-Lane Boundary

Work was performed only in `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M4` on branch `p15.m4-desktop-workspace-decision`.

P15.M2A, P15.M3 and other worktrees were not modified.

## Dynamic Start State

| Field | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M4` |
| Branch | `p15.m4-desktop-workspace-decision` |
| Dynamic HEAD | `525e1a13a0199e7648ccc332c1c06103bc269aaf` |
| Branch remote | `origin/p15.m4-desktop-workspace-decision` |
| Branch remote SHA | `525e1a13a0199e7648ccc332c1c06103bc269aaf` |
| Migration HEAD | `525e1a13a0199e7648ccc332c1c06103bc269aaf` |
| HEAD equals branch remote | `true` |
| HEAD equals migration head | `true` |
| P15.M1D ancestor | `true` |
| Index empty at start | `true` |
| Staged files at start | `0` |
| Tracked worktree clean at start | `true` |

## Prerequisites

Required committed records were present and used as binding authority:

| Record | Verdict |
| --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_migration_authorization.md` | `hermes_0_19_migration_authorized_with_constraints` |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline.md` | `hermes_0_19_product_baseline_ready_with_constraints` |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline_storage_reconciliation.md` | `hermes_0_19_product_baseline_portable_integrity_ready` |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline_commit_finalization.md` | `hermes_0_19_product_baseline_committed_integrity_finalized` |
| `0_architecture/governance/agent_platform_hermes_0_19_integrity_algorithm_canonicalization.md` | `hermes_0_19_baseline_integrity_algorithm_canonicalized` |

Binding P15.M0 surface authority remains active:

| Surface | P15.M0 role |
| --- | --- |
| Pepper P13 | current canonical product UI during migration |
| Hermes Web Dashboard | upstream route and UX comparison reference |
| Hermes Desktop | future governed local human-client candidate |
| Hermes Workspace | future adjacent operations-surface candidate |

P15.M0 also binds that neither Desktop nor Workspace may directly own Pepper policy, provider authority, credential authority, durable backend truth, product routing authority, worker authority, update authority or approval authority.

## Canonical V2 Integrity

Canonical utility:

```text
10_scripts/governance/pepper_baseline_integrity.py
```

Exact CLI:

```text
python 10_scripts/governance/pepper_baseline_integrity.py --repo-root . --product-root 2_products/pepper-agent --mode all --format json
```

Required result:

| Scope | Algorithm | Files | Bytes | SHA-256 |
| --- | --- | ---: | ---: | --- |
| Candidate | `agent-platform-git-tree-sha256-v2` | 6684 | 148145642 | `fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b` |
| Payload | `agent-platform-git-tree-sha256-v2` | 6681 | 145406255 | `3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073` |
| Baseline record | `sha256-git-blob-v1` | not_applicable | 25333 | `5aa7d9582e8036e66a9a81be772aa75b3cb930a978c0128bc0a6b2585baa0fea` |

The historical V1 product aggregate values remain non-authoritative for P15.M4 downstream gates.

## Source Identity Boundary

Hermes Workspace 2.3.0 remains an ignored source-only reference under `4_external/sources/hermes-workspace-v2.3.0`.

Locked Workspace upstream identity consumed from `0_architecture/governance/agent_platform_hermes_0_19_workspace_source_lock.md` and canonicalized by `0_architecture/governance/agent_platform_hermes_workspace_2_3_0_source_integrity_canonicalization.md`:

| Field | Value |
| --- | --- |
| Repository | `https://github.com/outsourc-e/hermes-workspace` |
| Version | `2.3.0` |
| Tag | `v2.3.0` |
| Tag object SHA | `0218dbafce50fa69ba9ce045e2c8a3f5383bd1db` |
| Commit | `15fa9cd706f5c04e4db288fb958e21d10fc776da` |
| Historical ambient archive SHA-256 | `10119f375ee7632443353fd7d2f1e45ca613caa971123f0f72c3890c8dc3c438` |
| Canonical archive SHA-256 | `12684835e4d0bf3acff0e6e8e044dde7fab3c2fa1ce91c50d9e377a0282c24c6` |
| Historical source-lock tree algorithm | `agent-platform-tree-sha256-v1` |
| Historical source-lock tree SHA-256 | `f00b66d6e7dc5bef87602cb026bdf14e593314b9fd242e3e1af48c20704616b9` |
| Current Git source tree algorithm | `agent-platform-git-source-tree-sha256-v2` |
| Current Git source tree SHA-256 | `6a16ebca192555e6afa95fe6bcd701c2d50e57440de4766cdf58e07a2054c394` |
| Current materialized source tree algorithm | `agent-platform-materialized-source-tree-sha256-v1` |
| Current materialized source tree SHA-256 | `6a16ebca192555e6afa95fe6bcd701c2d50e57440de4766cdf58e07a2054c394` |
| Regular files | 1057 |
| Directories | 142 |
| Regular-file bytes | 100314437 |
| Symlinks | 0 |
| Reparse points | 0 |
| Nested Git entries | 0 |
| Source manifest | `0_architecture/governance/agent_platform_hermes_workspace_2_3_0_source_manifest.tsv` |
| Source manifest rows | 1057 |
| Source manifest columns | 12 |
| Source manifest SHA-256 | `dfdbbd8e6eb1595661fec1dadb4392b6026863cfefbc66716795d07c572525ec` |

P15.M5A current worktree evidence:

| Check | Result |
| --- | --- |
| Source root present | `true` |
| Effective ignore rule | `.gitignore:16:4_external/sources/` |
| Tracked files under Workspace root | `0` |
| Visible untracked files under Workspace root | `0` |
| `package.json` identity | `name=hermes-workspace`, `version=2.3.0`, `private=true` |
| Current canonical count scan | `files=1057`, `dirs=142`, `bytes=100314437` |
| Git-source/materialized-source comparison | `match` |

The exact historical `agent-platform-tree-sha256-v1` source-tree implementation is not committed in this repository. P15.M5A therefore supersedes that value for current Workspace 2.3.0 source-integrity authority. This does not change the P15.M4 productization decision: Workspace is not imported, promoted, executed, deployed or adopted, and remains ignored reference-only source.

## Static Methodology

Static inspection used read-only file reads, content searches, Git status/identity checks and Python standard-library filesystem scans. Pepper, Desktop and Workspace modules were not imported or executed. Package managers, registries, builders, Desktop startup, Workspace startup, Docker, Compose, OAuth, provider calls, inference and Graphify were not run.

The machine-readable surface inventory is in `0_architecture/governance/agent_platform_hermes_0_19_desktop_workspace_manifest.tsv`.

## Final Decision

Selected productization posture:

```yaml
Pepper_P13: canonical_product_ui_now
Hermes_Web_Dashboard: route_by_route_reference_only
Hermes_Desktop: disabled_future_governed_local_client_candidate
Hermes_Workspace_2_3_0: ignored_reference_only_future_adjacent_operations_candidate
Workspace_import: unauthorized
Workspace_shell_replacement: unauthorized
Desktop_enablement: unauthorized
```

Decision table:

| Surface | Current source | P15.M4 decision | Product authority granted now |
| --- | --- | --- | --- |
| Pepper P13 | `2_products/hermes-agent/web/src/agent-platform` | Keep canonical route, navigation, product-config and safe-settings authority | yes, existing authority retained |
| Hermes Web Dashboard | `2_products/pepper-agent/web` | Keep as route-by-route reference for future reconciliation | no |
| Hermes Desktop | `2_products/pepper-agent/apps/desktop` | Keep present in baseline candidate but disabled; classify as future governed local-client candidate | no |
| Hermes Workspace 2.3.0 | `4_external/sources/hermes-workspace-v2.3.0` | Keep ignored and untracked as reference-only adjacent operations candidate | no |

This decision preserves P15.M0 Option 1: upgrade the current product baseline and forward-port deliberately, rather than replacing Pepper P13 with Desktop, Web Dashboard or Workspace.

## Four-Surface Comparison

| Surface | Primary value | Main governance issue | P15.M4 disposition |
| --- | --- | --- | --- |
| Pepper P13 | Current governed product namespace, static descriptors, feature gating, safe settings and protected `/agent-platform/**` route ownership | Still experimental and must be carried forward intentionally | Keep canonical |
| Hermes Web Dashboard | Mature upstream browser dashboard route inventory and gateway expectations | Wholesale adoption would bypass P13 descriptors, safe settings and product configuration | Reference route-by-route only |
| Hermes Desktop | Native human client, local/remote backend modes, package/update UX and machine integration | Owns process spawning, filesystem, terminal, Git, credentials, updater and runtime plugin authority | Future local-client candidate; disabled now |
| Hermes Workspace 2.3.0 | Broad TanStack operational shell with dashboard, chat, files, terminal, jobs, swarm, memory, skills, MCP and Compose deployment | Owns its own auth/session store, filesystem/terminal APIs, deployment volumes, provider env and shell authority | Ignored reference-only adjacent operations candidate |

## Pepper P13 Authority

Pepper P13 remains the only product UI route authority for the Agent Platform namespace.

Evidence:

- `2_products/hermes-agent/hermes_cli/agent_platform/product_config.py:68-89` declares the default product identity, feature flag and nine extension modules.
- `2_products/hermes-agent/hermes_cli/agent_platform/product_config.py:95-100` explicitly has no environment, user-config, managed-scope or provider override tier.
- `2_products/hermes-agent/web/src/agent-platform/product-config.ts:74-133` parses strict product configuration, fails closed to `null` and treats missing features as disabled.
- `2_products/hermes-agent/web/src/agent-platform/extensions.ts:52-60` statically imports reviewed descriptors only.
- `2_products/hermes-agent/web/src/agent-platform/extensions.ts:72-90` rejects duplicate, invalid, colliding or incorrectly anchored descriptors.
- `2_products/hermes-agent/web/src/agent-platform/extensions.ts:99-120` constrains product extension paths to canonical `/agent-platform/` descendants.
- `2_products/hermes-agent/web/src/App.tsx:466-508` resolves registered product extensions into routes and navigation.
- `2_products/hermes-agent/web/src/agent-platform/shell/navigation.ts:87-108` blocks plugin manifests whose path or override can claim the protected product namespace.

Canonical P13 route set:

| Route | Descriptor evidence | Current disposition |
| --- | --- | --- |
| `/agent-platform/overview` | `runtime-overview/descriptor.ts:6-21` | retain |
| `/agent-platform/projects` | `projects-tickets/descriptors.ts:8-23` | retain |
| `/agent-platform/projects/:boardSlug` | `projects-tickets/descriptors.ts:26-36` | retain |
| `/agent-platform/projects/:boardSlug/tickets/:taskId` | `projects-tickets/descriptors.ts:38-48` | retain |
| `/agent-platform/approvals` | `approval-inbox/descriptors.ts:7-22` | retain |
| `/agent-platform/approvals/:approvalId` | `approval-inbox/descriptors.ts:25-35` | retain |
| `/agent-platform/executions` | `execution-inspector/descriptors.ts:7-22` | retain |
| `/agent-platform/executions/:executionId` | `execution-inspector/descriptors.ts:25-35` | retain |
| `/agent-platform/settings` | `safe-settings/descriptor.ts:6-21` | retain |

## Desktop Decision

Hermes Desktop is not adopted or enabled by P15.M4. It remains a disabled future governed local-client candidate.

Static evidence shows Desktop is a mature native shell, not a passive route library:

| Boundary | Evidence | P15.M4 classification |
| --- | --- | --- |
| Package/build authority | `apps/desktop/package.json:13-52` declares dev, build, package, desktop test and check scripts | no scripts run; future packaging review required |
| Installer targets | `apps/desktop/package.json:157-268` configures Electron Builder, protocol, ASAR, macOS, Windows and Linux targets | no distribution authority now |
| Backend ownership | `apps/desktop/electron/backend-command.ts:18-22` builds `serve --host 127.0.0.1 --port 0` backend args | local backend process authority requires P14/P15 governance |
| Process spawning | `apps/desktop/electron/main.ts:7079-7106` spawns Hermes backend with Desktop-specific env | disabled until process and profile boundaries are governed |
| Update authority | `apps/desktop/electron/main.ts:2343-2349` states staged updater binary owns repository mutation for update/rebuild handoff | no update authority now |
| Remote gateway auth | `apps/desktop/electron/connection-config.ts:12-18` supports token auth and OAuth cookie plus WS ticket auth | credential and OAuth governance required before use |
| Secret storage | `apps/desktop/electron/hardening.ts:26-60` encrypts remote tokens through Electron `safeStorage` or refuses persistence | credential store boundary required before use |
| Sensitive files | `apps/desktop/electron/hardening.ts:62-108` blocks `.ssh`, `.gnupg`, AWS credentials, `.env`, key/cert files and auth config files | useful hardening pattern, not sufficient product approval |
| IPC bridge | `apps/desktop/electron/preload.ts:3-67` exposes backend, connection, OAuth/cloud, notification, file and preview IPC | capability audit required |
| Filesystem/Git IPC | `apps/desktop/electron/preload.ts:107-137` exposes directory, file, Git worktree, review, commit, push and PR IPC | no product Git authority now |
| Terminal IPC | `apps/desktop/electron/preload.ts:140-160` exposes terminal lifecycle and data channels | terminal/process authority requires governance |
| PTY process | `apps/desktop/electron/main.ts:9109-9124` spawns node-pty shell sessions | disabled until governed local-client profile exists |
| Runtime plugins | `apps/desktop/src/contrib/runtime-loader.ts:17-27` states loaded plugins have full app authority and are not sandboxed | no plugin authority now |

Desktop is strategically useful for a future Windows local client against a governed WSL2 or remote Linux backend. Promotion requires explicit P15.M7/P15.M8/P15.M18/P15.M19 work for process, profile, credential, update, plugin, filesystem and signing boundaries.

## Workspace Decision

Hermes Workspace 2.3.0 is not adopted, imported or used to replace Pepper P13. It remains ignored reference-only source for a possible future adjacent operations surface.

Static evidence shows Workspace is an independent shell and deployment product:

| Boundary | Evidence | P15.M4 classification |
| --- | --- | --- |
| Package identity | `4_external/sources/hermes-workspace-v2.3.0/package.json:2-8` declares `hermes-workspace`, version `2.3.0`, MIT, private, module package | source identity reference only |
| Scripts | `package.json:10-28` declares dev, build, start, managed smoke, playground WS, lint, format and Electron build scripts | no scripts run |
| TanStack shell | `src/routes/__root.tsx:117-190` creates the Workspace root route and document metadata | no shell replacement |
| Route map | `src/components/workspace-shell.tsx:94-108` maps dashboard, chat, files, terminal, jobs, swarm, memory, skills, MCP, profiles and settings | route inventory reference only |
| Mobile/page titles | `src/components/workspace-shell.tsx:168-184` includes terminal, files, jobs, conductor, operations, swarm, memory, skills, MCP, profiles, settings, debug and activity titles | adjacent UX reference only |
| Session persistence | `src/server/auth-middleware.ts:12-30` persists session tokens at `~/.hermes/workspace-sessions.json` with 30-day TTL | not compatible with shared credential/session authority now |
| Password/proxy auth | `src/server/auth-middleware.ts:140-158` reads `HERMES_PASSWORD` with `CLAUDE_PASSWORD` fallback and `src/server/auth-middleware.ts:203-245` gates forwarded headers behind `TRUST_PROXY` | future deployment hardening input |
| Gateway URLs | `src/server/gateway-capabilities.ts:1-17` documents gateway/dashboard probing, runtime override persistence and env/default URL precedence | service boundary required before use |
| Runtime overrides | `src/server/gateway-capabilities.ts:28-57` persists overrides in `~/.hermes/workspace-overrides.json` | shared state prohibited now |
| Tasks backend | `src/lib/tasks-api.ts:1-14` chooses `/api/hermes-tasks` or `/api/claude-tasks`, preferring Hermes task data | useful compatibility evidence only |
| Chat streaming | `src/routes/api/send-stream.ts:1-41` composes Workspace-scoped messages, sessions, gateway capabilities, OpenAI-compatible and Responses paths | provider/runtime authority not adopted |
| Files API | `src/routes/api/files.ts:31-64` resolves paths and rejects escapes outside selected workspace root | filesystem pattern reference only |
| Terminal sessions | `src/server/terminal-sessions.ts:1-4` describes terminal sessions through a Python PTY helper | process authority not adopted |
| PTY spawn | `src/server/terminal-sessions.ts:107-122` spawns `python3` with `pty-helper.py` and shell command args | not run; future process boundary required |
| Dockerfile | `Dockerfile:13-23` uses `node:22-slim`, Corepack, pnpm install and build | build not run; dependency/deployment review required |
| Runtime image | `Dockerfile:26-59` installs `python3`, runs as non-root UID `10010`, exposes `3000` and starts `server-entry.js` | future deployment reference only |
| Compose images | `docker-compose.yml:15-18` pulls mutable `nousresearch/hermes-agent:latest` and `ghcr.io/outsourc-e/hermes-workspace:latest` | rejected for P15.M10 until pinned/hardened |
| Provider env | `docker-compose.yml:47-63` passes provider keys and gateway API key from `.env` | no secret authority now |
| Published ports | `docker-compose.yml:97-112` documents password/cookie/proxy settings and binds Workspace to `127.0.0.1:3000` | future local deployment input only |
| Volumes | `docker-compose.yml:69-73` persists agent state in `claude-data:/opt/data` | shared writable volume prohibited now |

Workspace may inform route inventory, mobile patterns, task/job UX, deployment hardening and service-boundary design. It must not be imported wholesale because that would bypass Pepper descriptors, product configuration, protected namespace, safe settings, P14 runtime containment and P15 credential/provider/worker boundaries.

## Route And Navigation Reuse Matrix

| Pepper authority route or area | Current owner | Dashboard input | Desktop input | Workspace input | P15.M4 reuse decision |
| --- | --- | --- | --- | --- | --- |
| `/agent-platform/overview` | P13 descriptor | reference for runtime/dashboard aggregation | reference for local connection state | reference for dashboard/status shell | keep P13 implementation; compare only |
| `/agent-platform/projects` | P13 descriptor | reference for sessions/files/task-adjacent dashboard routes | reference for Git/worktree UX only | reference for task/job organization | keep P13 implementation; no import |
| `/agent-platform/projects/:boardSlug` | P13 descriptor | none as authority | none as authority | task list/detail patterns only | keep P13 implementation; no import |
| `/agent-platform/projects/:boardSlug/tickets/:taskId` | P13 descriptor | none as authority | none as authority | task mutation semantics reference only | keep P13 implementation; no import |
| `/agent-platform/approvals` | P13 descriptor | reference for admin/status patterns | Desktop notifications reference only | operations/conductor patterns reference only | keep P13 human approval authority |
| `/agent-platform/approvals/:approvalId` | P13 descriptor | none as authority | none as authority | none as authority | keep P13 implementation |
| `/agent-platform/executions` | P13 descriptor | reference for sessions/logs/analytics | local backend/terminal status reference only | jobs/terminal/swarm reference only | keep P13 implementation |
| `/agent-platform/executions/:executionId` | P13 descriptor | reference only | reference only | reference only | keep P13 implementation |
| `/agent-platform/settings` | P13 descriptor | reference for config/env/profile surfaces | reference for gateway/profile/credential UX | reference for settings/gateway/password UX | keep P13 safe-settings authority |
| `/chat`, `/sessions`, `/files`, `/models`, `/skills`, `/mcp`, `/profiles`, `/config` | Hermes tools and dashboard reference area, not Agent Platform route authority | compare route-by-route in P15.M5/P15.M6 | Desktop may host future local client chrome | Workspace may inform adjacent operations | no `/agent-platform/**` ownership transfer |

## Shared Backend, State And Credential Prohibitions

P15.M4 explicitly rejects implicit sharing between Pepper, Desktop and Workspace.

Prohibited until a future ticket grants exact authority:

- shared writable `HERMES_HOME` across Pepper server, Desktop client and Workspace service;
- Desktop encrypted remote token store reuse by Pepper or Workspace;
- Workspace `~/.hermes/workspace-sessions.json` reuse as Pepper session truth;
- Workspace `~/.hermes/workspace-overrides.json` reuse as Pepper gateway truth;
- Docker `claude-data` or host-path volume as shared product credential or runtime state;
- Desktop Git IPC, commit, push, PR or update IPC as frontend product authority;
- Desktop runtime plugin ESM as product extension mechanism;
- Workspace terminal/PTTY process APIs as product worker authority;
- Workspace provider `.env` and Compose secrets as P15 provider credential authority;
- any direct backend truth split between Pepper, Desktop and Workspace outside a governed Hermes gateway/service contract.

Allowed now:

- static comparison of routes, UI patterns, deployment assumptions and boundary risks;
- future extraction candidates recorded as requirements for P15.M5 through P15.M19;
- no runtime use.

## Asset Reuse And Obsolescence Decisions

| Asset or pattern | P15.M4 decision | Reason |
| --- | --- | --- |
| P13 descriptors and protected namespace | retain | current governed product authority |
| P13 safe settings | retain | only current settings authority |
| Web Dashboard route inventory | reference | useful route parity input without route authority transfer |
| Desktop package/build/update scripts | retain in candidate source only | future local-client packaging input, no current execution |
| Desktop backend spawn model | reference | useful for local-client design, requires P14 process governance |
| Desktop safeStorage token handling | reference | useful pattern, requires P15 credential governance |
| Desktop runtime plugin loader | do not reuse as product boundary | source states it is not a capability sandbox |
| Workspace TanStack shell | reference only | wholesale shell replacement unauthorized |
| Workspace mobile navigation and operations routes | reference only | potential adjacent UX input |
| Workspace auth/session store | do not reuse now | independent durable session authority conflicts with Pepper |
| Workspace filesystem and terminal APIs | reference only | process/filesystem authority requires service boundary |
| Workspace Dockerfile | reference only | no build/install/deployment authority |
| Workspace Compose `latest` images | obsolete for Pepper deployment as-is | mutable images violate future reproducibility requirements |
| Workspace provider `.env` pass-through | do not reuse now | P15 provider credential authority remains separate |

## Promotion Blockers And Owners

Desktop promotion blockers:

| Blocker | Required owner ticket |
| --- | --- |
| Local backend process spawn, env, readiness and shutdown mapped to Pepper runtime governance | P15.M7 |
| Desktop credential store, OAuth cookie, remote token and WS ticket boundaries mapped to P15 contracts | P15.M8 and P15.M11 |
| IPC capability audit for filesystem, Git, terminal, update, notifications, external URLs and previews | P15.M7 and P15.M18 |
| Runtime plugin sandbox or explicit local-trust-only policy | P15.M5 or later plugin governance ticket |
| Signed/provenanced update, rollback and package lifecycle | P15.M18 and P15.M19 |
| Windows WSL2 and remote Linux backend topology | P15.M9 and P15.M12 |

Workspace promotion blockers:

| Blocker | Required owner ticket |
| --- | --- |
| Adjacent service boundary, API contract and route ownership model | P15.M5 and P15.M6 |
| Session store and authentication separation from Pepper | P15.M8 and P15.M13 |
| Filesystem, terminal and job execution containment | P15.M7, P15.M10 and P15.M15 |
| Docker image pinning, volume boundaries and secret injection | P15.M10 |
| Provider env and gateway-token handling aligned with P15 credential authority | P15.M8 |
| VPS/reverse-proxy/TLS/cookie/proxy posture | P15.M13 and P15.M14 |
| Rollback and operations drill before promotion | P15.M16 and P15.M19 |

## Final Validation

Final validation was recorded after artifact creation in this same worktree.

| Check | Result |
| --- | --- |
| Canonical V2 utility | passed; candidate `6684` files, `148145642` bytes, `fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b`; payload `6681` files, `145406255` bytes, `3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073`; baseline record `25333` bytes, `5aa7d9582e8036e66a9a81be772aa75b3cb930a978c0128bc0a6b2585baa0fea` |
| Canonical utility tests | passed; `Ran 14 tests`, `OK` |
| Candidate file set | exactly two visible untracked authorized files; no tracked file diffs |
| Manifest rows | `80` data rows, `25` columns, duplicate IDs `0` |
| Manifest schema validation | blank mandatory fields `0`; invalid overlap classifications `0`; invalid adoption dispositions `0`; unresolved rows without explicit status `0`; adopt_now rows `0` |
| Manifest coverage validation | unclassified Desktop surfaces `0`; unclassified Workspace surfaces `0`; unclassified route overlaps `0`; unclassified current assets `0`; unclassified promotion blockers `0` |
| Manifest SHA-256 | `bee425d12235fccc49d12d755852100be4ccd3a9e7fd6b6f548ead689e3f3747` |
| Manifest bytes | `58468` |
| Trailing whitespace | passed for P15.M4 artifacts; `git diff --check` produced no output |
| Git status | only `?? 0_architecture/governance/agent_platform_hermes_0_19_desktop_workspace_manifest.tsv` and `?? 0_architecture/governance/agent_platform_hermes_0_19_desktop_workspace_productization_decision.md` |

## Git Boundary

P15.M4 does not stage, commit, push, stash, reset, clean, amend or force any file.
