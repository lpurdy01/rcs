"""Generate an illustrative RCS-vs-aspect-angle polar diagram.

Outputs a polar plot of backscatter magnitude vs observation angle with a simple
aircraft icon at the center and an example incidence-angle arrow.

Usage (Windows):
  py -3 figures\\make_rcs_polar_diagram.py

Optional args:
  py -3 figures\\make_rcs_polar_diagram.py --out figures\\rcs_polar_diagram

This script is intentionally self-contained and uses synthetic data (not tied to
any particular airframe) for explanatory figures in the article.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np


def _synthetic_rcs_db(theta_rad: np.ndarray) -> np.ndarray:
    """Create a plausible-looking, deterministic RCS pattern in dB (relative)."""
    # Broad body lobes + a few narrow "cavity"/"edge" highlights.
    base = (
        0.55 * np.cos(theta_rad - 0.2) ** 2
        + 0.25 * np.cos(2 * theta_rad + 0.7) ** 2
        + 0.15 * np.cos(3 * theta_rad - 1.1) ** 2
    )

    def spike(center_deg: float, width_deg: float, amp: float) -> np.ndarray:
        center = np.deg2rad(center_deg)
        width = np.deg2rad(width_deg)
        # Wrap-around safe angular distance
        d = np.angle(np.exp(1j * (theta_rad - center)))
        return amp * np.exp(-(d**2) / (2 * width**2))

    spikes = (
        spike(35, 6, 1.0)
        + spike(140, 10, 0.7)
        + spike(225, 7, 0.85)
        + spike(315, 9, 0.6)
    )

    lin = 0.12 + base + 0.65 * spikes
    lin = np.clip(lin, 1e-4, None)

    # Convert to relative dB, normalized to max = 0 dB.
    db = 10.0 * np.log10(lin)
    db -= np.max(db)
    return db


def _add_aircraft_icon(ax, size: float = 0.10, color: str = "#111111") -> None:
    """Draw a simple top-down aircraft silhouette in axes coordinates."""
    import matplotlib.patches as patches

    cx, cy = 0.5, 0.5

    # A very simple silhouette: fuselage + wings + tail.
    # Defined in a local coordinate system then shifted/scaled into axes coords.
    pts = np.array(
        [
            # Nose
            [0.0, 1.00],
            # Fuselage sides down
            [0.10, 0.55],
            [0.10, 0.15],
            # Tail right
            [0.22, -0.05],
            [0.08, -0.05],
            [0.08, -0.20],
            [0.00, -0.20],
            # Tail left
            [-0.08, -0.20],
            [-0.08, -0.05],
            [-0.22, -0.05],
            # Back up fuselage
            [-0.10, 0.15],
            [-0.10, 0.55],
        ]
    )

    # Wings (separate polygon)
    wings = np.array(
        [
            [-0.85, 0.30],
            [-0.12, 0.42],
            [-0.12, 0.18],
            [-0.85, 0.06],
            [0.85, 0.06],
            [0.12, 0.18],
            [0.12, 0.42],
            [0.85, 0.30],
            [0.85, 0.22],
            [-0.85, 0.22],
        ]
    )

    def to_axes(p: np.ndarray) -> np.ndarray:
        return np.column_stack([cx + size * p[:, 0], cy + size * p[:, 1]])

    fuselage = patches.Polygon(
        to_axes(pts),
        closed=True,
        facecolor=color,
        edgecolor="none",
        alpha=0.95,
        transform=ax.transAxes,
        zorder=10,
    )
    wing_poly = patches.Polygon(
        to_axes(wings),
        closed=True,
        facecolor=color,
        edgecolor="none",
        alpha=0.95,
        transform=ax.transAxes,
        zorder=9,
    )

    # White outline to keep it visible on dense gridlines.
    outline = patches.Polygon(
        to_axes(pts),
        closed=True,
        fill=False,
        edgecolor="white",
        linewidth=1.0,
        alpha=0.9,
        transform=ax.transAxes,
        zorder=11,
    )

    ax.add_patch(wing_poly)
    ax.add_patch(fuselage)
    ax.add_patch(outline)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        type=str,
        default=str(Path("figures") / "rcs_polar_diagram"),
        help="Output path without extension (default: figures/rcs_polar_diagram)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=220,
        help="DPI for PNG output.",
    )
    args = parser.parse_args()

    out_base = Path(args.out)
    out_base.parent.mkdir(parents=True, exist_ok=True)

    import matplotlib.pyplot as plt

    theta = np.linspace(0.0, 2.0 * np.pi, 720, endpoint=False)
    rcs_db = _synthetic_rcs_db(theta)

    # Map dB values to a positive radius so the polar plot is readable.
    # Here 0 dB is outer ring; -30 dB is near the center.
    r_min_db = -30.0
    r = np.clip(rcs_db, r_min_db, 0.0)
    r_plot = r - r_min_db

    fig = plt.figure(figsize=(7.2, 7.2), constrained_layout=True)
    ax = fig.add_subplot(111, projection="polar")

    ax.set_theta_zero_location("E")
    ax.set_theta_direction(-1)

    ax.plot(theta, r_plot, color="#1f77b4", linewidth=2.2, label="RCS vs aspect")
    ax.fill(theta, r_plot, color="#1f77b4", alpha=0.12)

    # Radial labels in dB.
    rticks_db = np.array([0, -5, -10, -15, -20, -25, -30], dtype=float)
    rticks = rticks_db - r_min_db
    ax.set_rticks(rticks)
    ax.set_yticklabels([f"{int(v)} dB" for v in rticks_db])

    ax.set_title("Illustrative RCS Pattern vs Observation Angle", pad=18)

    # Add aircraft icon at the center.
    _add_aircraft_icon(ax, size=0.10)

    # Example observation direction.
    obs_deg = 60.0
    obs_th = np.deg2rad(obs_deg)
    r_max = float(np.max(r_plot))

    ax.plot([obs_th, obs_th], [0.0, r_max], color="#d62728", linewidth=1.8, alpha=0.9)
    ax.annotate(
        "Observer angle θ",
        xy=(obs_th, r_max),
        xytext=(obs_th, r_max + 6.0),
        textcoords="data",
        ha="center",
        va="bottom",
        fontsize=10,
        color="#d62728",
        arrowprops=dict(arrowstyle="-|>", color="#d62728", lw=1.5),
    )

    ax.grid(True, alpha=0.30)

    # Save both vector (SVG) and raster (PNG)
    svg_path = out_base.with_suffix(".svg")
    png_path = out_base.with_suffix(".png")

    fig.savefig(svg_path, bbox_inches="tight")
    fig.savefig(png_path, bbox_inches="tight", dpi=args.dpi)

    print(f"Wrote: {svg_path}")
    print(f"Wrote: {png_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
