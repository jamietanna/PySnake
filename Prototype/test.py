#!/usr/bin/python

import random
import math
import os
import pygame
import sys

class BallClass(pygame.sprite.Sprite):
    def __init__(self, image_file, speed, location = [0, 0]):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed
        
    def move(self):
        global points, score_text
        self.rect = self.rect.move(self.speed)
        # bounce off the sides of the window
        if self.rect.left < 0 or self.rect.right > screen.get_width():
            self.speed[0] = -self.speed[0]
            if self.rect.top < screen.get_height():
                hit_wall.play()
        
        # bounce off the top of the window
        if self.rect.top <= 0 :
            self.speed[1] = -self.speed[1]
            points = points + 1
            score_text = font.render(str(points), 1, (0, 0, 0))
            get_point.play()
