import pygame

HIGH_SCORES_FILENAME = "highscores.pys"

# Note: All values here are defaults. 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DEFAULT_SCREEN_SIZE = [SCREEN_WIDTH, SCREEN_HEIGHT]

# needed for later, but won't have been already set
print "TODO: move screen out of here"
screen = pygame.display.set_mode(DEFAULT_SCREEN_SIZE)

## These two will definitely be overwritten
print "TODO: check that DIFF / DIFF_BON both changed"
DIFFICULTY = "Medium"

DIFFICULTY_BONUS_EASY = 0.5
DIFFICULTY_BONUS_MEDIUM = 1
DIFFICULTY_BONUS_HARD = 1.5


DIFFICULTY_BONUS = DIFFICULTY_BONUS_MEDIUM # default to medium

# PAGE_TITLE = 'PySnake - ' + level_files[(state % 9000) - 1]['fName']
PAGE_TITLE = 'Python - '

BACKGROUND_COLOUR = [0,0,0]#[0,0,0]
### will be overwritten
BACKGROUND = None

FPS = 25
SNAKE_SIZE = 10
INITIAL_LENGTH = 5

INITIAL_FOOD_NUM = 2
INITIAL_FOOD_SUPER_NUM = 1
INITIAL_FOOD_MYSTERIOUS_NUM = 0
INITIAL_FOOD_CURSE_NUM = 0
RANDOM_FOOD_MYSTERIOUS_CHANCE = 123
RANDOM_FOOD_CURSE_CHANCE = 127
FOOD_CURSE_TIME_TO_WEAR_OFF = 600

INITIAL_BALL_NUM = 2
MAX_BALLS = 5
INITIAL_BALL_KILLER_NUM = 0
BALL_SPEED = 10
BALL_SIZE = 10

