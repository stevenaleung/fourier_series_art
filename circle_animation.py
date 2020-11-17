import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

# setup
cmap = plt.rcParams['axes.prop_cycle'].by_key()['color']

# get the coordinates for a circle
radiusCircle = float(1)
x1 = np.linspace(1, -1, 100)
x2 = np.linspace(-1, 1, 100)
y1 = np.sqrt(np.power(radiusCircle,2)-np.power(x1,2))
y2 = -np.sqrt(np.power(radiusCircle,2)-np.power(x2,2))
xLocsCircle = np.concatenate((x1,x2))
yLocsCircle = np.concatenate((y1,y2))

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
ax.set_aspect('equal', 'box')
circle, = ax.plot(xLocsCircle, yLocsCircle, linewidth=0.5, color=cmap[0])
line, = ax.plot([], [], linewidth=2, color=cmap[0])
outline, = ax.plot([], [], linewidth=2, color=[0,0,0])

numFrames = 200

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
def animate(i):
    radiusCircle = float(1)
    angle_rad = float(i)/numFrames*2*np.pi
    xPos = np.cos(angle_rad)/radiusCircle
    yPos = np.sin(angle_rad)/radiusCircle
    # line drawing
    xLine = np.array([0, xPos])
    yLine = np.array([0, yPos])
    line.set_data(xLine, yLine)
    # outline drawing
    if i < numFrames/2:
        xOutline = np.linspace(1, xPos, 100)
        yOutline = np.sqrt(np.power(radiusCircle,2)-np.power(xOutline,2))
    else:
        xOutline1 = np.linspace(1, -1, 100)
        xOutline2 = np.linspace(-1, xPos, 100)
        yOutline1 = np.sqrt(np.power(radiusCircle,2)-np.power(xOutline1,2))
        yOutline2 = -np.sqrt(np.power(radiusCircle,2)-np.power(xOutline2,2))
        xOutline = np.concatenate((xOutline1,xOutline2))
        yOutline = np.concatenate((yOutline1,yOutline2))
    outline.set_data(xOutline, yOutline)
    return line, outline,

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