from random import randint

def random_rgb():
    rcolour = randint(50,255)
    bcolour = randint(50,255)
    gcolour = randint(50,255)
    return [rcolour, bcolour, gcolour]


# Static function
class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable
