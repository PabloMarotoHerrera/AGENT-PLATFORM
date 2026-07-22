# Hermes 0.19.0 and Workspace 2.3.0 Source Lock

Status: P15.U0 source-persistence reconciliation complete.

Final verdict: `hermes_0_19_workspace_sources_locked`

## Authority

P15.U0 locks exact local source-only references for Hermes Agent 0.18.2, Hermes Agent 0.19.0, and Hermes Workspace 2.3.0.

P15.U0 did not install dependencies, execute source files, run builds, run tests, start Hermes, start Workspace, start Docker, start OAuth, read credentials, call providers, perform inference, run Graphify, modify the editable product, stage, commit, push, stash, reset, clean, or create worktrees.

Task-specific source persistence is binding:

- source trees are local ignored immutable references;
- source trees are not Git commit candidates;
- `.gitignore` was not modified;
- no external source was force-added;
- this governance record is the only tracked P15.U0 candidate.

## Dynamic Start

- Branch: `p15.u-hermes-adoption-assessment`
- Dynamic start SHA: `fea7d3963a598b848768671e00d5bad8065a4421`
- Origin main at start: `fea7d3963a598b848768671e00d5bad8065a4421`
- HEAD equals origin/main at start: `true`
- Initial tracked worktree clean: `true`
- Initial index empty: `true`
- Initial P15.4 candidate present: `false`
- Initial P15.4 register rows present: `false`
- Initial source retrieval date UTC: `2026-07-22T10:08:55Z`
- Persistence reconciliation date UTC: `2026-07-22T10:46:30Z`

## Ignore Evidence

Source-root ignore rule:

` .gitignore:14:4_external/sources/`

Per-root evidence after reconciliation:

| Root | Exists | Ignored | Ignore rule source | Tracked file count | Visible untracked file count |
| --- | --- | --- | --- | ---: | ---: |
| `4_external/sources/hermes-agent` | true | true | `.gitignore:14:4_external/sources/` | 0 | 0 |
| `4_external/sources/hermes-agent-v0.19.0` | true | true | `.gitignore:14:4_external/sources/` | 0 | 0 |
| `4_external/sources/hermes-workspace-v2.3.0` | true | true | `.gitignore:14:4_external/sources/` | 0 | 0 |

Persistence classification:

- Tracked authorized candidates: `1`
- Tracked candidate: `0_architecture/governance/agent_platform_hermes_0_19_workspace_source_lock.md`
- Local immutable source roots: `3`
- Unexpected tracked candidates: `0`
- Unexpected visible untracked task candidates: `0`
- Missing local source roots: `0`

P15.U must run in this worktree while the verified local source roots remain present. Future worktrees must reacquire these sources from the exact locked identities and verify the recorded tree hashes.

## Acquisition Method

Each acquired source used a temporary acquisition root outside the repository, a temporary bare Git clone, exact approved tag fetch, tag-object resolution, peeled commit resolution, exact full commit verification, `.gitmodules` and `.gitattributes` inspection, `git archive` tar creation from the verified commit, archive SHA-256 calculation, plain source extraction, final tree verification, and temporary residue cleanup.

Allowed temporary Git operations used: `clone`, `fetch`, `rev-parse`, `cat-file`, `show`, and `archive`.

No source checkout, source execution, dependency installation, submodule initialization, Git LFS fetch, or Git LFS pull occurred.

## Hermes Agent 0.18.2

Persistence correction:

- Existing reference missing at start: `true`
- Reference reacquired from exact upstream identity: `true`
- Dirty checkout copy used: `false`

Identity:

- Repository: `https://github.com/NousResearch/hermes-agent`
- Version: `0.18.2`
- Tag: `v2026.7.7.2`
- Tag object type: `tag`
- Tag object SHA: `b7751df34688835a108e0d630f3495fc11f3df79`
- Peeled object type: `commit`
- Peeled commit SHA: `9de9c25f620ff7f1ce0fd5457d596052d5159596`
- Expected commit SHA: `9de9c25f620ff7f1ce0fd5457d596052d5159596`
- Commit match: `true`
- Destination: `4_external/sources/hermes-agent`

Archive and tree integrity:

- Archive format: `tar`
- Archive byte count: `140021760`
- Archive SHA-256: `9dc6657125d31b98233c172e504203a7128800e5f141ef4603f200adfbd0e683`
- Archive created from commit: `9de9c25f620ff7f1ce0fd5457d596052d5159596`
- Archive retained in repository: `false`
- Tree digest algorithm: `agent-platform-tree-sha256-v1`
- Tree SHA-256: `6038ff8d40235109dcf85ad8751b050700b31b9fcfb438915f437a91b3292849`
- Regular file count: `6171`
- Directory count: `869`
- Total regular-file bytes: `134815928`
- Zero-byte file count: `37`
- Symlink count: `0`
- Reparse-point count: `0`

Version declaration evidence:

- `pyproject.toml`, line 10: `0.18.2`, agrees.
- `hermes_cli/__init__.py`, line 17: `0.18.2`, agrees.
- `hermes_cli/__init__.py`, line 18: `2026.7.7.2`, agrees with tag.
- `acp_registry/agent.json`, line 4: `0.18.2`, agrees.
- `package.json` and `package-lock.json` root private JS metadata: `1.0.0`, recorded as non-authoritative for the Python Hermes Agent release.

License and notice inventory:

- `LICENSE` | bytes `1091` | SHA-256 `e29dfaf6905a8d396a58ea4bd84ad27057756bbd9599b5bec0971ae34d2a2118` | `MIT License`
- `plugins/hermes-achievements/LICENSE` | bytes `1110` | SHA-256 `d40010024938b643e3d5e304a17563a2eec1815b8686726474dc00b3f797edc0` | `MIT License`
- `plugins/security-guidance/LICENSE` | bytes `11560` | SHA-256 `3ddf9be5c28fe27dad143a5dc76eea25222ad1dd68934a047064e56ed2fa40c5` | `Apache License`
- `plugins/security-guidance/NOTICE` | bytes `1264` | SHA-256 `152c0f404a6bfcc9430cf90269fd05a984b92f2f971eeec7e6f1c4dc100a53af` | `Apache License`
- `skills/creative/humanizer/LICENSE` | bytes `1087` | SHA-256 `caa1be9cba41c1afb88fe730ab1a4e04728295ea5b29ac2ee9f003a4ffbe3a77` | `MIT License`
- `skills/productivity/powerpoint/LICENSE.txt` | bytes `1497` | SHA-256 `6f8bd7f4d8ec5cb52b7a59ccb9e8c14c2a4ba529cb5adfc5e0bc676892b8ca79` | `not_directly_stated`

Submodule, LFS, nested Git, and residue evidence:

- `.gitmodules`: `absent`
- `.gitattributes`: `present`
- Git LFS filters declared: `false`
- Git LFS pointer count: `0`
- Nested `.git` directories: `0`
- Nested `.git` files: `0`
- `node_modules` directories: `0`
- `.venv` or `venv` directories: `0`
- `__pycache__` directories: `0`
- `auth.json` files: `0`
- committed `.env` files: `0`
- Source files executed: `0`
- Scripts executed: `0`
- Dependency installations: `0`

Script-like inventory:

- `.py`: `2913`
- `.js`: `11`
- `.ts`: `779`
- `.tsx`: `419`
- `.sh`: `23`
- `.ps1`: `3`
- `.bat`: `0`
- `.cmd`: `1`
- `Dockerfile*`: `1`
- Compose files: `3`

## Hermes Agent 0.19.0

Reuse status:

- Provisional acquisition reused unchanged: `true`
- Current tree digest matches recorded digest: `true`

Identity:

- Repository: `https://github.com/NousResearch/hermes-agent`
- Version: `0.19.0`
- Tag: `v2026.7.20`
- Tag object type: `tag`
- Tag object SHA: `c7d08de287556b3d339df336b180a39d4980ebd7`
- Peeled object type: `commit`
- Peeled commit SHA: `3ef6bbd201263d354fd83ec55b3c306ded2eb72a`
- Expected commit SHA: `3ef6bbd201263d354fd83ec55b3c306ded2eb72a`
- Commit match: `true`
- Destination: `4_external/sources/hermes-agent-v0.19.0`

Archive and tree integrity:

- Archive format: `tar`
- Archive byte count: `154808320`
- Archive SHA-256: `5b1db2e6642f6aee669951a8440aab03ec76b1d2832cbf3062ab49754aec3ba0`
- Archive created from commit: `3ef6bbd201263d354fd83ec55b3c306ded2eb72a`
- Archive retained in repository: `false`
- Tree digest algorithm: `agent-platform-tree-sha256-v1`
- Tree SHA-256: `ca41c8c6c688f7a8e94c238cecb45cb60cbec6c37555ba5eeb92530674e39e07`
- Regular file count: `6737`
- Directory count: `905`
- Total regular-file bytes: `149140090`
- Zero-byte file count: `37`
- Symlink count: `0`
- Reparse-point count: `0`

Version declaration evidence:

- `pyproject.toml`, line 10: `0.19.0`, agrees.
- `hermes_cli/__init__.py`, line 17: `0.19.0`, agrees.
- `hermes_cli/__init__.py`, line 18: `2026.7.20`, agrees with tag.
- `acp_registry/agent.json`, line 4: `0.19.0`, agrees.
- `acp_registry/agent.json`, line 12: distribution pin `hermes-agent[acp]==0.19.0`, agrees.
- `package.json` and `package-lock.json` root private JS metadata: `1.0.0`, recorded as non-authoritative for the Python Hermes Agent release.

License and notice inventory:

- `LICENSE` | bytes `1091` | SHA-256 `e29dfaf6905a8d396a58ea4bd84ad27057756bbd9599b5bec0971ae34d2a2118` | `MIT License`
- `plugins/hermes-achievements/LICENSE` | bytes `1110` | SHA-256 `d40010024938b643e3d5e304a17563a2eec1815b8686726474dc00b3f797edc0` | `MIT License`
- `plugins/security-guidance/LICENSE` | bytes `11560` | SHA-256 `3ddf9be5c28fe27dad143a5dc76eea25222ad1dd68934a047064e56ed2fa40c5` | `Apache License`
- `plugins/security-guidance/NOTICE` | bytes `1264` | SHA-256 `152c0f404a6bfcc9430cf90269fd05a984b92f2f971eeec7e6f1c4dc100a53af` | `Apache License`
- `skills/creative/humanizer/LICENSE` | bytes `1087` | SHA-256 `caa1be9cba41c1afb88fe730ab1a4e04728295ea5b29ac2ee9f003a4ffbe3a77` | `MIT License`
- `skills/productivity/powerpoint/LICENSE.txt` | bytes `1497` | SHA-256 `6f8bd7f4d8ec5cb52b7a59ccb9e8c14c2a4ba529cb5adfc5e0bc676892b8ca79` | `not_directly_stated`

Submodule, LFS, nested Git, and residue evidence:

- `.gitmodules`: `absent`
- `.gitattributes`: `present`
- Git LFS filters declared: `false`
- Git LFS pointer count: `0`
- Nested `.git` directories: `0`
- Nested `.git` files: `0`
- `node_modules` directories: `0`
- `.venv` or `venv` directories: `0`
- `__pycache__` directories: `0`
- `auth.json` files: `0`
- committed `.env` files: `0`
- Upstream committed build-named directories: `plugins/hermes-achievements/dashboard/dist`, `plugins/kanban/dashboard/dist`
- Build outputs created by P15.U0: `0`
- Source files executed: `0`
- Scripts executed: `0`
- Dependency installations: `0`

Script-like inventory:

- `.py`: `3143`
- `.js`: `12`
- `.ts`: `993`
- `.tsx`: `494`
- `.sh`: `25`
- `.ps1`: `4`
- `.bat`: `0`
- `.cmd`: `1`
- `Dockerfile*`: `1`
- Compose files: `3`

## Hermes Workspace 2.3.0

Reuse status:

- Provisional acquisition reused unchanged: `true`
- Current tree digest matches recorded digest: `true`

Identity:

- Repository: `https://github.com/outsourc-e/hermes-workspace`
- Version: `2.3.0`
- Tag: `v2.3.0`
- Tag object type: `tag`
- Tag object SHA: `0218dbafce50fa69ba9ce045e2c8a3f5383bd1db`
- Peeled object type: `commit`
- Peeled commit SHA: `15fa9cd706f5c04e4db288fb958e21d10fc776da`
- Expected commit SHA: `15fa9cd706f5c04e4db288fb958e21d10fc776da`
- Commit match: `true`
- Destination: `4_external/sources/hermes-workspace-v2.3.0`

Archive and tree integrity:

- Archive format: `tar`
- Archive byte count: `101693440`
- Archive SHA-256: `10119f375ee7632443353fd7d2f1e45ca613caa971123f0f72c3890c8dc3c438`
- Archive created from commit: `15fa9cd706f5c04e4db288fb958e21d10fc776da`
- Archive retained in repository: `false`
- Tree digest algorithm: `agent-platform-tree-sha256-v1`
- Tree SHA-256: `f00b66d6e7dc5bef87602cb026bdf14e593314b9fd242e3e1af48c20704616b9`
- Regular file count: `1057`
- Directory count: `142`
- Total regular-file bytes: `100799318`
- Zero-byte file count: `0`
- Symlink count: `0`
- Reparse-point count: `0`

Version declaration evidence:

- `package.json`, line 3: `2.3.0`, agrees.
- `pnpm-lock.yaml`: present; no root version field identified in bounded metadata inspection.
- `package-lock.json`: absent.
- `pnpm-workspace.yaml`: absent.

License and notice inventory:

- `LICENSE` | bytes `1099` | SHA-256 `8ad52a97ec60cd6c4c125fd5996805c866477218d5552714f0395b3bb16e2286` | `MIT License`

Submodule, LFS, nested Git, and residue evidence:

- `.gitmodules`: `absent`
- `.gitattributes`: `absent`
- Git LFS filters declared: `false`
- Git LFS pointer count: `0`
- Nested `.git` directories: `0`
- Nested `.git` files: `0`
- `node_modules` directories: `0`
- `.venv` or `venv` directories: `0`
- `__pycache__` directories: `0`
- `auth.json` files: `0`
- committed `.env` files: `0`
- Build outputs created by P15.U0: `0`
- Source files executed: `0`
- Scripts executed: `0`
- Dependency installations: `0`

Script-like inventory:

- `.py`: `3`
- `.js`: `5`
- `.ts`: `415`
- `.tsx`: `341`
- `.sh`: `7`
- `.ps1`: `0`
- `.bat`: `0`
- `.cmd`: `0`
- `Dockerfile*`: `1`
- Compose files: `2`

## Product, Register, and Graphify Integrity

- Editable product path: `2_products/hermes-agent`
- Product tracked files before: `6246`
- Product tracked files after: `6246`
- New product files: `0`
- Editable product tracked changes: `0`
- `AGENT_PLATFORM_MODIFICATIONS.tsv` modified: `false`
- Register rows: `128`
- Register columns: `18`
- Register duplicate IDs: `0`
- Register duplicate paths: `0`
- Register missing fields: `0`
- Register hash mismatches: `0`
- Product manifests outside local source roots modified: `false`
- Product lockfiles outside local source roots modified: `false`
- Package manifests outside local source roots modified: `false`
- Lockfiles outside local source roots modified: `false`
- Graphify local frozen artifacts unavailable in this worktree: `true`
- Graphify commands executed: `0`
- Graphify files modified: `0`
- Graphify files copied from dirty checkout: `0`

## Residue Validation

- Temporary clones: `0`
- Temporary archives: `0`
- Temporary extraction roots: `0`
- Temporary acquisition helpers retained: `0`
- Nested Git entries: `0`
- `node_modules`: `0`
- Virtual environments created: `0`
- Running source processes: `0`
- Containers attributable to P15.U0: `0`
- Source executions: `0`
- Dependency installations: `0`

## Git Boundary

- Index empty: `true`
- Staged files: `none`
- `git add`: `0`
- `git commit`: `0`
- `git push`: `0`
- `git stash`: `0`
- `git reset`: `0`
- `git clean`: `0`
- `git worktree`: `0`
- Agent-created commits: `0`
- Agent pushes: `0`

## P15.U Handoff

P15.U0 locks local ignored immutable source references only. It does not approve Hermes Agent 0.19.0 adoption, Hermes Workspace 2.3.0 adoption, runtime migration, dependency installation, container startup, OAuth, provider calls, or inference.

Sequencing:

- P15.U0 is ready for human review and commit of the governance record only.
- P15.U remains blocked until P15.U0 is committed.
- P15.1A remains paused.
- P15.4 remains paused.
- Live OAuth remains unauthorized.
- Provider calls remain unauthorized.
