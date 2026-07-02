# Provider / Adapter Layer

## Purpose
This layer provides the first minimal governed provider/adapter metadata implementation for AGENT PLATFORM / Siamese.

## Current Status
Minimal implementation only. The layer is in-memory and metadata-only. It is not a provider client, API client, adapter runtime, MCP runtime, credential system, network permission system, or activation layer.

## What This Layer Can Represent
- Provider descriptors.
- Adapter descriptors.
- Adapter capabilities.
- Activation status metadata.
- Auth and network requirement metadata.
- Credential reference IDs.
- Evidence references.
- Limitations, blockers, and review-required status.

## What This Layer Cannot Approve
The layer cannot approve provider activation, adapter activation, MCP activation, network calls, API calls, authentication, credential access, tool execution, dependency adoption, source tracking, product activation, publication, CSS substrate selection, implementation readiness, or broad implementation.

## Relationship To IR-06
IR-06 provider/adapter/MCP activation blockers remain inherited. This layer records metadata only and does not weaken IR-06 activation boundaries.

## Relationship To Security/access Evaluator
The I-02 evaluator remains metadata-only and not runtime enforcement. Provider/adapter descriptors retain auth, network, credential, blocker, and review metadata for later security review.

## Relationship To Context Pack Runtime
The I-03 context pack runtime remains metadata-only. Context inclusion is not permission to transmit data to providers, adapters, APIs, or MCP.

## Relationship To Products
Products remain inactive. Product source remains local-only. Product integrations may be represented later as metadata only; product integrations are not executed or activated here.

## Relationship To Git And Source Tracking
Only exact I-04-created files may be considered for exact-path staging after human review. No broad source tracking is approved. Existing `3_platform` sibling contents remain uninspected and unapproved.

## Future Route
I-05 Agent Runtime Boundary may proceed only after explicit instruction. Future provider/adapter expansion requires separate gates for activation, credentials, dependencies, tests, network, APIs, MCP, runtime behavior, and security review.

## Stop Rules
Stop if work requires provider activation, adapter activation, MCP activation, API calls, network, auth, credential inspection, provider configs, adapter configs, MCP configs, package manifests, dependencies, tests, scripts, tools, CI, product activation, CSS substrate selection, existing `3_platform` inspection, Git mutation, or I-05 start.
