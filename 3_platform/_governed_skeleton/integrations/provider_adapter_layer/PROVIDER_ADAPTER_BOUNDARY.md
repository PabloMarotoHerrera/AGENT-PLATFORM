# Provider / Adapter Boundary

## Allowed Implementation
Allowed implementation is one minimal Python standard-library module that models provider descriptors, adapter descriptors, and adapter capabilities in memory, plus documentation that describes its boundaries.

## Forbidden Implementation
Forbidden implementation includes package manifests, lockfiles, tests, scripts, tools, CI, runners, CLI, runtime services, persistence, provider clients, API clients, provider configs, adapter configs, MCP configs, credential stores, network calls, authentication flows, provider activation, adapter activation, product activation, validation execution, security enforcement, and CSS prototype artifacts.

## No Provider Activation
Provider registration is not provider activation. Provider availability is not provider permission. Provider credentials are not provider permission.

## No Adapter Activation
Adapter registration is not adapter activation. Capability registration is not tool execution.

## No API/Network/Auth
The layer does not perform API calls, network calls, provider calls, package registry calls, authentication flows, or external service calls.

## No Credential Inspection
The layer does not inspect credentials, tokens, sessions, cookies, API keys, provider configs, auth stores, or local credential stores. Credential references are metadata IDs only.

## No MCP Activation
MCP availability is not MCP activation. MCP adapter metadata does not start, connect, register, list, authenticate, or invoke MCP servers, tools, or resources.

## No External Dependencies
The layer uses Python standard library only. No provider SDKs, client libraries, package manifests, lockfiles, or package managers are introduced.

## No Product Activation
Products remain inactive. Product source remains local-only and is not copied into the layer.

## No CSS Substrate Decision
Cognitive Semantic System remains the accepted name. Substrate remains deferred. Graph remains candidate only. The layer does not decide substrate.

## Stop Rules
Stop if work requires target overwrite, provider activation, adapter activation, MCP activation, credential inspection, auth, API calls, network calls, package files, dependencies, test execution, product source inspection, existing `3_platform` inspection, CSS substrate selection, Git mutation, or I-05 start.
