# AGENT PLATFORM Hermes Credential Delivery Boundary

Status: P15.1 candidate reconciled after `P15.1-CREDENTIAL-DELIVERY-BLOCKED`.

Final verdict: `hermes_openai_codex_credential_delivery_boundary_ready_with_constraints`.

## Dynamic Start

- Dynamic start SHA: `71a982b05a0d025055343cda84eec2258b1bfca3`.
- Branch: `main`.
- `HEAD == origin/main`: true at dynamic start.
- P15.0 prerequisite: `0_architecture/governance/agent_platform_hermes_provider_model_strategy.md` with `hermes_provider_model_strategy_ready_with_constraints`.
- P15.0 selected provider: `openai-codex`.
- P15.0 selected auth: `chatgpt_oauth`.
- P15.0 selected endpoint: `https://chatgpt.com/backend-api/codex`.
- P15.0 selected model: `gpt-5.5`.

## Candidate Set

Authorized candidate paths: 13.

- `0_architecture/governance/agent_platform_hermes_credential_delivery_boundary.md`
- `10_scripts/hermes/agent_platform_openai_codex_oauth_boundary.py`
- `12_tests/hermes/test_agent_platform_openai_codex_oauth_boundary.py`
- `2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv`
- `2_products/hermes-agent/hermes_cli/agent_platform/provider_credentials/__init__.py`
- `2_products/hermes-agent/hermes_cli/agent_platform/provider_credentials/contracts.py`
- `2_products/hermes-agent/hermes_cli/agent_platform/provider_credentials/store.py`
- `2_products/hermes-agent/hermes_cli/agent_platform/provider_credentials/delivery.py`
- `2_products/hermes-agent/hermes_cli/agent_platform/provider_credentials/oauth_acquisition.py`
- `2_products/hermes-agent/tests/hermes_cli/test_agent_platform_provider_credential_contracts.py`
- `2_products/hermes-agent/tests/hermes_cli/test_agent_platform_provider_credential_store.py`
- `2_products/hermes-agent/tests/hermes_cli/test_agent_platform_provider_credential_delivery.py`
- `2_products/hermes-agent/tests/hermes_cli/test_agent_platform_openai_codex_oauth_acquisition.py`

No other task-specific candidate path is authorized.

## Fixed Store Identity

- Schema version: `PROVIDER_CREDENTIAL_SCHEMA_VERSION = 1`.
- Store ID: `openai-codex.primary`.
- Public provider enum value: `openai_codex`.
- Public auth enum value: `chatgpt_oauth_device`.
- Hermes provider slug: `openai-codex`.
- Provider endpoint: `https://chatgpt.com/backend-api/codex`.
- Maximum credential count: 1.
- Credential-pool rotation: rejected by exact one-entry validation.
- Account switching: rejected by fixed store ID and no merge or overwrite.
- Caller-supplied labels: rejected. The store uses only the fixed internal label `AGENT PLATFORM OpenAI Codex OAuth`.

## Locked Hermes Auth Schema

The governed durable store is an isolated Hermes auth-shaped `auth.json`. It is not merged with a user's existing Hermes auth store.

Exact accepted top-level keys:

- `version`
- `updated_at`
- `active_provider`
- `providers`
- `credential_pool`

Exact accepted provider state:

- `providers.openai-codex.schema_version = 1`
- `providers.openai-codex.credential_store_id = openai-codex.primary`
- `providers.openai-codex.auth_mode = chatgpt`
- `providers.openai-codex.base_url = https://chatgpt.com/backend-api/codex`
- `providers.openai-codex.source = agent-platform:chatgpt_oauth_device`
- `providers.openai-codex.label = AGENT PLATFORM OpenAI Codex OAuth`
- `providers.openai-codex.last_refresh`
- `providers.openai-codex.expires_at`
- `providers.openai-codex.tokens.access_token`
- `providers.openai-codex.tokens.refresh_token`

Exact accepted pool state:

- `credential_pool.openai-codex` exists.
- It contains exactly one entry.
- The entry ID is `openai-codex.primary`.
- `auth_type = oauth`.
- `source = manual:device_code` for compatibility with the locked Hermes pool schema.
- Pool access and refresh tokens must match provider-state tokens.
- Pool `last_refresh` and `expires_at` must match provider-state values.

Rejected durable-store states:

- unrelated providers;
- missing `openai-codex` provider;
- extra provider-pool keys;
- zero or multiple `openai-codex` pool entries;
- pool token mismatch;
- label mismatch;
- endpoint mismatch;
- existing durable store before promotion.

## Trusted-Root Boundary

No public contract model contains a store root, Hermes home path, lease root, auth JSON path or arbitrary filesystem path.

Filesystem roots are trusted internal composition inputs only:

- durable store root: trusted internal composition input;
- lease root: trusted internal composition input;
- synthetic roots in tests: injected test seams only;
- production runner CLI: no root/path arguments.

These roots must not originate from a credential lease request, CLI argument, frontend, environment-selected arbitrary path, provider response or `RuntimeLaunchRequest`.

## Host-Store Policy

The production runner accepts only `status` and no path arguments. Its fixed host-store policy resolves internally to:

`get_hermes_home() / "agent-platform" / "provider-credentials" / "openai-codex.primary"`

P15.1 validation did not execute production `status` against the real host store. Runner behavior was validated with injected fake status readers and synthetic trusted roots in unit tests.

## Protection Policy

POSIX policy:

- store directories must be mode `0700`;
- auth file must be mode `0600`;
- group and other permissions are rejected;
- symlinks are rejected.

Windows policy:

- reparse points are rejected;
- DACL inspection is required;
- inability to inspect a DACL fails closed;
- allowed allow-ACE principals are limited to the governed policy: current user SID, LocalSystem `S-1-5-18`, and Builtin Administrators `S-1-5-32-544`;
- `Everyone` `S-1-1-0` is rejected;
- `Authenticated Users` `S-1-5-11` is rejected;
- `Users` `S-1-5-32-545` is rejected;
- unknown allow-ACE principals are rejected.

Tests use injected protection backends for synthetic filesystem roots and pure DACL-principal validation for forbidden Windows principals. Production behavior remains fail closed.

## Atomic Promotion

Promotion behavior:

- refuses an existing durable `auth.json` before staging;
- builds an isolated staging store;
- validates the staged JSON against the exact Hermes schema;
- validates exactly one Codex credential;
- validates protection;
- creates the final durable file with exclusive create semantics;
- never merges;
- never overwrites;
- removes staging residue on failure;
- removes a newly created final file if post-write validation fails.

Failure behavior tested: injected staging protection failure leaves no durable `auth.json` and no staging directory.

## Local Clear

Local clear deletes only the local governed durable store after exact schema and protection validation.

Remote OAuth revocation is not performed and not claimed.

Recorded remote revocation status: `not_supported_or_unverified`.

## Lease Policy

Lease constants:

- `maximum_active_leases: 1`
- `maximum_lease_ttl_ms: 900000`
- `minimum_remaining_credential_lifetime_ms: 300000`
- `automatic_refresh: false`
- `refresh_on_lease_acquisition: false`
- `refresh_writeback: false`

Lease behavior:

- second active lease is rejected;
- excessive TTL is rejected;
- expired credential is rejected;
- near-expiry credential is rejected unless it remains valid through lease expiry plus 300000 ms;
- provider mismatch is rejected;
- runtime mismatch is rejected;
- correlation mismatch is rejected;
- public lease reference contains no path and no token;
- internal projection returns `HERMES_HOME` only for trusted runtime composition;
- release requires a marker with the fixed store ID, runtime ID and correlation ID;
- release removes only the exact contained projection subtree;
- sibling paths are preserved;
- no secure deletion guarantee is made.

## OAuth Acquisition Boundary

Locked parser source:

- Parser: `2_products/hermes-agent/hermes_cli/subcommands/auth.py`, `build_auth_parser`, `auth_add` parser definition.
- OpenAI Codex branch: `2_products/hermes-agent/hermes_cli/auth_commands.py`, `auth_add_command`, `if provider == "openai-codex"` branch.

Supported argv shape verified from locked source:

`python -m hermes_cli.main auth add openai-codex --type oauth`

P15.1 acquisition boundary:

- resolves product-local Python from `2_products/hermes-agent/.venv/Scripts/python.exe` on this Windows checkout;
- uses fixed provider `openai-codex`;
- uses fixed OAuth type `--type oauth`;
- supplies no caller-controlled label;
- supplies no endpoint override;
- uses no shell;
- default execution path is dry-run;
- tests use only an injected fake executor.

No OAuth command was run during P15.1 validation.

## No Real-User Imports

P15.1 validation did not:

- start OAuth;
- open a browser;
- display a real device code;
- call `https://chatgpt.com/backend-api/codex`;
- read `~/.codex/auth.json`;
- read the real `~/.hermes/auth.json`;
- read env-carried tokens;
- inspect an OS credential manager;
- start a worker;
- start an agent;
- mutate Graphify;
- stage, commit or push.

## Validation Evidence

Interpreter:

`C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\2_products\hermes-agent\.venv\Scripts\python.exe`

Targeted P15.1 product tests:

- Command: product Python `-m pytest` on the four P15.1 product test files.
- Result: `21 passed`.

Complete committed P14 regression:

- Command: product Python `-m pytest` on 15 `test_agent_platform_runtime_*.py` files.
- Result: `143 passed, 5 skipped`.

Product config/routes regression:

- Command: product Python `-m pytest` on `test_agent_platform_product_config.py` and `test_agent_platform_product_routes.py`.
- Result: `16 passed`.

Runner tests:

- Command: product Python `-m unittest 12_tests.hermes.test_agent_platform_openai_codex_oauth_boundary`.
- Result: `Ran 3 tests`, `OK`.

Import smoke:

- Result: `import_smoke=passed modules=4`.

Contract-only root guard:

- Result: `contract_only_root_guard=passed exported=19`.

Compileall:

- Product candidate compileall: 9 product Python files, passed.
- Runner compileall: 2 Python files, passed.

Ruff:

- Product Ruff check: passed.
- Runner Ruff check: passed.
- Product Ruff format `--check`: 9 files already formatted.
- Runner Ruff format `--check`: 2 files already formatted.

Windows footgun scanner:

- Command: product Python `scripts/check-windows-footguns.py --all`.
- Result: `No Windows footguns found (779 file(s) scanned).`

Register validator:

- rows: 110;
- columns: 18;
- duplicate IDs: 0;
- duplicate paths: 0;
- missing fields: 0;
- hash mismatches: 0;
- P15.1 rows: 9.

Candidate audit:

- authorized candidates: 13;
- unexpected tracked candidates: 0;
- unexpected task-specific untracked candidates: 0;
- missing candidates: 0.

Product inventory:

- current tracked before commit: 6219;
- P15.1 new product files: 9;
- candidate product inventory after commit: 6228.

## Register Reconciliation

`2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` contains exactly nine P15.1 rows:

- `P15.1-001` through `P15.1-009`.

No P15.1 register rows exist for:

- `0_architecture/**`;
- `10_scripts/**`;
- `12_tests/**`.

## Handoff

P15.2 handoff:

- consume pathless lease refs and internal trusted projection details only through governed runtime composition;
- preserve one active credential lease maximum;
- do not add refresh, fallback, rotation or account switching.

P15.4 ownership:

- first live OAuth belongs to P15.4 or later human-approved work;
- P15.1 remains dry-run acquisition only;
- P15.4 must revalidate real OAuth UX, revocation semantics, token expiry extraction and user consent before any live credential use.

## Final Verdict

`hermes_openai_codex_credential_delivery_boundary_ready_with_constraints`
