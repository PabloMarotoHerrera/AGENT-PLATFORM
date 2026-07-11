# P2.2 - Cross-Lane Evidence Reference Contract

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | Cross-Lane Evidence Reference Contract |
| Ticket | P2.2 |
| Status | Accepted cross-lane evidence reference contract |
| Date | 2026-07-04 |
| Scope | Define the shared evidence reference contract across the P1 metadata-only lanes: context, providers/adapters, tools, agents, and Cognitive Semantic System. |
| Authority | Cross-lane evidence reference contract only, not validation execution, security enforcement runtime, source loading, source tracking approval, generated output tracking, provider/auth approval, API approval, MCP activation, tool execution approval, agent execution approval, product activation, Graphify adoption, or Cognitive Semantic System substrate selection. |
| Related documents | P0.1 Activation Gate Enforcement Map, P0.2 Validation Execution Gate Design, P0.3 Security Enforcement Hardening Plan, G-19 Hybrid Parallel Work Packet Dependency Map, activation gate charter, implementation audit, P1.1 Context Runtime Contract Hardening, P1.2 Provider Adapter Metadata Contract Hardening, P1.3 Tool Execution Boundary Contract Hardening, P1.4 Agent Runtime Boundary Contract Hardening, P1.5 Cognitive Semantic System Prototype Hardening, P2.1 not present and therefore not consumed, I-03 Context Pack Runtime, I-04 Provider / Adapter Layer, I-06 Tool Execution Boundary, I-05 Agent Runtime Boundary, I-07 Cognitive Semantic System Prototype, I-01 Validation Registry Implementation, I-02 Security / Access Enforcement, S-03 Local-only / Secrets / Credentials Policy, S-04 Tool / Shell / Network / MCP Execution Policy, CSS ADR/audit, Graphify Repo Map Summary, `.gitignore`, `.graphifyignore`, README.md. |
| Output | Cross-lane evidence reference contract. |

This document is the canonical Cross-Lane Evidence Reference Contract for AGENT PLATFORM / Siamese. P2.2 is cross-lane documentation and governance integration only.

## 2. Purpose

P1 hardened component-specific metadata contracts for context, providers/adapters, tools, agents, and the Cognitive Semantic System.

P2 integrates those contracts transversally without activation. P2.2 defines the common EvidenceRef shape and its relationships to SourceRef, ValidationRef, SecurityRef, GraphifyRef, ProductRef, generated outputs, local-only material, limitations, retention, and review requirements.

P2.2 resolves evidence-reference drift. P2.1 Shared Metadata Vocabulary Alignment is present and canonical; the former `pending_P2.1_alignment` markers are historical and closed by cross-lane reconciliation.

P2.2 does not run validation. P2.2 does not activate runtime. P2.2 does not start P2.3 or P3.1.

## 3. Current Cross-Lane Evidence Posture

P1.1 through P1.5 are metadata-only hardening lanes. Context, provider, tool, agent, and Cognitive Semantic System records may cite evidence.

Evidence references are not evidence content by default. Evidence content access remains governed by source classification, sensitivity, local-only posture, generated-output posture, product posture, validation posture, security posture, and retention posture.

Evidence supports; governance decides.

Evidence is not authority by itself.

Validation evaluates; governance decides.

Graphify evidence is supporting generated evidence only, not authority.

AGENT PLATFORM remains pre-active at AL-1.

## 4. Cross-Lane Evidence Reference Contract Definition

A cross-lane EvidenceRef is a metadata reference that records what evidence supports a claim, object, blocker, limitation, validation posture, security posture, or readiness assertion across AGENT PLATFORM lanes without embedding raw evidence content, authorizing evidence access, approving validation execution, approving source loading, approving source tracking, approving generated output tracking, approving provider/auth/API/MCP activation, approving tool execution, approving agent execution, activating the Siamese product, adopting Graphify as authority, or selecting a Cognitive Semantic System substrate.

| Clarification | Rule |
| --- | --- |
| EvidenceRef is metadata, not raw evidence content. | The record identifies evidence posture and references only. |
| Evidence supports; governance decides. | Evidence cannot decide governance. |
| Evidence is not authority by itself. | Cited evidence cannot become approval by citation. |
| EvidenceRef is not source loading approval. | Raw source access remains blocked until exact future gates approve. |
| EvidenceRef is not source tracking approval. | GT-02 and GT-12 remain required for tracking, staging, commit, push, force-add, or publication. |
| EvidenceRef is not validation execution approval. | GT-04 remains required for validation execution. |
| EvidenceRef is not security approval. | Security review and enforcement remain future-gated. |
| EvidenceRef is not provider/auth approval. | GT-08 and secure approval remain required. |
| EvidenceRef is not tool execution approval. | GT-07 remains required. |
| EvidenceRef is not agent execution approval. | Agent runtime and task execution remain blocked. |
| EvidenceRef is not product activation. | GT-09 remains required for product source and product activation. |
| EvidenceRef is not Graphify adoption. | Graphify remains supporting generated evidence only. |
| EvidenceRef is not Cognitive Semantic System substrate selection. | Cognitive Semantic System substrate remains deferred. |

## 5. Canonical EvidenceRef Shape

| field | required | meaning | allowed values or posture | forbidden content | validation posture | security posture |
| --- | --- | --- | --- | --- | --- | --- |
| `evidence_ref_id` | yes | Stable cross-lane evidence metadata identifier. | Unique ID scoped to the record family. | Raw evidence content or encoded payloads. | Future completeness check only. | Must not reveal sensitive values. |
| `evidence_kind` | yes | Evidence class. | Canonical terms in section 6 aligned with P2.1. | Secret, credential, raw source, or provider payload class disguised as evidence. | Vocabulary conformance future target. | Unknown kind blocks promotion. |
| `evidence_label` | yes | Human-readable safe label. | Safe metadata label. | Secret values, credentials, private identifiers, raw source excerpts. | Label consistency future target. | Redact or omit sensitive label details. |
| `evidence_scope` | yes | Exact claim, object, blocker, limitation, or posture supported. | Exact scope only. | Broad authority claims. | Scope completeness future target. | Broad or unknown scope blocks promotion. |
| `evidence_owner` | yes | Accountable owner or owning lane. | Governance, validation, security, context, provider, tool, agent, Cognitive Semantic System, Graphify evidence, product-readiness, audit, or `unknown`. | Credential owner details beyond safe metadata. | Owner required for future validation. | Unknown owner requires review. |
| `evidence_status` | yes | Current evidence status. | Canonical terms in section 7 aligned with P2.1. | Activation or approval status by implication. | Status vocabulary future target. | Blocked statuses must propagate. |
| `evidence_source_ref` | yes | SourceRef or source metadata reference. | SourceRef ID, curated summary ref, or blocked-source marker. | Raw source body, raw generated output, `.env` content. | Source relationship future target. | Preserve source sensitivity and classification. |
| `source_ref_relationship` | yes | How the EvidenceRef relates to SourceRef. | Terms in section 8. | Permission to read or track source. | Relationship conformance future target. | Blocked source relationships constrain use. |
| `validation_refs` | yes | ValidationRef IDs related to the evidence. | IDs, `none`, or blocked/future refs. | Validation command output unless future-gated and reviewed. | Validation relationship future target. | Sensitive validation output blocked. |
| `validation_ref_relationship` | yes | How validation posture relates to the evidence. | Terms in section 9. | Validation execution approval. | Must preserve not-executed and blocked states. | Security-sensitive validation requires review. |
| `security_refs` | yes | SecurityRef IDs constraining the evidence. | IDs, policy refs, blocker refs, or `none` only when no constraint is known. | Secret or credential values. | Security relationship future target. | Unknown security posture blocks promotion. |
| `security_ref_relationship` | yes | How security posture constrains the evidence. | Terms in section 10. | Security approval by citation. | Future blocker-preservation target. | Security refs are blockers unless exact gate says otherwise. |
| `graphify_refs` | yes | GraphifyRef IDs, if generated Graphify evidence is involved. | Curated summary refs or blocked raw-output refs. | Raw Graphify output, raw visuals, generated labels as authority. | Graphify support-only invariant future target. | Raw generated Graphify output remains local-only. |
| `graphify_ref_relationship` | yes | How Graphify evidence relates to the EvidenceRef. | Terms in section 11. | Graphify authority or substrate claim. | Future Graphify relationship target. | Graphify refs cannot bypass generated-output blockers. |
| `product_refs` | yes | ProductRef IDs, if product-readiness evidence is involved. | Product-readiness metadata, product gate refs, product blockers. | Product source content or product output payloads. | Product readiness future target. | Product source remains blocked until GT-09. |
| `product_ref_relationship` | yes | How ProductRef relates to evidence. | Terms in section 12. | Product activation or source inspection approval. | Future product relationship target. | Product blockers propagate. |
| `generated_output_posture` | yes | generated_output evidence posture for generated material. | Terms in section 13. | Raw generated payloads. | Future propagation target. | Generated output is local-only/generated-sensitive by default. |
| `local_only_posture` | yes | local-only evidence posture. | Terms in section 14. | Local-only content dumps. | Future propagation target. | Blocks publication and provider-bound transmission by default. |
| `sensitivity` | yes | Highest inherited sensitivity. | Public metadata, governance metadata, generated-sensitive, local-only, product-restricted, external, secret, credential, unknown. | Values that reveal secrets or credentials. | Sensitivity propagation future target. | Unknown, secret, or credential sensitivity blocks use. |
| `source_classification` | yes | Classification of referenced source or evidence origin. | Governance, implementation, validation, security, context, provider, tool, agent, semantic, Graphify summary, generated, local-only, product, external, audit, unknown. | Raw source content. | Classification conformance future target. | Unknown classification blocks promotion. |
| `authority_posture` | yes | Whether evidence has authority. | Terms in section 15. | Self-approval, Graphify authority, proof-as-governance. | Evidence-not-authority future target. | Authority unknown blocks promotion. |
| `decision_posture` | yes | Whether a decision exists and where. | Terms in section 15. | Decision embedded by evidence itself. | Decision posture future target. | Activation requires exact governance gate. |
| `retention_posture` | yes | How evidence metadata is retained. | Terms in section 17. | Retained secret or credential values, raw local-only dumps. | Retention propagation future target. | Quarantine/remove unsafe material. |
| `review_required` | yes | Required future reviews. | Terms in section 18. | Review treated as approval. | Review requirement future target. | Security review required for sensitive evidence. |
| `evidence_limitations` | yes | Known limitations and blocked inferences. | Limitation objects from section 16. | Claims that erase limitations. | Limitation propagation future target. | Limitations constrain promotion and publication. |
| `blockers` | yes | Active blockers attached to the evidence. | Gate, source, validation, security, local-only, product, provider, tool, agent, generated-output, retention blockers. | Bypass instructions or hidden exceptions. | Blocker preservation future target. | Blockers are binding until exact future gate changes them. |
| `aliases` | yes | Non-canonical aliases for readability or migration. | Safe alias terms only. | Deprecated terms as canonical. | Alias/deprecated detection future target. | Aliases cannot weaken blockers. |
| `deprecated_terms` | yes | Terms that must not be canonical downstream. | Deprecated or rejected examples. | Deprecated terms used as accepted names. | Deprecated-term detection future target. | Historical/rejected terms must be marked. |
| `pending_alignment_refs` | yes | Vocabulary or schema alignment dependencies. | Open alignment references only; the P2.1 marker is closed. | Silent vocabulary drift. | Alignment check future target. | Unknown drift requires review. |

EvidenceRef must never include raw secret values, credential values, API keys, tokens, passwords, private keys, browser auth, provider configs, `.env` contents, raw local-only source, raw product source, raw external source, raw generated Graphify output, provider output payloads, tool execution output payloads, or agent execution output payloads.

## 6. Evidence Kind Vocabulary

P2.1 is present. The evidence-kind vocabulary in this section is reconciled with the canonical shared vocabulary.

| evidence_kind | meaning | examples | allowed AL-1 use | blocked use | required future gate |
| --- | --- | --- | --- | --- | --- |
| `governance_document` | Accepted or draft governance document metadata. | P0.1, P0.2, P0.3, G-19, G-01, P1 records. | Cite metadata, blockers, decisions, limitations; `pending_P2.1_alignment`. | Runtime activation or broad approval. | Relevant GT gate for any activation. |
| `implementation_record` | Architecture implementation record, not live source. | I-01 through I-07, I-A. | Cite metadata-only component posture. | Reading live source or executing implementation. | GT-01, GT-04, GT-05, GT-07 as applicable. |
| `validation_record` | Validation design or metadata result posture. | P0.2, future validation records. | Cite validation posture and not-executed blockers. | Treating validation as governance approval. | GT-04 for execution. |
| `security_record` | Security policy or review metadata. | S-03, S-04, P0.3, I-02. | Cite constraints and blockers. | Treating security ref as runtime enforcement or activation. | GT-05 plus exact future gate. |
| `context_metadata` | Context pack, item, source ref, or context hardening metadata. | P1.1 context records. | Cite context metadata and blockers. | Source loading or provider transmission. | GT-01, GT-05, GT-08 as applicable. |
| `provider_metadata` | Provider/adapter metadata. | P1.2 provider descriptors. | Cite provider blockers and auth/network posture. | Provider/auth/API/MCP activation. | GT-08. |
| `tool_metadata` | Tool descriptor, request, decision, or output metadata. | P1.3 tool records. | Cite execution blockers and risk metadata. | Tool execution, shell, subprocess, Git, build/test/package actions. | GT-07, GT-14, GT-12 as applicable. |
| `agent_metadata` | Agent runtime, task, handoff, approval, or output metadata. | P1.4 agent records. | Cite agent blockers and metadata posture. | Agent runtime activation, task execution, handoff execution. | GT-06 and related gates. |
| `semantic_record` | Cognitive Semantic System entity, claim, relation, or substrate candidate metadata. | P1.5 semantic records. | Cite semantic metadata and substrate blockers. | Truth creation, reasoning runtime, substrate selection. | GT-10, GT-13 if state. |
| `graphify_summary` | Curated generated Graphify summary. | Graphify Repo Map Summary. | Supporting generated evidence with limitations. | Authority, source truth, substrate decision. | GT-04/GT-11/GT-12/GT-08 if rerun/provider/tracking. |
| `generated_output_summary` | Curated or safe summary of generated output. | Reviewed generated report summary. | Metadata citation with retention posture. | Raw payload publication or source tracking. | GT-05, GT-12, GT-15. |
| `generated_raw_output` | Raw generated artifact or output. | Raw Graphify output, logs, reports, provider output. | Blocked marker only. | Raw inclusion, authority, publication, tracking. | GT-05, GT-12, GT-15 and exact scope. |
| `local_only_metadata` | Safe metadata about local-only material. | Path/category/risk metadata. | Cite safe metadata only. | Reading or embedding content. | GT-01 and GT-05. |
| `local_only_source` | Raw local-only source or corpus. | Previous knowledge, datasets, artifacts, logs. | Blocked marker only. | Raw content loading, provider transmission, publication. | Exact source/security gate. |
| `product_readiness_metadata` | Siamese readiness metadata. | Product gate requirements, product blockers. | Cite readiness and blockers. | Product source inspection or activation. | GT-09. |
| `product_source` | Raw product source or product output. | Siamese source, product artifacts. | Blocked marker only. | Inspection, execution, source loading, tracking. | GT-09 plus security/validation/source posture. |
| `external_reference` | External-source metadata or external evidence reference. | External architecture metadata. | Cite metadata/provenance only. | Raw source adoption, execution, instruction adoption. | GT-11 plus security/license review. |
| `incident_record` | Safe incident metadata. | Quarantine, stop, exposure category. | Cite safe category and required response. | Secret values, payload dumps, remediation execution. | GT-15 and security review. |
| `audit_record` | Audit, retention, rollback, or review metadata. | I-A, future P2.3 audit records. | Cite audit posture and blockers. | Operational logging, persistence, publication by citation. | GT-15 and future audit gates. |
| `unknown_evidence` | Unclassified or mixed evidence. | Unknown source, unknown sensitivity. | Blocked marker only. | Promotion or activation. | Classification/security review. |

## 7. Evidence Status Vocabulary

P2.1 is absent. All evidence status vocabulary in this section is `pending_P2.1_alignment`.

| evidence_status | meaning | allowed use | blocked inference |
| --- | --- | --- | --- |
| `draft` | Incomplete evidence metadata. | Record early metadata with blockers. | Approval or acceptance. |
| `proposed` | Evidence is proposed for review. | Cite as unaccepted candidate. | Governance decision. |
| `referenced` | Evidence is cited by a metadata record. | Trace support. | Authority by citation. |
| `reviewed_metadata` | Metadata was reviewed without raw content activation. | Support metadata confidence. | Validation execution or activation. |
| `accepted_metadata_evidence` | Governance accepts metadata evidence for exact scope. | Support exact-scope metadata decisions. | Runtime, product, source, provider, tool, or agent activation. |
| `generated_unreviewed` | Generated evidence exists but is unreviewed. | Blocked generated marker. | Truth, authority, publication. |
| `generated_curated` | Generated evidence has curated safe summary. | Supporting generated evidence with limitations. | Raw-output tracking or authority. |
| `local_only_blocked` | Local-only posture blocks content use. | Safe metadata marker only. | Publication or provider transmission. |
| `product_blocked` | Product boundary blocks use. | Product readiness marker. | Product activation or source inspection. |
| `external_blocked` | External-source boundary blocks use. | External evidence marker. | External adoption or execution. |
| `security_blocked` | Security posture blocks use. | Preserve blocker. | Security approval or bypass. |
| `validation_blocked` | Validation posture blocks proof claim. | Preserve not-executed or failed posture. | Validation approval. |
| `deprecated` | Replaced or no longer valid. | Historical trace only. | Current canonical use. |
| `superseded` | Newer evidence replaces this. | Trace supersession. | Current authority. |
| `rejected_for_scope` | Evidence is unsafe, broad, or wrong scope. | Preserve rejection. | Adjacent use. |
| `unknown_status` | Status is unknown. | Blocked marker. | Promotion or activation. |

## 8. SourceRef Relationship Contract

| source_ref_relationship | meaning |
| --- | --- |
| `cites_source_metadata` | Evidence cites source metadata only. |
| `cites_source_path_only` | Evidence cites path/identifier only, not content. |
| `cites_curated_summary` | Evidence cites a curated safe summary. |
| `cites_generated_summary` | Evidence cites generated summary metadata. |
| `cites_raw_generated_output_blocked` | Evidence points to raw generated output but blocks access. |
| `cites_local_only_metadata` | Evidence cites safe local-only metadata. |
| `cites_local_only_source_blocked` | Evidence points to local-only source but blocks content access. |
| `cites_product_metadata` | Evidence cites product-readiness metadata. |
| `cites_product_source_blocked` | Evidence points to product source but blocks content access. |
| `cites_external_metadata` | Evidence cites external metadata only. |
| `cites_external_source_blocked` | Evidence points to external raw source but blocks content access. |
| `cites_secret_or_credential_ref_blocked` | Evidence records that secret or credential material is implicated and blocked. |
| `unknown_source_relationship` | Relationship is unknown and blocks promotion. |

SourceRef relationship is not permission to read source. SourceRef relationship is not source tracking approval.

SourceRef relationship must preserve source classification, sensitivity, local-only flags, product flags, external flags, generated-output flags, credential flags, and secret flags.

Raw source content remains blocked unless future exact-scope gates approve access. Product source remains blocked until GT-09. Generated outputs remain local-only/generated-sensitive unless curated by future gates.

## 9. ValidationRef Relationship Contract

| validation_ref_relationship | meaning |
| --- | --- |
| `cites_validation_design` | Evidence cites validation design or gate design. |
| `cites_validation_requirement` | Evidence cites a validation requirement or future target. |
| `cites_validation_result_metadata` | Evidence cites result metadata only, not raw output. |
| `cites_not_executed_validation` | Evidence records that validation was not executed. |
| `cites_future_validation_target` | Evidence cites a future proposed validation target. |
| `cites_blocked_validation` | Evidence cites validation blocked by gate, scope, security, source, or product posture. |
| `cites_failed_validation` | Evidence cites failed validation metadata. |
| `cites_unknown_validation_posture` | Validation posture is unknown and blocks proof promotion. |

ValidationRef relationship is not validation execution approval. Validation records can support evidence posture but cannot decide governance approval.

Validation evidence must cite GT-04 when execution is involved in the future. P2.2 does not run validation. Validation evaluates; governance decides.

## 10. SecurityRef Relationship Contract

| security_ref_relationship | meaning |
| --- | --- |
| `cites_security_policy` | Evidence cites security policy. |
| `cites_security_requirement` | Evidence cites security requirement. |
| `cites_security_review_metadata` | Evidence cites review metadata only. |
| `cites_security_blocker` | Evidence cites active security blocker. |
| `cites_incident_requirement` | Evidence cites incident handling requirement. |
| `cites_retention_requirement` | Evidence cites retention, redaction, quarantine, or deletion requirement. |
| `cites_publication_blocker` | Evidence cites publication, Git, tracking, or provider-transmission blocker. |
| `cites_unknown_security_posture` | Security posture is unknown and blocks promotion. |

SecurityRef relationship is not security approval by itself.

Security refs constrain evidence access, retention, publication, provider transmission, source loading, generated output handling, product access, MCP use, tool use, agent use, and credential handling.

EvidenceRef must consume security refs as blockers unless an exact future gate says otherwise. Unknown security posture blocks evidence promotion.

## 11. GraphifyRef Relationship Contract

| graphify_ref_relationship | meaning |
| --- | --- |
| `cites_curated_graphify_summary` | Evidence cites a curated safe Graphify summary. |
| `cites_graphify_repo_map_summary` | Evidence cites the Graphify Repo Map Summary. |
| `cites_graphify_generated_evidence` | Evidence cites generated Graphify evidence posture. |
| `cites_raw_graphify_output_blocked` | Evidence points to raw Graphify output but blocks access. |
| `cites_graphify_label_metadata` | Evidence cites generated label metadata as non-governance labels. |
| `cites_graphify_drift_observation` | Evidence cites observed drift or limitation from Graphify evidence. |
| `cites_graphify_limitations` | Evidence cites limitations of generated Graphify evidence. |
| `unknown_graphify_relationship` | Graphify relationship is unknown and blocks promotion. |

Graphify repo map summary is curated generated evidence only. Raw Graphify output under `9_artifacts/` is local-only. Graphify labels are not governance labels. `.graphifyignore` constrains Graphify input but is not permission.

Graphify evidence is supporting generated evidence only, not authority.

Graphify evidence cannot approve source loading, provider/auth, tool execution, agent execution, product activation, generated output tracking, source tracking expansion, or Cognitive Semantic System substrate selection.

## 12. ProductRef Relationship Contract

| product_ref_relationship | meaning |
| --- | --- |
| `cites_product_vision_metadata` | Evidence cites Siamese product vision metadata. |
| `cites_product_readiness_metadata` | Evidence cites readiness metadata or gate prerequisites. |
| `cites_product_gate_requirement` | Evidence cites product gate requirement. |
| `cites_product_source_blocked` | Evidence points to product source but blocks content access. |
| `cites_product_activation_blocker` | Evidence cites activation blocker. |
| `cites_product_rollback_requirement` | Evidence cites rollback requirement for future product work. |
| `cites_product_incident_requirement` | Evidence cites product incident handling requirement. |
| `unknown_product_relationship` | Product relationship is unknown and blocks promotion. |

Siamese is product vision, not product activation. ProductRef is metadata only. ProductRef is not product source inspection approval. ProductRef is not product activation.

Product source remains blocked until GT-09. Product-bound evidence requires security review, validation posture, source tracking posture, rollback posture, incident handling posture, and exact-scope governance approval before future activation.

## 13. Generated Output Evidence Posture

This section defines generated_output evidence posture values.

| generated_output_posture | meaning |
| --- | --- |
| `not_generated` | Evidence is not generated output. |
| `generated_metadata_only` | Evidence records generated-output metadata only. |
| `generated_summary_unreviewed` | Generated summary exists but has not been reviewed. |
| `generated_summary_curated` | Generated summary was curated for safe metadata use. |
| `generated_raw_output_blocked` | Raw generated output exists or is referenced but blocked. |
| `generated_sensitive_local_only` | Generated output is local-only/generated-sensitive. |
| `generated_output_tracking_not_approved` | Tracking is not approved. |
| `generated_output_tracking_required_future` | Future tracking would require gate approval. |
| `generated_output_quarantine_required` | Quarantine or removal review is required. |
| `unknown_generated_output_posture` | Generated-output posture is unknown and blocks promotion. |

Generated output evidence is not source by default. Generated output evidence cannot become authority by being cited. Raw generated output remains blocked by default. Generated Graphify output remains local-only unless curated through future gates.

P2.2 does not approve generated output tracking. Any generated-output evidence must include limitations and retention posture.

## 14. Local-Only Evidence Posture

This section defines local-only evidence posture values.

| local_only_posture | meaning |
| --- | --- |
| `not_local_only` | Evidence is not local-only. |
| `local_only_metadata` | Safe metadata about local-only material. |
| `local_only_summary` | Safe summary of local-only posture, not content. |
| `local_only_source_blocked` | Local-only source content is blocked. |
| `local_only_generated_output_blocked` | Local-only generated output content is blocked. |
| `local_only_secret_or_credential_blocked` | Secret or credential material is implicated and blocked. |
| `local_only_product_blocked` | Product local-only posture blocks use. |
| `local_only_publication_blocked` | Publication is blocked by local-only posture. |
| `unknown_local_only_posture` | Local-only posture is unknown and blocks promotion. |

Local-only evidence may be cited as metadata only when allowed by exact scope. Local-only evidence content must not be embedded by default.

Local-only evidence blocks publication by default. Local-only evidence blocks provider-bound transmission by default. Local-only source loading remains blocked. Local-only posture must propagate downstream.

## 15. Evidence Authority And Decision Posture

| authority_posture | meaning |
| --- | --- |
| `supporting_evidence_only` | Evidence supports a claim but does not decide it. |
| `not_authority` | Evidence has no authority status. |
| `governance_record_reference` | Evidence cites a governance record without becoming that record. |
| `validation_record_reference` | Evidence cites validation posture without deciding governance. |
| `security_record_reference` | Evidence cites security posture without granting permission. |
| `generated_evidence_not_authority` | Generated evidence is not authority. |
| `graphify_evidence_not_authority` | Graphify evidence is not authority. |
| `semantic_claim_not_authority` | Semantic claim is not authority by itself. |
| `unknown_authority_posture` | Authority posture is unknown and blocks promotion. |

| decision_posture | meaning |
| --- | --- |
| `no_decision` | No decision is recorded. |
| `decision_pending_governance` | Governance decision is pending. |
| `decision_requires_validation` | Future validation review is required. |
| `decision_requires_security` | Future security review is required. |
| `decision_requires_exact_scope_gate` | Exact future gate is required. |
| `decision_recorded_elsewhere` | Decision belongs to another cited governance record. |
| `decision_not_allowed_by_evidence` | Evidence cannot decide this matter. |
| `unknown_decision_posture` | Decision posture is unknown and blocks promotion. |

Evidence supports; governance decides. EvidenceRef cannot approve its own use. EvidenceRef cannot promote metadata to activation. Semantic inclusion is not truth creation. Validation records evaluate but do not govern by themselves. Security records constrain but do not activate by themselves. Graphify evidence is not authority.

## 16. Evidence Limitations Contract

| evidence_limitations field | meaning |
| --- | --- |
| `limitation_id` | Stable limitation identifier. |
| `limitation_type` | Limitation type from this section. |
| `limitation_description` | Safe description of the limitation. |
| `impacted_lanes` | Lanes affected by the limitation. |
| `blocked_inference` | Inference that must not be made. |
| `required_review` | Review required before promotion or use. |
| `required_gate` | Future gate required, if any. |
| `retention_impact` | Retention, redaction, quarantine, deletion, or publication impact. |
| `downstream_propagation_required` | Whether the limitation must travel downstream. |

| limitation_type | meaning |
| --- | --- |
| `incomplete_evidence` | Evidence metadata is incomplete. |
| `stale_evidence` | Evidence may be stale. |
| `generated_unreviewed` | Generated evidence is unreviewed. |
| `generated_local_only` | Generated evidence is local-only. |
| `source_unread` | Source content was not read. |
| `source_classification_unknown` | Source classification is unknown. |
| `sensitivity_unknown` | Sensitivity is unknown. |
| `product_blocked` | Product boundary blocks content use. |
| `external_blocked` | External boundary blocks use. |
| `credential_or_secret_related` | Credential or secret material is implicated. |
| `validation_not_executed` | Validation was not executed. |
| `security_not_reviewed` | Security review was not performed. |
| `graphify_support_only` | Graphify evidence is supporting only. |
| `vocabulary_pending_P2.1_alignment` | Vocabulary awaits P2.1 alignment. |
| `drift_detected_between_lanes` | Lane terms or semantics diverge and require review. |

## 17. Evidence Retention Contract

| retention_posture | meaning |
| --- | --- |
| `retain_metadata_only` | Retain only EvidenceRef metadata. |
| `retain_curated_summary_only` | Retain curated summary, not raw evidence. |
| `retain_until_superseded` | Retain until a newer record supersedes it. |
| `retain_with_redaction` | Retain only after redaction or omission of unsafe content. |
| `retain_local_only` | Retain locally only. |
| `retain_generated_sensitive` | Retain as generated-sensitive. |
| `quarantine_required` | Quarantine route is required. |
| `deletion_review_required` | Deletion/removal review is required. |
| `publication_blocked` | Publication is blocked. |
| `tracking_not_approved` | Source tracking is not approved. |
| `unknown_retention_posture` | Retention posture is unknown and blocks promotion. |

EvidenceRef retention is metadata retention, not raw evidence retention. Secret-bearing or credential-bearing evidence triggers quarantine/removal route. Product-source evidence remains blocked. Raw generated outputs remain blocked unless future gates approve.

Publication blockers must propagate. Source tracking blockers must propagate. P2.2 does not implement persistence, logging, telemetry, or automated retention.

## 18. Evidence Review Requirements

| review_required | meaning |
| --- | --- |
| `no_review_required_for_metadata_reference` | Metadata reference itself needs no further review for citation only. |
| `governance_review_required` | Governance review is required. |
| `validation_review_required` | Validation review is required. |
| `security_review_required` | Security review is required. |
| `source_tracking_review_required` | Source tracking or Git review is required. |
| `generated_output_review_required` | Generated output review is required. |
| `product_review_required` | Product review is required. |
| `provider_auth_review_required` | Provider/auth review is required. |
| `tool_execution_review_required` | Tool execution review is required. |
| `agent_execution_review_required` | Agent execution review is required. |
| `retention_review_required` | Retention, redaction, quarantine, or deletion review is required. |
| `incident_review_required` | Incident review is required. |
| `P2.1_alignment_required` | Shared vocabulary alignment is required. |
| `unknown_review_required` | Review requirement is unknown and blocks promotion. |

Review requirement is not approval. Security review is required for any evidence touching secrets, credentials, provider/auth, product source, local-only material, generated raw output, MCP, publication, or source tracking. Validation review is required for any evidence claimed as proof. Governance review is required for promotion or activation readiness. P2.2 does not perform these reviews.

## 19. Cross-Lane Evidence Mapping

| lane | evidence producer | evidence consumer | evidence ref object | required propagated blockers | required propagated limitations |
| --- | --- | --- | --- | --- | --- |
| Context lane | Context packs, items, source refs, P1.1 records. | Agents, tools, providers, validation, security, Cognitive Semantic System. | EvidenceRef with SourceRef, ValidationRef, SecurityRef. | Source loading, context permission, local-only, product, external, generated-output, secret, credential, provider-bound transmission blockers. | Source unread, sensitivity unknown, context inclusion not permission, generated/local-only limitations. |
| Provider/Adapter lane | ProviderDescriptor, AdapterDescriptor, CredentialRef, auth/network/MCP metadata. | Tools, agents, product-readiness, validation, security, Cognitive Semantic System. | EvidenceRef with ProviderRef, SecurityRef, ValidationRef, ProductRef. | Provider/auth/API/MCP, credential, network, context transmission, product, generated provider output blockers. | Credential metadata only, provider metadata not activation, API key availability not approval. |
| Tool lane | Tool descriptors, capabilities, requests, decisions, outputs. | Agents, validation, security, context, provider, Cognitive Semantic System. | EvidenceRef with ToolRef, ValidationRef, SecurityRef. | Tool execution, shell, subprocess, filesystem, network, package, build, test, CI, Git, MCP, generated-output blockers. | Tool metadata not execution, output generated-sensitive, unknown risk. |
| Agent lane | Agent runtime refs, task records, handoff records, output refs. | Context, tools, providers, validation, security, Cognitive Semantic System, product-readiness. | EvidenceRef with AgentRef, SourceRef, ValidationRef, SecurityRef. | Agent runtime, task execution, handoff execution, tool/provider/product/source-loading blockers. | Agent metadata not execution, generated agent output not authority. |
| Cognitive Semantic System lane | Semantic entities, claims, relations, substrate candidate records. | Governance, validation, security, context, product-readiness. | EvidenceRef with semantic refs, GraphifyRef, ProductRef. | Substrate selection, graph/vector/database/ontology runtime, persistence, source loading, truth-creation blockers. | Semantic claim not authority, substrate deferred, Graphify support only. |
| Validation lane | Validation design, validation target, future result metadata. | All lanes. | ValidationRef and EvidenceRef. | GT-04 not executed, failed validation, validation blocked, sensitive output blockers. | Validation evaluates; governance decides, validation not approval. |
| Security lane | S-03, S-04, P0.3, security review metadata. | All lanes. | SecurityRef and EvidenceRef. | Secret, credential, local-only, provider/auth, product, MCP, tool, source tracking, publication blockers. | Security constrains, not runtime enforcement by itself. |
| Graphify evidence lane | Curated Graphify Repo Map Summary, generated-evidence metadata. | Governance, Cognitive Semantic System, context, tools, agents, providers. | GraphifyRef and EvidenceRef. | Raw Graphify output, generated-output tracking, Graphify rerun, provider labels, Graphify adoption blockers. | Generated evidence only, not authority, not substrate. |
| Siamese product-readiness lane | Product-readiness metadata and gate requirements. | Governance, provider, agent, tool, Cognitive Semantic System, validation, security. | ProductRef and EvidenceRef. | GT-09 product source, product activation, product execution, product tracking blockers. | Siamese vision only, product source blocked, product-root collapse risk. |
| Audit/retention/rollback lane | Audit records, retention metadata, rollback and incident metadata. | All lanes. | EvidenceRef with retention posture and limitations. | Publication, tracking, quarantine, deletion review, incident, rollback blockers. | Metadata retention only, raw retention blocked, P2.3 not started. |

All lanes must preserve evidence sensitivity, source classification, local-only posture, generated-output posture, product posture, validation posture, security posture, blockers, limitations, retention posture, and review requirements.

## 20. Drift Detection And Alias Register

P2.1 is absent. Terms in this document are used for P2.2 and marked `pending_P2.1_alignment`.

| concept | canonical term | aliases | deprecated terms | affected lanes | resolution | pending alignment |
| --- | --- | --- | --- | --- | --- | --- |
| evidence reference | EvidenceRef | evidence refs, ProviderEvidenceRef, ToolEvidenceRef, AgentEvidenceRef, SemanticEvidenceRef | evidence authority | All lanes. | Use EvidenceRef for cross-lane object. | `pending_P2.1_alignment` |
| validation reference | ValidationRef | validation refs, ProviderValidationRef, ToolValidationRef, AgentValidationRef, SemanticValidationRef | validation approval | All lanes. | Use ValidationRef for validation posture. | `pending_P2.1_alignment` |
| security reference | SecurityRef | security refs, ProviderSecurityRef, ToolSecurityRef, AgentSecurityRef, SemanticSecurityRef | security approval by ref | All lanes. | Use SecurityRef for constraints. | `pending_P2.1_alignment` |
| source reference | SourceRef | source refs, ContextSourceRef, source path ref | source loading approval | Context, validation, security, all consumers. | Use SourceRef for metadata reference only. | `pending_P2.1_alignment` |
| graphify reference | GraphifyRef | SemanticGraphifyRef, graphify summary ref | Platform Graphify; Graphify Authority; Graphify owns truth | Graphify, Cognitive Semantic System, all consumers. | Rejected/prohibited/historical examples only; GraphifyRef is supporting generated-evidence reference only. | `pending_P2.1_alignment` |
| product reference | ProductRef | SemanticProductRef, product readiness ref | product activation ref | Product-readiness and all consumers. | Use ProductRef for product-readiness metadata only. | `pending_P2.1_alignment` |
| evidence status | evidence_status | status, ref status | approval status by evidence | All lanes. | Use section 7 terms until P2.1. | `pending_P2.1_alignment` |
| evidence limitation | evidence_limitations | limitations, evidence gaps | erased limitation | All lanes. | Use limitation object in section 16. | `pending_P2.1_alignment` |
| retention posture | retention_posture | retention class, output handling posture | raw retention approval | All lanes. | Use section 17 terms. | `pending_P2.1_alignment` |
| generated output posture | generated_output_posture | generated-output profile, generated evidence posture | generated source by default | Tool, Graphify, validation, product, all lanes. | Use section 13 terms. | `pending_P2.1_alignment` |
| local-only posture | local_only_posture | local-only profile, local evidence posture | local-only safe by default | Context, security, product, Graphify, all lanes. | Use section 14 terms. | `pending_P2.1_alignment` |
| authority posture | authority_posture | evidence authority posture | evidence as authority | All lanes. | Use section 15 terms. | `pending_P2.1_alignment` |
| decision posture | decision_posture | governance decision posture | evidence decision | All lanes. | Use section 15 terms. | `pending_P2.1_alignment` |

If P2.1 exists in the future, use its canonical vocabulary. Because P2.1 does not exist now, use the terms in this document and mark them as `pending_P2.1_alignment`. Deprecated terms must not be used as canonical terms downstream. Aliases may be recorded for migration/readability only.

## 21. Evidence Contract Invariants

| ID | Invariant |
| --- | --- |
| EVD-001 | EvidenceRef is metadata, not raw evidence content. |
| EVD-002 | Evidence supports; governance decides. |
| EVD-003 | Evidence is not authority by itself. |
| EVD-004 | EvidenceRef is not source loading approval. |
| EVD-005 | EvidenceRef is not source tracking approval. |
| EVD-006 | EvidenceRef is not validation execution approval. |
| EVD-007 | EvidenceRef is not security approval. |
| EVD-008 | EvidenceRef is not provider/auth/API/MCP activation. |
| EVD-009 | EvidenceRef is not tool execution approval. |
| EVD-010 | EvidenceRef is not agent execution approval. |
| EVD-011 | EvidenceRef is not product activation. |
| EVD-012 | EvidenceRef is not Graphify adoption. |
| EVD-013 | Graphify evidence is supporting generated evidence only, not authority. |
| EVD-014 | Generated outputs are not source by default. |
| EVD-015 | Local-only evidence blocks publication and provider-bound transmission by default. |
| EVD-016 | Secrets and credentials are never evidence content in EvidenceRef. |
| EVD-017 | Product source remains blocked until GT-09. |
| EVD-018 | Validation evaluates; governance decides. |
| EVD-019 | Cognitive Semantic System substrate remains deferred. |
| EVD-020 | AGENT PLATFORM remains pre-active at AL-1. |

## 22. Future Validation Targets

These are future validation targets only. P2.2 does not execute validation.

| Future validation target | Purpose |
| --- | --- |
| EvidenceRef required fields completeness | Check all required fields exist. |
| evidence kind vocabulary conformance | Check evidence_kind terms. |
| evidence status vocabulary conformance | Check evidence_status terms. |
| source_ref relationship preservation | Check SourceRef relationship values and blocker propagation. |
| validation_ref relationship preservation | Check ValidationRef relationship values and not-executed posture. |
| security_ref relationship preservation | Check SecurityRef relationship values and blockers. |
| graphify_ref relationship preservation | Check GraphifyRef support-only boundaries. |
| product_ref relationship preservation | Check ProductRef readiness-only boundaries. |
| generated_output_posture propagation | Check generated-output posture travels downstream. |
| local_only_posture propagation | Check local-only posture travels downstream. |
| evidence limitations propagation | Check limitations remain attached. |
| retention posture propagation | Check retention posture remains attached. |
| review requirement propagation | Check review_required values remain attached. |
| no-secret/no-credential EvidenceRef invariant | Check EvidenceRef excludes secret and credential content without scanning values. |
| no-raw-source EvidenceRef invariant | Check EvidenceRef excludes raw source content. |
| no-provider-output EvidenceRef invariant | Check EvidenceRef excludes provider output payloads. |
| Graphify support-only invariant | Check Graphify evidence remains supporting generated evidence only. |
| evidence-not-authority invariant | Check evidence is not treated as authority. |
| P2.1 vocabulary alignment check | Future check after P2.1 exists. |
| cross-lane alias/deprecated-term detection | Check aliases and deprecated terms do not become canonical. |

## 23. Future Hardening Candidates

These are future candidates only and are not started by P2.2.

| Candidate ticket | Purpose | P2.2 status |
| --- | --- | --- |
| EVD-HARD-01 - EvidenceRef Schema Alignment | Align EvidenceRef schemas across lane records. | Not started. |
| EVD-HARD-02 - EvidenceRef Relationship Vocabulary Alignment | Align SourceRef, ValidationRef, SecurityRef, GraphifyRef, and ProductRef relationships. | Not started. |
| EVD-HARD-03 - Evidence Limitation Propagation Contract | Harden limitation propagation across lanes. | Not started. |
| EVD-HARD-04 - Evidence Retention / Review Requirement Contract | Harden retention and review requirements. | Not started. |
| EVD-HARD-05 - Graphify Evidence Boundary Contract | Refine Graphify generated evidence boundaries. | Not started. |
| EVD-HARD-06 - Product-Bound Evidence Gate Contract | Refine product-bound evidence gate posture. | Not started. |
| EVD-HARD-07 - EvidenceRef Validation Readiness Targets | Prepare future validation target specifications. | Not started. |

## 24. Created / Not Created Register

| Artifact or action | P2.2 status |
| --- | --- |
| Cross-lane evidence reference contract document created | Created. |
| `0_architecture/governance/agent_platform_cross_lane_evidence_reference_contract.md` | Created. |
| Runtime code modified | No runtime code modified. |
| Context runtime code modified | No context runtime code modified. |
| Provider adapter runtime code modified | No provider adapter runtime code modified. |
| Tool execution code modified | No tool execution code modified. |
| Agent runtime code modified | No agent runtime code modified. |
| Cognitive Semantic System runtime code modified | No Cognitive Semantic System runtime code modified. |
| Validation registry code modified | No validation registry code modified. |
| Security implementation code modified | No security implementation code modified. |
| Validation command executed | No validation command executed. |
| Tests executed | No tests executed. |
| Provider/auth/API/MCP configured | No provider/auth/API/MCP configured. |
| Provider/API/network/MCP call executed | No provider/API/network/MCP call executed. |
| Tool execution approved | No tool execution approved. |
| Agent execution approved | No agent execution approved. |
| Source loading approved | No source loading approved. |
| Product source inspected | No product source inspected. |
| External source inspected | No external source inspected. |
| Secrets inspected | No secrets inspected. |
| Credentials inspected | No credentials inspected. |
| `.env` inspected | No `.env` inspected. |
| Generated output tracking approved | No generated output tracking approved. |
| Source tracking expansion approved | No source tracking expansion approved. |
| Graphify rerun | No Graphify rerun. |
| Graphify adoption | No Graphify adoption. |
| `.graphifyignore` modified | No `.graphifyignore` modified. |
| `.gitignore` modified | No `.gitignore` modified. |
| Generated outputs modified/tracked | No generated outputs modified or tracked. |
| Cognitive Semantic System substrate selected | No Cognitive Semantic System substrate selected. |
| P2.1 file created | No P2.1 file created. |
| P2.3 file created | No P2.3 file created. |
| P3.1 started | No P3.1 started. |
| P3.2 started | No P3.2 started. |
| Git staging/commit/push/force-add/publication performed | No Git staging, commit, push, force-add, or publication performed. |

## 25. Recommended Next Tickets

After P2.2:

| Ticket | Recommendation |
| --- | --- |
| P2.1 - Shared Metadata Vocabulary Alignment | Complete if not already completed. |
| P2.3 - Audit / Retention / Rollback Baseline | Follow after vocabulary/evidence posture is reviewed. |
| P3.1 - Validation Execution Readiness | Start only after P2.1 through P2.3 are reviewed together. |
| P3.2 - Security Enforcement Readiness | Start only after P2.1 through P2.3 are reviewed together. |

Recommended actual: P2.3 - Audit / Retention / Rollback Baseline, if P2.1 is already running or complete. Otherwise: P2.1 - Shared Metadata Vocabulary Alignment.

Do not start P2.3. Do not start P3.1. Do not start P3.2.

## 26. Final Verdict

| Question | Answer |
| --- | --- |
| What did P2.2 create? | The canonical Cross-Lane Evidence Reference Contract document. |
| What cross-lane evidence contract was defined? | A metadata-only EvidenceRef contract connecting SourceRef, ValidationRef, SecurityRef, GraphifyRef, ProductRef, generated-output posture, local-only posture, limitations, retention, and review requirements across P1 lanes. |
| What canonical EvidenceRef fields are required? | `evidence_ref_id`, `evidence_kind`, `evidence_label`, `evidence_scope`, `evidence_owner`, `evidence_status`, `evidence_source_ref`, `source_ref_relationship`, `validation_refs`, `validation_ref_relationship`, `security_refs`, `security_ref_relationship`, `graphify_refs`, `graphify_ref_relationship`, `product_refs`, `product_ref_relationship`, `generated_output_posture`, `local_only_posture`, `sensitivity`, `source_classification`, `authority_posture`, `decision_posture`, `retention_posture`, `review_required`, `evidence_limitations`, `blockers`, `aliases`, `deprecated_terms`, and `pending_alignment_refs`. |
| What evidence kind vocabulary was defined? | Governance document, implementation record, validation record, security record, context metadata, provider metadata, tool metadata, agent metadata, semantic record, Graphify summary, generated output summary, generated raw output, local-only metadata, local-only source, product readiness metadata, product source, external reference, incident record, audit record, and unknown evidence. |
| What evidence status vocabulary was defined? | Draft, proposed, referenced, reviewed metadata, accepted metadata evidence, generated unreviewed, generated curated, local-only blocked, product blocked, external blocked, security blocked, validation blocked, deprecated, superseded, rejected for scope, and unknown status. |
| What SourceRef relationships were defined? | Source metadata, source path only, curated summary, generated summary, raw generated output blocked, local-only metadata, local-only source blocked, product metadata, product source blocked, external metadata, external source blocked, secret or credential ref blocked, and unknown source relationship. |
| What ValidationRef relationships were defined? | Validation design, validation requirement, validation result metadata, not-executed validation, future validation target, blocked validation, failed validation, and unknown validation posture. |
| What SecurityRef relationships were defined? | Security policy, security requirement, security review metadata, security blocker, incident requirement, retention requirement, publication blocker, and unknown security posture. |
| What GraphifyRef relationships were defined? | Curated Graphify summary, Graphify repo map summary, Graphify generated evidence, raw Graphify output blocked, Graphify label metadata, Graphify drift observation, Graphify limitations, and unknown Graphify relationship. |
| What ProductRef relationships were defined? | Product vision metadata, product readiness metadata, product gate requirement, product source blocked, product activation blocker, product rollback requirement, product incident requirement, and unknown product relationship. |
| What generated output evidence posture was defined? | `not_generated`, `generated_metadata_only`, `generated_summary_unreviewed`, `generated_summary_curated`, `generated_raw_output_blocked`, `generated_sensitive_local_only`, `generated_output_tracking_not_approved`, `generated_output_tracking_required_future`, `generated_output_quarantine_required`, and `unknown_generated_output_posture`. |
| What local-only evidence posture was defined? | `not_local_only`, `local_only_metadata`, `local_only_summary`, `local_only_source_blocked`, `local_only_generated_output_blocked`, `local_only_secret_or_credential_blocked`, `local_only_product_blocked`, `local_only_publication_blocked`, and `unknown_local_only_posture`. |
| What retention posture was defined? | Metadata-only, curated-summary-only, until-superseded, with redaction, local-only, generated-sensitive, quarantine required, deletion review required, publication blocked, tracking not approved, and unknown retention posture. |
| What review requirements were defined? | Metadata-reference, governance, validation, security, source tracking, generated output, product, provider/auth, tool execution, agent execution, retention, incident, P2.1 alignment, and unknown review requirements. |
| What lanes were mapped? | Context, Provider/Adapter, Tool, Agent, Cognitive Semantic System, Validation, Security, Graphify evidence, Siamese product-readiness, and Audit/retention/rollback lanes. |
| What drift or pending alignment was recorded? | P2.1 is absent, so EvidenceRef vocabulary, relationship terms, status terms, aliases, and deprecated terms are marked `pending_P2.1_alignment`. |
| Did P2.2 run validation? | No. |
| Did P2.2 activate runtime? | No. |
| Did P2.2 approve provider/auth/API/MCP? | No. |
| Did P2.2 approve tool execution? | No. |
| Did P2.2 approve agent execution? | No. |
| Did P2.2 inspect product source? | No. |
| Did P2.2 approve source loading? | No. |
| Did P2.2 approve generated output tracking? | No. |
| Did P2.2 approve source tracking expansion? | No. |
| Did P2.2 rerun or adopt Graphify? | No. |
| Was Cognitive Semantic System substrate selected? | No. Cognitive Semantic System substrate remains deferred. |
| What is the next ticket? | P2.1 - Shared Metadata Vocabulary Alignment, because P2.1 is absent. If P2.1 is already running or complete elsewhere, P2.3 - Audit / Retention / Rollback Baseline is the next candidate after explicit instruction. |

Stop rule: P2.2 stops here. Do not start P2.1. Do not start P2.3. Do not start P3.1. Do not start P3.2. Do not implement code. Do not run validation. Do not run tests. Do not inspect secrets. Do not inspect credentials. Do not configure provider/auth. Do not call provider/API/network/MCP. Do not execute tools. Do not activate agents. Do not inspect product source. Do not load source. Do not approve generated output tracking. Do not approve source tracking expansion. Do not rerun Graphify. Do not adopt Graphify as authority. Do not modify generated outputs. Do not select Cognitive Semantic System substrate. Do not stage, commit, push, force-add, or publish.
