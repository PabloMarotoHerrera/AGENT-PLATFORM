"""Read-only dashboard transport for AGENT PLATFORM product configuration."""

from fastapi import APIRouter

from hermes_cli.agent_platform.product_config import (
    ProductConfiguration,
    load_product_configuration,
)


router = APIRouter(prefix="/api/agent-platform", tags=["agent-platform"])


@router.get(
    "/product-configuration",
    response_model=ProductConfiguration,
    summary="Get validated AGENT PLATFORM product configuration",
)
def get_product_configuration() -> ProductConfiguration:
    """Return deterministic metadata without consulting user or provider state."""

    return load_product_configuration()
