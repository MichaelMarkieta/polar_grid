"""
Copyright (c) 2012 Michael Markieta
See the file license.txt for copying permission.
"""
import numpy as np
try:
    import arcpy # arcpy used to build shapefile for ArcGIS users; only applicable to ArcGis users
except ImportError:
    pass


#noinspection PyUnusedLocal
def polar_grid(rho=1, centroid=(0,0), theta=4, rings=0, tau=4000):
    """
    This function is used to build a Numpy Array that contains the geometry
    necessary to build a polar grid shape on a geographic coordinate system.
    --------------------------------------------------------------------------------------------------------------------
    :param rho:         Radius of the grid
    :type rho:          Float
    :param centroid:    Origin of the grid
    :type centroid:     2 item tuple of floats (float, float)
    :param theta:       Number of radial dividers of Rho*2 distance that divide the grid into equal 1/2s, 1/4s, 1/8s...
    :type theta:        Integer
    :param rings:       [TODO:] Number of circular concentric dividers
    type Rings:         [TODO:] Integer
    :param tau:         Frequency at which points are placed along the perimeter of the grid
    :type tau:          Integer
    --------------------------------------------------------------------------------------------------------------------
    The geometry is returned in a numpy array of (unique_id, [[X1,Y1],[X2,Y2],...,[Xn,Yn]])
    unique_id:           The unique identifier for each radial divider
    x:                  The x coordinate pair of a point in the geometry of the respective radial divider
    y:                  The y coordinate pair of a point in the geometry of the respective radial divider
    """
    coord_list = [] # Store the coordinate pairs
    polar_geom = [] # Stores the unique id of a radial divider and it's geometric coordinate pairs

    # Number of points along the perimeter per radial divider in relation to Tau (more points as Tau increases)
    tau_relative_to_theta = np.floor(float(tau) * (1.0 / float(theta)))

    # Tau adjusted for rounding error in tau_relative_to_theta when using floor method
    adjusted_tau = tau_relative_to_theta * theta

    unique_id = 1 # The unique identifier for each radial divider
    count_iterations = 0 # Start counter for each pass in the for loop at 0

    min = 0.0 # First angle, in degrees, on our polar grid
    max = 360.0 # Last angle, in degrees, on our polar grid

    # Iterate around a circle (360 degrees), building the polar grid by catching the significant coordinate pairs
    for angle in np.linspace(min, max, num=adjusted_tau, endpoint=True):
        # Must convert degrees to radians here
        x = np.cos(angle * np.pi / 180.0)
        y = np.sin(angle * np.pi / 180.0)

        # Shift coordinates about centroid and extend to accommodate Rho
        adjusted_x = ((x * float(rho)) + (float(centroid[0])))
        adjusted_y = ((y * float(rho)) + (float(centroid[1])))

        # The first item in our for statement
        if angle == 0:
            coord_list.append([centroid[0], centroid[1]])
            coord_list.append([adjusted_x, adjusted_y])

        # Catches the final point along the perimeter of the polar grid and closes the geometry.
        elif angle == max:
            coord_list.append([adjusted_x, adjusted_y])
            coord_list.append([polar_geom[0][1][1][0],polar_geom[0][1][1][1]]) # First point on the first radial divider.
            coord_list.append([centroid[0], centroid[1]])
            polar_geom.append((unique_id, coord_list))

        # Catches the final point along the perimeter for each radial divider, and closes the geometry
        elif count_iterations % tau_relative_to_theta == 0:
            coord_list.append([adjusted_x, adjusted_y])
            coord_list.append([centroid[0], centroid[1]])
            polar_geom.append((unique_id, coord_list))

            unique_id += 1 # Increase the unique_id field for each subsequent radial divider geometry

            coord_list = [[centroid[0], centroid[1]],[adjusted_x, adjusted_y]]

        # All points along the perimeter of the polar grid that do not fall on angle Theta
        else:
            coord_list.append([adjusted_x, adjusted_y])

        count_iterations += 1

    # Determine the number of coordinate pair entries so that our np.array is created to size
    array_index = len(polar_geom[0][1]) # All radial dividers will have the same number (length) of coordinate pairs

    # Create a np.array that stores the polar grid geometry by radial divider
    polar_geom_array = np.asarray(polar_geom, np.dtype([('unique_id', np.str, 4),('XY', '<f8', (array_index, 2))]))
    return polar_geom_array


def to_shp(polar_geom_array, output):
    """
    This function is used to create a shapefile from the polar grid
    geometry array returned from the polar_grid function.
    --------------------------------------------------------------------------------------------------------------------
    :param polar_geom_array:    Array object returned by polar_grid function
    :type polar_geom_array:     np.array
    :param output:              Output path including name and format (C:/Path/To/File.shp)
    :type output:               String
    """
    point = arcpy.Point() # Empty point object
    array = arcpy.Array() # Empty array object

    feature_list = [] # A list that will hold each of the radial divider objects

    # For each coordinate pair, set the x,y properties and add to the Array object.
    for unique_id in range(0,len(polar_geom_array)):
        for coord_pair in polar_geom_array[unique_id][1]:
            point.X = coord_pair[0]
            point.Y = coord_pair[1]
            point.ID = unique_id
            array.add(point)

        polygon = arcpy.Polygon(array) # Create a polygon object based on the array of points
        array.removeAll() # Clear the array for future use
        feature_list.append(polygon) # Append to the list of polygon objects

    arcpy.CopyFeatures_management(feature_list, output) # Write the polar grid geometry to a shapefile
