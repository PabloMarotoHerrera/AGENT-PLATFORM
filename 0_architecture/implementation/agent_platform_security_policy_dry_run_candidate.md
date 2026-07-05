# P5.2 - Security Policy Dry-Run / Enforcement Candidate

## Document Header
| Field | Value |
| --- | --- |
| Title | Security Policy Dry-Run / Enforcement Candidate |
| Ticket | P5.2 |
| Status | Accepted security policy dry-run skeleton candidate |
| Date | 2026-07-05 |
| Scope | Create a controlled, product-independent, non-active security policy dry-run skeleton for AGENT PLATFORM / Siamese. |
| Authority | Inert security dry-run skeleton only, not security enforcement activation, runtime activation, scanner execution, source loading, product source inspection, provider/auth/API/MCP activation, credential use, tool execution, agent execution, live connector activation, GBrain/Hermes/Cadence activation, Graphify adoption, vector DB implementation, embedding generation, graph DB implementation, generated output tracking, source tracking expansion, publication, Git mutation, or Cognitive Semantic System substrate selection. |
| Related documents | P3.BR, P3.3, P3.4, P3.5, P3.R, P3.0, P3.1, P3.2, P2.KR, P2.R, P2.3, P2.2, P2.1, P1.1-P1.5, P0.1-P0.3, G-01, S-03, S-04, CSS ADR/audit, README.md, `.gitignore`, `.graphifyignore`, P5.1/P5.3/P5.7 if present. |
| Output | Security dry-run skeleton candidate. |

Implementation skeleton is not activation. Security enforcement remains non-active.

## Purpose
P5.2 creates the minimal inert security policy dry-run skeleton for AGENT PLATFORM / Siamese. It can represent metadata-only security subjects, controls, deny reasons, dry-run decisions, findings, and dry-run results.

The skeleton may evaluate a caller-supplied `SecuritySubject` object in memory and return `ALLOW_METADATA_ONLY`, `DENY`, or `DEFER` posture. It does not activate enforcement, run scanners, inspect secrets, inspect credentials, read `.env`, read provider configs, call providers, execute tools, load source, inspect product source, write persistence, create telemetry, or trigger runtime behavior.

## Current Posture
| Area | Current posture | P5.2 result |
| --- | --- | --- |
| P5 | Controlled Runtime Implementation phase. | Product-independent skeleton only. |
| Activation | AGENT PLATFORM remains pre-active unless a later gate changes it. | No activation level promotion. |
| P3.BR | P5 eligible only with blockers documented. | P5.2 preserves all blockers. |
| Tool execution | `tool_execution_activation_deferred`. | No tool execution. |
| Provider/auth/API/MCP | `provider_auth_api_mcp_activation_deferred`. | No provider/auth/API/MCP activation. |
| Agent runtime | `agent_runtime_activation_deferred_until_P3.3_P3.4_alignment`. | No agent execution. |
| Security | Security constrains; it does not activate. | Dry-run metadata only. |
| Validation | Validation evaluates; governance decides. | No validation execution. |
| Evidence | Evidence supports; it does not decide. | Evidence refs only. |
| Source classification | Source classification is not source loading permission. | No source loading. |
| Product / Siamese | Siamese is product vision, not product activation. | No product behavior. |
| Graphify | Graphify evidence is supporting generated evidence only, not authority. | No Graphify adoption or raw output inspection. |
| Cognitive Semantic System | Cognitive Semantic System substrate remains deferred. | No substrate selection. |
| GBrain / Hermes / Cadence | Future and inactive. | Not adopted, not executed, not activated. |

## Inputs Reviewed
Only governance, security, Cognitive Semantic System, README, `.gitignore`, and `.graphifyignore` inputs were reviewed. Product source, external source contents, GBrain contents, Hermes source, Graphify implementation source, raw Graphify output, secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, and generated raw outputs were not inspected.

Mandatory inputs reviewed:

| Input | P5.2 use |
| --- | --- |
| P3.BR Activation Decision Reconciliation Closure | Confirms product-independent P5 skeleton eligibility with blockers documented. |
| P3.3 Tool Execution Activation Decision | Preserves tool execution deferred posture. |
| P3.4 Provider/Auth/API/MCP Activation Decision | Preserves provider/auth/API/MCP deferred posture. |
| P3.5 Agent Runtime Activation Decision | Preserves agent runtime deferred posture. |
| P3.R Activation Readiness Reconciliation Closure | Confirms readiness is not activation. |
| P3.0 Controlled Source Classification Readiness | Supplies source classification blockers and path-only posture. |
| P3.1 Validation Execution Readiness | Supplies no-validation-execution boundary and future target posture. |
| P3.2 Security Enforcement Readiness | Supplies dry-run posture, deny conditions, no scanner, no enforcement boundaries. |
| P2.KR Knowledge Architecture Reconciliation Closure | Supplies retrieval, live connector, Cadence, GBrain/Hermes, and substrate boundaries. |
| P2.R Cross-Lane Integration Reconciliation Closure | Supplies reconciled P2 baseline and no unresolved P2 drift. |
| P2.1 Shared Metadata Vocabulary Alignment | Supplies canonical status, blocker, sensitivity, source, and ref vocabulary. |
| P2.2 Cross-Lane Evidence Reference Contract | Supplies EvidenceRef, SourceRef, ValidationRef, SecurityRef, GraphifyRef, and ProductRef semantics. |
| P2.3 Audit / Retention / Rollback Baseline | Supplies retention, rollback, incident, local-only, publication, and tracking blockers. |
| P1.1-P1.5 boundary contracts | Preserve context, provider, tool, agent, and Cognitive Semantic System metadata-only boundaries. |
| P0.1-P0.3 and G-01 | Supply activation gates, validation gate design, and security hardening design. |
| S-03 and S-04 | Supply local-only, secrets, credentials, execution, provider, network, and MCP constraints. |
| CSS ADR/audit | Confirms accepted Cognitive Semantic System name and deferred substrate. |
| README.md | Root workspace orientation. |
| `.gitignore` | Local-only, generated, secrets, credentials, provider auth, and artifact hygiene posture. |
| `.graphifyignore` | Graphify default-deny input boundary and hard exclusions. |

## Dependency Posture
| Dependency | Observation | P5.2 posture |
| --- | --- | --- |
| P5.1 validation runner implementation doc | Absent. | `pending_P5.1_validation_runner_alignment`. |
| P5.3 context assembly implementation doc | Absent. | `pending_P5.3_context_assembly_alignment`. |
| P5.7 audit retention rollback hooks doc | Absent. | `pending_P5.7_audit_retention_rollback_hooks_alignment`. |
| `3_platform/_governed_skeleton/validation/` | Present as path metadata only. | Not inspected or modified. |
| `3_platform/_governed_skeleton/context/` | Present as path metadata only. | Not inspected or modified. |
| `3_platform/_governed_skeleton/audit/` | Absent. | No P5.7 created. |
| `external/sources/gbrain-master` | Absent. | Path/class metadata only if referenced; contents not inspected. |

## Target Files
Created exact target files:

| File | Role |
| --- | --- |
| `3_platform/_governed_skeleton/security/__init__.py` | Import-safe package exports for inert dry-run skeleton. |
| `3_platform/_governed_skeleton/security/models.py` | Metadata-only enums and dataclasses. |
| `3_platform/_governed_skeleton/security/policy.py` | Deny-by-default `SecurityPolicy` and `default_deny_policy`. |
| `3_platform/_governed_skeleton/security/dry_run.py` | Pure in-memory `SecurityDryRunEvaluator`. |
| `0_architecture/implementation/agent_platform_security_policy_dry_run_candidate.md` | P5.2 implementation candidate record. |

## Implementation Scope
P5.2 created only the exact target files. It implemented metadata-only dataclasses/enums, a default deny policy object, and a pure in-memory dry-run evaluator.

The implementation includes no scanners, no enforcement runtime, no secret/credential inspection, no filesystem/network/tool/provider action, no source loading, and no product behavior.

## Explicit Non-Goals
| Non-goal | P5.2 posture |
| --- | --- |
| Active enforcement | Not created. |
| Runtime security middleware | Not created. |
| Scanner | Not created. |
| Secret scanning | Not created. |
| Credential scanning | Not created. |
| Filesystem scan | Not created. |
| Source scan | Not created. |
| Product scan | Not created. |
| Provider/auth config | Not created. |
| Network/MCP/API | Not created. |
| Persistence | Not created. |
| Telemetry | Not created. |
| Audit sink activation | Not created. |
| Validation execution | Not created. |
| Test execution | Not created. |

## Runtime Boundary
The package is import-safe by inspection. `__init__.py` exports types and functions only. No evaluation runs at import time. No file reads, environment inspection, logging handler configuration, persistence, telemetry, scheduler, worker, queue, service, subprocess, network action, or runtime behavior is created.

`SecurityDryRunEvaluator.evaluate()` accepts only a caller-supplied `SecuritySubject` object. It returns metadata objects and does not mutate external state.

## Security Boundary
Security policy remains a constraining metadata layer. P5.2 does not activate security enforcement. P5.2 does not run scanners. P5.2 does not inspect secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, or API keys.

The default policy blocks restricted source classifications, restricted sensitivities, and activation-related flags. Secret and credential values must never be stored in any P5.2 dataclass field.

## Validation Boundary
P5.2 does not run tests, validation, CI, lint, typecheck, builds, scripts, Python execution, package-manager commands, or Graphify. Future validation targets are listed only as future checks.

Validation evaluates; governance decides.

## Source Classification Boundary
`SourceClassification` is metadata only. Source classification is not source loading permission. Path presence is not content inspection permission.

The dry-run policy blocks raw generated output, local-only material, product source, external source, GBrain external candidates, Hermes external candidates, provider config, token store, browser auth, local credential store, environment file, secret or credential material, and unknown classes by default.

## Evidence / Retention / Rollback / Incident Interfaces
EvidenceRef, SourceRef, ValidationRef, SecurityRef, GraphifyRef, and ProductRef remain metadata references only. Evidence supports; it does not decide.

P5.2 creates no runtime logs, telemetry, persistence, audit sink, rollback hook, quarantine action, deletion action, credential rotation, or incident automation. Future retention, rollback, and incident handling must remain metadata-only until exact gates approve otherwise.

## Human Approval Requirements
Any future move from dry-run skeleton to active enforcement, scanner execution, runtime middleware, validation execution, provider/auth/API/MCP activation, source loading, product source inspection, tool execution, agent execution, live connector activation, publication, source tracking expansion, generated output tracking, or Cognitive Semantic System substrate selection requires exact human/governance approval.

AI agents may draft metadata and candidate code but cannot self-approve activation or override blockers.

## Stop Rules
| Stop trigger | Required result |
| --- | --- |
| Any task requires reading `.env`. | Stop. |
| Any task requires inspecting secrets or credentials. | Stop. |
| Any task requires provider config, token store, browser auth, local credential store, or API key access. | Stop. |
| Any task requires source loading beyond exact approved metadata files. | Stop. |
| Any task requires product source inspection. | Stop. |
| Any task requires GBrain/Hermes/Graphify source inspection. | Stop. |
| Any task requires scanner execution. | Stop. |
| Any task requires enforcement activation. | Stop. |
| Any task requires filesystem traversal. | Stop. |
| Any task requires network/API/MCP. | Stop. |
| Any task requires tool or agent execution. | Stop. |
| Any task requires generated output tracking, source tracking expansion, publication, or Git mutation. | Stop. |
| Any task requires selecting Cognitive Semantic System substrate. | Stop. |

## Future Validation Targets
Future validation targets only, not executed by P5.2:

| Target | Purpose |
| --- | --- |
| SecurityPolicy required fields completeness | Check policy object completeness. |
| SecuritySubject required fields completeness | Check evaluated subject shape. |
| SecurityDecisionStatus vocabulary conformance | Check enum vocabulary. |
| Default deny policy invariant | Check `default_deny_policy` blocks by default. |
| No-secret/no-credential guard metadata invariant | Check guard metadata exists without value inspection. |
| Blocked source class guard metadata invariant | Check blocked source classes are represented. |
| Dry-run-only invariant | Check dry-run results do not imply enforcement. |
| No scanner invariant | Check no scanner behavior exists. |
| No filesystem/network/tool/provider side-effect invariant | Check evaluator is pure in-memory by inspection. |
| No runtime activation invariant | Check no runtime behavior is created. |
| No enforcement activation invariant | Check enforcement remains inactive. |
| Product source blocked invariant | Check product source remains blocked. |
| GBrain/Hermes/Cadence inactive invariant | Check future candidates remain inactive. |
| Graphify support-only invariant | Check Graphify remains supporting generated evidence only. |
| Cognitive Semantic System substrate deferred invariant | Check substrate remains deferred. |
| P5.1/P5.3/P5.7 alignment checks | Check optional peer alignment if later created. |

## Created / Not Created Register
Created:

| Path | Status |
| --- | --- |
| `3_platform/_governed_skeleton/security/__init__.py` | Created. |
| `3_platform/_governed_skeleton/security/models.py` | Created. |
| `3_platform/_governed_skeleton/security/policy.py` | Created. |
| `3_platform/_governed_skeleton/security/dry_run.py` | Created. |
| `0_architecture/implementation/agent_platform_security_policy_dry_run_candidate.md` | Created. |

Modified:

| Path | Status |
| --- | --- |
| Existing target files | None existed before P5.2 creation. |
| Other files | None modified. |

Not created / not approved:

| Area | P5.2 result |
| --- | --- |
| Runtime activation | Not created or approved. |
| Security enforcement activation | Not created or approved. |
| Scanner execution | Not created or approved. |
| Validation execution | Not created or approved. |
| Tests / CI / scripts executed | Not executed. |
| Source loading | Not created or approved. |
| Product source inspection | Not created or approved. |
| External source inspection | Not created or approved. |
| GBrain source inspection | Not created or approved. |
| Hermes source inspection | Not created or approved. |
| Graphify source/output inspection | Not created or approved. |
| Provider/auth/API/MCP activation | Not created or approved. |
| Credential use | Not created or approved. |
| Secret inspection | Not performed. |
| Credential inspection | Not performed. |
| `.env` inspection | Not performed. |
| Provider config inspection | Not performed. |
| Token store inspection | Not performed. |
| Browser auth inspection | Not performed. |
| Local credential store inspection | Not performed. |
| API key inspection | Not performed. |
| Tool execution | Not created or approved. |
| Agent execution | Not created or approved. |
| Live connector activation | Not created or approved. |
| GBrain/Hermes/Cadence activation | Not created or approved. |
| Graphify rerun/adoption | Not created or approved. |
| Vector DB / embeddings | Not created or approved. |
| Graph DB / substrate selection | Not created or approved. |
| Generated output tracking | Not created or approved. |
| Source tracking expansion | Not created or approved. |
| Publication | Not created or approved. |
| Git mutation by the agent | Not performed. |

## Recommended Next Ticket
P5.1 - Validation Runner Minimal Implementation, if not already completed.

Otherwise: P5.3 - Context Assembly Runtime Candidate.

Do not start P5.3 from this ticket.

## Final Verdict
P5.2 is accepted as a controlled, product-independent, inert security policy dry-run skeleton candidate. Implementation skeleton is not activation. Security enforcement remains non-active. AGENT PLATFORM remains pre-active unless a later exact gate changes posture.
