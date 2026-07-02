# Agent Runtime Boundary

## Purpose
This boundary provides the first minimal governed agent runtime boundary metadata implementation for AGENT PLATFORM / Siamese.

## Current Status
Minimal implementation only. The boundary is in-memory and metadata-only. It is not an agent runtime, scheduler, worker loop, queue, orchestration engine, tool executor, provider bridge, MCP runtime, or product activation layer.

## What This Boundary Can Represent
- Agent descriptors.
- Agent capability descriptors.
- Task envelopes.
- Handoff records.
- Provider, adapter, tool, context, validation, security, and evidence references as metadata IDs.
- Limitations, blockers, and review-required status.

## What This Boundary Cannot Approve
The boundary cannot approve agent activation, task execution, handoff execution, tool execution, provider/API/MCP activation, network calls, authentication, credential access, source tracking, product activation, publication, CSS substrate selection, implementation readiness, or broad implementation.

## Relationship To IR-05
IR-05 runtime/agent/context blockers remain inherited. This boundary records metadata only and does not weaken runtime, agent, context, memory, state, handoff, or tool execution blockers.

## Relationship To Agent Operating Rules
W-series agent operating rules remain governance input. This boundary does not create autonomous permission, task authority, or execution authority.

## Relationship To Validation Registry
Agent/task/handoff metadata may be represented later in the I-01 validation registry as metadata only. The boundary does not execute validation.

## Relationship To Security/access Evaluator
The I-02 evaluator remains metadata-only and not runtime enforcement. Agent records retain blockers for tool, provider, network, credential, and local-only risk.

## Relationship To Context Pack Runtime
The I-03 runtime remains metadata-only. Context pack refs are metadata IDs only. Context inclusion is not permission.

## Relationship To Provider/adapter Layer
The I-04 layer remains metadata-only. Provider and adapter refs are metadata IDs only and do not activate providers or adapters.

## Relationship To Products
Products remain inactive. Product source remains local-only. Product agent metadata may be represented later as metadata only; product agents are not executed or activated here.

## Relationship To Git And Source Tracking
Only exact I-05-created files may be considered for exact-path staging after human review. No broad source tracking is approved. Existing `3_platform` sibling contents remain uninspected and unapproved.

## Future Route
I-06 Tool Execution Boundary may proceed only after explicit instruction. Future agent expansion requires separate gates for runtime activation, scheduling, orchestration, tools, providers, MCP, credentials, dependencies, tests, and security review.

## Stop Rules
Stop if work requires agent activation, task execution, handoff execution, tool execution, provider/API/MCP activation, API calls, network, auth, credential inspection, package manifests, dependencies, tests, scripts, tools, CI, product activation, CSS substrate selection, existing `3_platform` inspection, Git mutation, or I-06 start.
