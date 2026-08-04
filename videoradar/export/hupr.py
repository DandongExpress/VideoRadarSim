"""HuPR-format export helpers."""

from __future__ import annotations

from pathlib import Path

from videoradar.export.toolbox import export_simulation_bundle
from videoradar.pipeline import SimulationResult


def export_hupr_style(result: SimulationResult, output_dir: str | Path) -> Path:
    """Export with HuPR-oriented metadata defaults."""
    return export_simulation_bundle(
        result,
        output_dir,
        profile_name="ti_iwr1843boost",
        format_name="hupr",
    )
