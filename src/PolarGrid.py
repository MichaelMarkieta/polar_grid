import numpy as np

def PolarGrid(Rho=1, Centroid=(0,0), Theta=2, Rings=1, Tau=1000):
    """
    Returns the geometry of a polar grid, given:
    Rho:        Radius of the grid
    Centroid:   Origin of the grid
    Theta:      Number of radial dividers of Rho*2 distance that divide the grid into equal 1/2s, 1/4s, 1/8s, 1/16s...
    Tau:        Frequency at which points are placed along the perimeter of the grid (higher frequency = smoother edge)
    --------------------------------------------------------------------------------------------------------------------
    The geometry is returned in a numpy array of dtype.names (UniqueID, X, Y).
    """
    UniqueID = 1
    PolarGeom = []
    ThetaAngle = 360 / int(Theta)
    Precision = 360.0 / float(Tau)

    # First coordinate will be the centroid of the grid
    PolarGeom.append((0, Centroid[0], Centroid[1]))

    for angle in np.arange(0, 360.01, Precision):
        X = np.cos(np.radians(angle))
        Y = np.sin(np.radians(angle))

        AdjustedX = (X + float(Centroid[0])) * float(Rho)
        AdjustedY = (Y + float(Centroid[1])) * float(Rho)

        if UniqueID == 1:
            PolarGeom.append((UniqueID, AdjustedX, AdjustedY))
        elif angle % ThetaAngle == 0:
            PolarGeom.append((UniqueID, AdjustedX, AdjustedY))
            UniqueID += 1
            PolarGeom.append((UniqueID, Centroid[0], Centroid[1]))
        else:
            PolarGeom.append((UniqueID, AdjustedX, AdjustedY))

        UniqueID += 1

    PolarGeomArray = np.asarray(PolarGeom, dtype=([('UniqueID', 'i4'),('X','f4'),('Y','f4')]))
    return PolarGeomArray
