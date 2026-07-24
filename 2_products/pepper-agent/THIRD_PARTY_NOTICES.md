# Pepper Third-Party Notices

Status: source notice for the governed Pepper product candidate. This file is
not a legal certification, SBOM, dependency-license clearance, trademark grant,
binary distribution approval, dashboard bundle publication approval or container
publication approval.

## 1. Pepper Identity

Product name: Pepper

Product identifier: `pepper`

Product version: `0.1.0-dev`

## 2. Hermes Agent Attribution

Pepper is derived from Hermes Agent source material and preserves upstream
technical identifiers, package namespaces, environment-variable names and route
namespaces unless separately governed.

Upstream product name: Hermes Agent

Upstream version: `0.19.0`

## 3. Exact Upstream Source

Upstream repository: `https://github.com/NousResearch/hermes-agent`

Upstream tag: `v2026.7.20`

Upstream commit: `3ef6bbd201263d354fd83ec55b3c306ded2eb72a`

## 4. Root MIT License Reference

The root upstream license is preserved at:

```text
LICENSE
```

That file is the authoritative local license text for the included MIT-licensed
Hermes Agent source portions.

## 5. Included Apache-Licensed Components

The security-guidance plugin includes Apache-2.0 material. Its local license is
preserved at:

```text
plugins/security-guidance/LICENSE
```

## 6. Required NOTICE Preservation

The security-guidance plugin NOTICE file is preserved at:

```text
plugins/security-guidance/NOTICE
```

Any distribution that includes the security-guidance plugin must preserve the
applicable Apache-2.0 license and NOTICE obligations.

## 7. Included MIT Plugin And Skill References

Additional included permissive notices are preserved in place, including:

```text
plugins/hermes-achievements/LICENSE
skills/creative/humanizer/LICENSE
optional-skills/creative/pixel-art/ATTRIBUTION.md
skills/software-development/spike/SKILL.md
skills/creative/sketch/SKILL.md
```

Inline adapted-work attributions in included skill files must remain intact.

## 8. Excluded PowerPoint Subtree Statement

The restricted PowerPoint skill subtree and generated complete PowerPoint skill
documentation remain excluded from the Pepper product payload under the P15
license reconciliation. This notice does not include, relicense or authorize
that excluded material.

## 9. Dependency-License Uncertainty

Python and Node transitive dependency-license evidence remains incomplete for
public binary, bundled-asset or container distribution clearance. Source-level
presence of dependency manifests and lockfiles is not a public distribution
approval.

## 10. Desktop Binary-Distribution Restriction

Desktop binary packaging, signing, native dependency, installer and platform
notice obligations remain unresolved. This notice does not approve desktop
binary publication.

## 11. Dashboard Bundle-Distribution Restriction

Committed or future dashboard bundle assets require separate dependency and
bundle provenance review before public asset or binary distribution. This notice
does not approve dashboard bundle publication.

## 12. Container-Publication Restriction

Container base images, APT packages, runtime downloads, Playwright assets,
s6-overlay obligations and SBOM evidence remain unresolved. This notice does
not approve public container-image publication.

## 13. Trademark And Branding Statement

Hermes, Hermes Agent, Nous Research and related upstream names or marks are
attributed to their respective owners. Source licenses do not grant trademark
or brand endorsement rights. Pepper must not present itself as official Hermes
Agent or as endorsed by Nous Research without separate authorization.

## 14. Provider-Service Terms Separation

Provider accounts, OAuth flows, external services, API quotas, model access and
service endpoints are governed by separate provider terms. Source licenses do
not authorize provider-service use.

## 15. Preserved License-File Locations

Known preserved local license and notice locations include:

```text
LICENSE
plugins/hermes-achievements/LICENSE
plugins/security-guidance/LICENSE
plugins/security-guidance/NOTICE
skills/creative/humanizer/LICENSE
optional-skills/creative/pixel-art/ATTRIBUTION.md
```

File-specific terms in included templates and inline attributions remain
preserved where present.

## 16. Pepper Modification Attribution

Pepper product modifications are recorded in:

```text
AGENT_PLATFORM_MODIFICATIONS.tsv
```

P15.M6 adds a bounded Pepper product identity foundation, an authenticated
product-configuration endpoint, text-first shell branding, semantic token
aliases, protected product namespace filtering and this third-party notice. It
does not activate P13 product routes, Desktop, Workspace, providers, runtime
execution, credentials, package identity changes or public branding.
