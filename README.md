# VideoRadarSim

**From video to trainable mmWave data — physics-first, toolbox-ready.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](pyproject.toml)

VideoRadarSim is an open-source pipeline that synthesizes **mmWave FMCW radar signals** (Range-Angle-Doppler heatmaps) from human motion, starting from **RGB video** or **3D mesh sequences**. It is designed as a companion project to [RadarHPE-Toolbox](https://github.com/DandongExpress/RadarHPE-Toolbox) for privacy-preserving human pose estimation research.

> **Status:** v0.1 alpha — core physics pipeline works; video→SMPL backend coming in v0.2.

## Why

Real mmWave datasets are expensive to collect. Existing simulators are fragmented (Doppler-only, depth-camera dependent, or paper-specific). VideoRadarSim provides:

- A **unified** video/mesh → heatmap pipeline
- **Physics-guided** FMCW synthesis (not black-box only)
- **RadarHPE-Toolbox** compatible export
- Built-in TI radar profiles (HuPR / XRF55 / MMVR)

## Quick start

```bash
git clone https://github.com/DandongExpress/VideoRadarSim.git
cd VideoRadarSim
pip install -e .

# Demo without video or GPU
videoradar demo-mesh --frames 30 -o outputs/demo
```

## Python API

```python
from videoradar import simulate_from_video

result = simulate_from_video(
    "walk.mp4",
    radar_profile="ti_iwr1843boost",
    output_dir="synthetic/hupr/",
)
# result.heatmaps: (T, R, A)
```

## Architecture

```
Video / Mesh → Vision (SMPL) → Scatterers → FMCW IF → FFT → Heatmap → Export
```

| Module | Description |
|--------|-------------|
| `videoradar.vision` | Video → mesh recovery (WHAM planned) |
| `videoradar.scatter` | Mesh → radar scatterers |
| `videoradar.radar` | FMCW synthesis + DSP |
| `videoradar.export` | RadarHPE-Toolbox bundle export |

See [docs/physics_assumptions.md](docs/physics_assumptions.md) and [docs/roadmap.md](docs/roadmap.md).

## Related projects

- [RadarHPE-Toolbox](https://github.com/DandongExpress/RadarHPE-Toolbox) — unified training/eval for mmWave HPE
- [PPPR](https://github.com/DandongExpress/PPPR) — physics-informed representation (UbiComp/IMWUT 2026)
- [PULSE](https://github.com/DandongExpress/Doppler-Prompting-for-Stable-mmWave-based-Human-Pose-Estimation) — Doppler prompting (ICML 2026)

## Citation

If you use VideoRadarSim, please cite the corresponding method papers when using their radar models, and star both this repo and RadarHPE-Toolbox.

## License

MIT — see [LICENSE](LICENSE).
