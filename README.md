# RCS - Radar Cross Section Simulations with openEMS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![openEMS](https://img.shields.io/badge/openEMS-v0.0.34+-green.svg)](https://openems.de/)

This repository contains electromagnetic simulation examples and tools for computing Radar Cross Section (RCS) using openEMS, an open-source electromagnetic field solver.

## Overview

This project provides:
- **Example simulations** for various electromagnetic structures (antennas, waveguides, RCS targets)
- **Setup scripts** for installing openEMS and dependencies
- **Test targets** including STL models for RCS simulations
- **Simulation templates** for common electromagnetic scenarios

## Features

- RCS calculations for various geometries (spheres, cylinders, complex STL models)
- Antenna simulations (patch antennas, helical antennas)
- Waveguide and filter simulations
- Metamaterial parameter extraction (CRLH structures)

## Prerequisites

- **Operating System**: Ubuntu 22.04 or similar Linux distribution
- **Python**: 3.10 or higher
- **openEMS**: v0.0.34 or higher
- **CSXCAD**: Compatible version with openEMS

### Required System Packages

```bash
sudo apt update
sudo apt install -y build-essential cmake git
sudo apt install -y libhdf5-dev libvtk7-dev libboost-all-dev
sudo apt install -y libcgal-dev libtinyxml-dev qtbase5-dev libvtk7-qt-dev
sudo apt install -y python3-full python3-pip python-is-python3
```

### Required Python Packages

```bash
pip install numpy matplotlib cython h5py
```

## Installation

### 1. Install openEMS

Use the provided installation script:

```bash
bash setup_scripts_and_notes/install_openems.sh
```

Or follow the manual installation steps in the script.

### 2. Clone this Repository

```bash
git clone https://github.com/lpurdy01/rcs.git
cd rcs
```

### 3. Set Up Python Environment (Optional)

```bash
bash setup_scripts_and_notes/setup_venv.sh
source setup_scripts_and_notes/activate_venv.sh
```

## Usage

### Running Example Simulations

The `example_python_files/` directory contains several simulation examples:

#### RCS Sphere
Compute the radar cross section of a metallic sphere:
```bash
python example_python_files/RCS_Sphere.py
```

#### Simple Patch Antenna
Simulate a basic microstrip patch antenna:
```bash
python example_python_files/Simple_Patch_Antenna.py
```

#### Bent Patch Antenna
Simulate a conformal patch antenna on a curved surface:
```bash
python example_python_files/Bent_Patch_Antenna.py
```

#### Helical Antenna
Simulate a helical antenna design:
```bash
python example_python_files/Helical_Antenna.py
```

#### Rectangular Waveguide
Simulate propagation in a rectangular waveguide:
```bash
python example_python_files/Rect_Waveguide.py
```

#### Microstrip Line Notch Filter
Simulate a notch filter using microstrip lines:
```bash
python example_python_files/MSL_NotchFilter.py
```

#### CRLH Parameter Extraction
Extract metamaterial parameters from a CRLH structure:
```bash
python example_python_files/CRLH_Extraction.py
```

### Working with STL Targets

The `test_targets/` directory contains STL models that can be used for RCS simulations. These models can be imported into simulations for complex geometry analysis.

## Project Structure

```
rcs/
├── README.md                           # This file
├── example_python_files/               # Example simulation scripts
│   ├── RCS_Sphere.py                  # RCS of metallic sphere
│   ├── Simple_Patch_Antenna.py        # Basic patch antenna
│   ├── Bent_Patch_Antenna.py          # Conformal patch antenna
│   ├── Helical_Antenna.py             # Helical antenna
│   ├── Rect_Waveguide.py              # Rectangular waveguide
│   ├── MSL_NotchFilter.py             # Microstrip notch filter
│   └── CRLH_Extraction.py             # Metamaterial extraction
├── test_simulations/                   # Test simulation results
├── test_targets/                       # STL models for RCS targets
├── setup_scripts_and_notes/           # Installation and setup scripts
│   ├── install_openems.sh             # OpenEMS installation
│   ├── install_openscad.sh            # OpenSCAD installation
│   ├── install_paraview.sh            # ParaView installation
│   ├── setup_venv.sh                  # Python virtual environment
│   └── activate_venv.sh               # Activate virtual environment
└── AI_context_documentation/          # Context documentation for AI tools
```

## Visualization

Results can be visualized using:
- **ParaView**: For 3D field visualization (install with `setup_scripts_and_notes/install_paraview.sh`)
- **Matplotlib**: For plotting frequency responses and patterns (automatically used in examples)

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## References

- [openEMS Official Website](https://openems.de/)
- [openEMS GitHub Repository](https://github.com/thliebig/openEMS-Project)
- [openEMS Documentation](https://docs.openems.de/)

## Notes

- Simulation results are typically stored in temporary directories (e.g., `/tmp/`)
- The default openEMS installation path is `~/opt/openEMS/`
- Most example scripts are adapted from openEMS tutorials

## License

Please see the LICENSE file for details.

