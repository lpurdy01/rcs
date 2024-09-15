# -*- coding: utf-8 -*-
"""
Radar Cross Section (RCS) Simulation of a Metal Sphere
"""
import os
import tempfile
import numpy as np
from openEMS import openEMS
from CSXCAD import ContinuousStructure
from openEMS.physical_constants import *

# Setup the simulation directory
Sim_Path = os.path.join(tempfile.gettempdir(), 'RCS_Sphere')
if not os.path.exists(Sim_Path):
    os.mkdir(Sim_Path)

# Setup simulation parameters
unit = 1e-3  # All lengths in mm
sphere_rad = 200
SimBox = 1200
PW_Box = 750

# FDTD parameters & Gaussian excitation
f_start = 50e6  # start frequency
f_stop = 1000e6  # stop frequency
f0 = 0.5 * (f_start + f_stop)
fc = 0.5 * (f_stop - f_start)

FDTD = openEMS(EndCriteria=1e-5)
FDTD.SetGaussExcite(f0, fc)
FDTD.SetBoundaryCond(['PML_8', 'PML_8', 'PML_8', 'PML_8', 'PML_8', 'PML_8'])

# Create Geometry & Mesh
CSX = ContinuousStructure()
FDTD.SetCSX(CSX)
mesh = CSX.GetGrid()
mesh.SetDeltaUnit(unit)

# Create the mesh lines
mesh.SetLines('x', [-SimBox / 2, 0, SimBox / 2])
mesh.SmoothMeshLines('x', C0 / f_stop / unit / 20)
mesh.SetLines('y', mesh.GetLines('x'))
mesh.SetLines('z', mesh.GetLines('x'))

# Create a metal sphere (PEC)
sphere_metal = CSX.AddMetal('sphere')
sphere_metal.AddSphere(priority=10, center=[0, 0, 0], radius=sphere_rad)

# Plane wave excitation
inc_angle = 0  # incident angle (to x-axis) in degrees
k_dir = [np.cos(np.deg2rad(inc_angle)), np.sin(np.deg2rad(inc_angle)), 0]  # plane wave direction
E_dir = [0, 0, 1]  # plane wave polarization --> E_z
pw_exc = CSX.AddExcitation('plane_wave', exc_type=10, exc_val=E_dir)
pw_exc.SetPropagationDir(k_dir)
pw_exc.SetFrequency(f0)

# Set the box for the plane wave
start = np.array([-PW_Box / 2, -PW_Box / 2, -PW_Box / 2])
stop = -start
pw_exc.AddBox(start, stop)

# Write the XML (for visualization or debugging)
CSX_file = os.path.join(Sim_Path, 'RCS_Sphere.xml')
CSX.Write2XML(CSX_file)

# NF2FF (Near-Field to Far-Field) box setup
nf2ff = FDTD.CreateNF2FFBox()

# Run the simulation
FDTD.Run(Sim_Path, cleanup=True, setup_only=False, verbose=3)

print("Simulation completed successfully. Data saved at:", Sim_Path)
