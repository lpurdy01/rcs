# -*- coding: utf-8 -*-
"""
Hollow Aluminum Sphere RCS Simulation
"""
### Import Libraries
import os, tempfile
import numpy as np
from pylab import *

from CSXCAD import ContinuousStructure
from openEMS import openEMS
from openEMS.physical_constants import *
from openEMS.ports import UI_data

### Setup the simulation
Sim_Path = os.path.join(tempfile.gettempdir(), 'Hollow_Al_Sphere')
post_proc_only = True

unit = 1e-3  # all lengths in mm
sphere_outer_rad = 200  # Outer radius of the sphere in mm

# Frequency parameters
f_start = 50e6  # start frequency
f_stop = 1000e6  # stop frequency
f0 = 500e6  # central frequency
wavelength = C0 / f0  # wavelength in free space

# Sphere thickness < 1/10th of the wavelength
thickness = wavelength / 10  # thickness of the aluminum shell
sphere_inner_rad = sphere_outer_rad - thickness  # Inner radius of the hollow sphere

# Incident angle (to x-axis) in degrees
inc_angle = 0

# Size of the simulation box
SimBox = 1200
PW_Box = 750

### Setup FDTD parameters & excitation function
FDTD = openEMS(EndCriteria=1e-5)
FDTD.SetGaussExcite(0.5 * (f_start + f_stop), 0.5 * (f_stop - f_start))
FDTD.SetBoundaryCond(['PML_8', 'PML_8', 'PML_8', 'PML_8', 'PML_8', 'PML_8'])

### Setup Geometry & Mesh
CSX = ContinuousStructure()
FDTD.SetCSX(CSX)
mesh = CSX.GetGrid()
mesh.SetDeltaUnit(unit)

# Define a coarse mesh for the entire simulation region
mesh.SetLines('x', [-SimBox / 2, 0, SimBox / 2])
mesh.SmoothMeshLines('x', C0 / f_stop / unit / 15)  # Coarse mesh (lambda/15 resolution)

# Define finer mesh near the sphere to resolve the thin aluminum shell
fine_res = C0 / (f0 * 20)  # Lambda/20 mesh resolution
mesh_x = np.linspace(-sphere_outer_rad - 10, sphere_outer_rad + 10, 20)  # Fine mesh for the sphere region
mesh.SmoothMeshLines('x', fine_res)  # Apply finer mesh

# Apply the same mesh refinement to y and z directions
mesh.SetLines('y', mesh_x)
mesh.SetLines('z', mesh_x)

### Create an aluminum hollow sphere
aluminum_material = CSX.AddMaterial('Aluminum', epsilon=1, kappa=3.77e7)  # Conductivity of Aluminum
aluminum_material.AddSphere(priority=10, center=[0, 0, 0], radius=sphere_outer_rad)
CSX.AddMaterial('Air').AddSphere(priority=9, center=[0, 0, 0], radius=sphere_inner_rad)  # Hollow interior

### Plane wave excitation
k_dir = [np.cos(np.deg2rad(inc_angle)), np.sin(np.deg2rad(inc_angle)), 0]  # plane wave direction
E_dir = [0, 0, 1]  # plane wave polarization --> E_z

pw_exc = CSX.AddExcitation('plane_wave', exc_type=10, exc_val=E_dir)
pw_exc.SetPropagationDir(k_dir)
pw_exc.SetFrequency(f0)

start = np.array([-PW_Box / 2, -PW_Box / 2, -PW_Box / 2])
stop = -start
pw_exc.AddBox(start, stop)

# Near-Field to Far-Field (NF2FF) calculation setup
nf2ff = FDTD.CreateNF2FFBox()

### Field Dumping for Visualization in ParaView ###
# Set up E-field dump (frequency-domain)
E_dump = CSX.AddDump('E_dump', dump_type=0, file_type=0, frequency=[f0])  # E-field frequency-domain dump
E_dump.AddBox(start=start, stop=stop)

# Set up H-field dump (frequency-domain)
H_dump = CSX.AddDump('H_dump', dump_type=1, file_type=0, frequency=[f0])  # H-field frequency-domain dump
H_dump.AddBox(start=start, stop=stop)

### Run the simulation
if 1:  # debugging only
    CSX_file = os.path.join(Sim_Path, 'RCS_Sphere.xml')
    if not os.path.exists(Sim_Path):
        os.mkdir(Sim_Path)
    CSX.Write2XML(CSX_file)
    from CSXCAD import AppCSXCAD_BIN
    os.system(AppCSXCAD_BIN + ' "{}"'.format(CSX_file))

### Run the simulation
if not post_proc_only:
    FDTD.Run(Sim_Path, cleanup=True)

print(f"Simulation completed successfully. Data saved at: {Sim_Path}")
