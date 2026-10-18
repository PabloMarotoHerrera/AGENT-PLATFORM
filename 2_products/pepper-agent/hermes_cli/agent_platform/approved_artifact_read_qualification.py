"""Invocation-local C93 read attestation, NOT a production authority issuer.

Only trusted isolated composition installs an owner. Original C93 loaders and
validators produce the private capture; no public input accepts a qualification,
issuer or ALLOW as a credential. Python/OS and original store custody are trusted;
this is not a sandbox against arbitrary code in this interpreter. All positive
evidence here is MECHANICAL_SYNTHETIC_ONLY; independent issuer proof is pending.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import threading
from typing import Literal
from pydantic import Field, model_validator

from .harness.contracts import (
    ActorRef, AuthorityCurrentness, AuthorityReference, ContentRef, ContractRef,
    Effect, Scope, StateDimension, StateSupport, WorkflowState, _Contract,
)
from .harness.admissibility import (
    AdmissionInput, ConsentStatus, PrerequisiteObservation, QualifiedEvaluation, evaluate,
)
from .harness.observation import CheckStatus, Observation, ObservationStatus, SourceRef, SourceKind
from .admissibility_projection import binding_identity, operation_policy
from .pre_review_catalog import product_catalog, product_operations
from .handler_correspondence import BindingStatus, inspect_correspondence


CAPABILITY = ContractRef(contract_id="O03.validation_steps", version=1)
TRANSITION = ContractRef(contract_id="O03.validation_steps.transition", version=1)
OWNER = ContractRef(contract_id="pepper-c93-read-qualification-v1", version=1)
LEGACY = ContractRef(contract_id="pepper-ticket-architect-bridge-p18-9-0-v1", version=1)
PREREQUISITES = frozenset(ContractRef(contract_id=n, version=1) for n in (
    "approved_artifact_inspection.inspect", "pepper-ticket-architect-bridge-p18-9-0-v1",
    "O03.validation_steps.legacy-guard-result"))
SOURCE_FILES = (
    "tools/pepper_workflow_tools.py", "tools/registry.py",
    "hermes_cli/agent_platform/approved_artifact_inspection.py",
    "hermes_cli/agent_platform/approved_artifact_read_qualification.py",
    "hermes_cli/agent_platform/approved_artifact_routing.py",
    "hermes_cli/agent_platform/workflow/ticket_architect_bridge.py",
    "hermes_cli/agent_platform/work_packet/compiler.py",
    "hermes_cli/agent_platform/product_runtime.py",
    "hermes_cli/agent_platform/command_validation_context.py",
    "hermes_cli/agent_platform/pre_review_catalog.py",
    "hermes_cli/agent_platform/handler_correspondence.py",
    "hermes_cli/agent_platform/admissibility_projection.py",
    "hermes_cli/agent_platform/harness/admissibility.py",
    "hermes_cli/agent_platform/harness/contracts.py",
    "hermes_cli/agent_platform/harness/observation.py",
    "hermes_cli/agent_platform/harness/validation.py",
)


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _content(name, value):
    return ContentRef(content_id=name, sha256=hashlib.sha256((name + "\0" + _json(value)).encode()).hexdigest())


def _data(value):
    """Copy plain request data without invoking arbitrary coercion/serialization."""
    if value is None or type(value) in (str, int, bool):
        return {"type": type(value).__name__, "value": value}
    if type(value) is float:
        _json(value)  # rejects nonfinite numbers
        return {"type": "float", "value": value}
    if type(value) in (list, tuple):
        return {"type": type(value).__name__, "value": [_data(v) for v in value]}
    if type(value) is dict and all(type(k) is str for k in value):
        return {"type": "dict", "value": {k: _data(v) for k, v in value.items()}}
    raise ValueError("C93 unsupported qualification request data")


def _execution_context():
    try:
        task = asyncio.current_task()
    except RuntimeError:
        task = None
    return os.getpid(), threading.get_ident(), task


class C93ReadQualification(_Contract):
    """Observational serialized evidence; construction never authenticates issuer."""
    capability: Literal["O03.validation_steps@1"] = "O03.validation_steps@1"
    transition: Literal["O03.validation_steps.transition@1"] = "O03.validation_steps.transition@1"
    effect: Literal["OBSERVE"] = "OBSERVE"
    owner_policy: ContractRef
    legacy_policy: ContractRef
    proof_level: Literal["MECHANICAL_SYNTHETIC_ONLY"] = "MECHANICAL_SYNTHETIC_ONLY"
    issuer_proof: Literal["TRUSTED_ISSUER_PROOF_PENDING"] = "TRUSTED_ISSUER_PROOF_PENDING"
    lifetime: Literal["ONE_INVOCATION_ONE_EVALUATION_ONE_RELEASE"] = "ONE_INVOCATION_ONE_EVALUATION_ONE_RELEASE"
    raw_bytes_provenance: Literal["NOT_CAPTURED"] = "NOT_CAPTURED"
    raw_argument_model: Literal["ORIGINAL_SIGNATURE_NONE_COLLAPSES_OMISSION_AND_NULL"] = "ORIGINAL_SIGNATURE_NONE_COLLAPSES_OMISSION_AND_NULL"
    invocation_binding: ContentRef
    project_id: str
    ticket_id: str
    revision: str
    publication_revision: int = Field(ge=1)
    work_packet_id: str
    scope: Scope
    read_principal: ActorRef
    original_actor: str
    original_reviewer: str
    original_decision: Literal["approve"]
    artifact_binding: ContentRef
    original_generation: ContentRef
    original_approval: ContentRef
    original_workflow: ContentRef
    request: ContentRef
    section: ContentRef
    serialized_section: ContentRef
    response: ContentRef
    effective_parameters: ContentRef
    implementation: ContentRef
    validator_sources: tuple[ContentRef, ...] = Field(min_length=1, max_length=32)
    handler_correspondence: ContentRef
    capture: ContentRef
    admission_input: ContentRef
    qualified_facts: tuple[str, ...] = Field(min_length=14, max_length=14)
    original_algorithms: tuple[str, ...] = Field(min_length=3, max_length=3)
    source_closure: Literal["BROAD_REQUIRED_NOT_OPERATIONALLY_QUALIFIED"] = "BROAD_REQUIRED_NOT_OPERATIONALLY_QUALIFIED"
    currentness_model: Literal["SEQUENTIAL_OBSERVED_NOT_ATOMIC_AT_DELIVERY"] = "SEQUENTIAL_OBSERVED_NOT_ATOMIC_AT_DELIVERY"
    grants_authority: Literal[False] = False
    authorizes_execution: Literal[False] = False

    @model_validator(mode="after")
    def _bindings(self):
        if self.owner_policy != OWNER or self.legacy_policy != LEGACY:
            raise ValueError("C93 qualification policy/version mismatch")
        if self.scope.project_id != self.project_id or self.scope.workflow_id != "c93-approved-artifact-read":
            raise ValueError("C93 qualification resource scope mismatch")
        if self.revision != f"R{self.publication_revision:04d}":
            raise ValueError("C93 qualification revision mismatch")
        if self.qualified_facts != tuple("F%02d" % i for i in range(1, 15)):
            raise ValueError("C93 incomplete preflight facts")
        return self


@dataclass(eq=False)
class _Invocation:
    seal: object
    context: tuple
    capture: dict
    input: AdmissionInput
    qualification: C93ReadQualification
    outcome: str
    used: bool = False


class C93ReadQualificationOwner:
    """Controlled mechanical proof coordinator; never accepts caller credentials.

    Source root and nonlive store custody are trusted composition inputs, not tool
    arguments. Fresh-process loaded-code custody remains a proof assumption, not
    something a disk hash authenticates. No production construction is installed.
    """

    def __init__(self, *, isolated_repository: Path, isolated_home: Path):
        self._context = _execution_context()
        self._root = Path(isolated_repository).resolve(strict=True)
        self._home = Path(isolated_home).resolve(strict=True)
        # Confinement is an isolated-composition check, NOT human authentication.
        if Path(os.environ.get("HERMES_HOME", "")).resolve() != self._home:
            raise ValueError("C93 explicit isolated HERMES_HOME required")
        loaded = Path(__file__).resolve().parents[4]
        if loaded != self._root:
            raise ValueError("C93 proof must use its loaded disposable source")
        self._seal = object()
        self._active = {}
        self._sequence = 0
        self._sources, self._implementation = self._source()
        self._observations = []

    @property
    def observations(self):
        """Immutable diagnostics only; no method accepts them back as credentials."""
        return tuple(self._observations)

    def _source(self):
        from .command_validation_context import fingerprint
        product = self._root / "2_products/pepper-agent"
        sources = tuple(ContentRef(content_id="source." + str(i), sha256=hashlib.sha256(
            (product / p).read_bytes()).hexdigest()) for i, p in enumerate(SOURCE_FILES))
        broad = fingerprint(self._root)
        return sources, _content("c93-implementation", {"files": [s.model_dump(mode="json") for s in sources],
            "broad": broad, "loaded_source_model": "CONTROLLED_ISOLATED_PROCESS_ASSUMPTION"})

    def _check_context(self):
        if _execution_context() != self._context:
            raise ValueError("C93 foreign thread task or process")
        if Path(os.environ.get("HERMES_HOME", "")).resolve() != self._home:
            raise ValueError("C93 resource context changed")
        if self._source() != (self._sources, self._implementation):
            raise ValueError("C93 implementation source drift")

    def _prepare(self, capture):
        self._check_context()
        if len(self._active) or len(self._observations) >= 128:
            raise ValueError("C93 recursive or bounded invocation exceeded")
        g, d, current, response, request = (capture[k] for k in ("generation", "decision", "current", "response", "request"))
        if request["section_id"] != "validation_steps":
            raise ValueError("C93 selected section mismatch")
        if current is None or current.get("bridge_SHA256") != g["bridge_SHA256"]:
            raise ValueError("C93 currentness unavailable")
        if d.get("decision") != "approve":
            raise ValueError("C93 original approval required")
        if request["ticket_id"] != g["ticket_id"] or response["artifact_binding"]["ticket_id"] != g["ticket_id"]:
            raise ValueError("C93 ticket binding mismatch")
        # Original validators have already run in C93. Bind their actual complete
        # capture, never replace their algorithms with the metadata checks here.
        tagged = {k: _data(v) for k, v in request.items()}
        request_ref = _content("c93-request", tagged)
        capture_ref = _content("c93-capture", capture)
        binding = response["artifact_binding"]
        actor = ActorRef(actor_id="c93-isolated-local-reader")
        scope = Scope(project_id=g["project_id"], workflow_id="c93-approved-artifact-read",
            resource_ids=("approved." + _content("c93-resources", {"binding": binding, "home": str(self._home)}).sha256,))
        op = next(o for o in product_operations() if o.capability.capability == CAPABILITY)
        if op.transition.transition != TRANSITION or op.policy != LEGACY or op.capability.effect != Effect.OBSERVE:
            raise ValueError("C93 catalog version policy mismatch")
        source = (self._root / "2_products/pepper-agent/tools/pepper_workflow_tools.py").read_bytes()
        proof = inspect_correspondence(source, op.handler)
        if proof.status != BindingStatus.VERIFIED:
            raise ValueError("C93 handler correspondence unqualified")
        handler = binding_identity(proof)
        policy = operation_policy(CAPABILITY.contract_id, actor, scope)
        if frozenset(policy.prerequisites) != PREREQUISITES or policy.consent_kind is not None:
            raise ValueError("C93 actual policy requirements mismatch")
        evidence = _content("c93-preflight-facts", {"capture": capture_ref.model_dump(mode="json"),
            "implementation": self._implementation.model_dump(mode="json"),
            "handler": handler.model_dump(mode="json"), "scope": scope.model_dump(mode="json")})
        prerequisites = tuple(PrerequisiteObservation(requirement=p, observation=Observation(
            source=SourceRef(source_id=evidence.content_id, kind=SourceKind.FACT, format=OWNER),
            scope=scope, actor=actor, status=ObservationStatus.PRESENT, reason_code="original_c93_preflight_validated",
            source_content=evidence, observed_schema_version=1, integrity=CheckStatus.VERIFIED,
            structure=CheckStatus.VERIFIED, binding=CheckStatus.VERIFIED,
            consistency="STABLE_CAPTURE", completeness="BOUND_SOURCE_ONLY")) for p in policy.prerequisites)
        authority = AuthorityReference(authority_id="approved." + d["approval_publication_SHA256"],
            kind="current_approved_publication", issuer=ActorRef(actor_id="c93-read-owner"), subject=actor,
            scope=scope, policy=LEGACY, record=_content("c93-original-approval", d),
            dependencies=(capture_ref, self._implementation), currentness=AuthorityCurrentness.CURRENT)
        unknown = StateDimension(definition=ContractRef(contract_id="c93.unqualified-dimension", version=1),
            value="not_qualified_by_c93", support=StateSupport.UNKNOWN)
        value = AdmissionInput(catalog=product_catalog(), catalog_content=product_catalog().content_identity(),
            capability=op.capability, transition=op.transition, policy=policy, actor=actor, scope=scope,
            state=WorkflowState(publication=StateDimension(definition=ContractRef(contract_id="pepper.publication", version=1),
                value="approved", support=StateSupport.SUPPORTED), execution=unknown, validation=unknown,
                review=unknown, completion=unknown, authority_currentness=AuthorityCurrentness.CURRENT),
            authorities=(authority,), prerequisites=prerequisites,
            authority_version="c93-authority." + _content("c93-authority", binding).sha256,
            source_version=self._implementation, effect=Effect.OBSERVE, handler_evidence=handler, consent=ConsentStatus.MISSING)
        q = QualifiedEvaluation(issuer=OWNER, input=value.content_identity(), authority_ids=(authority.authority_id,),
            prerequisites=policy.prerequisites, handler_evidence=handler)
        result = evaluate(value, trusted_issuer=OWNER, qualification=q)
        if result.decision.outcome.value != "ALLOW" or result.continuations[0].kind.value != "OBSERVATION":
            raise ValueError("C93 HAR admission rejected; no fallback")
        publication = g["ticket_publication_result"]["publication"]
        from .workflow import ticket_architect_bridge as bridge
        from .work_packet.compiler import SOURCE_TICKET_DIGEST_ALGORITHM
        algorithms = (bridge.TICKET_ARCHITECT_BRIDGE_DIGEST_ALGORITHM,
            bridge.TICKET_APPROVAL_PUBLICATION_DIGEST_ALGORITHM, SOURCE_TICKET_DIGEST_ALGORITHM)
        if algorithms != ("agent-platform-ticket-architect-bridge-record-sha256-v1",
                "agent-platform-ticket-approval-publication-p18-9-0-sha256-v1",
                "agent-platform-work-packet-source-ticket-sha256-v1"):
            raise ValueError("C93 unsupported original digest versions")
        self._sequence += 1
        qualification = C93ReadQualification(owner_policy=OWNER, legacy_policy=LEGACY,
            invocation_binding=_content("c93-invocation", {"owner": id(self), "sequence": self._sequence,
                "process": self._context[0], "thread": self._context[1], "capture": capture_ref.sha256}),
            project_id=g["project_id"], ticket_id=g["ticket_id"], revision=binding["revision"],
            publication_revision=publication["revision"], work_packet_id=g["work_packet_id"],
            scope=scope, read_principal=actor, original_actor=d["actor"], original_reviewer=d["reviewer_id"],
            original_decision=d["decision"], artifact_binding=_content("c93-artifact-binding", binding),
            original_generation=_content("c93-original-generation", g), original_approval=authority.record,
            original_workflow=_content("c93-original-workflow", {"generation": g["workflow_transition_result"],
                "approval": d["workflow_transition_result"]}), request=request_ref,
            section=_content("c93-section", g["ticket_spec"]["validation_steps"]),
            serialized_section=ContentRef(content_id="c93-serialized-section", sha256=response["exact_body_serialized_SHA256"]),
            response=_content("c93-response", response), effective_parameters=_content("c93-effective-parameters", response["pagination"]),
            implementation=self._implementation, validator_sources=self._sources, handler_correspondence=handler,
            capture=capture_ref, admission_input=value.content_identity(), qualified_facts=tuple("F%02d" % i for i in range(1, 15)),
            original_algorithms=algorithms)
        invocation = _Invocation(self._seal, self._context, json.loads(_json(capture)), value, qualification, result.decision.outcome.value)
        self._active[id(invocation)] = invocation
        return invocation

    def _finish(self, invocation, capture):
        if self._active.get(id(invocation)) is not invocation or invocation.used:
            raise ValueError("C93 foreign or consumed qualification")
        if invocation.seal is not self._seal:
            raise ValueError("C93 forged issuer")
        self._check_context()
        if invocation.context != _execution_context():
            raise ValueError("C93 foreign invocation context")
        if _content("c93-capture", capture) != invocation.qualification.capture:
            raise ValueError("C93 request authority or parameters changed")
        if invocation.input.content_identity() != invocation.qualification.admission_input:
            raise ValueError("C93 admission input changed")
        invocation.used = True
        self._observations.append(invocation.qualification)

    def _discard(self, invocation):
        self._active.pop(id(invocation), None)
        invocation.used = True
