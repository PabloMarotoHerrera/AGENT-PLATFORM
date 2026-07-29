"""Dependency-only DAG and wave planning contracts for Pepper tickets."""

from __future__ import annotations

from enum import Enum
import hashlib
import json
import re
from typing import Annotated, Literal, TypeAlias

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StrictBool,
    StringConstraints,
    model_validator,
)

from hermes_cli.agent_platform.ticket_factory.specs import (
    DependencyKind,
    DependencyScope,
    ParallelizationHint,
    ProjectSpec,
    RepositoryPathPattern,
    TicketSpec,
)

DEPENDENCY_PLAN_SCHEMA_VERSION = 1
PLANNING_INPUT_DIGEST_ALGORITHM = "agent-platform-ticket-dependency-input-sha256-v1"
DEPENDENCY_PLAN_DIGEST_ALGORITHM = "agent-platform-ticket-dependency-plan-sha256-v1"


class DependencyPlanningError(ValueError):
    """Base error for dependency-only planning failures."""


class DependencyCollectionValidationError(DependencyPlanningError):
    """Raised when the ticket collection cannot form a valid planning input."""


class DependencyCycleError(DependencyPlanningError):
    """Raised when hard internal prerequisites contain a cycle."""

    def __init__(self, cycle_ticket_ids: tuple[str, ...]) -> None:
        self.cycle_ticket_ids = cycle_ticket_ids
        joined = " > ".join(cycle_ticket_ids)
        super().__init__(f"hard dependency cycle detected: ticket_ids={joined}")


class ExternalDependencyState(str, Enum):
    SATISFIED = "satisfied"
    UNRESOLVED = "unresolved"
    BLOCKED = "blocked"


class ScopeCollisionKind(str, Enum):
    EXACT_PATTERN = "exact_pattern"
    RECURSIVE_PREFIX = "recursive_prefix"
    GLOBAL_PATTERN = "global_pattern"
    AMBIGUOUS_GLOB = "ambiguous_glob"


class TicketBlockerKind(str, Enum):
    EXTERNAL_UNRESOLVED = "external_unresolved"
    EXTERNAL_BLOCKED = "external_blocked"
    UPSTREAM_BLOCKED = "upstream_blocked"


class WaveDisposition(str, Enum):
    DEPENDENCY_READY = "dependency_ready"
    SERIAL = "serial"
    SCOPE_REVIEW_REQUIRED = "scope_review_required"


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


def _reject_identifier_whitespace(value: object) -> object:
    if isinstance(value, str) and any(character.isspace() for character in value):
        raise ValueError("identifier must not contain whitespace")
    return value


ShortText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_reject_nul),
]
ProjectIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=2, max_length=5, pattern=r"^P[1-9][0-9]{0,3}$"),
]
TicketIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(
        min_length=4,
        max_length=64,
        pattern=r"^P[1-9][0-9]{0,3}(?:\.[A-Z0-9]+)+$",
    ),
]
CollisionIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=9, max_length=16, pattern=r"^SCOPE-[0-9]{3,10}$"),
]
WaveIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=8, max_length=8, pattern=r"^WAVE-[0-9]{3}$"),
]
DigestText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$"),
]


class _DependencyPlanningModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
    )


class ExternalDependencyResolution(_DependencyPlanningModel):
    ticket_id: TicketIdentifier
    state: ExternalDependencyState
    evidence_reference: ShortText | None = None
    rationale: ShortText

    @model_validator(mode="after")
    def _validate_resolution(self) -> ExternalDependencyResolution:
        if (
            self.state is ExternalDependencyState.SATISFIED
            and self.evidence_reference is None
        ):
            raise ValueError(
                "satisfied external dependencies require evidence_reference"
            )
        return self


class DependencyEdge(_DependencyPlanningModel):
    prerequisite_ticket_id: TicketIdentifier
    dependent_ticket_id: TicketIdentifier
    kind: DependencyKind
    scope: DependencyScope
    blocks_readiness: StrictBool

    @model_validator(mode="after")
    def _validate_edge(self) -> DependencyEdge:
        expected = self.kind is DependencyKind.HARD_PREREQUISITE
        if self.blocks_readiness is not expected:
            raise ValueError("blocks_readiness must match dependency kind")
        return self


class ScopeCollision(_DependencyPlanningModel):
    collision_id: CollisionIdentifier
    left_ticket_id: TicketIdentifier
    right_ticket_id: TicketIdentifier
    left_path_pattern: RepositoryPathPattern
    right_path_pattern: RepositoryPathPattern
    kind: ScopeCollisionKind
    blocks_same_wave: StrictBool

    @model_validator(mode="after")
    def _validate_collision(self) -> ScopeCollision:
        if _ticket_sort_key(self.left_ticket_id) >= _ticket_sort_key(
            self.right_ticket_id
        ):
            raise ValueError("ticket pair must be in canonical order")
        expected = self.kind is not ScopeCollisionKind.AMBIGUOUS_GLOB
        if self.blocks_same_wave is not expected:
            raise ValueError("blocks_same_wave must match collision kind")
        return self


class TicketBlocker(_DependencyPlanningModel):
    ticket_id: TicketIdentifier
    blocked_by_ticket_id: TicketIdentifier
    kind: TicketBlockerKind
    direct: StrictBool
    rationale: ShortText


class ParallelPlanningPolicy(_DependencyPlanningModel):
    max_wave_size: int = Field(default=32, ge=1, le=64, strict=True)
    separate_serial_tickets: Literal[True] = True
    separate_known_scope_collisions: Literal[True] = True
    ambiguous_glob_requires_review: Literal[True] = True


class TicketPlanningRequest(_DependencyPlanningModel):
    project_spec: ProjectSpec
    tickets: tuple[TicketSpec, ...] = Field(min_length=1, max_length=512)
    external_dependency_resolutions: tuple[ExternalDependencyResolution, ...] = Field(
        default=(), max_length=512
    )
    policy: ParallelPlanningPolicy = ParallelPlanningPolicy()

    @model_validator(mode="after")
    def _validate_request(self) -> TicketPlanningRequest:
        _validate_collection(self, error_type=ValueError)
        return self


class ParallelWave(_DependencyPlanningModel):
    # ParallelWave is dependency-ready planning metadata, not execution authority.
    wave_index: int = Field(ge=1, strict=True)
    wave_id: WaveIdentifier
    ticket_ids: tuple[TicketIdentifier, ...] = Field(min_length=1)
    disposition: WaveDisposition
    scope_collision_ids: tuple[CollisionIdentifier, ...] = ()

    @model_validator(mode="after")
    def _validate_wave(self) -> ParallelWave:
        if self.wave_id != _wave_id(self.wave_index):
            raise ValueError("wave_id must match wave_index")
        _reject_duplicate_strings(self.ticket_ids, "ticket_ids")
        _reject_duplicate_strings(self.scope_collision_ids, "scope_collision_ids")
        if self.disposition is WaveDisposition.SERIAL and len(self.ticket_ids) != 1:
            raise ValueError("serial waves must contain exactly one ticket")
        if self.disposition is WaveDisposition.SCOPE_REVIEW_REQUIRED:
            if not self.scope_collision_ids:
                raise ValueError("scope review waves require collision evidence")
        elif self.scope_collision_ids:
            raise ValueError("only scope review waves may carry collision evidence")
        return self


class TicketDependencyPlan(_DependencyPlanningModel):
    schema_version: Literal[1] = DEPENDENCY_PLAN_SCHEMA_VERSION
    project_id: ProjectIdentifier
    ticket_ids: tuple[TicketIdentifier, ...]
    planning_input_SHA256: DigestText
    edges: tuple[DependencyEdge, ...]
    scope_collisions: tuple[ScopeCollision, ...]
    blockers: tuple[TicketBlocker, ...]
    topological_order: tuple[TicketIdentifier, ...]
    waves: tuple[ParallelWave, ...]
    blocked_ticket_ids: tuple[TicketIdentifier, ...]
    unresolved_soft_external_dependency_ids: tuple[TicketIdentifier, ...]
    policy: ParallelPlanningPolicy
    plan_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_plan(self) -> TicketDependencyPlan:
        _reject_duplicate_strings(self.ticket_ids, "ticket_ids")
        if tuple(sorted(self.ticket_ids, key=_ticket_sort_key)) != self.ticket_ids:
            raise ValueError("ticket_ids must be in canonical order")
        if tuple(sorted(self.edges, key=_edge_sort_key)) != self.edges:
            raise ValueError("edges must be in deterministic order")
        if (
            tuple(sorted(self.scope_collisions, key=_collision_sort_key))
            != self.scope_collisions
        ):
            raise ValueError("scope_collisions must be in deterministic order")
        for index, collision in enumerate(self.scope_collisions, start=1):
            if collision.collision_id != _collision_id(index):
                raise ValueError("scope collision identifiers must be sequential")
        if tuple(sorted(self.blockers, key=_blocker_sort_key)) != self.blockers:
            raise ValueError("blockers must be in deterministic order")
        if frozenset(self.topological_order) != frozenset(self.ticket_ids):
            raise ValueError("topological_order must contain all tickets")
        if len(self.topological_order) != len(self.ticket_ids):
            raise ValueError("topological_order must not contain duplicates")
        _reject_duplicate_strings(self.blocked_ticket_ids, "blocked_ticket_ids")
        if (
            tuple(sorted(self.blocked_ticket_ids, key=_ticket_sort_key))
            != self.blocked_ticket_ids
        ):
            raise ValueError("blocked_ticket_ids must be in canonical order")
        _reject_duplicate_strings(
            self.unresolved_soft_external_dependency_ids,
            "unresolved_soft_external_dependency_ids",
        )
        if (
            tuple(
                sorted(
                    self.unresolved_soft_external_dependency_ids,
                    key=_ticket_sort_key,
                )
            )
            != self.unresolved_soft_external_dependency_ids
        ):
            raise ValueError(
                "unresolved_soft_external_dependency_ids must be in canonical order"
            )
        waved_ticket_ids = tuple(
            ticket_id for wave in self.waves for ticket_id in wave.ticket_ids
        )
        _reject_duplicate_strings(waved_ticket_ids, "wave ticket_ids")
        blocked_set = frozenset(self.blocked_ticket_ids)
        blocker_ticket_ids = frozenset(blocker.ticket_id for blocker in self.blockers)
        if blocker_ticket_ids != blocked_set:
            raise ValueError("blocked_ticket_ids must match blocker ticket IDs")
        if blocked_set.intersection(waved_ticket_ids):
            raise ValueError("blocked tickets must not appear in waves")
        if frozenset(waved_ticket_ids).union(blocked_set) != frozenset(self.ticket_ids):
            raise ValueError("waves plus blocked tickets must cover all tickets")
        if len(waved_ticket_ids) + len(blocked_set) != len(self.ticket_ids):
            raise ValueError("wave and blocked ticket counts must match ticket count")
        topo_index = {
            ticket_id: index for index, ticket_id in enumerate(self.topological_order)
        }
        wave_index_by_ticket_id = {
            ticket_id: wave.wave_index
            for wave in self.waves
            for ticket_id in wave.ticket_ids
        }
        for index, wave in enumerate(self.waves, start=1):
            if wave.wave_index != index:
                raise ValueError("wave indices must be sequential")
            if len(wave.ticket_ids) > self.policy.max_wave_size:
                raise ValueError(
                    "wave ticket count must not exceed policy max_wave_size"
                )
        for edge in self.edges:
            if (
                edge.scope is DependencyScope.INTERNAL_PROJECT
                and edge.blocks_readiness
                and topo_index[edge.prerequisite_ticket_id]
                >= topo_index[edge.dependent_ticket_id]
            ):
                raise ValueError("hard prerequisites must precede dependents")
            if (
                edge.scope is DependencyScope.INTERNAL_PROJECT
                and edge.blocks_readiness
                and edge.prerequisite_ticket_id not in blocked_set
                and edge.dependent_ticket_id not in blocked_set
                and wave_index_by_ticket_id[edge.prerequisite_ticket_id]
                >= wave_index_by_ticket_id[edge.dependent_ticket_id]
            ):
                raise ValueError("hard prerequisites must be in earlier waves")
        known_collision_pairs = frozenset(
            _collision_pair(collision.left_ticket_id, collision.right_ticket_id)
            for collision in self.scope_collisions
            if collision.blocks_same_wave
        )
        ambiguous_collision_ids = frozenset(
            collision.collision_id
            for collision in self.scope_collisions
            if collision.kind is ScopeCollisionKind.AMBIGUOUS_GLOB
        )
        for wave in self.waves:
            for left_index, left_ticket_id in enumerate(wave.ticket_ids):
                for right_ticket_id in wave.ticket_ids[left_index + 1 :]:
                    if (
                        _collision_pair(left_ticket_id, right_ticket_id)
                        in known_collision_pairs
                    ):
                        raise ValueError("known scope collisions must not share a wave")
            if any(
                collision_id not in ambiguous_collision_ids
                for collision_id in wave.scope_collision_ids
            ):
                raise ValueError(
                    "scope review waves must reference ambiguous collision IDs"
                )
        if self.plan_SHA256 != _plan_digest(
            schema_version=self.schema_version,
            project_id=self.project_id,
            ticket_ids=self.ticket_ids,
            planning_input_SHA256=self.planning_input_SHA256,
            edges=self.edges,
            scope_collisions=self.scope_collisions,
            blockers=self.blockers,
            topological_order=self.topological_order,
            waves=self.waves,
            blocked_ticket_ids=self.blocked_ticket_ids,
            unresolved_soft_external_dependency_ids=(
                self.unresolved_soft_external_dependency_ids
            ),
            policy=self.policy,
        ):
            raise ValueError("plan_SHA256 must match dependency plan digest record")
        return self


_TICKET_ID_PATTERN = re.compile(r"^P([1-9][0-9]{0,3})((?:\.[A-Z0-9]+)+)$")
_TOKEN_PATTERN = re.compile(r"[0-9]+|[A-Z]+")
_GLOB_CHARACTERS = frozenset("*?[")
_EDGE_KIND_RANK = {
    DependencyKind.HARD_PREREQUISITE: 0,
    DependencyKind.SOFT_PREDECESSOR: 1,
}
_EDGE_SCOPE_RANK = {
    DependencyScope.INTERNAL_PROJECT: 0,
    DependencyScope.EXTERNAL_PROJECT: 1,
}
_COLLISION_KIND_RANK = {
    ScopeCollisionKind.EXACT_PATTERN: 0,
    ScopeCollisionKind.RECURSIVE_PREFIX: 1,
    ScopeCollisionKind.GLOBAL_PATTERN: 2,
    ScopeCollisionKind.AMBIGUOUS_GLOB: 3,
}
_BLOCKER_KIND_RANK = {
    TicketBlockerKind.EXTERNAL_UNRESOLVED: 0,
    TicketBlockerKind.EXTERNAL_BLOCKED: 1,
    TicketBlockerKind.UPSTREAM_BLOCKED: 2,
}


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _deterministic_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _reject_duplicate_strings(values: tuple[str, ...], field_name: str) -> None:
    if len(values) != len(frozenset(values)):
        raise ValueError(f"{field_name} must not contain duplicate entries")


def _ticket_sort_key(
    ticket_id: str,
) -> tuple[int, tuple[tuple[tuple[int, int | str], ...], ...]]:
    match = _TICKET_ID_PATTERN.match(ticket_id)
    if match is None:
        return (0, ())
    project_number = int(match.group(1))
    segments = match.group(2).strip(".").split(".")
    segment_keys: list[tuple[tuple[int, int | str], ...]] = []
    for segment in segments:
        tokens: list[tuple[int, int | str]] = []
        for token in _TOKEN_PATTERN.findall(segment):
            if token.isdigit():
                tokens.append((0, int(token)))
            else:
                tokens.append((1, token))
        segment_keys.append(tuple(tokens))
    return (project_number, tuple(segment_keys))


def _edge_sort_key(edge: DependencyEdge) -> tuple[object, ...]:
    return (
        _ticket_sort_key(edge.prerequisite_ticket_id),
        _ticket_sort_key(edge.dependent_ticket_id),
        _EDGE_KIND_RANK[edge.kind],
        _EDGE_SCOPE_RANK[edge.scope],
    )


def _collision_sort_key(collision: ScopeCollision) -> tuple[object, ...]:
    return (
        _ticket_sort_key(collision.left_ticket_id),
        _ticket_sort_key(collision.right_ticket_id),
        _COLLISION_KIND_RANK[collision.kind],
        collision.left_path_pattern,
        collision.right_path_pattern,
    )


def _blocker_sort_key(blocker: TicketBlocker) -> tuple[object, ...]:
    return (
        _ticket_sort_key(blocker.ticket_id),
        _BLOCKER_KIND_RANK[blocker.kind],
        _ticket_sort_key(blocker.blocked_by_ticket_id),
        0 if blocker.direct else 1,
    )


def _resolution_sort_key(
    resolution: ExternalDependencyResolution,
) -> tuple[object, ...]:
    return (_ticket_sort_key(resolution.ticket_id), resolution.state.value)


def _collision_id(index: int) -> str:
    return f"SCOPE-{index:03d}"


def _wave_id(index: int) -> str:
    return f"WAVE-{index:03d}"


def _validate_collection(
    request: TicketPlanningRequest, *, error_type: type[Exception]
) -> None:
    project_id = request.project_spec.project_id
    ticket_ids = tuple(ticket.ticket_id for ticket in request.tickets)
    if len(ticket_ids) != len(frozenset(ticket_ids)):
        raise error_type("ticket IDs must be unique")
    ticket_id_set = frozenset(ticket_ids)
    declared_external_dependency_ids: set[str] = set()
    for ticket in request.tickets:
        if ticket.project_id != project_id:
            raise error_type(
                f"ticket project_id must match project: ticket_id={ticket.ticket_id}"
            )
        if not ticket.ticket_id.startswith(f"{project_id}."):
            raise error_type(
                f"ticket_id must use project prefix: ticket_id={ticket.ticket_id}"
            )
        for dependency in ticket.dependencies:
            dependency_is_current_project = dependency.ticket_id.startswith(
                f"{project_id}."
            )
            if dependency.scope is DependencyScope.INTERNAL_PROJECT:
                if not dependency_is_current_project:
                    raise error_type(
                        "internal dependency must use current project prefix: "
                        f"ticket_id={ticket.ticket_id}; dependency_ticket_id={dependency.ticket_id}"
                    )
                if dependency.ticket_id not in ticket_id_set:
                    raise error_type(
                        "internal dependency target is not in ticket collection: "
                        f"ticket_id={ticket.ticket_id}; dependency_ticket_id={dependency.ticket_id}"
                    )
            else:
                if dependency_is_current_project:
                    raise error_type(
                        "external dependency must not use current project prefix: "
                        f"ticket_id={ticket.ticket_id}; dependency_ticket_id={dependency.ticket_id}"
                    )
                declared_external_dependency_ids.add(dependency.ticket_id)
    resolution_ids = tuple(
        resolution.ticket_id for resolution in request.external_dependency_resolutions
    )
    if len(resolution_ids) != len(frozenset(resolution_ids)):
        raise error_type("external_dependency_resolutions must not contain duplicates")
    for resolution in request.external_dependency_resolutions:
        if resolution.ticket_id not in declared_external_dependency_ids:
            raise error_type(
                "external dependency resolution target is not declared: "
                f"dependency_ticket_id={resolution.ticket_id}"
            )


def _canonical_tickets(request: TicketPlanningRequest) -> tuple[TicketSpec, ...]:
    return tuple(
        sorted(request.tickets, key=lambda ticket: _ticket_sort_key(ticket.ticket_id))
    )


def _canonical_resolutions(
    request: TicketPlanningRequest,
) -> tuple[ExternalDependencyResolution, ...]:
    return tuple(
        sorted(request.external_dependency_resolutions, key=_resolution_sort_key)
    )


def _planning_input_digest(request: TicketPlanningRequest) -> str:
    record = {
        "algorithm": PLANNING_INPUT_DIGEST_ALGORITHM,
        "project_spec": request.project_spec.model_dump(mode="json"),
        "tickets": [
            ticket.model_dump(mode="json") for ticket in _canonical_tickets(request)
        ],
        "external_dependency_resolutions": [
            resolution.model_dump(mode="json")
            for resolution in _canonical_resolutions(request)
        ],
        "policy": request.policy.model_dump(mode="json"),
    }
    return _sha256_text(_deterministic_json(record))


def _plan_digest(
    *,
    schema_version: int,
    project_id: str,
    ticket_ids: tuple[str, ...],
    planning_input_SHA256: str,
    edges: tuple[DependencyEdge, ...],
    scope_collisions: tuple[ScopeCollision, ...],
    blockers: tuple[TicketBlocker, ...],
    topological_order: tuple[str, ...],
    waves: tuple[ParallelWave, ...],
    blocked_ticket_ids: tuple[str, ...],
    unresolved_soft_external_dependency_ids: tuple[str, ...],
    policy: ParallelPlanningPolicy,
) -> str:
    record = {
        "algorithm": DEPENDENCY_PLAN_DIGEST_ALGORITHM,
        "schema_version": schema_version,
        "project_id": project_id,
        "ticket_ids": list(ticket_ids),
        "planning_input_SHA256": planning_input_SHA256,
        "edges": [edge.model_dump(mode="json") for edge in edges],
        "scope_collisions": [
            collision.model_dump(mode="json") for collision in scope_collisions
        ],
        "blockers": [blocker.model_dump(mode="json") for blocker in blockers],
        "topological_order": list(topological_order),
        "waves": [wave.model_dump(mode="json") for wave in waves],
        "blocked_ticket_ids": list(blocked_ticket_ids),
        "unresolved_soft_external_dependency_ids": list(
            unresolved_soft_external_dependency_ids
        ),
        "policy": policy.model_dump(mode="json"),
    }
    return _sha256_text(_deterministic_json(record))


def _build_edges(tickets: tuple[TicketSpec, ...]) -> tuple[DependencyEdge, ...]:
    edges = tuple(
        DependencyEdge(
            prerequisite_ticket_id=dependency.ticket_id,
            dependent_ticket_id=ticket.ticket_id,
            kind=dependency.kind,
            scope=dependency.scope,
            blocks_readiness=dependency.kind is DependencyKind.HARD_PREREQUISITE,
        )
        for ticket in tickets
        for dependency in ticket.dependencies
    )
    return tuple(sorted(edges, key=_edge_sort_key))


def _hard_internal_adjacency(
    ticket_ids: tuple[str, ...], edges: tuple[DependencyEdge, ...]
) -> tuple[dict[str, tuple[str, ...]], dict[str, tuple[str, ...]]]:
    dependents: dict[str, list[str]] = {ticket_id: [] for ticket_id in ticket_ids}
    prerequisites: dict[str, list[str]] = {ticket_id: [] for ticket_id in ticket_ids}
    ticket_set = frozenset(ticket_ids)
    for edge in edges:
        if (
            edge.kind is DependencyKind.HARD_PREREQUISITE
            and edge.scope is DependencyScope.INTERNAL_PROJECT
            and edge.prerequisite_ticket_id in ticket_set
            and edge.dependent_ticket_id in ticket_set
        ):
            dependents[edge.prerequisite_ticket_id].append(edge.dependent_ticket_id)
            prerequisites[edge.dependent_ticket_id].append(edge.prerequisite_ticket_id)
    return (
        {
            ticket_id: tuple(sorted(values, key=_ticket_sort_key))
            for ticket_id, values in dependents.items()
        },
        {
            ticket_id: tuple(sorted(values, key=_ticket_sort_key))
            for ticket_id, values in prerequisites.items()
        },
    )


def _topological_order(
    ticket_ids: tuple[str, ...], dependents: dict[str, tuple[str, ...]]
) -> tuple[str, ...]:
    indegree = {ticket_id: 0 for ticket_id in ticket_ids}
    for prerequisite_dependents in dependents.values():
        for dependent in prerequisite_dependents:
            indegree[dependent] += 1
    ready = sorted(
        (ticket_id for ticket_id, count in indegree.items() if count == 0),
        key=_ticket_sort_key,
    )
    ordered: list[str] = []
    while ready:
        current = ready.pop(0)
        ordered.append(current)
        for dependent in dependents[current]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)
        ready.sort(key=_ticket_sort_key)
    if len(ordered) != len(ticket_ids):
        raise DependencyCycleError(_cycle_witness(ticket_ids, dependents))
    return tuple(ordered)


def _cycle_witness(
    ticket_ids: tuple[str, ...], dependents: dict[str, tuple[str, ...]]
) -> tuple[str, ...]:
    state: dict[str, str] = {}
    stack: list[str] = []
    found: list[str] = []

    def visit(ticket_id: str) -> bool:
        state[ticket_id] = "visiting"
        stack.append(ticket_id)
        for dependent in dependents[ticket_id]:
            dependent_state = state.get(dependent)
            if dependent_state is None:
                if visit(dependent):
                    return True
            elif dependent_state == "visiting":
                found.extend(stack[stack.index(dependent) :])
                return True
        stack.pop()
        state[ticket_id] = "visited"
        return False

    for ticket_id in sorted(ticket_ids, key=_ticket_sort_key):
        if state.get(ticket_id) is None and visit(ticket_id):
            break
    return _canonical_cycle(tuple(found))


def _canonical_cycle(cycle: tuple[str, ...]) -> tuple[str, ...]:
    if not cycle:
        return ()
    best_index = min(
        range(len(cycle)), key=lambda index: _ticket_sort_key(cycle[index])
    )
    return cycle[best_index:] + cycle[:best_index]


def _classify_scope_collision(
    left_pattern: str, right_pattern: str
) -> ScopeCollisionKind | None:
    if left_pattern == "**" or right_pattern == "**":
        return ScopeCollisionKind.GLOBAL_PATTERN
    if left_pattern == right_pattern:
        return ScopeCollisionKind.EXACT_PATTERN
    if _recursive_prefix_overlaps(left_pattern, right_pattern):
        return ScopeCollisionKind.RECURSIVE_PREFIX
    if _has_nontrivial_glob(left_pattern) or _has_nontrivial_glob(right_pattern):
        return ScopeCollisionKind.AMBIGUOUS_GLOB
    return None


def _has_nontrivial_glob(pattern: str) -> bool:
    return any(character in pattern for character in _GLOB_CHARACTERS)


def _recursive_prefix_overlaps(left_pattern: str, right_pattern: str) -> bool:
    left_prefix = _recursive_prefix(left_pattern)
    right_prefix = _recursive_prefix(right_pattern)
    if left_prefix is not None and _pattern_is_inside_prefix(
        right_pattern, left_prefix
    ):
        return True
    if right_prefix is not None and _pattern_is_inside_prefix(
        left_pattern, right_prefix
    ):
        return True
    return False


def _recursive_prefix(pattern: str) -> str | None:
    if pattern.endswith("/**") and pattern != "**":
        return pattern[:-3]
    return None


def _pattern_is_inside_prefix(pattern: str, prefix: str) -> bool:
    return pattern == prefix or pattern.startswith(f"{prefix}/")


def _detect_scope_collisions(
    tickets: tuple[TicketSpec, ...],
) -> tuple[ScopeCollision, ...]:
    collision_inputs: list[tuple[str, str, str, str, ScopeCollisionKind]] = []
    for left_index, left_ticket in enumerate(tickets):
        for right_ticket in tickets[left_index + 1 :]:
            for left_pattern in left_ticket.scope.allowed_paths:
                for right_pattern in right_ticket.scope.allowed_paths:
                    kind = _classify_scope_collision(left_pattern, right_pattern)
                    if kind is not None:
                        collision_inputs.append((
                            left_ticket.ticket_id,
                            right_ticket.ticket_id,
                            left_pattern,
                            right_pattern,
                            kind,
                        ))
    collision_inputs.sort(
        key=lambda item: (
            _ticket_sort_key(item[0]),
            _ticket_sort_key(item[1]),
            _COLLISION_KIND_RANK[item[4]],
            item[2],
            item[3],
        )
    )
    return tuple(
        ScopeCollision(
            collision_id=_collision_id(index),
            left_ticket_id=left_ticket_id,
            right_ticket_id=right_ticket_id,
            left_path_pattern=left_pattern,
            right_path_pattern=right_pattern,
            kind=kind,
            blocks_same_wave=kind is not ScopeCollisionKind.AMBIGUOUS_GLOB,
        )
        for index, (
            left_ticket_id,
            right_ticket_id,
            left_pattern,
            right_pattern,
            kind,
        ) in enumerate(collision_inputs, start=1)
    )


def _build_blockers(
    tickets: tuple[TicketSpec, ...],
    edges: tuple[DependencyEdge, ...],
    resolutions: tuple[ExternalDependencyResolution, ...],
    topological_order: tuple[str, ...],
    dependents: dict[str, tuple[str, ...]],
) -> tuple[TicketBlocker, ...]:
    resolution_by_ticket_id = {
        resolution.ticket_id: resolution for resolution in resolutions
    }
    blockers: list[TicketBlocker] = []
    blockers_by_ticket_id: dict[str, list[TicketBlocker]] = {
        ticket.ticket_id: [] for ticket in tickets
    }
    ticket_by_id = {ticket.ticket_id: ticket for ticket in tickets}
    for ticket in tickets:
        for dependency in ticket.dependencies:
            if (
                dependency.kind is not DependencyKind.HARD_PREREQUISITE
                or dependency.scope is not DependencyScope.EXTERNAL_PROJECT
            ):
                continue
            resolution = resolution_by_ticket_id.get(dependency.ticket_id)
            state = (
                ExternalDependencyState.UNRESOLVED
                if resolution is None
                else resolution.state
            )
            if state is ExternalDependencyState.SATISFIED:
                continue
            kind = (
                TicketBlockerKind.EXTERNAL_UNRESOLVED
                if state is ExternalDependencyState.UNRESOLVED
                else TicketBlockerKind.EXTERNAL_BLOCKED
            )
            blocker = TicketBlocker(
                ticket_id=ticket.ticket_id,
                blocked_by_ticket_id=dependency.ticket_id,
                kind=kind,
                direct=True,
                rationale=(
                    f"hard external dependency is {state.value}: "
                    f"dependency_ticket_id={dependency.ticket_id}"
                ),
            )
            blockers.append(blocker)
            blockers_by_ticket_id[ticket.ticket_id].append(blocker)
    for prerequisite_id in topological_order:
        if not blockers_by_ticket_id[prerequisite_id]:
            continue
        for dependent_id in dependents[prerequisite_id]:
            if dependent_id not in ticket_by_id:
                continue
            blocker = TicketBlocker(
                ticket_id=dependent_id,
                blocked_by_ticket_id=prerequisite_id,
                kind=TicketBlockerKind.UPSTREAM_BLOCKED,
                direct=False,
                rationale=(
                    "hard internal prerequisite is blocked: "
                    f"prerequisite_ticket_id={prerequisite_id}"
                ),
            )
            if blocker not in blockers_by_ticket_id[dependent_id]:
                blockers.append(blocker)
                blockers_by_ticket_id[dependent_id].append(blocker)
    return tuple(sorted(blockers, key=_blocker_sort_key))


def _unresolved_soft_external_dependency_ids(
    tickets: tuple[TicketSpec, ...],
    resolutions: tuple[ExternalDependencyResolution, ...],
) -> tuple[str, ...]:
    resolution_by_ticket_id = {
        resolution.ticket_id: resolution for resolution in resolutions
    }
    unresolved: set[str] = set()
    for ticket in tickets:
        for dependency in ticket.dependencies:
            if (
                dependency.kind is DependencyKind.SOFT_PREDECESSOR
                and dependency.scope is DependencyScope.EXTERNAL_PROJECT
            ):
                resolution = resolution_by_ticket_id.get(dependency.ticket_id)
                if (
                    resolution is None
                    or resolution.state is not ExternalDependencyState.SATISFIED
                ):
                    unresolved.add(dependency.ticket_id)
    return tuple(sorted(unresolved, key=_ticket_sort_key))


def _collision_pair(left_ticket_id: str, right_ticket_id: str) -> tuple[str, str]:
    if _ticket_sort_key(left_ticket_id) <= _ticket_sort_key(right_ticket_id):
        return (left_ticket_id, right_ticket_id)
    return (right_ticket_id, left_ticket_id)


def _collision_maps(
    collisions: tuple[ScopeCollision, ...],
) -> tuple[
    dict[tuple[str, str], tuple[str, ...]], dict[tuple[str, str], tuple[str, ...]]
]:
    known: dict[tuple[str, str], list[str]] = {}
    ambiguous: dict[tuple[str, str], list[str]] = {}
    for collision in collisions:
        pair = _collision_pair(collision.left_ticket_id, collision.right_ticket_id)
        target = (
            ambiguous if collision.kind is ScopeCollisionKind.AMBIGUOUS_GLOB else known
        )
        target.setdefault(pair, []).append(collision.collision_id)
    return (
        {key: tuple(value) for key, value in known.items()},
        {key: tuple(value) for key, value in ambiguous.items()},
    )


def _build_waves(
    *,
    tickets: tuple[TicketSpec, ...],
    policy: ParallelPlanningPolicy,
    blockers: tuple[TicketBlocker, ...],
    prerequisites: dict[str, tuple[str, ...]],
    collisions: tuple[ScopeCollision, ...],
) -> tuple[ParallelWave, ...]:
    ticket_by_id = {ticket.ticket_id: ticket for ticket in tickets}
    blocked_ids = frozenset(blocker.ticket_id for blocker in blockers)
    unblocked_ids = tuple(
        ticket.ticket_id for ticket in tickets if ticket.ticket_id not in blocked_ids
    )
    unassigned = set(unblocked_ids)
    assigned: set[str] = set()
    known_collisions, ambiguous_collisions = _collision_maps(collisions)
    waves: list[ParallelWave] = []

    while unassigned:
        ready = tuple(
            ticket_id
            for ticket_id in sorted(unassigned, key=_ticket_sort_key)
            if all(
                prerequisite in assigned for prerequisite in prerequisites[ticket_id]
            )
        )
        if not ready:
            raise DependencyPlanningError("no dependency-ready tickets remain")
        first = ready[0]
        if ticket_by_id[first].parallelization_hint is ParallelizationHint.SERIAL:
            wave_ticket_ids = (first,)
            disposition = WaveDisposition.SERIAL
            scope_collision_ids: tuple[str, ...] = ()
        else:
            selected: list[str] = []
            for ticket_id in ready:
                if (
                    ticket_by_id[ticket_id].parallelization_hint
                    is ParallelizationHint.SERIAL
                ):
                    continue
                if len(selected) >= policy.max_wave_size:
                    break
                if any(
                    _collision_pair(ticket_id, existing) in known_collisions
                    for existing in selected
                ):
                    continue
                selected.append(ticket_id)
            if not selected:
                selected.append(first)
            wave_ticket_ids = tuple(selected)
            ambiguous_ids: list[str] = []
            for left_index, left_ticket_id in enumerate(wave_ticket_ids):
                for right_ticket_id in wave_ticket_ids[left_index + 1 :]:
                    ambiguous_ids.extend(
                        ambiguous_collisions.get(
                            _collision_pair(left_ticket_id, right_ticket_id), ()
                        )
                    )
            scope_collision_ids = tuple(ambiguous_ids)
            disposition = (
                WaveDisposition.SCOPE_REVIEW_REQUIRED
                if scope_collision_ids
                else WaveDisposition.DEPENDENCY_READY
            )
        wave = ParallelWave(
            wave_index=len(waves) + 1,
            wave_id=_wave_id(len(waves) + 1),
            ticket_ids=wave_ticket_ids,
            disposition=disposition,
            scope_collision_ids=scope_collision_ids,
        )
        waves.append(wave)
        for ticket_id in wave_ticket_ids:
            unassigned.remove(ticket_id)
            assigned.add(ticket_id)
    return tuple(waves)


def build_ticket_dependency_plan(
    request: TicketPlanningRequest,
) -> TicketDependencyPlan:
    """Build a deterministic dependency-only plan without execution authority."""

    _validate_collection(request, error_type=DependencyCollectionValidationError)
    tickets = _canonical_tickets(request)
    ticket_ids = tuple(ticket.ticket_id for ticket in tickets)
    edges = _build_edges(tickets)
    dependents, prerequisites = _hard_internal_adjacency(ticket_ids, edges)
    topological_order = _topological_order(ticket_ids, dependents)
    scope_collisions = _detect_scope_collisions(tickets)
    blockers = _build_blockers(
        tickets,
        edges,
        _canonical_resolutions(request),
        topological_order,
        dependents,
    )
    blocked_ticket_ids = tuple(
        sorted(
            frozenset(blocker.ticket_id for blocker in blockers), key=_ticket_sort_key
        )
    )
    waves = _build_waves(
        tickets=tickets,
        policy=request.policy,
        blockers=blockers,
        prerequisites=prerequisites,
        collisions=scope_collisions,
    )
    unresolved_soft_external_dependency_ids = _unresolved_soft_external_dependency_ids(
        tickets, _canonical_resolutions(request)
    )
    planning_input_SHA256 = _planning_input_digest(request)
    plan_SHA256 = _plan_digest(
        schema_version=DEPENDENCY_PLAN_SCHEMA_VERSION,
        project_id=request.project_spec.project_id,
        ticket_ids=ticket_ids,
        planning_input_SHA256=planning_input_SHA256,
        edges=edges,
        scope_collisions=scope_collisions,
        blockers=blockers,
        topological_order=topological_order,
        waves=waves,
        blocked_ticket_ids=blocked_ticket_ids,
        unresolved_soft_external_dependency_ids=unresolved_soft_external_dependency_ids,
        policy=request.policy,
    )
    return TicketDependencyPlan(
        project_id=request.project_spec.project_id,
        ticket_ids=ticket_ids,
        planning_input_SHA256=planning_input_SHA256,
        edges=edges,
        scope_collisions=scope_collisions,
        blockers=blockers,
        topological_order=topological_order,
        waves=waves,
        blocked_ticket_ids=blocked_ticket_ids,
        unresolved_soft_external_dependency_ids=unresolved_soft_external_dependency_ids,
        policy=request.policy,
        plan_SHA256=plan_SHA256,
    )
