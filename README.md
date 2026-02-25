# RCS — Radar Cross Section Simulations with openEMS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![openEMS](https://img.shields.io/badge/openEMS-v0.0.34+-green.svg)](https://openems.de/)

Open-source RCS simulation and analysis using **openEMS** (FDTD), with analytical Mie series validation and a full technical report.

**[Read the report →](docs/report.html)**

---

## What this is

This project models the radar cross section of physical geometries — a small UAV airframe and a canonical metal sphere — using openEMS, a free FDTD electromagnetic solver. It includes:

- A **validated FDTD workflow**: the PEC sphere result is compared against the exact Mie series solution across the Rayleigh, resonance, and near-geometric-optics scattering regimes.
- A **UAV RCS study**: engine cavity energy trapping, directional dependence, and how small changes in geometry affect observability.
- A **devcontainer** that builds openEMS from source automatically — clone and open in VS Code, no manual setup.
- A **rendered technical report** (`docs/report.html`) covering methodology, results, and validation.

---

## Quick start (devcontainer, recommended)

1. Install [VS Code](https://code.visualstudio.com/) and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
2. Clone this repo and open it in VS Code.
3. When prompted, click **Reopen in Container** (or `F1 → Dev Containers: Reopen in Container`).
4. The post-create script builds openEMS from source and installs Python bindings into a venv automatically (~10–20 min first build).
5. Activate the venv: `source /home/vscode/opt/openEMS/venv/bin/activate`

### Without the devcontainer

Install openEMS manually using the provided script:
```bash
bash setup_scripts_and_notes/install_openems.sh
```
Then activate the venv it creates before running any simulation scripts.

---

## Running the sphere validation

The sphere simulation is pre-validated. To reproduce the full run and generate all validation figures:

```bash
# 1. Run the FDTD simulation (~5–15 min depending on hardware)
source /home/vscode/opt/openEMS/venv/bin/activate
python test_simulations/RCS_Sphere/rcs_sphere_full_sim.py

# 2. Generate Mie vs FDTD comparison figures (reads existing sim data, no re-run)
python docs/report_images/validate_sphere_rcs.py

# 3. (Optional) Rebuild the HTML report
python docs/build_report.py
```

The validation covers:
- **Rayleigh regime** (50–200 MHz, a/λ < 0.13): < 5 % error — mesh is orders-of-magnitude finer than the wavelength.
- **Resonance regime** (200–600 MHz, a/λ 0.13–0.40): ~15 % point-wise RMS from resonance-frequency shift (numerical dispersion at λ/20); smoothed amplitude bias < 1 dB.
- **Near-GO regime** (600–1000 MHz, a/λ > 0.40): larger point-wise errors from the same frequency-shift artefact, but amplitude level remains correct.

---

## Viewing the report

The report is a single HTML file served from `docs/`. To view it locally:

```bash
cd docs && python3 -m http.server 8080
# then open http://localhost:8080/report.html
```

The devcontainer uses `--net=host`, so the server is accessible from the host machine at the same URL.

---

## Project structure

```
rcs/
├── .devcontainer/                    # VS Code devcontainer (builds openEMS from source)
│   ├── Dockerfile
│   ├── devcontainer.json
│   └── post-create.sh
│
├── test_simulations/
│   └── RCS_Sphere/
│       └── rcs_sphere_full_sim.py   # Main sphere FDTD simulation
│
├── docs/
│   ├── report_composition.md        # Report source (Markdown + image refs)
│   ├── build_report.py              # Builds report.html from the Markdown source
│   ├── report.html                  # Rendered technical report
│   └── report_images/
│       ├── validate_sphere_rcs.py       # Mie vs FDTD validation (post-processing only)
│       ├── generate_sphere_comparison.py# Standalone Mie+FDTD comparison (runs own sim)
│       ├── generate_efield_slice.py     # E-field slice from H5 dump
│       ├── sphere_validation_rcs.png    # 4-panel RCS validation figure
│       ├── sphere_validation_polar.png  # Bistatic pattern — Rayleigh + Resonance regimes
│       └── sphere_mie_vs_fdtd_comparison.png
│
├── example_python_files/            # openEMS tutorial scripts (GPL v3)
│   ├── RCS_Sphere.py
│   ├── Simple_Patch_Antenna.py
│   ├── Bent_Patch_Antenna.py
│   ├── Helical_Antenna.py
│   ├── Rect_Waveguide.py
│   ├── MSL_NotchFilter.py
│   └── CRLH_Extraction.py
│
├── test_targets/                    # STL models for RCS targets
├── setup_scripts_and_notes/         # Manual install scripts
└── AI_context_documentation/        # Context docs used during AI-assisted development
```

---

## Key physics and methods

**FDTD simulation**: openEMS solves Maxwell's equations on a Yee grid. The sphere simulation uses:
- Perfect electric conductor (PEC) sphere, radius 200 mm
- Gaussian pulse excitation, 50 MHz – 1 GHz
- λ/20 mesh at 1 GHz (finest feature: ~15 mm cells)
- PML absorbing boundaries (8-cell, all faces)
- Near-field to far-field (NF2FF) transformation for RCS extraction

**Mie series**: The analytical PEC sphere solution uses the classic coefficients:
- `a_n = j_n(ka) / h_n⁽¹⁾(ka)`
- `b_n = [x·j_n(x)]′ / [x·h_n⁽¹⁾(x)]′`
- Wiscombe (1980) convergence criterion for truncation order N
- Bistatic pattern via π_n/τ_n angular function recurrences (Bohren & Huffman, App. A)

**FDTD accuracy**: at λ/20 resolution, numerical dispersion causes resonance peaks to shift ~5–7 % in frequency at 1 GHz. This appears as oscillating ±errors in point-wise comparisons (a phase artefact, not an amplitude error). The smoothed dB amplitude bias is < 1 dB across the full 50 MHz – 1 GHz band.

---

## License

- **Repo code, documentation, setup scripts**: MIT License
- **`example_python_files/`**: GNU GPL v3 (derived from openEMS tutorials by Thorsten Liebig)

See `LICENSE` for details.

---

## References

- Bohren & Huffman, *Absorption and Scattering of Light by Small Particles* (1983)
- Wiscombe, W. J., "Improved Mie scattering algorithms," *Applied Optics* 19 (1980)
- [openEMS official site](https://openems.de/)
- [openEMS GitHub](https://github.com/thliebig/openEMS-Project)
