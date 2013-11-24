#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame import *
from Food_Module import *
from Snake_Module import *
from Ball_Module import *
import random
from random import choice
from Game import *


global gameOver
global direction
global score
global userEscape

G = Game()

running = True
while running:
    G.update()
