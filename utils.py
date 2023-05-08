import csv
import numpy as np


def get_drawing_coordinates(filepath, step_size):
    xy_coordinates = get_coordinates(filepath)
    x_coordinates, y_coordinates = resample_coordinates(xy_coordinates, step_size)
    # negative sign used to account for coordinate axes difference btw inkscape and python
    return x_coordinates, -y_coordinates


def get_coordinates(filepath):
    with open(filepath, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        headers = csv_reader.__next__()
        xy_coordinates = []
        for row in csv_reader:
            xy_coordinates.append(row)
    xy_coordinates = np.asarray(xy_coordinates)
    return xy_coordinates


def resample_coordinates(xy_coordinates, step_size):
    # determine distance from each point to the starting point
    step_sizes = np.sum(np.power(np.diff(xy_coordinates, axis=0), 2), axis=1)
    distances_orig = np.insert(np.cumsum(step_sizes), 0, 0)

    # interpolate the x and y coordinate arrays
    distances_new = np.arange(0, distances_orig[-1], step_size)
    x_coordinates = np.interp(distances_new, distances_orig, xy_coordinates[:,0])
    y_coordinates = np.interp(distances_new, distances_orig, xy_coordinates[:,1])
    return x_coordinates, y_coordinates


def scale_coordinates(x_coords, y_coords, target_half_extent):
    coords_max_extent = np.maximum(np.ptp(x_coords), np.ptp(y_coords))
    x_coords_scaled = x_coords / coords_max_extent * (target_half_extent * 2)
    y_coords_scaled = y_coords / coords_max_extent * (target_half_extent * 2)
    return x_coords_scaled, y_coords_scaled


def get_fourier_components(x_coordinates, y_coordinates):
    ## calculate the fourier components
    # compute the fft for the coordinates
    complex_coordinates = x_coordinates + 1j*y_coordinates
    complex_coordinates_fft = np.fft.fftshift(np.fft.fft(complex_coordinates))
    freqs = np.fft.fftshift(np.fft.fftfreq(complex_coordinates.shape[-1]))

    # scale the coefficient magnitudes
    num_samples = complex_coordinates.shape[0]
    magnitudes = np.abs(complex_coordinates_fft) / num_samples

    # grab the phases
    phases = np.angle(complex_coordinates_fft)

    # sort by largest magnitude
    sort_order = np.argsort(magnitudes)[::-1]
    freqs_sorted = freqs[sort_order]
    magnitudes_sorted = magnitudes[sort_order]
    phases_sorted = phases[sort_order]

    ## output results
    return freqs_sorted, magnitudes_sorted, phases_sorted


def initialize_artists(artists):
    for artist in artists:
        artist.set_data([], [])
    return artists


def update_artists(artists, outline, num_freqs_to_draw, frame_num):
    for (idx, artist) in enumerate(artists):
        if idx == 0:
            new_position = np.array([0.0, 0.0])
        else:
            new_position = artists[idx-1].line_endpoint
        artist.update(new_position)
        if idx < num_freqs_to_draw:
            artist.draw()

    outline_new_point = artists[-1].line_endpoint
    update_outline(outline, outline_new_point[0], outline_new_point[1])

    circles = [artist.circle_drawing for artist in artists[0:num_freqs_to_draw]]
    lines = [artist.line_drawing for artist in artists[0:num_freqs_to_draw]]
    artists_and_outline = circles + lines + [outline]

    return artists_and_outline


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
        x_coords, y_coords = get_circle_coordinates(x_centers_circle[idx], y_centers_circle[idx], circle_radii[idx])
        circle.set_data(x_coords, y_coords)


def get_circle_coordinates(x_center, y_center, radius):
    degrees_in_circle = 360
    angles_degree = np.linspace(0, degrees_in_circle, 200)
    angles_radian = np.deg2rad(angles_degree)
    x_locs = radius * np.cos(angles_radian) + x_center
    y_locs = radius * np.sin(angles_radian) + y_center
    return x_locs, y_locs


def update_outline(outline, x_pos, y_pos):
    x_outline = np.concatenate((outline.get_xdata(), np.array(x_pos, ndmin=1)))
    y_outline = np.concatenate((outline.get_ydata(), np.array(y_pos, ndmin=1)))
    outline.set_data(x_outline, y_outline)
