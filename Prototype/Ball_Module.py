#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import math
import os
import pygame
import sys
from Config import *

NUMBER_OF_BALLS = 5
BALL_SPEED = 0.035
BALL_SIZE = 10


def appendBallToList(listOfBalls):
    x = random.randint(BALL_SIZE, SCREEN_WIDTH)
    y = random.randint(BALL_SIZE, SCREEN_HEIGHT)
    ball = Ball((x, y))
    listOfBalls.append(ball)



class Ball(pygame.sprite.Sprite):

    FILENAME = 'ball.png'

    def __init__(self, (x, y)):
        pygame.sprite.Sprite.__init__(self)
    
       ### TESTING HACK FOR EASE OF USE

        if os.name == 'nt':
            path = os.path.join('C:\\','Users','Mart','Documents','FSE','Prototype', self.FILENAME)
        else:
            path = os.path.join(os.getcwd(), self.FILENAME)
        

        self.image = pygame.image.load(path)
        #self.image = pygame.image.load(os.path.join(os.getcwd(), "ball.png"))
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

    # probably need to replace this with a better function using the sprite collision detection
    def collide(self, x, y):
        if x < self.x - self.size or x > self.x + self.size:
            return False
        elif y < self.y - self.size or y > self.y + self.size:
            return False
        else:
            return True



class BallStandard(Ball):

    FILENAME = 'ball.png'

    def __init__(self, (x, y)):
        super(BallStandard, self).__init__((x,y))

    def collision(self, ball):
        dx = self.x - ball.x
        dy = self.y - ball.y
        dist = math.hypot(dx, dy)
        if dist < self.size + ball.size:
            ### Is there a way to cut this down?
            
            tangent = math.atan2(dy, dx)
            angle = 0.5 * math.pi + tangent
            
            angle1 = 2*tangent - self.angle
            angle2 = 2*tangent - ball.angle
            
            self.x += math.sin(angle)
            self.y -= math.cos(angle)
            self.angle = angle1
            #self.display()
            
            ball.x -= math.sin(angle)
            ball.y += math.cos(angle)
            ball.angle = angle2
            #ball.display()

class BallKiller(Ball):

    FILENAME = 'ball2.png'

    def __init__(self, (x, y)):
        super(BallKiller, self).__init__((x,y))

    def collision(self, ball):
        dx = self.x - ball.x
        dy = self.y - ball.y
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent
        self.x += math.sin(angle)
        self.y -= math.cos(angle)
        ball.x -= math.sin(angle)
        ball.y += math.cos(angle)
        