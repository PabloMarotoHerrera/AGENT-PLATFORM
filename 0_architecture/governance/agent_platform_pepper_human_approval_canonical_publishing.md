# P16.6 Human Approval And Canonical Publishing Governance Record

## P16.6 Authority

P16 is Ticket Factory and Parallel Planning. P16.6 adds explicit human-gated approval evidence and in-memory logical canonical publication evidence after P16.5 multi-generator synthesis review.

The approval builder consumes the originating `ProjectSpec`, seed `TicketSpec`, a validated `TicketSynthesisReview`, explicit human approval evidence, optional human conflict resolutions, optional manual replacement evidence and optional fresh dependency-planning evidence. It produces either nonapproval evidence or an approved ticket record with lint and planning gates.

The publication builder consumes an approved `TicketApprovalRecord`, human publication evidence and optional prior publication evidence. It produces an in-memory canonical ticket artifact, optional supersession evidence and deterministic provenance digests.

P16.6 is not provider execution, prompt rendering, agent execution, dependency-plan mutation, automatic conflict resolution, file publication, repository publication, runtime scheduling, validation-command execution, worktree allocation or WorkPacket creation.

`TicketApprovalRecord`, `PublishedTicketArtifact`, `TicketSupersessionRecord` and `TicketPublicationResult` are evidence, not execution authority.

## Common P16 Branch Model

| Item | Value |
| --- | --- |
| P16 branch model | one common branch |
| Common branch | `p16-ticket-factory-and-parallel-planning` |
| Commit model | one reviewed commit per P16 ticket |
| Ticket-specific branches | absent |
| Agent branch creation | `0` |
| Agent staging, commit or push | `0` |

## Repository And Branch State

| Item | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM` |
| Branch | `p16-ticket-factory-and-parallel-planning` |
| Resolved P16.5 commit | `529d4ca37dd8ac860c638ea431c814bcca3f681c` |
| P16.5 commit message | `P16.5 Add multi-generator synthesis and conflict review` |
| HEAD at implementation | `529d4ca37dd8ac860c638ea431c814bcca3f681c` |
| Remote P16 at implementation | `529d4ca37dd8ac860c638ea431c814bcca3f681c` |
| P16.5 is ancestor of remote P16 | `true` |
| main at implementation | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| origin/main at implementation | `ffc850bb169364ae6ff64b66c75e15fcab38140d` |
| Worktree at gate | exactly 7 expected P16.6 candidates |
| Index at gate | empty |
| Omniverse tracked product files | `369` |

The P16.6 candidate remains uncommitted by instruction. No staging, commit, push, branch switch, reset, clean, stash, Docker command, dependency update, lockfile update, Graphify command or `graphify-out` modification was performed.

## Prerequisite Verdicts

| Prerequisite | Verdict |
| --- | --- |
| P16.0 | `hermes_0_19_pepper_project_ticket_spec_schema_ready_with_planning_only_authority` |
| P16.1 | `hermes_0_19_pepper_context_pack_assembler_ready_with_bounded_in_memory_authority` |
| P16.2 | `hermes_0_19_pepper_ticket_generator_agent_roles_ready_with_non_executing_proposal_authority` |
| P16.3 | `hermes_0_19_pepper_dependency_dag_parallel_wave_planner_ready_with_dependency_only_authority` |
| P16.4 | `hermes_0_19_pepper_ticket_policy_linter_ready_with_deterministic_non_mutating_authority` |
| P16.5 | `hermes_0_19_pepper_multi_generator_synthesis_conflict_review_ready_with_noncanonical_review_authority` |

P16.6 did not modify `specs.py`, `context_packs.py`, `generator_roles.py`, `dependency_planning.py`, `ticket_policy.py`, `proposal_synthesis.py` or the accepted P16.0/P16.1/P16.2/P16.3/P16.4/P16.5 focused tests.

## Pre-Change Pepper Identity

Committed P16.5 Pepper identity before P16.6 implementation:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate | `6850` | `150523920` | `e029604214f18c63ab59ebff4378c798011a054b10f23017e72ab0e349f725a3` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Pre-change governance integrity reported `14` tests, `0` failures and `0` errors.

## Post-Change Pepper Identity Projection

Working-tree Pepper projection after P16.6 focused test correction:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate | `6853` | `150673633` | `fc92e05dd8b6d852dbfbd3166a535943814ad6cd084d24b8ecd744a7bcf3bbb9` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Upstream payload changed: `false`. Baseline changed: `false`.

## Package Paths

| Path | Purpose |
| --- | --- |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py` | Public Ticket Factory export boundary extended additively for P16.6 while preserving the P16.4 final export block. |
| `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/approval_publishing.py` | Immutable P16.6 human approval and logical canonical publication contracts. |
| `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_ticket_factory_approval_publishing.py` | Focused P16.6 approval and publication contract tests. |
| `2_products/pepper-agent/docs/agent-platform/human_approval_canonical_publishing.md` | P16.6 operator and contract documentation. |

No parent `agent_platform` initializer, runtime route, frontend source, provider code, credential code, dependency file, prior P16 contract or prior P16 test was modified.

## Public Exports

P16.6 adds exactly these 24 public exports:

| Export |
| --- |
| `HUMAN_APPROVAL_PUBLISHING_SCHEMA_VERSION` |
| `HumanApprovalDecision` |
| `ConflictResolutionAction` |
| `TicketApprovalState` |
| `CanonicalTicketSource` |
| `TicketPublicationState` |
| `TicketPublicationFormat` |
| `HumanApprovalEvidence` |
| `HumanConflictResolution` |
| `ManualTicketReplacement` |
| `FreshDependencyPlanningEvidence` |
| `TicketApprovalRequest` |
| `TicketApprovalRecord` |
| `TicketPublicationEvidence` |
| `TicketPublicationRequest` |
| `PublishedTicketArtifact` |
| `TicketSupersessionRecord` |
| `TicketPublicationResult` |
| `TicketApprovalPublishingError` |
| `TicketApprovalInputError` |
| `TicketApprovalValidationError` |
| `TicketPublicationAuthorizationError` |
| `build_ticket_approval_record` |
| `publish_canonical_ticket` |

P16.0 exports preserved: `true`. P16.1 exports preserved: `true`. P16.2 exports preserved: `true`. P16.3 exports preserved: `true`. P16.4 exports preserved: `true`. P16.5 exports preserved: `true`. P16.4 final-block compatibility preserved: `true`. Duplicate exports: `0`. Private digest constants exported through package root: `0`. Import side effects: `0`.

## Schema Version And Enums

`HUMAN_APPROVAL_PUBLISHING_SCHEMA_VERSION = 1`. `TicketApprovalRecord.schema_version`, `PublishedTicketArtifact.schema_version` and `TicketPublicationResult.schema_version` are fixed to `Literal[1] = 1`. Alternative versions are rejected. Schema migration and runtime negotiation are absent.

| Enum | Values |
| --- | --- |
| `HumanApprovalDecision` | `approve`, `reject`, `request_revision` |
| `ConflictResolutionAction` | `acknowledge`, `accept_candidate`, `resolve_with_manual_replacement`, `reject` |
| `TicketApprovalState` | `approved`, `rejected`, `revision_required` |
| `CanonicalTicketSource` | `synthesized_candidate`, `manual_replacement` |
| `TicketPublicationState` | `published`, `superseded` |
| `TicketPublicationFormat` | `canonical_json_v1` |

Enum aliases: `0`. Unrestricted enum strings are rejected.

## Approval Rules

Approval requests must bind to one project, seed ticket and synthesis review. Synthesis review and candidate digests are revalidated. Candidate identity must match the seed project, ticket ID and ticket type. Manual replacements must preserve seed schema version, project ID, ticket ID and ticket type.

Approval decisions require selected ticket evidence from the P16.5 candidate or manual replacement. Every P16.5 conflict requires exactly one human resolution. Reject resolutions cannot approve. Human-review conflicts cannot be merely acknowledged. Blocking conflicts require manual replacement. Nonapproval decisions reject manual replacement and fresh planning evidence.

Approved tickets are linted again with P16.4. Blocked lint evidence blocks approval. Warning lint evidence requires explicit human policy-warning acknowledgement. Selected-ticket dependency or scope changes require fresh planning evidence that recomputes exactly, contains the selected ticket and does not block it. Planning warnings require explicit human planning-warning acknowledgement.

## Publication Rules

Only approved `TicketApprovalRecord` instances can be published. The approval record is revalidated before publication. Rejected and revision-required records are not publication authority.

Publication is in-memory and logical. First publication creates revision `1` and no supersession. Later publication requires a prior matching artifact and human supersession rationale, creates the next revision and records supersession evidence.

Publication IDs are derived from ticket ID and revision. Canonical ticket JSON is deterministic JSON over the approved `TicketSpec`. The builder does not write canonical JSON to disk or publish to a repository.

## Digest Evidence

Approval input digest algorithm: `agent-platform-ticket-approval-input-sha256-v1`. Approval record digest algorithm: `agent-platform-ticket-approval-record-sha256-v1`. Canonical ticket digest algorithm: `agent-platform-canonical-ticket-sha256-v1`. Published artifact digest algorithm: `agent-platform-published-ticket-artifact-sha256-v1`. Supersession digest algorithm: `agent-platform-ticket-supersession-sha256-v1`. Publication input digest algorithm: `agent-platform-ticket-publication-input-sha256-v1`. Publication result digest algorithm: `agent-platform-ticket-publication-result-sha256-v1`.

Approval, artifact, supersession and result digests exclude their own digest fields. Digests are neither security signatures nor deployment authorization tokens.

## Nonexecuting Approval And Publication Authority

P16.6 defines no ApprovalExecutor, PublicationWriter, CanonicalTicketWriter, WorkPacket, ExecutionLane, AgentAssignment, WorkerAssignment, WorktreeAssignment, approved-ticket runner, validation-command runner, file loader, file writer, repository publisher or Graphify operation public shape.

The builders do not mutate approval requests, synthesis reviews, lint reports, dependency plans, seed tickets, approved tickets, prior publication artifacts or publication requests.

## Tests

Focused P16.6 command from `2_products/pepper-agent`:

```text
python -m pytest -q tests/hermes_cli/test_agent_platform_ticket_factory_approval_publishing.py -p no:cacheprovider
```

Result: `202` passed, `0` failed, `0` errors, `0` unexpected skips, `0` warnings.

Focused combined P16.0/P16.1/P16.2/P16.3/P16.4/P16.5/P16.6 command from `2_products/pepper-agent`:

```text
python -m pytest -q tests/hermes_cli/test_agent_platform_ticket_factory_specs.py tests/hermes_cli/test_agent_platform_ticket_factory_context_packs.py tests/hermes_cli/test_agent_platform_ticket_factory_generator_roles.py tests/hermes_cli/test_agent_platform_ticket_factory_dependency_planning.py tests/hermes_cli/test_agent_platform_ticket_factory_ticket_policy.py tests/hermes_cli/test_agent_platform_ticket_factory_proposal_synthesis.py tests/hermes_cli/test_agent_platform_ticket_factory_approval_publishing.py -p no:cacheprovider
```

Result: `1004` passed, `0` failed, `0` errors, `0` unexpected skips, `0` warnings. Constituent counts: P16.0 `96`, P16.1 `75`, P16.2 `120`, P16.3 `133`, P16.4 `217`, P16.5 `161`, P16.6 `202`.

The direct validation commands used the active Windows Python with pytest. No dependency installation was performed.

Import smoke:

```text
TicketApprovalRequest TicketApprovalRecord TicketPublicationRequest PublishedTicketArtifact TicketPublicationResult build_ticket_approval_record publish_canonical_ticket
```

## Static Validation

Ruff check over the three P16.6 Python candidates reported `0` lint errors. Ruff format check reported `3` files already formatted. `ty` availability: `false`; type check was not run because the tool is unavailable and no dependency installation was performed.

Static import and authority scans for `approval_publishing.py` reported no forbidden provider, agent, tool, filesystem, network, subprocess, Git, Docker, Graphify, WorkPacket execution or file-publication imports or call terms.

## Modification Register

`2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` records exactly three new P16.6 product-addition rows: `P16.6-001`, `P16.6-002`, `P16.6-003`.

Existing row `P16.0-001` for `hermes_cli/agent_platform/ticket_factory/__init__.py` was preserved and updated to the additive P16.6 hash and description. Duplicate IDs: `0`. Missing destination paths: `0`. Unrelated row edits: `0` by intended candidate scope.

## Import Manifest

`2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` records three new P16.6 product-addition rows for approval/publication source, focused tests and documentation. Existing destination row `hermes_cli/agent_platform/ticket_factory/__init__.py` was updated to the additive P16.6 hash and rule. The governance record is not included in the Pepper import manifest.

Classification for new rows: `AGENT_PLATFORM_product_addition`. Included in upstream payload: `false`.

## Product File Hashes

| Path | SHA-256 |
| --- | --- |
| `hermes_cli/agent_platform/ticket_factory/__init__.py` | `673c41737e2f602b26c5e2856ed91247da73a5b877a1f2652d786e0a1814e060` |
| `hermes_cli/agent_platform/ticket_factory/approval_publishing.py` | `11eecc861b169338db6facc00ccafb7db44456e1d53595941558a99f7dbf2c4b` |
| `tests/hermes_cli/test_agent_platform_ticket_factory_approval_publishing.py` | `b4d835e84d2e7a2e1edbc4df38c3c8143b650f3bf411fa82ba55e4699bf1923c` |
| `docs/agent-platform/human_approval_canonical_publishing.md` | `a49aef7a1ce93576a7f33e9ac4e969e288009ae3e5a01e9e091a74984110cf18` |
| `AGENT_PLATFORM_MODIFICATIONS.tsv` | `974c7feea9d0d81cd7479ded8ed13c86070ba95406a123c74cfc103488904795` |
| `AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | `c6f6ec0262517767d8f3852186abfcc7384b07a31e1c6a3af9eb04a8a8e4f59b` |

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
| runtime agent actions by product code | `0` |
| tool actions by product code | `0` |
| Git actions by product code | `0` |
| Graphify actions | `0` |
| Docker actions | `0` |
| branch actions | `0` |
| worktree actions | `0` |
| proposal generation | `0` |
| provider/model execution | `0` |
| prompt rendering | `0` |
| dependency plan implicit rebuild | `0` |
| dependency plan mutation | `0` |
| ticket linting mutation | `0` |
| automated approval | `0` |
| filesystem publication | `0` |
| WorkPacket creation | `0` |
| validation command execution | `0` |
| ticket auto-fix | `0` |

Pydantic validation, review/lint/planning evidence checks, deterministic canonical JSON construction and SHA-256 hashing are the only runtime behaviors introduced by P16.6 product code.

## Exact Candidate Set

Created Pepper product files:

| Status | Path |
| --- | --- |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/approval_publishing.py` |
| Added | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_ticket_factory_approval_publishing.py` |
| Added | `2_products/pepper-agent/docs/agent-platform/human_approval_canonical_publishing.md` |

Modified Pepper product files:

| Status | Path |
| --- | --- |
| Modified | `2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` |

Created governance record:

| Status | Path |
| --- | --- |
| Added | `0_architecture/governance/agent_platform_pepper_human_approval_canonical_publishing.md` |

Candidate formula: `3` created Pepper product files plus `3` modified Pepper product files plus `1` created governance record equals `7` candidates. Created files: `4`. Modified files: `3`. Deleted files: `0`. Unexpected candidates: `0`. Prior P16 contract candidates: `0`. Prior P16 test candidates: `0`. Frontend candidates: `0`. Backend runtime candidates: `0`. Provider candidates: `0`. Worker candidates: `0`. Omniverse candidates: `0`. External source candidates: `0`. Graphify candidates: `0`. Dependency file candidates: `0`.

## P16.7 Handoff

P16.7 owns the historical regression corpus. P16.6 hands off explicit human approval records, logical canonical ticket artifact evidence and supersession evidence. P16.7 must not treat P16.6 publication evidence as filesystem persistence, repository publication or execution authority.

## Residual Constraints

| Item | State |
| --- | --- |
| approval record immutable | `true` |
| published artifact immutable | `true` |
| supersession record immutable | `true` |
| automated approval | `false` |
| filesystem publication | `false` |
| executable candidate | `false` |
| proposal generation | absent |
| provider/model execution | absent |
| prompt rendering | absent |
| agent execution | absent |
| worker assignment | absent |
| worktree assignment | absent |
| WorkPacket | absent |
| dependency plan implicitly rebuilt | `false` |
| dependency plan mutated | `false` |
| candidate lint mutates ticket | `false` |
| filesystem access | absent |
| network access | absent |
| Git access | absent |
| Graphify | frozen read-only; not run by P16.6 instruction |
| Docker | absent |
| production readiness | not claimed |

Canonical verdict occurrences in this record: `1`. Alternative P16.6 verdict occurrences: `0`.

## Final Verdict

hermes_0_19_pepper_human_approval_canonical_publishing_ready_with_explicit_human_gated_non_executing_authority
