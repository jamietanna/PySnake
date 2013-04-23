#! /usr/bin/python

## \file  example_simple.py
#  \brief A (very simple) example of using the menu system
#  \author Scott Barlow
#  \date 2009
#  \version 1.0.0
#
#  An example script to create a window and explore some of the features of the
#  menu class I've created.  This script just creates a very simple menu for
#  users that just want to see a plain and simply menu.  This could be made even
#  more simple, but I keep some features I deem "essential" (such as
#  non-blocking code and only updating the portion of the screen that changed).
#
#
#       Copyright 2009 Scott Barlow
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA or see <http://www.gnu.org/licenses/>.
#
#
#  Changelog
#     V1.0.0 - Initial Release
#     V1.0.1 - No change to this file
#     V1.0.2 - No change to this file
#     V1.0.3 - No change to this file
#


#-------------------------------------------------------------------------------
#---[ Imports ]-----------------------------------------------------------------
#-------------------------------------------------------------------------------
import sys, pygame
from menu import *
import os
from image import *

base_path = '/home/jamie/Programming/Python/jvt02u-g51fse/Prototype'


sys.path.append(base_path)


STATE_MAIN_MENU = 0
STATE_LEVEL_SELECT = 1
STATE_LEVEL_HAS_BEEN_CHOSEN = 2
STATE_LEVEL_CREATOR = 3
STATE_HIGH_SCORES = 4
STATE_RULES_P_ONE = 5
STATE_RULES_P_TWO = 6
STATE_EXIT = -1

global GAME_SETTINGS 
GAME_SETTINGS = dict()




# path = os.path.join('C:\\','Users','Mart','Documents','FSE','Prototype', 'levels/')
levels_path = os.path.join(base_path, 'levels') # "H:\Private\G51FSE\Coursework\jvt02u-g51fse\Prototype\levels"
level_list = os.listdir(levels_path)
num = 0
level_files = dict()

for root, dirs, filenames in os.walk(levels_path):
   for f in filenames:
      fileDetails = os.path.splitext(f)

      # only if we have a valid lvl file
      if fileDetails[1]  == '.lvl':
         level_files[num] = dict()
         settings = {}
         execfile( os.path.join(levels_path, f) , settings)

         level_files[num]['settings'] = settings
         level_files[num]['fName']    = fileDetails[0]
         level_files[num]['fExt']     = fileDetails[1]

         num += 1


def get_level_settings(fileName):
   global levels_path
   execfile(os.path.join(levels_path, fileName + '.lvl'), settings)
   return settings


img_dir = os.path.join(base_path, 'MenuClass_V1.0.3', 'images') # "H:\Private\G51FSE\Coursework\jvt02u-g51fse\Prototype\menu\MenuClass_V1.0.3\images"


## ---[ main ]------------------------------------------------------------------
#  This function runs the entire screen and contains the main while loop
#
def main():
   # Initialize Pygame
   pygame.init()
   # Create a window of 800x600 pixels
   screen = pygame.display.set_mode((800, 600))

   # Set the window caption
   pygame.display.set_caption("PySnake")
   bkg = load_image('pysnake.jpg', img_dir)
   rules_one = load_image('pysnake_rules_one.jpg', img_dir)
   rules_two = load_image('pysnake_rules_two.jpg', img_dir)
   # Create 3 diffrent menus.  One of them is only text, another one is only
   # images, and a third is -gasp- a mix of images and text buttons!  To
   # understand the input factors, see the menu file
   menu = cMenu(50, 50, 0, 0, 'vertical', 10, screen,
               [('Select Level', STATE_LEVEL_SELECT, None),
                ('Create Level',  STATE_LEVEL_CREATOR, None),
                ('High Scores', STATE_HIGH_SCORES, None),
                ('Game Rules', STATE_RULES_P_ONE, None),
                ('Exit', STATE_EXIT, None)])

   select_level_menu = cMenu(50, 50, 0, 0, 'vertical', 8, screen, [])
   high_scores_menu = cMenu(200, 200, 0, 0, 'horizontal', 8, screen, [('Return to Main', STATE_MAIN_MENU, None)])
   game_rules_one_menu = cMenu(200, 200, 0, 0, 'horizontal', 8, screen, [('Next', STATE_RULES_P_TWO, None),('Return to Main', STATE_MAIN_MENU, None)])
   game_rules_two_menu = cMenu(200, 200, 0, 0, 'horizontal', 8, screen, [('Previous', STATE_RULES_P_ONE, None),('Return to Main', STATE_MAIN_MENU, None)])

   # print "Loading Levels..."

   LEVEL_ID_OFFSET = 9000

   for x in range(len(level_files)):
      level_name = str(level_files[x]['settings']['level_name']) + " (" + str(level_files[x]['settings']['difficulty']) + ")"
      select_level_menu.add_buttons([(level_name, (9000 + x + 1), None)])

   # for level in level_list:
   #    print "-> " + str(level)
   #    select_level_menu.add_buttons([(level, 5, None)])
   # for level in level_list:
   #    print "-> " + str(level)
   #    select_level_menu.add_buttons([(level, 5, None)])
   # for level in level_list:
   #    print "-> " + str(level)
   #    select_level_menu.add_buttons([(level, 5, None)])
   # for level in level_list:
   #    print "-> " + str(level)
   #    select_level_menu.add_buttons([(level, 5, None)]) 
   # print "Levels Loaded Successfully..."

   select_level_menu.add_buttons([('Return to Main', STATE_MAIN_MENU, None)])

   
   menu.set_position(330,300)
   menu.set_alignment('center', 'center')
   menu.set_unselected_color([122,201,67])
   menu.set_selected_color([255,255,255])
   
   select_level_menu.set_position(50,250)
   select_level_menu.set_alignment('top', 'left')
   select_level_menu.set_unselected_color([122,201,67])
   select_level_menu.set_selected_color([255,255,255]) 

   high_scores_menu.set_unselected_color([122,201,67])
   high_scores_menu.set_selected_color([255,255,255])
   high_scores_menu.set_position(315,510)
   high_scores_menu.set_alignment('center', 'center')

   game_rules_one_menu.set_unselected_color([122,201,67])
   game_rules_one_menu.set_selected_color([255,255,255])
   game_rules_one_menu.set_position(200,510)
   game_rules_one_menu.set_alignment('center', 'center')

   game_rules_two_menu.set_unselected_color([122,201,67])
   game_rules_two_menu.set_selected_color([255,255,255])
   game_rules_two_menu.set_position(200,510)
   game_rules_two_menu.set_alignment('center', 'center')


   # Create the state variables (make them different so that the user event is
   # triggered at the start of the "while 1" loop so that the initial display
   # does not wait for user input)
   state = 0
   prev_state = 1

   # rect_list is the list of pygame.Rect's that will tell pygame where to
   # update the screen (there is no point in updating the entire screen if only
   # a small portion of it changed!)
   rect_list = []

   # Ignore mouse motion (greatly reduces resources when not needed)
   pygame.event.set_blocked(pygame.MOUSEMOTION)
   # The main while loop
   while 1:
      # Check if the state has changed, if it has, then post a user event to
      # the queue to force the menu to be shown at least once

      if prev_state != state:
         pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
         prev_state = state
         screen.blit(bkg, (0, 0))
         pygame.display.flip()

      # Get the next event
      e = pygame.event.wait()

      # Update the menu, based on which "state" we are in - When using the menu
      # in a more complex program, definitely make the states global variables
      # so that you can refer to them by a name
      if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
         if state == STATE_MAIN_MENU:
            rect_list, state = menu.update(e, state)

         elif state == STATE_LEVEL_SELECT:
            rect_list, state = select_level_menu.update(e, state)

         elif state > LEVEL_ID_OFFSET:
            rect_list, state = select_level_menu.update(e, state)
            level = select_level_menu.get_current_text()

            print "Level", (state % 9000)

            fName = level_files[(state % 9000) - 1]['fName']


            print get_level_settings(fName)


            # execfile('H:\Private\G51FSE\Coursework\jvt02u-g51fse\Prototype\Game.py')


            print "CHOSEN: ", level
            print "SPAWN NEW GAME"


            global GAME_SETTINGS 
            GAME_SETTINGS = get_level_settings(fName)

            for val in ['difficulty', 'level_name', 'initial_food_num', 'initial_food_super_num', 'initial_food_mysterious_num', 'initial_food_curse_num', 'initial_ball_num', 'initial_ball_killer_num', 'max_balls', 'ball_speed', 'ball_size', 'fps']:
               
               # type as they are

               if isinstance(GAME_SETTINGS[val], int):
                  exec (str(val.upper())+' = ' + str(GAME_SETTINGS[val]))
               elif isinstance(GAME_SETTINGS[val], str):
                  exec (str(val.upper())+' = "' + str(GAME_SETTINGS[val])+ '"')

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
               BACKGROUND_COLOUR = [0,0,128]#[0,0,0]
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
               PAGE_TITLE = 'PySnake - ' + level_files[(state % 9000) - 1]['fName']
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





            from Game import *
            pass # import everything

            # G = Game(GAME_SETTINGS)

            # running = True
            # while running:
            #     G.update()



            # temp, stop output
            print "STATE_LEVEL_RETRY?"
            state = STATE_LEVEL_SELECT

            # Select level menu

         elif state == STATE_LEVEL_CREATOR:
            print 'Create Level'
            print 'execute create level command line program'
            
            # temporary
            state = STATE_MAIN_MENU
         elif state == STATE_HIGH_SCORES:
            print 'High Scores'
            rect_list, state = high_scores_menu.update(e, state)
            # High scores menu
         
         elif state == STATE_RULES_P_ONE:
            rect_list, state = game_rules_one_menu.update(e, state)
            rect_list.append(screen.blit(rules_one, (20, 250)))
            print 'Page 1 of rules'
            # Game rules menu
         
         elif state == STATE_RULES_P_TWO:
            rect_list, state = game_rules_two_menu.update(e, state)
            rect_list.append(screen.blit(rules_two, (20, 250)))
            print 'Page 2 of rules'
         
         else:
            print 'Exit!'
            pygame.quit()
            sys.exit()

      # Quit if the user presses the exit button
      if e.type == pygame.QUIT:
         pygame.quit()
         sys.exit()

      # Update the screen
      pygame.display.update(rect_list)


## ---[ The python script starts here! ]----------------------------------------
# Run the script
if __name__ == "__main__":
   main()


#---[ END OF FILE ]-------------------------------------------------------------

