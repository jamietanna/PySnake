#! /usr/bin/env python
# adapted from http://lorenzod8n.wordpress.com/2008/03/01/pygame-tutorial-9-first-improvements-to-the-game/

import pygame
import random
import math
import sys

################################################ 
#### Globals
################################################ 

FOOD_SPEED_INCREASE_STEP = 10
FOOD_SPEED_INCREASE_AMT = 1
FOOD_LENGTH_INCREASE = 20
FOOD_EXPIRE_TIME = 5 # seconds

#### TODO: allow user to specify "mode" - denotes initial speed/steps etc
#### TODO: allow floating point speed :. can increment a lot easier
INITIAL_LENGTH = 50
INITIAL_SPEED = 1

FPS = 120

#### TODO; use argv to allow user to specify different resolution

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400

## ballS

#### TODO: Initial num balls determined by the level of difficulty

BALL_SIZE = 10
NUMBER_OF_BALLS = 2
MY_BALLS = []
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


#### TODO: ensure that food spawns in reachable place
#### TODO: if not collected within certain time, disappears
class Food:
    def __init__(self, surface):
        self.surface = surface
        self.x = random.randint(0, (surface.get_width() - 10))
        self.y = random.randint(0, (surface.get_height() - 10))
        self.color = 255, 255, 255
        self.time = FOOD_EXPIRE_TIME * FPS # otherwise clock ticks far too much and we lose it

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
    def expire(self):
	self.time -= 1 #decrement
	if self.time <= 0:
	    return 1
	else:
	    return 0

## BALL CLASS

class Ball():
    def __init__(self, (x, y), BALL_SIZE):
        self.x = x
        self.y = y
        self.size = BALL_SIZE
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
        if self.x > SCREEN_WIDTH - self.size:
            self.x = 2*(SCREEN_WIDTH - self.size) - self.x
            self.angle = - self.angle

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle

        if self.y > SCREEN_HEIGHT - self.size:
            self.y = 2*(SCREEN_HEIGHT - self.size) - self.y
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

for n in range(NUMBER_OF_BALLS):
    
    x = random.randint(BALL_SIZE, SCREEN_WIDTH)
    y = random.randint(BALL_SIZE, SCREEN_HEIGHT)
    ball = Ball((x, y), BALL_SIZE)
    ball.speed = 1
    ball.angle = random.uniform(0, math.pi*2)
    MY_BALLS.append(ball)

# initialise our screen, clock

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


# Our snake.
snake = Snake(screen)
#### TODO: multiple pieces of food
food = Food(screen)
running = True

# numeaten = 0

# create the score sprite
pygame.font.init()

#scoreFont = pygame.font.SysFont("monospace", 18)
smallFont= pygame.font.SysFont("monospace", 18)
bigFont = pygame.font.SysFont("monospace", 24)
    
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    snake.move()
    snake.draw()
    food.draw()
    for ball in MY_BALLS:
        ball.move()
        ball.bounce()
        ball.display()

    # http://stackoverflow.com/questions/10077644/python-display-text-w-font-color
    score = smallFont.render("Score: "+str(snake.num_eaten), 1, (255,255,0))
    screen.blit(score, (0, 0))
    
    timeLeft = smallFont.render("Time left: "+str(food.time), 1, (255,255,0))
    screen.blit(timeLeft, (0, 10))
    
    if snake.crashed:
        running = False
    elif snake.x <= 0 or snake.x >= SCREEN_WIDTH-1:
        running = False
    elif snake.y <= 0 or snake.y >= SCREEN_HEIGHT-1:
        running = False
    elif food.check(snake.x,snake.y):
        snake.eat()
        food.erase()
        food = Food(screen)
        # spawns more balls when eaten
        BALL_COUNT+=1
        if (BALL_COUNT == 1):
            x = random.randint(BALL_SIZE, SCREEN_WIDTH)
            y = random.randint(BALL_SIZE, SCREEN_HEIGHT)
            ball = Ball((x, y), BALL_SIZE)
            ball.speed = 1
            ball.angle = random.uniform(0, math.pi*2)
            MY_BALLS.append(ball)
            BALL_COUNT = 0
    elif food.expire():
	# if we've run out of time to collect the food, then respawn it
	food = Food(screen)

    # only if head collides with ball,tail is OK
    for ball in MY_BALLS:
        if ball.collide(snake.x,snake.y):
            running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            snake.key_event(event)

    pygame.display.flip()
    #clock.tick(FPS)

### For typography
if running == False:
    # here we have finished, therefore show scores etc (in the console)
    # however, this is going to be quite useless now we're showing it on screen
    #### TODO: Scoring system based on difficulty
    #### TODO: Score is increased dependant on time - aka you get more points for getting the food when there's more time on the clock
    #### TODO: Output score on game over, cleared screen
    #### TODO: Top scores
    print "You successfully got a total of", snake.num_eaten, "pieces of food!"
    
    #### TODO: inside the blit() ???
    
    gameOver = bigFont.render("Game Over! You lost.", 1, (255,255,0))
    screen.blit(gameOver, (SCREEN_WIDTH/2, (SCREEN_HEIGHT/2) - 40))
    
    finalScore = bigFont.render("Your final score was: "+str(snake.num_eaten), 1, (255,255,0))
    screen.blit(finalScore, (SCREEN_WIDTH/2, (SCREEN_HEIGHT/2) - 20))
    
    anyKey = bigFont.render("Press any key to exit.", 1, (255,255,0))
    screen.blit(anyKey, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    
    pygame.display.flip()
    
    
    # Not a nice hack - keep going until we hit a KEYDOWN
    while True:
      for event in pygame.event.get():
	  if event.type == pygame.KEYDOWN:
	      sys.exit()
	  else:
	      pass
    