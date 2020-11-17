import pdb

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

from createCirclePlot import *

# setup
cmap = plt.rcParams['axes.prop_cycle'].by_key()['color']

# setup the figure and axis
fig = plt.figure()
ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
ax.set_aspect('equal', 'box')

# setup the plot elements we want to animate
xyCentersCircle = [[0.0,0.0], [1.0,0.0], [1.5,0.0]]
circles = []
circles.extend(createCirclePlot(ax, 0.0, 0.0, 1.0, linewidth=0.5, color=cmap[0]))
circles.extend(createCirclePlot(ax, 1.0, 0.0, 0.5, linewidth=0.5, color=cmap[1]))
circles.extend(createCirclePlot(ax, 1.5, 0.0, 0.3, linewidth=0.5, color=cmap[2]))

circle, = ax.plot([], [], linewidth=2, color=cmap[0])
line, = ax.plot([], [], linewidth=2, color=cmap[0])
outline, = ax.plot([], [], linewidth=2, color=[0,0,0])

numFrames = 200

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    circle.set_data([], [])
    return line, circle,

# animation function. this is called sequentially
def animate(iteration):
    radiusCircle = float(1)
    angle_rad = float(iteration)/numFrames*2*np.pi
    xPos = np.cos(angle_rad)/radiusCircle
    yPos = np.sin(angle_rad)/radiusCircle
    # line drawing
    xLine = np.array([0, xPos])
    yLine = np.array([0, yPos])
    line.set_data(xLine, yLine)
    # circle drawing
    # circle.set_data(np.linspace(0,float(iteration)/numFrames,10), np.linspace(0,float(iteration)/numFrames,10))
    # circle.set_data(circles[1].get_xdata()+float(iteration)/numFrames, circles[1].get_ydata())
    circle.set_data(circles[1].get_xdata()+(xPos-xyCentersCircle[1][0]), circles[1].get_ydata()+(yPos-xyCentersCircle[1][1]))
    # outline drawing
    if iteration == 0:
        # need to handle empty array from get_xdata()
        xOutline = np.array(xPos)
        yOutline = np.array(yPos)
    elif iteration == 1:
        # need to handle scalar value from get_xdata()
        xOutline1 = np.array([outline.get_xdata()])
        xOutline2 = np.array([xPos])
        yOutline1 = np.array([outline.get_ydata()])
        yOutline2 = np.array([yPos])
        xOutline = np.concatenate((xOutline1,xOutline2))
        yOutline = np.concatenate((yOutline1,yOutline2))
    else:
        xOutline1 = np.array(outline.get_xdata())
        xOutline2 = np.array([xPos])
        yOutline1 = np.array(outline.get_ydata())
        yOutline2 = np.array([yPos])
        xOutline = np.concatenate((xOutline1,xOutline2))
        yOutline = np.concatenate((yOutline1,yOutline2))
    outline.set_data(xOutline, yOutline)
    return line, outline, circle

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=numFrames, interval=20, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html

# anim.save('circle_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
