import pygame
import numpy as np
import script.general.loader as ld
from SETTINGS import SETTINGS

class Tile(pygame.sprite.Sprite):
    def __init__(self, type_as_str, pos_as_tupple):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos_as_tupple
        self.__img = pygame.transform.scale(ld.loadimage(SETTINGS.FOLDER, "images/mapeditor", type_as_str + ".png"),(10,10))
        self.value = SETTINGS.MAPITEMS[type_as_str]
        self.__rect = self.__img.get_rect()
        self.__size = self.__img.get_size()

    def update(self,target_surface):
        target_surface.blit(self.__img, self.pos)