"""Mesh visibility filtering for radar line-of-sight."""

from __future__ import annotations

import numpy as np


def filter_visible_faces(
    vertices: np.ndarray,
    faces: np.ndarray,
    radar_position: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Back-face culling: keep triangles whose normals face the radar.

    Returns visible face indices and unit normals.
    """
    tri_verts = vertices[faces]
    v0, v1, v2 = tri_verts[:, 0], tri_verts[:, 1], tri_verts[:, 2]
    normals = np.cross(v1 - v0, v2 - v0)
    norm_len = np.linalg.norm(normals, axis=1, keepdims=True)
    norm_len = np.maximum(norm_len, 1e-9)
    normals = normals / norm_len

    centroids = tri_verts.mean(axis=1)
    view_dirs = radar_position - centroids
    view_dirs /= np.linalg.norm(view_dirs, axis=1, keepdims=True) + 1e-9

    visible = np.sum(normals * view_dirs, axis=1) > 0.0
    return faces[visible], normals[visible]
