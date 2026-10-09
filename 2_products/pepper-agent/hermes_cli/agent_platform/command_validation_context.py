"""Current-source validation context for terminal read-only/zero-change work.

No source is retroactively attributed to the worker run. Human consent binds a
separate fingerprint of the current canonical product source. Ordinary worker
and candidate validation retain their existing workspace rules.
"""

import hashlib
import os
from pathlib import Path

POLICY = "pepper-pre-review-canonical-source-validation-v1"
MAX_FILES = 30000
MAX_BYTES = 512 * 1024 * 1024


def canonical_source(projection, completion):
    from . import product_runtime as pr
    if pr._completion_durable_source_authority_reference(projection, completion) is not None:
        return None
    manifest, reference = pr._governed_autonomy_materialization_manifest(Path(str(completion.get("kanban_task_workspace_path") or "")))
    if manifest and reference and reference.get("available"):
        return None
    zero = pr.resolve_zero_change_authority(projection, completion)
    if zero.get("zero_change_result") is not True or not pr._review_prepare_eligible_result(
        completion, pr._acceptance_contract_for_review_projection(projection), zero_change_authority=zero,
    ):
        raise ValueError("canonical validation context requires explicit current zero-change authority")
    root = pr._agent_platform_repository_root().resolve(strict=True)
    return {"policy_id": POLICY, "source_root": str(root), **fingerprint(root)}


def fingerprint(root):
    from . import product_runtime as pr
    from .command_validation import digest
    rows = []
    total = 0
    source = root / "2_products/pepper-agent"
    if not source.is_dir():
        raise ValueError("canonical Pepper source unavailable")
    skip = pr._SCRATCH_SOURCE_SKIP_DIR_NAMES | {".codex", ".idea", ".vscode", "web_dist", "test-results", "playwright-report"}
    suffixes = {".py", ".sh", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".json", ".toml", ".yaml", ".yml", ".css", ".html", ".md", ".svg"}
    for current, dirs, names in os.walk(source):
        dirs[:] = sorted(d for d in dirs if d not in skip)
        for name in sorted(names):
            path = Path(current) / name
            if path.suffix not in suffixes or name.startswith(".env") or name in {"auth.json", "test_durations.json"}:
                continue
            resolved = path.resolve(strict=True)
            try:
                resolved.relative_to(root)
            except ValueError as exc:
                raise ValueError("canonical source escapes repository") from exc
            size = path.stat().st_size
            total += size
            if len(rows) >= MAX_FILES or total > MAX_BYTES:
                raise ValueError("canonical validation source exceeds bound")
            rows.append([path.relative_to(root).as_posix(), hashlib.sha256(path.read_bytes()).hexdigest()])
    return {"source_files_SHA256": digest(rows), "source_file_count": len(rows), "source_bytes": total}


def environment(projection, root):
    from .workflow import ticket_architect_bridge as bridge, work_packet_kanban_projection as wk
    from tools import governed_workpacket_file_guard as fg
    # File authority needs publication/approval/projection, not provider tokens
    # or worker dispatch. Do not manufacture a governed-worker identity.
    return {
        fg.WORKPACKET_ID_ENV: projection["work_packet_id"],
        fg.WORKPACKET_SHA256_ENV: projection["work_packet_SHA256"],
        fg.TICKET_SPEC_SHA256_ENV: projection["ticket_spec_SHA256"],
        fg.KANBAN_PROJECTION_SHA256_ENV: projection["projection_SHA256"],
        fg.GENERATION_RECORD_PATH_ENV: str(bridge.generation_record_path_for_ticket(projection["ticket_id"])),
        fg.APPROVAL_DECISION_RECORD_PATH_ENV: str(bridge.approval_decision_record_path_for_ticket(projection["ticket_id"])),
        fg.KANBAN_PROJECTION_RECORD_PATH_ENV: str(wk.kanban_projection_record_path_for_ticket(projection["ticket_id"])),
        "HERMES_KANBAN_WORKSPACE": str(root), "TERMINAL_CWD": str(root),
    }


def execution_context(projection, binding):
    source = binding["canonical_validation_source"]
    return {"worker_env": environment(projection, source["source_root"]),
            "validation_context": {"validation_origin": "pre_review_canonical_repository",
                                   "validation_workspace_policy_id": POLICY,
                                   "workspace_path": source["source_root"],
                                   "canonical_validation_source": source}}
