import pygame
from Controller import *
from rover import Rover
import cv2, numpy as np, pygame
from time import sleep
import time
import os
import sys

class RoverExtended(Rover):
    def __init__(self):
        Rover.__init__(self)
        self.image = None
        self.angles = []
        self.photos = []
        self.firstImage = None
        self.quit = False
        self.controller = None
        self.controllerType = None
        # angle ranges from 0 to 180 where 180 = hard left, 90 = forward and 0 = hard right
        self.angle = None
        self.treads = []
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
        elif self.angle == -180:
            self.treads = [-1, -1]
        else:
            self.treads = [0, 0]
        return self.treads

    def setControls(self):
        controls = raw_input('Enter K to control from Keyboard, or W to control from Wheel (K/W): ').upper()
        if controls == "K":
            self.controllerType = "Keyboard"
            self.controller = Keyboard()
            print ("To move around with the rover, click the PyGame window")
            print ("W = Forward, A = Left, S = Reverse, D = Right")
        elif controls == "W":
            self.controllerType = "Wheel"
            self.controller = Wheel()
        else:
            self.quit = True

    def reverse(self):
        self.angle = -180

    def freeze(self):
        self.treads = [0,0]
        self.set_wheel_treads(0,0)
    # takes input entire buttons array
    # looks for "1"s and calls functions for that button
    def useButtons(self):
        buttons = self.controller.getButtonStates()
        # left handel under wheel
        if buttons[0] == 1:
            print "Pressed button 1"
        # right handel under wheel
        elif buttons[1] == 1:
            print "Pressed button 2"
        # top left button
        elif buttons[2] == 1:
            self.endSession()
        # top right button
        elif buttons[3] == 1:
            self.freeze()
        # middle left button
        elif buttons[4] == 1:
            print "Pressed button 5"
        # middle right button
        elif buttons[5] == 1:
            print "Pressed button 6"
        # bottom left button
        elif buttons[6] == 1:
            print "Pressed button 7"
        # bottom right button
        elif buttons[7] == 1:
            print "Pressed button 8"
        # gear shift pushed towards you
        elif buttons[8] == 1:
            self.reverse()
        # gear shift pushed away from you
        elif buttons[9] == 1:
            self.reverse()

    def endSession(self):
        self.set_wheel_treads(0,0)
        self.quit = True
        pygame.quit()

    def process_video_from_rover(self, jpegbytes, timestamp_10msec):
        window_name = 'Machine Perception and Cognitive Robotics'
        array_of_bytes = np.fromstring(jpegbytes, np.uint8)
        self.image = cv2.imdecode(array_of_bytes, flags=3)
        k = cv2.waitKey(5) & 0xFF
        return self.image

    def run(self):
        print self.get_battery_percentage()
        oldTreads = None
        self.setControls()
        newTime = time.time()
        while not self.quit:
            if self.controllerType == "Wheel":
                self.angle = self.controller.getAngle()
                self.useButtons()
            else:
                key = self.controller.getActiveKey()
                if key:
                    self.angle = self.controller.getAngle(key)
                    if (self.angle == 1000):
                        self.Quit()
            cv2.imshow("RoverCam", self.image)
            self.imgEdges = self.edges(self.image)
            cv2.imshow("RoverCamEdges", self.imgEdges)
            newTreads = self.getNewTreads()
            self.angles.append(self.angle)
            self.photos.append(self.image)
            # self.process_video_from_rover()
            oldTime = time.time()
            timer = abs(newTime - oldTime)
            if oldTreads != newTreads:
                self.freeze()
            if oldTreads != newTreads or timer > 1:
                newTime = time.time()
                oldTreads = newTreads
                self.set_wheel_treads(newTreads[0],newTreads[1])
        self.endSession()

    def edges(self,image):
       imgEdges = cv2.Canny(image,50,200)
       return imgEdges

    def Quit(self):
        self.set_wheel_treads(0,0)
        self.quit = True
        self.close()
        pygame.quit()
        lenAngles = len(self.angles)
        directory =  os.getcwd()
        newpath = directory +"/Run " + str(time.time())
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        fname = newpath + "/ang"
        np.save(fname,self.angles)
        fname = newpath + "/img"
        np.save(fname,self.photos)
        sys.exit()


