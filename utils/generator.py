import h5py
import numpy as np
import random
import math

def generate_examples(hdf5_file, batch_size, start, end):
    xs = hdf5_file['x_dataset']
    ys = hdf5_file['y_dataset']

    window = end - start

    batches = window / float(batch_size)

    batches = range(int(math.ceil(batches)))

    while True:

        random.shuffle(batches)

        for batch in batches:
            batch_start = batch * batch_size
            batch_end = min(end, batch_start + batch_size)

            data_x = xs[batch_start : batch_end]
            data_y = ys[batch_start : batch_end]

            np.random.shuffle(data_x)
            np.random.shuffle(data_y)

            yield (data_x, data_y)
