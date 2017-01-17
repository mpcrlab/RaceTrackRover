from __future__ import division, print_function, absolute_import

from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

from models.AlexNet import AlexNet
from models.NvidiaNet import NvidiaNet
from models.VGG16 import VGG16Net
from models.SimpleNet import SimpleNet

from utils.generator import generate_examples

import h5py
import datetime
import os
import pygame
from Controller import *
from Data import *
from Pygame_UI import *
from rover import Rover
import cv2
import numpy as np
import time
import sys

class AIBrain(Rover):
    def __init__(self):
        Rover.__init__(self)

        self.model = NvidiaNet()
        self.model.load_weights(os.getcwd() + '/tmp.h5')
        
        self.userInterface = Pygame_UI()
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.image = None
        self.quit = False
        self.controller = None
        self.controllerType = None
        # angle ranges from 0 to 180 where 180 = hard left, 90 = forward and 0 = hard right
        self.angle = None
        self.predictedAngle = None
        self.timeStart = time.time()
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
        self.close()

    def process_video_from_rover(self, jpegbytes, timestamp_10msec):
        window_name = 'Machine Perception and Cognitive Robotics'
        array_of_bytes = np.fromstring(jpegbytes, np.uint8)
        self.image = cv2.imdecode(array_of_bytes, flags=3)
        k = cv2.waitKey(5) & 0xFF
        return self.image

    def useKey(self, key):
        self.isReversed = False
        key = chr(key)
        if key == 'z':
            self.quit = True


    def reverse(self):
        self.treads = [-1,-1]

    def freeze(self):
        self.treads = [0,0]
        self.set_wheel_treads(0,0)

    def displayDashboard(self):
        black = (0,0,0)

        self.userInterface.display_message("Rover Battery Percentage: " + str(self.get_battery_percentage()), black, 0,0)
        self.userInterface.display_message("Controller Type: " + self.controllerType, black, 0, self.userInterface.fontSize * 1)
        self.userInterface.display_message("Predicted Angle: " + str(self.predictedAngle), black, 0, self.userInterface.fontSize*3)
        self.userInterface.display_message("Treads: " + str(self.treads), black, 0, self.userInterface.fontSize*4)
        
    def getAngle(self):
        angle = self.model.predict(self.image.reshape(-1, 240, 320, 3))
        angle = (90 * angle) + 90
        self.predictedAngle = angle[0][0]
        return self.predictedAngle

    def checkTreadStatus(self, oldTreads):
        timeCurrent = time.time()
        timer = abs(self.timeStart - timeCurrent)
        newTreads = self.treads

        # Resetting tread state
        if oldTreads != newTreads:
            self.freeze()

        # Refreshing tread state
        if oldTreads != newTreads or timer > 1:
            self.timeStart = timeCurrent
            oldTreads = newTreads
            self.set_wheel_treads(newTreads[0],newTreads[1])
        return oldTreads

    def run(self):
        while type(self.image) == type(None):
            pass
        print(self.get_battery_percentage())
        oldTreads = None
        self.controllerType = "Keyboard"
        self.controller = Keyboard()
        while not self.quit:
            self.displayDashboard()

            # Getting user input to be used if needed
            key = self.controller.getActiveKey()
            if key:
                self.useKey(key)

            # Getting predicted angle given image
            self.angle = self.getAngle()

            # Getting new treads based on angle
            self.getNewTreads()

            # Ignore this, needed for fast tread switching
            # and to not back up the tread switching queue
            oldTreads = self.checkTreadStatus(oldTreads)

            # Displaying images 
            cv2.imshow("RoverCam", self.image)
            
            predictAngleImg = self.displayWithAngle(self.predictedAngle, self.image)
            cv2.imshow("Predicted Angle", predictAngleImg)
            
            self.clock.tick(self.FPS)
            pygame.display.flip()
            self.userInterface.screen.fill((255,255,255))
        self.endSession()

    def displayWithAngle(self, angle, frame):
        imgAngle = frame.copy()
        if self.predictedAngle:
            radius = 80
            angle = angle * math.pi / 180
            y = 240 - int(math.sin(angle) * radius)
            x = int(math.cos(angle) * radius) + 160
            # cv2.circle(frame, (160, 240), radius, (250, 250, 250), -1)
            cv2.line(imgAngle, (160, 240), (x, y), (0, 0, 0), 5)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(imgAngle, str(int(angle * 180 / math.pi)), (x, y), font, .8, (255, 0, 255), 2)
        return imgAngle