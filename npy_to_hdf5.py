import argparse
import h5py
import progressbar
import numpy as np

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Rover Numpy File to HDF5 Converter')
	parser.add_argument('--location', type=str, default='training_data')

	args = parser.parse_args()

	location = args.location

	np_x = np.load(location + "img.npy")
	np_y = np.load(location + "ang.npy")

	dataset_length = len(np_x)

	output_file = h5py.File(location + "output.h5")

	x_dest = output_file.create_dataset('x_dataset', (dataset_length, 240, 320, 3), dtype='int8')
	y_dest = output_file.create_dataset('y_dataset', (dataset_length, 1), dtype='int8')

	progress = progressbar.ProgressBar(maxval=dataset_length * 2)

	instance = 0
	progress.start()

	for i in range(len(np_x)):
		x = np_x[i]
		x_dest[i] = x
		instance += 1
		progress.update(instance)

	for j in range(len(np_y)):
		y = np_y[j]
		y_dest[j] = y
		progress.update(instance)

	progress.finish()