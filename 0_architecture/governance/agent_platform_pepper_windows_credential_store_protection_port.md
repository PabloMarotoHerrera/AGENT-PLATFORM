# P15.C1 - Pepper Windows Credential Store Protection Port

Status: P15.C1 controlled semantic forward-port ready with constraints.

Final verdict: `hermes_0_19_pepper_windows_credential_store_protection_port_ready_with_constraints`

## Ticket Authority

P15.C1 forward-ports the Windows credential-store DACL protection semantics from the legacy P15.1A source worktree into canonical Pepper while preserving Pepper/Hermes 0.19 credential-pool behavior.

P15.C1 does not repair the duplicated credential-store root, does not modify `2_products/hermes-agent/**`, does not run Graphify, does not install dependencies, does not start OAuth, provider, inference, worker, Docker or remote-host activity, and does not stage, commit, merge, rebase, reset, clean, stash, push or tag.

## Active Authority

| Field | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT PLATFORM` |
| Branch | `p15.cleanup-canonicalization` |
| HEAD | `da5deea2db860e8b50c805a9d2b8ed27495c5627` |
| Upstream tracking ref | `da5deea2db860e8b50c805a9d2b8ed27495c5627` |
| HEAD equals upstream | `true` |
| Product root | `2_products/pepper-agent` |
| Upstream project | `Hermes Agent` |
| Upstream version | `0.19.0` |
| Upstream commit | `3ef6bbd201263d354fd83ec55b3c306ded2eb72a` |
| Pepper canonical flag | `false` |
| Pepper candidate flag | `true` |

## Source Evidence

| Field | Value |
| --- | --- |
| Legacy source worktree | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15.1A` |
| Legacy source branch | `p15.1a-windows-protection` |
| Legacy source HEAD | `fea7d3963a598b848768671e00d5bad8065a4421` |
| Preserved inventory | `C:/Users/pablo/OneDrive/Escritorio/P15.1A-WINDOWS-PROTECTION-BACKUP/P15.C1-INVENTORY` |
| Source candidate files | `6` |
| Source hash mismatches after port | `0` |

The legacy source worktree retained the expected pre-existing status entries:

| Status | Path |
| --- | --- |
| `M` | `2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` |
| `M` | `2_products/hermes-agent/hermes_cli/agent_platform/provider_credentials/store.py` |
| `M` | `2_products/hermes-agent/tests/hermes_cli/test_agent_platform_provider_credential_store.py` |
| `??` | `0_architecture/governance/agent_platform_hermes_windows_credential_store_protection_correction.md` |
| `??` | `10_scripts/hermes/agent_platform_windows_credential_store_protection_smoke.py` |
| `??` | `12_tests/hermes/test_agent_platform_windows_credential_store_protection_smoke.py` |

## Semantic Port

| Area | Decision |
| --- | --- |
| Windows preparation | `StoreProtectionBackend.prepare_directory()` and `prepare_file()` now apply a Windows DACL before validation when `os.name == "nt"`. |
| DACL content | Applied SDDL grants full access only to current user, LocalSystem and Builtin Administrators: `D:P(A;;FA;;;current_user)(A;;FA;;;SY)(A;;FA;;;BA)`. |
| DACL inheritance | `SetNamedSecurityInfoW` uses `DACL_SECURITY_INFORMATION | PROTECTED_DACL_SECURITY_INFORMATION` (`0x80000004`). |
| Native boundary | `ctypes.wintypes` signatures cover `HANDLE`, `LPVOID`, `HLOCAL`, `DWORD`, `BOOL`, `LPWSTR` and related pointer outputs. |
| Pepper preservation | Pepper pool-only credential schema, `SecretStr` client-token status derivation and provider singleton rejection are preserved. |
| Deferred repair | `default_openai_codex_credential_store_root()` remains unchanged; duplicated root repair is reserved for P15.C2. |

## Changed Files

| Path | Disposition | SHA-256 |
| --- | --- | --- |
| `2_products/pepper-agent/hermes_cli/agent_platform/provider_credentials/store.py` | modified controlled semantic port | `8ec1f1d1de797a5f590cd474fe31c4dd1523c618244e2c57e80a95b818360c41` |
| `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_credential_store.py` | modified typed fake-WinDLL coverage | `7e2508d6878cb26548e6e5651225526841bdb5cb348696bb4b9fd351a00ae03a` |
| `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` | reconciled two credential-store register rows | `8f694d6b06725d3a913d4e09de26ab47aaabfcb8b6605ee8a30456e7c71b6d7a` |
| `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | added two product-local P15.M8/P15.C1 rows for store/test | `d52b070fa8075d48d2fd3ef7b609205910d61c9313ef175bc0fcdb2bd8627b7c` |
| `10_scripts/hermes/agent_platform_pepper_windows_credential_store_protection_smoke.py` | added bounded native smoke script | `393e3199e16d8f91adf8193e0f37eb531a8e17fa8451e19bdd83e71067340404` |
| `12_tests/hermes/test_agent_platform_pepper_windows_credential_store_protection_smoke.py` | added root smoke unittest | `a54c7eb289e715924333016c56d2fd023dc583e53e5b095c9e9d34123f82e75f` |

TSV schema checks:

| Path | Rows | Columns |
| --- | ---: | ---: |
| `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` | 111 | 18 |
| `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` | 6763 | 8 |

## Validation

| Command or check | Result |
| --- | --- |
| `bash scripts/run_tests.sh tests/hermes_cli/test_agent_platform_provider_credential_store.py -q` in `2_products/pepper-agent` | blocked: no `.venv` or `venv`, and `HERMES_PYTHON` is not a Python with pytest |
| `python -m py_compile ...` for edited/new Python files | passed |
| `python -m pytest -q tests\hermes_cli\test_agent_platform_provider_credential_store.py -p no:cacheprovider` | `10 passed in 0.45s` |
| `python -m pytest -q 12_tests\hermes\test_agent_platform_pepper_windows_credential_store_protection_smoke.py -p no:cacheprovider` | `4 passed in 0.03s` |
| `python 10_scripts\hermes\agent_platform_pepper_windows_credential_store_protection_smoke.py --format json` | `status=passed`; verdict `pepper_windows_credential_store_protection_smoke_passed`; synthetic cleanup removed; provider calls `0`; credential operations `0`; OAuth attempts `0`; real auth-store reads/writes `0` |
| `python 10_scripts\governance\pepper_baseline_integrity.py --repo-root . --product-root 2_products\pepper-agent --mode all --format json` | committed HEAD authority unchanged: candidate `f3b4bdd5ae57ad69fad41c3cf9c0ce39ac92fc846578f2cc14e8aa4c6f465c91`, payload `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c`, baseline `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |
| `python -m unittest discover -s 12_tests\governance -p test_pepper_baseline_integrity.py` | `Ran 14 tests`; `OK` |
| `git diff --check` | clean |
| Active branch/HEAD/upstream check | branch `p15.cleanup-canonicalization`; HEAD and upstream both `da5deea2db860e8b50c805a9d2b8ed27495c5627` |
| Source inventory hash check | `source_candidate_files=6`; `source_hash_mismatches=0` |

## Runtime Boundary

| Action | Count |
| --- | ---: |
| OAuth flows | 0 |
| Provider calls | 0 |
| Model list calls | 0 |
| Inference calls | 0 |
| Real credential reads | 0 |
| Real auth-store reads | 0 |
| Real auth-store writes | 0 |
| Workers started | 0 |
| Agents started | 0 |
| Graphify actions | 0 |
| Dependency installs | 0 |
| `2_products/hermes-agent/**` modifications | 0 |
| Git staging by agent | 0 |
| Git commits by agent | 0 |
| Git pushes by agent | 0 |

## Final Statement

P15.C1 is ready for human review with constraints. Pepper now applies and validates a protected Windows credential-store DACL through typed native security handles while preserving Hermes 0.19 Pepper credential-pool semantics. The duplicated credential-store root remains deliberately unchanged for P15.C2.
