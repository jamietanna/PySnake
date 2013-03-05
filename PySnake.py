#! /usr/bin/env python
# adapted from http://lorenzod8n.wordpress.com/2008/03/01/pygame-tutorial-9-first-improvements-to-the-game/

import pygame
import random
import math

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

## ballS

SIZE = 10
number_of_balls = 2
my_balls = []
BALL_COUNT = 0 

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

## BALL CLASS

class Ball():
    def __init__(self, (x, y), SIZE):
        self.x = x
        self.y = y
        self.size = SIZE
        self.colour = (0, 0, 255)
        self.thickness = 1
        self.speed = 2
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def bounce(self):
        if self.x > WIDTH - self.size:
            self.x = 2*(WIDTH - self.size) - self.x
            self.angle = - self.angle

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle

        if self.y > HEIGHT - self.size:
            self.y = 2*(HEIGHT - self.size) - self.y
            self.angle = math.pi - self.angle

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle

    def collide(self, x, y):
        if x < self.x - self.size or x > self.x + self.size:
            return False
        elif y < self.y - self.size or y > self.y + self.size:
            return False
        else:
            return True

# drawing the balls

for n in range(number_of_balls):
    
    x = random.randint(SIZE, WIDTH)
    y = random.randint(SIZE, HEIGHT)
    ball = Ball((x, y), SIZE)
    ball.speed = 1
    ball.angle = random.uniform(0, math.pi*2)
    my_balls.append(ball)

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
    for ball in my_balls:
        ball.move()
        ball.bounce()
        ball.display()

    # http://stackoverflow.com/questions/10077644/python-display-text-w-font-color
    myfont = pygame.font.SysFont("monospace", 18)
    label = myfont.render("Score: "+str(snake.num_eaten), 1, (255,255,0))
    screen.blit(label, (0, 0))
    
    if snake.crashed:
        running = False
    elif snake.x <= 0 or snake.x >= WIDTH-1:
        running = False
    elif snake.y <= 0 or snake.y >= HEIGHT-1:
        running = False
    elif food.check(snake.x,snake.y):
        snake.eat()
        food.erase()
        food = Food(screen)
        # spawns more balls when eaten
        BALL_COUNT+=1
        if (BALL_COUNT == 1):
            x = random.randint(SIZE, WIDTH)
            y = random.randint(SIZE, HEIGHT)
            ball = Ball((x, y), SIZE)
            ball.speed = 1
            ball.angle = random.uniform(0, math.pi*2)
            my_balls.append(ball)
            BALL_COUNT = 0

    # only if head collides with ball,tail is OK
    for ball in my_balls:
        if ball.collide(snake.x,snake.y):
            running = False

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
