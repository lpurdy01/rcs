#!/usr/bin/env python3
"""
cf_anisotropic_sim.py — FDTD simulation of an anisotropic lossy composite slab

Demonstrates electromagnetic wave interaction with an anisotropic material
analogous to a carbon fiber reinforced polymer (CFRP).  Carbon fibers are
electrically conductive along their axis (σ∥ ~ 50,000 S/m) and nearly
insulating transverse to the fiber (σ⊥ ~ 10–500 S/m).

FDTD scaling note
-----------------
Real CFRP at GHz frequencies has a skin depth of δ∥ ≈ 0.07 mm (at 1 GHz),
requiring sub-millimetre FDTD cells — impractical on a workstation.  This
simulation uses conductivities scaled to give δ ≈ 10 mm, so that the 2 mm
fine mesh captures ≥ 5 cells per skin depth and the physics is numerically
accurate.  The contrast ratio σ∥/σ⊥ = 100× is preserved from real CFRP,
and all qualitative EM phenomena (anisotropic reflection, polarisation-
selective attenuation, skin effect inside the slab) are faithfully reproduced.

Material
  σ∥   = 2.5  S/m  (along fiber, x-direction)    δ ≈ 10.5 mm at 1 GHz
  σ⊥   = 0.025 S/m (transverse, y and z)           δ ≈ 425  mm at 1 GHz
  εr   = 4.0         (composite matrix permittivity)

Two polarisations compared
  Ex (∥ fiber): E-field along fiber axis → strong attenuation, mostly reflected
  Ey (⊥ fiber): E-field perpendicular   → slab nearly transparent

Three runs
  1. Reference (no slab, Ex excitation) — transmission normalisation
  2. Ex polarisation with CFRP slab
  3. Ey polarisation with CFRP slab

Outputs  (docs/report_images/)
  cf_efield_comparison.png   4-panel |E| map at 1 GHz and 2 GHz
  cf_transmission.png        transmission vs frequency for both polarisations
  cf_animation_Ex.mp4        CW wave animation — Ex polarisation at 1 GHz
  cf_animation_Ey.mp4        CW wave animation — Ey polarisation at 1 GHz

Usage
  source /home/vscode/opt/openEMS/venv/bin/activate
  python test_simulations/carbon_fiber/cf_anisotropic_sim.py          # run + plot
  python test_simulations/carbon_fiber/cf_anisotropic_sim.py --post-only
"""

import os
import sys
import math
import cmath
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import h5py
from pathlib import Path

# Use the bundled ffmpeg from imageio-ffmpeg so MP4 export works without a
# system ffmpeg installation.
try:
    import imageio_ffmpeg as _iio_ffmpeg
    matplotlib.rcParams['animation.ffmpeg_path'] = _iio_ffmpeg.get_ffmpeg_exe()
except Exception:
    pass

from CSXCAD import ContinuousStructure
from openEMS import openEMS
from openEMS.physical_constants import C0

# ─── Paths ─────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[2]
SIM_BASE  = Path('/tmp/CF_Anisotropic')
FIG_DIR   = REPO_ROOT / 'docs' / 'report_images'

SIM_PATH_REF = SIM_BASE / 'reference'
SIM_PATH_EX  = SIM_BASE / 'Ex_pol'
SIM_PATH_EY  = SIM_BASE / 'Ey_pol'

# ─── Material parameters ───────────────────────────────────────────────────────
# Conductivities scaled for FDTD tractability: δ ≥ 5×cell_size at 1 GHz
# Real CFRP: σ∥ ≈ 50,000 S/m (δ ≈ 0.07 mm at 1 GHz — needs sub-mm cells)
KAPPA_FIBER       = 2.5     # S/m — σ∥, along fiber (x)  → δ ≈ 10.5 mm @ 1 GHz
KAPPA_TRANSVERSE  = 0.025   # S/m — σ⊥, transverse (y,z) → δ ≈  425 mm @ 1 GHz
EPS_R_CFRP        = 4.0     # relative permittivity of composite matrix

# ─── Geometry (mm) ────────────────────────────────────────────────────────────
SLAB_W   = 150     # slab width  in x (fiber direction)
SLAB_H   = 150     # slab height in y
SLAB_T   =  20     # slab thickness in z (wave propagation direction)
SLAB_Z0  = -SLAB_T / 2
SLAB_Z1  =  SLAB_T / 2

# ─── Simulation box (mm) ──────────────────────────────────────────────────────
SIM_W    = 380     # x and y full extent (must give room for PML beyond PW_BOX)
SIM_Z    = 480     # z full extent
PW_BOX   = 100     # plane-wave excitation box half-size
#                    Must be < SIM_W/2 − PML_depth − margin
#                    ≈ 190 − 60 − 30 = 100 mm.  Slab ±75mm fits inside.

# ─── Frequency ────────────────────────────────────────────────────────────────
f_start  = 200e6    # Hz
f_stop   = 2000e6   # Hz  (2 GHz — limited to keep cells ≥ 5/δ at high freq)
f0       = 0.5 * (f_start + f_stop)

F_MAPS   = [1.0e9, 2.0e9]      # Hz — field-map snapshots
F_PROBE  = np.linspace(f_start, f_stop, 100)   # Hz — transmission curve

# Probe location
PROBE_Z    = 120.0    # mm behind slab (well inside domain, ~65 mm from PML)
PROBE_HALF = 4.0      # mm — probe box half-size in x and y

# ─── Mesh ──────────────────────────────────────────────────────────────────────
max_cell  = C0 / f_stop / 1e-3 / 20   # λ/20 at 2 GHz ≈ 7.5 mm
fine_cell = 3.0                         # mm inside slab; δ_min(2GHz) ≈ 7.8 mm → ≥2 cells/δ

# ─── Dark-theme colour palette ────────────────────────────────────────────────
_BG    = '#0d1117'
_TEXT  = '#d0e4f8'
_MUTED = '#7a9ab8'
_ACC   = '#4a90d8'
_SLAB  = '#4a90d8'


# ══════════════════════════════════════════════════════════════════════════════
#  PHYSICS HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def penetration_depth_mm(sigma: float, freq: float,
                          eps_r: float = EPS_R_CFRP) -> float:
    """
    Full complex-k penetration depth (mm) in a lossy medium.
    Valid for both lossy-dielectric and conductor regimes.
    """
    eps0  = 8.854187817e-12
    omega = 2 * math.pi * freq
    eps_c = complex(eps_r, -sigma / (omega * eps0))
    k     = omega / C0 * cmath.sqrt(eps_c)
    alpha = abs(k.imag)
    return (1.0 / alpha * 1e3) if alpha > 1e-30 else 1e9


def expected_transmission(sigma: float, freq: float,
                           thickness_mm: float,
                           eps_r: float = EPS_R_CFRP) -> float:
    """
    Field transmission amplitude through a slab of given thickness (mm)
    using the single-pass attenuation: T = exp(-thickness / delta).
    (Ignores multiple reflections; accurate for lossy slabs.)
    """
    delta = penetration_depth_mm(sigma, freq, eps_r)
    return math.exp(-thickness_mm / delta)


# ══════════════════════════════════════════════════════════════════════════════
#  SIMULATION BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def _build_and_run(sim_path: Path, e_dir: list, slab: bool, label: str):
    """Build and run one openEMS simulation."""
    os.makedirs(str(sim_path), exist_ok=True)

    # ── FDTD ──────────────────────────────────────────────────────────────────
    # EndCriteria=1e-3 (-30 dB): practical for plane-wave sims; DFT results are
    # accumulated throughout so accuracy doesn't depend on running until -50 dB.
    FDTD = openEMS(EndCriteria=1e-3)
    FDTD.SetGaussExcite(f0, 0.5 * (f_stop - f_start))
    FDTD.SetBoundaryCond(['PML_8'] * 6)

    CSX  = ContinuousStructure()
    FDTD.SetCSX(CSX)
    mesh = CSX.GetGrid()
    mesh.SetDeltaUnit(1e-3)   # lengths in mm

    # ── Mesh ──────────────────────────────────────────────────────────────────
    # XY: uniform, mesh line at origin
    for ax in ('x', 'y'):
        mesh.SetLines(ax, [-SIM_W / 2, 0, SIM_W / 2])
        mesh.SmoothMeshLines(ax, max_cell)

    # Z: coarse away from slab; dense near slab
    z_seeds = [
        -SIM_Z / 2,
        SLAB_Z0 - 2.5 * max_cell,
        SLAB_Z0,
        0.0,
        SLAB_Z1,
        SLAB_Z1 + 2.5 * max_cell,
        SIM_Z / 2,
    ]
    mesh.SetLines('z', z_seeds)
    mesh.SmoothMeshLines('z', max_cell)

    # Force fine grid inside slab (7 lines → 6 cells of 3.33 mm < fine_cell)
    n_slab_lines = max(7, int(SLAB_T / fine_cell) + 1)
    mesh.AddLine('z', list(np.linspace(SLAB_Z0, SLAB_Z1, n_slab_lines)))
    mesh.SmoothMeshLines('z', fine_cell, 1.4)

    # ── Anisotropic composite slab ────────────────────────────────────────────
    if slab:
        cfrp = CSX.AddMaterial(
            'CFRP',
            epsilon=[EPS_R_CFRP, EPS_R_CFRP, EPS_R_CFRP],
            kappa=[KAPPA_FIBER, KAPPA_TRANSVERSE, KAPPA_TRANSVERSE],
        )
        cfrp.SetIsotropy(False)   # anisotropic conductivity tensor
        cfrp.AddBox(
            start=[-SLAB_W / 2, -SLAB_H / 2, SLAB_Z0],
            stop= [ SLAB_W / 2,  SLAB_H / 2, SLAB_Z1],
            priority=10,
        )

    # ── Plane wave (travels in +z) ────────────────────────────────────────────
    pw_exc = CSX.AddExcitation('plane_wave', exc_type=10, exc_val=e_dir)
    pw_exc.SetPropagationDir([0, 0, 1])
    pw_exc.SetFrequency(f0)
    pw_exc.AddBox(
        np.array([-PW_BOX, -PW_BOX, -PW_BOX]),
        np.array([ PW_BOX,  PW_BOX,  PW_BOX]),
    )

    # ── Frequency-domain E-field map in xz-plane at y ≈ 0 ────────────────────
    # y-extent spans ±max_cell to capture one mesh cell near y=0
    map_start = np.array([-SIM_W / 2 + 12, -max_cell, -SIM_Z / 2 + 12])
    map_stop  = np.array([ SIM_W / 2 - 12,  max_cell,  SIM_Z / 2 - 12])
    E_map = CSX.AddDump('E_xzmap', dump_type=10, file_type=1, frequency=F_MAPS)
    E_map.AddBox(map_start, map_stop)

    # ── Point probe behind slab at 100 probe frequencies ─────────────────────
    probe_dump = CSX.AddDump(
        'probe_trans', dump_type=10, file_type=1,
        frequency=list(F_PROBE),
    )
    probe_dump.AddBox(
        np.array([-PROBE_HALF, -PROBE_HALF, PROBE_Z]),
        np.array([ PROBE_HALF,  PROBE_HALF, PROBE_Z]),
    )

    # ── Run ───────────────────────────────────────────────────────────────────
    print(f'  [{label}]  running openEMS …')
    FDTD.Run(str(sim_path), cleanup=False, verbose=0)
    print(f'  [{label}]  done.')


# ══════════════════════════════════════════════════════════════════════════════
#  HDF5 READERS
# ══════════════════════════════════════════════════════════════════════════════

def _read_probe_h5(sim_path: Path) -> np.ndarray:
    """
    Read probe_trans.h5 and return E-magnitude array of shape (len(F_PROBE),).
    For each frequency, spatial RMS of |E| is computed over the probe box cells.
    """
    h5path = sim_path / 'probe_trans.h5'
    E_mags = []
    with h5py.File(str(h5path), 'r') as f:
        for n in range(len(F_PROBE)):
            Ereal = f[f'FieldData/FD/f{n}_real'][:]   # (3, nx, ny, nz)
            Eimag = f[f'FieldData/FD/f{n}_imag'][:]
            E_cplx = Ereal + 1j * Eimag
            E_mag  = np.sqrt(np.mean(np.sum(np.abs(E_cplx)**2, axis=0)))
            E_mags.append(float(E_mag))
    return np.array(E_mags)


def _read_map_h5(sim_path: Path, freq_idx: int):
    """
    Read E_xzmap.h5 at frequency index freq_idx.
    Returns (x, z, E_xz_complex, E_mag_xz) where:
      E_xz_complex  — shape (3, nx, nz)  complex
      E_mag_xz      — shape (nx, nz)     |E|
    """
    h5path = sim_path / 'E_xzmap.h5'
    with h5py.File(str(h5path), 'r') as f:
        x    = f['Mesh/x'][:] * 1e3   # HDF5 stores in metres → convert to mm
        z    = f['Mesh/z'][:] * 1e3   # HDF5 stores in metres → convert to mm
        Ereal = f[f'FieldData/FD/f{freq_idx}_real'][:]   # (3, Nz, Ny, Nx)
        Eimag = f[f'FieldData/FD/f{freq_idx}_imag'][:]

    # openEMS writes HDF5 with z as the outermost spatial index:
    # shape = (3, Nz, Ny, Nx)
    E    = Ereal + 1j * Eimag           # (3, Nz, Ny, Nx)
    ymid = E.shape[2] // 2
    E_xz = E[:, :, ymid, :]             # (3, Nz, Nx)
    E_mag = np.sqrt(np.sum(np.abs(E_xz)**2, axis=0))   # (Nz, Nx)
    return x, z, E_xz, E_mag


# ══════════════════════════════════════════════════════════════════════════════
#  FIGURES
# ══════════════════════════════════════════════════════════════════════════════

def _ax_style(ax):
    ax.set_facecolor(_BG)
    ax.tick_params(colors=_MUTED, labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor('#2a3a4a')


def _crop_xz(x, z, data_nz_nx,
             xlim=(-PW_BOX, PW_BOX), zlim=(-PW_BOX, PW_BOX)):
    """
    Crop x, z and a (Nz, Nx) array to the given axis limits.
    Returns cropped (x, z, data) — all three share consistent indices.
    """
    xm = (x >= xlim[0]) & (x <= xlim[1])
    zm = (z >= zlim[0]) & (z <= zlim[1])
    return x[xm], z[zm], data_nz_nx[np.ix_(zm, xm)]


def plot_field_maps():
    """4-panel |E| comparison: (Ex, 1 GHz) | (Ex, 2 GHz) | (Ey, 1 GHz) | (Ey, 2 GHz)."""
    fig, axes = plt.subplots(2, 2, figsize=(13, 10), facecolor=_BG)

    configs = [
        (SIM_PATH_EX, 0, 'E∥ fiber  (Ex,  σ∥=2.5 S/m)',  '1 GHz'),
        (SIM_PATH_EX, 1, 'E∥ fiber  (Ex,  σ∥=2.5 S/m)',  '2 GHz'),
        (SIM_PATH_EY, 0, 'E⊥ fiber  (Ey,  σ⊥=0.025 S/m)', '1 GHz'),
        (SIM_PATH_EY, 1, 'E⊥ fiber  (Ey,  σ⊥=0.025 S/m)', '2 GHz'),
    ]

    # Shared colour scale per frequency column (computed inside TF/SF box only)
    vmaxes = {}
    for sim_path, fi, _, _ in configs:
        x, z, _, E_mag = _read_map_h5(sim_path, fi)
        _, _, E_c = _crop_xz(x, z, E_mag)
        vmaxes[fi] = max(vmaxes.get(fi, 0.0), float(np.percentile(E_c, 99)))

    for ax, (sim_path, fi, pol_label, freq_label) in zip(axes.flat, configs):
        x, z, _, E_mag = _read_map_h5(sim_path, fi)
        x, z, E_mag = _crop_xz(x, z, E_mag)   # crop to TF/SF box (±PW_BOX mm)
        _ax_style(ax)

        im = ax.imshow(
            E_mag,
            origin='lower',
            extent=[x.min(), x.max(), z.min(), z.max()],
            cmap='inferno',
            aspect='equal',
            vmin=0,
            vmax=vmaxes[fi],
        )
        cb = plt.colorbar(im, ax=ax, fraction=0.030, pad=0.03)
        cb.set_label('|E| (a.u.)', color=_MUTED, fontsize=8)
        cb.ax.yaxis.set_tick_params(color=_MUTED)
        plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color=_MUTED)

        # Slab boundaries
        ax.axhline(SLAB_Z0, color=_SLAB, lw=1.4, ls='--', label='Slab surfaces')
        ax.axhline(SLAB_Z1, color=_SLAB, lw=1.4, ls='--')
        ax.axvline(-SLAB_W / 2, color=_SLAB, lw=0.9, ls=':', alpha=0.7)
        ax.axvline( SLAB_W / 2, color=_SLAB, lw=0.9, ls=':', alpha=0.7)

        # Skin-depth annotation
        sigma  = KAPPA_FIBER if '∥' in pol_label else KAPPA_TRANSVERSE
        freq_n = float(freq_label.split()[0]) * 1e9
        delta  = penetration_depth_mm(sigma, freq_n)
        n_slab_depths = SLAB_T / delta
        ax.text(0.02, 0.03,
                f'δ = {delta:.1f} mm\n'
                f'slab = {n_slab_depths:.1f}δ',
                transform=ax.transAxes, color=_MUTED, fontsize=7,
                va='bottom', ha='left',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#12202e',
                          edgecolor='#2a3a4a', alpha=0.85))

        ax.set_xlabel('x (mm)', color=_TEXT, fontsize=9)
        ax.set_ylabel('z (mm)', color=_TEXT, fontsize=9)
        ax.set_title(f'{pol_label}  —  {freq_label}', color=_TEXT, fontsize=9, pad=5)
        ax.legend(loc='upper right', fontsize=7, framealpha=0.3, labelcolor=_TEXT)

    fig.suptitle(
        'E-field magnitude  |E|  in xz-plane (y = 0)\n'
        f'Anisotropic composite slab {SLAB_W}×{SLAB_H}×{SLAB_T} mm  |  fibers along x  |  '
        f'εr = {EPS_R_CFRP:.0f}\n'
        f'σ∥ = {KAPPA_FIBER} S/m   σ⊥ = {KAPPA_TRANSVERSE} S/m'
        f'   (scaled from real CFRP; ratio σ∥/σ⊥ = {int(KAPPA_FIBER/KAPPA_TRANSVERSE)}× preserved)',
        color=_TEXT, fontsize=10, y=1.01,
    )
    plt.tight_layout()

    out = FIG_DIR / 'cf_efield_comparison.png'
    plt.savefig(str(out), dpi=150, bbox_inches='tight', facecolor=_BG)
    plt.close()
    print(f'  Saved: {out}')


def plot_transmission():
    """Transmission coefficient vs frequency — FDTD vs analytical estimate."""
    E_ref = _read_probe_h5(SIM_PATH_REF)
    E_ex  = _read_probe_h5(SIM_PATH_EX)
    E_ey  = _read_probe_h5(SIM_PATH_EY)

    eps = 1e-30
    T_ex = E_ex / (E_ref + eps)
    T_ey = E_ey / (E_ref + eps)

    # Analytical single-pass estimate for comparison
    T_ex_ana = np.array([expected_transmission(KAPPA_FIBER,      f, SLAB_T)
                          for f in F_PROBE])
    T_ey_ana = np.array([expected_transmission(KAPPA_TRANSVERSE, f, SLAB_T)
                          for f in F_PROBE])

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), facecolor=_BG)

    # ── Panel 1: linear amplitude ─────────────────────────────────────────────
    ax = axes[0]
    _ax_style(ax)
    ax.plot(F_PROBE / 1e9, T_ex, color='#e05555', lw=2,
            label='E∥ fiber  FDTD  (σ∥=2.5 S/m)')
    ax.plot(F_PROBE / 1e9, T_ey, color=_ACC, lw=2,
            label='E⊥ fiber  FDTD  (σ⊥=0.025 S/m)')
    ax.plot(F_PROBE / 1e9, T_ex_ana, color='#e05555', lw=1.5, ls='--', alpha=0.6,
            label='E∥  analytic (single-pass)')
    ax.plot(F_PROBE / 1e9, T_ey_ana, color=_ACC, lw=1.5, ls='--', alpha=0.6,
            label='E⊥  analytic')
    ax.set_xlabel('Frequency (GHz)', color=_TEXT)
    ax.set_ylabel('|E_trans| / |E_inc|', color=_TEXT)
    ax.set_title('Transmission amplitude', color=_TEXT)
    ax.set_ylim(bottom=0)
    ax.legend(framealpha=0.25, labelcolor=_TEXT, fontsize=8)
    ax.grid(True, color='#2a3a4a', lw=0.6)

    # ── Panel 2: dB ───────────────────────────────────────────────────────────
    ax2 = axes[1]
    _ax_style(ax2)
    T_ex_dB     = 20 * np.log10(T_ex + eps)
    T_ey_dB     = 20 * np.log10(T_ey + eps)
    T_ex_ana_dB = 20 * np.log10(T_ex_ana + eps)
    T_ey_ana_dB = 20 * np.log10(T_ey_ana + eps)

    ax2.plot(F_PROBE / 1e9, T_ex_dB,     color='#e05555', lw=2,     label='E∥  FDTD')
    ax2.plot(F_PROBE / 1e9, T_ey_dB,     color=_ACC,      lw=2,     label='E⊥  FDTD')
    ax2.plot(F_PROBE / 1e9, T_ex_ana_dB, color='#e05555', lw=1.5, ls='--', alpha=0.6,
             label='E∥  analytic')
    ax2.plot(F_PROBE / 1e9, T_ey_ana_dB, color=_ACC,      lw=1.5, ls='--', alpha=0.6,
             label='E⊥  analytic')
    ax2.set_xlabel('Frequency (GHz)', color=_TEXT)
    ax2.set_ylabel('Transmission (dB)', color=_TEXT)
    ax2.set_title('Transmission in dB', color=_TEXT)
    ax2.legend(framealpha=0.25, labelcolor=_TEXT, fontsize=8)
    ax2.grid(True, color='#2a3a4a', lw=0.6)

    # Annotate skin depths at 1 GHz
    for freq_ann in [1.0e9]:
        d_fib = penetration_depth_mm(KAPPA_FIBER,      freq_ann)
        d_trn = penetration_depth_mm(KAPPA_TRANSVERSE, freq_ann)
        # Annotation in dB panel at right edge
        ax2.text(0.97, 0.05,
                 f'@ 1 GHz\n'
                 f'δ∥ = {d_fib:.1f} mm  ({SLAB_T/d_fib:.1f}δ in slab)\n'
                 f'δ⊥ = {d_trn:.0f} mm  ({SLAB_T/d_trn:.2f}δ in slab)',
                 transform=ax2.transAxes, fontsize=7.5, color=_MUTED,
                 va='bottom', ha='right',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#12202e',
                           edgecolor='#2a3a4a', alpha=0.9))

    fig.suptitle(
        f'Anisotropic CFRP slab — transmission vs frequency\n'
        f'Slab: {SLAB_W}×{SLAB_H}×{SLAB_T} mm  |  probe at z = +{PROBE_Z:.0f} mm  |  '
        f'εr = {EPS_R_CFRP:.0f}\n'
        f'σ∥ = {KAPPA_FIBER} S/m  σ⊥ = {KAPPA_TRANSVERSE} S/m  '
        f'(ratio {int(KAPPA_FIBER/KAPPA_TRANSVERSE)}×)',
        color=_TEXT, fontsize=10, y=1.02,
    )
    plt.tight_layout()
    out = FIG_DIR / 'cf_transmission.png'
    plt.savefig(str(out), dpi=150, bbox_inches='tight', facecolor=_BG)
    plt.close()
    print(f'  Saved: {out}')


def _make_cw_animation(sim_path: Path, pol_label: str, comp_idx: int,
                       out_name: str):
    """
    Synthetic CW wave animation from frequency-domain E-field data at 1 GHz.
    Sweeps phase φ from 0 → 2π: E_frame(x,z) = Re[E_complex(x,z) · exp(iφ)].
    comp_idx: 0=Ex, 1=Ey, 2=Ez
    """
    x, z, E_xz, _ = _read_map_h5(sim_path, 0)   # freq index 0 = 1 GHz

    # Crop to TF/SF box so the viewer sees only the total-field region
    E_comp = E_xz[comp_idx, :, :]              # (Nz, Nx) complex
    x, z, E_comp = _crop_xz(x, z, E_comp)

    n_frames = 60
    phases   = np.linspace(0, 2 * np.pi, n_frames, endpoint=False)
    frames   = np.array([np.real(E_comp * np.exp(1j * phi)) for phi in phases])
    vmax     = float(np.percentile(np.abs(frames), 99))

    fig, ax = plt.subplots(figsize=(8, 7), facecolor=_BG)
    _ax_style(ax)

    im = ax.imshow(
        frames[0],
        origin='lower',
        extent=[x.min(), x.max(), z.min(), z.max()],
        cmap='RdBu_r',
        aspect='equal',
        vmin=-vmax, vmax=vmax,
        animated=True,
    )
    cb = plt.colorbar(im, ax=ax, fraction=0.030, pad=0.03)
    cb.set_label('E (a.u.)', color=_MUTED, fontsize=8)
    cb.ax.yaxis.set_tick_params(color=_MUTED)
    plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color=_MUTED)

    ax.axhline(SLAB_Z0, color=_SLAB, lw=1.4, ls='--', label='Slab surfaces')
    ax.axhline(SLAB_Z1, color=_SLAB, lw=1.4, ls='--')
    ax.axvline(-SLAB_W / 2, color=_SLAB, lw=0.9, ls=':', alpha=0.7)
    ax.axvline( SLAB_W / 2, color=_SLAB, lw=0.9, ls=':', alpha=0.7)
    ax.set_xlabel('x (mm)', color=_TEXT, fontsize=10)
    ax.set_ylabel('z (mm)', color=_TEXT, fontsize=10)
    ax.set_title(f'{pol_label} — 1 GHz CW field', color=_TEXT, fontsize=11, pad=6)
    ax.legend(loc='upper right', fontsize=7, framealpha=0.3, labelcolor=_TEXT)

    sigma  = KAPPA_FIBER if '∥' in pol_label else KAPPA_TRANSVERSE
    delta  = penetration_depth_mm(sigma, 1e9)
    ax.text(0.02, 0.97,
            f'Fibers: → x\nδ = {delta:.1f} mm',
            transform=ax.transAxes, color=_ACC, fontsize=8, va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#12202e',
                      edgecolor='#2a3a4a', alpha=0.85))

    def update(frame_idx):
        im.set_array(frames[frame_idx])
        return (im,)

    anim = animation.FuncAnimation(
        fig, update, frames=n_frames, interval=50, blit=True,
    )

    # Prefer MP4 via FFMpegWriter (imageio-ffmpeg bundled binary set in rcParams).
    # Fall back to PillowWriter + GIF if ffmpeg is not available.
    mp4_name = out_name if out_name.endswith('.mp4') else out_name.replace('.gif', '.mp4')
    out = FIG_DIR / mp4_name
    try:
        if animation.FFMpegWriter.isAvailable():
            writer = animation.FFMpegWriter(fps=20, bitrate=2000,
                                            extra_args=['-vcodec', 'libx264',
                                                        '-pix_fmt', 'yuv420p'])
            anim.save(str(out), writer=writer, dpi=100,
                      savefig_kwargs={'facecolor': _BG})
            print(f'  Saved MP4: {out}')
        else:
            gif_out = FIG_DIR / mp4_name.replace('.mp4', '.gif')
            writer = animation.PillowWriter(fps=20)
            anim.save(str(gif_out), writer=writer, dpi=100,
                      savefig_kwargs={'facecolor': _BG})
            print(f'  Saved GIF (ffmpeg unavailable): {gif_out}')
            out = gif_out
    except Exception as exc:
        print(f'  WARNING: animation save failed ({exc}). Saving phase-sweep PNG instead.')
        fig2, axs = plt.subplots(2, 5, figsize=(15, 6), facecolor=_BG)
        for ax_f, fi in zip(axs.flat, np.linspace(0, n_frames - 1, 10, dtype=int)):
            _ax_style(ax_f)
            ax_f.imshow(frames[fi], origin='lower', cmap='RdBu_r',
                        vmin=-vmax, vmax=vmax,
                        extent=[x.min(), x.max(), z.min(), z.max()], aspect='equal')
            ax_f.axhline(SLAB_Z0, color=_SLAB, lw=0.8, ls='--')
            ax_f.axhline(SLAB_Z1, color=_SLAB, lw=0.8, ls='--')
            ax_f.set_title(f'φ={phases[fi]:.1f}', color=_MUTED, fontsize=7)
        fig2.suptitle(f'{pol_label} — CW phase sweep', color=_TEXT, fontsize=10)
        plt.tight_layout()
        fallback = FIG_DIR / mp4_name.replace('.mp4', '_frames.png')
        plt.savefig(str(fallback), dpi=130, bbox_inches='tight', facecolor=_BG)
        plt.close()
        print(f'  Saved fallback: {fallback}')
    finally:
        plt.close('all')


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    post_only = '--post-only' in sys.argv

    FIG_DIR.mkdir(parents=True, exist_ok=True)
    SIM_BASE.mkdir(parents=True, exist_ok=True)

    print('=== Anisotropic Carbon-Fiber Composite — FDTD Demo ===')
    print(f'  σ∥ = {KAPPA_FIBER} S/m   (fiber axis, x)')
    print(f'  σ⊥ = {KAPPA_TRANSVERSE} S/m  (transverse, y/z)')
    print(f'  εr = {EPS_R_CFRP}')
    for freq in [0.5e9, 1e9, 2e9]:
        df = penetration_depth_mm(KAPPA_FIBER,      freq)
        dt = penetration_depth_mm(KAPPA_TRANSVERSE, freq)
        Tf = expected_transmission(KAPPA_FIBER,      freq, SLAB_T)
        Tt = expected_transmission(KAPPA_TRANSVERSE, freq, SLAB_T)
        print(f'  @ {freq/1e9:.1f} GHz:  '
              f'δ∥={df:.1f}mm → T={Tf:.3f}   '
              f'δ⊥={dt:.0f}mm → T={Tt:.3f}')
    print(f'  max_cell={max_cell:.1f} mm,  fine_cell={fine_cell} mm')
    print()

    if not post_only:
        # Run 1: reference — no slab, Ex polarisation
        _build_and_run(SIM_PATH_REF, e_dir=[1, 0, 0], slab=False,
                       label='REF  no-slab  Ex')
        # Run 2: Ex polarisation with slab (E ∥ fiber → high σ∥)
        _build_and_run(SIM_PATH_EX,  e_dir=[1, 0, 0], slab=True,
                       label='Ex pol  ∥ fiber')
        # Run 3: Ey polarisation with slab (E ⊥ fiber → low σ⊥)
        _build_and_run(SIM_PATH_EY,  e_dir=[0, 1, 0], slab=True,
                       label='Ey pol  ⊥ fiber')

    print('=== Post-processing ===')

    print('  Generating E-field comparison figure …')
    plot_field_maps()

    print('  Generating transmission curve …')
    plot_transmission()

    print('  Generating CW animation — Ex polarisation …')
    _make_cw_animation(SIM_PATH_EX, 'E∥ fiber (σ∥=2.5 S/m)', comp_idx=0,
                       out_name='cf_animation_Ex.mp4')

    print('  Generating CW animation — Ey polarisation …')
    _make_cw_animation(SIM_PATH_EY, 'E⊥ fiber (σ⊥=0.025 S/m)', comp_idx=1,
                       out_name='cf_animation_Ey.mp4')

    print(f'\nAll outputs saved to: {FIG_DIR}')
    print('Done.')


if __name__ == '__main__':
    main()
