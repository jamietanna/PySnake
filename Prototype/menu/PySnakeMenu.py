# implemented Scott Barlow's Menu system
# http://www.pygame.org/project-MenuClass-1260-.html

import sys, pygame
# from menu import *
import menu
import os
import image
import Config
# base_path = '/home/jamie/Programming/Python/jvt02u-g51fse/Prototype'
base_path = 'H:\Private\G51FSE\Coursework\jvt02u-g51fse\Prototype'

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

   print "OPENING FILE ", fileName

   execfile(os.path.join(levels_path, fileName + '.lvl'), settings)
   return settings


img_dir = os.path.join(base_path, 'menu', 'images') # "H:\Private\G51FSE\Coursework\jvt02u-g51fse\Prototype\menu\MenuClass_V1.0.3\images"


def generate_main_menu(screen):
   main_menu = menu.cMenu(50, 50, 0, 0, 'vertical', 10, screen,
               [('Select Level', STATE_LEVEL_SELECT, None),
                ('Create Level',  STATE_LEVEL_CREATOR, None),
                ('High Scores', STATE_HIGH_SCORES, None),
                ('Game Rules', STATE_RULES_P_ONE, None),
                ('Exit', STATE_EXIT, None)])

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

   if screenNum == 1:
      game_rules_menu = menu.cMenu(200, 200, 0, 0, 'horizontal', 8, screen, [('Next', STATE_RULES_P_TWO, None),('Return to Main', STATE_MAIN_MENU, None)])



   elif screenNum == 2:
      game_rules_menu = menu.cMenu(200, 200, 0, 0, 'horizontal', 8, screen, [('Previous', STATE_RULES_P_ONE, None),('Return to Main', STATE_MAIN_MENU, None)])

   game_rules_menu.set_unselected_color([122,201,67])
   game_rules_menu.set_selected_color([255,255,255])
   game_rules_menu.set_position(200,510)
   game_rules_menu.set_alignment('center', 'center')

   return game_rules_menu
   


## ---[ main ]------------------------------------------------------------------
#  This function runs the entire screen and contains the main while loop
#
def main():
   print "TODO: check expiry working - not sure?!"
   print "TODO: move these all into func, i.e. generate_select_level()"
   print "TODO: get all (50,250) etc as different variables, esp the colours"

   # Initialize Pygame
   pygame.init()
   # Create a window of 800x600 pixels
   print "TODO: grab res from Config"
   screen = pygame.display.set_mode(Config.DEFAULT_SCREEN_SIZE)

   # Set the window caption
   pygame.display.set_caption("PySnake")
   bkg = image.load_image(base_path + '\menu\images\pysnake.jpg', img_dir)
   
   print "TODO: more programmatic way, i.e. eval/exec"

   rules_one = image.load_image('pysnake_rules_one.jpg', img_dir)
   rules_two = image.load_image('pysnake_rules_two.jpg', img_dir)
   # Create 3 diffrent menus.  One of them is only text, another one is only
   # images, and a third is -gasp- a mix of images and text buttons!  To
   # understand the input factors, see the menu file
   menu = generate_main_menu(screen)

   level_select_menu = generate_level_select(screen)
   high_scores_menu = generate_high_scores(screen)
   game_rules_one_menu = generate_game_rules(screen,1)
   game_rules_two_menu = generate_game_rules(screen,2)

   # print "Loading Levels..."

   LEVEL_ID_OFFSET = 9000

   

   
   
   
   
   
   


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
   pygame.event.set_blocked(pygame.MOUSEMOTION)
   # The main while loop
   while True:
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

         if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE or e.key == pygame.K_q:
               # if we press escape/q on the main menu, quit
               if state == STATE_MAIN_MENU:
                  state = STATE_EXIT
               # otherwise return to the main menu
               else:
                  state = STATE_MAIN_MENU
               


         if state == STATE_MAIN_MENU:
            rect_list, state = menu.update(e, state)

         elif state == STATE_LEVEL_SELECT:
            rect_list, state = level_select_menu.update(e, state)

         elif state > LEVEL_ID_OFFSET:
            rect_list, state = level_select_menu.update(e, state)
            # level = level_select_menu.get_current_text()

            print "Level", (state % 9000)

            fName = level_files[(state % 9000) - 1]['fName']


            print "CHOSEN: \"", level_files[(state % 9000) - 1]['settings']['level_name'], "\""
            print "SPAWN NEW GAME"


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

            Config.PAGE_TITLE = Config.PAGE_TITLE + ' ' + level_files[(state % 9000) - 1]['fName']



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




            execfile('Snake.py')


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

