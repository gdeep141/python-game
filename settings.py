import random
import pygame as pg
import os

#screen settings 
TITLE = "Bouncy Ball"
ICON = pg.image.load(os.path.join('img', 'smallball.png'))
WIDTH = 480
HEIGHT = 550
FPS = 70
FONT_NAME = "arial"
HS_FILE = "highscore.txt"

#player character properties
PLAYER_ACC = 0.35  #acceleration
PLAYER_FRICTION = -0.05
PLAYER_GRAVITY = 0.3
PLAYER_JUMP = 12


# PLATFORM PROPERTIES
MIDDLE_TOLERANCE = 10  # increases size of 'middle' of platform
MIDDLE_JUMP_FACTOR = 1.4
PLATFORM_HEIGHT = 20
PLATFORM_WIDTH = 80
NUMBER_OF_PLATFORMS = 14
INITIAL_PLATFORM = ((WIDTH - PLATFORM_WIDTH)/2 + MIDDLE_TOLERANCE + 1,
					HEIGHT * 3/4)

                                   
#colours
WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE   # background colour
DARK_BLUE = (0, 0, 150)
