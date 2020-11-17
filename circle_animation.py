## imports
import pdb

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

from createCirclePlot import *


## setup
numFramesTotal = 100
numFramesSingleCycle = 200
numCircles = 3
radiiCircle = np.array([1.0, 0.5, 0.3])
rotationSpeed = np.array([1.0, 0.5, 0.3])

# get the default colormap
cmap = plt.rcParams['axes.prop_cycle'].by_key()['color']

# setup the figure and axis
fig = plt.figure()
ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
ax.set_aspect('equal', 'box')

# setup the plot elements we want to animate
lines = [ax.plot([], [], linewidth=2, color=cmap[ind])[0] for ind in range(numCircles)]
circles = [ax.plot([], [], linewidth=0.5, color=cmap[ind])[0] for ind in range(numCircles)]
outline = ax.plot([], [], linewidth=2, color=[0,0,0])
artists = lines + circles + outline

# setup the circle coordinates
xCentersCircle = np.insert(np.cumsum(radiiCircle)[0:2], 0, 0.0)
xyCentersCircle = np.hstack((np.expand_dims(xCentersCircle, axis=1), np.zeros((numCircles,1))))

xyCoordsCircle = np.empty([numCircles,2,200])
for ind in np.arange(numCircles):
    xyCoordsCircle[ind,0,:], xyCoordsCircle[ind,1,:] = createCircle(xyCentersCircle[ind][0], xyCentersCircle[ind][1],radiiCircle[ind]);

# setup the line coordinates

pdb.set_trace()



## animation
# initialization function: plot the background of each frame
def init():
    # initialize lines
    for line in lines:
        line.set_data([], [])

    # initialize circles
    for ind in np.arange(numCircles):
        circles[ind].set_data(xyCoordsCircle[ind][0], xyCoordsCircle[ind][1])

    return artists

# animate function. this is called sequentially
def animate(iteration):
    angle_rad = float(iteration)/numFramesTotal*2*np.pi*rotationSpeed
    xPositionsLine = np.cos(angle_rad)*radiiCircle
    yPositionsLine = np.sin(angle_rad)*radiiCircle
    xPositionsLineCumsum = np.cumsum(xPositionsLine)
    yPositionsLineCumsum = np.cumsum(yPositionsLine)
    xTmp = np.insert(xPositionsLineCumsum, 0, 0);
    yTmp = np.insert(yPositionsLineCumsum, 0, 0);

    # line drawing
    for ind in np.arange(numCircles):
        xLine = xTmp[ind:ind+2]
        yLine = yTmp[ind:ind+2]
        lines[ind].set_data(xLine, yLine)

    # circle drawing
    for ind in np.arange(1,numCircles):
        xCoordsCircle = xyCoordsCircle[ind][0]+(xPositionsLineCumsum[ind-1]-xyCentersCircle[ind][0])
        yCoordsCircle = xyCoordsCircle[ind][1]+(yPositionsLineCumsum[ind-1]-xyCentersCircle[ind][1])
        circles[ind].set_data(xCoordsCircle, yCoordsCircle)

    # outline drawing
    if iteration == 0:
        # need to handle empty array from get_xdata()
        xOutline = np.array(xPositionsLineCumsum[-1])
        yOutline = np.array(yPositionsLineCumsum[-1])
    elif iteration == 1:
        # need to handle scalar value from get_xdata()
        xOutline1 = np.array([outline[0].get_xdata()])
        xOutline2 = np.array([xPositionsLineCumsum[-1]])
        yOutline1 = np.array([outline[0].get_ydata()])
        yOutline2 = np.array([yPositionsLineCumsum[-1]])
        xOutline = np.concatenate((xOutline1,xOutline2))
        yOutline = np.concatenate((yOutline1,yOutline2))
    else:
        xOutline1 = np.array(outline[0].get_xdata())
        xOutline2 = np.array([xPositionsLineCumsum[-1]])
        yOutline1 = np.array(outline[0].get_ydata())
        yOutline2 = np.array([yPositionsLineCumsum[-1]])
        xOutline = np.concatenate((xOutline1,xOutline2))
        yOutline = np.concatenate((yOutline1,yOutline2))
    outline[0].set_data(xOutline, yOutline)

    return artists

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=numFramesTotal, interval=20, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html

# anim.save('circle_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
