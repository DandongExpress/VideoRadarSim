"""FMCW intermediate-frequency (IF) signal synthesis from scatterers."""

from __future__ import annotations

import numpy as np

from videoradar.radar.config import RadarProfile
from videoradar.radar.mimo import array_phase
from videoradar.scatter.triangle import ScattererSet


def synthesize_if_frame(
    scatterers: ScattererSet,
    profile: RadarProfile,
    *,
    add_noise: bool = False,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """
    Synthesize one radar frame of complex IF data.

    Returns
    -------
    if_data : (num_chirps, num_rx, num_adc_samples) complex64
        Slow-time × RX × fast-time ADC samples.
    """
    if rng is None:
        rng = np.random.default_rng()

    n_chirps = profile.num_chirps
    n_rx = profile.rx_antennas
    n_adc = profile.num_adc_samples
    dt = 1.0 / profile.sample_rate
    t_fast = np.arange(n_adc, dtype=np.float64) * dt

    if_data = np.zeros((n_chirps, n_rx, n_adc), dtype=np.complex64)

    if scatterers.positions.shape[0] == 0:
        return if_data

    radar_pos = profile.position
    rel = scatterers.positions - radar_pos
    ranges = np.linalg.norm(rel, axis=1)
    ranges = np.maximum(ranges, 1e-3)

    # Radial velocity toward radar (+ = approaching)
    direction = rel / ranges[:, None]
    radial_vel = np.sum(scatterers.velocities * direction, axis=1)

    slope = profile.chirp_slope
    tau = 2.0 * ranges / 3e8
    f_beat = slope * tau
    f_doppler = 2.0 * radial_vel / profile.wavelength

    # Round-trip path loss ~ 1/r^2 amplitude (power ~ 1/r^4)
    amplitude = scatterers.rcs * np.sqrt(profile.wavelength) / (ranges**2)
    amplitude = amplitude / (np.max(amplitude) + 1e-12)

    pri = profile.chirp_duration

    for chirp_idx in range(n_chirps):
        t_slow = chirp_idx * pri
        doppler_phase = 2.0 * np.pi * f_doppler * t_slow

        for rx_idx in range(n_rx):
            virt_ant = rx_idx % profile.num_virtual_antennas
            ant_phase = array_phase(profile, scatterers.positions, virt_ant)

            for i in range(scatterers.positions.shape[0]):
                phase = (
                    2.0 * np.pi * (profile.fc * tau[i] + f_beat[i] * t_fast)
                    + doppler_phase[i]
                    + np.angle(ant_phase[i])
                )
                if_data[chirp_idx, rx_idx, :] += amplitude[i] * np.exp(1j * phase).astype(
                    np.complex64
                )

    if add_noise:
        noise_power = 10 ** (profile.noise_floor_db / 10.0)
        noise = (
            rng.normal(scale=np.sqrt(noise_power / 2), size=if_data.shape)
            + 1j * rng.normal(scale=np.sqrt(noise_power / 2), size=if_data.shape)
        )
        if_data = if_data + noise.astype(np.complex64)

    return if_data
