import sys
import csv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import utils


## setup
numFramesTotal = 250
numFramesSingleCycle = 50
numCircles = 1000                               # number of frequencies to use
numCirclesToDraw = 50                           # number of frequencies to show in animation

frequencyScaling = 1000
amplitudeScaling = float(1/30)



## calculate fourier components
coordinatesFilepath = sys.argv[1]
xCoordinates, yCoordinates = utils.getDrawingCoordinates(coordinatesFilepath, stepSizeNew=1)
frequenciesAll, amplitudesAll, phasesAll = utils.calculateFourierComponents(xCoordinates, yCoordinates)

# specify circle rotation speed, amplitude, and starting phase
rotationSpeeds = -frequenciesAll[1:numCircles+1]*frequencyScaling       # negative sign used to account for coordinate axes difference btw inkscape and python
radiiCircle = amplitudesAll[1:numCircles+1]*amplitudeScaling
phases = phasesAll[1:numCircles+1]

# DC offset
dcOffsetX = np.ptp(xCoordinates)
dcOffsetY = np.ptp(yCoordinates)
dcOffsetX *= amplitudeScaling
dcOffsetY *= amplitudeScaling
dcOffsetX = 0
dcOffsetY = 0


## setup the figure and axis
cmap = plt.rcParams['axes.prop_cycle'].by_key()['color']
fig = plt.figure()
ax = plt.axes(xlim=(-10, 10), ylim=(-10, 10))
ax.set_aspect('equal', 'box')
plt.xticks([])
plt.yticks([])
# plt.axis('off')

# setup the plot elements we want to animate
lines = [ax.plot([], [], linewidth=2)[0] for ind in range(numCirclesToDraw)]
circles = [ax.plot([], [], linewidth=0.5)[0] for ind in range(numCirclesToDraw)]
outline = ax.plot([], [], linewidth=2, color=[0,0,0])
artists = lines + circles + outline

# setup the circle coordinates
xCentersCircle = np.insert(np.cumsum(radiiCircle)[0:numCirclesToDraw-1], 0, 0.0)
yCentersCircle = np.zeros((numCirclesToDraw,1))
xCentersCircle -= dcOffsetX
yCentersCircle -= dcOffsetY    
xyCentersCircle = np.hstack((np.expand_dims(xCentersCircle, axis=1), yCentersCircle))

xyCoordsCircle = np.empty([numCirclesToDraw,2,200])
for ind in np.arange(numCirclesToDraw):
    xyCoordsCircle[ind,0,:], xyCoordsCircle[ind,1,:] = utils.getCircleCoordinates(xyCentersCircle[ind][0], xyCentersCircle[ind][1],radiiCircle[ind]);


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
    # add all the lines end to end to determine where they each should be
    xPositionsLineCumsum = np.cumsum(xPositionsLine)
    yPositionsLineCumsum = np.cumsum(yPositionsLine)
    xPositionsLineCumsum -= dcOffsetX
    yPositionsLineCumsum -= dcOffsetY

    # line drawing
    xTmp = np.insert(xPositionsLineCumsum, 0, -dcOffsetX);
    yTmp = np.insert(yPositionsLineCumsum, 0, -dcOffsetY);
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

# movieSaveFilepath = coordinatesFilepath[:-4] + '.mp4'
# anim.save(movieSaveFilepath, fps=30, dpi=300, extra_args=['-vcodec', 'libx264'])
# movieSaveFilepath = coordinatesFilepath[:-4] + '.gif'
# anim.save(movieSaveFilepath, fps=30, writer='imagemagick')

plt.show()
