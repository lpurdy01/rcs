# Example Simulation Scripts

This directory contains example electromagnetic simulation scripts using openEMS.

## License Notice

**Important**: The example files in this directory are derived from openEMS tutorials originally authored by Thorsten Liebig and are licensed under the **GNU General Public License v3 (GPL v3)**.

- **Copyright**: (c) 2015-2023 Thorsten Liebig
- **License**: GPL v3 (see LICENSE file in this directory)
- **Source**: https://github.com/thliebig/openEMS-Project

Each file retains its original copyright notice. If you modify or distribute these files, you must comply with the GPL v3 license terms.

## Available Examples

### Antenna Simulations

#### Simple_Patch_Antenna.py
A basic microstrip patch antenna simulation. This example demonstrates:
- Patch antenna design on a substrate
- S-parameter calculation
- Radiation pattern computation
- Impedance bandwidth analysis

**Key Parameters:**
- Patch dimensions: 32mm × 40mm
- Operating frequency range: ~2.4 GHz
- Substrate material properties

#### Bent_Patch_Antenna.py
A conformal patch antenna on a curved surface. Shows:
- Modeling antennas on non-planar surfaces
- Effects of bending on antenna performance
- Conformal antenna analysis

#### Helical_Antenna.py
A helical antenna design demonstrating:
- Circular polarization
- Broadband characteristics
- Axial mode operation

### RCS (Radar Cross Section) Simulations

#### RCS_Sphere.py
Calculates the radar cross section of a metallic sphere. Features:
- Plane wave excitation
- RCS computation across frequency range
- Comparison with analytical solutions
- PML boundary conditions

**Key Parameters:**
- Sphere radius: 200mm
- Frequency range: 50 MHz - 1 GHz
- Incident angle: 0° (configurable)

### Waveguide and Filter Simulations

#### Rect_Waveguide.py
Rectangular waveguide simulation showing:
- Waveguide modes and propagation
- S-parameters
- Field distributions
- Cutoff frequency analysis

#### MSL_NotchFilter.py
Microstrip line notch filter design:
- Filter frequency response
- Impedance matching
- Transmission line analysis

### Metamaterial Simulations

#### CRLH_Extraction.py
Composite Right/Left-Handed (CRLH) transmission line parameter extraction:
- S-parameter to constitutive parameter extraction
- Dispersion analysis
- Metamaterial characterization

## Running the Examples

### Basic Usage

```bash
python example_python_files/RCS_Sphere.py
```

### Customizing Parameters

Each script contains editable parameters near the top of the file. Common parameters include:

- **Frequency ranges**: `f_start`, `f_stop`
- **Geometry dimensions**: Various dimension variables
- **Simulation box size**: `SimBox`, boundary conditions
- **Material properties**: Permittivity, conductivity

### Output

Simulation results are typically saved to:
- `/tmp/` directory (Linux/Unix)
- Temporary directory on Windows

Results include:
- Field data (HDF5 format)
- S-parameters
- Far-field patterns
- Visualization files for ParaView

## Viewing Results

### Using ParaView
```bash
paraview /tmp/[simulation_name]/[result_file].vts
```

### Using Matplotlib
Most examples generate plots automatically using matplotlib.

## Modifying Examples

When creating custom simulations based on these examples:

1. Copy the example script
2. Modify geometry parameters
3. Adjust frequency range as needed
4. Update simulation box size if necessary
5. Run and verify results

## Requirements

- Python 3.10+
- openEMS v0.0.34+
- CSXCAD
- NumPy, Matplotlib, h5py

See the main README.md for installation instructions.

## Notes

- Examples are adapted from openEMS tutorials
- Simulation time varies based on frequency range and mesh density
- Higher frequency simulations require finer mesh resolution
- PML (Perfectly Matched Layer) boundaries reduce simulation domain size

## Troubleshooting

**Issue**: Simulation takes too long
- **Solution**: Reduce frequency range or increase wavelength-based mesh size

**Issue**: Unexpected results
- **Solution**: Check mesh convergence by refining the mesh

**Issue**: Memory errors
- **Solution**: Reduce simulation box size or frequency range

## Additional Resources

- [openEMS Documentation](https://docs.openems.de/)
- [openEMS Tutorials](https://docs.openems.de/Tutorials)
- [CSXCAD Documentation](https://docs.openems.de/CSXCAD)
