"""Immutable human evidence for required manual WorkPacket validations."""

import hashlib
import json
from pathlib import Path
from typing import Any

from hermes_constants import get_hermes_home

POLICY = "pepper-manual-validation-v1"


def digest(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    return hashlib.sha256((POLICY + ":" + payload).encode("utf-8")).hexdigest()


def required_items(contract: dict) -> list[dict]:
    """Use the compiled contract, retaining wording and explicit requiredness."""
    items = []
    seen = set()
    for step in contract.get("work_packet_validation_steps", []):
        if (
            not isinstance(step, dict)
            or step.get("kind") != "manual"
            or step.get("required") is not True
        ):
            continue
        item = dict(step)
        validation_id = item.get("validation_id")
        if (
            not isinstance(validation_id, str)
            or not validation_id.strip()
            or validation_id in seen
        ):
            raise ValueError("manual validation id is missing or ambiguous")
        if (
            item.get("command") is not None
            or item.get("command_execution_authorized") is not False
        ):
            raise ValueError("manual validation must not authorize a command")
        seen.add(validation_id)
        items.append(item)
    return items


def binding(contract: dict, completion: dict, item: dict) -> dict:
    fields = (
        "project_id",
        "ticket_id",
        "ticket_spec_SHA256",
        "work_packet_id",
        "work_packet_SHA256",
    )
    result = {key: contract.get(key) for key in fields}
    metadata = completion.get("run_metadata")
    metadata = metadata if isinstance(metadata, dict) else {}
    # PREPARE enriches validation metadata, not the terminal candidate/run.
    # Keep the original completion binding (as zero-change authority does),
    # while independently binding all non-metadata terminal result fields.
    completion_sha = metadata.get(
        "review_prepare_pre_validation_completion_SHA256"
    ) or completion.get("kanban_completion_result_SHA256")
    result.update({
        "run_id": completion.get("run_id"),
        "kanban_board_slug": completion.get("kanban_board_slug"),
        "kanban_task_id": completion.get("kanban_task_id"),
        "completion_SHA256": completion_sha,
        "terminal_result_SHA256": digest({
            key: value
            for key, value in completion.items()
            if key not in {"run_metadata", "kanban_completion_result_SHA256"}
        }),
        "validation_id": item["validation_id"],
        "validation_item": item,
        "validation_contract_SHA256": digest(contract),
    })
    if any(
        result.get(key) in (None, "")
        for key in (*fields, "completion_SHA256", "kanban_board_slug", "kanban_task_id")
    ):
        raise ValueError("manual validation binding is incomplete")
    if type(result["run_id"]) is not int or result["run_id"] < 1:
        raise ValueError("manual validation requires an exact run id")
    return result


def record_path(identity: dict) -> Path:
    return (
        get_hermes_home()
        / "agent-platform"
        / "manual-validation"
        / (digest(identity) + ".json")
    )


def attestation_text(identity: dict, status: str) -> str:
    return (
        f"I attest manual validation {identity['validation_id']} {status} for "
        f"{identity['ticket_id']}, WorkPacket {identity['work_packet_id']} "
        f"({identity['work_packet_SHA256']}), run {identity['run_id']}, "
        f"contract {identity['validation_contract_SHA256']}."
    )


def validate_record(record: dict, identity: dict) -> dict:
    body = {key: value for key, value in record.items() if key != "evidence_SHA256"}
    if (
        record.get("evidence_SHA256") != digest(body)
        or record.get("binding") != identity
    ):
        raise ValueError("manual validation evidence identity/digest mismatch")
    if record.get("policy_id") != POLICY or record.get("status") not in {
        "passed",
        "failed",
    }:
        raise ValueError("invalid manual validation decision")
    if record.get("human_attestation_text") != attestation_text(
        identity, record["status"]
    ):
        raise ValueError("invalid manual validation attestation")
    if not isinstance(record.get("evidence"), str) or not record["evidence"].strip():
        raise ValueError("manual validation evidence is missing")
    if not isinstance(record.get("actor"), str) or not record["actor"].strip():
        raise ValueError("manual validation actor is missing")
    return record


def load(identity: dict) -> dict | None:
    path = record_path(identity)
    if not path.exists():
        return None
    record = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        raise ValueError("invalid manual validation record")
    return validate_record(record, identity)


def inspect(contract: dict, completion: dict) -> list[dict]:
    items = []
    for item in required_items(contract):
        identity = binding(contract, completion, item)
        record = load(identity)
        items.append({
            **item,
            "binding": identity,
            "binding_SHA256": digest(identity),
            "status": record["status"] if record else "pending",
            "evidence_SHA256": record["evidence_SHA256"] if record else None,
            "evidence": record["evidence"] if record else None,
            "dependency_evidence": record.get("dependency_evidence") if record else None,
            "source_authority": POLICY,
            "human_action_required": record is None,
            "required_attestation_text": {
                status: attestation_text(identity, status)
                for status in ("passed", "failed")
            },
        })
    from .command_validation import dependency_evidence
    for item in items:
        if item["status"] == "passed" and item.get("dependency_evidence") is not None:
            if item["dependency_evidence"] != dependency_evidence(item, contract, completion, items):
                raise ValueError("manual validation dependency evidence changed; governed resolution required")
    return items


def persist(
    identity: dict,
    *,
    status: str,
    human_attestation_text: str,
    evidence: str,
    actor: str,
    dependency_evidence: dict | None = None,
) -> tuple[dict, bool]:
    if status not in {"passed", "failed"}:
        raise ValueError("manual validation status must be passed or failed")
    if not isinstance(evidence, str) or not 1 <= len(evidence.strip()) <= 8000:
        raise ValueError(
            "explicit human validation evidence is required (1-8000 characters)"
        )
    record = {
        "policy_id": POLICY,
        "binding": identity,
        "status": status,
        "human_attestation_text": human_attestation_text,
        "evidence": evidence,
        "actor": actor,
    }
    if dependency_evidence:
        record["dependency_evidence"] = dependency_evidence
    record["evidence_SHA256"] = digest(record)
    validate_record(record, identity)
    path = record_path(identity)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
    except FileExistsError:
        existing = load(identity)
        if existing != record:
            raise ValueError("conflicting immutable manual validation evidence")
        return existing, True
    return record, False
