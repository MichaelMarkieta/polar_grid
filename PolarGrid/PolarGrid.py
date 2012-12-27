"""
Copyright (c) 2012 Michael Markieta
See the file license.txt for copying permission.
"""
import numpy as np

def PolarGrid(Rho=1, Centroid=(0,0), Theta=2, Rings=0, Tau=1000):
    """
    This function is used to build a Numpy Array that contains the geometry
    necessary to build a polar grid shape on a geographic coordinate system.
    --------------------------------------------------------------------------------------------------------------------
    :param Rho:         Radius of the grid
    :type Rho:          Float
    :param Centroid:    Origin of the grid
    :type Centroid:     2 item tuple of floats (float, float)
    :param Theta:       Number of radial dividers of Rho*2 distance that divide the grid into equal 1/2s, 1/4s, 1/8s...
    :type Theta:        Integer
    :param Rings:       [TODO:] Number of circular concentric dividers
    type Rings:         [TODO:] Integer
    :param Tau:         Frequency at which points are placed along the perimeter of the grid
    :type Tau:          Integer
    --------------------------------------------------------------------------------------------------------------------
    The geometry is returned in a numpy array of (UniqueID, [[X1,Y1],[X2,Y2],...,[Xn,Yn]])
    UniqueID:           The unique identifier for each radial divider
    X:                  The X coordinate pair of a point in the geometry of the respective radial divider
    Y:                  The Y coordinate pair of a point in the geometry of the respective radial divider
    """
    CoordList = [] # Store the coordinate pairs
    PolarGeom = [] # Stores the unique id of a radial divider and it's geometric coordinate pairs

    # Number of points along the perimeter per radial divider in relation to Tau (more points as Tau increases)
    TauRelativeToTheta = np.ceil(float(Tau) * (1.0 / float(Theta)))

    # Tau adjusted for rounding error in TauRelativeToTheta when using ceiling method
    AdjustedTau = TauRelativeToTheta * Theta

    UniqueID = 1 # The unique identifier for each radial divider
    CountIterations = 0 # Start counter for each pass in the for loop at 0

    Min = 0.0 # First angle, in degrees, on our polar grid
    Max = 360.0 # Last angle, in degrees, on our polar grid

    # Iterate around a circle (360 degrees), building the polar grid by catching the significant coordinate pairs
    for angle in np.linspace(Min, Max, num=AdjustedTau, endpoint=True):
        # Must convert degrees to radians here
        X = np.cos(np.radians(angle))
        Y = np.sin(np.radians(angle))

        # Shift coordinates about centroid and extend to accommodate Rho
        AdjustedX = ((X * float(Rho)) + (float(Centroid[0])))
        AdjustedY = ((Y * float(Rho)) + (float(Centroid[1])))

        # The first item in our for statement
        if angle == 0:
            CoordList.append([Centroid[0], Centroid[1]])
            CoordList.append([AdjustedX, AdjustedY])

        # Catches the final point along the perimeter of the polar grid and closes the geometry.
        elif angle == Max:
            CoordList.append([AdjustedX, AdjustedY])
            CoordList.append([PolarGeom[0][1][1][0],PolarGeom[0][1][1][1]]) # First point on the first radial divider.
            CoordList.append([Centroid[0], Centroid[1]])
            PolarGeom.append((UniqueID, CoordList))

        # Catches the final point along the perimeter for each radial divider, and closes the geometry
        elif CountIterations % TauRelativeToTheta == 0:
            CoordList.append([AdjustedX, AdjustedY])
            CoordList.append([Centroid[0], Centroid[1]])
            PolarGeom.append((UniqueID, CoordList))

            UniqueID += 1 # Increase the UniqueID field for each subsequent radial divider geometry
            CoordList = [] # Dump coordinate pairs from previous radial divider

            CoordList.append([Centroid[0], Centroid[1]])
            CoordList.append([AdjustedX, AdjustedY])

        # All points along the perimeter of the polar grid that do not fall on angle Theta
        else:
            CoordList.append([AdjustedX, AdjustedY])

        CountIterations += 1

    # Determine the number of coordinate pair entries so that our np.array is created to size
    ArrayIndex = len(PolarGeom[0][1]) # All radial dividers will have the same number (length) of coordinate pairs

    # Create a np.array that stores the polar grid geometry by radial divider
    PolarGeomArray = np.asarray(PolarGeom, np.dtype([('UniqueID', np.str, 4),('XY', '<f8', (ArrayIndex, 2))]))
    return PolarGeomArray
