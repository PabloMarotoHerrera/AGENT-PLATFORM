"""Safe inert rendering APIs for AGENT PLATFORM MVP-0.

Importing this package performs no runtime initialization, reads no files,
writes no files, executes no commands, calls no network, activates no MCP,
executes no harness, and mutates no Git.
"""

from .contracts import (
    CompactWorkPacket,
    HarnessInputPackage,
    RenderFormat,
    RenderResult,
    RenderSafetyPosture,
    RenderedPackage,
    RendererConfig,
)
from .harness_input_renderer import render_harness_input_package
from .workpacket_renderer import render_compact_workpacket

__all__ = (
    "CompactWorkPacket",
    "HarnessInputPackage",
    "RenderFormat",
    "RenderResult",
    "RenderSafetyPosture",
    "RenderedPackage",
    "RendererConfig",
    "render_compact_workpacket",
    "render_harness_input_package",
)
