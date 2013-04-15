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
        
        if 'size' not in effect:
            effect['size']  = 1
        if 'score' not in effect:
            effect['score'] = 1
        if 'curse' not in effect:
            effect['curse'] = False


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
            return False


class FoodNormal(Food):
    _DEFAULT_COLOUR = [255, 0, 0] # Red
    _DEFAULT_SIZE = [10, 10]
    def __init__(self, colour, size, effect, position):
        effect = dict()
        effect['score']  = 1
        effect['size']   = 2
        super(FoodNormal, self).__init__(self._DEFAULT_COLOUR, self._DEFAULT_SIZE, effect, position)



class FoodBlue(Food):
    _DEFAULT_COLOUR = [0, 0, 255] # Dark blue
    _DEFAULT_SIZE   = [15, 15]
    def __init__(self, colour, size, effect, position):
        effect = dict()
        effect['size']  = 2
        effect['score'] = 0
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