"""Metadata-only security dry-run data models.

The objects in this module store only policy metadata. They must not be
used to hold secret values, credential values, API keys, tokens, provider
configuration contents, environment file contents, browser auth material,
local credential store contents, product source, or raw generated output.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SecurityDecisionStatus(Enum):
    """Canonical metadata-only dry-run decision statuses."""

    ALLOW_METADATA_ONLY = "allow_metadata_only"
    DENY = "deny"
    DEFER = "defer"
    BLOCKED = "blocked"


class SensitivityLevel(Enum):
    """Metadata-only sensitivity labels."""

    PUBLIC_METADATA = "public_metadata"
    GOVERNANCE_METADATA = "governance_metadata"
    IMPLEMENTATION_METADATA = "implementation_metadata"
    LOCAL_ONLY = "local_only"
    PRODUCT_RESTRICTED = "product_restricted"
    EXTERNAL = "external"
    GENERATED_SENSITIVE = "generated_sensitive"
    SECRET_RELATED = "secret_related"
    CREDENTIAL_RELATED = "credential_related"
    UNKNOWN = "unknown"


class SourceClassification(Enum):
    """Metadata-only source classification labels."""

    GOVERNANCE_DOC = "governance_doc"
    IMPLEMENTATION_METADATA_RECORD = "implementation_metadata_record"
    SECURITY_POLICY = "security_policy"
    VALIDATION_READINESS_RECORD = "validation_readiness_record"
    GENERATED_EVIDENCE_SUMMARY = "generated_evidence_summary"
    RAW_GENERATED_OUTPUT = "raw_generated_output"
    LOCAL_ONLY_MATERIAL = "local_only_material"
    PRODUCT_SOURCE = "product_source"
    EXTERNAL_SOURCE = "external_source"
    GBRAIN_EXTERNAL_CANDIDATE = "gbrain_external_candidate"
    HERMES_EXTERNAL_CANDIDATE = "hermes_external_candidate"
    PROVIDER_CONFIG = "provider_config"
    TOKEN_STORE = "token_store"
    BROWSER_AUTH = "browser_auth"
    LOCAL_CREDENTIAL_STORE = "local_credential_store"
    ENV_FILE = "env_file"
    SECRET_OR_CREDENTIAL = "secret_or_credential"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class SecuritySubject:
    """Metadata subject supplied by a caller for in-memory dry-run review."""

    subject_id: str
    subject_type: str
    source_classification: SourceClassification
    sensitivity: SensitivityLevel
    metadata_only: bool = True
    local_only: bool = False
    product_related: bool = False
    external_related: bool = False
    generated_output_related: bool = False
    credential_related: bool = False
    secret_related: bool = False
    provider_auth_related: bool = False
    tool_execution_related: bool = False
    agent_execution_related: bool = False
    live_connector_related: bool = False
    gbrain_related: bool = False
    hermes_related: bool = False
    cadence_related: bool = False
    graphify_related: bool = False
    evidence_refs: tuple[str, ...] = ()
    validation_refs: tuple[str, ...] = ()
    security_refs: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()


@dataclass(frozen=True)
class SecurityControl:
    """Metadata control definition for a dry-run policy."""

    control_id: str
    control_name: str
    description: str
    default_status: SecurityDecisionStatus = SecurityDecisionStatus.DENY
    evidence_refs: tuple[str, ...] = ()
    validation_refs: tuple[str, ...] = ()
    security_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class DenyReason:
    """Reason metadata for deny or defer decisions."""

    reason_id: str
    reason_code: str
    message: str
    required_gate: str | None = None
    blocker_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class SecurityFinding:
    """Metadata finding produced by the in-memory dry-run evaluator."""

    finding_id: str
    subject_id: str
    decision_status: SecurityDecisionStatus
    reason: DenyReason
    evidence_refs: tuple[str, ...] = ()
    validation_refs: tuple[str, ...] = ()
    security_refs: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()


@dataclass(frozen=True)
class SecurityDecision:
    """Metadata-only security decision returned by dry-run evaluation."""

    decision_id: str
    subject_id: str
    status: SecurityDecisionStatus
    reasons: tuple[DenyReason, ...] = ()
    findings: tuple[SecurityFinding, ...] = ()
    human_approval_required: bool = True
    runtime_activation_approved: bool = False
    enforcement_active: bool = False
    limitations: tuple[str, ...] = ()


@dataclass(frozen=True)
class SecurityDryRunResult:
    """Metadata-only result for an in-memory security dry-run."""

    result_id: str
    policy_id: str
    subject_id: str
    decision: SecurityDecision
    findings: tuple[SecurityFinding, ...] = ()
    dry_run_only: bool = True
    side_effects: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
