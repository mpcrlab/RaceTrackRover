import pygame
from RoverExtended import *
from Keyboard import *
from Wheel import *
from rover import Rover
import math
from time import sleep
import cv2 as cv2

pygame.init()
# Set the width and height of the screen [width,height]
size = [250, 250]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False
cnt = 0
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

rover = RoverExtended()

controllerType = raw_input('Enter K to control from Keyboard, or W to control from Wheel (K/W): ')
if controllerType == "K":
    keyboard = Keyboard()
else:
    wheel = Wheel()
# -------- Main Program Loop -----------
while not done:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if controllerType == "K":
            if event.type == pygame.KEYDOWN:
                rover.angle = keyboard.getAngle(event.key)

    if controllerType == "W":
        wheel.getAngle()
    print rover.angle
    rover.setTreads()


    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()



    # Limit to 20 frames per second
    clock.tick(1000)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

