# Documentation for __init__.py



# Documentation for _nf2ff.py

## Classes and Methods
### Class: _nf2ff
#### Method: AnalyseFile
_No documentation available_
#### Method: SetMirror
_No documentation available_
#### Method: SetRadius
_No documentation available_
#### Method: SetVerboseLevel
_No documentation available_
#### Method: Write2HDF5
_No documentation available_
#### Method: __init__
_No documentation available_
#### Method: __new__
```
Create and return a new object.  See help(type) for accurate signature. 
```
#### Method: __reduce__
_No documentation available_
#### Method: __setstate__
_No documentation available_

## Functions
### Function: AnalyseFile
_No documentation available_
### Function: SetMirror
_No documentation available_
### Function: SetRadius
_No documentation available_
### Function: SetVerboseLevel
_No documentation available_
### Function: Write2HDF5
_No documentation available_



# Documentation for openEMS.py

## Classes and Methods
### Class: openEMS
#### Method: AddEdges2Grid
```
AddEdges2Grid(primitives, dirs, **kw)

        Add the edges of the given primitives to the FDTD grid.

        :param dirs: primitives -- one or more primitives
        :param dirs: str -- 'x','y','z' or 'xy', 'yz' or 'xyz' or 'all'
```
#### Method: AddLumpedPort
```
AddLumpedPort(port_nr, R, start, stop, p_dir, excite=0, **kw)

        Add a lumped port with the given values and location.

        See Also
        --------
        openEMS.ports.LumpedPort
```
#### Method: AddMSLPort
```
AddMSLPort(port_nr, metal_prop, start, stop, prop_dir, exc_dir, excite=0, **kw)

        Add a microstrip transmission line port.

        See Also
        --------
        openEMS.ports.MSLPort
```
#### Method: AddRectWaveGuidePort
```
AddRectWaveGuidePort(port_nr, start, stop, p_dir, a, b, mode_name, excite=0, **kw)

        Add a rectilinear waveguide port.

        See Also
        --------
        openEMS.ports.RectWGPort
```
#### Method: AddWaveGuidePort
```
AddWaveGuidePort(self, port_nr, start, stop, p_dir, E_func, H_func, kc, excite=0, **kw)

        Add a arbitrary waveguide port.

        See Also
        --------
        openEMS.ports.WaveguidePort
```
#### Method: CreateNF2FFBox
```
CreateNF2FFBox(name='nf2ff', start=None, stop=None, **kw)

        Create a near-field to far-field box.

        This method will automatically adept the recording box to the current
        FDTD grid and boundary conditions.

        Notes
        -----
        * Make sure the mesh grid and all boundary conditions are finially defined.

        See Also
        --------
        openEMS.nf2ff.nf2ff
```
#### Method: GetCSX
_No documentation available_
#### Method: Run
```
Run(sim_path, cleanup=False, setup_only=False, verbose=None)

        Run the openEMS FDTD simulation.

        :param sim_path: str -- path to run in and create result data
        :param cleanup: bool -- remove existing sim_path to cleanup old results
        :param setup_only: bool -- only perform FDTD setup, do not run simulation
        :param verbose: int -- set the openEMS verbosity level 0..3

        Additional keyword parameter:
        :param numThreads: int -- set the number of threads (default 0 --> max)
```
#### Method: SetAbort
_No documentation available_
#### Method: SetBoundaryCond
```
SetBoundaryCond(BC)

        Set the boundary conditions for all six FDTD directions.

        Options:

        * 0 or 'PEC' : perfect electric conductor (default)
        * 1 or 'PMC' : perfect magnetic conductor, useful for symmetries
        * 2 or 'MUR' : simple MUR absorbing boundary conditions
        * 3 or 'PML_8' : PML absorbing boundary conditions

        :param BC: (8,) array or list -- see options above
```
#### Method: SetCellConstantMaterial
```
SetCellConstantMaterial(val)

        Set cell material averaging to assume constant material inside each primary cell. (Advanced option)

        :param val: bool -- Enable or Disable (default disabled)
```
#### Method: SetCoordSystem
```
SetCoordSystem(val)

        Set the coordinate system. 0 --> Cartesian (default), 1 --> cylindrical
```
#### Method: SetCSX
```
SetCSX(CSX)

        Set the CSXCAD Continuous Structure for CAD data handling.

        See Also
        --------
        CSXCAD.ContinuousStructure
```
#### Method: SetCustomExcite
```
SetCustomExcite(_str, f0, fmax)

        Set a custom function as excitation signal. The custom function is supplied as a string which gets
        parsed using `Function Parser for C++ <http://warp.povusers.org/FunctionParser/fparser.html>`_.

        :param _str: str -- Custom function as string literal
        :param f0: -- Base frequency.
        :param fmax: -- Maximum frequency.
```
#### Method: SetCylinderCoords
```
SetCylinderCoords()

        Enable use of cylindircal coordinates.

        See Also
        --------
        openEMS.SetMultiGrid
```
#### Method: SetDiracExcite
```
SetDiracExcite(f_max)

        Set a dirac pulse as excitation signal.

        :param f_max: float -- maximum simulated frequency in Hz.
```
#### Method: SetEndCriteria
```
SetEndCriteria(val)

        Set the end criteria value. E.g. 1e-6 for -60dB
```
#### Method: SetGaussExcite
```
SetGaussExcite(f0, fc)

        Set a Gaussian pulse as excitation signal.

        :param f0: float -- Center frequency in Hz.
        :param fc: float -- -20dB bandwidth in Hz.
```
#### Method: SetMaxTime
```
SetMaxTime(val)

        Set max simulation time for a max. number of timesteps.
```
#### Method: SetMultiGrid
```
SetMultiGrid(radii)

        Define radii at which a cylindrical multi grid should be defined.

        :param radii: array like, multigrid radii

        See Also
        --------
        openEMS.SetCylinderCoords
```
#### Method: SetNumberOfTimeSteps
```
SetNumberOfTimeSteps(val)

        Set the number of timesteps. E.g. 5e4 (default is 1e9)
```
#### Method: SetOverSampling
```
SetOverSampling(val)

        Set the time domain signal oversampling as multiple of the Nyquist-rate.
```
#### Method: SetSinusExcite
```
SetSinusExcite(f0)

        Set a sinusoidal signal as excitation signal.

        :param f0: float -- frequency in Hz.
```
#### Method: SetStepExcite
```
SetStepExcite(f_max)

        Set a step function as excitation signal.

        :param f_max: float -- maximum simulated frequency in Hz.
```
#### Method: SetTimeStep
```
SetTimeStep(val)

        Set/force the timestep. (Advanced option)

        It is highly recommended to not use this method! You may use the
        SetTimeStepFactor instead to reduce the time step if necessary!
```
#### Method: SetTimeStepFactor
```
SetTimeStepFactor(val)

        Set a time step factor (>0..1) to increase FDTD stability.

        :param val: float -- >0..1
```
#### Method: SetTimeStepMethod
```
SetTimeStepMethod(val)

        Set the time step calculation method. (Advanced option)

        Options:

        * 1: CFL criteria
        * 3: Advanced Rennings criteria (default)

        :param val: int -- 1 or 3 (See above)
```
#### Method: WelcomeScreen
```
Show the openEMS welcome screen. 
```
#### Method: __init__
_No documentation available_
#### Method: __new__
```
Create and return a new object.  See help(type) for accurate signature. 
```
#### Method: __reduce__
_No documentation available_
#### Method: __setstate__
_No documentation available_

## Functions
### Function: AddEdges2Grid
```
AddEdges2Grid(primitives, dirs, **kw)

        Add the edges of the given primitives to the FDTD grid.

        :param dirs: primitives -- one or more primitives
        :param dirs: str -- 'x','y','z' or 'xy', 'yz' or 'xyz' or 'all'
```
### Function: AddLumpedPort
```
AddLumpedPort(port_nr, R, start, stop, p_dir, excite=0, **kw)

        Add a lumped port with the given values and location.

        See Also
        --------
        openEMS.ports.LumpedPort
```
### Function: AddMSLPort
```
AddMSLPort(port_nr, metal_prop, start, stop, prop_dir, exc_dir, excite=0, **kw)

        Add a microstrip transmission line port.

        See Also
        --------
        openEMS.ports.MSLPort
```
### Function: AddRectWaveGuidePort
```
AddRectWaveGuidePort(port_nr, start, stop, p_dir, a, b, mode_name, excite=0, **kw)

        Add a rectilinear waveguide port.

        See Also
        --------
        openEMS.ports.RectWGPort
```
### Function: AddWaveGuidePort
```
AddWaveGuidePort(self, port_nr, start, stop, p_dir, E_func, H_func, kc, excite=0, **kw)

        Add a arbitrary waveguide port.

        See Also
        --------
        openEMS.ports.WaveguidePort
```
### Function: CreateNF2FFBox
```
CreateNF2FFBox(name='nf2ff', start=None, stop=None, **kw)

        Create a near-field to far-field box.

        This method will automatically adept the recording box to the current
        FDTD grid and boundary conditions.

        Notes
        -----
        * Make sure the mesh grid and all boundary conditions are finially defined.

        See Also
        --------
        openEMS.nf2ff.nf2ff
```
### Function: GetCSX
_No documentation available_
### Function: Run
```
Run(sim_path, cleanup=False, setup_only=False, verbose=None)

        Run the openEMS FDTD simulation.

        :param sim_path: str -- path to run in and create result data
        :param cleanup: bool -- remove existing sim_path to cleanup old results
        :param setup_only: bool -- only perform FDTD setup, do not run simulation
        :param verbose: int -- set the openEMS verbosity level 0..3

        Additional keyword parameter:
        :param numThreads: int -- set the number of threads (default 0 --> max)
```
### Function: SetAbort
_No documentation available_
### Function: SetBoundaryCond
```
SetBoundaryCond(BC)

        Set the boundary conditions for all six FDTD directions.

        Options:

        * 0 or 'PEC' : perfect electric conductor (default)
        * 1 or 'PMC' : perfect magnetic conductor, useful for symmetries
        * 2 or 'MUR' : simple MUR absorbing boundary conditions
        * 3 or 'PML_8' : PML absorbing boundary conditions

        :param BC: (8,) array or list -- see options above
```
### Function: SetCellConstantMaterial
```
SetCellConstantMaterial(val)

        Set cell material averaging to assume constant material inside each primary cell. (Advanced option)

        :param val: bool -- Enable or Disable (default disabled)
```
### Function: SetCoordSystem
```
SetCoordSystem(val)

        Set the coordinate system. 0 --> Cartesian (default), 1 --> cylindrical
```
### Function: SetCSX
```
SetCSX(CSX)

        Set the CSXCAD Continuous Structure for CAD data handling.

        See Also
        --------
        CSXCAD.ContinuousStructure
```
### Function: SetCustomExcite
```
SetCustomExcite(_str, f0, fmax)

        Set a custom function as excitation signal. The custom function is supplied as a string which gets
        parsed using `Function Parser for C++ <http://warp.povusers.org/FunctionParser/fparser.html>`_.

        :param _str: str -- Custom function as string literal
        :param f0: -- Base frequency.
        :param fmax: -- Maximum frequency.
```
### Function: SetCylinderCoords
```
SetCylinderCoords()

        Enable use of cylindircal coordinates.

        See Also
        --------
        openEMS.SetMultiGrid
```
### Function: SetDiracExcite
```
SetDiracExcite(f_max)

        Set a dirac pulse as excitation signal.

        :param f_max: float -- maximum simulated frequency in Hz.
```
### Function: SetEndCriteria
```
SetEndCriteria(val)

        Set the end criteria value. E.g. 1e-6 for -60dB
```
### Function: SetGaussExcite
```
SetGaussExcite(f0, fc)

        Set a Gaussian pulse as excitation signal.

        :param f0: float -- Center frequency in Hz.
        :param fc: float -- -20dB bandwidth in Hz.
```
### Function: SetMaxTime
```
SetMaxTime(val)

        Set max simulation time for a max. number of timesteps.
```
### Function: SetMultiGrid
```
SetMultiGrid(radii)

        Define radii at which a cylindrical multi grid should be defined.

        :param radii: array like, multigrid radii

        See Also
        --------
        openEMS.SetCylinderCoords
```
### Function: SetNumberOfTimeSteps
```
SetNumberOfTimeSteps(val)

        Set the number of timesteps. E.g. 5e4 (default is 1e9)
```
### Function: SetOverSampling
```
SetOverSampling(val)

        Set the time domain signal oversampling as multiple of the Nyquist-rate.
```
### Function: SetSinusExcite
```
SetSinusExcite(f0)

        Set a sinusoidal signal as excitation signal.

        :param f0: float -- frequency in Hz.
```
### Function: SetStepExcite
```
SetStepExcite(f_max)

        Set a step function as excitation signal.

        :param f_max: float -- maximum simulated frequency in Hz.
```
### Function: SetTimeStep
```
SetTimeStep(val)

        Set/force the timestep. (Advanced option)

        It is highly recommended to not use this method! You may use the
        SetTimeStepFactor instead to reduce the time step if necessary!
```
### Function: SetTimeStepFactor
```
SetTimeStepFactor(val)

        Set a time step factor (>0..1) to increase FDTD stability.

        :param val: float -- >0..1
```
### Function: SetTimeStepMethod
```
SetTimeStepMethod(val)

        Set the time step calculation method. (Advanced option)

        Options:

        * 1: CFL criteria
        * 3: Advanced Rennings criteria (default)

        :param val: int -- 1 or 3 (See above)
```
### Function: WelcomeScreen
```
Show the openEMS welcome screen. 
```



