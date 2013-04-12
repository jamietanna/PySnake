#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import sys
import string
import random
from pygame import *
from Food_Module import *
from Snake_Module import *
from Ball_Module import *
from random import choice


global gameOver
global direction
global score
global userEscape

PAGE_TITLE = 'PySnake - Head & Body'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.font.init()
smallFont = pygame.font.SysFont('Arial', 10)

pygame.init()
DEFAULT_SCREEN_SIZE = [SCREEN_WIDTH, SCREEN_HEIGHT]

# possibleDirections = [Snake.SnakeMove.UP, Snake.SnakeMove.DOWN, Snake.SnakeMove.LEFT, Snake.SnakeMove.RIGHT]

# INITIAL_DIRECTION = choice(possibleDirections)

#### TODO bug when quickly change direction back on self i.e. from right go left and it dies, not sure how to fix

#### NOTE: random doesn't work as sometimes will spawn going the way it's body is aka die at the start - will need to safeguard
# maybe have random start position?

INITIAL_DIRECTION = Snake.SnakeMove.UP  # Random possibly?

# INITIAL_DIRECTION = Snake.SnakeMove.DOWN
# INITIAL_DIRECTION = Snake.SnakeMove.LEFT
# INITIAL_DIRECTION = Snake.SnakeMove.RIGHT

DEFAULT_UPDATE_SPEED = 60  # Speed of snake
INITIAL_FOOD_NUM = 3

updatetime = pygame.time.get_ticks() + DEFAULT_UPDATE_SPEED

# Set up Screen

screen = pygame.display.set_mode(DEFAULT_SCREEN_SIZE)
display.set_caption(PAGE_TITLE)

# Globals - Sprites

snake = Snake(None, None, None)
myBall = Ball((100,100))



# ........Snake(colour, size, position)

food = []  # define as an empty list

# Draws the snake on screen

def draw_snake():
    screen.blit(snake.head.image, snake.head.rect)  # Draw head
    for count in range(len(snake.tail.sections)):
        screen.blit(snake.tail.sections[count]['image'],
                    snake.tail.sections[count]['rect'])  # Draw all the tail sections on the screen


# Creates some new food in the food list, given the index of the element. if none, it appends one piece of food given by type
def create_food(idx=None, type='Food'):
    global food
    global snake

    # Keep food within decent boundaries

    hbound = DEFAULT_SCREEN_SIZE[0] / Food._DEFAULT_SIZE[0] - 1
    vbound = DEFAULT_SCREEN_SIZE[1] / Food._DEFAULT_SIZE[1] - 1
    (X, Y) = (None, None)

    # ### TODO check that food doesn't spawn over another piece of food

    # Make sure the food doesn't spawn over the snakes position

    while snake.occupies_position([X, Y]) == True:
        X = random.randint(0, hbound) * Food._DEFAULT_SIZE[0]
        Y = random.randint(0, vbound) * Food._DEFAULT_SIZE[1]

    if idx == None:
	# append if no index
	food.append(eval(type + '(None, None, [X, Y])'))
    else:
	# otherwise replace at correct index
        food[idx] = eval(type + '(None, None, [X, Y])')


# Draw food to screen, one piece of food at a time

def draw_food(foodBit):
    screen.blit(foodBit.image, foodBit.rect)


def exit_funct(score):
    print 'Final score was ' + str(score)
    exit()



userEscape = False  # User ends game by ESC
gameOver = False  # Game over by death
running = True
direction = None
score = 0

for n in range(INITIAL_FOOD_NUM):
    create_food()


create_food(None, 'FoodBlue')

while running:
    # print food
    screen.blit(smallFont.render('Score: ' + str(score), 1, (255,255, 255)), (40, 40))
    
    screen.fill(0)  # color screen black
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
            
            # enumerate through so we can get the index, too
            for (idx, foodBit) in enumerate(food):
		#print pygame.sprite.spritecollide(
		
		# if we've hit the food, then respawn it, and grow
                if snake.occupies_position(foodBit.rect.topleft) == True:
                    create_food(idx)

		    # If number is changed, tail will length by a greater value, seems to crash around 5
		    # ### TODO change depending on what eaten?
                    snake.lengthen_tail(1, direction)
                    score += 1
                    display.set_caption(PAGE_TITLE + ': ' + str(score))
                draw_food(foodBit)


            draw_snake()
            screen.blit(smallFont.render('Current Score: ' + str(score), 1, (255,255, 255)), (0, 0))
            screen.blit(smallFont.render('Food Time left: '+ str(foodBit.time), 1, (255, 255, 255)), (0,10))
            
            # Ball stuff
            screen.blit(myBall.image, myBall.rect)
            myBall.bounce()
            myBall.move()
            myBall.update()
            myBall.display()

            pygame.display.update()
            
            updatetime += DEFAULT_UPDATE_SPEED
            #print (str(myBall.x) + " " + str(myBall.y))

            if foodBit.expire():
                #snake.tail.fuck()
                #snake.tail.remove_tail_section(1)
                create_food(idx)


    else:
        display.set_caption(PAGE_TITLE + ': ' + str(score) + ' YOU DIED')

        # this is for when we're dead

        exit_funct(score)

    # if the user quits, then break

    if userEscape == True:
        break

# this is for when the user's escaped

exit_funct(score)
