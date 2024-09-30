# -*- coding: utf-8 -*-
"""
Post-processing script for RCS Sphere simulation

This script loads the saved data and generates the RCS plots.
It allows you to iterate on the visualization without re-running the simulation.

Tested with:
 - Python 3.10
 - openEMS v0.0.35+

(c) 2016-2023 Thorsten Liebig <thorsten.liebig@gmx.de>
"""

### Import Libraries
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend suitable for headless servers
import matplotlib.pyplot as plt
import pickle  # For loading simulation parameters
import tempfile
from openEMS.physical_constants import Z0, C0

def post_process(sim_path):
    # Load simulation parameters
    params_file = os.path.join(sim_path, 'sim_params.pkl')
    if not os.path.exists(params_file):
        print(f"Simulation parameters not found in: {params_file}")
        return

    with open(params_file, 'rb') as f:
        params = pickle.load(f)

    # Extract parameters
    #unit = params['unit']
    sphere_rad = 0.2
    f_start = params['f_start']
    f_stop = params['f_stop']
    f0 = params['f0']

    # Load saved data
    Pin = np.load(os.path.join(sim_path, 'Pin.npy'))
    E_dir = np.load(os.path.join(sim_path, 'E_dir.npy'))
    nf2ff_phi = np.load(os.path.join(sim_path, 'nf2ff_phi.npy'))
    nf2ff_P_rad = np.load(os.path.join(sim_path, 'nf2ff_P_rad.npy'))

    freq = np.load(os.path.join(sim_path, 'freq.npy'))
    Pin_freq = np.load(os.path.join(sim_path, 'Pin_freq.npy'))
    nf2ff_P_rad_freq = np.load(os.path.join(sim_path, 'nf2ff_P_rad_freq.npy'))

    # Calculate RCS at f0
    RCS = 4 * np.pi / Pin[0] * nf2ff_P_rad[0]

    # Save the polar plot with logarithmic radial scale
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(nf2ff_phi, RCS[0], 'k-', linewidth=2)
    ax.grid(True)
    ax.set_rscale('log')  # Set radial axis to logarithmic scale
    ax.set_rlim([1e-3, 1e2])  # Set limits for radial axis
    ax.set_rticks([1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2])  # Set radial ticks
    ax.set_rlabel_position(135)  # Move radial labels away from plotted line
    plt.savefig(os.path.join(sim_path, 'RCS_polar_plot_log.png'))
    plt.close()
    print(f"RCS polar plot (log scale) saved as: {os.path.join(sim_path, 'RCS_polar_plot_log.png')}")

    # Calculate backscatter RCS over frequency
    back_scat = np.array([4 * np.pi / Pin_freq[fn] * nf2ff_P_rad_freq[fn][0][0] for fn in range(len(freq))])

    # Save RCS vs frequency plot
    plt.figure()
    plt.plot(freq / 1e6, back_scat, linewidth=2)
    plt.grid()
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('RCS ($m^2$)')
    plt.title('Radar Cross Section')
    plt.savefig(os.path.join(sim_path, 'RCS_vs_frequency.png'))
    plt.close()
    print(f"RCS vs Frequency plot saved as: {os.path.join(sim_path, 'RCS_vs_frequency.png')}")

    # Save normalized RCS plot
    plt.figure()
    plt.semilogy(sphere_rad / C0 * freq, back_scat / (np.pi * (sphere_rad) ** 2), linewidth=2)
    plt.ylim([1e-2, 1e1])
    plt.grid()
    plt.xlabel('Sphere radius / wavelength')
    plt.ylabel('RCS / ($\pi a^2$)')
    plt.title('Normalized Radar Cross Section')
    plt.savefig(os.path.join(sim_path, 'Normalized_RCS.png'))
    plt.close()
    print(f"Normalized RCS plot saved as: {os.path.join(sim_path, 'Normalized_RCS.png')}")

if __name__ == '__main__':
    # Set the simulation path
    sim_path = os.path.join(tempfile.gettempdir(), 'RCS_Little_Plane_Al')

    if not os.path.exists(sim_path):
        print(f"Simulation directory not found: {sim_path}")
    else:
        post_process(sim_path)
