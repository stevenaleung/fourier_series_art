import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
ax.set_aspect('equal', 'box')
line, = ax.plot([], [], lw=2)

numFrames = 200

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
def animate(i):
    r = float(1)
    angle = float(i)/numFrames*2*np.pi
    x = np.cos(angle)/r
    y = np.sin(angle)/r
    if i < numFrames/2:
        x1 = np.linspace(1, x, 100)
        x = x1
        y = np.sqrt(np.power(r,2)-np.power(x,2))
    else:
        x1 = np.linspace(1, -1, 100)
        x2 = np.linspace(-1, x, 100)
        y1 = np.sqrt(np.power(r,2)-np.power(x1,2))
        y2 = -np.sqrt(np.power(r,2)-np.power(x2,2))
        x = np.concatenate((x1,x2))
        y = np.concatenate((y1,y2))
    # r = 1
    # if i<numFrames/2:
    #     x1 = np.linspace(1, 1-4*float(i)/numFrames, 100)
    #     x = x1
    #     y = np.sqrt(np.power(r,2)-np.power(x,2))
    # else:
    #     x1 = np.linspace(1, -1, 100)
    #     x2 = np.linspace(-1, -1+4*float(i-numFrames/2)/numFrames, 100)
    #     y1 = np.sqrt(np.power(r,2)-np.power(x1,2))
    #     y2 = -np.sqrt(np.power(r,2)-np.power(x2,2))
    #     x = np.concatenate((x1,x2))
    #     y = np.concatenate((y1,y2))
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=numFrames, interval=20, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html

anim.save('circle_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()