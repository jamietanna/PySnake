import pygame

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
            effect['size']  = 1
            effect['score'] = 1
        else:
            if 'size' not in effect:
                effect['size']  = 1
            if 'score' not in effect:
                effect['score'] = 1


        # Initalize
        self.colour = colour
        self.size   = size
        self.effect = effect
        # about 4 seconds
        self.time   = 160000000       # non editable for the time being

        self.image = pygame.Surface(size)
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.time = 150

    def get_properties(self):
        prop = dict()
        prop['colour']  = self.colour
        prop['size']    = self.size
        prop['type']    = self.__class__.__name__
        prop['effect']  = dict()
        ### TODO : MAKE ATTRIBUTE
        prop['effect']  = self.effect

        return prop

    def expire(self):
        self.time -= 1 # decrement
        if self.time <= 0:
            return True
        else:
            return False


class FoodNormal(Food):
    _DEFAULT_COLOUR = [255, 0, 0] # Red
    _DEFAULT_SIZE = [10, 10]
    def __init__(self, colour, size, effect, position):
        effect = dict()
        effect['score']  = 1
        super(FoodNormal, self).__init__(self._DEFAULT_COLOUR, self._DEFAULT_SIZE, effect, position)



class FoodBlue(Food):
    _DEFAULT_COLOUR = [0, 0, 255] # Dark blue
    _DEFAULT_SIZE   = [15, 15]
    def __init__(self, colour, size, effect, position):
        effect = dict()
        effect['size']  = 2
        effect['score'] = 0
        super(FoodBlue, self).__init__(self._DEFAULT_COLOUR, self._DEFAULT_SIZE, effect, position)