# External Source Root Normalization

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | External Source Root Normalization |
| Ticket | P9.1 |
| Status | Accepted External Source Root Normalization |
| Date | 2026-07-07 |
| Scope | Governance-only external source root normalization for AGENT PLATFORM / Siamese under the External Tool Integration Program. |
| Authority | External source root normalization only, not source inspection, not dependency approval, not external tool adoption, not execution, not adapter implementation, not runtime activation, not provider/API/MCP activation, not product/Siamese source inspection, not Git automation, not path migration execution, and not publication. |
| Prerequisite | P9.0 accepted at `0_architecture/governance/agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md`. |
| Canonical root | `4_external/sources` |
| Legacy root | `external/sources` |
| Known GStack path/class metadata | `4_external/sources/gstack-main` as path/class metadata only. |
| Related documents | P9.0, P8.R, P8.0-P8.R, P7.R, P6.R/P6.7, P5.R, P3.BR, P2.2/P2.3, P1 boundaries, P0 gates, S-03/S-04. |
| Output | External Source Root Normalization |
| Result marker | `external_source_root_normalization_ready` |

## 2. Purpose

P9.1 freezes the canonical external source root for the post-P8 External Tool Integration Program.

P9.1 prevents recurrence of `external/sources` versus `4_external/sources` drift. P9.1 normalizes known external candidate path handling, defines path-only metadata rules, defines legacy path handling, and defines stop rules for source inspection, listing, execution, adoption, and path migration.

P9.1 prepares P9.2-P9.6, P10, P11, P12, P13, and P14. P9.1 does not inspect external source contents. P9.1 does not move files. P9.1 does not create adapters. P9.1 does not execute tools. P9.1 does not mutate Git.

## 3. Current Posture

`4_external/sources` is canonical. `external/sources` is legacy.

| Area | Current state | P9.1 interpretation | Blocked interpretation |
| --- | --- | --- | --- |
| P8.R closure | MVP-0 closed as manual/non-executing readiness. | P9.1 inherits no runtime, no external adoption, and no Git automation readiness. | Runtime readiness or external runtime adoption readiness. |
| P9.0 charter | External integration charter accepted. | P9.1 follows adopt/adapt/wrap-before-rebuild under future gates. | P9.1 source inspection, execution, adoption, or adapter authorization. |
| Canonical source root | `4_external/sources` exists as canonical root. | Use as CanonicalExternalSourceRoot. | Source inspection permission or dependency approval. |
| Legacy source root | `external/sources` is absent or legacy/superseded. | Mention only as LegacyExternalSourceRoot drift reference. | Current canonical root, mandatory current input, or blocker if absent. |
| GStack path | `4_external/sources/gstack-main` exists. | Record as GStackPathClassMetadata and PathOnlyMetadata only. | GStack inspected, listed, imported, executed, configured, adopted, wrapped, forked, vendored, patched, or integrated. |
| Graphify candidate path | Not normalized by P9.1 beyond future owner. | `path_unknown_pending_authorized_inventory` until P10/P9 gates. | Graphify runtime active or Graphify execution. |
| Hermes candidate path | Not normalized by P9.1 beyond future owner. | `path_unknown_pending_authorized_inventory` until P11. | Hermes runtime active or Hermes source inspection. |
| GBrain candidate path | Not normalized by P9.1 beyond future owner. | `path_unknown_pending_authorized_inventory` until P12. | GBrain runtime active or GBrain source inspection. |
| ECC-main candidate path | Not normalized by P9.1 beyond future owner. | `path_unknown_pending_authorized_inventory` until P13. | ECC-main runtime active, execution, or agent OS activation. |
| OpenCode candidate path | Not normalized by P9.1 beyond future owner. | Preserve H0/user-operated harness boundary. | OpenCode source inspection or AGENT PLATFORM execution. |
| Provider/API/MCP | Blocked by security/local policies. | Future gated integration class only. | Provider/API/MCP active, credential use, or API/MCP calls. |
| Product/Siamese | Siamese remains product vision. | Product/Siamese source is outside P9.1 normalization. | Product/Siamese source readable by default. |
| Git automation | User-owned Git authority. | P9.1 may provide exact commit advice only. | Agent staging, commit, push, force-add, publication, or `git add .`. |
| Source inspection | Not authorized. | P9.3 must define source inspection gates. | Source tree scan, content review, automatic source ingestion. |
| Source execution | Not authorized. | P9.4 must define execution gates. | External tool runtime active. |
| Adapter implementation | Not authorized. | P9.5 and later gates must decide adoption mode first. | Adapter implementation by P9.1. |

## 4. Inputs Reviewed

Inputs were reviewed only through allowed governance checks and path-only metadata checks. External source roots were checked only with `Test-Path`; no directory was listed, enumerated, imported, executed, configured, adopted, or inspected.

| Input group | Document/path | Review mode | P9.1 use | Limitation |
| --- | --- | --- | --- | --- |
| P9.0 charter | `0_architecture/governance/agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md` | charter_review | Confirms P9.0 prerequisite and adopt/adapt/wrap posture. | No P9.0 modification. |
| P8 external boundary docs | P8.0 external boundary, external source inventory, security activation gate, Graphify boundary, GBrain/GStack boundary, Hermes boundary, OpenCode boundary, MVP-0 synthesis, MVP-0 implementation authorization, MVP-0 skeleton package | governance_markdown_review | Provides baseline boundaries and candidate context. | No older document modified. |
| P7/P6/P5/P3/P2/P1/P0 baseline docs | Manual workflow closure, reviewer mesh, harness strategy, audits, reconciliation closures, metadata/evidence contracts, rollback baseline, runtime/provider/tool/agent hardening, Cognitive Semantic System hardening, activation/validation/security hardening | governance_markdown_review | Confirms inherited governance posture. | No baseline document modified. |
| S-03/S-04 policies | `0_architecture/security/agent_platform_local_only_secrets_credentials_policy.md`; `0_architecture/security/agent_platform_tool_shell_network_mcp_execution_policy.md` | security_policy_review | Confirms secrets, credentials, shell, network, MCP, and tool execution remain gated. | No security enforcement activated. |
| Canonical external root path | `4_external/sources` | path_only_metadata_check | Confirms CanonicalExternalSourceRoot path reference. | Path presence is not source inspection permission. |
| Legacy external root path | `external/sources` | legacy_path_reference_check | Classifies as LegacyExternalSourceRoot only. | Absence must not block future tickets. |
| GStack path | `4_external/sources/gstack-main` | path_only_metadata_check | Records GStackPathClassMetadata. | No inspection, listing, import, execution, configuration, adoption, or dependency approval. |
| External source contents | All external source contents | not_reviewed_blocked | Not reviewed by P9.1. | Requires future P9.3 or candidate-specific source gate. |

## 5. Root Normalization Decision

Definitions:

- `CanonicalExternalSourceRoot`: the current approved external source root for AGENT PLATFORM external source references.
- `LegacyExternalSourceRoot`: a superseded historical path reference that must not be used as current canonical root.
- `ExternalSourceRootPolicy`: root policy metadata defining canonical status, legacy status, allowed path-only checks, and blocked interpretations.
- `ExternalSourcePathRef`: a normalized path reference to an external candidate, never content permission by itself.
- `ExternalSourceRootStatus`: root status vocabulary: `canonical`, `legacy_superseded`, `absent_legacy_ok`, `path_unknown_pending_authorized_inventory`, `blocked_as_permission`.

| Root | Status | Allowed use | Blocked use | Future migration requirement |
| --- | --- | --- | --- | --- |
| `4_external/sources` | `canonical` CanonicalExternalSourceRoot | Current external source root reference for post-P8 tickets; exact path-only checks. | Inspecting contents, listing children, dependency approval, adoption, execution, adapter authorization, runtime authorization. | All post-P8 tickets must reference this root when referring to external source roots. |
| `external/sources` | `legacy_superseded` LegacyExternalSourceRoot | Historical/legacy path note only to prevent drift. | Current canonical root, mandatory current root, source inspection basis, dependency approval basis, migration command target. | Future prompts using this as current root must mark `legacy_external_root_path_drift` and normalize to `4_external/sources`. |
| Unknown candidate root | `path_unknown_pending_authorized_inventory` | Record as unknown until authorized inventory. | Guessing paths, listing roots, source tree scan, automatic source ingestion. | Future ticket owner must define exact path inventory scope under gate. |

Required decisions:

- `4_external/sources` is canonical.
- `external/sources` is legacy/superseded.
- All post-P8 tickets must reference `4_external/sources`.
- Legacy `external/sources` may appear only as a historical or legacy path note.
- No ticket may stop because `external/sources` is absent.
- No ticket may use `external/sources` as the current external root.
- No ticket may inspect external source contents based only on root existence.

## 6. External Candidate Path Records

`ExternalCandidatePathRecord` records candidate path metadata without approving content inspection, dependency review, execution, adoption, adapters, runtime, or Git automation.

| Candidate | Normalized path | Path status | Inspection status | Execution status | Adoption status | Future ticket owner |
| --- | --- | --- | --- | --- | --- | --- |
| Graphify | `path_unknown_pending_authorized_inventory` | pending future authorized inventory | not inspected | not executed | not adopted | P10 |
| Hermes | `path_unknown_pending_authorized_inventory` | pending future authorized inventory | not inspected | not executed | not adopted | P11 |
| GBrain | `path_unknown_pending_authorized_inventory` | pending future authorized inventory | not inspected | not executed | not adopted | P12 |
| GStack | `4_external/sources/gstack-main` | PathOnlyMetadata | not inspected | not executed | not adopted | P12 |
| ECC-main | `path_unknown_pending_authorized_inventory` | pending future authorized inventory | not inspected | not executed | not adopted | P13 |
| OpenCode | `path_unknown_pending_authorized_inventory` | pending future authorized inventory | not inspected | not executed by AGENT PLATFORM | not adopted | Later OpenCode/H0 gate |
| Codegraph, if considered | `path_unknown_pending_authorized_inventory` | pending future authorized inventory | not inspected | not executed | not adopted | P10/P14 or later gate |
| Provider/API/MCP surfaces | not an external source root path by P9.1 | blocked pending policy gate | not inspected | not activated | not adopted | P9.4/P9.5 or later provider gate |
| Product/Siamese external-like surfaces | not part of P9.1 external root normalization | blocked pending product gate | not inspected | not executed | not integrated | P4 / GT-09 or equivalent plus P9/P10+ gates |

`GStackPathClassMetadata`:

```yaml
ExternalCandidatePathRecord:
  candidate: GStack
  normalized_path: 4_external/sources/gstack-main
  path_status: PathOnlyMetadata
  inspection_status: not_inspected
  execution_status: not_executed
  adoption_status: not_adopted
  future_ticket_owner: P12
```

## 7. Path-Only Metadata Policy

`PathOnlyMetadata` may record whether a path exists, a known path/class label, a candidate owner, and a future gate owner.

`PathOnlyMetadata` may not inspect contents, list children, import code, execute code, approve dependency use, approve an adapter, or approve runtime.

Path presence is not content inspection permission. Path presence is not dependency approval. Path presence is not adoption. Path presence is not execution.

| Allowed path-only action | Blocked action | Reason | Future gate |
| --- | --- | --- | --- |
| Record `Test-Path` result for `4_external/sources`. | Do not inspect root contents. | Root existence only normalizes references. | P9.3 source inspection gate. |
| Record `Test-Path` result for `4_external/sources/gstack-main`. | Do not list GStack. | GStack path/class metadata is not source review. | P12 source review authorization. |
| Record known candidate owner. | Do not adopt candidate by path. | Ownership only routes future tickets. | P9.5 adoption mode gate. |
| Record future gate owner. | Do not execute candidate by path. | Execution requires a separate model. | P9.4 execution gate. |
| Record legacy path status. | Do not migrate, move, rename, copy, symlink, or submodule paths. | P9.1 is not path migration execution. | Future explicit migration plan, if needed. |

## 8. Legacy Path Handling Policy

`external/sources` is legacy. The legacy path may be mentioned only to prevent drift. Legacy path absence must not block future tickets. Legacy path presence must not authorize inspection.

Future tickets must not request `external/sources` as a mandatory current input. If a future prompt uses `external/sources`, mark `legacy_external_root_path_drift` and normalize to `4_external/sources`.

| Legacy scenario | Required handling | Stop rule if unresolved |
| --- | --- | --- |
| Prompt names `external/sources` as current canonical root. | Reject as legacy path drift and normalize to `4_external/sources`. | Stop if user insists on legacy root as current canonical root. |
| Prompt requires `external/sources` as mandatory current root. | Treat as invalid mandatory input and request/record correction. | Stop if ticket cannot proceed without legacy current root. |
| `external/sources` is absent. | Do not block; record absence as acceptable legacy posture. | Stop only if a later authorized migration ticket explicitly depends on it. |
| `external/sources` is present. | Do not inspect; classify as LegacyExternalSourceRoot. | Stop if inspection/listing/migration is requested without gate. |
| Future source review references legacy root. | Rewrite to canonical root or mark candidate path unknown. | Stop if source review cannot be scoped to canonical root. |

## 9. External Root Drift Markers

`ExternalRootDriftMarker` identifies root/path drift and permission confusion before it becomes source inspection, execution, or adoption.

| Marker | Meaning | Required response | Future closure owner |
| --- | --- | --- | --- |
| `legacy_external_root_path_drift` | A prompt or document treats `external/sources` as current root. | Normalize to `4_external/sources`; record legacy drift. | P9.R |
| `external_root_canonicalization_missing` | Future ticket lacks canonical root reference. | Require CanonicalExternalSourceRoot reference. | P9.R |
| `external_candidate_path_unknown` | Candidate path is not known. | Record `path_unknown_pending_authorized_inventory`. | Candidate owner ticket. |
| `external_candidate_path_unverified` | Candidate path has not had allowed path-only check. | Use authorized `Test-Path` only. | Candidate owner ticket. |
| `path_presence_misread_as_permission` | Path existence is treated as source, dependency, execution, or adoption permission. | Stop and route to P9.3/P9.4/P9.5 as applicable. | P9.R |
| `external_source_inspection_attempted_without_gate` | Source contents or tree listing requested before gate. | Stop; require P9.3 or candidate-specific source gate. | P9.3/P9.R |
| `external_source_execution_attempted_without_gate` | External tool execution requested before gate. | Stop; require P9.4. | P9.4/P9.R |
| `external_source_adoption_attempted_without_gate` | Vendor/fork/wrapper/submodule/adoption requested before gate. | Stop; require P9.5. | P9.5/P9.R |

## 10. Future Ticket Consumption Rules

| Future ticket/project | Required use of P9.1 | Forbidden shortcut | Expected path handling |
| --- | --- | --- | --- |
| P9.2 External Source License / Trust Intake Model | Use canonical root only. | License/trust intake against `external/sources` as current root. | Define license/trust metadata under `4_external/sources` without source inspection unless authorized. |
| P9.3 External Source Inspection Permission Gate | Define inspection gates using canonical root only. | Source tree listing based on root existence. | Inspection must be explicit, scoped, path-bound, candidate-bound. |
| P9.4 External Tool Execution Gate Model | Define execution gates using canonical root only. | Executing from path-only metadata. | Execution requires exact command/scope and approval. |
| P9.5 Vendor / Fork / Wrapper / Submodule Decision Model | Define adoption modes using canonical root only. | Automatic vendor/fork/wrapper/submodule decision from path presence. | Decide mode only after license/trust/source/execution posture. |
| P9.6 External Integration Rollback / Incident Protocol | Define rollback/incident posture using canonical root only. | Incident implementation in P9.1. | Handle discovered secrets, unsafe source, or execution incidents later. |
| P9.R External Integration Foundation Closure | Audit P9.1 invariants. | Closing P9 with legacy root drift unresolved. | Confirm canonical root, legacy root status, no source inspection/execution/adoption. |
| P10 Graphify Markdown Evidence Integration | Consume canonical root if Graphify path is authorized. | Running Graphify or modifying `.graphifyignore` because P9.1 exists. | Graphify can proceed only once P9/P10 gates authorize. |
| P11 Hermes Real Integration | Consume canonical root for Hermes source review once authorized. | Hermes runtime or source inspection before P11.0. | Hermes may be inspected only after P11.0. |
| P12 GBrain / GStack Memory + Skill Stack Integration | Consume `4_external/sources/gstack-main` as GStack PathOnlyMetadata. | GStack source inspection/execution/adoption from P9.1. | GBrain/GStack may be inspected only after P12.0. |
| P13 ECC-main Agent OS Evaluation | Consume canonical root once ECC-main path is authorized. | ECC-main agent OS activation before source/execution gates. | ECC-main may be inspected only after P13.0. |
| P14 Integrated External Runtime Synthesis | Consume P10-P13 closures and P9.1 root normalization. | Synthesizing runtime before P10-P13 closures. | Synthesize only after P10-P13 closures. |

## 11. Source Inspection Boundary

P9.1 does not authorize source inspection. P9.1 does not authorize source tree listing. P9.1 does not authorize source review. P9.1 does not authorize dependency review. P9.1 does not authorize execution. P9.3 will define source inspection permission gates.

Source review must be explicit, scoped, path-bound, and candidate-bound.

| Source surface | P9.1 status | Future gate | Stop rule |
| --- | --- | --- | --- |
| `4_external/sources` | canonical root only | P9.3 | Stop on any request to inspect, list, enumerate, or ingest contents. |
| `4_external/sources/gstack-main` | PathOnlyMetadata only | P12.0 plus P9.3 | Stop on any request to inspect/list/import GStack. |
| `external/sources` | LegacyExternalSourceRoot only | Future explicit migration/source gate, if needed | Stop on current-root or inspection request. |
| Graphify source | not inspected | P10/P9.3 | Stop on Graphify source inspection without gate. |
| Hermes source | not inspected | P11.0/P9.3 | Stop on Hermes source inspection without gate. |
| GBrain source | not inspected | P12.0/P9.3 | Stop on GBrain source inspection without gate. |
| ECC-main source | not inspected | P13.0/P9.3 | Stop on ECC-main source inspection without gate. |
| OpenCode source | not inspected | later OpenCode gate/P9.3 | Stop on OpenCode source inspection without gate. |
| Provider SDKs / MCP servers/tools/resources | not inspected | provider/MCP source gate | Stop on provider/MCP source inspection or activation request. |
| Product/Siamese source | not inspected | P4 / GT-09 or equivalent plus relevant P9/P10+ gate | Stop on product/Siamese source inspection request. |

## 12. Execution Boundary

P9.1 does not authorize execution. P9.1 does not authorize local tool execution. P9.1 does not authorize external tool execution. P9.1 does not authorize provider/API/MCP execution. P9.1 does not authorize runtime adoption. P9.4 will define the External Tool Execution Gate Model.

| Execution scenario | P9.1 status | Future gate | Stop rule |
| --- | --- | --- | --- |
| Graphify execution or `/graphify` | not authorized | P10/P9.4 | Stop on execution request. |
| Hermes execution/runtime | not authorized | P11/P9.4 | Stop on execution/runtime request. |
| GBrain execution/runtime | not authorized | P12/P9.4 | Stop on execution/runtime request. |
| GStack execution | not authorized | P12/P9.4 | Stop on execution/configuration request. |
| ECC-main execution/agent OS | not authorized | P13/P9.4 | Stop on execution/agent OS request. |
| OpenCode execution by AGENT PLATFORM | not authorized | later OpenCode/H0 gate | Stop on AGENT PLATFORM execution request. |
| Codegraph execution | not authorized | P10/P14 or later | Stop on execution request. |
| Provider/API/model calls | not authorized | provider/API gate | Stop on provider/API call request. |
| MCP resource/tool activation | not authorized | MCP gate | Stop on MCP activation request. |
| Tests, CI, scripts, package managers, builds, Python | not authorized by P9.1 | appropriate validation/build gate | Stop on test/build/script/package-manager request. |

## 13. Adoption Boundary

P9.1 does not authorize adoption. P9.1 does not authorize vendoring. P9.1 does not authorize forking. P9.1 does not authorize wrapping. P9.1 does not authorize submodules. P9.1 does not authorize patching. P9.5 will define the Vendor / Fork / Wrapper / Submodule Decision Model.

| Adoption mode | P9.1 status | Future gate | Stop rule |
| --- | --- | --- | --- |
| reference_only | allowed as governance context only | P9.2/P9.3 if source details needed | Stop if reference becomes source inspection. |
| path_metadata_only | allowed | P9.1 | Stop if path presence is treated as permission. |
| source_review_candidate | not authorized by P9.1 | P9.3 and candidate ticket | Stop on source review request without gate. |
| vendor_snapshot | not authorized | P9.5 | Stop on vendoring request. |
| fork_and_patch | not authorized | P9.5 | Stop on fork/patch request. |
| wrap_existing_source | not authorized | P9.5 plus implementation gate | Stop on wrapper/adapter request. |
| submodule_or_dependency | not authorized | P9.5 plus dependency approval | Stop on submodule/dependency request. |
| direct_runtime_integration | not authorized | P9.4/P9.5/P14 | Stop on runtime integration request. |

## 14. Security / Secret Boundary

External source roots must never be assumed safe or secret-free merely because they are normalized. Path normalization does not inspect secrets. P9.1 does not scan for secrets.

If a future source inspection discovers secrets, route to P9.6 rollback/incident protocol or a candidate-specific incident path. `.env`, credentials, provider configs, token stores, browser auth, local credential stores, and API keys remain blocked.

| Sensitive surface | P9.1 status | Future gate | Incident posture |
| --- | --- | --- | --- |
| `.env` | not inspected | S-03 plus future incident gate | Stop and route to incident posture if encountered later. |
| Credentials / token stores / browser auth / local credential stores | not inspected | S-03/P9.6 | Stop and escalate if discovered during future authorized review. |
| API keys / provider configs | not inspected | S-03/provider gate/P9.6 | Stop and route to credential handling policy. |
| MCP server/tool/resource secrets | not inspected | S-04/MCP gate/P9.6 | Stop and route to MCP/security incident posture. |
| External source roots | path-only metadata only | P9.3/P9.6 | Do not scan or inspect in P9.1. |

## 15. Product / Siamese Boundary

Siamese is product vision, not product activation. Product/Siamese source is not part of external source root normalization.

Product-bound integration requires P4 / GT-09 or equivalent product readiness gate plus relevant P9/P10+ gates. P9.1 does not inspect product/Siamese source. P9.1 does not create product adapters.

| Product-bound scenario | P9.1 decision | Blocked shortcut | Future gate |
| --- | --- | --- | --- |
| Product/Siamese source inspection | not authorized | Reading product/Siamese source because external roots were normalized. | P4 / GT-09 or equivalent plus source gate. |
| Product adapter | not authorized | Creating adapter from path-only metadata. | Product readiness plus P9.5/implementation gate. |
| External tool to product runtime | not authorized | Runtime activation from external path presence. | Product readiness plus P9.4/P9.5/P14. |
| Product/provider/API/MCP activation | not authorized | Credential or provider activation from P9.1. | Provider/API/MCP gate plus product gate. |

## 16. Git Boundary

P9.1 may provide exact commit advice only. P9.1 must not mutate Git. The user performs Git manually. Never recommend `git add .`.

No path migration commands are authorized. No move/rename commands are authorized. No submodule commands are authorized.

Required command pattern:

```powershell
git status --short

git add <exact_path_1>

git commit -m "<exact ticket message>"

git push origin main
```

## 17. Stop Rules

`ExternalRootStopRule`:

- Stop on missing P9.0 request.
- Stop on request to use `external/sources` as canonical root.
- Stop on request to require `external/sources` as mandatory current root.
- Stop on request to inspect `4_external/sources`.
- Stop on request to list `4_external/sources`.
- Stop on request to enumerate `4_external/sources`.
- Stop on request to inspect `4_external/sources/gstack-main`.
- Stop on request to list `4_external/sources/gstack-main`.
- Stop on request to import GStack.
- Stop on request to execute GStack.
- Stop on request to configure GStack.
- Stop on request to adopt GStack.
- Stop on external source content inspection request.
- Stop on external source tree listing request.
- Stop on external source adoption request.
- Stop on external tool execution request.
- Stop on source review request without P9.3.
- Stop on execution request without P9.4.
- Stop on vendor/fork/wrapper/submodule request without P9.5.
- Stop on rollback/incident implementation request.
- Stop on Graphify execution request.
- Stop on Hermes execution request.
- Stop on GBrain execution request.
- Stop on ECC-main execution request.
- Stop on OpenCode execution request.
- Stop on provider/API/MCP request.
- Stop on credential request.
- Stop on `.env` request.
- Stop on product/Siamese source request.
- Stop on runtime activation request.
- Stop on adapter implementation request.
- Stop on persistence DB request.
- Stop on vector DB request.
- Stop on graph DB request.
- Stop on telemetry/event streaming request.
- Stop on generated output tracking request.
- Stop on source tracking expansion request.
- Stop on publication request.
- Stop on Git mutation by agent request.
- Stop on `git add .` recommendation request.
- Stop on request to create P9.2+ files in this ticket.

## 18. Future Validation Targets

Future validation targets are proposed only and were not executed by P9.1:

- P9.0 prerequisite invariant.
- Canonical root equals `4_external/sources`.
- Legacy root equals `external/sources`.
- No `external/sources` as canonical root invariant.
- GStack path equals `4_external/sources/gstack-main`.
- GStack path/class metadata only invariant.
- No external source listing invariant.
- No external source content inspection invariant.
- No path-presence-as-permission invariant.
- No path-presence-as-dependency-approval invariant.
- No execution invariant.
- No adoption invariant.
- No path migration execution invariant.
- Future P9.2-P9.6 consumption readiness.
- Future P10-P14 consumption readiness.
- No Git mutation invariant.
- No `git add .` invariant.

## 19. Future Hardening Candidates

Future hardening candidates are proposed only and were not started:

- P9-ROOT-HARD-01 - ExternalSourcePathRef Schema Candidate.
- P9-ROOT-HARD-02 - ExternalCandidatePathRecord Checklist.
- P9-ROOT-HARD-03 - Legacy External Root Drift Scanner Design.
- P9-ROOT-HARD-04 - External Root Prompt Normalization Checklist.
- P9-ROOT-HARD-05 - Path-Only Metadata Invariant Checklist.
- P9-ROOT-HARD-06 - GStack Path/Class Metadata Checklist.
- P9-ROOT-HARD-07 - Future External Path Migration Plan Candidate.
- P9-ROOT-HARD-08 - P9.R Root Normalization Audit Input.

## 20. Created / Not Created Register

Created:

- `0_architecture/governance/agent_platform_external_source_root_normalization.md`

Modified:

- none

Not created / not approved:

- no P9.2-P9.R files
- no P10-P14 files
- no external source directory creation
- no external source directory movement
- no external source directory rename
- no symlinks
- no submodules
- no vendor code
- no forked code
- no wrapped code
- no patched external code
- no external source inspection
- no external source listing
- no external source enumeration
- no GStack inspection
- no GStack listing
- no GStack import
- no GStack execution
- no GStack configuration
- no GStack adoption
- no Graphify execution
- no Hermes execution
- no GBrain execution
- no ECC-main execution
- no OpenCode execution
- no provider/API/MCP activation
- no credentials
- no API calls
- no MCP calls
- no live connectors
- no product/Siamese source inspection
- no source loading
- no tool execution
- no agent execution
- no automatic dispatch
- no runtime activation
- no persistence DB
- no vector DB
- no graph DB
- no telemetry
- no event streaming
- no generated output tracking
- no source tracking expansion
- no publication
- no Git mutation by the agent

## 21. Recommended Next Ticket

After P9.1, continue the P9 foundation parallel queue if not already complete:

- P9.2 - External Source License / Trust Intake Model.
- P9.3 - External Source Inspection Permission Gate.
- P9.4 - External Tool Execution Gate Model.
- P9.5 - Vendor / Fork / Wrapper / Submodule Decision Model.
- P9.6 - External Integration Rollback / Incident Protocol.

Recommended actual next ticket:

```text
P9.2 - External Source License / Trust Intake Model
```

Do not start P9.2. Do not start P9.3. Do not start P9.4. Do not start P9.5. Do not start P9.6. Do not start P9.R. Do not start P10. Do not start P11. Do not start P12. Do not start P13. Do not start P14.

## 22. Final Verdict

| Question | Answer |
| --- | --- |
| What did P9.1 create? | `0_architecture/governance/agent_platform_external_source_root_normalization.md`. |
| Was P9.0 present? | Yes, at `0_architecture/governance/agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md`. |
| What canonical external source root was frozen? | `4_external/sources`. |
| What legacy external source root was classified? | `external/sources`. |
| What GStack path/class metadata was recorded? | `4_external/sources/gstack-main` as GStackPathClassMetadata and PathOnlyMetadata only. |
| Did P9.1 inspect `4_external/sources`? | No. |
| Did P9.1 list `4_external/sources`? | No. |
| Did P9.1 inspect/list/import/execute/configure/adopt GStack? | No. |
| Did P9.1 inspect external source contents? | No. |
| Did P9.1 approve source review? | No. |
| Did P9.1 approve dependency review? | No. |
| Did P9.1 approve execution? | No. |
| Did P9.1 approve adoption/vendor/fork/wrapper/submodule? | No. |
| Did P9.1 move or rename directories? | No. |
| Did P9.1 create symlinks or submodules? | No. |
| Did P9.1 modify `.gitignore` or `.graphifyignore`? | No. |
| Did P9.1 activate providers/API/MCP? | No. |
| Did P9.1 inspect product/Siamese source? | No. |
| Did P9.1 mutate Git? | No. |
| What future tickets consume this normalization? | P9.2, P9.3, P9.4, P9.5, P9.6, P9.R, P10, P11, P12, P13, and P14. |
| What is the next recommended ticket? | P9.2 - External Source License / Trust Intake Model. |
