"""Bounded passive source correspondence, outside the pure harness.

Receives explicit bytes, never imports a registry/tool or opens a path. VERIFIED
means a source declaration names a unique undecorated handler and admits the
declared selectors; not runtime binding, availability or correctness of routing.
"""

import ast
import hashlib
from enum import Enum
from typing import Annotated

from pydantic import Field, model_validator

from .harness.contracts import ContentRef, ContractRef, Digest, Identifier, _Contract

MAX_SOURCE_BYTES = 2_097_152
MAX_AST_NODES = 100_000


class BindingStatus(str, Enum):
    VERIFIED = "VERIFIED"
    ABSENT = "ABSENT"
    AMBIGUOUS = "AMBIGUOUS"
    CONTRADICTORY = "CONTRADICTORY"
    UNVERIFIABLE = "UNVERIFIABLE"


class Selector(_Contract):
    field: Identifier
    value: Identifier | bool


class HandlerDeclaration(_Contract):
    capability: ContractRef
    tool_name: Identifier
    handler_symbol: Annotated[str, Field(pattern=r"^[A-Za-z_][A-Za-z0-9_]{0,127}$", max_length=128)]
    selectors: Annotated[tuple[Selector, ...], Field(max_length=8)] = ()

    @model_validator(mode="after")
    def _unique(self) -> "HandlerDeclaration":
        if len({s.field for s in self.selectors}) != len(self.selectors):
            raise ValueError("duplicate selector")
        return self


class BindingEvidence(_Contract):
    declaration: HandlerDeclaration
    status: BindingStatus
    reason_code: Identifier
    source: ContentRef
    registry_import_line: Annotated[int, Field(ge=1, le=1_000_000)] | None = None
    registration_line: Annotated[int, Field(ge=1, le=1_000_000)] | None = None
    handler_line: Annotated[int, Field(ge=1, le=1_000_000)] | None = None
    handler_ast_sha256: Digest | None = None
    registration_ast_sha256: Digest | None = None

    @model_validator(mode="after")
    def _proof(self) -> "BindingEvidence":
        if self.status == BindingStatus.VERIFIED and any(v is None for v in (
                self.registry_import_line, self.registration_line, self.handler_line,
                self.handler_ast_sha256, self.registration_ast_sha256)):
            raise ValueError("verified source correspondence requires provenance")
        return self


class _Unknown(Exception):
    pass


def _resolve(node, assignments):
    seen = set()
    while isinstance(node, ast.Name):
        if node.id in seen or len(seen) >= 8 or len(assignments.get(node.id, ())) != 1:
            raise _Unknown("unresolved static schema")
        seen.add(node.id)
        node = assignments[node.id][0]
    return node


def _field(node, key, assignments):
    node = _resolve(node, assignments)
    if not isinstance(node, ast.Dict):
        raise _Unknown("schema is not a literal dictionary")
    found = None
    for k, value in zip(node.keys, node.values):
        if k is None or not isinstance(k, ast.Constant):
            # An opaque spread before an explicit key is overwritten by that
            # key. A spread after it makes its final value unverifiable.
            found = None
        elif k.value == key:
            if found is not None:
                raise _Unknown("duplicate schema key")
            found = value
    if found is None:
        raise _Unknown("schema field unresolved")
    return _resolve(found, assignments)


def _admits(schema, selectors, assignments):
    if not selectors:
        return True  # No claim about the opaque schema's contents.
    properties = _field(schema, "properties", assignments)
    for selector in selectors:
        definition = _field(properties, selector.field, assignments)
        try:
            choices = _field(definition, "enum", assignments)
            if not isinstance(choices, (ast.List, ast.Tuple)) or any(not isinstance(v, ast.Constant) for v in choices.elts):
                raise _Unknown("nonliteral selector enum")
            values = [v.value for v in choices.elts]
        except _Unknown:
            try:
                constant = _field(definition, "const", assignments)
                if not isinstance(constant, ast.Constant):
                    raise _Unknown("nonliteral selector constant")
                values = [constant.value]
            except _Unknown:
                kind = _field(definition, "type", assignments)
                if not isinstance(selector.value,bool) or not isinstance(kind,ast.Constant) or kind.value != "boolean":
                    raise _Unknown("unsupported selector schema")
                values = [False,True]
        if not any(type(v) is type(selector.value) and v == selector.value for v in values):
            return False
    # Only property membership is claimed. Full JSON-schema branch validation
    # and handler control-flow semantics are not inferred from this static test.
    return True


def inspect_correspondence(source: bytes, declaration: HandlerDeclaration,
                           source_id: str = "tools.pepper_workflow_tools") -> BindingEvidence:
    if not isinstance(source, bytes):
        raise TypeError("explicit source bytes required")
    from .harness.validation import canonical_json, parse_contract
    declaration = HandlerDeclaration.model_validate(declaration)
    declaration = parse_contract(HandlerDeclaration, canonical_json(declaration))
    if len(source) > MAX_SOURCE_BYTES:
        raise ValueError("source_size_bound")
    content = ContentRef(content_id=source_id, sha256=hashlib.sha256(source).hexdigest())
    def outcome(status, reason, **proof):
        return BindingEvidence(declaration=declaration, status=status, reason_code=reason, source=content, **proof)
    try:
        tree = ast.parse(source.decode("utf-8"))
        if sum(1 for _ in ast.walk(tree)) > MAX_AST_NODES:
            return outcome(BindingStatus.UNVERIFIABLE, "source_node_bound")
    except (SyntaxError, UnicodeError, RecursionError, ValueError):
        return outcome(BindingStatus.UNVERIFIABLE, "source_syntax_unsupported")
    assignments = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assignments.setdefault(target.id, []).append(node.value)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            assignments.setdefault(node.target.id, []).append(node.value)
    matches = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name) and node.func.value.id == "registry"
                and node.func.attr == "register"):
            continue
        keywords = {kw.arg: kw.value for kw in node.keywords}
        name = keywords.get("name")
        if name is None or not isinstance(name, ast.Constant) or not isinstance(name.value, str):
            return outcome(BindingStatus.UNVERIFIABLE, "dynamic_registration_name")
        if name.value == declaration.tool_name:
            matches.append(node)
    if not matches:
        return outcome(BindingStatus.ABSENT, "registration_absent")
    if len(matches) != 1:
        return outcome(BindingStatus.AMBIGUOUS, "multiple_registration_declarations")
    call = matches[0]
    if not any(isinstance(n, ast.Expr) and n.value is call for n in tree.body):
        return outcome(BindingStatus.UNVERIFIABLE, "conditional_registration")
    if call.args or any(kw.arg is None for kw in call.keywords):
        return outcome(BindingStatus.UNVERIFIABLE, "dynamic_registration_arguments")
    if len({kw.arg for kw in call.keywords}) != len(call.keywords):
        return outcome(BindingStatus.CONTRADICTORY, "duplicate_registration_keyword")
    keywords = {kw.arg: kw.value for kw in call.keywords}
    handler = keywords.get("handler")
    if not isinstance(handler, ast.Name):
        return outcome(BindingStatus.UNVERIFIABLE, "dynamic_handler_reference")
    if handler.id != declaration.handler_symbol:
        return outcome(BindingStatus.CONTRADICTORY, "handler_symbol_mismatch")
    functions = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == handler.id]
    if len(functions) != 1:
        return outcome(BindingStatus.AMBIGUOUS if functions else BindingStatus.ABSENT, "handler_definition_not_unique")
    function = functions[0]
    if function.lineno >= call.lineno:
        return outcome(BindingStatus.CONTRADICTORY, "handler_defined_after_registration")
    if function.decorator_list or handler.id in assignments:
        return outcome(BindingStatus.UNVERIFIABLE, "handler_wrapped_or_rebound")
    owner_imports = [n for n in tree.body if isinstance(n, ast.ImportFrom)
        and n.module == "tools.registry" and n.level == 0
        and any(a.name == "registry" and a.asname in (None,"registry") for a in n.names)]
    if len(owner_imports) != 1 or owner_imports[0].lineno >= call.lineno:
        return outcome(BindingStatus.UNVERIFIABLE, "registry_owner_not_proven")
    for statement in tree.body:
        if isinstance(statement, (ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
            if statement.name == "registry":
                return outcome(BindingStatus.UNVERIFIABLE, "registry_rebound")
            continue
        for node in ast.walk(statement):
            if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store,ast.Del)) and node.id in {"registry",handler.id}:
                return outcome(BindingStatus.UNVERIFIABLE, "binding_name_reassigned")
            if isinstance(node, (ast.Import,ast.ImportFrom)):
                for alias in node.names:
                    bound = alias.asname or alias.name.split('.')[0]
                    if alias.name == '*' or bound == handler.id or (bound == "registry" and node is not owner_imports[0]):
                        return outcome(BindingStatus.UNVERIFIABLE, "binding_import_ambiguous")
    try:
        schema = _field(keywords["schema"], "parameters", assignments)
        if not _admits(schema, declaration.selectors, assignments):
            return outcome(BindingStatus.CONTRADICTORY, "selector_not_declared")
    except (KeyError, _Unknown):
        return outcome(BindingStatus.UNVERIFIABLE, "schema_not_statically_resolved")
    def digest(node):
        return hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
    return outcome(BindingStatus.VERIFIED, "source_registration_corresponds",
        registry_import_line=owner_imports[0].lineno, registration_line=call.lineno, handler_line=function.lineno,
        handler_ast_sha256=digest(function), registration_ast_sha256=digest(call))
