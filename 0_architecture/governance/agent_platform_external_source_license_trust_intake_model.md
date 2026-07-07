# External Source License / Trust Intake Model

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | External Source License / Trust Intake Model |
| Ticket | P9.2 |
| Status | Accepted governance-only license and trust intake model |
| Date | 2026-07-07 |
| Scope | Documentation-only model for external source license class, provenance, dependency trust, supply-chain risk, and adoption eligibility intake. |
| Authority | Intake model only, not license approval, not legal approval, not dependency approval, not source inspection approval, not external source content inspection, not LICENSE file inspection, not dependency manifest inspection, not lockfile inspection, not package metadata inspection, not source copying, not external adoption, not external execution, not package installation, not package-manager execution, not vulnerability scanning, not SBOM generation, not runtime activation, not adapter/wrapper implementation, not vendor/fork/submodule creation, not provider/auth/API/MCP activation, not credential use, not network calls, not validation execution, not tests, not builds, not scripts, not persistence, not vector DB, not graph DB, not telemetry, not publication, not Git mutation, and not Cognitive Semantic System substrate selection. |
| Required input | `0_architecture/governance/agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md` |
| Optional context | P8.1 external inventory, P8.5 security/activation gate model, S-03 local-only/secrets policy, S-04 tool/shell/network/MCP execution policy, P8.7 GBrain/GStack compatibility boundary if present. |
| Output | External source license/trust intake model. |
| Target file | `0_architecture/governance/agent_platform_external_source_license_trust_intake_model.md` |
| Result markers | `external_source_license_trust_intake_model_ready`; `mit_license_intake_policy_defined`; `dependency_trust_review_model_defined`; `supply_chain_risk_model_defined`; `adoption_not_rebuild_policy_supported`; `no_external_source_adoption`; `no_external_execution`; `no_dependency_approval_granted` |

## 2. Purpose

P9.2 defines how AGENT PLATFORM records license, trust, dependency, provenance, and supply-chain posture for external source candidates before any adoption decision.

P9.2 supports the P9.0 adopt-not-rebuild charter by making reuse safer to evaluate. It does not approve reuse by itself. It defines the record shapes and default verdicts needed before later tickets decide inspection scope, execution scope, adoption mode, rollback, incidents, and closure.

P9.2 is intentionally non-invasive. It does not open external source files. It does not read `LICENSE` files. It does not read dependency manifests, lockfiles, package metadata, source files, examples, instructions, scripts, or generated outputs. It does not execute anything under `4_external/sources`.

## 3. Current Posture

P9.0 established that validated external MIT or otherwise license-compatible tools may be evaluated for adoption, adaptation, wrapping, forking, vendoring, or dependency use before rebuilding from scratch.

P9.2 creates the intake model for that evaluation, but every candidate remains blocked until future gates supply exact authority.

| Area | P9.2 posture | Blocked interpretation |
| --- | --- | --- |
| P9.0 charter | Present at corrected path and accepted as prerequisite. | P9.2 can override P9.0 boundaries. |
| License posture | License classes and obligations can be modeled. | License approval or legal approval. |
| MIT posture | MIT is a favorable permissive candidate class when verified later. | Automatic trust, adoption, execution, dependency approval, provider/API/MCP approval, or product compatibility. |
| Provenance posture | Source provenance record shape can be defined. | Upstream identity verified by content inspection. |
| Dependency posture | Dependency trust review model can be defined. | Dependency manifest/lockfile/package approval. |
| Supply-chain posture | Risk model can be defined. | Vulnerability scanning, SBOM generation, package install, or audit execution. |
| External root | `4_external/sources` remains canonical external root. | Listing, traversing, or reading external source contents. |
| GStack | `4_external/sources/gstack-main` is path/class metadata only. | GStack adoption, execution, import, configuration, dependency approval, or source inspection. |
| Runtime | No execution or runtime activation. | Controlled execution or autonomous integration. |
| Git | Advisory exact-path commands only. | Git mutation or `git add .`. |

## 4. Inputs Reviewed

Inputs were consumed as governance and safe metadata only. No external source contents, LICENSE files, dependency manifests, lockfiles, package metadata, product/Siamese source, raw generated outputs, secrets, credentials, provider configs, token stores, browser auth, local credential stores, API keys, scripts, tests, builds, package managers, agents, tools, or runtimes were inspected or executed.

| Input | Review mode | P9.2 use | Limitation |
| --- | --- | --- | --- |
| `agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md` | Required governance document review | Confirms P9.0 charter, adopt-not-rebuild default, future P9 gate queue, and no-inspection/no-execution boundary. | No P9.0 modification. |
| Legacy P9.0 path without `p9_` prefix | Path absence metadata | Confirms corrected P9.0 path is canonical for this ticket. | Not treated as blocker. |
| P8.1 external source inventory | Governance metadata review | Supplies candidate inventory vocabulary and path/class metadata posture. | Earlier inventory used legacy path assumptions; P9.2 carries canonical root from P9.0. |
| P8.5 security/activation gate model | Governance metadata review | Supplies activation levels, source inspection gate, human approval, and execution blockers. | No gate enforcement implemented. |
| S-03 local-only/secrets policy | Security policy review | Preserves external raw source local-only, no secret/credential inspection, and no dependency adoption. | No secret handling performed. |
| S-04 tool/shell/network/MCP execution policy | Security policy review | Preserves no package manager, no execution, no network, no provider/API/MCP, and no external execution defaults. | No execution performed. |
| P8 readiness closure checked path | Path absence metadata from P9.2 preparation | Records missing direct closure artifact as limitation. | Not a hard blocker because P9.0 is the required P9.2 prerequisite. |
| P9.1, P9.3, P9.4, P9.5, P9.6 peers | Peer status metadata only | Records pending peer alignments without consuming peer contents. | P9.2 does not create, inspect, or replace peer tickets. |
| `4_external/sources` and candidate paths | Path metadata only from P9.2 preparation | Carries canonical root and candidate presence/absence without inspection. | No listing, traversal, or content inspection. |

## 5. P9.2 Authority Boundary

P9.2 may define records, vocabularies, gate preconditions, pending alignments, and blocked defaults.

P9.2 may not grant any operational permission.

| Action | P9.2 posture |
| --- | --- |
| Define license/trust intake records | Allowed. |
| Define MIT intake policy | Allowed as policy only. |
| Define dependency trust review model | Allowed as model only. |
| Define supply-chain risk model | Allowed as model only. |
| Record candidate path/class metadata | Allowed when path metadata is already in scope. |
| Inspect external source contents | Blocked. |
| Inspect `LICENSE` files | Blocked. |
| Inspect dependency manifests, lockfiles, package metadata, or package scripts | Blocked. |
| Install, audit, scan, build, test, run, or execute dependencies | Blocked. |
| Approve dependency use | Blocked. |
| Approve license compatibility | Blocked. |
| Adopt, vendor, fork, wrap, copy, submodule, or import external code | Blocked. |
| Activate runtime, provider/API/MCP, credentials, network, or telemetry | Blocked. |
| Mutate Git | Blocked. |

## 6. Intake Method And Non-Inspection Rule

The P9.2 intake method is model-first and evidence-later.

Allowed P9.2 method:

| Method | Use | Boundary |
| --- | --- | --- |
| Governance document review | Define policy and object model. | Governance metadata only. |
| Safe path metadata | Carry exact path presence/absence already checked for the active ticket. | No listing, traversal, or file content. |
| Candidate class metadata | Record candidate family, path, and future gate route. | Candidate class is not trust or adoption. |
| License class modeling | Define how future evidence will be classified. | No license evidence is verified by P9.2. |
| Dependency trust modeling | Define future dependency review fields and blockers. | No manifest, lockfile, package, registry, or audit content is inspected. |
| Supply-chain risk modeling | Define future provenance and risk fields. | No SBOM, vulnerability scan, network call, package install, or binary execution. |

Non-inspection invariant:

```text
P9.2 can define what must be reviewed later, but P9.2 does not perform that review.
```

## 7. ExternalSourceLicenseTrustIntakeModel

`ExternalSourceLicenseTrustIntakeModel` is the root governance object for future external source intake.

It aggregates license, provenance, trust, dependency, supply-chain, adoption eligibility, human approval, rollback, and incident requirements. It is metadata only.

| Field | Meaning |
| --- | --- |
| `model_id` | Stable identifier for the intake model instance. |
| `candidate_id` | External candidate identifier, such as `gstack`, `gbrain`, `graphify`, `hermes`, `ecc_main`, or `opencode`. |
| `candidate_name` | Human-readable candidate name. |
| `source_root` | Canonical root, default `4_external/sources`. |
| `observed_path_metadata` | Path/class metadata only. No tree listing or file content. |
| `provenance_record` | `SourceProvenanceRecord`. |
| `license_record` | `ExternalSourceLicenseRecord`. |
| `license_obligations` | `LicenseObligationRecord` entries. |
| `trust_record` | `ExternalSourceTrustRecord`. |
| `dependency_records` | `DependencyTrustRecord` entries or `not_reviewed`. |
| `supply_chain_risk_records` | `SupplyChainRiskRecord` entries. |
| `adoption_eligibility` | `ExternalAdoptionEligibility`. |
| `intake_verdict` | `IntakeVerdict`. |
| `adoption_mode_candidates` | `AdoptionModeCandidate` values for P9.5 consideration only. |
| `human_approval_requirements` | `HumanApprovalRequirement` entries. |
| `rollback_incident_requirements` | `RollbackIncidentRequirement` entries. |
| `pending_alignment_refs` | P9 peer and closure alignments. |
| `blocked_actions` | Actions not authorized by the intake. |
| `evidence_refs` | Governance refs only until P9.3 or later authorizes source inspection. |
| `limitations` | Known missing documents, unknowns, and deferred reviews. |

Canonical skeleton:

```yaml
ExternalSourceLicenseTrustIntakeModel:
  phase: P9_external_integration_foundation
  ticket: P9.2
  authority: governance_model_only
  source_root: 4_external/sources
  legacy_source_root: external/sources
  source_inspection_authorized_by_P9_2: false
  license_approval_granted_by_P9_2: false
  dependency_approval_granted_by_P9_2: false
  external_execution_authorized_by_P9_2: false
  external_adoption_authorized_by_P9_2: false
  adoption_not_rebuild_policy_supported: true
  next_required_gates:
    - P9.1_source_root_normalization
    - P9.3_source_inspection_permission_gate
    - P9.4_external_tool_execution_gate
    - P9.5_vendor_fork_wrapper_submodule_decision
    - P9.6_external_integration_rollback_incident
    - P9.R_external_integration_foundation_closure
```

## 8. SourceProvenanceRecord

`SourceProvenanceRecord` records where an external source candidate is believed to come from and how that belief must be verified later.

P9.2 does not verify provenance by reading source contents, Git metadata inside external sources, package metadata, lockfiles, or upstream network resources.

| Field | Meaning | P9.2 default |
| --- | --- | --- |
| `source_id` | Stable source identifier. | Candidate id or `unknown`. |
| `source_name` | Human-readable name. | Candidate name. |
| `canonical_local_root` | Local root containing raw snapshots. | `4_external/sources`. |
| `legacy_local_root` | Legacy drift path reference. | `external/sources`, non-canonical. |
| `observed_local_path` | Exact path metadata if known. | Path/class metadata only. |
| `path_status` | Present, absent, ambiguous, or unknown path metadata. | From allowed path checks only. |
| `upstream_origin` | Upstream URL, organization, package, or repository identity. | `not_verified_by_P9_2`. |
| `snapshot_origin` | How local snapshot arrived. | `not_verified_by_P9_2`. |
| `version_or_commit` | Version, tag, commit, release, or snapshot label. | `not_verified_by_P9_2`. |
| `integrity_evidence` | Hash, signature, checksum, or attestation evidence. | `not_reviewed`. |
| `maintainer_identity` | Maintainer or owner metadata. | `not_verified_by_P9_2`. |
| `instruction_posture` | Whether source-local instructions are active. | `inactive_evidence_only`. |
| `provenance_verdict` | Provenance confidence. | `unknown_pending_review`. |

Provenance rule:

```text
Path presence is not provenance verification.
```

## 9. ExternalSourceLicenseRecord

`ExternalSourceLicenseRecord` records license claim posture for an external source candidate.

P9.2 does not read or verify license files. Any MIT, permissive, copyleft, proprietary, or unknown classification at P9.2 is a candidate class until future review.

| Field | Meaning | P9.2 default |
| --- | --- | --- |
| `license_record_id` | Stable record id. | Required in future intake. |
| `candidate_id` | External candidate id. | Required in future intake. |
| `claimed_license` | License claimed by prior governance, user statement, package metadata, or upstream docs. | `not_verified_by_P9_2`. |
| `license_class` | `LicenseClass` value. | `unknown_or_unverified_candidate`. |
| `license_evidence_source` | Where the license evidence came from. | Governance/user metadata only unless future gate allows source inspection. |
| `license_file_path` | Local license file path if later authorized. | `not_inspected_by_P9_2`. |
| `license_text_review_status` | Whether license text was reviewed. | `not_reviewed`. |
| `copyright_notice_status` | Copyright notice posture. | `not_reviewed`. |
| `notice_preservation_required` | Whether notices must be preserved. | `assume_required_until_reviewed`. |
| `modification_notice_required` | Whether modifications need notice. | `unknown_pending_review`. |
| `attribution_required` | Whether attribution is required. | `assume_required_until_reviewed`. |
| `patent_terms_present` | Whether patent grant/termination terms exist. | `unknown_pending_review`. |
| `license_compatibility_decision` | `LicenseCompatibilityDecision` value. | `not_evaluated`. |
| `legal_review_required` | Whether legal/human review is required. | `true_before_adoption`. |
| `approval_status` | Whether license use is approved. | `not_approved_by_P9_2`. |

License rule:

```text
License metadata supports review; it does not grant use, adoption, execution, copying, vendoring, or dependency approval.
```

## 10. LicenseClass

`LicenseClass` is the license classification vocabulary for intake records.

Values are review classes, not approvals.

| LicenseClass | Meaning | P9.2 posture |
| --- | --- | --- |
| `mit_candidate` | Candidate appears or is claimed to be MIT. | Favorable permissive candidate only; verification required. |
| `permissive_candidate` | Candidate appears to use a permissive license class. | Favorable candidate only; obligations still required. |
| `apache_2_0_candidate` | Candidate appears to use Apache-2.0 style terms. | Requires patent/notice review before use. |
| `bsd_candidate` | Candidate appears to use BSD-style terms. | Requires notice/variant review before use. |
| `isc_candidate` | Candidate appears to use ISC-style terms. | Requires notice review before use. |
| `weak_copyleft_candidate` | Candidate appears to use LGPL/MPL/EPL-like terms. | Legal and architecture review required. |
| `strong_copyleft_candidate` | Candidate appears to use GPL/AGPL-like terms. | Blocked until legal/governance review. |
| `source_available_candidate` | Candidate source is available but rights may be restricted. | Blocked until legal/governance review. |
| `commercial_restricted_candidate` | Candidate has commercial or field-of-use restrictions. | Blocked until legal/governance review. |
| `proprietary_candidate` | Candidate is proprietary or closed-license. | Blocked unless explicit legal/governance approval exists. |
| `multi_license_candidate` | Candidate offers multiple license paths. | Requires exact license choice and obligations review. |
| `license_exception_candidate` | Candidate has exceptions or special terms. | Requires exact exception review. |
| `unlicensed_or_no_license_found` | No license is identified. | Blocked. |
| `unknown_or_unverified_candidate` | License is unknown or not verified. | Blocked by default. |

MIT intake policy:

```text
MIT is favorable for future review because it is generally permissive, but P9.2 does not verify MIT status or approve use. MIT candidates still require provenance review, notice preservation, dependency trust review, supply-chain risk review, source inspection authorization, adoption-mode decision, rollback/incident planning, and human approval before adoption.
```

## 11. LicenseCompatibilityDecision

`LicenseCompatibilityDecision` records the current compatibility posture for a candidate.

No value in this vocabulary grants source use by itself.

| LicenseCompatibilityDecision | Meaning |
| --- | --- |
| `not_evaluated` | No compatibility review has been performed. |
| `unknown_blocked` | License posture is unknown and blocks adoption. |
| `deferred_pending_license_evidence` | License evidence must be inspected later. |
| `deferred_pending_source_inspection` | Source or license file inspection requires P9.3 or later. |
| `deferred_pending_dependency_review` | Transitive dependency/license posture is unknown. |
| `deferred_pending_legal_review` | Human/legal review is required. |
| `compatible_candidate` | Appears compatible after future review, but not approved by this vocabulary alone. |
| `compatible_with_obligations_candidate` | Appears compatible if obligations are satisfied later. |
| `incompatible_candidate` | Appears incompatible; adoption should be rejected unless governance changes. |
| `rejected` | Reviewed and rejected by a future authorized gate. |

P9.2 default for all external candidates is `not_evaluated` or `deferred_pending_license_evidence`.

## 12. LicenseObligationRecord

`LicenseObligationRecord` records obligations that may need to be satisfied if a candidate is adopted later.

P9.2 records obligation categories only. It does not inspect license text and does not decide exact obligations.

| Field | Meaning | P9.2 default |
| --- | --- | --- |
| `obligation_id` | Stable obligation record id. | Future record field. |
| `candidate_id` | Candidate id. | Future record field. |
| `license_class` | Related `LicenseClass`. | `unknown_or_unverified_candidate`. |
| `obligation_type` | Notice, attribution, source offer, patent, modification, distribution, or other obligation. | `unknown_pending_review`. |
| `required_action` | Action required before use, distribution, vendoring, fork, or modification. | `not_defined_by_P9_2`. |
| `applies_to_mode` | Adoption mode where obligation applies. | Future P9.5 decision. |
| `evidence_needed` | License text, notice file, package metadata, or legal review needed. | Future P9.3/P9.5/P9.R. |
| `satisfaction_status` | Whether obligation has been satisfied. | `not_satisfied_by_P9_2`. |
| `retention_requirement` | What notice/evidence must be retained. | `retain_governance_metadata_only_now`. |

Obligation categories to evaluate later:

| Obligation category | Future review question |
| --- | --- |
| `notice_preservation` | Must original license or copyright notices be preserved? |
| `attribution` | Must attribution appear in docs, UI, source, or distribution? |
| `modification_notice` | Must modifications be marked? |
| `source_offer` | Must source or modifications be offered? |
| `patent_terms` | Are patent grants, retaliation, or patent notices involved? |
| `distribution_terms` | Do obligations change when redistributed, vendored, or packaged? |
| `network_use_terms` | Do obligations change when used over a network? |
| `trademark_name_use` | Are names/logos constrained? |

## 13. ExternalSourceTrustRecord

`ExternalSourceTrustRecord` records trust posture for an external source candidate.

Trust is not binary. Trust must be decomposed into signals and risks. P9.2 does not conclude that any candidate is trusted.

| Field | Meaning | P9.2 default |
| --- | --- | --- |
| `trust_record_id` | Stable trust record id. | Future record field. |
| `candidate_id` | External candidate id. | Future record field. |
| `trust_signals` | `TrustSignal` values observed by future review. | `not_reviewed`. |
| `trust_risks` | `TrustRisk` values observed by future review. | `unknown_risk_present`. |
| `maintainer_posture` | Maintainer identity/activity posture. | `not_verified_by_P9_2`. |
| `release_posture` | Release/tag/package posture. | `not_verified_by_P9_2`. |
| `security_policy_posture` | Security policy and disclosure posture. | `not_reviewed`. |
| `issue_history_posture` | Public issue/advisory posture. | `not_reviewed`. |
| `instruction_risk_posture` | Source-local instruction and automation risk. | `unreviewed_external_instructions_inactive`. |
| `trust_level` | Candidate trust rating. | `untrusted_until_reviewed`. |
| `trust_verdict` | Future trust decision. | `deferred_pending_review`. |

Trust invariant:

```text
Path presence, MIT candidacy, popularity, or useful functionality is not sufficient trust.
```

## 14. TrustSignal

`TrustSignal` values are positive signals future reviewers may record.

No signal grants adoption or execution by itself.

| TrustSignal | Meaning |
| --- | --- |
| `known_upstream_origin` | Upstream repository, package, or publisher is known and verified. |
| `stable_maintainer_identity` | Maintainers or organization are stable and identifiable. |
| `active_maintenance` | Project shows relevant maintenance activity. |
| `clear_license_evidence` | License evidence is available and reviewed. |
| `minimal_dependency_surface` | Dependency footprint is small and reviewable. |
| `reviewed_dependency_lock` | Lockfile or dependency snapshot is reviewed. |
| `no_package_lifecycle_scripts` | No install/build lifecycle scripts or they are reviewed and blocked/controlled. |
| `documented_security_policy` | Security policy or disclosure process exists. |
| `signed_or_attested_release` | Release has signature, checksum, attestation, or similar integrity evidence. |
| `reproducible_release_metadata` | Release/version metadata can be reproduced or verified. |
| `compatible_architecture_candidate` | Candidate appears aligned with AGENT PLATFORM architecture after governance review. |
| `manual_review_available` | Human review path is clear and bounded. |
| `local_path_metadata_known` | Local path metadata is known. This is weak and never sufficient alone. |

## 15. TrustRisk

`TrustRisk` values are risk signals future reviewers must consider.

Unknown status should be treated as risk until resolved.

| TrustRisk | Meaning |
| --- | --- |
| `unknown_provenance` | Origin, version, snapshot, or maintainer identity is unknown. |
| `missing_or_unclear_license` | License evidence is missing, unclear, or conflicting. |
| `license_obligation_mismatch` | License obligations may conflict with intended adoption mode. |
| `dependency_sprawl` | Large or unclear transitive dependency graph. |
| `native_binary_or_postinstall_risk` | Native binaries, installers, postinstall hooks, or lifecycle scripts may exist. |
| `network_or_auth_behavior_risk` | Candidate may call network, providers, APIs, registries, or auth surfaces. |
| `runtime_side_effect_risk` | Candidate may modify files, spawn processes, persist state, or alter environment. |
| `secret_or_credential_surface_risk` | Candidate may read, generate, store, or request secrets/credentials. |
| `instruction_injection_risk` | Source-local instructions, prompts, or agent files may conflict with AGENT PLATFORM policy. |
| `generated_output_contamination_risk` | Candidate may produce generated output that could be mistaken for authority. |
| `product_scope_contamination_risk` | Candidate may pressure product/Siamese source inspection or product activation. |
| `abandoned_or_unmaintained_risk` | Maintenance posture may be stale or unknown. |
| `unreviewed_release_artifact_risk` | Release artifacts, packages, archives, or binaries are not reviewed. |
| `supply_chain_compromise_risk` | Upstream, registry, package, or maintainer chain may be compromised or unverifiable. |
| `unknown_risk_present` | Risk is unknown and must block approval until reviewed. |

## 16. DependencyTrustRecord

`DependencyTrustRecord` defines future dependency review requirements.

P9.2 does not inspect dependency manifests, lockfiles, package metadata, package scripts, or dependency folders. It does not run package managers, audits, scanners, tests, builds, or SBOM tools.

| Field | Meaning | P9.2 default |
| --- | --- | --- |
| `dependency_record_id` | Stable dependency record id. | Future record field. |
| `candidate_id` | External candidate id. | Future record field. |
| `ecosystem` | Package ecosystem, such as npm, Python, Go, Rust, Docker, or unknown. | `not_reviewed`. |
| `manifest_paths` | Manifest paths if later authorized. | `not_inspected_by_P9_2`. |
| `lockfile_paths` | Lockfile paths if later authorized. | `not_inspected_by_P9_2`. |
| `direct_dependencies` | Direct dependency list. | `not_reviewed`. |
| `transitive_dependencies` | Transitive dependency list. | `not_reviewed`. |
| `dependency_license_posture` | License posture of dependencies. | `unknown_pending_review`. |
| `vulnerability_posture` | Vulnerability/advisory posture. | `not_scanned`. |
| `package_script_posture` | Install/build/test lifecycle script posture. | `not_reviewed`. |
| `native_module_posture` | Native/compiled module posture. | `not_reviewed`. |
| `registry_network_posture` | Registry/network exposure posture. | `blocked_not_reviewed`. |
| `dependency_approval_status` | Whether dependencies are approved. | `not_approved_by_P9_2`. |

Dependency trust review model:

```text
Dependency approval requires later exact-scope manifest/lockfile review, transitive license review, package script review, registry/network/auth review, vulnerability posture review, rollback/incident planning, and human approval. P9.2 grants none of these approvals.
```

## 17. SupplyChainRiskRecord

`SupplyChainRiskRecord` defines how supply-chain risk will be recorded before any candidate can be adopted.

P9.2 does not fetch upstream data, call registries, inspect package archives, inspect release artifacts, generate SBOMs, run scanners, or execute source-provided tools.

| Field | Meaning | P9.2 default |
| --- | --- | --- |
| `risk_record_id` | Stable risk record id. | Future record field. |
| `candidate_id` | External candidate id. | Future record field. |
| `source_channel` | Local snapshot, Git repo, package registry, release archive, submodule, or unknown. | `local_path_metadata_only_or_unknown`. |
| `integrity_status` | Signature, checksum, attestation, or reproducibility posture. | `not_verified_by_P9_2`. |
| `maintainer_risk` | Maintainer account/org risk. | `unknown_pending_review`. |
| `release_risk` | Release artifact and versioning risk. | `unknown_pending_review`. |
| `dependency_risk` | Direct and transitive dependency risk. | `unknown_pending_review`. |
| `script_risk` | Package scripts, setup scripts, install hooks, and examples risk. | `unknown_pending_review`. |
| `binary_risk` | Native binaries, compiled artifacts, or installers risk. | `unknown_pending_review`. |
| `network_risk` | Network, provider, registry, API, or telemetry behavior risk. | `unknown_pending_review`. |
| `credential_risk` | Secrets, tokens, auth configs, browser/session, or credential handling risk. | `unknown_pending_review`. |
| `instruction_risk` | README/agent/prompt/source-local instruction risk. | `external_instructions_inactive`. |
| `risk_rating` | Overall supply-chain risk rating. | `unknown_blocked`. |
| `required_mitigations` | Required mitigations before adoption. | Future P9.3-P9.6/P9.R. |

Supply-chain risk model:

```text
Unknown supply-chain status blocks adoption. It does not block keeping safe path/class metadata or planning future review gates.
```

## 18. IntakeVerdict

`IntakeVerdict` summarizes the result of a P9.2 intake record.

The verdict is a governance classification, not operational permission.

| IntakeVerdict | Meaning |
| --- | --- |
| `record_only` | Candidate can remain recorded as metadata only. |
| `needs_license_evidence` | Future authorized license evidence review is required. |
| `needs_provenance_evidence` | Future provenance review is required. |
| `needs_dependency_review` | Future dependency manifest/lockfile/package review is required. |
| `needs_supply_chain_review` | Future supply-chain review is required. |
| `needs_source_inspection_gate` | P9.3 or later must authorize exact source inspection. |
| `needs_execution_gate` | P9.4 or later must authorize exact execution if execution is ever needed. |
| `needs_adoption_mode_gate` | P9.5 must decide vendor/fork/wrapper/submodule/reject/defer. |
| `needs_rollback_incident_gate` | P9.6 must define rollback and incident handling before risky adoption or execution. |
| `blocked` | Candidate is blocked from adoption/use at current posture. |
| `defer_to_P9_R` | Reconciliation is required before P10+ work. |

P9.2 default verdict for known external candidates:

```yaml
IntakeVerdict:
  default: record_only
  adoption: blocked
  execution: blocked
  dependency_approval: blocked
  license_approval: not_granted
  required_next:
    - needs_license_evidence
    - needs_provenance_evidence
    - needs_dependency_review
    - needs_supply_chain_review
    - needs_source_inspection_gate
    - needs_adoption_mode_gate
    - needs_rollback_incident_gate
```

## 19. ExternalAdoptionEligibility

`ExternalAdoptionEligibility` records whether a candidate may move toward later adoption review.

Eligibility is permission to request a future gate, not permission to adopt.

| ExternalAdoptionEligibility | Meaning |
| --- | --- |
| `not_eligible_currently` | Candidate cannot be adopted at current posture. |
| `eligible_for_future_license_review_request` | Candidate may request exact license review later. |
| `eligible_for_future_source_inspection_request` | Candidate may request P9.3 exact inspection scope later. |
| `eligible_for_future_dependency_review_request` | Candidate may request dependency review later. |
| `eligible_for_future_adoption_mode_design` | Candidate may be considered by P9.5 after required reviews. |
| `eligible_for_future_execution_request` | Candidate may request exact execution gate later if needed. |
| `rejected_pending_reuse_rejection_record` | Candidate should not be used and any scratch rebuild should record why. |
| `deferred_pending_alignment` | Candidate remains deferred until P9 peers or P9.R align. |

P9.2 default:

```text
All candidates are not eligible for adoption now. They may be eligible only to request future reviews.
```

## 20. AdoptionModeCandidate

`AdoptionModeCandidate` carries the P9.0 adoption-mode vocabulary into the license/trust intake.

P9.2 may identify which modes require which license/trust evidence. P9.2 does not choose an adoption mode. P9.5 owns the vendor/fork/wrapper/submodule/reject/defer decision.

| AdoptionModeCandidate | License/trust implication | P9.2 posture |
| --- | --- | --- |
| `reference_only` | Lowest reuse pressure, but source-local instruction and citation risks still apply. | Candidate only. |
| `path_metadata_only` | Records existence/class only. | Allowed current posture. |
| `source_review_candidate` | Requires P9.3 exact inspection scope. | Future only. |
| `wrap_existing_source` | Requires license, dependency, execution, interface, rollback, and incident review. | Future only. |
| `fork_and_patch` | Requires license modification terms, notice preservation, maintenance, rollback, and divergence review. | Future only. |
| `vendor_snapshot` | Requires license notice retention, provenance, integrity, update, and publication review. | Future only. |
| `submodule_or_dependency` | Requires dependency trust, registry/network/auth, package script, lockfile, and update review. | Future only. |
| `direct_runtime_integration` | Requires execution gate, runtime security, rollback, incident, product/CSS boundaries, and human approval. | Future only; blocked by default. |
| `reject_after_review` | Requires review evidence and reason. | Future review result. |
| `defer_after_review` | Requires deferral reason and revisit condition. | Future review result. |

Adopt-not-rebuild support:

```text
P9.2 supports adopt-not-rebuild by requiring structured license, trust, dependency, and supply-chain review before rejecting a viable external candidate or rebuilding from scratch.
```

## 21. HumanApprovalRequirement

`HumanApprovalRequirement` defines approvals required before any future escalation.

P9.2 records requirements only. It grants no approval.

| Field | Meaning | Required before |
| --- | --- | --- |
| `approval_id` | Stable approval requirement id. | Any future escalation. |
| `approval_scope` | Exact candidate, path, action, and boundary. | Source inspection, dependency review, execution, adoption, Git. |
| `approver` | User, legal/governance reviewer, security reviewer, or named authority. | Scope-specific. |
| `allowed_action` | Exact action approved later. | Must be explicit. |
| `blocked_actions` | Adjacent actions still blocked. | Must be explicit. |
| `required_evidence` | License, provenance, dependency, trust, supply-chain, rollback, incident, and validation evidence. | Before approval. |
| `expiration_or_revisit` | When approval expires or must be revisited. | Before long-lived adoption. |
| `approval_status` | Whether approval exists. | `not_granted_by_P9_2`. |

Human approval is required for:

| Future action | Required gate |
| --- | --- |
| Reading external source content or `LICENSE` files | P9.3 exact source inspection permission gate. |
| Reading dependency manifests, lockfiles, package metadata, or package scripts | P9.3/P9.5 exact dependency review scope. |
| Running external commands, examples, tests, package managers, scanners, or audits | P9.4 exact execution gate. |
| Choosing vendor/fork/wrapper/submodule/dependency adoption | P9.5 adoption mode decision. |
| Defining rollback/incident response for external integration | P9.6 rollback/incident protocol. |
| Staging, committing, or pushing any file | User Git action only; exact paths required. |

## 22. RollbackIncidentRequirement

`RollbackIncidentRequirement` defines future rollback and incident prerequisites for external source adoption or execution.

P9.2 does not implement rollback automation and does not create incident tooling.

| Field | Meaning | P9.2 default |
| --- | --- | --- |
| `requirement_id` | Stable rollback/incident requirement id. | Future record field. |
| `candidate_id` | External candidate id. | Future record field. |
| `adoption_mode` | Candidate adoption mode. | Future P9.5 value. |
| `rollback_scope` | Exact files, dependencies, configs, generated outputs, state, and external refs to remove/disable. | `not_defined_by_P9_2`. |
| `incident_triggers` | Secret exposure, license mismatch, dependency compromise, unexpected execution, network/auth behavior, generated output leakage, or product contamination. | Future P9.6. |
| `evidence_retention` | What safe metadata must be retained. | Governance metadata only now. |
| `cleanup_plan` | How to remove or disable integration. | Future P9.6/P9.5. |
| `owner` | Human owner for incident response. | Future assignment. |
| `status` | Requirement satisfaction status. | `not_satisfied_by_P9_2`. |

Rollback and incident rule:

```text
No external adoption or execution should be approved unless rollback and incident requirements are defined first.
```

## 23. Candidate Path Metadata And Pending Alignments

Canonical external root:

```text
4_external/sources
```

Legacy drift reference only:

```text
external/sources
```

Known candidate path metadata carried from P9.2 preparation:

| Path | Metadata status | P9.2 interpretation |
| --- | --- | --- |
| `4_external/sources` | `present_path_not_inspected` | Canonical external root; no listing or traversal. |
| `external/sources` | `not_present` | Legacy drift path only. |
| `4_external/sources/gstack-main` | `present_path_not_inspected` | GStack path/class metadata only; no source inspection, execution, adoption, or dependency approval. |
| `4_external/sources/gbrain-master` | `present_path_not_inspected` | GBrain path/class metadata only. |
| `4_external/sources/hermes-main` | `not_present` | No Hermes source path at this checked spelling. |
| `4_external/sources/ecc-main` | `present_path_not_inspected` | ECC-main path/class metadata only. |
| `4_external/sources/opencode-main` | `not_present` | No OpenCode source path at this checked spelling. |

P9 peer alignments:

P9.2 preparation initially found P9 peer alignments unavailable. Final read-only Git status later showed separate untracked P9 peer files outside this ticket. P9.2 does not inspect or modify peer contents, so alignment remains pending until an explicit peer/reconciliation gate consumes them.

| Peer | Status during P9.2 preparation | Required alignment marker |
| --- | --- | --- |
| P9.1 External Source Root Normalization | Not consumed by P9.2; alignment pending. | `pending_P9.1_external_source_root_normalization_alignment` |
| P9.3 External Source Inspection Permission Gate | Not consumed by P9.2; alignment pending. | `pending_P9.3_external_source_inspection_permission_gate_alignment` |
| P9.4 External Tool Execution Gate Model | Not consumed by P9.2; alignment pending. | `pending_P9.4_external_tool_execution_gate_alignment` |
| P9.5 Vendor / Fork / Wrapper / Submodule Decision Model | Not consumed by P9.2; alignment pending. | `pending_P9.5_vendor_fork_wrapper_submodule_decision_alignment` |
| P9.6 External Integration Rollback / Incident Protocol | Not consumed by P9.2; alignment pending. | `pending_P9.6_external_integration_rollback_incident_alignment` |
| P9.R External Integration Foundation Closure | Not started. | `pending_P9.R_external_integration_foundation_reconciliation` |

P8 readiness limitation:

```text
0_architecture/governance/agent_platform_p8_mvp_readiness_closure.md was absent during P9.2 preparation. This is recorded as a limitation, not a P9.2 hard blocker, because the corrected P9.0 charter is the required P9.2 prerequisite.
```

## 24. Stop Rules

STOP and report `p9_0_missing_external_tool_integration_charter` if the corrected P9.0 charter is missing.

STOP if P9.2 requires any of the following:

| Stop trigger | Required response |
| --- | --- |
| External source content inspection | Stop; requires P9.3 or later exact scope. |
| `LICENSE` file inspection | Stop; requires future exact source/license inspection scope. |
| Dependency manifest, lockfile, package metadata, or package script inspection | Stop; requires future exact dependency review scope. |
| External source tree listing or traversal | Stop; requires future exact inspection scope. |
| External source execution, tests, examples, package managers, scanners, audits, or builds | Stop; requires P9.4 exact execution gate. |
| External adoption, source copying, vendoring, fork, wrapper, submodule, or dependency use | Stop; requires P9.5 and related gates. |
| Provider/auth/API/MCP, credentials, network, or registry access | Stop; requires explicit future security gate. |
| Product/Siamese source inspection or product activation | Stop; requires product readiness gate such as P4 / GT-09 equivalent. |
| Graphify execution/rerun or `.graphifyignore` modification | Stop; requires future Graphify gate. |
| Persistence, vector DB, graph DB, embeddings, telemetry, event streaming, or CSS substrate selection | Stop; requires future CSS/runtime gates. |
| Validation, tests, builds, scripts, Python, Node, package managers, or CI execution | Stop; not authorized by P9.2. |
| `.gitignore`, `.graphifyignore`, generated output, product, external, or P9 peer file modification | Stop; outside this ticket. |
| Git staging, commit, push, force-add, destructive Git, or `git add .` | Stop; Git mutation is user-owned and not authorized. |

## 25. Created / Modified / Not Created Register

Created:

| Path | Status |
| --- | --- |
| `0_architecture/governance/agent_platform_external_source_license_trust_intake_model.md` | Created as P9.2 governance-only license/trust intake model. |

Modified:

| Area | Status |
| --- | --- |
| Other files | None modified by P9.2. |

Not created / not approved:

| Area | Status |
| --- | --- |
| P9.1, P9.3, P9.4, P9.5, P9.6, P9.R, P10+, P4, EXT.* files | Not created by P9.2. |
| External source inspection | Not approved or performed. |
| `LICENSE` file inspection | Not approved or performed. |
| Dependency manifest/lockfile/package metadata inspection | Not approved or performed. |
| External source listing/traversal | Not approved or performed. |
| External source execution | Not approved or performed. |
| Dependency approval | Not granted. |
| License approval/legal approval | Not granted. |
| External adoption, vendor, fork, wrapper, submodule, dependency, import, or copy | Not approved or performed. |
| Provider/auth/API/MCP, network, credentials, registry, package manager | Not approved or used. |
| Runtime, persistence, vector DB, graph DB, embeddings, telemetry | Not created or activated. |
| Product/Siamese source inspection or activation | Not approved or performed. |
| `.gitignore` / `.graphifyignore` | Not modified. |
| Generated outputs or raw artifacts | Not inspected or modified. |
| Validation, tests, builds, scripts, scanners, SBOMs | Not run or generated. |
| Git staging, commit, push, publication | Not performed. |

## 26. Final Verdict

| Question | Answer |
| --- | --- |
| What did P9.2 create? | `0_architecture/governance/agent_platform_external_source_license_trust_intake_model.md`. |
| What model did P9.2 define? | `ExternalSourceLicenseTrustIntakeModel` with license, provenance, trust, dependency, supply-chain, adoption eligibility, human approval, rollback, and incident requirement records. |
| Did P9.2 support adopt-not-rebuild? | Yes. It defines intake requirements needed before rejecting reusable external candidates or rebuilding from scratch. |
| Did P9.2 verify MIT licenses? | No. It defines MIT as a favorable permissive candidate class only after future verification. |
| Did P9.2 approve any license? | No. |
| Did P9.2 grant dependency approval? | No. |
| Did P9.2 inspect external source contents? | No. |
| Did P9.2 inspect `LICENSE` files? | No. |
| Did P9.2 inspect dependency manifests, lockfiles, package metadata, or package scripts? | No. |
| Did P9.2 execute external tools or package managers? | No. |
| Did P9.2 adopt, vendor, fork, wrap, submodule, copy, import, or configure external source? | No. |
| Did P9.2 activate provider/auth/API/MCP, credentials, network, or runtime? | No. |
| Did P9.2 modify `.gitignore` or `.graphifyignore`? | No. |
| Did P9.2 mutate Git? | No. |
| What external root is canonical? | `4_external/sources`. |
| What legacy root is non-canonical? | `external/sources`. |
| What GStack path is carried forward? | `4_external/sources/gstack-main`, path/class metadata only. |
| What alignments remain pending? | P9.1, P9.3, P9.4, P9.5, P9.6, and P9.R. |
| What is required before P10+ external integration work? | P9.R reconciliation after required P9 peer gates. |

Final markers:

```text
external_source_license_trust_intake_model_ready
mit_license_intake_policy_defined
dependency_trust_review_model_defined
supply_chain_risk_model_defined
adoption_not_rebuild_policy_supported
no_external_source_adoption
no_external_execution
no_dependency_approval_granted
```

Stop after P9.2. Do not start P9.1, P9.3, P9.4, P9.5, P9.6, P9.R, P10+, P4, EXT.*, external source inspection, external execution, dependency approval, adoption, runtime, provider/API/MCP, validation, publication, or Git mutation from this ticket.
