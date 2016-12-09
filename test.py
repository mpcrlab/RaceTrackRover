from keras.models import load_model
import h5py
import numpy as np

hdf5_file = h5py.File('output.h5', 'r')

model = load_model('model_tmp.h5')

x_dataset = hdf5_file['x_dataset']
y_dataset = hdf5_file['y_dataset']


distinct_values = {}

for x_index in range(len(x_dataset)):
    x = x_dataset[x_index]
    pred_y = model.predict(x.reshape([-1, 240, 320, 3]))
    # print pred_y
    # print y_dataset[x_index]
    #
    # print '-' * 100

    pred_y = pred_y[0][0]

    if pred_y in distinct_values:
        distinct_values[pred_y] += 1
    else:
        distinct_values[pred_y] = 0
