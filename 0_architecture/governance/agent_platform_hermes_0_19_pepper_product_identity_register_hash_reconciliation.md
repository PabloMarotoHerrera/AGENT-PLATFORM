# P15.M6A - Pepper Product Identity Register Hash Reconciliation

Status: P15.M6A committed register hash reconciliation prepared for human review.

Final verdict: `hermes_0_19_pepper_product_identity_register_hashes_reconciled`

## Authority

P15.M6A is a bounded predecessor repair before restarting P15.M6R. It corrects
only the `current_product_sha256_or_none` field for three P15.M6 modification
register rows whose recorded values matched Windows working-tree bytes instead
of the exact committed Git blob bytes.

No implementation files, third-party notices, branding manifest, import
manifest, exclusion manifest, upstream baseline record or prior P15.M6
governance records are modified by this repair.

## Reconciled Rows

| Modification ID | Product path | Previous recorded SHA-256 | Exact HEAD Git blob SHA-256 |
| --- | --- | --- | --- |
| `P15.M6-002` | `hermes_cli/web_server.py` | `696e264cebfb5ce5e4062a44f821b188df9fc2c1f81a2e13d8978a75aafdd8ae` | `d08e29db31bb044f248e1593ddb06db486e6b04f9f05144f6daba421fc04c46e` |
| `P15.M6-020` | `web/src/main.tsx` | `a5d3d582e084d7274eef2be2ad272fef8a348bdbf567dccc7f9720db9cd28e8a` | `fc83d0f55f392c936231725731ff55deabb6f70b624c5aa6b5ff9cbb8bfd3dc9` |
| `P15.M6-021` | `web/src/App.tsx` | `8a252727299be199c75c0115a5f7f8442606a0468fefc6a9182faf72b80c6dc5` | `8ca66b772754824ac4ecada6f11c20ea8af518657bb3d272daef7d86d4987972` |

The replacement hashes were calculated from exact `HEAD` Git blob bytes under
`2_products/pepper-agent/`, not from checked-out working-tree files.

## Preserved Register Fields

P15.M6A preserves the 18-column schema, row ordering, all modification IDs,
paths, baseline upstream commits, baseline source object IDs, baseline source
SHA-256 values, classifications, intent text, reapplication predicates,
conflict owners, security or compatibility impacts, validation lanes, upstream
dispositions, rollback targets, retirement conditions, approval references and
statuses.

## Candidate Scope

| Path | Disposition |
| --- | --- |
| `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` | reconciles exactly three `current_product_sha256_or_none` values |
| `0_architecture/governance/agent_platform_hermes_0_19_pepper_product_identity_register_hash_reconciliation.md` | records this bounded repair |

## Runtime Boundary

| Action | Count |
| --- | ---: |
| Product implementation changes | 0 |
| Third-party notice changes | 0 |
| Branding manifest changes | 0 |
| Import manifest changes | 0 |
| Exclusion manifest changes | 0 |
| Upstream baseline changes | 0 |
| Prior P15.M6 governance changes | 0 |
| Graphify actions | 0 |
| Dependency installation | 0 |
| Build actions | 0 |
| Runtime service starts | 0 |
| OAuth flows | 0 |
| Provider calls | 0 |
| Inference calls | 0 |
| Git staging by agent | 0 |
| Git commits by agent | 0 |
| Git pushes by agent | 0 |

## Validation

| Check | Result |
| --- | --- |
| P15.M6 rows | `22` |
| Register schema | fixed `18` columns |
| Row ordering | preserved |
| Exact corrected rows | `3` |
| Corrected row IDs | `P15.M6-002`; `P15.M6-020`; `P15.M6-021` |
| Committed-blob hash mismatches after projected repair | `0` |
| Duplicate IDs | `0` |
| Duplicate paths | `0` |
| Blank mandatory fields | `0` |
| Invalid classifications | `0` |
| Unregistered P15.M6 product files | `0` |
| Register rows without P15.M6 product files | `0` |
| Product implementation changes | `0` |
| Unexpected candidates | `0` |
| `git diff --check` | clean |
| Index empty | `true` |
| Staged files | `0` |

Validation command:

```cmd
python "C:\Users\pablo\AppData\Local\Temp\opencode\p15m6a_validate.py"
```

## Restart Boundary

After human review, commit and push of P15.M6A, P15.M6R must restart from the
beginning against the new HEAD. P15.M6R must treat P15.M6A as an authorized
post-P15.M6 metadata correction and must not require zero commits after the
original P15.M6 commit.
