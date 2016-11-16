from __future__ import division, print_function, absolute_import

from keras.models import load_model
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

from AlexNet import AlexNet
from NvidiaNet import NvidiaNet

from util.generator import generate_examples

import pygame
from Controller import *
from Data import *
from Pygame_UI import *
from rover import Rover
import cv2
import numpy as np
import time
import sys
import math


class Brain(Rover):
    def __init__(self):
        Rover.__init__(self)

        self.fname = 'racetrackrover.model'
        self.model = self.alexNetModel()
        self.model = self.loadModel(self.model, self.fname)

        self.displayUI = Pygame_UI()
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.image = None
        self.quit = False
        self.controller = None
        self.controllerType = None
        # angle ranges from 0 to 180 where 180 = hard left, 90 = forward and 0 = hard right
        self.angle = None
        self.treads = [0,0]
        self.run()

    def getNewTreads(self):
        if self.angle <= 180 and self.angle >= 130:
            self.treads = [-1,1]
        elif self.angle < 130 and self.angle >= 100:
            self.treads = [-0.05, 1] #0,1
        elif self.angle < 100 and self.angle >= 80:
            self.treads = [1, 1]
        elif self.angle < 80 and self.angle >= 50:
            self.treads = [1, -0.05] #1,0
        elif self.angle < 50 and self.angle >= 0:
            self.treads = [1,-1]

    def endSession(self):
        self.set_wheel_treads(0,0)
        pygame.quit()
        cv2.destroyAllWindows()
        sys.exit()

    def process_video_from_rover(self, jpegbytes, timestamp_10msec):
        window_name = 'Machine Perception and Cognitive Robotics'
        array_of_bytes = np.fromstring(jpegbytes, np.uint8)
        self.image = cv2.imdecode(array_of_bytes, flags=3)
        k = cv2.waitKey(5) & 0xFF
        return self.image

    def useKey(self, key):
        self.isReversed = False
        key = chr(key)
        if key == 'w' or key == 'a' or key == 'd':
            self.angle = self.controller.getAngle(key)
        elif key == 'z':
            self.quit = True

    def reverse(self):
        self.treads = [-1,-1]

    def freeze(self):
        self.treads = [0,0]
        self.set_wheel_treads(0,0)

    def displayAllMessages(self):
        black = (0,0,0)
        # lightsBool = "On" if self.lightsOn else "Off"
        # motionBool = "Stopped" if self.paused else "Moving"
        # learning = "Learning" if self.isLearning else "Not Learning"

        self.displayUI.display_message("Rover Battery Percentage: " + str(self.get_battery_percentage()), black, 0,0)
        self.displayUI.display_message("Controller Type: " + self.controllerType, black, 0, self.displayUI.fontSize * 1)
        # self.displayUI.display_message("Lights: " + lightsBool, black, 0, self.displayUI.fontSize*2)
        self.displayUI.display_message("Steering Angle: " + str(self.angle), black, 0, self.displayUI.fontSize*3)
        self.displayUI.display_message("Treads: " + str(self.treads), black, 0, self.displayUI.fontSize*4)
        # self.displayUI.display_message("Motion: " + motionBool, black, 0, self.displayUI.fontSize*5)
        # self.displayUI.display_message("Reversed: " + str(self.isReversed), black, 0, self.displayUI.fontSize*6)
        # self.displayUI.display_message("Number of Frames Collected: " + str(len(self.d.angles)), black, 0, self.displayUI.fontSize*7)
        # self.displayUI.display_message("Can Collect Data (initialized at start): " + str(self.canSave), black, 0, self.displayUI.fontSize*8)
        # self.displayUI.display_message("To record data, must not be paused and not be reversed: " + learning, black, 0, self.displayUI.fontSize * 9)

    def getAngle(self):
        angle = self.model.predict([self.image])
        angle = (90 * angle) + 90  # converts tanh (-1,1) to 0-180 range??
        return angle

    def data_split(hdf5_file, training_ratio=0.7, validation_ratio=0.1):
        size = hdf5_file['x_dataset'].shape[0]
        training_size = int(training_ratio * size)
        validation_size = int(validation_ratio * size)
        validation_end = training_size + validation_size

        validation_data = validation_size != 0

        return (0, training_size), (training_size + 1, validation_end), (validation_end + 1, size), validation_data

    def input_shape(self, hdf5_file):
        shape = hdf5_file['x_dataset'].shape[1:]
        return shape

    def train_model(self, dataset, model_output, model_type, training_ratio=0.7, validation_ratio=0.1, epoch=10, batch_size=50, learning_rate=0.01):
        if dataset is None:
            raise ValueError('No dataset specified')

        hdf5_file = h5py.File(dataset, 'r')

        train, validation, test, validation_data = data_split(hdf5_file=hdf5_file, training_ratio=training_ratio, validation_ratio=validation_ratio)
        train_start, train_end = train
        validation_start, validation_end = validation
        test_start, test_end = test

        shape = input_shape(hdf5_file=hdf5_file)
        height, width, channels = shape

        if model_type in ['AlexNet', 'alexnet', 'ALEXNET', 'Alex', 'alex', 'ALEX']:
            model = AlexNet(learning_rate=learning_rate, width=width, height=height, channels=channels)
        elif model_type in ['NvidiaNet', 'nvidianet', 'NVIDIANET', 'Nvidia', 'nvidia', 'NVIDIA']:
            model = NvidiaNet(learning_rate=learning_rate, width=width, height=height, channels=channels)
        else:
            raise ValueError('Not a valid model type')
            sys.exit(0)

        if output:
            model_save_path, _ = os.path.splitext(model_save)
            model_filename = model_save_path + '-' + train_start_time
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
        callbacks = [loss_checkpoint, accuracy_checkpoint, early_stopping]

        if validation_data:
            model.fit_generator(generate_examples(hdf5_file=hdf5_file,
                                                  batch_size=batch_size,
                                                  start=train_start,
                                                  end=train_end),
                                samples_per_epoch=train_end - train_start,
                                validation_data=generate_examples(hdf5_file=hdf5_file,
                                                                  batch_size=batch_size,
                                                                  start=validation_start,
                                                                  end=validation_end),
                                nb_val_samples=validation_end - validation_start,
                                nb_epoch=epoch,
                                verbose=1,
                                callbacks=callbacks)
        else:
            model.fit_generator(generate_examples(hdf5_file=hdf5_file,
                                                  batch_size=batch_size,
                                                  start=train_start,
                                                  end=train_end),
                                samples_per_epoch=train_end - train_start,
                                nb_epoch=epoch,
                                verbose=1,
                                callbacks=callbacks)

        self.saveModel(model, model_filename + '.h5')
        # Just to be safe
        self.saveModel(model, 'tmp.h5')

        return model

    def loadModel(self, fname):
        return load_model(fname)

    def saveModel(self, model, fname):
        model.save(fname)
        return model

    def run(self):
        print(self.get_battery_percentage())
        oldTreads = None
        time.sleep(5)
        self.controllerType = "Keyboard"
        self.controller = Keyboard()
        newTime = time.time()
        while not self.quit:
            self.displayAllMessages()
            key = self.controller.getActiveKey()
            if key:
                self.useKey(key)
            self.angle = self.getAngle(self.image)
            self.getNewTreads()
            newTreads = self.treads
            # self.process_video_from_rover()
            oldTime = time.time()
            timer = abs(newTime - oldTime)
            if oldTreads != newTreads:
                self.freeze()
            if oldTreads != newTreads or timer > 1:
                newTime = time.time()
                oldTreads = newTreads
                self.set_wheel_treads(newTreads[0],newTreads[1])
            cv2.imshow("RoverCam", self.image)
            self.clock.tick(self.FPS)
            pygame.display.flip()
            self.displayUI.screen.fill((255,255,255))
        self.endSession()