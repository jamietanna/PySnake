# implemented Scott Barlow's Menu system
# http://www.pygame.org/project-MenuClass-1260-.html

import sys, pygame
# from menu import *
import menu
import os
import image
import Config
import string


# base_path = '/home/jamie/Programming/Python/jvt02u-g51fse/Prototype'
base_path = os.path.dirname(os.path.realpath(__file__)) #'H:\Private\G51FSE\Coursework\jvt02u-g51fse\Prototype'



sys.path.append(base_path)


STATE_MAIN_MENU = 0
STATE_LEVEL_SELECT = 1
STATE_LEVEL_HAS_BEEN_CHOSEN = 2
STATE_LEVEL_CREATOR = 3
STATE_HIGH_SCORES = 4
STATE_RULES_P_ONE = 5
STATE_RULES_P_TWO = 6
STATE_HIGH_SCORE_INPUT = 7
STATE_EXIT = -1

LEVEL_ID_OFFSET = 9000
HIGH_SCORE_INPUT_OFFSET = 26000




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

   print "OPENING FILE ", fileName

   execfile(os.path.join(levels_path, fileName + '.lvl'), settings)
   return settings


img_dir = os.path.join(base_path, 'images') # "H:\Private\G51FSE\Coursework\jvt02u-g51fse\Prototype\menu\MenuClass_V1.0.3\images"


def generate_main_menu(screen):
   main_menu = menu.cMenu(50, 50, 0, 0, 'vertical', 10, screen,
               [('Select Level', STATE_LEVEL_SELECT, None),
                ('Create Level',  STATE_LEVEL_CREATOR, None),
                ('High Scores', STATE_HIGH_SCORES, None),
                ('Game Rules', STATE_RULES_P_ONE, None),
                ('Exit', STATE_EXIT, None)])


   main_menu.add_buttons([('[[[SCORE INPUT]]]', HIGH_SCORE_INPUT_OFFSET, None)])



   main_menu.set_position(330,300)
   main_menu.set_alignment('center', 'center')
   main_menu.set_unselected_color([122,201,67])
   main_menu.set_selected_color([255,255,255])

   return main_menu


def generate_level_select(screen):
   level_select_menu = menu.cMenu(50, 50, 0, 0, 'vertical', 8, screen, [])
   
   for x in range(len(level_files)):
      level_name = str(level_files[x]['settings']['level_name']) + " (" + str(level_files[x]['settings']['difficulty']) + ")"
      level_select_menu.add_buttons([(level_name, (9000 + x + 1), None)])

   level_select_menu.add_buttons([('Return to Main', STATE_MAIN_MENU, None)])

   level_select_menu.set_position(50,250)
   level_select_menu.set_alignment('top', 'left')
   level_select_menu.set_unselected_color([122,201,67])
   level_select_menu.set_selected_color([255,255,255]) 

   return level_select_menu

def generate_high_scores(screen):
   high_scores_menu = menu.cMenu(200, 200, 0, 0, 'horizontal', 8, screen, [('Return to Main', STATE_MAIN_MENU, None)])

   high_scores_menu.set_unselected_color([122,201,67])
   high_scores_menu.set_selected_color([255,255,255])
   high_scores_menu.set_position(315,510)
   high_scores_menu.set_alignment('center', 'center')
   
   return high_scores_menu

def generate_game_rules(screen, screenNum):

   game_rules_menu = menu.cMenu(200, 200, 0, 0, 'horizontal', 8, screen, [])


   if screenNum == 1:
      game_rules_menu.add_buttons([('Next', STATE_RULES_P_TWO, None),('Return to Main', STATE_MAIN_MENU, None)])
   elif screenNum == 2:
      game_rules_menu.add_buttons([('Previous', STATE_RULES_P_ONE, None),('Return to Main', STATE_MAIN_MENU, None)])


   game_rules_menu.set_unselected_color([122,201,67])
   game_rules_menu.set_selected_color([255,255,255])
   game_rules_menu.set_position(200,510)
   game_rules_menu.set_alignment('center', 'center')

   return game_rules_menu



def generate_high_score_input(screen, name):
   # high_score_input = menu.cMenu(200, 200, 0, 0, 'horizontal', 8, screen, [('Return to Main', STATE_MAIN_MENU, None)])
   high_score_input = menu.cMenu(50, 50, 30, 30, 'vertical', 5, screen, [])

   high_score_input.add_buttons([(name, HIGH_SCORE_INPUT_OFFSET, None)])

   for c in string.uppercase:
      print c, HIGH_SCORE_INPUT_OFFSET + ord(c)
      high_score_input.add_buttons([(str(c), HIGH_SCORE_INPUT_OFFSET + ord(c), None)])

   high_score_input.set_position(50,250)
   high_score_input.set_alignment('top', 'left')
   high_score_input.set_unselected_color([122,201,67])
   high_score_input.set_selected_color([255,255,255]) 


   

   return high_score_input



import pickle
from random import randint
import bisect
import random








def isNewHighScore(score):

   # why add a terrible score?
   if score <= 0:
      return False

   highScoresList = getHighScores()

   # temp slice so we can say whether user's in the top 10 or not
   oldHighScores = highScoresList[:]

   length = len(oldHighScores)
   if length > 0:
      length =- 1
   
   highScoresList.append((score, '!!!TMP!!!'))
   highScoresList.sort(reverse=True)

   # just return whether the top 10 are the same elements as they are before
   # if they're the same, no dice
   # otherwise, we're in!
   return highScoresList[:10] != oldHighScores




def getHighScores():
   FILENAME = "highscores.pys"
   createNew = False
   
   try:
      highScores = open(FILENAME, "r")
      highScoresList = pickle.load(highScores)
   
   except EOFError:
      print "Blank high scores file"
      createNew = True
      
   except IOError:
      print "No file exists, creating new blank high scores file"
      createNew = True
      
   if createNew:
      highScores = open(FILENAME, "w+")
      highScoresList = []

   return highScoresList


def appendHighScore(score, name):
   
   highScoresList = getHighScores()

   # temp slice so we can say whether user's in the top 10 or not
   oldHighScores = highScoresList[:]

   length = len(oldHighScores)
   if length > 0:
      # print length
      # print "-1"
      length =- 1
   
#  highScores.close()
   
   highScoresList.append((score, name))
   highScoresList.sort(reverse=True)

   highScores = open("highscores.pys", "w")
   # only get top 10
   pickle.dump(highScoresList[:10], highScores)
   highScores.close()

   # just return whether the top 10 are the same elements as they are before
   # if they're the same, no dice
   # otherwise, we're in!
   return highScoresList[:10] != oldHighScores
   

## ---[ main ]------------------------------------------------------------------
#  This function runs the entire screen and contains the main while loop
#
def main():
   print "TODO: check expiry working - not sure?!"
   print "TODO: move these all into func, i.e. generate_select_level()"
   print "TODO: get all (50,250) etc as different variables, esp the colours"


   playerName = ''

   # Initialize Pygame
   pygame.init()
   # Create a window of 800x600 pixels
   print "TODO: grab res from Config"
   screen = pygame.display.set_mode(Config.DEFAULT_SCREEN_SIZE)

   # Set the window caption
   pygame.display.set_caption("PySnake")
   bkg = image.load_image('pysnake.jpg', img_dir)
   


   print "TODO: more programmatic way, i.e. eval/exec, need an offset"

   rules_one = image.load_image('pysnake_rules_one.jpg', img_dir)
   rules_two = image.load_image('pysnake_rules_two.jpg', img_dir)
   # Create 3 diffrent menus.  One of them is only text, another one is only
   # images, and a third is -gasp- a mix of images and text buttons!  To
   # understand the input factors, see the menu file
   menu = generate_main_menu(screen)

   level_select_menu = generate_level_select(screen)
   high_scores_menu = generate_high_scores(screen)
   game_rules_one_menu = generate_game_rules(screen, 1)
   game_rules_two_menu = generate_game_rules(screen, 2)

   high_score_input_menu = generate_high_score_input(screen, playerName)

   # print "Loading Levels..."



   

   
   
   
   
   
   


   # Create the state variables (make them different so that the user event is
   # triggered at the start of the "while 1" loop so that the initial display
   # does not wait for user input)
   state = STATE_MAIN_MENU
   prev_state = STATE_EXIT

   # rect_list is the list of pygame.Rect's that will tell pygame where to
   # update the screen (there is no point in updating the entire screen if only
   # a small portion of it changed!)
   rect_list = []


   imageIsShown = False

   EVENT_CHANGE_STATE = pygame.USEREVENT + 1

   # Ignore mouse motion (greatly reduces resources when not needed)
   
   # only allow what we want, therefore speed up the program
   pygame.event.set_allowed(None)
   pygame.event.set_allowed([pygame.KEYDOWN, EVENT_CHANGE_STATE, pygame.QUIT])


   print "BUG: in Game rules, press ESC, go back, no image"
   
   ourFont = pygame.font.SysFont('Arial', 24)

   # The main while loop
   while True:
      # Check if the state has changed, if it has, then post a user event to
      # the queue to force the menu to be shown at least once

      # high_score_input_menu = generate_high_score_input(screen, playerName)
        
      # if len(playerName) > 0:
      #    print playerName

      if prev_state != state:
         pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
         prev_state = state
         screen.blit(bkg, (0, 0))
         pygame.display.flip()

      # Get the next event
      e = pygame.event.wait()

      # if state > HIGH_SCORE_INPUT_OFFSET:
      #    if prev_state != state:
      #       print state, prev_state

      # print (state == STATE_MAIN_MENU)




      # Update the menu, based on which "state" we are in - When using the menu
      # in a more complex program, definitely make the states global variables
      # so that you can refer to them by a name
      if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:

         if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
               # if we press escape/q on the main menu, quit
               if state == STATE_MAIN_MENU:
                  state = STATE_EXIT
               # otherwise return to the main menu
               else:
                  state = STATE_MAIN_MENU

            # don't let the user press 
            # if pygame.key.name(e.key) in string.lowercase:
            #    state = ord(pygame.key.name(e.key)) + HIGH_SCORE_INPUT_OFFSET

         

         if state == STATE_MAIN_MENU:
            rect_list, state = menu.update(e, state)

         elif state == STATE_LEVEL_SELECT:
            rect_list, state = level_select_menu.update(e, state)

         elif state > LEVEL_ID_OFFSET and state < HIGH_SCORE_INPUT_OFFSET:
            rect_list, state = level_select_menu.update(e, state)
            # level = level_select_menu.get_current_text()

            # print "Level", (state % 9000)

            fName = level_files[(state % 9000) - 1]['fName']


            # print "CHOSEN: \"", level_files[(state % 9000) - 1]['settings']['level_name'], "\""
            # print "SPAWN NEW GAME"


            level_settings = get_level_settings(fName)

            # pass # import everything

            continueBool = False

            for val in ['difficulty', 'level_name', 'initial_food_num', 'initial_food_super_num', 'initial_food_mysterious_num', 'initial_food_curse_num', 'initial_ball_num', 'initial_ball_killer_num', 'max_balls', 'ball_speed', 'ball_size', 'fps','background_colour']:
               try:
                  if isinstance(level_settings[val], str):
                     pass
               except KeyError:
                  print "KEY ERROR", val
                  continueBool = True

               if continueBool:
                  continueBool = False
                  continue
            
               # print eval('Config.'+str(val.upper()))

               # type as they are
               if isinstance(level_settings[val], str):
                   exec ('Config.'+str(val.upper())+' = "' + str(level_settings[val])+ '"')
               else:
                   exec ('Config.'+str(val.upper())+' = ' + str(level_settings[val])+ '')
               
               print eval('Config.'+str(val.upper()))        
            # end for

            Config.PAGE_TITLE = Config.PAGE_TITLE + ' ' + level_files[(state % 9000) - 1]['settings']['level_name']


               # work out the bonus based on difficulty - will only work for valid difficulties
               # try:
            exec('Config.DIFFICULTY_BONUS = Config.DIFFICULTY_BONUS_'+Config.DIFFICULTY.upper())
            # except:
            #    print "ERROR"

            # if Config.DIFFICULTY == 'Easy':
            #    Config.DIFFICULTY_BONUS = 0.5
            # elif Config.DIFFICULTY == 'Medium':
            #    Config.DIFFICULTY_BONUS = 1
            # elif Config.DIFFICULTY == 'Hard':
            #    Config.DIFFICULTY_BONUS = 1.5
            # else:
            #    raise SyntaxError

            Config.BACKGROUND = pygame.Surface(screen.get_size())
            Config.BACKGROUND = Config.BACKGROUND.convert()
            Config.BACKGROUND.fill(Config.BACKGROUND_COLOUR)

            print "COLOUR: ", Config.BACKGROUND_COLOUR

            # better way of doing it?
            # execfile('Snake.py')

            import Game_Module

            G = Game_Module.Game(None)

            running = True
            while running:
                G.update()
                if G.gameOver:
                  playerScore = G.gameScore
                  del(G)
                  running = False
                  break

            if isNewHighScore(playerScore):
               state = STATE_HIGH_SCORE_INPUT
            else:
               print "TODO: Page that just says try again next time!"
               state = STATE_HIGH_SCORE_TRY_AGAIN
            
         elif state == STATE_HIGH_SCORE_INPUT:

            ##### http://www.facebook.com/l.php?u=http%3A%2F%2Fstackoverflow.com%2Fquestions%2F14111381%2Fhow-to-make-pygame-print-input-from-user&h=kAQHS8xjR


            rect_list, state = high_score_input_menu.update(e, state)

            if False:
               pass
               # print prev_state, state


               # if prev_state != state:
               #    print state % HIGH_SCORE_INPUT_OFFSET, chr(state % HIGH_SCORE_INPUT_OFFSET)

               # playerName += chr(state % HIGH_SCORE_INPUT_OFFSET)

               # state = HIGH_SCORE_INPUT_OFFSET

               # ourFont = pygame.font.SysFont('Arial', 18)

               # # text = pygame.font.Font.render(playerName, )

               # # screen.blit(ourFont.render('Press enter to begin, q to quit.', 1, (255,
               # # 255, 255)), (100,100))

               # # print rect_list            
      
               # # x = ourFont.render('Press enter to begin, q to quit.', 1, (255,
               # # 255, 255))

               # # rect_list.append(x.get_rect(center=(100,100)))






               # print len(playerName)

               # print ourFont.size(playerName)

               # print playerName


               # block = ourFont.render(playerName, True, (255, 255, 255))
               # rect = block.get_rect()
               # rect.center = screen.get_rect().center
               # # screen.blit(block, rect)
                  
               # rect_list = []

               # rect_list.append(rect)



               # # if len(playerName) == 0:
               # text = "_ _ _"
               # # else:
               # #    text = playerName   

               # screen.blit(ourFont.render(text, True, (255,0, 0)), (100,100))


               # nameLen = len(name)
               # nameText = name

               
               
               # while len(nameText) <= 3:
               #    nameText += '_'

               #playerName += chr(state % HIGH_SCORE_INPUT_OFFSET)

               #state = HIGH_SCORE_INPUT_OFFSET
               
            # getInput = True


            # while getInput:
            #    for keypress in pygame.event.get():

            #       print keypress.key 

            #       if keypress.type == pygame.KEYDOWN:
            #          if keypress.unicode.isalpha():
            #             playerName += keypress.unicode
            #          elif keypress.key == pygame.K_BACKSPACE:
            #                playerName = playerName[:-1]
            #                # playerName = ""
            #          elif keypress.key == pygame.K_RETURN:
            #             getInput = False
                  
            #       #block = font.render(name, True, (255, 255, 255))
            #       #rect = block.get_rect()
            #       #rect.center = screen.get_rect().center
            #       ourFont = pygame.font.SysFont('Arial', 18)
               
            #       text = ourFont.render(playerName, True, (255,0, 0))
            #       block = text.get_rect()
            #       block.center = screen.get_rect().center
            #       rect_list.append(screen.blit(text, block))


            #       # instr = ourFont.render('Please enter your name below, press enter to finish, and backspace to remove characters. ', True, (255,0, 0))
            #       # block = instr.get_rect()
            #       # block.center = (300,200)
            #       # rect_list.append(screen.blit(instr, block))


            #       screen.fill(0)

            #       pygame.display.update(rect_list)

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
        
                  #block = font.render(name, True, (255, 255, 255))
                  #rect = block.get_rect()
                  #rect.center = screen.get_rect().center
               if showUpdates:

                  screen.fill( (0,0,0) )
                  text = ourFont.render(playerName, True, (255,0, 0))
                  block = text.get_rect()
                  block.center = (400,300) #dead center
                  rect_list.append(screen.blit(text, block))

                  text = ourFont.render('Please type your name, press enter to finish, and backspace to remove characters. ', True, (0, 0, 255))
                  block = text.get_rect()
                  block.center = (400,250)
                  # block.center[1] -= 100
                  
                  rect_list.append(screen.blit(text, block))


                  pygame.display.update(rect_list)
                  showUpdates = False

            # end while
            print "Final name", playerName

            appendHighScore(playerScore, playerName)

            state = STATE_EXIT
            



         elif state == STATE_LEVEL_CREATOR:
            print 'Create Level'
            print 'execute create level command line program'
            
            # temporary
            state = STATE_MAIN_MENU
         elif state == STATE_HIGH_SCORES:
            print 'High Scores'
            rect_list, state = high_scores_menu.update(e, state)

            screen.fill( (0,0,0) )
            text = ourFont.render(playerName, True, (255,0, 0))
            block = text.get_rect()
            block.center = (400,300) #dead center
            rect_list.append(screen.blit(text, block))

            pygame.display.update(rect_list)

            # High scores menu
         
         elif state == STATE_RULES_P_ONE:
            rect_list, state = game_rules_one_menu.update(e, state)
            
            if not imageIsShown:
               # only show on the first page instance, otherwise will need to keep redrawing :. inefficient
               rect_list.append(screen.blit(rules_one, (20, 250)))
               imageIsShown = True

            if prev_state != state:
               # changed page
               imageIsShown = False

         elif state == STATE_RULES_P_TWO:
            rect_list, state = game_rules_two_menu.update(e, state)
            
            if not imageIsShown:
               # only show on the first page instance, otherwise will need to keep redrawing :. inefficient
               rect_list.append(screen.blit(rules_two, (20, 250)))
               imageIsShown = True

            if prev_state != state:
               # changed page
               imageIsShown = False

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

