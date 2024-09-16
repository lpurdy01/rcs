// cylinder.scad
$fn = 10;  // Resolution of the cylinder (number of facets)

diameter = 200;   // Diameter in mm
height = 100;     // Height in mm (adjust as needed)

// Create a cylinder centered at the origin
cylinder(h = height, d = diameter, center = true);
