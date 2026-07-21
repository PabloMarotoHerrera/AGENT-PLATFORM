"""Internal safe resolver for bounded provider-worker profile metadata."""

from __future__ import annotations

from hermes_cli.agent_platform.provider_credentials.contracts import (
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
)
from hermes_cli.agent_platform.provider_runtime.enums import (
    ProviderFeaturePolicy,
    ProviderRuntimeAuthentication,
    ProviderRuntimeProvider,
    ProviderRuntimeTransport,
)
from hermes_cli.agent_platform.provider_runtime.resolution import (
    resolve_provider_runtime_profile,
)
from hermes_cli.agent_platform.provider_worker.contracts import (
    COMPLETE_INFERENCE_TIMEOUT_MS,
    CONNECTION_TIMEOUT_MS,
    MAXIMUM_OUTPUT_TOKENS,
    MAXIMUM_PROMPT_TOKENS,
    MAXIMUM_USER_CONTENT_TOKENS,
    OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID,
    RESERVED_SYSTEM_INSTRUCTION_TOKENS,
    RESPONSE_HEADER_TIMEOUT_MS,
    BoundedProviderWorkerProfile,
    ProviderWorkerResolutionRequest,
    ResolvedProviderWorkerBinding,
)
from hermes_cli.agent_platform.provider_worker.enums import (
    ProviderWorkerFeaturePolicy,
    ProviderWorkerProfileState,
)
from hermes_cli.agent_platform.provider_worker.profiles import (
    ProviderWorkerError,
    get_provider_worker_profile,
)


class ProviderWorkerProfileValidationError(ProviderWorkerError):
    """Raised when the worker profile state is not authorized."""

    error_code = "provider_worker_profile_validation_error"


class ProviderWorkerProviderProfileMismatchError(ProviderWorkerError):
    """Raised when worker and provider-runtime profile metadata diverge."""

    error_code = "provider_worker_provider_profile_mismatch"


class ProviderWorkerCredentialRequirementError(ProviderWorkerError):
    """Raised when credential-store metadata is incompatible."""

    error_code = "provider_worker_credential_requirement_error"


class ProviderWorkerConcurrencyPolicyError(ProviderWorkerError):
    """Raised when single-worker or single-request policy is weakened."""

    error_code = "provider_worker_concurrency_policy_error"


class ProviderWorkerQueuePolicyError(ProviderWorkerError):
    """Raised when queue capacity is non-zero."""

    error_code = "provider_worker_queue_policy_error"


class ProviderWorkerRequestBudgetError(ProviderWorkerError):
    """Raised when request budgets diverge from provider-runtime bounds."""

    error_code = "provider_worker_request_budget_error"


class ProviderWorkerResultBudgetError(ProviderWorkerError):
    """Raised when result budgets diverge from provider-runtime bounds."""

    error_code = "provider_worker_result_budget_error"


class ProviderWorkerTimeoutPolicyError(ProviderWorkerError):
    """Raised when worker timeout policy exceeds provider-runtime maxima."""

    error_code = "provider_worker_timeout_policy_error"


class ProviderWorkerFeaturePolicyError(ProviderWorkerError):
    """Raised when a disabled feature is enabled."""

    error_code = "provider_worker_feature_policy_error"


class ProviderWorkerResolutionError(ProviderWorkerError):
    """Raised when safe provider-runtime metadata cannot be composed."""

    error_code = "provider_worker_resolution_error"


def resolve_provider_worker_profile(
    request: ProviderWorkerResolutionRequest,
) -> ResolvedProviderWorkerBinding:
    """Resolve a bounded worker binding from safe provider-runtime metadata."""

    worker_profile = get_provider_worker_profile(request.worker_profile_id)
    if (
        worker_profile.state
        is not ProviderWorkerProfileState.PROFILE_READY_RUNTIME_UNVERIFIED
    ):
        _raise(
            ProviderWorkerProfileValidationError,
            worker_profile,
            "worker_profile_state",
        )
    if (
        request.provider_resolution_request.profile_id
        != worker_profile.provider_runtime_profile_id
    ):
        _raise(
            ProviderWorkerProviderProfileMismatchError,
            worker_profile,
            "provider_runtime_profile_id",
            provider_profile_id=request.provider_resolution_request.profile_id,
        )

    try:
        provider_binding = resolve_provider_runtime_profile(
            request.provider_resolution_request
        )
    except Exception as exc:
        raise ProviderWorkerResolutionError(
            worker_profile_id=worker_profile.profile_id,
            provider_profile_id=request.provider_resolution_request.profile_id,
            validation_category="provider_runtime_resolution",
        ) from exc

    _validate_provider_binding(worker_profile, provider_binding.profile)
    _validate_credential_requirement(worker_profile, provider_binding)
    _validate_execution_policy(worker_profile)
    _validate_request_policy(worker_profile, provider_binding.profile)
    _validate_result_policy(worker_profile, provider_binding.profile)
    _validate_timeout_policy(worker_profile, provider_binding.profile)

    return ResolvedProviderWorkerBinding(
        worker_profile=worker_profile,
        provider_binding=provider_binding,
        resolved_state=ProviderWorkerProfileState.READY_FOR_INFERENCE_GATE,
        resolved_at_utc=request.evaluated_at_utc,
    )


def _validate_provider_binding(
    worker_profile: BoundedProviderWorkerProfile,
    provider_profile: object,
) -> None:
    if (
        getattr(provider_profile, "profile_id", None)
        != OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID
    ):
        _raise(
            ProviderWorkerProviderProfileMismatchError,
            worker_profile,
            "provider_profile_id",
            provider_profile_id=str(getattr(provider_profile, "profile_id", "unknown")),
        )
    if (
        getattr(provider_profile, "provider", None)
        is not ProviderRuntimeProvider.OPENAI_CODEX
    ):
        _raise(ProviderWorkerProviderProfileMismatchError, worker_profile, "provider")
    if (
        getattr(provider_profile, "authentication", None)
        is not ProviderRuntimeAuthentication.CHATGPT_OAUTH
    ):
        _raise(
            ProviderWorkerProviderProfileMismatchError,
            worker_profile,
            "authentication",
        )
    if (
        getattr(provider_profile, "transport", None)
        is not ProviderRuntimeTransport.CODEX_RESPONSES
    ):
        _raise(ProviderWorkerProviderProfileMismatchError, worker_profile, "transport")
    model_policy = getattr(provider_profile, "model_policy", None)
    if getattr(model_policy, "model_id", None) != "gpt-5.5":
        _raise(ProviderWorkerProviderProfileMismatchError, worker_profile, "model")


def _validate_credential_requirement(
    worker_profile: BoundedProviderWorkerProfile,
    provider_binding: object,
) -> None:
    provider_profile = provider_binding.profile
    requirement = provider_profile.credential_requirement
    if worker_profile.credential_store_id != OPENAI_CODEX_CREDENTIAL_STORE_ID:
        _raise(ProviderWorkerCredentialRequirementError, worker_profile, "worker_store")
    if requirement.credential_store_id != worker_profile.credential_store_id:
        _raise(
            ProviderWorkerCredentialRequirementError, worker_profile, "provider_store"
        )
    if (
        provider_binding.credential_store_ref.store_id
        != worker_profile.credential_store_id
    ):
        _raise(
            ProviderWorkerCredentialRequirementError, worker_profile, "binding_store"
        )


def _validate_execution_policy(worker_profile: BoundedProviderWorkerProfile) -> None:
    policy = worker_profile.execution_policy
    if (
        policy.maximum_concurrent_workers != 1
        or policy.maximum_concurrent_requests_per_worker != 1
        or policy.maximum_requests_per_worker_lifetime != 1
    ):
        _raise(ProviderWorkerConcurrencyPolicyError, worker_profile, "single_request")
    if policy.request_queue_capacity != 0:
        _raise(ProviderWorkerQueuePolicyError, worker_profile, "queue_capacity")
    if policy.provider_calls_per_request_maximum != 1:
        _raise(ProviderWorkerConcurrencyPolicyError, worker_profile, "provider_calls")
    if policy.model_list_calls_per_request_maximum != 0:
        _raise(ProviderWorkerFeaturePolicyError, worker_profile, "model_list_calls")
    if policy.credential_refresh_calls_per_request_maximum != 0:
        _raise(
            ProviderWorkerFeaturePolicyError, worker_profile, "credential_refresh_calls"
        )

    for field_name in (
        "process_reuse",
        "persistent_memory",
        "conversation_history",
        "background_tasks",
        "subworkers",
        "subagents",
        "tools",
        "hosted_tools",
        "MCP",
        "streaming",
        "automatic_retry",
        "automatic_fallback",
    ):
        if getattr(policy, field_name) is not ProviderWorkerFeaturePolicy.DISABLED:
            _raise(ProviderWorkerFeaturePolicyError, worker_profile, field_name)


def _validate_request_policy(
    worker_profile: BoundedProviderWorkerProfile,
    provider_profile: object,
) -> None:
    policy = worker_profile.request_policy
    generation = provider_profile.generation_policy
    if policy.provider_runtime_profile_id != provider_profile.profile_id:
        _raise(
            ProviderWorkerProviderProfileMismatchError,
            worker_profile,
            "request_provider_profile",
        )
    if policy.maximum_prompt_tokens != generation.maximum_prompt_tokens:
        _raise(
            ProviderWorkerRequestBudgetError, worker_profile, "maximum_prompt_tokens"
        )
    if (
        policy.reserved_system_instruction_tokens
        != generation.reserved_system_instruction_tokens
    ):
        _raise(
            ProviderWorkerRequestBudgetError,
            worker_profile,
            "reserved_system_instruction_tokens",
        )
    if policy.maximum_user_content_tokens != generation.maximum_user_content_tokens:
        _raise(
            ProviderWorkerRequestBudgetError,
            worker_profile,
            "maximum_user_content_tokens",
        )
    if (
        policy.reserved_system_instruction_tokens + policy.maximum_user_content_tokens
        > policy.maximum_prompt_tokens
    ):
        _raise(ProviderWorkerRequestBudgetError, worker_profile, "token_budget")
    if policy.maximum_prompt_tokens != MAXIMUM_PROMPT_TOKENS:
        _raise(ProviderWorkerRequestBudgetError, worker_profile, "prompt_bound")
    if policy.reserved_system_instruction_tokens != RESERVED_SYSTEM_INSTRUCTION_TOKENS:
        _raise(ProviderWorkerRequestBudgetError, worker_profile, "system_bound")
    if policy.maximum_user_content_tokens != MAXIMUM_USER_CONTENT_TOKENS:
        _raise(ProviderWorkerRequestBudgetError, worker_profile, "user_bound")


def _validate_result_policy(
    worker_profile: BoundedProviderWorkerProfile,
    provider_profile: object,
) -> None:
    policy = worker_profile.result_policy
    generation = provider_profile.generation_policy
    if policy.maximum_output_tokens != generation.maximum_output_tokens:
        _raise(ProviderWorkerResultBudgetError, worker_profile, "maximum_output_tokens")
    if policy.maximum_output_tokens != MAXIMUM_OUTPUT_TOKENS:
        _raise(ProviderWorkerResultBudgetError, worker_profile, "output_bound")


def _validate_timeout_policy(
    worker_profile: BoundedProviderWorkerProfile,
    provider_profile: object,
) -> None:
    policy = worker_profile.timeout_policy
    provider_timeout = provider_profile.timeout_policy
    if policy.connection_timeout_ms > provider_timeout.connection_timeout_ms:
        _raise(ProviderWorkerTimeoutPolicyError, worker_profile, "connection_timeout")
    if policy.response_header_timeout_ms > provider_timeout.response_header_timeout_ms:
        _raise(
            ProviderWorkerTimeoutPolicyError, worker_profile, "response_header_timeout"
        )
    if (
        policy.complete_inference_timeout_ms
        > provider_timeout.complete_inference_timeout_ms
    ):
        _raise(
            ProviderWorkerTimeoutPolicyError,
            worker_profile,
            "complete_inference_timeout",
        )
    if policy.cancellation_deadline_ms > provider_timeout.cancellation_deadline_ms:
        _raise(
            ProviderWorkerTimeoutPolicyError, worker_profile, "cancellation_deadline"
        )
    if policy.connection_timeout_ms != CONNECTION_TIMEOUT_MS:
        _raise(ProviderWorkerTimeoutPolicyError, worker_profile, "connection_bound")
    if policy.response_header_timeout_ms != RESPONSE_HEADER_TIMEOUT_MS:
        _raise(ProviderWorkerTimeoutPolicyError, worker_profile, "header_bound")
    if policy.complete_inference_timeout_ms != COMPLETE_INFERENCE_TIMEOUT_MS:
        _raise(ProviderWorkerTimeoutPolicyError, worker_profile, "complete_bound")


def _raise(
    error_type: type[ProviderWorkerError],
    worker_profile: BoundedProviderWorkerProfile,
    validation_category: str,
    *,
    provider_profile_id: str | None = None,
) -> None:
    raise error_type(
        worker_profile_id=worker_profile.profile_id,
        provider_profile_id=provider_profile_id
        or worker_profile.provider_runtime_profile_id,
        validation_category=validation_category,
    )


__all__ = [
    "ProviderWorkerConcurrencyPolicyError",
    "ProviderWorkerCredentialRequirementError",
    "ProviderWorkerFeaturePolicyError",
    "ProviderWorkerProfileValidationError",
    "ProviderWorkerProviderProfileMismatchError",
    "ProviderWorkerQueuePolicyError",
    "ProviderWorkerRequestBudgetError",
    "ProviderWorkerResolutionError",
    "ProviderWorkerResultBudgetError",
    "ProviderWorkerTimeoutPolicyError",
    "resolve_provider_worker_profile",
]
