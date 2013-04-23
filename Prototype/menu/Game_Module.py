# print "BEFORE REMOVE, CLEAR!"
print "SORT killerFromGroup()"
print "TODO: MAKE make_food(snake, foodType, properties)"
print "TODO: rules!!!"
print "TODO: replay?"

import pygame
import Food_Module
import Snake_Module
import Ball_Module
# from Config import *
import Config
import random
# from Game import *

def killerFromGroup(ballGroup):
    ### NEED A BETTER WAY OF DOING THIS
    G = pygame.sprite.Group()
    for b in ballGroup:
        if b.__class__.__name__ == 'BallKiller':
            return b
    return None

def generateXY():
    posx = random.randint(0, Config.DEFAULT_SCREEN_SIZE[0])
    posy = random.randint(0, Config.DEFAULT_SCREEN_SIZE[1])

    return (posx, posy)
            
def create_settings(settings):
    for s in settings:
        print s



class Game():
    
    def ballKillerSpawned(self):
        return (len(self.ballKillerGroup) > 0)


    def __init__(self, gameSettings = None):
        
        
        # ### TODO less {self.}



        ### --------- initialise pygame and set up the window
        pygame.init()
        pygame.display.set_caption(Config.PAGE_TITLE)
        Config.screen.fill(Config.BACKGROUND_COLOUR)


        self.gameScore = 0

        self.userEscape = False  # User ends game by ESC
        self.gameOver = False  # Game over by death

        self.freezeActiveBallsTimer = 0

        self.clock = pygame.time.Clock()

        ### --------- Generate the snake

        self.snake = Snake_Module.Snake()

        self.snakeSprite = pygame.sprite.Group()
        self.snakeSprite.add(self.snake.get_sections())

        

        # needed for clear/draw
        self.snakeSections = self.snake.get_sections()
        


        ### --------- Initial food

        self.foodGroup  = pygame.sprite.Group()
        # config['food']['standard']['initial']
        for n in range(Config.INITIAL_FOOD_NUM):
            self.foodGroup.add(Food_Module.make_food(self.snake))

        for n in range(Config.INITIAL_FOOD_SUPER_NUM):
            self.foodGroup.add(Food_Module.make_food(self.snake,'FoodSuper'))

        for n in range(Config.INITIAL_FOOD_MYSTERIOUS_NUM):
            self.foodGroup.add(Food_Module.make_food(self.snake, 'FoodMysterious'))

        for n in range(Config.INITIAL_FOOD_CURSE_NUM):
            self.foodGroup.add(Food_Module.make_food(self.snake, 'FoodCurse'))


        print "TODO: random food generation i.e. curse/mysterious i.e. if time() % 123 == 0"


        ### --------- Initial balls

        self.ballGroup  = pygame.sprite.Group()

        for n in range(Config.INITIAL_BALL_NUM):
            self.ballGroup.add(Ball_Module.BallStandard(generateXY()))

        self.ballKillerGroup = pygame.sprite.Group()
        if Config.INITIAL_BALL_KILLER_NUM != 0:
            self.ballKillerGroup.add(Ball_Module.BallKiller(generateXY()))            

    def update(self):
        # handle all updates - ALL CODE BELOW:
        self.clock.tick(Config.FPS)


        self.handleKeyPress()
        self.handleCollisions()
        self.handleExpiry()
        self.handleRandoms()
        
        ### ---------------- NEEDS TO BE SORTED OUT --------------
        # while >=0 aka not active
    
        
        if self.freezeActiveBallsTimer > 0:
            self.freezeActiveBallsTimer -= Config.FPS

        if self.gameOver == False:
            movement = self.snake.move(Config.DEFAULT_SCREEN_SIZE[0],
                                  Config.DEFAULT_SCREEN_SIZE[1])
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

        for keyPress in pygame.event.get():
            if keyPress.type == pygame.KEYDOWN:
                if keyPress.key == pygame.K_ESCAPE or keyPress.key == pygame.K_q:
                    self.userEscape = True
                elif keyPress.key == pygame.K_UP:
                    if direction != Snake_Module.Snake.SnakeMove.DOWN:
                        direction = Snake_Module.Snake.SnakeMove.UP
                elif keyPress.key == pygame.K_DOWN:
                    if direction != Snake_Module.Snake.SnakeMove.UP:
                        direction = Snake_Module.Snake.SnakeMove.DOWN
                elif keyPress.key == pygame.K_RIGHT:
                    if direction != Snake_Module.Snake.SnakeMove.LEFT:
                        direction = Snake_Module.Snake.SnakeMove.RIGHT
                elif keyPress.key == pygame.K_LEFT:
                    if direction != Snake_Module.Snake.SnakeMove.RIGHT:
                        direction = Snake_Module.Snake.SnakeMove.LEFT


                self.snake.direction = direction 
                #else:
                #else:
                 #   print "ELSE"




    def handleUpdates(self):
        # much better method of drawing them all - handled by the SpriteGroup
        # unfortunately, we need to keep this in - using group.clear() gives some sprites black backgrounds and it looks terrible
        Config.screen.fill(Config.BACKGROUND_COLOUR)

        for ballGroup in [self.ballGroup, self.ballKillerGroup]:
            if len(ballGroup) > 0:
                for ball in ballGroup:
                    ball.display()
                    if self.freezeActiveBallsTimer == 0:
                        ball.bounce()
                        ball.move()
                    
        for group in [self.foodGroup, self.snakeSections, self.ballGroup, self.ballKillerGroup]:
            
            # see note above re screen.fill()
            # group.clear(screen, BACKGROUND)

            # only draw if they've got anything in them!
            if len(group) > 0:
                group.draw(Config.screen)


        pygame.display.update()


    def handleCollisions(self):
        snakeHead = self.snake.get_head()

        #### FOOD


        collisionsFood = pygame.sprite.spritecollide(snakeHead,
                    self.foodGroup, True)
        if collisionsFood:

            # #### TODO reactToCollision(properties, snake, foodGroup)

            # get the collided food item, then recreate it in a new random, position

            properties = collisionsFood[0].get_properties()

            if properties['autoRespawn']:
                self.foodGroup.add(Food_Module.make_food(self.snake, properties['type'], properties['colour'], properties['size'], properties['effect']))

            if properties['effect']['curse'] == True:
                self.snake.curse_tail()

            if properties['effect']['spawnKiller']:
                # 20% chance
                if self.ballKillerSpawned() == False and (pygame.time.get_ticks() % 5 == 0):
                # need a function to generate generic safe spawn
                # maybe make the stimulus for a killer ball to be spawned more complicated 
                    self.ballKillerGroup.add(Ball_Module.BallKiller(generateXY()))

            if properties['effect']['spawnStandard']:
                if len(self.ballGroup) + 1 < Config.MAX_BALLS:
                    self.ballGroup.add(Ball_Module.BallStandard(generateXY()))

            if properties['effect']['freezeBall'] > 0:
                # then no hard coded values, works based on the FPS *not* faster/slower hardware values
                self.freezeActiveBallsTimer += Config.FPS * properties['effect']['freezeBall']

                print "Balls Frozen for " + str(self.freezeActiveBallsTimer)
                
                
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
            self.gameScore += int((round(_S / Config.FPS)) * Config.DIFFICULTY_BONUS)


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
                        self.foodGroup.add(Food_Module.make_food(self.snake, properties['type'], properties['colour'], properties['size'], properties['effect']))
            
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


    def handleRandoms(self):
        time = pygame.time.get_ticks()

        if ((time % Config.RANDOM_FOOD_MYSTERIOUS_CHANCE) == 0):
            print "Random Melon of Mystery generated"
            self.foodGroup.add(Food_Module.FoodMysterious(None, None, None, generateXY()))
        
        if ((time % Config.RANDOM_FOOD_CURSE_CHANCE) == 0):
            print "Random Berries of Bane generated"
            self.foodGroup.add(Food_Module.FoodCurse(None, None, None, generateXY()))


    def handleExpiry(self):
        
        for foodBit in self.foodGroup:
            if foodBit.expire():
                properties = foodBit.get_properties()
                ### OR just refresh the food element?
                ### TODO food.refresh() / food.respawn()
                if properties['autoRespawn']:
                    self.foodGroup.add(Food_Module.make_food(self.snake, properties['type'], properties['colour'], properties['size'], properties['effect']))
                self.foodGroup.remove(foodBit)

        # update the curse tail timer
        if self.snake.curseTail > 0:
            self.snake.curseTail -= Config.FPS
    
            # put this in here, otherwise it'll run every time :. random colours constantly
            if self.snake.curseTail <= 0:
                self.snake.curseTail = 0
                self.snake.randomize_snake_colour()
                

        

    def exitGame(self):
        print 'Final score was ' + str(self.gameScore)
        print str(self.userEscape) + ' ' + str(self.gameOver)
        exit()


    def setWindowTitle(self,str=None):
        if str == None:
            pygame.display.set_caption(Config.PAGE_TITLE)
        else:
            pygame.display.set_caption(Config.PAGE_TITLE + ' - ' + str)

class Level():
    pass
