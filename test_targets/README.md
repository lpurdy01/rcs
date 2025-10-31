# Test Targets for RCS Simulations

This directory contains 3D models and geometry files used as test targets for Radar Cross Section (RCS) simulations.

## Available Models

### STL Files

STL (STereoLithography) files are 3D mesh models that can be imported into openEMS simulations for complex geometry analysis.

#### cylinder_ascii.stl
A cylindrical target model in ASCII STL format.
- Format: ASCII STL
- Use case: RCS of cylindrical objects
- Can be used for bistatic or monostatic RCS calculations

#### little_plane_asci_mesh.stl
A simple aircraft-like geometry for RCS studies.
- Format: ASCII STL
- Use case: Basic aircraft RCS simulation
- Useful for understanding RCS patterns of aerospace shapes

#### stl_test_target_ASCI.stl
General test target in ASCII STL format.
- Format: ASCII STL
- Use case: Generic RCS testing and validation

### OpenSCAD Files

#### cylinder.scad
OpenSCAD source file for generating cylindrical models.
- Parametric design
- Can be modified to create cylinders of different dimensions
- Export to STL using OpenSCAD or the provided shell script

#### export_cylinder.sh
Shell script for exporting OpenSCAD models to STL format.
```bash
bash export_cylinder.sh
```

## Using STL Models in Simulations

### Importing STL in openEMS/Python

```python
from CSXCAD import ContinuousStructure

CSX = ContinuousStructure()

# Import STL file
stl_file = 'test_targets/cylinder_ascii.stl'
CSX.AddMetal('target')  # Add metal property
CSX.AddPolyhedronReader('target', filename=stl_file)
```

### Coordinate System Considerations

- Ensure STL model is properly scaled
- Check coordinate system orientation
- Center the model appropriately in the simulation domain

## Creating Custom Targets

### Using OpenSCAD

1. Install OpenSCAD (see `setup_scripts_and_notes/install_openscad.sh`)
2. Create or modify `.scad` files
3. Export to STL:
   ```bash
   openscad -o output.stl input.scad
   ```

### STL File Formats

- **ASCII STL**: Human-readable, larger file size
- **Binary STL**: Compact, faster to load
- openEMS supports both formats

### Mesh Quality

For accurate simulations:
- Use appropriate mesh density
- Avoid degenerate triangles
- Ensure watertight geometry (closed surfaces)

## Example RCS Simulation with STL Target

```python
import os
from CSXCAD import ContinuousStructure
from openEMS import openEMS

# Setup
FDTD = openEMS()
CSX = ContinuousStructure()
FDTD.SetCSX(CSX)

# Import target
stl_file = 'test_targets/cylinder_ascii.stl'
CSX.AddMetal('target')
CSX.AddPolyhedronReader('target', filename=stl_file)

# Set up plane wave excitation for RCS
# ... (additional simulation setup)

# Run simulation
FDTD.Run()
```

## Applications

These test targets are useful for:
- **RCS verification**: Compare with analytical or measured data
- **Algorithm validation**: Test RCS calculation methods
- **Geometry effects**: Study how shape affects radar returns
- **Frequency response**: Analyze RCS across frequency bands
- **Polarization studies**: Investigate co-pol and cross-pol responses

## File Formats Supported

- **.stl**: STereoLithography (both ASCII and binary)
- **.scad**: OpenSCAD parametric models
- **.ply**: Polygon File Format (via conversion)

## Tips

1. **Scale appropriately**: Ensure model dimensions match your wavelength
2. **Mesh resolution**: Finer mesh for higher frequencies
3. **Simplify when possible**: Complex models increase simulation time
4. **Validate results**: Compare simple geometries with analytical solutions

## Converting Between Formats

### STL to other formats
Use tools like MeshLab or Blender for format conversion.

### ASCII to Binary STL
Many CAD programs can convert between ASCII and binary STL formats.

## References

- [OpenSCAD User Manual](https://openscad.org/documentation.html)
- [STL File Format Specification](https://en.wikipedia.org/wiki/STL_(file_format))
- [openEMS STL Import Examples](https://docs.openems.de/)

## Notes

- Large STL files may significantly increase simulation time
- Consider mesh decimation for complex models
- Test with simple geometries before complex ones
