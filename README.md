# What is a Polar Grid? #

A polar grid can be defined as a circular grid that contain radial dividers
and concentric rings. This script lets us derive the geometry required to 
build a polar grid for use in various applications, including GIS. Polar grids 
are useful for visualizing data, but this script is not for that (I recommend 
matplotlib if that is what you're after)

# Why? #

It was built because I have not come accross any tools in a GIS that allow
you to build a polar grid. Rather, we are left to first building a circle (buffer),
then divide that buffer into multiple radial sections (pizza triangles), and
further subdivide that into circular concentric rings.

# How? #

