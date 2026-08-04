# Pepper P16.8 Ticket Factory Shadow Pilot Governance Record

## Decision

P16.8 is accepted as a deterministic, bounded, fully in-memory shadow pilot over the accepted P16.0 through P16.7 Ticket Factory contracts.

Verdict target: the canonical P16.8 shadow-pilot readiness verdict defined by the response contract.

## Corrected Pre-Change Authority

The authoritative P16.8 pre-change Pepper identity is the committed P16.7 Git tree at commit `80e585dcc39b3bc67c10f9ca597c1dca3f442f12`, not the stale uncommitted P16.7 working-tree projection.

| Projection | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Correct committed P16.7 candidate excluding baseline record | `6856` | `150781457` | `4372815b597e9973706a8f0b75db4b35768fabdc7a055760e9d7e3f54079905f` |
| Payload unchanged | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline unchanged | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

## Scope

Authorized product paths:

| Path | Role |
| --- | --- |
| `hermes_cli/agent_platform/ticket_factory/shadow_pilot.py` | Shadow pilot contracts, canonical request, runner, report validation and summary output. |
| `hermes_cli/agent_platform/ticket_factory/__init__.py` | Additive P16.8 public export boundary. |
| `tests/hermes_cli/test_agent_platform_ticket_factory_shadow_pilot.py` | Focused P16.8 behavioral regression suite. |
| `docs/agent-platform/ticket_factory_shadow_pilot.md` | Product documentation for P16.8. |
| `AGENT_PLATFORM_MODIFICATIONS.tsv` | Product modification register update. |
| `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | Import manifest update. |

Authorized governance path:

| Path | Role |
| --- | --- |
| `0_architecture/governance/agent_platform_pepper_ticket_factory_shadow_pilot.md` | Human-readable governance record and final evidence. |

## Contract

P16.8 defines exactly one canonical in-memory request and one canonical report shape:

| Field | Value |
| --- | --- |
| Schema version | `1` |
| Pilot ID | `pepper-ticket-factory-shadow-pilot-v1` |
| Revision | `1` |
| Shadow ticket | `P16.SP1` |
| Canonical request SHA-256 | `cd13ac9cfd84ee693c3ebb4550a6c46787ff19973b924f75042181056d0a5270` |
| Canonical report SHA-256 | `6cb4158558ebe0e321de10c397e16f05ab306ac3a69b3ef46460d6ab188840da` |
| Historical preflight | `pass`, 12 cases, 12 passed, 0 drifted |
| Generator assignments | `4` |
| Independent proposals | `4`: three seed-title proposals and one bounded alternate-title proposal |
| Synthesis disposition | `review_ready_with_dissent` |
| Synthesis conflicts | exactly one generated `field_dissent` on `title`; no field split, stale dependency-plan or stale scope conflicts |
| Approval conflict resolutions | exactly one `accept_candidate` resolution bound to the generated conflict ID |
| Approval state | `approved` |
| Publication state | `published` |

Canonical output:

```text
go_with_constraints P16.SP1 pass 12 12 0 4 4 approved published
```

## Authority Boundary

Allowed authority is limited to Pydantic validation, deterministic in-memory composition of accepted P16.0-P16.7 contracts, canonical JSON serialization, deterministic SHA-256 digest construction, bounded evidence envelopes and report validation.

Denied authority includes provider calls, model calls, prompt rendering, agent invocation, worker invocation, tool invocation, validation-command execution by the module, runtime launch, filesystem reads or writes, filesystem publication, repository publication, Git mutation, Graphify operation, Docker operation, WorkPacket creation, ticket persistence, ticket mutation and automated approval outside explicit synthetic evidence.

## Public API Decision

P16.8 adds 24 public root exports to `hermes_cli.agent_platform.ticket_factory`:

`TICKET_FACTORY_SHADOW_PILOT_SCHEMA_VERSION`, `TICKET_FACTORY_SHADOW_PILOT_ID`, `TICKET_FACTORY_SHADOW_PILOT_REVISION`, `ShadowPilotStage`, `ShadowPilotGate`, `ShadowPilotGateStatus`, `ShadowPilotDisposition`, `ShadowPilotArtifactKind`, `ShadowPilotEvidence`, `ShadowPilotStageResult`, `ShadowPilotGateResult`, `TicketFactoryShadowPilotRequest`, `TicketFactoryShadowPilotReport`, `TicketFactoryShadowPilotError`, `TicketFactoryShadowPilotInputError`, `TicketFactoryShadowPilotExecutionError`, `TicketFactoryShadowPilotIntegrityError`, `get_canonical_ticket_factory_shadow_pilot_request`, `run_ticket_factory_shadow_pilot`, `validate_ticket_factory_shadow_pilot_report`, `summarize_ticket_factory_shadow_pilot_report`, `get_ticket_factory_shadow_pilot_stage_order`, `get_ticket_factory_shadow_pilot_gate_order` and `canonical_ticket_factory_shadow_pilot_output`.

Digest algorithm constants remain module-local and are not exported through the package root.

## Evidence

Repository gate:

| Check | Result |
| --- | --- |
| Branch | `p16-ticket-factory-and-parallel-planning` |
| Resolved P16.7 commit | `80e585dcc39b3bc67c10f9ca597c1dca3f442f12` |
| Pre-change worktree/index | clean before P16.8 changes |
| P16.7 commit path count | `7` |
| P16.7 commit added/modified/deleted | `4` / `3` / `0` |
| P16.7 unexpected paths | `0` |

Candidate paths:

| Path | Status |
| --- | --- |
| `0_architecture/governance/agent_platform_pepper_ticket_factory_shadow_pilot.md` | new governance record |
| `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | modified manifest |
| `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` | modified register |
| `2_products/pepper-agent/docs/agent-platform/ticket_factory_shadow_pilot.md` | new documentation |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py` | modified additive exports |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/shadow_pilot.py` | new shadow pilot module |
| `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_ticket_factory_shadow_pilot.py` | new tests |

Validation commands:

| Command | Result |
| --- | --- |
| `%USERPROFILE%\anaconda3\python.exe -m pytest tests/hermes_cli/test_agent_platform_ticket_factory_shadow_pilot.py -q -p no:cacheprovider` | `192 passed in 2.76s` |
| `%USERPROFILE%\anaconda3\python.exe -m pytest tests/hermes_cli/test_agent_platform_ticket_factory_specs.py tests/hermes_cli/test_agent_platform_ticket_factory_context_packs.py tests/hermes_cli/test_agent_platform_ticket_factory_generator_roles.py tests/hermes_cli/test_agent_platform_ticket_factory_dependency_planning.py tests/hermes_cli/test_agent_platform_ticket_factory_ticket_policy.py tests/hermes_cli/test_agent_platform_ticket_factory_proposal_synthesis.py tests/hermes_cli/test_agent_platform_ticket_factory_approval_publishing.py tests/hermes_cli/test_agent_platform_ticket_factory_historical_regression.py tests/hermes_cli/test_agent_platform_ticket_factory_shadow_pilot.py -q -p no:cacheprovider` | `1504 passed in 39.84s` |
| `%USERPROFILE%\anaconda3\python.exe -m ruff check hermes_cli/agent_platform/ticket_factory/__init__.py hermes_cli/agent_platform/ticket_factory/shadow_pilot.py tests/hermes_cli/test_agent_platform_ticket_factory_shadow_pilot.py` | `All checks passed!` |
| `%USERPROFILE%\anaconda3\python.exe -m ruff format --check hermes_cli/agent_platform/ticket_factory/__init__.py hermes_cli/agent_platform/ticket_factory/shadow_pilot.py tests/hermes_cli/test_agent_platform_ticket_factory_shadow_pilot.py` | `3 files already formatted` |
| `%USERPROFILE%\anaconda3\python.exe -m unittest 12_tests/governance/test_pepper_baseline_integrity.py` | `Ran 14 tests in 0.003s`; `OK` |
| `where ty` | unavailable; no dependency installation performed |

Runtime evidence:

| Check | Result |
| --- | --- |
| Canonical shadow pilot output | `go_with_constraints P16.SP1 pass 12 12 0 4 4 approved published` |
| Canonical synthesis smoke | `review_ready_with_dissent 4 0 1 1 0 0 0 True 1 approved` |
| Import smoke | `TicketFactoryShadowPilotRequest TicketFactoryShadowPilotReport ShadowPilotDisposition get_canonical_ticket_factory_shadow_pilot_request run_ticket_factory_shadow_pilot` |
| Static authority scan | `static_authority_ok 3 python_files forbidden_hits 0 []` |
| Security/sanitization scan | `security_sanitization_ok report_bytes 3066203 marker_hits 0 []` |
| TSV structure | `AGENT_PLATFORM_MODIFICATIONS.tsv rows 179 width 18 bad []`; `AGENT_PLATFORM_IMPORT_MANIFEST.tsv rows 6833 width 8 bad []` |
| Manifest hash check | `manifest_hash_check seen [docs/agent-platform/ticket_factory_shadow_pilot.md, hermes_cli/agent_platform/ticket_factory/__init__.py, hermes_cli/agent_platform/ticket_factory/shadow_pilot.py, tests/hermes_cli/test_agent_platform_ticket_factory_shadow_pilot.py] bad []` |
| Committed P16.7 integrity authority | `candidate files=6856 bytes=150781457 sha256=4372815b597e9973706a8f0b75db4b35768fabdc7a055760e9d7e3f54079905f`; `payload files=6681 bytes=145409792 sha256=1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c`; `baseline bytes=38693 sha256=fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |
| P16.8 working-tree integrity projection | `candidate files=6859 bytes=150879344 sha256=b7719472b1fbe37734d1478302abd2f9d78af3a02d05a608d0509c4095ca2619`; `payload files=6681 bytes=145409792 sha256=1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c`; `baseline bytes=38693 sha256=fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |
| Candidate path set | `p16_8_candidate_paths 7 unexpected [] missing [] staged []` |

Graphify was not run under the explicit P16.8 constraint. No dependencies, lockfiles, staging, commits, pushes, branch switches, Docker commands or destructive Git operations were performed.

## Final Verdict

`hermes_0_19_pepper_ticket_factory_shadow_pilot_ready_with_shadow_only_non_executing_evidence`
