import csv
import numpy as np


def get_drawing_coordinates(filepath, stepSizeNew):
    ## create x and y coordinate arrays
    # read the coordinates file
    with open(filepath, newline='') as csvfile:
        csvfileReader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        headers = csvfileReader.__next__()
        xyCoordinates = []
        for row in csvfileReader:
            xyCoordinates.append(row)
    xyCoordinates = np.asarray(xyCoordinates)

    # determine distance from each point to the starting point
    stepSizes = np.sum(np.power(np.diff(xyCoordinates, axis=0), 2), axis=1)
    stepSizeMean = np.mean(stepSizes)
    distances = np.insert(np.cumsum(stepSizes), 0, 0)

    # interpolate the x and y coordinate arrays
    distancesNew = np.arange(0, distances[-1], stepSizeNew)
    xCoordinates = np.interp(distancesNew, distances, xyCoordinates[:,0])
    yCoordinates = np.interp(distancesNew, distances, xyCoordinates[:,1])

    return xCoordinates, yCoordinates


def get_fourier_components(xCoordinates, yCoordinates):
    ## calculate the fourier components
    # compute the fft for the coordinates
    tmp1 = xCoordinates + 1j*yCoordinates;
    tmp2 = np.fft.fftshift(np.fft.fft(tmp1))
    freqs = np.fft.fftshift(np.fft.fftfreq(tmp1.shape[-1]))

    # scale the coefficient amplitudes
    numSamples = tmp1.shape[0]
    amplitudes = 2/numSamples * np.abs(tmp2)

    # grab the phases
    phases = np.angle(tmp2)

    # sort by largest amplitude
    sortOrder = np.argsort(amplitudes)[::-1]
    freqsSorted = freqs[sortOrder]
    amplitudesSorted = amplitudes[sortOrder]
    phasesSorted = phases[sortOrder]

    ## output results
    return freqsSorted, amplitudesSorted, phasesSorted


def get_circle_coordinates(xCenter, yCenter, radius):
    radiusCircle = float(radius)
    x1 = np.linspace(radiusCircle, -radiusCircle, 100)
    x2 = np.linspace(-radiusCircle, radiusCircle, 100)
    y1 = np.sqrt(np.power(radiusCircle,2)-np.power(x1,2))
    y2 = -np.sqrt(np.power(radiusCircle,2)-np.power(x2,2))
    xLocsCircle = np.concatenate((x1,x2))+xCenter
    yLocsCircle = np.concatenate((y1,y2))+yCenter
    return xLocsCircle, yLocsCircle
