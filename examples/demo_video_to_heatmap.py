#!/usr/bin/env python3
"""Full pipeline demo (uses synthetic fallback when vision backend unavailable)."""

from pathlib import Path

from videoradar import simulate_from_video


def main() -> None:
    # Any path works in v0.1 — vision backend falls back to synthetic capsule motion
    video = Path("examples/placeholder.mp4")
    output = Path("outputs/video_sim")
    result = simulate_from_video(
        video,
        "ti_iwr1843boost",
        output_dir=output,
        max_frames=30,
    )
    print(f"Simulated {result.heatmaps.shape[0]} frames → {output}")
    print(f"Heatmap shape: {result.heatmaps.shape}")
    print(f"Source: {result.metadata.get('source')}")


if __name__ == "__main__":
    main()
