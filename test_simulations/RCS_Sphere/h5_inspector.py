import h5py
import os


def inspect_h5_file(file_path):
    """
    Inspects the structure of an HDF5 file and prints its groups and datasets.

    Args:
        file_path (str): Path to the .h5 file to inspect.
    """
    print(f"Inspecting file: {file_path}")
    with h5py.File(file_path, 'r') as f:
        def print_structure(name, obj):
            print(f"{name}: {type(obj)}")

        f.visititems(print_structure)


if __name__ == '__main__':
    # Set your simulation path
    sim_path = '/tmp/RCS_Sphere_FieldDump'

    # List the nf2ff_E and nf2ff_H files in the simulation directory
    nf2ff_e_files = sorted([f for f in os.listdir(sim_path) if f.startswith('nf2ff_E') and f.endswith('.h5')])
    nf2ff_h_files = sorted([f for f in os.listdir(sim_path) if f.startswith('nf2ff_H') and f.endswith('.h5')])

    # Inspect one of the nf2ff_E files
    if nf2ff_e_files:
        inspect_h5_file(os.path.join(sim_path, nf2ff_e_files[0]))
    else:
        print(f"No nf2ff_E files found in {sim_path}")
