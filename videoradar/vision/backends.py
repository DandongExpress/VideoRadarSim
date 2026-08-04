"""Optional vision backends (WHAM, etc.) — requires videoradar[vision]."""

from __future__ import annotations

from pathlib import Path

from videoradar.vision.mesh_recovery import MeshSequence, _synthetic_fallback


def recover_with_wham(
    video_path: str | Path,
    *,
    max_frames: int | None = None,
    fps: float = 30.0,
) -> MeshSequence:
    """
    Placeholder for WHAM-based mesh recovery.

    Install vision extras and provide model weights to enable this path.
    Until then, raises ImportError with setup instructions.
    """
    raise NotImplementedError(
        "WHAM backend is not yet wired in v0.1. "
        "Install videoradar[vision] and see docs/roadmap.md. "
        "The pipeline currently uses a synthetic capsule fallback."
    )
