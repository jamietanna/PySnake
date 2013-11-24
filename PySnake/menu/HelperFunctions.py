from random import randint
import Config
import pickle
import bisect
import random

def random_rgb():
    rcolour = randint(50,255)
    bcolour = randint(50,255)
    gcolour = randint(50,255)
    return [rcolour, bcolour, gcolour]


# Static function
class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

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
   createNew = False
   
   try:
      highScores = open(Config.HIGH_SCORES_FILENAME, "r")
      highScoresList = pickle.load(highScores)
   
   except EOFError:
      print "Blank high scores file"
      createNew = True
      
   except IOError:
      print "No file exists, creating new blank high scores file"
      createNew = True
      
   if createNew:
      highScores = open(Config.HIGH_SCORES_FILENAME, "w+")
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
   
   highScoresList.append((score, name))
   highScoresList.sort(reverse=True)

   highScores = open(Config.HIGH_SCORES_FILENAME, "w")
   # only get top 10
   pickle.dump(highScoresList[:10], highScores)
   highScores.close()

   # just return whether the top 10 are the same elements as they are before
   # if they're the same, no dice
   # otherwise, we're in!
   return highScoresList[:10] != oldHighScores
   


def makeTextRect(text, colour, xyTuple, screen, ourFont, isCentered = False):
   text = ourFont.render(text, True, colour)
   block = text.get_rect()
   if isCentered:
      block.center = xyTuple
   else:
      # print "TODO: nice centering"
      block.topleft = xyTuple 

   return screen.blit(text, block)

def generateXY():
    posx = random.randint(0, Config.DEFAULT_SCREEN_SIZE[0])
    posy = random.randint(0, Config.DEFAULT_SCREEN_SIZE[1])

    return (posx, posy)

def generateSafeXY(snake, ballGroup, killerBall, foodGroup):
   snakeHead = snake.get_head()

   notValidCoord = False

   posx = random.randint(0, Config.DEFAULT_SCREEN_SIZE[0])
   posy = random.randint(0, Config.DEFAULT_SCREEN_SIZE[1])


   while notValidCoord:

      posx = random.randint(0, Config.DEFAULT_SCREEN_SIZE[0])
      posy = random.randint(0, Config.DEFAULT_SCREEN_SIZE[1])
      
      test = Food(None, None, None, (posx, posy))

      if not pygame.sprite.spritecollide(test, snakeHead, False):
         if not pygame.sprite.spritecollide(test, ballGroup, False):
            if killerBall and not pygame.sprite.spritecollide(test, killerBall, False):
               if not pygame.sprite.spritecollide(test, foodGroup, False):
                  notValidCoord = True

   return (posx, posy)



   # return 
