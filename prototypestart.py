#!/usr/bin/env python

# import the pygame module, so you can use it
import pygame,random

from pygame.sprite import Sprite

HEIGHT=320
WIDTH=240

SLINGSHOTX=20
SLINGSHOTY=HEIGHT-100

class Pointer(Sprite):
    """
    Shows where to fire
    """
import os,sys
def load_image(name, colorkey=None):
    fullname = os.path.join('data', 'images')
    fullname = os.path.join(fullname, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
            
    return image

#class 

    
def main():# code stolen from pyong
    # create a screen surface of a given size
    screen = pygame.display.set_mode((320,240))
    # set window caption
    pygame.display.set_caption("OP JULES")
    
    # create background surface
    background = pygame.Surface([320, 240])
    background.fill(pygame.Color("black"))
    
    background = load_image('background.png', -1)
    
    
    
    
    # for y in range(0, 240, 10):
        # pygame.draw.line(background, pygame.Color("white"), (160,y), (160,y+3))
    # draw background on screen
    screen.blit(background, (0, 0))
    # display screen surface
    pygame.display.flip()
        
    # # draw a ball (color, position, radius)
    # pygame.draw.circle(screen, pygame.Color("white"), (160,120), 3)
    # # draw racket on the left
    # rectangle = pygame.Rect(10, 120-10, 4, 20) # (x, y, width, height)
    # pygame.draw.rect(screen, pygame.Color("white"), rectangle)
    
    # # draw racket on the right
    # rectangle = pygame.Rect(310-4, 120-10, 4, 20) # (x, y, width, height)
    # pygame.draw.rect(screen, pygame.Color("white"), rectangle)
    # # draw a ball (color, position, radius)
    # x, y = 160, 120
    # pygame.draw.circle(screen, pygame.Color("white"), (x,y), 3)
    
    # draw slingshot
    rectangle = pygame.Rect(SLINGSHOTX, SLINGSHOTY, 4, 20) # (x, y, width, height)
    pygame.draw.rect(screen, pygame.Color("red"), rectangle)
    
    
    
    
    
    
    
    
    # animate ball
    # pygame.draw.circle(screen, pygame.Color("black"), (x,y), 3)
    # x += random.randint(-3,3)
    # y += random.randint(-3,3)
    # pygame.draw.circle(screen, pygame.Color("white"), (x,y), 3)
    pygame.display.flip()
    
    
    # key_map = {
        # pygame.K_w: [player1.up, player1.down],
        # pygame.K_s: [player1.down, player1.up],
        # pygame.K_UP: [player2.up, player2.down],
        # pygame.K_DOWN: [player2.down, player2.up],
        # pygame.K_SPACE: [ball.serve, nop]
    # }
    
        
    # control variable for the main loop
    running = True
    
    # clock to control the game frame rate
    clock = pygame.time.Clock()
    # main game loop
    while running:
        # read events from the event queue
        # read events from the event queue
        for event in pygame.event.get():
            # on QUIT event, exit the main loop
            if event.type == pygame.QUIT:
                running = False
            # on key press
            elif event.type == pygame.KEYDOWN:
                print "DOWN: \t", event.key
            # on key release
            elif event.type == pygame.KEYUP:
                print "UP: \t",event.key
            
    
    #while True:
        #clock.tick(30)
        #pygame.display.set_caption("PONG - {0:.2f} fps".format(clock.get_fps()))
    
    
    
# if this module is executed as a script, run the main function
if __name__ == "__main__":
    main()
