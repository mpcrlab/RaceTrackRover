import math
import pygame

class Keyboard():
    def __init__(self):
        screen = pygame.display.set_mode((640, 400))
    def getAngle(self, key):
        key = chr(key)
        if key == 'a':
            angle = 135
        elif key == 'd':
            angle = 35
        elif key == 's':
            angle = -180
        elif key == 'z':
            return 1000
        else:
            angle = 90
        return angle

    def getActiveKey(self):
        key = None
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key = event.key
        return key

class Wheel():
    def __init__(self):
        # Initialize the joysticks
        pygame.init()
        pygame.joystick.init()

    def getAngle(self):

        # NEEDED TO RUN
        for event in pygame.event.get():
            pass

        angle = None
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
    # [1, 0, 0, 0, 0, 0, 0, 0, 0, 0] means the Button 1 is being pushed, the rest are not
    def getButtonStates(self):
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