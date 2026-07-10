# GStack License Dependency Skill Audit

## Summary

P12.2 completed a read-only audit of the local GStack source tree after closure of the GBrain P12.0A-P12.0E feasibility branch. The audit classified license posture, dependency posture, install lifecycle risk, skill surface, provider and credential surfaces, storage and file-write surfaces, execution surfaces, and the required controlled setup boundary.

No GStack command, setup script, package manager, runtime binary, skill, provider CLI, MCP command, browser daemon, test, build, install, credential inspection, environment secret inspection, staging command, or Git mutation was run.

Result marker:

```text
gstack_license_dependency_skill_audit_ready
```

Decision markers:

```text
gstack_source_review_readonly_complete
gstack_mit_license_confirmed
gstack_dependency_surface_classified
gstack_skill_surface_classified
gstack_provider_credential_surface_blocked
gstack_install_runtime_still_blocked
gstack_controlled_setup_plan_required
gstack_license_dependency_skill_audit_ready
```

Closure decision:

```text
GStack is license-permissible for further evaluation, but its dependency, install, skill, browser, provider, credential, hook, storage, and remote-agent surfaces are broad enough that it must remain blocked until a separate controlled setup plan is approved. P12.2 does not authorize installing GStack, running setup, enabling skills, registering hooks, launching browser daemons, importing cookies, using provider credentials, or treating GStack as an approved Graphify replacement.
```

```yaml
P12_2_GStack_Audit_Decision:
  ticket: P12.2
  date: "2026-07-10"
  outcome: "Outcome A - read-only audit complete; controlled setup required"
  source_root: "4_external/sources/gstack-main"
  package_name: "gstack"
  package_version: "1.58.5.0"
  declared_license: "MIT"
  license_file_mit: true
  top_level_bun_lock_present: true
  nested_diagram_package_present: true
  install_executed: false
  setup_executed: false
  package_manager_executed: false
  node_or_bun_runtime_executed: false
  gstack_runtime_executed: false
  gstack_skill_executed: false
  browser_daemon_executed: false
  provider_call_executed: false
  credential_or_env_secret_inspected: false
  mcp_registered_or_called: false
  git_mutation_executed: false
  runtime_allowed_now: false
  controlled_setup_plan_required: true
  final_marker: "gstack_license_dependency_skill_audit_ready"
```

## Scope

Read-only source root:

```text
4_external/sources/gstack-main
```

Dependency on prior governance closure:

```text
0_architecture/governance/agent_platform_gbrain_empty_graph_query_output_review.md
```

P12.2 scope was classification only. It did not attempt to prove runtime correctness, skill quality, Graphify replacement fitness, browser safety, provider behavior, GBrain sync behavior, or cross-agent coordination behavior.

## Files Inspected

GStack metadata and governance-relevant documentation inspected read-only:

```text
4_external/sources/gstack-main/package.json
4_external/sources/gstack-main/LICENSE
4_external/sources/gstack-main/README.md
4_external/sources/gstack-main/.gitignore
4_external/sources/gstack-main/AGENTS.md
4_external/sources/gstack-main/ARCHITECTURE.md
4_external/sources/gstack-main/BROWSER.md
4_external/sources/gstack-main/setup
4_external/sources/gstack-main/lib/diagram-render/package.json
```

Directory metadata inspected read-only:

```text
4_external/sources/gstack-main/
4_external/sources/gstack-main/**/SKILL.md
4_external/sources/gstack-main/**/SKILL.md.tmpl
```

Target file status before creation:

```text
0_architecture/governance/agent_platform_gstack_license_dependency_skill_audit.md did not exist
```

Not inspected:

```text
GStack node_modules contents
package cache contents
normal user ~/.gstack state
normal user ~/.claude state
normal user ~/.codex state
normal user ~/.config/opencode state
browser cookie stores
credential files
environment secret values
provider account configuration
MCP server runtime state
external network resources
GStack runtime-generated DBs, logs, caches, browser state, or telemetry state
```

## License Posture

Observed package metadata:

```yaml
name: "gstack"
version: "1.58.5.0"
license: "MIT"
type: "module"
bin:
  browse: "./browse/dist/browse"
  make-pdf: "./make-pdf/dist/pdf"
```

Observed license file:

```text
MIT License
Copyright (c) 2026 Garry Tan
```

Classification:

```yaml
license_permissive_for_further_evaluation: true
license_blocks_readonly_review: false
license_blocks_controlled_sandbox_plan: false
transitive_dependency_license_audit_completed: false
runtime_adoption_approved_by_license_review: false
```

Notes:

```text
The top-level GStack license is permissive MIT. P12.2 did not perform a full transitive dependency license audit because no install, package manager, node_modules traversal, SBOM generation, or external registry lookup was allowed.
```

## Dependency Posture

Top-level dependency set observed in `package.json`:

```yaml
runtime_dependencies:
  - "@huggingface/transformers: ^4.1.0"
  - "@ngrok/ngrok: ^1.7.0"
  - "diff: ^7.0.0"
  - "html-to-docx: 1.8.0"
  - "marked: ^18.0.2"
  - "playwright: ^1.58.2"
  - "puppeteer-core: ^24.40.0"
  - "socks: ^2.8.8"
dev_dependencies:
  - "@anthropic-ai/claude-agent-sdk: 0.2.117"
  - "@anthropic-ai/sdk: ^0.78.0"
  - "xterm: 5"
  - "xterm-addon-fit: ^0.8.0"
engine:
  bun: ">=1.0.0"
lockfile_present: true
```

Nested diagram-render package observed:

```yaml
package: "@gstack/diagram-render"
private: true
dependencies:
  - "@excalidraw/excalidraw: 0.18.0"
  - "@excalidraw/mermaid-to-excalidraw: 1.1.2"
  - "mermaid: 11.12.2"
  - "react: 18.3.1"
  - "react-dom: 18.3.1"
```

Dependency risk classification:

```yaml
browser_automation_dependency_surface: high
network_tunnel_dependency_surface: high
provider_sdk_dependency_surface: medium
local_ml_model_dependency_surface: medium
document_rendering_dependency_surface: medium
transitive_supply_chain_surface: unvalidated
package_install_allowed_now: false
```

Rationale:

```text
The dependency set includes browser automation, Chromium access, ngrok tunneling, provider SDKs, local ML/model loading, document conversion, terminal UI assets, and nested diagram rendering dependencies. These are not inherently disqualifying, but they require a controlled install plan and transitive dependency review before any runtime use.
```

## Package Scripts And Lifecycle Surface

Observed top-level scripts include build, browser/server development, diagram build, skill doc generation, test suites, eval suites, analytics, audit test, slop scan, and background eval helpers.

Representative surfaces:

```text
build: bash scripts/build.sh
server/start: bun run browse/src/server.ts
test/evals: bun test with multiple e2e/eval targets
slop: npx slop-scan scan .
build:diagram-render: cd lib/diagram-render && bun install && bun run scripts/build.ts
```

Classification:

```yaml
top_level_preinstall_postinstall_script_observed: false
setup_script_invokes_package_install: true
setup_script_invokes_build: true
setup_script_invokes_skill_generation: true
package_scripts_execute_shell_or_bun: true
package_scripts_allowed_now: false
```

## Install Lifecycle Risk

The README quick start asks an agent to clone GStack into a user skill directory and run setup:

```text
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup
```

The setup script was reviewed read-only and classified as broad lifecycle code. Observed setup behaviors include:

```text
checks for bun and prints curl-based Bun install guidance
detects host targets including claude, codex, kiro, factory, opencode, openclaw, hermes, and gbrain
can write or link skills into ~/.claude/skills, ~/.codex/skills, ~/.factory/skills, ~/.kiro/skills, and ~/.config/opencode/skills
runs bun install and bun run build when rebuild is needed
runs bun run gen:skill-docs for generated skill docs
runs bunx playwright install chromium when Chromium is missing
on Windows, can use node and npm install --no-save playwright / @ngrok/ngrok checks
on Linux, can attempt apt-get, dnf, pacman, or apk font installation unless skipped
on macOS, can attempt Homebrew coreutils installation unless skipped
can run migration shell scripts under gstack-upgrade/migrations
can write ~/.gstack version and welcome markers
can add or remove Claude settings hooks in team or plan-tune flows
can detect GBrain and regenerate brain-aware skills
can print or enable credential pre-push guard hints through config
```

Install classification:

```yaml
setup_safe_to_run_without_plan: false
setup_requires_human_approval: true
setup_requires_sandboxed_state_paths: true
setup_requires_network_decision: true
setup_requires_hook_decision: true
setup_requires_provider_key_absence: true
setup_requires_cookie_import_block: true
team_mode_allowed_now: false
auto_upgrade_allowed_now: false
```

## Skill Surface

GStack contains many generated and template-backed skill surfaces. AGENTS.md groups them into plan review, implementation/review, release/deploy, operational/memory, browser/agent integration, iOS QA, and safety/scoping groups.

Observed skill categories:

```text
planning and product review: /office-hours, /plan-ceo-review, /plan-eng-review, /plan-design-review, /plan-devex-review, /autoplan, /spec
implementation and review: /review, /codex, /investigate, /design-review, /devex-review, /qa, /qa-only, /scrape, /skillify
release and deploy: /ship, /land-and-deploy, /canary, /document-release, /document-generate, /setup-deploy, /gstack-upgrade
memory and operations: /context-save, /context-restore, /learn, /retro, /health, /benchmark, /benchmark-models, /cso, /setup-gbrain, /sync-gbrain
browser and agent integration: /browse, /open-gstack-browser, /setup-browser-cookies, /pair-agent
iOS QA: /ios-qa, /ios-fix, /ios-design-review, /ios-clean, /ios-sync
safety and scoping: /careful, /freeze, /guard, /unfreeze, /make-pdf, /diagram
```

Skill classification:

```yaml
skill_markdown_present: true
skill_templates_present: true
skill_execution_allowed_now: false
skills_can_instruct_file_writes: true
skills_can_instruct_git_operations: true
skills_can_instruct_browser_use: true
skills_can_instruct_provider_cli_use: true
skills_can_instruct_gbrain_setup_or_sync: true
skills_can_instruct_cookie_import: true
```

Governance note:

```text
The skills are operational prompts, not passive documentation. They can direct agents to run tests, edit files, use Git, launch browsers, import cookies, open tunnels, call provider CLIs, write memory, or register integrations. They must remain inactive until a controlled setup and permission model exists.
```

## Browser Runtime And Remote Agent Surface

Architecture documentation describes a persistent browser daemon:

```text
long-lived Chromium daemon
localhost HTTP server via Bun.serve
state file at .gstack/browse.json with pid, port, token, and version metadata
random localhost port range
Playwright/Chromium browser control through CDP
logs flushed to .gstack/*.log
```

Remote and browser integration surfaces observed:

```text
pair-agent can use ngrok tunnel behavior for remote agents
dual local/tunnel listeners are documented
root token, setup key, and scoped token model is documented
SSE session cookie and PTY session cookie are documented
cookie import from installed browsers is documented
sidebar agent can use Bash, Read, Glob, Grep, and WebFetch style tools
raw CDP escape hatch is documented with an allowlist model
```

Runtime classification:

```yaml
browser_daemon_allowed_now: false
local_http_runtime_allowed_now: false
ngrok_tunnel_allowed_now: false
remote_agent_pairing_allowed_now: false
cookie_import_allowed_now: false
raw_cdp_allowed_now: false
sidebar_agent_allowed_now: false
```

## Provider, MCP, Credential, And Environment Surface

Observed provider/tool references include:

```text
Claude Code and Claude PTY integration
OpenAI Codex CLI via /codex and benchmark paths
Gemini benchmark references
Anthropic SDK dependencies
GBrain setup and sync integration
Supabase setup paths and telemetry storage references
OpenClaw, Hermes, Codex, Cursor, Factory, Kiro, Slate, OpenCode host surfaces
```

Observed MCP references include:

```text
README guidance to avoid mcp__claude-in-chrome__* tools when using /browse
/setup-gbrain option to register gbrain as an MCP server for Claude Code
remote gbrain MCP path with URL and bearer token
Claude hook matcher for mcp__.*__AskUserQuestion in plan-tune flows
```

Observed credential and environment references include:

```text
browser cookies and cookie import
bearer tokens and scoped tokens for browser daemon/pair-agent
Supabase Personal Access Token path for GBrain setup
remote gbrain MCP URL and bearer token path
GSTACK_ANTHROPIC_API_KEY and GSTACK_OPENAI_API_KEY promotion path for Conductor
BROWSE_PROXY_USER and BROWSE_PROXY_PASS proxy credential path
GSTACK_HOME, CLAUDE_PLUGIN_DATA, CLAUDE_PLANS_DIR state path controls
GSTACK_SECURITY_OFF and GSTACK_SECURITY_ENSEMBLE security/model controls
```

Classification:

```yaml
provider_surface_present: true
mcp_surface_present: true
credential_surface_present: true
environment_knob_surface_present: true
credential_inspection_allowed_now: false
provider_calls_allowed_now: false
mcp_registration_allowed_now: false
```

## Storage, Cache, File Write, And Git Surface

Observed storage and write surfaces include:

```text
project .gstack/ browser state, logs, domain skills, browser skills, and saved browser state
global ~/.gstack config, analytics, sessions, security logs, model caches, and device salt
skill installation paths under ~/.claude, ~/.codex, ~/.factory, ~/.kiro, and ~/.config/opencode
generated .agents, .factory, .opencode, .gbrain, and related source-tree artifacts
browser-skill staging under ~/.gstack/.tmp/skillify-*
GBrain detection state under ~/.gstack/gbrain-detection.json
Claude settings hook writes through gstack-settings-hook flows
local analytics and telemetry staging JSONL files
team mode bootstrap instructions that include git add and git commit
continuous checkpoint mode that can auto-commit WIP changes when enabled
```

Observed `.gitignore` confirms local artifact exclusions for:

```text
.env
node_modules/
dist/
.gstack/
.claude/skills/
.agents/
.factory/
.kiro/
.opencode/
.openclaw/
.hermes/
.gbrain/
extension/.auth.json
.gstack-worktrees/
/tmp/
*.log
.sources/
```

Classification:

```yaml
file_write_surface_present: true
global_user_state_surface_present: true
project_local_state_surface_present: true
hook_mutation_surface_present: true
git_mutation_surface_present_in_skills_or_docs: true
file_write_allowed_now: false
git_mutation_allowed_now: false
```

## Execution Surface

Observed execution mechanisms include:

```text
setup shell execution
bun install and bun run commands
bunx playwright install chromium
node and npm fallback checks on Windows
system package manager calls for fonts on Linux
Homebrew call for coreutils on macOS
compiled browse and make-pdf binaries
Bun.serve HTTP server
Playwright/Chromium process launch
Bun.spawn and shell/subprocess references in source/docs
Claude/Codex/Gemini provider command paths
migration scripts under gstack-upgrade/migrations
Claude settings hooks and plan-tune hooks
remote agent tunnel flows
```

Classification:

```yaml
local_process_execution_surface: high
network_execution_surface: high
browser_execution_surface: high
agent_tool_execution_surface: high
execution_allowed_now: false
```

## Controlled Setup Handoff Requirements

Any future GStack setup ticket must be a separate approved plan. Minimum requirements:

```text
choose one host target explicitly instead of auto-detecting all hosts
force non-interactive setup flags where available
disable team mode and auto-upgrade for first evaluation
disable plan-tune hook installation unless explicitly approved
pin GSTACK_HOME and any writable state to an approved sandbox path
block cookie import, pair-agent, ngrok tunnel, browser daemon, and sidebar agent for first pass
run with no provider keys, no Supabase token, no gbrain MCP bearer token, and no proxy credentials
block telemetry or set it off before any runtime path that can ask or write state
avoid modifying user ~/.claude, ~/.codex, ~/.config/opencode, ~/.gstack unless explicitly approved
avoid Git add, commit, push, hooks, or checkpoint mode unless explicitly approved
record exact commands before execution
record all generated files and directories after execution
```

Candidate next governance ticket:

```text
P12.3 - GStack Controlled Setup Boundary Plan
```

## Runtime Boundary

Current allowed state after P12.2:

```yaml
read_gstack_source_for_governance: true
reference_gstack_license_metadata: true
draft_controlled_setup_plan: true
install_gstack: false
run_gstack_setup: false
run_bun_or_node_for_gstack: false
run_package_manager_for_gstack: false
launch_gstack_browser: false
execute_gstack_skill: false
import_browser_cookies: false
start_ngrok_or_pair_agent: false
register_mcp: false
call_provider_cli_or_api: false
write_user_skill_dirs: false
write_user_gstack_state: false
mutate_git: false
approve_graphify_replacement: false
```

## Evidence Limits

P12.2 did not validate:

```text
runtime safety
setup idempotence
dependency install reproducibility
transitive dependency licenses
browser daemon auth behavior
ngrok tunnel behavior
cookie import behavior
provider CLI behavior
GBrain setup/sync behavior
MCP registration behavior
hook rollback behavior
telemetry behavior
skill correctness
Windows runtime behavior
Graphify replacement quality
```

## Files Created

Created this governance audit record:

```text
0_architecture/governance/agent_platform_gstack_license_dependency_skill_audit.md
```

## Files Modified

No existing file was modified by P12.2.

## Commands And Runtime Not Run

Explicitly not run:

```text
no ./setup
no gstack command
no browse command
no make-pdf command
no skill command
no bun install
no bun run
no bun test
no bunx
no npm
no npx
no node
no python
no pip
no cargo
no go
no deno
no docker
no ollama
no graphify
no provider CLI
no MCP registration
no browser daemon
no ngrok tunnel
no cookie import
no credential or environment secret inspection
no Git mutation
no staging command
```

## Final Status

P12.2 is complete as a read-only audit.

Final marker:

```text
gstack_license_dependency_skill_audit_ready
```
