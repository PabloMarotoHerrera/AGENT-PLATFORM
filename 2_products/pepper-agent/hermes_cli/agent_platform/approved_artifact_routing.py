"""Private isolated composition only. No env, tool, HTTP or config activation."""
from contextlib import contextmanager

from .approved_artifact_read_qualification import C93ReadQualificationOwner


@contextmanager
def _mechanical_read_route(*, isolated_repository, isolated_home):
    from .approved_artifact_inspection import _READ_ROUTE
    owner = C93ReadQualificationOwner(isolated_repository=isolated_repository, isolated_home=isolated_home)
    token = _READ_ROUTE.set(owner)
    try:
        yield owner
    finally:
        _READ_ROUTE.reset(token)
