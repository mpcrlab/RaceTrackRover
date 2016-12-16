import argparse
import h5py
import numpy as np
import progressbar
import math
import cv2

def displayData(image, angle):
	radius = 80
	angle = (angle * 90) + 90
	angle = angle * math.pi / 180
	y = 240 - int(math.sin(angle) * radius)
	x = int(math.cos(angle) * radius) + 160
	cv2.line(image, (160, 240), (x, y), (0, 0, 0), 5)
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(image, str(int(angle * 180 / math.pi)), (x, y), font, .8, (255, 0, 255), 2)
	return image


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Visualizes frames and angles for a given h5 dataset')
	parser.add_argument('--file', type=str, default='dataset.h5')
	parser.add_argument('--run', type=str)

	args = parser.parse_args()
	file = args.file
	run = args.run

	f = h5py.File(file, 'r')

	keys = [x.encode('UTF8') for x in f.keys()]

	if not run:
		run = keys[0]
	print run

	dataset = f[run]

	dataset_length = dataset.shape[0]

	progress = progressbar.ProgressBar(maxval=dataset_length)
	progress.start()

	instance = 0

	for i in range(dataset_length):
		image = dataset[i]['image']
		angle = dataset[i]['angle']
		image = displayData(image, angle)
		cv2.imshow("Image", image)
		cv2.waitKey(20)
		instance += 1
		progress.update(instance)

	cv2.destroyAllWindows()
	progress.finish()
