import pyvista as pv
def read_vtr_file(vtr_file, field='E-Field'):
    """
    Read a .vtr (VTK Rectilinear Grid) file using PyVista and return the E-field and H-field data as numpy arrays.

    Args:
    - vtr_file: str, the file path of the VTR file.

    Returns:
    - E_field: numpy array, the E-field data.
    - H_field: numpy array, the H-field data.
    """
    # Load the .vtr file using PyVista
    grid = pv.read(vtr_file)

    # Extract the E-field and H-field arrays from the grid
    field_data = grid.point_data[field]

    # Reshape the data back into 3D arrays
    dims = grid.dimensions
    field = field_data.reshape(dims[0], dims[1], dims[2], 3, order='F')

    return field


def calculate_poynting_vector(E_field, H_field):
    """
    Calculate the Poynting vector (S = E x H) from E-field and H-field components.
    Args:
    - E_field: numpy array, E-field data.
    - H_field: numpy array, H-field data.

    Returns:
    - poynting_vector: numpy arrays Sx, Sy, Sz
    """
    # Access the components of the E-field and H-field
    Ex, Ey, Ez = E_field[0, ..., 0], E_field[0, ..., 1], E_field[0, ..., 2]
    Hx, Hy, Hz = H_field[0, ..., 0], H_field[0, ..., 1], H_field[0, ..., 2]

    # Calculate the Poynting vector components
    Sx = Ey * Hz - Ez * Hy
    Sy = Ez * Hx - Ex * Hz
    Sz = Ex * Hy - Ey * Hx

    return Sx, Sy, Sz