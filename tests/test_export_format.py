"""Tests for export format."""

from __future__ import annotations

import numpy as np

from videoradar.export.toolbox import export_simulation_bundle, load_toolbox_heatmap_sequence
from videoradar.pipeline import SimulationResult


def test_export_and_reload_roundtrip(tmp_path) -> None:
    result = SimulationResult(
        heatmaps=np.random.rand(5, 64, 32).astype(np.float32),
        range_doppler_maps=np.random.rand(5, 64, 128).astype(np.float32),
        if_frames=[],
        joint_positions=None,
        metadata={"source": "test"},
    )
    out = export_simulation_bundle(result, tmp_path, profile_name="ti_iwr1843boost")
    loaded = load_toolbox_heatmap_sequence(out)
    assert loaded.shape == result.heatmaps.shape
    assert np.allclose(loaded, result.heatmaps)
