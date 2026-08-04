# Limitations (v0.1)

## Vision module

- **Video → SMPL** is not fully integrated. Without `videoradar[vision]` backends, the pipeline uses a **synthetic capsule** motion sequence.
- WHAM / 4D-Humans integration is planned (see `docs/roadmap.md`).

## Physical fidelity

- Synthetic heatmaps will **not** match real TI radar captures pixel-wise.
- Suitable for: algorithm prototyping, pre-training exploration, teaching radar signal flow, Toolbox integration tests.
- Not suitable for: claiming SOTA on real benchmarks without real-data fine-tuning.

## Performance

- Triangle-mesh scatterers are capped (`max_scatterers=2000` by default).
- No GPU acceleration in v0.1; long videos should use `--max-frames`.

## Format compatibility

- Export layout is **RadarHPE-Toolbox oriented** but not yet a registered `create_dataset('synthetic')` loader.
- HuPR/XRF55 exact tensor shapes may require resizing in a future release.
