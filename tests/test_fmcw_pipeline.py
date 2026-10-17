"""Tests for FMCW synthesis and DSP pipeline."""

from __future__ import annotations

import numpy as np




from videoradar.mesh.synth import make_capsule_mesh
from videoradar.radar.config import load_radar_profile
from videoradar.radar.dsp import range_angle_heatmap
from videoradar.radar.fmcw import synthesize_if_frame
from videoradar.scatter.triangle import mesh_to_scatterers


def test_point_target_produces_peak_in_range_spectrum() -> None:
    profile = load_radar_profile("ti_iwr1843boost")
    # Small triangle ~2m in front of radar
    verts = np.array(
        [
            [-0.1, 2.0, -0.1],
            [0.1, 2.0, -0.1],
            [0.0, 2.0, 0.1],
        ],
        dtype=np.float64,
    )
    faces = np.array([[0, 1, 2]], dtype=np.int32)
    scatterers = mesh_to_scatterers(verts, faces, radar_position=profile.position)
    if_data = synthesize_if_frame(scatterers, profile, add_noise=False)
    assert if_data.shape == (profile.num_chirps, profile.rx_antennas, profile.num_adc_samples)
    assert np.abs(if_data).sum() > 0


def test_mesh_to_heatmap_pipeline() -> None:
    profile = load_radar_profile("ti_iwr1843boost")
    verts, faces = make_capsule_mesh()
    verts = verts + np.array([0.0, 2.0, 0.0])
    scatterers = mesh_to_scatterers(verts, faces, radar_position=profile.position)
    if_data = synthesize_if_frame(scatterers, profile)
    heatmap = range_angle_heatmap(if_data, profile)
    assert heatmap.ndim == 2
    assert heatmap.shape[0] > 0 and heatmap.shape[1] > 0
    assert np.isfinite(heatmap).all()
    assert heatmap.max() > 0


def test_radar_profile_loads() -> None:
    for name in ("ti_iwr1843boost", "ti_iwr6843isk", "ti_awr2243"):
        p = load_radar_profile(name)
        assert p.fc > 0
        assert p.bandwidth > 0
        assert p.num_chirps >= 1
