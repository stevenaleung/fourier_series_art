import csv
import numpy as np


def getDrawingCoordinates(filepath, stepSizeNew):


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


	##
	return xCoordinates, yCoordinates
