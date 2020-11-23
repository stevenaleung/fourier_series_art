import sys
import csv
import numpy as np
import matplotlib.pyplot as plt


## setup
stepSizeNew = 1


## specify file names and paths
coordinatesFilename = sys.argv[1]
openFilepath = coordinatesFilename + '_coordinates.csv'
saveFilepath = coordinatesFilename + '_fourier_components.csv'


## create x and y coordinate arrays
# read the coordinates file
with open(openFilepath, newline='') as csvfile:
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


## save values to csv file
sortOrder = np.argsort(amplitudes)[::-1]
freqsSorted = freqs[sortOrder]
amplitudesSorted = amplitudes[sortOrder]
phasesSorted = phases[sortOrder]
with open(saveFilepath, 'w', newline='') as csvfile:
    csvfileWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    csvfileWriter.writerow(['frequency', 'amplitude', 'phase'])
    for ind in np.arange(freqsSorted.shape[0]):
        csvfileWriter.writerow([freqsSorted[ind], amplitudesSorted[ind], phasesSorted[ind]])
