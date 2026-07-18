# GRAPHIFY-SCALE-01 - Scalable Hermes Graphify Refresh Pipeline

## Document Header

| Field | Value |
| --- | --- |
| Ticket | GRAPHIFY-SCALE-01 |
| Status | Accepted with recorded constraints |
| Date | 2026-07-18 |
| Result marker | `graphify_scalable_hermes_pipeline_ready_with_constraints` |
| Repository commit | `a42768937432c3e609c516208ef1184058f6dcc2` |
| Graphify version | `0.9.5` |
| Selected implementation | Path B, maintained version-pinned Python APIs |
| Maintained adapter | `10_scripts/graphify/refresh_hermes_graph.py` |
| Adapter SHA-256 | `f1ba45c6c9f8bfbf1a6dd35d791ce78c29a32ae6c3e93fcbe4ddf393ae4654b2` |
| Accepted provenance SHA-256 | `952a9f58997bb72974ef73a636d01800bf6f1c2862a6fa03044556d150ee6550` |
| Evidence root | `C:\Users\pablo\AppData\Local\Temp\agent-platform-graphify-scale-01-final-20260717-r2` |
| Generated output | `graphify-out/**`, local and untracked |

## Decision

GRAPHIFY-SCALE-01 establishes the maintained deterministic AST-only refresh
path required by the GRAPHIFY-SCOPE-01 closure. The accepted pipeline uses
Graphify 0.9.5 detection, sensitive filtering, extractors, graph builders,
source-replacement merge behavior, validation, serialization, clustering and
HTML export. It adds orchestration and evidence gates but does not invent AST
nodes, relationship types or IDs.

The pipeline is accepted for local generated supporting evidence under the
constraints in this record. It does not make Graphify an architecture authority,
source of truth, approval engine, semantic-memory substrate, runtime input or
deployment artifact.

## Path Selection

The official primary command was attempted first in an isolated repository
clone:

```text
graphify update .
```

It ran for 1,050.477 seconds and reached the official shrink guard with 151,055
nodes versus the 151,851-node seed. Graphify refused to overwrite the seed and
the workspace output remained unchanged. This made Path A unsuitable for the
governed refresh without weakening the installed guard.

Path B uses the following Graphify 0.9.5 interfaces:

- installed ignore, sensitivity, classification and extractor dispatch;
- `graphify.extract.extract` for official AST extraction;
- `graphify.build.build_from_json` for full graph construction;
- `graphify.build.build_merge` for source replacement and deletion pruning;
- `graphify.validate.validate_extraction` for installed schema checks;
- `graphify.export.to_json` for structured serialization;
- official `cluster-only` and `export html` commands for derived outputs.

`build_merge` is maintained by Graphify's incremental implementation but is not
top-level API with a version-stability guarantee. The adapter therefore pins
Graphify exactly to 0.9.5 and fails closed on another version.

## Scope And Inventory

The accepted inventory is generated from `git ls-files`, the installed
`.graphifyignore` parser, the installed sensitive-path filter and installed
extractor dispatch. Symlinks and repository-root escapes are denied.

| Inventory class | Count |
| --- | ---: |
| Tracked paths classified | 6,416 |
| Accepted sources | 5,881 |
| Ignored paths | 165 |
| Sensitive paths | 26 |
| Unsupported paths | 344 |
| Lexicographic cache-priming batches | 12 |

Inventory hashes:

```text
accepted     5aa9d1cb39ec68cb9751ef77a8e586a06d3ed6b20b61dd1d56fa151dfdb37519
ignored      fe55a83b472640c702e0435ef66c88ec469bebc8ac8bbf3720b073d426ae2abe
sensitive    cd283650e29d1a94fc18b97f91275f2e94fb225bee3a91f1aa01f92ac8ea5241
unsupported  d86884d282da8c2977ce5ce6e26e93bac486cb38faf893373de9ee4fffdbd405
batches      77bfd3fa31cb7f13b8ccb0467969a81504780865f2e810398c801ab4045abc96
```

The official `manifest.json` contains exactly the 5,881 accepted source paths.
The final graph represents 5,837 sources with nodes. The remaining 44 are valid
data-shaped JSON files that emitted zero nodes in both cached extraction and a
fresh maintained-extractor audit. Non-JSON, malformed JSON and structural JSON
are not eligible for zero-node acceptance.

## Deterministic Pipeline Contract

Each full run performs these operations:

1. Build and persist the immutable authorized, ignored, sensitive, unsupported
   and batch manifests.
2. Prime the Graphify AST cache in 500-file lexicographic batches while
   recording raw extraction, process, parser-failure and cache-read evidence.
3. Run one official full-corpus extraction to resolve cross-file relationships.
4. Build, validate and serialize through installed Graphify APIs.
5. Require the final source coverage to equal the immutable per-batch ledgers.
6. Rebuild the repository inventory before accepting the run.
7. Persist process exit status, timeout, duration, CPU, memory, stdout and stderr
   hashes, graph hashes and normalized structural fingerprints.

Incremental refresh uses a temporary graph, `build_merge`, explicit changed and
deleted source pruning, full validation and atomic replacement. It invalidates
stale clustering, HTML, report, labels and provenance after a graph mutation.
Deletion, rename, newly ignored, changed and zero-node sources are covered by
integration tests.

## Baseline Preservation

The governed baseline run accepted 194 sources and completed in 20.170 seconds.
It produced 5,320 nodes and 6,365 relationships. Direct normalized comparison
against `cold_run_1` found zero missing baseline nodes, relationships or
hyperedges, and equal `directed` and `multigraph` semantics.

```text
baseline normalized graph  a01c15d6eddeecb5f221a72182dc6729260b119fd8462d37154fdd0b111de0fd
baseline graph.json        d6cabade197af150fcf2b59cf57a11cc5fd4fd9d6e0baefa683f4c9b0ba34bc8
baseline comparison        accepted
```

The comparator binds the baseline and full run-result files, official
manifests, current inventories, graph hashes, structural integrity, source
coverage and fresh zero-node evidence. An empty or partial baseline cannot pass.

## Four-Run Evidence

Two cold and two warm runs used distinct graph files and one unchanged script,
commit, policy and authorized inventory.

| Run | Mode | Duration seconds | Peak memory bytes | Largest operation seconds |
| --- | --- | ---: | ---: | ---: |
| `cold_run_1` | cold | 727.665 | 3,579,125,760 | 237.804 |
| `cold_run_2` | cold | 730.599 | 3,579,686,912 | 237.488 |
| `warm_run_1` | warm from `cold_run_1` | 735.464 | 3,579,174,912 | 214.522 |
| `warm_run_2` | warm from `cold_run_2` | 743.018 | 3,579,555,840 | 216.108 |

Both cold runs began with an empty cache and produced the same 4,599-file cache
tree. Each warm run consumed the exact paired cold cache hash. Cold priming
recorded zero hits; warm priming recorded 4,598 successful reads. Every run
recorded 4,598 successful full-corpus cache reads.

All five determinism checks match across all four runs:

```text
node ID set                 48546e3294c06160b8b37af73dbf798c759a6d8c52dc55394c85b814e8061422
node content                0388984615f8069297049037aeb2b4159bb4568bd1c3df93cfc94f2598936f15
relationship endpoint/type 4c6692ade40831a39815daf75fd05487e0dc49314e1d20bdacbdc9d4e6f9b5a1
relationship content       08c22cb57b24f73e3ed683c67c26e7857e87fd4d8262a82d1b965d11e850b977
complete normalized graph  f29fd1e8eb903a638aad0f8bbece34f0cbd22bcab58000365678c321d86609e5
```

Every run produced 151,132 nodes, 263,635 relationships and zero hyperedges.
The determinism comparison SHA-256 is
`ec4a2de6197742e0fd2585acb75912e77be486cf7604a7897c95f09ac5c83b8d`.

## Structural And Scope Validation

Every accepted run reported zero for:

- duplicate or missing node IDs;
- duplicate relationships or dangling endpoints;
- invalid nodes or relationships;
- absolute, noncanonical, unresolved, unauthorized or unmanifested sources;
- Graphify self-ingestion, artifacts, external sources and sibling products;
- dependency, virtual-environment, generated-output and sensitive sources;
- parser failures and process timeouts.

Source-path validation includes nodes, relationships and hyperedges. Rooted,
drive-qualified, traversal and noncanonical paths fail before promotion.

## Finalization And Promotion

Finalization copied only `graph.json`, `manifest.json` and
`scale-manifest.json` from the immutable `warm_run_2` output into a fresh
candidate. Official clustering completed in 83.504 seconds and official HTML
export completed in 2.824 seconds. Structural fingerprints remained unchanged.

The final graph has 5,257 communities, 39,362 underlying cross-community
relationships and 11,729 unique community-pair edges in the aggregated HTML.
Labels, membership signatures, report counts, HTML counts and the sanitized
HTML title were recomputed and validated against `graph.json`.

Promotion copied only the eight canonical direct artifacts into an owned random
snapshot, validated that snapshot against all external evidence, copied it into
a second atomic staging directory, rechecked the current source inventory, and
atomically replaced `graphify-out`. A post-replacement inventory and graph check
also passed. Cache files and path-bearing cache metadata were not promoted.

## Final Artifacts

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `graph.json` | 201,495,538 | `02e3e4c8b32e77e6e71d8f6fdfb5cc647309b55713a3327c2534c2dace0291a2` |
| `graph.html` | 4,785,040 | `11aa574b4ee13eefe39dadcb727b4b6a8db0fb366fa9bbe0795cc935bad4a9ab` |
| `GRAPH_REPORT.md` | 1,986,661 | `05d042edd217fec84ec9cdf2c55293e607a378ca9c3f7f6176666583d271136a` |
| `manifest.json` | 1,165,071 | `bbf87d853cc9a31f3753bbc9a198ce4193c53ed96c6cc7964c0b1fe156798f59` |
| `scale-manifest.json` | 2,842,995 | `b89c204ce02be8226ea203b9478032820189cc4244d3b552c540d2096aa8d0ae` |
| `.graphify_labels.json` | 183,260 | `faddd4e3a5fb787d48e8b2dedbac8121dcbb7f4e6841e590936ac845762b35d0` |
| `.graphify_labels.json.sig` | 146,086 | `5d87d53d4fb52e516b102fdf6617009489d8ff4637c2548902066b8b165f79e1` |
| `provenance.json` | 55,438 | `952a9f58997bb72974ef73a636d01800bf6f1c2862a6fa03044556d150ee6550` |

The pre-promotion 4,646-file output remains at
`C:\Users\pablo\AppData\Local\Temp\agent-platform-graphify-scale-01-final-20260717-r2\pre-promotion-backup`.
Its `graph.json` SHA-256 remains
`cb04d5dfdb1414bc40977233c10564c5ab3687400a3ce14e96c1e0c984122d86`.
The earlier complete rollback copy is also retained until ticket cleanup is
explicitly authorized.

## Verification

The maintained implementation passed:

- 24 unit tests;
- two end-to-end integration tests using real Graphify extraction and merge;
- Ruff lint and formatting checks;
- repeated independent reviews of provenance, promotion, baseline, source-path,
  zero-node, cache and rollback gates.

The Hermes product files and locked upstream were not modified. No provider or
model was called. No file was staged, committed or pushed, and P13.7 was not
started.

## Constraints

- Graphify is pinned to 0.9.5 because the maintained Python interfaces used by
  Path B are not stability-versioned top-level APIs.
- Semantic provider or network-backed extraction remains prohibited and was not
  performed.
- Community assignments and HTML layout are derived outputs and are excluded
  from structural determinism hashes, then independently validated during
  finalization.
- The generated graph remains local supporting evidence and confers no runtime,
  approval, publication, deployment or semantic-authority status.

## Final Verdict

GRAPHIFY-SCALE-01 is accepted with the constraints above. It supersedes the
GRAPHIFY-SCOPE-01 fallback limitation and authorizes the maintained adapter as
the reproducible local Hermes AST refresh path for Graphify 0.9.5.

Result marker:

```text
graphify_scalable_hermes_pipeline_ready_with_constraints
```
