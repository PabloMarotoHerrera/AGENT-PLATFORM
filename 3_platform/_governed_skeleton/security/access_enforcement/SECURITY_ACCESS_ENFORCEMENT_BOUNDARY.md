# Security / Access Enforcement Boundary

## Allowed Implementation
Allowed implementation is one minimal Python standard-library module that evaluates declared access request metadata in memory and documentation that describes its boundaries.

## Forbidden Implementation
Forbidden implementation includes package manifests, lockfiles, tests, scripts, tools, CI, runners, CLI, runtime services, persistence, scanners, filesystem guards, network guards, providers, adapters, MCP, product activation, validation execution, and CSS prototype artifacts.

## No Runtime Enforcement
The evaluator does not enforce policy against the OS, Git, shell, filesystem, network, providers, MCP, products, or runtime.

## No Secret Scanning
The evaluator does not scan for secrets and does not inspect secret values.

## No Credential Reading
The evaluator does not read credentials, auth stores, tokens, provider configs, browser auth, local credential stores, or `.env` files.

## No Filesystem Scanning
The evaluator does not scan directories, inspect existing `3_platform` siblings, inspect product source, or inspect local-only folders.

## No Network
The evaluator does not perform network calls, API calls, package index calls, provider calls, authentication flows, or MCP activation.

## No Providers/API/MCP
The evaluator does not create or activate providers, adapters, APIs, MCP servers, MCP tools, MCP resources, network flows, or authentication flows.

## No Product Activation
Products remain inactive. Product source remains local-only and is not copied into the evaluator.

## No CSS Substrate Decision
Cognitive Semantic System remains the accepted name. Substrate remains deferred. Graph remains candidate only. The evaluator does not decide substrate.

## Stop Rules
Stop if work requires target overwrite, runtime enforcement, secret or credential inspection, filesystem scanning, network calls, test execution, dependency adoption, package files, provider/API/MCP activation, product source inspection, existing `3_platform` inspection, CSS substrate selection, Git mutation, or I-03 start.
