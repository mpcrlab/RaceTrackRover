import h5py
import numpy as np
import argparse
import progressbar

def get_onehot(angle):
	angle = (angle * 90) + 90
	if angle >= 100:
	    onehot = [0, 0, 1]
	elif angle < 100 and angle >= 80:
	    onehot = [0, 1, 0]
	elif angle < 80:
	    onehot = [1, 0, 0]
	return np.array(onehot)

def convert_to_onehot(dset_fname, onehot_fname, key_name):
	f = h5py.File(dset_fname, 'r')
	f_onehot = h5py.File(onehot_fname, 'a')
	
	dset = f[key_name]
	dataset_length = dset.shape[0]

	print "Saving as", key_name, "to", onehot_fname

	dt = np.dtype([('image', np.uint8, (240, 320, 3)), ('angle', np.int8, (3,))])
	output_onehot = f_onehot.create_dataset(key_name, (dataset_length, ), dtype=dt)

	progress = progressbar.ProgressBar(maxval=dataset_length)
	progress.start()

	instance = 0

	for i in range(dataset_length):
		image = dset[i]['image']
		angle = dset[i]['angle']
		angle_onehot = get_onehot(angle)
		output_onehot[instance] = (image, angle_onehot)
		instance += 1
		progress.update(instance)

	progress.finish()
	f.close()
	f_onehot.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Convert angles to a 3-state onehot vector')
	parser.add_argument('--original_file', type=str, default='dataset.h5')

	args = parser.parse_args()
	original_file = args.original_file

	f = h5py.File(original_file, 'r')

	keys = [x.encode('UTF8') for x in f.keys()]
	
	f.close()

	print("Total keys:", len(keys))
	for key in keys:
		convert_to_onehot(original_file, 'onehot_dataset.h5', key)