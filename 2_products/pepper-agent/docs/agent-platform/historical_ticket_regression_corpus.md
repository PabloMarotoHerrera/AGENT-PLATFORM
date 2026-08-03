# P16.7 Historical Ticket Regression Corpus

P16.7 adds a frozen in-memory historical regression corpus for the accepted P16.0 through P16.6 Ticket Factory contracts. It preserves compact sanitized fixtures, fixed provenance, fixed expectations and deterministic run evidence for the schema, context-pack, generator-role, dependency-planning, policy-linting, synthesis-review, approval and logical publication surfaces.

The corpus is regression authority only. It does not read historical ticket files, restore deleted Markdown, execute validation commands, call providers, inspect credentials, mutate tickets, write canonical artifacts, publish repository files, allocate WorkPackets, run Git, run Graphify or run Docker.

## Relationship To P16.0 Through P16.6

P16.0 owns `ProjectSpec` and `TicketSpec`. P16.1 owns bounded in-memory `ContextPack` assembly. P16.2 owns non-executing generator roles and proposal envelopes. P16.3 owns dependency DAG and parallel-wave planning. P16.4 owns deterministic non-mutating ticket policy linting. P16.5 owns noncanonical multi-generator synthesis and conflict review. P16.6 owns explicit human approval evidence and in-memory logical canonical publication.

P16.7 consumes those accepted contracts through fixed dispatch only. Each case stores canonical compact JSON input and a frozen expectation. A run executes the accepted builder or validator for the case stage, records a bounded observation, compares it to the frozen expectation and emits deterministic drift evidence if behavior changes.

## Authority Boundary

P16.7 performs Pydantic validation, canonical JSON parsing, bounded text sanitization, deterministic SHA-256 hashing, fixed in-memory dispatch and drift comparison.

P16.7 performs no filesystem reads or writes, no network access, no provider access, no credential access, no prompt rendering, no agent invocation, no worker invocation, no shell execution, no Git operation, no Graphify operation, no Docker operation, no WorkPacket creation, no ticket persistence, no auto-fix and no repository publication.

## Public Exports

P16.7 adds exactly 24 public names through `hermes_cli.agent_platform.ticket_factory`:

| Export | Purpose |
| --- | --- |
| `HISTORICAL_REGRESSION_CORPUS_SCHEMA_VERSION` | Fixed schema version, currently `1`. |
| `HISTORICAL_REGRESSION_CORPUS_ID` | Corpus identity, `pepper-ticket-factory-historical-regression-v1`. |
| `HISTORICAL_REGRESSION_CORPUS_REVISION` | Frozen revision, currently `1`. |
| `HistoricalRegressionStage` | Case dispatch stage vocabulary. |
| `HistoricalRegressionCaseClass` | Accepted, rejected and boundary case vocabulary. |
| `HistoricalProvenanceKind` | Current governance, read-only Git history and sanitized synthetic provenance vocabulary. |
| `HistoricalRegressionExpectedOutcome` | Success or bounded error expectation vocabulary. |
| `HistoricalRegressionDriftKind` | Drift taxonomy for unexpected outcomes, type mismatches, digest mismatches and exception mismatches. |
| `HistoricalRegressionRunDisposition` | Run disposition vocabulary. |
| `HistoricalTicketProvenance` | Sanitized provenance envelope for one historical case. |
| `HistoricalRegressionExpectation` | Frozen expected success or bounded error evidence. |
| `HistoricalRegressionCase` | One frozen case with canonical input JSON and case digest. |
| `HistoricalRegressionCorpus` | Frozen 12-case corpus envelope and corpus digest. |
| `HistoricalRegressionObservation` | Bounded observed output or exception evidence. |
| `HistoricalRegressionDrift` | Blocking drift record for a mismatched case. |
| `HistoricalRegressionCaseResult` | Case result, observation and result digest. |
| `HistoricalRegressionRun` | Full corpus run result and run digest. |
| `HistoricalRegressionError` | Base historical regression exception. |
| `HistoricalRegressionCorpusError` | Corpus or case integrity exception. |
| `HistoricalRegressionExecutionError` | Fixed-dispatch execution exception. |
| `get_historical_ticket_regression_corpus` | Return the single frozen in-memory corpus. |
| `validate_historical_ticket_regression_corpus` | Validate corpus identity, composition and digest integrity. |
| `run_historical_ticket_regression_case` | Execute one frozen case and return drift evidence. |
| `run_historical_ticket_regression_corpus` | Execute all cases in deterministic order. |

Digest algorithm constants are intentionally not exported through the package root.

## Corpus Composition

The corpus contains exactly 12 cases. Each P16.0 through P16.6 behavior band is represented by two cases:

| Stage | Cases | Coverage |
| --- | --- | --- |
| `ticket_spec_validation` | `HIST-001`, `HIST-002` | Valid `TicketSpec` acceptance and schema-version rejection. |
| `dependency_planning` | `HIST-003`, `HIST-004` | Deterministic hard-prerequisite planning and hard-cycle rejection. |
| `ticket_policy_lint` | `HIST-005`, `HIST-006` | Clean lint report and blocked lint report. |
| `proposal_synthesis` | `HIST-007`, `HIST-008` | Unanimous synthesis and split-field human-review boundary. |
| `human_approval` | `HIST-009`, `HIST-010` | Approval success and unresolved-conflict rejection. |
| `canonical_publication` | `HIST-011`, `HIST-012` | First logical publication and supersession boundary. |

Class composition is six accepted cases, four rejected cases and two boundary cases. Provenance composition is five current-governance cases, two read-only Git-history cases and five sanitized synthetic-derivation cases.

## Frozen Digests

Corpus SHA-256: `6b949789efafa2fac5d74eb16915aeb8c4c2a2d7123778c777e800f37beda099`.

Passing run SHA-256: `86bf357804b482d8a62d7b43ce5070e75723b3ccc19958c510466b3c6506d20d`.

Case digests are bound to the case metadata, sanitized provenance, stage, canonical input JSON, frozen expectation and tags. The corpus digest is bound to the complete ordered case set and excludes observed run output. The run digest is bound to the corpus identity and deterministic case results.

## Drift Behavior

`run_historical_ticket_regression_corpus()` validates corpus integrity before execution. It then runs every case in corpus order and does not stop at the first drift. A passing run has empty `drifted_case_ids`, all 12 case IDs in `passed_case_ids` and disposition `pass`.

If behavior changes, the run returns disposition `drift_detected`. Drift records are blocking and identify unexpected success, unexpected error, output type mismatch, output digest mismatch, exception type mismatch or exception message mismatch.

## Serialization

Standard Pydantic `model_dump()`, `model_dump_json()`, `model_validate()`, `model_validate_json()` and `model_json_schema()` are supported. Public models are frozen, extra-forbid and validate defaults.

Filesystem serialization, YAML support, Markdown fixture loading and file writers are absent.

## Validation

Focused validation command:

```bash
python -m pytest tests/hermes_cli/test_agent_platform_ticket_factory_historical_regression.py -q
```

The focused suite verifies root exports, corpus identity, composition, case order, fixture digests, case expectations, observation digests, result digests, deterministic run digest, tamper rejection, serialization and sanitized provenance.

## Deferred Responsibilities

P16.8 owns the shadow pilot. WorkPacket execution remains deferred to P17.

P16.7 does not claim production readiness.
