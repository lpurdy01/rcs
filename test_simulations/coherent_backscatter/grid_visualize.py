# -*- coding: utf-8 -*-
"""
Post-processing script for NF2FF grid data

This script loads the saved NF2FF grid data and generates a log-scale image.

Tested with:
 - Python 3.10
 - openEMS v0.0.35+

(c) 2023 Your Name
"""

### Import Libraries
import os
import numpy as np
import matplotlib

matplotlib.use('Agg')  # Use non-interactive backend suitable for headless servers
import matplotlib.pyplot as plt
import tempfile


def plot_nf2ff_grid(sim_path, grid_file='nf2ff_grid.npy', save_fig=True):
    # Load the saved NF2FF grid data
    grid_file_path = os.path.join(sim_path, grid_file)
    if not os.path.exists(grid_file_path):
        print(f"NF2FF grid data not found: {grid_file_path}")
        return

    nf2ff_grid = np.load(grid_file_path)
    print(f"Loaded NF2FF grid data from: {grid_file_path}")

    Pin = np.load(os.path.join(sim_path, 'Pin.npy'))

    # Calculate RCS at f0
    RCS = 4 * np.pi / Pin[0] * nf2ff_grid

    # Set up the figure for the log-scale image
    plt.figure(figsize=(10, 8))
    plt.imshow(
        RCS,  # Transpose to match y-z orientation
        origin='lower',  # Origin at the bottom-left
        aspect='auto',  # Aspect ratio
        cmap='jet',  # Color map
        norm=matplotlib.colors.LogNorm(vmin=RCS.min(), vmax=RCS.max())
    )
    plt.colorbar(label='NF2FF Value (log scale)')
    plt.title('NF2FF Log-Scale Image')
    plt.xlabel('y-axis Index')
    plt.ylabel('z-axis Index')
    plt.grid(False)

    # Save the image
    if save_fig:
        fig_file_path = os.path.join(sim_path, 'nf2ff_log_scale_image.png')
        plt.savefig(fig_file_path)
        print(f"Log-scale image saved as: {fig_file_path}")
    else:
        plt.show()

    plt.close()


if __name__ == '__main__':
    # Set the simulation path
    sim_path = os.path.join(tempfile.gettempdir(), 'RCS_Sphere_Simulation_Backscatter_Vis')

    if not os.path.exists(sim_path):
        print(f"Simulation directory not found: {sim_path}")
    else:
        plot_nf2ff_grid(sim_path)
