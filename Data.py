import time
import numpy as np
import h5py
import progressbar
import datetime

class Data():
    def __init__(self):
        self.angles = []
        self.images = []

    def load(self):
        pass

    def save(self, fname):
        self.images = np.array(self.images, dtype='uint8')

        self.angles = np.array(self.angles, dtype='float16')
        self.angles = (self.angles - 90) / 90

        save_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        dset_name = "Run-" + save_time

        dataset_length = self.angles.shape[0]
        output_dataset_length = dataset_length * 2

        print ("Saving dataset as", dset_name)

        f = h5py.File(fname, 'a')

        dt = np.dtype([('image', np.uint8, (240, 320, 3)), ('angle', np.float16)])
        output = f.create_dataset(dset_name, (output_dataset_length, ), dtype=dt)

        progress = progressbar.ProgressBar(maxval=output_dataset_length)
        progress.start()

        instance = 0

        for i in range(dataset_length):
            output[instance] = (self.images[i], self.angles[i])
            instance += 1
            progress.update(instance)

        for j in range(dataset_length):
            output[instance] = (np.fliplr(self.images[j]), self.angles[j] * -1)
            instance += 1
            progress.update(instance)

        progress.finish()