# P15.M2 - Hermes 0.19 License and Notice Reconciliation

Status: P15.M2 license, notice, attribution, branding, redistribution and publication posture ready with constraints.

Final verdict: `hermes_0_19_license_notice_reconciliation_ready_with_constraints`

## Ticket Authority

P15.M2 reconciles licensing and notice evidence for the exact Hermes Agent 0.19.0-derived Pepper migration candidate finalized by P15.M1C.

P15.M2 is an evidence and governance ticket. It does not modify `2_products/**`, does not modify manifests or registers, does not change `.gitattributes` or `.gitignore`, does not create the product `THIRD_PARTY_NOTICES.md`, does not install dependencies, does not query package registries, does not build, does not test, does not start runtimes, does not run Graphify, and does not stage, commit or push.

Authorized P15.M2 Git candidates:

| Path | Disposition |
| --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_license_notice_reconciliation.md` | created governance record |
| `0_architecture/governance/agent_platform_hermes_0_19_license_manifest.tsv` | created machine-readable license manifest |

The ignored local source root `4_external/sources/hermes-agent-v0.19.0` was reacquired only for excluded-source license evidence and remains non-authoritative as a Git candidate.

## Parallel-Lane Boundary

| Field | Value |
| --- | --- |
| P15.M2 worktree | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M2` |
| P15.M2 branch | `p15.m2-license-notice` |
| Branch remote | `origin/p15.m2-license-notice` |
| Integration branch | `origin/p15.m-hermes-0.19-migration` |
| P15.M3 worktree inspected | `false` |
| P15.M4 worktree inspected | `false` |
| Shared product files modified | `0` |

## Dynamic Start State

| Field | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M2` |
| Branch | `p15.m2-license-notice` |
| Dynamic start SHA | `02598c0b737d54e688e74a58ff4fb0d39d4bbd8c` |
| Branch remote SHA | `02598c0b737d54e688e74a58ff4fb0d39d4bbd8c` |
| Migration branch SHA | `02598c0b737d54e688e74a58ff4fb0d39d4bbd8c` |
| HEAD equals branch remote | `true` |
| HEAD equals migration branch | `true` |
| Index empty at start | `true` |
| Staged files at start | `0` |
| Tracked working tree clean at start | `true` |
| Visible untracked task candidates at start | `0` |

## Prerequisites

| Record | Required verdict | State |
| --- | --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_migration_authorization.md` | `hermes_0_19_migration_authorized_with_constraints` | tracked, committed in HEAD, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline.md` | `hermes_0_19_product_baseline_ready_with_constraints` | tracked, committed in HEAD, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline_storage_reconciliation.md` | `hermes_0_19_product_baseline_portable_integrity_ready` | tracked, committed in HEAD, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline_commit_finalization.md` | `hermes_0_19_product_baseline_committed_integrity_finalized` | tracked, committed in HEAD, locally unmodified, unstaged |

Candidate posture from `AGENT_PLATFORM_UPSTREAM_BASELINE.json`:

| Field | Value |
| --- | --- |
| canonical | `false` |
| migration candidate | `true` |
| upstream project | `Hermes Agent` |
| upstream version | `0.19.0` |
| upstream tag | `v2026.7.20` |
| upstream commit | `3ef6bbd201263d354fd83ec55b3c306ded2eb72a` |

## Portable Integrity

P15.M2A re-attests P15.M2 against the committed P15.M1D canonical integrity authority. The current downstream authority is `agent-platform-git-tree-sha256-v2` as implemented by `10_scripts/governance/pepper_baseline_integrity.py`.

| Scope | Algorithm | Files | Bytes | SHA-256 | Status |
| --- | --- | ---: | ---: | --- | --- |
| Candidate below `2_products/pepper-agent` excluding `AGENT_PLATFORM_UPSTREAM_BASELINE.json` | `agent-platform-git-tree-sha256-v2` | 6684 | 148145642 | `fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b` | matched canonical utility output from committed Git blobs |
| Included and transformed upstream payload rows only | `agent-platform-git-tree-sha256-v2` | 6681 | 145406255 | `3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073` | matched canonical utility output from committed Git blobs |
| Baseline record `AGENT_PLATFORM_UPSTREAM_BASELINE.json` | `sha256-git-blob-v1` | not_applicable | 25333 | `5aa7d9582e8036e66a9a81be772aa75b3cb930a978c0128bc0a6b2585baa0fea` | exact committed content hash matched |

Superseded historical values retained as evidence only:

| Value | Classification | Reason |
| --- | --- | --- |
| `27b457b65d8a89bb5c39041bc43b82e6f46c4924c1554f5a1c0fcc7682c19bf7` | `superseded_ambiguous` | P15.M1C candidate aggregate before the executable v2 record-stream contract. |
| `03295db99b2204ac962619251289e145432fe32946ee7efad6201dd0742e4ce6` | `superseded_ambiguous` | P15.M1C payload aggregate before the executable v2 record-stream contract. |
| `92b15fb828d105dbd144599c0a49fcef454646667b53b6de227c9716e1aa234c` | `superseded_baseline_record` | Pre-P15.M1D baseline-record blob hash before canonical metadata update. |
| `3c6f155eba3f01ad4ee924ba62c462de1cdb10fdc1f3099daa8ed1d82a9b912d` | `explained_legacy_variant` | checkout realization digest. |
| `511fffdc2f575506cdcba49b63de3324519b201a6146d680e8a6513f5b5551a6` | `explained_legacy_variant` | checkout realization digest. |
| `0eec7b33f97ba13f66b59d1b2cf3e1a66a26c7d90bfbd0ee5d88a8587cefc727` | `explained_legacy_variant` | superseded P15.M1B pre-commit projection. |

Dedicated re-attestation record: `0_architecture/governance/agent_platform_hermes_0_19_license_notice_v2_reattestation.md`.

## Raw Source Evidence

The exact upstream source was absent at start and was independently reacquired from GitHub because P15.M2 required excluded PowerPoint license evidence.

| Field | Value |
| --- | --- |
| Source repository | `https://github.com/NousResearch/hermes-agent` |
| Version | `0.19.0` |
| Tag | `v2026.7.20` |
| Tag object type | `tag` |
| Tag object SHA | `c7d08de287556b3d339df336b180a39d4980ebd7` |
| Peeled commit type | `commit` |
| Peeled commit SHA | `3ef6bbd201263d354fd83ec55b3c306ded2eb72a` |
| Archive byte count | `154808320` |
| Archive SHA-256 | `5b1db2e6642f6aee669951a8440aab03ec76b1d2832cbf3062ab49754aec3ba0` |
| Raw tree SHA-256 authority | `ca41c8c6c688f7a8e94c238cecb45cb60cbec6c37555ba5eeb92530674e39e07` |
| Extracted regular files | 6737 |
| Extracted regular-file bytes | 149140090 |
| Extracted directories | 905 |
| Nested `.git` directories | 0 |
| Nested `.git` files | 0 |
| Destination | `4_external/sources/hermes-agent-v0.19.0` |
| Destination ignored | `true` |
| Temporary acquisition residue | `0` |

Allowed network used: `https://github.com/NousResearch/hermes-agent` only. No package registries, license databases, Docker registries, provider endpoints or unrelated repositories were contacted.

## Evidence Hierarchy

P15.M2 used this evidence order:

1. P15.M1C committed-integrity record.
2. P15.M1B storage-reconciliation record.
3. P15.M1 baseline record.
4. `AGENT_PLATFORM_IMPORT_MANIFEST.tsv`.
5. `AGENT_PLATFORM_EXCLUSIONS.tsv`.
6. Exact locked Hermes Agent 0.19.0 source.
7. Committed Pepper candidate Git blobs.
8. Exact license and notice files.
9. Package and project license declarations.
10. Committed manifests and lockfiles.
11. Source headers and inline attribution evidence.
12. Upstream prose documentation.

No license was inferred from repository owner, package name, component name, popularity or marketing prose.

## Import Reconciliation

| Classification | Count | License treatment |
| --- | ---: | --- |
| `included_byte_exact` | 160 | included product content |
| `included_canonical_text_lf` | 6517 | included product content with unchanged obligations |
| `transformed_by_canonical_compliance_rule` | 4 | included transformed content with recorded rule |
| `excluded_by_canonical_policy` | 56 | not distributed product content |
| `blocked_unresolved` | 0 | none |

| Check | Result |
| --- | ---: |
| unclassified import rows | 0 |
| excluded content present in product | 0 |
| included content missing from product | 0 |
| duplicate source paths | 0 |
| duplicate destination paths | 0 |

LF canonicalization does not change license ownership, attribution or notice obligations.

## License Inventory

Included formal license and notice artifacts:

| Product path | Evidence | SHA-256 | Classification |
| --- | --- | --- | --- |
| `LICENSE` | MIT root license, Copyright (c) 2025 Nous Research | `821556e6336796450ab852d375117b48a4887e71d255794fd6318d99982a5ab6` | `included_permissive` |
| `plugins/hermes-achievements/LICENSE` | MIT plugin license, Copyright (c) 2026 Hermes Achievements contributors | `5c6bbd852eeff017e73830408977d26e4379c5f9bb6edb03fce171f81db5fe43` | `included_permissive` |
| `plugins/security-guidance/LICENSE` | Apache License 2.0 | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` | `included_notice_required` |
| `plugins/security-guidance/NOTICE` | Anthropic claude-plugins-official attribution | `adc3dd09b90dd9240f56d5b9c782986028a312ab150c84a208de1a5d2b948227` | `included_notice_required` |
| `skills/creative/humanizer/LICENSE` | MIT skill license, Copyright (c) 2025 Siqi Chen | `4ac4810254ab36d45419141aeb8e69bf50652cfafe5b2dab947d06d44e5cbf96` | `included_permissive` |

Additional attribution and restrictive evidence:

| Scope | Evidence | Classification |
| --- | --- | --- |
| GSD-adapted skills | `skills/software-development/spike/SKILL.md` and `skills/creative/sketch/SKILL.md` preserve MIT attribution to `gsd-build/get-shit-done` and Lex Christopherson | `included_notice_required` |
| Pixel art optional skill | `optional-skills/creative/pixel-art/ATTRIBUTION.md` preserves MIT attribution for pixel-art-studio palette material | `included_notice_required` |
| AAAI 2026 template style | `skills/research/research-paper-writing/templates/aaai2026/aaai2026.sty` contains file-specific no-modification and all-rights-reserved language for AAAI publication use | `included_restrictive` |
| PowerPoint skill license | raw source `skills/productivity/powerpoint/LICENSE.txt` restricts extraction, retention, derivative works and redistribution outside applicable Anthropic service terms | `excluded_restrictive` |

SPDX headers found: `0`.

Unclassified license artifacts: `0`.

Unknown licenses treated as permissive: `0`.

## Component Decisions

| Component | Decision | Evidence |
| --- | --- | --- |
| Hermes Agent root | MIT source license preserved; source migration can proceed internally; modified source redistribution is `ready_with_notices` when notices are preserved and file-specific restrictions are respected | `LICENSE`, `pyproject.toml`, `package.json`, `acp_registry/agent.json` |
| Web Dashboard | Source is covered by root MIT evidence; built assets are not committed; future built-asset distribution is `blocked_pending_review` pending dependency notice review | `web/package.json`, package locks, no `hermes_cli/web_dist/**` committed |
| Hermes Desktop | Source is covered by root MIT evidence; binary packaging is `blocked_pending_review` pending Electron, native module, installer, signing, notarization and dependency notice review | `apps/desktop/package.json` |
| Included plugins | `plugins/hermes-achievements` MIT license is preserved; `plugins/security-guidance` Apache-2.0 license and NOTICE are preserved | plugin license files and dashboard manifests |
| Included skills | Root MIT applies generally; `skills/creative/humanizer` carries its own MIT license; GSD and pixel-art attribution must be preserved | skill license and attribution evidence |
| Excluded PowerPoint subtree | `included_in_product=false`; disposition `remain_excluded`; future reconsideration requires separate legal decision | import and exclusion manifests plus raw source license |
| Vendored schemas | Included schema-related code has insufficient standalone license provenance; excluded Office schemas in the PowerPoint subtree remain excluded | schema inventory and exclusion rows |
| Generated or bundled artifacts | Committed plugin dashboard `dist/**` assets require bundle provenance review before public binary or asset redistribution | plugin dashboard manifests and dist file inventory |
| Workspace | Hermes Workspace 2.3.0 remains out of scope for P15.M2 and under P15.M4 | P15.M4 authority |

## PowerPoint Exclusion

The PowerPoint subtree remains excluded from the product.

| Field | Value |
| --- | --- |
| Product path exists | `false` |
| Raw source path exists | `true` |
| License path | `skills/productivity/powerpoint/LICENSE.txt` |
| License SHA-256 | `6f8bd7f4d8ec5cb52b7a59ccb9e8c14c2a4ba529cb5adfc5e0bc676892b8ca79` |
| License classification | `excluded_restrictive` |
| Exclusion rule | `P12_restricted_powerpoint_subtree` |
| Generated complete skill pages | excluded under `P12_restricted_generated_complete_skill_page` |
| Catalog and sidebar references | transformed to remove exact `productivity-powerpoint` entries |
| Future reconsideration | `separate_legal_decision_required` |

No excluded PowerPoint code or license file was copied into the product.

## Dependency Evidence

Dependency and lock evidence was inspected read-only. No dependency installation, package-manager execution or registry query occurred.

| Group | Count |
| --- | ---: |
| Python direct dependencies | 30 |
| Python optional dependency entries | 90 |
| Python optional groups | 42 |
| Node `package.json` files | 11 |
| Node dependency declarations | 157 |
| Node devDependency declarations | 92 |
| Node optionalDependency declarations | 0 |
| Direct dependency declarations total | 369 |
| `package-lock.json` files | 4 |
| Package-lock package records | 3137 |
| Package-lock records with local license fields | 3112 |
| `uv.lock` package records | 233 |
| `uv.lock` local license fields | 0 |
| Lockfile package records total | 3370 |
| Lockfile records with local license evidence | 3112 |
| Lockfile records without local license evidence | 258 |

Classification: `dependency_license_evidence_incomplete`.

Incomplete transitive evidence does not block internal source migration, P15.M3 analysis or P15.M4 analysis. It blocks claims that all dependencies are cleared and blocks public binary/container release until resolved.

## Distribution Decisions

| Gate | Decision |
| --- | --- |
| internal_source_development | `ready` |
| modified_source_redistribution | `ready_with_notices` |
| Desktop_binary_redistribution | `blocked_pending_review` |
| Dashboard_built_asset_redistribution | `blocked_pending_review` |
| container_image_publication | `blocked_pending_review` |
| public_Pepper_branding | `blocked_pending_trademark_review` |
| provider_service_use | `separate_terms_required` |
| PowerPoint_skill | `remain_excluded` |

Modified source redistribution remains notice-bound. It must preserve MIT notices, Apache-2.0 license and NOTICE material, included attribution records, and must not modify or redistribute file-specific restrictive content without review.

## Desktop Packaging Findings

Desktop source and packaging metadata include:

| Evidence | Value |
| --- | --- |
| Package name | `hermes` |
| Product name | `Hermes` |
| App ID | `com.nousresearch.hermes` |
| Protocol | `hermes` |
| Artifact name | `Hermes-${version}-${os}-${arch}.${ext}` |
| macOS targets | `dmg`, `zip` |
| Windows targets | `nsis`, `msi` |
| Linux targets | `AppImage`, `deb`, `rpm` |
| Copyright strings | `Copyright (c) 2026 Nous Research` and equivalent package metadata |
| Native updater | present upstream, not authorized for Pepper by P15.M1 baseline |

Desktop binary distribution remains blocked pending dependency notices, native module review, installer review, signing/notarization review and branding authorization.

## Dashboard Bundle Findings

Web Dashboard source is included, but built `hermes_cli/web_dist/**` is not committed in this candidate. Future Dashboard bundles require dependency license aggregation from the Node graph and generated asset provenance before public distribution.

Committed plugin dashboard bundles are present under:

| Path family | Files | Posture |
| --- | ---: | --- |
| `plugins/hermes-achievements/dashboard/dist/**` | 2 | blocked pending bundled dependency provenance |
| `plugins/kanban/dashboard/dist/**` | 2 | blocked pending bundled dependency provenance |

## Branding Boundary

Observed branding and trademark-sensitive evidence includes Hermes product names, Nous Research references, repository links, Desktop app IDs, protocol handlers, icons, installer names, package names, copyright strings and website links.

Required conclusion: the observed source licenses do not themselves grant trademark rights. Pepper must not be presented as an official Hermes or Nous Research release without separate branding authorization.

P15.M2 does not rename or modify product assets.

## Provider-Service Terms Boundary

Provider and ChatGPT OAuth posture: `external_service_terms_separate`.

Source licenses do not authorize ChatGPT subscription usage, OpenAI account usage, OAuth entitlement, model access, API quota, provider endpoints or other external service terms. P15.M2 performed no OAuth flow, credential read, provider call or inference.

## Container Findings

Container evidence was inspected read-only.

| Evidence | Value | Posture |
| --- | --- | --- |
| `FROM ghcr.io/astral-sh/uv:0.11.6-python3.13-trixie@sha256:b3c543b6c4f23a5f2df22866bd7857e5d304b67a564f4feab6ac22044dde719b` | pinned digest | base image license evidence incomplete |
| `FROM node:22-bookworm-slim@sha256:7af03b14a13c8cdd38e45058fd957bf00a72bbe17feac43b1c15a689c029c732` | pinned digest | base image license evidence incomplete |
| `FROM debian:13.4` | mutable tag | provenance and notice review required |
| APT packages | installed during build | package notice and SBOM review required |
| s6-overlay tarballs | downloaded from GitHub release with SHA-256 checks | license and notice review required |
| Playwright Chromium shell | downloaded during build | browser binary license and notice review required |
| Compose `image: hermes-agent` | local image reference | no independent license evidence |

Container image publication remains `blocked_pending_review` because base-image obligations, SBOM, transitive notices, mutable provenance and runtime/downloaded component obligations are unresolved.

## License Manifest

| Field | Value |
| --- | --- |
| Path | `0_architecture/governance/agent_platform_hermes_0_19_license_manifest.tsv` |
| Rows | 30 |
| Columns | 17 |
| SHA-256 | `5643d432579493a467aec17c0caf742f19d0f5bb9d9e54119b3c67c0845605fb` |
| Duplicate record IDs | 0 |
| Blank mandatory fields | 0 |
| Invalid primary classifications | 0 |
| Unresolved rows without explicit status | 0 |
| Trailing whitespace lines | 0 |

## Future Product Notice Contract

Future path:

```text
2_products/pepper-agent/THIRD_PARTY_NOTICES.md
```

Mandatory future sections:

1. Pepper identity.
2. Hermes Agent 0.19.0 attribution.
3. Exact upstream repository, version, tag and commit.
4. Root MIT license reference.
5. Included Apache-licensed components.
6. Required NOTICE preservation.
7. Included MIT plugin and skill references.
8. Excluded PowerPoint subtree statement.
9. Dependency-license uncertainty statement.
10. Desktop binary-distribution restriction.
11. Dashboard bundle-distribution restriction.
12. Container-publication restriction.
13. Trademark and branding statement.
14. Provider-service terms separation.
15. Preserved license-file locations.
16. Pepper modification attribution.

The future notice must reference preserved license files, must not replace license files, must not include excluded code, must not claim legal certification, must not imply Nous Research endorsement, must not authorize binary/container publication, and must be registered in `AGENT_PLATFORM_MODIFICATIONS.tsv` by a later integrated migration ticket.

Owner ticket: later integrated migration notice-application ticket after P15.M2/P15.M3/P15.M4 dependencies are reconciled.

## Unresolved Evidence

| Area | Status | Gate |
| --- | --- | --- |
| Python transitive dependency licenses | incomplete local license evidence in `uv.lock` | blocks public binary/container clearance claims |
| Node transitive dependency licenses | 25 package-lock records without local license fields | blocks public bundle/binary clearance claims |
| AAAI 2026 style file | file-specific no-modification and restrictive publication-use language | requires review before public redistribution claims or modification |
| Plugin dashboard bundles | committed dist assets without complete bundle provenance | blocks public asset/binary distribution |
| Desktop packages | Electron, native modules, signing, notarization and installer obligations unresolved | blocks Desktop binary distribution |
| Container images | base images, APT packages, s6-overlay, Playwright and SBOM unresolved | blocks public image publication |
| Branding | Hermes and Nous Research marks not licensed by source license | blocks public Pepper branding |
| Providers and OAuth | external terms separate from source license | source license cannot authorize service use |

## Rollback Or Rejection

If P15.M2 is rejected before commit, remove only the two P15.M2 governance candidates:

1. `0_architecture/governance/agent_platform_hermes_0_19_license_notice_reconciliation.md`.
2. `0_architecture/governance/agent_platform_hermes_0_19_license_manifest.tsv`.

The ignored source root may be removed by the human if no longer needed for evidence review. No product rollback is required because no product file was modified.

## Runtime Boundary

| Action | Count |
| --- | ---: |
| Graphify commands | 0 |
| Graphify modifications | 0 |
| dependency installations | 0 |
| package registry queries | 0 |
| builds | 0 |
| tests | 0 |
| runtime starts | 0 |
| Docker starts | 0 |
| WSL mutations | 0 |
| VPS provisioning | 0 |
| OAuth flows | 0 |
| credential reads | 0 |
| provider calls | 0 |
| inference calls | 0 |
| Git staging by agent | 0 |
| Git commits by agent | 0 |
| Git pushes by agent | 0 |

## Final Validation

| Check | Result |
| --- | --- |
| Candidate integrity files | `6684` |
| Candidate integrity bytes | `148145642` |
| Candidate integrity algorithm | `agent-platform-git-tree-sha256-v2` |
| Candidate integrity SHA-256 | `fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b` |
| Payload integrity SHA-256 | `3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073` |
| Baseline record SHA-256 | `5aa7d9582e8036e66a9a81be772aa75b3cb930a978c0128bc0a6b2585baa0fea` |
| Candidate digest before equals after | `true` |
| Baseline record hash before equals after | `true` |
| Product changes | `0` |
| Register changes | `0` |
| Current product changes | `0` |
| External source tracked changes | `0` |
| TSV parses | `true` |
| TSV exact column count | `true` |
| Markdown trailing whitespace | `0` |
| TSV trailing whitespace | `0` |
| P15.M2A re-attestation record | `0_architecture/governance/agent_platform_hermes_0_19_license_notice_v2_reattestation.md` |
| P15.M2A verdict | `hermes_0_19_license_notice_reconciliation_v2_reattested_with_constraints` |
| Authorized candidate files | `2` |
| Unexpected candidate files | `0` |

## Sequencing

P15.M2A is ready for human review and commit. P15.M3 may restart using V2. P15.M4 may proceed using V2. Product notice application remains dependency-gated. P15.M5 remains gated pending parallel-lane integration. Public binary distribution, public container publication, live OAuth, provider calls and inference remain unauthorized.

P15.M2A verdict: `hermes_0_19_license_notice_reconciliation_v2_reattested_with_constraints`.

Final verdict: `hermes_0_19_license_notice_reconciliation_ready_with_constraints`
