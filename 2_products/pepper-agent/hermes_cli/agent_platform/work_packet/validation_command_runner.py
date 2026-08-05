"""Governed validation-command runner for completed WorkPacket execution.

P17.4 runs only exact command-validation steps compiled into a WorkPacket,
after explicit human authorization. It never invokes a shell, never generates
commands, and never grants provider, model, Git, Docker, or Graphify authority.
"""

from __future__ import annotations

from enum import Enum
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import threading
import time
from typing import Annotated, Literal, TypeAlias

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StrictBool,
    StringConstraints,
    field_validator,
    model_validator,
)

from hermes_cli.agent_platform.work_packet.compiler import (
    WorkPacketCompilationResult,
    WorkPacketValidationKind,
    validate_work_packet,
)
from hermes_cli.agent_platform.work_packet.single_agent_execution import (
    SingleAgentExecutionResult,
    SingleAgentExecutionState,
    validate_single_agent_execution_result,
)
from hermes_cli.agent_platform.work_packet.tool_permissions import (
    ToolPermissionOperation,
    ToolPermissionProfileResult,
    validate_tool_permission_profile,
)
from hermes_cli.agent_platform.work_packet.workspace_allocator import (
    WorkspaceAllocation,
    WorkspaceAllocationResult,
    WorkspaceInspectionEvidence,
    inspect_human_provisioned_workspace,
    validate_workspace_allocation,
)

VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION = 1
VALIDATION_COMMAND_RUNNER_POLICY_ID = (
    "pepper-exact-human-authorized-validation-command-runner-v1"
)

ENVIRONMENT_POLICY_ID = "pepper-minimal-validation-command-environment-v1"
MAX_STDOUT_BYTES = 262144
MAX_STDERR_BYTES = 262144
RETAINED_STDOUT_BYTES = 65536
RETAINED_STDERR_BYTES = 65536
OUTPUT_READER_THREADS = 2
MAX_ARGV_TOKENS = 128
MAX_SOURCE_COMMAND_CHARACTERS = 8192
OUTPUT_CHUNK_BYTES = 8192
TERMINATION_GRACE_SECONDS = 2.0

BINDING_DIGEST_ALGORITHM = "agent-platform-validation-command-runtime-binding-sha256-v1"
SPECIFICATION_DIGEST_ALGORITHM = (
    "agent-platform-validation-command-specification-sha256-v1"
)
AUTHORIZATION_DIGEST_ALGORITHM = (
    "agent-platform-validation-command-runner-authorization-sha256-v1"
)
STREAM_DIGEST_ALGORITHM = "agent-platform-validation-command-captured-stream-sha256-v1"
EVIDENCE_DIGEST_ALGORITHM = (
    "agent-platform-validation-command-execution-evidence-sha256-v1"
)
SESSION_DIGEST_ALGORITHM = "agent-platform-validation-command-runner-session-sha256-v1"
EXECUTION_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-validation-command-execution-result-sha256-v1"
)
RUNNER_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-validation-command-runner-result-sha256-v1"
)

_DIGEST_PATTERN = r"^[a-f0-9]{64}$"
_COMMAND_ID_PATTERN = r"^VCMD-[0-9]{3}$"
_BINDING_ID_PATTERN = r"^VCB-P[1-9][0-9]{0,3}(?:-[A-Z0-9]+)+-R[0-9]{4}-[a-f0-9]{12}$"
_SESSION_ID_PATTERN = r"^VCR-P[1-9][0-9]{0,3}(?:-[A-Z0-9]+)+-R[0-9]{4}-[a-f0-9]{12}$"
_IDENTIFIER_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9._:@+-]{2,95}$"
_DRIVE_PATH_PATTERN = re.compile(r"^[A-Za-z]:")
_ENV_ASSIGNMENT_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
_CONTROL_CHARACTER_PATTERN = re.compile(r"[\x00-\x1f\x7f]")
_ANSI_ESCAPE_PATTERN = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
_SECRET_PATTERNS = (
    re.compile(r"Authorization:\s*Bearer\s+\S+", re.IGNORECASE),
    re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]{16,}", re.IGNORECASE),
    re.compile(r"access_token\s*=\s*[^\s]+", re.IGNORECASE),
    re.compile(r"refresh_token\s*=\s*[^\s]+", re.IGNORECASE),
    re.compile(r"password\s*=\s*[^\s]+", re.IGNORECASE),
    re.compile(r"client_secret\s*=\s*[^\s]+", re.IGNORECASE),
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
        re.DOTALL,
    ),
    re.compile(r"Cookie:\s*[^\n;]*auth[^\n]*", re.IGNORECASE),
)
_SECRET_COMMAND_MARKERS = (
    "Authorization: Bearer",
    "access_token=",
    "refresh_token=",
    "sk-",
    "-----BEGIN PRIVATE KEY-----",
    "-----BEGIN RSA PRIVATE KEY-----",
    "password=",
    "client_secret=",
)
_FORBIDDEN_SHELL_MARKERS = ("||", "&&", "<<", ">>", "$(", "${")
_FORBIDDEN_SHELL_TOKENS = ("|", "&", ";", ">", "<", "`")
_FIXED_ENVIRONMENT = (
    ("NO_COLOR", "1"),
    ("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "1"),
    ("PYTHONDONTWRITEBYTECODE", "1"),
    ("PYTHONHASHSEED", "0"),
    ("PYTHONIOENCODING", "utf-8"),
    ("PYTHONNOUSERSITE", "1"),
    ("PYTHONUTF8", "1"),
)
_INHERITED_ENVIRONMENT_ALLOWLIST = (
    "LANG",
    "LC_ALL",
    "SYSTEMROOT",
    "TEMP",
    "TMP",
    "TMPDIR",
    "WINDIR",
)


class ValidationCommandRunnerError(ValueError):
    """Base error for governed validation-command runner failures."""


class ValidationCommandRunnerInputError(ValidationCommandRunnerError):
    """Raised when runner inputs are structurally invalid."""


class ValidationCommandRunnerAuthorizationError(ValidationCommandRunnerError):
    """Raised when human validation-command authorization is invalid."""


class ValidationCommandRunnerIntegrityError(ValidationCommandRunnerError):
    """Raised when deterministic runner evidence fails integrity checks."""


class ValidationCommandPolicyError(ValidationCommandRunnerError):
    """Raised when a WorkPacket command violates the P17.4 command policy."""


class ValidationCommandExecutionError(ValidationCommandRunnerError):
    """Raised when a governed validation subprocess cannot be controlled."""


class ValidationCommandRunnerStateError(ValidationCommandRunnerError):
    """Raised when a runner session transition is not allowed."""


class ValidationCommandModule(str, Enum):
    PYTEST = "pytest"
    UNITTEST = "unittest"
    RUFF_CHECK = "ruff_check"
    RUFF_FORMAT_CHECK = "ruff_format_check"


class ValidationCommandRunnerState(str, Enum):
    PREPARED = "prepared"
    ACTIVE = "active"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class ValidationCommandDisposition(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    TIMED_OUT = "timed_out"
    OUTPUT_LIMIT_EXCEEDED = "output_limit_exceeded"
    CANCELLED = "cancelled"


class ValidationCommandFailureReason(str, Enum):
    NONE = "none"
    NONZERO_EXIT = "nonzero_exit"
    TIMEOUT = "timeout"
    OUTPUT_LIMIT = "output_limit"
    LAUNCH_ERROR = "launch_error"
    CANCELLED = "cancelled"


class ValidationCommandStreamKind(str, Enum):
    STDOUT = "stdout"
    STDERR = "stderr"


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


def _reject_identifier_whitespace(value: object) -> object:
    if isinstance(value, str) and any(character.isspace() for character in value):
        raise ValueError("identifier must not contain whitespace")
    return value


def _validate_identifier(value: str) -> str:
    if _is_shadow_identifier(value):
        raise ValueError("shadow authorizer is not authorized")
    lowered = value.casefold()
    for marker in ("token", "secret", "password", "credential", "bearer"):
        if marker in lowered:
            raise ValueError("identifier must not contain credential markers")
    return value


def _validate_bounded_command(value: str) -> str:
    if len(value) > MAX_SOURCE_COMMAND_CHARACTERS:
        raise ValueError("source command exceeds maximum length")
    return _reject_nul(value)


DigestText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=_DIGEST_PATTERN),
]
BoundedText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=1024),
    AfterValidator(_reject_nul),
]
BoundedIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=3, max_length=96, pattern=_IDENTIFIER_PATTERN),
    AfterValidator(_validate_identifier),
]
CommandIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=8, max_length=8, pattern=_COMMAND_ID_PATTERN),
]
BindingIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=28, max_length=96, pattern=_BINDING_ID_PATTERN),
]
SessionIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=28, max_length=96, pattern=_SESSION_ID_PATTERN),
]
SourceCommandText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=1, max_length=MAX_SOURCE_COMMAND_CHARACTERS),
    AfterValidator(_validate_bounded_command),
]
ShortText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=1, max_length=512),
    AfterValidator(_reject_nul),
]


class _ValidationCommandModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
        protected_namespaces=(),
    )


class ValidationCommandRuntimeBinding(_ValidationCommandModel):
    schema_version: Literal[1] = VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION
    binding_id: BindingIdentifier
    python_executable: ShortText
    resolved_python_executable: ShortText
    shell: Literal[False] = False
    stdin_disabled: Literal[True] = True
    working_directory: ShortText
    environment_policy_id: Literal[
        "pepper-minimal-validation-command-environment-v1"
    ] = ENVIRONMENT_POLICY_ID
    max_stdout_bytes: Literal[262144] = MAX_STDOUT_BYTES
    max_stderr_bytes: Literal[262144] = MAX_STDERR_BYTES
    retained_stdout_bytes: Literal[65536] = RETAINED_STDOUT_BYTES
    retained_stderr_bytes: Literal[65536] = RETAINED_STDERR_BYTES
    output_reader_threads: Literal[2] = OUTPUT_READER_THREADS
    network_isolation_guaranteed: Literal[False] = False
    process_tree_isolation_guaranteed: Literal[False] = False
    binding_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_binding(self) -> ValidationCommandRuntimeBinding:
        if self.binding_SHA256 != _runtime_binding_digest(self):
            raise ValueError("binding_SHA256 must match runtime binding digest")
        if self.binding_id != _runtime_binding_id_from_binding(self):
            raise ValueError("binding_id must match runtime binding digest")
        return self


class ValidationCommandAuthorizationRequest(_ValidationCommandModel):
    validation_id: BoundedText
    timeout_seconds: int = Field(ge=1, le=600, strict=True)
    expected_exit_codes: tuple[int, ...] = (0,)

    @field_validator("expected_exit_codes", mode="before")
    @classmethod
    def _normalize_exit_codes(cls, value: object) -> tuple[int, ...]:
        if value is None:
            return (0,)
        if isinstance(value, int):
            values = (value,)
        else:
            values = tuple(value)  # type: ignore[arg-type]
        if not values:
            raise ValueError("expected exit codes must not be empty")
        normalized: list[int] = []
        for item in values:
            if not isinstance(item, int) or isinstance(item, bool):
                raise ValueError("expected exit codes must be integers")
            if item < 0 or item > 255:
                raise ValueError("expected exit code out of range")
            normalized.append(item)
        if len(normalized) != len(frozenset(normalized)):
            raise ValueError("expected exit codes must be unique")
        return tuple(sorted(normalized))

    @field_validator("expected_exit_codes", mode="after")
    @classmethod
    def _validate_exit_codes(cls, value: tuple[int, ...]) -> tuple[int, ...]:
        if not value:
            raise ValueError("expected exit codes must not be empty")
        if value != tuple(sorted(value)) or len(value) != len(frozenset(value)):
            raise ValueError("expected exit codes must be sorted and unique")
        return value


class ValidationCommandSpecification(_ValidationCommandModel):
    schema_version: Literal[1] = VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION
    command_id: CommandIdentifier
    validation_id: BoundedText
    module: ValidationCommandModule
    source_command: SourceCommandText
    source_command_SHA256: DigestText
    effective_argv: tuple[ShortText, ...] = Field(min_length=3)
    working_directory: ShortText
    timeout_seconds: int = Field(ge=1, le=600, strict=True)
    expected_exit_codes: tuple[int, ...] = Field(min_length=1)
    max_stdout_bytes: Literal[262144] = MAX_STDOUT_BYTES
    max_stderr_bytes: Literal[262144] = MAX_STDERR_BYTES
    specification_SHA256: DigestText

    @field_validator("effective_argv", mode="after")
    @classmethod
    def _validate_effective_argv(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) > MAX_ARGV_TOKENS:
            raise ValueError("effective argv exceeds token bound")
        for token in value:
            _validate_argv_token(token)
        return value

    @field_validator("expected_exit_codes", mode="before")
    @classmethod
    def _normalize_exit_codes(cls, value: object) -> tuple[int, ...]:
        return ValidationCommandAuthorizationRequest._normalize_exit_codes(value)

    @model_validator(mode="after")
    def _validate_specification(self) -> ValidationCommandSpecification:
        if self.source_command_SHA256 != _sha256_text(self.source_command):
            raise ValueError("source_command_SHA256 must match source command")
        if self.specification_SHA256 != _specification_digest(self):
            raise ValueError("specification_SHA256 must match specification digest")
        if self.command_id != _command_id(_command_index(self.command_id)):
            raise ValueError("command_id must be canonical")
        return self


class ValidationCommandRunnerAuthorization(_ValidationCommandModel):
    schema_version: Literal[1] = VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION
    execution_authorized: Literal[True] = True
    synthetic: Literal[False] = False
    authorizer_id: BoundedIdentifier
    authorization_reference: BoundedText
    rationale: BoundedText
    risk_acknowledgement: BoundedText
    work_packet_id: str
    work_packet_SHA256: DigestText
    allocation_id: str
    allocation_SHA256: DigestText
    profile_id: str
    profile_SHA256: DigestText
    single_agent_result_SHA256: DigestText
    runtime_binding_SHA256: DigestText
    command_specifications: tuple[ValidationCommandSpecification, ...] = Field(
        min_length=1
    )
    authorization_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_authorization(self) -> ValidationCommandRunnerAuthorization:
        _validate_specification_sequence(self.command_specifications)
        if self.authorization_SHA256 != _authorization_digest(self):
            raise ValueError("authorization_SHA256 must match authorization digest")
        return self


class ValidationCommandRunnerRequest(_ValidationCommandModel):
    schema_version: Literal[1] = VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION
    policy_id: Literal["pepper-exact-human-authorized-validation-command-runner-v1"] = (
        VALIDATION_COMMAND_RUNNER_POLICY_ID
    )
    compilation_result: WorkPacketCompilationResult
    allocation_result: WorkspaceAllocationResult
    profile_result: ToolPermissionProfileResult
    single_agent_execution_result: SingleAgentExecutionResult
    runtime_binding: ValidationCommandRuntimeBinding
    runner_authorization: ValidationCommandRunnerAuthorization

    @model_validator(mode="after")
    def _validate_request(self) -> ValidationCommandRunnerRequest:
        _validate_request_bindings(self, error_type=ValueError)
        return self


class ValidationCommandCapturedStream(_ValidationCommandModel):
    stream: ValidationCommandStreamKind
    retained_text: str | None
    raw_byte_count: int = Field(ge=0, strict=True)
    retained_byte_count: int = Field(ge=0, strict=True)
    raw_SHA256: DigestText
    truncated: StrictBool
    redaction_count: int = Field(ge=0, strict=True)
    decode_replacement_count: int = Field(ge=0, strict=True)
    stream_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_stream(self) -> ValidationCommandCapturedStream:
        if self.raw_byte_count == 0:
            if self.retained_text is not None or self.retained_byte_count != 0:
                raise ValueError("empty stream must not retain text")
        elif self.retained_text is None:
            raise ValueError("nonempty stream must retain sanitized text")
        if self.stream_SHA256 != _captured_stream_digest(self):
            raise ValueError("stream_SHA256 must match stream digest")
        return self


class ValidationCommandExecutionEvidence(_ValidationCommandModel):
    schema_version: Literal[1] = VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION
    command_id: CommandIdentifier
    validation_id: BoundedText
    module: ValidationCommandModule
    disposition: ValidationCommandDisposition
    failure_reason: ValidationCommandFailureReason
    exit_code: int | None = Field(default=None, ge=0, le=255)
    timeout_seconds: int = Field(ge=1, le=600, strict=True)
    process_started: StrictBool
    terminate_requested: StrictBool
    kill_requested: StrictBool
    stdout_raw_byte_count: int = Field(ge=0, strict=True)
    stderr_raw_byte_count: int = Field(ge=0, strict=True)
    stdout_SHA256: DigestText
    stderr_SHA256: DigestText
    stdout_truncated: StrictBool
    stderr_truncated: StrictBool
    redaction_count: int = Field(ge=0, strict=True)
    workspace_status_entry_count_before: int | None = Field(default=None, ge=0)
    workspace_status_entry_count_after: int | None = Field(default=None, ge=0)
    workspace_inspection_before_SHA256: DigestText | None = None
    workspace_inspection_after_SHA256: DigestText | None = None
    evidence_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_evidence(self) -> ValidationCommandExecutionEvidence:
        if self.disposition is ValidationCommandDisposition.PASSED:
            if self.failure_reason is not ValidationCommandFailureReason.NONE:
                raise ValueError("passed evidence must not have failure reason")
            if not self.process_started or self.exit_code is None:
                raise ValueError("passed evidence requires process exit")
        elif self.disposition is ValidationCommandDisposition.FAILED:
            if self.failure_reason not in {
                ValidationCommandFailureReason.NONZERO_EXIT,
                ValidationCommandFailureReason.LAUNCH_ERROR,
            }:
                raise ValueError("failed evidence reason is invalid")
        elif self.disposition is ValidationCommandDisposition.TIMED_OUT:
            if (
                self.failure_reason is not ValidationCommandFailureReason.TIMEOUT
                or not self.process_started
                or not self.terminate_requested
            ):
                raise ValueError("timeout evidence posture is invalid")
        elif self.disposition is ValidationCommandDisposition.OUTPUT_LIMIT_EXCEEDED:
            if (
                self.failure_reason is not ValidationCommandFailureReason.OUTPUT_LIMIT
                or not self.process_started
                or not self.terminate_requested
            ):
                raise ValueError("output limit evidence posture is invalid")
        elif self.disposition is ValidationCommandDisposition.CANCELLED:
            if (
                self.failure_reason is not ValidationCommandFailureReason.CANCELLED
                or self.process_started
                or self.exit_code is not None
                or self.workspace_inspection_before_SHA256 is not None
                or self.workspace_inspection_after_SHA256 is not None
            ):
                raise ValueError("cancelled evidence posture is invalid")
        if self.evidence_SHA256 != _execution_evidence_digest(self):
            raise ValueError("evidence_SHA256 must match execution evidence digest")
        return self


class ValidationCommandRunnerSession(_ValidationCommandModel):
    schema_version: Literal[1] = VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION
    session_id: SessionIdentifier
    policy_id: Literal["pepper-exact-human-authorized-validation-command-runner-v1"] = (
        VALIDATION_COMMAND_RUNNER_POLICY_ID
    )
    state: ValidationCommandRunnerState
    work_packet_id: str
    work_packet_SHA256: DigestText
    allocation_id: str
    allocation_SHA256: DigestText
    profile_id: str
    profile_SHA256: DigestText
    single_agent_result_SHA256: DigestText
    runtime_binding_SHA256: DigestText
    authorization_SHA256: DigestText
    next_command_index: int = Field(ge=0, strict=True)
    completed_command_ids: tuple[CommandIdentifier, ...] = ()
    passed_validation_ids: tuple[str, ...] = ()
    manual_validation_ids_pending: tuple[str, ...] = ()
    command_evidence: tuple[ValidationCommandExecutionEvidence, ...] = ()
    execution_active: StrictBool
    validation_command_runner_requirement_satisfied: StrictBool
    result_envelopes_ready: Literal[False] = False
    diff_artifact_review_ready: Literal[False] = False
    human_git_handoff_ready: Literal[False] = False
    session_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_session(self) -> ValidationCommandRunnerSession:
        passed = tuple(
            evidence
            for evidence in self.command_evidence
            if evidence.disposition is ValidationCommandDisposition.PASSED
        )
        if self.completed_command_ids != tuple(item.command_id for item in passed):
            raise ValueError("completed command IDs must match passed evidence")
        if self.passed_validation_ids != tuple(item.validation_id for item in passed):
            raise ValueError("passed validation IDs must match passed evidence")
        if self.next_command_index < len(self.completed_command_ids):
            raise ValueError("next command index must not precede completed commands")
        if self.state in {
            ValidationCommandRunnerState.PREPARED,
            ValidationCommandRunnerState.ACTIVE,
        }:
            if not self.execution_active:
                raise ValueError("prepared or active session must be active")
            if self.validation_command_runner_requirement_satisfied:
                raise ValueError("active session must not satisfy requirement")
        elif self.state is ValidationCommandRunnerState.COMPLETED:
            if self.execution_active:
                raise ValueError("completed session must not be active")
            if not self.validation_command_runner_requirement_satisfied:
                raise ValueError("completed session must satisfy requirement")
        else:
            if (
                self.execution_active
                or self.validation_command_runner_requirement_satisfied
            ):
                raise ValueError("blocked or cancelled session must be inactive")
        if self.session_SHA256 != _session_digest(self):
            raise ValueError("session_SHA256 must match session digest")
        return self


class ValidationCommandExecutionRequest(_ValidationCommandModel):
    schema_version: Literal[1] = VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION
    runner_request: ValidationCommandRunnerRequest
    session: ValidationCommandRunnerSession
    cancellation_requested: StrictBool = False
    cancellation_reference: BoundedText | None = None

    @model_validator(mode="after")
    def _validate_request(self) -> ValidationCommandExecutionRequest:
        if self.cancellation_requested and self.cancellation_reference is None:
            raise ValueError("cancellation reference is required")
        if not self.cancellation_requested and self.cancellation_reference is not None:
            raise ValueError("cancellation reference requires cancellation request")
        _validate_session_request_binding(
            session=self.session,
            request=self.runner_request,
            error_type=ValueError,
        )
        return self


class ValidationCommandExecutionResult(_ValidationCommandModel):
    schema_version: Literal[1] = VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION
    disposition: ValidationCommandDisposition
    specification: ValidationCommandSpecification
    updated_session: ValidationCommandRunnerSession
    stdout: ValidationCommandCapturedStream
    stderr: ValidationCommandCapturedStream
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> ValidationCommandExecutionResult:
        if self.result_SHA256 != _execution_result_digest(self):
            raise ValueError("result_SHA256 must match execution result digest")
        return self


class ValidationCommandRunnerResult(_ValidationCommandModel):
    schema_version: Literal[1] = VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION
    policy_id: Literal["pepper-exact-human-authorized-validation-command-runner-v1"] = (
        VALIDATION_COMMAND_RUNNER_POLICY_ID
    )
    state: Literal[ValidationCommandRunnerState.COMPLETED] = (
        ValidationCommandRunnerState.COMPLETED
    )
    session: ValidationCommandRunnerSession
    completed_command_count: int = Field(ge=1, strict=True)
    passed_validation_ids: tuple[str, ...]
    manual_validation_ids_pending: tuple[str, ...]
    validation_command_runner_requirement_satisfied: Literal[True] = True
    result_envelopes_ready: Literal[False] = False
    diff_artifact_review_ready: Literal[False] = False
    human_git_handoff_ready: Literal[False] = False
    provider_dispatch_count: Literal[0] = 0
    model_inference_count: Literal[0] = 0
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> ValidationCommandRunnerResult:
        if self.session.state is not ValidationCommandRunnerState.COMPLETED:
            raise ValueError("runner result requires completed session")
        if self.completed_command_count != len(self.session.completed_command_ids):
            raise ValueError("completed command count must match session")
        if self.passed_validation_ids != self.session.passed_validation_ids:
            raise ValueError("passed validation IDs must match session")
        if (
            self.manual_validation_ids_pending
            != self.session.manual_validation_ids_pending
        ):
            raise ValueError("manual validation IDs must match session")
        if self.result_SHA256 != _runner_result_digest(self):
            raise ValueError("result_SHA256 must match runner result digest")
        return self


def build_validation_command_runtime_binding(
    *,
    python_executable: str,
    allocation_result: WorkspaceAllocationResult,
) -> ValidationCommandRuntimeBinding:
    try:
        validate_workspace_allocation(allocation_result.allocation)
        executable = Path(python_executable)
        if not executable.is_absolute():
            raise ValidationCommandRunnerInputError(
                "python executable must be absolute"
            )
        if (
            not executable.exists()
            or not executable.is_file()
            or executable.is_symlink()
        ):
            raise ValidationCommandRunnerInputError(
                "python executable must be a regular file"
            )
        resolved = executable.resolve(strict=True)
        if resolved != executable.absolute():
            raise ValidationCommandRunnerInputError(
                "python executable must not be a symlink"
            )
        current = Path(sys.executable).resolve(strict=True)
        if executable.absolute() != current:
            raise ValidationCommandRunnerInputError(
                "python executable path must be current interpreter"
            )
        if resolved != current:
            raise ValidationCommandRunnerInputError(
                "python executable must be current interpreter"
            )
        if os.name != "nt" and not os.access(resolved, os.X_OK):
            raise ValidationCommandRunnerInputError(
                "python executable must be executable"
            )
        allocation = allocation_result.allocation
        working = Path(allocation.resolved_workspace_root).resolve(strict=True)
        if (
            working.as_posix()
            != Path(allocation.resolved_workspace_root).resolve(strict=True).as_posix()
        ):
            raise ValidationCommandRunnerInputError("working directory mismatch")
        base_record = {
            "schema_version": VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION,
            "python_executable": executable.as_posix(),
            "resolved_python_executable": resolved.as_posix(),
            "shell": False,
            "stdin_disabled": True,
            "working_directory": allocation.resolved_workspace_root,
            "environment_policy_id": ENVIRONMENT_POLICY_ID,
            "max_stdout_bytes": MAX_STDOUT_BYTES,
            "max_stderr_bytes": MAX_STDERR_BYTES,
            "retained_stdout_bytes": RETAINED_STDOUT_BYTES,
            "retained_stderr_bytes": RETAINED_STDERR_BYTES,
            "output_reader_threads": OUTPUT_READER_THREADS,
            "network_isolation_guaranteed": False,
            "process_tree_isolation_guaranteed": False,
        }
        digest = _digest(BINDING_DIGEST_ALGORITHM, base_record)
        data = {
            **base_record,
            "binding_id": _binding_id(
                ticket_id=allocation_result.allocation.work_packet_id.split("-R", 1)[
                    0
                ].replace("WP-", ""),
                publication_revision=_publication_revision_from_work_packet_id(
                    allocation_result.allocation.work_packet_id
                ),
                digest_text=digest,
            ),
        }
        return ValidationCommandRuntimeBinding(
            **data,
            binding_SHA256=_runtime_binding_digest_from_record(data),
        )
    except ValidationCommandRunnerError:
        raise
    except Exception as exc:
        raise ValidationCommandRunnerInputError("runtime binding failed") from exc


def build_validation_command_runner_authorization(
    *,
    authorizer_id: str,
    authorization_reference: str,
    rationale: str,
    risk_acknowledgement: str,
    compilation_result: WorkPacketCompilationResult,
    allocation_result: WorkspaceAllocationResult,
    profile_result: ToolPermissionProfileResult,
    single_agent_execution_result: SingleAgentExecutionResult,
    runtime_binding: ValidationCommandRuntimeBinding,
    authorization_requests: tuple[ValidationCommandAuthorizationRequest, ...],
) -> ValidationCommandRunnerAuthorization:
    try:
        _validate_prerequisites(
            compilation_result=compilation_result,
            allocation_result=allocation_result,
            profile_result=profile_result,
            single_agent_execution_result=single_agent_execution_result,
            runtime_binding=runtime_binding,
        )
        specifications = _build_command_specifications(
            compilation_result=compilation_result,
            allocation_result=allocation_result,
            runtime_binding=runtime_binding,
            authorization_requests=authorization_requests,
        )
        data = {
            "schema_version": VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION,
            "execution_authorized": True,
            "synthetic": False,
            "authorizer_id": authorizer_id,
            "authorization_reference": authorization_reference,
            "rationale": rationale,
            "risk_acknowledgement": risk_acknowledgement,
            "work_packet_id": compilation_result.work_packet.work_packet_id,
            "work_packet_SHA256": compilation_result.work_packet.work_packet_SHA256,
            "allocation_id": allocation_result.allocation.allocation_id,
            "allocation_SHA256": allocation_result.allocation.allocation_SHA256,
            "profile_id": profile_result.profile.profile_id,
            "profile_SHA256": profile_result.profile.profile_SHA256,
            "single_agent_result_SHA256": single_agent_execution_result.result_SHA256,
            "runtime_binding_SHA256": runtime_binding.binding_SHA256,
            "command_specifications": specifications,
        }
        return ValidationCommandRunnerAuthorization(
            **data,
            authorization_SHA256=_authorization_digest_from_record(data),
        )
    except ValidationCommandRunnerError:
        raise
    except Exception as exc:
        raise ValidationCommandRunnerAuthorizationError("authorization failed") from exc


def prepare_validation_command_runner(
    request: ValidationCommandRunnerRequest,
) -> ValidationCommandRunnerSession:
    try:
        validated = ValidationCommandRunnerRequest.model_validate(request)
        _validate_prerequisites(
            compilation_result=validated.compilation_result,
            allocation_result=validated.allocation_result,
            profile_result=validated.profile_result,
            single_agent_execution_result=validated.single_agent_execution_result,
            runtime_binding=validated.runtime_binding,
        )
        _validate_request_bindings(
            validated, error_type=ValidationCommandRunnerInputError
        )
        _reinspect_workspace(validated.allocation_result.allocation)
        specifications = validated.runner_authorization.command_specifications
        manual_ids = tuple(
            step.validation_id
            for step in validated.compilation_result.work_packet.validation_steps
            if step.kind is WorkPacketValidationKind.MANUAL
        )
        data = {
            "schema_version": VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION,
            "session_id": _session_id(
                ticket_id=validated.compilation_result.work_packet.ticket_id,
                publication_revision=validated.compilation_result.work_packet.publication_revision,
                digest_text=_authorization_digest(validated.runner_authorization),
            ),
            "policy_id": VALIDATION_COMMAND_RUNNER_POLICY_ID,
            "state": ValidationCommandRunnerState.PREPARED,
            "work_packet_id": validated.compilation_result.work_packet.work_packet_id,
            "work_packet_SHA256": validated.compilation_result.work_packet.work_packet_SHA256,
            "allocation_id": validated.allocation_result.allocation.allocation_id,
            "allocation_SHA256": validated.allocation_result.allocation.allocation_SHA256,
            "profile_id": validated.profile_result.profile.profile_id,
            "profile_SHA256": validated.profile_result.profile.profile_SHA256,
            "single_agent_result_SHA256": validated.single_agent_execution_result.result_SHA256,
            "runtime_binding_SHA256": validated.runtime_binding.binding_SHA256,
            "authorization_SHA256": validated.runner_authorization.authorization_SHA256,
            "next_command_index": 0,
            "completed_command_ids": (),
            "passed_validation_ids": (),
            "manual_validation_ids_pending": manual_ids,
            "command_evidence": (),
            "execution_active": True,
            "validation_command_runner_requirement_satisfied": False,
            "result_envelopes_ready": False,
            "diff_artifact_review_ready": False,
            "human_git_handoff_ready": False,
        }
        _ = specifications
        return ValidationCommandRunnerSession(
            **data,
            session_SHA256=_session_digest_from_record(data),
        )
    except ValidationCommandRunnerError:
        raise
    except Exception as exc:
        raise ValidationCommandRunnerInputError(
            "prepare validation runner failed"
        ) from exc


def execute_validation_command(
    request: ValidationCommandExecutionRequest,
) -> ValidationCommandExecutionResult:
    try:
        validated = ValidationCommandExecutionRequest.model_validate(request)
        session = validated.session
        runner_request = validated.runner_request
        if session.state in {
            ValidationCommandRunnerState.BLOCKED,
            ValidationCommandRunnerState.CANCELLED,
            ValidationCommandRunnerState.COMPLETED,
        }:
            raise ValidationCommandRunnerStateError("runner session cannot continue")
        specifications = runner_request.runner_authorization.command_specifications
        if session.next_command_index >= len(specifications):
            raise ValidationCommandRunnerStateError("no next validation command")
        specification = specifications[session.next_command_index]
        if validated.cancellation_requested:
            stdout = _empty_stream(ValidationCommandStreamKind.STDOUT)
            stderr = _empty_stream(ValidationCommandStreamKind.STDERR)
            evidence = _build_evidence(
                specification=specification,
                disposition=ValidationCommandDisposition.CANCELLED,
                failure_reason=ValidationCommandFailureReason.CANCELLED,
                exit_code=None,
                process_started=False,
                terminate_requested=False,
                kill_requested=False,
                stdout=stdout,
                stderr=stderr,
                before=None,
                after=None,
            )
            updated = _append_evidence(
                request=runner_request,
                session=session,
                evidence=evidence,
                state=ValidationCommandRunnerState.CANCELLED,
                advance=False,
            )
            return _execution_result(
                disposition=ValidationCommandDisposition.CANCELLED,
                specification=specification,
                updated_session=updated,
                stdout=stdout,
                stderr=stderr,
            )
        before = _reinspect_workspace(runner_request.allocation_result.allocation)
        _validate_runtime_binding_current(runner_request.runtime_binding)
        environment = _minimal_environment()
        launch = _launch_and_capture(specification, environment)
        after = _reinspect_workspace(runner_request.allocation_result.allocation)
        stdout = _captured_stream(
            ValidationCommandStreamKind.STDOUT,
            launch.stdout_raw,
            runner_request.runtime_binding.retained_stdout_bytes,
            raw_byte_count=launch.stdout_raw_byte_count,
            raw_SHA256=launch.stdout_raw_SHA256,
        )
        stderr = _captured_stream(
            ValidationCommandStreamKind.STDERR,
            launch.stderr_raw,
            runner_request.runtime_binding.retained_stderr_bytes,
            raw_byte_count=launch.stderr_raw_byte_count,
            raw_SHA256=launch.stderr_raw_SHA256,
        )
        disposition, reason = _disposition_for_launch(specification, launch)
        evidence = _build_evidence(
            specification=specification,
            disposition=disposition,
            failure_reason=reason,
            exit_code=launch.exit_code,
            process_started=launch.process_started,
            terminate_requested=launch.terminate_requested,
            kill_requested=launch.kill_requested,
            stdout=stdout,
            stderr=stderr,
            before=before,
            after=after,
        )
        updated = _append_evidence(
            request=runner_request,
            session=session,
            evidence=evidence,
            state=ValidationCommandRunnerState.ACTIVE
            if disposition is ValidationCommandDisposition.PASSED
            else ValidationCommandRunnerState.BLOCKED,
            advance=disposition is ValidationCommandDisposition.PASSED,
        )
        return _execution_result(
            disposition=disposition,
            specification=specification,
            updated_session=updated,
            stdout=stdout,
            stderr=stderr,
        )
    except ValidationCommandRunnerError:
        raise
    except Exception as exc:
        raise ValidationCommandExecutionError(
            "execute validation command failed"
        ) from exc


def complete_validation_command_runner(
    session: ValidationCommandRunnerSession,
) -> ValidationCommandRunnerResult:
    try:
        validated = ValidationCommandRunnerSession.model_validate(session)
        if validated.state not in {
            ValidationCommandRunnerState.PREPARED,
            ValidationCommandRunnerState.ACTIVE,
        }:
            raise ValidationCommandRunnerStateError("runner session cannot complete")
        if not validated.command_evidence:
            raise ValidationCommandRunnerStateError("runner session has no evidence")
        if any(
            evidence.disposition is not ValidationCommandDisposition.PASSED
            for evidence in validated.command_evidence
        ):
            raise ValidationCommandRunnerStateError("all command evidence must pass")
        if validated.next_command_index != len(validated.command_evidence):
            raise ValidationCommandRunnerStateError(
                "runner command sequence incomplete"
            )
        completed_session = _complete_session(validated)
        data = {
            "schema_version": VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION,
            "policy_id": VALIDATION_COMMAND_RUNNER_POLICY_ID,
            "state": ValidationCommandRunnerState.COMPLETED,
            "session": completed_session,
            "completed_command_count": len(completed_session.completed_command_ids),
            "passed_validation_ids": completed_session.passed_validation_ids,
            "manual_validation_ids_pending": completed_session.manual_validation_ids_pending,
            "validation_command_runner_requirement_satisfied": True,
            "result_envelopes_ready": False,
            "diff_artifact_review_ready": False,
            "human_git_handoff_ready": False,
            "provider_dispatch_count": 0,
            "model_inference_count": 0,
        }
        return ValidationCommandRunnerResult(
            **data,
            result_SHA256=_runner_result_digest_from_record(data),
        )
    except ValidationCommandRunnerError:
        raise
    except Exception as exc:
        raise ValidationCommandRunnerStateError(
            "complete validation runner failed"
        ) from exc


def validate_validation_command_runner_session(
    session: ValidationCommandRunnerSession,
) -> None:
    try:
        ValidationCommandRunnerSession.model_validate(session)
    except Exception as exc:
        raise ValidationCommandRunnerIntegrityError("runner session invalid") from exc


def validate_validation_command_runner_result(
    result: ValidationCommandRunnerResult,
) -> None:
    try:
        ValidationCommandRunnerResult.model_validate(result)
    except Exception as exc:
        raise ValidationCommandRunnerIntegrityError("runner result invalid") from exc


class _LaunchResult:
    def __init__(
        self,
        *,
        exit_code: int | None,
        stdout_raw: bytes,
        stderr_raw: bytes,
        stdout_raw_byte_count: int | None = None,
        stderr_raw_byte_count: int | None = None,
        stdout_raw_SHA256: str | None = None,
        stderr_raw_SHA256: str | None = None,
        process_started: bool,
        terminate_requested: bool,
        kill_requested: bool,
        timed_out: bool,
        output_limit_exceeded: bool,
        launch_failed: bool,
    ) -> None:
        self.exit_code = exit_code
        self.stdout_raw = stdout_raw
        self.stderr_raw = stderr_raw
        self.stdout_raw_byte_count = (
            len(stdout_raw) if stdout_raw_byte_count is None else stdout_raw_byte_count
        )
        self.stderr_raw_byte_count = (
            len(stderr_raw) if stderr_raw_byte_count is None else stderr_raw_byte_count
        )
        self.stdout_raw_SHA256 = (
            _sha256_bytes(stdout_raw)
            if stdout_raw_SHA256 is None
            else stdout_raw_SHA256
        )
        self.stderr_raw_SHA256 = (
            _sha256_bytes(stderr_raw)
            if stderr_raw_SHA256 is None
            else stderr_raw_SHA256
        )
        self.process_started = process_started
        self.terminate_requested = terminate_requested
        self.kill_requested = kill_requested
        self.timed_out = timed_out
        self.output_limit_exceeded = output_limit_exceeded
        self.launch_failed = launch_failed


class _StreamCapture:
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.raw = bytearray()
        self.raw_byte_count = 0
        self.raw_SHA256 = hashlib.sha256()
        self.exceeded = False


def _launch_and_capture(
    specification: ValidationCommandSpecification,
    environment: dict[str, str],
) -> _LaunchResult:
    try:
        process = subprocess.Popen(
            tuple(specification.effective_argv),
            shell=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
            bufsize=0,
            cwd=specification.working_directory,
            env=environment,
            close_fds=True,
        )
    except Exception:
        return _LaunchResult(
            exit_code=None,
            stdout_raw=b"",
            stderr_raw=b"",
            process_started=False,
            terminate_requested=False,
            kill_requested=False,
            timed_out=False,
            output_limit_exceeded=False,
            launch_failed=True,
        )
    stdout_capture = _StreamCapture(specification.max_stdout_bytes)
    stderr_capture = _StreamCapture(specification.max_stderr_bytes)
    overflow = threading.Event()
    stdout_thread = threading.Thread(
        target=_read_stream,
        args=(process.stdout, stdout_capture, overflow),
    )
    stderr_thread = threading.Thread(
        target=_read_stream,
        args=(process.stderr, stderr_capture, overflow),
    )
    stdout_thread.start()
    stderr_thread.start()
    timed_out = False
    terminate_requested = False
    kill_requested = False
    deadline = time.monotonic() + specification.timeout_seconds
    while process.poll() is None:
        if overflow.is_set():
            terminate_requested = True
            _terminate_process(process)
            break
        if time.monotonic() >= deadline:
            timed_out = True
            terminate_requested = True
            _terminate_process(process)
            break
        time.sleep(0.01)
    if terminate_requested and process.poll() is None:
        grace_deadline = time.monotonic() + TERMINATION_GRACE_SECONDS
        while process.poll() is None and time.monotonic() < grace_deadline:
            time.sleep(0.01)
        if process.poll() is None:
            kill_requested = True
            process.kill()
    exit_code = process.wait()
    stdout_thread.join()
    stderr_thread.join()
    return _LaunchResult(
        exit_code=exit_code,
        stdout_raw=bytes(stdout_capture.raw),
        stderr_raw=bytes(stderr_capture.raw),
        stdout_raw_byte_count=stdout_capture.raw_byte_count,
        stderr_raw_byte_count=stderr_capture.raw_byte_count,
        stdout_raw_SHA256=stdout_capture.raw_SHA256.hexdigest(),
        stderr_raw_SHA256=stderr_capture.raw_SHA256.hexdigest(),
        process_started=True,
        terminate_requested=terminate_requested,
        kill_requested=kill_requested,
        timed_out=timed_out,
        output_limit_exceeded=stdout_capture.exceeded or stderr_capture.exceeded,
        launch_failed=False,
    )


def _read_stream(
    stream: object, capture: _StreamCapture, overflow: threading.Event
) -> None:
    if stream is None:
        return
    while True:
        chunk = stream.read(OUTPUT_CHUNK_BYTES)  # type: ignore[attr-defined]
        if not chunk:
            return
        capture.raw_byte_count += len(chunk)
        capture.raw_SHA256.update(chunk)
        remaining = capture.limit - len(capture.raw)
        if remaining > 0:
            capture.raw.extend(chunk[:remaining])
        if len(chunk) > remaining:
            capture.exceeded = True
            overflow.set()


def _terminate_process(process: subprocess.Popen[bytes]) -> None:
    try:
        process.terminate()
    except Exception as exc:
        raise ValidationCommandExecutionError("process termination failed") from exc


def _disposition_for_launch(
    specification: ValidationCommandSpecification,
    launch: _LaunchResult,
) -> tuple[ValidationCommandDisposition, ValidationCommandFailureReason]:
    if launch.launch_failed:
        return (
            ValidationCommandDisposition.FAILED,
            ValidationCommandFailureReason.LAUNCH_ERROR,
        )
    if launch.timed_out:
        return (
            ValidationCommandDisposition.TIMED_OUT,
            ValidationCommandFailureReason.TIMEOUT,
        )
    if launch.output_limit_exceeded:
        return (
            ValidationCommandDisposition.OUTPUT_LIMIT_EXCEEDED,
            ValidationCommandFailureReason.OUTPUT_LIMIT,
        )
    if launch.exit_code in specification.expected_exit_codes:
        return (
            ValidationCommandDisposition.PASSED,
            ValidationCommandFailureReason.NONE,
        )
    return (
        ValidationCommandDisposition.FAILED,
        ValidationCommandFailureReason.NONZERO_EXIT,
    )


def _build_command_specifications(
    *,
    compilation_result: WorkPacketCompilationResult,
    allocation_result: WorkspaceAllocationResult,
    runtime_binding: ValidationCommandRuntimeBinding,
    authorization_requests: tuple[ValidationCommandAuthorizationRequest, ...],
) -> tuple[ValidationCommandSpecification, ...]:
    command_steps = tuple(
        step
        for step in compilation_result.work_packet.validation_steps
        if step.kind is WorkPacketValidationKind.COMMAND
    )
    if not command_steps:
        raise ValidationCommandRunnerAuthorizationError("no command validation steps")
    requests_by_id: dict[str, ValidationCommandAuthorizationRequest] = {}
    for item in authorization_requests:
        if item.validation_id in requests_by_id:
            raise ValidationCommandRunnerAuthorizationError(
                "duplicate authorization request"
            )
        requests_by_id[item.validation_id] = item
    command_ids = {step.validation_id for step in command_steps}
    manual_ids = {
        step.validation_id
        for step in compilation_result.work_packet.validation_steps
        if step.kind is WorkPacketValidationKind.MANUAL
    }
    if set(requests_by_id) != command_ids:
        raise ValidationCommandRunnerAuthorizationError(
            "command authorization coverage mismatch"
        )
    if set(requests_by_id) & manual_ids:
        raise ValidationCommandRunnerAuthorizationError(
            "manual validation cannot be authorized"
        )
    specifications: list[ValidationCommandSpecification] = []
    for index, step in enumerate(command_steps, start=1):
        if step.command is None:
            raise ValidationCommandPolicyError(
                "command validation step command is missing"
            )
        request = requests_by_id[step.validation_id]
        module, effective_argv = _parse_command(
            source_command=step.command,
            runtime_binding=runtime_binding,
        )
        data = {
            "schema_version": VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION,
            "command_id": _command_id(index),
            "validation_id": step.validation_id,
            "module": module,
            "source_command": step.command,
            "source_command_SHA256": _sha256_text(step.command),
            "effective_argv": effective_argv,
            "working_directory": allocation_result.allocation.resolved_workspace_root,
            "timeout_seconds": request.timeout_seconds,
            "expected_exit_codes": request.expected_exit_codes,
            "max_stdout_bytes": MAX_STDOUT_BYTES,
            "max_stderr_bytes": MAX_STDERR_BYTES,
        }
        specifications.append(
            ValidationCommandSpecification(
                **data,
                specification_SHA256=_specification_digest_from_record(data),
            )
        )
    return tuple(specifications)


def _parse_command(
    *,
    source_command: str,
    runtime_binding: ValidationCommandRuntimeBinding,
) -> tuple[ValidationCommandModule, tuple[str, ...]]:
    _validate_source_command_text(source_command)
    try:
        tokens = tuple(shlex.split(source_command, posix=True))
    except ValueError as exc:
        raise ValidationCommandPolicyError("source command quoting is invalid") from exc
    if not tokens:
        raise ValidationCommandPolicyError("source command must not be empty")
    if len(tokens) > MAX_ARGV_TOKENS:
        raise ValidationCommandPolicyError("source command has too many tokens")
    for token in tokens:
        _validate_source_token(token)
    executable = tokens[0]
    allowed_executables = {
        "python",
        "python3",
        "py",
        Path(runtime_binding.resolved_python_executable).name,
    }
    if executable not in allowed_executables:
        raise ValidationCommandPolicyError("source executable is not allowed")
    if len(tokens) < 3 or tokens[1] != "-m":
        raise ValidationCommandPolicyError("source command must use python -m")
    module = tokens[2]
    args = tokens[3:]
    if module == "pytest":
        return ValidationCommandModule.PYTEST, _normalize_pytest(runtime_binding, args)
    if module == "unittest":
        return ValidationCommandModule.UNITTEST, _normalize_unittest(
            runtime_binding, args
        )
    if module == "ruff":
        return _normalize_ruff(runtime_binding, args)
    raise ValidationCommandPolicyError("unsupported validation command module")


def _validate_source_command_text(source_command: str) -> None:
    if not source_command:
        raise ValidationCommandPolicyError("source command must not be empty")
    if len(source_command) > MAX_SOURCE_COMMAND_CHARACTERS:
        raise ValidationCommandPolicyError("source command exceeds length bound")
    if "\x00" in source_command or "\n" in source_command or "\r" in source_command:
        raise ValidationCommandPolicyError("source command contains control separator")
    for marker in _FORBIDDEN_SHELL_MARKERS:
        if marker in source_command:
            raise ValidationCommandPolicyError("source command contains shell marker")
    for token in _FORBIDDEN_SHELL_TOKENS:
        if token in source_command:
            raise ValidationCommandPolicyError("source command contains shell token")
    if "\\" in source_command:
        raise ValidationCommandPolicyError("source command must use forward slashes")
    for marker in _SECRET_COMMAND_MARKERS:
        if marker.casefold() in source_command.casefold():
            raise ValidationCommandPolicyError(
                "source command contains secret-shaped text"
            )


def _validate_source_token(token: str) -> None:
    _validate_argv_token(token)
    if token in _FORBIDDEN_SHELL_TOKENS or any(
        marker in token for marker in _FORBIDDEN_SHELL_MARKERS
    ):
        raise ValidationCommandPolicyError("source token contains shell syntax")
    if token.startswith("@"):
        raise ValidationCommandPolicyError("response files are not allowed")
    if _ENV_ASSIGNMENT_PATTERN.match(token):
        raise ValidationCommandPolicyError("environment assignments are not allowed")
    if token == "-" or token == "-c":
        raise ValidationCommandPolicyError("script execution is not allowed")
    if _is_absolute_or_traversal_path(token):
        raise ValidationCommandPolicyError("unsafe path token")


def _validate_argv_token(token: str) -> None:
    if not token:
        raise ValueError("argv token must not be empty")
    if len(token) > 512:
        raise ValueError("argv token exceeds maximum length")
    if "\x00" in token or _CONTROL_CHARACTER_PATTERN.search(token):
        raise ValueError("argv token contains control character")
    if "\\" in token:
        raise ValueError("argv token must use forward slashes")


def _normalize_pytest(
    runtime_binding: ValidationCommandRuntimeBinding,
    args: tuple[str, ...],
) -> tuple[str, ...]:
    normalized = [runtime_binding.resolved_python_executable, "-m", "pytest"]
    saw_cache_disable = False
    index = 0
    while index < len(args):
        token = args[index]
        if token == "-p":
            if index + 1 >= len(args) or args[index + 1] != "no:cacheprovider":
                raise ValidationCommandPolicyError(
                    "pytest plugin requests are not allowed"
                )
            normalized.extend((token, args[index + 1]))
            saw_cache_disable = True
            index += 2
            continue
        if token.startswith("-p"):
            raise ValidationCommandPolicyError("pytest plugin requests are not allowed")
        if token in {"--trace", "--pdb"} or token.startswith((
            "--pdbcls",
            "--pastebin",
        )):
            raise ValidationCommandPolicyError(
                "interactive pytest options are not allowed"
            )
        normalized.append(token)
        index += 1
    if not saw_cache_disable:
        normalized.extend(("-p", "no:cacheprovider"))
    return tuple(normalized)


def _normalize_unittest(
    runtime_binding: ValidationCommandRuntimeBinding,
    args: tuple[str, ...],
) -> tuple[str, ...]:
    for token in args:
        if _is_absolute_or_traversal_path(token):
            raise ValidationCommandPolicyError("unsafe unittest path")
    return (runtime_binding.resolved_python_executable, "-m", "unittest", *args)


def _normalize_ruff(
    runtime_binding: ValidationCommandRuntimeBinding,
    args: tuple[str, ...],
) -> tuple[ValidationCommandModule, tuple[str, ...]]:
    if not args:
        raise ValidationCommandPolicyError("ruff subcommand is required")
    subcommand = args[0]
    rest = args[1:]
    if subcommand == "check":
        for token in rest:
            if token in {"--fix", "--fix-only", "--unsafe-fixes"}:
                raise ValidationCommandPolicyError("ruff write options are not allowed")
        effective = [runtime_binding.resolved_python_executable, "-m", "ruff", "check"]
        effective.extend(rest)
        if "--no-cache" not in rest:
            effective.append("--no-cache")
        return ValidationCommandModule.RUFF_CHECK, tuple(effective)
    if subcommand == "format":
        if "--check" not in rest:
            raise ValidationCommandPolicyError("ruff format requires --check")
        return (
            ValidationCommandModule.RUFF_FORMAT_CHECK,
            (runtime_binding.resolved_python_executable, "-m", "ruff", "format", *rest),
        )
    raise ValidationCommandPolicyError("unsupported ruff command")


def _is_absolute_or_traversal_path(token: str) -> bool:
    if token.startswith("/") or _DRIVE_PATH_PATTERN.match(token):
        return True
    return any(component in {"..", "."} for component in token.split("/"))


def _minimal_environment() -> dict[str, str]:
    data: dict[str, str] = {}
    for key, value in _FIXED_ENVIRONMENT:
        data[key] = value
    for key in _INHERITED_ENVIRONMENT_ALLOWLIST:
        if key in os.environ:
            data[key] = os.environ[key]
    return {key: data[key] for key in sorted(data)}


def _reinspect_workspace(
    allocation: WorkspaceAllocation,
) -> WorkspaceInspectionEvidence:
    evidence = inspect_human_provisioned_workspace(
        workspace_root=allocation.workspace_root,
        repository_identity=allocation.repository_identity,
        require_clean_worktree=False,
        require_linked_worktree=True,
    )
    _validate_workspace_identity(evidence=evidence, allocation=allocation)
    return evidence


def _validate_workspace_identity(
    *, evidence: WorkspaceInspectionEvidence, allocation: WorkspaceAllocation
) -> None:
    if evidence.workspace_root != allocation.workspace_root:
        raise ValidationCommandRunnerIntegrityError("workspace root mismatch")
    if evidence.resolved_workspace_root != allocation.resolved_workspace_root:
        raise ValidationCommandRunnerIntegrityError("resolved workspace root mismatch")
    if evidence.git_top_level != allocation.resolved_workspace_root:
        raise ValidationCommandRunnerIntegrityError("workspace top level mismatch")
    if evidence.source_commit != allocation.repository_identity.source_commit:
        raise ValidationCommandRunnerIntegrityError("workspace HEAD mismatch")
    if evidence.workspace_branch != allocation.repository_identity.workspace_branch:
        raise ValidationCommandRunnerIntegrityError("workspace branch mismatch")
    if not evidence.inside_work_tree or not evidence.linked_worktree:
        raise ValidationCommandRunnerIntegrityError("workspace must remain linked")


def _validate_prerequisites(
    *,
    compilation_result: WorkPacketCompilationResult,
    allocation_result: WorkspaceAllocationResult,
    profile_result: ToolPermissionProfileResult,
    single_agent_execution_result: SingleAgentExecutionResult,
    runtime_binding: ValidationCommandRuntimeBinding,
) -> None:
    try:
        validate_work_packet(compilation_result.work_packet)
        validate_workspace_allocation(allocation_result.allocation)
        validate_tool_permission_profile(profile_result.profile)
        validate_single_agent_execution_result(single_agent_execution_result)
        ValidationCommandRuntimeBinding.model_validate(runtime_binding)
    except Exception as exc:
        raise ValidationCommandRunnerIntegrityError(
            "prerequisite validation failed"
        ) from exc
    if (
        ToolPermissionOperation.VALIDATION_COMMAND
        not in profile_result.profile.denied_operations
    ):
        raise ValidationCommandRunnerAuthorizationError(
            "validation command must remain denied by P17.2"
        )
    if single_agent_execution_result.state is not SingleAgentExecutionState.COMPLETED:
        raise ValidationCommandRunnerInputError(
            "single-agent execution must be completed"
        )
    if (
        single_agent_execution_result.single_agent_execution_requirement_satisfied
        is not True
    ):
        raise ValidationCommandRunnerInputError(
            "single-agent execution requirement unsatisfied"
        )
    if single_agent_execution_result.validation_command_runner_ready is not False:
        raise ValidationCommandRunnerInputError(
            "validation runner must not be ready before P17.4"
        )
    if single_agent_execution_result.provider_dispatch_count != 0:
        raise ValidationCommandRunnerAuthorizationError(
            "provider dispatch count must be zero"
        )
    if single_agent_execution_result.model_inference_count != 0:
        raise ValidationCommandRunnerAuthorizationError(
            "model inference count must be zero"
        )
    allocation = allocation_result.allocation
    if runtime_binding.working_directory != allocation.resolved_workspace_root:
        raise ValidationCommandRunnerInputError(
            "runtime binding working directory mismatch"
        )


def _validate_request_bindings(
    request: ValidationCommandRunnerRequest,
    *,
    error_type: type[Exception],
) -> None:
    work_packet = request.compilation_result.work_packet
    allocation = request.allocation_result.allocation
    profile = request.profile_result.profile
    result = request.single_agent_execution_result
    authorization = request.runner_authorization
    if allocation.work_packet_id != work_packet.work_packet_id:
        raise error_type("allocation WorkPacket mismatch")
    if allocation.work_packet_SHA256 != work_packet.work_packet_SHA256:
        raise error_type("allocation WorkPacket digest mismatch")
    if profile.work_packet_id != work_packet.work_packet_id:
        raise error_type("profile WorkPacket mismatch")
    if profile.allocation_id != allocation.allocation_id:
        raise error_type("profile allocation mismatch")
    if result.session.work_packet_id != work_packet.work_packet_id:
        raise error_type("single-agent WorkPacket mismatch")
    if result.session.allocation_id != allocation.allocation_id:
        raise error_type("single-agent allocation mismatch")
    if result.session.profile_id != profile.profile_id:
        raise error_type("single-agent profile mismatch")
    if authorization.work_packet_id != work_packet.work_packet_id:
        raise error_type("authorization WorkPacket mismatch")
    if authorization.work_packet_SHA256 != work_packet.work_packet_SHA256:
        raise error_type("authorization WorkPacket digest mismatch")
    if authorization.allocation_id != allocation.allocation_id:
        raise error_type("authorization allocation mismatch")
    if authorization.allocation_SHA256 != allocation.allocation_SHA256:
        raise error_type("authorization allocation digest mismatch")
    if authorization.profile_id != profile.profile_id:
        raise error_type("authorization profile mismatch")
    if authorization.profile_SHA256 != profile.profile_SHA256:
        raise error_type("authorization profile digest mismatch")
    if authorization.single_agent_result_SHA256 != result.result_SHA256:
        raise error_type("authorization single-agent result mismatch")
    if authorization.runtime_binding_SHA256 != request.runtime_binding.binding_SHA256:
        raise error_type("authorization runtime binding mismatch")
    expected = _build_command_specifications(
        compilation_result=request.compilation_result,
        allocation_result=request.allocation_result,
        runtime_binding=request.runtime_binding,
        authorization_requests=tuple(
            ValidationCommandAuthorizationRequest(
                validation_id=spec.validation_id,
                timeout_seconds=spec.timeout_seconds,
                expected_exit_codes=spec.expected_exit_codes,
            )
            for spec in authorization.command_specifications
        ),
    )
    if expected != authorization.command_specifications:
        raise error_type("authorization command specification mismatch")


def _validate_session_request_binding(
    *,
    session: ValidationCommandRunnerSession,
    request: ValidationCommandRunnerRequest,
    error_type: type[Exception],
) -> None:
    authorization = request.runner_authorization
    if session.work_packet_id != authorization.work_packet_id:
        raise error_type("session WorkPacket mismatch")
    if session.work_packet_SHA256 != authorization.work_packet_SHA256:
        raise error_type("session WorkPacket digest mismatch")
    if session.allocation_id != authorization.allocation_id:
        raise error_type("session allocation mismatch")
    if session.allocation_SHA256 != authorization.allocation_SHA256:
        raise error_type("session allocation digest mismatch")
    if session.profile_id != authorization.profile_id:
        raise error_type("session profile mismatch")
    if session.profile_SHA256 != authorization.profile_SHA256:
        raise error_type("session profile digest mismatch")
    if session.single_agent_result_SHA256 != authorization.single_agent_result_SHA256:
        raise error_type("session single-agent result mismatch")
    if session.runtime_binding_SHA256 != authorization.runtime_binding_SHA256:
        raise error_type("session runtime binding mismatch")
    if session.authorization_SHA256 != authorization.authorization_SHA256:
        raise error_type("session authorization mismatch")


def _validate_runtime_binding_current(binding: ValidationCommandRuntimeBinding) -> None:
    resolved = Path(binding.resolved_python_executable).resolve(strict=True)
    current = Path(sys.executable).resolve(strict=True)
    if resolved != current:
        raise ValidationCommandRunnerInputError("runtime binding interpreter drift")


def _append_evidence(
    *,
    request: ValidationCommandRunnerRequest,
    session: ValidationCommandRunnerSession,
    evidence: ValidationCommandExecutionEvidence,
    state: ValidationCommandRunnerState,
    advance: bool,
) -> ValidationCommandRunnerSession:
    existing_evidence = (*session.command_evidence, evidence)
    completed = session.completed_command_ids
    passed = session.passed_validation_ids
    next_index = session.next_command_index
    if advance:
        completed = (*completed, evidence.command_id)
        passed = (*passed, evidence.validation_id)
        next_index += 1
    data = {
        "schema_version": VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION,
        "session_id": session.session_id,
        "policy_id": VALIDATION_COMMAND_RUNNER_POLICY_ID,
        "state": state,
        "work_packet_id": session.work_packet_id,
        "work_packet_SHA256": session.work_packet_SHA256,
        "allocation_id": session.allocation_id,
        "allocation_SHA256": session.allocation_SHA256,
        "profile_id": session.profile_id,
        "profile_SHA256": session.profile_SHA256,
        "single_agent_result_SHA256": session.single_agent_result_SHA256,
        "runtime_binding_SHA256": session.runtime_binding_SHA256,
        "authorization_SHA256": session.authorization_SHA256,
        "next_command_index": next_index,
        "completed_command_ids": completed,
        "passed_validation_ids": passed,
        "manual_validation_ids_pending": session.manual_validation_ids_pending,
        "command_evidence": existing_evidence,
        "execution_active": state
        in {ValidationCommandRunnerState.PREPARED, ValidationCommandRunnerState.ACTIVE},
        "validation_command_runner_requirement_satisfied": False,
        "result_envelopes_ready": False,
        "diff_artifact_review_ready": False,
        "human_git_handoff_ready": False,
    }
    if (
        next_index == len(request.runner_authorization.command_specifications)
        and advance
    ):
        data["state"] = ValidationCommandRunnerState.ACTIVE
    return ValidationCommandRunnerSession(
        **data,
        session_SHA256=_session_digest_from_record(data),
    )


def _complete_session(
    session: ValidationCommandRunnerSession,
) -> ValidationCommandRunnerSession:
    data = session.model_dump(mode="python", exclude={"session_SHA256"})
    data.update({
        "state": ValidationCommandRunnerState.COMPLETED,
        "execution_active": False,
        "validation_command_runner_requirement_satisfied": True,
    })
    return ValidationCommandRunnerSession(
        **data,
        session_SHA256=_session_digest_from_record(data),
    )


def _execution_result(
    *,
    disposition: ValidationCommandDisposition,
    specification: ValidationCommandSpecification,
    updated_session: ValidationCommandRunnerSession,
    stdout: ValidationCommandCapturedStream,
    stderr: ValidationCommandCapturedStream,
) -> ValidationCommandExecutionResult:
    data = {
        "schema_version": VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION,
        "disposition": disposition,
        "specification": specification,
        "updated_session": updated_session,
        "stdout": stdout,
        "stderr": stderr,
    }
    return ValidationCommandExecutionResult(
        **data,
        result_SHA256=_execution_result_digest_from_record(data),
    )


def _build_evidence(
    *,
    specification: ValidationCommandSpecification,
    disposition: ValidationCommandDisposition,
    failure_reason: ValidationCommandFailureReason,
    exit_code: int | None,
    process_started: bool,
    terminate_requested: bool,
    kill_requested: bool,
    stdout: ValidationCommandCapturedStream,
    stderr: ValidationCommandCapturedStream,
    before: WorkspaceInspectionEvidence | None,
    after: WorkspaceInspectionEvidence | None,
) -> ValidationCommandExecutionEvidence:
    data = {
        "schema_version": VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION,
        "command_id": specification.command_id,
        "validation_id": specification.validation_id,
        "module": specification.module,
        "disposition": disposition,
        "failure_reason": failure_reason,
        "exit_code": exit_code,
        "timeout_seconds": specification.timeout_seconds,
        "process_started": process_started,
        "terminate_requested": terminate_requested,
        "kill_requested": kill_requested,
        "stdout_raw_byte_count": stdout.raw_byte_count,
        "stderr_raw_byte_count": stderr.raw_byte_count,
        "stdout_SHA256": stdout.raw_SHA256,
        "stderr_SHA256": stderr.raw_SHA256,
        "stdout_truncated": stdout.truncated,
        "stderr_truncated": stderr.truncated,
        "redaction_count": stdout.redaction_count + stderr.redaction_count,
        "workspace_status_entry_count_before": before.status_entry_count
        if before is not None
        else None,
        "workspace_status_entry_count_after": after.status_entry_count
        if after is not None
        else None,
        "workspace_inspection_before_SHA256": before.inspection_SHA256
        if before is not None
        else None,
        "workspace_inspection_after_SHA256": after.inspection_SHA256
        if after is not None
        else None,
    }
    return ValidationCommandExecutionEvidence(
        **data,
        evidence_SHA256=_execution_evidence_digest_from_record(data),
    )


def _empty_stream(kind: ValidationCommandStreamKind) -> ValidationCommandCapturedStream:
    return _captured_stream(kind, b"", RETAINED_STDOUT_BYTES)


def _captured_stream(
    kind: ValidationCommandStreamKind,
    raw: bytes,
    retained_limit: int,
    *,
    raw_byte_count: int | None = None,
    raw_SHA256: str | None = None,
) -> ValidationCommandCapturedStream:
    count = len(raw) if raw_byte_count is None else raw_byte_count
    raw_sha = _sha256_bytes(raw) if raw_SHA256 is None else raw_SHA256
    if count == 0:
        data = {
            "stream": kind,
            "retained_text": None,
            "raw_byte_count": 0,
            "retained_byte_count": 0,
            "raw_SHA256": raw_sha,
            "truncated": False,
            "redaction_count": 0,
            "decode_replacement_count": 0,
        }
        return ValidationCommandCapturedStream(
            **data,
            stream_SHA256=_captured_stream_digest_from_record(data),
        )
    text, replacement_count = _decode_utf8(raw)
    sanitized, redactions = _sanitize_output(text)
    encoded = sanitized.encode("utf-8")
    truncated = len(encoded) > retained_limit
    retained = encoded[:retained_limit].decode("utf-8", errors="ignore").strip()
    data = {
        "stream": kind,
        "retained_text": retained,
        "raw_byte_count": count,
        "retained_byte_count": len(retained.encode("utf-8")),
        "raw_SHA256": raw_sha,
        "truncated": truncated,
        "redaction_count": redactions,
        "decode_replacement_count": replacement_count,
    }
    return ValidationCommandCapturedStream(
        **data,
        stream_SHA256=_captured_stream_digest_from_record(data),
    )


def _decode_utf8(raw: bytes) -> tuple[str, int]:
    text = raw.decode("utf-8", errors="replace")
    return text, text.count("\ufffd")


def _sanitize_output(text: str) -> tuple[str, int]:
    text = _ANSI_ESCAPE_PATTERN.sub("", text)
    text = "".join(
        character for character in text if character in "\n\r\t" or ord(character) >= 32
    )
    redactions = 0
    for pattern in _SECRET_PATTERNS:
        text, count = pattern.subn("<REDACTED>", text)
        redactions += count
    return text, redactions


def _validate_specification_sequence(
    specifications: tuple[ValidationCommandSpecification, ...],
) -> None:
    for index, specification in enumerate(specifications, start=1):
        if specification.command_id != _command_id(index):
            raise ValueError("command IDs must be contiguous")
    validation_ids = tuple(spec.validation_id for spec in specifications)
    if len(validation_ids) != len(frozenset(validation_ids)):
        raise ValueError("validation IDs must be unique")


def _command_id(index: int) -> str:
    return f"VCMD-{index:03d}"


def _command_index(command_id: str) -> int:
    return int(command_id.rsplit("-", 1)[1])


def _publication_revision_from_work_packet_id(work_packet_id: str) -> int:
    match = re.search(r"-R([0-9]{4})-", work_packet_id)
    if match is None:
        return 1
    return int(match.group(1))


def _binding_id(*, ticket_id: str, publication_revision: int, digest_text: str) -> str:
    return f"VCB-{ticket_id.replace('.', '-')}-R{publication_revision:04d}-{digest_text[:12]}"


def _session_id(*, ticket_id: str, publication_revision: int, digest_text: str) -> str:
    return f"VCR-{ticket_id.replace('.', '-')}-R{publication_revision:04d}-{digest_text[:12]}"


def _runtime_binding_id_from_binding(binding: ValidationCommandRuntimeBinding) -> str:
    prefix = binding.binding_id.rsplit("-", 1)[0]
    input_record = binding.model_dump(
        mode="json", exclude={"binding_id", "binding_SHA256"}
    )
    return f"{prefix}-{_digest(BINDING_DIGEST_ALGORITHM, input_record)[:12]}"


def _is_shadow_identifier(value: str) -> bool:
    return value.upper().startswith("SHADOW-") or value.casefold().startswith("shadow-")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _deterministic_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _dump_value(value: object) -> object:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple | list):
        return [_dump_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _dump_value(item) for key, item in value.items()}
    return value


def _normalized_record(record: dict[str, object]) -> dict[str, object]:
    return {key: _dump_value(value) for key, value in record.items()}


def _digest(algorithm: str, record: dict[str, object]) -> str:
    return _sha256_text(
        _deterministic_json({"algorithm": algorithm, **_normalized_record(record)})
    )


def _runtime_binding_digest(binding: ValidationCommandRuntimeBinding) -> str:
    return _runtime_binding_digest_from_record(
        binding.model_dump(mode="json", exclude={"binding_SHA256"})
    )


def _runtime_binding_digest_from_record(record: dict[str, object]) -> str:
    return _digest(BINDING_DIGEST_ALGORITHM, record)


def _specification_digest(specification: ValidationCommandSpecification) -> str:
    return _specification_digest_from_record(
        specification.model_dump(mode="json", exclude={"specification_SHA256"})
    )


def _specification_digest_from_record(record: dict[str, object]) -> str:
    return _digest(SPECIFICATION_DIGEST_ALGORITHM, record)


def _authorization_digest(authorization: ValidationCommandRunnerAuthorization) -> str:
    return _authorization_digest_from_record(
        authorization.model_dump(mode="json", exclude={"authorization_SHA256"})
    )


def _authorization_digest_from_record(record: dict[str, object]) -> str:
    return _digest(AUTHORIZATION_DIGEST_ALGORITHM, record)


def _captured_stream_digest(stream: ValidationCommandCapturedStream) -> str:
    return _captured_stream_digest_from_record(
        stream.model_dump(mode="json", exclude={"stream_SHA256"})
    )


def _captured_stream_digest_from_record(record: dict[str, object]) -> str:
    return _digest(STREAM_DIGEST_ALGORITHM, record)


def _execution_evidence_digest(evidence: ValidationCommandExecutionEvidence) -> str:
    return _execution_evidence_digest_from_record(
        evidence.model_dump(mode="json", exclude={"evidence_SHA256"})
    )


def _execution_evidence_digest_from_record(record: dict[str, object]) -> str:
    return _digest(EVIDENCE_DIGEST_ALGORITHM, record)


def _session_digest(session: ValidationCommandRunnerSession) -> str:
    return _session_digest_from_record(
        session.model_dump(mode="json", exclude={"session_SHA256"})
    )


def _session_digest_from_record(record: dict[str, object]) -> str:
    return _digest(SESSION_DIGEST_ALGORITHM, record)


def _execution_result_digest(result: ValidationCommandExecutionResult) -> str:
    return _execution_result_digest_from_record(
        result.model_dump(mode="json", exclude={"result_SHA256"})
    )


def _execution_result_digest_from_record(record: dict[str, object]) -> str:
    return _digest(EXECUTION_RESULT_DIGEST_ALGORITHM, record)


def _runner_result_digest(result: ValidationCommandRunnerResult) -> str:
    return _runner_result_digest_from_record(
        result.model_dump(mode="json", exclude={"result_SHA256"})
    )


def _runner_result_digest_from_record(record: dict[str, object]) -> str:
    return _digest(RUNNER_RESULT_DIGEST_ALGORITHM, record)
