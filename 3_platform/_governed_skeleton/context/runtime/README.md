# Context Pack Runtime

## Purpose
This runtime provides the first minimal governed context pack metadata implementation for AGENT PLATFORM / Siamese.

## Current Status
Minimal implementation only. The runtime is in-memory and metadata-only. It is not a source loader, permission engine, source tracker, migration engine, provider bridge, tool runner, product activation layer, or persistence layer.

## What This Runtime Can Represent
- Context source references as metadata.
- Context items containing safe summaries and evidence references.
- Context packs referencing item IDs.
- Sensitivity posture.
- Limitations, blockers, and review-required status.
- Assembly for review.

## What This Runtime Cannot Approve
The runtime cannot approve permissions, source tracking, migration, dependency adoption, provider activation, product activation, publication, CSS substrate selection, implementation readiness, or broad implementation.

## Relationship To W-series Context Strategy
The runtime implements a minimal metadata shape aligned with W-series context pack strategy. It does not replace governance and does not load raw source content.

## Relationship To Validation Registry
Context decisions may be represented later in the I-01 validation registry as metadata only. The runtime does not execute validation and does not approve validation results.

## Relationship To Security/access Evaluator
The I-02 evaluator remains metadata-only and not runtime enforcement. This runtime retains sensitivity, blockers, and limitations but does not enforce policy against files or systems.

## Relationship To Products
Products remain inactive. Product source remains local-only. Product context may be represented later as safe metadata only; product source is not loaded or copied here.

## Relationship To Git And Source Tracking
Only exact I-03-created files may be considered for exact-path staging after human review. No broad source tracking is approved. Existing `3_platform` sibling contents remain uninspected and unapproved.

## Future Route
I-04 Provider / Adapter Layer may proceed only after explicit instruction. Future context expansion requires separate gates for source loading, persistence, tests, enforcement, and provider/API/MCP integration.

## Stop Rules
Stop if work requires source loading, local-only inclusion, raw product source, raw external source, secrets, credentials, persistence, tests, scripts, tools, CI, package manifests, dependencies, providers, APIs, MCP, product activation, CSS substrate selection, existing `3_platform` inspection, Git mutation, or I-04 start.
