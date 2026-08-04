# Roadmap

## v0.1 (current) — Phase 0/1 MVP

- [x] Triangle-mesh scatterer model + back-face culling
- [x] FMCW IF synthesis + Range/Doppler/Angle FFT
- [x] TI radar profiles (IWR1843, IWR6843, AWR2243)
- [x] Synthetic capsule demo pipeline
- [x] Toolbox-oriented export bundle
- [x] CLI: `videoradar demo-mesh`, `videoradar simulate`

## v0.2 — Video + environment

- [ ] WHAM / 4D-Humans mesh recovery backend
- [ ] Savitzky-Golay temporal smoothing on SMPL parameters
- [ ] Simple box-room static clutter mesh
- [ ] HRPP-style first-order multipath (mmGen-inspired)
- [ ] Batch dataset generation script
- [ ] RadarHPE-Toolbox `synthetic_hupr` dataset loader PR

## v0.3 — Research integration

- [ ] PPPR Gaussian joint scatterer mode
- [ ] Differentiable radar forward (align with PPPR paper)
- [ ] Optional neural refiner (sim-to-real)
- [ ] Multi-person tracking
- [ ] Gradio / web demo

## v0.4 — Ecosystem

- [ ] Real-vs-synthetic benchmark report on HuPR subset
- [ ] Pretrained model augmentation recipes (PULSE / PPPR)
- [ ] CI GPU smoke tests
