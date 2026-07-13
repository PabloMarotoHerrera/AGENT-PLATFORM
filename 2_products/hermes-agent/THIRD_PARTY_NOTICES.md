# Third-Party Notices Baseline

This file is an engineering attribution baseline for the filtered Hermes Agent
product snapshot. It is not legal advice or complete release clearance.

## Upstream Identity

- Repository: `https://github.com/NousResearch/hermes-agent`
- Release: `0.18.2`
- Tag: `v2026.7.7.2`
- Commit: `9de9c25f620ff7f1ce0fd5457d596052d5159596`

## Known Imported MIT Materials

- Upstream Hermes project material under the top-level `LICENSE`.
- `plugins/hermes-achievements` under `plugins/hermes-achievements/LICENSE`.
- `skills/creative/humanizer` under `skills/creative/humanizer/LICENSE`.

These known classifications do not make the complete product tree uniformly
MIT and do not establish dependency-license clearance.

## Known Imported Apache-2.0 Material

- `plugins/security-guidance/LICENSE` preserves the Apache License 2.0 text.
- `plugins/security-guidance/NOTICE` preserves applicable attribution material.

The nested license and NOTICE remain part of the imported product snapshot.

## Excluded Material

- All 50 tracked files under `skills/productivity/powerpoint/**` were excluded
  because the restrictive license is not cleared.
- The English and Chinese generated complete-skill documentation pages for the
  excluded PowerPoint skill were excluded.
- Four tracked generated/cache files under `skills/index-cache/**` were
  excluded.
- Exact paths, blob IDs and source hashes are recorded in
  `SOURCE_EXCLUSIONS.tsv`.

## Unresolved Review

- Complete Python dependency SBOM has not been reviewed.
- Complete npm dependency SBOM has not been reviewed.
- Rust, native, Nix and container dependency posture is not cleared.
- Font, image, template and media provenance is not fully cleared.
- Documentation and generated-asset rights are not fully reviewed.
- Trademark and product-name use requires human/legal review.
- Hosted-service and commercial-distribution terms are not decided.
- Release-package contents have not been validated.
- Binary redistribution is not authorized.

Redistribution, publication, hosted production release and commercial release
remain blocked pending complete human/legal, SBOM, asset and packaging review.
