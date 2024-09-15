# Documentation for CSRectGrid.py

## Classes and Methods
### Class: CoordinateSystem
#### Method: _generate_next_value_
```
Generate the next value when not given.

        name: the name of the member
        start: the initial start value or None
        count: the number of existing members
        last_value: the last value assigned or None
```
#### Method: __init__
_No documentation available_
#### Method: __new__
_No documentation available_

### Class: CSRectGrid
#### Method: AddLine
```
AddLine(ny, lines)

        Add an array of lines. This will *not* clear the previous defined lines in
        the given direction.

        :param ny: int or str -- direction definition
        :param lines: array -- list of lines to be added in the given direction
```
#### Method: Clear
```
Clear all lines and delta unit. 
```
#### Method: ClearLines
```
ClearLines(ny)

        Clear all lines in a given direction `ny`.

        :param ny: int or str -- direction definition
```
#### Method: GetDeltaUnit
```
Get the drawing unit for all mesh lines. 
```
#### Method: GetLine
```
GetLine(ny, idx)

        Get the line in a given direction `ny` and index

        :param ny: int or str -- direction definition
        :param idx: int  -- line index
```
#### Method: GetLines
```
GetLines(ny, do_sort=False)

        Get all lines in a given direction `ny`.

        :param ny: int or str -- direction definition
        :param do_sort: bool  -- sort lines
```
#### Method: GetMeshType
_No documentation available_
#### Method: GetQtyLines
```
GetQtyLines(ny)

        :param ny: int or str -- direction definition
```
#### Method: GetSimArea
```
Get the simulation area as defined by the mesh.

        :returns: (2,3) array -- Simulation domain box
```
#### Method: IsValid
```
Check if the mesh is valid. That is at least 2 mesh lines in all directions. 
```
#### Method: SetDeltaUnit
```
SetDeltaUnit(unit)

        Set the drawing unit for all mesh lines. Default is 1 (m)
```
#### Method: SetLines
```
SetLines(ny, lines)

        Set an array of lines. This will clear all previous defined lines in
        the given direction.

        :param ny: int or str -- direction definition
        :param lines: array -- list of lines to be set in the given direction
```
#### Method: SetMeshType
```
SetMeshType(cs_type)

        Set the coordinate system type (Cartesian or cylindrical) for this mesh.

        :param cs_type: coordinate system (0 : Cartesian, 1 : Cylindrical)
```
#### Method: SmoothMeshLines
```
SmoothMeshLines(ny, max_res, ratio=1.5)

        Smooth all mesh lines in the given direction with a max. allowed resolution.

        :param ny: int or str -- direction definition or 'all' for all directions
        :param max_res: float -- max. allowed resolution
        :param ratio:   float -- max. allowed ration of mesh smoothing de/increase
```
#### Method: Snap2LineNumber
```
Snap2LineNumber(ny, value)

        Find a fitting mesh line index for the given direction and value.
```
#### Method: Sort
```
Sort(ny='all')

        Sort mesh lines in the given direction or all directions.
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
### Function: SmoothMeshLines
```
This is the form of a docstring.

    Parameters
    ----------

    lines : list
        List of mesh lines to be smoothed
    max_res : float
        Maximum allowed resolution, resulting mesh will always stay below that value
    ratio : float
        Ratio of increase or decrease of neighboring mesh lines
```
### Function: _generate_next_value_
```
Generate the next value when not given.

        name: the name of the member
        start: the initial start value or None
        count: the number of existing members
        last_value: the last value assigned or None
```
### Function: AddLine
```
AddLine(ny, lines)

        Add an array of lines. This will *not* clear the previous defined lines in
        the given direction.

        :param ny: int or str -- direction definition
        :param lines: array -- list of lines to be added in the given direction
```
### Function: Clear
```
Clear all lines and delta unit. 
```
### Function: ClearLines
```
ClearLines(ny)

        Clear all lines in a given direction `ny`.

        :param ny: int or str -- direction definition
```
### Function: GetDeltaUnit
```
Get the drawing unit for all mesh lines. 
```
### Function: GetLine
```
GetLine(ny, idx)

        Get the line in a given direction `ny` and index

        :param ny: int or str -- direction definition
        :param idx: int  -- line index
```
### Function: GetLines
```
GetLines(ny, do_sort=False)

        Get all lines in a given direction `ny`.

        :param ny: int or str -- direction definition
        :param do_sort: bool  -- sort lines
```
### Function: GetMeshType
_No documentation available_
### Function: GetQtyLines
```
GetQtyLines(ny)

        :param ny: int or str -- direction definition
```
### Function: GetSimArea
```
Get the simulation area as defined by the mesh.

        :returns: (2,3) array -- Simulation domain box
```
### Function: IsValid
```
Check if the mesh is valid. That is at least 2 mesh lines in all directions. 
```
### Function: SetDeltaUnit
```
SetDeltaUnit(unit)

        Set the drawing unit for all mesh lines. Default is 1 (m)
```
### Function: SetLines
```
SetLines(ny, lines)

        Set an array of lines. This will clear all previous defined lines in
        the given direction.

        :param ny: int or str -- direction definition
        :param lines: array -- list of lines to be set in the given direction
```
### Function: SetMeshType
```
SetMeshType(cs_type)

        Set the coordinate system type (Cartesian or cylindrical) for this mesh.

        :param cs_type: coordinate system (0 : Cartesian, 1 : Cylindrical)
```
### Function: SmoothMeshLines
```
SmoothMeshLines(ny, max_res, ratio=1.5)

        Smooth all mesh lines in the given direction with a max. allowed resolution.

        :param ny: int or str -- direction definition or 'all' for all directions
        :param max_res: float -- max. allowed resolution
        :param ratio:   float -- max. allowed ration of mesh smoothing de/increase
```
### Function: Snap2LineNumber
```
Snap2LineNumber(ny, value)

        Find a fitting mesh line index for the given direction and value.
```
### Function: Sort
```
Sort(ny='all')

        Sort mesh lines in the given direction or all directions.
```



# Documentation for ParameterObjects.py

## Classes and Methods
### Class: ParameterSet
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



# Documentation for Utilities.py

## Functions
### Function: CheckNyDir
```
CheckNyDir(ny)

    Translate directions like 'x'/'y' or 'z' into 0/1 or 2.
    Raise an assertion error otherwise.

    :param ny: int or str
    :returns: int -- direction as 0/1/2
```
### Function: GetMultiDirs
_No documentation available_



# Documentation for CSProperties.py

## Classes and Methods
### Class: CSProperties
#### Method: AddAttribute
```
AddAttribute(name, val)

        Add an attribure and value

        :param name: str -- Attribute name
        :param val: str -- Attribute value
```
#### Method: AddBox
```
AddBox(start, stop, **kw)

        Add a box to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimBox : See here for details on primitive arguments
```
#### Method: AddCurve
```
AddCurve(points, **kw)

        Add a curve to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimCurve : See here for details on primitive arguments
```
#### Method: AddCylinder
```
AddCylinder(start, stop, radius, **kw)

        Add a cylinder to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimCylinder : See here for details on primitive arguments
```
#### Method: AddCylindricalShell
```
AddCylindricalShell(start, stop, radius, shell_width, **kw)

        Add a cylindrical shell to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimCylindricalShell : See here for details on primitive arguments
```
#### Method: AddLinPoly
```
AddLinPoly(points, norm_dir, elevation, length, **kw)

        Add a linear extruded polygon to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimLinPoly : See here for details on primitive arguments
```
#### Method: AddPoint
```
AddPoint(coord, **kw)

        Add a point to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimPoint : See here for details on primitive arguments
```
#### Method: AddPolygon
```
AddPolygon(points, norm_dir, elevation, **kw)

        Add a polygon to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimPolygon : See here for details on primitive arguments
```
#### Method: AddPolyhedron
```
AddPolyhedron(**kw)

        Add a polyhedron to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimPolyhedron : See here for details on primitive arguments
```
#### Method: AddPolyhedronReader
```
AddPolyhedronReader(filename, **kw)

        Add a polyhedron from file to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimPolyhedronReader : See here for details on primitive arguments
```
#### Method: AddRotPoly
```
AddRotPoly(points, norm_dir, elevation, rot_axis, angle, **kw)

        Add a rotated polygon to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimRotPoly : See here for details on primitive arguments
```
#### Method: AddSphere
```
AddSphere(center, radius, **kw)

        Add a sphere to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimSphere : See here for details on primitive arguments
```
#### Method: AddSphericalShell
```
AddSphericalShell(center, radius, shell_width, **kw)

        Add a spherical shell to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimSphericalShell : See here for details on primitive arguments
```
#### Method: AddWire
```
AddWire(points, radius, **kw)

        Add a wire to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimWire : See here for details on primitive arguments
```
#### Method: ExistAttribute
```
ExistAttribute(name)

        Check if an attribute with the given `name` exists

        :param name: str -- Attribute name
        :returns: bool
```
#### Method: fromType
```
fromType(p_type, pset, no_init=False, **kw)

        Create a property specified by the `p_type`

        :param p_type: Property type
        :param pset: ParameterSet to assign to the new primitive
        :param no_init: do not create an actual C++ instance
```
#### Method: fromTypeName
```
fromTypeName(type_str, pset, no_init=False, **kw)

        Create a property specified by the `type_str`

        :param type_str: Property type name string
        :param pset: ParameterSet to assign to the new primitive
        :param no_init: do not create an actual C++ instance
```
#### Method: GetAllPrimitives
_No documentation available_
#### Method: GetAttributeValue
```
GetAttributeValue(name)

        Get the value of the attribute with the given `name`

        :param name: str -- Attribute name
        :returns: str -- Attribute value
```
#### Method: GetName
```
Get the name of this property

        :returns: str -- Name for this property
```
#### Method: GetParameterSet
```
Get the parameter set assigned to this class 
```
#### Method: GetPrimitive
_No documentation available_
#### Method: GetQtyPrimitives
```
Get the number of primitives assigned to this property

        :returns: int -- Number of primitives
```
#### Method: GetType
```
Get the type of the property

        :returns: int -- Type ID of this property
```
#### Method: GetTypeString
```
Get the type of the property as a string

        :returns: str -- Type name of this property type
```
#### Method: SetColor
```
SetColor(color, alpha=255)

        Set the fill and edge color for this property.

        :param color: hex color value
        :param alpha: transparency value
```
#### Method: SetEdgeColor
```
SetColor(color, alpha=255)

        Set the edge color for this property.

        :param color: hex color value
        :param alpha: transparency value
```
#### Method: SetFillColor
```
SetFillColor(color, alpha=255)

        Set the fill color for this property.

        :param color: hex color value
        :param alpha: transparency value
```
#### Method: SetName
```
SetName(name)

        Set the name of this property

        :params name: str -- Name for this property
```
#### Method: _CSProperties__CreatePrimitive
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

### Class: CSPropMetal
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

### Class: CSPropConductingSheet
#### Method: GetConductivity
```
GetConductivity() 
```
#### Method: GetThickness
```
GetThickness() 
```
#### Method: SetConductivity
```
SetConductivity(val) 
```
#### Method: SetThickness
```
SetThickness(val) 
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

### Class: CSPropProbeBox
#### Method: AddFrequency
```
AddFrequency(freq) 
```
#### Method: ClearFrequency
```
ClearFrequency() 
```
#### Method: GetFrequency
```
GetFrequency 
```
#### Method: GetFrequencyCount
```
GetFrequencyCount() 
```
#### Method: GetNormalDir
```
GetNormalDir() 
```
#### Method: GetProbeType
```
GetProbeType() 
```
#### Method: GetWeighting
```
GetWeighting() 
```
#### Method: SetFrequency
```
SetFrequency(freq) 
```
#### Method: SetModeFunction
```
SetModeFunction(mode_fun) 
```
#### Method: SetNormalDir
```
SetNormalDir(val) 
```
#### Method: SetProbeType
```
SetProbeType(val) 
```
#### Method: SetWeighting
```
SetWeighting(val) 
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

### Class: CSPropDumpBox
#### Method: GetDumpMode
```
GetDumpMode() 
```
#### Method: GetDumpType
```
GetDumpType() 
```
#### Method: GetFileType
```
GetFileType() 
```
#### Method: GetOptResolution
```
GetOptResolution() 
```
#### Method: GetSubSampling
```
GetSubSampling() 
```
#### Method: SetDumpMode
```
SetDumpMode(val) 
```
#### Method: SetDumpType
```
SetDumpType(val) 
```
#### Method: SetFileType
```
SetFileType(val) 
```
#### Method: SetOptResolution
```
SetOptResolution(val) 
```
#### Method: SetSubSampling
```
SetSubSampling(val) 
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

### Class: CSPropExcitation
#### Method: GetDelay
```
GetDelay() 
```
#### Method: GetExcitation
```
GetExcitation()

        :returns: (3,) array -- excitation vector
```
#### Method: GetExcitType
```
GetExcitType()
        Get the excitation type.

        :return: int -- excitation type (see above)
```
#### Method: GetFrequency
```
GetFrequency() 
```
#### Method: GetPropagationDir
```
GetPropagationDir()

        Get the propagation direction, e.g. of a plane wave excitation

        :returns: (3,) array -- propagation vector
```
#### Method: GetWeightFunction
```
GetWeightFunction()

        Get the weigthing function for the excitation.

        :returns: 3 element list of strings
```
#### Method: SetDelay
```
SetDelay(val)

        Set signal delay for this property.

        :param val: float -- Signal delay
```
#### Method: SetExcitation
```
SetExcitation(val)

        openEMS excitation types:

        * 0 : E-field soft excitation
        * 1 : E-field hard excitation
        * 2 : H-field soft excitation
        * 3 : H-field hard excitation
        * 10 : plane wave excitation

        :param val: (3,) array -- excitation vector
```
#### Method: SetExcitType
```
SetExcitType(val)

        :param val: int -- excitation type (see above)
```
#### Method: SetFrequency
```
SetFrequency(val)

        Frequency for numerical phase velocity compensation (optional)

        :param val: float -- Frequency
```
#### Method: SetPropagationDir
```
SetPropagationDir(val)

        Set the propagation direction, e.g. for a plane wave excitation

        :param val: (3,) array -- propagation vector
```
#### Method: SetWeightFunction
```
SetWeightFunction(func)

        Set the weigthing function for the excitation.
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

### Class: CSPropLumpedElement
#### Method: GetCapacity
```
GetCapacity() 
```
#### Method: GetCaps
```
GetCaps() 
```
#### Method: GetDirection
```
GetDirection() 
```
#### Method: GetInductance
```
GetInductance() 
```
#### Method: GetLEtype
```
GetLEtype() 
```
#### Method: GetResistance
```
GetResistance() 
```
#### Method: SetCapacity
```
SetCapacity(val) 
```
#### Method: SetCaps
```
SetCaps(val) 
```
#### Method: SetDirection
```
SetDirection(ny) 
```
#### Method: SetInductance
```
SetInductance(val) 
```
#### Method: SetLEtype
```
SetLEtype(val) 
```
#### Method: SetResistance
```
SetResistance(val) 
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

### Class: CSPropMaterial
#### Method: GetIsotropy
```
Get isotropy status for this material.

        :returns: bool -- isotropy status
```
#### Method: GetMaterialProperty
```
SetMaterialProperty(prop_name)
        Get the material property with of type `prop_name`.

        :params prop_name: str -- material property type
        :returns: float for isotropic material and `density` or else (3,) array
```
#### Method: GetMaterialWeight
```
GetMaterialWeight(prop_name)
        Get the material weighting function(s).

        :params prop_name: str -- material property type
        :returns: str for isotropic material and `density` or else str array
```
#### Method: SetIsotropy
```
SetIsotropy(val)

        Set isotropy status for this material.

        :param val: bool -- enable/disable isotropy
```
#### Method: SetMaterialProperty
```
SetMaterialProperty(**kw)
        Set the material properties.

        :params epsilon: scalar or vector - relative electric permeability
        :params mue:     scalar or vector - relative magnetic permittivity
        :params kappa:   scalar or vector - relectric conductivity
        :params sigma:   scalar or vector - magnetic conductivity
        :params density: float            - Density
```
#### Method: SetMaterialWeight
```
SetMaterialWeight(**kw)

        Set the material weighting function(s)

        The functions can use the variables:
        `x`,`y`,`z`
        `rho` for the distance to z-axis
        `r`   for the distance to origin
        `a`   for alpha or phi (as in cylindircal and spherical coord systems)
        `t`   for theta (as in the spherical coord system

        all these variables are not weighted with the drawing unit defined by
        the grid

        :params epsilon: str or str-vector - relative electric permeability
        :params mue:     str or str-vector - relative magnetic permittivity
        :params kappa:   str or str-vector - relectric conductivity
        :params sigma:   str or str-vector - magnetic conductivity
        :params density: str               - Density
```
#### Method: _CSPropMaterial__GetMaterialPropertyDir
_No documentation available_
#### Method: _CSPropMaterial__GetMaterialWeightDir
_No documentation available_
#### Method: _CSPropMaterial__SetMaterialPropertyDir
_No documentation available_
#### Method: _CSPropMaterial__SetMaterialWeightDir
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

### Class: LEtype
#### Method: _generate_next_value_
```
Generate the next value when not given.

        name: the name of the member
        start: the initial start value or None
        count: the number of existing members
        last_value: the last value assigned or None
```
#### Method: __init__
_No documentation available_
#### Method: __new__
_No documentation available_

### Class: PropertyType
#### Method: _generate_next_value_
```
Generate the next value when not given.

        name: the name of the member
        start: the initial start value or None
        count: the number of existing members
        last_value: the last value assigned or None
```
#### Method: __init__
_No documentation available_
#### Method: __new__
_No documentation available_

## Functions
### Function: hex2color
_No documentation available_
### Function: AddAttribute
```
AddAttribute(name, val)

        Add an attribure and value

        :param name: str -- Attribute name
        :param val: str -- Attribute value
```
### Function: AddBox
```
AddBox(start, stop, **kw)

        Add a box to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimBox : See here for details on primitive arguments
```
### Function: AddCurve
```
AddCurve(points, **kw)

        Add a curve to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimCurve : See here for details on primitive arguments
```
### Function: AddCylinder
```
AddCylinder(start, stop, radius, **kw)

        Add a cylinder to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimCylinder : See here for details on primitive arguments
```
### Function: AddCylindricalShell
```
AddCylindricalShell(start, stop, radius, shell_width, **kw)

        Add a cylindrical shell to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimCylindricalShell : See here for details on primitive arguments
```
### Function: AddLinPoly
```
AddLinPoly(points, norm_dir, elevation, length, **kw)

        Add a linear extruded polygon to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimLinPoly : See here for details on primitive arguments
```
### Function: AddPoint
```
AddPoint(coord, **kw)

        Add a point to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimPoint : See here for details on primitive arguments
```
### Function: AddPolygon
```
AddPolygon(points, norm_dir, elevation, **kw)

        Add a polygon to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimPolygon : See here for details on primitive arguments
```
### Function: AddPolyhedron
```
AddPolyhedron(**kw)

        Add a polyhedron to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimPolyhedron : See here for details on primitive arguments
```
### Function: AddPolyhedronReader
```
AddPolyhedronReader(filename, **kw)

        Add a polyhedron from file to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimPolyhedronReader : See here for details on primitive arguments
```
### Function: AddRotPoly
```
AddRotPoly(points, norm_dir, elevation, rot_axis, angle, **kw)

        Add a rotated polygon to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimRotPoly : See here for details on primitive arguments
```
### Function: AddSphere
```
AddSphere(center, radius, **kw)

        Add a sphere to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimSphere : See here for details on primitive arguments
```
### Function: AddSphericalShell
```
AddSphericalShell(center, radius, shell_width, **kw)

        Add a spherical shell to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimSphericalShell : See here for details on primitive arguments
```
### Function: AddWire
```
AddWire(points, radius, **kw)

        Add a wire to this property.

        See Also
        --------
        CSXCAD.CSPrimitives.CSPrimWire : See here for details on primitive arguments
```
### Function: ExistAttribute
```
ExistAttribute(name)

        Check if an attribute with the given `name` exists

        :param name: str -- Attribute name
        :returns: bool
```
### Function: fromType
```
fromType(p_type, pset, no_init=False, **kw)

        Create a property specified by the `p_type`

        :param p_type: Property type
        :param pset: ParameterSet to assign to the new primitive
        :param no_init: do not create an actual C++ instance
```
### Function: fromTypeName
```
fromTypeName(type_str, pset, no_init=False, **kw)

        Create a property specified by the `type_str`

        :param type_str: Property type name string
        :param pset: ParameterSet to assign to the new primitive
        :param no_init: do not create an actual C++ instance
```
### Function: GetAllPrimitives
_No documentation available_
### Function: GetAttributeValue
```
GetAttributeValue(name)

        Get the value of the attribute with the given `name`

        :param name: str -- Attribute name
        :returns: str -- Attribute value
```
### Function: GetName
```
Get the name of this property

        :returns: str -- Name for this property
```
### Function: GetParameterSet
```
Get the parameter set assigned to this class 
```
### Function: GetPrimitive
_No documentation available_
### Function: GetQtyPrimitives
```
Get the number of primitives assigned to this property

        :returns: int -- Number of primitives
```
### Function: GetType
```
Get the type of the property

        :returns: int -- Type ID of this property
```
### Function: GetTypeString
```
Get the type of the property as a string

        :returns: str -- Type name of this property type
```
### Function: SetColor
```
SetColor(color, alpha=255)

        Set the fill and edge color for this property.

        :param color: hex color value
        :param alpha: transparency value
```
### Function: SetEdgeColor
```
SetColor(color, alpha=255)

        Set the edge color for this property.

        :param color: hex color value
        :param alpha: transparency value
```
### Function: SetFillColor
```
SetFillColor(color, alpha=255)

        Set the fill color for this property.

        :param color: hex color value
        :param alpha: transparency value
```
### Function: SetName
```
SetName(name)

        Set the name of this property

        :params name: str -- Name for this property
```
### Function: _CSProperties__CreatePrimitive
_No documentation available_
### Function: GetConductivity
```
GetConductivity() 
```
### Function: GetThickness
```
GetThickness() 
```
### Function: SetConductivity
```
SetConductivity(val) 
```
### Function: SetThickness
```
SetThickness(val) 
```
### Function: AddFrequency
```
AddFrequency(freq) 
```
### Function: ClearFrequency
```
ClearFrequency() 
```
### Function: GetFrequency
```
GetFrequency 
```
### Function: GetFrequencyCount
```
GetFrequencyCount() 
```
### Function: GetNormalDir
```
GetNormalDir() 
```
### Function: GetProbeType
```
GetProbeType() 
```
### Function: GetWeighting
```
GetWeighting() 
```
### Function: SetFrequency
```
SetFrequency(freq) 
```
### Function: SetModeFunction
```
SetModeFunction(mode_fun) 
```
### Function: SetNormalDir
```
SetNormalDir(val) 
```
### Function: SetProbeType
```
SetProbeType(val) 
```
### Function: SetWeighting
```
SetWeighting(val) 
```
### Function: GetDumpMode
```
GetDumpMode() 
```
### Function: GetDumpType
```
GetDumpType() 
```
### Function: GetFileType
```
GetFileType() 
```
### Function: GetOptResolution
```
GetOptResolution() 
```
### Function: GetSubSampling
```
GetSubSampling() 
```
### Function: SetDumpMode
```
SetDumpMode(val) 
```
### Function: SetDumpType
```
SetDumpType(val) 
```
### Function: SetFileType
```
SetFileType(val) 
```
### Function: SetOptResolution
```
SetOptResolution(val) 
```
### Function: SetSubSampling
```
SetSubSampling(val) 
```
### Function: GetDelay
```
GetDelay() 
```
### Function: GetExcitation
```
GetExcitation()

        :returns: (3,) array -- excitation vector
```
### Function: GetExcitType
```
GetExcitType()
        Get the excitation type.

        :return: int -- excitation type (see above)
```
### Function: GetFrequency
```
GetFrequency() 
```
### Function: GetPropagationDir
```
GetPropagationDir()

        Get the propagation direction, e.g. of a plane wave excitation

        :returns: (3,) array -- propagation vector
```
### Function: GetWeightFunction
```
GetWeightFunction()

        Get the weigthing function for the excitation.

        :returns: 3 element list of strings
```
### Function: SetDelay
```
SetDelay(val)

        Set signal delay for this property.

        :param val: float -- Signal delay
```
### Function: SetExcitation
```
SetExcitation(val)

        openEMS excitation types:

        * 0 : E-field soft excitation
        * 1 : E-field hard excitation
        * 2 : H-field soft excitation
        * 3 : H-field hard excitation
        * 10 : plane wave excitation

        :param val: (3,) array -- excitation vector
```
### Function: SetExcitType
```
SetExcitType(val)

        :param val: int -- excitation type (see above)
```
### Function: SetFrequency
```
SetFrequency(val)

        Frequency for numerical phase velocity compensation (optional)

        :param val: float -- Frequency
```
### Function: SetPropagationDir
```
SetPropagationDir(val)

        Set the propagation direction, e.g. for a plane wave excitation

        :param val: (3,) array -- propagation vector
```
### Function: SetWeightFunction
```
SetWeightFunction(func)

        Set the weigthing function for the excitation.
```
### Function: GetCapacity
```
GetCapacity() 
```
### Function: GetCaps
```
GetCaps() 
```
### Function: GetDirection
```
GetDirection() 
```
### Function: GetInductance
```
GetInductance() 
```
### Function: GetLEtype
```
GetLEtype() 
```
### Function: GetResistance
```
GetResistance() 
```
### Function: SetCapacity
```
SetCapacity(val) 
```
### Function: SetCaps
```
SetCaps(val) 
```
### Function: SetDirection
```
SetDirection(ny) 
```
### Function: SetInductance
```
SetInductance(val) 
```
### Function: SetLEtype
```
SetLEtype(val) 
```
### Function: SetResistance
```
SetResistance(val) 
```
### Function: GetIsotropy
```
Get isotropy status for this material.

        :returns: bool -- isotropy status
```
### Function: GetMaterialProperty
```
SetMaterialProperty(prop_name)
        Get the material property with of type `prop_name`.

        :params prop_name: str -- material property type
        :returns: float for isotropic material and `density` or else (3,) array
```
### Function: GetMaterialWeight
```
GetMaterialWeight(prop_name)
        Get the material weighting function(s).

        :params prop_name: str -- material property type
        :returns: str for isotropic material and `density` or else str array
```
### Function: SetIsotropy
```
SetIsotropy(val)

        Set isotropy status for this material.

        :param val: bool -- enable/disable isotropy
```
### Function: SetMaterialProperty
```
SetMaterialProperty(**kw)
        Set the material properties.

        :params epsilon: scalar or vector - relative electric permeability
        :params mue:     scalar or vector - relative magnetic permittivity
        :params kappa:   scalar or vector - relectric conductivity
        :params sigma:   scalar or vector - magnetic conductivity
        :params density: float            - Density
```
### Function: SetMaterialWeight
```
SetMaterialWeight(**kw)

        Set the material weighting function(s)

        The functions can use the variables:
        `x`,`y`,`z`
        `rho` for the distance to z-axis
        `r`   for the distance to origin
        `a`   for alpha or phi (as in cylindircal and spherical coord systems)
        `t`   for theta (as in the spherical coord system

        all these variables are not weighted with the drawing unit defined by
        the grid

        :params epsilon: str or str-vector - relative electric permeability
        :params mue:     str or str-vector - relative magnetic permittivity
        :params kappa:   str or str-vector - relectric conductivity
        :params sigma:   str or str-vector - magnetic conductivity
        :params density: str               - Density
```
### Function: _CSPropMaterial__GetMaterialPropertyDir
_No documentation available_
### Function: _CSPropMaterial__GetMaterialWeightDir
_No documentation available_
### Function: _CSPropMaterial__SetMaterialPropertyDir
_No documentation available_
### Function: _CSPropMaterial__SetMaterialWeightDir
_No documentation available_
### Function: _generate_next_value_
```
Generate the next value when not given.

        name: the name of the member
        start: the initial start value or None
        count: the number of existing members
        last_value: the last value assigned or None
```
### Function: _generate_next_value_
```
Generate the next value when not given.

        name: the name of the member
        start: the initial start value or None
        count: the number of existing members
        last_value: the last value assigned or None
```



# Documentation for CSPrimitives.py

## Classes and Methods
### Class: CSPrimitives
#### Method: AddTransform
```
AddTransform(transform, *args, **kw)

        Add a transformation to this primitive.

        See Also
        --------
        CSXCAD.CSTransform.CSTransform.AddTransform
```
#### Method: fromType
```
fromType(prim_type, pset, prop, no_init=False, **kw)

        Create a primtive specified by the `prim_type`

        :param prim_type: Primitive type
        :param pset: ParameterSet to assign to the new primitive
        :param prop: CSProperty to assign to the new primitive
        :param no_init: do not create an actual C++ instance
```
#### Method: GetBoundBox
```
Get the bounding box for this primitive

        :returns: (2,3) ndarray -- bounding box for this primitive
```
#### Method: GetCoordinateSystem
```
GetCoordinateSystem

        :returns: coordinate system (0 : Cartesian, 1 : Cylindrical) or None
```
#### Method: GetDimension
```
Get the dimension of this primitive

        :returns: int -- dimension 0..3
```
#### Method: GetID
```
Get the ID for this primitive

        :returns: int -- ID for this primitive
```
#### Method: GetPrimitiveUsed
```
Get if this primitive has been used (used flag set) 
```
#### Method: GetPriority
```
Get the priority for this primitive

        :returns: int -- Priority for this primitive
```
#### Method: GetProperty
```
Get the property for this primitive

        :returns: CSProperties.CSProperties
```
#### Method: GetTransform
```
GetTransform()

        Get the transformation class assigned to this primitive.
        If this primitve does not have any, it will be created.

        :return: CSTransform class

        See Also
        --------
        CSXCAD.CSTransform.CSTransform
```
#### Method: GetType
```
Get the type as int for this primitive

        :returns: int -- Type for this primitive (e.g. 0 --> Point, 1 --> Box, ...)
```
#### Method: GetTypeName
```
Get the type as string (UTF-8) for this primitive

        :returns: str -- Type name for this primitive ("Point", "Box", ...)
```
#### Method: HasTransform
```
Check if this primitive has a transformation attached.
        It will not create one if it does not.

        :returns: bool
```
#### Method: IsInside
```
IsInside(coord, tol=0)

        Check if a given coordinate is inside this primitive.

        :param coord: (3,) array -- coordinate
        :returns: bool
```
#### Method: SetCoordinateSystem
```
SetCoordinateSystem(cs_type)

        Set the coordinate system type (Cartesian or cylindrical) for this primitive.
        If set to None, the mesh type of the assigned rect grid will be used.

        :param cs_type: coordinate system (0 : Cartesian, 1 : Cylindrical) or None

        See Also
        --------
        CSXCAD.CSRectGrid.CSRectGrid.SetMeshType
```
#### Method: SetPrimitiveUsed
```
SetPrimitiveUsed(val)

        Set used flag.
```
#### Method: SetPriority
```
SetPriority(val)

        Set the priority for this primitive

        :param val: int -- Higher priority values will override primitives with a lower priority
```
#### Method: Update
```
Trigger an internal update and report success and error message

        :returns: bool, err_msg -- success and error message (empty on success)
```
#### Method: _CSPrimitives__GetCSX
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

### Class: CSPrimBox
#### Method: GetStart
```
Get the start coordinate for this primitive.

        :returns: (3,) ndarray -- Start coordinate for this primitive
```
#### Method: GetStop
```
Get the stop coordinate for this primitive.

        :returns: (3,) ndarray -- Stop coordinate for this primitive
```
#### Method: SetStart
```
SetStart(coord)

        Set the start coordinate for this box primitive.

        :param coord: list/array of float -- Set the start point coordinate
```
#### Method: SetStop
```
SetStop(coord)

        Set the stop coordinate for this box primitive.

        :param coord: list/array of float -- Set the stop point coordinate
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

### Class: CSPrimCurve
#### Method: AddPoint
```
AddPoint(point)

        Add a single point to the list.

        :param point: (3,) array -- Add a single 3D point
```
#### Method: ClearPoints
```
Clear all points. 
```
#### Method: GetNumberOfPoints
```
Get the number of points.

        :return num: int -- Get the number of points.
```
#### Method: GetPoint
```
GetPoint(idx)

        Get a point with a given index.

        :param idx: int -- Index of point requested.
        :return point: (3,) array -- Point coordinate at index `idx`
```
#### Method: SetPoints
```
SetPoints(x, y, z)

        Set an array of 3D coordinates

        :param x,y,z: each (N,) array -- Array of 3D point components
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

### Class: CSPrimCylinder
#### Method: GetRadius
```
Get the cylinder radius.

        :returns: float -- Cylinder radius.
```
#### Method: GetStart
```
Get the axis start coordinate.

        :returns: (3,) ndarray -- Axis start coordinate.
```
#### Method: GetStop
```
Get the axis stop coordinate.

        :returns: (3,) ndarray -- Axis stop coordinate.
```
#### Method: SetRadius
```
SetRadius(val)

        Set the cylinder radius

        :param val: float -- Set the cylinder radius
```
#### Method: SetStart
```
SetStart(coord)

        Set the start coordinate for the cylinder axis.

        :param coord: list/array of float -- Set the axis start point coordinate.
```
#### Method: SetStop
```
SetStop(coord)

        Set the stop coordinate for the cylinder axis.

        :param coord: list/array of float -- Set the axis stop point coordinate.
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

### Class: CSPrimCylindricalShell
#### Method: GetShellWidth
```
Get the cylinder shell width.

        :returns: float -- Cylinder shell width.
```
#### Method: SetShellWidth
```
SetShellWidth(val)

        Set the cylinder shell width.

        :param val: float -- Set the cylinder shell width
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

### Class: CSPrimPolygon
#### Method: ClearCoords
```
Remove all coordinates. 
```
#### Method: GetCoords
```
Get the coordinates for the polygon

        :return x0, x1: (N,), (N,) Arrays for x0,x1 of the polygon coordinates
```
#### Method: GetElevation
```
Get the elevation in normal direction.

        :return val: float -- Get the elevation in normal direction.
```
#### Method: GetNormDir
```
Get the normal direction.

        :return ny: int -- Normal direction as 0, 1 or 2 meaning x,y or z
```
#### Method: GetQtyCoords
```
Get the number of coordinates for the polygon

        :return val: int -- Number of polygon coordinates.
```
#### Method: SetCoords
```
SetCoords(x0, x1)

        Set the coordinates for the polygon. This will clear all previous coordinates.

        :param x0, x1: (N,), (N,) Two arrays for x0/x1 of the polygon coordinates.
```
#### Method: SetElevation
```
SetElevation(val)

        Set the elevation in normal direction.

        :param val: float -- Elevation in normal direction.
```
#### Method: SetNormDir
```
SetNormDir(ny)

        Set the normal direction.

        :param ny: int or string -- Normal direction, either 0/1/2 or 'x'/'y'/'z'
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

### Class: CSPrimLinPoly
#### Method: GetLength
```
Get the extrusion length in normal direction.

        :return val: float -- Get the extrusion length in normal direction.
```
#### Method: SetLength
```
SetLength(val)

        Set the extrusion length in normal direction.

        :param val: float -- Extrusion length in normal direction.
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

### Class: CSPrimPoint
#### Method: GetCoord
```
Get the point coordinate for this primitive

        :returns: (3,) ndarray -- point coordinate for this primitive
```
#### Method: SetCoord
```
SetCoord(coord)

        Set the coordinate for this point primitive

        :param coord: list/array of float -- Set the point coordinate
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

### Class: CSPrimPolyhedron
#### Method: AddFace
```
AddFace(verts)

        Add a face with a given list of vertices.
        The vertices have to be added already.
        Currently only triangle faces are possible.

        :params verts: (N,) array -- Face with N vericies (currently N=3!)
```
#### Method: AddVertex
```
AddVertex(x, y, z)

        Add a single 3D vertex.

        :param x,y,z: float,float,float -- 3D vertex
```
#### Method: GetFace
```
GetFace(idx)

        Get the face vertex indicies for the given face index `idx`

        :param idx: int -- Face index to return
        :returns: (N,) array -- Vertices array for face with index `idx`
```
#### Method: GetNumFaces
```
Get the number of faces.

        :return num: int -- number of faces
```
#### Method: GetNumVertices
```
Get the number of vertices.

        :returns num: int -- Number of vertices
```
#### Method: GetVertex
```
GetVertex(idx)

        Get the vertex with index `idx`.

        :param idx: int -- Vertex index to return
        :returns point: (3,) array -- Vertex coordinate at index `idx`
```
#### Method: Reset
```
Reset the polyhedron, that means removeing all faces. 
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

### Class: CSPrimPolyhedronReader
#### Method: GetFilename
```
Get the file name.

        :returns fn: str -- File name to read
```
#### Method: GetFileType
```
Get the file type. 1 --> STL-File, 2 --> PLY, 0 --> other/unknown

        :return t: int -- File type (see above)
```
#### Method: ReadFile
```
Issue to read the file.

        :return succ: bool -- True on successful read
```
#### Method: SetFilename
```
SetFilename(fn)

        Set the file name to read. This will try set the propper file type as well.

        :param fn: str -- File name to read
```
#### Method: SetFileType
```
SetFileType(t)

        Set the file type. 1 --> STL-File, 2 --> PLY, 0 --> other/unknown

        :param t: int -- File type (see above)
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

### Class: CSPrimRotPoly
#### Method: GetAngle
```
Get the start/stop angle (rad) of rotation.

        :returns a0, a1: float, float -- Start/Stop angle (rad) of rotation.
```
#### Method: GetRotAxisDir
```
Get the rotation axis direction

        :returns ny: int -- Rotation axis direction as 0, 1 or 2 meaning x,y or z
```
#### Method: SetAngle
```
SetAngle(a0, a1)

        Set the start/stop angle (rad) of rotation. Default is (0, 2*pi).

        :param a0: float -- Start angle (rad) of rotation.
        :param a1: float -- Stop angle (rad) of rotation.
```
#### Method: SetRotAxisDir
```
SetRotAxisDir(ny)

        Set the rotation axis direction, either 0,1,2 or x/y/z respectively.

        :param ny: int or str -- Rotation axis direction, either 0,1,2 or x/y/z respectively.
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

### Class: CSPrimSphere
#### Method: GetCenter
```
Get the sphere center point.

        :returns: (3,) ndarray -- Center coordinate.
```
#### Method: GetRadius
```
Get the sphere radius.

        :returns: float -- Sphere radius.
```
#### Method: SetCenter
```
SetRadius(val)

        Set the sphere center point.

        :param coord: (3,) array -- Set the sphere center point.
```
#### Method: SetRadius
```
SetRadius(val)

        Set the sphere radius

        :param val: float -- Set the sphere radius
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

### Class: CSPrimSphericalShell
#### Method: GetShellWidth
```
Get the sphere shell width.

        :returns: float -- sphere shell width.
```
#### Method: SetShellWidth
```
SetShellWidth(val)

        Set the sphere shell width.

        :param val: float -- Set the sphere shell width
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

### Class: CSPrimWire
#### Method: GetWireRadius
```
Get the wire radius.

        :returns: float -- Wire radius.
```
#### Method: SetWireRadius
```
SetWireRadius(val)

        Set the wire radius

        :param val: float -- Set the wire radius
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

### Class: PrimitiveType
#### Method: _generate_next_value_
```
Generate the next value when not given.

        name: the name of the member
        start: the initial start value or None
        count: the number of existing members
        last_value: the last value assigned or None
```
#### Method: __init__
_No documentation available_
#### Method: __new__
_No documentation available_

## Functions
### Function: AddTransform
```
AddTransform(transform, *args, **kw)

        Add a transformation to this primitive.

        See Also
        --------
        CSXCAD.CSTransform.CSTransform.AddTransform
```
### Function: fromType
```
fromType(prim_type, pset, prop, no_init=False, **kw)

        Create a primtive specified by the `prim_type`

        :param prim_type: Primitive type
        :param pset: ParameterSet to assign to the new primitive
        :param prop: CSProperty to assign to the new primitive
        :param no_init: do not create an actual C++ instance
```
### Function: GetBoundBox
```
Get the bounding box for this primitive

        :returns: (2,3) ndarray -- bounding box for this primitive
```
### Function: GetCoordinateSystem
```
GetCoordinateSystem

        :returns: coordinate system (0 : Cartesian, 1 : Cylindrical) or None
```
### Function: GetDimension
```
Get the dimension of this primitive

        :returns: int -- dimension 0..3
```
### Function: GetID
```
Get the ID for this primitive

        :returns: int -- ID for this primitive
```
### Function: GetPrimitiveUsed
```
Get if this primitive has been used (used flag set) 
```
### Function: GetPriority
```
Get the priority for this primitive

        :returns: int -- Priority for this primitive
```
### Function: GetProperty
```
Get the property for this primitive

        :returns: CSProperties.CSProperties
```
### Function: GetTransform
```
GetTransform()

        Get the transformation class assigned to this primitive.
        If this primitve does not have any, it will be created.

        :return: CSTransform class

        See Also
        --------
        CSXCAD.CSTransform.CSTransform
```
### Function: GetType
```
Get the type as int for this primitive

        :returns: int -- Type for this primitive (e.g. 0 --> Point, 1 --> Box, ...)
```
### Function: GetTypeName
```
Get the type as string (UTF-8) for this primitive

        :returns: str -- Type name for this primitive ("Point", "Box", ...)
```
### Function: HasTransform
```
Check if this primitive has a transformation attached.
        It will not create one if it does not.

        :returns: bool
```
### Function: IsInside
```
IsInside(coord, tol=0)

        Check if a given coordinate is inside this primitive.

        :param coord: (3,) array -- coordinate
        :returns: bool
```
### Function: SetCoordinateSystem
```
SetCoordinateSystem(cs_type)

        Set the coordinate system type (Cartesian or cylindrical) for this primitive.
        If set to None, the mesh type of the assigned rect grid will be used.

        :param cs_type: coordinate system (0 : Cartesian, 1 : Cylindrical) or None

        See Also
        --------
        CSXCAD.CSRectGrid.CSRectGrid.SetMeshType
```
### Function: SetPrimitiveUsed
```
SetPrimitiveUsed(val)

        Set used flag.
```
### Function: SetPriority
```
SetPriority(val)

        Set the priority for this primitive

        :param val: int -- Higher priority values will override primitives with a lower priority
```
### Function: Update
```
Trigger an internal update and report success and error message

        :returns: bool, err_msg -- success and error message (empty on success)
```
### Function: _CSPrimitives__GetCSX
_No documentation available_
### Function: GetStart
```
Get the start coordinate for this primitive.

        :returns: (3,) ndarray -- Start coordinate for this primitive
```
### Function: GetStop
```
Get the stop coordinate for this primitive.

        :returns: (3,) ndarray -- Stop coordinate for this primitive
```
### Function: SetStart
```
SetStart(coord)

        Set the start coordinate for this box primitive.

        :param coord: list/array of float -- Set the start point coordinate
```
### Function: SetStop
```
SetStop(coord)

        Set the stop coordinate for this box primitive.

        :param coord: list/array of float -- Set the stop point coordinate
```
### Function: AddPoint
```
AddPoint(point)

        Add a single point to the list.

        :param point: (3,) array -- Add a single 3D point
```
### Function: ClearPoints
```
Clear all points. 
```
### Function: GetNumberOfPoints
```
Get the number of points.

        :return num: int -- Get the number of points.
```
### Function: GetPoint
```
GetPoint(idx)

        Get a point with a given index.

        :param idx: int -- Index of point requested.
        :return point: (3,) array -- Point coordinate at index `idx`
```
### Function: SetPoints
```
SetPoints(x, y, z)

        Set an array of 3D coordinates

        :param x,y,z: each (N,) array -- Array of 3D point components
```
### Function: GetRadius
```
Get the cylinder radius.

        :returns: float -- Cylinder radius.
```
### Function: GetStart
```
Get the axis start coordinate.

        :returns: (3,) ndarray -- Axis start coordinate.
```
### Function: GetStop
```
Get the axis stop coordinate.

        :returns: (3,) ndarray -- Axis stop coordinate.
```
### Function: SetRadius
```
SetRadius(val)

        Set the cylinder radius

        :param val: float -- Set the cylinder radius
```
### Function: SetStart
```
SetStart(coord)

        Set the start coordinate for the cylinder axis.

        :param coord: list/array of float -- Set the axis start point coordinate.
```
### Function: SetStop
```
SetStop(coord)

        Set the stop coordinate for the cylinder axis.

        :param coord: list/array of float -- Set the axis stop point coordinate.
```
### Function: GetShellWidth
```
Get the cylinder shell width.

        :returns: float -- Cylinder shell width.
```
### Function: SetShellWidth
```
SetShellWidth(val)

        Set the cylinder shell width.

        :param val: float -- Set the cylinder shell width
```
### Function: ClearCoords
```
Remove all coordinates. 
```
### Function: GetCoords
```
Get the coordinates for the polygon

        :return x0, x1: (N,), (N,) Arrays for x0,x1 of the polygon coordinates
```
### Function: GetElevation
```
Get the elevation in normal direction.

        :return val: float -- Get the elevation in normal direction.
```
### Function: GetNormDir
```
Get the normal direction.

        :return ny: int -- Normal direction as 0, 1 or 2 meaning x,y or z
```
### Function: GetQtyCoords
```
Get the number of coordinates for the polygon

        :return val: int -- Number of polygon coordinates.
```
### Function: SetCoords
```
SetCoords(x0, x1)

        Set the coordinates for the polygon. This will clear all previous coordinates.

        :param x0, x1: (N,), (N,) Two arrays for x0/x1 of the polygon coordinates.
```
### Function: SetElevation
```
SetElevation(val)

        Set the elevation in normal direction.

        :param val: float -- Elevation in normal direction.
```
### Function: SetNormDir
```
SetNormDir(ny)

        Set the normal direction.

        :param ny: int or string -- Normal direction, either 0/1/2 or 'x'/'y'/'z'
```
### Function: GetLength
```
Get the extrusion length in normal direction.

        :return val: float -- Get the extrusion length in normal direction.
```
### Function: SetLength
```
SetLength(val)

        Set the extrusion length in normal direction.

        :param val: float -- Extrusion length in normal direction.
```
### Function: GetCoord
```
Get the point coordinate for this primitive

        :returns: (3,) ndarray -- point coordinate for this primitive
```
### Function: SetCoord
```
SetCoord(coord)

        Set the coordinate for this point primitive

        :param coord: list/array of float -- Set the point coordinate
```
### Function: AddFace
```
AddFace(verts)

        Add a face with a given list of vertices.
        The vertices have to be added already.
        Currently only triangle faces are possible.

        :params verts: (N,) array -- Face with N vericies (currently N=3!)
```
### Function: AddVertex
```
AddVertex(x, y, z)

        Add a single 3D vertex.

        :param x,y,z: float,float,float -- 3D vertex
```
### Function: GetFace
```
GetFace(idx)

        Get the face vertex indicies for the given face index `idx`

        :param idx: int -- Face index to return
        :returns: (N,) array -- Vertices array for face with index `idx`
```
### Function: GetNumFaces
```
Get the number of faces.

        :return num: int -- number of faces
```
### Function: GetNumVertices
```
Get the number of vertices.

        :returns num: int -- Number of vertices
```
### Function: GetVertex
```
GetVertex(idx)

        Get the vertex with index `idx`.

        :param idx: int -- Vertex index to return
        :returns point: (3,) array -- Vertex coordinate at index `idx`
```
### Function: Reset
```
Reset the polyhedron, that means removeing all faces. 
```
### Function: GetFilename
```
Get the file name.

        :returns fn: str -- File name to read
```
### Function: GetFileType
```
Get the file type. 1 --> STL-File, 2 --> PLY, 0 --> other/unknown

        :return t: int -- File type (see above)
```
### Function: ReadFile
```
Issue to read the file.

        :return succ: bool -- True on successful read
```
### Function: SetFilename
```
SetFilename(fn)

        Set the file name to read. This will try set the propper file type as well.

        :param fn: str -- File name to read
```
### Function: SetFileType
```
SetFileType(t)

        Set the file type. 1 --> STL-File, 2 --> PLY, 0 --> other/unknown

        :param t: int -- File type (see above)
```
### Function: GetAngle
```
Get the start/stop angle (rad) of rotation.

        :returns a0, a1: float, float -- Start/Stop angle (rad) of rotation.
```
### Function: GetRotAxisDir
```
Get the rotation axis direction

        :returns ny: int -- Rotation axis direction as 0, 1 or 2 meaning x,y or z
```
### Function: SetAngle
```
SetAngle(a0, a1)

        Set the start/stop angle (rad) of rotation. Default is (0, 2*pi).

        :param a0: float -- Start angle (rad) of rotation.
        :param a1: float -- Stop angle (rad) of rotation.
```
### Function: SetRotAxisDir
```
SetRotAxisDir(ny)

        Set the rotation axis direction, either 0,1,2 or x/y/z respectively.

        :param ny: int or str -- Rotation axis direction, either 0,1,2 or x/y/z respectively.
```
### Function: GetCenter
```
Get the sphere center point.

        :returns: (3,) ndarray -- Center coordinate.
```
### Function: GetRadius
```
Get the sphere radius.

        :returns: float -- Sphere radius.
```
### Function: SetCenter
```
SetRadius(val)

        Set the sphere center point.

        :param coord: (3,) array -- Set the sphere center point.
```
### Function: SetRadius
```
SetRadius(val)

        Set the sphere radius

        :param val: float -- Set the sphere radius
```
### Function: GetShellWidth
```
Get the sphere shell width.

        :returns: float -- sphere shell width.
```
### Function: SetShellWidth
```
SetShellWidth(val)

        Set the sphere shell width.

        :param val: float -- Set the sphere shell width
```
### Function: GetWireRadius
```
Get the wire radius.

        :returns: float -- Wire radius.
```
### Function: SetWireRadius
```
SetWireRadius(val)

        Set the wire radius

        :param val: float -- Set the wire radius
```
### Function: _generate_next_value_
```
Generate the next value when not given.

        name: the name of the member
        start: the initial start value or None
        count: the number of existing members
        last_value: the last value assigned or None
```



# Documentation for __init__.py



# Documentation for CSTransform.py

## Classes and Methods
### Class: CSTransform
#### Method: AddTransform
```
AddTransform(transform, *args, **kw)

        Add a transform by name and arguments.

        Examples
        --------
        Add a translation and 30° rotation around the z-axis:

        >>> tr = CSTransform()
        >>> tr.AddTransform('Translate', [10, 4,6])
        >>> tr.AddTransform('RotateAxis', 'z', 30)

        Add a rotation around the axis=[1, 1, 0] by pi/3 (30°):

        >>> tr = CSTransform()
        >>> tr.AddTransform('RotateOrigin', [1, 1, 0], np.pi/3, deg=False)

        Available Transformation keywords:

        * RotateAxis : Rotate around x,y or z-axis
        * RotateOrigin : Rotate around a given axis
        * Translate : Translation vector
        * Scale : Scale value or vector
        * Matrix : A affine transformation matrix as (4,4) array

        :param transform: str -- transformation name or keyword.
```
#### Method: GetMatrix
```
Get the full 4x4 transformation matrix used for transformation.

        :returns: (4,4) array -- transformation matrix
```
#### Method: HasTransform
```
Check if any transformations are set. 
```
#### Method: Reset
```
Reset all transformations. 
```
#### Method: RotateAxis
```
RotateAxis(ny, angle, deg=True, concatenate=True)

        Add a rotation transformation around a cartesian axis (x,y or z).

        :param ny: int or str -- translation axis vector 0/1/2 or 'x'/'y'/'z.
        :param angle: float -- rotation angle (default in degrees)
        :param deg: bool -- set degree or radiant for angle (default True)
```
#### Method: RotateOrigin
```
RotateOrigin(vec, angle, deg=True, concatenate=True)

        Add a rotation transformation around an arbitrary axis.

        :param vec: (3,) array -- translation axis vector.
        :param angle: float -- rotation angle (default in degrees)
        :param deg: bool -- set degree or radiant for angle (default True)
```
#### Method: Scale
```
Scale(scale, concatenate=True)

        Add a scaleing transformation.

        :param scale: float or (3,) array -- Scaling factor
```
#### Method: SetMatrix
```
SetMatrix(mat, concatenate=True)

        Add an arbitrary (invertable) trsanslation matrix.

        :param mat: (3,) array -- translation vector
```
#### Method: SetPostMultiply
```
Set all following transformations as post multiply (default) 
```
#### Method: SetPreMultiply
```
Set all following transformations as pre multiply (default is post multiply) 
```
#### Method: Transform
```
Transform(coord, invers)

        Apply a transformation to the given coordinate.

        :param coord: (3,) array -- coordinate to transform
        :param invers: bool -- do an invers transformation
        :returns: (3,) array -- transformed coordinates
```
#### Method: Translate
```
Translate(vec, concatenate=True)

        Add a trsanslation transformation.

        :param vec: (3,) array -- translation vector
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
### Function: AddTransform
```
AddTransform(transform, *args, **kw)

        Add a transform by name and arguments.

        Examples
        --------
        Add a translation and 30° rotation around the z-axis:

        >>> tr = CSTransform()
        >>> tr.AddTransform('Translate', [10, 4,6])
        >>> tr.AddTransform('RotateAxis', 'z', 30)

        Add a rotation around the axis=[1, 1, 0] by pi/3 (30°):

        >>> tr = CSTransform()
        >>> tr.AddTransform('RotateOrigin', [1, 1, 0], np.pi/3, deg=False)

        Available Transformation keywords:

        * RotateAxis : Rotate around x,y or z-axis
        * RotateOrigin : Rotate around a given axis
        * Translate : Translation vector
        * Scale : Scale value or vector
        * Matrix : A affine transformation matrix as (4,4) array

        :param transform: str -- transformation name or keyword.
```
### Function: GetMatrix
```
Get the full 4x4 transformation matrix used for transformation.

        :returns: (4,4) array -- transformation matrix
```
### Function: HasTransform
```
Check if any transformations are set. 
```
### Function: Reset
```
Reset all transformations. 
```
### Function: RotateAxis
```
RotateAxis(ny, angle, deg=True, concatenate=True)

        Add a rotation transformation around a cartesian axis (x,y or z).

        :param ny: int or str -- translation axis vector 0/1/2 or 'x'/'y'/'z.
        :param angle: float -- rotation angle (default in degrees)
        :param deg: bool -- set degree or radiant for angle (default True)
```
### Function: RotateOrigin
```
RotateOrigin(vec, angle, deg=True, concatenate=True)

        Add a rotation transformation around an arbitrary axis.

        :param vec: (3,) array -- translation axis vector.
        :param angle: float -- rotation angle (default in degrees)
        :param deg: bool -- set degree or radiant for angle (default True)
```
### Function: Scale
```
Scale(scale, concatenate=True)

        Add a scaleing transformation.

        :param scale: float or (3,) array -- Scaling factor
```
### Function: SetMatrix
```
SetMatrix(mat, concatenate=True)

        Add an arbitrary (invertable) trsanslation matrix.

        :param mat: (3,) array -- translation vector
```
### Function: SetPostMultiply
```
Set all following transformations as post multiply (default) 
```
### Function: SetPreMultiply
```
Set all following transformations as pre multiply (default is post multiply) 
```
### Function: Transform
```
Transform(coord, invers)

        Apply a transformation to the given coordinate.

        :param coord: (3,) array -- coordinate to transform
        :param invers: bool -- do an invers transformation
        :returns: (3,) array -- transformed coordinates
```
### Function: Translate
```
Translate(vec, concatenate=True)

        Add a trsanslation transformation.

        :param vec: (3,) array -- translation vector
```



# Documentation for CSXCAD.py

## Classes and Methods
### Class: ContinuousStructure
#### Method: AddConductingSheet
```
AddConductingSheet(name, **kw)

        Add a conducting sheet with name `name`.

        See Also
        --------
        CSXCAD.CSProperties.CSPropConductingSheet
```
#### Method: AddDump
```
AddDump(name, **kw)

        Add a dump property with name `name`.

        See Also
        --------
        CSXCAD.CSProperties.CSPropDumpBox
```
#### Method: AddExcitation
```
AddExcitation(name, exc_type, exc_val, **kw)

        Add an excitation property with name `name`.

        See Also
        --------
        CSXCAD.CSProperties.CSPropExcitation
```
#### Method: AddLumpedElement
```
AddLumpedElement(name, **kw)

        Add a lumped element with name `name`.

        See Also
        --------
        CSXCAD.CSProperties.CSPropLumpedElement
```
#### Method: AddMaterial
```
AddMaterial(name, **kw)

        Add a material property with name `name`.

        See Also
        --------
        CSXCAD.CSProperties.CSPropMaterial
```
#### Method: AddMetal
```
AddMetal(name)

        Add a metal property with name `name`.

        See Also
        --------
        CSXCAD.CSProperties.CSPropMetal
```
#### Method: AddProbe
```
AddProbe(name, p_type, **kw)

        Add a probe property with name `name`.

        See Also
        --------
        CSXCAD.CSProperties.CSPropProbeBox
```
#### Method: AddProperty
```
AddProperty(prop)

        Add an already created property (`prop`) to this class.

        Notes
        -----
        This class will take ownership of the property.
```
#### Method: DefineGrid
```
DefineGrid(mesh, unit, smooth_mesh_res=None)

        Assign a mesh lines to the grid assigned to this property.

        :param mesh: (3,) list of mesh lines
        :param unit: float -- drawing unit
        :param smooth_mesh_res: an optional mesh smoothing

        See Also
        --------
        CSXCAD.CSRectGrid, GetGrid, CSXCAD.SmoothMeshLines.SmoothMeshLines
```
#### Method: GetAllPrimitives
```
GetAllPrimitives(sort, prop_type)

        Get a list of all primitives.
```
#### Method: GetAllProperties
```
GetAllProperties()

        Get a list of all properties
```
#### Method: GetGrid
```
Get the CSRectGrid assigned to this class.

        See Also
        --------
        CSXCAD.CSRectGrid, DefineGrid
```
#### Method: GetParameterSet
```
Get the parameter set assigned to this class 
```
#### Method: GetPropertiesByName
```
GetPropertiesByName(name)

        Get all the property specifed by their name
```
#### Method: GetProperty
```
GetProperty(index)

        Get the property at the given index

        See Also
        --------
        CSXCAD.GetQtyProperties
```
#### Method: GetPropertyByCoordPriority
```
GetPropertyByCoordPriority(coord, prop_type=None, markFoundAsUsed=False) 
```
#### Method: GetPropertyByType
```
GetPropertyByType(prop_type)

        Get a list of properties specified by their type
```
#### Method: GetQtyPrimitives
_No documentation available_
#### Method: GetQtyProperties
_No documentation available_
#### Method: ReadFromXML
```
ReadFromXML(fn)

        Read geometry from xml-file

        :param fn: str -- file name
```
#### Method: SetMeshType
_No documentation available_
#### Method: Update
_No documentation available_
#### Method: Write2XML
```
Write2XML(fn)

        Write geometry to an xml-file

        :param fn: str -- file name
```
#### Method: _ContinuousStructure__CreateProperty
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
### Function: SmoothMeshLines
```
This is the form of a docstring.

    Parameters
    ----------

    lines : list
        List of mesh lines to be smoothed
    max_res : float
        Maximum allowed resolution, resulting mesh will always stay below that value
    ratio : float
        Ratio of increase or decrease of neighboring mesh lines
```
### Function: AddConductingSheet
```
AddConductingSheet(name, **kw)

        Add a conducting sheet with name `name`.

        See Also
        --------
        CSXCAD.CSProperties.CSPropConductingSheet
```
### Function: AddDump
```
AddDump(name, **kw)

        Add a dump property with name `name`.

        See Also
        --------
        CSXCAD.CSProperties.CSPropDumpBox
```
### Function: AddExcitation
```
AddExcitation(name, exc_type, exc_val, **kw)

        Add an excitation property with name `name`.

        See Also
        --------
        CSXCAD.CSProperties.CSPropExcitation
```
### Function: AddLumpedElement
```
AddLumpedElement(name, **kw)

        Add a lumped element with name `name`.

        See Also
        --------
        CSXCAD.CSProperties.CSPropLumpedElement
```
### Function: AddMaterial
```
AddMaterial(name, **kw)

        Add a material property with name `name`.

        See Also
        --------
        CSXCAD.CSProperties.CSPropMaterial
```
### Function: AddMetal
```
AddMetal(name)

        Add a metal property with name `name`.

        See Also
        --------
        CSXCAD.CSProperties.CSPropMetal
```
### Function: AddProbe
```
AddProbe(name, p_type, **kw)

        Add a probe property with name `name`.

        See Also
        --------
        CSXCAD.CSProperties.CSPropProbeBox
```
### Function: AddProperty
```
AddProperty(prop)

        Add an already created property (`prop`) to this class.

        Notes
        -----
        This class will take ownership of the property.
```
### Function: DefineGrid
```
DefineGrid(mesh, unit, smooth_mesh_res=None)

        Assign a mesh lines to the grid assigned to this property.

        :param mesh: (3,) list of mesh lines
        :param unit: float -- drawing unit
        :param smooth_mesh_res: an optional mesh smoothing

        See Also
        --------
        CSXCAD.CSRectGrid, GetGrid, CSXCAD.SmoothMeshLines.SmoothMeshLines
```
### Function: GetAllPrimitives
```
GetAllPrimitives(sort, prop_type)

        Get a list of all primitives.
```
### Function: GetAllProperties
```
GetAllProperties()

        Get a list of all properties
```
### Function: GetGrid
```
Get the CSRectGrid assigned to this class.

        See Also
        --------
        CSXCAD.CSRectGrid, DefineGrid
```
### Function: GetParameterSet
```
Get the parameter set assigned to this class 
```
### Function: GetPropertiesByName
```
GetPropertiesByName(name)

        Get all the property specifed by their name
```
### Function: GetProperty
```
GetProperty(index)

        Get the property at the given index

        See Also
        --------
        CSXCAD.GetQtyProperties
```
### Function: GetPropertyByCoordPriority
```
GetPropertyByCoordPriority(coord, prop_type=None, markFoundAsUsed=False) 
```
### Function: GetPropertyByType
```
GetPropertyByType(prop_type)

        Get a list of properties specified by their type
```
### Function: GetQtyPrimitives
_No documentation available_
### Function: GetQtyProperties
_No documentation available_
### Function: ReadFromXML
```
ReadFromXML(fn)

        Read geometry from xml-file

        :param fn: str -- file name
```
### Function: SetMeshType
_No documentation available_
### Function: Update
_No documentation available_
### Function: Write2XML
```
Write2XML(fn)

        Write geometry to an xml-file

        :param fn: str -- file name
```
### Function: _ContinuousStructure__CreateProperty
_No documentation available_



