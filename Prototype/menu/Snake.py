#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import Food_Module
import Snake_Module
import Ball_Module
from random import choice
import Game_Module
import Config

global gameOver
global direction
global score
global userEscape

G = Game_Module.Game(None)

running = True
while running:
    G.update()
