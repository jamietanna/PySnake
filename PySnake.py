#! /usr/bin/env python
# adapted from http://lorenzod8n.wordpress.com/2008/03/01/pygame-tutorial-9-first-improvements-to-the-game/

import pygame
import random

################################################ 
#### Globals
################################################ 

FOOD_SPEED_INCREASE_STEP = 5
FOOD_SPEED_INCREASE_AMT = 1
FOOD_LENGTH_INCREASE = 20

#### TODO: allow user to specify "mode" - denotes initial speed/steps etc

INITIAL_LENGTH = 50
INITIAL_SPEED = 2

FPS = 120

#### TODO; use argv to allow user to specify different resolution

WIDTH = 640
HEIGHT = 400
TOP_GUTTER = 20




################################################ 
########### Main Code
################################################

class Snake:
    """ A snake. """
    
    num_eaten = 0

    def __init__(self, surface):
        self.surface = surface
        self.x = surface.get_width() / 2
        self.y = surface.get_height() / 2
        self.len = INITIAL_LENGTH
        self.vx = 0
        self.vy = -1
        self.body_list=[[self.x, self.y +i] for i in range (self.len)]
        self.crashed = False
        self.colour = 255, 255, 255
        self.speed = INITIAL_SPEED

    def eat(self):
        self.len += FOOD_LENGTH_INCREASE
        self.num_eaten += 1
        if self.num_eaten % FOOD_SPEED_INCREASE_STEP == 0:
            self.speed += FOOD_SPEED_INCREASE_AMT
#        self.speed
#        self.speed += FOOD_SPEED_INCREASE

    def key_event(self, event):
        """ Handle key events that affect the snake. """
        if event.key == pygame.K_UP:
            if self.vy == 1: return
            self.vx = 0
            self.vy = -1
        elif event.key == pygame.K_DOWN:
            if self.vy == -1: return
            self.vx = 0
            self.vy = 1
        elif event.key == pygame.K_LEFT:
            if self.vx == 1: return
            self.vx = -1
            self.vy = 0
        elif event.key == pygame.K_RIGHT:
            if self.vx == -1: return
            self.vx = 1
            self.vy = 0

    def move(self):
        """ Move the snake. """
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed
        
        if [self.x,self.y] in self.body_list:
            self.crashed = True
            
        self.body_list.insert(0, [self.x, self.y])
        
        if len(self.body_list) > self.len:
            self.body_list.pop()
        
    def draw(self):
        for i in self.body_list:
            pygame.draw.circle(self.surface, self.colour, (i[0],i[1]), 2)
#            pygame.draw.rect(self.surface,self.colour, (i[0],i[1], 5,),2)


#### TODO: if not collected within certain time, disappears
class Food:
    def __init__(self, surface):
        self.surface = surface
        self.x = random.randint(0, (surface.get_width() - 10))
        self.y = random.randint(0, (surface.get_height() - 10))
        self.color = 255, 255, 255

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, 10, 10), 0)

    def erase(self):
        pygame.draw.rect(self.surface, (0, 0, 0), (self.x, self.y, 10, 10), 0)

    def check(self, x, y):
        if x < self.x or x > self.x + 10:
            return False
        elif y < self.y or y > self.y + 10:
            return False
        else:
            return True

# initialise our screen, clock

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


# Our snake.
snake = Snake(screen)
#### TODO: multiple pieces of food
food = Food(screen)
running = True

# numeaten = 0

# create the score sprite
pygame.font.init()


while running:
    screen.fill((0, 0, 0))
    snake.move()
    snake.draw()
    food.draw()

    # http://stackoverflow.com/questions/10077644/python-display-text-w-font-color
    myfont = pygame.font.SysFont("monospace", 18)
    label = myfont.render("Score: "+str(snake.num_eaten), 1, (255,255,0))
    screen.blit(label, (0, 0))
    
    if snake.crashed:
        running = False
    elif snake.x <= 0 or snake.x >= WIDTH-1:
        running = False
    elif snake.y <= 0 or snake.y >= HEIGHT-1:
#        print "Crash!"
        running = False
    elif food.check(snake.x,snake.y):
        snake.eat()
        food.erase()
        food = Food(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            snake.key_event(event)

    pygame.display.flip()
    clock.tick(FPS)

# here we have finished, therefore show scores etc (in the console)
# however, this is going to be quite useless now we're showing it on screen
print "You successfully got a total of", snake.num_eaten, "pieces of food!"
