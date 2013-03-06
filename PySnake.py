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

#### TODO: Pause?
#### TODO: Rules?
#### TODO: Nightmare mode - have to press E before eating, otherwise blows up & kills
#### TODO: Twitter Bot
#### TODO: Speed multiplier for different screen sizes
#### TODO: Collisions only on ball's radius, not on rect around it
#### TODO: Chances of positive/negative specials

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400

FPS = 100

### Count how many used so far - will then generate on the 0.3th one, +- random percent

SPECIAL_FOOD_CHANCE = 0.3

POSSIBLE_MODES = ['EASY', 'MEDIUM', 'HARD']

if len(sys.argv) > 1:

    # print string.upper(sys.argv[1])

    if string.upper(sys.argv[1]) in POSSIBLE_MODES:
        MODE = string.upper(sys.argv[1])
    elif sys.argv[1] == '?':
        print 'Usage: % [Easy, Medium, Hard] [Width] [Height]' \
            % sys.argv[0]
    else:
        print 'Invalid Mode. Can only have: ', POSSIBLE_MODES
        MODE = 'MEDIUM'
    if len(sys.argv) == 4:
        SCREEN_WIDTH = int(sys.argv[2])
        SCREEN_HEIGHT = int(sys.argv[3])
else:

    # catch default

    MODE = 'MEDIUM'

if MODE == 'EASY':

    FOOD_LENGTH_INCREASE = 20
    FOOD_EXPIRE_TIME = 10  # seconds

  # ### TODO: allow floating point speed :. can increment a lot easier

    INITIAL_LENGTH = 50
    INITIAL_SPEED = 1

    SCORE_MULTIPLIER = 0.5  # easy

    NUMBER_OF_BALLS = 1
    BALL_SPEED = 1
    BALL_SIZE = 10

    SPECIAL_FOOD_GOOD = 70  # %
elif MODE == 'MEDIUM':

    # HUNGER_TIME_TO_HIT = -1
    # HUNGER_TIME_TO_KILL = -1

    FOOD_LENGTH_INCREASE = 30
    FOOD_EXPIRE_TIME = 7  # seconds

    INITIAL_LENGTH = 60
    INITIAL_SPEED = 1

    SCORE_MULTIPLIER = 1

    NUMBER_OF_BALLS = 2
    BALL_SPEED = 2
    BALL_SIZE = 15

    SPECIAL_FOOD_GOOD = 50  # %
elif MODE == 'HARD':

    # HUNGER_TIME_TO_HIT = 20
    # HUNGER_TIME_TO_KILL = 20

    FOOD_LENGTH_INCREASE = 40

    FOOD_EXPIRE_TIME = 5  # seconds

    INITIAL_LENGTH = 70
    INITIAL_SPEED = 2

    SCORE_MULTIPLIER = 1.5

    NUMBER_OF_BALLS = 5
    BALL_SPEED = 3
    BALL_SIZE = 20

    SPECIAL_FOOD_GOOD = 30  # %

    # HUNGER_TIME_TO_HIT = 15
    # HUNGER_TIME_TO_KILL = 10

#### TODO; use argv to allow user to specify different resolution

FOOD_SPEED_INCREASE_STEP = 10
FOOD_SPEED_INCREASE_AMT = 1


###

## Round down to nearest 10, then score multiply it

def calculateScore(timeLeftForFood):
    return int(math.floor(timeLeftForFood / 10) * 10 * SCORE_MULTIPLIER)


def appendBallToList(listOfBalls):
    x = random.randint(BALL_SIZE, SCREEN_WIDTH)
    y = random.randint(BALL_SIZE, SCREEN_HEIGHT)
    ball = Ball((x, y), BALL_SIZE)
    ball.speed = 1
    ball.angle = random.uniform(0, math.pi * 2)
    listOfBalls.append(ball)


total_score = 0

## ballS

active_balls = []
BALL_COUNT = 0

SNAKE_COLOUR = (255, 255, 255)  # white
SNAKE_SPECIAL_COLOUR_GOOD = (0, 255, 0)  # green
SNAKE_SPECIAL_COLOUR_BAD = (255, 0, 0)  # red
FOOD_COLOUR = (255, 255, 255)  # white
SPECIAL_COLOUR = (128, 128, 255)  # purple-y

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

#        self.speed10
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

#            pygame.draw.circle(self.surface, self.colour,
#                               (int(math.floor(i[0])),
#                               int(math.floor(i[1]))), int(2))

            pygame.draw.rect(self.surface, self.colour, (i[0], i[1], 5,
                             5), 2)


#### TODO: ensure that food spawns in reachable place
#### TODO: food flashes when almost gone

# inherits object so we can call super()
# aka to make it a new-style class

class Food(object):

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
            return True
        else:
            return False


class SpecialFood(Food):

    def __init__(self, surface):

    # call the standard

        super(SpecialFood, self).__init__(surface)

        self.color = SPECIAL_COLOUR

        powers = ['points', 'speed', 'size', 'balls']

    # need to check MODE here

    # SPECIAL_FOOD_GOOD

    # do between 0,10
    # if in range(SPECIAL_FOOD_GOOD)
    # then good, else bad

    # i.e. 0..SPECIAL_FOOD_CHANCE

        if random.randint(0, 100) in range(SPECIAL_FOOD_GOOD):
            self.specialGood = True
        else:

            self.specialGood = False

        self.specialPower = powers[random.randint(0, 100) % 4]
        self.specialDuration = random.randint(1, 20) * FPS

    # print self.specialGood, self.specialPower

    def draw(self):
        super(SpecialFood, self).draw()

    def erase(self):
        return super(SpecialFood, self).erase()

    def check(self, x, y):
        return super(SpecialFood, self).check(x, y)

    def expire(self):
        return super(SpecialFood, self).expire()


class SpecialEffect:

    # def __init__(self):
    # self.isSet = False

    # ### TODO: use self.vals to make this less confuzzling? i.e. 2-self.speedVal = 0.8 etc?

    def __init__(
        self,
        power,
        goodBad,
        duration,
        theSnake,
        ):

        self.isSet = True
        self.power = power
        self.goodBad = goodBad
        self.duration = duration

        if self.power == 'speed':
            if self.goodBad:
                theSnake.speed *= 1.2
            else:
                theSnake.speed *= 0.8
        elif self.power == 'size':
            if self.goodBad:
                theSnake.speed *= 0.75
            else:
                theSnake.len *= 1.5
        if self.goodBad and theSnake.colour == SNAKE_SPECIAL_COLOUR_BAD \
            or not self.goodBad and theSnake.colour \
            == SNAKE_SPECIAL_COLOUR_GOOD:

# ....    if theSnake.colour == SNAKE_SPECIAL_COLOUR_BAD:
# ........theSnake.colour = SNAKE_SPECIAL_COLOUR_GOOD
# ....    else:
# ........theSnake.colour = SNAKE_SPECIAL_COLOUR_BAD

            theSnake.colour = (128, 128, 128)
        elif self.goodBad:
            theSnake.colour = SNAKE_SPECIAL_COLOUR_GOOD
        elif not self.goodBad:
            theSnake.colour = SNAKE_SPECIAL_COLOUR_BAD

    # ### TODO: no size increase when
    # ### TODO: make colour == red when affected
    # ### TODO: timer to say when special effect will wear off

    def tick(self, theSnake):
        if self.isSet:
            if self.goodBad and theSnake.colour \
                == SNAKE_SPECIAL_COLOUR_BAD or not self.goodBad \
                and theSnake.colour == SNAKE_SPECIAL_COLOUR_GOOD:

          # ....    if theSnake.colour == SNAKE_SPECIAL_COLOUR_BAD:
  # ........theSnake.colour = SNAKE_SPECIAL_COLOUR_GOOD
  # ....    else:
  # ........theSnake.colour = SNAKE_SPECIAL_COLOUR_BAD

                theSnake.colour = (128, 128, 128)
            elif self.goodBad:

                theSnake.colour = SNAKE_SPECIAL_COLOUR_GOOD
            elif not self.goodBad:
                theSnake.colour = SNAKE_SPECIAL_COLOUR_BAD

        # start to fix all we've changed

            if self.duration <= 0:
                self.isSet = False
                if self.power == 'speed':
                    if self.goodBad:
                        theSnake.speed *= 0.8
                    else:
                        theSnake.speed *= 1.2
                if self.power == 'size':
                    if self.goodBad:
                        theSnake.len *= 1.5
                    else:
                        theSnake.len *= 0.75
                theSnake.colour = SNAKE_COLOUR
            else:
                pass

        # powers = ['points', 'speed', 'size', 'balls']

        # if self.duration % 10 == 0:
          #  print "INSIDE", self.duration, "left for", self.power

        return theSnake


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
    appendBallToList(active_balls)

# initialise our screen, clock

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Our snake.

snake = Snake(screen)

#### TODO: multiple pieces of food
#### TODO: make_labels(lists)

active_food = []

# for n in range(15):

active_food.append(Food(screen))

# for n in range(15):
  # active_food.append(SpecialFood(screen))

active_effects = []

# food = Food(screen)
# specialFood = SpecialFood(screen)

running = True

# numeaten = 0

# create the score sprite

pygame.font.init()

# scoreFont = pygame.font.SysFont("monospace", 18)

smallFont = pygame.font.SysFont('Arial', 18)
bigFont = pygame.font.SysFont('Arial', 24)

# don't render in the loop as it never changes

screen.blit(bigFont.render('Press enter to begin, q to quit.', 1, (255,
            255, 0)), (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3 - 40))

# print "[",indx,"]", food.__class__.__name__, food.time....

pygame.display.flip()

begin = False

# specialEffect = SpecialEffect()

while begin == False:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                begin = True
            elif event.key == pygame.K_q:
                sys.exit()

spawnedFood = 0

while running:

    # # Perform draws, any any other I/O

    clock.tick(FPS)
    screen.fill((0, 0, 0))

    snake.move()
    snake.draw()
    pass

    # snake = specialEffect.tick(snake)

    for effect in active_effects:
        snake = effect.tick(snake)
    for food in active_food:
        food.draw()

    # specialFood.draw()

    for ball in active_balls:
        ball.move()
        ball.bounce()
        ball.display()

    # # Score etc

    # http://stackoverflow.com/questions/10077644/python-display-text-w-font-color

    screen.blit(smallFont.render('Score: ' + str(total_score), 1, (255,
                255, 0)), (0, 0))

    topoffset = 10

    for food in active_food:
        if food.__class__.__name__ == 'Food':
            screen.blit(smallFont.render('Time left: '
                        + str(food.time), 1, (255, 255, 0)), (0,
                        topoffset))
        elif food.__class__.__name__ == 'SpecialFood':

          # screen.blit(smallFont.render('Time left (special - ' + food.specialPower + ' - ' + str(food.specialGood) + '): ' + str(food.time), 1, (255, 255, 0)), (0, topoffset))

            screen.blit(smallFont.render('Time left (special): '
                        + str(food.time), 1, SPECIAL_COLOUR), (0,
                        topoffset))
        topoffset += 10  # inc

    for effect in active_effects:

    # ### TODO:

        if effect.duration > 0:

            if effect.power == 'speed':
                if effect.goodBad:
                    screen.blit(smallFont.render(effect.power
                                + ' increase: ' + str(effect.duration),
                                1, SNAKE_SPECIAL_COLOUR_GOOD), (0,
                                topoffset))
                else:

# ........    theSnake.speed *= 1.2

                    screen.blit(smallFont.render(effect.power
                                + ' decrease: ' + str(effect.duration),
                                1, SNAKE_SPECIAL_COLOUR_BAD), (0,
                                topoffset))
            elif effect.power == 'size':

# ........    theSnake.speed *= 0.8

                if effect.goodBad:

# ........    theSnake.speed *= 0.75

                    screen.blit(smallFont.render(effect.power
                                + ' decrease: ' + str(effect.duration),
                                1, SNAKE_SPECIAL_COLOUR_GOOD), (0,
                                topoffset))
                else:
                    screen.blit(smallFont.render(effect.power
                                + ' increase: ' + str(effect.duration),
                                1, SNAKE_SPECIAL_COLOUR_BAD), (0,
                                topoffset))

# ........    theSnake.len *= 1.5

            topoffset += 10  # inc

    # end if > 0

    screen.blit(smallFont.render('Mode: ' + MODE, 1, (255, 255, 0)),
                (0, topoffset))  # grab last value

    # # Check current state of the game

    if snake.crashed:
        running = False
    elif snake.x <= 0 or snake.x >= SCREEN_WIDTH - 1:
        running = False
    elif snake.y <= 0 or snake.y >= SCREEN_HEIGHT - 1:
        running = False

    # http://stackoverflow.com/questions/522563/accessing-the-index-in-python-for-loops

    for (indx, food) in enumerate(active_food):

      # print

        if food.check(snake.x, snake.y):
            snake.eat()
            spawnedFood += 1

      # # Handle effects here

            if food.__class__.__name__ == 'Food':
                total_score += calculateScore(food.time)
            elif food.__class__.__name__ == 'SpecialFood':

          # reverse any size increases - not meant to grow when eating specials

                snake.len -= FOOD_LENGTH_INCREASE

          # powers = ['points', 'speed', 'size', 'balls']

                if food.specialPower == 'speed' or food.specialPower \
                    == 'size':

                    print 'Player got hit with', food.specialPower, \
                        'which will last for', food.specialDuration

          # ### TODO: notification(text) -> label on screen, flashes red when arrives, disappears after 5 seconds

                if food.specialPower == 'points':

                    newScore = calculateScore(food.time)

                    if food.specialGood:
                        print 'Player gained', newScore, 'points'
                        total_score += newScore
                    else:

              # ### TODO: extra penalty  ?

                        print 'Player lost', newScore, 'points'
                        total_score -= newScore
                elif food.specialPower == 'speed':

                    if food.specialGood:
                        print "Player's speed increased for", \
                            food.specialDuration, 'seconds!'
                    else:
                        print "Player's speed decreased for", \
                            food.specialDuration, 'seconds!'

                    active_effects.append(SpecialEffect(food.specialPower,
                            food.specialGood, food.specialDuration,
                            snake))
                elif food.specialPower == 'size':

          # active_food[indx].doSpecial = True
          # print indx, food.doSpecial
          # food.specialPowerFunct(screen)

                    if food.specialGood:
                        print "Player's size decreased for", \
                            food.specialDuration, 'seconds!'
                    else:
                        print "Player's size increased for", \
                            food.specialDuration, 'seconds!'

                    active_effects.append(SpecialEffect(food.specialPower,
                            food.specialGood, food.specialDuration,
                            snake))
                elif food.specialPower == 'balls':
                    if food.specialGood:
                        print 'One of the balls was removed!'
                        del active_balls[-1]  # last element
                    else:
                        print 'Another ball was added!'
                        appendBallToList(active_balls)

          # if food.__class__.__name__ == 'SpecialFood':

      # # Create a new one

            active_food[indx].erase()

            if food.__class__.__name__ == 'Food':

          # add new piece of food, and add a new ball to the screen

                active_food[indx] = Food(screen)
                appendBallToList(active_balls)
            elif food.__class__.__name__ == 'SpecialFood':
                del active_food[indx]

            #    active_food[indx] = SpecialFood(screen)

        if food.expire():
            if food.__class__.__name__ == 'Food':
                active_food[indx] = Food(screen)

            # elif food.__class__.__name__ == 'SpecialFood':
            #    active_food[indx] = SpecialFood(screen)

            spawnedFood += 1

      # else:
      # print "[",indx,"]", food.__class__.__name__, food.time....

    # only if head collides with ball,tail is OK

    for ball in active_balls:
        if ball.collide(snake.x, snake.y):
            running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            snake.key_event(event)

    if spawnedFood % 10 == SPECIAL_FOOD_CHANCE * 10:
        specialExists = False
        for food in active_food:
            if food.__class__.__name__ == 'SpecialFood':
                specialExists = True
                break
        if not specialExists:
            active_food.append(SpecialFood(screen))

    pygame.display.flip()

    # clock.tick(FPS)

# end while running

### For typography, Game Over!

if running == False:

    # here we have finished, therefore show scores etc (in the console)
    # however, this is going to be quite useless now we're showing it on screen
    # ### TODO: Top scores
    # ### TODO: inside the blit() ???
    # ### TODO: You survived for ___ seconds?
    # ### TODO: Press ___ to restart
    # ### TODO: Press p/space to pause - set FPS = 0

    GAME_OVER_WIDTH = SCREEN_WIDTH / 3
    GAME_OVER_HEIGHT = SCREEN_WIDTH / 3

    screen.blit(bigFont.render('Game Over! You lost.', 1, (255, 255,
                0)), (GAME_OVER_WIDTH, GAME_OVER_HEIGHT - 40))

    if total_score < 0:
        theStr = 'You got ' + str(total_score) + '. Like, wat. '
        theCol = (255, 0, 0)
    elif total_score == 0:
        theStr = 'You got no points at all, call yourself a gamer?'
        theCol = (255, 255, 0)
    else:
        theStr = 'You got ' + str(total_score) + ' points, not bad. '
        theCol = (255, 255, 0)

    screen.blit(bigFont.render(theStr, 1, theCol), (GAME_OVER_WIDTH,
                GAME_OVER_HEIGHT - 20))

    anyKey = bigFont.render('Press the enter key to exit.', 1, (255,
                            255, 0))
    screen.blit(anyKey, (GAME_OVER_WIDTH, GAME_OVER_HEIGHT))

    pygame.display.flip()

    # Not a nice hack - keep going until we hit the enter key

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    sys.exit()
                if event.key == pygame.K_r:
                    main()
            else:
                pass

