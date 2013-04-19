#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import os
import pygame
import sys
from Config import *

#BALL_SPEED = 0.035
#BALL_SIZE = 10
## Moved to config file

def appendBallToList(listOfBalls):
    x = random.randint(BALL_SIZE, SCREEN_WIDTH)
    y = random.randint(BALL_SIZE, SCREEN_HEIGHT)
    ball = Ball((x, y))
    listOfBalls.append(ball)

class Ball(pygame.sprite.Sprite):

    FILENAME = 'ball.png'

    def __init__(self, (x, y)):
        pygame.sprite.Sprite.__init__(self)
    
        # ### TESTING HACK FOR EASE OF USE

        #  if os.name == 'nt':
        #      path = os.path.join('C:\\','Users','Mart','Documents','FSE','Prototype', self.FILENAME)
        #  else:
        path = os.path.join(os.getcwd(), self.FILENAME)
        
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.centerx, self.rect.centery = [x,y]
        self.speed = BALL_SPEED
        self.angle = random.uniform(0, math.pi * 2)
        self.size = BALL_SIZE


    def display(self):
        self.rect.centerx, self.rect.centery = [self.x,self.y]

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def bounce(self):
        if self.x > SCREEN_WIDTH - self.size:
            self.x = 2 * (SCREEN_WIDTH - self.size) - self.x
            self.angle = -self.angle
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = -self.angle

        if self.y > SCREEN_HEIGHT - self.size:
            self.y = 2 * (SCREEN_HEIGHT - self.size) - self.y
            self.angle = math.pi - self.angle
        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle



class BallStandard(Ball):

    FILENAME = 'ball.png'

    def __init__(self, (x, y)):
        super(BallStandard, self).__init__((x,y))

    # used for collisions with a killer ball
    def collision(self, ball):
        (dx,dy) = (self.x - ball.x, self.y - ball.y) 
        contact = math.hypot(dx, dy)
        if contact < self.size + ball.size:
    
            tangent = math.atan2(dy, dx)
            collision_angle = 0.5 * math.pi + tangent
            
            new_self_angle = 2*tangent - self.angle
            new_ball_angle = 2*tangent - ball.angle
            
            self.x += math.sin(collision_angle)
            self.y -= math.cos(collision_angle)
            ball.x -= math.sin(collision_angle)
            ball.y += math.cos(collision_angle)
            (self.angle, ball.angle) = (new_self_angle, new_ball_angle)
 

class BallKiller(Ball):

    FILENAME = 'ball2.png'

    def __init__(self, (x, y)):
        super(BallKiller, self).__init__((x,y))
        self.speed = BALL_SPEED * 1.5