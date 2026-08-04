"""MIMO virtual array geometry and phase modeling."""

from __future__ import annotations

import numpy as np

from videoradar.radar.config import RadarProfile


def virtual_antenna_offsets(profile: RadarProfile) -> np.ndarray:
    """Return (V, 3) offsets for virtual antennas in wavelength units (az, el, 0)."""
    v = profile.num_virtual_antennas
    lam = profile.wavelength
    d_az = profile.azimuth_spacing * lam
    d_el = profile.elevation_spacing * lam

    offsets = np.zeros((v, 3), dtype=np.float64)
    for tx in range(profile.tx_antennas):
        for rx in range(profile.rx_antennas):
            idx = tx * profile.rx_antennas + rx
            offsets[idx, 0] = rx * d_az + tx * d_az * 0.5
            offsets[idx, 1] = tx * d_el
    return offsets


def array_phase(
    profile: RadarProfile,
    points: np.ndarray,
    antenna_index: int,
) -> np.ndarray:
    """
    Compute exp(j * 2π/λ * r·u) phase for each scatterer point.

    Parameters
    ----------
    points : (N, 3) scatterer positions in world frame
    antenna_index : virtual antenna index
    """
    offsets = virtual_antenna_offsets(profile)
    radar_pos = profile.position
    rel = points - radar_pos
    dist = np.linalg.norm(rel, axis=1, keepdims=True)
    dist = np.maximum(dist, 1e-6)
    direction = rel / dist

    u = offsets[antenna_index]
    phase = 2.0 * np.pi / profile.wavelength * (direction @ u)
    return np.exp(1j * phase)
