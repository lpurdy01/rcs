# -*- coding: utf-8 -*-
"""
Post-processing script for accumulating Poynting vector biases across multiple timesteps

This script processes the .vtr files generated from openEMS, accumulates the biased Poynting vector over time,
and generates a log-scale image of the total biased Poynting vector magnitude.

Tested with:
 - Python 3.10
 - openEMS v0.0.35+
 - pyvista, numpy for VTR file handling

(c) 2023 Your Name
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from field_processing import read_vtr_file, calculate_poynting_vector  # Import the necessary functions
import tempfile

matplotlib.use('Agg')  # Use non-interactive backend suitable for headless servers


def accumulate_poynting_magnitude(sim_path, desired_direction=[-1, 0, 0], bias_factor=5, epsilon=1e-40, save_fig=True):
    """
    Accumulate Poynting vector biases over all available timesteps.

    Args:
    - sim_path: str, path to the simulation directory containing .vtr files
    - base_filename: str, base name of the E-field and H-field .vtr files without timestep
    - desired_direction: list of 3 floats, the direction to bias the Poynting vector towards
    - bias_factor: int, power to raise the Poynting vector projection to, increasing the bias towards aligned fields
    - epsilon: float, small value to avoid log(0)
    - save_fig: bool, whether to save the final image or display it

    Returns:
    - Accumulated Poynting vector magnitude biased in the specified direction.
    """

    # Find all VTR files in the directory
    e_vtr_files = sorted([f for f in os.listdir(sim_path) if f.startswith("E_dump_outside") and f.endswith(".vtr")])
    h_vtr_files = sorted([f for f in os.listdir(sim_path) if f.startswith("H_dump_outside") and f.endswith(".vtr")])

    if len(e_vtr_files) != len(h_vtr_files):
        raise ValueError("Mismatch between the number of E-field and H-field VTR files!")

    print(f"Found {len(e_vtr_files)} timesteps for accumulation.")

    # Initialize an array to accumulate the biased Poynting vector across timesteps
    accumulated_S_biased = None

    for e_vtr_file, h_vtr_file in zip(e_vtr_files, h_vtr_files):
        # Load the E-field and H-field data for the current timestep
        E_field = read_vtr_file(os.path.join(sim_path, e_vtr_file), field='E-Field')
        H_field = read_vtr_file(os.path.join(sim_path, h_vtr_file), field='H-Field')

        E_field = np.array(E_field)
        H_field = np.array(H_field)

        # Calculate the Poynting vector components
        Sx, Sy, Sz = calculate_poynting_vector(E_field, H_field)

        # Normalize the desired direction
        desired_direction = np.array(desired_direction)
        desired_direction = desired_direction / np.linalg.norm(desired_direction)

        # Compute the dot product between Poynting vector and desired direction
        S_projection = Sx * desired_direction[0] + Sy * desired_direction[1] + Sz * desired_direction[2]

        # Apply bias by raising the absolute value of the dot product to the power of 'bias_factor'
        S_biased = np.sign(S_projection) * np.abs(S_projection) ** bias_factor

        # Clip negative values or set them to zero (if you only want to show waves going back along [-1, 0, 0])
        S_biased = np.maximum(S_biased, 0)

        # Accumulate the biased Poynting vector over time
        if accumulated_S_biased is None:
            accumulated_S_biased = S_biased
        else:
            accumulated_S_biased += S_biased

    # Add a small epsilon to avoid log(0)
    accumulated_S_biased_log = np.log10(accumulated_S_biased + epsilon)

    # Print the range to verify the data
    print("Accumulated S_biased range:", np.min(accumulated_S_biased), np.max(accumulated_S_biased))

    # Set up the figure for the log-scale image
    plt.figure(figsize=(10, 8))
    plt.imshow(
        accumulated_S_biased_log,  # Log scale of the accumulated biased Poynting vector
        origin='lower',  # Origin at the bottom-left
        aspect='auto',  # Aspect ratio
        cmap='jet',  # Color map
    )
    plt.colorbar(label=f'Accumulated Biased Poynting Vector (log scale) [Bias Factor: {bias_factor}]')
    plt.title(f'Accumulated Poynting Vector Projection with Bias (Log-Scale) in yz-plane')
    plt.xlabel('y-axis Index')
    plt.ylabel('z-axis Index')
    plt.grid(False)

    # Save the image
    if save_fig:
        fig_file_path = os.path.join(sim_path, f'accumulated_biased_poynting_log_scale_image.png')
        plt.savefig(fig_file_path)
        print(f"Log-scale image of accumulated biased Poynting vector projection saved as: {fig_file_path}")
    else:
        plt.show()

    plt.close()


if __name__ == '__main__':
    # Set the simulation path and base filename
    sim_path = os.path.join(tempfile.gettempdir(), 'RCS_Little_Plane_Al_hi_frq')

    if not os.path.exists(sim_path):
        print(f"Simulation directory not found: {sim_path}")
    else:
        accumulate_poynting_magnitude(sim_path)
