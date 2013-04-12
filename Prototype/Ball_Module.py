#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import math
import os
import pygame
import sys


BALL_COLOUR = (0, 0, 255)
NUMBER_OF_BALLS = 1
BALL_SPEED = 5
BALL_SIZE = 10
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DEFAULT_SCREEN_SIZE = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(DEFAULT_SCREEN_SIZE)

class Ball(pygame.sprite.Sprite):

    def __init__(self, (x, y)):
        pygame.sprite.Sprite.__init__(self)
        path = os.path.join('C:\\','Users','Mart','Documents','FSE','Prototype', 'ball.png')
        #self.image = pygame.image.load(path)
        self.image = pygame.image.load(os.path.join(os.getcwd(), "ball.png"))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.centerx, self.rect.centery = [x,y]
        self.speed = BALL_SPEED
        self.angle = 45
        self.size = 10

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

    def collide(self, x, y):
        if x < self.x - self.size or x > self.x + self.size:
            return False
        elif y < self.y - self.size or y > self.y + self.size:
            return False
        else:
            return True

def appendBallToList(listOfBalls):
    x = random.randint(BALL_SIZE, SCREEN_WIDTH)
    y = random.randint(BALL_SIZE, SCREEN_HEIGHT)
    ball = Ball((x, y), BALL_SIZE)
    ball.speed = 1
    ball.angle = random.uniform(0, math.pi * 2)
    listOfBalls.append(ball)