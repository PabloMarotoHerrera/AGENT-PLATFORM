"""Pure lifecycle state machine for runtime-adapter contracts."""

from __future__ import annotations

from hermes_cli.agent_platform.runtime_adapter.enums import (
    RuntimeLifecycleAction,
    RuntimeLifecycleState,
)
from hermes_cli.agent_platform.runtime_adapter.errors import (
    InvalidRuntimeTransitionError,
)


_TRANSITIONS: dict[
    RuntimeLifecycleState,
    tuple[tuple[RuntimeLifecycleAction, RuntimeLifecycleState], ...],
] = {
    RuntimeLifecycleState.CREATED: (
        (RuntimeLifecycleAction.VALIDATE, RuntimeLifecycleState.VALIDATING),
        (
            RuntimeLifecycleAction.REQUEST_CANCELLATION,
            RuntimeLifecycleState.CANCELLATION_REQUESTED,
        ),
        (RuntimeLifecycleAction.MARK_FAILED, RuntimeLifecycleState.FAILED),
    ),
    RuntimeLifecycleState.VALIDATING: (
        (RuntimeLifecycleAction.START, RuntimeLifecycleState.STARTING),
        (
            RuntimeLifecycleAction.REQUEST_CANCELLATION,
            RuntimeLifecycleState.CANCELLATION_REQUESTED,
        ),
        (RuntimeLifecycleAction.MARK_FAILED, RuntimeLifecycleState.FAILED),
    ),
    RuntimeLifecycleState.STARTING: (
        (
            RuntimeLifecycleAction.WAIT_FOR_READINESS,
            RuntimeLifecycleState.WAITING_FOR_READINESS,
        ),
        (
            RuntimeLifecycleAction.REQUEST_CANCELLATION,
            RuntimeLifecycleState.CANCELLATION_REQUESTED,
        ),
        (RuntimeLifecycleAction.BEGIN_STOP, RuntimeLifecycleState.STOPPING),
        (RuntimeLifecycleAction.MARK_FAILED, RuntimeLifecycleState.FAILED),
    ),
    RuntimeLifecycleState.WAITING_FOR_READINESS: (
        (RuntimeLifecycleAction.MARK_READY, RuntimeLifecycleState.READY),
        (
            RuntimeLifecycleAction.REQUEST_CANCELLATION,
            RuntimeLifecycleState.CANCELLATION_REQUESTED,
        ),
        (RuntimeLifecycleAction.BEGIN_STOP, RuntimeLifecycleState.STOPPING),
        (RuntimeLifecycleAction.MARK_FAILED, RuntimeLifecycleState.FAILED),
    ),
    RuntimeLifecycleState.READY: (
        (
            RuntimeLifecycleAction.REQUEST_CANCELLATION,
            RuntimeLifecycleState.CANCELLATION_REQUESTED,
        ),
        (RuntimeLifecycleAction.BEGIN_STOP, RuntimeLifecycleState.STOPPING),
        (RuntimeLifecycleAction.MARK_FAILED, RuntimeLifecycleState.FAILED),
    ),
    RuntimeLifecycleState.CANCELLATION_REQUESTED: (
        (
            RuntimeLifecycleAction.REQUEST_CANCELLATION,
            RuntimeLifecycleState.CANCELLATION_REQUESTED,
        ),
        (RuntimeLifecycleAction.BEGIN_STOP, RuntimeLifecycleState.STOPPING),
        (RuntimeLifecycleAction.MARK_CANCELLED, RuntimeLifecycleState.CANCELLED),
        (RuntimeLifecycleAction.MARK_FAILED, RuntimeLifecycleState.FAILED),
    ),
    RuntimeLifecycleState.STOPPING: (
        (RuntimeLifecycleAction.BEGIN_STOP, RuntimeLifecycleState.STOPPING),
        (RuntimeLifecycleAction.REQUEST_CANCELLATION, RuntimeLifecycleState.STOPPING),
        (RuntimeLifecycleAction.MARK_STOPPED, RuntimeLifecycleState.STOPPED),
        (RuntimeLifecycleAction.MARK_CANCELLED, RuntimeLifecycleState.CANCELLED),
        (RuntimeLifecycleAction.MARK_FAILED, RuntimeLifecycleState.FAILED),
    ),
    RuntimeLifecycleState.STOPPED: (
        (RuntimeLifecycleAction.BEGIN_STOP, RuntimeLifecycleState.STOPPED),
        (RuntimeLifecycleAction.REQUEST_CANCELLATION, RuntimeLifecycleState.STOPPED),
        (RuntimeLifecycleAction.BEGIN_ROLLBACK, RuntimeLifecycleState.ROLLBACK_PENDING),
    ),
    RuntimeLifecycleState.CANCELLED: (
        (RuntimeLifecycleAction.REQUEST_CANCELLATION, RuntimeLifecycleState.CANCELLED),
        (RuntimeLifecycleAction.BEGIN_STOP, RuntimeLifecycleState.CANCELLED),
        (RuntimeLifecycleAction.BEGIN_ROLLBACK, RuntimeLifecycleState.ROLLBACK_PENDING),
    ),
    RuntimeLifecycleState.FAILED: (
        (RuntimeLifecycleAction.BEGIN_ROLLBACK, RuntimeLifecycleState.ROLLBACK_PENDING),
    ),
    RuntimeLifecycleState.ROLLBACK_PENDING: (
        (
            RuntimeLifecycleAction.BEGIN_ROLLBACK,
            RuntimeLifecycleState.ROLLBACK_PENDING,
        ),
        (RuntimeLifecycleAction.MARK_ROLLED_BACK, RuntimeLifecycleState.ROLLED_BACK),
        (
            RuntimeLifecycleAction.MARK_ROLLBACK_FAILED,
            RuntimeLifecycleState.ROLLBACK_FAILED,
        ),
    ),
    RuntimeLifecycleState.ROLLED_BACK: (
        (RuntimeLifecycleAction.BEGIN_STOP, RuntimeLifecycleState.ROLLED_BACK),
        (
            RuntimeLifecycleAction.REQUEST_CANCELLATION,
            RuntimeLifecycleState.ROLLED_BACK,
        ),
        (RuntimeLifecycleAction.BEGIN_ROLLBACK, RuntimeLifecycleState.ROLLED_BACK),
        (RuntimeLifecycleAction.MARK_ROLLED_BACK, RuntimeLifecycleState.ROLLED_BACK),
    ),
    RuntimeLifecycleState.ROLLBACK_FAILED: (
        (RuntimeLifecycleAction.BEGIN_STOP, RuntimeLifecycleState.ROLLBACK_FAILED),
        (
            RuntimeLifecycleAction.REQUEST_CANCELLATION,
            RuntimeLifecycleState.ROLLBACK_FAILED,
        ),
        (
            RuntimeLifecycleAction.MARK_ROLLBACK_FAILED,
            RuntimeLifecycleState.ROLLBACK_FAILED,
        ),
    ),
}

_TRANSITION_LOOKUP = {state: dict(actions) for state, actions in _TRANSITIONS.items()}

_TERMINAL_WITHOUT_ROLLBACK = frozenset({
    RuntimeLifecycleState.STOPPED,
    RuntimeLifecycleState.CANCELLED,
    RuntimeLifecycleState.FAILED,
    RuntimeLifecycleState.ROLLED_BACK,
    RuntimeLifecycleState.ROLLBACK_FAILED,
})
_TERMINAL_WITH_ROLLBACK = frozenset({
    RuntimeLifecycleState.ROLLED_BACK,
    RuntimeLifecycleState.ROLLBACK_FAILED,
})


def allowed_runtime_actions(
    state: RuntimeLifecycleState,
) -> tuple[RuntimeLifecycleAction, ...]:
    """Return actions accepted from ``state`` in deterministic table order."""

    return tuple(action for action, _ in _TRANSITIONS[state])


def transition_runtime_state(
    current_state: RuntimeLifecycleState,
    action: RuntimeLifecycleAction,
) -> RuntimeLifecycleState:
    """Apply one validated lifecycle transition."""

    target = _TRANSITION_LOOKUP[current_state].get(action)
    if target is None:
        raise InvalidRuntimeTransitionError(
            current_state=current_state,
            requested_action=action,
            allowed_actions=allowed_runtime_actions(current_state),
        )
    return target


def is_runtime_terminal(
    state: RuntimeLifecycleState,
    *,
    rollback_required: bool,
) -> bool:
    """Return whether ``state`` is terminal under the requested rollback policy."""

    terminal = (
        _TERMINAL_WITH_ROLLBACK if rollback_required else _TERMINAL_WITHOUT_ROLLBACK
    )
    return state in terminal
