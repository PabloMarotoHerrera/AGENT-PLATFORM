"""Pure local Integrator / CommitCandidate rendering for MVP-0.

This module converts caller-supplied review and integration metadata into
structured advisory objects. It does not inspect files, modify files, activate
runtime behavior, call networks, call providers, call harnesses, use Git
libraries, or mutate Git.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence


DEFAULT_REMOTE = "origin"
DEFAULT_BRANCH = "main"
WILDCARD_CHARS = frozenset("*?[]{}")
SHELL_META_CHARS = frozenset(";&|<>`$\"'")
GIT_COMMAND = "git"
GIT_ADD_PREFIX = GIT_COMMAND + " add "
BAD_GIT_ADD_DOT = GIT_ADD_PREFIX + "."
NEVER_GIT_ADD_DOT_POLICY = "Never recommend git add ."


@dataclass(frozen=True)
class DriftItem:
    drift_item_id: str
    description: str
    status: str = "unresolved"
    severity: str = "informational"
    source_ref: str = "manual_review_or_integration_record"
    accepted_limitation: str = ""
    rationale: str = ""
    limitations: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class DriftRegister:
    drift_register_id: str
    ticket_id: str
    drift_items: Sequence[DriftItem] = field(default_factory=tuple)
    unresolved_count: int = 0
    accepted_with_limitations_count: int = 0
    blocked_count: int = 0
    status: str = "clear"
    limitations: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class AcceptedOutputItem:
    item_id: str
    path_ref: str
    review_ref: str = "manual_review_required"
    integration_ref: str = "manual_integration_required"
    rationale: str = "accepted by supplied review metadata"
    retention_posture: str = "manual_retention_review_required"
    rollback_posture: str = "manual_rollback_review_required"
    incident_posture: str = "no_incident_claimed"
    limitations: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class AcceptedOutputRegister:
    accepted_register_id: str
    ticket_id: str
    accepted_items: Sequence[AcceptedOutputItem] = field(default_factory=tuple)
    path_refs: Sequence[str] = field(default_factory=tuple)
    review_refs: Sequence[str] = field(default_factory=tuple)
    integration_refs: Sequence[str] = field(default_factory=tuple)
    retention_posture: str = "manual_retention_review_required"
    rollback_posture: str = "manual_rollback_review_required"
    incident_posture: str = "no_incident_claimed"
    limitations: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class RejectedOutputItem:
    item_id: str
    path_ref: str = ""
    output_id: str = ""
    rejection_reason: str = "rejected by supplied review metadata"
    review_ref: str = "manual_review_required"
    integration_ref: str = "manual_integration_required"
    reviewer_rationale: str = ""
    integrator_rationale: str = ""
    retention_posture: str = "manual_retention_review_required"
    rollback_posture: str = "manual_rollback_review_required"
    incident_posture: str = "no_incident_claimed"
    limitations: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class RejectedOutputRegister:
    rejected_register_id: str
    ticket_id: str
    rejected_items: Sequence[RejectedOutputItem] = field(default_factory=tuple)
    path_refs: Sequence[str] = field(default_factory=tuple)
    rejection_reasons: Sequence[str] = field(default_factory=tuple)
    review_refs: Sequence[str] = field(default_factory=tuple)
    integration_refs: Sequence[str] = field(default_factory=tuple)
    retention_posture: str = "manual_retention_review_required"
    rollback_posture: str = "manual_rollback_review_required"
    incident_posture: str = "no_incident_claimed"
    limitations: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class RollbackNote:
    rollback_note_id: str
    ticket_id: str
    notes: Sequence[str] = field(default_factory=tuple)
    rendered_text: str = ""
    human_approval_required: bool = True
    limitations: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class PushInstruction:
    push_instruction_id: str
    commit_candidate_ref: str
    target_remote: str = DEFAULT_REMOTE
    target_branch: str = DEFAULT_BRANCH
    rendered_text: str = ""
    advisory_only: bool = True
    user_executes_manually: bool = True
    limitations: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class CommitCandidate:
    commit_candidate_id: str
    ticket_id: str
    ticket_title: str
    exact_add_paths: Sequence[str] = field(default_factory=tuple)
    excluded_paths: Sequence[str] = field(default_factory=tuple)
    generated_output_paths: Sequence[str] = field(default_factory=tuple)
    ignored_artifact_paths: Sequence[str] = field(default_factory=tuple)
    quarantined_paths: Sequence[str] = field(default_factory=tuple)
    commit_message: str = ""
    push_target: str = ""
    human_approval_required: bool = True
    git_mutation_forbidden_for_agent: bool = True
    never_git_add_dot: bool = True
    drift_status: str = "clear"
    retention_posture: str = "manual_retention_review_required"
    rollback_note: str = "manual rollback review required"
    incident_posture: str = "no_incident_claimed"
    limitations: Sequence[str] = field(default_factory=tuple)
    blocked: bool = False
    blockers: Sequence[str] = field(default_factory=tuple)
    exclusion_reasons: Mapping[str, Sequence[str]] = field(default_factory=dict)


@dataclass(frozen=True)
class CommitCommandBlock:
    command_block_id: str
    commit_candidate_ref: str
    commands: Sequence[str] = field(default_factory=tuple)
    rendered_text: str = ""
    contains_only_exact_paths: bool = False
    contains_git_add_dot: bool = False
    contains_wildcards: bool = False
    user_executes_manually: bool = True
    limitations: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class IntegrationSummary:
    integration_summary_id: str
    ticket_id: str
    ticket_title: str
    accepted_register_ref: str = ""
    accepted_items: Sequence[AcceptedOutputItem] = field(default_factory=tuple)
    rejected_register_ref: str = ""
    rejected_items: Sequence[RejectedOutputItem] = field(default_factory=tuple)
    drift_register_ref: str = ""
    drift_items: Sequence[DriftItem] = field(default_factory=tuple)
    commit_candidate_ref: str = ""
    review_summary: str = "manual review metadata supplied"
    integration_notes: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    retention_posture: str = "manual_retention_review_required"
    rollback_posture: str = "manual_rollback_review_required"
    incident_posture: str = "no_incident_claimed"
    human_approval_required: bool = True
    rendered_text: str = ""


@dataclass(frozen=True)
class IntegrationRenderRequest:
    ticket_id: str
    ticket_title: str
    created_paths: Sequence[str] = field(default_factory=tuple)
    modified_paths: Sequence[str] = field(default_factory=tuple)
    deleted_paths: Sequence[str] = field(default_factory=tuple)
    accepted_paths: Sequence[str] = field(default_factory=tuple)
    rejected_paths: Sequence[str] = field(default_factory=tuple)
    excluded_paths: Sequence[str] = field(default_factory=tuple)
    generated_output_paths: Sequence[str] = field(default_factory=tuple)
    ignored_artifact_paths: Sequence[str] = field(default_factory=tuple)
    quarantined_paths: Sequence[str] = field(default_factory=tuple)
    blocked_paths: Sequence[str] = field(default_factory=tuple)
    unknown_sensitivity_paths: Sequence[str] = field(default_factory=tuple)
    drift_items: Sequence[DriftItem] = field(default_factory=tuple)
    accepted_items: Sequence[AcceptedOutputItem] = field(default_factory=tuple)
    rejected_items: Sequence[RejectedOutputItem] = field(default_factory=tuple)
    review_verdicts: Sequence[str] = field(default_factory=tuple)
    integration_notes: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    rollback_notes: Sequence[str] = field(default_factory=tuple)
    human_approval_required: bool = True
    target_remote: str = DEFAULT_REMOTE
    target_branch: str = DEFAULT_BRANCH
    tracking_allowed_by_future_gate: bool = False
    product_source_gate_approved: bool = False
    retention_posture: str = "manual_retention_review_required"
    rollback_posture: str = "manual_rollback_review_required"
    incident_posture: str = "no_incident_claimed"


@dataclass(frozen=True)
class GitAdvisory:
    advisory_id: str
    integration_summary: IntegrationSummary
    drift_register: DriftRegister
    accepted_output_register: AcceptedOutputRegister
    rejected_output_register: RejectedOutputRegister
    commit_candidate: CommitCandidate
    command_block: CommitCommandBlock
    push_instruction: PushInstruction
    rollback_note: RollbackNote
    human_approval_required: bool = True
    git_mutation_forbidden_for_agent: bool = True
    limitations: Sequence[str] = field(default_factory=tuple)


def build_drift_register(
    ticket_id: str,
    drift_items: Sequence[DriftItem] = (),
    limitations: Sequence[str] = (),
) -> DriftRegister:
    items = tuple(drift_items)
    unresolved_count = sum(1 for item in items if _is_unresolved_drift(item.status))
    accepted_count = sum(
        1 for item in items if _normal_status(item.status) == "accepted_with_limitations"
    )
    blocked_count = sum(1 for item in items if _normal_status(item.status) == "blocked")
    if blocked_count or unresolved_count:
        status = "blocked_by_unresolved_drift"
    elif accepted_count:
        status = "accepted_with_limitations"
    else:
        status = "clear"
    return DriftRegister(
        drift_register_id=f"{ticket_id}:drift_register",
        ticket_id=ticket_id,
        drift_items=items,
        unresolved_count=unresolved_count,
        accepted_with_limitations_count=accepted_count,
        blocked_count=blocked_count,
        status=status,
        limitations=tuple(limitations),
    )


def build_accepted_output_register(
    ticket_id: str,
    accepted_paths: Sequence[str] = (),
    accepted_items: Sequence[AcceptedOutputItem] = (),
    retention_posture: str = "manual_retention_review_required",
    rollback_posture: str = "manual_rollback_review_required",
    incident_posture: str = "no_incident_claimed",
    limitations: Sequence[str] = (),
) -> AcceptedOutputRegister:
    path_items = tuple(
        AcceptedOutputItem(
            item_id=f"{ticket_id}:accepted:{index}",
            path_ref=path,
            retention_posture=retention_posture,
            rollback_posture=rollback_posture,
            incident_posture=incident_posture,
        )
        for index, path in enumerate(accepted_paths, start=1)
    )
    items = tuple(accepted_items) + path_items
    return AcceptedOutputRegister(
        accepted_register_id=f"{ticket_id}:accepted_output_register",
        ticket_id=ticket_id,
        accepted_items=items,
        path_refs=tuple(item.path_ref for item in items if item.path_ref),
        review_refs=tuple(item.review_ref for item in items if item.review_ref),
        integration_refs=tuple(item.integration_ref for item in items if item.integration_ref),
        retention_posture=retention_posture,
        rollback_posture=rollback_posture,
        incident_posture=incident_posture,
        limitations=tuple(limitations),
    )


def build_rejected_output_register(
    ticket_id: str,
    rejected_paths: Sequence[str] = (),
    rejected_items: Sequence[RejectedOutputItem] = (),
    retention_posture: str = "manual_retention_review_required",
    rollback_posture: str = "manual_rollback_review_required",
    incident_posture: str = "no_incident_claimed",
    limitations: Sequence[str] = (),
) -> RejectedOutputRegister:
    path_items = tuple(
        RejectedOutputItem(
            item_id=f"{ticket_id}:rejected:{index}",
            path_ref=path,
            rejection_reason="rejected path excluded from CommitCandidate",
            retention_posture=retention_posture,
            rollback_posture=rollback_posture,
            incident_posture=incident_posture,
        )
        for index, path in enumerate(rejected_paths, start=1)
    )
    items = tuple(rejected_items) + path_items
    return RejectedOutputRegister(
        rejected_register_id=f"{ticket_id}:rejected_output_register",
        ticket_id=ticket_id,
        rejected_items=items,
        path_refs=tuple(item.path_ref for item in items if item.path_ref),
        rejection_reasons=tuple(item.rejection_reason for item in items if item.rejection_reason),
        review_refs=tuple(item.review_ref for item in items if item.review_ref),
        integration_refs=tuple(item.integration_ref for item in items if item.integration_ref),
        retention_posture=retention_posture,
        rollback_posture=rollback_posture,
        incident_posture=incident_posture,
        limitations=tuple(limitations),
    )


def build_commit_candidate(
    request: IntegrationRenderRequest,
    drift_register: DriftRegister | None = None,
) -> CommitCandidate:
    drift = drift_register or build_drift_register(
        request.ticket_id,
        request.drift_items,
        request.limitations,
    )
    commit_message = _sanitize_commit_message(request.ticket_id, request.ticket_title)
    push_target = _render_push_target(request.target_remote, request.target_branch)
    rollback_note = _render_rollback_note_text(request.ticket_id, request.rollback_notes)
    base_limitations = (
        "CommitCandidate is advisory only",
        "user executes Git manually",
        "agent Git mutation is forbidden",
        "generated output tracking is not approved by P8.15",
        "source tracking expansion is not approved by P8.15",
    )
    limitations = base_limitations + tuple(request.limitations)
    blockers: list[str] = []

    if drift.status == "blocked_by_unresolved_drift":
        blockers.append("unresolved or blocked drift prevents clean commit recommendation")

    path_selection = _select_exact_add_paths(request)
    exact_add_paths = path_selection[0]
    excluded_paths = path_selection[1]
    exclusion_reasons = path_selection[2]
    blockers.extend(path_selection[3])

    if not exact_add_paths:
        blockers.append("no exact accepted add paths available")

    blocked = bool(blockers)
    if blocked:
        exact_add_paths = ()

    if drift.status == "accepted_with_limitations":
        limitations = limitations + ("drift accepted with limitations by supplied metadata",)

    return CommitCandidate(
        commit_candidate_id=f"{request.ticket_id}:commit_candidate",
        ticket_id=request.ticket_id,
        ticket_title=request.ticket_title,
        exact_add_paths=exact_add_paths,
        excluded_paths=excluded_paths,
        generated_output_paths=tuple(request.generated_output_paths),
        ignored_artifact_paths=tuple(request.ignored_artifact_paths),
        quarantined_paths=tuple(request.quarantined_paths),
        commit_message=commit_message,
        push_target=push_target,
        human_approval_required=request.human_approval_required,
        git_mutation_forbidden_for_agent=True,
        never_git_add_dot=True,
        drift_status=drift.status,
        retention_posture=request.retention_posture,
        rollback_note=rollback_note,
        incident_posture=request.incident_posture,
        limitations=limitations,
        blocked=blocked,
        blockers=tuple(_unique_strings(blockers)),
        exclusion_reasons=exclusion_reasons,
    )


def build_commit_command_block(candidate: CommitCandidate) -> CommitCommandBlock:
    limitations = (
        "CommitCommandBlock is advisory only",
        "user executes commands manually",
        "agent must not execute rendered commands",
    ) + tuple(candidate.limitations)
    commands = ["git status --short"]

    if not candidate.blocked:
        commands.extend(f"{GIT_ADD_PREFIX}{_quote_git_path(path)}" for path in candidate.exact_add_paths)
        commands.append(f'git commit -m "{candidate.commit_message}"')
        if candidate.push_target:
            commands.append(f"git push {candidate.push_target}")

    command_tuple = tuple(commands)
    contains_git_add_dot = any(_is_git_add_dot(command) for command in command_tuple)
    contains_wildcards = any(_contains_wildcard(command) for command in command_tuple)
    contains_only_exact_paths = (
        bool(candidate.exact_add_paths)
        and not candidate.blocked
        and not contains_git_add_dot
        and not contains_wildcards
        and all(_is_exact_path(path)[0] for path in candidate.exact_add_paths)
    )
    rendered_text = _render_command_block_text(candidate, command_tuple)
    return CommitCommandBlock(
        command_block_id=f"{candidate.commit_candidate_id}:command_block",
        commit_candidate_ref=candidate.commit_candidate_id,
        commands=command_tuple,
        rendered_text=rendered_text,
        contains_only_exact_paths=contains_only_exact_paths,
        contains_git_add_dot=contains_git_add_dot,
        contains_wildcards=contains_wildcards,
        user_executes_manually=True,
        limitations=limitations,
    )


def build_push_instruction(candidate: CommitCandidate) -> PushInstruction:
    if candidate.blocked or not candidate.push_target:
        rendered_text = "No push instruction is rendered because the CommitCandidate is blocked."
    else:
        rendered_text = (
            "Advisory only. The user may manually run "
            f"`git push {candidate.push_target}` after reviewing the commit."
        )
    target_remote, target_branch = _split_push_target(candidate.push_target)
    return PushInstruction(
        push_instruction_id=f"{candidate.commit_candidate_id}:push_instruction",
        commit_candidate_ref=candidate.commit_candidate_id,
        target_remote=target_remote,
        target_branch=target_branch,
        rendered_text=rendered_text,
        advisory_only=True,
        user_executes_manually=True,
        limitations=(
            "PushInstruction is advisory only",
            "agent must not push",
            "human approval required before push",
        ),
    )


def build_rollback_note(request: IntegrationRenderRequest) -> RollbackNote:
    rendered_text = _render_rollback_note_text(request.ticket_id, request.rollback_notes)
    limitations = (
        "RollbackNote is advisory only",
        "rollback is not executed by AGENT PLATFORM",
    ) + tuple(request.limitations)
    return RollbackNote(
        rollback_note_id=f"{request.ticket_id}:rollback_note",
        ticket_id=request.ticket_id,
        notes=tuple(request.rollback_notes),
        rendered_text=rendered_text,
        human_approval_required=request.human_approval_required,
        limitations=limitations,
    )


def build_integration_summary(
    request: IntegrationRenderRequest,
    accepted_register: AcceptedOutputRegister,
    rejected_register: RejectedOutputRegister,
    drift_register: DriftRegister,
    commit_candidate: CommitCandidate,
) -> IntegrationSummary:
    limitations = tuple(request.limitations)
    if drift_register.status == "accepted_with_limitations":
        limitations = limitations + ("accepted drift limitations remain active",)
    if commit_candidate.blocked:
        limitations = limitations + tuple(commit_candidate.blockers)
    summary = IntegrationSummary(
        integration_summary_id=f"{request.ticket_id}:integration_summary",
        ticket_id=request.ticket_id,
        ticket_title=request.ticket_title,
        accepted_register_ref=accepted_register.accepted_register_id,
        accepted_items=tuple(accepted_register.accepted_items),
        rejected_register_ref=rejected_register.rejected_register_id,
        rejected_items=tuple(rejected_register.rejected_items),
        drift_register_ref=drift_register.drift_register_id,
        drift_items=tuple(drift_register.drift_items),
        commit_candidate_ref=commit_candidate.commit_candidate_id,
        review_summary=_render_review_summary(request.review_verdicts),
        integration_notes=tuple(request.integration_notes),
        limitations=limitations,
        retention_posture=request.retention_posture,
        rollback_posture=request.rollback_posture,
        incident_posture=request.incident_posture,
        human_approval_required=request.human_approval_required,
    )
    return IntegrationSummary(
        **{**summary.__dict__, "rendered_text": render_integration_summary(summary)}
    )


def build_git_advisory(request: IntegrationRenderRequest) -> GitAdvisory:
    drift_register = build_drift_register(
        request.ticket_id,
        request.drift_items,
        request.limitations,
    )
    accepted_register = build_accepted_output_register(
        request.ticket_id,
        request.accepted_paths,
        request.accepted_items,
        request.retention_posture,
        request.rollback_posture,
        request.incident_posture,
        request.limitations,
    )
    rejected_register = build_rejected_output_register(
        request.ticket_id,
        request.rejected_paths,
        request.rejected_items,
        request.retention_posture,
        request.rollback_posture,
        request.incident_posture,
        request.limitations,
    )
    commit_candidate = build_commit_candidate(request, drift_register)
    command_block = build_commit_command_block(commit_candidate)
    push_instruction = build_push_instruction(commit_candidate)
    rollback_note = build_rollback_note(request)
    integration_summary = build_integration_summary(
        request,
        accepted_register,
        rejected_register,
        drift_register,
        commit_candidate,
    )
    return GitAdvisory(
        advisory_id=f"{request.ticket_id}:git_advisory",
        integration_summary=integration_summary,
        drift_register=drift_register,
        accepted_output_register=accepted_register,
        rejected_output_register=rejected_register,
        commit_candidate=commit_candidate,
        command_block=command_block,
        push_instruction=push_instruction,
        rollback_note=rollback_note,
        human_approval_required=request.human_approval_required,
        git_mutation_forbidden_for_agent=True,
        limitations=(
            "advisory rendering only",
            "manual Git authority preserved",
            "no automatic integration",
        ) + tuple(request.limitations),
    )


def render_integration_summary(summary: IntegrationSummary) -> str:
    lines = [
        f"# IntegrationSummary: {summary.ticket_id}",
        "",
        f"Ticket: {summary.ticket_title}",
        f"Accepted register: {summary.accepted_register_ref}",
        f"Rejected register: {summary.rejected_register_ref}",
        f"Drift register: {summary.drift_register_ref}",
        f"Commit candidate: {summary.commit_candidate_ref}",
        f"Human approval required: {summary.human_approval_required}",
        f"Retention posture: {summary.retention_posture}",
        f"Rollback posture: {summary.rollback_posture}",
        f"Incident posture: {summary.incident_posture}",
        "",
        "## Review Summary",
        summary.review_summary,
        "",
        "## Integration Notes",
    ]
    lines.extend(_bullet_lines(summary.integration_notes))
    lines.extend(("", "## Limitations"))
    lines.extend(_bullet_lines(summary.limitations))
    return "\n".join(lines)


def render_drift_register(register: DriftRegister) -> str:
    lines = [
        f"# DriftRegister: {register.ticket_id}",
        "",
        f"Status: {register.status}",
        f"Unresolved count: {register.unresolved_count}",
        f"Accepted with limitations count: {register.accepted_with_limitations_count}",
        f"Blocked count: {register.blocked_count}",
        "",
        "## Drift Items",
    ]
    if register.drift_items:
        for item in register.drift_items:
            lines.append(
                f"- {item.drift_item_id}: {item.status} - {item.description}"
            )
    else:
        lines.append("- none")
    lines.extend(("", "## Limitations"))
    lines.extend(_bullet_lines(register.limitations))
    return "\n".join(lines)


def render_accepted_output_register(register: AcceptedOutputRegister) -> str:
    lines = [
        f"# AcceptedOutputRegister: {register.ticket_id}",
        "",
        f"Retention posture: {register.retention_posture}",
        f"Rollback posture: {register.rollback_posture}",
        f"Incident posture: {register.incident_posture}",
        "",
        "## Accepted Items",
    ]
    if register.accepted_items:
        for item in register.accepted_items:
            lines.append(f"- {item.item_id}: {item.path_ref} - {item.rationale}")
    else:
        lines.append("- none")
    lines.extend(("", "## Limitations"))
    lines.extend(_bullet_lines(register.limitations))
    return "\n".join(lines)


def render_rejected_output_register(register: RejectedOutputRegister) -> str:
    lines = [
        f"# RejectedOutputRegister: {register.ticket_id}",
        "",
        f"Retention posture: {register.retention_posture}",
        f"Rollback posture: {register.rollback_posture}",
        f"Incident posture: {register.incident_posture}",
        "",
        "## Rejected Items",
    ]
    if register.rejected_items:
        for item in register.rejected_items:
            ref = item.path_ref or item.output_id
            lines.append(f"- {item.item_id}: {ref} - {item.rejection_reason}")
    else:
        lines.append("- none")
    lines.extend(("", "## Limitations"))
    lines.extend(_bullet_lines(register.limitations))
    return "\n".join(lines)


def _select_exact_add_paths(
    request: IntegrationRenderRequest,
) -> tuple[tuple[str, ...], tuple[str, ...], dict[str, tuple[str, ...]], tuple[str, ...]]:
    accepted_path_inputs = tuple(request.accepted_paths) + tuple(
        item.path_ref for item in request.accepted_items if item.path_ref
    )
    rejected_path_inputs = tuple(request.rejected_paths) + tuple(
        item.path_ref for item in request.rejected_items if item.path_ref
    )
    changed_paths = set(
        _normalize_path(path)
        for path in tuple(request.created_paths) + tuple(request.modified_paths) + tuple(request.deleted_paths)
        if _normalize_path(path)
    )
    rejected = set(_normalize_path(path) for path in rejected_path_inputs if _normalize_path(path))
    generated = set(
        _normalize_path(path) for path in request.generated_output_paths if _normalize_path(path)
    )
    ignored = set(
        _normalize_path(path) for path in request.ignored_artifact_paths if _normalize_path(path)
    )
    quarantined = set(_normalize_path(path) for path in request.quarantined_paths if _normalize_path(path))
    blocked = set(_normalize_path(path) for path in request.blocked_paths if _normalize_path(path))
    unknown = set(
        _normalize_path(path) for path in request.unknown_sensitivity_paths if _normalize_path(path)
    )
    explicit_excluded = set(
        _normalize_path(path) for path in request.excluded_paths if _normalize_path(path)
    )

    exact_paths: list[str] = []
    excluded_paths: list[str] = []
    exclusion_reasons: dict[str, tuple[str, ...]] = {}
    blockers: list[str] = []

    for raw_path in accepted_path_inputs:
        normalized = _normalize_path(raw_path)
        valid, reasons = _is_exact_path(raw_path)
        path_reasons = list(reasons)
        if not normalized:
            normalized = str(raw_path)
        if normalized not in changed_paths:
            path_reasons.append("path_not_declared_created_modified_or_deleted")
        if normalized in rejected:
            path_reasons.append("path_rejected")
        if normalized in ignored:
            path_reasons.append("ignored_artifact_excluded")
        if normalized in quarantined:
            path_reasons.append("quarantined_artifact_excluded")
        if normalized in blocked:
            path_reasons.append("blocked_path_excluded")
        if normalized in unknown:
            path_reasons.append("unknown_sensitivity_path_excluded")
        if normalized in explicit_excluded:
            path_reasons.append("explicitly_excluded")
        if normalized in generated and not request.tracking_allowed_by_future_gate:
            path_reasons.append("generated_output_excluded_without_future_gate")
        if _is_sensitive_or_blocked_path(normalized, request.product_source_gate_approved):
            path_reasons.append("sensitive_or_blocked_path_excluded")

        if valid and not path_reasons:
            exact_paths.append(normalized)
        else:
            excluded_paths.append(normalized)
            exclusion_reasons[normalized] = tuple(_unique_strings(path_reasons))

    for raw_path in rejected_path_inputs + tuple(request.excluded_paths):
        normalized = _normalize_path(raw_path)
        if normalized:
            excluded_paths.append(normalized)
            exclusion_reasons.setdefault(normalized, ("not_accepted_for_commit",))

    for raw_path in tuple(request.ignored_artifact_paths) + tuple(request.quarantined_paths):
        normalized = _normalize_path(raw_path)
        if normalized:
            excluded_paths.append(normalized)
            exclusion_reasons.setdefault(normalized, ("artifact_excluded_by_policy",))

    for raw_path in request.generated_output_paths:
        normalized = _normalize_path(raw_path)
        if normalized and normalized not in exact_paths:
            excluded_paths.append(normalized)
            exclusion_reasons.setdefault(
                normalized,
                ("generated_output_excluded_by_default",),
            )

    for path, reasons in exclusion_reasons.items():
        if any(reason.endswith("excluded") or reason.startswith("path_") for reason in reasons):
            blockers.append(f"excluded unsafe or ineligible path: {path}")

    return (
        tuple(_unique_strings(exact_paths)),
        tuple(_unique_strings(excluded_paths)),
        exclusion_reasons,
        tuple(_unique_strings(blockers)),
    )


def _is_exact_path(raw_path: str) -> tuple[bool, tuple[str, ...]]:
    path = _normalize_path(raw_path)
    reasons: list[str] = []
    if not path:
        reasons.append("empty_path")
    if path in {".", "./"}:
        reasons.append("dot_path_forbidden")
    if _is_absolute_or_drive_path(str(raw_path)) or _is_absolute_or_drive_path(path):
        reasons.append("absolute_path_forbidden")
    if ".." in path.split("/"):
        reasons.append("path_traversal_forbidden")
    if _contains_wildcard(path):
        reasons.append("wildcard_or_glob_forbidden")
    if any(char in path for char in SHELL_META_CHARS):
        reasons.append("shell_metacharacter_forbidden")
    if any(char in path for char in ("\n", "\r", "\t", "\0")):
        reasons.append("control_character_forbidden")
    return (not reasons, tuple(reasons))


def _normalize_path(raw_path: str) -> str:
    path = str(raw_path).strip().replace("\\", "/")
    while path.startswith("./"):
        path = path[2:]
    while "//" in path:
        path = path.replace("//", "/")
    return path.rstrip("/") if path != "/" else path


def _is_absolute_or_drive_path(path: str) -> bool:
    if path.startswith("/") or path.startswith("\\"):
        return True
    return len(path) >= 2 and path[1] == ":"


def _contains_wildcard(value: str) -> bool:
    return any(char in value for char in WILDCARD_CHARS)


def _is_git_add_dot(command: str) -> bool:
    normalized = " ".join(command.strip().lower().split())
    return normalized == BAD_GIT_ADD_DOT


def _is_sensitive_or_blocked_path(path: str, product_source_gate_approved: bool) -> bool:
    lowered = path.lower()
    blocked_exact = {".env", ".gitignore", ".graphifyignore"}
    blocked_prefixes = (
        ".git/",
        "9_artifacts/",
        "graphify-out/",
        "4_external/sources/",
        "external/sources/",
    )
    sensitive_markers = (
        "/.env",
        "secret",
        "credential",
        "token",
        "api_key",
        "apikey",
        "provider_config",
        "provider-config",
        "browser_auth",
        "local_credential_store",
    )
    product_markers = (
        "siamese/",
        "/siamese/",
        "product/",
        "products/",
        "omniverse",
        "energyplus",
    )
    if lowered in blocked_exact:
        return True
    if any(lowered.startswith(prefix) for prefix in blocked_prefixes):
        return True
    if any(marker in lowered for marker in sensitive_markers):
        return True
    return not product_source_gate_approved and any(
        marker in lowered for marker in product_markers
    )


def _sanitize_commit_message(ticket_id: str, ticket_title: str) -> str:
    raw = f"{ticket_id} - {ticket_title}"
    sanitized = raw.replace("\r", " ").replace("\n", " ").replace('"', "'")
    return " ".join(sanitized.split()) or "MVP-0 integration advisory update"


def _quote_git_path(path: str) -> str:
    if any(char.isspace() for char in path):
        return f'"{path}"'
    return path


def _render_push_target(remote: str, branch: str) -> str:
    safe_remote = _sanitize_push_part(remote) or DEFAULT_REMOTE
    safe_branch = _sanitize_push_part(branch) or DEFAULT_BRANCH
    return f"{safe_remote} {safe_branch}"


def _split_push_target(push_target: str) -> tuple[str, str]:
    parts = push_target.split()
    if len(parts) == 2:
        return (parts[0], parts[1])
    return (DEFAULT_REMOTE, DEFAULT_BRANCH)


def _sanitize_push_part(value: str) -> str:
    stripped = str(value).strip()
    if not stripped or _contains_wildcard(stripped):
        return ""
    if any(char in stripped for char in SHELL_META_CHARS):
        return ""
    if any(char in stripped for char in ("\n", "\r", "\t", "\0", "/", "\\")):
        return ""
    return stripped


def _render_command_block_text(candidate: CommitCandidate, commands: Sequence[str]) -> str:
    lines = [
        "CommitCommandBlock advisory only.",
        "The user executes these commands manually after review.",
    ]
    if candidate.blocked:
        lines.append("Clean commit recommendation blocked.")
        lines.extend(_bullet_lines(candidate.blockers))
    lines.append("")
    lines.append("```powershell")
    lines.extend(commands)
    lines.append("```")
    return "\n".join(lines)


def _render_rollback_note_text(ticket_id: str, rollback_notes: Sequence[str]) -> str:
    lines = [
        f"RollbackNote for {ticket_id} is advisory only.",
        "The user remains responsible for any rollback decision and Git action.",
    ]
    lines.extend(_bullet_lines(rollback_notes))
    return "\n".join(lines)


def _render_review_summary(review_verdicts: Sequence[str]) -> str:
    if not review_verdicts:
        return "manual review metadata supplied; no final approval implied"
    return "; ".join(" ".join(str(verdict).split()) for verdict in review_verdicts)


def _bullet_lines(values: Sequence[str]) -> list[str]:
    if not values:
        return ["- none"]
    return [f"- {value}" for value in values]


def _normal_status(status: str) -> str:
    return str(status).strip().lower().replace("-", "_").replace(" ", "_")


def _is_unresolved_drift(status: str) -> bool:
    return _normal_status(status) in {"unresolved", "pending", "open"}


def _unique_strings(values: Sequence[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        string_value = str(value)
        if string_value not in seen:
            seen.add(string_value)
            unique.append(string_value)
    return tuple(unique)
