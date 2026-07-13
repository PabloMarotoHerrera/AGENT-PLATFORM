# P12.3 - Hermes Reproducible Development Environment

## Document Header

| Field | Value |
| --- | --- |
| Project | P12 - Hermes Productization Foundation |
| Ticket | P12.3 - Reproducible Development Environment |
| Type | Development environment / dependency / reproducibility |
| Date | 2026-07-13 |
| Status | `reproducible_development_environment_ready` |
| Canonical output | `0_architecture/governance/agent_platform_hermes_reproducible_development_environment.md` |
| Workspace | `C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM` |
| Product root | `2_products/hermes-agent` |
| Environment posture | Product-local, ignored, frozen-lock installation |
| Application execution | Not performed |

## Purpose

Define and validate a deterministic local development environment for the committed Hermes product snapshot without launching Hermes, starting services, activating providers, using credentials, changing source or lockfiles, or mutating Git index/history.

P12.3 activates only the Python core/development environment and the root npm workspace required for P12.4 core, dashboard, TUI and desktop validation. Documentation-site, optional bridge, Rust/Tauri, Nix and container environments are classified but deferred.

## P12.2 Prerequisite Status

```yaml
P12_2_PrerequisiteStatus:
  baseline_status: license_exclusion_notice_baseline_ready
  baseline_main_repository_commit: e3455d9135096e1901f563359d7911abbf3d4bbc
  product_files_on_disk: 6120
  tracked_product_files: 6120
  import_manifest_rows: 6115
  exclusion_manifest_rows: 56
  product_status_paths_before_setup: 0
  staged_product_paths_before_setup: 0
  nested_git_exists: false
  restricted_paths_absent: true
  main_repository_clean_except_excluded_unrelated_paths: true
```

The only pre-existing untracked paths were `.opencode/`, `AGENTS.md` and `graphify-out/`; they were excluded from P12.3 and not inspected as project inputs.

The locked upstream remained clean at commit `9de9c25f620ff7f1ce0fd5457d596052d5159596`, tag `v2026.7.7.2`, with normalized official origin.

## Workspace and Product Boundary

```yaml
HermesDevelopmentBoundary:
  workspace_root: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM
  product_root: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\2_products\hermes-agent
  workspace_git_root_matches: true
  product_is_main_repository_subtree: true
  product_nested_git: false
  workspace_reparse_point: false
  products_parent_reparse_point: false
  product_root_reparse_point: false
  approved_infrastructure_parent: C:\Users\pablo\OneDrive\Escritorio
```

Permanent project-owned environment state remains inside the product root. Package-manager download caches remain in their standard per-user locations. No sibling repository, worktree, submodule, remote or independent product history was created.

## Source and Lockfile Inventory

| Ecosystem/surface | Declaration | Lock/constraint | Authority | P12.3 decision |
| --- | --- | --- | --- | --- |
| Python core/dev | `pyproject.toml` | `uv.lock` | Authoritative | Activate |
| Root Node workspaces | `package.json` plus workspace package manifests | `package-lock.json` v3 | Authoritative | Activate |
| Website/docs | `website/package.json` | `website/package-lock.json` | Separate authoritative root | Defer; not needed for selected P12.4 baseline |
| WhatsApp bridge | `scripts/whatsapp-bridge/package.json` | local `package-lock.json` | Optional platform root | Defer |
| Photon sidecar | `plugins/platforms/photon/sidecar/package.json` | local `package-lock.json` | Optional plugin root | Defer |
| Rust/Tauri bootstrap | `apps/bootstrap-installer/src-tauri/Cargo.toml` | No `Cargo.lock` | Insufficient frozen authority | Defer |
| Nix | `flake.nix` | `flake.lock` | Secondary/best-effort environment | Defer on native Windows |
| Container | `Dockerfile`, compose files | Pinned images and source locks | CI/release alternative | Inspect only |
| Termux | `constraints-termux.txt` | Platform constraint | Android-specific | Defer |
| Optional DCF skill | local `requirements.txt` | No lockfile | Optional skill | Defer |
| Legacy setup scripts | root/subdirectory `setup.py` files | N/A | Non-authoritative compatibility/tooling | Reject as dependency authority |

Selected immutable input hashes:

```yaml
HermesSelectedDependencyInputs:
  pyproject_toml_sha256: 7F0180B23C28EA3F7A32E037BCFB1D986FA1925D0A9331112BDCE82EF1BFBF45
  uv_lock_sha256: 92D8153C76379A4D427EAF37CD77CEDEF9DC093C6C44C1386ABD4546578F709A
  package_json_sha256: 07B1B0C8D196C93CC4876092907E7350CFC8B04DB18CE34DEBB522AEAD4AD1C0
  package_lock_sha256: BC11D099F043E142764E66F60F2B558ADD882948649101645D56319D188861DF
```

Deferred authoritative/declaration hashes:

```yaml
HermesDeferredDependencyInputs:
  website_package_json: E8F2FAD107A3913ED24B8EAA4C07F579C1003F08BB8F13D63C5CF5B17A4AB7B4
  website_package_lock: 48D7E92FF55640D03E7A783D03F2102D957DC32957F99BCE5B604422516FC658
  whatsapp_package_json: 51678E5E739149C050C257592CD449ECBB8D306C308CF6698CC82BC3092E6CA6
  whatsapp_package_lock: 346391BAB09F6E264E454D776C4461FC3B112AB1038B76E308B9D2C78D29119D
  photon_package_json: 7209A1174D9F6BAF4ADA18FC72D36012325B3DEACB5AC39D6807E471873A2A48
  photon_package_lock: 9D72974A52CB890F3152A6A8B2A0C1AE190CDB9AE4CA13335A278C0A99065189
  cargo_toml: 9C3A89FB7B42D4FEC1340F832ED15650D03D2966176C2568614616E5F430F1E7
  flake_nix: 3F647CB1203955BEBE4E07A093BA9D5F22C1D02A07309E3A99B36410C7C314FF
  flake_lock: 974B9B6338C4BB804937568A8904BE3CB51D920C34FEC3C42E1BE443E8C65CE9
  dockerfile: F2BA5713E5B91B2AA7D8C629FED6A10A0F3796705C45271C834BC3F8D5471FFA
```

## Environment Surface Classification

```yaml
HermesEnvironmentSurfaces:
  - ecosystem: python
    declaration_path: pyproject.toml
    purpose: core_and_development
    authoritative: true
    lockfile_present: true
    required_for_P12_4: true
    activation_decision: activate
    rationale: core runtime, tests, lint and type tooling use the root uv lock
  - ecosystem: node
    declaration_path: package.json
    purpose: dashboard_tui_desktop_shared_bootstrap_frontend
    authoritative: true
    lockfile_present: true
    required_for_P12_4: true
    activation_decision: activate
    rationale: CI installs the root workspace before frontend checks/builds
  - ecosystem: node
    declaration_path: website/package.json
    purpose: documentation_website
    authoritative: true
    lockfile_present: true
    required_for_P12_4: false
    activation_decision: defer
    rationale: separate docs-site lane outside selected product UI baseline
  - ecosystem: node
    declaration_path: scripts/whatsapp-bridge/package.json
    purpose: optional_platform_bridge
    authoritative: true
    lockfile_present: true
    required_for_P12_4: false
    activation_decision: defer
    rationale: provider/platform activation is outside P12.3
  - ecosystem: node
    declaration_path: plugins/platforms/photon/sidecar/package.json
    purpose: optional_plugin_sidecar
    authoritative: true
    lockfile_present: true
    required_for_P12_4: false
    activation_decision: defer
    rationale: optional plugin runtime is outside P12.3
  - ecosystem: rust
    declaration_path: apps/bootstrap-installer/src-tauri/Cargo.toml
    purpose: installer_packaging
    authoritative: false
    lockfile_present: false
    required_for_P12_4: false
    activation_decision: defer
    rationale: no Cargo.lock and no installer packaging baseline selected
  - ecosystem: nix
    declaration_path: flake.nix
    purpose: secondary_reproducibility
    authoritative: true
    lockfile_present: true
    required_for_P12_4: false
    activation_decision: defer
    rationale: best-effort non-native-Windows path
  - ecosystem: container
    declaration_path: Dockerfile
    purpose: CI_release_runtime_alternative
    authoritative: false
    lockfile_present: true
    required_for_P12_4: false
    activation_decision: defer
    rationale: P12.3 does not build or start containers
```

## Runtime Version Resolution

| Runtime/tool | Declared constraint/evidence | Selected version | Status |
| --- | --- | --- | --- |
| Python | `>=3.11,<3.14`; CI selects 3.11 | `3.12.3` at `C:\Users\pablo\anaconda3\python.exe` | Compatible; no runtime installation required |
| uv | Docker pins `0.11.6`; CI uses setup-uv | `0.11.6` temporary bootstrap | Exact pinned package manager |
| Node.js | Root `>=20`; desktop `^20.19.0 || >=22.12.0`; CI selects 22 | `24.12.0` x64 | Compatible with declarations; newer than CI baseline |
| npm | Root lockfile v3; npm 10+ behavior documented | `11.6.2` | Compatible |
| Rust | Cargo minimum `1.77`, no lockfile | `rustc 1.94.0`, `cargo 1.94.0` available | Deferred, not activated |
| Nix | Flake present | Not installed | Deferred |
| Docker | Container alternative | `29.4.1` available | Inspected only; not activated |
| Shell | Ticket execution shell | Windows PowerShell `5.1.26100.8737` | Supported |

Host OS: Microsoft Windows NT `10.0.26200.0`, x64. Native Windows is documented as supported; the embedded dashboard terminal pane remains WSL/POSIX-only, but this does not block core/dashboard/TUI/desktop dependency setup.

## Package Manager Decision

```yaml
HermesPackageManagers:
  python:
    selected: uv 0.11.6
    source: Dockerfile pinned uv stage plus root CI workflow
    bootstrap: exact PyPI wheel in an OS-temporary isolated venv
    global_install: false
  node:
    selected: npm 11.6.2
    source: root package-lock v3 and CI npm ci workflow
    global_install: false
  rejected:
    - pip as product dependency authority
    - yarn
    - pnpm
    - npm install for selected root dependency materialization
```

## Lockfile Authority Decision

```yaml
HermesLockfileAuthority:
  - ecosystem: python
    manifest: pyproject.toml
    lockfile: uv.lock
    package_manager: uv 0.11.6
    frozen_install_supported: true
    selected_for_P12_3: true
    dependency_selection:
      - all
      - dev
    reason: exact root CI core/test environment with no lockfile rewrite
  - ecosystem: node_root_workspace
    manifest: package.json
    lockfile: package-lock.json
    package_manager: npm 11.6.2
    frozen_install_supported: true
    selected_for_P12_3: true
    reason: npm ci is the root-workspace CI authority
```

`uv lock --check` resolved 233 lock packages and passed. No selected lockfile was regenerated or updated.

## Network and Registry Boundary

The selected installations were authorized only after lockfile and credential gates passed.

```yaml
HermesPackageSources:
  python_package_manager_bootstrap:
    - https://pypi.org/simple
    - https://files.pythonhosted.org
  python_locked_dependencies:
    - https://pypi.org/simple
    - https://files.pythonhosted.org
  node_locked_dependencies:
    - https://registry.npmjs.org/
  private_registry_required: false
  git_dependency_selected: false
  provider_or_model_endpoint_contacted: false
```

Declared npm install scripts were allowed as part of the authoritative `npm ci` workflow; no dev server, browser, provider, OAuth or application process was started. No retained installation log was necessary.

## Credential and Provider Boundary

```yaml
HermesEnvironmentCredentialBoundary:
  dependency_install_requires_credentials: false
  private_registry_required: false
  provider_key_required_for_install: false
  provider_key_required_for_environment_verification: false
  real_env_file_created: false
  authentication_performed: false
  credential_value_inspected: false
  provider_activation_performed: false
```

Only public declarations and documented `.env.example` variable names were considered. No real `.env`, user Hermes home, OAuth state, browser profile, provider configuration or token file was read or created.

## Python Environment

```yaml
HermesPythonEnvironment:
  activated: true
  python_version: 3.12.3
  package_manager: uv 0.11.6
  manifest: pyproject.toml
  lockfile: uv.lock
  environment_path: 2_products/hermes-agent/.venv
  dependency_extras:
    - all
    - dev
  frozen_install: true
  locked_packages_checked: 107
  installed_distribution_count: 108
  project_distribution: hermes-agent 0.18.2
  source_files_modified: []
```

Verified development tools include pytest `9.0.2`, ruff `0.15.10`, ty `0.0.21` and debugpy `1.8.20`. Package metadata was queried without importing Hermes application modules.

## Node Environment

```yaml
HermesNodeEnvironment:
  activated: true
  package_root: 2_products/hermes-agent
  node_version: 24.12.0
  package_manager: npm 11.6.2
  lockfile: package-lock.json
  lockfile_version: 3
  frozen_install: true
  npm_ci_added_packages: 1300
  npm_audited_packages: 1307
  npm_reported_vulnerabilities: 0
  npm_query_entries: 1301
  npm_ls_exit_code: 0
  source_files_modified: []
```

`npm ls --all --depth=0` returned exit `0`. It reported five optional/platform support packages as extraneous; this is retained as a limitation because `npm ci`, lock hashes and source status all passed.

## Rust/Native Environment

Rust `1.94.0` and Cargo `1.94.0` were present, but the only Cargo surface is the optional Tauri bootstrap installer and no `Cargo.lock` exists. Rust/Tauri activation and system compiler/SDK installation were therefore deferred. npm-managed native dependencies, including `node-pty`, installed successfully through the selected root lock workflow.

No system-wide compiler, SDK, Rust component or native package was installed.

## Nix/Container Posture

Nix is a secondary best-effort environment with a committed flake lock but is unavailable on this native Windows host; it was not installed or evaluated. Docker `29.4.1` is available and the Dockerfile records Python 3.13, uv 0.11.6 and Node 22 evidence, but no image was built and no container or service was started.

## Generated-State Policy

| Path | Created | Ignored | Tracked/staged | Reparse posture |
| --- | --- | --- | --- | --- |
| `.venv/` | Yes | Yes | None | Root is a normal directory |
| `node_modules/` | Yes | Yes | None | Root is a normal directory |
| `hermes_agent.egg-info/` | Yes | Yes | None | Generated editable-install metadata |
| `C:\Users\pablo\AppData\Local\uv\cache` | External standard cache | N/A | Outside repository | User cache |
| `C:\Users\pablo\AppData\Local\npm-cache` | External standard cache | N/A | Outside repository | User cache |

npm created six expected workspace junctions inside ignored `node_modules`; each resolves to an exact tracked workspace inside the product root: desktop, TUI, web, bootstrap installer, Hermes Ink and shared. No unexpected reparse path was accepted.

No `9_artifacts/hermes/p12.3` evidence path was needed.

## Environment Creation

Exact executed creation sequence:

```powershell
$Bootstrap = "C:\Users\pablo\AppData\Local\Temp\opencode\p12_3_uv_bootstrap"
$Python = "C:\Users\pablo\anaconda3\python.exe"

& $Python -m venv $Bootstrap
& "$Bootstrap\Scripts\python.exe" -m pip install `
    --disable-pip-version-check `
    --no-input `
    uv==0.11.6

& "$Bootstrap\Scripts\uv.exe" lock --check
& "$Bootstrap\Scripts\uv.exe" sync `
    --frozen `
    --python $Python `
    --extra all `
    --extra dev

npm ci
```

The temporary uv bootstrap was outside the repository, non-reparse, and removed after successful verification. `.venv` and `node_modules` remain available for P12.4.

## Dependency Installation

Python installation prepared and installed 107 locked packages plus the editable Hermes distribution. Root npm installation added 1,300 packages, audited 1,307 and reported zero vulnerabilities. Both operations completed without credentials, private registries, lockfile updates or product-source changes.

No website-only, WhatsApp, Photon, Rust/Tauri, Nix, container, optional-skill or global dependency installation occurred.

## Environment Verification

Executed side-effect-free verification:

```powershell
& ".venv\Scripts\python.exe" --version
& ".venv\Scripts\python.exe" -c `
  "import importlib.metadata as m; print(len(list(m.distributions())))"

& "$Bootstrap\Scripts\uv.exe" sync `
    --frozen `
    --check `
    --python ".venv\Scripts\python.exe" `
    --extra all `
    --extra dev

npm ls --all --depth=0
npm query "*" --json
```

Results:

```yaml
HermesEnvironmentVerification:
  python_version_matches: true
  python_distribution_metadata_readable: true
  uv_frozen_check_result: would_make_no_changes
  npm_ls_exit_code: 0
  npm_query_succeeded: true
  generated_roots_ignored: true
  generated_roots_untracked: true
  generated_roots_unstaged: true
  application_runtime_executed: false
```

No Python import that initializes Hermes, provider, user state or runtime services was performed.

## Source Drift Validation

Before and after both installations:

- product Git status was empty;
- no product path was staged;
- all 6,120 baseline files remained tracked;
- dependency manifests, lockfiles and P12.2 legal/provenance hashes were unchanged.

```yaml
HermesSourceDriftValidation:
  pyproject_unchanged: true
  uv_lock_unchanged: true
  package_json_unchanged: true
  package_lock_unchanged: true
  P12_2_legal_provenance_files_unchanged: true
  product_source_change_count: 0
  lockfile_change_count: 0
  source_drift_detected: false
```

## Teardown Procedure

Teardown is defined but was not executed because P12.4 requires the environment to remain available.

```powershell
$ProductRoot = "C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\2_products\hermes-agent"
$GeneratedRelative = @(
    ".venv",
    "node_modules",
    "hermes_agent.egg-info"
)

foreach ($Relative in $GeneratedRelative) {
    $Full = [IO.Path]::GetFullPath((Join-Path $ProductRoot $Relative))
    if (-not $Full.StartsWith($ProductRoot + "\", [StringComparison]::OrdinalIgnoreCase)) {
        throw "Generated path escaped product root: $Full"
    }

    git -C $ProductRoot check-ignore -q -- $Relative
    if ($LASTEXITCODE -ne 0) {
        throw "Generated path is not ignored: $Full"
    }

    if (@(git -C $ProductRoot ls-files -- $Relative "$Relative/**").Count -ne 0) {
        throw "Generated path is tracked: $Full"
    }

    $Item = Get-Item -LiteralPath $Full -Force
    if ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
        throw "Generated root is a reparse point: $Full"
    }

    Remove-Item -LiteralPath $Full -Recurse -Force
}
```

The exact generated roots only may be removed. Preserve product source, lockfiles, manifests and all P12.2 legal/provenance files. Never use Git clean/reset/restore, wildcard deletion or parent-directory deletion.

## Clean Recreation Procedure

The broader destructive drill is deferred to P12.7. Deterministic recreation is defined as:

1. Verify committed clean product source and immutable input hashes.
2. Verify Python `3.12.3`, Node `24.12.0` and npm `11.6.2` or stop on mismatch.
3. Create the exact temporary uv bootstrap and install `uv==0.11.6`.
4. Run `uv lock --check`.
5. Run `uv sync --frozen --python <exact-python> --extra all --extra dev`.
6. Run root `npm ci`.
7. Run the environment verification commands.
8. Require unchanged lock/source hashes and empty product Git status.
9. Remove only the temporary uv bootstrap; retain `.venv` and `node_modules` for development.

No full teardown/recreation cycle was performed in P12.3.

```yaml
HermesDevelopmentEnvironmentRecipe:
  workspace_root: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM
  product_root: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\2_products\hermes-agent
  prerequisites:
    - Python 3.12.3 x64
    - Node.js 24.12.0 x64
    - npm 11.6.2
    - public PyPI and npm registry access
  create:
    - python -m venv <approved-temp>/p12_3_uv_bootstrap
    - <bootstrap-python> -m pip install --no-input uv==0.11.6
    - uv lock --check
    - uv sync --frozen --python <python-3.12.3> --extra all --extra dev
    - npm ci
  verify:
    - .venv/Scripts/python.exe --version
    - uv sync --frozen --check --python .venv/Scripts/python.exe --extra all --extra dev
    - npm ls --all --depth=0
    - npm query * --json
    - compare immutable hashes and Git status
  deactivate:
    - no persistent shell activation required
  teardown:
    - remove exact ignored .venv, node_modules and hermes_agent.egg-info after containment checks
  recreate:
    - repeat create and verify from the committed locks
```

## P12.4 Handoff

P12.4 may proceed only after human acceptance and commit of this P12.3 record while the repository is clean and `.venv`/`node_modules` remain available.

P12.4 owns Python tests, lint/type checks, frontend builds, baseline application/UI launch and lifecycle evidence. It must use the installed locks without changing dependencies and must preserve the credential/provider boundary. The separate docs website, optional bridges, Rust/Tauri packaging, Nix and container builds are not activated by this baseline and require explicit P12.4 scope if needed.

```text
hermes_P12_4_ready
```

## P12.5 Relationship

P12.5 synchronization-strategy design may consume:

```text
pyproject.toml and uv.lock authority
root package.json and package-lock.json authority
.venv, node_modules and hermes_agent.egg-info generated-state policy
Python 3.12.3 / uv 0.11.6 behavior
Node 24.12.0 / npm 11.6.2 behavior
Windows workspace-junction posture
deferred website, optional bridge, Rust, Nix and container surfaces
```

P12.3 performed no upstream fetch or synchronization.

## Created / Modified / Generated / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_hermes_reproducible_development_environment.md
```

Generated and ignored:

```text
2_products/hermes-agent/.venv/**
2_products/hermes-agent/node_modules/**
2_products/hermes-agent/hermes_agent.egg-info/**
standard external uv and npm cache entries
```

Transient and removed:

```text
C:\Users\pablo\AppData\Local\Temp\opencode\p12_3_uv_bootstrap
```

Modified product source/configuration:

```text
none
```

Not created, modified or activated:

```text
root or product-local .gitignore
pyproject.toml, uv.lock, package.json or package-lock.json
P12.2 legal/provenance files and manifests
P12.C1, P12.C2, P12.C3, P12.1 or P12.2 records
locked upstream or sibling products
real .env, credentials, OAuth state or provider configuration
website node_modules, optional bridge environments, Cargo/Nix/container environment
9_artifacts/hermes/p12.3
nested Git, product branch, remote, worktree or submodule
build, test, coverage or application runtime output
additional governance Markdown
```

## Limitations

- Local Python `3.12.3` is permitted by the lock and project range but differs from CI's primary Python `3.11` selection and Docker's Python `3.13` image.
- Local Node `24.12.0` satisfies declared engines but is newer than CI/Docker Node `22`.
- `npm ls` returned success while labeling five optional/platform-support transitive packages as extraneous.
- npm workspaces use six expected junctions inside ignored `node_modules`; all targets remain inside the product root.
- Website/docs dependencies, optional bridge/plugin dependencies, Rust/Tauri, Nix and container environments were not activated.
- No build, test, lint, typecheck, application import, server, dashboard, worker, agent loop or UI launch was run; those product-level checks belong to P12.4.
- Full teardown/recreation is defined but deferred to P12.7.
- Legal, SBOM, redistribution, publication and hosted-release blockers from P12.2 remain unchanged.

## Final Verdict

```yaml
P12_3_ReproducibleDevelopmentEnvironmentVerdict:
  p12_2_baseline_committed: true
  main_repository_clean_before_setup: true
  product_baseline_verified: true
  environment_surfaces_inventory_complete: true
  runtime_requirements_resolved: true
  package_managers_resolved: true
  lockfile_authority_resolved: true
  frozen_dependency_installation_used: true
  python_environment_ready: true
  node_environment_ready: true
  native_environment_ready: deferred_not_required
  generated_state_ignored: true
  lockfiles_unchanged: true
  source_drift_detected: false
  credentials_used: false
  provider_activation_performed: false
  application_runtime_executed: false
  teardown_defined: true
  clean_recreation_defined: true
  P12_4_may_proceed: true
  final_verdict: reproducible_development_environment_ready
```

```text
hermes_reproducible_development_environment_ready
hermes_language_runtime_requirements_resolved
hermes_package_manager_requirements_resolved
hermes_lockfile_authority_resolved
hermes_python_environment_created
hermes_node_environment_created_if_required
hermes_dependency_installation_completed
hermes_environment_verification_passed
hermes_generated_state_isolated
hermes_cache_paths_governed
hermes_environment_teardown_defined
hermes_clean_recreation_defined
hermes_P12_4_ready
no_provider_activation
no_credentials_used
no_application_runtime_execution
no_network_service_started
no_git_mutation_by_agent
```

## Human Commit Boundary

The agent did not stage, commit or push. After human review:

```powershell
$Record = "0_architecture/governance/agent_platform_hermes_reproducible_development_environment.md"

git status --short
git add -- $Record

$Staged = @(
    git diff --cached --name-only |
        Sort-Object -Unique
)

if ($Staged.Count -ne 1 -or $Staged[0] -ne $Record) {
    throw "Unexpected staged paths: $($Staged -join ', ')"
}

git commit -m "P12.3 - Define Hermes reproducible development environment"
git push origin main
```

Never use `git add .`, `git add -A` or `git add -f`.
