# I-04 - Provider / Adapter Layer

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Provider / Adapter Layer |
| Ticket | I-04 |
| Status | Accepted minimal provider / adapter layer implementation |
| Date | 2026-07-02 |
| Scope | Create the first minimal governed provider/adapter metadata layer for AGENT PLATFORM / Siamese. |
| Authority | Minimal provider / adapter metadata layer only, not provider/adapter activation. |
| Related documents | I-00, I-01, I-02, I-03, IR-A, IR-06, IR-04, S-series, V-series, H-series, P-A, `.gitignore`, README.md, Siamese Product Vision |
| Implementation target | Exact provider/adapter files under `3_platform/_governed_skeleton/integrations/provider_adapter_layer/` |

## 2. Purpose
I-00 created only the governed skeleton. I-01 added a metadata-only validation registry. I-02 added a metadata-only security/access evaluator. I-03 added a metadata-only context pack runtime. I-04 adds the first minimal provider/adapter metadata layer. I-04 does not activate providers. I-04 does not create API clients. I-04 does not call network. I-04 does not authenticate. I-04 does not start I-05.

## 3. Provider / Adapter Layer Definition
A Provider / Adapter Layer is a minimal in-memory metadata layer for provider descriptors, adapter descriptors, capabilities, activation blockers, limitations, evidence references, and review posture.

Provider registration is not provider activation. Adapter registration is not adapter activation. Capability registration is not tool execution. Provider metadata is not provider permission. Adapter metadata is not implementation readiness. Credential reference is not credential access. Network-required metadata is not network approval. MCP adapter metadata is not MCP activation.

## 4. Decision Summary
Create exact provider/adapter implementation files only. Create one pure Python module. Create no package manifests. Create no tests. Create no runtime service. Create no persistence. Create no dependencies. Preserve source tracking boundaries. Preserve provider/API/MCP activation blockers. Preserve existing `3_platform` sibling quarantine. I-05 may proceed only after explicit instruction.

## 5. Authority Boundary
| actor | authority |
| --- | --- |
| Governance | Decides provider activation. |
| Security | Constrains credentials, network, and data exposure. |
| Validation | Evaluates evidence. |
| Provider/adapter layer | Records metadata only. |
| Git | Records artifacts but does not approve provider/adapter status. |
| Agent | Cannot stage, commit, push, execute, install, publish, authenticate, call providers, or start I-05. |

## 6. Source Boundary
I-00 skeleton is the implementation base. I-01 registry remains metadata-only. I-02 evaluator remains metadata-only. I-03 context runtime remains metadata-only. IR-A blockers remain inherited. IR-06 provides provider/adapter/MCP activation boundaries. H-series provides harness/provider/tool/MCP boundaries. S-series provides local-only/security/access boundaries. V-series provides evidence/proof boundaries. Raw `3_platform` siblings are not inspected. Product source remains local-only. Secrets and credentials are not inspected.

## 7. Exact Target Scope
Files created: `0_architecture/implementation/agent_platform_provider_adapter_layer.md`, `3_platform/_governed_skeleton/integrations/provider_adapter_layer/README.md`, `3_platform/_governed_skeleton/integrations/provider_adapter_layer/PROVIDER_ADAPTER_BOUNDARY.md`, `3_platform/_governed_skeleton/integrations/provider_adapter_layer/PROVIDER_ADAPTER_CONTRACT.md`, and `3_platform/_governed_skeleton/integrations/provider_adapter_layer/provider_adapter_layer.py`.

Directory created only as needed: `3_platform/_governed_skeleton/integrations/provider_adapter_layer/`. No sibling paths are in scope.

## 8. Implementation File Contract
`provider_adapter_layer.py` contains one minimal import-side-effect-free Python standard-library module. It may define provider kinds, adapter kinds, activation statuses, provider descriptors, adapter descriptors, adapter capabilities, and an in-memory provider/adapter layer. It must not persist files, read files, write files, access process variables, call network, spawn processes, import external packages, approve governance decisions, activate providers, activate adapters, activate MCP, execute validation, enforce security, or inspect credentials.

## 9. Provider Descriptor Contract
Required fields are `provider_id`, `name`, `provider_kind`, `description`, `activation_status`, `auth_required`, `network_required`, `data_exposure_risk`, `credential_refs`, `evidence_refs`, `limitations`, `blockers`, `created_at`, and `review_required`. Provider kinds include LLM, cloud, storage, identity/auth, package registry, telemetry/analytics, hosting/deployment, simulation solver, Omniverse Nucleus, data ingestion, notification, local service, and unknown providers. Activation statuses are `metadata_only`, `blocked`, `needs_review`, `activation_not_approved`, and `rejected_for_scope`. `auth_required=True` or `network_required=True` requires review and blockers. Credential refs are metadata IDs only.

## 10. Adapter Descriptor Contract
Required fields are `adapter_id`, `provider_id`, `name`, `adapter_kind`, `description`, `activation_status`, `allowed_scope`, `forbidden_scope`, `evidence_refs`, `limitations`, `blockers`, `created_at`, and `review_required`. Adapter kinds include provider API, local tool, shell command, file system, Git, validation, security, product backend, Omniverse, EnergyPlus, web, desktop, CLI, MCP, and unknown adapters. Adapter registration is metadata only and not activation.

## 11. Adapter Capability Contract
Required fields are `capability_id`, `adapter_id`, `name`, `description`, `activation_status`, `input_classes`, `output_classes`, `side_effects`, `network_behavior`, `credential_behavior`, `evidence_refs`, `limitations`, `blockers`, `created_at`, and `review_required`. Capability registration is metadata only and not tool execution. Capabilities with side effects require review and blockers. Evidence references are metadata IDs only.

## 12. Documentation File Contract
`README.md` describes purpose, current status, representable metadata, non-approval boundaries, IR-06 relationship, security/access evaluator relationship, context pack runtime relationship, product relationship, Git/source tracking relationship, future route, and stop rules. `PROVIDER_ADAPTER_BOUNDARY.md` describes allowed and forbidden implementation. `PROVIDER_ADAPTER_CONTRACT.md` describes descriptor and capability fields, provider kinds, adapter kinds, activation statuses, credential reference rules, network/auth rules, evidence reference rules, blocker rules, limitation rules, review-required rule, and non-activation semantics.

## 13. Source Tracking / Git Boundary
Only exact I-04-created files may be considered for exact-path staging after human review. No broad source tracking is approved. Existing `3_platform` sibling contents remain not trackable. `.gitignore` is unchanged. No force-add is authorized. No `git add .`.

## 14. Dependency Boundary
No dependencies are adopted. No package manifests are created. No lockfiles are created. No package managers are run. Pure Python standard library only. Provider SDKs and client libraries are not adopted.

## 15. Security / Credential Boundary
No credential reading occurs. No auth flow occurs. No provider config is created. Credential references are metadata IDs only. `auth_required=True` requires review and blockers. Secrets and credentials remain excluded.

## 16. Network / API / MCP Boundary
No network is used. No API calls occur. No MCP activation occurs. No provider activation occurs. No tool execution occurs. MCP adapter kind is metadata only.

## 17. Validation Boundary
No validation execution occurs. No validation/security enforcement runtime is created. Provider/adapter metadata may be represented later in the validation registry as metadata only.

## 18. Runtime / Agent / Context Boundary
No runtime service is created. No agent runtime is created. No context runtime expansion is created. No tools are executed. Context inclusion is not permission to transmit provider data.

## 19. Cognitive Semantic System Boundary
Cognitive Semantic System name remains accepted. Substrate remains deferred. Graph remains candidate only. Graphify remains evidence only, not authority. The provider/adapter layer does not decide substrate.

## 20. Product Boundary
Products remain inactive. Product source remains local-only. Product provider/adapter metadata may be represented later as metadata only. Product integrations are not executed or activated. EnergyPlus, OpenStudio, Omniverse, Nucleus, Web, Desktop, and CLI integrations are not activated.

## 21. Created Files Register
| file | type | purpose | contains code? | executable? | dependency impact? | future owner |
| --- | --- | --- | --- | --- | --- | --- |
| `0_architecture/implementation/agent_platform_provider_adapter_layer.md` | Markdown | I-04 record | no | no | none | governance/integrations |
| `3_platform/_governed_skeleton/integrations/provider_adapter_layer/README.md` | Markdown | layer overview | no | no | none | integrations |
| `3_platform/_governed_skeleton/integrations/provider_adapter_layer/PROVIDER_ADAPTER_BOUNDARY.md` | Markdown | layer boundary | no | no | none | integrations/security |
| `3_platform/_governed_skeleton/integrations/provider_adapter_layer/PROVIDER_ADAPTER_CONTRACT.md` | Markdown | descriptor contract | no | no | none | integrations |
| `3_platform/_governed_skeleton/integrations/provider_adapter_layer/provider_adapter_layer.py` | Python | in-memory provider/adapter metadata layer | yes | no runtime service | stdlib only | integrations |

## 22. Non-created Artifacts Register
| artifact | status | future route |
| --- | --- | --- |
| provider client | not created | activation/dependency gate |
| API client | not created | activation gate |
| provider config | not created | security/config gate |
| credential store | not created | security gate |
| adapter runtime | not created | runtime gate |
| MCP server/config | not created | MCP gate |
| tests | not created | future test gate |
| scripts/tools | not created | future tool gate |
| CI | not created | future CI gate |
| package manifests | not created | dependency gate |
| product source | not copied | product governance |
| CSS prototype | not created | CSS governance and I-07 |

## 23. I-04 Gate Checklist
| gate | pass condition | current result | blocker if failed |
| --- | --- | --- | --- |
| I-00 exists | skeleton record exists | pass | stop |
| I-01 exists | registry record exists | pass | stop |
| I-02 exists | security/access record exists | pass | stop |
| I-03 exists | context runtime record exists | pass | stop |
| exact target files absent before creation | no overwrite | pass | stop |
| exact provider/adapter path under governed skeleton | path is scoped | pass | stop |
| Python stdlib only | module imports stdlib only | pass | stop |
| no package manifests | none created | pass | stop |
| no tests | none created | pass | stop |
| no execution | no module/provider/test execution | pass | stop |
| no dependencies adopted | none adopted | pass | stop |
| no credentials inspected | none inspected | pass | stop |
| no network/API calls | none performed | pass | stop |
| no provider/API/MCP activation | none activated | pass | stop |
| no existing `3_platform` sibling approval | siblings uninspected/unapproved | pass | stop |
| I-05 not started | no I-05 artifact | pass | stop |

## 24. Residual Risk Register
| risk | severity | mitigation | route |
| --- | --- | --- | --- |
| no provider runtime | blocker | keep metadata-only scope explicit | future activation gate |
| no adapter runtime | blocker | runtime gate | future |
| no credential store | blocker | security gate | future |
| no API client | blocker | activation/dependency gate | future |
| no MCP implementation | blocker | MCP gate | future |
| no tests | major_gap | future test gate | future |
| no persistence | major_gap | keep in-memory scope explicit | future persistence gate |
| no dependency review for future expansion | blocker | dependency gate | future |
| no source tracking broad approval | blocker | exact-path review only | governance |
| existing `3_platform` siblings unknown | blocker | keep quarantine | future classification |
| product integrations inactive | blocker | product governance | future |
| CSS substrate deferred | blocker | CSS governance | I-07 |

## 25. Blocker Register
| blocker | stop behavior | required future action | blocks broad implementation? |
| --- | --- | --- | --- |
| need provider activation | stop | activation gate | yes |
| need adapter execution | stop | runtime gate | yes |
| need credential access | stop | security approval | yes |
| need network/API call | stop | activation approval | yes |
| need MCP activation | stop | MCP gate | yes |
| need tests | stop | test gate | yes |
| need persistence | stop | persistence gate | yes |
| need dependency | stop | dependency review | yes |
| need source tracking beyond exact files | stop | tracking gate | yes |
| need product integration execution | stop | product governance | yes |
| need CSS substrate | stop | CSS governance | yes |
| I-05 scope pressure | stop | finish I-04 only | yes |

## 26. Incident Handling
Incidents include target overwrite, dependency import, file/network/process-variable access, credential inspection, auth flow, API/network call, provider activation, adapter execution, MCP activation, package manifest creation, test execution, product source inspection, existing `3_platform` inspection, Git mutation, or I-05 started.

Response: STOP, report safe metadata only, do not continue adjacent work, and require human/security/governance decision.

## 27. I-04 Invariants
| id | invariant |
| --- | --- |
| I04-001 | Provider/adapter layer is metadata-only. |
| I04-002 | Provider registration is not provider activation. |
| I04-003 | Adapter registration is not adapter activation. |
| I04-004 | Capability registration is not tool execution. |
| I04-005 | Credential references are metadata only. |
| I04-006 | Network-required metadata is not network approval. |
| I04-007 | MCP adapter metadata is not MCP activation. |
| I04-008 | No external dependencies are adopted. |
| I04-009 | No package manifests or lockfiles are created. |
| I04-010 | No tests/scripts/tools/CI are created. |
| I04-011 | No provider/API/MCP activation occurs. |
| I04-012 | Existing 3_platform contents remain uninspected and unapproved. |
| I04-013 | Product source remains local-only. |
| I04-014 | Cognitive Semantic System substrate remains deferred. |
| I04-015 | Validation evaluates; governance decides. |
| I04-016 | I-04 stops before I-05. |

## 28. Anti-patterns
Anti-patterns: provider metadata as provider activation; adapter metadata as adapter implementation; capability metadata as tool execution; credential reference as credential access; network-required field as network approval; MCP adapter as MCP activation; provider need as dependency adoption; product integration metadata as product activation; package manifest as harmless; existing `3_platform` as approved source; starting I-05 inside I-04; `git add .`.

## 29. Readiness For I-05
I-05 - Agent Runtime Boundary is ready after explicit instruction if I-04 provider/adapter layer exists; only exact I-04 files were created; layer is metadata-only and in-memory; no provider/API/MCP activation occurred; no network/auth/credential use occurred; no dependencies were adopted; no source tracking was broadly approved; existing `3_platform` contents remain uninspected and unapproved; and no product activation, CSS substrate decision, publication, Git mutation, or broad implementation is implied.

Do not create I-05.

## 30. Final Verdict
I-04 created the exact architecture record, provider/adapter documentation, provider/adapter contract, and one minimal pure-stdlib in-memory provider/adapter metadata layer. I-04 did not activate providers. I-04 did not create or activate adapters. I-04 did not call APIs or network. I-04 did not authenticate or inspect credentials. I-04 did not activate MCP. I-04 did not create package manifests or lockfiles. I-04 did not adopt dependencies. I-04 did not create tests, scripts, tools, or CI. I-04 did not approve source tracking broadly. I-04 did not inspect or approve existing `3_platform` contents. I-04 did not decide CSS substrate.

Blocked items remain: provider activation, adapter execution, credential access, network/API calls, MCP activation, tests, persistence, dependency adoption, package manifests, source tracking beyond exact files, product integration execution, product activation, existing `3_platform` approval, CSS substrate decision, publication, staging, commit, push, and I-05. I-05 is ready after explicit instruction only.
