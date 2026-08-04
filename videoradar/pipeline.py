"""End-to-end simulation pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from videoradar.export.toolbox import export_simulation_bundle
from videoradar.radar.config import RadarProfile, load_radar_profile
from videoradar.radar.dsp import range_angle_heatmap, range_doppler_map
from videoradar.radar.fmcw import synthesize_if_frame
from videoradar.scatter.triangle import mesh_to_scatterers
from videoradar.vision.mesh_recovery import MeshSequence, recover_mesh_from_video


@dataclass
class SimulationResult:
    """Container for one synthetic mmWave sequence."""

    heatmaps: np.ndarray  # (T, R, A)
    range_doppler_maps: np.ndarray  # (T, R, D)
    if_frames: list[np.ndarray]
    joint_positions: np.ndarray | None  # (T, J, 3) if available
    metadata: dict[str, Any] = field(default_factory=dict)


def simulate_from_mesh_sequence(
    mesh_sequence: MeshSequence,
    profile: RadarProfile | str,
    *,
    add_noise: bool = False,
    max_scatterers: int = 2000,
) -> SimulationResult:
    """Synthesize mmWave frames from a sequence of mesh frames."""
    if isinstance(profile, str):
        profile = load_radar_profile(profile)

    heatmaps: list[np.ndarray] = []
    rd_maps: list[np.ndarray] = []
    if_frames: list[np.ndarray] = []

    prev_vertices: np.ndarray | None = None
    fps = mesh_sequence.fps

    for frame in mesh_sequence.frames:
        vertex_vel = None
        if prev_vertices is not None:
            vertex_vel = (frame.vertices - prev_vertices) * fps
        prev_vertices = frame.vertices.copy()

        scatterers = mesh_to_scatterers(
            frame.vertices,
            frame.faces,
            vertex_vel,
            radar_position=profile.position,
            max_scatterers=max_scatterers,
        )
        if_data = synthesize_if_frame(scatterers, profile, add_noise=add_noise)
        heatmaps.append(range_angle_heatmap(if_data, profile))
        rd_maps.append(range_doppler_map(if_data, profile))
        if_frames.append(if_data)

    joints = None
    if all(f.joints is not None for f in mesh_sequence.frames):
        joints = np.stack([f.joints for f in mesh_sequence.frames], axis=0)

    return SimulationResult(
        heatmaps=np.stack(heatmaps, axis=0),
        range_doppler_maps=np.stack(rd_maps, axis=0),
        if_frames=if_frames,
        joint_positions=joints,
        metadata={
            "radar_profile": profile.to_dict(),
            "num_frames": len(mesh_sequence.frames),
            "fps": fps,
            "source": mesh_sequence.source,
        },
    )


def simulate_from_video(
    video_path: str | Path,
    profile: RadarProfile | str,
    *,
    output_dir: str | Path | None = None,
    max_frames: int | None = None,
    add_noise: bool = False,
) -> SimulationResult:
    """
    Full pipeline: video → mesh recovery → radar synthesis.

    Vision backends require optional `videoradar[vision]` dependencies.
    Falls back to a synthetic capsule motion sequence when video backend is unavailable.
    """
    mesh_sequence = recover_mesh_from_video(video_path, max_frames=max_frames)
    result = simulate_from_mesh_sequence(mesh_sequence, profile, add_noise=add_noise)

    if output_dir is not None:
        export_simulation_bundle(result, output_dir, profile_name=(
            profile if isinstance(profile, str) else profile.name
        ))

    return result
