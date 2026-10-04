"""Bounded diagnostics for the non-persisting material-revision preflight."""

from contextlib import contextmanager

ISSUE_LIMIT = 32
TEXT_LIMIT = 600


def _text(value):
    from .ticket_architect_bridge import _safe_lint_diagnostic_text

    return _safe_lint_diagnostic_text(value, fallback="unavailable")[:TEXT_LIMIT]


def run(stage, function, *args, _failure_context=None, **kwargs):
    """Tag the innermost failing construction stage without changing its rules."""
    try:
        return function(*args, **kwargs)
    except Exception as exc:
        metadata = {
            **(_failure_context or {}),
            **(getattr(exc, "failure_metadata", None) or {}),
        }
        metadata.setdefault("source_stage", stage)
        exc.failure_metadata = metadata
        raise


def _issues(exc, metadata, stage):
    from .ticket_architect_bridge import _revision_exception_chain

    lint = metadata.get("lint_diagnostics")
    if isinstance(lint, list):
        count = metadata["lint_summary"]["diagnostic_count"]
        return [
            {
                "issue_code": _text(d.get("code")),
                "severity": d.get("severity"),
                "field_path": _text(d.get("field_path")),
                "message": _text(d.get("message")),
                "expected_constraint": _text(
                    metadata.get("material_revision_lint_remediations", {}).get(
                        d.get("diagnostic_id")
                    )
                ),
                "actual_value_summary": "See the named field in the submitted revision contract; raw values omitted.",
                "source_stage": stage,
            }
            for d in lint[:ISSUE_LIMIT]
        ], count
    if metadata.get("revision_issue"):
        return [{**metadata["revision_issue"], "source_stage": stage}], 1
    for cause in _revision_exception_chain(exc):
        if not hasattr(cause, "errors"):
            continue
        errors = cause.errors(include_input=False, include_url=False)
        issues = []
        for item in errors[:ISSUE_LIMIT]:
            limits = {
                key: value
                for key, value in (item.get("ctx") or {}).items()
                if key
                in {"min_length", "max_length", "ge", "le", "pattern", "expected"}
                and isinstance(value, (str, int, float, bool))
            }
            issues.append({
                "issue_code": "schema." + _text(item["type"]),
                "severity": "error",
                "field_path": _text(".".join(map(str, item.get("loc") or ())) or "$"),
                "message": _text(item["msg"]),
                "expected_constraint": _text(limits) if limits else None,
                "actual_value_summary": "Rejected input omitted; no raw input or model dump is exposed.",
                "source_stage": stage,
            })
        return issues, len(errors)
    return [
        {
            "issue_code": "material_revision_preflight_failed",
            "severity": "error",
            "field_path": "$",
            "message": _text(exc),
            "expected_constraint": None,
            "actual_value_summary": None,
            "source_stage": stage,
        }
    ], 1


@contextmanager
def preflight(*, ticket_id, revision_attempt):
    """Only wrap construction/validation, never a block that persists authority."""
    from . import ticket_architect_bridge as bridge

    try:
        yield
    except Exception as exc:
        metadata = bridge._bridge_failure_metadata(exc)
        stage = metadata.get("source_stage", "ticketspec_build")
        issues, count = _issues(exc, metadata, stage)
        envelope = {
            "diagnostic_policy_id": "pepper-material-revision-preflight-v1",
            "ticket_id": ticket_id,
            "revision_attempt": revision_attempt,
            "revision_status": "preflight_failed",
            "source_stage": stage,
            "lint_passed": bool(metadata.get("lint_passed", False)),
            "lint_evaluated": bool(
                metadata.get("lint_evaluated", "lint_diagnostics" in metadata)
            ),
            "lint_issue_count": metadata.get("lint_summary", {}).get(
                "diagnostic_count", 0
            ),
            "issue_count": count,
            "issues": issues,
            "issues_omitted_count": max(0, count - len(issues)),
            "issues_truncated": count > len(issues),
            "generated_pre_lint_ticket_spec_SHA256": metadata.get(
                "generated_pre_lint_ticket_spec_SHA256"
            ),
            "publication_occurred": False,
            "generation_record_changed": False,
            "approval_occurred": False,
            "projection_occurred": False,
            "task_created": False,
            "execution_started": False,
            "Git_mutation": False,
            "auto_retry": False,
        }
        error_type = (
            bridge.TicketArchitectBridgeInputError
            if isinstance(exc, bridge.TicketArchitectBridgeInputError)
            else bridge.TicketArchitectBridgeGenerationError
        )
        # Keep the public error bounded too; Pydantic str(exc) contains raw input.
        message = (
            "structured TicketSpec revision contract is invalid"
            if stage == "revision_contract_validation"
            else f"{ticket_id} material revision preflight failed at {stage}"
        )
        raise error_type(
            message, failure_envelope=envelope, failure_metadata=metadata
        ) from exc
