#!/usr/bin/python
# -*- coding: utf-8 -*-

############# http://stackoverflow.com/questions/13801828/how-to-create-a-play-again-option-with-pygame

print 'TODO: Colours as const'

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# implemented Scott Barlow's Menu system
# http://www.pygame.org/project-MenuClass-1260-.html

import sys
import pygame

# from menu import *

import menu
import os
import image
import Config
import string
import HelperFunctions
import Game_Module

# base_path = '/home/jamie/Programming/Python/jvt02u-g51fse/Prototype'

base_path = os.path.dirname(os.path.realpath(__file__))  # 'H:\Private\G51FSE\Coursework\jvt02u-g51fse\Prototype'

sys.path.append(base_path)

STATE_MAIN_MENU = 0
STATE_LEVEL_SELECT = 1
STATE_LEVEL_HAS_BEEN_CHOSEN = 2
STATE_LEVEL_CREATOR = 3
STATE_HIGH_SCORES = 4
STATE_RULES_P_ONE = 5
STATE_RULES_P_TWO = 6
STATE_HIGH_SCORE_INPUT = 7
STATE_HIGH_SCORE_TRY_AGAIN = 8
STATE_EXIT = -1

LEVEL_ID_OFFSET = 9000
HIGH_SCORE_INPUT_OFFSET = 26000

levels_path = os.path.join(base_path, 'levels')
img_dir = os.path.join(base_path, 'images')  # "H:\Private\G51FSE\Coursework\jvt02u-g51fse\Prototype\menu\MenuClass_V1.0.3\images"

# path = os.path.join('C:\\','Users','Mart','Documents','FSE','Prototype', 'levels/')

num = 0


def get_level_list():
    level_files = dict()

    for (root, dirs, filenames) in os.walk(levels_path):
        level_list = os.listdir(levels_path)
        num = 0
        for f in filenames:
            fileDetails = os.path.splitext(f)

          # only if we have a valid lvl file

            if fileDetails[1] == '.lvl':
                level_files[num] = dict()
                settings = {}
                execfile(os.path.join(levels_path, f), settings)

                level_files[num]['settings'] = settings
                level_files[num]['fName'] = fileDetails[0]
                level_files[num]['fExt'] = fileDetails[1]

                num += 1
    return level_files


def get_level_settings(fileName):
    global levels_path

    execfile(os.path.join(levels_path, fileName + '.lvl'), settings)
    return settings


def generate_main_menu(screen):
    main_menu = menu.cMenu(
        50,
        50,
        0,
        0,
        'vertical',
        10,
        screen,
        [('Select Level', STATE_LEVEL_SELECT, None), ('Create Level',
         STATE_LEVEL_CREATOR, None), ('High Scores', STATE_HIGH_SCORES,
         None), ('Game Rules', STATE_RULES_P_ONE, None), ('Exit',
         STATE_EXIT, None)],
        )

    main_menu.set_position(330, 300)
    main_menu.set_alignment('center', 'center')
    main_menu.set_unselected_color([122, 201, 67])
    main_menu.set_selected_color([255, 255, 255])

    return main_menu


def generate_level_select(screen):

    level_files = get_level_list()

    level_select_menu = menu.cMenu(
        50,
        50,
        0,
        0,
        'vertical',
        8,
        screen,
        [],
        )

    for x in range(len(level_files)):
        level_name = str(level_files[x]['settings']['level_name']) \
            + ' (' + str(level_files[x]['settings']['difficulty']) + ')'
        level_select_menu.add_buttons([(level_name, 9000 + x + 1,
                None)])

    level_select_menu.add_buttons([('Return to Main', STATE_MAIN_MENU,
                                  None)])

    level_select_menu.set_position(50, 250)
    level_select_menu.set_alignment('top', 'left')
    level_select_menu.set_unselected_color([122, 201, 67])
    level_select_menu.set_selected_color([255, 255, 255])

    return level_select_menu


def generate_high_scores(screen):
    high_scores_menu = menu.cMenu(
        200,
        200,
        0,
        0,
        'horizontal',
        8,
        screen,
        [('Return to Main', STATE_MAIN_MENU, None)],
        )

    high_scores_menu.set_unselected_color([122, 201, 67])
    high_scores_menu.set_selected_color([255, 255, 255])
    high_scores_menu.set_position(315, 510)
    high_scores_menu.set_alignment('center', 'center')

    return high_scores_menu


def generate_game_rules(screen, screenNum):

    game_rules_menu = menu.cMenu(
        200,
        200,
        0,
        0,
        'horizontal',
        8,
        screen,
        [],
        )

    if screenNum == 1:
        game_rules_menu.add_buttons([('Next', STATE_RULES_P_TWO, None),
                                    ('Return to Main', STATE_MAIN_MENU,
                                    None)])
    elif screenNum == 2:
        game_rules_menu.add_buttons([('Previous', STATE_RULES_P_ONE,
                                    None), ('Return to Main',
                                    STATE_MAIN_MENU, None)])

    game_rules_menu.set_unselected_color([122, 201, 67])
    game_rules_menu.set_selected_color([255, 255, 255])
    game_rules_menu.set_position(200, 510)
    game_rules_menu.set_alignment('center', 'center')

    return game_rules_menu


def generate_high_score_input(screen, name):

   # high_score_input = menu.cMenu(200, 200, 0, 0, 'horizontal', 8, screen, [('Return to Main', STATE_MAIN_MENU, None)])

    high_score_input = menu.cMenu(
        50,
        50,
        30,
        30,
        'vertical',
        5,
        screen,
        [],
        )

    high_score_input.add_buttons([(name, HIGH_SCORE_INPUT_OFFSET,
                                 None)])

    high_score_input.set_position(50, 250)
    high_score_input.set_alignment('top', 'left')
    high_score_input.set_unselected_color([122, 201, 67])
    high_score_input.set_selected_color([255, 255, 255])

    return high_score_input


# def initialize_level(...):
   # print "Level", (state % 9000)

   # return high_score_input

## ---[ main ]------------------------------------------------------------------
#  This function runs the entire screen and contains the main while loop
#

def main():

    print 'TODO: get all (50,250) etc as different variables, esp the colours'

    playerName = ''

   # Initialize Pygame

    pygame.init()

   # Create a window of 800x600 pixels

    screen = pygame.display.set_mode(Config.DEFAULT_SCREEN_SIZE)

   # Set the window caption

    pygame.display.set_caption('PySnake')
    bkg = image.load_image('pysnake.jpg', img_dir)

    rules_one = image.load_image('pysnake_rules_one.jpg', img_dir)
    rules_two = image.load_image('pysnake_rules_two.jpg', img_dir)

    menu = generate_main_menu(screen)

    level_select_menu = generate_level_select(screen)
    high_scores_menu = generate_high_scores(screen)
    game_rules_one_menu = generate_game_rules(screen, 1)
    game_rules_two_menu = generate_game_rules(screen, 2)

    high_score_input_menu = generate_high_score_input(screen,
            playerName)

    state = STATE_MAIN_MENU
    prev_state = STATE_EXIT

   # rect_list is the list of pygame.Rect's that will tell pygame where to
   # update the screen (there is no point in updating the entire screen if only
   # a small portion of it changed!)

    rect_list = []

    imageIsShown = False

    EVENT_CHANGE_STATE = pygame.USEREVENT + 1

   # only allow what we will be dealing with, therefore speed up the program

    pygame.event.set_allowed(None)
    pygame.event.set_allowed([pygame.KEYDOWN, EVENT_CHANGE_STATE,
                             pygame.QUIT])

    print 'BUG: in Game rules, press ESC, go back, no image'

    ourFont = pygame.font.SysFont('Arial', 24)

   # The main while loop

    while True:

      # Check if the state has changed, if it has, then post a user event to
      # the queue to force the menu to be shown at least once

      # high_score_input_menu = generate_high_score_input(screen, playerName)

      # if len(playerName) > 0:
      #    print playerName

        if prev_state != state:
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE,
                              key=0))
            prev_state = state
            screen.blit(bkg, (0, 0))
            pygame.display.flip()

      # Get the next event

        e = pygame.event.wait()

      # Update the menu, based on which "state" we are in - When using the menu
      # in a more complex program, definitely make the states global variables
      # so that you can refer to them by a name

        if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:

               # if we press escape/q on the main menu, quit

                    if state == STATE_MAIN_MENU:
                        state = STATE_EXIT
                    else:
                        # otherwise return to the main menu
                        state = STATE_MAIN_MENU

            # don't let the user press
            # if pygame.key.name(e.key) in string.lowercase:
            #    state = ord(pygame.key.name(e.key)) + HIGH_SCORE_INPUT_OFFSET

            if state == STATE_MAIN_MENU:
                (rect_list, state) = menu.update(e, state)
            elif state == STATE_LEVEL_SELECT:

                (rect_list, state) = level_select_menu.update(e, state)
            elif state > LEVEL_ID_OFFSET and state \
                < HIGH_SCORE_INPUT_OFFSET:

                (rect_list, state) = level_select_menu.update(e, state)

               # G = Game_Module.Game()

                level_files = get_level_list()

                fName = level_files[state % 9000 - 1]['fName']

                level_settings = get_level_settings(fName)

                continueBool = False

                for val in [
                    'difficulty',
                    'level_name',
                    'initial_food_num',
                    'initial_food_super_num',
                    'initial_food_mysterious_num',
                    'initial_food_curse_num',
                    'initial_ball_num',
                    'initial_ball_killer_num',
                    'max_balls',
                    'ball_speed',
                    'ball_size',
                    'fps',
                    'background_colour',
                    ]:
                    try:
                        if isinstance(level_settings[val], str):
                            pass
                    except KeyError:
                        print 'KEY ERROR', val
                        continueBool = True

                    if continueBool:
                        continueBool = False
                        continue

                  # surround strings with double quotes, leave integers as they are

                    if isinstance(level_settings[val], str):
                        exec 'Config.' + str(val.upper()) + ' = "' \
                            + str(level_settings[val]) + '"'
                    else:
                        exec 'Config.' + str(val.upper()) + ' = ' \
                            + str(level_settings[val]) + ''

                    # print eval('Config.' + str(val.upper()))

               # end for

                Config.PAGE_TITLE = Config.PAGE_TITLE + ' ' \
                    + level_files[state % 9000 - 1]['settings'
                        ]['level_name']

               # work out the bonus based on difficulty - will only work for valid difficulties
               # try:

                exec 'Config.DIFFICULTY_BONUS = Config.DIFFICULTY_BONUS_' \
                    + Config.DIFFICULTY.upper()

                Config.BACKGROUND = pygame.Surface(screen.get_size())
                Config.BACKGROUND = Config.BACKGROUND.convert()
                Config.BACKGROUND.fill(Config.BACKGROUND_COLOUR)
                Config.screen = \
                    pygame.display.set_mode(Config.DEFAULT_SCREEN_SIZE)

            # print "COLOUR: ", Config.BACKGROUND_COLOUR

            # better way of doing it?
            # execfile('Snake.py')

                G = Game_Module.Game(None)

                running = True
                while running:
                    G.update()
                    if G.gameOver:
                        playerScore = G.gameScore
                        del G
                        running = False
                        break

                if HelperFunctions.isNewHighScore(playerScore):
                    state = STATE_HIGH_SCORE_INPUT
                else:
                    # state = STATE_EXIT
                    state = STATE_HIGH_SCORE_TRY_AGAIN

            elif state == STATE_HIGH_SCORE_INPUT:

               # state = STATE_HIGH_SCORE_TRY_AGAIN

            # #### http://www.facebook.com/l.php?u=http%3A%2F%2Fstackoverflow.com%2Fquestions%2F14111381%2Fhow-to-make-pygame-print-input-from-user&h=kAQHS8xjR

                (rect_list, state) = high_score_input_menu.update(e,
                        state)

                if False:
                    pass

                getInput = True
                showUpdates = True

                while getInput:
                    for keypress in pygame.event.get():
                        if keypress.type == pygame.KEYDOWN:
                            if keypress.unicode.isalpha():
                                playerName += keypress.unicode
                                showUpdates = True
                            elif keypress.key == pygame.K_BACKSPACE:

                                playerName = playerName[:-1]
                                showUpdates = True
                            elif keypress.key == pygame.K_RETURN:

                                getInput = False
                                continue

                    if showUpdates:

                        screen.fill((0, 0, 0))
                        text = ourFont.render(playerName, True, (255,
                                0, 0))
                        block = text.get_rect()
                        block.center = (400, 300)  # dead center
                        rect_list.append(screen.blit(text, block))

                        text = \
                            ourFont.render('Please type your name, press enter to finish, and backspace to remove characters. '
                                , True, (255, 255, 255))
                        block = text.get_rect()
                        block.center = (400, 250)

                  # block.center[1] -= 100

                        rect_list.append(screen.blit(text, block))

                        pygame.display.update(rect_list)
                        showUpdates = False

            # end while

                print 'Final name', playerName

                HelperFunctions.appendHighScore(playerScore, playerName)

                state = STATE_HIGH_SCORE_TRY_AGAIN

            elif state == STATE_LEVEL_CREATOR:
                screen.fill((0, 0, 0))

                rect_list.append(HelperFunctions.makeTextRect(
                    'Please follow the instructions in the console.',
                    (255, 255, 255),
                    (400, 250),
                    screen,
                    ourFont,
                    True,
                    ))

                rect_list.append(HelperFunctions.makeTextRect(
                    'Once complete, please restart the menu. ',
                    (255, 255, 255),
                    (400, 300),
                    screen,
                    ourFont,
                    True,
                    ))

                pygame.display.update(rect_list)

                os.system(sys.executable + ' level_creator.py')

                state = STATE_EXIT
            elif state == STATE_HIGH_SCORES:

                # print 'High Scores'

                (rect_list, state) = high_scores_menu.update(e, state)

                highScoresList = HelperFunctions.getHighScores()

                yOffset = 220

                screen.fill((0, 0, 0))

                rect_list.append(HelperFunctions.makeTextRect('Rank',
                                 GREEN, (100, yOffset), screen,
                                 ourFont))
                rect_list.append(HelperFunctions.makeTextRect('Name',
                                 GREEN, (200, yOffset), screen,
                                 ourFont))
                rect_list.append(HelperFunctions.makeTextRect('Score',
                                 GREEN, (450, yOffset), screen,
                                 ourFont))

                yOffset += 30

                colour = dict()
                colour['normal'] = (255, 255, 255)
                colour['bronze'] = (128, 64, 0)
                colour['silver'] = (192, 192, 192)
                colour['gold'] = (232, 232, 0)

                for (idx, tup) in enumerate(highScoresList):

                    # print idx

                    if idx == 0:
                        c = colour['gold']
                    elif idx == 1:
                        c = colour['silver']
                    elif idx == 2:
                        c = colour['bronze']
                    else:
                        c = colour['normal']

                    rect_list.append(HelperFunctions.makeTextRect(str(idx
                            + 1) + '. ', c, (100, yOffset), screen,
                            ourFont))
                    rect_list.append(HelperFunctions.makeTextRect(str(tup[1]),
                            c, (200, yOffset), screen, ourFont))
                    rect_list.append(HelperFunctions.makeTextRect(str(tup[0]),
                            c, (450, yOffset), screen, ourFont))
                    yOffset += 30

                rect_list.append(HelperFunctions.makeTextRect('Press enter or escape to return'
                                 , (255, 255, 255), (500, 300), screen,
                                 ourFont))
                rect_list.append(HelperFunctions.makeTextRect('to the main menu'
                                 , (255, 255, 255), (500, 320), screen,
                                 ourFont))

                pygame.display.update(rect_list)
            elif state == STATE_RULES_P_ONE:

               # High scores menu

                (rect_list, state) = game_rules_one_menu.update(e,
                        state)

                if not imageIsShown:

               # only show on the first page instance, otherwise will need to keep redrawing :. inefficient

                    rect_list.append(screen.blit(rules_one, (20, 250)))
                    imageIsShown = True

                if prev_state != state:

               # changed page

                    imageIsShown = False
            elif state == STATE_RULES_P_TWO:

                (rect_list, state) = game_rules_two_menu.update(e,
                        state)

                if not imageIsShown:

               # only show on the first page instance, otherwise will need to keep redrawing :. inefficient

                    rect_list.append(screen.blit(rules_two, (20, 250)))
                    imageIsShown = True

                if prev_state != state:

               # changed page

                    imageIsShown = False
            
            elif state == STATE_HIGH_SCORE_TRY_AGAIN:
               screen.fill((0, 0, 0))

               rect_list.append(HelperFunctions.makeTextRect(
                     'Your final score was ' + str(playerScore) + '. Try again next time!',
                     (255, 255, 255),
                     (400, 250),
                     screen,
                     ourFont,
                     True,
                     ))
 
               rect_list.append(HelperFunctions.makeTextRect(
                     'Press any key to exit. ',
                     (255, 255, 255),
                     (400, 300),
                     screen,
                     ourFont,
                     True,
                     ))

               pygame.display.update(rect_list)

               # state = STATE_EXIT

               # wait until we get some user input, so we know they've seen the message, then exit
               e = pygame.event.wait()

               if e.type == pygame.KEYDOWN or e.type == pygame.QUIT:
                  state = STATE_EXIT

            else:
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

if __name__ == '__main__':
    main()

# ---[ END OF FILE ]-------------------------------------------------------------
