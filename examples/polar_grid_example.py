"""
Copyright (c) 2012 Michael Markieta
See the file license.txt for copying permission.
"""
from polar_grid import polar_grid
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.axislines import SubplotZero

# Setup plotting for our polar grid
fig = plt.figure(1, figsize=(7,7))
ax = SubplotZero(fig, 111)
fig.add_subplot(ax)

# add axis lines for coordinate geometry (4 quadrants)
for direction in ["xzero", "yzero"]:
    ax.axis[direction].set_axisline_style("-|>", size=.75)
    ax.axis[direction].set_visible(True)

# remove axis lines/labels for rectangular geometry (-x and -y don't exist)
for direction in ["left", "right", "bottom", "top"]:
    ax.axis[direction].set_visible(False)

X = [] # hold x-coordinates from radial dividers
Y = [] # hold y-coordinates from radial dividers

# Generate geometry for a polar grid of 4-unit radius, centroid at (-2,1), with 8 divisions and precision of 4000 points
geom = polar_grid(rho=4, centroid=(-2,1), theta=8, tau=4000)

# Add coordinates from each radial divider to the X and Y lists
for num in range(0, len(geom)):
    for (x,y) in geom[num][1]:
        X.append(x)
        Y.append(y)

# Plot the coordinate pairs and connect each subsequent pair with a basic line
ax.plot(X,Y, color='red', linewidth=.75)
plt.margins(.25)
plt.show()
