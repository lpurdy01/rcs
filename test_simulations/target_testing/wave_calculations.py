import numpy as np

def calculate_wave_direction(heading, elevation):
    """
    Calculate the wave direction (k_dir) based on the heading and elevation.

    Parameters:
    - heading: Angle of the wave direction in the x-z plane (degrees).
    - elevation: Angle of the wave direction relative to the horizontal plane (degrees).

    Returns:
    - k_dir: A 3-element list representing the direction vector.
    """
    heading_rad = np.deg2rad(heading)
    elevation_rad = np.deg2rad(elevation)

    k_dir_x = np.cos(elevation_rad) * np.cos(heading_rad)
    k_dir_z = np.cos(elevation_rad) * np.sin(heading_rad)
    k_dir_y = np.sin(elevation_rad)

    return [k_dir_x, k_dir_y, k_dir_z]

if __name__ == '__main__':
    # Define the heading and elevation of the incoming wave
    heading = 90  # Degrees, rotation in the x-z plane
    elevation = 0  # Degrees, angle from horizontal plane (negative means downward)

    # Calculate the wave direction based on the heading and elevation
    k_dir = calculate_wave_direction(heading, elevation)
    print(k_dir)

    # The electric field polarization should always be vertical (in the y-direction)
    E_dir = [0, 1, 0]  # Vertically polarized wave