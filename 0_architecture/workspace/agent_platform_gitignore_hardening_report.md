# AGENT PLATFORM .gitignore Hardening Report

Status: GIT-01 hardening report  
Date: 2026-06-28  
Scope: Root `.gitignore` hardening for AGENT PLATFORM local-only policy  
Authority: Git ignore hygiene only. This report does not stage, commit, push, migrate `previusknowledge/`, inspect product or external source code deeply, run external code, install dependencies, authenticate services, start next-phase tickets, or decide the Cognitive Semantic System substrate.

## 1. Purpose

GIT-01 hardens the root `.gitignore` so it better matches the AGENT PLATFORM local-only policy identified by W-A and related W-series documents.

The change addresses two concrete gaps:

| Gap | Resolution |
| --- | --- |
| `previusknowledge/` was policy-local-only but not ignored. | Added `previusknowledge/`. |
| Secrets and credentials were policy-blocked but lacked explicit ignore patterns. | Added explicit environment, key, token, credential, cloud/provider auth, and local auth patterns. |

This ticket is not commit approval. The files remain unstaged until a human explicitly stages and commits them.

## 2. Existing .gitignore Posture

Before GIT-01, `.gitignore` already covered these local-only classes:

| Class | Existing patterns |
| --- | --- |
| OS / Office | `desktop.ini`, `Thumbs.db`, `~$*`, `*.xlsx`, `*.xls` |
| Product candidates | `2_products/` |
| Raw external source snapshots | `4_external/sources/` |
| Data/model/artifact stores | `7_datasets/`, `8_models/`, `9_artifacts/` |
| Runtime/generated outputs | `logs/`, `runs/`, `outputs/`, `tmp/`, `temp/`, `cache/` |
| Python / Node dependency and build material | `__pycache__/`, `*.py[cod]`, `.venv/`, `venv/`, `node_modules/`, `dist/`, `build/` |

The existing posture was mostly aligned with W-series policy, but W-A identified missing enforcement for previous knowledge and explicit secret/credential patterns.

## 3. W-A Gaps Addressed

Mandatory inputs confirmed the following:

| Source | Relevant finding |
| --- | --- |
| `agent_platform_workspace_architecture_audit.md` | `previusknowledge/` is policy-local-only but was not ignored; secrets/credentials were policy-blocked but lacked explicit ignore patterns. |
| `agent_platform_agent_operating_rules.md` | Agents must not stage local-only areas, must not use broad staging, and must never commit secrets or credentials. |
| `agent_platform_workspace_responsibility_map.md` | `previusknowledge/` should remain local-only until governance decides; products, external sources, datasets, models, artifacts, Office files, and runtime outputs remain local-only. |
| `agent_platform_workspace_topology.md` | Local-only topology includes `previusknowledge/`, products, raw external sources, datasets, models, artifacts, generated outputs, runtime logs, Office temp files, secrets, and credentials. |
| `agent_platform_external_source_handling_policy.md` | External source snapshots remain local-only; credentialed execution and provider auth remain blocked without approval. |

GIT-01 addresses the W-A `.gitignore` gaps without weakening existing local-only boundaries.

## 4. Patterns Added

Added previous-knowledge coverage:

```text
previusknowledge/
```

Added explicit secrets and credentials coverage:

```text
.env
.env.*
!.env.example
!.env.template
*.pem
*.key
*.p12
*.pfx
*.cer
*.crt
*.csr
*.jks
*.keystore
id_rsa
id_rsa.*
id_ed25519
id_ed25519.*
*_rsa
*_rsa.*
*_ed25519
*_ed25519.*
secrets/
credentials/
.credential/
.credentials/
*.secret
*.secrets
*.token
*.tokens
*.auth
*.oauth
*.apikey
*.api_key
```

Added cloud, provider, and local auth coverage:

```text
.aws/
.azure/
.gcloud/
.config/gcloud/
.netrc
.npmrc
.pypirc
docker-compose.override.yml
```

Added local environment and IDE cache coverage:

```text
.local/
.cache/
.ipynb_checkpoints/
```

## 5. Patterns Preserved

No existing local-only patterns were removed.

Preserved patterns:

```text
desktop.ini
Thumbs.db
~$*
*.xlsx
*.xls
2_products/
4_external/sources/
7_datasets/
8_models/
9_artifacts/
logs/
runs/
outputs/
tmp/
temp/
cache/
__pycache__/
*.py[cod]
.venv/
venv/
node_modules/
dist/
build/
```

Preservation verdict:

```text
Existing product, external source, dataset, model, artifact, generated output,
runtime, Office, Python, Node, dependency, and build ignore boundaries were
preserved.
```

## 6. Local-Only Areas Now Covered

After GIT-01, `.gitignore` explicitly covers:

| Local-only class | Coverage status |
| --- | --- |
| Previous knowledge migration corpus | Covered by `previusknowledge/`. |
| Product candidates | Covered by `2_products/`. |
| Raw external source snapshots | Covered by `4_external/sources/`. |
| Datasets | Covered by `7_datasets/`. |
| Models/checkpoints | Covered by `8_models/`. |
| Generated artifacts | Covered by `9_artifacts/`, `outputs/`, and related runtime/generated patterns. |
| Runtime logs/runs/temp/cache | Covered by `logs/`, `runs/`, `tmp/`, `temp/`, `cache/`, `.cache/`. |
| Office/OS local files | Covered by `desktop.ini`, `Thumbs.db`, `~$*`, `*.xlsx`, `*.xls`. |
| Secrets/credentials | Covered by environment, key, cert, token, credential, auth, and secret patterns. |
| Cloud/provider/local auth | Covered by `.aws/`, `.azure/`, `.gcloud/`, `.config/gcloud/`, `.netrc`, `.npmrc`, `.pypirc`, `docker-compose.override.yml`. |
| Dependency/build folders | Covered by `.venv/`, `venv/`, `node_modules/`, `dist/`, `build/`, `__pycache__/`. |
| Local environment / IDE caches | Covered by `.local/`, `.cache/`, `.ipynb_checkpoints/`. |

## 7. Remaining Cautions

| Caution | Impact | Handling |
| --- | --- | --- |
| `.gitignore` does not untrack files already tracked by Git. | If sensitive or local-only material were already tracked, ignore rules would not remove it. | Review with exact Git status/diff checks; do not use broad staging. |
| `.env.example` and `.env.template` are intentionally unignored. | Templates can be committed only if they contain placeholders, not real secrets. | Review template contents before committing any template file. |
| Ignore rules reduce accidental staging but do not provide security by themselves. | Secrets can still leak through copied content, tracked files, logs, docs, or screenshots. | Future `S-00 - Security / Access Architecture` should define secure secret handling. |
| Broad staging remains unsafe. | `git add .` can still stage tracked changes or unexpected files. | Use exact file staging only after human approval. |
| This ticket does not migrate or archive `previusknowledge/`. | Previous knowledge remains local migration evidence. | Future migration/archive work requires explicit ticket and governance posture. |

## 8. Validation Result

Validation performed after editing `.gitignore` and before creating this report confirmed:

| Command | Result |
| --- | --- |
| `git status --short` | `.gitignore` modified; this GIT-01 report untracked; no staging performed. |
| `git diff -- .gitignore` | Shows only additions for `previusknowledge/`, secrets/credentials, cloud/provider/local auth, and local cache patterns. |
| `Test-Path .gitignore` | `True` |
| `Test-Path previusknowledge` | `True` |
| `Test-Path 2_products` | `True` |
| `Test-Path 4_external/sources` | `True` |
| `git check-ignore previusknowledge/` | `previusknowledge/` |
| `git check-ignore 2_products/` | `2_products/` |
| `git check-ignore 4_external/sources/` | `4_external/sources/` |
| `git check-ignore 7_datasets/` | `7_datasets/` |
| `git check-ignore 8_models/` | `8_models/` |
| `git check-ignore 9_artifacts/` | `9_artifacts/` |
| `git check-ignore .env` | `.env` |
| `git check-ignore .env.local` | `.env.local` |
| `git check-ignore secrets/test.txt` | `secrets/test.txt` |
| `git check-ignore credentials/test.txt` | `credentials/test.txt` |
| `git check-ignore test.pem` | `test.pem` |
| `git check-ignore test.key` | `test.key` |

Final validation after creating this report confirmed:

| Command | Result |
| --- | --- |
| `Test-Path 0_architecture/workspace/agent_platform_gitignore_hardening_report.md` | `True` |
| `Get-Item 0_architecture/workspace/agent_platform_gitignore_hardening_report.md` | Report exists; final metadata captured in the GIT-01 response. |

## 9. Final Verdict

GIT-01 successfully hardens `.gitignore` against the W-A gaps.

Final verdict:

```text
The root `.gitignore` now matches the current AGENT PLATFORM local-only policy more
closely. `previusknowledge/` is ignored, explicit secrets/credentials and provider
auth patterns are ignored, and existing local-only boundaries remain preserved.
No staging, commit, push, migration, product activation, external source adoption,
or next-phase ticket was performed.
```

Stop rule:

```text
After GIT-01, stop. Do not stage, commit, push, move files, delete files, migrate
previous knowledge, inspect product or external source code deeply, run external
code, install dependencies, authenticate, or start the next ticket.
```
