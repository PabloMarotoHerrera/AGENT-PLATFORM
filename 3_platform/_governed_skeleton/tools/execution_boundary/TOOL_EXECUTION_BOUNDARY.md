# Tool Execution Boundary

## Allowed Implementation
Allowed implementation is one minimal Python standard-library module that models tool descriptors, capabilities, execution requests, and execution decisions in memory, plus documentation that describes its boundaries.

## Forbidden Implementation
Forbidden implementation includes package manifests, lockfiles, tests, scripts, tools, CI, runners, CLI, runtime services, schedulers, worker loops, queues, tool executors, shell runners, filesystem guards, network clients, provider clients, API clients, MCP configs, credential stores, package manager wrappers, build runners, test runners, Git mutation wrappers, validation execution, security enforcement, product activation, and CSS prototype artifacts.

## No Tool Activation
Tool registration is not tool activation. Tool availability is not permission.

## No Tool Execution
Execution request creation is not execution approval. Execution decision metadata is not execution authorization.

## No Shell/subprocess
Shell availability is not command approval. No shell or subprocess execution occurs.

## No Filesystem Read/write
No file or directory is read, written, scanned, copied, moved, deleted, archived, normalized, or transformed by the boundary.

## No Network/API
No network calls, API calls, package registry calls, provider calls, authentication flows, or external service calls occur.

## No Credential Inspection
The boundary does not inspect credentials, tokens, sessions, cookies, API keys, provider configs, auth stores, process variables, or local credential stores.

## No Provider/API/MCP Activation
Provider, adapter, and MCP references are metadata only. MCP tool availability is not MCP activation.

## No Runtime Service
No scheduler, worker loop, queue, event loop, orchestration engine, runtime service, or tool process is created.

## No External Dependencies
The boundary uses Python standard library only. No tool framework, automation framework, package manager, build system, test runner, SDK, package manifest, lockfile, or package manager is introduced.

## No Product Activation
Products remain inactive. Product source remains local-only and is not copied into the boundary.

## No CSS Substrate Decision
Cognitive Semantic System remains the accepted name. Substrate remains deferred. Graph remains candidate only. The boundary does not decide substrate.

## Stop Rules
Stop if work requires target overwrite, tool activation, tool execution, shell/subprocess execution, filesystem read/write, network/API calls, provider/API/MCP activation, credential inspection, auth, package files, dependencies, test execution, product source inspection, existing `3_platform` inspection, CSS substrate selection, Git mutation, or I-07 start.
