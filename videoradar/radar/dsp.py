"""Range-Doppler-Angle DSP pipeline for FMCW radar."""

from __future__ import annotations

import numpy as np
from scipy.signal import windows

from videoradar.radar.config import RadarProfile


def range_fft(if_data: np.ndarray, profile: RadarProfile) -> np.ndarray:
    """Fast-time FFT → (chirps, rx, range_bins)."""
    win = windows.hann(if_data.shape[-1], sym=False)
    windowed = if_data * win[None, None, :]
    return np.fft.fft(windowed, axis=-1)


def doppler_fft(range_data: np.ndarray) -> np.ndarray:
    """Slow-time FFT → (doppler_bins, rx, range_bins)."""
    win = windows.hann(range_data.shape[0], sym=False)
    windowed = range_data * win[:, None, None]
    return np.fft.fftshift(np.fft.fft(windowed, axis=0), axes=0)


def angle_fft(doppler_data: np.ndarray, profile: RadarProfile) -> np.ndarray:
    """Virtual-array FFT along RX dimension → (doppler, angle, range)."""
    n_virt = profile.num_virtual_antennas
    n_rx = doppler_data.shape[1]
    if n_rx < n_virt:
        padded = np.zeros(
            (doppler_data.shape[0], n_virt, doppler_data.shape[2]),
            dtype=doppler_data.dtype,
        )
        padded[:, :n_rx, :] = doppler_data
        doppler_data = padded

    win = windows.hann(doppler_data.shape[1], sym=False)
    windowed = doppler_data * win[None, :, None]
    angle_spectrum = np.fft.fftshift(np.fft.fft(windowed, axis=1), axes=1)
    return angle_spectrum


def range_angle_heatmap(
    if_data: np.ndarray,
    profile: RadarProfile,
    *,
    collapse_doppler: bool = True,
) -> np.ndarray:
    """
    Produce a magnitude Range-Angle heatmap (R × A).

    Typical HPE datasets use 2D RA maps after Doppler integration.
    """
    range_spec = range_fft(if_data, profile)
    doppler_spec = doppler_fft(range_spec)
    angle_spec = angle_fft(doppler_spec, profile)

    magnitude = np.abs(angle_spec)
    if collapse_doppler:
        magnitude = np.max(magnitude, axis=0)  # (angle, range)
    else:
        magnitude = np.transpose(magnitude, (1, 0, 2))  # (angle, doppler, range)

    # Transpose to (range, angle) for HuPR-like layouts
    if collapse_doppler:
        return magnitude.T
    return magnitude


def range_doppler_map(if_data: np.ndarray, profile: RadarProfile) -> np.ndarray:
    """Magnitude Range-Doppler map averaged over RX antennas."""
    range_spec = range_fft(if_data, profile)
    doppler_spec = doppler_fft(range_spec)
    magnitude = np.abs(doppler_spec).mean(axis=1)  # (doppler, range)
    return magnitude.T


def cfar_point_cloud(
    heatmap: np.ndarray,
    *,
    threshold_percentile: float = 95.0,
    max_points: int = 512,
) -> np.ndarray:
    """
    Simple CFAR-like peak extraction from a 2D heatmap.

    Returns (N, 3) as (range_idx, angle_idx, magnitude).
    """
    thresh = np.percentile(heatmap, threshold_percentile)
    mask = heatmap >= thresh
    r_idx, a_idx = np.where(mask)
    mags = heatmap[r_idx, a_idx]
    order = np.argsort(mags)[::-1][:max_points]
    points = np.stack([r_idx[order], a_idx[order], mags[order]], axis=1)
    return points.astype(np.float32)
