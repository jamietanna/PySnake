
#!/usr/bin/python
import os 
import Config

# for filename
import re, string


MAX_FOOD_SETTING = 10
MIN_FOOD_SETTING = 0

MAX_BALL_SETTING = 10
MIN_BALL_SETTING = 0
MIN_SPEED_BALL   = 5
MAX_SPEED_BALL   = 25
MIN_SIZE_BALL    = 5
MAX_SIZE_BALL    = 25

MIN_FPS = 15
MAX_FPS = 35

FPSdict = dict()
FPSdict['easy'] = 20
FPSdict['medium'] = 25
FPSdict['hard'] = 30

STRING = 0
BOOLEAN = 1
SET = 2
INT = 3



print "TODO: make settings dict, then iterate through - keys as values stored in the file"
print "TODO: suggest settings i.e. ball size"

def setToString(set):
    theString = '['

    for s in set:
        theString += s.title() + ', '

    # remove the trailing ", "
    theString = theString[:-2] +  ']'

    return theString

def getUserInput(inputType=STRING, limLow = None, limHigh = None, inputMessage = None, validSet = None):
    isValidated = False
    userInput = None
    validUserInputs = False
    errorMsg = None
    validateLimits = False
    userInputToTest = None

    if inputType == BOOLEAN:
        # keep lowercase to make it easier
        validUserInputs = ['yes', 'no']
        errorMsg = 'Invalid input. Please enter either \'Yes\' or \'No\'. '
        inputMsg = inputMessage + ' (Yes/No): '

    elif inputType == STRING:
        errorMsg = 'Invalid input. Must be a non-empty string. '
        inputMsg = inputMessage + ': '

    elif inputType == SET:
        validUserInputs = validSet
        errorMsg = 'Invalid input. Must be one of the following choices: ' + setToString(validUserInputs)
        inputMsg = inputMessage + ' ' + setToString(validUserInputs) + ': '

    elif inputType == INT:
        # range(10) = 0-9, :. to include 10, add 1
        validUserInputs = range(limLow, limHigh + 1)
        errorMsg = 'Invalid input. Must be an integer in the range ' + str(limLow) + '>= input >= ' + str(limHigh) +'. '
        inputMsg = inputMessage + ' (' + str(limLow) + '>= input >= ' + str(limHigh) +'): '
    else:
        raise Exception

    
    while isValidated == False:
        userInput = raw_input(inputMsg)
        
        if inputType == STRING:
            # that's valid tbh
            userInputToTest = str(userInput)
            isValidated = True
        else:
            if inputType == INT:
                userInputToTest = int(userInput)
            else:
                userInputToTest = userInput.lower()
            
            if userInputToTest in validUserInputs:
                isValidated = True

        if not isValidated:
            print errorMsg
            print ""
        
    if userInputToTest == None:
        raise Exception

    # put these prints in to make all the menu nicer
    print ""
    print ""


    if inputType == BOOLEAN:
        return (userInputToTest == 'yes')
    else:
        return userInputToTest



print '*******         *******         ******* **    ** *******'
print '*******         *******         ******* **    ** *******'
print '**   **         **                   ** **   **  **   **'
print '**   **         **                   ** **   **  **   **'
print '******* **   ** ******* ******* ******* ******   *******'
print '******* **   ** ******* ******* ******* ******   *******'
print '**      **   **      ** **   ** **   ** **   **  **'
print '**      **   **      ** **   ** **   ** **   **  **'
print '**      ******* ******* **   ** ******* **    ** *******'
print '**      ******* ******* **   ** ******* **    ** *******'
print '             **'
print '             **  Level Creator'
print '        *******  V 1.0'
print '        *******'
print ""
print "================================================================="
print "Note: any spaces in 'level name' will be converted to underscores"
print "================================================================="
print ""
print "================================================================="
print "                         Level Options:"
print "================================================================="
print ""
# levelName = raw_input('Enter the name of your level: ').replace(' ','_')

levelName = getUserInput(STRING, None, None, 'Enter the name of your level')

# sanitise
# levelName.replace('\'',' ')
# levelName.replace('_',' ')
levelName.replace('"','\"')


levelDifficulty = getUserInput(SET, None, None, 'Set the level difficulty', ['hard', 'medium', 'easy'])

doSetBackgroundColour = getUserInput(BOOLEAN, None, None, 'Do you wish to change the arena\'s background colour?')

if doSetBackgroundColour:
    redCol = getUserInput(INT, 0, 255, 'Background Colour - Enter the red element')

    greenCol = getUserInput(INT, 0, 255, 'Background Colour - Enter the green element')
    
    blueCol = getUserInput(INT, 0, 255, 'Background Colour - Enter the blue element')

    rgb_colour = [redCol, greenCol, blueCol]
else:
    rgb_colour = Config.BACKGROUND_COLOUR

print ""
print "=================================================================="
print "                         Food Options"
print "=================================================================="
print ""

initialFood = getUserInput(INT, MIN_FOOD_SETTING, MAX_FOOD_SETTING, 'Enter the initial amount of Base Bananas')

initialSuperFood = getUserInput(INT, MIN_FOOD_SETTING, MAX_FOOD_SETTING, 'Enter the initial amount of Lemons of Length')

initialMysteriousFood = getUserInput(INT, MIN_FOOD_SETTING, MAX_FOOD_SETTING, 'Enter the initial amount of Mysterious Melons')

initialCurseFood = getUserInput(INT, MIN_FOOD_SETTING, MAX_FOOD_SETTING, 'Enter the initial amount of Berries of Bane')





print ""
print "=================================================================="
print "                         Ball Options"
print "=================================================================="
print ""

initialBalls = getUserInput(INT, MIN_BALL_SETTING, MAX_BALL_SETTING, 'Enter the initial amount of normal obstacle balls')

maxBalls = getUserInput(INT, MIN_BALL_SETTING, MAX_BALL_SETTING, 'Enter the maximum amount of obstacle balls')

speedBalls = getUserInput(INT, MIN_SPEED_BALL, MAX_SPEED_BALL, 'Enter the speed of the obstacle balls')

sizeBalls = getUserInput(INT, MIN_SIZE_BALL, MAX_SIZE_BALL, 'Enter the size of the obstacle balls')

setKillerBall = getUserInput(BOOLEAN, None, None, 'Initially spawn the killer ball?')


print ""
print "=================================================================="
print "                         Video Options"
print "=================================================================="
print ""

FPSMessage = 'Enter the size of the obstacle balls'



FPSMessage += ', ' + str(FPSdict[levelDifficulty]) + ' suggested for ' + levelDifficulty.title()


FPS = getUserInput(INT, MIN_FPS, MAX_FPS, FPSMessage)


print ""
print "=================================================================="
print "                         Summary"
print "=================================================================="
print ""

print "Level Name: " + levelName
print "Level Difficulity: " + levelDifficulty.title()
print "Initial Food: " + str(initialFood)
print "Initial Super Food: " + str(initialSuperFood)
print "Initial Mysterious Food: " + str(initialMysteriousFood)
print "Initial Cursed Food: " + str(initialCurseFood)
print "Initial Obstacle Balls: " + str(initialBalls)
print "Maximum Obstacle Balls: " + str(maxBalls)
print "Obstacle Ball Speed: " + str(speedBalls)
print "Obstacle Ball Size: " + str(sizeBalls)
print "Spawn the Killer Ball: " + str(setKillerBall)
print "FPS: " + str(FPS)
print "Background Colour: " + str(rgb_colour)
print ""
print ""


createLevel = getUserInput(BOOLEAN, None, None, 'Create level?')

if createLevel:
    # adapted from http://stackoverflow.com/questions/12985456/replace-all-non-alphanumeric-characters-in-a-string
    fileName = re.sub('[^0-9a-zA-Z]+', '_', levelName)

    with open('levels/' + levelName + ".lvl", "w") as text_file:
        text_file.write("level_name = \"" + levelName + "\"\n")
        text_file.write("difficulty = \"" + levelDifficulty.title() + "\"\n")
        text_file.write("initial_food_num = " + str(initialFood) + "\n")
        text_file.write("initial_food_super_num = " + str(initialSuperFood) + "\n")
        text_file.write("initial_food_mysterious_num = " + str(initialMysteriousFood) + "\n")
        text_file.write("initial_food_curse_num = " + str(initialCurseFood) + "\n")
        text_file.write("initial_ball_num = " + str(initialCurseFood) + "\n")
        
        text_file.write("initial_ball_killer_num = ")
        text_file.write('1\n' if setKillerBall else '0\n')
        
        text_file.write("max_balls = " + str(maxBalls) + "\n")
        text_file.write("ball_speed = " + str(speedBalls) + "\n")
        text_file.write("ball_size = " + str(sizeBalls) + "\n")
        text_file.write("fps = " + str(FPS) + "\n")
        text_file.write("background_colour = " + str(rgb_colour))

        print ""
        print ""
        print "Success - Level has been created, please run PySnake to play!"
        print ""
        print ""
