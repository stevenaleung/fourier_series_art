## imports
import pdb

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import csv

from createCirclePlot import *


## setup
numFramesTotal = 500
numFramesSingleCycle = 100
numCirclesToDraw = 10

# load fourier components
with open('hummingbird_fourier_components.csv', newline='') as csvfile:
    csvfileReader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    headers = csvfileReader.__next__()
    data = []
    for row in csvfileReader:
        data.append(row)
data = np.asarray(data)
numCircles = 1000
rotationSpeeds = -data[1:numCircles+1,0]*1000
radiiCircle = data[1:numCircles+1,1]/30
phases = data[1:numCircles+1,2]

# get the default colormap
cmap = plt.rcParams['axes.prop_cycle'].by_key()['color']

# setup the figure and axis
fig = plt.figure()
# ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
ax = plt.axes(xlim=(-10, 10), ylim=(-10, 10))
ax.set_aspect('equal', 'box')

# setup the plot elements we want to animate
lines = [ax.plot([], [], linewidth=2, color=cmap[ind])[0] for ind in range(numCirclesToDraw)]
circles = [ax.plot([], [], linewidth=0.5, color=cmap[ind])[0] for ind in range(numCirclesToDraw)]
outline = ax.plot([], [], linewidth=2, color=[0,0,0])
artists = lines + circles + outline

# setup the circle coordinates
xCentersCircle = np.insert(np.cumsum(radiiCircle)[0:numCirclesToDraw-1], 0, 0.0)
xyCentersCircle = np.hstack((np.expand_dims(xCentersCircle, axis=1), np.zeros((numCirclesToDraw,1))))
xyCoordsCircle = np.empty([numCirclesToDraw,2,200])
for ind in np.arange(numCirclesToDraw):
    xyCoordsCircle[ind,0,:], xyCoordsCircle[ind,1,:] = createCircle(xyCentersCircle[ind][0], xyCentersCircle[ind][1],radiiCircle[ind]);


## animation
# initialization function: plot the background of each frame
def init():
    # initialize lines
    for line in lines:
        line.set_data([], [])

    # initialize circles
    for ind in np.arange(numCirclesToDraw):
        circles[ind].set_data(xyCoordsCircle[ind][0], xyCoordsCircle[ind][1])

    return artists

# animate function. this is called sequentially
def animate(iteration):
    angle_rad = float(iteration)/numFramesSingleCycle*2*np.pi*rotationSpeeds-phases
    xPositionsLine = np.cos(angle_rad)*radiiCircle
    yPositionsLine = np.sin(angle_rad)*radiiCircle
    xPositionsLineCumsum = np.cumsum(xPositionsLine)
    yPositionsLineCumsum = np.cumsum(yPositionsLine)
    xTmp = np.insert(xPositionsLineCumsum, 0, 0);
    yTmp = np.insert(yPositionsLineCumsum, 0, 0);

    # line drawing
    for ind in np.arange(numCirclesToDraw):
        xLine = xTmp[ind:ind+2]
        yLine = yTmp[ind:ind+2]
        lines[ind].set_data(xLine, yLine)

    # circle drawing
    for ind in np.arange(1,numCirclesToDraw):
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
