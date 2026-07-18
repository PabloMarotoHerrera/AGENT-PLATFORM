"""Contract errors for the governed runtime adapter package."""

from __future__ import annotations

from hermes_cli.agent_platform.runtime_adapter.enums import (
    RuntimeLifecycleAction,
    RuntimeLifecycleState,
)


class RuntimeAdapterContractError(RuntimeError):
    """Base class for bounded runtime-adapter contract errors."""

    error_code = "runtime_adapter_contract_error"


class RuntimeContractValidationError(RuntimeAdapterContractError):
    """Raised when runtime-adapter contract input is invalid."""

    error_code = "runtime_contract_validation_error"


class InvalidRuntimeTransitionError(RuntimeAdapterContractError):
    """Raised for a lifecycle action that is not valid from the current state."""

    error_code = "invalid_runtime_transition"

    current_state: RuntimeLifecycleState
    requested_action: RuntimeLifecycleAction
    allowed_actions: tuple[RuntimeLifecycleAction, ...]

    def __init__(
        self,
        *,
        current_state: RuntimeLifecycleState,
        requested_action: RuntimeLifecycleAction,
        allowed_actions: tuple[RuntimeLifecycleAction, ...],
    ) -> None:
        self.current_state = current_state
        self.requested_action = requested_action
        self.allowed_actions = allowed_actions
        allowed = ",".join(action.value for action in allowed_actions) or "none"
        super().__init__(
            "Invalid runtime transition: "
            f"state={current_state.value} action={requested_action.value} allowed={allowed}"
        )
