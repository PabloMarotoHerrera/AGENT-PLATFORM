# P11.1 - Hermes License / Dependency / Runtime Audit

## Status

P11.1 completed a bounded, static audit of the exact Hermes source authorized by P11.0.

```text
repository: https://github.com/NousResearch/hermes-agent
release: 0.18.2
tag: v2026.7.7.2
commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
local path: 4_external/sources/hermes-agent
source identity: verified
working tree: clean
review mode: static source inspection only
```

Completion markers:

```text
hermes_license_dependency_runtime_audit_ready
hermes_installation_footprint_recorded
hermes_runtime_footprint_recorded
hermes_persistent_state_inventory_recorded
hermes_network_inventory_recorded
hermes_provider_inventory_recorded
hermes_optional_feature_matrix_recorded
hermes_minimum_local_profile_defined
hermes_full_feature_profile_defined
```

Boundary markers:

```text
no_hermes_execution
no_installation
no_provider_activation
no_credential_access
no_git_mutation
```

These markers mean the audit evidence is ready for downstream governance. They do not approve installation, execution, adoption, redistribution, provider access, or integration.

## Executive Verdict

Hermes is a broad agent runtime, not a narrow library. Its default core tool surface includes terminal and process control, file writes, browser automation, memory, code execution, delegation, and cron management. Optional surfaces add messaging gateways, dashboard and API listeners, model and memory providers, MCP, desktop control, plugins, telemetry, Kanban workers, and persistent scheduling.

The core repository is MIT-licensed, but the inspected checkout is not uniformly MIT:

- `plugins/security-guidance/` contains Apache-2.0 material with a required NOTICE.
- `skills/productivity/powerpoint/LICENSE.txt` contains restrictive Anthropic terms that prohibit extraction, retention outside the services, reproduction, derivatives, and redistribution except as allowed by an applicable Anthropic agreement.

Therefore:

```text
static audit: complete
core MIT claim: verified
full-tree unrestricted MIT treatment: rejected
full-tree redistribution/adoption: blocked pending license disposition
installation/execution/integration: not authorized
```

At minimum, the PowerPoint skill must be excluded or separately cleared before any vendoring, redistribution, mirroring, or derivative distribution. Apache-2.0 attribution and NOTICE obligations must be preserved. Third-party dependency and asset licenses still require an SBOM-level clearance pass before distribution.

## Authorization and Identity

Canonical authorization:

```text
0_architecture/governance/agent_platform_hermes_source_review_authorization.md
```

The repository was rechecked with a temporary per-command `safe.directory` override. No global Git configuration changed.

| Check | Required | Observed | Result |
| --- | --- | --- | --- |
| Git work tree | `true` | `true` | Pass |
| Origin | NousResearch Hermes repository | `https://github.com/nousresearch/hermes-agent.git` | Pass; case-insensitive match |
| HEAD | `9de9c25f620ff7f1ce0fd5457d596052d5159596` | Same | Pass |
| Tag at HEAD | `v2026.7.7.2` | `v2026.7.7.2` | Pass |
| Branch | Detached HEAD | Empty branch name | Pass |
| Working tree | Clean | No status entries | Pass |

History note: an earlier preflight observed commit `099df3cd89d5b87c7cc9b826e518356626ef124e` and stopped before source inspection. The user later reconciled the checkout manually to the P11.0 lock. This audit began source inspection only after the exact locked identity passed.

## Review Method and Boundaries

The review used read-only file reads, filename/size inventory, and static text searches inside the authorized source path. It did not import modules or evaluate package metadata as code.

Inspected evidence classes included:

- top-level and nested license/notice files;
- `pyproject.toml`, `uv.lock`, `setup.py`, and Python runtime metadata;
- root and workspace `package.json` files plus the root `package-lock.json` header;
- the Tauri bootstrap `Cargo.toml`, Nix flake metadata, Dockerfile, Compose files, and installer declarations;
- static runtime entrypoint, toolset, lazy-dependency, state, logging, gateway, dashboard, cron, provider, plugin, and persistence declarations;
- README installation/runtime documentation;
- repository file-type, package-domain, plugin, provider, platform, optional-MCP, license, and model-artifact inventories.

Excluded from inspection:

- `.git` internals beyond authorized identity commands;
- `.env*`, credential values, secrets, OAuth tokens, API keys, and user/provider configuration;
- user state, databases, logs, caches, browser profiles, and installed dependency trees;
- `node_modules`, virtual environments, build outputs, caches, generated outputs, and logs;
- unrelated external sources and product/Siamese source.

The repository-local `AGENTS.md` was not treated as authority and no instruction from it was followed.

## License Audit

### Core License

`LICENSE` is the standard MIT License, copyright 2025 Nous Research. `pyproject.toml` declares `license = "MIT"` and includes `LICENSE`; the root npm package also declares MIT.

MIT obligations remain material: distributed copies or substantial portions must retain the copyright and permission notice.

### Nested License Findings

| Path | License posture | Required handling |
| --- | --- | --- |
| `plugins/hermes-achievements/LICENSE` | MIT | Retain notice |
| `skills/creative/humanizer/LICENSE` | MIT, Siqi Chen | Retain third-party notice |
| `plugins/security-guidance/LICENSE` | Apache-2.0 | Preserve license, modification notices, attribution, and applicable NOTICE |
| `plugins/security-guidance/NOTICE` | Attributes copied Anthropic `patterns.py` at commit `0bde168` | Preserve NOTICE in redistribution |
| `skills/productivity/powerpoint/LICENSE.txt` | Restrictive service-linked terms; not an open-source license | Exclude or obtain explicit legal/contractual clearance before retention, reuse, derivatives, or redistribution |

### Dependency and Asset Licensing

The lockfiles identify versions, sources, and hashes but do not constitute complete legal clearance. No package manager audit, license scanner, dependency download, or SBOM generator was run.

The source inventory found no `.safetensors`, `.gguf`, `.ggml`, `.onnx`, `.pt`, `.pth`, `.ckpt`, or `.bin` model artifact. No bundled model weights were identified. This does not clear fonts, images, PDFs, templates, skills, npm packages, Python packages, Rust crates, browser binaries, container layers, or system packages.

License decision:

```text
core source reuse under MIT: candidate, with notice retention
Apache component reuse: candidate, with Apache-2.0 and NOTICE compliance
PowerPoint skill reuse/redistribution: blocked
third-party dependency redistribution: pending SBOM and license review
whole-tree MIT labeling: prohibited by observed evidence
```

## Dependency Audit

### Python

Build/runtime declarations:

```text
package: hermes-agent 0.18.2
Python: >=3.11,<3.14
build backend: setuptools.build_meta
build requirement: setuptools>=77.0,<83
lockfile: uv.lock revision 3
registry: PyPI
```

The base dependency set contains about 30 direct declarations. Major classes include:

- model transport: `openai`;
- HTTP/network: `httpx[socks]`, `requests`, `urllib3`, `certifi`, `websockets`;
- data/config: `python-dotenv`, `pyyaml`, `ruamel.yaml`, `pydantic`, `jinja2`;
- CLI/runtime: `fire`, `rich`, `prompt_toolkit`, `tenacity`, `packaging`, `psutil`;
- scheduling and content: `croniter`, `Markdown`;
- cryptography/auth support: `PyJWT[crypto]`, `cryptography`;
- web server: `fastapi`, `uvicorn[standard]`, `python-multipart`;
- media and filesystem: `Pillow`, `pathspec`;
- platform-specific PTY, timezone, and log rotation packages.

Most base packages are exact-pinned. A smaller set uses bounded ranges. `uv.lock` records resolved artifacts and hashes for supported Python versions.

Optional extras cover provider SDKs, web search, image generation, TTS/STT, terminal backends, memory providers, development tooling, messaging platforms, Matrix encryption, MCP, Home Assistant, SMS, Teams, ACP, cloud credentials, Google APIs, YouTube, dashboard, Termux, and an aggregate `[all]` profile.

`tools/lazy_deps.py` defines 34 allowlisted feature keys across model providers, search, speech, image generation, memory, messaging, remote terminal backends, skills, ACP, dashboard, vision, computer use, and trace upload. The static default is:

```text
security.allow_lazy_installs: true
```

At first use, an enabled optional backend may invoke a venv-scoped package install. Specs are allowlisted and URL/file specs are rejected, but this remains runtime package mutation and network access. The minimum profile must set this option to false.

### Node and Browser Tooling

The root npm package is private, requires Node 20+, uses npm workspaces, and has a lockfileVersion 3 lock. Workspaces include bootstrap installer, desktop, shared code, TUI, dashboard web UI, and nested Ink package. Additional standalone package manifests exist for the Photon sidecar, WhatsApp bridge, and documentation website.

Notable runtime/build dependencies include Electron, React, Vite, Tauri frontend packages, xterm, Ink, `node-pty`, `agent-browser`, Playwright/Chromium-related tooling, Baileys/Express for WhatsApp, and `spectrum-ts` for Photon.

Lifecycle/script findings:

- root `postinstall` runs an echo command;
- Photon sidecar `postinstall` runs `node patch-spectrum-mixed-attachments.mjs`;
- desktop and web packages define build, packaging, signing, test, and development scripts;
- desktop packaging targets DMG/ZIP, NSIS/MSI, AppImage, DEB, and RPM;
- npm dependencies commonly use semver ranges, while selected packages and overrides are exact-pinned;
- the lockfile has an install-script flag and must be treated as executable supply-chain input.

### Rust and Nix

The Windows bootstrap installer has a Tauri/Rust `Cargo.toml`, Rust 1.77 minimum, and dependencies including Tauri plugins, Tokio, Reqwest/rustls, tracing, serialization, and Windows APIs. No `Cargo.lock` was found in the bounded native-manifest inventory, so reproducible Rust resolution is not demonstrated by this checkout.

Nix support uses `flake.nix` plus `flake.lock` and imports package, overlay, module, check, and dev-shell definitions. It targets x86_64 Linux, aarch64 Linux, and aarch64 Darwin.

### Native and Binary Risk

Potential native/binary surfaces include PTYs, cryptography, Pillow codecs, voice/audio dependencies, Matrix `python-olm`, Electron, `node-pty`, Tauri/Rust, Playwright Chromium, ffmpeg, Docker CLI, compilers, and platform-specific installers. These expand architecture, signing, CVE, and provenance requirements.

No dependency was installed, resolved, imported, downloaded, updated, or audited dynamically.

## Installation Footprint

Declared installation routes include remote shell/PowerShell installers, source checkout installation, Docker/Compose, Nix, Homebrew packaging documentation, Termux, and desktop installers.

### Native Installers

The official quick-install documentation invokes remote scripts from `hermes-agent.nousresearch.com`. Static installer declarations show that installation may:

- download or locate `uv`;
- provision Python and create a virtual environment;
- clone or update a Git checkout;
- install Python dependencies from `uv.lock` or fallback resolution paths;
- install or locate Node.js and npm;
- install `agent-browser`, CamoFox/browser dependencies, and Chromium;
- install or locate ripgrep, ffmpeg, and Git;
- seed bundled skills into `HERMES_HOME`;
- create command wrappers and PATH changes;
- invoke setup and optionally configure a gateway service;
- use system package managers or elevated commands on supported Unix paths.

Default data/code locations include `~/.hermes` on POSIX and `%LOCALAPPDATA%\hermes` on native Windows, with a separate code checkout/venv under the managed installation layout. Root Linux installs may place code under `/usr/local/lib/hermes-agent` while keeping data in `HERMES_HOME`.

The legacy `setup-hermes.sh` can remove an existing `venv`, create a new environment, install dependencies, optionally install ripgrep, synchronize skills, and invoke interactive setup. It must not be used in a controlled integration without a separate installer review.

### Docker

The Docker image is a multi-stage Debian 13.4 build with pinned uv and Node 22 source images. It installs system packages including Python, Git, SSH client, ripgrep, ffmpeg, C/C++ build tools, libffi, libolm, process tools, Docker CLI, and xz utilities. It also installs s6-overlay, npm workspaces, Playwright Chromium, Python extras, and prebuilt web/TUI assets.

Runtime layout:

```text
immutable application tree: /opt/hermes
durable state volume: /opt/data
HERMES_HOME: /opt/data
runtime user: hermes, default UID 10000
process supervisor/PID 1: s6-overlay /init
```

The image redirects optional lazy packages to `/opt/data/lazy-packages`, although the sealed image also sets a lazy-install disable flag. Compose mounts host Hermes state into `/opt/data`.

### Entrypoints

Python console entrypoints are:

```text
hermes -> hermes_cli.main:main
hermes-agent -> run_agent:main
hermes-acp -> acp_adapter.entry:main
```

No installer, setup hook, lifecycle hook, package manager, build, test, or entrypoint was run during P11.1.

## Runtime Footprint

### Process and Capability Surfaces

Static surfaces include:

- classic Python CLI and Node/Ink TUI;
- Electron desktop application and Tauri bootstrap installer;
- FastAPI dashboard/headless server and WebSocket/PTY bridges;
- multi-platform messaging gateway;
- OpenAI-compatible API server and generic webhook receiver;
- ACP editor adapter and optional MCP clients/servers;
- local, Docker, SSH, Singularity, Modal, and Daytona terminal environments;
- browser/CDP automation and computer-use integration;
- cron scheduler, background jobs, subagents, process registry, and Kanban dispatcher/workers;
- plugin, skill, memory, model-provider, observability, search, media, and messaging extensions.

The default core tool list is high privilege. It statically includes terminal/process control, file read/write/patch/search, browser control, skills management, memory, session search, code execution, delegation, and cron management. Some tools have runtime availability gates, but inclusion is broader than a least-privilege integration baseline.

Relevant defaults when their parent runtime is active include:

```text
lazy dependency installation: allowed
code execution mode: project working directory
remote model catalog fetch: enabled, one-hour cache TTL
cron provider: built-in in-process ticker, 60-second interval
Kanban dispatch inside gateway: enabled
Kanban auto-decompose: enabled
gateway legacy sessions.json mirror: enabled
```

Running only an interactive CLI does not itself start every service. Gateway, dashboard, API, webhook, cron, Kanban, provider, browser, and plugin behaviors depend on commands and configuration. Their presence nevertheless creates significant future activation risk.

No shutdown path, process isolation claim, approval control, redaction rule, or kill-switch behavior was validated dynamically.

## Persistent-State Inventory

`HERMES_HOME` is the primary profile-scoped state root. Defaults are `~/.hermes` on POSIX, `%LOCALAPPDATA%\hermes` on native Windows, and `/opt/data` in Docker. Named profiles use separate subdirectories.

Major declared state includes:

| State class | Representative paths/data |
| --- | --- |
| Configuration and sensitive stores | `config.yaml`, `.env`, auth/token stores; paths identified only, contents not inspected |
| Sessions | `state.db`, SQLite WAL/FTS5; full system prompts, messages, reasoning, tool calls, model/config metadata, CWD, Git metadata, usage and cost fields |
| Gateway | routing table in `state.db`, optional `sessions/sessions.json`, channel aliases/directory, pairing/platform state, dead targets, response store, PID/restart/drain markers |
| Logs | `logs/agent.log`, `errors.log`, `gateway.log`, `gui.log`, worker/curator/plugin logs |
| Cron | `cron/jobs.json`, lock/heartbeat/success files, `cron/output/<job>/<timestamp>.md` |
| Memory and learning | `memories/`, `skills/`, skill usage/curator state/backups, provider-specific memory state |
| Caches/media | `cache/images`, `cache/videos`, audio/documents/screenshots, model metadata, browser state, terminal temp/cache data |
| Execution | `sandboxes/`, `checkpoints/`, `processes.json`, snapshots, hook output spill, scripts, lazy packages, LSP binaries |
| Coordination | Kanban database and worker logs, verification evidence database, async/subagent state |
| Backups | full and quick snapshots under `backups/`; some providers may declare state outside `HERMES_HOME` |

Logging defaults are INFO with 5 MiB `agent.log` plus three backups. `errors.log` uses 2 MiB plus two backups; gateway uses 5 MiB plus three; GUI uses 10 MiB plus five. A redacting formatter is declared, but redaction completeness was not runtime-tested.

State cleanup cannot be represented as deleting one database. A controlled uninstall must inventory the active profile, shared root, code installation, virtual environment, managed Node/browser binaries, lazy packages, plugins, provider state outside `HERMES_HOME`, backups, services, wrappers, and container volumes. Backups may intentionally preserve otherwise deleted data.

No user state file or database was opened.

## Network Inventory

### Inbound Listeners

| Surface | Static default | Activation note |
| --- | --- | --- |
| Dashboard/headless server | `127.0.0.1:9119` | Explicit dashboard/serve command; HTTP and multiple WebSocket routes |
| OpenAI-compatible API server | `127.0.0.1:8642` | Gateway platform, disabled unless configured/enabled |
| Generic webhook | `0.0.0.0:8644` | Gateway platform; public-bind risk requires explicit authentication and network controls |
| Platform callbacks | Platform-specific, including callback/webhook listeners | Only when corresponding platform is enabled |

The dashboard source declares loopback defaults, an ephemeral session token, Host/Origin checks, and an authentication requirement for non-loopback binds. These are static controls, not runtime assurance. The Linux Compose file uses host networking. The Windows Compose file exposes dashboard port 9119 only on host loopback while binding inside the container to all interfaces.

### Outbound Network Classes

Potential outbound traffic includes:

- model inference and model-catalog endpoints;
- provider discovery and cloud credential flows;
- web search/extraction, browser navigation, and downloads;
- image, video, TTS, STT, and trace-upload services;
- messaging platforms, email, webhooks, and smart-home integrations;
- cloud terminal/sandbox providers;
- memory providers and observability backends;
- package registries, installer downloads, Git repositories, updates, browser binaries, and plugin/skill catalogs;
- optional MCP transports and external local services.

The remote model catalog is enabled by default in static configuration. Optional Langfuse observability is opt-in; Photon telemetry is declared default-false. No blanket no-telemetry conclusion is warranted for all optional third-party SDKs.

No socket was opened and no network endpoint was contacted during P11.1.

## Provider Inventory

Bundled model-provider plugin directories observed:

```text
alibaba, alibaba-coding-plan, anthropic, arcee, azure-foundry, bedrock,
copilot, copilot-acp, custom, deepseek, gemini, gmi, huggingface, kilocode,
kimi-coding, minimax, nous, novita, nvidia, ollama-cloud, openai-codex,
opencode-zen, openrouter, qwen-oauth, stepfun, vertex, xai, xiaomi, zai
```

The provider registry is lazy and supports user overrides under `HERMES_HOME`. Provider selection can alter transport behavior, endpoints, models, authentication method, and optional SDK installation.

Additional provider classes include:

- search: Exa, Firecrawl, Parallel and other plugin-defined routes;
- memory: Byterover, Hindsight, Holographic, Honcho, Mem0, OpenViking, RetainDB, Supermemory;
- messaging/platform plugins: DingTalk, Discord, email, Feishu, Google Chat, Home Assistant, IRC, LINE, Matrix, Mattermost, ntfy, Photon, Raft, SimpleX, Slack, SMS, Teams, Telegram, WeCom, WhatsApp, plus QQBot and other gateway adapters;
- media: image, video, TTS, STT, browser, and computer-use backends;
- remote execution: Modal and Daytona plus local/container/SSH/Singularity environments;
- observability and gateway/dashboard authentication plugins.

No provider configuration, secret, token, OAuth state, API, MCP server, or account was accessed or activated.

## Optional-Feature Matrix

| Feature | Static posture | Main footprint/risk | Minimum-profile decision |
| --- | --- | --- | --- |
| Terminal/process | In core tool list | Arbitrary local command and process control | Disable |
| File write/patch | In core tool list | Workspace and host file mutation | Disable; retain read-only evidence access only if needed |
| Browser/computer use | Browser tools in core; computer use gated | Browser state, downloads, remote content, OS interaction | Disable |
| Code execution | In core; project mode default | Executes generated code in working directory | Disable |
| Delegation/subagents | In core | Child processes, parallel activity, inherited capabilities | Disable |
| Memory/skills | In core | Persistent personal/context data and self-modification | Disable mutation and persistence |
| Cron | Tool in core; scheduler under runtime | Durable unattended execution and delivery | Disable |
| Kanban | Gateway dispatcher default-on | SQLite queue, worker spawning, retries/reclaim | Disable |
| Gateway/messaging | Explicit service | Long-lived network connections and inbound untrusted content | Do not start |
| Dashboard/API/webhooks | Explicit services | HTTP/WebSocket/PTY exposure; public-bind risk | Do not start |
| Model providers | Selection required for useful agent work | Credentials, inference egress, provider SDKs | Loopback-only custom endpoint for minimum candidate |
| Lazy dependencies | Allowed by default | Runtime package mutation and registry access | Set false |
| MCP | Optional catalogs and runtime client | External tools/process/network expansion | Disable |
| Plugins | Bundled and user-discoverable | Arbitrary extension code and hooks | Disable nonessential plugins |
| Observability/telemetry | Optional plugins/SDKs | Conversation, tool, and usage data egress | Disable |
| TUI/desktop | Optional UI surfaces | Node/Electron, PTY, WebSocket, packaging footprint | Exclude from minimum |
| Voice/media | Optional | Native libraries, devices, provider egress, cached media | Disable |
| Remote terminal backends | Optional | Cloud/container/SSH execution and state | Disable |
| Optional skills/MCP catalogs | Shipped but not all active | Instruction and dependency expansion | Do not install/activate |

## Minimum Local Profile

This is a governance definition only. It is not an installation or execution authorization.

```text
purpose: bounded, temporary evaluation of the core conversation loop
runtime: Python 3.11-3.13 in an isolated environment
dependency source: exact approved lock/SBOM only
state root: dedicated temporary HERMES_HOME, never the user's normal home
model route: one explicitly approved loopback OpenAI-compatible endpoint
external egress: deny by default
listeners: none
services: no gateway, dashboard, API, webhook, cron, Kanban, ACP, or MCP
package mutation: security.allow_lazy_installs=false
remote catalog: disabled
tools: no terminal/process, write/patch, browser, computer use, code execution,
       delegation, cron, Kanban, messaging, memory persistence, or skill mutation
plugins/optional skills: disabled except an explicitly reviewed minimum allowlist
logging: warning/error only where possible; temporary and deleted after review
persistence: no retained sessions, memory, caches, media, browser state, or backups
shutdown: supervised process kill plus post-run process/port/state verification
```

Before this candidate can run, governance must resolve the PowerPoint license exception, produce an approved dependency/SBOM set, verify that the tool allowlist is enforceable, define egress denial, define cleanup checks, and issue a separate runtime gate.

## Full-Feature Profile

The full-feature profile includes Python, Node 22, browser binaries, native/system packages, dashboard/TUI/desktop assets, provider and messaging extras, optional lazy dependencies, gateway services, persistent state, plugins, skills, memory, cron, Kanban, subagents, browser/computer use, MCP, observability, and remote execution backends.

Required controls before any full-profile evaluation:

- license disposition for every non-MIT component and all distributed dependencies/assets;
- signed SBOM, provenance, vulnerability, lockfile, and lifecycle-script review;
- isolated host or container with immutable code and a dedicated state volume;
- explicit provider, plugin, tool, platform, and network allowlists;
- no public listener by default; authenticated reverse proxy and TLS for any approved remote access;
- scoped secrets with rotation and no inheritance into tools/subprocesses;
- command approval, filesystem boundaries, sandbox escape review, and egress filtering;
- retention, backup, deletion, incident, audit, and provider-data handling policies;
- resource limits, worker/subagent/cron/Kanban concurrency bounds, and runaway controls;
- deterministic startup/shutdown, service inventory, port inventory, and emergency kill switch;
- independent P11 architecture, runtime-boundary, adoption-mode, adapter, spike, and safety approvals.

The full-feature profile is documented but not approved.

## Static Security Controls and Residual Risks

Observed static controls include exact or bounded Python dependencies, hash-bearing lock data, allowlisted lazy package specs, profile-scoped state, source-tree read-only Docker permissions, non-root container services, loopback defaults for dashboard/API, webhook-safe tool reduction, dangerous-command approval references, filesystem guards, log redaction, credential-scrub declarations for code execution, and plugin/tool availability checks.

Residual risks remain substantial:

- broad high-privilege tools are part of the core/default platform bundles;
- runtime lazy installation is enabled by default;
- remote installers and package lifecycle scripts execute downloaded code;
- user and bundled plugins can expand code, tools, hooks, network, and state;
- session storage contains full prompts, messages, reasoning, tool calls, and workspace metadata;
- gateway and webhook inputs are untrusted prompt content with paths to powerful tools;
- public listener configuration is possible;
- npm semver ranges and an unlocked Rust bootstrap dependency graph reduce reproducibility;
- optional provider SDKs add independent telemetry, credential, and supply-chain behavior;
- static controls were not exercised and must not be assumed effective;
- the restricted PowerPoint skill prevents whole-tree MIT treatment.

## Limitations

- This was a targeted static audit, not a line-by-line review of all 6,000+ allowed source files.
- No dependency tree was resolved and no complete transitive license or vulnerability report was generated.
- Lockfile presence and declared hashes were observed but not cryptographically reverified against downloaded artifacts.
- No installer, import, entrypoint, service, test, build, script, hook, package manager, or lifecycle command ran.
- No runtime behavior, resource use, shutdown, cleanup, sandbox, approval, redaction, or network control was validated.
- No credential, `.env`, user/provider configuration, OAuth state, API, MCP, browser auth, user state, or database was inspected.
- Source filenames and comments are evidence of intended behavior, not proof of deployed behavior.

## Downstream Decision

P11.1 is ready as an evidence input for P11.2-P11.4, subject to each ticket's own prerequisites and identity checks.

Downstream tickets must carry these blockers explicitly:

```text
HERMES-LIC-001: restricted PowerPoint skill license
HERMES-LIC-002: Apache-2.0 NOTICE preservation
HERMES-DEP-001: no complete dependency SBOM/license clearance
HERMES-DEP-002: runtime lazy installation enabled by default
HERMES-DEP-003: Rust bootstrap dependencies lack an observed Cargo.lock
HERMES-RUN-001: broad default high-privilege tool surface
HERMES-STATE-001: extensive sensitive persistent state
HERMES-NET-001: provider egress and optional/public listener surfaces
HERMES-OPS-001: shutdown, cleanup, and kill-switch behavior unverified
```

No adoption mode, adapter design, local spike, installation, execution, or integration is approved by P11.1.

## Change Register

Updated in place:

```text
0_architecture/governance/agent_platform_hermes_license_dependency_runtime_audit.md
```

Not created or modified by this ticket continuation:

```text
no rerun document
no identity-resolution document
no safe-block document
no marker-alignment document
no diagnostic record
no Hermes source file
no P11.2 architecture document
```

Operational boundary:

```text
Hermes installed: false
Hermes imported/executed: false
package manager/resolver run: false
dependencies or browser binaries installed: false
tests/builds/scripts/hooks/CI run: false
services/ports/daemons started: false
providers/APIs/OAuth/MCP activated: false
credentials/user state accessed: false
Hermes source modified: false
Git mutated: false
```
