import sys
import csv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import utils


## setup
axes_half_extent = 10
drawing_coverage_fraction = 0.6
drawing_half_extent = axes_half_extent * drawing_coverage_fraction

num_frames = 250
num_frames_per_cycle = 50
num_freqs = 1000                    # number of frequencies to use
num_circles_to_draw = 50            # number of frequencies to show in animation

frequency_scaling = 1000
step_size = 1

# calculate fourier components
coordinates_filepath = sys.argv[1]
x_coords, y_coords = utils.get_drawing_coordinates(coordinates_filepath, step_size)
x_coords_scaled, y_coords_scaled = utils.scale_coordinates(x_coords, y_coords, drawing_half_extent)
frequencies, magnitudes, phases = utils.get_fourier_components(x_coords_scaled, y_coords_scaled)

# specify circle rotation speed, radius, and starting phase
rotation_speeds = frequencies[1:num_freqs+1] * frequency_scaling
circle_radii = magnitudes[1:num_freqs+1]
start_phases = phases[1:num_freqs+1]

# setup the figure and axis
cmap = plt.rcParams['axes.prop_cycle'].by_key()['color']
fig = plt.figure()
axes_limits = (-axes_half_extent, axes_half_extent)
ax = plt.axes(xlim=axes_limits, ylim=axes_limits)
ax.set_aspect('equal', 'box')
plt.xticks([])
plt.yticks([])

# setup the plot elements we want to animate
lines = [ax.plot([], [], linewidth=2)[0] for ind in range(num_circles_to_draw)]
circles = [ax.plot([], [], linewidth=0.5)[0] for ind in range(num_circles_to_draw)]
outline = ax.plot([], [], linewidth=2, color=[0,0,0])[0]
artists = lines + circles + [outline]


## animation
def initialize_artists():
    for artist in artists:
        artist.set_data([], [])
    return artists


def update_artists(iteration):
    current_phases_radian = float(iteration)/num_frames_per_cycle*2*np.pi*rotation_speeds + start_phases
    x_centers_circle, y_centers_circle = get_circle_centers(circle_radii, current_phases_radian)
    update_lines(lines, x_centers_circle, y_centers_circle)
    update_circles(circles, circle_radii, x_centers_circle, y_centers_circle)
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
