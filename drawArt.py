import sys
import utils
from matplotlib import pyplot as plt
from matplotlib import animation
from functools import partial
from os import path


## setup
axes_half_extent = 10
drawing_coverage_fraction = 0.6
drawing_half_extent = axes_half_extent * drawing_coverage_fraction

step_size = 1

num_freqs = 1000                    # number of frequencies to use
num_freqs_to_draw = 100             # number of frequencies to show in animation
frequency_scaling = 1000

num_frames = 250
num_frames_per_cycle = 50


def main():
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
    lines = [ax.plot([], [], linewidth=2)[0] for _ in range(num_freqs_to_draw)]
    circles = [ax.plot([], [], linewidth=0.5)[0] for _ in range(num_freqs_to_draw)]
    outline = ax.plot([], [], linewidth=2, color=[0,0,0])[0]
    artists = lines + circles + [outline]

    # animation
    anim = animation.FuncAnimation(
        fig,
        partial(utils.update_artists, lines, circles, outline, rotation_speeds, start_phases, circle_radii, num_frames_per_cycle),
        init_func=partial(utils.initialize_artists, artists),
        frames=num_frames,
        interval=20,
        blit=True,
    )

    # coordinates_filename = path.basename(coordinates_filepath)
    # save_path = "output"
    # gif_save_name = coordinates_filename.split(".csv")[0] + ".gif"
    # gif_save_path = path.join(save_path, gif_save_name)
    # anim.save(gif_save_path, fps=30)

    plt.show()


if __name__ == "__main__":
    main()
