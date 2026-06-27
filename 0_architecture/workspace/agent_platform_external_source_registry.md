# AGENT PLATFORM External Source Registry

Status: Canonical W-03 workspace output  
Date: 2026-06-27  
Scope: Governed registry for `4_external/sources/`  
Authority: Classification and handling guidance only. No external source is promoted by this document.

## 1. Purpose

This registry classifies the external source snapshots under `4_external/sources/` so future agents and humans can use them as evidence without mistaking proximity for authority.

The registry exists to answer four questions:

- What kind of source is each external repository or distribution?
- What value can it provide to AGENT PLATFORM architecture work?
- What risks must be controlled before any reuse, execution, integration, or promotion?
- What is explicitly not allowed to be inferred from the source being present in the workspace?

This document does not approve running external code, installing dependencies, authenticating with external services, copying source into internal products, or treating external project instructions as active workspace instructions.

## 2. Registry Model

Each source is classified with these fields.

| Field | Meaning |
| --- | --- |
| Source | Directory name under `4_external/sources/`. |
| Evidence inspected | Local files used as classification evidence. |
| Source type | The kind of external material represented by the source. |
| Primary domain | The domain the source appears to address. |
| Role | How the source may inform AGENT PLATFORM. |
| Authority posture | Whether the source has any current AGENT PLATFORM authority. |
| License / reuse posture | Current license signal and reuse constraint. |
| Runtime / security / data risk | Risk if installed, executed, authenticated, or integrated. |
| Reuse / relevance level | Architectural relevance before any promotion. |
| Promotion status | Current governance state inside this workspace. |
| Recommended future use | Safe future review direction. |
| Must not use for | Explicit forbidden interpretation or use. |

## 3. Source Type Taxonomy

| Source type | Definition | Sources |
| --- | --- | --- |
| Agent harness / coding-agent reference | Agent loop, tool execution, provider abstraction, session, CLI, TUI, or harness design material. | `ECC-main`, `hermes-agent`, `opencode`, `pi`, `tau` |
| Assistant / gateway / protocol integration | Assistant gateway, ACP client, multi-channel, or integration surface. | `acpx`, `openclaw` |
| Registry / catalog | Package, skill, or extension registry pattern. | `clawhub` |
| Cookbook / example corpus | Example-oriented AI application or integration recipes. | `ai-cookbook-main` |
| Domain simulation / SDK reference | Building-energy simulation engine, SDK, or product-domain tooling. | `EnergyPlusV24-2-0`, `openstudio` |
| Semantic projection / candidate substrate reference | Graph or semantic projection tooling useful as evidence for future substrate evaluation. | `graphify` |

## 4. Authority Posture

All external sources have the same current authority posture:

| Rule | Posture |
| --- | --- |
| Workspace authority | None by default. |
| Evidence status | External reference evidence only. |
| Promotion status | Not promoted. |
| Instruction status | External `AGENTS.md` or equivalent files are repository-local evidence only. |
| Naming authority | No source names the future AGENT PLATFORM semantic authority system. |
| Substrate authority | No source decides whether graph, relational, document, vector, hybrid, or another substrate becomes canonical. |

The neutral working name for the future semantic authority remains `Cognitive Semantic System`. External graph-oriented tooling may inform evaluation, but it does not name or decide the system.

## 5. License / Reuse Posture

License posture is evidence-level only. It is not legal approval.

| Posture | Sources | Handling |
| --- | --- | --- |
| MIT indicated by local evidence | `acpx`, `ai-cookbook-main`, `clawhub`, `ECC-main`, `graphify`, `hermes-agent`, `openclaw`, `opencode`, `pi` | Potentially reusable only after provenance, notice, security, dependency, and governance review. |
| Custom / domain-specific license indicated | `EnergyPlusV24-2-0`, `openstudio` | Treat as domain/product reference only until license and name-use constraints are reviewed. |
| No visible top-level license file in inspected root | `tau` | Do not reuse source code until license provenance is resolved upstream or by deeper review. |

## 6. External Source Inventory

### 6.1 `acpx`

| Field | Classification |
| --- | --- |
| Evidence inspected | `README.md`, `LICENSE`, `package.json` |
| Source type | Assistant / gateway / protocol integration |
| Primary domain | Agent Client Protocol headless CLI client |
| Role | ACP integration evidence and protocol-facing adapter pattern source |
| Authority posture | External evidence only; not internal adapter authority |
| License / reuse posture | MIT indicated; reuse still requires provenance, security, and dependency review |
| Runtime / security / data risk | Medium; protocol clients can bridge local agent sessions, tools, and external endpoints |
| Reuse / relevance level | Medium |
| Promotion status | Not promoted; integration review candidate only |
| Recommended future use | Review for ACP boundary vocabulary, CLI invocation shape, and adapter risk controls |
| Must not use for | Current adapter architecture, approved dependency, active protocol bridge, or runtime execution |

### 6.2 `ai-cookbook-main`

| Field | Classification |
| --- | --- |
| Evidence inspected | Nested `ai-cookbook-main/README.md`, `LICENCE` |
| Source type | Cookbook / example corpus |
| Primary domain | AI application examples and implementation recipes |
| Role | Pattern evidence for examples, prompts, model integrations, and educational structure |
| Authority posture | External example evidence only |
| License / reuse posture | MIT indicated by `LICENCE`; examples require per-file and dependency review before reuse |
| Runtime / security / data risk | Medium; example code may call external APIs, require credentials, or embed incomplete safety assumptions |
| Reuse / relevance level | Medium-low for platform root; higher for future example curation |
| Promotion status | Not promoted; example corpus only |
| Recommended future use | Mine for documentation style and example taxonomy after source and dependency review |
| Must not use for | Canonical architecture, validated implementation, security guidance, or credentialed execution |

### 6.3 `clawhub`

| Field | Classification |
| --- | --- |
| Evidence inspected | `README.md`, `LICENSE`, `package.json` |
| Source type | Registry / catalog |
| Primary domain | Public skill registry and package catalog for OpenClaw-style skills |
| Role | Evidence for skill distribution, catalog metadata, and registry governance patterns |
| Authority posture | External evidence only; no internal package registry authority |
| License / reuse posture | MIT indicated; private package/workspace posture requires care before reuse |
| Runtime / security / data risk | Medium; registry and skill catalogs introduce supply-chain, provenance, trust, and package-execution risk |
| Reuse / relevance level | Medium |
| Promotion status | Not promoted; registry pattern candidate only |
| Recommended future use | Review for future skill catalog policy, package metadata, trust labels, and publishing controls |
| Must not use for | Approved package source, trusted skill registry, or default extension-distribution model |

### 6.4 `ECC-main`

| Field | Classification |
| --- | --- |
| Evidence inspected | `README.md`, `LICENSE`, `package.json` |
| Source type | Agent harness / coding-agent reference |
| Primary domain | Harness-native agent operating system |
| Role | High-value architecture evidence for agent OS, harness decomposition, and multi-capability coordination |
| Authority posture | External evidence only; not AGENT PLATFORM runtime or governance authority |
| License / reuse posture | MIT indicated; package metadata identifies `ecc-universal` version `2.0.0` and upstream GitHub provenance |
| Runtime / security / data risk | High; an agent operating system can combine tools, providers, execution, memory, and workspace access |
| Reuse / relevance level | High |
| Promotion status | Not promoted; architecture-pattern review candidate |
| Recommended future use | Review for harness boundaries, OS metaphors, extension model, and runtime participation posture |
| Must not use for | Current platform runtime, installed agent OS, execution authority, or governance model |

### 6.5 `EnergyPlusV24-2-0`

| Field | Classification |
| --- | --- |
| Evidence inspected | `readme.html`, `LICENSE.txt` |
| Source type | Domain simulation / SDK reference |
| Primary domain | Building energy simulation engine and distribution |
| Role | Product/domain reference for building-energy modeling, not platform-root architecture |
| Authority posture | External domain evidence only |
| License / reuse posture | Custom domain distribution license indicated, including DOE/name-use conditions; legal review required before reuse |
| Runtime / security / data risk | High; native executables, DLLs, simulation files, and large binary/runtime surface |
| Reuse / relevance level | Low for AGENT PLATFORM root; high only for a future energy/building product workspace |
| Promotion status | Not promoted; product/domain review candidate only |
| Recommended future use | Preserve as domain evidence until a product workspace defines energy-modeling scope and license controls |
| Must not use for | Generic platform architecture, root authority, runtime execution, dependency adoption, or product integration without review |

### 6.6 `graphify`

| Field | Classification |
| --- | --- |
| Evidence inspected | `README.md`, `ARCHITECTURE.md`, `LICENSE`, `pyproject.toml` |
| Source type | Semantic projection / candidate substrate reference |
| Primary domain | Graph and semantic projection tooling |
| Role | Evidence for graph-oriented representation, projection, reports, and possible substrate evaluation |
| Authority posture | External evidence only; not the Cognitive Semantic System and not naming authority |
| License / reuse posture | MIT indicated; `pyproject.toml` package name observed as `graphifyy` version `0.8.49` |
| Runtime / security / data risk | Medium; projection tools can transform source material into persuasive generated artifacts that may be mistaken for truth |
| Reuse / relevance level | High as evaluation evidence; not authoritative |
| Promotion status | Not promoted; candidate-substrate and projection review source only |
| Recommended future use | Review for projection boundaries, generated artifact labeling, provenance, drift handling, and graph-substrate tradeoffs |
| Must not use for | Naming the future system, deciding the final substrate, treating generated graph outputs as authority, or replacing governance |

### 6.7 `hermes-agent`

| Field | Classification |
| --- | --- |
| Evidence inspected | `README.md`, `LICENSE`, `pyproject.toml`, `package.json` |
| Source type | Agent harness / coding-agent reference |
| Primary domain | Self-improving AI agent |
| Role | Evidence for self-improvement, agent lifecycle, package split, and risk posture |
| Authority posture | External evidence only; no internal self-modification authority |
| License / reuse posture | MIT indicated; exact-pinned dependency posture observed and requires dependency review |
| Runtime / security / data risk | High; self-improving agent behavior can affect code, prompts, dependencies, credentials, and workspace state |
| Reuse / relevance level | Medium-high |
| Promotion status | Not promoted; high-risk architecture review candidate only |
| Recommended future use | Review for explicit improvement loops, rollback requirements, validation gates, and self-modification governance |
| Must not use for | Active self-improving behavior, autonomous code modification policy, or dependency adoption without review |

### 6.8 `openclaw`

| Field | Classification |
| --- | --- |
| Evidence inspected | `README.md`, `LICENSE`, `package.json` |
| Source type | Assistant / gateway / protocol integration |
| Primary domain | Personal AI assistant and multi-channel gateway |
| Role | Evidence for assistant UX, channel routing, skill packaging, and gateway architecture |
| Authority posture | External evidence only; not AGENT PLATFORM assistant or gateway authority |
| License / reuse posture | MIT indicated; third-party notices present and must be preserved if reuse is approved |
| Runtime / security / data risk | High; assistant gateways may handle credentials, user data, external channels, package execution, and provider access |
| Reuse / relevance level | Medium |
| Promotion status | Not promoted; gateway pattern review candidate only |
| Recommended future use | Review for channel boundaries, package/skill trust, credential isolation, and user-data handling |
| Must not use for | Active assistant gateway, trusted skill source, authentication path, or user-data policy |

### 6.9 `opencode`

| Field | Classification |
| --- | --- |
| Evidence inspected | `README.md`, `CONTEXT.md`, `LICENSE`, `package.json` |
| Source type | Agent harness / coding-agent reference |
| Primary domain | Open-source AI coding agent |
| Role | High-value evidence for coding-agent sessions, context vocabulary, tool execution, and productized agent UX |
| Authority posture | External evidence only; not workspace execution or context authority |
| License / reuse posture | MIT indicated; source reuse still requires provenance, notice, dependency, and security review |
| Runtime / security / data risk | High; coding agents can read/write files, run shell commands, manage sessions, and call model providers |
| Reuse / relevance level | High |
| Promotion status | Not promoted; architecture-pattern review candidate |
| Recommended future use | Review `CONTEXT.md` for context/session vocabulary, transcript handling, and bounded tool-execution design |
| Must not use for | Active workspace agent configuration, default context model, shell/file execution policy, or approved dependency |

### 6.10 `openstudio`

| Field | Classification |
| --- | --- |
| Evidence inspected | `README.md`, `LICENSE.md`, `conanfile.py` |
| Source type | Domain simulation / SDK reference |
| Primary domain | Building energy modeling SDK and tooling |
| Role | Product/domain reference for building modeling, workflows, SDK packaging, and domain integration |
| Authority posture | External domain evidence only |
| License / reuse posture | Domain SDK license with designation/name-use conditions indicated; package and binary integration require legal and security review |
| Runtime / security / data risk | High; SDKs, native dependencies, package managers, and modeling workflows create broad supply-chain and runtime surface |
| Reuse / relevance level | Low for AGENT PLATFORM root; high only for future energy/building product scope |
| Promotion status | Not promoted; product/domain review candidate only |
| Recommended future use | Review only after a bounded product workspace defines building-energy modeling requirements and license controls |
| Must not use for | Root architecture, generic platform SDK posture, runtime execution, dependency adoption, or product claim without review |

### 6.11 `pi`

| Field | Classification |
| --- | --- |
| Evidence inspected | `README.md`, `LICENSE`, `package.json` |
| Source type | Agent harness / coding-agent reference |
| Primary domain | Pi agent harness and coding-agent architecture |
| Role | High-value evidence for harness design, agent core, provider API, coding tools, and multi-provider LLM integration |
| Authority posture | External evidence only; not AGENT PLATFORM harness authority |
| License / reuse posture | MIT indicated; dependency and provider integration require review before reuse |
| Runtime / security / data risk | High; coding-agent harnesses can access files, shell tools, providers, sessions, and credentials |
| Reuse / relevance level | High |
| Promotion status | Not promoted; architecture-pattern review candidate |
| Recommended future use | Review for harness/session separation, provider-neutral event contracts, tool schemas, and deterministic tests |
| Must not use for | Active harness implementation, provider configuration, tool execution policy, or direct source adoption without review |

### 6.12 `tau`

| Field | Classification |
| --- | --- |
| Evidence inspected | `README.md`, `pyproject.toml`, `AGENTS.md`, `mkdocs.yml` |
| Source type | Agent harness / coding-agent reference |
| Primary domain | Python minimalist Pi-style coding-agent harness and teaching implementation |
| Role | High-value evidence for readable harness layering, phase documentation, event contracts, tools, sessions, skills, and TUI separation |
| Authority posture | External evidence only; its `AGENTS.md` is not active workspace instruction |
| License / reuse posture | No visible top-level license file in inspected root; do not reuse source code until license provenance is resolved |
| Runtime / security / data risk | High; Tau reads project context, exposes local coding tools, stores credentials/session data, and can authenticate providers |
| Reuse / relevance level | High |
| Promotion status | Not promoted; architecture-pattern review candidate |
| Recommended future use | Review for educational architecture sequencing, `AgentHarness` / `AgentSession` / TUI boundary, event stream contracts, session persistence, and compaction vocabulary |
| Must not use for | Active instructions, source reuse before license review, installed CLI, provider authentication, or workspace execution |

## 7. Harness Strategy Signal

The highest-value harness signals come from `pi`, `tau`, `opencode`, `ECC-main`, and selected `hermes-agent` evidence.

| Signal | Sources | W-03 interpretation |
| --- | --- | --- |
| Harness/session/frontend separation | `pi`, `tau`, `opencode` | Strong candidate pattern for future architecture review. Not adopted yet. |
| Event stream as contract | `tau`, `pi`, `opencode` | Useful for provider-neutral rendering, testing, logging, and session replay. Requires validation later. |
| Typed tools and deterministic tool results | `pi`, `tau`, `opencode` | Useful for safety, auditability, and testability. Does not define tool policy yet. |
| Provider abstraction and retry/thinking events | `tau`, `pi`, `opencode` | Useful input for adapter/provider posture. Must remain separate from provider authority. |
| Durable sessions, transcripts, resume, branch, export | `tau`, `opencode`, `pi` | Useful for context continuity and evidence handling. Requires privacy and retention rules. |
| Context accounting and compaction | `tau`, `opencode` | Useful for agent cognition and bounded context selection. Not equivalent to semantic truth. |
| Skills, resources, and project-local instructions | `tau`, `opencode`, `openclaw`, `clawhub` | Useful but high-risk. Must distinguish evidence, prompts, instructions, policy, and authority. |
| Agent OS and orchestration framing | `ECC-main` | Useful conceptual input for runtime participation posture. Not runtime authority. |
| Self-improvement loops | `hermes-agent` | Useful as a risk pattern, not as a default goal. Requires strong governance gates. |

W-03 conclusion: the external harness sources justify future review of agent-loop, tool, provider, session, context, and frontend boundaries. They do not authorize implementation, dependency adoption, or runtime behavior.

## 8. Cognitive Workspace Relevance

The external sources support the agent-native cognitive workspace in bounded ways.

| Relevance area | Useful sources | Boundary |
| --- | --- | --- |
| Agent cognition through bounded context | `opencode`, `tau`, `pi` | Context windows, compaction, and transcripts are evidence-management mechanisms, not truth. |
| Semantic projection and substrate evaluation | `graphify` | Graph is a candidate representation and projection mode, not the decided substrate. |
| Governance of skills and packages | `clawhub`, `openclaw`, `tau` | Skill discovery must not bypass source, license, trust, or execution review. |
| Runtime participation posture | `ECC-main`, `pi`, `tau`, `opencode` | Runtime participation does not own semantic authority or governance approval. |
| Product/domain cognition | `EnergyPlusV24-2-0`, `openstudio` | Domain engines belong to bounded product workspaces, not root platform authority. |
| Example curation | `ai-cookbook-main` | Examples need provenance, validation, and dependency review before use. |

The Cognitive Semantic System remains future conceptual authority. This registry only preserves external evidence and risk labels for later decisions.

## 9. Risk Register

| Risk ID | Risk | Affected sources | Required control |
| --- | --- | --- | --- |
| R-01 | Authority contamination from cloned sources | All | Treat sources as external evidence until explicit promotion. |
| R-02 | License or name-use violation | All, especially `EnergyPlusV24-2-0`, `openstudio`, `tau` | Perform license and notice review before reuse, distribution, or product claims. |
| R-03 | Runtime execution and native binary risk | `EnergyPlusV24-2-0`, `openstudio`, agent harness sources | Do not execute or install without security and environment review. |
| R-04 | Credential, OAuth, provider, or API-key exposure | `opencode`, `tau`, `pi`, `openclaw`, `hermes-agent`, `ai-cookbook-main` | Do not authenticate or run provider-connected workflows without approval. |
| R-05 | Supply-chain and package registry risk | `clawhub`, `openclaw`, `pi`, `tau`, `opencode`, `ECC-main`, `hermes-agent` | Require package provenance, lockfile, dependency, and trust review. |
| R-06 | External project instructions leaking into AGENT PLATFORM behavior | `tau` and any source with `AGENTS.md` or equivalent | Treat external instructions as evidence only. Do not execute them as workspace policy. |
| R-07 | Semantic naming and substrate confusion | `graphify`, prior graph-oriented evidence | Use `Cognitive Semantic System` as neutral name and keep substrate undecided. |
| R-08 | Product/domain material becoming root platform authority | `EnergyPlusV24-2-0`, `openstudio` | Keep domain engines inside future bounded product scopes unless promoted. |
| R-09 | Session, transcript, and context privacy | `opencode`, `tau`, `pi`, `hermes-agent` | Define retention, redaction, export, and access rules before adoption. |
| R-10 | Generated artifacts mistaken for truth | `graphify`, cookbook examples, agent outputs | Label generated artifacts as projections or evidence until governed promotion. |

## 10. Promotion Rules

An external source can move beyond external evidence only through explicit promotion.

Minimum promotion requirements:

- Declared target scope: root platform, product workspace, example corpus, adapter, provider, runtime posture, validation, security, or documentation.
- Provenance record: upstream URL, version, commit, archive source, and local snapshot date where available.
- License record: license text, notices, name-use constraints, redistribution constraints, and compatibility assessment.
- Security record: runtime permissions, dependency graph, native binaries, network use, credential handling, file access, and data retention.
- Authority record: what is promoted, what remains external, who approved it, and what supersedes or constrains it.
- Validation record: tests, reproducibility, non-execution review, threat model, or other evidence appropriate to the promotion.
- Governance record: approval owner, decision date, rollback path, drift-review cadence, and exception handling.

Promotion prohibitions:

- A source is not promoted because it is cloned under `4_external/sources/`.
- MIT or permissive license evidence is not enough to approve source reuse.
- Runtime execution is not approved by architecture interest.
- External project instructions are not active AGENT PLATFORM instructions.
- Generated graph outputs, projections, transcripts, examples, or agent reports are not Cognitive Semantic System authority by default.
- Domain engines do not define root platform scope unless a later governance decision explicitly promotes that boundary.

## 11. Recommended Source Handling

| Handling track | Sources | Recommendation |
| --- | --- | --- |
| High-value harness architecture review | `pi`, `tau`, `opencode`, `ECC-main` | Review first for future agent-loop, session, tool, provider, context, and frontend boundary work. |
| High-risk self-improvement review | `hermes-agent` | Review primarily as a governance and safety risk source before considering any design adoption. |
| Semantic projection and substrate review | `graphify` | Review for generated artifact posture and substrate tradeoffs without adopting name or graph as final substrate. |
| Skill, package, and gateway review | `clawhub`, `openclaw`, `acpx` | Review for trust, registry metadata, channel boundaries, package provenance, and protocol mediation. |
| Example corpus review | `ai-cookbook-main` | Review for documentation and example taxonomy only; do not execute credentialed examples. |
| Product/domain review | `EnergyPlusV24-2-0`, `openstudio` | Defer until a bounded energy/building product workspace exists with legal and security review. |

## 12. Registry Counts

| Count type | Count |
| --- | ---: |
| Total external source directories inspected | 12 |
| Not promoted / external reference only | 12 |
| MIT indicated by local evidence | 9 |
| Custom / domain-specific license indicated | 2 |
| No visible top-level license file in inspected root | 1 |
| High-value harness or coding-agent references | 5 |
| Assistant / gateway / protocol integration sources | 2 |
| Registry / catalog sources | 1 |
| Cookbook / example corpus sources | 1 |
| Domain simulation / SDK references | 2 |
| Semantic projection / candidate substrate references | 1 |
| High runtime/security/data risk if executed or integrated | 8 |
| Medium runtime/security/data risk if executed or integrated | 4 |

## 13. Highest-Value Sources

| Source | Why it is high value |
| --- | --- |
| `pi` | Direct harness, coding-agent, provider, tool, and multi-provider design evidence. |
| `tau` | Readable Python teaching implementation with explicit harness/session/TUI separation and phase documentation. |
| `opencode` | Production-oriented coding-agent context, session, tool, and UX evidence. |
| `ECC-main` | Agent OS and multi-capability orchestration evidence. |
| `graphify` | Useful for semantic projection and candidate substrate evaluation, with strong naming and authority boundaries required. |

## 14. Highest-Risk Sources

| Source | Primary risk |
| --- | --- |
| `EnergyPlusV24-2-0` | Native binaries, domain license/name-use constraints, and product-domain scope risk. |
| `openstudio` | SDK/native dependency surface, package integration, domain license/name-use constraints. |
| `opencode` | Coding-agent file, shell, provider, session, and credential exposure if run. |
| `tau` | Local coding tools, credentials, project-context discovery, external `AGENTS.md`, and no visible top-level license file. |
| `pi` | Coding-agent harness with provider, file, shell, and session risk if executed. |
| `hermes-agent` | Self-improvement and dependency posture risk. |
| `openclaw` | Multi-channel gateway, skill/package, credential, and user-data risk. |
| `ECC-main` | Agent OS/runtime framing that could collapse execution, authority, and governance if adopted carelessly. |

## 15. Recommended Future Reviews

Recommended review sequence:

1. Harness boundaries: `pi`, `tau`, `opencode`, and `ECC-main`.
2. Context/session/privacy model: `opencode`, `tau`, and `pi`.
3. Tool execution and provider mediation: `pi`, `tau`, `opencode`, `acpx`, and `openclaw`.
4. Skill/package registry trust: `clawhub`, `openclaw`, and `tau`.
5. Semantic projection and substrate options: `graphify` as one candidate input only.
6. Self-improvement governance: `hermes-agent` as a risk-first review.
7. Product/domain scope: `EnergyPlusV24-2-0` and `openstudio` only after product workspace boundaries exist.

## 16. Final Verdict

The `4_external/sources/` tree is valuable as a controlled evidence library. It is not an authority layer, implementation dependency set, runtime sandbox, product workspace, or semantic truth store.

All 12 inspected sources remain external references. The strongest architecture inputs are agent harness, context/session, tool boundary, provider mediation, skill/package governance, and semantic projection patterns. The strongest risks are authority contamination, execution without review, credential exposure, license/name-use constraints, supply-chain exposure, external instruction leakage, and premature substrate decisions.

Future work may cite this registry when selecting sources for deeper review, but any promotion must pass explicit provenance, license, security, validation, and governance controls.
