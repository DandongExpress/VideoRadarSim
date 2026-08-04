"""Export formats compatible with RadarHPE-Toolbox and public datasets."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import yaml

from videoradar.pipeline import SimulationResult


def export_simulation_bundle(
    result: SimulationResult,
    output_dir: str | Path,
    *,
    profile_name: str = "ti_iwr1843boost",
    format_name: str = "toolbox",
) -> Path:
    """
    Write heatmaps, metadata, and optional pose GT to disk.

    Layout (RadarHPE-Toolbox friendly):
        output_dir/
          heatmaps/frame_XXXXXX.npy
          metadata.yaml
          poses_3d.npy  (if available)
    """
    output_dir = Path(output_dir)
    heatmap_dir = output_dir / "heatmaps"
    heatmap_dir.mkdir(parents=True, exist_ok=True)

    for i, hm in enumerate(result.heatmaps):
        np.save(heatmap_dir / f"frame_{i:06d}.npy", hm.astype(np.float32))

    meta = {
        "format": format_name,
        "radar_profile": profile_name,
        "num_frames": int(result.heatmaps.shape[0]),
        "heatmap_shape": list(result.heatmaps.shape[1:]),
        **result.metadata,
    }
    with (output_dir / "metadata.yaml").open("w", encoding="utf-8") as f:
        yaml.safe_dump(meta, f, sort_keys=False)

    if result.joint_positions is not None:
        np.save(output_dir / "poses_3d.npy", result.joint_positions.astype(np.float32))

    manifest = {
        "heatmap_files": [f"heatmaps/frame_{i:06d}.npy" for i in range(result.heatmaps.shape[0])],
        "metadata": "metadata.yaml",
    }
    with (output_dir / "manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return output_dir


def load_toolbox_heatmap_sequence(data_dir: str | Path) -> np.ndarray:
    """Load exported heatmap sequence (T, R, A)."""
    data_dir = Path(data_dir)
    files = sorted((data_dir / "heatmaps").glob("frame_*.npy"))
    if not files:
        raise FileNotFoundError(f"No heatmaps found in {data_dir / 'heatmaps'}")
    return np.stack([np.load(f) for f in files], axis=0)
