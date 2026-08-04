# Tutorials

## Install

```bash
git clone https://github.com/DandongExpress/VideoRadarSim.git
cd VideoRadarSim
pip install -e .
# Optional: pip install -e ".[dev]"
```

## 1. Quick demo (no video, no GPU)

```bash
videoradar demo-mesh --frames 30 --output outputs/demo
```

This runs: synthetic capsule mesh → FMCW IF → Range-Angle heatmaps → `outputs/demo/`.

## 2. Python API

```python
from videoradar import simulate_from_mesh_sequence, load_radar_profile
from videoradar.mesh.synth import make_capsule_mesh, animate_capsule_wave
from videoradar.vision.mesh_recovery import MeshFrame, MeshSequence

verts, faces = make_capsule_mesh()
frames = []
for t in range(30):
    v, _ = animate_capsule_wave(verts, faces, t)
    frames.append(MeshFrame(vertices=v + [0, 2, 0], faces=faces))

result = simulate_from_mesh_sequence(
    MeshSequence(frames=frames, fps=30, source="tutorial"),
    load_radar_profile("ti_iwr1843boost"),
)
print(result.heatmaps.shape)  # (T, range_bins, angle_bins)
```

## 3. Video pipeline (v0.1 fallback)

```bash
videoradar simulate path/to/video.mp4 -o outputs/sim --max-frames 60
```

Without vision extras, this uses the synthetic capsule fallback but preserves the same export format.

## 4. RadarHPE-Toolbox integration

Exported bundles can be loaded manually:

```python
from videoradar.export.toolbox import load_toolbox_heatmap_sequence
heatmaps = load_toolbox_heatmap_sequence("outputs/demo")
```

A native Toolbox loader is planned in v0.2 — see [RadarHPE-Toolbox](https://github.com/DandongExpress/RadarHPE-Toolbox).

## 5. List radar profiles

```bash
videoradar list-profiles
```

Profiles: `ti_iwr1843boost` (HuPR), `ti_iwr6843isk` (XRF55), `ti_awr2243` (MMVR).
