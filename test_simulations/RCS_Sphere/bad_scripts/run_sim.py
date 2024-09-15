# -*- coding: utf-8 -*-
"""
Part 2: Run the simulation and dump data for visualization

This script loads the previously generated XML file, runs the simulation, and stores
the results in the specified directory for future visualization.
"""

# Import required libraries
import os
from openEMS import openEMS
import tempfile
from CSXCAD import ContinuousStructure

# Define paths
Sim_Path = os.path.join(tempfile.gettempdir(), 'RCS_Sphere')
xml_file = os.path.join(Sim_Path, 'RCS_Sphere.xml')

# Initialize openEMS and CSXCAD objects
sim = openEMS()
csx = ContinuousStructure()

# Load the XML file into the CSX structure
csx.ReadFromXML(xml_file)

# Assign the CSX structure to the openEMS simulation
sim.SetCSX(csx)

# Set additional simulation parameters if needed
sim.SetEndCriteria(1e-6)  # Adjust end criteria if required

# Set boundary conditions if needed (already set in XML)
# sim.SetBoundaryCond(...)

# Run the simulation and store the results in Sim_Path
sim.Run(Sim_Path, cleanup=False, setup_only=False, verbose=3)

print(f"Simulation complete! Results are saved in: {Sim_Path}")
