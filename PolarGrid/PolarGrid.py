"""
Copyright (c) 2012 Michael Markieta
See the file license.txt for copying permission.
"""
import numpy as np

def PolarGrid(Rho=1, Centroid=(0,0), Theta=2, Rings=1, Tau=1000):
    """
    This function is used to build a Numpy Array that contains the geometry
    necessary to build a polar grid shape on a geographic coordinate system.
    --------------------------------------------------------------------------------------------------------------------
    Rho:        Radius of the grid
    Centroid:   Origin of the grid
    Theta:      Number of radial dividers of Rho*2 distance that divide the grid into equal 1/2s, 1/4s, 1/8s...
    Rings:      [To come] Number of circular concentric dividers
    Tau:        Frequency at which points are placed along the perimeter of the grid (higher frequency = smoother edge)
    --------------------------------------------------------------------------------------------------------------------
    The geometry is returned in a numpy array of (UniqueID, [[X1,Y1],[X2,Y2],...,[Xn,Yn]])
    UniqueID:   The unique identifier for each radial divider
    X:          The X coordinate pair of a point in the geometry of the respective radial divider
    Y:          The Y coordinate pair of a point in the geometry of the respective radial divider
    """
    CoordList = [] # Store the coordinate pairs
    PolarGeom = [] # Stores the unique id of a radial divider and it's geometric coordinate pairs

    AngleTheta = 360 / int(Theta)
    Precision = 360.0 / float(Tau)
    UniqueID = 1

    # Iterate around a circle (360 degrees), building the polar grid by catching the significant coordinate pairs
    for angle in np.arange(0, 360.01, Precision):
        # Must convert degrees to radians here
        X = np.cos(np.radians(angle))
        Y = np.sin(np.radians(angle))

        # Shift coordinates about centroid and extend to accommodate Rho
        AdjustedX = (X + float(Centroid[0])) * float(Rho)
        AdjustedY = (Y + float(Centroid[1])) * float(Rho)

        # The first item in our for statement
        if angle == 0:
            CoordList.append([Centroid[0], Centroid[1]])
            CoordList.append([AdjustedX, AdjustedY])

        # Catches the final point along the perimeter of the polar grid at any angle Theta, and closes the geometry
        elif angle % AngleTheta == 0:
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

    # Determine the number of coordinate pair entries so that our np.array is created to size
    ArrayIndex = len(PolarGeom[0][1])

    # Create a np.array that stores the polar grid geometry by radial divider
    PolarGeomArray = np.asarray(PolarGeom, np.dtype([('UniqueID', np.str, 4),('XY', '<f8', (ArrayIndex, 2))]))
    return PolarGeomArray
