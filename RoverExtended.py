import pygame
from Controller import *
from rover import Rover
import time

class RoverExtended(Rover):
    def __init__(self):
        Rover.__init__(self)
        self.image = None
        self.quit = False
        self.controller = None
        self.controllerType = None
        # angle ranges from 0 to 180 where 180 = hard left, 90 = forward and 0 = hard right
        self.angle = None
        self.treads = []
        self.run()

    def getNewTreads(self):
        if self.angle > 100 and self.angle <= 180:
            self.treads = [0, 1] #0,1
        elif self.angle > 80 and self.angle < 100:
            self.treads = [1, 1]
        elif self.angle < 80 and self.angle >= 0:
            self.treads = [1, 0] #1,0
        elif self.angle == -180:
            self.treads = [-1, -1]
        else:
            self.treads = [0, 0]
        return self.treads

    def setControls(self):
        type = raw_input('Enter K to control from Keyboard, or W to control from Wheel (K/W): ').upper()
        if type == "K":
            self.controllerType = "Keyboard"
            self.controller = Keyboard()
            print ("To move around with the rover, click the PyGame window")
            print ("W = Left, W = Forward, E = Right")
        elif type == "W":
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
        self.quit = True
        pygame.quit()

    def run(self):
        print self.get_battery_percentage()
        oldTreads = None
        self.setControls()
        newTime = time.time()
        while not self.quit:
            if self.controllerType == "Wheel":
                self.angle = self.controller.getAngle()
            else:
                key = self.controller.getActiveKey()
                if key:
                    self.angle = self.controller.getAngle(key)
            if self.controllerType == "Wheel":
                self.useButtons()
            newTreads = self.getNewTreads()
            oldTime = time.time()
            timer = abs(newTime - oldTime)
            if oldTreads != newTreads:
                self.freeze()
            if oldTreads != newTreads or timer > 1:
                newTime = time.time()
                oldTreads = newTreads
                self.set_wheel_treads(newTreads[0],newTreads[1])
        self.endSession()
