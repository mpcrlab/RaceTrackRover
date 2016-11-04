import pygame
from Controller import *
from Data import *
from rover import Rover
import cv2, numpy as np, pygame
from time import sleep
import time
import sys

class RoverExtended(Rover):
    def __init__(self):
        Rover.__init__(self)
        self.d = Data()
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.image = None
        self.firstImage = None
        self.count = 1
        self.quit = False
        self.controller = None
        self.controllerType = None
        self.canSave = False
        self.paused = False
        self.isReversed = False
        self.isLearning = False
        self.lightsOn = False
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

    def setControls(self):
        controls = raw_input('Enter K to control from Keyboard, or W to control from Wheel (K/W): ').upper()
        self.canSave = raw_input('Do you want this data to be recorded? (Y/N)').upper()
        if self.canSave == 'Y':
            self.canSave = True
            self.isLearning = True
        else:
            self.canSave = False
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
        if self.canSave:
            print ('Data is recording...')

    def reverse(self):
        self.treads = [-1,-1]

    def freeze(self):
        self.treads = [0,0]
        self.set_wheel_treads(0,0)

    # takes input entire buttons array
    # looks for "1"s and calls functions for that button
    def useButtons(self):
        buttons = self.controller.getButtonStates()
        if len(buttons) == 0:
            print "\n\n Plug in the wheel!"
            sys.exit()

        # only runs once per press, instead of constant hold down
        if not any(buttons):
            self.count = 0
        if any(buttons) and self.count == 0:
            self.count = 1
            # left handel under wheel
            if buttons[0] == 1:
                self.lightsOn = not self.lightsOn
                if self.lightsOn:
                    print "Lights on"
                else:
                    print "Lights off"
            # right handel under wheel
            elif buttons[1] == 1:
                print "Battery percentage:", self.get_battery_percentage()
            # top left button
            elif buttons[2] == 1:
                self.paused = not self.paused
                if self.paused:
                    print "Movement stopped"
                else:
                    print "Movement started"
            # top right button
            elif buttons[3] == 1:
                self.isLearning = not self.isLearning
                if self.isLearning:
                    print "Learning started"
                else:
                    print "Learning stopped"
            # middle left button
            elif buttons[4] == 1:
                self.eraseFrames(self.FPS)
            # middle right button
            elif buttons[5] == 1:
                self.eraseFrames(self.FPS * 60)
            # bottom left button
            elif buttons[6] == 1:
                print len(self.d.angles), "frames saved"
            # bottom right button
            elif buttons[7] == 1:
                self.quit = True
                print "Program stopping..."
            # gear shift pushed towards you
            elif buttons[8] == 1:
                self.isReversed = not self.isReversed
            # gear shift pushed away from you
            elif buttons[9] == 1:
                self.isReversed = not self.isReversed

    def endSession(self):
        self.set_wheel_treads(0,0)
        if self.canSave:
            self.d.save()
        pygame.quit()
        cv2.destroyAllWindows()

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
        elif key == 's':
            self.isReversed = True
        elif key == 'b':
            print self.get_battery_percentage()
        elif key == ' ':
            self.paused = not self.paused
        elif key == 'p':
            self.eraseFrames(self.FPS)
        elif key == 'l':
            self.pauseLearning()

    def eraseFrames(self, count):
        size = len(self.d.angles)
        if (size - count > 0):
            print "--", "Deleting 1 second of frames!"
            self.d.angles = self.d.angles[:size - count]
            self.d.photos = self.d.photos[:size - count]
        else:
            print "Couldn't delete! List has less than", count, "frames!"

    def pauseLearning(self):
        self.isLearning = not self.isLearning

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
                    self.useKey(key)
            self.getNewTreads()
            if self.isReversed:
                tr = list(self.treads)
                tr = [tr[1] * -1, tr[0] * -1]
                self.treads = tr
            if self.paused:
                self.freeze()
            if self.lightsOn:
                self.turn_the_lights_on()
            else:
                self.turn_the_lights_off()
            newTreads = self.treads
            if self.canSave and not self.isReversed and self.isLearning and not self.paused:
                self.d.angles.append(self.angle)
                self.d.photos.append(self.image)
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
            self.imgEdges = self.edges(self.image)
            cv2.imshow("RoverCamEdges", self.imgEdges)

            self.clock.tick(self.FPS)
        self.endSession()

    def edges(self,image):
       imgEdges = cv2.Canny(image,50,200)
       return imgEdges


