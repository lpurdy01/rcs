# -*- coding: utf-8 -*-
"""
Simulation Setup for RCS of an Object Imported from an STL File

This script runs the simulation using an STL file as the object under test,
saves the data needed for post-processing, and includes an E-field dump.

Tested with:
 - Python 3.10
 - openEMS v0.0.35+

(c) 2023 Your Name
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

# Import the helper function to import STL files
from stl_import import import_stl_into_openems, copy_stl_to_simulation_path

### Setup the simulation
# Define the simulation path
Sim_Path = os.path.join(tempfile.gettempdir(), 'No_target_0_calib')
post_proc_only = False  # Set to True to skip simulation run

# All lengths in meters
# Remove unit conversion; units are now in meters

# Incident angle (to x-axis) in degrees
inc_angle = 0

# Size of the simulation box in meters (set separately for x, y, z)
SimBox_x = 2  # meters
SimBox_y = 2  # meters
SimBox_z = 2  # meters

# Size of the plane wave excitation box in meters
PW_Box_x = 1  # meters
PW_Box_y = 1  # meters
PW_Box_z = 1  # meters

### Setup FDTD parameters & excitation function
FDTD = openEMS(EndCriteria=1e-3)

f_start = 50e6   # Start frequency in Hz
f_stop = 1000e6  # Stop frequency in Hz
f0 = 0.5 * (f_start + f_stop)  # Center frequency

FDTD.SetGaussExcite(f0, 0.5 * (f_stop - f_start))

FDTD.SetBoundaryCond(['PML_8'] * 6)

### Setup Geometry & Mesh
CSX = ContinuousStructure()
FDTD.SetCSX(CSX)
mesh = CSX.GetGrid()
# Not using SetDeltaUnit; units are in meters

# Create mesh
# Define the simulation space (in meters)
mesh_x_lines = [-SimBox_x / 2, 0, SimBox_x / 2]
mesh_y_lines = [-SimBox_y / 2, 0, SimBox_y / 2]
mesh_z_lines = [-SimBox_z / 2, 0, SimBox_z / 2]

mesh.SetLines('x', mesh_x_lines)
mesh.SetLines('y', mesh_y_lines)
mesh.SetLines('z', mesh_z_lines)

# Mesh refinement parameters
mesh_resolution = C0 / f_stop / 10  # Cell size: lambda/40 at highest frequency

# Smooth the mesh lines
mesh.SmoothMeshLines('x', mesh_resolution)
mesh.SmoothMeshLines('y', mesh_resolution)
mesh.SmoothMeshLines('z', mesh_resolution)

# Since we are not refining the mesh around the STL object, we skip adding mesh lines at its boundaries

### Plane wave excitation
# Plane wave direction and polarization
k_dir = [-1, 0, 0] # plane wave direction --> Wave is coming from the +x direction
E_dir = [0, 0, 1] # plane wave polarization --> E_z

pw_exc = CSX.AddExcitation('plane_wave', exc_type=10, exc_val=E_dir)
pw_exc.SetPropagationDir(k_dir)
pw_exc.SetFrequency(f0)

# Define the plane wave excitation region (in meters)
start = np.array([-PW_Box_x / 2, -PW_Box_y / 2, -PW_Box_z / 2])
stop = -start
pw_exc.AddBox(start, stop)

# NF2FF calculation setup
nf2ff = FDTD.CreateNF2FFBox()

### Add E-field dump
E_dump = CSX.AddDump('E_dump', dump_type=0, file_type=0, frequency=[f0])
E_dump.AddBox(start=start, stop=stop)

### Save the simulation setup to an XML file
# Create the simulation directory if it doesn't exist
if not os.path.exists(Sim_Path):
    os.makedirs(Sim_Path)

# Write the simulation setup to an XML file
CSX_file = os.path.join(Sim_Path, 'RCS_STL_Object.xml')
CSX.Write2XML(CSX_file)
print(f"Simulation setup saved to XML file: {CSX_file}")

# Optionally, use AppCSXCAD to visualize the simulation setup
try:
    from CSXCAD import AppCSXCAD_BIN
    os.system(AppCSXCAD_BIN + f' "{CSX_file}"')
except ImportError:
    print("AppCSXCAD_BIN not found. Please ensure that AppCSXCAD is installed and in your PATH.")

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
    nf2ff_res_freq = nf2ff.CalcNF2FF(Sim_Path, freq, 90, 0)

    # Save NF2FF results over frequency
    np.save(os.path.join(Sim_Path, 'nf2ff_P_rad_freq.npy'), nf2ff_res_freq.P_rad)

    # Save simulation parameters for post-processing
    sim_params = {
        'Sim_Path': Sim_Path,
        'f_start': f_start,
        'f_stop': f_stop,
        'f0': f0,
    }

    # Save the simulation parameters to a file
    params_file = os.path.join(Sim_Path, 'sim_params.pkl')
    with open(params_file, 'wb') as f:
        pickle.dump(sim_params, f)

    print(f"Simulation and data saving completed successfully. Data saved at: {Sim_Path}")
