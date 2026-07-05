"""Deny-by-default security policy metadata for P5.2.

The policy object is inert metadata. It provides default deny controls,
no-secret and no-credential guards, blocked class metadata, no scanner
behavior, and no enforcement activation.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import SecurityControl, SecurityDecisionStatus, SensitivityLevel, SourceClassification


@dataclass(frozen=True)
class SecurityPolicy:
    """Metadata-only policy object for dry-run evaluation."""

    policy_id: str
    policy_name: str
    description: str
    controls: tuple[SecurityControl, ...]
    blocked_source_classifications: tuple[SourceClassification, ...]
    blocked_sensitivities: tuple[SensitivityLevel, ...]
    blocked_subject_flags: tuple[str, ...]
    default_status: SecurityDecisionStatus = SecurityDecisionStatus.DENY
    dry_run_only: bool = True
    scanner_active: bool = False
    enforcement_active: bool = False
    limitations: tuple[str, ...] = ()


def default_deny_policy() -> SecurityPolicy:
    """Return the default deny metadata policy without side effects."""

    controls = (
        SecurityControl(
            control_id="P5.2-SEC-CTRL-001",
            control_name="default deny metadata guard",
            description="default deny posture for security dry-run metadata only",
        ),
        SecurityControl(
            control_id="P5.2-SEC-CTRL-002",
            control_name="no-secret metadata guard",
            description="no-secret guard metadata only; no secret inspection or storage",
        ),
        SecurityControl(
            control_id="P5.2-SEC-CTRL-003",
            control_name="no-credential metadata guard",
            description="no-credential guard metadata only; no credential inspection or use",
        ),
        SecurityControl(
            control_id="P5.2-SEC-CTRL-004",
            control_name="blocked source class guard",
            description="blocked source class guard metadata only",
        ),
        SecurityControl(
            control_id="P5.2-SEC-CTRL-005",
            control_name="blocked live connector guard",
            description="blocked live connector guard metadata only",
        ),
        SecurityControl(
            control_id="P5.2-SEC-CTRL-006",
            control_name="blocked provider/auth guard",
            description="blocked provider/auth guard metadata only",
        ),
        SecurityControl(
            control_id="P5.2-SEC-CTRL-007",
            control_name="blocked tool/agent execution guard",
            description="blocked tool/agent execution guard metadata only",
        ),
        SecurityControl(
            control_id="P5.2-SEC-CTRL-008",
            control_name="blocked GBrain/Hermes/Cadence guard",
            description="blocked GBrain/Hermes/Cadence guard metadata only",
        ),
        SecurityControl(
            control_id="P5.2-SEC-CTRL-009",
            control_name="no scanner behavior guard",
            description="no scanner behavior; policy object does not scan files or content",
        ),
        SecurityControl(
            control_id="P5.2-SEC-CTRL-010",
            control_name="no enforcement activation guard",
            description="no enforcement activation; policy object is dry-run metadata only",
        ),
    )
    return SecurityPolicy(
        policy_id="P5.2-SECURITY-DEFAULT-DENY-POLICY",
        policy_name="P5.2 SecurityPolicy default deny dry-run policy",
        description="Metadata-only SecurityPolicy for deny-by-default dry-run decisions.",
        controls=controls,
        blocked_source_classifications=(
            SourceClassification.RAW_GENERATED_OUTPUT,
            SourceClassification.LOCAL_ONLY_MATERIAL,
            SourceClassification.PRODUCT_SOURCE,
            SourceClassification.EXTERNAL_SOURCE,
            SourceClassification.GBRAIN_EXTERNAL_CANDIDATE,
            SourceClassification.HERMES_EXTERNAL_CANDIDATE,
            SourceClassification.PROVIDER_CONFIG,
            SourceClassification.TOKEN_STORE,
            SourceClassification.BROWSER_AUTH,
            SourceClassification.LOCAL_CREDENTIAL_STORE,
            SourceClassification.ENV_FILE,
            SourceClassification.SECRET_OR_CREDENTIAL,
            SourceClassification.UNKNOWN,
        ),
        blocked_sensitivities=(
            SensitivityLevel.LOCAL_ONLY,
            SensitivityLevel.PRODUCT_RESTRICTED,
            SensitivityLevel.EXTERNAL,
            SensitivityLevel.GENERATED_SENSITIVE,
            SensitivityLevel.SECRET_RELATED,
            SensitivityLevel.CREDENTIAL_RELATED,
            SensitivityLevel.UNKNOWN,
        ),
        blocked_subject_flags=(
            "secret_related",
            "credential_related",
            "provider_auth_related",
            "tool_execution_related",
            "agent_execution_related",
            "live_connector_related",
            "gbrain_related",
            "hermes_related",
            "cadence_related",
        ),
        limitations=(
            "Policy metadata is not runtime enforcement.",
            "Policy metadata performs no scanner behavior.",
            "Policy metadata does not read files, environment variables, credentials, or secrets.",
        ),
    )
