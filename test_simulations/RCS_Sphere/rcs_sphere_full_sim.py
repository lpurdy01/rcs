# -*- coding: utf-8 -*-
"""
Tutorials / Radar Cross Section of a Metal Sphere

This script runs the simulation and performs the NF2FF calculations and post-processing.
"""

### Import Libraries
import os
import tempfile
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend suitable for headless servers
import matplotlib.pyplot as plt
from CSXCAD import ContinuousStructure
from openEMS import openEMS
from openEMS.physical_constants import *
from openEMS.ports import UI_data

### Setup the simulation
Sim_Path = os.path.join(tempfile.gettempdir(), 'RCS_Sphere_Simulation_Full')
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
# Set up E-field dump (frequency-domain)
E_dump = CSX.AddDump('E_dump', dump_type=10, file_type=1, frequency=[f0])
E_dump.AddBox(start=start, stop=stop)  # Add the box defining the region

# Set up H-field dump (frequency-domain)
H_dump = CSX.AddDump('H_dump', dump_type=11, file_type=1, frequency=[f0])
H_dump.AddBox(start=start, stop=stop)  # Add the box defining the region

### Run the simulation
if not post_proc_only:
    FDTD.Run(Sim_Path, cleanup=False)  # Set cleanup to False to retain files

### Post-Processing
# Get Gaussian pulse strength at frequency f0
ef = UI_data('et', Sim_Path, freq=f0)
Pin = 0.5 * np.linalg.norm(E_dir)**2 / Z0 * abs(ef.ui_f_val[0])**2

# Calculate NF2FF at specific angles
nf2ff_res = nf2ff.CalcNF2FF(Sim_Path, f0, 90, np.arange(-180, 180.1, 2))
RCS = 4 * np.pi / Pin[0] * nf2ff_res.P_rad[0]

# Create the polar plot of RCS
plt.figure()
ax = plt.subplot(111, polar=True)
ax.plot(np.deg2rad(nf2ff_res.phi), RCS[0], 'k-', linewidth=2)
ax.grid(True)
plt.savefig(os.path.join(Sim_Path, 'RCS_polar_plot.png'))
print(f"RCS polar plot saved as: {os.path.join(Sim_Path, 'RCS_polar_plot.png')}")
plt.close()

# Calculate and plot RCS over frequency
freq = np.linspace(f_start, f_stop, 100)
ef = UI_data('et', Sim_Path, freq)
Pin = 0.5 * np.linalg.norm(E_dir)**2 / Z0 * abs(np.array(ef.ui_f_val[0]))**2

nf2ff_res = nf2ff.CalcNF2FF(Sim_Path, freq, 90, 180 + inc_angle)

back_scat = np.array([4 * np.pi / Pin[fn] * nf2ff_res.P_rad[fn][0][0] for fn in range(len(freq))])

# Plot radar cross section over frequency
plt.figure()
plt.plot(freq / 1e6, back_scat, linewidth=2)
plt.grid()
plt.xlabel('Frequency (MHz)')
plt.ylabel('RCS ($m^2$)')
plt.title('Radar Cross Section')
plt.savefig(os.path.join(Sim_Path, 'RCS_vs_frequency.png'))
print(f"RCS vs Frequency plot saved as: {os.path.join(Sim_Path, 'RCS_vs_frequency.png')}")
plt.close()

# Plot normalized radar cross section
plt.figure()
plt.semilogy(sphere_rad * unit / C0 * freq, back_scat / (np.pi * (sphere_rad * unit)**2), linewidth=2)
plt.ylim([1e-2, 1e1])
plt.grid()
plt.xlabel('Sphere radius / wavelength')
plt.ylabel('RCS / ($\pi a^2$)')
plt.title('Normalized Radar Cross Section')
plt.savefig(os.path.join(Sim_Path, 'Normalized_RCS.png'))
print(f"Normalized RCS plot saved as: {os.path.join(Sim_Path, 'Normalized_RCS.png')}")
plt.close()

print(f"Simulation and post-processing completed successfully. Data saved at: {Sim_Path}")
