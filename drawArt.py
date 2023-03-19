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

# setup the circle coordinates
x_centers_circle = np.insert(np.cumsum(circle_radii)[0:num_circles_to_draw-1], 0, 0.0)
y_centers_circle = np.zeros((num_circles_to_draw,1))
x_centers_circle -= dc_offset_x
y_centers_circle -= dc_offset_y    
xy_centers_circle = np.hstack((np.expand_dims(x_centers_circle, axis=1), y_centers_circle))

xy_coords_circle = np.empty([num_circles_to_draw,2,200])
for ind in np.arange(num_circles_to_draw):
    xy_coords_circle[ind,0,:], xy_coords_circle[ind,1,:] = utils.get_circle_coordinates(xy_centers_circle[ind][0], xy_centers_circle[ind][1],circle_radii[ind]);


## animation
# initialization function: plot the background of each frame
def initialize_artists():
    # initialize lines
    for line in lines:
        line.set_data([], [])

    # initialize circles
    for ind in np.arange(num_circles_to_draw):
        circles[ind].set_data(xy_coords_circle[ind][0], xy_coords_circle[ind][1])

    outline.set_data([], [])

    return artists

# animate function. this is called sequentially
def update_artists(iteration):
    angle_rad = float(iteration)/num_frames_per_cycle*2*np.pi*rotation_speeds-phases
    x_positions_line = np.cos(angle_rad)*circle_radii 
    y_positions_line = np.sin(angle_rad)*circle_radii
    # add all the lines end to end to determine where they each should be
    x_positions_line_cumsum = np.cumsum(x_positions_line)
    y_positions_line_cumsum = np.cumsum(y_positions_line)
    x_positions_line_cumsum -= dc_offset_x
    y_positions_line_cumsum -= dc_offset_y

    # line drawing
    x_tmp = np.insert(x_positions_line_cumsum, 0, -dc_offset_x);
    y_tmp = np.insert(y_positions_line_cumsum, 0, -dc_offset_y);
    for ind in np.arange(num_circles_to_draw):
        x_line = x_tmp[ind:ind+2]
        y_line = y_tmp[ind:ind+2]
        lines[ind].set_data(x_line, y_line)

    # circle drawing
    for ind in np.arange(1,num_circles_to_draw):
        x_coords_circle = xy_coords_circle[ind][0]+(x_positions_line_cumsum[ind-1]-xy_centers_circle[ind][0])
        y_coords_circle = xy_coords_circle[ind][1]+(y_positions_line_cumsum[ind-1]-xy_centers_circle[ind][1])
        circles[ind].set_data(x_coords_circle, y_coords_circle)

    # outline drawing
    x_outline1 = np.array(outline.get_xdata())
    x_outline2 = np.array([x_positions_line_cumsum[-1]])
    y_outline1 = np.array(outline.get_ydata())
    y_outline2 = np.array([y_positions_line_cumsum[-1]])
    x_outline = np.concatenate((x_outline1,x_outline2))
    y_outline = np.concatenate((y_outline1,y_outline2))
    outline.set_data(x_outline, y_outline)

    return artists

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
