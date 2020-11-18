## imports
import pdb

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

from createCirclePlot import *


import csv

with open('fourierComponents2.csv', newline='') as csvfile:
    csvfileReader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    headers = csvfileReader.__next__()
    data = []
    for row in csvfileReader:
        data.append(row)
data = np.asarray(data)
numCircles = 10
# rotationSpeeds = data[1:numCircles+1,0]*1000
# radiiCircle = data[1:numCircles+1,1]/70
# phases = data[1:numCircles+1,2]
rotationSpeeds = data[:numCircles,0]*1000
radiiCircle = data[:numCircles,1]/70
phases = data[:numCircles,2]


## setup
numFramesTotal = 2000
numFramesSingleCycle = 100
numCircles = 10
np.random.seed(94305)
# # # radiiCircle = np.sort(np.random.rand(numCircles)*0.5)[::-1]
# # # rotationSpeeds = np.sort(np.random.rand(numCircles))
# # radiiCircle = np.array([356.13125198,  78.31835378,  30.84879318,  20.99292418, 17.60222215,  16.34525484,  16.09254732,  15.05001482, 11.7131337 ,  10.57782973])
# # radiiCircle = radiiCircle/100
# # rotationSpeeds = np.array([ 0.        ,  0.00044484, -0.00088968, -0.00133452,  0.00133452, -0.00044484, -0.00177936,  0.00088968, -0.0022242 ,  0.00177936])
# # rotationSpeeds = rotationSpeeds*1000
# rotationSpeeds = np.array([ 0.00000000e+00, -9.08677874e-05, -3.63471149e-04,  9.08677874e-05,
#         1.81735575e-04,  2.72603362e-04, -2.72603362e-04,  5.45206724e-04,
#        -1.81735575e-04,  3.63471149e-04])*1000
# radiiCircle = np.array([366.16072071,  75.09359933,  70.91904466,  67.1571062 ,
#         57.52167601,  49.13138792,  27.82769199,  27.53797902,
#         26.7499727 ,  26.08882441])/100

# get the default colormap
cmap = plt.rcParams['axes.prop_cycle'].by_key()['color']

# setup the figure and axis
fig = plt.figure()
# ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
ax = plt.axes(xlim=(-10, 10), ylim=(-10, 10))
ax.set_aspect('equal', 'box')

# setup the plot elements we want to animate
lines = [ax.plot([], [], linewidth=2, color=cmap[ind])[0] for ind in range(numCircles)]
circles = [ax.plot([], [], linewidth=0.5, color=cmap[ind])[0] for ind in range(numCircles)]
outline = ax.plot([], [], linewidth=2, color=[0,0,0])
artists = lines + circles + outline

# setup the circle coordinates
xCentersCircle = np.insert(np.cumsum(radiiCircle)[0:numCircles-1], 0, 0.0)
xyCentersCircle = np.hstack((np.expand_dims(xCentersCircle, axis=1), np.zeros((numCircles,1))))
xyCoordsCircle = np.empty([numCircles,2,200])
for ind in np.arange(numCircles):
    xyCoordsCircle[ind,0,:], xyCoordsCircle[ind,1,:] = createCircle(xyCentersCircle[ind][0], xyCentersCircle[ind][1],radiiCircle[ind]);


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
    angle_rad = float(iteration)/numFramesSingleCycle*2*np.pi*rotationSpeeds+phases
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
