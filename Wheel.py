import pygame
from RoverExtended import *
from Keyboard import *
from rover import Rover
import math
from time import sleep
import cv2 as cv2


class Wheel:
    def getAngle(self):
        # Get count of joysticks
        joystick_count = pygame.joystick.get_count()

        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            for i in range(1):
                axis = joystick.get_axis(0)
                # ranges between 0 -> 180
                angle = math.acos(axis)
                angle *= 180 / math.pi
        return angle

    # returns an array of states of the buttons 1-10
    # 1 means being pushed, 0 means inactive, etc.
    # [1, 0, 0, 0, 0, 0, 0, 0, 0, 0] means the Button1 is being pushed, the rest are not
    def getAllButtons(self):
        # Get count of joysticks
        joystick_count = pygame.joystick.get_count()

        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            # number of buttons
            num_buttons = joystick.get_numbuttons()
            buttons = []
            for i in range(num_buttons):
                button = joystick.get_button(i)
                buttons.append(button)
        return buttons

    # takes input entire buttons array
    # looks for "1"s and calls functions for that button
    def useButtons(self, buttons):
        # gear shift pulled towards you
        if buttons[0] == 1:
            # for instance here you could call a Reverse() function or perform some action()
            pass
        # gear shift pushed away from you
        elif buttons[1] == 1:
            pass
        # top left button
        elif buttons[2] == 1:
            pass
        # top right button
        elif buttons[3] == 1:
            pass
        # middle left button
        elif buttons[4] == 1:
            pass
        # middle right button
        elif buttons[5] == 1:
            pass
        # bottom left button
        elif buttons[6] == 1:
            pass
        # bottom right button
        elif buttons[7] == 1:
            pass
        # left handel under wheel
        elif buttons[8] == 1:
            pass
        # right handel under wheel
        elif buttons[9] == 1:
            pass
