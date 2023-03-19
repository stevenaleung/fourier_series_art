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


def get_circle_coordinates(x_center, y_center, radius):
    degrees_in_circle = 360
    angles_degree = np.linspace(0, degrees_in_circle, 200)
    angles_radian = np.deg2rad(angles_degree)
    x_locs = radius * np.cos(angles_radian) + x_center
    y_locs = radius * np.sin(angles_radian) + y_center
    return x_locs, y_locs


def initialize_artists(artists):
    for artist in artists:
        artist.set_data([], [])
    return artists
