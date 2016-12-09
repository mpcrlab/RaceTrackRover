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

    if model_type in ['AlexNet', 'alexnet', 'ALEXNET', 'Alex', 'alex', 'ALEX', 'alex_net', 'Alex_Net', 'ALEX_NET']:
        model = AlexNet(learning_rate=learning_rate, width=width, height=height, channels=channels)
    elif model_type in ['NvidiaNet', 'nvidianet', 'NVIDIANET', 'Nvidia', 'nvidia', 'NVIDIA', 'nvidia_net', 'Nvidia_Net', 'NVIDIA_NET']:
        model = NvidiaNet(learning_rate=learning_rate, width=width, height=height, channels=channels)
    elif model_type in ['VGG16', 'vgg16', 'Vgg16', 'VGG', 'Vgg', 'vgg']:
        model = VGG16Net(learning_rate=learning_rate, width=width, height=height, channels=channels)
    elif model_type in ['SimpleNet', 'simplenet', 'SIMPLENET', 'Simplenet', 'simple', 'SIMPLE']:
        model = SimpleNet(learning_rate=learning_rate, width=width, height=height, channels=channels)    
    else:
        raise ValueError('Not a valid model type')
        sys.exit(0)

    train_start_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    if model_output:
        model_output_path, _ = os.path.splitext(model_output)
        model_filename = model_output_path + '-' + train_start_time
    else:
        dataset_path, _ = os.path.splitext(dataset)
        dataset_filename = dataset_path[dataset_path.find('/') + 1:]
        model_filename = 'models/' + dataset_filename + '-' + train_start_time

    loss_checkpoint = ModelCheckpoint(model_filename + '-val-loss-lowest.h5', monitor='val_loss', verbose=1,
                                      save_best_only=True,
                                      mode='min')
    accuracy_checkpoint = ModelCheckpoint(model_filename + '-val-acc-highest.h5', monitor='val_acc', verbose=1,
                                          save_best_only=True,
                                          mode='max')
    early_stopping = EarlyStopping(monitor='val_loss', patience=6, verbose=1, mode='min')
    reduce_learning_rate = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=5)

    callbacks = [loss_checkpoint, accuracy_checkpoint]
    if validation_data:
        train_gen = generate_examples(hdf5_file=hdf5_file,
                                              batch_size=batch_size,
                                              start=train_start,
                                              end=train_end)
        validation_gen = generate_examples(hdf5_file=hdf5_file,
                                              batch_size=batch_size,
                                              start=validation_start,
                                              end=validation_end)

        model.fit_generator(train_gen,
                                samples_per_epoch=train_end - train_start,
                                validation_data=validation_gen,
                                nb_val_samples=validation_end - validation_start,
                                nb_epoch=epoch,
                                verbose=1,
                                callbacks=callbacks)
    else:
        train_gen = generate_examples(hdf5_file=hdf5_file,
                                              batch_size=batch_size,
                                              start=train_start,
                                              end=train_end)
        model.fit_generator(train_gen,
                            samples_per_epoch=train_end - train_start,
                            nb_epoch=epoch,
                            verbose=1,
                            callbacks=callbacks)

    model.save(model_filename + '.h5')
    # Just to be safe
    model.save('tmp.h5')

    return model


def test_model(dataset, model, training_ratio=0.7, validation_ratio=0.1, batch_size=50):
    if dataset is None:
        raise ValueError('No dataset specified')

    hdf5_file = h5py.File(dataset, 'r')

    train, validation, test, validation_data = data_split(hdf5_file=hdf5_file, training_ratio=training_ratio, validation_ratio=validation_ratio)
    train_start, train_end = train
    validation_start, validation_end = validation
    test_start, test_end = test

    evaluation = model.evaluate_generator(generate_examples(hdf5_file=hdf5_file,
                                                      batch_size=batch_size,
                                                      start=test_start,
                                                      end=test_end),
                                    val_samples=test_end - test_start)


    print(evaluation)
    print(model.metrics_names)

    return model


if __name__ == "__main__":
    # model = train_model(dataset='dataset_with_flips.h5', model_output='nvidia_model.h5', model_type='nvidia', epoch=75, batch_size=32)
    model = load_model('tmp.h5')
    model = test_model(dataset='dataset_with_flips.h5', model=model, batch_size=50)
