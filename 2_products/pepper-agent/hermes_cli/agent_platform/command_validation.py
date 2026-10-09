"""Human-authorized command evidence before final manual validation/review.

The compiled contract has no dependency graph. Commands therefore have no
manual prerequisites. Independently supportable items remain attestable at any
time; explicit item references and regression-debt conclusions are downstream
of command evidence. These are derived gates, never new immutable item fields.
"""

import hashlib
import json
import re

from hermes_constants import get_hermes_home
from . import manual_validation as mv
from .post_accept_material_revision import serialized

POLICY = "pepper-pre-review-command-validation-v1"
MAX_BYTES = 4 * 1024 * 1024


def digest(value):
    return hashlib.sha256((POLICY + ":" + json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False,
    )).encode()).hexdigest()


def action_id(ticket):
    from . import product_runtime as pr
    return f"VALIDATE_{pr.governed_ticket_lifecycle_action_token(ticket)}_COMMANDS"


def identity(projection, completion, contract):
    from .workflow import ticket_architect_bridge as bridge
    generation = bridge.load_generation_record(ticket_id=projection["ticket_id"])
    if not generation or generation["work_packet_SHA256"] != projection["work_packet_SHA256"]:
        raise ValueError("command validation current generation mismatch")
    from .command_validation_context import canonical_source
    source = canonical_source(projection, completion)
    return {
        **({"canonical_validation_source": source} if source else {}),
        **{key: projection[key] for key in (
            "project_id", "ticket_id", "ticket_spec_SHA256", "work_packet_id",
            "work_packet_SHA256", "projection_SHA256", "kanban_board_slug", "kanban_task_id",
        )},
        "revision": bridge._publication_from_generation_record(generation).revision,
        "run_id": completion["run_id"],
        "completion_SHA256": completion["kanban_completion_result_SHA256"],
        "validation_contract_SHA256": mv.digest(contract),
    }


def path_for(binding):
    return get_hermes_home() / "agent-platform/pre-review-command-validation" / (digest(binding) + ".json")


def consent(binding):
    return f"{action_id(binding['ticket_id'])} BINDING {digest(binding)}"


def load(binding):
    path = path_for(binding)
    if not path.exists():
        return None
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("command validation evidence exceeds bound")
    record = json.loads(raw)
    if not isinstance(record, dict) or record.get("record_SHA256") != digest({
        k: v for k, v in record.items() if k != "record_SHA256"
    }):
        raise ValueError("command validation record digest mismatch")
    if record.get("policy_id") != POLICY or record.get("binding") != binding or record.get("human_authorization_text") != consent(binding):
        raise ValueError("command validation authority mismatch")
    from tools import workpacket_validation_tool as vt
    validation = record["validation"]
    authority = validation["review_prepare_validation_authority"]
    if not isinstance(authority, dict) or authority.get("pre_review_binding") != binding:
        raise ValueError("command result current authority mismatch")
    expected = vt._digest_payload(vt._REVIEW_PREPARE_VALIDATION_AUTHORITY_DIGEST_ALGORITHM, {
        k: v for k, v in authority.items() if k != "review_prepare_validation_authority_SHA256"
    })
    if authority.get("review_prepare_validation_authority_SHA256") != expected or validation.get("review_prepare_validation_authority_SHA256") != expected:
        raise ValueError("command authority digest mismatch")
    for result in validation["validation_command_results"]:
        if (result.get("review_prepare_validation_authority") != authority
                or result.get("review_prepare_validation_authority_SHA256") != expected
                or result.get("validation_result_SHA256") != vt._validation_result_payload_digest(result)):
            raise ValueError("command result digest/authority mismatch")
    return record


def enrich(projection, completion, contract=None):
    """Derive evidence without changing the durable terminal completion."""
    from . import product_runtime as pr
    if completion.get("blocker_code") or not completion.get("run_id"):
        return completion
    # Legacy tickets without this new evidence retain their exact read behavior.
    directory = get_hermes_home() / "agent-platform/pre-review-command-validation"
    if not directory.exists():
        return completion
    contract = contract or pr._acceptance_contract_for_review_projection(projection)
    record = load(identity(projection, completion, contract))
    if record is None:
        return completion
    return pr._review_completion_with_prepare_validation_results(completion, validation=record["validation"])


def dependencies(item, contract):
    """Derive only explicit cross-item references and regression-debt evidence.

    Self references (e.g. 'V7 smoke') do not establish dependencies. A generic
    numeric range includes every existing item in that range. No ticket IDs or
    particular validation numbers are policy inputs.
    """
    text = " ".join(str(item.get(k) or "") for k in ("description", "expected_result"))
    steps = contract.get("work_packet_validation_steps", [])
    ids = {step["validation_id"] for step in steps}
    refs = set(re.findall(r"\b[A-Z]+\d+\b", text)) & ids
    for prefix, first, last in re.findall(r"\b([A-Z]+)(\d+)\s*[-–]\s*(?:[A-Z]+)?(\d+)\b", text):
        refs.update(i for i in ids if re.fullmatch(prefix + r"\d+", i) and int(first) <= int(i[len(prefix):]) <= int(last))
    if re.search(r"regression\s+failures|known[- ]debt|command\s+results", text, re.I):
        refs.update(step["validation_id"] for step in steps if step.get("kind") == "command" and step.get("required"))
    return sorted(refs - {item["validation_id"]})


def manual_blocker(item, contract, completion, items):
    from tools import workpacket_validation_tool as vt
    requirements = {r["validation_id"]: r for r in vt.review_prepare_validation_requirements(contract)}
    results = vt.review_prepare_validation_result_records(completion)
    statuses = {i["validation_id"]: i["status"] for i in items}
    pending = []
    for dep in dependencies(item, contract):
        if dep in requirements:
            if not any(command_evidence_exists(r, requirements[dep], contract, completion) for r in results):
                pending.append(dep)
        elif statuses.get(dep) != "passed":
            pending.append(dep)
    return pending


def dependency_evidence(item, contract, completion, items):
    """Bind new human conclusions to the evidence they actually aggregate."""
    from tools import workpacket_validation_tool as vt
    requirements = {r["validation_id"]: r for r in vt.review_prepare_validation_requirements(contract)}
    records = vt.review_prepare_validation_result_records(completion)
    manual = {i["validation_id"]: i.get("evidence_SHA256") for i in items}
    return {dep: (next((r.get("validation_result_SHA256") for r in records
                       if command_evidence_exists(r, requirements[dep], contract, completion)), None)
                  if dep in requirements else manual.get(dep)) for dep in dependencies(item, contract)}


def command_evidence_exists(result, requirement, contract, completion):
    """Failed command outcomes can inform human debt classification, never pass review."""
    from tools import workpacket_validation_tool as vt
    if vt.review_prepare_validation_result_matches_requirement(result, requirement, acceptance_contract=contract):
        return True
    authority = result.get("review_prepare_validation_authority") or {}
    binding = authority.get("pre_review_binding") or {}
    command = result.get("command") or {}
    return (
        result.get("validation_result_SHA256") == vt._validation_result_payload_digest(result)
        and binding.get("run_id") == completion.get("run_id")
        and binding.get("validation_contract_SHA256") == mv.digest(contract)
        and all(binding.get(key) == contract.get(key) for key in ("ticket_id", "ticket_spec_SHA256", "work_packet_id", "work_packet_SHA256"))
        and command.get("source_command") == requirement["source_command"]
        and command.get("validation_id") == requirement["validation_id"]
        and vt._public_command_matches_requirement_authority(command, requirement)
        and ((result.get("process_started") is True and type(result.get("exit_code")) is int)
             or (result.get("process_started") is False and result.get("disposition") in {"blocked", "failed"}
                 and result.get("error_code") in {
                     vt.WORKPACKET_VALIDATION_RUNTIME_UNAVAILABLE,
                     vt.WORKPACKET_VALIDATION_COMMAND_POLICY_DENIED,
                     vt.WORKPACKET_VALIDATION_SCRIPT_IDENTITY_DRIFT,
                 }))
    )


def capabilities(projection, completion, contract):
    """Resolve plans without launching, rematerializing, or granting consent."""
    from pathlib import Path
    from .workflow import ticket_architect_bridge as bridge
    from .work_packet import WorkPacketCompilationResult
    from tools import workpacket_validation_tool as vt
    from tools.governed_workpacket_file_guard import WorkPacketFileAuthority
    from tools.pre_review_validation_commands import extend_specs
    from . import product_runtime as pr
    workspace = Path(str(completion.get("kanban_task_workspace_path") or ""))
    manifest, reference = pr._governed_autonomy_materialization_manifest(workspace)
    rematerialization = not (workspace.is_absolute() and workspace.is_dir() and manifest and reference and reference.get("available"))
    canonical = False
    if rematerialization:
        source_ref = pr._completion_durable_source_authority_reference(projection, completion)
        if source_ref is None:
            from .command_validation_context import canonical_source
            source = canonical_source(projection, completion)
            workspace = Path(source["source_root"])
            rematerialization = False
            canonical = True
        else:
            source = pr._load_governed_source_authority_from_reference(source_ref, projection=projection, run_id=completion["run_id"])
            workspace = Path(source["snapshot_root"])
    packet = WorkPacketCompilationResult.model_validate(
        bridge.load_generation_record(ticket_id=projection["ticket_id"])["work_packet_compilation_result"]
    ).work_packet
    authority = WorkPacketFileAuthority(
        **{k: projection[k] for k in ("ticket_id", "ticket_spec_SHA256", "work_packet_id", "work_packet_SHA256", "projection_SHA256")},
        allowed_paths=tuple(packet.repository_scope.allowed_paths), forbidden_paths=tuple(packet.repository_scope.forbidden_paths),
        workspace_root=workspace, resolved_workspace_root=workspace.resolve(),
    )
    specs = extend_specs(authority, packet, vt.build_governed_validation_command_specs(authority, packet))
    missing = [r["validation_id"] for r in vt.review_prepare_validation_requirements(contract)
               if vt._review_prepare_validation_spec_for_requirement(specs, r) is None]
    return {"status": "command_authority_unavailable" if missing else "resolved",
            "governed_rematerialization_required": rematerialization,
            "plan_context": "canonical_repository" if canonical else "immutable_source_snapshot_preview" if rematerialization else "terminal_workspace",
            "missing_validation_ids": missing, "commands": [{**vt._public_command(s),
                "execution_plan": [vt._public_plan_step(step) for step in vt._command_plan(s)]} for s in specs]}


def inspect():
    from . import product_runtime as pr
    from tools import workpacket_validation_tool as vt
    p = pr._load_current_projection_record()
    pr._validate_execution_start_authority(p)
    c = pr._current_review_round_completion_source_raw(p)
    if c.get("blocker_code") or not pr._completion_binds_current_terminal_run(p, c):
        raise ValueError("command validation requires the current terminal run")
    contract = pr._acceptance_contract_for_review_projection(p)
    zero = pr.resolve_zero_change_authority(p, c)
    if not pr._review_prepare_eligible_result(c, contract, zero_change_authority=zero):
        raise ValueError("candidate/zero-change authority must be resolved first")
    binding = identity(p, c, contract)
    effective = enrich(p, c, contract)
    requirements = vt.review_prepare_validation_requirements(contract)
    if not requirements:
        raise ValueError("no required command validations")
    items = mv.inspect(contract, effective)
    if any(i["status"] == "failed" for i in items):
        raise ValueError("failed manual validation requires governed resolution")
    passed = vt.review_prepare_validation_contract_satisfied(effective, contract)
    results = vt.review_prepare_validation_result_records(effective)
    complete = all(any(command_evidence_exists(r, req, contract, effective) for r in results) for req in requirements)
    return {"binding": binding, "next_action_id": action_id(p["ticket_id"]),
            "required_human_authorization_text": consent(binding),
            "command_validation_complete": complete,
            "command_validation_passed": passed,
            "command_capability": capabilities(p, c, contract),
            "requirements": [vt.review_prepare_validation_requirement_public(r) for r in requirements],
            "validation_command_results": list(vt.review_prepare_validation_result_records(effective)),
            "read_only": True, "review_preparation_recorded": False}


@serialized
def execute(*, binding, human_authorization_text):
    from . import product_runtime as pr
    from tools import workpacket_validation_tool as vt
    context = inspect()
    if digest(binding) != digest(context["binding"]) or human_authorization_text != consent(context["binding"]):
        raise ValueError("command validation binding/human authorization mismatch")
    if context["command_capability"]["status"] == "command_authority_unavailable":
        raise ValueError("approved validation command specs unavailable: " + ", ".join(context["command_capability"]["missing_validation_ids"]))
    workflow = pr.build_workflow_control_snapshot()
    if (workflow.get("current_ticket_id") != binding["ticket_id"] or workflow.get("remaining_blockers")
            or workflow.get("active_execution_count") != 0 or workflow.get("pending_ticket_approval_count") != 0
            or workflow.get("recovery_state") != "not_required"
            or workflow.get("workflow_status") not in {"execution_completed", "execution_completed_pending_manual_validation"}):
        raise ValueError("command validation is not available in the current lifecycle")
    prior = load(binding)
    if prior is not None:
        return {"success": True, "idempotent_replay": True, "record": prior, "review_preparation_recorded": False}
    p = pr._load_current_projection_record()
    c = pr._current_review_round_completion_source_raw(p)
    contract = pr._acceptance_contract_for_review_projection(p)
    if binding.get("canonical_validation_source"):
        from .command_validation_context import execution_context
        execution = execution_context(p, binding)
    else:
        execution = pr._review_prepare_validation_context(p, c)
    result = vt.run_review_prepare_validation_commands(
        projection=p, completion=c, acceptance_contract=contract,
        worker_env=execution["worker_env"], validation_context=execution["validation_context"],
        requested_project_id=binding["project_id"], requested_ticket_id=binding["ticket_id"],
        requested_next_action_id=action_id(binding["ticket_id"]), pre_review_binding=binding,
    )
    if result.get("review_prepare_validation_authority") is None:
        raise ValueError(result.get("failure_detail") or "command authority unavailable")
    # Revalidate current authority after execution, before publishing evidence.
    if inspect()["binding"] != binding:
        raise ValueError("command validation authority changed during execution")
    record = {"policy_id": POLICY, "binding": binding, "human_authorization_text": human_authorization_text, "validation": result}
    record["record_SHA256"] = digest(record)
    if len(json.dumps(record).encode()) > MAX_BYTES:
        raise ValueError("command validation result exceeds persistence bound")
    from .zero_change_decision import persist
    persist(path_for(binding), record)
    load(binding)
    return {"success": True, "idempotent_replay": False, "record": record, "review_preparation_recorded": False}


def overlay(projection, completion, contract, items):
    from tools import workpacket_validation_tool as vt
    requirements = vt.review_prepare_validation_requirements(contract)
    if not requirements:
        return {}
    passed = vt.review_prepare_validation_contract_satisfied(completion, contract)
    results = vt.review_prepare_validation_result_records(completion)
    complete = all(any(command_evidence_exists(r, req, contract, completion) for r in results) for req in requirements)
    independent = [i["validation_id"] for i in items if i["status"] == "pending" and not dependencies(i, contract)]
    pending = [i["validation_id"] for i in items if i["status"] == "pending"]
    phase = ("manual_validation_preliminary_pending" if independent else "command_validation_pending") if not complete else ("manual_validation_final_pending" if pending else "command_validation_complete")
    result = {"validation_lifecycle_phase": phase, "command_validation_complete": complete,
              "command_validation_passed": passed,
              "preliminary_manual_validation_ids": independent, "pending_manual_validation_ids": pending}
    if not passed:
        result.update(validation_contract_satisfied=False, reviewable_result=False,
                      review_state="blocked_pending_contract_validation")
    if not complete and not any(i["status"] == "failed" for i in items):
        try:
            context = inspect()
        except (ValueError, OSError, KeyError) as exc:
            # Legacy incomplete authority cannot authorize this new boundary.
            # Preserve independent manual evidence and the existing review gate.
            result.update(command_validation_available=False,
                          command_validation_blocker=str(exc)[:300])
            return result
        action = {"id": context["next_action_id"], "target_ticket_id": projection["ticket_id"],
                  "tool": "prepare_current_ticket_review", "operation": "run_commands",
                  "binding": context["binding"], "required_human_authorization_text": context["required_human_authorization_text"],
                  "label": "Authorize governed command validation before final human evidence.",
                  "required_human_action": "command_validation_authorization"}
        result["command_validation_action"] = action
        result["command_validation_available"] = context["command_capability"]["status"] != "command_authority_unavailable"
        result["alternative_actions"] = [action]
        if not independent:
            result.update(next_action=action, validation_contract_satisfied=False,
                          reviewable_result=False, review_state="blocked_pending_contract_validation")
    return result


def public(result):
    """Keep tool responses bounded; complete signed evidence remains durable."""
    def bounded_result(r):
        command = r.get("command") or {}
        return {**{key: r.get(key) for key in (
            "success", "validation_result_SHA256", "review_prepare_validation_authority_SHA256",
            "process_started", "exit_code", "disposition", "failure_reason", "error_code",
        )}, "validation_id": command.get("validation_id"), "command_id": command.get("command_id"),
                "command_authority_SHA256": command.get("command_authority_SHA256"),
                "execution_plan_SHA256": command.get("execution_plan_SHA256"),
                "error_detail": str(r.get("error_detail") or r.get("error") or "")[:600],
                "stdout_excerpt": str(r.get("stdout") or "")[:1200],
                "stderr_excerpt": str(r.get("stderr") or "")[:1200]}
    projected = dict(result)
    if "record" in result:
        record = result["record"]
        validation = record["validation"]
        projected["record"] = {"binding": record["binding"], "record_SHA256": record["record_SHA256"],
            "source_record_path": str(path_for(record["binding"])),
            "validation": {**{k: validation.get(k) for k in (
                "validation_executed", "validation_complete", "validation_passed", "failure_detail",
                "review_prepare_validation_authority_SHA256",
            )}, "validation_command_results": [bounded_result(r) for r in validation["validation_command_results"]]}}
    if "validation_command_results" in result:
        projected["validation_command_results"] = [bounded_result(r) for r in result["validation_command_results"]]
    return projected
