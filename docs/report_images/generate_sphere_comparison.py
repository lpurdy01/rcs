#!/usr/bin/env python3
"""
generate_sphere_comparison.py
──────────────────────────────
Generates a publication-quality comparison of the analytical Mie series solution
against the openEMS FDTD simulation result for a perfectly-conducting (PEC) sphere.

The plot shows normalised backscattering RCS  σ / (π a²)  vs  a / λ,
the classic form used to validate Mie-regime solvers.

Usage
─────
Standalone (analytical curve only, no openEMS needed):
    python generate_sphere_comparison.py

With FDTD simulation (requires openEMS Python bindings):
    python generate_sphere_comparison.py --run-fdtd

Load pre-computed FDTD data from a numpy .npz file:
    python generate_sphere_comparison.py --fdtd-data path/to/data.npz

Output
──────
Saves the figure to:
    docs/report_images/sphere_mie_vs_fdtd_comparison.png

Also saves the FDTD data (when --run-fdtd is used) to:
    docs/report_images/sphere_fdtd_data.npz
so later runs can reload it without re-running the simulation.

Theory reference
────────────────
Bohren & Huffman, "Absorption and Scattering of Light by Small Particles",
Chapter 4 (Mie theory).  For a PEC sphere:

    a_n = j_n(x) / h_n^(1)(x)
    b_n = [x j_n(x)]' / [x h_n^(1)(x)]'

    Q_back = σ_back / (π a²)
           = (1 / x²) |Σ_{n=1}^{N} (−1)^n (2n+1)(a_n − b_n)|²

where x = ka = 2π a / λ  and  N follows the Wiscombe convergence criterion.
"""

import argparse
import os
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')   # headless rendering; swap for 'TkAgg' / 'Qt5Agg' for interactive
import matplotlib.pyplot as plt
from scipy.special import spherical_jn, spherical_yn

# ─── Simulation parameters (must match the openEMS sphere scripts) ─────────
SPHERE_RAD_MM   = 200          # sphere radius [mm]
SPHERE_RAD_M    = SPHERE_RAD_MM * 1e-3   # [m]
F_START_HZ      = 50e6         # 50 MHz
F_STOP_HZ       = 1000e6       # 1 GHz
N_FREQ_POINTS   = 200          # resolution for Mie curve

C0              = 299_792_458  # speed of light [m/s]

# ─── Output paths ──────────────────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
OUT_FIGURE   = os.path.join(SCRIPT_DIR, "sphere_mie_vs_fdtd_comparison.png")
OUT_FDTD_NPZ = os.path.join(SCRIPT_DIR, "sphere_fdtd_data.npz")


# ═══════════════════════════════════════════════════════════════════════════
# Mie series
# ═══════════════════════════════════════════════════════════════════════════

def mie_pec_backscatter_normalised(ka_values: np.ndarray, n_extra: int = 5) -> np.ndarray:
    """
    Compute normalised backscattering RCS  Q_back = σ / (π a²)  for a PEC sphere.

    Parameters
    ----------
    ka_values : 1-D array of ka = 2π a / λ  values.
    n_extra   : extra Mie terms beyond the Wiscombe criterion for safety margin.

    Returns
    -------
    Q_back : same shape as ka_values.
    """
    ka_values = np.asarray(ka_values, dtype=float)
    Q_back    = np.zeros_like(ka_values)

    for i, ka in enumerate(ka_values):
        if ka < 1e-9:
            Q_back[i] = 0.0
            continue

        # Wiscombe (1980) convergence criterion
        N = int(np.ceil(ka + 4.05 * ka ** (1.0 / 3.0) + 2.0)) + n_extra

        series = 0.0 + 0.0j

        for n in range(1, N + 1):
            jn  = spherical_jn(n, ka)
            yn  = spherical_yn(n, ka)
            djn = spherical_jn(n, ka, derivative=True)
            dyn = spherical_yn(n, ka, derivative=True)

            # Spherical Hankel function of the first kind and its derivative
            hn  = jn + 1j * yn
            dhn = djn + 1j * dyn

            # Mie coefficients for a PEC sphere
            # a_n = j_n(x) / h_n^(1)(x)
            an = jn / hn

            # b_n = [x j_n(x)]' / [x h_n^(1)(x)]'
            #     = (j_n + x j_n') / (h_n + x h_n')
            bn = (jn + ka * djn) / (hn + ka * dhn)

            series += (-1) ** n * (2 * n + 1) * (an - bn)

        Q_back[i] = abs(series) ** 2 / ka ** 2

    return Q_back


def mie_curve(f_start: float, f_stop: float, sphere_rad: float, n_points: int = 200):
    """
    Return (a_over_lambda, Q_back) for the analytical Mie solution.
    a_over_lambda = a / λ = sphere_rad * freq / C0
    """
    freq         = np.linspace(f_start, f_stop, n_points)
    a_over_lam   = sphere_rad * freq / C0
    ka           = 2 * np.pi * a_over_lam
    Q_back       = mie_pec_backscatter_normalised(ka)
    return a_over_lam, Q_back


# ═══════════════════════════════════════════════════════════════════════════
# FDTD simulation via openEMS
# ═══════════════════════════════════════════════════════════════════════════

def run_fdtd_sphere():
    """
    Run the openEMS FDTD simulation for a PEC sphere and return
    (a_over_lambda, Q_back_fdtd) arrays.

    Requires openEMS Python bindings to be installed.
    """
    import tempfile
    try:
        from CSXCAD import ContinuousStructure
        from openEMS import openEMS as OpenEMS
        from openEMS.physical_constants import C0 as _C0, Z0
        from openEMS.ports import UI_data
    except ImportError as exc:
        print(f"ERROR: openEMS not importable — {exc}")
        print("Install openEMS Python bindings or skip --run-fdtd.")
        sys.exit(1)

    Sim_Path = os.path.join(tempfile.gettempdir(), "RCS_Sphere_Mie_Compare")
    unit     = 1e-3  # all lengths in mm

    sphere_rad = SPHERE_RAD_MM   # mm
    SimBox     = 1200
    PW_Box     = 750

    FDTD = OpenEMS(EndCriteria=1e-5)

    f_start = F_START_HZ
    f_stop  = F_STOP_HZ
    f0      = 0.5 * (f_start + f_stop)
    FDTD.SetGaussExcite(f0, 0.5 * (f_stop - f_start))
    FDTD.SetBoundaryCond(['PML_8'] * 6)

    CSX  = ContinuousStructure()
    FDTD.SetCSX(CSX)
    mesh = CSX.GetGrid()
    mesh.SetDeltaUnit(unit)

    mesh.SetLines('x', [-SimBox / 2, 0, SimBox / 2])
    mesh.SmoothMeshLines('x', _C0 / f_stop / unit / 20)
    mesh.SetLines('y', mesh.GetLines('x'))
    mesh.SetLines('z', mesh.GetLines('x'))

    sphere_metal = CSX.AddMetal('sphere')
    sphere_metal.AddSphere(priority=10, center=[0, 0, 0], radius=sphere_rad)

    inc_angle = 0
    k_dir = [np.cos(np.deg2rad(inc_angle)), np.sin(np.deg2rad(inc_angle)), 0]
    E_dir = [0, 0, 1]

    pw_exc = CSX.AddExcitation('plane_wave', exc_type=10, exc_val=E_dir)
    pw_exc.SetPropagationDir(k_dir)
    pw_exc.SetFrequency(f0)

    start = np.array([-PW_Box / 2, -PW_Box / 2, -PW_Box / 2])
    stop  = -start
    pw_exc.AddBox(start, stop)

    nf2ff = FDTD.CreateNF2FFBox()

    print("[FDTD] Running openEMS simulation …")
    FDTD.Run(Sim_Path, cleanup=False)
    print("[FDTD] Simulation complete.  Post-processing …")

    freq = np.linspace(f_start, f_stop, 100)
    ef   = UI_data('et', Sim_Path, freq)
    Pin  = 0.5 * np.linalg.norm(E_dir) ** 2 / Z0 * abs(np.array(ef.ui_f_val[0])) ** 2

    nf2ff_res  = nf2ff.CalcNF2FF(Sim_Path, freq, 90, 180 + inc_angle,
                                  outfile='back_nf2ff.h5')
    back_scat  = np.array([4 * np.pi / Pin[fn] * nf2ff_res.P_rad[fn][0][0]
                            for fn in range(len(freq))])

    a_over_lam = sphere_rad * unit / _C0 * freq
    Q_back     = back_scat / (np.pi * (sphere_rad * unit) ** 2)

    # Persist for reuse
    np.savez(OUT_FDTD_NPZ, a_over_lam=a_over_lam, Q_back=Q_back)
    print(f"[FDTD] Data saved to {OUT_FDTD_NPZ}")

    return a_over_lam, Q_back


def load_fdtd_data(path: str):
    """Load pre-computed FDTD data from a .npz file."""
    data = np.load(path)
    return data['a_over_lam'], data['Q_back']


# ═══════════════════════════════════════════════════════════════════════════
# Plotting
# ═══════════════════════════════════════════════════════════════════════════

def make_comparison_figure(mie_x, mie_y, fdtd_x=None, fdtd_y=None):
    """
    Build and save the comparison figure.

    Parameters
    ----------
    mie_x, mie_y  : analytical Mie curve (a/λ, Q_back).
    fdtd_x, fdtd_y: FDTD simulation data, or None.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.semilogy(mie_x, mie_y, 'b-', linewidth=2,
                label='Mie series (analytical, PEC sphere)')

    if fdtd_x is not None and fdtd_y is not None:
        ax.semilogy(fdtd_x, fdtd_y, 'r--', linewidth=1.8,
                    label='openEMS FDTD simulation')

    # Geometric-optics limit: σ/(πa²) → 1
    ax.axhline(1.0, color='gray', linestyle=':', linewidth=1.0,
               label='Geometric optics limit (σ = πa²)')

    ax.set_xlim(left=0)
    ax.set_ylim([1e-2, 10])
    ax.set_xlabel('Sphere radius / wavelength  ($a/\\lambda$)', fontsize=12)
    ax.set_ylabel('Normalised RCS  $\\sigma\\,/\\,(\\pi a^2)$', fontsize=12)
    ax.set_title('Sphere RCS Validation: Mie Series vs openEMS FDTD\n'
                 f'(PEC sphere, $a = {SPHERE_RAD_MM}\\,$mm, '
                 f'{F_START_HZ/1e6:.0f}–{F_STOP_HZ/1e6:.0f} MHz)', fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(True, which='both', alpha=0.3)

    status = "analytical only" if fdtd_x is None else "Mie + FDTD"
    fig.text(0.99, 0.01,
             f'openEMS FDTD / Mie series comparison — {status}',
             ha='right', va='bottom', fontsize=7, color='gray')

    plt.tight_layout()
    plt.savefig(OUT_FIGURE, dpi=150, bbox_inches='tight')
    print(f"Figure saved to {OUT_FIGURE}")
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════
# CLI entry point
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Generate Mie-series vs FDTD comparison plot for a PEC sphere.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--run-fdtd', action='store_true',
                       help='Run the openEMS FDTD simulation (requires openEMS).')
    group.add_argument('--fdtd-data', metavar='PATH',
                       help='Path to a .npz file with pre-computed FDTD data.')
    args = parser.parse_args()

    # ── Analytical Mie curve (always computed) ──────────────────────────
    print("Computing Mie series …")
    mie_x, mie_y = mie_curve(F_START_HZ, F_STOP_HZ, SPHERE_RAD_M, N_FREQ_POINTS)
    print(f"  a/λ range: {mie_x[0]:.3f} – {mie_x[-1]:.3f}")
    print(f"  Q_back range: {mie_y.min():.3f} – {mie_y.max():.3f}")

    # ── Optional FDTD data ───────────────────────────────────────────────
    fdtd_x = fdtd_y = None

    if args.run_fdtd:
        fdtd_x, fdtd_y = run_fdtd_sphere()
    elif args.fdtd_data:
        print(f"Loading FDTD data from {args.fdtd_data} …")
        fdtd_x, fdtd_y = load_fdtd_data(args.fdtd_data)
    elif os.path.exists(OUT_FDTD_NPZ):
        print(f"Found cached FDTD data at {OUT_FDTD_NPZ} — loading.")
        fdtd_x, fdtd_y = load_fdtd_data(OUT_FDTD_NPZ)
    else:
        print("No FDTD data provided.  Plotting analytical Mie curve only.")
        print("Use --run-fdtd to also run the openEMS simulation.")

    # ── Plot ─────────────────────────────────────────────────────────────
    make_comparison_figure(mie_x, mie_y, fdtd_x, fdtd_y)


if __name__ == '__main__':
    main()
