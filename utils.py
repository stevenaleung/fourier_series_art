import csv
import numpy as np


def get_drawing_coordinates(filepath, step_size):
    xy_coordinates = get_coordinates(filepath)
    x_coordinates, y_coordinates = resample_coordinates(xy_coordinates, step_size)
    return x_coordinates, y_coordinates


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


def get_fourier_components(x_coordinates, y_coordinates):
    ## calculate the fourier components
    # compute the fft for the coordinates
    complex_coordinates = x_coordinates + 1j*y_coordinates
    complex_coordinates_fft = np.fft.fftshift(np.fft.fft(complex_coordinates))
    freqs = np.fft.fftshift(np.fft.fftfreq(complex_coordinates.shape[-1]))

    # scale the coefficient magnitudes
    num_samples = complex_coordinates.shape[0]
    magnitudes = np.abs(complex_coordinates_fft) / num_samples * 2

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
    radius_circle = float(radius)
    x1 = np.linspace(radius_circle, -radius_circle, 100)
    x2 = np.linspace(-radius_circle, radius_circle, 100)
    y1 = np.sqrt(np.power(radius_circle,2)-np.power(x1,2))
    y2 = -np.sqrt(np.power(radius_circle,2)-np.power(x2,2))
    x_locs_circle = np.concatenate((x1,x2))+x_center
    y_locs_circle = np.concatenate((y1,y2))+y_center
    return x_locs_circle, y_locs_circle
