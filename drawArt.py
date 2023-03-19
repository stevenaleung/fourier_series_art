import sys
import csv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import utils


## setup
num_frames = 250
num_frames_per_cycle = 50
num_circles = 1000                  # number of frequencies to use
num_circles_to_draw = 50            # number of frequencies to show in animation

frequency_scaling = 1000
amplitude_scaling = float(1/30)

step_size = 1


## calculate fourier components
coordinates_filepath = sys.argv[1]
x_coordinates, y_coordinates = utils.get_drawing_coordinates(coordinates_filepath, step_size)
frequencies_all, amplitudes_all, phases_all = utils.get_fourier_components(x_coordinates, y_coordinates)

# specify circle rotation speed, amplitude, and starting phase
rotation_speeds = -frequencies_all[1:num_circles+1]*frequency_scaling       # negative sign used to account for coordinate axes difference btw inkscape and python
circle_radii = amplitudes_all[1:num_circles+1]*amplitude_scaling
phases = phases_all[1:num_circles+1]

# DC offset
dc_offset_x = np.ptp(x_coordinates)
dc_offset_y = np.ptp(y_coordinates)
dc_offset_x *= amplitude_scaling
dc_offset_y *= amplitude_scaling
dc_offset_x = 0
dc_offset_y = 0


## setup the figure and axis
cmap = plt.rcParams['axes.prop_cycle'].by_key()['color']
fig = plt.figure()
ax = plt.axes(xlim=(-10, 10), ylim=(-10, 10))
ax.set_aspect('equal', 'box')
plt.xticks([])
plt.yticks([])
# plt.axis('off')

# setup the plot elements we want to animate
lines = [ax.plot([], [], linewidth=2)[0] for ind in range(num_circles_to_draw)]
circles = [ax.plot([], [], linewidth=0.5)[0] for ind in range(num_circles_to_draw)]
outline = ax.plot([], [], linewidth=2, color=[0,0,0])[0]
artists = lines + circles + [outline]


## animation
# initialization function: plot the background of each frame
def initialize_artists():
    for artist in artists:
        artist.set_data([], [])
    return artists


# animate function. this is called sequentially
def update_artists(iteration):
    current_phases_radian = float(iteration)/num_frames_per_cycle*2*np.pi*rotation_speeds - phases
    x_centers_circle, y_centers_circle = get_circle_centers(circle_radii, current_phases_radian)

    # line drawing
    update_lines(lines, x_centers_circle, y_centers_circle)

    # circle drawing
    update_circles(circles, circle_radii, x_centers_circle, y_centers_circle)

    # outline drawing
    update_outline(outline, x_centers_circle[-1], y_centers_circle[-1])

    return artists


def get_circle_centers(radii, phases_radian):
    x_line_endpoints = np.cos(phases_radian) * radii
    y_line_endpoints = np.sin(phases_radian) * radii

    # add the lines end to end to find the circle centers
    x_centers_circle = np.concatenate(([0], np.cumsum(x_line_endpoints)))
    y_centers_circle = np.concatenate(([0], np.cumsum(y_line_endpoints)))

    return x_centers_circle, y_centers_circle


def update_lines(lines, x_line_endpoints, y_line_endpoints):
    for idx, line in enumerate(lines):
        x_line = x_line_endpoints[idx:idx+2]
        y_line = y_line_endpoints[idx:idx+2]
        line.set_data(x_line, y_line)


def update_circles(circles, circle_radii, x_centers_circle, y_centers_circle):
    for idx, circle in enumerate(circles):
        x_coords, y_coords = utils.get_circle_coordinates(x_centers_circle[idx], y_centers_circle[idx], circle_radii[idx])
        circle.set_data(x_coords, y_coords)


def update_outline(outline, x_pos, y_pos):
    x_outline = np.concatenate((outline.get_xdata(), np.array(x_pos, ndmin=1)))
    y_outline = np.concatenate((outline.get_ydata(), np.array(y_pos, ndmin=1)))
    outline.set_data(x_outline, y_outline)


# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(
    fig,
    update_artists,
    init_func=initialize_artists,
    frames=num_frames,
    interval=20,
    blit=True,
)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html

# movieSaveFilepath = coordinates_filepath[:-4] + '.mp4'
# anim.save(movieSaveFilepath, fps=30, dpi=300, extra_args=['-vcodec', 'libx264'])
# movieSaveFilepath = coordinates_filepath[:-4] + '.gif'
# anim.save(movieSaveFilepath, fps=30, writer='imagemagick')

plt.show()
