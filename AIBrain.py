from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

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

#load the data
X = np.load("dataset/img.npy")
Y = np.load("dataset/ang.npy")

X = X / 255

Y= (Y - 90)/90


class AIBrain(Rover):
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

    def alexNetModel(self):
        # Building 'AlexNet'
        network = input_data(shape=[None, 240, 320, 3])
        network = conv_2d(network, 96, 11, strides=4, activation='relu')
        network = max_pool_2d(network, 3, strides=2)
        network = local_response_normalization(network)
        network = conv_2d(network, 256, 5, activation='relu')
        network = max_pool_2d(network, 3, strides=2)
        network = local_response_normalization(network)
        network = conv_2d(network, 384, 3, activation='relu')
        network = conv_2d(network, 384, 3, activation='relu')
        network = conv_2d(network, 256, 3, activation='relu')
        network = max_pool_2d(network, 3, strides=2)
        network = local_response_normalization(network)
        network = fully_connected(network, 4096, activation='tanh')
        network = dropout(network, 0.5)
        network = fully_connected(network, 4096, activation='tanh')
        network = dropout(network, 0.5)
        network = fully_connected(network, 1, activation='tanh')
        network = regression(network, optimizer='momentum',
                             loss='categorical_crossentropy',
                             learning_rate=0.001)

        # Training
        model = tflearn.DNN(network, checkpoint_path='model_rtr', max_checkpoints=1, tensorboard_verbose=2)
        return model

    def fitModel(self, model):
        model.fit(X, Y, n_epoch=1000, validation_set=0.1, shuffle=True,
                  show_metric=True, batch_size=64, snapshot_step=200,
        snapshot_epoch=False, run_id='model_racetrackrover')
        return model

    def loadModel(self, model,fname):
        model.load(fname)
        return model

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