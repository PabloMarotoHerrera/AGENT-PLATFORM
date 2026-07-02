"""I-02 minimal security/access policy evaluator boundary.

This module models declared access requests in memory only. It does not scan
files, inspect secrets, read credentials, call external systems, execute
runtime enforcement, activate providers, approve governance decisions, or imply
readiness. Validation evaluates; governance decides. Security policy flags
risk; governance decides.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Sequence


class SensitivityLevel(str, Enum):
    """Declared target sensitivity values."""

    PUBLIC_METADATA = "public_metadata"
    GOVERNANCE_METADATA = "governance_metadata"
    LOCAL_ONLY = "local_only"
    GENERATED_SENSITIVE = "generated_sensitive"
    SECRET = "secret"
    CREDENTIAL = "credential"
    UNKNOWN = "unknown"


class ActionCategory(str, Enum):
    """Declared action categories for access requests."""

    READ_GOVERNANCE_METADATA = "read_governance_metadata"
    RECORD_VALIDATION_METADATA = "record_validation_metadata"
    CREATE_GOVERNANCE_ARTIFACT = "create_governance_artifact"
    INSPECT_LOCAL_ONLY_SOURCE = "inspect_local_only_source"
    READ_SECRET = "read_secret"
    READ_CREDENTIAL = "read_credential"
    EXECUTE_TOOL = "execute_tool"
    SHELL_COMMAND = "shell_command"
    NETWORK_CALL = "network_call"
    PROVIDER_API_CALL = "provider_api_call"
    MCP_ACTIVATION = "mcp_activation"
    SOURCE_TRACKING = "source_tracking"
    GIT_MUTATION = "git_mutation"
    FORCE_ADD = "force_add"
    PUBLISH = "publish"
    ADOPT_DEPENDENCY = "adopt_dependency"
    ACTIVATE_PRODUCT = "activate_product"
    CREATE_RUNTIME = "create_runtime"
    UNKNOWN = "unknown"


class AccessDecisionStatus(str, Enum):
    """Decision statuses for declared metadata access requests."""

    ALLOWED_FOR_METADATA_ONLY = "allowed_for_metadata_only"
    BLOCKED = "blocked"
    NEEDS_REVIEW = "needs_review"
    REJECTED_FOR_SCOPE = "rejected_for_scope"


ALLOWED_FOR_METADATA_ONLY_IS_NOT_GOVERNANCE_APPROVAL = (
    "allowed_for_metadata_only is not governance approval"
)
ALLOWED_FOR_METADATA_ONLY_IS_NOT_AUTHORIZATION = (
    "allowed_for_metadata_only does not authorize execution or activation"
)
EVIDENCE_REFS_ARE_METADATA_ONLY = "evidence_refs are metadata references only"

SAFE_METADATA_ACTIONS = {
    ActionCategory.READ_GOVERNANCE_METADATA.value,
    ActionCategory.RECORD_VALIDATION_METADATA.value,
    ActionCategory.CREATE_GOVERNANCE_ARTIFACT.value,
}

BLOCKED_ACTIONS = {
    ActionCategory.INSPECT_LOCAL_ONLY_SOURCE.value,
    ActionCategory.READ_SECRET.value,
    ActionCategory.READ_CREDENTIAL.value,
    ActionCategory.EXECUTE_TOOL.value,
    ActionCategory.SHELL_COMMAND.value,
    ActionCategory.NETWORK_CALL.value,
    ActionCategory.PROVIDER_API_CALL.value,
    ActionCategory.MCP_ACTIVATION.value,
    ActionCategory.SOURCE_TRACKING.value,
    ActionCategory.GIT_MUTATION.value,
    ActionCategory.FORCE_ADD.value,
    ActionCategory.PUBLISH.value,
    ActionCategory.ADOPT_DEPENDENCY.value,
    ActionCategory.ACTIVATE_PRODUCT.value,
    ActionCategory.CREATE_RUNTIME.value,
}

BLOCKED_SENSITIVITIES = {
    SensitivityLevel.SECRET.value,
    SensitivityLevel.CREDENTIAL.value,
}

REVIEW_SENSITIVITIES = {
    SensitivityLevel.UNKNOWN.value,
    SensitivityLevel.LOCAL_ONLY.value,
    SensitivityLevel.GENERATED_SENSITIVE.value,
}


def _value(value: object) -> object:
    if isinstance(value, Enum):
        return value.value
    return value


def _tuple_of_strings(values: object) -> object:
    if isinstance(values, str):
        return values
    try:
        return tuple(values)
    except TypeError:
        return values


@dataclass(frozen=True)
class AccessRequest:
    """Declared metadata-only access request."""

    request_id: str
    actor_id: str
    action: str
    target: str
    target_sensitivity: str
    purpose: str
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    created_at: str = ""
    review_required: bool = True
    blockers: Sequence[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "action", _value(self.action))
        object.__setattr__(self, "target_sensitivity", _value(self.target_sensitivity))
        object.__setattr__(self, "evidence_refs", _tuple_of_strings(self.evidence_refs))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))


@dataclass(frozen=True)
class AccessDecision:
    """Decision metadata for a declared access request."""

    request_id: str
    status: str
    reasons: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    review_required: bool = True
    created_at: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", _value(self.status))
        object.__setattr__(self, "reasons", _tuple_of_strings(self.reasons))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))


class SecurityAccessEnforcer:
    """In-memory metadata policy evaluator only."""

    def __init__(self) -> None:
        self._decisions: Dict[str, AccessDecision] = {}

    def evaluate_request(self, request: AccessRequest) -> AccessDecision:
        """Evaluate a declared request and store the decision in memory."""
        errors = self.validate_request(request)
        if errors:
            decision = AccessDecision(
                request_id=_request_id_or_empty(request),
                status=AccessDecisionStatus.REJECTED_FOR_SCOPE.value,
                reasons=errors,
                blockers=_request_blockers_or_empty(request) + tuple(errors),
                limitations=("request validation failed",),
                review_required=True,
                created_at=_request_created_at_or_empty(request),
            )
            if decision.request_id:
                self._decisions[decision.request_id] = decision
            return decision

        status = AccessDecisionStatus.ALLOWED_FOR_METADATA_ONLY.value
        reasons = ["safe metadata action for declared non-secret and non-credential scope"]
        blockers = list(request.blockers)
        limitations = [
            ALLOWED_FOR_METADATA_ONLY_IS_NOT_GOVERNANCE_APPROVAL,
            ALLOWED_FOR_METADATA_ONLY_IS_NOT_AUTHORIZATION,
        ]
        review_required = request.review_required

        if request.target_sensitivity in BLOCKED_SENSITIVITIES:
            status = AccessDecisionStatus.BLOCKED.value
            reasons = ["secret or credential sensitivity is blocked"]
            blockers.append("secret_or_credential_request_blocked")
            review_required = True
        elif request.action in BLOCKED_ACTIONS:
            status = AccessDecisionStatus.BLOCKED.value
            reasons = ["high-risk action category is blocked"]
            blockers.append("high_risk_action_blocked")
            review_required = True
        elif request.target_sensitivity in REVIEW_SENSITIVITIES:
            status = AccessDecisionStatus.NEEDS_REVIEW.value
            reasons = ["target sensitivity requires review"]
            blockers.append("sensitivity_review_required")
            review_required = True
        elif request.action == ActionCategory.UNKNOWN.value:
            status = AccessDecisionStatus.NEEDS_REVIEW.value
            reasons = ["unknown action requires review"]
            blockers.append("unknown_action_review_required")
            review_required = True
        elif request.action not in SAFE_METADATA_ACTIONS:
            status = AccessDecisionStatus.NEEDS_REVIEW.value
            reasons = ["action is outside safe metadata scope"]
            blockers.append("unsafe_metadata_scope")
            review_required = True

        decision = AccessDecision(
            request_id=request.request_id,
            status=status,
            reasons=tuple(reasons),
            blockers=tuple(blockers),
            limitations=tuple(limitations),
            review_required=review_required,
            created_at=request.created_at,
        )
        self._decisions[request.request_id] = decision
        return decision

    def get_decision(self, request_id: str) -> Optional[AccessDecision]:
        """Return a decision by request ID, or None when absent."""
        return self._decisions.get(request_id)

    def list_decisions(self) -> List[AccessDecision]:
        """Return all decision records in insertion order."""
        return list(self._decisions.values())

    @staticmethod
    def validate_request(request: AccessRequest) -> List[str]:
        """Return validation errors for required request metadata fields."""
        if not isinstance(request, AccessRequest):
            return ["request must be an AccessRequest"]

        errors: List[str] = []
        required_text = {
            "request_id": request.request_id,
            "actor_id": request.actor_id,
            "action": request.action,
            "target": request.target,
            "target_sensitivity": request.target_sensitivity,
            "purpose": request.purpose,
            "created_at": request.created_at,
        }

        for field_name, value in required_text.items():
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{field_name} is required")

        allowed_actions = {action.value for action in ActionCategory}
        if isinstance(request.action, str) and request.action not in allowed_actions:
            errors.append(f"action must be one of: {', '.join(sorted(allowed_actions))}")

        allowed_sensitivities = {level.value for level in SensitivityLevel}
        if (
            isinstance(request.target_sensitivity, str)
            and request.target_sensitivity not in allowed_sensitivities
        ):
            errors.append(
                "target_sensitivity must be one of: "
                f"{', '.join(sorted(allowed_sensitivities))}"
            )

        errors.extend(_validate_string_sequence("evidence_refs", request.evidence_refs))
        errors.extend(_validate_string_sequence("blockers", request.blockers))

        for evidence_ref in _iter_strings(request.evidence_refs):
            if "\n" in evidence_ref or "\r" in evidence_ref:
                errors.append("evidence_refs must be references or IDs, not raw contents")

        if not isinstance(request.review_required, bool):
            errors.append("review_required must be a boolean")

        return errors


def _validate_string_sequence(field_name: str, values: object) -> List[str]:
    if isinstance(values, str):
        return [f"{field_name} must be a sequence of strings"]
    try:
        iterator = iter(values)
    except TypeError:
        return [f"{field_name} must be a sequence of strings"]
    errors: List[str] = []
    for index, value in enumerate(iterator):
        if not isinstance(value, str):
            errors.append(f"{field_name}[{index}] must be a string")
    return errors


def _iter_strings(values: object) -> List[str]:
    if isinstance(values, str):
        return []
    try:
        return [value for value in values if isinstance(value, str)]
    except TypeError:
        return []


def _request_id_or_empty(request: object) -> str:
    if isinstance(request, AccessRequest) and isinstance(request.request_id, str):
        return request.request_id
    return ""


def _request_created_at_or_empty(request: object) -> str:
    if isinstance(request, AccessRequest) and isinstance(request.created_at, str):
        return request.created_at
    return ""


def _request_blockers_or_empty(request: object) -> Sequence[str]:
    if isinstance(request, AccessRequest):
        return tuple(_iter_strings(request.blockers))
    return tuple()
