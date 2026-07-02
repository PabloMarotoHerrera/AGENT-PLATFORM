# Agent Runtime Boundary

## Allowed Implementation
Allowed implementation is one minimal Python standard-library module that models agent descriptors, capabilities, task envelopes, and handoff records in memory, plus documentation that describes its boundaries.

## Forbidden Implementation
Forbidden implementation includes package manifests, lockfiles, tests, scripts, tools, CI, runners, CLI, runtime services, schedulers, worker loops, queues, orchestration engines, agent execution, task execution, handoff execution, tool execution, provider clients, API clients, provider configs, adapter configs, MCP configs, credential stores, validation execution, security enforcement, product activation, and CSS prototype artifacts.

## No Agent Activation
Agent registration is not agent activation. Agent availability is not runtime approval.

## No Task Execution
Task envelope creation is not task execution.

## No Handoff Execution
Handoff record creation is not handoff execution.

## No Tool Execution
Capability registration is not tool permission. Tool references are metadata only.

## No Provider/API/MCP Activation
Provider/adapter references are metadata only. No provider, adapter, API, network, authentication, or MCP activation occurs.

## No Runtime Service
No scheduler, worker loop, queue, event loop, orchestration engine, runtime service, or agent process is created.

## No External Dependencies
The boundary uses Python standard library only. No agent framework, orchestration framework, workflow engine, queue, scheduler, provider SDK, package manifest, lockfile, or package manager is introduced.

## No Product Activation
Products remain inactive. Product source remains local-only and is not copied into the boundary.

## No CSS Substrate Decision
Cognitive Semantic System remains the accepted name. Substrate remains deferred. Graph remains candidate only. The boundary does not decide substrate.

## Stop Rules
Stop if work requires target overwrite, agent activation, task execution, handoff execution, tool execution, provider/API/MCP activation, credential inspection, auth, API calls, network calls, package files, dependencies, test execution, product source inspection, existing `3_platform` inspection, CSS substrate selection, Git mutation, or I-06 start.
