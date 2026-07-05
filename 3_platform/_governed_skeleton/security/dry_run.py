"""Pure in-memory security dry-run evaluator.

The evaluator accepts caller-supplied SecuritySubject metadata and returns
SecurityDryRunResult metadata. It performs no scanner behavior, file reads,
environment inspection, credential inspection, secret inspection, provider
calls, network calls, tool invocation, persistence, or enforcement activation.
"""

from __future__ import annotations

from .models import (
    DenyReason,
    SecurityDecision,
    SecurityDecisionStatus,
    SecurityDryRunResult,
    SecurityFinding,
    SecuritySubject,
)
from .policy import SecurityPolicy, default_deny_policy


DRY_RUN_LIMITATION = "dry-run result is not runtime enforcement"


class SecurityDryRunEvaluator:
    """Evaluate supplied metadata against a SecurityPolicy in memory only."""

    def __init__(self, policy: SecurityPolicy | None = None) -> None:
        self.policy = policy if policy is not None else default_deny_policy()

    def evaluate(self, subject: SecuritySubject) -> SecurityDryRunResult:
        """Evaluate one caller-supplied SecuritySubject without side effects."""

        if not isinstance(subject, SecuritySubject):
            raise TypeError("SecurityDryRunEvaluator.evaluate accepts SecuritySubject only")

        reasons: list[DenyReason] = []

        if subject.source_classification in self.policy.blocked_source_classifications:
            reasons.append(
                DenyReason(
                    reason_id="P5.2-DENY-SOURCE-CLASS",
                    reason_code="blocked_source_classification",
                    message="Subject source classification is blocked by policy.",
                    required_gate="GT-01/GT-05 as applicable",
                    blocker_refs=("source_loading_blocker",),
                )
            )

        if subject.sensitivity in self.policy.blocked_sensitivities:
            reasons.append(
                DenyReason(
                    reason_id="P5.2-DENY-SENSITIVITY",
                    reason_code="blocked_sensitivity",
                    message="Subject sensitivity is blocked by policy.",
                    required_gate="GT-05/GT-15 as applicable",
                    blocker_refs=("security_review_blocker",),
                )
            )

        for flag_name in self.policy.blocked_subject_flags:
            if getattr(subject, flag_name):
                reasons.append(
                    DenyReason(
                        reason_id=f"P5.2-DENY-FLAG-{flag_name.upper()}",
                        reason_code="blocked_subject_flag",
                        message=f"Subject flag {flag_name} is blocked by policy.",
                        required_gate="future exact governance gate",
                        blocker_refs=(flag_name,),
                    )
                )

        if reasons:
            status = SecurityDecisionStatus.DENY
        else:
            defer_reason = self._defer_reason(subject)
            if defer_reason is not None:
                reasons = [defer_reason]
                status = SecurityDecisionStatus.DEFER
            else:
                status = SecurityDecisionStatus.ALLOW_METADATA_ONLY

        findings = self._findings(subject, status, tuple(reasons))
        limitations = (DRY_RUN_LIMITATION,) + subject.limitations
        decision = SecurityDecision(
            decision_id=f"P5.2-SECURITY-DECISION-{subject.subject_id}",
            subject_id=subject.subject_id,
            status=status,
            reasons=tuple(reasons),
            findings=findings,
            human_approval_required=True,
            runtime_activation_approved=False,
            enforcement_active=False,
            limitations=limitations,
        )
        return SecurityDryRunResult(
            result_id=f"P5.2-SECURITY-DRY-RUN-{subject.subject_id}",
            policy_id=self.policy.policy_id,
            subject_id=subject.subject_id,
            decision=decision,
            findings=findings,
            dry_run_only=True,
            side_effects=(),
            limitations=limitations,
        )

    def _defer_reason(self, subject: SecuritySubject) -> DenyReason | None:
        if not subject.subject_id or not subject.subject_type:
            return DenyReason(
                reason_id="P5.2-DEFER-MISSING-SUBJECT-METADATA",
                reason_code="missing_subject_metadata",
                message="Subject identity or type is missing; posture remains deferred.",
                required_gate="metadata completeness review",
                blocker_refs=("unknown_sensitivity_blocker",),
            )
        if not subject.metadata_only:
            return DenyReason(
                reason_id="P5.2-DEFER-NON-METADATA-ONLY",
                reason_code="non_metadata_only_subject",
                message="Subject is not declared metadata-only; posture remains deferred.",
                required_gate="future exact governance gate",
                blocker_refs=("runtime_activation_blocker",),
            )
        if subject.blockers:
            return DenyReason(
                reason_id="P5.2-DEFER-ACTIVE-BLOCKERS",
                reason_code="active_subject_blockers",
                message="Subject carries blockers that require future review.",
                required_gate="blocker-specific review",
                blocker_refs=subject.blockers,
            )
        return None

    def _findings(
        self,
        subject: SecuritySubject,
        status: SecurityDecisionStatus,
        reasons: tuple[DenyReason, ...],
    ) -> tuple[SecurityFinding, ...]:
        return tuple(
            SecurityFinding(
                finding_id=f"P5.2-SECURITY-FINDING-{subject.subject_id}-{index}",
                subject_id=subject.subject_id,
                decision_status=status,
                reason=reason,
                evidence_refs=subject.evidence_refs,
                validation_refs=subject.validation_refs,
                security_refs=subject.security_refs,
                limitations=(DRY_RUN_LIMITATION,) + subject.limitations,
            )
            for index, reason in enumerate(reasons, start=1)
        )
