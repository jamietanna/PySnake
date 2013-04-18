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
		if fileDetails[1]  == '.lvl':
			num += 1
			files[num] = fileDetails
			print str(num) + ") " + fileDetails[0]

#### TODO  ... == None ---> not ...


# http://en.wikibooks.org/wiki/Python_Programming/Input_and_output
levelNum = None
while not levelNum:
    try:
        levelNum = int(raw_input('Which level would you like to play? Please enter the number: '))
    except ValueError:
        print 'Invalid Number'

print 



settings = {}
execfile('levels/'+ files[levelNum][0]+'.lvl', settings)



for val in ['level_name', 'initial_food_num', 'initial_food_blue_num', 'initial_food_mysterious_num', 'initial_ball_num', 'initial_ball_killer_num', 'max_balls', 'ball_speed', 'ball_size', 'fps']:
	exec(string.upper(val) + ' = settings["'+str(val)+'"]')



### Not sure if there's an easier way of doing this unless we make a default file?

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
	INITIAL_FOOD_BLUE_NUM
except NameError:
	INITIAL_FOOD_BLUE_NUM = 1
else:
	pass

try:
	INITIAL_FOOD_MYSTERIOUS_NUM
except NameError:
	INITIAL_FOOD_MYSTERIOUS_NUM = 10
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
else:
	pass


try:
	BACKGROUND
except NameError:
	BACKGROUND = BACKGROUND.convert()
else:
	pass


try:
	BACKGROUND
except NameError:
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

