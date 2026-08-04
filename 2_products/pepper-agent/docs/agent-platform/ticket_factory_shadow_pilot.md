# P16.8 Ticket Factory Shadow Pilot

P16.8 adds a deterministic shadow pilot over the accepted P16.0 through P16.7 Ticket Factory contracts. It composes the schema, context-pack, generator-role, dependency-planning, policy-linting, synthesis-review, human-approval, logical-publication and historical-regression surfaces in memory and emits bounded evidence for one synthetic ticket, `P16.SP1`.

The shadow pilot is non-executing. It does not call providers or models, render prompts, invoke agents or workers, run validation commands, launch runtimes, allocate WorkPackets, read or write filesystem state, mutate Git, run Graphify, run Docker or publish repository files.

## Relationship To P16.0 Through P16.7

P16.0 owns `ProjectSpec` and `TicketSpec`. P16.1 owns bounded in-memory `ContextPack` assembly. P16.2 owns non-executing generator-role assignments and proposal envelopes. P16.3 owns dependency-only planning. P16.4 owns deterministic non-mutating policy linting. P16.5 owns noncanonical multi-generator synthesis review. P16.6 owns explicit human approval evidence and in-memory logical canonical publication. P16.7 owns the frozen historical regression corpus.

P16.8 consumes those contracts as a shadow pilot. It first runs the P16.7 corpus and requires `pass` with 12 passed cases and zero drift. It then builds context, dependency, lint, four generator assignments, four independent proposals, one generated title dissent in synthesis review, explicit synthetic approval evidence resolving that dissent and one logical publication result.

## Public Exports

P16.8 adds exactly 24 public names through `hermes_cli.agent_platform.ticket_factory`:

| Export | Purpose |
| --- | --- |
| `TICKET_FACTORY_SHADOW_PILOT_SCHEMA_VERSION` | Fixed schema version, currently `1`. |
| `TICKET_FACTORY_SHADOW_PILOT_ID` | Pilot identity, `pepper-ticket-factory-shadow-pilot-v1`. |
| `TICKET_FACTORY_SHADOW_PILOT_REVISION` | Frozen revision, currently `1`. |
| `ShadowPilotStage` | Canonical stage vocabulary. |
| `ShadowPilotGate` | Canonical gate vocabulary. |
| `ShadowPilotGateStatus` | Gate and stage status vocabulary. |
| `ShadowPilotDisposition` | Final report disposition vocabulary. |
| `ShadowPilotArtifactKind` | Evidence artifact-kind vocabulary. |
| `ShadowPilotEvidence` | Stage artifact digest evidence. |
| `ShadowPilotStageResult` | Per-stage status, evidence and digest envelope. |
| `ShadowPilotGateResult` | Per-gate status and digest envelope. |
| `TicketFactoryShadowPilotRequest` | Immutable shadow pilot request. |
| `TicketFactoryShadowPilotReport` | Immutable shadow pilot report. |
| `TicketFactoryShadowPilotError` | Base shadow pilot exception. |
| `TicketFactoryShadowPilotInputError` | Request consistency exception. |
| `TicketFactoryShadowPilotExecutionError` | In-memory composition exception. |
| `TicketFactoryShadowPilotIntegrityError` | Report integrity exception. |
| `get_canonical_ticket_factory_shadow_pilot_request` | Return the canonical P16.8 request. |
| `run_ticket_factory_shadow_pilot` | Run the deterministic in-memory pilot. |
| `validate_ticket_factory_shadow_pilot_report` | Validate report integrity. |
| `summarize_ticket_factory_shadow_pilot_report` | Return the one-line report summary. |
| `get_ticket_factory_shadow_pilot_stage_order` | Return canonical stage order. |
| `get_ticket_factory_shadow_pilot_gate_order` | Return canonical gate order. |
| `canonical_ticket_factory_shadow_pilot_output` | Run and return the exact smoke output. |

Digest algorithm constants are intentionally module-local and are not exported through the package root.

## Canonical Output

The canonical smoke output is:

```text
go_with_constraints P16.SP1 pass 12 12 0 4 4 approved published
```

Field order is disposition, ticket ID, historical run disposition, historical case count, passed case count, drifted case count, assignment count, proposal count, approval state and publication state.

## Stages And Gates

The report contains eight ordered stages:

| Stage | Artifact |
| --- | --- |
| `historical_preflight` | P16.7 `HistoricalRegressionRun`. |
| `context_assembly` | P16.1 `ContextPack`. |
| `dependency_planning` | P16.3 `TicketDependencyPlan`. |
| `generator_assignment` | Four P16.2 `GeneratorAssignment` records. |
| `proposal_review` | Four P16.2 `TicketProposal` records with lint evidence. |
| `synthesis_review` | P16.5 `TicketSynthesisReview`. |
| `human_approval` | P16.6 `TicketApprovalRecord`. |
| `canonical_publication` | P16.6 `TicketPublicationResult`. |

The report contains four ordered gates: `historical_regression_clean`, `policy_lint_pass`, `synthesis_review_ready` and `human_approval_present`. Passing gates produce `go_with_constraints`, not execution readiness. The constraint is the shadow-only boundary.

## Canonical Dissent Scenario

The canonical pilot uses four proposal roles: `architecture`, `integration`, `governance` and `documentation`. Three proposals preserve the seed title `Ticket Factory shadow pilot`; the documentation proposal uses the bounded alternate title `Ticket Factory shadow pilot dissent check`. All other synthesizable fields preserve the seed values.

`build_ticket_synthesis_review(...)` therefore produces exactly one `field_dissent` conflict for `title`, no `field_split`, no stale dependency-plan conflict and no stale scope-plan conflict. The candidate remains equal to the seed ticket, the synthesis disposition is `review_ready_with_dissent` and the approval record resolves the generated conflict with `accept_candidate` before logical publication.

## Frozen Identity

Canonical request SHA-256: `cd13ac9cfd84ee693c3ebb4550a6c46787ff19973b924f75042181056d0a5270`.

Canonical report SHA-256: `6cb4158558ebe0e321de10c397e16f05ab306ac3a69b3ef46460d6ab188840da`.

The stage evidence binds to the upstream artifact digests exposed by prior accepted contracts, including the P16.7 run SHA-256 `86bf357804b482d8a62d7b43ce5070e75723b3ccc19958c510466b3c6506d20d`.

## Validation

Focused validation command:

```bash
python -m pytest tests/hermes_cli/test_agent_platform_ticket_factory_shadow_pilot.py -q
```

The focused suite verifies root exports, model posture, canonical output, stage and gate order, frozen digests, historical preflight, assignments, proposals, generated title dissent, synthesis fields, approval conflict coverage, logical publication, request authority flags and tamper rejection.

## Deferred Responsibilities

P16.8 does not claim production readiness. WorkPacket execution, runtime scheduling, real ticket execution, repository publication and operator rollout remain deferred to later authorized work.
