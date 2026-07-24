# P15.M3 - Hermes 0.19 Dependency and Lock Reconciliation

Status: P15.M3 dependency and lock reconciliation ready with constraints.

Final verdict: `hermes_0_19_dependency_lock_reconciliation_ready_with_constraints`

## Ticket Authority

P15.M3 statically reconciles dependency declarations, lock authority, toolchain declarations, container references, runtime-download surfaces, generated bundles and current-product dependency deltas for the Hermes Agent 0.19.0-derived Pepper candidate.

No dependency installation, registry query, lock regeneration, build, lint, typecheck, product test, runtime start, Docker start, WSL mutation, OAuth flow, credential read, provider call, inference call or Graphify command was performed.

Authorized P15.M3 candidates:

| Path | Disposition |
| --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_dependency_lock_reconciliation.md` | created governance record |
| `0_architecture/governance/agent_platform_hermes_0_19_dependency_lock_manifest.tsv` | created machine-readable dependency/lock manifest |

## Parallel-Lane Boundary

Work was performed only in `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M3` on branch `p15.m3-dependency-lock`. P15.M2A and P15.M4 were not inspected or modified.

## Dynamic Start State

| Field | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M3` |
| Branch | `p15.m3-dependency-lock` |
| Dynamic HEAD | `525e1a13a0199e7648ccc332c1c06103bc269aaf` |
| Branch remote | `origin/p15.m3-dependency-lock` |
| Branch remote SHA | `525e1a13a0199e7648ccc332c1c06103bc269aaf` |
| Migration HEAD | `525e1a13a0199e7648ccc332c1c06103bc269aaf` |
| HEAD equals branch remote | `true` |
| HEAD equals migration head | `true` |
| P15.M1D ancestor | `true` |
| Index empty at start | `true` |
| Staged files at start | `0` |
| Tracked worktree clean at start | `true` |
| Visible untracked task candidates at start | `0` |

## Prerequisites

Required committed records were present, tracked, locally unmodified and unstaged:

| Record | Verdict |
| --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_migration_authorization.md` | `hermes_0_19_migration_authorized_with_constraints` |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline.md` | `hermes_0_19_product_baseline_ready_with_constraints` |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline_storage_reconciliation.md` | `hermes_0_19_product_baseline_portable_integrity_ready` |
| `0_architecture/governance/agent_platform_hermes_0_19_product_baseline_commit_finalization.md` | `hermes_0_19_product_baseline_committed_integrity_finalized` |
| `0_architecture/governance/agent_platform_hermes_0_19_integrity_algorithm_canonicalization.md` | `hermes_0_19_baseline_integrity_algorithm_canonicalized` |

Required candidate posture remains:

```yaml
path: 2_products/pepper-agent
canonical: false
migration_candidate: true
upstream_project: Hermes Agent
upstream_version: 0.19.0
upstream_tag: v2026.7.20
upstream_commit: 3ef6bbd201263d354fd83ec55b3c306ded2eb72a
```

## Canonical V2 Integrity

Canonical utility:

```text
10_scripts/governance/pepper_baseline_integrity.py
```

Exact CLI:

```text
python 10_scripts/governance/pepper_baseline_integrity.py --repo-root . --product-root 2_products/pepper-agent --mode all --format json
```

Result:

| Scope | Algorithm | Files | Bytes | SHA-256 |
| --- | --- | ---: | ---: | --- |
| Candidate | `agent-platform-git-tree-sha256-v2` | 6684 | 148145642 | `fae505873168de748dd966972e2c20cbea15ac2cfc0ffdc075168ebcf525fa5b` |
| Payload | `agent-platform-git-tree-sha256-v2` | 6681 | 145406255 | `3470f71442bd0dd0ee15a1e70268db7cfe03d787adf58ba16697952c30e0d073` |
| Baseline record | `sha256-git-blob-v1` | not_applicable | 25333 | `5aa7d9582e8036e66a9a81be772aa75b3cb930a978c0128bc0a6b2585baa0fea` |

The historical V1 values are non-authoritative for P15.M3.

## Canonical Utility Tests

Exact command:

```text
python -m unittest discover -s 12_tests/governance -p test_pepper_baseline_integrity.py
```

Result:

```yaml
tests_run: 14
failures: 0
errors: 0
golden_vector_match: true
```

## Static Parsing Methodology

Static parsing used only PowerShell, read-only Git operations and Python standard-library parsers (`json`, `csv`, `tomllib`, `hashlib`, `pathlib`, `re`). Pepper and Hermes source modules were not imported or executed. Package managers, registry queries, lock resolution and lifecycle scripts were not run.

## Dependency Authority Inventory

Candidate authority files parsed: `45`.

| Family | Count / Paths |
| --- | --- |
| Python authority | `pyproject.toml`, `uv.lock`, `setup.py`, `hermes_cli/setup.py`, `hermes_cli/subcommands/setup.py`, `constraints-termux.txt`, skill requirements/setup files |
| Node authority | root `package.json` and `package-lock.json`, workspace package manifests, website/WhatsApp/Photon component manifests and locks |
| Cargo authority | `apps/bootstrap-installer/src-tauri/Cargo.toml`; no `Cargo.lock` committed |
| Container authority | `Dockerfile`, `docker-compose.yml`, `tests/e2e/matrix_xsign_bootstrap/docker-compose.yml` |
| CI authority | `48` workflow setup/install/download lines across candidate workflow files |
| Generated bundles | `4` committed plugin dashboard dist files |

Unclassified dependency authority files: `0`.
Unparsed required files: `0`.

Ecosystems present: `python`, `npm`, `cargo`, `apt`, `container_image`, `git`, `workspace_local`, `runtime_download`, `toolchain`, `not_applicable`.

Component scopes present: `root_python_project`, `root_node_project`, `web_dashboard`, `desktop`, `shared_frontend_package`, `hermes_cli`, `plugin:photon`, `plugin:whatsapp-bridge`, `plugin:kanban`, `plugin:hermes-achievements`, `skill:dcf-model`, `skill:google-workspace`, `tests`, `documentation_build`, `container`, `workflow_CI`, `other_explicit`.

## Lock Authority Decisions

| Component | Manifest | Lock | Decision | Reason |
| --- | --- | --- | --- | --- |
| Root Python project | `pyproject.toml` | `uv.lock` | `single_authoritative_lock` | `uv.lock` contains `233` package entries with resolved versions and hashes for registry artifacts |
| Root Node workspace | `package.json` | `package-lock.json` | `workspace_root_lock` | root npm lockfile version 3 governs root workspaces |
| Web Dashboard | `web/package.json` | `package-lock.json` | `workspace_root_lock` | web is listed in root npm workspaces |
| Desktop | `apps/desktop/package.json`, `apps/bootstrap-installer/package.json` | `package-lock.json` | `workspace_root_lock` | desktop packages are covered by root workspace lock; Rust side lacks Cargo.lock |
| Shared frontend package | `apps/shared/package.json` | `package-lock.json` | `workspace_root_lock` | shared package is a root workspace member |
| TUI workspace | `ui-tui/package.json`, `ui-tui/packages/hermes-ink/package.json` | `package-lock.json` | `workspace_root_lock` | TUI packages are root workspace members |
| Website docs | `website/package.json` | `website/package-lock.json` | `component_local_lock` | docs site uses its own npm lock |
| WhatsApp bridge | `scripts/whatsapp-bridge/package.json` | `scripts/whatsapp-bridge/package-lock.json` | `component_local_lock` | bridge uses component-local npm lock |
| Photon sidecar | `plugins/platforms/photon/sidecar/package.json` | `plugins/platforms/photon/sidecar/package-lock.json` | `component_local_lock` | sidecar uses component-local npm lock |
| Bootstrap Rust/Tauri | `apps/bootstrap-installer/src-tauri/Cargo.toml` | none | `manifest_only_no_lock` | no `Cargo.lock` is committed for Rust dependencies |
| Skill requirements | requirements/setup files | none | `manifest_only_no_lock` | skill-specific Python requirements are ranged and unlocked |
| Containers and OS packages | Dockerfile/Compose | none | `system_packages_no_lock` | images and apt packages require P15.M10 realization |

Components without lock decision: `0`.

Package-lock counts:

- `2_products/pepper-agent/package-lock.json`: lockfileVersion `3`, package entries `1383`
- `2_products/pepper-agent/plugins/platforms/photon/sidecar/package-lock.json`: lockfileVersion `3`, package entries `144`
- `2_products/pepper-agent/scripts/whatsapp-bridge/package-lock.json`: lockfileVersion `3`, package entries `167`
- `2_products/pepper-agent/website/package-lock.json`: lockfileVersion `3`, package entries `1443`

## Python Findings

| Finding | Value |
| --- | --- |
| Manifest authority | `2_products/pepper-agent/pyproject.toml` |
| Lock authority | `2_products/pepper-agent/uv.lock` |
| Python supported range | `>=3.11,<3.14` |
| Exact local analysis target | `3.13` from `tool.ty.environment.python-version` |
| Core direct dependencies | `30` |
| Optional/development direct declarations | `90` |
| uv.lock package entries | `233` |
| VCS/direct URL/path dependencies in uv.lock | editable local `hermes-agent` only |
| Installation authorized | `false` |

Python direct declarations are mostly exact-pinned, but several direct runtime and skill declarations are ranged: `urllib3`, `fastapi`, `uvicorn`, `python-multipart`, `ptyprocess`, `pywinpty`, `nemo-relay`, `openpyxl`, `requests` and Termux constraints. A ranged direct declaration remains ranged even when resolved by `uv.lock`.

Python_manifest: `future_change_required`.
Python_lock: `retain_exact`.
Python_installation_authorized: `false`.

## Node, Dashboard And Desktop Findings

| Finding | Value |
| --- | --- |
| Root workspace declaration | `apps/*`, `ui-tui`, `ui-tui/packages/*`, `web`, `tests-js` |
| Node package direct declarations | `251` |
| Workspace declaration rows | `5` |
| npm lock package entries | `3133` |
| Root Node engine | `>=20.0.0` |
| Desktop Node engine | `^20.19.0 || >=22.12.0` |
| Package manager field | absent; npm inferred from committed package-lock files |
| Native modules | `node-pty`, Electron, Tauri/Rust, Playwright browser asset path |
| Install/build scripts | present; static review only |

Root Node manifest: `future_change_required`.
Root Node lock: `retain_exact`.
Web manifest: `future_change_required`.
Web lock: `workspace_root_authority`.
Desktop manifest: `future_change_required`.
Desktop lock: `workspace_root_authority`.
Desktop install scripts: `review_required`.

## Plugin Findings

Photon sidecar and WhatsApp bridge each have component-local `package-lock.json` authority. Plugin dashboard `dist` bundles are committed for Kanban and Hermes Achievements; their source-output mapping remains incomplete and is assigned to P15.M4/P15.MR for later productization review.

## Container And OS Package Findings

| Surface | Finding |
| --- | --- |
| Docker base images | `3` Dockerfile `FROM` entries inspected |
| Digest-pinned images | `ghcr.io/astral-sh/uv:0.11.6-python3.13-trixie@sha256:...`, `node:22-bookworm-slim@sha256:...` |
| Tag-only image | `debian:13.4` |
| Mutable compose image | `ghcr.io/continuwuity/continuwuity:latest` in test Matrix bootstrap compose |
| Local compose service image | `hermes-agent` service image built locally from Dockerfile |
| OS package group | apt install group in Dockerfile; package versions not pinned |
| Container realization owner | `P15.M10` |

container_reproducibility: `blocked_pending_digest_pinning`.

## Runtime Downloads And Native Updater

Runtime/download rows recorded: `9`.

Verified or partially verified:

- Dockerfile s6-overlay tarballs use SHA-256 ARGs and `sha256sum -c`.

Unverified or mutable:

- uv installer from `https://astral.sh/uv/install.sh` has no pinned script hash;
- Node latest-v22 downloads from `nodejs.org/dist/latest-v*.x` are dynamically resolved in shell, PowerShell and runtime self-heal paths;
- Playwright browser asset download occurs during Docker build without an artifact hash in Dockerfile;
- native desktop updater delegates to `hermes update --yes --gateway --branch`, and is not authoritative for Pepper.

runtime_download_integrity: `partial`.

native_Hermes_updater:

```yaml
authoritative_for_Pepper: false
disposition: adapt_to_governed_updater
future_owner: P15.M17_and_P15.M18
```

## Generated And Bundled Artifacts

Generated or bundled rows recorded: `4`. The committed plugin dashboard bundles are reference-only for this ticket; no rebuild was attempted. Source-output mapping remains incomplete and is a promotion blocker until later productization review.

## Current Product Versus 0.19 Baseline

Material authority deltas recorded: `27`.

Changed upstream authority files:

- `Dockerfile`
- `apps/bootstrap-installer/package.json`
- `apps/desktop/package.json`
- `apps/shared/package.json`
- `hermes_cli/setup.py`
- `package-lock.json`
- `package.json`
- `pyproject.toml`
- `ui-tui/package.json`
- `ui-tui/packages/hermes-ink/package.json`
- `uv.lock`
- `web/package.json`

Added in upstream 0.19 authority files:

- `tests-js/package.json`

Removed upstream 0.19 authority files:

- none

Unchanged authority files:

- `apps/bootstrap-installer/src-tauri/Cargo.toml`
- `constraints-termux.txt`
- `docker-compose.yml`
- `hermes_cli/subcommands/setup.py`
- `optional-skills/finance/dcf-model/requirements.txt`
- `plugins/platforms/photon/sidecar/package-lock.json`
- `plugins/platforms/photon/sidecar/package.json`
- `scripts/whatsapp-bridge/package-lock.json`
- `scripts/whatsapp-bridge/package.json`
- `setup.py`
- `skills/productivity/google-workspace/scripts/setup.py`
- `tests/e2e/matrix_xsign_bootstrap/docker-compose.yml`
- `website/package-lock.json`
- `website/package.json`

Unclassified material deltas: `0`.

## Current Modification Register Review

Precise path-based review of `2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` found:

```yaml
dependency_related_current_register_rows: 0
unclassified_dependency_register_rows: 0
```

No current-register row directly modified dependency manifests, lockfiles, Dockerfiles, Compose files, toolchain files, setup files, requirements files, installer files, update files or download files. Broader text hits mentioning dependency/runtime concepts were non-authoritative product UI/runtime rows and are not dependency authority rows.

## Mutable And Unverified References

| Blocker | Classification | Owner |
| --- | --- | --- |
| conflicting lock managers | `not_present` | P15.MR |
| missing authoritative Python lock | `not_present` | P15.MR |
| missing Cargo lock for Tauri bootstrap | `present_blocking_distribution` | P15.M4/P15.MR |
| floating VCS refs | `present_non_blocking_internal` | P15.M18 |
| unhashed direct URLs | `present_blocking_distribution` | P15.M9/P15.M10/P15.M18 |
| mutable container tags | `present_blocking_distribution` | P15.M10 |
| unverified runtime downloads | `present_blocking_distribution` | P15.M9/P15.M18 |
| unbounded toolchain versions | `present_blocking_build` | P15.M9 |
| native install scripts | `present_blocking_distribution` | P15.M4/P15.M9 |
| platform-specific native modules | `present_non_blocking_internal` | P15.M9/P15.M10 |
| manifest/lock inconsistencies | `unresolved` | P15.M17/P15.MR |
| Pepper dependency deltas not forward-ported | `present_blocking_build` | P15.M4/P15.MR |
| bundles not reproducible | `present_blocking_distribution` | P15.M4/P15.MR |

## Decision Gates

```yaml
Python_manifest: future_change_required
Python_lock: retain_exact
root_Node_manifest: future_change_required
root_Node_lock: retain_exact
Web_manifest: future_change_required
Web_lock: workspace_root_authority
Desktop_manifest: future_change_required
Desktop_lock: workspace_root_authority
Desktop_install_scripts: review_required
container_reproducibility: blocked_pending_digest_pinning
runtime_download_integrity: partial
native_Hermes_updater:
  authoritative_for_Pepper: false
  disposition: adapt_to_governed_updater
dependency_installation_authorized: false
lockfile_regeneration_authorized: false
dependency_reconciliation: ready_for_later_application
lock_reconciliation: ready_for_later_application
```

## Future Application Ownership

| Owner | Files / surfaces |
| --- | --- |
| P15.M3 | this inventory and dependency/lock authority record |
| P15.M4 | `package.json`, `package-lock.json`, `apps/desktop/package.json`, `apps/bootstrap-installer/package.json`, `apps/bootstrap-installer/src-tauri/Cargo.toml`, `apps/shared/package.json`, `web/package.json`, `ui-tui/package.json`, `ui-tui/packages/hermes-ink/package.json`, plugin dashboard bundles |
| P15.M7 | runtime adapter dependency application and runtime package surfaces derived from `pyproject.toml` |
| P15.M8 | provider and credential package extras in `pyproject.toml` and provider-related optional dependency groups |
| P15.M9 | Python/Node/Rust local toolchain realization, install scripts, CI setup-python/setup-node declarations, Node bootstrap downloads |
| P15.M10 | `Dockerfile`, `docker-compose.yml`, test compose, base-image digest pinning, apt package snapshotting, Playwright image asset policy |
| P15.M17 | governed upstream dependency update planning for `pyproject.toml`, `uv.lock`, package manifests and lockfiles |
| P15.M18 | native updater, `hermes update`, desktop update orchestration, passive remote update checks and runtime Node self-heal |
| P15.MR | final dependency and lock promotion gate |

P15.M3 does not authorize those later mutations.

## Dependency Manifest

Path: `0_architecture/governance/agent_platform_hermes_0_19_dependency_lock_manifest.tsv`

```yaml
rows: 3920
columns: 25
bytes: 2109973
SHA256: a2e9c734494a294b65c3785edf5c06c5f3e1939fa7b084d6b1d9681cc1c368f5
duplicate_record_ids: 0
blank_mandatory_fields: 0
invalid_ecosystems: 0
invalid_entry_kinds: 0
invalid_delta_classifications: 0
invalid_reproducibility_classifications: 0
invalid_security_classifications: 0
invalid_lock_authorities: 0
unresolved_rows_without_explicit_status: 0
trailing_whitespace_lines: 0
```

## Product Immutability

```yaml
candidate_before_equals_after: true
payload_before_equals_after: true
baseline_record_before_equals_after: true
Pepper_product_changes: 0
Pepper_register_changes: 0
current_product_changes: 0
current_register_changes: 0
external_source_tracked_changes: 0
Graphify_commands: 0
Graphify_modifications: 0
candidate_files: 2
unexpected_candidate_files: 0
dependency_installations: 0
package_registry_queries: 0
network_dependency_queries: 0
lockfile_regenerations: 0
manifest_modifications: 0
builds: 0
lints: 0
typechecks: 0
product_tests: 0
source_imports: 0
runtime_starts: 0
Docker_starts: 0
WSL_mutations: 0
VPS_provisioning: 0
OAuth_flows: 0
credential_reads: 0
provider_calls: 0
inference_calls: 0
```

## Rollback And Rejection

If P15.M3 is rejected before commit, remove only:

```text
0_architecture/governance/agent_platform_hermes_0_19_dependency_lock_reconciliation.md
0_architecture/governance/agent_platform_hermes_0_19_dependency_lock_manifest.tsv
```

Do not modify `2_products/**`, `.gitattributes`, `.gitignore`, package manifests, lockfiles, scripts, tests, Graphify output, dependency manifests or other worktrees.

## Sequencing

P15.M3 is ready for human review and commit. P15.M2A remains independent in its own branch. P15.M4 may continue using V2. P15.M5 remains gated pending parallel-lane integration. Dependency and lock application remains unauthorized. Live OAuth, provider calls and inference remain unauthorized.

Final verdict:

```text
hermes_0_19_dependency_lock_reconciliation_ready_with_constraints
```
