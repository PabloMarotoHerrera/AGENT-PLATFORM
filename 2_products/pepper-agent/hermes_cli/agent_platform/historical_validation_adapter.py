"""Passive, frozen projections of supplied historical schema-1 validation views.

No historical modules are imported. Full signed document/digest verification and
runtime guard qualification remain with their existing owners. The byte digest
here identifies supplied bytes, never replaces the historical signed digest.
C91 textual interpretation is copied as a named frozen policy and is explicitly
ambiguous as a declaration of intended dependencies. No projection is authority.
"""

import json
import re
from typing import Annotated, Literal

from pydantic import Field

from .harness.contracts import ContentRef, ContractRef, Identifier, Observational, _Contract
from .harness.validation import MAX_JSON_BYTES, _unique_object, sha256_bytes
from .harness.validation_dag import (AcceptanceCriterion, EvidenceDependency,
    ValidationBoundary, ValidationContext, ValidationDAG, ValidationRequirement)
from .harness.validation_dag_verifier import POLICY

COMPATIBILITY_POLICY = ContractRef(contract_id="pepper-historical-validation-projection", version=1)
MappingStatus = Literal["EXACT_COMPATIBLE", "PARTIALLY_OBSERVABLE", "AMBIGUOUS_HISTORICAL_SEMANTICS",
                        "UNSUPPORTED_HISTORICAL_SCHEMA", "VERSION_CONFLICT", "INVALID_HISTORICAL_INPUT"]


class HistoricalValidationProjection(_Contract):
    source: ContentRef
    original_schema: ContractRef
    compatibility_policy: ContractRef = COMPATIBILITY_POLICY
    mapping: MappingStatus
    graph: ValidationDAG | None
    graph_identity: ContentRef | None
    diagnostics: Annotated[tuple[Identifier, ...], Field(max_length=128)]
    historical_digest_verified: Literal[False] = False
    observational: Observational = True
    grants_authority: Literal[False] = False


def _dependencies(item, steps):
    """Frozen C91 dependencies() interpretation, not a new semantic rule."""
    text = " ".join(str(item.get(k) or "") for k in ("description", "expected_result"))
    ids = {s["validation_id"] for s in steps}
    refs = set(re.findall(r"\b[A-Z]+\d+\b", text)) & ids
    for prefix, first, last in re.findall(r"\b([A-Z]+)(\d+)\s*[-\u2013]\s*(?:[A-Z]+)?(\d+)\b", text):
        refs.update(i for i in ids if re.fullmatch(prefix + r"\d+", i) and int(first) <= int(i[len(prefix):]) <= int(last))
    if re.search(r"regression\s+failures|known[- ]debt|command\s+results", text, re.I):
        refs.update(s["validation_id"] for s in steps if s.get("kind") == "command" and s.get("required"))
    return tuple(sorted(refs - {item["validation_id"]}))


def project_historical(raw: bytes, *, source: ContentRef, original_schema: ContractRef,
                       context: ValidationContext) -> HistoricalValidationProjection:
    """Only injected bytes; no locator/discovery/rewrite or executable imports.

    TicketSpec/WorkPacket v1 validation-step subsets are observable, not complete
    model/digest validation. All such graphs block acceptance until future
    independently authorized qualification. Order and prose remain in source.
    """
    source = ContentRef.model_validate(source)
    original_schema = ContractRef.model_validate(original_schema)
    context = ValidationContext.model_validate(context)

    def outcome(mapping, diagnostics, graph=None):
        return HistoricalValidationProjection(source=source, original_schema=original_schema,
            mapping=mapping, graph=graph, graph_identity=graph.identity() if graph else None,
            diagnostics=tuple(sorted(diagnostics)))

    if type(raw) is not bytes or len(raw) > MAX_JSON_BYTES:
        return outcome("INVALID_HISTORICAL_INPUT", ("invalid_transport",))
    if sha256_bytes(raw) != source.sha256:
        return outcome("INVALID_HISTORICAL_INPUT", ("source_digest_mismatch",))
    if original_schema.contract_id not in {"pepper-ticket-spec", "pepper-work-packet"} or original_schema.version != 1:
        return outcome("UNSUPPORTED_HISTORICAL_SCHEMA", ("unsupported_schema",))
    try:
        body = json.loads(raw, object_pairs_hook=_unique_object)
        if not isinstance(body, dict) or type(body.get("schema_version")) is not int:
            raise ValueError("missing schema")
        if body["schema_version"] != original_schema.version:
            return outcome("VERSION_CONFLICT", ("source_schema_version_conflict",))
        if body.get("ticket_id") != context.current_ticket:
            raise ValueError("source ticket mismatch")
        steps = body["validation_steps"]
        if not isinstance(steps, list) or not 1 <= len(steps) <= 32:
            raise ValueError("invalid steps")
        ids = []
        for ordinal, step in enumerate(steps, 1):
            if not isinstance(step, dict):
                raise ValueError("invalid step")
            name = step["validation_id"]
            ContractRef(contract_id=name, version=1)
            if name in ids or type(step.get("required")) is not bool:
                raise ValueError("ambiguous ID or requiredness")
            ids.append(name)
            if not all(isinstance(step.get(k), str) and 1 <= len(step[k]) <= 2000 for k in ("description", "expected_result")):
                raise ValueError("missing wording")
            command = step.get("command")
            if command is not None and (not isinstance(command, str) or not command.strip() or len(command) > 2000):
                raise ValueError("invalid command")
            if original_schema.contract_id == "pepper-work-packet":
                if step.get("ordinal") != ordinal or type(step.get("ordinal")) is not int or step.get("kind") != ("command" if command is not None else "manual"):
                    raise ValueError("invalid compiled ordinal/kind")
                if type(step.get("command_execution_authorized")) is not bool:
                    raise ValueError("missing authority declaration")
                if command is None and step["command_execution_authorized"]:
                    raise ValueError("manual command authority conflict")
                ContentRef(content_id="historical-step", sha256=step["step_SHA256"])
    except (ValueError, KeyError, TypeError, RecursionError):
        return outcome("INVALID_HISTORICAL_INPUT", ("invalid_validation_view",))
    # Copy only; input/source bytes and signed structures are never changed.
    normalized = [{**s, "kind": "command" if s.get("command") is not None else "manual"} for s in steps]
    refs = {s["validation_id"]: ContractRef(contract_id=s["validation_id"], version=1) for s in normalized}
    boundaries, requirements, dependencies, criteria = [], [], [], []
    diagnostics = {"full_historical_schema_and_digest_qualification_external", "runtime_guards_not_projected"}
    ambiguous = False
    for s in normalized:
        name = s["validation_id"]
        boundary_ref = ContractRef(contract_id="historical-producer." + name, version=1)
        boundaries.append(ValidationBoundary(producer=boundary_ref, output=refs[name],
            kind="EXTERNAL" if s["kind"] == "command" else "HUMAN", provenance=source))
    for s in normalized:
        if not s["required"]:
            diagnostics.add("optional_validation_not_acceptance_requirement")
            continue
        name = s["validation_id"]
        inferred = _dependencies(s, normalized) if s["kind"] == "manual" else ()
        if inferred:
            ambiguous = True
            diagnostics.add("textual_dependencies_are_frozen_interpretation_not_signed_edges")
        # Own evidence is still necessary. An inferred aggregate is human-only,
        # never an automated rule that blesses failed upstream evidence.
        expected = (name, *inferred)
        conditions = {}
        for dep in expected:
            target = next(x for x in normalized if x["validation_id"] == dep)
            conditions[dep] = "RECORDED" if dep != name and target["kind"] == "command" else "PASSED"
        human = s["kind"] == "manual"
        criterion_ref = ContractRef(contract_id="criterion." + name, version=1)
        criteria.append(AcceptanceCriterion(criterion=criterion_ref,
            kind="FAILURE_CLASSIFICATION" if inferred else "HUMAN_ACCEPTANCE" if human else "ALL_PASSED",
            required_facts=tuple(sorted(set(conditions.values()))), authority_class="HUMAN" if human else "NONE",
            machine_evaluable=not human, human_decision_required=human))
        requirements.append(ValidationRequirement(requirement=refs[name], category="MANUAL" if human else "COMMAND",
            criterion=criterion_ref, expects=tuple(refs[x] for x in expected), context=context,
            human_authority=human, description=s["description"]))
        for dep in expected:
            dependencies.append(EvidenceDependency(dependency_id=name + ".requires." + dep,
                consumer=refs[name], producer=ContractRef(contract_id="historical-producer." + dep, version=1),
                evidence=refs[dep], expected_source=source, condition=conditions[dep]))
    mapping = "AMBIGUOUS_HISTORICAL_SEMANTICS" if ambiguous else "PARTIALLY_OBSERVABLE"
    # Too many historical edges are unsupported, never truncated into apparent parity.
    if len(dependencies) > 256:
        return outcome("INVALID_HISTORICAL_INPUT", ("projection_edge_bound",))
    graph = ValidationDAG(graph=ContractRef(contract_id="historical-validation-projection", version=1),
        policy=POLICY, requirements=tuple(requirements), producers=(), dependencies=tuple(dependencies),
        criteria=tuple(criteria), boundaries=tuple(boundaries), historical_mapping=mapping,
        historical_source=source, compatibility_policy=COMPATIBILITY_POLICY,
        unresolved_history=tuple(sorted(diagnostics)))
    return outcome(mapping, diagnostics, graph)
