import pygame
from rover import Rover
import math
from time import sleep
import cv2 as cv2

class Keyboard():
    def getAngle(self, key):
        if key == pygame.K_q:
            angle = 135
            print "pressed"
        elif key == pygame.K_e:
            angle = 35
            print "Pressed"
        else:
            angle = 90

        return angle