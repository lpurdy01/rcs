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
from stl_import import import_stl_into_openems

### Setup the simulation
# Define the simulation path
Sim_Path = os.path.join(tempfile.gettempdir(), 'RCS_STL_Simulation')
post_proc_only = False  # Set to False to run the simulation

unit = 1e-3  # All lengths in meters (unit conversion factor)

# Define the path to your STL file
stl_file_path = '/home/azureuser/repos/rcs/test_targets/stl_test_target_ASCI.stl'

# Incident angle (to x-axis) in degrees
inc_angle = 0

# Size of the simulation box
SimBox = 1200  # Simulation box size in mm
SimBox_y = 400
PW_Box = 600  # Plane wave excitation box size in mm
PW_Box_y = 200

# Convert lengths to meters for consistency
SimBox_m = SimBox * unit  # 1500 mm -> 1.5 meters
SimBox_y_m = SimBox * unit
PW_Box_m = PW_Box * unit  # 750 mm -> 0.75 meters
PW_Box_y_m = PW_Box_y * unit

### Setup FDTD parameters & excitation function
FDTD = openEMS(EndCriteria=1e-5)

f_start = 50e6  # Start frequency in Hz
f_stop = 1000e6  # Stop frequency in Hz
f0 = 0.5 * (f_start + f_stop)  # Center frequency

FDTD.SetGaussExcite(f0, 0.5 * (f_stop - f_start))
FDTD.SetBoundaryCond(['PML_8'] * 6)

### Setup Geometry & Mesh
CSX = ContinuousStructure()
FDTD.SetCSX(CSX)
mesh = CSX.GetGrid()

# Create mesh
mesh_size_m = SimBox_m  # Simulation domain size in meters
mesh_lines = [-mesh_size_m / 2, 0, mesh_size_m / 2]
mesh.SetLines('x', mesh_lines)
mesh.SetLines('z', mesh_lines)

mesh

# Mesh refinement parameters
mesh_resolution = C0 / f_stop / 20  # Cell size: lambda/20 at the highest frequency

# Smooth the mesh lines
mesh.SmoothMeshLines('x', mesh_resolution)
mesh.SmoothMeshLines('y', mesh_resolution)
mesh.SmoothMeshLines('z', mesh_resolution)

### Import the STL object
# Define transformations if needed
transform = {
    'Scale': [0.001, 0.001, 0.001],  # Scale from mm to meters if STL is in mm
    'Rotate': [0.0, 0.0, 0.0],  # No rotation
    'Translate': [0.0, 0.0, 0.0],  # No translation
}

# Import the STL object into the simulation
polyhedron = import_stl_into_openems(
    CSX,
    stl_file_path,
    material_name='stl_object',
    material_properties=None,  # Use PEC material
    priority=10,
    transform=transform
)
'''
# Refine the mesh around the STL object
bbox = polyhedron.GetBoundBox()
mesh.AddLine('x', bbox[0][0])
mesh.AddLine('x', bbox[1][0])
mesh.AddLine('y', bbox[0][1])
mesh.AddLine('y', bbox[1][1])
mesh.AddLine('z', bbox[0][2])
mesh.AddLine('z', bbox[1][2])

# Smooth the mesh lines again after adding the object boundaries
mesh.SmoothMeshLines('x', mesh_resolution)
mesh.SmoothMeshLines('y', mesh_resolution)
mesh.SmoothMeshLines('z', mesh_resolution)
'''

### Plane wave excitation
# Plane wave direction and polarization
k_dir = [np.cos(np.deg2rad(inc_angle)), np.sin(np.deg2rad(inc_angle)), 0]  # Plane wave direction
E_dir = [0, 0, 1]  # Plane wave polarization --> E_z

pw_exc = CSX.AddExcitation('plane_wave', exc_type=10, exc_val=E_dir)
pw_exc.SetPropagationDir(k_dir)
pw_exc.SetFrequency(f0)

# Define the plane wave excitation region in meters
start = np.array([-PW_Box_m / 2, -PW_Box_m / 2, -PW_Box_m / 2])
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
    nf2ff_res_freq = nf2ff.CalcNF2FF(Sim_Path, freq, 90, 180 + inc_angle)

    # Save NF2FF results over frequency
    np.save(os.path.join(Sim_Path, 'nf2ff_P_rad_freq.npy'), nf2ff_res_freq.P_rad)

    # Save simulation parameters for post-processing
    sim_params = {
        'Sim_Path': Sim_Path,
        'unit': unit,
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
