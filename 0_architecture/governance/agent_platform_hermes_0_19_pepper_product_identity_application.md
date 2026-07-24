# P15.M6 - Pepper Product Identity Application

Status: P15.M6 Pepper product identity applied with constraints.

Final verdict: `hermes_0_19_pepper_product_identity_application_ready_with_constraints`

## Ticket Authority

P15.M6 applies the bounded Pepper product identity foundation to the Hermes
Agent 0.19.0-derived editable product baseline. It establishes credential-free
product configuration, protected configuration transport, text-first shell
branding, semantic token aliases, fail-closed extension resolution, protected
`/agent-platform/**` namespace handling, upstream attribution, legal notice and
modification-register rows.

P15.M6 does not activate P13 product routes, Desktop, Workspace, provider
runtime behavior, credential behavior, package identities, public branding,
binary publication, dashboard bundle publication or container publication.

## Pre-Edit Gate

Required P15M gate checks were performed before any edits:

| Check | Result |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| HEAD | `3af2e51bef4a03086d404619a96bbf5bb366b468` |
| origin/p15.m-hermes-0.19-migration | `3af2e51bef4a03086d404619a96bbf5bb366b468` |
| HEAD equals branch remote | `true` |
| Index empty before edits | `true` |
| Staged files before edits | `0` |
| Tracked worktree clean before edits | `true` |
| Prerequisite verdict committed | `hermes_0_19_integrated_interaction_surface_reconciliation_ready_with_constraints` |

No files or uncommitted state were copied from `AGENT-PLATFORM-P15U`.

## Bound Product Identity

| Field | Value |
| --- | --- |
| Product ID | `pepper` |
| Product display name | `Pepper` |
| Product version | `0.1.0-dev` |
| Upstream product name | `Hermes Agent` |
| Upstream version | `0.19.0` |
| Upstream tag | `v2026.7.20` |
| Upstream commit | `3ef6bbd201263d354fd83ec55b3c306ded2eb72a` |
| Product UI feature | `agent_platform.product_ui = disabled` |
| Extension modules | `[]` |

## Product Changes

| Path | Disposition |
| --- | --- |
| `2_products/pepper-agent/hermes_cli/agent_platform/product_config.py` | added validated backend product identity contract |
| `2_products/pepper-agent/hermes_cli/web_server.py` | added protected read-only `GET /api/agent-platform/product-configuration` endpoint |
| `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_product_config.py` | added backend product configuration tests |
| `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_product_routes.py` | added integrated route/auth tests |
| `2_products/pepper-agent/web/src/agent-platform/product-config.ts` | added frontend wire parser and loader |
| `2_products/pepper-agent/web/src/agent-platform/product-config-context.ts` | added product configuration context |
| `2_products/pepper-agent/web/src/agent-platform/product-config-provider.tsx` | added provider and semantic token CSS import |
| `2_products/pepper-agent/web/src/agent-platform/product-config.test.ts` | added frontend parser/loader tests |
| `2_products/pepper-agent/web/src/agent-platform/design-system/brand.ts` | added product/upstream brand projection |
| `2_products/pepper-agent/web/src/agent-platform/design-system/tokens.ts` | added semantic token catalog |
| `2_products/pepper-agent/web/src/agent-platform/design-system/tokens.css` | added semantic CSS aliases over existing theme variables |
| `2_products/pepper-agent/web/src/agent-platform/design-system/index.ts` | added bounded design-system exports |
| `2_products/pepper-agent/web/src/agent-platform/design-system/design-system.test.ts` | added design-system and disabled activation tests |
| `2_products/pepper-agent/web/src/agent-platform/shell/brand-lockup.tsx` | added text-first product/upstream lockup |
| `2_products/pepper-agent/web/src/agent-platform/shell/navigation.ts` | added semantic grouping and protected namespace filtering |
| `2_products/pepper-agent/web/src/agent-platform/shell/index.ts` | added bounded shell exports |
| `2_products/pepper-agent/web/src/agent-platform/shell/shell.test.tsx` | added shell branding/navigation tests |
| `2_products/pepper-agent/web/src/agent-platform/extensions.ts` | added empty fail-closed product extension registry and resolver |
| `2_products/pepper-agent/web/src/agent-platform/extensions.test.ts` | added empty-registry and resolver tests |
| `2_products/pepper-agent/web/src/main.tsx` | added pre-mount product configuration load and provider wrapping |
| `2_products/pepper-agent/web/src/App.tsx` | added brand lockup, semantic navigation grouping, empty registry composition and protected plugin filtering |
| `2_products/pepper-agent/THIRD_PARTY_NOTICES.md` | added Pepper third-party notice and distribution constraints |
| `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` | appended P15.M6 register rows for product divergence authority |

## Governance Artifacts

| Path | Rows | Columns | SHA-256 |
| --- | ---: | ---: | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_pepper_branding_manifest.tsv` | 16 | 17 | `fc691e10c3d53c6dbc20f35ef9090dd0c2e64b14e60a4f9d5302b97380bc23d2` |
| `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` | 22 | 18 | `c8c5e4b7487bc11c6c2f32f998dfe3b44288184cd626c08c50d3793a3eef293e` |

The modification register is intentionally not self-hashed by a row in itself;
it remains the control file for product divergence rows.

The branding manifest records use `record_id` values that match the applicable
P15.M6 product modification IDs. Test files and the modification-register
control file are excluded from branding/application evidence rows because they
validate or govern product mutations but do not themselves apply product
identity, visible branding, semantic design, shell composition, route transport
or legal notice text.

## Legal Notice Boundary

`2_products/pepper-agent/THIRD_PARTY_NOTICES.md` records Pepper identity,
Hermes Agent 0.19.0 attribution, upstream repository/tag/commit, root MIT
license preservation, Apache-2.0 and NOTICE preservation, included MIT plugin
and skill references, excluded PowerPoint material, dependency-license
uncertainty, Desktop/dashboard bundle/container restrictions, trademark and
branding limits, provider-service terms separation, preserved license-file
locations and Pepper modification attribution.

The notice does not replace license files, claim legal certification, imply
Nous Research endorsement or authorize public binary, dashboard bundle or
container distribution.

## Validation

| Command | Result |
| --- | --- |
| `python -c "import py_compile; py_compile.compile('hermes_cli/agent_platform/product_config.py', cfile=r'C:\Users\pablo\AppData\Local\Temp\opencode\p15m_product_config.pyc', doraise=True); py_compile.compile('hermes_cli/web_server.py', cfile=r'C:\Users\pablo\AppData\Local\Temp\opencode\p15m_web_server.pyc', doraise=True)"` | passed |
| `set PYTHONDONTWRITEBYTECODE=1&& pytest -q tests/hermes_cli/test_agent_platform_product_config.py -p no:cacheprovider` | `10 passed in 0.64s` |
| `python 10_scripts/governance/pepper_baseline_integrity.py --repo-root . --product-root 2_products/pepper-agent --mode all --format json` | HEAD candidate, payload and baseline record identities matched required values |
| `python -m unittest discover -s 12_tests/governance -p test_pepper_baseline_integrity.py` | `Ran 14 tests in 0.003s`; `OK` |
| `git diff --check` | no whitespace errors; emitted CRLF normalization warnings for existing modified files |
| `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` width check | `22` rows, fixed `18` columns |
| `AGENT_PLATFORM_MODIFICATIONS.tsv` current hash consistency check | `register_hash_match_count=22` |
| `0_architecture/governance/agent_platform_hermes_0_19_pepper_branding_manifest.tsv` width check | `16` rows, fixed `17` columns |

Blocked local validation:

| Command | Blocking condition |
| --- | --- |
| `set PYTHONDONTWRITEBYTECODE=1&& pytest -q tests/hermes_cli/test_agent_platform_product_config.py tests/hermes_cli/test_agent_platform_product_routes.py -p no:cacheprovider` | `ModuleNotFoundError: No module named 'fastapi'` while collecting route tests |
| `npm run typecheck` in `2_products/pepper-agent/web` | local `tsc` executable unavailable because frontend dependencies are not installed |
| `npx vitest run src/agent-platform/product-config.test.ts src/agent-platform/extensions.test.ts src/agent-platform/design-system/design-system.test.ts src/agent-platform/shell/shell.test.tsx` | local Vitest/Vite dependencies unavailable; config imports `vitest/config` and `@vitejs/plugin-react` could not resolve |

No dependency installation was performed by P15.M6.

## Runtime Boundary

| Action | Count |
| --- | ---: |
| Provider calls | 0 |
| OAuth flows | 0 |
| Credential reads | 0 |
| Inference calls | 0 |
| Runtime adapter activation | 0 |
| Desktop activation | 0 |
| Workspace import or activation | 0 |
| Docker or container execution | 0 |
| WSL mutation | 0 |
| Package identity changes | 0 |
| P13 route activation | 0 |
| Git staging by agent | 0 |
| Git commits by agent | 0 |
| Git pushes by agent | 0 |

## Rollback

If P15.M6 is rejected before commit, remove the added product-owned
`agent-platform` files and `THIRD_PARTY_NOTICES.md`, restore
`2_products/pepper-agent/hermes_cli/web_server.py`,
`2_products/pepper-agent/web/src/main.tsx` and
`2_products/pepper-agent/web/src/App.tsx` to their recorded baseline source
SHA-256 values, and restore `AGENT_PLATFORM_MODIFICATIONS.tsv` to the prior
header-only file. Remove the two P15.M6 governance artifacts.

## Final Statement

P15.M6 is ready for human review with constraints. Pepper identity and upstream
attribution are applied through bounded product-owned seams; the P13 product UI
remains disabled; no P13 routes or extension modules are registered; Desktop and
Workspace remain inactive; provider/runtime/credential behavior is unchanged;
public branding and distribution remain blocked pending separate authorization.
