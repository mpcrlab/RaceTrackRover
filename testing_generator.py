from __future__ import division, print_function, absolute_import

from keras.models import load_model
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

from models.AlexNet import AlexNet
from models.NvidiaNet import NvidiaNet
from models.VGG16 import VGG16Net
from models.SimpleNet import SimpleNet

from utils.generator import generate_examples

import h5py
import datetime
import os


"""
Other than the nvidia network with is from the End to End Deep Learning for Self Driving Cars paper

Model code was sourced from https://github.com/heuritech/convnets-keras
because i'm tired and want this to work
"""


def data_split(hdf5_file, training_ratio=0.7, validation_ratio=0.1):
    size = hdf5_file['x_dataset'].shape[0]
    training_size = int(training_ratio * size)
    validation_size = int(validation_ratio * size)
    validation_end = training_size + validation_size

    validation_data = validation_size != 0

    return (0, training_size), (training_size + 1, validation_end), (validation_end + 1, size), validation_data

def input_shape(hdf5_file):
    shape = hdf5_file['x_dataset'].shape[1:]
    return shape

def train_model(dataset, model_output, model_type, training_ratio=0.7, validation_ratio=0.1, epoch=10, batch_size=50, learning_rate=0.01):
    if dataset is None:
        raise ValueError('No dataset specified')

    hdf5_file = h5py.File(dataset, 'r')

    train, validation, test, validation_data = data_split(hdf5_file=hdf5_file, training_ratio=training_ratio, validation_ratio=validation_ratio)
    train_start, train_end = train
    validation_start, validation_end = validation
    test_start, test_end = test

    shape = input_shape(hdf5_file=hdf5_file)
    height, width, channels = shape

    t = generate_examples(hdf5_file=hdf5_file,
                          batch_size=batch_size,
                          start=train_start,
                          end=train_end)

    return t


if __name__ == "__main__":
    #model = train_model(dataset='output.h5', model_output='model_output.h5', model_type='vgg', epoch=50, batch_size=16)
    t = train_model(dataset='output.h5', model_output='model_output.h5', model_type='SimpleNet', epoch=10, batch_size=16)
