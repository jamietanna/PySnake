import pygame
import random
from random import randint

# Static function
class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

class Snake(pygame.sprite.Sprite):
    # Private constants
    _DEFAULT_COLOUR = [255, 255, 255] # White
    _DEFAULT_SIZE = [10, 10]
    _DEFAULT_POSITION = [100, 100] # Any for now

    #-----PRIVATE CLASSES-------------------------------------------------------
    class _SnakeTail(pygame.sprite.Sprite):
        def __init__(self):
            self.sections = []

        def add_tail_section(self, colour, size, position):
            section = pygame.Surface(size)
            section.fill(colour)
            rect = section.get_rect()
            rect.topleft = position
            self.sections.append({'image':section, 'rect':rect})

    class _SnakeHead(pygame.sprite.Sprite):
        def __init__(self, colour, size, position):
            self.image = pygame.Surface(size)
            self.image.fill(colour)
            self.rect = self.image.get_rect()
            self.rect.topleft = position
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

    def __init__(self, colour, size, position):
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
        self.head = Snake._SnakeHead(colour, size, position)
        self.tail = Snake._SnakeTail()

        for x in range(1, 5): # Initial Length
            tailposition = [(position[0] - x*size[0]), position[1]]
            self.tail.add_tail_section(colour, size, tailposition)

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

        # Loop through tail to move it to new position
        for count in range(len(self.tail.sections)):
            previousTailSectionPos = self.tail.sections[count]['rect'].topleft 
            # Each tail section is moved to the previous section's position, the first tail section moves to the head's previous position
            self.tail.sections[count]['rect'].topleft = newTailSectionPos
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

        for count in range(len(self.tail.sections)):
            if self.tail.sections[count]['rect'].topleft[0] == position[0] \
            and self.tail.sections[count]['rect'].topleft[1] == position[1]:
                return True

        return False

    def lengthen_tail(self, number, current_direction):
        size = self.size[0] # make new tail section same size as previous tail sections

        for count in range(number):
	    # ### TODO - randomly generate from the colour of the food eaten
            rcolour = randint(50,255)
            bcolour = randint(50,255)
            gcolour = randint(50,255)
            color = [rcolour, bcolour, gcolour]
            # Randomise colour of new tail section

            lastindex = len(self.tail.sections) - 1
            X = self.tail.sections[lastindex]['rect'].topleft[0]
            Y = self.tail.sections[lastindex]['rect'].topleft[1]

            # New tail section position
            if current_direction == Snake.SnakeMove.RIGHT:
                X = X - size + (count*size)
            elif current_direction == Snake.SnakeMove.LEFT:
                X = X + size + (count*size)
            elif current_direction == Snake.SnakeMove.UP:
                Y = Y - size + (count*size)
            elif current_direction == Snake.SnakeMove.DOWN:
                Y = Y + size + (count*size)

            self.tail.add_tail_section(color, self.size, [X, Y])