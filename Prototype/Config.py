import pygame
import Snake_Module

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DEFAULT_SCREEN_SIZE = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(DEFAULT_SCREEN_SIZE)
BACKGROUND_COLOUR = [0,0,0]


#INITIAL_DIRECTION = Snake.SnakeMove.UP  # Random possibly?
#DEFAULT_UPDATE_SPEED = 70  # Speed of snake, lower the quicker
INITIAL_FOOD_NUM = 3
INITIAL_FOOD_BLUE_NUM = 1
INITIAL_BALL_NUM = 1
PAGE_TITLE = 'PySnake - [Level Name]'
FPS = 25

BACKGROUND = pygame.Surface(screen.get_size())
BACKGROUND = BACKGROUND.convert()
BACKGROUND.fill(BACKGROUND_COLOUR)


### INITIAL LENGTH




BALL_SPEED = 10#0.035
BALL_SIZE = 10