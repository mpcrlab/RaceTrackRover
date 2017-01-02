import argparse
import h5py
import progressbar
import numpy as np
import datetime
import os

def convert_and_save(parent_loc, run_loc):
	np_x = np.load(parent_loc + "/" + run_loc + "/img.npy")
	np_y = np.load(parent_loc + "/" + run_loc + "/ang.npy")

	np_y = (np_y - 90) / 90

	dataset_length = len(np_x)
	output_dataset_length = dataset_length * 2
	dset_fname = "dset_test.h5"
	f = h5py.File(dset_fname, 'a')

	save_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
	dset_name = "Run-" + save_time

	print "Saving as", dset_name, "to", dset_fname

	dt = np.dtype([('image', np.uint8, (240, 320, 3)), ('angle', np.float16)])
	output = f.create_dataset(dset_name, (output_dataset_length, ), dtype=dt)

	progress = progressbar.ProgressBar(maxval=output_dataset_length)
	progress.start()

	instance = 0

	for i in range(dataset_length):
		output[instance] = (np_x[i], np_y[i])
		instance += 1
		progress.update(instance)

	for j in range(dataset_length):
		output[instance] = (np.fliplr(np_x[j]), np_y[j] * -1)
		instance += 1
		progress.update(instance)

	progress.finish()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Rover Numpy File to HDF5 Converter')
	parser.add_argument('--parent_loc', type=str, default='training_data')

	args = parser.parse_args()

	parent_loc = args.parent_loc
	files = os.listdir(os.getcwd() + "/" + parent_loc)
	for file in files:
		if file[:3] == "Run":
			print "Converting", file
			convert_and_save(parent_loc, file)