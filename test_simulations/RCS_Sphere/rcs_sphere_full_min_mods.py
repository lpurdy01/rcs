# -*- coding: utf-8 -*-
"""
Tutorials / Radar Cross Section of a Metal Sphere

This script runs the simulation and saves the data needed for post-processing.

Tested with:
 - Python 3.10
 - openEMS v0.0.35+

(c) 2016-2023 Thorsten Liebig <thorsten.liebig@gmx.de>
"""

### Import Libraries
import os
import numpy as np
import pickle  # For saving simulation parameters
from CSXCAD import ContinuousStructure
from openEMS import openEMS
from openEMS.physical_constants import *
from openEMS.ports import UI_data
import tempfile

### Setup the simulation
Sim_Path = os.path.join(tempfile.gettempdir(), 'RCS_Sphere_Simulation')
post_proc_only = False

unit = 1e-3  # all lengths in mm

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
mesh.SmoothMeshLines('x', C0 / f_stop / unit / 40)  # Cell size: lambda/20
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

# NF2FF calculation setup
nf2ff = FDTD.CreateNF2FFBox()

### Run the simulation
if not post_proc_only:
    FDTD.Run(Sim_Path, cleanup=False)  # Set cleanup=False to retain files

### Postprocessing & data saving
# Get Gaussian pulse strength at frequency f0
ef = UI_data('et', Sim_Path, freq=f0)
Pin = 0.5 * np.linalg.norm(E_dir) ** 2 / Z0 * abs(ef.ui_f_val[0]) ** 2

# Save Pin
np.save(os.path.join(Sim_Path, 'Pin.npy'), Pin)

# Save E_dir
np.save(os.path.join(Sim_Path, 'E_dir.npy'), E_dir)

# Calculate NF2FF at specific angles
angles_phi = np.arange(-180, 180.1, 2)
nf2ff_res = nf2ff.CalcNF2FF(Sim_Path, f0, 90, angles_phi)

# Save NF2FF results at f0
np.save(os.path.join(Sim_Path, 'nf2ff_phi.npy'), nf2ff_res.phi)
np.save(os.path.join(Sim_Path, 'nf2ff_P_rad.npy'), nf2ff_res.P_rad)

# Calculate RCS over frequency
freq = np.linspace(f_start, f_stop, 100)
ef_freq = UI_data('et', Sim_Path, freq)  # Time domain/freq domain voltage
Pin_freq = 0.5 * np.linalg.norm(E_dir) ** 2 / Z0 * abs(np.array(ef_freq.ui_f_val[0])) ** 2

# Save Pin_freq and freq
np.save(os.path.join(Sim_Path, 'Pin_freq.npy'), Pin_freq)
np.save(os.path.join(Sim_Path, 'freq.npy'), freq)

# Calculate NF2FF over frequency at specific angle
nf2ff_res_freq = nf2ff.CalcNF2FF(Sim_Path, freq, 90, 180 + inc_angle)

# Save NF2FF results over frequency
np.save(os.path.join(Sim_Path, 'nf2ff_P_rad_freq.npy'), nf2ff_res_freq.P_rad)

# Save simulation parameters for post-processing
sim_params = {
    'Sim_Path': Sim_Path,
    'unit': unit,
    'sphere_rad': sphere_rad,
    'inc_angle': inc_angle,
    'f_start': f_start,
    'f_stop': f_stop,
    'f0': f0,
}

# Save the simulation parameters to a file
params_file = os.path.join(Sim_Path, 'sim_params.pkl')
with open(params_file, 'wb') as f:
    pickle.dump(sim_params, f)

print(f"Simulation and data saving completed successfully. Data saved at: {Sim_Path}")
