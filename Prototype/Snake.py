#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame import *
from Food_Module import *
from Snake_Module import *
from Ball_Module import *
from Config import *
import random
from random import choice

global gameOver
global direction
global score
global userEscape


def make_food(type='FoodNormal', colour=None, size=None, effect=None):
    global snake

    # Keep food within decent boundaries
    # Use eval in case we're spawning a different type of food

    hbound = DEFAULT_SCREEN_SIZE[0] / eval(type
            + '._DEFAULT_SIZE[0] - 1')
    vbound = DEFAULT_SCREEN_SIZE[1] / eval(type
            + '._DEFAULT_SIZE[1] - 1')
    (X, Y) = (None, None)

    # ### TODO check that food doesn't spawn over another piece of food

    # Make sure the food doesn't spawn over the snakes position

    while snake.occupies_position([X, Y]) == True:
        X = random.randint(0, hbound) * Food._DEFAULT_SIZE[0]
        Y = random.randint(0, vbound) * Food._DEFAULT_SIZE[1]

    return eval(type + '(' + str(colour) + ', ' + str(size) + ', ' + str(effect) + ', ['+str(X)+', '+str(Y)+'])')


############ TODO: light blue = neutralFood - literally just testing
#### other types of food i.e. standard increase, bad, etc
### maybe they all have a few properties like effects? i.e. +-growth

# Draw food to screen, one piece of food at a time


def exit_funct(score):
    print 'Final score was ' + str(score)
    exit()


PAGE_TITLE = 'PySnake - Head & Body'

pygame.init()

# possibleDirections = [Snake.SnakeMove.UP, Snake.SnakeMove.DOWN, Snake.SnakeMove.LEFT, Snake.SnakeMove.RIGHT]

# INITIAL_DIRECTION = choice(possibleDirections)

#### TODO bug when quickly change direction back on self i.e. from right go left and it dies, not sure how to fix

#### NOTE: random doesn't work as sometimes will spawn going the way it's body is aka die at the start - will need to safeguard
# maybe have random start position?

INITIAL_DIRECTION = Snake.SnakeMove.UP  # Random possibly?

# INITIAL_DIRECTION = Snake.SnakeMove.DOWN
# INITIAL_DIRECTION = Snake.SnakeMove.LEFT
# INITIAL_DIRECTION = Snake.SnakeMove.RIGHT

DEFAULT_UPDATE_SPEED = 70  # Speed of snake, lower the quicker
INITIAL_FOOD_NUM = 3
INITIAL_BALL_NUM = 5

updatetime = pygame.time.get_ticks() + DEFAULT_UPDATE_SPEED

# Set up Screen


display.set_caption(PAGE_TITLE)

# Globals - Sprites

snake = Snake()

# ........Snake(colour, size, position)

foodGroup = pygame.sprite.Group()
ballGroup = pygame.sprite.Group()
# returns a Food object given from the parameters
#### TODO: option to check collisons with existing food



userEscape = False  # User ends game by ESC
gameOver = False  # Game over by death
running = True
direction = None
score = 0

## Generate our initial food items

for n in range(INITIAL_FOOD_NUM):
    foodGroup.add(make_food())

for n in range(INITIAL_BALL_NUM):
    pos = randint(0,400)
    ballGroup.add(BallStandard((pos,pos)))

killerBall=BallKiller((200,0))

    
foodGroup.add(FoodBlue([0, 0, 255], [15, 15], {'size': 2}, [10, 30]))
foodGroup.add(FoodBlue([0, 0, 255], None, None, [200, 200]))
foodGroup.add(FoodCurse(None, None, None, [100,100]))



#### Sprite collision apadted from:
#### https://github.com/ankur0890/Pygame-Examples-For-Learning/blob/master/detectSpriteCollision.py
#### http://www.devshed.com/c/a/Python/PyGame-for-Game-Development-Sprite-Groups-and-Collision-Detection/

snakeSprite = pygame.sprite.Group()

snakeSprite.add(snake.get_sections())
snakeSections = snake.get_sections()
snakeHead = snake.get_head()

while running:

    #for snakeSegment in snakeSections:

    collisions = pygame.sprite.spritecollide(snakeHead,
                foodGroup, True)
    if collisions:

            # #### TODO reactToCollision(properties, snake, foodGroup)

            # get the collided food item, then recreate it in a new random, position

        properties = collisions[0].get_properties()
        foodGroup.add(make_food(properties['type'], properties['colour'], properties['size'], properties['effect']))

        if properties['effect']['curse'] == True:
            snake.curse_tail(True)

                # ##################

                ## snake.adjust_tail_size()

        snake.adjust_tail_size(properties['effect']['size'], direction)

            #snake.lengthen_tail(1, direction)
        score += properties['effect']['score']
        display.set_caption(PAGE_TITLE + ': ' + str(score))

            # update these so we can then redraw them later - only update once we've got a larger snake, otherwise we're wasting CPU!

        snakeSprite = pygame.sprite.Group()
        snakeSprite.add(snake.get_sections())
        snakeSections = snake.get_sections()
 
    collisions = pygame.sprite.spritecollide(snakeHead,ballGroup, False)
    #if collisions:
        #print "COLLISION"

    #for ball in ballGroup:
        #if pygame.sprite.spritecollide(ball,ballGroup, False):
           #print "BOUNCE"
  
    collisions = pygame.sprite.spritecollide(killerBall,ballGroup, False)
    for ball in collisions:
        ball.collision(killerBall)
            
        # the final boolean indicates whether to remove any collided objects from the Group, namely tmp - which we don't want generally

    ##### TODO: BALLS

    
    screen.blit(killerBall.image, killerBall.rect)
    killerBall.bounce()
    killerBall.move()
    killerBall.update()
    killerBall.display()
    
    for ball in ballGroup:
        ball.bounce()
        ball.move()
        ball.update()
        ball.display()



    for (idx, foodBit) in enumerate(foodGroup):
        if foodBit.expire():
            properties = foodBit.get_properties()
            foodGroup.add(make_food(properties['type'], properties['colour'], properties['size'], properties['effect']))
            foodGroup.remove(foodBit)
            

    screen.fill(BACKGROUND_COLOUR)  # color screen black
    if direction == None:
        direction = INITIAL_DIRECTION

    # Validates key press

    for keyPress in event.get():
        if keyPress.type == KEYDOWN:
            if keyPress.key == K_ESCAPE or keyPress.key == K_q:
                userEscape = True
            elif keyPress.key == K_UP:
                if direction != Snake.SnakeMove.DOWN:
                    direction = Snake.SnakeMove.UP
            elif keyPress.key == K_DOWN:
                if direction != Snake.SnakeMove.UP:
                    direction = Snake.SnakeMove.DOWN
            elif keyPress.key == K_RIGHT:
                if direction != Snake.SnakeMove.LEFT:
                    direction = Snake.SnakeMove.RIGHT
            elif keyPress.key == K_LEFT:
                if direction != Snake.SnakeMove.RIGHT:
                    direction = Snake.SnakeMove.LEFT

    # Update dislay

    currenttime = pygame.time.get_ticks()
    if gameOver == False:
        if currenttime >= updatetime:
            movement = snake.move(direction, DEFAULT_SCREEN_SIZE[0],
                                  DEFAULT_SCREEN_SIZE[1])
            if movement == False:
                gameOver = True

            # much better method of drawing them all - handled by the SpriteGroup

            foodGroup.draw(screen)
            snakeSprite.draw(screen)
            ballGroup.draw(screen)
            screen.blit(killerBall.image, killerBall.rect)


            pygame.display.update()
            updatetime += DEFAULT_UPDATE_SPEED
    else:
        display.set_caption(PAGE_TITLE + ': ' + str(score) + ' YOU DIED'
                            )

        # this is for when we're dead

        exit_funct(score)

    # if the user quits, then break

    if userEscape == True:
        break

# this is for when the user's escaped

exit_funct(score)



