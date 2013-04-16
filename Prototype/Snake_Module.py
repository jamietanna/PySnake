#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
#import random
from random import randint


CURSE_TAIL_COLOUR = [0,0,0]#[100,100,100]

def random_rgb():
    rcolour = randint(50,255)
    bcolour = randint(50,255)
    gcolour = randint(50,255)
    return [rcolour, bcolour, gcolour]


# Static function
class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

class Snake(pygame.sprite.Sprite):
    # Private constants
    _DEFAULT_COLOUR = [255, 255, 255] # White
    _DEFAULT_SIZE = [10, 10]
    _DEFAULT_POSITION = [300, 300] # Any for now

    segments = []

    def get_sections(self):
        G = pygame.sprite.Group()
    
        for s in self.segments:
            G.add(s)

        return G

    def get_head(self):

        return self.head

    #-----PRIVATE CLASSES-------------------------------------------------------

    class _SnakeSegment(pygame.sprite.Sprite):
        def __init__(self, colour, size, position):
            # magic
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface(size)
            self.image.fill(colour)
            self.rect = self.image.get_rect()
            self.rect.topleft = position
        
        def set_colour(self, colour):
            self.image.fill(colour)

    #---------------------------------------------------------------------------

    class SnakeMove():
        # Valid directions for the snake to move
        UP = '1Y'
        DOWN = '-1Y'
        RIGHT = '1X'
        LEFT = '-1X'

        # Check direction is valid
        def SnakeMove_is_member(direction):
            if direction == Snake.SnakeMove.UP:
                return True
            elif direction == Snake.SnakeMove.DOWN:
                return True
            elif direction == Snake.SnakeMove.RIGHT:
                return True
            elif direction == Snake.SnakeMove.LEFT:
                return True

            return False

        #makes the function 'is_member' a static function
        SnakeMove_is_member = Callable(SnakeMove_is_member)

    def __init__(self, colour=None, size=None, position=None):
        pygame.sprite.Sprite.__init__(self)
        # Make sure snake valid parameters
        if colour == None:
            colour = Snake._DEFAULT_COLOUR
        if size == None:
            size = Snake._DEFAULT_SIZE
        #if size[0] != size[1]:
        #    raise Exception('Invalid tile size. Width and height must be equal.')
        if position == None:
            position = Snake._DEFAULT_POSITION

        self.color = colour
        self.size = size
        #self.head = Snake._SnakeHead(colour, size, position)
        self.segments.append(Snake._SnakeSegment(colour, size, position))

        self.head = self.segments[0]
        #self.tail = Snake._SnakeTail()

        self.curseTail = False


        for x in range(1, 5): # Initial Length
            tailposition = [(position[0] - x*size[0]), position[1]]
            #self.tail.add_tail_section(colour, size, tailposition)
            self.segments.append(Snake._SnakeSegment(colour, size, tailposition))


    def move(self, direction, frame_width, frame_height):
        # New Position
        stepSize = self.head.image.get_rect()[2] # Size of head
        newHeadPos = [self.head.rect.topleft[0], self.head.rect.topleft[1]]
        
        # This allows it to move through walls, will remove when updating next prototype
        if direction == Snake.SnakeMove.RIGHT:
            newHeadPos[0] = (newHeadPos[0]+stepSize)%frame_width
        elif direction == Snake.SnakeMove.LEFT:
            newHeadPos[0] = (newHeadPos[0]-stepSize)%frame_width
        elif direction == Snake.SnakeMove.UP:
            newHeadPos[1] = (newHeadPos[1]-stepSize)%frame_height
        elif direction  == Snake.SnakeMove.DOWN:
            newHeadPos[1] = (newHeadPos[1]+stepSize)%frame_height

        # Check to see if the snake crashes into itself
        if self.occupies_position(newHeadPos):
            return False

        # Head's old position becomes first section of tail's new position
        newTailSectionPos = self.head.rect.topleft
        # Head's position updates
        self.head.rect.topleft = newHeadPos

        # Loop through segments to move it to new position
        # ignore [0] as that's our head
        for count in range(1,len(self.segments)):
            previousTailSectionPos = self.segments[count].rect.topleft 
            # Each tail section is moved to the previous section's position, the first tail section moves to the head's previous position
            self.segments[count].rect.topleft = newTailSectionPos
            newTailSectionPos = previousTailSectionPos

        return True

    #checks if this snake's body occupies a given position
    def occupies_position(self, position):
        #parameter validation
        if position[0] == None or position[1] == None:
            return True

        if self.head.rect.topleft[0] == position[0] \
            and self.head.rect.topleft[1] == position[1]:
                return True

        for count in range(len(self.segments)):
            if self.segments[count].rect.topleft[0] == position[0] \
            and self.segments[count].rect.topleft[1] == position[1]:
                return True

        return False

    def adjust_tail_size(self, number, current_direction):
        size = self.size[0]

        if number > 0:
            for count in range(number):
            # ### TODO - randomly generate from the colour of the food eaten
                
                if self.curseTail:
                    colour = CURSE_TAIL_COLOUR
                else:
                    colour = random_rgb()
                # Randomise colour of new tail section

                lastindex = len(self.segments) - 1
                X = self.segments[lastindex].rect.topleft[0]
                Y = self.segments[lastindex].rect.topleft[1]
                
                
                # New tail section position
                if current_direction == Snake.SnakeMove.RIGHT:
                    X = X - size + (count*size)
                elif current_direction == Snake.SnakeMove.LEFT:
                    X = X + size + (count*size)
                elif current_direction == Snake.SnakeMove.UP:
                    Y = Y - size + (count*size)
                elif current_direction == Snake.SnakeMove.DOWN:
                    Y = Y + size + (count*size)

                #self.tail.add_tail_section(color, self.size, [X, Y])
                self.segments.append(Snake._SnakeSegment(colour, self.size, [X, Y]))
        else:
            for count in range(abs(number)):
                print len(self.segments)
                print self.segments
                if(len(self.segments) > 1):
                    del self.segments[-1]
                ### TODO if length 0 then die?
    
    def curse_tail(self,enable=True):
        self.curseTail = enable

        for (idx, s) in enumerate(self.segments):
            # show the head
            if idx > 0:
                if self.curseTail:
                    s.set_colour(CURSE_TAIL_COLOUR)
                else:
                    s.set_colour(random_rgb())
            else:
                s.set_colour(random_rgb())