# Context Runtime Boundary

## Allowed Implementation
Allowed implementation is one minimal Python standard-library module that models context source references, context items, and context packs in memory, plus documentation that describes its boundaries.

## Forbidden Implementation
Forbidden implementation includes package manifests, lockfiles, tests, scripts, tools, CI, runners, CLI, runtime services, persistence, source loaders, scanners, provider integrations, adapters, MCP, product activation, validation execution, security enforcement, and CSS prototype artifacts.

## No Raw Source Loading
The runtime does not load source files, source trees, product source, external source, datasets, models, artifacts, generated outputs, or unclassified `3_platform` contents.

## No Local-only Leakage
Local-only material, secrets, credentials, raw product source, raw external source, generated-sensitive material, datasets, models, artifacts, and unclassified content are not included.

## No Permission Semantics
Context inclusion is not permission. `included_for_review` and `assembled_for_review` do not approve action.

## No Source Tracking Semantics
Context inclusion is not source tracking. `allowed_for_context` does not approve staging, commit, push, publication, or force-add.

## No Providers/API/MCP
The runtime does not create or activate providers, adapters, APIs, MCP servers, MCP tools, MCP resources, network flows, or authentication flows.

## No Product Activation
Products remain inactive. Product source remains local-only and is not copied into the runtime.

## No CSS Substrate Decision
Cognitive Semantic System remains the accepted name. Substrate remains deferred. Graph remains candidate only. The runtime does not decide substrate.

## Stop Rules
Stop if work requires target overwrite, source loading, local-only inclusion, raw source copying, secret or credential inclusion, persistence, test execution, dependency adoption, package files, provider/API/MCP activation, product source inspection, existing `3_platform` inspection, CSS substrate selection, Git mutation, or I-04 start.
