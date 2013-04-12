import pygame

class Food(pygame.sprite.Sprite):
    # Private Constants
    _DEFAULT_COLOUR = [255, 0, 0] # Red
    _DEFAULT_SIZE = [10, 10]
    def __init__(self, colour, size, position):
        # Validation
        if colour == None:
            colour = Food._DEFAULT_COLOUR
        if size == None:
            size = Food._DEFAULT_SIZE
        if position == None:
            raise Exception('Invalid position.')

        # Initalize
        self.color = colour
        self.size = size
        self.image = pygame.Surface(size)
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

class FoodBlue(Food):
    _DEFAULT_COLOUR = [0, 0, 255]
    _DEFAULT_SIZE   = [15, 15]
    def __init__(self, colour, size, position):
	super(FoodBlue, self).__init__(self._DEFAULT_COLOUR, self._DEFAULT_SIZE, position)