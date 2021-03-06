import pdb
import numpy as np


def getCircleCoordinates(xCenter, yCenter, radius):
	radiusCircle = float(radius)
	x1 = np.linspace(radiusCircle, -radiusCircle, 100)
	x2 = np.linspace(-radiusCircle, radiusCircle, 100)
	y1 = np.sqrt(np.power(radiusCircle,2)-np.power(x1,2))
	y2 = -np.sqrt(np.power(radiusCircle,2)-np.power(x2,2))
	xLocsCircle = np.concatenate((x1,x2))+xCenter
	yLocsCircle = np.concatenate((y1,y2))+yCenter
	return xLocsCircle, yLocsCircle
