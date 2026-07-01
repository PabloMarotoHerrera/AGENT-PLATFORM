# M-06 - External Metadata Migration
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | External Metadata Migration |
| Ticket | M-06 |
| Status | Accepted external-metadata migration planning |
| Date | 2026-07-01 |
| Scope | Safe-metadata planning records for current external source snapshots under `4_external/sources/` |
| Authority | Planning only; not source review execution, source copying, external adoption, dependency adoption, execution approval, provider/API/MCP activation, product activation, substrate decision, archive execution, staging, commit, push, publication, or M-07 start |
| Related documents | W-03, W-13, V-05, M-02, M-03, M-04, M-05, W-08, W-11, W-12, A-00, A-01, CSS-series, H-series, S-series |

## 2. Purpose
M-06 converts the existing W-03/W-13 external source inventory into bounded migration-planning records so future work can decide which external metadata reviews, pattern reviews, product reviews, or substrate-evidence reviews may be useful.
M-06 preserves names, classes, local references, posture, blockers, and routes. It does not inspect raw source trees deeply, copy source content, run commands from sources, or promote any source.

## 3. Active Scope
| In scope | Handling |
| --- | --- |
| W-03 source names and classes | Preserve as safe metadata. |
| W-13 handling policy | Apply as boundary and stop-rule authority. |
| V-05 validation posture | Apply as readiness and blocker language. |
| M-05 research context | Use as prior evidence-curation posture only. |
| Metadata planning records | Create M-06 candidate records for future review routing. |

## 4. Non-Scope
| Out of scope | Reason |
| --- | --- |
| Raw external source content | Source trees remain local-only and not migrated. |
| README/setup/license text copying | Only safe posture and references are retained. |
| Source execution or package install | W-13 and V-05 block execution and dependency adoption. |
| Provider/API/MCP activation | Network/auth/provider actions require separate approval. |
| Product activation | W-12 product scope is not active. |
| Substrate decision | The Cognitive Semantic System substrate remains undecided. |
| Git staging, commit, push, publication | Not authorized by M-06. |

## 5. Input Authority Order
| Priority | Input | M-06 use |
| ---: | --- | --- |
| 1 | W-03 external source registry | Primary current inventory, class, risk, license, relevance, and recommended use. |
| 2 | W-13 external source handling policy | Primary boundary for metadata, instruction, execution, dependency, product, substrate, Git, and agent handling. |
| 3 | V-05 external source validation model | Validation posture, proof levels, blockers, incidents, and verdict vocabulary. |
| 4 | M-05 research evidence migration | Prior evidence-curation context and external/source neutrality. |
| 5 | M-02, M-03, M-04 | Prior migration planning inputs by reference, not embedded documents. |
| 6 | W-08, W-11, W-12, A-00, A-01, CSS/H/S-series | Migration, governance, product, lifecycle, naming, harness, and security boundaries. |

## 6. Source Boundary
M-06 uses architecture metadata from allowed documents. It does not deeply inspect `4_external/sources/`, `previusknowledge/`, `2_products/`, datasets, models, artifacts, secrets, credentials, or local-only folders.
External source names and local references are retained as metadata labels only. They do not name AGENT PLATFORM systems and do not create authority.

## 7. External Metadata Definition
External metadata is curated information about an external source: source name, local reference, class, provenance posture, license posture, risk posture, instruction status, allowed use, blocked use, validation posture, lifecycle posture, and future route.
External metadata is not source code, external documentation content, setup text, license text, dependency approval, execution approval, product activation, or semantic truth.

## 8. Authority Boundary
| Layer | M-06 boundary |
| --- | --- |
| Governance | Decides promotion, rejection, dependency adoption, execution, product activation, publication, and lifecycle. |
| Validation | Evaluates readiness and blockers; it does not approve action. |
| Security | Blocks execution, secrets, credentials, local-only exposure, provider/API/MCP activation, unsafe publication, and broad Git actions. |
| Metadata | Records safe planning posture only. |
| Agents | May curate safe metadata in this file; cannot promote, adopt, run, install, authenticate, stage, commit, push, or start M-07. |

## 9. Current Inventory
| Source | Local reference | W-03/W-13 class | License posture | Risk posture | M-06 route |
| --- | --- | --- | --- | --- | --- |
| `acpx` | `4_external/sources/acpx` | Assistant / gateway / protocol integration | MIT indicated | Medium protocol bridge/session/network risk | Adapter-boundary metadata candidate. |
| `ai-cookbook-main` | `4_external/sources/ai-cookbook-main` | Cookbook / example corpus | MIT indicated by `LICENCE` | Medium API/credentialed-example risk | Example taxonomy metadata candidate. |
| `clawhub` | `4_external/sources/clawhub` | Registry / catalog | MIT indicated | Medium supply-chain/package-trust risk | Registry metadata candidate. |
| `ECC-main` | `4_external/sources/ECC-main` | Agent harness / coding-agent reference | MIT indicated | High runtime/authority-collapse risk | Harness-pattern metadata candidate. |
| `EnergyPlusV24-2-0` | `4_external/sources/EnergyPlusV24-2-0` | Domain simulation / SDK reference | Custom/domain license indicated | High native/license/product risk | Product/domain blocker metadata candidate. |
| `graphify` | `4_external/sources/graphify` | Semantic projection / candidate substrate reference | MIT indicated | Medium projection/truth/naming risk | Substrate-neutral projection metadata candidate. |
| `hermes-agent` | `4_external/sources/hermes-agent` | Agent harness / coding-agent reference | MIT indicated | High self-improvement/dependency risk | Risk-first harness metadata candidate. |
| `openclaw` | `4_external/sources/openclaw` | Assistant / gateway / protocol integration | MIT indicated | High gateway/credential/user-data risk | Gateway/skill boundary metadata candidate. |
| `opencode` | `4_external/sources/opencode` | Agent harness / coding-agent reference | MIT indicated | High file/shell/provider/session risk | Context/tool/session metadata candidate. |
| `openstudio` | `4_external/sources/openstudio` | Domain simulation / SDK reference | Domain SDK license indicated | High SDK/native/package/license risk | Product/domain blocker metadata candidate. |
| `pi` | `4_external/sources/pi` | Agent harness / coding-agent reference | MIT indicated | High provider/file/shell/session risk | Harness/provider-tool metadata candidate. |
| `tau` | `4_external/sources/tau` | Agent harness / coding-agent reference | No visible top-level license in inspected root | High instruction/credential/license-gap risk | Instruction/license/harness metadata candidate. |

## 10. Source Class Catalog
| Class | Sources | M-06 handling |
| --- | --- | --- |
| Agent harness / coding-agent reference | `ECC-main`, `hermes-agent`, `opencode`, `pi`, `tau` | Evidence for future harness/session/tool/provider/context review only. |
| Assistant / gateway / protocol integration | `acpx`, `openclaw` | Evidence for adapter, channel, gateway, and protocol boundary review only. |
| Registry / catalog | `clawhub` | Evidence for trust, package metadata, publishing, and supply-chain review only. |
| Cookbook / example corpus | `ai-cookbook-main` | Evidence for example taxonomy and documentation structure only. |
| Domain simulation / SDK reference | `EnergyPlusV24-2-0`, `openstudio` | Product/domain evidence only until product governance exists. |
| Semantic projection / candidate substrate reference | `graphify` | Candidate projection/substrate evidence only; no naming or final substrate authority. |

## 11. Current Status Baseline
All 12 sources are `observed_snapshot`, `classified_external_reference`, `local_only`, `not_promoted`, `execution_blocked`, `dependency_blocked`, and `instruction_blocked` unless a narrower W-03/W-13 risk label is stated.
M-06 adds planning labels only: `m06_metadata_planning_candidate`, `m06_deferred_to_review`, `m06_blocked_for_execution`, and `m06_blocked_for_adoption`.

## 12. Metadata Record Model
Conceptual fields: `candidate_id`, source name, local reference, source class, current status, provenance posture, license posture, notice posture, runtime/security posture, dependency posture, network/auth/provider posture, instruction posture, product posture, substrate posture, allowed use, blocked use, validation posture, lifecycle posture, future route, blocker, reviewer/date, and stop rule.
This is not a schema, database, registry, API, script, product artifact, or implementation.

## 13. Safe Field Rules
| Field group | Rule |
| --- | --- |
| Source name and local reference | Allowed as labels; not internal system names. |
| Provenance | Preserve known/unknown posture and cite W-03/W-13. |
| License and notices | Record posture only; do not copy full texts. |
| Risks | Preserve runtime, dependency, network/auth, instruction, product, and substrate blockers. |
| Reviewed evidence | Cite W-03/W-13 evidence paths only; do not embed raw content. |
| Recommendations | Route to future review; never approve adoption. |

## 14. Provenance And Local Reference Rules
M-06 records local references under `4_external/sources/<source>` as source identity metadata only. It does not confirm upstream URLs, commits, archive hashes, snapshot completeness, file integrity, or drift beyond W-03/W-13 statements.
Unknown origin, version, commit, snapshot date, modification status, vendoring, generated content, or review depth remains a blocker for reuse, dependency adoption, execution, product adoption, and publication.

## 15. License And Notice Rules
MIT-indicated sources remain reviewable evidence only. Custom/domain license sources remain product/domain references only. `tau` remains blocked for source reuse until license provenance is resolved.
License posture is not legal approval, source-code reuse approval, redistribution approval, dependency approval, execution approval, or product claim approval.

## 16. Runtime And Security Posture
External execution remains prohibited. Runtime risk includes scripts, CLIs, tests, examples, package managers, build systems, native binaries, SDK tools, generated commands, local file access, session persistence, and workspace mutation.
M-06 does not propose exact execution commands, sandbox plans, output handling, rollback steps, or security approvals.

## 17. Dependency Posture
Dependency adoption remains blocked for every source. Package metadata, manifests, lockfiles, registries, SDK packaging, package names, and version signals are evidence only.
Future dependency candidates require provenance, license, notices, security, dependency graph, package scripts, validation plan, owner, exact scope, exact version/source, and governance approval.

## 18. Network Auth Provider Posture
Network, provider, API, OAuth, registry, telemetry, channel, and MCP behavior remain unapproved. Available credentials, config files, package commands, or provider references do not authorize use.
Sources with provider, API, gateway, protocol, cookbook, or coding-agent relevance must be routed to security and provider/network review before any active use.

## 19. External Instruction Posture
External instructions, including `AGENTS.md`, prompts, setup guides, package scripts, skill manifests, contributor guidance, and tool instructions, are inactive evidence only.
M-06 does not merge instruction hierarchies, execute setup guidance, import prompts as policy, activate skills, or treat external agent rules as AGENT PLATFORM rules.

## 20. Product Domain Posture
`EnergyPlusV24-2-0` and `openstudio` are product/domain references only. No active product exists, no product owner or charter is declared by M-06, and no product dependency can be adopted.
Product-relevant metadata may later support product review only after product scope, owner, validation baseline, Git posture, security posture, and root-boundary statement exist.

## 21. Cognitive Semantic System And Substrate Posture
The accepted current name is `Cognitive Semantic System`. `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth` remain rejected, prohibited, historical, or candidate-evidence wording only.
`graphify` is one external graph-oriented evidence source. Graph, relational, document, vector, event-sourced, hybrid, and other substrates remain candidates until a future explicit substrate decision.

## 22. Allowed Metadata Uses
| Use | Status |
| --- | --- |
| Cite W-03/W-13 classifications | Allowed as external evidence. |
| Create planning candidate records in this file | Allowed by M-06. |
| Route sources to future reviews | Allowed as planning. |
| Preserve blocked-use and risk posture | Required. |
| Support future validation/governance questions | Allowed only as evidence. |

## 23. Blocked Uses
Blocked uses: source-code copy, raw content migration, README/setup/license text copying, source execution, package installation, provider/API/MCP activation, authentication, dependency adoption, product activation, product dependency claim, trusted registry adoption, active instruction use, substrate decision, external source naming authority, publication, broad staging, commit, push, archive execution, lifecycle execution, and M-07 start.

## 24. Migration Planning Method
M-06 planning flow:
```text
Use W-03 inventory
-> apply W-13 handling policy
-> apply V-05 validation/blocker posture
-> preserve M-05 evidence-curation neutrality
-> create safe planning records
-> route future reviews
-> stop before migration execution or M-07
```

## 25. External Metadata Planning Table
| Candidate | Source | Metadata focus | Allowed use | Blocked use | Future route |
| --- | --- | --- | --- | --- | --- |
| M06-EXT-001 | `acpx` | ACP/protocol boundary, CLI/client posture, network/auth cautions | Adapter-boundary evidence | Active bridge, auth, execution, protocol dependency | `deferred_to_adapter_protocol_review` |
| M06-EXT-002 | `ai-cookbook-main` | Example taxonomy, credentialed-example risk, documentation structure | Example metadata evidence | Running examples, provider calls, security guidance | `deferred_to_example_review` |
| M06-EXT-003 | `clawhub` | Registry metadata, trust labels, package/skill distribution risk | Registry-pattern evidence | Trusted registry, install/publish source | `deferred_to_registry_trust_review` |
| M06-EXT-004 | `ECC-main` | Agent OS/harness orchestration, authority-collapse risk | Harness architecture evidence | Runtime/governance authority, source copy | `deferred_to_harness_review` |
| M06-EXT-005 | `EnergyPlusV24-2-0` | Domain engine, native/runtime, license/name-use posture | Product/domain evidence | Root dependency, execution, product claim | `deferred_to_product_domain_review` |
| M06-EXT-006 | `graphify` | Projection, generated-artifact, naming/substrate risk | Substrate-neutral evidence | System naming, graph decision, generated truth | `deferred_to_css_substrate_evaluation` |
| M06-EXT-007 | `hermes-agent` | Self-improvement, lifecycle, dependency risk | Risk-first harness evidence | Self-modification adoption, dependency pins | `deferred_to_governance_safety_review` |
| M06-EXT-008 | `openclaw` | Gateway, channel, skill packaging, user-data risk | Gateway/skill boundary evidence | Active gateway, auth path, trusted skills | `deferred_to_gateway_skill_review` |
| M06-EXT-009 | `opencode` | Coding-agent session, context, tools, transcript privacy | Context/tool evidence | Workspace config, shell/file policy, execution | `deferred_to_agent_context_harness_review` |
| M06-EXT-010 | `openstudio` | SDK/tooling, native/package/license posture | Product/domain evidence | Root SDK, product claim, package integration | `deferred_to_product_domain_review` |
| M06-EXT-011 | `pi` | Harness/session/provider/tool design, provider risk | Harness/provider-tool evidence | Active harness, provider config, tool policy | `deferred_to_harness_provider_review` |
| M06-EXT-012 | `tau` | Harness layering, instructions, license gap, credentials | Instruction/license/harness evidence | Active instructions, source reuse, provider auth | `deferred_to_instruction_license_review` |

## 26. Source Route Summary
| Route | Sources | Future review focus |
| --- | --- | --- |
| `deferred_to_harness_review` | `ECC-main`, `opencode`, `pi`, `tau`, `hermes-agent` | Agent loop, session, tool, provider, context, runtime, privacy, and authority boundaries. |
| `deferred_to_gateway_skill_review` | `acpx`, `openclaw`, `clawhub` | Protocols, channels, registries, skills, packages, trust, and supply chain. |
| `deferred_to_example_review` | `ai-cookbook-main` | Documentation examples, credentials, provider calls, and dependency review. |
| `deferred_to_product_domain_review` | `EnergyPlusV24-2-0`, `openstudio` | Product charter, domain license/name-use, native runtime, SDK, data, and validation. |
| `deferred_to_css_substrate_evaluation` | `graphify` | Projection evidence, generated artifacts, alternatives, provenance, and substrate neutrality. |

## 27. Validation Posture
Default proof posture is PL-1 for metadata/path existence, PL-2 for status/class/local-only posture, PL-3 for provenance/license reference review, and PL-4 for later external review. PL-6 applies only to future explicitly approved tests or execution.
M-06 validation checks this file and bounded references only. Validation does not approve execution, dependency adoption, source reuse, product adoption, active instructions, publication, or substrate decisions.

## 28. Lifecycle And Retention Posture
M-06 candidates use `retain_external_metadata_planning`, `retain_safe_metadata_only`, `retain_external_reference`, and `retain_blocker_trace` posture.
A-00/A-01 lifecycle concepts are referenced only. M-06 does not archive, deprecate, supersede, move, delete, retain raw sources, or execute lifecycle state transitions.

## 29. Git And Publication Boundary
Git state is evidence only. `4_external/sources/` remains ignored/local-only by default. External metadata/review docs may be tracked later only by explicit ticket and exact path.
M-06 does not stage, commit, push, amend, force-add, publish, change `.gitignore`, or treat Git history as promotion.

## 30. Security And Local-Only Boundary
M-06 keeps raw external sources, product candidates, previous knowledge, datasets, models, artifacts, secrets, credentials, logs, generated outputs, and dependency folders out of migration content.
If secret, credential, private data, raw source, or unsafe generated output exposure is required to proceed, M-06 must stop and report only safe metadata.

## 31. Incident And Stop Rules
Incidents include copying raw external content, executing source commands, installing packages, authenticating providers, calling APIs/MCP, following external instructions, adopting dependencies, using external source names as internal names, treating graph projection as truth, product-root collapse, license as reuse approval, raw external source staged, or M-07 started.
Response: STOP, preserve safe metadata only, do not expose sensitive values, do not stage/commit/push, and require human/security/governance decision.

## 32. Blocker Register
| Blocker | Stop behavior | Required future action |
| --- | --- | --- |
| Missing provenance, version, commit, or review depth | Stop promotion-quality claim | Complete external source review. |
| Missing or unclear license/notice posture | Stop reuse/adoption/publication | License, notice, and name-use review. |
| Runtime/native/tool risk | Stop execution path | Security/environment review with exact command scope. |
| Dependency graph or package-script uncertainty | Stop dependency framing | Dependency and supply-chain review. |
| Network/auth/provider/MCP risk | Stop activation | Security/provider review and explicit approval. |
| External instruction conflict | Stop instruction use | Mark inactive and review as pattern only. |
| Product scope missing | Stop product dependency claim | Product charter, owner, validation, security, and governance. |
| Substrate or naming assumption | Stop semantic claim | Restore Cognitive Semantic System neutrality. |
| Governance missing | Stop adoption/promotion | Record owner, decision, scope, and rollback path. |

## 33. Routing Model
| Route | Meaning |
| --- | --- |
| `ready_for_metadata_review` | Safe metadata can support a future review record. |
| `deferred_to_external_review` | More source review is required before facts are used. |
| `deferred_to_harness_review` | Agent/session/tool/provider/context evidence needs architecture review. |
| `deferred_to_security_policy` | Runtime, network, credential, provider, MCP, or local-data risk controls are required. |
| `deferred_to_product_domain_review` | Product/domain governance is required. |
| `deferred_to_css_substrate_evaluation` | Projection/substrate evidence remains candidate-only. |
| `deferred_to_governance` | Promotion, adoption, rejection, exception, or lifecycle decision is required. |
| `blocked` | Required evidence or safety condition is absent. |

## 34. Citation Rules
Future metadata or review records should cite W-03 for source inventory and classification, W-13 for handling policy, V-05 for validation posture, W-08 for migration posture, W-11 for governance, W-12 for product boundaries, S-series for security/access, CSS-series for naming/substrate neutrality, and this M-06 record for planning route.
Citation is provenance, not truth or approval.

## 35. Relationship To M-02 Through M-05
M-02 and M-03 provide prior carry-forward and conflicted normalization context. M-04 provides agent/context/runtime/provider/adapter/tool/MCP planning context. M-05 provides research-evidence curation posture.
M-06 does not embed those documents, reopen prior classifications, inspect raw previous knowledge, or promote prior research facts. It uses them only to keep external metadata planning aligned with migration, evidence, and substrate boundaries.

## 36. Remaining Gaps
No per-source external review records, provenance registry, license/notice audit, dependency graph review, execution review, product dependency review, substrate evaluation, security approval, provider/API/MCP approval, publication review, external metadata repository, schema, scanner, CI, tests, implementation, archive action, lifecycle action, staging, commit, push, or M-07 artifact exists.

## 37. M-07 Readiness And Stop Boundary
M-07 is not started. A future M-07 can proceed only after explicit instruction and must define its own target file, scope, inputs, validation, blockers, and stop rule.
M-06 leaves future work ready to choose exact external metadata reviews, but not ready to adopt, run, install, authenticate, copy, publish, activate products, approve dependencies, or decide the Cognitive Semantic System substrate.

## 38. Final Verdict
| Question | Answer |
| --- | --- |
| What does M-06 create? | One safe external-metadata migration-planning document. |
| How many sources are represented? | 12 current W-03/W-13 external source snapshots. |
| Did M-06 inspect raw external source trees deeply? | No. |
| Did M-06 copy source code, README/setup/license text, product content, or previous-knowledge content? | No. Safe metadata only. |
| Are any sources promoted, adopted, executable, or dependency-approved? | No. |
| Are external instructions active? | No. |
| Are product dependencies or products activated? | No. |
| Is the Cognitive Semantic System substrate selected? | No. Graph remains a candidate only. |
| What remains blocked? | Raw content migration, source reuse, execution, install, provider/API/MCP activation, authentication, dependency adoption, product activation, publication, lifecycle execution, archive execution, staging, commit, push, and M-07. |
Final M-06 statement:
```text
M-06 preserves external source metadata as migration-planning evidence only. It keeps
all 12 external sources external, local-only, unpromoted, execution-blocked,
dependency-blocked, instruction-blocked, product-unactivated, and substrate-neutral,
and it stops before migration execution, adoption, publication, Git actions, and M-07.
```
