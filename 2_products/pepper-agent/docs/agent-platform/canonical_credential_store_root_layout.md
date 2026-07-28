# Canonical Credential Store Root Layout

P15.C2 repairs Pepper's default OpenAI Codex credential-store root layout while preserving legacy discoverability for an already materialized duplicated store.

The canonical Pepper credential-store root contains exactly one agent-platform/provider-credentials hierarchy.

## Authority

P15.C2 owns only the default root layout and compatibility resolver for the Pepper product. It does not migrate, inspect, copy, move, delete, refresh or rotate credentials.

P15.C1 Windows credential-store protection remains authoritative for directory and file DACL application and validation after a root is selected.

## Layouts

Canonical root:

```text
<HERMES_HOME>/agent-platform/provider-credentials/openai-codex.primary
```

Legacy duplicated root:

```text
<HERMES_HOME>/agent-platform/provider-credentials/agent-platform/provider-credentials/openai-codex.primary
```

The legacy layout came from a previous helper that appended `agent-platform/provider-credentials` twice when composing the default store root.

## Resolution Matrix

| Canonical root | Legacy duplicated root | Result |
| --- | --- | --- |
| absent | absent | select canonical root for new stores |
| present | absent | select canonical root |
| absent | present | select legacy duplicated root for compatibility |
| present | present | fail closed as ambiguous |

An existing duplicated legacy root remains selectable only when the canonical root is absent.

When both canonical and legacy roots exist, Pepper fails closed rather than choosing one silently.

## Compatibility Boundary

Root resolution checks only whether the canonical or legacy root path is present. A present directory, file, symlink or reparse-point root is treated as present and remains subject to later store validation.

Root resolution does not inspect, copy, move, delete, refresh or rotate credential contents.

The resolver does not create canonical or legacy directories. New clean environments select the canonical root, and the later promotion path creates and protects that canonical root.

The legacy duplicated root is not documented as canonical and is not claimed as permanent. It exists only as compatibility until a later reviewed migration or removal decision.

## Windows Protection

P15.C1 remains responsible for Windows DACL protection. After root selection, store preparation applies a protected DACL for the current user, LocalSystem and Builtin Administrators, then validation rejects broad or unexpected principals.

## Testability

The public helper accepts an explicit Hermes home path for synthetic tests. When explicit root input is supplied, no home fallback or environment expansion is needed by the root composition helpers.

Tests and smoke validation use temporary synthetic Hermes homes only. They do not use the real home directory, real auth stores or real credentials.

## Operational Constraints

P15.C2 performs no OAuth, provider calls, worker starts, credential leases, Docker execution, remote-host access, Graphify activity, dependency installation, Git staging, commits or pushes.

## P15.C3 Handoff

P15.C3 owns legacy Hermes product removal. It must consume the committed P15.C2 root repair, keep `2_products/pepper-agent` intact and avoid deleting durable credential stores or external source references.
