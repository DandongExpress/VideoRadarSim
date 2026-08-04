#!/usr/bin/env python3
"""Phase-0 demo: synthetic mesh → Range-Angle heatmap (no video)."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from videoradar.mesh.synth import animate_capsule_wave, make_capsule_mesh
from videoradar.pipeline import simulate_from_mesh_sequence
from videoradar.vision.mesh_recovery import MeshFrame, MeshSequence


def main() -> None:
    base_verts, faces = make_capsule_mesh()
    offset = np.array([0.0, 2.0, 0.0])
    frames = []
    for t in range(20):
        verts, _ = animate_capsule_wave(base_verts, faces, t)
        frames.append(MeshFrame(vertices=verts + offset, faces=faces))

    sequence = MeshSequence(frames=frames, fps=30.0, source="demo_single_frame")
    result = simulate_from_mesh_sequence(sequence, "ti_iwr1843boost")

    out = Path("outputs")
    out.mkdir(exist_ok=True)
    hm = result.heatmaps[10]
    plt.figure(figsize=(8, 4))
    plt.imshow(hm, aspect="auto", origin="lower", cmap="hot")
    plt.xlabel("Azimuth bin")
    plt.ylabel("Range bin")
    plt.title("Synthetic Range-Angle Heatmap (frame 10)")
    plt.colorbar(label="Magnitude")
    plt.tight_layout()
    save_path = out / "demo_ra_heatmap.png"
    plt.savefig(save_path, dpi=150)
    print(f"Saved {save_path}, heatmap shape={hm.shape}")


if __name__ == "__main__":
    main()
