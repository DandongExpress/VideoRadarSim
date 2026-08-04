"""PPPR-style Gaussian joint scatterers (placeholder for v0.3)."""

from __future__ import annotations

import numpy as np

from videoradar.scatter.triangle import ScattererSet


def joints_to_scatterers(
    joint_positions: np.ndarray,
    joint_velocities: np.ndarray | None = None,
    *,
    joint_rcs: float = 1.0,
) -> ScattererSet:
    """
    Represent each joint as a single isotropic scatterer.

    This is a lightweight placeholder aligned with PPPR's per-joint modeling.
    """
    n = joint_positions.shape[0]
    if joint_velocities is None:
        joint_velocities = np.zeros_like(joint_positions)
    rcs = np.full(n, joint_rcs, dtype=np.float64)
    return ScattererSet(
        positions=joint_positions.astype(np.float64),
        velocities=joint_velocities.astype(np.float64),
        rcs=rcs,
    )
