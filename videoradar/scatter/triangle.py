"""Scatterer extraction from triangle meshes."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from videoradar.scatter.visibility import filter_visible_faces


@dataclass
class ScattererSet:
    """Radar scatterers derived from a surface mesh."""

    positions: np.ndarray  # (N, 3)
    velocities: np.ndarray  # (N, 3)
    rcs: np.ndarray  # (N,) relative radar cross-section


def mesh_to_scatterers(
    vertices: np.ndarray,
    faces: np.ndarray,
    vertex_velocities: np.ndarray | None = None,
    *,
    radar_position: np.ndarray | None = None,
    max_scatterers: int = 2000,
    specular_width: float = 0.3,
    body_rcs: float = 1.0,
) -> ScattererSet:
    """
    Convert a triangle mesh to radar scatterers at triangle centroids.

    Parameters
    ----------
    vertices : (V, 3) mesh vertices at one time step
    faces : (F, 3) triangle indices
    vertex_velocities : optional (V, 3) per-vertex velocity
    radar_position : (3,) for visibility and orientation weighting
    """
    if radar_position is None:
        radar_position = np.zeros(3, dtype=np.float64)

    visible_faces, normals = filter_visible_faces(vertices, faces, radar_position)
    if visible_faces.shape[0] == 0:
        return ScattererSet(
            positions=np.zeros((0, 3), dtype=np.float64),
            velocities=np.zeros((0, 3), dtype=np.float64),
            rcs=np.zeros(0, dtype=np.float64),
        )

    tri_verts = vertices[visible_faces]  # (F, 3, 3)
    centroids = tri_verts.mean(axis=1)
    areas = _triangle_areas(tri_verts)

    # Quasi-specular orientation weighting (mmGen-style Gaussian lobe)
    to_radar = radar_position - centroids
    to_radar /= np.linalg.norm(to_radar, axis=1, keepdims=True) + 1e-9
    cos_alpha = np.abs(np.sum(normals * to_radar, axis=1))
    orientation_weight = np.exp(-((1.0 - cos_alpha) ** 2) / (2.0 * specular_width**2))

    rcs = body_rcs * areas * orientation_weight

    if vertex_velocities is not None:
        v0 = vertex_velocities[visible_faces[:, 0]]
        v1 = vertex_velocities[visible_faces[:, 1]]
        v2 = vertex_velocities[visible_faces[:, 2]]
        velocities = (v0 + v1 + v2) / 3.0
    else:
        velocities = np.zeros_like(centroids)

    if centroids.shape[0] > max_scatterers:
        order = np.argsort(rcs)[::-1][:max_scatterers]
        centroids = centroids[order]
        velocities = velocities[order]
        rcs = rcs[order]

    return ScattererSet(
        positions=centroids.astype(np.float64),
        velocities=velocities.astype(np.float64),
        rcs=rcs.astype(np.float64),
    )


def _triangle_areas(tri_verts: np.ndarray) -> np.ndarray:
    e1 = tri_verts[:, 1] - tri_verts[:, 0]
    e2 = tri_verts[:, 2] - tri_verts[:, 0]
    cross = np.cross(e1, e2)
    return 0.5 * np.linalg.norm(cross, axis=1)
