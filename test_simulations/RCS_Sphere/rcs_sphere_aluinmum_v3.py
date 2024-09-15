# -*- coding: utf-8 -*-
"""
Hollow Aluminum Sphere RCS Simulation
"""
### Import Libraries
import os
import tempfile
import numpy as np

from CSXCAD import ContinuousStructure
from openEMS import openEMS
from openEMS.physical_constants import *

### Setup the simulation
Sim_Path = os.path.join(tempfile.gettempdir(), 'Hollow_Al_Sphere')
post_proc_only = False

unit = 1e-3  # All lengths in mm
sphere_outer_rad = 200  # Outer radius of the sphere in mm

# Frequency parameters
f_start = 50e6  # Start frequency
f_stop = 1000e6  # Stop frequency
f0 = 0.5 * (f_start + f_stop)  # Central frequency
wavelength = C0 / f0  # Wavelength in free space (in meters)
wavelength_unit = wavelength / unit  # Convert to simulation units (mm)

# Sphere thickness < 1/10th of the wavelength
thickness = wavelength / 20 # Thickness in meters
thickness_unit = thickness / unit  # Convert to simulation units (mm)
sphere_inner_rad = sphere_outer_rad - thickness_unit  # Inner radius of the hollow sphere in mm

# Incident angle (to x-axis) in degrees
inc_angle = 0

# Size of the simulation box
SimBox = 1200
PW_Box = 750

### Setup FDTD parameters & excitation function
FDTD = openEMS(EndCriteria=1e-5)
FDTD.SetGaussExcite(f0, 0.5 * (f_stop - f_start))
FDTD.SetBoundaryCond(['PML_8'] * 6)

### Setup Geometry & Mesh
CSX = ContinuousStructure()
FDTD.SetCSX(CSX)
mesh = CSX.GetGrid()
mesh.SetDeltaUnit(unit)

# Create mesh
mesh.SetLines('x', [-SimBox/2, 0, SimBox/2])
mesh.SmoothMeshLines('x', C0 / f_stop / unit / 40)  # cell size: lambda/20
mesh.SetLines('y', mesh.GetLines('x'))
mesh.SetLines('z', mesh.GetLines('x'))

### Create an aluminum hollow sphere
# Aluminum conductivity
sigma_aluminum = 3.77e7  # S/m

aluminum_material = CSX.AddMaterial('Aluminum', epsilon=1, kappa=sigma_aluminum)
# Outer sphere (aluminum shell)
aluminum_material.AddSphere(priority=10, center=[0, 0, 0], radius=sphere_outer_rad)
# Inner sphere (air)
air_material = CSX.AddMaterial('Air', epsilon=1, kappa=0)
air_material.AddSphere(priority=11, center=[0, 0, 0], radius=sphere_inner_rad)

### Plane wave excitation
k_dir = [np.cos(np.deg2rad(inc_angle)), np.sin(np.deg2rad(inc_angle)), 0]  # Plane wave direction
E_dir = [0, 0, 1]  # Plane wave polarization --> E_z

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
E_dump = CSX.AddDump('E_dump', dump_type=0, file_type=0, frequency=[f0])
E_dump.AddBox(start=start, stop=stop)

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
