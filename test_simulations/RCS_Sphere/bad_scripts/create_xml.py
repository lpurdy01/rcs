# -*- coding: utf-8 -*-
"""
Part 1: Generate XML file for CSXCAD visualization

This script generates the XML file to view and verify the simulation setup in the CSXCAD GUI.
"""

# Import Libraries
import os
import tempfile
from CSXCAD import ContinuousStructure
from openEMS import openEMS
from openEMS.physical_constants import *

# Setup paths
Sim_Path = os.path.join(tempfile.gettempdir(), 'RCS_Sphere')
if not os.path.exists(Sim_Path):
    os.mkdir(Sim_Path)

# Setup the simulation unit and geometry
unit = 1e-3  # All lengths in mm
sphere_rad = 200
SimBox = 1200
PW_Box = 750

# Setup FDTD parameters & excitation function
FDTD = openEMS(EndCriteria=1e-5)

f_start = 50e6  # start frequency
f_stop = 1000e6  # stop frequency
f0 = 0.5 * (f_start + f_stop)
fc = 0.5 * (f_stop - f_start)

# Set Gaussian excitation (same as the original script)
FDTD.SetGaussExcite(f0, fc)

# Boundary conditions (PML_8 in all directions)
FDTD.SetBoundaryCond(['PML_8', 'PML_8', 'PML_8', 'PML_8', 'PML_8', 'PML_8'])

# Create geometry & mesh
CSX = ContinuousStructure()
FDTD.SetCSX(CSX)
mesh = CSX.GetGrid()
mesh.SetDeltaUnit(unit)

# Create mesh
mesh.SetLines('x', [-SimBox / 2, 0, SimBox / 2])
mesh.SmoothMeshLines('x', C0 / f_stop / unit / 20)  # Cell size: lambda/20
mesh.SetLines('y', mesh.GetLines('x'))
mesh.SetLines('z', mesh.GetLines('x'))

# Create a metal sphere
sphere_metal = CSX.AddMetal('sphere')  # Create a perfect electric conductor (PEC)
sphere_metal.AddSphere(priority=10, center=[0, 0, 0], radius=sphere_rad)

# Plane wave excitation (correcting excitation)
k_dir = [1, 0, 0]  # plane wave direction (incident along x-axis)
E_dir = [0, 0, 1]  # plane wave polarization --> E_z

pw_exc = CSX.AddExcitation('plane_wave', exc_type=10, exc_val=E_dir)
pw_exc.SetPropagationDir(k_dir)
pw_exc.SetFrequency(f0)

start = [-PW_Box / 2, -PW_Box / 2, -PW_Box / 2]
stop = [PW_Box / 2, PW_Box / 2, PW_Box / 2]
pw_exc.AddBox(start, stop)

# Generate and save the XML file for CSXCAD visualization
CSX_file = os.path.join(Sim_Path, 'RCS_Sphere.xml')
CSX.Write2XML(CSX_file)

print(f"XML file saved at: {CSX_file}")
