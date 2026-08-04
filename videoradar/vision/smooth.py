"""Temporal smoothing for mesh sequences."""

from __future__ import annotations

import numpy as np
from scipy.signal import savgol_filter

from videoradar.vision.mesh_recovery import MeshSequence


def savgol_smooth_vertices(
    sequence: MeshSequence,
    *,
    window_length: int = 9,
    polyorder: int = 2,
) -> MeshSequence:
    """Apply Savitzky-Golay smoothing along time for each vertex coordinate."""
    if len(sequence.frames) < window_length:
        return sequence

    verts = np.stack([f.vertices for f in sequence.frames], axis=0)  # (T, V, 3)
    smoothed = np.zeros_like(verts)
    for v in range(verts.shape[1]):
        for c in range(3):
            smoothed[:, v, c] = savgol_filter(
                verts[:, v, c],
                window_length=window_length,
                polyorder=polyorder,
            )

    from videoradar.vision.mesh_recovery import MeshFrame

    frames = [
        MeshFrame(vertices=smoothed[t], faces=sequence.frames[t].faces, joints=sequence.frames[t].joints)
        for t in range(len(sequence.frames))
    ]
    return MeshSequence(frames=frames, fps=sequence.fps, source=sequence.source + "+savgol")
