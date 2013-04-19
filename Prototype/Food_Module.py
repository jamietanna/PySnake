#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import random
import math
import os
import pygame
import sys


from Config import *
from Snake_Module import *
import random
from random import choice

class Food(pygame.sprite.Sprite):
    # Private Constants
    _DEFAULT_COLOUR = [255, 174, 201] # Pink
    _DEFAULT_SIZE = [10, 10]
    def __init__(self, colour, size, effect, position):
        
        pygame.sprite.Sprite.__init__(self)
        
        # Validation
        if colour == None:
            colour = Food._DEFAULT_COLOUR
        if size == None:
            size = Food._DEFAULT_SIZE
        if position == None:
            raise Exception('Invalid position.')
        if effect == None:
            effect = dict()
        
        if 'size' not in effect:
            effect['size']  = 2
        if 'score' not in effect:
            effect['score'] = 1
        if 'curse' not in effect:
            effect['curse'] = False
        if 'removeKiller' not in effect:
            effect['removeKiller'] = False
        if 'freezeBall' not in effect:
            effect['freezeBall'] = False
        if 'removeStandard' not in effect:
            effect['removeStandard'] = False
        if 'spawnKiller' not in effect:
            effect['spawnKiller'] = False
        if 'spawnStandard' not in effect:
            effect['spawnStandard'] = False


        self.properties = dict()

        # Initalize
        self.properties['colour'] = colour
        self.properties['size']   = size
        self.properties['effect'] = effect
        self.properties['time']   = 4 * FPS # -1 = infinite
        self.properties['autoRespawn'] = True
        self.properties['type'] = self.__class__.__name__

        if self.FILENAME != None:
            path = os.path.join(os.getcwd(), self.FILENAME)
            self.image = pygame.image.load(path)
            # resize it so it's better
            self.image = pygame.transform.scale(self.image, size)
        else:
            self.image = pygame.Surface(size)
            self.image.fill(colour)

        self.rect = self.image.get_rect()
        self.rect.topleft = position
        

    def get_properties(self):
        return self.properties

    def expire(self):
        if self.properties['time'] > 0:
            self.properties['time'] -= 1 # decrement
            return (self.properties['time'] <= 0)
        else:
            # -1 indicates infinite
            return False


class FoodNormal(Food):
    _DEFAULT_COLOUR = [255, 0, 0] # Red
    _DEFAULT_SIZE = [15, 15]
    
    FILENAME = 'food_5.png'
    
    def __init__(self, colour, size, effect, position):
        
        """BASE BANANAS"""
        
        effect = dict()
        effect['score']  = +2
        effect['size']   = +2
        effect['spawnStandard'] = True
        super(FoodNormal, self).__init__(self._DEFAULT_COLOUR, self._DEFAULT_SIZE, effect, position)

class FoodSuper(Food):
    _DEFAULT_COLOUR = [0, 0, 255] # Dark blue
    _DEFAULT_SIZE   = [20, 20]
    
    FILENAME = 'lemon.png'
    
    def __init__(self, colour, size, effect, position):
        
        """LEMON OF LENGTH"""
        
        effect = dict()
        effect['size']  = +3
        effect['score'] = +5
        effect['spawnKiller'] = True
        super(FoodSuper, self).__init__(self._DEFAULT_COLOUR, self._DEFAULT_SIZE, effect, position)

        # self.rect = pygame.Rect((position), (10, 20))
        # self.rect.topleft = position

class FoodCurse(Food):
    _DEFAULT_COLOUR = BACKGROUND_COLOUR
    _DEFAULT_SIZE   = [20, 20]
    
    FILENAME = 'food_4.png'

    def __init__(self, colour, size, effect, position):
        
        """BERRIES OF BANE"""

        effect = dict()
        effect['curse'] = True
        effect['size']  = +2
        effect['score'] = -5
        super(FoodCurse, self).__init__(self._DEFAULT_COLOUR, self._DEFAULT_SIZE, effect, position)
        self.properties['autoRespawn'] = False
        self.properties['time'] = -1

class FoodMysterious(Food):
    _DEFAULT_COLOUR = [0, 250, 0] # Green
    _DEFAULT_SIZE   = [15, 15]

    RANDOM_MAX = 20

    FILENAME = 'food_1.png'
    
    def __init__(self, colour, size, effect, position):
        
        """MYSTERY MELON"""

        effect = dict()
        x = random.randint(0,self.RANDOM_MAX)

        # 50% chance
        for e in ['removeStandard']:
            effect[e] = (x <= (self.RANDOM_MAX / 2))

        # 1/4 chance
        for e in ['spawnStandard', 'removeKiller']:
            effect[e] = (x >= (self.RANDOM_MAX / 4))

        # 1/20 chance
        for e in ['spawnKiller']:
            effect[e] = (x == (self.RANDOM_MAX / 20))

        if (x % 2) == 0:
            # * 20 can give quite a large amount of freeze time
            effect['freezeBall'] = x * 20


        effect['score'] = x / 2
        if (x % 2) == 0:
            effect['score'] = - (effect['score'] / 2)

        
        # probablity way too high
        # need to be synched together
        # maybe do groupings instead of individual ifs

        effect['curse'] = False
        effect['size']  = 0
        super(FoodMysterious, self).__init__(self._DEFAULT_COLOUR, self._DEFAULT_SIZE, effect, position)
        self.properties['autoRespawn'] = False
        self.properties['time'] *= 2
        

def make_food(snake, foodType='FoodNormal', colour=None, size=None, effect=None):
    #global snake

    if foodType == None:
        foodType = 'FoodNormal'

    # Keep food within decent boundaries
    # Use eval in case we're spawning a different foodType of food


    foodTypeX = eval(foodType + '._DEFAULT_SIZE[0]')
    foodTypeY = eval(foodType + '._DEFAULT_SIZE[1]')

    hbound = DEFAULT_SCREEN_SIZE[0] / (foodTypeX - 1)
    vbound = DEFAULT_SCREEN_SIZE[1] /  (foodTypeY- 1)
    (X, Y) = (None, None)

    # ### TODO check that food doesn't spawn over another piece of food

    # Make sure the food doesn't spawn over the snakes position

    #### TODO [0,1] -> X,Y

    while snake.occupies_position([X, Y]) == True:
        X = random.randint(0, hbound) * eval(foodType + '._DEFAULT_SIZE[0]')
        Y = random.randint(0, vbound) * eval(foodType + '._DEFAULT_SIZE[1]')

    return eval(foodType + '(' + str(colour) + ', ' + str(size) + ', ' + str(effect) + ', ['+str(X)+', '+str(Y)+'])')
