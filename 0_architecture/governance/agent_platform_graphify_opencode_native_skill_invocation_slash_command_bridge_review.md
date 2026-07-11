# Graphify OpenCode Native Skill Invocation / Slash-Command Bridge Review

## Summary

P10.5I-A completed a static OpenCode/Graphify invocation-mechanism review and exactly one authorized native skill-load probe.

Decision outcome:

```text
Outcome A - native skill invocation verified
```

The installed project-local Graphify Agent Skill has valid frontmatter, a matching directory name, the expected reference sidecars, and is discoverable by OpenCode's native `skill` tool. The exact probe `skill({ name: "graphify" })` succeeded without a permission prompt or denial and loaded the Graphify instructions into GPT-5.6 context.

No instruction returned by the loaded skill was executed. No Graphify command, detection, extraction, subagent, build, report, export, output write, model inference, or slash command was run.

Static review also confirms that Graphify `0.9.5` installs an OpenCode skill, AGENTS guidance, and an auto-discovered reminder plugin, but does not create an OpenCode custom command file. The project has no `.opencode/commands/graphify.md` or `.opencode/command/graphify.md`. The advertised `/graphify` syntax in Graphify's skill text therefore does not itself establish a registered OpenCode slash command.

The selected next path is native skill controlled execution. A slash-command bridge is deferred until native runtime validation succeeds.

Result marker:

```text
graphify_opencode_native_skill_invocation_slash_command_bridge_review_ready
```

Decision markers:

```text
graphify_opencode_skill_path_valid
graphify_opencode_skill_frontmatter_valid
graphify_opencode_skill_name_directory_match
graphify_opencode_project_plugin_path_remediation_verified
graphify_opencode_slash_command_bridge_absent_confirmed
graphify_opencode_native_skill_load_verified
graphify_native_skill_path_selected
graphify_slash_bridge_deferred_until_native_runtime_validation
p10_5i_b_native_skill_controlled_execution_ready
```

```yaml
P10_5I_A_Graphify_OpenCode_Native_Skill_Invocation_Slash_Command_Bridge_Review:
  ticket: "P10.5I-A"
  date: "2026-07-11"
  status: "diagnostic_review_with_single_skill_load_probe"
  outcome: "Outcome A - native skill invocation verified"
  output_file: "0_architecture/governance/agent_platform_graphify_opencode_native_skill_invocation_slash_command_bridge_review.md"
  explicit_human_approval_present: true
  p10_5h_dependency_confirmed: true
  p10_ollama_model_dependency_confirmed: true
  p10_5i_dependency_confirmed: true
  opencode_executable: "C:\\Users\\pablo\\AppData\\Roaming\\npm\\opencode.ps1"
  opencode_version: "1.17.18"
  graphify_executable: "C:\\Users\\pablo\\anaconda3\\Scripts\\graphify.exe"
  graphify_package: "C:\\Users\\pablo\\anaconda3\\Lib\\site-packages\\graphify\\__init__.py"
  graphify_distribution_version: "0.9.5"
  graphify_skill_path: ".opencode/skills/graphify/SKILL.md"
  graphify_skill_frontmatter_valid: true
  graphify_skill_name: "graphify"
  graphify_skill_description_nonempty: true
  graphify_skill_name_directory_match: true
  graphify_reference_sidecar_present: true
  graphify_plugin_present: true
  graphify_plugin_hook: "tool.execute.before"
  graphify_plugin_is_skill_loader: false
  graphify_plugin_is_slash_command: false
  graphify_project_plural_command_file_present: false
  graphify_project_singular_command_file_present: false
  graphify_inline_command_marker_found_in_project_config: false
  graphify_redundant_plugin_marker_found_in_project_config: false
  graphify_duplicate_opencode_path_marker_found_in_project_config: false
  opencode_startup_after_plugin_remediation_user_attested: true
  native_skill_probe_authorized: true
  native_skill_probe_count: 1
  native_skill_probe_name: "graphify"
  native_skill_tool_available: true
  native_skill_discovered: true
  native_skill_load_succeeded: true
  native_skill_permission_requested: false
  native_skill_permission_denied: false
  loaded_skill_identified_as_graphify: true
  loaded_skill_base_directory_resolved: true
  loaded_skill_sidecars_named: true
  loaded_skill_workflow_executed: false
  graphify_runtime_executed: false
  ollama_model_executed: false
  subagent_dispatched: false
  graphify_output_written: false
  command_bridge_created: false
  selected_next_path: "native skill controlled execution"
  selected_next_ticket: "P10.5I-B - Graphify OpenCode Native Skill Reduced-Scope Controlled Execution"
  git_mutated: false
  final_marker: "graphify_opencode_native_skill_invocation_slash_command_bridge_review_ready"
```

## Files Inspected

Governance dependencies inspected by marker search:

```text
0_architecture/governance/agent_platform_graphify_opencode_explicit_current_session_subagent_routing_retry_record.md
0_architecture/governance/agent_platform_ollama_agentic_skill_model_selection_pull_record.md
0_architecture/governance/agent_platform_graphify_opencode_qwen3_5_9b_context_reduced_scope_execution_record.md
```

Project-local integration inspected within the approved bounds:

```text
.opencode/skills/graphify/SKILL.md
.opencode/skills/graphify/.graphify_version
.opencode/skills/graphify/references/extraction-spec.md
.opencode/plugins/graphify.js
.opencode/opencode.json targeted key/path markers only
AGENTS.md Graphify-owned section only
```

Installed Graphify package source inspected within the approved routing/install bounds:

```text
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\__main__.py
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\skill-opencode.md
```

No provider values, model configuration values, credentials, `.env`, token stores, normal-user application configuration, Graphify outputs, product paths, external sources, or artifacts were inspected.

## Files Created

Created exactly one governance review:

```text
0_architecture/governance/agent_platform_graphify_opencode_native_skill_invocation_slash_command_bridge_review.md
```

## Files Modified

No existing file was modified by P10.5I-A.

Specifically not modified:

```text
.opencode/**
AGENTS.md
OpenCode configuration
Graphify package source
.graphifyignore
.gitignore
graphify-out/**
Git index or history
```

## Commands Run

Read-only path and metadata checks:

```text
Test-Path for approved project integration and command paths
Get-Item metadata for approved project integration paths
targeted project-config marker search
git status --short
```

OpenCode metadata/help commands:

```text
Get-Command opencode -ErrorAction SilentlyContinue
opencode --version
opencode --help
opencode debug --help
```

Graphify executable/package metadata commands:

```text
Get-Command graphify -ErrorAction SilentlyContinue
C:\Users\pablo\anaconda3\python.exe -c "import graphify; print(graphify.__file__)"
C:\Users\pablo\anaconda3\python.exe -c "import importlib.metadata as m; print(m.version('graphifyy'))"
```

Exactly one native OpenCode skill-load probe:

```text
skill({ name: "graphify" })
```

Explicitly not run:

```text
/graphify
/graphify .
graphify detect
graphify extract
graphify build
graphify install
graphify update
graphify query
graphify path
graphify explain
qwen3.5 inference
qwen2.5 inference
ollama run
ollama pull
ollama serve
OpenCode subagents
tests
builds
CI
MCP servers
graph database commands
Git hooks
git add
git commit
git push
```

## Human Approval Status

Explicit approval existed outside the ticket body for exactly one native skill-load probe using the exact name `graphify`.

The approval covered only discovery and loading of the Graphify skill instructions into GPT-5.6 context. It did not authorize following the loaded instructions.

No approval existed for Graphify runtime, model inference, subagents, corpus reads, output writes, slash-command execution, command-bridge creation, configuration mutation, or Git mutation.

## P10.5I Dependency Status

P10.5I record exists and required markers were confirmed:

```text
ollama_qwen3_5_9b_context_64k_verified
ollama_qwen3_5_9b_gpu_runtime_verified
opencode_qwen3_5_9b_readiness_verified
graphify_opencode_skill_tool_not_invoked
graphify_qwen3_5_9b_agentic_capability_not_yet_determined
graphify_reduced_scope_outputs_absent
```

P10.5I established that qwen3.5 context/GPU readiness passed but plain-text `/graphify` routing did not invoke the native skill. P10.5I-A closes that invocation-mechanism uncertainty by verifying native skill discovery directly.

## OpenCode Version/Help Status

OpenCode executable:

```text
C:\Users\pablo\AppData\Roaming\npm\opencode.ps1
```

Version:

```text
1.17.18
```

`opencode --help` exposed the general TUI/run/debug surfaces.

`opencode debug --help` exposed:

```text
opencode debug skill - list all available skills
```

This confirms current OpenCode has a native skill-discovery model distinct from custom command registration.

No unsupported help subcommand was improvised.

## Project Plugin-Path Remediation Status

The plugin exists at the auto-discovery path:

```text
.opencode/plugins/graphify.js
```

Bounded plugin inspection confirms:

```text
named export: GraphifyPlugin
hook: tool.execute.before
behavior: inject a one-time bash-output reminder when graphify-out/graph.json exists
```

The plugin does not load the Graphify skill and does not register `/graphify`.

Targeted project-config marker search returned no matches for:

```text
"plugin"
.opencode/plugins/graphify.js
.opencode/.opencode
```

It also returned no `command`, `graphify`, `permission`, or `skill` control marker. No provider/model values were inspected.

The user attested that OpenCode starts successfully after removing the redundant explicit plugin registration that had resolved as `.opencode/.opencode/plugins/graphify.js`.

Marker:

```text
graphify_opencode_project_plugin_path_remediation_verified
```

## Graphify Skill Path Status

Path metadata:

| Path | Exists | Length |
| --- | --- | ---: |
| `.opencode/skills/graphify/SKILL.md` | yes | 37477 |
| `.opencode/skills/graphify/.graphify_version` | yes | 5 |
| `.opencode/skills/graphify/references/extraction-spec.md` | yes | 7960 |

The containing directory is named `graphify`, matching the declared skill name.

Marker:

```text
graphify_opencode_skill_path_valid
```

## Graphify Skill Frontmatter Validation

The initial bounded frontmatter block is:

```yaml
---
name: graphify
description: "Use for any question about a codebase, its architecture, file relationships, or project content ..."
---
```

Validation results:

```text
opening delimiter present
closing delimiter present
name present
name exactly graphify
name lowercase and valid
description present and non-empty
directory name matches declared name
```

Markers:

```text
graphify_opencode_skill_frontmatter_valid
graphify_opencode_skill_name_directory_match
```

## OpenCode Native Skill Discovery Model

OpenCode treats project files under:

```text
.opencode/skills/<name>/SKILL.md
```

as native Agent Skills discoverable and loadable through the `skill` tool.

This mechanism is distinct from:

```text
custom slash commands under .opencode/commands or command configuration
plugins under .opencode/plugins
AGENTS.md always-on guidance
```

The native skill tool loads reusable instructions into the current agent context. Loading does not itself execute the instructions.

## Native Skill-Load Probe Result

Exactly one probe was performed:

```text
skill({ name: "graphify" })
```

Result:

```text
skill tool exists: yes
load succeeded: yes
permission requested: no
permission denied: no
returned skill identifies itself as Graphify: yes
base directory resolved: yes
reference sidecars named: yes
workflow executed: no
```

The returned content identified:

```text
Skill: graphify
Base directory: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\.opencode\skills\graphify
```

It named the expected reference sidecars:

```text
references/add-watch.md
references/exports.md
references/extraction-spec.md
references/github-and-merge.md
references/hooks.md
references/query.md
references/transcribe.md
references/update.md
```

No loaded instruction was followed.

Marker:

```text
graphify_opencode_native_skill_load_verified
```

The probe is invocation-mechanism evidence only. It is not Graphify runtime validation or model capability validation.

## Slash-Command Registration Status

Project command directory/path metadata:

```text
.opencode/commands: absent
.opencode/commands/graphify.md: absent
.opencode/command/graphify.md: absent
```

Targeted project-config marker search found no top-level `command` or `graphify` marker.

Classification:

```text
native Graphify skill: present
Graphify plugin: present
Graphify slash-command bridge: absent
```

Marker:

```text
graphify_opencode_slash_command_bridge_absent_confirmed
```

The absence is material to `/graphify` UX but does not block native skill-tool invocation.

## Plugin Versus Skill Versus Command Classification

| Mechanism | Present | Purpose | Executes Graphify by itself |
| --- | --- | --- | --- |
| Agent Skill | yes | Reusable Graphify instructions loaded through native `skill` tool | no; load only |
| Custom Command | no | Would map `/graphify` and `$ARGUMENTS` to a prompt template | not present |
| Plugin | yes | One-time bash reminder when a graph already exists | no |
| AGENTS.md | yes | Always-on instruction to use Graphify when appropriate | no deterministic command registration |

The previous failures occurred because text beginning `/graphify` was not proven to invoke the native skill tool. The native probe now proves direct skill loading works.

## Installed Graphify Package Behavior

Resolved package:

```text
executable: C:\Users\pablo\anaconda3\Scripts\graphify.exe
package: C:\Users\pablo\anaconda3\Lib\site-packages\graphify\__init__.py
distribution: graphifyy 0.9.5
```

Bounded source findings:

```text
OpenCode project skill destination is .opencode/skills/graphify/SKILL.md.
The packaged OpenCode skill source is skill-opencode.md.
OpenCode references are installed alongside the skill.
Project installation writes/updates AGENTS.md.
Project installation writes .opencode/plugins/graphify.js.
Project installation attempts explicit registration in .opencode/opencode.json.
No OpenCode command file creation path was found.
Command-file creation exists for another platform (Kilo), showing commands are handled explicitly where implemented.
```

The installed skill advertises `/graphify` syntax and OpenCode `@mention` semantic dispatch. Graphify `0.9.5` appears to assume that OpenCode/agent routing will map the advertised slash syntax to the installed skill instructions, but its installer does not create the custom command artifact required for deterministic `/graphify` UX in current OpenCode.

Current OpenCode semantics distinguish native skill loading from custom slash commands. The native skill path is compatible and verified; the advertised slash syntax is not registered by the package install.

## Slash-Command Bridge Candidate

Candidate path, design only:

```text
.opencode/commands/graphify.md
```

Candidate draft:

```markdown
---
description: Run the installed Graphify skill for an explicitly supplied path
agent: build
---

Load the native OpenCode skill named `graphify` using the `skill` tool before taking any other action.

After the skill has loaded, execute its Graphify build workflow for exactly:

$ARGUMENTS

Do not substitute a generic repository exploration or summary for the Graphify workflow.
Do not expand the input beyond the supplied path.
Do not use a hosted provider unless separately authorized.
```

Classification:

```text
candidate bridge only
not installed
not runtime-authorized
not yet validated
```

The bridge is compatible in principle with current OpenCode command semantics because it uses a project command file, a prompt body, and `$ARGUMENTS`. However, native controlled execution should be validated before introducing this additional artifact.

## Decision Outcome

Selected outcome:

```text
Outcome A - native skill invocation verified
```

Requirements satisfied:

```text
frontmatter valid
skill discovered
native skill tool available
skill({ name: "graphify" }) succeeded
no permission block
no Graphify workflow executed
```

The native mechanism closes the core invocation question. A command bridge is useful only for slash UX and is not required to prove native skill execution.

## Selected Next Path

Exactly one next path is selected:

```text
native skill controlled execution
```

Selected next ticket:

```text
P10.5I-B - Graphify OpenCode Native Skill Reduced-Scope Controlled Execution
```

Markers:

```text
graphify_native_skill_path_selected
graphify_slash_bridge_deferred_until_native_runtime_validation
p10_5i_b_native_skill_controlled_execution_ready
```

The next ticket should invoke the native Graphify skill explicitly, provide the exact reduced path after successful load, and preserve the existing local qwen3.5/context/provider boundaries. It must not use another plain-text `/graphify` retry.

## Authority Classification

The native skill-load result is invocation-mechanism evidence only.

It is not:

```text
Graphify runtime validation
qwen3.5 capability validation
subagent validation
graph-output validation
authority
approval
source of truth
```

The candidate bridge is design evidence only, not installed, not runtime-authorized, and not architecture authority.

Graphify remains an evidence-map, visualization, and report candidate, not source of truth, approval, runtime authority, memory authority, or Cognitive Semantic System substrate.

## Created / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_graphify_opencode_native_skill_invocation_slash_command_bridge_review.md
```

Not created, modified, run, or approved:

```text
.opencode/commands/graphify.md
.opencode modification
AGENTS.md modification
Graphify reinstall or update
/graphify
/graphify .
Graphify detection
Graphify extraction
Graphify subagents
Graphify build
Graphify report
Graphify export
qwen3.5 inference
qwen2.5 inference
graph.json
graph.html
GRAPH_REPORT.md
provider change
credential inspection
output cleanup
output tracking
Git mutation
git add .
```

## Limitations

The native probe loaded the full skill text into GPT-5.6 context because that is the behavior being tested. It did not execute the text.

No native controlled Graphify runtime has yet been performed. The review therefore does not establish that qwen3.5 follows the loaded skill, dispatches OpenCode subagents, emits valid semantic JSON, or completes a graph build.

The targeted project-config marker search established no relevant project-local keys, but no normal-user configuration or merged resolved configuration was inspected.

The candidate bridge has not been installed or validated. Its exact execution behavior remains subject to a separate gate if native controlled execution later demonstrates a need for slash UX.

## Commit Commands

No Git mutation command was run. If this review is accepted, stage only this governance file:

```powershell
git status --short

git add 0_architecture/governance/agent_platform_graphify_opencode_native_skill_invocation_slash_command_bridge_review.md

git commit -m "Review Graphify OpenCode native skill invocation"

git push
```

Do not stage:

```text
.opencode/**
AGENTS.md
graphify-out/**
0_architecture/implementation/graphify_command_candidate_confirmation.md
```

Do not use `git add .`.

## Final Declaration

P10.5I-A verified that OpenCode `1.17.18` discovers and loads the project-local Graphify Agent Skill through the native `skill` tool. Graphify `0.9.5` does not install an OpenCode slash-command bridge, and the reminder plugin is neither a skill loader nor a command. Native skill controlled execution is selected as the single next path; slash-command bridge work is deferred until native runtime validation.

Final marker:

```text
graphify_opencode_native_skill_invocation_slash_command_bridge_review_ready
```
