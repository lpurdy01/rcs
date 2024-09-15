# -*- coding: utf-8 -*-
"""
Tutorials / Radar Cross Section of a Metal Sphere
"""

### Import Libraries
import os
import tempfile
import numpy as np
import pickle  # For saving simulation parameters
from CSXCAD import ContinuousStructure
from openEMS import openEMS
from openEMS.physical_constants import *
from openEMS.ports import UI_data

### Setup the simulation
Sim_Path = os.path.join(tempfile.gettempdir(), 'RCS_Sphere_FieldDump')
post_proc_only = False

unit = 1e-3  # All lengths in mm

sphere_rad = 200  # Sphere radius in mm

inc_angle = 0  # Incident angle (to x-axis) in degrees

# Size of the simulation box
SimBox = 1200
PW_Box = 750

### Setup FDTD parameters & excitation function
FDTD = openEMS(EndCriteria=1e-5)

f_start = 50e6  # Start frequency
f_stop = 1000e6  # Stop frequency
f0 = 0.5 * (f_start + f_stop)  # Center frequency
FDTD.SetGaussExcite(f0, 0.5 * (f_stop - f_start))

FDTD.SetBoundaryCond(['PML_8'] * 6)

### Setup Geometry & Mesh
CSX = ContinuousStructure()
FDTD.SetCSX(CSX)
mesh = CSX.GetGrid()
mesh.SetDeltaUnit(unit)

# Create mesh
mesh.SetLines('x', [-SimBox / 2, 0, SimBox / 2])
mesh.SmoothMeshLines('x', C0 / f_stop / unit / 20)  # Cell size: lambda/20
mesh.SetLines('y', mesh.GetLines('x'))
mesh.SetLines('z', mesh.GetLines('x'))

### Create a metal sphere and plane wave source
sphere_metal = CSX.AddMetal('sphere')  # Create a perfect electric conductor (PEC)
sphere_metal.AddSphere(priority=10, center=[0, 0, 0], radius=sphere_rad)

# Plane wave excitation
k_dir = [np.cos(np.deg2rad(inc_angle)), np.sin(np.deg2rad(inc_angle)), 0]  # Plane wave direction
E_dir = [0, 0, 1]  # Plane wave polarization --> E_z

pw_exc = CSX.AddExcitation('plane_wave', exc_type=10, exc_val=E_dir)
pw_exc.SetPropagationDir(k_dir)
pw_exc.SetFrequency(f0)

start = np.array([-PW_Box / 2, -PW_Box / 2, -PW_Box / 2])
stop = -start
pw_exc.AddBox(start, stop)

# Setup NF2FF (Near-Field to Far-Field transformation)
nf2ff = FDTD.CreateNF2FFBox()

### Field Dumping for Visualization in ParaView
# Set up E-field dump (time-domain)
E_dump = CSX.AddDump('E_dump', dump_type=0, file_type=0)
E_dump.AddBox(start=start, stop=stop)  # Add the box defining the region

# Set up H-field dump (time-domain)
H_dump = CSX.AddDump('H_dump', dump_type=1, file_type=0)
H_dump.AddBox(start=start, stop=stop)  # Add the box defining the region

### Save Simulation Parameters for Post-Processing
sim_params = {
    'Sim_Path': Sim_Path,
    'unit': unit,
    'sphere_rad': sphere_rad,
    'inc_angle': inc_angle,
    'f_start': f_start,
    'f_stop': f_stop,
    'f0': f0,
    'E_dir': E_dir,
}
# Save the simulation parameters to a file
params_file = os.path.join(Sim_Path, 'sim_params.pkl')
os.makedirs(Sim_Path, exist_ok=True)
with open(params_file, 'wb') as f:
    pickle.dump(sim_params, f)

### Run the simulation
if not post_proc_only:
    FDTD.Run(Sim_Path, cleanup=False)  # Set cleanup to False to retain files

### Perform NF2FF Calculations and Save Results
# Get Gaussian pulse strength at frequency f0
ef = UI_data('et', Sim_Path, freq=f0)
Pin = 0.5 * np.linalg.norm(E_dir)**2 / Z0 * abs(ef.ui_f_val[0])**2

# Calculate NF2FF at specific angles
nf2ff_res = nf2ff.CalcNF2FF(Sim_Path, f0, 90, np.arange(-180, 180.1, 2))
# Save NF2FF results
nf2ff_res.SaveNF2FF(os.path.join(Sim_Path, 'nf2ff_results_f0.h5'))

# Calculate NF2FF over frequency
freq = np.linspace(f_start, f_stop, 100)
ef = UI_data('et', Sim_Path, freq)
Pin = 0.5 * np.linalg.norm(E_dir)**2 / Z0 * abs(np.array(ef.ui_f_val[0]))**2

nf2ff_res_freq = nf2ff.CalcNF2FF(Sim_Path, freq, 90, 180 + inc_angle)
# Save NF2FF results over frequency
nf2ff_res_freq.SaveNF2FF(os.path.join(Sim_Path, 'nf2ff_results_freq.h5'))

# Also save Pin for use in post-processing
np.save(os.path.join(Sim_Path, 'Pin_f0.npy'), Pin)
np.save(os.path.join(Sim_Path, 'Pin_freq.npy'), Pin)

print(f"Simulation and NF2FF calculations completed successfully. Data saved at: {Sim_Path}")
