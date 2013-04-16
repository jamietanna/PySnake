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
            effect['size']  = 1
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
        self.properties['effect']= effect
        # about 4 seconds
        #self.time   = 1600000       # non editable for the time being
                                    # -1 = inf
        self.properties['time']   = -1
        self.properties['autoRespawn'] = True
        self.properties['type'] = self.__class__.__name__

        self.image = pygame.Surface(size)
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def get_properties(self):
        # prop = dict()
        # prop['colour']  = self.colour
        # prop['size']    = self.size
        # prop['type']    = self.__class__.__name__
        # prop['effect']  = dict()
        # ### TODO : MAKE ATTRIBUTE
        # prop['effect']  = self.effect

        # return prop
        return self.properties

    def expire(self):
        if self.properties['time'] > 0:
            self.properties['time'] -= 1 # decrement
            if self.properties['time'] <= 0:
                return True
            else:
                return False
        else:
            # -1 indicates infinite
            return False


class FoodNormal(Food):
    _DEFAULT_COLOUR = [255, 0, 0] # Red
    _DEFAULT_SIZE = [10, 10]
    def __init__(self, colour, size, effect, position):
        effect = dict()
        effect['score']  = 1
        effect['size']   = 2
        effect['spawnKiller'] = True
        super(FoodNormal, self).__init__(self._DEFAULT_COLOUR, self._DEFAULT_SIZE, effect, position)

class FoodBlue(Food):
    _DEFAULT_COLOUR = [0, 0, 255] # Dark blue
    _DEFAULT_SIZE   = [15, 15]
    def __init__(self, colour, size, effect, position):
        effect = dict()
        effect['size']  = 2
        effect['score'] = 0
        effect['spawnStandard'] = True
        super(FoodBlue, self).__init__(self._DEFAULT_COLOUR, self._DEFAULT_SIZE, effect, position)

class FoodCurse(Food):
    _DEFAULT_COLOUR = [20, 20, 20] # BACKGROUND_COLOUR
    _DEFAULT_SIZE   = [30, 30]
    def __init__(self, colour, size, effect, position):
        effect = dict()
        effect['curse'] = True
        effect['size']  = 2
        effect['score'] = -5
        super(FoodCurse, self).__init__(self._DEFAULT_COLOUR, self._DEFAULT_SIZE, effect, position)
        self.properties['autoRespawn'] = False
        print "TODO: FoodCurse expiry"

class FoodMysterious(Food):
    _DEFAULT_COLOUR = [0, 250, 0] # Green
    _DEFAULT_SIZE   = [10, 10]
    def __init__(self, colour, size, effect, position):
        effect = dict()
        x = random.randint(0,20)

        if x <= 5: # 1/4 chance
            spawnStandard = True
        else:
            spawnStandard = False

        if x == 20: # 1/20 chance
            spawnKiller = True
        else:
            spawnKiller = False

        if x >= 10: # 1/2 chance
            freezeBall = True
        else: 
            freezeBall = False 

        if x >= 15: # 1/4 chance
            removeKiller = True
        else: 
            removeKiller = False

        if x <= 10: # 1/2 chance
            removeStandard = True
        else:
            removeStandard = False

        # probablity way too high
        # need to be synched together
        # maybe do groupings instead of individual ifs

        effect['spawnStandard'] = spawnStandard
        effect['spawnKiller'] = spawnKiller
        effect['curse'] = False
        effect['size']  = 0
        effect['score'] = 0 # make it random?
        effect['freezeBall'] = freezeBall
        effect['removeKiller'] = removeKiller
        effect['removeStandard'] = removeStandard
        super(FoodMysterious, self).__init__(self._DEFAULT_COLOUR, self._DEFAULT_SIZE, effect, position)
        self.properties['autoRespawn'] = False
        print "TODO: FoodCurse expiry"

def make_food(snake, foodType='FoodNormal', colour=None, size=None, effect=None):
    print "TODO: MAKE make_food(snake, foodType, properties)"
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
