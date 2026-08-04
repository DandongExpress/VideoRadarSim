"""Command-line interface for VideoRadarSim."""

from __future__ import annotations

from pathlib import Path

import typer
from rich import print as rprint

from videoradar.mesh.synth import animate_capsule_wave, make_capsule_mesh
from videoradar.pipeline import simulate_from_mesh_sequence, simulate_from_video
from videoradar.radar.config import load_radar_profile
from videoradar.vision.mesh_recovery import MeshFrame, MeshSequence

app = typer.Typer(
    name="videoradar",
    help="Physics-first video-to-mmWave radar simulation for HPE research.",
    add_completion=False,
)


@app.command("simulate")
def simulate(
    video: Path = typer.Argument(..., help="Input video path (or placeholder for synthetic demo)"),
    output: Path = typer.Option(Path("outputs/sim"), "--output", "-o", help="Output directory"),
    profile: str = typer.Option("ti_iwr1843boost", "--profile", "-p", help="Radar profile name or YAML path"),
    max_frames: int = typer.Option(60, "--max-frames", help="Maximum frames to simulate"),
    noise: bool = typer.Option(False, "--noise", help="Add thermal noise to IF data"),
) -> None:
    """Run video → mesh → radar synthesis pipeline."""
    rprint(f"[bold]Profile:[/bold] {profile}")
    rprint(f"[bold]Video:[/bold] {video}")
    result = simulate_from_video(
        video,
        profile,
        output_dir=output,
        max_frames=max_frames,
        add_noise=noise,
    )
    rprint(
        f"[green]Done.[/green] {result.heatmaps.shape[0]} frames, "
        f"heatmap shape {tuple(result.heatmaps.shape[1:])} → {output}"
    )


@app.command("demo-mesh")
def demo_mesh(
    output: Path = typer.Option(Path("outputs/demo_mesh"), "--output", "-o"),
    profile: str = typer.Option("ti_iwr1843boost", "--profile", "-p"),
    num_frames: int = typer.Option(30, "--frames"),
    noise: bool = typer.Option(False, "--noise"),
) -> None:
    """Phase-0 demo: synthetic capsule mesh → heatmap sequence (no video required)."""
    base_verts, faces = make_capsule_mesh()
    offset = (0.0, 2.0, 0.0)
    frames: list[MeshFrame] = []
    for t in range(num_frames):
        verts, _ = animate_capsule_wave(base_verts, faces, t)
        frames.append(MeshFrame(vertices=verts + offset, faces=faces))

    sequence = MeshSequence(frames=frames, fps=30.0, source="cli_demo_capsule")
    result = simulate_from_mesh_sequence(sequence, profile, add_noise=noise)

    from videoradar.export.toolbox import export_simulation_bundle

    export_simulation_bundle(result, output, profile_name=profile)
    rprint(f"[green]Demo complete.[/green] Exported to {output}")


@app.command("list-profiles")
def list_profiles() -> None:
    """List built-in radar profiles."""
    from videoradar.radar.config import _PROFILES_DIR

    for path in sorted(_PROFILES_DIR.glob("*.yaml")):
        prof = load_radar_profile(path.stem)
        rprint(f"  [cyan]{path.stem}[/cyan]  fc={prof.fc/1e9:.1f} GHz  B={prof.bandwidth/1e9:.1f} GHz")


if __name__ == "__main__":
    app()
