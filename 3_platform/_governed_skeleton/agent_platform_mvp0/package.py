"""No-op package facade for MVP-0 metadata placeholders."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .boundary import DEFAULT_MVP0_BOUNDARY_POLICY, Mvp0BoundaryPolicy
from .contracts import (
    CommitCandidateRef,
    HarnessInputPackageDraftRef,
    HarnessOutputPackageRef,
    IntegrationChecklistRef,
    Mvp0BlockedReason,
    Mvp0OperationResult,
    ReviewChecklistRef,
    UserObjectiveEnvelope,
    WorkPacketDraftRef,
)
from .noop import build_blocked_result


@dataclass(frozen=True)
class NoOpMvp0Package:
    """Non-executing facade for future MVP-0 surfaces.

    Methods create metadata envelopes/refs or blocked operation results. They
    do not render full WorkPackets, parse harness output, execute review,
    integrate outputs, render final Git commands, persist state, read files,
    call external systems, or mutate Git.
    """

    boundary_policy: Mvp0BoundaryPolicy = DEFAULT_MVP0_BOUNDARY_POLICY

    def capture_user_objective_metadata(
        self,
        objective_id: str = "user_objective_metadata_only",
        title: str = "metadata-only user objective",
        description: str = "not executed",
    ) -> UserObjectiveEnvelope:
        return UserObjectiveEnvelope(
            objective_id=objective_id,
            title=title,
            description=description,
        )

    def draft_work_packet_ref(
        self,
        draft_id: str = "work_packet_draft_ref_metadata_only",
        title: str = "metadata-only WorkPacket draft ref",
    ) -> WorkPacketDraftRef:
        return WorkPacketDraftRef(draft_id=draft_id, title=title)

    def draft_harness_input_ref(
        self,
        draft_id: str = "harness_input_package_draft_ref_metadata_only",
        target_harness: str = "H0_user_operated_harness",
    ) -> HarnessInputPackageDraftRef:
        return HarnessInputPackageDraftRef(draft_id=draft_id, target_harness=target_harness)

    def record_harness_output_ref(
        self,
        package_id: str = "harness_output_package_ref_metadata_only",
        source_harness: str = "user_pasted_harness_output",
    ) -> HarnessOutputPackageRef:
        return HarnessOutputPackageRef(package_id=package_id, source_harness=source_harness)

    def draft_review_checklist_ref(
        self,
        checklist_id: str = "review_checklist_ref_metadata_only",
    ) -> ReviewChecklistRef:
        return ReviewChecklistRef(checklist_id=checklist_id)

    def draft_integration_checklist_ref(
        self,
        checklist_id: str = "integration_checklist_ref_metadata_only",
    ) -> IntegrationChecklistRef:
        return IntegrationChecklistRef(checklist_id=checklist_id)

    def draft_commit_candidate_ref(
        self,
        commit_candidate_id: str = "commit_candidate_ref_metadata_only",
    ) -> CommitCandidateRef:
        return CommitCandidateRef(commit_candidate_id=commit_candidate_id)

    def blocked_operation(
        self,
        operation_name: str = "blocked_mvp0_operation",
        blocked_reasons: Tuple[Mvp0BlockedReason, ...] = (Mvp0BlockedReason.UNKNOWN,),
    ) -> Mvp0OperationResult:
        return build_blocked_result(
            operation_name=operation_name,
            blocked_reasons=blocked_reasons,
        )
