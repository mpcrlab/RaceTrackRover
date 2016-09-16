import pygame
from rover import Rover
import math
from time import sleep
import cv2 as cv2

class RoverExtended(Rover):
    def __init__(self):
        Rover.__init__(self)
        self.image = None
        self.quit = False

        # angle ranges from 0 to 180 where 180 = hard left, 90 = foward,
        # and 0 = hard right
        self.angle = None

    def run(self):
        sleep(1.5)
        while not self.quit:
            self.process_video_from_rover()
        self.quit = True
        pygame.quit()

    def setTreads(self):
        if self.angle == None:
            treads = [0, 0]
        elif self.angle > 100:
            treads = [0, 1]
        elif self.angle > 80 and self.angle < 100:
            treads = [.5, .5]
        elif self.angle < 80:
            treads = [1, 0]

        self.set_wheel_treads(treads[0],treads[1])
        return treads
