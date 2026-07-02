# Validation Registry

## Purpose
This registry provides the first minimal governed validation metadata implementation for AGENT PLATFORM / Siamese.

## Current Status
Minimal implementation only. The registry is in-memory, metadata-only, and not a validation runner, persistence layer, runtime service, or enforcement mechanism.

## What This Registry Can Represent
- Validation record IDs.
- Target IDs.
- Claims.
- Scope-bound validation status.
- Proof levels PL-0 through PL-8.
- Evidence references or IDs.
- Limitations.
- Blockers.
- Creator and timestamp metadata.
- Review-required status.

## What This Registry Cannot Approve
The registry cannot approve governance decisions, execution, source tracking, dependency adoption, provider activation, product activation, publication, implementation readiness, security exceptions, or broad implementation.

## Relationship To V-series
The registry implements a minimal metadata shape aligned with V-series validation, proof, and evidence concepts. It does not replace V-series governance and does not execute validation.

## Relationship To Security
Security boundaries remain active. The registry does not inspect secrets or credentials, does not enforce access control, does not scan content, and does not publish artifacts.

## Relationship To Products
Products remain inactive. Product source remains local-only. Product validation records may be represented later as metadata only; product validation is not executed here.

## Relationship To Git And Source Tracking
Only exact I-01-created files may be considered for exact-path staging after human review. No broad source tracking is approved. Existing `3_platform` sibling contents remain uninspected and unapproved.

## Future Route
I-02 Security / Access Enforcement may proceed only after explicit instruction. Future validation expansion requires separate gates for persistence, execution, tests, and enforcement.

## Stop Rules
Stop if work requires validation execution, security enforcement, persistence, tests, scripts, tools, CI, package manifests, dependencies, providers, APIs, MCP, product activation, CSS substrate selection, existing `3_platform` inspection, Git mutation, or I-02 start.
