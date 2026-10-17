"""VideoRadarSim — physics-first video-to-mmWave simulation."""

from videoradar.pipeline import SimulationResult, simulate_from_mesh_sequence, simulate_from_video
from videoradar.radar.config import RadarProfile, load_radar_profile

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "RadarProfile",
    "load_radar_profile",
    "SimulationResult",
    "simulate_from_mesh_sequence",
    "simulate_from_video",
]



