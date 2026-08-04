"""Synthetic mesh utilities for demos and unit tests."""

from __future__ import annotations

import numpy as np


def make_capsule_mesh(
    length: float = 1.7,
    radius: float = 0.18,
    *,
    n_rings: int = 12,
    n_segments: int = 16,
) -> tuple[np.ndarray, np.ndarray]:
    """Create a simple upright capsule (human proxy) centered at origin."""
    vertices: list[np.ndarray] = []
    faces: list[np.ndarray] = []

    # Cylinder body
    for i in range(n_rings + 1):
        z = -length / 2 + (length * i) / n_rings
        for j in range(n_segments):
            theta = 2.0 * np.pi * j / n_segments
            x = radius * np.cos(theta)
            y = radius * np.sin(theta)
            vertices.append([x, y, z])

    def idx(ring: int, seg: int) -> int:
        return ring * n_segments + seg

    for ring in range(n_rings):
        for seg in range(n_segments):
            s1 = (seg + 1) % n_segments
            v00 = idx(ring, seg)
            v01 = idx(ring, s1)
            v10 = idx(ring + 1, seg)
            v11 = idx(ring + 1, s1)
            faces.append([v00, v10, v01])
            faces.append([v01, v10, v11])

    return np.asarray(vertices, dtype=np.float64), np.asarray(faces, dtype=np.int32)


def animate_capsule_wave(
    vertices: np.ndarray,
    faces: np.ndarray,
    frame_index: int,
    *,
    fps: float = 30.0,
    amplitude: float = 0.08,
) -> tuple[np.ndarray, np.ndarray]:
    """Apply a simple sinusoidal arm-swing motion for temporal testing."""
    t = frame_index / fps
    verts = vertices.copy()
    z = verts[:, 2]
    mask = (z > 0.3) & (np.abs(verts[:, 0]) > 0.05)
    verts[mask, 0] += amplitude * np.sin(2.0 * np.pi * 0.5 * t) * (z[mask] - 0.3)

    prev_verts = vertices.copy()
    prev_verts[mask, 0] += amplitude * np.sin(2.0 * np.pi * 0.5 * (t - 1.0 / fps)) * (
        z[mask] - 0.3
    )
    velocities = (verts - prev_verts) * fps
    velocities = np.broadcast_to(velocities, verts.shape).copy()
    return verts, velocities
