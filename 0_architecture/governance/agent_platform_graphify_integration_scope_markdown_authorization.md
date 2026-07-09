# Graphify Integration Scope / Markdown Authorization

## 0. Contexto obligatorio

P10 is Graphify Markdown Evidence Integration. P10.0 is the serial opener. P10.0 authorizes conceptual scope only.

P10.0 does not execute Graphify. P10.0 does not modify `.graphifyignore`. P10.0 does not create or inspect Graphify outputs. P10.0 does not import Graphify outputs. P10.0 does not make Graphify authority. P10.0 does not make Graphify source of truth. P10.0 does not make Graphify runtime. P10.0 does not make Graphify Cognitive Semantic System substrate.

Later P10 tickets must preserve this boundary.

Result marker: `graphify_markdown_scope_authorization_ready`.

Core rule:

```text
Graphify = evidence map
Graphify ≠ authority
Graphify ≠ source of truth
Graphify ≠ approval engine
Graphify ≠ runtime
Graphify ≠ Cognitive Semantic System substrate
```

## 1. Tipo

governance

## 2. Objetivo

P10.0 authorizes controlled markdown visibility for Graphify and governed skeleton Python visibility for Graphify in later gated tickets.

P10.0 defines allowed scope, blocked scope, Graphify authority boundary, human approval requirements, future consumers P10.1-P10.R, and non-execution posture.

P10.0 does not execute Graphify, does not run `/graphify`, does not modify `.graphifyignore`, does not modify `.gitignore`, does not inspect external sources, does not inspect generated outputs, does not inspect product/Siamese source, does not inspect secrets or credentials, does not import Graphify outputs, does not create runtime behavior, and does not mutate Git.

## 3. Alcance permitido

`AllowedMarkdownScope`:

- `README.md`
- `0_architecture/**/*.md`

`AllowedPythonScope`:

- `3_platform/_governed_skeleton/**/*.py`

| Scope pattern | Class | Allowed reason | Future consumer | Guardrail |
| --- | --- | --- | --- | --- |
| `README.md` | AllowedMarkdownScope | Repository orientation and governance context. | P10.1-P10.5 | Read-only for later Graphify run; no secrets, no product/Siamese, no generated outputs. |
| `0_architecture/**/*.md` | AllowedMarkdownScope | Architecture/governance markdown evidence. | P10.1-P10.5 | Markdown is architecture/governance only; no scope expansion in-flight. |
| `3_platform/_governed_skeleton/**/*.py` | AllowedPythonScope | Governed MVP-0 skeleton Python evidence. | P10.1-P10.5 | Python is governed skeleton only; no runtime execution. |

Allowed scope remains read-only for any later Graphify run. Allowed scope excludes product/Siamese source, external source, secrets, credentials, generated outputs, raw Graphify outputs, provider configs, token stores, and unapproved artifacts.

## 4. Alcance prohibido

`BlockedSecretScope`:

- `.env`
- `credentials/**`
- `secrets/**`
- provider configs
- token stores
- browser auth
- local credential stores
- API keys

`BlockedExternalSourceScope`:

- `4_external/sources/**`
- `external/sources/**` as legacy path if present
- `4_external/sources/gstack-main/**`
- Graphify source
- Hermes source
- GBrain source
- GStack source
- ECC-main source
- OpenCode source
- Codegraph source

`BlockedGeneratedOutputScope`:

- `9_artifacts/**`
- `graphify-out/**`
- generated outputs not explicitly approved
- raw Graphify outputs
- unreviewed evidence exports

`BlockedProductScope`:

- `2_products/**`
- product/Siamese source
- product adapters
- product data
- product runtime surfaces

| Blocked pattern | Classification | Reason | Risk | Stop rule |
| --- | --- | --- | --- | --- |
| `.env`, `credentials/**`, `secrets/**`, provider configs, token stores, browser auth, local credential stores, API keys | BlockedSecretScope | Secrets and credentials are never included by P10.0. | Credential exposure. | Stop on any request to inspect or include. |
| `4_external/sources/**` | BlockedExternalSourceScope | External source inspection requires separate gates. | Source permission drift. | Stop on any request to inspect, list, enumerate, import, execute, configure, adopt, or include. |
| `external/sources/**` | BlockedExternalSourceScope legacy reference | Legacy root only, not canonical scope. | Legacy path drift. | Stop if used as canonical or included. |
| `4_external/sources/gstack-main/**` | BlockedExternalSourceScope | GStack remains path/class metadata only. | Unauthorized GStack inspection/execution/adoption. | Stop on inspect/list/import/execute/configure/adopt request. |
| `9_artifacts/**` | BlockedGeneratedOutputScope | Generated/artifact surface is not approved input. | Generated output feedback loop. | Stop on inspection/import/tracking request. |
| `graphify-out/**` | BlockedGeneratedOutputScope | Raw Graphify outputs are not input scope. | Generated evidence contamination. | Stop on inspection/import/tracking request. |
| `2_products/**` | BlockedProductScope | Product/Siamese source is outside P10.0. | Product boundary breach. | Stop on product/Siamese source inspection request. |

## 5. Tareas

The P10.0 agent must:

1. Verify P9.0, P9.1, and P9.2 exist.
2. Create only the P10.0 target governance document.
3. Define `GraphifyIntegrationScopeAuthorization`.
4. Define `AllowedMarkdownScope`.
5. Define `AllowedPythonScope`.
6. Define `BlockedSecretScope`.
7. Define `BlockedExternalSourceScope`.
8. Define `BlockedGeneratedOutputScope`.
9. Define `BlockedProductScope`.
10. Define `GraphifyAuthorityBoundary`.
11. Define `GraphifyExecutionBlocker`.
12. Define `GraphifyIgnorePatchBlocker`.
13. Define `GraphifyHumanApprovalRequirement`.
14. Define `GeneratedEvidenceOnly` baseline.
15. Define P10.1-P10.R future consumption rules.
16. Define stop rules.
17. Define created / not created register.
18. Provide exact commit commands.

## 6. Criterios de aceptación

| Criterion | Status |
| --- | --- |
| Target document exists. | satisfied by this document. |
| Allowed markdown scope is explicit. | satisfied. |
| Allowed Python scope is explicit. | satisfied. |
| Blocked secret scope is explicit. | satisfied. |
| Blocked external source scope is explicit. | satisfied. |
| Blocked generated output scope is explicit. | satisfied. |
| Blocked product scope is explicit. | satisfied. |
| Graphify authority boundary is explicit. | satisfied. |
| Graphify execution is explicitly blocked. | satisfied: no Graphify execution. |
| `.graphifyignore` modification is explicitly blocked. | satisfied: no .graphifyignore modification. |
| Graphify rerun is explicitly blocked. | satisfied. |
| Graphify output import is explicitly blocked. | satisfied. |
| Graphify output is classified as generated evidence baseline only. | satisfied: GeneratedEvidenceOnly. |
| Human approval requirements are explicit. | satisfied. |
| P10 future consumption rules are explicit. | satisfied. |
| No extra files created. | satisfied by P10.0 scope. |
| No Graphify execution occurred. | satisfied. |
| No `.graphifyignore` modification occurred. | satisfied. |
| No external source inspection occurred. | satisfied. |
| No product/Siamese inspection occurred. | satisfied. |
| No generated output inspection occurred. | satisfied. |
| No Git mutation occurred. | satisfied. |

## 7. Validación requerida

Do not run tests or validation commands.

Allowed validation is limited to `Test-Path` checks, `Select-String` marker checks, and `git status --short`.

The final response must report files inspected, files created, files modified, commands run, acceptance criteria status, limitations, and next recommended ticket.

## 8. Formato de respuesta esperado

Expected response headings:

- Summary
- Files inspected
- Files created
- Files modified
- Tests/commands run
- P9 prerequisite status
- Pending alignments
- Scope authorization decision
- Allowed markdown scope
- Allowed Python scope
- Blocked secret scope
- Blocked external source scope
- Blocked generated output scope
- Blocked product scope
- Graphify authority boundary
- Graphify execution blocker
- Graphify ignore patch blocker
- Human approval requirements
- Future P10 consumption rules
- Stop rules
- Created / Not Created Register
- Limitations
- Recommended next ticket
- Commit commands

## 9. Restricciones importantes

Graphify evidence is generated evidence only. Graphify evidence may support decisions but may not decide. Canonical governance docs override Graphify. Human approval is required for later execution.

P10.1 must not be treated as already authorized to patch `.graphifyignore` until this document exists. P10.5 must not execute until P10.1-P10.4 are accepted and human approval is present. P10.6/P10.7 must not run before P10.5. P10.R must not run before P10.6/P10.7.

Never recommend git add .

## 10. Stop rules

`GraphifyScopeStopRule`:

- Stop on missing P9.0.
- Stop on missing P9.1.
- Stop on missing P9.2.
- Stop on request to run Graphify.
- Stop on request to run `/graphify`.
- Stop on request to modify `.graphifyignore`.
- Stop on request to inspect external sources.
- Stop on request to inspect `4_external/sources`.
- Stop on request to inspect/list `4_external/sources/gstack-main`.
- Stop on request to inspect product/Siamese source.
- Stop on request to inspect generated outputs.
- Stop on request to inspect `9_artifacts`.
- Stop on request to inspect `graphify-out`.
- Stop on request to inspect secrets.
- Stop on request to inspect credentials.
- Stop on request to inspect `.env`.
- Stop on request to activate provider/API/MCP.
- Stop on request to call external services.
- Stop on request to create adapters.
- Stop on request to create runtime.
- Stop on request to create graph DB.
- Stop on request to create vector DB.
- Stop on request to generate embeddings.
- Stop on request to select Cognitive Semantic System substrate.
- Stop on request to make Graphify authority.
- Stop on request to make Graphify source of truth.
- Stop on request to make Graphify approval engine.
- Stop on request to make Graphify task router.
- Stop on request to make Graphify repo writer.
- Stop on request to activate Git automation.
- Stop on request to mutate Git.
- Stop on request to recommend `git add .`.
- Stop on request to create P10.1+ files in this ticket.

## 11. Dependencies / parallelization notes

P10.0 is serial. P10.0 blocks all P10 tickets.

After P10.0, P10.2, P10.3, and P10.4 may be generated/executed in parallel. P10.1 may be generated after P10.0, but execution is recommended after P10.2 because it modifies `.graphifyignore`. P10.5 depends on P10.1, P10.2, P10.3, and P10.4. P10.6 and P10.7 may run in parallel after P10.5. P10.R depends on P10.6 and P10.7.

P10.0 does not start P10.1. P10.0 does not start P10.2. P10.0 does not start P10.3. P10.0 does not start P10.4. P10.0 does not start P10.5. P10.0 does not start P10.6. P10.0 does not start P10.7. P10.0 does not start P10.R.

## 12. GraphifyScopeDecision

`GraphifyScopeDecision` authorizes scope conceptually. It does not execute Graphify.

```yaml
GraphifyIntegrationScopeAuthorization:
  decision_id: P10.0-graphify-scope-authorization
  decision_label: Graphify Integration Scope / Markdown Authorization
  ticket: P10.0
  allowed_markdown_scope:
    - README.md
    - 0_architecture/**/*.md
  allowed_python_scope:
    - 3_platform/_governed_skeleton/**/*.py
  blocked_secret_scope:
    - .env
    - credentials/**
    - secrets/**
    - provider_configs
    - token_stores
    - browser_auth
    - local_credential_stores
    - API_keys
  blocked_external_source_scope:
    - 4_external/sources/**
    - external/sources/**
    - 4_external/sources/gstack-main/**
  blocked_generated_output_scope:
    - 9_artifacts/**
    - graphify-out/**
  blocked_product_scope:
    - 2_products/**
    - product/Siamese source
  authority_boundary: GraphifyAuthorityBoundary
  execution_boundary: GraphifyExecutionBlocker
  ignore_patch_boundary: GraphifyIgnorePatchBlocker
  human_approval_required: GraphifyHumanApprovalRequirement
  generated_evidence_classification: GeneratedEvidenceOnly
  future_consumer_tickets:
    - P10.1
    - P10.2
    - P10.3
    - P10.4
    - P10.5
    - P10.6
    - P10.7
    - P10.R
  limitations:
    - conceptual_scope_only
    - no Graphify execution
    - no .graphifyignore modification
    - no generated_output_tracking
    - no source_tracking_expansion
    - no runtime_activation
    - no Git mutation
  stop_rules: GraphifyScopeStopRule
```

`GraphifyScopeSurface` records allowed and blocked path patterns only. Context inclusion is not permission. Source path is not source permission.

## 13. GraphifyAuthorityBoundary

`GraphifyAuthorityBoundary`:

- Graphify is evidence map only.
- Graphify is not authority.
- Graphify is not source of truth.
- Graphify is not approval engine.
- Graphify is not runtime.
- Graphify is not Cognitive Semantic System substrate.
- Graphify cannot override canonical governance docs.
- Graphify cannot approve scope expansion.
- Graphify cannot approve source inspection.
- Graphify cannot approve generated output tracking.
- Graphify cannot approve product/Siamese source access.
- Graphify cannot approve Git mutation.

`GraphifyExecutionBlocker`: no Graphify execution, no `/graphify`, no Graphify rerun, no Codegraph execution, no external tool execution, no runtime activation.

`GraphifyIgnorePatchBlocker`: no `.graphifyignore` modification by P10.0. Later P10.1 may propose an exact patch only after this document exists and under its own gate.

`GeneratedEvidenceOnly`: Graphify output, if later generated under P10 gates, is generated evidence only. It may support decisions but may not decide.

`GraphifyHumanApprovalRequirement`: later execution, `.graphifyignore` modification, output classification, generated evidence import boundary, and closure require explicit scope-bound human approval.

## 14. Future P10 Consumption Rules

| Future ticket | What it consumes from P10.0 | What remains blocked | Required additional gate |
| --- | --- | --- | --- |
| P10.1 | Allowed and blocked scope definitions for `.graphifyignore` patch planning. | Patch is not authorized by P10.0. | Exact patch authorization and review. |
| P10.2 | AllowedMarkdownScope and blocked scope guardrails. | Graphify execution and output inspection. | Markdown Scope Safety Review. |
| P10.3 | GraphifyExecutionBlocker and human approval requirement. | Actual Graphify run. | Controlled Rerun Plan acceptance. |
| P10.4 | GeneratedEvidenceOnly baseline. | Importing or tracking outputs. | Evidence Output Classification acceptance. |
| P10.5 | Complete P10.1-P10.4 gate chain. | Execution before accepted gates and human approval. | First controlled Graphify execution gate. |
| P10.6 | Generated evidence from accepted P10.5 only. | Running before P10.5. | Refreshed evidence report gate. |
| P10.7 | Output import boundary from accepted P10.5/P10.6 only. | Importing raw Graphify outputs as authority. | Evidence import boundary gate. |
| P10.R | P10.6 and P10.7 closure inputs. | Closing P10 before evidence/report/import boundary. | P10 closure gate. |

`GraphifyScopeFutureConsumer`: P10.1-P10.R must preserve P10.0 boundaries unless a later exact ticket explicitly narrows or safely expands scope under human approval.

## 15. Created / Not Created Register

Created:

- `0_architecture/governance/agent_platform_graphify_integration_scope_markdown_authorization.md`

Modified:

- none

Not created / not approved:

- no `.graphifyignore` patch
- no Graphify execution
- no `/graphify` execution
- no Graphify rerun
- no Graphify output import
- no Graphify output tracking
- no generated output tracking
- no source tracking expansion
- no Graphify authority
- no Graphify source of truth
- no Graphify approval engine
- no Graphify runtime
- no Graphify substrate
- no graph DB
- no vector DB
- no embeddings
- no semantic search
- no ontology runtime
- no relationship persistence
- no external source inspection
- no `4_external/sources` inspection
- no GStack inspection/list/import/execute/configure/adopt
- no product/Siamese source inspection
- no secrets inspection
- no credentials inspection
- no provider/API/MCP activation
- no runtime activation
- no autonomous orchestration
- no adapters
- no tool execution
- no agent execution
- no Git mutation

## 16. Recommended Next Ticket

Recommended strict sequence:

- P10.2 - Graphify Markdown Scope Safety Review.
- P10.3 - Graphify Controlled Rerun Plan.
- P10.4 - Graphify Evidence Output Classification.

Recommended actual:

```text
P10.2 - Graphify Markdown Scope Safety Review
```

Do not start P10.2. Do not start P10.3. Do not start P10.4. Do not start P10.1. Do not start P10.5. Do not start P10.6. Do not start P10.7. Do not start P10.R.

## 17. Final Verdict

| Question | Answer |
| --- | --- |
| What did P10.0 create? | `0_architecture/governance/agent_platform_graphify_integration_scope_markdown_authorization.md`. |
| Was P9.0 present? | Yes, at accepted path `0_architecture/governance/agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md`; prompt-listed alias without `p9_` is absent. |
| Was P9.1 present? | Yes. |
| Was P9.2 present? | Yes. |
| What markdown scope was authorized? | `README.md` and `0_architecture/**/*.md`. |
| What Python scope was authorized? | `3_platform/_governed_skeleton/**/*.py`. |
| What secret scope was blocked? | `.env`, `credentials/**`, `secrets/**`, provider configs, token stores, browser auth, local credential stores, and API keys. |
| What external source scope was blocked? | `4_external/sources/**`, `external/sources/**`, `4_external/sources/gstack-main/**`, and external candidate source surfaces. |
| What generated output scope was blocked? | `9_artifacts/**`, `graphify-out/**`, generated outputs not explicitly approved, raw Graphify outputs, and unreviewed evidence exports. |
| What product/Siamese scope was blocked? | `2_products/**`, product/Siamese source, product adapters, product data, and product runtime surfaces. |
| What Graphify authority boundary was defined? | Graphify is evidence map only, not authority, source of truth, approval engine, runtime, Cognitive Semantic System substrate, graph DB, vector DB, architecture decider, task router, repo writer, or scope approver. |
| Did P10.0 execute Graphify? | No. |
| Did P10.0 modify `.graphifyignore`? | No. |
| Did P10.0 inspect external sources? | No. |
| Did P10.0 inspect generated outputs? | No. |
| Did P10.0 inspect product/Siamese source? | No. |
| Did P10.0 inspect secrets or credentials? | No. |
| Did P10.0 import Graphify outputs? | No. |
| Did P10.0 approve generated output tracking? | No. |
| Did P10.0 make Graphify authority/source of truth/approval engine/runtime/substrate? | No. |
| Did P10.0 mutate Git? | No. |
| What tickets can run next? | P10.2, P10.3, and P10.4 may be prepared after P10.0; P10.1 may be generated after P10.0 but patch execution is recommended after P10.2. |
| What is the recommended next ticket? | P10.2 - Graphify Markdown Scope Safety Review. |
