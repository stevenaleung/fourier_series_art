import csv
import numpy as np

openFilename = 'testCoordinates2.csv'
saveFilename = 'fourierComponents2.csv'

with open(openFilename, newline='') as csvfile:
    csvfileReader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    headers = csvfileReader.__next__()
    xyCoordinates = []
    for row in csvfileReader:
        xyCoordinates.append(row)

xyCoordinates = np.asarray(xyCoordinates)

stepSizes = np.sum(np.power(np.diff(xyCoordinates, axis=0), 2), axis=1)
stepSizeMean = np.mean(stepSizes)

distances = np.insert(np.cumsum(stepSizes), 0, 0)

stepSizeNew = 1
distancesNew = np.arange(0, distances[-1], stepSizeNew)
xCoordinates = np.interp(distancesNew, distances, xyCoordinates[:,0])
yCoordinates = np.interp(distancesNew, distances, xyCoordinates[:,1])


import matplotlib.pyplot as plt

fig = plt.figure()
plt.plot(distances, xyCoordinates[:,0])
plt.plot(distances, xyCoordinates[:,1])
# plt.show()


fig = plt.figure()
plt.plot(xCoordinates, yCoordinates)
plt.axis('equal')
# plt.show()


fig = plt.figure()
plt.plot(distancesNew, xCoordinates)
plt.plot(distancesNew, yCoordinates)
# plt.show()

tmp1 = xCoordinates + 1j*yCoordinates;
tmp2 = np.fft.fftshift(np.fft.fft(tmp1))
freqs = np.fft.fftshift(np.fft.fftfreq(tmp1.shape[-1]))

numSamples = tmp1.shape[0]
amplitudes = 2/numSamples * np.abs(tmp2)
phases = np.angle(tmp2)


fig = plt.figure()
plt.plot(freqs, amplitudes)
# plt.show()

plt.plot(np.real(tmp2))
plt.plot(np.imag(tmp2))


sortOrder = np.argsort(amplitudes)[::-1]
freqsSorted = freqs[sortOrder]
amplitudesSorted = amplitudes[sortOrder]
phasesSorted = phases[sortOrder]


with open(saveFilename, 'w', newline='') as csvfile:
    csvfileWriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    csvfileWriter.writerow(['frequency', 'amplitude', 'phase'])
    for ind in np.arange(freqsSorted.shape[0]):
        csvfileWriter.writerow([freqsSorted[ind], amplitudesSorted[ind], phasesSorted[ind]])

