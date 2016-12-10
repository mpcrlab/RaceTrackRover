import h5py
import numpy as np
import progressbar
import math
import cv2

def displayData(frame, angle):
	radius = 80
	angle = (angle * 90) + 90
	angle = angle * math.pi / 180
	y = 240 - int(math.sin(angle) * radius)
	x = int(math.cos(angle) * radius) + 160
	#cv2.circle(frame, (160, 240), radius, (250, 250, 250), -1)
	cv2.line(frame, (160, 240), (x, y), (0, 0, 0), 5)
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(frame, str(int(angle * 180 / math.pi)), (x, y), font, .8, (255, 0, 255), 2)
	return frame


if __name__ == "__main__":
	dataset = "dataset.h5"
	hdf5_file = h5py.File(dataset, 'r')
	xs = hdf5_file['x_dataset']
	ys = hdf5_file['y_dataset']
	dataset_length = len(xs)

	progress = progressbar.ProgressBar(maxval=dataset_length)
	progress.start()

	instance = 0

	for i in range(dataset_length):
	    frame = xs[i]
	    angle = ys[i]
	    visualize = displayData(frame, angle)
	    cv2.imshow("Frame", visualize)
	    cv2.waitKey(5)
	    instance += 1
	    progress.update(instance)

	cv2.destroyAllWindows()
	progress.finish()
