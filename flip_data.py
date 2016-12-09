import argparse
import h5py
import progressbar
import numpy as np

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Rover HDF5 Concatenator')
	parser.add_argument('--dataset', type=str, default='training_data/output.h5')
	parser.add_argument('--output', type=str, default='output_flipped.h5')

	args = parser.parse_args()

	dataset = args.dataset
	output = args.output

	print '-' * 20
	print dataset
	print output

	hdf5_file = h5py.File(dataset, 'r')
	xs = hdf5_file['x_dataset']
	ys = hdf5_file['y_dataset']
	dataset_length = len(xs)

	output_file = h5py.File(output, 'a')
	output_dataset_length = dataset_length * 2
	output_xs = output_file.create_dataset('x_dataset', (output_dataset_length, 240, 320, 3), dtype='int8')
	output_ys = output_file.create_dataset('y_dataset', (output_dataset_length, 1), dtype='int8')


	progress = progressbar.ProgressBar(maxval=output_dataset_length)
	progress.start()

	instance = 0

	for i in range(dataset_length):
	    output_xs[instance] = xs[i]
	    output_ys[instance] = ys[i]
	    instance += 1
	    progress.update(instance)

	for j in range(dataset_length):
	    output_xs[instance] = np.fliplr(xs[j])
	    output_ys[instance] = ys[j] * -1
	    instance += 1
	    progress.update(instance)

	progress.finish()












# f = h5py.File('output_lowprecision.h5','a')

# images = f['x_dataset']
# angles = f['y_dataset']

# # distinct_values = {}

# # for i in range(len(angles)):
# # 	angle = angles[i][0]
# # 	if angle in distinct_values:
# # 		distinct_values[angle] += 1
# # 	else:
# # 		distinct_values[angle] = 0






# # count = 0
# # for i in range(len(angles)):
# # 	angle = angles[i][0]
# # 	if angle < 0.01 and angle > -0.01:
# # 		count+=1

# # print count






# first_image = np.fliplr(images[0])
# first_images = np.array([first_image])
# x_flipped = f.create_dataset('x_flipped',data=first_images, maxshape=(None, 240, 320, 3))

# for i in range(1, len(images)):
# 	image = images[i]
# 	new_image = np.fliplr(image)
# 	new_size = x_flipped.shape[0] + 1
# 	x_flipped.resize((new_size, 240, 320, 3))
# 	x_flipped[new_size - 1] = new_image




# first_angle = angles[0] * -1
# first_angles = np.array([first_angle])
# y_flipped = f.create_dataset('y_flipped',data=first_angles, maxshape=(None, 1))

# for i in range(1, len(angles)):
# 	new_angle = angles[i] * -1
# 	new_size = y_flipped.shape[0] + 1
# 	y_flipped.resize((new_size, 1))
# 	y_flipped[new_size - 1] = new_angle

# # print("Starting")

# # x_combined = f.create_dataset('x_combined',data=images, maxshape=(None, 240, 320, 3))
# # y_combined = f.create_dataset('y_combined',data=angles, maxshape=(None, 1))

# # print("Copy completed..")

# # x_flipped = f['x_flipped']
# # y_flipped = f['y_flipped']

# # for i in range(len(x_flipped)):
# # 	image = x_flipped[i]
# # 	new_size = x_combined.shape[0] + 1
# # 	x_combined.resize((new_size, 240, 320, 3))
# # 	x_combined[new_size - 1] = image
# # 	if i % 10000 == 0:
# # 		print("Images", i, "of 141746")

# # print("Images done")

# # for i in range(len(y_flipped)):
# # 	angle = y_flipped[i]
# # 	new_size = y_combined.shape[0] + 1
# # 	y_combined.resize((new_size, 1))
# # 	y_combined[new_size - 1] = angle
# # 	if i % 10000 == 0:
# # 		print("Angles", i, "of 141746")

# # print("Angles done")