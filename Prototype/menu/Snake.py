#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
# import Food_Module
# import Snake_Module
# import Ball_Module
# from random import choice
import Game_Module
import Config

global gameOver
global direction
global score
# global userEscape
try:
    Config.screen
except:
    Config.screen = pygame.display.set_mode(Config.DEFAULT_SCREEN_SIZE)    



G = Game_Module.Game(None)


running = True
while running:
    G.update()
    if G.gameOver:
    	break
