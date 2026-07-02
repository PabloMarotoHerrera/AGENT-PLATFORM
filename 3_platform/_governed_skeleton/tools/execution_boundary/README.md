# Tool Execution Boundary

## Purpose
This boundary provides the first minimal governed tool execution boundary metadata implementation for AGENT PLATFORM / Siamese.

## Current Status
Minimal implementation only. The boundary is in-memory and metadata-only. It is not a tool executor, shell runner, filesystem guard, network client, provider client, MCP runtime, package manager wrapper, build runner, test runner, or runtime service.

## What This Boundary Can Represent
- Tool descriptors.
- Tool capability descriptors.
- Tool execution requests as metadata.
- Tool execution decisions as metadata.
- Risk levels, blockers, limitations, reasons, and review-required status.
- Provider, adapter, MCP, context, validation, security, and agent task references as metadata IDs.

## What This Boundary Cannot Approve
The boundary cannot approve tool activation, tool execution, shell commands, subprocesses, filesystem access, network calls, API calls, provider activation, MCP activation, credential access, source tracking, dependency adoption, product activation, publication, CSS substrate selection, implementation readiness, or broad implementation.

## Relationship To IR-06
IR-06 provider/adapter/MCP activation blockers remain inherited. This boundary records metadata only and does not weaken tool, network, API, provider, adapter, or MCP blockers.

## Relationship To Agent Operating Rules
W-series agent operating rules remain governance input. Tool metadata does not create permission for agents to execute tools.

## Relationship To Validation Registry
Tool metadata, requests, and decisions may be represented later in the I-01 validation registry as metadata only. The boundary does not execute validation.

## Relationship To Security/access Evaluator
The I-02 evaluator remains metadata-only and not runtime enforcement. Tool records retain blockers for shell, filesystem, network, provider, credential, product, and destructive risk.

## Relationship To Context Pack Runtime
The I-03 runtime remains metadata-only. Context pack refs are metadata IDs only. Context inclusion is not permission.

## Relationship To Provider/adapter Layer
The I-04 layer remains metadata-only. Provider, adapter, and MCP refs are metadata IDs only and do not activate providers, adapters, or MCP.

## Relationship To Agent Runtime Boundary
The I-05 boundary remains metadata-only. Agent task refs are metadata IDs only and do not execute agent tasks.

## Relationship To Products
Products remain inactive. Product source remains local-only. Product tool metadata may be represented later as metadata only; product tools are not executed or activated here.

## Relationship To Git And Source Tracking
Only exact I-06-created files may be considered for exact-path staging after human review. No broad source tracking is approved. Existing `3_platform` sibling contents remain uninspected and unapproved.

## Future Route
I-07 Cognitive Semantic System Prototype may proceed only after explicit instruction. Future tool expansion requires separate gates for execution, shell, filesystem, network, providers, MCP, credentials, dependencies, tests, and security review.

## Stop Rules
Stop if work requires tool activation, tool execution, shell/subprocess execution, filesystem access, network/API calls, provider/API/MCP activation, auth, credential inspection, package manifests, dependencies, tests, scripts, tools, CI, product activation, CSS substrate selection, existing `3_platform` inspection, Git mutation, or I-07 start.
