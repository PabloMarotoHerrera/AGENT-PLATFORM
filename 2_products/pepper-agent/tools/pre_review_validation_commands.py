"""Bounded context adapters for approved legacy WorkPacket commands.

Only the separately authorized pre-review boundary uses these adapters. They
do not grant worker execution authority or change the published WorkPacket.
"""

from pathlib import Path
import shlex
import shutil

PRODUCT = "2_products/pepper-agent"
POLICY = "pepper-pre-review-approved-command-context-v1"


def extend_specs(authority, packet, existing):
    from tools import workpacket_validation_tool as vt

    specs = list(existing)
    covered = {s.validation_id for s in specs if s.acceptance_authorized}
    for index, step in enumerate(packet.validation_steps, 1):
        if step.validation_id in covered or not step.required or not step.command or step.command_authority is not None:
            continue
        # A compiled, digest-validated approved step is mandatory. This adapter
        # supplies execution context under separate human consent, not content.
        if not step.step_SHA256:
            continue
        source = vt._step_command(step)
        plan = wrapper_plan(authority, source) or package_plan(authority, source)
        if not plan:
            continue
        kind = "repository_test_wrapper" if plan[0].get("repository_test_wrapper") else "package_script"
        command_authority = {"policy_id": POLICY, "ticket_spec_SHA256": authority.ticket_spec_SHA256,
                             "work_packet_SHA256": authority.work_packet_SHA256, "step_SHA256": step.step_SHA256,
                             "source_command": source, "plan": plan}
        command_sha = vt._digest_payload(POLICY, command_authority)
        specs.append(vt.GovernedValidationCommandSpec(
            command_id="", validation_id=step.validation_id, source=POLICY, source_command=source,
            effective_argv=tuple(plan[0]["effective_argv"]), working_directory=plan[0]["working_directory"],
            timeout_seconds=1800, expected_exit_codes=vt._step_expected_exit_codes(step),
            runtime_available=not any(p.get("runtime_unavailable_reason") for p in plan),
            runtime_unavailable_reason=next((p["runtime_unavailable_reason"] for p in plan if p.get("runtime_unavailable_reason")), None),
            execution_plan=tuple(plan), command_authority_kind="explicit_human_pre_review_command",
            command_authority_id=f"PRE-REVIEW-{step.validation_id}", command_authority_SHA256=command_sha,
            ticket_spec_SHA256=authority.ticket_spec_SHA256, work_packet_id=authority.work_packet_id,
            work_packet_SHA256=authority.work_packet_SHA256, work_packet_validation_step_SHA256=step.step_SHA256,
            command_family=kind,
        ))
    return vt._finalize_command_specs(tuple(specs))


def contained_file(root, relative):
    path = root / relative
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(root.resolve(strict=True))
    except (ValueError, OSError):
        return None
    return resolved if resolved.is_file() else None


def wrapper_plan(authority, source):
    from tools import workpacket_validation_tool as vt
    try:
        tokens = tuple(shlex.split(source))
    except ValueError:
        return None
    if not tokens or tokens[0] != "scripts/run_tests.sh" or not 2 <= len(tokens) <= 65:
        return None
    # Only explicit test paths: no shell operators, pytest plugins, flags,
    # injected modules, response files, arbitrary executables or inline code.
    if not vt._package_command_tokens_shell_safe(tokens):
        return None
    root = Path(authority.resolved_workspace_root)
    tests = tokens[1:]
    missing = []
    for token in tests:
        relative = vt._safe_relative_command_path(token)
        if relative is None or not relative.startswith("tests/") or not relative.endswith(".py"):
            return None
        if not vt._path_is_authorized(authority, f"{PRODUCT}/{relative}"):
            return None
        if contained_file(root, f"{PRODUCT}/{relative}") is None:
            missing.append(relative)
    runner_files = [contained_file(root, f"{PRODUCT}/scripts/{name}") for name in ("run_tests.sh", "run_tests_parallel.py")]
    if any(p is None for p in runner_files):
        return None
    bash = shutil.which("bash")
    if not bash:
        return None
    return [{"effective_argv": (str(Path(bash).resolve()), str(runner_files[0]), *tests),
             "working_directory": str(root / PRODUCT), "timeout_seconds": 1800,
             "expected_exit_codes": [0], "repository_test_wrapper": True,
             "runtime_unavailable_reason": ("required test paths unavailable: " + ", ".join(missing)) if missing else None,
             "wrapper_files": {str(p): vt._file_sha256(p) for p in runner_files}}]


def package_plan(authority, source):
    from tools import workpacket_validation_tool as vt
    segments = vt._package_script_segments(source)
    if not segments or len(segments) > 2:
        return None
    requests = [vt._package_script_request(s) for s in segments]
    if any(r is None or r[0] not in {"test", "typecheck", "build"} for r in requests):
        return None
    root = Path(authority.resolved_workspace_root)
    candidates = []
    for _name, relative in vt._PACKAGE_TARGETS:
        if not vt._package_path_in_workpacket_scope(authority, relative):
            continue
        package = root / relative
        if contained_file(root, f"{relative}/package.json") is None:
            continue
        plan = []
        for script_name, args in requests:
            script = vt._package_script(package, script_name)
            if not script:
                break
            # Preserve product-relative selectors while executing inside the
            # unique authorized package that owns them (e.g. web/src -> src).
            prefix = relative.removeprefix(PRODUCT + "/") + "/"
            args = tuple(a[len(prefix):] if a.startswith(prefix) else a for a in args)
            steps = vt._package_script_execution_plan(
                authority, root, relative, package, script_name=script_name, script=script,
                extra_args=args, expected_exit_codes=(0,), node_path=vt._resolve_node_executable(),
                timeout_seconds=1800,
            )
            if not steps:
                break
            plan.extend(steps)
        else:
            candidates.append(plan)
    # No guessing across multiple valid packages.
    return candidates[0] if len(candidates) == 1 else None
