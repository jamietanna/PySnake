#!/usr/bin/python
# -*- coding: utf-8 -*-

# adapted from http://lorenzod8n.wordpress.com/2008/03/01/pygame-tutorial-9-first-improvements-to-the-game/

import pygame
import random
import math
import sys
import string

################################################
#### Globals
################################################

#### TODO: How to specify mode
#### TODO: Pause?
#### TODO: Rules?

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400

FPS = 120

POSSIBLE_MODES = ['EASY', 'MEDIUM', 'HARD']

if len(sys.argv) > 1:
    # print string.upper(sys.argv[1])
    if string.upper(sys.argv[1]) in POSSIBLE_MODES:
	MODE = string.upper(sys.argv[1])
    elif sys.argv[1] == '?':
	print "Usage: % [Easy, Medium, Hard] [Width] [Height]" % sys.argv[0]
    else:
	print "Invalid Mode. Can only have: ", POSSIBLE_MODES
	MODE = 'MEDIUM'
    if len(sys.argv) == 4:
	SCREEN_WIDTH = int(sys.argv[2])
	SCREEN_HEIGHT = int(sys.argv[3])

if MODE == 'EASY':

    FOOD_SPEED_INCREASE_STEP = 10
    FOOD_SPEED_INCREASE_AMT = 1
    FOOD_LENGTH_INCREASE = 20
    FOOD_EXPIRE_TIME = 10  # seconds

  # ### TODO: allow floating point speed :. can increment a lot easier

    INITIAL_LENGTH = 50
    INITIAL_SPEED = 1

    SCORE_MULTIPLIER = 0.5  # easy

    NUMBER_OF_BALLS = 1
    BALL_SPEED = 1
elif MODE == 'MEDIUM':

    FOOD_SPEED_INCREASE_STEP = 10
    FOOD_SPEED_INCREASE_AMT = 1
    FOOD_LENGTH_INCREASE = 30
    FOOD_EXPIRE_TIME = 7  # seconds

  # ### TODO: allow floating point speed :. can increment a lot easier

    INITIAL_LENGTH = 60
    INITIAL_SPEED = 1

    SCORE_MULTIPLIER = 1

    NUMBER_OF_BALLS = 2
    BALL_SPEED = 2
elif MODE == 'HARD':

    FOOD_SPEED_INCREASE_STEP = 10
    FOOD_SPEED_INCREASE_AMT = 1
    FOOD_LENGTH_INCREASE = 40
    FOOD_EXPIRE_TIME = 5  # seconds

  # ### TODO: allow floating point speed :. can increment a lot easier

    INITIAL_LENGTH = 70
    INITIAL_SPEED = 2

    SCORE_MULTIPLIER = 1.5

    NUMBER_OF_BALLS = 5
    BALL_SPEED = 3

#### TODO; use argv to allow user to specify different resolution




###

## Round down to nearest 10, then score multiply it

def calculateScore(timeLeftForFood):
    return int(math.floor(timeLeftForFood / 10) * 10 * SCORE_MULTIPLIER)


total_score = 0

## ballS
#### TODO: Initial num balls determined by the level of difficulty

BALL_SIZE = 10
active_balls = []
BALL_COUNT = 0

SNAKE_COLOUR = (255, 255, 255)
FOOD_COLOUR = (255, 255, 255)

# SPECIAL_COLOUR =

BALL_COLOUR = (0, 0, 255)


################################################
########### Classes
################################################

class Snake:

    """ A snake. """

    num_eaten = 0

    def __init__(self, surface):
        self.surface = surface
        self.x = surface.get_width() / 2
        self.y = surface.get_height() / 2
        self.len = INITIAL_LENGTH
        self.vx = 0
        self.vy = -1
        self.body_list = [[self.x, self.y + i] for i in range(self.len)]
        self.crashed = False
        self.colour = SNAKE_COLOUR
        self.speed = INITIAL_SPEED

    def eat(self):
        self.len += FOOD_LENGTH_INCREASE
        self.num_eaten += 1
        if self.num_eaten % FOOD_SPEED_INCREASE_STEP == 0:
            self.speed += FOOD_SPEED_INCREASE_AMT

#        self.speed
#        self.speed += FOOD_SPEED_INCREASE

    def key_event(self, event):
        """ Handle key events that affect the snake. """

        if event.key == pygame.K_UP:
            if self.vy == 1:
                return
            self.vx = 0
            self.vy = -1
        elif event.key == pygame.K_DOWN:
            if self.vy == -1:
                return
            self.vx = 0
            self.vy = 1
        elif event.key == pygame.K_LEFT:
            if self.vx == 1:
                return
            self.vx = -1
            self.vy = 0
        elif event.key == pygame.K_RIGHT:
            if self.vx == -1:
                return
            self.vx = 1
            self.vy = 0

    def move(self):
        """ Move the snake. """

        self.x += self.vx * self.speed
        self.y += self.vy * self.speed

        if [self.x, self.y] in self.body_list:
            self.crashed = True

        self.body_list.insert(0, [self.x, self.y])

        if len(self.body_list) > self.len:
            self.body_list.pop()

    def draw(self):
        for i in self.body_list:
            pygame.draw.circle(self.surface, self.colour, (i[0], i[1]),
                               2)


#            pygame.draw.rect(self.surface,self.colour, (i[0],i[1], 5,),2)

#### TODO: ensure that food spawns in reachable place

class Food:

    def __init__(self, surface):
        self.surface = surface
        self.x = random.randint(0, surface.get_width() - 10)
        self.y = random.randint(0, surface.get_height() - 10)
        self.color = FOOD_COLOUR
        self.time = FOOD_EXPIRE_TIME * FPS  # otherwise clock ticks far too much and we lose it

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, 10,
                         10), 0)

    def erase(self):
        pygame.draw.rect(self.surface, (0, 0, 0), (self.x, self.y, 10,
                         10), 0)

    def check(self, x, y):
        if x < self.x or x > self.x + 10:
            return False
        elif y < self.y or y > self.y + 10:
            return False
        else:
            return True

    def expire(self):
        self.time -= 1  # decrement
        if self.time <= 0:
            return 1
        else:
            return 0


## BALL CLASS

class Ball:

    def __init__(self, (x, y), BALL_SIZE):
        self.x = x
        self.y = y
        self.size = BALL_SIZE
        self.colour = BALL_COLOUR
        self.thickness = 1
        self.speed = BALL_SPEED
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x),
                           int(self.y)), self.size, self.thickness)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def bounce(self):
        if self.x > SCREEN_WIDTH - self.size:
            self.x = 2 * (SCREEN_WIDTH - self.size) - self.x
            self.angle = -self.angle
        elif self.x < self.size:

            self.x = 2 * self.size - self.x
            self.angle = -self.angle

        if self.y > SCREEN_HEIGHT - self.size:
            self.y = 2 * (SCREEN_HEIGHT - self.size) - self.y
            self.angle = math.pi - self.angle
        elif self.y < self.size:

            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle

    def collide(self, x, y):
        if x < self.x - self.size or x > self.x + self.size:
            return False
        elif y < self.y - self.size or y > self.y + self.size:
            return False
        else:
            return True


################################################
########### Main Code
################################################

# drawing the balls

for n in range(NUMBER_OF_BALLS):

    x = random.randint(BALL_SIZE, SCREEN_WIDTH)
    y = random.randint(BALL_SIZE, SCREEN_HEIGHT)
    ball = Ball((x, y), BALL_SIZE)
    ball.speed = 1  # ### TODO: change for difficulty ?
    ball.angle = random.uniform(0, math.pi * 2)
    active_balls.append(ball)

# initialise our screen, clock

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Our snake.

snake = Snake(screen)

#### TODO: multiple pieces of food

food = Food(screen)
running = True

# numeaten = 0

# create the score sprite

pygame.font.init()

# scoreFont = pygame.font.SysFont("monospace", 18)

smallFont = pygame.font.SysFont('monospace', 18)
bigFont = pygame.font.SysFont('monospace', 24)

# don't render in the loop as it never changes
    


while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    snake.move()
    snake.draw()
    food.draw()
    for ball in active_balls:
        ball.move()
        ball.bounce()
        ball.display()

    # http://stackoverflow.com/questions/10077644/python-display-text-w-font-color

    screen.blit(smallFont.render('Score: ' + str(total_score), 1,
                             (255, 255, 0)), (0, 0))

    screen.blit(smallFont.render('Time left: ' + str(food.time), 1,
                                (255, 255, 0)), (0, 10))

    screen.blit(smallFont.render('Mode: ' + MODE, 1,
                                (255, 255, 0)), (0, 20))

    
    if snake.crashed:
        running = False
    elif snake.x <= 0 or snake.x >= SCREEN_WIDTH - 1:
        running = False
    elif snake.y <= 0 or snake.y >= SCREEN_HEIGHT - 1:
        running = False
    elif food.check(snake.x, snake.y):
        snake.eat()

        total_score += calculateScore(food.time)

        food.erase()
        food = Food(screen)

        # spawns more balls when eaten

        BALL_COUNT += 1
        if BALL_COUNT == 1:
            x = random.randint(BALL_SIZE, SCREEN_WIDTH)
            y = random.randint(BALL_SIZE, SCREEN_HEIGHT)
            ball = Ball((x, y), BALL_SIZE)
            ball.speed = 1
            ball.angle = random.uniform(0, math.pi * 2)
            active_balls.append(ball)
            BALL_COUNT = 0
    elif food.expire():

    # if we've run out of time to collect the food, then respawn it

        food = Food(screen)

    # only if head collides with ball,tail is OK

    for ball in active_balls:
        if ball.collide(snake.x, snake.y):
            running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            snake.key_event(event)

    pygame.display.flip()

    # clock.tick(FPS)

### For typography, Game Over!

if running == False:

    # here we have finished, therefore show scores etc (in the console)
    # however, this is going to be quite useless now we're showing it on screen
    # ### TODO: Scoring system based on difficulty
    # ### TODO: Top scores
    # ### TODO: inside the blit() ???
    # ### TODO: You survived for ___ seconds?
    # ### TODO: Press ___ to restart

    screen.blit(bigFont.render('Game Over! You lost.', 1, (255, 255,
                0)), (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40))

    screen.blit(bigFont.render('Your final score was: '
                + str(total_score), 1, (255, 255, 0)),
                (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20))

    anyKey = bigFont.render('Press the enter key to exit.', 1, (255,
                            255, 0))
    screen.blit(anyKey, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    pygame.display.flip()

    # Not a nice hack - keep going until we hit the enter key

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    sys.exit()
            else:
                pass
