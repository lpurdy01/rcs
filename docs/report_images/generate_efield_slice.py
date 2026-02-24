"""
Generate a mid-plane (z=0) |E| slice image from the sphere FDTD E_dump.h5.
Saves to docs/report_images/sphere_efield_slice.png
"""
import h5py
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

H5_PATH = '/tmp/RCS_Sphere_Simulation_Full/E_dump.h5'
OUT_PATH = os.path.join(os.path.dirname(__file__), 'sphere_efield_slice.png')
SPHERE_RADIUS_MM = 0.15  # sphere radius in mm (matches simulation)

with h5py.File(H5_PATH, 'r') as f:
    x = f['Mesh/x'][:]  # mm
    y = f['Mesh/y'][:]  # mm
    z = f['Mesh/z'][:]  # mm
    E_real = f['FieldData/FD/f0_real'][:]  # shape (3, nx, ny, nz)
    E_imag = f['FieldData/FD/f0_imag'][:]  # shape (3, nx, ny, nz)

# Complex field magnitude |E|
E_complex = E_real + 1j * E_imag  # (3, 53, 53, 53)
E_mag = np.sqrt(np.sum(np.abs(E_complex)**2, axis=0))  # (53, 53, 53)

# Mid-plane slice at z=0
z_idx = np.argmin(np.abs(z))
E_slice = E_mag[:, :, z_idx]  # (nx, ny)

# Plot
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(
    E_slice.T,
    origin='lower',
    extent=[x.min(), x.max(), y.min(), y.max()],
    cmap='inferno',
    aspect='equal',
)
cbar = fig.colorbar(im, ax=ax)
cbar.set_label('|E| (V/m, normalised)', fontsize=10)

# Overlay sphere boundary
theta = np.linspace(0, 2 * np.pi, 300)
ax.plot(SPHERE_RADIUS_MM * np.cos(theta),
        SPHERE_RADIUS_MM * np.sin(theta),
        'w--', linewidth=1.2, label='Sphere boundary')
ax.legend(fontsize=8, loc='upper right')

ax.set_xlabel('x (mm)', fontsize=11)
ax.set_ylabel('y (mm)', fontsize=11)
ax.set_title('E-field magnitude — mid-plane slice (z = 0)', fontsize=12)

plt.tight_layout()
plt.savefig(OUT_PATH, dpi=150)
print(f'Saved: {OUT_PATH}')
