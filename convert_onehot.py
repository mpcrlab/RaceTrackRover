import h5py
import numpy as np

f = h5py.File('output_onehot.h5','a')

images = f['x_dataset']
angles = f['y_dataset']

index_to_delete = []
onehot_list = []

for index in range(len(angles)):
	angle = angles[index][0]
	if angle <= 180 and angle >= 130:
	    index_to_delete.append(index)
	elif angle < 130 and angle >= 100:
	    onehot = [0, 0, 1]
	    onehot_list.append(onehot)
	elif angle < 100 and angle >= 80:
	    onehot = [0, 1, 0]
	    onehot_list.append(onehot)
	elif angle < 80 and angle >= 50:
	    onehot = [1, 0, 0]
	    onehot_list.append(onehot)
	elif angle < 50 and angle >= 0:
	    index_to_delete.append(index)

onehot_list = np.asarray(onehot_list)

f.__delitem__('y_dataset')
f.create_dataset('y_dataset', data=onehot_list)

for index in range(len(images)):
	reverse_index = len(images) - 1
	image = images[reverse_index]
	if index in index_to_delete:
		images.remove(image) #wont work cause its h5 object