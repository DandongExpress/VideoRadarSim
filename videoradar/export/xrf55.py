"""XRF55-format export helpers (placeholder)."""

from __future__ import annotations

from pathlib import Path

from videoradar.export.toolbox import export_simulation_bundle
from videoradar.pipeline import SimulationResult


def export_xrf55_style(result: SimulationResult, output_dir: str | Path) -> Path:
    return export_simulation_bundle(
        result,
        output_dir,
        profile_name="ti_iwr6843isk",
        format_name="xrf55",
    )
