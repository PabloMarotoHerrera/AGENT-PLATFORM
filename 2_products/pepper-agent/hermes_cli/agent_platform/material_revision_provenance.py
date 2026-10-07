"""Bounded, read-only projection of persisted revision evidence, never contracts.

The generation envelope is the atomic transition: its bridge digest binds the
accepted authority, publication, TicketSpec, WorkPacket and creation timestamp.
The append-only history is an additional source for superseded generations;
it is not required to repair or manufacture a current generation's authority.
"""

from datetime import datetime
import hashlib
import json
from pathlib import Path

from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge

MAX_BYTES = 32 * 1024 * 1024
MAX_ENTRIES = 128


def validate_record(record: dict) -> dict:
    """Validate the self-contained envelope without regenerating a contract."""
    bridge._validate_historical_generation_record(record)
    target = bridge._historical_target_from_record(record)
    authority = bridge._validate_material_revision_authority(
        record["revision_authority"], target=target,
    )
    publication = bridge._publication_from_generation_record(record)
    packet = bridge.WorkPacketCompilationResult.model_validate(
        record["work_packet_compilation_result"]
    ).work_packet
    checks = (
        record["revision_authority_SHA256"] == authority["revision_authority_SHA256"],
        record["revision_sequence"] == authority["new_publication_revision"],
        publication.revision == authority["new_publication_revision"],
        publication.supersedes_publication_id == authority["previous_publication_id"],
        publication.ticket_id == record["ticket_id"],
        publication.canonical_ticket == packet.source_ticket,
        packet.publication_revision == publication.revision,
        packet.source_ticket_SHA256 == record["ticket_spec_SHA256"],
    )
    if not all(checks):
        raise ValueError("revision/publication/TicketSpec linkage mismatch")
    text = authority["human_authorization_text"]
    if bridge._validate_revision_authorization_text(
        text, ticket_id=record["ticket_id"],
        revise_next_action_id=target.revise_next_action_id,
    ) != text:
        raise ValueError("authorization text is not the accepted canonical text")
    if datetime.fromisoformat(record["created_at"].replace("Z", "+00:00")).tzinfo is None:
        raise ValueError("transition timestamp has no timezone")
    return {
        "ticket_id": record["ticket_id"],
        "source_revision": authority["previous_publication_revision"],
        "target_revision": publication.revision,
        "authority_sha256": authority["revision_authority_SHA256"],
        "authorization_evidence_identity": authority["revision_authority_SHA256"],
        "authorization_text": text,
        "authorization_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "authorizer_id": authority["authorizer_id"],
        "revision_action_id": authority["revision_action_id"],
        "revision_reason": authority.get("revision_reason"),
        "source_generation_sha256": authority["previous_bridge_SHA256"],
        "source_publication_id": authority["previous_publication_id"],
        "source_ticket_spec_sha256": authority["previous_ticket_spec_SHA256"],
        "publication_id": publication.publication_id,
        "publication_artifact_sha256": publication.artifact_SHA256,
        "publication_canonical_ticket_sha256": publication.canonical_ticket_SHA256,
        "ticket_spec_sha256": record["ticket_spec_SHA256"],
        "work_packet_id": record["work_packet_id"],
        "work_packet_sha256": record["work_packet_SHA256"],
        "transition_timestamp": record["created_at"],
        "record_integrity_sha256": record["bridge_SHA256"],
    }


def _read(path: Path) -> str | None:
    try:
        with path.open("rb") as handle:
            raw = handle.read(MAX_BYTES + 1)
    except FileNotFoundError:
        return None
    if len(raw) > MAX_BYTES:
        raise ValueError("provenance source exceeds inspection bound")
    return raw.decode("utf-8")


def inspect(*, ticket_id: str, revision: int | None = None,
            expected_authority_sha256: str | None = None) -> dict:
    """Inspect only canonical persisted records; expected SHA is a comparison.

    No validation-step wording is read. An absent authority cannot be recovered
    from an expected value. Identical replay records collapse by bridge digest;
    competing envelopes for one publication revision fail closed.
    """
    result = {
        "ticket_id": ticket_id, "target_revision": revision,
        "status": "MISSING", "classification": "MATERIAL_REVISION_PROVENANCE_MISSING",
        "read_only": True, "auto_validation": False,
        "human_attestation_required": True, "validation_attested": False,
    }
    try:
        if not isinstance(ticket_id, str) or len(ticket_id) > 128:
            result["ticket_id"] = None
            raise ValueError("ticket id exceeds inspection bound")
        ticket_id = bridge._safe_ticket_id(ticket_id)
        if revision is not None and (type(revision) is not int or revision < 1):
            raise ValueError("revision must be a positive integer")
        if expected_authority_sha256 is not None:
            bridge._safe_digest(expected_authority_sha256)
        candidates = []
        current_path = bridge.generation_record_path_for_ticket(ticket_id)
        raw = _read(current_path)
        current = json.loads(raw) if raw is not None else None
        if current is not None:
            bridge._validate_historical_generation_record(current)
            if current["ticket_id"] != ticket_id:
                raise ValueError("current generation ticket mismatch")
            if revision is None:
                revision = bridge._publication_from_generation_record(current).revision
                result["target_revision"] = revision
            candidates.append((current, "generation", current["bridge_SHA256"]))
        for path in (
            bridge.current_ticket_material_revision_history_path_for_ticket(ticket_id),
            bridge.rejected_successor_revision_history_path_for_ticket(ticket_id),
        ):
            raw = _read(path)
            lines = raw.splitlines() if raw else []
            if len(lines) > MAX_ENTRIES:
                raise ValueError("provenance history exceeds inspection bound")
            for line in lines:
                entry = json.loads(line)
                if not isinstance(entry, dict):
                    raise ValueError("history entry is not an object")
                if entry.get("revision_SHA256") != bridge._revision_history_record_digest(entry):
                    raise ValueError("history integrity mismatch")
                if entry.get("ticket_id") != ticket_id:
                    raise ValueError("history ticket mismatch")
                new = entry["new_generation_record"]
                # Both history formats bind the full resulting envelope.
                if new["bridge_SHA256"] != entry["revised_generation_bridge_SHA256"]:
                    raise ValueError("history generation reference mismatch")
                bridge._validate_historical_generation_record(new)
                if bridge._publication_from_generation_record(new).revision == revision:
                    authority = new["revision_authority"]
                    if entry["human_authorization_text"] != authority["human_authorization_text"]:
                        raise ValueError("history authorization mismatch")
                    old = entry.get("historical_current_generation_record", entry.get("historical_rejected_generation_record"))
                    bridge._validate_historical_generation_record(old)
                    bridge._validate_material_revision_generation(
                        rejected_generation=old, revised_generation=new,
                        revision_authority=authority,
                    )
                    if old["ticket_id"] != ticket_id or any(
                        authority[key] != old[field] for key, field in (
                            ("previous_bridge_SHA256", "bridge_SHA256"),
                            ("previous_ticket_spec_SHA256", "ticket_spec_SHA256"),
                            ("previous_work_packet_id", "work_packet_id"),
                            ("previous_work_packet_SHA256", "work_packet_SHA256"),
                        )
                    ):
                        raise ValueError("history predecessor mismatch")
                candidates.append((new, path.name, entry["revision_SHA256"]))
        matching = [(g, source, sha) for g, source, sha in candidates
                    if bridge._publication_from_generation_record(g).revision == revision]
        if len({g["bridge_SHA256"] for g, _, _ in matching}) > 1:
            raise ValueError("ambiguous revision envelopes")
        if not matching or matching[0][0].get("revision_authority") is None:
            return result
        record = matching[0][0]
        if record["ticket_id"] != ticket_id:
            raise ValueError("revision ticket mismatch")
        projection = validate_record(record)
        result.update(projection)
        result["source_records"] = [
            {"kind": source, "sha256": sha}
            for source, sha in sorted({(source, sha) for _, source, sha in matching})
        ]
        if expected_authority_sha256 is not None and projection["authority_sha256"] != expected_authority_sha256:
            result.update(status="AUTHORITY_MISMATCH", classification="MATERIAL_REVISION_AUTHORITY_MISMATCH")
        else:
            result.update(status="PROVEN", classification="PATH_A_EXISTING_PROVENANCE")
        return result
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        # Do not return partial evidence, contract text or unrelated state on error.
        return {**{k: result[k] for k in (
            "ticket_id", "target_revision", "read_only", "auto_validation",
            "human_attestation_required", "validation_attested",
        )}, "status": "INCONSISTENT", "classification": "MATERIAL_REVISION_PROVENANCE_INCONSISTENT"}
