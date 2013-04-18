print "BEFORE REMOVE, CLEAR!"
print "SORT killerFromGroup()"
print "TODO: FoodCurse expiry"
print "TODO: MAKE make_food(snake, foodType, properties)"
        
import pygame
from pygame import *
from Food_Module import *
from Snake_Module import *
from Ball_Module import *
from Config import *
import random
from random import choice
# from Game import *

def killerFromGroup(ballGroup):
    ### NEED A BETTER WAY OF DOING THIS
    G = pygame.sprite.Group()
    for b in ballGroup:
        if b.__class__.__name__ == 'BallKiller':
            return b
    return None

def generateXY():
    posx = randint(0, DEFAULT_SCREEN_SIZE[0])
    posy = randint(0, DEFAULT_SCREEN_SIZE[1])

    return (posx, posy)
            


class Game():
    
    def ballKillerSpawned(self):
        return (len(self.ballKillerGroup) > 0)


    def __init__(self, level = None):
        
        # ### TODO less {self.}



        ### --------- initialise pygame and set up the window
        pygame.init()

        display.set_caption(PAGE_TITLE)
        screen.fill(BACKGROUND_COLOUR)


        self.gameScore = 0

        self.userEscape = False  # User ends game by ESC
        self.gameOver = False  # Game over by death

        self.freezeActiveBallsTimer = 0

        self.clock = pygame.time.Clock()

        ### --------- Generate the snake

        self.snake = Snake()

        self.snakeSprite = pygame.sprite.Group()
        self.snakeSprite.add(self.snake.get_sections())

        

        # needed for clear/draw
        self.snakeSections = self.snake.get_sections()
        


        ### --------- Initial food

        self.foodGroup  = pygame.sprite.Group()
        # config['food']['standard']['initial']
        for n in range(INITIAL_FOOD_NUM):
            self.foodGroup.add(make_food(self.snake))

        for n in range(INITIAL_FOOD_BLUE_NUM):
            self.foodGroup.add(make_food(self.snake,'FoodBlue'))

        for n in range(INITIAL_FOOD_MYSTERIOUS_NUM):
            self.foodGroup.add(make_food(self.snake, 'FoodMysterious'))

        for n in range(INITIAL_FOOD_CURSE_NUM):
            self.foodGroup.add(make_food(self.snake, 'FoodCurse'))


        print "TODO: random food generation i.e. curse/mysterious i.e. if time() % 123 == 0"


        ### --------- Initial balls

        self.ballGroup  = pygame.sprite.Group()

        for n in range(INITIAL_BALL_NUM):
            self.ballGroup.add(BallStandard(generateXY()))

        self.ballKillerGroup = pygame.sprite.Group()
        if INITIAL_BALL_KILLER_NUM != 0:
            self.ballKillerGroup.add(BallKiller(generateXY()))            

    def update(self):
        # handle all updates - ALL CODE BELOW:
        self.clock.tick(FPS)

        self.handleKeyPress()
        self.handleCollisions()
        self.handleExpiry()
        
        
        ### ---------------- NEEDS TO BE SORTED OUT --------------
        # while >=0 aka not active
    
        
        if self.freezeActiveBallsTimer > 0:
            self.freezeActiveBallsTimer -= FPS

        if self.gameOver == False:
            movement = self.snake.move(DEFAULT_SCREEN_SIZE[0],
                                  DEFAULT_SCREEN_SIZE[1])
            if movement != False:
                self.handleUpdates()
            else:
                self.gameOver = True
                self.exitGame()

        if ((self.gameOver == True) or (self.userEscape == True)):
            self.exitGame()

        # while running:
        # # # game.update()

    def handleKeyPress(self):

        direction = self.snake.direction

        for keyPress in event.get():
            if keyPress.type == KEYDOWN:
                if keyPress.key == K_ESCAPE or keyPress.key == K_q:
                    self.userEscape = True
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


                self.snake.direction = direction 
                #else:
                #else:
                 #   print "ELSE"




    def handleUpdates(self):
        # much better method of drawing them all - handled by the SpriteGroup
      ##################################################################################################################
        screen.fill(BACKGROUND_COLOUR)
########################################################################################################################################################
        for ballGroup in [self.ballGroup, self.ballKillerGroup]:
            if len(ballGroup) > 0:
                for ball in ballGroup:
                    ball.display()
                    if self.freezeActiveBallsTimer == 0:
                        ball.bounce()
                        ball.move()
                    
        for group in [self.foodGroup, self.snakeSections, self.ballGroup, self.ballKillerGroup]:
            
            # always clear in case we removed it this update()
            # clear any used areas from the last iteration, replacing them with the background
            #### NOT WORKING
            # group.clear(screen, BACKGROUND)

            # only draw if they've got anything in them!
            if len(group) > 0:
                group.draw(screen)


        pygame.display.update()


    def handleCollisions(self):
        # bubble search style collision check?
        

        snakeHead = self.snake.get_head()

        #### FOOD


        collisionsFood = pygame.sprite.spritecollide(snakeHead,
                    self.foodGroup, True)
        if collisionsFood:

            # #### TODO reactToCollision(properties, snake, foodGroup)

            # get the collided food item, then recreate it in a new random, position

            properties = collisionsFood[0].get_properties()

            if properties['autoRespawn']:
                self.foodGroup.add(make_food(self.snake, properties['type'], properties['colour'], properties['size'], properties['effect']))

            if properties['effect']['curse'] == True:
                self.snake.curse_tail(True)

            if properties['effect']['spawnKiller']:
                if self.ballKillerSpawned() == False:
                # need a function to generate generic safe spawn
                # maybe make the stimulus for a killer ball to be spawned more complicated 
                    self.ballKillerGroup.add( BallKiller(generateXY()))

            if properties['effect']['spawnStandard']:
                if len(self.ballGroup) + 1 < MAX_BALLS:
                    self.ballGroup.add(BallStandard(generateXY()))
                    # ##################

            if properties['effect']['freezeBall'] > 0:
                print "Balls Frozen"
                self.freezeActiveBalls = True
                # then no hard coded values, works based on the FPS *not* faster/slower hardware values
                self.freezeActiveBallsTimer += FPS * properties['effect']['freezeBall']
                print self.freezeActiveBallsTimer
                
            if properties['effect']['removeStandard']:
                print "Removed ball"
                # bad way of removing the first element 

                for b in self.ballGroup:
                    self.ballGroup.remove(b)
                    break

            if properties['effect']['removeKiller']:
                print "Removed killer ball"
                if self.ballKillerSpawned():
                    self.ballKillerGroup.empty()

            self.snake.adjust_tail_size(properties['effect']['size'])

            _S = (float) ((properties['effect']['score'] * properties['time']))
            self.gameScore += int((round(_S / FPS)) * DIFFICULTY_BONUS)


            self.setWindowTitle(str(self.gameScore))

                # update these so we can then redraw them later - only update once we've got a larger snake, otherwise we're wasting CPU!

            self.snakeSprite = pygame.sprite.Group()
            self.snakeSprite.add(self.snake.get_sections())
            self.snakeSections = self.snake.get_sections()

        #### END collisionsFood


        # only work on collisions with ballKiller if we've got one in play
        # if len(self.ballKillerGroup) > 0:
        ballKiller = killerFromGroup(self.ballKillerGroup)

        if ballKiller != None:
            collisionsFoodKiller = pygame.sprite.spritecollide(ballKiller, self.foodGroup, True)

            if collisionsFoodKiller:
                for f in collisionsFoodKiller:
                    properties = collisionsFoodKiller[0].get_properties()
                    if properties['autoRespawn']:
                        self.foodGroup.add(make_food(self.snake, properties['type'], properties['colour'], properties['size'], properties['effect']))
            
            # don't remove balls, just bounce
            collisionsBallsKiller = pygame.sprite.spritecollide(ballKiller, self.ballGroup, False)    

            if collisionsBallsKiller:
                for b in collisionsBallsKiller:
                    b.collision(ballKiller)
            

        # handle this more quickly
        allBalls = pygame.sprite.Group()

        allBalls.add(self.ballGroup)
        allBalls.add(self.ballKillerGroup)

        if len(allBalls) > 0:
            collisionsBall = pygame.sprite.spritecollide(snakeHead, allBalls, False)
            if collisionsBall:
                self.gameOver = True

    def handleExpiry(self):
        for foodBit in self.foodGroup:
            if foodBit.expire():
                properties = foodBit.get_properties()
                ### OR just refresh the food element?
                ### TODO food.refresh() / food.respawn()
                if properties['autoRespawn']:
                    self.foodGroup.add(make_food(self.snake, properties['type'], properties['colour'], properties['size'], properties['effect']))
                self.foodGroup.remove(foodBit)

    def exitGame(self):
        print 'Final score was ' + str(self.gameScore)
        print str(self.userEscape) + ' ' + str(self.gameOver)
        exit()


    def setWindowTitle(self,str=None):
        if str == None:
            display.set_caption(PAGE_TITLE)
        else:
            display.set_caption(PAGE_TITLE + ' - ' + str)

class Level():
    pass
