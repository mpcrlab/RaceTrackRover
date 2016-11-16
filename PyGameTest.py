# HUD:
#
# Show Screen with current key(s) being Pressed
# Constantly show rover battery life (Refresh every minute)
#
# WASD Controls
#
# 2 Modes:
#     Implicit Movement:
#         4 Actions:
#             Left, Right, Stop, Reverse (Switches to reverse & vice versa)
#     Explicit Movement:
#         4 Actions:
#             Left, Right, Foward, Reverse


import pygame

# Screen setup
pygame.init()
screen = pygame.display.set_mode(window_size)
screen.fill(background_color)
pygame.display.set_caption('Rover Dashboard v1')
pygame.display.flip()

# Constants
window_size = (600, 400)
background_color = (150, 150, 150)

# default_font = pygame.font.get_default_font()

# title_font = pygame.font.SysFont('Helvetica', 40)

# class Helper:
#     def create_text(text, font, color, background = None):
#         text_surface = font.render(text, True, color, background)
#         return text_surface, text_surface.get_rect()
#
#
#
# def text_objects(text, font, color):
#     textSurface = font.render(text, True, color)
#     return textSurface, textSurface.get_rect()
#
# def button(surface, msg, x, y, w, h, ic, ac):
#     mouse = pygame.mouse.get_pos()
#
#     if x+w > mouse[0] > x and y+h > mouse[1] > y:
#         pygame.draw.rect(surface, ac,(x,y,w,h))
#     else:
#         pygame.draw.rect(surface, ic,(x,y,w,h))
#
#     smallText = pygame.font.Font("freesansbold.ttf", 20)
#     textSurf, textRect = text_objects(msg, smallText, (0, 0, 0))
#     textRect.center = ( (x+(w/2)), (y+(h/2)) )
#     surface.blit(textSurf, textRect)
#

def menu():
    # button(screen, "Quit", 400, 20, 50, 25, (0, 255, 0), (255, 0, 0))

    # title_surface, title_rect = Helper.create_text("Rover Dashboard v1", title_font)
    # title_rect.center = (window_size[0] / 2, window[1] / 4)
    #
    # screen.blit(text_surface, text_rect)
    # pygame.display.update()

    try:
        while True:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT: # Window close button
                    print('Quiting')
                    pygame.quit()
                    quit()
    except KeyboardInterrupt:
        print('\nQuiting')
        pygame.quit()
        quit()


    # Keep window active unless quit from keyboard or command line
    #
    # Show image to show rover search in progress
    #
    # Add button for keyboard / controller when rover is found
    #
    # If keyboard is selected show WASD and a toggle to select between implicit and explicit movement modes
    #
    # Show what key(s) are currently being pressed




if __name__ == '__main__':
    menu()
