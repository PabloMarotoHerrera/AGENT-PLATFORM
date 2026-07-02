# Validation Registry Boundary

## Allowed Implementation
Allowed implementation is one minimal Python standard-library module that models validation records in memory and documentation that describes its boundaries.

## Forbidden Implementation
Forbidden implementation includes package manifests, lockfiles, tests, scripts, tools, CI, runners, CLI, services, persistence, schemas, databases, validation execution, security enforcement, providers, adapters, MCP, product activation, and CSS prototype artifacts.

## No Execution
The registry does not execute validation, tests, scans, scripts, tools, products, solvers, SDKs, native binaries, providers, APIs, MCP, network calls, or authentication flows.

## No Approval Semantics
Validation registry status is not governance approval. Proof level is not authorization. Validation evaluates; governance decides.

## No Enforcement
The registry does not enforce validation, security, access control, source tracking, dependency rules, publication rules, or product activation rules.

## No Persistence
The registry stores records in memory only. No filesystem, database, cache, graph, vector, ontology, event store, or external persistence is introduced.

## No External Dependencies
The registry uses Python standard library only. No package manifests, lockfiles, package managers, or external packages are introduced.

## No Providers/API/MCP
The registry does not create or activate providers, adapters, APIs, MCP servers, MCP tools, MCP resources, network flows, or authentication flows.

## No Product Activation
Products remain inactive. Product source remains local-only and is not copied into the registry.

## No CSS Substrate Decision
Cognitive Semantic System remains the accepted name. Substrate remains deferred. Graph remains candidate only. The registry does not decide substrate.

## Stop Rules
Stop if work requires target overwrite, file persistence, validation execution, test execution, dependency adoption, package files, security enforcement, provider/API/MCP activation, product source inspection, existing `3_platform` inspection, CSS substrate selection, Git mutation, or I-02 start.
