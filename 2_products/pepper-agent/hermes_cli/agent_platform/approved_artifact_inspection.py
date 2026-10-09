"""Exact, bounded reads through the existing approval artifact boundary."""

import hashlib


def inspect(*, ticket_id, section_id, expected_binding=None, chunk_index=None, max_chars=None):
    from . import product_runtime as pr
    from .workflow import ticket_architect_bridge as bridge
    from .work_packet.compiler import _source_ticket_digest

    if section_id not in {"ticket_spec", "validation_steps"}:
        raise ValueError("current approved inspection supports ticket_spec or validation_steps")
    # Never resolve a caller-supplied filesystem path or fall back to older revisions.
    ticket_id = bridge._safe_ticket_id(ticket_id)
    generation = bridge.load_generation_record(ticket_id=ticket_id)
    if generation is None:
        raise ValueError("current generated artifact unavailable")
    current = pr._current_incomplete_generation_record_from_records()
    if current is None or current.get("bridge_SHA256") != generation["bridge_SHA256"]:
        raise ValueError("artifact is not the current governed generation")
    decision = bridge.load_approval_decision_record(ticket_id=ticket_id, generation_record=generation)
    if decision is None or decision.get("decision") != "approve":
        raise ValueError("current generation requires an approved decision")
    # Validate embedded identities too; returning the stored object avoids model
    # serialization/default insertion or projection-based reconstruction.
    bridge._validate_historical_generation_record(generation)
    publication = generation["ticket_publication_result"]["publication"]
    approved_publication = decision["ticket_publication_result"]["publication"]
    body = publication["canonical_ticket"]
    packet = generation["work_packet_compilation_result"]["work_packet"]
    if (body != generation["ticket_spec"]
            or body != approved_publication["canonical_ticket"]
            or body != decision["ticket_approval_record"]["approved_ticket"]
            or body != packet["source_ticket"]
            or _source_ticket_digest(bridge.TicketSpec.model_validate(body)) != generation["ticket_spec_SHA256"]
            or publication["publication_id"] != packet["publication_id"]
            or publication["artifact_SHA256"] != packet["publication_artifact_SHA256"]
            or publication["revision"] != packet["publication_revision"]):
        raise ValueError("approved artifact identity mismatch")
    binding = {key: generation[key] for key in (
        "project_id", "ticket_id", "ticket_spec_SHA256", "work_packet_id", "work_packet_SHA256", "bridge_SHA256")}
    binding.update(revision=f"R{publication['revision']:04d}",
                   publication_id=publication["publication_id"],
                   publication_artifact_SHA256=publication["artifact_SHA256"],
                   approval_publication_SHA256=decision["approval_publication_SHA256"],
                   approval_publication_id=approved_publication["publication_id"],
                   approval_SHA256=decision["ticket_approval_record"]["approval_SHA256"])
    if expected_binding is not None and expected_binding != binding:
        raise ValueError("requested current approved artifact binding mismatch")
    section = body if section_id == "ticket_spec" else body["validation_steps"]
    serialized = pr._serialized_artifact_section_body(section)
    size = pr._bounded_artifact_section_chars(max_chars)
    index = 0 if chunk_index is None else chunk_index
    count = max(1, (len(serialized) + size - 1) // size)
    if type(index) is not int or not 0 <= index < count:
        raise ValueError("artifact section chunk is out of range")
    chunked = count > 1 or chunk_index is not None
    # Revalidate current authority after assembling the response; no lock files,
    # repair operations, counters, or workflow transitions are needed for a read.
    if (bridge.load_generation_record(ticket_id=ticket_id) != generation
            or bridge.load_approval_decision_record(ticket_id=ticket_id, generation_record=generation) != decision
            or pr._current_incomplete_generation_record_from_records() != current):
        raise ValueError("current approved authority changed during inspection")
    return {
        "read_only": True, "validated": True, "inspection_status": "available",
        "authority_scope": "current_approved", "artifact_type": "TicketSpec",
        "section_id": section_id, "artifact_binding": binding,
        "source_authority": "pepper-ticket-architect-bridge-authority",
        "exact_body": serialized[index * size:(index + 1) * size] if chunked else section,
        "exact_body_format": "canonical_json_chunk" if chunked else "json",
        "exact_body_serialized_SHA256": hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
        "pagination": {"chunked": chunked, "chunk_index": index, "total_chunks": count,
                       "chunk_size_chars": size, "serialized_length_chars": len(serialized),
                       "next_chunk_index": index + 1 if index + 1 < count else None},
        "command_execution_authorized": False, "revision_authorized": False,
        "auto_approval": False, "Git_mutation": False,
    }
