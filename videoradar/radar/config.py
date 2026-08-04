"""Radar configuration and profile loading."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import yaml

_PROFILES_DIR = Path(__file__).parent / "profiles"


@dataclass
class RadarProfile:
    """FMCW MIMO radar configuration aligned with common TI mmWave setups."""

    name: str
    fc: float
    bandwidth: float
    chirp_duration: float
    num_chirps: int
    num_adc_samples: int
    sample_rate: float
    tx_antennas: int
    rx_antennas: int
    tx_power_dbm: float = 12.0
    # Radar position in world frame (meters)
    position: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))
    # L-shaped virtual array spacing (wavelength fractions)
    azimuth_spacing: float = 0.5
    elevation_spacing: float = 0.5
    fft_config: str = "3d_unified"
    range_max: float = 5.0
    azimuth_fov_deg: float = 120.0
    elevation_fov_deg: float = 30.0
    noise_floor_db: float = -80.0

    @property
    def wavelength(self) -> float:
        return 3e8 / self.fc

    @property
    def chirp_slope(self) -> float:
        return self.bandwidth / self.chirp_duration

    @property
    def range_resolution(self) -> float:
        return 3e8 / (2.0 * self.bandwidth)

    @property
    def velocity_max(self) -> float:
        pri = self.chirp_duration
        return self.wavelength / (4.0 * pri)

    @property
    def num_virtual_antennas(self) -> int:
        return self.tx_antennas * self.rx_antennas

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "fc": self.fc,
            "bandwidth": self.bandwidth,
            "chirp_duration": self.chirp_duration,
            "num_chirps": self.num_chirps,
            "num_adc_samples": self.num_adc_samples,
            "sample_rate": self.sample_rate,
            "tx_antennas": self.tx_antennas,
            "rx_antennas": self.rx_antennas,
            "tx_power_dbm": self.tx_power_dbm,
            "position": self.position.tolist(),
            "azimuth_spacing": self.azimuth_spacing,
            "elevation_spacing": self.elevation_spacing,
            "fft_config": self.fft_config,
            "range_max": self.range_max,
            "azimuth_fov_deg": self.azimuth_fov_deg,
            "elevation_fov_deg": self.elevation_fov_deg,
            "noise_floor_db": self.noise_floor_db,
        }


def load_radar_profile(name_or_path: str | Path) -> RadarProfile:
    """Load a built-in profile by name or a custom YAML file path."""
    path = Path(name_or_path)
    if not path.suffix:
        path = _PROFILES_DIR / f"{name_or_path}.yaml"
    if not path.exists():
        available = sorted(p.stem for p in _PROFILES_DIR.glob("*.yaml"))
        raise FileNotFoundError(
            f"Radar profile '{name_or_path}' not found. Available: {available}"
        )

    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    position = np.asarray(data.pop("position", [0.0, 0.0, 0.0]), dtype=np.float64)
    name = data.pop("name", path.stem)
    return RadarProfile(name=name, position=position, **data)
