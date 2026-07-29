# P16.1 Context Pack Assembler Governance Record

## P16.1 Authority

P16 is Ticket Factory and Parallel Planning. P16.1 adds only a deterministic, bounded, in-memory Context Pack Assembler for Pepper planning specs.

The assembler consumes one P16.0 `ProjectSpec`, one P16.0 `TicketSpec`, explicit caller-supplied `ContextSourceSpec` values and an explicit `ContextAssemblyPolicy`. It emits an immutable `ContextPack` with ordered items, omitted IDs, truncated IDs, total included character count and a deterministic SHA-256 digest record.

P16.1 is not a prompt renderer, generated ticket, WorkPacket, approval record, publication record, dependency planner, repository scanner, semantic searcher, runtime adapter, provider request or execution plan.

## Repository and Branch State

| Item | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM` |
| Branch | `p16.1-context-pack-assembler` |
| Required parent | `c6bee5218d68af0c40efbfa98933cf45888e325f` |
| Parent message | `P16.0 Add ProjectSpec and TicketSpec schema` |
| HEAD at implementation | `c6bee5218d68af0c40efbfa98933cf45888e325f` |
| main at implementation | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| origin/main at implementation | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| Registered worktrees | `1` |

The P16.1 candidate remains uncommitted by instruction. No staging, commit, push, branch switch, reset, clean, stash, Docker command, dependency update, lockfile update, Graphify command or `graphify-out` modification was performed.

## P16.0 Dependency

| Item | Value |
| --- | --- |
| P16.0 commit | `c6bee5218d68af0c40efbfa98933cf45888e325f` |
| P16.0 verdict | `hermes_0_19_pepper_project_ticket_spec_schema_ready_with_planning_only_authority` |
| P16.0 consumed by P16.1 | `true` |
| P16.0 schema module modified by P16.1 | `false` |
| P16.0 schema documentation modified by P16.1 | `false` |
| P16.0 governance record modified by P16.1 | `false` |

The inherited P16.0 focused export test was corrected under explicit continuation authority to assert additive export preservation rather than a closed-world package export set. P16.0 exports remain present and in P16.0 relative order.

## Canonical Pepper Identity

Pre-change P16.1 Pepper identity matched the committed P16.0 parent projection:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate | `6835` | `149992431` | `ff1f82524d64b86e5bc0a76f71a16144570fb83dc0d49ef6b5e61dfa271c419b` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

The existing integrity utility computes committed `HEAD` blob identity. Because P16.1 is not committed by the agent, the expected post-commit Pepper identity was computed with the same v2 record-stream algorithm over the current working-tree candidate set:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate post-commit projection | `6838` | `150069044` | `b5b134c74aad812e37774743823733354ac3d8a9305f02247c6c37c0afa0bb45` |
| Payload post-commit projection | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record post-commit projection | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Upstream payload changed: `false`. Baseline changed: `false`. New Pepper product files: `3`.

## Product Boundary

P16.1 adds no runtime routes, frontend code, provider configuration, credentials, workers, tool registrations, MCP servers, scheduler entries, repository mutation authority, dependency graph authority, ticket generation authority or WorkPacket authority.

All caller context is supplied in memory as `ContextSourceSpec.content`. `source_reference` values are descriptive provenance only. The assembler does not read repository files, inspect paths, fetch URLs, search the workspace, inspect Git, call tools, call providers, parse prompts, generate tickets or infer missing content.

## Public Package Paths

| Path | Purpose |
| --- | --- |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py` | Public Ticket Factory export boundary extended additively for P16.1. |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/context_packs.py` | Immutable P16.1 Context Pack Assembler contracts and pure assembly function. |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/specs.py` | Unmodified P16.0 ProjectSpec and TicketSpec contracts consumed by P16.1. |

`2_products/pepper-agent/hermes_cli/agent_platform/__init__.py` was not modified. No import-time registration or runtime discovery was added.

## P16.1 Public Exports

The P16.1 exports are additive and preserve relative order within the P16.1 subset:

| Export |
| --- |
| `CONTEXT_PACK_SCHEMA_VERSION` |
| `ContextSourceKind` |
| `ContextSensitivity` |
| `ContextPriority` |
| `OptionalSourceOverflowStrategy` |
| `ContextSourceSpec` |
| `ContextAssemblyPolicy` |
| `ContextAssemblyRequest` |
| `ContextPackItem` |
| `ContextPack` |
| `ContextPackAssemblyError` |
| `ContextPackBudgetError` |
| `ContextPackSensitiveContentError` |
| `assemble_context_pack` |

Duplicate exports: `0`. Private helpers exported: `0`. Import side effects: `0`.

## Schema Version

`CONTEXT_PACK_SCHEMA_VERSION = 1`. `ContextPack.schema_version` is fixed to `Literal[1] = 1`. Alternative context-pack schema versions are rejected. No version negotiation or migration exists.

## Enum Contracts

| Enum | Values |
| --- | --- |
| `ContextSourceKind` | `project_spec`, `ticket_spec`, `governance_record`, `repository_file`, `external_source`, `human_instruction`, `historical_ticket` |
| `ContextSensitivity` | `public`, `internal`, `sensitive`, `secret` |
| `ContextPriority` | `critical`, `high`, `normal`, `low` |
| `OptionalSourceOverflowStrategy` | `reject`, `truncate_then_omit`, `omit` |

Enum aliases: `0`.

## Source Contracts

`ContextSourceSpec` field order: `source_id`, `kind`, `title`, `source_reference`, `content`, `authority_references`, `sensitivity`, `priority`, `required`.

Source IDs match `^CTX-[A-Z0-9]+(?:-[A-Z0-9]+)*$`, reject whitespace without rewriting and are bounded at `96` characters. `CTX-PROJECT-SPEC` and `CTX-TICKET-SPEC` are reserved assembler-owned IDs. `project_spec` and `ticket_spec` source kinds are reserved assembler-owned kinds.

Caller source content is explicit, stripped, NUL-free and bounded at `32768` characters. Duplicate source IDs and duplicate source kind/reference pairs are rejected. Duplicate authority-reference kind/value pairs are rejected.

## Policy Contracts

`ContextAssemblyPolicy` field order: `max_items`, `max_total_characters`, `max_item_characters`, `optional_overflow_strategy`.

Defaults: `max_items=32`, `max_total_characters=65536`, `max_item_characters=16384`, `optional_overflow_strategy=truncate_then_omit`.

Bounds: `max_items` from `2` to `66`, `max_total_characters` from `4096` to `131072`, and `max_item_characters` from `256` to `32768`. `max_item_characters` must not exceed `max_total_characters`.

The policy contains no tokenizer, provider, model, prompt template, role selector, execution lane, filesystem root or path discovery setting.

## Assembly Request Contracts

`ContextAssemblyRequest` field order: `project_spec`, `ticket_spec`, `sources`, `policy`.

`project_spec.project_id` must equal `ticket_spec.project_id`. `sources` defaults to an empty tuple and is bounded to `64` caller sources. Mutable input sequences are normalized to tuples.

## Context Pack Contracts

`ContextPackItem` field order: `source_id`, `kind`, `title`, `source_reference`, `authority_references`, `sensitivity`, `priority`, `required`, `content`, `original_character_count`, `included_character_count`, `truncated`, `source_SHA256`, `included_SHA256`.

`ContextPack` field order: `schema_version`, `project_id`, `ticket_id`, `items`, `omitted_source_ids`, `truncated_source_ids`, `total_included_characters`, `policy`, `context_pack_SHA256`.

The first item is always `CTX-PROJECT-SPEC`. The second item is always `CTX-TICKET-SPEC`. Duplicate included item IDs, duplicate omitted IDs, duplicate truncated IDs, omitted/included overlap, truncated IDs not included, total-character mismatches and digest mismatches are rejected.

## Source Ordering

Caller sources are ordered after the two reserved items by required before optional, priority `critical`, `high`, `normal`, `low`, kind order `governance_record`, `repository_file`, `human_instruction`, `historical_ticket`, `external_source`, then `source_id` by ordinal code-point order.

Input order does not affect output order or the context-pack digest.

## Budget Behavior

Required sources include the two reserved items and caller sources with `required=true`. Required sources are never truncated or omitted. Required source overflow raises `ContextPackBudgetError` with source ID and category only.

Optional overflow behavior is controlled by `optional_overflow_strategy`:

| Strategy | Behavior |
| --- | --- |
| `reject` | Raise `ContextPackBudgetError` on optional overflow. |
| `omit` | Record overflowing optional source IDs in `omitted_source_ids`. |
| `truncate_then_omit` | Truncate optional oversized content when possible, otherwise omit. |

Truncated content ends with newline plus `[CONTEXT_TRUNCATED]`. The marker counts toward included characters. Total-budget truncation is allowed only when at least `128` characters remain.

## Sensitive Boundary

Caller sources marked `sensitive` or `secret` are rejected with `ContextPackSensitiveContentError`. P16.1 does not redact and continue.

The assembler also applies a bounded marker scan for private-key markers, OpenSSH private-key markers, bearer credential markers, token-assignment markers and long provider-key-shaped markers. Explicit placeholders such as `<REDACTED>`, `REDACTED`, `<SECRET>`, `synthetic-token`, `synthetic-access-token` and `synthetic-refresh-token` are allowed.

This scan is bounded heuristic protection only. It is not complete DLP.

## Digest Boundary

Every item records SHA-256 over UTF-8 for original source content and included content. Untruncated sources have equal original and included digests. Truncated sources have distinct digests.

The context-pack digest algorithm is `agent-platform-context-pack-sha256-v1`. The digest record includes schema version, project ID, ticket ID, ordered item metadata, ordered item source and included digests, omitted IDs, truncated IDs, total included characters and assembly policy. It excludes `context_pack_SHA256` itself.

The digest is reproducibility evidence only. It is not a canonical published ticket identity, approval signature, execution identity or security signature.

## Serialization Boundary

Allowed serialization behavior is standard Pydantic only: `model_dump()`, `model_dump_json()`, `model_validate()`, `model_validate_json()` and `model_json_schema()`.

Filesystem serialization, YAML support, Markdown rendering, file loaders and file writers are absent.

## Tests

Focused P16.1 command from `2_products/pepper-agent`:

```text
python -m pytest -q tests/hermes_cli/test_agent_platform_ticket_factory_context_packs.py -p no:cacheprovider
```

Result: `75` passed, `0` failed, `0` errors, `0` unexpected skips, `0` warnings reported.

Focused P16.0 command from `2_products/pepper-agent`:

```text
python -m pytest -q tests/hermes_cli/test_agent_platform_ticket_factory_specs.py -p no:cacheprovider
```

Result: `96` passed, `0` failed, `0` errors, `0` warnings reported.

Focused combined command from `2_products/pepper-agent`:

```text
python -m pytest -q tests/hermes_cli/test_agent_platform_ticket_factory_specs.py tests/hermes_cli/test_agent_platform_ticket_factory_context_packs.py -p no:cacheprovider
```

Result: `171` passed, `0` failed, `0` errors, `0` unexpected skips, `0` warnings reported.

Governance integrity command from repository root:

```text
python -B -m unittest discover -s "12_tests/governance" -p "test_pepper_baseline_integrity.py" -v
```

Result: `14` tests, `0` failures, `0` errors.

## Ruff Validation

| Command | Result |
| --- | --- |
| `python -m ruff format ...` | `1` P16.1 test file reformatted |
| `python -m ruff check ...` | `0` lint errors |
| `python -m ruff format --check ...` | `0` format errors |

Type validation: `ty_available: false`, `type_check: not_run_tool_unavailable`, `type_errors: not_asserted`, `dependency_installation: 0`.

## Static Boundary Scan

Focused import scan of `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/*.py` found no imports of `subprocess`, `socket`, `requests`, `httpx`, `openai`, `Path`, `os.environ`, `shutil`, `docker` or `git`.

Focused public-surface tests found no callable file loader, file writer, command executor, scheduler, publisher, WorkPacket, execution, runtime, provider request, prompt template, agent assignment or dependency graph surface.

File reads from P16.1 product code: `0`. File writes from P16.1 product code: `0`. Network calls: `0`. Subprocess calls: `0`. Git calls: `0`. Provider calls: `0`. Worker calls: `0`.

## Secret Scan

Placeholder-aware secret-shape scan across all `8` candidate files reported `SECRET_SHAPE_SCAN_OK` with `real_secret_shaped_findings=0`.

Synthetic test and documentation placeholders are limited to allowed values such as `<REDACTED>`, `<SECRET>`, `synthetic-access-token` and `synthetic-refresh-token`.

## Product File Hashes

| Path | SHA-256 |
| --- | --- |
| `hermes_cli/agent_platform/ticket_factory/__init__.py` | `c97462702e477f8ef20897dc81204aececf970bba0a835885d4b23ec59774484` |
| `hermes_cli/agent_platform/ticket_factory/context_packs.py` | `b947774c28044028468ae5e42f895462056d453cc005fed1987a5c7d48e3e529` |
| `tests/hermes_cli/test_agent_platform_ticket_factory_specs.py` | `0425ae4ecacec2ecd0fa85843c71fe68280318f60a8d5e8cd7157325891be9b3` |
| `tests/hermes_cli/test_agent_platform_ticket_factory_context_packs.py` | `bb38b96a5e1784cca28d153f4d2068c85dd54f8fdc8867f3bc8cb63f5c5c376b` |
| `docs/agent-platform/context_pack_assembler.md` | `2942f26a5db1a8bb0756bc6c313472652f4aa04ecfbead8ac8cc548e21ce562c` |
| `AGENT_PLATFORM_MODIFICATIONS.tsv` | `c253ee2f1a4068806dc2649ce0587e066b7c0f5568d3ad5153f4e101553323ba` |
| `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | `28244ce9b6891b58b3de2d95dd6ecabf5c22f5a3e37f3d730a93531040b6f4e1` |

## Modification Register

`2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` records three P16.1 product-addition rows: `P16.1-001`, `P16.1-002`, `P16.1-003`.

Existing P16.0 rows for `hermes_cli/agent_platform/ticket_factory/__init__.py` and `tests/hermes_cli/test_agent_platform_ticket_factory_specs.py` were updated to their current hashes and additive P16.1 intent. Duplicate modification IDs: `0`. Duplicate destination paths introduced by P16.1: `0`. Missing destination paths: `0`.

Focused test coverage correction updated the existing `P16.1-002` row hash only. New correction rows: `0`. Duplicate IDs: `0`. Unrelated rows modified by the correction: `0`.

## Import Manifest

`2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` records three new P16.1 product-addition rows for the new context-pack source, test and documentation files.

Existing manifest rows for `hermes_cli/agent_platform/ticket_factory/__init__.py` and `tests/hermes_cli/test_agent_platform_ticket_factory_specs.py` were updated to the current destination hashes. The governance record is not included in the Pepper import manifest.

Focused test coverage correction updated the existing `tests/hermes_cli/test_agent_platform_ticket_factory_context_packs.py` destination hash only. New correction rows: `0`. Duplicate concrete destinations introduced by the correction: `0`. Hash mismatches: `0`.

## Operational Counters

| Counter | Value |
| --- | ---: |
| filesystem reads by product code | `0` |
| filesystem writes by product code | `0` |
| subprocesses by product code | `0` |
| shell execution by product code | `0` |
| network calls by product code | `0` |
| provider calls by product code | `0` |
| OAuth actions by product code | `0` |
| credential access by product code | `0` |
| worker actions by product code | `0` |
| agent actions by product code | `0` |
| tool actions by product code | `0` |
| WorkPacket creation by product code | `0` |
| Git actions by product code | `0` |
| Graphify actions | `0` |
| Docker actions | `0` |

Pydantic validation, deterministic JSON materialization, in-memory sorting, bounded truncation and SHA-256 calculation are the only runtime behaviors introduced by P16.1 product code.

## Exact Candidate Set

Created Pepper product files:

| Status | Path |
| --- | --- |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/context_packs.py` |
| Added | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_ticket_factory_context_packs.py` |
| Added | `2_products/pepper-agent/docs/agent-platform/context_pack_assembler.md` |

Modified Pepper product files:

| Status | Path |
| --- | --- |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` |
| Modified | `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py` |
| Modified | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_ticket_factory_specs.py` |

Created governance record:

| Status | Path |
| --- | --- |
| Added | `0_architecture/governance/agent_platform_pepper_context_pack_assembler.md` |

Candidate formula: `3` created Pepper product files plus `4` modified Pepper product files plus `1` created governance record equals `8` candidates. Created files: `4`. Modified files: `4`. Deleted files: `0`. Unexpected candidates: `0`. Frontend candidates: `0`. Backend runtime candidates: `0`. Provider candidates: `0`. Worker candidates: `0`. Omniverse candidates: `0`. External source candidates: `0`. Graphify candidates: `0`. Dependency candidates: `0`.

## Deferred Responsibilities

P16.2 owns generator role taxonomy and role-specific Context Pack consumption. P16.3 owns dependency DAGs, cycle detection, topological ordering and parallel wave planning. P16.4 owns ticket policy and linting. P16.5 owns multi-generator synthesis and conflict review. P16.6 owns human approval and canonical publishing. WorkPacket execution remains deferred to P17.

## Residual Constraints

| Item | State |
| --- | --- |
| ProjectSpec modified | `false` |
| TicketSpec modified | `false` |
| ContextPack persisted | `false` |
| ContextPack executable | `false` |
| repository file loading | absent |
| URL fetching | absent |
| semantic search | absent |
| prompt rendering | absent |
| ticket generation | absent |
| dependency graph | absent |
| parallel planner | absent |
| human approval | absent |
| WorkPacket | absent |
| agent assignment | absent |
| provider access | absent |
| credential access | absent |
| runtime routes | `0` |
| product UI | disabled |
| Graphify | not run by P16.1 instruction |
| production readiness | not claimed |

Canonical verdict occurrences in this record: `1`. Alternative P16.1 verdict occurrences: `0`.

## Final Verdict

hermes_0_19_pepper_context_pack_assembler_ready_with_bounded_in_memory_authority
