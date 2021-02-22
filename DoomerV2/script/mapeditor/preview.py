import pygame
import script.general.loader as ld
from SETTINGS import SETTINGS

class Preview(pygame.sprite.Sprite):
    def __init__(self, itemlist, pos_tupple):
        pygame.sprite.Sprite.__init__(self)
        imglist = []
        for item in itemlist:
            imglist.append(pygame.transform.scale(ld.loadimage(SETTINGS.FOLDER, "images/gameobjects", item + ".png"),(50,50)))
        self.__itemdict = dict(zip(itemlist, imglist))
        self.__pos = pos_tupple
        self.__square = pygame.Rect(*pos_tupple, 50, 50)

    def update(self, target_surface, item=""):
        if item in self.__itemdict:
            img = self.__itemdict[item]
            target_surface.blit(img, self.__pos)
        pygame.draw.rect(target_surface, (0,0,0), self.__square, 1)