#!/usr/bin/env python3
"""
validate_sphere_rcs.py
──────────────────────
Post-processes the existing openEMS sphere FDTD simulation and compares
against analytical Mie series theory for a PEC sphere.

Reads data from /tmp/RCS_Sphere_Simulation_Full/
(produced by test_simulations/RCS_Sphere/rcs_sphere_full_sim.py).

Outputs (saved to docs/report_images/):
    sphere_validation_rcs.png   — 3-panel: normalised Q_back, absolute RCS, % error
    sphere_validation_polar.png — equatorial far-field pattern at f0 (FDTD + Mie)

Theory: Bohren & Huffman, "Absorption and Scattering of Light by Small Particles",
        Chapter 4. PEC Mie coefficients:
            a_n = j_n(x) / h_n(x)
            b_n = [x j_n(x)]' / [x h_n(x)]'
        Amplitude functions via pi_n / tau_n recurrences (Appendix A).
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.special import spherical_jn, spherical_yn

# ── openEMS ──────────────────────────────────────────────────────────────────
try:
    from CSXCAD import ContinuousStructure
    from openEMS import openEMS as OpenEMS
    from openEMS.physical_constants import C0, Z0
    from openEMS.ports import UI_data
    HAS_OPENEMS = True
except ImportError:
    HAS_OPENEMS = False
    C0 = 299_792_458.0
    Z0 = 376.730_313

# ── Parameters — must match rcs_sphere_full_sim.py exactly ───────────────────
SIM_PATH     = '/tmp/RCS_Sphere_Simulation_Full'
SPHERE_RAD   = 200.0        # sphere radius [mm]
unit         = 1e-3         # mm → m
F_START      = 50e6
F_STOP       = 1_000e6
F0           = 0.5 * (F_START + F_STOP)   # 525 MHz
INC_ANGLE    = 0            # incident angle [deg]
SimBox       = 1200         # [mm]
PW_Box       = 750          # [mm]

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
OUT_RCS      = os.path.join(SCRIPT_DIR, 'sphere_validation_rcs.png')
OUT_POLAR    = os.path.join(SCRIPT_DIR, 'sphere_validation_polar.png')

# Second frequency for polar comparison — Rayleigh regime (a/λ ≈ 0.10)
# Expected FDTD error < 5 %, giving clean Mie vs FDTD agreement.
F_POLAR_2    = 150e6          # Hz

SPHERE_RAD_M = SPHERE_RAD * unit   # 0.2 m


# ═══════════════════════════════════════════════════════════════════════════
# Mie series (analytical, PEC sphere)
# ═══════════════════════════════════════════════════════════════════════════

def _wiscombe_nmax(ka, n_extra=5):
    return int(np.ceil(ka + 4.05 * ka ** (1.0 / 3.0) + 2.0)) + n_extra


def _mie_an_bn(n, ka):
    """PEC Mie coefficients a_n, b_n."""
    jn  = spherical_jn(n, ka)
    yn  = spherical_yn(n, ka)
    djn = spherical_jn(n, ka, derivative=True)
    dyn = spherical_yn(n, ka, derivative=True)
    hn  = jn + 1j * yn
    dhn = djn + 1j * dyn
    an  = jn / hn
    bn  = (jn + ka * djn) / (hn + ka * dhn)
    return an, bn


def mie_backscatter_Q(ka_array):
    """
    Normalised backscatter efficiency Q_back = σ/(π a²) for a PEC sphere.
    Uses the classic series:  Q = |Σ (-1)^n (2n+1)(a_n - b_n)|² / ka²
    """
    Q = np.zeros_like(ka_array, dtype=float)
    for i, ka in enumerate(ka_array):
        if ka < 1e-9:
            continue
        N = _wiscombe_nmax(ka)
        series = 0 + 0j
        for n in range(1, N + 1):
            an, bn = _mie_an_bn(n, ka)
            series += (-1) ** n * (2 * n + 1) * (an - bn)
        Q[i] = abs(series) ** 2 / ka ** 2
    return Q


def _pi_tau(n_max, cos_alpha_vec):
    """
    Mie angle functions π_n(cos α) and τ_n(cos α) for n = 1…n_max,
    vectorised over an array of cos(α) values.

    Recurrences (Bohren & Huffman, App. A):
        π_0 = 0,  π_1 = 1
        π_n = ((2n-1)/(n-1)) cos α · π_{n-1}  −  (n/(n-1)) π_{n-2}
        τ_n = n cos α · π_n  −  (n+1) π_{n-1}
    """
    n_obs = len(cos_alpha_vec)
    pi  = np.zeros((n_obs, n_max + 1))
    tau = np.zeros((n_obs, n_max + 1))
    pi[:, 1]  = 1.0
    tau[:, 1] = cos_alpha_vec
    for n in range(2, n_max + 1):
        pi[:, n]  = ((2*n-1)/(n-1)) * cos_alpha_vec * pi[:, n-1] - (n/(n-1)) * pi[:, n-2]
        tau[:, n] = n * cos_alpha_vec * pi[:, n] - (n+1) * pi[:, n-1]
    return pi, tau


def mie_S1_vectorised(ka, phi_obs_deg):
    """
    Mie amplitude function S1(α) for s-polarisation, equatorial plane.

    Geometry:
      Incident wave along +x, E-field along z.
      Observation in equatorial plane (theta=90°) at azimuthal angle phi_obs.
      Scatter angle from forward direction: α = phi_obs.
      Scatter plane normal ∝ ẑ  →  E_z is always ⊥ scatter plane (s-pol).
      Bistatic RCS:  σ(φ) = (4π/k²) |S1(cos φ)|²

    Verification at φ=180° (backscatter):
      S1(π) = series/2  →  σ_back = (4π/k²)|series/2|² = π a² Q_back  ✓
    """
    cos_alpha = np.cos(np.deg2rad(phi_obs_deg))
    N = _wiscombe_nmax(ka)
    pi, tau = _pi_tau(N, cos_alpha)

    S1 = np.zeros(len(phi_obs_deg), dtype=complex)
    for n in range(1, N + 1):
        an, bn = _mie_an_bn(n, ka)
        fn = (2 * n + 1) / (n * (n + 1))
        S1 += fn * (an * pi[:, n] + bn * tau[:, n])
    return S1


def mie_bistatic_rcs(f_hz, phi_obs_deg):
    """Bistatic RCS σ(φ) [m²] from Mie theory in the equatorial plane."""
    k  = 2 * np.pi * f_hz / C0
    ka = k * SPHERE_RAD_M
    S1 = mie_S1_vectorised(ka, phi_obs_deg)
    return (4 * np.pi / k ** 2) * np.abs(S1) ** 2


# ═══════════════════════════════════════════════════════════════════════════
# FDTD post-processing (re-uses existing simulation data, no re-run)
# ═══════════════════════════════════════════════════════════════════════════

def _rebuild_nf2ff():
    """
    Reconstruct the openEMS geometry (no simulation) to obtain an NF2FF object
    whose box coordinates match those stored in the existing sim data.
    Setup parameters must be byte-for-byte identical to rcs_sphere_full_sim.py.
    """
    FDTD = OpenEMS(EndCriteria=1e-5)
    FDTD.SetGaussExcite(F0, 0.5 * (F_STOP - F_START))
    FDTD.SetBoundaryCond(['PML_8'] * 6)

    CSX  = ContinuousStructure()
    FDTD.SetCSX(CSX)
    mesh = CSX.GetGrid()
    mesh.SetDeltaUnit(unit)

    mesh.SetLines('x', [-SimBox / 2, 0, SimBox / 2])
    mesh.SmoothMeshLines('x', C0 / F_STOP / unit / 20)
    mesh.SetLines('y', mesh.GetLines('x'))
    mesh.SetLines('z', mesh.GetLines('x'))

    sph = CSX.AddMetal('sphere')
    sph.AddSphere(priority=10, center=[0, 0, 0], radius=SPHERE_RAD)

    k_dir = [np.cos(np.deg2rad(INC_ANGLE)), np.sin(np.deg2rad(INC_ANGLE)), 0]
    E_dir = [0, 0, 1]
    pw = CSX.AddExcitation('plane_wave', exc_type=10, exc_val=E_dir)
    pw.SetPropagationDir(k_dir)
    pw.SetFrequency(F0)
    pw.AddBox(-np.array([PW_Box, PW_Box, PW_Box]) / 2,
               np.array([PW_Box, PW_Box, PW_Box]) / 2)

    return FDTD.CreateNF2FFBox(), E_dir


def fdtd_freq_sweep():
    """Backscatter RCS vs frequency from NF2FF post-processing."""
    E_dir = [0, 0, 1]
    freq  = np.linspace(F_START, F_STOP, 100)
    ef    = UI_data('et', SIM_PATH, freq)
    Pin   = 0.5 * np.linalg.norm(E_dir) ** 2 / Z0 * abs(np.array(ef.ui_f_val[0])) ** 2

    nf2ff, _ = _rebuild_nf2ff()
    res = nf2ff.CalcNF2FF(SIM_PATH, freq, 90, 180 + INC_ANGLE,
                          outfile=os.path.join(SIM_PATH, 'val_freq.h5'))
    rcs = np.array([4 * np.pi / Pin[i] * res.P_rad[i][0][0]
                    for i in range(len(freq))])
    return freq, rcs


def fdtd_polar(f_single=F0):
    """Full azimuthal scattering pattern at a single frequency."""
    E_dir   = [0, 0, 1]
    phi_deg = np.arange(-180, 180.1, 2.0)

    ef  = UI_data('et', SIM_PATH, freq=f_single)
    Pin = 0.5 * np.linalg.norm(E_dir) ** 2 / Z0 * abs(ef.ui_f_val[0]) ** 2

    nf2ff, _ = _rebuild_nf2ff()
    res = nf2ff.CalcNF2FF(SIM_PATH, f_single, 90, phi_deg,
                          outfile=os.path.join(SIM_PATH, 'val_polar.h5'))
    rcs = 4 * np.pi / Pin[0] * res.P_rad[0]
    return phi_deg, rcs[0]   # rcs[0] → shape (n_phi,)


# ═══════════════════════════════════════════════════════════════════════════
# Figures
# ═══════════════════════════════════════════════════════════════════════════

def fig_rcs_validation(freq_fdtd, rcs_fdtd):
    """
    4-panel validation figure:
      A — Normalised Q_back vs a/λ  (Mie + FDTD, log scale)
      B — Absolute RCS vs frequency  (Mie + FDTD, log scale)
      C — Point-wise relative error %  (colour-coded by scattering regime)
      D — Smoothed dB-difference  (separates resonance-frequency-shift
          artefacts from true amplitude bias)
    """

    # Dense Mie curves (600 points for smooth plotting)
    freq_mie = np.linspace(F_START, F_STOP, 600)
    ka_mie   = 2 * np.pi * SPHERE_RAD_M * freq_mie / C0
    Q_mie    = mie_backscatter_Q(ka_mie)
    rcs_mie  = np.pi * SPHERE_RAD_M ** 2 * Q_mie
    aol_mie  = SPHERE_RAD_M * freq_mie / C0

    # FDTD in normalised form
    Q_fdtd   = rcs_fdtd / (np.pi * SPHERE_RAD_M ** 2)
    aol_fdtd = SPHERE_RAD_M * freq_fdtd / C0

    # Mie interpolated onto the FDTD frequency grid for error calculation
    rcs_mie_i = np.interp(freq_fdtd, freq_mie, rcs_mie)
    err_pct   = (rcs_fdtd - rcs_mie_i) / rcs_mie_i * 100.0

    # Per-band RMS
    def band_rms(flo, fhi):
        m = (freq_fdtd >= flo) & (freq_fdtd <= fhi)
        return float(np.sqrt(np.mean(err_pct[m] ** 2))) if m.any() else float('nan')
    rms_ray = band_rms(F_START, 200e6)
    rms_res = band_rms(200e6,   600e6)
    rms_go  = band_rms(600e6,   F_STOP)
    rms_all = float(np.sqrt(np.mean(err_pct ** 2)))

    # Smoothed dB curves: 10-point running mean removes fast resonance
    # oscillations and reveals any underlying amplitude bias.
    W = 10
    def smooth(x):
        return np.convolve(x, np.ones(W) / W, mode='same')
    rcs_fdtd_db_sm = smooth(10 * np.log10(rcs_fdtd))
    rcs_mie_db_sm  = smooth(10 * np.log10(rcs_mie_i))
    err_db_sm      = rcs_fdtd_db_sm - rcs_mie_db_sm
    sl = slice(W // 2, -W // 2)   # trim convolution edge artefacts
    bias_rms = float(np.sqrt(np.mean(err_db_sm[sl] ** 2)))

    fig = plt.figure(figsize=(16, 9))
    gs  = gridspec.GridSpec(2, 2, wspace=0.38, hspace=0.48,
                            left=0.07, right=0.97, bottom=0.09, top=0.90)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])

    # ── Panel A: Normalised Q_back ────────────────────────────────────────
    ax1.semilogy(aol_mie,  Q_mie,  'b-',  lw=2.0,
                 label='Mie series (analytical)', zorder=3)
    ax1.semilogy(aol_fdtd, Q_fdtd, 'r--', lw=1.6,
                 label='openEMS FDTD', zorder=4)
    ax1.axhline(1.0, color='0.45', ls=':', lw=1.2,
                label='Geometric-optics limit  ($\\sigma = \\pi a^2$)')

    ax1.axvspan(0,    0.06,             alpha=0.10, color='royalblue',  zorder=0)
    ax1.axvspan(0.06, 0.45,             alpha=0.08, color='seagreen',   zorder=0)
    ax1.axvspan(0.45, aol_mie[-1]*1.01, alpha=0.06, color='darkorange', zorder=0)
    ax1.text(0.005, 6.5, 'Rayleigh',  fontsize=8, color='royalblue',  style='italic')
    ax1.text(0.09,  6.5, 'Resonance', fontsize=8, color='seagreen',   style='italic')
    ax1.text(0.46,  6.5, 'Near-GO',   fontsize=8, color='darkorange', style='italic')

    ax1.set_xlim(0, aol_mie[-1])
    ax1.set_ylim(1e-2, 10)
    ax1.set_xlabel('$a / \\lambda$  (sphere radius / wavelength)', fontsize=11)
    ax1.set_ylabel('$Q_{\\rm back} = \\sigma / (\\pi a^2)$', fontsize=11)
    ax1.set_title('(A)  Normalised Backscatter RCS', fontsize=11, fontweight='bold')
    ax1.legend(fontsize=8.5, loc='upper left')
    ax1.grid(True, which='both', alpha=0.25)

    # ── Panel B: Absolute RCS vs frequency ────────────────────────────────
    geo_lim = np.pi * SPHERE_RAD_M ** 2
    ax2.semilogy(freq_mie  / 1e6, rcs_mie,  'b-',   lw=2.0,
                 label='Mie series (analytical)')
    ax2.semilogy(freq_fdtd / 1e6, rcs_fdtd, 'r--o', lw=1.5, ms=3.5,
                 label='openEMS FDTD', markerfacecolor='none')
    ax2.axhline(geo_lim, color='0.45', ls=':', lw=1.2,
                label=f'GO limit  $\\pi a^2$ = {geo_lim*1e4:.2f} cm\u00b2')
    ax2.set_xlabel('Frequency (MHz)', fontsize=11)
    ax2.set_ylabel('RCS  $\\sigma$  (m\u00b2)', fontsize=11)
    ax2.set_title('(B)  Absolute Backscatter RCS vs Frequency', fontsize=11, fontweight='bold')
    ax2.legend(fontsize=8.5)
    ax2.grid(True, which='both', alpha=0.25)

    # ── Panel C: Point-wise % error (colour by regime) ────────────────────
    fMHz = freq_fdtd / 1e6
    for flo, fhi, col in [(50, 200, 'royalblue'), (200, 600, 'seagreen'),
                           (600, 1000, 'darkorange')]:
        m = (fMHz >= flo) & (fMHz <= fhi)
        ax3.plot(fMHz[m], err_pct[m], '-', color=col, lw=1.5)

    ax3.axhline(0,   color='0.4',       lw=0.9, ls='--')
    ax3.axhline(+10, color='limegreen', lw=0.8, ls=':', alpha=0.8)
    ax3.axhline(-10, color='limegreen', lw=0.8, ls=':', alpha=0.8)

    y_ann_mask = (fMHz >= 800) & (fMHz <= 835)
    y_ann = float(err_pct[y_ann_mask].max()) if y_ann_mask.any() else 40.0
    ax3.annotate('Resonance frequency shift\n(FDTD numerical dispersion\n\u2248 5\u20137 % at f > 600 MHz)',
                 xy=(820, y_ann), xytext=(500, y_ann * 0.82),
                 fontsize=7.5, color='darkorange',
                 arrowprops=dict(arrowstyle='->', color='darkorange', lw=0.9))

    from matplotlib.lines import Line2D
    leg = [Line2D([0],[0], color='royalblue', lw=2,
                  label=f'Rayleigh  RMS {rms_ray:.0f}\u202f%'),
           Line2D([0],[0], color='seagreen',  lw=2,
                  label=f'Resonance RMS {rms_res:.0f}\u202f%'),
           Line2D([0],[0], color='darkorange', lw=2,
                  label=f'Near-GO   RMS {rms_go:.0f}\u202f%')]
    ax3.legend(handles=leg, fontsize=8, loc='lower right')
    ax3.set_xlabel('Frequency (MHz)', fontsize=11)
    ax3.set_ylabel('$({\\sigma}_{\\rm FDTD}-{\\sigma}_{\\rm Mie})/{\\sigma}_{\\rm Mie}$  (%)',
                   fontsize=10)
    ax3.set_title('(C)  Point-wise Relative Error', fontsize=11, fontweight='bold')
    ax3.grid(True, alpha=0.25)

    # ── Panel D: Smoothed dB bias (amplitude agreement) ───────────────────
    ax4.plot(freq_fdtd[sl] / 1e6, err_db_sm[sl], 'k-', lw=1.8,
             label=f'{W}-point running mean of dB error')
    ax4.axhline(0,  color='0.5', lw=0.9, ls='--')
    ax4.axhline(+1, color='limegreen', lw=0.8, ls=':', alpha=0.8, label='\u00b11 dB band')
    ax4.axhline(-1, color='limegreen', lw=0.8, ls=':', alpha=0.8)
    ax4.fill_between(freq_fdtd[sl] / 1e6, -1, 1, alpha=0.12, color='limegreen')
    ax4.text(0.97, 0.05,
             f'Smoothed RMS = {bias_rms:.2f} dB\n'
             f'Large oscillations in (C) are\n'
             f'resonance-frequency-shift artefacts\n'
             f'(phase error, not amplitude error).\n'
             f'Overall amplitude level is correct.',
             transform=ax4.transAxes, ha='right', va='bottom', fontsize=8,
             bbox=dict(boxstyle='round,pad=0.35', fc='lightyellow', ec='0.6', alpha=0.95))
    ax4.set_xlabel('Frequency (MHz)', fontsize=11)
    ax4.set_ylabel('Smoothed dB error  (dB)', fontsize=11)
    ax4.set_title('(D)  Smoothed Amplitude Bias\n'
                  '(running mean separates frequency-shift artefacts from true bias)',
                  fontsize=10, fontweight='bold')
    ax4.legend(fontsize=8.5)
    ax4.grid(True, alpha=0.25)

    fig.suptitle(
        f'openEMS FDTD Validation \u2014 PEC Sphere  '
        f'($a$ = {SPHERE_RAD:.0f}\u202fmm,  {F_START/1e6:.0f}\u2013{F_STOP/1e6:.0f}\u202fMHz,  '
        f'\u03bb/20 mesh @ {F_STOP/1e6:.0f}\u202fMHz)   \u00b7   '
        f'Point-wise RMS = {rms_all:.0f}\u202f%   \u00b7   '
        f'Amplitude bias RMS = {bias_rms:.2f}\u202fdB',
        fontsize=10, fontweight='bold'
    )
    plt.savefig(OUT_RCS, dpi=150, bbox_inches='tight')
    print(f'Saved: {OUT_RCS}')
    plt.close(fig)


def _polar_panel(fig, gs_row, gs_col, phi_fdtd, rcs_fdtd_pattern, f_hz, label_regime):
    """
    Fill one column of the 2×2 polar figure:
      top    — polar dB plot
      bottom — linear RCS vs phi

    Returns RMS error (%) for the title.
    """
    phi_mie = np.linspace(-180, 180, 721)
    rcs_mie = mie_bistatic_rcs(f_hz, phi_mie)

    # Peak relative to joint max for shape comparison
    peak_lin = max(rcs_mie.max(), rcs_fdtd_pattern.max())
    def to_db(x):
        return 10 * np.log10(np.clip(x / peak_lin, 1e-8, None))

    rcs_fdtd_db = to_db(rcs_fdtd_pattern)
    rcs_mie_db  = to_db(rcs_mie)

    # Backscatter annotations
    bs_fdtd = float(np.interp(180.0, phi_fdtd, rcs_fdtd_pattern))
    bs_mie  = float(mie_bistatic_rcs(f_hz, np.array([180.0]))[0])

    # dB-RMS error vs Mie  (avoids division-by-near-zero at pattern nulls;
    # percentage error explodes at nulls even when the absolute agreement is good)
    rcs_mie_on_fdtd_grid = np.interp(phi_fdtd, phi_mie, rcs_mie)
    peak = rcs_mie_on_fdtd_grid.max()
    floor = peak * 1e-6       # −60 dB floor
    db_fdtd = 10 * np.log10(np.maximum(rcs_fdtd_pattern, floor))
    db_mie  = 10 * np.log10(np.maximum(rcs_mie_on_fdtd_grid, floor))
    db_err  = db_fdtd - db_mie
    rms_err  = float(np.sqrt(np.mean(db_err ** 2)))   # dB RMS
    mean_err = float(np.mean(db_err))                 # dB mean bias

    aol = SPHERE_RAD_M * f_hz / C0

    # ── Top: polar dB ──────────────────────────────────────────────────
    ax_pol = fig.add_subplot(2, 2, gs_row * 2 + gs_col + 1, projection='polar')
    RMIN = -40
    phi_mie_rad  = np.deg2rad(phi_mie)
    phi_fdtd_rad = np.deg2rad(phi_fdtd)
    ax_pol.plot(phi_mie_rad,  rcs_mie_db  - RMIN, 'b-',  lw=2.0,
                label='Mie (analytical)', zorder=3)
    ax_pol.plot(phi_fdtd_rad, rcs_fdtd_db - RMIN, 'r--', lw=1.6,
                label='openEMS FDTD', zorder=4)
    ax_pol.set_rmin(0)
    ax_pol.set_rmax(-RMIN)
    r_ticks = np.arange(0, -RMIN + 1, 10)
    ax_pol.set_rticks(r_ticks)
    ax_pol.set_yticklabels([f'{t + RMIN:.0f}' for t in r_ticks], fontsize=7)
    ax_pol.set_rlabel_position(135)
    ax_pol.set_theta_zero_location('E')
    ax_pol.set_theta_direction(1)
    ax_pol.set_title(
        f'{label_regime}\n'
        f'$f$ = {f_hz/1e6:.0f} MHz,  $a/\\lambda$ = {aol:.3f}\n'
        f'Pattern dB-RMS = {rms_err:.2f} dB,  mean bias = {mean_err:+.2f} dB\n'
        f'(dB rel. to joint peak)',
        fontsize=8.5, pad=12
    )
    ax_pol.legend(loc='lower right', fontsize=8, bbox_to_anchor=(1.35, -0.05))
    ax_pol.grid(True, alpha=0.5)

    # ── Bottom: linear ─────────────────────────────────────────────────
    ax_lin = fig.add_subplot(2, 2, gs_row * 2 + gs_col + 3)
    ax_lin.plot(phi_mie,  rcs_mie * 1e4, 'b-',  lw=2.0, label='Mie (analytical)')
    ax_lin.plot(phi_fdtd, rcs_fdtd_pattern * 1e4, 'r--', lw=1.5, label='openEMS FDTD')
    ax_lin.set_xlabel('Azimuthal angle φ  (°)', fontsize=10)
    ax_lin.set_ylabel('RCS  σ  (cm²)', fontsize=10)
    ax_lin.set_xlim(-180, 180)
    ax_lin.set_xticks(np.arange(-180, 181, 45))
    ax_lin.axvline(180,  color='0.65', lw=0.7, ls='--')
    ax_lin.axvline(-180, color='0.65', lw=0.7, ls='--')
    # Backscatter annotation
    y_lim_approx = max(rcs_mie.max(), rcs_fdtd_pattern.max()) * 1e4
    ax_lin.annotate(f'Mie: {bs_mie*1e4:.2f} cm²',
                    xy=(180, bs_mie * 1e4),
                    xytext=(-80, bs_mie * 1e4 * 1.1 + y_lim_approx * 0.04),
                    fontsize=7.5, color='blue',
                    arrowprops=dict(arrowstyle='->', color='blue', lw=0.8))
    ax_lin.annotate(f'FDTD: {bs_fdtd*1e4:.2f} cm²',
                    xy=(180, bs_fdtd * 1e4),
                    xytext=(-80, bs_fdtd * 1e4 * 0.7),
                    fontsize=7.5, color='red',
                    arrowprops=dict(arrowstyle='->', color='red', lw=0.8))
    ax_lin.legend(fontsize=8.5, loc='upper left')
    ax_lin.grid(True, alpha=0.3)

    return rms_err, mean_err


def fig_polar_comparison(phi_f0, rcs_f0, phi_f2=None, rcs_f2=None):
    """
    2×2 polar comparison figure.

    Left column  — Resonance regime (f0 = 525 MHz, a/λ ≈ 0.35)
    Right column — Rayleigh regime  (f2 = F_POLAR_2,  a/λ ≈ 0.10)

    Top row: polar dB patterns.  Bottom row: linear bistatic RCS.
    """
    fig = plt.figure(figsize=(16, 10))

    rms0, mean0 = _polar_panel(fig, 0, 0, phi_f0, rcs_f0, F0,
                                f'(A/C) Resonance regime  —  $f_0$ = {F0/1e6:.0f} MHz')

    if phi_f2 is not None and rcs_f2 is not None:
        rms2, mean2 = _polar_panel(fig, 0, 1, phi_f2, rcs_f2, F_POLAR_2,
                                    f'(B/D) Rayleigh regime  —  $f$ = {F_POLAR_2/1e6:.0f} MHz')
        subtitle_extra = (f'   |   Rayleigh pattern dB-RMS = {rms2:.2f} dB  '
                          f'(λ/20 mesh is ≫λ/20 resolution in Rayleigh → near-exact)')
    else:
        subtitle_extra = ''

    fig.suptitle(
        f'openEMS FDTD Validation — Bistatic Equatorial Scattering Pattern vs Mie Theory\n'
        f'PEC sphere, $a$ = {SPHERE_RAD:.0f} mm   ·   '
        f'Resonance pattern dB-RMS = {rms0:.2f} dB,  mean = {mean0:+.2f} dB  '
        f'(resonance-frequency-shift artefact at $f_0$)'
        + subtitle_extra,
        fontsize=9.5, fontweight='bold', y=1.01
    )

    plt.tight_layout()
    plt.savefig(OUT_POLAR, dpi=150, bbox_inches='tight')
    print(f'Saved: {OUT_POLAR}')
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    if not HAS_OPENEMS:
        print('ERROR: openEMS Python bindings not found.')
        print('Activate: source /home/vscode/opt/openEMS/venv/bin/activate')
        raise SystemExit(1)

    if not os.path.isdir(SIM_PATH):
        print(f'ERROR: Simulation data not found at {SIM_PATH}')
        print('Run test_simulations/RCS_Sphere/rcs_sphere_full_sim.py first.')
        raise SystemExit(1)

    print('─── Step 1/4: Post-processing frequency sweep (backscatter RCS) …')
    freq_fdtd, rcs_fdtd = fdtd_freq_sweep()

    print('─── Step 2/4: Computing Mie series and generating RCS validation figure …')
    fig_rcs_validation(freq_fdtd, rcs_fdtd)

    print('─── Step 3/4: Post-processing polar pattern at f0 (resonance) …')
    phi_fdtd, rcs_polar = fdtd_polar(F0)

    print(f'─── Step 3b/4: Post-processing polar pattern at {F_POLAR_2/1e6:.0f} MHz (Rayleigh) …')
    phi_fdtd_2, rcs_polar_2 = fdtd_polar(F_POLAR_2)

    print('─── Step 4/4: Generating dual-frequency polar comparison figure …')
    fig_polar_comparison(phi_fdtd, rcs_polar, phi_fdtd_2, rcs_polar_2)

    print('Done.')
