sim k_dir [1,0,0] is wave approaching from x- direction.
sim k_dir [0,1,0] is wave approaching from y- direction.

nvm I needed a review of polarization and the right hand rule:

In openEMS, k_dir and E_dir are used to define the direction of wave propagation and the polarization of the electric field for the excitation, respectively.

Definitions:
k_dir (Wave Vector Direction): This specifies the direction from which the plane wave is propagating. It is a unit vector that defines the direction of the wave.
E_dir (Electric Field Direction): This specifies the direction of the electric field vector, which is perpendicular to the direction of propagation (k_dir). The direction of the magnetic field (H_dir) is determined by the right-hand rule (i.e., it's perpendicular to both k_dir and E_dir).
To set up a wave incoming from the +z direction:
Wave Propagation Direction (k_dir): For a wave incoming from the +z direction, k_dir should be [0, 0, -1]. This means the wave is propagating in the negative z-direction (incoming from +z).

Electric Field Direction (E_dir): Since the electric field is perpendicular to the propagation direction, you can set E_dir to be along either the x- or y-axis, depending on your desired polarization. For example:

For a wave polarized in the x-direction: E_dir = [1, 0, 0].
For a wave polarized in the y-direction: E_dir = [0, 1, 0].
Example:
To configure a plane wave propagating from the +z direction, with the electric field polarized along the x-axis, you can set:

python
Copy code
k_dir = [0, 0, -1]  # Wave propagating in the -z direction (incoming from +z)
E_dir = [1, 0, 0]   # Electric field polarized along the x-axis
This setup means:

The wave is moving from the +z direction towards the -z direction.
The electric field is oscillating along the x-axis (perpendicular to the propagation direction).
The magnetic field will automatically be set by the right-hand rule, oscillating in the y-axis.
If you want to change the polarization or the direction of the incoming wave, you can adjust k_dir and E_dir accordingly.

Recap on Right-Hand Rule:
The right-hand rule ensures that if you point your thumb in the direction of k_dir (propagation), and your index finger in the direction of E_dir (electric field), your middle finger will point in the direction of the magnetic field.


## Coordinate space in sims
Angles appear to be relative to x axis.

