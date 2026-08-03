# Pepper P16.7 Historical Ticket Regression Corpus Governance Record

## Decision

P16.7 is accepted as a frozen, sanitized, deterministic, in-memory historical regression authority for the accepted P16.0 through P16.6 Ticket Factory contracts.

Verdict target: `hermes_0_19_pepper_historical_ticket_regression_corpus_ready_with_frozen_in_memory_regression_authority`.

## Scope

Authorized product paths:

| Path | Role |
| --- | --- |
| `hermes_cli/agent_platform/ticket_factory/historical_regression.py` | Frozen corpus contracts, fixtures, validation and run functions. |
| `hermes_cli/agent_platform/ticket_factory/__init__.py` | Additive P16.7 public export boundary. |
| `tests/hermes_cli/test_agent_platform_ticket_factory_historical_regression.py` | Focused P16.7 behavioral regression suite. |
| `docs/agent-platform/historical_ticket_regression_corpus.md` | Product documentation for P16.7. |
| `AGENT_PLATFORM_MODIFICATIONS.tsv` | Product modification register update. |
| `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | Import manifest update. |

Authorized governance path:

| Path | Role |
| --- | --- |
| `0_architecture/governance/agent_platform_pepper_historical_ticket_regression_corpus.md` | Human-readable governance record and final evidence. |

## Contract

P16.7 defines exactly one in-memory corpus:

| Field | Value |
| --- | --- |
| Schema version | `1` |
| Corpus ID | `pepper-ticket-factory-historical-regression-v1` |
| Revision | `1` |
| Case count | `12` |
| Corpus SHA-256 | `6b949789efafa2fac5d74eb16915aeb8c4c2a2d7123778c777e800f37beda099` |
| Passing run SHA-256 | `86bf357804b482d8a62d7b43ce5070e75723b3ccc19958c510466b3c6506d20d` |

The corpus covers two cases each for `ticket_spec_validation`, `dependency_planning`, `ticket_policy_lint`, `proposal_synthesis`, `human_approval` and `canonical_publication`.

## Authority Boundary

Allowed authority is limited to Pydantic validation, canonical JSON validation, bounded text sanitization, deterministic SHA-256 digest construction, in-memory fixed dispatch and drift comparison.

Denied authority includes filesystem fixture loading, historical Markdown restoration, file writes, provider calls, credential access, prompt rendering, agent execution, worker execution, tool invocation, validation-command execution, Git mutation, Graphify operation, Docker operation, WorkPacket creation, ticket persistence, automated approval and repository publication.

## Sanitization Posture

Fixtures are compact synthetic or sanitized behavior fixtures. They preserve accepted contract behavior patterns only and do not embed raw historical ticket text, provider responses, prompt dumps, reasoning traces, secret-shaped content, credential material, personal absolute paths or deleted filenames as authority.

Read-only Git-history provenance is represented by commit identity only: `3245b93074fd2218cb9f98ba3d25e53cf9bfbec1`.

## Public API Decision

P16.7 adds 24 public root exports to `hermes_cli.agent_platform.ticket_factory`:

`HISTORICAL_REGRESSION_CORPUS_SCHEMA_VERSION`, `HISTORICAL_REGRESSION_CORPUS_ID`, `HISTORICAL_REGRESSION_CORPUS_REVISION`, `HistoricalRegressionStage`, `HistoricalRegressionCaseClass`, `HistoricalProvenanceKind`, `HistoricalRegressionExpectedOutcome`, `HistoricalRegressionDriftKind`, `HistoricalRegressionRunDisposition`, `HistoricalTicketProvenance`, `HistoricalRegressionExpectation`, `HistoricalRegressionCase`, `HistoricalRegressionCorpus`, `HistoricalRegressionObservation`, `HistoricalRegressionDrift`, `HistoricalRegressionCaseResult`, `HistoricalRegressionRun`, `HistoricalRegressionError`, `HistoricalRegressionCorpusError`, `HistoricalRegressionExecutionError`, `get_historical_ticket_regression_corpus`, `validate_historical_ticket_regression_corpus`, `run_historical_ticket_regression_case` and `run_historical_ticket_regression_corpus`.

Digest algorithm constants remain module-local and are not exported through the package root.

## Evidence

Repository gate:

| Check | Result |
| --- | --- |
| Branch | `p16-ticket-factory-and-parallel-planning` |
| HEAD | `3245b93074fd2218cb9f98ba3d25e53cf9bfbec1` |
| HEAD matches resolved P16.6 commit | `true` |
| Remote branch matches resolved P16.6 commit | `true` |
| Staged files | `[]` |
| Candidate worktree paths | `7` |

Candidate paths:

| Path | Status |
| --- | --- |
| `0_architecture/governance/agent_platform_pepper_historical_ticket_regression_corpus.md` | new governance record |
| `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | modified manifest |
| `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` | modified register |
| `2_products/pepper-agent/docs/agent-platform/historical_ticket_regression_corpus.md` | new documentation |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py` | modified additive exports |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/historical_regression.py` | new corpus module |
| `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_ticket_factory_historical_regression.py` | new tests |

Validation commands:

| Command | Result |
| --- | --- |
| `%USERPROFILE%\anaconda3\python.exe -m pytest tests/hermes_cli/test_agent_platform_ticket_factory_historical_regression.py -q` | `308 passed in 4.81s` |
| `%USERPROFILE%\anaconda3\python.exe -m pytest tests/hermes_cli/test_agent_platform_ticket_factory_specs.py tests/hermes_cli/test_agent_platform_ticket_factory_context_packs.py tests/hermes_cli/test_agent_platform_ticket_factory_generator_roles.py tests/hermes_cli/test_agent_platform_ticket_factory_dependency_planning.py tests/hermes_cli/test_agent_platform_ticket_factory_ticket_policy.py tests/hermes_cli/test_agent_platform_ticket_factory_proposal_synthesis.py tests/hermes_cli/test_agent_platform_ticket_factory_approval_publishing.py tests/hermes_cli/test_agent_platform_ticket_factory_historical_regression.py -q` | `1312 passed in 32.30s` |
| `%USERPROFILE%\anaconda3\python.exe -m ruff check hermes_cli/agent_platform/ticket_factory/__init__.py hermes_cli/agent_platform/ticket_factory/historical_regression.py tests/hermes_cli/test_agent_platform_ticket_factory_historical_regression.py` | `All checks passed!` |
| `%USERPROFILE%\anaconda3\python.exe -m ruff format --check hermes_cli/agent_platform/ticket_factory/__init__.py hermes_cli/agent_platform/ticket_factory/historical_regression.py tests/hermes_cli/test_agent_platform_ticket_factory_historical_regression.py` | `3 files already formatted` |
| `%USERPROFILE%\anaconda3\python.exe -m unittest 12_tests/governance/test_pepper_baseline_integrity.py` | `Ran 14 tests in 0.003s`; `OK` |
| `where ty` | unavailable; no dependency installation performed |

Runtime evidence:

| Check | Result |
| --- | --- |
| Canonical corpus run | `6b949789efafa2fac5d74eb16915aeb8c4c2a2d7123778c777e800f37beda099 pass 12 0 86bf357804b482d8a62d7b43ce5070e75723b3ccc19958c510466b3c6506d20d` |
| Import smoke | `pepper-ticket-factory-historical-regression-v1 HistoricalRegressionCase HistoricalRegressionCorpus HistoricalRegressionRun True pass` |
| Static authority scan | `static_authority_ok 3 python_files forbidden_hits 0` |
| Sanitization scan | `security_sanitization_ok 12 cases path_hits 0` |
| TSV structure | `AGENT_PLATFORM_MODIFICATIONS.tsv rows 175 width 18 bad []`; `AGENT_PLATFORM_IMPORT_MANIFEST.tsv rows 6829 width 8 bad []` |

Working-tree Pepper integrity projection:

| Projection | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate excluding baseline record | `6856` | `150788463` | `37425e5e7fe0eadecfea637bf2a5c475a8a48e707ef9dbdb8f1e95a726772c9d` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Graphify was not run under the explicit P16.7 constraint. No dependencies, lockfiles, staging, commits, pushes, branch switches, Docker commands or destructive Git operations were performed.

## Final Verdict

`hermes_0_19_pepper_historical_ticket_regression_corpus_ready_with_frozen_in_memory_regression_authority`
