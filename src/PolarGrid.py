import numpy as np

def BuildCircle(Rho=1, Centroid=(0,0), Tau=1000):
    CircleGeom = []
    UniqueID = 1
    Precision = 360.0 / float(Tau)
    for angle in np.arange(0, 360.001, Precision):
        Y = np.sin(np.radians(angle))
        X = np.cos(np.radians(angle))

        AdjustedY = (Y + float(Centroid[1])) * float(Rho)
        AdjustedX = (X + float(Centroid[0])) * float(Rho)

        CircleGeom.append((UniqueID, AdjustedX, AdjustedY))
        UniqueID += 1

    CircleArray = np.asarray(CircleGeom, dtype=([('UniqueID', 'i4'),('X','f4'),('Y','f4')]))

    return CircleArray
