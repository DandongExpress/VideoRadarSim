"""Video → 3D mesh recovery (with optional vision backends)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from videoradar.mesh.synth import animate_capsule_wave, make_capsule_mesh


@dataclass
class MeshFrame:
    vertices: np.ndarray  # (V, 3)
    faces: np.ndarray  # (F, 3)
    joints: np.ndarray | None = None  # (J, 3)


@dataclass
class MeshSequence:
    frames: list[MeshFrame]
    fps: float = 30.0
    source: str = "unknown"


def recover_mesh_from_video(
    video_path: str | Path,
    *,
    max_frames: int | None = 60,
    fps: float = 30.0,
) -> MeshSequence:
    """
    Recover per-frame SMPL-like meshes from video.

    MVP: uses a synthetic capsule sequence when no vision backend is installed.
    Future: WHAM / 4D-Humans integration via `videoradar[vision]`.
    """
    video_path = Path(video_path)
    backend = _try_load_vision_backend()
    if backend is not None:
        return backend(video_path, max_frames=max_frames, fps=fps)

    return _synthetic_fallback(video_path, max_frames=max_frames or 60, fps=fps)


def _try_load_vision_backend():
    try:
        from videoradar.vision.backends import recover_with_wham  # noqa: F401

        return recover_with_wham
    except ImportError:
        return None


def _synthetic_fallback(
    video_path: Path,
    *,
    max_frames: int,
    fps: float,
) -> MeshSequence:
    """Deterministic capsule animation for pipeline testing without GPU vision models."""
    base_verts, faces = make_capsule_mesh()
    # Place human ~2m in front of radar at z=0, facing radar at origin
    offset = np.array([0.0, 2.0, 0.0], dtype=np.float64)

    frames: list[MeshFrame] = []
    for t in range(max_frames):
        verts, _ = animate_capsule_wave(base_verts, faces, t, fps=fps)
        verts = verts + offset
        frames.append(MeshFrame(vertices=verts, faces=faces))

    return MeshSequence(
        frames=frames,
        fps=fps,
        source=f"synthetic_capsule (video={video_path.name})",
    )
