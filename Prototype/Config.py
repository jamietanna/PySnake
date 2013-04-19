#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import string
import os


# http://stackoverflow.com/questions/8225954/python-configuration-file-any-file-format-recommendation-ini-format-still-appr

# http://stackoverflow.com/questions/11801309/python-loop-over-files
num = 0
dirToSearch = 'levels/'

files = dict()

for root, dirs, filenames in os.walk(dirToSearch):
	for f in filenames:
		fileDetails = os.path.splitext(f)

		# only if we have a valid lvl file
		if fileDetails[1]  == '.lvl':
			num += 1
			files[num] = dict()
			settings = {}
			execfile('levels/'+ f , settings)

			files[num]['settings'] = settings
			files[num]['fName']    = fileDetails[0]
			files[num]['fExt']     = fileDetails[1]

			# output nice option
			print str(num) + ") " + str(settings['level_name']) + " (" + str(settings['difficulty']) + ")"

# http://en.wikibooks.org/wiki/Python_Programming/Input_and_output
levelNum = None
while not levelNum:
    try:
        levelNum = int(raw_input('Which level would you like to play? Please enter the number: '))
        if levelNum <= 0 or levelNum > num:
        	levelNum = None
        	raise ValueError
    except ValueError:
        print 'Invalid Number'

print 



# easier way to grab them all, much easier than the horrible try/except or hard coded ifs

for val in ['difficulty', 'level_name', 'initial_food_num', 'initial_food_super_num', 'initial_food_mysterious_num', 'initial_food_curse_num', 'initial_ball_num', 'initial_ball_killer_num', 'max_balls', 'ball_speed', 'ball_size', 'fps']:
	# instead of eval
	exec(string.upper(val) + ' = files['+str(levelNum)+']["settings"]["'+str(val)+'"]')



### Not sure if there's an easier way of doing this unless we make a default file?

if DIFFICULTY == 'Easy':
	DIFFICULTY_BONUS = 0.5
elif DIFFICULTY == 'Medium':
	DIFFICULTY_BONUS = 1
elif DIFFICULTY == 'Hard':
	DIFFICULTY_BONUS = 1.5




try:
	SCREEN_WIDTH
except NameError:
	SCREEN_WIDTH = 800
else:
	pass

try:
	SCREEN_HEIGHT
except NameError:
	SCREEN_HEIGHT = 600
else:
	pass

try:
	DEFAULT_SCREEN_SIZE
except NameError:
	DEFAULT_SCREEN_SIZE = [SCREEN_WIDTH, SCREEN_HEIGHT]
else:
	pass

# needed for later, but won't have been already set
screen = pygame.display.set_mode(DEFAULT_SCREEN_SIZE)



try:
	BACKGROUND_COLOUR
except NameError:
	BACKGROUND_COLOUR = [0,0,0]
else:
	pass

try:
	SNAKE_SIZE
except NameError:
	SNAKE_SIZE = 10
else:
	pass

try:
	INITIAL_FOOD_NUM
except NameError:
	INITIAL_FOOD_NUM = 2
else:
	pass

try:
	INITIAL_FOOD_SUPER_NUM
except NameError:
	INITIAL_FOOD_SUPER_NUM = 1
else:
	pass

try:
	INITIAL_FOOD_MYSTERIOUS_NUM
except NameError:
	INITIAL_FOOD_MYSTERIOUS_NUM = 10
else:
	pass


try:
	INITIAL_FOOD_CURSE_NUM
except NameError:
	INITIAL_FOOD_CURSE_NUM = 10
else:
	pass


try:
	INITIAL_BALL_NUM
except NameError:
	INITIAL_BALL_NUM = 2
else:
	pass


try:
	PAGE_TITLE
except NameError:
	PAGE_TITLE = 'PySnake - ' + LEVEL_NAME
else:
	pass


try:
	FPS
except NameError:
	FPS = 25
else:
	pass


try:
	BACKGROUND
except NameError:
	BACKGROUND = pygame.Surface(screen.get_size())
	BACKGROUND = BACKGROUND.convert()
	BACKGROUND.fill(BACKGROUND_COLOUR)
else:
	pass


try:
	INITIAL_LENGTH
except NameError:
	INITIAL_LENGTH = 5
else:
	pass


try:
	BALL_SPEED
except NameError:
	BALL_SPEED = 10#0.035
else:
	pass


try:
	BALL_SIZE
except NameError:
	BALL_SIZE = 10
else:
	pass

try:
	RANDOM_FOOD_MYSTERIOUS_CHANCE
except NameError:
	RANDOM_FOOD_MYSTERIOUS_CHANCE = 123
else:
	pass


try:
	RANDOM_FOOD_CURSE_CHANCE
except NameError:
	RANDOM_FOOD_CURSE_CHANCE = 127
else:
	pass


try:
	FOOD_CURSE_TIME_TO_WEAR_OFF
except NameError:
	FOOD_CURSE_TIME_TO_WEAR_OFF = 600
else:
	pass

