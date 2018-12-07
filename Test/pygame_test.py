import time
import pygame
from pygame.locals import * # for event MOUSE variables
import os #for OS calls
os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(True)

black = 0,0,0
white = 255,255,255
size = width, height = 320, 240
screen = pygame.display.set_mode((320,240))
my_font = pygame.font.Font(None, 35)
screen.fill(black) # Erase the Work space
start_surface = my_font.render('PARK', True, white)
rect_start = start_surface.get_rect(center=(160,120))
screen.blit(start_surface, rect_start)
pygame.display.flip()

play = True
startTime = time.time()
while play:
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            if(rect_start.collidepoint(pos)):
                screen.fill(black) # Erase the Work space
                play = False
    time.sleep(0.2)
    if ((time.time() - startTime)>10):
        break
