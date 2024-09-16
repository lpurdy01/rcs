import os
import shutil

def import_stl_into_openems(CSX, stl_file_path, material_name='stl_object', material_properties=None, priority=10, transform=None):
    """
    Imports an STL file into the openEMS simulation using the AddPolyhedronReader method.

    Parameters:
    - CSX: The ContinuousStructure object from openEMS.
    - stl_file_path: Path to the STL file.
    - material_name: Name for the material.
    - material_properties: Dictionary with material properties, e.g., {'epsilon': 1.0, 'kappa': 0.0}
    - priority: Priority for the object in the simulation hierarchy.
    - transform: Dictionary with transformation parameters, e.g., {'Scale': [1,1,1], 'Rotate': [0,0,0], 'Translate': [0,0,0]}
    """

    # Create the material
    if material_properties is None:
        # Use PEC material
        material = CSX.AddMetal(material_name)
    else:
        # Create material with specified properties
        material = CSX.AddMaterial(material_name, **material_properties)

    # Add the STL object using AddPolyhedronReader
    polyhedron = material.AddPolyhedronReader(stl_file_path)
    polyhedron.ReadFile()
    polyhedron.SetPriority(priority)

    # Apply transformations if any
    if transform is not None:
        # Apply scaling
        if 'Scale' in transform:
            scale_factors = transform['Scale']
            # Apply scaling transformation
            polyhedron.AddTransform('Scale', scale_factors)

        # Apply rotation
        if 'Rotate' in transform:
            rotation_angles = transform['Rotate']  # In degrees
            # Apply rotations around x, y, z axes
            if rotation_angles[0] != 0:
                polyhedron.AddTransform('RotateAxis', 'x', rotation_angles[0])
            if rotation_angles[1] != 0:
                polyhedron.AddTransform('RotateAxis', 'y', rotation_angles[1])
            if rotation_angles[2] != 0:
                polyhedron.AddTransform('RotateAxis', 'z', rotation_angles[2])

        # Apply translation
        if 'Translate' in transform:
            translation_vector = transform['Translate']
            polyhedron.AddTransform('Translate', translation_vector)

    # Return the polyhedron object in case further manipulation is needed
    return polyhedron


import os
import shutil


def copy_stl_to_simulation_path(stl_file_path, sim_path):
    """
    Copies the STL file to the simulation directory.

    Args:
        stl_file_path (str): Path to the original STL file.
        sim_path (str): Path to the simulation directory where the STL file should be copied.

    Returns:
        str: The new path to the copied STL file in the simulation directory.
    """
    # Create the simulation directory if it doesn't exist
    if not os.path.exists(sim_path):
        os.makedirs(sim_path)

    # Define the new path for the STL file in the simulation directory
    new_stl_file_path = os.path.join(sim_path, os.path.basename(stl_file_path))

    # Copy the STL file to the simulation directory
    shutil.copyfile(stl_file_path, new_stl_file_path)

    print(f"STL file copied to: {new_stl_file_path}")
    return new_stl_file_path


