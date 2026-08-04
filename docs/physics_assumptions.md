# Physics assumptions (MVP v0.1)

VideoRadarSim uses a **simplified physical model** intended for scalable synthetic data generation, not hardware-identical emulation.

## Human reflection model

- Human body represented as a triangle mesh (or joint scatterers in future PPPR mode).
- Each visible triangle contributes one scatterer at its centroid.
- Back-face culling removes triangles not facing the radar (no inter-body occlusion yet).
- Amplitude follows approximate path loss \( \propto 1/r^2 \) with quasi-specular orientation weighting.

## FMCW IF synthesis

- Beat frequency from round-trip delay: \( f_{beat} = S \cdot 2R/c \).
- Doppler from radial velocity: \( f_d = 2 v_r / \lambda \).
- MIMO phase from virtual antenna offsets (L-shaped array approximation).

## DSP

- Hann-windowed Range / Doppler / Angle FFTs.
- Range-Angle heatmap via Doppler max-projection (HuPR-style 2D map).

## Explicit simplifications

| Factor | MVP status |
|--------|------------|
| Multipath | Not modeled |
| Environment clutter | Not modeled |
| Material / Fresnel | Uniform body RCS |
| Antenna patterns | Isotropic |
| Hardware non-idealities | Optional noise floor only |
| Multi-person | Single subject |

These assumptions are documented so downstream users can interpret sim-to-real gaps correctly.
