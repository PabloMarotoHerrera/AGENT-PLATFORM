# Context Pack Assembler

P16.1 adds a deterministic, bounded and in-memory Context Pack Assembler for Pepper Ticket Factory planning. It builds on the P16.0 `ProjectSpec` and `TicketSpec` contracts and produces an immutable `ContextPack` from one project, one ticket, explicitly supplied context sources and an explicit assembly policy.

The context pack is not a prompt, generated ticket, WorkPacket, approval record, publication record or execution plan. P16.1 performs no filesystem loading, network retrieval, semantic search, provider calls, tool calls, dependency planning or ticket generation.

## Relationship To P16.0

P16.0 owns `ProjectSpec` and `TicketSpec`. P16.1 consumes those immutable planning specs, materializes each as deterministic JSON and preserves their authority references in the reserved project and ticket context items.

P16.1 does not change the P16.0 schema module. It adds context-pack contracts and the `assemble_context_pack()` function under the existing `ticket_factory` package export boundary. The inherited P16.0 focused export test now uses additive export preservation so later Ticket Factory tickets can add public exports while preserving P16.0 exports and relative order.

## In-Memory Authority

All source content is supplied by the caller as `ContextSourceSpec.content`. Repository-file references and external-source references are descriptive provenance only. The assembler does not read paths, resolve URLs, fetch content, inspect Git, call connected services, inspect workspace data or infer missing source content.

## Controlled Enums

| Enum | Values |
| --- | --- |
| `ContextSourceKind` | `project_spec`, `ticket_spec`, `governance_record`, `repository_file`, `external_source`, `human_instruction`, `historical_ticket` |
| `ContextSensitivity` | `public`, `internal`, `sensitive`, `secret` |
| `ContextPriority` | `critical`, `high`, `normal`, `low` |
| `OptionalSourceOverflowStrategy` | `reject`, `truncate_then_omit`, `omit` |

Caller sources may use `governance_record`, `repository_file`, `external_source`, `human_instruction` and `historical_ticket`. `project_spec` and `ticket_spec` are reserved for assembler-generated items.

## ContextSourceSpec

Field order: `source_id`, `kind`, `title`, `source_reference`, `content`, `authority_references`, `sensitivity`, `priority`, `required`.

| Field | Contract |
| --- | --- |
| `source_id` | `CTX-` identifier matching `^CTX-[A-Z0-9]+(?:-[A-Z0-9]+)*$`, max length `96` |
| `kind` | `ContextSourceKind` |
| `title` | bounded title, max `256` characters |
| `source_reference` | bounded inert reference, max `1024` characters |
| `content` | explicit bounded content, max `32768` characters |
| `authority_references` | tuple of P16.0 `AuthorityReferenceSpec`, default empty |
| `sensitivity` | `ContextSensitivity`, default `internal` |
| `priority` | `ContextPriority`, default `normal` |
| `required` | strict boolean, default `false` |

Reserved source IDs `CTX-PROJECT-SPEC` and `CTX-TICKET-SPEC` are rejected for caller sources. Duplicate authority-reference kind/value pairs are rejected. Source content is never loaded by the product code.

## ContextAssemblyPolicy

Field order: `max_items`, `max_total_characters`, `max_item_characters`, `optional_overflow_strategy`.

Defaults: `max_items=32`, `max_total_characters=65536`, `max_item_characters=16384`, `optional_overflow_strategy=truncate_then_omit`.

Bounds: `max_items` from `2` to `66`, `max_total_characters` from `4096` to `131072`, `max_item_characters` from `256` to `32768`. `max_item_characters` must not exceed `max_total_characters`. Character counts are Python Unicode string lengths; token counting is deferred.

The policy contains no tokenizer, model name, provider, temperature, prompt template, agent role, execution lane or filesystem root.

## ContextAssemblyRequest

Field order: `project_spec`, `ticket_spec`, `sources`, `policy`.

The request requires one P16.0 `ProjectSpec`, one P16.0 `TicketSpec`, a tuple of caller sources and an assembly policy. `sources` defaults to an empty tuple and is capped at `64` caller sources. `policy` defaults to `ContextAssemblyPolicy()`.

`project_spec.project_id` must equal `ticket_spec.project_id`. Source IDs must be unique. Source kind/reference pairs must be unique. Identifiers are not inferred or rewritten.

## ContextPackItem

Field order: `source_id`, `kind`, `title`, `source_reference`, `authority_references`, `sensitivity`, `priority`, `required`, `content`, `original_character_count`, `included_character_count`, `truncated`, `source_SHA256`, `included_SHA256`.

`source_SHA256` is the SHA-256 digest of the full original source content encoded as UTF-8. `included_SHA256` is the SHA-256 digest of the exact included content. `original_character_count` and `included_character_count` use Python string lengths. `truncated` is true only when included content differs from original content due to policy.

## ContextPack

Field order: `schema_version`, `project_id`, `ticket_id`, `items`, `omitted_source_ids`, `truncated_source_ids`, `total_included_characters`, `policy`, `context_pack_SHA256`.

`schema_version` is fixed at `1`. The first item is always `CTX-PROJECT-SPEC`; the second item is always `CTX-TICKET-SPEC`. Duplicate item IDs, duplicate omitted IDs, duplicate truncated IDs, omitted/included overlap, truncated-but-not-included IDs and total-character mismatches are rejected.

The context pack has no prompt, messages, agent, provider, model, tool configuration, runtime state, execution command, WorkPacket, approval state or publication state.

## Public Exceptions And Assembler

`ContextPackAssemblyError` is the base assembly error. `ContextPackBudgetError` reports bounded policy failures. `ContextPackSensitiveContentError` reports sensitive-source posture or bounded secret-shaped marker failures. Error messages identify source IDs and failure categories but do not reproduce source content.

`assemble_context_pack(request)` returns a `ContextPack`. It is pure in-memory and deterministic, and does not mutate the request.

## Reserved Materialization

The assembler always creates two required internal, critical items first:

| Source ID | Kind | Title | Reference |
| --- | --- | --- | --- |
| `CTX-PROJECT-SPEC` | `project_spec` | `ProjectSpec <project_id>` | `ProjectSpec:<project_id>` |
| `CTX-TICKET-SPEC` | `ticket_spec` | `TicketSpec <ticket_id>` | `TicketSpec:<ticket_id>` |

The source content is deterministic JSON from `model_dump(mode="json")` encoded with `ensure_ascii=False`, compact separators and `sort_keys=True`. This is the context materialization format only. It is not canonical published ProjectSpec format, canonical published TicketSpec format, canonical ticket identity or human-readable ticket rendering.

## Source Ordering

Caller sources are sorted after the two reserved items by required sources before optional sources, priority `critical`, `high`, `normal`, `low`, canonical kind order `governance_record`, `repository_file`, `human_instruction`, `historical_ticket`, `external_source`, then `source_id` by ordinal code-point order.

Input order does not affect output order or context-pack digest. Filesystem order and insertion order are not authority.

## Budget Behavior

Required sources include the two reserved items and caller sources with `required=true`. Required sources are never truncated or omitted. Required source per-item overflow, total overflow or item-count overflow raises `ContextPackBudgetError`.

Optional sources follow `optional_overflow_strategy`. `reject` raises `ContextPackBudgetError` on per-item overflow, total overflow or item-count overflow. `omit` records overflowing optional source IDs in `omitted_source_ids`. `truncate_then_omit` truncates oversized optional content when possible and otherwise omits.

The truncation marker is a newline followed by `[CONTEXT_TRUNCATED]`, and it counts toward included characters. For total-budget overflow, truncation is allowed only when at least `128` characters of budget remain. If the source cannot include at least one original content character plus the full marker, it is omitted. Omitted and truncated IDs follow deterministic caller-source order.

## Sensitive And Secret Marker Boundary

Caller sources marked `sensitive` or `secret` are rejected with `ContextPackSensitiveContentError`, whether required or optional. P16.1 does not perform automatic redaction.

The assembler applies a bounded marker scan to materialized source content for private-key markers, bearer credential markers, token-assignment markers and long provider-key-shaped markers. Explicit placeholders such as `<REDACTED>`, `REDACTED`, `<SECRET>`, `synthetic-token`, `synthetic-access-token` and `synthetic-refresh-token` are allowed.

This is a bounded heuristic only. It is not complete DLP and does not claim complete secret detection.

## Digests

Every item records SHA-256 over UTF-8 for original source content and included content. Unchanged sources have equal source and included digests. Truncated sources have distinct source and included digests.

The context-pack digest algorithm is `agent-platform-context-pack-sha256-v1`. The digest record includes schema version, project ID, ticket ID, ordered item metadata, ordered item source and included digests, omitted IDs, truncated IDs, total included characters and assembly policy. It excludes `context_pack_SHA256` itself.

The digest is provenance and reproducibility evidence. It is not canonical published ticket identity, approval signature, execution identity or security signature.

## JSON Behavior

Standard Pydantic `model_dump()`, `model_dump_json()`, `model_validate()`, `model_validate_json()` and `model_json_schema()` are supported. JSON arrays are normalized to tuples. Filesystem serialization, YAML support, Markdown rendering, file loaders and file writers are absent.

## Synthetic Request Example

```python
from hermes_cli.agent_platform.ticket_factory import (
    ContextAssemblyPolicy,
    ContextAssemblyRequest,
    ContextSourceKind,
    ContextSourceSpec,
    assemble_context_pack,
)

source = ContextSourceSpec(
    source_id="CTX-GOV-P16",
    kind=ContextSourceKind.GOVERNANCE_RECORD,
    title="Synthetic governance note",
    source_reference="0_architecture/governance/example.md",
    content="Synthetic context supplied directly by the caller.",
    required=True,
)

request = ContextAssemblyRequest(
    project_spec=project_spec,
    ticket_spec=ticket_spec,
    sources=(source,),
    policy=ContextAssemblyPolicy(max_items=8),
)
pack = assemble_context_pack(request)
```

## Synthetic Output Summary

A valid pack begins with `CTX-PROJECT-SPEC`, then `CTX-TICKET-SPEC`, then sorted caller sources. It reports omitted and truncated source IDs, total included characters, item digests and one context-pack digest.

## Failure Examples

A required source larger than `max_item_characters` raises `ContextPackBudgetError` and names only the source ID and budget category.

A caller source marked `secret` raises `ContextPackSensitiveContentError` and does not include source content in the error.

## Deferred P16 Responsibilities

P16.2 owns generator role taxonomy and role-specific Context Pack consumption. P16.3 owns dependency DAGs, cycle detection, topological ordering and parallel wave planning. P16.4 owns ticket policy and linting. P16.5 owns multi-generator synthesis and conflict review. P16.6 owns human approval and canonical publishing. WorkPacket execution remains deferred to P17.
