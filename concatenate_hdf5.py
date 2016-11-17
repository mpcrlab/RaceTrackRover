import argparse
import h5py
import progressbar
import numpy as np

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Rover HDF5 Concatenator')
	parser.add_argument('--first_dataset', type=str, default='training_data/output.h5')
	parser.add_argument('--second_dataset', type=str, default='training_data/output.h5')
	parser.add_argument('--output', type=str, default='output.h5')

	args = parser.parse_args()

	first_dataset = args.first_dataset
	second_dataset = args.second_dataset
	output = args.output

	first_hdf5_file = h5py.File(first_dataset, 'r')
	first_xs = first_hdf5_file['x_dataset']
	first_ys = first_hdf5_file['y_dataset']
	first_dataset_length = len(first_xs)

	second_hdf5_file = h5py.File(second_dataset, 'r')
	second_xs = second_hdf5_file['x_dataset']
	second_ys = second_hdf5_file['y_dataset']
	second_dataset_length = len(second_xs)

	output_filename = output

	output_file = h5py.File(output_filename, 'a')
	output_dataset_length = first_dataset_length + second_dataset_length
	output_xs = output_file.create_dataset('x_dataset', (output_dataset_length, 240, 320, 3), dtype='int8')
	output_ys = output_file.create_dataset('y_dataset', (output_dataset_length, 1), dtype='int8')


	progress = progressbar.ProgressBar(maxval=output_dataset_length)
	progress.start()

	instance = 0

	for i in range(first_dataset_length):
	    output_xs[instance] = first_xs[i]
	    output_ys[instance] = first_ys[i]
	    instance += 1
	    progress.update(instance)

	for j in range(second_dataset_length):
	    output_xs[instance] = second_xs[j]
	    output_ys[instance] = second_ys[j]
	    instance += 1
	    progress.update(instance)

	progress.finish()
