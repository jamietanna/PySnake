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
    g = pygame.sprite.Group()
    for b in ballGroup:
        if b.__class__.__name__ == 'BallKiller':
            g.add(b)
    return b


class Game():
    
    def __init__(self, level = None):
        
        # ### TODO less {self.}



        ### --------- initialise pygame and set up the window
        pygame.init()

        display.set_caption(PAGE_TITLE)
        screen.fill(BACKGROUND_COLOUR)


        self.gameScore = 0

        self.userEscape = False  # User ends game by ESC
        self.gameOver = False  # Game over by death

        self.clock = pygame.time.Clock()

        ### --------- Generate the snake

        self.snake = Snake()

        self.snakeSprite = pygame.sprite.Group()
        self.snakeSprite.add(self.snake.get_sections())

        

        ##### NEEDED?
        self.snakeSections = self.snake.get_sections()
        self.snakeHead = self.snake.get_head()





        ### --------- Initial food

        self.foodGroup  = pygame.sprite.Group()
        # config['food']['standard']['initial']
        for n in range(INITIAL_FOOD_NUM):
            self.foodGroup.add(make_food(self.snake))

        for n in range(INITIAL_FOOD_BLUE_NUM):
            self.foodGroup.add(make_food(self.snake,'FoodBlue'))

        self.foodGroup.add(make_food(self.snake, 'FoodCurse'))
        self.foodGroup.add(make_food(self.snake, 'FoodMysterious'))


        ### --------- Initial balls

        self.ballGroup  = pygame.sprite.Group()

        for n in range(INITIAL_BALL_NUM):
            posx = randint(0,400)
            posy = randint(0,400)
            self.ballGroup.add(BallStandard((posx,posy)))

        self.ballGroup.add(BallKiller((200,0)))

        
        #self.updatetime = pygame.time.get_ticks() + DEFAULT_UPDATE_SPEED


        self.direction = Snake.SnakeMove.UP





        ####


    def update(self):
        # handle all updates - ALL CODE BELOW:
        self.clock.tick(FPS)

        self.handleKeyPress()
        self.handleCollisions()
        self.handleExpiry()
        
        
        ### ---------------- NEEDS TO BE SORTED OUT --------------
        for ball in self.ballGroup:
            ball.bounce()
            ball.move()
            ball.update()
            ball.display()

        if self.gameOver == False:
            movement = self.snake.move(self.direction, DEFAULT_SCREEN_SIZE[0],
                                  DEFAULT_SCREEN_SIZE[1])
            if movement != False:
                self.handleUpdates()
            else:
                self.gameOver = True
                self.exitGame()

        if ((self.gameOver == True) or (self.userEscape == True)):
            display.set_caption(PAGE_TITLE + ': ' + str(self.gameScore) + ' YOU DIED')
            self.exitGame()

        # while running:
        # # # game.update()

    def handleKeyPress(self):
        for keyPress in event.get():
            if keyPress.type == KEYDOWN:
                if keyPress.key == K_ESCAPE or keyPress.key == K_q:
                    self.userEscape = True
                elif keyPress.key == K_UP:
                    if self.direction != Snake.SnakeMove.DOWN:
                        self.direction = Snake.SnakeMove.UP
                elif keyPress.key == K_DOWN:
                    if self.direction != Snake.SnakeMove.UP:
                        self.direction = Snake.SnakeMove.DOWN
                elif keyPress.key == K_RIGHT:
                    if self.direction != Snake.SnakeMove.LEFT:
                        self.direction = Snake.SnakeMove.RIGHT
                elif keyPress.key == K_LEFT:
                    if self.direction != Snake.SnakeMove.RIGHT:
                        self.direction = Snake.SnakeMove.LEFT
                #else:
                 #   print "ELSE"




    def handleUpdates(self):
        # much better method of drawing them all - handled by the SpriteGroup
        
        # clear any used areas from the last iteration, replacing them with the background
        self.foodGroup.clear(screen, BACKGROUND)
        self.snakeSections.clear(screen, BACKGROUND)
        self.ballGroup.clear(screen, BACKGROUND)

        
        # then draw the new content
        self.foodGroup.draw(screen)
        self.snakeSections.draw(screen)
        self.ballGroup.draw(screen)

        pygame.display.update()


    def handleCollisions(self):
        # bubble search style collision check?
        

        #### FOOD


        collisionsFood = pygame.sprite.spritecollide(self.snakeHead,
                    self.foodGroup, True)
        if collisionsFood:

            # #### TODO reactToCollision(properties, snake, foodGroup)

            # get the collided food item, then recreate it in a new random, position

            properties = collisionsFood[0].get_properties()
            self.foodGroup.add(make_food(self.snake, properties['type'], properties['colour'], properties['size'], properties['effect']))

            if properties['effect']['curse'] == True:
                self.snake.curse_tail(True)

                    # ##################

                    ## snake.adjust_tail_size()

            self.snake.adjust_tail_size(properties['effect']['size'], self.direction)

                #snake.lengthen_tail(1, direction)
            self.gameScore += properties['effect']['score']
            self.setWindowTitle(str(self.gameScore))

                # update these so we can then redraw them later - only update once we've got a larger snake, otherwise we're wasting CPU!

            self.snakeSprite = pygame.sprite.Group()
            self.snakeSprite.add(self.snake.get_sections())
            self.snakeSections = self.snake.get_sections()

        collisionsFoodKiller = pygame.sprite.spritecollide(killerFromGroup(self.ballGroup), self.foodGroup, True)
        if collisionsFoodKiller:
            for f in collisionsFoodKiller:
                properties = collisionsFoodKiller[0].get_properties()
                self.foodGroup.add(make_food(self.snake, properties['type'], properties['colour'], properties['size'], properties['effect']))
                self.foodGroup.remove(f)

        collisionsBall = pygame.sprite.spritecollide(self.snakeHead,self.ballGroup, False)
        if collisionsBall:
            self.gameOver = True

    def handleExpiry(self):
        for (idx, foodBit) in enumerate(self.foodGroup):
                if foodBit.expire():
                    properties = foodBit.get_properties()
                    ### OR just refresh the food element?
                    ### TODO food.refresh() / food.respawn()
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