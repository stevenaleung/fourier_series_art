import csv
import numpy as np
import matplotlib.pyplot as plt


def calculateFourierComponents(xCoordinates, yCoordinates):


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