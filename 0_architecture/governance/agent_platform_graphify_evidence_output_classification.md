# Graphify Evidence Output Classification

## Document Header

| Field | Value |
| --- | --- |
| Title | Graphify Evidence Output Classification |
| Ticket | P10.4 |
| Status | Accepted Graphify evidence output classification |
| Date | 2026-07-07 |
| Scope | Governance classification for expected Graphify outputs from a future controlled markdown rerun. |
| Authority | Graphify evidence output classification only, not Graphify execution, Graphify rerun, Graphify adoption as authority, output import, output promotion, output tracking, source tracking expansion, runtime activation, provider/auth/API/MCP activation, credential use, API calls, MCP activation, source loading, source inspection, product source inspection, external source inspection, validation execution, security enforcement activation, persistence/database/event streaming, telemetry, vector DB, embeddings, graph DB, substrate implementation, publication, Git mutation, or Cognitive Semantic System substrate selection. |
| Related documents | P10.0, P10.1 if present, P10.2 if present, P10.3 if present, P9.R, P9.4, P9.0, P9.1, P9.2, P9.3, P9.5, P9.6, P8.R, P3.BR, P3.0, P3.1, P3.2, P2.1, P2.2, P2.3, P1.1, P1.3, P1.5, P0.1, P0.2, P0.3, S-03, S-04, CSS ADR/audit, README, `.gitignore`, `.graphifyignore`. |
| Output | Graphify evidence output classification |
| Target file | `0_architecture/governance/agent_platform_graphify_evidence_output_classification.md` |

Final declaration: `graphify_evidence_output_classification_ready_for_P10_5`.

## Purpose

P10 integrates Graphify as controlled repository evidence mapping.

P10.0 authorizes the conceptual markdown scope.

P10.4 classifies expected Graphify outputs before controlled execution.

P10.4 enables P10.5 to know how generated outputs must be handled.

P10.4 enables P10.6 to report refreshed evidence without authority drift.

P10.4 enables P10.7 to define import boundaries without automatic import.

P10.4 keeps Graphify as evidence map only.

P10.4 does not run Graphify.

P10.4 does not read raw outputs.

P10.4 does not import outputs.

P10.4 does not approve tracking.

P10.4 does not start P10.5.

## Current Posture

Graphify = evidence map.

Graphify != authority.

Graphify != source of truth operativo.

Graphify != approval engine.

Graphify != runtime.

Graphify != Cognitive Semantic System substrate.

Graphify output is generated evidence by default.

Graphify output may support decisions.

Graphify output cannot decide.

Graphify output cannot approve source loading.

Graphify output cannot approve source tracking.

Graphify output cannot approve generated output tracking.

Graphify output cannot approve tool execution.

Graphify output cannot approve provider/auth/API/MCP.

Graphify output cannot approve product/Siamese inspection.

Graphify output cannot activate runtime.

Graphify output cannot select substrate.

No Graphify execution is approved by P10.4.

No generated output tracking is approved by P10.4.

Cognitive Semantic System substrate remains deferred.

P10.2 and P10.3 were missing during P10.4 path posture checks and remain pending sibling alignment. P10.4 does not synthesize them.

## Graphify Output Classification Model

Output classification values:

- raw_generated_evidence
- curated_evidence
- reviewed_evidence
- derived_report
- import_candidate
- accepted_architectural_evidence
- rejected_evidence
- stale_evidence
- conflicting_evidence
- blocked_generated_local_only_output
- trackable_output_only_under_future_gate
- quarantined_output
- delete_candidate_output

All Graphify outputs default to raw_generated_evidence unless explicitly reviewed and reclassified.

No output may become authority by classification alone.

No output may become trackable by classification alone.

No output may become imported by classification alone.

No output may become Cognitive Semantic System substrate by classification alone.

## Graphify Output Object Model

| object | meaning | required fields | forbidden fields | security posture | validation posture | authority posture | tracking posture |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GraphifyOutputRecord | Metadata record for one expected Graphify output. | output id, type, path/identifier, run ref, scope, sensitivity, postures | authority flag, tracking approval, imported payload | security posture required | validation posture required | not authority | not tracking approval |
| GraphifyRawOutputRef | Reference to raw generated evidence. | output ref, run ref, local-only marker | source truth claim, approval claim | local-only unless reviewed | unevaluated by default | not authority | not tracked by default |
| GraphifyCuratedEvidenceRef | Manually reviewed supporting evidence ref. | review ref, EvidenceRef, limitations | approval, source-of-truth claim | security refs if constrained | validation refs if evaluated | supports only | tracking requires future gate |
| GraphifyReviewedEvidenceRef | Evidence with reviewer status. | reviewer ref, review status, limitations | automated approval | reviewer posture required | validation optional | not decision | not tracking approval |
| GraphifyDerivedReportRef | Human/agent report derived from outputs. | report ref, evidence refs, limitations | raw output import by default | report sensitivity posture | report validation posture | not authority | track only if report gate allows |
| GraphifyImportCandidateRef | Proposed future consumption candidate. | candidate ref, import scope, blockers | import approval, memory ingestion | import risk posture | import validation posture | candidate only | not tracked by default |
| GraphifyAcceptedEvidenceRef | Evidence accepted as architectural support. | acceptance ref, scope, limitations | governance decision by itself | accepted-evidence security posture | reviewed validation posture | support only | no tracking by itself |
| GraphifyRejectedEvidenceRef | Evidence rejected after review. | rejection reason, reviewer ref | reuse as support | rejection retention posture | not valid support | rejected | not tracked |
| GraphifyStaleEvidenceRef | Evidence potentially outdated. | staleness marker, date/ref, reviewer requirement | current-state claim | staleness risk | requires review | stale support only | not tracked by default |
| GraphifyConflictRef | Evidence conflict marker. | conflict marker, conflicting refs, route | override governance | conflict risk | requires reconciliation | no authority | not tracked |
| GraphifyBlockedOutputRef | Blocked generated local-only output. | blocker, safe metadata, incident posture | unsafe summary, import | quarantine/security posture | blocked validation | no authority | no tracking |
| GraphifyTrackableCandidateRef | Output that could be tracked only after future gate. | exact future gate refs, path refs | immediate tracking approval | tracking risk posture | tracking validation posture | not authority | future gate only |
| GraphifyRetentionRef | Retention metadata for output class. | retention period/posture, owner | indefinite retention by default | retention risk | retention validation if needed | not authority | not tracking |
| GraphifyRollbackRef | Rollback metadata for consumed evidence. | rollback route, owner | automatic rollback | rollback risk | rollback validation if needed | not authority | not tracking |
| GraphifyIncidentRef | Incident route for sensitive exposure. | severity, route, safe metadata | secret content | incident posture required | incident validation if needed | not authority | not tracking |
| GraphifyCitationRef | Supporting citation to output or derived report. | citation id, target refs, scope, freshness, limitations | import payload | citation safety posture | citation validation posture | citation is not authority | citation is not tracking |
| GraphifyReviewRequirement | Review requirement for output class. | reviewer role, review scope, stop rules | implicit approval | review safety posture | review criteria | no automatic authority | no tracking approval |

## GraphifyOutputRecord Contract

GraphifyOutputRecord fields:

- graphify_output_id
- output_title
- output_type
- output_path_or_identifier
- generation_run_ref
- input_scope_ref
- allowed_input_scope
- blocked_input_scope
- source_classification
- sensitivity
- generated_output_related
- local_only
- product_related
- external_related
- credential_related
- secret_related
- contains_raw_source_indicator
- contains_generated_summary_indicator
- contains_relationship_map_indicator
- contains_code_structure_indicator
- contains_markdown_structure_indicator
- contains_evidence_refs_indicator
- authority_posture
- evidence_posture
- validation_posture
- security_posture
- review_status
- curation_status
- import_status
- tracking_posture
- retention_posture
- rollback_posture
- incident_posture
- citation_strategy
- staleness_marker
- conflict_marker
- blockers
- limitations

GraphifyOutputRecord is metadata.

GraphifyOutputRecord is not output import.

GraphifyOutputRecord is not generated output tracking approval.

GraphifyOutputRecord is not authority.

## Graphify Raw Output Classification

raw_generated_evidence is the default classification for generated Graphify outputs immediately after P10.5.

Allowed use:

- local review
- manual evidence inspection if future scope allows
- supporting reference for P10.6 report
- candidate input to P10.7 boundary definition

Blocked use:

- authority
- automatic import
- automatic memory ingestion
- Graph DB import
- vector DB import
- Cognitive Semantic System substrate
- source tracking
- generated output tracking
- publication
- product decision authority
- provider/tool/agent activation

Raw Graphify output remains generated local-only evidence unless reviewed and governed.

## Curated Evidence Classification

curated_evidence is Graphify output or summary that has been manually reviewed, scoped, and limited for use as supporting evidence.

Required before curation:

- source scope verification
- blocked path verification
- secret/credential absence posture
- product/Siamese absence posture
- external source absence posture
- generated-output posture
- EvidenceRef binding
- SecurityRef binding if constrained
- ValidationRef binding if evaluated
- retention posture
- rollback posture
- incident posture
- limitations

Curated evidence supports; it does not decide.

Curated evidence is not authority.

Curated evidence is not import approval.

## Derived Report Classification

derived_report is a human- or agent-created report based on Graphify outputs.

Examples:

- P10.6 refresh report
- risk notes
- coverage summary
- missing-area report
- blocked-area preservation report

Allowed use:

- supporting governance report
- evidence freshness note
- integration planning evidence

Blocked use:

- runtime activation
- automatic import
- source of truth
- tracking generated source without gate

Derived reports must cite Graphify evidence but cannot convert it into authority.

## Import Candidate Classification

import_candidate is a Graphify-derived record proposed for future consumption by AGENT PLATFORM.

Import candidate may include:

- relationship evidence candidate
- repo map evidence candidate
- documentation visibility candidate
- dependency visibility candidate
- architecture coverage candidate
- review checklist candidate

Blocked until future gate:

- automatic import
- memory insertion
- Graph DB import
- vector DB import
- Cognitive Semantic System record creation
- substrate selection
- persistent storage
- tracking
- publication

Import candidate is not import approval.

P10.7 owns evidence import boundary.

P10.4 only defines classification.

## Blocked / Local-Only Output Classification

blocked_generated_local_only_output is any Graphify output that includes or appears to derive from blocked scope, unknown sensitivity, secrets risk, credential risk, product/Siamese risk, external source risk, raw generated-output risk, local-only risk, or source tracking risk.

Required behavior:

- mark blocked
- do not import
- do not track
- do not publish
- do not summarize unsafe content
- trigger incident route if sensitive exposure is suspected
- preserve safe metadata only

Blocked generated local-only output cannot become curated evidence.

## Trackable Output Only Under Future Gate

trackable_output_only_under_future_gate is output that could only be recommended for tracking after exact future gate approval.

Required before any tracking recommendation:

- source classification
- generated-output classification
- security review
- validation posture
- retention posture
- rollback posture
- incident route
- human approval
- exact path list
- source tracking posture
- generated output tracking posture
- Git advisory boundary

P10.4 does not approve tracking.

P10.4 must not recommend tracking.

Never recommend git add ..

## Authority Boundary

Graphify output is not authority.

Graphify output is not governance decision.

Graphify output is not source of truth.

Graphify output is not approval.

Graphify output is not validation result unless separately evaluated.

Graphify output is not security review unless separately evaluated.

Graphify output is not source inspection permission.

Graphify output is not runtime permission.

Graphify output is not Cognitive Semantic System substrate.

Graphify output is not product activation.

Graphify output is not Git permission.

## Evidence / Validation / Security Interface

Evidence supports; it does not decide.

Validation evaluates; governance decides.

Security constrains; it does not activate.

Graphify outputs must be treated as evidence candidates.

Graphify output classification must preserve EvidenceRef semantics from P2.2.

Graphify output classification must preserve retention / rollback / incident semantics from P2.3.

Graphify output classification must preserve source classification and security posture from P3.0 / P3.2.

Validation may evaluate output classification in the future but cannot promote outputs by itself.

Security may block outputs but cannot activate import or tracking by itself.

## Retention / Rollback / Incident Posture

| output class | retention posture | rollback posture | incident posture |
| --- | --- | --- | --- |
| raw_generated_evidence | local-only generated evidence retention until reviewed or expired | remove from consideration if out of scope | incident route if sensitive exposure suspected |
| curated_evidence | retain with EvidenceRef, limitations, and review metadata | revoke curation if source/scope conflict appears | incident route if sensitive exposure later found |
| reviewed_evidence | retain review result and limitation metadata | rollback to raw/rejected if review invalidated | incident route if unsafe material is discovered |
| derived_report | retain report with citations and disclaimers | revise or supersede report if evidence invalidated | incident route if report exposes blocked material |
| import_candidate | retain candidate metadata only | remove candidate if import boundary blocks it | incident route if candidate references unsafe material |
| accepted_architectural_evidence | retain as supporting evidence with limitations | revoke accepted status on conflict/staleness | incident route if sensitive exposure discovered |
| rejected_evidence | retain rejection reason and safe metadata | no promotion without new review | incident route if rejection involved sensitive exposure |
| stale_evidence | retain staleness marker until reviewed | replace or retire when refreshed | incident route if stale evidence causes unsafe recommendation |
| conflicting_evidence | retain conflict marker and reconciliation route | rollback any prior consumption | incident route if conflict exposes sensitive material |
| blocked_generated_local_only_output | quarantine or deletion-candidate posture | do not consume; remove from workflow if safe | incident route required if sensitive exposure suspected |
| trackable_output_only_under_future_gate | retain as future-gate candidate metadata only | remove from tracking consideration without gate | incident route if tracking would expose sensitive material |
| quarantined_output | retain safe metadata only under quarantine | do not release without incident resolution | incident route required |
| delete_candidate_output | retain deletion candidate metadata only | delete only under authorized retention/incident route | incident route if sensitive exposure suspected |

Every Graphify output class must have retention posture.

Every Graphify output class must have rollback posture.

Every Graphify output class must have incident posture where sensitive exposure is suspected.

Blocked outputs require quarantine or deletion candidate posture.

Stale outputs require staleness marker and review requirement.

Conflicting outputs require conflict marker and review requirement.

## Citation / Reference Strategy

GraphifyCitationRef is a reference to a Graphify output or derived report used as supporting evidence.

Citation refs must include:

- citation_ref_id
- target_output_ref
- target_report_ref
- evidence_scope
- source_scope
- freshness_marker
- staleness_marker
- limitations
- blocked_material_notice
- review_status
- authority_disclaimer

Citation is not authority.

Citation is not import.

Citation is not tracking.

Citation is not source loading permission.

Citation must preserve limitations and authority disclaimer.

## Staleness / Conflict Handling

stale_evidence marks output that may no longer reflect current repo state.

conflicting_evidence marks output that conflicts with governance documents, source classification, security posture, or manual review.

Required behavior:

- do not promote
- do not import
- do not track
- require reviewer pass
- require integrator pass
- record limitation
- record rollback if previously consumed

Governance documents override Graphify evidence.

Manual review and reconciliation are required for conflicts.

## Source Scope Boundary

Allowed P10 input scope:

- README.md
- 0_architecture/**/*.md
- 3_platform/_governed_skeleton/**/*.py

Blocked P10 input scope:

- .env
- credentials/**
- secrets/**
- provider configs
- token stores
- 4_external/sources/**
- 9_artifacts/**
- graphify-out/**
- product/Siamese source
- generated outputs not explicitly approved

If any output indicates blocked scope traversal, classify as blocked_generated_local_only_output and trigger stop / incident posture.

## Generated Output Tracking Boundary

P10.4 does not approve generated output tracking.

Generated output tracking requires future exact gate.

Graphify raw outputs must not be tracked by default.

Graphify derived reports may be trackable only if they are human-authored or governance-authored under exact tracking approval.

Exact tracking approval must list paths.

Never recommend git add ..

## Git Advisory Boundary

The agent never mutates Git.

The user commits and pushes manually.

P10.4 must not stage, commit, push, force-add, or publish.

P10.4 must not recommend tracking generated Graphify outputs.

P10.4 may later produce commit advice only for the created governance document after human approval.

Never recommend git add ..

## Graphify Output Decision Matrix

| output_class | meaning | default authority posture | allowed use | blocked use | review requirement | retention posture | rollback posture | incident posture | tracking posture |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| raw_generated_evidence | immediate generated output from Graphify | not authority | local review, P10.6 support, P10.7 boundary input | import, tracking, runtime, substrate | required before promotion | local-only until reviewed | remove from consideration if invalid | incident if sensitive | not tracked by default |
| curated_evidence | manually reviewed and scoped supporting evidence | not authority | governance support | decision authority, import approval | completed manual review | retain with EvidenceRef | revoke if conflict | incident if exposure found | future gate only |
| reviewed_evidence | evidence with review status | not authority | support with reviewer limitations | auto-approval | reviewer pass required | retain review metadata | revert if review invalidated | incident if unsafe | future gate only |
| derived_report | report based on Graphify outputs | not authority | governance report, freshness note | runtime, source of truth, import | report review required | retain report/citations | revise or supersede | incident if unsafe summary | only if exact gate allows |
| import_candidate | proposed future consumption record | candidate only | P10.7 boundary planning | automatic import, memory insertion, Graph DB/vector DB | import review required | retain candidate metadata | remove if boundary blocks | incident if unsafe ref | not tracked by default |
| accepted_architectural_evidence | accepted support for architecture reasoning | support only | architectural support | decision by itself | acceptance review required | retain accepted evidence refs | revoke on staleness/conflict | incident if exposure | future gate only |
| rejected_evidence | evidence rejected after review | no authority | rejection audit | reuse as support | rejection review required | retain safe rejection metadata | no promotion without new review | incident if sensitive | not tracked |
| stale_evidence | evidence possibly outdated | stale support only | freshness warning | current-state claim | staleness review required | retain staleness marker | replace/retire | incident if unsafe recommendation | not tracked by default |
| conflicting_evidence | evidence conflicting with governance/review | no authority | reconciliation input | promotion, import, tracking | reviewer and integrator pass required | retain conflict marker | rollback prior consumption | incident if exposure | not tracked |
| blocked_generated_local_only_output | output with blocked/unknown-sensitive risk | no authority | safe metadata only | summary, import, tracking, publish | incident/security review required | quarantine/delete-candidate | do not consume | incident route required | never tracked by P10.4 |
| trackable_output_only_under_future_gate | output that could be trackable only later | not authority | future tracking gate planning | immediate tracking | future tracking review required | retain candidate metadata | remove without gate | incident if tracking unsafe | future exact gate only |
| quarantined_output | output held due to risk | no authority | safe metadata only | release/import/tracking | security/incident review required | quarantine posture | release only by incident route | incident route required | not tracked |
| delete_candidate_output | output recommended for deletion route | no authority | safe deletion-candidate metadata | publication/tracking | retention/incident review required | deletion candidate posture | remove only by approved route | incident if sensitive | not tracked |

## P10.5 Interface

P10.5 must classify outputs produced by controlled rerun using the P10.4 model.

P10.5 must not expand classification scope during execution.

P10.5 must stop if blocked scope appears.

P10.5 must preserve generated evidence posture.

P10.5 must not track generated outputs unless future exact gate exists.

P10.5 must not treat successful Graphify execution as authority.

## P10.6 Interface

P10.6 must report refreshed markdown evidence using the P10.4 output classifications.

P10.6 must distinguish raw generated evidence from curated evidence and derived report content.

P10.6 must preserve authority disclaimers.

P10.6 must report missing areas, blocked areas, limitations, and evidence freshness.

P10.6 must not promote outputs automatically.

## P10.7 Interface

P10.7 must use P10.4 output classes to define import boundaries.

P10.7 must distinguish raw output, curated evidence, reviewed evidence, import candidate, accepted architectural evidence, rejected evidence, and stale evidence.

P10.7 must not implement automatic import.

P10.7 must not create Graph DB, vector DB, embeddings, or Cognitive Semantic System substrate.

## P10.R Interface

P10.R must verify P10.4 output classification was accepted.

P10.R must verify Graphify remains evidence-only.

P10.R must verify no authority drift.

P10.R must verify no generated output tracking drift.

P10.R must verify no source expansion drift.

P10.R must verify no product/Siamese drift.

P10.R must verify no secrets drift.

P10.R must verify no Git mutation.

## Required P10.4 Invariants

GFOC-001 P10.4 creates Graphify evidence output classification only.

GFOC-002 Graphify = evidence map.

GFOC-003 Graphify output is generated evidence by default.

GFOC-004 Graphify output is not authority.

GFOC-005 Graphify output is not source of truth operativo.

GFOC-006 Graphify output is not approval.

GFOC-007 Graphify output is not runtime.

GFOC-008 Graphify output is not Cognitive Semantic System substrate.

GFOC-009 Evidence supports; it does not decide.

GFOC-010 Validation evaluates; governance decides.

GFOC-011 Security constrains; it does not activate.

GFOC-012 Raw Graphify output remains generated local-only evidence unless reviewed and governed.

GFOC-013 Curated evidence supports; it does not decide.

GFOC-014 Import candidate is not import approval.

GFOC-015 Trackable output only under future gate is not tracking approval.

GFOC-016 Blocked generated local-only output must not be imported, tracked, or published.

GFOC-017 P10.4 does not execute Graphify.

GFOC-018 P10.4 does not read raw Graphify outputs.

GFOC-019 P10.4 does not import Graphify outputs.

GFOC-020 P10.4 does not approve generated output tracking.

GFOC-021 P10.4 does not approve source tracking expansion.

GFOC-022 P10.4 does not modify `.graphifyignore`.

GFOC-023 P10.4 does not start P10.5.

GFOC-024 Governance documents override Graphify evidence.

GFOC-025 Never recommend git add ..

## Future Validation Targets

- GraphifyOutputRecord required fields completeness
- raw_generated_evidence default classification check
- curated_evidence review requirement completeness
- derived_report authority disclaimer check
- import_candidate no-import-approval invariant
- blocked_generated_local_only_output blocker preservation
- trackable_output_only_under_future_gate no-tracking invariant
- GraphifyCitationRef required fields completeness
- stale_evidence marker completeness
- conflicting_evidence marker completeness
- retention / rollback / incident posture completeness
- EvidenceRef conformance
- SecurityRef conformance
- ValidationRef conformance
- no-authority-drift invariant
- no-source-of-truth-drift invariant
- no-approval-drift invariant
- no-runtime-drift invariant
- no-CSS-substrate-drift invariant
- no-generated-output-tracking-without-gate invariant
- no-source-tracking-expansion-without-gate invariant
- blocked-scope-output classification check
- P10.5 output classification readiness check
- P10.6 report classification conformance
- P10.7 import boundary classification conformance
- P10.R closure classification audit

No future validation target is executed by P10.4.

## Future Hardening Candidates

- GFOC-HARD-01 - GraphifyOutputRecord Schema Alignment
- GFOC-HARD-02 - Graphify Citation / Reference Contract
- GFOC-HARD-03 - Graphify Staleness / Conflict Marker Contract
- GFOC-HARD-04 - Graphify Curated Evidence Promotion Checklist
- GFOC-HARD-05 - Graphify Generated Output Retention Checklist
- GFOC-HARD-06 - Graphify Import Candidate Review Checklist
- GFOC-HARD-07 - Graphify No-Authority-Drift Validation Checklist
- GFOC-HARD-08 - Graphify Tracking Gate Checklist

These are candidates only. P10.4 does not start them.

## Created / Not Created Register

Created:

- Graphify evidence output classification document created
- GraphifyOutputRecord model created
- GraphifyRawOutputRef model created
- GraphifyCuratedEvidenceRef model created
- GraphifyReviewedEvidenceRef model created
- GraphifyDerivedReportRef model created
- GraphifyImportCandidateRef model created
- GraphifyAcceptedEvidenceRef model created
- GraphifyRejectedEvidenceRef model created
- GraphifyStaleEvidenceRef model created
- GraphifyConflictRef model created
- GraphifyBlockedOutputRef model created
- GraphifyTrackableCandidateRef model created
- GraphifyRetentionRef model created
- GraphifyRollbackRef model created
- GraphifyIncidentRef model created
- GraphifyCitationRef model created
- GraphifyReviewRequirement model created
- raw generated evidence classification defined
- curated evidence classification defined
- derived report classification defined
- import candidate classification defined
- blocked/generated local-only output classification defined
- trackable output only under future gate classification defined

Not created / not approved:

- no Graphify execution
- no Graphify rerun
- no /graphify execution
- no raw Graphify output read
- no Graphify output import
- no automatic evidence import
- no Graph DB created
- no vector DB created
- no embeddings generated
- no Cognitive Semantic System substrate selected
- no generated output tracking approved
- no source tracking expansion approved
- no .graphifyignore modified
- no .gitignore modified
- no generated outputs modified/tracked
- no 9_artifacts read or modified
- no graphify-out read or modified
- no external source inspection
- no 4_external/sources inspection
- no product/Siamese source inspection
- no secrets inspected
- no credentials inspected
- no .env inspected
- no provider configs inspected
- no token stores inspected
- no browser auth inspected
- no local credential stores inspected
- no API keys inspected
- no provider/auth/API/MCP activation
- no credential use
- no API calls
- no MCP activation
- no live connector activation
- no runtime activation
- no agent execution
- no validation execution
- no tests / CI / scripts / builds
- no security enforcement activation
- no publication
- no Git mutation
- no P10.5 started
- no P10.6 started
- no P10.7 started
- no P10.R started
- no P11/P12/P13/P14 started

## Recommended Next Tickets

P10.4 is one preparation ticket after P10.0.

Parallel preparation tickets after P10.0:

- P10.2 - Graphify Markdown Scope Safety Review
- P10.3 - Graphify Controlled Rerun Plan
- P10.4 - Graphify Evidence Output Classification
- P10.1 - Graphify Ignore Policy Patch may be generated in parallel, but execution should be conditioned on P10.0 and preferably P10.2.

After P10.1-P10.4 are accepted:

- P10.5 - Graphify Controlled Rerun Execution

After P10.5:

- P10.6 - Graphify Markdown Evidence Refresh Report
- P10.7 - Graphify Evidence Import Boundary

After P10.6 and P10.7:

- P10.R - Graphify Evidence Integration Closure

Recommended actual: Continue P10 preparation tickets until P10.1-P10.4 are complete.

Do not start P10.5 inside P10.4.

## Final Verdict

What did P10.4 create? `0_architecture/governance/agent_platform_graphify_evidence_output_classification.md`.

What output classification model was defined? A Graphify evidence output classification model covering raw generated evidence, curated evidence, reviewed evidence, derived reports, import candidates, accepted/rejected evidence, stale/conflicting evidence, blocked local-only output, trackable-only-under-future-gate output, quarantined output, and delete-candidate output.

What is the default classification for Graphify outputs? `raw_generated_evidence`.

What is raw generated evidence? Generated local-only Graphify evidence immediately after a future controlled run, not reviewed, not imported, not tracked, and not authority.

What is curated evidence? Manually reviewed, scoped, limited supporting evidence that preserves EvidenceRef, SecurityRef, ValidationRef, retention, rollback, incident, and limitations posture.

What is reviewed evidence? Evidence with a reviewer status and limitations, still not authority or approval.

What is a derived report? A human- or agent-created report based on Graphify outputs that cites evidence without converting it into authority.

What is an import candidate? A Graphify-derived record proposed for future consumption by AGENT PLATFORM, not import approval.

What is blocked/generated local-only output? Output with blocked-scope, unknown sensitivity, secret, credential, product/Siamese, external source, raw generated-output, local-only, or source tracking risk that must not be imported, tracked, published, or summarized unsafely.

What is trackable output only under future gate? Output that could only be recommended for tracking after exact future gate approval and exact path review.

Can Graphify output become authority? No.

Can Graphify output become source of truth operativo? No.

Can Graphify output approve actions? No.

Can Graphify output activate runtime? No.

Can Graphify output select Cognitive Semantic System substrate? No.

Did P10.4 execute Graphify? No.

Did P10.4 read raw Graphify outputs? No.

Did P10.4 import outputs? No.

Did P10.4 approve generated output tracking? No.

Did P10.4 approve source tracking expansion? No.

Did P10.4 modify `.graphifyignore`? No.

Did P10.4 inspect external sources? No.

Did P10.4 inspect product/Siamese source? No.

Did P10.4 inspect secrets or credentials? No.

Did P10.4 mutate Git? No.

What is the next ticket? Continue P10 preparation tickets until P10.1-P10.4 are complete; do not start P10.5 inside P10.4.

Expected final declaration: `graphify_evidence_output_classification_ready_for_P10_5`.
