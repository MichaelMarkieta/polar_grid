# What is a Polar Grid?

A polar grid can be defined as a circular grid that contain radial dividers
and concentric rings. This script lets us derive the geometry required to 
build a polar grid for use in various applications, including GIS. Polar grids 
are useful for visualizing data, but this script is not for that (I recommend 
matplotlib if that is what you're after)

# Why is it useful?

It was built because I have not come accross any tools in a GIS that allow
you to build a polar grid. Rather, we are left to first building a circle (buffer),
then divide that buffer into multiple radial sections (pizza triangles), and
further subdivide that into circular concentric rings.

# Want PolarGrid?

### Use `pip`

    $ pip install PolarGrid
    
Don't know what pip is? Wiki and download [here](http://pypi.python.org/pypi/pip).

### Or manually

Download and extract the latest working distribution: [0.1](https://github.com/MichaelMarkieta/PolarGrid/blob/master/dist/PolarGrid-0.1.zip)

    $ cd PolarGrid-0.1
    $ python setup.py install

# How do I use it?

    $ python
    >>>from PolarGrid import *
    >>>PolarGrid()

<img src="https://dl-web.dropbox.com/get/Photos/PolarGrid/Example1.png?w=7d4e6a67" width="400px"/>

    >>>PolarGrid(Rho=3, Centroid=(1,2), Theta=8, Tau=1000)

<img src="https://dl-web.dropbox.com/get/Photos/PolarGrid/Example2.png?w=673f971c" width="400px"/>

    >>>PolarGrid(4, (2,2), 16, 1000)
    
<img src="https://dl-web.dropbox.com/get/Photos/PolarGrid/Example3.png?w=7c277ed6" width="400px"/>

