import pygame
from PygameUILib import *
from PygameAnimationLib import *

class Browser:
    def __init__(self, x, y, w, h, custom = False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def ParseURL(self, url):
        pass

    def Visit(self, url):
        pass

    def Update(self, surface):
        pass
