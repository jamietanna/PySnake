#! /usr/bin/env python

# Move a worm across the screen. Beware of borders and self!

import pygame
import random

class Worm:
    """ A worm. """

    def __init__(self, surface):
        self.surface = surface
        self.x = surface.get_width() / 2
        self.y = surface.get_height() / 2
        self.len = 50
        self.vx = 0
        self.vy = -1
        self.body_list=[[self.x, self.y +i] for i in range (self.len)]
        self.crashed = False
        self.colour = 255, 255, 255
        self.speed = 1

    def eat(self):
        self.len +=50
        self.speed += 1

    def key_event(self, event):
        """ Handle key events that affect the worm. """
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
        """ Move the worm. """
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed
        
        if [self.x,self.y] in self.body_list:
            self.crashed = True
            
            
        self.body_list.insert(0, [self.x, self.y])
        
        if len(self.body_list) > self.len:
            self.body_list.pop()
        
    def draw(self):
        for i in self.body_list:
            pygame.draw.circle(self.surface,self.colour, (i[0],i[1]), 2)

class Food:
    def __init__(self, surface):
        self.surface = surface
        self.x = random.randint(0, (surface.get_width() - 10))
        self.y = random.randint(0, (surface.get_height() - 10))
        self.color = 255, 255, 255

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




# Dimensions.
width = 640 
height = 400

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


# Our worm.
worm = Worm(screen)
food = Food(screen)
running = True

while running:
    screen.fill((0, 0, 0))
    worm.move()
    worm.draw()
    food.draw()

    if worm.crashed:
        running = False
    elif worm.x <= 0 or worm.x >= width-1:
        running = False
    elif worm.y <= 0 or worm.y >= height-1:
        print "Crash!"
        running = False
    elif food.check(worm.x,worm.y):
        worm.eat()
        food.erase()
        food = Food(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            worm.key_event(event)

    pygame.display.flip()
    clock.tick(120)
